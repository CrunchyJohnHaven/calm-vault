"""calm_witness.schema — JSON Schema (v0) for ``user_state.jsonl`` records.

Schema-level acceptance for Everest 26. The schema mirrors USER_STATE_PROTOCOL.md
and constrains every chain record to a small, evolvable set of ``kind`` discriminators.

We avoid a third-party schema validator because (a) the chain verifier already
ships stdlib-only and (b) the schema has only a handful of conditional rules.
``validate_record`` returns a list of error strings; an empty list means valid.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

SCHEMA_VERSION = 0

# Kinds that are valid in v0. Keeping the registry explicit forces every new
# kind to be reviewed (no silent extension); maps to Everest 7 review process.
KIND_REGISTRY = {
    "self_report.morning",
    "self_report.evening",
    "self_report.midday",
    "self_report.adhoc",
    "self_report.test",          # reserved for fixture chains
    "identity_assertion",
    "summit_bagged",
    "enrollment",
    "witness_attestation",
    "biometric_sample",
    "consent_grant",
    "consent_revoke",
    "disclosure",
    "correction",
    "genesis_attestation",       # binds seq=1 to a CredexAI VC after E22 lands
}

REQUIRED_TOP_LEVEL = (
    "kind",
    "operator",
    "payload",
    "prev_hash",
    "principal",
    "record_hash",
    "schema_version",
    "seq",
    "ts",
    "ts_source",
)

HASH_LEN = 64  # sha256 hex


def _is_hex(s: Any, length: int) -> bool:
    if not isinstance(s, str) or len(s) != length:
        return False
    try:
        int(s, 16)
    except ValueError:
        return False
    return True


def _validate_self_report(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ("affect", "known_health_issues", "note", "readiness", "restedness")
    for field in required:
        if field not in payload:
            errors.append(f"payload.{field} missing")
    if "affect" in payload and not isinstance(payload["affect"], list):
        errors.append("payload.affect must be a list of strings")
    if "known_health_issues" in payload and not isinstance(payload["known_health_issues"], list):
        errors.append("payload.known_health_issues must be a list")
    if "restedness" in payload and payload["restedness"] not in {
        "fully_rested", "rested", "mixed", "tired", "exhausted",
    }:
        errors.append(f"payload.restedness has unknown value: {payload['restedness']}")
    return errors


def _validate_summit_bagged(payload: Dict[str, Any]) -> List[str]:
    """v0 is intentionally permissive about summit_bagged record shape.

    Multiple autonomous sessions converged on slightly different field names
    (``summit_number`` vs ``summit_number_in_route_map``; ``evidence_path`` vs
    ``evidence_paths``; ``evidence_sha256`` as scalar vs map). The v0 contract:

    - Hard-required: ``summit_name`` and ``phase`` (one summit, one phase).
    - Soft-required (record must contain at least one of each pair):
      a route-map number AND a path or paths to the evidence.
    - Hex validation runs whenever a sha256-shaped field is present.

    Future versions (E54 review process) may tighten this.
    """
    errors: List[str] = []
    for field in ("summit_name", "phase"):
        if field not in payload:
            errors.append(f"payload.{field} missing")
    if not (
        "summit_number" in payload or "summit_number_in_route_map" in payload
    ):
        errors.append(
            "payload missing route-map index "
            "(need 'summit_number' or 'summit_number_in_route_map')"
        )
    for field in ("summit_number", "summit_number_in_route_map"):
        if field in payload:
            n = payload[field]
            if not isinstance(n, int) or not (1 <= n <= 100):
                errors.append(f"payload.{field} must be int in [1, 100]")
    if not ("evidence_path" in payload or "evidence_paths" in payload):
        errors.append(
            "payload missing evidence (need 'evidence_path' or 'evidence_paths')"
        )
    evid = payload.get("evidence_sha256")
    if isinstance(evid, str) and not _is_hex(evid, HASH_LEN):
        errors.append("payload.evidence_sha256 (scalar) must be 64-char hex")
    elif isinstance(evid, dict):
        for key, val in evid.items():
            if not _is_hex(val, HASH_LEN):
                errors.append(f"payload.evidence_sha256[{key!r}] must be 64-char hex")
    return errors


def _validate_genesis_attestation(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ("genesis_record_hash", "credexai_vc_hash", "principal_legal_name")
    for field in required:
        if field not in payload:
            errors.append(f"payload.{field} missing")
    if "genesis_record_hash" in payload and not _is_hex(payload["genesis_record_hash"], HASH_LEN):
        errors.append("payload.genesis_record_hash must be 64-char hex")
    if "credexai_vc_hash" in payload and not _is_hex(payload["credexai_vc_hash"], HASH_LEN):
        errors.append("payload.credexai_vc_hash must be 64-char hex")
    return errors


def _validate_disclosure(payload: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    required = ("predicate_id", "counterparty_class", "counterparty_id_hash")
    for field in required:
        if field not in payload:
            errors.append(f"payload.{field} missing")
    if "predicate_id" in payload and not str(payload["predicate_id"]).startswith(
        "calm-witness/predicate/v0/"
    ):
        errors.append("payload.predicate_id must be a v0 registry slug")
    return errors


PAYLOAD_VALIDATORS = {
    "self_report.morning": _validate_self_report,
    "self_report.evening": _validate_self_report,
    "self_report.midday": _validate_self_report,
    "self_report.adhoc": _validate_self_report,
    # self_report.test is intentionally permissive (test-fixture kind).
    "summit_bagged": _validate_summit_bagged,
    "genesis_attestation": _validate_genesis_attestation,
    "disclosure": _validate_disclosure,
}


def validate_record(record: Dict[str, Any]) -> List[str]:
    """Return a list of error strings; empty list means valid."""
    errors: List[str] = []

    for field in REQUIRED_TOP_LEVEL:
        if field not in record:
            errors.append(f"missing top-level field: {field}")

    if errors:  # don't probe further on a structurally broken record
        return errors

    if not isinstance(record["seq"], int) or record["seq"] < 1:
        errors.append("seq must be a positive int")

    if record["schema_version"] != SCHEMA_VERSION:
        errors.append(
            f"schema_version mismatch: expected {SCHEMA_VERSION}, got {record['schema_version']}"
        )

    if not _is_hex(record["record_hash"], HASH_LEN):
        errors.append("record_hash must be 64-char hex")
    if not _is_hex(record["prev_hash"], HASH_LEN):
        errors.append("prev_hash must be 64-char hex")

    kind = record["kind"]
    if kind not in KIND_REGISTRY:
        errors.append(f"unknown kind: {kind} (must be one of KIND_REGISTRY)")

    payload = record.get("payload")
    if not isinstance(payload, dict):
        errors.append("payload must be an object")
    else:
        validator = PAYLOAD_VALIDATORS.get(kind)
        if validator is not None:
            errors.extend(validator(payload))
        # kinds without a specific validator (witness_attestation, biometric_sample,
        # enrollment, consent_*, correction, identity_assertion) are intentionally
        # permissive in v0; they bag their own validators when their summits ship.

    return errors


def validate_chain(records: List[Dict[str, Any]]) -> Dict[int, List[str]]:
    """Validate every record; return ``{seq: errors}`` for records with errors."""
    out: Dict[int, List[str]] = {}
    for rec in records:
        errs = validate_record(rec)
        if errs:
            out[rec.get("seq", -1)] = errs
    return out


__all__ = [
    "SCHEMA_VERSION",
    "KIND_REGISTRY",
    "validate_record",
    "validate_chain",
]
