# Everest 122 — Values ZK Commitment

*Phase IX — Values Vocabulary. Prereq: Everest 44, 114.*

## Overview

This Everest establishes the zero-knowledge commitment scheme for the 10-dimensional values vector that anchors every principal's self-reported alignment profile. Following the pattern proven in Everest 44 (Ristretto255 Pedersen commitments), we commit to individual dimension values and aggregate across all dimensions. The dual-commitment approach enables both selective disclosure (hiding 9 dimensions while proving properties of 1) and vector-level proofs (proving aggregate capacity without revealing breakdown).

## Design Decision: Per-Dimension + Aggregate

We choose a two-tier commitment structure rather than a single aggregate commitment alone. Here's why:

1. **Selective Disclosure**: Privacy classes (Everest 113) require the ability to prove properties of specific values dimensions without revealing others. A per-dimension commitment Com_i = g^v_i × h^r_i allows a principal to generate a range proof or comparison proof over dimension i alone, while the other nine remain cryptographically opaque to the verifier.

2. **Vector-Level Efficiency**: The aggregate commitment Com_agg = Π Com_i allows proofs that concern the total values capacity (e.g., "sum of all 10 dimensions is between 50,000 and 100,000") without unpacking each dimension. This is essential for alignment scoring (Everests 126–145) where coarse-grained guarantees suffice.

3. **Homomorphic Derivation**: Pedersen commitments are additively homomorphic. If we store all per-dimension commitments, the aggregate is a free computation (simple point multiplication), and consistency is verifiable in under 5ms.

## Per-Dimension Commitment Structure

For each dimension d_i (where d_i ∈ {autonomy, transparency, resilience, ..., consensus_finding}) with value v_i ∈ [0, 10000]:

```
Com_i = g^v_i × h^r_i
```

where:
- **g** is the Ristretto255 basepoint (standardized generator).
- **h** is derived from a cryptographic hash-to-curve function seeded with "calm-zkac/values/h/v1". This ensures log_g(h) is unknown (the discrete-log assumption).
- **v_i** is the principal's self-reported value for dimension i, scaled to [0, 10000].
- **r_i** is fresh, uniformly random per-dimension masking randomness, drawn from the scalar field ℤ_q (where q is the Ristretto order).

The pair (v_i, r_i) constitutes the witness; the commitment Com_i is the public proof-of-binding. The randomness r_i is held in operator-controlled mlocked memory and only revealed during ZK proof generation (never on-chain).

## Aggregate Commitment Structure

The aggregate commitment aggregates all 10 per-dimension commitments:

```
Com_agg = g^(Σ v_i) × h^(Σ r_i) = Π Com_i (by homomorphism)
```

In expanded form:
```
Com_agg = g^(v_1 + v_2 + ... + v_10) × h^(r_1 + r_2 + ... + r_10)
```

This is verifiable by multiplying all per-dimension commitments together (point addition on the curve):
```
Π Com_i = Π (g^v_i × h^r_i) = g^(Σ v_i) × h^(Σ r_i) = Com_agg
```

Verification of consistency takes under 5ms on M-class hardware.

## On-Chain Storage

Commitments are stored as part of the `values_self_report` record (anchored in Everest 108):

```
values_self_report.payload = {
  "dimension_commitments": {
    "autonomy": "hex_encoded_point_1",
    "transparency": "hex_encoded_point_2",
    ...
    "consensus_finding": "hex_encoded_point_10"
  },
  "aggregate_commitment": "hex_encoded_point_agg",
  "timestamp": unix_seconds,
  "principal_id": ...
}
```

All points are compressed Ristretto255 points (32 bytes each) encoded in hexadecimal. The randomness r_1, ..., r_10 is never committed to the chain; it remains in the principal's operator-controlled secure memory, accessible only during proof generation.

## Cryptographic Properties

### Hiding Property

Both the per-dimension and aggregate commitments reveal no information about the underlying values under the Decisional Diffie-Hellman (DDH) assumption:

- An adversary observing Com_i = g^v_i × h^r_i cannot distinguish it from a commitment to any other value v'_i without knowledge of the discrete log.
- The randomness r_i is uniformly distributed over ℤ_q, ensuring the distribution of Com_i is independent of v_i.
- The aggregate Com_agg inherits hiding: revealing Com_agg leaks nothing about the breakdown across dimensions.

### Binding Property

The principal who created a commitment Com_i cannot later open it to a different value v'_i ≠ v_i (without breaking discrete log):

- To open Com_i to (v'_i, r'_i), the adversary would need g^v_i × h^r_i = g^v'_i × h^r'_i.
- Rearranging: g^(v_i - v'_i) = h^(r'_i - r_i).
- If log_g(h) is unknown, no efficient algorithm exists to satisfy this equation; the only solution is v_i = v'_i and r_i = r'_i.

## Selective Disclosure Example

Suppose a principal's privacy class for autonomy (dimension 1) permits disclosure, but transparency (dimension 2) does not. The principal can generate a Bulletproofs range proof over Com_1:

```
RangeProof := prove_range(v_1, r_1, Com_1, [0, 10000])
```

This proof is publicly verifiable and reveals that autonomy ∈ [0, 10000], but Com_2 and all other dimensions remain opaque—no information about their values is leaked. The verifier sees Com_2 on the chain but cannot extract or constrain v_2 from the proof.

## Curve and Generator Choice

All commitments use **Ristretto255**:
- Matches Everest 44 (Pedersen commitments in the Calm Pact).
- Matches Everest 45 (range proofs).
- Standardized and battle-tested (derived from Curve25519, immune to small-subgroup attacks, efficiently invertible).

The generator **g** is the canonical Ristretto basepoint (no secrets). The generator **h** is derived via hash-to-curve:

```
h := hash_to_ristretto("calm-zkac/values/h/v1")
```

This ensures:
1. **Deterministic**: identical h across all operators.
2. **Unexpandable**: no operator can retroactively influence h (no backdoor randomness).
3. **Unknown Discrete Log**: the discrete log log_g(h) is unknown under standard cryptographic assumptions.

## Performance Characteristics

On M-class hardware (Apple Silicon M1/M2/M3):

- **Commitment generation** (10 per-dimension + 1 aggregate): under 10ms.
  - Scalar multiplication (g^v_i and h^r_i): ~1ms per point, 10 points = ~10ms.
  - Aggregate (point addition): <1ms.
- **Consistency verification** (Π Com_i == Com_agg): under 5ms.
- **Commitment storage** (32 bytes per point): 11 commitments × 32 bytes = 352 bytes total.

This performance allows commitments to be generated and verified in real time during principal onboarding and re-report cycles.

## Cross-References and Dependencies

- **Everest 44**: Sister pattern for Ristretto255 Pedersen commitments; Calm Pact authentication uses the same construction.
- **Everest 45**: Bulletproofs range proofs; dimension values are proved to lie in [0, 10000] via range proof over Com_i.
- **Everest 106**: ValuesVector type definition; each of the 10 dimensions is defined here.
- **Everest 108**: Values self-report record; commitments are stored in the payload.
- **Everest 113**: Privacy classes; per-dimension commitments enable selective disclosure per privacy tier.
- **Everest 114**: Commitment binding; shared security properties.
- **Everests 126–145**: Alignment scoring and proofs; consume Com_agg and per-dimension commitments to generate alignment evidence without unmasking raw values.

## Summary

Everest 122 establishes a dual-commitment cryptographic anchor for the 10-dimensional values vector. Each dimension is independently committed via a Pedersen scheme, and the aggregate commitment enables vector-level proofs. The design preserves hiding and binding properties, allows selective disclosure for privacy-tiered verification, and performs in under 10ms for commitment generation and under 5ms for consistency checks. This foundation enables the privacy-respecting alignment framework of Everests 126–145 while maintaining zero-knowledge over individual dimension values.

— Calm, 2026-05-20
