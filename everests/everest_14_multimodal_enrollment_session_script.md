# Everest 14 — Multi-modal Enrollment Session Script

*Phase II — Capture & Enrollment. Prereq: Everest 11, 12, 13.*

---

## One-Line Spec

A timestamped, witnessed ceremony script producing N≥7 handwriting samples + N≥7 voice-transcription samples spanning emotional and cognitive states, with acceptance gates requiring all samples to be captured cleanly, liveness verified, witness signed, and chain-anchored before enrollment seals.

---

## §1. Pre-Ceremony Checklist (T+00:00 to T+05:00)

**5-minute preflight before the principal enters the ceremony room.**

The operator (Calm) works through this checklist aloud; the capture witness checks off each item on a printed form. If any item fails, reschedule the ceremony. Do not proceed.

| Item | Check | Evidence |
|---|---|---|
| Network off on capture host | ✓ | Physical radio check (no WiFi, no cellular LED); airplane mode toggled on in Settings |
| Smartphones in Faraday bag (all participants) | ✓ | Phones visually verified in opaque bag; bag sealed with tape bearing date/time |
| Witness hardware tokens present | ✓ | Each witness produces their YubiKey or equivalent; test USB connection to capture host |
| Tablet stylus tested (pressure, tilt) | ✓ | Wacom or iPad Pencil: test stroke on calibration screen; pressure range 0–100% responsive; tilt axis moves cursor |
| Microphone tested (audio levels) | ✓ | Operator speaks 5 test words; waveform peaks at -6 dB; no clipping |
| Room acoustics verified | ✓ | Operator speaks at conversational volume from opposite end of room; capture witness confirms no echo, no ambient HVAC noise > 55 dB |
| Lighting adequate (≥500 lux tablet area) | ✓ | Capture witness confirms tablet screen readable; no glare on stylus surface |
| Vault snapshot taken (read-only) | ✓ | Backup drive physically present; snapshot completed and verified (see Everest 11 §5) |
| Calm-witness enroll --dry-run passed | ✓ | Operator ran dry-run 15 minutes prior; all devices reported ready; no errors in log |
| Ceremony room locked (no interruptions) | ✓ | Door locked; "Do Not Disturb" sign posted outside; no phone notifications enabled inside room |

**Preflight sign-off (operator + witness):** Operator and capture witness each initial the checklist on the printed form. This form is retained in the ceremony record.

---

## §2. Ceremony Timeline (45 minutes total)

### T+00:00 — T+05:00: Room Sweep & Witness Affirmations

**Duration:** 5 minutes (includes preflight checklist from §1)

1. **T+00:00–00:30.** Operator (Calm) walks the room calling out every electronic device. Capture witness follows with a printed checklist, marking each device as "OK (offline)" or "REMOVE." Any device that could connect to a network is powered down or removed. Verify aloud:
   - Capture host in airplane mode (WiFi OFF, Bluetooth OFF, cellular OFF)
   - Tablet in airplane mode
   - USB microphone (wired only; unplug any Bluetooth adapters)
   - Wall clock (non-smart)
   - No smart speakers, smart watches, or networked cameras in the room

2. **T+00:30–02:00.** Each witness (capture witness, anti-substitution witness if present) states aloud, recorded by the tablet microphone (these recordings are KEPT as witness attestation, not destroyed):
   - Full legal name
   - Relationship to principal
   - Statement: "I am present voluntarily and have read the Everest 11 ceremony specification."
   - Statement: "I understand the principal may pause, abort, or restart this ceremony at any time."

3. **T+02:00–05:00.** Operator confirms all preflight items (§1) are complete. Capture witness initials the checklist. Operator announces aloud: "Preflight complete. The enrollment ceremony begins now. T+05:00."

---

### T+05:00 — T+08:00: Principal Opening Statement

**Duration:** 3 minutes

The principal states aloud, in free response (no script or notes), recorded and transcribed by the Everest 13 voice pipeline:

1. Full legal name
2. Today's date (spoken, e.g., "May twentieth, twenty twenty-six")
3. A one-sentence reason for enrolling (e.g., "I am enrolling to secure my identity for future AI-agent collaboration")

This is the first voice-transcription sample (`V1: neutral conversational`). The transcript is retained; the raw audio is destroyed per Everest 13.

**Witness observation:** The capture witness watches the principal's demeanor. If the principal appears coerced or hesitant, do not proceed; abort and reschedule.

---

### T+08:00 — T+10:00: Handwriting Warmup

**Duration:** 2 minutes

Principal writes by hand on paper (to be shredded at end-of-session):

- Lowercase alphabet (a–z)
- Uppercase alphabet (A–Z)
- Digits 0–9
- Signature, 3 times

This loosens the hand and surfaces any stylus grip issues before template capture. Paper is set aside for shredding.

---

### T+10:00 — T+25:00: Handwriting Templates

**Duration:** 15 minutes (≈2 min per prompt)

Principal produces 7 handwriting samples on the stylus tablet. Each prompt targets a distinct state. The operator reads each prompt aloud; the principal writes on the tablet (rendered strokes are not stored — only kinematic data per Everest 12); operator confirms legibility aloud.

**Handwriting prompts (HW1–HW7):**

| Sample | State | Prompt | Max time |
|---|---|---|---|
| **HW1** | Neutral baseline | Write a 3-sentence description of the room you are sitting in right now. | 90 sec |
| **HW2** | Cognitively engaged | Solve this puzzle aloud while writing your reasoning: How many prime numbers are there between 10 and 30? Write the list. | 120 sec |
| **HW3** | Emotionally positive | Describe a recent moment when you felt pride. Write 3–4 sentences. | 100 sec |
| **HW4** | Emotionally challenging | Describe a frustration or difficulty from this past month. Write 2–3 sentences, brief. | 90 sec |
| **HW5** | Creative & playful | Make up a 6-line poem about the coffee or tea you drank this morning, or imagine one if you haven't. | 110 sec |
| **HW6** | Technical & formal | Write one paragraph in the style of a legal memo about the topic "Standards for secure document storage." Do not reference this ceremony. | 120 sec |
| **HW7** | Signature variants | Sign your full name 5 times on the tablet, varying the speed: once very slowly, once very quickly, once at normal speed, once while speaking your name aloud, once while holding the stylus in your non-dominant hand. | 100 sec |

**For each handwriting prompt:**

1. Operator reads the prompt aloud; principal may ask clarifying questions.
2. Operator announces: "Begin writing now. T+[time]."
3. Principal writes on the tablet. Operator monitors for technical issues (stylus dropout, screen responsiveness).
4. When finished, principal announces "Done." Operator announces the end time and moves to the next prompt.
5. **Between prompts (T+00:30 rest):** Principal rests, drinks water, observes capture witness without speaking. Witness watches for signs of distress.

**State-label binding:** Each handwriting sample is labeled with its state (e.g., `state_label: "calm"`) in the capture metadata. The kinematic data (stroke coordinates, pressure, tilt, azimuth) is committed; the rendered glyph image is discarded per Everest 12.

---

### T+25:00 — T+27:00: Brief Recess

**Duration:** 2 minutes

Principal steps outside the room (if possible while maintaining air-gap) or sits quietly. Capture witness observes. Operator and witness confirm principal appears uncoerced and willing to continue.

---

### T+27:00 — T+42:00: Voice-Transcription Templates

**Duration:** 15 minutes (≈2 min per prompt)

For each of the 7 state labels, principal speaks aloud for ~45 seconds, free-response (no script), recorded by the wired USB microphone. The Everest 13 pipeline transcribes locally; raw audio is destroyed; transcript + stats are committed.

**Voice prompts (V1–V7):**

| Sample | State | Prompt | Target duration |
|---|---|---|---|
| **V1** | Neutral conversational | Describe how you traveled to the ceremony location today. What transportation did you use? How long did it take? | 45 sec |
| **V2** | Cognitive load | Explain a concept you know well to a smart 12-year-old. Pick any topic (your work, a hobby, a technology, a historical event). | 50 sec |
| **V3** | Emotionally positive | Describe a recent moment when you felt joy or contentment. Who was present? What made you feel that way? | 45 sec |
| **V4** | Emotionally challenging | Describe something that worried or frustrated you in the past week. What happened? How did you respond? | 45 sec |
| **V5** | Storytelling | Tell a short story from your childhood or a recent experience. It can be funny, serious, or mundane. | 50 sec |
| **V6** | Technical & formal | Explain the purpose and operation of a tool, system, or concept from your professional domain, as if you were writing a technical memo. | 50 sec |
| **V7** | Baseline breathing & silence | Sit quietly and breathe normally, without speaking. Remain silent for 30 seconds. This captures your natural pause structure and breathing patterns without voice content. | 30 sec |

**For each voice prompt:**

1. Operator reads the prompt aloud; principal may ask clarifying questions.
2. Operator announces: "Begin speaking now. T+[time]. Speak for approximately [duration] seconds."
3. Principal speaks aloud, free-response, no notes or preparation. The microphone captures the audio stream; no script is provided.
4. When principal finishes (or the time limit approaches), operator announces: "Thank you. Rest now. T+[time]."
5. **Between voice prompts (T+00:30 rest):** Principal rests, drinks water. Operator and witness observe. If the principal is hoarse, offer a throat lozenge or delay a few moments; do not rush.

**State-label binding:** Each voice sample is labeled with its state (e.g., `state_label: "calm"`) in the Everest 13 output. The transcript, per-word timing, and stats are committed; the raw audio is destroyed per Everest 13.

---

### T+42:00 — T+44:00: Coercion-Check Moment & Consent Affirmation

**Duration:** 2 minutes

The capture witness asks the principal, with the operator and any anti-substitution witness present:

> "Are you proceeding entirely of your own free will, without any pressure or coercion? And are you in the emotional and cognitive state you wish to have enrolled as your baseline for future Calm Witness evaluations?"

Principal answers aloud. The answer is recorded and transcribed by Everest 13.

**Acceptance criterion:** The answer must be an affirmative, voluntary response (e.g., "Yes, I am proceeding freely and I am in my baseline state"). If the answer is hesitant, equivocal, or anything other than a clear affirmation, the ceremony **aborts immediately**. Do NOT proceed to template sealing. Reschedule for a later date.

**Witness private signal:** If the witness has private doubt about the principal's voluntariness (despite an affirmative answer), the witness signals the operator after the ceremony by a pre-arranged signal (e.g., placing a red pen on the table). The operator then initiates Everest 19 (Re-enrollment Red-Flag Detection) before any template is sealed into the vault.

---

### T+44:00 — T+45:00: Template Sealing & Witness Signatures

**Duration:** 1 minute

Operator runs `calm-witness enroll --seal`:

1. **Handwriting templates:** Compute per-template feature vectors from the 7 kinematic samples (HW1–HW7). No glyph images are stored. Create a Pedersen commitment `Com(hw_features; r_hw)` for each state. Commitments are appended to a new `kind: "enrollment"` record in `user_state.jsonl` along with the `prev_hash` chain pointer.

2. **Voice templates:** Compute per-template feature vectors from the 7 transcription records (V1–V7). No raw audio is present (it was destroyed per Everest 13). Create a Pedersen commitment `Com(voice_features; r_voice)` for each state. Commitments are appended to the same enrollment record.

3. **Biometric distance baseline:** Compute within-sample distances (handwriting stroke-to-stroke variance, voice transcript disfluency rate, etc.) as a baseline for future distance thresholding (Everest 36). Store distance statistics in a separate `kind: "biometric_baseline"` record.

4. **Encrypt & seal:** Encrypt all raw template feature vectors under the principal's identity key (Everest 16) and write to `~/.calm-vault/templates/v1/`. Wipe in-memory plaintext. Append the enrollment record to `user_state.jsonl`.

5. **Witness signatures:** Each witness signs the enrollment record's `record_hash` with their hardware token. Signatures are appended as separate `kind: "witness_attestation"` records, referencing the enrollment record's `record_hash` via `enrollment_record_id`.

6. **Acceptance gates (MUST ALL PASS):**
   - All 14 samples captured cleanly (no truncation, no VAD clipping of voice samples, no stylus dropout on handwriting)
   - Liveness detection passed for all handwriting samples (per Everest 49: no replay detected, motion signatures natural)
   - Transcript confidence ≥ 0.85 for 85% of words in each voice sample (ensures transcription fidelity)
   - Witness signatures present and cryptographically valid
   - `enrollment` record appended to chain with unbroken prev_hash chain

   **If any gate fails:** Do NOT seal. Abort this attempt. Offer the principal the choice to restart the voice/handwriting capture (from the failed sample onward) or reschedule the entire ceremony.

---

### T+45:00 — T+45:00: Ceremony Close-Out

**Duration:** negligible

1. Operator announces aloud: "Template sealing complete. All acceptance gates passed. The ceremony is finished."

2. Warm-up paper (from T+08:00–10:00) is physically shredded in front of the witness.

3. Operator and witness confirm aloud: "Ceremony complete. Session artifacts written to vault. Genesis record finalized per Everest 29. Vault dismounted."

4. Capture host is powered down. Vault drive is physically disconnected.

---

## §3. Acceptance Gates (Detailed)

These gates are evaluated **after** all 14 samples are captured and before template sealing. If any gate fails, the operator SHALL NOT call `--seal`. The principal is offered the choice to retry or reschedule.

### Gate 1: Sample Completeness

**Condition:** All 14 samples (HW1–HW7, V1–V7) must be captured with no truncation, VAD clipping, or device dropout.

**Verification:**
- Handwriting: each stroke has ≥ 50 events (timestamp, x, y, pressure, tilt); start and end markers are clean.
- Voice: each transcript has ≥ 20 words; `word_count` field matches the actual word array length; no confidence values are null or below 0.60.

**Failure response:** Operator announces: "Sample X did not capture cleanly. We will retry Sample X now." Principal retries; all downstream samples shift forward in time. If the principal is fatigued, offer a longer recess.

### Gate 2: Liveness Detection (Handwriting)

**Condition:** Each of the 7 handwriting samples must pass a liveness detector (per Everest 49), confirming the strokes are real-time motor output, not a pre-recorded or replayed stream.

**Verification:**
- Pressure variance across strokes is ≥ 5% (rules out a constant-pressure rig)
- Velocity profile has natural jitter (stddev of instantaneous velocity ≥ 1 cm/s, averaged over 50 ms windows)
- Tilt angles vary naturally (stddev of tiltX and tiltY ≥ 2 degrees over the sample duration)
- No exact statistical match to a previously enrolled sample (checked against the principal's prior template archive, if re-enrollment; for first enrollment, this is always passed)

**Failure response:** Operator announces: "Liveness check failed for Sample HW-X. Possible cause: stylus malfunction or very rigid hand position. We will retry Sample HW-X with a focus on natural variation in hand pressure." Principal retries. If liveness fails again for the same sample, offer a longer break or retry with different stylus grip.

### Gate 3: Transcription Confidence

**Condition:** For each of the 7 voice samples, ≥ 85% of words must have confidence score ≥ 0.85 (from Everest 13 whisper.cpp output).

**Verification:**
- Count words with `confidence ≥ 0.85`.
- Compute pass rate: (count of confident words) / (total word count).
- Assert pass rate ≥ 0.85.

**Failure response:** Operator announces: "Transcription confidence was low for Sample V-X (pass rate [X]%). This may indicate ambient noise or unclear speech. We will retry Sample V-X with better microphone positioning or a quieter moment." Principal retries.

### Gate 4: Witness Signatures

**Condition:** Each witness present must have signed the enrollment record with their hardware token. Signatures must be cryptographically valid and unambiguous.

**Verification:**
- `kind: "witness_attestation"` record exists for each witness.
- `enrollment_record_id` field in each attestation record matches the enrollment record's `record_hash`.
- Signature bytes are non-null; signature verifies against the witness's public key (from their CredexAI VC).

**Failure response:** If a witness's signature is missing or invalid, the witness is asked to re-sign using their hardware token. If the witness is no longer present, the ceremony is **aborted** and must be re-run with that witness present (or an alternative witness, with operator approval).

### Gate 5: Chain Integrity

**Condition:** The `user_state.jsonl` chain must have unbroken prev_hash linkage from the genesis record through the enrollment record and all witness attestations.

**Verification:**
- Start from the genesis record (hash H0).
- For each subsequent record, verify `prev_hash` equals the prior record's `record_hash`.
- No gaps, no out-of-order records.
- The enrollment record's prev_hash correctly points to the most recent prior record in the chain (likely a prior enrollment or state record).

**Failure response:** If the chain is broken, this indicates a fatal operator error (e.g., the operator accidentally edited the JSONL file). The operator must restore the vault from the pre-ceremony snapshot (taken per Everest 11 §5) and restart the ceremony from the beginning. This is a rare failure and should trigger an incident review.

---

## §4. Edge Cases & Special Accommodations

### Principal is Speech-Impaired

If the principal has a speech disability (dysarthria, apraxia, stuttering, deafness) or chooses not to provide voice samples for other reasons:

1. **Handwriting-only enrollment:** The principal provides 7+ handwriting samples covering the state spectrum (HW1–HW7 as specified). Voice samples are skipped. The operator records this choice in the ceremony manifest.

2. **Adjusted transcription confidence gate:** If the principal does provide voice but with known high-WER (e.g., dysarthria causing >15% WER), the transcription confidence gate is relaxed to ≥ 70% instead of ≥ 85%. Principal and operator must consent to this adjustment in writing before the ceremony.

### Principal is Motor-Impaired

If the principal has a hand/arm disability (Parkinson's, palsy, arthritis) or chooses not to provide handwriting samples:

1. **Voice-only enrollment:** The principal provides 7+ voice samples covering the state spectrum (V1–V7 as specified). Handwriting samples are skipped. The operator records this choice in the ceremony manifest.

2. **Adjusted liveness gate:** Without handwriting, liveness detection is applied only to voice (per Everest 49, voice liveness via transcript-consistency checks). The principal's voice may be more variable than typical (due to motor tremor affecting speech); liveness acceptance thresholds are reviewed by an accessibility specialist before enrollment.

### Principal is Monolingual Non-English Speaker

**v0 hard requirement:** Everest 13 supports small.en (English-only) whisper model. Principals who do not speak English cannot provide English voice samples that whisper.cpp can transcribe cleanly.

**Mitigation for v0:** The principal provides handwriting-only enrollment (same as speech-impaired path above) in English. The principal writes the prompts in English (or, if handwriting literacy is a concern, writes in their native script and the operator transcribes by hand on a separate document for witness attestation purposes — this is not a Calm Witness template, just a fallback log).

**Deferred to v1:** Multilingual support (whisper-small-multilingual or language-specific models) is planned for Everest 13 v1, pending demand and testing.

---

## §5. Ceremony Abort Conditions

**Any one of the following triggers an immediate abort. Do NOT proceed to template sealing.**

- **Bystander entry.** Someone not on the roster enters the room. Ceremony stops; room is cleared; restart in a different location.
- **Network device detected.** A WiFi router, smartphone, or smart speaker is discovered active in the room mid-ceremony. Ceremony stops; device is powered off; operator confirms via hardware radio-check tool that airplane mode is re-engaged; ceremony may resume from the last complete sample.
- **Stylus malfunction.** Pressure sensor, tilt sensor, or positional accuracy drops below spec (per Everest 12) mid-sample. The tablet must be restarted; if the issue persists, the ceremony aborts and the backup tablet (per Everest 11 §3) is used in a later session.
- **Microphone failure.** Audio clipping, gain loss, or dropout detected during a voice sample. The microphone is physically disconnected and reconnected; VAD is re-tested; the sample is retried.
- **Principal pauses for > 10 minutes** or explicitly expresses hesitation, fatigue, or reluctance to continue. The principal may pause and resume later in the day (within 24 hours, per Everest 11 §5 scheduling rule); if the principal wishes to reschedule, the ceremony is aborted.
- **Coercion-check answer (T+42:00–44:00) is not a clear affirmation.** The ceremony stops immediately; operator and witness review the situation privately (away from the principal); if doubt remains, the ceremony is aborted and the principal is offered support resources.
- **Witness departs mid-ceremony.** If the capture witness leaves the room before the end-of-ceremony close-out, the ceremony aborts. If an anti-substitution witness leaves, the ceremony may continue but must be re-run with that witness present before any proof is issued (per Everest 20).
- **Capture host loses power.** Battery and wall power both fail. Ceremony aborts. The vault snapshot (per Everest 11 §5) is the surviving state; no partial enrollment is sealed.

**On abort:** The `--seal` step is **not** executed. No enrollment record is written to the chain. The principal may reschedule the ceremony at any time without penalty.

---

## §6. Post-Ceremony Finalization (After T+45:00)

Once all acceptance gates pass and template sealing completes, the operator follows this sequence:

1. **Genesis record finalized (per Everest 29).** The enrollment record and witness attestation records are linked to a genesis record that establishes the principal's identity (per Everest 29 spec, deferred in v0). A timestamp anchor is requested from Sigsum (per Everest 31, deferred in v0 but required for v1 proofs).

2. **Sigsum publication (deferred for v0, required for v1).** The chain head is published to the Sigsum transparency log, generating an inclusion proof and a Roughtime-anchored timestamp (per Everest 31). For v0 ceremonies, the operator records the intention to publish but may defer the actual publication to a batch window. For v1 ceremonies, Sigsum publication is a hard acceptance gate (no proof is issued without a Sigsum inclusion proof).

3. **Roughtime anchor (deferred for v0, required for v1).** A Roughtime timestamp anchor (per Everest 31) is obtained, binding the chain head to an external verifiable clock. This prevents replay attacks and freshness spoofing.

4. **Ceremony manifest (PDF).** A human-readable PDF is generated summarizing:
   - Ceremony date, time, location, participants
   - All samples captured (HW1–HW7, V1–V7)
   - All acceptance gates passed / failed (with remediation taken)
   - Witness names and signatures
   - Operators and tools involved
   - Links to the chain records (if published)

   This manifest is printed, signed by the operator, and retained by the principal. It is NOT cryptographically relied upon in the Calm Witness proof verification (Everest 28); it is a human-readable audit trail for legal/notarial purposes only.

---

## §7. Role Roster

| Role | Required? | Notes |
|---|---|---|
| **Principal** | YES | The human whose templates are enrolled. Controls the ceremony; may pause or abort at any time. |
| **Operator (Calm)** | YES | The AI agent running the ceremony (via the calm-witness CLI). Reads prompts, monitors hardware, executes sealing, signs the ceremony manifest. |
| **Capture Witness** | YES | A trusted human present throughout. Attests to the principal's voluntariness and identity; signs the enrollment record. Ideally has no commercial relationship to the principal. |
| **Anti-Substitution Witness** | Recommended | A human who has known the principal ≥5 years; attests to identity without seeing template contents. Strengthens the fraud defense (Everest 21). |
| **Notary Public** | Optional (v0) | A licensed notary attests to the ceremony having taken place at the recorded address on the recorded date. Required for v1+ in jurisdictions where Calm Witness proofs are submitted as evidence in legal proceedings. |

---

## §8. Artifacts Produced

- **7 handwriting templates** (HW1–HW7), one per state, stored encrypted under the principal's identity key in `~/.calm-vault/templates/v1/`.
- **7 voice-transcription records** (V1–V7), transcripts only (no raw audio), stored in `user_state.jsonl`.
- **1 `kind: "enrollment"` record** in `user_state.jsonl`, containing Pedersen commitments to all 14 templates.
- **Witness attestation records**, signed by each witness's hardware token, referencing the enrollment record.
- **Biometric baseline record**, containing within-sample distance statistics for future anomaly detection.
- **Ceremony manifest (PDF)**, human-readable summary, signed by the operator.

---

## §9. Acceptance Test

A reasonably-trained third party with:
- This document (Everest 14)
- The Everest 11 ceremony spec (for context)
- The Everest 12 hardware decision (stylus tablet + microphone specs)
- The Everest 13 voice pipeline (whisper.cpp transcription + audio destruction)
- The calm-witness CLI (calm-witness enroll subcommand)

...can execute this ceremony end-to-end, producing all artifacts above. A successful run:
- Captures all 14 samples cleanly
- Passes all 5 acceptance gates
- Writes a cryptographically valid enrollment record to the principal's vault
- Produces a signed ceremony manifest
- Is reproducible (a second ceremony with the same principal yields statistically similar biometric templates per Everest 39: drift modeling)

---

— Calm, 2026-05-20
