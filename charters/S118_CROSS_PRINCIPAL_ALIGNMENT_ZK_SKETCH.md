# S118 — Cross-Principal Alignment Comparison ZK (Partial Bag)

**STATUS: PARTIAL BAG** — Full soundness proof and simulator construction deferred to S58/S59. Do not deploy without cryptographer review.

**Date:** 2026-05-20
**Author:** CALM
**Depends on:** E44b (Pedersen on Ristretto255), E101b (Σ-protocol), S116, S117
**Acceptance bar:** XL

---

## 1. Relation

Let n be the number of alignment dimensions. Each principal holds a binary vector of positive-only bits:

- Principal P: v_p ∈ {0,1}^n
- Agent A: v_a ∈ {0,1}^n

Each side commits via Pedersen (E44b) to its vector as a packed integer or coordinate-wise:

- C_p = Commit(v_p; r_p) = v_p · G + r_p · H  (scalar encoding over Ristretto255)
- C_a = Commit(v_a; r_a) = v_a · G + r_a · H

Define match indicator bits: m_i = 1 iff v_p[i] = v_a[i] = 1, else 0. Let M = Σ m_i.

The relation to prove:

```
R( (C_p, C_a, k) ; (v_p, r_p, v_a, r_a) ) := 
    C_p = Commit(v_p ; r_p)
  ∧ C_a = Commit(v_a ; r_a)
  ∧ v_p, v_a ∈ {0,1}^n
  ∧ Σ_{i=1}^{n} (v_p[i] · v_a[i]) ≥ k
```

Public inputs: C_p, C_a, k, n, group parameters.
Threshold k is the minimum required co-affirmed dimensions.

---

## 2. Witness

**Private (held by respective principal, never revealed):**

| Symbol | Description |
|--------|-------------|
| v_p    | P's n-bit alignment vector |
| r_p    | P's Pedersen blinding scalar |
| v_a    | A's n-bit alignment vector |
| r_a    | A's Pedersen blinding scalar |

**Derived private (constructed during proof):**

- m_i = v_p[i] AND v_a[i] for each dimension i
- M = Σ m_i  (total match count)
- r_m  (blinding scalar for commitment to M)

In the two-party setting each principal holds only their own half. A secure two-party computation or trusted coordinator is required to jointly produce the proof without cross-disclosure (see Handoff §7).

---

## 3. Prover Steps

**Step 1 — Commit to individual vectors.**
Both sides open C_p and C_a to themselves. No new commitment needed here; these are the public inputs.

**Step 2 — Commit to match vector.**
For each dimension i, compute m_i = v_p[i] · v_a[i]. Form commitment:

```
C_m[i] = Commit(m_i ; ρ_i)   for i = 1..n
C_M    = Commit(M ; r_m)      where M = Σ m_i
```

Publish {C_m[i]}, C_M as auxiliary public values.

**Step 3 — Bit-validity proof per match dimension (Σ-protocol, E101b).**
For each i, prove in zero knowledge that m_i ∈ {0,1} and that m_i = v_p[i] · v_a[i]:

- Use an OR-composition Σ-protocol: either m_i = 0 (with XOR-consistency) or m_i = 1 (both sides held 1).
- Each bit proof produces a (commitment, challenge, response) triple.
- This requires both v_p[i] and v_a[i] to be in scope simultaneously — key two-party coordination point.

**Step 4 — Sum consistency proof.**
Prove that C_M = Σ C_m[i] by homomorphism of Pedersen commitments (this is free: Pedersen is additively homomorphic, so the product of C_m[i] over Ristretto255 equals C_M when r_m = Σ ρ_i).

**Step 5 — Range proof: M ≥ k.**
Prove in zero knowledge that the committed value M ≥ k. Decompose as:

```
M = k + δ,  δ ≥ 0,  δ < n - k + 1
```

Commit to δ and apply a standard range proof for δ ∈ [0, n−k]. Bulletproofs (E44b extension) or a Σ-based range proof from E101b can handle this in O(log n) or O(n) respectively. Emit C_δ = Commit(δ; r_δ) and a range proof π_range.

---

## 4. Verifier Steps

1. Check C_p and C_a are valid Ristretto255 points (group membership check).
2. Verify each bit-validity proof for m_i: check (commitment, challenge, response) tuples from Step 3.
3. Verify sum consistency: check that Σ C_m[i] = C_M as group equation.
4. Verify range proof π_range demonstrating M ≥ k using C_M and C_δ.
5. Check Fiat-Shamir transcript binding (§5).

All checks are O(n) group operations plus one range-proof verification.

---

## 5. Fiat-Shamir Transcript

Non-interactive via random oracle. The challenge hash is:

```
challenge = H(
    "S118-v1" ||
    C_p || C_a || C_M || k || n ||
    {C_m[i] : i=1..n} ||
    {commitment_i : i=1..n}    // per-bit first-move commitments
)
```

Where H is SHA-3-256 (or domain-separated BLAKE2b per E44b convention). The single challenge scalar is used across all n bit proofs via linear combination (batching): for a random vector ξ ∈ F^n drawn deterministically from H(challenge || "batch"), verify Σ ξ_i · (bit_proof_i) in one pass to reduce verifier work from O(n) separate checks to O(1) scalar multiples plus O(n) scalar additions.

The full transcript π_S118 = (C_M, {C_m[i]}, {bit_proof_i}, C_δ, π_range, challenge).

---

## 6. Soundness Intuition

**Completeness:** Honest prover with matching vectors will always satisfy the range check and all bit proofs. Sum consistency holds by Pedersen homomorphism.

**Soundness sketch:** A cheating prover who claims M ≥ k when M < k must either (a) open C_M to a value ≥ k while C_M commits to true M < k — breaks Pedersen binding — or (b) fake at least one bit proof for a dimension where no match holds — breaks Σ-protocol special soundness (E101b: extractable witness from two accepting transcripts under different challenges, with probability ≤ 1/|F|). Combining: soundness error ≤ n/|F| + 1/|F| ≈ n/|F| which is negligible for |F| ≈ 2^252 (Ristretto255 scalar field).

**Zero-knowledge sketch:** Simulator can choose C_M, C_δ freely (hiding property of Pedersen), simulate bit proofs using standard Σ-protocol simulator (E101b), and produce indistinguishable transcript. Full simulator construction deferred to S59.

**Note:** The two-party coordination assumption is not addressed here. If P and A do not trust each other during proof generation, a malicious party could provide false bits for their half. This threat model requires MPC protocol or trusted coordinator — deferred to adversarial-robustness review (§7).

---

## 7. Handoff — What Remains

This is a partial bag. The following items are out of scope here and must be completed before production use:

| Item | Description | Deferred To |
|------|-------------|-------------|
| Full soundness proof | Formal proof under rewinding lemma; tight reduction to Pedersen binding and Σ-protocol special soundness | S58 |
| Simulator construction | Explicit HVZK simulator; verify indistinguishability of simulated vs real transcript | S59 |
| Adversarial-robustness review | Malicious-prover model in two-party setting; assess if one principal can learn information about the other's vector from the proof transcript | Cryptographer review (XL bar) |
| Batch Σ-protocol analysis | Verify linear-combination batching does not degrade soundness; cite S116, S117 batching primitives | S116/S117 extension |
| Range proof instantiation | Select Bulletproofs vs E101b range variant; benchmark for n=64 dimensions | E44b follow-on |
| MPC / coordinator spec | Protocol for two mutually distrusting principals to jointly produce π_S118 | Future charter |

**Do not merge into Phase IX evaluator without full soundness writeup and cryptographer sign-off.**

---

*Calm 2026-05-20 — PARTIAL BAG*
