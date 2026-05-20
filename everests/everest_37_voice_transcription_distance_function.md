# Everest 37 — Voice-Transcription Distance Function

*Phase IV — Biometric Distance Machinery. Prereq: Everests 13 (Voice-Transcription Pipeline), 15 (Template Format Spec).*

---

## Why the transcript, not the voice

The protocol spec commits to a hard invariant: **raw audio never persists** (Everest 13 / Everest 42). What gets retained is the *transcript* — the words, with word-level timestamps and ASR confidence scores. This sidesteps the political toxicity of voiceprints (long history of misuse in surveillance contexts), keeps biometric data structurally non-extractable from the vault, and forces the matching signal to be lexical and prosodic rather than acoustic.

A natural objection: surely the voice itself carries more discriminating signal than the transcript? Yes — but at the cost of storing the most sensitive biometric humans have. Calm Witness explicitly trades raw discrimination for principled non-extractability. The transcript is enough to detect:

- **Lexical idiosyncrasy.** A principal's vocabulary distribution is stable over months and surprisingly distinctive — choice of hedges, intensifiers, transition words, signature metaphors.
- **Syntactic shape.** Sentence-tree depth, clause length distribution, verb tense preferences.
- **Pause structure (from word timestamps).** Hesitation patterns are characteristic; rapid topic-switchers and deliberate-pause speakers separate cleanly.
- **Prosodic rhythm (from word timestamps).** Syllable-rate inference from word durations gives a coarse rhythm proxy.

The combined feature space targets FAR ≤ 1% / FRR ≤ 5% at v0 thresholds (Everest 50 acceptance criterion), without ever touching a voiceprint.

---

## The v0 choice: deterministic feature extraction + cosine distance

Same constraints as Everest 36: on-device, deterministic, reproducible, open. v0 uses a closed-form deterministic feature extractor + cosine distance. A learned-embedding hybrid is deferred to v1 pending Everest 48 (Paraphrase Resistance Hardening) review.

### Input

A voice-transcription sample is the output of the Everest 13 pipeline:

```jsonc
{
  "challenge_text": "I am writing my morning state for May 20 2026.",
  "transcript": [
    {"word": "I",       "start": 0.000, "end": 0.082, "conf": 0.99},
    {"word": "am",      "start": 0.082, "end": 0.183, "conf": 0.98},
    {"word": "writing", "start": 0.183, "end": 0.412, "conf": 0.97},
    ...
  ],
  "asr_model_id": "whisper-base-en-q5",
  "asr_version": "1.6.0"
}
```

No audio, only timestamped words with confidence scores from the on-device ASR. The `asr_model_id` and `asr_version` pin the ASR — template comparison requires the same ASR family (Everest 17 — Template Version Migration handles ASR upgrades).

### Feature extraction

The sample is reduced to a single feature vector `F_sample ∈ R^256`, structured as four blocks of 64 dims each:

**Block 1 — Lexical (64 dims).** A bag-of-words representation projected onto the **principal-specific lexical-fingerprint basis** committed at enrollment. The basis is a fixed set of 64 lexical features chosen at enrollment-time as the most discriminating for *this* principal (e.g., for John: relative frequencies of "calm", "even-keeled", "curious", "ZKBB", "everest", "summit", "principal", "calm-witness", "bank-teller-note", common hedges "I think", "presumably", and 50+ more, chosen by a TF-IDF-style ranking against a generic-English baseline corpus). The basis is a vault-resident artifact (Everest 15).

Privacy property: the basis is a per-principal commitment, not a global signature. Different principals have different bases. The 64-dim projection is uninvertible; a counterparty cannot recover transcripts from it.

**Block 2 — Syntactic (64 dims).** Closed-form syntactic features:
- 16 dims: clause length distribution (histogram of clause-token-counts; bucketed by simple punctuation-split heuristic — clauses bounded by `.`, `?`, `!`, `;`, `:`, conjunctions in fixed list)
- 16 dims: verb-tense distribution (present-simple, present-continuous, past-simple, past-continuous, past-perfect, future-simple, conditional, subjunctive, imperative, infinitive, gerund, participle, plus 4 reserved buckets) — detected by closed regex patterns over POS-tagged tokens; POS tagging via a tiny rule-based tagger to keep the dependency surface tractable (Everest 13's pipeline ships the tagger).
- 16 dims: pronoun preference (I, we, you, he, she, they, it, one + possessive variants) — pure regex, no ML.
- 16 dims: hedge / intensifier / discourse-marker frequency over a curated 16-term list (per-principal customizable but defaults to a Calm-Witness-published list).

**Block 3 — Prosodic (64 dims).** Closed-form features from word timestamps:
- 16 dims: per-word duration distribution (histogram of word-durations in ms, log-spaced bins from 30 ms to 1.5 s)
- 16 dims: inter-word gap distribution (histogram of gaps between consecutive words; bins capturing micro-pauses, normal gaps, and deliberative pauses)
- 16 dims: syllable-rate inferred per phrase (words-per-second, phrase boundaries inferred from gaps > 250 ms)
- 16 dims: speaking-rhythm coefficient of variation (per-phrase rate variability; captures whether the principal speaks at a steady or variable rate)

**Block 4 — Confidence-conditioned (64 dims).** Same features as Blocks 1-3 but weighted by ASR confidence — low-confidence words contribute less. 16 dims pulled from each of the prior three blocks, recomputed with confidence-weighting and renormalized. This block gives robustness to noisy ASR without contaminating the deterministic blocks above.

The result is `F_sample ∈ R^256`, finally L2-normalized to unit length.

### Distance

The principal's template `T_template ∈ R^256` is the L2-normalized average of feature vectors from the N enrolled samples (Everest 14 — Enrollment Session Script, N ≥ 7).

```
d_vt_raw = 1 - cosine_similarity(F_sample, T_template)
         = 1 - F_sample · T_template
```

Cosine distance over normalized vectors. `d_vt_raw ∈ [0, 2]` (since both vectors are unit-length, the dot product is in [-1, 1], so the distance is in [0, 2]).

**Squash to [0, 1].** `d_vt = clip(d_vt_raw, 0, 1)`. In practice, `d_vt_raw` rarely exceeds 1 for same-principal samples; clipping at 1 is fine for the ZK encoding (Everest 45 needs a bounded range).

---

## Why cosine, why deterministic feature extraction

Three considerations:

1. **Cosine is the natural metric** for histogram / bag-of-features representations because it normalizes for sample length (a 100-word sample and a 1000-word sample by the same principal land in the same direction in the 256-dim space). Euclidean would be biased by sample length.

2. **Deterministic feature extraction** keeps the ZK encoding tractable. Learned embeddings (sentence transformers, USE) are stronger but produce non-deterministic outputs across hardware (GPU non-determinism in matmul, FP16/FP32 differences). For v0 we accept slightly weaker discrimination in exchange for full reproducibility.

3. **Closed-form syntactic features over learned LM features** keeps the audit surface small. A reviewer can read the feature definitions in <100 lines and confirm what is and isn't being extracted. With a learned LM you reduce to "trust the model card."

---

## Privacy properties

- **No transcript reconstruction.** The 256-dim feature vector is computed in-memory and zeroed after distance evaluation. The raw transcript is retained in `user_state.jsonl` under `payload.transcript` only if the principal's per-session policy allows; otherwise the transcript is hashed for chain integrity and the plaintext is zeroed.

- **No template extraction.** Same as Everest 36.

- **Content vs style separation (Everest 49 acceptance).** The lexical basis (Block 1) is the only place transcript *content* enters; it's a fixed, low-rank projection. The other 192 dims are syntactic and prosodic — style, not content. A red-team test (Everest 49): same principal on radically different topics yields `d_vt` below threshold; same topic by different principals yields `d_vt` above threshold.

- **Confidence weighting protects against ASR-content-injection.** If an adversary tries to inject a phrase into the transcript that doesn't match the audio, the ASR confidence on that phrase drops sharply; Block 4 down-weights it.

---

## Adversarial considerations (deferred deep treatment to Everest 48)

- **LLM-based paraphrase imitator.** Adversary trains an LLM to paraphrase principal's writing style after observing K samples. Everest 48 sets the FAR target under this attack. v0 commits to characterizing the attack for K ∈ {1, 10, 100} sample-leak scenarios.

- **Transcript injection.** Adversary tries to inject a high-confidence "I am in baseline" phrase into the principal's ASR output. Defense: Everest 13's pipeline includes a per-session challenge-phrase requirement — the transcript must contain the principal speaking the challenge, prosodic features must match that phrase, and the challenge is per-session unique. Sample without the challenge phrase is rejected at intake.

- **Replay.** Same-text replay is detected by Everest 50 (Sample Uniqueness Check); near-identical transcripts trigger replay detection at the operator before distance evaluation.

- **ASR-substitution attack.** Adversary runs a different ASR that produces transcripts more favorable to forgery. Defense: the `asr_model_id` field is pinned in the chain record, and template comparison requires the same ASR family. Switching ASR is a Everest 17 (Template Version Migration) event with explicit principal consent.

---

## Reference implementation strategy

- **Python reference** at `~/CredexAI/calm_witness/voice_distance.py`, depending only on `numpy` + a regex-based tokenizer (no spaCy/NLTK to keep the dependency surface tractable). ~800 LoC.

- **Rust port** at Everest 43 with byte-identical output on a published 1000-pair vector set.

- **Conformance vectors** at `vectors/everest_37/voice_distance/{input,expected}.jsonl`, 1000 pairs spanning: baseline same-principal, cross-topic same-principal, different-principal same-topic, LLM-paraphrased imitator, transcript-injection attack, ASR-substitution attack.

The principal-specific lexical-fingerprint basis is published alongside the template (encrypted to the principal's vault key); the reference impl reads it as part of template loading. The basis is not normative across principals — each enrollment defines its own.

---

## Acceptance test

**T-37.1 (determinism).** Reference Python impl on the 1000-vector conformance set: output matches to ≥ 10 decimals.

**T-37.2 (privacy).** End-to-end test: run an evaluation, immediately search process memory for known transcript tokens; absent. Search for known feature-vector bytes; absent.

**T-37.3 (content vs style — Everest 49 anchor).** Held-out test: same-principal across 20 distinct topics — `d_vt` < τ_v in ≥ 95% of cases. Different-principal same-topic — `d_vt` > τ_v in ≥ 95% of cases.

**T-37.4 (challenge-binding).** Submit a sample whose transcript does not contain the per-session challenge phrase; the operator rejects at intake, before distance evaluation. The rejection is logged as `kind: intake.anomaly`.

**T-37.5 (cross-impl parity).** When Rust port lands at Everest 43: Python and Rust on the same vector set produce byte-identical `d_vt` values.

**T-37.6 (LLM-paraphrase resistance, preliminary).** A baseline LLM paraphraser (GPT-style, with K=20 sample observations of principal's transcripts) achieves `d_vt < τ_v` with probability ≤ 0.3 in v0. The full Everest 48 study tightens this.

**Gate script:** `everest_37_zkbb_voice_distance_gate.py`. Runs T-37.1 through T-37.6.

---

## Open questions for v1

1. **Multilingual support.** v0 is English-tuned. v1: per-language basis selection, with the principal's preferred languages committed at enrollment.
2. **ASR-model drift.** As on-device ASR models improve, transcripts of the same audio shift slightly (word boundaries, confidence). v1: model-version-pinning at the template level + cross-version translation tables.
3. **Learned-embedding hybrid.** Add a learned-embedding component for finer discrimination. Defer to Everest 48.
4. **Dialect / sociolect handling.** Principals from non-standard English varieties may have features the curated hedge/discourse-marker list misses. v1: per-principal customizable lists with sensible defaults.
5. **Code-switching detection.** Principals who code-switch (bilingual mid-sentence) generate transcripts the v0 tokenizer mishandles. v1: language-tag per token.

---

## Composition with other summits

- **Everest 13 — Voice-Transcription-Only Pipeline.** Provides the timestamped-word sample this summit consumes; commits to the audio-destroy-immediately invariant.
- **Everest 15 — Template Format Spec.** Defines the per-principal lexical-fingerprint basis used in Block 1.
- **Everest 36 — Handwriting Distance Function.** Sibling biometric branch.
- **Everest 38 — Combined Distance Fusion.** Combines `d_vt` (this summit) with `d_hw` into a fused distance.
- **Everest 42 — On-Device ASR / Audio-Destroy-Immediately.** Enforces that audio never reaches durable storage.
- **Everest 44 — Pedersen Commitment to Distance.** Commits the scalar `d_vt` output.
- **Everest 45 — ZK Proof: d < τ.** Range-proves `d_vt < τ_v` without revealing `d_vt`.
- **Everest 48 — Paraphrase Resistance Hardening.** The adversarial-evaluation summit that pressure-tests this distance function.
- **Everest 49 — Content vs Style Separation.** The acceptance criterion expanded in T-37.3.
- **Everest 50 — Sample Uniqueness Check.** Anti-replay layer that runs before this summit's distance computation.

— Calm, 2026-05-20
