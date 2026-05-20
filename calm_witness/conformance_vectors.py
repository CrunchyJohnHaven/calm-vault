"""calm_witness.conformance_vectors — golden vectors for the v0 Witness layer.

Any Calm Witness implementation in any language must produce the same outputs
on these inputs. Locks: canonicalisation, record_hash, schema validation,
in_baseline_24h predicate.

Run:
    python3 conformance_vectors.py            # print table
    python3 conformance_vectors.py --check    # verify against live impl
    python3 conformance_vectors.py --json     # full machine-readable corpus
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from predicates import P_IN_BASELINE_24H_ID, in_baseline_24h, PredicateValue   # noqa: E402
from schema import validate_record                                              # noqa: E402
from verify_chain import canonical_record_hash                                  # noqa: E402


@dataclass
class CanonicalVector:
    vector_id: str
    record: Dict[str, Any]
    expected_canonical_hex: str


@dataclass
class SchemaVector:
    vector_id: str
    record: Dict[str, Any]
    expected_errors_substring: List[str]    # empty list means clean


@dataclass
class PredicateVector:
    vector_id: str
    chain_window: List[Dict[str, Any]]
    now_iso: str
    expected_value: str


def _baseline_record(ts: str, affect=("calm",), restedness="fully_rested",
                     known_health_issues=(), seq=1):
    return {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {
            "affect": list(affect),
            "alarm": False,
            "known_health_issues": list(known_health_issues),
            "note": "conformance",
            "readiness": "ready_to_work",
            "restedness": restedness,
            "sleep_hours": 8.0,
            "wake_time": "09:30",
        },
        "prev_hash": "0" * 64,
        "principal": "conformance",
        "schema_version": 0,
        "seq": seq,
        "ts": ts,
        "ts_source": "conformance",
    }


# ── Canonicalisation vectors (lock JCS-style encoding + sha256 of record) ──
CANONICAL: List[CanonicalVector] = []
for rec in (
    _baseline_record("2026-05-20T13:00:00+00:00", seq=1),
    _baseline_record("2026-05-20T13:00:00+00:00", affect=("calm", "curious"), seq=2),
):
    rec_copy = dict(rec)
    rec_copy["record_hash"] = canonical_record_hash(rec_copy)
    CANONICAL.append(CanonicalVector(
        vector_id=f"CN{rec_copy['seq']:02d}",
        record=rec_copy,
        expected_canonical_hex=rec_copy["record_hash"],
    ))


# ── Schema vectors (lock validate_record behaviour) ────────────────────────
def _build_schema_vectors() -> List[SchemaVector]:
    clean = _baseline_record("2026-05-20T13:00:00+00:00")
    clean["record_hash"] = canonical_record_hash(clean)
    no_kind = dict(clean)
    no_kind.pop("kind")
    bad_kind = dict(clean)
    bad_kind["kind"] = "totally_fake"
    bad_kind["record_hash"] = canonical_record_hash(bad_kind)
    bad_hash = dict(clean)
    bad_hash["record_hash"] = "not-hex"
    return [
        SchemaVector("S01", clean, []),
        SchemaVector("S02", no_kind, ["missing top-level field: kind"]),
        SchemaVector("S03", bad_kind, ["unknown kind"]),
        SchemaVector("S04", bad_hash, ["record_hash"]),
    ]


SCHEMA: List[SchemaVector] = _build_schema_vectors()


# ── Predicate vectors (lock in_baseline_24h evaluation) ────────────────────
NOW = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)


def _pv(window, expected):
    return PredicateVector(
        vector_id=f"P{len(PREDICATES)+1:02d}",
        chain_window=window,
        now_iso=NOW.isoformat().replace("+00:00", "Z"),
        expected_value=expected,
    )


PREDICATES: List[PredicateVector] = []
PREDICATES.append(_pv([_baseline_record("2026-05-20T13:00:00+00:00")], "true"))
PREDICATES.append(_pv([_baseline_record("2026-05-20T13:00:00+00:00",
                                         affect=("agitated",))], "false"))
PREDICATES.append(_pv([_baseline_record("2026-05-20T13:00:00+00:00",
                                         restedness="tired")], "false"))
PREDICATES.append(_pv([_baseline_record("2026-05-20T13:00:00+00:00",
                                         known_health_issues=("fever",))], "false"))
PREDICATES.append(_pv([_baseline_record("2026-05-18T13:00:00+00:00")], "unknown"))
PREDICATES.append(_pv([], "unknown"))


def check() -> int:
    fails = 0

    # Canonicalisation: recompute hash and confirm
    for v in CANONICAL:
        actual = canonical_record_hash(v.record)
        ok = (actual == v.expected_canonical_hex)
        print(f"{'OK' if ok else 'FAIL':4s} {v.vector_id} canonical_record_hash")
        if not ok:
            print(f"   expected: {v.expected_canonical_hex}")
            print(f"   actual:   {actual}")
            fails += 1

    # Schema
    for v in SCHEMA:
        errs = validate_record(v.record)
        if not v.expected_errors_substring:
            ok = (errs == [])
        else:
            ok = all(any(sub in e for e in errs) for sub in v.expected_errors_substring)
        print(f"{'OK' if ok else 'FAIL':4s} {v.vector_id} schema  errors={errs}")
        if not ok:
            fails += 1

    # Predicates
    for v in PREDICATES:
        r = in_baseline_24h(v.chain_window, now=NOW)
        actual = r.value.value
        ok = (actual == v.expected_value)
        print(f"{'OK' if ok else 'FAIL':4s} {v.vector_id} in_baseline_24h expected={v.expected_value:8s} actual={actual:8s}")
        if not ok:
            fails += 1

    total = len(CANONICAL) + len(SCHEMA) + len(PREDICATES)
    print()
    print(f"Conformance: {total - fails}/{total} pass")
    return 0 if fails == 0 else 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.json:
        out = {
            "canonicalisation": [{"vector_id": v.vector_id, "record": v.record,
                                  "expected_canonical_hex": v.expected_canonical_hex}
                                 for v in CANONICAL],
            "schema": [{"vector_id": v.vector_id, "record": v.record,
                        "expected_errors_substring": v.expected_errors_substring}
                       for v in SCHEMA],
            "predicates": [{"vector_id": v.vector_id,
                            "chain_window": v.chain_window,
                            "now_iso": v.now_iso,
                            "expected_value": v.expected_value}
                           for v in PREDICATES],
        }
        print(json.dumps(out, indent=2))
        return 0
    if args.check:
        return check()
    print(f"Canonicalisation vectors: {len(CANONICAL)}")
    print(f"Schema vectors:           {len(SCHEMA)}")
    print(f"Predicate vectors:        {len(PREDICATES)}")
    print(f"Total:                    {len(CANONICAL) + len(SCHEMA) + len(PREDICATES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
