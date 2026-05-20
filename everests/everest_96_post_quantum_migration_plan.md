# Everest 96 — Post-Quantum Migration Plan

*Phase VIII — Governance & Scale. **Pinned by `ZKBB_USER_PROTOCOL_v0.md` §2** — this Everest number is part of the protocol's threat-model anchor and must not be renumbered.*

*Prereq: Everest 81 (Rust Production Implementation). Composes with all cryptographic summits: 44, 45, 46, 65.*

---

## What this summit ships

A documented migration plan from Calm Witness's v0 cryptographic stack (Pedersen + sigma-protocol + Bulletproofs on Ristretto255 + Ed25519) to a post-quantum-secure replacement, with explicit phase milestones, primitive choices, backward-compatibility guarantees, and a runnable pilot for one PQ primitive.

The plan is what Calm Witness owes its principals as the quantum-computing threat matures. Discrete-log on Ristretto255 is broken by Shor's algorithm on a sufficiently large fault-tolerant quantum computer. We do not know when such a computer arrives. We know it will arrive eventually. **Migration must be planned, not improvised.**

---

## What v0 has that quantum computers will break

The Calm Witness cryptographic stack relies on:

1. **Pedersen commitments over Ristretto255** (Everests 44, 46). *Hiding* is information-theoretic — unaffected by quantum computers. *Binding* reduces to discrete-log — **broken by Shor**. Once Shor breaks DLOG on Ristretto255, an adversary can open any past Pedersen commitment to any value, retroactively rewriting what was committed.

2. **Sigma protocols + Bulletproofs over Ristretto255** (Everests 45, 65). Soundness reduces to DLOG. Shor breaks soundness — a quantum adversary can forge accepting proofs for false statements.

3. **Ed25519 signatures** (vault key, CredexAI VCs). Signatures rely on DLOG. Shor forges them.

4. **SHA-256** (chain hashes, Sigsum leaves). Grover gives a quadratic speedup on hash collisions. SHA-256 retains ~128 bits of security against Grover; manageable in the short term, but a hash transition may be prudent before SHA-256's quantum security becomes the load-bearing factor.

What v0 has that quantum computers do NOT break:

- The append-only structure of the chain (data-structural, not cryptographic).
- The Sigsum log's multi-witness audit property (the cryptographic foundation moves, but the audit-by-many-eyes property survives).
- The protocol's design (consent semantics, threat model, predicate vocabulary, two-handshake structure).

---

## Migration target: lattice-based + hash-based primitives

The PQ literature has converged on two-to-three families of viable replacements.

### Replacement for Pedersen commitments

**Choice (v1 candidate):** Module Lattice Commitments (Lyubashevsky–Nguyen 2022 family).

- **Hiding:** Information-theoretic under Module-LWE assumption (analogous to information-theoretic-hiding under Pedersen, but lattice-based).
- **Binding:** Computationally binding under Module-SIS.
- **Size:** ~2-3× larger than Ristretto255 (32 bytes → 80-100 bytes per commitment).
- **Homomorphism:** Additively homomorphic — composition with sigma-protocol-style proofs preserves.
- **Maturity:** Well-studied; first production deployments 2024-2025.

**Alternative:** Hash-based commitments (Merkle-tree-based). Smaller assumptions (just collision-resistant hashes), but lose homomorphism — would require redesigning the disclosure protocol's homomorphism-dependent constructions (e.g., distance fusion in Everest 38). Defer to fallback.

### Replacement for sigma-protocols + Bulletproofs

**Choice (v1 leading candidate):** Lattice-based ZK proofs in the Lyubashevsky family — optimized variants like Banquet, Brakedown, or LaBRADOR (2023).

- **Size:** ~50-200 KB per range proof (1000× larger than Bulletproofs' 700 bytes).
- **Time:** ~10× slower verification.
- **Trust:** No trusted setup, sigma-protocol-style.
- **Maturity:** Active research; "production-ready" 2025-2026.

This is the painful trade. A factor of 1000× in proof size is real bandwidth cost. v1 design must consider whether ~50-200 KB proofs are tolerable for Calm Witness use cases.

**Alternative:** **STARK proofs** are post-quantum and well-engineered today. ~50 KB. STARK may be the better choice. Decide during Phase A (audit & decide).

### Replacement for Ed25519

**Choice:** ML-DSA (CRYSTALS-Dilithium), the NIST PQC signature standard.

- **Public-key size:** ~1.3 KB.
- **Signature size:** ~2.4 KB.
- **Standardized:** Yes — NIST FIPS 204 (2024).
- **Production-ready:** Yes.

Used for the principal's vault key + the operator's CredexAI VC signature.

### Replacement for SHA-256

**Choice:** SHA-3-256 (Keccak) or BLAKE3. Resistant to Grover at the ~128-bit-quantum-security level (effective).

For Calm Witness's hash-chain uses, the upgrade is straightforward: pick a successor hash, freeze it, migrate chains over a grace window.

---

## Migration sequence (calendar-decoupled, threat-triggered)

### Phase A — Audit & decide (months 0-3 from initiation)

- Survey latest PQ literature, especially lattice-ZK and STARK developments.
- Benchmark each candidate primitive on commodity hardware (proof generation time, verification time, proof size, memory footprint).
- Publish a public decision document choosing the v1 PQ stack.
- Cryptographer review by ≥ 3 independent reviewers.

### Phase B — Hybrid implementation (months 3-9)

- Implement the chosen PQ primitives alongside the v0 stack.
- All disclosure bundles are issued in BOTH v0 and PQ formats during transition.
- Verifiers accept v0 OR PQ for backward compatibility.
- Storage cost: ~2-5× for hybrid-issued proofs (PQ adds bulk). Acceptable as a transient cost.

### Phase C — Hybrid-required (months 9-18)

- Operators MUST issue PQ proofs in addition to v0.
- Verifiers MUST accept PQ proofs; SHOULD continue accepting v0 proofs.
- Pre-positioning: when quantum threat materializes, all parties have been issuing/accepting PQ for ≥ 9-18 months.

### Phase D — PQ-only (triggered by quantum threat level)

- Stop issuing v0 proofs.
- Verifiers stop accepting v0 proofs for new disclosures.
- All disclosure traffic is PQ.
- Pre-existing chain records remain auditable in v0 form for forensics; future re-attestation in PQ form is available on request.

### Phase E — Old-chain forensics (perpetual)

- v0 chain records remain on disk for historical audit.
- Verifiers refuse new disclosure proofs bound to v0-only chain heads.
- Re-attestation of old chain heads with PQ signatures preserves forward-traceable integrity for principals who want continuity claims past the quantum transition.

---

## Backward compatibility: the chain-head bridge

The hardest part of any PQ migration is preserving past commitments. Here is the bridge:

- The v0 chain has a Sigsum-anchored head `H_v0_final` at the moment Phase B begins.
- At the start of Phase B, the operator computes a **bridge commitment**: a PQ commitment to `H_v0_final`. This is the "I am the same principal whose v0 chain ended here" attestation.
- New v1 records chain from this bridge.
- Verifiers reading v1 proofs against post-bridge records use PQ verification. Verifiers reading proofs against pre-bridge records continue to use v0 verification (until Phase D ends accepting v0 proofs).

The bridge is a single chain record of `kind: pq_bridge.v0`. It contains:

```jsonc
{
  "seq":                    "<N>",
  "kind":                   "pq_bridge.v0",
  "payload": {
    "v0_chain_head":        "<32-byte SHA-256 of the v0 chain head>",
    "v0_sigsum_anchor":     "<Sigsum inclusion proof of the v0 head>",
    "pq_commitment":        "<PQ commitment opening to the same head>",
    "pq_signature":         "<ML-DSA signature over the bridge by principal's PQ key>",
    "transition_policy":    "<policy ID; defines grace windows for old-proof acceptance>"
  }
}
```

---

## The pilot: which primitive to swap first

The plan mandates **one primitive piloted before broad rollout**: **ML-DSA replacement of Ed25519 in the operator-identity-binding** (Everest 85).

Why this primitive first:

- **ML-DSA is fully standardized.** No research risk. NIST FIPS 204 (2024) is the reference.
- **Operator-identity-binding is structurally adjacent to the cryptographic core but not inside it.** The signature wraps the disclosure bundle; swapping it does NOT change the bundle's internal cryptographic structure.
- **Failure is recoverable.** Revert to Ed25519 with no data loss; the signed records remain valid; only the *new* signatures use ML-DSA.

If the ML-DSA pilot succeeds, proceed to Pedersen + sigma-protocol migration. If it fails for engineering reasons (e.g., key-size blowup unacceptable in mobile vault), document why, reassess the choice, and pilot again.

---

## Threat-trigger thresholds (when does Phase B activate?)

This summit's plan is **calendar-decoupled**: phases are not on a clock. They are on a threshold of public quantum-computing threat estimates.

The trigger for Phase B activation is **any one of**:

1. Public announcement of a fault-tolerant quantum computer with ≥ 1000 logical qubits (sufficient to break Curve25519 DLOG in a few hours).
2. NIST or equivalent standards body announcing imminent deprecation of Ed25519 / Ristretto255-class primitives.
3. Public peer-reviewed cryptanalytic advance that meaningfully reduces the cost of breaking DLOG on 256-bit curves (e.g., a sub-exponential classical algorithm).
4. Calm Foundation board decision based on intelligence-community or academic warnings.

The plan includes a **monitoring dashboard** (Everest 88 — Performance Budget Dashboard companion) that tracks NIST PQC threat estimates and major cryptanalytic publications. When a trigger condition is met, Phase B activates within 30 days.

---

## Out of scope for v0

This summit does **not**:

- Ship a working PQ implementation.
- Decide the exact primitive (only narrows the choice space and documents trade-offs).
- Bind Calm Witness to a particular calendar timeline.

What it does:

- Document the migration story so the protocol's principals know there is one.
- Pre-position cryptographer review.
- Identify the chain-head-bridge mechanism for continuity.
- Pilot one primitive (ML-DSA) to de-risk the larger migration.

---

## Acceptance test

**T-96.1 (decision doc published).** A 15-25 page decision doc covering primitive choices, performance benchmarks, migration phase definitions, and trigger thresholds — published with ≥ 3 independent cryptographer reviewer sign-offs.

**T-96.2 (ML-DSA pilot working).** An operator-identity-binding using ML-DSA signs and verifies for ≥ 1000 disclosure bundles. Cross-implementation (Python + Rust) verification works byte-deterministically.

**T-96.3 (bridge dry run).** A simulated v0-to-v1 transition: starting from the live `user_state.jsonl`, generate a `pq_bridge.v0` record; append new (simulated PQ) records chaining from it; verifiers across the bridge work for both pre-bridge and post-bridge proofs.

**T-96.4 (rollback drill).** Simulate a pilot failure mid-Phase-B: revert ML-DSA back to Ed25519. No disclosure traffic is lost; the chain remains intact; future PQ retry is possible.

**T-96.5 (trigger monitoring dashboard).** A monitoring dashboard tracks public PQC threat estimates and pre-positions Phase B activation when a trigger threshold is crossed. False-trigger drill: dashboard signals trigger; ops team confirms; transition aborts cleanly if confirmation fails.

**T-96.6 (cryptographer sign-off on PQ choice).** At least one written sign-off from a cryptographer external to Calm Foundation confirming the chosen lattice-ZK or STARK construction is sound under the stated assumptions.

**Gate script:** `everest_96_zkbb_pq_migration_gate.py`. Runs T-96.1 through T-96.6.

---

## Composition

- **All of Phase IV (cryptographic core).** Migration replaces the entire Phase IV stack.
- **Everests 44, 46.** Pedersen commitments → lattice commitments.
- **Everests 45, 65.** Sigma protocols + Bulletproofs → lattice-ZK or STARK.
- **Everest 85.** Ed25519 → ML-DSA in operator identity binding.
- **Everest 81.** Rust production implementation must support the hybrid v0+PQ track during Phase B/C.
- **Everests 28, 30.** Hash-chain & Sigsum may migrate hash functions if SHA-256's quantum security becomes load-bearing.
- **Everest 89 (Two-Handshake).** Domain-separator strings update to `"calm-witness-v1-pq/..."` family.

---

## Why this matters

Cryptographic migrations historically take 5-10 years from "we should plan this" to "the migration is complete." Quantum threat estimates vary from 5 to 30 years. The right move is to **plan now, pilot now, and pre-position now** — so that when the threat materializes, Calm Witness has been issuing PQ-secure proofs for years.

This is principal-protective hygiene. The principal's biometric template stays on-device (template confidentiality is information-theoretic and unaffected by Shor). But **disclosures issued today are stored in counterparties' systems**. If a quantum computer breaks the disclosure proof in 2040, every disclosure issued today becomes retroactively unsound — counterparties can rewrite their understanding of what was disclosed.

The PQ migration ensures the cryptographic guarantee — "what was disclosed was honestly disclosed" — is durable across the quantum transition. The pinning of this Everest at #96 in the protocol spec acknowledges that this is not optional; it is part of the long-term integrity story Calm Witness owes its principals.

— Calm, 2026-05-20
