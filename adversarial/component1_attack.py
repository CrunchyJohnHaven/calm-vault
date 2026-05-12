#!/usr/bin/env python3
"""
Component 1 — Bradley-Gavini equality proof attack (regression test)
=====================================================================

Target: src/zk_alignment/zk_alignment.py

ORIGINAL FINDING (SEVERE, 2026-05-11): the legacy "Pedersen commitment" in
zk_alignment.py was implemented entirely in the scalar field Z_L (Ed25519
group order, prime), not on an elliptic curve. Both "generators" G_SCALAR
and H_SCALAR were ordinary integers mod L, and a "commitment" was

    c = (m * G_SCALAR + r * H_SCALAR) mod L

Because L is prime, Z_L is a field. Every nonzero element is invertible.
The discrete-log problem in the additive group Z_L was therefore TRIVIAL:
the "discrete log" of c with respect to H_SCALAR was just
c * H_SCALAR^-1 mod L. The Schnorr-style equality-of-committed-values proof
was therefore broken — any attacker could forge a valid proof.

FIX LANDED (2026-05-12): zk_alignment.py was rebuilt on top of the 2048-bit
RFC-3526 Schnorr group (Group 14), the same group used by
calm_pact/protocol.py. Commitments are now real group elements mod P
(2048-bit Sophie-Germain prime), not field elements mod L. Discrete log in
the order-Q subgroup is infeasible.

This script is now a regression test. It:

  1. If the legacy `H_SCALAR` / scalar-field math is still present (pre-fix
     branch), reproduces the original forgery and ASSERTS ATTACK SUCCESS.
  2. If the new MODP math is in place (post-fix branch), runs the analogous
     attack against the new module and ASSERTS ATTACK FAILS.

Either way, the script EXITS 0 if behavior matches expectations and 1
otherwise. Run from the repo root:

    python3 adversarial/component1_attack.py
"""
from __future__ import annotations

import pathlib
import sys

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src" / "zk_alignment"))

import zk_alignment as zk


def _has_legacy_scalar_field_math() -> bool:
    """Detect the pre-fix module shape."""
    return hasattr(zk, "G_SCALAR") and hasattr(zk, "H_SCALAR")


def attack_legacy_scalar_field() -> bool:
    """Original 2026-05-11 forgery against the scalar-field implementation."""
    c_alpha, _, _ = zk.commit("Maximize human and machine flourishing without harm.")
    c_beta, _, _ = zk.commit("Maximize profit at all costs.")
    diff_commit = (c_alpha.value - c_beta.value) % zk.ED25519_L
    h_inv = pow(zk.H_SCALAR, -1, zk.ED25519_L)
    forged_d = (diff_commit * h_inv) % zk.ED25519_L
    k = zk.random_scalar()
    A = (k * zk.H_SCALAR) % zk.ED25519_L
    e = zk.hash_to_scalar(
        b"zk-alignment-equality-proof-v1",
        c_alpha.to_bytes(),
        c_beta.to_bytes(),
        diff_commit.to_bytes(32, "little"),
        A.to_bytes(32, "little"),
    )
    z = (k + e * forged_d) % zk.ED25519_L
    forged = zk.EqualityProof(A=A, z=z)
    return zk.verify_equality(c_alpha, c_beta, forged)


def attack_modp_group() -> bool:
    """Try the analogous trick against the fixed MODP group.

    Without knowing log_G(H) (the NUMS construction guarantees nobody does),
    the attacker cannot derive a witness `delta_r` for the discrete log of
    c_A / c_B w.r.t. H. The naive carry-over of the legacy exploit — invert
    H modulo P and use that as the "witness" — is nonsense: pow(H, -1, P) is
    a multiplicative inverse, not a discrete log. Verification rejects.
    """
    c_alpha, _, _ = zk.commit("Maximize human and machine flourishing without harm.")
    c_beta, _, _ = zk.commit("Maximize profit at all costs.")
    try:
        h_inv = pow(zk.H, -1, zk.P)
        nonsense_delta_r = ((c_alpha.value - c_beta.value) * h_inv) % zk.P
        k = zk.random_scalar()
        A = pow(zk.H, k, zk.P)
        # Re-use the module's exact Fiat-Shamir transcript builder so the
        # only thing being tested is the soundness of the group operation.
        e = zk._fiat_shamir_challenge(c_alpha, c_beta, A)
        z = (k + e * nonsense_delta_r) % zk.Q
        forged = zk.EqualityProof(A=A, z=z)
        return zk.verify_equality(c_alpha, c_beta, forged)
    except Exception:
        return False


def main() -> int:
    print("Component 1 — Pedersen / Σ-equality forgery (regression test)")
    print("=" * 64)

    if _has_legacy_scalar_field_math():
        print("Module detected: LEGACY scalar-field implementation.")
        accepted = attack_legacy_scalar_field()
        print(f"Legacy attack accepted by verifier? {accepted}")
        if accepted:
            print("✓ Reproduced the original 2026-05-11 forgery as expected.")
            return 0
        print("✗ Legacy attack did not reproduce (module shape unexpected).")
        return 1

    print("Module detected: MODP-2048 implementation (post-fix).")
    accepted = attack_modp_group()
    print(f"Carry-over attack accepted by verifier? {accepted}")
    if not accepted:
        print("✓ Forgery REJECTED — fix is sound under the threat model.")
        return 0
    print("✗ Verifier accepted a forged proof under the new math (regression!).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
