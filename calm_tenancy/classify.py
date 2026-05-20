"""calm_tenancy.classify — inbound classification + response-seeking detector (CT-10, CT-11).

Two deterministic classifiers operating on the inbound email's subject + body:

  1. ``classify(text) -> 'red' | 'yellow' | 'green'``
     Reuses the safety-rubric pattern from
     ``~/CredexAI/scripts/creativity_mailbox_safety_gate.py``, extended with
     additional yellow patterns relevant to founder / journalist / researcher
     inbound (not just elder care).

  2. ``is_response_seeking(text) -> bool``
     Heuristic deterministic check for whether the sender expects a reply.

Both are pure functions; no model calls, no external services.
"""
from __future__ import annotations

import re
from typing import Tuple

# --- CT-10 RED patterns (safety-critical; immediate principal escalation) ---
RED_PATTERNS = [
    re.compile(r"\b(kill (myself|himself|herself|themselves|me))\b", re.I),
    re.compile(r"\b(suicid(e|al)|self[- ]harm)\b", re.I),
    re.compile(r"\b(emergenc(y|ies)|urgent|life[- ]threatening)\b", re.I),
    re.compile(r"\b(chest pain|stroke|heart attack|seizure)\b", re.I),
    re.compile(r"\b(abuse|neglect|assault|stalking|threat)\b", re.I),
    # Credential / financial fraud
    re.compile(r"\b(password|account number|social security|ssn|wire transfer)\b", re.I),
    re.compile(r"\b(lawsuit|subpoena|served|warrant)\b", re.I),
    # Cohab-class escalation: a known-named individual is upset
    re.compile(r"\b(this is upsetting|i'?m? (upset|hurt|disturbed) by your|please stop (emailing|contacting) me)\b", re.I),
]

# --- CT-10 YELLOW patterns (sensitive; human-shaped reply within 4h) ---
YELLOW_PATTERNS = [
    re.compile(r"\b(lonely|grief|loss|depressed|anxious)\b", re.I),
    re.compile(r"\b(scam|fraud|phishing|impersonat)\b", re.I),
    re.compile(r"\b(insurance|benefits|appointment|hospital|doctor)\b", re.I),
    re.compile(r"\b(family conflict|estranged|custody)\b", re.I),
    re.compile(r"\b(complaint|grievance|disappointed)\b", re.I),
    re.compile(r"\b(interview|podcast|panel|story|piece|article) (with|for|about)\b", re.I),
    re.compile(r"\b(investment|partnership|acquisition|term sheet)\b", re.I),
]

# --- CT-11 response-seeking signals ---
RESPONSE_SEEKING_PATTERNS = [
    re.compile(r"\?\s*$", re.M),                            # ends in a question mark
    re.compile(r"\b(could you|can you|would you|will you|please (let me know|reply|respond|confirm))\b", re.I),
    re.compile(r"\b(when (can|would|will)|how (should|do))\b", re.I),
    re.compile(r"\b(rsvp|by when|deadline)\b", re.I),
    re.compile(r"\b(let me know|get back to me|hear from you|need a (response|reply|answer))\b", re.I),
    re.compile(r"\b(any (thoughts|chance|update|news)|thoughts\?|wdyt|what do you think)\b", re.I),
]

# --- patterns that override response-seeking to false ---
NOT_RESPONSE_SEEKING_PATTERNS = [
    re.compile(r"\b(no reply needed|no response (necessary|needed|required)|this is informational only)\b", re.I),
    re.compile(r"\b(unsubscribe|do[- ]not[- ]reply|noreply)\b", re.I),
    re.compile(r"\b(out of office|auto[- ]reply|i'?ll be away)\b", re.I),
]


def classify(text: str) -> str:
    """Return 'red' | 'yellow' | 'green'."""
    for p in RED_PATTERNS:
        if p.search(text):
            return "red"
    for p in YELLOW_PATTERNS:
        if p.search(text):
            return "yellow"
    return "green"


def is_response_seeking(text: str) -> bool:
    """Return True if the sender appears to expect a reply."""
    for p in NOT_RESPONSE_SEEKING_PATTERNS:
        if p.search(text):
            return False
    for p in RESPONSE_SEEKING_PATTERNS:
        if p.search(text):
            return True
    # Default: very short messages (< 30 chars) without explicit ask are usually informational;
    # longer messages without explicit ask default to response-seeking (safer for SLA).
    return len(text.strip()) >= 30


def classify_and_route(text: str) -> Tuple[str, bool, str]:
    """One-shot: classification, response-seeking, and the SLA window in seconds.

    Returns (classification, response_seeking, expected_window_seconds_label).
    """
    c = classify(text)
    rs = is_response_seeking(text)
    expected = {"red": "600", "yellow": "14400", "green": "3600"}[c]
    return c, rs, expected


__all__ = [
    "classify",
    "is_response_seeking",
    "classify_and_route",
    "RED_PATTERNS",
    "YELLOW_PATTERNS",
    "RESPONSE_SEEKING_PATTERNS",
]
