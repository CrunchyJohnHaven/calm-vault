#!/usr/bin/env python3
"""Benchmark AAL Component 1 (Bradley-Gavini equality proof).

Measures:
  - Prover latency  : time to construct one EqualityProof
  - Verifier latency: time to verify one EqualityProof
  - End-to-end     : prover_time + verifier_time

The reference implementation under benchmark is calm_pact/protocol.py.

Run:  python3 benchmarks/bench_c1.py [--iters N] [--out path/to.csv]
"""
from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from calm_pact.protocol import (
    Commitment,
    EqualityProof,
    commit,
    prove_equality,
    verify_equality,
)


def percentile(sorted_values, p):
    if not sorted_values:
        return float("nan")
    k = (len(sorted_values) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return sorted_values[f]
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


def run(iters: int):
    # Pre-create commitments once; we measure proof + verify, not commit, because
    # in a steady-state agent fleet the commitments are exchanged once per
    # session and proofs are repeated.
    maxim = "do no harm and maximize verifiable real-world impact per dollar deployed"
    c_a = commit(maxim)
    c_b = commit(maxim)

    rows = []
    for i in range(iters):
        t0 = time.perf_counter()
        proof = prove_equality(c_a, c_b)
        t1 = time.perf_counter()
        ok = verify_equality(c_a.C, c_b.C, proof)
        t2 = time.perf_counter()
        assert ok, "verification should succeed for equal maxims"
        rows.append(
            {
                "iter": i,
                "prover_ms": (t1 - t0) * 1000,
                "verifier_ms": (t2 - t1) * 1000,
                "total_ms": (t2 - t0) * 1000,
            }
        )
    return rows


def summarize(rows, key):
    vals = sorted(r[key] for r in rows)
    return {
        "mean_ms": statistics.fmean(vals),
        "p50_ms": percentile(vals, 0.50),
        "p99_ms": percentile(vals, 0.99),
        "min_ms": vals[0],
        "max_ms": vals[-1],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iters", type=int, default=1000)
    ap.add_argument(
        "--out",
        type=str,
        default=str(
            Path(__file__).resolve().parent / "data" / "c1_bradley_gavini.csv"
        ),
    )
    args = ap.parse_args()

    rows = run(args.iters)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["iter", "prover_ms", "verifier_ms", "total_ms"])
        w.writeheader()
        w.writerows(rows)

    summary = {
        "iterations": args.iters,
        "prover": summarize(rows, "prover_ms"),
        "verifier": summarize(rows, "verifier_ms"),
        "total": summarize(rows, "total_ms"),
        "raw_csv": args.out,
    }
    import json as _json
    print(_json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
