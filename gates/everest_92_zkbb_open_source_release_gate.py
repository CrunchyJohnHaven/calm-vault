#!/usr/bin/env python3
"""Gate for SUMMIT 92/300 (E92 — Open-Source Release).

Checks that the public-release artifacts exist + meet shape requirements.
Exit 0 if all hold, 1 otherwise.
"""
from __future__ import annotations

from pathlib import Path

_ROOT = Path("/Users/johnbradley/AllData/calm_vault_market")


def main() -> int:
    checks = []

    # 1. LICENSE Apache-2.0
    lic = _ROOT / "LICENSE"
    ok = lic.exists() and "Apache" in lic.read_text() and "Version 2.0" in lic.read_text()
    checks.append(("LICENSE Apache-2.0", ok))

    # 2. calm_witness README.md > 500 bytes and mentions Apache-2.0
    rd = _ROOT / "calm_witness" / "README.md"
    ok = rd.exists() and rd.stat().st_size > 500 and "Apache-2.0" in rd.read_text()
    checks.append(("calm_witness/README.md (>500B + Apache-2.0)", ok))

    # 3-7. Package __init__.py existence per package
    for pkg in ("calm_witness", "calm_tenancy", "calm_compass", "calm_stack", "calm_operations"):
        init = _ROOT / pkg / "__init__.py"
        ok = init.exists()
        checks.append((f"{pkg}/__init__.py", ok))

    fails = 0
    for label, ok in checks:
        status = "OK" if ok else "FAIL"
        print(f"{status:4s} {label}")
        if not ok:
            fails += 1
    print()
    print(f"RESULT: {len(checks) - fails}/{len(checks)} checks passed")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
