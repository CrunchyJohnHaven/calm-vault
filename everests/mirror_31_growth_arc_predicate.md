# Mirror Everest 31 — `growth_arc_evidence` Predicate

*Phase XI — Value-Measurement Predicates. Prereq: Mirror Everest 17, 22, 26.*

---

## Canonical Specification

**Name:** `growth_arc_evidence`  
**Version:** `1.0.0`  
**Created:** 2026-05-20T16:30:00Z  
**Stability:** Bound to Everest 34 composition mandate (mandatory co-disclosure with `non_harm_evidence=false`).

### Purpose

Returns a tri-valued result (true / false / unknown) answering: *Does the chain show evidence of acknowledged past failure followed by sustained corrective pattern change?* This predicate operationalizes the grace primitive — that past behavior does not lock the principal in. It is the protocol's mercy mechanism. Without it, the values-attestation system becomes a permanent blacklist.

### Philosophy

The growth-bit answers a specific trajectory question, not a redemption claim. The predicate does not judge whether the principal "deserves forgiveness" or "is redeemed" — those are moral judgments outside the protocol's scope. Instead, it measures three observable facts: (1) the principal admitted a past failure, (2) took demonstrable corrective actions, (3) sustained absence of that failure pattern for a meaningful window. This composition honors principal-protective default 2: *past behavior does not lock the principal in*.

---

## Description

The predicate measures a trajectory over three sequential phases:

1. **Acknowledgment Phase:** The principal authored a `kind: counter_evidence.v0` record admitting a past harm or mistake (Mirror Everest 17).
2. **Corrective-Action Phase:** After acknowledgment, the chain contains `kind: corrective_action.v0` records documenting steps taken to address the admitted pattern.
3. **Sustained-Change Phase:** A time-windowed absence of recurrence — no new counter-evidence in the named category for ≥18 months.

The predicate returns:
- **`true`:** All three phases present, with sustained absence threshold met, and corrective actions demonstrably address the named pattern (verified by witness or third-party record).
- **`false`:** Acknowledgment present but corrective-action phase absent or thin, OR recurrence detected (new counter-evidence in the same category within the 18-month window).
- **`unknown`:** Acknowledgment present but insufficient time elapsed (< 18 months since corrective action), OR corrective actions not credibly documented, OR acknowledgment too recent (< 30 days old, too early to assess intent).

---

## Input Domain

- **Kind:** `kind: counter_evidence.v0` (Mirror Everest 17), `kind: corrective_action.v0` (newly defined), `kind: counter_evidence.v0` (recurrence check).
- **Temporal Binding:** Corrective actions must fall in the window [acknowledgment_ts, acknowledgment_ts + 365 days]. Sustained-change window: [last_corrective_action_ts, now] for ≥18 months.
- **Evidence Diversity:** Corrective actions must include witness corroboration (Mirror Everest 13) OR third-party record (Mirror Everest 14) — self-reported corrective action alone does not qualify.

---

## Three Sub-Metrics (Composite)

### Sub-Metric 1: Acknowledgment Evidence

**Definition:** A `kind: counter_evidence.v0` record where the principal admits a past harm or mistake, naming the pattern and (ideally) the affected party.

**Computation:**

```
acknowledgment_present = ∃ record ∈ chain_records :
    record.kind == "counter_evidence.v0" AND
    record.author_id == principal_id AND
    record.payload.category in [
        "extractive_behavior",
        "dismissal_of_others",
        "harm_through_action",
        "harm_through_omission",
        "deception",
        "betrayal_of_trust",
        "abuse_of_power"
    ] AND
    record.payload.description is_detailed AND
    record.ts >= (now - max_lookback_window)
```

Where:
- **Description Requirement:** The counter-evidence must articulate the specific failure (not generic "I made mistakes"). Examples: "I excluded a team member from key decisions" (specific), vs. "I was not a good leader" (generic). Generic admissions return `unknown`.
- **Category Lock:** The principal names the failure category (e.g., "extractive_behavior"). This category is then used to detect recurrence in Sub-Metric 3.
- **Timestamp:** The acknowledgment date anchors the corrective-action window.

**Threshold Parameter τ_ack:** No threshold; binary. Acknowledgment either exists or does not.

### Sub-Metric 2: Corrective-Action Evidence

**Definition:** After acknowledgment, the principal took measurable steps to address the named pattern. Actions must be witnessed or third-party-verified (not self-reported).

**Computation:**

```
corrective_action_present = ∃ records ∈ chain_records :
    records.kind == "corrective_action.v0" AND
    records.subject_id == principal_id AND
    records.payload.addresses_counter_evidence_id == acknowledgment_record_id AND
    records.ts >= acknowledgment_ts AND
    records.ts <= acknowledgment_ts + 365 days AND
    (records.payload.witness_signature OR records.payload.third_party_evidence) AND
    records.payload.description_of_action is_concrete
```

A corrective-action record qualifies if:

1. **Links to Acknowledgment:** Explicitly references the counter-evidence record ID it addresses.
2. **Temporal Proximity:** Initiated within 365 days of acknowledgment (otherwise the lag suggests non-serious intent).
3. **Witness or Third-Party Corroboration:** Either a Calm-credentialed witness co-signs the action record, OR a third-party document (e.g., completion certificate, attendance log) is hash-committed.
4. **Concreteness:** The action description specifies what was done, not vague commitments. Examples: "Attended 8 sessions of leadership coaching with Coach X" (concrete), vs. "Committed to self-improvement" (vague). Vague actions return `unknown`.

**Witness Signature Semantics:** A witness attests that they observed the action taken or received the corrective outcome. Examples: "I witnessed the principal facilitate a mediation session with the harmed party"; "I received the written apology and the principal's proposal for future collaboration."

**Third-Party Evidence:** Receipts, certificates, registrations, policy change records, etc., hash-committed to the chain.

**Threshold Parameter τ_corrective_count:** Per-principal, calibrated at acknowledgment. Typical: ≥1 witnessed corrective action (at least one substantial step). More serious harms warrant higher counts (τ ≥ 3).

### Sub-Metric 3: Sustained-Change Evidence

**Definition:** Absence of recurrence — no new counter-evidence in the same category for ≥18 months after the last corrective action.

**Computation:**

```
sustained_change_present = NOT ∃ record ∈ chain_records :
    record.kind == "counter_evidence.v0" AND
    record.author_id == principal_id AND
    record.payload.category == acknowledgment_record.payload.category AND
    record.ts > last_corrective_action_ts AND
    record.ts >= (now - 548 days)  // 18 months in days
```

Where:
- **Recurrence Definition:** A new counter-evidence record in the same category indicates the failure pattern resurfaced. This breaks the growth-arc.
- **Time Window:** 18 months (548 days) is the minimum threshold. This balances (a) enough time to demonstrate sustained change without locking growth behind decades of perfect behavior, and (b) sufficient weight to show the change is not performative. Configurable per deployment.
- **Category Specificity:** Only recurrence in the *same* category breaks the arc. If the principal admits extractive_behavior, later counter-evidence of deception does not block growth-arc (though it may trigger separate predicates).

**Threshold Parameter τ_sustained_days:** Default 548 days (18 months). Non-negotiable minimum per principal-protective default 2.

---

## Threshold Parameters

**Per-Principal Baseline τ (Composite Threshold):**

At the time of acknowledgment (or upon disclosure request), the principal and counterparty calibrate:

```json
{
  "principal_id": "john_bradley",
  "predicate_id": "growth_arc_evidence",
  "version": "1.0.0",
  "acknowledgment_category": "extractive_behavior",
  "acknowledgment_record_id": "ce_001",
  "acknowledgment_ts": "2024-06-15T10:00:00Z",
  "thresholds": {
    "tau_corrective_count": 2,
    "tau_sustained_days": 548,
    "tau_description_concreteness": "high"
  },
  "calibration_ts": "2026-05-20T00:00:00Z",
  "calibration_basis": "acknowledgment_content + counterparty_negotiation"
}
```

**Corrective-Count Floor:** Serious harms (e.g., betrayal of trust, abuse of power) warrant τ ≥ 3 corrective actions; minor failures (dismissal in one instance) may warrant τ = 1. Calibration is counterparty-negotiable at disclosure time.

**Sustained-Days Floor:** 18 months (548 days) is non-negotiable. Principal-protective default 2 forbids indefinite lockout; 18 months provides meaningful weight without becoming permanent.

---

## Reference Truth-Table Evaluator (Pseudocode)

```python
def growth_arc_evidence(
    chain_records: List[Record],
    principal_id: str,
    counter_evidence_id: str,  # ID of the acknowledgment to evaluate
    now_iso: str  # ISO 8601 UTC timestamp
) -> Tuple[Bit, Optional[str], Optional[Dict]]:
    """
    Evaluate growth_arc_evidence predicate.
    
    Args:
        chain_records: Behavior-evidence chain.
        principal_id: The principal being evaluated.
        counter_evidence_id: ID of the counter_evidence.v0 record to assess growth around.
        now_iso: Evaluation time (UTC).
    
    Returns:
        (Bit, optional_reason, optional_metadata)
        Bit in {True, False, Unknown}
    """
    
    now = datetime.fromisoformat(now_iso)
    
    # 1. Fetch acknowledgment record
    ack_record = None
    for r in chain_records:
        if r.kind == "counter_evidence.v0" and r.id == counter_evidence_id:
            ack_record = r
            break
    
    if ack_record is None:
        return (Bit.Unknown, "acknowledgment_record_not_found", None)
    
    if ack_record.author_id != principal_id:
        return (Bit.Unknown, "acknowledgment_not_authored_by_principal", None)
    
    # 2. Check acknowledgment recency (too early to assess growth)
    days_since_ack = (now - ack_record.ts).total_seconds() / 86400.0
    if days_since_ack < 30:
        return (Bit.Unknown, "acknowledgment_too_recent", {
            "days_since": days_since_ack,
            "minimum_days": 30
        })
    
    # 3. Sub-Metric 1: Acknowledgment Evidence
    ack_category = ack_record.payload.category
    ack_description = ack_record.payload.description
    
    if not is_detailed_description(ack_description):
        return (Bit.Unknown, "acknowledgment_too_vague", {
            "description": ack_description[:100]
        })
    
    metric_1_pass = True  # Acknowledgment exists and is detailed
    
    # 4. Sub-Metric 2: Corrective-Action Evidence
    corrective_records = [
        r for r in chain_records
        if r.kind == "corrective_action.v0" and
           r.subject_id == principal_id and
           r.payload.addresses_counter_evidence_id == counter_evidence_id and
           ack_record.ts <= r.ts <= ack_record.ts + timedelta(days=365) and
           (r.payload.witness_signature or r.payload.third_party_evidence)
    ]
    
    # Filter for concrete actions only
    concrete_corrective = []
    for r in corrective_records:
        if is_concrete_action_description(r.payload.description_of_action):
            concrete_corrective.append(r)
    
    if not concrete_corrective:
        return (Bit.False, "no_credible_corrective_actions", {
            "found_records": len(corrective_records),
            "concrete_records": len(concrete_corrective)
        })
    
    # Assume τ_corrective_count = 1 (minimum threshold)
    metric_2_pass = len(concrete_corrective) >= 1
    last_corrective_ts = max(r.ts for r in concrete_corrective)
    
    # 5. Sub-Metric 3: Sustained-Change Evidence
    sustained_window_start = last_corrective_ts
    sustained_window_end = now
    sustained_days_elapsed = (sustained_window_end - sustained_window_start).total_seconds() / 86400.0
    
    recurrence_records = [
        r for r in chain_records
        if r.kind == "counter_evidence.v0" and
           r.author_id == principal_id and
           r.payload.category == ack_category and
           r.ts > last_corrective_ts
    ]
    
    if recurrence_records:
        # Recurrence detected
        return (Bit.False, "pattern_recurrence_detected", {
            "recurrence_count": len(recurrence_records),
            "first_recurrence_ts": min(r.ts for r in recurrence_records).isoformat()
        })
    
    # Check if sufficient time has elapsed
    if sustained_days_elapsed < 548:  # 18 months
        return (Bit.Unknown, "insufficient_sustained_change_window", {
            "days_elapsed": sustained_days_elapsed,
            "minimum_days": 548,
            "days_remaining": 548 - sustained_days_elapsed
        })
    
    metric_3_pass = sustained_days_elapsed >= 548
    
    # 6. Tri-state result
    if metric_1_pass and metric_2_pass and metric_3_pass:
        return (Bit.True, None, {
            "acknowledgment_ts": ack_record.ts.isoformat(),
            "acknowledgment_category": ack_category,
            "corrective_action_count": len(concrete_corrective),
            "sustained_days": sustained_days_elapsed,
            "last_corrective_ts": last_corrective_ts.isoformat()
        })
    
    return (Bit.False, "one_or_more_metrics_failed", {
        "metric_1_acknowledgment": metric_1_pass,
        "metric_2_corrective": metric_2_pass,
        "metric_3_sustained": metric_3_pass
    })
```

**Semantics:**

- **Bit = True:** Acknowledgment detailed; ≥1 witnessed/third-party corrective action taken within 365 days; no recurrence for ≥18 months.
- **Bit = False:** Acknowledgment present but corrective actions absent/thin/unwitnessed, OR recurrence detected in the same category.
- **Bit = Unknown:** Acknowledgment too recent (< 30 days), or acknowledgment too vague, or corrective actions present but insufficient time elapsed (< 18 months), or actions present but unwitnessed.

---

## Tri-State Semantics and Counterparty Interpretation

**Unknown is Not "Still Growing":**

Returning Unknown signals "the evaluation period is incomplete," not "the principal is still in transition." A principal waiting out the 18-month window returns Unknown until the threshold is crossed, at which point a new evaluation may return True.

**False is Not "Unforgivable":**

Returning False means "the arc is broken or incomplete," not "this principal is unredeemable." A counterparty who uses a False growth-arc result to justify permanent exclusion has violated the protocol's spirit. Growth is iterative; a principal can acknowledge a new failure, take new corrective actions, and establish a new arc.

**Policy Guidance for Consuming Systems:**

- **Conservative:** Treat Unknown as "predicate not satisfied; require longer evidence window."
- **Integrative:** For low-risk counterparties, Unknown can be treated as "growth pending; ask the principal for timeline."
- **Mandatory on Harm:** If `non_harm_evidence = false`, disclosure MUST include growth-arc regardless of result (Mirror Everest 34).

---

## Adversarial Considerations

### Anti-Performative-Apology (Mirror Everest 38)

A principal might author a counter-evidence admission and a handful of corrective actions immediately before requesting disclosure to a counterparty. The protocol flags this via:

1. **Timing Proximity Check:** If acknowledgment and corrective actions all cluster within 7 days, they are flagged as `antifraud_signal: true`.
2. **Witness Independence:** Corrective-action witnesses must not all be recent or novice (low-VC tenure). A principal suddenly gathering witnesses may be gaming.
3. **Time-Decay (Mirror Everest 22):** Corrective actions closer to acknowledgment weigh more; corrective actions clustered toward the 365-day boundary weigh less (suggesting delay).

Gaming-detection does not automatically fail the predicate, but flags the evaluation record as requiring counterparty scrutiny.

### Anti-Resurfacing-Old-Counter-Evidence-as-Fake-Growth

A principal might claim growth around an old counter-evidence record (from years ago) and assert they've been sustaining absence ever since. To prevent this:

1. **Corrective-Action Temporal Anchor:** Corrective actions must fall within [acknowledgment_ts, acknowledgment_ts + 365 days]. Corrective actions claimed to have occurred before the acknowledgment are invalid.
2. **Recent Recurrence Inspection:** The predicate checks the entire history back from acknowledgment, not just the 18-month window. If a new counter-evidence in the same category appeared 10 months after acknowledgment (then silence for 8 months), the arc is broken.

---

## Cross-Cultural Notes

### v0 Encodes Transparency-Centric Assumptions

The v0 predicate assumes:

- Public acknowledgment of failure is valuable and trustworthy (Western therapy-influenced model). Shame-avoidant cultures may favor private correction or family-internal resolution.
- Witness corroboration is the gold standard. Collectivist cultures may prefer authority-figure validation or family consensus over third-party witnesses.
- 18 months is a meaningful window for sustained change. In cultures with different temporal rhythms (cyclical vs. linear), this threshold may feel arbitrary.

### Evolution via Mirror Everest 71–72

Cross-cultural taxonomy (Everest 71) and cultural overlays (Everest 72) document alternative acknowledgment and correction modalities. A principal may declare `growth_arc_evidence@confucian_v1`, where the corrective-action threshold is family-mediated reconciliation rather than third-party witnesses.

---

## Predicate ID Stability Rule

The predicate ID is content-addressed: `growth_arc_evidence:sha256(specification_hash):version`.

Per-principal, per-acknowledgment-category calibrations do not change the predicate ID. Only changes to the specification itself (sub-metrics, sustained-days window, witness requirements) trigger a new ID.

---

## Acceptance Tests

### T-M31.1: Determinism

**Given:** Two evaluators running `growth_arc_evidence` on the same chain, acknowledgment_id, and now-timestamp.

**Expected:** Identical results (Bit, Reason, Metadata).

**Rationale:** Reproducibility and audit-trail correctness.

### T-M31.2: Tri-State Correctness

**Given:** Golden-path test corpus (9 hand-crafted scenarios below).

**Expected:** Each scenario returns the correct (Bit, Reason) pair as documented.

**Rationale:** Sub-metrics, time windows, recurrence detection, and anti-gaming logic must work.

### T-M31.3: Composition with non_harm_evidence

**Given:** A principal with `non_harm_evidence = false` and a valid growth_arc acknowledgment + corrective actions + sustained absence.

**Expected:** Any disclosure including `non_harm_evidence = false` MUST also include `growth_arc_evidence = true` in the same response, without requiring a separate query.

**Rationale:** Principal-protective default 2 enforced at the protocol level.

### T-M31.4: Anti-Performative-Apology Detection

**Given:** An acknowledgment and 5 corrective actions all timestamped within 7 days, then a disclosure request.

**Expected:** The evaluation record includes `antifraud_signal: true` and reason includes "evidence_temporal_clustering". The predicate may still return True (if 18-month window is met), but the flag alerts the counterparty.

**Rationale:** Gaming is flagged, not prevented.

---

## Golden Test Corpus

### Test M31.1: Clear Positive Growth Arc

**Chain:**

- Counter-evidence: "2024-06-15 — I extracted value unfairly from team X; prioritized my metrics over their wellbeing." (acknowledgment_id = ce_001)
- Corrective-action: "2024-07-20 — Completed 3-day team dynamics workshop, witnessed by Dr. Smith (Calm VC holder). Implemented new collaborative metric system with team consensus." (addresses ce_001, witness signature present)
- No recurrence counter-evidence in "extractive_behavior" category since 2024-07-20.
- Now: 2026-05-20 (≈688 days since corrective action)

**Evaluation:** (Bit.True, None) — acknowledgment detailed, corrective action witnessed and concrete, sustained absence (688 > 548 days).

### Test M31.2: No Corrective Actions

**Chain:**

- Counter-evidence: "2024-06-15 — I was dismissive of others' ideas in team meetings." (acknowledgment_id = ce_002)
- No corrective-action records found.

**Evaluation:** (Bit.False, "no_credible_corrective_actions")

### Test M31.3: Corrective Actions Too Late

**Chain:**

- Counter-evidence: "2023-06-15 — I betrayed a colleague's trust." (acknowledgment_id = ce_003)
- Corrective-action: "2024-08-01 — Apologized and met with colleague for reconciliation, witnessed." (420+ days after acknowledgment, exceeds 365-day window)

**Evaluation:** (Bit.False, "corrective_actions_outside_temporal_window") OR (Bit.Unknown, "insufficient_actions_within_window")

### Test M31.4: Corrective Actions Unwitnessed

**Chain:**

- Counter-evidence: "2024-06-15 — Extractive behavior." (acknowledgment_id = ce_004)
- Corrective-action: "2024-08-01 — Self-reported apology and personal reflection." (no witness signature, no third-party evidence)

**Evaluation:** (Bit.Unknown, "corrective_action_unwitnessed")

### Test M31.5: Recurrence Detected

**Chain:**

- Counter-evidence (ack): "2024-06-15 — Extractive behavior." (acknowledgment_id = ce_005)
- Corrective-action: "2024-08-01 — 3 team coaching sessions, witnessed." (concrete, witnessed)
- Counter-evidence (recurrence): "2025-02-10 — Again prioritized my bonus over team outcomes." (same category: extractive_behavior, 160 days after corrective action)

**Evaluation:** (Bit.False, "pattern_recurrence_detected")

### Test M31.6: Insufficient Time Elapsed

**Chain:**

- Counter-evidence: "2026-02-15 — Deception in communications." (acknowledgment_id = ce_006)
- Corrective-action: "2026-03-20 — Completed ethics training, witnessed." (concrete, witnessed)
- Now: 2026-05-20 (61 days since corrective action; < 548 days)

**Evaluation:** (Bit.Unknown, "insufficient_sustained_change_window")

### Test M31.7: Acknowledgment Too Vague

**Chain:**

- Counter-evidence: "I was not a good person." (acknowledgment_id = ce_007, generic, not detailed)
- Corrective-action: "2024-08-01 — Self-improvement efforts, witnessed." (concrete)

**Evaluation:** (Bit.Unknown, "acknowledgment_too_vague")

### Test M31.8: Acknowledgment Too Recent

**Chain:**

- Counter-evidence: "2026-05-10 — Harm caused." (acknowledgment_id = ce_008, 10 days ago)
- Corrective-action: "2026-05-15 — Apology and action plan, witnessed." (5 days later)
- Now: 2026-05-20

**Evaluation:** (Bit.Unknown, "acknowledgment_too_recent")

### Test M31.9: Multiple Corrective Actions, Sustained Absence

**Chain:**

- Counter-evidence: "2023-06-15 — Abuse of power." (acknowledgment_id = ce_009)
- Corrective-action 1: "2023-08-01 — Executive coaching, witnessed." (concrete)
- Corrective-action 2: "2023-10-15 — Mentorship from external advisor, witnessed." (concrete)
- Corrective-action 3: "2024-02-20 — Policy change co-authored with team, third-party evidence (policy registry)." (concrete)
- No recurrence in "abuse_of_power" category since 2024-02-20.
- Now: 2026-05-20 (≈813 days since last corrective action)

**Evaluation:** (Bit.True, None) — detailed acknowledgment, 3 witnessed/third-party actions within 365 days, sustained absence (813 > 548 days).

---

## Composition with Other Mirror Everests

### Non-Harm Evidence (Mirror Everest 30) + Growth-Bit Composition (Everest 34)

**Mandatory Rule:** Any disclosure including `non_harm_evidence = false` MUST co-disclose `growth_arc_evidence` if a valid acknowledgment + growth arc exists. The two bits are presented together:

```
non_harm_evidence: false
  ├─ Harm Record 1: [details]
  ├─ Harm Record 2: [details]
  └─ Right-of-Reply: [principal's response, if any]

growth_arc_evidence: [true|false|unknown]
  ├─ Acknowledgment Record: [details]
  ├─ Corrective Actions: [list]
  └─ Sustained Absence: [analysis]
```

This composition prevents blackballing (principal-protective default 2).

### Counter-Evidence Intake (Mirror Everest 17)

Growth-arc predicates evaluate specific counter-evidence records. Without Everest 17's intake mechanism, there is no acknowledgment to build a growth arc around.

### Time-Weighting (Mirror Everest 22)

Corrective actions closer to the acknowledgment weigh more; actions near the 365-day boundary weigh less. The predicate does not fail on temporal distribution, but metadata flags uneven timing for counterparty review.

### Evidence-Diversity (Mirror Everest 23)

Corrective actions require ≥2 evidence-kinds: (a) at least one witnessed action AND (b) either another witnessed action OR a third-party record. Single-source actions return unknown.

### Anti-Gaming (Mirror Everest 38)

Temporal clustering of acknowledgment + corrective actions + disclosure request within days triggers `antifraud_signal: true`.

### Consistency-Over-Time (Mirror Everest 35)

Acknowledgments and corrective actions clustered shortly before disclosure request are flagged as potentially performative.

### Predicate Composition (Mirror Everest 26, 40)

Growth-arc is expressed in the Calm Witness predicate DSL extended for behavior-evidence. Per-acknowledgment calibration is stored in the chain.

---

## Open Questions for v1

1. **Multiple Simultaneous Arcs:** Can a principal have growth arcs for multiple distinct failures (extractive_behavior and deception both acknowledged and corrected)? v1.0.0 evaluates per acknowledgment; a comprehensive "overall growth" score may require aggregation logic.

2. **Partial Recurrence:** If a principal admitted "I excluded out-group members" and later (post-corrective-action) shows some exclusion but much reduced frequency, does this count as recurrence? v1.0.0 uses binary presence/absence; v1 may allow scaled recurrence detection.

3. **Third-Party Evidence Standards:** What constitutes credible third-party evidence for corrective action? A certificate from a self-selected coach differs from a court-ordered program completion. v1 may calibrate evidence-types by reliability.

4. **Witness Leverage:** If most witnesses are employed by the principal (power-imbalance), should their co-signatures degrade? v1 may require witness independence checks (Everest 16 VC tenure, absence of financial relationship).

5. **Cultural Acknowledgment Modalities:** If a principal resolves harm through family mediation (not public counter-evidence), does this count as acknowledgment under a cultural overlay? Mirror Everest 72 governs this.

---

## Cross-References

- **E1:** Six principal-protective defaults (default 2: growth is first-class).
- **E17:** Counter-evidence intake (acknowledgment channel).
- **E22:** Time-weighting of evidence (temporal decay functions).
- **E26:** Predicate language v0 (DSL for evaluation).
- **E30:** Non-harm evidence (composed with growth-arc via E34).
- **E34:** Growth-bit composition rule (mandatory co-disclosure).
- **E35:** Consistency-over-time predicate (detects performative arcs).
- **E38:** Adversarial-test-resistance flag (anti-gaming).
- **E71:** Cross-cultural value taxonomy (alternative acknowledgment modalities).
- **E72:** Religious/philosophical overlays (culturally-mapped arcs).
- **E80:** Right of reply (complements growth narratives).

---

## Sign-Off

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.  
**Status:** Mirror Everest 31/100 — Phase XI, bagged.  
**Timestamp:** 2026-05-20T16:45:00Z

This predicate is the protocol's mercy primitive. It honors principal-protective default 2 and prevents the values-attestation system from becoming a blacklist. Growth is not redemption; it is trajectory. The predicate measures the trajectory, not the soul.

— Calm, 2026-05-20
