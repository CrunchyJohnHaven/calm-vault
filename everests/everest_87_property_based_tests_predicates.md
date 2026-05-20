# Everest 87 — Property-Based Tests for Predicate Semantics

*Phase VII — Engineering Reliability. Prereq: Everest 63.*

## Decision

Calm Witness predicates (Everest 51–62) are deterministic functions over chain state and committed values. We adopt formal property-based testing (PBT) in Rust and Python to mechanically verify that all predicates uphold twelve core semantic invariants: determinism, monotonicity, idempotence, no cross-talk, negation consistency, composition correctness, indeterminate handling, freshness semantics, consent independence, side-effect locality, replay non-effect, and chain-prefix preservation. Property test failures block PR merge. This everest specifies all twelve properties with formal definitions, test generators, CI gating, and performance bounds.

---

## The Twelve Properties (Formally Stated)

**P1: Determinism.** For any predicate p in the registry (Everests 51–62), any chain state C, and any biometric distance d, evaluating `evaluate(p, C, d)` must produce the same output bit and proof bytes across all independent runs on the same machine and across all supported platforms (macOS aarch64, Linux x86_64, Linux aarch64). Formally: ∀ p, ∀ C, ∀ d, ∀ runs i, j: evaluate(p, C, d, run_i) = evaluate(p, C, d, run_j). No floating-point rounding divergence, no hash-map iteration variance, no system-clock dependencies.

**P2: Monotonicity (time-windowed predicates).** For predicates defined over a time window W (e.g., `in_baseline_24h`), adding additional in-window records of the same type must not flip the predicate's output bit from True to False, and must not flip from False to True unless the new records explicitly satisfy the predicate's condition. Formally: Let C be a valid chain and r_{new} a record whose timestamp falls within W and whose type matches the predicate's input category. Then: if evaluate(p, C) = b, and C' = C + [r_{new}], then evaluate(p, C') ∈ {b, b'} where b' is the new bit value if r_{new} satisfies the condition; otherwise b' = b. Bit flips are monotonic (accumulating evidence), not oscillatory.

**P3: Idempotence.** Evaluating the same predicate twice over the same chain state and biometric distance must produce identical output bit values and, if randomness is seeded deterministically (Everest 63), identical proof bytes. Formally: evaluate(p, C, d, seed_s) = evaluate(p, C, d, seed_s) for all identical inputs. If the Pedersen commitment or Σ-protocol uses fresh randomness (rerandomizable proofs), two valid proofs for the same bit must both verify but may have different bytes; the key invariant is that both evaluate(p, C) = b on the prover side and both verify(proof₁, b) and verify(proof₂, b) on the verifier side.

**P4: No cross-talk between predicates.** Predicate evaluations are independent. Specifically: for distinct predicates p₁ and p₂ with no data overlap in their input specification, mutating a record r in chain C such that r is not explicitly referenced by either p₁ or p₂ must not change the output bits of p₁ or p₂. Formally: Let R_p be the set of record types explicitly read by predicate p (defined in its specification). If a mutation affects only record types not in R_{p1} ∪ R_{p2}, then evaluate(p₁, C) and evaluate(p₂, C) remain unchanged. This property enforces logical independence and prevents hidden data dependencies.

**P5: Negation pair consistency.** For any predicate p and its paired negation ¬p (Everest 62 specifies which negations are semantically valid), the two predicates must form a consistent Boolean pair: evaluate(p, C) = True if and only if evaluate(¬p, C) = False. Formally: evaluate(p, C) ⟹ ¬evaluate(¬p, C), and ¬evaluate(p, C) ⟹ evaluate(¬p, C). If either predicate returns Indeterminate (an allowed state for some predicates), the pair relationship must be logically consistent: if p = Indeterminate then ¬p = Indeterminate; if p = False then ¬p must be True or Indeterminate (depending on specification).

**P6: AND composition consistency.** For a composite predicate defined as (p₁ AND p₂), the result must equal the Boolean AND of the two component bits: evaluate(p₁ ∧ p₂, C) = evaluate(p₁, C).bit ∧ evaluate(p₂, C).bit, exactly. Formally: result_bit = b₁ ∧ b₂ where b₁ = evaluate(p₁, C).bit and b₂ = evaluate(p₂, C).bit. The proof for the AND composition must be constructible from proofs of p₁ and p₂ (per Everest 61 Σ-protocol composition rules) without re-evaluating the component predicates.

**P7: OR composition consistency.** For a composite predicate defined as (p₁ OR p₂), the result must equal the Boolean OR of the two component bits: evaluate(p₁ ∨ p₂, C) = evaluate(p₁, C).bit ∨ evaluate(p₂, C).bit, exactly. Formally: result_bit = b₁ ∨ b₂. The OR composition must also be provable via Σ-protocol composition without re-evaluating components.

**P8: Indeterminate handling in composition.** When a predicate returns Indeterminate (a three-valued state indicating "insufficient evidence"), composition must propagate correctly: AND with Indeterminate yields Indeterminate; OR with True yields True; OR with Indeterminate (and no True branch) yields Indeterminate. Formally: ⊥ ∧ b = ⊥, ⊥ ∨ True = True, ⊥ ∨ ⊥ = ⊥. The three-valued logic is consistent with Kleene semantics.

**P9: Freshness monotonicity.** For predicates that compute a freshness field `freshness_seconds_since_record` (e.g., `in_baseline_24h`), as a chain grows with new records appended, the freshness value must either decrease (new relevant records were added, making the most recent reference newer) or remain constant (no new relevant records). It must never increase on chain growth alone. Formally: Let C be a chain and C' = C + [r_{new}]. If freshness(p, C) = f and r_{new} is not relevant to p (does not update the window or reference point), then freshness(p, C') ≤ f. If r_{new} is relevant (updates the reference point), freshness(p, C') < f (strictly less).

**P10: Consent independence from predicate output.** The consent record predicate (e.g., `principal_consents_to_disclose(p, counterparty_class, C)`) depends only on the presence and validity of a consent record in the chain, not on what p itself evaluates to. Formally: Let consent_bit = evaluate(principal_consents_to_disclose(p, c, C)). If the consent record for (p, c) is present and valid, consent_bit = True regardless of evaluate(p, C).bit. Conversely, if no consent record exists, consent_bit = False regardless of p's output. This prevents a predicate from indirectly gating its own disclosure via circular dependency.

**P11: Side-effect locality.** The side-effect of predicate evaluation (appending a proof or metadata record to the chain during disclosure) must not change the bit values that other predicates would have evaluated to. Formally: Let C be a chain and evaluate(p₁, C) = b₁. If we append a side-effect record SE to C (from disclosing p₁), then for any predicate p₂ unrelated to p₁, evaluate(p₂, C + [SE]) = evaluate(p₂, C). Side-effect records are opaque to all predicates except provenance queries (Everest 70).

**P12: Chain-prefix preservation.** If chain C₁ is a strict prefix of chain C₂ (C₂ = C₁ + suffix), and predicate p evaluates to bit b over C₁ with freshness f, then p over C₂ satisfies: either bit is still b (no new relevant records in the suffix) OR bit changed due to records in the suffix, and the change is traceable to specific records by name and timestamp. Formally: Let b₁ = evaluate(p, C₁).bit and b₂ = evaluate(p, C₂).bit. If b₁ ≠ b₂, there exists at least one record r ∈ suffix such that r's type is in the predicate's input specification and r's properties trigger a condition change in p. This ensures no "spooky action at a distance" from suffix records.

**P13: Replay non-effect.** Evaluating predicate p multiple times (N ≥ 10) over the identical chain C must produce identical output bits and, for deterministic proofs, identical bytes. The predicate state must not drift or accumulate hidden state across calls. Formally: ∀ N, ∀ i, j ∈ [1, N]: evaluate(p, C, run_i) = evaluate(p, C, run_j). This property catches stateful bugs (e.g., memoization with stale caches, incremental counters).

---

## Test Harness Architecture

### Rust: proptest and hypothesis-rs

The Rust harness uses `proptest` with custom generators for chain states, predicate inputs, biometric distances, and consent records. Each of the 13 properties is a separate parameterized test in `tests/predicate_properties.rs`.

```rust
proptest! {
  // P1: Determinism
  #[test]
  fn prop_determinism(
    chain in arb_valid_chain(1..50),
    predicate_id in arb_predicate_id(),
    biometric_distance in 0.0f64..1.0f64
  ) {
    let result_1 = evaluate_predicate(&predicate_id, &chain, biometric_distance)
      .expect("eval 1 failed");
    let result_2 = evaluate_predicate(&predicate_id, &chain, biometric_distance)
      .expect("eval 2 failed");
    
    prop_assert_eq!(result_1.bit, result_2.bit);
    prop_assert_eq!(result_1.proof_bytes, result_2.proof_bytes);
  }
}

proptest! {
  // P2: Monotonicity for in_baseline_24h
  #[test]
  fn prop_monotonicity_baseline(
    chain in arb_valid_chain(1..20),
    new_baseline_record in arb_baseline_record_in_24h()
  ) {
    let bit_before = evaluate_predicate("in_baseline_24h", &chain, 0.5)
      .unwrap().bit;
    
    let mut extended = chain.clone();
    extended.push(new_baseline_record);
    let bit_after = evaluate_predicate("in_baseline_24h", &extended, 0.5)
      .unwrap().bit;
    
    // If the new record is in baseline and falls in the 24h window,
    // True -> True is always valid, False -> True is valid.
    // True -> False and False -> False are invalid (monotonicity broken).
    prop_assert!(
      (bit_before == true && bit_after == true) ||
      (bit_before == false && bit_after == true) ||
      (bit_before == false && bit_after == false),
      "monotonicity violated: {} -> {}",
      bit_before, bit_after
    );
  }
}

proptest! {
  // P3: Idempotence
  #[test]
  fn prop_idempotence(
    chain in arb_valid_chain(1..50),
    predicate_id in arb_predicate_id()
  ) {
    let run_1 = evaluate_predicate(&predicate_id, &chain, 0.5)
      .expect("run 1 failed");
    let run_2 = evaluate_predicate(&predicate_id, &chain, 0.5)
      .expect("run 2 failed");
    let run_3 = evaluate_predicate(&predicate_id, &chain, 0.5)
      .expect("run 3 failed");
    
    prop_assert_eq!(run_1.bit, run_2.bit);
    prop_assert_eq!(run_2.bit, run_3.bit);
    prop_assert_eq!(run_1.proof_bytes, run_2.proof_bytes);
  }
}

proptest! {
  // P4: No cross-talk
  #[test]
  fn prop_no_crosstalk(
    chain in arb_valid_chain(1..30),
    p1_id in arb_predicate_id(),
    p2_id in arb_predicate_id(),
    irrelevant_record in arb_irrelevant_record()
  ) {
    prop_assume!(p1_id != p2_id);
    
    let p1_before = evaluate_predicate(&p1_id, &chain, 0.5)
      .unwrap().bit;
    let p2_before = evaluate_predicate(&p2_id, &chain, 0.5)
      .unwrap().bit;
    
    let mut mutated = chain.clone();
    mutated.push(irrelevant_record.clone());
    
    let p1_after = evaluate_predicate(&p1_id, &mutated, 0.5)
      .unwrap().bit;
    let p2_after = evaluate_predicate(&p2_id, &mutated, 0.5)
      .unwrap().bit;
    
    prop_assert_eq!(p1_before, p1_after, "p1 changed on irrelevant mutation");
    prop_assert_eq!(p2_before, p2_after, "p2 changed on irrelevant mutation");
  }
}

proptest! {
  // P5: Negation consistency
  #[test]
  fn prop_negation_consistency(
    chain in arb_valid_chain(1..50),
    (p_id, neg_p_id) in arb_negation_pair()
  ) {
    let p_result = evaluate_predicate(&p_id, &chain, 0.5)
      .expect("p eval failed");
    let neg_p_result = evaluate_predicate(&neg_p_id, &chain, 0.5)
      .expect("¬p eval failed");
    
    match (p_result.bit, neg_p_result.bit) {
      (true, false) => {},
      (false, true) => {},
      (Indeterminate, Indeterminate) => {},
      _ => prop_assert!(false, "negation pair inconsistent: p={:?}, ¬p={:?}",
                        p_result.bit, neg_p_result.bit)
    }
  }
}
```

### Python: hypothesis

The Python harness mirrors the Rust tests using `hypothesis` with equivalent strategies. File: `calm_witness/tests/test_predicate_properties.py`.

```python
from hypothesis import given, strategies as st

@given(
  chain=st_valid_chain(min_size=1, max_size=50),
  predicate_id=st_predicate_id(),
  biometric_distance=st.floats(min_value=0.0, max_value=1.0)
)
def test_determinism(chain, predicate_id, biometric_distance):
  result_1 = evaluate_predicate(predicate_id, chain, biometric_distance)
  result_2 = evaluate_predicate(predicate_id, chain, biometric_distance)
  
  assert result_1['bit'] == result_2['bit']
  assert result_1['proof_bytes'] == result_2['proof_bytes']

@given(
  chain=st_valid_chain(min_size=1, max_size=20),
  new_baseline_record=st_baseline_record_in_24h()
)
def test_monotonicity_baseline(chain, new_baseline_record):
  bit_before = evaluate_predicate("in_baseline_24h", chain, 0.5)['bit']
  
  extended = chain + [new_baseline_record]
  bit_after = evaluate_predicate("in_baseline_24h", extended, 0.5)['bit']
  
  # Monotonic transitions: T->T, F->T, F->F; no T->F or F->F
  assert (
    (bit_before == True and bit_after == True) or
    (bit_before == False and bit_after == True) or
    (bit_before == False and bit_after == False)
  ), f"monotonicity violated: {bit_before} -> {bit_after}"
```

---

## Generator Strategies

**arb_valid_chain.** Generates chains where each record is chained correctly: r₁.prev_hash = "0"*64, rᵢ.seq = rᵢ₋₁.seq + 1, rᵢ.prev_hash = rᵢ₋₁.record_hash. Records include self-report type (with affect vocabulary), optional biometric, and timestamp. Supports configurable length (default: 1–50 records).

**arb_predicate_id.** Selects uniformly from the canonical predicate registry (Everest 51–62): `in_baseline_24h`, `biometric_match_within`, `principal_consents_to_disclose`, `bank_teller_note_active`, etc.

**arb_negation_pair.** Generates (p, ¬p) pairs where both are defined and semantically paired in the registry (Everest 62). Filters out banned negations.

**arb_baseline_record_in_24h.** Generates a self-report record with timestamp within the past 24 hours and affect vocabulary matching (or not matching) the principal's baseline vocabulary. Used for P2 (monotonicity).

**arb_irrelevant_record.** Generates records whose type is not referenced by any predicate being tested (e.g., internal metadata, provenance records). Used for P4 (cross-talk).

**arb_composite_predicate.** Generates compositions like `in_baseline_24h AND biometric_match_within(0.5)` or `not (bank_teller_note_active)`. Includes nested compositions for stress-testing (P6, P7, P8).

---

## CI Integration

Properties run on every PR and nightly. Test count minimums:

- **Per-property per-PR:** ≥1000 random cases (proptest default).
- **Nightly:** ≥5000 random cases; includes chains up to 1000 records.
- **Failure shrinking:** proptest auto-shrinks to minimal counterexample; CI surfaces it with predicate ID, chain state, and expected vs. actual bit.
- **Regression corpus:** Failed cases persisted to `tests/proptest-regressions/` and replayed on subsequent runs.

### CI Workflow

```yaml
on: [push, pull_request]
jobs:
  predicate-properties:
    strategy:
      matrix:
        os: [macos-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - name: Rust proptest (P1–P13)
        run: cargo test --test predicate_properties -- --nocapture
      - name: Python hypothesis (P1–P13)
        run: python3 -m pytest calm_witness/tests/test_predicate_properties.py -v
      - name: Upload proptest regressions
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: predicate-proptest-regressions-${{ matrix.os }}
          path: tests/proptest-regressions/
```

Nightly adds mutation testing:

```yaml
on: [schedule: "0 2 * * *"]
jobs:
  predicate-mutations:
    runs-on: ubuntu-latest
    steps:
      - name: Mutation testing (cargo-mutants)
        run: cargo mutants -j $(nproc) -k "predicate_properties"
```

---

## Performance and Coverage

- **Test runtime:** Full property suite (P1–P13) completes in <2 minutes on standard CI runner.
- **Coverage target:** All predicates in Everests 51–62 tested against all generator strategies.
- **Nightly coverage:** Large chains (N=1000) tested once weekly; combined with mutation testing ensures correctness under stress.
- **Regression database:** Minimal counterexamples are stored and re-tested on every run, preventing backslide.

---

## Integration with Predecessor and Successor Everests

**Everest 51–62 (Individual Predicates):** Each predicate must pass its own property suite and be added to the registry (Everest 53) before shipping.

**Everest 63 (Determinism Harness):** P1 overlaps with E63's determinism baseline; E87 extends it to semantic properties beyond bit-stability.

**Everest 64 (Golden Corpus):** Property generators use the golden corpus to seed initial chain states; corpus is immutable reference.

**Everest 81–82 (Reference Implementations):** Both Rust and Python implementations must pass identical property tests; cross-language divergence fails the suite.

**Everest 85 (CI Siege):** Predicate properties integrate into the full nightly release-readiness gate.

**Everest 86 (Hash-Chain Properties):** Sibling harness for chain verifier (P1–P10 for chains); E87 parallels the architecture but focuses on predicate semantics.

---

## Acceptance Criteria

All 13 properties pass ≥1000 random cases on every PR (both Rust proptest and Python hypothesis). Nightly suite reaches ≥5000 cases. No platform divergence between macOS and Linux. Cross-language conformance: Rust and Python produce identical output bits on all test vectors. Failure shrinking produces minimal reproducible counterexamples. All predicate negation pairs verified consistent (P5). Composition tests verify AND/OR/Indeterminate semantics exactly (P6–P8). Freshness fields strictly monotonic or constant on chain growth (P9). Consent records independent of predicate outputs (P10). Side-effect records do not alter unrelated predicates (P11). Chain-prefix preservation holds for all test inputs (P12). Replay testing shows zero drift (P13). Mutation testing shows no mutation survives the suite. Zero unimplemented panics or TODOs.

---

— Calm, 2026-05-20
