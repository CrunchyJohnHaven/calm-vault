"""AAL Component 2 — Cryptographic Action Watermarking.

Append-only, signature-chained, tamper-evident log of AI agent actions,
composing with Bradley-Gavini agent registration (Component 1).
"""
from .action_chain import (
    Block,
    ActionChain,
    block_canonical_bytes,
    block_hash,
    payload_commitment,
)
from .agent_signer import (
    AgentSigner,
    Principal,
    AgentAttestation,
)
from .action_verifier import (
    ChainVerifier,
    VerificationError,
    verify_block,
    verify_chain,
)

__all__ = [
    "Block",
    "ActionChain",
    "block_canonical_bytes",
    "block_hash",
    "payload_commitment",
    "AgentSigner",
    "Principal",
    "AgentAttestation",
    "ChainVerifier",
    "VerificationError",
    "verify_block",
    "verify_chain",
]
