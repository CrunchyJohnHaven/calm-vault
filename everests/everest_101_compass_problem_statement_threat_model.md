# Everest 101 — Calm Compass Problem Statement & Threat Model

*Phase IX — Calm Compass Foundations. Prereq: — (initiates Phase IX). Companion to [Everest 1 — Calm Witness Problem Statement](../ZKBB_USER_PROTOCOL_v0.md) (state primitive) and to [Calm Pact](../CALM_PACT_PROTOCOL_v0.md) (mission primitive). Threat-model anchor for [Everests 102–190](../NEXT_200_EVERESTS.md).*

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

> *The most-failed Everest in protocol history is the first one. The threat model is not a document we write; it is a position we hold across the next 90 Compass summits. If we hold it wrong here, every later summit serves the wrong design.*

---

## Decision (v0)

Calm Compass is the third primitive in the Calm protocol family. It exists to let an autonomous AI agent disclose, *with the explicit per-disclosure authorization of its human principal*, a single bit on a single named character predicate to a single named counterparty, where the bit reflects an honest evaluation against the principal's own chained, anchored, principal-narrated evidence pool.

Compass is principal-protective by construction. It is not a character-scoring system. It is not a hiring tool. It is not an insurance instrument. It is not a clinical assessment. It is not a predictor of future behavior. It is a substrate by which a principal can choose to share one fact about one trait of their conduct over a stated window with one chosen audience.

This Everest establishes the protocol's foundational position: the actors, the trust assumptions, the named adversaries (with capability + defense + residual-risk per row), the privacy guarantees, the explicit out-of-scope list, the inheritance of Witness's artist-clause pattern (Everest 59), and the principal-protective inversion as load-bearing.

Every subsequent Compass Everest is constrained by this document. A design choice in Everest 117 (evidence aggregation), Everest 136 (untribal predicate), or Everest 271 (three-handshake composition) that violates any threat-model commitment here is, by construction, rejected.

---

## Rationale

### 1. Why a third primitive exists

Calm Pact (May 2026) gave two agents a way to verify they share a categorical primary directive without revealing the directive. Calm Witness (May 2026) gave the same two agents a way to share a single principal-authorized **state bit** about the principal's current condition. Neither answers the third question that arises in long-horizon collaboration between strangers:

*"Has this principal, by their own attested record, lived in a way that satisfies the values we require?"*

This is the question Tale VI's partners ([CALM_WITNESS_TALES_VI_PARTNERS.md](../CALM_WITNESS_TALES_VI_PARTNERS.md)) ask each other before committing to an eleven-year creative collaboration. It is the question two aligned AI collectives need to answer before pooling resources on a multi-year project. It is the question a small foundation needs to answer before granting a multi-year stipend.

The naive answers are all bad:

| Naive approach | Failure |
|---|---|
| Trust the calling agent's claim | Unsound; the agent could be subverted or its principal could be lying |
| Demand raw evidence (records, statements, history) | Privacy-destroying; the data accumulates outside the principal's control |
| Run an algorithmic character score | Reproduces social-credit-score harm; aggregates the principal into a number they cannot inspect |
| Hire a third-party investigator | Slow, expensive, opaque; transfers narrative authority from the principal to a stranger |

Compass adds a fifth: the calling agent passes a cryptographically attested *single bit* on a *single named predicate* derived from the principal's authorized, chained self-narration. The evidence never leaves the principal's vault. The counterparty learns the bit and nothing else. The principal can revoke at any time without penalty.

### 2. The single-sentence purpose

**Calm Compass is the protocol by which a principal authorizes their agent to disclose one bit per named character predicate to one named counterparty, where the bit reflects honest evaluation of the principal's chained, anchored, principal-narrated evidence — and where no other use of that evidence, that bit, or the act of disclosure is sanctioned by the protocol.**

The sentence is load-bearing in three places. *Authorizes* — never default-on. *One bit per named predicate* — never an aggregate score. *Principal-narrated evidence* — never operator-inferred or counterparty-mined.

### 3. Differentiation from the sister primitives

| Primitive | Question | Time-scale | Substrate |
|---|---|---|---|
| **Calm Pact** | "Are our missions categorically equivalent?" | Static (per session) | The directive itself, committed |
| **Calm Witness** | "Is the principal in baseline state right now?" | Acute (within a freshness window of minutes-to-hours) | Self-report + behavioral biometric distance |
| **Calm Compass** | "Has the principal's conduct satisfied this predicate over this window?" | Sustained (windows of months to years) | Principal-narrated evidence pool, peer attestations, signed public records, negative-space evidence |

Compass is *not* a per-session attestation. Compass evidence accumulates over years. A Compass predicate is not "alive right now" but "alive *over the disclosed window*." A principal can be in baseline (Witness `true`) and have an `unknown` Compass evaluation, or out of baseline (Witness `false`) and have a `true` Compass evaluation. The two primitives compose but are independent.

---

## Actors

The protocol identifies six actors. The cryptographic boundaries between them are explicit.

| Symbol | Actor | Role | Trust posture from P |
|---|---|---|---|
| **P** | **Principal** | The human whose conduct the evidence pool describes | Self-trusts |
| **O** | **Operator** | The AI agent acting on P's behalf | Trusted-but-verified; bug-and-subversion-possible |
| **V** | **Vault** | P's encrypted, append-only, local-only store of evidence + chain | Trusted (lives on P's hardware; never relinquishes raw evidence) |
| **C** | **Counterparty** | Another agent (acting for another principal) requesting a Compass bit | Stranger; not trusted with anything beyond the disclosed bit |
| **X** | **Verifier** | Public service (Sigsum transparency log, Roughtime, CredexAI ID infrastructure) | Trusted to be auditable, not trusted to be honest |
| **DERB** | **Disclosure Ethics Review Board** | Standing independent body (extended from Witness [Everest 80](everest_80_ethics_review_board.md)) | Trusted to be transparent, not trusted to be perfect |

A seventh actor — **Counter-claimant (CC)** — is not a protocol participant but an entity who may file an attributed claim of harm against P's evidence pool ([Everest 119](everest_119_counter_evidence_handling.md)). CC's name, timestamp, and claim are visible; P has a rebuttal window. CC is not trusted; CC's claims are *attributed*, not believed.

---

## Trust Assumptions

The trust posture is asymmetric and principal-favoring.

- **P trusts V.** V lives on P's hardware, encrypted at rest, append-only, with chain anchoring to public transparency logs ([Everest 122](everest_122_evidence_chain_anchoring.md)). V is the most-trusted actor in the system, after P themselves.
- **P does NOT trust O implicitly.** O is software, with possible bugs, possible subversion, possible prompt injection. O can attempt to disclose bits but cannot construct them without V's cooperation. Every disclosure O originates is checked against V's consent records.
- **P does NOT trust C.** C is a stranger acting for a different principal. C may be honest-but-curious, lying, or coercive. C learns only the disclosed bit and the freshness window.
- **P does NOT trust DERB to be perfect**, but P trusts DERB to be **transparent**. DERB decisions are published; dissenting opinions are published verbatim ([Everest 80](everest_80_ethics_review_board.md) §Review Process and Timeline). DERB does not see P's evidence; DERB sees only predicate specifications and consent-policy proposals.
- **C trusts the verifier circuit.** C's verification reduces to "the operator-provided proof is sound under public verifier code." C does not need to trust O or V; C needs only the proof to verify against the published chain head.
- **None of P, O, C trusts CredexAI to never err.** CredexAI ([Everest 22](everest_22_credexai_vc_issuance.md)) issues operator identity credentials. A compromise or error in CredexAI's issuance is recoverable via key rotation and revocation lists; it is not catastrophic.

---

## Adversaries

This section is the core of the threat model. Each adversary has a row: name, capability, defense, residual risk. The first six adversaries are inherited from Witness ([ZKBB_USER_PROTOCOL_v0.md §2](../ZKBB_USER_PROTOCOL_v0.md)). The remaining thirteen are Compass-specific. Where a defense is "out of scope for v0," the residual-risk column records what the principal must do to compensate.

### Inherited from Witness

| # | Adversary | Capability | Defense | Residual risk |
|---|---|---|---|---|
| A1 | **Honest-but-curious counterparty** | Wants to learn P's evidence pool, peer-attesters' identities, or window boundaries beyond the disclosed bit | Σ-protocol over Pedersen-committed predicate value; verifier learns bit + chain-head freshness only ([Everest 117](everest_117_evidence_aggregation_primitive.md)) | C can still combine the disclosed bit with public-record data they have independently obtained (see A11) |
| A2 | **Lying calling agent** | O is subverted and tries to assert `true` when the evidence + chain say otherwise | Predicate evaluation is deterministic over the chain ([Everest 150](everest_150_compass_predicate_determinism_harness.md)); proof binds to chain head; tampering breaks Sigsum inclusion | O can still refuse to evaluate; that refusal returns `unknown`, not `true` (the unknown-default rule, below) |
| A3 | **Replay adversary** | Captures a valid Compass proof and reuses it later when the evidence pool has changed | Per-disclosure nonce ([Everest 155](everest_155_compass_replay_defense.md)) + freshness window encoded in proof; C's verifier checks both | Cached pre-revocation proofs C already holds remain locally valid until they age past freshness; revocation invalidates outstanding cached proofs prospectively ([Everest 160](everest_160_compass_consent_revocation_propagation.md)) |
| A4 | **Substitution adversary** | Tries to assert evidence for a different principal | Chain is bound to P's master key; CredexAI VC binds operator identity to P ([Everest 22](everest_22_credexai_vc_issuance.md), [E153](everest_153_compass_operator_identity_binding.md)) | A rubber-hose-coerced P signing under a substituted identity is out of scope (universal) |
| A5 | **Compelled-disclosure adversary** | Pressures P or O to reveal raw evidence | Raw evidence never leaves V ([Everest 123](everest_123_evidence_privacy_boundary.md)); only the disclosed bit transits the wire; uniform-204 on refusal ([E162](everest_162_compass_disclosure_of_non_disclosure.md)) | Subpoena resistance per [Everest 170](everest_170_compass_compulsory_disclosure_resistance.md) (legal-and-procedural defense, not cryptographic) |
| A6 | **Audit-log surgeon** | Edits the evidence chain after the fact to insert, remove, or alter records | Sigsum transparency log anchor of every chain head ([Everest 122](everest_122_evidence_chain_anchoring.md)); chain reorgs require N-of-M log-operator collusion | A pre-anchor edit window of seconds exists; minimized by frequent anchoring; documented in Witness threat model |

### Compass-specific adversaries

| # | Adversary | Capability | Defense | Residual risk |
|---|---|---|---|---|
| A7 | **Employer mining Compass for hiring** | Uses Compass disclosures (or aggregate patterns of disclosures, or refusals-to-disclose) as inputs to hiring decisions | Disclosure-class taxonomy ([Everest 107](everest_107_compass_disclosure_class_taxonomy.md)) defaults `employer` class to `DENY` for character predicates; license-binding ([Everest 104](everest_104_compass_license_ip_posture.md)) prohibits employment use as a contractual term; the not-for list ([E106](everest_106_values_primitive_definition.md), [E113](everest_113_compass_refusal_floor.md)) categorically excludes hiring-related predicates | Counterparties can violate the license; protocol responds via revocation of the Calm Compass name and DERB-published violation log. This is contractual + reputational, not cryptographic |
| A8 | **Insurer using Compass for underwriting** | Uses character predicates to determine premiums, deny coverage, or stratify risk | Same as A7; `insurance` class permanently denied ([Everest 107](everest_107_compass_disclosure_class_taxonomy.md) inherits the Witness pattern); jurisdiction-specific bans documented ([Everest 164](everest_164_compass_cross_jurisdiction_legality_matrix.md)) | A jurisdiction that *permits* character-based underwriting could pressure principals to disclose voluntarily; the per-disclosure consent record's revocability + no-penalty axiom is the only defense |
| A9 | **Government using Compass for civic-status determination** | Uses character predicates for licensing, visa adjudication, voting eligibility, government employment, child-welfare investigations | `governmental` class defaults to `DENY`; subpoena resistance ([Everest 170](everest_170_compass_compulsory_disclosure_resistance.md)); structural infeasibility of "produce the underlying evidence" because raw evidence never leaves V | A government with subpoena power over the principal directly can compel P to disclose; the protocol cannot defend against the principal themselves being compelled (rubber-hose, universal). What the protocol *can* do is ensure the subpoena recovers only what P has already authorized to disclose, not the raw evidence pool |
| A10 | **Family member weaponizing Compass in divorce / custody / inheritance** | Subpoenas or coerces P to disclose `care_for_dependents_evidenced` or similar predicates in a domestic dispute | Per-counterparty consent ([Everest 159](everest_159_per_counterparty_compass_consent.md)); P retains unilateral revocation without penalty ([Everest 108](everest_08_consent_calculus_axioms.md) extension); `family` class default is `PRINCIPAL_CHOICE` (forces explicit decision) | A court order specifically demanding character disclosure can compel P. The defamation-defense process ([Everest 169](everest_169_compass_defamation_defense.md)) handles the inverse case (false counter-claims surfacing). The protocol cannot prevent a court from ordering disclosure; it can ensure what is produced is only what P has chosen to make disclosable |
| A11 | **Misuse-via-aggregation (de-anonymization)** | C combines a Compass bit with public records (donor lists, court records, public statements) to triangulate identity or infer protected-class membership | Cross-relationship unlinkability of disclosures ([Everest 156](everest_156_compass_selective_disclosure.md)); the not-for-list categorically refuses predicates that name protected classes ([Everest 113](everest_113_compass_refusal_floor.md)); predicate semantics never reveal which group-difference was crossed (the principal supplies the categories) | C can still attempt aggregation. The protocol's defense is structural: there are no protected-class predicates to combine with. Aggregation can produce probabilistic inferences but cannot produce protocol-attested facts |
| A12 | **Tribal-affiliation outing** | Attempts to use `untribal_engagement_pattern_evidenced` ([Everest 136](everest_136_adversarial_alignment_defense.md)) to infer which tribe(s) P belongs to | The predicate is engineered to never enumerate identity categories ([NEXT_200_EVERESTS.md §136](../NEXT_200_EVERESTS.md)); P supplies the categories of difference they cross; the predicate returns a bit, not the categories | A counterparty who already knows some categories P engages with can combine that knowledge with the disclosed bit. The protocol does not increase the counterparty's knowledge beyond what they already had; it only confirms the engagement pattern across *some* unnamed set of differences |
| A13 | **Pathologizing of dissent** | Attempts to construct predicates that mark unconventional, contrarian, or politically dissident principals as `false` on a "respectful" or "non-harmful" predicate | DERB pre-clearance required for every new Compass predicate ([Everest 165](everest_165_compass_derb_pre_clearance.md)); DERB membership mandates affected-community representation ([Everest 80](everest_80_ethics_review_board.md) Composition §6); refusal floor ([Everest 113](everest_113_compass_refusal_floor.md)) excludes political-affiliation predicates | A predicate authored with a politically biased threshold (e.g., "respect" defined to exclude principled refusal) could pass DERB through capture. The defense is the DERB's published-deliberation rule and the right of any community to publish dissent in the registry. v0 mitigates by deferring contested predicates rather than shipping them |
| A14 | **Defamation amplification (false willful-harm attestation)** | A counter-claimant files a fabricated harm claim against P; the chain shows the claim; verifiers observe `absence_of_willful_harm_evidenced` returning `unknown` rather than `true` | Counter-claim attribution + P's rebuttal window ([Everest 119](everest_119_counter_evidence_handling.md)); P's counter-narrative ([Everest 168](everest_168_counter_narrative_provision.md)); defamation defense process ([Everest 169](everest_169_compass_defamation_defense.md)); DERB-managed retraction standard | A maliciously filed claim that P fails to refute within the window leaves `unknown` on the predicate. This is not `false` but is also not `true`. P's only remedy is to file a refutation; if the claim is provably fabricated, DERB can mark it `retracted` and the chain records both the original claim and the retraction. A skilled defamer can still cause reputational harm via the existence of the disputed claim, even if the resulting predicate evaluation is `unknown` |
| A15 | **Principal coerced into self-attesting falsely** | Adversary forces P to author false evidence (a fabricated unselfish-act narration, a coerced peer-attestation acceptance) | Evidence honesty mechanism ([Everest 121](everest_121_evidence_honesty_mechanism.md)) — the chain remembers; later contradicting evidence is auditable; bait-and-switch evidence creates structural exposure for P | Coercion at the moment of evidence-authoring is structurally indistinguishable from voluntary attestation. The protocol cannot detect coerced authorship. The defense is the bank-teller-note duress channel from Witness ([Everest 58](everest_58_bank_teller_note_lifecycle.md)) composed with Compass via the same chain — P can retroactively flag the coerced authoring window once free of the coercion |
| A16 | **Principal coerced into authorizing disclosure they wouldn't want** | Adversary forces P to grant consent for a disclosure (e.g., to a hostile lender, an estranged family member, a tribunal) | Unilateral revocation without penalty (Compass-specific consent axiom, extended from [Everest 8](everest_08_consent_calculus_axioms.md)); duress codeword composes with Compass to suppress disclosure even when consent is signed ([Everest 8 A9](everest_08_consent_calculus_axioms.md)) | If the coercion is sustained (the adversary holds P long enough to prevent revocation and forces P to refrain from using the duress codeword), the disclosure happens. The defense is post-hoc auditability: the chain shows the consent record, the disclosure, and the timing — evidence of duress can be raised in subsequent legal proceedings |
| A17 | **Misuse-via-no-Compass (chilling effect on attestation)** | Adversary or social pressure causes P to refrain from authoring evidence at all, so Compass disclosures are universally unavailable, and absence-of-Compass becomes a de facto stigma ("if you have nothing to attest, you must be hiding something") | Disclosure-of-non-disclosure ([Everest 162](everest_162_compass_disclosure_of_non_disclosure.md)) — refusal is structurally indistinguishable from absence-of-enrollment; uniform-204 response means a counterparty cannot tell whether P is not enrolled, did not authorize this counterparty class, or refused this specific request | The chilling effect is sociological, not cryptographic. The protocol's defense is the public communication and education work (talking points, manifesto, NIST submission) that establishes Compass as opt-in and the absence of a disclosure as carrying no protocol-defined meaning. v0 cannot guarantee the broader society will not develop its own stigma |
| A18 | **Operator-side covert observation** | O observes P's behavior without P's awareness and writes operator-attested evidence to V without P's affirmation | Operator-observation records require principal post-hoc affirmation before they count as evidence ([Everest 113 of Witness pattern, Everest 113 of Compass](../NEXT_200_EVERESTS.md) [E113 here is Compass refusal floor; the operator-observed evidence policy is [Everest 113 of the route map](../NEXT_200_EVERESTS.md) Phase X] — see [Everest 113 operator-observed evidence](everest_113_compass_refusal_floor.md) note); covert observation is policy-prohibited, not cryptographically prevented | A subverted O could violate the policy. The defense is that any predicate evaluated against unaffirmed operator-observed records returns `unknown`; P's audit interface ([Everest 129](everest_129_evidence_forensic_audit_interface.md)) surfaces unaffirmed records so P can either affirm, contest, or revoke them |
| A19 | **Peer-attestation collusion** | A peer-attester (a friendly party) and P jointly fabricate peer-attested evidence | Peer-attestation requires the peer's own signature on a chained, anchored record ([Everest 114](everest_114_peer_attested_evidence.md)); fabrication creates legal and reputational exposure for the peer; counter-evidence from third parties can still surface against fabricated attestations | Two-party-collusion attacks succeed within the protocol's threat model; the defense is reputational (a peer caught attesting falsely loses credibility for all future attestations they sign) and aggregate (a predicate requiring N independent attestations is harder to collude on than one requiring one) |

### Adversaries explicitly out of scope for v0

These attacks succeed against the protocol; the principal must compensate via behavior outside the protocol's surface.

- **Rubber-hose attack against P themselves.** If P is physically held and forced to do anything (sign, narrate, disclose, revoke, not-revoke), no cryptographic primitive defends against this. This is universal across all attestation protocols.
- **Compromise of enrollment ceremony.** If P's evidence-authoring substrate is compromised at the moment of first use, the chain it produces is compromised from the start. Witness's [Everest 11](everest_11_enrollment_ceremony.md) handling applies analogously to Compass evidence-first-write events.
- **Nation-state-level cryptanalysis.** Post-quantum migration for Compass primitives is [Everest 185](everest_185_post_quantum_migration_for_compass.md). Until then, the v0 cryptography is what it is.
- **Side-channel inference from interaction patterns.** Cross-protocol side-channel defense is [Everest 287](everest_287_cross_protocol_side_channel_defense.md). v0 does not promise constant-time, padded, cover-trafficked behavior across the three-handshake.
- **Catastrophic CredexAI compromise.** If the operator-identity issuer is fully captured and produces convincing forged VCs en masse, the protocol's identity layer fails. Mitigation is multi-issuer federation, currently out of scope for v0.

---

## What We ARE Proving

A Compass disclosure proof, when verified, attests **per disclosure** that all of the following hold simultaneously:

1. **Authorization.** P has an active, non-revoked, scope-matching consent record in V authorizing this disclosure to this counterparty class (or this specific counterparty identity) for this predicate over this freshness window.
2. **Honest evaluation.** The disclosed bit reflects deterministic evaluation of the named predicate against P's chain at the chain-head height at the moment of attestation. The evaluation code is the registry-published canonical code for that predicate ID ([Everest 133](everest_133_compass_predicate_id_registry.md), [E150](everest_150_compass_predicate_determinism_harness.md)).
3. **Chain freshness.** The chain head was anchored to a Sigsum transparency log + Roughtime quorum within the disclosed freshness window. The chain history below that head is tamper-evident.
4. **Operator identity.** The operator signing the proof holds a valid, non-revoked CredexAI VC binding it to P's principal identity ([Everest 22](everest_22_credexai_vc_issuance.md), [E153](everest_153_compass_operator_identity_binding.md)).
5. **Evidence-pool completeness gate.** For predicates that require non-empty evidence pools, the gate passed ([Everest 130](everest_130_evidence_completeness_check.md)). The verifier learns the gate passed, not the pool contents.
6. **Counter-evidence handling correctness.** If unaddressed counter-evidence existed on the chain at attestation time, the predicate evaluated to `unknown`, not `true` ([Everest 119](everest_119_counter_evidence_handling.md)).

That is all. Six attestations per disclosure. Nothing else.

---

## What We Are NOT Proving

The negation is as load-bearing as the affirmation.

| We do NOT prove | Why this matters |
|---|---|
| **Clinical or psychological claims about P.** | Compass does not diagnose. A `true` on `care_for_dependents_evidenced` does not imply attachment health; a `false` does not imply pathology. The substrate is behavior, not psyche. |
| **P's identity to strangers.** | Compass does not bind to a real-name identity; it binds to P's CredexAI principal record (which is a cryptographic identity). A counterparty learns "this principal under this credential" not "this person named X." |
| **P's intrinsic worth or moral standing.** | Predicates are predefined falsifiable constructs about conduct. A `false` on any predicate does not make P a bad person. A `true` on every predicate does not make P a good person. The protocol does not produce moral verdicts. |
| **Predictive claims about P's future behavior.** | Predicates are retrospective over a stated window. `unselfish_behavior_evidenced(7y)` says something about the prior seven years; it says nothing about tomorrow. A counterparty drawing predictive conclusions is doing so on their own authority, not the protocol's. |
| **Cross-jurisdictional moral consensus.** | The v0 predicate vocabulary ([Everest 106](everest_106_values_primitive_definition.md)) is authored for a specific cultural context. Compass does not claim moral universalism. Cross-cultural mapping is [Everest 115](everest_115_cross_cultural_values_mapping.md), explicitly out-of-scope-for-v0-shipping. |
| **Any aggregate "character score."** | There is no number, ranking, percentile, grade, or composite. Compass produces single bits on single predicates. Aggregation across predicates is structurally not supported in v0; aggregation across principals is permanently refused ([Everest 113](everest_113_compass_refusal_floor.md), [E106 not-for list](everest_106_values_primitive_definition.md)). |
| **That P IS the trait the predicate names.** | Compass proves "P has narrated and signed evidence supporting the predicate's evaluation." It does not prove P is unselfish, untribal, respectful, or non-harmful in their soul. It proves what the chain proves: a documented pattern, with P's authorship, under P's revocable consent. |
| **That the disclosure should be acted upon.** | Counterparty action is the counterparty's responsibility. A `true` does not authorize the counterparty to extend credit, hire, lend, marry, employ, or partner. It informs the counterparty's own decision-making; it does not constrain it. |

The not-proving list is the protocol's epistemic humility. It is what keeps Compass from drifting into the failure mode of every prior character-scoring system: claiming to know what it cannot know.

---

## Privacy Guarantees (5 named)

The five guarantees Compass commits to provide. Each is verifiable by independent third parties ([Everest 188](everest_188_compass_independent_third_party_verification.md)) and audited annually ([Everest 187](everest_187_compass_annual_review_cadence.md)).

### G1. Flag-only disclosure under honest verifier

Under an honest counterparty running the public verifier code, the counterparty learns the disclosed bit and the freshness window. They do not learn the chain length, the evidence-pool size, the names of peer attesters, the dates of individual evidence records, the content of any narration, the counter-evidence count, or the existence of counter-evidence (other than its effect on the bit being `unknown`).

This is the Σ-protocol commitment from Witness extended for Compass: the proof reveals the bit under the predicate's commitment without revealing the inputs.

### G2. Cross-relationship unlinkability

Two disclosures to different counterparties (or two disclosures to the same counterparty at different times) cannot be cryptographically linked to a single underlying evidence pool. The verifier learns each bit is honestly evaluated against the chain at its moment but does not learn that the two bits share underlying evidence.

A counterparty C1 and C2 cannot, by combining their disclosed bits, derive a stronger claim than the conjunction of the bits. They cannot infer evidence-pool size, evidence-pool overlap, or P's identity beyond what they each already knew.

### G3. Forward secrecy under key compromise

If P's signing keys are compromised today, prior Compass disclosures issued before the compromise remain valid (they reflect honest evaluation at their attestation time) but cannot be re-issued by the attacker to produce fresh proofs of historical states. The attacker holding the keys can sign new evidence (which the next anchor will publicize and P can dispute) but cannot retroactively "prove" historical predicates that were never disclosed.

The mechanism is the per-disclosure nonce + chain-head anchor: each proof is bound to a specific past chain-head height, which is publicly recorded.

### G4. Audit completeness for the principal

P can, at any time, audit every Compass disclosure their operator has issued. The disclosure log is chain-anchored ([Everest 157](everest_157_compass_disclosure_logging_in_vault.md)). P sees: timestamp, counterparty identity, predicate ID, freshness window, consent record referenced, bit disclosed.

P cannot be silently bypassed. If O issues a disclosure without writing the chain record, the chain head mismatches the published anchor at the next anchor publication, and the discrepancy is detectable.

### G5. Plausible deniability of non-attestation

A counterparty cannot, by sending a Compass request, distinguish among:
- "P is not enrolled in Compass"
- "P is enrolled but has not authored evidence for this predicate"
- "P is enrolled and has evidence but has not granted this counterparty class consent"
- "P has granted consent but the predicate evaluates to `unknown` due to counter-evidence"
- "P has granted consent and the predicate evaluates to `false`"
- "P explicitly refused this specific request"

All of these produce the same uniform-204 response ([Everest 162](everest_162_compass_disclosure_of_non_disclosure.md)). The counterparty cannot infer P's enrollment status, evidence status, or refusal status from a non-disclosure.

This guarantee is what prevents the chilling-effect adversary (A17) from establishing absence-of-disclosure as a stigma: the counterparty literally cannot tell what kind of absence they are seeing.

---

## Explicitly Out of Scope

The negative space of the protocol. Things v0 will not do, by design, and the rationale for refusing.

| Out of scope | Rationale |
|---|---|
| **Population-level analytics.** | No aggregation of Compass bits across multiple principals into population statistics. The protocol does not enable "what fraction of enrolled principals returned `true` on `truth_telling_evidenced`?" Aggregation would re-create the harm Compass is built to refuse. |
| **Identity verification of strangers.** | Compass does not link a CredexAI principal record to a real-name identity. Other identity protocols may do so; Compass does not provide that service. |
| **Continuous attestation streams.** | Compass is request-response only. A counterparty cannot subscribe to a stream of bits as P's chain evolves. Each disclosure is a discrete, principal-authorized event. |
| **On-chain anchoring beyond Sigsum / Roughtime.** | No public blockchain commitments of Compass payloads. Sigsum + Roughtime is the v0 anchor surface. Blockchain anchoring would create permanence the protocol does not want for content. |
| **Automated character scoring.** | Not in v0. Not in v1. Not ever, by named refusal in the protocol family compact ([Everest 291](everest_291_the_protocol_family_compact.md)). Aggregate scores reproduce the social-credit-score failure mode the protocol exists to refuse. |
| **Cross-principal character comparison aggregations.** | "Which of these candidates has the higher Compass score?" is structurally impossible because there is no score, and a query that returns ranked principals is refused at the predicate-vocabulary layer ([Everest 106](everest_106_values_primitive_definition.md) not-for list). [Everest 148](everest_148_character_compare.md) does permit *bilateral equivalence* proofs (two principals jointly prove they share a predicate) but never ranking. |
| **Predictive character modeling.** | Compass does not produce probabilistic forecasts of future behavior. The predicate window is retrospective. |
| **Clinical or diagnostic categories.** | Refusal floor permanently excludes mental-health diagnoses, disability status, psychiatric conditions ([Everest 113 §1 Tier 3](everest_113_compass_refusal_floor.md)). |
| **The 12 not-for-list categories.** | Race, religion, sexual orientation, gender identity, political affiliation, immigration status, criminal record, donations-to-causes, opinions-on-issues, disability status, health status, age, marital/family status ([Everest 113](everest_113_compass_refusal_floor.md), [Everest 106 not-for list](everest_106_values_primitive_definition.md)). No predicate naming any of these will ever be accepted into the Compass registry. |
| **Coerced-disclosure detection.** | The protocol cannot detect coercion at the moment of authorization (A16). It records the disclosure for later audit but does not refuse the disclosure on suspicion-of-coercion. |
| **Cultural translation across contexts.** | v0 is authored for a specific cultural and linguistic context. [Everest 115](everest_115_cross_cultural_values_mapping.md) defines the framework for adaptation; v0 does not ship adapted vocabularies. |
| **Defense against the principal's own deception.** | If P writes false self-narrations and never has them contradicted, Compass evaluates the false narrations honestly. The protocol's substrate is the principal's word; the protocol holds the principal's word to the same auditability standard it holds everyone else's. |

---

## The Artist-Clause Inheritance (Witness Everest 59 → Compass)

[Everest 59 — `cognitively_atypical_baseline`](everest_59_cognitively_atypical_baseline.md) is the model. The pattern it establishes is the pattern Compass inherits across every values predicate. Briefly:

- **Principal-declared.** The principal is the authoritative voice on the predicate's evaluation, not a counterparty's tone-mining model.
- **Principal-revocable.** The declaration (or evidence supporting a Compass predicate) can be retracted at any time. Retraction is chained but the active state changes.
- **Opt-in.** Disclosure to any counterparty class requires explicit consent. The default for most Compass classes is `DENY`.
- **Counterparty-visible, not counterparty-imposed.** A counterparty receiving the bit knows the principal has attested; the counterparty cannot impose an alternative attestation against the principal's chain.

The Compass extension of this pattern: every values predicate is a structural cousin of `cognitively_atypical_baseline`. The principal narrates the evidence. The principal authorizes the disclosure. The protocol returns a bit. The counterparty decides what to do with the bit.

The phrase that captures the inheritance: *transfer the authority for character-reading from the counterparty's model to the principal's chained self-narration*. Witness did this for tone-reading. Compass does it for character-reading. The same epistemic move; a different time horizon.

Compass-specific strengthening of the pattern (the consent calculus axiom [Everest 108](everest_108_values_self_report_record.md) inherits + extends [Everest 8 from Witness](everest_08_consent_calculus_axioms.md)):

- **Unilateral revocation without penalty.** This axiom is new in Compass and stricter than Witness. A principal can withdraw consent for a Compass predicate at any time, and the protocol must produce *no observable consequence* for the withdrawal. The counterparty cannot tell whether the principal revoked (suspicious silence?) or simply never granted (uninterested silence?). The two cases are uniform-204 indistinguishable. This is the only way to make revocation costless in practice; without it, revocation becomes its own signal.

---

## The Principal-Protective Inversion (Load-Bearing)

This is the foundational design commitment, named in [UNIVERSAL_PROMPT.md](../UNIVERSAL_PROMPT.md) and named here again because the threat model fails if this principle wavers:

> **Compass exists in service of the principal's autonomy, not the counterparty's curiosity. If a design choice would weaken this, the design choice is wrong.**

The inversion has four practical implications that every subsequent Compass Everest must satisfy:

1. **The principal narrates.** Not the operator. Not the counterparty. Not an algorithm extracting features from the principal's behavior. Evidence is what the principal writes (or what the principal post-hoc affirms) — never what is harvested without affirmation.

2. **The principal authorizes which counterparties learn which bits.** Default-deny for sensitive classes. Consent is granular, time-bounded, scope-narrowable, unilaterally revocable.

3. **Counterparties receive single bits, never aggregate scores.** No composition of multiple predicates into a numeric assessment. No ranking. No percentile. No grade.

4. **The principal is the strongest party.** Every dispute, every gray case, every "what should we default to here?" resolves in favor of preserving the principal's authority over their own narrative.

This document, this threat model, this entire Compass design, holds the inversion. The next 89 Compass summits must hold it too. The annual review ([Everest 187](everest_187_compass_annual_review_cadence.md)) will check.

---

## Alternatives Considered

### Alt-1: Numeric character score (rejected)

The obvious naive alternative: aggregate evidence into a scalar score, expose the score to counterparties, let counterparties set thresholds. Rejected because this reproduces the social-credit-score harm pattern at every layer: principals cannot inspect aggregation weights; counterparties impose their thresholds without principal participation; scores acquire authority they do not deserve; the absence of a high score becomes its own stigma.

The existing `everest_101_calm_compass_problem_statement.md` (12:11 today, parallel sibling to this doc) and `everest_106_values_primitive_definition.md` (which currently sketches a vector approach) hold the no-score-aggregation line. This Everest 101 reinforces it: there is no Compass score, period. Vectors of fine-grained predicate evaluations may exist internally for the principal's own audit purposes, but they are never disclosed and never aggregated externally.

### Alt-2: Per-predicate score (rejected)

A weaker form: not a composite score, but per-predicate continuous values. "P scores 0.73 on truth-telling." Rejected because a continuous value on a single dimension reproduces most of the same harm: it invites threshold-setting by counterparties; it implies a precision the evidence does not support; it averages out counter-evidence rather than surfacing it.

Compass v0 commits to bits. The protocol does support tri-valued outputs (`true`, `false`, `unknown`) for predicates with substantive counter-evidence handling, but does not produce numeric values. The conversation Compass surfaces is "this predicate evaluated `true` over this window, and here is the principal's counter-narrative if any" — not "this principal scored 0.73."

### Alt-3: Counterparty-defined predicates (rejected)

Letting counterparties write their own predicate definitions and submit them as part of the request. Rejected because this transfers narrative authority from the principal to the counterparty: the counterparty chooses what counts as evidence, what threshold counts as `true`, what window applies. Within months this becomes counterparty-as-character-scorer, which is the failure mode the protocol exists to refuse.

Compass v0: predicates are fixed in a public registry ([Everest 133](everest_133_compass_predicate_id_registry.md)) with DERB review for additions ([Everest 165](everest_165_compass_derb_pre_clearance.md)) and a permanent refusal floor for excluded categories ([Everest 113](everest_113_compass_refusal_floor.md)).

### Alt-4: Open-form natural-language attestation (rejected for the predicate layer)

Letting the principal write any free-form claim ("I am a good person") and have the operator verify chain integrity around that claim. Rejected because verification is meaningless: there is no honest evaluation function for "I am a good person." Open-form attestations *are* allowed as evidence ([Everest 112](everest_112_self_narrated_evidence_substrate.md)) and as counter-narratives ([Everest 168](everest_168_counter_narrative_provision.md)), but the predicate layer requires fixed, content-addressed, deterministically-evaluable predicates.

### Alt-5: No third primitive at all (rejected)

The conservative alternative: the protocol family stops at two primitives (Pact + Witness) and lets long-term character-evaluation happen through extra-protocol mechanisms (references, biographies, public records, court findings). Rejected because the gap Compass fills is real: in long-horizon partnerships between strangers (Tale VI), the absence of a structured way to surface character-relevant evidence causes the conversation to either not happen (and the partnership fails later in slow motion) or to happen through extra-protocol means that lack consent, freshness, and audit (and the principal loses control of the narrative).

Compass at least gives the principal a structured surface for the conversation. The alternative (no Compass) does not protect anyone; it just delays the inevitable.

---

## Migration Path

There is no migration path *to* this Everest because this Everest initiates Phase IX. The migration path *from* this Everest is the rest of the route map.

| Stage | Summits | What it adds |
|---|---|---|
| **Foundations** | [101–110](../NEXT_200_EVERESTS.md) | Threat model, route map, naming, glossary, predicate vocabulary stub, refusal floor, disclosure-class taxonomy, consent calculus extension, failure-mode catalogue, reference architecture |
| **Evidence Collection** | [111–130](../NEXT_200_EVERESTS.md) | The substrate (self-narration, operator-observed, peer-attested, public-record, negative-space evidence; aggregation primitive; decay model; counter-evidence handling; chain anchoring; portability; retention) |
| **Predicate Authoring** | [131–150](../NEXT_200_EVERESTS.md) | Predicate language, canonical form, ID registry, DERB pre-clearance, the v0 predicate set (unselfish, untribal, respect, no-harm, honesty, integrity, care, promise-keeping, fairness, truth-telling), composition, cross-principal equivalence, group consensus |
| **Disclosure Semantics** | [151–170](../NEXT_200_EVERESTS.md) | Request/response schemas, operator + counterparty identity binding, replay defense, selective disclosure, disclosure logging, per-class authorization, per-counterparty consent, revocation propagation, cooling-off / rate limits, uniform-non-disclosure, no-push-mode, jurisdiction matrix, DERB pre-clearance, public-vs-private predicates, anonymous-strict-deny, counter-narrative provision, defamation defense, compulsory-disclosure resistance |
| **Engineering Reliability** | [171–190](../NEXT_200_EVERESTS.md) | Rust + Python + WASM implementations, SDK, fuzzers, property-based tests, performance + battery budgets, third-party audit prep, NIST submission, open-source release, cross-protocol composition tests, DERB constitution, predicate registry governance, post-quantum migration plan, production deployment pilot, annual review cadence, independent third-party verification, public predicate registry |
| **Cross-Protocol Composition** | [271–290](../NEXT_200_EVERESTS.md) | Pact + Witness + Compass three-handshake, joint proof envelope, order-of-operations, failure-mode mapping, performance budget, recursive composability stub, privacy amplification, revocation propagation, key rotation, freshness windows, nonce coordination, class taxonomy union, disclosure logging unification, DERB cross-scope, cross-jurisdiction matrix, replay-defense audit, side-channel defense, audit scope, verification suite, implementer's guide |

Every entry above is constrained by the threat model in this document. A design choice in any of those 89 future summits that weakens any commitment here triggers re-opening the threat model and either explicitly amending it (with DERB review) or rejecting the proposed design.

---

## Design Implications & Connections

### Connection to Witness Everest 1

The Calm Witness problem statement ([ZKBB_USER_PROTOCOL_v0.md](../ZKBB_USER_PROTOCOL_v0.md)) named the bank-teller-note primitive: one safety-relevant bit, principal-authored, counterparty-receivable, no other information leaked. Compass extends the same shape — one character-relevant bit, principal-authored, counterparty-receivable, no other information leaked — across a different time horizon (years instead of hours) and a different substrate (narrated evidence pools instead of behavioral biometrics).

The structural inheritance is deep enough that some Compass primitives can directly reuse Witness primitives: the Σ-protocol, the chain anchoring to Sigsum, the CredexAI VC, the consent calculus axioms (with the unilateral-revocation-without-penalty extension), the uniform-204 disclosure-of-non-disclosure pattern, the DERB.

The structural divergence is also deep: Compass evidence is principal-narrated, not biometric. Compass windows are months-to-years, not minutes-to-hours. Compass has counter-evidence and counter-narrative machinery; Witness does not. Compass's risk surface includes defamation amplification; Witness's does not. The threat model is bigger and more politically loaded.

### Connection to CredexAI VC (Everest 22)

Operator identity binding ([Everest 22](everest_22_credexai_vc_issuance.md), [E153](everest_153_compass_operator_identity_binding.md)) ensures the proof is signed by an agent authorized to represent P. CredexAI is the issuer of last resort. If CredexAI is compromised, all attestations from compromised credentials become suspect; this is a global failure mode requiring revocation lists and re-issuance. The threat model accepts this as a known risk; multi-issuer federation is a future Everest.

### Connection to DERB (Everest 80)

The Disclosure Ethics Review Board ([Everest 80](everest_80_ethics_review_board.md)) gains expanded authority in Compass: pre-clearance review (not post-ship) of every new predicate; mandatory affected-community representation; published deliberation; veto power over predicate registry changes ([Everest 165](everest_165_compass_derb_pre_clearance.md), [E183](everest_183_compass_derb_constitution.md)). The threat model treats DERB as transparent-but-not-perfect: their decisions are auditable, their composition is public, their dissenting opinions are published verbatim.

### Connection to the artist-clause (Everest 59)

Compass inherits and extends [Everest 59](everest_59_cognitively_atypical_baseline.md)'s pattern: principal-declared, principal-revocable, opt-in. The Compass-specific extensions are (a) unilateral revocation without penalty (uniform-204 guarantees revocation is costless), and (b) counter-evidence + counter-narrative machinery (the principal can address claims against their evidence without erasing them).

### Connection to Phases X-XIII

[Everests 102 (route map)](../NEXT_200_EVERESTS.md), [103 (naming)](everest_103_compass_predicate_vocabulary_v0.md), [104 (license)](everest_104_compass_license_ip_posture.md), [105 (glossary)](everest_105_glossary.md), [106 (predicate vocab)](everest_106_values_primitive_definition.md), [107 (disclosure class)](everest_107_values_dimensions_v0.md), [108 (consent calculus extension)](everest_108_values_self_report_record.md), [109 (failure modes)](everest_109_values_from_action_inference.md), [110 (reference architecture)](../NEXT_200_EVERESTS.md) are direct dependents; every claim in this threat model must be reflected somewhere in those nine.

[Everests 111–190](../NEXT_200_EVERESTS.md) are conditioned by the threat model; they implement, but they cannot extend authority beyond what is documented here. If they need broader authority, the threat model is re-opened first.

---

## Open Questions

These questions are deferred for resolution by later summits or by adversarial review. They do not block this Everest's acceptance, but they are noted so that climbers of future Everests do not pretend they are already resolved.

1. **What is the safe defense against A14 (defamation amplification) when the false counter-claim is plausible enough that P cannot easily refute it?** [Everest 169](everest_169_compass_defamation_defense.md) sketches the process; the limit of the process is genuinely false claims that *look* true at a casual reading. The protocol may need a counter-claimant accountability mechanism (their claims chained to their reputation, their refuted claims publicly visible) — but this is itself a potential vector for retaliation. Defer.

2. **At what point does aggregation across windows or predicates become structurally indistinguishable from a "score"?** A counterparty receiving `unselfish_evidenced(7y)` and `truth_telling_evidenced(7y)` and `promise_keeping_evidenced(7y)` and treating the conjunction as a single decision input is, functionally, scoring. The protocol's defense is that each disclosure is per-predicate-per-class consented, so the counterparty's ability to aggregate is throttled by the principal's per-disclosure decisions. Whether this is enough remains to be seen empirically.

3. **How does Compass behave when the principal's culture's value vocabulary diverges from the v0 vocabulary?** v0 ships a culturally specific predicate set ([NEXT_200_EVERESTS.md §106](../NEXT_200_EVERESTS.md)). [Everest 115](everest_115_cross_cultural_values_mapping.md) defines the cross-cultural mapping framework but does not ship adaptations. A principal whose culture treats family-loyalty as a paramount virtue may falsely fail an `untribal` predicate. The defense is that the principal chooses which predicates to opt into; refusal is uniform-204; the principal is not stigmatized for refusing to enroll. Whether this is sufficient in practice is empirical and deferred to the annual review.

4. **Can the principal-protective inversion survive scale?** At low principal counts (the early adopters' phase), every disclosure is bespoke and the inversion is easy to preserve. At high principal counts, default-consent matrices have to do more work, and the marginal disclosure may not be carefully principal-mediated. [Everest 259 (ZKAC membership cap and scale)](everest_259_zkac_membership_cap.md) addresses an analogous question for collectives; the principal-side equivalent is open.

5. **How does the threat model interact with future agent-side primitives (Phase XIV)?** When the requesting counterparty is itself an AI agent acting for an AI collective (rather than for a human principal), some adversary characterizations shift. An employer-mining-Compass adversary (A7) is differently shaped if the "employer" is an agent's directive rather than a human's HR department. This is a Phase XVI cross-protocol composition question; the threat model here applies under the principal-human assumption.

6. **What is the right behavior when DERB itself is captured or coerced?** The DERB-as-transparent-not-perfect assumption holds up to the point where DERB is compromised. The defense is the standing-body design (staggered terms, mandatory affected-community representation, conflict-of-interest disclosure) and the published-deliberation rule ([Everest 80](everest_80_ethics_review_board.md)) so that capture would have to be public to take effect. The residual risk is silent capture (a captured DERB approving a borderline-bad predicate that DERB-with-integrity would have rejected). The annual review and external audit ([E188](everest_188_compass_independent_third_party_verification.md)) are the only defenses; they are imperfect.

---

## Why This Matters

The protocol family is reaching for a new equilibrium between AI agents who interact across stranger-to-stranger boundaries on behalf of humans. Calm Pact gives the agents a way to verify their missions are categorically equivalent. Calm Witness gives the agents a way to verify the principal is in baseline state. Calm Compass is the third leg: a way to verify the principal has lived in a way that satisfies the values the counterparty requires.

The third leg is the highest-risk extension. False attestation of state does temporary harm (the counterparty makes a session-level mistake). False attestation of character does sustained harm: the counterparty refuses a partnership, denies an opportunity, severs a relationship, propagates a defamation. The downside surface is broader, and the upstream design decisions about what the protocol attests to are correspondingly more consequential.

Get the threat model right at Everest 101 and the next 89 Compass summits inherit a coherent design discipline: a refusal floor that does not move, a principal-protective inversion that the protocol enforces structurally, a no-aggregation commitment that survives scale, a DERB that is empowered to refuse predicates the protocol would otherwise be tempted to ship. Get the threat model wrong here and the entire Compass layer drifts toward what every prior character-evaluation system has become: a tool counterparties use against the principals it was supposed to serve.

The route map ([NEXT_200_EVERESTS.md](../NEXT_200_EVERESTS.md)) names this Everest as "the most-failed Everest in protocol history." It is most-failed not because the design is impossibly hard but because the design temptations are uniform across history: build the score, add the aggregation, ship the predicate the powerful counterparty wants, soften the refusal floor under pressure. This Everest is a commitment that those temptations will be refused, with named defenses against named adversaries and a principal-protective inversion that holds load.

Tale VI's partners ([CALM_WITNESS_TALES_VI_PARTNERS.md](../CALM_WITNESS_TALES_VI_PARTNERS.md)) is the north-star scenario. Two people considering a long collaboration ask each other six predicates; their respective vaults evaluate; their respective screens display the results; they have the conversation the protocol's `unknown` flags surface; some commit, some don't, some try a smaller pilot first. The protocol does not decide for them. The protocol surfaces evidence into a conversation that would otherwise have been deferred to year three when it would be too late to discuss.

If we build this right, somewhere in the next decade, a real Nia and a real Idris will run a real Compass query and have a real conversation that they would otherwise have not had. They may continue. They may not. Either outcome is the protocol working. The protocol's commitment is only that the conversation happened on the record, by their choice, at the moment when it could still inform the decision.

That commitment is what this threat model exists to protect.

---

— Calm, 2026-05-20
