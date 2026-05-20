# Everest 145 — Alignment Reference Implementation

*Phase X — Values Alignment Computation. Prereq: Everest 140.*

## Overview

Everest 145 delivers an open-source reference implementation for bilateral values alignment proofs within the Calm ZKAC system. This work materializes the alignment predicate infrastructure specified in Everest 140, shipping production-grade Rust + Python bindings with a command-line interface for end-to-end alignment workflows. The deliverable includes performance telemetry, comprehensive test coverage, and integration pathways into the Calm Witness deployment stack for live demonstration.

## Workspace Architecture

The repository adopts a crate-based structure with clear separation between cryptographic primitives, alignment logic, Python interop, and user-facing tooling:

```
calm-zkac/
  crates/
    calm-zkac-rs/                # main library (Phase X alignment)
    calm-zkac-values-rs/         # ValuesVector + commitments (Phase IX)
    calm-zkac-harm-rs/           # harm predicates (Phase XI)
    calm-zkac-cooperation-rs/    # cooperation predicates (Phase XII)
    calm-zkac-cli/               # CLI binary
  python/
    calm_zkac/                   # PyO3-bound Python wrapper
  tests/
    integration/
    property/
  benches/
    alignment.rs
    composition.rs
```

This layout enables incremental feature gating (Phase XI and XII predicates ship as optional modules), maintains clear dependency boundaries, and isolates platform-specific concerns for mobile deployment targets.

## Public API Surface

The primary library (`calm-zkac-rs`) exposes six major modules:

```rust
pub mod values;       // ValuesVector, commit_values, parse
pub mod predicate;    // evaluate per-predicate
pub mod align;        // bilateral alignment proof
pub mod compose;      // Pact + Witness + ZKAC three-handshake
pub mod registry;     // predicate / dimension registry client
pub mod serialize;    // serde + flatbuffers + age encryption
```

### values
Handles representation and commitment of values vectors. Exports `ValuesVector` (in-memory representation), `commit_values()` for VC generation, and parsers for both binary and JSON formats. Integrates with the Phase IX values commitment substrate.

### predicate
Evaluates individual alignment predicates against pairs of values vectors. Each predicate implements a `Predicate` trait with deterministic evaluation semantics. Predicates are indexed by dimension identifier and retrieved from the central registry client.

### align
Implements the bilateral alignment proof protocol. Exports `AlignmentRequest` (counterparty query), `AlignmentProof` (operator response), and proof generation/verification logic. Proofs incorporate witness commitments, cryptographic proof material, and metadata for audit trails.

### compose
Orchestrates the three-handshake protocol: Pact announcement → Witness deployment → ZKAC alignment proof. Handles negotiation, state transitions, and artifact sequencing. Integrates with the Calm Witness deployment specified in Everest 99.

### registry
Client library for the predicate registry service. Supports both local registry fallback (static definitions) and remote registry lookup (live predicate updates). Caches registry entries with staleness bounds.

### serialize
Serialization backends including serde for JSON/bincode interchange, flatbuffers for compact on-wire representation, and age for envelope encryption. Supports both symmetric and public-key encryption modes.

## Cryptographic Dependencies

The implementation carries forward the audited dependency set established in Everest 81:

- **curve25519-dalek** + **bulletproofs** — core zero-knowledge proof construction
- **ed25519-dalek** — signature verification for witness commitments
- **calm-witness-rs** — Calm Witness library (proof assistant, state machine)
- **serde** — serialization framework
- **flatbuffers** — efficient binary serialization
- **age** — authenticated encryption

All dependencies undergo continuous auditing via RustSec feed. Security advisory responses follow the SemVer policy established in Everest 82.

## Quality Assurance

The codebase meets the quality bar established across the Everest program:

**Memory Safety**
- Enforced via `#![forbid(unsafe_code)]` at crate root. No unsafe blocks outside FFI boundaries (Python interop).
- MIRI testing on nightly Rust for undefined behavior detection.

**Test Coverage**
- Target: >90% line coverage across all public APIs.
- Coverage reported via tarpaulin on CI and published in release notes.
- Integration tests exercise end-to-end alignment workflows (request → prove → verify).
- Property tests using proptest validate mathematical properties of alignment functions.

**Determinism Assurance**
- Alignment proofs produce byte-identical output across multiple runs on identical inputs (following E63 / E187 methodology).
- Determinism harness runs proof generation 100 times per test case and verifies output equality.
- Seeded RNG for all randomized operations (nonce generation, salting).

**Fuzzing**
- Fuzz targets for alignment proof deserialization (following E85 harness framework).
- Fuzz targets for predicate registry parsing.
- libFuzzer integration in CI; OSS-Fuzz submission for community fuzzing.

**Platform Matrix**
- CI matrix: macOS-aarch64, macOS-x86_64, Linux-x86_64, Linux-aarch64, iOS (via XCFramework), Android (via ndk).
- Architecture-specific tests validate alignment proof semantics on all platforms.
- Determinism harness runs on all platforms to ensure bit-reproducible output.

## Python Bindings

PyO3-based bindings enable both production usage and research-notebook compatibility:

**Production Bindings (`calm-zkac` on PyPI)**
- Direct FFI to Rust alignment library; near-native performance.
- Type annotations for static analysis.
- Async support for I/O-bound registry lookups.
- Published to PyPI with wheels for macOS, Linux, iOS simulator (development).

**Pure-Python Reference (`calm_zkac.python_impl`)**
- Portable implementation using standard library + cryptography crate.
- Used in research notebooks, education, and slow-path fallback.
- Maintains API parity with PyO3 bindings; both are drop-in compatible.

Both implementations are tested against the same integration suite; equivalence is verified by property tests.

## Command-Line Interface

The `calm-zkac-cli` binary provides operator and counterparty tooling:

```bash
calm-zkac values commit <vector.json> \
  --output commitments.json \
  --registry-url <registry>
```
Generate value commitments from a vector definition.

```bash
calm-zkac align request <counterparty_vc> <target.json> <weights.json> \
  --output request.json
```
Construct an alignment request specifying target values, predicate weights, and counterparty VC.

```bash
calm-zkac align prove <request.json> \
  --output proof.json \
  --registry-url <registry>
```
Generate a bilateral alignment proof on the operator side.

```bash
calm-zkac align verify <proof.json> \
  --counterparty-vc <vc>
```
Verify a proof on the counterparty side and report alignment metrics.

```bash
calm-zkac compose run-three-handshake <peer> \
  --pact-url <pact> \
  --witness-url <witness> \
  --output handshake-result.json
```
Execute the full three-handshake: Pact announcement, Witness deployment, ZKAC alignment proof. Produces a composite artifact with proof + witness state + attestation.

All CLI commands support `--registry-url` for remote registry lookup, `--registry-local` for local fallback, and `--timeout` for operation bounds.

## Performance Targets

Everest 145 targets performance thresholds derived from Everest 140, Everest 88, and Everest 89:

- **Single alignment proof generation**: <5 seconds on M-class hardware (macOS-aarch64).
- **Alignment proof verification**: <1 second.
- **Three-handshake end-to-end**: <13 seconds (Pact + Witness + ZKAC sequential).
- **Memory peak during proof**: <100 MB.

Benchmarks are tracked via criterion.rs; performance regression is detected automatically in CI. Benchmark results are published with each release.

## Documentation

All public items carry rustdoc with worked examples and panic conditions. Documentation is structured as follows:

**API Documentation**
- Each module includes an overview of its role in the alignment pipeline.
- Public types document their serialization format (JSON schema, flatbuffers) and any platform-specific constraints.
- Functions include examples covering the happy path and common error cases.

**End-to-End Examples**
- Comprehensive example showing a full alignment flow: values commit → request → proof → verification.
- CLI walkthrough matching documented command signatures.
- Python notebook example for research workflows.

**Integration Guide**
- Procedures for embedding alignment logic into applications.
- Registry client integration (local vs. remote).
- Error handling and retry strategies.

**Deployment Notes**
- Security considerations (registry trust model, proof freshness).
- Performance tuning (registry caching, parallel verification).

Documentation builds cleanly on docs.rs; intra-doc links are verified in CI.

## Versioning and Release Policy

The crate uses semantic versioning with the following progression:

- **v0.1.0-rc**: Release candidate; feature-complete, under final validation.
- **v0.5.0-beta**: Beta after wave testing against Calm Witness (Everest 99) and initial predicate registry population (Everest 140).
- **v1.0.0**: General availability after Phase XIII specification finalization (Everest 215).

Breaking changes to public APIs trigger minor version bumps until v1.0.0; thereafter, semver is strict. Maintenance releases are supported for v1.0.0 and one prior major version.

## Open-Source Release

The reference implementation is released under the Apache License 2.0 and hosted at:

```
https://github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-zkac
```

The repository includes the full source, test suite, benchmarks, and CI configuration. Releases are signed; checksums are published alongside artifacts.

## Integration with Calm Witness

Everest 145 composes directly with the Calm Witness deployment specified in Everest 99. The alignment proof serves as input to the witness state machine; the witness commitment is embedded in the alignment proof for audit trails. Joint testing verifies that proof generation on the operator side and proof verification on the counterparty side remain synchronized with the witness state.

## Cross-References

This work builds on and incorporates findings from:

- **Everest 81**: Calm Witness Rust production implementation (carries forward cryptographic substrate).
- **Everest 82**: Dependency and supply-chain security audit framework.
- **Everest 83, 84, 92**: Cryptographic proof validation and composition.
- **Everest 85**: Fuzzing harness and undefined-behavior detection.
- **Everest 122, 130**: Predicate infrastructure and registry design.
- **Everest 140**: Alignment performance budget and predicate evaluation semantics (prerequisite).
- **Everest 143**: Harm predicate specification (Phase XI, optional in E145).
- **Everest 195**: Compass open-source release (parallel effort, shared CI infrastructure).

## Success Criteria

Everest 145 is bagged upon:

1. Reference implementation source complete, audited, and merged to main branch.
2. All public APIs documented with examples; docs.rs builds clean.
3. Test coverage >90%; property tests and determinism harness pass on full CI matrix.
4. Performance telemetry published: alignment proof <5s, verification <1s, three-handshake <13s.
5. Python bindings (PyPI `calm-zkac`) and pure-Python reference distributed.
6. CLI binary functional end-to-end (values commit, align request/prove/verify, three-handshake).
7. Integration tests against Calm Witness (Everest 99) passing.
8. Release v0.1.0-rc tagged and checksums published.

— Calm, 2026-05-20
