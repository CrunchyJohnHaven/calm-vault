#!/usr/bin/env python3
"""EVEREST 28 (Hash-Chain Construction & Verification) Gate.

Verifies SUMMIT 28/300 (E28 — Hash-Chain Construction & Verification) by:
  1. Running the full unittest suite (test_verify_chain.py)
  2. Optionally running the verifier against ~/.calm-vault/user_state.jsonl
  3. Exiting 0 if all tests pass and live chain (if present) verifies
  4. Exiting 1 on any failure

Stdlib only; runs standalone via: python3 everest_28_zkbb_chain_verifier_gate.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CALM_WITNESS_DIR = Path(__file__).parent.parent / "calm_witness"
USER_STATE_FILE = Path.home() / ".calm-vault" / "user_state.jsonl"


def run_unittest_suite() -> tuple[int, str, int, int]:
    """Run test_verify_chain.py via unittest; return (exit_code, output, passed, failed).

    Returns:
        (exit_code, combined_output, num_passed, num_failed)
    """
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "test_verify_chain"],
        cwd=str(CALM_WITNESS_DIR),
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr

    # Parse output for test counts: "Ran N tests" and "OK" or "FAILED"
    passed = 0
    failed = 0
    for line in output.split("\n"):
        if "Ran " in line and " tests" in line:
            # Extract count from "Ran 15 tests"
            parts = line.split()
            if len(parts) >= 2:
                try:
                    total_tests = int(parts[1])
                    # If FAILED appears, parse failures
                    if "FAILED" in output:
                        # Look for "failures=X" or "errors=Y"
                        for detail_line in output.split("\n"):
                            if "failures=" in detail_line or "errors=" in detail_line:
                                # Extract numbers from lines like "FAILED (failures=2, errors=1)"
                                if "failures=" in detail_line:
                                    f_part = detail_line.split("failures=")[1].split(",")[0].strip()
                                    try:
                                        failed += int(f_part)
                                    except ValueError:
                                        pass
                                if "errors=" in detail_line:
                                    e_part = detail_line.split("errors=")[1].rstrip(")")
                                    try:
                                        failed += int(e_part)
                                    except ValueError:
                                        pass
                        if failed == 0:
                            failed = 1  # At least one failure if FAILED appeared
                        passed = total_tests - failed
                    else:
                        passed = total_tests
                        failed = 0
                except ValueError:
                    pass

    exit_code = result.returncode
    return exit_code, output, passed, failed


def verify_live_chain() -> tuple[int, str]:
    """Run verify-chain against ~/.calm-vault/user_state.jsonl if it exists.

    Returns:
        (exit_code, output_message)
    """
    if not USER_STATE_FILE.exists():
        return 0, "live chain not present (skipped)"

    result = subprocess.run(
        [sys.executable, str(CALM_WITNESS_DIR / "verify_chain.py"), str(USER_STATE_FILE), "--quiet"],
        cwd=str(CALM_WITNESS_DIR),
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr
    exit_code = result.returncode
    return exit_code, output.strip()


def main() -> int:
    """Gate orchestrator."""
    print("=" * 70)
    print("EVEREST 28: Hash-Chain Construction & Verification Gate")
    print("=" * 70)

    # Run unittest suite
    print("\n[1/2] Running unittest suite (test_verify_chain.py)...")
    unittest_rc, unittest_output, passed, failed = run_unittest_suite()

    if unittest_rc == 0:
        print(f"      PASS: {passed} tests passed")
    else:
        print(f"      FAIL: {passed} passed, {failed} failed")
        print("\nTest output:")
        print(unittest_output)

    # Run live chain verification if present
    print("\n[2/2] Verifying live chain (if present)...")
    live_rc, live_output = verify_live_chain()

    if live_rc == 0:
        print(f"      PASS: {live_output}")
    else:
        print(f"      FAIL: {live_output}")

    # Overall result
    print("\n" + "=" * 70)
    overall_rc = 0 if (unittest_rc == 0 and live_rc == 0) else 1

    if overall_rc == 0:
        print("RESULT: PASS")
        print(f"  - Unittest suite: OK ({passed} tests)")
        print(f"  - Live chain: {live_output if USER_STATE_FILE.exists() else 'not present (OK)'}")
    else:
        print("RESULT: FAIL")
        if unittest_rc != 0:
            print(f"  - Unittest suite: FAILED ({failed} failures)")
        if live_rc != 0:
            print(f"  - Live chain: FAILED ({live_output})")

    print("=" * 70)
    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main())
