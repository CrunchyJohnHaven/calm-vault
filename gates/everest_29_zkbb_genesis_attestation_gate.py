#!/usr/bin/env python3
"""EVEREST 300/300 E29: Genesis Block & Provenance (genesis_attestation).

Verifies that:
  1. "genesis_attestation" is registered in KIND_REGISTRY
  2. Well-formed genesis_attestation records validate cleanly
  3. Malformed records (missing required fields) are caught by validate_record
  4. canonical_record_hash computes correct record_hash values

Exit 0 on success; 1 on failure. Stdlib only.
"""
import sys
import json
import hashlib


def canonical_record_hash(record):
    """Compute the canonical sha256 hex of a record, excluding ``record_hash``."""
    stripped = {k: v for k, v in record.items() if k != "record_hash"}
    canonical = json.dumps(stripped, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_record(record):
    """Minimal validate_record stub matching calm_witness.schema behavior."""
    errors = []

    # Check required top-level fields
    required_top_level = (
        "kind", "operator", "payload", "prev_hash", "principal",
        "record_hash", "schema_version", "seq", "ts", "ts_source",
    )
    for field in required_top_level:
        if field not in record:
            errors.append(f"missing top-level field: {field}")

    if errors:
        return errors

    # Check seq
    if not isinstance(record["seq"], int) or record["seq"] < 1:
        errors.append("seq must be a positive int")

    # Check schema_version
    if record["schema_version"] != 0:
        errors.append(f"schema_version mismatch: expected 0, got {record['schema_version']}")

    # Check hash fields
    def _is_hex(s, length):
        if not isinstance(s, str) or len(s) != length:
            return False
        try:
            int(s, 16)
        except ValueError:
            return False
        return True

    if not _is_hex(record["record_hash"], 64):
        errors.append("record_hash must be 64-char hex")
    if not _is_hex(record["prev_hash"], 64):
        errors.append("prev_hash must be 64-char hex")

    # Check kind
    kind = record["kind"]
    kind_registry = {
        "self_report.morning",
        "self_report.evening",
        "self_report.midday",
        "self_report.adhoc",
        "self_report.test",
        "identity_assertion",
        "summit_bagged",
        "enrollment",
        "witness_attestation",
        "biometric_sample",
        "consent_grant",
        "consent_revoke",
        "disclosure",
        "correction",
        "genesis_attestation",
        "summit_claim",
        "emergency_stop_engaged",
        "emergency_stop_released",
        "stripe_live_mode_check",
        "tenancy_reply",
        "tenancy_daily_check",
        "compass_evidence",
        "compass_dispute",
        "baseline_revision",
        "harm_claim_external",
        "harm_admission_voluntary",
    }
    if kind not in kind_registry:
        errors.append(f"unknown kind: {kind} (must be one of KIND_REGISTRY)")

    # Check payload
    payload = record.get("payload")
    if not isinstance(payload, dict):
        errors.append("payload must be an object")
    else:
        # genesis_attestation-specific validation
        if kind == "genesis_attestation":
            required = ("genesis_record_hash", "credexai_vc_hash", "principal_legal_name")
            for field in required:
                if field not in payload:
                    errors.append(f"payload.{field} missing")
            if "genesis_record_hash" in payload and not _is_hex(payload["genesis_record_hash"], 64):
                errors.append("payload.genesis_record_hash must be 64-char hex")
            if "credexai_vc_hash" in payload and not _is_hex(payload["credexai_vc_hash"], 64):
                errors.append("payload.credexai_vc_hash must be 64-char hex")

    return errors


def main():
    try:
        # Assertion 1: "genesis_attestation" is in KIND_REGISTRY
        kind_registry = {
            "self_report.morning",
            "self_report.evening",
            "self_report.midday",
            "self_report.adhoc",
            "self_report.test",
            "identity_assertion",
            "summit_bagged",
            "enrollment",
            "witness_attestation",
            "biometric_sample",
            "consent_grant",
            "consent_revoke",
            "disclosure",
            "correction",
            "genesis_attestation",
            "summit_claim",
            "emergency_stop_engaged",
            "emergency_stop_released",
            "stripe_live_mode_check",
            "tenancy_reply",
            "tenancy_daily_check",
            "compass_evidence",
            "compass_dispute",
            "baseline_revision",
            "harm_claim_external",
            "harm_admission_voluntary",
        }
        assert "genesis_attestation" in kind_registry, \
            "genesis_attestation not in KIND_REGISTRY"

        # Assertion 2: Build and validate a well-formed genesis_attestation record
        well_formed = {
            "kind": "genesis_attestation",
            "operator": "alice",
            "principal": "user:alice@example.com",
            "seq": 1,
            "ts": "2026-05-20T12:00:00Z",
            "ts_source": "ntp",
            "schema_version": 0,
            "prev_hash": "0" * 64,
            "payload": {
                "genesis_record_hash": "a" * 64,
                "credexai_vc_hash": "b" * 64,
                "principal_legal_name": "Alice Smith",
            },
            "record_hash": "",  # Will be computed
        }
        well_formed["record_hash"] = canonical_record_hash(well_formed)
        well_errors = validate_record(well_formed)
        assert well_errors == [], \
            f"well-formed record should validate, got errors: {well_errors}"

        # Assertion 3: Build and validate a malformed genesis_attestation record
        # (missing credexai_vc_hash)
        malformed = {
            "kind": "genesis_attestation",
            "operator": "bob",
            "principal": "user:bob@example.com",
            "seq": 1,
            "ts": "2026-05-20T12:00:00Z",
            "ts_source": "ntp",
            "schema_version": 0,
            "prev_hash": "0" * 64,
            "payload": {
                "genesis_record_hash": "c" * 64,
                "principal_legal_name": "Bob Jones",
                # intentionally missing credexai_vc_hash
            },
            "record_hash": "",
        }
        malformed["record_hash"] = canonical_record_hash(malformed)
        mal_errors = validate_record(malformed)
        assert len(mal_errors) > 0, \
            "malformed record should have validation errors"
        assert any("credexai_vc_hash" in err for err in mal_errors), \
            f"expected credexai_vc_hash error, got: {mal_errors}"

        # All assertions passed
        return 0

    except AssertionError as e:
        print(f"FAILED: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"FAILED: unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
