# Everest 96 — Post-Quantum Migration Plan

*Phase VIII — Governance & Scale. Prereq: Everest 81.*

---

## 1. Introduction: The PQ Challenge

Calm Witness v0 is built on classical elliptic-curve cryptography: Pedersen commitments over Ristretto255, Ed25519 Schnorr signatures, and Bulletproof range proofs. All three primitives are vulnerable to Shor's algorithm. When quantum computers with sufficient qubit counts arrive—a timeline estimated at 10–20 years, though uncertainty is high—these proofs become forgeable and commitments become reversible.

This document specifies a **post-quantum migration path** that does not ship PQ primitives in v0 but instead establishes a forward-compatible governance story for transitioning to NIST-standardized post-quantum cryptography (PQC) in v1 and beyond. The goal is to protect new disclosures immediately upon v1 rollout while maintaining verifiability of legacy v0 proofs indefinitely.

---

## 2. V0 Status: Pre-Quantum Baseline

Calm Witness v0 employs the following cryptographic components:

**Commitment scheme:**
- Pedersen commitments over Ristretto255 (Edwards curve, prime-order subgroup).
- Commitment C = g^d × h^r hiding distance d under the discrete-logarithm assumption.
- No post-quantum analogue with equivalent performance is standardized.

**Signatures:**
- Ed25519 (Edwards curve) for operator identity credentials and Calm Witness proof signatures.
- Broken by Shor's algorithm: given Ed25519 public key pk, a quantum attacker computes the discrete log to forge signatures.

**Range proofs:**
- Bulletproofs (Bünz et al., 2018) for proving 0 ≤ d < τ without revealing d.
- Security relies on discrete-log hardness and group operations.
- Bulletproof size (approximately 700 bytes for 32-bit range) depends on DL security; post-quantum replacements are substantially larger.

**Hash functions:**
- SHA-256 for Fiat-Shamir challenges and transcript hashing.
- Post-quantum resilience: Grover's algorithm reduces 256-bit security to 128-bit effective strength.
- Acceptable for v0+; no upgrade required for hashing.

**Quantum-vulnerable surfaces:**
1. Pedersen commitments: discrete log → Shor breaks it.
2. Ed25519 signatures: discrete log → Shor breaks it.
3. Bulletproofs: group operations → Shor breaks it (structural, not just DL).
4. Scalar field arithmetic: all rely on discrete log.

---

## 3. Threat Model: Harvest Now, Decrypt Later

A **harvest-now-decrypt-later (HNDL) attack** assumes an adversary with current network access (can eavesdrop and intercept messages) and future quantum capability (can break discrete-log assumptions).

**Attack timeline:**
- **2026 (now):** Adversary stores all intercepted v0 Calm Witness proofs, commitments, and signatures.
- **2040–2046:** Quantum computers scale to sufficient qubit counts.
- **2046+:** Attacker decrypts stored material retroactively.

**Impact on Calm Witness:**
- Pedersen commitments C = g^d × h^r can be inverted: adversary recovers d (the biometric distance).
- Ed25519 signatures can be forged: adversary can impersonate operators or principals.
- Bulletproof range proofs collapse: adversary learns whether d < τ and can construct false proofs.

**Specific risk to principals:**
- Disclosed distance d reveals how closely the principal's biometric sample matched the enrolled template.
- If d ≈ 0, the sample was a strong match (likely the principal themselves).
- If d ≈ 1, the sample was a weak match (possible impostorship or biometric drift).
- Retroactive disclosure of a principal's biometric state at a specific time.

**Mitigation strategy:**
- v1+ hybrid proofs (classical + PQ signatures) ensure that by the time quantum computers arrive, old v0 commitments are already superseded.
- Principals who disclosed in 2026–2032 (v0 era) accepted a known risk window; v1 commitments created after migration are quantum-safe.
- Cross-references (Everest 44, Everest 45, Everest 46, Everest 81) ensure v1 proofs can identify and supersede v0 commitments systematically.

---

## 4. NIST Post-Quantum Cryptography Standards (2026 Landscape)

NIST finalized PQC standardization in August 2024, with early 2026 implementations widely available. Key standards relevant to Calm Witness:

**Signatures (FIPS 204–206):**
- **ML-DSA (Dilithium, FIPS 204):** Lattice-based (MLWE). Signature size ~2.5 KB (vs. Ed25519's 64 bytes). Fast verification (~10 ms). Mature Rust implementation in `liboqs` and `oqs-rs`.
- **Falcon (FIPS 205):** Lattice-based (NTRU). Signature size ~660 bytes (smaller than Dilithium). Slower verification (~100 ms). Cryptanalytic pressure: several attacks in academic literature (all well below the security parameter). Conservative choice: prefer ML-DSA.
- **SLH-DSA (SPHINCS+, FIPS 206):** Hash-based. Signature size ~17 KB. Extremely slow (~100+ ms signing). Stateless. Use case: long-term reference signatures only (not for frequent disclosure proofs).

**Key Encapsulation Mechanisms (FIPS 203):**
- **ML-KEM (Kyber, FIPS 203):** Lattice-based (MLWE). Ciphertext ~1 KB, shared secret ~32 bytes. Used for symmetric-key establishment, not directly for commitments.

**Commitments:**
- **No NIST standardization yet (as of 2026).** Lattice-based Pedersen analogues exist in research (e.g., RLWE-based, Ring-SIS), but production implementations are limited.
- Candidates: Ring-LWE over polynomial rings, lattice-based vector commitments (e.g., from the Aurora ZK proof system).
- **Implication:** v1 commitments will likely use a non-standard but auditable lattice-based scheme. Everest 96 defers detailed specification to v1 working groups.

**Range proofs:**
- **No standardized production replacement (as of 2026).**
- Research-stage: lattice-based range proofs (e.g., LaBRADOR, Lattice-Based Range proof Amortized Decentralized Operations).
- Conservative path: v1 uses hybrid proofs (Bulletproof + lattice-based alternative in parallel) until a single lattice-based scheme matures.

---

## 5. Migration Path: Five Steps

### Step 1: V0 (2026–2027) — Pre-Quantum Baseline

**Crypto stack:**
- All primitives are classical (Ristretto255, Ed25519, Bulletproofs, SHA-256).
- Operationally: document the PQ risk explicitly in operator handbooks and consent forms.

**Governance:**
- Principals are informed that v0 proofs are vulnerable to quantum computers.
- Everest 81 (governance framework) establishes a "PQ sunset clause": v0 proofs remain valid forever, but new disclosures after v1 launch MUST use v1 or higher.

**Storage:**
- All v0 proofs include a `version` field (e.g., `"crypto_version": "v0"`).
- The commit hash of the proof (via Everest 19 transparency log) includes version metadata.

### Step 2: V1 (2027–2029) — Hybrid Signatures

**Signature upgrade:**
- Operators sign all new proofs with **both Ed25519 AND ML-DSA** (Dilithium-3 or ML-DSA-87).
- A proof's signature field becomes a pair: `(sig_ed25519, sig_mldsa)`.
- Verifier accepts proof if either signature verifies (quorum = 1-of-2).

**Rationale:**
- Pedersen commitments remain unchanged (no post-quantum replacement yet).
- Bulletproofs remain unchanged (range proofs still rely on DL).
- Signatures are the attack surface for immediate impersonation; hybrid signing stops adversaries from forging operator identity even if Ed25519 breaks.

**Backward compatibility:**
- v0 proofs (signed only with Ed25519) remain verifiable; v1 verifiers skip ML-DSA check for v0 proofs.
- v1 proofs with both signatures are rejected by v0 verifiers (which ignore ML-DSA entirely), but this is intentional: v0 verifiers should not be deployed beyond 2029.

**Proof size overhead:**
- Hybrid signature: Ed25519 (64 bytes) + ML-DSA (approximately 2.5 KB) ≈ 2.6 KB vs. 64 bytes (approximately 40× increase).
- Acceptable for v1; new disclosures are infrequent (per-principal proofs occur once per session).

### Step 3: V1+ (2029–2032) — Hybrid Commitments

**Commitment upgrade:**
- Introduce a lattice-based commitment scheme alongside Pedersen.
- Each distance d is committed twice: C_pedersen = g^d × h^r (classical) and C_lattice = commit_lwe(d, r_lwe) (post-quantum).
- A proof's commitment field becomes a pair: `(com_pedersen, com_lattice)`.
- Verifier checks both; ZK proof can be verified against either commitment (or both for redundancy).

**Rationale:**
- Lattice-based commitments (e.g., Ring-LWE) are believed secure against quantum adversaries (hardness of LWE is not known to be broken by Shor's algorithm).
- Dual commitments provide a transition window: old v0/v1 proofs use only Pedersen (still verifiable), new v1+ proofs are quantum-safe.

**Range proof adjustment:**
- Bulletproofs in v1+ are still computed over Pedersen commitments (DL-based proofs persist).
- A separate, lattice-based range proof is added for C_lattice (specification deferred to v1+ working groups).
- Aggregate proof size: approximately 700 bytes (Bulletproof) + X bytes (lattice-based RP) ≈ 1.5–2 KB per disclosure.

### Step 4: V2 (2032–2035) — Deprecate Classical Primitives

**Signature**:
- Ed25519 signatures are removed entirely.
- Operators sign only with ML-DSA (or a successor PQC signature scheme, if NIST updates standards).

**Commitments & proofs:**
- Pedersen commitments are deprecated from new proofs.
- All new disclosures use C_lattice exclusively.
- Bulletproofs are deprecated; range proofs are lattice-based only.

**Backward compatibility:**
- v0/v1 proofs remain verifiable (v2 verifiers understand legacy formats).
- Operators no longer issue new v0/v1 proofs; v0 software is archived and not deployed.

### Step 5: V2+ (2035+) — PQ-Only Stack

**End-to-end post-quantum:**
- All commitments, signatures, and range proofs are quantum-safe.
- No classical cryptography in the active protocol.
- v0/v1 proofs are archival: verified only when required for historical audit or legal purposes.

---

## 6. Backward Compatibility: Verifying Legacy Proofs in V2

A critical requirement: v0 Calm Witness proofs created in 2026 must remain verifiable in 2035, even after classical cryptography is deprecated.

**Mechanism:**
- The v2 verifier includes legacy cryptographic libraries (Ristretto255, Ed25519, Bulletproofs) as **deprecated but preserved modules**.
- A proof's version tag (e.g., `"crypto_version": "v0"`) directs the verifier to use the appropriate classical libraries.
- The transparency-log anchor (Everest 19) is verified using the original hashing and signature scheme from the era the proof was created.

**Example verification flow (v0 proof, v2 verifier):**
1. Parse proof: extract `crypto_version = "v0"`.
2. Load legacy verifier context: Ristretto255 group, Ed25519 signature verification.
3. Verify Ed25519 signature of the proof against operator identity credential (stored at the time of issuance).
4. Verify transparency-log anchor using Sigsum + Roughtime (both support legacy hash-to-verify).
5. Verify Bulletproof range proof using legacy DLP-based verifier.
6. If all checks pass: proof is valid as of 2026; counterparty has proof that this disclosure occurred.

**Assumption:**
- Quantum computers do not exist in 2026–2034 (reasonable given current timelines).
- If a quantum computer *does* exist in 2027 and an attacker retroactively forges v0 proofs, the forgery is detected only if the attack surface (e.g., operator identity keys) is observed to be compromised. This is a governance problem, not a cryptographic one (Everest 81 handles response protocols).

---

## 7. Implementation: Open Quantum Safe and Library Choices

**ML-DSA (Dilithium) integration:**
- Rust crate: `liboqs-rs` (maintained by Open Quantum Safe) or `oqs-rs` (lighter wrapper).
- Parameters: ML-DSA-87 (approximately 128-bit post-quantum security, analogous to 256-bit classical).
- API: `generate_keypair()` → (pk, sk), `sign(msg, sk)` → sig, `verify(msg, pk, sig)` → bool.
- Performance: ~5–10 ms signing, ~10 ms verification (acceptable for per-session disclosure).

**Lattice-based commitments (v1+ phase):**
- Research libraries: `fhe.rs`, `lattice-algebra` (lattice-based cryptography toolkits).
- Candidates: Ring-LWE commitments (polynomial-ring parameterization) or Pedersen-style lattice commitments.
- Deferred: full specification to v1 working group (2028–2029).

**Lattice-based range proofs (v1+ phase):**
- Research stage; no production-ready crate as of 2026.
- Likely approach: adapt Bulletproof methodology (inner-product argument) to Ring-LWE, or use a different circuit-based approach (e.g., Fiat-Shamir over lattice-based commitments).
- Performance target: proof size ≤ 2 KB (vs. Bulletproof's 700 bytes), verification ≤ 50 ms.
- Deferred: to v1 working group.

**Testing & validation:**
- Implement hybrid signature verification in v1 release candidate (2028).
- Test interoperability: v1 verifier must accept v0 proofs, v0 verifier must reject v1 proofs (intentional).
- Cross-platform determinism (Everest 63): ensure ML-DSA proofs are bit-identical across Linux, macOS, Windows, ARM.

---

## 8. Timeline and Governance

**2026 (v0 launch, now):**
- Deploy Calm Witness v0 with explicit PQ risk statement in operator documentation.
- Begin threat modeling and community review (Everest 81 feedback).

**2027–2028 (v1 development):**
- Integrate ML-DSA via Open Quantum Safe.
- Implement hybrid signature verification.
- Begin lattice-based commitment research; issue RFP for academic partners.

**2028 (v1 beta):**
- Deploy v1 with hybrid signatures (optional ML-DSA signing).
- v0 verifiers coexist; v1 proofs are rejected by v0 but logged.

**2029 (v1 general availability):**
- ML-DSA signing becomes mandatory for all new proofs.
- v0 proofs are marked "sunset" in the protocol; operators discourage new v0 disclosures (retroactively, for principals who created v0 proofs pre-2029, the proofs remain valid).

**2029–2032 (v1+ hybrid commitments):**
- Deploy lattice-based commitment scheme.
- Dual-commit strategy: every distance is committed to Pedersen and Ring-LWE.
- Hybrid range proofs: Bulletproof + lattice-based range proof.

**2032 (v2 launch):**
- Ed25519 signatures removed.
- Pedersen commitments removed from new proofs.
- Bulletproofs deprecated (lattice-based range proofs mandated).

**2035+ (v2+ steady-state):**
- All cryptography is post-quantum.
- Legacy verifiers (v0/v1 libraries) are maintained for archival purposes only.

---

## 9. Risk Assessment & Mitigations

**Residual risk: HNDL attacks on v0 commitments (2026–2034):**
- Principal's biometric distance retroactively leaked in ~2035 if quantum computer arrives early or if academic break is discovered.
- **Mitigation:** principals use Calm Witness v1+ proofs (hybrid/PQ-safe) for any new disclosures after 2029. Old v0 proofs become archival only.
- **Governance:** Everest 81 establishes a "proof refresh" option: principal can request re-disclosure in v1+ format (new proof, new timestamp). This replaces the v0 proof in active use but does not erase history.

**Residual risk: Academic break in lattice-based cryptography:**
- Ring-LWE, Module-LWE, or ML-DSA is shown to be weaker than claimed (e.g., subexponential algorithm discovered).
- **Mitigation:** v2+ migration uses NIST-standardized primitives only; if NIST withdraws ML-DSA, fallback to SLH-DSA (hash-based, slower but provably secure) or wait for NIST's next round.
- **Mitigation:** Dual-commit in v1+ ensures even if one lattice scheme breaks, the dual commitment provides a fallback (classical Pedersen is unaffected by lattice-based breaks).

**Residual risk: Lattice-based library bugs:**
- Incorrect implementation of ML-DSA or Ring-LWE commitments leads to weak keys or forgeable proofs.
- **Mitigation:** Open Quantum Safe libraries are audited by academic teams. Independent audits are commissioned (e.g., by Creativity Machine LLC) for v1 release.
- **Mitigation:** All lattice-based code uses constant-time arithmetic (Rust type system enforces this via `subtle`, `zeroize` crates).

---

## 10. Cross-References and Interdependencies

This plan integrates with the following Everests:

- **Everest 19**: Transparency-log anchoring (Sigsum). v2 verifier must support legacy Sigsum anchors from 2026–2034 for v0 proof verification.
- **Everest 44**: Pedersen commitments. v1+ will add lattice-based sibling; v44 remains valid but becomes classical-only after v2.
- **Everest 45**: Bulletproofs range proofs. v1+ adds lattice-based sibling; v45 remains classical-only after v2.
- **Everest 46**: Template identity commitment. Uses Pedersen; v1+ dual-commit strategy applies here as well.
- **Everest 56**: Biometric match predicate. Consumes proofs from E44/E45; will consume dual-commitment proofs in v1+.
- **Everest 63**: Determinism harness. Must validate that hybrid signature generation (Ed25519 + ML-DSA) is deterministic across platforms.
- **Everest 68**: Operator identity credentials. Ed25519 keys are transitioned to ML-DSA keys in v1; dual-credential strategy (both key types issued) during transition window (2027–2032).
- **Everest 81**: Governance framework. Establishes policy for sunset clauses, proof refresh, and emergency cryptographic breaks.
- **Everest 91**: Deployment and operations. Specifies upgrade path from v0 to v1 to v2; handles coexistence of verifiers during transition phases.
- **NIST PQ submission references**: This plan is the NIST submission response for the "post-quantum migration" requirement in Calm Witness's formal assurance documentation.

---

## 11. Conclusion

Calm Witness v0 ships pre-quantum. The migration plan does not defer PQ safety indefinitely; instead, it establishes a clear governance path:

- v0 is known to be vulnerable; principals and operators acknowledge the risk window.
- v1 introduces hybrid signatures (immediate PQ-safe identity for operators).
- v1+ introduces hybrid commitments (PQ-safe distance commitments for sensitive disclosures).
- v2 deprecates classical cryptography entirely.
- v2+ is PQ-only.

The strategy is conservative: no unaudited lattice-based primitives in v0, no forced migration (v0 proofs remain valid forever), and a transition window (2027–2032) for adopting PQ standards as they mature.

This plan protects new disclosures beginning in 2029 (v1+ hybrid proofs) and ensures that by 2032 (v2 launch), Calm Witness is quantum-safe against all known threats. Legacy v0 proofs are archival by that date; new principals and operators use only v2+ cryptography.

---

— Calm, 2026-05-20
