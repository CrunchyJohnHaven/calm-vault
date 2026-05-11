#!/usr/bin/env python3
"""Per-agent Ed25519 signing for the AAL action chain.

Composition with Bradley-Gavini (Component 1):

    Principal (human / org)
        ├── Ed25519 keypair (root of trust)
        ├── registers an agent: signs an AgentAttestation
        │       attestation = sign_principal( agent_id || agent_pubkey || valid_from )
        └── distributes the principal_pubkey publicly so anyone can verify
            both the attestation and (transitively) every action block the
            agent signs.

    Agent
        ├── Ed25519 keypair (per-agent; sees rotation independently of principal)
        ├── holds its principal's AgentAttestation
        └── signs each action block over (prev_hash || canonical_body)

This means:

  * A regulator with only the principal's pubkey can audit every action
    every agent of that principal has ever taken.
  * A compromised agent key cannot retroactively forge older blocks
    (their prev_hash chain is immutable).
  * Rotating an agent key requires a fresh attestation from the principal,
    which is itself publicly verifiable.

This file uses ``cryptography.hazmat.primitives.asymmetric.ed25519`` —
the same library already used elsewhere in calm-vault (see
``src/calm_vault.py``, ``src/zk_alignment/zk_alignment.py``).
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .action_chain import (
    Block,
    block_canonical_bytes,
    block_hash,
    now_ns,
    signing_message,
)


ATTESTATION_DOMAIN = b"aal-attestation-v2|"
ED25519_SIG_BYTES = 64
ED25519_KEY_BYTES = 32


# -----------------------------------------------------------------------------
# Keypair helpers
# -----------------------------------------------------------------------------


def pubkey_bytes(pk: Ed25519PublicKey) -> bytes:
    return pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def privkey_bytes(sk: Ed25519PrivateKey) -> bytes:
    return sk.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def load_pubkey(b: bytes) -> Ed25519PublicKey:
    if len(b) != ED25519_KEY_BYTES:
        raise ValueError("Ed25519 pubkey must be 32 bytes")
    return Ed25519PublicKey.from_public_bytes(b)


def load_privkey(b: bytes) -> Ed25519PrivateKey:
    if len(b) != ED25519_KEY_BYTES:
        raise ValueError("Ed25519 seed must be 32 bytes")
    return Ed25519PrivateKey.from_private_bytes(b)


# -----------------------------------------------------------------------------
# Attestation: principal signs (agent_id, agent_pubkey, valid_from)
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class AgentAttestation:
    """Principal's signed statement that an agent_id maps to an agent pubkey.

    Anyone holding the principal's pubkey can verify the attestation and
    thereby trust action blocks signed by that agent pubkey, until
    ``valid_until_ns`` (if set) or until the principal explicitly rotates
    the agent.
    """

    principal_pubkey: bytes  # 32 bytes Ed25519
    agent_id: str
    agent_pubkey: bytes  # 32 bytes Ed25519
    valid_from_ns: int
    valid_until_ns: Optional[int]  # None = no expiry
    signature: bytes  # principal's Ed25519 sig over the canonical body

    def canonical_body(self) -> bytes:
        body = {
            "version": "aal-attestation-v2",
            "principal_pubkey": self.principal_pubkey.hex(),
            "agent_id": self.agent_id,
            "agent_pubkey": self.agent_pubkey.hex(),
            "valid_from_ns": int(self.valid_from_ns),
            "valid_until_ns": (
                None if self.valid_until_ns is None else int(self.valid_until_ns)
            ),
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def signing_payload(self) -> bytes:
        return ATTESTATION_DOMAIN + self.canonical_body()

    def verify(self) -> bool:
        """Verify the attestation under its embedded principal_pubkey."""
        try:
            pk = load_pubkey(self.principal_pubkey)
            pk.verify(self.signature, self.signing_payload())
        except (InvalidSignature, ValueError, TypeError):
            return False
        return True

    def is_active_at(self, now: int) -> bool:
        if now < self.valid_from_ns:
            return False
        if self.valid_until_ns is not None and now > self.valid_until_ns:
            return False
        return True

    def to_dict(self) -> dict:
        return {
            "principal_pubkey": self.principal_pubkey.hex(),
            "agent_id": self.agent_id,
            "agent_pubkey": self.agent_pubkey.hex(),
            "valid_from_ns": self.valid_from_ns,
            "valid_until_ns": self.valid_until_ns,
            "signature": self.signature.hex(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "AgentAttestation":
        return cls(
            principal_pubkey=bytes.fromhex(d["principal_pubkey"]),
            agent_id=str(d["agent_id"]),
            agent_pubkey=bytes.fromhex(d["agent_pubkey"]),
            valid_from_ns=int(d["valid_from_ns"]),
            valid_until_ns=(
                None if d.get("valid_until_ns") is None else int(d["valid_until_ns"])
            ),
            signature=bytes.fromhex(d["signature"]),
        )


# -----------------------------------------------------------------------------
# Principal — the human / organisation that registers agents
# -----------------------------------------------------------------------------


@dataclass
class Principal:
    """A human or organisation that owns one or more AI agents.

    Holds the Ed25519 master keypair. The principal *registers* an agent
    by signing an :class:`AgentAttestation` that binds an agent_id to an
    agent pubkey for a validity window.
    """

    private_key: Ed25519PrivateKey
    public_key: Ed25519PublicKey = field(init=False)

    def __post_init__(self) -> None:
        self.public_key = self.private_key.public_key()

    @classmethod
    def generate(cls) -> "Principal":
        return cls(private_key=Ed25519PrivateKey.generate())

    @classmethod
    def from_seed(cls, seed: bytes) -> "Principal":
        return cls(private_key=load_privkey(seed))

    @property
    def pubkey_bytes(self) -> bytes:
        return pubkey_bytes(self.public_key)

    def register_agent(
        self,
        *,
        agent_id: str,
        agent_pubkey: bytes,
        valid_from_ns: Optional[int] = None,
        valid_until_ns: Optional[int] = None,
    ) -> AgentAttestation:
        """Sign an :class:`AgentAttestation` for the given agent."""
        if len(agent_pubkey) != ED25519_KEY_BYTES:
            raise ValueError("agent_pubkey must be 32 bytes")
        if not agent_id:
            raise ValueError("agent_id must be non-empty")
        if valid_from_ns is None:
            valid_from_ns = now_ns()
        if valid_until_ns is not None and valid_until_ns < valid_from_ns:
            raise ValueError("valid_until_ns must be >= valid_from_ns")
        # Build the attestation unsigned, sign it, return final.
        attestation_unsigned = AgentAttestation(
            principal_pubkey=self.pubkey_bytes,
            agent_id=agent_id,
            agent_pubkey=agent_pubkey,
            valid_from_ns=valid_from_ns,
            valid_until_ns=valid_until_ns,
            signature=b"",
        )
        sig = self.private_key.sign(attestation_unsigned.signing_payload())
        return AgentAttestation(
            principal_pubkey=self.pubkey_bytes,
            agent_id=agent_id,
            agent_pubkey=agent_pubkey,
            valid_from_ns=valid_from_ns,
            valid_until_ns=valid_until_ns,
            signature=sig,
        )


# -----------------------------------------------------------------------------
# AgentSigner — produces signed action blocks
# -----------------------------------------------------------------------------


@dataclass
class AgentSigner:
    """Per-agent Ed25519 signer that emits :class:`Block` instances.

    Build one of these per agent process. It holds the agent's private
    key (which should NEVER leave the agent's secure enclave / process
    memory in production) and the principal's signed :class:`AgentAttestation`.
    """

    agent_id: str
    private_key: Ed25519PrivateKey
    attestation: AgentAttestation
    public_key: Ed25519PublicKey = field(init=False)

    def __post_init__(self) -> None:
        self.public_key = self.private_key.public_key()
        # Sanity-check: the attestation must be for *this* agent.
        if self.attestation.agent_id != self.agent_id:
            raise ValueError("attestation.agent_id does not match agent_id")
        if self.attestation.agent_pubkey != self.pubkey_bytes:
            raise ValueError("attestation.agent_pubkey does not match the signer's pubkey")
        if not self.attestation.verify():
            raise ValueError("attestation does not verify under its principal_pubkey")

    @property
    def pubkey_bytes(self) -> bytes:
        return pubkey_bytes(self.public_key)

    @classmethod
    def create(
        cls,
        *,
        principal: Principal,
        agent_id: str,
        valid_until_ns: Optional[int] = None,
    ) -> Tuple["AgentSigner", AgentAttestation]:
        """Generate a fresh Ed25519 agent keypair, get it attested by the
        principal, and return a ready-to-use :class:`AgentSigner`.
        """
        sk = Ed25519PrivateKey.generate()
        pk_bytes = pubkey_bytes(sk.public_key())
        attestation = principal.register_agent(
            agent_id=agent_id,
            agent_pubkey=pk_bytes,
            valid_until_ns=valid_until_ns,
        )
        signer = cls(agent_id=agent_id, private_key=sk, attestation=attestation)
        return signer, attestation

    def sign_action(
        self,
        *,
        action_kind: str,
        payload_commitment_C: int,
        prev_hash: bytes,
        block_index: int,
        timestamp_ns: Optional[int] = None,
    ) -> Block:
        """Build + sign one :class:`Block`.

        The caller is responsible for sourcing ``prev_hash`` (the chain
        tip) and ``block_index`` (chain length). Typically the caller is
        an :class:`ActionChain` wrapper that drives this for each action.
        """
        if timestamp_ns is None:
            timestamp_ns = now_ns()
        canonical = block_canonical_bytes(
            block_index=block_index,
            timestamp_ns=timestamp_ns,
            agent_id=self.agent_id,
            action_kind=action_kind,
            payload_commitment_C=payload_commitment_C,
        )
        msg = signing_message(prev_hash, canonical)
        signature = self.private_key.sign(msg)
        h = block_hash(prev_hash, canonical, signature)
        return Block(
            block_index=block_index,
            timestamp_ns=timestamp_ns,
            agent_id=self.agent_id,
            action_kind=action_kind,
            payload_commitment_C=payload_commitment_C,
            prev_hash=prev_hash,
            signature=signature,
            block_hash=h,
        )
