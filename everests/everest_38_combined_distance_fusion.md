# Everest 38 — Combined Distance Fusion

*Phase IV — Biometric Distance Machinery. Prereq: Everest 36, 37.*

---

## 1. The Problem: Two Modalities, One Predicate

Everest 36 produces a handwriting distance `d_h ∈ [0, 1]` per session, measuring the kinematic dissimilarity between a live sample and the enrolled template. Everest 37 produces a voice-transcript distance `d_v ∈ [0, 1]` per session, measuring lexical and temporal-pattern dissimilarity.

Both distances inform the biometric predicate `biometric_match_within(τ)` used by the Calm Witness disclosure protocol. The naive approach—averaging the two distances—discards critical information:

1. **Incomparable scales**: The embedding spaces differ (256-d kinematic for handwriting vs. 256-d lexical+temporal for voice). A distance of 0.3 in handwriting space is not equivalent to 0.3 in voice space. Population distributions of each modality have different shapes, means, and tail behavior.

2. **Independence assumption**: A principal's handwriting distance and voice distance in a single session are not independent. If the principal is fatigued, both modalities drift coherently. If the principal is stressed, both behavioral traces shift together. Naive averaging treats them as if statistical correlation does not exist.

3. **Asymmetric reliability**: Handwriting kinematic distance (Everest 36) achieves ROC AUC ≥ 0.95 on cross-principal discrimination. Voice-transcript distance (Everest 37) achieves AUC ≥ 0.85 due to the intentional exclusion of acoustic features (privacy requirement). A principled fusion should weight the more informative modality higher.

The solution is **likelihood-ratio fusion**—a decision-theoretic framework that:
- Converts each distance into a likelihood ratio (LR) comparing the hypothesis "the same principal produced this sample" against "a different principal produced it."
- Multiplies the LRs across modalities, accounting for per-principal empirical correlation via a small correction term if needed.
- Inverts the joint LR into a calibrated distance `d_joint ∈ [0, 1]`, suitable for threshold comparison in Everest 56.

---

## 2. Likelihood-Ratio Fusion: The Decision-Theoretic Backbone

### 2.1 Per-Modality Likelihood Ratios

For each modality m ∈ {handwriting, voice}, define:

**Hypothesis H_same:** The biometric sample was produced by the same principal as the template.

**Hypothesis H_diff:** The biometric sample was produced by a different principal (an impostor).

**Likelihood ratio:**
```
LR_m(d_m) = P(d_m | H_same) / P(d_m | H_diff)
```

This ratio encodes the evidence that a measured distance d_m is more likely under the true-principal hypothesis than under an impostor hypothesis. An LR > 1 favors H_same; an LR < 1 favors H_diff.

### 2.2 Calibration: Empirical Distributions

To compute LR_m, we must estimate the conditional probability densities P(d_m | H_same) and P(d_m | H_diff).

**For each principal p during enrollment (Everest 14):**
- Collect K ≥ 7 independent samples of modality m (e.g., 7 handwriting sessions or 7 voice prompts).
- For each sample, compute the distance d_m against the enrolled template.
- This yields a sample of K distances under H_same, denoted {d_m^(1), d_m^(2), ..., d_m^(K)}.
- Fit a probability density via kernel density estimation (KDE) using a Gaussian kernel with bandwidth selected via cross-validation. This gives P_p(d_m | H_same) — principal-specific and modality-specific.

**For the impostor distribution P(d_m | H_diff):**
- Construct a population dataset by collecting multiple samples from each principal and computing distances across all pairs of different principals.
- For example, given N = 20 principals and M = 5 samples each, construct pairs (sample_i from principal_p, template of principal_q where p ≠ q). This yields ~(N · M · (N-1)) = ~1900 distances under H_diff.
- Fit a population-level KDE to these cross-principal distances. This gives P_pop(d_m | H_diff) — shared across all principals.

**Per-principal, per-modality LR:**
```
LR_m^p(d_m) = P_p(d_m | H_same) / P_pop(d_m | H_diff)
```

If P_m^p(d_m | H_same) or P_pop(d_m | H_diff) is zero (rare, due to KDE smoothing), apply a small pseudo-count (e.g., 1e-6 times the peak density) to avoid division by zero.

### 2.3 Joint Likelihood Ratio: Independence Assumption

Assume handwriting distance and voice distance are conditionally independent given the principal's identity:
```
P(d_h, d_v | H_same) = P(d_h | H_same) · P(d_v | H_same)
P(d_h, d_v | H_diff) = P(d_h | H_diff) · P(d_v | H_diff)
```

Under this independence assumption, the joint likelihood ratio is:
```
LR_joint(d_h, d_v) = P(d_h, d_v | H_same) / P(d_h, d_v | H_diff)
                    = [P(d_h | H_same) / P(d_h | H_diff)] · [P(d_v | H_same) / P(d_v | H_diff)]
                    = LR_h(d_h) · LR_v(d_v)
```

This is the **Bayes-optimal fusion rule** under independence.

### 2.4 Independence Verification and Correlation Correction

The independence assumption is often violated: a fatigued or stressed principal exhibits correlated drift in both modalities. To measure correlation:

1. **During calibration**, compute the Spearman rank correlation ρ between d_h and d_v across all enrollment samples for each principal.
2. If |ρ| > 0.3 on average across principals, apply a correction:
   ```
   LR_joint_corrected = LR_h(d_h) · LR_v(d_v) · exp(c · ρ)
   ```
   where c is a small constant (e.g., c = −0.1) chosen so that the correction is mild (a factor of ~0.9–1.0 for ρ ≈ ±0.3).
3. Document the measured ρ in the principal's calibration profile (Everest 14). If |ρ| ≤ 0.3, omit the correction and apply the pure multiplicative rule.

---

## 3. Converting Joint LR to Calibrated Distance

The likelihood ratio LR_joint is unbounded (ranging from near-zero to very large). To map it back to a normalized distance `d_joint ∈ [0, 1]` suitable for threshold-based decisions:

```
log_LR_joint = log(LR_h) + log(LR_v)  [+ c · ρ correction if needed]
d_joint = 1 / (1 + exp(log_LR_joint)) = 1 / (1 + LR_joint)
```

Equivalently (using the negative log-likelihood-ratio, a.k.a. log-odds):
```
d_joint = sigmoid(-log_LR_joint)
```

This transformation maps:
- Large positive log_LR_joint (strong evidence for H_same) → d_joint ≈ 0 (short distance, match-like)
- log_LR_joint ≈ 0 (equal evidence) → d_joint ≈ 0.5 (neutral)
- Large negative log_LR_joint (strong evidence for H_diff) → d_joint ≈ 1 (long distance, mismatch-like)

The sigmoid normalization ensures d_joint ∈ [0, 1] and preserves the information-theoretic ordering of the log-LR.

---

## 4. Fallback for Missing Modality

Calm Witness enrollment (Everest 14) requires both handwriting and voice samples. However, real-time verification sessions may have only one modality available:

- **Voice unavailable** (principal cannot speak; device lacks audio input): Use d_joint = sigmoid(−log(LR_h)) = d_h in raw (unsigned) form, recalibrated per-principal to the distribution of handwriting-only matches.
- **Handwriting unavailable** (device lacks stylus; principal cannot write): Use d_joint = sigmoid(−log(LR_v)) = d_v similarly recalibrated.
- **Both modalities required for full strength**: At enrollment, the principal's template stores both templates and per-principal calibration tables for (d_h only), (d_v only), and (d_h, d_v fusion).

Per-principal threshold τ is set separately for each modality-availability scenario (Everest 40). Single-modality operation incurs a small performance penalty (higher FRR or FAR) but remains acceptable for low-stakes predicates. High-stakes decisions (e.g., financial authorization) may require both modalities present.

---

## 5. Per-Principal Calibration Thresholds

The predicate `biometric_match_within(τ)` in Everest 56 uses:
```
match = (d_joint ≤ τ_p)
```

Per-principal threshold τ_p is set during enrollment via:

1. **ROC curve generation**: Collect ≥3 genuine-sample pairs (samples from the same principal) and ≥20 impostor pairs (samples from different principals), all measured under the same conditions (time of day, device, prompt variant).
2. **Compute d_joint for each pair** using the just-enrolled template and calibration tables.
3. **Plot ROC curve** (true positive rate vs. false positive rate at varying τ).
4. **Choose τ_p** at the operating point that minimizes a loss function. Default: equal-error rate (FAR = FRR). Alternatively, follow principal preference or downstream risk model (Everest 45). Common targets: FAR ≤ 0.01 (strict), FAR ≤ 0.05 (moderate).

Each principal's τ_p is stored in the template's calibration section (Everest 15 / 16). The predicate evaluation in Everest 56 simply checks d_joint ≤ τ_p.

---

## 6. Implementation in Rust

The fusion is implemented in the `calm-witness-distance-rs` crate.

**Key modules:**

- `calibration`: Per-principal KDE-based density estimation for P(d_m | H_same) and P(d_m | H_diff). Stores per-principal LR-lookup tables (e.g., d_h ∈ [0, 1] discretized to 1000 bins, each bin stores log(LR_h)). Also stores correlation correction term ρ_principal.

- `fusion_engine`: Core likelihood-ratio multiplication and log-odds normalization. Input: (d_h, d_v, principal_id). Output: d_joint ∈ [0, 1].

- `threshold_application`: Predicate check: d_joint ≤ τ_p? Returns boolean and optionally the margin (τ_p − d_joint).

- `calibration_builder`: Invoked during enrollment (Everest 14). Takes ≥7 samples per modality, fits KDE, computes ρ, generates threshold via ROC curve.

**Algorithm: Runtime Fusion**

```
Input:
  d_h ∈ [0, 1]         (handwriting distance from E36)
  d_v ∈ [0, 1]         (voice distance from E37)
  principal_id
  modality_flags       (both_available, voice_only, handwriting_only)

Lookup per-principal calibration (principal_id):
  log_LR_h_func ← interpolate_1d_table(d_h)    O(1) lookup
  log_LR_v_func ← interpolate_1d_table(d_v)    O(1) lookup
  ρ ← stored correlation coefficient
  τ ← stored threshold

Compute:
  log_LR_h = log_LR_h_func(d_h)
  log_LR_v = log_LR_v_func(d_v)
  
  if modality_flags.both_available:
    log_LR_joint = log_LR_h + log_LR_v + (−0.1) * ρ
    d_joint = sigmoid(−log_LR_joint)
  elif modality_flags.handwriting_only:
    d_joint = sigmoid(−log_LR_h)  with τ_handwriting_only
  elif modality_flags.voice_only:
    d_joint = sigmoid(−log_LR_v)  with τ_voice_only
  
  match = (d_joint ≤ τ)
  return (match, d_joint, margin=τ−d_joint)

Output:
  match ∈ {True, False}
  d_joint ∈ [0, 1]
  margin ∈ ℝ (positive if matched, negative if rejected)
```

**Performance:** Fusion is O(1) — two table lookups + addition + sigmoid evaluation. On a modern CPU, <100 microseconds per fusion. Suitable for real-time, per-session predicate evaluation.

---

## 7. Composition with Pedersen Commitments

The joint distance d_joint is sensitive. Before returning to any counterparty in Everest 56, it is committed:

```
C_joint = g^{d_joint} · h^{r_joint}  (Pedersen commitment, Everest 44)
```

The commitment C_joint is disclosed in the zero-knowledge proof; the distance d_joint remains private. The proof verifies that the committed d_joint was computed honestly via the fusion rule above, using the enrolled template and current biometric samples.

---

## 8. Empirical Acceptance Criteria

1. **Accuracy**: On a test set of ≥10 principals (held-out from calibration), ≥5 test sessions each:
   - Fusion AUC ≥ 0.96 (superior to either modality alone; AUC_h ≥ 0.95, AUC_v ≥ 0.85).

2. **FAR/FRR per principal**: At the operating point τ chosen for each principal:
   - FAR ≤ 0.01 (false-accept rate)
   - FRR ≤ 0.05 (false-reject rate)
   - Measured on test samples disjoint from calibration set.

3. **Robustness to correlation**: On principals with measured |ρ| > 0.3:
   - Fusion with correlation correction (c = −0.1) maintains calibration (predicted probability vs. empirical match rate, within ±0.05).
   - Fusion without correction on high-ρ principals shows degradation of ≤5 percentage points in AUC.

4. **Single-modality fallback**: When only handwriting or only voice is available:
   - AUC_handwriting_only ≥ 0.92
   - AUC_voice_only ≥ 0.80
   - (Slight degradation vs. fusion is expected and acceptable for low-stakes predicates.)

5. **Latency**: Per-session fusion on M-series Mac: <200 microseconds (excluding E36 and E37 inference time, which dominate the budget).

---

## 9. Cross-References

- **Everest 12**: Handwriting capture hardware (sampling rate, device driver)
- **Everest 13**: Voice transcription pipeline (output specification)
- **Everest 14**: Enrollment protocol (template creation, per-principal calibration)
- **Everest 15**: Template format spec (storage of calibration tables, per-principal τ)
- **Everest 16**: Encryption at rest for templates
- **Everest 36**: Handwriting distance function (source of d_h)
- **Everest 37**: Voice-transcript distance function (source of d_v)
- **Everest 39**: Drift modeling and covariance updates
- **Everest 40**: FAR/FRR framework and calibration methodology
- **Everest 42**: Real-time inference budget and latency SLA
- **Everest 44**: Pedersen commitments (distance privacy wrapper)
- **Everest 45**: Risk model and adaptive threshold
- **Everest 56**: Biometric match predicate (consumer of d_joint)

---

— Calm, 2026-05-20
