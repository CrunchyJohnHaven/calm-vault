# Everest 81 — Rust Production Implementation

*Phase VII — Engineering Reliability. Prereq: Everest 43, 65.*

---

## 1. Overview

Everest 81 specifies the production-grade Rust crate workspace that consolidates the full Calm Witness implementation stack into a single, deployable artifact matching the zkac_v0 quality bar. This is not a research reference implementation; it is the canonical production build for operators, counterparty agents, and downstream credential-exchange infrastructure.

The `calm-witness` workspace integrates:
- Biometric distance computation (Everest 43: handwriting, voice, fusion)
- Zero-knowledge proof generation (Everest 65: Bulletproofs, Σ-protocols, Schnorr)
- Hash-chained user-state log (Everest 26, 28: append, verify, snapshot)
- Freshness anchoring via Sigsum and Roughtime (Everest 30, 31)
- Vault management and encryption at rest (Everest 16, 32, 33)
- Enrollment ceremony orchestration (Everest 11, 14)
- Disclosure request/response flow
- Command-line interface for operators

The acceptance criterion is a Rust crate ecosystem with zero `unsafe` (except cryptographic FFI boundaries), >90% test coverage, property-based testing via proptest, determinism harness integration, CI across six platforms, and documentation suitable for docs.rs publication.

---

## 2. Workspace Structure

```
calm-witness/
  Cargo.toml                      # Workspace root (version 0.1.0-rc1)
  Cargo.lock                      # Pinned reproducible builds
  
  crates/
    calm-witness-rs/              # Main library: public API root
    calm-witness-zk-rs/           # ZK primitives: proofs, verification
    calm-witness-chain/           # JSONL chain: append, verify, anchor
    calm-witness-template/        # FlatBuffers: biometric template serialization
    calm-witness-distance/        # Biometric distance: handwriting, voice, fusion
    calm-witness-anchors/         # Sigsum + Roughtime: freshness proofs
    calm-witness-vault/           # Vault mgmt: storage, encryption, cleanup
    calm-witness-enroll/          # Enrollment ceremony: multi-phase orchestration
    calm-witness-cli/             # Binary: operator CLI
    calm-witness-types/           # Shared types: errors, codecs, constants
  
  scripts/
    ci/
      verify_determinism.sh       # Bit-for-bit reproducibility harness
      coverage.sh                 # Test coverage thresholds (>90%)
      audit.sh                    # cargo audit, dependency scan
      bench_regress.sh            # Criterion latency gate
    dist/
      build_release.sh            # Strip, checksum, sign binaries
      publish_crates.sh           # crates.io publication
  
  docs/
    ARCHITECTURE.md               # Design overview, module graph
    SECURITY.md                   # Threat model, mitigation strategies
    TESTING.md                    # Test categorization, examples
    BUILD_AND_DEPLOY.md           # CI/CD, release checklist
  
  .github/
    workflows/
      ci.yml                      # GitHub Actions matrix
      coverage.yml                # codecov integration
      release.yml                 # Pre-built binary distribution
```

---

## 3. Public API Surface

The root crate `calm-witness-rs` re-exports a stable, versioned API:

```rust
pub mod chain;       // append, verify, snapshot, anchor binding
pub mod predicate;   // register, evaluate, query predicates
pub mod prove;       // generate_proof, proof_bundle serialization
pub mod verify;      // verify_proof, counterparty verification
pub mod disclose;    // request_predicate, respond_with_proof, consent flow
pub mod enroll;      // enrollment_ceremony, certificate issuance
pub mod vault;       // open, lock, list_records, cleanup
pub mod anchor;      // refresh_sigsum, refresh_roughtime, verify_freshness
pub mod biometric;   // distance, commit, template management (re-export from distance crate)
pub mod types;       // Error, ProofBundle, VaultRecord, all public types
pub mod constants;   // algorithm parameters, thresholds, windows
```

No `use crate::*` exports; all modules are explicitly namespaced. Every public item has rustdoc with examples. Error types implement `std::error::Error` and are exhaustively documentable.

---

## 4. Workspace Crate Descriptions

### calm-witness-rs (root library)

**Purpose:** Public API surface, integration point, re-exports.

**Key modules:**
- `lib.rs`: Root entry, public module tree.
- `version.rs`: Version constant (matches Cargo.toml).
- `integration_tests/`: End-to-end disclosure workflows.

**Dependencies:** All workspace crates (path dependencies), plus curve25519-dalek, serde, anyhow.

**Coverage:** >95% (integration-heavy).

### calm-witness-zk-rs (cryptographic proofs)

**Purpose:** Bulletproofs, Σ-protocols, Schnorr, Fiat-Shamir transcripts.

**Key modules:**
- `circuit_def.rs`: Parse, validate, cache circuit definitions from registry.
- `atomics/bulletproof.rs`: RangeProof wrapper (distance < tau).
- `atomics/schnorr.rs`: EqualityProof (template, chain-head, consent bindings).
- `atomics/sigma_set.rs`: MembershipProof (OR-composition for deniability).
- `generator.rs`: ProofGenerator orchestrator (E65 §7).
- `verifier.rs`: ProofVerifier, offline verification.
- `fiat_shamir.rs`: Transcript rolling-hash protocol.
- `bundle.rs`: ProofBundle serde codec (bincode + size limits).
- `anchor.rs`: Sigsum inclusion proof binding.

**Dependencies:** bulletproofs, curve25519-dalek, sha2, blake3, serde, bincode, calm-witness-types.

**Coverage:** >90% (cryptographic operations unit-tested; property tests via proptest for Fiat-Shamir transcript invariants).

**No unsafe:** Bulletproofs crate is all-safe Rust. Curve25519-dalek is all-safe Rust. FFI boundary: none in this crate.

### calm-witness-chain (JSONL chain)

**Purpose:** Append-only log, chain-of-custody, Sigsum anchoring.

**Key modules:**
- `append.rs`: Append record with prev_hash (BLAKE3), return new head.
- `verify.rs`: Verify chain from genesis to current head (hash-chain correctness, no branches).
- `snapshot.rs`: Export chain segment with Merkle proof.
- `anchor.rs`: Publish chain head to Sigsum, receive inclusion proof.
- `inmemory.rs`: ChainStore trait; impl for tests.
- `filestore.rs`: ChainStore impl using JSONL (prod).

**Dependencies:** serde_json, blake3, calm-witness-anchors, calm-witness-types.

**Coverage:** >90% (property tests: reflexivity of hash chains, deterministic head after append).

**No unsafe.**

### calm-witness-template (FlatBuffers serialization)

**Purpose:** Biometric template binary format (schema-driven, zero-copy).

**Key modules:**
- `schema.rs`: FlatBuffers schema definition (Rust code generation).
- `template.rs`: PrincipalTemplate codec (serialize, deserialize).
- `validate.rs`: Schema validation, version checks.

**Dependencies:** flatbuffers, serde, blake3.

**Coverage:** >90% (golden test vectors from E15 spec).

**No unsafe:** FlatBuffers safe bindings.

### calm-witness-distance (Everest 43 implementation)

**Purpose:** Handwriting, voice, biometric distance, fusion.

**Key modules:**
- `handwriting/capture.rs`: Event ingestion (Everest 12).
- `handwriting/embed.rs`: CNN embedding (ONNX inference).
- `handwriting/distance.rs`: DTW, per-session aggregation.
- `voice/asr.rs`: Whisper.cpp FFI wrapper.
- `voice/embed.rs`: Feature projection (256-d).
- `voice/distance.rs`: Transcript distance.
- `fusion.rs`: Likelihood-ratio fusion (Everest 38).
- `drift.rs`: EMA re-calibration.
- `commit.rs`: Pedersen commitment to distance.

**Dependencies:** onnxruntime, curve25519-dalek, rand, mlock (via libsodium), zeroize.

**Coverage:** >90% (property tests: distance reflexivity, triangle inequality approximation; golden vectors from research codebase).

**Unsafe:** `mlock`/`munlock` via libc on Unix; minimal, audited.

**Side-channel resistance:** All buffers holding embeddings explicitly zeroed on drop; no template content logged.

### calm-witness-anchors (Sigsum + Roughtime)

**Purpose:** Freshness anchoring, public-transparency-log integration, time proofs.

**Key modules:**
- `sigsum.rs`: Client for Sigsum log (append, get, verify inclusion).
- `roughtime.rs`: Roughtime protocol (fetch time proofs).
- `proof.rs`: Anchor proof serialization and verification.
- `cache.rs`: Local caching of tree heads and time proofs (age-limited).

**Dependencies:** tokio, reqwest, sha2, serde_json, calm-witness-types.

**Coverage:** >90% (mocked Sigsum/Roughtime for unit tests; integration tests use public staging logs).

**Async boundary:** I/O only (network fetches).

### calm-witness-vault (Everest 16, 32, 33)

**Purpose:** Local encrypted storage, key derivation, cleanup.

**Key modules:**
- `vault.rs`: Vault trait; open, lock, list_records, cleanup.
- `local_store.rs`: On-disk JSONL + age encryption.
- `key_derivation.rs`: PBKDF2 from principal passphrase.
- `sealing.rs`: Envelope (principal_id, permissions, expiry).
- `cleanup.rs`: Zero stale records, audit log rotation.

**Dependencies:** age, rage, sha2, zeroize, calm-witness-types.

**Coverage:** >90% (property tests: decryption round-trips; golden test vectors for key derivation).

**Unsafe:** None.

### calm-witness-enroll (Everest 11, 14)

**Purpose:** Multi-phase enrollment ceremony, template creation, certificate issuance.

**Key modules:**
- `ceremony.rs`: State machine (Unauthenticated → Capture → Verification → Issued).
- `phases/capture.rs`: Collect biometric samples (handwriting + voice).
- `phases/verify.rs`: Distance thresholds, FAR/FRR validation.
- `phases/issue.rs`: Create PrincipalTemplate, issue enrollment certificate.
- `consent.rs`: Consent record registration.

**Dependencies:** calm-witness-distance, calm-witness-template, calm-witness-chain, calm-witness-types.

**Coverage:** >90% (property tests: state-machine transitions valid; no bypasses).

**No unsafe.**

### calm-witness-cli (binary)

**Purpose:** Operator command-line interface.

**Subcommands:**
```
calm-witness enroll --principal-id <id>      # Ceremony orchestration
calm-witness disclose --predicate <p>        # Generate proof
calm-witness verify <proof.json>             # Verify bundle
calm-witness chain snapshot --since <time>   # Export chain segment
calm-witness vault lock --principal <id>     # Encrypt, close
calm-witness anchor refresh                  # Fetch Sigsum/Roughtime proofs
```

**Dependencies:** clap, serde_json, calm-witness-rs (root).

**Binary size (release, stripped):** <8 MB on x86_64.

**No unsafe.**

### calm-witness-types (shared codecs)

**Purpose:** Canonical error types, enums, constants.

**Exports:**
- `Error` enum (ProofError, VaultError, ChainError, etc.).
- `ProofBundle`, `VaultRecord`, `ChainRecord` type definitions.
- Constants: WINDOW_24H_SECONDS, BIOMETRIC_MATCH_THRESHOLD, etc.

**Dependencies:** serde, thiserror.

**Coverage:** >95% (error construction tests).

**No unsafe.**

---

## 5. Memory Safety and Determinism

### Forbid Unsafe

```rust
#![forbid(unsafe_code)]
```

Applied to every crate **except**:
- `calm-witness-distance`: libc::mlock for template buffers (audited, minimal).
- Any FFI boundary for ONNX Runtime or cryptographic libraries (bulletproofs, curve25519-dalek are all-safe Rust; no unsafe needed).

All sensitive buffers (embeddings, distance values, randomness) are wrapped in `SensitiveBuffer` (RAII, zero on drop).

### Determinism Harness (E63)

**Script:** `scripts/ci/verify_determinism.sh`

```bash
#!/bin/bash
set -e

# Build twice with identical environment
cargo build --release --locked -p calm-witness-rs
cp target/release/libcalm_witness.rlib /tmp/run1.rlib

cargo clean
cargo build --release --locked -p calm-witness-rs
cp target/release/libcalm_witness.rlib /tmp/run2.rlib

# Byte-for-byte comparison
if cmp -s /tmp/run1.rlib /tmp/run2.rlib; then
    echo "PASS: Determinism verified"
    exit 0
else
    echo "FAIL: Non-deterministic output detected"
    exit 1
fi
```

Applied to:
- Proof generation (same witness → same proof bytes).
- Biometric distance computation (same sample → same distance).
- Chain verification (same chain → same head hash).

---

## 6. Build Matrix and CI

**GitHub Actions workflow:** `.github/workflows/ci.yml`

Platforms tested per commit:
- macOS aarch64 (M-series)
- macOS x86_64 (Intel)
- Linux aarch64 (ARM64)
- Linux x86_64
- iOS aarch64 (via cargo-lipo for `--lib` only; no binary)
- Android aarch64 (via cargo-ndk for `--lib` only)

Per-platform matrix:
1. `cargo build --release --all --locked`
2. `cargo test --all --locked`
3. `cargo test --all --locked --release` (property tests with more iterations)
4. Property-based test suites (proptest with 1000+ cases per property).
5. Fuzz targets (via cargo-fuzz; example: `fuzz_chain_verify`, `fuzz_proof_bundle_decode`).
6. `cargo clippy -- -D warnings` (deny all lints).
7. `cargo audit` (zero advisories).
8. Coverage report (codecov integration, >90% threshold).
9. Determinism harness on macOS aarch64.
10. Criterion regression tests (latency budgets per Everest 42).

**Artifacts published:**
- Stripped release binaries for calm-witness-cli (macOS, Linux).
- Checksummed (blake3) and signed (GPG).
- Published to GitHub Releases.

**crates.io publication:**
- Triggered on git tag `v0.Y.Z`.
- Requires all CI to pass.
- docs.rs build must succeed.

---

## 7. Testing Strategy

### Unit Tests (per module)

Every module has a `#[cfg(test)] mod tests { ... }` block with:
- Constructor invariant checks.
- Error path coverage (invalid inputs, out-of-bounds, corruption).
- Round-trip serialization (encode → decode → original).
- Golden test vectors (fixed, checked-in test data).

### Integration Tests

Placed in `tests/` directories:
- **disclosure_flow.rs:** Full end-to-end (enroll → capture → disclose → verify).
- **chain_workflow.rs:** Append, verify, snapshot, anchor, re-verify.
- **vault_workflow.rs:** Open, store record, lock, decrypt, cleanup.
- **multimodal_biometric.rs:** Handwriting + voice fusion, distance computation.

### Property-Based Tests (proptest)

`tests/property/`:
- **distance_properties.rs:** Distance functions satisfy metric axioms (reflexivity, triangle inequality, symmetry approximations).
- **fiat_shamir_properties.rs:** Transcript rolling-hash deterministic and collision-resistant.
- **chain_properties.rs:** Hash-chain append + verify is idempotent; no spurious rejects.

### Fuzz Targets (cargo-fuzz)

`fuzz/`:
- `fuzz_chain_verify.rs`: Corrupted chain records → reject or log.
- `fuzz_proof_bundle_decode.rs`: Malformed proof bundles → error, never panic.
- `fuzz_biometric_distance.rs`: Out-of-range embeddings → handled gracefully.

### Determinism Tests (E63)

`tests/determinism/`:
- Enroll principal twice with same inputs → identical template.
- Generate proof twice with same operator state → identical proof bytes.
- Verify chain head twice → identical result.

### Benchmarks (Criterion)

`benches/`:
- `biometric_latency.rs`: Handwriting + voice + fusion, per-session end-to-end.
- `proof_generation.rs`: Single-predicate and multi-predicate proof generation.
- `chain_append_verify.rs`: Chain operations (append, verify, snapshot).
- `vault_encrypt_decrypt.rs`: Encryption, decryption latency.

Criterion output compared against baseline commit; >5% regression triggers CI failure (unless explicitly approved).

---

## 8. Performance Budgets (Everest 42, 88)

**Per-session latency (handwriting + voice + fusion + proof):**
- M-series Mac: <3 seconds (typical: 2–2.4 s)
  - Handwriting embed: 500 ms
  - Voice embed: 300 ms
  - Fusion: 10 ms
  - Proof generation: 500 ms
  - Sigsum anchor: 200 ms
  - Serialization + signature: 50 ms
- Phone (iOS/Android aarch64): <6 seconds

**Memory per session:**
- ONNX model in memory: 1.2 MB
- Working buffers: 15–30 KB
- Proof bundle serialized: ~2 KB
- Peak heap: <100 MB

**Proof verification (stateless, counterparty):**
- Single proof: <10 ms (Bulletproof verify, Schnorr verify, Sigsum anchor verify in parallel).
- Four proofs (typical disclosure): <50 ms.

---

## 9. Dependencies (Audited Shortlist)

**Cryptography:**
- `curve25519-dalek` (v4.0+): Schnorr, commitments.
- `bulletproofs` (v0.12+): Range proofs.
- `sha2` (v0.10+): Fiat-Shamir, hashing.
- `blake3` (v1.5+): Fast chain hashing.
- `ed25519-dalek` (v1.10+): Operator identity signatures.

**Serialization:**
- `flatbuffers` (v23.1+): Template format.
- `serde` (v1.0+), `serde_json` (v1.0+), `bincode` (v1.3+): Codecs.

**Encryption:**
- `age` (v0.10+): XChaCha20-Poly1305 envelope.
- `rand_chacha` (v0.3+): Deterministic RNG for tests.

**Inference:**
- `onnxruntime` (v0.16+): Embedding models (C FFI, safe Rust bindings).

**Testing:**
- `proptest` (v1.3+): Generative property tests.
- `criterion` (v0.5+): Benchmarking.

**Async I/O:**
- `tokio` (v1.35+): Sigsum/Roughtime fetches only.

**CLI:**
- `clap` (v4.0+): Argument parsing.

**Utilities:**
- `anyhow` (v1.0+): Error context.
- `thiserror` (v1.0+): Error types.
- `zeroize` (v1.6+): Explicit zeroing.

All locked in `Cargo.lock`. Transitive dependencies must have permissive licenses (MIT, Apache-2.0, BSD-3-Clause, ISC). `cargo audit` must pass (zero advisories).

---

## 10. Documentation

**Public API:** Comprehensive rustdoc on every public item. Every function has:
- Short description.
- Preconditions (if any).
- Panics (if any; we minimize panics for invalid input — prefer `Result`).
- Errors (all error variants documented).
- Example code (runnable, idiomatic).

**Module-level docs:** Architecture, module purpose, invariants, cross-references.

**Examples in source:**
- `examples/enroll.rs`: Full enrollment ceremony walkthrough.
- `examples/disclose.rs`: Proof generation and verification.
- `examples/chain_workflow.rs`: Chain append, verify, anchor.

**docs.rs:** Generated from Cargo.toml metadata; builds pass CI.

**ARCHITECTURE.md:** High-level design, crate dependency graph, threat model summary, integration points.

**SECURITY.md:** Per-module memory-safety guarantees, side-channel mitigations, threat model (Everest 79), adversary assumptions.

**TESTING.md:** Test categorization, coverage metrics, how to run property tests and fuzz, benchmark baselines.

**BUILD_AND_DEPLOY.md:** CI setup, reproducible builds, release checklist, binary signing, crates.io publication.

---

## 11. Version and Stability

**Versioning:** Semantic versioning per Everest 92.

- **v0.1.0-rc1** (current): Release candidate; public API subject to change before 1.0.0.
- **v0.5.0-beta1**: Beta; feature-complete; minor API polish.
- **v1.0.0 GA**: Stable API, long-term support commitment.

**Stability guarantee:** Within a minor version (0.Y.*), public API is stable; behavior is deterministic (same input → same output, across patch versions). Distance function, proof generation, chain verification output is locked per minor version.

**Backward compatibility:** Templates created under calm-witness v0.Y.0 are readable by v0.Y'.* where Y' >= Y. Proof bundles signed under v0.Y.0 verify under v0.Y'.* (signature format immutable).

---

## 12. Cross-References

This specification integrates and consolidates:
- **Everest 11:** Enrollment ceremony (calm-witness-enroll).
- **Everest 12, 13:** Hardware capture drivers (calm-witness-distance interfaces).
- **Everest 14:** Enrollment protocol state machine (calm-witness-enroll).
- **Everest 15:** FlatBuffers template schema (calm-witness-template).
- **Everest 16, 32, 33:** Vault encryption and lifecycle (calm-witness-vault).
- **Everest 26, 28:** Chain append and verify (calm-witness-chain).
- **Everest 30, 31:** Sigsum and Roughtime anchoring (calm-witness-anchors).
- **Everest 36, 37, 38:** Biometric distance (calm-witness-distance).
- **Everest 42:** Latency budgets (criterion benchmarks, CI gates).
- **Everest 43:** Reference biometric implementation (calm-witness-distance realization).
- **Everest 44, 45, 46:** Commitments and range proofs (calm-witness-zk-rs).
- **Everest 63:** Determinism harness (scripts/ci/verify_determinism.sh).
- **Everest 65:** ZK proof generation (calm-witness-zk-rs realization).
- **Everest 79:** Threat model (SECURITY.md summary).
- **Everest 81:** Self.
- **Everest 82:** Post-deployment observability and logging (separate crate, calm-witness-observe).
- **Everest 85, 86, 87:** Fuzz targets, property tests (fuzz/, tests/property/).
- **Everest 88, 89:** Performance budgets and monitoring (Criterion, CI regression gates).
- **Everest 92:** Semantic versioning and stability (above).

---

## 13. Acceptance Criteria

The workspace is accepted when:

1. **Correctness (E36, E37, E38, E65):** All distance and proof functions match research specifications to machine precision. Golden test vectors pass <1e-6 relative error. Proof verification succeeds for honest proofs; rejects corrupted bundles deterministically.

2. **Performance (E42, E88):** Per-session latency <3 s (M-series), <6 s (phone). Memory peak <100 MB. Proof latency <500 ms. All criterion benchmarks pass; >5% regression triggers failure.

3. **Coverage:** >90% line coverage. All public APIs tested. Edge cases (invalid input, corruption, abort paths) covered. Coverage report published to codecov.

4. **Security:** `cargo audit` zero advisories. No `unsafe` outside FFI boundaries (audited, minimal). All sensitive buffers explicitly zeroed. Zero template or biometric content in logs, panics, error messages. Determinism harness passes (bit-for-bit reproducibility).

5. **Compatibility:** Builds and tests pass on all six platform/architecture combinations (macOS aarch64, x86_64; Linux aarch64, x86_64; iOS, Android). ONNX model loader accepts E15 format. FlatBuffers schema matches spec.

6. **Documentation:** Every public item has rustdoc with example. docs.rs build clean. ARCHITECTURE.md, SECURITY.md, TESTING.md, BUILD_AND_DEPLOY.md complete. Integration examples runnable.

7. **CI/CD:** GitHub Actions workflow green on all commits. Pre-built binaries published to releases. crates.io publication succeeds. Dependencies locked in Cargo.lock.

8. **Fuzzable:** All parsers (chain, proof bundle, template, vault record) fuzzed. No panics on malformed input; graceful error paths.

---

## 14. Deployment

**Pre-deployment checklist:**
- [ ] All CI passing (six platforms, property tests, fuzz, coverage >90%).
- [ ] `cargo audit` passes (zero advisories).
- [ ] Determinism harness passes.
- [ ] Release notes prepared.
- [ ] Binary checksums (blake3) computed and signed (GPG key pinned in repo).

**Publication flow:**
1. Tag commit with `v0.Y.Z`.
2. GitHub Actions builds release binaries, publishes to Releases.
3. Automated publish to crates.io.
4. Documentation published to docs.rs.
5. Release notes posted (GitHub, announcements).

**Version compatibility during transitions:**
- Parallel crate versions (calm-witness-v1, calm-witness-v2) can coexist during model or algorithm updates (Everest 92).
- Old templates remain readable by newer crates (backward compatibility).

---

— Calm, 2026-05-20
