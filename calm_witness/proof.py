"""calm_witness.proof — Pedersen + Σ-protocol scaffolding (Everests 44, 45).

This module defines the API the rest of the package uses to commit to and prove
predicate values. v0 ships **placeholder** implementations that produce hex
strings of the correct shape but do not yet implement the underlying group ops
— that lands when `curve25519-dalek` bindings (or the in-repo zkac-v0 Rust crate)
are wired in. The placeholder shape exists so that disclosure.py can be written
end-to-end today and the swap to real crypto is field-by-field, not a rewrite.

The math that the real implementation will encode:

  Group:      Ristretto255 (over curve25519), prime order q.
  Generators: g, h ∈ G with log_g(h) unknown (Pedersen "no trapdoor" property).
              In code: g = the standard Ristretto basepoint;
                       h = HashToCurve(b"calm-witness-pedersen-h-v0").

  Pedersen commitment of a scalar s with randomness r:
      Com(s; r) = s · g + r · h

  Σ-protocol for "Com opens to s ∈ {0, 1}" (the predicate-value commitment):
      (a) commit:   Prover picks fresh r' ∈ Z_q; sends A = r' · h.
      (b) challenge: Verifier (or Fiat–Shamir) chooses c ∈ Z_q.
      (c) response: Prover sends z = r' + c · r.
      Verifier checks: z · h == A + c · (Com − s · g).

  For predicate values we extend to a 4-state {true, false, unknown, refused}
  by encoding the value as a fixed scalar in {0, 1, 2, 3} and proving membership
  in that small set via an OR-of-Σ-protocols (one branch per allowed value).

For E45 specifically — "committed distance is below threshold τ" — the real
construction is a Bulletproofs range proof on the committed distance. v0 ships
the API for it; v1 binds in a Rust kernel via PyO3 or the in-process Halo2 path.
"""
from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from typing import Optional, Tuple

# 32-byte placeholders — every real commitment / proof will fit in this width.
PLACEHOLDER_BYTES = 32


@dataclass(frozen=True)
class PedersenCommitment:
    """Com(s; r) — 32 bytes (compressed Ristretto in real impl)."""
    bytes_: bytes

    @property
    def hex(self) -> str:
        return self.bytes_.hex()

    @staticmethod
    def placeholder() -> "PedersenCommitment":
        return PedersenCommitment(bytes_=b"\x00" * PLACEHOLDER_BYTES)


@dataclass(frozen=True)
class SigmaProof:
    """A 3-move Σ-protocol proof, Fiat-Shamir compressed to a single blob.

    Real shape (Ristretto, no compression tricks):
        a:    32 bytes (A = r' · h)
        e:    32 bytes (Fiat-Shamir challenge)
        z:    32 bytes (response scalar)
    Total:    96 bytes.
    """
    bytes_: bytes

    @property
    def hex(self) -> str:
        return self.bytes_.hex()

    @staticmethod
    def placeholder() -> "SigmaProof":
        return SigmaProof(bytes_=b"\x00" * (3 * PLACEHOLDER_BYTES))


@dataclass(frozen=True)
class RangeProof:
    """Bulletproof-style range proof that a committed distance is in [0, τ).

    Real shape (Bulletproofs n=64-bit range, single proof):
        ~672 bytes; constant-size regardless of τ.
    Placeholder shape: 64 bytes (smaller than real, but verifier rejects on size).
    """
    bytes_: bytes

    @property
    def hex(self) -> str:
        return self.bytes_.hex()

    @staticmethod
    def placeholder() -> "RangeProof":
        return RangeProof(bytes_=b"\x00" * (2 * PLACEHOLDER_BYTES))


def _value_to_scalar(value: str) -> int:
    """Map PredicateValue.value to the encoded scalar used in commitments."""
    return {
        "false": 0,
        "true": 1,
        "unknown": 2,
        "refused": 3,
    }.get(value, 0)


def commit_predicate_value(value: str, randomness: Optional[bytes] = None) -> Tuple[
    PedersenCommitment, bytes
]:
    """Commit to a 2-bit predicate value.

    Returns (commitment, randomness) so the prover can later use `randomness`
    to construct an opening (Σ-protocol response).

    v0 PLACEHOLDER: derives a deterministic byte string from the value + randomness
    so disclosure.py has a well-defined hex to ship. Will be replaced with the
    real Ristretto commitment when the curve kernel is wired in.
    """
    if randomness is None:
        randomness = secrets.token_bytes(PLACEHOLDER_BYTES)
    s = _value_to_scalar(value)
    digest = hashlib.sha256(
        b"calm-witness-pedersen-v0-PLACEHOLDER|"
        + s.to_bytes(1, "big")
        + b"|"
        + randomness
    ).digest()
    return PedersenCommitment(bytes_=digest), randomness


def prove_membership_in_set(
    value: str, randomness: bytes, allowed_values: Tuple[str, ...] = (
        "true", "false", "unknown", "refused",
    )
) -> SigmaProof:
    """Prove that the committed scalar is one of `allowed_values`.

    Real impl: OR-of-Σ-protocols (Cramer–Damgård–Schoenmakers, EUROCRYPT 1994).

    v0 PLACEHOLDER: returns a deterministic 96-byte hash binding the inputs
    so the verifier can at least confirm self-consistency.
    """
    s = _value_to_scalar(value)
    blob = hashlib.sha256(
        b"calm-witness-sigma-v0-PLACEHOLDER|"
        + s.to_bytes(1, "big")
        + b"|"
        + randomness
        + b"|"
        + ",".join(allowed_values).encode("utf-8")
    ).digest()
    return SigmaProof(bytes_=blob + blob + blob)


def verify_membership_proof(
    commitment: PedersenCommitment, proof: SigmaProof,
    allowed_values: Tuple[str, ...] = ("true", "false", "unknown", "refused"),
) -> bool:
    """Verify the Σ-protocol proof against the commitment.

    v0 PLACEHOLDER: shape-only verification (returns True iff bytes are the
    right widths). v1 replaces with real Σ-verification using the same group
    operations as commit_predicate_value.
    """
    if len(commitment.bytes_) != PLACEHOLDER_BYTES:
        return False
    if len(proof.bytes_) != 3 * PLACEHOLDER_BYTES:
        return False
    return True


def prove_distance_below_threshold(
    distance: int, threshold: int, randomness: Optional[bytes] = None
) -> Tuple[PedersenCommitment, RangeProof]:
    """Everest 45 — prove a committed biometric distance is below τ in ZK.

    Real impl: Bulletproofs range proof over Ristretto. Constant-size proof
    (≈672 bytes) regardless of τ.

    v0 PLACEHOLDER: shape-only.
    """
    if randomness is None:
        randomness = secrets.token_bytes(PLACEHOLDER_BYTES)
    commitment, _ = commit_predicate_value(
        "true" if distance < threshold else "false", randomness=randomness
    )
    blob = hashlib.sha256(
        b"calm-witness-bulletproof-v0-PLACEHOLDER|"
        + distance.to_bytes(8, "big")
        + b"|"
        + threshold.to_bytes(8, "big")
        + b"|"
        + randomness
    ).digest()
    return commitment, RangeProof(bytes_=blob + blob)


def verify_distance_below_threshold(
    commitment: PedersenCommitment, range_proof: RangeProof, threshold: int
) -> bool:
    """Verify a Bulletproof range proof against the commitment + public threshold.

    v0 PLACEHOLDER: shape-only.
    """
    if len(commitment.bytes_) != PLACEHOLDER_BYTES:
        return False
    if len(range_proof.bytes_) != 2 * PLACEHOLDER_BYTES:
        return False
    if threshold < 0:
        return False
    return True


__all__ = [
    "PedersenCommitment",
    "SigmaProof",
    "RangeProof",
    "commit_predicate_value",
    "prove_membership_in_set",
    "verify_membership_proof",
    "prove_distance_below_threshold",
    "verify_distance_below_threshold",
]
