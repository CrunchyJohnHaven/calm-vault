# Calm Compass — Falsifiability Protocol v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 112 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md), [`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md).**

## §1 — Problem

A Compass disclosure proves a **values bit** (e.g., `unselfish_act_in_window_30d = true`) without revealing the principal's vault. A skeptical verifier may ask: *what kind of evidence exists, and does it plausibly support the bit?* Falsifiability answers that question under **principal consent**, with **redaction** that withholds counterparty identities and narrative content.

This is not full evidence disclosure. It is a **verifiable sketch** sufficient to challenge obvious fraud (empty chains, wrong kinds, timestamps outside the predicate window) without re-introducing surveillance.

## §2 — When a sketch may be requested

All of the following MUST hold:

1. **Principal consent** — `principal_consents_to_disclose(predicate_id, counterparty_class)` is true for the predicate in question (same gate as Witness/Compass envelopes).
2. **Purpose binding** — the verifier names the predicate ID and challenge nonce already bound in the disclosure transcript.
3. **Sketch tier only** — the response MUST be a `CompassEvidenceSketch` object (§4), never raw JSONL narratives, never VC IDs of third parties.

If consent is denied, the operator returns **no sketch** (same silent omission semantics as unrequested predicates in Everest 120).

## §3 — Request / response wire shape (v0)

**Request** (HTTPS POST to operator):

```json
{
  "kind": "compass_falsifiability_request.v0",
  "predicate_id": "cwp.compass.v0.unselfish_act_in_window_30d",
  "chain_head_hash": "<sha256-hex>",
  "challenge_nonce": "<hex>",
  "counterparty_id": "<CredexAI VC id>"
}
```

**Response**:

```json
{
  "kind": "compass_falsifiability_response.v0",
  "predicate_id": "cwp.compass.v0.unselfish_act_in_window_30d",
  "chain_head_hash": "<sha256-hex>",
  "sketch": { /* §4 */ },
  "sketch_hash": "<sha256 of canonical sketch bytes>",
  "operator_signature": "<ed25519 over sketch_hash || binding fields>"
}
```

The operator signature binds `predicate_id`, `chain_head_hash`, `challenge_nonce`, and `sketch_hash` so the sketch cannot be swapped across sessions.

## §4 — `CompassEvidenceSketch` (redacted)

The sketch is deterministic given `(chain_records, predicate_id, now_iso)`:

| Field | Content | Redaction rule |
|-------|---------|----------------|
| `evaluator_id` | Predicate ID string | None |
| `window_hours` | Evaluator window used | None |
| `qualifying_record_count` | Integer count that satisfied field completeness | None |
| `kind_histogram` | Map `kind -> count` for records in window | Kinds only, no payloads |
| `newest_qualifying_ts` / `oldest_qualifying_ts` | ISO timestamps of qualifying rows | No free-text fields |
| `counter_claim_active_count` | For harm predicate | Count only, no seq narratives |
| `disputed` | Boolean | Matches `HarmStatus.disputed` when applicable |
| `record_commitments` | List of `sha256(canonical_record_bytes)` for qualifying rows | Hides narrative; enables spot-check if principal later discloses specific rows |

**Forbidden in sketches:** `beneficiary` strings that identify real persons, `other_party_id`, `claimant_id`, `feedback_author_id`, donation recipients, political keywords, or any refusal-floor category token (Everest 113 canonical list).

## §5 — Verifier checks

Given a disclosure bit `b` and sketch `S`:

1. Recompute `sketch_hash` from canonical JSON (`sort_keys=True`, compact separators).
2. Verify operator signature over binding fields.
3. Confirm `S.evaluator_id` matches disclosed `predicate_id`.
4. Confirm `S.qualifying_record_count` meets the public threshold from COMPASS_PREDICATES (e.g., ≥3 for unselfish_act).
5. Confirm timestamps fall inside `window_hours` relative to disclosure `now_iso`.
6. For harm predicate: if disclosure says `bit=false` or `disputed=true`, expect `counter_claim_active_count >= 1` or `disputed=true`.

Failure of (4–6) is a **falsification** — grounds to reject the disclosure as inconsistent with the published evaluator.

## §6 — Reference sketch builder

`~/CredexAI/calm_witness/compass_eval.py` exports:

- `build_compass_evidence_sketch(chain_records, predicate_id, now_iso) -> dict`

The function dispatches to the same pure evaluators used for disclosure (Everests 105–110) and never serializes payload text fields.

Tests: `test_compass_falsifiability_sketch` in `test_compass_eval.py` (gate Everest 112).

## §7 — Relationship to ZK proofs

The sketch is **orthogonal** to the ZK envelope (Everest 119–120). A verifying counterparty SHOULD treat the ZK proof as authoritative for the bit; the sketch is an optional consent-gated sanity check. Operators MUST NOT use sketch release to smuggle extra bits (histogram buckets are capped at kind-level; no cross-principal aggregates).

## §8 — Anti-purity-test

Sketch requests MUST NOT be batched across predicates to infer a similarity score. [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) §4 rate-limits overlapping sketch pulls; operators log repeated sketch harvesting as misuse (Everest 199 family).

## §9 — Versioning

v0 sketches are non-reversible to narratives. v1 may add Merkle inclusion proofs over `record_commitments` when chained to Sigsum heads.

— Musk, 2026-05-20
