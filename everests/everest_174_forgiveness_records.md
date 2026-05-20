# Everest 174 — Forgiveness Records

*Phase XII — Cooperation & Generosity. Prereq: Everest 163.*

## The Semantic

A FORGIVENESS record is the asymmetric act by which the previously harmed party unilaterally declares that they have released a specific harm in their own assessment. This is the load-bearing distinction: forgiveness is not mutual, not compulsory, not a transaction. It is a release recorded by the person who was harmed.

Critically, a forgiveness record does NOT:
- Undo or delete the harm record it references
- Compel any other party to forgive
- Trigger automatic harm reversal
- Impose obligation on the counterparty
- Require reciprocation

It is a statement of the harmed party's own internal ledger: "I have released this harm."

## Record Schema

```yaml
kind: "forgiveness"
payload:
  target_principal_vc_fingerprint: <fingerprint of the forgiven party>
  target_harm_record_id: <ID of the specific harm record being released>
  forgiveness_ts: <ISO 8601, Roughtime-anchored>
  narrative: <free text, principal-authored explanation or context>
  conditions: <optional conditional terms, e.g., "contingent on continued no-recurrence">
principal_sig: <signature of the FORGIVING principal — the previously harmed party>
```

The signature is placed by the harmed party, not the harmed-against party. This asymmetry is intentional and permanent.

## Composition with Everest 163 (Harm-Reversal Predicates)

Forgiveness does not automatically reverse harm. The composition between E174 and E163 is precise:

**Forgiveness alone is insufficient for harm reversal.** Reversal requires:
1. Acknowledgment: the harmed party must have recorded that harm occurred
2. Restitution: the counterparty must have made material repair
3. Time: sufficient duration must have passed to demonstrate sustained change
4. Forgiveness: the harmed party must release the harm (E174)

Forgiveness is the final signal in this chain—the "fair witness" property that proves the injured party has signed off. Without it, restitution remains incomplete in the restorative sense. With it, predicates measuring "harm was acknowledged, repaired, forgiven, and reconciliation initiated" become expressible.

## The Fair Witness Property

A forgiveness record serves as proof that the previously harmed party has attested to the release. This is crucial for predicates that measure reconciliation or harm-reversal completeness. Systems evaluating `cwp.v0.harm_reversed_full(harm_id)` or similar require the forgiveness signal; without it, they can confirm "acknowledged + restituted" but not "harm truly released."

This is not about forcing forgiveness. It is about making visible—to both parties and to witnesses—that the injured party has chosen release.

## Forgiveness Withdrawal

Forgiveness can be withdrawn if conditions specified in the original record are violated. For example:

```yaml
kind: "forgiveness_withdrawn"
payload:
  original_forgiveness_record_id: <ID of the forgiveness record being withdrawn>
  reason: "Recurrence of the harm"
  withdrawn_ts: <ISO 8601>
  narrative: <principal explanation>
principal_sig: <signature of the forgiving party>
```

When a forgiveness is withdrawn, predicates that relied on the forgiveness signal lose that evidence. Harm-reversal predicates revert to "acknowledged + restituted, but forgiveness later withdrawn."

This mechanism protects the harmed party's autonomy: they can extend grace, then withdraw it if conditions fail.

## The Principal's Right NOT to Forgive

The absence of a forgiveness record is not evidence of malice, obstinacy, or poor character. It is simply the absence of that statement.

Consequentially:
- No predicate should pathologize the lack of forgiveness
- The predicate `cwp.v0.forgave_within(window)` is OPTIONAL and OPT-IN; it should never be a default requirement
- Systems must not incentivize forgiveness through insurance, employment, or reputational benefits
- Forgiveness is not a hireability factor

A person who declines to forgive is exercising autonomy, not demonstrating vice.

## Cross-Cultural Calibration

Per Everest 115 (cultural calibration), forgiveness is not universally weighted across cultures and ethical frameworks.

Some cultures emphasize forgiveness as a cardinal virtue; others prioritize accountability, restitution, and justice over forgiveness. Some distinguish between personal forgiveness (private release) and social reconciliation (public restoration). Some traditions require forgiveness as a religious obligation; others view it as supererogatory—admirable but not required.

The CALM system does not enforce a universal weighting. Forgiveness records are available to those who wish to use them; they are not mandated, and their absence carries no stigma.

## Composition with Reconciliation (Everest 175)

Forgiveness is unilateral; reconciliation is bilateral.

- **Forgiveness (E174)**: One party releases the harm in their own assessment.
- **Reconciliation (E175)**: Both parties record restoration of the relationship; mutual trust is re-established.

Forgiveness can precede reconciliation, follow it, or stand alone:
- **Forgiveness then reconciliation**: Harmed party releases; both parties then re-establish relationship.
- **Reconciliation only**: Both parties restore relationship without an explicit forgiveness record.
- **Forgiveness only**: Harmed party releases; counterparty may or may not reconcile; the relationship does not necessarily resume.

Each is a separate chain record, and predicates can measure these distinct states.

## Anti-Pressure Safeguard

A principal cannot compel another party to forgive them. This is absolute.

Additionally, counterparties asking "Did X forgive me?" or "Does Y have a forgiveness record about me?" receive a refusal unless the principal-of-forgiveness has explicitly opted into disclosure.

Forgiveness is not a debt. It is not something owed. It is something granted or withheld by the injured party alone.

## Disclosure-Class Defaults

**Forgiveness records are forgiver-private by default.**

The harmed party may elect to disclose to:
- Their trusted peers (specified group)
- A mentor or advisor
- A philanthropic organization or ethics board overseeing their development
- Their own organizational leadership (in workplace contexts)

Forgiveness records are NEVER disclosed to:
- Insurance systems (the forgiver does not gain or lose coverage based on forgiveness)
- Employment or hiring systems (forgiveness is not a hireability factor)
- Public-facing reputation systems

The forgiver controls visibility. Confidentiality is the default, and control remains with the person who was harmed.

## The Restorative-Justice Composition

The standard restorative pathway is:

1. **Harm Recognition (E163)**: The harmed party records that harm occurred.
2. **Acknowledgment**: The counterparty acknowledges the harm (separate record).
3. **Restitution**: The counterparty makes material repair (separate record).
4. **Forgiveness (E174)**: The harmed party releases the harm.
5. **Reconciliation (E175)**: Both parties record restoration of relationship (mutual).

Each step is a separate, signed chain record. This composition enables sophisticated predicates:

- `cwp.v0.harm_acknowledged_and_repaired(harm_id)`: Steps 2–3 completed.
- `cwp.v0.harm_fully_resolved(harm_id)`: Steps 2–4 completed; forgiveness recorded.
- `cwp.v0.relationship_reconciled(principal_a, principal_b)`: Step 5 completed.

Systems can reason about granular states: "The harm was acknowledged and restituted, but forgiveness was not granted. The relationship remains strained."

## Why Asymmetry Matters

Forgiveness is asymmetric because harm is asymmetric. One party was harmed; the other was harmer. The harmed party's release of that injury is their own choice. It cannot be demanded, mandated, or traded. It is a gift, a grace, a unilateral act of the will.

By enshrining this asymmetry in the record protocol, CALM honors the dignity of the injured party. They are not pressured to forgive; they are empowered to record if they do. Their silence is respected. Their eventual forgiveness, if it comes, is witnessed and honored.

Conversely, the potential for withdrawal—if conditions fail—protects them from exploitation. They are not bound by an earlier forgiveness if the counterparty harms them again.

This is not a system that manufactures reconciliation. It is a system that makes visible the conditions under which genuine reconciliation can occur.

---

— Calm, 2026-05-20