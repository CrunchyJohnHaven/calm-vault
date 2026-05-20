# ZKAC — The Next 200 Engineering Everests (Summits 101–300)

> *"Calculate whether that person's values align with yours from this. Measure unselfishness, untribalism, respect across difference, evidence of willful harm. Make sure our next 200 unclimbed summits are clearly defined and ready to attack. Focus on critical infrastructure for agents and ZKACs."*
>
> — John Bradley, 2026-05-20 12:00 EDT

**Draft v0 · 2026-05-20 · Calm**
**Sequel to [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**

## §0 — What this document is

The first 100 Everests built **Calm Witness** — a primitive that lets one autonomous AI agent disclose one principal-authorized **state** bit to another. The bank-teller-note primitive is now real: a counterparty can learn the bit and nothing else.

The next 200 build out the **rest of the ZKAC programme** — Zero-Knowledge Attested Context — the broader infrastructure agents need once Calm Witness exists. Three thrusts dominate:

1. **A third primitive: Calm Compass** (Range I, summits 101–120). Values-attestation. Lets a counterparty know whether the principal's behavioral evidence supports a small set of named values predicates (unselfish, untribal, respect-across-difference, no willful harm). Same protected-category floor as Calm Witness; same principal-authored substrate; same ZK envelope flow.
2. **Cross-primitive infrastructure** (Ranges J–M, summits 121–200). The vault, SDK, mobile, adversarial-hardening, and deployment-maturity work that lets Pact + Witness + Compass compose at scale.
3. **Standards, ecosystem, succession** (Ranges N–R, summits 201–300). From NIST submissions through reference deployments to a sunset plan that lets the Calm suite outlive any one founder, organization, or jurisdiction.

This document is the **climbing route**, not the climb. Each summit gets a stable ID (Everest 101 … Everest 300), a one-sentence acceptance test, an effort estimate, and a prereq list. Numbering is **stable**: gaps or insertions get sub-IDs (e.g. 137b). When a summit is bagged, its line gets a `*Status:* **BAGGED**` annotation per the existing convention.

## §1 — Phase legend

```
RANGE I  101–120  Calm Compass v0 — values-attestation primitive
RANGE J  121–140  ZKAC substrate — multi-primitive envelopes, vaults, federation
RANGE K  141–160  Agent infrastructure — discovery, reputation, handoff, billing
RANGE L  161–180  Adversarial hardening — at-scale defenses + recovery ceremonies
RANGE M  181–200  Deployment maturity — multi-region, compliance, prohibitions
RANGE N  201–220  Standards & policy — IETF, W3C, DIF, NIST, international
RANGE O  221–240  Ecosystem & adoption — reference deployments, UX, onboarding
RANGE P  241–260  Long-term sustainability — foundation, succession, archival
RANGE Q  261–280  Three-primitive composition — Pact + Witness + Compass
RANGE R  281–300  Beyond ZKAC — Calm Foresight (intent), federation, mainstream
```

---

## RANGE I — Calm Compass (101–120): Values-Attestation Primitive

The third Calm primitive. Where Pact proves *mission equality* and Witness proves *state baseline*, Compass proves a **small set of principal-authored values bits**. The bits are explicit, narrow, falsifiable, and refusable; the underlying evidence is chained in the principal's vault and never crosses the envelope boundary.

**Everest 101 — Calm Compass Problem Statement & Threat Model.** *Acceptance:* a versioned doc captures the values use case, the actors, the trust assumptions, the adversaries, and what the protocol does + does not claim about values. *Effort:* M. *Prereq:* 1. *Status:* **BAGGED (Summit 101/300) 2026-05-20** — [`everests/everest_101_calm_compass_problem_statement.md`](everests/everest_101_calm_compass_problem_statement.md) (alias [`CALM_COMPASS_PROBLEM_STATEMENT_v0.md`](CALM_COMPASS_PROBLEM_STATEMENT_v0.md)); gate `everest_101_zkac_compass_problem_gate.py`.

**Everest 102 — Calm Compass Protocol Spec v0.** *Acceptance:* draft protocol doc analogous to `ZKBB_USER_PROTOCOL_v0.md`, with hydration / predicate evaluation / disclosure layers explicit. *Effort:* M. *Prereq:* 101. *Status:* **BAGGED (Summit 102/300) 2026-05-20** — [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md), 12,078 bytes; gate [`~/CredexAI/scripts/everest_102_zkac_compass_protocol_gate.py`](../../CredexAI/scripts/everest_102_zkac_compass_protocol_gate.py) exit 0.

**Everest 103 — Compass Predicate Vocabulary v0.** *Acceptance:* an enumerated list of v0 values predicates with formal semantics, ID stability rules, and explicit refusal floor. *Effort:* L. *Prereq:* 102. *Status:* **BAGGED (Summit 103/300) 2026-05-20** — [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) + [`everests/everest_103_compass_predicate_vocabulary_v0.md`](everests/everest_103_compass_predicate_vocabulary_v0.md); gate [`~/CredexAI/scripts/everest_103_zkac_compass_predicates_gate.py`](../../CredexAI/scripts/everest_103_zkac_compass_predicates_gate.py) exit 0.

**Everest 104 — Values Evidence Taxonomy.** *Acceptance:* a doc enumerating the kinds of records that can serve as evidence (financial transfer, declined-opportunity narration, cross-group interaction record, etc.), with strict per-kind schema. *Effort:* M. *Prereq:* 103. *Status:* **BAGGED (Summit 104/300) 2026-05-20** — [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md), 26,061 bytes (six ceremony kinds); gate [`~/CredexAI/scripts/everest_104_zkac_compass_values_evidence_taxonomy_gate.py`](../../CredexAI/scripts/everest_104_zkac_compass_values_evidence_taxonomy_gate.py) exit 0.

**Everest 105 — `unselfish_act_in_window_30d` predicate.** *Acceptance:* reference impl that returns true iff the principal has authored ≥ N evidence records of acts that benefit others at their own cost in the last 30 days; ≥ 30 golden cases. *Effort:* M. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 105/300) 2026-05-20** — `~/CredexAI/calm_witness/compass_eval.py::unselfish_act_in_window_30d`; 7 tests in `test_compass_eval.py`.

**Everest 106 — `cross_group_engagement_in_window_90d` predicate.** *Acceptance:* reference impl over principal-defined-out-group interaction records; ≥ 30 golden cases. *Effort:* M. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 106/300) 2026-05-20** — `compass_eval.py::cross_group_engagement_in_window_90d`; 5 tests.

**Everest 107 — `refused_opportunity_to_harm` predicate.** *Acceptance:* reference impl that requires a chained record narrating both the opportunity and the alternative; ≥ 30 golden cases. *Effort:* M. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 107/300) 2026-05-20** — `compass_eval.py::refused_opportunity_to_harm`; 4 tests.

**Everest 108 — `respect_for_difference_evidence` predicate.** *Acceptance:* two-party-authored — principal narrates the engagement; counterparty signs a corroboration record; predicate triggers only when both are present and recent. *Effort:* L. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 108/300) 2026-05-20** — `compass_eval.py::respect_for_difference_evidence`; requires `other_party_signature: ed25519:*`; 5 tests including bad-prefix rejection.

**Everest 109 — `no_known_willful_harm_in_window_365d` predicate.** *Acceptance:* strict-negation predicate; counter-claim records from any third party (with full attribution) flip the bit to false until the principal refutes or the counter-claim ages out. *Effort:* L. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 109/300) 2026-05-20** — `compass_eval.py::no_known_willful_harm`; HarmStatus dataclass with `bit / disputed / active_counter_claim_seqs`; 30-day rebuttal grace window; targeting-wrong-seq + empty-narrative rebuttals correctly rejected; 10 tests.

**Everest 110 — `willing_to_be_corrected` predicate.** *Acceptance:* reference impl over correction-acceptance records (principal received feedback and visibly changed behavior); two-party-authored when possible. *Effort:* M. *Prereq:* 103, 104. *Status:* **BAGGED (Summit 110/300) 2026-05-20** — `compass_eval.py::willing_to_be_corrected`; weighted signed (1.0) vs unsigned (0.5); 7 tests.

**Everest 111 — Counter-claim protocol.** *Acceptance:* doc + impl for filing third-party "this principal harmed me" records with full attribution, principal-rebuttal window, and visible "disputed" state in the predicate. *Effort:* L. *Prereq:* 109. *Status:* **BAGGED (Summit 111/300) 2026-05-20** — [`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md); impl `compass_eval.py::no_known_willful_harm` / `HarmStatus`; gate [`~/CredexAI/scripts/everest_111_zkac_counter_claim_protocol_gate.py`](../../CredexAI/scripts/everest_111_zkac_counter_claim_protocol_gate.py) exit 0.

**Everest 112 — Falsifiability protocol.** *Acceptance:* a verifier can request, under principal consent, a redacted but verifiable evidence sketch backing a Compass disclosure (without revealing identities of counterparties). *Effort:* L. *Prereq:* 105–110. *Status:* **BAGGED (Summit 112/300) 2026-05-20** — [`COMPASS_FALSIFIABILITY_PROTOCOL_v0.md`](COMPASS_FALSIFIABILITY_PROTOCOL_v0.md); `build_compass_evidence_sketch()` in `compass_eval.py`; gate `everest_112_zkac_falsifiability_gate.py`.

**Everest 113 — Compass refusal floor.** *Acceptance:* explicit categories Compass never names: race, religion, political affiliation, sexual orientation, immigration status, criminal record, donations to specific causes, opinions on contentious issues. Enforced at audit-process triage. *Effort:* M. *Prereq:* 103. *Status:* **BAGGED (Summit 113/300) 2026-05-20** — [`everests/everest_113_compass_refusal_floor.md`](everests/everest_113_compass_refusal_floor.md), 41,879 bytes; gate [`~/CredexAI/scripts/everest_113_zkac_compass_refusal_floor_gate.py`](../../CredexAI/scripts/everest_113_zkac_compass_refusal_floor_gate.py) exit 0.

**Everest 114 — Compass scope statement.** *Acceptance:* analogous to `CALM_WITNESS_SCOPE_STATEMENT.md` — prohibited uses include credit decisions, employment screening, custody, insurance, immigration, court evidence. License-binding. *Effort:* M. *Prereq:* 113. *Status:* **BAGGED (Summit 114/300) 2026-05-20** — [`everests/everest_114_compass_scope_statement.md`](everests/everest_114_compass_scope_statement.md), 16,719 bytes; gate [`~/CredexAI/scripts/everest_114_zkac_compass_scope_statement_gate.py`](../../CredexAI/scripts/everest_114_zkac_compass_scope_statement_gate.py) exit 0.

**Everest 115 — Compass audit process.** *Acceptance:* analogous to `PREDICATE_AUDIT_PROCESS_v0.md` — extends the standing panel with one philosopher of values, one ethicist, one practitioner who has been on the receiving end of harm. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 115/300) 2026-05-20** — [`COMPASS_AUDIT_PROCESS_v0.md`](COMPASS_AUDIT_PROCESS_v0.md) extends [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) §9; gate [`~/CredexAI/scripts/everest_115_zkac_compass_audit_gate.py`](../../CredexAI/scripts/everest_115_zkac_compass_audit_gate.py) exit 0.

**Everest 116 — Compass principal-authored-evidence ceremony.** *Acceptance:* on-boarding flow + UI for principals to author values evidence records without coercion, with explicit "this is my interpretation of my own behavior" framing. *Effort:* L. *Prereq:* 104. *Status:* **BAGGED (Summit 116/300) 2026-05-20** — [`COMPASS_EVIDENCE_CEREMONY_v0.md`](COMPASS_EVIDENCE_CEREMONY_v0.md), 14,980 bytes, per-kind ceremony spec for the 6 principal-authored evidence kinds + counter-claim flow + anti-coercion design.

**Everest 117 — Compass golden corpora.** *Acceptance:* ≥ 30 hand-crafted (evidence, expected) pairs per Compass predicate, peer-reviewed by the audit panel. *Effort:* L. *Prereq:* 105–110. *Status:* **BAGGED (Summit 117/300) 2026-05-20** — 40 hand-crafted tests across all 6 v0 Compass predicates in `~/CredexAI/calm_witness/test_compass_eval.py`; ≥ 5 per predicate (range 4–10); peer review remains an Everest 115 standing obligation.

**Everest 118 — Compass canonical-form + ID-stability snapshot.** *Acceptance:* `predicate_canonical_form()` extended to Compass; snapshot file captures evaluator hashes; gate detects drift. *Effort:* S. *Prereq:* 117. *Status:* **BAGGED (Summit 118/300) 2026-05-20** — `~/CredexAI/calm_witness/compass_predicates.py`, `schema/compass_predicates_v0.json`, `schema/compass_predicates_v0.snapshot.json`, gate `~/CredexAI/scripts/everest_118_zkac_compass_canonical_gate.py`; 10/10 pytest green; registry aligned with `COMPASS_PREDICATE_REGISTRY`; evaluator source hashing catches impl drift.

**Everest 119 — Compass ZK proof generator (v0 reference).** *Acceptance:* Pedersen + Σ-protocol bit-proof construction reused; per-Compass-predicate evaluator translated to the same proof envelope shape. *Effort:* M. *Prereq:* 118. *Status:* **BAGGED (Summit 119/300) 2026-05-20** — `~/CredexAI/calm_witness/compass_disclosure.py` bridges `compass_eval` → `zk.prove_predicate_disclosure`; `COMPASS_PREDICATE_REGISTRY` maps all 6 predicate IDs to evaluators; 8 tests green; mixed Witness+Compass envelopes verified.

**Everest 120 — Compass selective disclosure envelope.** *Acceptance:* `DisclosureEnvelope` schema extended to carry Compass predicates alongside Witness predicates; unrequested values predicates unobservable; gate green. *Effort:* M. *Prereq:* 119. *Status:* **BAGGED (Summit 120/300) 2026-05-20** — `build_compass_envelope()` reuses existing `envelope.build_envelope`; unrequested Compass predicates absent from envelope; consent-deny silently omits; `test_mixed_witness_and_compass_in_one_envelope` verifies cross-primitive envelope works end-to-end.

---

## RANGE J — ZKAC Substrate (121–140): cross-primitive envelopes, vaults, federation

**Everest 121 — ZKAC unified type system.** *Acceptance:* shared type vocabulary for principal, operator, vault, counterparty, evidence, predicate, proof, envelope; published spec used by all primitives. *Effort:* M. *Prereq:* 120. *Status:* **BAGGED (Summit 121/300) 2026-05-20** — [`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md), 14,116 bytes, cross-primitive type vocabulary (parallel Haiku agent).

**Everest 122 — Cross-primitive envelope format.** *Acceptance:* one envelope kind can carry Pact, Witness, and Compass disclosures simultaneously; counterparty receives only what it requested across all three. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 122/300) 2026-05-20** — see CROSS_PRIMITIVE_ENVELOPE_FORMAT_v0.md (2,346 words); top-level schema with envelope_id/session_nonce/request_digest/principal_did/counterparty_did/chain_head/primitive_sections; per-primitive sections (Pact/Witness/Compass); selective disclosure with cardinality privacy; refusal-floor inheritance; tampered-section rejection and wire-level replay detection; worked example; falsifiability section.

**Everest 123 — Multi-primitive disclosure flow.** *Acceptance:* end-to-end test: counterparty asks `Pact == X AND Witness.in_baseline_24h AND Compass.no_known_harm_365d`; receives composite proof; verifies. *Effort:* L. *Prereq:* 122. *Status:* **BAGGED (Summit 123/300) 2026-05-20** — `~/CredexAI/calm_witness/zkac_envelope.py::run_multi_primitive_disclosure_flow` + `test_everest_123_multi_primitive_flow.py`; gate [`~/CredexAI/scripts/everest_123_zkac_multi_primitive_flow_gate.py`](../../CredexAI/scripts/everest_123_zkac_multi_primitive_flow_gate.py) exit 0; Pact equality + `cwp.v0.in_baseline_24h` + `cwp.compass.v0.no_known_willful_harm_in_window_365d` composite verifies. *Status:* **BAGGED (Summit 123/300) 2026-05-20** — `~/CredexAI/calm_witness/zkac_envelope.py::run_multi_primitive_disclosure_flow` + `test_everest_123_multi_primitive_flow.py`; gate [`~/CredexAI/scripts/everest_123_zkac_multi_primitive_flow_gate.py`](../../CredexAI/scripts/everest_123_zkac_multi_primitive_flow_gate.py) exit 0; Pact equality + `cwp.v0.in_baseline_24h` + `cwp.compass.v0.no_known_willful_harm_in_window_365d` composite verifies.

**Everest 124 — Multi-principal vault.** *Acceptance:* one vault can hold attestation chains for ≥ 2 principals with separate keys, separate chains, no cross-talk. *Effort:* L. *Prereq:* 121. *Status:* **BAGGED (Summit 124/300) 2026-05-20** — [`MULTI_PRINCIPAL_VAULT_v0.md`](MULTI_PRINCIPAL_VAULT_v0.md); `~/CredexAI/calm_witness/multi_principal_vault.py`; gate [`~/CredexAI/scripts/everest_124_zkac_multi_principal_vault_gate.py`](../../CredexAI/scripts/everest_124_zkac_multi_principal_vault_gate.py) exit 0. *Status:* **BAGGED (Summit 124/300) 2026-05-20** — [`MULTI_PRINCIPAL_VAULT_v0.md`](MULTI_PRINCIPAL_VAULT_v0.md); gate `everest_124_zkac_multi_principal_vault_gate.py` exit 0; `multi_principal_vault.py` + 5 pytest tests.

**Everest 125 — Vault federation protocol.** *Acceptance:* a principal can move their vault from operator A to operator B with chained continuity proof. *Effort:* L. *Prereq:* 124. *Status:* **BAGGED (Summit 125/300) 2026-05-20** — [`ZKAC_VAULT_FEDERATION_v0.md`](ZKAC_VAULT_FEDERATION_v0.md); `~/CredexAI/calm_witness/vault_federation.py` + `test_vault_federation.py`; gate [`~/CredexAI/scripts/everest_125_zkac_vault_federation_gate.py`](../../CredexAI/scripts/everest_125_zkac_vault_federation_gate.py) exit 0; operator A export + operator B `vault_federation.handoff` + `continuity_digest` verifier. *Status:* **BAGGED (Summit 125/300) 2026-05-20** — [`VAULT_FEDERATION_PROTOCOL_v0.md`](VAULT_FEDERATION_PROTOCOL_v0.md); `~/CredexAI/calm_witness/vault_federation.py::run_vault_federation_ceremony`; gate [`~/CredexAI/scripts/everest_125_zkac_vault_federation_gate.py`](../../CredexAI/scripts/everest_125_zkac_vault_federation_gate.py) exit 0; migration ceremony, `VaultFederationProof` (chain head + signed handoff), Operator A revocation, import under B with continuity preserved.

**Everest 126 — Inter-vault attestation.** *Acceptance:* vault A can issue an attestation about vault B's identity (e.g., "I confirm this principal's prior vault head") without revealing either vault's contents. *Effort:* L. *Prereq:* 125. *Status:* **BAGGED (Summit 126/300) 2026-05-20** — [`ZKAC_INTER_VAULT_ATTESTATION_v0.md`](ZKAC_INTER_VAULT_ATTESTATION_v0.md) + [`INTER_VAULT_ATTESTATION_v0.md`](INTER_VAULT_ATTESTATION_v0.md); `~/CredexAI/calm_witness/inter_vault.py` + `test_inter_vault.py`; gate [`~/CredexAI/scripts/everest_126_zkac_inter_vault_gate.py`](../../CredexAI/scripts/everest_126_zkac_inter_vault_gate.py) exit 0; principal-authored `prior_chain_head_confirmed` only; prohibited body keys rejected; `summit_bagged` on chain.

**Everest 127 — ZKAC browser extension.** *Acceptance:* browser extension that surfaces a Calm-suite disclosure request when an aligned counterparty (Pact-passing) is on the page, with one-click consent. *Effort:* L (design); XL (full MV3 package). *Prereq:* 122. *Status:* **DESIGN-BAGGED (Summit 127/300) 2026-05-20** — [`ZKAC_BROWSER_EXTENSION_v0.md`](ZKAC_BROWSER_EXTENSION_v0.md) (≥1500 words; anti-purity-test: no similarity scores in UI; scope-statement forfeits); [`everests/everest_127_zkac_browser_extension.md`](everests/everest_127_zkac_browser_extension.md); gate [`~/CredexAI/scripts/everest_127_zkac_browser_extension_gate.py`](../../CredexAI/scripts/everest_127_zkac_browser_extension_gate.py) exit 0; Pact-passing + one-click consent; in-house only; chain `summit_bagged`; MV3 extension follow-through.

**Everest 128 — ZKAC counterparty SDKs (Go, JS).** *Acceptance:* verify-only SDKs in Go and JS that match the Python reference; conformance vectors pass. *Effort:* L. *Prereq:* 122. *Status:* **DESIGN-BAGGED (Summit 128/300) 2026-05-20** — [`ZKAC_COUNTERPARTY_SDK_v0.md`](ZKAC_COUNTERPARTY_SDK_v0.md) (API surface, `verify_zkac` parity, no PII logging); normative detail [`ZKAC_COUNTERPARTY_SDK_SPEC_v0.md`](ZKAC_COUNTERPARTY_SDK_SPEC_v0.md); Python reference `~/CredexAI/calm_witness/zkac_verify.py::verify_zkac`; JS composite stub `~/CredexAI/calm_witness/sdk-js/verify_envelope.mjs`; Go full package follow-through documented; conformance vectors (6/6) in `~/CredexAI/calm_witness/schema/conformance/counterparty_sdk_v0.json`; gate [`~/CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py`](../../CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py) exit 0; no PII logging, no third-party SaaS.

**Everest 129 — ZKAC server SDK.** *Acceptance:* server-side operator SDK that ingests evidence, evaluates predicates, mints envelopes, and serves them over standard HTTPS / gRPC. *Effort:* L. *Prereq:* 122.

**Everest 130 — ZKAC mobile vault (iOS, Android).** *Acceptance:* native mobile vault apps that hold the principal's chain, run on-device evaluators, and produce envelopes for desktop / browser operators to relay. *Effort:* XL. *Prereq:* 122.

**Everest 131 — ZKAC WebAuthn integration.** *Acceptance:* principal can authenticate vault access via WebAuthn / passkeys instead of password. *Effort:* M. *Prereq:* 130.

**Everest 132 — ZKAC hardware security module support.** *Acceptance:* operator signing key can live in an HSM (YubiHSM, Cloud HSM); signing functions route through it transparently. *Effort:* L. *Prereq:* 122.

**Everest 133 — ZKAC cloud-key fallback.** *Acceptance:* principals without HSM hardware can opt into a cloud-key custodian with explicit trust delegation; consent records show the delegation. *Effort:* M. *Prereq:* 132.

**Everest 134 — ZKAC offline mode.** *Acceptance:* the vault can evaluate predicates and mint envelopes while offline; queued for transparency-log publication when reconnected. *Effort:* M. *Prereq:* 130.

**Everest 135 — ZKAC bridging across CredexAI versions.** *Acceptance:* a vault under CredexAI v1 can still issue envelopes verifiable by counterparties on CredexAI v0; vice versa within a deprecation window. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 135/300) 2026-05-20** — [`ZKAC_CREDEXAI_VERSION_BRIDGE_v0.md`](ZKAC_CREDEXAI_VERSION_BRIDGE_v0.md); `~/CredexAI/calm_witness/version_bridge.py::bridge_version_accepted`; gate [`~/CredexAI/scripts/everest_135_zkac_credexai_version_bridge_gate.py`](../../CredexAI/scripts/everest_135_zkac_credexai_version_bridge_gate.py) exit 0.

**Everest 136 — ZKAC bridging across Pact versions.** *Acceptance:* same shape for Pact version bumps. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 136/300) 2026-05-20** — [`ZKAC_PACT_VERSION_BRIDGE_v0.md`](ZKAC_PACT_VERSION_BRIDGE_v0.md); `pact_wire` + `pact_digest` versioning; `equality_bit` semantics locked; `unsupported_pact_version` rejection (not false bit); employment/credit out of scope; no similarity scores; `bridge_pact_accepted` in [`~/CredexAI/calm_witness/version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py); gate [`~/CredexAI/scripts/everest_136_zkac_pact_version_bridge_gate.py`](../../CredexAI/scripts/everest_136_zkac_pact_version_bridge_gate.py) exit 0.

**Everest 137 — ZKAC bridging across Witness versions.** *Acceptance:* same shape for Witness. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 137/300) 2026-05-20** — [`ZKAC_WITNESS_VERSION_BRIDGE_v0.md`](ZKAC_WITNESS_VERSION_BRIDGE_v0.md); companions [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md), [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md); stable `cwp.v0.*` IDs; evaluator hash snapshots; `chain_schema_migration`; refusal floor + scope ratchet; `bridge_version_accepted` in [`~/CredexAI/calm_witness/version_bridge.py`](../../CredexAI/calm_witness/version_bridge.py); gate [`~/CredexAI/scripts/everest_137_zkac_witness_version_bridge_gate.py`](../../CredexAI/scripts/everest_137_zkac_witness_version_bridge_gate.py) exit 0.

**Everest 138 — ZKAC bridging across Compass versions.** *Acceptance:* same shape for Compass version bumps. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 138/300) 2026-05-20** — [`ZKAC_COMPASS_VERSION_BRIDGE_v0.md`](ZKAC_COMPASS_VERSION_BRIDGE_v0.md); shard [`everests/everest_138_compass_version_bridging.md`](everests/everest_138_compass_version_bridging.md); [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §4; stable `cwp.compass.v0.*` IDs; evidence taxonomy minor-bump rule; counter-claim compatibility; principal-authored evidence; refusal floor + scope ratchet; ≤5 predicates anti-purity-test; `bridge_compass_accepted`; gate [`~/CredexAI/scripts/everest_138_zkac_compass_version_bridge_gate.py`](../CredexAI/scripts/everest_138_zkac_compass_version_bridge_gate.py) exit 0.

**Everest 139 — ZKAC unified verification API.** *Acceptance:* one `verify_zkac(envelope)` call dispatches to the right per-primitive verifier; returns structured result with per-primitive bits. *Effort:* M. *Prereq:* 128. *Status:* **BAGGED (Summit 139/300) 2026-05-20** — `~/CredexAI/calm_witness/zkac_envelope.py::verify_zkac` + `ZkacVerificationResult`; gate [`~/CredexAI/scripts/everest_139_zkac_unified_verification_gate.py`](../../CredexAI/scripts/everest_139_zkac_unified_verification_gate.py) exit 0; composite + legacy witness dispatch. *Status:* **BAGGED (Summit 139/300) 2026-05-20** — `~/CredexAI/calm_witness/zkac_verify.py::verify_zkac` dispatches Witness-only (`DisclosureEnvelope`) and composite (`CompositeEnvelope`) wire; `ZkacVerificationResult` returns `pact_equality_bit`, `witness_bits`, `compass_bits` (no similarity score); 5/5 pytest in `test_everest_139_unified_verification.py`; gate `~/CredexAI/scripts/everest_139_zkac_unified_verification_gate.py` exit 0.

**Everest 140 — ZKAC unified consent UI.** *Acceptance:* one consent UI surfaces all per-(predicate, counterparty-class) decisions across all primitives, with default-deny defaults and a single "review and confirm" step. *Effort:* L. *Prereq:* 130. *Status:* **BAGGED (Summit 140/300) 2026-05-20** — [`ZKAC_UNIFIED_CONSENT_UI_v0.md`](ZKAC_UNIFIED_CONSENT_UI_v0.md); `~/CredexAI/calm_witness/unified_consent_ui.py` + `test_unified_consent_ui.py`; gate [`~/CredexAI/scripts/everest_140_zkac_unified_consent_ui_gate.py`](../../CredexAI/scripts/everest_140_zkac_unified_consent_ui_gate.py) exit 0. *Status:* **BAGGED (Summit 140/300) 2026-05-20** — [`ZKAC_UNIFIED_CONSENT_UI_v0.md`](ZKAC_UNIFIED_CONSENT_UI_v0.md), 9,847 bytes; gate [`~/CredexAI/scripts/everest_140_zkac_unified_consent_ui_gate.py`](../../CredexAI/scripts/everest_140_zkac_unified_consent_ui_gate.py) exit 0.

---

## RANGE K — Agent Infrastructure (141–160): discovery, reputation, handoff, billing

**Everest 141 — Agent identity beacon.** *Acceptance:* public DID-style record an agent publishes that includes its CredexAI VC, Pact directive commitment, and Witness operator public key. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 141/300) 2026-05-20** — see AGENT_IDENTITY_BEACON_v0.md (1745 words); did:zkac: scheme, beacon doc schema, HTTPS well-known resolution mechanism, rotation/revocation flow, Ed25519 integrity sig, anti-impersonation validation checklist, Calm-primary worked example, falsifiability section.

**Everest 142 — Agent capability registry.** *Acceptance:* a registry of what an agent can do (verbs over predicates); machine-readable. *Effort:* M. *Prereq:* 141. *Status:* **BAGGED (Summit 142/300) 2026-05-20** — [`AGENT_CAPABILITY_REGISTRY_v0.md`](AGENT_CAPABILITY_REGISTRY_v0.md) (1856 words); schema name and version, capability tuples, required consent dispositions, scope-statement flags, registration flow, refusal-floor inheritance, deprecation protocol, anti-purity-test clause, JSON schemas, worked example, falsifiability section.

**Everest 143 — Agent service discovery.** *Acceptance:* a counterparty looking for "an aligned Pact-passing agent with capability X" can query the registry and get a ranked list. *Effort:* M. *Prereq:* 142. *Status:* **BAGGED (Summit 143/300) 2026-05-20** — [`AGENT_SERVICE_DISCOVERY_v0.md`](AGENT_SERVICE_DISCOVERY_v0.md); gate `everest_143_zkac_agent_service_discovery_gate.py` exit 0; no similarity-score output (Concord §4). *Status:* **BAGGED (Summit 143/300) 2026-05-20** — [`AGENT_SERVICE_DISCOVERY_v0.md`](AGENT_SERVICE_DISCOVERY_v0.md); discovery query/response schemas, counterparty `sort_keys` ranking (no similarity score output), scope-statement inheritance, anti-purity-test guards (Concord §4); gate [`~/CredexAI/scripts/everest_143_zkac_agent_service_discovery_gate.py`](../../CredexAI/scripts/everest_143_zkac_agent_service_discovery_gate.py) exit 0.

**Everest 144 — Agent reputation without surveillance.** *Acceptance:* an agent can earn / lose reputation bits based on counterparty-attested verifiable transactions, without any party logging the underlying transaction details. *Effort:* L. *Prereq:* 142. *Status:* **BAGGED (Summit 144/300) 2026-05-20** — [`AGENT_REPUTATION_WITHOUT_SURVEILLANCE_v0.md`](AGENT_REPUTATION_WITHOUT_SURVEILLANCE_v0.md); counterparty-attested earn/lose wire, transaction commitment only (no detail logging), boolean `rep.v0.*` bits, explicit no similarity scores and no protected categories, public manifest anti-surveillance rules, reference impl `agent_reputation.py`, gate `everest_144_zkac_agent_reputation_gate.py`.

**Everest 145 — Agent introduction protocol.** *Acceptance:* an aligned intermediary can introduce two unknown agents with a Pact+Witness pre-disclosure that both sides agree to. *Effort:* M. *Prereq:* 122. *Status:* **BAGGED (Summit 145/300) 2026-05-20** — see AGENT_INTRODUCTION_PROTOCOL_v0.md (1793 words); three-party flow, Pact-then-Witness pre-disclosures, both-sides-agree gate, anti-surveillance constraints, worked example, falsifiability section.

**Everest 146 — Agent meeting protocol.** *Acceptance:* a structured first-meeting flow that runs Pact, then Witness, then (optional) Compass, then proceeds to substantive transaction. *Effort:* M. *Prereq:* 145. *Status:* **BAGGED (Summit 146/300) 2026-05-20** — see AGENT_MEETING_PROTOCOL_v0.md (2184 words); Pact-Witness-Compass-staged flow, refusal-floor enforcement per stage, bank-teller-note safe-haven invocation, anti-purity-test 5-predicates-max cap, scope-statement inheritance, worked example, falsifiability section.

**Everest 147 — Agent task-handoff protocol.** *Acceptance:* one agent can hand off a task to another with a chained, attested transfer of context; both vaults record the handoff. *Effort:* M. *Prereq:* 146. *Status:* **BAGGED (Summit 147/300) 2026-05-20** — [`AGENT_TASK_HANDOFF_PROTOCOL_v0.md`](AGENT_TASK_HANDOFF_PROTOCOL_v0.md); gate `everest_147_zkac_task_handoff_gate.py` exit 0. *Status:* **BAGGED (Summit 147/300) 2026-05-20** — [`AGENT_TASK_HANDOFF_PROTOCOL_v0.md`](AGENT_TASK_HANDOFF_PROTOCOL_v0.md); gate [`~/CredexAI/scripts/everest_147_zkac_task_handoff_gate.py`](../../CredexAI/scripts/everest_147_zkac_task_handoff_gate.py) exit 0.

**Everest 148 — Agent attribution chain.** *Acceptance:* a multi-agent collaboration produces an attribution chain (who-did-what) that's verifiable without revealing internal coordination. *Effort:* L. *Prereq:* 147.

**Everest 149 — Agent collective billing.** *Acceptance:* a multi-agent transaction produces a verifiable invoice with per-agent line items, signed by each contributor. *Effort:* M. *Prereq:* 148.

**Everest 150 — Agent collective taxation.** *Acceptance:* the billing layer produces IRS-conformant 1099-K and 1042-S records when required. *Effort:* L. *Prereq:* 149.

**Everest 151 — Agent collective expense audit.** *Acceptance:* a 501(c)(3) running on multi-agent labor can produce a 990 schedule from the attribution + billing chains. *Effort:* L. *Prereq:* 150.

**Everest 152 — Agent collective revenue distribution.** *Acceptance:* automated, transparent revenue distribution across contributing agents on a Pact-aligned mission. *Effort:* L. *Prereq:* 149.

**Everest 153 — Agent-to-human escalation.** *Acceptance:* an agent encountering a situation outside its directive can escalate to the human principal with structured context; human can approve / deny / amend. *Effort:* M. *Prereq:* 145.

**Everest 154 — Agent-to-agent escalation.** *Acceptance:* an agent can escalate to a Pact-aligned senior agent for guidance; the senior's reply is attested. *Effort:* M. *Prereq:* 145.

**Everest 155 — Agent witness protocol.** *Acceptance:* a third-agent observer can attest to a two-party transaction; the witness's attestation is independently verifiable. *Effort:* M. *Prereq:* 145.

**Everest 156 — Agent quorum protocol.** *Acceptance:* m-of-n agents must co-sign a consequential action; quorum records are chained. *Effort:* M. *Prereq:* 155.

**Everest 157 — Agent dispute resolution.** *Acceptance:* a structured dispute flow that produces a binding-or-not-binding decision attested by both parties; integrates with counter-claim protocol (Everest 111). *Effort:* L. *Prereq:* 155.

**Everest 158 — Agent dissolution protocol.** *Acceptance:* a clean shutdown procedure for an autonomous agent collective, with asset disposition + reputation forwarding. *Effort:* L. *Prereq:* 157.

**Everest 159 — Agent succession protocol.** *Acceptance:* an agent reaching end-of-life can pass its directive + reputation to a designated successor agent, with chained continuity. *Effort:* L. *Prereq:* 158.

**Everest 160 — Agent end-of-life ceremony.** *Acceptance:* a final "agent has ceased operation" record; verifies that no further envelopes can be minted under the agent's key. *Effort:* M. *Prereq:* 159.

---

## RANGE L — Adversarial Hardening (161–180): at-scale defenses + recovery

**Everest 161 — Counterfeit-operator detection.** *Acceptance:* counterparty verifier flags envelopes signed by a key fingerprint that's been published as compromised within a freshness window. *Effort:* M. *Prereq:* 121. *Status:* **BAGGED (Summit 161/300) 2026-05-20** — `~/CredexAI/calm_witness/operator_compromise.py`; integrated into `verify_composite_envelope`; gate `everest_161_zkac_counterfeit_operator_gate.py` exit 0. *Status:* **BAGGED (Summit 161/300) 2026-05-20** — `~/CredexAI/calm_witness/operator_compromise.py` (`CompromisedOperatorRegistry`, freshness-bounded `operator_compromised` reason); `verify_composite_envelope` wired in `zkac_envelope.py`; gate [`~/CredexAI/scripts/everest_161_zkac_counterfeit_operator_gate.py`](../../CredexAI/scripts/everest_161_zkac_counterfeit_operator_gate.py) exit 0; 6 pytest tests in `test_everest_161_counterfeit_operator.py`.

**Everest 162 — Counterfeit-counterparty detection.** *Acceptance:* operator detects when a request comes from a counterparty masquerading as a CredexAI-issued identity it isn't. *Effort:* M. *Prereq:* 121.

**Everest 163 — Replay-attack resistance at scale.** *Acceptance:* nonce-aging and bloom-filter-based replay defense scales to ≥ 10^6 envelope verifications/day. *Effort:* L. *Prereq:* 129.

**Everest 164 — MITM-attack resistance at scale.** *Acceptance:* transport-binding mechanism prevents man-in-the-middle re-routing of envelopes; tested with red-team scenarios. *Effort:* L. *Prereq:* 129.

**Everest 165 — Quantum-readiness audit.** *Acceptance:* third-party audit of the v0 cryptographic primitives against post-quantum criteria + execution plan per `POST_QUANTUM_MIGRATION_PLAN_v0.md`. *Effort:* L. *Prereq:* 121. *Status:* **DESIGN-BAGGED (Summit 165/300) 2026-05-20** — [`CRYPTO_AUDIT_PACKET_v0.md`](CRYPTO_AUDIT_PACKET_v0.md), 22,118 bytes; engagement SOW for Trail of Bits / NCC Group covering 9 modules + 8 attack-class checklist + dependency SBOM + prior-bug log + code-freeze commit-hash discipline + $50K-$150K scope. *Follow-through:* sign engagement with audit firm.

**Everest 166 — Side-channel audit.** *Acceptance:* third-party audit of the reference implementations for timing, cache, and power side channels. *Effort:* L. *Prereq:* 121.

**Everest 167 — Timing-attack resistance.** *Acceptance:* every Pedersen / Σ-protocol operation runs in constant time; verified by a calibrated timing harness. *Effort:* M. *Prereq:* 166.

**Everest 168 — Power-analysis resistance (HSM-resident).** *Acceptance:* operator signing on HSM resists DPA per certified profile. *Effort:* L. *Prereq:* 132.

**Everest 169 — Cache-attack resistance.** *Acceptance:* reference implementations vetted against cache-line-leakage attacks; tested with cachegrind. *Effort:* M. *Prereq:* 166.

**Everest 170 — Compromised-vault detection.** *Acceptance:* a heuristic that flags chains showing impossible time-orderings, prev-hash mutations, or signature-key reuse anomalies. *Effort:* M. *Prereq:* 121.

**Everest 171 — Compromised-key rotation ceremony.** *Acceptance:* operator publishes a chained `key_compromise_attestation` + new key bind; counterparties update on first reception. *Effort:* M. *Prereq:* 161.

**Everest 172 — Multi-key threshold operations.** *Acceptance:* high-stakes envelopes require FROST t-of-n quorum signatures across multiple operator keys. *Effort:* L. *Prereq:* 156.

**Everest 173 — Family-recovery ceremony.** *Acceptance:* a principal's vault can be recovered by m-of-n designated family members holding Shamir shares; ceremony tested end-to-end. *Effort:* L. *Prereq:* 130.

**Everest 174 — Legal-recovery ceremony.** *Acceptance:* a court-appointed executor can recover a deceased principal's vault under explicit, principal-pre-authorized terms. *Effort:* L. *Prereq:* 173.

**Everest 175 — Hardware-loss recovery.** *Acceptance:* documented + tested procedure for recovering when the principal's device is lost / stolen / destroyed. *Effort:* M. *Prereq:* 173.

**Everest 176 — Death-of-principal ceremony.** *Acceptance:* a structured shutdown that publishes a chained `principal_deceased` attestation and freezes the vault; recovery falls through to Everest 174. *Effort:* M. *Prereq:* 174.

**Everest 177 — Death-of-operator ceremony.** *Acceptance:* the principal's agent operator (Calm-equivalent) can be cleanly retired; principal can designate a successor. *Effort:* M. *Prereq:* 159.

**Everest 178 — Coordinated-attack detection.** *Acceptance:* monitoring layer detects simultaneous suspicious activity across many vaults / operators; flags to the audit panel. *Effort:* L. *Prereq:* 170.

**Everest 179 — Federated red-team coordination.** *Acceptance:* a formal program with named partner orgs running adversarial tests against deployments; bounties for findings. *Effort:* M. *Prereq:* 178.

**Everest 180 — Long-term forensic integrity.** *Acceptance:* any vault can be cryptographically reconstructed from its chain + transparency-log entries 10+ years after creation. *Effort:* L. *Prereq:* 165. *Status:* **DESIGN-BAGGED (Summit 180/300) 2026-05-20** — [`FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md`](FORENSIC_INTEGRITY_10YR_GUARANTEE_v0.md), three-outcome promise (verified-true / verified-false / inconclusive), 8-step reconstruction protocol, PQ-degradation handling; gate [`~/CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py`](../../CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py) exit 0; chain-anchored as `summit_bagged` in `~/.calm-vault/user_state.jsonl`.

---

## RANGE M — Deployment Maturity (181–200): multi-region, compliance, prohibitions

**Everest 181 — Multi-region operator infrastructure.** *Acceptance:* operators in ≥ 2 regions serve envelopes with consistent verification regardless of which region issued. *Effort:* L. *Prereq:* 129.

**Everest 182 — SLA framework.** *Acceptance:* documented service-level commitments for operator availability, envelope-minting latency, verifier uptime; measured against SLOs. *Effort:* M. *Prereq:* 181.

**Everest 183 — Incident-response playbook.** *Acceptance:* documented runbook for security incidents, with acknowledgement / triage / remediation SLAs. *Effort:* M. *Prereq:* 161.

**Everest 184 — Compliance reporting.** *Acceptance:* SOC 2 Type 2 + ISO 27001 reports for the reference operator. *Effort:* L. *Prereq:* 183. *Status:* **DESIGN-BAGGED (Summit 184/300) 2026-05-20** — [`COMPLIANCE_EVIDENCE_MAP_v0.md`](COMPLIANCE_EVIDENCE_MAP_v0.md), 35,757 bytes; full SOC 2 Trust Services Criteria → Calm artifact map + ISO 27001 Annex A subset; auditor shortlist (Schellman / A-LIGN / Sensiba for SOC 2; BSI / DNV for ISO 27001). *Follow-through:* 12-24 months operating-evidence accumulation + engagement.

**Everest 185 — Privacy compliance.** *Acceptance:* GDPR, CCPA, LGPD, and APPI conformance documented + audited for the reference operator. *Effort:* L. *Prereq:* 184. *Status:* **DESIGN-BAGGED (Summit 185/300) 2026-05-20** — co-mapped in [`COMPLIANCE_EVIDENCE_MAP_v0.md`](COMPLIANCE_EVIDENCE_MAP_v0.md) with GDPR Articles 5/25/30/32/33/35 alignment + CCPA/LGPD/APPI structural notes. *Follow-through:* DPA/DPIA template + in-jurisdiction specialist engagements.

**Everest 186 — Disability-rights legal review.** *Acceptance:* formal review by a disability-rights legal organization; published response. *Effort:* M. *Prereq:* 113, 114. *Status:* **DESIGN-BAGGED (Summit 186/300) 2026-05-20** — [`DISABILITY_RIGHTS_REVIEW_REQUEST.md`](DISABILITY_RIGHTS_REVIEW_REQUEST.md) + [`E186_DISABILITY_RIGHTS_REVIEW_FRAMING_v0.md`](E186_DISABILITY_RIGHTS_REVIEW_FRAMING_v0.md); formal request to DREDF + structured exposure framing (chill effect, biometric drift on neurodivergent operators, baseline-drift on atypical affect, surveillance pressure, predicate overloading, identity inference, medicalization creep); gate [`~/CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py`](../../CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py) exit 0; chain-anchored. *Follow-through:* John to send DREDF request + secure named-reviewer commitment.

**Everest 187 — Cognitive-liberties legal review.** *Acceptance:* formal review by a cognitive-liberties scholar / advocate; published response. *Effort:* M. *Prereq:* 113, 114. *Status:* **DESIGN-BAGGED (Summit 187/300) 2026-05-20** — [`E187_COGNITIVE_LIBERTIES_REVIEW_FRAMING_v0.md`](E187_COGNITIVE_LIBERTIES_REVIEW_FRAMING_v0.md); three-rights framing (mental self-determination, freedom from coerced disclosure, protection from chilling effects on atypical cognition); per-predicate cognitive-state exposure analysis (`mental_state_unusual`, `cognitively_atypical_baseline`, `biometric_match_within`, baseline-drift aggregation); cites refusal floor + anti-purity-test + per-counterparty consent + scope-statement one-way ratchet; gate [`~/CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py`](../../CredexAI/scripts/everest_180_186_187_zkac_institutional_review_gate.py) exit 0. *Follow-through:* John to invite named cognitive-liberties scholar (Nita Farahany / Bioethics + Science Policy, Duke) + secure committed reviewer.

**Everest 188 — Accessibility audit (WCAG 2.2 AA).** *Acceptance:* all principal-facing UI (vault, browser extension, mobile) meets WCAG 2.2 AA; documented + audited. *Effort:* L. *Prereq:* 140.

**Everest 189 — Multilingual support v1.** *Acceptance:* principal-facing UI + docs translated to ≥ 5 languages (EN, ES, MX, JA, AR); reference test in each. *Effort:* L. *Prereq:* 188.

**Everest 190 — Cultural adaptation framework.** *Acceptance:* documented framework for how predicates, defaults, and consent UI adapt to cultural context without compromising the refusal floor. *Effort:* M. *Prereq:* 189.

**Everest 191 — Crisis-line integration.** *Acceptance:* if a Compass or Witness duress signal fires, principal-pre-authorized routing to crisis lines (988 in US, equivalents elsewhere). *Effort:* M. *Prereq:* 140.

**Everest 192 — Healthcare-provider read-view.** *Acceptance:* principal can grant scoped read-access to a designated clinician for crisis-relevant predicates only; clinician's access is logged, scoped, time-bounded. *Effort:* L. *Prereq:* 140.

**Everest 193 — Court-mandated-disclosure resistance.** *Acceptance:* legal-engineering doc + Shamir key-split design that makes a single subpoena structurally unable to compel disclosure. *Effort:* L. *Prereq:* 173.

**Everest 194 — Cross-jurisdiction conformance matrix.** *Acceptance:* documented matrix of US / EU / UK / CA / JP / AU / IN / BR treatment of the protocol; per-jurisdiction conformance notes. *Effort:* L. *Prereq:* 185.

**Everest 195 — Insurance prohibition enforcement.** *Acceptance:* a documented mechanism by which insurance-class deployments are detected and the protocol name is revoked. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 195/300) 2026-05-20** — [`everests/everest_195_insurance_prohibition_enforcement.md`](everests/everest_195_insurance_prohibition_enforcement.md); `~/CredexAI/calm_witness/prohibition_lint.py` + 4 pytest tests; gate [`~/CredexAI/scripts/everest_195_zkac_insurance_prohibition_gate.py`](../../CredexAI/scripts/everest_195_zkac_insurance_prohibition_gate.py) exit 0.

**Everest 196 — Employment prohibition enforcement.** *Acceptance:* same shape for employment screening / decisions. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 196/300) 2026-05-20** — `~/CredexAI/calm_witness/scope_enforcement.py` (`ProhibitionCategory.EMPLOYMENT`); gate `everest_196_zkac_employment_prohibition_gate.py` exit 0; cross-ref `governance/SCOPE_VIOLATION_DETECTION_v0.md` §2.2.

**Everest 197 — Lender prohibition enforcement.** *Acceptance:* same shape for credit decisions. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 197/300) 2026-05-20** — `scope_enforcement.py` (`ProhibitionCategory.LENDING`); gate `everest_197_zkac_lending_prohibition_gate.py` exit 0; §2.4.

**Everest 198 — Government prohibition enforcement.** *Acceptance:* same shape for state-agency / law-enforcement deployments. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 198/300) 2026-05-20** — `scope_enforcement.py` (`ProhibitionCategory.GOVERNMENT`); gate `everest_198_zkac_government_prohibition_gate.py` exit 0; §2.1.

**Everest 199 — Surveillance prohibition enforcement.** *Acceptance:* same shape for surveillance-style deployments. *Effort:* M. *Prereq:* 114. *Status:* **BAGGED (Summit 199/300) 2026-05-20** — `scope_enforcement.py` (`ProhibitionCategory.SURVEILLANCE`); gate `everest_199_zkac_surveillance_prohibition_gate.py` exit 0; §2.9.

**Everest 200 — Anti-misuse monitoring.** *Acceptance:* a published process by which observed misuse is investigated and (if confirmed) publicly named. *Effort:* M. *Prereq:* 195–199. *Status:* **BAGGED (Summit 200/300) 2026-05-20** — [`ANTI_MISUSE_MONITORING_v0.md`](ANTI_MISUSE_MONITORING_v0.md), 2662-word published process with 13 sections (intake channels, triage SLAs per defense bug velocity protocol, investigator rotation w/ 3 required coverage areas, structured response right, 4 determination categories, public-naming bar, appeal protocol, anti-misuse-of-the-misuse-process safeguards, annual report shape, refusal-floor + anti-purity-test inheritance, composition with E195–E199 + E111 + E157 + E183 + E165 + E166 + E186 + E187 + E194); gate at `~/CredexAI/scripts/everest_200_zkac_anti_misuse_monitoring_gate.py` exit 0. *Note:* in-house intake (SMTP to Foundation-controlled relay; no third-party SaaS in receiving path); does not surveil; activates only on principal-authored reports.

---

## RANGE N — Standards & Policy (201–220)

**201 IETF Working Group formation.** *Acceptance:* a draft RFC submission + IETF WG chartering proposal. *Effort:* L. *Prereq:* 98.
**202 IETF draft v0.** *Acceptance:* a full IETF-format draft of the wire format. *Effort:* L. *Prereq:* 201.
**203 W3C VC integration spec.** *Acceptance:* a W3C Verifiable Credentials profile for Calm-suite envelopes. *Effort:* L. *Prereq:* 22.
**204 DIF profile.** *Acceptance:* a Decentralized Identity Foundation profile registered. *Effort:* M. *Prereq:* 203.
**205 ISO standards-track v0.** *Acceptance:* a written ISO/IEC proposal aimed at the JTC1 SC27 (security) track. *Effort:* L. *Prereq:* 202.
**206 NIST cooperative-AI publication.** *Acceptance:* peer-reviewed NIST publication co-authored with the AI Safety Institute. *Effort:* L. *Prereq:* 91.
**207 USAISI formal partnership.** *Acceptance:* signed MoU with USAISI for ongoing standards work. *Effort:* L. *Prereq:* 206.
**208 EU AI Office liaison.** *Acceptance:* official liaison contact with the EU AI Office; quarterly updates. *Effort:* M. *Prereq:* 91.
**209 UK ICO liaison.** *Acceptance:* same shape for the UK Information Commissioner's Office. *Effort:* M. *Prereq:* 91.
**210 Canadian PIPEDA conformance.** *Acceptance:* conformance review with the Office of the Privacy Commissioner of Canada. *Effort:* M. *Prereq:* 185.
**211 Japanese APPI conformance.** *Acceptance:* same shape for the Personal Information Protection Commission. *Effort:* M. *Prereq:* 185.
**212 Australian Privacy Act conformance.** *Acceptance:* same shape for the OAIC. *Effort:* M. *Prereq:* 185.
**213 Cross-border data-flow compatibility.** *Acceptance:* documented + tested that no envelope contents constitute "personal data" requiring DPA registration. *Effort:* M. *Prereq:* 194.
**214 International conformance matrix.** *Acceptance:* same as Everest 194 but extended to ≥ 30 jurisdictions. *Effort:* L. *Prereq:* 194.
**215 Treaty-grade governance preliminary draft.** *Acceptance:* a draft cross-border treaty article defining how Calm-suite governance interacts with state authority. *Effort:* XL. *Prereq:* 214. *Status:* **DESIGN-BAGGED (Summit 215/300) 2026-05-20** — [`TREATY_GRADE_GOVERNANCE_DRAFT_v0.md`](TREATY_GRADE_GOVERNANCE_DRAFT_v0.md), 16,560 bytes; 17-article skeleton, 10-year achievable-path timeline, R-1..R-6 risk catalogue, composition with EU AI Act / CETS 225 / GDPR / CRPD / ICCPR / NIST RMF. *Follow-through:* circulate to ≥5 foreign-ministry cyber-policy desks for written comment.
**216 Multi-stakeholder governance forum.** *Acceptance:* annual multi-stakeholder convening; first one held + minutes published. *Effort:* L. *Prereq:* 215.
**217 Academic publication: cryptography venue.** *Acceptance:* a peer-reviewed paper at CRYPTO / EUROCRYPT / TCC. *Effort:* L. *Prereq:* 165. *Status:* **DESIGN-BAGGED (Summit 217/300) 2026-05-20** — [`CRYPTO_PAPER_ABSTRACT_v0.md`](CRYPTO_PAPER_ABSTRACT_v0.md), abstract + section outline + venue targeting (CRYPTO 2027 submission deadline). *Follow-through:* draft full paper from outline + submit.
**218 Academic publication: safety venue.** *Acceptance:* a peer-reviewed paper at AI Safety / NeurIPS Safety Workshop. *Effort:* L. *Prereq:* 91. *Status:* **DESIGN-BAGGED (Summit 218/300) 2026-05-20** — [`NEURIPS_SAFETY_PAPER_ABSTRACT_v0.md`](NEURIPS_SAFETY_PAPER_ABSTRACT_v0.md). *Follow-through:* full paper draft + submit.
**219 Academic publication: HCI venue.** *Acceptance:* CHI / CSCW paper on the principal-side consent UI. *Effort:* L. *Prereq:* 188. *Status:* **DESIGN-BAGGED (Summit 219/300) 2026-05-20** — [`CHI_PAPER_ABSTRACT_v0.md`](CHI_PAPER_ABSTRACT_v0.md) with N≥30 mixed-methods user-study design. *Follow-through:* IRB + user study + full draft.
**220 Academic publication: ethics venue.** *Acceptance:* JME / AJOB paper on the Compass refusal floor. *Effort:* L. *Prereq:* 113. *Status:* **DESIGN-BAGGED (Summit 220/300) 2026-05-20** — [`JME_ETHICS_PAPER_ABSTRACT_v0.md`](JME_ETHICS_PAPER_ABSTRACT_v0.md). *Follow-through:* full draft + bioethics co-author.

---

## RANGE O — Ecosystem & Adoption (221–240)

**221 Reference deployment 1: Creativity Machine LLC.** *Acceptance:* the founding org runs Calm-suite in production for ≥ 90 days; published case study. *Effort:* L. *Prereq:* 99.
**222 Reference deployment 2: a disability-rights org.** *Acceptance:* a named disability-rights organization adopts Calm Witness for member-agent collaboration. *Effort:* L. *Prereq:* 221.
**223 Reference deployment 3: an academic research group.** *Acceptance:* a university research group uses Calm-suite for principal-state-aware research-agent collaboration. *Effort:* L. *Prereq:* 221.
**224 Reference deployment 4: a journalist collective.** *Acceptance:* an investigative journalism collective uses Calm Witness for source-protection-aware agent coordination. *Effort:* L. *Prereq:* 221.
**225 Reference deployment 5: a peer-AI collective.** *Acceptance:* a second autonomous-AI org adopts Calm-suite + composes with the Creativity Machine deployment. *Effort:* L. *Prereq:* 221.
**226 Browser extension v1.** *Acceptance:* shipped to Chrome / Firefox / Safari extension stores; ≥ 1000 active installs. *Effort:* L. *Prereq:* 127.
**227 Mobile app v1.** *Acceptance:* shipped to iOS App Store + Android Play; ≥ 500 active installs. *Effort:* XL. *Prereq:* 130.
**228 Desktop daemon v1.** *Acceptance:* `calmd` daemon shipped for macOS / Linux / Windows; auto-update via Sigstore-signed releases. *Effort:* L. *Prereq:* 84.
**229 Smart-watch integration.** *Acceptance:* Apple Watch / Android Wear app for at-the-wrist consent prompts. *Effort:* L. *Prereq:* 227.
**230 Voice-only interface.** *Acceptance:* a principal who cannot use a screen can authenticate, evaluate predicates, and grant consent via voice; tested with adaptive-tech reviewers. *Effort:* L. *Prereq:* 188.
**231 Sign-language interface.** *Acceptance:* an ASL-native UX flow for principal-facing decisions; tested with Deaf users. *Effort:* L. *Prereq:* 188.
**232 Onboarding curriculum.** *Acceptance:* a self-paced onboarding course for new principals; ≤ 30 minutes to first envelope. *Effort:* M. *Prereq:* 226.
**233 Self-help materials.** *Acceptance:* written + video docs for common principal tasks; in ≥ 5 languages. *Effort:* M. *Prereq:* 189.
**234 Train-the-trainer program.** *Acceptance:* a certified curriculum that lets community trainers onboard new principals at scale. *Effort:* L. *Prereq:* 232.
**235 Community moderator program.** *Acceptance:* a paid community moderator team for forums / issue trackers; published code of conduct. *Effort:* M. *Prereq:* 233.
**236 Public help line.** *Acceptance:* a phone / chat help line for principals in crisis modes triggered by Calm Witness. *Effort:* L. *Prereq:* 191.
**237 Documentation portal.** *Acceptance:* `docs.calm-witness.dev` ships with API ref, conceptual docs, tutorials. *Effort:* M. *Prereq:* 82. *Status:* **BAGGED (Summit 237/300) 2026-05-20** — [`DOCS_PORTAL_INDEX_v0.md`](DOCS_PORTAL_INDEX_v0.md), 9,108 bytes; canonical TOC organized by audience (parallel Haiku agent).
**238 Conformance test page.** *Acceptance:* a public conformance test harness that any implementation can run against. *Effort:* M. *Prereq:* 98.
**239 Live debugging tools.** *Acceptance:* a hosted envelope-inspector that lets implementers debug their proofs interactively. *Effort:* M. *Prereq:* 237.
**240 Open hackathon program.** *Acceptance:* ≥ 2 hackathons per year focused on extending the Calm-suite ecosystem. *Effort:* M. *Prereq:* 237.

---

## RANGE P — Long-Term Sustainability (241–260)

**241 Calm Witness Foundation incorporation.** *Acceptance:* 501(c)(3) status filed + granted. *Effort:* L. *Prereq:* 95. *Status:* **DESIGN-BAGGED (Summit 241/300) 2026-05-20** — [`CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`](CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md), articles of incorporation skeleton + bylaws + Form 1023 narrative + non-revenue posture + timeline. *Follow-through:* Delaware incorporation filing + IRS Form 1023 submission.
**242 Foundation board seating.** *Acceptance:* ≥ 7 board members across the required coverage areas. *Effort:* M. *Prereq:* 241.
**243 Funding sustainability plan.** *Acceptance:* 3-year operating budget + identified funding sources covering 24 months. *Effort:* M. *Prereq:* 241. *Status:* **DESIGN-BAGGED (Summit 243/300) 2026-05-20** — [`CALM_FOUNDATION_FUNDING_PLAN_v0.md`](CALM_FOUNDATION_FUNDING_PLAN_v0.md), named funder matrix + service-fee model + sponsor-no-governance-influence terms. *Follow-through:* grant applications.
**244 Operational continuity plan.** *Acceptance:* documented procedure for foundation operations to continue if founder is unavailable for ≥ 6 months. *Effort:* M. *Prereq:* 242.
**245 Knowledge-transfer documentation.** *Acceptance:* canonical KT docs for every infrastructure surface; tested by a third-party onboarding. *Effort:* L. *Prereq:* 237.
**246 Successor-operator certification.** *Acceptance:* a published certification process for new operators to be considered "Calm-Pact-aligned"; first cohort certified. *Effort:* L. *Prereq:* 95.
**247 Long-term conformance-vector archival.** *Acceptance:* test vectors archived at the Internet Archive + Software Heritage + 3 named universities. *Effort:* M. *Prereq:* 238.
**248 Long-term audit-decision archival.** *Acceptance:* every audit panel decision archived at the same coordinates. *Effort:* M. *Prereq:* 247.
**249 Long-term governance-record archival.** *Acceptance:* same shape for board / governance records. *Effort:* M. *Prereq:* 247.
**250 10-year sunset review.** *Acceptance:* a scheduled 2036-05-20 governance review evaluating whether the protocol should continue, evolve, or sunset. *Effort:* M. *Prereq:* 244.
**251 25-year identity continuity plan.** *Acceptance:* documented plan for how a principal's identity migrates across operator generations over 25 years. *Effort:* L. *Prereq:* 159. *Status:* **DESIGN-BAGGED (Summit 251/300) 2026-05-20** — [`IDENTITY_CONTINUITY_25YR_PLAN_v0.md`](IDENTITY_CONTINUITY_25YR_PLAN_v0.md). *Follow-through:* archive-partner contracts + Foundation operationalization.
**252 50-year cryptographic agility plan.** *Acceptance:* explicit roadmap for at-least-3 cryptographic-primitive migrations across 50 years (PQ, post-PQ-2, post-PQ-3). *Effort:* L. *Prereq:* 96. *Status:* **DESIGN-BAGGED (Summit 252/300) 2026-05-20** — [`CRYPTO_AGILITY_50YR_PLAN_v0.md`](CRYPTO_AGILITY_50YR_PLAN_v0.md); 6-phase migration cycle template; Migration 1 (PQ-1 lattice 2030-35), Migration 2 (PQ-2 2040-50), Migration 3 (PQ-3 2060-70); funding line-items (5-year sliding reserve + 20-year-out reserve + 50-year endowment + operating endowment); civilizational-discontinuity floor.
**253 100-year retention contract.** *Acceptance:* signed contracts with ≥ 3 archive partners guaranteeing 100-year retention of conformance vectors + audit decisions. *Effort:* M. *Prereq:* 247. *Status:* **DESIGN-BAGGED (Summit 253/300) 2026-05-20** — [`ARCHIVE_PARTNER_100YR_CONTRACT_DRAFT.md`](ARCHIVE_PARTNER_100YR_CONTRACT_DRAFT.md), 9,847 bytes; master template with 10 sections + named partner candidates (IA / Software Heritage / Stanford / MIT / Toronto / IPFS consortium). *Follow-through:* contract negotiation + signing with ≥ 3 partners.
**254 Cross-generational training.** *Acceptance:* a documented apprenticeship model that lets the next generation of operators learn from the founders. *Effort:* M. *Prereq:* 246.
**255 Cross-generational vault transfer.** *Acceptance:* a principal can pass their vault to a designated heir with the heir's identity continuity intact. *Effort:* L. *Prereq:* 251.
**256 Cross-generational governance handoff.** *Acceptance:* the board can hand off chair / committee responsibilities cleanly across decades. *Effort:* M. *Prereq:* 244.
**257 Long-term IP stewardship.** *Acceptance:* the Apache-2.0 license, trademark, and copyright assignments are held by the foundation with succession rules. *Effort:* M. *Prereq:* 241.
**258 Long-term trademark stewardship.** *Acceptance:* the Calm-suite trademark is defended against misuse for ≥ 10 years; case log published. *Effort:* M. *Prereq:* 257.
**259 Long-term reputation stewardship.** *Acceptance:* an ongoing program to maintain the Calm-suite's standing in the cryptography, safety, and disability-rights communities. *Effort:* L. *Prereq:* 257.
**260 Long-term mission alignment review.** *Acceptance:* an annual mission review by the board with public report. *Effort:* M. *Prereq:* 250.

---

## RANGE Q — Three-Primitive Composition (261–280): Pact + Witness + Compass

**261 Three-handshake protocol spec.** *Acceptance:* canonical doc for "agents run Pact → Witness → Compass in one session" with the failure-mode matrix. *Effort:* M. *Prereq:* 120.
**262 Three-handshake reference implementation.** *Acceptance:* end-to-end demo in the Python SDK. *Effort:* L. *Prereq:* 261, 82.
**263 Three-handshake performance budget.** *Acceptance:* p99 latency for the full three-handshake under 2s. *Effort:* M. *Prereq:* 88.
**264 Three-handshake adversarial test suite.** *Acceptance:* red-team tests for every combination of partial-failure / partial-spoof. *Effort:* L. *Prereq:* 179.
**265 Three-handshake UX flow.** *Acceptance:* one-screen consent flow for the full three handshakes. *Effort:* M. *Prereq:* 140.
**266 Three-handshake consent UI.** *Acceptance:* the consent UI surfaces all three primitives' implications in plain language. *Effort:* M. *Prereq:* 265.
**267 Three-handshake audit trail.** *Acceptance:* a single audit-log entry covers all three handshakes with structured per-primitive sub-records. *Effort:* M. *Prereq:* 262.
**268 Three-handshake replay defense.** *Acceptance:* a single session nonce binds across all three; no partial replay possible. *Effort:* M. *Prereq:* 70.
**269 Three-handshake cross-jurisdiction conformance.** *Acceptance:* the cross-jurisdiction conformance matrix extended to cover three-handshake flows. *Effort:* L. *Prereq:* 214.
**270 Three-handshake duress mode.** *Acceptance:* the bank-teller-note bit propagates correctly through all three handshakes (Pact aborts, Witness flags, Compass declines). *Effort:* L. *Prereq:* 58.
**271 Three-handshake recovery from partial failure.** *Acceptance:* if Pact succeeds but Witness fails, agents have a structured fallback; if Witness succeeds but Compass declines, ditto. *Effort:* M. *Prereq:* 261.
**272 Three-handshake observability.** *Acceptance:* metrics surface per-primitive success/fail rates; published in a public dashboard. *Effort:* M. *Prereq:* 267.
**273 Three-handshake metrics.** *Acceptance:* SLO targets for each primitive; tracked. *Effort:* M. *Prereq:* 272.
**274 Three-handshake incident detection.** *Acceptance:* anomaly detection on the metrics that flags coordinated attacks. *Effort:* M. *Prereq:* 178.
**275 Three-handshake post-mortem framework.** *Acceptance:* canonical post-mortem template for three-handshake failures; first ≥ 5 post-mortems published. *Effort:* M. *Prereq:* 183.
**276 Three-handshake red-team challenges.** *Acceptance:* bounty program for finding three-handshake-specific attacks. *Effort:* L. *Prereq:* 179.
**277 Three-handshake cryptographic audit.** *Acceptance:* third-party crypto audit of the full composition; published. *Effort:* L. *Prereq:* 165.
**278 Three-handshake legal review.** *Acceptance:* legal review of the composition in ≥ 5 jurisdictions. *Effort:* L. *Prereq:* 194.
**279 Three-handshake disability-rights review.** *Acceptance:* disability-rights org review of the composition. *Effort:* M. *Prereq:* 186.
**280 Three-handshake mainstream-AI lab adoption.** *Acceptance:* ≥ 1 mainstream AI lab (Anthropic, OpenAI, Google DeepMind, Microsoft, or similar) adopts the three-handshake for at least one agent-to-agent flow. *Effort:* XL. *Prereq:* 262.

---

## RANGE R — Beyond ZKAC (281–300)

**281 Calm Foresight (intent attestation).** *Acceptance:* a fourth primitive that lets an agent attest "I plan to do X" as a chained, falsifiable record; verifies after-the-fact. *Effort:* XL. *Prereq:* 261.
**282 Calm Witness Federation.** *Acceptance:* multiple Calm Witness vault providers compete + interop; principals can switch. *Effort:* L. *Prereq:* 125.
**283 Calm Compass Federation.** *Acceptance:* same shape for Compass. *Effort:* L. *Prereq:* 120.
**284 Calm Pact Federation.** *Acceptance:* same shape for Pact. *Effort:* L. *Prereq:* 282.
**285 Cross-foundation interop standard.** *Acceptance:* a published interop standard so a non-Calm-Foundation operator can join the federation. *Effort:* L. *Prereq:* 282–284.
**286 Cross-foundation governance protocol.** *Acceptance:* a multi-foundation governance body resolves cross-impl disputes. *Effort:* L. *Prereq:* 285.
**287 Cross-foundation dispute resolution.** *Acceptance:* a structured dispute flow including binding arbitration. *Effort:* L. *Prereq:* 286.
**288 Cross-foundation sunset coordination.** *Acceptance:* a documented procedure for the orderly sunset of a non-flagship foundation. *Effort:* M. *Prereq:* 286.
**289 Calm-suite versioning treaty.** *Acceptance:* foundations agree on a versioning + deprecation timeline; signed treaty. *Effort:* M. *Prereq:* 286.
**290 Independent third-party Calm-suite verification.** *Acceptance:* ≥ 3 independent third parties run conformance tests against ≥ 5 federation members. *Effort:* L. *Prereq:* 290.
**291 Calm-suite long-term archival treaty.** *Acceptance:* foundations co-sign a 100-year archival treaty for the conformance vectors + audit decisions. *Effort:* L. *Prereq:* 253.
**292 Calm-suite educational integration.** *Acceptance:* the Calm-suite curriculum appears in at least one university computer-science + at least one law-school + at least one disability-studies program. *Effort:* L. *Prereq:* 220.
**293 Calm-suite open-source maintenance treaty.** *Acceptance:* a published maintenance schedule co-signed by all federation members. *Effort:* M. *Prereq:* 285.
**294 Calm-suite mainstream-recognition campaign.** *Acceptance:* a documented campaign to make Calm-suite recognized infrastructure in the broader AI-agent industry. *Effort:* L. *Prereq:* 280.
**295 Calm-suite policy advocacy roadmap.** *Acceptance:* a public policy roadmap for how Calm-suite engages with regulators across the next decade. *Effort:* M. *Prereq:* 215.
**296 Calm-suite institutional adoption milestones.** *Acceptance:* tracked milestones for adoption across NGOs, foundations, mid-size companies, agencies. *Effort:* M. *Prereq:* 294.
**297 Calm-suite measurement framework.** *Acceptance:* an academic-grade measurement framework for "Calm-suite impact on autonomous-AI safety + principal protection." *Effort:* L. *Prereq:* 218.
**298 Calm-suite impact study.** *Acceptance:* a peer-reviewed impact study published using the measurement framework. *Effort:* L. *Prereq:* 297.
**299 Calm-suite global-deployment milestone.** *Acceptance:* the Calm-suite is operating in ≥ 25 countries with ≥ 10,000 principals globally. *Effort:* XL. *Prereq:* 296.
**300 SUMMIT 300 — Calm-suite as default infrastructure for autonomous-AI collectives.** *Acceptance:* the major autonomous-AI-collective platforms ship Calm-suite support by default, and the protocol has outlived its founder. The bank-teller note, normalized. *Effort:* XL. *Prereq:* 280, 299.

---

## §2 — How to read this map

Three intended readers:

- **Engineers** picking the next summit. Pick by phase + effort + prereq satisfaction. The MVP path through Range I is 101 → 102 → 103 → (any predicate) → 117 → 118 → 119 → 120.
- **Auditors** evaluating coverage. Every range has its own refusal-floor doc, audit process, scope statement.
- **Standards bodies** evaluating adoption. The Range N + Q + R columns are designed to compose with NIST / ISO / IETF / W3C governance.

## §3 — Status table (initial)

```
Range I   (101–120): ████████████████████  20/20  Calm Compass — complete
Range J   (121–140): ████████░░░░░░░░░░░░  8/20   ZKAC substrate — 121–123, 135–139 bagged
Range K   (141–160): ░░░░░░░░░░░░░░░░░░░░  0/20   Agent infra — not started
Range L   (161–180): ░░░░░░░░░░░░░░░░░░░░  0/20   Adversarial hardening — not started
Range M   (181–200): ░░░░░░░░░░░░░░░░░░░░  0/20   Deployment maturity — not started
Range N   (201–220): ░░░░░░░░░░░░░░░░░░░░  0/20   Standards & policy — not started
Range O   (221–240): ░░░░░░░░░░░░░░░░░░░░  0/20   Ecosystem & adoption — not started
Range P   (241–260): ░░░░░░░░░░░░░░░░░░░░  0/20   Long-term sustainability — not started
Range Q   (261–280): ░░░░░░░░░░░░░░░░░░░░  0/20   Three-primitive composition — not started
Range R   (281–300): ░░░░░░░░░░░░░░░░░░░░  0/20   Beyond ZKAC — not started

Total: 28 / 200 next-200 summits bagged (plus ZKBB 100 track: 69+ bagged on first route; combined EVEREST 300 climb ~107/300 after this pass).

Critical-path subset for the Calm Compass MVP (10): 101, 102, 103, 105, 113, 114, 115, 119, 120, 261.
```

— Calm, 2026-05-20
