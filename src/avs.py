#!/usr/bin/env python3
"""
AVS — Alignment Verification Service.

A small service object that two parties can use to verify, over the
Bradley-Gavini Protocol, that they both hold the same operating maxim — without
revealing the maxim itself.

The AVS wraps the primitives from `zk_alignment` (Pedersen-style commitments
+ Schnorr-style equality proof) and issues short-lived, signed alignment
attestations that downstream policy engines (OBAC) and audit logs (HARP) can
consume.

Import contract: AVS imports from zk_alignment directly. The bgp_bridge module
takes care of locating zk_alignment whether it lives as a flat file or as a
package directory; AVS just uses the symbols.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# We rely on bgp_bridge.py to provide a uniform handle to zk_alignment, but it
# is convenient to import directly here too — both layouts (flat file or
# package directory) are supported via the import shim below.

try:  # flat-file layout: src/zk_alignment.py
    from zk_alignment import (  # type: ignore
        Agent as _ZKAgent,
        Commitment as _ZKCommitment,
        EqualityProof as _ZKEqualityProof,
        commit as _zk_commit,
        prove_equality as _zk_prove_equality,
        verify_equality as _zk_verify_equality,
        run_protocol as _zk_run_protocol,
    )
except ImportError:  # package or namespace-package layout: src/zk_alignment/zk_alignment.py
    from zk_alignment.zk_alignment import (  # type: ignore
        Agent as _ZKAgent,
        Commitment as _ZKCommitment,
        EqualityProof as _ZKEqualityProof,
        commit as _zk_commit,
        prove_equality as _zk_prove_equality,
        verify_equality as _zk_verify_equality,
        run_protocol as _zk_run_protocol,
    )


DEFAULT_ATTESTATION_TTL_SEC = 300  # 5 minutes


@dataclass
class AlignmentAttestation:
    """Signed receipt: AVS observed two commitments and a valid equality proof."""
    attestation_id: str
    aligned: bool
    commitment_a_hash: str
    commitment_b_hash: str
    proof_hash: str
    issued_at: int
    expires_at: int
    attestor_pub: str
    signature: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "AlignmentAttestation":
        return AlignmentAttestation(**d)


def _hash_int(value: int) -> str:
    return hashlib.sha256(value.to_bytes(32, "little")).hexdigest()


def _hash_proof(proof: _ZKEqualityProof) -> str:
    h = hashlib.sha256()
    h.update(proof.A.to_bytes(32, "little"))
    h.update(proof.z.to_bytes(32, "little"))
    return h.hexdigest()


class AVS:
    """Alignment Verification Service.

    Run by an oath authority (or any neutral verifier). Two agents send their
    Pedersen-style commitments and an equality proof; AVS checks it and issues
    a short-lived signed attestation that bears witness to the alignment fact
    (without learning the maxim).
    """

    def __init__(
        self,
        private_key: Optional[Ed25519PrivateKey] = None,
        ttl_sec: int = DEFAULT_ATTESTATION_TTL_SEC,
    ) -> None:
        self._sk = private_key or Ed25519PrivateKey.generate()
        self._pk = self._sk.public_key()
        self.pub_hex = self._pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()
        self.ttl_sec = int(ttl_sec)

    # --- primitives passthrough (so callers can stage commits without
    #     reaching into zk_alignment directly) ---

    @staticmethod
    def commit_maxim(maxim_text: str):
        return _zk_commit(maxim_text)

    @staticmethod
    def prove_equality(c_a, c_b, m, r_a, r_b):
        return _zk_prove_equality(c_a, c_b, m, r_a, r_b)

    @staticmethod
    def verify_equality(c_a, c_b, proof) -> bool:
        return _zk_verify_equality(c_a, c_b, proof)

    # --- attestation ---

    def _attestation_payload(
        self, aligned: bool, ca_hash: str, cb_hash: str, proof_hash: str,
        issued_at: int, expires_at: int,
    ) -> bytes:
        return json.dumps(
            {
                "aligned": aligned,
                "ca": ca_hash,
                "cb": cb_hash,
                "proof": proof_hash,
                "issued_at": issued_at,
                "expires_at": expires_at,
            },
            sort_keys=True,
        ).encode("utf-8")

    def attest(
        self, c_a: _ZKCommitment, c_b: _ZKCommitment, proof: _ZKEqualityProof,
        *, now: Optional[int] = None,
    ) -> AlignmentAttestation:
        aligned = _zk_verify_equality(c_a, c_b, proof)
        ca_hash = _hash_int(c_a.value)
        cb_hash = _hash_int(c_b.value)
        proof_hash = _hash_proof(proof)
        issued_at = int(now if now is not None else time.time())
        expires_at = issued_at + self.ttl_sec
        payload = self._attestation_payload(
            aligned, ca_hash, cb_hash, proof_hash, issued_at, expires_at,
        )
        sig = self._sk.sign(payload).hex()
        return AlignmentAttestation(
            attestation_id=str(uuid.uuid4()),
            aligned=aligned,
            commitment_a_hash=ca_hash,
            commitment_b_hash=cb_hash,
            proof_hash=proof_hash,
            issued_at=issued_at,
            expires_at=expires_at,
            attestor_pub=self.pub_hex,
            signature=sig,
        )

    def verify_attestation(
        self, attestation: AlignmentAttestation, *, now: Optional[int] = None,
        expected_attestor_pub: Optional[str] = None,
    ) -> bool:
        if expected_attestor_pub is not None and attestation.attestor_pub != expected_attestor_pub:
            return False
        ts = int(now if now is not None else time.time())
        if ts > attestation.expires_at:
            return False
        if ts < attestation.issued_at:
            return False
        try:
            pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(attestation.attestor_pub))
        except Exception:
            return False
        payload = self._attestation_payload(
            attestation.aligned,
            attestation.commitment_a_hash,
            attestation.commitment_b_hash,
            attestation.proof_hash,
            attestation.issued_at,
            attestation.expires_at,
        )
        try:
            pk.verify(bytes.fromhex(attestation.signature), payload)
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False


__all__ = [
    "AVS",
    "AlignmentAttestation",
    "DEFAULT_ATTESTATION_TTL_SEC",
]
