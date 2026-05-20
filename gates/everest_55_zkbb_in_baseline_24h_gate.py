#!/usr/bin/env python3
"""SUMMIT 55/300 (E55) ZKBB in_baseline_24h predicate reference implementation gate.

Verifies that the in_baseline_24h predicate reference implementation (ZKBB)
passes all published conformance vectors from the calm_witness layer.

Exit 0 if all conformance vectors pass. Exit 1 otherwise.
"""
import subprocess
import sys
from pathlib import Path


def run_gate() -> int:
    """Run conformance_vectors.py --check and return exit code."""
    # Locate the calm_witness directory relative to this script.
    gates_dir = Path(__file__).resolve().parent
    vault_root = gates_dir.parent
    calm_witness_dir = vault_root / "calm_witness"

    # Verify required files exist.
    predicates_file = calm_witness_dir / "predicates.py"
    conformance_file = calm_witness_dir / "conformance_vectors.py"

    if not predicates_file.exists():
        print(f"FAIL: {predicates_file} not found")
        return 1

    if not conformance_file.exists():
        print(f"FAIL: {conformance_file} not found")
        return 1

    # Run conformance_vectors.py --check from calm_witness directory.
    try:
        result = subprocess.run(
            ["python3", "conformance_vectors.py", "--check"],
            cwd=str(calm_witness_dir),
            capture_output=False,
            text=True,
        )
        exit_code = result.returncode
    except Exception as e:
        print(f"FAIL: Exception running conformance check: {e}")
        return 1

    # Return the exit code from conformance_vectors.py --check.
    return exit_code


if __name__ == "__main__":
    sys.exit(run_gate())
