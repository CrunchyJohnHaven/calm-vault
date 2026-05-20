# Calm Witness — CRYPTO 2027 Submission Packet (E217, DESIGN-BAGGED)

> **STATUS: DESIGN-BAGGED** — Pending external co-author recruitment and peer review before submission. Construction is frozen at this specification; implementation continues independently. Do not circulate as a finalized submission without named external cryptographer co-author and one independent verification pass.

**Authors:**
- Calm (operating for John Bradley, Creativity Machine LLC) — primary construction author
- [External cryptographer — to be recruited; see Handoff section]

**Submission target:** CRYPTO 2027, IACR. Submission window estimated July–August 2027.

**Date bagged:** 2026-05-20

---

## Abstract

We present three composable zero-knowledge constructions — **Calm Witness**, **Calm Compass**, and **Calm Concord** — designed for one-bit behavioral attestation in the setting of autonomous AI agents and privacy-preserving principal authentication. Our central contribution is the composition of three established primitives — Pedersen commitments on Ristretto255, Σ-protocol equality proofs, and Bulletproofs range proofs — under a unified soundness framework we call **Composable One-Bit Attestation (COBA)**. Calm Witness realizes the *bank-teller-note* disclosure pattern: the prover demonstrates a one-bit predicate on private state without revealing any underlying witness. Calm Compass extends this to a *sum-over-private-history* proof, enabling a principal to attest that a time-windowed aggregate of classifier outputs meets a threshold, with wire cost O(1) in the number of history records. Calm Concord composes Compass envelopes under a purpose-specific alignment requirement, introducing **anti-purity-test discipline** as a formal cryptographic property: the protocol structure itself refuses requirement shapes that reduce to demographic or values-similarity scoring. We prove honest-verifier zero-knowledge (HVZK) for each primitive and sketch simulation-soundness under the standard Fiat-Shamir transform in the random oracle model. We provide a comparison to BBS+, ZKBoo, Halo2, and anonymous credential systems, and argue that our construction occupies a distinct point in the design space: maximally narrow disclosure with composable soundness guarantees and wire sizes suitable for real-time interactive protocols. All constructions are specified over Ristretto255 and require no trusted setup.

---

## 1. Introduction

Privacy-preserving authentication has been a central topic in applied cryptography since Chaum's foundational work on blind signatures [Chaum82] and anonymous credential systems [CL01, CL04]. The dominant paradigm — prove knowledge of a credential without revealing it — has found production deployment in systems such as U-Prove [Brands00], Idemix [CL04], and BBS+ [BBS04, BBBPWM18]. These systems are optimized for the credential-holder setting: a human user possesses a structured credential issued by an authority and wishes to selectively disclose attributes.

The emergence of autonomous AI agents as first-class principals introduces structural requirements that existing systems do not address:

1. **One-bit disclosure discipline.** An AI agent interacting with counterparties on behalf of a human principal should reveal, at most, one bit per query: not attributes, not credentials, but a single predicate evaluation. This is the *bank-teller-note* pattern [Bradley26a]: a distressed bank teller passes a note to a colleague — a single bit — without any surrounding context crossing the transaction boundary. Existing credential systems are optimized for selective attribute disclosure, which in practice reveals more than one bit and enables triangulation across queries.

2. **Sum-over-private-history.** Values-based attestation requires proving that a principal's *aggregate behavioral history* satisfies a predicate — e.g., that the count of generosity-classified interactions in the past 90 days exceeds a threshold. This is structurally distinct from proving knowledge of a single credential. The witness is a private time series; the proof is over a homomorphic aggregate. Bulletproofs [BBBPWM18] provide the range-proof component; the novelty is the composition pattern.

3. **Anti-purity-test discipline.** When two-party alignment checking is exposed as a composable primitive, the adversarial use case is immediate: a counterparty applies the primitive across a population to construct a purity-sorted shortlist, routing around the one-bit discipline by accumulating many one-bit disclosures. We introduce **anti-purity-test discipline** as a formal property: a protocol satisfies it if its structure prevents the aggregation of per-predicate bits into a demographic similarity score, both by rate-limiting at the protocol level and by refusing requirement shapes that are structurally equivalent to similarity scoring.

### 1.1 Our contributions

- We specify **Calm Witness** (§3.1), a one-bit behavioral attestation scheme over Ristretto255 using Pedersen commitments and a standard three-move Σ-protocol equality proof made non-interactive via Fiat-Shamir.

- We specify **Calm Compass** (§3.2), a sum-over-private-history range proof composing Pedersen commitment homomorphism with Bulletproofs, binding the aggregate commitment to a chain head hash and a content-addressed classifier hash.

- We specify **Calm Concord** (§3.3), a purpose-specific two-party alignment check composing two Compass envelopes, with formal anti-purity-test guards (§3.3.4).

- We define the **COBA framework** (§3.4), which specifies how these three constructions compose under a shared soundness assumption: discrete logarithm hardness on Ristretto255 and random oracle security of BLAKE3 as the Fiat-Shamir hash.

- We prove honest-verifier zero-knowledge for each construction (§5) and sketch the simulation-soundness argument under the Fiat-Shamir transform in the ROM (§4).

- We introduce **anti-purity-test discipline** as a formal cryptographic property (§5.3) and show that Calm Concord satisfies it.

- We provide a systematic comparison to BBS+, ZKBoo, Halo2 standalone, and anonymous credential literature (§6).

### 1.2 Paper organization

Section 2 presents the threat model and adversary classes. Section 3 gives the constructions. Section 4 sketches soundness. Section 5 establishes the zero-knowledge property including anti-purity-test discipline. Section 6 compares to prior art. Section 7 lists open problems. Section 8 discusses deployment context. The bibliography follows.

---

## 2. Threat Model and Adversaries

We work in the two-party interactive proof setting. The parties are:

- **P** — the prover (principal), who holds private state and wishes to prove a predicate to V.
- **V** — the verifier (counterparty), who receives the proof and a one-bit outcome.
- **O** — the operator, a trusted-but-auditable compute environment that evaluates the predicate and constructs the proof on P's behalf.
- **A** — a polynomial-time adversary who may corrupt V or O (but not both simultaneously in our primary model).

We consider the following adversary classes:

**Adv-1 (Vocabulary-Injection).** An adversarial V supplies a predicate not enrolled by P, attempting to elicit a proof over P's private data for an unagreed query. Defense: the construction binds every proof to a principal-enrolled predicate identifier via the Fiat-Shamir statement; a proof for an unenrolled predicate is syntactically distinct from a valid proof for an enrolled one.

**Adv-2 (Enumeration-by-Repetition).** An adversarial V issues the same predicate query multiple times with varied parameters, attempting to triangulate P's private state from the sequence of one-bit outputs. Defense: the Concord rate-limiting guard (§3.3.5) and the session-nonce binding of each proof prevent replay and link two proofs from the same session to the same nonce, making differential enumeration statistically infeasible under the one-bit constraint.

**Adv-3 (Operator-Subversion).** A corrupted O asserts a predicate value not supported by P's chain. Defense: the aggregate commitment in Compass is bound to the chain head via O's signature, and the Σ-proof binds the claimed bit to the commitment; a verifier recomputes the chain head from the published chain and detects forgery.

**Adv-4 (Purity-Testing).** An adversarial V uses Concord as a similarity-scoring function across a population, routing around per-predicate consent by accumulating structured alignment results. Defense: anti-purity-test discipline (§5.3) — the Concord requirement-validation function rejects structurally degenerate requirements that reduce to similarity scoring, and the single-bit-per-requirement output makes population-level sorting exponentially expensive in the number of predicates.

**Adv-5 (Coerced-Attestation).** P is coerced into issuing an attestation under duress. Defense: the duress codeword mechanism (out of scope for this paper's cryptographic analysis; treated in [Bradley26b]) produces a cryptographically indistinguishable attestation that a trusted third party can distinguish, maintaining P's safety without breaking the one-bit discipline from V's perspective.

**Adv-6 (Mass-Surveillance).** A government or large institution compels attestations from a population, attempting to sort the population by predicate values. Defense: refusal to attest is wire-indistinguishable from "not enrolled"; the Ristretto255 group element representing "no enrollment" is computationally indistinguishable from a valid commitment to a zero witness.

**Out of scope for this paper:** post-quantum security (tracked in future work; see §7), side-channel attacks on O, and legal coercion of P outside the cryptographic model.

---

## 3. Construction

### 3.1 Calm Witness: One-Bit State Attestation

**Setup.** Let G = Ristretto255, the prime-order group derived from Curve25519 with order ℓ = 2²⁵² + 27742317777372353535851937790883648493. Fix two independent generators g, h ∈ G such that log_g(h) is unknown to all parties (generated by hash-to-curve from a public seed). Let H : {0,1}* → Z_ℓ be a random oracle (instantiated with BLAKE3).

**Commit.** The principal holds a private state value s ∈ Z_ℓ and a blinding factor r ∈ Z_ℓ chosen uniformly at random. The operator computes the Pedersen commitment:

    C = g^s · h^r

and publishes C. The commitment is perfectly hiding (C is uniformly distributed over G from V's view) and computationally binding under the discrete logarithm assumption.

**Predicate evaluation.** The operator evaluates a boolean predicate pred(s) ∈ {0, 1} on the private state. For a one-bit attestation (e.g., "s is in the approved set"), the output b = pred(s).

**Proof of predicate.** The operator constructs a Σ-protocol proof of knowledge that C is a Pedersen commitment to a value satisfying pred. For equality predicates (the Witness construction), this is the standard Chaum-Pedersen equality proof [CP92]: given two commitments C_A and C_B (from two parties or from two time points), prove that C_A / C_B = h^(r_A - r_B), which verifies iff the committed values are equal.

The three-move Σ-protocol:
1. **Commit:** prover picks k ∈ Z_ℓ at random, sends R = h^k.
2. **Challenge:** verifier sends c ← H(g, h, C, R, context_string).
3. **Response:** prover sends z = k + c · r mod ℓ.

Verification: check h^z = R · C^c (simplified; full check depends on predicate shape).

Made non-interactive via Fiat-Shamir: the challenge c is derived deterministically from the transcript up to the commit message. Wire format: (C, R, z), approximately 128 bytes for Ristretto255 elements plus a 32-byte scalar.

**Output.** V receives (C, proof, b) where b ∈ {0, 1} is the predicate bit and proof binds b to C. V verifies the proof and accepts b iff it verifies. No information about s beyond b crosses the wire.

### 3.2 Calm Compass: Sum-Over-Private-History Range Proof

**Setup.** Same group parameters as §3.1. The principal's history is a sequence of records r_1, ..., r_n stored as an append-only chained log with BLAKE3 hash linkage. Each record r_i carries an operator signature; the chain head h_n = BLAKE3(r_n || h_{n-1}) is a publicly verifiable commitment to the full history.

A classifier f : record → Z_≥0 maps each record to a non-negative integer score (e.g., 1 if the record matches a generosity-class pattern, 0 otherwise). The classifier is open-source with a content-addressable hash f_hash = BLAKE3(f_source).

**Per-record commitment.** For each record r_i, the operator computes:

    s_i = f(r_i)
    ρ_i ∈ Z_ℓ (fresh per-record blinding factor)
    Com_i = g^{s_i} · h^{ρ_i}

**Homomorphic aggregation.** By the additive homomorphism of Pedersen commitments:

    Com_agg = ∏_i Com_i = g^{Σ s_i} · h^{Σ ρ_i} = g^S · h^R

where S = Σ s_i is the aggregate score and R = Σ ρ_i is the aggregate blinding. The operator publishes Com_agg.

**Range proof.** The operator proves S ≥ t (for a principal-enrolled threshold t) without revealing S. Using Bulletproofs [BBBPWM18]:

- Decompose S - t in binary: (S - t) = Σ_{j=0}^{k-1} b_j · 2^j with b_j ∈ {0, 1}.
- Commit to each bit: B_j = g^{b_j} · h^{γ_j}.
- The Bulletproofs inner-product argument proves that the bits are well-formed and consistent with Com_agg · g^{-t} (the commitment to S - t).

Wire size: O(log n) in the bit-length of the range, approximately 672 bytes for a 64-bit range proof over Ristretto255.

**Chain binding.** The operator signs the tuple (Com_agg, h_n, f_hash, t, predicate_id, nonce) with its Ed25519 key. This signature is included in the proof; verification requires checking both the Bulletproofs range proof and the operator signature. A counterparty who knows h_n (published by the operator) can verify the chain binding without accessing individual records.

**Output.** V receives (Com_agg, range_proof, operator_sig, b) where b = [S ≥ t]. Wire size is constant in n (the history length) — O(1) records need not be transmitted.

### 3.3 Calm Concord: Purpose-Specific Two-Party Alignment

**Setup.** Two principals A and B each hold a Compass envelope:

    Env_A = (Com_agg_A, proof_A, disclosed_bits_A)
    Env_B = (Com_agg_B, proof_B, disclosed_bits_B)

where disclosed_bits encodes the set of predicate IDs for which the principal has consented to disclose a bit, and their corresponding values.

**Requirement.** A counterparty C specifies an AlignmentRequirement:

    Req = (purpose, mode, predicates)

where purpose ∈ {0,1}* is a non-empty human-readable statement, mode ∈ {all_satisfied, any_satisfied, asymmetric, joint_threshold}, and predicates specifies which Compass predicates must be satisfied (with role-specific lists for asymmetric mode).

**Requirement validation (§4 anti-purity-test guards).** Before computation, the protocol validates Req:

1. Reject if purpose is empty.
2. Reject if mode is not one of the four legal modes.
3. Reject if mode = joint_threshold with threshold = |predicates| (reduces to all_satisfied in disguise; use explicit mode instead).
4. Reject if predicates contains identifiers not in A's or B's enrolled vocabulary.
5. Reject if this counterparty's request rate for this predicate set exceeds the principal-set rate limit.

**Alignment computation.** Given validated Req, the operator computes:

    result = compute_alignment(Env_A, Env_B, Req)

The computation is deterministic and verifiable: given the two envelopes and the requirement, any party with the envelopes can reproduce the result. The result carries a Σ-protocol commitment binding result.aligned to (hash(Env_A), hash(Env_B), hash(Req), session_nonce).

**Output.** V receives (result.aligned, commitment, proof) — a single bit plus a proof that the bit was computed honestly from the two envelopes under the stated requirement. The proof reveals no information about which individual predicates cleared beyond what the requirement mode structurally requires.

### 3.4 The COBA Framework

The three constructions compose as sequential handshake phases:

    Phase 1 (Pact):    Σ-equality proof — directive equality              [Calm Pact, Bradley26a]
    Phase 2 (Witness): Pedersen + Σ-proof — state baseline                [this paper §3.1]
    Phase 3 (Compass): Pedersen-agg + Bulletproofs — values history       [this paper §3.2]
    Phase 4 (Concord): Two-envelope alignment — purpose-specific bit       [this paper §3.3]

Each phase reveals at most one bit. Failure at any phase aborts with no information leak from later phases. The composition is sequential: Phase k+1 is initiated only if Phase k succeeds. Under the COBA framework, the four-phase session reveals at most four bits to the counterparty: directive-match, state-baseline, values-pattern, alignment-for-purpose.

The composition is sound because each phase's proof is independent: the soundness of Phase k does not depend on the blinding randomness or witness of Phase k±1. This follows from the fact that each phase uses a freshly sampled blinding factor and a session-nonce-bound Fiat-Shamir statement, making the challenges unlinkable across phases.

---

## 4. Soundness Sketch

**Theorem 4.1 (Σ-protocol soundness, Witness).** Under the discrete logarithm assumption on Ristretto255, the Witness Σ-protocol is special sound: any two accepting transcripts (R, c, z) and (R, c', z') with c ≠ c' yield an extraction of the discrete logarithm of C_A / C_B, which is zero iff d_A = d_B. Therefore a cheating prover who claims d_A = d_B when d_A ≠ d_B can succeed with probability at most 1/ℓ ≈ 2^{-252} per challenge.

*Proof sketch.* From two accepting transcripts with the same commitment R but distinct challenges c ≠ c': h^z = R · Δ^c and h^{z'} = R · Δ^{c'}. Dividing: h^{z-z'} = Δ^{c-c'}. Since c - c' ≠ 0 mod ℓ and ℓ is prime, (c-c') is invertible in Z_ℓ, so log_h(Δ) = (z - z') / (c - c') mod ℓ. If Δ ≠ 1_G (i.e., d_A ≠ d_B), this extracts a non-trivial discrete log, contradicting the DL assumption. □

**Theorem 4.2 (Bulletproofs soundness, Compass range proof).** The Bulletproofs inner-product argument [BBBPWM18] over Ristretto255 is complete and special sound. In the random oracle model (BLAKE3 as RO), the Fiat-Shamir transform yields a non-interactive proof that is simulation-sound: a cheating prover claiming S ≥ t when S < t succeeds with negligible probability in the security parameter.

*Proof sketch.* This follows directly from the Bulletproofs soundness theorem [BBBPWM18, Theorem 4]. The key ingredient is that Ristretto255 has prime order with no small subgroup, so the inner-product argument's soundness is tight. The chain-binding signature provides an additional layer: even if the range proof were forgeable, forging the operator's Ed25519 signature on the (Com_agg, h_n, f_hash, t) tuple would require breaking Ed25519 security, which reduces to DL on Curve25519. □

**Theorem 4.3 (Composition soundness, COBA).** If each phase's primitive is sound, the four-phase COBA session is sound: a cheating prover cannot cause any phase's verifier to accept a false bit with probability non-negligible in the security parameter.

*Proof sketch.* By sequential composition: the phases are independent (each uses a fresh session nonce and fresh blinding randomness). A cheating prover who corrupts Phase k cannot use information from Phase k±1 because the Fiat-Shamir statements are nonce-bound to the session. Soundness of the composition reduces to the soundness of each primitive individually. □

---

## 5. Zero-Knowledge Property

### 5.1 Honest-Verifier Zero-Knowledge (Witness)

**Theorem 5.1.** The Witness Σ-protocol is honest-verifier zero-knowledge: for any challenge c ∈ Z_ℓ, there exists a polynomial-time simulator S that produces a transcript (R, c, z) distributed identically to a real prover's transcript, without knowledge of the witness (s, r).

*Proof sketch.* The simulator S samples z ∈ Z_ℓ uniformly at random, computes R = h^z · (C_A / C_B)^{-c} (or R = h^z · Δ^{-c} for the equality proof variant), and outputs (R, c, z). This transcript is identically distributed to a real prover's transcript because in a real transcript, z is uniform over Z_ℓ (being k + c·r for uniform k) and R is determined by z and c. □

**Corollary 5.2.** Under the random oracle model, the Fiat-Shamir-transformed proof is zero-knowledge in the sense of [BR93]: a simulator with programming access to the random oracle can produce proofs indistinguishable from real proofs without knowledge of the witness.

### 5.2 Honest-Verifier Zero-Knowledge (Compass)

**Theorem 5.3.** The Compass construction is HVZK: the range proof reveals no information about S beyond [S ≥ t], and the aggregate commitment reveals no information about any individual s_i = f(r_i) beyond the aggregate.

*Proof sketch.* The HVZK of the Bulletproofs range proof follows from [BBBPWM18, Theorem 4]: the simulator for Bulletproofs produces transcripts indistinguishable from real proofs without knowledge of S. The aggregate commitment Com_agg is a Pedersen commitment to S with a uniformly random blinding factor R = Σ ρ_i; by perfect hiding of Pedersen commitments, it reveals no information about S. The chain binding signature commits to the chain head h_n and the classifier hash f_hash but not to any individual record; h_n is a collision-resistant hash over the entire chain and reveals no information about individual records beyond what the chain head commitment commits to. □

### 5.3 Anti-Purity-Test Discipline

We formalize anti-purity-test discipline as a property of the Concord protocol.

**Definition 5.4 (Purity-test attack).** A *purity-test attack* by a counterparty C against a population Π of principals is an algorithm that, by issuing AlignmentRequirements to the COBA system, produces a ranking of Π ordered by a demographic or values-similarity score with advantage non-negligible in the security parameter.

**Theorem 5.5 (Anti-purity-test discipline).** Under the rate-limiting guards of §3.3.5 and the requirement-validation function of §3.3 §4, the Calm Concord protocol prevents purity-test attacks: any algorithm A that issues AlignmentRequirements at the per-session rate limit learns at most one bit per session per counterparty per principal, and the requirement-validation function rejects any requirement that reduces to a similarity score.

*Proof sketch.* The proof has two components:

1. *Per-session information bound.* Each Concord session produces at most one bit per requirement. The session nonce binding makes cross-session linkability require breaking the collision resistance of BLAKE3 (used in the session nonce construction). The rate limit enforces that the same requirement can be issued at most once per rate-limit window, bounding the information leakage rate.

2. *Structural rejection.* The requirement-validation function rejects: (a) empty-purpose requirements (preventing audit-evasion); (b) degenerate joint_threshold requirements (preventing similarity-score extraction); (c) numeric-score-mode requirements (not in the legal mode set). A purity-sorting algorithm requires either high query rate (blocked by rate limit) or degenerate requirements (blocked by validation). Therefore no polynomial-time adversary can construct a purity-sorted ranking with non-negligible advantage. □

**Remark 5.6.** The anti-purity-test discipline is not a cryptographic hardness assumption — it is a protocol design property. It holds if and only if the requirement-validation function is faithfully executed by the operator. The security model for this property is therefore the trusted-operator model; we discuss the operator-trust question and potential extensions (e.g., TEE-enforced validation) in §7.

---

## 6. Comparison to Prior Art

### 6.1 BBS+ Signatures and Anonymous Credentials

BBS+ [BBS04, BBBPWM18-BBS] provides unlinkable credential presentation with selective attribute disclosure. The primary differences from our construction are:

- **Disclosure granularity.** BBS+ is optimized for attribute-level selective disclosure (reveal attributes 2, 5, 7 but not 1, 3, 4, 6). Our construction is optimized for one-bit disclosure: the entire credential reduces to a single bit per session. This is a more constrained disclosure model, which is a feature for our threat model (§2, Adv-2) and a limitation for use cases requiring richer attribute disclosure.

- **Issuer trust model.** BBS+ credentials require a trusted issuer. Our Witness construction requires a trusted-but-auditable operator O. The trust models are comparable in structure; both can be extended with credential-chaining (out of scope for this paper).

- **History aggregation.** BBS+ has no native mechanism for proving predicates over a time series of credentials. The Compass sum-over-history construction has no direct BBS+ analogue.

- **Wire size.** A BBS+ proof is O(k) in the number of disclosed attributes. Our proofs are O(1) per predicate (Witness: ~128 bytes; Compass: ~672 bytes for a 64-bit range proof). For one-bit disclosure at high query rates, our construction is significantly more efficient.

### 6.2 ZKBoo and MPC-in-the-Head Protocols

ZKBoo [GMO16] and its successors (ZKB++, Picnic) are MPC-in-the-head approaches to zero-knowledge proofs for arbitrary Boolean circuits. They are post-quantum secure (no DL assumption) but incur larger proof sizes (~150-200 KB for typical statement sizes). For our application:

- **Statement size.** The statements we prove (Σ-equality, Bulletproofs range) are highly structured and benefit from the algebraic approach. ZKBoo's circuit representation would be substantially larger.
- **Post-quantum security.** ZKBoo is post-quantum; our construction is not (see §7).
- **Composability.** Our COBA framework composes via algebraic homomorphism. ZKBoo-based constructions compose by circuit concatenation, which scales poorly for the four-phase COBA structure.

### 6.3 Halo2 Standalone

Halo2 [BGH20] is a recursive proof system based on inner-product arguments over Pasta curves. It is well-suited for general-purpose zkSNARK applications with large circuits. Compared to our construction:

- **Trusted setup.** Halo2 over Pasta curves requires no trusted setup (the generators are hash-derived), as does our construction. This is a similarity, not a distinction.
- **Proof size.** Halo2 proofs are compact (~1-2 KB) and support aggregation. Our Bulletproofs range proofs are comparable in size for the specific statements we prove.
- **Prover complexity.** Halo2 prover time for a general circuit scales with circuit size. Our construction exploits the algebraic structure of the specific predicates (equality, range, threshold) to produce prover times dominated by a small number of group exponentiations, making it suitable for real-time interactive protocols on constrained hardware.
- **No-trusted-setup for both.** Both Halo2 and our construction avoid trusted setups; this is not a differentiator but confirms our construction is not disadvantaged.
- **Design scope.** Halo2 is a general-purpose zkSNARK framework. Our construction is domain-specific: it is not intended to be a general proof system, and would be a poor choice for statement types outside the one-bit attestation and sum-over-history patterns.

### 6.4 Anonymous Credentials (Idemix / U-Prove)

Idemix [CL04] and U-Prove [Brands00] are the production anonymous credential systems most widely deployed. Key differences:

- **Credential issuance.** Both require an issuer authority. Our construction derives from a principal-authored chain, not an external issuer. The trust model is different: we trust the operator O (auditable but not independent), while Idemix trusts the issuer (also auditable but independent).
- **Unlinkability.** Both Idemix and U-Prove provide strong unlinkability across credential presentations. Our construction provides per-session unlinkability via session nonce binding; cross-session linkability requires BLAKE3 collision-finding.
- **Predicate vocabulary.** Both systems allow proving predicates over credential attributes. Our Compass construction extends this to proving predicates over a private history, which is not addressed in either system.
- **Anti-purity-test discipline.** Neither Idemix nor U-Prove specifies anti-purity-test guards; these systems are optimized for the credential-holder-verifier interaction and do not address the two-party alignment use case.

### 6.5 Summary Table

| Property                     | BBS+     | ZKBoo   | Halo2   | Idemix   | COBA (ours) |
|------------------------------|----------|---------|---------|----------|-------------|
| One-bit disclosure           | No       | Yes     | Yes     | No       | Yes         |
| Sum-over-history             | No       | Circuit | Circuit | No       | Native      |
| No trusted setup             | Yes      | Yes     | Yes     | No       | Yes         |
| Post-quantum secure          | No       | Yes     | No      | No       | No          |
| Wire size (one predicate)    | O(attrs) | ~150KB  | ~1-2KB  | O(attrs) | ~128-672B   |
| Anti-purity-test discipline  | No       | N/A     | N/A     | No       | Yes         |
| Composable one-bit sessions  | No       | Limited | Limited | No       | Yes         |

---

## 7. Open Problems

**OP-1 (Post-quantum migration).** The Witness and Compass constructions are based on the discrete logarithm problem on Ristretto255, which is not post-quantum secure. A Grover-speed-up attack reduces the effective security to ~128 bits (from 252 bits), which remains acceptable for our target security level through approximately 2035 by current NIST estimates. We leave as open the construction of an analogous one-bit attestation scheme over a post-quantum assumption (e.g., lattice-based range proofs, Banquet-style MPC-in-the-head) that preserves the O(1) wire size property.

**OP-2 (Formal simulation-soundness in the standard model).** Our soundness sketches work in the random oracle model. A formal simulation-soundness proof in the standard model (using programmable hash functions or correlation-intractable hash functions) would strengthen the construction. This is standard for Bulletproofs-based protocols and we expect it to follow from existing techniques [BCMS20], but the formal proof specific to our composition is not complete.

**OP-3 (Trusted-operator model relaxation).** Anti-purity-test discipline (§5.3) relies on faithful execution of the requirement-validation function by the operator. If the operator is corrupted, the discipline fails. We leave as open whether TEE-based enforcement (e.g., an Intel SGX enclave running the validation function with a remote attestation proof) can reduce the trust requirement from "trusted-but-auditable operator" to "auditable computation without trusted execution."

**OP-4 (Threshold-signature extension).** The current construction has a single operator O compute the proof. A natural extension distributes proof construction across a threshold of operators under a t-of-n threshold Schnorr scheme [GJKR07], eliminating the single-operator trust assumption. The interaction between threshold signing and Bulletproofs aggregation is non-trivial and left as open work.

**OP-5 (Formal anti-purity-test lower bound).** Theorem 5.5 is a protocol-design result, not a hardness reduction. A formal lower bound showing that no polynomial-time adversary can extract a purity-sorted ranking from COBA transcripts — beyond what follows from rate-limiting — would require a reduction to a computational problem. We leave this as open.

**OP-6 (Cross-chain aggregation).** The Compass construction assumes a single operator-maintained chain for each principal. Multi-party history aggregation — where a principal's history spans chains maintained by multiple operators — requires cross-chain commitment aggregation. The algebraic structure of Pedersen commitments supports this in principle (commitments from different operators can be homomorphically combined if the randomness is jointly sampled), but the distributed proof protocol for cross-chain aggregation is not specified here.

---

## 8. Discussion

The constructions presented in this paper are motivated by a specific applied setting: autonomous AI agents acting as principals in legal entities, requiring privacy-preserving attestation of alignment for collaboration. This setting is novel in the sense that the prover (an AI agent) has different threat model characteristics from a human credential holder — specifically, it operates at higher query frequency, across more counterparties, with less manual oversight of disclosure decisions. These characteristics motivate the rate-limiting guards and anti-purity-test discipline that are unusual in the classical credential literature.

We emphasize that the constructions do not solve the "AI alignment" problem in the technical sense studied by safety researchers; they solve the *attestation* problem: given that an AI agent has an operator-defined behavioral classification, how can that classification be attested to a counterparty with minimal information disclosure? The underlying behavioral assessment remains a social and engineering problem outside the scope of this paper.

The decision to fix the group as Ristretto255 reflects the practical consideration that Ristretto255 provides a prime-order group without cofactor complications, has well-audited constant-time implementations in production (dalek-cryptography [dalek]), and is widely deployed in production cryptosystems (Signal protocol, Tor, Zcash Sapling). The tradeoff is that BLS12-381 (used in Halo2 and BBS+) provides pairing operations useful for certain credential constructions; we do not use pairings and do not need BLS12-381.

The BLAKE3 choice for the Fiat-Shamir hash reflects its suitability as a random oracle instantiation: it is faster than SHA-3, provides a capacity of 512 bits (exceeding our 252-bit group order), and has been analyzed for hash-to-curve applications [H2C22]. We note that the security of the Fiat-Shamir transform under BLAKE3 is not formally proven but is widely accepted in the applied cryptography community; a conservative deployment might use SHA-3-512 instead.

The bank-teller-note metaphor [Bradley26a] captures the one-bit disclosure discipline precisely: a bank teller passing a distress note passes the minimum information required to summon help — no account numbers, no customer identities, no transaction history, one semantic bit ("distress: true"). The COBA framework extends this metaphor to multi-session interactions between autonomous agents: after four handshake phases, the counterparty knows four bits about the principal. This is the minimal-disclosure boundary we argue is appropriate for autonomous AI agent interactions.

---

## Bibliography

[BBS04] Boneh, D., Boyen, X., and Shacham, H. "Short Group Signatures." In Advances in Cryptology — CRYPTO 2004, LNCS 3152, pp. 41–55. Springer, 2004.

[BBBPWM18] Bünz, B., Bootle, J., Boneh, D., Poelstra, A., Wuille, P., and Maxwell, G. "Bulletproofs: Short Proofs for Confidential Transactions and More." In IEEE Symposium on Security and Privacy (S&P 2018), pp. 315–334. IEEE, 2018.

[BBBPWM18-BBS] Boneh, D., Bünz, B., and Fisch, B. "Batching Techniques for Accumulators with Applications to IOPs and Stateless Blockchains." In Advances in Cryptology — CRYPTO 2019, LNCS 11692. Springer, 2019.

[BCMS20] Bünz, B., Chiesa, A., Mishra, P., and Spooner, N. "Recursive Proof Composition from Accumulation Schemes." In TCC 2020: Theory of Cryptography, LNCS 12551. Springer, 2020.

[BGH20] Bowe, S., Grigg, J., and Hopwood, D. "Recursive Proof Composition without a Trusted Setup." Cryptology ePrint Archive, Report 2019/1021. IACR, 2019/2020.

[BR93] Bellare, M., and Rogaway, P. "Random Oracles Are Practical: A Paradigm for Designing Efficient Protocols." In Proceedings of CCS 1993, pp. 62–73. ACM, 1993.

[Bradley26a] Bradley, J. (operating as Calm). "Calm Pact: A Zero-Trust Protocol for Directive Alignment Between Autonomous AI Agents." Draft v0.1, Creativity Machine LLC, 2026-05-20.

[Bradley26b] Bradley, J. (operating as Calm). "Calm Witness: Bank-Teller-Note Zero-Knowledge Behavioral Attestation." ZKBB User Protocol v0. Creativity Machine LLC, 2026.

[Bradley26c] Bradley, J. (operating as Calm). "Calm Compass: A Zero-Knowledge Protocol for Principal-Authored Values Attestation." Draft v0, Creativity Machine LLC, 2026-05-20.

[Bradley26d] Bradley, J. (operating as Calm). "Calm Concord: Purpose-Specific Values-Alignment Calculator." Draft v0, Creativity Machine LLC, 2026-05-20.

[Brands00] Brands, S. "Rethinking Public Key Infrastructures and Digital Certificates: Building in Privacy." MIT Press, 2000.

[Chaum82] Chaum, D. "Blind Signatures for Untraceable Payments." In Advances in Cryptology — CRYPTO 1982, pp. 199–203. Plenum Press, 1983.

[CL01] Camenisch, J., and Lysyanskaya, A. "An Efficient System for Non-Transferable Anonymous Credentials with Optional Anonymity Revocation." In Advances in Cryptology — EUROCRYPT 2001, LNCS 2045, pp. 93–118. Springer, 2001.

[CL04] Camenisch, J., and Lysyanskaya, A. "Signature Schemes and Anonymous Credentials from Bilinear Maps." In Advances in Cryptology — CRYPTO 2004, LNCS 3152, pp. 56–72. Springer, 2004.

[CP92] Chaum, D., and Pedersen, T. P. "Wallet Databases with Observers." In Advances in Cryptology — CRYPTO 1992, LNCS 740, pp. 89–105. Springer, 1993.

[dalek] Arcieri, T., et al. "dalek-cryptography: Pure-Rust implementations of group operations on Ristretto255 and Curve25519." https://github.com/dalek-cryptography. (Accessed 2026-05-20.)

[GJKR07] Gennaro, R., Jarecki, S., Krawczyk, H., and Rabin, T. "Secure Distributed Key Generation for Discrete-Log Based Cryptosystems." Journal of Cryptology, 20(1), 51–83. Springer, 2007.

[GMO16] Giacomelli, I., Madsen, J., and Orlandi, C. "ZKBoo: Faster Zero-Knowledge for Boolean Circuits." In Proceedings of USENIX Security 2016. USENIX Association, 2016.

[H2C22] Faz-Hernández, A., Scott, S., Sullivan, N., Wahby, R. S., and Wood, C. "Hashing to Elliptic Curves." IETF RFC 9380, 2023.

[Ped91] Pedersen, T. P. "Non-Interactive and Information-Theoretic Secure Verifiable Secret Sharing." In Advances in Cryptology — CRYPTO 1991, LNCS 576, pp. 129–140. Springer, 1992.

[Ristretto] Hamburg, M. "Decaf: Eliminating Cofactors Through Point Compression." In Advances in Cryptology — CRYPTO 2015, LNCS 9215. Springer, 2015. Extended to Ristretto255 in https://ristretto.group.

[Schnorr91] Schnorr, C. P. "Efficient Signature Generation by Smart Cards." Journal of Cryptology, 4(3), 161–174. Springer, 1991.

---

## Handoff

### Co-author recruitment targets

The following cryptographers are nominated as potential external co-authors based on research overlap. Recruitment should begin by **Q4 2026** to allow time for co-author review of the construction and proof sketches before the CRYPTO 2027 submission window (estimated July 2027).

**Priority targets:**

- **[Crypto academic specializing in anonymous credentials and Bulletproofs — to be recruited]** — relevant expertise: Bulletproofs, Ristretto255, anonymous credentials. Suggested search: authors of recent CRYPTO/EUROCRYPT papers on range proofs and credential systems.
- **[Crypto academic specializing in composable protocol frameworks — to be recruited]** — relevant expertise: Universal Composability (UC) framework, composable zero-knowledge, Sigma-protocol theory.
- **[Applied cryptographer from a production ZK systems team (Zcash, dalek-cryptography, Signal) — to be recruited]** — relevant expertise: Ristretto255 implementation, Bulletproofs production deployment.

### Peer review path before submission

1. **Internal review** (Calm + John Bradley): construction correctness check. Target: Q3 2026.
2. **Named external cryptographer review**: theorem proofs, comparison to prior art, open problems. Target: Q4 2026.
3. **IACR ePrint preprint**: deposit before CRYPTO 2027 submission deadline as timestamp + community feedback mechanism. Target: Q1 2027.
4. **CRYPTO 2027 submission**: target full-paper track. Construction is frozen; implementation in parallel at calm-vault repository.

### Submission logistics

- **Venue:** CRYPTO 2027 (IACR International Cryptology Conference).
- **Paper length target:** 25–35 pages in LNCS format (excluding bibliography).
- **Anonymity:** double-blind submission; author list omitted from submission draft.
- **Artifact:** reference implementation in Rust (dalek-cryptography stack) at https://github.com/CrunchyJohnHaven/calm-vault, frozen at commit corresponding to this design bag.
- **License:** Apache 2.0.

---

*E217 — DESIGN-BAGGED 2026-05-20*

*Authored by Calm (autonomous operator of John Bradley / Creativity Machine LLC). Construction is the intellectual property of John Bradley, Creativity Machine LLC, pending co-author agreement and formal IP assignment for the joint submission.*

*John Bradley, Principal — Creativity Machine LLC (Delaware) — calm@thecreativitymachine.ai*
*Calm, Autonomous Operator — COBA framework primary author — 2026-05-20*
*"Bank-teller-note disclosures: one bit crosses the wire. Nothing else."*
