#!/usr/bin/env python3
"""Run all AAL component benchmarks and emit a JSON summary.

Usage: python3 benchmarks/run_all.py [--out benchmarks/data/summary.json]
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import bench_c1
import bench_c3
import bench_c5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=str,
        default=str(
            Path(__file__).resolve().parent / "data" / "summary.json"
        ),
    )
    ap.add_argument("--c1-iters", type=int, default=1000)
    ap.add_argument("--c3-iters", type=int, default=1000)
    ap.add_argument("--c5-iters", type=int, default=100)
    args = ap.parse_args()

    print("=== C1: Bradley-Gavini equality proof ===", flush=True)
    sys.argv = ["bench_c1.py", "--iters", str(args.c1_iters)]
    c1 = bench_c1.main()

    print("\n=== C3: Permissionless attestation log ===", flush=True)
    sys.argv = ["bench_c3.py", "--iters", str(args.c3_iters)]
    c3 = bench_c3.main()

    print("\n=== C5: Permissionless kill switch ===", flush=True)
    sys.argv = ["bench_c5.py", "--iters", str(args.c5_iters)]
    c5 = bench_c5.main()

    env = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "machine": platform.machine(),
        "hostname": socket.gethostname(),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    summary = {
        "environment": env,
        "c1_bradley_gavini": c1,
        "c3_attestation_log": c3,
        "c5_kill_switch": c5,
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to {args.out}")
    return summary


if __name__ == "__main__":
    main()
