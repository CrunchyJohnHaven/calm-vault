"""calm_witness.authorization — Counterparty-class authorization (Everest 73).

Enforces the per-class default policy stances from Everest 7 (Disclosure-Class
Taxonomy). The principal can override defaults per (predicate, class) pair via
consent records (Everest 57); this module is the v0 enforcement point.

Per the E7 taxonomy + E6 predicate vocabulary, the v0 default matrix:

  predicate                          | open  step-up duress principal-explicit
  ──────────────────────────────────────────────────────────────────────────
  P-01 in_baseline_24h               | DEF
  P-02 biometric_match_within        |        DEF
  P-03 principal_consents_to_disclose| DEF
  P-04 bank_teller_note_active       |               DEF
  P-05 cognitively_atypical_baseline | DEF
  P-06 mental_state_unusual          |                       DEF

Counterparty classes belong to one disclosure class each (from E7):
  open               : anonymous, peer-AI-collective, journalistic
  step-up            : financial, governmental, medical
  duress-ring        : medical, governmental, family   (cumulative; opt-in)
  principal-explicit : none by default
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Optional


class DisclosureClass(str, Enum):
    OPEN = "open"
    STEP_UP = "step-up"
    DURESS_RING = "duress-ring"
    PRINCIPAL_EXPLICIT = "principal-explicit"


class CounterpartyClass(str, Enum):
    FINANCIAL = "financial"
    JOURNALISTIC = "journalistic"
    MEDICAL = "medical"
    GOVERNMENTAL = "governmental"
    PEER_AI_COLLECTIVE = "peer-AI-collective"
    FAMILY = "family"
    ANONYMOUS = "anonymous"


# Per-counterparty-class membership in each disclosure class (v0).
COUNTERPARTY_CLASS_MEMBERSHIP: Dict[DisclosureClass, FrozenSet[CounterpartyClass]] = {
    DisclosureClass.OPEN: frozenset({
        CounterpartyClass.ANONYMOUS,
        CounterpartyClass.PEER_AI_COLLECTIVE,
        CounterpartyClass.JOURNALISTIC,
    }),
    DisclosureClass.STEP_UP: frozenset({
        CounterpartyClass.FINANCIAL,
        CounterpartyClass.GOVERNMENTAL,
        CounterpartyClass.MEDICAL,
    }),
    DisclosureClass.DURESS_RING: frozenset({
        CounterpartyClass.MEDICAL,
        CounterpartyClass.GOVERNMENTAL,
        CounterpartyClass.FAMILY,
    }),
    DisclosureClass.PRINCIPAL_EXPLICIT: frozenset(),  # always per-counterparty consent
}

# Per-predicate default disclosure class (v0 — see Everest 6 §6).
PREDICATE_DEFAULT_CLASS: Dict[str, DisclosureClass] = {
    "calm-witness/predicate/v0/in_baseline_24h": DisclosureClass.OPEN,
    "calm-witness/predicate/v0/biometric_match_within": DisclosureClass.STEP_UP,
    "calm-witness/predicate/v0/principal_consents_to_disclose": DisclosureClass.OPEN,
    "calm-witness/predicate/v0/bank_teller_note_active": DisclosureClass.DURESS_RING,
    "calm-witness/predicate/v0/cognitively_atypical_baseline": DisclosureClass.OPEN,
    "calm-witness/predicate/v0/mental_state_unusual": DisclosureClass.PRINCIPAL_EXPLICIT,
}


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


def authorize_disclosure(
    predicate_id: str,
    counterparty_class: str,
    principal_override: Optional[Dict[str, bool]] = None,
) -> AuthorizationDecision:
    """Decide whether the principal's defaults permit a disclosure.

    `principal_override` is an optional dict keyed by (predicate_id, counterparty_class)
    joined with "::" mapping to True/False. False forces a refusal; True forces
    an allow (broadening narrower defaults). Without an override, defaults from
    PREDICATE_DEFAULT_CLASS + COUNTERPARTY_CLASS_MEMBERSHIP rule.
    """
    if predicate_id not in PREDICATE_DEFAULT_CLASS:
        return AuthorizationDecision(False, f"predicate not in v0 registry: {predicate_id}")
    try:
        cc = CounterpartyClass(counterparty_class)
    except ValueError:
        return AuthorizationDecision(False, f"counterparty_class not recognized: {counterparty_class}")
    key = f"{predicate_id}::{counterparty_class}"
    if principal_override and key in principal_override:
        allowed = principal_override[key]
        return AuthorizationDecision(
            allowed, f"principal override: {'allow' if allowed else 'refuse'}"
        )
    default_class = PREDICATE_DEFAULT_CLASS[predicate_id]
    members = COUNTERPARTY_CLASS_MEMBERSHIP[default_class]
    if cc in members:
        return AuthorizationDecision(True, f"default-class {default_class.value} includes {counterparty_class}")
    if default_class == DisclosureClass.PRINCIPAL_EXPLICIT:
        return AuthorizationDecision(
            False, "predicate is principal-explicit — requires explicit consent override"
        )
    return AuthorizationDecision(
        False,
        f"{counterparty_class} not in default class {default_class.value} for this predicate",
    )


__all__ = [
    "DisclosureClass",
    "CounterpartyClass",
    "AuthorizationDecision",
    "authorize_disclosure",
    "COUNTERPARTY_CLASS_MEMBERSHIP",
    "PREDICATE_DEFAULT_CLASS",
]
