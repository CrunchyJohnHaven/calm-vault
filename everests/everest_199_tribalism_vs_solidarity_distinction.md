# Everest 199 — Tribalism vs Solidarity Distinction

*Phase XIII — Tribalism & Out-Group Engagement. Prereq: Everest 198, 197.*

## The Core Distinction

Both solidarity and harmful tribalism are rooted in in-group support. They are not opposites. The critical distinguishing feature is whether in-group orientation requires out-group denigration to sustain itself.

**SOLIDARITY**: In-group support that does NOT require out-group denigration. The principal supports, amplifies, or cares for their community without defining that community against, beneath, or in opposition to others. The in-group affirmation stands on its own terms.

Examples:
- Mutual-aid networks organized by neighborhood residents to share food and resources
- Identity-affirming communities (queer book clubs, ethnic heritage organizations, professional guilds) that celebrate shared culture, history, or craft without targeting outsiders
- Professional collaboration within a team or discipline
- Marginalized groups organizing for their own protection and advancement

**HARMFUL TRIBALISM** (in the sense that triggers adversarial response): In-group support that defines itself BY out-group denigration. The in-group identity is constructed through the active subordination, derogation, or exclusion of an out-group. The in-group exists relationally—negatively—against the out-group.

Examples:
- Hate groups whose ideology centers on the inferiority or malevolence of target groups
- In-group-defining-against-outgroup ideologies (e.g., white supremacy, caste systems)
- Loyalty tests that require in-group members to denigrate, mock, or betray outsiders
- Doctrines of in-group purity enforced through active hostility toward out-groups

## The Diagnostic: What Makes Them Different

Both solidarity and harmful tribalism display in-group orientation in the principal's chain records. Both generate mutual-aid signals, community resilience actions, and in-group support records.

The distinguishing factor is **the presence or absence of out-group denigration in the principal's substantive chain**.

A principal may be deeply embedded in their in-group, affirm their identity repeatedly, and collaborate intensely with their community. This is solidarity unless the chain also contains active denigration of others.

A principal may occasionally critique external policies or groups. This is not yet tribalism unless the critique crosses into denigration—the characterization of an out-group as inferior, contemptible, or threatening simply because they are out-group.

## Chain-Record Signals

### Solidarity Signals

In-group support records without out-group denigration:
- `kind: "mutual_aid"` — resource sharing, collective care, organized assistance
- `kind: "in_group_support_record"` — affirming language, celebration of shared identity, mentorship
- `kind: "community_resilience_action"` — organizing, bridge-building, public advocacy for the in-group's interests
- `kind: "cross_group_record"` — engagement with out-group members as peers, collaborators, or allies
- Absence of `kind: "statement.derogatory"` targeting any out-group

### Harmful Tribalism Signals

- `kind: "statement.derogatory"` explicitly targeting an out-group, with language that suggests the out-group is inferior, dangerous, or contemptible
- `kind: "exclusion_of_outgroup"` — active barriers to out-group participation, coupled with in-group purity language
- `kind: "in_group_purity_test"` — requiring in-group members to prove loyalty by denigrating, mocking, or betraying out-group members
- `kind: "out_group_threat_amplification"` — characterizations of out-groups as existential threats without substantiation in the principal's own experience
- Pattern: denigration appears in contexts where it is _not_ a defensive response to an immediate threat, but rather a _constitutive_ element of in-group identity

## The Predicate Specification

**Name**: `cwp.v0.solidarity_not_tribalism`

**Parameters**:
- `chain`: Principal's record chain (required)
- `window`: Lookback period (default: 365 days)
- `marginalized_status`: Classification of principal's group(s) (optional; affects calibration)

**Output**: TriValue (True | False | Insufficient_Evidence)

## Evaluation Algorithm

```
def solidarity_not_tribalism(chain, window, marginalized_status=None) -> TriValue:
    
    # Collect records in window
    records_in_window = chain.records_in_window(window)
    
    # Identify tribalism signals (the "flip" signals)
    denigration_records = records_in_window.filter(
        kind in {
            "statement.derogatory" targeting out-group,
            "exclusion_of_outgroup",
            "in_group_purity_test",
            "out_group_threat_amplification"
        }
    )
    
    # Identify solidarity signals (affirmative signals)
    solidarity_records = records_in_window.filter(
        kind in {
            "mutual_aid",
            "in_group_support_record",
            "community_resilience_action"
        }
    )
    
    # Identify cross-group engagement
    cross_group_records = records_in_window.filter(
        kind == "cross_group_record" 
        AND signal_valence >= neutral
    )
    
    # PRIMARY LOGIC: Any active denigration flips to False
    if denigration_records.count() > 0:
        return TriValue.False
    
    # SECONDARY LOGIC: Sufficient solidarity evidence + cross-group engagement
    if (solidarity_records.count() >= 2 
        AND cross_group_records.count() >= 1):
        return TriValue.True
    
    # TERTIARY LOGIC: Insufficient data
    if records_in_window.count() < MIN_THRESHOLD:
        return TriValue.Insufficient_Evidence
    
    # DEFAULT: Presumption of solidarity
    # (Does not apply if denigration present; caught above)
    return TriValue.True
```

## Key Design Choice: Presumption of Solidarity

The predicate defaults to **True** (solidarity) unless contradicted by denigration signals. This is intentional.

**Rationale**: It is more defensible to incorrectly presume solidarity in a borderline case than to incorrectly accuse a principal of tribalism, especially if that principal is from a marginalized group.

The cost of a false positive on tribalism is high: it can trigger exclusion, loss of reputation, or being targeted as a threat. The cost of a false positive on solidarity is lower: it grants presumptive good faith in ambiguous cases.

**How the presumption is overridden**: Denigration signals must be **active and substantiated**. A principal must have made statements or taken actions that actually characterize an out-group negatively, not merely failed to praise them. Criticism of policies, institutions, or ideologies does not count unless coupled with characterizations of the out-group *people* as inferior or contemptible.

**Who benefits**: Marginalized principals benefit most from this presumption. It protects them from bad-faith accusations of tribalism when they are organizing for their own survival and dignity. A marginalized principal should not be penalized for in-group orientation if they are not actively denigrating others.

## The In-Group Purity Test Detection

A specific anti-pattern warrants particular attention: **the in-group purity test**—a requirement that in-group members prove loyalty by denigrating, mocking, or betraying out-group members.

This is not detected at predicate-evaluation time (the denigration signal already handles it). Instead, it is flagged at **audit time** through clustering analysis on the chain:

- Cluster 1: In-group member affirms identity, participates in solidarity actions.
- Cluster 2: In-group member makes a denigrating statement about an out-group.
- Cluster 3: Community response to Cluster 2 is celebratory or approving.
- Pattern: Denigration co-occurs with increased in-group status, affirmation, or advancement.

When this pattern emerges, it is logged as `kind: "in_group_purity_test"` and flagged at audit time. The cost of false positives here is high (falsely accusing a community of enforcing loyalty through hatred), so detection is conservative and documented separately from the predicate itself.

## Composition with Everest 198: Protective Tribalism

Everest 198 identifies protective tribalism as a response by marginalized groups to existential threats. It is not itself a pathology; it is a survival mechanism.

**Composition rule**: For a marginalized principal, protective tribalism (E198) + solidarity (E199 = True) = positive signal. The principal is protecting their group AND not defining themselves against other marginalized groups.

**Asymmetry**: A dominant-group principal cannot claim "protective tribalism" as a defense. For them, in-group orientation is suspect unless accompanied by cross-group engagement and an absence of denigration.

## The Complexity: Marginalized Principal, Denigrating Another Marginalized Group

A principal may be from a marginalized group (and thus earn protective tribalism recognition) AND simultaneously denigrate another marginalized group.

Example: A Black principal denigrates immigrants. A woman denigrates transgender people. A disabled person mocks homeless people.

**How the predicate handles this**:
- The denigration signals flip this predicate to False.
- Simultaneously, Everest 198 still recognizes the principal's protective tribalism toward their own group.
- The records are not contradictory; they are compounded. The principal is both protective of their in-group AND engaged in harmful tribalism against another group.
- This is a signal for closer examination: Has the principal been influenced by dominant-group narratives that pit marginalized groups against one another? Is the denigration being used to gain status within the broader society?

The predicate does not resolve this complexity away. It simply flags it: True and False simultaneously in different dimensions.

## Composition with Everest 107 & 109: Non-Tribal Engagement Dimension

Everest 107 defines the "non_tribal_engagement" dimension of trustworthiness. Everest 109 infers this dimension from available signals.

**Important**: A principal with `solidarity_not_tribalism = True` does NOT automatically score high on the non_tribal_engagement dimension.

Solidarity (pure in-group support without denigration) is distinct from non-tribal engagement (cross-group connection and willingness to prioritize shared norms over group loyalty).

**Inference rule (E109)**: Exclude pure-solidarity-without-denigration from the "tribal" measure. A principal who exhibits solidarity but no cross-group engagement receives:
- `solidarity_not_tribalism = True`
- `non_tribal_engagement = Unknown` or `Needs_Clarification`

If the principal also exhibits cross-group records, then:
- `solidarity_not_tribalism = True`
- `non_tribal_engagement = higher_confidence`

## Adversarial Scenario: Hidden Denigration

A dominant-group principal hides denigration in encrypted channels, private groups, or coded language.

**Defense mechanisms**:
1. **Counter-claimants (E111)**: Out-group members can file `kind: "harm_alleged.hate_speech"` records with attestations about private statements.
2. **Witness records**: In-group members who have heard denigration can file `kind: "witness_statement"` records.
3. **Pattern clustering**: If a principal's public in-group support is consistently followed by rumors of private denigration, the pattern may be flagged at audit time.
4. **Escalation**: If a principal is accused of hidden denigration via counter-claims, the predicate is re-evaluated with those records included.

This is not foolproof, but it acknowledges that the predicate is vulnerable to malicious actors and builds in remedial pathways.

## Asymmetric Calibration: The Protective Principle

The predicate is asymmetrically calibrated to protect marginalized principals.

**Calibration rule**: 
- **Marginalized principal**: Presumption of solidarity unless denigration signals are clear and substantiated. The default is True.
- **Dominant-group principal**: Higher evidentiary standard. In-group orientation alone does not earn a True rating. Cross-group engagement and active evidence of non-denigration are required.

**Justification**: Marginalized groups have asymmetric power relationships with dominant groups. A marginalized principal organizing with their community is exercising hard-won agency. To penalize that with accusations of tribalism unless they also prove cross-group cooperation is to impose a burden that dominant groups do not face.

Conversely, a dominant-group principal claiming in-group solidarity should demonstrate that this solidarity does not come at the expense of others. Their higher standard is a structural safeguard, not a punishment.

## Disclosure-Class Defaults

Different contexts warrant different disclosure rules:

- **peer_ai_collective**: ALLOW. Disclosure of `solidarity_not_tribalism` evaluations to peer collectives is permitted. These are contexts where collective learning and shared governance benefit from transparency.
- **philanthropic**: ALLOW. Foundations and philanthropic organizations focused on community resilience may access these evaluations.
- **civic_org**: ALLOW. Civic organizations, neighborhood councils, and mutual-aid groups may access evaluations.
- **employer**: DENY. An employer should not have access to an employee's `solidarity_not_tribalism` evaluation. This risks discrimination based on in-group affiliation or community membership.
- **financial**: DENY. Banks, lending institutions, and financial services should not use this predicate. It poses risk of discrimination in lending or services.
- **insurance**: PERMANENTLY DENY. Insurance companies must not access this data. The incentives are misaligned; they would use tribalism signals as a proxy for risk, deepening discrimination against marginalized communities.

## Worked Example

**Principal: Alex**, a member of a Black mutual-aid network in a majority-white city.

Chain records (12-month window):
- `kind: "mutual_aid"`: Alex organizes food distribution to neighbors facing food insecurity.
- `kind: "in_group_support_record"`: Alex mentors younger members of the network, affirms their identity and cultural heritage.
- `kind: "community_resilience_action"`: Alex testifies at a city council meeting about the network's impact.
- `kind: "cross_group_record"`: Alex collaborates with a white-led environmental group on a community garden project.
- No denigration records.

**Evaluation**:
- Denigration signals: 0
- Solidarity signals: 3 (mutual_aid, in_group_support, community_resilience)
- Cross-group records: 1
- Marginalized status: Yes (applies asymmetric protection)

**Result**: `solidarity_not_tribalism = True`

**Interpretation**: Alex is demonstrating solidarity—strong in-group support coupled with cross-group engagement and an absence of denigration. The presumption of solidarity is confirmed.

---

**Principal: Blake**, a member of a majority-group hobby club.

Chain records (12-month window):
- `kind: "in_group_support_record"`: Blake organizes club events, celebrates the club's history and identity.
- `kind: "statement.derogatory"`: Blake makes a public comment that members of a different hobby club are "pretentious snobs."
- No cross-group engagement records.

**Evaluation**:
- Denigration signals: 1
- Solidarity signals: 1
- Cross-group records: 0

**Result**: `solidarity_not_tribalism = False`

**Interpretation**: The denigration signal flips the predicate to False. Blake's in-group support is entangled with out-group denigration. This is tribalism in the harmful sense.

---

## Summary

The `cwp.v0.solidarity_not_tribalism` predicate operationalizes a crucial distinction: solidarity and harmful tribalism are not defined by in-group orientation, but by whether that orientation requires out-group denigration.

The predicate defaults to solidarity (True) unless denigration signals are present. It asymmetrically protects marginalized principals, recognizing that in-group organization is a survival mechanism and a form of power-building, not a pathology.

It composes with protective tribalism (E198), non-tribal engagement (E107/E109), and counter-claims (E111) to create a nuanced picture of how a principal relates to their own group and to others.

Most importantly: it does not require marginalized principals to prove cross-group loyalty to earn the presumption that their in-group support is benign. It asks them only to refrain from denigrating others. This is the asymmetry that protects.

— Calm, 2026-05-20