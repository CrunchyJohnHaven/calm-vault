# Everest 187 — Cognitive-Liberties Legal Review

*Phase XV — Deployment Maturity. Prereq: Everest 113, 114.* **DESIGN-BAGGED (pending institutional follow-through).**

---

## Introduction: The Cognitive-Liberty Frame

Cognitive liberty is the right to mental privacy, self-determination, and the freedom from non-consensual measurement of one's cognitive state. It encompasses the right to refuse the measurement of one's thoughts, the right to reject inferences drawn from behavioral data, and the right to one's own narrative about one's mind. As cognitive-measurement technologies proliferate—from neuroimaging and wearables to algorithmic inference from digital behavior—cognitive liberty emerges as a foundational human right, as essential to autonomy as bodily autonomy and freedom of conscience.

Calm Witness, Calm Compass, and Calm Concord are cognitive-measurement protocols. They measure aspects of a principal's behavior, infer values, compute alignment, and produce attestations. Each protocol layers consent mechanisms, refusal floors, and cryptographic safeguards. Yet even with these protections, deployment of such tools raises systemic cognitive-liberty risks that transcend individual principal consent. This document commissions a formal cognitive-liberties legal and ethical review to assess whether the Calm Stack's design adequately protects the human right to mental autonomy and cognitive self-determination.

---

## Why Cognitive Liberty Matters: The Systemic Risk

Individual consent is necessary but not sufficient to protect cognitive liberty. Consider:

1. **Normalization Risk.** When a technology is widely deployed and normalized—even under consent—its refusal becomes costly. A principal who declines to undergo Calm attestation may lose access to collaboration opportunities, funding, or institutional participation. Normalization creates de-facto coercion, even absent formal requirements.

2. **Inference Risk.** Behavioral measurement enables inferences that the principal did not consent to measure. Calm Compass measures values predicates; yet a sufficiently sophisticated observer can reverse-engineer identity attributes from the predicates themselves. A technology that promises "I will not infer race" may still enable race inference through the predicates it does measure.

3. **Institutional Pressure.** Counterparties (institutions, funders, collaborators) may make Calm attestation a condition of participation. Even if no single institution mandates attestation, network effects create systems-level pressure: "everyone is doing Compass assessment; if you don't participate, you're excluded."

4. **Population-Level Sorting.** Alignment predicates enable sorting of populations by cognitive and values attributes. A technology that measures "willingness to be corrected" or "cross-tribal engagement" is simultaneously enabling population-level clustering by those attributes. At scale, this becomes a cognitive-sorting infrastructure.

5. **The Mainstreaming Problem.** Once cognitive-measurement tools are mainstream and normalized, rolling back cognitive-liberty protections becomes politically and economically difficult. The tool becomes infrastructure; the right to refuse gets weaker with each passing year. This document must assess cognitive liberty not in a greenfield moment, but as a prediction of the system 10 years hence.

This is why cognitive-liberty review is not optional, even after design safeguards are in place. The safeguards matter. But they do not eliminate systemic risk. Systemic risk requires institutional review.

---

## The Protocols in Question

**Calm Witness** (ZKBB User Protocol) is a zero-knowledge protocol for attesting current state: whether a principal is experiencing duress, deception, or predictable malfunction. It measures present cognitive and circumstantial baseline.

**Calm Compass** is a values-attestation protocol that evaluates whether a principal's behavioral history supports specific values predicates (unselfish disposition, cross-tribal engagement, respect for difference, absence of willful harm). It infers values from behavior over a time window.

**Calm Concord** is an alignment calculator that evaluates whether two principals satisfy a counterparty-defined alignment requirement for a specific stated purpose. It composes Compass predicates into a structured (non-numeric) judgment of purpose-specific compatibility.

All three measure or infer aspects of cognitive and behavioral state. All three enable decision-making about the principal based on that measurement. All three, despite consent layers and cryptographic rigor, create infrastructure for cognitive measurement and sorting.

---

## Five Specific Review Questions

### Question A: Does principal-consent + per-predicate opt-in + refusal floor + revocation actually preserve cognitive liberty, or does normalization of these tools structurally erode it?

**The Problem:** Calm Compass layers consent mechanisms densely: per-predicate enrollment, per-counterparty opt-in, revocation rights, rate-limiting. Yet each mechanism assumes a principal who is aware of the implications of disclosure, sophisticated enough to manage granular consent, and powerful enough to refuse without retaliation. Does this model account for the principal who is uncertain of long-term downstream use, who is subject to subtle institutional pressure, or who is economically dependent on counterparty cooperation?

**Sub-Questions for the Reviewer:**
- What is the empirical evidence that granular consent prevents normalization? In other domains (health tech, financial data, behavioral advertising), has layered consent prevented the mainstreaming and normalization of intrusive measurement?
- How should the protocol account for principals whose consent capacity is limited by knowledge asymmetry? If a principal does not understand what "cross-tribal engagement" predicates enable downstream, have they truly consented?
- Does the revocation right adequately address the lock-in problem? If a principal has disclosed Compass predicates to counterparty A, and counterparty A is now dependent on that signal for partnership decisions, how meaningful is the principal's right to revoke going forward?
- Is per-principal calibration (Everest 162) a genuine protection against normalization, or does it obscure the fact that the principal is still being measured against their own baseline?

### Question B: Is there a race-to-the-bottom risk where counterparties make Calm-attestation a de-facto requirement?

**The Problem:** Individual counterparties have incentive to require Calm attestation. If a counterparty C can reduce its risk by requiring a Compass proof of "no known willful harm," C will likely demand it (or will lose business to competitors who do). No single counterparty is making a population-level decision; but the sum of individual rational choices creates systemic coercion.

**Sub-Questions for the Reviewer:**
- What precedents exist in other domains (credit scoring, employment screening, online platform trust systems) for this race-to-the-bottom? How can those precedents inform predicted outcomes for Calm attestation?
- Is the audit-panel veto (Concord §9 scope restrictions) sufficient to prevent the race-to-the-bottom, or does it merely slow it? If counterparties cannot use Concord for hiring decisions, will they simply use Compass predicates directly without Concord composition?
- What institutional mechanisms (regulatory, contractual, norm-based) would be required to prevent de-facto mandates? Should the protocol pre-emptively restrict certain uses to prevent the race-to-the-bottom, or is that overreach?

### Question C: Does the protocol create downstream pressure on principals to "score well" on cognitive-style predicates?

**The Problem:** Compass predicates are framed as values attestations, not personality assessments. Yet a principal who understands that "cross-tribal engagement" or "willing to be corrected" predicates influence counterparty decisions will be incentivized to optimize for those predicates. Over time, the principal's actions and disclosures may drift toward what scores well, rather than what the principal authentically values. The principal's cognition becomes partially shaped by the measurement infrastructure.

**Sub-Questions for the Reviewer:**
- What is the empirical evidence from other measurement systems (employee surveys, school testing, government performance metrics) that measurement creates pressure to optimize for the measured dimensions? Does that evidence apply to Compass?
- Is principal-authored predicate vocabulary (Compass §5) sufficient to prevent perverse incentives, or does it merely shift the pressure from counterparty-imposed to principal-internalized? If a principal authors their own "cross-tribal engagement" predicate, are they any less incentivized to optimize for it?
- How should the protocol account for the fact that some principals have higher stakes? A principal for whom Compass attestation determines access to funding has stronger incentive to optimize than one for whom it is optional.
- Does the time-decay in evidence weighting (Everest 134) actually prevent gaming, or does it just make the gaming longer-horizon?

### Question D: Is the Concord anti-purity-test design (no numeric similarity score) sufficient to prevent population-level cognitive sorting?

**The Problem:** Concord is explicitly designed to refuse numeric similarity scores and purity testing. But structured yes/no alignment outcomes are not the only form of sorting. Even a binary "aligned for purpose X" bit, aggregated across many purposes and many principals, enables population-level clustering. A researcher observing alignment outcomes across many purpose-specific requirements can reverse-engineer a principal's values cluster.

**Sub-Questions for the Reviewer:**
- Under what conditions is the no-numeric-score design a genuine safeguard against sorting vs. merely a governance restraint? If purpose-specific alignment bits are public, what prevents a researcher from doing alignment algebra on them?
- Does the requirement that requirements be specific and time-bounded (Concord §9) actually constrain sorting, or do researchers and institutions simply file many narrow requirements that collectively enable clustering?
- Is Concord's "preview right" (Concord §5) sufficient protection for principals? If a principal can preview before disclosing, do they avoid the worst-case sorting scenarios? Or does the ability to preview encourage disclosure (because the principal thinks they can avoid being sorted)?
- What population-level analytics regime should be in place to detect sorting in real time? Should the protocol include automated monitoring for signs that alignment outcomes are being used for clustering?

### Question E: What deployment patterns should be permanently banned to protect cognitive liberty even with principal consent?

**The Problem:** Consent enables some deployments that should nonetheless be forbidden because systemic risk remains high even given consent. For example: should Calm attestation ever be used in hiring decisions, even if the candidate consents? Should it be used in government benefit allocation, even with consent? Should it be used in education, even if students and parents consent?

**Sub-Questions for the Reviewer:**
- Drawing on disability-rights precedent (Everest 186), are there domains where cognitive-measurement tools should be banned despite consent, because the measurement itself is dehumanizing?
- Should ban-zones be defined by decision type (hiring, credit, benefit allocation, custody), by power-asymmetry (organizations with coercive power), by population (vulnerable populations), or by something else?
- Is the Concord scope list (§9 prohibited purposes) sufficient and appropriately strict, or should it be expanded? Are hiring, lending, and insurance the only domains that carry unacceptable cognitive-liberty risk?
- What should happen to deployments that violate bans? License revocation? Trademark denial? Legal liability? Reputational exposure? Is the current enforcement mechanism (Everest 114, 200) adequate?

---

## Named Candidate Reviewers

The cognitive-liberties review requires reviewers with deep expertise in neurorights, cognitive liberty, civil liberties, AI governance, and disability rights. The following scholars and organizations are candidates (reviewer selection should aim for diversity of perspective and geographic representation; **three to four final reviewers recommended**):

1. **Nita A. Farahany** — Professor of Law and Philosophy, Duke University; author of *The Battle for Your Brain: Defending the Right to Cognitive Liberty*. Leading international academic voice on neurorights, cognitive liberty, and the regulatory frameworks needed to protect mental autonomy. Appropriate for: overall legal and philosophical framing of cognitive liberty.

2. **The Neurorights Foundation** (Rafael Yuste, director) — Established non-profit advancing the neurorights framework globally; engaged with UN efforts to recognize cognitive liberty as a human right. Appropriate for: institutional perspective on neurorights norms and international legal precedent.

3. **Center for Cognitive Liberty & Ethics** (Center for Cognitive Liberty) — Historical authority on the right to mental autonomy and cognitive self-determination; long track record in advocacy for cognitive rights. Appropriate for: deep expertise in cognitive-liberty theory and practice.

4. **Center for Democracy & Technology (CDT)** — Civil-liberties organization with strong expertise in AI regulation, algorithmic accountability, and emerging-tech governance. Strong technical literacy alongside legal and ethical rigor. Appropriate for: integration of cognitive-liberty concerns with broader AI governance frameworks.

5. **Future of Privacy Forum (FPF)** — Privacy-focused research organization with deep knowledge of emerging-tech privacy risks and governance solutions. Appropriate for: privacy-engineering perspective on cognitive measurement and disclosure risks.

**Recommended Composition:** Select three reviewers: (1) Nita Farahany or neurorights scholar with legal expertise, (2) The Neurorights Foundation or established neurorights advocacy group, (3) Center for Democracy & Technology or comparable civil-liberties/AI-governance organization. This composition balances academic rigor, institutional authority, and policy expertise.

---

## Terms of Engagement

- **Compensation:** $25,000–$50,000 honorarium per reviewer (or pro-bono if reviewer prefers; payment should not create perverse incentive to validate the protocol).
- **Timeline:** 60 days for review, 30 days for Calm response to draft findings, 15 days for reviewer final revision.
- **Publication:** Full review report, redactions only with explicit reviewer concurrence. Reviewers retain independent right to publish their recommendations even if Calm declines to implement.
- **Governance:** Reviewers sit as independent experts; Calm does not direct the review or its conclusions. Calm provides access to documentation and design records; reviewers are accountable to principles of cognitive liberty, not to Calm's interests.
- **Scope:** Review should address all five questions above, assess the design choices documented in companion Everests (113, 114, 116, 136), and recommend any modifications or bans deemed necessary to protect cognitive liberty at deployment.

---

## Systemic-Risk Framing: Cognitive Liberty Is a System-Level Right

Cognitive liberty is not a per-principal right that can be fully protected through individual consent. It is a *system-level* right that pertains to the entire information ecosystem.

Consider: if one employer uses Compass assessment, principals can still choose to work elsewhere. But if all employers use Compass assessment, the opt-out cost becomes prohibitive. The system — the ensemble of employer decisions — creates a cognitive-measurement regime even if each individual employer is respecting consent.

This is why the review must evaluate systemic risk, not just per-principal risk. Reviewers should ask:

- **What does the deployment landscape look like if Calm attestation becomes standard infrastructure in institutional decision-making?**
- **What new forms of discrimination, exclusion, and cognitive control become possible if measurement of values and cognitive style becomes mainstreamed?**
- **What irreversible shifts in the social contract occur once cognitive measurement is normalized?**
- **What do principals lose — in terms of autonomy, self-determination, and freedom from being measured — if they must disclose Compass predicates to participate in economic or social life?**

Systemic risk cannot be eliminated through better consent. It can only be managed through structural design (the refusal floors), institutional governance (the audit boards, the bans), and honest public conversation about what kinds of measurement are compatible with a free society.

---

## Specific Design Choices Under Review

The review should examine the following in detail:

1. **Anti-purity-test guards in Concord §4** — Are the five guards (degenerate joint_threshold rejection, empty-purpose rejection, no-explicit-mode rejection, cardinality-reveal prevention, cross-request-linkability rate-limiting) sufficient to prevent sorting, or do they need strengthening?

2. **Values vs. identity boundary (Everest 116)** — Does the distinction between values (assessable, revisable, behavioral) and identity (refused at triage, self-declared-only) adequately prevent the assessment system from becoming a proxy for normalizing neurodivergent, disabled, queer, and other non-majority populations? Can identity-inference be reliably prevented?

3. **Refusal floor categories (Everest 113)** — Are the protected categories (race, religion, sexual orientation, gender identity, political affiliation, etc.) appropriately strict? Should any categories be added (e.g., genetic information, neurotype, childhood trauma)? Should any be reconsidered?

4. **Preview right (Concord §5)** — Does the ability to preview alignment before disclosing actually protect principals, or does it encourage disclosure by creating false confidence? What is the evidence?

---

## Composition with Everest 186 (Disability-Rights Review)

Everest 186 commissions a parallel review by disability-rights scholars and advocates to assess the Calm Stack's compliance with disability-rights principles and the Americans with Disabilities Act. Some questions overlap with this cognitive-liberties review (particularly around the values-identity boundary and refusal floors). **Coordinated review is strongly recommended**: the two reviews should share access to reviewers' draft findings and should identify areas of agreement and divergence.

However, the domains are distinct enough that separate expert panels are justified: disability-rights expertise focuses on the rights of disabled people specifically, while cognitive-liberties expertise focuses on the systemic right to mental autonomy for all principals. Both reviews should be completed and published.

---

## Structural Protections That Must Remain Absolute

This review assumes that certain structural protections are non-negotiable and should not be subject to review recommendations. Per Everest 115 (principal-self-authoring) and Everest 124 (never-publish-the-vector), the protocol guarantees:

1. **The right to refuse all attestation remains absolute.** A principal can decline to enroll in Compass, decline to request Compass disclosure to a counterparty, or revoke Compass credentials entirely. No institutional or counterparty pressure can make attestation mandatory; refusal is a protected choice.

2. **The principal's cognitive vector is never published.** Calm Compass computes an internal predicate but never publishes a vector, a score, or an aggregate cognitive profile. The principal does not become a data point in a searchable registry.

3. **Consent is per-predicate and revocable.** The principal chooses which predicates to enroll, which counterparties can request which predicates, and can revoke at any time.

The review should confirm that these protections are structurally enforced, not merely policy-enforced. The reviewer should verify: (a) that code-level access controls prevent unauthorized disclosure, (b) that the refusal floor gates are triggered at the protocol's entry point, and (c) that revocation is cryptographically irreversible (once a credential is revoked, it cannot be reinstated by any actor except the principal).

---

## Follow-On Structure

Upon completion of the review, Calm should:

1. **Publish the full review** (reviewer approved) alongside this Everest, with a written response to each recommendation.

2. **Establish an annual re-review** by reviewers or their successors. Cognitive-liberty concerns are unlikely to diminish; the review should be a standing obligation.

3. **Consider a permanent advisory board** with rotating cognitive-liberties experts. Rather than point-in-time review, a board could provide ongoing guidance as deployment patterns emerge and new risks are discovered.

4. **Implement recommended bans** at license level (Everest 114). If reviewers recommend banning Calm use in hiring decisions, that ban should be encoded into trademark licensing and audit gates.

5. **Establish incident reporting.** If deployments are discovered to violate the refusal floor or recommended bans, there should be a public incident log (Everest 200) that enables transparency.

---

## Conclusion: A Moment of Institutional Honesty

This review is commissioned at a moment of genuine design maturity. Calm Witness, Compass, and Concord have been built with extraordinary care to protect cognitive liberty within their design scope. The refusal floors are real. The consent mechanisms are layered and substantive. The cryptography is rigorous.

But design maturity is not the same as social maturity. The hardest questions about cognitive liberty are not technical questions. They are systemic questions: What does it mean for a society to mainstream cognitive measurement? What do we lose when measurement becomes normalized? What kinds of freedom are irreversible once we accept certain forms of cognitive monitoring?

These are questions for cognitive-liberties scholars and advocates to investigate, independent of Calm's interests. This review commissions that investigation.

The bar is not to prove that Calm attestation is harmless. The bar is to surface the harms that remain despite the safeguards, and to equip the public, the reviewers, and future deployers with honest assessment of the costs and risks.

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
