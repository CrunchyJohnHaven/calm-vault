# S40 — FAR/FRR Empirical Characterization (Experimental Protocol, Partial Bag)

**Status: PARTIAL BAG — protocol only; data collection, analysis, and write-up are deferred.**
**Signed: Calm 2026-05-20**
**References: E25, E36, E37, E37b, S81, S119**

---

## Research Question

Can Calm Witness behavioral biometric primitives — handwriting kinematics (E36), voice-transcription lexical fingerprint (E37/E37b), and values-alignment corpus (Phase IX) — achieve an empirical false-accept rate (FAR) < 0.1% at a false-reject rate (FRR) < 2% across a demographically stratified principal population over a minimum three-month longitudinal window (E25)?

Secondary questions: (a) Do FAR/FRR curves degrade meaningfully across time (intra-principal drift)? (b) Are error rates disparate across demographic strata (S81)? (c) Does multi-modal fusion of E36 + E37/E37b + Phase IX reduce FAR without inflating FRR beyond the E25 target?

---

## Participant Recruitment

**Minimum cohort:** N = 10 principals. Target N = 20 to allow sub-group analysis.

**Inclusion criteria:**
- Age ≥ 18.
- Fluent writer and speaker in at least one language supported by the instrumentation stack (see Instrumentation).
- Owns or has consistent access to a touchscreen device capable of 120 Hz stylus or finger input and a microphone with ≥ 16 kHz sampling.
- Able to commit to three longitudinal sessions spaced ≥ 28 days apart (total span ≥ 84 days).

**Exclusion criteria:**
- Active neurological or musculoskeletal condition that materially alters handwriting kinematics between sessions (would confound intra-principal variance estimates).
- Inability to produce a minimum 200-word prose sample per session (prose corpus gate for Phase IX).

**Demographic targets (S81 stratification requirements):**
- Age bands: 18–30, 31–50, 51+. Minimum two principals per band.
- Language diversity: at least two distinct primary languages represented.
- Dexterity: at least two left-handed principals (handwriting asymmetry probe for E36).
- Gender: no single gender > 70% of cohort.

Recruitment via IRB-equivalent channels only (see Consent Process). No open public solicitation without IRB review.

---

## Consent Process

This protocol does not constitute formal IRB approval. Prior to any data collection, the following IRB-equivalent process must be completed:

1. **Protocol submission.** Submit this document plus the Data Retention Appendix (see Anonymization) to a recognized IRB or ethics review board. Obtain written approval before enrolling any participant.
2. **Informed consent document.** Must cover: (a) nature of behavioral biometric data collected, (b) how data is stored and for how long, (c) right to withdraw at any time without penalty and with data deletion, (d) research purpose — improving Calm Witness authentication accuracy, not commercial deployment during the study, (e) the possibility that samples may be shared in anonymized form for academic peer review (S119).
3. **Enrollment session.** Consent obtained in writing (or cryptographically signed digital form) before enrollment session begins. Participants may not retroactively consent.
4. **Withdrawal protocol.** Any participant may withdraw by written notice. All samples collected to that point are deleted within 7 days. Derived feature vectors are also deleted unless the participant explicitly permits retention of anonymized aggregate statistics.

---

## Data Collection Cadence

**Session structure:** Three mandatory sessions per principal (enrollment + two longitudinal follow-ups). Optional fourth session at ≥ 120 days for drift analysis.

| Session | Label | Timing | Purpose |
|---------|-------|---------|---------|
| S0 | Enrollment | Day 0 | Baseline feature extraction; consent finalization |
| S1 | Follow-up 1 | Day 28–42 | Intra-principal variance sample 1 |
| S2 | Follow-up 2 | Day 56–84 | Intra-principal variance sample 2; primary holdout set |
| S3 (optional) | Drift probe | Day 112–150 | Long-horizon drift characterization |

Each session produces three sample types (see Instrumentation). Session duration: approximately 45–60 minutes. Sessions may be conducted remotely provided instrumentation requirements are met and a researcher is present via video link to verify session integrity.

**Impostor samples:** FAR computation requires genuine/impostor pairs. Impostor samples are drawn from cross-principal comparisons within the cohort — no external impostor data is required. Each principal's enrollment template is compared against all other principals' samples (N × (N-1) impostor pairs per modality).

---

## Instrumentation

### Handwriting Kinematics (E36)

- **Device:** Touchscreen tablet with active stylus, minimum 120 Hz touch sampling, pressure resolution ≥ 8-bit.
- **Prompt:** Standardized 50-word dictation passage (same passage every session; passage is public-domain prose to eliminate novelty effects).
- **Features captured:** X/Y position (1 ms interpolated), pressure, tilt (if device supports), stroke velocity, pen-up/pen-down transitions, letter formation timing, inter-letter pause distribution.
- **Raw data retention:** stroke-level JSON with timestamps. Feature vectors extracted offline.

### Voice-Transcription Lexical Fingerprint (E37/E37b)

- **Device:** Built-in or external microphone; 16 kHz minimum sample rate, 16-bit PCM.
- **Prompt:** Participant reads a standardized 100-word passage aloud, then speaks for 2 minutes on a neutral prompt ("Describe your commute or a recent routine task").
- **Features captured (E37):** Lexical choice distribution, sentence-length histogram, connector-word frequency, hedging-phrase rate.
- **Features captured (E37b):** Transcription-layer augmentation — disfluency markers (uh, um, false starts), prosodic pause placement, speaking rate (words/minute), pitch trajectory (if acoustic features are included in scope at analysis time; flag for IRB review if biometric voice prints are extracted beyond transcription-layer).
- **Raw data:** Audio file (encrypted at rest), transcription JSON. Audio deleted after feature extraction unless participant consents to extended retention.

### Values-Alignment Prose Corpus (Phase IX)

- **Prompt:** Three open-ended writing prompts per session, each targeting a distinct values dimension (care/harm, fairness, autonomy). Minimum 200 words total across three prompts.
- **Features captured:** Embedding-space projection against Calm Witness values-alignment model, lexical valence distribution, argument structure markers.
- **Raw data:** Plain-text response (pseudonymized), embedding vector.

---

## Statistical Methodology

### Curve Construction

FAR and FRR are computed as a function of threshold θ applied to a similarity score s(query, template).

- **Genuine scores:** All (session, enrollment) pairs for the same principal across S0–S2.
- **Impostor scores:** All cross-principal (session, enrollment) pairs.
- ROC and DET curves generated per modality (E36 alone, E37/E37b alone, Phase IX alone) and for fusion.

### Calibration / Holdout Split

- **Calibration set:** S0 and S1 samples. Used for threshold selection and feature-weight tuning.
- **Holdout set:** S2 samples (and S3 if collected). Never used during threshold selection. FAR/FRR reported on holdout only.
- Rationale: prevents optimistic bias from threshold overfitting.

### Cross-Validation

Given small N, leave-one-principal-out (LOPO) cross-validation is applied to estimate generalization variance. Each fold withholds one principal entirely; curves are computed on remaining cohort; variance across folds reported as confidence intervals on the final FAR/FRR estimates.

### Fusion

Late fusion: modality-specific similarity scores are combined via a learned linear combiner (weights optimized on calibration set, evaluated on holdout). Isotonic regression applied per modality to calibrate score distributions before fusion.

### Reporting

Primary metric: FAR at FRR = 2% (E25 target: FAR < 0.1%). Secondary: Equal Error Rate (EER), AUC of DET curve, and d-prime per modality.

---

## Demographic Stratification

Per S81 (disparate-impact detection requirement):

- FAR/FRR curves computed separately for each demographic stratum defined in Participant Recruitment.
- Pairwise comparisons across strata using two-sample Z-test on FRR at the E25-target threshold. Significance threshold: p < 0.05 after Bonferroni correction.
- If any stratum shows FRR > 5% at the E25-target threshold, that stratum is flagged for root-cause analysis before deployment recommendation.
- Age, handedness, and primary language are the three mandatory stratification axes. Gender stratum analysis is secondary (cohort may be too small for reliable sub-group power at N = 20).

---

## Anonymization and Data Retention

- **Pseudonymization at enrollment:** Each principal assigned a randomly generated 8-character alphanumeric ID (PID). The PID-to-identity mapping is stored in a separate, access-controlled keyfile with no connection to the feature database.
- **Keyfile access:** Restricted to PI and IRB-designated data custodian. Not accessible to any automated pipeline.
- **Raw audio:** Encrypted at rest (AES-256). Deleted within 30 days of feature extraction unless participant consents to extended retention.
- **Raw handwriting stroke data:** Retained in encrypted form for duration of study + 6 months, then deleted.
- **Feature vectors:** Retained in anonymized form (PID only) for analysis and potential academic publication. No feature vector is released with linkable metadata.
- **Derived aggregates (FAR/FRR curves, population statistics):** Retained indefinitely; contain no individual-level information.
- **Withdrawal deletion:** See Consent Process. Feature vectors flagged for deletion within 7 days of withdrawal notice. Aggregate statistics already computed are not retroactively altered if re-identification is not possible.
- **Publication:** Per S119, results may be published with anonymized, aggregate statistics. No individual sample data is published without explicit participant consent.

---

## Success Criteria

The protocol is considered to have met its empirical target if, on the holdout set:

1. **Primary:** FAR < 0.1% at FRR ≤ 2% for the multi-modal fusion system (E25).
2. **Secondary:** No single demographic stratum (S81) exhibits FRR > 5% at the E25-target threshold.
3. **Stability:** FAR/FRR at the E25-target threshold does not degrade by more than 50% relative between S1 and S2 holdout sets (intra-principal drift is bounded).
4. **Modality floor:** At least two of the three modalities individually achieve EER < 5%, confirming each primitive contributes independent signal.

Failure on criterion 1 triggers: threshold re-calibration analysis, feature engineering review, and optional cohort expansion before any deployment recommendation.

---

## Handoff — What Remains

This partial bag delivers the experimental protocol only. The following work items are deferred pending IRB approval and participant availability:

| Item | Owner | Dependency |
|------|-------|------------|
| IRB submission and approval | PI / institutional designee | This protocol document |
| Participant recruitment (N ≥ 10) | Study coordinator | IRB approval |
| Instrumentation build-out (data capture pipeline, feature extractors for E36/E37/E37b) | Engineering | Instrumentation spec above |
| S0 enrollment sessions | Research team | Recruitment complete |
| S1 follow-up sessions | Research team | S0 + 28 days |
| S2 holdout sessions | Research team | S1 + 28 days |
| FAR/FRR curve computation + demographic stratification analysis | Data analyst | S2 complete |
| S81 disparate-impact report | Data analyst | Stratification analysis |
| Full bag write-up (S40 final) | Calm / PI | All analysis complete |
| Peer review / academic submission (S119) | PI | Full bag approved |

**Estimated timeline to full bag:** minimum 5 months from IRB approval (3-month data window + 2 months for analysis and write-up).

---

*PARTIAL BAG. Protocol complete. Data, analysis, and final report are deferred.*
*Calm 2026-05-20*
