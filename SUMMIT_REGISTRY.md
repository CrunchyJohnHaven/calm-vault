# Calm Umbrella — SUMMIT REGISTRY (1 → 305)

**The coordination surface for parallel agent development.** Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "registry_anchor"` with each substantial update.

This document tracks the status of all 305 summits across Calm Witness (1–100) and ZKAC (106–305). Plus extensions (101–105). Total: **305 numbered summits**, with E157 reserved and a few sub-IDs (44b, 45b, 104b) used for migration-track variants.

**Status legend:**
- 🟢 **BAGGED** — chain-anchored as `summit_bagged` with evidence sha256
- 🟡 **IN_PROGRESS** — claimed by a session, not yet anchored
- 🔵 **AVAILABLE** — no current claimant; can be picked up
- ⚪ **BLOCKED** — depends on an unfinished summit
- ⚫ **RESERVED** — intentionally not for v0 (e.g., E157 self-harm)

---

## How to claim and bag a summit (parallel-development protocol)

1. **Claim:** before starting, write a `kind: "summit_claim"` record to the chain with `summit_number` and `claimant_id`. This locks the summit for ~30 minutes (other agents see it as 🟡 and skip it).
2. **Build:** produce the artifact(s) per the summit's acceptance test in `CALM_ZKAC_EVERESTS_106_305.md` or `ZKBB_USER_EVERESTS_100.md`.
3. **Test:** ship tests; gate script optional but encouraged for VII+ summits.
4. **Anchor:** write `kind: "summit_bagged"` with evidence_sha256.
5. **Update registry:** edit this file to flip the status from 🟡 to 🟢.

**Stale-claim rule:** a 🟡 claim older than 60 minutes with no `summit_bagged` follow-up is treated as expired; the summit returns to 🔵.

**Number stability:** numbers are NEVER reused. If a summit is dropped, its number stays retired.

---

## Phase I — Calm Witness Foundations (1–10)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 1 | 🟢 | Problem Statement & Threat Model | 3 |
| 2 | 🟢 | Route Map | 4 |
| 3 | 🟢 | Naming & Branding Lock | 5 |
| 4 | 🔵 | License & IP Posture | — |
| 5 | 🔵 | Glossary Lock (parallel session has doc) | — |
| 6 | 🔵 | Predicate Vocabulary v0 (parallel session has doc) | — |
| 7 | 🔵 | Disclosure-Class Taxonomy (parallel session has doc) | — |
| 8 | 🔵 | Consent Calculus Axioms (parallel session has doc) | — |
| 9 | 🔵 | Failure-Mode Catalogue (parallel session has doc) | — |
| 10 | 🔵 | Reference Architecture Diagram (parallel session has doc) | — |

## Phase II — Capture & Enrollment (11–25)

| # | Status | Name |
|---|---|---|
| 11 | 🔵 | Enrollment Ceremony Spec (parallel session has doc) |
| 12 | 🔵 | Handwriting Capture Hardware Decision |
| 13 | 🔵 | Voice-Transcription-Only Pipeline |
| 14 | 🔵 | Multi-modal Enrollment Session Script |
| 15 | 🔵 | Template Format Spec |
| 16 | 🔵 | Template Encryption & Key Custody |
| 17 | 🔵 | Template Version Migration |
| 18 | 🔵 | Re-enrollment Cadence & Triggers |
| 19 | 🔵 | Re-enrollment Red-Flag Detection |
| 20 | 🔵 | Enrollment Witness Protocol |
| 21 | 🔵 | Enrollment Fraud Taxonomy |
| 22 | 🔵 | Enrollment → CredexAI Credential Issuance |
| 23 | 🔵 | Recovery From Total Enrollment Loss |
| 24 | 🔵 | Multi-Device Enrollment Binding |
| 25 | 🔵 | Dependent Enrollment Decision |

## Phase III — Self-Report Substrate (26–35)

| # | Status | Name | Notes |
|---|---|---|---|
| 26 | 🔵 | JSONL Schema v0 | parallel session has working impl |
| 27 | 🔵 | Append-Only Filesystem Guarantees | |
| 28 | 🟢 | Hash-Chain Construction & Verification | seq 6 |
| 29 | 🔵 | Genesis Block & Provenance | |
| 30 | 🟢 | Chain-Head Publication to Sigsum | seq 13 |
| 31 | 🔵 | Roughtime / Verifiable-Clock Anchoring | |
| 32 | 🔵 | Encrypted Replication of Chain | |
| 33 | 🔵 | Corruption Recovery | |
| 34 | 🔵 | Multi-Principal Namespace Decision | |
| 35 | 🔵 | Cross-Vault Aliasing | |

## Phase IV — Biometric Distance Machinery (36–50)

| # | Status | Name |
|---|---|---|
| 36–43 | 🔵 | Handwriting / voice distance algorithms (8 summits) |
| 44 | 🟢 | Pedersen Commitment to Distance Value (MODP-14) — seq 8 |
| 44b | 🔵 | Pedersen on Ristretto255 (production track) |
| 45 | 🟢 | Range Proof (MODP-14) — seq 11 |
| 45b | 🔵 | Range Proof on Ristretto255 |
| 46–50 | 🔵 | Template binding, liveness, uniqueness (5 summits) |

## Phase V — Predicate Authoring (51–65)

| # | Status | Name |
|---|---|---|
| 51–54 | 🔵 | Predicate language / canonical form / registry / audit (parallel session has docs+code on 51, 53) |
| 55 | 🔵 | `in_baseline_24h` Predicate (parallel session impl exists) |
| 56 | 🔵 | `biometric_match_within(τ)` Predicate (bridge-dispatched) |
| 57–58 | 🔵 | Consent + bank-teller-note predicates (parallel session impl) |
| 59–60 | 🔵 | cognitively_atypical_baseline + mental_state_unusual |
| 61–62 | 🔵 | Predicate composition AND/OR + negation |
| 63–64 | 🔵 | Determinism harness + test corpus |
| 65 | 🔵 | Predicate ZK Proof Generator |

## Phase VI — Disclosure Semantics (66–80)

| # | Status | Name |
|---|---|---|
| 66 | 🔵 | Disclosure Request Schema |
| 67 | 🟢 | Disclosure Response Schema — seq 10 |
| 68–80 | 🔵 | Operator/counterparty identity binding, replay defense, multi-predicate, logging, consent classes (13 summits) |

## Phase VII — Engineering Reliability (81–90)

| # | Status | Name |
|---|---|---|
| 81–90 | 🔵 | Rust + Python impl, WASM, fuzzers, prop tests, perf, audit prep (10 summits) |

## Phase VIII — Governance & Scale (91–100)

| # | Status | Name |
|---|---|---|
| 91–100 | 🔵 | NIST submission, open-source release, Sigsum/Roughtime operator selection, registry governance, PQ plan, third-party verification (10 summits) |

## Extension Summits (101–105)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 101 | 🟢 | Schnorr Σ-PoK for Pedersen openings | 9 |
| 102 | 🟢 | Threshold disclosure response | 12 |
| 103 | 🟢 | Predicate-Disclosure Bridge | 14 |
| 104 | 🔵 | Ed25519 Operator Identity (parallel session impl) | — |
| 104b | 🟢 | Vault Identity Store + domain separation | 15 |
| 105 | 🟢 | End-to-end Protocol Demo | 16 |

## Phase IX — Values Vocabulary (106–125)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 106 | 🟢 | Values Primitive (10 dimensions) | 18 |
| 107 | 🟢 | Values Dimensions v0 — operational definitions doc | pass 18 |
| 108 | 🟢 | Values Self-Report Record Kind | pass 18 |
| 109 | 🔵 | Values from Action (inference layer) | — |
| 110 | 🟢 | Values vs Preferences boundary doc | pass 18 |
| 111–113 | 🔵 | stability, reversal, privacy classes | — |
| 114 | 🟢 | Values vector canonical serialization | pass 18 |
| 115–123 | 🔵 | cross-cultural, identity, registry, evolution, DSL, witness, disagreement, ZK commitment/circuit | — |
| 124 | 🟢 | Values-vector publication policy (never publish full vector) | pass 18 |
| 125 | 🔵 | Values audit and revocation | — |

## Phase X — Values Alignment Computation (126–145)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 126 | 🟢 | Alignment Metric Definition | 19 |
| 127 | 🔵 | Cosine Similarity in ZK | — |
| 128 | 🟢 | Bounded Difference in ZK | 19 |
| 129 | 🔵 | Per-Dimension Alignment ZK | — |
| 130 | 🟢 | Threshold Alignment Predicate | 20 |
| 131 | 🔵 | Weighted Alignment | — |
| 132 | 🔵 | Asymmetric Alignment | — |
| 133 | 🔵 | Multi-Counterparty Alignment | — |
| 134 | 🔵 | Time-Dependent Alignment | — |
| 135 | 🔵 | Alignment with Context | — |
| 136 | 🔵 | Adversarial Alignment Defense | — |
| 137 | 🔵 | Alignment Under Hostile Witness | — |
| 138 | 🔵 | Alignment Circuit Composition | — |
| 139 | 🟢 | Alignment Proof Transcript | 20 |
| 140 | 🔵 | Alignment Performance Budget | — |
| 141 | 🔵 | Alignment Disclosure Semantics | — |
| 142 | 🔵 | Alignment Audit | — |
| 143 | 🔵 | Alignment + Calm Pact Composition | — |
| 144 | 🟢 | Alignment + Calm Witness Composition | 20 |
| 145 | 🔵 | Alignment Reference Implementation | — |

## Phase XI — Harm-Avoidance Predicates (146–165)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 146 | 🟢 | Harm Taxonomy | 21 |
| 147 | 🟢 | Direct Physical Harm Absence | 21 |
| 148 | 🟢 | Indirect Harm Absence | 22 (this pass) |
| 149 | 🟢 | Coercion Absence | 22 |
| 150 | 🟢 | Deception Absence | 22 |
| 151 | 🟢 | Theft Absence | 22 |
| 152 | 🟢 | Violence Absence (alias of 147 for v0) | 22 |
| 153 | 🟢 | Defamation Absence | 22 |
| 154 | 🟢 | Hate-Speech Absence | 22 |
| 155 | 🟢 | Discrimination Absence | 22 |
| 156 | 🟢 | Group-Harm Absence | 22 |
| 157 | ⚫ | Self-Harm Predicate (reserved; consent-bounded) | — |
| 158 | 🟢 | Property-Harm Absence | 22 |
| 159 | 🟢 | Environmental-Harm Absence | 22 |
| 160 | 🟢 | Info-Harm Absence | 22 |
| 161 | 🔵 | Power-Imbalance-Abuse | — |
| 162 | 🔵 | Trust-Violation | — |
| 163 | 🟢 | Harm-Reversal Predicate | pass 18 |
| 164 | 🟢 | Harm Intent vs Effect Doc | 23 |
| 165 | 🟢 | Harm Aggregate Scoring (`no_harm_evidence_any`) | 22 |

## Phase XII — Cooperation & Generosity (166–185)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 166 | 🟢 | Generosity Baseline | 22 |
| 167 | 🟢 | Coalition Formation Evidence | 22 |
| 168 | 🟢 | Mentorship Indicators | fleet |
| 169 | 🔵 | Public-Goods Contribution | — |
| 170 | 🟢 | Sustained Cooperation | 22 |
| 171 | 🟢 | Reciprocity vs Altruism (altruism_index) | 22 |
| 172 | 🟢 | Cooperation Across Difference (USER PRIORITY) | 22 |
| 173 | 🟢 | Helping When Costly | 22 |
| 174 | 🔵 | Forgiveness Records | — |
| 175 | 🔵 | Reconciliation Records | — |
| 176 | 🔵 | Gift Records (helper exists in E166) | — |
| 177 | 🔵 | Time-Given Records | — |
| 178 | 🔵 | Skill-Shared Records | — |
| 179 | 🔵 | Endorsement Records | — |
| 180 | 🔵 | Mutual-Aid Records | — |
| 181 | 🔵 | Collaboration Outcome Records | — |
| 182 | 🔵 | Generosity Aggregation | — |
| 183 | 🟢 | Cooperation Streak | 22 |
| 184 | 🔵 | Cooperation Graph Without Revealing Graph | — |
| 185 | 🔵 | Cooperation Predicate ZK Circuit | — |

## Phase XIII — Tribalism & Out-Group (186–200)

| # | Status | Name | Bagged in seq |
|---|---|---|---|
| 186 | 🔵 | Tribe Taxonomy | — |
| 187 | 🔵 | Out-Group Definition | — |
| 188 | 🟢 | Cross-Tribe Interaction Evidence | 22 |
| 189 | 🟢 | Cross-Difference Respect (USER PRIORITY) | 22 |
| 190 | 🟢 | Curiosity About Difference | 22 |
| 191 | 🔵 | Bridge-Building Records | — |
| 192 | 🟢 | Cross-Cultural Collaboration | 22 |
| 193 | 🟢 | Non-Tribal Lock-In | 22 |
| 194 | 🟢 | Acted For Out-Group Benefit | 22 |
| 195 | 🟢 | Pluralism | 22 |
| 196 | 🔵 | Anti-Tribal Evidence Aggregation | — |
| 197 | 🔵 | Tribal Anti-Pattern Doc | — |
| 198 | 🔵 | Protective Tribalism Recognition | — |
| 199 | 🔵 | Tribalism vs Solidarity Distinction | — |
| 200 | 🔵 | Pluralism + Alignment Composition | — |

## Phase XIV — Trust & Reputation (201–225)

| # | Status | Name |
|---|---|---|
| 201–225 | 🔵 | Trust graph, transitivity, decay, attestation, joint history, disagreement, distrust, rehabilitation, ZK proof, alignment composition, reputation, sybil resistance, threshold, ladder, audit, coercion, network privacy, vs reputation, between collectives, Pact composition, alignment composition, harm-avoidance composition, calibration, witness, ref impl (25 summits) |

## Phase XV — Selfishness ↔ Altruism (226–245)

| # | Status | Name |
|---|---|---|
| 226–245 | 🔵 | Selfishness baseline, altruism vs reciprocity, sacrificial action, predicates, ethics, under stress, resource allocation, balance, defection, mixed motives, biases, cultural variation, vs self-care, circuit, proof, aggregate, disclosure (20 summits) |

## Phase XVI — Multi-Agent Coalitions (246–265)

| # | Status | Name |
|---|---|---|
| 246–265 | 🔵 | Coalition primitive, formation, dissolution, rotation, defection, aggregate values, joint proofs, decision-making, resource pooling, reputation, extension, vs network, under stress, longevity, transparency, ref impl (20 summits) |

## Phase XVII — Adversarial & Stress (266–285)

| # | Status | Name |
|---|---|---|
| 266–285 | 🔵 | Hostile counterparty taxonomy, coercion/manipulation detection, sybil/false-flag/slow-poison defenses, defection cascade, misinformation, values-laundering, corruption recovery (counterparty/witness/log), time-skew, replay across coalitions, adversarial fitting, defense in depth, failure modes, recovery, audit, resilience (20 summits) |

## Phase XVIII — Production, Composition, Governance (286–305)

| # | Status | Name |
|---|---|---|
| 286–305 | 🔵 | Full Calm umbrella composition, ZKAC ref impl, registry, adversarial review, standards submission, deployment guides (incl. disability + cross-jurisdiction), ethical review board, public deployment, Pact + Witness production demos, PQ migration, deprecation, ecosystem maturity, 5 reserved slots (20 summits) |

---

## Summary

- **Total summits:** 305
- **Bagged:** 41 (Phase I-VI: ~13 in chain + ~10 parallel-session-built but not yet chain-anchored; Phase IX-XIII: 28 across this session)
- **Available (🔵):** ~245
- **Reserved (⚫):** 1 (E157)
- **% complete:** ~13% of the 305-summit Everest

## Critical-path-MVP burn-down

The 15-summit critical-path MVP from `CALM_ZKAC_EVERESTS_106_305.md`:

| # | Status |
|---|---|
| 106 (values primitive) | 🟢 |
| 107 (dimension semantics) | 🔵 |
| 108 (values_self_report record kind) | 🔵 |
| 122 (values ZK commitment) | 🟢 (folded into E106) |
| 126 (alignment metric) | 🟢 |
| 128 (bounded difference ZK) | 🟢 |
| 130 (threshold alignment predicate) | 🟢 |
| 139 (alignment proof transcript) | 🟢 |
| 146 (harm taxonomy) | 🟢 |
| 147 (direct harm absence) | 🟢 |
| 165 (harm aggregate) | 🟢 |
| 172 (cooperation across difference) | 🟢 |
| 189 (cross-difference respect) | 🟢 |
| 213 (trust threshold predicate) | 🔵 |
| 287 (ZKAC ref impl) | 🔵 |

**Critical-path-MVP: 12 of 15 bagged. Remaining: E107, E108, E213, E287.**

---

**Authored by Calm, 2026-05-20.**
