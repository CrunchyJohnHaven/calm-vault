# Everest 89 — Mobile Vault Native Apps (iOS + Android)

**DESIGN-BAGGED · Institutional Follow-Through — Multi-Quarter Mobile App Development**

Phase VII—Engineering Reliability. Prereqs: Everests 81 (Rust crate), 88 (biometric budget), 12 (handwriting), 13 (voice), 74 (accessibility).

---

## 1. Overview

This Everest specifies native mobile vault applications for iOS (Swift/SwiftUI) and Android (Kotlin/Compose) as the primary user-facing interface for Calm Witness disclosure workflows. The apps embed the E81 Rust cryptographic core via FFI, run biometric predicates locally on-device (E12, E13, E88), and enforce battery efficiency (≤5%/hour) while maintaining non-custodial key security through Secure Enclave (iOS) and StrongBox (Android) integration.

**Non-negotiable constraints:**
- Native implementation required; React Native and Dart cross-platform frameworks are rejected due to performance loss, Secure Enclave/StrongBox access limitations, and Pencil/stroke capture precision requirements.
- No server-side predicate evaluation; all disclosure logic runs locally with zero trust in mobile OS or network operator.
- Offline-first architecture: vault functions without network; sync occurs opportunistically when reachable.
- App Store + Play Store distribution via standard developer enrollment; no sideload requirement.
- Compliance with platform accessibility standards (WCAG 2.1 AA) and neurodiversity-aware UI patterns per E74.

---

## 2. Platform Strategy

### 2.1 iOS (Swift 5.8+, SwiftUI, iOS 14+)

**Language & Framework:**
- Swift with SwiftUI for native UI composition; UIKit bridging for legacy system integration (e.g., ASAuthorizationController for biometric UI).
- Deployment target: iOS 14.0 to support iPhone 6S+ and iPad Air 2+; target adoption at iOS 16+.
- Xcode 14+ build chain; Swift Package Manager (SPM) for dependency management where possible.

**Secure Enclave Integration:**
- All disclosure templates and biometric commitments encrypted via SecKey operations; private keys never leave Secure Enclave.
- SecKeyCreateSignature used for disclosure response signing; no key export.
- Template symmetric key (AES-256-GCM) derived via SecKeyDerive with domain separation labels per E104b.
- Biometric capture (Touch ID / Face ID) gated through LocalAuthentication framework; user consent required for each vault operation.

**Pencil / Stroke Capture:**
- PencilKit framework for stylus input (iPad Pro 2018+, iPad Air 2022+).
- Stroke serialization to ProtoBuf (interop with E12 preprocessing pipeline) with on-device compression (zstandard).
- Fallback to finger-drawing on non-Pencil devices with degraded accuracy signal passed to E88 distance predicates.

**Voice Transcription (On-Device ASR):**
- Whisper.cpp compiled to iOS arm64 via Xcode; inference runs on Neural Engine where available, CPU fallback for older devices.
- Audio capture via AVAudioEngine; silence detection and VAD (voice activity detection) to minimize compute.
- Transcripts held in memory only during active session; no persistent audio files stored.

**Background Activity:**
- BackgroundTasks framework: one scheduled background task per hour for anchor refresh (Sigsum + Roughtime verification).
- BGProcessingTask for heavier work (e.g., full chain validation on network change); platform allows ~10 min/hour CPU budget.
- Sentinel monitoring delegated to UNNotificationRequest with push-based notifications from background process (requires server coordination; see Section 8).

### 2.2 Android (Kotlin 1.8+, Jetpack Compose, Android 9+)

**Language & Framework:**
- Kotlin with Jetpack Compose for declarative UI; AndroidX libraries for compatibility.
- Minimum SDK 28 (Android 9); target SDK 34 (Android 14).
- Gradle 7.5+ build system; Kotlin Multiplatform Mobile (KMM) considered only for Rust bindings, not UI code.

**StrongBox Integration:**
- AndroidKeyStore with isUserAuthenticationRequired() and hardware-backed keymaster3+ on devices with StrongBox Keymaster; software fallback on older devices with reduced security guarantee flagged to user.
- KeyGenParameterSpec.Builder with PURPOSE_SIGN for disclosure signing; no private key export.
- Template symmetric key derivation mirrors iOS SecKeyDerive semantics; domain separation via HKDF as per E104b.
- Biometric authentication via BiometricPrompt; system-level encryption of sensitive data on lock.

**Pencil / Stylus Capture (Android):**
- MotionEvent.getToolType() filtering for stylus input on Samsung S-Pen, Apple Pencil (via USB-C adapter on Samsung tablets), or generic active stylus.
- Pressure and tilt data captured via MotionEvent attributes; serialization to ProtoBuf matching iOS path.
- On-device preprocessing (curvature, velocity features) for E12 integration.

**Voice Transcription (On-Device ASR):**
- Whisper.cpp compiled to Android arm64-v8a and x86_64 ABIs.
- SpeechRecognizer APIs for audio capture; Google's on-device speech recognizer (available on Android 12+ devices with Google Play Services) used as secondary fallback if Whisper.cpp unavailable.
- Transcripts ephemeral; no persisted audio files.

**Background Activity:**
- WorkManager with doze-aware scheduling: anchor refresh as periodic work (interval 60 min, flex window 10 min).
- Sentinel monitoring as low-priority background work; frequency reduced in battery-saver mode via Device.getBatteryManager().isLowPowerMode().
- Job Scheduler for API 31+ devices supporting expedited work (reserved for urgent disclosure responses only).

---

## 3. On-Device Predicate Evaluation

### 3.1 Architecture

All predicate evaluation runs locally; disclosure decision is binary local output (true/false) before proof generation. No server-side re-evaluation or dynamic predicate loading.

**Predicate Class Taxonomy:**
- **Temporal**: in_baseline_24h (rolling 24h capture window via E55).
- **Biometric**: biometric_match_within(τ) dispatched to E88 (distance threshold predicates).
- **Cognitive**: cognitively_atypical_baseline, mental_state_unusual (inferred from voice/handwriting variance per E59–60).
- **Consent**: explicit_disclosure_consent (user tap; consent recorded to chain per E57).
- **Values**: alignment_threshold(v_user, v_counterparty, τ_sim) composition per E130.
- **Harm**: no_harm_evidence_any aggregation per E165 (union of E147–156, E158–160).
- **Cooperation**: sustained_cooperation, reciprocity_ratio(threshold), cross_difference_respect per E170–E172.

### 3.2 Evaluation Runtime

Built-in predicate evaluator in Swift/Kotlin with no external dependencies:

```
Predicate := AND(predicates) | OR(predicates) | NOT(predicate) | 
             Temporal(key) | Biometric(template, τ) | Cognitive(envelope) | 
             Consent | Values(alignment_proof) | Harm(absence_evidence) | 
             Cooperation(streak_ct)

eval(predicate, vault_state, counterparty_context) → boolean
```

**Evaluation Order (short-circuit):**
1. Consent (fail-fast if not present).
2. Harm aggregates (fail-fast if harm evidence present).
3. Temporal checks (cache-friendly, low latency).
4. Biometric predicates (invoke E88 distance machinery; 1–2 second latency).
5. Values alignment (invoke E130 ZK proof verification; <500 ms).
6. Cooperation aggregates (chain walk; bounded by 100-entry window to avoid O(n) latency).

**Error Handling:**
- Predicate evaluation errors (e.g., corrupted template, missing baseline) do not block user; errors are logged to audit chain and a conservative default (false) returned.
- User is notified of evaluation failures but allowed to retry with fresh capture.

### 3.3 State Machine for Disclosure

```
IDLE
  ↓ [disclosure_request received]
  EVALUATING_PREDICATES
  ↓ [predicates = false] → REJECTED (notify user + log to chain)
  ↓ [predicates = true] → PROOF_GENERATION
  PROOF_GENERATION
  ↓ [Rust proof generation complete]
  RESPONDING
  ↓ [response signed + serialized]
  DELIVERED (or QUEUED if network unavailable)
```

---

## 4. Biometric Capture Pipeline

### 4.1 Pencil/Stroke Capture (Handwriting)

**Workflow:**
1. User opens vault app, taps "Capture Signature" (E12 design).
2. PencilKit canvas presented; optional on-screen prompt (e.g., "Sign as you would on paper").
3. Real-time pressure, tilt, altitude captured via MotionEvent (Android) or UITouch.stylusProperties (iOS 16.1+).
4. Stroke serialization to E12 ProtoBuf schema; on-device compression (zstandard level 10).
5. Hash commitment computed (SHA-256) and appended to chain record.
6. Template encrypted to Secure Enclave/StrongBox; original stroke data cleared from memory.

**Quality Control:**
- Minimum stroke duration: 500 ms (reject single taps).
- Minimum stroke complexity: 5 inflection points (reject near-linear strokes).
- Pressure variance: reject if pressure range < 20 units or max pressure < threshold (device dependent; calibrated per E88).
- Fallback prompt: if quality check fails, user invited to retry or skip to voice enrollment.

### 4.2 Voice Transcription-Only Pipeline

**Workflow (E13 interface):**
1. User taps "Capture Voice" button.
2. AVAudioEngine (iOS) / AudioRecord (Android) captures at 16 kHz mono PCM.
3. VAD (voice activity detection) via Whisper.cpp silence detection; record stops after 2 seconds silence.
4. Whisper.cpp inference (encoder-only, no generation) transcribes audio to text.
5. Transcript hashed (SHA-256) and appended to chain; audio file NOT stored on device.
6. Metadata (duration, VAD confidence, ambient noise estimate) recorded for E88 inference.

**Security Properties:**
- Audio never persisted; inference happens on Neural Engine (iOS) or CPU with immediate buffer clear.
- Transcript limited to confidential vault context (never synced to cloud, never used for other app features).
- Biometric identifier derived from acoustic features (pitch contour, speech rate, spectral variance) per E13, not transcript content.

### 4.3 Multi-Modal Enrollment

**Typical flow (E11 ceremony):**
1. Handwriting: 3 signature repetitions, 30 seconds apart, to capture baseline variance.
2. Voice: 2 read-aloud phrases (randomized from list of 50 to defend against recording attack), ~15 seconds each.
3. Face/fingerprint: platform biometric (Touch ID / Face ID on iOS; BiometricPrompt on Android) tied to Secure Enclave/StrongBox.
4. Composite template: weighted blend of handwriting, voice, face/fingerprint feature vectors. Template size <5 MB encrypted.

**Re-enrollment Cadence (E18):**
- Automatic refresh trigger: 90 days or 50 disclosures, whichever comes first.
- User-initiated refresh: any time from settings.
- Re-enrollment flagged as high-stakes: explicit consent required, new 3-signature baseline captured.

---

## 5. Key Custody & Secure Storage

### 5.1 iOS Secure Enclave

**Disclosure Signing Key:**
```swift
let tag = Data("com.calmvault.disclosure.signing".utf8)
var query = [kSecClass: kSecClassKey, kSecAttrKeyType: kSecAttrKeyTypeECSHA256, 
             kSecAttrApplicationTag: tag, kSecAttrKeyClass: kSecAttrKeyClassPrivate]
var result: CFTypeRef?
let status = SecItemCopyMatching(query as CFDictionary, &result)
if status != errSecSuccess {
  // Generate new key in Secure Enclave
  let attributes = [kSecAttrTokenOID: kSecAttrTokenOIDSecureEnclave, 
                    kSecAttrKeyType: kSecAttrKeyTypeECSHA256]
  SecKeyCreateRandomKey(attributes as CFDictionary, &error)
}
let signature = SecKeyCreateSignature(privateKey, .ecdsaSignatureMessageSHA256, 
                                      disclosure_bytes, &error)
```

**Template Encryption Key:**
- Derived via PBKDF2(user_password_hash, domain_salt="com.calmvault.template.v1", iterations=100000, length=32).
- Stored in Keychain with kSecAttrAccessibleWhenUnlockedThisDeviceOnly.
- Decryption requires user unlock (device passcode or biometric).

### 5.2 Android StrongBox Keymaster

**Disclosure Signing Key:**
```kotlin
val keyGenSpec = KeyGenParameterSpec.Builder("com.calmvault.signing", KeyProperties.PURPOSE_SIGN)
  .setKeySize(256)
  .setDigests(KeyProperties.DIGEST_SHA256)
  .setUserAuthenticationRequired(true)
  .setUserAuthenticationValidityDurationSeconds(300)
  .setIsStrongBoxBacked(true) // Hardware-backed; software fallback if unavailable
  .build()
val keyGenerator = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_EC, "AndroidKeyStore")
keyGenerator.initialize(keyGenSpec)
val keyPair = keyGenerator.generateKeyPair()
```

**Template Encryption:**
- AES-256-GCM key stored in AndroidKeyStore.
- Encryption handled via Cipher.getInstance("AES/GCM/NoPadding", "AndroidKeyStore").

### 5.3 Offline-Capable Key Material

- Disclosure signing key: always hardware-backed (non-exportable).
- Template encryption key: derivable from user password + hardware salt (device-specific entropy from TEE).
- If hardware-backed keystore unavailable (rare): user notified; software keystore used with warning banner; user may decline and reset device.

---

## 6. Battery Budget Implementation

Per E89, target is ≤5% per hour. Strategies:

**Disclosure without biometric refresh:** <0.1% battery
- Lookup proof from cache (typically 1–2 MB chain segment).
- Cryptographic signature validation (100 ms on main CPU).
- Network send (500 ms radio on-time; coalesced with other outbound traffic).

**Disclosure with biometric refresh:** <0.5% battery
- Handwriting: 10–30 seconds capture + E12 preprocessing (~200 ms) + distance evaluation (~500 ms).
- Voice: 30 seconds recording + Whisper.cpp inference (5–10 seconds on Neural Engine) + E13 extraction (~500 ms).
- Face/fingerprint: 1–2 seconds via BiometricPrompt API.
- Total: ~30 seconds elapsed time; 2–5 seconds CPU; metabolized across full-hour cycle.

**Anchor refresh (hourly):** <0.05% battery
- Fetch latest Sigsum and Roughtime proofs (network fetch ~500 ms).
- Verify signatures (E30, E31 cost ~100 ms).
- Update cache (disk write 50 ms).
- Batching: multiple anchor refreshes coalesced into one network transaction if they occur within 10-minute window.

**Sentinel monitoring:** <1% per hour
- Probabilistic anomaly detection (Bloom filter lookups on event stream; see Section 9).
- Frequency: every 30 seconds (configurable; reduced in battery-saver mode to every 5 minutes).
- CPU cost: <10 ms per check.

**Optimization Implementation:**
- Network coalescing: batch outbound sync requests; queue arrival events.
- CPU scheduling: defer non-urgent proof generation to low-activity windows (detected via MotionManager and user input history).
- Hardware acceleration: BiometricPrompt and Neural Engine for biometric inference; Secure Enclave/StrongBox for crypto; main CPU reserved for logical dispatch only.
- Adaptive frequency: reduce background task frequency on low battery (<20%); suspend non-urgent work at <10%.

---

## 7. Cross-Device Pairing & Multi-Device Principals

**Design:**
- User enrolls on Device A (primary); unique device_id generated from TEE entropy.
- User initiates pairing on Device B (secondary); generates separate device_id.
- Out-of-band verification: QR code scan or 6-digit code display (both devices show matching code).
- Pairing record: signed by both device keys and appended to chain with kind: "device_pairing".

**Disclosure Multi-Device Flow:**
1. Disclosure request arrives at Device A.
2. If predicate requires fresh biometric: Device A captures, evaluates locally.
3. Device A generates proof and responds; proof is device_A_signed.
4. If multi-device endorsement required (user preference): Device B receives notification.
5. Device B user biometrically approves; signs a device_B_acknowledgment appended to chain.
6. Counterparty receives Device A primary proof + Device B acknowledgment metadata.

**Device Compromise Mitigation:**
- If Device A suspects compromise (e.g., repeated anomaly signals), user can revoke pairing from Device B.
- Revocation is chain-signed and published; any proofs signed by Device A after revocation_time are treated as suspect.
- User must re-enroll on a trusted device (Device C) to continue disclosures.

---

## 8. Offline Operation & Sync

**Offline-First Architecture:**
- Disclosure request arrives (via local notification, deep link, or background message queue).
- Predicate evaluation runs entirely locally; no network call required.
- Proof generation (cryptographic) runs entirely locally.
- Disclosure response serialized and queued to outbound_queue.

**Network Availability States:**
1. **Online**: Responses sent immediately (latency <2 seconds).
2. **Offline**: Responses queued; pending indicator shown to user.
3. **Intermittent**: On network change event, attempt flush of outbound_queue; exponential backoff if network flaky.

**Sync Protocol:**
- Once connectivity detected: enumerate outbound_queue.
- For each queued response: attempt POST to counterparty endpoint (URL from disclosure_request metadata).
- If successful: move to sent_log and purge from queue.
- If failed (4xx/5xx): leave in queue; retry after backoff interval (60 s, 5 min, 30 min, 4 hours).
- After 4 failed attempts: escalate to user notification ("Failed to send disclosure response; tap to retry").

**Local Anchoring (No Network):**
- Chain appends happen locally without Sigsum/Roughtime anchor.
- Records flagged with anchor_status: "pending".
- On network return: batch pending records and submit to Sigsum (cost ~100 ms per batch).

---

## 9. Sentinel Monitoring (Anomaly Detection)

**On-Device Sentinel Process:**
- Runs as low-priority background work; detection uses probabilistic data structures (Bloom filters, HyperLogLog) to minimize memory.
- Monitors:
  1. Anomalous disclosure request patterns (e.g., >10 requests from same counterparty within 5 min).
  2. Biometric mismatch signals (E88 distance exceeds threshold; user queried; baseline corrupted).
  3. Key access anomalies (e.g., Secure Enclave signature attempt fails 5+ times).
  4. Time-skew signals (device clock jumped backward; chain anchor verification fails).

**Detection Mechanics:**
- Bloom filter of disclosed-to counterparty IDs (rolling 24h window); collision acceptable (false-positive tolerable; user notified if detected).
- HyperLogLog cardinality estimate of unique counterparties per hour; alert if cardinality spike (e.g., 10× baseline).
- Time-series anomaly detection on biometric distance values (rolling 7-day z-score; alert if >3σ).

**Escalation:**
- Low confidence (0.5–0.7): logged to audit chain; no user notification.
- Medium confidence (0.7–0.9): background notification; user invited to review audit log.
- High confidence (>0.9): immediate foreground alert; user action required to dismiss (cannot be silent); option to invoke recovery workflow.

**Recovery Workflow:**
- User prompted: "Anomalous activity detected. Options: (1) Review audit log, (2) Rotate template, (3) Revoke device (if multi-device)."
- Option 1: Show last 20 disclosure events with counterparty, time, predicate_result.
- Option 2: Initiate new biometric enrollment (Section 4.3).
- Option 3: Mark device as untrusted; no further disclosures until manual unlock (requires passcode entry on another device or user waiting 24h).

---

## 10. Accessibility & Neurodiversity (Per E74 Review)

**Required Accommodations:**

1. **Cognitive Load Minimization:**
   - Single-decision consent screens: never show values-similarity slider or composite predicates.
   - Each screen asks one discrete question: "Do you consent to disclose [single predicate]?"
   - If composite predicate (AND/OR): decompose; show each conjunct separately.
   - Example: instead of "Consent to disclose (consent AND harm_absence AND cooperation)", show three screens:
     - "Does the counterparty have your explicit consent?"
     - "Is there evidence of potential harm?"
     - "Have you sustained cooperation with this counterparty?"

2. **Alternative Input Modalities:**
   - Handwriting capture optional; voice enrollment equally weighted.
   - Text-based input for disclosure context (if user prefers typing to voice).
   - Eye-tracking support via platform APIs (iOS Pointer Interaction; Android Eye Tracking enabled by third-party software).

3. **Temporal Flexibility:**
   - No time-pressure interfaces (e.g., "Respond within 30 seconds").
   - Disclosure request persists indefinitely; user may respond days later without penalty.
   - Background sync does not trigger foreground notifications; user controls notification schedule (quiet hours respected).

4. **Color & Contrast:**
   - WCAG 2.1 AA minimum (7:1 contrast for text; 4.5:1 for UI controls).
   - No color-coding without text labels (e.g., red/green status indicators paired with "Unsafe" / "Safe" text).
   - Dark mode support with forced color adjustment (iOS: supports dynamic type + light/dark variants).

5. **Text Sizing & Readability:**
   - Dynamic Type support (iOS) / system font scaling (Android).
   - Minimum font size: 14pt; clear sans-serif typeface (SF Pro Display / Roboto).
   - Line spacing: 1.5× minimum for body text.

6. **Screen Reader Support:**
   - Full VoiceOver (iOS) / TalkBack (Android) compatibility.
   - Semantic HTML/UIAccessibility labels on all interactive elements.
   - Status changes announced (e.g., "Disclosure response sent").

---

## 11. App Store & Play Store Distribution

**iOS App Store (Apple Inc.)**
- Developer Account enrollment; annual $99 USD fee.
- Code signing with Apple Developer certificate; app notarization (automated).
- Review process: ~24–48 hours; primary risk is Secure Enclave API usage (Apple approves for authentication; approval expected).
- Privacy label completion: data collection categories (biometric template, user disclosure history) disclosed; no third-party sharing.
- SKU: com.calmvault.vault (or per branding decision).

**Google Play Store (Google LLC)**
- Developer Account enrollment; one-time $25 USD registration fee.
- Signing with upload key (Google Play handles re-signing).
- Review process: ~2–4 hours; no known blocking risk for StrongBox integration.
- Privacy label: biometric data collection and on-device processing disclosed; no third-party sharing.
- SKU: com.calmvault.vault.

**Post-Launch Updates:**
- iOS: incremental updates via App Store; forced minimum OS version bump requires new review (expected quarterly for security patches).
- Android: incremental updates via Play Store; no review delay for patch releases in same major version.
- Rollback: if critical bug detected post-release, immediately pull app version from store and push patch; user retention of old version is device owner's choice.

---

## 12. Concord-Compliant UI Surface

**Consent Screen Design per E57:**

All disclosure consent interactions must adhere to Concord compliance (see E57 for definitions):

```
Screen Layout (single predicate per screen):

┌──────────────────────────────────────────┐
│  [Close]                    [Settings]    │
├──────────────────────────────────────────┤
│                                          │
│  Disclosure Request                      │
│  ─────────────────────────────────────   │
│                                          │
│  Counterparty: Alice (alice@example.com) │
│  Time: 2026-05-20 14:30 UTC              │
│                                          │
│  Question:                               │
│  Do you consent to disclose your         │
│  [PREDICATE NAME]?                       │
│                                          │
│  [Why this?] [What will be shared?]      │
│                                          │
│  ┌──────────────────────────────────┐    │
│  │  [DECLINE]    [ACCEPT & DISCLOSE]│    │
│  └──────────────────────────────────┘    │
│                                          │
│  Estimated battery impact: <0.5%         │
│                                          │
└──────────────────────────────────────────┘
```

**Information Architecture:**
- "Do you consent?" is the primary question; no values-alignment slider or composite scoring metric visible.
- "[Why this?]" expandable: explains why predicate required (e.g., "Harm absence check protects both you and the counterparty").
- "[What will be shared?]" expandable: names the specific predicate result (true/false) and any auxiliary data (e.g., biometric match confidence as percentile, not raw distance).
- Buttons: high-contrast (WCAG 2.1 AA), large touch targets (≥48pt), clear label ("DECLINE" / "ACCEPT & DISCLOSE").

**Multi-Predicate Disclosure:**
- If counterparty requests AND(consent, harm_absence, cooperation_streak):
  - Show three screens sequentially; user may decline at any screen (abandons disclosure).
  - Each screen evaluates one predicate independently.
  - No aggregated decision shown ("Overall: 80% aligned"); decompose to component truths.

**Predicate Result Granularity:**
- Biometric match: show "Match confidence: 94th percentile" (not raw distance; not similarity score).
- Harm absence: show "No harm signals detected" (boolean; no confidence percent).
- Cooperation streak: show "Cooperation streak: 23 days" (factual counter; not score).

---

## 13. T-E89.1–7 Acceptance Gates

**T-E89.1: Native Framework Compilation**
- iOS: Swift codebase compiles to arm64 + x86_64 (simulator) without warnings.
- Android: Kotlin codebase compiles to arm64-v8a, x86_64, armeabi-v7a ABIs.
- Criterion: zero compiler warnings in release build; code size <150 MB per app (including Rust cryptographic core).

**T-E89.2: Secure Enclave / StrongBox Integration**
- iOS: Disclosure signing key created in Secure Enclave; signature operations verified to be non-exportable (test via attempted key export; must fail).
- Android: StrongBox key generation succeeds on Pixel 6/7/8; software keystore fallback used on test device without hardware-backed keymaster.
- Criterion: all crypto operations complete without exporting private key material.

**T-E89.3: Biometric Capture (Pencil + Voice)**
- Handwriting: 10 signature captures on iPad Pro 6th gen; stroke pressure variance measured; quality check logic rejects single-tap inputs.
- Voice: 5 voice transcriptions at 16 kHz; Whisper.cpp inference latency <8 seconds on iPhone 13+ (Neural Engine) and <15 seconds on older devices (CPU).
- Criterion: stroke and voice templates created; no raw data persisted; templates encrypt under Secure Enclave/StrongBox keys.

**T-E89.4: Battery Budget (<5% per hour)**
- 24-hour soak test: 10 simulated disclosures (5 without refresh, 5 with), 2 hourly anchor refreshes, continuous sentinel monitoring.
- Measurement: battery telemetry from XCTest (iOS) / Battery Historian (Android).
- Criterion: total battery consumed <5% per hour under test profile; thermal peak <75°C sustained.

**T-E89.5: Offline Operation**
- Disconnect network after disclosure request arrives.
- Predicate evaluation and proof generation complete locally.
- Disclosure response queued.
- Restore network; response sent successfully.
- Criterion: user sees no blocking network errors; response eventually delivered.

**T-E89.6: Sentinel Anomaly Detection**
- Inject 100 anomalous disclosure requests to same counterparty within 5 seconds.
- Sentinel detects spike (Bloom filter cardinality explosion).
- User notified within 10 seconds.
- Criterion: notification appears; audit log shows anomaly record; user can review and rotate template.

**T-E89.7: Accessibility Compliance**
- iOS: VoiceOver enabled; all UI elements announced correctly; tap targets ≥48pt; dynamic type scales to 200% without truncation.
- Android: TalkBack enabled; semantic labels correct; high contrast mode (7:1 minimum); screen reader announces status changes.
- Criterion: third-party accessibility audit (e.g., WAVE, Lighthouse) reports zero critical violations; warning-only on WCAG 2.1 A/AA deviations.

---

## 14. Mobile-Team Hiring & Multi-Quarter Timeline

**Phase 1: Hiring & Onboarding (Weeks 1–4)**
- iOS Lead: Senior Swift/SwiftUI engineer (5+ years iOS, Secure Enclave experience preferred).
- Android Lead: Senior Kotlin/Compose engineer (5+ years Android, StrongBox experience preferred).
- QA Engineer: Mobile testing specialist (iOS + Android; cross-platform test automation).
- PM: Product manager experienced in financial/security apps; clear on E89 requirements.

**Phase 2: Architecture & Setup (Weeks 5–8)**
- Rust FFI bindings: iOS (Swift-C interop layer) and Android (Kotlin JNI wrapper).
- E81 Rust crate integration: compile E81 crypto to iOS + Android targets; verify symbol exports.
- CI/CD pipeline: GitHub Actions for iOS (Xcode build, codesign) and Android (Gradle, Play Store staging).
- Architecture review: design document finalized; team sign-off on Secure Enclave/StrongBox approach.

**Phase 3: Core Features (Weeks 9–16)**
- iOS native UI: SwiftUI app shell, predicate evaluation screen, disclosure request handler.
- Android native UI: Jetpack Compose equivalent.
- Secure Enclave/StrongBox integration: key generation, signing, template encryption.
- Biometric capture (Pencil + Voice): E12/E13 integration; on-device ASR (Whisper.cpp); capture quality validation.

**Phase 4: Battery Optimization (Weeks 17–20)**
- Instrumentation: iOS Energy Impact tool, Android Battery Historian.
- Profiling: identify hotspots (biometric inference, network, proof generation).
- Optimization: background scheduling, coalescing, hardware acceleration, adaptive frequency.
- Acceptance test: battery soak test per T-E89.4; iterate until <5% per hour achieved.

**Phase 5: Offline & Sentinel (Weeks 21–24)**
- Offline queueing: outbound_queue implementation, sync retry logic.
- Sentinel monitoring: probabilistic anomaly detection (Bloom filter, HyperLogLog).
- Escalation: user notification, recovery workflow (rotate template, revoke device).
- End-to-end testing: offline disclosure request → response → delivery on reconnect.

**Phase 6: Accessibility & Compliance (Weeks 25–28)**
- E74 review integration: WCAG 2.1 AA audit, neurodiversity accommodations, UI refactor (predicate decomposition, temporal flexibility).
- VoiceOver / TalkBack: full annotation of UI elements.
- Privacy label: Apple App Store + Google Play Store metadata completion.
- Legal review: privacy policy, terms of service, GDPR data processing addendum.

**Phase 7: Testing & Hardening (Weeks 29–32)**
- T-E89.1 to T-E89.7 acceptance gates: team-run tests; third-party validation for T-E89.7 (accessibility).
- Security review: no hardcoded keys, no unencrypted secrets, no credential exfiltration.
- Performance profiling: memory leaks, crash reporting integration (Sentry or equivalent).
- Beta release: internal distribution via TestFlight (iOS) / Firebase App Distribution (Android).

**Phase 8: App Store / Play Store Submission (Weeks 33–36)**
- iOS: developer account enrollment, code signing, app submission, review process.
- Android: Play Store enrollment, signed APK / AAB submission, review process.
- Launch preparation: press release, public-facing documentation, user onboarding.

**Total: 9 months (36 weeks) for production-ready v1.0 release to general availability.**

---

## 15. Composition & Cross-Cutting Integration

### E81 (Rust Cryptographic Core)
- **Input**: compiled Rust .a (iOS) and .so (Android) libraries; symbol exports defined.
- **Output**: disclosed proof cryptographic validity; battery impact <0.5% per disclosure.

### E12 (Handwriting Capture)
- **Input**: ProtoBuf schema for stroke serialization; quality validation heuristics.
- **Output**: on-device preprocessing (curvature, velocity features) fed to E88 distance algorithm.

### E13 (Voice-Transcription Pipeline)
- **Input**: Whisper.cpp compiled binary; sampling rate 16 kHz.
- **Output**: acoustic feature vectors (pitch, spectral shape) for E88 distance evaluation; no persistent transcript.

### E88 (Biometric Distance & Battery Budget)
- **Input**: handwriting/voice feature vectors; threshold parameters (τ).
- **Output**: distance predicate result (true/false); battery consumption <0.5% per evaluation.

### E74 (Disability & Neurodiversity Review)
- **Input**: WCAG 2.1 AA checklist; neurodiversity-aware UI patterns (cognitive load, temporal flexibility).
- **Output**: accessibility-compliant app; T-E89.7 passing third-party audit.

### E104b (Vault Identity & Domain Separation)
- **Input**: device_id derivation from TEE; HKDF domain labels.
- **Output**: unique key material per device; template encryption keys domain-separated per device.

---

## 16. Risk Mitigation & Fallbacks

**Secure Enclave Unavailable (iOS):**
- Device upgrade required; user notified on first app launch.
- Software keystore fallback available but flagged as lower security; user may decline and reset device.

**StrongBox Unavailable (Android):**
- Software-backed AndroidKeyStore used; user informed.
- Security guarantee degraded (private key potentially exportable by privileged process, though not via app API).
- Risk mitigated by disclosure request integrity verification (counterparty checks E30 Sigsum anchor).

**Network Loss During Disclosure Response:**
- Response queued locally; user sees "Pending" status.
- Retry occurs automatically on network restoration; no user action required.
- If network unavailable >24 hours: user notified; manual retry option provided.

**Biometric Template Corruption:**
- E88 distance evaluation throws error; user prompted to rotate template.
- Recovery: initiate new multi-modal enrollment (Section 4.3); old template marked untrusted.

**Sentinel False Positives:**
- High false-positive rate expected for anomaly detection; user informed that escalations are advisory.
- Recovery workflow (rotate template) always available; user not forced to act.
- Escalation threshold tuned in Phase 4 to balance signal/noise.

---

## 17. Success Criteria & Metrics

**Functional:**
- All T-E89.1 to T-E89.7 acceptance gates pass.
- Disclosure request → response latency <5 seconds on-device (not network-blocked).
- Offline operation: 100 queued responses delivered successfully on network restoration.
- Sentinel: anomalies detected with <10% false-positive rate over 7-day beta soak.

**Performance:**
- Battery: <5% per hour under typical use profile (T-E89.4).
- Memory: resident footprint <30 MB; peak <100 MB.
- Biometric latency: handwriting capture 10–30 seconds; voice 15–45 seconds; inference <8 seconds (iPhone 13+).

**Accessibility:**
- T-E89.7 third-party audit: zero critical violations; ≤2 warning-level deviations.
- VoiceOver / TalkBack: 100% of interactive elements annotated and tested.

**Distribution:**
- iOS App Store: approved and released within 2 weeks of submission.
- Google Play Store: approved and released within 1 week of submission.
- Initial user retention: >70% at 30 days post-launch.

---

## 18. Assumptions & Non-Negotiable Constraints

**Architectural:**
- Native implementation only; no cross-platform framework (React Native, Dart, etc.) due to performance and API access loss.
- Secure Enclave (iOS) and StrongBox (Android) are mandatory for signing keys; software fallback acceptable only for template encryption with user consent + audit logging.
- All predicate evaluation runs on-device; zero server-side trust.
- Biometric capture (handwriting, voice) is optional enrollment; at least one modality required for multi-modal template.

**Functional:**
- No persistent audio/video files; transcripts ephemeral.
- No automatic consent (user must explicitly approve each disclosure).
- No external APIs for predicate evaluation; all logic bundled in-app.
- Offline-first: vault functions without network; sync is optional optimization.

**Scope Boundaries:**
- App does NOT manage user accounts, passwords, or email signup (out of scope; handled by prior identity provisioning).
- App does NOT generate disclosure requests (counterparty responsibility; app only responds).
- App does NOT publish to public blockchains or external ledgers (Sigsum/Roughtime publication is separate infrastructure; see E30).

---

## 19. Signoff & Authority

This Everest establishes institutional follow-through for multi-quarter mobile app development. The specification adheres to Musk discipline: requirements less dumb → delete → simplify → accelerate → automate. No feature bloat; no over-engineering. The bar is surpass, not match. The best part is no part.

Acceptance of this design commits the mobile-team hiring timeline (Section 14), T-E89.1–7 testing gates, and production release to App Store + Play Store within 36 weeks.

**Authored by Calm Witness, 2026-05-20.**

— Musk
