# ZKAC Witness Version Bridge v0

**Everest 137 · ZKAC bridging across Witness versions · 2026-05-20**

**Closes Everest 137 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Companions:** [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md), [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md), [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §3.

**Prereq:** Everest 121 ([`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md)), [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md).

**Acceptance test:** A Witness disclosure envelope minted at `calm-stack/wire/v1` verifies on counterparties that advertise only `calm-witness/wire/v0` or `calm-stack/wire/v0` support during the published deprecation window, and the inverse holds for legacy minters against v1 verifiers. Predicate IDs remain stable; evaluator semantics are pinned by hash snapshots; chain schema bumps append migration records; refusal floor and scope ratchet survive every wire bump. Unknown witness wire labels reject with `unsupported_wire_version`, never with a false predicate bit.

---

## §1 | Problem statement

Calm Witness lets one autonomous agent disclose one principal-authorized safety-relevant bit to another without leaking biometrics, transcripts, or medical history ([`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)). On-the-wire layout is normative in [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md). Disclosure envelopes carry `wire_version`, `predicate_id`, proof bytes, and a chain head anchored in a transparency log.

When the Witness wire bumps from `calm-witness/wire/v0` (Witness-only envelopes) to `calm-stack/wire/v0` (composite ZKAC stack) and onward to `calm-stack/wire/v1` (successor commitment encoding), counterparties must not fracture. A counterparty on legacy wire must still verify v1 envelopes that pass downgrade rules. A v1 verifier must accept legacy envelopes during the window. A verifier that receives an unknown wire must refuse parsing and return `unsupported_wire_version`. It must not map unknown wire to `claimed_bit: 0`.

This document specifies **Calm Witness primitive bridging only**. CredexAI platform bridging is Everest 135. Pact and Compass wire bumps are Everests 136 and 138. Shared window discipline lives in [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §3.

---

## §2 | Normative definitions

| Term | Meaning |
| --- | --- |
| **Witness wire v0** | Wire label `calm-witness/wire/v0`. Witness-only `DisclosureEnvelope` layout per [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md). |
| **Stack wire v0** | Wire label `calm-stack/wire/v0`. Composite and Witness sections share this label in the unified stack. |
| **Stack wire v1** | Successor label `calm-stack/wire/v1`. May add optional metadata slots; commitment encoding may differ; predicate bit semantics unchanged. |
| **predicate_id** | Immutable string `cwp.vN.<slug>` (e.g. `cwp.v0.in_baseline_24h`). Wire bumps do not rename IDs. |
| **evaluator_hash** | SHA-256 of canonical JSON over `(id, type, parameters, evaluator)` per reference `evaluator_hash()` in [`predicates.py`](../CredexAI/calm_witness/predicates.py). |
| **evaluator snapshot** | Content-addressed map `predicate_id → evaluator_hash` shipped as `predicates_v0.snapshot.json`. |
| **Deprecation window** | 180 calendar days per successor wire in `DEPRECATION_WINDOWS` ([`version_bridge.py`](../CredexAI/calm_witness/version_bridge.py)). |
| **chain_schema_migration** | Principal chain record `kind: chain_schema_migration` linking old and new `schema_version` for `user_state.jsonl` records. |
| **Refusal floor** | Minimum uniform rejection behavior for scope violations, permanent deny classes, and downgrade paths that must not leak protected-category text. |
| **Scope ratchet** | [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §4: §2 prohibited uses may tighten, never loosen. |

---

## §3 | Witness wire versioning

### §3.1 | Wire label map

| Label | Role | Successor (window) |
| --- | --- | --- |
| `calm-witness/wire/v0` | Legacy Witness-only envelopes | `calm-stack/wire/v0` (180 days) |
| `calm-stack/wire/v0` | Current composite and Witness default | `calm-stack/wire/v1` (180 days) |
| `calm-stack/wire/v1` | Successor encoding | (future v2 TBD) |

### §3.2 | Verifier acceptance

Before parsing disclosures, verifiers call:

```
bridge_version_accepted(envelope.wire_version, verifier_supported_wire) == true
```

If false, return `unsupported_wire_version` and MUST NOT treat `disclosures[].claimed_bit` as authoritative.

### §3.3 | Minter default

During the deprecation window, v1-capable minters SHOULD default to `calm-stack/wire/v1` when all proofs use v1 encodings. When any disclosure requires v0-only proof shape, the minter MUST emit `calm-stack/wire/v0` or dual-stack proofs per §6.

Legacy Witness-only minters MAY continue emitting `calm-witness/wire/v0` until the `calm-witness` → `calm-stack` window closes.

### §3.4 | Commitment encoding vs predicate semantics

Wire bumps affect Pedersen commitment layout, proof tuple shape, and optional envelope metadata only. They do **not** change:

- Predicate evaluator pseudocode for an existing `predicate_id`.
- Default-consent matrix cells for a given counterparty class.
- The meaning of `claimed_bit ∈ {0, 1}` for bool predicates.

---

## §4 | Predicate ID stability

Predicate ID stability is load-bearing ([`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) §2). Witness version bridging inherits these rules:

### §4.1 | Append-only registry

1. Published IDs are permanent. Evaluator semantics for `cwp.v0.*` cannot change after release.
2. Semantic changes require a new ID under a new namespace version (`cwp.v1.*`), not an in-place edit.
3. `deprecated` IDs remain verifiable; `tombstoned` IDs are rejected forward but never reissued.
4. Wire bumps MUST NOT rename, split, or merge existing `cwp.v0.*` strings.

### §4.2 | Registry pinning across wires

v0 and v1 verifiers load the same content hash for `cwp.v0.*` entries during the deprecation window. A registry extension for `cwp.v1.*` MUST NOT alter hashes of v0 entries in the snapshot file.

### §4.3 | Consent and composite envelopes

`ConsentRecord` objects reference `predicate_id` strings. Witness wire migration does not invalidate consent: the Operator re-evaluates consent against the same IDs post-migration.

Composite envelopes (Everest 122) bind multiple Witness predicate IDs. Mixed-namespace envelopes are forbidden during the window unless every ID appears in the counterparty `supported_predicate_namespaces` well-known field.

### §4.4 | Golden corpora (Everest 55)

Golden disclosure vectors MUST pass on both sides of each active deprecation window. A wire bump is not BAGGED until:

- Same `predicate_id`, same evaluator snapshot hash, same `claimed_bit` on v0 and v1 verifier paths after downgrade.
- Failure to reproduce any golden tuple blocks release.

---

## §5 | Evaluator hash snapshots

Wire bumps do not substitute for vocabulary governance. Evaluator semantics are pinned independently of `wire_version`.

### §5.1 | Snapshot material

For each predicate `p`, the reference implementation computes:

```python
evaluator_hash(p) = SHA-256(canonical_json({
  "id": p.id,
  "type": p.type,
  "parameters": p.parameters,
  "evaluator": p.evaluator,
}))
```

The shipped snapshot [`predicates_v0.snapshot.json`](../CredexAI/calm_witness/schema/predicates_v0.snapshot.json) maps every `cwp.v0.*` ID to its hash at release time.

### §5.2 | stability_check gate

Before minting envelopes at a new Witness wire label, CI and release gates run `stability_check()` ([`predicates.py`](../CredexAI/calm_witness/predicates.py)):

- Every ID present in the prior snapshot MUST hash to the same value in the current vocabulary JSON.
- New IDs are allowed (append-only).
- Mutated evaluator text for an existing ID fails with `evaluator_hash_mismatch`.

Witness wire bumps MUST NOT ship without a green `stability_check` for the pinned vocabulary generation.

### §5.3 | Well-known publication

Each Operator publishes `predicate_registry_sha256` and `evaluator_snapshot_sha256` in `/.well-known/calm-operator.json` alongside `supported_wire_versions`. Counterparties MAY reject envelopes when the operator advertises a snapshot hash that does not match the public registry artifact they pinned.

### §5.4 | Counterexample

A falsifying observation: same `predicate_id`, same `wire_version`, two envelopes with different `claimed_bit` values, both accepted by the same verifier, without a `tombstone` or `deprecated` registry entry explaining the divergence. If evaluator hashes differ across those envelopes, the vocabulary release is invalid regardless of wire label.

---

## §6 | Envelope downgrade rules

Downgrade is the deterministic transform that strips v1-only fields so a v0 or legacy Witness verifier parses a bit-equivalent envelope.

### §6.1 | Allowed transforms

| v1-only field | Downgrade action |
| --- | --- |
| `proof_encoding` = `ristretto_v1` | Verify `proof` (v0 shape) when dual-stack present; else `downgrade_proof_missing` |
| `attestation_fingerprint` (optional) | Omit when v0 schema has no slot |
| `platform_version` | Omit; infer from operator attestation |
| Extra `disclosures[]` entries | Reject with `downgrade_extra_disclosure`; no silent drop |

### §6.2 | Dual-stack minting

v1 minters targeting legacy counterparties SHOULD mint dual-stack disclosures when proof encodings differ: both `proof` and `proof_v1` per `PredicateDisclosure`, with `wire_version` at `calm-stack/wire/v1`. Legacy verifiers verify `proof` only after downgrade.

### §6.3 | Forbidden downgrades

Implementations MUST NOT:

- Coerce `claimed_bit` from 1 to 0 or 0 to 1.
- Drop `operator_signature`, `chain_head`, `request_digest`, or `session_nonce`.
- Strip or rename `disclosures[].predicate_id`.
- Relax freshness: `issued_at_iso` and Sigsum anchors must survive downgrade unchanged.

### §6.4 | Legacy alias

`calm-witness/wire/v0` envelopes downgrade to `calm-stack/wire/v0` field layout before v1 stripping. `bridge_version_accepted` treats the legacy label as N-1 of stack v0 during the window ([`version_bridge.py`](../CredexAI/calm_witness/version_bridge.py)).

---

## §7 | Chain schema migration

Witness proofs bind to `chain_head` over `user_state.jsonl` ([`schema/user_state_v0.json`](../CredexAI/calm_witness/schema/user_state_v0.json)). When record layout bumps, migration is explicit on the chain, not silent in verifiers.

### §7.1 | schema_version field

Each JSONL record carries integer `schema_version` (minimum 0). Evaluators for v0 predicates read only fields defined for their window unless a migration record authorizes broader parsing.

### §7.2 | chain_schema_migration record

When the principal vault adopts a new chain schema (new required payload keys, renamed self-report kinds, or stricter validation), the Operator MUST append:

```json
{
  "kind": "chain_schema_migration",
  "payload": {
    "from_schema_version": 0,
    "to_schema_version": 1,
    "from_chain_head": "<64-hex>",
    "to_chain_head": "<64-hex>",
    "migration_at_iso": "<ISO8601>",
    "migration_reason": "user_state_v0_1_adoption",
    "evaluator_snapshot_sha256": "<64-hex>",
    "principal_signature": "<64-hex sig over canonical record>"
  }
}
```

### §7.3 | Verifier behavior

Counterparties verifying post-migration envelopes MUST treat proofs bound to `from_chain_head` as stale unless `issued_at_iso` predates migration and freshness rules still hold. Proofs bound to `to_chain_head` are authoritative after migration.

Predicate evaluation over migrated chains MUST use the evaluator snapshot hash pinned at migration time for all `cwp.v0.*` IDs. Schema bumps do not authorize evaluator edits without a new predicate ID.

### §7.4 | Relationship to template migration

Biometric template supersession ([`everests/everest_17_template_version_migration.md`](everests/everest_17_template_version_migration.md)) uses `kind: template.migration`. Chain schema migration is orthogonal: a vault may migrate chain layout without rotating templates, and vice versa. Both records MUST appear on the chain when both events occur.

### §7.5 | Failure codes

| Code | Meaning |
| --- | --- |
| `chain_schema_stale` | `chain_head` predates `chain_schema_migration` without valid freshness exception |
| `chain_schema_unknown` | Record `schema_version` not supported by verifier |
| `evaluator_snapshot_mismatch` | Operator snapshot hash differs from pinned public artifact |

---

## §8 | Refusal floor inheritance

Witness wire bumps do not relax prohibited uses in [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §2 or default-deny matrices in [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md).

### §8.1 | Uniform refusal on version mismatch

When `bridge_version_accepted` returns false, the verifier returns `unsupported_wire_version` with the same uniform external shape as scope refusal (`refusal_floor`, `permanently_deny`, or `uniform_204` per suite policy). It MUST NOT return a false `claimed_bit` as a stand-in for rejection.

### §8.2 | Downgrade and protected categories

When downgrade would expose a refusal reason that legacy UI cannot render, the verifier returns the same uniform refusal code the native v0 path would have returned. Downgrade MUST NOT leak governmental, medical, employment-adjacent, or protected-category text that v0 suppressed.

### §8.3 | Counterparty class preservation

Default-deny entries for `governmental`, `medical`, `anonymous`, and classes without an employment or insurance slot survive wire migration unchanged. v1 Operators MUST NOT map new counterparty classes to old IDs with looser defaults.

### §8.4 | License and trademark

Deployments that use a Witness wire bump to enable a §2 prohibited use forfeit Calm Witness naming rights per scope statement §3.2. Wire version is visible in envelope metadata; misuses are attributable to the deployment fingerprint.

---

## §9 | Scope statement ratchet

[`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §4 defines a one-way ratchet. Witness version bridging adds wire-level inheritance rules.

### §9.1 | Ratchet rules

1. Wire bumps MAY add §2 prohibited uses (tightening).
2. Wire bumps MUST NOT remove or weaken §2 entries.
3. Wire bumps MUST NOT introduce a flag that bypasses `principal_consents_to_disclose` or permanent-deny classes.
4. No new predicate categories may enter via wire bump alone; minting requires Everest 54 audit and a new `cwp.vN.*` ID.

### §9.2 | Scope-statement versioning

The scope statement document version is independent of `wire_version`. Tightening edits ship as scope patches. Loosening edits are forbidden regardless of Witness wire label.

### §9.3 | Concord inheritance

Composite envelopes inherit Concord anti-purity-test rules from Everest 113. Witness bridging MUST NOT add graded alignment or population ranking fields to Witness sections when the composite wire increments.

---

## §10 | Falsifiability

### §10.1 | Published supported sets

Each Operator publishes in `/.well-known/calm-operator.json`:

```json
{
  "supported_wire_versions": [
    "calm-witness/wire/v0",
    "calm-stack/wire/v0",
    "calm-stack/wire/v1"
  ],
  "predicate_registry_sha256": "<64-hex>",
  "evaluator_snapshot_sha256": "<64-hex>",
  "deprecation_window_end_iso": "2026-11-20T00:00:00Z"
}
```

Counterparties reject envelopes outside advertised sets before parsing proofs.

### §10.2 | Golden corpus tuples

The repo maintains four tuples per active window edge: legacy/v0, v1/v0, v1/v1, v0/v1. Each asserts expected `claimed_bit` per `predicate_id` and absence of score or similarity fields in verifier output.

### §10.3 | Transparency log anchor

A falsifying observation: same `predicate_id`, same claimed bit, different `chain_head`, both accepted by the same verifier across Witness wire versions without a `chain_schema_migration` or `platform_migration` record between them.

### §10.4 | Error code registry

| Code | Meaning |
| --- | --- |
| `unsupported_wire_version` | `bridge_version_accepted` returned false |
| `downgrade_proof_missing` | v1 proof cannot map to v0 |
| `downgrade_extra_disclosure` | Disclosure count mismatch after strip |
| `evaluator_hash_mismatch` | `stability_check` failed for pinned ID |
| `chain_schema_stale` | Head predates migration |

---

## §11 | Reference implementation and gates

| Artifact | Path |
| --- | --- |
| This document (canonical v0) | [`ZKAC_WITNESS_VERSION_BRIDGE_v0.md`](ZKAC_WITNESS_VERSION_BRIDGE_v0.md) |
| Everest narrative companion | [`everests/everest_137_witness_version_bridging.md`](everests/everest_137_witness_version_bridging.md) |
| Wire format RFC | [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md) |
| Shared bridging rules (135 to 138) | [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §3 |
| `bridge_version_accepted` | [`~/CredexAI/calm_witness/version_bridge.py`](../CredexAI/calm_witness/version_bridge.py) |
| `evaluator_hash`, `stability_check` | [`~/CredexAI/calm_witness/predicates.py`](../CredexAI/calm_witness/predicates.py) |
| Evaluator snapshot | [`~/CredexAI/calm_witness/schema/predicates_v0.snapshot.json`](../CredexAI/calm_witness/schema/predicates_v0.snapshot.json) |
| Chain record schema | [`~/CredexAI/calm_witness/schema/user_state_v0.json`](../CredexAI/calm_witness/schema/user_state_v0.json) |
| Everest 137 gate | [`~/CredexAI/scripts/everest_137_zkac_witness_version_bridge_gate.py`](../CredexAI/scripts/everest_137_zkac_witness_version_bridge_gate.py) |

---

## §12 | Acceptance checklist

1. v1 minter envelope verifies on legacy/v0 counterparty within 180-day window.
2. `wire_version` checked via `bridge_version_accepted`; legacy `calm-witness/wire/v0` aliases during window.
3. `cwp.v0.*` predicate IDs unchanged; `stability_check` green against snapshot.
4. Downgrade rules produce bit-identical verification on v0 verifiers.
5. `chain_schema_migration` required when `schema_version` bumps; stale heads rejected.
6. Witness scope §2 prohibitions unchanged; refusal floor and scope ratchet inherited.
7. Golden corpus and gate exit 0.

---

Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

**One-line result:** Everest 137 Witness version bridging is BAGGED; stable `cwp.v0.*` IDs, evaluator hash snapshots, explicit chain schema migration, and N/N-1 wire windows preserve the refusal floor and scope ratchet without false bits on unknown wire.
