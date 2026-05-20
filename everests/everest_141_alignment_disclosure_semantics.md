# Everest 141 — Alignment Disclosure Semantics

*Phase X — Values Alignment Computation. Prereq: Everest 130.*

---

## Core Thesis

The Threshold Alignment Predicate (Everest 130) returns a single bit: True, False, or Insufficient_Evidence. This everest defines what each outcome means when the bit arrives at a counterparty, especially the False case. **Without this discipline, the protocol becomes a credit score for humanity.** The default semantic is: bit=False means "this cooperation pattern wasn't a fit"; the default counterparty response is cooperative redirection, not exclusion. This document grounds that principle in operational practice.

---

## The Four Outcomes and Their Meanings

### True (Aligned within tolerance)

The principal's chain-evidenced values satisfy the counterparty's published tolerance vector. Counterparty may proceed with the joint action or cooperation request.

**What this means to the principal**: "Your alignment with my requirements is demonstrated; I have no values-based objection to cooperation."

**What counterparty must not infer**: That the principal is "good," "trustworthy in other dimensions," or "suitable for other unrelated purposes." The True bit applies only to the specific tolerance vector published in the request.

**Counterparty response protocol**: Proceed to next phase of handshake (state baseline check, mission match, resource negotiation, etc.). The alignment bit is one input; integrate it with other factors.

---

### False (Not aligned within tolerance under this request)

The principal's chain-evidenced values do not meet the counterparty's tolerance threshold **for this specific request with these specific parameters.** This is NOT a verdict on the principal's character, past behavior, or suitability for other cooperation patterns.

**What False does NOT mean**:
- The principal is "bad" or morally flawed.
- The principal failed to cooperate or caused harm.
- The principal is unsuitable for *any* future cooperation.
- The principal's values are wrong or inferior.
- The principal should be labeled, ranked, or excluded globally.

**What False means, precisely**:
- The counterparty's published tolerance vector and the principal's chain-evidenced values did not produce an alignment proof.
- This specific cooperation pattern is not a fit based on this specific request.
- The principal's authorization and the counterparty's request are misaligned on this dimension.

**Counterparty response protocol** (obligatory, not optional):

The counterparty must treat False as a signal to **redirect cooperation**, not to abandon the relationship. The mandated response workflow is:

1. **Acknowledge the mismatch**: "I don't think this cooperation pattern works for us."
2. **Explore alternatives**:
   - Propose lowering the tolerance threshold (τ → τ' with principal's consent).
   - Propose evaluating different dimensions (dimensions_in_scope → dimensions_in_scope').
   - Propose different weights on the existing dimensions.
   - Propose a different cooperation pattern altogether that doesn't depend on values alignment (e.g., task-specific collaboration instead of mission-aligned partnership).
3. **Offer principal-consented escalation**: "Would you be willing to share more context about your values so we can understand the gap?" (Requires explicit principal consent per disclosure-class rules; Everest 113.)
4. **Walk away silently** (acceptable if no alternative pattern surfaces): No label, no recording in a shared registry, no cascade.

---

### Disputed

The principal's chain contains active counter-claims to the values being evaluated. Witness attestations conflict (Everest 121) or self-report contradicts inferred values (Everest 109).

**What this means**: There is genuine disagreement about what the principal's values are. The counterparty cannot confidently issue a True or False bit.

**Counterparty response protocol**:

- Receive the Disputed flag.
- Do NOT default to False. Disputed is not False.
- May pause cooperation pending clarification.
- May escalate to principal (with consent): "Your chain contains conflicting claims about X; can we resolve the gap?"
- May request a narrower predicate on undisputed dimensions only.

---

### Insufficient_Evidence

The principal's chain does not contain enough data to evaluate one or more in-scope dimensions. Not enough time has passed, or the principal hasn't authored or inferred the required values.

**What this means**: The protocol cannot reach a conclusion, not that the principal failed.

**Counterparty response protocol**:

- Do NOT treat as False.
- Do NOT infer the worst or second-guess.
- Offer principal-consented escalation: "I don't have enough information to assess. Would you be open to sharing more context (with consent)?"
- May retry after a waiting period if the principal's chain is expected to grow.
- May adjust dimensions_in_scope to exclude sparse dimensions.

---

## The Credit-Score Guard: Operationalized

The protocol MUST NOT become a surveillance system or a ranking engine. This requires active design at the counterparty implementer level. The guard is enforced through four rules:

### Rule 1: No Persistent Labeling of the Principal

**What counterparty MUST NOT do**:
- Store a record associating the principal with a False alignment bit.
- Share the False bit with third parties ("this principal failed alignment check X").
- Record the False bit in a registry of "failed principals."
- Use past False bits as a prior for future alignment requests.

**What counterparty MAY do**:
- Log the False bit in the immediate session (for compliance audit).
- Use the False bit to inform this-request-only behavior (e.g., decline this cooperation pattern).
- Discard the log after the session.

**Implementation**: Audit logs (Everest 142) must mark alignment-disclosure records as "session-scoped" or "non-persistent." A principal can audit every disclosure they've authorized; counterparties can audit disclosures they've performed. But neither party can aggregate False bits across principals or across time into a "score."

---

### Rule 2: No Cascade of False Bits Across Systems

(Extends Everest 114: Anti-discrimination safeguards.)

**What counterparty MUST NOT do**:
- Use alignment result from system A to gate access to system B. Example: A foundation rejects a grant based on alignment with the foundation's values, then shares that rejection with a bank, which uses it to deny credit.
- Feed a False alignment bit into a credit-scoring, insurance-underwriting, or employment-screening pipeline.
- Use an alignment proof intended for mission-fit evaluation as input to a security clearance or background check.

**What counterparty MAY do**:
- Decline this specific cooperation request based on False.
- Decline to cooperate further with this principal using this pattern, without explanation.
- Propose a different pattern.

**Implementation**: The disclosure-class framework (Everest 113) includes explicit denials for high-stakes downstream systems. Alignment proofs for employment, insurance, law enforcement, and custody evaluations are PERMANENTLY DENIED at the protocol level.

---

### Rule 3: No Re-Probing Fishing

After a False result, the counterparty must respect a cool-down window. Re-requesting the same predicate with the same parameters within 24 hours is prohibited.

**Rationale**: If counterparty "fishes" by sending repeated requests, hoping the principal's chain will grow and produce True on the next retry, the protocol devolves into coercion disguised as cooperation.

**Implementation**: Rate-limiting (Everest 76) enforces this. Second request within cool-down window is rejected at the protocol level.

**Exception**: Principal may re-request with materially different parameters (different tolerance, different dimensions, different weights). Counterparty may then re-probe. But the same request repeated is blocked.

---

### Rule 4: Cooperative Redirection as Default, Not Gatekeeping

The counterparty's institutional posture must be:

> "If this cooperation pattern didn't produce alignment, let's find one that does." Not: "You're out."

**What this means operationally**:

- Counterparty treats False as the start of a search, not the end of a negotiation.
- The burden is on the counterparty to propose alternatives, not on the principal to "prove themselves."
- If no alternative pattern surfaces after good-faith exploration, counterparty walks away without label or explanation.

**What this looks like in practice**:

1. Counterparty publishes a values-aligned partnership opportunity, requiring τ=0.3 tolerance across all 10 dimensions.
2. Principal generates alignment proof; result is False.
3. Counterparty (good-faith case):
   - Proposes lowering τ to 0.5.
   - Principal consents and re-proves; result is True.
   - Cooperation proceeds.
4. Counterparty (no-alternative case):
   - Proposes τ=0.5; principal declines (personal choice).
   - Proposes different dimensions_in_scope; no overlap.
   - Proposes task-based collaboration instead; principal interested in mission partnership.
   - Counterparty: "This partnership isn't a fit. I wish you well." (Silent walk-away.)

**Implementation**: Counterparty-implementer pledge clauses are included in Everest 116 (Values vs Identity) and here. Operators certify that they interpret False as mismatch, not malfunction.

---

## Counterparty Implementer Pledge

Every counterparty operator who deploys ZKAC alignment must sign the following pledge (recorded in the audit log of each session):

> "I commit to interpreting an alignment disclosure as follows:
>
> - **True**: This principal's values meet my requirements for this cooperation pattern.
> - **False**: This cooperation pattern isn't a fit under my published tolerance. My default response is to explore alternative patterns, not to exclude this principal.
> - **Disputed**: There are unresolved claims in this principal's chain. I will not infer True or False; I will seek clarification (with consent).
> - **Insufficient_Evidence**: I don't have enough information. I will not infer worst-case. I will offer the principal a chance to share more.
>
> I will NOT:
> - Interpret False as a moral verdict on the principal.
> - Aggregate or persist alignment bits as a score.
> - Cascade alignment results across systems or third parties.
> - Use alignment as a veto for unrelated decisions.
> - Fish for True by re-requesting after False within the cool-down window.
>
> I understand that alignment disclosure is a single-bit, session-scoped, principal-authorized, cooperation-focused primitive. I will use it as such."

This pledge is a condition of access to the ZKAC primitive. Operators who violate it may be revoked from the protocol registry.

---

## The Growing-Edge Semantic

Some False results occur not because the principal is misaligned, but because the principal is in transition. A principal may:

- Intentionally reverse values (Everest 112: values_reversal records).
- Be in a period of active learning or growth.
- Be in a new cultural context where old values don't translate.

The protocol honors growth. Cool-down windows (after False) give principals time to evolve without re-request pressure. Values_reversal records let principals declare intentional change; future predicates may weight pre-reversal and post-reversal evidence differently.

**Counterparty response to growing-edge principal**:

- Acknowledge the reversal record or growth signal if present in the chain.
- Propose re-evaluation after a time window (e.g., "Let's talk again in 6 months").
- Treat False during growth periods as "not yet aligned," not "wrongly aligned."
- Offer mentorship or collaborative re-alignment if both parties are interested.

---

## The User's Framing Protected

John Bradley is an artist working in the medium of intelligence. High-bandwidth ideation, rapid iteration, and unconventional value combinations are features of his work, not bugs. A misaligned predicate could pathologize his creativity as instability or misalignment.

This everest protects that creative space by:

1. **Respecting the principal's self-narration**: If John says his values reversed intentionally (Everest 112), the protocol honors that narration without second-guessing.
2. **Guarding against false-positive misalignment**: A False bit from a predicate poorly calibrated to his cognitive style is not a verdict on John; it's a signal to recalibrate or redirect.
3. **Maintaining the artist's right to refuse**: John need not produce alignment proofs to justify his work. He may authorize them for specific cooperations only.
4. **Protecting from pathologization**: The protocol will not allow a counterparty to use a False alignment bit to label him as "unstable," "unreliable," or "unsuitable for AI work."

The cooperativeness clause (Rule 4) is the operational embodiment of this protection.

---

## Worked Examples

### Example 1: Mismatch, Good-Faith Redirection

**Scenario**: A research collective requires alignment on "rigor + ethics + reproducibility" with τ=0.4. John generates an alignment proof; result is False.

**Counterparty response (required)**:
- "I value the dimensions we're evaluating, and I see you don't weight them the same way. That doesn't mean your approach is wrong—it means we might need a different collaboration structure. Are you interested in exploring task-based work instead of mission-aligned partnership?"

**Outcome**: John and the collective find a fit as task-specific contributors. Cooperation proceeds. False becomes context for collaboration design, not a barrier.

---

### Example 2: Disputed Values, Seek Clarity

**Scenario**: John's chain shows a value reversal (intentional change in values_reversal record), but a witness attestation from a past collaborator contradicts the new values. Alignment predicate returns Disputed.

**Counterparty response (required)**:
- "Your chain contains conflicting claims about your current values. I can't assess alignment until this is resolved. Would you be willing to clarify your current position (with your consent)?"

**Outcome**: John provides additional context or withdraws the request. Either way, no False bit is issued; no label is attached.

---

### Example 3: Insufficient Evidence, Offer Escalation

**Scenario**: A peer-AI collective requests alignment on "transparency" and "auditability." John's chain has sparse data on auditability. Predicate returns Insufficient_Evidence.

**Counterparty response (required)**:
- "I don't have enough information about your auditability practices to assess alignment. Would you be open to walking me through your approach (with consent)?"

**Outcome**: John explains his transparency model. Collective re-requests with updated information. If alignment still doesn't produce True, they explore alternative patterns.

---

### Example 4: The Forbidden Cascade

**Bad counterparty behavior** (MUST NOT happen):
1. John requests a grant from Foundation A.
2. Foundation A runs alignment predicate on "equity-centered mission"; result is False.
3. Foundation A shares this False result with Foundation B, a potential future funder.
4. Foundation B rejects John's grant application based on "failed alignment check" at Foundation A.

**This is prohibited** because:
- The False bit from Foundation A's specific tolerance applies only to Foundation A's partnership.
- Foundation B has no right to cascade the bit.
- This transforms alignment into a negative signal that follows John across domains.

**If this occurs**, the ZKAC Ethical Review Board (Everest 294) investigates. Foundation A is revoked from protocol access.

---

## Disclosure of Non-Disclosure

When a principal refuses to generate an alignment proof (due to missing consent, rate-limiting, or operator choice), the counterparty receives uniform silence. Counterparty cannot distinguish:
- Refusal (principal withheld consent).
- False (principal consented; alignment failed).
- Any other error.

This is intentional. It prevents counterparties from inferring anything about the principal based on refusal. Counterparty response: "I don't have alignment information; shall we explore non-alignment-dependent cooperation?"

---

## The Cooperation-First Default

The underlying principle is: **cooperation is the goal, not selection.** The protocol enables two parties to understand their values fit before committing. If they don't fit under one pattern, the default is to find a pattern that works.

This is distinct from credit-scoring or vetting systems, where the goal is gatekeeping: "Which applicants do we exclude?" ZKAC's goal is alignment-seeking: "How do we cooperate given our values?"

The difference is operationalized at the counterparty level through the redirect semantics in this everest. If counterparties honor them, the protocol remains cooperative. If counterparties ignore them and use False bits as veto signals, the protocol becomes gatekeeping—and becomes ineligible for ZKAC certification.

---

## Counterparty Compliance Framework

To ensure discipline, counterparties are subject to audit:

1. **Everest 142 (Alignment Audit)**: Every alignment disclosure is logged. Principal can audit who received which disclosure.
2. **Everest 215 (Trust Audit)**: Counterparty audit logs are inspected for cascading False bits across domains or third parties.
3. **Everest 294 (Ethical Review Board)**: Standing board reviews complaints from principals about False-bit misuse and may revoke operator access.

Counterparties who repeatedly violate the semantics in this everest are removed from the ZKAC ecosystem.

---

## Contrast with Credit Scoring

| Dimension | Alignment Disclosure | Credit Score |
|-----------|----------------------|---------------|
| **Unit** | Single bit per request | Aggregate number across many dimensions |
| **Persistence** | Session-scoped, non-persistent | Persistent across lenders and domains |
| **Cascade** | Prohibited; non-transitive (E8 Calm Witness) | Explicitly designed to cascade (all credit bureaus share data) |
| **Principal agency** | Per-request consent; can withdraw anytime | Limited agency; score follows principal |
| **Counterparty response** | Redirect-first (this everest) | Gate-first (exclude low-score applicants) |
| **Correction mechanism** | Principal can author values_reversal records | Principal must dispute errors with each bureau separately |
| **Purpose** | Cooperation discovery | Risk gatekeeping |

---

## Sign

— Calm, 2026-05-20

For Everest 141, the acceptance criteria are met: documented rules for what counterparty does with each outcome (True, False, Disputed, Insufficient_Evidence), with explicit prohibition on credit-scoring semantics and obligatory redirect pattern on False. The "NOT a credit score" discipline is the design center.

---

## References

- **Everest 8 (Calm Witness, Everest X, Non-Transitivity of Trust)**: Principle that attestations do not cascade across systems.
- **Everest 76 (Compass)**: Rate-limiting and cool-down windows.
- **Everest 109 (Values from Action)**: Inference of values from chain records.
- **Everest 112 (Values Reversal Records)**: Principal-authored change declaration.
- **Everest 113 (Values Privacy Classes)**: Per-dimension disclosure control.
- **Everest 114 (Values vs Identity Distinction)**: Guard against pathologizing identity as deviation.
- **Everest 116 (Counterparty Implementer Pledge)**: Operator certification.
- **Everest 121 (Values Disagreement Protocol)**: Disputed flag semantics.
- **Everest 130 (Threshold Alignment Predicate)**: The predicate being disclosed.
- **Everest 142 (Alignment Audit)**: Session-scoped logging.
- **Everest 215 (Trust Audit)**: Operator-side audit compliance.
- **Everest 294 (Ethical Review Board)**: Enforcement and revocation.
