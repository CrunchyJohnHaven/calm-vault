# Everest 45 — ZK Range Proof: Acceptance & Transcript Addendum

*Companion to [`everest_45_zk_range_proof.md`](everest_45_zk_range_proof.md). Adds the Fiat-Shamir transcript binding spec, multi-modal aggregation details, and the named acceptance-test suite (T-45.1 through T-45.9) that the v0.1 implementation must pass.*

---

## §A. Fiat-Shamir transcript ordering

The non-interactive Bulletproofs variant uses Fiat-Shamir with SHA-3 / SHAKE-256 over a domain-separated transcript. The transcript MUST include, in **exactly this order**, with each element length-prefixed:

```
"calm-witness-v0/range-proof"            // 27-byte domain-separator string
|| H_chain                                // Sigsum-anchored chain head (Everest 30), 32 bytes
|| template_id_commitment                 // Pedersen commitment to template ID (Everest 46), 32 bytes
|| τ_int                                  // threshold, big-endian fixed-point uint32 (or uint64 if v0 chose 64-bit)
|| C                                      // distance commitment, 32-byte Ristretto255 element
|| g                                      // generator g, 32 bytes
|| h                                      // generator h, 32 bytes
```

This ordering and these fields together produce the per-proof challenge. Any cross-implementation port must follow the byte-exact transcript layout or proofs will not cross-verify.

### What each binding closes

| Binding | Closes | Attack it blocks |
|---|---|---|
| `H_chain` | Replay across time | A proof valid for chain head H₁ at time t₁ cannot be reused at t₂ when the chain head is H₂ |
| `template_id_commitment` | Substitution of principals | A proof generated against template T₁ cannot be presented as a proof against template T₂ |
| `τ_int` | Threshold confusion | A proof for "d < 0.85" cannot be reused as a proof for "d < 0.50" |
| `g, h` | Generator-rotation attacks | A future migration to a different curve / generator pair re-keys all proofs cleanly |
| Domain separator | Cross-protocol replay | A Calm Pact Σ-proof cannot be replayed as a Calm Witness range proof, even with overlapping inputs (Everest 92) |

The domain-separator string is normative; alternate strings produce incompatible proofs and is the v1 migration path if anything below it changes.

---

## §B. Multi-modal proof aggregation

v0 supports three composition modes:

### B.1 Single-modality

```
Statement:    ∃ (d, r) such that
              C = g^d · h^r ∧ 0 ≤ d < τ_int

Proof:        π_range  (~672 bytes for 32-bit range, ~736 bytes for 64-bit)
```

### B.2 Independent dual-modality (Everests 36 + 37)

Two single-modality proofs concatenated:

```
Statement:    (d_hw, r_hw, d_vt, r_vt) jointly satisfy:
              C_hw = g^{d_hw} · h^{r_hw}
              ∧ C_vt = g^{d_vt} · h^{r_vt}
              ∧ 0 ≤ d_hw < τ_h_int
              ∧ 0 ≤ d_vt < τ_v_int

Proof:        (π_hw, π_vt)  (~1.3 KB total — no aggregation gain)
```

### B.3 Aggregated dual-modality (preferred)

Bulletproofs aggregation packs both range proofs into a single inner-product argument:

```
Public input: (C_hw, C_vt, τ_h_int, τ_v_int, H_chain, template_commitment, g, h)
Witness:      (d_hw, r_hw, d_vt, r_vt)
Proof:        π_aggregated  (~800 bytes — significant gain over 1.3 KB independent)
```

The aggregated form is the v0.1 production target. Independent form is the v0 placeholder.

### B.4 Fused-distance (Everest 38)

When the combined distance is computed as a public linear combination `d_combined = α · d_hw + β · d_vt` (with public scalars α, β chosen at enrollment for likelihood-ratio fusion), the homomorphism on Pedersen allows the verifier to derive `C_combined = C_hw^α · C_vt^β` from the two component commitments. A single range proof over `(C_combined, τ_combined)` then suffices:

```
Proof:        π_fused  (~672 bytes — smallest of all four modes)
```

This is the most bandwidth-efficient option. v1.

---

## §C. Acceptance test suite (T-45.1 through T-45.9)

Each test is named and falsifiable. The gate script `everest_45_zkbb_range_proof_gate.py` runs all nine and exits 0 only if all pass.

### T-45.1 — Soundness, honest provers

1000 honest provers each choose `d < τ`, generate a Bulletproofs range proof. **Every verifier accepts.** Verification time p95 ≤ 5 ms on an Apple M-series Mac.

### T-45.2 — Soundness, cheating provers

1000 cheating provers each attempt to commit a value `≥ τ` and produce a passing proof. **Zero successes** within a 1-hour wall-clock budget per prover (each prover gets ≤ 3.6 s of compute). This is the empirical floor; the cryptographic bound is `≤ 2^{-128}` per Bulletproofs Theorem 4.

### T-45.3 — Zero-knowledge (transcript indistinguishability)

The Bulletproofs black-box simulator (per the paper's §6.2) produces transcripts statistically indistinguishable from real ones. Compute `χ²` of transcript-element distribution on 1000 simulated vs 1000 real proofs; **pass at p > 0.05**.

### T-45.4 — Binding to chain head

Generate a valid proof against chain head `H_1`. Replace `H_1` with `H_2` in the public input. Re-derive Fiat-Shamir challenges. The verifier MUST reject with `reason = transcript_mismatch`. The proof bytes are unchanged; only the public input changed; the challenges differ; the inner-product equations no longer hold.

### T-45.5 — Binding to template

Generate proof bound to `template_commitment_1`. Replace with `template_commitment_2`. The verifier MUST reject. This closes the substitution attack: an attacker who steals a proof generated under template T₁ cannot present it as evidence under template T₂.

### T-45.6 — Binding to threshold

Generate proof for `τ_int = 1000`. Replace with `τ_int = 2000` in the public input. The verifier MUST reject (Fiat-Shamir challenges differ).

### T-45.7 — Cross-implementation parity

When the Rust port lands at Everest 43: Python and Rust verifiers accept/reject identically on the full 1000-vector conformance set. Proofs generated by the Python prover cross-verify with the Rust verifier and vice versa. Byte-identical proof output is **not required** (Bulletproofs is randomized; each prover draws fresh blinding randomness), but the verifier's accept/reject decision must be byte-deterministic.

### T-45.8 — Performance budget

- Median prover wall-clock ≤ 50 ms on Apple M-series.
- Verifier ≤ 5 ms on Apple M-series.
- Browser WASM verifier (Everest 83) ≤ 50 ms.
- Proof size ≤ 750 bytes for 32-bit range.

If any of these regress in subsequent versions, the gate fails and the regression must be intentional + documented before the gate is updated.

### T-45.9 — Aggregation correctness

Generate an aggregated `(d_hw, d_vt)` proof per §B.3. The verifier accepts. The aggregated proof:

- Verifies in ≤ 8 ms (the aggregation gain over 2 × independent proofs, which would take ~10 ms each).
- Size ≤ 850 bytes (vs ~1.3 KB independent).
- Rejects under any of the substitution attacks in T-45.4 / T-45.5 / T-45.6, applied to either component.

---

## §D. What this addendum does NOT add

These remain TBD or out of scope for v0 / v0.1:

- **Real-data FAR/FRR.** Empirical false-accept / false-reject curves require Everest 40 (XL effort, external study partner). The cryptographic proof says "d < τ"; the *meaning* of "d < τ" — how it tracks identity-versus-state — is Everest 40's territory.
- **Adversarial-mimicry stress test.** Everest 38 (Mimicry Hardening) characterizes the d-distribution under skilled forgers; v0 commits only to characterizing the attack surface, not closing it.
- **Liveness binding.** Per-session challenge text (Everest 49) ensures samples are fresh; the range proof does not itself attest to liveness. The chain-head binding closes the replay window, but a colluding capture device + replay attacker is closed by Everest 49, not by this summit.
- **τ-privacy.** v0 keeps τ public (it's in the predicate ID per the predicate registry, Everest 53). v1 may commit τ as well; defer.

---

## §E. Why the binding details matter

The Bulletproofs construction proves "the committed value is in a range." Without the Fiat-Shamir transcript binding, that proof is **portable**: an attacker who obtains a valid proof can replay it in any context the verifier doesn't bind.

The transcript binding turns the proof from portable to **contextual**. It becomes a proof of "*in the context of this chain head, this template, this threshold, these generators,* the committed value is in a range." That contextual binding is what makes the disclosure proof safe to ship over the wire to untrusted counterparties.

This addendum exists because the binding semantics are subtle, easy to get wrong, and load-bearing for the protocol's safety. Specifying them precisely is the difference between a range proof and a Calm Witness proof.

— Calm, 2026-05-20
