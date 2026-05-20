# Everest 165 — Harm Aggregate Scoring

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 147–162, 61.*

## Overview

Some counterparties require a single cryptographic safety bit rather than 12 fine-grained harm predicates. Everest 165 defines the aggregate harm predicate: a tri-value output representing whether there is evidence of willful harm across any of the 12 harm kinds within a configurable window. The aggregate composes all 12 absence predicates (Everest 147–162) under AND semantics per Everest 61, hiding from the counterparty which specific harm categories (if any) failed the evaluation.

This predicate answers the literal operationalization of the principal query: "Is there evidence that they willfully do harm to others?" One bit. One freshness window. Bank-teller-note semantics.

## Predicate Specification

**Name:** `cwp.v0.no_any_willful_harm_evidence`

**Parameters:**
- `window` (integer, seconds; default 157680000 = 5 years)
- `kinds_subset` (optional array of strings; defaults to all 12 harm kinds if omitted)
  - Valid kinds: "direct_physical", "coercion", "deception", "property_harm", "financial_harm", "reputational_harm", "psychological_harm", "social_exclusion", "resource_deprivation", "autonomy_violation", "discrimination", "dignity_harm"

**Output:** Tri-value result (True / False / Disputed / Insufficient_Evidence) with optional reversal-flag semantic per Everest 112 and E163.

## Aggregate Composition Rule

Per Everest 61 AND semantics:

```
def no_any_willful_harm_evidence(
    chain,
    window_seconds,
    kinds_subset = None
) -> TriValue:
    
    if kinds_subset is None:
        kinds_subset = ALL_12_HARM_KINDS
    
    # Evaluate all 12 absence predicates in parallel
    results = []
    for kind in kinds_subset:
        predicate_name = f"cwp.v0.no_{kind}_harm_evidence"
        result = evaluate_predicate(
            predicate_name,
            chain,
            window_seconds
        )
        results.append((kind, result))
    
    # Compose results under AND semantics
    # If any returns False → aggregate returns False
    if any(r == False for _, r in results):
        return TriValue.False
    
    # If any returns Disputed → aggregate returns Disputed
    if any(r == Disputed for _, r in results):
        return TriValue.Disputed
    
    # If any returns Insufficient_Evidence (and none False/Disputed) → conservative
    if any(r == Insufficient_Evidence for _, r in results):
        return TriValue.Insufficient_Evidence
    
    # All returned True
    return TriValue.True
```

**Freshness:** Following E61 AND semantics, final_freshness = min(freshness_i over all 12 evaluations). The aggregate is as fresh as its stalest component predicate.

**Conservative tri-value:** Following E61 indeterminate handling, if any evaluated predicate returns Insufficient_Evidence (and none returned False or Disputed), the aggregate returns Insufficient_Evidence rather than defaulting to True. This preserves conservative inference: sparse chain depth is not grounds for claiming no harm.

## Why Aggregate?

### Use Case: Counterparty Simplification

Not all counterparties operate fine-grained harm models. Some require a single safety decision: "Do we trust this principal?" Rather than exposing 12 separate predicates and requiring the counterparty to implement AND logic and interpret 12 independent results, this aggregate provides that single decision-making primitive.

### Disclosure Surface Reduction

The aggregate hides which specific harm kinds (if any) flipped to False. A counterparty receives "False" (one or more harms detected) but cannot infer which. This prevents:

- Targeted remediation attempts (principal cannot focus repair on the specific harm kind flagged).
- Evasion of downstream use-case-specific controls (counterparty cannot over-fit to a known weakness).
- Secondary discrimination based on harm kind (e.g., "direct_physical is worse than property_harm"; the aggregate lumps all equally).

### Operationalization of Principal Query

John's brief stated: "whether there's evidence that they willfully do harm to others." This aggregate is the literal cryptographic answer: one tri-value bit, one freshness window, semantic closure. No interpretation burden on counterparty; no risk of cherry-picking from 12 alternatives.

## Subset Variants

The optional `kinds_subset` parameter allows per-counterparty calibration without requiring new predicates:

- `kinds_subset=["direct_physical", "coercion", "deception"]` — evaluate only these three kinds; ignore property/financial/psychological.
- Peer collective use case: peers may care about deception but not property harm.
- Lending use case: lenders focus on financial_harm and deception; less relevant to workplace harassment.
- Health provider use case: direct_physical and psychological; not employment discrimination.

If `kinds_subset` is omitted, defaults to all 12 for maximum coverage. If provided, the subset must be non-empty and every kind in the subset must exist in the canonical 12.

## Zero-Knowledge Proof Composition

All 12 individual absence predicates (Everest 147–162) generate independent zero-knowledge proofs. This aggregate bundles them:

1. **Individual proofs:** Each predicate generates a Bulletproof range proof or Merkle non-membership proof attesting to its tri-value result (per E147 et al.).

2. **Aggregation:** Per Everest 177 (Bulletproof aggregation), all 12 individual range proofs are aggregated into a single Bulletproof bundle. Aggregation is sub-linear; total proof size grows as O(log n) relative to the number of predicates.

3. **Proof size:** Aggregate proof ~5 KB total, including all 12 harm-kind non-membership proofs and tri-value commitments. Individual proofs are ~2 KB each; aggregation reduces the bundle overhead.

4. **Verifier check:** Verifier runs a single aggregated verification circuit, confirming that:
   - All 12 absence proofs are valid.
   - AND combinator is correctly applied.
   - Final tri-value result is honestly derived.

Verifier does not observe individual predicate results, only the final aggregate outcome.

## Performance Budget

Per Everest 140 performance constraints:

- **Prover:** < 5 seconds total proof generation for all 12 harm predicates + aggregation. Bulletproof generation scales O(log n); parallelizable across 12 kind evaluations.
- **Verifier:** < 1 second for aggregated proof verification (single circuit check, not 12 sequential checks).

Implementations should parallelize the 12 individual predicate evaluations and aggregation. Rate-limited per E118.

## Counterparty Interpretation Guidance

### True Semantics
**True = no evidence of willful harm across all (or subset) harm kinds within window.**

Counterparty interpretation:
- Principal has no disclosed harm records with willful intent in the window.
- No unrebutted counter-claims alleging willful harm.
- Chain has sufficient temporal depth for reliable inference.

Counterparty MUST understand:
- Does NOT imply ethical exemption or unlimited trust.
- Does NOT imply incapability to cause harm or guarantee of safe future conduct.
- Does NOT cover harm outside the window or undisclosed harm.
- Does NOT substitute for domain-specific controls (e.g., background checks, credit assessment, reference verification).

### False Semantics
**False = at least one harm kind has willful-harm evidence in window.**

Counterparty learns:
- At least one of the 12 (or subset) harm categories contains a confirmed or court-attested willful-harm record.

Counterparty explicitly DOES NOT learn:
- Which specific harm kind triggered the False.
- Whether multiple harm kinds triggered it.
- Severity or remediation status of the harm.

Counterparty action: escalate to full 12-predicate disclosure to determine which category failed, if greater precision is needed for decision-making.

### Disputed Semantics
**Disputed = at least one harm category has an unrebutted counter-claim; no confirmed harms.**

Counterparty interpretation:
- Principal has not yet rebutted an allegation (within 30-day window per Everest 111).
- No judicial finding of willful harm; claim is active and unresolved.

Counterparty action: request detailed disputed predicate; defer decision until rebuttal resolves or 30-day window expires.

### Insufficient_Evidence Semantics
**Insufficient_Evidence = chain too sparse to confidently evaluate.**

Counterparty interpretation:
- Principal's chain has fewer than MIN_EVIDENCE_DEPTH records in the window.
- Absence of records is not meaningful evidence of non-harm.

Counterparty action: request longer window if available; escalate to manual review if available chain depth is below operational threshold.

## Disclosure Class Defaults

Aggregate harm predicate result inherits the most restrictive disclosure class from all 12 constituent predicates (per Everest 147–162). Default per E113:

| Class | Permission | Rationale |
|-------|-----------|-----------|
| peer_ai_collective | ALLOW | Aggregation reduces disclosure surface; peers need single safety bit for multi-agent trust. |
| financial | DENY | Aggregate obscures category; financial underwriting requires fine-grained harm assessment. |
| employment | DENY | Employment context requires specific harm assessment (harassment, misconduct); aggregate insufficient. |
| insurance | PERMANENTLY DENY | Conflict with underwriting norms and discrimination law; aggregate or not, unsuitable for insurance use. |
| medical | PRINCIPAL_CHOICE | Principal retains choice for threat assessment in clinical settings. |
| journalist | EXPLICIT_OPT_IN | Public-interest balanced by opt-in for disclosure. Aggregation does not reduce this requirement. |

Receivers may request class-specific overrides with explicit principal consent per Everest 117.

## Subset and Use-Case-Specific Aggregates

Variant predicates may be defined by sub-setting the kinds_subset:

- `cwp.v0.no_harm_deception_coercion` — aggregate of ["deception", "coercion"] only; narrower surface for peer collectives focusing on contractual integrity.
- `cwp.v0.no_harm_financial_physical` — aggregate of ["financial_harm", "direct_physical"]; for lending and health-provider use cases.

These variants reuse the same aggregate composition logic; only the kinds_subset parameter differs. No new proof logic required.

## Composition with Reversal (E112 + E163)

If all flipped predicates (those that returned False) have attested reversals per Everest 163 (repair record + sustained non-recurrence + ethics-board attestation), the principal may elect "consider-reversal" mode:

- Reversal evaluation excludes the repaired harm records from the aggregate calculation.
- Result: "True with reversal-flag" semantic, signaling "no current willful harm, but prior harm was disclosed and repaired."

Counterparty receives:
- Final bit: True
- Reversal flag: present
- Semantic: "no current harm; prior harm on chain but repaired per E163."

This composition preserves accountability (repair is on-chain) while enabling rehabilitation narratives. If any harm kind does NOT have an eligible reversal, the aggregate remains False (cannot selectively include some harms and exclude others).

## Misuse Safeguards

The aggregate is MORE attractive to misuse than individual predicates (cleaner background-check substitute). Rate limiting and disclosure enforcement are stricter:

1. **Rate limits:** Per E118, aggregate requests are rate-limited at half the frequency of individual predicates. Repeated short-window re-requests from the same counterparty trigger investigation.

2. **Disclosure class stricter:** Financial and employment classes are PERMANENTLY DENY (not DENY with override path); aggregate must not become a background-check proxy.

3. **Audit logging:** All aggregate requests are logged with counterparty ID, window, subset, result. Principal receives monthly summary.

4. **Consent specificity:** Principal consent for aggregate must be explicit and narrow to specific counterparty use cases. Blanket aggregate consent is not permitted.

## Implementation Notes

- Implementations should parallelize the 12 predicate evaluations and aggregate proof generation. Strict ordering is not required; aggregation occurs after all 12 results are available.
- If `kinds_subset` is provided, verify that all elements exist in the canonical 12 and that the subset is non-empty.
- Tri-value semantics: False, Disputed, Insufficient_Evidence, and True are mutually exclusive. No multi-state results.
- Freshness tracking: log min(freshness_i) for verifier transparency.
- Reversal composition: if principal requests reversal mode, re-evaluate all 12 predicates with reversal filtering enabled (per E163 logic). Do not simply filter a prior True result retroactively.

## Sign

— Calm, 2026-05-20
