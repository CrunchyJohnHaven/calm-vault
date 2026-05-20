#!/usr/bin/env python3
"""EVEREST 61 — Predicate composition AND/OR/NOT with REFUSED-absorbing semantics.

This gate verifies SUMMIT 61/300 (E61) by running a truth-table coverage test
of compose_and, compose_or, and negate with proper REFUSED absorption.

REFUSED is absorbing: any operand refused → result refused.
UNKNOWN propagates conservatively: T∧U=U, F∧U=F, F∨U=U, T∨U=T.
"""
import sys

# Add path for imports
sys.path.insert(0, "/Users/johnbradley/AllData/calm_vault_market")

from calm_witness.composition import compose_and, compose_or, negate
from calm_witness.predicates import EvaluationResult, PredicateValue, P_IN_BASELINE_24H_ID

# Construct helper EvaluationResult instances for each truth value
TRUE_result = EvaluationResult(
    predicate_id=P_IN_BASELINE_24H_ID,
    value=PredicateValue.TRUE,
    freshness_window_seconds=0,
    reason="test: TRUE"
)

FALSE_result = EvaluationResult(
    predicate_id=P_IN_BASELINE_24H_ID,
    value=PredicateValue.FALSE,
    freshness_window_seconds=0,
    reason="test: FALSE"
)

UNKNOWN_result = EvaluationResult(
    predicate_id=P_IN_BASELINE_24H_ID,
    value=PredicateValue.UNKNOWN,
    freshness_window_seconds=None,
    reason="test: UNKNOWN"
)

REFUSED_result = EvaluationResult(
    predicate_id=P_IN_BASELINE_24H_ID,
    value=PredicateValue.REFUSED,
    freshness_window_seconds=None,
    reason="test: REFUSED"
)

# Track assertions
assertions = []


def check(name: str, actual: PredicateValue, expected: PredicateValue) -> bool:
    """Run one assertion; track result; print pass/fail."""
    passed = actual == expected
    status = "PASS" if passed else "FAIL"
    print(f"  {status}: {name}")
    if not passed:
        print(f"    expected {expected}, got {actual}")
    assertions.append((name, passed))
    return passed


def main() -> int:
    """Run all 10 assertions from the truth table."""
    all_passed = True

    print("Testing compose_and (4 assertions):")
    all_passed &= check("compose_and([TRUE, TRUE]) == TRUE",
                       compose_and([TRUE_result, TRUE_result]),
                       PredicateValue.TRUE)
    all_passed &= check("compose_and([TRUE, FALSE]) == FALSE",
                       compose_and([TRUE_result, FALSE_result]),
                       PredicateValue.FALSE)
    all_passed &= check("compose_and([TRUE, UNKNOWN]) == UNKNOWN",
                       compose_and([TRUE_result, UNKNOWN_result]),
                       PredicateValue.UNKNOWN)
    all_passed &= check("compose_and([TRUE, REFUSED]) == REFUSED",
                       compose_and([TRUE_result, REFUSED_result]),
                       PredicateValue.REFUSED)

    print("\nTesting compose_or (3 assertions):")
    all_passed &= check("compose_or([FALSE, FALSE]) == FALSE",
                       compose_or([FALSE_result, FALSE_result]),
                       PredicateValue.FALSE)
    all_passed &= check("compose_or([FALSE, TRUE]) == TRUE",
                       compose_or([FALSE_result, TRUE_result]),
                       PredicateValue.TRUE)
    all_passed &= check("compose_or([TRUE, REFUSED]) == REFUSED (REFUSED absorbs)",
                       compose_or([TRUE_result, REFUSED_result]),
                       PredicateValue.REFUSED)

    print("\nTesting negate (3 assertions):")
    all_passed &= check("negate(TRUE) == FALSE",
                       negate(TRUE_result),
                       PredicateValue.FALSE)
    all_passed &= check("negate(UNKNOWN) == UNKNOWN",
                       negate(UNKNOWN_result),
                       PredicateValue.UNKNOWN)
    all_passed &= check("negate(REFUSED) == REFUSED",
                       negate(REFUSED_result),
                       PredicateValue.REFUSED)

    print(f"\n{'='*60}")
    passed_count = sum(1 for _, passed in assertions if passed)
    total_count = len(assertions)
    print(f"Result: {passed_count}/{total_count} assertions passed")
    print(f"{'='*60}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
