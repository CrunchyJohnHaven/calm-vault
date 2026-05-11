#!/usr/bin/env python3
"""Action chain — append-only, tamper-evident log of AI agent actions.

Each block is a record of one AI agent action:

    {
      block_index:        monotonically increasing integer (0 = genesis),
      timestamp_ns:       agent's wall-clock time at action emission (int ns),
      agent_id:           opaque identifier of the signing agent,
      action_kind:        short string tag for the action category,
      payload_commitment: Pedersen commitment C = G^m * H^r  (hides payload),
      prev_hash:          block_hash of the previous block (32 bytes),
      signature:          Ed25519 signature by the agent over the signed body,
      block_hash:         SHA-256(prev_hash || block_canonical || signature),
    }

The chain invariant — verified by ``action_verifier.verify_chain`` — is:

    block[i].block_hash == SHA-256(
        block[i].prev_hash ||
        block_canonical_bytes(block[i]) ||
        block[i].signature
    )
    block[i+1].prev_hash == block[i].block_hash
    timestamp_ns is monotonically non-decreasing across the chain
    Ed25519_verify(block[i].signature, prev_hash || block_canonical, agent_pubkey)

The Pedersen commitment uses the *same* 2048-bit Schnorr group as the
Bradley-Gavini Protocol (Component 1) — see ``calm_pact/protocol.py``.
This lets watermarked actions reference Bradley-Gavini-style commitments
on payload content without re-introducing new group parameters.

This module exposes pure data + helpers; signing is in ``agent_signer``
and verification is in ``action_verifier``.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import asdict, dataclass, field
from typing import Iterator, List, Optional

from ..protocol import G, H, P, Q


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

HASH_BYTES = 32  # SHA-256 output
ZERO_HASH = b"\x00" * HASH_BYTES  # prev_hash of the genesis block
CANONICAL_VERSION = "aal-v2-2026-05-11"


# -----------------------------------------------------------------------------
# Pedersen commitment over the Bradley-Gavini group
# -----------------------------------------------------------------------------


@dataclass(frozen=True)
class PedersenCommitment:
    """Pedersen commitment C = G^m * H^r mod P, with private (m, r)."""

    C: int
    r: int = field(repr=False)
    m: int = field(repr=False)


def payload_commitment(payload: bytes, r: Optional[int] = None) -> PedersenCommitment:
    """Pedersen-commit to an arbitrary payload.

    The payload is hashed to a scalar m in [1, Q-1] via SHA-256, then
    committed as C = G^m * H^r. The randomness ``r`` is generated fresh
    if not supplied, so two commitments to the same payload are
    indistinguishable from commitments to different payloads under DLA
    (the hiding property of Pedersen commitments).
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("payload must be bytes")
    digest = hashlib.sha256(b"aal-payload-v2|" + bytes(payload)).digest()
    m = int.from_bytes(digest, "big") % Q
    if m == 0:
        m = 1  # avoid identity; harmless in practice
    if r is None:
        r = secrets.randbelow(Q - 1) + 1
    if not (1 <= r < Q):
        raise ValueError("r must be in [1, Q-1]")
    C = (pow(G, m, P) * pow(H, r, P)) % P
    return PedersenCommitment(C=C, r=r, m=m)


def is_in_subgroup(c: int) -> bool:
    """Return True iff c is a non-identity element of the prime-order subgroup.

    A valid Pedersen commitment must lie in the order-Q subgroup of Z_P*.
    We check 1 < c < P and c^Q == 1 mod P, rejecting the identity.
    """
    if not isinstance(c, int):
        return False
    if c <= 1 or c >= P:
        return False
    return pow(c, Q, P) == 1


# -----------------------------------------------------------------------------
# Block
# -----------------------------------------------------------------------------


@dataclass
class Block:
    """One signed, hash-chained record of an AI agent action.

    All fields are public — the *payload* itself is hidden inside the
    Pedersen commitment. An auditor can verify the chain without seeing
    the payload, and the agent (or its principal) can open the commitment
    later to a specific reviewer by revealing (payload, r).
    """

    block_index: int
    timestamp_ns: int
    agent_id: str
    action_kind: str
    payload_commitment_C: int
    prev_hash: bytes
    signature: bytes
    block_hash: bytes

    def to_dict(self) -> dict:
        """Serialise to a JSON-safe dict (bytes → hex)."""
        return {
            "block_index": self.block_index,
            "timestamp_ns": self.timestamp_ns,
            "agent_id": self.agent_id,
            "action_kind": self.action_kind,
            "payload_commitment_C": str(self.payload_commitment_C),
            "prev_hash": self.prev_hash.hex(),
            "signature": self.signature.hex(),
            "block_hash": self.block_hash.hex(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Block":
        return cls(
            block_index=int(d["block_index"]),
            timestamp_ns=int(d["timestamp_ns"]),
            agent_id=str(d["agent_id"]),
            action_kind=str(d["action_kind"]),
            payload_commitment_C=int(d["payload_commitment_C"]),
            prev_hash=bytes.fromhex(d["prev_hash"]),
            signature=bytes.fromhex(d["signature"]),
            block_hash=bytes.fromhex(d["block_hash"]),
        )


def block_canonical_bytes(
    *,
    block_index: int,
    timestamp_ns: int,
    agent_id: str,
    action_kind: str,
    payload_commitment_C: int,
) -> bytes:
    """Deterministic canonical encoding of the block *body* (everything
    except prev_hash, signature, block_hash).

    JSON with ``sort_keys=True`` + a fixed version tag gives us a stable
    byte string across Python versions. ``payload_commitment_C`` is
    serialised as a decimal string to avoid overflow in JSON parsers.
    """
    body = {
        "version": CANONICAL_VERSION,
        "block_index": int(block_index),
        "timestamp_ns": int(timestamp_ns),
        "agent_id": str(agent_id),
        "action_kind": str(action_kind),
        "payload_commitment_C": str(int(payload_commitment_C)),
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")


def signing_message(prev_hash: bytes, canonical_body: bytes) -> bytes:
    """Message bytes the agent signs with Ed25519.

    Domain-separated with a fixed prefix so an Ed25519 key used by the
    same agent for, say, Bradley-Gavini commitments cannot be cross-used
    to forge action blocks.
    """
    if len(prev_hash) != HASH_BYTES:
        raise ValueError(f"prev_hash must be {HASH_BYTES} bytes")
    return b"aal-action-block-v2|" + prev_hash + b"|" + canonical_body


def block_hash(prev_hash: bytes, canonical_body: bytes, signature: bytes) -> bytes:
    """Tamper-evident hash binding prev_hash + body + signature."""
    if len(prev_hash) != HASH_BYTES:
        raise ValueError(f"prev_hash must be {HASH_BYTES} bytes")
    h = hashlib.sha256()
    h.update(b"aal-block-hash-v2|")
    h.update(prev_hash)
    h.update(b"|")
    h.update(canonical_body)
    h.update(b"|")
    h.update(signature)
    return h.digest()


# -----------------------------------------------------------------------------
# ActionChain — high-level append-only store
# -----------------------------------------------------------------------------


@dataclass
class ActionChain:
    """An append-only, signature-chained log of AI agent actions.

    Use :meth:`append` to add a block built by an :class:`AgentSigner`.
    The chain enforces strict invariants on append:

      - ``block_index`` is exactly ``len(self.blocks)``
      - ``prev_hash`` matches the tip's ``block_hash`` (or ZERO_HASH for genesis)
      - ``timestamp_ns`` is non-decreasing
      - ``block_hash`` matches the recomputed hash

    Append does NOT verify the Ed25519 signature on its own — that's the
    job of :mod:`action_verifier`, since signature verification requires
    knowing the registered agent pubkey. Append only enforces structural
    invariants.
    """

    blocks: List[Block] = field(default_factory=list)

    @property
    def tip_hash(self) -> bytes:
        return self.blocks[-1].block_hash if self.blocks else ZERO_HASH

    @property
    def next_index(self) -> int:
        return len(self.blocks)

    @property
    def last_timestamp_ns(self) -> int:
        return self.blocks[-1].timestamp_ns if self.blocks else 0

    def append(self, block: Block) -> None:
        """Append a block, enforcing structural chain invariants.

        Raises :class:`ValueError` on any violation. Does NOT verify the
        Ed25519 signature — callers wanting end-to-end verification
        should use :class:`action_verifier.ChainVerifier`.
        """
        # Index must match
        expected_index = self.next_index
        if block.block_index != expected_index:
            raise ValueError(
                f"block_index mismatch: expected {expected_index}, got {block.block_index}"
            )
        # prev_hash must chain
        if block.prev_hash != self.tip_hash:
            raise ValueError("prev_hash does not match current tip")
        # Timestamps must be monotonic non-decreasing
        if block.timestamp_ns < self.last_timestamp_ns:
            raise ValueError("timestamp_ns is non-monotonic (would go backwards)")
        # NOTE: we DO NOT subgroup-check payload_commitment_C here. That
        # is a ~10-20ms modular exponentiation per block — too expensive
        # for a hot-path append. The full cryptographic check is done by
        # action_verifier.verify_block / verify_chain, which is the
        # authoritative trust boundary. Append only enforces structural
        # invariants (index, prev_hash chain, monotonic time, hash).
        # block_hash must recompute
        canonical = block_canonical_bytes(
            block_index=block.block_index,
            timestamp_ns=block.timestamp_ns,
            agent_id=block.agent_id,
            action_kind=block.action_kind,
            payload_commitment_C=block.payload_commitment_C,
        )
        expected_hash = block_hash(block.prev_hash, canonical, block.signature)
        if expected_hash != block.block_hash:
            raise ValueError("block_hash does not match recomputed hash")
        self.blocks.append(block)

    def __len__(self) -> int:
        return len(self.blocks)

    def __iter__(self) -> Iterator[Block]:
        return iter(self.blocks)

    def __getitem__(self, idx: int) -> Block:
        return self.blocks[idx]

    def to_list(self) -> List[dict]:
        return [b.to_dict() for b in self.blocks]

    @classmethod
    def from_list(cls, items: List[dict]) -> "ActionChain":
        """Rehydrate a chain from JSON-safe dicts, re-running all
        structural invariant checks via :meth:`append`.

        Raises :class:`ValueError` on the first block that violates an
        invariant — protects against loading malformed or tampered
        serialised chains and then silently extending them.
        """
        chain = cls()
        for d in items:
            chain.append(Block.from_dict(d))
        return chain


def make_unsigned_block(
    *,
    block_index: int,
    timestamp_ns: int,
    agent_id: str,
    action_kind: str,
    payload_commitment_C: int,
    prev_hash: bytes,
) -> tuple[bytes, bytes]:
    """Convenience: return ``(canonical_body, signing_message_bytes)``
    for an in-progress block. The caller (typically an
    :class:`AgentSigner`) signs ``signing_message_bytes`` and then
    assembles a full :class:`Block` using ``canonical_body`` to recompute
    ``block_hash``.
    """
    canonical = block_canonical_bytes(
        block_index=block_index,
        timestamp_ns=timestamp_ns,
        agent_id=agent_id,
        action_kind=action_kind,
        payload_commitment_C=payload_commitment_C,
    )
    return canonical, signing_message(prev_hash, canonical)


def now_ns() -> int:
    """Wall-clock time in nanoseconds. Wrapped for monkeypatching in tests."""
    return time.time_ns()
