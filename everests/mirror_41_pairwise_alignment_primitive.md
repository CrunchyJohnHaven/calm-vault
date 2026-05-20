# Mirror Everest 41: Pairwise Alignment Computation Primitive

## Phase XII / Prerequisite 40

This primitive enables two principals to determine the intersection of their published value-commitments and compute joint alignment signals across shared predicates, without revealing non-shared positions.

## Overview

The pairwise alignment primitive is the cryptographic kernel of the Mirror exchange (E58). Each principal publishes a set of evaluable predicates—statements about the world they commit to keep answerable—along with per-predicate evaluation commitments (the predicate's truth value under specified conditions, or a withhold signal). The primitive computes: (1) which predicates both principals value, (2) whether each shared predicate aligns across the two principals, (3) an alignment vector capturing the degree of overlap.

This enables the Mirror exchange to match principals on genuinely shared ground without revealing unshared positions, satisfying the withhold-any-bit composition (E51).

## Inputs

**Principal A:**
- Predicate set P_A = {p_1, p_2, …, p_m}
- Evaluation commitments E_A = {e_1, e_2, …, e_m} where e_i ∈ {true, false, withhold}

**Principal B:**
- Predicate set P_B = {q_1, q_2, …, q_n}
- Evaluation commitments E_B = {f_1, f_2, …, f_n} where f_j ∈ {true, false, withhold}

Both sets are published on a tamper-evident log (user-state attestation per ZKBB-User 100).

## Outputs

**Intersection Set:**
- V_shared = P_A ∩ P_B (the predicates both principals recognize)
- |V_shared| = k ≤ min(m, n)

**Per-Predicate Joint Bits:**
- For each v ∈ V_shared, compute alignment_bit(v):
  - 1 if both principals' commitments evaluate to the same truth value (both true or both false)
  - 0 if commitments differ
  - withhold if either commitment is withheld

**Alignment Vector:**
- α = [alignment_bit(v_1), alignment_bit(v_2), …, alignment_bit(v_k)]
- alignment_score = (count of 1s) / k (fraction of shared predicates where both agree)

## Algorithm Steps

**Step 1: Vocabulary Intersection**
Compute V_shared by exact string match on predicate identifiers. Record ordinal position in both sets. Preserve order deterministically (lexicographic tiebreak).

**Step 2: Per-Predicate MPC Sketch**
For each v ∈ V_shared:
- Retrieve commitment_A(v) and commitment_B(v)
- If either is withhold: output withhold; skip further processing
- If both are true or both are false: alignment_bit(v) = 1
- Otherwise: alignment_bit(v) = 0

This step is non-interactive for withhold-or-evaluate commitments (no secure multi-party computation needed if commitments are already published with cryptographic binding).

**Step 3: Vector Aggregation**
Concatenate alignment bits in V_shared order. Compute alignment_score as unweighted fraction. Record:
- raw_agreement_count
- total_shared_predicate_count
- withhold_count (withheld predicates excluded from both denominator and alignment score)

## Composition with Other Primitives

**Composition with MPC (E58):**
The alignment vector feeds into the Mirror exchange mechanism (E58), where principals use alignment_score as a fairness metric. High alignment signals are correlated with beneficial exchange; low or zero scores terminate negotiation.

**Composition with Withhold-Any-Bit (E51):**
When a principal withholds on a predicate, that predicate is removed from V_shared without signaling which principal withheld it. The intersection is computed on the reduced set. This preserves privacy: an observer cannot infer which predicates either principal was unwilling to evaluate.

**Composition with E40 and E42:**
E40 (prerequisite) establishes the user-state attestation layer on which predicates are published. E42 (successor) uses alignment vectors to guide principal matching in cohort formation.

## Properties

**Symmetry:** alignment_bit(v) is identical for both principals; order of computation does not affect the output.

**Fairness:** No principal gains advantage by withholding or false-committing. The alignment score is symmetric and both principals observe the same computation.

**No Information Leak Beyond Stated Output:** V_shared and α are revealed; P_A \ P_B and P_B \ P_A remain private. Withholding is not attributed. Evaluation commitments on non-shared predicates are not observed.

**Determinism:** Given identical inputs, the computation produces identical outputs.

## Acceptance Tests

**T-M41.1:** Intersection of two identical predicate sets yields all predicates with alignment_score = 1.0.

**T-M41.2:** Intersection of disjoint predicate sets yields empty V_shared.

**T-M41.3:** Withholding on a predicate in V_shared removes it from alignment computation without signaling which principal withheld.

**T-M41.4:** Alignment vector length equals |V_shared|; withhold signals do not expand vector length.

**T-M41.5:** Alignment_score is invariant to predicate ordering within each principal's original set.

## Composition Map

- **E40** (prerequisite): user-state attestation, predicate publication
- **E41** (this primitive): pairwise alignment computation
- **E42** (successor): cohort matching using alignment signals
- **E49** (reference): reciprocal disclosure protocol (uses alignment to gate disclosure depth)
- **E51** (reference): withhold-any-bit mechanism (consumes alignment vector without attribution)
- **E58** (reference): Mirror exchange main loop (uses alignment_score for negotiation fairness)

## Version 1 Questions

1. Should alignment_score weight predicates by relevance rank, or remain unweighted?
2. Does withhold trigger principal-to-principal notification (abort negotiation), or silent reduction of V_shared?
3. Should the primitive emit a "sufficiency" flag if |V_shared| < threshold, or leave that to E58?
4. Is the predicate identifier comparison case-sensitive and whitespace-sensitive?
5. Should commitment publication timestamp be part of the input, for freshness validation?

## Signoff

— Calm, 2026-05-20

