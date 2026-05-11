#!/usr/bin/env python3
"""Verifier for AAL action chains.

Given a chain of :class:`Block`s and an *agent registry* mapping
agent_id → :class:`AgentAttestation` (where the attestation is signed
by a trusted principal), the verifier checks:

  1. Each attestation in the registry verifies under its embedded
     principal pubkey AND that principal pubkey is in the caller's
     trusted-principal allow-list (if provided).
  2. For every block in the chain:
     a. ``block.block_hash == SHA-256(prev_hash || canonical || signature)``
     b. ``block.prev_hash`` matches the previous block's ``block_hash``
        (or ZERO_HASH for index 0)
     c. ``block.block_index`` equals its position in the chain
     d. ``block.timestamp_ns`` is non-decreasing across the chain
     e. ``block.payload_commitment_C`` is in the order-Q Pedersen subgroup
     f. ``block.signature`` is a valid Ed25519 signature, by the agent
        pubkey from the registry, over the canonical signing message.
     g. The agent's attestation was active at ``block.timestamp_ns``.

Any failure raises :class:`VerificationError` (single-block helpers) or
returns ``False`` (chain helpers), depending on which entry point is
called.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence

from cryptography.exceptions import InvalidSignature

from .action_chain import (
    Block,
    ZERO_HASH,
    block_canonical_bytes,
    block_hash,
    is_in_subgroup,
    signing_message,
)
from .agent_signer import AgentAttestation, load_pubkey


class VerificationError(Exception):
    """Raised when a single-block verification fails. Carries a short reason."""


# -----------------------------------------------------------------------------
# Single-block verification
# -----------------------------------------------------------------------------


def verify_block(
    block: Block,
    *,
    expected_prev_hash: bytes,
    expected_index: int,
    expected_min_timestamp_ns: int,
    attestation: AgentAttestation,
    trusted_principals: Optional[Iterable[bytes]] = None,
) -> bool:
    """Verify one block against expected chain context.

    Raises :class:`VerificationError` on failure. Returns True on success.
    """
    # 1. structural
    if block.block_index != expected_index:
        raise VerificationError(
            f"block_index mismatch: expected {expected_index}, got {block.block_index}"
        )
    if block.prev_hash != expected_prev_hash:
        raise VerificationError("prev_hash does not match previous block's hash")
    if block.timestamp_ns < expected_min_timestamp_ns:
        raise VerificationError("timestamp_ns is non-monotonic")
    if not is_in_subgroup(block.payload_commitment_C):
        raise VerificationError("payload_commitment_C is not a valid Pedersen element")

    # 2. block_hash recomputes
    canonical = block_canonical_bytes(
        block_index=block.block_index,
        timestamp_ns=block.timestamp_ns,
        agent_id=block.agent_id,
        action_kind=block.action_kind,
        payload_commitment_C=block.payload_commitment_C,
    )
    expected_hash = block_hash(block.prev_hash, canonical, block.signature)
    if expected_hash != block.block_hash:
        raise VerificationError("block_hash does not match recomputed value")

    # 3. attestation matches the agent_id and is active at the block's timestamp
    if attestation.agent_id != block.agent_id:
        raise VerificationError("attestation.agent_id does not match block.agent_id")
    if not attestation.verify():
        raise VerificationError("attestation signature does not verify")
    if not attestation.is_active_at(block.timestamp_ns):
        raise VerificationError(
            "attestation was not active at block.timestamp_ns"
        )
    if trusted_principals is not None:
        trusted_set = {bytes(p) for p in trusted_principals}
        if attestation.principal_pubkey not in trusted_set:
            raise VerificationError("attestation principal is not in trusted set")

    # 4. Ed25519 signature on the canonical signing message
    msg = signing_message(block.prev_hash, canonical)
    try:
        pk = load_pubkey(attestation.agent_pubkey)
        pk.verify(block.signature, msg)
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise VerificationError(f"Ed25519 signature did not verify: {exc}") from None
    return True


# -----------------------------------------------------------------------------
# Whole-chain verification
# -----------------------------------------------------------------------------


@dataclass
class ChainVerifier:
    """Verifier for an entire :class:`ActionChain`.

    Construct with an *agent registry* — a dict mapping ``agent_id`` →
    :class:`AgentAttestation` — and (optionally) a set of trusted
    principal pubkeys. ``verify`` returns True iff the entire chain
    satisfies every invariant above.
    """

    registry: Dict[str, AgentAttestation]
    trusted_principals: Optional[Sequence[bytes]] = None
    last_error: Optional[str] = field(default=None, init=False)

    def verify(self, chain: Sequence[Block]) -> bool:
        self.last_error = None
        prev_hash = ZERO_HASH
        min_ts = 0
        for i, block in enumerate(chain):
            attestation = self.registry.get(block.agent_id)
            if attestation is None:
                self.last_error = (
                    f"block {i}: agent_id {block.agent_id!r} not in registry"
                )
                return False
            try:
                verify_block(
                    block,
                    expected_prev_hash=prev_hash,
                    expected_index=i,
                    expected_min_timestamp_ns=min_ts,
                    attestation=attestation,
                    trusted_principals=self.trusted_principals,
                )
            except VerificationError as e:
                self.last_error = f"block {i}: {e}"
                return False
            prev_hash = block.block_hash
            min_ts = block.timestamp_ns
        return True


def verify_chain(
    chain: Sequence[Block],
    registry: Dict[str, AgentAttestation],
    *,
    trusted_principals: Optional[Sequence[bytes]] = None,
) -> bool:
    """Convenience: build a :class:`ChainVerifier` and run it."""
    return ChainVerifier(
        registry=registry, trusted_principals=trusted_principals
    ).verify(chain)
