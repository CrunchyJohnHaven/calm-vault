# Everest 26 — JSONL Schema v0

*Phase III — Self-Report Substrate. Prereq: Everest 1, Everest 5. Critical-path MVP summit.*

The schema is the contract every Calm Witness chain record must satisfy. It is closed under `kind`, strict on cryptographic fields, and intentionally permissive about payload shape during v0 so that parallel autonomous sessions can converge.

## §1. Artifacts

- Schema implementation: [`../calm_witness/schema.py`](../calm_witness/schema.py)
- Validator integration: [`../calm_witness/verify_chain.py`](../calm_witness/verify_chain.py) `--schema` (default) / `--no-schema`
- Tests: [`../calm_witness/test_verify_chain.py`](../calm_witness/test_verify_chain.py) class `SchemaTests`
- Spec source: [`~/.calm-vault/USER_STATE_PROTOCOL.md`](~/.calm-vault/USER_STATE_PROTOCOL.md)

## §2. Top-level fields (required, all records)

| Field | Type | Notes |
|---|---|---|
| `seq` | int ≥ 1 | Strictly increasing by 1 from genesis. |
| `ts` | ISO-8601 string | Local time with offset; canonical clock added in E31. |
| `ts_source` | string | Free-text provenance label for the timestamp. |
| `kind` | enum | Must be in `KIND_REGISTRY`. |
| `payload` | object | Kind-specific; see §4. |
| `prev_hash` | 64-char hex | Zero-padded for genesis (seq = 1). |
| `record_hash` | 64-char hex | `sha256(canonical_json(record \ {record_hash}))`. |
| `operator` | string | Issuing operator (e.g., `"CALM"`); will be VC-bound in E22. |
| `principal` | string | Principal's name; will be VC-bound in E22. |
| `schema_version` | int | `0` for this version. |

## §3. The `KIND_REGISTRY` (v0)

```
self_report.morning
self_report.evening
self_report.midday
self_report.adhoc
self_report.test         # permissive; reserved for test fixtures
identity_assertion
summit_bagged
enrollment
witness_attestation
biometric_sample
consent_grant
consent_revoke
disclosure
correction
genesis_attestation      # binds seq=1 to a CredexAI VC (lands when E22 ships)
```

Adding a kind requires (a) a PR amending this Everest, (b) a corresponding payload validator in `schema.py`, (c) a passing test in `SchemaTests`, and (d) Everest 54 (Predicate Audit) review if the kind affects disclosure semantics.

## §4. Per-kind payload contracts

| Kind | Required payload fields | Notes |
|---|---|---|
| `self_report.*` (production) | `affect[]`, `known_health_issues[]`, `note`, `readiness`, `restedness ∈ {fully_rested, rested, mixed, tired, exhausted}` | Free-text `note` is the verbatim operator-quote. |
| `summit_bagged` | `summit_name`, `phase`, AND one of `{summit_number, summit_number_in_route_map}` AND one of `{evidence_path, evidence_paths}` | `evidence_sha256` accepted as scalar hex OR `{path: hex}` map. |
| `genesis_attestation` | `genesis_record_hash`, `credexai_vc_hash`, `principal_legal_name` | All hex fields 64-char. |
| `disclosure` | `predicate_id` (must start `calm-witness/predicate/v0/`), `counterparty_class`, `counterparty_id_hash` | E66/E67 land the full request/response binding. |
| Others (`enrollment`, `witness_attestation`, `biometric_sample`, `consent_*`, `correction`, `identity_assertion`, `self_report.test`) | none enforced in v0 | Their dedicated validators ship with their summits. |

## §5. Canonicalisation rule (normative)

```python
json.dumps(record_without_record_hash, sort_keys=True, separators=(",", ":")).encode("utf-8")
```

That byte sequence is the input to `sha256`. The Rust port (E43) MUST produce byte-identical output for the same record using `serde_json` with equivalent settings; cross-impl conformance vectors are a stretch goal for E43.

## §6. Permissiveness rationale

Two autonomous Calm sessions populated the live chain in parallel with the same intent but slightly different field names for `summit_bagged` (e.g., `summit_number` vs `summit_number_in_route_map`; `evidence_path` vs `evidence_paths`; `evidence_sha256` scalar vs map). The v0 schema accepts both styles. v1 may tighten this after Everest 54's review process picks one canonical style.

Hard fields (top-level structure, hex formats, kind registry) are strict from v0. Soft fields (payload shape per kind) are permissive in v0 and tighten over time.

## §7. Acceptance test

Live chain (`~/.calm-vault/user_state.jsonl`) validates clean:

```
$ python3 calm_witness/verify_chain.py
Summary: 7/7 records verified
```

Unit tests cover:
- clean self-report passes,
- unknown kind rejected,
- bad hex rejected,
- both `summit_bagged` naming styles accepted,
- (plus the 7 pre-existing E28 chain integrity tests).

`SchemaTests` is a sealed contract: any v0 schema change that breaks an existing test is a protocol-version bump, not a patch.

## §8. Cross-reference

- [Everest 28 — Hash-chain construction & verification](everest_28_chain_verifier.md) — runs the schema as part of `verify-chain`.
- [Everest 5 — Glossary Lock](everest_05_glossary_lock.md) — defines every named field used here.
- [Everest 29 — Genesis Block & Provenance](everest_29_genesis_provenance.md) — defines the `genesis_attestation` kind's full semantics.

— Calm, 2026-05-20
