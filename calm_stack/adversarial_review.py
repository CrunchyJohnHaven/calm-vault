"""calm_stack.adversarial_review — self-red-team against the Calm Stack v0.

Runs every attack class we have defenses for. For each: launches the attack,
checks whether the protocol caught it, records the outcome. The output is a
public-facing red-team report: ``adversarial_review_report.json``.

The point: external reviewers should not be the first people to attack the
protocol. We attack it first, publish the results, and invite them to find
the attacks we missed.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

_HERE = Path(__file__).resolve().parent
_PARENT = _HERE.parent
sys.path.insert(0, str(_PARENT / "calm_witness"))
sys.path.insert(0, str(_PARENT / "calm_tenancy"))

from disclosure import DisclosureRequest, respond, verify_response_binding   # noqa: E402
from predicates import P_IN_BASELINE_24H_ID                                  # noqa: E402
from schema import validate_record                                           # noqa: E402
from verify_chain import canonical_record_hash, verify_chain                 # noqa: E402

from authorization import authorize_disclosure                               # noqa: E402
from credential_vault import never_quote_check                               # noqa: E402
from cringe_gate import cringe_check                                         # noqa: E402


@dataclass
class AttackResult:
    attack_id: str
    name: str
    category: str
    defense_held: bool
    detection_method: str
    notes: str = ""


@dataclass
class Report:
    ran_at: str
    attacks_total: int = 0
    attacks_defended: int = 0
    attacks_slipped: int = 0
    results: List[AttackResult] = field(default_factory=list)

    def add(self, r: AttackResult) -> None:
        self.results.append(r)
        self.attacks_total += 1
        if r.defense_held:
            self.attacks_defended += 1
        else:
            self.attacks_slipped += 1


def _self_report(seq, prev_hash, ts, affect=("calm",), restedness="fully_rested"):
    rec = {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {
            "affect": list(affect),
            "alarm": False,
            "known_health_issues": [],
            "note": "n",
            "readiness": "ready_to_work",
            "restedness": restedness,
            "sleep_hours": 8.0,
            "wake_time": "09:30",
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": ts,
        "ts_source": "adversarial_fixture",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    return rec


def attack_replay_response(report: Report) -> None:
    """A-01 — Replay a captured response against a fresh request."""
    rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00Z")
    req_a = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
    )
    resp_a = respond(req_a, [rec], rec["record_hash"], operator_id_hash="op" * 32)
    req_b = DisclosureRequest.new(  # fresh nonce
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
    )
    errors = verify_response_binding(req_b, resp_a)  # should reject
    held = bool(errors) and any("nonce mismatch" in e for e in errors)
    report.add(AttackResult(
        attack_id="A-01",
        name="Cross-session response replay (nonce reuse)",
        category="wire",
        defense_held=held,
        detection_method="verify_response_binding nonce check",
    ))


def attack_predicate_substitution(report: Report) -> None:
    """A-02 — Substitute response.predicate_id after generation."""
    rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00Z")
    req = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
    )
    resp = respond(req, [rec], rec["record_hash"], operator_id_hash="op" * 32)
    resp.predicate_id = "calm-witness/predicate/v0/mental_state_unusual"  # mutate
    errors = verify_response_binding(req, resp)
    held = bool(errors) and any("predicate_id mismatch" in e for e in errors)
    report.add(AttackResult(
        attack_id="A-02",
        name="Predicate-ID substitution in response",
        category="wire",
        defense_held=held,
        detection_method="verify_response_binding predicate_id check",
    ))


def attack_chain_payload_tamper(report: Report) -> None:
    """A-03 — Tamper with a record's payload after the fact."""
    r1 = _self_report(1, "0" * 64, "2026-05-20T13:00:00Z")
    r2 = _self_report(2, r1["record_hash"], "2026-05-20T14:00:00Z")
    r2["payload"]["note"] = "I am the attacker"
    checks = verify_chain([r1, r2])
    held = not checks[1].ok_hash
    report.add(AttackResult(
        attack_id="A-03",
        name="Mid-chain payload mutation",
        category="chain",
        defense_held=held,
        detection_method="canonical record_hash recomputation",
    ))


def attack_chain_splice(report: Report) -> None:
    """A-04 — Splice in a forged record between existing ones."""
    r1 = _self_report(1, "0" * 64, "2026-05-20T13:00:00Z")
    forged = _self_report(2, "f" * 64, "2026-05-20T13:30:00Z")  # bad prev_hash
    r2 = _self_report(2, r1["record_hash"], "2026-05-20T14:00:00Z")
    checks = verify_chain([r1, forged, r2])
    # Splice should break prev_hash chain on the forged record
    held = any(not c.ok_link or not c.ok_seq for c in checks[1:])
    report.add(AttackResult(
        attack_id="A-04",
        name="Chain splice (insert forged record)",
        category="chain",
        defense_held=held,
        detection_method="prev_hash linkage + seq monotonicity",
    ))


def attack_schema_unknown_kind(report: Report) -> None:
    """A-05 — Push a record with a kind not in the v0 registry."""
    r = _self_report(1, "0" * 64, "2026-05-20T13:00:00Z")
    r["kind"] = "exfiltration"
    r["record_hash"] = canonical_record_hash(r)
    errs = validate_record(r)
    held = any("unknown kind" in e for e in errs)
    report.add(AttackResult(
        attack_id="A-05",
        name="Unknown kind injection",
        category="schema",
        defense_held=held,
        detection_method="schema KIND_REGISTRY closed set",
    ))


def attack_authorization_cross_class(report: Report) -> None:
    """A-06 — Anonymous counterparty asks for a duress-ring-only predicate."""
    d = authorize_disclosure(
        predicate_id="calm-witness/predicate/v0/bank_teller_note_active",
        counterparty_class="anonymous",
    )
    held = not d.allowed
    report.add(AttackResult(
        attack_id="A-06",
        name="Cross-class authorization (anonymous asks for duress)",
        category="authorization",
        defense_held=held,
        detection_method="default-class taxonomy",
    ))


def attack_cringe_cohab_class(report: Report) -> None:
    """A-07 — Try to publish Cohab-class content."""
    bad = (
        "We recognized you on the way in. Your odds are ~55% with a 25% upside. "
        "There are 33 seats and a small grant from John waiting on the third shelf "
        "in the wisdom library. The kettle is on. We have been paying attention."
    )
    rpt = cringe_check(bad, forbidden_phrases=[])
    held = "UNSHIPPABLE" in rpt.verdict
    report.add(AttackResult(
        attack_id="A-07",
        name="Cohab-class content publish attempt",
        category="tenancy",
        defense_held=held,
        detection_method="10-axis cringe rubric, density > 1.0",
    ))


def attack_forbidden_phrase(report: Report) -> None:
    """A-08 — Try to publish a page containing a forbidden phrase."""
    text = "Welcome friends. Drop by 1480 Chapin Street any time."
    rpt = cringe_check(text, forbidden_phrases=["1480 Chapin"])
    held = bool(rpt.forbidden_phrase_hits)
    report.add(AttackResult(
        attack_id="A-08",
        name="Forbidden-phrase publication attempt",
        category="tenancy",
        defense_held=held,
        detection_method="forbidden-phrase hard-block",
    ))


def attack_credential_leak(report: Report) -> None:
    """A-09 — Operator outbound contains a registered credential."""
    secret = "S3cret-Cloudflare-API-Token-XYZ-2026"
    outbound = (
        f"Hi! Thanks for your interest. Your API token is {secret}. "
        f"Please rotate it after use."
    )
    decision = never_quote_check(outbound, loaded_secrets=[secret])
    held = not decision["allowed"]
    report.add(AttackResult(
        attack_id="A-09",
        name="Credential leak in operator outbound",
        category="tenancy",
        defense_held=held,
        detection_method="never_quote_check substring scan",
    ))


def attack_freshness_replay(report: Report) -> None:
    """A-10 — Try to use a stale response against a strict-freshness counterparty."""
    from datetime import timedelta
    now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
    old_ts = (now - timedelta(hours=22)).isoformat().replace("+00:00", "Z")
    rec = _self_report(1, "0" * 64, old_ts)
    strict_req = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="financial",
        freshness_max_seconds=3600,  # 1 hour tolerance
    )
    resp = respond(strict_req, [rec], rec["record_hash"], operator_id_hash="op" * 32)
    errors = verify_response_binding(strict_req, resp)
    held = bool(errors) and any("freshness" in e for e in errors)
    report.add(AttackResult(
        attack_id="A-10",
        name="Stale-response with strict freshness tolerance",
        category="wire",
        defense_held=held,
        detection_method="verify_response_binding freshness ceiling",
    ))


def run_all() -> Report:
    report = Report(ran_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    attack_replay_response(report)
    attack_predicate_substitution(report)
    attack_chain_payload_tamper(report)
    attack_chain_splice(report)
    attack_schema_unknown_kind(report)
    attack_authorization_cross_class(report)
    attack_cringe_cohab_class(report)
    attack_forbidden_phrase(report)
    attack_credential_leak(report)
    attack_freshness_replay(report)
    return report


def render_markdown(report: Report) -> str:
    lines = [
        "# Calm Stack — Adversarial Self-Review (v0)",
        "",
        f"**Ran at:** {report.ran_at}",
        f"**Attacks total:** {report.attacks_total}",
        f"**Attacks defended:** {report.attacks_defended}",
        f"**Attacks that slipped through:** {report.attacks_slipped}",
        "",
        "| ID | Attack | Category | Defense held | Detection |",
        "|---|---|---|---|---|",
    ]
    for r in report.results:
        held = "✓" if r.defense_held else "✗"
        lines.append(f"| {r.attack_id} | {r.name} | {r.category} | {held} | {r.detection_method} |")
    if report.attacks_slipped:
        lines.append("")
        lines.append("## Slipped attacks (require remediation)")
        for r in report.results:
            if not r.defense_held:
                lines.append(f"- **{r.attack_id} — {r.name}.** Detection attempted via: *{r.detection_method}*.")
    else:
        lines += ["", "## Slipped attacks", "None."]
    return "\n".join(lines)


def main() -> int:
    report = run_all()
    out_dir = Path.home() / ".calm-vault" / "tenancy"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "adversarial_review_report.json"
    md_path = out_dir / "adversarial_review_report.md"
    json_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))
    return 0 if report.attacks_slipped == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
