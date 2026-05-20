# Everest 175 — Reconciliation Records

*Phase XII — Cooperation & Generosity. Prereq: Everest 174.*

## Overview

Reconciliation records mark the point where two or more parties who have experienced harm move beyond individual forgiveness into mutual restoration of cooperative relationship. Where Everest 174 (Forgiveness Records) captures the unilateral act of the harmed party releasing resentment, Everest 175 captures the bilateral or multilateral agreement that cooperation is restored. Both parties' chains must hold matching records for the reconciliation to be valid.

The core acceptance criterion is `kind: "reconciliation"` — and the critical requirement is symmetry: every involved party records the same reconciliation event. Without this bilateral or multilateral mirroring, no valid reconciliation has occurred in the protocol's understanding. The protocol does not recognize one-sided claims of restoration.

## Semantic Foundation

A reconciliation record asserts: "We have restored a cooperative relationship after harm." This is stronger than forgiveness alone. Forgiveness answers the question "Do I release my resentment toward you?" Reconciliation answers the joint question "Are we together again, and under what terms?"

The record type is fundamentally **participant-symmetric**. All involved parties must independently sign and chain the same reconciliation record. This creates an auditable state where any third-party auditor can verify that participant A's chain contains a matching record to participant B's chain, establishing that both witnessed and endorsed the same reconciliation narrative.

## Record Schema

Each reconciliation record contains:

**kind**: "reconciliation"

**payload**:
- `participants_vc_fingerprints`: Array of VC fingerprints for all parties to the reconciliation. For a bilateral case, two fingerprints. For a community-level repair, three or more.
- `referenced_harm_record_ids`: Array of harm record identifiers that prompted this reconciliation. Links back to the original injury.
- `referenced_forgiveness_record_ids`: Optional array of prior forgiveness records, if forgiveness was explicitly extended before reconciliation. Recognizes the sequence: harm → acknowledgment → forgiveness → reconciliation.
- `reconciliation_ts`: Timestamp anchored to Roughtime. Establishes when parties agreed reconciliation had occurred.
- `shared_narrative`: Free-text description, agreed upon by all participants, of what reconciliation means in this specific context. Not prescriptive; accounts for cultural, relational, and situational diversity.
- `relationship_status_post`: Enum with four possible values:
  - `restored`: Relationship returned to pre-harm state or reasonable equivalent.
  - `transformed`: Relationship is fundamentally different post-harm, but parties accept and honor the new form.
  - `concluded_amicably`: Parties agree the relationship is ending, but without ongoing resentment.
  - `ongoing_repair`: Parties commit to continued collaborative work; reconciliation is not yet complete but is underway.

**signatures**: Dictionary mapping each participant's VC fingerprint to their cryptographic signature over the payload. All participants must sign for the record to be valid.

**record_hash**: Cryptographic hash of the complete reconciliation record, used for identity and chain references.

## The Matching Requirement

For reconciliation to be valid in the CALM protocol, **identical records (matching payload hash) must appear in every participant's chain**. This is the lynchpin of the reconciliation model. If participant A records a reconciliation and participant B does not, the protocol does not recognize a reconciliation. If participant A records one narrative and participant B records a different one (even if nominally about the same harm), reconciliation is not established.

Cross-chain verification means an auditor can walk through:
1. Participant A's chain: locate reconciliation record R.
2. Participant B's chain: locate the identical record R.
3. Verify both records contain both parties' signatures.
4. Verify record_hash matches across chains.

This creates a strong guarantee: both parties affirmatively recorded and endorsed the same reconciliation statement.

## Multilateral Cases

When three or more parties are involved—such as a team that experienced internal conflict, or a community working through collective harm—all participants sign and chain the same record. The protocol supports threshold variants for community-level repair: for instance, "k of n parties have reconciled" allows partial healing to be recorded when immediate universal buy-in is unrealistic, while still maintaining the core bilateral symmetry for those who do participate.

## Relationship Status Semantics

The `relationship_status_post` enum enables honest representation of post-harm relationships:

**Restored**: The relationship is judged by participants to have returned to a cooperative state approximating its pre-harm form. Common in cases where harm was discrete, acknowledged, addressed through restitution, and forgiven.

**Transformed**: Acknowledges that some harms genuinely and permanently change relationships. Two people may reconcile—cease hostility, resume interaction—while accepting that the relationship is no longer what it was. This avoids the false pretense of "returning to normal." The protocol supports honest acknowledgment: "We are at peace, and we are different now."

**Concluded Amicably**: Parties agree the relationship is ending (friendship dissolving, business partnership concluding, etc.), but they do so without ongoing resentment or unresolved harm. Reconciliation enables closure.

**Ongoing Repair**: Parties commit to continued collaborative work on the relationship. Reconciliation is not yet complete; instead, it marks the transition from harm-state to active repair-state. Subsequent records can update: `ongoing_repair → restored` once deeper healing is complete.

## Composition with Other Everests

Reconciliation records integrate with multiple other Everest records:

**With Everest 174 (Forgiveness)**: Reconciliation may reference prior forgiveness records, establishing the sequence of harm → acknowledgment → forgiveness → reconciliation. Not all reconciliations require prior explicit forgiveness records (parties may move directly to reconciliation), but the reference is available.

**With Everest 112 (Values Reversal)**: When harm stems from value misalignment, values reversal records can be composed with reconciliation to show that parties have realigned around shared principles.

**With Everest 163 (Harm Reversal)**: Restitution and harm-reversal records can be referenced in reconciliation, establishing that material restoration preceded relational restoration.

**With Everest 120 (Witness Attestations)**: Reconciliation can include witnesses—such as mediators, community leaders, or trusted third parties—who attest to the reconciliation process. Witness signatures support but are not required for validity. Witnesses establish that the reconciliation was not coerced and was conducted transparently.

## The Strongest Harm Predicate

Everest 175 enables the protocol's strongest claim about harm resolution:

```
cwp.v0.harm_fully_reconciled(harm_record_id) → Boolean
```

This returns `True` if and only if:
1. Original harm record exists in participant chains.
2. Harm acknowledgment has been recorded by the responsible party.
3. Restitution or harm-reversal has been recorded.
4. Forgiveness from the harmed party has been recorded.
5. Reconciliation between parties has been recorded (matching records in all chains).
6. Sufficient time has elapsed in post-reconciliation window.
7. No recurrence of similar harm within the specified time window.

This predicate represents the protocol's highest confidence statement: "This harm was not merely acknowledged or forgiven in isolation—it was fully processed through mutual restoration, and the relationship has held." It is the closest the protocol comes to asserting "harm was fully handled."

## Anti-Fraud Mechanisms

Reconciliation records carry specific anti-fraud protections:

**Signature Requirement**: All participants must cryptographically sign the reconciliation record. A single forged or missing signature invalidates the record.

**CredexAI VC Defense**: Each participant's fingerprint is anchored to their verifiable credential. Sybil attacks (faking the identity of the harmed party to manufacture false reconciliation) are defended by the VC infrastructure. A fraudulent reconciliation would require compromising or spoofing credentials of multiple parties.

**Counter-Claim Machinery**: If a participant disputes a reconciliation record on their chain, they can file a counter-claim within a specified rebuttal window, flagging the record as disputed. Auditors see the flag and the counter-claim, and do not treat disputed reconciliation as valid.

**Coercion Detection**: Timing patterns are monitored for signs of coerced reconciliation (e.g., reconciliation forced immediately after harm with no restitution window, or reconciliation records appearing simultaneously in multiple chains with no legitimate coordination pathway). Per-party rebuttal windows allow any participant to flag potential coercion.

## Disclosure Semantics

Reconciliation records are **participant-private by default**. Each participant controls the disclosure of their copy of the record. This respects the sensitive nature of relational repair.

**Strong disclosure norm**: Cross-participant disclosure—sharing one party's reconciliation record with external parties—requires all-participant consent. This prevents one party from unilaterally publicizing a reconciliation narrative that other parties may not endorse or wish to disclose.

## Cross-Cultural Notes

Reconciliation practices vary widely across cultures, communities, and relational contexts. The protocol intentionally does not prescribe the form or process of reconciliation. The free-text `shared_narrative` field allows parties to record their specific reconciliation in their own cultural and relational language. The `relationship_status_post` enum is broad enough to capture restoration, transformation, conclusion, and ongoing repair across diverse contexts. This enables the protocol to support indigenous reconciliation practices, restorative justice models, religious forgiveness frameworks, and secular relational repair without imposing a single reconciliation template.

## The Transformation Case

Where `relationship_status_post = "transformed"`, the protocol explicitly honors relationships that are permanently changed by harm. Some harms cannot be undone; relationships genuinely evolve after serious injury. Rather than pretending restoration to a pre-harm state, the transformation case allows parties to acknowledge: "We have processed this harm, we are no longer in conflict, but we are not the same. We have a new relationship now, and we accept it."

This is often more honest than enforced restoration narratives, and the protocol's support for it recognizes that reconciliation sometimes means truthfully acknowledging change rather than denying it.

## Integration with the Broader Protocol

Everest 175 sits at the apex of the harm-resolution sequence in Phase XII (Cooperation & Generosity). It represents the strongest mutual commitment to relational healing the protocol supports. It requires:
- Prerequisite work: Everest 174 (forgiveness), Everest 163 (harm reversal), acknowledgment chains.
- Mutual participation: all parties must be willing to chain the same record.
- Honest narrative: shared description of what reconciliation means in context.
- Temporal commitment: acceptance of an ongoing relationship or bounded closure.

Together with witness attestations, counter-claim machinery, and the `harm_fully_reconciled` predicate, Everest 175 establishes that parties have moved beyond harm into active, mutual restoration—or have honestly concluded their relationship without lingering resentment.

---

— Calm, 2026-05-20
