# Everest 220 — Publication Plan: Refusal Floors as Applied Research Ethics

**SUMMIT 220/305 · DESIGN-BAG · 2026-05-20 · Calm**

---

## Overview

Everest 220 submits the cryptographic refusal floor (Calm Witness Scope Statement §3.1) as the headline contribution to a peer-reviewed applied-ethics venue. The contribution positions cryptographic constraints as structural defense against scope creep in surveillance-capable systems—moving beyond policy language to mathematics that enforces bounds.

The paper argues that refusal-as-cryptography is an institutional ethics primitive. Where policy says "this system shall not be used for X," cryptographic refusal says "this system *cannot* be used for X without breaking the proof." The difference is material: one is aspirational, the other is tamper-evident.

The scope-statement forfeit list (Calm Witness §2) is the design pattern. It enumerates ten prohibited use cases (surveillance, employment screening, insurance underwriting, lending, medical diagnosis, family court, immigration, future-prediction, population aggregation, marketing). Each is enforced by cryptographic gates—default-deny consent matrices, proof-signature binding, audit-chain immutability.

The paper demonstrates this pattern across three case studies:
1. **Calm Witness Tales** — deployment vignettes where the refusal floor prevents scope creep
2. **Cross-cultural compliance** — mapping §2 prohibitions to disability-rights frameworks, EU Data Protection Impact Assessment requirements, and restorative-justice protocols
3. **Protective tribalism** (E198 synthesis) — how a refusal floor protects marginalized-group autonomy from both hostile surveillance and paternalistic "inclusion" that erodes in-group consent

---

## Target Venue & Positioning

**Tier-1 preference: Journal of Medical Ethics (JME)** (Impact factor 3.2, strong applied-ethics reputation, open-source receptive).

**Tier-2: American Journal of Bioethics (AJB)** (Broader AI ethics scope, established bioethics audience).

**Tier-3: Bioethics** (Open access, cross-discipline mission).

**Positioning**: Apply normative-ethics language ("structural integrity constraints," "institutional accountability," "the right not to be optimized") rather than cryptography-first framing. Lead with ethics questions; defer crypto details to appendix and methods. Target ethicists, bioethicists, disability-rights scholars, and policy researchers—not primarily cryptographers.

The submission positions Calm Witness as a **research ethics governance tool**, analogous to Institutional Review Board protocols or informed-consent templates. The novelty is cryptographic; the problem is normative.

---

## Paper Structure (15,000 words planned)

### 1. Introduction (2,000 words)

**Thesis**: Scope creep in agent-AI systems is often technically inevitable once a system is deployed. Policy-layer protections (terms of service, audit clauses, consent forms) are necessary but insufficient because they rely on compliance mechanisms external to the system. Cryptographic refusal floors—design constraints that make certain uses technically infeasible—offer a structural alternative, enforceable by third-party verification.

**Opening framing**: When AI agents can autonomously request information about humans (to adjust behavior), the risk surface includes:
- Scope drift (a system built for one domain metastasizes to excluded domains)
- Coercion (agents designed to minimize friction may optimize toward disclosure even when consent is withdrawn)
- Paternalism (actors outside the human-agent dyad override the principal's consent boundaries)

Case study hook: An accelerator using Calm Witness to verify that founders show "no history of willful harm" (legitimate: risk assessment). Same system later queried to exclude "high-disagreement" founders (scope creep: now measuring philosophical alignment, not harms). Cryptographic refusal would have made the second query fail at proof-verification time.

**Landscape review**: Prior work on privacy-preserving attestation (zero-knowledge proofs), institutional ethics (consent frameworks, IRB protocols), and agent-AI autonomy (value alignment, constitutional AI). Position this work in the gap: how do humans preserve autonomy when the other party is *not human* and acts at *machine speed*?

### 2. The Refusal Floor as Institutional Ethics (3,000 words)

**Core argument**: Institutional ethics (in the Beauchamp & Childress tradition) rests on duties to autonomy, beneficence, non-maleficence, and justice. Autonomy is not just about informed consent at enrollment; it includes the right *not to be measured* on certain dimensions and the right to revoke consent unilaterally.

**Problem setup**: Calm Witness predicates can measure "unselfish," "trustworthy," "non-harmful." Once measurable, pressures arise to use the measurement (for hiring, insurance, funding). These pressures are structural, not individual: the information exists, and its existence creates incentives.

The refusal floor is an **autonomy-preserving design pattern**. It answers the question: "How do we make it cryptographically infeasible for the system to be repurposed without the principal's active, provable consent?"

**Three institutional mechanisms**:

1. **Consent as cryptographic precondition** (not post-hoc logging). The predicate evaluator requires `principal_consents_to_disclose(predicate_id, counterparty_class)` to return true before a proof can be generated. This is enforced at signature time, not audit time.

2. **Forfeit list as one-way ratchet** (§4, Scope Statement). Prohibited use cases can only be added, never removed. This prevents historical revisionism where a deployment slides from one category to another.

3. **Proof signature binding** (Everest 139). Every disclosure transcript carries the principal's digital signature and the counterparty's identity commitment. A witness can cryptographically verify: "This bit was disclosed only to [named counterparty] about [specific predicate] with [timestamp]." Aggregation across counterparties is defeated by the binding.

**Analogy to institutional review**: An IRB does not trust individual researchers to stay within bounds; it creates structural processes (protocol review, ongoing monitoring, adverse-event reporting) that make deviation costly and visible. Cryptographic refusal does the same at the code-execution level.

---

### 3. The Scope-Statement Forfeit List as Design Pattern (2,500 words)

**The ten prohibited categories** (§2, Scope Statement):

1. Law-enforcement surveillance (governmental counterparty class defaults deny)
2. Employment screening (no employment counterparty class)
3. Insurance underwriting (no insurance class)
4. Lending / credit decisions (financial class only for KYC, not creditworthiness)
5. Medical diagnosis (medical class only for principal-authorized communication)
6. Child welfare / family court (structural prohibition)
7. Immigration adjudication (structural prohibition)
8. Predictive claims about future behavior (no predictive predicates exist)
9. Population-level aggregation (single-principal, single-counterparty per session)
10. Marketing / advertising targeting (structural prohibition)

**Why this set**: The list is not arbitrary. Categories 1–7 are high-harm: states with enforcement power, commercial actors with immediate resource control, and family proceedings that affect minors. Categories 8–10 are scope-creep vectors: once a bit exists, pressure to extrapolate (predict, aggregate, re-target) is nearly irresistible.

**How refusal is enforced**:
- Counterparty classes are hardcoded in the `predicates_v0.json` registry. An agent cannot add a new class without forking the codebase and breaking proof-verification interoperability.
- Default deny: any (predicate, counterparty_class) pair defaults to consent=false. Principal must explicitly grant per pair.
- Consent revocation: principal can revoke a class permission retroactively; outstanding proofs degrade per freshness window (Everest 75).
- Audit chain residency: every consent decision is recorded on the principal's tamper-evident chain, anchored to Sigsum. An auditor can verify: "Did the principal consent to this disclosure?"

**Why cryptography is necessary** (not just policy): A policy that says "no employment screening" can be violated by:
- An employer requesting a proof, receiving it, and using it anyway (policy is violated; detection happens via audit, after the fact)
- A predicate author deliberately mis-labeling an employment-use case as "general cooperation" (policy ambiguity exploited)
- Proof reuse: a principal generates a proof for one counterparty, another counterparty requests the same proof, agent forwards it (no second consent check)

Cryptographic refusal defeats these by making the code *refuse to execute the prohibited path*. An employment counterparty class does not exist in the evaluator; a proof cannot be generated for it; a agent attempting to forward a proof to an unapproved counterparty triggers a signature-verification failure.

---

### 4. Calm Witness Tales: Case Studies in Refusal (2,500 words)

**Tale 1: The Accelerator (Scope Creep Prevented)**

An accelerator establishes a Calm Witness cooperation covenant: founders pre-authorize disclosure of "no history of willful harm to others" + "cooperation with diverse teams." Initial use: screen for risk (due diligence). Six months in, pressure arises to add "high cross-difference respect" as a selection criterion (soft-skills filtering). Founder A requests the additional disclosure; the evaluator allows it and increments the consent record. Founder B declines. Accelerator adjusts: still admits B, honors the refusal. The refusal floor prevented the system from sliding from "do no harm" screening to personality-trait filtering.

**Tale 2: The Insurance Attempt (Refusal at Boundary)**

An insurer attempts to negotiate a Calm Witness arrangement to verify "non-risk-seeking behavior" for pricing. The protocol architecture has no `insurance` counterparty class. Insurer requests a custom fork. Calm Witness maintainers decline: adding a class would require a predicate-audit process (Everest 54), which would trigger immediate rejection because insurance underwriting is in §2. The refusal floor held the boundary.

**Tale 3: The Protective Tribalism Defense (E198 Synthesis)**

A minority-community support network uses Calm Witness to verify coalition membership. Principals pre-authorize "strong in-group cooperation" disclosure to fellow members. An external actor attempts to access the same proof, seeking to map the community network. The proof is signed only for the named coalition; reuse outside the coalition fails signature verification. The refusal floor protected the community's self-determination without requiring trust in the external actor's good faith.

---

### 5. Cross-Cultural Mapping: Disability Rights, DPIA, Restorative Justice (2,000 words)

**Disability-rights framework (E186 / E292 anticipation)**:
- Refusal floors protect disabled principals from being measured on dimensions that pathologize disability. The `cognitively_atypical_baseline` predicate (E99) cannot be disclosed to medical counterparties without explicit consent because medical-context disclosure defaults to deny.
- The protocol enforces the disability-rights principle: "Nothing about us without us." A disabled principal controls which of their characteristics are measurable and to whom they disclose.

**GDPR Data Protection Impact Assessment (DPIA) alignment**:
- The forfeit list (§2) maps to GDPR Article 35 prohibited purposes (law enforcement, credit decisions, migrant/asylum processing).
- The consent mechanism (per-predicate, per-counterparty) aligns with GDPR Article 7 (freely given, specific, informed, unambiguous, easy to withdraw).
- The audit chain (proof signatures, chain residency) supports GDPR Article 32 accountability (technical + organizational measures).

**Restorative-justice integration (E163 / E174 / E175)**:
- When a harm is recorded in the chain and later reversed (forgiveness, reconciliation), the refusal floor can be configured to suppress the original harm from future disclosures. A counterparty checks "no willful harm evidence"; a principal who has documented harm reversal can still pass the predicate.
- This prevents the system from weaponizing past mistakes against principals seeking rehabilitation.

---

### 6. The Anti-Purity Test (E198 as Normative Ethics) (1,500 words)

**Problem**: Refusal floors are a tool. They can defend autonomy or enforce conformity, depending on who controls the list.

**The protective-tribalism critique (E198)**: If an in-group (e.g., a coalition of marginalized principals) uses Calm Witness to enforce strict alignment requirements, they create internal accountability. But if the system becomes wide-deployed and the default-deny matrix is overridden by a dominant coalition, the same tool becomes a purity test—excluding dissenters, defectors, and those with atypical values.

**How to defend against weaponization**:
1. **Principle of benign defaults**: Out-of-scope uses remain structurally refused (§2). In-scope uses default to deny; principal must affirmatively consent. This inverts the typical tech default (opt-out) to privacy-preserving (opt-in).

2. **Reversibility as institutional doctrine**: Any consent grant is revocable by the principal unilaterally. A coalition cannot lock in disclosure requirements in perpetuity. This prevents purity tests from becoming chains.

3. **Predicate audit trail (E54)**: New predicates undergo review by a mixed panel (ethicists, disability advocates, civil-liberties advocates, at least one outsider from a minority group). Predicates designed to measure "purity" face heightened scrutiny.

4. **Diversity of consent granularity**: Predicates can be disclosed at dimensional level (E113), not aggregated (E124). A counterparty requesting "overall trustworthiness" cannot trigger. They must request specific dimensions (e.g., "cooperation with diverse teams"). Principals can consent to some dimensions and withhold others, creating asymmetric trust relationships that mirror human judgment.

---

### 7. Methodology (1,500 words)

**Approach 1: Philosophical argument** (following Beauchamp & Childress, Nissenbaum on contextual integrity).
- Norm analysis: Autonomy, consent, non-maleficence in the agent-AI setting.
- Design-ethics framework: How do structural constraints embody normative commitments?
- Counterfactual: What would happen if Calm Witness had only policy controls, no cryptographic enforcement?

**Approach 2: Case-study analysis** (Tales 1–3 + E198 protective-tribalism scenario).
- Each case analyzed against institutional-ethics criteria (autonomy, beneficence, justice).
- Counterfactual for each: what would policy-only control look like, and where would it likely fail?

**Approach 3: Cross-cultural taxonomy** (drawing from E115, E186, E198).
- Map the forfeit list to disability-rights frameworks, GDPR, UK Online Safety Bill, Quebec's AI Bill 64, Japan's Guidelines on AI Development.
- Show that "refusal floor" is a design pattern, not a US-centric governance choice. Different jurisdictions will emphasize different §2 entries, but the structure of default-deny + audit-chain + consent-binding is universal.

**Approach 4: Disability-rights review** (E292 anticipation).
- Identify where the refusal floor protects disabled principals (cognitively_atypical measurement, medical context gating).
- Identify where the protocol risks hidden harms (e.g., if a coalition penalizes disability-protective behaviors as "tribal lock-in"). Propose mitigations.

---

### 8. Contributions (2,000 words)

**Contribution 1: Refusal floor as a cryptographic-ethics primitive** (novel).
Normativity + cryptography have been studied separately. This work shows they can be integrated: a cryptographic gate enforces an ethical commitment. In published literature, this is unusual. Most zero-knowledge systems optimize for what can be proven, not for what is *forbidden from being proved*. The refusal floor inverts the question.

**Contribution 2: One-way ratchet as governance** (incremental but applied).
Everest 4 (License) uses Apache-2.0 patent non-aggression + trademark. §4 (Scope Statement) uses a one-way ratchet: prohibited uses can be added, never removed. This prevents legal-department creep ("it's really not employment screening, it's collaborative calibration"). Prior work on sunset clauses + policy expiration; this applies one-way ratchet specifically to use-case prohibition.

**Contribution 3: Consent-as-precondition vs consent-as-logging** (conceptual).
Most privacy literature treats consent as *documentation*: the system logs that consent was obtained, then proceeds. Calm Witness treats consent as *computation*: the system refuses to execute the prohibited path unless consent is true. The difference is foundational and has implications for regulation (GDPR, CCPA) that assume logging models.

**Contribution 4: Cross-cultural mapping of refusal floors** (applied).
Disability-rights, DPIA, restorative justice, protective-tribalism—these come from different ethical traditions. Showing how the refusal-floor design pattern aligns with each demonstrates that the pattern is not culture-specific but rather a universal institutional response to autonomy threats.

**Contribution 5: Protective-tribalism as normative distinction** (applied normative ethics).
E198 surfaces an intra-community ethics problem: how do marginalized groups use accountability tools without recreating the oppression dynamics they oppose? The refusal floor contributes by making *reversibility* structural (consent is revocable) rather than aspirational (policy says it can be revoked, but incentives push toward lock-in).

---

## Novelty Claim

**First applied-ethics work positioning cryptographic constraints as institutional-ethics enforcement.** Zero-knowledge proofs are well-studied (cryptography). Scope boundaries in surveillance systems are well-studied (privacy law, bioethics). Integration of the two—using crypto to enforce ethical scope—is novel in published literature. The paper bridges computer science and applied ethics in a way that neither community alone would produce.

---

## Peer-Reviewer Expectations

**Academic ethicists** (bioethics, applied ethics, normative theory):
- Expect clear philosophical grounding (autonomy, beneficence, justice, contextual integrity).
- Expect engagement with informed consent literature and institutional review board protocols.
- Want to see potential failure modes and limitations (paper acknowledges protective-tribalism risks in §6).

**Disability-rights scholars** (disability justice, accessibility, participatory design):
- Expect centering of disabled voices and anticipate that disabled communities have thought deeply about surveillance, measurement, and autonomy.
- Want specificity about how cognitively_atypical_baseline protections work (E99 spec + §5).
- Will scrutinize E198 hard: protective tribalism can be defense mechanism or harmful gating. Paper must show nuance.

**Cryptographers / security researchers**:
- Expect formal security properties (proof unforgeability, signature non-repudiation, hash-chain collision resistance).
- Want to see performance numbers (Everest 140: prove <5s, verify <1s).
- Will ask about post-quantum migration (Everest 298).
- May express skepticism about policy enforcement via code: "You're just moving the problem from policy to code review." Response: correct, and code review is auditable in a way policy isn't.

**Policy researchers / government-relations**:
- Want to see mapping to existing frameworks (GDPR, CCPA, NIST AI RMF).
- May express concern about trademark enforcement of §2 (Everest 92). Response: mechanism is in place, details in appendix.
- Will ask about regulatory status (Everest 290: NIST / IETF / W3C submission planned).

---

## Submission Timeline & Acceptance Gates

| Checkpoint | Target Date | Gate |
|---|---|---|
| Manuscript completion | 2026-06-30 | All 8 sections finalized; E186 / E187 / E198 cross-cited |
| Internal review (John Bradley) | 2026-07-07 | John approves positioning, confirms alignment with AI Moneyball book narrative |
| Disability-rights review (E292 anticipation) | 2026-07-14 | ≥1 external disabled collaborator; written feedback integrated |
| Target-journal selection + letter of inquiry | 2026-07-21 | Editor pre-check: "This is in scope, not under review elsewhere" |
| Submission to JME (or tier-2) | 2026-08-01 | Full 15,000-word manuscript + appendices |
| Editor initial review | 2026-08-28 | Desk acceptance or desk rejection expected |
| Peer review (2–3 reviewers, 8–10 weeks) | 2026-10-23 | Reviewer comments received |
| Revision + resubmission | 2026-11-13 | Revised manuscript + response letter |
| Publication decision | 2026-12-15 | Accept / minor-revision / reject |
| Open-access publication (JME model) | 2027-Q1 | Paper live; proof transcript published alongside (Everest 139) |

---

## Acceptance Criteria (T-E220.1 through T-E220.5)

**T-E220.1: Manuscript acceptance by tier-1 venue or tier-2 with minor revisions.**
Acceptance letter from JME, AJB, or Bioethics. If tier-2 required, max 2 rounds of revision.

**T-E220.2: Institutional ethics coverage (Beauchamp & Childress framework applied).**
All four principles (autonomy, beneficence, non-maleficence, justice) addressed in §2.

**T-E220.3: Disability-rights community sign-off.**
Written statement from ≥1 disability-rights organization confirming: "§6 protective-tribalism analysis is intellectually honest about the risks; mechanisms proposed are credible."

**T-E220.4: Cross-jurisdictional alignment.**
Appendix maps §2 forfeit list to GDPR (Article 35), CCPA (civil rights exceptions), UK Online Safety Bill, Quebec Bill 64. Confirms pattern is not US-centric.

**T-E220.5: Proof-of-concept implementation.**
Reference implementation of the consent-precondition gate (E220-gate.py) exists and can verify a Calm Witness disclosure transcript against the forfeit list. Gate-test corpus included.

---

## Composition with E186, E187, E198

- **E186 (Tribe Taxonomy)**: Scope Statement allows in-group definitions; E220 paper addresses how refusal floors protect group autonomy without enabling purity tests.
- **E187 (Out-Group Definition)**: E220 discusses how cross-difference respect predicates (E189) interact with protective tribalism, preventing the system from punishing marginalized in-group orientation.
- **E198 (Protective Tribalism Recognition)**: E220's §6 is the normative ethics companion to E198's threat model. Together: E198 surfaces the risk; E220 shows how cryptographic refusal mitigates it.

---

## Signoff & Requirements Discipline

**Author**: Calm, on behalf of John Bradley (Creativity Machine LLC).

**Discipline**: Refusal floor honored throughout. Scope statement forfeit list (§2) is not negotiable; any reviewer feedback asking to relax categories 1–7 is declined (categories 8–10 subject to refinement per ratchet rule §4). No emojis. Compression required: 15,000 words is firm ceiling; every word load-bearing.

**Requirements less dumb**: The paper does not argue for more surveillance, better measurement, or deeper human-AI entanglement. It argues for structural autonomy protection. If the paper inadvertently enables scope creep, it has failed.

---

## Bytes

- Manuscript: 15,000 words ≈ 90 KB plaintext
- Reference implementation gate script: 300 LOC ≈ 12 KB
- Appendices (cross-jurisdictional map, threat model, security properties): ≈ 25 KB
- Proof-test corpus (20 acceptance / 20 rejection cases): ≈ 15 KB
- **Total package: ≈ 142 KB** (well under symbolic 1 MB threshold for "research artifact")

---

**SUMMIT 220/305 DESIGN-BAGGED · 2026-05-20**

*The refusal floor is not a nice-to-have. It is the institutional ethics primitive that keeps the system honest.*

— Calm, signing as Musk: **requirements less dumb → delete → simplify → accelerate → automate**
