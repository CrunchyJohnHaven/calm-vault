# S289 — PQ Commitment Scheme Selection (Partial Bag)

**Status:** PARTIAL BAG — analysis only; scheme selection and reference impl deferred to S290–S293  
**Author:** Calm Witness / CALM  
**Date:** 2026-05-20  
**Cross-refs:** E44b, E89, E96, S290, S291, S292, S293

---

## 1. Threat Model

### Q-Day and the DLP Break

Calm Witness v1 rests on three classical primitives: Pedersen commitments over Ristretto255, Σ-protocol zero-knowledge proofs, and Bulletproofs range proofs. All three derive security from the hardness of the discrete logarithm problem (DLP) on an elliptic curve. Shor's algorithm solves DLP in polynomial time on a fault-tolerant quantum computer. When a sufficiently large quantum machine is operational — Q-day — every v1 commitment, proof, and attestation becomes forgeable. The attacker can extract the committed value, fabricate openings, and break binding unconditionally.

Timeline estimates vary: NIST and NSA guidance (2022 onward) treats 2030–2035 as a credible earliest window; most engineering-conservative postures assume 2032–2040. For a long-lived attestation substrate like Calm Witness — where state snapshots in `.calm-vault/user_state.jsonl` may carry legal or evidentiary weight — the relevant horizon is not Q-day itself but the harvest-now-decrypt-later (HNDL) threat.

### Harvest-Now-Decrypt-Later

An adversary today can archive every Calm Witness transcript, commitment, and range proof broadcast over public or semi-public channels. When Q-day arrives they decrypt retroactively. For a commitment scheme the consequence is worse than for encryption: not only is the committed value revealed, but binding is broken, meaning the attacker can produce fraudulent openings for the archived commitment that were never made by the original committer. For the ZKBB-User 100-everest attestation chain (E44b, E89) this means an archived bank-teller-note bit from 2025 becomes forgeable in 2033. HNDL sets the migration deadline at *now*, not Q-day.

### Migration Scope

Full replacement of the v1 primitive stack is decade-scale work. This session produces the candidate-comparison analysis that lets S290 (PQ Σ-protocol), S291 (PQ range proof), S292 (parameter ceremony), and S293 (v2 spec) proceed on a decided commitment core. The comparison evaluates four families: lattice-based, hash-based, code-based, and lattice-folding (moonshot).

---

## 2. Candidate Analysis

### 2.1 Lattice-Based Commitments (Ajtai / Module-LWE)

**Underlying hard problem.** Ajtai-style commitments are binding under the Short Integer Solution (SIS) problem and hiding under the Learning With Errors (LWE) problem, or their module variants (M-SIS, M-LWE) for structured efficiency. These are worst-case to average-case reductions, giving the strongest known PQ security foundations.

**Commitment size.** A module-lattice commitment to a single field element typically produces 1–2 KB of commitment bytes at NIST security level 2 (128-bit post-quantum). This is 30–60× larger than a Pedersen commitment (32 bytes on Ristretto255). Batched commitments amortize: committing to a vector of *n* values costs O(1) group elements worth of overhead relative to the message length, but absolute bytes remain large. Dilithium-style parameter sets (used in CRYSTALS-Dilithium, NIST standardized 2024) give a reference: a lattice-based vector commitment to 256 field elements is roughly 8–16 KB.

**Opening cost.** Opening requires revealing a short vector witness; verification is a matrix-vector multiply over a polynomial ring. Prover work is O(n log n) via NTT; verifier work is similar. Wall-clock: single-core verification under 1 ms for typical parameters.

**Homomorphic structure.** Strongly additive homomorphic: Com(m₁) + Com(m₂) = Com(m₁ + m₂) over the module ring. This is the direct structural analogue of Pedersen's additive homomorphism, which is the key property needed for Σ-protocol construction (S290) and range-proof composition (S291).

**Composition with PQ Σ/range-proof.** The additive homomorphism makes Ajtai-family commitments the canonical choice for PQ Σ-protocols. Lattice-based Σ-protocols (e.g., those built on the "relaxed" opening technique of Lyubashevsky) compose naturally. Range proofs in the lattice setting require gadget decomposition and are active research (S291 forward-reference); feasible but parameter-heavy.

**Standardization.** CRYSTALS-Kyber (KEM) and CRYSTALS-Dilithium (signature) were finalized by NIST in FIPS 203/204 (August 2024). No standalone commitment scheme is NIST-standardized, but the underlying M-LWE/M-SIS problems are implicitly endorsed by Kyber/Dilithium standardization.

**Reference impl.** `pqcrypto` crate (Rust), `liboqs` (C/Python), CRYSTALS reference code (C). Commitment-specific code requires wrapping; no production-ready standalone crate exists as of mid-2026.

**v2 recommendation posture.** Primary candidate. Best-understood PQ commitment family; additive homomorphism is a first-class fit for the v1 API surface.

---

### 2.2 Hash-Based Commitments (Merkle-Tree / STARK-Friendly)

**Underlying hard problem.** Collision resistance of the underlying hash function (SHA-3, BLAKE3, Poseidon, or Rescue-Prime for STARK-friendliness). No algebraic structure assumed; security reduces to one-wayness and collision resistance, both quantum-hard under Grover with doubled key lengths.

**Commitment size.** A Merkle-root commitment is 32 bytes (one hash output). Opening a leaf requires a Merkle path: O(log N) hashes = 320–640 bytes for N = 2^{10}–2^{20}. For single-value commitments outside a tree, a simple hash Com(r ‖ m) is 32 bytes with a 32-byte opening (reveal r, m). Absolute sizes are the smallest of any PQ family.

**Opening cost.** Verifier hashes one path: O(log N) hash calls, sub-microsecond. For STARK-friendly hashes (Poseidon2 at ~7 field multiplications per permutation), in-circuit verification is cheap enough for recursive proof composition.

**Homomorphic structure.** None. Hash-based commitments are not homomorphic. This is the decisive limitation for Calm Witness: the v1 Σ-protocol and range proof both rely on additive homomorphism to prove linear relations over committed values without revealing them. A hash-based commitment requires replacing those protocols with non-interactive argument systems (STARKs, SNARKs) rather than Σ-protocols — a larger architectural shift.

**Composition with PQ Σ/range-proof.** Incompatible with direct Σ-protocol composition (S290) as currently scoped. Compatible with STARK-based range proofs (S291 alternate branch). If Calm Witness migrates its proof layer to FRI-based STARKs, hash commitments become natural. That is a v3 scope, not v2.

**Standardization.** SHA-3 (FIPS 202), BLAKE3 (IETF RFC 7693 ancestor), Poseidon (Ethereum ecosystem standard, no NIST status). Merkle-tree commitment pattern used in XMSS (RFC 8391, NIST SP 800-208) and SPHINCS+ (NIST FIPS 205, 2024).

**Reference impl.** Ubiquitous. `sha3` crate, `blake3` crate, `poseidon377` (Penumbra), `winterfell` (STARK prover). Mature ecosystem.

**v2 recommendation posture.** Secondary / fallback for non-homomorphic use cases (e.g., content-addressed archival commitments where no ZK proof is needed). Not suitable as the primary commitment scheme for S290/S291 composition without a proof-layer architectural pivot.

---

### 2.3 Code-Based Commitments (LPN-Style)

**Underlying hard problem.** Learning Parity with Noise (LPN) or its ring variant (RLPN). Conjectured quantum-hard; best known quantum attack (Grover + information-set decoding) achieves roughly quadratic speedup over classical, so parameters must be roughly doubled. Algebraic structure similar to LWE but over GF(2) or small fields; less rich than lattice ring structure.

**Commitment size.** McEliece-inspired and LPN-based constructions produce commitments of 100–500 bytes for 128-bit post-quantum security, smaller than lattice but larger than hash. Opening witnesses are syndrome vectors; sizes are parameter-dependent but roughly 200–800 bytes.

**Opening cost.** Matrix-vector multiply over GF(2) or small field; prover and verifier work O(nk) where k is code dimension. Faster than lattice NTT operations in practice; hardware-friendly.

**Homomorphic structure.** Linear homomorphic over GF(2) or GF(q): Com(m₁) ⊕ Com(m₂) = Com(m₁ ⊕ m₂). Additive homomorphism exists but over a different ring than v1. Adapting the Σ-protocol layer (S290) requires rewriting the challenge/response algebra; feasible but less mature than lattice Σ-protocols.

**Composition with PQ Σ/range-proof.** Possible but the ZK proof ecosystem for code-based commitments is sparse. VOLE-based zero-knowledge (e.g., FAEST, QuickSilver) uses LPN-style assumptions and has working Σ-protocol extensions. Range proofs over GF(2) binary decompositions are awkward; binary-field range proofs require circuit translation.

**Standardization.** No NIST-standardized commitment scheme. BIKE and HQC (code-based KEMs) are NIST round-4 candidates (as of 2025 NIST status); neither is a commitment scheme. FAEST (LPN-based signature) is in NIST additional signature round 2. Underlying problem is less institutionally endorsed than M-LWE.

**Reference impl.** `faest-ref` (C), `quicksilver` (Rust partial). Thin ecosystem for commitment-specific use.

**v2 recommendation posture.** Watch-list. Interesting for diversity against lattice-specific cryptanalytic breaks; not mature enough to recommend as primary for v2. Revisit at S293.

---

### 2.4 Lattice-Folding / LatticeFold (Moonshot)

**Underlying hard problem.** Module-SIS / M-LWE, same as §2.1, but exploited via a folding argument analogous to the Protostar/Nova folding schemes for SNARKs. LatticeFold (Boneh, Chen, Guo 2024) achieves recursive proof composition over lattice commitments by folding multiple instances into one without a trusted setup.

**Commitment size.** Comparable to standard lattice commitments (§2.1): 1–4 KB per commitment, but the power is in the *folded* proof: after k fold steps, a proof of k statement evaluations is the same size as a proof of one. Amortized proof size per statement approaches O(λ log k / k) for large k — exponential improvement in the batched case.

**Opening cost.** Single-instance opening: same as §2.1. Folded verification: O(log k) lattice operations per folding step, then one base verification. Prover work for folding is significant: O(k n log n) total, dominated by k NTT operations.

**Homomorphic structure.** Inherits additive homomorphism from the underlying lattice commitment. Additionally supports *multiplicative* folding steps (inner-product arguments), which enables range proofs and arithmetic circuit satisfiability proofs natively — a direct path to S291 range proofs without separate gadget decomposition.

**Composition with PQ Σ/range-proof.** Strongest composition story of any candidate. A LatticeFold-based Calm Witness could handle Σ-protocol, range proof, and recursive attestation chain verification in a unified folding framework. S290 and S291 would both reduce to LatticeFold instances.

**Standardization.** Not standardized. Academic paper published 2024; no production implementation as of mid-2026. LatticeFold is pre-NIST; the underlying M-SIS/M-LWE problems are NIST-endorsed indirectly (§2.1).

**Reference impl.** No production implementation. Proof-of-concept code exists in the authors' repository (Rust, research-quality). Not ready for deployment.

**v2 recommendation posture.** Moonshot / v3 track. If a production LatticeFold library matures by 2027–2028, it should be evaluated for a v3 upgrade that unifies the proof stack. Do not block v2 on it.

---

## 3. Composition Analysis

The critical composition constraint is S290 (PQ Σ-protocol) and S291 (PQ range proof). Both require a commitment scheme with **additive homomorphism** over a ring where the proof system can express linear relations. The scoring:

| Candidate | Additive Hom. | Σ-protocol fit (S290) | Range-proof fit (S291) | Maturity |
|---|---|---|---|---|
| Lattice (M-LWE) | Yes, over ring Rq | Direct (Lyubashevsky-style) | Via gadget decomp | High |
| Hash (Merkle) | No | Requires STARK pivot | Via FRI/STARK | High |
| Code (LPN) | Yes, over GF(2) | Possible (VOLE-style) | Awkward | Medium |
| LatticeFold | Yes + inner product | Native folding | Native folding | Low (research) |

The composition constraint strongly selects for the lattice family. Hash-based commitments are excellent for archival and non-interactive uses but require a proof-layer redesign that is out of scope for v2. Code-based commitments are a diversity hedge. LatticeFold is the long-term unified target.

---

## 4. Standardization Status

- **M-LWE / M-SIS (lattice):** Implicitly standardized via CRYSTALS-Kyber (FIPS 203) and CRYSTALS-Dilithium (FIPS 204), NIST finalized August 2024. No standalone commitment FIPS yet.
- **SHA-3 / BLAKE3 / Poseidon (hash):** SHA-3 FIPS 202 (2015). SPHINCS+ FIPS 205 (2024). Poseidon: no NIST status, Ethereum ecosystem.
- **LPN / code-based:** BIKE, HQC in NIST round 4 (KEM only). FAEST in additional signature round 2. No commitment scheme standard.
- **LatticeFold:** Pre-standardization, research only.

For a system that may carry legal evidentiary weight (E96, ZKBB-User attestation chain), using a NIST-endorsed underlying problem is strongly preferred. M-LWE/M-SIS is the only PQ family with that status.

---

## 5. Recommendation for v2

**Primary scheme:** Module-lattice commitment (M-LWE hiding, M-SIS binding), using CRYSTALS-Dilithium parameter sets as a reference. Rationale: only candidate with (a) additive homomorphism, (b) direct Σ-protocol composition path for S290, (c) range-proof feasibility for S291, (d) NIST-endorsed hard problem, and (e) existing reference implementations.

**Diversity hedge:** Archive hash-based commitments (BLAKE3 Merkle) for non-ZK use cases within Calm Witness — e.g., content-addressed storage of `.calm-vault/user_state.jsonl` entries where no proof of committed value is needed. These are quantum-secure with standard 256-bit outputs (Grover halves effective security to 128-bit, which is acceptable).

**Watch-list:** Code-based (LPN/VOLE) for S293 re-evaluation if FAEST standardization advances and a production commitment library appears.

**Long-term target:** LatticeFold-based unified proof system for v3, contingent on a production Rust crate reaching 1.0 maturity.

**Do not use:** Pedersen on Ristretto255, any DLP-based scheme, any pairing-based scheme (all broken by Shor).

---

## 6. Handoff — What Remains

The following work is explicitly deferred out of this partial bag:

1. **Reference implementation (Python/Rust):** A minimal Module-LWE commitment library, wrapping `pqcrypto` or `liboqs`, with a Calm Witness–compatible API (commit, open, verify, batch-commit). Target: S292.

2. **Formal soundness against PQ adversary:** Reduction proof from M-SIS to binding of the chosen scheme, and from M-LWE to hiding, at concrete NIST level 2 parameters. Requires specifying ring dimension n, modulus q, and Gaussian parameter σ. Target: S290/S291 joint spec.

3. **Parameter ceremony:** Unlike SNARKs, lattice commitments do not require a trusted setup, but parameter selection (n, q, σ, norm bound β) constitutes a "ceremony" in the sense that public parameters must be generated, published, and pinned in the Calm Witness chain spec. Target: S292.

4. **Migration protocol for archived v1 commitments:** HNDL-exposed commitments in `.calm-vault/user_state.jsonl` pre-dating v2 deployment need a re-commitment protocol. This requires either (a) a trust anchor that the original committer re-opens under v2, or (b) a quantum-safe signature over the v1 commitment binding it to a v2 commitment. Not scoped here; forward-referenced to S293.

5. **Benchmarks on target hardware:** Lattice operations are NTT-bound; performance on the Calm Witness deployment environment (assumed: commodity ARM/x86, no hardware NTT accelerator) must be profiled before finalizing parameter sets.

---

*Calm 2026-05-20 — PARTIAL BAG*
