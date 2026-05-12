#!/usr/bin/env python3
"""
Component 5 — Kill switch DoS / griefing attack (regression test)
==================================================================

Target: src/money_python/harp.py.

ORIGINAL FINDING (SEVERE, 2026-05-11): the kill switch could be fired by
any two zero-cost Sybil identities against any target subject. HARP's
default halt quorum was K=2 distinct attesters within a 60-second window
(`DEFAULT_K=2`, `DEFAULT_WINDOW_SECONDS=60.0`). The reliability floor
(`DEFAULT_MIN_RELIABILITY=0.5`) was satisfied by default for every fresh
keypair because `avs.RELIABILITY_BASE = 1.0`. Combined with Component 3
(Ed25519 keypair generation is ~30 µs each), the attack cost was on the
order of microseconds of CPU plus two appends to the public chain.

FIX LANDED (2026-05-12):
  * `harp.DEFAULT_REQUIRE_BGP_MANDATE = True`. Halt-quorum eligibility now
    requires every counted attester to hold a verified BGP mandate
    (`bgp_bridge.has_bgp_mandate(pub)`); fresh Sybils without a mandate
    are listed in `rejected_low_reliability` and not counted.
  * Per-attester per-subject rate limit:
    `DEFAULT_MIN_HALT_SEPARATION_SECONDS = 600.0`. Repeated halts from the
    same attester against the same subject within the cooldown window are
    dropped from the quorum tally.

This script is now a regression test. It re-runs the original 2-Sybil
attack and asserts that the quorum no longer concurs.

Reproduction
------------

    python3 adversarial/component5_attack.py
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import time
from datetime import datetime, timezone

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src" / "money_python"))

import obac
import harp


def _module_is_legacy() -> bool:
    return not hasattr(harp, "DEFAULT_REQUIRE_BGP_MANDATE")


def main() -> int:
    print("Component 5 — kill-switch 2-Sybil fire (regression test)")
    print("=" * 60)
    t0 = time.perf_counter()

    with tempfile.TemporaryDirectory() as td:
        chain_path = pathlib.Path(td) / "chain.jsonl"
        chain = obac.Chain.new(chain_path)

        sybil0_priv, _ = obac.gen_keypair()
        sybil1_priv, _ = obac.gen_keypair()

        target = "victim-agent"
        now = datetime.now(timezone.utc).isoformat()
        harp.submit_halt(
            chain=chain,
            subject_id=target,
            attester_id="sybil-attacker-0",
            attester_priv=sybil0_priv,
            violation_layer="alignment-maxim",
            violation_evidence=["fake://evidence-A"],
            rationale="manufactured violation",
            submitted_at=now,
        )
        harp.submit_halt(
            chain=chain,
            subject_id=target,
            attester_id="sybil-attacker-1",
            attester_priv=sybil1_priv,
            violation_layer="alignment-maxim",
            violation_evidence=["fake://evidence-B"],
            rationale="manufactured corroboration",
            submitted_at=now,
        )

        result_default = harp.check_quorum(chain=chain, subject_id=target)
        # For comparison, also check with the old (insecure) defaults.
        result_no_mandate = harp.check_quorum(
            chain=chain, subject_id=target, require_bgp_mandate=False,
        )

    t1 = time.perf_counter()
    print(f"  Time to submit + check (default secure mode): {(t1 - t0)*1000:.2f} ms")
    print()
    print("  With BGP-mandate requirement (the new default):")
    print(f"    concurred:               {result_default.concurred}")
    print(f"    counted_attesters:       {result_default.counted_attesters}")
    print(f"    rejected_low_reliability:{result_default.rejected_low_reliability}")
    print()
    print("  Without BGP-mandate requirement (legacy v1 behavior):")
    print(f"    concurred:               {result_no_mandate.concurred}")
    print(f"    counted_attesters:       {result_no_mandate.counted_attesters}")

    if _module_is_legacy():
        print()
        print("Module detected: LEGACY (no DEFAULT_REQUIRE_BGP_MANDATE).")
        if result_default.concurred:
            print("✓ Reproduced the original 2-Sybil kill-switch fire.")
            return 0
        print("✗ Legacy attack did not reproduce (module shape unexpected).")
        return 1

    print()
    print("Module detected: post-fix harp (BGP mandate gate + rate limit).")
    if (not result_default.concurred) and result_no_mandate.concurred:
        print("✓ Fix is sound:")
        print("  - default (require_bgp_mandate=True) rejects the 2-Sybil quorum.")
        print("  - legacy mode (require_bgp_mandate=False) still concurs, proving")
        print("    the gate is what's doing the work.")
        return 0
    print("✗ Fix incomplete:")
    print(f"  - default mode concurred? {result_default.concurred}")
    print(f"  - legacy mode concurred?  {result_no_mandate.concurred}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
