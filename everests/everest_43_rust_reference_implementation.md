# Everest 43 — Rust Reference Implementation (biometric stack)

*Phase IV — Biometric Distance Machinery. Prereq: Everest 36, 37, 38.*

---

## 1. Overview

Everest 43 specifies the production-grade Rust reference implementation for the biometric distance and fusion machinery defined in Everests 36 (handwriting kinematic distance), 37 (voice-transcript distance), and 38 (likelihood-ratio fusion). The crate—named `calm-witness-rs`—serves as both a research artifact for protocol validation and the baseline implementation for integration into credential-exchange infrastructure.

This specification establishes crate structure, dependency governance, memory-safety guarantees, cross-platform build matrices, and the public API surface suitable for downstream consumers (enrollment services, verification operators, zero-knowledge provers).

---

## 2. Crate Layout and Module Organization

The `calm-witness-rs` crate follows a modular architecture that separates concerns across handwriting, voice, fusion, and cryptographic commitment layers:

```
calm-witness-rs/
  Cargo.toml                    # Manifest: edition 2021, minimal MSRV (1.70)
  Cargo.lock                    # Pinned dependency versions
  src/
    lib.rs                      # Public module re-exports, root API
    
    handwriting/
      mod.rs                    # Submodule entry
      capture.rs                # Raw event ingestion from E12 hardware
      embed.rs                  # 256-d embedding inference (ONNX)
      distance.rs               # Per-stroke, per-session, DTW
      liveness.rs               # Liveness challenge verification (E49)
    
    voice/
      mod.rs
      asr.rs                    # Whisper.cpp FFI (E13 transcript input)
      embed.rs                  # 432-d to 256-d embedding projection
      distance.rs               # Per-session and aggregation
    
    fusion.rs                   # Likelihood-ratio fusion (E38 core)
    template.rs                 # FlatBuffers serialization and layout
    drift.rs                    # EMA drift modeling (E39)
    commit.rs                   # Pedersen commitments (E44)
    
  tests/
    property/                   # Property-based tests (proptest, E86)
    integration/                # End-to-end enrollment → match scenarios
    golden/                     # Regression suite with fixed test vectors
  
  benches/
    latency.rs                  # Latency regression via criterion
  
  examples/
    simulate_enrollment.rs      # Walkthrough: enroll → capture → match
    compare_samples.rs          # Standalone distance computation
  
  README.md                     # Project orientation
  LICENSE                       # Apache-2.0 header
```

Each module is accompanied by inline documentation (rustdoc comments) explaining thread-safety guarantees, panic safety, and examples. Public types and functions are exhaustively documented.

---

## 3. Dependencies and Auditing

All direct dependencies are widely-used, auditable crates with active maintenance:

**Cryptography and signatures:**
- `ed25519-dalek` (v1.10+): EdDSA signatures for template authentication
- `curve25519-dalek` (v4.0+): Curve25519 scalar arithmetic for Pedersen commitments and Schnorr proofs
- `blake3` (v1.5+): Fast hashing for template integrity
- `sha2` (v0.10+): SHA-256 for additional keying material

**Inference and embeddings:**
- `onnxruntime` (v0.16+): ONNX Runtime C FFI bindings for embedding models (handwriting CNN + Transformer, voice feature projection)

**Serialization:**
- `flatbuffers` (v23.1+): Schema-driven, zero-copy serialization for template storage (E15 format)
- `serde` (v1.0+) and `serde_json` (v1.0+): Auxiliary serialization for configuration and test fixtures

**Cryptographic utilities:**
- `age` (v0.10+): Encryption-at-rest for template files (XChaCha20-Poly1305)
- `rand_chacha` (v0.3+): Deterministic RNG for reproducible tests; `rand` (v0.8+) for nondeterministic enrollment randomness

**Property-based testing:**
- `proptest` (v1.3+): Generative testing for distance function properties (reflexivity, triangle inequality approximation)

**Benchmarking:**
- `criterion` (v0.5+): Statistical regression detection for latency budgets (E42)

All dependencies are locked in `Cargo.lock` for reproducible builds. A `cargo audit` pass (zero advisories) is enforced in CI. Dev-only dependencies (test utilities, example binaries) are marked `dev-dependencies` to avoid runtime bloat.

---

## 4. Concurrency Model

By design, `calm-witness-rs` is **single-threaded**. This decision enforces:

1. **Determinism (E63 harness)**: All computations are strictly deterministic; no thread-local state or racing data accesses.
2. **Memory safety**: mlock'd regions and explicit_bzero operations are unambiguous in a single-threaded context; no cache-coherency or memory-ordering subtleties.
3. **Simplicity**: Complexity in concurrent systems leads to subtle bugs; the threat model (Everest 79) does not require parallelism within a single verification session.

**Async I/O boundary exception:** When fetching remote time proofs (Roughtime) or fetching transcript from a Sigsum log, async is acceptable *only* at I/O boundaries using `tokio` (v1.35+). The bulk of distance computation remains synchronous.

A future optimization (separate crate, E81) may introduce multithreaded enrollment pipelines for bulk calibration; the single-threaded invariant is preserved by pub-sub message passing, not shared mutable state.

---

## 5. Memory Safety and Side-Channel Resistance

The biometric samples and templates are sensitive data. The implementation enforces:

**Protected memory regions:**
- `mlock` via `libsodium`'s `sodium_mlock` (or raw `libc::mlock` on Unix, `VirtualLock` on Windows) for all allocated buffers containing:
  - Raw biometric event sequences (handwriting strokes, voice transcripts)
  - Embeddings (256-d or 432-d vectors)
  - Mahalanobis weight matrices (256×256)
  - Pedersen randomness values
- Regions are unlocked and zeroed atomically on drop via RAII guards (`SensitiveBuffer` type).

**Explicit zeroing:**
- All stack-allocated buffers containing embeddings or samples are explicitly zeroed via `explicit_bzero` (from `zeroize` crate v1.6+) before function return or panic unwinding.
- Panic safety: buffers are held in types implementing `Drop` that zero on both normal and panicked paths.

**Logging discipline:**
- Zero template content, embeddings, or biometric samples appear in log output or error messages.
- Distance values are logged only when committed via Pedersen (commitment is logged, not the distance).

**No template in panics:**
- Panic messages and backtraces are scrubbed of sensitive data (via wrapper types that impl Debug without exposing content).

---

## 6. Build Matrix and CI

The crate targets production deployments across multiple architectures and operating systems. The CI matrix (GitHub Actions) enforces:

**Platforms:**
- macOS aarch64 (M-series: M1, M2, M3)
- macOS x86_64 (legacy Intel)
- Linux aarch64 (ARM64)
- Linux x86_64
- iOS aarch64 (via `cargo-lipo`)
- Android aarch64 (via `cargo-ndk`)

**Per-platform testing:**
- Unit tests: `cargo test --lib`
- Integration tests: `cargo test --test '*'`
- Property tests: proptest suite exercising distance function invariants
- Benchmarks with regression detection: criterion.rs comparing against baseline commit

**Artifact validation:**
- ONNX model files are checksummed (blake3) and validated against committed hashes (Everest 15).
- Binary size checked: stripped release binary <5 MB on typical platforms.
- Dependency license audit: all transitive deps are permissive (MIT, Apache-2.0, BSD-3-Clause).

**Determinism verification (E63):**
- Enrollment and distance computations are run twice with identical inputs; byte-for-byte output match is enforced.

---

## 7. Performance Targets and Budgets

Per Everest 42, the implementation must meet:

**Per-session latency (total: handwriting + voice + fusion):**
- M-series Mac: <2 seconds (typical: 1.2–1.6 s)
- Phone (iOS/Android aarch64): <5 seconds (typical: 3–4 s)

**Breakdown (M-series baseline):**
- Handwriting embedding inference (256-d, ~20 strokes): ~500 ms
- Voice embedding inference (256-d): ~300 ms
- Per-session distance aggregation and fusion: <10 ms
- Pedersen commitment: ~50 ms

**Memory footprint (per session):**
- ONNX model in memory: ~1.2 MB
- Per-session working buffers: O(num_strokes + transcript_length) ≈ 15–30 KB
- Per-principal state (Λ matrix, τ, correlation): ~64 KB cached at enrollment

**Benchmarks:**
- Criterion regression tests are part of CI. Any change degrading per-session latency >5% triggers CI failure unless explicitly approved.

---

## 8. Public API Surface

The library exports a stable, version-controlled API:

```rust
// Enrollment and initialization
pub fn enroll(
    principal_id: &str,
    handwriting_samples: &[HandwritingSample],
    voice_samples: &[VoiceSample],
    config: &EnrollmentConfig,
) -> Result<PrincipalTemplate, EnrollmentError>;

// Handwriting capture and comparison
pub fn capture_handwriting(
    events: &[StrokeEvent],
    device_info: &DeviceInfo,
) -> Result<HandwritingSample, CaptureError>;

pub fn compute_handwriting_distance(
    sample: &HandwritingSample,
    template: &PrincipalTemplate,
) -> Result<Distance, DistanceError>;

// Voice transcription and comparison
pub fn compute_voice_distance(
    transcript: &TranscriptRecord,
    template: &PrincipalTemplate,
) -> Result<Distance, DistanceError>;

// Multimodal fusion
pub fn fuse_distances(
    d_handwriting: Distance,
    d_voice: Distance,
    principal_id: &str,
    template: &PrincipalTemplate,
) -> Result<FusedDistance, FusionError>;

// Biometric match predicate
pub fn biometric_match_within(
    d_fused: FusedDistance,
    template: &PrincipalTemplate,
) -> bool;

// Pedersen commitment
pub fn commit_distance(
    d: &Distance,
    randomness: &Randomness,
) -> Result<PedersenCommitment, CommitmentError>;

// Template serialization
pub fn serialize_template(template: &PrincipalTemplate) -> Result<Vec<u8>, SerializationError>;
pub fn deserialize_template(data: &[u8]) -> Result<PrincipalTemplate, DeserializationError>;
```

All functions are `#[must_use]` where appropriate. Error types are `std::error::Error` implementors with context via `anyhow::Context`. No panics occur for invalid input; all errors are recoverable.

---

## 9. Stability Commitment and Versioning

The crate follows Semantic Versioning (semver):

- **Major version (X.0.0):** Breaking changes to public API, distance function algorithm, or embedding model.
- **Minor version (0.Y.0):** Additive API changes, performance improvements, bugfixes. All 0.Y.* versions are backward compatible in *behavior* (same input → same output); new functions or modules may be added.
- **Patch version (0.0.Z):** Bugfixes and security patches. No semantic changes.

**Stability guarantee:** Distance function output (per E36, E37, E38) is bit-for-bit stable across patch versions within the same minor. If the embedding model is updated, the minor version is incremented, and a parallel crate version (e.g., `calm-witness-rs-v2`) may be published to support old and new models concurrently during transition periods.

---

## 10. Integration Points and Cross-References

Everest 43 serves as the engine for:

- **E14 (Enrollment protocol):** `enroll()` is invoked per principal to create the initial template and calibration tables.
- **E12, E13 (Hardware capture):** `capture_handwriting()` and voice input consume raw events from capture drivers.
- **E15 (Template format):** `serialize_template()` and `deserialize_template()` maintain the FlatBuffers schema and integrity checks.
- **E16 (Encryption at rest):** Template data is encrypted via `age` before file storage; key management is left to the operator (separate from this crate).
- **E36, E37, E38 (Distance functions):** The core algorithms are faithfully implemented; all distance properties (calibration, threshold setting) are preserved.
- **E39 (Drift modeling):** EMA updates to Mahalanobis matrices and thresholds are computed during periodic re-calibration.
- **E40 (FAR/FRR validation):** Testing harness uses reference corpus to generate ROC curves and acceptance metrics.
- **E42 (Latency budgets):** Criterion benchmarks validate sub-second per-session latency.
- **E44 (Pedersen commitments):** `commit_distance()` wraps all disclosed distances.
- **E45 (Risk model):** Threshold adaptation logic is parameterized; per-principal τ reflects downstream risk classification.
- **E49 (Liveness detection):** `liveness.rs` module validates real-time challenge-response before distance computation.
- **E56 (Match predicate):** `biometric_match_within()` is the consumer of fused distances.
- **E63 (Determinism harness):** All computations are deterministic; CI enforces reproducibility.
- **E81 (Production deployment):** This crate is the baseline; production may add multi-threaded wrapper layers or GPU inference (separate).
- **E86, E87 (Property tests):** Proptest suite validates distance function properties (metric axioms, monotonicity, equivalence class transitions).

---

## 11. Development and Testing Workflow

**Local development:**
```
cargo build --release                          # Optimized binary
cargo test                                     # All tests (units, integration, property)
cargo bench                                    # Latency regression
cargo doc --open                               # View rustdoc
cargo clippy -- -D warnings                    # Lint compliance
cargo audit                                    # Security advisory scan
```

**Reproducible builds:**
```
cargo build --release --locked                 # Use pinned Cargo.lock
./scripts/verify_determinism.sh                # Validate bit-for-bit reproducibility
```

**Integration with enrollment service:**
```
# In downstream crate's Cargo.toml:
[dependencies]
calm-witness = { path = "../calm-witness-rs", version = "0.3" }
```

---

## 12. Acceptance Criteria

The reference implementation is accepted when:

1. **Correctness:**
   - Distance functions match Everests 36, 37, 38 to machine precision.
   - Test vectors (golden set) from research codebase pass with <1e-6 relative error.

2. **Performance:**
   - Per-session latency: M-series Mac <2 s, phone <5 s (measured via criterion).
   - Memory peak: <50 MB per session.
   - Model inference time: <2 ms per stroke (handwriting), <500 ms per session (voice).

3. **Security:**
   - No advisories from `cargo audit`.
   - Explicit_bzero and mlock coverage: 100% of sensitive buffers.
   - Zero template content in logs, panics, or error messages.

4. **Compatibility:**
   - Builds and tests pass on all six platform/architecture combinations.
   - ONNX model loader accepts model files from Everest 15.
   - FlatBuffers schema version matches Everest 15 spec.

5. **Stability:**
   - Public API is documented and stable (semver compliance).
   - No breaking changes without major version bump.

---

## 13. Deployment and Release

**Release process:**
1. Tag commit with `v0.Y.Z` on main branch.
2. GitHub Actions publishes to crates.io.
3. Documentation deployed to docs.rs.
4. Binary artifacts (stripped, checksummed) uploaded to releases.io.
5. Security audit (advisory scan) must pass before release.

**Version compatibility matrix:**
- Crate version 0.Y.* → ONNX model version M_Y (updated on minor bump).
- Templates created under crate 0.Y.* are readable by 0.Y'.* where Y' ≥ Y (backward compatibility).

---

— Calm, 2026-05-20
