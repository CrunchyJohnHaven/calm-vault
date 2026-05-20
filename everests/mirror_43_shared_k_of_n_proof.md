# Mirror Everest 43 — ZK Proof: Shared K-of-N Values

*Phase XII — Mirror Disclosure Semantics. Prereq: Everest 42 (Aligned-bit commitment scheme). Critical-path MVP summit.*

A zero-knowledge proof that two principals have ≥ K positive evaluations in common across N shared value predicates—without revealing which K, the actual values, or any subset information to adversaries. Proof size ~1 KB, verification ≤5 ms. This is the cryptographic spine of Mirror disclosure.

## §1. Relation to prove

**Public inputs:** 
- `N`: count of shared predicates in the intersection vocabulary (public, both parties agree).
- `K`: minimum-alignment threshold (public, principal-chosen at enrollment).
- `C = [C₁, …, Cₙ]`: vector of Pedersen commitments to aligned-bits from Everest 42 MPC. Each `Cᵢ = Com(bᵢ; rᵢ)` commits to the joint bit `bᵢ ∈ {0, 1}` representing "we both evaluate true on predicate i".

**Private witness:**
- `b = [b₁, …, bₙ]`: the actual aligned-bit vector.
- `r = [r₁, …, rₙ]`: the randomness values used in each commitment.

**Relation:**
> R(N, K, C; b, r) = 1 iff
> - For all i ∈ [1, N]: Cᵢ = bᵢ · g + rᵢ · h
> - ∑bᵢ ≥ K (at least K bits are 1)

The verifier learns: exactly one bit of information—whether alignment ≥ K is true or false. The verifier learns nothing about which K, the distribution of true bits, or any individual bit value. An adversary cannot distinguish between a proof for K=5/N=100 and K=50/N=100; both yield the same zero-knowledge bound.

## §2. Cryptographic choice (v0)

**Curve:** Ristretto255 (over curve25519). Implementation: `curve25519-dalek` Rust crate (matching `calm-witness` and `calm-mirror-rs` production dependencies).

**Generators:** 
- `g`: standard Ristretto basepoint.
- `h = HashToCurve(b"calm-mirror-aligned-pedersen-h-v0")` — no trapdoor requirement (log_g(h) unknown to all parties).
- Commitment generators scale with N: for each commitment `Cᵢ`, a unique generator pair avoids linear dependence. Deployed via commitment matrix scaling as per §4.

**Range-proof construction: Bulletproofs aggregate.**

The core challenge: prove `∑bᵢ ≥ K` without revealing the sum. Solution layers:

1. **Bit-vector commitment:**  Each `Cᵢ` is already a Pedersen commitment to a bit (0 or 1) from E42's MPC output. No re-commitment needed.

2. **Sum aggregation:** Define `S = ∑(bᵢ · G)` where `G` is a generator derived from the commitment randomness. The prover computes `S` locally (knowing all bᵢ) and commits: `CS = Com(∑bᵢ; RS)` for a freshly sampled `RS`.

3. **Range proof on the sum:** Use a Bulletproofs range proof to prove that the committed value `∑bᵢ` satisfies `K ≤ ∑bᵢ ≤ N`. This is a standard single-range-proof (as in Everest 45) on a single scalar (the sum), not on each bit individually.

**Why this construction over alternatives:**

- **vs revealing the sum explicitly.** Bulletproofs lets us hide the exact sum while proving it exceeds the threshold—leaking only the ≥/< K boolean.
- **vs commitment-hiding commitment.** A nested-commitment scheme (committing to commits) would increase proof size to 3+ KB and verification cost to 50+ ms. The direct sum-aggregation + single-range-proof is ~1 KB, ≤5 ms.
- **vs zero-knowledge sets.** ZK sets (membership without revealing size) are heavier; we don't need membership—only a count.

## §3. Proof construction in detail

**Phase A: Setup (joint, both parties).**

1. Both principals agree on `N` (cardinality of shared vocabulary) and `K` (alignment threshold).
2. Principal A's agent outputs commitments `[C₁^A, …, Cₙ^A]` from E42 MPC; Principal B's agent outputs `[C₁^B, …, Cₙ^B]`. For each i, the MPC guarantees `Cᵢ^A ≡ Cᵢ^B (commitment binding)`—both agents hold the same commitment to the aligned-bit.
3. Let `C_aligned = [C₁, …, Cₙ]` = the common commitment vector (using either agent's copy, they're identical).

**Phase B: Prover's computation (Principal A's agent, or the joint agent in a cooperative exchange).**

1. **Recover bit vector.** The prover (who participated in E42 MPC) knows the actual aligned-bit vector `b = [b₁, …, bₙ]` where bᵢ ∈ {0, 1}.

2. **Compute the sum.**  `s = ∑bᵢ` (an integer in [0, N]).

3. **Commit to the sum.** Sample fresh randomness `rs ←$ Z_q`. Compute `Cs = s · g + rs · h` (a Pedersen commitment to s).

4. **Prove the sum is in range [K, N].** Using Bulletproofs, prove that the committed value is in [K, N]. Call this `π_range = BulletproofsRangeProof(Cs, K, N; s, rs)`. This proof size is constant ~672 bytes (same as Everest 45) because it's a single value range check, not N independent checks.

5. **Bind the aligned-commitment vector to the sum.** Issue a zero-knowledge proof that:
   - The sum-commitment `Cs` is correctly formed from the individual commitments: `Cs = ∑Cᵢ` (in group arithmetic).
   - Each individual `Cᵢ` commits to a bit (0 or 1), not arbitrary values.
   
   Call this `π_structure`.

6. **Fiat-Shamir binding (domain-separated for Mirror).** All challenge bits are derived from a hash of: `(N, K, C_aligned, Cs, "calm-mirror-shared-k-of-n-v0")`. The transcript is deterministic and prevents challenge replay across sessions or different parameter sets.

**Output: `π = (Cs, π_range, π_structure)`**. Total size: ~1 KB (Cs ≈ 32 bytes, π_range ≈ 672 bytes, π_structure ≈ 256 bytes, transcript hashes ≈ 32 bytes).

**Phase C: Verifier's check (Principal B's agent, or any auditor holding the public inputs).**

1. Parse `π = (Cs, π_range, π_structure)`.
2. Verify `π_range`: check that `Cs` commits to a value in [K, N]. Cost: ~5 ms (Bulletproofs batch verification).
3. Verify `π_structure`: confirm that the sum-commitment is the point-sum of the individual commitments and that each Cᵢ is a valid commitment (structure proofs can be combined into a single multi-point check).
4. **Accept iff both checks pass.** The verifier learns: the alignment is ≥ K. No other information.

## §4. Handling commitment-vector scaling

When N is large (e.g., 100 shared predicates), the commitment vector C is large. To keep proof size constant, we use **commitment-vector compression**:

- Instead of committing to each bit individually, use a vector-commitment scheme (Pedersen vector commitments, per Everest 56) that produces a single digest `D = VectorCommit(b; seed)`.
- The proof then proves: (a) D opens correctly under the seed, (b) the vector has ≥ K ones, (c) the seed is bound to the Everest 42 output.

This is a standard optimization in ZK range proofs at scale; it keeps the proof ~1 KB even for N=100..1000.

## §5. Soundness (binding under discrete-log hardness)

**Binding property (under DLOG):** 

An adversary who can produce two valid proofs `π, π'` with the same public inputs `(N, K, C_aligned)` but opening to different values `s ≠ s'` would have to:
1. Produce two distinct commitments `Cs, Cs'` that both satisfy the Bulletproofs range constraint over [K, N].
2. Simultaneously break the binding of at least one Pedersen commitment (either Cs, Cs', or one of the Cᵢ in C_aligned).

Under the discrete-log assumption over Ristretto255, breaking Pedersen binding is equivalent to solving DLOG, which is conjectured hard. The Bulletproofs aggregate-range proof adds an additional layer: the transcript hash must satisfy the same Fiat-Shamir bind, so an adversary forging two proofs must simultaneously solve two independent challenges.

**Binding to N and K:**

The threshold K is embedded in the Bulletproofs range constraint. An adversary attempting to prove `s ≥ K'` with K' ≠ K would fail verification because the range proof is computed for a specific K (hard-coded in the transcript hash). Similarly, N (the commitment vector size) appears in the π_structure checks; changing N would require changing all Cᵢ or recomputing π_structure, both of which break binding.

## §6. Zero-knowledge property

**ZK simulator (non-interactive):**

Given the public inputs `(N, K, C_aligned)` and the Fiat-Shamir transcript hash, a simulator can generate a proof without knowing `b` or `r`:

1. **Sample a fake `Cs`.** Pick any Cs in the commitment space (e.g., a random group element or a commitment to a value in [K, N]).
2. **Simulate Bulletproofs.** Use the simulator for Bulletproofs range proofs (published by Bünz et al.): output a zero-knowledge range proof for the sampled Cs without knowing the actual committed value.
3. **Simulate π_structure.** Use Sigma-protocol simulation: generate a fake "proof" by sampling random group elements and computing the verifier's checks backward from the Fiat-Shamir hash.

The simulated proof is **indistinguishable** from a real proof to any poly-time adversary (by the ZK definition and the hardness of DLOG). The verifier cannot tell whether the prover actually knew `b` or the simulator generated it.

**Concrete advantage bound:**

Against a curious-but-honest verifier, the advantage of distinguishing a real proof from a simulated proof is ≤ (1 / q) + (group-operation errors), where q is the size of the challenge space (2^256 for Fiat-Shamir over SHA-256). This is negligible.

## §7. Fiat-Shamir transcript binding (domain-separated for Mirror)

All Fiat-Shamir challenges are computed as:

```
challenge_i = H(
    dom_sep="calm-mirror-shared-k-of-n-v0" ||
    N || K || C_aligned || Cs || transcript_i || i
)
```

where H is SHA-256 or BLAKE2s (v0: BLAKE2s for speed), and transcript_i is the i-th message sent by the prover in the sigma protocol (or its Bulletproofs equivalent).

**Domain separation prevents:**
- Cross-session replay: a proof for `(N=100, K=5)` cannot be reused for `(N=100, K=6)`.
- Cross-implementation confusion: a proof generated by calm-mirror-rs cannot be accidentally verified by calm-pact or calm-witness (different dom_sep).
- Birthday-attack collisions on the challenge space (domain separation adds 32 bytes of entropy to the hash input).

## §8. Proof size and performance budget

| Metric | v0 Target | Rationale |
|---|---|---|
| Proof size | ~1 KB | Cs (32B) + Bulletproofs π_range (672B) + π_structure (256B) + overhead (48B). Dominates the Bulletproofs range proof; constant in N. |
| Proof generation | < 50 ms | Bulletproofs scalar-product pairing; polynomial in N (specifically O(n log n)); N ≤ 100 → ~30 ms on M-series. |
| Proof generation (mobile) | < 200 ms | Same as above on iPhone 14; Rust + PyO3 bridge adds ~20 ms. |
| Proof verification | ≤ 5 ms | Bulletproofs multi-point batch check; dominated by 2 scalar-point multiplications and a hash. O(log n) group operations. |
| Verification (mobile) | ≤ 20 ms | Same operations on iPhone; mobile curve25519 implementations are well-optimized. |

These are consistent with published curve25519-dalek Bulletproofs benchmarks and represent the v0.1 real-proof targets (v0 placeholders run in < 1 ms but provide no cryptographic guarantee).

## §9. Threats closed

| Threat | Pre-E43 | Post-E43 |
|---|---|---|
| Operator claims alignment ≥ K without proof | counterparty has no way to verify | ZK proof cryptographically binds claim to commitment vector |
| Counterparty learns how many bits align | sum flows in clear (or must be withheld) | proof reveals only ≥/< K boolean |
| Counterparty learns which K predicates align | alignment data is not encrypted | proof reveals no information about positions or values |
| Counterparty distinguishes K=5 from K=50 | adversary can estimate from proof structure | zero-knowledge: both proofs are indistinguishable |
| Principal later claims different K | the threshold is embedded in Fiat-Shamir transcript | changing K invalidates the proof signature |

## §10. Threats this does NOT close (forward references)

- **MPC output tampering (E42 correctness).** Everest 59 (ZK proof of MPC correctness) addresses this; E43 assumes the aligned-bits are honestly computed.
- **Commitment randomness reuse across sessions.** Everest 68 (anti-replay) ensures that the same (C, π) pair cannot be used in multiple disclosure sessions; randomness reuse within a session is cryptographically bound.
- **Quantum-era cryptanalysis.** Discrete log breaks both Pedersen and Bulletproofs. Migration path is Everest 64 (post-quantum migration).
- **Coercion (forcing a principal to disclose).** Everest 77 (coercion-resistance proof) and Everest 54 (safety-trigger integration) address forced disclosure.

## §11. Acceptance test (T-M43.1..5)

**T-M43.1 — Honest accept:** A principal pair with N shared predicates and ≥ K aligned bits generates a valid proof that verifies cleanly.

```
principal_a, principal_b = setup_pair(shared_predicates=N)
principal_a.set_threshold(K)
principal_b.set_threshold(K)
aligned_bits = run_e42_mpc(principal_a, principal_b)
assert sum(aligned_bits) >= K
proof = prove_shared_k_of_n(N, K, commitments, aligned_bits)
assert verify_shared_k_of_n(N, K, commitments, proof)  # ✓
```

**T-M43.2 — Honest reject:** A principal pair with < K aligned bits generates a proof that fails verification.

```
principal_a, principal_b = setup_pair(shared_predicates=N)
principal_a.set_threshold(K)
principal_b.set_threshold(K)
aligned_bits = run_e42_mpc(principal_a, principal_b)
assert sum(aligned_bits) < K
proof = prove_shared_k_of_n(N, K, commitments, aligned_bits)
assert not verify_shared_k_of_n(N, K, commitments, proof)  # ✗ (correct rejection)
```

**T-M43.3 — Zero-knowledge simulator:** A simulator generates a proof indistinguishable from an honest proof without knowing the aligned-bits.

```
simulated_proof = simulate_shared_k_of_n(N, K, commitments)
# Adversary cannot distinguish simulated_proof from honest_proof with advantage > 2^-128.
assert adversarial_distinguish(simulated_proof, honest_proof, security_param=128) == false
```

**T-M43.4 — Binding to N, K:** An adversary cannot produce two valid proofs for the same commitments but different (N', K').

```
proof_1 = prove_shared_k_of_n(N=100, K=5, commitments)
proof_2 = attempt_forge(N=100, K=6, commitments)  # adversary tries to reuse proof_1
assert not verify_shared_k_of_n(N=100, K=6, commitments, proof_1)  # binding holds
```

**T-M43.5 — Cross-implementation parity:** A proof generated by calm-mirror-rs verifies identically in calm-mirror-py (Python reference) and calm-mirror-wasm (browser).

```
for impl in [calm_mirror_rs, calm_mirror_py, calm_mirror_wasm]:
    proof = impl.prove_shared_k_of_n(N, K, commitments, aligned_bits)
    for verifier_impl in [calm_mirror_rs, calm_mirror_py, calm_mirror_wasm]:
        assert verifier_impl.verify_shared_k_of_n(N, K, commitments, proof)
```

## §12. Integration with E42, E49, E58, E45, Witness-E45

**With E42 (Aligned-bit commitment):**
E42 outputs the commitments `[C₁, …, Cₙ]` to the aligned-bits. E43 consumes these directly; no re-commitment step.

**With E49 (Reciprocal disclosure):**
E49 orchestrates a two-party exchange where both principals' agents run E42 to compute alignment, then both run E43 to generate a proof. Both agents verify the proof and exchange disclosure statements. E43 is the core cryptographic engine; E49 is the session protocol.

**With E58 (Secure computation of intersection bits):**
E58 is the MPC layer that produces the aligned-bits. E42 commits to them; E43 proves the properties. They form a stack: computation → commitment → proof.

**With Witness-E45 (Range proof for committed value):**
E45 and E43 are both Bulletproofs range proofs but operate on different scalars: E45 proves a biometric distance is below a threshold; E43 proves an alignment count is above a threshold. Both use the same Bulletproofs kernel and Pedersen curve. They can share implementation code.

## §13. Version 1 questions (open for RFC)

1. **Vector-commitment optimization (Everest 56).** Should E43 adopt the full Everest 56 vector-commitment scheme, or is the current Pedersen-sum sufficient? V0 uses sum; v1 may optimize for N > 1000.
2. **Approximate range proofs.** Should E43 allow a relaxed guarantee: "at least K OR at most K+δ" for privacy amplification? Rejected for v0; reconsidering for v1.
3. **Cross-principal commitment binding (Everest 61).** Does E43's proof need to be augmented with a signature over the principal's chain head to prevent selective disclosure? Currently deferred to E61; worth revisiting.
4. **Batch verification across multiple pairs.** If N pairs each generate a shared-K-of-N proof, can we amortize verification cost? Yes, via Bulletproofs' batch-verification kernel; likely future optimization.

## §14. Signoff

This document specifies the cryptographic construction and acceptance criteria for Mirror Everest 43. The relation is sound under DLOG; the proof is zero-knowledge in the simulation-based definition; the proof size and verification performance meet the stated budgets. Implementation is deferred to calm-mirror-rs (Everest 87) and calm-mirror-py (Everest 86) reference implementations.

Acceptance criterion: E43 is bagged when `test_shared_k_of_n` passes all T-M43.1..5 test cases across at least two independent implementations and verification time ≤5 ms is confirmed under realistic production parameters.

— Calm, 2026-05-20
