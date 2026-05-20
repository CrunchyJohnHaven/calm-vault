# Calm Compass — Evidence-Record Validator Spec v0

**Date:** 2026-05-20
**Status:** Draft
**Authority:** COMPASS_PREDICATES_v0.md §3; Calm Witness Everest 26 (E26), Everest 28 (E28)

---

## Scope

This specification defines validation rules for the six evidence-record kinds introduced in COMPASS_PREDICATES_v0.md §3: `unselfish_act`, `cross_group_interaction`, `refused_harm`, `counter_claim`, `principal_rebuttal`, `respect_engagement`, and `correction_accepted`. A reference Python module sketch (`calm_witness/compass_validator.py`) accompanies these rules. Validators conforming to this spec MUST implement all checks labeled HARD. Checks labeled SOFT produce warnings, not errors. Records failing a HARD check are rejected. Records failing a SOFT check are flagged but retained unless a Content Guard mandates exclusion.

---

## Per-Kind Field Completeness

### unselfish_act

Required fields and types:

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"unselfish_act"` |
| `subject_id` | `str` | HARD |
| `other_party_id` | `str` | HARD |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `description` | `str` | HARD; non-empty |
| `expectation_of_return` | `bool` | HARD |
| `other_party_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

### cross_group_interaction

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"cross_group_interaction"` |
| `subject_id` | `str` | HARD |
| `other_party_id` | `str` | HARD |
| `group_distance_axis` | `str` | HARD; non-empty |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `description` | `str` | HARD; non-empty |
| `other_party_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

### refused_harm

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"refused_harm"` |
| `subject_id` | `str` | HARD |
| `harm_category` | `str` | HARD; non-empty |
| `pressure_source` | `str` | SOFT; omission triggers warning |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `description` | `str` | HARD; non-empty |
| `record_hash` | `str` (hex SHA-256) | HARD |

Note: `refused_harm` is a single-party record; `other_party_signature` is absent by design. Chain-integrity check still applies via `record_hash`.

### counter_claim

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"counter_claim"` |
| `subject_id` | `str` | HARD |
| `claimant_id` | `str` | HARD; see Counter-Claim Attribution |
| `target_record_id` | `str` (UUID v4) | HARD; must reference an existing record |
| `claim_text` | `str` | HARD; non-empty |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `claimant_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

### principal_rebuttal

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"principal_rebuttal"` |
| `subject_id` | `str` | HARD |
| `target_counter_claim_id` | `str` (UUID v4) | HARD; must reference a `counter_claim` record |
| `rebuttal_text` | `str` | HARD; non-empty |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `subject_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

### respect_engagement

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"respect_engagement"` |
| `subject_id` | `str` | HARD |
| `other_party_id` | `str` | HARD |
| `engagement_context` | `str` | HARD; non-empty |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `description` | `str` | HARD; non-empty |
| `other_party_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

### correction_accepted

| Field | Type | Constraint |
|---|---|---|
| `record_id` | `str` (UUID v4) | HARD |
| `record_kind` | `str` | HARD; value must be `"correction_accepted"` |
| `subject_id` | `str` | HARD |
| `corrector_id` | `str` | HARD |
| `prior_claim_or_behavior` | `str` | HARD; non-empty |
| `correction_text` | `str` | HARD; non-empty |
| `timestamp_utc` | `str` (ISO 8601) | HARD |
| `corrector_signature` | `str` (base64url Ed25519) | HARD |
| `record_hash` | `str` (hex SHA-256) | HARD |

---

## Content Guards

**CG-1 (unselfish_act — silent exclusion).** If `expectation_of_return` is `true`, the record is silently excluded from all predicate sums. It is NOT an error; no `Issue` is emitted. The record is retained in the vault but contributes zero weight to any compass computation. Validators MUST NOT raise an error on this field value.

**CG-2 (timestamp ordering).** `timestamp_utc` must parse as a valid ISO 8601 datetime. Records with unparseable timestamps are HARD-rejected.

**CG-3 (description floor).** `description` and equivalent prose fields (`claim_text`, `rebuttal_text`, `correction_text`, `prior_claim_or_behavior`) must contain at least 10 non-whitespace characters. Shorter values are HARD-rejected.

**CG-4 (group distance axis non-null).** `group_distance_axis` in `cross_group_interaction` must not be `"none"` or an empty string. HARD.

**CG-5 (self-referential records).** `other_party_id` must differ from `subject_id`. Same-value pairs are HARD-rejected for all two-party kinds.

---

## Two-Party-Record Signatures

Applies to: `unselfish_act`, `cross_group_interaction`, `respect_engagement`, `correction_accepted`, `counter_claim` (via `claimant_signature`), `principal_rebuttal` (via `subject_signature`).

**Canonical bytes:** The canonical form is the JSON serialization of the record with `other_party_signature` (or the relevant signature field) removed, keys sorted lexicographically, no trailing whitespace, UTF-8 encoded.

**Verification:** The validator resolves the public key registered to the signing party (`other_party_id`, `claimant_id`, `corrector_id`, or `subject_id` as applicable) from the E26 identity registry, then verifies the Ed25519 signature over the canonical bytes. Failure is HARD-rejected with issue code `SIG_INVALID`.

**Key resolution failure:** If the signing party's public key cannot be resolved from E26, emit issue code `SIG_KEY_UNKNOWN` (HARD).

---

## Counter-Claim Attribution

**CC-1 (no anonymous counter-claims).** `claimant_id` must be a non-empty string identifying a registered principal. An empty, null, or `"anonymous"` value is HARD-rejected with issue code `COUNTER_CLAIM_ANONYMOUS`.

**CC-2 (target record existence).** `target_record_id` must resolve to an existing record in the vault. Dangling references are HARD-rejected with issue code `COUNTER_CLAIM_TARGET_MISSING`.

**CC-3 (claimant signature required).** `claimant_signature` must pass Ed25519 verification as specified in Two-Party-Record Signatures. Unsigned counter-claims are HARD-rejected with issue code `SIG_INVALID`.

---

## Chain Integrity

Every evidence record carries a `record_hash` field. This hash must validate per the Calm Witness Everest 28 chain-integrity protocol:

1. Recompute `record_hash` as `SHA-256(canonical_bytes)` where canonical bytes are defined identically to the signature canonical form above, except the `record_hash` field itself is also excluded before serialization.
2. Compare the recomputed hash to the stored `record_hash` value (hex, lowercase). Mismatch is HARD-rejected with issue code `HASH_MISMATCH`.
3. The E28 chain verifier must additionally confirm that `record_hash` appears in the append-only Everest chain at the expected sequence position. Absence from the chain is HARD-rejected with issue code `CHAIN_MISSING`.

The validator delegates step 3 to the E28 chain verifier module (`calm_witness.chain.everest28.verify_record_in_chain`). If that module is unavailable, validators MUST surface issue code `CHAIN_VERIFIER_UNAVAILABLE` and abort the record rather than silently passing.

---

## Python Module Sketch

```python
# calm_witness/compass_validator.py
"""
Evidence-record validator for Calm Compass.
Cross-references: E26 schema validator (calm_witness.schema.e26),
                  E28 chain verifier (calm_witness.chain.everest28).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class Issue:
    record_id: str | None
    severity: str          # "error" | "warning"
    code: str              # e.g. "SIG_INVALID", "HASH_MISMATCH"
    detail: str

def validate_evidence_record(record: dict[str, Any]) -> list[Issue]:
    """
    Validate a single evidence record dict.

    Returns a list of Issue objects. An empty list means the record
    passed all HARD checks (warnings may still appear in the list).
    Records with expectation_of_return=true for unselfish_act produce
    no Issues; callers must separately check the exclusion flag.

    Raises nothing — all anomalies are surfaced as Issue objects.
    """
    issues: list[Issue] = []
    record_id: str | None = record.get("record_id")
    kind: str | None = record.get("record_kind")

    issues += _check_field_completeness(record_id, kind, record)
    if _has_hard_error(issues):
        return issues

    issues += _check_content_guards(record_id, kind, record)
    if kind != "refused_harm":
        issues += _check_signature(record_id, kind, record)
    if kind == "counter_claim":
        issues += _check_counter_claim_attribution(record_id, record)

    issues += _check_chain_integrity(record_id, record)
    return issues

# -- private helpers (signatures only; implementations omitted) --

def _check_field_completeness(
    record_id: str | None, kind: str | None, record: dict[str, Any]
) -> list[Issue]: ...

def _check_content_guards(
    record_id: str | None, kind: str | None, record: dict[str, Any]
) -> list[Issue]: ...

def _check_signature(
    record_id: str | None, kind: str | None, record: dict[str, Any]
) -> list[Issue]: ...

def _check_counter_claim_attribution(
    record_id: str | None, record: dict[str, Any]
) -> list[Issue]: ...

def _check_chain_integrity(
    record_id: str | None, record: dict[str, Any]
) -> list[Issue]: ...

def _has_hard_error(issues: list[Issue]) -> bool:
    return any(i.severity == "error" for i in issues)
```

Callers accumulating scores MUST check whether `record.get("record_kind") == "unselfish_act"` and `record.get("expectation_of_return") is True` before applying weight, and silently skip such records from all sums regardless of validation outcome.

---

## Cross-References

| Reference | Role |
|---|---|
| `COMPASS_PREDICATES_v0.md §3` | Authoritative record-kind schemas |
| E26 — Everest 26 schema validator (`calm_witness.schema.e26`) | Identity registry; public-key resolution for signature checks |
| E28 — Everest 28 chain verifier (`calm_witness.chain.everest28.verify_record_in_chain`) | Append-only chain membership; `CHAIN_MISSING` and `CHAIN_VERIFIER_UNAVAILABLE` issue codes |
| Calm Witness ZKBB-User Everest route | Tamperproof user-state attestation context; bank-teller-note bit |

Implementations MUST pin to the same E26 identity-registry snapshot used when the record was originally committed. Time-of-check vs. time-of-use key rotation is out of scope for v0 and deferred to v1.

---

*Specification authored by CALM (AI Moneyball / Calm Witness project).*
*Signed: CALM — 2026-05-20*
*Operator signature block: John Bradley, CALM project principal, calm_vault_market, 2026-05-20*
