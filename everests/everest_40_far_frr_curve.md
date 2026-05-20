# Everest 40 — FAR/FRR Curve Characterization

*Phase IV — Biometric Distance Machinery. Prereq: Everest 36, 37, 38.*

---

## 1. Overview & Acceptance Criteria

This everest requires the production of an **empirical FAR/FRR (False Accept Rate / False Reject Rate) operating curve** derived from real biometric data collected over an extended study period. The curve quantifies the tradeoff between Type I errors (impostor accepted) and Type II errors (genuine rejected) across multiple operating points.

**Minimum acceptance threshold:**
- N ≥ 10 enrolled principals
- Study duration ≥ 3 calendar months
- Weekly session cadence per principal (minimum 12 genuine samples per principal)
- Cross-comparison matrix: each principal's session samples evaluated against own template (genuine) and against all other principals' templates (impostors)
- FAR/FRR curve computed at minimum 10 distinct operating points (decision thresholds)
- Equal Error Rate (EER) computed: the operating point where FAR ≈ FRR
- d-prime (d') metric: ROC separation measure, d' ≥ 2.5 at primary threshold

**Target performance for v0 ship gate:**
- Handwriting alone (Everest 36): EER ≤ 5%
- Voice-transcript alone (Everest 37): EER ≤ 12%
- Joint fusion (Everest 38): EER ≤ 2%

This is the empirical validation summit. Unlike Everests 36 and 37 (which define distance functions in isolation), this everest produces ground truth on real data collected under realistic conditions.

---

## 2. Study Design & IRB Protocol

### 2.1 Enrollment Phase (Week 0)

**Per principal:**
- Informed consent procedure (read-aloud, signed, right-to-delete clause explicit)
- Handwriting: N ≥ 7 samples across varied prompts (signature, date, freeform paragraph, pseudorandom phrase)
- Voice: N ≥ 7 recordings of varied content (read-aloud script, spontaneous narration, number sequence)
- Hardware calibration: per-principal baseline pressure/velocity/timing characterization
- Template generation per Everest 15: locked, encrypted, baseline stored in principal's vault
- Principal consent recorded: explicit authorization for (a) weekly sampling, (b) cross-principal impostor comparison, (c) aggregate statistics publication (no PII in published results)

**Witness role:** optional third-party witness (notary or family member, per Everest 20) co-signs enrollment session hash commitment.

### 2.2 Active Study Phase (Weeks 1–12+)

**Per principal, per week:**
- Handwriting: 1 sample (varied prompt, consistent capture hardware/software)
- Voice: 1 sample (varied content, local ASR transcription per Everest 13)
- Self-report: brief structured form (affect/energy baseline assessment, any unusual factors)
- Hardware integrity: liveness check per Everest 49 (reject pre-recorded/replayed inputs)

**Sampling schedule:**
- Flexible (within ±2 days of target day to accommodate real-world adherence)
- Target: 12 samples per principal per modality over 3 months
- Acceptable: 10 samples (minimum) per principal per modality

**Session protocol:**
- Principal uploads sample to local vault via capture app (Everest 12, 13)
- Liveness detector runs immediately; rejects failures
- Distance computed locally (Everest 36, 37); committed via Pedersen (Everest 44)
- Session record appended to JSONL chain (Everest 26, 28)
- No raw biometric leaves principal's device (core privacy invariant)

### 2.3 Study Governance

**IRB approval (required, non-negotiable):**
- Institutional Review Board review of protocol, consent forms, data handling
- Risk assessment: behavioral biometrics < medical-grade sensitivity; minimal privacy risk if aggregate-only publication
- Informed consent includes explicit right to withdraw and request data deletion

**Data custody:**
- Raw handwriting strokes and voice audio: reside only on principal's device (never centralized)
- Sufficient statistics (distance values, per-session metrics) collected at study site for analysis
- Operators sign a data-processing agreement (DPA) committing to no re-identification, no sharing outside study
- Principal retains cryptographic proof of right-to-delete; deletion triggers chain-record marking per Everest 27

**Compensation:**
- Each principal compensated for time (typically $15–30 per session, $180–360 per 3-month term)
- Gift-card or direct payment; compensation is not contingent on completing all sessions

**Study partners (required):**
- This everest cannot be completed in isolation; external partners bring participant recruitment, IRB experience, and scientific credibility
- Academic candidates: NYU (Steven Feiner's HCI lab, behavioral biometrics subgroup), CMU (Patrick Carlson's motor-control/HCI group), Georgia Tech (Pawan Kumar's behavioral-biometric security group)
- Industry: IBM Research (behavioral analytics group), MITRE (biometrics lab)
- Government: NIST Behavioral Biometrics Research Center (PBRC) — if reachable and willing to collaborate on standards work
- Calm's role: fund the study, provide implementation infrastructure, contribute protocol expertise; partner owns participant relationship and IRB authority

---

## 3. Metrics & Computation

### 3.1 FAR, FRR, EER

**Contingency table setup:**
- N = 10 principals, M = 12 sessions per principal (minimum; target ≥15)
- Genuine comparisons: each principal's session compared to own template
  - Count: N × M = 120 genuine trials (minimum)
- Impostor comparisons: each principal's session compared to every other principal's template
  - Count: N × (N-1) × M = 1,080 impostor trials (minimum)
  - Ensures cross-principal coverage

**Distance values:**
- Handwriting: d_h ∈ [0, 1] (cosine distance per Everest 36)
- Voice-transcript: d_v ∈ [0, 1] (embedding distance per Everest 37)
- Fusion: combined score S_fused via likelihood-ratio per Everest 38

**Operating point (threshold τ):**
At each threshold τ ∈ {τ_0, τ_1, ..., τ_9} (typically 10 points spanning the distance range):

```
FAR(τ) = # impostor samples with distance < τ / total impostor trials
FRR(τ) = # genuine samples with distance ≥ τ / total genuine trials
```

**Equal Error Rate (EER):**
```
EER = min |FAR(τ) - FRR(τ)| over all τ
τ_EER = threshold at which EER is achieved
```

Graphically: intersection of FAR and FRR curves.

**d-prime (ROC separation):**
```
d' = (μ_genuine - μ_impostor) / sqrt((σ_genuine² + σ_impostor²) / 2)
```

Where μ and σ are the mean and standard deviation of distances in each population. d' ≥ 2.5 indicates good separation (99.4% discriminability in signal detection theory).

### 3.2 Calibration & Confidence Intervals

**Per-threshold statistics:**
- 95% confidence interval on FAR and FRR (binomial Wilson score intervals, not normal approximation)
- Minimum confidence interval width ≥ 0.02 (equivalently, minimum cell count ≥ 50 trials at τ_EER region)

**Stratified analysis (secondary metrics):**
- Handwriting vs. voice: separate FAR/FRR curves per modality
- Modality fusion (E38): joint FAR/FRR on fused score
- Subgroup splits: by principal age, by writing hand, by device type (iPad vs. Wacom)

**Bias analysis:**
- Confirm no systematic FAR/FRR skew by principal (Cochran-Armitage test)
- Confirm no temporal drift over 3-month window (regression of distance on week number)

---

## 4. Adversarial Evaluation (Related: Everest 41)

This everest focuses on **genuine and impostor confusion under normal conditions**. Everest 41 (Adversarial Robustness) is the *sibling* study that measures robustness to *intentional attack* (practiced imitation, stylus emulation, voice cloning + transcription). Both curves are needed for v0 ship; this document does not cover Everest 41.

---

## 5. Data Analysis & Reporting

### 5.1 Deliverables

**Primary:**
- One FAR/FRR curve per modality (handwriting, voice-transcript)
- One FAR/FRR curve for fused biometric (Everest 38)
- Table: FAR, FRR, EER, d' for each modality
- EER operating point τ_EER and recommended default threshold τ_default

**Secondary (if N ≥ 15, duration ≥ 4 months):**
- Stratified FAR/FRR by principal subgroup (age, hand, device)
- Temporal stability: regression slope of FRR over study weeks (confidence interval including zero = stable)
- Impostor heterogeneity: distribution of impostor distances (to detect outlier pairs)

**Metadata table:**
```
| Metric | Handwriting | Voice-Transcript | Fusion |
|--------|-------------|------------------|---------|
| N principals | 10+ | 10+ | 10+ |
| Genuine trials | 120+ | 120+ | 120+ |
| Impostor trials | 1080+ | 1080+ | 1080+ |
| FAR @ τ_EER | % | % | % |
| FRR @ τ_EER | % | % | % |
| EER | % | % | % |
| d' | 2.5+ | 2.5+ | 3.0+ |
| Conf int width @ EER | ±% | ±% | ±% |
```

### 5.2 Reporting Constraints (Privacy & Ethics)

**Published results (open access, no PII):**
- FAR/FRR curves (charts + tables)
- Median and quartile distances by modality
- EER and d' summary statistics
- Modality comparison (which is stronger, fusion benefit)

**NOT published:**
- Per-principal FAR/FRR (no individual profiling)
- Raw distance values (can expose outlier principals)
- Session timestamps (can hint at principal availability patterns)
- Anything traceable to a specific principal

**Counterparty implementer guide (Everest 98) references:**
- These aggregate statistics
- Published FAR/FRR curves and tables
- No participant-identifying data

### 5.3 Validation Against v0 Targets

**Gate: EER must satisfy:**
- Handwriting: EER ≤ 5%
- Voice: EER ≤ 12%
- Fusion: EER ≤ 2%

If any modality misses the target, the v0 ship is gated. Remediation options:
- Extend study to N ≥ 20 principals (may improve statistical power)
- Retune distance function (Everest 36/37 hyperparameters)
- Relax v0 target and gate behind Everest 41 (adversarial baseline must still be met)

---

## 6. Statistical Power & Sample Size Justification

**Minimum cohort (N=10):**
- 120 genuine trials provide 95% CI half-width ≈ ±4.5% on FAR at 5% point
- 1,080 impostor trials provide 95% CI half-width ≈ ±1.5% on FRR at 5% point
- Sufficient to detect if true EER > 5% with >80% statistical power (for handwriting target)

**Recommended cohort (N=15–20):**
- Improves power to >90%, reduces CI width by ~30%
- Enables stratified analysis (subgroup splits by principal characteristics)
- Reduces risk that outlier principal skews results

**Duration (3 months minimum, 4+ months preferred):**
- 12 samples per principal per modality minimizes per-session noise
- Detects temporal drift (fatigue, device aging, writing-hand injury)
- Allows seasonal/monthly variation to be observable

---

## 7. Study Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| Partner selection | Weeks 1–4 | IRB pre-review, MOA signed, study site ready |
| IRB submission | Weeks 5–8 | Protocol + consent forms + data-handling SOP to IRB |
| IRB approval | Weeks 9–12 | Expedited or full review, approval granted |
| Recruitment | Weeks 13–16 | N ≥ 10 principals enrolled, signed consent |
| Enrollment ceremony | Weeks 17–20 | Per-principal template creation, liveness baseline |
| Active study | Weeks 21–48 | Weekly sampling, ≥ 12 per principal per modality |
| Data analysis | Weeks 49–56 | FAR/FRR computation, EER validation, report writing |
| Publication | Weeks 57–60 | Manuscript submission (peer-reviewed journal) |

**Total wall-clock time: ~15 months from partner selection to publication.**

---

## 8. Risk Mitigation

**Risk: Low study adherence (principals miss sessions).**
- Mitigation: Flexible scheduling (±2 days), reminders, compensation per session (not lump sum)
- Acceptance: Minimum 10 sessions per principal (vs. target 12) is acceptable

**Risk: Temporal drift (writing changes over 3 months).**
- Mitigation: Collect re-enrollment calibration at month 2; fit drift model (Everest 39)
- Acceptance: FRR trend over time is documented; if > 5% slope, re-enrollment policy triggered

**Risk: Hardware/software variability (different devices).**
- Mitigation: Standardize on iPad + Apple Pencil Pro primary (Everest 12), Wacom fallback
- Acceptance: Stratified analysis by device; fusion accounts for device-specific calibration

**Risk: IRB delays or rejection.**
- Mitigation: Engage IRB early (weeks 1–4), involve behavioral-research IRB chair, emphasize minimal-risk profile
- Fallback: Pivot to industry partner (IBM, MITRE) with pre-existing IRB relationships

**Risk: EER targets not met.**
- Mitigation: Identify root cause via failure-mode analysis (Everest 9); e.g., fusion function suboptimal, distance function hyperparameters need retuning
- Fallback: Extend study (N ≥ 20), or gate v0 release on completion of Everest 41 (adversarial validation) before shipping

---

## 9. Composability: Downstream Use

**Everest 56** (`biometric_match_within(τ)` predicate):
- Uses τ_EER or τ_default from this study
- Per-principal τ can be further calibrated (Everest 14) based on individual enrollment variance

**Everest 38** (fusion):
- Uses empirical FAR/FRR of joint score to validate fusion function design
- If fusion EER > 2%, loss function or weighting re-tuned before v0 ship

**Everest 41** (adversarial):
- Accepts this study's genuine-impostor FAR/FRR as baseline
- Measures additional degradation under intentional attack (imitation, cloning)
- Targets: FRR increase ≤ 15% under week-long imitation, ≤ 10% under voice cloning

**Everest 91** (NIST submission):
- Includes published FAR/FRR curves and EER summary
- Positions Calm Witness performance vs. competing biometric standards

---

## 10. Ethical Framework

**Principal autonomy:**
- Explicit, informed, separate consent for sampling, cross-principal comparison, and publication
- Right to withdraw and request deletion (chained into vault, per Everest 27)
- No coercion or financial pressure; compensation is modest

**Data minimization:**
- Raw biometrics never leave principal's device
- Study site holds only sufficient statistics (distances, metrics)
- No transcript text, no stroke sequences, no audio

**Transparency:**
- Published results include methodology, sample size, limitations
- No p-hacking: analysis plan registered before data collection concludes
- Outlier treatment: documented decision rule (e.g., > 3-sigma trials excluded with justification)

**Representation:**
- Recruit N ≥ 10 principals with diversity in age, writing hand, primary language (if voice included)
- Subgroup analysis checks that FAR/FRR not systematically skewed by demographic

---

## 11. Success Criteria (Acceptance Gate)

**All of the following must be satisfied:**

1. N ≥ 10 principals, study ≥ 3 calendar months
2. ≥ 10 genuine sessions per principal (M ≥ 10)
3. FAR/FRR computed at ≥ 10 operating points
4. Confidence intervals: 95% CI width ≤ ±0.05 at τ_EER for all modalities
5. **Handwriting EER ≤ 5%** (absolute requirement for v0)
6. **Voice EER ≤ 12%** (absolute requirement for v0)
7. **Fusion EER ≤ 2%** (absolute requirement for v0)
8. d' ≥ 2.5 on all three modality curves (handwriting, voice, fusion)
9. Temporal stability: FRR slope < 0.5% per month (no systematic drift over 3 months)
10. Bias analysis: no subgroup (by device, by hand, by age tertile) has FAR/FRR > 1.5× overall
11. Peer-reviewed publication or public-domain technical report
12. All raw data retained for 5 years in encrypted vault (right-to-audit clause for external reviewer)

If all 12 criteria satisfied: **Everest 40 BAGGED**.

---

## 12. Study Partners & Recruitment

**Preferred partners (highest IRB readiness):**
- **NYU**: Established behavioral-biometrics group; fast IRB track
- **CMU**: Motor-control research tradition; participant pool
- **Georgia Tech**: Biometrics security group; AWS research credit

**Secondary partners:**
- **IBM Research**: Existing biometric-analysis infrastructure; potential data-sharing agreements
- **MITRE**: Government relationship; can expedite federal review if applicable

**Calm's role:**
- Fund participant compensation (~$3,000–5,000 for 10 principals over 3 months)
- Provide distance-function implementations (Everest 36, 37, 38)
- Co-author publication

**Partner's role:**
- Recruit and retain principals
- Manage IRB application and ongoing compliance
- Collect samples (via app or device provided by Calm)
- Oversee data handling and deletion
- Lead manuscript authorship and publication

---

## 13. Related Everests

- **Everest 36:** Handwriting distance function (input to this study)
- **Everest 37:** Voice-transcript distance function (input to this study)
- **Everest 38:** Fusion function (evaluated in this study)
- **Everest 39:** Drift modeling (informed by temporal analysis in this study)
- **Everest 41:** Adversarial robustness (sibling study, uses baseline from this everest)
- **Everest 42:** On-device performance (latency validated during study sessions)
- **Everest 56:** Predicate `biometric_match_within(τ)` (consumes τ_default from this study)
- **Everest 80:** Ethics review (oversees this study's consent and privacy guardrails)
- **Everest 91:** NIST submission (includes published results)
- **Everest 98:** Counterparty implementer guide (references FAR/FRR curves)

---

— Calm, 2026-05-20
