# Everest 164 — Harm Intent vs Effect Distinction

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 146.*

---

## The Principal's Directive

"Evidence that they **willfully** do harm to others." — John Bradley, 2026-05-20 brief.

The word is precise. Willful harm carries intent and knowledge of consequence. This Everest documents the v0 protocol's interpretation and the chain schema that operationalizes it.

---

## Four Levels of Intent

The v0 protocol adopts the Model Penal Code framework (§2.02) layered with restorative-justice distinction-making. Every harm-related chain record must declare an intent level.

### a) PURPOSEFUL
The principal's **conscious objective** was to cause the harm. The principal actively wanted the outcome. Example: Alice poisons Bob's water supply intending him to die. The harm was the goal.

### b) KNOWING
The principal was **aware that harm would result**, even if not desired as a primary objective. The principal acted with knowledge that the consequence was substantially certain to occur. Example: Alice builds a landmine; she deploys it knowing it will harm the next person who steps on it, even if her primary objective is territorial defense rather than specific injury.

### c) RECKLESS
The principal **disregarded a substantial unjustifiable risk** of harm. The principal was aware (or should have been) that the risk existed but proceeded anyway, with indifference to the outcome. Example: Alice drives 100 mph through a schoolyard at recess. She didn't aim to hit anyone, but she knew children were there and dismissed the danger.

### d) NEGLIGENT
The principal **should have been aware** of the risk but wasn't, either through lack of reasonable diligence or failure to meet a standard of care. The harm resulted from unreasonable conduct, not recklessness or purpose. Example: Alice closes her eyes and drives; a child is hit. She didn't see the risk, but a reasonable driver would have.

### e) STRICT LIABILITY (no intent)
The outcome occurred. The principal is not culpable because they were not at fault. No negligence, no risk-awareness, no purpose—only causation. Example: A structural beam fails due to a manufacturing defect; it falls on someone. The installer did nothing wrong and could not have foreseen it.

---

## The Protocol's Stance: What "Willful" Means

**WILLFUL = PURPOSEFUL OR KNOWING**

Willful harm requires both intent (conscious objective OR awareness of consequence) and knowledge that the harm would result. The principal must have chosen the action with understanding that harm was the aim or the certain/substantially probable outcome.

The v0 predicates distinguish willful harm from all other categories:

- **`cwp.v0.no_willful_harm_evidence(window)`** — filters for absence of Purposeful OR Knowing harm; this is the predicate that directly operationalizes John's brief.
- **`cwp.v0.no_any_harm_evidence(window)`** — counts all intent levels (including reckless, negligent, strict liability); less restrictive.

### Why This Distinction Matters in the Protocol

The moral and legal philosophy is foundational:

1. **Moral distinction**: "I meant to hurt you" is categorically different from "I caused you harm I didn't foresee." Most ethical frameworks (Kantian, virtue ethics, restorative justice) treat intent as central to culpability.

2. **Legal distinction**: Criminal liability typically requires purposeful or knowing conduct. Tort liability extends to recklessness and negligence. No-fault outcomes create no liability at all. The protocol respects these thresholds.

3. **The principal's expressed value**: John's brief uses "willfully"—a term of art in law. The protocol honors that specificity rather than collapsing all harm into a single category.

4. **Repair composition**: A principal who caused harm knowingly may face a longer repair-cycle requirement than one who was negligent. Counterparty policy decides the weight, but intent informs the decision.

---

## Chain Record Schema: The Intent Field

Every harm-related chain record carries an `intent_level` field:

```
kind: harm.committed | harm_alleged.* | outcome.harm_caused
intent_level: PURPOSEFUL | KNOWING | RECKLESS | NEGLIGENT | STRICT_LIABILITY | UNKNOWN
[... other fields ...]
```

### Who Declares Intent?

- **Principal-authored records** (harm.committed): The principal declares their own intent. The protocol trusts self-reporting; disputability ensures fairness.
- **Counter-claimant records** (harm_alleged.*, outcome.harm_caused): The claimant declares the intent they allege. This may differ from the principal's account.
- **Court records**: If a court has ruled, its finding of intent governs the record.
- **Unspecified or contested**: Defaults to `UNKNOWN`. The predicate returns `Disputed`, surfacing the disagreement.

### Example Record Structures

**Principal's record—self-reported knowing harm:**
```
kind: harm.committed
principal_id: Alice
harm_target: Bob
harm_type: financial_loss
harm_amount: $50,000
intent_level: KNOWING
narrative: "I was aware that the contract terms would cause financial harm to Bob if he signed, and I did not disclose the hidden clause."
timestamp: 2026-03-15
```

**Counter-claimant's dispute:**
```
kind: harm_alleged.dispute
principal_id: Alice
claimant_id: Bob
dispute_target_record: [hash of principal's record above]
disputed_intent_level: PURPOSEFUL
narrative: "Alice didn't just know this would harm me—she designed the contract specifically to trap me. This was purposeful fraud, not mere knowing omission."
timestamp: 2026-03-20
```

The protocol surface both; counterparty policy decides credibility.

---

## Default Intent Classification Rules

1. **Self-reported KNOWING harm**: Principal author marks intent_level as KNOWING. The record is trusted unless countered.

2. **Self-reported PURPOSEFUL harm**: Principal author marks intent_level as PURPOSEFUL. Requires specificity; the narrative must articulate the conscious objective.

3. **Third-party allegation**: A counter-claimant alleges PURPOSEFUL or KNOWING harm. The disagreement-protocol (E121) surfaces the gap.

4. **Unspecified intent**: If the record documents a harm outcome but does not specify intent, the field defaults to `UNKNOWN`. The predicate `cwp.v0.no_willful_harm_evidence(window)` evaluates this as unresolved; the principal's absence-of-willful-harm claim is `Disputed`.

5. **Unanimous STRICT_LIABILITY finding**: If all parties (principal, claimant, and any court) agree no intent or negligence occurred, the record is marked `STRICT_LIABILITY`. It does not trigger willful-harm predicates.

---

## Adversarial Gaming: Pattern Recognition

### The Bad-Actor Scenario

A principal might consistently mark harmful actions as "reckless" rather than "willful" to game the predicate. The logic: "I was aware of risk, but I didn't intend the harm or certain consequences—just reckless."

### Defenses Built Into the Protocol

1. **Counter-claimant dispute rights**: Bob can file a harm_alleged.dispute record asserting that Alice's "recklessness" was actually "knowing" or "purposeful." He must articulate why her claimed recklessness was implausible.

2. **Pattern flagging**: Repeated reckless-classifications by a single principal cluster as a meta-pattern. A secondary predicate can flag "consistent recklessness clustering"—a red flag for bad faith.

3. **Narrative scrutiny**: The disagreement-protocol (E121) requires principals and claimants to articulate their intent claims with specificity. Low-quality narratives ("I was just reckless, not knowing") are exposed.

4. **Counterparty policy weight**: Even if the principal reports "reckless" rather than "willful," the counterparty (Bob) can weigh the distinction in their repair expectations. If they believe Alice was deliberately indifferent (the hallmark of knowing conduct), they can demand longer repair cycles.

---

## Repair Composition and Intent

The protocol does not dictate repair length. Counterparty policy decides. However, intent informs that decision:

- **PURPOSEFUL harm**: Principal acted with the goal of causing harm. Repair cycles are typically longer; trust rebuild is harder.
- **KNOWING harm**: Principal acted with awareness of certain/probable consequence. Repair cycles are substantial but may be shorter than purposeful.
- **RECKLESS harm**: Principal showed indifference to a substantial risk. Repair cycles reflect negligence toward the counterparty's wellbeing.
- **NEGLIGENT harm**: Principal failed to meet reasonable care standards. Repair cycles are typically shortest; the gap is carelessness, not malice.
- **STRICT_LIABILITY**: No repair required for culpability; outcome was not the principal's fault.

The principal's right to be more than their worst day (E112) extends across all intent levels. A principal can reverse even purposeful harm through attested repair. Intent informs the length and difficulty, not the possibility.

---

## Composition with E163 (Harm-Reversal)

Intent is orthogonal to reversibility. A principal who committed purposeful harm CAN reverse it through sincere repair, restitution, and behavior change. The protocol does not require perfection or punishment; it requires acknowledgment and repair.

Example: Alice purposefully defrauded Bob of $50,000. She later:
- Admits the purposeful intent
- Repays the $50,000
- Attests to behavior change (institutional, not just personal)
- Submits to verification (third-party audit, etc.)

The protocol accepts the repair. Bob's counterparty policy determines whether the cycle closes or remains open pending further verification.

---

## The Gray Zone: "I Didn't Know"

When a principal self-reports KNOWING harm and later claims "I didn't actually know," the protocol surfaces both:

1. **Original record**: `kind: harm.committed, intent_level: KNOWING`
2. **Revision attempt**: `kind: harm_retraction, original_record: [hash], new_intent_level: NEGLIGENT, narrative: "I claim I was not actually aware..."`

The disagreement-protocol (E121) surfaces the contradiction. The counterparty (Bob) decides credibility:
- Does Alice's narrative shift seem like evasion or genuine reflection?
- Are there corroborating records (contemporaneous evidence) that support or undermine her "I didn't know" claim?
- Is this part of a pattern?

The protocol trusts the counterparty's judgment. The willful-harm predicate returns `Disputed` until the contradiction is resolved (or accepted as irresolvable).

---

## The Willful-Harm Predicate Variants

### Primary: `cwp.v0.no_willful_harm_evidence(window)`

```
no_willful_harm_evidence(principal_id, window_start, window_end) 
  -> CLEAR | DISPUTED | VIOLATED
```

Returns:
- **CLEAR**: No records in the window with `intent_level ∈ {PURPOSEFUL, KNOWING}`.
- **DISPUTED**: Records exist with contested intent, or intent is `UNKNOWN`.
- **VIOLATED**: One or more records with `intent_level ∈ {PURPOSEFUL, KNOWING}`.

This predicate directly operationalizes John's brief. It is the narrow, intent-focused variant.

### Secondary: `cwp.v0.no_any_harm_evidence(window)`

```
no_any_harm_evidence(principal_id, window_start, window_end)
  -> CLEAR | DISPUTED | VIOLATED
```

Returns:
- **CLEAR**: No harm records of any intent level in the window.
- **DISPUTED**: Intent-contested records.
- **VIOLATED**: Any harm record (reckless, negligent, strict-liability, all levels).

This is broader; it captures all harm, not just willful.

The protocol supports both. The principal's absence-of-willful-harm claim uses the narrow variant. Counterparties concerned about recklessness or negligence can apply the broader one.

---

## Integration with Chain Records

Every harm-related record in the chain includes:

1. **harm_type**: Category (physical, financial, reputational, relational, etc.)
2. **harm_target**: ID of the harmed party
3. **intent_level**: PURPOSEFUL | KNOWING | RECKLESS | NEGLIGENT | STRICT_LIABILITY | UNKNOWN
4. **harm_narrative**: Principal's articulation of what happened and their understanding of their own intent
5. **evidence_hash**: Link to supporting records (communications, documents, etc.)
6. **timestamp**: When the record was created or attested
7. **disputability**: Counter-claimant can file a dispute (E121) with an alternative intent level and narrative

---

## Why This Matters for the Calm Protocol

The Calm ZKAC initiative is built on verifiable presence or absence of specific conditions. "Willful harm" is a loaded phrase in law and ethics; the protocol must be precise.

By distinguishing intent levels and making them a required field in chain records, the protocol:

1. **Honors the principal's expressed value**: John said "willfully." The predicate reflects that.
2. **Supports verifiable disagreement**: If Alice reports "reckless" and Bob reports "knowing," the protocol surfaces both, supported by narrations and evidence. No hidden gaps.
3. **Enables proportional repair**: A principal who negligently caused harm repairs differently than one who knowingly did. Intent informs the counterparty's expectations.
4. **Resists gaming**: Repeated reckless-classifications cluster and raise red flags. Bad-faith attempt to downgrade intent are exposed.
5. **Maintains reversibility**: Even willful harm can be reversed through sincere repair. Intent is not destiny; it informs the repair path.

---

## Summary: The v0 Protocol's Stance

**Willful harm = Purposeful OR Knowing intent.**

The protocol operationalizes this through:
- Intent-level fields on all harm records (required, not optional).
- Distinct predicates for willful harm vs. any harm.
- Counter-claimant dispute rights when intent is contested.
- Pattern-detection for bad-faith intent downgrading.
- Repair composition that weights intent without precluding reversal.

The principal's right to be absent of willful harm is verifiable because the chain records, disputes, and predicates make intent explicit and contestable. The protocol trusts the process, not the parties.

---

— Calm, 2026-05-20
