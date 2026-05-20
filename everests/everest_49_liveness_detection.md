# Everest 49 — Liveness Detection at Capture Time

*Phase IV — Biometric Distance Machinery. Prereq: Everest 12, 13.*

## The Threat Model

Liveness detection exists to answer a single critical question: *Is the input stream being captured right now a live human sample, or a replay of a previously recorded one?*

Three attack vectors motivate this Everest:

**Stroke Replay.** An adversary who has observed or intercepted a previous session's stylus event stream (coordinates, pressure, timing) can attempt to re-inject it via a hardware emulator or app-level spoofing. The replayed stream will be byte-identical to the original — same strokes, same sequence, same pressure curve. Without liveness detection, the biometric matcher would accept it as a valid sample.

**Transcript Paste.** In our transcript-only voice pipeline, an adversary holding a copy of the principal's previous transcript can attempt to reproduce it: either by having the principal read the same text aloud on a second occasion, or by synthesizing the principal's voice via TTS and playing it during capture. The captured transcript will match the stored one exactly. Liveness detection must catch the unnatural timing or hesitation patterns that betray non-live input.

**Pre-recorded Audio.** While our architecture does not store raw voice files (transcript-only reduces attack surface), an adversary in physical proximity during capture could play back a synthesized or previously recorded voice sample through the principal's microphone. The transcript-only pipeline defends by not being fooled by audio characteristics — but if the principal is forced to read a script, transcript-alone is insufficient.

All three attacks exploit the same vulnerability: the absence of the micro-entropy that characterizes live human input.

## The Principle: Micro-Entropy

Live human input — whether writing or speaking — is never perfectly repeatable. Every time a person performs the same task, tiny variations emerge:

- Finger tremor and micro-corrections in pen pressure
- Variable hesitation pauses before words
- Slight jitter in hand velocity
- Organic interjections ("uh," "um") and self-corrections in speech
- Realistic latency between stimulus and response

These variations are not noise to be suppressed; they are *the signal of liveness*. A replayed stroke stream or synthesized transcript lacks them — either because it was perfectly recorded in a previous session (and replay preserves that perfection) or because it was artificially generated (and no generator can simultaneously replicate all high-frequency entropy characteristics).

Liveness detection is thus the inverse of biometric matching: instead of asking "how close is this sample to the template?", we ask "how much random variation does this sample contain in ways that are hard to fake?"

## Handwriting Liveness

The capture pipeline for handwriting (seeded in Everest 12) has access to raw device events from Apple Pencil Pro or Wacom Intuos Pro. These events include:

- Stylus position (x, y) at sub-millisecond resolution
- Pen-tip pressure (0–4095 uint for Apple; similar for Wacom)
- Tilt angle (if available)
- Contact state (pen-down, pen-up)
- High-precision timestamp (sub-100 microsecond resolution on modern hardware)

Four statistical signatures of liveness emerge:

**Pen-Tip Pressure Microvariation.** Live writing produces high-frequency jitter in the pressure signal — tremor from the hand's involuntary micro-movements and conscious pressure adjustments during stroke execution. This jitter is typically 50–200 Hz. A replayed stream, captured at 100–200 Hz sample rate, will have quantized or smoothed pressure values; the jitter is absent or flattened. Detector: compute the power spectral density in the 50–200 Hz band; live samples have significantly higher power than replayed ones.

**Inter-Stroke Pause Distribution.** Between strokes, there are pauses (pen-up intervals). Live writing has variable pauses: short pauses before familiar letters, longer pauses before difficult strokes or while planning. The distribution of pause durations follows a Lognormal shape (heavy right tail). A replayed stream may have *constant* pauses (if the recording captured uniform breaks) or a flat distribution (if the adversary is naively re-playing without temporal structure). Detector: fit a Lognormal to the observed pause distribution; compute KL-divergence from the theoretical Lognormal; live samples have low divergence.

**Hand-Eye-Pen Coupling.** There is a measurable correlation between pen velocity (stroke speed) and the length of the *subsequent* pause. Fast strokes are often followed by short pauses; slow, deliberate strokes by longer pauses (the hand is planning the next move). This correlation is a hallmark of the cognitive process of writing. A replayed stream, if it preserves individual stroke timings but was re-ordered or edited, may break this correlation. Detector: compute cross-correlation between velocity profile and next-pause duration; live samples show significant correlation.

**Surface Contact Noise.** The physical interaction of the stylus with the screen (or tablet surface) produces micro-contact transients — brief, high-frequency accelerations in the pressure signal as the pen makes and breaks contact. These are present in live capture but absent in purely simulated or replayed streams. Detector: apply a high-pass filter (5–10 kHz) and measure energy; live samples have detectable contact-noise energy.

## Voice Liveness (Transcript-Only)

Within the transcript-only architecture, we do not store voice; we store only the time-aligned transcript of what was spoken. Yet we can still detect liveness using the *timing* of the transcript itself.

**Word-Timing Entropy.** Each word in the transcript has a start time and end time (derived during speech-to-text alignment). The duration of each word varies; "cat" might take 0.3 seconds while "antidisestablishmentarianism" takes 2.5 seconds. Live speech shows natural variation in word durations around the mean, reflecting how naturally a person articulates. TTS-synthesized speech or read-aloud scripts often have lower variance — TTS engines produce consistent durations; readers follow a script at near-constant pace. Detector: compute the coefficient of variation (std / mean) of word durations; live speech has higher variation.

**Hesitation Patterns.** Live speakers naturally insert hesitations: "um," "uh," "like," and filled pauses. They also make self-corrections: false starts and backtracking. These are captured in the transcript as special tokens or noted in the timing (gaps with no recognized speech). Replayed or TTS-generated transcripts have few or no such patterns. Detector: count hesitation tokens and self-correction events per minute; live samples have higher counts.

**Response-to-Prompt Latency.** Between the moment a prompt is shown (or read aloud) and the moment the principal begins speaking, there is a measurable latency. Live respondents typically have latencies of 0.5–2.0 seconds as they comprehend the prompt and formulate a response. A pre-recorded or replayed transcript (e.g., someone playing back a synthesized audio file) has zero latency or misaligned latency. Detector: measure the time between prompt termination and first-word onset; live samples have latencies in the expected range.

However, we acknowledge that voice liveness in a transcript-only pipeline is fundamentally weaker than liveness detection on raw voice. A determined adversary with a live accomplice (the principal forced to read a script) can defeat all four detectors. This is by design: the *composition* of defenses is load-bearing, not any single layer. Handwriting liveness is strong; voice liveness is a secondary check; and ceremony witness (the human attestor in Everest 18) is the ultimate backstop.

## Capture-Time Enforcement

The liveness pipeline runs *synchronously at the moment of capture*. This is non-negotiable:

1. A user initiates a capture session (handwriting or voice).
2. Raw device events stream into the `calm-witness-capture` daemon.
3. The daemon computes a fixed feature vector (~32 floats per sample) using the `liveness_features` module.
4. A small neural-net classifier (1–2 MLP layers, ~50 KB) ingests this vector and outputs a scalar: liveness probability in [0, 1].
5. If probability < THRESHOLD (default 0.85), the sample is **rejected immediately**. The user is prompted to re-capture.
6. If probability >= THRESHOLD, the sample is accepted and added to `user_state.jsonl`.
7. Rejected samples are logged as kind `capture.liveness_rejected` with metadata: timestamp, computed features, classifier output, reason for rejection.

No rejected sample is ever added to the biometric store. This prevents an adversary who successfully crafts a marginal-liveness input from contaminating the template.

The threshold default of 0.85 is conservatively high, favoring false-reject over false-accept. A user who fails liveness on a legitimate sample simply re-captures; the cost is minor friction. An adversary who succeeds in injecting a replay is a cryptographic failure. This asymmetry justifies the high bar.

## Per-Principal Threshold Calibration

During enrollment (Everest 14, handwriting subsection), each principal provides 10–20 live samples under supervision. The liveness classifier is applied to each; the distribution of outputs is recorded. The enrollment process then sets THRESHOLD for that principal such that:

- 95% of the principal's own samples are accepted (false-reject rate ≤ 5%).
- The principal's samples occupy a range [T_min, 1.0], and THRESHOLD is set to T_min – δ, where δ is a small margin (e.g., 0.02).

This per-principal calibration accounts for natural variation: some individuals write with high-frequency tremor (high liveness scores even for live samples); others write with steadier hands (lower liveness scores for live samples). A universal threshold would reject too many live samples from the latter group.

The per-principal THRESHOLD is stored in `principal_metadata.json` and is non-modifiable after enrollment (it is signed cryptographically as part of Everest 30, the certification layer).

## Liveness Feature Vector

The `liveness_features` module computes a fixed 32-dimensional vector per sample:

**For handwriting (16 features):**
- Pressure microvariation power (5-point summary: min, Q1, median, Q3, max)
- Inter-stroke pause distribution parameters (Lognormal μ, σ, KS-divergence)
- Velocity-pause correlation coefficient
- Contact-noise energy (high-pass filtered)

**For voice (16 features):**
- Word-duration coefficient of variation
- Hesitation-token frequency (per minute)
- Response-latency quantiles (5, 25, 50, 75, 95)
- Transcript length and entropy (Shannon entropy of word-frequency distribution)

The vector is computed in real time by `calm-witness-capture` and is fed to the classifier. Latency must be <50 ms; on modern hardware (2024+), inference on a ~50 KB MLP is typically 5–15 ms.

## Adversarial Robustness

**Naive Replay.** An adversary who captures and replays a stroke stream without modification will fail liveness detection because the replayed stream lacks the source's original micro-entropy. The pressure jitter, pause distribution, and contact noise are all absent or flattened in the recording medium.

**Informed Adversary.** If the adversary knows the liveness features (e.g., from reverse-engineering the app or leaked documentation), they can attempt to synthetically add noise to a replayed stream. However, the four features are *interdependent*: adding random pressure jitter does not automatically produce the correct velocity-pause correlation; synthetic contact-noise has different frequency characteristics than real contact-noise. An ensemble detector that evaluates all four features simultaneously is hard to forge. Continuous retraining on observed attacks (Everest 48, anomaly detection) raises the bar further.

**Imitator Attack.** An accomplice with knowledge of the principal's biometric signature could attempt to *live-write* strokes that match the principal's handwriting. This is biomimicry rather than replay. Liveness detection does not defend against this directly: the accomplice's strokes are genuinely live and will pass liveness checks. However, the downstream biometric distance matcher (Everest 36) will reject the imitator's strokes because they do not match the principal's biometric template. The liveness layer ensures *liveness*; the distance layer ensures *identity*.

## Composition with Other Everests

Liveness detection is one layer in a multi-layered authentication stack:

- **Everest 12 (Handwriting Hardware).** Provides the raw device event stream and calibration of hardware entropy sources (pen pressure, contact timing).
- **Everest 13 (Voice Transcription Pipeline).** Provides transcript time-alignment data and word-duration statistics.
- **Everest 36 (Handwriting Biometric Distance).** Downstream consumer. Only receives liveness-approved samples as input.
- **Everest 48 (Anomaly Detection).** Monitors accept/reject patterns at scale; triggers retraining if adversarial patterns emerge.
- **Everest 50 (Sample Uniqueness).** Orthogonal defense: prevents replay of the *same* sample across sessions, even if that sample initially passed liveness.
- **Everest 18 (Ceremony Witness).** Human attestor who observes enrollment and challenge sessions; ultimate arbiter in case of ambiguity.

## Implementation Constraints

**Model Size.** The liveness classifier is a small neural network: input layer (32), hidden layer (64 units, ReLU), output layer (1, sigmoid). Total parameters ≈ 2200; serialized size ≈ 50 KB. This fits in the app bundle without bloat.

**Inference Latency.** On a 2024-era ARM processor (iPhone 15, iPad Pro), inference takes 5–15 ms. The total capture-time latency budget is 50 ms; liveness inference occupies only 10–30% of this.

**Training Data.** Minimum 100 live samples + 100 replayed samples per device type (Apple Pencil Pro, Wacom Intuos Pro). Cross-device transferability is tested; a classifier trained on iPad samples should generalize reasonably to Wacom tablets (transfer learning is acceptable, but device-specific tuning is preferred).

**Adversarial Dataset.** In addition to naive replays, the training set includes adversarial examples: synthetically generated stroke streams designed to fool simple pressure-variance detectors. This hardens the classifier against known evasion techniques.

## Failure Modes and Mitigation

**False Rejection of Legitimate Samples.** A user whose genuine handwriting has low pressure variance (steady, controlled hand) might be rejected by an overly aggressive liveness detector. Mitigation: per-principal threshold calibration (described above). If the principal is repeatedly rejected, the threshold is adjusted upward during a recalibration session.

**Liveness-Classifier Poisoning.** If an attacker gains write access to the model file, they could replace it with a permissive fake. Mitigation: the model is signed cryptographically (Everest 30, certification layer) and verified at load time. Tampering is detected and the app halts.

**Concept Drift.** As the population of principals grows, new writing and speaking styles may emerge that the training set did not cover. A cohort of principals with unusual handwriting characteristics might experience higher false-reject rates than the initial cohort. Mitigation: continuous monitoring via Everest 48; automated retraining when false-reject rates exceed a threshold in a cohort.

## Test Corpus and Acceptance Criteria

- Minimum 100 live handwriting samples per device.
- Minimum 100 replayed handwriting samples (same strokes, captured and replayed without modification).
- Minimum 100 live voice transcripts per language.
- Minimum 100 synthesized or read-aloud transcripts (same content, different liveness characteristics).
- Cross-device transferability: classifier trained on Apple Pencil must achieve ≥90% accuracy on Wacom test set (or vice versa) without retraining.
- Adversarial robustness: classifier trained on naive replays must achieve ≥85% accuracy on adversarial test set (synthetically crafted strokes designed to fool simple detectors).
- Per-principal calibration: 95% of enrolled principals must pass liveness on their own live samples during recalibration tests.

## Summary

Liveness detection at capture time is a hard real-time constraint in the calm-witness authentication pipeline. It leverages the micro-entropy of live human input — pressure jitter, timing variation, hesitation patterns — to reject replayed or synthesized samples before they contaminate the biometric store. The liveness layer is not the sole defense against forgery; it is composed with biometric distance matching (Everest 36), sample uniqueness checking (Everest 50), and human witness testimony (Everest 18). Together, these layers form a defense-in-depth posture that raises the cost of successful attack from "simple replay" to "breaking multiple independent mechanisms."

— Calm, 2026-05-20