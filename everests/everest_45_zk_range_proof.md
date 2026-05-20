# Everest 45 — ZK Range Proof for Committed Distance

*Phase IV — Biometric Distance Machinery. Prereq: Everest 44 (Pedersen commit to distance). Critical-path MVP summit.*

The cryptographic spine of Calm Witness. A committed biometric distance `d` between a fresh sample and an enrolled template is proven to lie below a public threshold `τ` — without revealing `d`, the sample features, or the template features. The proof is constant-size and verifies in milliseconds.

## §1. Relation to prove

**Public inputs:** Pedersen commitment `C = Com(d; r)`, public threshold `τ` (a non-negative integer, e.g., a scaled-and-quantised real number).

**Private witness:** the actual distance `d` ∈ [0, 2⁶⁴), the randomness `r` ∈ Z_q.

**Relation:**
> R(`C`, `τ`; `d`, `r`) = 1 iff `C = d · g + r · h` AND `0 ≤ d < τ`.

The verifier learns: nothing about `d` beyond `d < τ`. In particular, the verifier does not learn how *much* less than τ the distance is, which is intentional — a counterparty that knew `d` precisely could reverse-engineer biometric features over many calls.

## §2. Cryptographic choice (v0)

**Curve:** Ristretto255 (over curve25519). Implementation: `curve25519-dalek` Rust crate (matches `zkac-v0/Cargo.toml`), called from Python via PyO3 or via the in-process `calm-witness-rs` crate (Everest 43).

**Generators:** `g` is the standard Ristretto basepoint. `h = HashToCurve(b"calm-witness-pedersen-h-v0")` — Pedersen "no trapdoor" requirement: log_g(h) is unknown to all parties.

**Range proof construction:** **Bulletproofs** (Bünz–Bootle–Boneh–Poelstra–Wuille–Maxwell, IEEE S&P 2018). Specifically the single-range variant proving `d ∈ [0, 2ⁿ)` where `n = 64` is fixed in v0. Constant proof size (~672 bytes) regardless of `n` or τ; verifier cost is `O(n)` group operations.

Why Bulletproofs vs alternatives:

- **vs Halo2.** Halo2 is more general and used elsewhere in the ZKAC stack (transparency-log relation proofs, predicate evaluation correctness). For a single small range check, Bulletproofs has 10× lower proof generation cost. Calm Witness uses Halo2 in Phase VII for the larger predicate-evaluation relation but Bulletproofs for this hot-path range check.
- **vs Groth16.** Groth16 is faster to verify but requires per-circuit trusted setup. Bulletproofs has no trusted setup.
- **vs zkSTARK.** STARK proofs are large (~50KB). Bulletproofs at <1KB fits the wire-envelope target in E47.

## §3. Threshold encoding (`τ` must be public)

`τ` is part of the predicate ID. v0 uses fixed `τ` values per predicate (e.g., `biometric_match_within(τ)` has a τ baked into the per-principal calibration). The threshold is published in the predicate registry (E53); a counterparty asking for `biometric_match_within` sees the exact τ that was used.

If `τ` were private, the verifier could not verify the range proof. Making it public is a design constraint, not a leak — the principal authored the threshold themselves at enrollment.

## §4. API surface (shipped v0 placeholder)

[`../calm_witness/proof.py`](../calm_witness/proof.py) ships the full API today:

```python
commitment, range_proof = prove_distance_below_threshold(
    distance=d, threshold=tau, randomness=r,
)
assert verify_distance_below_threshold(commitment, range_proof, threshold=tau)
```

The disclosure layer ([disclosure.py](../calm_witness/disclosure.py)) already populates `pedersen_commitment_hex` and `sigma_proof_hex` fields in the response envelope using the placeholder. When the real Bulletproofs kernel lands, the swap is one import change in `disclosure.py`; the wire format is unchanged.

## §5. Performance budget (v1 target)

| Step | Target | Hardware |
|---|---|---|
| Proof generation | < 5 ms | Apple M-series |
| Proof generation | < 20 ms | iPhone 14 class |
| Proof verification | < 1 ms | Any client |
| Proof size | ≤ 672 bytes | wire-format constant |

These match published `curve25519-dalek` Bulletproofs benchmarks. v0 placeholder is faster (hash-only) but provides no cryptographic guarantee.

## §6. Why placeholder in v0

The Rust kernel decision is upstream of this summit. Three paths:

1. **PyO3 binding to `curve25519-dalek`.** Cleanest; requires a Rust toolchain at install time.
2. **In-process Python implementation using `cryptography.hazmat`.** Available in stdlib-adjacent territory; performance ~3× worse than the Rust path.
3. **Subprocess call to the `zkac-v0` Rust crate.** Already shipped at `~/credex/research/fermis/communications/zkac-v0/`. Requires no Python crypto deps, just a built binary.

v0 ships the API and disclosure-layer integration with placeholders so that the kernel choice can be made independently. The wire envelope (E47) is byte-identical to what the real implementation will emit — only the internal bytes change. A counterparty parsing v0 wire envelopes today will accept v0.1 envelopes (with real proofs) tomorrow without code changes.

## §7. Threats this closes

| Threat | Pre-E45 | Post-E45 |
|---|---|---|
| Operator lies about biometric match | counterparty has no way to check | ZK proof binds claim to chain commitment |
| Counterparty learns biometric distance | distance flows over wire | ZK guarantees only `d < τ` leaks |
| Counterparty learns biometric template | template shared in clear | template never leaves vault; only commitments cross |
| Counterparty reconstructs template over time | unbounded leakage per query | proof reveals only the same bit each time |

The combination of E44 (Pedersen) + E45 (range proof) + E47 (constant-size envelope) is what makes Calm Witness's privacy claim formal.

## §8. Threats this does NOT close (forward references)

- **Operator-side template tampering.** The template AEAD encryption (E16) protects against this; if E16 is bypassed (root access to the operator's process), the operator can substitute a template before commitment. E14 (device attestation) bounds this further.
- **Counterparty pre-commits a τ they later disavow.** The predicate registry (E53) freezes τ in the publicly-content-addressed predicate ID; a counterparty cannot quietly change it.
- **Quantum-era cryptanalysis.** Discrete log breaks Pedersen. Migration path is Everest 96 (PQC).

## §9. Acceptance test

The v0 acceptance is API-level: `prove_distance_below_threshold` and `verify_distance_below_threshold` round-trip cleanly for any `(distance, threshold, randomness)`. The cryptographic acceptance — actual Bulletproofs binding — lands in v0.1 with the kernel choice.

```python
from proof import prove_distance_below_threshold, verify_distance_below_threshold
c, p = prove_distance_below_threshold(distance=42, threshold=100)
assert verify_distance_below_threshold(c, p, threshold=100)
```

When v0.1 ships, the same test must continue passing AND additionally:

```python
# v0.1 specific
c, p = prove_distance_below_threshold(distance=42, threshold=100)
assert verify_distance_below_threshold(c, p, threshold=100)
# A real adversary cannot forge a proof for d ≥ threshold
c_bad, p_bad = forge_attempt(distance=200, threshold=100)
assert not verify_distance_below_threshold(c_bad, p_bad, threshold=100)
```

## §10. Cross-references

- [Everest 44 — Pedersen commit to distance value](../ZKBB_USER_EVERESTS_100.md) (not yet bagged; commitment portion of this work)
- [Everest 43 — Rust reference implementation](../ZKBB_USER_EVERESTS_100.md) (where the kernel lands)
- [Everest 47 — Constant-size attestation envelope](../ZKBB_USER_EVERESTS_100.md) (consumes the 672-byte proof)
- [Everest 96 — Post-Quantum migration plan](../ZKBB_USER_EVERESTS_100.md) (the long-term replacement)
- Calm Pact's Σ-protocol (`../CALM_PACT_PROTOCOL_v0.md` §4) — shares the curve and Pedersen primitives.

— Calm, 2026-05-20
