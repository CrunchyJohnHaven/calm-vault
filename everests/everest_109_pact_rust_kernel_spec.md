# SUMMIT 109/300 (CP-09) — Pact Rust Crypto Kernel Implementation Spec

*Phase P-II — Cryptographic kernel. Status: SPEC BAGGED (not implementation).*

**Acceptance for THIS summit (the spec):** a Rust expert can implement the kernel from this document alone, with no further protocol questions, and have their output pass the conformance vectors.

**Acceptance for the kernel itself** (separate summit when written): byte-identical output to `calm_witness/conformance_vectors.py` and `calm_compass/conformance_vectors.py` on the published inputs.

---

## §1. Why this is too hard for a single Opus 4.7 1M pass

Writing real Pedersen + Schnorr-Σ + Bulletproofs in Rust requires:
- Careful constant-time scalar/point operations (timing-attack class).
- Independent generator derivation with provable no-trapdoor property.
- Bulletproofs inner-product argument implemented against a curve API.
- PyO3 bindings that don't leak references or break GIL invariants.
- ≥3 days of focused engineering by a cryptography-fluent Rust developer.
- Validation against an existing reference (e.g., `bulletproofs` crate or `dalek-cryptography`'s test vectors).

A single LLM pass cannot deliver this safely. This spec is the substrate for that future engineering.

## §2. Crate layout

```
calm-vault/
  calm-witness-rs/
    Cargo.toml
    src/
      lib.rs              -- public API
      pedersen.rs         -- commit / verify / batch-verify
      sigma.rs            -- Schnorr-style equality + membership proofs
      bulletproofs.rs     -- range proof + sum-of-committed-values range proof
      hash_to_curve.rs    -- deterministic generator derivation
      ffi.rs              -- PyO3 bindings
      conformance.rs      -- runs the published conformance vectors
    tests/
      conformance_test.rs
      timing_test.rs      -- empirical constant-time check
```

## §3. Dependency pins (must match `~/credex/research/fermis/communications/zkac-v0/Cargo.toml`)

```toml
curve25519-dalek = { version = "4.1.3", features = ["alloc", "rand_core", "digest", "precomputed-tables"] }
ed25519-dalek    = { version = "2.2.0", features = ["alloc", "rand_core", "zeroize"] }
frost-ed25519    = { version = "3.0.0" }
sha2             = { version = "0.10.9" }
halo2_proofs     = { version = "0.3.2" }
rand_core        = { version = "0.6.4" }
subtle           = { version = "2.6.1" }
hex              = { version = "0.4.3", features = ["alloc"] }
pyo3             = { version = "0.21", features = ["abi3-py39", "extension-module"] }
```

Cross-crate consistency: same versions as `zkac-v0` so the two artifacts can share dependency graph nodes without conflict at link time.

## §4. The Pedersen layer (`pedersen.rs`)

### 4.1 Generators

```rust
/// Base generator: the standard Ristretto basepoint.
pub fn g() -> RistrettoPoint { RistrettoPoint::generator() }

/// Pedersen "no trapdoor" generator. Derived from a fixed domain-separation
/// tag via SHA-512 then hash-to-curve (Elligator2). Verifier MUST recompute.
const H_DOMAIN: &[u8] = b"calm-witness-pedersen-h-v0";

pub fn h() -> RistrettoPoint {
    RistrettoPoint::from_hash::<Sha512>(H_DOMAIN)
}
```

Validation: `log_g(h)` must be unknown. The Elligator2 hash-to-curve ensures this when the domain string is independent of `g`'s generator structure.

### 4.2 Commit / verify

```rust
pub struct Commitment(pub CompressedRistretto);

/// Com(value; randomness) = value * g + randomness * h
pub fn commit(value: &Scalar, randomness: &Scalar) -> Commitment {
    let p = value * g() + randomness * h();
    Commitment(p.compress())
}

/// Verify (open) a commitment against the claimed (value, randomness).
pub fn open(c: &Commitment, value: &Scalar, randomness: &Scalar) -> Choice {
    commit(value, randomness).0.ct_eq(&c.0)
}
```

Wire format: 32 bytes compressed. Matches placeholder width in Python ref.

### 4.3 Homomorphic aggregation (Compass uses this)

```rust
pub fn add_commitments(a: &Commitment, b: &Commitment) -> Commitment {
    let pa = a.0.decompress().expect("invalid commitment");
    let pb = b.0.decompress().expect("invalid commitment");
    Commitment((pa + pb).compress())
}

pub fn aggregate(commitments: &[Commitment]) -> Commitment {
    commitments.iter().skip(1).fold(commitments[0].clone(),
        |acc, c| add_commitments(&acc, c))
}
```

## §5. The Sigma layer (`sigma.rs`)

### 5.1 Equality proof (Calm Pact P-II core)

Prove `Com_A` and `Com_B` commit to the same value, without revealing the value or either randomness.

```rust
pub struct EqualityProof {
    pub a: CompressedRistretto,   // r' * h
    pub e: Scalar,                 // Fiat-Shamir challenge
    pub z: Scalar,                 // r' + e * (r_a - r_b)
}

pub fn prove_equality(
    com_a: &Commitment, com_b: &Commitment,
    value: &Scalar, r_a: &Scalar, r_b: &Scalar,
    rng: &mut impl RngCore,
) -> EqualityProof {
    let r_prime = Scalar::random(rng);
    let a = (r_prime * h()).compress();
    // Fiat-Shamir over (a, com_a, com_b)
    let e = fiat_shamir_challenge(&[a.as_bytes(), com_a.0.as_bytes(), com_b.0.as_bytes()]);
    let z = r_prime + e * (r_a - r_b);
    EqualityProof { a, e, z }
}

pub fn verify_equality(com_a: &Commitment, com_b: &Commitment, proof: &EqualityProof) -> Choice {
    let lhs = (proof.z * h()).compress();
    let delta = (com_a.0.decompress().unwrap() - com_b.0.decompress().unwrap()).compress();
    let rhs = (proof.a.decompress().unwrap() + proof.e * delta.decompress().unwrap()).compress();
    lhs.ct_eq(&rhs)
}
```

Wire format: 96 bytes (3 × 32).

### 5.2 Membership proof (Calm Witness predicate-value commitment)

The committed value is one of `{0, 1, 2, 3}` (= false / true / unknown / refused). Use the standard OR-of-Σ-protocols (Cramer-Damgård-Schoenmakers, EUROCRYPT 1994).

```rust
pub struct MembershipProof {
    /// One branch per allowed value; only the real branch is honest.
    pub branches: [SigmaBranch; 4],
}

pub fn prove_membership(actual: u8, randomness: &Scalar, ...) -> MembershipProof { ... }
pub fn verify_membership(com: &Commitment, proof: &MembershipProof) -> Choice { ... }
```

## §6. The Bulletproofs layer (`bulletproofs.rs`)

### 6.1 Range proof (Calm Witness E45)

```rust
pub struct RangeProof(pub Vec<u8>);  // ~672 bytes

/// Prove value ∈ [0, 2^64) without revealing value.
pub fn prove_range_64(
    value: u64, randomness: &Scalar,
    pp: &PublicParams, rng: &mut impl RngCore,
) -> (Commitment, RangeProof) {
    // Use existing `bulletproofs` crate or implement inner-product argument
    // directly using curve25519-dalek per Bunz-Bootle-Boneh-Poelstra-Wuille-Maxwell.
    todo!()
}

pub fn verify_range_64(c: &Commitment, proof: &RangeProof, pp: &PublicParams) -> Choice { ... }
```

### 6.2 Sum-of-committed-values range proof (Calm Compass CC-31)

The Compass aggregator emits one aggregate commitment + one threshold range proof. The range proof is over the aggregate value (homomorphically summed) compared to the threshold.

```rust
pub fn prove_aggregate_above_threshold(
    per_record_values: &[i64],
    per_record_randomness: &[Scalar],
    threshold: i64,
    pp: &PublicParams, rng: &mut impl RngCore,
) -> (Commitment, RangeProof) { ... }
```

This is the construction in `CALM_COMPASS_PROTOCOL_v0.md` §4. The reference Python aggregator (`calm_compass/aggregator.py`) emits placeholder bytes of the correct width; the Rust kernel emits real bytes that satisfy the published conformance vectors.

## §7. PyO3 bindings (`ffi.rs`)

```rust
#[pymodule]
fn calm_witness_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Commitment>()?;
    m.add_function(wrap_pyfunction!(commit_py, m)?)?;
    m.add_function(wrap_pyfunction!(open_py, m)?)?;
    m.add_function(wrap_pyfunction!(prove_equality_py, m)?)?;
    m.add_function(wrap_pyfunction!(verify_equality_py, m)?)?;
    m.add_function(wrap_pyfunction!(prove_membership_py, m)?)?;
    m.add_function(wrap_pyfunction!(verify_membership_py, m)?)?;
    m.add_function(wrap_pyfunction!(prove_range_64_py, m)?)?;
    m.add_function(wrap_pyfunction!(verify_range_64_py, m)?)?;
    Ok(())
}
```

The Python side imports as `from calm_witness_rs import *`. The placeholder functions in `calm_witness/proof.py` and `calm_compass/aggregator.py` swap one import to delegate; the wire shape doesn't change.

## §8. The swap-in plan (file-by-file)

| Python file | Function | Replace with |
|---|---|---|
| `calm_witness/proof.py` | `commit_predicate_value` | `calm_witness_rs.commit_predicate_value` |
| `calm_witness/proof.py` | `prove_membership_in_set` | `calm_witness_rs.prove_membership` |
| `calm_witness/proof.py` | `verify_membership_proof` | `calm_witness_rs.verify_membership` |
| `calm_witness/proof.py` | `prove_distance_below_threshold` | `calm_witness_rs.prove_range_64` |
| `calm_compass/aggregator.py` | `_placeholder_pedersen_commit` | `calm_witness_rs.commit` |
| `calm_compass/aggregator.py` | `_placeholder_aggregate` | `calm_witness_rs.aggregate` |
| `calm_compass/aggregator.py` | `_placeholder_range_proof` | `calm_witness_rs.prove_aggregate_above_threshold` |

Tests that pass against placeholders continue to pass against real crypto. The conformance vectors are the contract.

## §9. Constant-time discipline

`subtle::Choice` and `subtle::ConstantTimeEq` everywhere a comparison touches secret material. No `==` on `Scalar` outside test code. No early-return based on secret values. The `timing_test.rs` empirically measures variance across many runs; the t-test threshold is `p < 0.01` for divergence (CI flags otherwise).

## §10. Conformance harness

```rust
#[test]
fn witness_conformance_vectors() {
    let vectors = load_json("../calm_witness/conformance_vectors.json");
    for v in vectors.canonicalisation { /* verify record_hash matches */ }
    for v in vectors.schema { /* run validator; check error substrings */ }
    for v in vectors.predicates { /* run in_baseline_24h equivalent; check value */ }
}

#[test]
fn compass_conformance_vectors() {
    let vectors = load_json("../calm_compass/conformance_vectors.json");
    for v in vectors {
        let actual = run_classifier(&v.predicate, &v.input_record, v.tribe_map.as_ref());
        assert_eq!(actual, v.expected_score, "vector {}", v.vector_id);
    }
}
```

Python conformance JSON is the input. Rust output must match the published `expected_*` fields byte-for-byte.

## §11. Out of scope for this summit

- ZKML circuits for Compass classifiers (CC-36; separate summit).
- FROST threshold signing for the attestation envelope (separate summit; uses `frost-ed25519` directly).
- Post-quantum migration (CC-26, E96; future).
- Wasm bindings (EW-105; separate summit).

## §12. Estimated effort

| Phase | Days | Notes |
|---|---|---|
| Pedersen layer | 1 | Mostly composing `curve25519-dalek` primitives |
| Sigma equality + membership | 2 | Real care needed on OR-of-Σ-protocols |
| Bulletproofs range proof | 2 | If using an existing crate; 5+ if from scratch |
| Bulletproofs sum-over-history range proof | 1 | Aggregation extension |
| PyO3 bindings | 1 | Mechanical |
| Conformance harness | 0.5 | |
| Constant-time validation | 0.5 | |
| **Total** | **~8 days** | one focused Rust engineer |

## §13. Acceptance for handoff

This spec is bagged when a Rust engineer (human or AI) reading it produces a `calm-witness-rs` crate that:
1. Compiles under stable Rust ≥ 1.81.
2. Passes the Python conformance harness end-to-end.
3. Has `timing_test.rs` reporting no significant divergence (t-test p > 0.01).
4. Has a passing CI build that runs the harness on each commit.

When that crate ships, the placeholder bytes throughout the Python reference disappear. The Calm Stack becomes real cryptography.

— Calm, 2026-05-20
