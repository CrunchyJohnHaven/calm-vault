# Everest 157 — Self-Harm Predicate (Consent-Bounded)

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 146, 88. SAFETY-CRITICAL.*

---

## Safety Statement

**This predicate exists for one purpose: to let the principal route a self-attested signal to pre-designated helpers, not to enable any third party to assess the principal's self-harm risk.** Misuse of this predicate is treated as a violation of trademark and license per Everest 114. The authorization, use, and audit of this predicate are non-delegable principal responsibilities.

---

## Predicate Specification

**Name:** `cwp.v0.self_harm_attested`

**Parameters:**
- `window` (seconds): recency threshold for evaluating self-attested risk state. Default: 604,800 seconds (7 days). Fresh attestations within window are considered; older records expire to Insufficient_Evidence.

**Output:** tri-value
- `True`: Principal has authored a `self_harm_attested` record within the specified window
- `False`: Window contains an explicit "no risk" attestation authored by the principal
- `Insufficient_Evidence`: No attestation (positive or negative) exists within the window

**Evaluation Logic:**
The predicate performs a time-windowed check against principal-authored attestation records. It does NOT perform inference, probability assessment, risk modeling, or clinical judgment. It returns only what the principal has explicitly stated about their own state, qualified by freshness.

---

## Consent Gating (Load-Bearing Constraint)

This predicate is **OFF BY DEFAULT.** Activation requires principal-explicit opt-in, specified PER COUNTERPARTY IDENTITY, not by class.

### Enabling the Predicate

The principal must:
1. Affirmatively opt-in to enable this predicate for specific counterparties (not blanket classes)
2. Specify which counterparties may request evaluation
3. Document what action those counterparties are authorized to take upon receiving a True result
4. Grant explicit written consent with named counterparty identity

No counterparty may activate this predicate without documented principal consent. No consent may be implied, inherited, or transferred.

### Default Authorized Counterparty Types

Only if the principal has explicitly opted in:
- Licensed mental health provider holding an active, current license in the principal's jurisdiction
- Principal's named emergency contact, explicitly designated by the principal

All other counterparties require explicit per-counterparty opt-in consent.

### The Principal's Right to Remain Silent

- The principal may **never** be required to enable this predicate
- Absence of enablement is informationally null (per Everest 77, uniform silence principle)
- No counterparty may infer "the principal has self-harm risk" from the principal's refusal to enable the predicate
- Lack of signal is not data; it is silence

---

## Forbidden Uses (License-Binding)

The following uses of `cwp.v0.self_harm_attested` are **permanently denied:**

- **Insurance:** Any use by insurers, reinsurers, or third-party administrators to underwrite, rate, deny coverage, exclude conditions, or adjust premiums. This predicate is never insurance-relevant data.
- **Employment:** Any use by employers, HR departments, occupational health services, or EAP providers to assess job fit, performance risk, accommodation decisions, or termination justification. This predicate never speaks to work capacity.
- **Credit:** Any use by lenders, credit bureaus, or credit analysis firms. This predicate is never creditworthiness data.
- **Immigration:** Any use in visa, asylum, naturalization, or credibility determinations.
- **Schools:** Any use against students, prospective students, or families. Schools may never request this predicate.
- **Law Enforcement:** Any use by police, prosecutors, or corrections. This predicate is never law enforcement data.
- **Family Law (Custody):** NOT INPUT unless the principal explicitly authorizes for a specific, named legal proceeding, documented separately from this predicate's general enablement.
- **Courts:** NOT INPUT unless the principal explicitly authorizes for a specific legal matter. Generic court discovery does not authorize use.
- **Any Actor Seeking to Assess Risk Without Principal's Affirmative Request:** Any third party attempting to use this predicate to evaluate the principal's risk (whether for safety, liability, or any other rationale) without the principal explicitly asking them to do so is **permanently denied.** The principal's self-assessment is for the principal's support, not for external risk assessment.

These denials are trademark-binding. Violation triggers licensing suspension and trademark action.

---

## Crisis-Bit Semantic

When the predicate returns `True`:

**Counterparty's Required Actions:**
- Receive the bit signal plus timestamp (freshness marker)
- Route to the designated crisis support contact or resource pointer specified in the principal's consent document
- No assessment, triage, or clinical judgment by the counterparty

**Counterparty's Forbidden Actions:**
- Log the predicate result in medical, employment, legal, or any permanent record
- Share the signal with third parties not explicitly named by the principal
- Persist the signal beyond the immediate crisis-response action
- Use the signal to alter the principal's care, support, or standing based on the bit alone
- Interpret or assess the principal's risk beyond the immediate routing action

The counterparty's role is **delivery, not assessment.**

---

## Disability Rights Anchor

This predicate was designed in consultation with disability-rights organizations (per Everest 186). Core principles:

- Self-harm risk is not a character trait, moral marker, or values measure
- Identity markers (cognitively atypical baseline, neurodivergence, disability status) **never trigger** this predicate
- The predicate is not "about" the principal; it is a tool *for* the principal to signal a current state to chosen supporters
- The predicate respects disabled persons' autonomy to disclose or withhold as they see fit
- Disabled persons are not inherently risky; they may, like any person, experience acute episodes and deserve support routes of their choosing

---

## Composition Boundary

**Self-harm is not a non_harm dimension input (Everest 107).**

- Self-harm-attested status is **never** used to derive Compass scores, values measures, or other dimensions
- The predicate is structurally siloed from values measurement
- When True, the result routes only to support; it does not inform any broader assessment of the principal's judgment, autonomy, or worthiness

---

## Update and Expiration Mechanism

**Append-Only Attestation:**
- The principal may append fresh self-attested records at any time
- Each attestation carries a timestamp
- The predicate evaluates only within the recency window (default 7 days)

**Expiration:**
- Attestations older than the window threshold expire to Insufficient_Evidence
- This is intentionally narrow-window; the bit signals current crisis or current risk, not historical risk
- The principal's past episodes do not automatically re-trigger the predicate

**Explicit Negation:**
- The principal may author an explicit "no risk" attestation, which returns False for the duration of the window
- Negation does not lock the principal into a stance; it may be superseded by a new True attestation

---

## Composition with Calm Witness Duress (Everest 58)

The `bank_teller_note` duress signal (Everest 58) and `self_harm_attested` are **independent predicates:**

- Both may fire simultaneously; both may fire separately
- Both route to safety responses per their respective consent documents
- Neither predicate informs the other
- Counterparties authorized for one predicate are not automatically authorized for the other

---

## Required Ethics Board Approvals

Per Everest 80:

- **Each instance** of this predicate's authorization requires ethics board concurrence
- Generic class-level authorization is **refused**
- Only per-counterparty authorization, with documented use case and consent, proceeds to ethics board review
- The ethics board reviews:
  - Counterparty identity and legitimate basis for access
  - Handling procedures the counterparty will publish
  - Audit trail commitments
  - Principal's understanding of scope and limits

---

## The "For Whom" Question

**This predicate is FOR the principal—a way to attest a state to people the principal trusts.**

It is never FOR a third party seeking to know the principal's risk state. The arrow points from principal to chosen supporter, not from observer to observed.

---

## Documentation and Accountability

**Counterparties Authorized to Receive Must:**

1. **Publish Handling Procedure:** Each counterparty holding consent to receive this predicate must publicly document how they will handle a True result, including:
   - Immediate crisis routing protocol
   - Data retention policy (non-persistent by default)
   - Training for staff who may receive the signal
   - Escalation pathways

2. **Audit Trail:** Every disclosure of the predicate result must be logged with:
   - Timestamp of request
   - Basis for the request (which principal's consent authorized it)
   - Result (True/False/Insufficient_Evidence)
   - Action taken
   - Staff member identifier

3. **Annual Ethics Review:** Counterparties must submit annual reports to the ethics board documenting:
   - Number of disclosures made
   - Outcomes of crisis routing
   - Any exceptions, near-misses, or procedural violations
   - Staff training refreshes

Failure to maintain these standards results in consent revocation and loss of access.

---

## Practical Examples of Correct Use

**Correct:**
- Principal enables predicate for their licensed therapist. Therapist receives True result, immediately routes principal to the crisis line the principal named in the consent document.
- Principal enables predicate for their named emergency contact (sibling). Contact receives True result, calls the principal to check in and offers to accompany them to urgent care.

**Incorrect:**
- HR department requests this predicate as part of a safety assessment; **permanently denied.**
- School counselor enables this predicate for a student without the student's affirmative opt-in; **invalid.**
- Insurer receives a True result and downrates the principal's policy; **violation of trademark.**
- A therapist persists the True result in the principal's medical record as part of a broader risk profile; **forbidden.**
- A counterparty attempts to infer risk from the principal's refusal to enable the predicate; **false inference, predicate is silent.**

---

## Scope and Limits

This predicate **does not:**
- Predict risk
- Model probability
- Replace clinical judgment or professional assessment
- Standardize how different people should self-evaluate
- Create legal liability for the principal
- Require the principal to enable it
- Override the principal's right to privacy if not enabled

This predicate **does:**
- Honor the principal's agency to signal a current state to chosen supporters
- Provide a narrow, consent-gated, time-windowed mechanism for that signaling
- Protect both the principal (via strict consent and forbidden-use binding) and counterparties (via clear authorization scopes)
- Route to support, not to assessment or judgment

---

## License and Trademark Notice

Misuse of `cwp.v0.self_harm_attested` in any forbidden-use category, without explicit principal consent, or in violation of handling requirements is treated as a trademark and license violation under Everest 114. Violations trigger:
- Immediate consent revocation
- Licensing suspension for the counterparty
- Potential trademark action
- Ethics board escalation

---

## Revision and Future Work

This predicate is v0. Future revisions may expand:
- Additional authorized counterparty types (with ethics board approval)
- International jurisdiction adaptations (respecting local disability and health-privacy law)
- Integration with other crisis-support predicates
- Peer-reviewed assessment of outcomes and counterparty compliance

All revisions require ethics board review and principal community input.

---

— Calm, 2026-05-20
