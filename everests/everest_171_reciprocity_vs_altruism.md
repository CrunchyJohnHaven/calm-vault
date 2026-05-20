# Everest 171 — Reciprocity vs Altruism

*Phase XII — Cooperation & Generosity. Prereq: Everest 166.*

## The Core Distinction

The user's brief demands precision on "unselfish." In everyday language, "unselfish" collapses two separate phenomena into one:

1. **Reciprocal helping**: Principal helps in expectation of receiving help back. The giving is transactional. It may be genuinely valuable to both parties, delayed, or asymmetric in form—but it is contingent on anticipated return.

2. **Altruistic helping**: Principal helps with no expectation of return. The giving is independent of anticipated reciprocity. The principal may coincidentally receive help later, but that is not the reason for the original gift.

Both patterns can coexist in the same actor's chain. The question is: what is the ratio?

"Unselfish" operationalizes as **high altruism_index**: the principal's giving is predominantly driven by factors other than reciprocal exchange. This is not a claim that the principal is naive, lacks relationships, or never benefits from others. It is a claim that **the giving is not contingent on receiving**.

## The Altruism Index: Specification

**Predicate name**: `cwp.v0.altruism_index`

**Parameters**:
- `window`: time window in seconds (default: 365 days)

**Output**:
- Scalar value in [0, 1], mapped to tri-value semantics:
  - altruism_index ≥ 0.7 → TriValue.True (predominantly altruistic)
  - altruism_index ≤ 0.3 → TriValue.False (predominantly reciprocal)
  - 0.3 < index < 0.7 → TriValue.Mixed; the actual index value is conveyed as bounded auxiliary data

**Computation**:

```python
def altruism_index(chain, window) -> float:
    """
    Measure the ratio of altruistic to reciprocal giving in a chain over a time window.
    
    Args:
        chain: A principal's transaction/event chain.
        window: Observation window in seconds. Default 365 days.
    
    Returns:
        Float in [0, 1]. None if insufficient evidence (zero giving records).
    
    Semantics:
        altruism_index = altruistic_count / (altruistic_count + reciprocal_count)
    """
    RECIPROCITY_WINDOW = 90 * 86400  # 90 days in seconds; configurable per cultural context
    
    giving_records = chain.records_in_window(window).filter(
        kind in ['transfer', 'gift', 'aid', 'loan', 'time', 'attention', 'advocacy']
    )
    
    altruistic_count = 0
    reciprocal_count = 0
    
    for record in giving_records:
        recipient = record.payload.recipient
        record_ts = record.timestamp
        record_value = record.payload.value  # Normalized to common unit or magnitude class
        
        # Search for return-of-value from recipient to principal
        # within the reciprocity window (default 90 days post-gift)
        return_records = chain.records_from_source_to_principal(
            source=recipient,
            start_ts=record_ts,
            end_ts=record_ts + RECIPROCITY_WINDOW,
            kinds=['transfer', 'gift', 'aid', 'loan', 'time', 'attention', 'advocacy']
        )
        
        if return_records and _value_approximately_matches(return_records, record_value):
            # Recipient gave back comparable value within reciprocity window
            reciprocal_count += 1
        else:
            # No comparable return detected
            altruistic_count += 1
    
    total = altruistic_count + reciprocal_count
    if total == 0:
        return None  # Insufficient evidence
    
    return altruistic_count / float(total)


def _value_approximately_matches(return_records, original_value) -> bool:
    """
    Check if aggregate return value is approximately equal to original giving.
    Magnitude tolerance: 0.8x to 1.2x (configurable).
    """
    return_total = sum(r.payload.value for r in return_records)
    tolerance_min = original_value * 0.8
    tolerance_max = original_value * 1.2
    return tolerance_min <= return_total <= tolerance_max
```

## What "Unselfish" Means in This Framework

The user's "unselfish" is now operationalized. An actor exhibits unselfish behavior when:

1. **The giving is not contingent on receiving**: Observed return-of-value to the principal is absent or delayed well beyond social reciprocity norms (the RECIPROCITY_WINDOW). The principal gave *anyway*.

2. **The ratio tips altruistic**: Over the observation window, the principal's altruistic acts exceed reciprocal ones significantly enough (threshold ≥ 0.7) that we classify the pattern as "predominantly altruistic."

3. **Giving is real and material**: The predicate measures actual transfers, time, advocacy, and attention—not just intentions or statements. A principal who claims altruism but consistently expects equivalent return will register as reciprocal.

4. **The pattern is robust**: The altruism_index is computed over sustained observation (default 365 days). A single act of altruism is not sufficient; the question is whether the pattern persists.

## Adversarial Gaming and Defenses

A bad actor might attempt to artificially inflate their altruism_index:

**Attack 1: One-way recipients**. Engineer the chain to include many gifts to charities, governments, or one-time recipients (who cannot reciprocate). This genuinely lowers the measured reciprocity but inflates altruism artificially.

*Defense*: Capacity normalization (E166) factors in the principal's total wealth and giving capacity. An actor who gives only to entities incapable of reciprocating will show a low generosity_baseline score. Compose altruism_index with generosity_baseline; high altruism paired with low generosity capacity signals possible gaming.

**Attack 2: Hidden reciprocity**. The principal's actual reciprocity happens in private side-channels (verbal promises, off-ledger arrangements, social debt). The chain appears altruistic but conceals true reciprocal intent.

*Defense*: Witness-attested recipients (E115 cross-cultural context) and chain-wide pattern recognition. If the principal's language or behavior with recipients contradicts the measured pattern, the inconsistency surfaces via other predicates (E172 cooperation_across_difference, E173 help_when_costly).

**Attack 3: Temporal manipulation**. The principal deliberately delays reciprocal returns beyond the RECIPROCITY_WINDOW to evade detection.

*Defense*: Extended observation windows and cultural calibration. The RECIPROCITY_WINDOW is not absolute; it is tuned to expected norms in the principal's cultural context (E115). For long-time-horizon cultures, the window extends to 1–2 years. The index still measures the ratio correctly; the calibration simply reflects realistic expectations.

## The Delayed Reciprocity Subtlety

Not all cultures operate on a 90-day reciprocity cycle. Some emphasize long-time-horizon, asymmetric returns:

- In some East Asian and Indigenous gift economies, reciprocal obligation can span years or generations.
- The return may not be identical in form or magnitude; the relationship itself is the currency.
- A principal who gives to a young mentee today, expecting mentorship of their own child in 20 years, is still operating within a reciprocal framework—just a very long-horizon one.

The v0 default RECIPROCITY_WINDOW of 90 days will misclassify delayed-reciprocity giving as altruism in these contexts. The fix is **cross-cultural calibration** (E115):

- Extract the principal's cultural context (via home, language, community ties, witness networks).
- Adjust the RECIPROCITY_WINDOW accordingly: 90 days for rapid-reciprocity cultures, 1–2 years for delayed-reciprocity cultures.
- Recompute the altruism_index with the calibrated window.

The index still measures the ratio correctly; the window parameter is simply context-aware.

## Composition with Related Predicates

Everest 171 does not stand alone. It composes with other cooperation and generosity predicates:

- **E166 (generosity_baseline)**: Does the principal give anything non-reciprocal? altruism_index ≥ 0.5 implies E166 is True.
- **E172 (cooperation_across_difference)**: Does the principal help across tribal lines? Altruism across difference is a stronger signal than altruism within in-group.
- **E173 (help_when_costly)**: Does the principal give at evident personal cost? Altruism + cost = strongest generosity signal.

The composition **altruism_index ≥ 0.7 AND cooperation_across_difference AND help_when_costly** is the Everest's anchor pattern: the principal is unselfish even when it costs them, even to outsiders. This is the "unselfish" the user's brief targets.

## Integration with the Generosity Dimension

The altruism_index feeds into the broader generosity dimension (E107, E109):

- Generosity_dimension = f(generosity_baseline, altruism_index, help_when_costly, cooperation_across_difference, ...)
- High altruism_index contributes strong signal to high generosity_score.
- A principal with high capacity (E166) and high altruism (E171) registers as highly generous in the aggregate dimension.

## Threshold Semantics and Tri-Value Mapping

The altruism_index is a continuous scalar [0, 1], but it maps to a tri-value (True, False, Mixed) for integration into Boolean-centric predicate systems:

- **altruism_index ≥ 0.7**: TriValue.True. Interpret as "predominantly altruistic."
- **altruism_index ≤ 0.3**: TriValue.False. Interpret as "predominantly reciprocal."
- **0.3 < altruism_index < 0.7**: TriValue.Mixed. The actual index value is conveyed as bounded auxiliary. Example: index = 0.55 reads as "mixed, skewing slightly altruistic."

This design preserves the full richness of the continuous measure while supporting discrete reasoning systems.

## Disclosure and Opt-Out

The altruism_index is sensitive data. It infers private intent (whether the principal expects return) from transaction patterns. Disclosure rules apply:

- **Allowed (peer_ai_collective, mentor/mentee, philanthropic)**: The index may be disclosed to collaborators, mentors, or in philanthropic contexts where it directly informs trust or partnership assessment.
- **Denied (financial, employer, insurance)**: The index must not be shared with financial institutions, employers, or insurers, even if the principal consents, because the data is too sensitive to the principal's bargaining position and autonomy.
- **Permanently denied (insurance)**: Insurance contexts are high-stakes adversarial. The altruism_index is permanently withheld regardless of consent.

The principal has the right to opt-out entirely. Some principals reasonably believe reciprocity is the ethical norm and do not wish to be measured against an altruism standard. The predicate is opt-in; the principal must explicitly enable it, and they may disable it at any time without penalty.

## The Principal's Autonomy: Reciprocity Is Not Pathologized

This predicate does not pathologize reciprocity. Reciprocal exchange is a valid and often ethical mode of cooperation. A principal with altruism_index = 0.2 (predominantly reciprocal) is not deficient; they are simply operating in a different cooperation model.

The altruism_index is a **measurement tool**, not a moral judgment. It answers the question: "In this principal's observed behavior, how much of the giving is contingent on anticipated return?" That is a factual question with a factual answer. How the answer is *used* is a separate ethical question, and that question belongs to the principal and their community, not to this predicate.

## Specification Closure

The altruism_index is specified, testable, and composable. It operationalizes "unselfish" as high-ratio altruistic-over-reciprocal giving, calibrated to cultural context, robust to adversarial gaming, and integrated into the generosity dimension. The predicate respects the principal's autonomy to opt-out and does not pathologize reciprocal exchange.

The user's "unselfish" is now a measurable, actionable property of a principal's chain.

---

*Everest 171 — Reciprocity vs Altruism. Phase XII — Cooperation & Generosity.*

*— Calm, 2026-05-20*
