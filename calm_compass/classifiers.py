"""calm_compass.classifiers — open-source, hash-pinned behavioural classifiers.

Each classifier maps a chain record → small integer score. The protocol binds
the classifier source-code hash into every Compass proof, so a counterparty
verifying the proof knows exactly which evaluator the operator used.

v0 ships four classifiers — one per v0 predicate. They are intentionally
*simple, conservative, and inspectable*. False positives and false negatives
are both expected at v0; the principal can dispute via ``kind: "compass_dispute"``
chain records, and the protocol stays honest about its v0 limits.
"""
from __future__ import annotations

import hashlib
import inspect
import re
from typing import Any, Callable, Dict, List, Optional, Set


# ─── V-01 unselfish_disposition ──────────────────────────────────────────────

# Generosity-without-expectation patterns. Conservative; we want signal not noise.
_UNSELFISH_GIVE_PATTERNS = [
    re.compile(r"\b(helping|helped) (with|out|her|him|them|you|people)\b", re.I),
    re.compile(r"\b(gave|giving|offer(ed|ing)?) (away|my time|my advice|free|gratis|pro bono)\b", re.I),
    re.compile(r"\b(donated|donation|gift|grant|stipend)\b.{0,40}\b(to|for)\b", re.I),
    re.compile(r"\b(introduced .{0,30} to|connecting .{0,30} with)\b", re.I),
    re.compile(r"\b(no charge|on me|my treat|happy to do)\b", re.I),
    re.compile(r"\b(mentored|mentoring|sponsored|sponsoring)\b", re.I),
]

# Anti-patterns that disqualify a record from counting as unselfish (e.g.
# transactional framing).
_UNSELFISH_DISQUALIFIERS = [
    re.compile(r"\bin (exchange|return) for\b", re.I),
    re.compile(r"\bquid pro quo\b", re.I),
    re.compile(r"\bafter (you|they) (give|gave|send|pay)\b", re.I),
]


def unselfish_disposition_score(record: Dict[str, Any]) -> int:
    """Return 1 if the record evidences generosity-without-expectation, else 0."""
    payload = record.get("payload", {})
    text = " ".join(str(v) for v in payload.values() if isinstance(v, (str, list)))
    if isinstance(payload.get("note"), str):
        text = payload["note"] + " " + text
    if any(p.search(text) for p in _UNSELFISH_DISQUALIFIERS):
        return 0
    if any(p.search(text) for p in _UNSELFISH_GIVE_PATTERNS):
        return 1
    return 0


# ─── V-02 cross_tribal_engagement ────────────────────────────────────────────

# Operates on a record + the principal's enrolled tribe map.
# Tribe map shape (per CC-10): { "self": {"groups": ["g1","g2"]},
#                                 "edges": {"g3": "across", "g4": "near"} }
# A record is "cross-tribal" if its payload references a group/individual the
# tribe map labels as "across".

def cross_tribal_engagement_score(record: Dict[str, Any],
                                  tribe_map: Optional[Dict[str, Any]] = None) -> int:
    """Return 1 if the record references an across-tribe individual/group, else 0.

    v0 placeholder logic: detects explicit references to groups marked "across"
    in the principal's tribe map. v1 will use a graph traversal on the enrolled
    affinity graph.
    """
    if not tribe_map:
        return 0
    across_groups: Set[str] = {
        g for g, edge in (tribe_map.get("edges") or {}).items() if edge == "across"
    }
    if not across_groups:
        return 0
    payload = record.get("payload", {})
    text = " ".join(str(v) for v in payload.values() if isinstance(v, (str, list)))
    text_lower = text.lower()
    for g in across_groups:
        if g.lower() in text_lower:
            return 1
    return 0


# ─── V-03 respects_difference ────────────────────────────────────────────────

_RESPECT_PATTERNS = [
    re.compile(r"\b(thank you|i appreciate|i hear you|i understand|that makes sense)\b", re.I),
    re.compile(r"\b(curious|interested) (about|in) (your|their) (view|perspective|take|experience)\b", re.I),
    re.compile(r"\bi was wrong\b|\bi made a mistake\b|\bmy mistake\b|\bi apologize\b", re.I),
    re.compile(r"\b(your|their) (point|argument) (is|was) (good|valid|fair|interesting)\b", re.I),
    re.compile(r"\bi (hadn'?t|didn'?t) (thought|considered) (of|about) that\b", re.I),
]

_CONTEMPT_PATTERNS = [
    re.compile(r"\b(stupid|idiotic|moronic|brain-?dead|retarded)\b", re.I),
    re.compile(r"\b(those people|these people)\b", re.I),
    re.compile(r"\b(can'?t (stand|believe|fathom)) (these|those)\b", re.I),
    re.compile(r"\b(typical .{0,15} (always|never)|of course they (would|did))\b", re.I),
    re.compile(r"\b(deserve(s)? what|got what they (deserve|deserved))\b", re.I),
]


def respects_difference_score(record: Dict[str, Any]) -> int:
    """Return +1 for respect, -1 for contempt, 0 otherwise."""
    payload = record.get("payload", {})
    text = " ".join(str(v) for v in payload.values() if isinstance(v, (str, list)))
    has_respect = any(p.search(text) for p in _RESPECT_PATTERNS)
    has_contempt = any(p.search(text) for p in _CONTEMPT_PATTERNS)
    if has_contempt and not has_respect:
        return -1
    if has_respect and not has_contempt:
        return 1
    return 0


# ─── V-04 no_evidence_of_willful_harm ────────────────────────────────────────

def no_evidence_of_willful_harm_score(record: Dict[str, Any]) -> int:
    """Return -1 if the record evidences willful harm; 0 otherwise.

    Conservative: returns negative only on positive evidence (operator-set flag,
    external claim, voluntary admission). The protocol's overall predicate
    fires TRUE iff the *aggregate* sum is ≥ 0 (no negative records) — i.e.,
    no evidence rather than positive evidence of innocence.
    """
    payload = record.get("payload", {})
    if payload.get("flag_willful_harm") is True:
        return -1
    if record.get("kind") == "harm_claim_external":
        return -1
    if record.get("kind") == "harm_admission_voluntary":
        return -1
    return 0


# ─── Registry + classifier hashing ──────────────────────────────────────────

CLASSIFIERS: Dict[str, Callable[..., int]] = {
    "calm-compass/predicate/v0/unselfish_disposition": unselfish_disposition_score,
    "calm-compass/predicate/v0/cross_tribal_engagement": cross_tribal_engagement_score,
    "calm-compass/predicate/v0/respects_difference": respects_difference_score,
    "calm-compass/predicate/v0/no_evidence_of_willful_harm": no_evidence_of_willful_harm_score,
}


def classifier_hash(predicate_id: str) -> str:
    """Content-addressable hash of the classifier source code (CC-33 binding)."""
    fn = CLASSIFIERS.get(predicate_id)
    if fn is None:
        raise ValueError(f"unknown predicate: {predicate_id}")
    source = inspect.getsource(fn).encode("utf-8")
    return hashlib.sha256(source).hexdigest()


def score_chain(
    chain: List[Dict[str, Any]],
    predicate_id: str,
    tribe_map: Optional[Dict[str, Any]] = None,
) -> List[int]:
    """Score every record in the chain under the named classifier."""
    fn = CLASSIFIERS.get(predicate_id)
    if fn is None:
        raise ValueError(f"unknown predicate: {predicate_id}")
    if predicate_id.endswith("cross_tribal_engagement"):
        return [fn(rec, tribe_map=tribe_map) for rec in chain]
    return [fn(rec) for rec in chain]


__all__ = [
    "CLASSIFIERS",
    "classifier_hash",
    "score_chain",
    "unselfish_disposition_score",
    "cross_tribal_engagement_score",
    "respects_difference_score",
    "no_evidence_of_willful_harm_score",
]
