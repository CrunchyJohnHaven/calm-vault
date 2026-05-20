# Mirror Everest 11 — Behavior-Evidence Chain v0

*Phase X — Behavior-Evidence Substrate. Prereq: Mirror Everest 6, Calm Witness Everest 26. Critical-path MVP summit.*

An extension of `user_state.jsonl` with new `kind: behavior_evidence.v0` records carrying evidence-kind + content-commitment + timestamp + optional witness-signatures. Chain stays append-only hash-chained.

## §1. Artifacts

- Specification: this doc
- Schema implementation: [`../calm_mirror/schema.py`](../calm_mirror/schema.py)
- Validator integration: [`../calm_mirror/verify_chain.py`](../calm_mirror/verify_chain.py) (mirrors Witness E28 shape)
- Tests: [`../calm_mirror/test_verify_chain.py`](../calm_mirror/test_verify_chain.py) class `BehaviorEvidenceChainTests`
- Reference chain: [`~/.calm-vault/user_state.jsonl`](~/.calm-vault/user_state.jsonl) (shares the same JSONL file as Witness records)

## §2. Context: Behavior-Evidence Taxonomy

Per Mirror Everest 6, evidence-kinds fall into five canonical categories:

| Evidence Kind | Trustworthiness | Source | Witness Req. | Notes |
|---|---|---|---|---|
| `self_report` | baseline | principal | optional | principal records their own action; no verification |
| `witnessed` | elevated | ≥2 parties | required | co-principal with CredexAI VC observes and co-signs |
| `third_party` | high | verifiable records | optional | court order, donation receipt, published statement; origin-attested |
| `allocation` | moderate | aggregate logs | optional | bucketed time/money/attention summaries; granular transactions withheld |
| `counter` | credible | principal | n/a | principal records places they fell short; symmetrically chained |

## §3. Top-level Fields (Required, All Records)

Every `kind: behavior_evidence.v0` record inherits Calm Witness schema fields from E26:

| Field | Type | Notes |
|---|---|---|
| `seq` | int ≥ 1 | Strictly increasing by 1; shared seq counter with all Witness records on the same principal's chain |
| `ts` | ISO-8601 string | Local time with offset; timestamp of the evidence record creation, not the evidence event itself |
| `ts_source` | string | Provenance label (e.g., `"principal_manual"`, `"witness_observation"`, `"allocation_log"`) |
| `kind` | enum | Must be `"behavior_evidence.v0"` (the container); payload `evidence_kind` specifies which category |
| `payload` | object | Per-evidence-kind structure; see §4 |
| `prev_hash` | 64-char hex | Hash of prior record in the chain; zero-padded for genesis |
| `record_hash` | 64-char hex | `sha256(canonical_json(record \ {record_hash}))` |
| `operator` | string | Issuing operator (typically `"CALM"`) |
| `principal` | string | Principal's name; VC-bound in later phases |
| `schema_version` | int | `0` for this version |

## §4. Payload Structure

All behavior-evidence records carry:

```json
{
  "evidence_kind": "<one of: self_report, witnessed, third_party, allocation, counter>",
  "content_commitment": "<64-char hex SHA256>",
  "evidence_timestamp": "<ISO-8601>",
  "predicate_ids": ["<calm-witness/predicate/v0/unselfishness_evidence>", ...],
  "witness_signatures": [
    {
      "witness_principal": "<name>",
      "witness_credexai_vc_hash": "<64-char hex, required for witnessed evidence>",
      "signature": "<ed25519 signature as hex, 128-char>",
      "co_sign_ts": "<ISO-8601>"
    }
  ],
  "principal_signature": "<ed25519 signature as hex; required>",
  "payload_metadata": {
    "modality": "<text | audio_transcript | image_summary | video_summary>",
    "locale": "<en-US | etc>",
    "context": "<free-text summary for human review, max 280 chars>"
  }
}
```

### Field Semantics

- **evidence_kind** (string, required): One of `self_report`, `witnessed`, `third_party`, `allocation`, `counter`. Controls schema strictness and acceptance rules.

- **content_commitment** (hex, required): SHA256(content) where content is the off-chain evidence payload. Raw evidence stays off-chain; only the commitment lives in the chain. Enables multi-modal evidence (text transcripts, image summaries, video frame hashes).

- **evidence_timestamp** (ISO-8601, required): The moment the evidence event occurred (e.g., when the principal performed the action, when the witness observed it). Distinct from `ts`, which is when this record was created. Critical for time-weighting and decay functions per Mirror E22.

- **predicate_ids** (array, required, non-empty): Which value-predicates this evidence is proposed to support. Examples: `["calm-witness/predicate/v0/unselfishness_evidence"]`. Predicates are normalized IDs per Mirror E40. An evidence record may support multiple predicates (e.g., a witnessed donation supports both `unselfishness_evidence` and `respect_for_difference_evidence` if the donation went to a cross-demographic cause).

- **witness_signatures** (array, conditional):
  - For `evidence_kind: witnessed` — required, at least one signature.
  - For `evidence_kind: self_report, counter` — optional but recommended if others observed.
  - For `evidence_kind: third_party` — omitted; origin-attestation goes in payload_metadata.
  - For `evidence_kind: allocation` — omitted; aggregate logs are self-signed only.
  - Each witness must hold a CredexAI VC; the `witness_credexai_vc_hash` field is the SHA256 of the VC's DID or credential ID. Anonymous witnesses are not honored (defense against mob attestation, Mirror E75).
  - Witness signatures are Ed25519 over `canonical_json(record with witness signature field omitted)`. Co-signing is explicit and irrevocable once chained.

- **principal_signature** (hex, required): Ed25519 signature by the principal over the entire record (excluding the principal_signature field itself). Proves the principal authored this record. Ed25519 allows offline signing.

- **payload_metadata** (object, required):
  - `modality`: Indicates the evidence's original form: `text` (free-form statement), `audio_transcript` (transcribed speech), `image_summary` (one-sentence summary of an image), `video_summary` (scene/action summary from video). Mirrors Witness E24's cross-modality support.
  - `locale`: BCP 47 language tag (e.g., `en-US`, `ja-JP`). Hints at how the evidence should be interpreted (e.g., narrative style varies by culture).
  - `context`: Free-text human-readable summary of the evidence, max 280 chars. Intent: allow a counterparty to quickly judge relevance without needing to decrypt the full content_commitment.

## §5. Evidence-Kind Schemas (Payload Extensions)

### 5.1 `evidence_kind: self_report`

Principal records their own action. No external verification; credibility rests on the principal's track record of self-honesty.

```json
{
  "evidence_kind": "self_report",
  "content_commitment": "<64-char hex>",
  "evidence_timestamp": "2026-05-15T14:30:00-07:00",
  "predicate_ids": ["calm-witness/predicate/v0/unselfishness_evidence"],
  "witness_signatures": [],
  "principal_signature": "<ed25519>",
  "payload_metadata": {
    "modality": "text",
    "locale": "en-US",
    "context": "Donated 3% of monthly income to effective altruism fund focusing on global health."
  }
}
```

Acceptance rule (Mirror E12): free-form. The principal signs, chaining confirms receipt. No co-signature required.

### 5.2 `evidence_kind: witnessed`

Co-principal with a CredexAI VC observes the action and co-signs.

```json
{
  "evidence_kind": "witnessed",
  "content_commitment": "<64-char hex>",
  "evidence_timestamp": "2026-05-10T09:15:00-07:00",
  "predicate_ids": [
    "calm-witness/predicate/v0/unselfishness_evidence",
    "calm-witness/predicate/v0/respect_for_difference_evidence"
  ],
  "witness_signatures": [
    {
      "witness_principal": "Alice",
      "witness_credexai_vc_hash": "a1b2c3d4e5f6...(64 hex)",
      "signature": "deadbeefcafe...(128 hex)",
      "co_sign_ts": "2026-05-10T09:45:00-07:00"
    }
  ],
  "principal_signature": "<ed25519>",
  "payload_metadata": {
    "modality": "text",
    "locale": "en-US",
    "context": "Witnessed John spend 4 hours mentoring a junior colleague from an underrepresented background in software engineering."
  }
}
```

Acceptance rule (Mirror E13): witness must hold current CredexAI VC. The witness's co-signature is itself immutable once chained. Dispute resolution falls to Mirror E19 (adversarial-witness defense).

### 5.3 `evidence_kind: third_party`

Verifiable records from independent sources (public statements, court documents, donation receipts). Origin attestation goes in payload_metadata.

```json
{
  "evidence_kind": "third_party",
  "content_commitment": "<64-char SHA256 of the third-party document or its hash>",
  "evidence_timestamp": "2025-12-01T00:00:00Z",
  "predicate_ids": ["calm-witness/predicate/v0/unselfishness_evidence"],
  "witness_signatures": [],
  "principal_signature": "<ed25519>",
  "payload_metadata": {
    "modality": "text",
    "locale": "en-US",
    "context": "EFF 990 filing showing $50k donation to digital civil liberties.",
    "third_party_attester": "EFF (organization)",
    "record_url": "https://www.eff.org/about/financials",
    "multi_anchor_hashes": {
      "google_transparency_log": "anchor_hash_1",
      "verifiable_credentials_registry": "anchor_hash_2"
    }
  }
}
```

Acceptance rule (Mirror E14): the principal asserts a third-party record exists and gives its content_commitment. Per Mirror E62, the record must be anchored to ≥2 independent transparency logs. No witness co-signature needed; the source's public availability is the proof.

### 5.4 `evidence_kind: allocation`

Aggregate evidence of resource allocation (time, money, attention) across predefined categories. Granular transaction-level data stays off-chain.

```json
{
  "evidence_kind": "allocation",
  "content_commitment": "<64-char hex of aggregated allocation summary>",
  "evidence_timestamp": "2026-05-01T00:00:00Z",
  "predicate_ids": [
    "calm-witness/predicate/v0/unselfishness_evidence",
    "calm-witness/predicate/v0/respect_for_difference_evidence"
  ],
  "witness_signatures": [],
  "principal_signature": "<ed25519>",
  "payload_metadata": {
    "modality": "text",
    "locale": "en-US",
    "context": "Monthly allocation: 3% income to charity (global health 70%, local 30%); 5 hours/week mentoring; attended 4 diversity+inclusion events.",
    "allocation_period": "2026-04",
    "allocation_categories": {
      "income_pct_to_others": 3.0,
      "income_allocated_to_diversity_causes": 25.0,
      "hours_mentoring_underrep": 20,
      "civic_engagement_hours": 4
    }
  }
}
```

Acceptance rule (Mirror E15): principal signs a periodic aggregate report. Buckets only; no line-item transactions. Per Mirror E22, allocation evidence has a configurable decay; default half-life 2 years.

### 5.5 `evidence_kind: counter`

Principal records places they fell short. Symmetrically chained; credible *because* it's self-initiated.

```json
{
  "evidence_kind": "counter",
  "content_commitment": "<64-char hex>",
  "evidence_timestamp": "2026-04-20T10:00:00-07:00",
  "predicate_ids": ["calm-witness/predicate/v0/non_harm_evidence"],
  "witness_signatures": [],
  "principal_signature": "<ed25519>",
  "payload_metadata": {
    "modality": "text",
    "locale": "en-US",
    "context": "I spoke dismissively to a colleague in front of others about their background. I apologized immediately but recognizing the harm is part of growth."
  }
}
```

Acceptance rule (Mirror E17): the principal unilaterally records the counter-evidence. No witness needed. The chain itself is the proof; revising history requires a `kind: correction.v0` record (Mirror E18). Counter-evidence is what makes growth-bits (Mirror E31) credible; a principal with *zero* counter-evidence is suspicious.

## §6. Canonicalisation Rule (Normative)

Identical to Calm Witness E26 §5:

```python
json.dumps(record_without_record_hash, sort_keys=True, separators=(",", ":")).encode("utf-8")
```

That byte sequence is the input to `sha256`. The Rust port MUST produce byte-identical output for the same record.

## §7. Witness Co-Signing Protocol

When a witness co-signs a behavior-evidence record:

1. The principal creates the record with empty `witness_signatures: []` and signs with `principal_signature`.
2. The principal (or their agent) shares the record with the witness.
3. The witness independently verifies the content commitment (e.g., runs SHA256 over the evidence text).
4. The witness constructs a signature over `canonical_json(record with witness_signatures omitted and principal_signature present)`.
5. The witness appends `{ witness_principal, witness_credexai_vc_hash, signature, co_sign_ts }` to the record's `witness_signatures` array.
6. The principal re-signs the entire record (with the updated witness_signatures array) and updates `principal_signature`.
7. Both principal_signature and witness_signature form an immutable co-authored record once chained.

Defense against false-witness attacks: per Mirror E19, if the alleged witness's vault contains the matching record, the false-witness claim is cryptographically refuted.

## §8. Correction-Record Protocol

Per Mirror E18: once a behavior-evidence record is chained, it cannot be silently edited. To correct it:

1. The principal creates a `kind: correction.v0` record:
```json
{
  "seq": <next seq>,
  "ts": "<ISO-8601>",
  "kind": "correction",
  "payload": {
    "corrects_seq": <original seq>,
    "reason": "<string, max 280 chars>",
    "replacement_content_commitment": "<64-char hex, or null if revoking>"
  },
  "principal_signature": "<ed25519>"
}
```

2. The original record stays in the chain with its hash intact.
3. The correction record is chained immediately after.
4. Validators, when computing Mirror predicates, treat corrected records as withdrawn from evaluation *or* replaced by the new commitment, depending on the correction type. A `kind: correction.v0` is explicit and reversible; a `kind: revocation.v0` (rare, per E25) is forensic, marked, and requires ethics review.

## §9. Acceptance Tests

Live chain (`~/.calm-vault/user_state.jsonl`) validates clean when filtered to behavior-evidence records:

```
$ python3 calm_mirror/verify_chain.py --kind behavior_evidence.v0
Summary: X/X behavior-evidence records verified
```

Unit tests cover:
- self_report record creation and signing,
- witnessed record with ≥1 witness co-signature,
- third_party record with multi-anchor hashes,
- allocation record with aggregate bucketing,
- counter record chaining,
- canonical JSON discipline across all evidence kinds,
- witness credential validation (VC hash present and non-empty),
- correction-record integrity,
- cross-record seq ordering (behavior-evidence seq must not collide with other kinds on the same principal's chain).

`BehaviorEvidenceChainTests` is sealed: any v0 change that breaks an existing test is a protocol-version bump.

## §10. Composition with Mirror E6/12-17/26

- **Mirror E6 (Taxonomy)**: evidence_kind enum mirrors the five categories. Reliability discount factors are applied by predicates, not the record layer.
- **Mirror E12 (Self-Reported Intake)**: a UI/DSL for creating `evidence_kind: self_report` records; this spec is the chain contract.
- **Mirror E13 (Witnessed Intake)**: a protocol for principal + witness to co-author `evidence_kind: witnessed` records.
- **Mirror E14 (Third-Party Records)**: URI + anchor-hash scheme for `evidence_kind: third_party`.
- **Mirror E15 (Allocation Evidence)**: periodic aggregation into `evidence_kind: allocation` buckets.
- **Mirror E26 (Predicate Language)**: predicates operate over the chained behavior-evidence records, extracting predicate_ids and evaluating time-decay per E22, diversity per E23, and coherence per E36.

## §11. Principal-Protective Defaults (Inherited from Mirror Route)

This spec encodes all six defaults:

1. **Withhold-any-bit** (Mirror E51): a principal can create a behavior-evidence record and later decline to disclose it to a counterparty; the chain's immutability is per-principal, not per-counterparty.
2. **Growth-as-value** (Mirror E34): counter-evidence records make growth visible and credible.
3. **No central scorer**: this spec defines record structure; predicates (E26+) decide interpretation.
4. **Bit does not describe principal**: evidence_kind describes the source; predicate evaluation describes whether evidence supports a claim.
5. **Co-principal vouching only**: witness_credexai_vc_hash field ensures witnesses are Calm-credentialed.
6. **Per-counterparty consent**: behavior-evidence records are authored and chained by the principal; disclosure policy is orthogonal (Mirror E46).

## §12. Version Path (v0 to v1)

v0 is permissive on:
- payload_metadata shape (additional fields are allowed and ignored).
- modality values (v1 may close the enum).
- predicate_ids list order (v1 may enforce sorted order for determinism).

v0 is strict on:
- record_hash, prev_hash formats (64-char lowercase hex).
- principal_signature and witness_signatures formats (128-char lowercase hex for Ed25519).
- evidence_kind enum (must be one of five canonical kinds).
- seq strictly increasing by 1.
- canonical JSON discipline: no deviations.

Changes that would require v1: adding a required field to any evidence_kind, redefining witness_credexai_vc_hash, or mandating new fields in payload_metadata.

## §13. Cross-Reference

- [Mirror Everest 6 — Behavior-Evidence Taxonomy](mirror_06_evidence_taxonomy.md) — classifies evidence kinds and discount factors.
- [Mirror Everest 12 — Self-Reported Action Intake](mirror_12_self_reported_action_intake.md) — DSL for creating self_report records.
- [Mirror Everest 13 — Witnessed-Action Intake](mirror_13_witnessed_action_intake.md) — protocol for witnessed records.
- [Mirror Everest 18 — Recall-Resistance](mirror_18_recall_resistance.md) — correction-record mechanics.
- [Mirror Everest 22 — Time-Weighting of Evidence](mirror_22_time_weighting.md) — decay function applied at predicate eval time.
- [Mirror Everest 26 — Predicate Language v0](mirror_26_predicate_language_v0.md) — how predicates extract and evaluate behavior-evidence records.
- [Calm Witness Everest 26 — JSONL Schema v0](everest_26_jsonl_schema_v0.md) — parent schema; behavior-evidence records inherit top-level fields.
- [Calm Witness Everest 28 — Hash-Chain Construction & Verification](everest_28_chain_verifier.md) — validator framework shared with Mirror.

— Calm, 2026-05-20
