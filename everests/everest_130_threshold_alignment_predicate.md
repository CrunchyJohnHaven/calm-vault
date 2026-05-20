# Everest 130 — Threshold Alignment Predicate

*Phase X — Values Alignment Computation. Prereq: Everest 129, 53.*

## Overview

The Threshold Alignment Predicate is the headline computation of Phase X: a single zero-knowledge proof that answers "Are this principal's values aligned with the values I require for cooperation?" The predicate returns a tri-valued result (True, False, Insufficient_Evidence) derived from a weighted distance metric over the principal's value commitments, without revealing the principal's underlying vector, per-dimension values, or exact alignment distance. It is the keystone of cooperative-trust handshake semantics, composable with Mission Match (Everest 143, Pact), State Baseline (Everest 141), and Compass (Everest 76) into a full disclosure and verification workflow.

## Predicate Specification

### Canonical Form

```
name: cwp.v0.values_aligned_within

parameters:
  counterparty_commitment_set: vector<pedersen_commitment>
    # Per-dimension Pedersen commitments to counterparty's target vector v_target
    
  weights: vector<field>
    # Public weight vector; Σ w_i = 1; non-negative
    # Dimensions correspond to v0 canonical basis (10 dimensions)
    
  tolerance: field ∈ (0, 1]
    # Threshold for alignment; typically τ ∈ {0.1, 0.2, 0.5, 1.0}
    
  dimensions_in_scope: vector<index> ⊆ [0..9]
    # Subset of v0 dimensions to evaluate; defaults to {0..9}
    # Enables selective alignment queries
    
output: {True, False, Insufficient_Evidence}
```

### Evaluation Logic

1. **Distance Computation (via Everest 128)**
   - Use the ZK bounded-difference proof from Everest 128 to compute the weighted L1 distance between the principal's committed value vector and the counterparty's target vector.
   - Distance formula: d = Σ_{i ∈ dimensions_in_scope} w_i · |principal_v[i] - target_v[i]|
   - Proof bounds: each dimension's difference in [-1, 1]; prove without revealing individual differences or absolute values.

2. **Alignment Decision**
   - **True**: distance ≤ tolerance AND all dimensions in dimensions_in_scope have sufficient evidence (see Evidence Requirement below).
   - **False**: distance > tolerance OR any in-scope dimension fails evidence check.
   - **Insufficient_Evidence**: proof generation fails because principal's chain does not contain sufficient value data to derive the principal value for one or more in-scope dimensions.

3. **Evidence Requirement**
   - A dimension has sufficient evidence if the principal has published an explicit or derived value commitment for that dimension on their authoritative chain (per Everest 53, values baseline).
   - If dimensions_in_scope includes a dimension with no published value, the proof cannot complete and the predicate returns Insufficient_Evidence rather than False. This prevents false negatives due to missing data.

## Privacy Properties

### Counterparty Learns

- The alignment bit (True, False, or Insufficient_Evidence).
- Freshness window (timestamp bounds on the principal's value commitments used in proof).
- Proof validity confirmation (non-repudiation of the operator's attestation).

### Counterparty Does NOT Learn

- The principal's actual value vector v_principal.
- Any per-dimension value or commitment.
- The exact weighted L1 distance d.
- Magnitudes of individual dimension differences.
- Which dimensions contributed most to alignment or misalignment.
- The principal's decision-making rationale or hidden preferences.

### Principal's Counterparty Vector Privacy

- The counterparty's target vector v_target is Pedersen-committed; the counterparty reveals only commitments, never the plaintext vector.
- The principal's operator does not learn v_target; the operator verifies the proof against commitments only.
- Enables mutual privacy: neither party reveals its full preference vector.

## Compositional Integration with Phase X Workflow

The Threshold Alignment Predicate is one component of a full cooperative-trust handshake defined by the Pact (Everest 143) and supporting proofs:

1. **Mission Match (Everest 143)**: Counterparty publishes a mission statement and verifies principal's mission compatibility.
2. **State Baseline (Everest 141)**: Counterparty and principal agree on an initial state snapshot.
3. **Compass (Everest 76)**: Counterparty and principal establish rate limits and request freshness bounds.
4. **Values Alignment (Everest 130)**: Counterparty verifies that principal's values fall within counterparty's acceptable tolerance.

A session can carry all four proofs, forming a complete cooperative-trust assertion. The alignment predicate output is treated as one input among many to consequential decisions, never as the sole input (per Everest 114 anti-discrimination safeguards).

## Counterparty-Side Workflow

1. **Publication Phase**: Counterparty publishes a commitment set to their target vector v_target, along with public weights and tolerance threshold.
2. **Disclosure Request**: Counterparty submits a disclosure request to the principal's operator, including the commitment set, weights, tolerance, and dimensions_in_scope.
3. **Proof Generation**: Principal's operator evaluates the disclosure against the principal's authoritative value chain. If evidence is sufficient, the operator generates a ZK proof of alignment without revealing the principal's vector.
4. **Proof Transmission**: Operator sends the proof (and metadata: freshness, dimensions covered) to the counterparty.
5. **Verification**: Counterparty verifies the proof using the published commitments. On success, the counterparty learns the alignment bit and freshness window.
6. **Decision**: Counterparty incorporates the alignment bit into broader cooperative-trust evaluation, alongside mission match, state baseline, and other factors.

## Disclosure-Class Defaults

Everest 130 integrates with the disclosure-class framework (per Everest 114) to enforce default privacy policies:

- **peer_ai_collective**: ALLOW (within trusted collective; mutual alignment checks expected).
- **foundation_grantmaker**: ALLOW (grantmakers evaluate alignment with their mission).
- **mentor**: ALLOW (mentors assess compatibility with mentee's stated values).
- **employer**: DENY (composition with Everest 114 employment-screening safeguards; values alignment cannot be used for employment screening).
- **financial**: DENY (financial institutions cannot unilaterally screen on values).
- **insurance**: PERMANENTLY DENY (values alignment is not admissible in insurance underwriting).
- **civic_coalition**: PRINCIPAL_CHOICE (principal decides whether to disclose alignment for coalition participation).

A principal can override defaults on a per-request basis, subject to anti-discrimination and transparency constraints (Everest 114).

## Anti-Discrimination Guard

The predicate output is a single bit. To prevent misuse as a sole input to high-impact decisions, the anti-discrimination guard (Everest 114) requires:

- The alignment bit may NOT be the sole input to consequential decisions (hiring, lending, insurance, resource allocation).
- Counterparty implementers pledge to incorporate alignment alongside other factors (domain expertise, mission fit, prior collaboration history, etc.).
- Audit logs must record that alignment was one of multiple decision inputs.
- Explainability: if alignment was True and the decision was negative, counterparty must disclose that other factors drove the decision.

This guard prevents weaponization of alignment as a veto mechanism by counterparties seeking to implement hidden selection criteria.

## Rate Limiting and Freshness

Integration with Everest 76 (Compass) and Everest 140 (Performance Budget):

- **Default rate limit**: 5 alignment requests per day per counterparty-class.
- **Cool-down on False**: After a False result, the counterparty must wait 1 hour before submitting another request. Prevents repeated probing.
- **Freshness bounds**: Proofs reference the principal's value commitments at a specific point in time. Counterparties can request proof freshness within the last N days (default: 30 days). Stale requests are rejected.
- **Performance budget**: Proof generation must complete in < 5 seconds (per Everest 140 performance SLO).

## Specification Example: Mission Alignment Query

A foundation grantmaker publishes:
- Target vector v_target: {0.8 (climate), 0.6 (equity), 0.3 (innovation), ...} (committed).
- Weights: {0.3, 0.3, 0.2, 0.05, ...} (public).
- Tolerance: τ = 0.25.
- Dimensions_in_scope: {climate, equity, innovation, governance} (4 dimensions).

A principal's operator receives the request and evaluates the principal's chain:
- Principal's v_principal: {0.75 (climate), 0.65 (equity), 0.35 (innovation), 0.4 (governance), ...} (committed, not disclosed).
- Compute weighted L1: 0.3·|0.75-0.8| + 0.3·|0.65-0.6| + 0.2·|0.35-0.3| + 0.05·|0.4-?| = 0.015 + 0.015 + 0.01 + (error if governance missing).
- If all evidence present: d ≈ 0.04 ≤ 0.25, so True.
- Operator generates proof: no disclosure of v_principal or exact d, only True.
- Foundation learns: "This principal's values are aligned within our tolerance." Foundation can proceed with further evaluation.

## Cross-References

- **Everest 45**: Confidentiality framework; values are private by default.
- **Everest 52**: Canonical predicate form; Everest 130 follows canonical specification.
- **Everest 53**: Values baseline; defines the v0 canonical 10-dimension value space.
- **Everest 76**: Compass; rate limiting and freshness bounds.
- **Everest 107**: Zero-knowledge proof architecture.
- **Everest 114**: Anti-discrimination and transparency safeguards; governs use of alignment in consequential decisions.
- **Everest 122**: Pedersen commitments; underlies the commitment set for counterparty vectors.
- **Everest 126**: Alignment metric definition; mathematical framework for distance computation.
- **Everest 128**: Bounded-difference ZK proof; engine for distance computation.
- **Everest 129**: Weighted distance aggregation; mathematical component of Everest 130 evaluation.
- **Everest 140**: Performance budget; < 5s proof generation.
- **Everest 141**: State baseline; sibling predicate in Phase X.
- **Everest 143**: Pact (Mission Match); compositional sibling; full handshake including values alignment.

## Acceptance Criteria

1. Predicate `cwp.v0.values_aligned_within(counterparty_commitment_set, weights, tolerance, dimensions_in_scope)` is defined and returns a tri-value.
2. Evaluation logic (distance, evidence, decision) is specified without ambiguity.
3. Privacy properties are guaranteed: counterparty learns only the bit and freshness, not the principal's vector or exact distance.
4. Compositional integration with Phase X (Pact, State Baseline, Compass) is defined.
5. Counterparty-side workflow (publication, request, proof generation, verification) is fully specified.
6. Disclosure-class defaults and anti-discrimination guards are in place.
7. Rate limits and performance budget are enforced.
8. The predicate is the single headline bit of Phase X: "Are values aligned enough for cooperation?"

## Implementation Notes

The proof system for Everest 130 relies on Everest 128 (bounded-difference ZK) and Everest 129 (weighted aggregation). The operator's implementation must:

- Load the principal's value commitments from the authoritative chain (per Everest 53).
- Parse the counterparty's commitment set and public parameters.
- Invoke the Everest 128 proof engine with the computed weighted distance.
- Return the tri-valued result and proof metadata (freshness, dimensions, evidence status).
- Log the request and result for audit compliance.

---

— Calm, 2026-05-20
