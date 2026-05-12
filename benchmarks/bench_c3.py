#!/usr/bin/env python3
"""Benchmark AAL Component 3 (Permissionless Attestation Log).

Measures:
  - Write latency : submit one signed attestation, including Merkle-chain update.
  - Read latency  : aggregate-attestation query for a randomly chosen subject.

Uses the minimal reference implementation under benchmarks/aal_c3_attestation_log.py.

Run:  python3 benchmarks/bench_c3.py [--iters N] [--out path/to.csv]
"""
from __future__ import annotations

import argparse
import csv
import os
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from aal_c3_attestation_log import AttestationLog


def percentile(sorted_values, p):
    if not sorted_values:
        return float("nan")
    k = (len(sorted_values) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return sorted_values[f]
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)


def run(iters: int, num_subjects: int = 100, num_attesters: int = 50):
    rng = random.Random(20260512)
    log = AttestationLog()
    subjects = [f"subject-{i:04d}" for i in range(num_subjects)]
    attesters = [Ed25519PrivateKey.generate() for _ in range(num_attesters)]

    rows = []
    for i in range(iters):
        subj = rng.choice(subjects)
        attester = rng.choice(attesters)
        claim = f"observation-{i}: output meets spec"

        t0 = time.perf_counter()
        log.submit(subj, attester, claim)
        t1 = time.perf_counter()

        query_subj = rng.choice(subjects)
        t2 = time.perf_counter()
        results = log.query_subject(query_subj)
        t3 = time.perf_counter()

        rows.append(
            {
                "iter": i,
                "write_ms": (t1 - t0) * 1000,
                "read_ms": (t3 - t2) * 1000,
                "read_results": len(results),
            }
        )
    return rows, log


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
            Path(__file__).resolve().parent / "data" / "c3_attestation_log.csv"
        ),
    )
    args = ap.parse_args()

    rows, log = run(args.iters)

    # Sanity: every entry should chain correctly. We skip this in the hot
    # path; here we run it once at the end as a correctness check.
    assert log.verify_chain(), "C3 chain failed end-of-run integrity check"

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["iter", "write_ms", "read_ms", "read_results"]
        )
        w.writeheader()
        w.writerows(rows)

    summary = {
        "iterations": args.iters,
        "write": summarize(rows, "write_ms"),
        "read": summarize(rows, "read_ms"),
        "chain_integrity_ok": True,
        "raw_csv": args.out,
    }
    import json as _json
    print(_json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
