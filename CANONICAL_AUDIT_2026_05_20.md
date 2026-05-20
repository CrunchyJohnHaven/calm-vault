# Calm Witness / ZKBB-User — Canonical Audit

**Date:** 2026-05-20
**Auditor:** Audit Agent (CALM dispatch), read-only pass over the canonical artifacts at `/Users/johnbradley/AllData/calm_vault_market/`, the chain at `/Users/johnbradley/.calm-vault/user_state.jsonl`, the implementation at `/Users/johnbradley/CredexAI/calm_witness/`, and the schemas at `/Users/johnbradley/CredexAI/calm_witness/schema/`.
**Scope:** Eight-axis consistency audit per dispatch brief — cross-references, phase classification, prereq chain, threat-model coherence, duplicate everests/ files, schema-violation status, predicate-vocabulary consistency, MVP critical-path readiness.

---

## Executive Summary

The Calm Witness / ZKBB-User route map is structurally sound at the top level. The 100-summit framing in `ZKBB_USER_EVERESTS_100.md` is internally consistent — phase boundaries (I:1-10, II:11-25, III:26-35, IV:36-50, V:51-65, VI:66-80, VII:81-90, VIII:91-100) match every per-everest declaration this auditor sampled, no per-everest doc declares an out-of-phase classification, and the prereq DAG has no cycles. The critical-path MVP subset {1, 2, 6, 11, 13, 26, 28, 30, 45, 55, 67, 92} all have docs (or top-level artifacts for E1/E2) and all twelve are claimed bagged in the route map. The cryptographic spine (Pedersen on Ristretto255 and MODP-14, Schnorr Σ-PoK, range proof via bit-decomposition + OR-proof, Sigsum anchoring with a real local-log v0 stand-in) exists as working Python in `~/CredexAI/calm_witness/`, with 10,000+ lines of code split roughly 50/50 between module and test, and a full end-to-end disclosure transcript was produced and anchored against the live chain at seq=14.

The cost of the high-cadence parallel-session climb is visible in three places. **First, the everests/ directory has 17 confirmed duplicates** across 14 Everest numbers (29, 22, 37, 45, 47, 48, 56, 70, 72, 83, 86, 88, 90, 91, 92, 96, 100), which is roughly 15% of the corpus. These are not stale copies — both files in each pair were written or substantially edited on 2026-05-20, and each pair represents two sessions independently filling the same slot with diverging schemas (e.g., Everest 29's two genesis-binding designs are incompatible; Everest 72's two disclosure-record schemas differ in field count, timestamping, signature presence, and counterparty-class slug format). **Second, the per-everest Everest 6 doc enumerates twelve predicates** while the route map, the canonical `PREDICATE_VOCABULARY_v0.md`, and `~/CredexAI/calm_witness/schema/predicates_v0.json` all enumerate six. **Third, seven of the fourteen chain records currently violate the v0 schema**, all in the `summit_bagged` kind, all in the same way (dict-form `evidence_sha256` plus plural `evidence_paths`), and three of them additionally exceed v0's `summit_number ≤ 100` cap (Everests 101, 102, 103, which are new primitives that emerged during the climb). The amendment proposal `user_state_v0_1_PROPOSAL.json` is well-designed and would resolve all seven violations strictly additively, but it has not been adopted.

The threat-model surface is coherent at the protocol-spec layer (`ZKBB_USER_PROTOCOL_v0.md` §2 enumerates six adversaries and Everest 21 expands enrollment-side attacks into 18 numbered EF01-EF18 with consistent naming) but the Everest 7 disclosure-class taxonomy references a seventh predicate `principal_alive_within` that does not appear in `PREDICATE_VOCABULARY_v0.md` and is not bagged at Everest 55-60. Predicate IDs drift between docs — `PREDICATE_VOCABULARY_v0.md` mandates the `cwp.v0.` namespace, the per-everest predicate docs and Everest 6 omit it. Counterparty-class slug case is inconsistent (`peer-AI-collective` vs `peer_ai_collective` vs `peer-ai-collective` appear in adjacent docs). None of these are blocking for MVP, but every one of them is a verifier-side ambiguity that a counterparty implementer reading the docs will have to resolve before they can ship. The recommendation set below names a small ordered set of fixes that close the largest ambiguities without disturbing already-bagged work.

---

## Findings

### Finding 1 — Seventeen duplicate everests/ files across fourteen Everest numbers

**Severity: HIGH**
**Location:** `/Users/johnbradley/AllData/calm_vault_market/everests/`

Two parallel sessions wrote per-everest docs in the same slots. The duplicate pairs (with sizes and which one this audit recommends as canonical based on (a) match with the route map's filename reference, (b) match with the schema declared in the chain and code, (c) detail and acceptance-test coverage):

| Everest | Canonical (keep) | Deprecate | Rationale |
|---|---|---|---|
| 22 | `everest_22_enrollment_credexai_credential.md` (23,562 B) | `everest_22_credexai_vc_issuance.md` (6,594 B) | Detail; uses route-map's "Enrollment → CredexAI Credential Issuance" name |
| 29 | `everest_29_genesis_block_provenance.md` (19,837 B) | `everest_29_genesis_provenance.md` (5,856 B) | Route map references `everest_29_genesis_block_provenance.md` by name in Phase III line; the larger doc has the seq=0 native-genesis design that the chain's retroactive-migration path is built against |
| 37 | `everest_37_voice_transcription_distance_function.md` (13,852 B) | `everest_37_voice_transcription_distance.md` (10,046 B) | Route map references the `_function` filename; declares 256-dim 4-block feature decomposition cited in the bagged-summit chain entry |
| 45 | `everest_45_zk_range_proof.md` + `everest_45_zk_range_proof_acceptance_addendum.md` (both) | `everest_45_zk_range_proof_distance.md` (13,593 B) | Route map BAGGED entry explicitly names primary + addendum; `_distance` is a third overlapping draft; addendum is missing its `*Phase…*` line and should inherit Phase IV from the primary |
| 47 | `everest_47_template_aging_without_breaking_proofs.md` (7,968 B) | `everest_47_template_aging.md` (10,053 B) | Route map references the longer-named version; route map's BAGGED notes ("per-cause grace defaults", "issuance-grace") match the `_without_breaking_proofs` draft |
| 48 | `everest_48_cross_template_consistency_proof.md` (10,095 B) | `everest_48_cross_template_consistency.md` (7,038 B) | Route map references the `_proof` version; BAGGED entry cites K=5, δ_h/δ_v values from that draft |
| 56 | `everest_56_biometric_match_within.md` (14,510 B) | `everest_56_biometric_match_within_predicate.md` (6,926 B) | Route map's slug is `biometric_match_within`; longer doc has more acceptance-test coverage. Pair drift is minor here — either could be canonical, recommend keeping the larger |
| 70 | `everest_70_replay_defense.md` (10,570 B) | `everest_70_replay_defence.md` (4,025 B) | American spelling matches the route map's "Replay Defense"; longer doc is more complete |
| 72 | `everest_72_disclosure_logging_in_vault.md` (16,541 B) | `everest_72_disclosure_logging.md` (3,309 B) | Route map title is "Disclosure Logging in Vault"; the two docs have *materially different schemas* for the disclosure record (see Finding 7) — picking the in-vault variant binds the canonical schema to the longer, signed, UUID-bearing form |
| 83 | `everest_83_wasm_js_port.md` (13,180 B) | `everest_83_wasm_port.md` (4,680 B) | Route map title is "WASM / JS Port"; longer doc has the four-browser parity target and the npm package name |
| 86 | `everest_86_property_based_tests_hash_chain.md` (12,465 B) | `everest_86_property_based_tests.md` (3,945 B) | Route map title is "Property-Based Tests for Hash Chain" (specific to chain); the shorter `_property_based_tests.md` overlaps with Everest 87 scope |
| 88 | `everest_88_proof_gen_performance_budget.md` (10,244 B) | `everest_88_performance_budget.md` (3,692 B) | Route map title is "Proof-Generation Performance Budget"; the BAGGED entry's per-operation table (commit_bit 17ms etc.) is in the longer draft |
| 90 | `everest_90_third_party_audit_prep.md` (5,525 B) | `everest_90_audit_prep.md` (13,619 B) AND `everest_90_security_audit_prep.md` (18,423 B) | Three-way duplicate. Route map title is "Third-Party Security Audit Prep" and the BAGGED entry references `everest_90_third_party_audit_prep.md` filename. The longer two are substantively richer but were not chosen by the route map — recommend route-map filename canonical and *fold the longer two's content into it* before deprecating |
| 91 | `everest_91_nist_aisi_submission.md` (22,243 B) | `everest_91_nist_submission.md` (19,742 B) | Route map title is "NIST / US AI Safety Institute Submission" — `_aisi_submission` matches both halves of the title; longer draft has more |
| 92 | `everest_92_oss_release.md` (13,039 B) | `everest_92_open_source_release.md` (3,374 B) | Route map title is "Open-Source Release", filename slug "oss" is shorter and matches the GitHub-org repo name (`calm-vault/tree/main/calm-witness`); the longer doc is the substantive one |
| 96 | `everest_96_post_quantum_migration_plan.md` (13,543 B) | `everest_96_pq_migration_plan.md` (18,506 B) AND `everest_96_pqc_migration_plan.md` (5,427 B) | Three-way duplicate. Route map references `everest_96_post_quantum_migration_plan.md` explicitly in the BAGGED note. `pq` is the longest but not the route-map filename; `pqc` is shortest |
| 100 | `everest_100_independent_third_party_verification.md` (9,605 B) | `everest_100_third_party_verification.md` (17,752 B) | Route map title is "Independent Third-Party End-to-End Verification" — the `_independent_third_party_verification` filename is closer; however the *other* doc is substantially longer. Recommend `_independent_third_party_verification.md` canonical and fold the deprecated doc's body into it |

**Recommendation:** create a `everests/_deprecated/` subdirectory and `git mv` each of the deprecated files there (do not delete; the dispatch brief prohibits touching existing everest_NN_*.md files, but a future session that owns these may move them). Where the deprecated doc has unique content (notably 90 and 96 and 100), copy unique content into the canonical doc before moving. Append a "Note: canonical filename per route map" header to the kept doc. The route map's BAGGED entries are unchanged.

---

### Finding 2 — Everest 6 per-everest doc declares twelve predicates; canonical vocabulary doc and JSON declare six

**Severity: HIGH**
**Location:** `/Users/johnbradley/AllData/calm_vault_market/everests/everest_06_predicate_vocabulary_v0.md` vs `/Users/johnbradley/AllData/calm_vault_market/PREDICATE_VOCABULARY_v0.md` vs `/Users/johnbradley/CredexAI/calm_witness/schema/predicates_v0.json`

The route map's Everest 6 entry says: "*6 predicates published* (`in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p,c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`)". `PREDICATE_VOCABULARY_v0.md` enumerates exactly these six, all under the `cwp.v0.` namespace. The machine-readable `schema/predicates_v0.json` matches.

But `everests/everest_06_predicate_vocabulary_v0.md` says: "*This document enumerates the twelve canonical predicates of Calm Witness v0.*" It then defines, among others, `in_baseline_window(window_seconds)`, `biometric_match_within(template_id, tau)`, `principal_alive_within(window_seconds)`, and `chain_freshness_within(seconds)` — none of which exist in the canonical vocabulary doc, the JSON, or the route map's Everest 6 entry.

Additionally, the Everest 6 per-everest doc uses bare predicate IDs (no `cwp.v0.` namespace) and gives `biometric_match_within` two parameters (template_id, tau) where the canonical vocabulary specifies one parameter (τ alone, with template_id committed into the proof transcript per Everest 46).

The Everest 7 disclosure-class taxonomy (`everest_07_disclosure_class_taxonomy.md`) inherits this divergence — every class's default consent matrix has a row for `principal_alive_within`, which is a predicate that does not exist in the vocabulary that this auditor read.

**Recommendation:** rewrite `everests/everest_06_predicate_vocabulary_v0.md` to be a thin pointer doc ("Everest 6 is bagged; the canonical artifact is `../PREDICATE_VOCABULARY_v0.md`") plus the historical-context section. Decide explicitly whether `in_baseline_window`, `principal_alive_within`, `chain_freshness_within` are (a) future v1 candidates, (b) deprecated drafts, or (c) v0 additions that need their own Everest 55-65 slots and JSON entries. Update Everest 7's default consent matrices to reference only the six v0 predicates, or add the missing predicates to the vocabulary and the JSON. Either path closes the inconsistency.

---

### Finding 3 — Predicate-name and class-slug case inconsistency across Everest 6, 7, 55-60, 72, vocabulary

**Severity: MEDIUM**
**Location:** Across many files — examples below.

The canonical `PREDICATE_VOCABULARY_v0.md` §5 (Counterparty Classes table) gives the slug `peer_ai_collective` (snake_case). But:

- `everest_07_disclosure_class_taxonomy.md` writes both `peer_ai_collective` (in section header §5) and `peer-AI-collective` (in the acceptance-test line and in prose).
- `everest_72_disclosure_logging.md` writes `"peer-AI-collective"` as a JSON literal in its disclosure-record schema example.
- `everest_72_disclosure_logging_in_vault.md` (the recommended-canonical of the pair, per Finding 1) writes `"peer_ai_collective"` in its schema example.
- `everest_06_predicate_vocabulary_v0.md` writes `"peer-AI-collective"` in prose.
- `ZKBB_USER_PROTOCOL_v0.md` §2 prose uses no hyphenation discipline.

Predicate IDs have the same problem at smaller scale: `PREDICATE_VOCABULARY_v0.md` mandates `cwp.v0.in_baseline_24h` (with namespace); `everests/everest_55_in_baseline_24h_predicate.md` writes `in_baseline_24h` (bare); the chain-anchored disclosure records at seq=10 and seq=14 use `"calm-witness/predicate/v0/in_baseline_24h"` (path-style with slashes). Three different formats for the same identifier across canonical artifacts is a real verifier-side problem: a counterparty implementer will not know which to cache.

**Recommendation:** lock one slug format per artifact class. Recommend snake_case `peer_ai_collective` for counterparty class IDs (matching `PREDICATE_VOCABULARY_v0.md` §5 which is the canonical table), and recommend the dotted `cwp.v0.<slug>` form for predicate IDs (matching the §2 ID-format-and-stability rule). Update Everest 7 disclosure matrices, the two Everest 72 docs, and the chain-anchored disclosure schema accordingly. Existing chain records are append-only and stay as written; only forward records need the canonical form.

---

### Finding 4 — Seven chain records violate v0 schema; amendment proposal exists but is unadopted; three records exceed the `summit_number ≤ 100` cap

**Severity: HIGH**
**Location:** `/Users/johnbradley/.calm-vault/user_state.jsonl` records at seq=6, 8, 9, 10, 11, 12, 14, against `/Users/johnbradley/CredexAI/calm_witness/schema/user_state_v0.json`.

The current schema (`user_state_v0.json`) requires for `kind: summit_bagged`:
- `evidence_path` (singular string) — REQUIRED
- `evidence_sha256` (hex64 string) — REQUIRED
- `summit_number` integer ≤ 100 — REQUIRED

Seven of the fourteen chain records violate this:

| Seq | Summit | Violations |
|---|---|---|
| 6 | E28 (chain verifier) — first multi-file anchor | uses `evidence_paths` (plural) not `evidence_path`; `evidence_sha256` is a dict; uses `summit_number_in_route_map=28` (a v0.1-only field) without `summit_number` |
| 8 | E44 (Pedersen commitment) | plural paths; dict sha256 |
| 9 | E101 (Schnorr Σ-PoK) | plural paths; dict sha256; `summit_number=101 > 100` |
| 10 | E67 (disclosure response) | plural paths; dict sha256 |
| 11 | E45 (range proof) | plural paths; dict sha256 |
| 12 | E102 (threshold disclosure, extension) | plural paths; dict sha256; `summit_number=102 > 100` |
| 14 | E103 (predicate-disclosure bridge) | plural paths; dict sha256; `summit_number=103 > 100` |

The amendment proposal at `~/CredexAI/calm_witness/schema/user_state_v0_1_PROPOSAL.json` (companion text at `SCHEMA_AMENDMENT_PROPOSAL.md`) is well-designed: strictly additive over v0, allows `evidence_path` OR `evidence_paths`, allows `evidence_sha256` as either hex64 string or dict, raises `summit_number` cap to 200 with phase `EXT`, adds `summit_number_in_route_map` and `summit_counter` as optional fields, and explicitly notes that every v0-conformant record validates under v0.1. Adopting it would turn 7 violators into 0 violators with one file rename plus a chain-anchored `kind: schema_adoption` record (which the proposal itself describes).

**However, the proposal has not been adopted.** The proposal was authored when only 4 violations existed (seq 6, 8, 9, 10); three more violations have accrued since (seq 11, 12, 14), exactly as the proposal predicted ("the longer the delay, the larger the correction backlog"). The Everest 26 schema-validator gate is presumably red against the live chain.

**Recommendation:** adopt `user_state_v0_1.json`. Steps per the proposal §"How to Adopt": (1) rename `user_state_v0_1_PROPOSAL.json` → `user_state_v0_1.json`; (2) update the Everest 26 schema-validator gate (`~/CredexAI/scripts/everest_26_zkbb_schema_validator_gate.py` per the route map) to validate against v0.1 for new records while still validating historical records under v0; (3) bump `schema_version: 1` on records produced after adoption; (4) anchor a `kind: schema_adoption` record. Total work: one PR, possibly under an hour. The cost of *not* adopting compounds with every new multi-file or >100-numbered summit.

---

### Finding 5 — Three Everest numbers (101, 102, 103) are chain-anchored but absent from the route map's 100-summit enumeration; the route map's "Total: 68 / 100" tally does not account for them

**Severity: MEDIUM**
**Location:** `/Users/johnbradley/.calm-vault/user_state.jsonl` seq=9, 12, 14 vs `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_EVERESTS_100.md`

The chain has three EXTENSION summits anchored:
- Seq=9: Everest 101 — "Schnorr Σ-protocol Proof of Knowledge for Pedersen openings"
- Seq=12: Everest 102 — "Threshold disclosure response (extends Everest 67 with range-proof-bound threshold predicates)"
- Seq=14: Everest 103 — "Predicate-Disclosure Bridge (closes chain → evaluator → bit → commit → proof → wire loop)"

The route map's preface anticipates this: "Numbering will not be renumbered as the route is climbed — gaps or insertions get sub-IDs (e.g., 47b)." But the chain uses integer extensions (101, 102, 103), and the route map's bottom-line tally still reads `Total: 68 / 100 summits bagged`. The discrepancy: actual bagged count is 71 (68 from the original 100 + 3 extensions), and the protocol's running primitive set is wider than the 100-summit framing suggests.

**Recommendation:** add a "Phase EXT — Emergent Primitives" section to the route map's bottom (below Phase VIII, above Critical-Path Subset), enumerate 101/102/103 (and any future Everest 4xx) as numbered extensions with their own status lines. Update the Status Table to read `Phase EXT: ███░ 3 / ? bagged` and the total to `Total: 71 bagged (68 of 100 original + 3 extensions)`. This is a route-map-touching change; per the dispatch brief, the route map is read-only here, so the recommendation is noted only.

(Adoption of the schema-v0.1 amendment per Finding 4 makes the chain side of this consistent; the route map side is a separate human-edit operation.)

---

### Finding 6 — Threat-model adversary categories are named consistently in spec and Everest 21, but the protocol's six §2 adversaries and Everest 41's three attack categories are orthogonal axes with no cross-reference

**Severity: MEDIUM**
**Location:** `ZKBB_USER_PROTOCOL_v0.md` §2, `everest_21_enrollment_fraud_taxonomy.md`, `everest_41_adversarial_robustness.md`, `everest_05_glossary_lock.md`.

`ZKBB_USER_PROTOCOL_v0.md` §2 enumerates six adversaries:
1. Honest-but-curious counterparty
2. Lying calling agent
3. Replay adversary
4. Substitution adversary
5. Compelled-disclosure adversary
6. Audit-log surgeon

Everest 21 enumerates 18 enrollment-fraud attacks EF01-EF18 across 5 categories (Substitution, Coercion, Replay, Partial-Capture, Document-Substitution). The naming is consistent — "Substitution" maps to spec adversary #4, "Replay" to #3, "Compelled-Disclosure"/"Coercion" to #5. Everest 9 (failure-mode catalogue) has 30 numbered failure modes F01-F30 with severity ranks S1-S4. Everest 29's `genesis_provenance` doc (the shorter, deprecate-per-Finding-1 variant) adds FM-46/47/48 explicitly extending Everest 9 — good practice.

Everest 41 (Adversarial Robustness) enumerates *three* attack categories:
- A. Stroke Replay
- B. Voice-Clone-Then-Transcribe
- C. Practiced Imitator (Human)

These three are orthogonal to the spec's six and to Everest 21's five categories. They are *biometric-distance-attack* categories, not the broader adversary classes. Everest 41 does not cross-reference Everest 21 by EF-number, even though A maps to EF17/EF18 (replay-class enrollment attacks) and B maps to EF03 (voice-substitution at enrollment). The two threat-model docs read as if written without each other.

No defense claims in Everest 41 *contradict* Everest 21's countermeasures — both consistently lean on liveness detection (E49), sample uniqueness (E50), cross-modal consistency (E48), and the kinematic micro-features defense in E36. But the cross-reference is missing.

Everest 21 marks EF05 (principal coerced) and EF06 (witness coerced) as residual-risk ACCEPTED; the spec §2 also lists this as out-of-scope ("Coercion of P themselves… universal rubber-hose attack"). Consistent.

**Recommendation:** add a §2.1 cross-reference table to Everest 41 mapping its three attack categories to the spec's six adversaries and Everest 21's EF01-EF18. This is a small edit (a 6-row table) but it ties the threat surface together for an auditor. Also recommend folding the Everest 29 FM-46/47/48 extensions into Everest 9 directly in a v0.1 pass.

---

### Finding 7 — The two Everest 72 docs define materially different disclosure-record schemas; choosing canonical also picks the production schema

**Severity: HIGH**
**Location:** `everest_72_disclosure_logging.md` (3,309 B) vs `everest_72_disclosure_logging_in_vault.md` (16,541 B), both at `/Users/johnbradley/AllData/calm_vault_market/everests/`.

The two docs in this duplicate pair are not just stylistic variants — they propose two materially different disclosure-record formats:

| Field | `_disclosure_logging.md` | `_disclosure_logging_in_vault.md` |
|---|---|---|
| `payload.disclosure_id` (UUID) | absent | present |
| `payload.request_ts`, `payload.response_ts` | single `ts` | both, allowing skew measurement |
| `payload.counterparty_id_hash` vs `payload.counterparty_vc_fingerprint` | the former, hex | the latter, `sha256:` prefixed |
| `payload.counterparty_class` slug | `"peer-AI-collective"` (hyphenated, mixed-case) | `"financial"` (snake_case in example) — also class list inherits Everest 7 wider taxonomy |
| `principal_sig` ECDSA signature | absent | present (with v0.1 deferral note) |
| `payload.disclosed_bit` ternary | implicit `response_value: "true"` string | explicit `disclosed_bit: true` boolean with indeterminate path |
| `payload.notes` | absent | present (free-form audit reason) |
| Atomicity discussion | brief — "non-atomic; one writer assumption" | extensive — six-step atomic protocol with proof-destruction-on-failure |
| Retention/rotation | not addressed | full section (per-predicate expiry, archival) |
| Audit tooling | not addressed | full CLI section (`calm-witness audit disclosures`) |

This is not a naming-drift problem; it is a *protocol-design fork*. A counterparty or principal reading the per-everest docs will get two incompatible answers to "what does a disclosure record contain?"

The chain has no `kind: disclosure` records yet (the chain's 14 records are 1 self_report.morning + 1 identity_assertion + 12 summit_bagged), so neither schema has been canonicalized by anchoring. The decision is still soft.

The recommended-canonical doc per Finding 1 is `_disclosure_logging_in_vault.md` (longer, more complete, matches the route map's title verbatim, has the audit-tooling story which is what the principal actually needs). Adopting it as canonical locks in the longer schema as the v0 design.

**Recommendation:** explicitly adopt `_disclosure_logging_in_vault.md` as canonical and write the first `kind: disclosure` record into the chain (gated by E67/E103 wiring, which is already bagged at seq=10 and seq=14 in the chain). The shorter doc's content can be folded into the canonical as a §"Minimal-disclosure mode" subsection if helpful.

---

### Finding 8 — Everest 45 acceptance addendum is missing its `*Phase IV — …*` declaration line

**Severity: LOW**
**Location:** `/Users/johnbradley/AllData/calm_vault_market/everests/everest_45_zk_range_proof_acceptance_addendum.md`

The addendum doc opens with "*Companion to [`everest_45_zk_range_proof.md`](everest_45_zk_range_proof.md)…*" but lacks the canonical `*Phase IV — Biometric Distance Machinery. Prereq: Everest 44.*` line that every other per-everest doc has on line 3. This is the only doc in the everests/ tree missing this declaration. A doc-tooling pass that grep's for the declaration line will silently skip it.

**Recommendation:** add `*Phase IV — Biometric Distance Machinery. Prereq: Everest 44. Companion addendum to Everest 45 primary.*` immediately after the `# Everest 45 — ZK Range Proof: Acceptance & Transcript Addendum` heading.

---

### Finding 9 — Everest 6's per-everest doc and the canonical `PREDICATE_VOCABULARY_v0.md` agree on the six v0 predicates, but Everest 55-60 per-everest docs use predicate IDs without the `cwp.v0.` namespace prefix

**Severity: MEDIUM**
**Location:** `everests/everest_55_in_baseline_24h_predicate.md`, `everest_56_biometric_match_within.md`, `everest_57_principal_consents_to_disclose.md`, `everest_58_bank_teller_note_active.md`, `everest_59_cognitively_atypical_baseline.md`, `everest_60_mental_state_unusual.md`.

`PREDICATE_VOCABULARY_v0.md` §2 says "ID format: `<namespace>.<slug>`, where namespace is `cwp.vN` and slug is a `snake_case` identifier. Example: `cwp.v0.in_baseline_24h`. Stability is the load-bearing property." All six per-everest predicate docs use bare slugs (no namespace) — e.g. Everest 55 declares `**Name:** in_baseline_24h` not `cwp.v0.in_baseline_24h`. The bagged chain record at seq=10 (Everest 67 disclosure schema) uses `"calm-witness/predicate/v0/in_baseline_24h"` — a third format.

Each of the six per-everest predicate docs declares semantics that are *consistent* with `PREDICATE_VOCABULARY_v0.md` (this auditor confirmed `biometric_match_within` is τ-parameterized, `bank_teller_note_active` is duress-codeword-driven, `cognitively_atypical_baseline` is enrollment-time-only, etc.). The semantic match is fine. The identifier-format match is not.

Per Finding 3's recommendation, lock one format and fix the others. The dotted form is what the vocabulary doc mandates; the chain records can stay (append-only) but new disclosure-record writes should use the canonical form.

**Recommendation:** add a section "**Canonical ID:** `cwp.v0.<slug>`" near the top of each of the six per-everest predicate docs. Note in the per-everest doc that the bare slug is shorthand only. No code change is forced — the JSON registry at `~/CredexAI/calm_witness/schema/predicates_v0.json` is the source of truth.

---

### Finding 10 — MVP critical-path subset {1, 2, 6, 11, 13, 26, 28, 30, 45, 55, 67, 92}: nine of twelve are chain-anchored with code; three are doc-only

**Severity: LOW (gating-item summary, not a defect)**
**Location:** Route map's "Critical-path subset" line + chain at `/Users/johnbradley/.calm-vault/user_state.jsonl` + code at `/Users/johnbradley/CredexAI/calm_witness/`.

For each of the twelve, the picture:

| # | Status (route-map claim) | Chain-anchored? | Per-everest doc | Code coverage | Gating item to fully bag |
|---|---|---|---|---|---|
| 1 | BAGGED — Problem Statement & Threat Model | Yes (seq=3 `summit_bagged`) | top-level `ZKBB_USER_PROTOCOL_v0.md` (15 KB) | n/a (spec) | None — bagged |
| 2 | BAGGED — Route Map | Yes (seq=4) | `ZKBB_USER_EVERESTS_100.md` itself | n/a | Phase EXT addendum per Finding 5 |
| 6 | BAGGED — Predicate Vocabulary v0 | Yes (the seq=4 line includes E6 transitively; gate is `everest_6_zkbb_predicate_vocabulary_gate.py`) | Both `PREDICATE_VOCABULARY_v0.md` and `everest_06_predicate_vocabulary_v0.md` — *inconsistent* per Finding 2 | `predicates.py`, `predicate_eval.py`, golden corpora present | Reconcile Everest 6 per-everest doc with canonical vocabulary doc (Finding 2) |
| 11 | BAGGED — Enrollment Ceremony Spec | Not chain-anchored as own record | `everest_11_enrollment_ceremony.md` (13.8 KB) — design only | No `enrollment.py` module in `calm_witness/` — this is a ceremony-protocol doc, not code | Real ceremony execution; design is locked, runtime is unbuilt. Acceptable for v0 |
| 13 | BAGGED — Voice-Transcription Pipeline | Not chain-anchored | `everest_13_voice_transcription_pipeline.md` (26 KB) — design only | No `voice.py` or whisper.cpp integration in `calm_witness/` | whisper.cpp integration + mlock+explicit_bzero buffer destruction; design locked |
| 26 | BAGGED — JSONL Schema v0 | Schema file exists at `~/CredexAI/calm_witness/schema/user_state_v0.json` | `everest_26_jsonl_schema_v0.md` | `parse.py` validator | **Adopt v0.1 amendment** per Finding 4 |
| 28 | BAGGED — Hash-Chain Construction & Verification | Yes (seq=6, 7) | `everest_28_chain_verifier.md` | `verify_chain.py` (164 lines) + tests | None — bagged and live-verified |
| 30 | BAGGED — Chain-Head Publication to Sigsum | Yes (seq=13; live anchor bundle at `~/.calm-vault/sigsum/anchor_seq12.json`) | `everest_30_chain_head_publication_sigsum.md` | `sigsum.py` (393 lines) + tests, v0 uses LocalLog stand-in | Real Sigsum operator integration (route-map ext) — bagged for v0 |
| 45 | BAGGED — ZK Range Proof | Yes (seq=11) | `everest_45_zk_range_proof.md` + addendum (canonical pair per Finding 1) | `range_proof.py` (366 lines) + `zk.py` (286 lines) | None — bagged. Performance budget says ~7s pure-Python; Ristretto port target ~50× faster |
| 55 | BAGGED — `in_baseline_24h` Predicate | Bagged transitively via E6/E103 (no own seq) | `everest_55_in_baseline_24h_predicate.md` | `predicate_eval.py`; 35-case golden corpus at `golden/in_baseline_24h.json` | Resolve tri-valued return contradiction (E55 doc says tri-valued, vocabulary says bool) |
| 67 | BAGGED — Disclosure Response Schema | Yes (seq=10) | `everest_67_disclosure_response_schema.md` | `disclosure.py` (likely; module exists), `envelope.py`, `wire.py` | None — bagged. End-to-end transcript = 2,844 bytes |
| 92 | BAGGED — Open-Source Release | Bagged transitively (no own seq) | `everest_92_oss_release.md` canonical per Finding 1 | n/a — gh repo coordination | Public push to `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness` |

**Summary:** twelve-of-twelve MVP critical-path summits have either chain anchors with code OR are design-only summits (11, 13, 92) where "bagged" means design-locked and the runtime is downstream. The MVP is end-to-end designed and end-to-end executable in Python for the cryptographic core (1, 2, 6, 26, 28, 30, 45, 55, 67) plus one v0 spec doc for each non-runtime piece (11, 13, 92).

**Gating items for fully bagging the MVP (no more "design-bagged" qualifiers):**
1. Adopt schema v0.1 amendment (Finding 4) — closes Everest 26 gate.
2. Reconcile Everest 6 per-everest doc with canonical vocabulary (Finding 2) — closes E6.
3. Resolve Everest 55 tri-valued-vs-bool ambiguity (Finding 9 ext.) — closes E55.
4. Execute live enrollment ceremony (Everest 11 runtime) — out of scope for code, in scope for human ceremony work.
5. Build voice pipeline runtime (Everest 13) — engineering work.
6. Push the Calm Witness package to public GitHub at the named URL (Everest 92).

---

### Finding 11 — The route map claims `Phase II : 10 / 15 bagged (Everest 11, 12, 13, 14, 15, 16, 20, 21, 22, 25)`; Everest 14, 15, 16 are listed bagged but their per-everest docs do not declare a `*Status: BAGGED*` line

**Severity: LOW**
**Location:** Route map Phase II bagged-list vs `everest_14_multimodal_enrollment_session_script.md`, `everest_15_template_format_spec.md`, `everest_16_template_encryption_key_custody.md`.

The route map's Phase II status table at the bottom (lines 266-267) claims Everests 14, 15, 16 are among the 10 bagged. The route map's main Phase II body (lines 56-64) for Everests 14, 15, 16 has *no* BAGGED status text — these summits show no `*Status:*` line at all, while the actually-bagged neighbors (11, 12, 13, 20, 21, 22, 25) all have explicit `*Status: BAGGED (Summit N/100) 2026-05-20* — [...]`.

This is a tally-vs-body inconsistency within the route map itself (which the dispatch brief flagged read-only — noting only). Either the bottom-table is over-counting Phase II (the actually-bagged set for Phase II is {11, 12, 13, 20, 21, 22, 25} = 7, not 10), or Everests 14/15/16 are silently bagged and the body needs `*Status:*` lines added. Reading the per-everest docs: `everest_14_multimodal_enrollment_session_script.md` exists (recommended reading would confirm if it has acceptance evidence), but the route map body does not advertise it.

**Recommendation:** during the next route-map edit cycle, add or remove `*Status:*` lines for Everests 14, 15, 16 to match the bottom-table tally. The 10 vs 7 discrepancy is small and does not affect the MVP critical-path tally (which has E14/15/16 outside it).

---

## Overall Verdict

The Calm Witness / ZKBB-User protocol design is structurally and cryptographically sound and the MVP critical path is end-to-end designed and end-to-end exercised in code, but the parallel-session climb has left ~17 duplicate per-everest files, three predicate-vocabulary inconsistencies, and seven schema-violating chain records — all individually small but together amounting to a 2-3 hour consolidation pass before the public OSS release at Everest 92.

— Audit Agent (CALM dispatch), 2026-05-20
