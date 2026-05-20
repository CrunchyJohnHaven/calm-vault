# Everest 170 — Sustained Cooperation Predicate

*Phase XII — Cooperation & Generosity. Prereq: Everest 167.*

## Predicate Specification

**Name:** `cwp.v0.sustained_cooperation`

**Purpose:** Measure whether a principal maintains cooperation across multiple relationships over substantial durations, distinguishing genuine long-term partnership commitment from transactional one-off collaboration.

**Parameters:**
- `window` (default: 730 days / 2 years) — lookback period for evaluation
- `min_relationships` (default: 5) — minimum count of sustained relationships required
- `min_duration_per_relationship` (default: 180 days) — minimum span for a relationship to count as "sustained"

**Output:** TriValue (True / False / Insufficient_Evidence)

## Core Concept

Sustained cooperation differs fundamentally from generosity (Everest 166) and single acts of collaboration. Where generosity measures the outbound impulse to give or assist, sustained cooperation measures the willingness to maintain reciprocal engagement over time. A single generous act can occur in isolation. Sustained cooperation requires repeated investment, trust-building across multiple cycles, and demonstrated commitment to continuity despite friction points or changing incentives.

The "sustained" filter is the operative distinction. A principal may perform generous acts in bursts — responding to crisis, supporting a friend's startup for three months, then disengaging. This is generous but not sustained. Sustained cooperation shows up as:

- Multiple collaboration sessions with the same counterpart separated by intervals
- Continuation through difficulty or changing circumstances
- Evidence of relationship maintenance, not just task completion
- Pattern across several independent relationships simultaneously

This pattern indicates structural orientation toward long-term partnership rather than episodic altruism.

## Evaluation Logic

```
def sustained_cooperation(chain, window, min_relationships, min_duration_per_relationship) -> TriValue:
    # Extract cooperation records from designated window
    cooperation_records = chain.records_in_window(window).filter(
        kind in ["action.collaboration", "collaboration_outcome"]
    )
    
    # Handle insufficient data
    if not cooperation_records:
        return TriValue.Insufficient_Evidence
    
    # Group records by counterpart identity
    by_counterpart = group_by_counterpart(cooperation_records)
    
    # Filter to relationships meeting minimum duration threshold
    sustained = [
        (counterpart, records) 
        for counterpart, records in by_counterpart.items()
        if (records.last_timestamp - records.first_timestamp) >= min_duration_per_relationship
    ]
    
    # Apply threshold
    if len(sustained) >= min_relationships:
        return TriValue.True
    elif chain.depth_in_window(window) < MIN_DEPTH_THRESHOLD:
        return TriValue.Insufficient_Evidence
    else:
        return TriValue.False
```

**Key Steps:**

1. **Record collection:** Identify action.collaboration and collaboration_outcome records within the window. These may include signed testimony from counterparts, transaction logs of collaborative projects, ongoing mentorship records, or structured peer-review partnerships.

2. **Counterpart grouping:** Organize by distinct counterpart. A counterpart is a unique principal with whom sustained cooperation is claimed. Transitive collaborations (working through intermediaries) do not count unless there is direct sustained relationship evidence.

3. **Duration filtering:** For each counterpart, calculate span = (final interaction timestamp - first interaction timestamp). Include only relationships where span >= min_duration_per_relationship. Isolated events do not qualify.

4. **Threshold evaluation:** Count relationships meeting the duration criterion. If count >= min_relationships, return True. If the chain lacks sufficient depth to evaluate (e.g., new principal with limited collaboration history), return Insufficient_Evidence.

## Why Sustained Cooperation Matters

**Signal of commitment depth:** Maintaining collaboration across multiple relationships over 6+ months each signals genuine investment in partnership, not opportunistic alliance-building. One-off collaborations can indicate a transactional approach: work together, extract value, move on.

**Trust and reciprocity foundation:** Relationships that persist over time typically involve reciprocal learning, dispute resolution, and adaptation. A principal who sustains cooperation has demonstrated ability to weather disagreement, adjust expectations, and remain engaged through asymmetry.

**Distinction from generosity:** A principal may be generous (Everest 166) and create value for others without sustaining relationships. Conversely, a principal may have shallow transactional relationships with many counterparts and fail the sustained cooperation test. Both dimensions matter independently.

**Structural stability:** Sustained cooperation creates network resilience. Communities where principals maintain multiple long-term collaborations show lower churn and higher capacity to coordinate across change.

## Anti-Gaming Defenses

**Witness attestation:** Counterparts' chains must include signed records acknowledging the collaboration. Self-reported cooperation without corroboration from counterpart does not satisfy the predicate. This prevents sock-puppet relationships and inflated claims.

**Counterpart chain depth:** Verify that claimed counterparts have non-trivial chain depth within the same window. A principal cannot claim sustained cooperation with a one-time NPC or a counterpart with no independent evidence of participation in the ecosystem.

**Recency and monotonicity:** Cooperation records should show evidence of bidirectional engagement. One-directional support (e.g., principal A consistently mentors principal B, but B never reciprocates or acknowledges the relationship) may count toward generosity but not sustained cooperation.

**Project-level validation:** For collaboration_outcome records, verify that the outcome was meaningfully contested or required mutual commitment. Rubber-stamp co-authorship or hollow committee membership do not qualify.

## Composition: Sustained Cooperation Under Stress

When a principal's chain contains hard-time markers (documented stressors, setbacks, or periods of reduced capacity) within the cooperation window, and cooperation records continue across those markers, the evaluation composes with Everest 107 (consistency_under_stress). A principal sustaining cooperation despite stress demonstrates stronger commitment than cooperation in favorable conditions.

```
sustained_and_consistent = sustained_cooperation(chain, window, min_relationships, min_duration_per_relationship) 
                          AND consistency_under_stress(chain, stressor_types)
```

This composite signal indicates both breadth (multiple relationships) and robustness (maintained commitment despite difficulty).

## Composition: Sustained AND Across Difference

When combined with Everest 172 (cooperation_across_difference), sustained cooperation takes on additional weight. A principal who sustains cooperation with counterparts of differing backgrounds, expertise, or worldviews demonstrates not just relationship commitment but adaptability and genuine partnership (not ideological alignment).

```
sustained_and_diverse = sustained_cooperation(...) AND cooperation_across_difference(...)
```

This is one of the strongest cooperation signals available, indicating principal is neither tribal nor opportunistic, but genuinely collaborative across boundaries.

## Cultural Calibration

The default 180-day min_duration_per_relationship parameter is calibrated to Western professional norms emphasizing formal project cycles and documented outcomes. Cultures prioritizing intensive short-term collaboration (research sprints, hackathons, crisis response) or those with different relationship formalization timelines may require parameter adjustment per Everest 115 (cultural_calibration).

A cross-cultural evaluation framework should:
- Allow min_duration_per_relationship adjustment by declared cultural context
- Recognize informal collaboration records and oral testimony in addition to formal documents
- Weight intensity and depth of engagement in short duration alongside continuation in longer duration
- Adjust min_relationships count for cultures with smaller trust circles

## Disclosure-Class Defaults

Sustained cooperation may be evaluated and disclosed depending on counterpart class and consent context:

- **peer_ai_collective:** ALLOW — evaluation and disclosure permitted; serves coordination signal
- **foundation_grantmaker:** ALLOW — relevant to stewardship and long-term funding relationships
- **mentor:** ALLOW — mentorship relationships are typically explicitly acknowledged
- **employer:** DENY — employment relationships involve power asymmetry; sustained "cooperation" may be confused with loyalty under obligation
- **financial:** DENY — sustained financial partnerships involve confidentiality concerns
- **insurance/legal:** PERMANENTLY DENY — fiduciary relationships require strict privacy boundaries

When counterpart class is ambiguous, default to DENY unless explicit consent is documented.

## Zero-Knowledge Proof Construction

Sustained cooperation predicates compose with Everest 45 (Bulletproof range proofs) for ZK attestation:

1. **Range proof on relationship count:** Prove count(sustained_relationships) >= min_relationships without revealing identities or specifics of counterparts

2. **Per-relationship duration proof:** For each sustained relationship, prove (last_ts - first_ts) >= min_duration_per_relationship using timestamp commitments

3. **Non-fraud commitment:** Include Merkle tree proof that records are authentic (signed by principal and counterparts) without revealing record content

4. **Composition proof:** When sustained_cooperation composes with consistency_under_stress or cooperation_across_difference, include ZK proof of composition without revealing stress markers or diversity dimensions

This construction allows disclosure of the predicate result (True/False/Insufficient) to authorized parties without exposing relationship details to general audiences.

## Implementation Notes

**Record types:** action.collaboration records should include timestamps (first engagement, last engagement), counterpart identifier, project/context description, and cryptographic commitment to both parties' attestation. collaboration_outcome records should include measurable output, witness signatures, and duration metadata.

**Grouping heuristic:** Two records belong to the same relationship if they reference the same counterpart identifier and occur within reasonable interval (e.g., < 2 years apart). If a counterpart re-engages after 3+ years silence, treat as separate relationship instance.

**MIN_DEPTH_THRESHOLD:** Set to minimum record count indicating principal has sufficient history to evaluate. Typically 10-20 records in window; may be culture-specific.

**Temporal bucketing:** For performance, may bucket records into 90-day periods and count unique counterparts per bucket to identify sustained relationships more efficiently than iterating all pairs.

## References

- **Everest 107:** consistency_under_stress — robustness of cooperation under adversity
- **Everest 115:** cultural_calibration — adaptation of predicate parameters to cultural context
- **Everest 166:** generosity_predicate — outbound value creation, distinct from relationship sustainability
- **Everest 167:** coalition_formation_predicate — prerequisite; measures ability to initiate cooperation
- **Everest 172:** cooperation_across_difference — breadth of collaboration across diverse counterparts
- **Everest 45:** Bulletproof_range_proofs — ZK proof framework for predicate composition

---

— Calm, 2026-05-20