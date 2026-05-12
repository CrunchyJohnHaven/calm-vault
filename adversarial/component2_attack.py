#!/usr/bin/env python3
"""
Component 2 — OBAC Merkle chain attack (regression test)
=========================================================

Target: src/money_python/obac.py.

ORIGINAL FINDING (MODERATE, 2026-05-11): the Merkle tree used the classic
CVE-2012-2459 "duplicate-the-last-leaf-when-odd" pattern. Internal nodes
were not domain-separated from leaves and chain length was not committed
in the root. Two distinct entry-hash lists produced the same Merkle root:

    leaves L  = [h0, h1, h2]             (odd → duplicate last)
    leaves L' = [h0, h1, h2, h2]         (even, no duplication)

Both yielded identical roots:

    R = SHA256( SHA256(h0||h1) || SHA256(h2||h2) )

A verifier cannot distinguish them, so a prover could forge a Merkle proof
for a phantom leaf at index 3 in a 3-entry chain.

FIX LANDED (2026-05-12): leaves are now hashed under domain tag 0x00,
internal nodes under tag 0x01, and the final root commits the chain length
under tag 0x02. `merkle_proof` carries the length as a sentinel side='N'
entry; `verify_merkle_proof` rejects proofs that omit the sentinel.

This script is now a regression test. It tries both halves of the original
exploit and asserts they FAIL against the fixed code (and SUCCEED against
the legacy code, if the module is still on the pre-fix branch).

Reproduction
------------

    python3 adversarial/component2_attack.py
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src" / "money_python"))

import obac


def _module_is_legacy() -> bool:
    """The legacy module had no _MERKLE_LEAF_TAG."""
    return not hasattr(obac, "_MERKLE_LEAF_TAG")


def collision_attempt():
    """Build two leaf lists that collide under the legacy Merkle algorithm."""
    h0 = hashlib.sha256(b"entry-0").hexdigest()
    h1 = hashlib.sha256(b"entry-1").hexdigest()
    h2 = hashlib.sha256(b"entry-2").hexdigest()
    leaves_3 = [h0, h1, h2]
    leaves_4 = [h0, h1, h2, h2]
    root_3 = obac.merkle_root(leaves_3)
    root_4 = obac.merkle_root(leaves_4)
    return h0, h1, h2, root_3, root_4


def phantom_proof_attempt():
    """Re-create the legacy phantom proof and check the verifier still rejects it."""
    h0 = hashlib.sha256(b"entry-0").hexdigest()
    h1 = hashlib.sha256(b"entry-1").hexdigest()
    h2 = hashlib.sha256(b"entry-2").hexdigest()
    # Pretend we have a 3-entry chain and try to forge inclusion of h2 at
    # phantom index 3 using the "duplicate-last" expansion.
    real_root = obac.merkle_root([h0, h1, h2])
    # Build the legacy-shape proof entirely by hand (no length sentinel).
    legacy_proof = [
        (h2, "L"),
        (hashlib.sha256(bytes.fromhex(h0) + bytes.fromhex(h1)).hexdigest(), "L"),
    ]
    return real_root, obac.verify_merkle_proof(h2, legacy_proof, real_root)


def main() -> int:
    print("Component 2 — Merkle duplicate-last-leaf forgery (regression test)")
    print("=" * 66)

    h0, h1, h2, root_3, root_4 = collision_attempt()
    legacy_attack_succeeded = root_3 == root_4
    print(f"root over [h0, h1, h2]     = {root_3}")
    print(f"root over [h0, h1, h2, h2] = {root_4}")
    print(f"Collision present?          {legacy_attack_succeeded}")

    real_root, phantom_accepted = phantom_proof_attempt()
    print(f"Legacy-shape phantom proof accepted? {phantom_accepted}")

    if _module_is_legacy():
        print()
        print("Module detected: LEGACY (no domain separation).")
        if legacy_attack_succeeded and phantom_accepted:
            print("✓ Reproduced the original 2026-05-11 collision + phantom proof.")
            return 0
        print("✗ Legacy attack did not reproduce (module shape unexpected).")
        return 1

    print()
    print("Module detected: domain-separated, length-committed (post-fix).")
    if (not legacy_attack_succeeded) and (not phantom_accepted):
        print("✓ Both halves of the original attack are REJECTED by the fixed code.")
        return 0
    print("✗ Fix appears incomplete:")
    print(f"  - collision still present? {legacy_attack_succeeded}")
    print(f"  - phantom proof still accepted? {phantom_accepted}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
