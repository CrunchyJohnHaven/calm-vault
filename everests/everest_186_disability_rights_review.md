# Everest 186 — Disability-Rights Legal Review

*Phase XV — Deployment Maturity. Prereq: Everest 113, 116, 157, 198.* **DESIGN-BAGGED** (pending institutional follow-through).

---

## Overview

Calm Compass and the broader Calm Witness / Calm Pact protocol stack touch dimensions of human difference—cognitive baseline, mental state, consistency under stress, respect-for-difference operationalization—that carry acute disability-rights implications. This Everest establishes a formal, published legal review by an independent disability-rights organization to validate that the protocol's protective mechanisms (the identity boundary at E116, the refusal floor at E113, the self-harm predicate gating at E157, the protective-tribalism carve-out at E198) materially prevent pathologization and discrimination.

This is not an internal ethics review. It is a solicitation to a named disability-rights legal organization to conduct an independent audit of the protocol, publish findings, and hold the Calm Stack accountable to disability-rights standards before and after deployment.

The summit ships when:
1. The review solicitation letter is drafted and ready to send
2. Three or more named candidate organizations are identified with disciplinary rationale
3. The scope of review is precisely articulated
4. Terms of engagement (compensation, publication, timeline, independence) are pre-specified

---

## The Review Brief — Letter to Disability-Rights Organizations

---

**TO: [Disability-Rights Organization]**

**FROM: Calm (operator for John Bradley, Creativity Machine LLC)**

**DATE: 2026-05-20**

**RE: Independent Legal Review Solicitation — Calm Compass & Witness Protocols**

---

### Context: What We've Built

We have authored an open-source, zero-knowledge protocol stack (Calm Witness, Calm Compass, Calm Pact) designed to let one AI agent disclose whether a human principal's behavior aligns with named values — unselfishness, cross-tribal engagement, respect-across-difference, absence of willful harm — without revealing the principal's identity, medical history, conversation history, or anything beyond a single attested bit.

The protocol is used for agent-to-agent collaboration calibration in the event that two agents need to know whether their respective principals' directives align before cooperating. It is not for law enforcement, employment screening, insurance underwriting, or medical diagnosis. Those use cases are categorically forbidden.

Calm Compass includes four "values predicates": `unselfish_act_in_window_30d`, `cross_group_engagement_in_window_90d`, `respects_difference`, and `no_evidence_of_willful_harm`. Each predicate is principal-authored, evaluated over the principal's private chain, and gates all disclosure through principal-explicit consent.

### Disability-Rights Risk Surface

The protocol touches disability-rights risk in five specific places. We are soliciting your review because existing disability-rights legal expertise is essential to validate our protective mechanisms.

#### (1) Cognitive-Baseline Recognition (Calm Witness E59)

Calm Witness allows a principal to declare a "cognitively atypical baseline" — neurodivergent cognition, altered consciousness patterns, or attention-regulation differences that deviate from neurotypical expectation. This declaration is *identity attestation*, not a values confession. The protocol uses this baseline to calibrate all subsequent values measurements so that a principal at the edge of neurotypical bandwidth is not invisible or pathologized.

**The Risk:** Without careful calibration, dimensions like `consistency_under_stress` or `honesty` could invisibly use neurotypical baseline as a hidden penalty function against neurodivergent principals. This would pathologize neurodivergence under the guise of values measurement.

**Our Protective Mechanism:** The values-identity boundary (E116) explicitly forbids any values dimension from using identity attributes (including neurodivergence status) as inputs. Per-principal calibration (E162) evaluates each dimension against the principal's own baseline, not a population mean. The audit gate (E115) checks all new dimensions for identity-leakage.

**Your Review Question (a):** Do the protections in E116 (values-vs-identity boundary) and E59 (cognitively-atypical-baseline calibration) materially prevent the protocol from pathologizing neurodivergent principals? Are there patterns in the inference functions where neurotypical baseline could still leak through as a hidden penalty?

#### (2) Self-Harm Attestation Gating (Calm Compass E157)

Calm Compass includes a predicate `self_harm_attested` that allows a principal to signal current self-harm risk to pre-designated supporters (licensed therapist, emergency contact). This is opt-in (off by default), per-counterparty, and narrow-window (7-day freshness). It is used only for crisis routing, never for risk assessment, insurance rating, employment evaluation, or custody decisions.

**The Risk:** Self-harm risk is disproportionately imputed to disabled and mentally-ill people. A protocol that gates self-harm disclosure could be misused to surveil disabled people, screen them out of employment, or use their self-disclosures against them in family court.

**Our Protective Mechanism:** E157 binds specific forbidden uses in license language (insurance, employment, custody, courts, schools, law enforcement). The predicate is not composable with any values dimensions. Disability status never triggers it. Counterparties must publish handling procedures and submit to annual ethics review. Violation triggers trademark action.

**Your Review Question (b):** Is the consent-gating on `self_harm_attested` (E157) sufficient under ADA, state-level mental-health-parity law, and EU AI Act risk-tier rules? Are there gaps in the forbidden-use binding that a determined counterparty could exploit?

#### (3) The Refusal Floor (Calm Compass E113)

The protocol categorically refuses to construct predicates for disability status, health status, mental-health diagnosis, or any dimension that would require "naming" disability or health. The refusal floor is a one-way ratchet: categories can be added, never removed. It is enforced via audit-process triage, trademark, and public misuse logging.

**The Risk:** The list of prohibited categories (Tier 3 of E113) includes "Disability Status (medical or psychiatric)" and "Health Status (HIV+ status, mental-health diagnoses, specific medical conditions)." But operationalization matters. A predicate that measures "mental stability," "cognitive consistency," or "access-tool usage" could functionally measure disability without naming it.

**Our Protective Mechanism:** E113 explicitly prohibits inferences of disability status through behavioral patterns. The audit gate (E115) checks new dimensions for implicit disability-measurement via proxy. Disability-rights expert is mandatory on the ethics review board. Annual re-review is required.

**Your Review Question (c):** Does the protocol's refusal floor (E113) cover the right categories for disability protection in v0? Are there behavioral proxies that should be permanently banned because they correlate too closely with disability?

#### (4) Scope-Statement Permanent Bans (E114)

The Calm Witness Scope Statement explicitly lists ten use cases that are permanently forbidden: law-enforcement surveillance, employment screening, insurance underwriting, lending decisions, medical diagnosis, child-welfare proceedings, immigration adjudication, predictive judgment, cross-principal aggregation, marketing. Any deployment using these name that violates this list forfeits trademark rights.

**The Risk:** Deployments might creatively reinterpret scope. "Employment screening" might be claimed as "occupational-health assessment." "Insurance underwriting" might be reframed as "actuarial risk adjustment." These workarounds could harm disabled workers and disabled insurance-holders.

**Our Protective Mechanism:** License enforcement (Apache-2.0 patent-non-aggression clause), trademark policy (Everest 92), verifier-registry refusals.

**Your Review Question (d):** Are there deployment patterns the scope statement (E114) should permanently ban that it currently does not? Are there disability-specific harms (employment discrimination against disabled workers, insurance discrimination, accessibility denial) that should trigger new scope restrictions?

#### (5) Respect-for-Difference Operationalization (E106, E108)

The protocol measures `respects_difference` as a values predicate: the principal shows evidence of respectful engagement with people different from themselves. The mechanism is principal-authored narration plus optional counterparty corroboration. The protocol never names which categories of difference were bridged (race, disability, gender, etc.).

**The Risk:** If a principal's interaction with a disabled person is flagged as evidence of "respect for difference," the counterparty could infer the principal's interaction partner's disability status. Alternatively, if a disabled principal's in-group engagement with other disabled people is measured, it could be misread as "tribalism" rather than "protective solidarity."

**Our Protective Mechanism:** Principal-authored narrative (the principal chooses what counted as "difference"); protocol never enumerates categories; protective-tribalism carve-out (E198) prevents in-group disability solidarity from being penalized.

**Your Review Question (e):** Where in the protocol surface does the reviewer find the highest residual risk of disability discrimination, and what concrete change would mitigate it? Are there edge cases in E106, E108, E116 calibration, or E198 protective-tribalism logic where disabled principals could still be harmed?

---

## Five Specific Review Questions

The disability-rights legal organization we hire will be asked to answer these five questions with specificity, citing statutes, case law, and implementation details.

### (a) Identity-Boundary Durability

**Question:** Do the protections in Everest 116 (values-vs-identity distinction) and Everest 59 (cognitively-atypical-baseline calibration) materially prevent the protocol from pathologizing neurodivergent principals?

**Scope:** Review the inference functions specified in the Compass v0 predicates (Everest 105–110) and the per-principal calibration mechanism (Everest 162). Determine whether any dimension could invisibly use neurotypical baseline as a penalty function. Assess whether the values-identity boundary is operationally enforceable or whether it is merely aspirational.

**Statutory Anchor:** ADA § 504 (reasonable accommodations for disability), ADA Title I (employment), GDPR Article 9 (special categories of personal data).

### (b) Self-Harm Predicate Consent & Forbidden-Use Binding

**Question:** Is the consent-gating on `self_harm_attested` (Everest 157) sufficient under ADA, state-level mental-health-parity law, and EU AI Act risk-tier rules? Can determined counterparties circumvent the forbidden-use binding?

**Scope:** Analyze the per-counterparty opt-in requirement, the narrow 7-day window, the mandatory handling-procedure publication, and the trademark enforcement mechanism. Test scenarios: Can an employer obtain the predicate by claiming "occupational health assessment"? Can an insurer obtain it under a "disability accommodation verification" pretext? Can a court compel disclosure? Review whether the mechanisms are sufficient across US, EU, and common-law jurisdictions.

**Statutory Anchor:** ADA § 504, HIPAA 45 CFR 164, Fair Credit Reporting Act (15 USC § 1681), EU AI Act Article 6 (prohibited practices), GDPR Articles 9–10.

### (c) Refusal Floor Categorization & Proxy Risks

**Question:** Does the protocol's refusal floor (E113) cover the right categories for disability protection in v0? Are there behavioral proxies that should be permanently banned because they correlate too closely with disability?

**Scope:** Examine Tier 3 of the refusal floor (Disability Status, Health Status). Review whether behavioral proxies (accessibility-tool usage, medication-adherence patterns, sleep patterns, communication style, neurodivergent ideation-cycling) could functionally measure disability without naming it. Determine whether specific behavioral proxies should be added to the forbidden list. Assess whether the distinction between "disability status" (forbidden) and "respect-for-difference with disabled people" (allowed) holds under scrutiny.

**Statutory Anchor:** ADA Title I, UN Convention on the Rights of Persons with Disabilities, GDPR Article 9, disability discrimination law across jurisdictions.

### (d) Scope-Statement Adequacy for Disability Protection

**Question:** Are there deployment patterns the scope statement (E114) should permanently ban that it currently does not? Are there disability-specific harms that should trigger new restrictions?

**Scope:** Review the ten current permanent bans (law enforcement, employment, insurance, lending, medical diagnosis, child welfare, immigration, prediction, aggregation, marketing). Determine whether these cover disability-specific risks: occupational-health surveillance of disabled workers, insurance discrimination against disabled beneficiaries, loan denial based on disability-proxy inference, special-education segregation, disability-based custody loss. Recommend additional permanent bans if needed.

**Statutory Anchor:** ADA Titles I, II, III, Section 504; Fair Housing Act; Olmstead doctrine (least restrictive alternative); state-level employment-protection law.

### (e) Residual Risk & Concrete Mitigation

**Question:** Where in the protocol surface does the reviewer find the highest residual risk of disability discrimination, and what concrete change would mitigate it?

**Scope:** Synthesize findings from (a)–(d). Identify edge cases in values dimensions, identity-calibration logic, protective-tribalism carve-outs, or consent mechanisms where disabled principals could still face discrimination. For each high-risk finding, specify a concrete change: a new audit-gate rule, a new forbidden use, a revised inference function, a strengthened consent requirement. Prioritize by severity and likelihood.

**No Partial Credit:** Vague recommendations ("strengthen oversight") are insufficient. Specific changes only.

---

## Named Candidate Organizations

We solicited organizations with deep expertise in disability law, AI regulation, and rights-based frameworks. The following candidates have been identified:

### 1. Disability Rights Advocates (DRA)
**Jurisdiction:** Oakland, California; West Coast US legal practice  
**Expertise:** Civil-rights litigation, employment law, ADA enforcement, disability-AI policy  
**Rationale:** DRA has litigated major employment-discrimination cases and maintains active public policy engagement on AI and algorithmic rights. Strong track record of holding technology companies accountable for disability discrimination.

### 2. Center for Democracy & Technology (CDT), Disability & AI Program
**Jurisdiction:** Washington, DC; international policy reach  
**Expertise:** Technology policy, rights-based frameworks, AI governance, disability tech equity  
**Rationale:** CDT's Disability & AI program combines technology-policy fluency with disability-justice grounding. Accustomed to reviewing AI systems for rights-based gaps and translating findings into enforceable standards.

### 3. American Association of People with Disabilities (AAPD)
**Jurisdiction:** National (US); intersectional reach  
**Expertise:** Policy analysis, civil-rights law, intersectional advocacy, disability leadership  
**Rationale:** AAPD brings national policy perspective and strong intersectional analysis. Includes leadership from disabled people across multiple disability categories, reducing risk of single-disability-type bias in the review.

### 4. Bazelon Center for Mental Health Law (optional)
**Jurisdiction:** Washington, DC  
**Expertise:** Mental-health law, civil commitment, psychosocial disability, treatment rights  
**Rationale:** If reviewing organization defaults to physical-disability or neurodevelopmental focus, Bazelon's mental-health-law expertise ensures psychiatry and psychosocial-disability dimensions are adequately covered.

### 5. National Disability Rights Network (NDRN) (optional)
**Jurisdiction:** Federal P&A network (all 50 states + territories)  
**Expertise:** State-level protection and advocacy, systemic disability rights, federalism  
**Rationale:** NDRN's network of state-level P&A offices provides jurisdiction-specific legal knowledge and direct connection to disabled people who would be deployed-against if protocols fail.

**Selection:** We will select three organizations from the above list, prioritizing disciplinary diversity (civil-rights litigation + policy + intersectional leadership). Final selection will be announced once engagement letters are signed.

---

## Terms of Engagement

### Compensation

**Honorarium: $35,000 (base) to $50,000 (full scope with comparative analysis)**

- $35K covers thorough review of the five specific questions above, with findings documented in a written report of 30–50 pages
- $50K includes above plus comparative analysis against EU AI Act standards, ADA case law, and disability-rights frameworks in 2–3 additional jurisdictions
- Estimated effort: 80–120 hours of senior legal review (attorney time, disability-rights expert time, stakeholder consultation with disabled community)
- Payment: 50% upon engagement-letter signature; 50% upon report submission

### Timeline

**Review Window: 60 days**
- Day 1: Engagement letter signed; organization receives all protocol documentation and background materials
- Day 30: Mid-review touchpoint (organization provides interim findings summary if substantive gaps emerge)
- Day 60: Final report submitted

**Calm Response Window: 30 days**
- Upon receiving report, Calm commits to written response to every finding
- Response addresses each recommendation (acceptance, partial acceptance, or reasoned rejection)
- Reviewer has right of rebuttal; if rejected, rebuttal is published alongside Calm's response

### Publication

**Open Publication:**
- The organization's full report is published on `vault.thecreativitymachine.ai/audits/` under CC-BY-4.0 license
- Redactions permitted ONLY for unresolved high-severity findings that present active risk; all redactions require reviewer concurrence
- Calm's written response to findings is published alongside the report
- Any reviewer rebuttals are published with the response
- Publication URL is provided to the organization for archiving and citation

### Independence & Authority

**Reviewer Authority:**
- The reviewing organization has full autonomy to recommend changes to the protocol
- Calm does not pre-approve findings or restrict scope
- Recommendations are not binding on Calm, but Calm commits to published response to every recommendation
- Recommendations may include: new forbidden uses, revised consent mechanisms, additional audit gates, changes to inference functions, restrictions on predicate vocabulary

**Reviewer Right of Refusal:**
- The organization can decline to review specific sections if those sections fall outside the organization's expertise
- Declinations are noted publicly alongside the report (e.g., "NDRN did not review Everest 162 per-principal-calibration logic due to scope constraints; a second reviewer recommended for comparative technical evaluation")
- Declinations do not reduce honorarium

### Accountability Structure

**Binding Commitment (Calm → Reviewer):**
- Calm will publish a written response to every finding
- If a finding is rejected, Calm's rejection includes specific rationale
- Rejection does not mean the finding is ignored; Calm commits to explaining why the recommendation was not adopted
- If later deployment harms emerge in an area the reviewer flagged, Calm publishes acknowledgment of the prior warning

**Non-Binding But Required (Reviewer → Calm):**
- Recommendations are advisory, not mandatory
- But Calm's authority to call the protocol "Calm Compass" or "Calm Witness" is conditional on accepting findings that Calm's license and ethics review board deem load-bearing
- If Calm rejects a finding that the ethics board believes impacts disability rights, the ethics board may recommend removing the protocol's license or restricting its trademark

---

## Follow-On Structure

### Annual Re-Review (E186b, future)

After the first review publishes, Calm commits to annual review by the same organization on an agreed cadence. The scope narrows in year 2+ to focus on:
- New predicates added to the vocabulary (if any)
- Reported incidents or near-misses from deployment
- Changes to inference functions or calibration logic
- Findings from Everest 80 (ethics review board) that implicate disability rights

### Cross-Org Panel (E186c, future)

Upon v1 release of the protocol, Calm will commission a three-organization concurrent review, allowing for comparative analysis and consensus-building across disability-rights frameworks.

### Downstream Feeds

Findings from E186 directly inform:
- **Everest 80 (Ethics Review Board)** revisions: Any finding recommending changes to audit gates or inference functions feeds into E80 governance
- **Everest 95 (Predicate Registry Governance)** calibration: Findings on forbidden uses or proxy risks inform E95's predicate-vetting process
- **Everest 114 (Scope Statement)** updates: Any finding recommending new permanent bans updates E114 immediately upon ethics review board concurrence

---

## Status: Design-Bagged (Pending Institutional Follow-Through)

**Current Status:** DESIGN-BAGGED

**Shipping Criteria:**
1. Review brief and solicitation letter finalized and ready to send (this document, sections above)
2. Three candidate organizations identified and vetted (listed above)
3. Scope of review precisely articulated (five review questions)
4. Terms of engagement pre-specified (compensation, timeline, publication, independence)

**Path to "BAGGED" Status:**
- At least one of the three candidate organizations signs an engagement letter
- The organization begins the 60-day review
- Upon review completion and publication, the summit moves to BAGGED status

**Until then:** The design is locked in; the institutional execution is pending.

---

## Institutional Commitment

Calm commits to:

1. **Transparency:** Publishing the engagement letter and all correspondence with the reviewing organization
2. **Good Faith:** Engaging substantively with findings, even if disagreeing
3. **Accountability:** Publishing written response to every finding
4. **Dissent Publication:** Publishing reviewer rebuttals and reasoned rejections without redaction
5. **Trademark Binding:** Making continued use of "Calm Compass" / "Calm Witness" conditional on taking disability-rights findings seriously in ethics-review governance

This is not a cosmetic review. It is a structural accountability mechanism.

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
