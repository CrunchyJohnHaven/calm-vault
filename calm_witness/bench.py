"""calm_witness.bench — Everest 88 (performance budget).

Microbenchmarks for the hot paths. Stdlib timeit only — no third-party deps.
Run: ``python3 bench.py``.

Budget (v0 targets, m-series Apple silicon):

  verify_chain (per record)        : < 100 µs
  validate_record (per record)     : < 50 µs
  in_baseline_24h (one self-report): < 50 µs
  build_disclosure_record          : < 200 µs

These are placeholder budgets for the pure-Python v0. When the Rust kernel
(E43, E81) lands, the budget for cryptographic ops drops by ~10×.
"""
from __future__ import annotations

import statistics
import timeit
from typing import Callable

from disclosure import (
    DisclosureRequest,
    build_disclosure_record,
    respond,
)
from predicates import P_IN_BASELINE_24H_ID, in_baseline_24h
from schema import validate_record
from verify_chain import canonical_record_hash, verify_chain


def _self_report(seq, prev_hash, ts):
    rec = {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {
            "affect": ["calm", "even-keeled", "curious"],
            "alarm": False,
            "known_health_issues": [],
            "note": "n",
            "readiness": "ready_to_work",
            "restedness": "fully_rested",
            "sleep_hours": 8.0,
            "wake_time": "09:30",
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": ts,
        "ts_source": "test",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    return rec


def bench(label: str, fn: Callable[[], None], iterations: int = 1000):
    samples = timeit.repeat(fn, number=iterations, repeat=5)
    per_call_us = [s / iterations * 1e6 for s in samples]
    return label, min(per_call_us), statistics.median(per_call_us)


def main():
    chain = [_self_report(i, "0" * 64 if i == 1 else "f" * 64, f"2026-05-20T13:0{i}:00+00:00")
             for i in range(1, 11)]

    req = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
    )

    cases = [
        bench("verify_chain (10 records, no schema)",
              lambda: verify_chain(chain, check_schema=False)),
        bench("verify_chain (10 records, with schema)",
              lambda: verify_chain(chain, check_schema=True)),
        bench("validate_record (per record)",
              lambda: validate_record(chain[0])),
        bench("in_baseline_24h (one self-report)",
              lambda: in_baseline_24h([chain[0]])),
        bench("respond + build_disclosure_record",
              lambda: build_disclosure_record(
                  request=req,
                  response=respond(req, chain_window=[chain[0]],
                                   chain_head=chain[0]["record_hash"],
                                   operator_id_hash="b" * 64),
                  seq=2,
                  prev_hash=chain[0]["record_hash"],
              )),
    ]

    print(f"{'case':<48} {'min (µs)':>10} {'median (µs)':>14}")
    print("-" * 76)
    for label, mn, med in cases:
        print(f"{label:<48} {mn:>10.2f} {med:>14.2f}")


if __name__ == "__main__":
    main()
