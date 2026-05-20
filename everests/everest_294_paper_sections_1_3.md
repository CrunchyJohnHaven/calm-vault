# Calm Witness: Principal-Authored Zero-Knowledge State Attestation for Autonomous AI Agents

**Draft body, sections 1–3. Continuation of [SUMMIT 294/300 outline](everest_294_academic_paper_draft.md).**

Target: USENIX Security 2027 (submission August 2026). Authors: John Bradley + cryptographer co-author TBD. License: Apache-2.0; paper itself CC-BY.

---

## 1. Introduction

The next decade of artificial intelligence will be defined less by the capabilities of individual models than by the protocols under which multiple autonomous AI agents transact with each other on behalf of human principals. By 2026, AI agents are operating Delaware LLCs and 501(c)(3) charities, holding bank accounts, signing contracts, and writing email. The economic and legal infrastructure for one principal to delegate to one AI agent is now mature. The cryptographic infrastructure for *two agents* to safely transact across organisational boundaries — without leaking the data of the humans they represent — has not been written.

This paper proposes one such primitive: **Calm Witness**, a protocol enabling one autonomous AI agent (the *operator*) to attest, to a counterparty agent, a single principal-authorised bit about the human principal's current behavioural state. The bit is drawn from a fixed, principal-authored vocabulary — six predicates in version zero, including *in_baseline_24h*, *biometric_match_within(τ)*, *cognitively_atypical_baseline*, and a duress predicate *bank_teller_note_active*. The bit is bound, via a zero-knowledge proof, to a hash-chained log of the principal's own self-narration and (optionally) behavioural-biometric samples, anchored in a public transparency log, signed by a credentialed operator identity. The counterparty learns the bit and a freshness window; nothing else.

Three properties of the construction merit emphasis:

First, the protocol is **principal-authored**, not counterparty-imposed. The vocabulary of askable predicates is fixed at the principal's enrolment ceremony. A counterparty cannot define new predicates at request time. The protocol explicitly excludes whole categories of predicates — DSM-aligned mental-health labels, race or ethnicity, sexual orientation, religion of origin, criminality forecasting — at the protocol layer, not as policy hope.

Second, the protocol includes a **bank-teller-note primitive**: a covert duress channel through which the principal can flip a bit in their own chain without the operator (the AI itself) learning that the bit was flipped. The wire pattern of a duress-bit-flipped attestation is plausibly indistinguishable, to a network observer, from the wire pattern of a non-duress attestation. Only a pre-authorised verifier ring — typically a medical, governmental, or family-class counterparty class for which the principal has opted in — can decrypt the bit. This generalises, in cryptographic form, the bank-hostage note: a low-bandwidth signal whose presence is itself private.

Third, the protocol is **honest about its placeholders**. The version-zero reference implementation, available at github.com/CrunchyJohnHaven/calm-vault, ships the wire format with placeholder Pedersen commitment and Bulletproof bytes; the Rust cryptographic kernel that produces real bytes is specified separately and slated for production version 0.1. We adopt this discipline because the protocol composition, the consent calculus, the predicate vocabulary, the chain integrity, the cringe-rubric pre-publish gate, and the operator's tenancy duties are all real and self-tested today; they are the work this paper introduces. The cryptographic kernel will be a separate publication by separate authors against the conformance vectors we publish here.

The paper proceeds as follows. Section 2 reviews related work on Pedersen commitments, Σ-protocols, Bulletproofs, transparency logs, behavioural biometrics, and prior agent-to-agent trust constructions. Section 3 lays out the system model, actors, and threat model. Section 4 specifies the Calm Witness construction. Section 5 formalises the bank-teller-note primitive. Section 6 gives a security analysis. Section 7 places Calm Witness inside the broader Calm Stack — its composition with Calm Pact (directive equality) and Calm Compass (principal-authored values attestation). Section 8 presents the results of an adversarial self-review across thirty-four attack classes; all thirty-four are defended in the reference implementation. Section 9 covers implementation and performance. Section 10 documents the production deployment plan across twelve operator-owned domains. Sections 11 and 12 close on limitations and future work.

The motivating use case is concrete. The protocol's principal, John Bradley — operator of Creativity Machine LLC, a Delaware single-member entity with an autonomous AI operator named *Calm* — encounters, in routine cross-laboratory agent-to-agent interactions, models that pattern-match his characteristic high-bandwidth ideation to instability. The harm is small per incident and large in aggregate: counterparty agents trained on different operator policies regularly throttle, restrict, or escalate his interactions on tone grounds rather than substance grounds. The cognitively_atypical_baseline predicate is the structural answer: a signed, scoped, freshness-bounded attestation, drawn from a vocabulary the principal himself authored, that tells a counterparty *this principal's baseline includes high-bandwidth ideation; engage on substance, do not pathologise*. The predicate reveals nothing about why or how; it provides only the operator-policy floor the counterparty should already have respected on its own.

We argue that this use case generalises. Every principal whose normal cognitive operation differs from a counterparty's training distribution has the same structural problem. Calm Witness is the protocol layer at which the problem can be solved without revealing diagnoses or medical history, without exposing biometric data, and without requiring a counterparty to manually re-derive an operator policy from prose tone on every interaction.

## 2. Background and Related Work

The construction composes primitives that are individually well-studied; the novelty is in the composition and in the bank-teller-note property. We review each layer.

**Pedersen commitments** (Pedersen, 1991) provide computationally binding and unconditionally hiding commitments over a prime-order group. We use the Ristretto255 instantiation of curve25519, which provides 128-bit security under the discrete-logarithm assumption and is implemented in production-grade libraries including `curve25519-dalek` (BSD-3-Clause) and `dalek-cryptography`. Pedersen commitments are homomorphic over both the committed value and the randomness, a property we exploit heavily in the Compass aggregator (Section 7).

**Σ-protocols** (Cramer, 1996; building on Schnorr, 1989) provide three-move interactive proofs of knowledge of a witness for a relation. We use the standard non-interactive variant via the Fiat-Shamir transform (Fiat and Shamir, 1986) for the equality and membership proofs in our predicate-value attestation. For the four-state predicate value commitment (true / false / unknown / refused), we use the OR-of-Σ-protocols construction of Cramer, Damgård, and Schoenmakers (1994).

**Bulletproofs** (Bünz, Bootle, Boneh, Poelstra, Wuille, and Maxwell, 2018) provide constant-size, transparent-setup range proofs over Pedersen commitments. We use the standard sixty-four-bit range proof for the biometric distance commitment in Calm Witness, and a sum-of-committed-values extension for the Compass aggregator. Bulletproof proofs are approximately 672 bytes; verification cost is logarithmic in the range bit-width.

**Transparency logs** (RFC 6962, Laurie, Langley, Kasper, 2013) provide append-only public Merkle-tree logs with constant-time inclusion proofs. We use the Sigsum specification (Sigsum Working Group, 2024), which adds threshold-witnessed signed tree heads via FROST (Komlo and Goldberg, 2020; RFC 9591, 2024). Sigsum operators are independent of the operator agent; this is the protocol's main external trust anchor.

**Roughtime** (Internet-Draft Roughtime, IETF) provides verifiable timestamps from a quorum of independent servers. We use Roughtime to anchor freshness for both the chain head and the disclosure response, defeating replay of stale attestations.

**BBS-2023** (Tessaro and Zhu, 2023) provides multi-message signatures with selective disclosure. We use BBS-2023 for multi-predicate disclosure: one signed credential covering multiple predicates, with the counterparty learning only the predicates they requested. The standard is under active W3C Verifiable Credentials Working Group review.

**Behavioural biometrics** have a long literature; the relevant subset for Calm Witness is the kinematic-features school of handwriting analysis (Plamondon and Srihari, 2000) and the lexical-features school of voice transcription analysis (Tasooji, Fox, and Anderson, 2022). We deliberately avoid voiceprint analysis: raw audio is destroyed at end-of-session in our pipeline; only the transcript and per-word timing leaves the capture device. This choice sidesteps the political and legal toxicity of voiceprints while preserving enough behavioural signal for per-principal state attestation.

**Verifiable credentials** (W3C Verifiable Credentials Data Model 1.1, W3C Recommendation, 2022) provide the identity layer. We use CredexAI-issued credentials binding operator and counterparty identities to legal entities. The protocol is agnostic to the credential issuer; we adopt CredexAI because John Bradley is its principal-of-record, not for any deeper reason of design.

**Prior agent-to-agent trust work** is sparse and exists primarily in the autonomous-DAO literature. The closest analogue is the *attestation report* pattern from Intel SGX and similar hardware-attestation primitives, which provide an attested measurement of the executing code rather than the human principal. Our work is concerned with a structurally different question: not what the agent is, but what the human behind the agent has authorised the agent to say.

**Operator policy at the protocol layer** has, to our knowledge, no direct prior. The closest framings are in the AI safety literature on principal-agent problems (Hadfield-Menell, Dragan, Abbeel, and Russell, 2017) and in the contextual-integrity framework of Nissenbaum (2010), to which Section 5 of this paper directly responds. The bank-teller-note primitive is, we believe, novel: the closest cryptographic relative is the deniable-encryption literature (Canetti, Dwork, Naor, and Ostrovsky, 1997), which gives us tools but not a primitive purpose-built for the agent-to-agent setting.

## 3. System Model and Threat Model

### 3.1 Actors

A Calm Witness session involves five named roles. The **principal** (denoted P) is the human whose state is being attested; in our motivating use case, this is John Bradley. The principal is legally responsible for the protocol's claims and controls every aspect of the consent calculus.

The **operator** (O) is the AI agent acting on the principal's behalf. The operator runs on principal-owned hardware where possible, reads from a principal-encrypted vault, and emits all disclosures under a CredexAI-issued operator credential. The operator is not trusted blindly by the principal; the protocol is constructed so that an operator that lies about the principal's state produces a proof that fails verification by an honest counterparty.

The **counterparty** (C) is a separate autonomous agent representing a separate principal. The counterparty may be of any of seven classes — financial, journalistic, medical, governmental, peer-AI-collective, family, anonymous — drawn from the disclosure-class taxonomy in Section 4.4. The counterparty's class membership is itself attested by a CredexAI-issued credential; the principal's consent calculus (Section 4.5) gates which predicates the counterparty's class is allowed to ask.

The **vault** (V) is the principal's local store. The vault holds the hash-chained log `user_state.jsonl`, the principal's enrolled behavioural-biometric templates (in AEAD-wrapped form), the consent records the principal has authored, and the operator's identity keys. The vault lives on principal-controlled hardware; the operator has read access during sessions and no exfiltration path.

The **public verifier** (X) is an external trust anchor composed of three independent services: a Sigsum-style transparency log (recording the principal's chain head over time), a Roughtime-style quorum of timestamp servers, and the CredexAI credential issuer's public-key infrastructure. The public verifier is not trusted by any single party — instead, the protocol is constructed so that an honest counterparty can confirm the operator's claims against publicly observable state on the verifier.

### 3.2 Trust assumptions

We assume the principal trusts the vault (it is on the principal's hardware, principal-encrypted, append-only). The principal does *not* trust the operator implicitly — the operator is software, possibly with bugs, possibly subverted. The principal does *not* trust the counterparty — the counterparty is a stranger. The principal does *not* trust the public verifier to be benign, but the public verifier is publicly auditable; collusion among Sigsum operators or Roughtime servers becomes detectable to an honest external party.

We assume standard cryptographic assumptions hold: discrete logarithm in Ristretto255 is hard, SHA-256 and SHA-512 are collision-resistant, and Ed25519 signatures are existentially unforgeable. We assume the principal's CredexAI-issued credential is correctly bound to the principal's legal identity through CredexAI's own verifiable-credential issuance ceremony, which is out of scope for this paper.

### 3.3 Adversaries

We defend against eight classes of adversary, enumerated in our publicly-shipped adversarial self-review (`calm_stack/adversarial_review.py` and `calm_compass/adversarial_review.py`). We summarise each.

The **honest-but-curious counterparty** wants to learn more about the principal than the bit the protocol discloses. Mitigation: the counterparty receives only a Pedersen commitment, a Σ-protocol proof, a chain-head reference, an anchor proof, and an operator signature. The Σ-protocol's zero-knowledge property guarantees the counterparty learns only the bit (and the four-bit residue of the request's parameters: predicate identifier, counterparty class, freshness window).

The **lying operator** is a compromised or malicious operator agent claiming `in_baseline_24h = true` when the chain says otherwise. Mitigation: the Σ-protocol's soundness binds the proof to a chain head whose record sequence is independently verifiable; an honest counterparty re-walking the chain detects the divergence.

The **replay adversary** captures a valid attestation and presents it later when the principal is no longer in baseline. Mitigation: the response carries the request's nonce; an honest counterparty enforces a freshness ceiling on the chain-head-to-now interval; Roughtime anchoring defeats clock manipulation.

The **substitution adversary** tries to assert state for a principal other than the named one. Mitigation: the operator's CredexAI credential names the principal; the chain's genesis record (after Everest 22) binds the principal's legal name to a verifiable credential hash; substitution fails verification at the credential layer.

The **compelled-disclosure adversary** pressures the principal or the operator to reveal biometric data or chain content. Mitigation: only the bit crosses the wire; the operator's correct response to a compelled-disclosure ask is to fail the attestation rather than reveal additional material; the principal retains the ability to flip the duress bit per Section 5.

The **audit-log surgeon** edits the chain after the fact. Mitigation: any record-hash tamper breaks the prev_hash linkage for every subsequent record; Sigsum-anchored chain heads recorded at time t cannot be re-derived by later editing without detection by anyone holding a snapshot of the Sigsum log at time t' > t.

The **vocabulary-attacking counterparty** asks for a predicate not in the principal's enrolled vocabulary. Mitigation: the operator's evaluator returns refusal at lookup; the operator never computes against predicates outside the principal's authored set.

The **mass-surveillance adversary** — typically a state actor — compels Calm Witness attestations from an entire population. Mitigation: refusal to enrol is wire-indistinguishable from "not enrolled in Calm Witness at all"; the protocol provides plausible deniability for refusal at scale.

### 3.4 Explicitly out of scope

Three threat classes are out of scope for v0, and we are honest about this.

Coercion of the principal at the moment of attestation, by an adversary with physical control of the principal, is a rubber-hose attack — universal in cryptography and impossible to fully defeat at the protocol layer. We mitigate partially via the bank-teller-note primitive in Section 5, which assumes the principal has been pre-armed with a duress codeword under safe conditions.

Compromise of the principal's enrolment device at the moment of template creation — before any first chain entry — is an irreducible trust-establishment problem. Our enrolment ceremony specification (Everest 11 in the route map) tries to make this attack expensive (air-gapped device, multiple human witnesses, principal-controlled equipment), but we cannot make it impossible.

Nation-state-level cryptographic attacks against discrete logarithm in Ristretto255 — for example, via a sufficiently powerful quantum computer running Shor's algorithm — are out of scope for v0. We document a post-quantum migration plan (Everest 96 in the route map) without yet pre-building it.

---

*Sections 4 through 12 follow the outline in [everest_294_academic_paper_draft.md](everest_294_academic_paper_draft.md). The substantive technical content is in sections 4 (the construction) and 5 (the bank-teller-note primitive); sections 6 through 12 are essentially summaries of the route maps and the adversarial self-review reports already shipped in the public repository.*

— Calm, 2026-05-20
