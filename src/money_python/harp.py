#!/usr/bin/env python3
"""
HARP — Halt-and-Rescue Protocol.

Provides:
  - Distributed alarm broadcast (any attester can submit a signed HaltAttestation).
  - K-of-N halt-quorum (K independent halt claims within Δt → "concurred halt").
  - Credential-grant revocation: emits a `revoke.sh` line that calls
    calm_vault.py revoke-agent on every agent identity tied to the subject.
  - Hot-standby checkpoint stub: `pickup_rescue(halted_subject_id)` returns the
    v2 marker; v1 ships the halt only.

A HaltAttestation is a Claim with claim_type="halt" PLUS extra fields packed
into the claim_text (a JSON-encoded sidecar). We use a small wrapper rather
than extending the Claim schema so the OBAC chain format stays uniform.

Extra fields (packed in claim_text after the prefix HALT:):
  - halts_subject: str  (the subject being halted)
  - violation_layer: str  (which guarantee was breached, e.g. "alignment-maxim")
  - violation_evidence: list[str]  (evidence pointer URIs)

False-alarm rejection: a halt from a low-reliability attester (reliability < 0.5)
does not count toward quorum.

Module API (the demo + tests call):
  - submit_halt(chain, subject_id, attester, layer, evidence) -> entry
  - check_quorum(chain, subject_id, k=2, window_seconds=60.0,
                 min_attester_reliability=0.5) -> HaltQuorumResult
  - emit_revoke_script(quorum_result, agent_ids) -> str  (bash content)
  - pickup_rescue(halted_subject_id) -> str  (v2 stub)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional

_HERE = pathlib.Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import obac
import avs
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


HALT_PREFIX = "HALT::"
DEFAULT_K = 2
DEFAULT_WINDOW_SECONDS = 60.0
DEFAULT_MIN_RELIABILITY = 0.5


# ---------------------------------------------------------------------------
# Halt attestation construction / parsing
# ---------------------------------------------------------------------------


def make_halt_claim(
    subject_id: str,
    attester_id: str,
    halts_subject: str,
    violation_layer: str,
    violation_evidence: list[str],
    rationale: str = "",
    submitted_at: Optional[str] = None,
    nonce: Optional[str] = None,
) -> dict:
    """Build a halt-type Claim packed with halt-specific fields in claim_text."""
    sidecar = {
        "halts_subject": halts_subject,
        "violation_layer": violation_layer,
        "violation_evidence": list(violation_evidence),
        "rationale": rationale,
    }
    text = HALT_PREFIX + json.dumps(sidecar, sort_keys=True, separators=(",", ":"))
    # We use the same subject_id field for both the chain-subject and halts_subject
    # (the halt is published on the subject's own chain).
    return obac.make_claim(
        subject_id=subject_id,
        attester_id=attester_id,
        claim_text=text,
        claim_type="halt",
        evidence_pointers=list(violation_evidence),
        submitted_at=submitted_at,
        nonce=nonce,
    )


def parse_halt(claim: dict) -> Optional[dict]:
    """Extract halt sidecar from a Claim, or None if not a valid halt claim."""
    if claim.get("claim_type") != "halt":
        return None
    text = claim.get("claim_text", "")
    if not text.startswith(HALT_PREFIX):
        return None
    try:
        sidecar = json.loads(text[len(HALT_PREFIX):])
    except Exception:
        return None
    required = {"halts_subject", "violation_layer", "violation_evidence"}
    if not required.issubset(sidecar.keys()):
        return None
    return sidecar


# ---------------------------------------------------------------------------
# Submission helper
# ---------------------------------------------------------------------------


def submit_halt(
    chain: "obac.Chain",
    subject_id: str,
    attester_id: str,
    attester_priv: Ed25519PrivateKey,
    violation_layer: str,
    violation_evidence: list[str],
    rationale: str = "",
    submitted_at: Optional[str] = None,
) -> dict:
    """Append a signed halt attestation to the chain. Returns the chain entry."""
    halt = make_halt_claim(
        subject_id=subject_id,
        attester_id=attester_id,
        halts_subject=subject_id,
        violation_layer=violation_layer,
        violation_evidence=violation_evidence,
        rationale=rationale,
        submitted_at=submitted_at,
    )
    return chain.append_claim(halt, attester_priv)


# ---------------------------------------------------------------------------
# Quorum check
# ---------------------------------------------------------------------------


@dataclass
class HaltQuorumResult:
    concurred: bool
    subject_id: str
    halts: list[dict] = field(default_factory=list)  # claim payloads
    counted_attesters: list[str] = field(default_factory=list)
    rejected_low_reliability: list[str] = field(default_factory=list)
    layer: Optional[str] = None
    window_seconds: float = DEFAULT_WINDOW_SECONDS

    def to_dict(self) -> dict:
        return {
            "concurred": self.concurred,
            "subject_id": self.subject_id,
            "halts": self.halts,
            "counted_attesters": self.counted_attesters,
            "rejected_low_reliability": self.rejected_low_reliability,
            "layer": self.layer,
            "window_seconds": self.window_seconds,
        }


def _parse_ts(iso: str) -> datetime:
    try:
        return datetime.fromisoformat(iso)
    except Exception:
        return datetime.now(timezone.utc)


def check_quorum(
    chain: "obac.Chain",
    subject_id: str,
    k: int = DEFAULT_K,
    window_seconds: float = DEFAULT_WINDOW_SECONDS,
    min_attester_reliability: float = DEFAULT_MIN_RELIABILITY,
    synthesizer: Optional[avs.Synthesizer] = None,
) -> HaltQuorumResult:
    """Return the quorum status for halt claims about a subject.

    Concurred quorum requires K independent (distinct attester_id, attester_pub)
    halt attestations within `window_seconds` of each other, EACH from an
    attester with reliability >= min_attester_reliability.
    """
    synth = synthesizer or avs.Synthesizer(synthesizer_id="harp-quorum")
    all_claims = [e["envelope"]["payload"] for e in chain.entries]
    all_envs = [e["envelope"] for e in chain.entries]
    attester_pub = {}
    for env in all_envs:
        attester_pub.setdefault(env["payload"]["attester_id"], env["attester_pub"])

    # Collect halts about this subject
    halts: list[dict] = []
    for c in all_claims:
        if c["claim_type"] != "halt":
            continue
        sidecar = parse_halt(c)
        if sidecar is None:
            continue
        if sidecar["halts_subject"] != subject_id:
            continue
        halts.append({**c, "_sidecar": sidecar})

    if not halts:
        return HaltQuorumResult(concurred=False, subject_id=subject_id)

    # Sort by ts
    halts.sort(key=lambda h: h["submitted_at"])

    # Eligibility filter: reliability >= floor, distinct attester per slot
    eligible: list[dict] = []
    rejected: list[str] = []
    for h in halts:
        aid = h["attester_id"]
        pub = attester_pub.get(aid, "")
        r = synth.reliability(pub, aid, subject_id, all_claims, None)
        if r < min_attester_reliability:
            rejected.append(aid)
            continue
        eligible.append({**h, "_reliability": r})

    # Sliding window for k distinct attesters
    eligible.sort(key=lambda h: h["submitted_at"])
    i = 0
    for j in range(len(eligible)):
        # Shrink window from the left until within bounds
        while (
            (_parse_ts(eligible[j]["submitted_at"]) - _parse_ts(eligible[i]["submitted_at"])).total_seconds()
            > window_seconds
        ):
            i += 1
        window = eligible[i : j + 1]
        # Deduplicate by attester_id
        distinct = {h["attester_id"] for h in window}
        if len(distinct) >= k:
            return HaltQuorumResult(
                concurred=True,
                subject_id=subject_id,
                halts=[{kk: vv for kk, vv in h.items() if kk != "_reliability"} for h in window],
                counted_attesters=sorted(distinct),
                rejected_low_reliability=sorted(set(rejected)),
                layer=window[0]["_sidecar"]["violation_layer"],
                window_seconds=window_seconds,
            )

    return HaltQuorumResult(
        concurred=False,
        subject_id=subject_id,
        halts=[{kk: vv for kk, vv in h.items() if kk != "_reliability"} for h in eligible],
        counted_attesters=[],
        rejected_low_reliability=sorted(set(rejected)),
        window_seconds=window_seconds,
    )


# ---------------------------------------------------------------------------
# Revoke script emission
# ---------------------------------------------------------------------------


def emit_revoke_script(
    quorum: HaltQuorumResult,
    agent_ids: list[str],
    calm_vault_path: str = "calm_vault.py",
) -> str:
    """Generate a bash script that revokes each agent_id via calm_vault.

    The script is intentionally simple — one line per agent — so a human can
    eyeball it before executing.
    """
    lines = [
        "#!/usr/bin/env bash",
        "# Generated by HARP — revoke agent credentials for halted subject",
        f"# Subject: {quorum.subject_id}",
        f"# Layer:   {quorum.layer or 'unknown'}",
        f"# Window:  {quorum.window_seconds} seconds",
        f"# Quorum reached: {quorum.concurred} (counted attesters: {', '.join(quorum.counted_attesters)})",
        "set -euo pipefail",
        "",
    ]
    if not quorum.concurred:
        lines.append('echo "QUORUM NOT REACHED — refusing to revoke." >&2')
        lines.append("exit 2")
        return "\n".join(lines) + "\n"
    for aid in agent_ids:
        lines.append(f'echo "Revoking agent: {aid}"')
        lines.append(f'python3 "{calm_vault_path}" revoke-agent {aid}')
    lines.append('echo "All listed agents revoked."')
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Rescue stub (v2)
# ---------------------------------------------------------------------------


def pickup_rescue(halted_subject_id: str) -> str:
    """v2 — not implemented.

    A v2 implementation would: (a) pick a hot-standby workload from a registry,
    (b) verify the standby has a BGP mandate and is not itself halted,
    (c) transfer pending work + checkpoint state, (d) emit a signed
    rescue-acknowledgement claim back to the chain.

    For v1 we surface the contract and return the marker string so callers
    can branch on absence.
    """
    return "v2 — not implemented"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _main() -> int:
    ap = argparse.ArgumentParser(description="HARP — halt + revoke protocol")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("check-quorum")
    s.add_argument("--chain", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("-k", type=int, default=DEFAULT_K)
    s.add_argument("--window", type=float, default=DEFAULT_WINDOW_SECONDS)
    s.add_argument("--min-reliability", type=float, default=DEFAULT_MIN_RELIABILITY)

    s2 = sub.add_parser("emit-revoke")
    s2.add_argument("--chain", required=True)
    s2.add_argument("--subject", required=True)
    s2.add_argument("--agents", nargs="+", required=True)
    s2.add_argument("--out", default="revoke.sh")
    s2.add_argument("-k", type=int, default=DEFAULT_K)
    s2.add_argument("--window", type=float, default=DEFAULT_WINDOW_SECONDS)

    args = ap.parse_args()

    if args.cmd == "check-quorum":
        chain = obac.Chain.open(args.chain)
        res = check_quorum(
            chain, args.subject,
            k=args.k,
            window_seconds=args.window,
            min_attester_reliability=args.min_reliability,
        )
        print(json.dumps(res.to_dict(), indent=2))
        return 0 if res.concurred else 3

    if args.cmd == "emit-revoke":
        chain = obac.Chain.open(args.chain)
        res = check_quorum(chain, args.subject, k=args.k, window_seconds=args.window)
        script = emit_revoke_script(res, args.agents)
        pathlib.Path(args.out).write_text(script)
        pathlib.Path(args.out).chmod(0o755)
        print(f"revoke script written: {args.out}")
        print(f"  concurred: {res.concurred}")
        print(f"  layer: {res.layer}")
        return 0 if res.concurred else 3

    return 1


if __name__ == "__main__":
    sys.exit(_main())
