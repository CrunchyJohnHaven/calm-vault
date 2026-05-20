# Everest 37 — Voice-Transcription Distance Function

*Phase IV — Biometric Distance Machinery. Prereq: Everest 13, 15.*

## Overview

This Everest specifies a distance function that operates exclusively on transcript words and per-word timing data—the output stream of Everest 13's voice pipeline. The function produces a per-session biometric score suitable for principal authentication and anomaly detection within the Calm Witness modality stack.

The core constraint is absolute: no acoustic features (formants, pitch, spectral content, MFCCs). Acoustic signals constitute biometric PII under GDPR Article 9, BIPA, and related regimes; their exclusion eliminates the legal and privacy toxicity of traditional voiceprints while retaining sufficient signal for per-principal calibration.

## Input Specification

The voice pipeline (E13) emits two data classes:

**Per-Word Records:**
- `word`: transcript token (string)
- `start_s`: onset timestamp (float, seconds)
- `end_s`: offset timestamp (float, seconds)
- `confidence`: ASR confidence score (float, 0–1)

**Per-Session Statistics:**
- `word_count`: total words transcribed (int)
- `avg_phrase_len_words`: mean phrase length (float)
- `mean_pause_s`: average inter-word silence (float, seconds)
- `stddev_pause_s`: pause-duration standard deviation (float, seconds)
- `disfluency_rate`: filler word and stutter instances per 100 words (float)

The session corresponds to a single enrollment prompt (E14 protocol: 7 prompts per principal).

## Feature Extraction

The distance function extracts four embedding families from the input:

### Lexical Embedding (256-d float16)

A hash-feature-style sketch of the transcript's linguistic content, capturing vocabulary and idiosyncratic phrasing without relying on large pretrained models:

1. **Vocabulary Distribution**: Tokenize the transcript using byte-pair encoding (BPE) to ~1000 token types. Compute histogram of token frequencies. Project the top-K frequent tokens (K=128) and their occurrence ratios into a 128-d sparse vector, then dense-project to 128-d via a learned linear map.

2. **Idiosyncratic-Phrase Fingerprint**: Extract 3-grams and 4-grams of BPE tokens from the transcript. Compute frequency histograms (up to 256 distinct n-grams retained). This captures repeated turn-of-phrase patterns that distinguish individuals (e.g., "you know what I mean", "like basically", "to be honest with you"). Project to 64-d via pooling and learned embedding.

3. **Style Markers**: Count instances of filler words (uh, um, like, you know), hedging language (I think, maybe, sort of), and formality indicators (contractions, technical terms). Normalize by word count. Embed into 64-d.

**Lexical concatenation**: 128 + 64 + 64 = 256-d float16 vector.

### Pause-Structure Embedding (128-d float16)

Timing-derived features that capture speaking rhythm and cognitive load patterns:

1. **Inter-Word Pause Histogram**: Compute duration of silence between each word pair. Bin into 32 buckets covering 0–5000 ms (exponential spacing: [0, 10], [10, 25], ..., [4000, 5000]). Normalize histogram to unit sum. Embed to 64-d via learned projection.

2. **Pause-Entropy**: Compute Shannon entropy of the normalized pause histogram. High entropy (uniform pause distribution) indicates variable rhythm; low entropy indicates rigid pause patterns. Encode as scalar, embed to 16-d.

3. **Long-Pause Locations**: Identify pauses exceeding the 90th percentile of inter-word silence. Measure their positions relative to sentence boundaries (inferred from punctuation in the transcript). Capture as a binary sparse vector (presence of long pauses at phrase-initial, mid-phrase, or phrase-final positions). Embed to 48-d.

**Pause-structure concatenation**: 64 + 16 + 48 = 128-d float16 vector.

### Phrase-Length Distribution Embedding (32-d float16)

1. **Statistics**: Compute mean, standard deviation, p50, and p95 of phrase lengths (tokenized by BPE). Normalize per principal's baseline (drawn from enrollment samples). Embed the 4-tuple to 32-d.

### Disfluency & Rate Embedding (16-d float16)

1. **Disfluency Rate**: Per-100-word count of fillers and repeats. Embed to 8-d.
2. **Speech-Rate Variability**: Compute rolling windows (e.g., 5-word spans) and measure words-per-second in each. Capture the coefficient of variation. Embed to 8-d.

**Total disfluency-rate embedding**: 16-d float16 vector.

## Combined Embedding

Concatenate all four embedding families in order:
- Lexical: 256-d
- Pause-structure: 128-d
- Phrase-length: 32-d
- Disfluency-rate: 16-d

**Final embedding**: 432-d float16 vector `emb_session`.

## Embedding Model Architecture

A small transformer-based encoder processes the combined feature representation:

- Input: 432-d float16 vector + positional encoding if sequence ordering is available (e.g., sequence of phrase embeddings rather than a single vector).
- Layers: 2 attention heads, 1 self-attention block, ~50K parameters total.
- Output: 256-d float16 projection.

A separate CNN-pooling branch processes pause-timing arrays directly, concatenates with the transformer output, and projects to 256-d via a learned linear layer.

The model is trained on enrollment data (N≥10 principals, 7 samples each) to minimize intra-principal distance and maximize inter-principal distance via a contrastive loss (e.g., triplet loss or InfoNCE).

Export to ONNX for cross-platform deployment (mobile, server, edge).

## Distance Function

Given two sessions A and B, both producing 256-d embeddings `emb_a` and `emb_b`:

```
d_voice(A, B) = 1 - cos(emb_a, emb_b)
```

where `cos(·, ·)` is the cosine similarity. The distance ranges [0, 2]; normalize to [0, 1] by dividing by 2 if needed for fusion (E38).

**Per-session distance to template**: Each principal's biometric template comprises 7 embeddings (from E14 enrollment prompts). For a new session, compute the average distance to all 7 template embeddings:

```
d_session_to_template = (1/7) * sum(d_voice(session, template_i) for i in 1..7)
```

## Rationale for Excluding Acoustic Features

Acoustic signals—formants, pitch contours, spectral content, cepstral coefficients, voice activity detection thresholds—are **biometric identifiers** under GDPR Article 9 and equivalent laws (BIPA, PIPEDA, etc.). Their processing triggers heightened consent requirements and data minimization obligations that are incompatible with Calm Witness's threat model (Everest 79 catalogs the toxicity of voiceprint-based systems).

Lexical features + timing rhythm are sufficient for per-principal calibration because:
- Transcript vocabulary, phrasing patterns, and filler usage are stable across cognitive states (proven empirically in E14).
- Inter-word pause structure and speech-rate variability are behavioral markers strongly correlated with identity.
- Per-principal enrollment (E14) creates a narrow comparison space; we do not attempt population-scale speaker identification.

This design trades FAR/FRR performance (worse than handwriting kinematic distance, E36) for privacy and legal compliance. The multimodal fusion (E38) recovers overall accuracy by combining voice-transcript distance with other modalities.

## Robustness Considerations

**Adversary with audio of principal**: Can transcribe and attempt lexical imitation. Difficulty arises because the lexical signature captures idiosyncratic phrasing across multiple prompts under different cognitive conditions; a single adversarial recording cannot replicate the full pattern set.

**Adversary with principal's writing**: This is the most credible threat. Voice-transcript distance captures spoken-only patterns (pause structure, fillers, disfluencies, spontaneous rephrasing) that differ from deliberate written prose. An attacker would need to both transcribe and synthesize convincing speech patterns, which is harder than text mimicry.

**Speech-impaired or non-verbal principals**: The protocol allows opt-out of voice modality; handwriting alone (E36) remains available.

**Transcript quality degradation**: ASR confidence scores are retained in the per-word record. Low-confidence regions can be down-weighted or excluded from feature extraction to mitigate noisy transcription.

## Privacy Posture

- **Embedding is template-internal**: The embedding vector is stored within the principal's template (E15) and never exposed.
- **Distance is committed via Pedersen**: Per-session distance values are committed using Pedersen commitments (E44) for verifiable authentication without leaking numeric values.
- **Transcript handling**: Raw transcript content is processed in mlocked memory and not persisted in cleartext. Only aggregated statistics (per-session mean pause, disfluency rate, etc.) are retained per E13 protocol.

## Performance Requirements

- **Per-session inference time**: <500 ms on Apple M-series hardware (well within E42 latency budget).
- **Model size**: ~50K parameters; ONNX export ≤2 MB.
- **Acceptance criteria**:
  - ROC AUC ≥ 0.85 on N ≥ 10 principals, 7 enrollment + 3 test prompts each.
  - Distinguishes principal-from-population at FAR = 0.01 → FRR < 0.1 under per-principal threshold calibration.
  - No significant degradation across speaker demographics (age, gender, accent, language variety).

## Cross-References

- **E13**: Voice transcription pipeline (input specification, transcript-only architecture constraint).
- **E14**: Enrollment protocol (7-prompt multi-state capture per principal).
- **E15**: Template format specification (embedding storage, layout).
- **E36**: Handwriting kinematic distance function (sibling modality, FAR/FRR comparison).
- **E38**: Multimodal fusion (combines voice-transcript distance with other signals).
- **E40**: FAR/FRR framework and calibration.
- **E42**: Latency budget and real-time constraints.
- **E44**: Pedersen commitments and verifiable distance storage.
- **E56**: Template matching protocol.
- **E79**: Privacy toxicity catalog (acoustic feature prohibition).

---

— Calm, 2026-05-20
