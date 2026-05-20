# Everest 13 — Voice-Transcription-Only Pipeline

*Phase II — Capture & Enrollment. Prereq: Everest 11.*

---

## One-Line Decision

A local-only automatic-speech-recognition (ASR) pipeline using whisper.cpp small.en model produces transcript + per-word timing output only, with the raw audio file destroyed at end-of-session via explicit_bzero(). Raw audio never persists to disk or network, making voiceprint leakage structurally impossible.

---

## §1. Top-Level Architecture

The voice-transcription pipeline accepts microphone input, performs local inference via whisper.cpp, and outputs a structured transcript with per-word timing and confidence scores. The input is buffered in a memory region locked with mlock(2) to prevent swap-to-disk. After inference is complete, the raw audio buffer is overwritten with zeros using explicit_bzero() to ensure cryptographic destruction; the buffer memory region is then released. A destruction-proof record is written to the chain, confirming the buffer was zeroed (as evidenced by a NULL SHA-256 hash of the now-empty region). At no point does the operator, the principal, or any downstream system have access to the raw audio itself — only the transcribed text and temporal metadata.

This design eliminates the most severe threat in voice-based biometrics: the voiceprint (speaker embedding). Voiceprints encode fundamental frequency, formants, spectral features, and speaker-identification vectors — all of which are classified as biometric data under GDPR Art. 9 and similar high-bar consent regimes (BIPA, California CCPA). Transcripts carry only lexical and timing-derived features: word sequence, vocabulary frequency, pause structure, disfluency rate — features rich enough to serve as a behavioral signature but acoustically opaque. An attacker with possession of a transcript cannot reconstruct voiceprint features because the audio that generated it is cryptographically destroyed at the source.

---

## §2. Pipeline Architecture (Numbered Steps)

1. **Microphone input acquisition (16 kHz, 16-bit PCM).** The principal speaks into a wired USB microphone or the capture tablet's integrated microphone. Audio is streamed at 16 kHz sampling rate, 16-bit signed integer samples. The audio stream is directed into an in-memory circular buffer of fixed size (e.g., 10 seconds at 16 kHz = 160k samples = 320 KB). This buffer is allocated via mmap(MAP_PRIVATE | MAP_ANONYMOUS) and locked immediately with mlock(2), preventing the kernel from paging it to swap. All pointer-to-buffer operations are wrapped in volatile casts to prevent compiler reordering of the buffer access relative to the destruction step.

2. **Voice activity detection (VAD) for buffer efficiency.** Before whisper.cpp inference, a lightweight voice-activity detector (e.g., WebRTC VAD, running in-process) identifies and trims silent regions. This step keeps the buffer small and avoids passing long silences to the inference engine. The VAD is stateless and operates on a fixed window (e.g., 20 ms frames). Silence trimming occurs in-place: the trimmed buffer (containing only the voiced regions) is passed to step 3. No auxiliary buffer is allocated for trimming.

3. **whisper.cpp local inference (small.en, ~244 MB model).** The trimmed buffer is passed to whisper.cpp's local inference engine. The model runs entirely on the device (no cloud call, no network transmission of audio). Output includes:
   - An array of transcribed words (UTF-8 strings).
   - Per-word start and end timestamps (in seconds, float).
   - Per-word confidence scores (0–1 float).
   - Sentence and paragraph breaks inferred from longer pauses.
   Model version: "whisper-small.en-v3" (English-only for v0; multilingual added in v1). The small.en model achieves ~7% word-error-rate on conversational English, runs in <2x real-time on M-series silicon (M1/M2/M3), and is openly licensed under MIT.

4. **Output struct construction and raw-audio destruction.** Upon successful inference, construct a transcript output struct:
   ```
   {
     "transcript_words": [
       { "word": "hello", "start_s": 0.12, "end_s": 0.35, "confidence": 0.98 },
       { "word": "world", "start_s": 0.45, "end_s": 0.62, "confidence": 0.96 },
       ...
     ],
     "stats": {
       "word_count": N,
       "avg_phrase_len_words": float,
       "mean_pause_s": float,
       "stddev_pause_s": float,
       "disfluency_rate": float
     },
     "model_version": "whisper-small.en-v3",
     "model_hash": "<sha256 of model binary>",
     "session_id": "<uuid>",
     "sample_id": "<uuid>",
     "destruction_proof": null
   }
   ```
   **Critical: Before returning the output struct, destroy the raw audio buffer.** Call explicit_bzero(audio_buffer, buffer_size_bytes) to overwrite every byte with zero. Use explicit_bzero (not memset or loop-based clearing) to prevent compiler elision of the overwrite as dead code. After zeroing, call munmap() to release the locked memory region. Record the buffer's original SHA-256 hash prior to zeroing; after zeroing, recompute the hash — it should be the SHA-256 of all-zeros (i.e., a canonical NULL hash). Write this NULL hash to the `"destruction_proof"` field in the output struct as cryptographic evidence that the buffer was destroyed.

5. **Append transcript to chain.** The output struct is serialized to JSON and appended to the principal's `user_state.jsonl` with:
   - `kind: "voice_sample"`
   - `prev_hash: <sha256 of prior record>`
   - All fields from step 4 above.
   - No `raw_audio` field. No compressed audio. No spectrogram. No acoustic embeddings.
   Write this record to the chain-head (published to Sigsum transparency log in a subsequent session for freshness anchoring per Everest 31).

---

## §3. Model Choice: whisper.cpp small.en

**Why whisper.cpp:** OpenAI's Whisper model is openly licensed (MIT), fully local (no cloud calls), deterministic (whisper.cpp flag: WHISPER_DETERMINISTIC), and has published accuracy data. It runs on consumer hardware without a GPU. The .cpp variant (whisper.cpp by Georgi Gerganov) is a pure C++ inference engine with no external ML runtime dependency, reducing supply-chain attack surface.

**Why small.en, not other sizes:**

- **Reject tiny.** ~39 MB, ~16 WER. Too lossy; phrase-structure fidelity degrades unacceptably.
- **Small (244 MB), ~7 WER.** Sweet spot: sufficient accuracy to capture idiomatic speech patterns (phrase length, vocabulary choice, pause structure) without excess latency.
- **Reject medium/large.** Medium is ~1.5 GB, ~4–5 WER; large is ~2.9 GB, ~3–4 WER. For lexical-signature purposes, the WER gain does not justify the 6–12x memory and latency cost. M1 median inference time: small ~10 seconds per minute of audio; large ~40+ seconds. Enrollment ceremony time already runs 60+ minutes (per Everest 11); we do not burden it with unnecessary latency.

**Model determinism:**

Compile whisper.cpp with WHISPER_DETERMINISTIC=1 to disable non-deterministic operations (e.g., variable-precision floating-point accumulation). With this flag, the same audio file produces bit-stable output across multiple runs. Acceptance test (§5) verifies this.

**English-only in v0:**

Everest 13 v0 supports small.en only (English). Multilingual support (small / medium multilingual) is deferred to v1. Code-switching (e.g., "the project is très intéressant") is also v1+. Principals who speak languages other than English can use handwriting-only enrollment (Everest 11 permits this) until the multilingual pipeline ships.

---

## §4. Lexical Fingerprint: What is Captured

The transcript + timing record encodes:

- **Token sequence.** The exact ordered sequence of words spoken.
- **Vocabulary frequency.** Which words the principal uses; relative frequency of rare vs. common words.
- **Phrase-level statistics.** Average length of spoken phrases (measured in words); distribution of phrase lengths.
- **Pause structure.** Inter-word and inter-phrase pause durations (start_s and end_s fields); mean, median, standard deviation, and distribution shape of pauses.
- **Disfluency rate.** Count of filler words ("um," "uh," "like," "well," "you know") as a fraction of total words.
- **Punctuation-equivalent rhythm.** Longer pauses (e.g., >0.5 seconds) inferred from per-word timing mark sentence or clause boundaries; the pattern of pause magnitudes encodes speaking rhythm.
- **Utterance length and complexity.** Total word count and mean complexity (proxy: average word length in characters).

This lexical profile is robust over weeks and months — it captures habitual speech patterns that persist even when a principal is tired, ill, or in an unusual emotional state. Under time pressure or during high-stress conversation, the profile remains recognizable because a principal cannot easily suppress their vocabulary, phrase patterns, or pause habits.

---

## §5. What is NOT Captured (Structural Impossibility of Voiceprint Leakage)

The following acoustic features are **not** stored, **not** computed, and **structurally impossible** to extract from the pipeline's output:

- **Pitch / fundamental frequency (F0).** Requires spectral analysis of the raw audio waveform. Removed at step 4 (buffer destroyed before any spectral operation).
- **Formants (F1, F2, F3, ...).** Frequency-domain features extracted from the audio signal. Impossible without raw audio.
- **Speaker embedding (x-vectors, d-vectors, w2v2 embeddings).** Neural models trained to map audio to a continuous speaker-identity space. Requires raw waveform input.
- **Mel-frequency cepstral coefficients (MFCCs).** Spectrograms and spectral features. Removed at step 4.
- **Speaker identification likelihood (PLDA, i-vector scores).** Probabilistic models trained to map acoustic features to speaker identity. Removed at step 4.
- **Prosodic features (intensity contour, spectral tilt, voice quality).** Requires full-waveform analysis.

The destruction of the raw audio buffer at step 4 occurs **before** any of these features could be extracted. whisper.cpp's internal inference does compute spectrograms and acoustic embeddings (internally, to feed the Transformer), but these are ephemeral — they exist only in CPU cache and VRAM during the forward pass and are not persisted. The only persistent output is the text transcript and timing.

An attacker with read access to the entire `user_state.jsonl` chain cannot recover voiceprint features because they were never stored. An attacker who compromises the principal's device *during* the buffer-destruction step might capture the buffer before destruction, but the protocol does not assume defense against a live, mid-execution compromise — that is Everest 21 (Enrollment Fraud Taxonomy). For v0, the threat model assumes an attacker with post-hoc access to the vault's persistent state, not real-time memory access during inference.

---

## §6. Audio Destruction Protocol (Critical Security Property)

1. **Buffer allocation with memory-lock guarantee.** At pipeline start, allocate the circular buffer:
   ```c
   audio_buf = mmap(NULL, BUF_SIZE, PROT_READ | PROT_WRITE,
                     MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
   mlock(audio_buf, BUF_SIZE);  // Prevent swap to disk
   ```
   mlock(2) raises MEMLOCK ulimit if needed (requires privilege or CAP_IPC_LOCK). The buffer never leaves physical RAM; if the system runs out of memory and kills processes, the audio buffer will be the first evicted (it is not in swap, and the kernel's OOM killer will use lru_gen or similar). On M-series Macs, mlock is a no-op for usable RAM; the kernel's page replacement is memory-efficient enough that this buffer will remain resident.

2. **Inference and zeroing.** After whisper.cpp inference completes:
   ```c
   sha256_hash_before = sha256(audio_buf, buf_size);  // Record for proof
   explicit_bzero(audio_buf, buf_size);                // Overwrite with zeros
   sha256_hash_after = sha256(audio_buf, buf_size);   // Should be NULL-hash
   assert(sha256_hash_after == sha256_zeros);          // Verify destruction
   munmap(audio_buf, buf_size);                        // Release region
   ```

3. **Compiler reordering protection.** The explicit_bzero() function (or equivalent from libsodium or Rust's zeroize crate) is defined to prevent the compiler from dead-code-eliminating the overwrite. Unlike memset(), which a compiler can omit if it sees the buffer is no longer used after the call, explicit_bzero() is a volatile operation that the compiler must emit. In Rust, use `zeroize::Zeroize` trait or the zeroize macro. In C, use explicit_bzero() from string.h (POSIX 2016) or SecureZeroMemory() (Windows), or libsodium's sodium_memzero().

4. **Destruction confirmation record.** After successful zeroing and munmap(), write a record to the chain:
   ```json
   {
     "kind": "voice_audio_destroyed",
     "session_id": "<uuid>",
     "buffer_size_bytes": 320000,
     "sha256_before_destruction": "abc123...",
     "sha256_after_destruction": "<canonical null-hash>",
     "timestamp": "<iso8601>",
     "prev_hash": "<prior record hash>"
   }
   ```
   This record proves (to the chain verifier) that the audio buffer was destroyed. An attacker reviewing the chain sees the NULL hash and can verify that the buffer was zeroed (the NULL hash is a canonical value everyone can compute). The attacker cannot forge this record because it is part of the chain and would require re-signing and re-anchoring the entire chain head in Sigsum.

5. **No auxiliary buffers.** Ensure no copy of the audio is made during the pipeline. Do not write to temporary files. Do not pass to external processes. Do not log the raw waveform. Streaming directly from microphone → VAD → whisper.cpp → destruction, with no intermediate persistence.

---

## §7. Implementation Language and Runtime

**Primary implementation: Rust (calm-witness-voice crate).**

Reason: Rust's memory-safety guarantees (borrow checker, no use-after-free, no buffer overflows) make it much harder to accidentally leak the audio buffer or introduce a dangling-pointer vulnerability. Rust's wrapper around mlock/munmap is straightforward; zeroize crate is audited and widely used. FFI bindings to whisper.cpp are auto-generated via bindgen or hand-written with unsafe blocks clearly marked for review.

**whisper.cpp binding via FFI (C).**

whisper.cpp is C/C++; Rust calls it via a thin C interface:
```rust
extern "C" {
    fn whisper_init(model_path: *const c_char) -> *mut whisper_context;
    fn whisper_full(ctx: *mut whisper_context, params: whisper_full_params,
                    audio: *const f32, n_samples: c_int) -> c_int;
    fn whisper_get_segment_text(ctx: *mut whisper_context, i_segment: c_int) -> *const c_char;
    // ... etc
}
```

The audio pointer passed to whisper_full() is derived from the mlock'd buffer. whisper.cpp reads the buffer but does not assume it persists beyond the function call.

**Python bindings for testing and reference.**

PyO3 bindings expose the Rust crate to Python for development, testing, and reference implementations. The Python interface is:
```python
from calm_witness_voice import TranscribeSession

session = TranscribeSession(model="small.en")
result = session.transcribe_from_microphone(duration_sec=60)
# result.transcript, result.stats, result.destruction_proof
# Audio buffer is destroyed before result is returned to Python.
```

This allows rapid iteration of tests, enrollment ceremony scripts, and integration with the broader Calm Witness pipeline.

---

## §8. Test Corpus and Acceptance Criteria

**Test data collection:**

Record N=20 sessions of varied speaking content with the full pipeline in the loop:
- Calm, slow narrative (~120 wpm, structured thought).
- Technical explanation (code-like syntax and concepts, jargon-heavy).
- Agitated speech (rapid delivery, higher pitch variation, filler-dense).
- Whispered speech (low amplitude, high SNR required).
- Multilingual code-switch (English + one other language, only for v1 after model upgrade).

For each session, record metadata: speaker age, sex, dialect region (if relevant), ambient noise level (dB), microphone model, and ground-truth transcription (human-verified).

**Acceptance tests:**

1. **Determinism.** Run the same audio file through the pipeline 5 times with WHISPER_DETERMINISTIC=1. Assert that the `transcript_words[]` array (word sequence, timing, confidence) is identical across all 5 runs. Accept tolerance: ±1 millisecond on timestamps due to floating-point rounding in timestamp conversion.

2. **Buffer-zeroed confirmation.** After each test run, assert that the `destruction_proof.sha256_after_destruction` matches the canonical NULL hash (SHA-256 of all-zeros: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Parse the chain record and verify it was written atomically (prev_hash chain is unbroken).

3. **Latency on M-series.** Measure end-to-end latency (audio start → output struct available) for the N=20 corpus. Assert: median latency < 2x audio duration on M2 Mac (1 minute of audio → <2 minutes wall-clock). Assert: 95th-percentile latency < 4x on M1 (higher variance on older silicon).

4. **Transcript fidelity (WER vs. ground truth).** For each session, compute word-error-rate (WER = (S+D+I)/N where S=substitutions, D=deletions, I=insertions, N=reference words). Assert: median WER across corpus < 10%. (small.en achieves ~7% on LibriSpeech; our test corpus is less formal, so 10% is reasonable.) Accept failure if WER > 10%: re-train model or request upgrade to small-multilingual (v1).

5. **Stats computation correctness.** For a subset (N=5) of the test sessions, hand-verify the stats:
   - avg_phrase_len_words: compute from transcript_words[] by identifying phrase breaks (pauses > 0.5s); average the word counts in each phrase. Assert computed value matches stats.avg_phrase_len_words.
   - mean_pause_s, stddev_pause_s: extract inter-word gaps (start_s[i+1] - end_s[i]); compute mean and std deviation; assert match.
   - disfluency_rate: count words matching regex (/um|uh|like|well|you know|...); divide by total word count; assert match.

6. **No raw audio in chain.** Parse all records written to `user_state.jsonl` during the test. Assert: no record contains a field matching `raw_audio`, `audio_data`, `wav_base64`, or similar. Assert: the `voice_audio_destroyed` record is present for each voice sample.

---

## §9. Lexical Fingerprint Variables: What the Transcript Captures

For each enrolled voice sample, compute and commit:

- **Word-level fingerprint:**
  - `token_sequence`: ordered list of words from transcript_words[].word.
  - `vocabulary_size`: count of unique words.
  - `vocab_frequency_distribution`: histogram of (word → count). Ordered by count descending.

- **Phrase-level fingerprint:**
  - `phrase_count`: number of pauses > 0.5s (assumed phrase breaks).
  - `avg_phrase_len_words`: mean word count per phrase.
  - `phrase_len_distribution`: histogram of phrase lengths.
  - `phrase_len_stddev`: standard deviation of phrase lengths.

- **Timing-derived fingerprint:**
  - `inter_word_pauses`: array of (start_s[i+1] - end_s[i]) for all adjacent words. Exclude pauses > 2 seconds (assumed turn-taking, not natural speech).
  - `mean_pause_s`: mean of inter_word_pauses.
  - `median_pause_s`: median of inter_word_pauses.
  - `stddev_pause_s`: standard deviation of inter_word_pauses.
  - `pause_distribution_percentiles`: 25th, 50th, 75th, 90th percentiles of inter_word_pauses. Captures the shape of the pause distribution (whether the principal speaks in bursts or at steady cadence).

- **Disfluency fingerprint:**
  - `filler_words`: set of words matching /um|uh|like|well|you know|kind of|sort of|basically|literally|.../ (principal-specific list).
  - `disfluency_count`: count of filler words in transcript.
  - `disfluency_rate`: disfluency_count / total_word_count.
  - `filler_position_distribution`: histogram of (word_index_of_filler % 10) — does the principal cluster fillers at phrase starts or throughout?

- **Utterance-level fingerprint:**
  - `total_word_count`: N in the transcript.
  - `utterance_duration_s`: end_s[N-1] (or a rounded variant to nearest 0.5s, to avoid leaking too much timing precision).
  - `speaking_rate_words_per_sec`: total_word_count / utterance_duration_s.

---

## §10. Output Record Format

Each `voice_sample` record written to the chain:

```json
{
  "kind": "voice_sample",
  "prev_hash": "<sha256 of prior record>",
  "record_hash": "<sha256 of this record's payload>",
  "session_id": "<uuidv4>",
  "sample_id": "<uuidv4>",
  "state_label": "calm",
  "timestamp": "<iso8601>",
  "transcript": {
    "words": [
      { "word": "hello", "start_s": 0.12, "end_s": 0.35, "confidence": 0.98 },
      { "word": "world", "start_s": 0.45, "end_s": 0.62, "confidence": 0.96 }
    ],
    "word_count": 2
  },
  "stats": {
    "avg_phrase_len_words": 1.5,
    "mean_pause_s": 0.08,
    "stddev_pause_s": 0.02,
    "disfluency_rate": 0.0,
    "speaking_rate_wps": 2.5
  },
  "model_version": "whisper-small.en-v3",
  "model_hash": "<sha256 of model binary>",
  "destruction_proof": "<canonical null-hash from step 6>",
  "no_raw_audio_field": true
}
```

**Critical invariant:** There is no `raw_audio`, `audio_data`, `wav`, `opus`, `mp3`, `spectral_features`, `speaker_embedding`, or any field containing acoustic-domain information beyond text and timing. The `no_raw_audio_field` boolean is a deliberate reminder to code reviewers and auditors.

---

## §11. Threat Model Deltas (vs. "No Voice at All")

**Pro (added capability):**

The lexical fingerprint (second modality) adds behavioral-biometric strength at a conceptual level (Everest 38: multimodal fusion). A principal's handwriting (kinematic motor signature) + voice transcript (lexical signature) together create a higher-entropy baseline than either alone. An attacker who compromises one modality (e.g., forges handwriting strokes via a stylus rig) still must match the lexical signature under time pressure — much harder than matching a voiceprint, which is learnable from movies, deepfake audio, or voice-clone software.

**Con (added attack surface):**

Someone with real-time access to the audio buffer (during inference, before destruction) could capture the raw audio and re-run their own ASR system to extract voiceprint features. This is explicitly scoped as a live-compromise attack (Everest 21) and is outside the threat model of Everest 13. The protocol assumes an attacker with read access to persistent state (the vault, the chain), not real-time kernel-level access during a running process.

**Mitigation for the con:**

The enrollment ceremony (Everest 11) requires an air-gap: the capture host has no network connectivity. An attacker who wishes to exfiltrate the audio buffer in real-time must have physical access to the device and the ability to run malware during the ceremony. The presence of a witness (Everest 11 §2) provides deterrence. The witness-signed attestation (Everest 11 §9) provides a post-facto audit trail if tampering is suspected.

---

## §12. Open Questions Deferred to Future Everests

1. **Multilingual support.** v0 ships small.en only. v1 will add whisper-small-multilingual, which supports ~99 languages but has higher WER on each individual language and slower inference. Multilingual threshold: when N ≥ 10% of enrolled principals request non-English support.

2. **Code-switching.** Principals who speak multiple languages within a single utterance (e.g., code-switching from English to Spanish within a sentence) are not fully supported in v0. whisper-small-multilingual can output code-switched transcripts, but the lexical-fingerprint stats (phrase-length, disfluency-rate) may be confounded by language shifts. v1 will add per-language stats.

3. **Speech-impaired principals.** v0 supports any principal who chooses to enroll with voice. Principals with speech disabilities (dysarthria, apraxia, stuttering, deafness) have a fully supported alternate modality: handwriting-only enrollment (Everest 11 permits this, requiring N ≥ 7 handwriting samples per state). If a speech-disabled principal chooses voice for multimodal fusion, the expected WER will be higher; re-enrollment consent and clarity-of-expectation are required.

4. **Accent and dialects.** whisper-small.en is trained on diverse accents (LibriSpeech, Common Voice) but has known performance gaps on non-standard and low-resource dialects. If a principal's dialect causes WER > 15%, they can request re-enrollment with a higher-WER tolerance or switch to handwriting-only. v1 may include accent-specific models.

5. **Adversarial robustness.** whisper.cpp is not robust to adversarial audio (e.g., imperceptibly perturbed audio designed to trigger misrecognition). This is an open problem in ASR. v0 assumes a threat model where the attacker cannot manipulate the microphone input in real-time (the enrollment ceremony is witnessed, per Everest 11). If adversarial robustness becomes a concern, defenses would be added in v2 (e.g., ensemble transcription across models, confidence thresholding).

---

## §13. Acceptance Test (Final)

This document + the calm-witness-voice crate (Rust + whisper.cpp FFI) + PyO3 bindings constitute the specification. Acceptance:

1. A reasonably-trained third party with this document, a laptop (M1/M2/Intel x86-64), and the calm-witness-voice source code can build the binary: `cargo build --release`.

2. That binary, when invoked with `calm-witness-voice transcribe --model small.en --input sample.wav --destroy-after`, produces a JSON output struct with the fields listed in §10 and writes a `voice_audio_destroyed` record to the chain.

3. The test corpus (§8) is run end-to-end; all acceptance tests pass (determinism, buffer-zeroed, latency, WER, stats, no raw audio).

4. The chain is verified with `calm-witness verify-chain`, confirming prev_hash consistency and no raw audio fields.

---

— Calm, 2026-05-20
