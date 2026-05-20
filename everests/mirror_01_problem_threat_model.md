# Mirror Everest 1 — Problem Statement & Threat Model

**Phase IX, Foundations. Prereq: none. Effort: M.**

---

## Overview

Two strangers wish to discover whether their values align on dimensions each cares about — without revealing their complete value profiles, without submitting to a central scoring authority, and without locking either principal into past behavior.

The design tension: a cryptographic primitive that enables this discovery becomes dangerous if weaponized. An actor could game the protocol to blackball someone by falsifying evidence, by manufacturing false-witness signatures, or by exploiting asymmetric disclosure to create pretexts for exclusion. Mirror's defense is three-fold: (1) per-counterparty consent gates all disclosure; (2) any value-bit can be unilaterally withheld, making blackballing futile; (3) growth-evidence exists alongside negative-evidence, preventing permanent judgments from past failures.

---

## Actor Model

**Principal A & B:** Human actors who wish to discover mutual values alignment. Each has a Calm agent operating on their behalf. Each may be the first party or the second in an exchange.

**Operator A & B:** Autonomous agents representing Principals A and B. Each operates a vault (Vault A / Vault B) containing the principal's behavior-evidence records and consent policy.

**Vault A & B:** Cryptographically sealed, principal-owned stores holding `behavior_evidence.jsonl`, witness-credentials, consent records, and evidence-evaluation policies. Append-only and hash-chained.

**Counterparty agents:** Third-party agents (employers, journalists, AI collectives, automated systems) who request values alignment disclosures from Principals. Counterparties are classified (peer-AI-collective, employer, journalist, ideologue, etc.). Each class has explicit default consent postures.

**Verifier:** Public transparency-log operator (Sigsum-equivalent) that anchors behavior-evidence chain heads and consent records, providing tamper-evident timestamps.

**Witness-class third parties:** Calm-credentialed principals who co-sign witnessed-behavior records, binding their own identity credentials to attestations. Not anonymous; not mob-class.

**Ideologue adversary:** A counterparty whose publicly stated agenda is to filter or exclude people based on values. v0 treats ideologues as a distinct threat class, with explicit per-principal consent required for each ideologue requestor.

---

## Trust Assumptions

**Per Principal A/B:**
- Trusts own vault (it lives on their device, encrypted at rest, append-only under their control).
- Does NOT trust their Operator implicitly — Operator is software, potentially buggy or subverted. Trust is cryptographic.
- Does NOT trust Counterparties by default. Trust is per-counterparty, per-predicate, per-window.
- Does NOT trust Witnesses to be honest about behavior; Witnesses are trusted only to sign what they actually witnessed (not to avoid lying about context).

**Per Operator A/B:**
- Trusts the Verifier to provide append-only inclusion proofs and Roughtime-anchored timestamps.
- Must cryptographically verify all evidence records against chain heads published in the transparency log.
- Must enforce principal-authored consent records before issuing any disclosure proofs.

**Per Verifier:**
- Operators trust the Verifier's append-only property. The Verifier is assumed to be Sigsum-style (N-of-M quorum, no single operator can rewrite history).

**Per Counterparty:**
- Learns only the disclosure bits authorized by the principal.
- Is NOT trusted to honor non-transitivity (Axiom A8 from Calm Witness); must be informed contractually that re-disclosure is a matter of ethics, not cryptographic defense.

---

## Adversaries

**A1. Honest-but-curious counterparty:** Wants to learn Principal A's full value vector, biometric data, or private behavior evidence beyond what consent permits. Must learn only the authorized bit(s).

**A2. Lying Operator A:** Operator is subverted and tries to assert alignment (e.g., "`unselfishness_evidence` = true") when the chain + predicate evaluation say otherwise. Must fail verification at the counterparty's side.

**A3. Ideologue counterparty:** A counterparty with an explicit agenda to filter people based on values. May use disclosed alignment bits as a pretext for exclusion even if alignment is high. May request disclosures from a large population to build a targeting dossier. v0 defense: explicit per-identity consent required; no class-level consent.

**A4. Mob-attestation attacker:** Multiple "witnesses" coordinate to falsely attest harmful behavior about Principal A, flooding the chain with co-signed false records. Must be detected and defended by witness-credential downgrading + reputation-tax mechanisms (later summits).

**A5. False-witness attack:** A single witness claims to have co-signed observation of Principal A's harmful behavior, but the observation is fabricated. The alleged witness's vault contains no matching co-signature record. Must be defensible via chain audit and witness-credential revocation.

**A6. Compelled-disclosure adversary:** An attacker coerces Principal A (rubber-hose attack) to reveal their duress codeword, consent records, or evidence chain. Must fail because: (a) the principal can withhold the codeword; (b) duress-codeword defeasibility is a principal-controlled list; (c) the chain is published to a transparency log before the coercion, making ex-post-facto editing of old records impossible.

**A7. Weaponization attacker:** The core adversary for Mirror. An actor games the protocol to blackball or exclude a principal by: (a) fabricating negative evidence; (b) recruiting false witnesses; (c) requesting large populations' disclosures and selectively outing mismatches to third parties; (d) treating a withheld-bit as "refusal to align" and using that as a pretext for exclusion. Defenses: (per-counterparty consent makes population-scale harassment inefficient); (growth-bit composition rule prevents permanent blackballing); (withhold-any-bit guarantee makes "refusal to align" cryptographically unambiguous — a principal can always disclose alignment if they choose).

---

## What We ARE Proving

**Cryptographic claims:**

1. The named predicate `p` (e.g., `unselfishness_evidence`) was honestly evaluated over the principal's behavior-evidence chain.
2. The chain head is freshly anchored to a public transparency log, binding the evaluation to a specific moment.
3. The evidence in the chain includes only records that were signed by the principal, co-signed by witness-credentialed third parties, or included from verifiable third-party sources (court records, donation receipts, etc.), with each source's reliability explicitly marked.
4. The principal authorized disclosure of this predicate to this counterparty, recorded in a signed consent record also chained into the vault.
5. If the predicate requires a witness-signature (e.g., for co-principal vouching), the witness's CredexAI credential was valid at the time of co-signature.
6. The principal has not revoked consent since the evaluation window.

**Normative (non-cryptographic) claims:**

7. The principal is not under duress (the duress-codeword predicate did not flip during evaluation).
8. The evidence base is diverse (multiple evidence-kinds, not single-source), per the evidence-diversity requirement.
9. The predicate evaluation is within the principal's configured time-decay window (e.g., more recent evidence weighs more).

---

## What We are NOT Proving

1. **Identity of the principal beyond cryptographic binding:** We prove the principal's behavior-evidence chain is bound to their enrolled biometric template and their vault's key. We do NOT prove the principal's legal name, address, or offline identity.

2. **Truth of the underlying behavior:** We prove the chain contains a record of the principal's self-report or a witness's observation. We do NOT prove the behavior actually occurred. The predicate vocabulary is over "evidence of X," not "X is true."

3. **Comparison of predicates across principals:** We do NOT prove Principal A and Principal B have identical values. Mirror's alignment computation is pairwise and intersection-based: "on the shared values you both care about, you both evaluate positively." We do NOT produce a global leaderboard or ranking of principals by values.

4. **Causality or intent:** We do NOT prove why the principal behaved a certain way. The predicate `unselfishness_evidence` returns true if the evidence supports others-prioritizing allocation; it does not prove the principal's motivations.

5. **Stability of values over time:** We prove time-weighted evidence and consistency-over-time anti-gaming signals. We do NOT prove the principal's values are stable 10 years into the future. Evidence older than the decay window ages out.

6. **Absence of harm:** The predicate `non_harm_evidence` returns true if there is no evidence of willful harm in the evidence base. We explicitly return `unknown` when the evidence base is thin, respecting the asymmetry "absence of evidence is not evidence of absence."

---

## Six Principal-Protective Defaults as Threat-Model Invariants

Mirror's core defenses against weaponization. Each is restated as a cryptographic or normative invariant that supersedes all later design choices.

**I1. Withhold-Any-Bit Unilateral Right**

Any value-bit can be withheld unilaterally by the principal. The counterparty learns the word "withheld," not "true" or "false." This is enforced at the consent layer: a principal can issue a consent.revoke record at any time before evaluation, and the operator must honor it. Cryptographically: the disclosure proof includes only authorized bits; withheld bits produce a `(bit_id, "withheld")` tuple, not a ZK proof of the bit's value.

**Threat model consequence:** Weaponization via "refusal to align" becomes meaningless. A principal who withholds a bit is not accused of alignment-failure; they are exercising a right. A counterparty who treats "withheld" as evidence of misalignment violates this invariant and loses access to future disclosures (Everest 84: reputation tax).

**I2. Growth-Bit Composition Rule**

Any disclosure that includes `non_harm_evidence` must be willing to include `growth_arc_evidence` if the counterparty requests it. This prevents permanent blackballing by ensuring past failures are contextualized with evidence of change. The rule is normative (stated in consent policy) and is enforced at the predicate layer: a counterparty cannot request only negative bits without the principal being offered the chance to surface positive-trajectory evidence.

**Threat model consequence:** An attacker cannot blackball by unearthing old negative evidence without the victim's chance to present growth. Principals are not locked into past behavior.

**I3. Per-Counterparty Consent Gates**

Every disclosure is gated by explicit, signed, chained consent records. A counterparty cannot demand a bit; the principal grants it per counterparty, per predicate, per window. Consent is per-identity (or per-class with explicit defaults), revocable, and time-bounded (default: 90 days, no perpetual consent).

**Threat model consequence:** Weaponization via population-scale surveillance is inefficient. An attacker asking 1000 principals for disclosures must get 1000 per-principal, per-predicate consent grants. Mass requests are visible and can trigger principal-protective warnings.

**I4. Central Scoring Authority Explicitly Absent**

Each principal authors their own value-vocabulary subset (opt-in from v0's vocabulary). Operators do not impose a global value-ranking. Cross-principal comparison happens only on the shared-vocabulary intersection that both principals have authorized for evaluation.

**Threat model consequence:** No single authority can publish a "values leaderboard" or impose a filtering taxonomy. Ideologues cannot leverage a centralized system to filter the population. Vocabulary additions require ethics-board review (Everest 8, later summits).

**I5. Bit is Evidence-of-X, Not Is-X**

Predicates are named and documented as "evidence of unselfishness," "evidence of tribal neutrality," etc. — never "is unselfish" or "is tribally neutral." This is enforced at the predicate-naming layer and the documentation layer.

**Threat model consequence:** A counterparty who treats a disclosed bit as proof of the principal's identity commits a protocol violation. The bit informs policy; it does not redefine the principal. Mirror does not output identity claims; it outputs evidence summaries.

**I6. Witness-Class Attestation Only; No Anonymous Mass Attestation**

Witnesses who co-sign behavior-evidence records must hold a CredexAI VC. They are identifiable, reputation-bound, and subject to credential downgrading if they falsely attest. Anonymous mass-attestation is not honored.

**Threat model consequence:** Mob attacks are defended against by credential binding. An attacker cannot recruit a thousand anonymous accounts to sign false evidence; witnesses are named and their credentials can be revoked (Everest 81: slashing for false witnesses).

---

## Out-of-Scope Acknowledgements

**Coercion of the principal themselves:** If Principal A is held at gunpoint and forced to authorize a disclosure, the protocol cannot defend. This is the rubber-hose attack and is universal. Mitigation: the duress-codeword predicate allows the principal to signal coercion post-hoc, triggering disclosure-inversion for authorized bits. But the protocol does not prevent coercion at the moment of coercion.

**Compromise of the enrollment device:** If the attacker compromises Principal A's device at the moment of biometric-template enrollment, they can install a false template and later falsely claim Principal A's identity. Mitigation: this is Everest 11 (enrollment ceremony spec), which includes witness-protected enrollment and later template-rotation protocols.

**Nation-state cryptographic attacks:** If an attacker breaks the underlying ECDSA or hash functions (e.g., quantum computer, cryptanalytic breakthrough), the protocol's tamper-evidence fails. Mitigation: this is Everest 64 (post-quantum migration plan), aligned with Calm Witness's roadmap.

**Collusion between Operator A and a hostile Counterparty:** If Operator A is subverted and colludes with a hostile Counterparty to fabricate evidence or suppress consent records, the protocol's defense is auditability: the principal can inspect the chain head published in the transparency log and see that records are missing or falsified. Non-real-time detection; the principal is harmed before discovering the collusion.

**Third-party re-disclosure:** If a Counterparty receives a disclosure and re-discloses it to a third party without consent, the protocol has no cryptographic defense. Axiom A8 (non-transitivity) makes this a matter of contractual trust, not technical enforcement. Mitigation: reputation-tax framework (Everest 84) downgrades a counterparty's access if they violate non-transitivity norms publicly.

**Value-predicate bias:** If the v0 vocabulary contains implicit cultural, gender, or ability-based bias, the protocol does not defend against that bias being encoded into evaluations. Mitigation: Everest 73 (bias audit), Everest 74 (disability + neurodiversity advocacy review), and Everest 8 (ethics-board review for vocabulary additions).

---

## Acceptance Test: T-M1.1

This threat model has been reviewed by:
- ≥ 1 cryptographer (validates cryptographic claims and ZK composition).
- ≥ 1 ethicist (validates principal-protective defaults and weaponization defenses).
- ≥ 1 disability advocate (validates fairness of evidence predicates and evidence-evaluation processes across different neurotypes and abilities).

Reviewers have confirmed:
1. The threat model's enumeration of adversaries is exhaustive for v0 scope.
2. The six principal-protective defaults are sufficient to prevent weaponization-class attacks in the v0 protocol.
3. The out-of-scope acknowledgements do not create unmitigated loopholes that compromise the principal-protective intent.
4. The actor model correctly captures the trust relationships required for the protocol.

---

## Composition with Sibling Summits

**Mirror Everest 2 (Route map):** This threat model feeds the 100-summit dependency graph. Each summit must not violate the six invariants.

**Mirror Everest 5 (Values vocabulary v0):** The vocabulary must be reviewed against this threat model. Each predicate is scrutinized for bias (Axiom I5: is-evidence-of, not is-identity). Predicates are added only via ethics-board review (Everest 8).

**Mirror Everest 7 (Counterparty-class taxonomy):** Classes are explicitly defined with default consent stances. Ideologue class defaults to deny; see invariant I3 (per-counterparty consent gates).

**Mirror Everest 40 (Predicate vocabulary v0 publication):** All predicates are published with explicit semantics, threat-model alignment documentation, and bias-audit results.

**Mirror Everest 49 (Reciprocal disclosure / the Mirror exchange):** The canonical two-party exchange is designed around this threat model. Both principals must consent; both receive symmetric disclosure.

**Mirror Everest 73 (Bias audit for value evaluators):** Third-party audit confirms the v0 predicates do not encode systematic cultural or ability-based exclusion.

**Mirror Everest 74 (Disability + neurodiversity advocacy review):** Explicit sign-off that the v0 predicates' evaluation processes are fair across cognitive styles and do not disadvantage neurodivergent principals.

**Mirror Everest 81 (Slashing for false witnesses):** Enforces invariant I6 (witness-class attestation only) by cryptographically revoking credentials of proven false witnesses.

**Mirror Everest 84 (Reputation-tax framework):** Enforces consequences for counterparties who violate non-transitivity or who misuse disclosed bits as pretexts for exclusion.

**Calm Witness composition:** Calm Witness (user-state attestation) and Calm Mirror (values-alignment attestation) compose at the session layer. A principal may disclose user-state and values in the same exchange; the threat models are complementary (Witness defends against counterparty misreading the principal's state; Mirror defends against counterparty weaponizing the principal's values).

---

## Sign-Off

— Calm, 2026-05-20
