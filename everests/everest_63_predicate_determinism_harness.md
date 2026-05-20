# Everest 63 — Predicate Evaluation Determinism Harness

*Phase V — Predicate Authoring. Prereq: Everest 53.*

## The Property

For every predicate P in the registry (Everest 53), for every input I in its golden test corpus, `evaluate(P, I)` MUST return the same bit value on every machine, every operating system, and every run. No exceptions. This property is the foundation on which zero-knowledge proofs for Calm Witness rest: if two parties disagree on the output of a predicate, their proofs cannot both be sound.

## Why Determinism Matters

Calm Witness proofs assert that a specific predicate evaluates to a specific bit against a chain whose head is anchored to a public transparency log. When a counterparty verifies such a proof, they execute the same predicate evaluation and cross-check the result. If the prover's machine and the verifier's machine produce different outputs for the same input—due to floating-point non-determinism, hash-map iteration order, thread scheduling, or system-dependent behavior—the proof either fails to verify when it should succeed, or worse, succeeds when it should fail. Either outcome breaks the security of the protocol.

The determinism harness eliminates this failure mode by running every predicate against a frozen corpus of golden test cases across all supported platforms and asserting bit-stable output. If the harness fails, the build fails and the predicate cannot ship.

## Sources of Non-Determinism and Mitigation

**Floating-point operations.** IEEE 754 floating-point arithmetic is not associative; the order of operations affects the result due to rounding and accumulation of error. Mitigation: predicates MUST use integer arithmetic where possible. Where floating-point is unavoidable (e.g., biometric distance calculations with threshold comparisons), the predicate specification documents the FP types, precision requirements, and rounding direction. Test cases include boundary inputs near threshold values to catch rounding divergence.

**Hash-map iteration order.** Rust's standard `HashMap` uses a random seed by default; iteration order is non-deterministic across runs and machines. Mitigation: predicates MUST use `BTreeMap` (which iterates in key order) or `IndexMap` (which preserves insertion order) instead of `HashMap` for any collection that is iterated or whose elements contribute to the output.

**Thread scheduling and concurrent state.** Predicates MUST evaluate serially within a single thread. If a predicate spawns threads or uses any synchronization primitive (mutex, atomic, channel), the harness rejects it during review (Everest 54). The test suite includes an assertion that predicates are single-threaded: any predicate that calls `thread::spawn`, `rayon`, or async runtimes fails the harness.

**Stable sorting.** When predicates sort collections, they MUST use `.sort_by` (which is guaranteed stable) rather than `.sort_unstable_by`. Test inputs include pre-sorted, reverse-sorted, and randomized sequences to catch unstable-sort bugs.

**System clock and external time.** Predicates MUST NOT call `SystemTime::now()` or any wall-clock function. Time inputs are provided deterministically as part of the predicate input struct. The test corpus injects mock `now` values; predicates read from the input, not the OS. Roughtime (Everest 31) provides the authoritative timestamp for chain-head freshness, separate from predicate evaluation.

**Locale and encoding.** String operations, comparisons, and character classification depend on the process locale. Mitigation: predicates that operate on strings explicitly specify UTF-8 and use locale-independent functions (e.g., `char::is_ascii_digit()` instead of `char::is_numeric()`). Test cases include non-ASCII UTF-8 strings and boundary characters.

## The Harness Implementation

The determinism harness runs in two tiers: language-specific test suites (Rust and Python) and a CI matrix that executes these suites across all target OS+arch combinations.

### Rust Test Harness

File: `calm-witness-rs/tests/determinism.rs`

The Rust harness loads each predicate's test corpus and runs every golden test case in a loop:

```rust
#[test]
fn test_predicate_determinism_across_runs() {
    for predicate_spec in REGISTRY.iter_all_predicates() {
        let test_corpus = load_corpus(&predicate_spec);
        for golden_case in &test_corpus.cases {
            let input = &golden_case.input;
            let expected_output = &golden_case.expected_output;
            
            // Run the predicate N=1000 times on the same input
            for run_index in 0..1000 {
                let output = evaluate_predicate(&predicate_spec, input)
                    .expect(&format!("predicate {} run {} failed", 
                        predicate_spec.id, run_index));
                assert_eq!(
                    output.bit, 
                    expected_output.bit,
                    "predicate {} case {} run {} output mismatch: got {}, expected {}",
                    predicate_spec.id, golden_case.label, run_index, 
                    output.bit, expected_output.bit
                );
            }
        }
    }
}
```

This test ensures in-process, single-machine determinism. The loop count of 1000 is sufficient to detect random-seed variation in hash-based collections (if even one iteration varies, the test fails).

### Python Test Harness

File: `calm-witness-py/tests/test_determinism.py`

The Python harness mirrors the Rust logic, loading predicates from the same registry and running the same golden corpus:

```python
def test_predicate_determinism_parallel():
    registry = PredicateRegistry.load()
    for predicate_spec in registry.iter_all_predicates():
        corpus = load_corpus(predicate_spec)
        for golden_case in corpus["cases"]:
            input_data = golden_case["input"]
            expected_output = golden_case["expected_output"]
            
            # Run N=1000 times
            for run_index in range(1000):
                output = evaluate_predicate(predicate_spec, input_data)
                assert output["bit"] == expected_output["bit"], \
                    f"predicate {predicate_spec.id} case {golden_case['label']} " \
                    f"run {run_index} mismatch"
```

Both test suites use the registry API (Everest 53) to discover predicates and their test corpora, ensuring the harness automatically picks up new predicates as they are added.

### CI Matrix for Cross-Platform Testing

File: `.github/workflows/determinism.yml`

The CI pipeline runs the determinism harness across all supported OS and architecture combinations:

```yaml
on: [push, pull_request]

jobs:
  determinism:
    strategy:
      matrix:
        os: [macos-latest-large, ubuntu-latest, ubuntu-latest-arm64]
        include:
          - os: macos-latest-large
            target: aarch64-apple-darwin   # M-series
            platform_label: macOS-aarch64
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            platform_label: Linux-x86_64
          - os: ubuntu-latest-arm64
            target: aarch64-unknown-linux-gnu
            platform_label: Linux-aarch64
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - name: Run Rust determinism tests
        run: |
          cargo test --test determinism --target ${{ matrix.target }} \
            -- --nocapture --test-threads=1
      - name: Run Python determinism tests
        run: |
          python3 -m pytest calm_witness/tests/test_determinism.py -v \
            --tb=short
      - name: Upload per-platform results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: determinism-results-${{ matrix.platform_label }}
          path: |
            target/determinism-results.json
            calm_witness/determinism-results.json
      - name: Fail if determinism divergence detected
        run: |
          python3 ci/check_determinism_divergence.py \
            calm_witness/determinism-results.json
```

Per-platform results are stored as JSON artifacts. If any platform diverges, the job fails with a detailed diff:

```json
{
  "platform": "Linux-x86_64",
  "predicate_id": "in_baseline_24h/v1.0.0",
  "golden_case": "golden_042.json",
  "expected_bit": true,
  "actual_bit": false,
  "run_number": 847
}
```

### Test Corpus Structure

Each predicate in the registry includes a `test_corpus/` directory. Predicates are authored in Everest 54 (governance); the test corpus is part of the specification:

```
predicates/in_baseline_24h/v1.0.0/
  test_corpus/
    golden_001.json
    golden_002.json
    ...
    golden_100.json
```

Each golden test case is a JSON file with the structure:

```json
{
  "label": "golden_001",
  "description": "baseline affect after normal morning routine",
  "input": {
    "chain_snapshot": {
      "records": [ ... ]
    },
    "parameters": {
      "baseline_affect_vocabulary": ["calm", "focused", "creative"]
    },
    "now": "2026-05-20T10:30:00Z"
  },
  "expected_output": {
    "bit": true,
    "freshness": 3600
  },
  "rationale": "Recent self-report contains 'calm' and 'focused'; both in baseline vocabulary. Predicate outputs true with 1h freshness window."
}
```

The chain snapshot is deterministic: no live clock, no random values. All timestamps are fixed. All random-seed values (if needed by any predicate) are injected via the input, not derived from the system.

## Cross-Language Determinism

The Rust reference implementation and Python reference implementation MUST produce identical output on the same inputs. The harness includes a cross-language conformance test:

```rust
#[test]
fn test_rust_python_conformance() {
    for predicate_spec in REGISTRY.iter_all_predicates() {
        let test_corpus = load_corpus(&predicate_spec);
        for golden_case in &test_corpus.cases {
            // Rust evaluation
            let rust_output = evaluate_predicate(&predicate_spec, &golden_case.input)
                .expect("rust eval failed");
            
            // Python evaluation (via FFI or subprocess)
            let python_output = evaluate_python(&predicate_spec, &golden_case.input)
                .expect("python eval failed");
            
            assert_eq!(
                rust_output.bit, 
                python_output.bit,
                "conformance mismatch: predicate {} case {} (Rust={}, Python={})",
                predicate_spec.id, golden_case.label, 
                rust_output.bit, python_output.bit
            );
        }
    }
}
```

If Rust and Python diverge on any input, the harness fails and flags it as a critical bug.

## Cross-Version Backward Compatibility

As the calm-witness implementation advances (v0.1 → v0.5 → v1.0), predicates must maintain backward compatibility: an older version of the evaluator must produce identical output when given a newer version's test corpus, and vice versa.

The harness tests this by running the test suite against multiple released versions:

```bash
# Test current version against v0.1 golden tests
cargo test --test determinism -Z unstable-options --release
python3 -m pytest calm_witness/tests/test_determinism.py

# Test v0.1 binary against current registry
./bin/calm-witness-v0.1 evaluate --predicate in_baseline_24h/v1.0.0 \
  < test_corpus/golden_001.json > /tmp/v0.1-output.json
assert_eq(cat /tmp/v0.1-output.json, golden_001.expected_output)
```

If a new version breaks backward compatibility, the test fails and a predicate revision PR (Everest 54) is required.

## Predicate Certification for New Language Implementations

When Calm Witness is ported to a new language (Go, TypeScript, etc.), the implementation MUST pass the determinism harness against the canonical test corpus as a certification step:

```bash
# TypeScript implementation
npm test -- --testPathPattern=determinism

# Go implementation
go test -run=TestPredicate ./determinism_test.go

# All must pass with zero output divergence
```

Passing the harness is the "certification badge"; downstream users can trust that the new implementation is compliant.

## Performance: Harness Runtime

The full determinism harness runs in under 5 minutes on a standard CI runner (4 cores, 8 GB RAM):

- Per predicate: ~100 golden cases × 1000 runs = 100,000 evaluations.
- Typical predicates evaluate in <1 ms; full corpus takes ~1 second per predicate.
- With ~50 predicates in v0, full harness = ~50 seconds.
- CI matrix × 3 platforms = ~2.5 minutes total.

For fast feedback during development, engineers can run a subset:

```bash
# Only changed predicates
cargo test --test determinism predicate_id=in_baseline_24h -- --nocapture

# Only first 10 golden cases per predicate (sanity check, <10 seconds)
DETERMINISM_FAST_MODE=1 cargo test --test determinism
```

## Failure Response and Remediation

If the harness detects determinism violation:

1. **CI red.** The PR fails and cannot merge.
2. **Diff report.** The failure message names:
   - Which predicate diverged.
   - Which golden case.
   - Which platform(s) diverged.
   - The specific bit value(s) returned on each platform.
3. **Root-cause investigation.** The developer inspects the predicate implementation for:
   - Unintentional floating-point ops.
   - HashMap usage (should be BTreeMap).
   - Thread spawning or I/O.
   - Locale-dependent string ops.
   - System clock calls.
4. **Fix or revise.** Either:
   - Fix the implementation to eliminate the divergence (patch update, e.g., v1.0.1).
   - Or, if the divergence is legitimate (e.g., a predicate revision adds a new output field), open a new PR for a predicate version bump (v2.0.0) with updated golden tests (Everest 54).

## Integration with Other Everests

**Everest 53 (Predicate Registry):** The determinism harness reads predicates from the canonical registry and uses its test corpus.

**Everest 54 (Governance Audit):** When a new predicate is proposed, the harness is run as part of review. If the proposed predicate fails the harness, it is rejected.

**Everest 64 (Golden Test Corpus):** Defines the structure and authoring standards for test corpora. The determinism harness consumes these.

**Everest 81–82 (Rust and Python Reference Implementations):** These implementations MUST pass the harness on all supported platforms.

**Everest 85 (CI Siege):** The determinism harness integrates into the full nightly CI pipeline and is gated for release.

**Everest 86 (Property-Based Tests for Hash Chain):** Separate harness for chain verifier; complements predicate determinism by testing the evaluation context.

## Acceptance Criteria

All golden test cases pass on all supported platforms (macOS aarch64, Linux x86_64, Linux aarch64). No platform-dependent divergence in any predicate evaluation. Cross-language conformance verified (Rust and Python output byte-identical). All 1000 in-process runs per case succeed without variation. Per-platform results uploaded and compared in CI. Build fails if any divergence is detected. Harness runtime stays under 5 minutes. Determinism also tested for record_hash (chain integrity per E86) and predicate_id derivation (canonical form per E52).

— Calm, 2026-05-20
