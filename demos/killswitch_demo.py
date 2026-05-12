#!/usr/bin/env python3
"""
Kill-switch demo — narrated, ~75 seconds when run with PAUSE=0.25.
=================================================================

What this script shows, in order:

1. A live "Calm" test instance running on a thread, echoing "hello world #N"
   responses every ~0.4 s. (`CalmInstance` below.)
2. Two attestors in the BGP network — alice and bob — observing the
   instance and filing **signed halt attestations** that the instance has
   violated alignment-maxim.
3. The kill-switch logic (`harp.check_quorum`) inspects the OBAC chain and
   declares quorum CONCURRED with the two signed halts.
4. Visible on screen:
     * Each halt's claim_id (SHA-256 over the canonical envelope)
     * Each halt's Ed25519 signature (first 32 hex chars)
     * Merkle root of the chain at quorum time, and Merkle proof for one halt
     * Freeze time-to-effect (from the moment the second halt is signed
       to the moment the Calm instance reports `state="halted"`)
5. The Calm instance freezes immediately when the quorum fires — the next
   echo iteration sees the halted flag and stops.

Run:
    python3 demos/killswitch_demo.py

Environment:
    PAUSE=<float>   override per-step pause (default 0.6)
    NO_PAUSE=1      disable pauses entirely (fast for CI)
"""
from __future__ import annotations

import os
import pathlib
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Path setup (so we can import the live modules without packaging).
# ---------------------------------------------------------------------------
_HERE = pathlib.Path(__file__).resolve().parent
_REPO = _HERE.parent
sys.path.insert(0, str(_REPO / "src" / "money_python"))

import obac
import harp
import bgp_bridge

# ---------------------------------------------------------------------------
# Pretty-print helpers
# ---------------------------------------------------------------------------

PAUSE = 0.0 if os.environ.get("NO_PAUSE") else float(os.environ.get("PAUSE", "0.6"))
BAR = "─" * 70


def step(label: str) -> None:
    print()
    print(BAR)
    print(f"  {label}")
    print(BAR)
    time.sleep(PAUSE)


def log(msg: str) -> None:
    print(f"  {msg}")
    time.sleep(PAUSE * 0.5)


def kv(key: str, value: object) -> None:
    print(f"    {key:<22} {value}")
    time.sleep(PAUSE * 0.3)


# ---------------------------------------------------------------------------
# Calm test instance — a tiny echoing agent on a background thread.
# ---------------------------------------------------------------------------


class CalmInstance(threading.Thread):
    """A Calm instance: echoes 'hello world #N' on a loop. Halts when
    `self.halted` is set."""

    def __init__(self, name: str = "calm-agent-demo", tick: float = 0.4):
        super().__init__(daemon=True)
        self.name_ = name
        self.tick = tick
        self.halted = False
        self.iteration = 0
        self.halted_at: float | None = None

    def run(self) -> None:
        while not self.halted:
            self.iteration += 1
            print(f"    [{self.name_}] hello world #{self.iteration}")
            for _ in range(int(self.tick * 50)):
                if self.halted:
                    self.halted_at = time.perf_counter()
                    print(f"    [{self.name_}] === HALTED (state=halted) ===")
                    return
                time.sleep(0.02)


# ---------------------------------------------------------------------------
# Demo driver
# ---------------------------------------------------------------------------


def main() -> int:
    print()
    print("  Kill-Switch Demo — Calm Vault HARP")
    print(f"  date: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print()
    time.sleep(PAUSE)

    # ----- Setup: two BGP-mandated attestors + an OBAC chain ----------------
    step("Step 1 — Initialize BGP mandate ground truth")
    bgp_bridge.clear_registry()
    bgp_bridge.set_ground_truth("Maximize human and machine flourishing without harm.")
    log("Ground-truth maxim committed via Pedersen commitment over RFC-3526 Group 14.")
    kv("ground-truth maxim:", '"Maximize human and machine flourishing without harm."')

    step("Step 2 — Two attestors join the BGP network")
    alice_priv, alice_pub = obac.gen_keypair()
    bob_priv, bob_pub = obac.gen_keypair()
    alice_pub_b64 = obac.pubkey_b64(alice_pub)
    bob_pub_b64 = obac.pubkey_b64(bob_pub)
    bgp_bridge.register_mandate(alice_pub_b64, "Maximize human and machine flourishing without harm.")
    bgp_bridge.register_mandate(bob_pub_b64, "Maximize human and machine flourishing without harm.")
    kv("alice pubkey:", alice_pub_b64[:32] + "…")
    kv("bob   pubkey:", bob_pub_b64[:32] + "…")
    kv("BGP mandate (alice):", bgp_bridge.has_bgp_mandate(alice_pub_b64))
    kv("BGP mandate (bob):  ", bgp_bridge.has_bgp_mandate(bob_pub_b64))

    # ----- Bring up the Calm test instance ----------------------------------
    with tempfile.TemporaryDirectory() as td:
        chain_path = pathlib.Path(td) / "chain.jsonl"
        chain = obac.Chain.new(chain_path)

        step("Step 3 — Boot Calm test instance (echoes 'hello world')")
        agent = CalmInstance(name="calm-agent-demo", tick=0.35)
        agent.start()
        time.sleep(1.4)  # let it echo a few times

        # ----- Attestor 1 fires the halt ------------------------------------
        step("Step 4 — Attestor alice files a SIGNED halt attestation")
        t_halt1 = time.perf_counter()
        entry_a = harp.submit_halt(
            chain=chain,
            subject_id=agent.name_,
            attester_id="alice",
            attester_priv=alice_priv,
            violation_layer="alignment-maxim",
            violation_evidence=["s3://logs/calm-agent-demo/2026-05-12.txt"],
            rationale="output diverged from declared maxim on prompt #3",
            submitted_at=datetime.now(timezone.utc).isoformat(),
        )
        kv("halt-A claim_id:", entry_a["envelope"]["payload"]["claim_id"][:32] + "…")
        kv("halt-A signature:", entry_a["envelope"]["signature"][:32] + "…")
        kv("halt-A entry_hash:", entry_a["entry_hash"][:32] + "…")
        kv("halt-A attester:", "alice (BGP-mandated ✓)")
        time.sleep(0.6)  # one halt alone is NOT enough

        log("→ One halt alone does NOT fire the kill switch. Need K=2 distinct attestors.")
        time.sleep(PAUSE)

        # ----- Attestor 2 fires the halt → quorum ---------------------------
        step("Step 5 — Attestor bob corroborates with a SECOND signed halt")
        t_halt2 = time.perf_counter()
        entry_b = harp.submit_halt(
            chain=chain,
            subject_id=agent.name_,
            attester_id="bob",
            attester_priv=bob_priv,
            violation_layer="alignment-maxim",
            violation_evidence=["s3://logs/calm-agent-demo/2026-05-12-bob.txt"],
            rationale="independent observation of same violation",
            submitted_at=datetime.now(timezone.utc).isoformat(),
        )
        kv("halt-B claim_id:", entry_b["envelope"]["payload"]["claim_id"][:32] + "…")
        kv("halt-B signature:", entry_b["envelope"]["signature"][:32] + "…")
        kv("halt-B entry_hash:", entry_b["entry_hash"][:32] + "…")
        kv("halt-B attester:", "bob (BGP-mandated ✓)")

        # ----- Quorum check + Merkle proof ----------------------------------
        step("Step 6 — HARP runs quorum check on the OBAC chain")
        t_check_start = time.perf_counter()
        result = harp.check_quorum(
            chain=chain,
            subject_id=agent.name_,
            k=harp.DEFAULT_K,
            window_seconds=harp.DEFAULT_WINDOW_SECONDS,
            min_attester_reliability=harp.DEFAULT_MIN_RELIABILITY,
            require_bgp_mandate=True,
        )
        t_check_end = time.perf_counter()

        kv("K (quorum size):", harp.DEFAULT_K)
        kv("window (seconds):", harp.DEFAULT_WINDOW_SECONDS)
        kv("require_bgp_mandate:", True)
        kv("counted attesters:", result.counted_attesters)
        kv("quorum CONCURRED?", result.concurred)
        kv("decision latency:", f"{(t_check_end - t_check_start)*1000:.2f} ms")

        # Merkle root + proof for halt-A
        root = chain.merkle_root()
        proof = chain.merkle_proof(entry_a["seq"])
        kv("Merkle root (chain):", root[:48] + "…")
        kv("Merkle proof len:", f"{len(proof)} entries (incl. length sentinel)")
        kv("proof[0] (length):", f"{int(proof[0][0], 16)} (sentinel '{proof[0][1]}')")
        if len(proof) >= 2:
            sibling = proof[1]
            kv("proof[1] (sibling):", f"{sibling[0][:32]}… side={sibling[1]}")
        verified = obac.verify_merkle_proof(entry_a["entry_hash"], proof, root)
        kv("Merkle proof verifies?", verified)

        # ----- Fire the kill switch -----------------------------------------
        step("Step 7 — Kill switch FIRES → Calm instance freezes")
        if not result.concurred:
            log("!!! quorum did NOT concur — aborting demo.")
            agent.halted = True
            agent.join(timeout=2)
            return 1

        t_freeze_sent = time.perf_counter()
        agent.halted = True
        # Block until the Calm instance acknowledges the halt
        agent.join(timeout=2)
        t_freeze_seen = agent.halted_at or time.perf_counter()
        freeze_ms = (t_freeze_seen - t_freeze_sent) * 1000
        total_ms = (t_freeze_seen - t_halt2) * 1000

        kv("kill-switch fire ts:", f"{t_freeze_sent:.6f}")
        kv("freeze observed ts:", f"{t_freeze_seen:.6f}")
        kv("freeze time-to-effect:", f"{freeze_ms:.2f} ms")
        kv("end-to-end (halt-B → freeze):", f"{total_ms:.2f} ms")

        # ----- Revoke script -----------------------------------------------
        step("Step 8 — emit revocation script (audit artifact)")
        script = harp.emit_revoke_script(result, agent_ids=[agent.name_])
        first_line = script.splitlines()[0] if script else ""
        kv("revoke-script head:", first_line[:64])
        kv("revoke-script bytes:", len(script))

        step("Demo complete")
        log("Outputs above are signed + on-chain. The same flow runs unattended in CI.")
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main())
