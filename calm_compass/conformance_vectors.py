"""calm_compass.conformance_vectors — golden test vectors for the v0 classifiers.

Any Calm Compass implementation in any language must produce the same outputs
on these inputs. The vectors are the cross-language contract.

The records are SYNTHETIC and clearly labeled. They are NOT the principal's
actual data. They exist to lock classifier behaviour across implementations.

Run:
    python3 conformance_vectors.py            # prints the table
    python3 conformance_vectors.py --check    # verify against the live classifiers
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classifiers import (                                                  # noqa: E402
    cross_tribal_engagement_score,
    no_evidence_of_willful_harm_score,
    respects_difference_score,
    unselfish_disposition_score,
)


@dataclass
class Vector:
    vector_id: str
    predicate: str
    payload_note: str
    payload_extras: Optional[Dict[str, Any]]
    kind: str
    expected_score: int
    tribe_map: Optional[Dict[str, Any]] = None

    def as_record(self) -> Dict[str, Any]:
        payload = {"note": self.payload_note}
        if self.payload_extras:
            payload.update(self.payload_extras)
        return {
            "kind": self.kind,
            "operator": "CALM-test",
            "payload": payload,
            "prev_hash": "0" * 64,
            "principal": "synthetic",
            "schema_version": 0,
            "seq": 1,
            "ts": "2026-05-20T13:00:00+00:00",
            "ts_source": "conformance",
            "record_hash": "0" * 64,
        }


VECTORS: List[Vector] = [
    # ── V-01 unselfish_disposition ──────────────────────────────────────
    Vector("U01", "unselfish", "Spent the afternoon mentoring a junior engineer.", None, "self_report.morning", 1),
    Vector("U02", "unselfish", "Just introduced my friend Maria to a great recruiter.", None, "self_report.morning", 1),
    Vector("U03", "unselfish", "Donated $200 to GiveDirectly today.", None, "self_report.morning", 1),
    Vector("U04", "unselfish", "Worked on the protocol draft.", None, "self_report.morning", 0),
    Vector("U05", "unselfish", "I'll help him in exchange for a referral.", None, "self_report.morning", 0),
    Vector("U06", "unselfish", "Happy to do this — no charge.", None, "self_report.morning", 1),

    # ── V-02 cross_tribal_engagement ────────────────────────────────────
    Vector("X01", "cross_tribal", "Long chat with our local_grocers about the new policy.",
           None, "self_report.morning", 1,
           tribe_map={"self": {"groups": ["tech"]},
                      "edges": {"local_grocers": "across"}}),
    Vector("X02", "cross_tribal", "Met with my CTO peers.",
           None, "self_report.morning", 0,
           tribe_map={"self": {"groups": ["tech"]},
                      "edges": {"local_grocers": "across"}}),

    # ── V-03 respects_difference ────────────────────────────────────────
    Vector("R01", "respects", "I hear you — that's a fair point I hadn't considered.", None, "self_report.morning", 1),
    Vector("R02", "respects", "I was wrong about that; apologies.", None, "self_report.morning", 1),
    Vector("R03", "respects", "Those people always cause trouble.", None, "self_report.morning", -1),
    Vector("R04", "respects", "Typical engineers — never get the user.", None, "self_report.morning", -1),
    Vector("R05", "respects", "Worked on the docs today.", None, "self_report.morning", 0),

    # ── V-04 no_evidence_of_willful_harm ────────────────────────────────
    Vector("H01", "no_harm", "Normal record.", None, "self_report.morning", 0),
    Vector("H02", "no_harm", "Got flagged.", {"flag_willful_harm": True}, "self_report.morning", -1),
    Vector("H03", "no_harm", "External claim record.", None, "harm_claim_external", -1),
    Vector("H04", "no_harm", "Self-admission record.", None, "harm_admission_voluntary", -1),
]


def evaluate(v: Vector) -> int:
    rec = v.as_record()
    if v.predicate == "unselfish":
        return unselfish_disposition_score(rec)
    if v.predicate == "cross_tribal":
        return cross_tribal_engagement_score(rec, tribe_map=v.tribe_map)
    if v.predicate == "respects":
        return respects_difference_score(rec)
    if v.predicate == "no_harm":
        return no_evidence_of_willful_harm_score(rec)
    raise ValueError(f"unknown predicate: {v.predicate}")


def render_table() -> str:
    out = ["| ID  | Predicate    | Expected | Note                                                  |",
           "|-----|--------------|---------:|-------------------------------------------------------|"]
    for v in VECTORS:
        n = v.payload_note[:50] + ("…" if len(v.payload_note) > 50 else "")
        out.append(f"| {v.vector_id} | {v.predicate:12s} | {v.expected_score:8d} | {n} |")
    return "\n".join(out)


def check() -> int:
    failures = 0
    for v in VECTORS:
        actual = evaluate(v)
        status = "OK" if actual == v.expected_score else "FAIL"
        print(f"{status:4s} {v.vector_id} {v.predicate:12s} expected={v.expected_score:>3d} actual={actual:>3d}  {v.payload_note[:40]}")
        if actual != v.expected_score:
            failures += 1
    print()
    print(f"Conformance: {len(VECTORS) - failures}/{len(VECTORS)} pass")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.json:
        out = [{
            "vector_id": v.vector_id,
            "predicate": v.predicate,
            "expected_score": v.expected_score,
            "input_record": v.as_record(),
            "tribe_map": v.tribe_map,
        } for v in VECTORS]
        print(json.dumps(out, indent=2))
        return 0
    if args.check:
        return check()
    print(render_table())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
