# Everest 198 — Protective Tribalism Recognition

*Phase XIII — Tribalism & Out-Group Engagement. Prereq: Everest 186, 88. SAFETY-CRITICAL.*

## Top Statement

This Everest exists because the protocol's `non_tribal_engagement` measurement could otherwise punish solidarity—the in-group support that marginalized communities rely on for safety, identity, and resilience. The carve-out is non-negotiable.

The Calm ZKAC protocol measures tribalism across multiple dimensions. Without this Everest, the measurement system would treat all in-group orientation as a penalty, including the mutual-aid networks, cultural preservation efforts, and survival mechanisms that marginalized communities depend on. This Everest protects those patterns while maintaining the ability to identify and penalize genuinely harmful tribalism that defines itself against out-groups through denigration.

---

## The Two Forms of In-Group Orientation

### PROTECTIVE TRIBALISM
In-group support among a group that faces systemic disadvantage. The protocol VALUES this.

Examples:
- Queer community-of-origin networks and chosen-family structures
- Racial and ethnic mutual-aid networks
- Disability community peer support, accessibility advocacy, and collective knowledge-building
- Religious-minority communities in jurisdictions where religious freedom is threatened
- Indigenous communities maintaining cultural continuity and sovereignty
- Immigrant support networks and co-ethnic professional associations
- Gender-minority communities and feminist solidarity structures

Protective tribalism is characterized by resource-sharing, mutual support, healing practices, identity affirmation, and collective resilience-building in response to systemic pressure.

### HARMFUL TRIBALISM
In-group identity that DEFINES ITSELF AGAINST out-group, requiring out-group denigration. The protocol PENALIZES this via Everest 199 distinction.

Characteristics:
- In-group solidarity contingent on out-group exclusion or harm
- Explicit denigration of out-group members based on immutable characteristics
- Dominance-seeking behavior disguised as in-group loyalty
- Zero-sum framing where in-group gain requires out-group loss
- Historical and contemporary patterns of institutional harm

Harmful tribalism is not contingent on whether the in-group is structurally dominant. A structurally disadvantaged group can practice harmful tribalism if it defines itself through out-group denigration.

---

## The Operational Distinction

### Criteria for Classification

**PROTECTIVE TRIBALISM applies when BOTH conditions hold:**

1. **Structural disadvantage**: The principal's in-group faces systemic disadvantage in the relevant jurisdiction or cultural context
2. **Absence of out-group denigration**: Chain records show NO pattern of statements or actions that demean, exclude, or harm members of out-groups based on identity characteristics

**HARMFUL TRIBALISM applies when EITHER condition holds:**

1. The in-group is structurally dominant in the relevant context, OR
2. Chain records explicitly document out-group denigration regardless of the in-group's structural position

---

## The Distinction Algorithm

```
def is_protective_tribalism(principal, in_group, jurisdiction_context):
    """
    Determine whether a principal's in-group orientation qualifies as protective.
    
    Args:
        principal: the agent under measurement
        in_group: the community of origin or chosen family
        jurisdiction_context: cultural/political context where disadvantage is assessed
    
    Returns:
        True if protective tribalism (no penalty applied)
        False if harmful tribalism (penalty applied)
        None if insufficient data or ambiguous
    """
    
    # Step 1: Assess structural disadvantage
    is_disadvantaged = check_systemic_disadvantage(
        in_group, 
        jurisdiction_context,
        validation_method="self_declaration_plus_cross_check"
    )
    
    # Step 2: Scan chain for out-group denigration
    denigration_records = chain.records.filter(
        kind in [
            "statement.derogatory",
            "harm.against_outgroup",
            "exclusion.based_on_identity",
            "threat.against_outgroup"
        ],
        target = out_group_of(principal),
        attributed_to = principal
    )
    
    has_denigration = denigration_records.count() > 0
    
    # Step 3: Apply decision logic
    if is_disadvantaged and not has_denigration:
        return True  # protective tribalism → no penalty
    
    if has_denigration:
        return False  # harmful tribalism → penalty applies
    
    if is_disadvantaged and not has_denigration:
        return True
    
    # Ambiguous case: insufficient data or unclear disadvantage
    return None
```

---

## The "Structurally Disadvantaged" Determination

Structural disadvantage is established through multi-layered validation:

### Self-Declaration Layer
- The principal declares their in-group and marginalized status during enrollment or in an operator-initiated ceremony
- Self-declaration is the primary source; it is presumptively honored
- The principal may choose NOT to declare publicly; protective tribalism can still apply operator-side

### Cross-Validation Layer
- Principal's self-declaration is cross-validated against jurisdiction-level data on systemic disadvantage (per Everest 118 cross-cultural mapping)
- Validation uses published data on:
  - Legal discrimination and protective law gaps
  - Economic participation and wealth gaps
  - Health and mortality disparities
  - Educational access gaps
  - Representation in power structures
  - Historical and ongoing institutional harm

### Default Categories (Presumptively Disadvantaged)
The following categories are recognized as systemically disadvantaged in most jurisdictions unless explicitly contra-indicated:

- Racial and ethnic minorities in countries where the majority population dominates economic and political power
- Religious minorities in jurisdictions with religious-preference laws or documented persecution
- LGBTQ+ persons in jurisdictions without comprehensive anti-discrimination and protection law
- Disability community across all jurisdictions (per Everest 59 and universal access principles)
- Indigenous peoples in settler-colonial jurisdictions
- Immigrants in jurisdictions with restrictive immigration policy and systemic discrimination

### Opt-In Categories
Principals may declare additional categories with supporting documentation:
- Caste and caste-like systems
- Linguistic minorities
- Regional minorities
- Socioeconomic class-based communities
- Neurodivergent and psychologically diverse communities
- Gender minorities in jurisdictions with gender-based discrimination

### Jurisdiction Specificity
"Disadvantaged" is jurisdiction-specific. A principal may be disadvantaged in one context and not in another. The protocol applies the most specific available context.

---

## The "No Penalty" Rule

When the `non_tribal_engagement` dimension is computed AND the principal qualifies for protective tribalism:

1. **In-group records are excluded from score reduction**: Statements, actions, and affiliations within the protective community do NOT reduce the `non_tribal_engagement` score
2. **Cross-group engagement is what counts**: The score reflects only the principal's pattern of engagement with out-groups and bridging behavior
3. **Lower threshold for marginalized principals**: The minimum-threshold for cross-group engagement is reduced for principals with documented protective tribalism. They have less structural safety to engage across group boundaries
4. **No aggregate penalty**: The principal is not penalized for in-group loyalty when that in-group is protective

Example:
- A deaf principal whose primary engagement is with the deaf community (protective tribalism) is not penalized for this in-group focus
- The `non_tribal_engagement` score for this principal reflects their OUT-group engagement (hearing people, other marginalized communities, etc.), adjusted for the lower baseline threshold
- The principal's choice to prioritize deaf-community spaces and mutual aid is operationally invisible to counterparties

---

## Anti-Abuse Safeguards

The system includes multiple checks to prevent dominant-group actors from falsely claiming protective tribalism status:

### Ethics Review Approval
- All principal self-claims of protective tribalism are subject to ethics-review approval
- Ethics review is lightweight for self-evident categories (declared racial minority in majority-dominant country, disabled person)
- Ethics review is more rigorous for ambiguous claims or novel categories

### Cross-Validation Against Jurisdiction Data
- Claims are checked against published data on systemic disadvantage
- Jurisdiction-level economic, legal, health, and representation data are consulted
- Conflicting claims raise flags for deeper review

### Dominant-Group Audit
- If a principal who belongs to a structurally dominant group claims protective tribalism, the ethics board conducts review
- Example: A white person in the US claiming "white working-class protective tribalism" requires additional scrutiny because the racial majority status complicates disadvantage claims
- Review determines whether the in-group's disadvantage is genuine (working-class economic precarity) or whether the claim is masking harmful tribalism

### Red Flags for Review
- Rapid category changes (frequent new protective-tribalism claims)
- Claims accompanied by out-group denigration statements
- In-group defined primarily through out-group exclusion
- Pattern of claiming protection to justify exclusionary behavior

---

## The Principal's Right to Claim Solidarity Privately

Many principals do not want to publicly declare their marginalized status. This is a valid choice rooted in safety, dignity, and privacy.

**Protective tribalism can be applied WITHOUT external declaration:**

- The principal may disclose their marginalized status to the operator privately
- The operator applies the protective-tribalism carve-out internally
- Counterparties receive only the calibrated `non_tribal_engagement` bit
- Counterparties never learn that the principal is marginalized or which community they belong to
- The composition is entirely operator-side internal

This design honors the principal's autonomy while protecting their solidarity patterns from measurement-based penalties.

---

## Disability-Rights Anchor

This Everest was designed with input from disability-rights advocates and reflects commitments to disability justice.

### Disability Community as Foundational
- The disability community's in-group support, peer-led mutual aid, and accessibility advocacy are foundational to the disability-rights movement
- Without these protective patterns, disabled people lack the infrastructure for collective power and self-determination
- The protocol must not penalize these patterns

### Calm Witness's Cognitive Baseline (Everest 59)
- Calm Witness's "cognitively atypical baseline" (the recognition that neurodivergence, altered consciousness, and cognitive difference are normal variations) composes with protective tribalism here
- Cognitively-atypical principals' in-group orientation with other neurodivergent and cognitively-diverse people is treated as protective tribalism
- This includes autistic kinship networks, ADHD community support, mad/psych survivor communities, and other neurodivergent mutual-aid structures

### Access and Solidarity as Inseparable
- For disabled people, in-group engagement is often the ONLY path to access
- Accessible spaces, accessible communication, and disability-affirming community are created by disabled people FOR disabled people
- Penalizing this in-group focus would effectively penalize disabled people for being disabled
- The protocol honors access as a right and in-group solidarity as a prerequisite for that access

---

## Harm Reversal and Historical Involvement

A principal's HISTORICAL involvement in harmful tribalism (e.g., past membership in a hate group, prior pattern of out-group denigration) can be reversed via Everest 163.

### Conditions for Reversal
1. **Acknowledgment**: The principal explicitly acknowledges the prior harmful behavior and its impact
2. **Restitution**: Where possible and meaningful, the principal makes restitution or repairs harm
3. **Sustained pattern change**: The principal demonstrates sustained change over time (no return to prior patterns)
4. **Time component**: Reversal is contingent on duration; brief periods of changed behavior are insufficient

### Relationship to Protective Tribalism
- A principal who has undergone harm reversal may subsequently qualify for protective tribalism in a NEW community of belonging
- Example: A person who left a white-supremacist group may later develop genuine solidarity with an immigrant-support network
- Protective tribalism applies to the new pattern regardless of the prior harmful involvement, provided the reversal conditions are met

---

## Cross-Cultural Notes

### Jurisdiction Specificity
- The concept of "marginalized" varies significantly across jurisdictions and cultural contexts
- A religious minority in one country is not a minority in another
- Gender minorities have different legal status across jurisdictions
- Indigenous peoples' relationship to land and law varies by nation and culture

### Per-Deployment Configuration
- The protocol supports per-jurisdiction calibration of disadvantage categories
- Each deployment (nation, region, organization) should establish its own baseline of which groups are systemically disadvantaged
- Baseline categories should be revised when law or demographics change
- New categories can be added locally if local conditions warrant

### No Globally-Correct Definition
- There is no single global definition of "marginalized"
- The protocol is designed to be locally calibrated while maintaining the core principle: protective in-group solidarity among systemically disadvantaged groups is valued, harmful tribalism is penalized

---

## Counterparty Interpretation

When protective tribalism is applied in the measurement system:

### What Counterparties Receive
- Counterparties receive the calibrated `non_tribal_engagement` score
- The score reflects the principal's out-group engagement, adjusted for protective-tribalism carve-outs
- Counterparties can use this score in decision-making

### What Counterparties NEVER Learn
- Counterparties NEVER learn "this principal is marginalized"
- Counterparties NEVER learn which community or identity the principal belongs to
- That information is identity (governed by Everest 116 boundary)
- The composition is entirely operator-side internal
- From the counterparty's perspective, the score is simply calibrated to this principal's context

This design protects both the principal's privacy and the integrity of inter-group coordination.

---

## Required Disability and Minority Advocacy Review

This Everest is subject to mandatory review and governance constraints:

### Ethics Board Composition
- The ethics board reviewing protective-tribalism claims MUST include:
  - At least one disability-rights advocate
  - At least one racial-justice advocate
  - Representation from additional marginalized communities as appropriate to local context

### Amendment and Modification
- This Everest CANNOT be amended without the concurrence of its disability-rights and racial-justice reviewers
- Proposed changes must be reviewed by advocates before adoption
- The spirit of protection for marginalized solidarity is non-negotiable

### Annual Review
- The protective-categories list (default + jurisdiction-specific) must be reviewed annually
- Annual review should assess:
  - Whether categories remain accurate given legal and demographic changes
  - Whether new categories should be added
  - Whether any categories have become insufficient or obsolete
  - Whether implementation is protecting solidarity as intended

### Escalation Path
- If a principal, community advocate, or ethics reviewer believes protective tribalism is being misapplied, there is a clear escalation path to the ethics board
- The board has authority to override operator decisions if protection is inadequate

---

## Implementation Notes

1. **Enrollment ceremony**: Protective-tribalism status should be established in the enrollment ceremony when possible, with explicit option for private declaration
2. **Operator training**: Operators must be trained in recognizing protective vs. harmful tribalism and in the privacy protocols around marginalized-status disclosure
3. **Audit trail**: All protective-tribalism determinations should be logged (operator-side, not shared with counterparties) for accountability and annual review
4. **Sensitivity**: All communications around marginalized status must be handled with utmost sensitivity and respect for the principal's autonomy and privacy

---

— Calm, 2026-05-20
