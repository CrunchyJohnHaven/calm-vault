#!/usr/bin/env python3
"""Benchmark AAL Component 5 (Permissionless Kill Switch).

Measures fire-to-freeze latency:
  - From the start of a fire() call by an arbitrary network participant
  - To the moment is_frozen(target) returns True for the target entity.

This is the key latency the manifesto claims: "ANY party in the network
can fire the kill switch on a misbehaving entity. The entity freezes
immediately."

Run:  python3 benchmarks/bench_c5.py [--iters N] [--out path/to.csv]
"""
from __future__ import annotations

import argparse
import csv
import os
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from aal_c5_kill_switch import KillSwitchRegistry


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
    rows = []
    for i in range(iters):
        # Fresh registry each iteration so we measure a clean fire-to-freeze.
        registry = KillSwitchRegistry()
        firer = Ed25519PrivateKey.generate()
        target = f"agent-{i:05d}"

        # Precondition: target is NOT frozen.
        assert not registry.is_frozen(target)

        t0 = time.perf_counter()
        registry.fire(target, firer, reason="misalignment-detected")
        # Postcondition: target IS frozen. Probe it inside the timed window.
        frozen = registry.is_frozen(target)
        t1 = time.perf_counter()
        assert frozen, "fire() did not freeze the target"

        rows.append(
            {
                "iter": i,
                "fire_to_freeze_ms": (t1 - t0) * 1000,
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
    ap.add_argument("--iters", type=int, default=100)
    ap.add_argument(
        "--out",
        type=str,
        default=str(
            Path(__file__).resolve().parent / "data" / "c5_kill_switch.csv"
        ),
    )
    args = ap.parse_args()

    rows = run(args.iters)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["iter", "fire_to_freeze_ms"])
        w.writeheader()
        w.writerows(rows)

    summary = {
        "iterations": args.iters,
        "fire_to_freeze": summarize(rows, "fire_to_freeze_ms"),
        "raw_csv": args.out,
    }
    import json as _json
    print(_json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
