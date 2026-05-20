# Everest 12 — Handwriting Capture Hardware Decision

*Phase II — Capture & Enrollment. Prereq: Everest 11.*

## The Decision

**Primary: Apple Pencil Pro + iPad Pro M-series. Fallback: Wacom Intuos Pro M.**

---

## Hardware Comparison Table

| Device Family | Sampling Rate | Pressure Levels | Tilt | Latency | OS | Local-Pipeline Support | Audit-Trail Capable | Cost (USD) |
|---|---|---|---|---|---|---|---|---|
| **Apple Pencil 2 + iPad Pro M** | 240 Hz | 4096 | Yes | ~9 ms | iOS 17+ | Excellent (PencilKit) | Yes (Secure Enclave) | ~$2200 |
| **Apple Pencil Pro + iPad Pro M** | 240 Hz | 4096 | Yes, + barrel-roll | ~9 ms | iOS 18+ | Excellent (PencilKit) | Yes (Secure Enclave) | ~$2400 |
| **Wacom Intuos Pro M** | ~200 Hz | 8192 | Yes | ~15 ms | macOS, Linux, Windows | Good (native API) | Moderate (no TEE) | $380 |
| **Wacom Cintiq Pro 27** | ~200 Hz | 8192 | Yes | ~15 ms | Windows, macOS | Good (native API) | Moderate (no TEE) | $3500 |
| **reMarkable 2** | 96 Hz | 4096 | Yes | ~25 ms | Proprietary Linux | Limited (SDK exists) | Limited | $398 |
| **Samsung Galaxy Tab S10 + S Pen** | ~240 Hz | 4096 | Yes | ~12 ms | Android 14+ | Fair (Samsung DeX) | Limited (Knox: vendor lock) | ~$1500 |
| **Microsoft Surface Pro 11 + Pen** | ~200 Hz | 4096 | Yes | ~20 ms | Windows 11 | Fair (Windows Ink) | Moderate | ~$1800 |

---

## Rationale

### Kinematics > Glyphs

The enrolled templates in Calm Witness must capture motor micro-signatures — velocity profiles, pressure curves, jerk discontinuities, tremor oscillations — that differentiate one principal's hand from another. These signatures are the substrate of the biometric distance comparator (Everest 36). Apple Pencil Pro and Wacom Intuos Pro both deliver the pressure and tilt resolution necessary. Apple Pencil Pro's 240 Hz polling (vs. Wacom's ~200 Hz) gives us finer granularity in velocity and acceleration, the features most robust to volitional imitation. Critically, the comparator runs on-device in the principal's vault; no raw kinematic data leaves the device.

### Apple Pencil Pro as Primary

Apple Pencil Pro brings four decisive advantages. First, it pairs with iPad Pro M-series (running iOS 18+), which integrates tight sandboxing via the Secure Enclave: the capture app can be containerized in a way that is difficult to replicate on a general-purpose OS. The Secure Enclave can sign the raw event stream, binding it cryptographically to the device and making tampering visible to the comparator downstream. Second, the 240 Hz sampling rate and 4096 pressure levels exceed the floor and give headroom for feature extraction; the barrel-roll sensor (new in Pro) adds azimuth as an additional axis, making substitution attacks marginally harder. Third, the ecosystem maturity — PencilKit, UIPencilHoverInteraction, the low-latency rendering path — means the capture app can be built to production quality in our budget window. Fourth, an iPad is a single-purpose capture device for the enrollment ceremony; it is easier to justify air-gapping an iPad than a Windows laptop or a MacBook Pro.

The cost (~$2400 for an iPad Pro M-series + Apple Pencil Pro) is justified by the Secure Enclave binding and the sandbox assurance it brings to the enrollment ceremony (Everest 11 §H).

### Wacom Intuos Pro as Fallback

Not every principal uses Apple hardware. The Wacom Intuos Pro M ($380) is a cross-platform fallback covering macOS, Windows, and Linux principals. Its 8192 pressure levels exceed our floor (2048) and give fine-grain motor data. The ~200 Hz sampling rate is acceptable for offline comparison (the difference between 200 and 240 Hz is ~0.5 milliseconds per sample; kinematic features average over windows of 50–500 ms, so the difference is marginal for most motor signatures). The Wacom native API (WinTab, macOS IOKit) provides direct event-stream access without going through a rendered-ink layer, which is what we need for kinematic capture. Wacom tablets lack a TEE equivalent, but we compensate via the calm-witness-cli's own integrity logging (Everest 14: Capture-Device Attestation).

A principal on Windows or Linux can enroll using Intuos Pro + a dedicated air-gapped capture host (calm-witness enroll --device=wacom), with Wacom's native driver pinned to a known firmware version and the ceremony rig itself kept offline per Everest 11 §1.

### Hardware Requirements (Floor)

Any compliant capture device must meet these minima:

- **Sampling rate ≥ 120 Hz** — Apple Pencil Pro: 240 Hz, Wacom: ~200 Hz. This ensures velocity estimates have noise floor < 1 cm/s.
- **Pressure levels ≥ 2048** — Apple Pencil Pro: 4096, Wacom: 8192. This ensures pressure granularity < 0.05 relative units.
- **Tilt sensing: REQUIRED** — Both primary and fallback support tilt; reMarkable and some Android tablets omit this. Tilt is a low-entropy dimension but contributes to motor-signature binding.
- **Latency ≤ 20 ms end-to-end** — From stylus motion to event emission. Apple Pencil Pro: ~9 ms (OS-level priority), Wacom: ~15 ms (driver level). Both well within budget.
- **Raw event-stream API** — The capture app must read (timestamp, x, y, pressure, tiltX, tiltY, azimuth) tuples *before* they are rendered into an image. For Apple, this is PencilKit's PKStroke + UIPencilHoverInteraction. For Wacom, this is the native WinTab event loop. Rendered-ink images are lossy and leak visual features that the comparator does not need.
- **Simultaneous audio capability** — The same device must run the voice-transcription pipeline (Everest 13) so that handwriting and voice samples share a session ID and wall-clock anchor. An external USB microphone on the Wacom path, iPad's built-in mic for Apple. No Bluetooth audio.

### Capture Data Format Specification

The capture API will emit (into the principal's local vault, never over the network):

```
per_stroke:
  [ (timestamp_ms, x_px, y_px, pressure_0_to_1, tiltX_deg, tiltY_deg, azimuth_deg), ... ]

per_stroke_metadata:
  {
    stroke_id: "uuid",
    state_label: "calm" | "creative" | ... (from Everest 11 §E),
    start_ts_ms: int,
    end_ts_ms: int
  }

per_session_envelope:
  {
    session_id: "uuid",
    device_model: "iPad Pro M-series" | "Wacom Intuos Pro M",
    device_firmware_hash: "sha256",
    capture_app_version: "calm-witness 0.1.0",
    timestamp_anchor: { timestamp_ms, sigsum_proof }
  }
```

The raw kinematic tuples (not the rendered ink image) are what feed into the comparator. This design ensures the templates remain tied to motor biometrics, which are hard to imitate, rather than glyph geometry, which is easier to forge.

### Threat Model Coverage

**Imitation under observation:** An adversary with a video of the principal writing cannot reproduce the pressure, tilt, and jerk profiles even if they can see the letter shapes. The kinematic signatures are involuntary.

**Replay of stroke stream:** Deferred to Everest 49 (Liveness Detection). At capture time, we trust the tablet's hardware attestation (Everest 14) that the strokes are real-time events, not pre-recorded samples. If needed, we can add challenge-response prompts (e.g., "write this random phrase") at enrollment, making any later replay obviously stale.

**Device-firmware tampering:** Deferred to Everest 21 (Enrollment Fraud Taxonomy). We assume the iPad or Wacom device is trustworthy at ceremony time (or at minimum, that any compromise is detectable via Secure Enclave signing on Apple, or via external attestation on Wacom). If a principal's device is suspected to be compromised *after* enrollment, Everest 21 governs re-enrollment and fraud investigation.

**Substitution (different human pretending to be principal):** Covered by Everest 11 §2 (anti-substitution witness). The hardware itself does not prevent substitution, but the ceremony's witness structure does.

### Procurement and v0 Budget

Initial enrollment ceremony kit:
- 2× iPad Pro M-series (64 GB, Wi-Fi): ~$1200
- 2× Apple Pencil Pro: ~$400
- 1× Wacom Intuos Pro M (as cross-platform fallback): ~$380
- **Total: ~$2000–2500 USD**

One iPad + Pencil Pro is the ceremony rig; the second is a hot spare (device failure is an abort condition per Everest 11 §8). The Wacom Intuos Pro serves future principals who bring non-Apple hardware. This budget is reasonable for a cryptographic biometric system's enrollment infrastructure.

---

— Calm, 2026-05-20
