# Everest 11 — Enrollment Ceremony Spec

*Phase II — Capture & Enrollment. Prereq: Everest 1, Everest 10.*

If enrollment is compromised, every later Calm Witness proof is theatre. This summit specifies the one-time, physical, witnessed ceremony that produces the principal's enrolled handwriting and voice-transcription templates. The ceremony is the **trust origin** of the entire primitive; everything downstream — biometric distance, predicate evaluation, disclosure — rides on the unfalsifiability of the templates produced here.

## §0. One-line spec

> A reproducible, scriptable, air-gapped, witness-signed session in which the principal produces a calibrated set of handwriting and voice-transcription samples sufficient to span their behavioral baseline, terminating with sealed templates committed into the principal's vault and a witness-signed Pedersen commitment published to the chain.

## §1. Operating principles (non-negotiable)

1. **Air-gap.** No network-connected device in the room except the capture device, and that device must be in airplane mode with all radios off before the ceremony begins. Verified physically and logged.
2. **No spectators.** Only the principal, the operator (if separate), and the named human witnesses are present. No cameras, no microphones outside the ceremony rig, no smart speakers.
3. **Principal-driven.** The principal can pause, abort, or restart at any point, for any reason, without explanation. An abort is not a failure; it is the protocol working correctly.
4. **No coercion screening from outside.** The witnesses' duty is to attest that the principal appeared uncoerced *at the time of the ceremony*. They are not deputised to evaluate state retroactively.
5. **Reproducible.** A reasonably-trained third party with this document and the capture rig must be able to run the ceremony without further instruction.
6. **No raw audio persisted.** Voice samples are transcribed locally and the raw audio is destroyed at end-of-session. (Everest 13.)
7. **Re-enrollment is normal.** This ceremony will be run again — every N months, on biometric drift detection, or on principal request (Everest 18). The first run is not "the" enrollment; it is the first enrollment.

## §2. Roster

| Role | Required | Notes |
|---|---|---|
| **Principal** | yes | The human whose templates are being enrolled. |
| **Operator (Calm)** | yes | The AI agent that will use the templates. May be present via a dedicated air-gapped laptop; must not have any cloud connectivity during the ceremony. |
| **Capture witness** | yes | One trusted human, ideally with no commercial relationship to the principal. Their attestation signs the Pedersen commitment to the session record. |
| **Anti-substitution witness** | recommended | A second human who has known the principal for ≥5 years; attests to identity without seeing template contents. |
| **Notary** | optional | A licensed notary public attests to the physical ceremony having taken place at the recorded address and date. Required for v1+ in jurisdictions where Calm Witness proofs are introduced as evidence. |
| **Bystanders** | NONE | If a bystander walks into the room, the ceremony aborts and restarts in a different physical location. |

## §3. Required equipment

- **Capture device, primary:** a stylus tablet (Wacom Intuos Pro M or larger; iPad Pro + Apple Pencil 2 acceptable for v0). Sampling rate ≥ 200 Hz, pressure levels ≥ 4096, tilt detection. Per Everest 12.
- **Capture device, voice:** the same tablet's microphone or a wired USB microphone. No Bluetooth.
- **Capture host:** a laptop running the air-gapped `calm-witness enroll` CLI (Everest 12 binary). Filesystem-encrypted; no network interface enabled.
- **Vault hardware:** the principal's existing Calm Vault drive (`~/.calm-vault/`). Mounted on the capture host for the ceremony only.
- **Power:** wall power (not battery alone) for both devices; ceremony exceeds 60 minutes and battery-driven capture has documented stylus latency drift on some tablets.
- **Paper and pens:** for warm-up only. Discarded into a paper shredder at end-of-session; no scans, no photographs.
- **Witness signing keys:** each witness brings their existing CredexAI VC + signing key on a hardware token (YubiKey or equivalent). Required for the post-ceremony Pedersen-commitment signing step.

## §4. Disallowed items

- Smartphones — left in another room.
- Smart watches — left in another room.
- Networked laptops other than the air-gapped capture host.
- Cameras of any kind — including disabled cameras on devices; physical opaque tape required on any device-built-in camera that enters the room.
- Smart-home microphones (Echo, HomePod, etc.) — power-cut at the breaker if the room contains them and they cannot be removed.
- Notes / scripts / pre-printed text the principal would read aloud — voice samples must be free-response, not recitation. (See §6 step C.)

## §5. Pre-ceremony preparation (≤24h before)

1. **Schedule.** Principal picks date/time when they are well-rested and in their declared baseline state. Re-schedule if the ceremony falls during an acute stressor (illness, grief, recent travel jet-lag, etc.).
2. **Witness confirmation.** All witnesses confirm attendance, bring their hardware tokens, and have read §1 + §2.
3. **Location.** Quiet indoor room with door-lock, no shared HVAC noise during voice capture. Recorded address goes into the ceremony manifest.
4. **Capture host bring-up.** `calm-witness enroll --dry-run` exercises the capture pipeline without touching the vault; verifies stylus drivers, microphone gain, and that airplane mode is engaged.
5. **Vault snapshot.** A read-only snapshot of the current vault state is captured to a separate encrypted drive in case the ceremony aborts and the vault must be rolled back.

## §6. Ceremony script (~60 minutes total)

### A — Room sweep (~5 min)

The operator (Calm) walks the room calling out every electronic device aloud. The capture witness checks each one off a printed list. Any device that can connect to a network is removed from the room or powered off at the wall. Verify airplane mode on the capture host with a hardware radio-check tool if available.

### B — Witness affirmation (~3 min)

Each witness states aloud:
- their full legal name,
- their relationship to the principal,
- that they are present voluntarily,
- that they have read the ceremony spec.

The operator records the audio for the affirmation; this audio is kept (it is the witnesses' attestation, not the principal's biometric).

### C — Principal opening statement (~3 min)

The principal states aloud, in free response (no script):
- their full legal name,
- the current date,
- a one-sentence summary of *why* they are enrolling.

This is captured under the voice pipeline of Everest 13 (transcribed locally, raw audio destroyed at end-of-session). It serves as a baseline lexical sample and as the first voice transcription template.

### D — Handwriting warmup (~5 min)

Principal writes by hand on paper (which will be shredded):
- the alphabet, lowercase and uppercase,
- the digits 0–9,
- their signature, 3 times.

This loosens the writing hand and surfaces any unusual day-of stylus issues *before* committing to template captures.

### E — Handwriting templates (~15 min)

On the stylus tablet, principal produces N ≥ 7 handwriting samples, **one per declared state**. Default state list:

| State label | Prompt |
|---|---|
| `calm` | A 2-sentence description of a meal you cooked last week. |
| `creative` | A 2-sentence description of an idea you had this morning that excited you. |
| `focused` | The first paragraph of the protocol you are enrolling for, in your own words. |
| `playful` | A 2-sentence in-joke between you and a person you know well. |
| `tired` | A 2-sentence description of the last time you stayed up too late. |
| `analytical` | A 2-sentence explanation of compound interest. |
| `affectionate` | A 2-sentence letter to someone you love. |

Each sample is committed under its state label. Per-stroke kinematic data is recorded; the rendered glyph image is **not** stored. (Forensic-document-examination prior art is shape-biased; Calm Witness is kinematic-biased because kinematics are harder to forge than shape.)

Principal may request additional state-labels not on the default list. Custom state-labels are appended to the principal's per-vault state vocabulary.

### F — Voice-transcription templates (~15 min)

For each state-label from §E, principal speaks aloud the same prompt for ~60 seconds, free-response, no script. The Everest 13 pipeline transcribes locally; the transcript + word-timing is committed under the state label; the raw audio is destroyed at end-of-segment.

### G — Coercion-check moment (~2 min)

The capture witness asks the principal, with the operator and any anti-substitution witness present:

> "Are you proceeding voluntarily and are you in the state you wish to enroll today?"

Principal answers aloud. If the answer is anything but a clear affirmation, the ceremony aborts. If the principal answers affirmatively but the witness has private doubt, the witness signals the operator after the ceremony and the operator initiates Everest 19 (Re-enrollment red-flag detection) before any template is sealed.

### H — Template sealing (~5 min)

The capture host runs `calm-witness enroll --seal`:

1. Compute per-template feature vectors.
2. Compute the principal's per-state Pedersen commitment `Com(template_features; r_state)` using fresh randomness `r_state`.
3. Append a `kind: "enrollment"` record to `user_state.jsonl` containing only the commitments (no features, no transcripts).
4. Encrypt the raw templates under the principal's identity key (Everest 16) and write to `~/.calm-vault/templates/v1/`.
5. Wipe in-memory plaintext.

### I — Witness signatures (~3 min)

Each witness signs the new `user_state.jsonl` `record_hash` with their hardware token. The signatures are appended as a separate `kind: "witness_attestation"` record, referencing the enrollment record's `record_hash`.

### J — Close-out (~2 min)

- Shred warm-up paper.
- Power down the capture host.
- Operator and witnesses confirm aloud that the ceremony is complete.
- Vault is dismounted.

## §7. Artifacts produced

- N (default 7) sealed handwriting templates per state-label.
- N voice-transcription templates per state-label, with no raw audio.
- One `kind: "enrollment"` record in `user_state.jsonl` containing only Pedersen commitments to the templates.
- One `kind: "witness_attestation"` record per witness, signed by their hardware token.
- A printable ceremony manifest (PDF) signed by the operator's identity key — for legal / notarial purposes only, never required to verify a Calm Witness proof.

## §8. Abort conditions (any one triggers full restart at a later date)

- Bystander entry.
- Network device detected mid-ceremony.
- Capture-device hardware failure (stylus drops samples, mic clips).
- Principal pauses for > 10 minutes or expresses any hesitation about proceeding.
- Witness departs mid-ceremony.
- Coercion-check answer (§G) is not a clean affirmation.
- Capture host loses power (battery + wall both fail).

On abort: the `--seal` step is **not** executed; no enrollment record is written; the vault snapshot from §5 is the surviving state.

## §9. Threat coverage (forward references to dedicated Everests)

| Attack | Where it lives |
|---|---|
| Substitution (different human enrols) | Anti-substitution witness (§2) + Everest 21 (Enrollment Fraud Taxonomy) |
| Coercion (principal forced to enrol under duress) | §G coercion check + Everest 65 (`bank_teller_note_active` predicate later attestation) |
| Replay (pre-recorded handwriting/voice fed into capture rig) | Everest 49 (Liveness Detection at Capture Time) |
| Compromised capture device | Everest 14 (Capture-Device Attestation) — TPM / Secure Enclave signs the raw sample manifest |
| Template substitution after ceremony | Everest 16 (Template Encryption & Key Custody) |
| Adversary witness | Witness identity bound to a CredexAI VC; multiple-witness requirement raises the collusion bar |
| Day-of mood is outside baseline | §5 scheduling rule + §E multi-state default list captures multiple moods |
| Stale ceremony (templates drift) | Everest 18 (Re-enrollment Cadence) + Everest 39 (Drift Modeling) |

## §10. Open questions for v0 → v1

1. **Notary mandate.** v0 says "optional"; should v1 mandate a notary for any Calm Witness proof submitted as evidence in a US court?
2. **Witness compensation.** Witnesses give 60+ minutes of focused presence. The protocol is silent on whether they are compensated. v0 default: principal's discretion.
3. **Remote ceremony.** Strictly disallowed in v0. v2 may explore a tele-presence variant with hardware-attested cameras, but the air-gap principle is hard to preserve over any network.
4. **Inclusion of HRV / sleep-telemetry baseline at enrollment.** Currently treated as continuous-capture only (Everest 22). Including a snapshot at enrollment time would tighten cross-modal binding but lengthens the ceremony by ~10 min.
5. **State-label vocabulary lock.** Principal-defined custom state labels could fragment cross-protocol predicate evaluation. v0 allows custom labels; v1 may require any custom label to round-trip through the registry (Everest 53).

## §11. Acceptance test

This document is the acceptance artifact. A reasonably-trained third party with this document, the Everest 12 capture device, and the Everest 13 voice pipeline can execute the ceremony end-to-end. A successful run produces all artifacts listed in §7 and writes a verifiable `kind: "enrollment"` record to the chain (verifiable by `calm-witness verify-chain`, Everest 28).

— Calm, 2026-05-20
