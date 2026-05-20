# ZKAC Cross-Primitive Envelope Format v0

**Closes Everest 122 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

**Prereq:** [`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md) (Everest 121), [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md), [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md).

**Reference impl:** [`~/CredexAI/calm_witness/zkac_envelope.py`](../../CredexAI/calm_witness/zkac_envelope.py)

---

## §0 — Purpose

Everest 120 proved Witness and Compass predicates can share one flat `DisclosureEnvelope`. Everest 122 introduces **`CompositeEnvelope`**: a single signed message with **three optional sections** — **Pact**, **Witness**, and **Compass** — so a counterparty can request alignment proof (Pact), state bits (Witness), and values bits (Compass) in one round-trip while receiving **only** what it asked for.

---

## §1 — Wire version and kind

```
wire_version = "calm-stack/wire/v0"
kind         = "CompositeEnvelope"
```

Top-level composite messages use the unified stack wire version from the ZKAC type system. Witness-only and Compass-only single-primitive envelopes remain on `calm-witness/wire/v0` until a future migration; verifiers accept both shapes.

Implementations MUST reject unknown `wire_version` values.

---

## §2 — `CompositeDisclosureRequest`

A counterparty's signed request binding Pact + Witness + Compass asks:

```json
{
  "wire_version": "calm-stack/wire/v0",
  "kind": "CompositeDisclosureRequest",
  "counterparty_id": "<string>",
  "session_nonce": "<string>",
  "request_pact_equality": true | false,
  "witness_predicate_ids": ["cwp.v0.in_baseline_24h", ...],
  "compass_predicate_ids": ["cwp.compass.v0.unselfish_act_in_window_30d", ...],
  "chain_head_at_request": "<64-hex>",
  "freshness_window_seconds": <int>,
  "counterparty_signature": "<opaque>"
}
```

`request_digest` = `SHA-256(canonical_json(content_fields))` excluding `wire_version`, `kind`, and `counterparty_signature` from the signed material (same binding rule as Witness Wire Format §6).

**Routing rule:** predicate IDs MUST NOT appear in the wrong array. Witness IDs use namespace `cwp.v0.*`; Compass IDs use `cwp.compass.v0.*`. Pact equality is requested only via `request_pact_equality`; there is no Pact predicate ID in the witness/compass arrays.

---

## §3 — `CompositeEnvelope`

The operator's response:

```json
{
  "wire_version": "calm-stack/wire/v0",
  "kind": "CompositeEnvelope",
  "request_digest": "<64-hex>",
  "session_nonce": "<string>",
  "chain_head": "<64-hex>",
  "issued_at_iso": "<ISO 8601>",
  "issued_by_operator": "<64-hex>",
  "pact": { ... PactSection ... },
  "witness": { "disclosures": [ ... PredicateDisclosure ... ] },
  "compass": { "disclosures": [ ... PredicateDisclosure ... ] },
  "operator_signature": "sha256:<hex> | ed25519:<hex>"
}
```

### §3.1 — `PactSection` (v0 stub)

Full Calm Pact Σ-protocol equality proofs ship in a later Everest. v0 carries a **stub** sufficient for binding and selective disclosure:

```json
{
  "pact_digest": "<64-hex SHA-256 of canonical pact session material>",
  "equality_bit": 0 | 1,
  "proof_bytes": "<hex, opaque placeholder — v0 stub, not a production Σ-proof>"
}
```

- `pact_digest` binds the Pact session (counterparty commitments exchange + session nonce).
- `equality_bit` is the single bit the counterparty learns: directives categorically equal (1) or not (0).
- `proof_bytes` is opaque at v0; verifiers check presence and hex validity only.

### §3.2 — `witness` and `compass` sections

Each section mirrors Calm Witness Wire Format §5 `PredicateDisclosure` arrays:

```json
{
  "disclosures": [
    {
      "predicate_id": "cwp.v0.in_baseline_24h",
      "commitment_hex": "<hex>",
      "proof": { "a0": "...", "a1": "...", "e0": "...", "e1": "...", "z0": "...", "z1": "...", "claimed_bit": 0 | 1 }
    }
  ]
}
```

Witness disclosures use Witness evaluators; Compass disclosures use Compass evaluators (`compass_disclosure.py`). Proof verification follows CALM_WITNESS_WIRE_FORMAT_v0 §4.

---

## §4 — Selective disclosure rules

These rules are **normative** for operators and verifiers.

### §4.1 — Section presence

| Request field | Envelope MUST contain | Envelope MUST NOT contain |
|---------------|----------------------|---------------------------|
| `request_pact_equality: false` | (omit `pact` key entirely) | `pact` object |
| `request_pact_equality: true` + consent | `pact` object | — |
| `request_pact_equality: true` + no consent | (omit `pact` key) | `pact` object |
| `witness_predicate_ids: []` | (omit `witness` key) | non-empty witness disclosures |
| `compass_predicate_ids: []` | (omit `compass` key) | non-empty compass disclosures |

Absent keys are indistinguishable from "not requested" and "denied by consent" — **no refusal signal**.

### §4.2 — Predicate cardinality

1. Every `witness.disclosures[].predicate_id` MUST be in `witness_predicate_ids`.
2. Every `compass.disclosures[].predicate_id` MUST be in `compass_predicate_ids`.
3. Witness predicate IDs MUST NOT appear under `compass`; Compass IDs MUST NOT appear under `witness`.
4. Smuggled IDs (in envelope but not in request) cause verification failure.

### §4.3 — Consent gates

Per ZKAC type system §4 invariant 2, consent is predicate-specific:

- **Pact:** `pact_consent: bool` — if False, omit `pact` even when requested.
- **Witness:** per-predicate consent map; denied predicates silently omitted.
- **Compass:** per-predicate consent map; denied predicates silently omitted.

### §4.4 — Unobservability

A counterparty that receives a composite envelope learns:

- The disclosed Pact equality bit (if `pact` present).
- The disclosed Witness and Compass bits (per section).
- Session binding (`session_nonce`, `request_digest`, `chain_head`, `issued_at_iso`, `issued_by_operator`).

It does **not** learn:

- Whether other Witness or Compass predicates exist or were evaluated.
- Whether Pact was evaluated but consent-denied (indistinguishable from not requested).
- The cardinality of the principal's full disclosure capability across primitives.

### §4.5 — Global invariants (from ZKAC type system §4)

- **Chain-head freshness:** all Witness and Compass disclosures bind to the same `chain_head` in the envelope.
- **Counterparty fixation:** `request_digest` binds to one `counterparty_id`; envelopes MUST NOT be reused for another counterparty.
- **Proof non-transfer:** composite envelopes are session-bound; replay across sessions fails verification.

---

## §5 — Verification order

A receiving counterparty MUST verify, in order:

1. `wire_version == "calm-stack/wire/v0"`.
2. `kind == "CompositeEnvelope"`.
3. `request_digest` matches `CompositeDisclosureRequest.request_digest()`.
4. `session_nonce` matches the request.
5. **Pact** (if `request_pact_equality`): if `pact` present, validate `pact_digest` hex, `equality_bit ∈ {0,1}`, `proof_bytes` non-empty hex; if absent, accept only when consent may have denied (no error).
6. **Witness:** each disclosure's `predicate_id` ∈ `witness_predicate_ids`; each proof sound per Witness Wire Format §4.
7. **Compass:** each disclosure's `predicate_id` ∈ `compass_predicate_ids`; each proof sound.
8. Reject any disclosure in the wrong section.
9. `operator_signature` valid over canonical content (excluding signature field).

Failures SHOULD return a structured `reasons` list.

---

## §6 — Relationship to single-primitive envelopes

| Primitive | v0 envelope kind | Composite section |
|-----------|------------------|-------------------|
| Calm Pact | (CredexAI VC layer; not Witness `DisclosureEnvelope`) | `pact` stub |
| Calm Witness | `DisclosureEnvelope` | `witness.disclosures` |
| Calm Compass | same shape as Witness | `compass.disclosures` |
| Calm Concord | Everest 123 `AlignmentEnvelope` | (not in v0 composite) |

Everest 123 adds end-to-end multi-primitive **flow** tests; Everest 122 defines the **format**.

---

## §7 — Forward compatibility

- Optional top-level fields MAY be added within `calm-stack/wire/v0` if absent semantics unchanged.
- Production Pact Σ-proofs will replace `proof_bytes` stub without changing `pact_digest` / `equality_bit` binding.
- Concord section (`concord: { ... }`) is reserved for Everest 123+.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match*
