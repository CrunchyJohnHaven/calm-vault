"""calm_witness.disclosure — request, response, and replay-defence (Everests 66, 67, 70, 72).

Wire format (v0 plaintext): JSON. ZK proof and Pedersen commitment fields are
placeholders that ship as opaque hex strings in v0; their generation lands with
Everests 44/45 (Pedersen commit + Σ-protocol range proof).

Replay defence: every request carries a counterparty-chosen nonce; the response
binds the nonce into a signature payload alongside the chain head, predicate ID,
and freshness window. A verifier rejects any response whose `nonce` does not
match its own outstanding request.

Disclosure logging: every successful disclosure appends a `kind: "disclosure"`
record to `user_state.jsonl`. Implemented here so the operator cannot disclose
without leaving an audit trail; future hardening (E72b) makes the append
atomic with the wire send.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from predicates import EvaluationResult, evaluate
except ImportError:  # pragma: no cover
    from calm_witness.predicates import EvaluationResult, evaluate

try:
    from verify_chain import canonical_record_hash
except ImportError:  # pragma: no cover
    from calm_witness.verify_chain import canonical_record_hash


WIRE_VERSION = 0


@dataclass
class DisclosureRequest:
    """Everest 66 — counterparty's signed request for a predicate disclosure."""
    predicate_id: str
    counterparty_id_hash: str          # sha256 of counterparty CredexAI VC
    counterparty_class: str            # e.g. "financial", "peer-AI-collective"
    nonce: str                         # 32-byte hex; replay defence anchor
    freshness_max_seconds: int = 86400 # default 24h; counterparty's tolerance
    requested_at: float = field(default_factory=time.time)
    wire_version: int = WIRE_VERSION

    @staticmethod
    def new(
        predicate_id: str,
        counterparty_id_hash: str,
        counterparty_class: str,
        freshness_max_seconds: int = 86400,
    ) -> "DisclosureRequest":
        return DisclosureRequest(
            predicate_id=predicate_id,
            counterparty_id_hash=counterparty_id_hash,
            counterparty_class=counterparty_class,
            nonce=secrets.token_hex(32),
            freshness_max_seconds=freshness_max_seconds,
        )

    def to_canonical_bytes(self) -> bytes:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":")).encode("utf-8")

    def digest(self) -> str:
        return hashlib.sha256(self.to_canonical_bytes()).hexdigest()


@dataclass
class DisclosureResponse:
    """Everest 67 — operator's bound disclosure carrying the proof envelope."""
    predicate_id: str
    value: str                         # "true" | "false" | "unknown" | "refused"
    freshness_window_seconds: Optional[int]
    nonce: str                         # echoes the request's nonce
    chain_head: str                    # latest record_hash in the operator's vault
    pedersen_commitment_hex: str       # v0: placeholder ("00..." until E44)
    sigma_proof_hex: str               # v0: placeholder ("00..." until E45)
    operator_id_hash: str              # sha256 of operator CredexAI VC
    operator_sig_hex: str              # Ed25519 over the canonical response bytes (E2)
    wire_version: int = WIRE_VERSION

    def to_canonical_bytes(self) -> bytes:
        # Sign over everything except the signature itself.
        d = asdict(self)
        d.pop("operator_sig_hex", None)
        return json.dumps(d, sort_keys=True, separators=(",", ":")).encode("utf-8")


def respond(
    request: DisclosureRequest,
    chain_window: List[Dict[str, Any]],
    chain_head: str,
    operator_id_hash: str,
    operator_sign: Optional[Any] = None,  # callable(bytes) -> sig_hex, optional in v0
) -> DisclosureResponse:
    """Evaluate the requested predicate and produce a signed, nonce-bound response.

    operator_sign is a callable that takes the canonical response bytes and returns
    a hex Ed25519 signature. In v0 tests we pass None; the field is the empty string.
    """
    result: EvaluationResult = evaluate(
        request.predicate_id,
        chain_window=chain_window,
        counterparty_class=request.counterparty_class,
    )
    resp = DisclosureResponse(
        predicate_id=request.predicate_id,
        value=result.value.value,
        freshness_window_seconds=result.freshness_window_seconds,
        nonce=request.nonce,           # E70: bind to request
        chain_head=chain_head,
        pedersen_commitment_hex="00" * 32,  # placeholder until E44
        sigma_proof_hex="00" * 32,          # placeholder until E45
        operator_id_hash=operator_id_hash,
        operator_sig_hex="",
    )
    if operator_sign is not None:
        resp.operator_sig_hex = operator_sign(resp.to_canonical_bytes())
    return resp


def verify_response_binding(
    request: DisclosureRequest, response: DisclosureResponse
) -> List[str]:
    """E70 — confirm that a response is bound to the request and not a replay."""
    errors: List[str] = []
    if response.predicate_id != request.predicate_id:
        errors.append("predicate_id mismatch")
    if response.nonce != request.nonce:
        errors.append("nonce mismatch — replay or wrong session")
    if response.wire_version != request.wire_version:
        errors.append("wire_version mismatch")
    if response.freshness_window_seconds is not None and (
        response.freshness_window_seconds > request.freshness_max_seconds
    ):
        errors.append(
            f"freshness {response.freshness_window_seconds}s > tolerance "
            f"{request.freshness_max_seconds}s"
        )
    return errors


# --- E72 disclosure logging -------------------------------------------------

def build_disclosure_record(
    request: DisclosureRequest,
    response: DisclosureResponse,
    seq: int,
    prev_hash: str,
    principal: str = "John Bradley",
    operator: str = "CALM",
    ts_iso: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a `kind: disclosure` record ready for chain append.

    Logs the predicate ID, counterparty class, request digest, response digest,
    and operator identity. Does NOT log the full request/response payloads — the
    audit trail records *that* a disclosure happened, not its content.
    """
    if ts_iso is None:
        ts_iso = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
        # Insert colon in tz offset (+HHMM -> +HH:MM)
        if len(ts_iso) >= 5 and ts_iso[-5] in "+-":
            ts_iso = ts_iso[:-2] + ":" + ts_iso[-2:]

    record = {
        "kind": "disclosure",
        "operator": operator,
        "payload": {
            "predicate_id": request.predicate_id,
            "counterparty_class": request.counterparty_class,
            "counterparty_id_hash": request.counterparty_id_hash,
            "request_digest": request.digest(),
            "response_value": response.value,
            "response_nonce": response.nonce,
            "chain_head_at_response": response.chain_head,
        },
        "prev_hash": prev_hash,
        "principal": principal,
        "schema_version": 0,
        "seq": seq,
        "ts": ts_iso,
        "ts_source": "operator_local_clock",
    }
    record["record_hash"] = canonical_record_hash(record)
    return record


def append_disclosure_record(
    chain_path: Path, request: DisclosureRequest, response: DisclosureResponse
) -> Dict[str, Any]:
    """Append a disclosure record to user_state.jsonl. Returns the new record."""
    chain_path = Path(chain_path).expanduser()
    # Load the existing chain to find next seq and prev_hash. Stdlib only.
    last_seq = 0
    prev_hash = "0" * 64
    if chain_path.exists():
        with chain_path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                last_seq = rec.get("seq", last_seq)
                prev_hash = rec.get("record_hash", prev_hash)
    record = build_disclosure_record(
        request=request,
        response=response,
        seq=last_seq + 1,
        prev_hash=prev_hash,
    )
    with chain_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True, separators=(",", ":")))
        fh.write("\n")
    return record


__all__ = [
    "WIRE_VERSION",
    "DisclosureRequest",
    "DisclosureResponse",
    "respond",
    "verify_response_binding",
    "build_disclosure_record",
    "append_disclosure_record",
]
