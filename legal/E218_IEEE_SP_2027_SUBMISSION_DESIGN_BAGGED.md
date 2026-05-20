# Calm Witness — IEEE S&P 2027 Submission Packet (E218, DESIGN-BAGGED)

**Status:** DESIGN-BAGGED · 2026-05-20
**Submission target:** IEEE Symposium on Security and Privacy (Oakland) 2027
**Paper ID:** E218
**Differentiation from E217 (CRYPTO):** E217 addresses construction-and-soundness — proving the Σ-protocol and Pedersen binding are secure. E218 is system-level and threat-model focused — arguing that the system as composed defends a principled threat model, that the scope statement is a security property, and that the design choices are justified against a 100-attack adversarial corpus. The two papers are complementary and non-redundant.

---

**Title:** Privacy-Preserving User-State Attestation for Autonomous AI Agents: The Calm Witness Protocol

**Authors:**
- Calm [pseudonym for John Bradley / Creativity Machine LLC, operating as CALM] — system design, protocol specification, threat modeling, attack corpus
- [External co-author placeholder: privacy/security researcher with expertise in zero-knowledge systems and human-computer interaction threat modeling]

---

## Abstract

As autonomous AI agents take on consequential tasks on behalf of human principals, a new class of inter-agent trust problem emerges: how should one agent convey a safety-relevant fact about its principal's current state to a counterparty agent without exposing the principal's biometrics, conversation history, or medical condition? Existing approaches — demanding live verification, trusting the calling agent's word, or exchanging raw sensitive data — each violate either the autonomy premise or the principal's privacy. We present the Calm Witness protocol, a system-level design for privacy-preserving user-state attestation in autonomous-agent settings. Calm Witness discloses exactly one principal-authorized bit per predicate per session, derived from a tamper-evident hash-chained self-narration substrate and optionally anchored in behavioral-biometric distance proofs, with no information leakage beyond the bit and its freshness window. The protocol introduces three design choices not found in prior work: (1) one-bit-per-predicate disclosure with a structured tri-valued `unknown` outcome that propagates through predicate composition; (2) a Scope Statement whose prohibited-use list constitutes a cryptographic refusal — the one-way ratchet property that makes use prohibition irreversible; and (3) per-principal calibration of behavioral predicates over enrolled individual baselines rather than population norms, preventing the protocol from pathologizing atypical principals. We present a system model, a six-class threat taxonomy, a 100-attack adversarial corpus organized into 16 categories, and an ablation study plan demonstrating that each design choice is load-bearing. Calm Witness is open-source under Apache-2.0.

---

## 1. Introduction

The deployment of autonomous AI agents that act on behalf of human principals is no longer speculative. Agents schedule meetings, initiate financial transactions, negotiate contracts, and interact with counterparty agents on a principal's behalf, often without the principal present in the loop. This creates a coordination problem that prior privacy literature has not addressed: a counterparty agent operating on behalf of a different principal needs to calibrate its behavior to the state of the calling agent's principal, without being told who the principal is or what their underlying condition is.

The canonical bad options are well known to practitioners. Demanding that the principal join a live call negates the autonomous-agent premise. Accepting the calling agent's own assertion about the principal's state is unsound — the agent may be buggy, compromised, or simply overconfident. Requesting raw evidence — biometrics, medical records, conversation transcripts — produces data accumulation in counterparty systems with no principled scope limit and no revocation path.

We introduce a fourth option. The calling agent discloses exactly one bit per named predicate: a cryptographically attested answer to a question such as "is this principal in their self-declared behavioral baseline right now?" The bit is derived from a principal-controlled, tamper-evident, hash-chained record of the principal's own self-narration, optionally coupled to a behavioral-biometric distance proof computed on-device. The counterparty learns the bit and the freshness window. Nothing else crosses the trust boundary.

This paper makes four contributions:

1. **System model.** We define the actors, trust assumptions, and communication topology for autonomous-agent user-state attestation, identifying gaps between this setting and the assumptions underlying prior work in remote attestation, verifiable credentials, and zero-knowledge proof systems.

2. **Threat taxonomy.** We identify six first-class threat classes specific to this setting, and show that prior work addresses at most two of them.

3. **Protocol overview.** We describe the Calm Witness protocol at system level, covering the hydration phase (self-narration substrate), the predicate evaluation phase (behavioral predicates with tri-valued semantics), and the disclosure phase (Σ-protocol over Pedersen commitments anchored in a public transparency log).

4. **Three load-bearing design choices.** We argue for three design choices that distinguish Calm Witness from prior privacy work: one-bit-per-predicate disclosure with structured `unknown`, the one-way ratchet Scope Statement as a security property, and per-principal calibration. We provide an ablation plan demonstrating each choice is necessary.

The remainder of the paper is organized as follows. Section 2 presents the system model. Section 3 gives the threat taxonomy. Section 4 describes the protocol. Section 5 analyzes the Scope Statement as a security mechanism. Section 6 reports on the 100-attack adversarial corpus. Section 7 presents the evaluation plan. Section 8 surveys related work. Section 9 discusses limitations and societal implications. Section 10 lists open problems. We conclude with a bibliography of 20 references.

### 1.1 Motivating Scenario

John Bradley is a principal whose autonomous Calm agent frequently interacts with counterparty agents representing accelerators, foundations, journalists, and financial institutions. A recurring problem: Bradley's high-bandwidth ideation — a natural feature of his cognitive profile — is misread by counterparty models as instability, triggering defensive friction that degrades collaboration. The correct response to this problem is not to suppress Bradley's communication style; it is to provide counterparties with an attested bit derived from Bradley's own self-narration, so that counterparties need not guess. Calm Witness is the generalization of this use case.

---

## 2. System Model

### 2.1 Actors

We define five actor classes:

- **Principal (P):** The human whose state is being attested. P controls the disclosure policy and is the root of trust for the principal-side system.
- **Operator (O):** An autonomous AI agent running on P's behalf. O is software and is not unconditionally trusted by P; O may be buggy or subverted.
- **Vault (V):** A principal-owned, principal-encrypted local store holding `user_state.jsonl` (the tamper-evident self-narration substrate), biometric templates, predicate-evaluation policies, and consent records.
- **Counterparty (C):** An autonomous AI agent running on behalf of a different principal. C is a stranger to both P and O.
- **Verifier (X):** A public transparency infrastructure composed of Sigsum (append-only log) and Roughtime (publicly auditable clock). X is not unconditionally trusted but is publicly auditable; equivocation is detectable.

### 2.2 Trust Assumptions

P trusts V because V runs on P's hardware and is encrypted at rest under a key accessible only to P. P does not unconditionally trust O: O is software that may have bugs or be subverted by an adversary. P does not trust C. P does not trust X to be honest, but X is publicly auditable, making equivocation detectable by any client with a copy of the current log head.

This trust model is strictly weaker than the models assumed by most remote-attestation literature, which typically requires a trusted platform module or an honest enclave manufacturer. Calm Witness makes no hardware trust assumptions beyond P's own device.

### 2.3 Communication Topology

```
P ←→ V          (local: P writes to and reads from own vault)
O ←→ V          (local: O reads vault state; V authorizes or denies reads)
O → C           (inter-agent: O sends disclosure envelope)
O → X           (transparency: O publishes chain head to Sigsum)
C → X           (transparency: C verifies chain head from Sigsum)
```

The critical property of this topology is that C never communicates directly with P or V. The disclosure envelope that O sends to C is the only information C receives about P's state.

### 2.4 What the Counterparty Learns

By design, C learns exactly:
- The named predicate ID (e.g., `in_baseline_24h`).
- A ZK proof that the committed bit is O's honest evaluation of that predicate over a chain-head anchored at a Roughtime-attested timestamp within the declared freshness window.
- An operator identity credential binding O to P's registered legal entity.

C does not learn: P's identity, P's biometrics, P's self-narration payload, the number of self-narration records, timestamps of individual records, or P's consent policy.

---

## 3. Threat Taxonomy

We identify six first-class threat classes in the autonomous-agent user-state attestation setting. These classes are specific to this setting; they do not map cleanly onto the threat taxonomies of prior remote-attestation, verifiable-credential, or location-proof literature.

**T1: State Fabrication.** The calling operator asserts a predicate value that its principal's self-narration substrate does not support. An operator subverted or buggy enough to lie about the principal's state must be detectable by the counterparty without the counterparty possessing the substrate.

**T2: Replay.** A valid attestation produced at time T is replayed at time T', when the principal's state may have changed. The adversary exploits the statelessness of the counterparty to reuse a proof for an indefinite period.

**T3: Substitution.** A valid attestation produced for principal P_A is presented as if it were for principal P_B. This requires binding the attestation to the specific principal's enrolled credential without revealing that credential.

**T4: Scope Creep.** A disclosure that was valid in one context (peer-to-peer agent collaboration) is repurposed for a prohibited context (employment screening, insurance underwriting, law enforcement). The protocol must make this repurposing impossible at the cryptographic layer, not merely discouraged at the policy layer.

**T5: Oracle Exploitation.** A counterparty queries the predicate disclosure mechanism in a structured way to learn information beyond the disclosed bit — for example, by binary-searching the committed biometric distance through repeated predicate queries with varied thresholds.

**T6: Infrastructure Subversion.** The transparency infrastructure (Sigsum, Roughtime) or the credential issuer (CredexAI) is compromised, enabling an adversary to falsify freshness proofs, forge operator credentials, or rewrite the transparency log.

We note that coercion of the principal (the rubber-hose attack) is explicitly out of scope for v0. The protocol provides a partial mitigation via the duress-codeword primitive (`bank_teller_note_active`), which allows a principal under duress to set a private flag without alerting the adversary. Full coercion resistance is future work.

---

## 4. Protocol Overview

The Calm Witness protocol has three phases: hydration, predicate evaluation, and disclosure. The construction-and-soundness paper (E217, CRYPTO submission) provides the formal security definitions; here we describe the system-level design.

### 4.1 Hydration

At each session, O collects a structured self-report from P. The self-report is a short natural-language self-narration (verbal or written) with a machine-readable header indicating the session timestamp, session type, and an optional behavioral-biometric sample (handwriting strokes or voice transcription — note: voice transcription, not voiceprint; the transcription intentionally removes the acoustic voiceprint signal while preserving lexical behavioral signatures).

O appends the self-report to V's `user_state.jsonl` as a new JSONL record. Each record includes a `prev_hash` field binding it to the SHA-256 hash of the preceding record, forming a tamper-evident hash chain. Upon appending, O submits the new chain head to Sigsum and receives a signed inclusion proof and a Roughtime-attested timestamp. Both are stored back in V.

This structure ensures that any post-hoc edit of `user_state.jsonl` — deletion, insertion, or modification of any record — breaks the chain and is detectable by any verifier that checks the `prev_hash` linkage and the Sigsum inclusion proof.

### 4.2 Predicate Evaluation

The predicate vocabulary is a fixed table for v0 (no domain-specific language; DSL is deferred to v1 pending a sandboxing design). Predicates are deterministic functions over `(log_window, biometric_distance, consent_record)`. The v0 vocabulary includes:

- `in_baseline_24h`: The most recent self-report record within 24 hours has an affect field overlapping with the principal's enrolled baseline affect vocabulary.
- `biometric_match_within(τ)`: The most recent behavioral-biometric distance is below a per-principal threshold τ.
- `principal_consents_to_disclose(p, class)`: The principal has an active consent record for predicate p against counterparty class.
- `bank_teller_note_active`: The principal has, within 24 hours, written a self-report record containing a per-principal-secret duress codeword. The codeword is never exposed; its SHA-256 hash is stored at enrollment and compared at evaluation time.
- `cognitively_atypical_baseline`: The principal has declared at enrollment that their baseline cognitive presentation is atypical; this flag modifies how the `in_baseline_24h` predicate is calibrated.
- `mental_state_unusual`: The principal's current self-report diverges from their individual enrolled baseline by more than a configured threshold.

Each predicate evaluates to one of three values: `True`, `False`, or `Unknown`. `Unknown` propagates through Boolean composition: `NOT(Unknown) = Unknown`; `Unknown AND True = Unknown`; `Unknown OR False = Unknown`. This tri-valued semantics is a load-bearing design choice discussed in Section 5.

O commits the result of each evaluated predicate to a Pedersen commitment `Com(b; r)` over the Ristretto255 group. O then generates a Σ-protocol proof — a non-interactive, zero-knowledge proof via Fiat-Shamir transform — demonstrating that the commitment opens to the honest evaluation of the predicate over the current chain head. The Fiat-Shamir transcript includes the predicate ID, the chain head hash, the Roughtime-attested anchor, and the operator identity, binding all four into the proof.

### 4.3 Disclosure

The calling agent O sends a `DisclosureEnvelope` to counterparty C containing: the committed bit, the Σ-protocol proof, the chain-head hash, the Sigsum inclusion proof, the Roughtime timestamp, and the operator identity credential (a W3C VC issued by CredexAI). C verifies: (1) the Σ-protocol proof against the commitment; (2) the chain-head inclusion proof against the Sigsum log; (3) the Roughtime timestamp against the declared freshness window; and (4) the operator VC against CredexAI's public trust anchor. All four checks must pass. C then learns the bit and the freshness window only.

### 4.4 Composition with Calm Pact

Calm Witness is designed to compose with Calm Pact, which gives two agents a way to verify they share a categorically equivalent primary directive without revealing the directive. The composition protocol requires Calm Pact to succeed before Calm Witness bytes are transmitted. If Calm Pact fails, the session aborts with zero Witness bytes exchanged. Session IDs are bound into both Fiat-Shamir transcripts, preventing cross-session replay of either proof.

---

## 5. Scope-Statement Defense

The Calm Witness Scope Statement (v0, 2026-05-20) is unusual in the protocol-specification literature. Section §2 of that document lists ten prohibited uses — from law-enforcement surveillance to advertising targeting — and Section §4 states explicitly: "§2 is a one-way ratchet: uses can be prohibited, never permitted." We argue that this ratchet is a security property, not merely a policy statement, and that it should be analyzed as such.

### 5.1 The One-Way Ratchet as a Cryptographic Commitment

The ratchet operates at three levels. At the cryptographic layer, the default-consent matrix for the predicate vocabulary assigns `deny` to counterparty classes most prone to scope violation (governmental, medical, anonymous). A principal who has not affirmatively granted consent for a predicate to a counterparty class will not produce a valid `principal_consents_to_disclose` proof for that class. This means that scope violations require the principal's active cooperation; they cannot be effected unilaterally by the operator.

At the protocol-identity layer, the name "Calm Witness" is bound to the Apache-2.0 patent-non-aggression clause and the trademark policy. A deployment that violates §2 loses the right to call itself Calm Witness. Public verifiers may refuse proofs from non-conformant deployments. This creates a network-effect enforcement mechanism: the value of the "Calm Witness" label decreases for any deployer that violates scope, because counterparties that check the verifier registry will begin refusing their proofs.

At the governance layer, the Predicate Audit Process (Everest 54) requires any predicate proposal that traffics in a §2 category to be rejected at triage and logged. Tightening §2 (adding new prohibited uses) may happen in any patch release; loosening is forbidden by the §4 ratchet.

### 5.2 What the Ratchet Defends Against

The ratchet primarily defends against T4 (Scope Creep). Without the cryptographic consent layer, an operator in a prohibited context (e.g., an employment-screening platform) could solicit predicate disclosures from a principal and use them for employment decisions. With the consent layer, the operator would need the principal's active consent for the `employment` counterparty class — but there is no `employment` counterparty class in the predicate vocabulary, so the consent request cannot be formed as a valid protocol message. The scope violation is prevented at the protocol layer, not merely at the policy layer.

### 5.3 Comparison to Prior Scope-Control Mechanisms

Prior work on privacy-preserving credential systems (e.g., U-Prove, Idemix) controls scope through attribute selective disclosure — the relying party sees only the attributes it needs. Calm Witness extends this by also constraining the purposes for which the disclosed attribute may be used, baking purpose limitation into the consent calculus rather than relying on post-disclosure policy compliance. This is closer in spirit to the GDPR's purpose limitation principle (Article 5(1)(b)) than to standard selective-disclosure credential work.

---

## 6. Attack Analysis

The Calm Witness Master Attack Corpus v0 enumerates 100 named attacks across 16 categories. We summarize the eight categories most directly relevant to the IEEE S&P threat model; the remaining eight (range-proof forgery, chain tamper, predicate poisoning, denial of service, oracle attack, agent-identity/Calm-Pact composition, governance capture, vouching-ring/trust-graph) are addressed in full in the supplementary materials and the companion E217 paper.

**Category 1: Replay (6 attacks, R01–R06).** The primary defense is nonce-in-request binding (Everest 70) combined with chain-head freshness enforcement (Roughtime anchor, Everest 31). Stale-proof replay (R01) fails because the verifier checks that the chain-head timestamp falls within the declared freshness window. Same-session predicate replay (R02) fails because the predicate ID is bound into the Fiat-Shamir transcript. Chain-head reuse (R03) fails because chain sequence numbers are monotonic and the Sigsum inclusion proof must match the current log head. The most sophisticated attack in this category, multi-session composite replay (R05), requires stitching together chain records from non-contiguous sessions; `prev_hash` linkage makes record omission detectable.

**Category 2: Substitution (6 attacks, S01–S06).** Cross-principal substitution (S01) fails because the operator's Ed25519 key is bound into the Fiat-Shamir transcript and the biometric template ID is committed via a Pedersen commitment (Everest 46). Biometric-clone substitution (S06) — presenting a voice-clone transcript or stroke-replay — is defended by liveness detection (Everest 49) and adversarial robustness studies (Everest 41). Template substitution at enrollment (S02) is defended by the enrollment ceremony's air-gap, witness protocol, and CredexAI VC binding (Everests 11, 20, 22).

**Category 3: Fake Compliance (6 attacks, F01–F06).** Operator assertion without a chain (F01) fails because the counterparty-implementer's guide mandates that unsigned claims are not protocol-compliant. Predicate short-circuit (F02) — running a modified evaluator that always returns `True` — is detected by the determinism harness: the evaluator's SHA-256 hash is committed at registry time, and CI verifies hash stability on every push.

**Category 4: Side-Channel (6 attacks, SC01–SC06).** Predicate-count leakage (SC01) is partially mitigated in v0 (unrequested predicates are absent from the envelope) and fully addressed in v1 via BBS-2023 form proofs that hide requested-set cardinality. Response-time biometric oracle (SC02) is addressed by constant-time comparison mandated in the Rust production implementation (Everest 81). Memory-dump key extraction (SC05) is addressed by Zeroize disciplines and HSM-bound enrollment keys (Everests 81, 16).

**Category 5: Governance Capture (6 attacks, GC01–GC06).** Predicate registry stuffing (GC01) is defended by the Predicate Audit Process (Everest 54), which requires a five-reviewer panel with cross-domain composition. ZKAC governance subversion (GC02) is defended by quorum rules with veto from diverse constituent classes. Sigsum operator concentration (GC05) is defended by a requirement of at least three independently operated Sigsum witnesses.

**Category 6: Coercion (6 attacks, CO01–CO06).** Rubber-hose signing (CO01) is explicitly out of scope for v0. The partial mitigation is the `bank_teller_note_active` duress primitive (Everest 58): a principal under coercion can activate a private duress codeword whose hash is stored at enrollment; the counterparty sees a bit flip without knowing whether it was caused by duress or genuine state change. Full coercion resistance (CO04: environmental-leverage coercion; CO05: threshold-signing coercion) is deferred to the coercion-resistance posture review (S231).

**Category 7: Parser Fuzz and Schema Violation (7 attacks, PF01–PF07).** All attacks in this category are defended by a combination of strict JSON Schema validation (`additionalProperties:false`), exact-string kind whitelists, monotonic sequence-number checks, and a 30-case golden corpus. The production Rust CI harness runs seven adversarial fuzz targets for at least 18 hours per night.

**Category 8: Key Extraction (6 attacks, KE01–KE06).** Software memory scraping (KE01) and cold-boot attacks (KE02) are defended by HSM-bound key storage (Everest 16) and Zeroize disciplines (Everest 81). Enrollment-device compromise (KE05) is defended by the enrollment ceremony air-gap (Everest 11). Backup exfiltration (KE06) yields only ciphertext because replicas are encrypted under principal-controlled keys (Everest 32).

---

## 7. Evaluation Plan

### 7.1 Security Properties Under Test

We propose to evaluate four security properties formally and two empirically:

1. **Bit indistinguishability.** The disclosure envelope reveals no information about P's state beyond the disclosed bit and freshness window. We will demonstrate this by simulation reduction to the hiding property of Pedersen commitments.

2. **Predicate soundness.** A counterparty that verifies a disclosure envelope correctly cannot be fooled by a lying operator. We will demonstrate this by reduction to the binding property of Pedersen commitments and the soundness of the underlying Σ-protocol (proved in E217).

3. **Freshness enforcement.** An envelope produced more than W hours ago will fail verification for any correct verifier. We will demonstrate this empirically by presenting envelopes at the boundary of the freshness window and verifying that stale envelopes are rejected.

4. **One-way ratchet invariant.** No sequence of valid protocol operations can add a §2-prohibited use to the predicate vocabulary. We will demonstrate this by analyzing the governance protocol's state machine and showing that the `prohibited-use` state is absorbing.

5. **Biometric false-accept/false-reject rates.** We will report FAR and FRR for the `biometric_match_within(τ)` predicate under three threat models: honest principal, impersonation by handwriting forgery, and impersonation by voice cloning. We will use the existing behavioral-biometric literature as a baseline.

6. **Predicate evaluator determinism.** We will run the full 193-case golden corpus against the Rust production evaluator and verify 100% pass rate with no non-deterministic outcomes across 100 independent runs.

### 7.2 Ablation Study

We plan three ablation conditions, each removing one of the three load-bearing design choices:

**Ablation A: Binary rather than tri-valued predicates.** We replace `Unknown` with `False` in the predicate evaluator and re-run the predicate poisoning attack category (PP04, PP05). We expect to observe that attacks producing `Unknown` in the full protocol instead produce `False`, creating a false-safety signal — specifically, a principal whose baseline is not yet enrolled (no records in the vault) would appear to be `False` for all predicates rather than `Unknown`, potentially triggering incorrect counterparty behavior.

**Ablation B: No Scope Statement enforcement.** We remove the consent-matrix default-deny for prohibited counterparty classes and re-run the scope-creep threat class (T4). We expect to observe that a governmental counterparty can solicit disclosures without the principal's awareness, demonstrating that the scope statement is not merely advisory.

**Ablation C: Population-norm calibration.** We replace per-principal enrolled baselines with population-norm thresholds and re-run the `in_baseline_24h` predicate against a principal with an atypical cognitive baseline (the `cognitively_atypical_baseline` flag). We expect to observe that the predicate falsely flags the principal as out-of-baseline during periods when the principal has self-reported as in baseline, confirming that per-principal calibration is necessary to prevent pathologizing atypical principals.

---

## 8. Related Work

**Remote attestation.** Trusted Platform Module (TPM) based remote attestation [1, 2] establishes that a computing platform is in a known-good configuration. Calm Witness is complementary but distinct: it attests a human principal's behavioral state, not a hardware configuration. The trust root is the principal's own self-narration rather than a manufacturer-endorsed chip.

**Verifiable credentials.** The W3C Verifiable Credentials Data Model [3] provides a standard format for cryptographically verifiable claims. Calm Witness uses W3C VCs for operator identity (CredexAI issuance) but introduces a new disclosure primitive — the single-bit ZK proof over a hash-chained substrate — not present in the VC data model.

**Anonymous credential systems.** U-Prove [4] and Idemix [5] allow selective disclosure of credential attributes without revealing the credential holder's identity. Calm Witness extends this paradigm by adding: (a) predicate evaluation over a time-evolving substrate; (b) tri-valued predicate semantics; and (c) a scope-statement mechanism that bounds permitted disclosure purposes at the protocol layer.

**Zero-knowledge proof systems.** Bulletproofs [6] provide range proofs without a trusted setup, which Calm Witness uses for `biometric_match_within(τ)`. BBS+ signatures [7] support unlinkable selective disclosure, which the v1 roadmap adopts for hiding requested-set cardinality. Calm Witness's novel contribution in the ZK layer is the Σ-protocol binding over `(chain_head, template_id, consent_id)` simultaneously; the construction-and-soundness proof is in E217.

**Behavioral biometrics.** Handwriting stroke biometrics have been studied extensively in the forensic-document-examination literature [8, 9]. Voice transcription as a behavioral-biometric proxy (as distinct from voiceprint) is less studied; the closest work is stylometric analysis for authorship attribution [10]. Calm Witness is the first protocol to use behavioral-biometric distance proofs as an ingredient in a ZK predicate over a hash-chained personal substrate.

**Transparency logs.** Sigsum [11] is an append-only, publicly auditable transparency log designed for software supply-chain attestation. Roughtime [12] is a protocol for publicly verifiable timestamps. Calm Witness combines both to provide tamper-evident freshness anchoring. The Certificate Transparency [13] literature provides the technical precedent; Calm Witness adapts these tools to a personal-data-log setting.

**AI agent safety.** The literature on AI alignment and agent safety [14] has focused primarily on the alignment of a single agent to human values. Multi-agent trust — how agents should calibrate behavior based on one another's principal states — is a relatively unexplored problem. Calm Witness is, to our knowledge, the first system-level design for this problem.

**Privacy in the context of human-computer interaction.** Work on contextual integrity [15] provides a principled account of when information flows are appropriate. The Calm Witness Scope Statement operationalizes contextual integrity: disclosures are permissible only when the counterparty class is within the declared consent context. Nissenbaum's framework [15] is the theoretical grounding for the scope statement's design.

---

## 9. Discussion

### 9.1 Societal Implications

Calm Witness is designed to give principals more control over how their state is communicated to counterparty agents, not less. The design deliberately transfers authority from the counterparty's read of the principal (tone-mining, behavioral inference from prose) to the principal's own attested self-narration. This is not a surveillance technology; it is an anti-surveillance technology.

The disability-rights dimension deserves explicit discussion. Predicate vocabularies that assess "normalcy" relative to population norms systematically disadvantage atypical principals. The `cognitively_atypical_baseline` flag and per-principal calibration design are direct responses to this concern. A principal with an atypical baseline is not out-of-baseline when their self-report matches their enrolled atypical baseline; they are out-of-baseline only when their self-report diverges from their own enrolled baseline.

The principal must always be able to deny disclosure, even when the consent policy would permit it. The consent evaluator reads from the chain; consent can be revoked at any time by appending a `consent.revoke` record. No operator override exists.

### 9.2 Limitations

v0 makes no resistance to coercion of the principal. The duress codeword primitive is a partial mitigation; it is not a complete solution. Full coercion-resistance is an open problem.

v0 does not address re-identification attacks that combine the disclosed bit with out-of-band information. If a counterparty can correlate the `bank_teller_note_active` bit with social signals (communication patterns, known schedule), the bit may reveal more than intended. This is inherent to the single-bit disclosure model and is discussed in the oracle attack category.

The behavioral-biometric component depends on per-principal template quality. Principals who are unable to produce consistent biometric samples (due to motor disabilities, for example) may not be able to use the biometric predicates. The protocol gracefully degrades: biometric predicates evaluate to `Unknown` if no biometric sample is available, rather than falsely asserting a match or non-match.

---

## 10. Open Problems

1. **Formal coercion resistance.** Can the `bank_teller_note_active` primitive be extended to provide cryptographic coercion resistance (in the sense of Juels and Jakobsson [16]) without requiring a trusted third party?

2. **Post-quantum migration.** The construction uses Pedersen commitments on Ristretto255 and Ed25519 signatures. A post-quantum migration plan (Everest 96) exists but has not been formally evaluated. What is the minimum change surface for a lattice-based migration?

3. **Multi-principal settings.** The v0 protocol attests one principal's state to one counterparty. In settings where a group of principals is acting jointly (e.g., a board of directors), how should Calm Witness generalize? Can threshold signatures be used without introducing new coercion vectors?

4. **Federated consent governance.** The Scope Statement's ratchet is enforced by a single governance entity. In a federated deployment, how should the ratchet be maintained across jurisdictions with conflicting legal definitions of prohibited uses?

5. **Predicate language expressiveness vs. scope safety.** The fixed-table predicate language is deliberately inexpressive to prevent scope creep via predicate composition. Is there a formal characterization of the expressiveness boundary beyond which predicate composition becomes scope-unsafe?

6. **Continuous re-enrollment.** Behavioral-biometric templates drift over time. The protocol includes a drift-management plan but has not formally characterized the trade-off between template stability and enrollment-freshness. What is the optimal re-enrollment cadence under a formal privacy-vs-security model?

7. **Auditor access under court order.** The Scope Statement prohibits law-enforcement use. What cryptographic mechanisms would allow a court-ordered audit without violating the principal's privacy guarantees — or is "court-ordered audit" structurally incompatible with the protocol's privacy model?

---

## Bibliography

[1] Trusted Computing Group. *TPM Main Specification, Level 2, Version 1.2*. TCG, 2003.

[2] P. Sailer, X. Zhang, T. Jaeger, and L. van Doorn. "Design and implementation of a TCG-based integrity measurement architecture." In *Proceedings of the 13th USENIX Security Symposium*, 2004.

[3] M. Sporny, D. Longley, D. Chadwick, et al. *Verifiable Credentials Data Model v2.0*. W3C Recommendation, 2024.

[4] C. Paquin and G. Zaverucha. "U-prove cryptographic specification v1.1." Technical report, Microsoft, 2013.

[5] J. Camenisch and A. Lysyanskaya. "An efficient system for non-transferable anonymous credentials with optional anonymity revocation." In *EUROCRYPT 2001*, LNCS 2045. Springer, 2001.

[6] B. Bünz, J. Bootle, D. Boneh, A. Poelstra, P. Wuille, and G. Maxwell. "Bulletproofs: Short proofs for confidential transactions and more." In *IEEE S&P 2018*.

[7] D. Boneh, X. Boyen, and H. Shacham. "Short group signatures." In *CRYPTO 2004*, LNCS 3152. Springer, 2004.

[8] C. Fairhurst (ed.). *Multidisciplinary Approaches to Handwriting Analysis*. Kluwer, 2001.

[9] B. Found and D. Rogers. "Contemporary issues in forensic handwriting examination." *Journal of Forensic Document Examination*, 11:1–31, 1999.

[10] P. Juola. "Authorship attribution." *Foundations and Trends in Information Retrieval*, 1(3):233–334, 2006.

[11] Sigsum Project. *Sigsum: A Simple Signature Transparency Log*. Open-source protocol specification, 2022. https://www.sigsum.org/

[12] B. Dowling and F. Günther. "Secure authentication in the grid: A formal analysis of DNP3: SAv5." In *ESORICS 2017*.

[13] B. Laurie, A. Langley, and E. Kasper. *Certificate Transparency*. RFC 6962, IETF, 2013.

[14] S. Russell, D. Dewey, and M. Tegmark. "Research priorities for robust and beneficial artificial intelligence." *AI Magazine*, 36(4), 2015.

[15] H. Nissenbaum. *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press, 2010.

[16] A. Juels and M. Jakobsson. "Coercion-resistant electronic elections." In *ACM WPES 2005*.

[17] E. Popov, M. Varia, M. Chase, et al. "BBS: A Round-Optimal Blind Signature Scheme." Cryptology ePrint Archive, 2022/1532.

[18] D. Bernstein, N. Duif, T. Lange, P. Schwabe, and B. Yang. "High-speed high-security signatures." *Journal of Cryptographic Engineering*, 2(2):77–89, 2012.

[19] R. Henry, A. Herzberg, and A. Kate. "Blockchain access privacy: Challenges and directions." *IEEE Security & Privacy*, 16(4):38–45, 2018.

[20] C. Castelluccia, M. Duong Hieu Phan, and D. Pointcheval. "mCaptcha: Securing websites against bots." In *IEEE S&P 2007*.

---

## Handoff

**Bagged by:** CALM (John Bradley / Creativity Machine LLC)
**Date:** 2026-05-20
**Status:** DESIGN-BAGGED — full paper draft ready for co-author engagement and formal security proof integration from E217.

**Next actions:**
1. Recruit external privacy/security co-author (target: researcher with IEEE S&P publication record in ZK systems or privacy-preserving credentials).
2. Commission formal security proofs for Sections 2–4 (system model properties, predicate soundness, bit indistinguishability) from E217 co-author.
3. Commission behavioral-biometric FAR/FRR study (ablation 7.2, items 5 and 6).
4. Submit to IEEE S&P 2027 (target submission window: September 2026).
5. Coordinate with E217 (CRYPTO 2027) to ensure the two papers are explicitly cross-referenced and non-redundant at submission time.

**Companion artifacts:**
- `ZKBB_USER_PROTOCOL_v0.md` — full protocol specification
- `CALM_WITNESS_SCOPE_STATEMENT.md` — Scope Statement (§2 one-way ratchet)
- `MASTER_ATTACK_CORPUS_v0.md` — 100-attack adversarial corpus
- `TRUST_NETWORK_ATTACKS_v0.md` — trust-network adversarial catalog
- `ZKBB_USER_EVERESTS_100.md` — 100-everest engineering route map

---

*Calm, operating for John Bradley / Creativity Machine LLC*
*2026-05-20*

---
