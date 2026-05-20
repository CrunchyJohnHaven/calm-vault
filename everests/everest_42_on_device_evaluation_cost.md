# Everest 42 — On-Device Evaluation Cost Target

*Phase IV — Biometric Distance Machinery. Prereq: Everest 36, 37.*

---

## 1. Purpose and Scope

This Everest defines the latency and resource budgets for real-time, on-device evaluation of biometric distance functions (Everest 36: handwriting kinematic distance; Everest 37: voice-transcription distance; Everest 38: joint multimodal fusion) across a spectrum of hardware platforms. The acceptance criterion is unambiguous: both primary distance functions must complete within strict latency bounds on representative device classes, with predictable performance and no regression across software versions.

The latency budget is composed of per-modality inference time, feature aggregation, and distance computation. It excludes proof generation (Everest 65 owns proof latency and documents its budget here by reference).

---

## 2. Hardware Platform Tiers

Distance evaluation targets four hardware classes, each with a distinct latency ceiling:

**Tier 1: M-series Mac (M1, M2, M3, M3 Max)**
- Target latency: <2 seconds for full re-evaluation (all modalities, all samples)
- Sustained budget: ~1.5 seconds
- Headroom: 0.5 seconds (reserved for proof generation, logging, state reconciliation)

**Tier 2: iPhone 15, iPad Pro (2022+), flagship Android**
- Target latency: <3 seconds for full session evaluation
- Sustained budget: ~2.5 seconds
- Headroom: 0.5 seconds

**Tier 3: iPhone 13–14, iPad Air, mid-range Android (Snapdragon 8 Gen 1)**
- Target latency: <5 seconds for full session evaluation
- Sustained budget: ~3.5 seconds
- Headroom: 1.5 seconds

**Tier 4: iPhone 12 or older, entry-level Android**
- Not supported in v0. Upgrade path via CLI-only evaluation on paired desktop (Everest 48).

---

## 3. Per-Modality Latency Budget

### 3.1 Handwriting Distance (Everest 36)

A typical evaluation session comprises 7 handwriting samples, each with ~25–30 strokes captured during enrollment (Everest 14).

**Per-stroke inference:**
- Input: kinematic events (timestamps, x, y, pressure, tilt, azimuth)
- Embedding model: 1D-CNN (3 layers) + lightweight Transformer, 250K parameters
- Output: 256-d embedding vector
- Latency: <1 ms per stroke on M-series Mac (ONNX runtime + SIMD acceleration)

**Per-sample aggregation (7 strokes per sample):**
- Distance computation: cosine or Mahalanobis across aligned stroke embeddings
- Aggregation: median + 95th percentile weighting
- Latency: ~10 ms per sample

**Per-sample total:** ~1 ms × 30 strokes + 10 ms aggregation = **~40 ms per sample**

**Full session (7 samples):** 40 ms × 7 samples = **~280 ms**

**With DTW (cross-prompt comparison, optional):**
- DTW alignment cost: O(M × N) where M, N ≤ 30 strokes
- Approximately 2–3× slower; approximately 70 ms per sample pair
- Typical use: compare live sample to all 7 template samples → 70 ms × 7 = **~490 ms**

**Handwriting budget allocation:**
- M-series Mac: 350 ms (inclusive of DTW if needed)
- Tier 2: 500 ms
- Tier 3: 1000 ms

---

### 3.2 Voice-Transcription Distance (Everest 37)

A typical enrollment session yields a 7-item template (one embedding per prompt, Everest 14). Per-session evaluation compares a new recording against all 7 templates.

**Per-sample feature extraction:**
- Input: transcript words (tokens, timings, ASR confidence)
- Feature families: lexical (256-d), pause-structure (128-d), phrase-length (32-d), disfluency-rate (16-d)
- Extraction latency: ~20 ms per sample

**Per-sample embedding inference:**
- Small transformer + CNN-pooling, ~50K parameters
- Output: 256-d float16
- Latency: ~30 ms per sample on M-series Mac

**Per-session distance (7 template embeddings):**
- Cosine distance: O(1) per pair, ~1 ms × 7 = ~7 ms
- Average to template: <1 ms

**Voice-transcript budget allocation:**
- Per-sample embedding + feature extraction: ~50 ms
- Per-session comparison (7 templates): ~210 ms (7 samples × 30 ms each)
- Total: **~210–260 ms per session**

---

### 3.3 Joint Multimodal Fusion (Everest 38)

Fusion of handwriting distance and voice-transcription distance via likelihood-ratio test (Everest 38 owns the statistical model).

**Computation:**
- Input: d_h (handwriting distance), d_v (voice distance), per-principal calibration parameters
- Likelihood-ratio: `LR = P(d_h, d_v | same) / P(d_h, d_v | different)` — estimated via logistic regression or Bayes' rule
- Output: fused distance or binary decision

**Latency: <1 ms** (O(1) algebraic operation, no inference)

---

## 4. Total Session Evaluation Budget

### 4.1 M-series Mac (Tier 1)

| Component | Latency | Notes |
|-----------|---------|-------|
| Handwriting (7 samples + aggregation) | 350 ms | Cosine distance, no DTW |
| Voice-transcription (7 samples) | 210 ms | Feature extraction + embedding inference |
| Multimodal fusion (Everest 38) | <1 ms | Likelihood-ratio computation |
| **Subtotal** | **~560 ms** | |
| Headroom | 940 ms | Available for proof generation, logging, state |
| **Total budget** | **<2000 ms** | Acceptance: p99 < 2 s |

### 4.2 iPhone 15 / iPad Pro (Tier 2)

| Component | Latency | Notes |
|-----------|---------|-------|
| Handwriting (7 samples) | 500 ms | Account for slower CPU than M3 |
| Voice-transcription | 350 ms | Slightly slower embedding inference |
| Multimodal fusion | <1 ms | |
| **Subtotal** | **~850 ms** | |
| Headroom | 1150 ms | Proof generation, optional ML acceleration |
| **Total budget** | **<3000 ms** | Acceptance: p99 < 3 s |

### 4.3 iPhone 13–14 (Tier 3)

| Component | Latency | Notes |
|-----------|---------|-------|
| Handwriting (7 samples) | 1000 ms | 2–3× slower than M-series |
| Voice-transcription | 700 ms | Slower transformer inference |
| Multimodal fusion | <1 ms | |
| **Subtotal** | **~1700 ms** | |
| Headroom | 3300 ms | Proof generation, caching, retry logic |
| **Total budget** | **<5000 ms** | Acceptance: p99 < 5 s |

---

## 5. Optimization Strategies

### 5.1 Cached Embeddings

The embedding vectors (handwriting 256-d, voice 256-d) for the enrolled template are precomputed and stored encrypted at rest (Everest 16). On-device evaluation uses cached embeddings without recomputation unless the template is updated (rare operation, excluded from session latency).

**Implication:** Distance evaluation is O(1) per sample pair, avoiding redundant embedding inference.

### 5.2 Model Quantization

Both the handwriting and voice embedders are quantized to int8 precision via ONNX quantization tools. This reduces model size (~40% reduction) and inference latency (2–3× speedup) with minimal accuracy loss (< 1% FAR/FRR change, validated per Everest 40).

**Tier 1 (M-series):** Quantization optional; use fp32 for maximum precision if latency headroom permits.

**Tier 2–3 (mobile):** Quantization mandatory to meet latency targets.

### 5.3 GPU Acceleration (Optional)

**iOS:** CoreML model export (iPhone 15 Pro has Neural Engine; iPhone 13–14 falls back to CPU). CoreML inference is 1.5–2× faster than ONNX runtime on CPU.

**Android:** NNAPI (Android Neural Networks API) on Snapdragon 8 Gen 2+ offers similar acceleration.

**Budget impact:** 30–40% latency reduction on Tier 2–3 devices. Not assumed in the budgets above (conservative estimate).

### 5.4 Predicate Short-Circuiting

Some predicates (Everest 56) may not require full re-evaluation of distance functions. For example, `in_baseline_24h` depends only on the log, not the biometric distance. If a predicate's truth can be determined from cached state without fresh distance computation, skip evaluation.

**CI enforcement:** the benchmark suite verifies that unnecessary re-evaluations are not triggered.

---

## 6. Performance Regression Detection and CI

Every pull request that touches distance-function code, quantization definitions, or inference pipeline must pass a automated benchmark suite.

**CI harness:**
- Benchmark suite: `calm-witness benchmark distance --modality {handwriting,voice,joint}` (synthetic data, reference hardware)
- `calm-witness benchmark proof` (proof-generation latency, owned by Everest 65)
- Runs on a fixed hardware fleet (one Mac M2, one iPhone 14, one Snapdragon 8 Gen 1 representative device)
- Measured metrics: p50, p95, p99 latency for each modality and per platform

**Regression gate:**
- If any p99 latency increases >10% on any platform: PR is blocked pending investigation and explanation
- If median latency increases >5% across all platforms: PR author must justify or refactor
- Metrics are tracked in CI artifacts for historical trending

**Test corpus:** 50 representative sessions (handwriting + voice samples) from N ≥ 10 principals, multiple cognitive states.

---

## 7. Memory Budget

The total runtime memory footprint must remain below 50 MB on all Tier 2+ devices to avoid OOM events during evaluation.

**Breakdown:**

| Component | Size | Notes |
|-----------|------|-------|
| Distance models (ONNX, quantized) | <10 MB | Handwriting ~1.2 MB, voice ~2 MB, totals after quantization |
| Per-session working memory | ~50 KB | Embeddings, distance matrices, temporary tensors |
| Template (encrypted at rest, decrypted in-memory) | <5 MB | 7 handwriting embeddings (7 × 256-d float32) + 7 voice embeddings + metadata |
| Proof-generation scratch | ~20 MB | Pedersen commitments, temporary polynomials (owned by Everest 65) |
| Rust runtime, ONNX allocators | ~10 MB | Base overhead |
| **Total** | **<50 MB** | Sustained; excludes OS memory mapping |

---

## 8. Power Budget (Composition with Everest 89)

On mobile platforms, biometric evaluation must not drain battery excessively.

**Per-session evaluation:** <0.2% of battery capacity on iPhone 14
- Rationale: A user might evaluate 20 times per day; acceptable total is <4% per day.

**Per-disclosure event (evaluation + proof generation):** <0.5% of battery
- Includes proof-generation overhead (Everest 88).

**Validation:** Power measurements via Xcode Instruments (Energy Impact profile) or Android's Battery Historian. If measured power exceeds budget, implement CPU throttling or deferral strategies (Everest 89 owns these trade-offs).

---

## 9. Implementation Notes

### 9.1 Runtime and Libraries

**Language:** Rust  
**Inference engine:** onnxruntime (v1.18+, cross-platform)  
**Linear algebra:** ndarray + BLAS (via openblas or Accelerate framework on macOS)  
**SIMD acceleration:** portable_simd for custom cosine distance and Mahalanobis distance kernels

**FFI bindings:**
- onnxruntime-rust (official bindings)
- iOS/Android: platform-specific ONNX runtime builds (CoreML export for iOS, NNAPI for Android where available)

### 9.2 Profiling and Instrumentation

**Profiling harness:**

```bash
calm-witness benchmark distance --modality handwriting --samples 50 --verbose
calm-witness benchmark distance --modality voice --samples 50 --verbose
calm-witness benchmark distance --modality joint --samples 50 --verbose
calm-witness benchmark proof --samples 50 --verbose
```

Each harness emits:
- Per-modality latency histogram (p50, p95, p99)
- Per-component breakdown (feature extraction, embedding inference, distance computation, aggregation)
- Memory peak (via system allocation trackers)
- Per-platform results table (Mac M2, iPhone 14, Snapdragon device)

---

## 10. Interdependencies

- **Everest 36:** Handwriting distance function (consumer of this latency budget)
- **Everest 37:** Voice-transcription distance function (consumer)
- **Everest 38:** Multimodal fusion (consumer; adds <1 ms)
- **Everest 40:** Accuracy validation (FAR/FRR targets; latency is independent of accuracy)
- **Everest 45:** Risk model and threshold tuning (may adjust distance-computation depth; coordinated with latency budget)
- **Everest 48:** Unsupported-device fallback (CLI-only on paired desktop)
- **Everest 56:** Template matching predicate (consumer of distance evaluation)
- **Everest 65:** Proof-generation budget (sibling; documented separately; combined total <2 s on Mac)
- **Everest 81:** Rust implementation (owns the code that executes within this budget)
- **Everest 85:** CI performance-regression detection (runs automated benchmarks per PR)
- **Everest 88:** Proof-generation performance budget (separate, but composes with this budget for total session latency)
- **Everest 89:** Mobile power budget (composition; this latency determines power draw)

---

## 11. Acceptance Criteria

1. **Handwriting distance evaluation:**
   - M-series Mac: <350 ms (7 samples, all modalities)
   - Tier 2 (iPhone 15): <500 ms
   - Tier 3 (iPhone 13–14): <1000 ms

2. **Voice-transcription distance evaluation:**
   - M-series Mac: <210 ms
   - Tier 2: <350 ms
   - Tier 3: <700 ms

3. **Multimodal fusion:**
   - All platforms: <1 ms

4. **Full session evaluation (all modalities, templates, aggregation):**
   - M-series Mac: p99 < 2 seconds (sustained <1.5 s)
   - Tier 2: p99 < 3 seconds (sustained <2.5 s)
   - Tier 3: p99 < 5 seconds (sustained <3.5 s)

5. **Performance regression detection:**
   - Every PR: benchmark suite runs on fixed fleet
   - Regression gate: p99 latency increase >10% on any platform blocks PR
   - Metrics tracked historically for trending

6. **Memory footprint:**
   - Distance models: <10 MB
   - Template (in-memory decrypted): <5 MB
   - Total runtime: <50 MB on Tier 2+ devices

7. **Power consumption (Tier 2–3 devices):**
   - Per-session evaluation: <0.2% battery
   - Per-disclosure event: <0.5% battery

---

— Calm, 2026-05-20
