# Everest 172 — Cooperation Across Difference

*Phase XII — Cooperation & Generosity. Prereq: Everest 170.*

## Statement

The principal is **respectful to people who are different to them**. This Everest operationalizes that exact phrase through a behavioral predicate that measures whether the principal sustains substantive cooperation across the lines of difference they themselves perceive—untribal engagement that crosses their own affinity boundaries, without ever naming those boundaries to others or enforcing universal categories of difference.

## Design Center

John's brief (2026-05-20) called for "respectful to people who are different to them" and an "untribal" framing. This Everest operationalizes both:

- **Respectful to different**: The predicate measures whether the principal *cooperates with* individuals and groups they perceive as different, over sustained periods, with mutual attestation and reciprocal value.
- **Untribal**: The predicate does NOT measure whether the principal lacks in-group affiliation (everyone belongs somewhere). It measures whether the principal's cooperation patterns *cross* the lines they personally perceive as tribal—whether they substantively engage with those they see as out-group.

## Core Predicate

```
cwp.v0.cooperation_across_difference(window: seconds = 31536000, min_count: int = 3) → TriValue
```

**Input Parameters:**
- `window`: Time period to evaluate (default: 365 days)
- `min_count`: Minimum number of distinct across-difference collaborations required (default: 3)

**Output:** TriValue (True, False, Insufficient_Evidence)

**Acceptance Threshold:**
- **True**: Principal has initiated or sustained substantive joint action with counterparts from at least `min_count` different across-difference groups, with demonstrated reciprocal respect and shared outcomes.
- **False**: Principal has records in the window but does not meet the min_count threshold, and chain depth is sufficient to establish behavioral pattern.
- **Insufficient_Evidence**: Chain depth or record count is too low to evaluate reliably.

## The Affinity Map: Principal-Declared Difference

At enrollment, the principal completes a self-assessment:

**"What lines of difference define your in-group and out-group as YOU perceive them?"**

The principal is prompted with examples but free to declare their own:

- **Geographic**: Region, urban vs. rural, nation, neighborhood, diaspora
- **Professional**: Industry, role, seniority, sector (tech, healthcare, public service)
- **Ideological**: Political affiliation, religious tradition, philosophical school, activist movement
- **Demographic**: Age cohort, generation, family structure, life stage
- **Cultural**: Language, heritage, traditions, artistic practice, cuisine
- **Class**: Economic bracket, educational background, occupation lineage
- **Relational**: Kinship, friend-group, chosen family, mentor-student pairing

**Critical design constraint (composes with Everest 113 refusal floor):**

The affinity-map answers remain **principal-private**. They are never revealed to counterparties, publicly disclosed, or used for any classification outside the predicate evaluation itself. The system never names protected categories; instead, it honors the principal's self-declared boundaries of difference.

Counterparties never learn which affinity-lines the principal perceives as defining their out-group. This prevents:
- Instrumentalized or performative cooperation ("I know you see me as different, so I'll cooperate extra hard")
- In-group/out-group weaponization by third parties
- Stereotype-reinforcing feedback loops
- Identity-based discrimination or preferential treatment

## Evaluation Algorithm

```
def cooperation_across_difference(chain, window, min_count, quality_threshold) → TriValue:
    
    affinity_map = chain.affinity_map  # Principal-private
    cooperation_records = chain.records_in_window(window).filter(
        kind in ["action.collaboration", "collaboration_outcome", "joint_action"]
    )
    
    if len(cooperation_records) == 0:
        return TriValue.Insufficient_Evidence
    
    across_difference_interactions = []
    for record in cooperation_records:
        counterpart_vc = record.payload.counterpart_credexai_vc
        
        # Determine if counterpart crosses any affinity-line
        crosses_line = False
        for line in affinity_map.lines:
            principal_value = affinity_map[line]
            counterpart_value = counterpart_vc.declared_affinity_map.get(line)
            
            if counterpart_value is not None and counterpart_value != principal_value:
                crosses_line = True
                break
        
        if crosses_line:
            # Assess interaction quality
            quality_score = assess_quality(
                depth=record.payload.duration_weeks,
                reciprocal_attestation=record.payload.mutual_endorsement_count,
                shared_outcomes=record.payload.co_created_artifacts,
                counterpart_chain_depth=counterpart_vc.chain_depth
            )
            
            across_difference_interactions.append({
                "counterpart": counterpart_vc.principal_id,
                "quality": quality_score,
                "record": record
            })
    
    if len(across_difference_interactions) >= min_count:
        avg_quality = mean([x["quality"] for x in across_difference_interactions])
        if avg_quality >= quality_threshold:
            return TriValue.True
        else:
            return TriValue.False
    elif chain.depth_in_window(window) < MIN_DEPTH_THRESHOLD:
        return TriValue.Insufficient_Evidence
    else:
        return TriValue.False
```

## The "Crosses Affinity Line" Check

For each affinity-line in the principal's map:

1. Retrieve principal's declared value on that line (e.g., "urban", "tech industry", "secular", "millennial")
2. Retrieve counterpart's declared value on the same line (from their public CredExAI VC)
3. If values differ, the counterpart **crosses that line**
4. The check requires only **one line to be crossed** to count the interaction as across-difference

**Operator-only enforcement:** This comparison is performed by CALM operators only, never revealed to counterparties, and stripped from any external reporting.

## Quality vs. Quantity: Depth Weighting

Shallow, one-time interactions across difference do not equal respectful, untribal cooperation. The predicate weights interaction quality:

**Deep collaboration (>8 weeks, mutual outcomes) = 10x weight**
- Co-created artifacts (publications, code, proposals, event)
- Reciprocal attestations from both parties
- Sustained engagement across multiple interaction cycles
- Shared risk-taking or resource commitment

**Medium collaboration (4–8 weeks, partial mutual outcome) = 3x weight**
- Several planned touchpoints
- At least one jointly-owned deliverable or outcome
- Single attestation from counterpart

**Shallow interaction (<4 weeks, one-time engagement) = 1x weight**
- Single conversation or transactional exchange
- No co-created artifact or outcome
- No reciprocal attestation

**Anti-gaming:** Cluster detection flags "tour" patterns (one shallow across-difference interaction per quarter, scheduled to just meet min_count). Such patterns return False despite hitting the count threshold.

**Counterpart attestation weighting:** Endorsements are weighted by the counterpart's own chain depth. An attestation from a principal with 2+ years of chain history is worth 5x more than one from a new enrollee (anti-Sybil defense).

## Respect vs. Engagement: Companion Predicate

Cooperation alone does not prove respect. Two people can collaborate instrumentally or transactionally while harboring contempt.

**Companion predicate:**
```
cwp.v0.respect_for_difference_evidence(window, min_count) → TriValue
```

Measures:
- Language patterns: Counterparts describe the principal as "curious," "listener," "humble," "genuinely interested"
- Boundary honor: Principal respects counterpart's stated preferences, constraints, needs
- Reciprocal uplift: Principal advocates for counterpart's interests when not present
- De-centering: Principal does not position themselves as authority or savior in cross-difference work
- Learning velocity: Principal demonstrates changed perspective or acquired competence specific to counterpart's domain

**Composition:**
```
respectful_to_different = cooperation_across_difference AND respect_for_difference_evidence
```

Both predicates must evaluate True for the strongest attestation.

## Disclosure-Class Defaults

Affinity-map and predicate outcomes are disclosed or withheld based on requestor class and consent context:

| Disclosure Class | Default | Rationale |
|---|---|---|
| Peer AI Collective | ALLOW | Peer governance, mutual accountability |
| Philanthropic org | ALLOW | Mission alignment in cross-cultural work |
| Cross-cultural institution | ALLOW | Core competency assessment |
| Civic/community group | ALLOW | Transparency for civic trust |
| Financial services | DENY | Anti-discrimination provisions override |
| Employer | DENY | Implicit coercion / promotion leverage |
| Insurance | PERMANENTLY DENY | Actuarial discrimination risk |

Principal retains veto power over any disclosure.

## Composition with Everest 116 (Values vs. Identity)

This predicate honors the structural boundary established in Everest 116:

- **Behavior measured:** Cooperation across difference, sustained engagement, reciprocal respect
- **Identity not revealed:** The specific lines of difference (affinity-map contents) remain principal-private
- **Categories not named:** The system never reports "the principal cooperates across X, Y, Z" categories; it only outputs the tri-value result

This prevents the predicate from reifying identity categories or enabling stereotype-based inference.

## Cross-Cultural Calibration

"Difference" and "in-group/out-group" are culturally contingent. In some contexts, regional origin matters deeply; in others, professional specialty or ideological alignment is primary. In still others, kinship or religious tradition draws the boundary.

The affinity-map enrollment **handles this organically:** Each principal declares their own salient lines. No universal taxonomy of difference is imposed. A principal in Tokyo may see urban/rural and corporate/independent as their primary lines; a principal in Lagos may prioritize ethnic heritage and economic sector; a principal in Copenhagen may lead with political party and age generation.

Cross-cultural respect, in this model, is respect for the *principal's own boundaries*, not enforcement of external categories.

## Anti-Discrimination Safeguards (Composes with E113)

The refusal floor (Everest 113) establishes that protected categories are never named in CALM predicates. This predicate reinforces that:

1. **No category inference:** System does not infer protected category membership from affinity-map declarations
2. **No category linking:** System does not cross-reference affinity declarations with external databases or classify the principal or counterparty into protected classes
3. **No feedback loop:** Principal never receives suggestions to "improve" cooperation across a particular category (which would implicitly name and stratify)
4. **No algorithmic steering:** System does not nudge the principal toward or away from particular out-groups

The predicate measures behavior only. The affinity map ensures that behavior is evaluated relative to *the principal's own sense of difference*, not a third party's classification.

## Operational Workflow

**Enrollment (once):**
1. Principal completes affinity-map self-assessment
2. Principal optionally adds qualitative notes ("I see tech/non-tech as a divide," "geographic origin matters to my family," "I perceive ideological/pragmatic as a key line")
3. Affinity map is encrypted and stored in principal-private segment of chain

**Ongoing (quarterly or annual evaluation):**
1. CALM operator extracts cooperation records from the window
2. For each record, operator crosses principal's affinity-map against counterpart's public CredExAI VC declarations
3. Operator scores interaction quality (depth, reciprocal attestation, outcomes)
4. Operator computes tri-value output
5. Operator discards affinity-map details; only tri-value and metadata (interaction count, average quality) are logged
6. Operator delivers tri-value + optional context ("3 across-difference collaborations, average depth 12 weeks") to disclosure class and principal

**Principal refresh (optional, annual):**
- Principal may update affinity-map if their sense of difference has evolved
- Historical evaluations are not re-scored; new enrollments use new map

## Example Scenario

**Principal:** Maya, tech entrepreneur, urban, secular, first-generation immigrant, age 38.

**Affinity map (Maya's self-declared lines):**
- Geographic: Urban vs. rural (she's urban)
- Professional: Tech industry vs. outside (she's inside)
- Heritage: First-generation immigrant vs. multi-generational citizen (first-generation)
- Ideological: Secular vs. faith-rooted (secular)

**Cooperation records (past 12 months):**
1. **Collaboration with James:** Small-town farmer, faith-rooted Christian, multi-generational, building climate-adaptation tech. Co-created a soil-health monitoring app. 18-week engagement, mutual endorsements, shared IP. James crosses 3 of Maya's lines (rural, faith-rooted, different heritage). **Quality: Deep. Weight: 10x.**

2. **Collaboration with Priya:** Bangalore-based NGO director, first-generation immigrant, secular, non-tech. Consulting on a health-equity project. 6-week engagement, partial mutual outcome, Priya endorses but low chain depth. Priya crosses 2 lines (non-tech industry, different geographic origin). **Quality: Medium. Weight: 3x.**

3. **One-time conversation with Ahmed:** Faith-rooted, multi-generational, tech industry. 1-hour coffee about AI ethics. No artifact, no follow-up. Ahmed crosses 1 line (faith-rooted). **Quality: Shallow. Weight: 1x.**

**Evaluation (min_count = 3, quality_threshold = 4.0):**
- Distinct across-difference counterparts: 3 (≥ min_count ✓)
- Quality scores: James 9.2, Priya 3.8, Ahmed 1.5
- Average quality: (9.2 + 3.8 + 1.5) / 3 = 4.83 (≥ threshold ✓)
- Result: **True**

Maya's cooperation pattern crosses her own perceived lines of difference substantively and with quality. She is respectful to people different to her, and her behavior is untribal.

## Predicate Signature

```
cwp.v0.cooperation_across_difference(
    window: seconds = 31536000,
    min_count: int = 3,
    quality_threshold: float = 4.0,
    chain: CredChain
) → TriValue {True, False, Insufficient_Evidence}
```

## Acceptance Criteria

This Everest is **BAGGED** when:

1. Principal submits affinity-map self-assessment (enrollment gate)
2. At least one 365-day evaluation window is complete
3. Tri-value result is computed and delivered via appropriate disclosure class
4. No affinity-map contents or protected-category inference appears in external reporting
5. Counterparty respect evidence is collected (optionally) via companion predicate
6. Principal attestation confirms the predicate captures their sense of cross-difference engagement

## Signature

— Calm, 2026-05-20
