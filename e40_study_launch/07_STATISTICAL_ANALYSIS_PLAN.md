# Statistical Analysis Plan (Pre-Registration)

*Everest 40 — Empirical FAR/FRR Characterization of the Calm Witness Biometric Distance Stack*

**Pre-registration target:** OSF.io, lodged before week 17 of the study timeline (enrollment ceremony begin), and irrevocable thereafter except by explicit amendment with OSF version history.

**Version:** 1.0 — 2026-05-20.

---

## 1. Study Design and Pre-Registration Scope

This document specifies, in advance of any data collection, the analyses that will be performed on the Everest 40 study data, the metrics that will be reported, the inferential procedures, and the publication commitment. Deviations from this plan are permitted only via dated, public amendment with prior justification.

The primary scientific question: *Do the locked Calm Witness biometric primitives (Plamondon Sigma-Lognormal for handwriting; Burrows Cosine Delta + Koppel-Seidman Impostors over CrisperWhisper for voice; likelihood-ratio fusion for joint) meet pre-specified Equal-Error-Rate ship-gate thresholds under naturalistic multi-month collection conditions?*

## 2. Hypotheses

### 2.1 Primary Hypotheses (all pre-registered, all to be reported)

- **H1 (handwriting).** The empirical Equal Error Rate for the handwriting-only modality is ≤ 5%.
- **H2 (voice).** The empirical Equal Error Rate for the voice-transcript-only modality is ≤ 12%.
- **H3 (fusion).** The empirical Equal Error Rate for the joint (likelihood-ratio-fused) modality is ≤ 2%.
- **H4 (separation).** d-prime ≥ 2.5 on each of the three modality curves at the primary threshold.

Each hypothesis is tested by computing the lower bound of the 95% Wilson-score confidence interval on EER and checking whether the upper bound of that interval is ≤ the pre-specified threshold. Failure on any of H1-H4 gates the v0 ship; null results will be published.

### 2.2 Secondary Hypotheses (pre-registered, to be reported)

- **H5 (temporal stability).** The regression slope of within-principal genuine-distance on week-of-study is statistically indistinguishable from zero at α=0.05, OR less than 0.5% per month in magnitude. Failure prompts a re-enrollment-policy recommendation in the publication.
- **H6 (no demographic bias).** Stratified FAR/FRR by age tertile, writing-hand-dominance, and device type does not exhibit > 1.5× variation in EER between any pair of subgroups (Cochran-Armitage test for trend, two-sided α=0.05).
- **H7 (modality complementarity).** Joint-fusion EER is strictly lower than the minimum single-modality EER, by a margin exceeding the 95% confidence-interval width of the fused-modality EER.

## 3. Sample Size Justification

Per the Everest 40 design doc Section 6: with **N = 10 principals × M = 12 weekly sessions**, the study collects:

- **120 genuine trials** per modality.
- **N × (N-1) × M = 1,080 impostor trials** per modality.

At a true EER of 5%, the 95% Wilson-score confidence half-width is approximately:
- ±4.5% on FAR at the 5% point (driven by genuine-trial count).
- ±1.5% on FRR at the 5% point (driven by impostor-trial count).

This yields **>80% statistical power** to detect a true EER > 5% if the system is at the boundary. Power is computed via Monte Carlo simulation under the prior assumption that genuine and impostor distance distributions are approximately Gaussian with equal variance (the simulation will be checked against actual data; deviations will be reported).

The **target cohort of N = 15** improves power to **>90%** and reduces CI width by approximately 30%, and is the operational target. The minimum N = 10 is the acceptance gate; below N = 10 the study is considered incomplete.

A small-cohort sensitivity analysis (N as a function from 10 to 15) will be reported in the manuscript appendix.

## 4. Primary Outcome Measures

For each modality m ∈ {handwriting, voice, fusion}:

### 4.1 FAR and FRR Curves
- Compute distance value d for every genuine and every impostor trial.
- For each threshold τ in a pre-specified grid of 10 operating points (τ_0 through τ_9, spanning the empirical range of distances at the 5th and 95th percentile of the impostor distribution):
  - FAR(τ) = (# impostor trials with d < τ) / (total impostor trials).
  - FRR(τ) = (# genuine trials with d ≥ τ) / (total genuine trials).
- 95% confidence intervals on FAR and FRR computed via **Wilson score interval** (not normal approximation; not Clopper-Pearson). Wilson is the pre-registered choice because it has the best coverage properties for binomial proportions near 0 and 1.

### 4.2 Equal Error Rate (EER)
- EER = the operating threshold at which |FAR(τ) - FRR(τ)| is minimized.
- Computed by linear interpolation between the two adjacent grid points where FAR-FRR crosses zero.
- 95% CI on EER is computed by bootstrap (2,000 resamples, stratified by principal), reporting the 2.5th and 97.5th percentiles.

### 4.3 d-prime (ROC Separation)
- d' = (μ_genuine - μ_impostor) / sqrt((σ_genuine² + σ_impostor²) / 2)
- Where μ and σ are computed across all genuine and impostor trials respectively.
- 95% CI on d' computed by bootstrap as above.

## 5. Secondary Outcome Measures

### 5.1 Stratified Analyses
- EER, d', and 95% CI for each subgroup:
  - **Age tertile**: ≤30, 31-50, 51+.
  - **Writing-hand dominance**: right-handed vs. left-handed.
  - **Device type**: iPad + Apple Pencil Pro vs. Wacom + Microsoft Surface Pen (if device heterogeneity present in cohort).
- Stratified analysis is reported descriptively. Subgroup-difference test: Cochran-Armitage test for trend (for age) and Fisher's exact test (for binary subgroups), two-sided, α = 0.05. Multiple-testing correction by Benjamini-Hochberg at FDR = 0.10 within the secondary-analysis family.

### 5.2 Temporal Drift
- Linear mixed-effects model: distance ~ week + (week | principal), fit to genuine trials only.
- The fixed-effect slope on `week` is the population-level temporal-drift coefficient. 95% CI on this slope via Wald approximation, with Satterthwaite degrees of freedom.
- Pre-registered acceptance: |slope| ≤ 0.5% per month (or, equivalently, CI containing zero) is reported as "stable." Greater drift triggers a re-enrollment-policy recommendation in the Discussion section.

### 5.3 Impostor Heterogeneity
- Distribution of impostor distances, broken down by principal-pair. Pre-registered visualization: violin plot of impostor-distance distributions, one violin per principal.
- Outlier-pair detection: principal pairs whose median impostor distance is more than 2 inter-quartile ranges below the cohort median are reported (without identification by principal name).

### 5.4 Adversarial-Sample Hooks (link to Everest 41)
- Genuine and impostor distance distributions are saved in their final form (per the data retention policy) so that the Everest 41 adversarial-robustness study can directly use them as the baseline against which adversarial degradation is measured. No additional statistical analysis is performed in this study on the adversarial samples; they are out of scope.

## 6. Handling of Missing Data and Protocol Deviations

- **Missed weekly sessions:** Sessions missed within the ±2-day flexibility window are not counted as missing. Sessions missed beyond that window are not back-filled. The analysis proceeds with whatever sessions each principal actually completed.
- **Minimum per-principal sessions:** Principals with < 10 completed weekly sessions across the study are reported but excluded from the primary FAR/FRR analysis. A sensitivity analysis (including-vs-excluding these participants) is reported in the appendix.
- **Liveness-rejected sessions:** A session that fails the liveness check (Everest 49) is logged but not counted as a completed session. If a principal accumulates more than 3 liveness-failed sessions, they are flagged for individual follow-up (the protocol expects an aggregate liveness-rejection rate of < 1%, and a principal substantially above that rate may indicate a hardware/software issue).
- **Withdrawals:** Withdrawing participants are reported in the cohort flow (CONSORT-style diagram). Data already collected prior to withdrawal is deleted per the IRB protocol and is *not* included in the analysis.

## 7. Bias Checks

- **No cherry-picking:** All ten operating thresholds are pre-specified before unblinding. The EER computation method is fixed.
- **No post-hoc subgroup discovery:** Subgroup splits are limited to those pre-registered in Section 5.1. Additional subgroup analyses, if reported, are clearly flagged as exploratory and not used for inferential claims.
- **Per-principal contribution check:** Mean genuine distance per principal is computed. If any single principal contributes > 2 standard deviations more than the cohort mean, the analysis is repeated with that principal excluded (sensitivity analysis), and the result reported.
- **No selective stopping:** The study runs for the pre-specified 12 weeks of active sampling regardless of interim analyses. Interim analyses are *not* performed for stopping; they are performed only for participant-retention monitoring (a separate operational concern).

## 8. Software and Reproducibility

- **Analysis code** will be written in Python (numpy, scipy, statsmodels, scikit-learn) and committed to a public GitHub repository at the time of OSF pre-registration. The code is fully executable on a single machine with the dataset.
- **Distance-function implementations** (Everest 36, 37, 38) are open-source under the Calm Witness project repository, with version pin specified in the SAP at pre-registration time.
- **Reproducibility package** at publication time includes: aggregate-statistics dataset, analysis code, expected outputs, and a reproducibility container (Docker image).
- **Statistical computing environment** is pinned via `requirements.txt` and a Docker image; the published manuscript references the exact image hash.

## 9. Publication Commitment

We commit to publishing the results of this study **regardless of whether the ship-gate thresholds are met**, and **regardless of whether secondary hypotheses are confirmed or refuted**.

- **Target venue:** *IEEE Transactions on Biometrics, Behavior, and Identity Science* (primary) or *ACM Transactions on Privacy and Security* (secondary).
- **Preprint:** arXiv preprint posted simultaneously with peer-review submission, no embargo.
- **Data:** Aggregate-statistics dataset posted to the OSF.io project alongside this SAP, under CC-BY-4.0.
- **Code:** Analysis code posted to GitHub under Apache-2.0.
- **Timeline:** Manuscript submission within 8 weeks of the last analytical run; in no case later than 6 months after the last weekly session.
- **Pre-print disclosure:** Any partial results (e.g., conference talk slides) released prior to peer-review submission will reference the OSF pre-registration and clearly label which analyses are pre-registered vs. exploratory.

## 10. Amendments

Amendments to this SAP must be:
1. Dated.
2. Justified (1-2 paragraphs explaining the reason).
3. Posted as a new version on the OSF project page (preserving previous versions).
4. Disclosed in any subsequent publication.

Amendments before unblinding are unrestricted (with justification). Amendments after unblinding are *not* permitted for primary analyses; for secondary or exploratory analyses they are permitted only with explicit "post-hoc" flagging.

---

— Calm, 2026-05-20
