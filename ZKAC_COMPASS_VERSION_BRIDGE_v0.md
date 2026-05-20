# ZKAC Compass Version Bridge v0

**Everest 138 · ZKAC bridging across Compass versions · 2026-05-20**

**Closes Everest 138 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Companions:** [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md), [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md), [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §4.

**Prereq:** Everest 121 ([`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md)), Everest 104 ([`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md)), Everest 111 ([`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md)).

**Everest detail shard:** [`everests/everest_138_compass_version_bridging.md`](everests/everest_138_compass_version_bridging.md) (same normative text; this file is the canonical vault path).

**Acceptance test:** A vault minting Compass disclosures under `calm-compass/wire/v1` produces envelopes that counterparties on `calm-compass/wire/v0` verify within the published deprecation window, with stable `cwp.compass.v0.*` predicate IDs, backward-compatible evidence taxonomy minor bumps, unchanged counter-claim semantics, principal-authored evidence rules preserved, and anti-purity-test caps enforced. The inverse holds for v0 minters against v1 verifiers during the same window.

---

## §1 | Problem statement

Calm Compass evaluates principal-authored values evidence and returns one-bit predicates bound to a chain head. When Compass wire layout or evidence taxonomy increments, vaults, operators, and verifiers must not fracture the ZKAC graph or reopen purity-testing via version salami-slicing.

This document specifies **Compass primitive bridging only**. CredexAI platform bridging is Everest 135. Pact and Witness wire bumps are Everests 136 and 137. Shared N/N-1 discipline lives in [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §0 and §4.

---

## §2 | Normative definitions

| Term | Meaning |
| --- | --- |
| **compass_wire** | Envelope primitive label `calm-compass/wire/v0` or successor `calm-compass/wire/v1` inside `primitive_sections.compass`. Distinct from top-level `wire_version` (`calm-stack/wire/v*`). |
| **evidence_taxonomy_version** | Content-addressed label for [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md) and its JSON Schema extension. v0 today; v1 requires major bump ceremony. |
| **ceremony_version** | UI and audit-process version for evidence authoring ([`COMPASS_EVIDENCE_CEREMONY_v0.md`](COMPASS_EVIDENCE_CEREMONY_v0.md)). Major taxonomy bumps require new ceremony version. |
| **Refusal floor** | Minimum uniform rejection behavior for protected categories, scope violations, and version mismatch paths that must not leak prohibited inference text. |
| **Scope ratchet** | [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md) and predicates §4: prohibited uses may tighten, never loosen. |
| **Deprecation window** | 180 calendar days after Compass wire v1 GA. v1 verifiers accept v0 Compass sections; v0 verifiers accept v1 sections that pass downgrade rules in §5. |
| **Predicate ID** | Immutable string under `cwp.compass.v0.*` per [`COMPASS_PREDICATES_v0.md`](../COMPASS_PREDICATES_v0.md). Wire bumps do not rename IDs. |

---

## §3 | Predicate ID stability (`cwp.compass.v0.*`)

Compass predicate IDs are **immutable** across Compass wire versions (ZKAC Type System §1, Everest 103, Everest 118).

1. **MUST NOT** rename any `cwp.compass.v0.*` identifier during a wire or taxonomy minor bump.
2. **MAY** add predicates only under a new namespace (`cwp.compass.v1.*`) with audit panel review (Everest 115) and a separate registry hash.
3. **MUST NOT** change evaluator semantics for an existing ID without a new predicate ID and a logged protocol amendment.

### §3.1 | v0 predicate registry (frozen during window)

The six v0 predicates in [`COMPASS_PREDICATES_v0.md`](../COMPASS_PREDICATES_v0.md) §2 remain the authoritative set for `cwp.compass.v0.*`:

| ID | Role in bridging |
| --- | --- |
| `cwp.compass.v0.unselfish_act_in_window_30d` | Principal-authored evidence only |
| `cwp.compass.v0.cross_group_engagement_in_window_90d` | Principal-authored; principal-named out-group |
| `cwp.compass.v0.refused_opportunity_to_harm` | Principal-authored |
| `cwp.compass.v0.no_known_willful_harm_in_window_365d` | Counter-claim protocol bound |
| `cwp.compass.v0.respect_for_difference_evidence` | Two-party-authored |
| `cwp.compass.v0.willing_to_be_corrected` | Principal-authored; optional second-party sig |

Verifiers load the same content-addressed registry hash for these six entries during the deprecation window.

---

## §4 | Evidence taxonomy version bumps

Evidence kinds are defined in [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](../COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md). Version bumps are **orthogonal** to `compass_wire` but MUST be declared in operator well-known metadata (§8).

### §4.1 | Minor bump (additive)

A **minor** taxonomy bump:

- Adds **optional** payload fields on existing `compass_evidence.*` kinds only.
- Does **not** rename kinds, remove fields, or change required-field semantics.
- Does **not** require new `cwp.compass.v0.*` predicate IDs.
- v0 evaluators **ignore** unknown optional fields (forward compatible).
- v1 evaluators **accept** records missing new optional fields (backward compatible).

Example (illustrative): `compass_evidence.unselfish_act` gains optional `locale_hint` string; evaluators for `unselfish_act_in_window_30d` unchanged.

### §4.2 | Major bump (breaking)

A **major** taxonomy bump:

- Renames or removes a kind, changes required fields, or alters counter-claim field semantics.
- Requires `evidence_taxonomy_version: calm-compass/evidence/v1` (or successor).
- Requires new **ceremony_version** and audit panel publication (Everest 115).
- Requires **180-day deprecation window** during which v1 verifiers accept v0 records via explicit downgrade map (§5.2).
- **MUST NOT** enter via `compass_wire` increment alone (ZKAC_VERSION_BRIDGING §7).

### §4.3 | Immutability preserved

Taxonomy §11 immutability holds across bumps: no post-sign edits, no version field inside chain records. Bumps affect **validator and evaluator** behavior only, not retroactive chain mutation.

### §4.4 | Registry pinning

`/.well-known/calm-operator.json` MUST publish:

```json
{
  "compass_wire_supported": ["calm-compass/wire/v0", "calm-compass/wire/v1"],
  "evidence_taxonomy_version": "calm-compass/evidence/v0",
  "compass_predicate_registry_sha256": "<64-hex>"
}
```

Counterparties reject Compass sections when taxonomy version is outside the advertised set.

---

## §5 | Counter-claim protocol compatibility

[`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](../COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md) semantics are **stable** across Compass wire v0 and v1.

### §5.1 | Wire-stable fields

These fields and behaviors MUST NOT change on minor wire or taxonomy bumps:

| Artifact | Stability rule |
| --- | --- |
| `compass_evidence.counter_claim` | `claimant_id`, `alleged_harm_narrative`, `alleged_harm_window`, `submitted_via` required |
| `compass_evidence.principal_rebuttal` | `targets_counter_claim_seq`, substantive `rebuttal_narrative` |
| `HarmStatus` | `bit`, `disputed`, `active_counter_claim_seqs` from `no_known_willful_harm()` |
| Grace period | 30 days default before claim goes active |
| Claim window | 365 days default |

### §5.2 | Major taxonomy downgrade

If a major bump renames counter-claim payload keys, the downgrade map MUST:

1. Map v1 records to v0 parser shape deterministically.
2. Preserve `seq` and `ts` unchanged.
3. Never drop active counter-claims silently.
4. Return `downgrade_counter_claim_incompatible` when mapping fails.

### §5.3 | Verifier interpretation across versions

| State | `no_known_willful_harm` wire bit | `disputed` flag |
| --- | --- | --- |
| No claims | true | false |
| Claims in grace | true | false |
| Active unrebutted | false | true |
| Rebutted or aged out | true | false |

v0 and v1 verifiers MUST produce identical `(bit, disputed)` for the same chain snapshot.

### §5.4 | Counter-claim metadata in falsification

Counter-claims filed during a version transition MUST record `compass_wire` and `evidence_taxonomy_version` in audit-panel metadata (not in the public chain record) so falsifiers know which downgrade path applied.

---

## §6 | Principal-authored evidence across versions

Rules from taxonomy §1A and [`CALM_COMPASS_PROTOCOL_v0.md`](../CALM_COMPASS_PROTOCOL_v0.md) §3A survive all bumps in this Everest.

### §6.1 | Author binding

| Kind | Author | Operator on record |
| --- | --- | --- |
| `unselfish_act`, `cross_group_interaction`, `refused_harm`, `principal_rebuttal` | Principal P | P's operator only |
| `correction_accepted` (principal phase) | Principal P | P's operator |
| `counter_claim` | Claimant Q | Q's operator (not P's) |
| `respect_engagement` | P + other party O | P's operator; O signs |

v1 hydrators MUST reject principal-authored kinds where `operator` does not match P's registered operator fingerprint.

### §6.2 | Evaluator completeness

`compass_eval.py` drop rules (missing fields, `expectation_of_return: true`, `substantive: false`, zero cost) are unchanged across minor bumps. New optional fields MUST NOT relax completeness checks.

### §6.3 | Voluntary cadence

No operator auto-mint, streak scoring, or nudge fields may appear in a wire bump. Version increments MUST NOT introduce gamification metadata on evidence records.

### §6.4 | Witness duress composition

If the same composite envelope carries `cwp.v0.bank_teller_note_active = true`, every Compass predicate in the envelope downgrades to **Unknown** on v0 and v1 verifiers alike ([`COMPASS_PREDICATES_v0.md`](../COMPASS_PREDICATES_v0.md) §6).

---

## §7 | Anti-purity-test (≤5 predicates per envelope)

Concord and refusal-floor discipline ([`CALM_CONCORD_PROTOCOL_v0.md`](../CALM_CONCORD_PROTOCOL_v0.md) §4, [`REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md`](../REFUSAL_FLOOR_PRESSURE_THREAT_MODEL_v0.md) §2.2) extends to Compass bridging.

### §7.1 | Cardinality cap

A single composite envelope MUST NOT disclose more than **five** distinct `cwp.compass.v0.*` predicates in `primitive_sections.compass`, across any supported `compass_wire` label.

Rationale: v0 defines six predicates; the cap prevents a counterparty from requesting all six in one session to approximate a similarity vector. Principals needing a sixth predicate MUST use a separate consent grant and session nonce.

### §7.2 | Forbidden outputs across versions

Bridging MUST NOT introduce:

- Numeric alignment, similarity, or match-quality scores on Compass sections.
- Ranked predicate lists ordered by "values closeness."
- Cross-principal comparison fields in Compass wire extensions.

### §7.3 | Degenerate requirement rejection

Requirements that name five predicates with `joint_threshold` N=5 are rejected as degenerate `all_satisfied` purity tests (Concord §4.1). Wire bumps MUST NOT add modes that bypass this check.

### §7.4 | Output shape

Bridging APIs return one bit per disclosed `cwp.compass.v0.*` predicate plus structured error codes. No similarity scores, no ranked predicate lists, no cross-principal comparison fields.

---

## §8 | Refusal floor inheritance

Compass wire bumps do not relax prohibited uses in [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md) or the permanent deny classes in [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4.

### §8.1 | Uniform refusal on version mismatch

When `bridge_compass_accepted` returns false, the verifier returns `unsupported_compass_wire` with the same uniform external shape as scope refusal (`refusal_floor`, `permanently_deny`, or `uniform_204` per suite policy). It MUST NOT return a false `claimed_bit` as a stand-in for rejection.

### §8.2 | Protected categories (PREDICATE_VOCABULARY §4 + COMPASS §4)

Wire bumps MUST NOT enable predicates or evidence fields that infer race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations-to-causes, contentious opinion, cross-principal comparison, predictive character assessment, or non-principal-defined group membership. Downgrade paths MUST NOT leak text that v0 suppressed for those classes.

### §8.3 | Downgrade and counter-claims

When downgrade would expose a refusal reason that legacy UI cannot render, the verifier returns the same uniform refusal code the native v0 path would have returned. Downgrade MUST NOT drop `disputed` visibility on `no_known_willful_harm` when active counter-claims exist.

### §8.4 | Counterparty class preservation

Default-deny entries for `governmental`, `medical`, `financial`, `journalistic`, and `anonymous` survive wire migration unchanged. v1 Operators MUST NOT map new counterparty classes to old IDs with looser defaults.

---

## §9 | Scope statement ratchet

[`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md) and [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4 define a one-way ratchet. Compass version bridging adds wire-level inheritance rules.

### §9.1 | Ratchet rules

1. Wire bumps MAY add prohibited uses (tightening).
2. Wire bumps MUST NOT remove or weaken §2 scope entries or predicate §4 refusal floor items.
3. Wire bumps MUST NOT introduce a flag that bypasses `principal_consents_to_disclose` or permanent-deny classes.
4. No new `cwp.compass.v0.*` predicates may enter via wire bump alone; minting requires audit panel review (Everest 115) and a new namespace.

### §9.2 | Employment, credit, and screening (out of scope)

Compass bridging MUST NOT be used to prove suitability for **employment**, **credit**, **insurance underwriting**, **tenant screening**, or **medical diagnosis**. Wire bumps do not authorize new evidence kinds for those domains. Operators deploying Compass for those purposes forfeit attestation regardless of `compass_wire`.

### §9.3 | Concord inheritance

Composite envelopes inherit Concord anti-purity-test rules from Everest 113. Compass bridging MUST NOT add graded alignment or population ranking fields to Compass sections when the composite wire increments.

---

## §10 | Envelope downgrade rules (Compass section)

### §10.1 | Allowed transforms (v1 to v0)

| v1-only field | Downgrade action |
| --- | --- |
| Optional taxonomy fields on evidence sketches in proofs | Omit in v0 verifier view |
| `compass_wire` = `calm-compass/wire/v1` | Verify via `bridge_version_accepted` then strip v1-only proof encoding |
| Extra classifier hash slot | Omit if v0 schema has single `classifier_hash` |

### §10.2 | Forbidden downgrades

Implementations MUST NOT:

- Coerce a Compass claimed bit between 0 and 1.
- Drop `disputed` visibility on `no_known_willful_harm` when active counter-claims exist.
- Strip `predicate_id` or rename `cwp.compass.v0.*` strings.
- Merge two sessions to infer a sixth predicate without fresh consent.

### §10.3 | Failure codes

| Code | Meaning |
| --- | --- |
| `unsupported_compass_wire` | `compass_wire` not in verifier supported set |
| `unsupported_evidence_taxonomy` | taxonomy version not advertised |
| `compass_predicate_cap_exceeded` | more than five Compass predicates requested |
| `downgrade_counter_claim_incompatible` | major taxonomy map failed |

---

## §11 | Falsifiability

### §11.1 | Published supported sets

Operators publish `compass_wire_supported`, `evidence_taxonomy_version`, and `compass_predicate_registry_sha256` in `/.well-known/calm-operator.json`. Counterparties check before parsing Compass sections.

### §11.2 | Golden corpus

Golden envelopes required before BAGGED:

1. v0 Compass minter / v0 verifier
2. v1 Compass minter / v0 verifier (downgrade path)
3. v1 minter / v1 verifier
4. v0 minter / v1 verifier
5. Mixed composite with exactly five Compass predicates (cap boundary)

Each tuple must agree on bits for all disclosed `cwp.compass.v0.*` IDs.

### §11.3 | Counterexample protocol

A counterparty may file a counter-claim or audit request when the same `predicate_id` and chain head yield different bits across `compass_wire` labels without a published taxonomy migration record.

### §11.4 | Top-level wire check

Compass bridging sits inside composite envelopes. Verifiers MUST call `bridge_version_accepted(envelope.wire_version, supported)` and `bridge_compass_accepted(compass_wire, supported)` from [`version_bridge.py`](../CredexAI/calm_witness/version_bridge.py) before Compass-specific parsing.

---

## §12 | Reference implementation and gates

| Artifact | Path |
| --- | --- |
| Shared bridging (135 to 138) | [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) |
| Canonical Compass bridge (this file) | [`ZKAC_COMPASS_VERSION_BRIDGE_v0.md`](ZKAC_COMPASS_VERSION_BRIDGE_v0.md) |
| Everest detail shard | [`everests/everest_138_compass_version_bridging.md`](everests/everest_138_compass_version_bridging.md) |
| `bridge_compass_accepted` | [`~/CredexAI/calm_witness/version_bridge.py`](../CredexAI/calm_witness/version_bridge.py) |
| Everest 138 gate | [`~/CredexAI/scripts/everest_138_zkac_compass_version_bridge_gate.py`](../CredexAI/scripts/everest_138_zkac_compass_version_bridge_gate.py) |
| Combined 135 to 138 gate | [`~/CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py`](../CredexAI/scripts/everest_135_138_zkac_version_bridging_gate.py) |

---

## §13 | Acceptance checklist

1. `cwp.compass.v0.*` IDs unchanged across Compass wire bump.
2. Minor taxonomy bumps add optional fields only; major bumps use ceremony + window.
3. Counter-claim and `HarmStatus` semantics identical on v0 and v1 verifiers for the same chain.
4. Principal-authored and two-party-authored binding rules preserved.
5. At most five Compass predicates per composite envelope (anti-purity-test).
6. `bridge_compass_accepted` passes for supported Compass wire sets; golden corpus green.
7. Refusal floor and scope ratchet sections unchanged in meaning across bumps.

---

**One-line result:** Everest 138 BAGGED: Compass `cwp.compass.v0.*` IDs and counter-claim semantics stay stable across wire and taxonomy bumps; minor evidence fields only; ≤5 predicates per envelope; refusal floor and scope ratchet inherited; `bridge_compass_accepted` gates the shared N/N-1 window.

Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
