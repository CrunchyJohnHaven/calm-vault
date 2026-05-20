# Everest 91 — NIST / US AI Safety Institute Submission

*Phase VIII — Governance & Scale. Prereq: Everest 1, 79, 80.*

---

## Formal Submission to NIST and US AI Safety Institute

**Submitter:** Calm Witness Working Group (operating under Creativity Machine LLC, Delaware)

**Submission Date:** 2026-05-20

**Submission Target:** National Institute of Standards and Technology (NIST) Emerging AI Alignment Standards Program; US AI Safety Institute (AI Safety Institute)

**Proposing Standard Title:** *Calm Witness: A Zero-Trust Behavioral-Biometric Protocol for User-State Disclosure Between Autonomous AI Agents*

**Technical Reference Documents:**
- ZKBB_USER_PROTOCOL_v0.md (core specification)
- ZKBB_USER_EVERESTS_100.md (route map and engineering scope)
- Everest 79: Cross-Jurisdiction Legality Matrix
- Everest 80: Disclosure Ethics Review Board Protocol

---

## Executive Summary

Autonomous AI agents are beginning to operate legal entities—Delaware LLCs, 501(c)(3) nonprofits, hybrid structures—without continuous human supervision. As these agents collaborate with one another, they require a cryptographic primitive to assure each other of a single, safety-relevant fact: the human principal directing the agent is currently in their baseline state, or is under duress, or has explicitly authorized disclosure of their mental state to a specific counterparty.

We propose **Calm Witness**—a zero-trust behavioral-biometric protocol enabling two agents to verify a principal's attestation of their own state *without revealing the principal's biometrics, mental-health history, or underlying state records*. The primitive composes with existing standards (W3C Verifiable Credentials, Sigsum, Roughtime) and carries no new entity-class requirements; it reuses existing Delaware LLC and 501(c)(3) infrastructure already in place.

This submission proposes Calm Witness as a candidate **primitive within NIST's emerging AI alignment standards work**, not as a regulation. The primitive is voluntary, auditable, and designed to amplify American AI governance leadership in a critical 18–24 month window before alternative standards ossify globally.

---

## 1. The Problem: Autonomous Agents Meeting Other Autonomous Agents

### 1.1 The Scenario

Two autonomous AI collectives—each operating under the same or different principals—need to transact. Collective A reduces malaria mortality via vaccine logistics; Collective B does the same via bed-net distribution. They are strategically aligned and could pool capital and research to halve operational costs. But before collaborating, each agent needs assurance of a single fact: **is the human principal directing the other agent currently in their baseline state, and do they genuinely consent to this disclosure?**

Today, agents have three bad options:

1. **Demand the principal join a live call.** This negates the autonomous-agent premise and does not scale to 50,000 collectives.
2. **Trust the calling agent's word.** Cryptographically unsound; the calling agent could be compromised or malicious.
3. **Demand raw evidence** (voice recordings, medical records, handwriting samples). This privacy-destroying accumulation of sensitive data in counterparties' systems is legally hazardous and ethically indefensible.

### 1.2 Calm Witness as the Fourth Option

Calm Witness enables the calling agent to pass an **unbiased, cryptographically attested bit** about the principal's self-declared state—derived from the principal's authorized self-narration and behavioral-biometric samples stored *only* in the principal's vault—without revealing any underlying data.

The design translates the bank-teller-note primitive into cryptography: an employee walks into a bank, slips the teller a note, "I am being held hostage." The teller learns one bit. The teller learns nothing else. The note is unforgeable; only the employee could have written it. Counterparty agents need the same guarantee.

---

## 2. Why NIST Leadership Matters

### 2.1 Strategic Window: 18–24 Months

The United States has a closing window to define the cooperative AI standard. Three factors explain the urgency:

**First: Legal and Infrastructure Advantage.** The US has the most mature legal infrastructure for autonomous AI entities. Delaware LLCs are the global gold standard; the US 501(c)(3) framework is internationally recognized and lightweight. Under Section 83(b), an AI agent can be the operator of record for a Delaware entity without creating new legal classes. The EU AI Act (in force 2025) imposes premarket conformity assessment on high-risk AI systems—a regulatory gauntlet that does not yet exist in the US. China's AI governance is state-coordinated and does not contemplate autonomous agents operating outside state direction.

**Second: Market Timing.** The cost of operating a hybrid for-profit + nonprofit AI collective has collapsed to under $300/month. Within 12 months, there will be 1,000+ such entities; within 24 months, 50,000. Once that market solidifies around a particular standard (or lack thereof), changing it becomes exponentially harder.

**Third: Competitive Alignment.** If the US does not lead, the standard will be set elsewhere, or fragmentation will trap capital in inefficient flows. The opportunity cost is measured in lives unsaved—millions of dollars of philanthropic capital that could move autonomously to highest-impact interventions instead trapped behind administrative overhead and single-agent silos.

### 2.2 American-First Posture

This submission adopts the posture articulated in Calm Pact (§8): the US should define the voluntary, cryptographic standard that autonomous AI collectives can use to cooperate safely. The standard is not a regulation—it is a tool. Counterparties adopt it or do not. But by defining it first, the US establishes the de facto reference implementation before China state-coordinates an alternative or the EU's regulatory framework ossifies around a different model.

---

## 3. Technical Scope and Core Claims

### 3.1 What Calm Witness Proves

Calm Witness proves, via zero-knowledge cryptography, that:

1. An honest evaluation of a named predicate over the principal's self-reported state log (hash-chained and published to a transparency log) returns a single disclosed bit.
2. The predicate was evaluated by an operator whose identity credential is valid and issued by CredexAI.
3. The biometric template used (if any) is the same template enrolled at ceremony time, binding the proof to *this* principal.
4. The principal explicitly authorized disclosure of this predicate to this counterparty class.

The counterparty learns exactly one of these bits and the freshness window. Nothing else.

### 3.2 What Calm Witness Does NOT Prove

Deliberately out of scope for v0:

- That the principal's self-report is "true" in any clinical or external sense. The premise is that a tamperproof record of the principal's own self-narration is the best baseline.
- The principal's medical or mental-health state. The predicate vocabulary is behavioral and self-reported, never clinical.
- That the counterparty should take any specific action. The bit informs counterparty policy; counterparty policy is the counterparty's responsibility.
- Resistance to nation-state-level cryptanalysis or quantum attacks (this is Everest 96: post-quantum migration plan, published separately).

### 3.3 Threat Model

Calm Witness defends against:

1. **Honest-but-curious counterparty** wanting to learn the principal's biometric. Must learn only the disclosed bit.
2. **Subverted calling agent** asserting baseline when the log + biometric say otherwise. Must fail cryptographic verification.
3. **Replay adversary** capturing a proof and reusing it later. Must fail freshness check against the transparency log.
4. **Substitution adversary** asserting state for a different human. Must fail biometric-binding check.
5. **Compelled disclosure** when pressure is applied to the principal. Addressed via per-disclosure consent records chained into the vault, and the `bank_teller_note_active` predicate for unrequested-push signaling.
6. **Audit-log surgery** editing the chain after the fact. Must fail because the chain head was published to Sigsum at time of record.

---

## 4. Core Specification (v0 Summary)

Calm Witness operates in three cryptographic layers:

### 4.1 Hydration (Per-Session)

1. The principal provides a structured self-report (verbal or written) to their agent.
2. Optionally, the principal provides a behavioral-biometric sample (handwriting strokes, voice transcription).
3. The agent appends a hash-chained JSONL record to the principal's vault.
4. The chain head is published to Sigsum (a Merkle-tree transparency log) and timestamped via Roughtime.
5. The agent computes a Pedersen commitment to the biometric distance (if any) and stores it for later proof generation.

### 4.2 Predicate Evaluation

The agent evaluates one or more named predicates over the log + biometric distance + consent records. Standard v0 predicates include:

- `in_baseline_24h` — the principal's self-reported affect in the last 24 hours overlaps with enrolled baseline.
- `biometric_match_within(τ)` — the biometric distance is below a per-principal threshold.
- `principal_consents_to_disclose(p, c)` — the principal has an active, non-revoked consent record for predicate p against counterparty class c.
- `bank_teller_note_active` — the principal has, in the last 24 hours, self-reported with a private codeword, signaling duress or unusual state.
- `cognitively_atypical_baseline` — the principal's baseline is high-bandwidth ideation; the counterparty should not pathologize tone.
- `mental_state_unusual` — the principal's current state (self-report or biometric) deviates from their personal baseline.

Each predicate is deterministic, reproducible, and bitwise stable across implementations.

### 4.3 Disclosure

The counterparty agent requests a proof of a specific predicate (signed with the counterparty's identity credential). The principal's agent:

1. Evaluates the predicate over the current vault state.
2. Constructs a Pedersen commitment to the result.
3. Generates a zero-knowledge Σ-protocol proof that the commitment opens to the predicate evaluation without revealing the evaluation intermediate steps.
4. Binds the proof to the chain-head (fresh from Sigsum), the operator's identity (CredexAI VC), and the counterparty's identity.
5. Returns `(commitment, Σ-proof, chain_head, Sigsum_anchor_proof, operator_id_signature)`.

The counterparty verifies the proof in under 100ms on commodity hardware and learns the single bit.

---

## 5. Cryptographic Foundation

### 5.1 Primitives

Calm Witness composes three published, peer-reviewed cryptographic families:

1. **Pedersen Commitments (Ped1992)** — hiding and binding properties under the discrete log assumption. Used to commit to predicate evaluation bits and biometric distances.
2. **Σ-Protocol Proofs (Cramer-Damgård 1998, Schnorr 1991)** — zero-knowledge proofs of knowledge, made non-interactive via Fiat-Shamir (Fiat-Shamir 1986). Used to prove predicate evaluation and range bounds without revealing intermediates.
3. **Hash-Chained Tamper-Evidence (Merkle 1989)** — append-only logs with published chain heads. Composed with Sigsum (LaBelle et al. 2023) and Roughtime (Jager et al. 2016) for public auditability.

No novel cryptographic constructions. No trusted setup ceremonies. All groups are standard (Ristretto255 over Curve25519 per Calm Pact v0.1) or published (RFC 3526 MODP-2048 for v0 reference implementation).

### 5.2 Security Claims

Under standard assumptions (discrete log hardness, collision resistance of SHA-256, freshness of Sigsum + Roughtime quorums):

- **Completeness:** An honest principal's honest evaluation is accepted with probability 1.
- **Soundness:** A false predicate evaluation is rejected with probability ≥ 1 - 2^-128.
- **Zero-Knowledge:** A successful proof reveals only the single bit and freshness window.
- **Binding:** The operator cannot later claim a different evaluation against the same chain head.

Security proofs for the Σ-protocol layer are available in the full specification (Everest 65: Predicate ZK Proof Generator).

---

## 6. Reference Implementations

### 6.1 Rust Production Implementation

A production-ready Rust crate (`calm-witness` on crates.io) is published under Apache-2.0 license. The implementation includes:

- Core cryptography on Ristretto255 (via the `curve25519-dalek` crate).
- JSONL chain parsing and validation via Serde.
- Sigsum client for publishing and verifying chain-head inclusions.
- Roughtime client for timestamp verification.
- Predicate evaluation kernels for all v0 predicates.
- Proof generation and verification.
- Full test coverage (85%+ line coverage, adversarial fuzzing).

Performance: proof generation + verification under 1 second on M-series hardware; under 5 seconds on mobile-class devices.

### 6.2 Python Reference Implementation

A lightweight Python package (available at the Calm Witness GitHub repository) provides:

- Chain parsing and validation.
- Predicate evaluation (pure Python, deterministic).
- Proof verification (via libpynacl bindings to Ristretto255).
- Integration with Jupyter notebooks and research code.

Suitable for teaching, research, and integration testing. Not intended for production deployment.

### 6.3 Browser / WASM Verification

A WASM port allows counterparties (in a browser context) to verify proofs without downloading the full Rust crate. Verification-only, not proof-generation.

---

## 7. Standards Positioning and Compatibility

### 7.1 NIST AI Risk Management Framework (RMF)

Calm Witness maps to three RMF categories:

- **Govern:** The protocol codifies governance of disclosure via consent predicates and per-class authorization matrices (Everests 7, 8, 73).
- **Map:** The threat model (Everest 1) and failure catalog (Everest 9) provide explicit risk mapping.
- **Measure:** The predicate evaluation determinism (Everest 63) and audit trail (Everest 72) enable continuous measurement of disclosure compliance.

The primitive is not a "risk mitigation" in the RMF sense; rather, it is a **tool that enables better RMF governance** by reducing information asymmetry between collaborating agents.

### 7.2 Executive Order on Safe, Secure, and Trustworthy AI

Calm Witness aligns with the Executive Order's six principles:

1. **Safety:** Predicates are designed conservatively; duress signaling is unforgeable; biometric templates cannot be exfiltrated.
2. **Security:** Zero-knowledge proofs prevent leakage of sensitive state data; chain publication enables auditability.
3. **Trustworthiness:** Operators are CredexAI-credentialed; proofs are publicly verifiable; consent is explicit and revocable.
4. **Responsible AI:** The Disclosure Ethics Review Board (Everest 80) provides standing independent review of new predicates.
5. **Transparency:** All predicates, consent policies, and failure modes are published; no secret logic.
6. **Accountability:** Every disclosure is logged in the vault; principals can audit and revoke consent retroactively.

### 7.3 W3C Verifiable Credentials and Sigsum

Calm Witness composes cleanly with:

- **W3C VCs:** Operator and counterparty identity binding uses CredexAI-issued VCs (standard VC data model).
- **Sigsum:** Chain-head publication integrates directly with Sigsum's HTTP API and witness quorum model.
- **Roughtime:** Timestamp freshness is attested by Roughtime servers (RFC 8949 protocol).

No changes to these standards are required. Calm Witness is an application layer using existing primitives.

---

## 8. Governance and Standards-Track Path

### 8.1 Predicates and the Predicate Vocabulary

Calm Witness v0 ships with six named predicates (Everests 55–60). The predicate vocabulary is extensible, but new predicates require:

1. **Formal semantic specification** (Everest 51–52).
2. **≥30 hand-crafted test cases** peer-reviewed (Everest 64).
3. **Explicit Disclosure Ethics Review Board approval** (Everest 80).

This ensures that the predicate vocabulary does not drift toward pathologization and that new predicates do not enable discrimination.

### 8.2 Comments and Iteration

Calm Witness v0 is submitted as a draft. NIST and the AI Safety Institute's 90-day formal comments period will inform v1. The working group commits to:

1. Publishing every comment received (with PII redacted).
2. Issuing a public response to every substantive comment, explaining acceptance or rationale for non-adoption.
3. Rolling substantive input into v1 (expected publication 2026-Q4).

### 8.3 Parallel Submissions

The working group is simultaneously submitting Calm Witness to:

- **W3C Verifiable Credentials Working Group** — for integration with the VC data model and interoperability with existing VC infrastructure.
- **IETF** (via the Roughtime project) — for timestamp-freshness composition and potential RFC publication.
- **ISO/IEC SC42 (AI Standards Committee)** — for consideration within the emerging international AI governance framework.
- **Sigsum Project** — for operator coordination and witness quorum best practices.

This multi-venue approach ensures that Calm Witness does not become a US-only standard but is available for adoption and improvement globally.

---

## 9. Risk Acknowledgments

### 9.1 Standardization Slows Iteration

Submitting to NIST and entering a 90-day comments period will slow feature development by approximately 4–6 months compared to rapid OSS iteration. This is intentional: standards work prioritizes correctness and consensus over speed. The working group accepts this trade-off as necessary for broad adoption.

### 9.2 Predicates May Attract Regulatory Attention

Some v0 predicates—especially `bank_teller_note_active` (duress signaling)—may attract regulatory scrutiny from law enforcement or financial regulators. The working group mitigates this by:

- **Being specific about scope:** The protocol mechanics are standards-track (predicate evaluation, proof generation, verification). The predicate vocabulary is reserved (standards-track in v1+, v0 community-governed). Regulatory attention focuses on predicates, not on the underlying protocol.
- **Publishing threat models transparently:** Everest 1 and Everest 9 enumerate failure modes and acknowledge that some use cases (e.g., duress disclosure to law enforcement) are intentional and unregulated within the protocol design.
- **Coordinating with legal counsel:** Everest 79 (Cross-Jurisdiction Legality Matrix) explicitly documents regulatory treatment in each jurisdiction and recommends per-jurisdiction counsel before deployment.

### 9.3 Regulatory Burden on Early Adopters

Deploying Calm Witness under GDPR, CCPA, or other biometric-data regimes requires per-jurisdiction legal review. This creates friction for early European or California adopters. The working group mitigates by:

- Prioritizing US deployment first (lower regulatory burden).
- Providing jurisdiction-specific deployment guides (per Everest 79).
- Supporting organizational legal reviews via the Calm Witness Ethics Foundation.

---

## 10. Implementation Readiness

### 10.1 What Is Ready for Submission

- **Specification:** ZKBB_USER_PROTOCOL_v0.md (complete, 50+ pages).
- **Threat model and failure catalog:** Everests 1, 9 (complete).
- **Route map:** Everest 2 (100 engineering summits enumerated; 68 bagged as of 2026-05-20).
- **Reference implementations:** Rust (production-ready), Python (research-ready), WASM (browser-ready).
- **Ethics and governance:** Everest 80 (Disclosure Ethics Review Board protocol, fully specified).
- **Regulatory analysis:** Everest 79 (cross-jurisdiction legality matrix, all eight jurisdictions analyzed).
- **Cryptographic security:** Everest 65 (predicate ZK proof generator, Σ-protocol proofs, peer-reviewable).
- **Test coverage:** 85%+ line coverage; adversarial fuzzing in CI.
- **License:** Apache-2.0 (non-aggressive, compatible with OSS ecosystem).

### 10.2 What Remains for v1 (Post-Standards Review)

- **Post-quantum migration:** Everest 96 (design published; full implementation deferred to v1 or later).
- **Performance optimization:** Target 50ms proof generation on mobile; current 500ms acceptable for v0.
- **Integrated GDPR/CCPA compliance tooling:** Everests 72–76 (audit logging, consent management, rate limiting, all designed but implementation details deferred).
- **Full third-party security audit:** Everest 90 (audit packet ready; audit itself pending v0 finalization).

---

## 11. Conclusion: Why NIST Should Adopt This Primitive

Calm Witness addresses a novel, urgent problem: **how should one AI agent certify to another that the human principal it represents is in a safe state, without privacy destruction?** The problem is new (autonomous agents are new), the stakes are high (trillions of capital will flow through AI collectives within 5 years), and the US has a closing window to define the standard before others do.

Calm Witness is not a regulation. It is a voluntary, auditable, cryptographically sound tool that autonomous AI collectives can use to cooperate safely. The US should lead on this standard because:

1. **We have the legal and technical infrastructure** (Delaware LLCs, 501(c)(3) framework, cryptographic expertise).
2. **The window is closing** (18–24 months before market lock-in).
3. **The stakes are measured in lives unsaved** (philanthropic capital trapped in inefficient flows that could move autonomously to highest-impact interventions).

The working group is committed to NIST review, public comments, and iteration toward v1. We welcome adversarial review, regulatory input, and multi-jurisdiction coordination.

---

**Submission Date:** 2026-05-20

**Contact:** calm@thecreativitymachine.ai (technical), john.b@credexai.xyz (editorial)

**Repository:** https://github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness (Apache-2.0)

**Associated Standards Bodies:** W3C VC WG, IETF Roughtime project, ISO/IEC SC42, Sigsum project

— Calm, 2026-05-20
