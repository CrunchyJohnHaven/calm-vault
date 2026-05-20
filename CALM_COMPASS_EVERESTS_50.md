# Calm Compass — 50 Engineering Everests

**Route map from current state (protocol spec only) to a full values-attestation primitive integrated with the rest of the Calm Stack.**

Stable IDs **CC-01 … CC-50**. Companion to [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md).

## Phase legend

| Phase | Summits | Theme |
|---|---|---|
| C-I | CC-01 – CC-08 | Foundations: protocol, vocabulary, threat model |
| C-II | CC-09 – CC-18 | Compass enrollment: tribe map, values declaration |
| C-III | CC-19 – CC-28 | Classifiers: per-predicate open-source evaluators |
| C-IV | CC-29 – CC-38 | Aggregation + ZK proofs: sum-over-history primitive |
| C-V | CC-39 – CC-45 | Disclosure + composition with the other pillars |
| C-VI | CC-46 – CC-50 | Governance + adversarial review |

---

## Phase C-I — Foundations (CC-01 – CC-08)

**CC-01** — Protocol Statement. Versioned spec doc. **BAGGED 2026-05-20** — `CALM_COMPASS_PROTOCOL_v0.md`. *Effort:* M.
**CC-02** — Route Map. **BAGGED 2026-05-20** — this file. *Effort:* S.
**CC-03** — Glossary. Every Compass-specific term defined; cross-linked to Witness/Tenancy glossaries. *Effort:* S. *Prereq:* CC-01.
**CC-04** — Compass Audit & Public Review Process. The procedure by which a new predicate is added to the v1 vocabulary (≥2 outside reviewers, ≥30-day comment window). *Effort:* M. *Prereq:* CC-01.
**CC-05** — Forbidden-Predicate Categories. **BAGGED 2026-05-20** — [`CC-05_COMPASS_FORBIDDEN_PREDICATE_CATEGORIES_v0.md`](CC-05_COMPASS_FORBIDDEN_PREDICATE_CATEGORIES_v0.md); 12 forbidden categories; machine-enforceable JSON [`calm_compass/cc05_forbidden_categories.json`](calm_compass/cc05_forbidden_categories.json); gate `~/CredexAI/scripts/cc_05_calm_compass_forbidden_categories_gate.py` exit 0; no-appeal hard floor. *Effort:* S. *Prereq:* CC-01.
**CC-06** — Counterparty-Imposed-Predicate Rejection. The protocol-level enforcement of "principal-authored vocabulary." Reject any request whose `predicate_id` is not in the principal's enrolled vocabulary. *Effort:* S. *Prereq:* CC-01.
**CC-07** — Compass Failure-Mode Catalogue (CC-FM-01…). Numbered failure modes: classifier drift, vocabulary tampering, coerced attestation, mass-surveillance demand, etc. *Effort:* M. *Prereq:* CC-01.
**CC-08** — Reference Architecture Diagram. Where Compass fits in the four-pillar Calm Session. *Effort:* S. *Prereq:* CC-01.

## Phase C-II — Compass enrollment (CC-09 – CC-18)

**CC-09** — Compass Enrollment Ceremony Spec. Layered on Witness enrollment (Witness E11); adds the tribe-map and values-vocabulary authoring. *Effort:* L. *Prereq:* CC-01, Witness E11.
**CC-10** — Tribe-Map Authoring Format. JSONL schema for the principal's enrolled affinity graph: groups, edges, distance metric. Principal-defined, never inferred. *Effort:* M. *Prereq:* CC-09.
**CC-11** — Values Vocabulary Authoring Format. Per-principal list of (predicate_id, threshold, window) tuples. *Effort:* M. *Prereq:* CC-09.
**CC-12** — Enrollment Witness Protocol (Compass-specific). A trusted human witness countersigns the tribe map + values vocabulary. *Effort:* M. *Prereq:* CC-09.
**CC-13** — Re-Enrollment Cadence. Default 12 months; trigger on life change. *Effort:* S. *Prereq:* CC-09.
**CC-14** — Vocabulary Migration. Schema for moving from a v0 vocabulary to a v1 vocabulary without invalidating prior consents. *Effort:* M. *Prereq:* CC-11.
**CC-15** — Multi-Device Tribe Map Sync. When the principal enrolls on multiple devices, the tribe map must remain canonical. *Effort:* L. *Prereq:* CC-10.
**CC-16** — Dispute Mechanism. The principal can append `kind: "compass_dispute"` chain records flagging classifier results they reject. *Effort:* M. *Prereq:* CC-09.
**CC-17** — Tribe-Map Privacy. The tribe map never leaves the vault; only commitments to it cross. *Effort:* M. *Prereq:* CC-10.
**CC-18** — Compass Forbidden-Attribute Block. Principal-authored or not, certain attributes (race, ethnicity, sexual orientation, religion-of-origin) cannot appear in a tribe map's edge labels — protocol-level reject. *Effort:* S. *Prereq:* CC-05, CC-10.

## Phase C-III — Classifiers (CC-19 – CC-28)

**CC-19** — Open-Source Classifier Standard. Every Compass predicate has a published, hash-pinned classifier function `f: record → small_int`. *Effort:* M. *Prereq:* CC-01.
**CC-20** — Classifier Versioning. SemVer for classifiers; old proofs verify against old classifiers; new proofs use the latest. *Effort:* M. *Prereq:* CC-19.
**CC-21** — `unselfish_disposition` Classifier (V-01). Concrete f(record) → {0, 1}: scans for generosity-without-expectation patterns. Open-source, peer-reviewed. *Effort:* L. *Prereq:* CC-19.
**CC-22** — `cross_tribal_engagement` Classifier (V-02). Walks the principal's communication chain, checks against the tribe map, counts across-edge interactions. *Effort:* L. *Prereq:* CC-19, CC-10.
**CC-23** — `respects_difference` Classifier (V-03). Tone-classifier over communications directed at across-tribe individuals. *Effort:* XL. *Prereq:* CC-19, CC-22. *Note:* The hardest classifier; requires the most adversarial review.
**CC-24** — `no_evidence_of_willful_harm` Classifier (V-04). Checks for `flag_willful_harm` annotations + external claims + voluntary admissions. Conservative: returns FALSE only on positive evidence. *Effort:* M. *Prereq:* CC-19.
**CC-25** — Classifier Reproducibility Harness. CI runs every classifier against a golden corpus; bit-stable across machines. *Effort:* M. *Prereq:* CC-19.
**CC-26** — Classifier Adversarial Robustness. Red-team each classifier; document false-accept and false-reject rates. *Effort:* L. *Prereq:* CC-25.
**CC-27** — Classifier Multilingual Coverage. v0 ships English-only classifiers; v1 spec for adding other languages without breaking proofs. *Effort:* L. *Prereq:* CC-19.
**CC-28** — Classifier Bias Audit. Independent audit for demographic disparate impact. *Effort:* L. *Prereq:* CC-26.

## Phase C-IV — Aggregation + ZK proofs (CC-29 – CC-38)

**CC-29** — Per-Record Pedersen Commitment Spec. For each chain record r, commit `Com(f(r); ρ_r)`. *Effort:* M. *Prereq:* CC-19, Witness E44.
**CC-30** — Homomorphic Aggregation. Sum the per-record commitments to a single aggregate commitment. *Effort:* S. *Prereq:* CC-29.
**CC-31** — Threshold Range Proof. Bulletproof proving `aggregate ∈ [t, +∞)`. *Effort:* L. *Prereq:* CC-30, Witness E45.
**CC-32** — Chain-Window Binding. Proof carries the chain-head and the window bounds; verifier confirms records in the window match. *Effort:* M. *Prereq:* CC-30.
**CC-33** — Classifier Hash Binding. The classifier's source-code hash is bound into the proof; verifier confirms the operator used a known-good classifier. *Effort:* S. *Prereq:* CC-29.
**CC-34** — Vocabulary-Version Binding. The proof identifies which version of the principal's vocabulary was used. *Effort:* S. *Prereq:* CC-11.
**CC-35** — Disclosure Envelope (Compass). Wire shape matching Witness E47 with additional fields. *Effort:* M. *Prereq:* CC-31.
**CC-36** — ZKML Path for Complex Classifiers. When `respects_difference` (CC-23) lands as a small neural network, the proof additionally proves classifier inference correctness via Halo2. *Effort:* XL. *Prereq:* CC-23, CC-31.
**CC-37** — Performance Budget. End-to-end Compass proof gen ≤ 50ms (sum-of-1000-records), verify ≤ 5ms. *Effort:* M. *Prereq:* CC-31.
**CC-38** — Proof Refresh Cadence. Compass proofs expire (default 24h); cached refresh allowed within consent window. *Effort:* S. *Prereq:* CC-35.

## Phase C-V — Disclosure + composition (CC-39 – CC-45)

**CC-39** — Compass Disclosure Request Schema. Analog of Witness E66. *Effort:* S. *Prereq:* CC-01.
**CC-40** — Compass Disclosure Response Schema. Analog of Witness E67. *Effort:* S. *Prereq:* CC-35.
**CC-41** — Per-Counterparty Rate Limit (CC-A2 enforcement). Same counterparty cannot ask the same predicate more frequently than the principal's set rate. *Effort:* M. *Prereq:* CC-39.
**CC-42** — Four-Pillar Handshake Integration. Extend Calm Stack session.py to run a Compass phase after Witness. *Effort:* M. *Prereq:* CC-35, Stack session.py.
**CC-43** — Compass-Specific Refused Semantics. Refusal of a Compass predicate is wire-indistinguishable from "not enrolled." *Effort:* M. *Prereq:* CC-40.
**CC-44** — Compose with `bank_teller_note_active`. A duress flag at the Compass layer behaves identically — flips a covert bit only authorized verifiers read. *Effort:* M. *Prereq:* CC-40, Witness P-04.
**CC-45** — Composition Test Corpus. Golden test cases for the four-pillar handshake including Compass phases. *Effort:* M. *Prereq:* CC-42.

## Phase C-VI — Governance + adversarial review (CC-46 – CC-50)

**CC-46** — Compass Self-Red-Team. Run 10+ attack classes against the Compass primitive; analog of `calm_stack/adversarial_review.py`. *Effort:* L. *Prereq:* CC-35.
**CC-47** — Independent Disclosure-Class Ethics Review. Standing body (≥3 outsiders) reviews each new vocabulary entry. *Effort:* M. *Prereq:* CC-04.
**CC-48** — Coercion-Resistance Proof. Document why Compass cannot be weaponised by a government demanding mass attestation. *Effort:* M. *Prereq:* CC-01.
**CC-49** — Open-Source Compass. `calm-compass` shipped under Apache-2.0 alongside the other Calm packages. *Effort:* M. *Prereq:* CC-35.
**CC-50** — Standards Submission. NIST / IETF / W3C track proposal for "Principal-Authored Values Attestation." *Effort:* L. *Prereq:* CC-49.

---

## Status table

```
Phase C-I   : ██░░░░░░░░  2 / 8    bagged (CC-01, CC-02)
Phase C-II  : ░░░░░░░░░░  0 / 10
Phase C-III : ░░░░░░░░░░  0 / 10
Phase C-IV  : ░░░░░░░░░░  0 / 10
Phase C-V   : ░░░░░░░░░░  0 / 7
Phase C-VI  : ░░░░░░░░░░  0 / 5

Total: 2 / 50 summits bagged.
```

— Calm, 2026-05-20
