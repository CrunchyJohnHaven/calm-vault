"""calm_compass.disclosure — Compass disclosure request + response (CC-39, CC-40, CC-41).

Analog of ``calm_witness/disclosure.py``. Wire shape mirrors Witness so a
counterparty already integrated with Witness can add Compass with minimal code.
Adds CC-41: per-counterparty rate limit (same counterparty cannot ask the same
Compass predicate more frequently than the principal's set rate).
"""
from __future__ import annotations

import hashlib
import json
import secrets
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregator import CompassProof, build_compass_proof, verify_compass_proof   # noqa: E402

WIRE_VERSION = 0


@dataclass
class CompassDisclosureRequest:
    """CC-39 — counterparty's signed request for a Compass disclosure."""
    predicate_id: str
    threshold: int
    window_days: int
    counterparty_id_hash: str
    counterparty_class: str
    nonce: str
    requested_at: float = field(default_factory=time.time)
    wire_version: int = WIRE_VERSION

    @staticmethod
    def new(predicate_id: str, threshold: int, counterparty_id_hash: str,
            counterparty_class: str, window_days: int = 180) -> "CompassDisclosureRequest":
        return CompassDisclosureRequest(
            predicate_id=predicate_id,
            threshold=threshold,
            window_days=window_days,
            counterparty_id_hash=counterparty_id_hash,
            counterparty_class=counterparty_class,
            nonce=secrets.token_hex(32),
        )

    def to_canonical_bytes(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True,
                          separators=(",", ":")).encode("utf-8")

    def digest(self) -> str:
        return hashlib.sha256(self.to_canonical_bytes()).hexdigest()


@dataclass
class CompassDisclosureResponse:
    """CC-40 — operator's bound Compass response carrying the proof envelope."""
    predicate_id: str
    threshold: int
    value: str
    n_records_considered: int
    classifier_hash_hex: str
    aggregate_commitment_hex: str
    range_proof_hex: str
    chain_head: str
    nonce: str                                # echoes the request's nonce
    operator_id_hash: str
    operator_sig_hex: str = ""
    wire_version: int = WIRE_VERSION

    @staticmethod
    def from_proof(proof: CompassProof, threshold: int,
                   operator_sign=None) -> "CompassDisclosureResponse":
        resp = CompassDisclosureResponse(
            predicate_id=proof.predicate_id,
            threshold=threshold,
            value=proof.value,
            n_records_considered=proof.n_records_considered,
            classifier_hash_hex=proof.classifier_hash_hex,
            aggregate_commitment_hex=proof.aggregate_commitment_hex,
            range_proof_hex=proof.range_proof_hex,
            chain_head=proof.chain_head,
            nonce=proof.nonce,
            operator_id_hash=proof.operator_id_hash,
        )
        if operator_sign is not None:
            resp.operator_sig_hex = operator_sign(resp.to_canonical_bytes())
        return resp

    def to_canonical_bytes(self) -> bytes:
        d = asdict(self)
        d.pop("operator_sig_hex", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


def respond_compass(
    request: CompassDisclosureRequest,
    chain: List[Dict[str, Any]],
    operator_id_hash: str,
    tribe_map: Optional[Dict[str, Any]] = None,
    now: Optional[datetime] = None,
    operator_sign=None,
) -> CompassDisclosureResponse:
    """Build a Compass proof against the request's terms and wrap as a response.

    The response nonce echoes the request nonce — replay defence is identical
    to Witness E70.
    """
    now = now or datetime.now(timezone.utc)
    proof = build_compass_proof(
        chain=chain,
        predicate_id=request.predicate_id,
        threshold=request.threshold,
        window_start=now - timedelta(days=request.window_days),
        window_end=now + timedelta(hours=1),
        operator_id_hash=operator_id_hash,
        nonce=request.nonce,
        tribe_map=tribe_map,
    )
    return CompassDisclosureResponse.from_proof(
        proof, threshold=request.threshold, operator_sign=operator_sign
    )


def verify_compass_response_binding(
    request: CompassDisclosureRequest,
    response: CompassDisclosureResponse,
) -> List[str]:
    """Counterparty-side binding check for a Compass response."""
    errors: List[str] = []
    if response.predicate_id != request.predicate_id:
        errors.append("predicate_id mismatch")
    if response.nonce != request.nonce:
        errors.append("nonce mismatch — replay or wrong session")
    if response.wire_version != request.wire_version:
        errors.append("wire_version mismatch")
    if response.threshold != request.threshold:
        errors.append("threshold mismatch")
    return errors


# ─── CC-41 — Per-counterparty rate limit ────────────────────────────────────

DEFAULT_RATE_LIMIT_DAYS = 90


@dataclass
class RateLimitState:
    """Persistent state for CC-41. One row per (counterparty_id_hash, predicate_id)."""
    counterparty_id_hash: str
    predicate_id: str
    last_request_iso: str
    request_count: int


def _rate_limit_store_path() -> Path:
    p = Path.home() / ".calm-vault" / "tenancy" / "compass_rate_limits.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def check_rate_limit(
    counterparty_id_hash: str,
    predicate_id: str,
    rate_limit_days: int = DEFAULT_RATE_LIMIT_DAYS,
    now: Optional[datetime] = None,
    store_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """CC-41 — Refuse repeated requests from the same counterparty inside the window."""
    store_path = store_path or _rate_limit_store_path()
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=rate_limit_days)

    matching: Optional[RateLimitState] = None
    if store_path.exists():
        with store_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                if (row["counterparty_id_hash"] == counterparty_id_hash
                        and row["predicate_id"] == predicate_id):
                    matching = RateLimitState(**row)

    if matching:
        last = datetime.fromisoformat(matching.last_request_iso.replace("Z", "+00:00"))
        if last >= cutoff:
            seconds_until_ok = int((last + timedelta(days=rate_limit_days) - now).total_seconds())
            return {
                "allowed": False,
                "reason": "rate-limited",
                "seconds_until_ok": seconds_until_ok,
                "last_request_iso": matching.last_request_iso,
            }
    return {"allowed": True, "reason": "ok"}


def record_request(
    counterparty_id_hash: str,
    predicate_id: str,
    now: Optional[datetime] = None,
    store_path: Optional[Path] = None,
) -> None:
    """Append a rate-limit row after issuing a (granted) disclosure."""
    store_path = store_path or _rate_limit_store_path()
    now = now or datetime.now(timezone.utc)
    row = {
        "counterparty_id_hash": counterparty_id_hash,
        "predicate_id": predicate_id,
        "last_request_iso": now.isoformat().replace("+00:00", "Z"),
        "request_count": 1,
    }
    with store_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True, separators=(",", ":")))
        fh.write("\n")


__all__ = [
    "WIRE_VERSION",
    "CompassDisclosureRequest",
    "CompassDisclosureResponse",
    "respond_compass",
    "verify_compass_response_binding",
    "check_rate_limit",
    "record_request",
    "DEFAULT_RATE_LIMIT_DAYS",
]
