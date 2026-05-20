"""calm_witness.predicates — v0 predicate evaluators (Everest 55).

Pure, deterministic functions over (chain_window, consent, counterparty_class).
Each predicate returns a PredicateValue enum literal: TRUE / FALSE / UNKNOWN / REFUSED.

This module ships the v0 canonical predicate `in_baseline_24h` (Everest 55) and
stubs for the other five vocabulary entries. The stubs raise NotImplementedError
deliberately — they bag at their own summits (E56, E57, E58, E59, E60).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional

PREDICATE_NAMESPACE = "calm-witness/predicate/v0/"


class PredicateValue(str, Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"
    REFUSED = "refused"


@dataclass(frozen=True)
class EvaluationResult:
    predicate_id: str
    value: PredicateValue
    freshness_window_seconds: Optional[int]
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "predicate_id": self.predicate_id,
            "value": self.value.value,
            "freshness_window_seconds": self.freshness_window_seconds,
            "reason": self.reason,
        }


# --- helpers ----------------------------------------------------------------

def _parse_iso(ts: str) -> datetime:
    # Python 3.11+ fromisoformat handles the offset; 3.9-3.10 needs a small shim.
    s = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(s)


def _filter_window(
    chain: Iterable[Dict[str, Any]], now: datetime, window_seconds: int
) -> List[Dict[str, Any]]:
    cutoff = now - timedelta(seconds=window_seconds)
    out: List[Dict[str, Any]] = []
    for rec in chain:
        try:
            ts = _parse_iso(rec["ts"])
        except (KeyError, ValueError):
            continue
        if ts >= cutoff:
            out.append(rec)
    return out


def _is_self_report(rec: Dict[str, Any]) -> bool:
    return str(rec.get("kind", "")).startswith("self_report.")


# --- P-01 in_baseline_24h ---------------------------------------------------

# The set of affect tokens that count as in-baseline for v0. This is the
# principal's enrolled baseline-affect vocabulary; in v0 it is hard-coded to
# the operator-quoted morning vocabulary. v1 lifts this to a per-principal
# enrolled list (Everest 11 §E template state-labels).
V0_BASELINE_AFFECT_VOCABULARY = frozenset(
    {
        "calm",
        "even-keeled",
        "curious",
        "rested",
        "focused",
        "centered",
        "playful",
        "creative",
        "analytical",
        "affectionate",
    }
)

V0_BASELINE_RESTEDNESS = frozenset({"fully_rested", "rested"})

P_IN_BASELINE_24H_ID = PREDICATE_NAMESPACE + "in_baseline_24h"


def in_baseline_24h(
    chain_window: List[Dict[str, Any]],
    now: Optional[datetime] = None,
    consent_record: Optional[Dict[str, Any]] = None,
    counterparty_class: str = "anonymous",
) -> EvaluationResult:
    """Predicate P-01.

    Returns TRUE iff the most recent self-report within 24h has
      - non-empty intersection between payload.affect and the v0 baseline vocabulary,
      - payload.restedness in {fully_rested, rested},
      - empty payload.known_health_issues.

    Returns UNKNOWN if no self-report in window.
    Returns REFUSED if consent_record explicitly denies disclosure.
    """
    pid = P_IN_BASELINE_24H_ID

    if consent_record is not None and consent_record.get("denied") is True:
        return EvaluationResult(pid, PredicateValue.REFUSED, None, "consent denied")

    if now is None:
        now = datetime.now(timezone.utc)

    window = _filter_window(chain_window, now, 24 * 3600)
    self_reports = [r for r in window if _is_self_report(r)]
    if not self_reports:
        return EvaluationResult(
            pid, PredicateValue.UNKNOWN, None, "no self-report in 24h window"
        )

    latest = max(self_reports, key=lambda r: r["ts"])
    payload = latest.get("payload", {})

    affect = set(payload.get("affect", []) or [])
    if not affect & V0_BASELINE_AFFECT_VOCABULARY:
        return EvaluationResult(
            pid,
            PredicateValue.FALSE,
            int((now - _parse_iso(latest["ts"])).total_seconds()),
            "affect does not intersect baseline vocabulary",
        )

    restedness = payload.get("restedness")
    if restedness not in V0_BASELINE_RESTEDNESS:
        return EvaluationResult(
            pid,
            PredicateValue.FALSE,
            int((now - _parse_iso(latest["ts"])).total_seconds()),
            f"restedness={restedness} not in baseline",
        )

    issues = payload.get("known_health_issues") or []
    if issues:
        return EvaluationResult(
            pid,
            PredicateValue.FALSE,
            int((now - _parse_iso(latest["ts"])).total_seconds()),
            f"known_health_issues non-empty ({len(issues)})",
        )

    freshness = int((now - _parse_iso(latest["ts"])).total_seconds())
    return EvaluationResult(
        pid,
        PredicateValue.TRUE,
        freshness,
        f"self-report within {freshness}s of now in baseline",
    )


# --- Stubs for the other v0 predicates (bag at their own summits) -----------

def biometric_match_within(*args, **kwargs) -> EvaluationResult:
    """Predicate P-02 — bags at Everest 56."""
    raise NotImplementedError("P-02 lands with Everest 56 (biometric distance proof).")


def principal_consents_to_disclose(*args, **kwargs) -> EvaluationResult:
    """Predicate P-03 — bags at Everest 57."""
    raise NotImplementedError("P-03 lands with Everest 57 (consent calculus impl).")


def bank_teller_note_active(*args, **kwargs) -> EvaluationResult:
    """Predicate P-04 — bags at Everest 58."""
    raise NotImplementedError("P-04 lands with Everest 58 (duress codeword evaluator).")


def cognitively_atypical_baseline(*args, **kwargs) -> EvaluationResult:
    """Predicate P-05 — bags at Everest 59."""
    raise NotImplementedError("P-05 lands with Everest 59 (artist-clause attestation).")


def mental_state_unusual(*args, **kwargs) -> EvaluationResult:
    """Predicate P-06 — bags at Everest 60."""
    raise NotImplementedError("P-06 lands with Everest 60 (unusual-state evaluator).")


# --- Registry ---------------------------------------------------------------

REGISTRY = {
    P_IN_BASELINE_24H_ID: in_baseline_24h,
    PREDICATE_NAMESPACE + "biometric_match_within": biometric_match_within,
    PREDICATE_NAMESPACE + "principal_consents_to_disclose": principal_consents_to_disclose,
    PREDICATE_NAMESPACE + "bank_teller_note_active": bank_teller_note_active,
    PREDICATE_NAMESPACE + "cognitively_atypical_baseline": cognitively_atypical_baseline,
    PREDICATE_NAMESPACE + "mental_state_unusual": mental_state_unusual,
}


def evaluate(
    predicate_id: str,
    chain_window: List[Dict[str, Any]],
    now: Optional[datetime] = None,
    consent_record: Optional[Dict[str, Any]] = None,
    counterparty_class: str = "anonymous",
) -> EvaluationResult:
    """Look up and evaluate a predicate by ID."""
    fn = REGISTRY.get(predicate_id)
    if fn is None:
        raise ValueError(f"unknown predicate: {predicate_id}")
    return fn(
        chain_window=chain_window,
        now=now,
        consent_record=consent_record,
        counterparty_class=counterparty_class,
    )


__all__ = [
    "PREDICATE_NAMESPACE",
    "P_IN_BASELINE_24H_ID",
    "PredicateValue",
    "EvaluationResult",
    "REGISTRY",
    "evaluate",
    "in_baseline_24h",
]
