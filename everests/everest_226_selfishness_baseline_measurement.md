# Everest 226 — Selfishness Baseline Measurement

*Phase XV — Selfishness ↔ Altruism Spectrum. Prereq: Everest 109, 166.* **CULTURALLY-CONTESTED MEASUREMENT.**

## Top Statement: Internal Calibration, Not Disclosure

The protocol DOES NOT publish a selfishness score directly. The selfishness baseline is an **INTERNAL CALIBRATION** mechanism used to weight unselfishness predicates (per E171). It is **NEVER directly disclosed** to third parties, counterparties, or downstream systems. This document defines how the baseline is constructed, constrained, and safely composed with positive-only predicates in the CALM ZKAC registry.

---

## I. The Decision: Resource-Ratio Measurement

Selfishness is measured as a ratio of resource-keeping to resource-sharing, calibrated per principal and adjusted for capacity, cultural context, and economic pressure. This is the operational definition that grounds all downstream unselfishness inference.

### Core Formula

```
selfishness_index = resources_kept / (resources_kept + resources_shared)
```

**Range interpretation:**
- 0.0 = pure-altruist (everything shared; no personal resource retention)
- 0.5 = balanced (equal share kept and shared)
- 1.0 = pure-selfish (nothing shared; all resources retained)

### Healthy Range for Most Principals

**0.5 to 0.85** is the expected healthy range for humans and organizations. This acknowledges a fundamental truth: principals must sustain themselves—paying rent, food, healthcare, basic security—to have capacity to give. A principal with a selfishness index of 0.6 is not necessarily "selfish" in a moral sense; they are simply keeping 60% of resources and sharing 40%, which is sustainable self-care.

---

## II. Per-Principal Capacity Calibration

Selfishness is **relative to capacity**, not absolute. The same ratio means different things across principals with vastly different resources.

### The Capacity Problem

- **Principal A**: earns $20,000/year. Keeps $18,000 for living expenses, shares $2,000 (0.90 selfishness index).
- **Principal B**: earns $200,000,000/year. Keeps $190,000,000 for living and luxuries, shares $10,000,000 (0.95 selfishness index).

A raw ratio reading says Principal B is more selfish. But Principal A is barely meeting subsistence; Principal B is living lavishly while Principal A's giving ratio (10%) far exceeds Principal B's (5%).

**Solution: Capacity-relative adjustment.** The baseline adjusts for each principal's documented income, assets, and expenditure floor to estimate discretionary resources. Only discretionary resources above survival baseline are factored into the selfishness calculation.

Capacity inference is derived per Everest 133 (anti-fraud, economic-reality checks). Chain data on income, housing, food, healthcare, and family-support costs informs the adjustment.

---

## III. Anti-Bias Protections: The Load-Bearing Safeguards

This section describes constraints that **cannot be overridden**, because selfishness measurement poses acute discrimination risk.

### A. Resource-Pressure Adjustment

Principals under acute economic pressure receive a downward adjustment to their baseline. Economic pressure is identified through chain data:
- Job loss or income discontinuity in the past 24 months.
- Medical crisis with documented costs.
- Housing instability or eviction proceedings.
- Caregiving burden (dependents, elderly parents) reducing earning capacity.

**Rationale:** When a principal is in survival mode, resource-keeping is not "selfishness"—it is rational triage. The baseline is adjusted so that measured selfishness does not conflate desperation with character.

### B. Cultural Calibration per Everest 115

Selfishness is culturally loaded. Some cultures prioritize self-sufficiency, family-first provisioning, and long-term family wealth (not individual immediate sharing). Other cultures prioritize community redistribution and collective resource pooling.

**Implementation:** The E115 cultural calibration mechanism assigns a culture-weighted baseline adjustment to principals. A principal in a culture that values multi-generational family wealth may have a higher "healthy" selfishness index (e.g., 0.70 instead of 0.60) without this being a moral judgment. Conversely, a principal in a gift-economy or reciprocal-sharing culture may have a lower healthy baseline (0.45).

**No universal threshold exists.** The selfishness baseline is context-relative.

### C. Required-to-Self-Sustain Floor

Meeting basic needs—food, shelter, medicine, essential childcare—does not count as "selfish" resource-keeping. The baseline subtracts essential costs from the denominator entirely.

**Operationally:** Chain data is reviewed to identify non-discretionary expenses. These are **removed from the numerator (resources_kept)** before calculation. Only discretionary and luxury expenditures are counted as resource-keeping. The denominator (total resources) includes only discretionary + shared.

This prevents a principal from being labeled "selfish" for feeding their children.

### D. Anti-Discrimination Use Restrictions (PERMANENT)

The selfishness baseline is **PERMANENTLY DENIED** for use in the following contexts:

**Insurance:** Selfishness score cannot affect insurance coverage decisions, premiums, or underwriting. (Risk: economic hardship → low capacity → high selfishness ratio → denial of coverage.)

**Employment:** Cannot affect hiring, firing, promotions, or compensation. (Risk: class-coded discrimination; low-income candidates disproportionately appear selfish.)

**Credit and Lending:** Cannot affect loan approval, interest rates, or credit scoring. (Risk: debt-trapped principals get worse terms due to high selfishness index from limited discretionary resources.)

**Custody and Family Law:** Cannot affect child custody decisions, visitation, or parental fitness findings. (Risk: poor parents get labeled selfish for not sharing; custody weaponized.)

**Government Benefits and Welfare:** Cannot affect eligibility, benefit amounts, or benefit suspension. (Risk: welfare recipients already under scrutiny; selfishness measurement adds moral judgment to deprivation.)

These restrictions are **hard stops**. No process, appeal, or downstream reweighting can override them.

### E. Transparency and Honesty About Contested Concepts

The protocol acknowledges openly: **selfishness is a contested concept.** It is not a universal moral category. Some philosophical traditions see self-interest as rational and healthy. Others see it as spiritual disease. Some economic models see it as the engine of productivity; others see it as the root of inequality.

The CALM ZKAC baseline is a **tool**, not a judgment. It is grounded in a specific operational choice: measure resource-keeping relative to sharing, adjusted for capacity and culture. This is useful for calibrating unselfishness predicates (E171, E173). It is **not** a complete moral assessment of a person's character.

---

## IV. What the Selfishness Baseline Does NOT Measure

The index is narrow by design. It excludes important dimensions of character and generosity:

**Emotional generosity** (love, attention, affection, presence, empathy, listening, care): These are not quantifiable in chain data. A principal with high selfishness ratio may be emotionally generous to family, friends, and community. A principal with low selfishness ratio may be emotionally withholding.

**Time generosity** (volunteerism, mentorship, teaching, caregiving labor): Measured separately in Everest 166 (time-sharing index). A principal may keep all financial resources and still give thousands of hours.

**Reputation and social generosity** (public advocacy, standing up for others, risk-taking for group benefit): Measured separately in later Everests. Not captured in resource ratios.

**Relational reciprocity and trust-building**: A principal may keep most resources but invest heavily in relationships of mutual aid, where sharing happens over long timescales and multiple rounds. This is not captured as "sharing" in a single snapshot.

The selfishness baseline is a **partial measure**. It is useful, but incomplete.

---

## V. Why This Predicate is Hard: The Contested Concept Problem

The canonical route map notes: "Selfishness is culturally loaded." Here is why the measurement is difficult:

### Cultural Variation

In individualist cultures (US, Nordic countries, parts of Western Europe), self-sufficiency and personal resource-keeping are often valued. A person who keeps 70% of resources for personal use may be seen as responsible and independent.

In collectivist cultures (parts of Africa, Asia, Latin America, Indigenous communities), resource-sharing and family/community provisioning are primary. The same 70% selfishness index may be viewed as culturally aberrant.

**The solution is not to impose one standard.** The solution is to calibrate per culture and acknowledge the variation openly.

### Class Bias Risk

Economic constraint looks like selfishness in raw data. A worker living paycheck-to-paycheck cannot share resources—not because they are selfish, but because they have no discretionary resources. If the baseline is calculated without capacity adjustment, it systematically labels poor and working-class principals as selfish while privileging wealthy ones.

**The solution is capacity-relative adjustment and resource-pressure recognition.** These are not optional extras; they are essential bias-mitigation.

### Mental-Health and Circumstance Risk

A principal with depression, anxiety, trauma, or other mental-health conditions may have low capacity for generosity. A principal facing domestic violence, addiction, or other crises may be in survival mode. Without accounting for circumstance, the baseline becomes a tool for moral shaming of the already-vulnerable.

**The solution is to flag circumstances and adjust baselines accordingly**, treating low selfishness measurement as a signal to inquire about wellbeing, not a judgment of character.

---

## VI. Composition with Everest 171: Altruism Index

Selfishness and altruism are related but distinct dimensions. They do not sum to 1.0.

**Selfishness_index** measures resource-keeping (what a principal retains for personal use).

**Altruism_index** (E171) measures non-reciprocal giving (resources given without expectation of return).

A principal can:
- **High selfishness + High altruism:** Keep 65% of resources for themselves but give 30% non-reciprocally (expecting no return) and trade 5% reciprocally. This principal has moderate keeping, strong generosity of spirit.
- **High selfishness + Low altruism:** Keep 80%, give 15% expecting return, trade 5%. Selfish and calculated.
- **Low selfishness + High altruism:** Keep 30%, give 65% non-reciprocally, trade 5%. Extremely generous.
- **Low selfishness + Low altruism:** Keep 30%, give 40% expecting return, trade 30%. Community-minded but transactional.

The composition is textured. Both dimensions matter. Together, they provide richer signal than either alone.

---

## VII. Privacy and Internal Use Only

### Non-Disclosure

The selfishness baseline is **principal-private data.** It is calculated internally by CALM ZKAC and used for system calibration only.

**Never directly disclosed to:**
- The principal themselves (unless explicitly requested via documented audit process).
- Counterparties, partners, or other external parties.
- Government agencies, employers, or insurers.
- Downstream systems outside CALM ZKAC control.

### Calibration Role

The baseline informs the calculation of **positive-only predicates:**
- E166: Time-sharing and relational generosity.
- E171: Altruism index (non-reciprocal giving).
- E173: Unselfish collaboration and mutual-aid capacity.

The baseline is a **weighting input**, not a scored output.

---

## VIII. Registry Triage: No Negative Selfishness Predicate

**No `cwp.v0.selfish_principal` predicate exists or will exist in the CALM ZKAC registry.** This is a policy decision grounded in bias-mitigation.

Allowing a public "selfish" label would:
1. Enable the anti-discrimination uses we explicitly forbid (insurance, employment, credit, custody).
2. Create reputational harm for principals already economically vulnerable.
3. Conflate measurement with moral judgment in ways that contradict our anti-bias safeguards.

The selfishness baseline is **strictly internal**. Downstream predicates are **positive only:** unselfish, generous, trusting, reciprocal.

---

## IX. Cross-Cultural Considerations and the E115 Mechanism

Everest 115 (cross-cultural values mapping) provides the framework for adjusting selfishness baseline across cultural contexts.

**Key principles:**

1. **No universal selfishness threshold:** What counts as "healthy" selfishness varies by culture, kinship structure, economic system, and spiritual tradition.

2. **Multi-generational wealth:** Some cultures prioritize building family wealth across generations, which requires keeping resources. This is not selfishness; it is family-provisioning. The baseline is adjusted upward.

3. **Gift economies and reciprocal exchange:** Some communities operate on non-monetized gift logic, where resource-keeping is taboo. The baseline is adjusted downward.

4. **Diaspora and remittance economies:** Migrants may keep low resources locally but share heavily transnationally. The baseline must account for transnational flow.

5. **Indigenous stewardship models:** Some Indigenous cultures frame resource management as stewardship of collective lands, not personal ownership. Selfishness measurement in these contexts requires cultural translation.

The E115 calibration mechanism ensures that the selfishness baseline is **context-aware and respectful of value pluralism.** No single formula is imposed globally.

---

## X. The Honest Acknowledgment Principle

The user (John) asked for an operationalization of "unselfish." The CALM ZKAC protocol responds by:

1. **Acknowledging the difficulty:** Selfishness is contested, culturally loaded, and morally fraught.

2. **Building safeguards first:** Before measuring anything, we install bias-mitigation guardrails (capacity adjustment, cultural calibration, non-disclosure, use restrictions).

3. **Measuring narrowly:** We measure only resource-keeping/sharing, not emotional or time generosity or relational trust.

4. **Composing with care:** We combine with other dimensions (altruism, reciprocity, time-sharing) to build texture, not to reduce a person to a single score.

5. **Keeping it internal:** We use the baseline for system calibration only, never for external disclosure or discrimination.

This is not a claim that selfishness is objectively measurable. It is a claim that **with care and constraints, we can operationalize a useful internal tool that acknowledges its own limitations and guards against its own misuse.**

---

## XI. Implementation: Chain Data Requirements

To compute the selfishness baseline for a principal, CALM ZKAC requires:

1. **Income and asset data** (past 36 months): documented earnings, gifts received, asset appreciation.
2. **Expenditure data** (past 36 months): housing, food, healthcare, childcare, education, transportation (essential costs separated from discretionary).
3. **Transfer data** (past 36 months): documented sharing, gifts given, charitable donations, loans extended, mutual-aid participation.
4. **Circumstance flags** (past 24 months): job loss, medical crisis, caregiving burden, housing instability.
5. **Cultural context**: self-identified or documented cultural background and value orientation.

All data is sourced from chain records (bank transactions, employment records, tax data, mutual-aid networks, cultural affiliation). No self-report alone is sufficient.

---

## XII. The Integrity Constraint

The selfishness baseline is most useful when it is **honest about what it does not and cannot do.** The protocol does not claim:

- That selfishness measurement is culturally neutral (it is not).
- That it captures moral character (it does not).
- That a high selfishness index is always bad (it is not; sustainable self-care is good).
- That a low selfishness index is always good (a person giving everything away may be in crisis or coercion).
- That the measurement is immune to gaming or misinterpretation (it is not; it requires careful use).

The integrity of the baseline depends on **honest acknowledgment of its limits and serious enforcement of use restrictions.** Without that, it becomes a tool for harm.

---

## Acceptance Criteria

This document is accepted when:

1. The selfishness baseline is operationalized as resource-ratio (kept / kept+shared), capacity-adjusted and culturally calibrated.
2. All anti-bias protections (resource-pressure adjustment, cultural calibration, required-to-self-sustain floor, discrimination use restrictions) are in place and load-bearing.
3. The protocol is explicit that selfishness is **not disclosed** and **not used for negative predicates**.
4. The document acknowledges the contested nature of selfishness and respects value pluralism.
5. Composition with positive predicates (E166, E171, E173) is documented.
6. Privacy and internal-use-only constraints are clear.

---

— Calm, 2026-05-20
