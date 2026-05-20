# Everest 36 — Handwriting Distance Function Spec

*Phase IV — Biometric Distance Machinery. Prereq: Everest 12, 15.*

---

## 1. Overview & Design Philosophy

This everest specifies the formal distance function for comparing handwriting samples within the Calm Witness biometric subsystem. The core commitment is kinematic-first: handwriting identity is encoded in motor control signals (pressure, velocity, acceleration, jerk, tilt dynamics) rather than visual appearance. This reflects forensic document examination (FDE) practice since Osborn (1910) and validated by contemporary motor neuroscience.

The distance function serves the biometric_match_within(τ) predicate (Everest 56), enabling both:
- **Liveness verification**: comparing enrollment samples to real-time capture
- **Cross-prompt resilience**: comparing handwriting from different writing tasks (via optional DTW alignment)

Kinematic approaches defeat imitation attacks that fool visual-only systems; pressure and jerk profiles are subconscious motor signatures, difficult for a human imitator to replicate over weeks of practice.

---

## 2. Kinematic Signal: Why Not Visual

Visual handwriting—post-rendered ink images—discards the signal that makes forensic handwriting unique and difficult to forge:

1. **Pressure dynamics**: Force exerted at each pen point. Unique per writer; varies with emotional state and fatigue but stable within enrollment.
2. **Velocity and acceleration**: Speed and rate-of-speed-change. Tied to motor control loop frequency (~100–300 Hz). Difficult to replicate without motor practice.
3. **Jerk (da/dt)**: Rate of acceleration change. Subconscious micro-tremor is writer-specific and nearly impossible to imitate.
4. **Tilt and azimuth**: Pen orientation changes during writing. Biomechanically constrained by hand/wrist geometry.

An imitator copying visual appearance can succeed on static ink images. But if they haven't practiced for weeks, their pressure/jerk signatures will differ. Forensic examiners since Hagan (1950) rely on these kinematic markers; modern handwriting-recognition systems (e.g., Plamondon's Sigma-Lognormal model) are built on the same principle.

Pure-visual systems are rejected here.

---

## 3. Per-Stroke Feature Extraction

Each stroke is a pen-down sequence of raw biometric events. The capture hardware (Everest 12) logs:

```
Event = (timestamp_ms, x_px, y_px, pressure_norm, tiltX_deg, tiltY_deg, azimuth_deg)
```

Per stroke, derive:

**Primary features (computed via finite differences):**
- Velocity: v = √((Δx/Δt)² + (Δy/Δt)²)
- Velocity components: vx = Δx/Δt, vy = Δy/Δt
- Acceleration: a = dv/dt
- Jerk: j = da/dt
- Pressure derivative: dp/dt
- Tilt rate: d(tilt_angle)/dt
- Azimuth rate: d(azimuth)/dt

**Aggregate features:**
- Stroke duration: t_stroke = t_end − t_start (ms)
- Stroke length: ∫|v| dt (pixels)
- Mean velocity: length / duration
- Pressure range: max(p) − min(p)
- Peak jerk: max(|j|) over stroke
- Curvature: integrated absolute turning angle (radians)
- Initial/terminal speed: v(0), v(t_end)

All features are normalized per-stroke (z-score within that stroke's event sequence) to handle writer-dependent absolute scales (e.g., one writer presses harder than another).

---

## 4. Embedding Model

A learned embedding compresses the per-stroke kinematic profile into a fixed-dimensional representation, enabling fast distance computation and Mahalanobis weighting.

**Architecture:**
- Input: sequence of normalized event vectors, length L (variable, typically 20–300 per stroke)
- Processor: 1D-CNN (3 layers, 64→128→256 channels) followed by a lightweight Transformer encoder (2 heads, 1 layer)
- Output: single 256-dimensional embedding vector per stroke

**Parameter count:** ~250K parameters. Inference time: <2 ms per stroke on M-series Mac.

**Training procedure:**
- Corpus: enrollment samples from N ≥ 10 principals, multiple prompts per principal
- Objective: contrastive learning (Siamese networks following Bromley & LeCun)
  - Positive pair: two strokes from the same writer, same writing task
  - Negative pair: one stroke from writer A, one from writer B
  - Loss: triplet or NT-Xent (symmetric cross-entropy), margin ε = 0.2
- Validation: held-out test set, ROC AUC ≥ 0.95

The embedding is **never disclosed** to a counterparty; it remains internal to template processing.

---

## 5. Distance Function Design

### 5.1 Per-Stroke Distance

For two embedding vectors **e_a** and **e_b** (both 256-d):

```
d_stroke = 1 − cos(e_a, e_b) = 1 − (e_a · e_b) / (‖e_a‖ ‖e_b‖)
```

Cosine distance ranges [0, 2]; we map to [0, 1] via the formula above. Same-writer strokes: d ≈ 0.1–0.2. Different-writer strokes: d ≈ 0.7–0.9.

### 5.2 Per-Session Distance (Single Prompt)

Given two handwriting samples A and B from the same writing prompt (e.g., "Sign your name"), each containing M and N strokes respectively:

1. **Align strokes** (if M ≈ N, one-to-one; if very different, optional DTW pre-alignment)
2. **Compute per-stroke distances** between aligned pairs
3. **Aggregate:**
   ```
   distances = [d_1, d_2, ..., d_K]  (K = min(M, N))
   median_d = median(distances)
   p95_d = 95th percentile(distances)
   d_session = α · median_d + (1 − α) · p95_d
   ```
   Default: α = 0.7.

**Rationale:** The median captures typical stroke similarity; the 95th percentile captures outlier sensitivity. Weighting 0.7/0.3 avoids over-penalizing occasional jitter while staying sensitive to systematic differences.

### 5.3 Cross-Prompt Distance (Optional DTW)

When comparing samples from different writing tasks (e.g., enrollment on "Sign your name" vs. verification on "Write the date"), stroke counts and timing differ. Invoke Dynamic Time Warping (DTW):

```
DTW_cost(A, B) = min over all alignments of sum(d_stroke(a_i, b_j))
d_session_DTW = DTW_cost(A, B) / max(M, N)  (normalized by longer sequence)
```

DTW is more expensive (~O(M·N) in stroke count) but necessary for cross-prompt comparisons. For same-prompt verification, skip DTW and use the direct aggregation above.

---

## 6. Mahalanobis Weighting

The embedding's 256 dimensions are not equally informative. The Mahalanobis weight matrix Λ is learned from the enrollment corpus and refined during operation.

**Enrollment (Everest 14):**
- Collect K reference samples per principal
- Compute per-stroke embeddings for all strokes
- Estimate covariance matrix Σ and its inverse Λ = Σ⁻¹
- Store Λ (256×256) in the principal's encrypted profile (Everest 16)

**Distance with Mahalanobis weighting:**
```
d_mahal(e_a, e_b) = sqrt( (e_a − e_b)ᵀ · Λ · (e_a − e_b) )
```

This replaces the cosine distance for applications requiring per-principal calibration. It adapts the metric to each writer's natural variation pattern.

**Drift modeling (Everest 39):** As the principal's writing changes over months (aging, injury, device drift), the Mahalanobis matrix is incrementally updated via Bayesian covariance estimation.

---

## 7. Threshold Semantics

The predicate `biometric_match_within(τ)` uses:

```
match = (d_session ≤ τ)  or  (d_mahal ≤ τ_mahal)
```

**Default threshold:** τ = 0.3 (in cosine-distance units). This is calibrated on a corpus of ≥10 principals to yield FAR ≤ 0.01, FRR ≤ 0.05 (see Everest 40 for empirical validation).

**Per-principal calibration:** Each principal's profile (Everest 16) stores a calibrated τ_principal, optimized for that writer's enrollment corpus.

**Setting τ:** Initial τ is chosen to equalize FAR and FRR (typical operating point). Deployment may adjust based on risk model (Everest 45).

---

## 8. Inference Performance & Budget

**Latency targets (Everest 42):**
- Per-session inference on M-series Mac: <2 seconds (embedding + distance)
- Per-session inference on phone: <5 seconds
- Per-stroke embedding: <2 ms (CPU bound; negligible for real-time capture)

**Memory footprint:**
- Model file (ONNX): ~1.2 MB
- Per-session working memory: O(M + N) = O(300 + 300) = ~15 KB
- Per-principal state (Λ, τ): ~64 KB + constants

---

## 9. Adversarial Robustness

**Threat: Deliberate imitation by a motivated imitator (weeks of practice).**
- Kinematic approach defeats this. Subconscious jerk and pressure-noise patterns are motor-control artifacts that resist training.
- Visual similarity alone (which an imitator could achieve) is insufficient to match the embedding.

**Threat: Stylus emulation or replay attack.**
- Defeated by liveness detector (Everest 49) *before* this distance function is invoked. Liveness captures real-time pen dynamics (e.g., random challenges: "write this phrase").
- Replay of a recorded stroke sequence lacks the noise that distinguishes live capture.

**Threat: Same-glove, different-person spoofing.**
- Wearing the same glove does not replicate another person's kinematic signature (pressure, jerk, velocity profile). Highly resistant in practice.

---

## 10. Privacy & Commitment

The distance value itself is sensitive. Prior to disclosure:

**Pedersen commitment (Everest 44):**
- The operator computes d_session locally.
- Before returning to any counterparty, the distance is committed: C = g^d · h^r (Pedersen).
- The commitment C is disclosed; the distance d remains private.

**Embedding encapsulation:**
- The 256-d embedding is *never* disclosed or exported.
- All comparisons happen inside the template's protected memory.
- Template encryption at rest (Everest 16) shields embeddings from disk access.

**Composition with voice (Everests 37, 38):**
- Handwriting distance d_h and voice-transcript distance d_v are fused via likelihood-ratio:
  ```
  LR = P(d_h, d_v | same writer) / P(d_h, d_v | different writers)
  ```
- Neither distance is disclosed separately; only the fused LR (or a binary decision) leaves the operator.

---

## 11. Reference Implementation

**Language:** Rust  
**Crate:** `calm-witness-handwriting-rs`

**Key modules:**
- `kinematic_extractor`: per-stroke feature derivation
- `embedding_model`: 1D-CNN + Transformer, loads ONNX model
- `distance_engine`: cosine, Mahalanobis, DTW implementations
- `enrollment_calibrator`: Λ matrix and per-principal τ computation

**Model serialization:**
- Format: ONNX (cross-platform, widely auditable)
- Model hash: committed to Everest 15's template format spec
- Versioning: model version tagged in template manifest

**Testing:**
- Unit tests: per-feature extraction, embedding forward pass, distance computation
- Integration tests: enrollment → comparison → decision on reference corpus (N=10, M=5 prompts per principal)
- Adversarial tests: deliberate imitation attempts, stylus emulation detection

---

## 12. Acceptance Metrics

1. **Accuracy:** ROC AUC ≥ 0.95 on held-out test set (≥10 principals, ≥3 samples per principal per prompt)
2. **FAR/FRR:** At τ = 0.3:
   - FAR ≤ 0.01 (false accept rate)
   - FRR ≤ 0.05 (false reject rate)
3. **Latency:**
   - Per-session: <2 s (Mac), <5 s (phone)
   - Per-stroke embedding: <2 ms
4. **Model integrity:**
   - ONNX model hash matches committed hash in Everest 15
   - Embedding dimensionality: 256
   - Parameter count: ~250K
5. **Cross-prompt robustness:**
   - DTW-aligned distances show AUC ≥ 0.92 when enrollment and verification prompts differ
6. **Calibration curve:** predicted probability (from distance) vs. empirical match rate, within ±0.05

---

## 13. Related Work & Anchors

**Forensic document examination:**
- Osborn, A. S. (1910). *Questioned Documents*. Establishes kinematic basis for handwriting individuality.
- Hagan, D. J. (1950). *Handwriting Identification*. Pressure and jerk as writer-specific markers.

**Motor control & biometrics:**
- Plamondon, R., & Srihari, S. N. (2000). Online and off-line handwriting recognition. *IEEE Trans. Pattern Anal. Mach. Intell.* — Sigma-Lognormal model of handwriting motor control.
- Bromley, J., Bentz, J. W., Bottou, L., et al. (1994). Signature verification using a "siamese" time delay neural network. *International Journal of Pattern Recognition and Artificial Intelligence.* — Contrastive learning for biometrics.

**Benchmark datasets:**
- ICDAR Handwriting Signature Verification Competition (ongoing). Establishes evaluation protocols for kinematic-based methods.

---

## 14. Cross-References

- **Everest 12:** Handwriting capture hardware (sampling rate, calibration)
- **Everest 14:** Enrollment & principal calibration (Λ matrix, per-principal τ)
- **Everest 15:** Template format spec (model hash commitment)
- **Everest 16:** Encryption at rest for templates
- **Everest 37:** Voice-transcript distance function
- **Everest 38:** Likelihood-ratio fusion of voice + handwriting
- **Everest 39:** Drift modeling and covariance matrix updates
- **Everest 40:** Empirical FAR/FRR validation suite
- **Everest 42:** Real-time inference budget (latency SLA)
- **Everest 44:** Pedersen commitments for distance privacy
- **Everest 45:** Risk model and threshold adaptation
- **Everest 49:** Liveness detector (pre-filter before distance computation)
- **Everest 50:** Adversarial robustness test suite
- **Everest 56:** Biometric match predicate (consumer of this distance)

---

— Calm, 2026-05-20
