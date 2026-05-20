# Everest 88 — Proof-Generation Performance Budget

*Phase VII — Engineering Reliability. Prereq: Everest 81.*

## Executive Summary

End-to-end zero-knowledge proof generation must complete within 1 second on M-series Mac hardware and 3 seconds on phone-class devices. This document establishes the performance budget across all cryptographic components, defines measurement methodology, and specifies regression detection and optimization techniques.

## M-Series Mac Budget: 1 Second End-to-End

The proof-generation pipeline must complete within a hard boundary of 1000 milliseconds on standardized M-class hardware (M1/M2/M3 series). This accounts for the full cycle from predicate evaluation through serialization and operator signature.

### Per-Component Breakdown

**Predicate Evaluation: ≤50ms**

Predicate evaluation reads the results of biometric evaluation and applies conditional logic without re-running biometric matching. The biometric evaluation itself (Everest 42) runs once during proof initialization at approximately 350ms; this cost is amortized across all proofs sharing that identity evaluation within a session. The 50ms budget for predicate evaluation covers: reading cached biometric results, evaluating match-within thresholds, constructing selective disclosure masks, and preparing input to commitment generation.

**Pedersen Commitments: <5ms per commitment**

Each predicate generates one commitment. Typical proofs use 1–4 commitments depending on disclosure granularity. Pedersen commitment construction is a fixed-time scalar multiplication; at <5ms per commitment, a four-predicate proof consumes no more than 20ms total.

**Bulletproof Range Proofs: 30–50ms each (Everest 45)**

Range proofs are the primary cryptographic burden after biometric evaluation. Each selective disclosure predicate requires one Bulletproof to prove a value lies within acceptable range (e.g., biometric_confidence ∈ [0.95, 1.0]). The 30–50ms range reflects platform variation; Bulletproof generation via curve arithmetic scales predictably. Four proofs in a worst-case selective disclosure consume 200ms.

**Schnorr Equality Proofs: ~10ms each**

Equality proofs link commitments across predicates and demonstrate that the same value was committed in multiple forms. A four-predicate disclosure requires up to four equality proofs (10ms each = 40ms total).

**Aggregation: ~20ms**

Combining multiple proofs into a single compact object (merging commitments, deduplicating common references) takes approximately 20ms at typical proof cardinality.

**Chain Anchor Lookup: ~5ms**

Proof validity requires a reference to the on-chain operator state snapshot at time of proof generation. Lookup from operator-side cache adds ~5ms.

**Operator Signature: ~1ms**

The operator signs the complete proof package with its long-term key. Signature generation is negligible compared to proof construction.

**Serialization: ~5ms**

Converting the proof structure to wire format (protobuf or JSON) takes approximately 5ms.

### Worst-Case Scenario: Four-Predicate Selective Disclosure with Biometric Match-Within

The most demanding typical workload combines four selective disclosure predicates with biometric_match_within evaluation:

- Biometric evaluation: 350ms (first proof only; subsequent proofs in session amortize this)
- 4 × Bulletproof range proofs: 4 × 50ms = 200ms
- 4 × Schnorr equality proofs: 4 × 10ms = 40ms
- Aggregation: 30ms
- Chain anchor lookup + operator signature + serialization: 10ms
- **Total: ~630ms**

This result sits comfortably within the 1000ms budget, leaving 370ms for platform variance, network jitter, and unforeseen operations.

### Amortization Within Sessions

Biometric evaluation is the highest-cost single operation at ~350ms. Within a user session, the biometric result is cached after the first proof. Subsequent proofs using the same biometric data reference the cached result, reducing the amortized cost to the 50ms predicate-evaluation budget. A session generating 5 proofs with shared biometric data consumes approximately 50ms + 4×(350ms + 400ms) = 3450ms total, or 690ms amortized per proof.

## Phone-Class Device Budget: 3 Seconds End-to-End

Mobile devices (iOS/Android running Rust via Flutter bindings or native bridging) typically exhibit 2–3× slower cryptographic performance due to CPU clock rate and instruction set constraints. The phone budget is set at 3 seconds end-to-end.

Using the same component ratios:
- Biometric evaluation: 700–1050ms
- 4 × Bulletproof: 240–300ms
- 4 × Schnorr proofs: 40ms
- Aggregation: 40ms
- Serialization + signature: 20ms
- **Total: ~1040–1450ms**

This remains within the 3000ms budget. Mobile implementations must prioritize: pre-computation of fixed-base multiplication tables, SIMD acceleration via portable_simd where available, and batch proof generation to reduce per-proof overhead.

## Performance CI and Regression Detection

Every pull request that modifies cryptographic operations, commitment generation, or proof serialization must run a standardized benchmark suite on CI hardware.

**Benchmark Specification**
- Hardware: Mac mini M2 (uniform baseline)
- Test: 100 iterations of each operation (predicate evaluation, Bulletproof generation, aggregation, full end-to-end proof)
- Metrics: p50, p95, p99 latency; heap peak memory
- Regression threshold: > 10% slowdown on p50 blocks the PR

**Metrics Tracked**
- Per-component breakdown (each Bulletproof, each Schnorr proof, aggregation)
- End-to-end proof generation (single proof)
- End-to-end with session amortization (5 consecutive proofs)
- Memory profile: peak heap usage, steady-state working set

**Failure Modes**
- p50 latency increase > 10%
- p99 latency > 1200ms on M-series
- Peak memory > 120MB
- Throughput drop below 5 proofs/sec sustained

CI failures trigger a mandatory performance review before merge. If regression is justified by feature addition, the budget baseline is explicitly updated with justification in commit message.

## Optimization Techniques

When profiling reveals component bottlenecks, the following techniques reduce latency without compromising security:

**Pre-Computed Scalar Multiplication Tables (Fixed-Base)**

Bulletproof and Pedersen commitment generation involve scalar multiplication against fixed generators. Pre-computing lookup tables for common base points (e.g., the canonical generator G) eliminates repeated arithmetic, reducing per-proof time by 15–20%.

**Batch Range Proofs**

Selective disclosure with multiple predicates can merge range proofs under certain conditions (e.g., range proofs for related bounds on similar values). Batching reduces witness size and proof-generation cost by 10–15% in cases with 3+ proofs.

**SIMD Acceleration via portable_simd**

The portable_simd crate enables SIMD-friendly curve arithmetic on platforms that support it (x86-64, ARM64). Vectorizing scalar multiplication reduces latency by 20–30% on supported hardware without sacrificing portability.

**Operator-Side Commitment Caching**

The operator may cache Pedersen commitments for frequently used reference values (e.g., biometric_confidence_bounds, issued_date) with appropriate privacy controls (only cache on private operator hardware, not in shared state). Retrieving a cached commitment costs <1ms versus generating it on-the-fly (~5ms), saving ~4ms per proof in high-volume scenarios.

## Memory Budget

**Peak Memory: < 100 MB**

During proof generation, intermediate witness values, Bulletproof transcript, and serialization buffers must stay below 100MB peak usage. A four-predicate proof typically uses 50–70MB at peak.

**Steady-State: < 30 MB**

The cached biometric evaluation and per-session proof state consume approximately 20–30MB steady-state.

Implementations must profile heap usage on phone-class devices and establish regression checks: any PR that increases peak memory by >20% requires justification.

## Throughput and Rate-Limiting

The operator must support concurrent proof-generation requests while maintaining QoS.

**Sustained Throughput: ≤ 10 proofs/sec**

A single operator instance can generate and validate up to 10 proofs per second sustained without queue buildup. This assumes ~100ms amortized per proof under typical conditions (session-cached biometric).

**Burst Capacity: 50 proofs in 5 seconds**

Short bursts up to 50 proofs in 5 seconds are accepted. Beyond this rate, the operator applies token-bucket rate-limiting (Everest 76).

## Cross-References and Dependencies

This budget builds on and references:

- **E36**: Commitment scheme security and zero-knowledge properties
- **E37**: Selective disclosure logic and mask generation
- **E38**: Operator state snapshots and chain anchors
- **E42**: Biometric evaluation performance baseline (350ms on M-series)
- **E44**: Schnorr proof construction and verification
- **E45**: Bulletproof range proof construction and performance (30–50ms)
- **E46**: Proof serialization format (protobuf/JSON efficiency)
- **E65**: Predicate ZK proof generator (proof assembly orchestration)
- **E76**: Rate-limiting and queue management
- **E81**: Cryptographic operation security and test harness (prereq)
- **E85**: Operator infrastructure and scaling
- **E89**: Mobile performance budget and lower-performance-tier guidance
- **E90**: Audit preparation and performance data retention

Everest 81 (cryptographic operation test harness and security validation) is a prerequisite; proof-generation performance cannot be validated without a robust testing infrastructure.

## Conclusion

This budget establishes aggressive but achievable targets: 1 second on M-series hardware, 3 seconds on mobile. The per-component breakdown provides clear optimization targets, and the CI regression detection ensures performance is monitored continuously. Biometric evaluation amortization, pre-computation tables, and SIMD acceleration enable headroom for feature additions without breaching the budget. Success requires discipline in code review (no unexplained performance deltas) and investment in mobile profiling to ensure phone-class targets remain achievable as the codebase evolves.

— Calm, 2026-05-20
