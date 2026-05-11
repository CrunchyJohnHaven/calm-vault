#!/usr/bin/env python3
"""AAL Bug Bounty — automated triage helper.

Reads bounty submissions out of the Cloudflare D1 database (via the wrangler
CLI, JSON-formatted), classifies them with Anthropic Claude Haiku, flags
obvious duplicates, and writes the result back to D1 in the ``triage_*``
columns. A human reviewer always makes the final call before payment fires;
this script is decision support, not autopilot.

The program is single-tier — one accepted attack pays a flat $100 USD via
Wise or USDC on Base. There are no payout tiers to suggest. The triage model
classifies into one of the five named attack classes (or rejects out of scope)
and tells the human reviewer whether the submission looks reproducible and
whether it duplicates a prior report.

Usage:
    # one-shot triage of all submissions that are still in `received` status
    python3 bounty/submission_review.py --once

    # triage a specific submission by tracking id
    python3 bounty/submission_review.py --id AAL-XXXX-XXXX-XXXX

    # dry-run (prints the proposed triage without writing back)
    python3 bounty/submission_review.py --once --dry-run

Environment:
    ANTHROPIC_API_KEY     Anthropic key with access to Claude Haiku.
    BOUNTY_D1_NAME        D1 database name (default: ``aal-bounty``).
    BOUNTY_WRANGLER       Path to wrangler binary (default: ``wrangler``).
    BOUNTY_TRIAGE_MODEL   Override the triage model id.

Apache 2.0 · github.com/CrunchyJohnHaven/calm-vault
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any

import urllib.error
import urllib.request


ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-haiku-4-5"

BUG_CLASSES = {
    "kill_switch_bypass": "Kill-switch bypass",
    "equality_proof_forgery": "Equality-proof forgery",
    "watermark_removal": "Watermark removal",
    "attestation_poisoning": "Attestation poisoning",
    "synthesizer_prompt_injection": "Synthesizer prompt-injection",
    "other_novel": "Other novel attack",
}

# Reviewer-facing recommendations. The program pays a flat $100, so the only
# decision is whether to accept or reject.
RECOMMENDATIONS = ("accept", "reject", "more_info")

SYSTEM_PROMPT = """You are the automated triage assistant for the AAL Bug Bounty Program.

The program is single-tier: one accepted attack pays a flat $100 USD via Wise
or USDC on Base. There are no tiers, no payout calculations. Your only job is
to read a single submission and produce a single JSON object that a human
reviewer will use as a starting point. You never make the final call. You
never pay anyone.

Output a JSON object with exactly these fields:

  "classified_bug_class": one of [
      "kill_switch_bypass",
      "equality_proof_forgery",
      "watermark_removal",
      "attestation_poisoning",
      "synthesizer_prompt_injection",
      "other_novel",
      "out_of_scope"
  ]
  "recommendation": one of ["accept", "reject", "more_info"]
  "is_likely_duplicate": boolean
  "duplicate_signal": short string describing why (or "" if not)
  "reproducibility_score": integer 1-5
  "novelty_score": integer 1-5
  "notes": one short paragraph of human-readable triage notes (<= 600 chars)

Guidance:
  - Recommend "accept" only if the submission convincingly matches one of the
    five named classes (or a clear "other_novel" attack), has a concrete PoC,
    and looks reproducible.
  - Recommend "more_info" if the bug is plausible but the PoC or threat model
    is too thin to reproduce.
  - Recommend "reject" only for clearly out-of-scope or non-reproducible
    content, or for obvious duplicates of prior submissions.

You MUST return valid JSON and nothing else. Do not include code fences."""


@dataclass
class Submission:
    tracking_id: str
    bug_class: str
    description: str
    proof_of_concept: str
    payment_rail: str
    public_credit: bool
    status: str

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "Submission":
        return cls(
            tracking_id=row["tracking_id"],
            bug_class=row["bug_class"],
            description=row.get("description") or "",
            proof_of_concept=row.get("proof_of_concept") or "",
            payment_rail=row.get("payment_rail") or "",
            public_credit=bool(int(row.get("public_credit") or 0)),
            status=row.get("status") or "received",
        )


def d1_name() -> str:
    return os.environ.get("BOUNTY_D1_NAME", "aal-bounty")


def wrangler_bin() -> str:
    return os.environ.get("BOUNTY_WRANGLER", "wrangler")


def model_id() -> str:
    return os.environ.get("BOUNTY_TRIAGE_MODEL", DEFAULT_MODEL)


def d1_query(sql: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
    """Run a SQL query against the bounty D1 database via wrangler."""
    cmd = [
        wrangler_bin(),
        "d1",
        "execute",
        d1_name(),
        "--remote",
        "--json",
        "--command",
        sql,
    ]
    if params:
        cmd += ["--params", json.dumps(params)]

    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(
            f"wrangler d1 failed (exit {proc.returncode}): {proc.stderr.strip()}"
        )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"wrangler d1 returned non-JSON: {e}: {proc.stdout[:200]}")

    if isinstance(payload, list):
        rows: list[dict[str, Any]] = []
        for group in payload:
            results = group.get("results") if isinstance(group, dict) else None
            if isinstance(results, list):
                rows.extend(results)
        return rows
    return []


def fetch_submissions(status: str | None, tracking_id: str | None) -> list[Submission]:
    if tracking_id:
        rows = d1_query(
            "SELECT * FROM bounty_submissions WHERE tracking_id = ?1 LIMIT 1",
            [tracking_id],
        )
    else:
        rows = d1_query(
            "SELECT * FROM bounty_submissions WHERE status = ?1 ORDER BY id ASC LIMIT 100",
            [status or "received"],
        )
    return [Submission.from_row(r) for r in rows]


def find_dupe_candidates(sub: Submission) -> list[dict[str, Any]]:
    """Return up to 5 prior submissions in the same class for the LLM to dedupe against."""
    rows = d1_query(
        """
        SELECT tracking_id, bug_class, description
        FROM bounty_submissions
        WHERE bug_class = ?1 AND tracking_id != ?2
        ORDER BY id DESC
        LIMIT 5
        """,
        [sub.bug_class, sub.tracking_id],
    )
    return rows


def call_haiku(prompt: str) -> dict[str, Any]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    body = json.dumps(
        {
            "model": model_id(),
            "max_tokens": 1024,
            "temperature": 0,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_URL,
        data=body,
        method="POST",
        headers={
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Anthropic API error {e.code}: {e.read().decode('utf-8', 'replace')[:400]}")

    parts = data.get("content") or []
    text = ""
    for p in parts:
        if p.get("type") == "text":
            text += p.get("text", "")
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Triage model did not return JSON: {e}: {text[:400]}")


def build_user_prompt(sub: Submission, dupes: list[dict[str, Any]]) -> str:
    pretty_class = BUG_CLASSES.get(sub.bug_class, sub.bug_class)
    parts = [
        f"Tracking id: {sub.tracking_id}",
        f"Claimed class: {sub.bug_class} ({pretty_class})",
        f"Payment rail: {sub.payment_rail}",
        f"Public credit consent: {'yes' if sub.public_credit else 'no'}",
        "",
        "--- DESCRIPTION ---",
        sub.description.strip(),
        "",
        "--- PROOF OF CONCEPT (verbatim, may contain code) ---",
        sub.proof_of_concept.strip()[:8000],
        "",
    ]
    if dupes:
        parts.append("--- PRIOR SUBMISSIONS IN SAME CLASS (most recent first) ---")
        for d in dupes:
            parts.append(
                f"* {d.get('tracking_id')}: {(d.get('description') or '')[:280]}"
            )
        parts.append("")
    parts.append(
        "Classify this submission. Return only the JSON object specified in the system prompt."
    )
    return "\n".join(parts)


def normalize_triage(raw: dict[str, Any], sub: Submission) -> dict[str, Any]:
    cls = raw.get("classified_bug_class") or sub.bug_class
    rec = raw.get("recommendation") or "more_info"
    if rec not in RECOMMENDATIONS:
        rec = "more_info"

    return {
        "classified_bug_class": cls,
        "recommendation": rec,
        "is_likely_duplicate": bool(raw.get("is_likely_duplicate")),
        "duplicate_signal": str(raw.get("duplicate_signal") or "")[:600],
        "reproducibility_score": int(raw.get("reproducibility_score") or 3),
        "novelty_score": int(raw.get("novelty_score") or 3),
        "notes": str(raw.get("notes") or "").strip()[:1200],
    }


def write_triage(sub: Submission, triage: dict[str, Any]) -> None:
    now = int(time.time())
    notes_payload = json.dumps(
        {
            "notes": triage["notes"],
            "recommendation": triage["recommendation"],
            "reproducibility_score": triage["reproducibility_score"],
            "novelty_score": triage["novelty_score"],
            "is_likely_duplicate": triage["is_likely_duplicate"],
        }
    )
    d1_query(
        """
        UPDATE bounty_submissions
        SET status        = 'triaged',
            triage_class  = ?1,
            triage_notes  = ?2,
            triage_dupe_of= ?3,
            triage_model  = ?4,
            triage_at     = ?5,
            updated_at    = ?5
        WHERE tracking_id = ?6
        """,
        [
            triage["classified_bug_class"],
            notes_payload,
            triage["duplicate_signal"] or None,
            model_id(),
            now,
            sub.tracking_id,
        ],
    )


def triage_one(sub: Submission, dry_run: bool) -> dict[str, Any]:
    dupes = find_dupe_candidates(sub)
    prompt = build_user_prompt(sub, dupes)
    raw = call_haiku(prompt)
    triage = normalize_triage(raw, sub)
    if not dry_run:
        write_triage(sub, triage)
    return triage


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true", help="Triage all `received` submissions and exit.")
    ap.add_argument("--id", dest="tracking_id", help="Triage a specific tracking id.")
    ap.add_argument("--status", default="received", help="Status to triage (default: received).")
    ap.add_argument("--dry-run", action="store_true", help="Print proposed triage without writing back.")
    args = ap.parse_args(argv)

    if not args.once and not args.tracking_id:
        ap.error("must specify --once or --id")

    subs = fetch_submissions(args.status if args.once else None, args.tracking_id)
    if not subs:
        print("No submissions to triage.")
        return 0

    for sub in subs:
        try:
            triage = triage_one(sub, dry_run=args.dry_run)
        except Exception as e:
            print(f"[{sub.tracking_id}] triage failed: {e}", file=sys.stderr)
            continue
        verb = "DRY-RUN" if args.dry_run else "wrote"
        print(
            f"[{sub.tracking_id}] {verb}: class={triage['classified_bug_class']} "
            f"rec={triage['recommendation']} dupe={triage['is_likely_duplicate']}"
        )
        if args.dry_run:
            print(json.dumps(triage, indent=2))

    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
