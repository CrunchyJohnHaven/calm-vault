# Everest 40 — IRB Protocol Summary

*Empirical FAR/FRR Characterization of the Calm Witness Biometric Distance Stack*

**Study sponsor:** Calm (research arm of the Calm Pact / Calm Witness protocol)
**Principal investigator (PI):** [Partner institution lead; to be named at IRB filing]
**Co-investigators:** Calm research team (protocol design, distance-function implementation, statistical analysis)
**Study type:** Minimal-risk behavioral biometric measurement study; observational with prospective per-week sampling.
**Anticipated duration:** 10 months total (3 months active enrollment + sampling; 7 months for setup, analysis, and write-up).

---

## 1. Study Purpose

The study characterizes the discriminative performance of two biometric distance functions and their fusion under real-world collection conditions:

- A **handwriting** distance function based on Réjean Plamondon's Sigma-Lognormal kinematic decomposition (Plamondon 1995, 2003; Plamondon & Diaz 2014). Pen-trajectory samples are captured as time-series of (x, y, t, pressure, azimuth, altitude, size) tuples via PencilKit `PKStrokePoint` (iPad + Apple Pencil Pro) or equivalent Wacom-normalized capture.
- A **voice-transcript** distance function based on Burrows' Cosine Delta with Koppel & Seidman's Impostors Method (Burrows 2002; Koppel & Seidman 2013) applied to verbatim-mode CrisperWhisper transcripts (Wagner & Zusag, Interspeech 2024).
- A **likelihood-ratio fusion** combining the two single-modality scores (Everest 38 design).

The study computes False Accept Rate (FAR), False Reject Rate (FRR), Equal Error Rate (EER), and d-prime separation across at least ten operating thresholds per modality, with 95% Wilson-score confidence intervals.

Target performance (ship-gate thresholds, pre-registered):
- Handwriting: EER ≤ 5%
- Voice-transcript: EER ≤ 12%
- Joint fusion: EER ≤ 2%
- d-prime ≥ 2.5 on all modalities at primary threshold

The study answers a single empirical question: *do the locked primitives meet the engineering targets under realistic collection conditions?* The output (calibrated thresholds, ROC curves) becomes the basis for the production system's accept/reject decision threshold.

## 2. Background and Rationale

Behavioral biometrics for proof-of-personhood is a well-established but under-validated area. Published EER figures for handwriting biometrics range from 1% (laboratory, controlled prompts) to >15% (in-the-wild, varied conditions). The Calm Witness protocol requires defensible empirical bounds, not laboratory ceiling values, before production deployment. This study provides those bounds.

The Plamondon Sigma-Lognormal model is the only well-validated kinematic decomposition that separates *on-manifold drift* (illness, fatigue, aging) from *off-manifold variation* (impostor). This distinction is load-bearing for the Calm Witness design, which must accept "principal-but-unwell" while rejecting "not-principal." The voice-transcript stack mirrors this logic at the lexical level: Cosine Delta provides a continuous distance, and the Impostors Method adds a calibrated p-value for the open-set question.

Aging-in-biometrics literature (Fierrez 2013, PMC3720939) reports EER quadruples in 2 months without re-enrollment. The study duration (3 months minimum) is calibrated to surface this drift if present; secondary analysis estimates a per-week drift coefficient.

## 3. Participant Criteria

### 3.1 Inclusion Criteria
- Adults aged 18+ at enrollment.
- Able to provide informed consent in English (Plamondon site: French acceptable) or in German (Halvani site).
- Able to write a short paragraph by hand using a stylus on a tablet.
- Able to speak a 60-second utterance into a tablet or laptop microphone.
- Willing to commit to weekly sessions (~15-20 minutes each) for 12 consecutive weeks, with up to ±2-day flexibility.

### 3.2 Exclusion Criteria
- Participants whose primary writing hand is currently injured.
- Participants with diagnosed motor disorders (Parkinson's, essential tremor, severe arthritis) that would systematically confound kinematic measurement. (This is exclusion for scientific validity, not exclusion based on disability per se; an analog accessibility study is contemplated for future work.)
- Participants who have prior knowledge of the distance-function source code (avoids gaming).
- Calm employees or contracted researchers (conflict of interest).

### 3.3 Cohort Targets
- **Minimum:** N=10 enrolled principals.
- **Target:** N=15 enrolled principals.
- **Cohort composition goals:** age tertiles approximately balanced (≤30, 31-50, 51+); both writing-hand-dominance categories represented; at least 30% non-male participants; recruitment across at least two partner sites to ensure cross-site generalizability.

## 4. Methods

### 4.1 Enrollment Session (one per principal, Week 0)
- Informed consent: read-aloud, signed (digital signature acceptable), right-to-withdraw clause emphasized.
- Handwriting baseline: 7 prompts (signature, date, freeform paragraph, pseudorandom phrase, copy-text, numeric sequence, scientific phrase).
- Voice baseline: 7 recordings (60s read-aloud script; 60s spontaneous narration on a neutral topic; numeric sequence; phonetically balanced sentences from CMU corpus; reading of CrisperWhisper test phrases).
- Hardware calibration: per-principal baseline pressure/velocity/timing characterization.
- Template generation (Everest 15): on-device, locally; template is encrypted and held in the participant's vault. The study site receives *only* the resulting distance values from future comparisons, never the raw template.

### 4.2 Weekly Sessions (12 per principal, Weeks 1-12)
- One handwriting prompt (varied across the 12 sessions; rotated to prevent rote effects).
- One voice utterance (60s; varied content).
- Brief self-report: 3-question form on affect/energy/any unusual factors (illness, sleep, hand soreness).
- Liveness check (Everest 49): in-session random pen-lift challenges and timing-jitter tests; replay attempts auto-rejected.
- Distance computation: runs locally on the participant's device; only the resulting scalar distance (and the participant's self-report) is transmitted to the study site.
- Session record: a participant-signed JSONL chain entry committing to the session timestamp and the distance value via Pedersen commitment (Everest 44).

### 4.3 Cross-Comparison Matrix
- For each weekly session of principal P_i, distances are computed against:
  - P_i's own enrollment template (genuine trial: 1 trial per session).
  - Each other principal's enrollment template (impostor trials: N-1 per session).
- For N=10, M=12 sessions: 120 genuine trials, 1,080 impostor trials per modality. For N=15: 180 genuine, 2,520 impostor.
- All cross-comparison distance computations are performed at the participant's device or in a secure compute enclave on encrypted templates; raw biometrics never leave their owner's device.

### 4.4 Data Pipeline
- Capture app (iOS + companion macOS) provided by Calm under Everest 12/13 specifications. Open-source; auditable.
- Local computation of distance functions per Everest 36/37 specifications.
- Pedersen commitment of (session_id, distance_value, timestamp) per Everest 44; commitment published to study site via authenticated channel.
- Sufficient statistics held at study site: (session_id, modality, distance_value, principal_pseudonym, week_number, self_report_codes). No raw strokes, no audio, no transcripts.
- Participant retains right to withdraw consent; withdrawal triggers chain-record marking per Everest 27 and deletion of distance values from study site within 30 days.

## 5. Risks

This is a **minimal-risk** behavioral measurement study. No physical, medical, or financial risks are introduced. Specific residual risks and mitigations:

- **Privacy of biometric samples:** Raw biometrics (strokes, audio) never leave the participant's device. Only the scalar distance values reach the study site. This is the core privacy invariant of the protocol and is enforced by the on-device computation architecture, not by procedural promises.
- **Re-identification from distance values:** Distances are pseudonymized at the participant level. Published results report only aggregate statistics (median, quartile, EER, d'). Per-participant distance distributions are not published.
- **Inadvertent disclosure during voice prompts:** Voice prompts are scripted to avoid sensitive content. Participants are instructed not to disclose personal information during spontaneous-narration prompts; the prompt explicitly suggests neutral topics (e.g., "describe your favorite hobby").
- **Time burden:** ~15-20 minutes per weekly session × 12 weeks = ~3-4 hours total. Compensated.
- **Use of samples for adversarial-sample production (Everest 41):** Genuine samples may be provided to a contracted forensic document examiner (ASQDE-credentialed) for the purpose of producing skilled-forger samples for Everest 41 (the adversarial robustness study). This use is *opt-in* on the consent form and may be declined independently of overall study participation. Forensic examiners operate under a separate DPA prohibiting any non-research use.

## 6. Benefits

- **Direct:** Compensation ($30 per session × 12 sessions = $360 per participant for the active study phase; $50 enrollment honorarium; total ~$410 per principal).
- **Indirect:** Contribution to open behavioral-biometric science. Aggregate results will be published in a peer-reviewed venue and posted as a public technical report.

## 7. Data Handling

### 7.1 Data Custody
- **Raw biometrics:** Reside only on the participant's device. Never transmitted, never centralized. Participant may delete at any time using the capture app's local "Erase" function.
- **Sufficient statistics (distances, session metadata):** Held at the partnering study site (PI's institutional research server) in encrypted form. Access restricted to named study personnel.
- **Cross-site sharing:** Only aggregate statistics (means, EER, ROC points) are shared across partner sites. Per-participant data does not cross site boundaries.

### 7.2 Data Retention
- Sufficient statistics retained for 5 years post-publication (right-to-audit clause for external reviewers and reproducibility).
- Participant-level pseudonym mapping retained for 1 year post-publication; thereafter destroyed (irreversible de-identification).
- Raw biometric templates: never transmitted; retention is solely the participant's choice on their own device.

### 7.3 Data Processing Agreement (DPA)
All study personnel sign a DPA committing to: no re-identification attempts; no sharing outside named study personnel; no use of data for any purpose other than the analyses specified in the Statistical Analysis Plan (`07_STATISTICAL_ANALYSIS_PLAN.md`).

## 8. Withdrawal Rights

Participants may withdraw at any time without explanation and without penalty. Withdrawal triggers:
1. Immediate cessation of sampling requests.
2. Pro-rated compensation through the session most recently completed.
3. Within 30 calendar days, deletion of all sufficient-statistics records for that participant from the study-site database.
4. Marking of the participant's chain-record as withdrawn (Everest 27); aggregate analyses already published prior to withdrawal cannot be retracted, but no further analyses will include the withdrawn participant.

## 9. Consent Process

- Consent is obtained at enrollment in a one-on-one session with study personnel.
- The consent form (`02_INFORMED_CONSENT_TEMPLATE.md`) is read aloud, with pauses for questions.
- The form is signed digitally; a paper copy is offered.
- Participants are explicitly informed of: the right to withdraw; the right to delete data; the opt-in/opt-out nature of adversarial-sample use; the publication plan; the compensation structure.
- A copy of the signed consent is provided to the participant and retained by the PI's institutional records office per local IRB requirements.

## 10. Statistical Analysis

See `07_STATISTICAL_ANALYSIS_PLAN.md` for the full pre-registered SAP. Briefly: Wilson-score 95% confidence intervals on FAR and FRR at each of 10+ operating thresholds; EER computed as the threshold of FAR-FRR equality; d-prime computed from genuine-vs-impostor distance distributions; Cochran-Armitage bias check across principal subgroups; temporal-drift regression of distance on session-week. Primary analyses are pre-registered to OSF.io before week 17 (enrollment ceremony).

## 11. Publication Commitment

Aggregate results will be submitted to a peer-reviewed venue (target: *IEEE Transactions on Biometrics, Behavior, and Identity Science* or *ACM Transactions on Privacy and Security*) regardless of whether the ship-gate thresholds are met. A null or negative result will be published with the same rigor as a positive result. A public preprint will be posted to arXiv simultaneously with peer-review submission.

---

— Calm, 2026-05-20
