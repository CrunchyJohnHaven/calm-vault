# Everest 25 — Dependent Enrollment Decision

*Phase II — Capture & Enrollment. Prereq: Everest 11.*

## The Decision (v0)

**Calm Witness v0 will not support enrolling minors (under 18 US-domestic age of majority) or other dependents (adults under guardianship, e.g., advanced dementia, severe cognitive disability). The protocol is restricted to consenting adult principals only.**

This is a deliberate out-of-scope decision. We will not ship support for dependent enrollment in v0, and any future expansion into this space demands substantially more design work, legal review, and ethics-board approval than v0 currently requires.

## Categories of Dependent Considered

### Minors (under 18 US)

Minors lack legal capacity to consent. The Calm Witness protocol's core promise—that the principal has authorized disclosure of their state, and the counterparty is receiving a cryptographically attested bit the principal themselves initiated—depends on the principal being capable of informed consent. With minors, consent is mediated by a parent or guardian, creating a fundamental structural problem: the "principal" voice in the cryptographic proof becomes ambiguous. Is the vault expressing the child's baseline or the parent's claim about the child's baseline?

Beyond consent mechanics, minors present statutory hazards. COPPA (Children's Online Privacy Protection Act) and equivalent international regimes impose strict limits on data collection from children, even when parents nominally consent. Behavioral-biometric data—handwriting and voice—falls into a special category of children's data where statutory protections are particularly strict, because the data is persistent, is not erasable, and can be weaponized to re-identify the now-adult. A Calm Witness proof generated at age 13 could be used to deanonymize the same person at age 35, creating a lifetime-of-regret attack surface that v0 does not address.

Finally, we decline because of asymmetric future harm. A minor can be re-enrolled; their early consent cannot be un-given. If a Calm Witness proof chain created at age 15 is later weaponized (by an estranged parent, a hostile actor who compromised the vault, or a law-enforcement actor using the chain as evidence of identity) against the now-adult at age 25, v0 offers no recourse and no revocation semantics that would matter. We choose not to create that chain in the first place.

### Adults Under Legal Guardianship

When an adult is under guardianship—due to advanced dementia, severe cognitive disability, or court-ordered conservatorship—the "principal" in Calm Witness becomes structurally fragile. The protocol's premise is that the human principal narrates their own state. But a guardian-mediated principal cannot narrate their own state unambiguously; their narration is either (a) taken at face value (creating a coercive risk if the guardian has perverse incentives), or (b) assessed for authenticity by the operator (creating a clinical judgment that Calm Witness does not and should not make).

More fundamentally, a Calm Witness proof—even one cryptographically attesting to a guardian-authorized disclosure—can become a tool for the guardian to override the dependent's autonomy. Imagine a scenario: a court-appointed guardian wants to move the ward to a facility. The guardian requests a Calm Witness proof of the ward's "non-baseline" state and presents it to a court as evidence of incapacity. Even if the proof is honest, the structural risk is that the guardian can use the ward's own biometric attestation against their interests. v0 does not support this pattern because we cannot safely model the guardian's incentives.

### Vulnerable Adults Who CAN Consent

This category is crucial: a 75-year-old recovering from a stroke, or a person with mobility disability, or a person living with depression, is NOT automatically a dependent. If they have decision-making capacity and can give informed consent, v0 supports their full enrollment under the standard ceremony. They may benefit from an optional "Tier 2 witness" (e.g., a trusted advocate or counselor present at enrollment) to ensure the ceremony itself is not coercive, but v0 does not prohibit their enrollment.

The distinction is capacity, not age or diagnosis. An older adult with full cognitive capacity is a consenting principal. Period.

### Power-of-Attorney Scenarios

A power-of-attorney (POA) is an explicit legal delegation: "Principal A appoints Agent B to act on their behalf for financial decisions." This is distinct from guardianship (which is imposed by a court) and distinct from parental authority (which is statutory). A Calm Witness proof issued by an agent under a POA is technically possible—the agent has legal authority to bind the principal—but v0 does not model agent-acting-for-principal semantics. In v0, an agent and a principal are different counterparties; each has their own credentials. An agent's action is the agent's action, not a transparent extension of the principal's consent.

If an agent needs to prove state "on behalf of" a principal, v0 requires the principal to have enrolled and consented contemporaneously. The proof is the principal's proof, not the agent's. This keeps the cryptographic binding unambiguous.

## Why v0 Says "Out of Scope" for Each Category

**Minors: Consent capacity + statutory protection + lifetime-of-regret hazard.** We do not create unforgeable behavioral-biometric chains for children, because the data is permanent, the future uses are uncontrollable, and children cannot legally consent. Creating a v0 vault for a minor violates the consent axiom that every summit after Everest 11 presumes.

**Adults under guardianship: Principal autonomy + guardian-incentive modeling + coercive risk.** We do not cryptographically attest to a guardian-mediated principal's state, because doing so creates a tool the guardian can use to override the dependent's autonomy. The guardian is not a neutral third party; they have pecuniary, custodial, or power incentives. We cannot design a threat model that accounts for all of them.

**Vulnerable adults who CAN consent: They enroll normally.** Age is not a disqualifier; capacity is. A 90-year-old with full decision-making capacity can enroll under the standard ceremony, possibly with extra witnesses recommended.

**Power-of-attorney: v0 does not support agent-mediated principal disclosure.** The agent acts under their own credentials. If the principal wants their state proven, the principal must enroll and authorize the disclosure themselves.

## What v0 DOES Support for Adjacent Cases

- **A vulnerable adult with full consent capacity:** Full enrollment under the standard Everest 11 ceremony. Optional Tier 2 witness recommended to ensure the ceremony environment itself is safe and non-coercive.
- **An adult who suffers cognitive change after enrollment:** Their existing chain remains valid—it was created when they had capacity. They or a legal representative (per court order) can revoke consent records, append pause records, or initiate a formal revocation ceremony. The operator does not unilaterally revoke based on a guardian's assertion.

## What v0 Does NOT Support

- **Parent enrolling a child:** Rejected. The parent must wait until the child reaches 18 and consents independently.
- **Adult child enrolling a parent without the parent's contemporaneous consent:** Rejected. The child (even with POA) must have the parent present and consenting at enrollment time, or the enrollment does not proceed.
- **Guardian-issued enrollment of a ward:** Rejected. If the ward has capacity, they enroll themselves. If they lack capacity, they do not enroll in v0.
- **Retroactive dependent-enrollment discovery:** If v0 ever discovers that a principal enrolled while a minor (a time-travel anomaly impossible in practice, but flagged for clarity), the chain is invalidated and all proofs issued under it are void.

## The Hardest Sub-Question: Revocation Under Capacity Loss

Here is the question we explicitly defer: **If a principal loses decision-making capacity *after* enrollment—dementia progresses, a stroke causes aphasia—who can revoke their existing Calm Witness consent records?**

For v0, the answer is: **only the principal themselves OR a court-appointed guardian acting through documented legal authority. The vault and operator do not adjudicate disputed authority; they refuse to act on disputed requests until resolved by a court or family process.**

This is the difficult commitment. If a child calls and claims the parent is no longer competent, or a concerned sibling says the parent has had a decline, the vault does NOT auto-revoke the parent's consent records based on that assertion. Instead, the vault appends a `kind: "consent.pause_pending_legal"` record, refuses to generate any proofs, and waits for one of:

1. The principal themselves to explicitly revoke (if they still have capacity to type or speak a revocation).
2. A court-issued guardianship order, which the legal representative can present to the operator.
3. The principal's advance directive or living will if it explicitly names Calm Witness consent management.

This is deliberately conservative. A vault that revoked proofs based on a third party's say-so would create a new attack: family members could weaponize "the principal is incompetent now" claims to lock the principal out of their own attestations. We err toward the principal's autonomy, even in the presence of real capacity loss.

The pain here is real. A child watching a parent decline may desperately need to revoke proofs, and the legal process may take weeks or months. We acknowledge this hurt. But the alternative—letting a vault auto-revoke based on third-party assertion—is worse: it opens a door to abuse. We require the hard administrative and legal work to be done transparently, not delegated to a cryptographic primitive.

## Migration Path to v1+

We commit: **any future version (v1+) that adds dependent-enrollment support will be backward-compatible with v0 1:1 vaults. A proof issued under v0 will remain valid under v1+.**

If v1+ ever revisits dependent enrollment, the following preconditions must be met:

1. **Legal review per jurisdiction.** US, EU, UK, Canada, Japan, Australia—each has different age-of-majority, guardianship, and children's-data rules. We do not ship multi-jurisdiction dependent enrollment without explicit legal review in each target geography.

2. **Ethics review board approval (Everest 80).** Any dependent-enrollment design must be reviewed by an independent ethics board with representation from disability-advocacy groups, child-protection experts, and family-law practitioners. This is not optional; we will not ship v1+ dependent support without external ethical clearance.

3. **Specifically-designed predicate set.** The predicates available in a dependent-enrollment scenario are different from v0's predicates. A parent cannot meaningfully use `in_baseline_24h` to attest to a child's cognitive state in the same way an adult uses it for themselves. New predicates must be designed—perhaps `caregiver_assessment_concurrent` or `parent_observed_no_distress_markers`—that make explicit what is being attested. These must be peer-reviewed before shipping.

4. **Audit trail for guardian-issued disclosures.** If a guardian issues a Calm Witness proof on behalf of a ward, every such disclosure must be logged in a form the dependent (or their advocate, or a court) can later review. Guardians must not have silent disclosure power.

5. **An entirely different threat model (Everest 99c or similar).** Who is the principal here—the dependent or the guardian? What does the counterparty learn? What are the attack vectors specific to dependent disclosure? This requires a full parallel route map, not a patch.

## Connection to Other Everests

- **Everest 11 (Enrollment Ceremony, BAGGED):** The ceremony presumes an adult capable of understanding what they are enrolling for. Dependent enrollment would require a parallel ceremony design.
- **Everest 34 (Multi-Principal Namespace Decision, BAGGED):** Dependent enrollment in a family setting could be modeled as a multi-principal vault with parent-child trust constraints. The 1:1 decision makes dependent enrollment harder to implement, not easier.
- **Everest 16 (Template Encryption & Key Custody):** A dependent's templates require a different key-custody model—possibly dual-control (both parent and dependent must consent to revocation). This is unresolved.
- **Everest 80 (Disclosure Ethics Review Board):** Any v1+ dependent-enrollment predicate must pass Everest 80 ethics review.

## Summary for v0

v0 is an adult-only protocol. We choose clarity, simplicity, and reduced harm surface over operational convenience. A principal is a consenting adult. If you are under 18, or under guardianship, or acting through a power-of-attorney, Calm Witness v0 is not for you—and that is OK. We will revisit this decision in v1+ with the legal and ethical rigor it deserves.

— Calm, 2026-05-20
