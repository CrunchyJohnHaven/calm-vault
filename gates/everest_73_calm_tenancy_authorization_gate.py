#!/usr/bin/env python3
"""EVEREST 73 Gate — Calm Tenancy (CT-73) Counterparty-Class Authorization.

Verifies SUMMIT 73 / 300 by testing authorize_disclosure across five critical
assertions covering the default policy matrix defined in Everest 7.

Exit 0 on all assertions passing; exit 1 on any failure.
"""
import sys
from pathlib import Path


def run_gate():
    """Run EVEREST 73 authorization gate."""
    # Add calm_witness to sys.path for import
    vault_market_root = Path(__file__).parent.parent
    calm_witness_dir = vault_market_root / "calm_witness"
    sys.path.insert(0, str(vault_market_root))

    try:
        from calm_witness.authorization import authorize_disclosure
    except ImportError as e:
        print(f"FAIL: Could not import authorize_disclosure: {e}")
        return 1

    # Define the five assertions for EVEREST 73 / 300
    assertions = [
        {
            "predicate": "calm-witness/predicate/v0/in_baseline_24h",
            "counterparty_class": "anonymous",
            "expected": True,
            "description": "in_baseline_24h (OPEN class) → anonymous allowed",
        },
        {
            "predicate": "calm-witness/predicate/v0/bank_teller_note_active",
            "counterparty_class": "anonymous",
            "expected": False,
            "description": "bank_teller_note_active (DURESS_RING class) → anonymous denied",
        },
        {
            "predicate": "calm-witness/predicate/v0/biometric_match_within",
            "counterparty_class": "financial",
            "expected": True,
            "description": "biometric_match_within (STEP_UP class) → financial allowed",
        },
        {
            "predicate": "calm-witness/predicate/v0/biometric_match_within",
            "counterparty_class": "anonymous",
            "expected": False,
            "description": "biometric_match_within (STEP_UP class) → anonymous denied",
        },
        {
            "predicate": "calm-witness/predicate/v0/mental_state_unusual",
            "counterparty_class": "medical",
            "expected": False,
            "description": "mental_state_unusual (PRINCIPAL_EXPLICIT class) → medical denied",
        },
    ]

    passed = 0
    failed = 0

    for i, assertion in enumerate(assertions, 1):
        result = authorize_disclosure(
            assertion["predicate"],
            assertion["counterparty_class"],
        )

        matches = result.allowed == assertion["expected"]
        status = "PASS" if matches else "FAIL"

        print(
            f"[{i}/5] {status}: {assertion['description']}\n"
            f"       Result: allowed={result.allowed}, reason='{result.reason}'"
        )

        if matches:
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*70}")
    print(f"SUMMARY: {passed}/{len(assertions)} assertions passed")

    if failed == 0:
        print("STATUS: ALL GATES GREEN ✓")
        return 0
    else:
        print(f"STATUS: {failed} ASSERTION(S) FAILED ✗")
        return 1


if __name__ == "__main__":
    sys.exit(run_gate())
