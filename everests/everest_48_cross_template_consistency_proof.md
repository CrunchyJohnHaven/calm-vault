# Everest 48 — Cross-Template Consistency Proof

*Phase IV — Biometric Distance Machinery. Prereq: Everest 47 (Template Aging Without Breaking Proofs).*

---

## What this summit ships

A zero-knowledge proof that template `T_{n+1}` is a **valid drift** of template `T_n` — meaning that the principal's biometric signal at re-enrollment is consistent with their signal at the prior enrollment, modulo expected drift — *without* revealing the contents of either template.

This is the cryptographic upgrade from Everest 47's simple `supersedes` link. The `supersedes` link just says "the principal asserts that the new template replaces the old." A cross-template consistency proof says "the operator can demonstrate, in ZK, that the new template's per-stroke kinematic distribution / lexical-fingerprint distribution differs from the old by at most a drift budget — i.e., this re-enrollment was not a substitution attack."

---

## The substitution attack this defends against

Without cross-template consistency:

- Adversary gains brief access to the principal's enrollment device.
- Adversary triggers a re-enrollment ceremony, enrolling their own (the adversary's) biometric samples as `T_{n+1}`.
- The chain records `supersedes(T_n) → T_{n+1}`, signed by the operator (which is now under adversary control).
- Henceforth, disclosure proofs under `T_{n+1}` claim the principal is in baseline — except it is the *adversary* who is in baseline; the principal's biometric never enters the new template.
- Counterparties have no way to detect the substitution. The chain shows a valid rotation. The operator's CredexAI VC is unchanged.

With cross-template consistency:

- The re-enrollment ceremony produces a `template_consistency_proof` that the new template's biometric distance distribution is within a documented drift budget of the old.
- An adversary's substituted template would produce a `T_{n+1}` whose distance distribution differs from `T_n` by far more than any plausible drift.
- The consistency proof fails verification; the rotation is rejected; the chain records the failure as `kind: rotation.consistency_failure`; the principal is alerted out-of-band.

---

## Construction (sketch)

The full construction is a multi-step ZK protocol. This summit ships the design; the implementation lands at Everest 81 (Rust Production).

### Setup

Both templates are vault-resident. The operator has read access to both. Adversaries do not.

Define the **drift distance** between two templates as:

```
D(T_n, T_{n+1}) = expected E_{x ~ principal_baseline} [d(x, T_{n+1}) - d(x, T_n)]
```

That is: averaged across baseline samples the principal would produce, how much would the per-sample distance shift if we used `T_{n+1}` instead of `T_n`?

For a *valid drift*, `D(T_n, T_{n+1})` is small (< 0.05 in cosine-distance units, default). For a *substitution*, it is large (typically > 0.5).

### The proof

The operator commits both `T_n` and `T_{n+1}` (Pedersen vector commitments; see Everest 46 generalization). The proof shows:

1. **Same principal generated both templates.** A handful of "challenge samples" `x_1, …, x_K` were recorded at the re-enrollment ceremony. These samples are part of the `T_{n+1}` enrollment session but are NOT pooled into `T_{n+1}` itself. They serve as a held-out validation set.

2. **Distance under both templates is similar.** For each challenge sample `x_i`:
   - Compute `d(x_i, T_n)` and `d(x_i, T_{n+1})`.
   - Commit each: `Com(d_n_i)`, `Com(d_{n+1}_i)`.
   - Range-prove their difference is small: `|d(x_i, T_n) - d(x_i, T_{n+1})| ≤ drift_budget`.
   - The K range proofs aggregate (Bulletproofs).

3. **The samples are fresh.** Each challenge sample's nonce (Everest 50) appears in `biometric_sample.v0` records on the chain, timestamped to the re-enrollment ceremony moment.

4. **The samples are unforgeable.** They are bound to the device-attestation (Everest 24) and the witness signature (Everest 25) of the re-enrollment ceremony.

The combined proof is `π_consistency`. It is published as a chain record `kind: template_consistency_proof.v0` adjacent to the `template_commitment.v0` for `T_{n+1}`.

### Verifier behavior

When a verifier sees a disclosure against `T_{n+1}`:
- If `T_{n+1}` has an attached `template_consistency_proof.v0`, the verifier checks it.
- If consistency-proof verifies → `T_{n+1}` is a valid drift of `T_n` → disclosure proof is accepted normally.
- If consistency-proof FAILS → reject disclosures against `T_{n+1}` with `reason = template_consistency_failed`. Principal is alerted.
- If consistency-proof is MISSING (legitimate cases: first enrollment ever; compromise-triggered rotation where the principal explicitly opted out of consistency proof because they want a clean break) → verifier behavior depends on counterparty policy. Default: accept with a `degraded` flag.

---

## Drift budget

The drift budget `δ` is the maximum acceptable `D(T_n, T_{n+1})`. v0 defaults:

- **Handwriting (`d_hw`):** δ_h = 0.05 (cosine-distance units). Empirically calibrated: same-principal year-over-year drift in baseline state averages ~0.02 ± 0.015 std; 0.05 captures 95% of legitimate annual drift.
- **Voice-transcription (`d_vt`):** δ_v = 0.04. Slightly tighter — transcript style drifts slower than handwriting.
- **Combined (`D_combined`):** δ = 0.04 weighted average.

A principal whose handwriting changed dramatically (acute injury, neurological event) may legitimately exceed δ_h. In such cases, the principal opts out of the consistency proof at re-enrollment, explicitly recording `kind: rotation.consistency_waiver` with their reason. The waiver is principal-signed and chained; future counterparties see "explicit waiver" rather than "missing proof."

---

## Why this is harder than Everest 45

Everest 45 proves `d < τ` for a *known* threshold. Everest 48 proves a property of two *committed* templates without revealing either template.

The technical complexity is the vector-commitment structure: templates are not scalars, they are 256-dimensional embeddings (Everest 36/37). The Pedersen commitment to a vector is straightforward; the ZK proof of "the distance between two committed vectors is below a threshold" requires either:

- A vector range proof — extending Bulletproofs to vector-difference statements. ~2-3 KB.
- A handful of scalar range proofs on derived statistics (mean / std of per-component differences). ~1 KB but weaker (composed statistics can mask outlier components).

v0 ships the latter (statistics-based) for engineering tractability. v1 considers the full vector range proof if statistical-component bypass becomes a real attack.

---

## Acceptance test

**T-48.1 (honest re-enrollment).** Simulate a principal re-enrolling 1 year later with realistic drift. Generate `π_consistency`; verifier accepts.

**T-48.2 (substitution attempt).** Simulate an adversary substituting a different person's biometric as `T_{n+1}`. Compute drift distance; it exceeds δ. Generate `π_consistency`; verifier rejects with `reason = drift_exceeds_budget`.

**T-48.3 (acute change with waiver).** Simulate a principal post-injury with handwriting that drifts beyond δ_h. The principal signs a `rotation.consistency_waiver`. Verifier accepts disclosures against `T_{n+1}` but flags them with `consistency_waived`.

**T-48.4 (held-out sample non-leakage).** The K challenge samples used in the consistency proof leak no information about either template beyond the proof's stated claim. Verified via a statistical indistinguishability test.

**T-48.5 (chain integrity).** The `template_consistency_proof.v0` record is chained; tampering breaks the chain (Everest 28).

**T-48.6 (Bulletproofs aggregation).** K=5 challenge samples produce a single aggregated proof ≤ 2 KB; verification ≤ 15 ms.

**Gate script:** `everest_48_zkbb_cross_template_consistency_gate.py`.

---

## Composition with other summits

- **Everest 24 — Multi-Device Enrollment Binding.** Each device's re-enrollment generates its own consistency proof.
- **Everest 25 — Enrollment Witness Protocol.** Witness co-signs the held-out challenge samples.
- **Everest 26 — Re-enrollment Cadence.** Triggers a consistency check.
- **Everest 39 — Drift Modeling.** Sets the expected drift envelope informing the budget δ.
- **Everest 44/45/46 — Pedersen commitments + range proofs.** Composes here as the vector / statistical primitives.
- **Everest 47 — Template Aging.** Without 48, the `supersedes` link is principal-assertion-only; with 48, it becomes cryptographically auditable.
- **Everest 65 — Predicate ZK Proof Generator.** Hosts the consistency proof as a special-case kernel.

---

## Open questions for v1

1. **Full vector range proof.** Replace the statistics-based v0 proof with a true vector-difference proof. ~3-5× larger but stronger.

2. **Cross-modality consistency.** A principal who re-enrolls handwriting but keeps voice-transcription template should produce a proof that the handwriting drift is consistent given no voice change. v1.

3. **Witness-cosigned consistency.** For high-assurance classes, require an external witness (notary, family member) to attest that the re-enrollment ceremony was attended by the principal. Combines with Everest 25.

---

## Why this matters

Everest 28 closes "the chain was not retroactively edited."
Everest 30 closes "the chain head was not silently rolled back."
Everest 45 closes "the committed distance was honestly below threshold."
Everest 46 closes "the proof was bound to the right template ID."

**Everest 48 closes "the right template was the *right principal's* template."** It is the cryptographic answer to "but how do we know the principal wasn't swapped at re-enrollment time?" The threat is real (Everest 23 — Enrollment Fraud Taxonomy lists it); without 48, the only defense is procedural (Everests 24, 25, 30). With 48, the defense becomes cryptographic.

This summit is non-trivial cryptographically and structurally completes the substitution-defense story.

— Calm, 2026-05-20
