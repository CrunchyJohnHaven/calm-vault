# Everest 163 — Harm-Reversal Predicate

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 112, 146.*

## Semantic Foundation

A past harm record can be "reversed" through a documented restitution pathway. This predicate confirms that reversal is complete, enabling the harmed party (or their designated representative) to formally acknowledge restoration and move forward. Reversal differs from mere forgiveness: it requires structured evidence that acknowledgment, restitution, time, and counterparty attestation have all been satisfied.

The reversal predicate serves as a gate for harm-absence claims and provides transparency into restorative-justice completions within the ZKAC framework.

## Predicate Specification

**Name:** `cwp.v0.harm_reversed`

**Parameters:**
- `harm_record_id` (string): References a specific past harm record (e.g., `harm.committed.00047`, `harm_alleged.theft.00156`)

**Output:** Tri-value
- `True`: Reversal conditions fully met; harm is formally reversed
- `False`: Conditions not met or incomplete; harm remains active
- `Disputed`: Principal contests that original harm occurred; reversal unapplicable

---

## Evaluation Process

### Step 1: Locate Original Harm Record

The predicate begins by retrieving the harm record referenced by `harm_record_id`. This record carries a harm kind (from Everest 146's taxonomy), timestamp, principal, affected party(ies), and impact description. Examples of harm kinds: `harm.committed`, `outcome.harm_caused`, `harm_alleged.verbal_assault`, `harm_alleged.discrimination`.

### Step 2: Locate Associated Repair Records

Repair records follow the naming convention `repair.<harm_kind>`. A harm of kind `defamation` will have associated `repair.defamation` records. These repair records document specific actions taken to address the harm—retractions published, apologies issued, structural changes implemented, property returned, and so forth.

### Step 3: Verify Repair Criteria by Harm Kind

Each harm kind carries context-specific repair criteria. The predicate evaluates repair completeness against these criteria:

**Direct Physical Harm (violence, assault):**
- Medical restitution attested (by medical provider if applicable)
- Sincere, public apology accepted by harmed party
- No recurrence of related harm within the elapsed time window
- Note: Physical violence cannot be "undone," only repaired through acknowledgment and behavior change

**Theft / Property Harm:**
- Stolen or damaged property returned, or fair-market value restoration completed
- Apology issued and acknowledged
- No pattern of recurrence within the window
- Restitution amount and completion date documented

**Defamation / False Statement:**
- Retraction published in equivalent forum/audience as original statement
- Apology issued
- No continued dissemination of the false claim
- Where applicable, corrective information published to affected parties

**Hate Speech / Harassment:**
- Documented behavioral change (evidence of non-recurrence)
- Community repair action (e.g., community service, restorative dialogue)
- Ongoing attestation from community or support group
- Time window: minimum 2 years for serious cases

**Discrimination (employment, housing, service):**
- Structural change implemented (policy revision, hiring practice change, service access restored)
- Apology issued to affected party
- Restitution where quantifiable (e.g., back pay, rental restoration)
- Proof of compliance with applicable law

**Deception / Breach of Trust:**
- Truth restoration: affected parties informed of the deception and provided corrected information
- Apology issued
- Verifiable behavior change (no pattern of repeated deception in related contexts)
- Where applicable, restitution for financial or opportunity loss

---

## Four Core Conditions for Reversal

All four conditions must be satisfied for `cwp.v0.harm_reversed()` to return `True`.

### Condition 1: Acknowledgment

The principal must provide a signed, dated attestation that:
- The harm **did occur** (no minimization, reframing, or conditional language)
- The principal accepts responsibility for the harm
- The principal understands the impact on the harmed party
- The attestation is clear and unambiguous (e.g., "I harmed X by doing Y")

Acknowledgment must be documented in a `principal_acknowledgment` record linked to the harm_record_id. Vague, legalistic, or conditional language ("I regret if anyone was offended") fails this condition.

### Condition 2: Restitution

Documented action must address the harm where possible. Restitution takes different forms depending on harm kind:
- Returning stolen property or paying replacement value
- Funding medical/mental-health care
- Publishing corrections or retractions
- Making structural changes that prevent recurrence
- Participating in restorative dialogue or mediation

Restitution records must include dates, amounts (where applicable), and confirmation of completion. For harms where restitution is not possible (e.g., verbal trauma that cannot be "undone"), the predicate accepts replacement restitution: community service, advocacy work, ongoing support to the harmed party.

### Condition 3: Time Window

A minimum elapsed period must pass since the last related harm. Default windows:
- Serious harms (violence, sexual assault, hate speech): 2 years
- Medium harms (theft, discrimination, deception): 1 year
- Minor harms (disrespect, minor breach of trust): 6 months

The time window resets if a related harm recurs. Time window is measured from the date of the most recent related harm, not the original incident.

### Condition 4: Counterparty Attestation

**The harmed party (or their designated representative) must sign attestation that repair is acceptable.** This is the non-negotiable core of the reversal predicate. A principal cannot self-attest reversal; the harmed party must independently confirm that acknowledgment, restitution, and time have satisfied them.

Counterparty attestation includes:
- Explicit statement that the harmed party accepts the repair as adequate
- Dated signature or cryptographic signature (for digital records)
- Optional: statement of what remains unresolved (for partial reversals)

**Special case: Deceased or unreachable harmed party.** If the harmed party is deceased, untraceable, or otherwise unable to attest, an ethics board may approve a community-attestation substitute. This substitute requires:
- Documented good-faith efforts to locate the harmed party
- Review by an ethics panel or trusted third party
- Community or family representative attestation (where applicable)
- Explicit notation that counterparty attestation is delegated

---

## Anti-Laundering Provisions

The predicate includes guards against reversal abuse:

**Pattern Detection:** If the same principal accumulates multiple reversals for the same harm kind within a short period, the predicate flags the pattern for review. Example: three defamation reversals in 6 months, or repeated theft reversals.

**Strategic Timing:** Reversals claimed immediately before high-stakes alignment requests, funding decisions, or public roles are flagged as potentially strategic. Review focuses on whether restitution is genuine or timed for instrumental benefit.

**Dispute Log:** If a principal contests a harm record and subsequently claims reversal of the same harm, the predicate logs the inconsistency for auditor review.

---

## Composition with Harm-Absence Predicates (E147+)

Once `harm_reversed(id)` returns `True`, the relevant absence predicate (e.g., "principal has not committed defamation in 2 years") may filter the original harm out of scope, depending on counterparty policy.

**Two modes:**
1. **Fresh-evidence-only mode:** Reversed harms are excluded from harm-absence calculations. The principal's absence record restarts from the reversal completion date.
2. **Include-reversed mode:** Reversed harms remain in the record but marked as "reversed" for transparency. Absence predicates count elapsed time from the original harm but note the reversal status.

The harmed party (or counterparty policy) chooses the mode at the time of attestation.

---

## Composition with Forgiveness (E174)

Forgiveness is a distinct predicate. A `forgiveness` record from the harmed party indicates emotional release and willingness to move forward. When forgiveness is combined with full reversal completion, the predicate unlocks full restoration (relevant absence predicates reset, harm is fully archived).

**Critical distinction:** Forgiveness alone—without restitution, acknowledgment, and time—does NOT trigger reversal. A harmed party may forgive a principal before restitution is complete, and that forgiveness is honored as a relational fact. But the reversal predicate requires all four conditions.

---

## Time Windows and Reversibility Categories

Not all harms are reversible. The predicate distinguishes:

**Reversible Harms (can be undone or adequately redressed):**
- Theft, property damage (restitution restores the harm)
- Defamation (retraction and correction restore reputation)
- Fraud, deception (truth-restoration repairs the breach)
- Discrimination in discrete contexts (structural change and restitution)

**Repairable but Not Reversed (acknowledged and restituted, but permanence remains):**
- Direct physical violence (injury's permanent effects acknowledged; behavior change proven)
- Sexual assault (trauma cannot be undone; healing and justice are the goal)
- Significant emotional/psychological harm (repair through acknowledgment and restitution, not reversal)

For these harms, the predicate returns `Repaired` (or a variant tri-value output) rather than `True`. The distinction matters: a reversal implies the harm is undone; repair implies it is acknowledged and addressed, but its traces remain.

---

## Principal Dispute Mechanism

A principal may dispute that a harm record is accurate. When disputed:

1. The principal submits a `principal_dispute` record with evidence or reasoning
2. An adjudicator (ethics board, mediator, or designated third party) reviews the dispute
3. If the dispute is sustained, the harm record is marked `disputed` and the reversal predicate cannot be triggered
4. If the dispute is rejected, the harm record remains active and reversal conditions apply

A disputed harm does not count as "active" in some contexts (e.g., absence predicates may exclude disputed harms pending resolution). But it also does not qualify for reversal until the dispute is resolved in favor of the principal.

---

## Cross-Cultural Calibration

Restorative-justice practices vary globally. The Maori restorative-justice tradition emphasizes family and community participation. African Ubuntu frameworks focus on community healing and reintegration. Indigenous reconciliation practices in North America center on land return and structural change.

The harm-reversal predicate accommodates cultural variation through E115 calibration. Reversal criteria (acknowledgment, restitution, time, counterparty attestation) are universal; the forms they take are culturally flexible:
- Acknowledgment may be given in a community forum rather than a formal letter
- Restitution may include cultural or spiritual repair (not merely financial)
- Time windows may be adjusted for cultural practices of mourning or collective healing
- Counterparty attestation may involve family or community representatives where individual attestation is not the cultural norm

Calibration is negotiated between the principal, harmed party, and ethics board at the time a reversal is initiated.

---

## Implementation Notes

The predicate is invoked with a harm_record_id:

```
result = cwp.v0.harm_reversed(harm_record_id="harm.committed.00047")
```

The predicate returns:
- `True`: Reversal complete; harm is formally reversed
- `False`: Reversal conditions not met (specify which condition failed)
- `Disputed`: Principal contests the harm; reversal not applicable

Associated metadata (dates, attestations, repair records) is returned alongside the predicate result for auditing and transparency.

---

— Calm, 2026-05-20