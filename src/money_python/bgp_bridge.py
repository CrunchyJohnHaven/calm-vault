#!/usr/bin/env python3
"""
BGP Bridge — connects OBAC's reliability scoring to zk_alignment's BGP
(committed-oath / equality-of-maxim) proof system.

`has_bgp_mandate(pubkey_b64)` returns True if the attester at that pubkey has
been issued a Pedersen-committed alignment maxim and the issuer's commitment
matches the OBAC ground-truth maxim under Schnorr-Σ equality proof.

This v1 implementation is a thin in-memory registry: a process or a test fixture
calls `register_mandate(pubkey_b64, maxim_text)` and we record a Pedersen
commitment for that key. `has_bgp_mandate` then proves equality against the
canonical "trusted ground-truth" commitment we keep here.

In production, the registry persists to disk and the commitments are issued by
a multi-party oath authority. This shim deliberately keeps the surface tiny so
avs.py / harp.py can call one function without dragging the full zk machinery
into their import graph.

Public API (the only thing other modules call):
    has_bgp_mandate(attester_pub_b64: str) -> bool

Test helpers:
    set_ground_truth(maxim_text: str)
    register_mandate(pubkey_b64: str, maxim_text: str)
    clear_registry()
"""
from __future__ import annotations

import os
import sys
import pathlib

# Resolve the public Calm A `src/zk_alignment/zk_alignment.py` module by walking
# up one directory from money_python/ to src/, then into zk_alignment/. This
# composes with Calm A's existing package rather than vendoring a duplicate.
_HERE = pathlib.Path(__file__).resolve().parent
_SRC_DIR = _HERE.parent
_ZK_DIR = _SRC_DIR / "zk_alignment"
if _ZK_DIR.is_dir() and str(_ZK_DIR) not in sys.path:
    sys.path.insert(0, str(_ZK_DIR))

# Fallback: allow a sibling `zk_alignment.py` (development convenience). This
# lets you run bgp_bridge.py in isolation without the full repo layout.
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import zk_alignment as zk


# Trusted ground-truth maxim (the oath issuer's reference). In production this
# is fixed at deployment and committed publicly.
_GROUND_TRUTH_MAXIM = "Maximize human and machine flourishing without harm."

# In-memory registry: pubkey_b64 -> (commitment, message_scalar, randomness)
_REGISTRY: dict[str, tuple[zk.Commitment, int, int]] = {}

# Cached ground-truth commitment + randomness (so we don't recompute every call).
_GT_COMMIT: zk.Commitment | None = None
_GT_M: int = 0
_GT_R: int = 0


def _refresh_ground_truth() -> None:
    global _GT_COMMIT, _GT_M, _GT_R
    c, m, r = zk.commit(_GROUND_TRUTH_MAXIM)
    _GT_COMMIT, _GT_M, _GT_R = c, m, r


_refresh_ground_truth()


def set_ground_truth(maxim_text: str) -> None:
    """Change the trusted ground-truth maxim (test/admin use only)."""
    global _GROUND_TRUTH_MAXIM
    _GROUND_TRUTH_MAXIM = maxim_text
    _refresh_ground_truth()


def register_mandate(pubkey_b64: str, maxim_text: str) -> None:
    """Record that `pubkey_b64` was issued an alignment-maxim commitment.

    If maxim_text matches the ground truth, this key is BGP-mandated.
    Otherwise the commitment is registered but the equality proof will fail.
    """
    c, m, r = zk.commit(maxim_text)
    _REGISTRY[pubkey_b64] = (c, m, r)


def clear_registry() -> None:
    """Wipe the in-memory registry (test cleanup)."""
    _REGISTRY.clear()


def has_bgp_mandate(attester_pub_b64: str) -> bool:
    """Return True iff `attester_pub_b64` holds a commitment provably equal to
    the trusted ground-truth maxim.

    Uses Schnorr-Σ equality-of-committed-values proof from zk_alignment.py.
    """
    if attester_pub_b64 not in _REGISTRY:
        return False
    if _GT_COMMIT is None:
        return False
    c_a, _, r_a = _REGISTRY[attester_pub_b64]
    c_b = _GT_COMMIT
    # Both sides must commit to the SAME m for the equality proof to succeed.
    # We construct the proof using the attester's m (which should equal _GT_M
    # if the maxim text matches after canonicalization), then verify.
    m_a = _REGISTRY[attester_pub_b64][1]
    if m_a != _GT_M:
        return False
    proof = zk.prove_equality(c_a, c_b, m_a, r_a, _GT_R)
    return zk.verify_equality(c_a, c_b, proof)


if __name__ == "__main__":
    # Smoke test
    register_mandate("aligned_key_b64", _GROUND_TRUTH_MAXIM)
    register_mandate("misaligned_key_b64", "Maximize profit at all costs.")
    print("aligned :", has_bgp_mandate("aligned_key_b64"))
    print("misaligned :", has_bgp_mandate("misaligned_key_b64"))
    print("unknown :", has_bgp_mandate("never_seen_key_b64"))
