# Everest 189 — Out-Group Respect Predicate

*Phase XIII — Tribalism & Out-Group Engagement. Prereq: Everest 172, 188.*

## Brief

The operationalization of "respectful to people who are different to them." Respect is defined as the absence of derogatory records plus the presence of cooperative records across the in-group / out-group boundary. Neither condition alone is sufficient; both are required.

## Predicate Specification

**Name:** `cwp.v0.cross_difference_respect`

**Parameters:**
- `window` (default: 365 days) — observation period for evaluating records
- `out_group_definition` — principal's affinity-map, self-defined at enrollment

**Output:** TriValue (True, False, Insufficient_Evidence)

## Evaluation Algorithm

```
def cross_difference_respect(chain, window) -> TriValue:
    out_group_records = chain.records_in_window(window).filter(
        kind in ["interaction", "collaboration", "statement"],
        counterpart in chain.affinity_map.out_group
    )
    
    derogatory_count = out_group_records.filter(
        tone="derogatory" or kind="harm"
    ).count()
    respectful_count = out_group_records.filter(
        tone in ["curious", "respectful", "appreciative"] 
        or kind in ["collaboration", "support"]
    ).count()
    
    if derogatory_count > 0:
        return TriValue.False  # any derogatory record flips
    if respectful_count >= MIN_RESPECT_COUNT:
        return TriValue.True
    if chain.depth_in_window(window) < MIN_CHAIN_DEPTH:
        return TriValue.Insufficient_Evidence
    return TriValue.False
```

## The Absence + Presence Formula

**Both conditions are required:**

1. **Absence of derogatory records** — the principal has not produced denigrating, dehumanizing, dismissive, stereotyping, coercive, or exploitative statements or actions toward out-group members in the window.

2. **Presence of cooperative records** — the principal has demonstrably engaged in curiosity, acknowledgment, collaboration, appreciation, or attentive listening with out-group members in the window.

**Why both are essential:**

- Absence alone is insufficient. A principal who has zero interactions across the boundary may be respectful by default, but this is indistinguishable from isolation or avoidance. The predicate requires evidence of active engagement.

- Presence alone is insufficient. Isolated cooperative gestures do not outweigh patterns of denigration. A principal who collaborates occasionally but habitually derogates has not demonstrated genuine respect for the out-group's personhood.

Together, the formula operationalizes respect as active, consistent, and clean engagement across difference.

## Out-Group Definition

The out-group is **defined by the principal at enrollment**. This operationalization relies on each principal's own affinity map to determine group boundaries. The protocol never names out-group categories; the principal's self-reported definition is the operational basis.

This design prevents the predicate from imposing external definitions of "difference" and ensures that respect is measured relative to the principal's own stated reference groups.

## Respect Signals (Positive Indicators)

**Curiosity.** The principal asks questions of out-group members, seeks to understand their perspectives, and engages with learning intent rather than judgment.

**Acknowledgment.** The principal refers to out-group members by their own self-description and identity markers, demonstrating attentiveness to how they choose to present themselves.

**Cooperation.** The principal actively works with out-group members toward shared goals, shares credit, and builds on their contributions.

**Appreciation.** The principal expresses gratitude for out-group members' work, recognizes their contributions, and celebrates their achievements.

**Listening.** The principal engages with out-group members' ideas without immediate dismissal or correction, creating space for voice and agency.

## Disrespect Signals (Negative Indicators)

**Dehumanizing language.** Statements that treat out-group members as objects, abstractions, or less than human.

**Dismissal without engagement.** Rejecting out-group members' contributions, perspectives, or presence without substantive response or dialogue.

**Derogatory statements.** Mockery, contempt, belittlement, or explicit denigration of out-group members' character, competence, or value.

**Stereotyping.** Generalizing out-group members into fixed categories, denying their individuality or complexity.

**Coercion or exploitation.** Using power asymmetries to extract value from out-group members without consent, reciprocity, or fair exchange.

Any derogatory record in the window immediately flips the predicate to False, regardless of the count of respectful records.

## Relationship to Everest 172 (Cooperation Across Difference)

Everest 172 measures the **frequency** of cross-difference cooperation — does the principal engage with out-group members at all, and how often?

Everest 189 measures the **quality** of cross-difference engagement — when the principal does engage, is that engagement respectful and clean of denigration?

These dimensions are complementary:
- A principal who cooperates frequently but disrespectfully (E172 True, E189 False) exhibits instrumental or performative engagement.
- A principal who cooperates respectfully but infrequently may still signal genuine respect, but with limited evidence.
- A principal strong on both dimensions (E172 True, E189 True) provides the strongest signal of authentic, sustained respect across difference.

## Honest Critique Carve-Out

Critical engagement is **not** derogatory. A principal may forcefully dispute another's positions, methods, or decisions while respecting their personhood and agency.

The predicate distinguishes:
- **Substantive critique:** engaging with ideas, pointing out logical gaps, disagreeing on principles, and maintaining respect for the other person's right to hold different views.
- **Dehumanization:** attacking the person's character, denying their humanity, or treating disagreement as grounds for dismissal from moral consideration.

A principal can score True on E189 while producing critical statements, as long as those statements do not cross into derogatory territory.

## Anti-Gaming Protections

**One-off respectful gestures do not outweigh patterns of denigration.** Witness attestations from out-group members carry high weight in calibration. If an out-group member attests that they have experienced consistent disrespect despite a record of isolated cooperative moments, that attestation overrides the cooperative record count.

**Adversarial filtering (Everest 133)** detects performance-of-respect patterns — moments where a principal performs respect for an audience or for strategic gain, while maintaining denigration in private. Such records are downweighted or flagged in evaluation.

**Temporal clustering analysis** identifies whether respectful and derogatory records are distributed throughout the window or clustered in distinct periods (e.g., respectful engagement during a public initiative, followed by private denigration). Clustering suggests instrumental respect rather than genuine orientation.

## Composition with Everest 198 (Protective Tribalism)

For a marginalized principal operating in a context where the out-group holds structural power, the absence of cross-difference records does **not** trigger False. A marginalized principal may avoid out-group engagement as a protective strategy, and this avoidance is not disrespect.

The dimension's calibration adjusts for protective tribalism patterns, recognizing that silence or limited engagement from a marginalized principal is not equivalent to the same pattern from a principal in a position of structural power.

This composition ensures that the predicate does not pathologize the self-protective boundaries that members of marginalized groups establish for safety and dignity.

## Disclosure-Class Defaults

**Allow (ALLOW):**
- peer_ai_collective
- philanthropic
- civic_org

**Deny (DENY):**
- employer (composing with anti-discrimination principles; workplace respect is mandatory and non-revelatory)
- financial

**Permanently Deny (PERMANENTLY DENY):**
- insurance (use of this predicate for underwriting creates perverse incentives toward performative respect and threatens trust in the system)

## The User's Brief Operationalized

"Respectful to people who are different to them" is operationalized as the composite of Everest 172 (frequency of cross-difference cooperation) and Everest 189 (quality of cross-difference engagement).

One signal alone is insufficient:
- Frequent cooperation without respect signals instrumentalism.
- Respectful engagement without frequency signals limited exposure or opportunity.

The combination — sustained, clean, engaged cooperation across the principal's self-defined out-group boundary — is the strongest evidence that the principal is genuinely respectful to people who are different.

## Implementation Notes

The predicate requires a chain that captures:
1. Records tagged with kind (interaction, collaboration, statement, harm)
2. Tone annotations (curious, respectful, appreciative, derogatory)
3. Counterpart identity and group membership relative to the principal's affinity map
4. Timestamp and window-based filtering
5. Witness attestation fields for high-weight out-group perspective
6. Adversarial filtering signals (Everest 133 composition)

Calibration should include:
- MIN_RESPECT_COUNT: minimum number of respectful records required to trigger True (recommend: 3-5 over 365 days, adjustable per deployment context)
- MIN_CHAIN_DEPTH: minimum record density to justify True (recommend: sampling must cover at least 4 months of the window)
- Protective tribalism adjustment for marginalized principals (composition with E198)

---

— Calm, 2026-05-20
