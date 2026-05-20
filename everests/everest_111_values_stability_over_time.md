# Everest 111 — Values Stability over Time

*Phase IX — Values Vocabulary. Prereq: Everest 109.*

## Why Drift Detection Matters

Two opposing tensions define values stability:

1. **Legitimate Evolution.** A 20-year-old's values are not their 40-year-old's. Life experience, hardship, parenthood, and reflection reshape how we prioritize fairness, generosity, and harm-avoidance. The protocol must distinguish between principled growth and stagnation. Values drift is evidence of learning.

2. **Values-Laundering.** An adversary with a reputation for corner-cutting suddenly self-reports alignment with honesty. A cartel operator suddenly claims deep non-harm orientation. Abusers claim repair capacity they have not earned. The protocol must catch these sudden, unexplained shifts—the hallmark of reputation hijacking.

The drift detector resolves this by flagging *speed* rather than direction. Gradual, consistent movement is expected. Sudden reversals without authored explanation are anomalous.

## The Drift Detection Algorithm

For each dimension *d* in the values vocabulary:

1. **Collect inferred scores** across the principal's chain history, indexed by timestamp.

2. **Compute rolling exponential moving average (EMA):**
   - EMA_recent = EMA(scores from 0 to 45 days ago), weight parameter λ = 0.15
   - EMA_older = EMA(scores from 45 to 135 days ago), weight parameter λ = 0.15
   - time_delta = 90 days (the window length)

3. **Calculate drift rate:**
   - drift_rate(d) = |EMA_recent - EMA_older| / time_delta
   - Reported as drift units per year

4. **Compare to threshold:**
   - If drift_rate(d) > threshold_d: flag as "drift_anomaly"
   - If drift_rate(d) ≤ threshold_d: no action

The EMA smooths out single-inference noise while preserving genuine trend signal. A 90-day window balances responsiveness (catching month-long campaigns) with stability (ignoring day-to-day volatility).

## Per-Dimension Drift Thresholds

Default thresholds are calibrated on baseline US/EU longitudinal data. All rates expressed as maximum acceptable drift per year:

| Dimension | Threshold | Rationale |
|-----------|-----------|-----------|
| cooperation | 0.15 / year | Cooperation patterns—reciprocity norms, willingness to coordinate—are foundational and slow to change. Sudden reversals signal either deception or severe trauma. Positive drift acceptable; negative drift is red flag. |
| fairness | 0.10 / year | Among the most stable values. A shift in fairness orientation signals fundamental ideological realignment. Very conservative threshold. |
| honesty | 0.10 / year | Honesty is earned through years of consistent behavior. Sudden claims of honesty improvement warrant skepticism. Negative drift (drift toward deception) is immediately suspicious. |
| non_harm | 0.05 / year | The most conservative threshold. Harm-avoidance is the floor of trustworthiness. Any *positive* drift is welcome and expected; negative drift is immediately flagged at lower thresholds. Asymmetric detection. |
| cross_difference_respect | 0.20 / year | Tolerance and perspective-taking expand with exposure, education, and travel. Legitimate drift is common, especially in younger principals. Growth is default. Negative drift is flagged. |
| generosity | 0.20 / year | Directly tied to income, health, and family circumstances. A principal's capacity to give oscillates with life stage. Threshold reflects this volatility while catching sudden claims of extreme generosity without income shift. |
| non_tribal_engagement | 0.25 / year | Geographic relocation, job changes, and social mobility drive shifts. This is the most volatile dimension. Threshold is permissive; anomalies only flagged at 0.25+/year. |
| repair_after_harm | 0.30 / year | One complete repair cycle can substantially shift this dimension. A principal making amends demonstrates change; threshold reflects earned plasticity. Highest threshold. |
| consistency_under_stress | 0.10 / year | Stress resilience is deep-structure. Sudden claims of newfound calm warrant scrutiny unless authored separately (E112). Conservative threshold. |
| principal_authored_other | 0.20 / year | Principals vary in how openly they construct their own narrative. Shifts in self-authored identity are expected as context changes. Permissive threshold. |

## The "Legitimate Change" Carve-Out: Values Reversal (E112)

If a principal authors a `values_reversal` record (Everest 112), the drift detector enters a **grace period** for affected dimensions:

- The post-reversal window is treated as t=0 for all affected dimensions
- Drift is *expected*, not anomalous, for 180 days post-reversal
- After 180 days, normal thresholds apply to the new baseline
- Multiple reversals on the same dimension within 12 months trigger a "reversal churn" anomaly (separate from drift)

This carve-out prevents false positives when a principal genuinely changes course. However, it requires authored testimony; self-reported inference alone is insufficient.

## The Drift Anomaly Record

When drift_rate(d) > threshold_d, the system appends an immutable `values_drift_anomaly` record:

```
kind: "values_drift_anomaly"
dimension: "honesty"
observed_drift_rate: 0.18 / year
threshold: 0.10 / year
window_used: 90 days
severity: "moderate"  # {low, moderate, high, critical}
inferred_EMA_recent: 0.72
inferred_EMA_older: 0.51
timestamp: [ISO 8601]
principal_visible: true
counterparty_visible: false  # Predicates only
```

The principal can rebut by appending a `values_drift_explanation` record:

```
kind: "values_drift_explanation"
responds_to: [anomaly_record_id]
dimension: "honesty"
explanation: "Career transition into compliance role; formal ethics training completed Feb 2026. Drift expected and healthy."
authored_by: [principal_signature]
timestamp: [ISO 8601]
```

Explanations are logged but do not suppress the anomaly flag. They inform counterparties' interpretation.

## Counterparty-Side Use: The Stability Predicate

Counterparties do not access raw anomaly records. Instead, they query:

```
values_dimension_stable_over_window(
  dimension: "honesty",
  window: 180 days,
  max_drift: 0.08 / year
) → {true, false, insufficient_evidence}
```

Returns:
- **true:** drift < max_drift over the window. No anomalies during the period.
- **false:** drift >= max_drift OR one or more unresolved anomalies.
- **insufficient_evidence:** fewer than 4 inferred data points in the window.

Counterparties can verify "not values-laundering" by querying the predicate. No exposure to anomaly content or explanation records; the counterparty only learns the boolean result.

## Privacy Architecture

- **Drift detection runs on inferred values** (E109), not raw chain content.
- **Anomaly records are principal-visible:** full access to their own flagged drifts and explanations.
- **Counterparties see only the predicate result** (stable/unstable/insufficient), not the underlying data or anomaly content.
- **No third-party auditor access** to drift details without principal consent via explicit grant record.

This preserves principal privacy while enabling counterparties to conduct due diligence.

## Edge Cases and Handling

**Sparse chain (fewer than 4 inference records):**
- Drift detector returns `Insufficient_Evidence`
- Predicates return `insufficient_evidence`
- No anomaly record appended

**Recent reversal (within 180 days):**
- Drift detector uses post-reversal window only
- Pre-reversal data excluded from EMA
- Threshold temporarily elevated to avoid false positives during grace period

**Multi-dimensional drift correlation:**
- If 3+ dimensions show simultaneous drift > threshold, flag as `compound_drift_anomaly`
- Higher severity; indicates possible systematic values shift (e.g., reputation rehab campaign) rather than isolated change
- Reported separately; may trigger human review

**Negative drift on non_harm:**
- Automatically escalated to severity "critical" regardless of magnitude
- Principal notified; counterparty predicate returns `false` immediately

**Reversal churn (3+ reversals on same dimension in 12 months):**
- Flagged as `reversal_churn_anomaly`
- Suggests opportunistic value-shifting; treated as erosion of authored credibility
- Threshold tightened for subsequent intervals

## Composition with Cross-Cultural Mapping (Everest 115)

Default thresholds are calibrated on US/EU baseline data. Principals from other cultural contexts may have legitimate, faster drift patterns:

- Per-principal cultural calibration override: operator specifies `cultural_calibration_factor` ∈ [0.8, 1.5]
- Thresholds scaled by this factor before comparison
- Requires principal-authored `cultural_context` record and optional counterparty consent
- Override does not suppress anomalies; it adjusts severity calculation

Example: A principal from a community with rapid social mobility might have `cultural_calibration_factor=1.3` for generosity and non_tribal_engagement, widening acceptable drift bands.

## Reference Implementation

Core logic: `/Users/johnbradley/AllData/calm_vault_market/values_stability.py`

Public interface:
```python
def compute_drift_rate(dimension: str, chain: List[InferenceRecord], window_days: int = 90) -> float
def check_drift_anomaly(dimension: str, drift_rate: float) -> bool
def values_dimension_stable_over_window(principal_id: str, dimension: str, window_days: int, max_drift: float) -> PredicateResult
def append_drift_anomaly_record(principal_id: str, anomaly: DriftAnomalyRecord) -> None
```

## Summary

Everest 111 operationalizes the tension between legitimate values evolution and values-laundering. The drift detector is neither a moralist (rejecting all change) nor naive (accepting sudden reversals). It flags *speed*—the marker of deception—while permitting gradual, authored growth. Per-dimension thresholds encode the stability properties of each value, calibrated on longitudinal data. Counterparties access only a boolean predicate, preserving principal privacy. The carve-out for authored reversals (E112) ensures the protocol respects agency and growth.

— Calm, 2026-05-20
