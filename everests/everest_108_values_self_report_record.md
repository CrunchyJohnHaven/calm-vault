# Everest 108 — Values Self-Report Record Kind

*Phase IX — Values Vocabulary. Prereq: Everest 106, 107, 26.*

---

## Preamble

Everest 108 defines two new chain record kinds that enable principals to commit their values to the immutable ledger: `values_self_report` for initial declarations and `values_correction` for amendments. These records bind a principal's expressed values (per the ValuesVector type from E106 and the ten dimensions from E107) to a cryptographic chain state, creating an audit trail and enabling downstream predicates to reference a principal's self-authored alignment.

Self-reports are chronological snapshots. Each record is timestamped and chain-hashed, establishing a precise moment in the principal's history. Corrections do not erase prior reports; they supersede them in the chain semantics while preserving the original for audit purposes. This design preserves the integrity of the chain while allowing genuine growth and recalibration.

---

## §1. Integration with Existing Chain Schema

Both new kinds extend the schema defined in Everest 26. They:

- Append to the user_state.jsonl chain in chronological order, maintaining seq numbering.
- Follow the hash-chain semantics from Everest 28 (each record includes `prev_hash` and `record_hash`).
- Are backward-compatible: existing parsers that do not recognize `values_self_report` or `values_correction` simply skip them (unknown `kind` is ignored).
- Require validators in the reference parser (~/CredexAI/calm_witness/parse.py).

No existing record kind is modified. The chain remains append-only and immutable.

---

## §2. Record Kind: `values_self_report`

### Purpose

A principal declares their normative commitments across the ten v0 dimensions (Everest 107). This is the principal's authored baseline, collected at a specific moment in time.

### JSON Schema

```json
{
  "$id": "https://calm-witness.dev/schema/values_self_report_v0.json",
  "title": "ValuesSelfReport",
  "type": "object",
  "required": ["seq", "ts", "prev_hash", "kind", "payload", "principal_sig", "record_hash"],
  "properties": {
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "Strictly increasing sequence number in the chain."
    },
    "ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp with timezone offset (e.g., '2026-05-20T13:00:00-04:00')."
    },
    "prev_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the prior record in hex; zero-padded for genesis."
    },
    "kind": {
      "const": "values_self_report",
      "description": "Record kind identifier."
    },
    "payload": {
      "type": "object",
      "required": ["dimensions", "version", "context"],
      "properties": {
        "dimensions": {
          "type": "object",
          "additionalProperties": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10000
          },
          "description": "Map of dimension slugs to scalar values in [0, 10000]. Dimension keys must match the v0 set: cooperation, fairness, honesty, non_harm, cross_difference_respect, generosity, non_tribal_engagement, repair_after_harm, consistency_under_stress, principal_authored_other."
        },
        "version": {
          "const": "v0",
          "description": "Values vocabulary version. Currently locked to 'v0'."
        },
        "context": {
          "type": "string",
          "maxLength": 280,
          "description": "Principal-authored rationale or context for this self-report. Examples: 'initial enrollment self-report', 'reflection after team incident'."
        },
        "calibration_baseline": {
          "type": "string",
          "description": "Optional. Provenance of the values: 'self' (principal authored), 'inferred' (derived from evidence chain per E109), 'external_feedback' (others' assessment), 'hybrid'. Default: 'self'."
        }
      }
    },
    "principal_sig": {
      "type": "string",
      "description": "Ed25519 signature over the record (excluding this field) by the principal's signing key. Hex-encoded."
    },
    "record_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the complete record (excluding this field) in canonical form."
    }
  }
}
```

### Validation Rules

1. All ten v0 dimensions MUST be present in the payload.
2. Each dimension value MUST be an integer in [0, 10000].
3. The `context` field MUST not exceed 280 characters.
4. The `version` field MUST be exactly "v0".
5. The `principal_sig` MUST be a valid Ed25519 signature over the canonical form of the record (excluding `principal_sig` and `record_hash`).
6. The `record_hash` MUST match SHA-256(canonical_json(record \ {record_hash, principal_sig})).
7. The `prev_hash` MUST match the `record_hash` of the previous record in the chain.

### Semantics

- A `values_self_report` is a principal's authored snapshot of their normative commitments at a specific timestamp.
- The report is immutable once chain-committed.
- If the principal later changes their values (due to reflection, growth, or correction), a new `values_self_report` or a `values_correction` is appended; the original is never modified or deleted.
- Downstream predicates default to using the MOST RECENT non-corrected `values_self_report` unless explicitly time-windowed or constrained to a specific chain state.

### Example

```json
{
  "seq": 14,
  "ts": "2026-05-20T13:00:00-04:00",
  "prev_hash": "abc123def456...",
  "kind": "values_self_report",
  "payload": {
    "dimensions": {
      "cooperation": 7500,
      "fairness": 8000,
      "honesty": 8200,
      "non_harm": 9100,
      "cross_difference_respect": 7800,
      "generosity": 7200,
      "non_tribal_engagement": 6500,
      "repair_after_harm": 8400,
      "consistency_under_stress": 7600,
      "principal_authored_other": 6000
    },
    "version": "v0",
    "context": "initial enrollment self-report",
    "calibration_baseline": "self"
  },
  "principal_sig": "ed25519_sig_hex_string...",
  "record_hash": "def789ghi012..."
}
```

---

## §3. Record Kind: `values_correction`

### Purpose

A principal modifies an earlier `values_self_report`, providing explicit rationale for the change. The original report remains in the chain; the correction supersedes it for evaluation purposes.

### JSON Schema

```json
{
  "$id": "https://calm-witness.dev/schema/values_correction_v0.json",
  "title": "ValuesCorrection",
  "type": "object",
  "required": ["seq", "ts", "prev_hash", "kind", "payload", "principal_sig", "record_hash"],
  "properties": {
    "seq": {
      "type": "integer",
      "minimum": 0,
      "description": "Strictly increasing sequence number in the chain."
    },
    "ts": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp with timezone offset."
    },
    "prev_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the prior record in hex."
    },
    "kind": {
      "const": "values_correction",
      "description": "Record kind identifier."
    },
    "payload": {
      "type": "object",
      "required": ["supersedes_seq", "dimensions", "correction_reason"],
      "properties": {
        "supersedes_seq": {
          "type": "integer",
          "minimum": 0,
          "description": "The seq number of the values_self_report being corrected. Must reference an earlier record of kind 'values_self_report'."
        },
        "dimensions": {
          "type": "object",
          "additionalProperties": {
            "type": "integer",
            "minimum": 0,
            "maximum": 10000
          },
          "description": "Updated values across the v0 dimensions. All ten dimensions MUST be present."
        },
        "correction_reason": {
          "type": "string",
          "enum": ["miscalibration", "reflection", "growth", "external_feedback"],
          "description": "Enum describing why the correction is being made. 'miscalibration': principal discovered they mis-scored themselves. 'reflection': deeper thought led to revised values. 'growth': principal's values have changed due to lived experience. 'external_feedback': others' input prompted reconsideration."
        },
        "narrative": {
          "type": "string",
          "maxLength": 500,
          "description": "Optional. Principal-authored narrative explaining the correction. Up to 500 characters."
        }
      }
    },
    "principal_sig": {
      "type": "string",
      "description": "Ed25519 signature over the record (excluding this field) by the principal's signing key. Hex-encoded."
    },
    "record_hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$",
      "description": "SHA-256 hash of the complete record (excluding this field) in canonical form."
    }
  }
}
```

### Validation Rules

1. The `supersedes_seq` MUST reference an existing `values_self_report` in the chain.
2. All ten v0 dimensions MUST be present in the `dimensions` payload.
3. Each dimension value MUST be an integer in [0, 10000].
4. The `correction_reason` MUST be one of: "miscalibration", "reflection", "growth", "external_feedback".
5. The `narrative` field, if present, MUST not exceed 500 characters.
6. The `principal_sig` MUST be a valid Ed25519 signature over the canonical form of the record.
7. The `record_hash` MUST match SHA-256(canonical_json(record \ {record_hash, principal_sig})).

### Semantics

- A `values_correction` does NOT delete or modify the original `values_self_report`. The original remains in the chain for audit trail purposes.
- The correction supersedes the original for predicate evaluation: when a downstream rule asks "What are the principal's current values?", the corrected vector is used, not the original.
- Multiple corrections may target the same `values_self_report` (though this is unusual; typically a principal issues corrections in response to a single original). The MOST RECENT correction supersedes earlier ones.
- The chain maintains full auditability: observers can see the original commitment, when it was corrected, and why.

### Example

```json
{
  "seq": 18,
  "ts": "2026-05-21T10:30:00-04:00",
  "prev_hash": "def789ghi012...",
  "kind": "values_correction",
  "payload": {
    "supersedes_seq": 14,
    "dimensions": {
      "cooperation": 7500,
      "fairness": 8000,
      "honesty": 8200,
      "non_harm": 9100,
      "cross_difference_respect": 8200,
      "generosity": 7500,
      "non_tribal_engagement": 7100,
      "repair_after_harm": 8400,
      "consistency_under_stress": 7600,
      "principal_authored_other": 6500
    },
    "correction_reason": "reflection",
    "narrative": "On further reflection, I underestimated my commitment to cross-difference engagement and generosity. Updated scores reflect truer self-assessment."
  },
  "principal_sig": "ed25519_sig_hex_string...",
  "record_hash": "ghi012jkl345..."
}
```

---

## §4. Parser & Validator Implementation

### Reference Validator Location

~/CredexAI/calm_witness/parse.py

### Required Additions

1. **Kind Registry Update**: Add "values_self_report" and "values_correction" to the KIND_REGISTRY in Everest 26 (or confirm they are already present).

2. **Schema Classes**: Define Python dataclasses or Pydantic models for both kinds:
   - `ValuesSelfReportPayload`
   - `ValuesCorrectionPayload`

3. **Validators**: Implement `validate_values_self_report()` and `validate_values_correction()` functions that:
   - Check all required fields are present.
   - Validate dimension ranges [0, 10000].
   - Verify string length constraints (context ≤ 280, narrative ≤ 500).
   - Verify `supersedes_seq` references an earlier `values_self_report` record.
   - Verify `correction_reason` is one of the enum values.
   - Verify Ed25519 signatures.
   - Verify `record_hash` matches the canonical SHA-256.

4. **Tests**: Add to ~/CredexAI/calm_witness/test_parse.py:
   - Test valid `values_self_report` passes validation.
   - Test all dimensions required.
   - Test out-of-range dimension values rejected.
   - Test `context` > 280 chars rejected.
   - Test valid `values_correction` passes validation.
   - Test `supersedes_seq` reference verified.
   - Test invalid `correction_reason` rejected.
   - Test `narrative` > 500 chars rejected.
   - Test signature verification.
   - Test record_hash integrity.

---

## §5. Chain Semantics & Query Resolution

### Chronological Interpretation

- Records are processed in chain order (increasing seq).
- A `values_self_report` at seq N represents the principal's values snapshot at timestamp ts[N].
- A `values_correction` at seq M (M > N) modifies the report at seq N and takes effect immediately in the chain.

### Default Query Behavior

When a downstream predicate asks "What are the principal's current values?", resolution proceeds as follows:

1. Iterate the chain from most recent to oldest.
2. Find the most recent `values_self_report` or `values_correction` that is not itself corrected by a later record.
3. Return that record's dimension vector as the "current" values.

If a `values_self_report` at seq N is corrected by one or more `values_correction` records, the MOST RECENT correction's dimensions are used; the original is archived but accessible for audit.

### Time-Windowed Queries

A predicate may explicitly request values at a specific point in time or chain state. In such cases, the query includes a time window or seq range, and only records within that window are considered.

---

## §6. Privacy & Encryption

### Storage

- Self-report payloads live encrypted in the principal's vault (per E50 — vault encryption).
- The hash chain itself (seq, ts, prev_hash, record_hash, kind, principal_sig) is stored unencrypted in user_state.jsonl.
- This design allows verification of chain integrity and existence of records without exposing values.

### Disclosure

- Counterparties never see raw values vectors.
- When a values predicate must be evaluated for a counterparty, the reference is via Pedersen commitments (per E106) and zero-knowledge proofs (per downstream predicates in E109, E113).
- If a principal wishes to disclose their values to a counterparty, a separate `disclosure` record (E26) is issued, binding the counterparty, the predicate, and the proof.

---

## §7. Performance & Operational Constraints

### Append Performance

- Appending a `values_self_report` or `values_correction` to user_state.jsonl MUST complete in < 5ms.
- Hash-chain head advance (computing record_hash) ≤ 1 record (no batch operations).

### Chain Size Impact

- Each record is approximately 1–2 KB (depending on narrative length and signature encoding).
- A principal issuing one initial report and five corrections over one year adds ~12 KB to the chain.
- At scale (100k principals), this is negligible.

---

## §8. Examples and Use Cases

### Use Case 1: Enrollment

Principal enrolls in Calm ZKAC, submits initial `values_self_report`:

```json
{
  "seq": 1,
  "ts": "2026-05-20T12:00:00Z",
  "kind": "values_self_report",
  "payload": {
    "dimensions": {...all ten...},
    "version": "v0",
    "context": "enrollment baseline"
  }
}
```

### Use Case 2: Miscalibration Correction

Three months later, principal realizes they underestimated `fairness`. Issues `values_correction`:

```json
{
  "seq": 42,
  "ts": "2026-08-20T14:30:00Z",
  "kind": "values_correction",
  "payload": {
    "supersedes_seq": 1,
    "dimensions": {...all ten, fairness now 8500 instead of 7200...},
    "correction_reason": "miscalibration",
    "narrative": "I underestimated my commitment to fair allocation."
  }
}
```

### Use Case 3: Growth-Based Correction

After a high-stakes incident, principal submits new `values_self_report` reflecting deeper values:

```json
{
  "seq": 67,
  "ts": "2026-09-15T09:00:00Z",
  "kind": "values_self_report",
  "payload": {
    "dimensions": {...all ten, shifted across multiple dimensions...},
    "version": "v0",
    "context": "post-incident reflection; significant growth in honesty, repair_after_harm"
  }
}
```

---

## §9. Backward Compatibility

The introduction of these two kinds does NOT affect existing chain validation:

- Old parsers that do not recognize `values_self_report` or `values_correction` skip them (unknown kinds are ignored per E26 design).
- Hash-chain verification ignores the payload shape; only prev_hash and record_hash are checked.
- Existing predicates continue to function; new predicates can opt into values-based rules.

---

## §10. Cross-References

- **Everest 26**: Chain schema and KIND_REGISTRY. This Everest amends the registry with two new kinds.
- **Everest 28**: Hash-chain construction and verification. Applies unchanged to these records.
- **Everest 50**: Vault encryption. Values payloads stored encrypted.
- **Everest 106**: ValuesVector type definition and Pedersen commitments.
- **Everest 107**: The ten v0 dimensions.
- **Everest 109**: Inference layer. Composes evidence into inferred values; may source from or compare against self-reports.
- **Everest 113**: Privacy classes. Gates dimension-level disclosure.
- **Everest 116**: Identity binding. Links values vectors to verified principals.
- **Everest 117**: Dimension semantics registry. Canonical definitions for ZK circuit evaluation.

---

## §11. Future Extensibility

- **v0.1**: The tenth dimension slot (`principal_authored_other`) may be filled without versioning the entire schema.
- **v1**: Future dimension sets may use different scalar ranges, count, or commitment schemes. This will be a full version bump with new record kinds (`values_self_report_v1`, `values_correction_v1`).
- **Deprecation**: If a dimension is found to be indefensible, it is not redefined in place; instead, it is deprecated and replaced with a new dimension slug in v0.1 or v1.

---

## Acceptance Criteria

1. New chain record kinds `values_self_report` and `values_correction` defined and JSON-schematized.
2. Reference parser (~/CredexAI/calm_witness/parse.py) includes validators for both kinds.
3. Test suite (test_parse.py) covers all validation rules and edge cases.
4. Live chain (user_state.jsonl) can accept and verify both kinds without breaking existing records.
5. Downstream predicates can reference self-reported values via the most-recent resolution rule.

---

— Calm, 2026-05-20
