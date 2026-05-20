#!/usr/bin/env python3
"""
Everest 300 Registry Sync Gate: Verifies §2 bagged table vs grep **BAGGED counts.
Tolerance: ±1 per pillar (accounts for partials, in-flight bags, edge timing).
Signed: Elon Musk, 2026-05-20.
"""

import os
import re
import sys
from pathlib import Path

REGISTRY_PATH = Path("/Users/johnbradley/AllData/calm_vault_market/THE_EVEREST_300.md")
VAULT_ROOT = Path("/Users/johnbradley/AllData/calm_vault_market")

PILLARS = {
    "1-100": {
        "name": "Witness",
        "file": "ZKBB_USER_EVERESTS_100.md",
        "pattern": r"1–100\s+Witness",
    },
    "101-130": {
        "name": "Pact",
        "file": "CALM_PACT_EVERESTS_30.md",
        "pattern": r"101–130\s+Pact",
    },
    "131-180": {
        "name": "Compass",
        "file": "CALM_COMPASS_EVERESTS_50.md",
        "pattern": r"131–180\s+Compass",
    },
    "181-230": {
        "name": "Tenancy",
        "file": "CALM_TENANCY_EVERESTS_50.md",
        "pattern": r"181–230\s+Tenancy",
    },
    "231-280": {
        "name": "Operations",
        "file": "CALM_OPERATIONS_EVERESTS_50.md",
        "pattern": r"231–280\s+Operations",
    },
    "281-300": {
        "name": "Governance",
        "file": "STACK_GOVERNANCE_20.md",
        "pattern": r"281–300\s+Governance",
    },
}

TOLERANCE = 1


def grep_bagged_count(filepath):
    """Count **BAGGED occurrences in a file."""
    if not filepath.exists():
        return 0
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(re.findall(r"\*\*BAGGED", content))


def extract_table_counts(registry_path):
    """Extract bagged counts from §2 table."""
    with open(registry_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    counts = {}
    
    for range_key, pillar_info in PILLARS.items():
        # Find the line matching this pillar in the table
        pattern = pillar_info["pattern"]
        match = re.search(pattern + r"\s+\|\s+(\d+)", content)
        if match:
            counts[range_key] = int(match.group(1))
        else:
            counts[range_key] = 0
    
    return counts


def main():
    print("=" * 70)
    print("EVEREST 300 REGISTRY SYNC GATE")
    print("=" * 70)
    
    table_counts = extract_table_counts(REGISTRY_PATH)
    grepped_counts = {}
    mismatches = []
    
    for range_key, pillar_info in PILLARS.items():
        filepath = VAULT_ROOT / pillar_info["file"]
        grepped = grep_bagged_count(filepath)
        grepped_counts[range_key] = grepped
        
        table_val = table_counts.get(range_key, 0)
        diff = abs(grepped - table_val)
        
        status = "✓ OK" if diff <= TOLERANCE else "✗ MISMATCH"
        if diff > TOLERANCE:
            mismatches.append(range_key)
        
        print(f"{pillar_info['name']:12} | grep: {grepped:2} | table: {table_val:2} | {status}")
    
    print("=" * 70)
    
    total_grepped = sum(grepped_counts.values())
    total_table = sum(table_counts.values())
    
    print(f"TOTAL       | grep: {total_grepped:2} | table: {total_table:2} | diff: {abs(total_grepped - total_table)}")
    print("=" * 70)
    
    if mismatches:
        print(f"✗ GATE FAILED: {len(mismatches)} pillar(s) exceed tolerance of ±{TOLERANCE}:")
        for m in mismatches:
            print(f"  - {PILLARS[m]['name']}")
        sys.exit(1)
    else:
        print("✓ GATE PASSED: All pillars within tolerance. Registry verified.")
        print("\n— Elon Musk, 2026-05-20")
        sys.exit(0)


if __name__ == "__main__":
    main()
