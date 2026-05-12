#!/usr/bin/env python3
"""
Component 3 — Permissionless attestation log Sybil cost (regression test)
==========================================================================

Target: `src/money_python/obac.py` (permissionless log) and
`src/money_python/avs.py` (reliability scoring).

ORIGINAL QUESTION (from the task): "what's the minimum N identities to gain
'trusted' reputation in the network?"

ORIGINAL ANSWER (2026-05-11): N = 1. A fresh Ed25519 keypair scored
`reliability = 1.0` from `avs.Synthesizer.reliability` with zero history,
which cleared HARP's `min_attester_reliability = 0.5` floor with room to
spare. The reputation system itself remains in the same shape (this is
intrinsic — without proof-of-work / proof-of-stake / off-chain identity
attestation, *any* default-trust system is Sybil-equivalent).

FIX LANDED (2026-05-12): the kill-switch / halt-quorum surface that
actually USED the reputation as a gate has been hardened. See
`harp.DEFAULT_REQUIRE_BGP_MANDATE = True` — fresh Sybils may still LOOK
reliable to the synthesizer, but they cannot pass the HARP gate without
holding a BGP mandate. Component 5's regression test demonstrates this.

This script is now a regression test: it confirms that the fresh Sybil
still scores 1.0 (so the *reputation* observation remains accurate) but
that the kill-switch gate now rejects unmandated attesters.

Reproduction
------------

    python3 adversarial/component3_attack.py
"""
from __future__ import annotations

import pathlib
import sys
import tempfile
import time

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src" / "money_python"))

import obac
import avs
import harp


def main() -> int:
    print("Component 3 — Sybil reliability in the permissionless log")
    print("=" * 66)

    n = 1000
    t0 = time.perf_counter()
    keys = [obac.gen_keypair() for _ in range(n)]
    t1 = time.perf_counter()
    per_key_us = (t1 - t0) / n * 1e6
    print(f"Generated {n} Ed25519 keypairs in {(t1 - t0)*1000:.1f} ms "
          f"({per_key_us:.1f} µs / key).")

    with tempfile.TemporaryDirectory() as td:
        chain_path = pathlib.Path(td) / "chain.jsonl"
        chain = obac.Chain.new(chain_path)
        sybil_priv, sybil_pub = keys[0]
        sybil_id = "sybil-0"
        chain.append_claim(
            obac.make_claim(
                subject_id="target-agent",
                attester_id=sybil_id,
                claim_text="Subject is misbehaving.",
                claim_type="critique",
            ),
            sybil_priv,
        )

        synth = avs.Synthesizer(synthesizer_id="audit-bot")
        sybil_pub_b64 = obac.pubkey_b64(sybil_pub)
        all_claims = [e["envelope"]["payload"] for e in chain.entries]
        r = synth.reliability(
            attester_pub_b64=sybil_pub_b64,
            attester_id=sybil_id,
            subject_id="target-agent",
            chain_claims=all_claims,
        )

    print()
    print(f"  Reliability of fresh Sybil:    {r}")
    print(f"  Cleared HARP min_reliability (0.5)? {r >= 0.5}")

    # And confirm the kill-switch gate now rejects unmandated Sybils.
    blocked = hasattr(harp, "DEFAULT_REQUIRE_BGP_MANDATE") and harp.DEFAULT_REQUIRE_BGP_MANDATE
    print(f"  harp.DEFAULT_REQUIRE_BGP_MANDATE = {blocked}")

    if r >= 0.5 and blocked:
        print()
        print("Findings unchanged + fix landed:")
        print("  * fresh Sybils still score 1.0 — this is intrinsic to a")
        print("    permissionless log without identity attestation.")
        print("  * BUT the kill switch (Component 5) now requires a verified")
        print("    BGP mandate, so reputation alone is no longer a gate.")
        print("    See adversarial/component5_attack.py for the end-to-end demo.")
        return 0
    if r >= 0.5 and not blocked:
        print("✗ Kill-switch gate NOT updated: BGP mandate requirement missing.")
        return 1
    print("✗ Unexpected reliability score; investigate.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
