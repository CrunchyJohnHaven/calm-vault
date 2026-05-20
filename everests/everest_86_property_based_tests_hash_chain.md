# Everest 86 — Property-Based Tests for Hash Chain

*Phase VII — Engineering Reliability. Prereq: Everest 28.*

## Decision

Calm Witness requires absolute confidence in the hash-chain verifier's correctness. We adopt property-based testing (PBT) across Rust and Python to formalize and mechanically verify invariants that the chain construction and verification must uphold. This everest specifies ten formal properties, test harnesses in both languages, generator strategies, CI integration, performance bounds, fuzzing complements, and cross-language conformance vectors.

## The Ten Properties (Formally Stated)

**P1: Append-then-verify.** For any valid chain C = [r₁, r₂, …, rₙ] and any valid record r_{n+1} constructed such that r_{n+1}.prev_hash = rₙ.record_hash and r_{n+1}.seq = rₙ.seq + 1, the sequence append(C, r_{n+1}) shall satisfy verify_chain(append(C, r_{n+1})) = PASS.

**P2: Mutation-breaks-verification.** For any valid chain C and any byte position b in any record rᵢ (except within the record_hash field itself), if we flip one bit at position b, recompute the record_hash for rᵢ, and leave all other records unchanged, then verify_chain(C') shall return FAIL at record i or at the first successor record j > i whose prev_hash no longer matches rᵢ.record_hash.

**P3: Hash-chain link integrity.** For each record rᵢ where i > 1, if rᵢ.prev_hash ≠ r_{i-1}.record_hash, then verify_chain(C) shall return FAIL and identify record i as the failing position. The failure message shall include both stored and computed prev_hash values.

**P4: Genesis anchor.** The first record r₁ must satisfy r₁.prev_hash = "0" * 64 (sixty-four hex zeros). If r₁.prev_hash has any other value, verify_chain(C) shall return FAIL.

**P5: Monotonic seq.** For a valid chain C = [r₁, r₂, …, rₙ], every seq value must satisfy r₁.seq = 1 and rᵢ.seq = r_{i-1}.seq + 1 for all i ∈ [2, n]. Any gap (e.g., rᵢ.seq ≠ r_{i-1}.seq + 1) or duplicate (rᵢ.seq = r_{i-1}.seq) shall cause verify_chain(C) to return FAIL.

**P6: Determinism.** For any fixed chain C and M independent verifier runs (M ≥ 10) on the same input bytes, verify_chain(C) shall return the same result (either PASS or FAIL with identical fault position). No randomness, no race conditions, no external state dependency.

**P7: Record-hash canonicalization.** For any record r with fields {f₁, f₂, …, fₖ}, if we reserialize r using `json.dumps(r \ {record_hash}, sort_keys=True, separators=(",", ":"))` and recompute its hash, the result must be identical to r.record_hash. Conversely, if any field is reordered or any field separator is changed during serialization, the recomputed hash will differ and verify_chain(C) shall FAIL at that record.

**P8: Prefix preservation.** If chain C₁ is a strict prefix of chain C₂ (i.e., C₂ = C₁ + [r_{n+1}, r_{n+2}, …, r_{n+k}]) and verify_chain(C₁) = PASS, then verify_chain(C₂) restricted to the first |C₁| records shall yield the same verified chain head and record_hash values as full verification of C₁.

**P9: Cross-platform canonicalization.** For any record r generated on platform P₁ (macOS) and the same record r on platform P₂ (Linux), the canonical JSON serialization and resulting record_hash shall produce identical byte sequences. Byte-for-byte SHA-256 equality; no platform-dependent floating-point, endianness, or locale artifacts.

**P10: Forward-secrecy of record edits.** For any valid chain C and any record rᵢ where 1 ≤ i < n, if rᵢ is mutated and its record_hash is recomputed, then verify_chain(C) shall fail not only at record i but also at every successor record j > i (because rⱼ.prev_hash will no longer match the new rᵢ.record_hash). There is no way to "patch" the chain by editing record i alone; every downstream record must be recomputed, which is detectable.

## Test Harness Architecture

### Rust: proptest

The Rust harness uses the `proptest` crate to implement QuickCheck-style property testing with automatic shrinking. Each property is a separate test case in `tests/property_tests.rs`.

```rust
// Example structure for P1:
proptest! {
  #[test]
  fn prop_append_then_verify(
    valid_chain in arb_valid_chain(1..10),
    new_record in arb_valid_record_for(&valid_chain)
  ) {
    let mut extended = valid_chain.clone();
    extended.push(new_record);
    prop_assert!(verify_chain(&extended).is_ok());
  }
}
```

### Python: hypothesis

The Python harness uses the `hypothesis` library with equivalent generators and property assertions, running against the v0 stdlib-only verifier in `calm_witness/verify_chain.py`.

```python
# Example structure for P1:
@given(
  valid_chain=st_valid_chain(min_size=1, max_size=10),
  new_record=st_valid_record_chained()
)
def test_append_then_verify(valid_chain, new_record):
  extended = valid_chain + [new_record]
  assert verify_chain(extended) is True
```

## Generator Strategies

**arb_valid_record.** Generates records with all required fields: `seq`, `prev_hash`, payload, `ts`, and `record_hash`. The record_hash is computed correctly using the same canonical-JSON serialization rule as the verifier.

**arb_valid_chain.** Generates a sequence [r₁, r₂, …, rₙ] where r₁.prev_hash = "0" * 64, r₁.seq = 1, and each rᵢ (i > 1) is chained correctly to r_{i-1}. Chain length is bounded by a parameter (default: 0–1000 records).

**arb_adversarial_mutation.** Takes a valid chain and produces a mutated variant by: (1) selecting a random record, (2) flipping exactly one bit in a randomly chosen field (excluding record_hash), and (3) recomputing only that record's record_hash (not downstream records, thus breaking the chain). The mutated chain is expected to fail verification.

**arb_genesis_broken.** Produces a chain where r₁.prev_hash is any value except "0" * 64. Used to test P4.

**arb_seq_gap.** Produces chains with seq discontinuities (gaps, duplicates, or non-monotonic jumps). Used to test P5.

**arb_length_bounded.** Three variants:
- Small: 1–10 records (fast regression on CI).
- Medium: 10–100 records (standard PBT suite).
- Large: 100–10000 records (nightly regression, stress-tests memory and O(1) claims).

## CI Integration

Properties run on every PR and nightly. Test count minimums:

- **Per-property per-PR:** ≥1000 random cases.
- **Nightly:** ≥10000 random cases; includes large (N=10000) chains.
- **Failure shrinking:** proptest shrinks failures to minimal counterexample automatically; CI surfaces this in the failure report.
- **Regression corpus:** Failed test cases are persisted to `tests/proptest-regressions/` and replayed on subsequent runs, ensuring no regression.

### CI Workflow

```yaml
on: [push, pull_request]
jobs:
  property-tests:
    runs-on: [ubuntu-latest, macos-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Rust proptest (P1–P10)
        run: cargo test --test property_tests -- --nocapture
      - name: Python hypothesis (P1–P10)
        run: python3 -m pytest calm_witness/test_properties.py -v
      - name: Upload proptest regressions
        uses: actions/upload-artifact@v2
        if: always()
        with:
          name: proptest-regressions
          path: tests/proptest-regressions/
```

Nightly adds fuzzing and larger-scale runs:

```yaml
on: [schedule: "0 2 * * *"]
jobs:
  fuzz-and-stress:
    runs-on: ubuntu-latest
    steps:
      - name: Cargo fuzz (libFuzzer + corpus)
        run: cargo +nightly fuzz run chain-parser -- -max_len=100000 -jobs=4
      - name: Mutation testing (cargo-mutants)
        run: cargo mutants -j $(nproc)
```

## Performance Bounds

All performance tests run on both platforms (macOS, Linux) and are gated to PR merge:

- **Append latency p99:** < 5ms per record (single-threaded, no I/O).
- **Verify latency (N=1000):** < 100ms total (streaming verifier, O(1) memory overhead).
- **Memory regression:** `verify_chain` uses O(1) extra heap beyond input size (streaming, not load-whole-chain).

Performance test harness (Rust + Criterion):

```rust
#[bench]
fn bench_append_latency(b: &mut Bencher) {
  let chain = gen_chain(100);
  let new_record = gen_record_for(&chain);
  b.iter(|| chain.append(new_record.clone()));
}

#[bench]
fn bench_verify_1000_records(b: &mut Bencher) {
  let chain = gen_chain(1000);
  b.iter(|| verify_chain(&chain));
}
```

## Complementary Fuzzing

Property testing covers logical invariants; fuzzing covers byte-level chaos and parser robustness. The fuzz target is the chain-parser entry point:

```rust
#[cfg(fuzzing)]
pub fn fuzz_chain_parser(data: &[u8]) {
    let _ = parse_chain(data);
    // Parser must not panic, OOM, or exhibit undefined behavior
}
```

Fuzzing runs in nightly CI with libFuzzer, accumulates coverage corpus in `.cargo/fuzz/corpus/chain-parser/`, and surfaces any crash or timeout to the team.

## Mutation Testing

`cargo-mutants` runs in nightly to verify that our property tests actually catch implementation bugs. If a mutation passes all property tests, the test suite is insufficient; we strengthen the properties or generators.

Mutation testing gates the "ready for release" signal.

## Cross-Language Conformance

The Python reference parser (from Everest 26) and the Rust reference parser run on the same generated chain inputs. For each chain C:

- Rust: `verify_chain(C)` → result₁, chain_head₁
- Python: `verify_chain(C)` → result₂, chain_head₂
- Assert: result₁ = result₂ and chain_head₁ = chain_head₂ (byte equality)

This is the conformance vector set; it runs in CI on every PR. Zero tolerance for cross-language divergence.

## Phase Plan

**Phase A (Week 1):** P1, P2, P3, P4, P5 in Rust proptest. Generator strategies for valid chains and adversarial mutations. Basic CI gate.

**Phase B (Week 2):** P6, P7, P8 in both Rust and Python. Determinism tests, canonicalization vectors, prefix-preservation checks. Cross-language conformance harness.

**Phase C (Week 3):** P9, P10 + cross-platform testing (macOS + Linux). Mutation testing integration. Performance benchmarking gate.

**Phase D (Week 4):** Fuzzing corpus, nightly regression, final readiness audit. Integration with Everest 85 (CI siege).

## Edge Cases & Boundary Tests

- **Empty chain:** Expected to fail (genesis record mandatory). Test that rejection is explicit.
- **Single-record chain:** Only genesis, no successors. Valid if r₁.prev_hash = "0" * 64 and r₁.seq = 1.
- **Max-length chain:** N = 10000 records. Verify within time and memory bounds (P5: monotonic seq across 10k records).
- **seq overflow:** seq = 2³²−1 (max u32). Next record would overflow; test rejection.
- **Canonical JSON edge cases:** Unicode normalization, null bytes in payload, deeply nested JSON, large integers, special IEEE-754 floats. All must round-trip through canonical serialization with byte equality.

## Deliverables

- `tests/property_tests.rs` — Rust proptest suite for P1–P10.
- `calm_witness/test_properties.py` — Python hypothesis suite for P1–P10.
- `tests/proptest-regressions/` — Regression corpus (auto-managed by proptest).
- `.github/workflows/property-tests.yml` — CI gate (PR + nightly).
- `benches/chain_perf.rs` — Performance criterion harness.
- `.cargo/fuzz/fuzz_targets/chain_parser.rs` — libFuzzer target.
- Documentation in this file and inline test comments (no separate architecture doc).

## Composition with Later Summits

- **Everest 28 (Hash-Chain Verifier):** This summit proves the core verifier correct.
- **Everest 43 (Rust Reference Implementation):** Cross-language conformance vectors ensure byte-identical results.
- **Everest 85 (CI Siege):** Property tests integrate into the full CI pipeline and nightly stress suite.
- **Everest 87 (Predicate Property Tests):** Separate property harness for Calm Witness predicates (in_baseline, biometric_match, etc.); uses similar architecture but different invariants.

## Acceptance Criteria

All ten properties pass ≥1000 random cases on every PR. Nightly suite reaches ≥10000 cases on large chains. Minimal counterexample shrinking is active (proptest default). Cross-language conformance is zero-variance (byte equality on all test vectors). Performance benchmarks show no regression >5% week-over-week. Mutation testing shows no mutation survives the suite. Fuzzing corpus accumulates without crash or timeout. Zero TODOs or unimplemented panics.

— Calm, 2026-05-20
