"""calm_stack.session — the unified four-pillar handshake.

A ``CalmSession`` represents one end-to-end interaction between two agents:
the **operator** (e.g., Calm acting for John) and the **counterparty** (e.g., a
peer-AI-collective's operator). The session runs in up to four sequential phases:

    Phase 1: Pact     — categorical directive equality
    Phase 2: Witness  — user-state attestation (the state bit)
    Phase 3: Compass  — principal-authored values attestation (the values bit)
    Phase 4: Tenancy  — every reply and disclosure is logged + gated

Compass is optional per session: not every counterparty class is authorized for
values disclosure. The session transcript records which pillars actually ran.

A session that completes all enabled phases produces a structured
``SessionTranscript`` any third party can later audit: who spoke to whom, under
what directive class, with what user-state predicate, with what values predicate,
with what tenancy SLA — and never anything more.

The transcript is the artifact that demonstrates the four pillars composed.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Cross-package imports — composition without re-implementation.
_HERE = Path(__file__).resolve().parent
_PARENT = _HERE.parent
sys.path.insert(0, str(_PARENT / "calm_witness"))
sys.path.insert(0, str(_PARENT / "calm_tenancy"))
sys.path.insert(0, str(_PARENT / "calm_compass"))

from disclosure import DisclosureRequest, respond, verify_response_binding  # noqa: E402
from predicates import (                                                      # noqa: E402
    P_IN_BASELINE_24H_ID,
    PredicateValue,
)
from verify_chain import load_jsonl, verify_chain                              # noqa: E402

from cringe_gate import cringe_check                                          # noqa: E402
from classify import classify_and_route                                       # noqa: E402

from aggregator import (                                                      # noqa: E402
    CompassProof,
    build_compass_proof,
    verify_compass_proof,
)


PROTOCOL_VERSION = "calm-stack/v0"


@dataclass
class PactPhase:
    """Calm Pact directive-equality proof (placeholder bytes in v0)."""
    operator_directive_commitment: str
    counterparty_directive_commitment: str
    equality_proof: str
    verified: bool
    note: str = ""


@dataclass
class CompassPhase:
    """Calm Compass values attestation."""
    predicate_id: str
    threshold: int
    value: str
    n_records_considered: int
    classifier_hash_hex: str
    aggregate_commitment_hex: str
    range_proof_hex: str
    chain_head: str
    nonce: str
    binding_errors: List[str]
    verified: bool


@dataclass
class WitnessPhase:
    """Calm Witness predicate disclosure."""
    predicate_id: str
    value: str
    freshness_window_seconds: Optional[int]
    chain_head: str
    nonce: str
    binding_errors: List[str]
    verified: bool


@dataclass
class TenancyPhase:
    """Calm Tenancy bounded-surface confirmation."""
    operator_domain: str
    mailbox: str
    sla_first_ack_seconds: int
    rubric_version: str
    inbound_classification: Optional[str]
    inbound_response_seeking: Optional[bool]
    page_passed_cringe: Optional[bool]
    page_density: Optional[float]


@dataclass
class SessionTranscript:
    session_id: str
    protocol_version: str
    started_at: str
    completed_at: Optional[str]
    operator_did: str
    counterparty_did: str
    pact: Optional[PactPhase] = None
    witness: Optional[WitnessPhase] = None
    compass: Optional[CompassPhase] = None
    tenancy: Optional[TenancyPhase] = None
    outcome: str = "incomplete"               # complete | refused | failed | incomplete
    failure_reason: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), indent=2)

    def digest(self) -> str:
        canonical = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# --- Phase 1: Pact (placeholder until real Pact module is wired in) ---------

def _placeholder_pact(
    operator_directive: str,
    counterparty_directive: str,
) -> PactPhase:
    """v0 placeholder for the Calm Pact directive-equality proof.

    Real Calm Pact ships at ``calm_pact/protocol.py``. v0 here uses a stand-in
    that returns ``verified=True`` iff the two directives are byte-equal. When
    the real Σ-protocol is wired, this function becomes a thin call to it.
    """
    com_a = hashlib.sha256(f"pact/v0/a|{operator_directive}".encode("utf-8")).hexdigest()
    com_b = hashlib.sha256(f"pact/v0/b|{counterparty_directive}".encode("utf-8")).hexdigest()
    proof = hashlib.sha256(f"pact/v0/proof|{com_a}|{com_b}".encode("utf-8")).hexdigest()
    return PactPhase(
        operator_directive_commitment=com_a,
        counterparty_directive_commitment=com_b,
        equality_proof=proof,
        verified=(operator_directive == counterparty_directive),
        note="v0 placeholder; real Σ-protocol lives in calm_pact/protocol.py",
    )


# --- Phase 2: Witness (real, runs against the live chain) -------------------

def _run_witness(
    chain_path: Path,
    operator_id_hash: str,
    counterparty_id_hash: str,
    counterparty_class: str,
    predicate_id: str,
) -> WitnessPhase:
    """Real Calm Witness disclosure path against the chain at ``chain_path``."""
    records = load_jsonl(chain_path) if chain_path.exists() else []
    request = DisclosureRequest.new(
        predicate_id=predicate_id,
        counterparty_id_hash=counterparty_id_hash,
        counterparty_class=counterparty_class,
    )
    chain_head = records[-1].get("record_hash", "0" * 64) if records else "0" * 64
    response = respond(
        request,
        chain_window=records,
        chain_head=chain_head,
        operator_id_hash=operator_id_hash,
    )
    binding_errors = verify_response_binding(request, response)
    return WitnessPhase(
        predicate_id=response.predicate_id,
        value=response.value,
        freshness_window_seconds=response.freshness_window_seconds,
        chain_head=response.chain_head,
        nonce=response.nonce,
        binding_errors=binding_errors,
        verified=not binding_errors,
    )


# --- Phase 3: Tenancy (per-message surface gate) ----------------------------

def _run_tenancy(
    operator_domain: str,
    sla_first_ack_seconds: int = 600,
    inbound_text: Optional[str] = None,
    page_text: Optional[str] = None,
    forbidden_phrases: Optional[List[str]] = None,
) -> TenancyPhase:
    """Run the Calm Tenancy surface checks for this session."""
    classification = None
    response_seeking = None
    if inbound_text is not None:
        c, rs, _ = classify_and_route(inbound_text)
        classification = c
        response_seeking = rs

    page_passed = None
    page_density = None
    if page_text is not None:
        rpt = cringe_check(page_text, forbidden_phrases=forbidden_phrases or [])
        page_passed = (rpt.verdict == "SHIP")
        page_density = rpt.density

    return TenancyPhase(
        operator_domain=operator_domain,
        mailbox=f"calm@{operator_domain}",
        sla_first_ack_seconds=sla_first_ack_seconds,
        rubric_version="cringe-rubric/v1",
        inbound_classification=classification,
        inbound_response_seeking=response_seeking,
        page_passed_cringe=page_passed,
        page_density=page_density,
    )


# --- The unified handshake --------------------------------------------------

def run_calm_session(
    operator_directive: str,
    counterparty_directive: str,
    operator_did: str,
    counterparty_did: str,
    operator_domain: str,
    chain_path: Optional[Path] = None,
    operator_id_hash: str = "",
    counterparty_id_hash: str = "",
    counterparty_class: str = "peer-AI-collective",
    predicate_id: str = P_IN_BASELINE_24H_ID,
    inbound_text: Optional[str] = None,
    page_text: Optional[str] = None,
    forbidden_phrases: Optional[List[str]] = None,
    compass_predicate_id: Optional[str] = None,
    compass_threshold: int = 1,
    compass_window_days: int = 180,
    tribe_map: Optional[Dict[str, Any]] = None,
) -> SessionTranscript:
    """Run the three-phase Calm Session and produce a transcript."""
    transcript = SessionTranscript(
        session_id=str(uuid.uuid4()),
        protocol_version=PROTOCOL_VERSION,
        started_at=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        completed_at=None,
        operator_did=operator_did,
        counterparty_did=counterparty_did,
    )

    # Phase 1 — Pact
    transcript.pact = _placeholder_pact(operator_directive, counterparty_directive)
    if not transcript.pact.verified:
        transcript.outcome = "failed"
        transcript.failure_reason = "Pact directive-equality failed; walk away."
        transcript.completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return transcript

    # Phase 2 — Witness
    chain_path = Path(chain_path or Path.home() / ".calm-vault" / "user_state.jsonl")
    if not operator_id_hash:
        operator_id_hash = hashlib.sha256(operator_did.encode("utf-8")).hexdigest()
    if not counterparty_id_hash:
        counterparty_id_hash = hashlib.sha256(counterparty_did.encode("utf-8")).hexdigest()
    transcript.witness = _run_witness(
        chain_path=chain_path,
        operator_id_hash=operator_id_hash,
        counterparty_id_hash=counterparty_id_hash,
        counterparty_class=counterparty_class,
        predicate_id=predicate_id,
    )
    if not transcript.witness.verified:
        transcript.outcome = "failed"
        transcript.failure_reason = (
            "Witness binding failed: " + ", ".join(transcript.witness.binding_errors)
        )
        transcript.completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        return transcript

    if transcript.witness.value == "refused":
        transcript.outcome = "refused"
        transcript.failure_reason = "Principal refused this disclosure class for this predicate."
        # Tenancy phase still runs — the refusal is a *valid* protocol output.

    # Phase 3 — Compass (optional)
    if compass_predicate_id:
        from datetime import timedelta
        records = load_jsonl(chain_path) if chain_path.exists() else []
        now = datetime.now(timezone.utc)
        try:
            cproof = build_compass_proof(
                chain=records,
                predicate_id=compass_predicate_id,
                threshold=compass_threshold,
                window_start=now - timedelta(days=compass_window_days),
                window_end=now + timedelta(hours=1),
                operator_id_hash=operator_id_hash,
                tribe_map=tribe_map,
            )
            cerrors = verify_compass_proof(
                proof=cproof,
                expected_threshold=compass_threshold,
                expected_predicate_id=compass_predicate_id,
            )
            transcript.compass = CompassPhase(
                predicate_id=cproof.predicate_id,
                threshold=cproof.threshold,
                value=cproof.value,
                n_records_considered=cproof.n_records_considered,
                classifier_hash_hex=cproof.classifier_hash_hex,
                aggregate_commitment_hex=cproof.aggregate_commitment_hex,
                range_proof_hex=cproof.range_proof_hex,
                chain_head=cproof.chain_head,
                nonce=cproof.nonce,
                binding_errors=cerrors,
                verified=not cerrors,
            )
        except Exception as exc:                                # noqa: BLE001
            transcript.outcome = "failed"
            transcript.failure_reason = f"Compass phase error: {exc}"
            transcript.completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            return transcript

    # Phase 4 — Tenancy
    transcript.tenancy = _run_tenancy(
        operator_domain=operator_domain,
        inbound_text=inbound_text,
        page_text=page_text,
        forbidden_phrases=forbidden_phrases,
    )

    if transcript.outcome == "incomplete":
        transcript.outcome = "complete"
    transcript.completed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return transcript


__all__ = [
    "PROTOCOL_VERSION",
    "PactPhase",
    "WitnessPhase",
    "TenancyPhase",
    "SessionTranscript",
    "run_calm_session",
]
