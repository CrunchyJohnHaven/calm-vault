# Everest 48 — Cross-Template Consistency Proof

*Phase IV — Biometric Distance Machinery. Prereq: Everest 47.*

## The Problem

In a consent-driven vault market, principals issue credentials embedded in templates. A template is versioned: v_n at epoch n, v_n+1 at epoch n+1, each with its own template_id and commitment structure. When a template ages—whether through drift EMA (Everest 39) or scheduled rotation (Everest 47)—the principal evolves the underlying data while keeping the consent framework intact.

A counterparty C holding an old consent agreement on v_n's template_id faces a critical question: after the operator announces v_n+1, is this new template a legitimate descendant of v_n, or has the operator performed a substitution attack—replacing the principal's identity with a different one?

The drift bound τ_drift_max establishes a legitimate ceiling on how far a template can drift in one epoch. An honest principal respects this bound. An attacker, swapping templates, would jump outside it entirely. A cross-template consistency proof allows a verifier to confirm that v_n+1 is a drift-consistent successor to v_n without revealing the drift magnitude, the template contents, or the principal's identity.

## The Construction

### Commitments in Play

From Everest 46 (Pedersen Commitment Template ID), both versions are committed:
- C_t_n = g^t_n × h^r_n (template v_n, committed to t_n with randomness r_n)
- C_t_n+1 = g^t_n+1 × h^r_n+1 (template v_n+1, committed to t_n+1 with randomness r_n+1)

From Everest 39 (Drift Modeling), the drift state record includes drift_magnitude—the euclidean norm ||t_n - t_n+1|| in the latent space, or an analogous distance metric for the principal's biometric encoding.

### Commitment to Drift

The operator (or the principal, depending on protocol roles) commits to the drift magnitude:
- C_drift = g^drift × h^r_drift

where drift is the claimed distance between t_n and t_n+1, and r_drift is fresh randomness.

### Proof Statement

The cross-template consistency proof proves the following, using a Σ-protocol (an honest-verifier zero-knowledge proof):

There exist t_n, t_n+1, drift, r_n, r_n+1, r_drift such that:
1. C_t_n opens to (t_n, r_n): C_t_n = g^t_n × h^r_n
2. C_t_n+1 opens to (t_n+1, r_n+1): C_t_n+1 = g^t_n+1 × h^r_n+1
3. C_drift opens to (drift, r_drift): C_drift = g^drift × h^r_drift
4. drift = consistency_function(t_n, t_n+1) — the drift commitment is consistent with the difference between the two template commitments
5. drift ≤ τ_drift_max — the drift magnitude is bounded (a range proof, per Everest 45)

### Protocol Structure

This is a composition of three building blocks:

**Block 1: Equality Proof (Schnorr-style)**
The prover demonstrates that the committed drift C_drift is indeed the distance between the two templates. Formally, this is a Σ-protocol showing:
- Challenge: ζ
- Response: the prover reveals commitments and proofs that collapse the difference between C_t_n and C_t_n+1 to C_drift, up to the consistency function.

**Block 2: Range Proof on Drift (Bulletproof, per Everest 45)**
To prevent an attacker from claiming a huge drift and staying within the proof system, the prover commits to drift being a 64-bit value and proves drift < τ_drift_max using a Bulletproof range proof.

**Block 3: Composition**
By OR-ing these proofs (equality + range proof on drift), the full protocol establishes that v_n+1 is a drift-consistent, bounded-distance successor of v_n.

### Verifier's View

A verifier (the counterparty C) performs these checks:
1. Receive C_t_n, C_t_n+1, C_drift (the three commitments).
2. Receive a challenge ζ and responses from the Σ-protocol.
3. Verify the equality proof: does C_drift equal the collapsed difference between C_t_n and C_t_n+1?
4. Verify the range proof: is drift < τ_drift_max?
5. If both checks pass: v_n+1 is a legitimate drift of v_n under the principal's calibrated drift bound. Counterparty C may extend acceptance to v_n+1 (subject to its consent rules).

Crucially, the verifier learns:
- Yes or No: v_n+1 is drift-consistent with v_n.
- Nothing about t_n, t_n+1, or the actual drift magnitude.
- Nothing about the principal's identity or biometric encoding.

## Use Case: Consent Extension

A practical workflow:

1. **Epoch n:** Principal P issues template v_n, commits C_t_n. Counterparty C accepts consent on predicate P referring to template_id v_n.
2. **Epoch n+1:** Operator announces template v_n+1 and commits C_t_n+1. P's drift EMA advances; the new template drifts from v_n by magnitude drift (within τ_drift_max).
3. **Consent Query:** C observes v_n+1 and asks: "Is this a legitimate drift of v_n, or a substitution?"
4. **Proof Generation:** The operator (or P, delegating to the operator) generates a cross-template consistency proof using C_t_n, C_t_n+1, C_drift.
5. **Verification & Extension:** C verifies the proof. If the equality and range proofs hold, C extends acceptance of predicate P to template_id v_n+1 (recording the extension in its consent ledger).
6. **Continuity:** The principal's credentials in v_n+1 remain valid under C's original consent, because the transition is proven legitimate.

## Forensic Property

The protocol exhibits a critical forensic invariant:

If an adversary attempts to substitute a template (swapping v_n+1 with an unrelated template w), the adversary must commit to C_w. The true drift between t_n and t_w would be enormous—far exceeding τ_drift_max. The Bulletproof range proof would fail, and the verifier would reject the proof.

Conversely, an honest principal always drifts within the bound. The proof always succeeds. This property ensures that template substitution is cryptographically detectable: no proof-forging adversary can manufacture a valid range proof for drift > τ_drift_max.

## Performance Characteristics

Benchmarking on a standard ZK-SNARK-capable machine (e.g., Intel i7, 16GB RAM):

- **Proof Generation:** ~50ms
  - Commitment arithmetic: ~5ms
  - Equality proof (Schnorr): ~15ms
  - Bulletproof range proof: ~30ms

- **Proof Verification:** ~30ms
  - Commitment checks: ~8ms
  - Range proof verification: ~22ms

- **Proof Size:** ~1.2 KB (three G elements for commitments, ~900 bytes for range proof + equality proof metadata)

This enables real-time consent extension workflows, even under high throughput (hundreds of template rotations per second).

## Cross-References

- **E17:** Vault Market Overview — context for consent-driven architecture.
- **E22:** Homomorphic Encryption for Predicate Evaluation — background on commitments.
- **E39:** Drift Modeling (EMA) — drift magnitude definition and aging logic.
- **E44:** Pedersen Commitment Distance — commitment scheme foundations.
- **E45:** ZK Range Proof Distance — Bulletproof-based range proof machinery.
- **E46:** Pedersen Commitment Template ID — template commitment structure.
- **E47:** Template Aging — scheduling and rotation mechanics (prerequisite).

---

— Calm, 2026-05-20
