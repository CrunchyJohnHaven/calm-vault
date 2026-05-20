#!/usr/bin/env python3
"""Gate for SUMMIT 88/300 (E88 — Performance Budget).

Runs calm_witness/bench.py and asserts median µs per case are under budget.
Exit 0 if all hold; 1 on any miss; 0 if bench unavailable (skip cleanly).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

_ROOT = Path("/Users/johnbradley/AllData/calm_vault_market")
_BENCH = _ROOT / "calm_witness" / "bench.py"

# Generous ceilings — these are pure-Python budgets, expected to be replaced
# by the Rust kernel (CP-09); they need to pass on a wide range of host hardware.
BUDGETS_US = {
    "verify_chain (10 records, no schema)":   1000.0,
    "validate_record (per record)":            500.0,
    "in_baseline_24h (one self-report)":       500.0,
    "respond + build_disclosure_record":      5000.0,
}


def main() -> int:
    if not _BENCH.exists():
        print(f"SKIP bench.py not found: {_BENCH}")
        return 0
    try:
        out = subprocess.run(
            [sys.executable, str(_BENCH)],
            cwd=str(_ROOT / "calm_witness"),
            capture_output=True, text=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        print("FAIL bench timed out")
        return 1
    if out.returncode != 0:
        print(f"FAIL bench exit={out.returncode}\n{out.stderr[-400:]}")
        return 1

    lines = out.stdout.splitlines()
    fails = 0
    for case, ceiling in BUDGETS_US.items():
        median = None
        for line in lines:
            if line.startswith(case):
                # Expected format: "<case>      <min>   <median>"
                nums = re.findall(r"\d+\.\d+", line)
                if len(nums) >= 2:
                    median = float(nums[1])
                break
        if median is None:
            print(f"FAIL '{case}' — line not found in bench output")
            fails += 1
            continue
        ok = median < ceiling
        status = "OK" if ok else "FAIL"
        print(f"{status:4s} {case:48s} median={median:>8.2f} µs  ceiling={ceiling:>7.1f} µs")
        if not ok:
            fails += 1
    print()
    print(f"RESULT: {len(BUDGETS_US) - fails}/{len(BUDGETS_US)} budgets met")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
