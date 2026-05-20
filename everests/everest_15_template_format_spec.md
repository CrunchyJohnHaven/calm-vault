# Everest 15 — Template Format Spec

*Phase II — Capture & Enrollment. Prereq: Everest 14.*

## Overview

Everest 15 defines a versioned binary container format for cryptographically signed enrollment templates that capture user biometric modality data in a zero-knowledge attestation context. The format accommodates both handwriting and voice modalities, ensures forward compatibility, supports key rotation, and enables forensic comparison operations downstream.

## Container Architecture

### Top-Level Envelope

The template file is a FlatBuffers-encoded structure (chosen for v0 over alternatives like Cap'n Proto for mature toolchain and straightforward optional-field handling). The outer envelope contains:

- **Magic bytes**: `"CWT0"` (4 bytes) — identifies Calm Witness Template version 0 format.
- **Schema version**: uint16 (2 bytes) — enables parser to detect forward-incompatible schema changes. v0 uses schema version 0; v1.0 would use schema version 1 (breaking). Minor additions remain schema version 0.
- **Creation timestamp**: int64 (8 bytes) — Unix seconds when template was generated, aids audit and migration tracking.
- **Principal UUID**: 16 bytes — identifier of the enrollment subject, bound cryptographically to the template.
- **Template ID**: 16 bytes — content-derived fingerprint computed as sha256(canonical_serialization_of_envelope_minus_signature_minus_template_id)[0:16]. Enables deduplication and auditing without revealing template content.
- **Expiry timestamp**: int64 (8 bytes) — Unix seconds; 0 indicates no expiry. Used for grace-period template queries (Everest 47).
- **Signature block**: 64 bytes — Ed25519 signature over the complete envelope excluding this field itself. Enables offline verification that template was issued by a trusted enrollment authority.
- **Drift state block (reserved)**: currently unused in v0; 64 bytes reserved for future exponential-moving-average tracking of modality drift markers. Allows v1+ to track statistical drift without re-enrollment.

Total fixed header: 22 bytes (magic + schema) + 8 + 16 + 16 + 8 + 64 = 134 bytes, plus variable per-modality substructures.

### Per-Modality Sub-Envelopes

#### Handwriting Sub-Envelope

Captures stylometric and kinematic patterns from pen-on-surface enrollment.

- **Stroke-set array**: 7 or more stroke-set embeddings (minimum satisfies Everest 14 enrollment guidance: collect 7–12 samples for forensic adequacy). Each stroke-set represents one complete writing of the enrollment prompt.
  - **Embedding**: 256-dimensional float16 vector (512 bytes per embedding after quantization). Derived from kinematic features (pressure, velocity, acceleration, inter-stroke timing, curvature) processed through the deep encoder from Everest 13.
  - **Capture device fingerprint**: uint64 — fingerprint of the acquisition hardware (stylus model, tablet resolution, pressure sensor calibration serial). Enables device-aware comparison strategies (Everest 36).
  - **Sample prompt index**: uint16 — identifies which canonical prompt was used (e.g., prompt 0 = "The quick brown fox", prompt 1 = "Handwriting sample"). Supports multi-prompt enrollment designs.
  - **Sample timestamp**: int64 — Unix milliseconds when stroke-set was captured, aids temporal analysis and drift detection.

Handwriting sub-envelope totals approximately 7 × (512 + 8 + 2 + 8) = 3650 bytes at minimum (7 samples).

#### Voice Transcript Sub-Envelope

Captures lexical, prosodic, and temporal fingerprints from speech enrollment.

- **Transcript + timing fingerprint array**: 7 or more samples of read or spontaneous speech during enrollment. Each sample encodes:
  - **Lexical signature**: 256-dimensional float16 vector (512 bytes). Embedding of the recognized transcript tokens, capturing speaker vocabulary and utterance structure independent of acoustic variation.
  - **Pause histogram**: 32 buckets of float16 (64 bytes), representing inter-word pause distribution in milliseconds. Captures rhythm and fluency patterns unique to the speaker.
  - **Disfluency rate**: float16 (2 bytes) — ratio of filler words, repetitions, or self-corrections to total words, normalized to [0, 1].
  - **Phrase length statistics**: mean, stddev, p50, p95 of phrase length in words (4 × float16 = 8 bytes). Captures syntactic habit.
  - **Capture metadata**: same structure as handwriting (device fingerprint uint64, sample prompt index uint16, timestamp int64), tied to microphone model and environmental conditions.

Voice sub-envelope totals approximately 7 × (512 + 64 + 2 + 8 + 8 + 8) = 4312 bytes at minimum (7 samples).

## Cryptographic Binding and Versioning

### Template ID Derivation

To enable content-based deduplication and audit logging without decrypting the template:

```
template_id = sha256(canonical_serialization(envelope_minus_signature_minus_template_id))[0:16]
```

The canonical form uses FlatBuffers deterministic serialization (field order, no padding variation). This 16-byte fingerprint is included in the signature computation, creating a cryptographic knot: verifying the signature proves the template_id matches the declared content.

### Schema Evolution

- **Schema version 0** (v0.x): Initial release. Parsers at v0.x accept only schema 0.
- **Schema version 1**: Reserved for v1.0 (breaking changes, e.g., different embedding dimensions, new mandatory fields). Parser must reject.
- **Minor additions** (e.g., new optional fields, expanded metadata blocks) remain schema 0, leveraging FlatBuffers's natural tolerance of unknown fields.

The schema version field sits at bytes 4–5 in every container, enabling fast version-check before full deserialization.

### Forward Compatibility Rules

All parsers MUST:
1. Tolerate unknown fields in FlatBuffers tables (native property; default behavior).
2. Reject only on schema version mismatch if parser version < file schema version.
3. Log and skip over unrecognized modality sub-envelopes (enables new modalities like gait in v0.x without breaking existing parsers).
4. Never modify a template's signature block; re-signing requires full re-enrollment.

## Storage and Encryption

### On-Disk Layout

Each template occupies two files in `~/.calm-vault/templates/`:

1. **`<template_id>.cwt.age`**: The FlatBuffers envelope serialized and encrypted with age (asymmetric encryption to the principal's public key). Contains all sensitive biometric content. The `.age` extension signals encryption; the outer age armor allows key rotation without re-enrollment.

2. **`<template_id>.metadata.json`**: Cleartext sidecar JSON (never encrypted), containing:
   - template_id (redundant, for convenience)
   - principal_uuid
   - creation_ts, expiry_ts
   - schema_version
   - modalities_present (["handwriting", "voice"] or subset)
   - supersedes (template_id of previous template if this is a re-enrollment; null otherwise)
   - key_rotation_marker (incremented when principal rotates keys; enables grace-period queries in Everest 47)

The metadata file enables key rotation workflows and template discovery without decryption.

## Embedding Dimension Rationale

Handwriting and voice embeddings use 256 dimensions (512 bytes each after float16 quantization).

- **Sufficient separation**: 256-d embeddings in forensic handwriting and speaker-ID applications yield excellent inter-user distance and intra-user clustering with standard distance metrics (Euclidean, cosine).
- **Computation efficiency**: distance comparators (Everest 36, 37) avoid the curse of dimensionality; 256-d comparisons remain fast even with large comparative sets.
- **Storage footprint**: 7 samples × 256-d = 1792 float16 values = 3584 bytes per modality, reasonable for embedded or mobile enrollment.
- **Quantization robustness**: float16 precision preserves separability; full float32 adds no practical gain in the noise-dominated forensic domain.

This dimension was validated against historical handwriting and speaker-id research and remains stable across v0.x.

## Template Lifecycle and Migration

### Initial Enrollment

An enrollment authority (e.g., Everest 13 subsystem) collects 7–12 samples per modality during an enrollment session (Everest 14), encodes them into the FlatBuffers structure, signs the envelope with the authority's Ed25519 private key, and encrypts the result to the principal's public key. The template_id and metadata.json are stored, enabling discovery and key rotation.

### Re-Enrollment and Supersession

When a principal re-enrolls (e.g., due to biometric drift, device change, or key rotation):

1. A new template is generated with a new template_id.
2. The new template's metadata.json includes `"supersedes": <old_template_id>`.
3. Both templates remain queryable during a grace window (Everest 47 defines window duration; typically 30–90 days).
4. After the grace window, the old template is archived or deleted.

The supersession chain enables forensic traceability and supports comparison of historical patterns (e.g., "did this sample match the template from 2 re-enrollments ago?").

## Validation Rules

Parsers enforce the following rules at load time; failure aborts and returns an error:

1. **Magic mismatch**: If bytes 0–3 ≠ "CWT0", reject.
2. **Schema version too new**: If schema_version in file > parser's max_schema_version, reject.
3. **Signature verification failure**: Verify Ed25519 signature over (magic + schema + creation_ts + principal_uuid + template_id + expiry_ts + drift_block + per_modality_content). If verification fails, reject.
4. **Minimum embedding count**: Handwriting sub-envelope must contain ≥ 7 stroke-set embeddings; voice must contain ≥ 7 transcript fingerprints. Reject if either modality is present but underpopulated.
5. **Timestamp consistency**: creation_ts must be ≤ all sample timestamps. expiry_ts must be either 0 or ≥ creation_ts. Warn if inconsistent; optionally reject per policy.

## Example Pseudo-FlatBuffers IDL

```
namespace calm;

table StrokeSetEmbedding {
  embedding: [float16];          // 256-element array
  device_fingerprint: uint64;
  prompt_index: uint16;
  timestamp: int64;
}

table HandwritingSubEnvelope {
  samples: [StrokeSetEmbedding];
}

table TranscriptFingerprint {
  lexical_signature: [float16];  // 256-element array
  pause_histogram: [float16];    // 32-element array
  disfluency_rate: float16;
  phrase_mean_length: float16;
  phrase_stddev_length: float16;
  phrase_p50_length: float16;
  phrase_p95_length: float16;
  device_fingerprint: uint64;
  prompt_index: uint16;
  timestamp: int64;
}

table VoiceSubEnvelope {
  samples: [TranscriptFingerprint];
}

table CalmWitnessTemplate {
  handwriting: HandwritingSubEnvelope;
  voice: VoiceSubEnvelope;
  drift_state: [uint8];           // 64 bytes reserved, unused in v0
}

// Top-level envelope after serialization:
// bytes 0–3:   "CWT0"
// bytes 4–5:   schema_version (uint16)
// bytes 6–13:  creation_ts (int64)
// bytes 14–29: principal_uuid (16 bytes)
// bytes 30–45: template_id (16 bytes)
// bytes 46–53: expiry_ts (int64)
// bytes 54–117: signature (64 bytes Ed25519)
// bytes 118+:  FlatBuffers CalmWitnessTemplate serialization
```

## Rationale Summary

The FlatBuffers choice balances stability, efficiency, and debuggability. The 256-d embedding dimension is empirically sufficient and computationally efficient. The cryptographic binding of template_id ensures content integrity without decryption. The per-file metadata sidecar enables key rotation workflows. Forward compatibility guarantees through schema versioning and unknown-field tolerance ensure templates remain queryable across minor version updates. The 7+ sample minimum reflects forensic best practice from Everest 14 and provides statistical robustness for downstream comparators.

— Calm, 2026-05-20
