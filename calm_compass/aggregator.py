"""calm_compass.aggregator — sum-over-private-history + threshold predicate (CC-29, CC-30, CC-31, CC-32).

The Compass cryptographic spine. For a given predicate, classifier, and chain
window, produce:

  • per-record Pedersen commitments (placeholder bytes in v0)
  • the homomorphically-aggregated commitment
  • a Bulletproof-style threshold proof that the aggregate ≥ T  (placeholder)
  • a chain-window binding to (chain_head, window_start, window_end)
  • a classifier-hash binding

The placeholder bytes match the wire shape the real Bulletproofs kernel will
produce; the swap point is shared with Calm Witness E45.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "calm_witness"))

from classifiers import CLASSIFIERS, classifier_hash, score_chain         # noqa: E402

PROTOCOL_VERSION = "calm-compass/v0"
PLACEHOLDER_BYTES = 32
RANGE_PROOF_PLACEHOLDER_BYTES = 64


@dataclass
class CompassProof:
    """The wire-format Compass attestation envelope."""
    protocol_version: str
    predicate_id: str
    classifier_hash_hex: str
    window_start_iso: str
    window_end_iso: str
    chain_head: str
    threshold: int
    aggregate_commitment_hex: str
    range_proof_hex: str
    operator_id_hash: str
    nonce: str
    value: str                                  # "true" | "false" | "unknown" | "refused"
    n_records_considered: int

    def to_canonical_bytes(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True,
                          separators=(",", ":")).encode("utf-8")

    def digest(self) -> str:
        return hashlib.sha256(self.to_canonical_bytes()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _placeholder_pedersen_commit(score: int, randomness: bytes) -> bytes:
    """v0 placeholder. Real impl: ``score · g + randomness · h`` on Ristretto255."""
    return hashlib.sha256(
        b"calm-compass-pedersen-v0|"
        + score.to_bytes(2, "big", signed=True)
        + b"|"
        + randomness
    ).digest()


def _placeholder_aggregate(commitments: List[bytes]) -> bytes:
    """v0 placeholder. Real impl: pointwise addition on Ristretto255."""
    h = hashlib.sha256()
    h.update(b"calm-compass-aggregate-v0|")
    for c in commitments:
        h.update(c)
    return h.digest()


def _placeholder_range_proof(
    aggregate: bytes, threshold: int, total_score: int, randomness_sum: bytes
) -> bytes:
    """v0 placeholder. Real impl: Bulletproof range proof aggregate ≥ threshold."""
    blob = hashlib.sha256(
        b"calm-compass-rangeproof-v0|"
        + aggregate
        + b"|"
        + threshold.to_bytes(8, "big", signed=True)
        + b"|"
        + total_score.to_bytes(8, "big", signed=True)
        + b"|"
        + randomness_sum
    ).digest()
    # 64-byte placeholder (matches real Bulletproof witness width).
    return blob + blob


def _filter_window(
    chain: List[Dict[str, Any]],
    window_start: datetime,
    window_end: datetime,
) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for rec in chain:
        ts_str = rec.get("ts", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if window_start <= ts <= window_end:
            out.append(rec)
    return out


def build_compass_proof(
    chain: List[Dict[str, Any]],
    predicate_id: str,
    threshold: int,
    window_start: datetime,
    window_end: datetime,
    operator_id_hash: str,
    nonce: Optional[str] = None,
    tribe_map: Optional[Dict[str, Any]] = None,
) -> CompassProof:
    """Build a Compass proof for the named predicate over the chain window."""
    if predicate_id not in CLASSIFIERS:
        raise ValueError(f"unknown predicate: {predicate_id}")
    if nonce is None:
        nonce = secrets.token_hex(32)

    window = _filter_window(chain, window_start, window_end)
    scores = score_chain(window, predicate_id, tribe_map=tribe_map)
    chain_head = chain[-1].get("record_hash", "0" * 64) if chain else "0" * 64

    randomness_per = [secrets.token_bytes(PLACEHOLDER_BYTES) for _ in scores]
    commitments = [_placeholder_pedersen_commit(s, r)
                   for s, r in zip(scores, randomness_per)]
    aggregate = _placeholder_aggregate(commitments)
    total = sum(scores)
    randomness_sum = hashlib.sha256(b"".join(randomness_per)).digest()
    range_proof = _placeholder_range_proof(aggregate, threshold, total, randomness_sum)

    if total >= threshold:
        value = "true"
    else:
        value = "false"

    return CompassProof(
        protocol_version=PROTOCOL_VERSION,
        predicate_id=predicate_id,
        classifier_hash_hex=classifier_hash(predicate_id),
        window_start_iso=window_start.isoformat().replace("+00:00", "Z"),
        window_end_iso=window_end.isoformat().replace("+00:00", "Z"),
        chain_head=chain_head,
        threshold=threshold,
        aggregate_commitment_hex=aggregate.hex(),
        range_proof_hex=range_proof.hex(),
        operator_id_hash=operator_id_hash,
        nonce=nonce,
        value=value,
        n_records_considered=len(window),
    )


def verify_compass_proof(
    proof: CompassProof,
    expected_threshold: int,
    expected_predicate_id: str,
    expected_chain_head: Optional[str] = None,
) -> List[str]:
    """v0 placeholder verification. Real impl: re-verify Bulletproof.

    Returns a list of error strings; empty list means structurally valid.
    Real cryptographic verification swaps in at E45 with the Rust kernel.
    """
    errors: List[str] = []
    if proof.protocol_version != PROTOCOL_VERSION:
        errors.append(f"protocol_version mismatch: {proof.protocol_version}")
    if proof.predicate_id != expected_predicate_id:
        errors.append("predicate_id mismatch")
    if proof.threshold != expected_threshold:
        errors.append(f"threshold mismatch (proof={proof.threshold}, expected={expected_threshold})")
    if expected_chain_head and proof.chain_head != expected_chain_head:
        errors.append("chain_head mismatch")
    if proof.classifier_hash_hex != classifier_hash(proof.predicate_id):
        errors.append("classifier_hash drift — operator used a different evaluator")
    if len(bytes.fromhex(proof.aggregate_commitment_hex)) != PLACEHOLDER_BYTES:
        errors.append("aggregate_commitment_hex width wrong")
    if len(bytes.fromhex(proof.range_proof_hex)) != RANGE_PROOF_PLACEHOLDER_BYTES:
        errors.append("range_proof_hex width wrong")
    if proof.value not in {"true", "false", "unknown", "refused"}:
        errors.append(f"value not in canonical set: {proof.value}")
    return errors


__all__ = [
    "PROTOCOL_VERSION",
    "CompassProof",
    "build_compass_proof",
    "verify_compass_proof",
]
