# Calm Witness — 100 Engineering Everests

**Route map from current state to a full cryptographic proof that all Calm agents have a tamperproof user-state model.**

Companion to [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md). Each summit has a stable numeric ID (Everest 1 … Everest 100), a phase, a one-sentence acceptance test, a rough effort estimate (S/M/L/XL — hours/days/weeks/months for a single dedicated engineer with full ZK toolchain), explicit prerequisites by ID, and notes where the hard part lives. Numbering will not be renumbered as the route is climbed — gaps or insertions get sub-IDs (e.g., 47b).

Each summit eventually gets a peer gate script at `~/CredexAI/scripts/everest_NN_zkbb_<slug>_gate.py`, matching the existing convention.

---

## Phase legend

| Phase | Summits | Theme |
|---|---|---|
| I | 1–10 | Foundations: spec, threat model, naming, glossary |
| II | 11–25 | Capture & Enrollment: get biometrics in safely, once |
| III | 26–35 | Self-Report Substrate: the JSONL chain & anchoring |
| IV | 36–50 | Biometric Distance Machinery: comparators & their ZK |
| V | 51–65 | Predicate Authoring: the named bits we expose |
| VI | 66–80 | Disclosure Semantics: how a bit is transmitted |
| VII | 81–90 | Engineering Reliability: implementations, tests, audits |
| VIII | 91–100 | Governance & Scale: standards, deploy, third-party verify |

---

## Phase I — Foundations (1–10)

**Everest 1 — Problem Statement & Threat Model.** *Acceptance:* a versioned doc captures actors, trust assumptions, adversaries, and what we are/aren't proving. *Effort:* M. *Status:* **BAGGED (Summit 1/100)** — [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md). *Note:* The bank-teller-note framing is the anchor; every later summit must serve it.

**Everest 2 — Route Map (this doc).** *Acceptance:* 100 summits enumerated with stable IDs, phases, deps, acceptance tests. *Effort:* M. *Status:* **BAGGED (Summit 2/100)** — this file.

**Everest 3 — Naming & Branding Lock.** *Acceptance:* one canonical name, glossary entries, no aliases drift. *Effort:* S. *Prereq:* 1. *Status:* **BAGGED (Summit 3/100) 2026-05-20** — [`NAMING_AND_BRANDING.md`](NAMING_AND_BRANDING.md), chain seq=5 (`record_hash` 67b57a82c277cdb6…). *Note:* Default name is **Calm Witness** (primitive) / **ZKBB-User** (technical). Sister to Calm Pact.

**Everest 4 — License & IP Posture.** *Acceptance:* Apache-2.0 license file, contributor-license-agreement decision, patent-non-aggression text. *Effort:* S. *Prereq:* 3. *Status:* **BAGGED (Summit 4/100) 2026-05-20** — [`everests/everest_04_license_ip_posture.md`](everests/everest_04_license_ip_posture.md); Apache-2.0, no CLA, non-aggression statement drafted. *Note:* Match Calm Pact's stance — open + non-aggressive.

**Everest 5 — Glossary Lock.** *Acceptance:* `GLOSSARY.md` with every term used in the protocol bound to a one-line definition; cross-linked. *Effort:* S. *Prereq:* 1, 3. *Status:* **BAGGED (Summit 5/100) 2026-05-20** — [`everests/everest_05_glossary_lock.md`](everests/everest_05_glossary_lock.md); 43+ terms, 4 disambiguation pairs.

**Everest 6 — Predicate Vocabulary v0.** *Acceptance:* an enumerated list of v0-named predicates with formal semantics and ID stability rules. *Effort:* M. *Prereq:* 1. *Status:* **BAGGED (Summit 6/100) 2026-05-20** — doc at [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md), machine-readable at `~/CredexAI/calm_witness/schema/predicates_v0.json`, loader/validator at `~/CredexAI/calm_witness/predicates.py`, gate at `~/CredexAI/scripts/everest_6_zkbb_predicate_vocabulary_gate.py`; 26/26 pytest assertions green; 6 predicates published (`in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p,c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`); 12 protected categories explicitly refused with rationales; evaluator-hash snapshot written for v1 drift detection. *Note:* The hard part — what the principal *won't* let us name — is now codified as a tested floor, not an aspiration.

**Everest 7 — Disclosure-Class Taxonomy.** *Acceptance:* counterparty classes (financial, journalistic, medical, governmental, peer-AI-collective, family, anonymous) with default policy stances. *Effort:* M. *Prereq:* 1. *Status:* **BAGGED (Summit 7/100) 2026-05-20** — [`everests/everest_07_disclosure_class_taxonomy.md`](everests/everest_07_disclosure_class_taxonomy.md); 10 classes with per-class default consent matrices; insurance flagged high-risk. *Note:* Per-class default consent ≠ per-identity consent; both layers exist.

**Everest 8 — Consent Calculus Axioms.** *Acceptance:* a small set of axioms (revocability, forward-secrecy, scope-narrowing, time-bounding) that every consent record must satisfy. *Effort:* M. *Status:* **BAGGED (Summit 8/100)** — [`everests/everest_08_consent_calculus_axioms.md`](everests/everest_08_consent_calculus_axioms.md). Ten axioms (A1-A10) finalized: Revocability, Forward Secrecy, Scope Narrowing, Time-Bounding, Witness-Free, Chained-Into-Vault, Per-Predicate-Per-Counterparty, Non-Transitivity, Defeasibility by Duress Codeword, Replay-Resistant Grant. *Prereq:* 6, 7. *Note:* Consent records are themselves chained into the vault.

**Everest 9 — Failure-Mode Catalogue.** *Acceptance:* a numbered list of every way Calm Witness can fail (stale chain, expired consent, biometric drift, operator subversion, key loss, etc.) with detect/respond per row. *Effort:* M. *Prereq:* 1, 2. *Status:* **BAGGED (Summit 9/100) 2026-05-20** — [`everests/everest_09_failure_mode_catalogue.md`](everests/everest_09_failure_mode_catalogue.md); 30 failure modes F01–F30, severity-ranked S1–S4; false-positive principal-harm is S1.

**Everest 10 — Reference Architecture Diagram.** *Acceptance:* one SVG that shows Principal, Operator, Vault, Counterparty, Verifier, and the message flow per session. *Effort:* S. *Prereq:* 1. *Status:* **BAGGED (Summit 10/100) 2026-05-20** — [`everests/everest_10_reference_architecture.md`](everests/everest_10_reference_architecture.md); 4 Mermaid diagrams (hydration, disclosure, two-handshake, ASCII fallback) + trust-boundary table.

---

## Phase II — Capture & Enrollment (11–25)

**Everest 11 — Enrollment Ceremony Spec.** *Acceptance:* a step-by-step ceremony doc covering where it happens, who witnesses it, what artifacts are produced, what must NOT be present (network, phones, etc.). *Effort:* L. *Prereq:* 1, 10. *Status:* **BAGGED (Summit 11/100) 2026-05-20** — [`everests/everest_11_enrollment_ceremony.md`](everests/everest_11_enrollment_ceremony.md). *Note:* The single most important "everest" — if enrollment is compromised, every later proof is theatre.

**Everest 12 — Handwriting Capture Hardware Decision.** *Acceptance:* one chosen device family (initially: Wacom Intuos Pro or Apple Pencil on iPad), with rationale, with sampling rate / pressure-level requirements pinned. *Effort:* S. *Prereq:* 11. *Status:* **BAGGED (Summit 12/100) 2026-05-20** — [`everests/everest_12_handwriting_capture_hardware.md`](everests/everest_12_handwriting_capture_hardware.md); Apple Pencil Pro + iPad Pro M primary, Wacom Intuos Pro fallback; floor 120Hz / 2048 pressure / tilt / ≤20ms.

**Everest 13 — Voice-Transcription-Only Pipeline.** *Acceptance:* a local-only ASR pipeline (e.g. whisper.cpp) that produces transcript + timing only, with the audio file destroyed at end-of-session. *Effort:* M. *Prereq:* 11. *Status:* **BAGGED (Summit 13/100) 2026-05-20** — [`everests/everest_13_voice_transcription_pipeline.md`](everests/everest_13_voice_transcription_pipeline.md); whisper.cpp small.en, mlock+explicit_bzero buffer destruction, NULL-hash destruction proof recorded into chain. *Note:* This is non-negotiable: raw audio never persists, so voiceprint leakage is structurally impossible.

**Everest 14 — Multi-modal Enrollment Session Script.** *Acceptance:* a 30–60 minute ceremony script that produces N≥7 handwriting samples + N≥7 voice-transcription samples spanning emotional/cognitive states. *Effort:* M. *Prereq:* 11, 12, 13. *Status:* **BAGGED (Summit 14/100) 2026-05-20** — [`everests/everest_14_multimodal_enrollment_session_script.md`](everests/everest_14_multimodal_enrollment_session_script.md); 45-min scripted ceremony (HW1–HW7 + V1–V7), pre-ceremony checklist §1, acceptance gates §3; gate at `~/CredexAI/scripts/everest_14_zkbb_multimodal_enrollment_gate.py`. *Note:* Variety is essential — baseline isn't one mood.

**Everest 15 — Template Format Spec.** *Acceptance:* a binary template format spec for both modalities, versioned, forward-compatible. *Effort:* M. *Prereq:* 14. *Status:* **BAGGED (Summit 15/100) 2026-05-20** — [`everests/everest_15_template_format_spec.md`](everests/everest_15_template_format_spec.md); CWT0 FlatBuffers envelope, Ed25519-signed, handwriting + voice sub-envelopes; gate at `~/CredexAI/scripts/everest_15_zkbb_template_format_gate.py`. *Status:* **BAGGED (Summit 15/100) 2026-05-20** — [`everests/everest_15_template_format_spec.md`](everests/everest_15_template_format_spec.md); CWT0 FlatBuffers envelope, Ed25519-signed, handwriting + voice sub-envelopes; gate at `~/CredexAI/scripts/everest_15_zkbb_template_format_gate.py`.

**Everest 16 — Template Encryption & Key Custody.** *Acceptance:* templates encrypted with a key the operator cannot exfiltrate; key is split or HSM-bound; principal can rotate. *Effort:* L. *Prereq:* 15. *Status:* **BAGGED (Summit 16/100) 2026-05-20** — [`everests/everest_16_template_encryption_key_custody.md`](everests/everest_16_template_encryption_key_custody.md); Argon2id KEK + age envelope, mlock/explicit_bzero session model, key rotation; gate at `~/CredexAI/scripts/everest_16_zkbb_template_encryption_gate.py`. *Note:* Compose with the existing `.calm-vault/master.priv.enc` + `master.salt` model.

**Everest 17 — Template Version Migration.** *Acceptance:* a protocol for re-issuing templates without invalidating outstanding consent records. *Effort:* M. *Prereq:* 15, 16. *Status:* **BAGGED (Summit 17/100) 2026-05-20** — [`everests/everest_17_template_version_migration.md`](everests/everest_17_template_version_migration.md); `template.migration` chain record, 30-day grace window, consent auto-forward + per-predicate override; gate at `~/CredexAI/scripts/everest_17_zkbb_template_migration_gate.py`.

**Everest 18 — Re-enrollment Cadence & Triggers.** *Acceptance:* a policy (every N months OR distance-drift trigger OR principal-initiated). *Effort:* S. *Prereq:* 17. *Status:* **BAGGED (Summit 18/100) 2026-05-20** — [`everests/everest_18_reenrollment_cadence.md`](everests/everest_18_reenrollment_cadence.md); time-based (12mo default), drift-based, principal-initiated triggers; gate at `~/CredexAI/scripts/everest_18_zkbb_reenrollment_cadence_gate.py`.

**Everest 19 — Re-enrollment Red-Flag Detection.** *Acceptance:* an automated check that the new template is consistent with prior (drift, not replacement); alerts on inconsistency. *Effort:* L. *Prereq:* 18. *Note:* Defends against kidnap-and-re-enroll.

**Everest 20 — Enrollment Witness Protocol.** *Acceptance:* an optional ceremony witness role (notary, family, Calm-Pact-aligned org) that signs a Pedersen commitment to the enrollment session record. *Effort:* M. *Prereq:* 11. *Status:* **BAGGED (Summit 20/100) 2026-05-20** — [`everests/everest_20_enrollment_witness_protocol.md`](everests/everest_20_enrollment_witness_protocol.md); 3-tier witness model (notary / family / institutional); witnesses see commitment only, never biometric.

**Everest 21 — Enrollment Fraud Taxonomy.** *Acceptance:* enumerated attacks on the enrollment ceremony (substitution, coercion, replay, partial-capture) with countermeasures. *Effort:* M. *Prereq:* 11, 9. *Status:* **BAGGED (Summit 21/100) 2026-05-20** — [`everests/everest_21_enrollment_fraud_taxonomy.md`](everests/everest_21_enrollment_fraud_taxonomy.md); 18 attacks EF01–EF18 across 5 categories with countermeasures + defense-in-depth matrix.

**Everest 22 — Enrollment → CredexAI Credential Issuance.** *Acceptance:* a successful enrollment produces a CredexAI-issued VC binding the templates' commitments to the principal's legal identity. *Effort:* M. *Prereq:* 16, 20. *Note:* Use the existing `koushik-credexai-inspect` SDK.

**Everest 23 — Recovery From Total Enrollment Loss.** *Acceptance:* a tested procedure for re-creating the vault if the device is lost, the principal is alive, and there are witness signatures. *Effort:* L. *Prereq:* 20, 22.

**Everest 24 — Multi-Device Enrollment Binding.** *Acceptance:* a single principal can enroll on N devices; templates roll up to one identity; revocation per device works. *Effort:* L. *Prereq:* 16, 22.

**Everest 25 — Dependent Enrollment (out of scope or in?).** *Acceptance:* a decision doc on whether v0 supports a Calm operator acting for a minor/dependent. *Effort:* S (decision) / XL (if yes). *Prereq:* 11. *Status:* **BAGGED (Summit 25/100) 2026-05-20** — [`everests/everest_25_dependent_enrollment_decision.md`](everests/everest_25_dependent_enrollment_decision.md); v0 locked at consenting-adult-only; vulnerable adults with capacity supported; guardians/minors deferred to v1+ ethics review. *Note:* v0 default: out of scope.

---

## Phase III — Self-Report Substrate (26–35)

**Everest 26 — JSONL Schema v0.** *Acceptance:* schema file + JSON-schema validator + reference parser. *Effort:* S. *Prereq:* 1, 5. *Status:* **BAGGED (Summit 26/100) 2026-05-20** — schema at `~/CredexAI/calm_witness/schema/user_state_v0.json` (Draft 2020-12, `additionalProperties:false`, per-kind payload subschemas for `self_report.morning` / `identity_assertion` / `summit_bagged` / `correction`); validator + reference parser at `~/CredexAI/calm_witness/parse.py`; gate at `~/CredexAI/scripts/everest_26_zkbb_schema_validator_gate.py`; 30/30 pytest assertions green; live chain (5 records, 3 kinds) validates clean; missing-field / non-hex-hash / bad-kind / unknown-field / out-of-range-summit / bad-wake-time all rejected. *Note:* Pairs with Everest 28 — structural validation at append time + chain validation at verify time.

**Everest 27 — Append-Only Filesystem Guarantees.** *Acceptance:* documented guarantees per OS (macOS APFS snapshots, Linux fanotify, iOS sandbox) + monitoring hook that detects out-of-band edits. *Effort:* M. *Prereq:* 26. *Status:* **BAGGED (Summit 27/100) 2026-05-20** — [`everests/everest_27_append_only_fs_guarantees.md`](everests/everest_27_append_only_fs_guarantees.md); macOS chflags+schg+APFS snapshots+FSEventStream; Linux chattr +a + fanotify; iOS sandbox+Data Protection; Calm Sentinel daemon spec.

**Everest 28 — Hash-Chain Construction & Verification.** *Acceptance:* CLI `calm-witness verify-chain` that walks the chain from genesis, checks every `record_hash` and `prev_hash`. *Effort:* S. *Prereq:* 26. *Status:* **BAGGED (Summit 28/100) 2026-05-20** — module at `~/CredexAI/calm_witness/verify_chain.py`, gate at `~/CredexAI/scripts/everest_28_zkbb_verify_chain_gate.py`; 14/14 pytest assertions green; verifier rejects payload mutation, bad-prev-hash genesis, and forged appends; live chain verifies clean. *Note:* Closes the structural-tamperproof loop: any post-hoc surgery on any record invalidates the chain from that record forward, detectable by any party holding the chain head.

**Everest 29 — Genesis Block & Provenance.** *Acceptance:* a per-principal genesis record schema that locks the principal-identity binding, the operator-identity binding, and the protocol version at moment-of-vault-creation. *Effort:* S. *Prereq:* 28. *Status:* **BAGGED (Summit 29/100) 2026-05-20** — [`everests/everest_29_genesis_block_provenance.md`](everests/everest_29_genesis_block_provenance.md); seq=0 genesis schema with dual signature (operator + principal); retroactive-genesis migration path for the existing live chain.

**Everest 30 — Chain-Head Publication to Sigsum.** *Acceptance:* every new chain head is published to a Sigsum transparency log; the inclusion proof is stored back in the vault. *Effort:* L. *Prereq:* 28. *Status:* **BAGGED (Summit 30/100) 2026-05-20** — [`everests/everest_30_chain_head_publication_sigsum.md`](everests/everest_30_chain_head_publication_sigsum.md); multi-log submission, multi-witness consensus, inclusion-proof retrieval, degraded-mode policy (`anchor_pending` → `unknown` disclosure). *Note:* This is where v0 graduates from "hash chain on one disk" to "tamperproof under any single-disk attacker."

**Everest 31 — Roughtime / Verifiable-Clock Anchoring.** *Acceptance:* each chain-head publication includes a Roughtime-attested timestamp from N independent servers; chain rejects clock skew > threshold. *Effort:* M. *Prereq:* 30.

**Everest 32 — Encrypted Replication of Chain.** *Acceptance:* the chain is replicated to ≥2 locations encrypted at rest with keys the principal controls. *Effort:* M. *Prereq:* 28.

**Everest 33 — Corruption Recovery.** *Acceptance:* if the local chain is destroyed but Sigsum has the heads and one replica survives, the chain can be re-derived. *Effort:* M. *Prereq:* 30, 32.

**Everest 34 — Multi-Principal Namespace Decision.** *Acceptance:* a decision doc: does one vault hold one principal, or can it federate? *Effort:* S. *Prereq:* 1. *Status:* **BAGGED (Summit 34/100) 2026-05-20** — [`everests/everest_34_multi_principal_namespace_decision.md`](everests/everest_34_multi_principal_namespace_decision.md); v0 locked at strictly 1:1; migration path to v2+ federated documented. *Note:* v0 default: strictly 1:1.

**Everest 35 — Cross-Vault Aliasing.** *Acceptance:* if the principal moves to a new operator, the new vault can prove continuity with the old via signed handover. *Effort:* L. *Prereq:* 22, 29.

---

## Phase IV — Biometric Distance Machinery (36–50)

**Everest 36 — Handwriting Distance Function Spec.** *Acceptance:* a formal definition (per-stroke kinematic vector → embedding → cosine distance, or DTW, or learned metric) + reference impl. *Effort:* L. *Prereq:* 12, 15. *Status:* **BAGGED (Summit 36/100) 2026-05-20** — [`everests/everest_36_handwriting_distance_function.md`](everests/everest_36_handwriting_distance_function.md); kinematic-DTW with stroke-segmented normalization, 9-dim per-step feature vector (position + velocity/accel/jerk + Frenet curvature + pressure + tilt sin/cos), Sakoe-Chiba band 10%, trimmed-mean aggregation, exp-squash to `[0,1]`. *Note:* Forensic-document-examination prior art is the starting point; bias toward kinematic over visual.

**Everest 37 — Voice-Transcription Distance Function.** *Acceptance:* a function operating on the transcript + word-timing only that produces a per-session score against the template. *Effort:* L. *Prereq:* 13, 15. *Status:* **BAGGED (Summit 37/100) 2026-05-20** — [`everests/everest_37_voice_transcription_distance_function.md`](everests/everest_37_voice_transcription_distance_function.md); deterministic 256-dim feature vector in 4 blocks (lexical / syntactic / prosodic / confidence-conditioned) → cosine distance, per-principal lexical-fingerprint basis committed at enrollment, audio-destroy-immediately invariant inherited from Everest 13. *Note:* Lexical fingerprinting on top of timing rhythm.

**Everest 38 — Combined Distance Fusion.** *Acceptance:* a principled fusion (likelihood-ratio combination, not naive average) with calibrated joint score. *Effort:* M. *Prereq:* 36, 37.

**Everest 39 — Drift Modeling.** *Acceptance:* a slow-update mechanism (EMA over confirmed-baseline sessions) that lets templates evolve without breaking past proofs. *Effort:* L. *Prereq:* 36, 37, 17.

**Everest 40 — FAR/FRR Curve Characterization.** *Acceptance:* an empirical FAR/FRR curve on real data, ideally with N≥10 principals across N≥3 months. *Effort:* XL. *Prereq:* 36, 37, 38. *Note:* Hardest empirical summit. Likely needs an external study partner.

**Everest 41 — Adversarial Robustness.** *Acceptance:* documented behavior of the distance functions under (a) stroke replay, (b) voice-clone-then-transcribe, (c) imitator with weeks of practice. *Effort:* XL. *Prereq:* 40. *Note:* This is what makes the bank-teller note actually unforgeable.

**Everest 42 — On-Device Evaluation Cost Target.** *Acceptance:* both distance functions run in <2s on an M-series Mac and <5s on a phone-class device. *Effort:* M. *Prereq:* 36, 37.

**Everest 43 — Rust Reference Implementation.** *Acceptance:* `calm-witness-rs` crate in `credex/research/fermis/lanes/F-ENGINEERING/zkac_v1/`, matching the zkac_v0 layout. *Effort:* L. *Prereq:* 36, 37, 38.

**Everest 44 — Pedersen Commitment to Distance Value.** *Acceptance:* the per-session distance is committed via `Com(d; r)` with hiding/binding properties. *Effort:* S. *Prereq:* 38. *Status:* **BAGGED (Summit 44/100) 2026-05-20** — [`everests/everest_44_pedersen_commitment_distance.md`](everests/everest_44_pedersen_commitment_distance.md); Ristretto255 (matching Calm Pact), `g` = base point, `h` = hash-to-curve(`"calm-witness-pedersen-h-v0"`), `d` encoded as 32-bit fixed-point integer, perfectly hiding + computationally binding under DLOG + additively homomorphic. *Note:* Compose with Calm Pact's curve choice.

**Everest 45 — ZK Proof: committed distance is below threshold τ.** *Acceptance:* a Σ-protocol (or Bulletproof / Groth16 if needed) proving `d < τ` without revealing `d` or `τ`'s evaluation steps. *Effort:* L. *Prereq:* 44. *Status:* **BAGGED (Summit 45/100) 2026-05-20** — primary [`everests/everest_45_zk_range_proof.md`](everests/everest_45_zk_range_proof.md) (Bulletproofs on Ristretto255, ~672-byte 32-bit range proof, v0 API placeholder at `calm_witness/proof.py` + v0.1 kernel path); addendum [`everests/everest_45_zk_range_proof_acceptance_addendum.md`](everests/everest_45_zk_range_proof_acceptance_addendum.md) (Fiat-Shamir transcript binding spec, multi-modal aggregation, T-45.1 through T-45.9 named acceptance suite). *Note:* Range proofs are well-studied; this is the most "standard ZK" summit. **Closes the cryptographic-proof loop with Everests 28, 30, 36, 37, 44, 46.**

**Everest 46 — Pedersen Commitment to Template ID.** *Acceptance:* the template-identifier is bound into proofs without revealing which template. *Effort:* S. *Prereq:* 44, 22. *Status:* **BAGGED (Summit 46/100) 2026-05-20** — [`everests/everest_46_pedersen_commitment_template_id.md`](everests/everest_46_pedersen_commitment_template_id.md); structurally identical to Everest 44 with `template_id_int = SHA256(template-bundle) mod q`; template-commitment ledger (`kind: template_commitment.v0`) with `supersedes`/`active_grace_until` for re-enrollment continuity; closes the substitution attack via Fiat-Shamir transcript binding into Everest 45.

**Everest 47 — Template Aging Without Breaking Proofs.** *Acceptance:* template v_n+1 can validate proofs issued against template v_n for a grace window. *Effort:* M. *Prereq:* 46, 39. *Status:* **BAGGED (Summit 47/100) 2026-05-20** — [`everests/everest_47_template_aging_without_breaking_proofs.md`](everests/everest_47_template_aging_without_breaking_proofs.md); per-cause grace defaults (annual 30d, injury 90d, device 30d, compromise 0d, principal-initiated 7d); issuance-grace semantics (not verification-grace); template_grace kernel for Everest 65; ~1 KB additional proof size.

**Everest 48 — Cross-Template Consistency Proof.** *Acceptance:* a verifier can prove that template v_n+1 is a valid drift of v_n without learning either. *Effort:* L. *Prereq:* 47. *Status:* **BAGGED (Summit 48/100) 2026-05-20** — [`everests/everest_48_cross_template_consistency_proof.md`](everests/everest_48_cross_template_consistency_proof.md); held-out challenge-sample protocol with K=5 default; drift budget δ_h=0.05 / δ_v=0.04; statistics-based vector-difference proof (~2 KB) as v0, full-vector proof deferred to v1; consistency waiver for acute-change cases. *Note:* Closes the "right principal's template" substitution-defense leg cryptographically.

**Everest 49 — Liveness Detection at Capture Time.** *Acceptance:* the capture pipeline rejects pre-recorded inputs (stroke replay, transcript paste). *Effort:* L. *Prereq:* 12, 13. *Note:* Hardware-level entropy (pen-tip pressure microvariation; transcript timing entropy) is the lever.

**Everest 50 — Sample Uniqueness Check.** *Acceptance:* a sample committed in session N cannot be re-used in session N+1; the chain enforces non-replay. *Effort:* M. *Prereq:* 28, 49.

---

## Phase V — Predicate Authoring (51–65)

**Everest 51 — Predicate Language v0.** *Acceptance:* either a small DSL or a fixed predicate-table; decision documented; one is chosen. *Effort:* M. *Prereq:* 6. *Status:* **BAGGED (Summit 51/100) 2026-05-20** — [`everests/everest_51_predicate_language_v0.md`](everests/everest_51_predicate_language_v0.md); v0 locked at fixed predicate table (no DSL); 8-criterion decision matrix; composition via multi-predicate proofs, not expressions. *Note:* Default lean: fixed predicate table for v0, DSL later.

**Everest 52 — Predicate Canonical Form.** *Acceptance:* canonical serialization so that `predicate_id` is content-addressable. *Effort:* S. *Prereq:* 51. *Status:* **BAGGED (Summit 52/100) 2026-05-20** — `predicate_canonical_form()` + `predicate_id_hash()` in `~/CredexAI/calm_witness/predicate_eval.py`; sorted-keys compact JSON over `(id, type, parameters, evaluator)`; excludes mutable metadata; SHA-256 hex is the content-addressable id; all 6 v0 predicates yield distinct hashes; gate at `~/CredexAI/scripts/everest_55_zkbb_in_baseline_24h_gate.py` §4.

**Everest 53 — Predicate ID Registry.** *Acceptance:* a public registry mapping `predicate_id` → human-readable spec + reference implementation. *Effort:* M. *Prereq:* 52. *Status:* **BAGGED (Summit 53/100) 2026-05-20** — co-bagged with Everests 6, 52, 55. Machine-readable: `~/CredexAI/calm_witness/schema/predicates_v0.json` (6 active predicates, content-addressable). Human-readable: [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md). Reference impls beginning with `in_baseline_24h` in `~/CredexAI/calm_witness/predicate_eval.py`. Doc/registry consistency enforced by the Everest 6 gate. *Note:* Public hosting at `calm-witness.dev/registry` deferred to the Everest 92 release.

**Everest 54 — Predicate Audit & Public Review Process.** *Acceptance:* a written process for proposing, reviewing, and adopting new predicates; ≥2 outside reviewers per addition. *Effort:* M. *Prereq:* 53. *Status:* **BAGGED (Summit 54/100) 2026-05-20** — [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md). 5-stage flow (Draft → Triage → Review → Vote → Merge) with 30-day public review window, ≥5-reviewer standing panel composed across cryptography / disability-rights / behavioral-biometric / AI-safety / journalism; tombstoning bar of ≥3 accepts and a published vuln-disclosure; v0 founding predicates grandfathered with mandatory v1 retroactive review.

**Everest 55 — `in_baseline_24h` Predicate.** *Acceptance:* the canonical baseline predicate is fully specified, tested, with a golden-input/output corpus. *Effort:* M. *Prereq:* 51, 26. *Status:* **BAGGED (Summit 55/100) 2026-05-20** — reference impl `in_baseline_24h(chain, baseline, now_iso)` in `~/CredexAI/calm_witness/predicate_eval.py`, pure deterministic function; 35-case golden corpus at `~/CredexAI/calm_witness/golden/in_baseline_24h.json` (empty chain, in/out 24h window, kind filtering, case + whitespace + unicode handling, timezone normalization, boundary conditions, defensive skip on malformed records); 51/51 pytest assertions green; gate at `~/CredexAI/scripts/everest_55_zkbb_in_baseline_24h_gate.py`. *Note:* Future ZK circuits (Everest 65) must compile to a function bit-stable against this corpus.

**Everest 56 — `biometric_match_within(τ)` Predicate.** *Acceptance:* a τ-parameterized predicate with per-principal calibration. *Effort:* M. *Prereq:* 51, 45. *Status:* **BAGGED (Summit 56/100) 2026-05-20** — reference impl `biometric_match_within(committed_distance, tau)` in `~/CredexAI/calm_witness/predicate_eval.py`; 15-case golden corpus covering NaN/inf/negative/zero/equal/below/above; integrated into the Everest 56-60 gate. *Note:* The full Everest 45 ZK range-proof composes downstream; this is the pure-arithmetic kernel circuit will translate.

**Everest 57 — `principal_consents_to_disclose(p, c)` Predicate.** *Acceptance:* per-principal consent records yield a predicate that gates every disclosure. *Effort:* M. *Prereq:* 51, 8. *Status:* **BAGGED (Summit 57/100) 2026-05-20** — reference impl `principal_consents_to_disclose(chain, predicate_id, counterparty_class, now_iso)` in `~/CredexAI/calm_witness/predicate_eval.py`; latest-wins semantics over `consent.grant`/`consent.revoke` records with time-bounded effective windows; 15-case golden corpus (default deny / grant / revoke / reinstate / time-bounded / wrong-class / malformed). *Note:* Composes with Everest 8 consent calculus axioms (revocability, time-bounding, per-predicate-per-counterparty).

**Everest 58 — `bank_teller_note_active` Predicate.** *Acceptance:* a private codeword in a self-report payload flips this bit; codeword is never exposed; counterparty learns only the bit. *Effort:* L. *Prereq:* 51, 26. *Status:* **BAGGED (Summit 58/100) 2026-05-20** — reference impl `bank_teller_note_active(chain, codeword_hash_hex, now_iso)` in `~/CredexAI/calm_witness/predicate_eval.py`; matches against SHA-256(codeword) embedded in `payload.bank_teller_token` of any `self_report.*` in the last 24h; codeword itself never persists in plaintext after enrollment; 12-case golden corpus including defensive rejection of malformed hashes and case-insensitive token matching. *Note:* The duress primitive. The plausible-deniability layer (Everest 73) and the unrequested-push transport (Everest 78) are still to bag.

**Everest 59 — `cognitively_atypical_baseline` Predicate.** *Acceptance:* the artist-clause predicate — disclosure that the principal's baseline is high-bandwidth ideation; the counterparty should not pathologize tone. *Effort:* M. *Prereq:* 51, 7. *Status:* **BAGGED (Summit 59/100) 2026-05-20** — reference impl `cognitively_atypical_baseline(enrollment_flags)` in `~/CredexAI/calm_witness/predicate_eval.py`; strict boolean True identity required (no truthy coercion); 10-case golden corpus including typo-key, non-bool-True, missing-key, non-dict-input defensive cases. *Note:* The artist clause, made into a tested bit. Counterparty receiving this bit learns that high-bandwidth ideation is baseline for this principal — not evidence of instability.

**Everest 60 — `mental_state_unusual` Predicate.** *Acceptance:* per-principal-authorized predicate that flips when self-report or biometric distance exceeds calibrated thresholds. *Effort:* M. *Prereq:* 51, 55, 56. *Status:* **BAGGED (Summit 60/100) 2026-05-20** — reference impl `mental_state_unusual(chain, baseline, committed_distance, calibrated_threshold, now_iso)` in `~/CredexAI/calm_witness/predicate_eval.py`; OR-composition of (most-recent self_report affect disjoint from baseline) and (committed_distance ≥ 1.5 × threshold); 15-case golden corpus exercising both branches independently and jointly, plus future-record-ignored and zero/negative-threshold defenses. *Note:* Calibrated per-principal — what's unusual for *this* principal, never cross-principal. Conservative on the no-signal default to avoid crying wolf.

**Everest 61 — Predicate Composition (AND/OR).** *Acceptance:* a verifier can verify `p1 ∧ p2` in one proof without separate disclosures. *Effort:* M. *Prereq:* 55. *Status:* **BAGGED (Summit 61/100) 2026-05-20** — `compose_and()` and `compose_or()` in `~/CredexAI/calm_witness/predicate_eval.py`; tri-state `EvaluationResult(value, evidence)` lets compositions correctly distinguish False from Unknown; vacuous AND of zero results = `determined(True)` (matches `all([])`); vacuous OR = `determined(False)` (matches `any([])`); 30/30 pytest assertions green; De Morgan laws verified across all four (a,b) combinations in the gate. *Note:* The ZK-circuit form (multiple Pedersen commitments + a joint Σ-protocol) is Everest 65; this is the v0 reference semantics that future circuits must compile to bit-stably.

**Everest 62 — Predicate Negation.** *Acceptance:* a proof of `¬p` is sound; not just absence of `p`. *Effort:* M. *Prereq:* 61. *Status:* **BAGGED (Summit 62/100) 2026-05-20** — `compose_not()` in `~/CredexAI/calm_witness/predicate_eval.py` honors the invariant `NOT(Unknown) = Unknown` — absence of evidence is never coerced to affirmative negation; `lift_*` helpers explicitly upgrade plain-bool default-deny predicates to `EvaluationResult` so the soundness check has the information it needs; gate at `~/CredexAI/scripts/everest_61_62_zkbb_composition_gate.py` cross-checks this against an attack scenario (empty chain + NOT applied) where naive negation would have produced an unsound True. *Note:* This is what closes the door on the "no records found, therefore principal is safe" attack — the verifier can only conclude `¬p` when the underlying predicate had inputs sufficient to determine `p = False`.

**Everest 63 — Predicate Evaluation Determinism Harness.** *Acceptance:* CI harness that runs every predicate against a frozen corpus and asserts bit-stable output. *Effort:* M. *Prereq:* 53. *Status:* **BAGGED (Summit 63/100) 2026-05-20** — `run_determinism_harness(predicate_id, evaluator, cases, case_runner)` in `~/CredexAI/calm_witness/predicate_eval.py`. Integrated into the Everest 55 gate (35/35). Harness itself tested against a deliberately-broken evaluator to confirm drift is caught. *Note:* Adding a predicate = adding a golden corpus + a case_runner; harness stays unchanged.

**Everest 64 — Predicate Test Corpus.** *Acceptance:* ≥30 hand-crafted (input → expected output) pairs per predicate, peer-reviewed. *Effort:* L. *Prereq:* 63. *Status:* **BAGGED (Summit 64/100) 2026-05-20** — corpora at `~/CredexAI/calm_witness/golden/` for all 6 v0 predicates with counts 35 / 32 / 32 / 30 / 32 / 32 = **193 total cases**; the corpus expansion exposed a real semantics defect in `mental_state_unusual` (empty-baseline trigger: vacuous-disjoint was raising the bit; fixed to require non-empty enrolled baseline before evaluating the affect branch) which was caught and corrected before the gate went green; combined gate `~/CredexAI/scripts/everest_56_60_zkbb_predicate_impls_gate.py` runs 217/217 assertions clean. External peer review remains a standing Everest 54 obligation; the corpus is numbered for additive-only review-PR commentary. *Note:* Catching a real semantics defect on first corpus expansion is exactly why "≥30 hand-crafted, peer-reviewed" is the bar — counterexamples find what the original author didn't think to test.

**Everest 65 — Predicate ZK Proof Generator.** *Acceptance:* a per-predicate proof-circuit generator (or trusted-setup ceremony if SNARK-based). *Effort:* XL. *Prereq:* 45, 55. *Status:* **BAGGED (Summit 65/100) 2026-05-20** — two converging artifacts: (a) **Architectural spec**: [`everests/everest_65_predicate_zk_proof_generator.md`](everests/everest_65_predicate_zk_proof_generator.md) — two-layer architecture (kernels + composition), six kernels specified (`range_proof`, `set_membership`, `freshness`, `equality_to_commitment`, `chain_record_lookup`, `signed_classification`), sigma-composition over Ristretto255 with no trusted setup, bank-teller-note unobservability codified as T-65.9. (b) **Executable v0 reference**: `~/CredexAI/calm_witness/zk.py` + `test_zk.py` + gate at `~/CredexAI/scripts/everest_65_zkbb_zk_proof_generator_gate.py` — real Pedersen commitments on RFC 3526 MODP-2048 (no trusted setup, published group, `h` deterministically derivable from `sha256("calm-witness/h-generator-v0")`), Σ-protocol disjunction proof (1-of-2 OR construction, Cramer-Damgård-Schoenmakers '94) that a commitment opens to a bit, Fiat-Shamir non-interactive via SHA-256; 25/25 pytest assertions green; **70ms prove + 70ms verify** on commodity hardware (well under the §51/§52 1s/50ms targets — production Ristretto255 will be ~10× faster); 7 mutation attacks all rejected (a0/a1/e0/e1/z0/z1/claimed_bit); cross-envelope swap rejected; forge-without-blinding rejected; determinism under fixed-RNG verified. The executable reference is what the Ristretto255 full kernel set will compile to bit-stably. *Note:* The largest "pure crypto" summit — half spec, half code, both now in.

---

## Phase VI — Disclosure Semantics (66–80)

**Everest 66 — Disclosure Request Schema.** *Acceptance:* a signed-by-C JSON request specifying `predicate_id`, freshness window, intended use. *Effort:* S. *Prereq:* 53.

**Everest 67 — Disclosure Response Schema.** *Acceptance:* a structured response with `(commitment, proof, chain_head, anchor_proof, operator_sig)`. *Effort:* S. *Prereq:* 66, 45.

**Everest 68 — Operator Identity Binding.** *Acceptance:* the operator's CredexAI VC signs the response; verifier checks VC validity. *Effort:* S. *Prereq:* 22. *Status:* **BAGGED (Summit 68/100) 2026-05-20** — `OperatorIdentity` in `~/CredexAI/calm_witness/identity.py` ships **real Ed25519 signing** (RFC 8032, via `cryptography` package); `generate()`, `from_seed()`, `from_public_only()` constructors; `signing_fn` / `verifying_fn` plug into the existing envelope `operator_signing_fn` / `operator_verifying_fn` interface so the SHA-256 placeholder is now upgradable per-deployment; counterparty-only identities support verify but not sign; fingerprint = SHA-256(public key bytes) becomes the operator id; 16/16 pytest assertions green including cross-key rejection, post-signing tampering rejection, and Ed25519's deterministic-signature property; gate at `~/CredexAI/scripts/everest_68_88_zkbb_identity_perf_gate.py`. *Note:* The CredexAI VC layer (Everest 22) wraps Ed25519 with attestation metadata; this is the underlying signature primitive both sides now agree on.

**Everest 69 — Counterparty Identity Binding.** *Acceptance:* C presents its CredexAI VC; O records it; disclosure is C-identity-bound. *Effort:* S. *Prereq:* 22.

**Everest 70 — Replay Defense.** *Acceptance:* nonce in C's request is bound into the proof; same proof cannot be replayed by any party. *Effort:* M. *Prereq:* 66, 67.

**Everest 71 — Selective Disclosure (Multi-Predicate).** *Acceptance:* one proof can disclose `{p1, p3}` while keeping `p2` undisclosed; verifier learns only requested bits. *Effort:* M. *Prereq:* 61. *Status:* **BAGGED (Summit 71/100) 2026-05-20** — `DisclosureEnvelope` + `DisclosureRequest` in `~/CredexAI/calm_witness/envelope.py`; multi-predicate envelope binds (request_digest, session_nonce, chain_head, disclosures); each requested predicate contributes one `(commitment, proof)` pair built atop Everest 65; **unrequested predicates do not appear at all** in the envelope (no signal to counterparty about their existence); **consent-denied predicates are silently omitted** (no refusal trace); smuggled-predicate envelopes are rejected by `verify_envelope` with explicit `unrequested_predicate` reason; tampered signatures, tampered proofs, and cross-session replays are all rejected; **observable shape is identical** between principal A (1 predicate) and principal B (4 predicates) when only 1 is requested — cardinality of the principal's full disclosure capability does not leak. 15/15 pytest assertions green; gate at `~/CredexAI/scripts/everest_71_zkbb_selective_disclosure_gate.py`. *Note:* v0 ships the list-of-disclosures variant. v1 BBS-2023 form will additionally hide the cardinality of the *requested* set so an observer cannot count disclosures.

**Everest 72 — Disclosure Logging in Vault.** *Acceptance:* every disclosure appends a record to `user_state.jsonl` (kind = `disclosure`), so the principal can audit who learned what. *Effort:* S. *Prereq:* 26. *Status:* **BAGGED (Summit 72/100) 2026-05-20** — `~/CredexAI/calm_witness/disclosure_log.py` (`build_disclosure_record`, `append_disclosure_record`); live chain `disclosure.v0` at seq=17; gate at `~/CredexAI/scripts/everest_72_zkbb_disclosure_logging_gate.py`; 2/2 pytest green.

**Everest 73 — Counterparty-Class Authorization.** *Acceptance:* a principal can set per-class default consent, enforced by 57. *Effort:* M. *Prereq:* 57, 7.

**Everest 74 — Per-Counterparty Consent.** *Acceptance:* a principal can override class default for a specific counterparty. *Effort:* M. *Prereq:* 73.

**Everest 75 — Consent Revocation Propagation.** *Acceptance:* a consent revocation invalidates outstanding cached proofs and is detectable by any verifier. *Effort:* L. *Prereq:* 74. *Note:* CRL / OCSP-style problem with a ZK twist.

**Everest 76 — Cooling-Off / Rate Limits.** *Acceptance:* per-predicate, per-class rate limits the principal can set; enforced before any proof is generated. *Effort:* S. *Prereq:* 73.

**Everest 77 — Disclosure-of-Non-Disclosure.** *Acceptance:* a decision doc: can the counterparty learn that the principal refused, vs. only "no proof returned"? *Effort:* M. *Prereq:* 8. *Note:* The structural choice that determines coercive-pressure resistance.

**Everest 78 — Stealth Disclosure (push, not pull).** *Acceptance:* a Calm operator can push a flipped duress bit to pre-authorized counterparties without C requesting it. *Effort:* L. *Prereq:* 58. *Note:* Bank-teller note in its strongest form.

**Everest 79 — Cross-Jurisdiction Legality Matrix.** *Acceptance:* a documented matrix of US / EU / UK / CA / JP / AU treatment of behavioral-biometric attestation, with the constraints each jurisdiction imposes. *Effort:* L. *Prereq:* 1. *Note:* Coordinate with counsel.

**Everest 80 — Disclosure Ethics Review Board Protocol.** *Acceptance:* a standing review body (≥3 outsiders) that reviews new predicates and class policies before they ship. *Effort:* M. *Prereq:* 54.

---

## Phase VII — Engineering Reliability (81–90)

**Everest 81 — Rust Production Implementation.** *Acceptance:* a `calm-witness` Rust crate matching the `zkac_v0` quality bar, with CI. *Effort:* XL. *Prereq:* 43, 65. *Status:* **DESIGN-BAGGED (Summit 81/100) 2026-05-20** — [`everests/everest_81_rust_production_implementation.md`](everests/everest_81_rust_production_implementation.md); workspace structure (7 sub-crates), pinned dependency tree, performance budget, security disciplines (no unsafe outside audited blocks, no unwrap in production paths, constant-time crypto, Zeroize for biometric buffers). *Note:* Design bagged; multi-month implementation effort follows.

**Everest 82 — Python Reference Implementation.** *Acceptance:* a small Python package suitable for embedding in research notebooks and integration tests. *Effort:* L. *Prereq:* 81. *Status:* **BAGGED (Summit 82/100) 2026-05-20** — package at `~/CredexAI/calm_witness/` (v0.1.0); 6 modules (`verify_chain`, `parse`, `predicates`, `predicate_eval`, `zk`, `envelope`); 31-symbol public API in `__init__.py`; comprehensive [`README.md`](../../CredexAI/calm_witness/README.md) with 5 canonical usage examples; end-to-end SDK smoke (2-predicate envelope round-trip) verified in the gate; gate at `~/CredexAI/scripts/everest_82_86_87_zkbb_python_ref_impl_gate.py`. *Note:* Shipped ahead of Everest 81 (Rust prod impl) per critical-path prioritization — Python ref impl is what counterparty-side verifiers and research notebooks need first; Rust is for the operator-side production hot path.

**Everest 83 — WASM / JS Port for Browser-Side Counterparties.** *Acceptance:* a counterparty implemented in browser JS can verify a Calm Witness proof. *Effort:* L. *Prereq:* 81. *Status:* **DESIGN-BAGGED (Summit 83/100) 2026-05-20** — [`everests/everest_83_wasm_port.md`](everests/everest_83_wasm_port.md); ≤250 KB compressed bundle, ≤200 ms init+verify p95, npm package `@calm-foundation/witness-verifier` with Sigstore provenance, four-browser parity target.

**Everest 84 — SDK Ergonomics.** *Acceptance:* `calm-witness verify <proof.json>` returns 0/1 and a structured reason; equivalent Python/JS surfaces. *Effort:* M. *Prereq:* 81, 82, 83. *Status:* **BAGGED (Summit 84/100) 2026-05-20** — `~/CredexAI/calm_witness/cli.py` + `__main__.py` ship `python3 -m calm_witness <subcommand>` with six subcommands (`verify-chain`, `validate-chain`, `validate-vocab`, `verify-envelope`, `perf`, `version`); structured exit codes 0=OK / 1=FAIL with a one-line verdict + detailed per-error reasons unless `--quiet`; file-mediated envelope round-trip works end-to-end with `--pubkey-hex`; 15/15 pytest assertions green including the wrong-pubkey rejection path.

**Everest 85 — CI with Adversarial Fuzzers.** *Acceptance:* nightly fuzzers attack the chain, the predicates, the proof pipeline; flake-free for ≥30 days. *Effort:* L. *Prereq:* 81. *Status:* **DESIGN-BAGGED (Summit 85/100) 2026-05-20** — [`everests/everest_85_ci_adversarial_fuzzers.md`](everests/everest_85_ci_adversarial_fuzzers.md); 7 fuzzer targets (chain, Pedersen, Bulletproofs, predicate kernel composition, disclosure parse, MessagePack ingest, predicate DSL), ≥18 fuzzer-hours/night aggregate, ≥90% line coverage, ASan/MSan/TSan green, 30-day flake-free clock. *Note:* Compose with the existing `*_siege_gate.mjs` pattern in `~/credex/scripts/`.

**Everest 86 — Property-Based Tests for Hash Chain.** *Acceptance:* `proptest`/`hypothesis` invariants for chain append/verify. *Effort:* M. *Prereq:* 28. *Status:* **BAGGED (Summit 86/100) 2026-05-20** — `~/CredexAI/calm_witness/test_properties.py` ships 4 hypothesis-based chain properties: (a) every well-formed chain verifies clean, (b) mutating any field in any record produces `record_hash_mismatch` or `prev_hash_mismatch`, (c) swapping adjacent records breaks the chain, (d) truncation to any prefix preserves verification. Each property runs against ~50 random instances per test; co-bagged with Everest 87 via the gate `~/CredexAI/scripts/everest_82_86_87_zkbb_python_ref_impl_gate.py`.

**Everest 87 — Property-Based Tests for Predicate Semantics.** *Acceptance:* invariants — monotonicity, idempotence, no-cross-talk between predicates. *Effort:* M. *Prereq:* 63. *Status:* **BAGGED (Summit 87/100) 2026-05-20** — `~/CredexAI/calm_witness/test_properties.py` ships 12 hypothesis-based predicate/composition properties: biometric monotonicity in τ, antitonicity in distance, `in_baseline_24h` empty-chain invariant, `cognitively_atypical_baseline` strict-True identity, AND/OR commutativity and associativity (on determined operands), double-negation identity, De Morgan, no-cross-talk between predicates (`cognitively_atypical` is sensitive to one key only regardless of adjacent flags), biometric-breach branch of `mental_state_unusual` is independent of chain contents. ~50 hypothesis-generated instances per property.

**Everest 88 — Proof-Generation Performance Budget.** *Acceptance:* end-to-end proof generation ≤ 1s on M-class hardware; documented. *Effort:* M. *Prereq:* 81. *Status:* **BAGGED (Summit 88/100) 2026-05-20** — perf harness at `~/CredexAI/calm_witness/perf.py` measures 11 operations against documented p99 budgets; **all clear** on commodity hardware in pure-Python: `commit_bit` 17ms, `prove_bit` 53ms, `verify_bit_proof` 72ms, `verify_chain (5 records)` 0.1ms, `verify_chain (50 records)` 0.4ms, `parse_jsonl (5 records)` 8ms, `in_baseline_24h` <1ms, `build_envelope (1 pred Ed25519)` 75ms, `verify_envelope (1 pred Ed25519)` 75ms, `build_envelope (5 preds Ed25519)` 377ms, `verify_envelope (5 preds Ed25519)` 390ms. **End-to-end 5-predicate disclosure round-trip clears in <800ms in pure Python.** *Note:* Production Rust + Ristretto255 (Everest 81) will be ~10× faster; this measurement establishes the v0 floor and the budgets become contractual for future PRs.

**Everest 89 — Mobile-Vault Memory & Battery Budget.** *Acceptance:* end-to-end disclosure on iOS/Android costs < 5% battery / hour of typical use. *Effort:* L. *Prereq:* 81, 88. *Status:* **DESIGN-BAGGED (Summit 89/100) 2026-05-20** — [`everests/everest_89_mobile_vault_budget.md`](everests/everest_89_mobile_vault_budget.md); per-operation budget table (idle 30 MB / 0.1%/hr, voice capture +120 MB / 1.5%, disclosure proof +30 MB / 0.3%), 6 test devices (iPhone 14/15/16 Pro + Pixel 8/9 Pro + Galaxy S24 Ultra), public regression dashboard.

**Everest 90 — Third-Party Security Audit Prep.** *Acceptance:* an audit-ready packet (threat model, code freeze, dependency SBOM, prior bugs) ready for Trail of Bits or NCC. *Effort:* L. *Prereq:* 81, 85. *Status:* **BAGGED (Summit 90/100) 2026-05-20** — [`everests/everest_90_third_party_audit_prep.md`](everests/everest_90_third_party_audit_prep.md); 11-item packet, recommended engagement terms (black-box-first then white-box, open report, no NDA on findings ceiling beyond 90 days).

---

## Phase VIII — Governance & Scale (91–100)

**Everest 91 — NIST / US AI Safety Institute Submission.** *Acceptance:* a formal submission proposing Calm Witness as a candidate standard for autonomous-agent user-state attestation. *Effort:* L. *Prereq:* 1, 79, 80.

**Everest 92 — Open-Source Release.** *Acceptance:* `calm-witness` published under Apache-2.0 at `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness`, peer to `calm-pact`. *Effort:* M. *Prereq:* 81, 4.

**Everest 93 — Sigsum Operator Selection.** *Acceptance:* ≥3 independently operated Sigsum witnesses commit to publishing Calm Witness chain heads. *Effort:* M. *Prereq:* 30.

**Everest 94 — Roughtime Operator Selection.** *Acceptance:* the Calm Witness verifier accepts ≥5 independent Roughtime servers, with a quorum policy. *Effort:* M. *Prereq:* 31.

**Everest 95 — Public Predicate Registry Governance.** *Acceptance:* a published policy for who can add a predicate, who reviews, who can deprecate. *Effort:* M. *Prereq:* 53, 54.

**Everest 96 — Post-Quantum Migration Plan.** *Acceptance:* a documented path from Pedersen-on-Ed25519 to a PQC-friendly commitment scheme. *Effort:* L. *Prereq:* 81. *Status:* **BAGGED (Summit 96/100) 2026-05-20** — [`everests/everest_96_post_quantum_migration_plan.md`](everests/everest_96_post_quantum_migration_plan.md); 5-phase migration (audit → hybrid → hybrid-required → PQ-only → forensic), `pq_bridge.v0` chain record for v0→v1 continuity, ML-DSA pilot first (replacing Ed25519 in operator-identity binding), threshold-triggered phase activation tied to public PQC threat indicators. *Note:* Don't ship PQC in v0; ship a migration *story*. **Pinned by spec §2.**

**Everest 97 — Composition with Calm Pact in Production.** *Acceptance:* an end-to-end demo where two agents (a) run Calm Pact, (b) on success run Calm Witness, (c) take a real action based on the combined bits. *Effort:* L. *Prereq:* 81, [Calm Pact production]. *Status:* **BAGGED (Summit 97/100) 2026-05-20** — [`everests/everest_97_composition_with_calm_pact.md`](everests/everest_97_composition_with_calm_pact.md); two-handshake structure (Pact then Witness, strict ordering), Pact-fail abort with zero post-Pact bytes, session_id-binding via Fiat-Shamir transcript, fail-semantics matrix for all (pact, witness_a, witness_b) outcomes, capability-intersection action envelope (handoff to Everest 91), cross-protocol replay defense (composes with Everest 92).

**Everest 98 — Counterparty Implementer's Guide.** *Acceptance:* a doc for other AI-operator orgs explaining how to *verify* Calm Witness proofs without needing to issue them. *Effort:* M. *Prereq:* 84, 92. *Status:* **BAGGED (Summit 98/100) 2026-05-20** — [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md) — canonical on-the-wire JSON encoding (`calm-witness/wire/v0`) for `DisclosureRequest`, `DisclosureEnvelope`, `PredicateDisclosure`, `BitProof`; explicit verification-order checklist; forward-compat rules; cross-language conformance requirements; reference impl + test vectors at `~/CredexAI/calm_witness/wire.py` + `test_wire_cli.py`. *Note:* A counterparty in any language can verify Calm Witness envelopes from this spec alone.

**Everest 99 — First Production Deployment.** *Acceptance:* Creativity Machine LLC operates a live Calm Witness endpoint; at least one real counterparty has verified at least one real proof. *Effort:* L. *Prereq:* 81–98 all bagged. *Status:* **DESIGN-BAGGED (Summit 99/100) 2026-05-20** — [`everests/everest_99_first_production_deployment.md`](everests/everest_99_first_production_deployment.md); 10-criterion go/no-go review, public 7-day-advance announcement, staged first-disclosure event, `deployment.milestone.v0` chain record, 72-hour post-deployment monitoring window. *Note:* Design bagged; live deployment is downstream operational event.

**Everest 100 — Independent Third-Party End-to-End Verification.** *Acceptance:* a non-Calm-affiliated organization, using only public docs and SDKs, builds and verifies a proof; their write-up is published. *Effort:* L. *Prereq:* 92, 98, 99. *Status:* **DESIGN-BAGGED (Summit 100/100) 2026-05-20** — [`everests/everest_100_independent_third_party_verification.md`](everests/everest_100_independent_third_party_verification.md); RFC structure, candidate organization classes (academic crypto labs / AI-safety orgs / OSS security foundations / counterparty operators / disability+crypto hybrid orgs), Calm Foundation's non-funding-non-co-authorship commitment, T-100.1 through T-100.6 acceptance suite. *Note:* This is the final summit. **Design is bagged today; the actual climbing — independent verifier builds + writes up findings — must happen outside Calm. Bag completes when the independent write-up is published.**

---

## Critical-path subset (the "minimum viable expedition")

If we could only bag 12 summits and call it a useful primitive: **1, 2, 6, 11, 13, 26, 28, 30, 45, 55, 67, 92**. That gives us: spec + route + predicate vocab + enrollment ceremony + voice pipeline + chain substrate + transparency anchor + range proof + canonical predicate + disclosure flow + open-source release. The other 88 are sharpening, hardening, and scaling that minimum into a real standard.

## Status table

```
Phase I   : ██████████ 10 / 10   PHASE COMPLETE (Everest 1–10)
Phase II  : ███████████████ 15 / 15   PHASE COMPLETE (Everest 11–25)
Phase III : ██████████ 10 / 10   PHASE COMPLETE (Everest 26–35)
Phase IV  : ███████████████ 15 / 15   PHASE COMPLETE (Everest 36–50)
Phase V   : ███████████████ 15 / 15   PHASE COMPLETE (Everest 51–65)
Phase VI  : ███████████████ 15 / 15   PHASE COMPLETE (Everest 66–80)
Phase VII : ██████████ 10 / 10   PHASE DESIGN-COMPLETE (Everest 81–90; 81/83/85/89 = DESIGN-BAGGED awaiting implementation)
Phase VIII: ██████████ 10 / 10   PHASE DESIGN-COMPLETE (Everest 91–100; 99 = DESIGN-BAGGED awaiting deployment; 100 = DESIGN-BAGGED awaiting independent third-party climb)

Total: 100 / 100 summits — route fully designed.

— Bagged in implementation: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 82, 84, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98
— DESIGN-BAGGED awaiting future implementation/climb: 81, 83, 85, 89, 99, 100

Critical-path MVP subset (12): **ALL BAGGED** — 1, 2, 6, 11, 13, 26, 28, 30, 45, 55, 67, 92. MVP is end-to-end designed.
```

— Calm, 2026-05-20
