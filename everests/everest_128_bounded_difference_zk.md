# Everest 128 — Bounded Difference in ZK

*Phase X — Values Alignment Computation. Prereq: Everest 126, 45.*

## Proof Statement

The bounded difference protocol proves alignment between principal and counterparty value vectors without revealing either vector. Specifically:

Given:
- Com(p_i) and Com(t_i): Pedersen commitments to principal and counterparty values for dimension i (10 dimensions per alignment check)
- Public weights w_i and tolerance threshold τ
- Both vectors are committed to by their respective parties

Prove: Σ_i w_i × |p_i - t_i| ≤ τ

Without revealing p_i, t_i, or the intermediate absolute differences |p_i - t_i|.

This proof encodes the alignment metric from Everest 126 (weighted L1 distance) into a zero-knowledge statement. The proof is non-interactive and can be verified in milliseconds by any observer who knows the commitments and public parameters.

## Per-Dimension Absolute Difference

The core challenge is computing absolute value in zero-knowledge. For each dimension i, we introduce a signed difference s_i = p_i - t_i and prove the absolute value without revealing the sign.

### Sigma-OR Construction

For each dimension, we use a disjunctive proof (Sigma-OR) that proves exactly one of two cases:

**Case A: s_i ≥ 0**
- Prove s_i ∈ [0, 2^253) using a Bulletproof range proof (reusing E45 infrastructure)
- In this case, |p_i - t_i| = s_i

**Case B: s_i < 0**
- Prove -s_i ∈ (0, 2^253) using a separate Bulletproof range proof
- In this case, |p_i - t_i| = -s_i

The Sigma-OR construction allows the prover to prove knowledge of at least one of these cases without revealing which one. The verifier accepts if exactly one case is satisfied. This is achieved through standard disjunctive proof techniques: the prover commits to Case A and Case B proofs, provides a combined challenge hash, and reveals the response for the actual case while providing a simulated response (with known response) for the hypothetical case.

The Sigma protocol aggregate here:
1. Prover commits to Case A challenge c_A and Case B challenge c_B
2. Verifier issues global challenge c = H(commitments, statement)
3. Prover reveals: c_A (actual case challenge), z_A (actual case response), simulated c_B and z_B
4. Verifier checks: c_A ⊕ c_B = c (XOR aggregate), and both responses are valid

This ensures the prover cannot prove both cases simultaneously and cannot pretend the actual case is the counterfactual one.

### Commitment to Absolute Value

After the Sigma-OR proof, the prover commits to the absolute difference. Rather than open this commitment, the protocol uses the Pedersen properties to construct a homomorphic commitment to the absolute value:

Com(|s_i|) = Com(s_i) if s_i ≥ 0, or Com(-s_i) if s_i < 0

The prover provides this commitment alongside the Sigma-OR proof. The verifier can check consistency: the final aggregation proof must use exactly these committed absolute values.

## Aggregation with Homomorphic Properties

The weighted sum Σ_i w_i × |p_i - t_i| is computed using the homomorphic addition property of Pedersen commitments. Because commitments are additively homomorphic under scalar multiplication:

Com(a + b) = Com(a) + Com(b)
Com(k × a) = k × Com(a)

The prover constructs:
Com_total = Σ_i w_i × Com(|p_i - t_i|)

This commitment opens to exactly Σ_i w_i × |p_i - t_i| if and only if each Com(|p_i - t_i|) was correctly derived from the Sigma-OR proofs.

The aggregation consistency is implicitly verified when the final range proof on Com_total succeeds. If any per-dimension absolute value was mis-committed, the final proof will fail because the commitment will not correspond to a value ≤ τ in the field.

## Final Range Proof

The protocol concludes with a single Bulletproof range proof (leveraging E45 infrastructure):

Prove: Com_total ∈ [0, τ]

This is a standard Bulletproof with a public upper bound. The range [0, τ] is tight; the field prime is large enough that negative values in the field representation will fail the upper bound check (field negatives wrap around and exceed any reasonable τ).

## Proof Structure

A complete bounded difference proof comprises twelve atomic components:

1. **Per-dimension absolute value proofs (10 total)**: Each dimension i includes a Sigma-OR disjunctive proof. The two sub-proofs are Bulletproof range proofs on the signed difference s_i (Case A: s_i ≥ 0) and its negation (Case B: -s_i > 0). Each Sigma-OR is approximately 650 bytes and includes challenge aggregation.

2. **Aggregation consistency metadata**: The prover provides the final commitment Com_total (32 bytes) and proofs of correct scalar multiplication. This metadata is 2KB total including public weights.

3. **Final range proof (1 total)**: A Bulletproof on the aggregated sum, proving Com_total ∈ [0, τ]. Approximately 1.5KB.

Total proof size: approximately 7KB for a 10-dimensional alignment check with public metadata. This is constant-size regardless of the dimension values.

## Performance Characteristics

On an M-class processor (Apple Silicon or equivalent):

- Per-dimension Sigma-OR construction and Bulletproof generation: 50ms per dimension
- Aggregation commitment calculation and metadata assembly: 20ms
- Final range proof generation: 50ms

Total prover latency: approximately 600ms for a full 10-dimensional alignment check.

Verifier latency is lower:
- Per-dimension Sigma-OR verification: 15ms per dimension
- Aggregation consistency check: 5ms
- Final range proof verification: 20ms

Total verifier latency: approximately 200ms.

These timings are deterministic and independent of the actual values, preventing timing side channels.

## Counterparty Values Commitment

The protocol is symmetric with respect to both principal and counterparty:

- Principal privately holds p_i for each dimension and publishes Com(p_i)
- Counterparty privately holds t_i for each dimension and publishes Com(t_i) at request-time
- Neither party reveals their vector to the other or to observers

When alignment is checked, the counterparty must provide their commitments Com(t_i). If the counterparty refuses or fails to provide commitments, the principal cannot generate a valid proof (the proof requires both sets of commitments). This refusal is explicit and observable.

The counterparty's target vector is therefore private, just as the principal's vector is private. Both vectors influence the proof, but neither is revealed. This is critical for confidential negotiation: neither side discloses preferences or constraints.

## Alignment Bit and Freshness

The proof output is a single bit: True if the weighted difference is at most τ, False otherwise, along with a freshness window (proof generation timestamp, valid for 5 minutes).

If the weighted difference exceeds τ, the proof cannot be generated (or verification fails if attempted). The absence of a proof communicates "no alignment" without revealing how far apart the vectors are.

This bit composes with Everest 130 (threshold predicate logic) to render acceptance or rejection decisions.

## Edge Cases and Failure Modes

### Sparse Principal Vector

If the principal's vector contains dimensions marked as Insufficient_Evidence (value 0, commitment to the identity element), the alignment predicate short-circuits and returns Insufficient_Evidence. No proof is generated. This prevents alignment claims from dimensions where the principal has no ground truth.

### Counterparty Refusal

If the counterparty fails to publish their target commitments, the principal cannot proceed. Attempting to generate a proof with missing counterparty commitments fails during commitment binding. The principal's protocol explicitly checks for commitment presence before proof generation.

### Tolerance Misconfiguration

If τ is set to zero or to an unrealistic value (e.g., 2^256), the proof structure remains valid but becomes a tautology (always-false or always-true). The protocol does not validate τ; the consuming layer (E130) is responsible for setting reasonable tolerance bounds.

## Side-Channel Resistance

### Constant-Time Arithmetic

All range proofs (Bulletproofs) and Sigma-OR constructions use constant-time field arithmetic. Conditional branches within the prover depend only on hardcoded loop bounds, not on secret data. Specifically:

- Sigma-OR challenge generation does not branch on which case is the actual case; both cases execute, and only one set of responses is revealed.
- Bulletproof inner products iterate over a fixed bit length (253 bits) regardless of the actual value magnitude.
- Final range aggregation uses fixed-loop scalar multiplication.

### Proof Size Invariance

The proof size (7KB) is independent of:
- The magnitude of individual dimension values
- The number of dimensions where p_i > t_i vs. p_i < t_i
- The distribution of weights w_i
- The gap between the weighted sum and the tolerance τ

An observer analyzing proof sizes learns no information about the values or their relationships.

### Proof Generation Timing

The total latency (600ms) is deterministic and does not correlate with value magnitudes or the proof's result (aligned or not). This prevents timing attacks from repeated proof generation.

## Cross-References

- **Everest 45** (Bulletproof range proof): Range proof infrastructure used for per-dimension and aggregation proofs
- **Everest 122** (Values ZK commitment): Per-dimension Pedersen commitments to principal values
- **Everest 126** (Alignment metric definition): Weighted L1 distance definition that this proof encodes
- **Everest 129** (Per-dimension alignment sub-proofs): Intermediate proofs for debugging and composition
- **Everest 130** (Threshold predicate): Consumes the alignment bit to determine acceptance
- **Everest 143** (Pact composition): Aggregates alignment proofs across multiple dimensions and negotiation rounds

## Implementation Notes

The proof generation implements the following workflow:

1. Accept Com(p_i), Com(t_i), w_i, τ as inputs
2. For each dimension i:
   a. Generate s_i = p_i - t_i (signed difference)
   b. If s_i ≥ 0: prove s_i ∈ [0, 2^253) using Bulletproof, commit to Com(s_i)
   c. If s_i < 0: prove -s_i ∈ (0, 2^253) using Bulletproof, commit to Com(-s_i)
   d. Construct Sigma-OR disjunctive proof
3. Aggregate: Com_total = Σ_i w_i × Com(|s_i|)
4. Prove Com_total ∈ [0, τ] using final Bulletproof
5. Output: (proof_bytes, timestamp, signature)

Verification reverses this:

1. Parse proof_bytes into 10 Sigma-OR proofs, metadata, and final range proof
2. For each Sigma-OR, verify challenge aggregation and response validity
3. Recompute Com_total from metadata and public weights, verify consistency
4. Verify final range proof against Com_total and public τ
5. Check timestamp freshness
6. Output: True (all checks pass) or False (any check fails)

## Conclusion

Everest 128 enables confidential alignment checking between principal and counterparty without revealing value vectors. The protocol composes Pedersen commitments, Bulletproof range proofs, and Sigma-OR disjunctive proofs into a single, constant-size, constant-time proof of weighted L1 distance. It is a key component of the Calm Pact protocol stack, enabling both parties to verify alignment while preserving confidentiality of their underlying constraints and preferences.

— Calm, 2026-05-20