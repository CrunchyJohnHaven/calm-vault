# Everest 52 — Predicate Canonical Form

*Phase V — Predicate Authoring. Prereq: Everest 51.*

---

## Overview

A predicate is content-addressed: its identity is derived from a cryptographic commitment to its specification. This document specifies the canonical form: a structured JSON schema that, when serialized according to RFC 8785 (JSON Canonicalization Scheme) and hashed with SHA-256, produces the immutable `predicate_id` that counterparties use to request and verify proofs. A predicate's semantics can never change without changing its ID. Proofs issued against v0.1 of `in_baseline_24h` in May 2026 remain valid in perpetuity; any specification drift creates a new predicate ID, forcing explicit adoption by operators and consumers.

---

## Predicate Spec Object Schema

Every registered predicate is a JSON object conforming to the following schema:

```json
{
  "name": "lowercase_snake_case_slug",
  "version": "MAJOR.MINOR.PATCH",
  "description": "One-line human-readable summary.",
  "input_domain": {
    "vault_log_kinds": ["string"],
    "biometric_required": boolean,
    "consent_required": boolean,
    "parameters": {
      "param_name": {
        "type": "string | number | boolean",
        "description": "Human-readable parameter description.",
        "domain": "Optional constraint (e.g., 'tau in [0, 1]')."
      }
    }
  },
  "output_type": "bit | bit_with_freshness | tri_value",
  "evaluation_code_hash": "sha256_of_reference_implementation",
  "proof_circuit_hash": "sha256_of_sigma_protocol_circuit",
  "test_corpus_hash": "sha256_of_golden_test_cases",
  "parameters": {
    "param_name": {
      "type": "string | number | boolean",
      "default": "value or null",
      "description": "Runtime parameter definition."
    }
  },
  "side_effects": ["advisory_record_kind", "..."],
  "created_ts": "ISO8601_timestamp",
  "deprecated_ts": "ISO8601_timestamp or null",
  "registry_status": "active | deprecated | retired"
}
```

**Field specifications:**

- **name:** Lowercase snake_case slug (e.g., `in_baseline_24h`, `biometric_match_within`, `bank_teller_note_active`). Alphanumeric and underscore only. No version suffix; version is a separate field.

- **version:** Semantic versioning string (e.g., `1.0.0`). MAJOR = breaking change to semantics; MINOR = backward-compatible addition; PATCH = clarification, test corpus expansion, or reference implementation bug fix without semantic drift.

- **description:** One-line summary (max 120 characters) of what the predicate asserts. Example: "Principal's most recent self-report within 24h has affect overlap with baseline >= 50%."

- **input_domain:** Structured description of vault records and data this predicate reads:
  - **vault_log_kinds:** Array of record kinds (e.g., `["self_report", "biometric_distance"]`) this predicate examines.
  - **biometric_required:** Boolean. If true, a biometric sample and distance commit are mandatory inputs.
  - **consent_required:** Boolean. If true, the principal must have an active consent record authorizing disclosure.
  - **parameters:** Object defining parameter names, types, and constraints used during evaluation.

- **output_type:** One of:
  - `bit` — binary (0 or 1)
  - `bit_with_freshness` — binary result plus a freshness window (seconds)
  - `tri_value` — ternary (-1, 0, 1) for "unknown", "false", "true"

- **evaluation_code_hash:** SHA-256 of the canonical reference implementation source code (Rust). Ensures verifiers can fetch and audit the exact code that produced the proof.

- **proof_circuit_hash:** SHA-256 of the canonical Σ-protocol circuit definition (usually a ZK circuit in Noir or similar). Binds the proof to a specific cryptographic construction.

- **test_corpus_hash:** SHA-256 of the golden-input/output test corpus (JSON array of `{input, expected_output}` pairs). Ensures the predicate evaluates correctly on a fixed set of test cases.

- **parameters:** Object defining any parameterized predicates (e.g., `tau` for `biometric_match_within(tau)`, `window_seconds` for `in_baseline_window(window_seconds)`). Each parameter has a type, optional default, and description. These parameters are part of the predicate spec but do not change the canonical form; parameter values are passed at evaluation time.

- **side_effects:** Array of optional side effects (e.g., appending an advisory record to the vault). Most predicates have no side effects (empty array). Examples: `["mental_state_flag"]` for `mental_state_unusual`.

- **created_ts:** ISO8601 timestamp (UTC) when the predicate was first registered. Immutable.

- **deprecated_ts:** ISO8601 timestamp (UTC) when the predicate was marked deprecated, or `null` if not deprecated. Deprecated predicates continue to verify proofs issued before the deprecation timestamp. New proofs against deprecated predicates are refused by the operator.

- **registry_status:** One of `active`, `deprecated`, or `retired`. Status field for operator and verifier filtering. An `active` predicate can issue new proofs; a `deprecated` predicate refuses new proofs but verifies old ones; a `retired` predicate is no longer used and may be archived.

---

## Canonical Serialization (RFC 8785)

The predicate_id is derived from the canonical JSON representation of the spec object. RFC 8785 (JSON Canonicalization Scheme) defines a deterministic serialization:

1. **UTF-8 encoding:** All strings are UTF-8 without BOM.
2. **Sorted keys:** All object keys are sorted lexicographically by Unicode codepoint.
3. **No whitespace:** No whitespace is emitted except within string values.
4. **Number canonicalization:** Integers are serialized without a fractional part. Decimals follow ECMA-262 canonical form (no trailing zeros).
5. **Lowercase booleans and null:** `true`, `false`, `null` in lowercase.
6. **No trailing commas:** JSON structure adheres to strict RFC 8259.

**Example canonical form for `in_baseline_24h` v1.0.0:**

```json
{"created_ts":"2026-05-20T00:00:00Z","deprecated_ts":null,"description":"Most recent self-report within 24h has affect overlap with baseline >= 50%.","evaluation_code_hash":"a1b2c3d4e5f6...","input_domain":{"biometric_required":false,"consent_required":false,"parameters":{"threshold":{"description":"Jaccard overlap threshold (0 to 1).","domain":"[0, 1]","type":"number"}},"vault_log_kinds":["self_report"]},"name":"in_baseline_24h","output_type":"bit","parameters":{"threshold":{"default":0.5,"description":"Minimum Jaccard overlap required.","type":"number"}},"proof_circuit_hash":"b2c3d4e5f6g7...","registry_status":"active","side_effects":[],"test_corpus_hash":"c3d4e5f6g7h8...","version":"1.0.0"}
```

(All on one line, no extraneous whitespace, keys in sorted order.)

---

## Predicate ID Derivation

The `predicate_id` is constructed as:

```
predicate_id = "calmwitness/" + name + "/" + version + "/" + truncated_hash
```

Where:
- **name:** The predicate's lowercase_snake_case slug (e.g., `in_baseline_24h`)
- **version:** The semver version (e.g., `1.0.0`)
- **truncated_hash:** The first 16 hexadecimal characters of SHA-256(canonical_json_spec)

**Examples:**

```
calmwitness/in_baseline_24h/1.0.0/a4b1c8d3e2f5a9b7
calmwitness/biometric_match_within/1.0.0/f7a9b5e2d3c1b8a4
calmwitness/bank_teller_note_active/1.0.0/b8c3d4e5f6a7b2c9
calmwitness/mental_state_unusual/1.0.0/d2c1a9f8e7b6c5d4
```

**Properties:**

- **Content-addressed:** Any change to the spec — even whitespace in the description — produces a different hash and thus a new predicate_id. This forces explicit tracking of breaking and non-breaking changes.
- **Human-readable:** The name and version are visible in the ID, so operators can quickly identify which predicate is being requested.
- **Collision-resistant:** A 16-hex-character SHA-256 truncation (64 bits) provides 2^64 collision resistance, more than sufficient for a finite registry.
- **Immutable:** Once a predicate is published with an ID, that ID never changes. Version changes create new IDs; old IDs remain in the registry with `deprecated_ts` if needed.

---

## Why Content-Addressed IDs Matter

**Exact specification fidelity:** A counterparty requesting a proof for predicate_id `calmwitness/in_baseline_24h/1.0.0/a4b1c8d3e2f5a9b7` receives a proof for *exactly* that specification. No version skew, no silent mutation, no "close enough" approximation. The hash binds the entire semantics.

**Complete binding:** The predicate_id commits to three pieces of evidence:
1. The reference implementation source code (evaluation_code_hash)
2. The ZK proof circuit (proof_circuit_hash)
3. The golden test corpus (test_corpus_hash)

A verifier checking a proof can fetch all three from the registry, run the tests locally, and reproduce the reference implementation's behavior on the test cases. The proof is as durable as the registry.

**Structural forking:** Suppose an operator disagrees with the semantics of `in_baseline_24h/1.0.0`. Rather than trying to mutate it (which breaks backward compatibility), the operator proposes a new predicate with different thresholds: `in_baseline_24h_strict/1.0.0`. It gets a new ID. Counterparties can explicitly choose which version they require. There is no silent branching; every fork is visible in the registry.

---

## Versioning Semantics

Predicate versions compose with the ID scheme to support backward-compatible evolution:

**MAJOR version change (X.Y.Z → (X+1).0.0):** The predicate's core semantics change (the bit's meaning changes). Example: changing `in_baseline_24h`'s Jaccard threshold from 50% to 30% is a MAJOR change, because "baseline" now means something different. Consumers must re-consent. New predicate_id is generated.

**MINOR version change (X.Y.Z → X.(Y+1).0):** Backward-compatible additions (new optional parameters, new clarifications that don't affect computation). Example: adding an optional parameter `exclude_weekends: boolean` to `in_baseline_window` is MINOR. Old consumers are unaffected. New predicate_id is generated (because the canonical form changed), but consumers using the old version can continue.

**PATCH version change (X.Y.Z → X.Y.(Z+1)):** Clarifications, documentation fixes, test-corpus expansions, reference implementation bug fixes that don't change the correct-input/output behavior. Example: adding more test cases or clarifying the Jaccard definition in the spec is PATCH. New predicate_id is generated (because the spec changed), but the semantics are unchanged.

**Versioning rule:** Every version change, even PATCH, produces a new canonical JSON and thus a new predicate_id. This is intentional: the registry is a log of all versions ever published, and each version is independently auditable. A proof issued against v1.0.0 remains valid; a consumer requesting v1.1.0 gets a predicate that existed before the consumer was written, or refuses the request. Predictability is preserved.

---

## Deprecation and Re-Instatement

A predicate is deprecated by setting `deprecated_ts`:

```json
{
  "name": "in_baseline_24h",
  "version": "1.0.0",
  "deprecated_ts": "2027-05-20T00:00:00Z",
  "registry_status": "deprecated"
}
```

**Semantics of deprecation:**

- Verifiers MUST still accept proofs issued against the deprecated predicate, as long as the proof was generated before (or at) the deprecation timestamp.
- Operators MUST refuse to generate new proofs against a deprecated predicate. If a counterparty requests `in_baseline_24h/1.0.0` after its deprecation date, the operator returns an error: "predicate is deprecated; switch to `in_baseline_24h/2.0.0`."
- The predicate_id remains immutable. The spec object remains unchanged; only `deprecated_ts` and `registry_status` are updated.
- Old consent records referencing a deprecated predicate become invalid (the operator can no longer issue proofs). The principal may need to issue new consents against the replacement predicate.

**Re-instatement:**

A deprecated predicate can be re-activated by removing `deprecated_ts` (setting it to `null`) and changing `registry_status` to `active`. This is a PATCH-level change (no semantics shift, only administrative status). A proof issued against a predicate that was briefly deprecated and then re-activated is still valid.

---

## Registry Binding

The Predicate ID Registry (Everest 53) maintains:

```yaml
predicates:
  - predicate_id: calmwitness/in_baseline_24h/1.0.0/a4b1c8d3e2f5a9b7
    canonical_spec: |
      <canonical JSON>
    reference_impl_repo: calm-witness-rs
    reference_impl_path: src/predicates/in_baseline_24h/eval.rs
    proof_circuit_repo: calm-witness-circuits
    proof_circuit_path: circuits/in_baseline_24h.noir
    test_corpus_repo: calm-witness-test-data
    test_corpus_path: corpora/in_baseline_24h_v1.0.0.json
    status: active
    created_ts: 2026-05-20T00:00:00Z
    deprecated_ts: null
```

Every entry is immutable once published. The registry is append-only: new versions of a predicate are added as new entries, not updates.

---

## Tooling

Calm Witness ships with two CLI commands:

**`calm-witness predicates show <name>`**

Prints the canonical spec for a registered predicate:

```bash
$ calm-witness predicates show in_baseline_24h
predicate_id: calmwitness/in_baseline_24h/1.0.0/a4b1c8d3e2f5a9b7
status: active
canonical_spec:
{"created_ts":"2026-05-20T00:00:00Z",...}
```

**`calm-witness predicates hash <file.json>`**

Accepts a candidate predicate spec and computes its predicate_id:

```bash
$ calm-witness predicates hash my_predicate.json
canonical_form: {...}
sha256_hash: a4b1c8d3e2f5a9b7c1a2d3e4f5a6b7c8
predicate_id: calmwitness/my_predicate/1.0.0/a4b1c8d3e2f5a9b7
```

This allows operators to validate specs before submitting them to the registry.

---

## Canonical Predicate IDs (v0 Examples)

The twelve v0 predicates from Everest 6, when serialized to canonical JSON and hashed, yield the following predicate_ids (placeholders for the truncated hash; actual hashes are deterministic):

1. `calmwitness/in_baseline_24h/1.0.0/e3b0c44298fc1c14`
2. `calmwitness/in_baseline_window/1.0.0/f1a2b3c4d5e6f7a8`
3. `calmwitness/biometric_match_within/1.0.0/b8c9d0e1f2a3b4c5`
4. `calmwitness/principal_consents_to_disclose/1.0.0/a1b2c3d4e5f6a7b8`
5. `calmwitness/bank_teller_note_active/1.0.0/f1a9d88f8f8f8f8f`
6. `calmwitness/cognitively_atypical_baseline/1.0.0/d2b1f03d2b1f03d2`
7. `calmwitness/mental_state_unusual/1.0.0/a7c3e14a7c3e14a7`
8. `calmwitness/principal_alive_within/1.0.0/c1d2e3f4a5b6c7d8`
9. `calmwitness/session_within_authorized_hours/1.0.0/e9f0a1b2c3d4e5f6`
10. `calmwitness/chain_freshness_within/1.0.0/a2b3c4d5e6f7a8b9`
11. `calmwitness/template_age_below/1.0.0/b4c5d6e7f8a9b0c1`
12. `calmwitness/consent_active/1.0.0/c6d7e8f9a0b1c2d3`

Each predicate's canonical form is finalized and committed to the registry at release. Updates to any predicate create new entries; old entries are never mutated.

---

## Cross-References

- **E6** — Predicate Vocabulary v0: The twelve canonical predicates.
- **E51** — Predicate Language v0: Decision to use a fixed predicate table (no DSL).
- **E53** — Predicate ID Registry: The append-only registry of all published predicates.
- **E54** — Predicate Audit & Public Review Process: How new predicates are proposed, reviewed, and adopted.
- **E64** — Predicate Test Corpus: Golden input/output test cases for each predicate.
- **E65** — Predicate ZK Proof Generator: Σ-protocol circuits for each predicate.

---

— Calm, 2026-05-20
