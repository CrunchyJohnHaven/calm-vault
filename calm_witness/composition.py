"""calm_witness.composition — predicate AND/OR composition (Everest 61).

Composes evaluation results from multiple predicates into a single response
without leaking the constituent values. The composed value follows three-valued
logic (`true`, `false`, `unknown`) with `refused` as an absorbing element.

Truth tables (v0):

  AND:  T F U R           OR:  T F U R
       ┌────────              ┌────────
     T │ T F U R            T │ T T T R
     F │ F F F R            F │ T F U R
     U │ U F U R            U │ T U U R
     R │ R R R R            R │ R R R R

Rationale:
  - REFUSED is absorbing: any operand refused → result refused (the principal
    has spoken; the operator must not leak even the *composed* bit).
  - UNKNOWN propagates conservatively: T∧U = U, F∧U = F (false dominates AND);
    F∨U = U, T∨U = T (true dominates OR).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

try:
    from predicates import EvaluationResult, PredicateValue
except ImportError:  # pragma: no cover
    from calm_witness.predicates import EvaluationResult, PredicateValue


def _v(r: EvaluationResult) -> PredicateValue:
    return r.value


def compose_and(results: Iterable[EvaluationResult]) -> PredicateValue:
    # REFUSED is absorbing; check all operands before short-circuiting on FALSE,
    # to avoid leaking "the refused branch was X" by way of the composite bit.
    values = [_v(r) for r in results]
    if PredicateValue.REFUSED in values:
        return PredicateValue.REFUSED
    if PredicateValue.FALSE in values:
        return PredicateValue.FALSE
    if PredicateValue.UNKNOWN in values:
        return PredicateValue.UNKNOWN
    return PredicateValue.TRUE


def compose_or(results: Iterable[EvaluationResult]) -> PredicateValue:
    values = [_v(r) for r in results]
    if PredicateValue.REFUSED in values:
        return PredicateValue.REFUSED
    if PredicateValue.TRUE in values:
        return PredicateValue.TRUE
    if PredicateValue.UNKNOWN in values:
        return PredicateValue.UNKNOWN
    return PredicateValue.FALSE


def negate(result: EvaluationResult) -> PredicateValue:
    """Proof of `¬p` is sound only when a positive proof of `false` exists.

    Per Everest 62 (Predicate Negation), `¬UNKNOWN = UNKNOWN` and
    `¬REFUSED = REFUSED` — absence of evidence is not evidence of absence.
    """
    v = _v(result)
    if v == PredicateValue.TRUE:
        return PredicateValue.FALSE
    if v == PredicateValue.FALSE:
        return PredicateValue.TRUE
    return v


@dataclass(frozen=True)
class CompositionDescriptor:
    """A counterparty's composed-disclosure request payload.

    Example: ``and(in_baseline_24h, not(mental_state_unusual))``
    """
    op: str  # "and" | "or"
    predicate_ids: List[str]


__all__ = [
    "compose_and",
    "compose_or",
    "negate",
    "CompositionDescriptor",
]
