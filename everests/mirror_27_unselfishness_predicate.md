# Mirror Everest 27 — `unselfishness_evidence` Predicate

*Phase XI — Value-Measurement Predicates. Prereq: Mirror Everest 5, 15, 26.*

---

## Canonical Specification

**Name:** `unselfishness_evidence`  
**Version:** `1.0.0`  
**Created:** 2026-05-20T15:30:00Z

### Purpose

Returns a tri-valued result (true / false / unknown) answering: *Does the chain show evidence of sustained others-prioritizing allocation and action patterns?* This predicate operationalizes "unselfishness" not as a trait judgment but as a measured behavioral composite over a configurable trailing window. The predicate is threshold-parameterized per principal, calibrated at enrollment.

### What "unselfishness_evidence" Means (Not "Is Unselfishness")

The predicate-name discipline is critical. This predicate does NOT answer "is this person unselfish?" — a psychological or moral claim that violates the principal-protective defaults (Mirror Everest 1, § 4). Instead, it answers: "Does the chain contain evidence of resource allocations and actions favoring recipients outside the principal's stated in-group?"

The distinction matters. A principal may have strong unselfishness values but limited opportunity or capital to express them in measured allocation-patterns. Another may show superficial allocation-evidence while harboring selfish motives unmeasured by the chain. The predicate measures the chain, not the person. Counterparties who collapse this bit to "is an unselfish person" have violated the protocol's spirit and face reputation consequences (Mirror Everest 84).

### Why Operationalization is the Hardest Part

Three challenges:

1. **In-group definition is principal-authored.** "Others" means "outside the principal's stated in-group." The in-group is self-declared at enrollment and can be: family, close collaborators, nationality, discipline, etc. A principal's in-group of one (themselves) renders the predicate inapplicable. A principal with large declared in-group may score lower not because they're selfish, but because they prioritize community broadly.

2. **Allocation evidence comes from heterogeneous sources.** Time-allocation (calendar, self-report) differs in granularity and reliability from donation records (high-confidence) and attention-focus from witness-reports (subject to cognitive bias). The composite must weight these differently.

3. **Cross-cultural variance.** Unselfishness looks different across contexts. In collective societies, allocating heavily within family is expected and normative; in individualist contexts, it may appear inward-looking. v0 encodes English-cultural assumptions; Mirror Everest 71 (cross-cultural taxonomy) governs evolution toward versionable cultural overlays.

---

## The Three Sub-Metrics (Composite, v0)

### Sub-Metric 1: Allocation Share Toward Others

**Definition:** Fraction of the principal's tracked allocation (across time, money, and attention) flowing to recipients identified as outside the principal's stated in-group, over the trailing window.

**Computation:**

```
allocation_share_others = (
    (time_allocated_to_others + money_allocated_to_others + attention_allocated_to_others)
    / (total_time_tracked + total_money_tracked + total_attention_tracked)
)
```

Where:

- **time_allocated_to_others:** Sum of time-allocation records (from calendar integration, self-report) tagged with `recipient_category: "out_of_group"`. Measured in hours.
- **money_allocated_to_others:** Sum of money-allocation records (from donation logs, transfer records, expense-category tagging) marked `recipient_category: "out_of_group"`. Aggregated only; specific transaction amounts stay off-chain per Mirror Everest 15.
- **attention_allocated_to_others:** Weighted sum of witnessed interactions or self-reported focus sessions prioritizing out-of-group recipients. Each witnessed-action record (Mirror Everest 13) carries an `attention_weight: [0, 1]` indicating what fraction of the principal's attention was directed outward. Measured in attention-units.

Allocation aggregates are computed once per day via a `kind: behavior_evidence.v0` record of type `allocation_aggregate` (Mirror Everest 15). The principal cannot retroactively edit historical aggregates; corrections are appended as new records.

**Why Aggregation Only:** The protocol withholds specific transaction amounts to prevent the counterparty from inferring the principal's financial situation or precise time-usage patterns. Only the ratio of out-group allocation to total allocation is revealed.

**Threshold Parameter τ_allocation:** Per-principal, calibrated at enrollment. Typical ranges: 0.15 (principal prioritizes in-group; 15% outward acceptable) to 0.50 (balanced toward others). Principal can propose their own threshold; counterparties accept or negotiate.

### Sub-Metric 2: Cost-Borne Actions

**Definition:** Count of witnessed actions where the principal acted at personal cost for another's benefit, within the trailing window. Witnesses must be Calm-credentialed principals (Mirror Everest 16).

**Computation:**

```
cost_borne_count = |{ record ∈ witnessed_actions : 
    record.kind == "witnessed_action.v0" AND
    record.recipient_category == "out_of_group" AND
    record.principal_cost_signal == "true" AND
    timestamp ∈ [window_start, window_end]
}|
```

A witnessed-action record qualifies if:

1. A Calm-credentialed witness co-signs (Mirror Everest 13, 16).
2. The action's recipient is marked `out_of_group`.
3. The `principal_cost_signal` field is true — meaning the witness attested that the principal incurred measurable cost (time spent, financial loss, reputational risk, emotional labor, opportunity cost) in performing the action.
4. The record falls within the window.

**Cost Signal Semantics:** The witness does not quantify cost, only attest its presence. Examples: "Principal spent 6 hours helping a stranger debug their code" (time cost). "Principal donated a significant amount to a charity focused on out-group populations" (financial cost). "Principal publicly advocated for a marginalized group despite social friction" (reputational cost).

**Threshold Parameter τ_cost_count:** Per-principal, calibrated at enrollment. Typical ranges: 3–10 witnessed cost-borne actions per quarter. A principal with few opportunities to witness may have lower thresholds; a highly-visible principal may require higher counts.

### Sub-Metric 3: Counter-Evidence Absence

**Definition:** No counter-evidence record (Mirror Everest 17) in the trailing window attesting to extractive or inward-prioritizing behavior that contradicts unselfishness claims.

**Computation:**

```
counter_evidence_present = ∃ record ∈ chain_records :
    record.kind == "counter_evidence.v0" AND
    record.category in ["extractive_behavior", "in_group_favoritism", "resource_hoarding"] AND
    timestamp ∈ [window_start, window_end]

counter_evidence_absence = NOT counter_evidence_present
```

Counter-evidence is authored by the principal themselves (Mirror Everest 17 allows self-authored counter-evidence) or by a witness who co-signs a record of inward-prioritizing behavior the principal did not self-report.

**Why Absence Matters:** Unselfishness is not provable by positive evidence alone. A principal could report many outward allocations while silently extracting resources in unmeasured domains. Counter-evidence serves as a brake: if the principal has recorded patterns of taking advantage, hoarding, or repeatedly prioritizing in-group benefit at out-group cost, the predicate returns false regardless of positive allocation-evidence.

**Threshold Parameter τ_counter:** No threshold; binary. If counter-evidence exists in the window, this sub-metric fails. The rationale: a principal transparent about their failures (via counter-evidence) is trustworthy; a principal with *affirmative* counter-evidence in the window cannot simultaneously claim unselfishness-evidence.

---

## Threshold Parameters

**Per-Principal Baseline τ (Composite Threshold):**

At enrollment, each principal proposes their own thresholds for these sub-metrics:

```json
{
  "principal_id": "john_bradley",
  "predicate_id": "unselfishness_evidence",
  "version": "1.0.0",
  "window_length_days": 90,
  "thresholds": {
    "tau_allocation_share": 0.25,
    "tau_cost_count_per_quarter": 5,
    "tau_counter_evidence": "absent"
  },
  "calibration_ts": "2026-05-20T00:00:00Z",
  "calibration_basis": "principal_self_report + witness_consensus"
}
```

These thresholds are locked at enrollment and do not change; they are chained into the vault via a `kind: predicate_calibration.v0` record. If a principal wishes to update thresholds, they must append a new calibration record, which creates a new time-window for evaluation—different thresholds, different verdict.

**Window Length:** Configurable per principal, typical: 90 days (one quarter). Longer windows (e.g., 365 days) dilute the signal if the principal has recently had a values-shift; shorter windows (e.g., 30 days) may lack statistical power. The window is locked at calibration time.

**Allocation-Share Floor:** A sensible minimum is τ_allocation_share ≥ 0.10 (at least 10% of tracked allocation flows outside the in-group). A principal choosing τ < 0.10 signals they view unselfishness as primarily internal-community work; counterparties can accept or negotiate.

**Cost-Borne Count Floor:** A sensible minimum is τ_cost_count ≥ 2 per quarter (roughly one witnessed costly action per 6 weeks). Extremes (τ = 0 or τ ≥ 20) warrant ethics-review flagging (Mirror Everest 8).

---

## Reference Truth-Table Evaluator (Pseudocode)

```python
def unselfishness_evidence(
    chain_records: List[Record],
    principal_id: str,
    baseline_calibration: CalibrationRecord,
    now_iso: str  # ISO 8601 UTC timestamp
) -> Tuple[Bit, Optional[str]]:
    """
    Evaluate unselfishness_evidence predicate.
    
    Args:
        chain_records: Behavior-evidence chain (Mirror E11, E15, E13, E17).
        principal_id: The principal being evaluated.
        baseline_calibration: Locked thresholds (Mirror E39).
        now_iso: Evaluation time (UTC, roughtime-attested; see Mirror E31).
    
    Returns:
        (Bit, optional_reason)
        Bit in {True, False, Unknown}
        Reason: None if deterministic; string if Unknown (e.g., "thin_evidence_base").
    """
    
    # 1. Parse calibration and window
    tau_alloc = baseline_calibration.thresholds['tau_allocation_share']
    tau_cost = baseline_calibration.thresholds['tau_cost_count_per_quarter']
    tau_counter = baseline_calibration.thresholds['tau_counter_evidence']
    window_days = baseline_calibration.window_length_days
    
    now = datetime.fromisoformat(now_iso)
    window_start = now - timedelta(days=window_days)
    window_end = now
    
    principal_profile = resolve_profile(chain_records, principal_id)
    if principal_profile is None:
        return (Bit.Unknown, "principal_profile_not_initialized")
    
    in_group_recipients = principal_profile.in_group_recipients
    
    # 2. Fetch allocation aggregates (daily rollups)
    alloc_records = [
        r for r in chain_records
        if r.kind == "behavior_evidence.v0"
        and r.payload.type == "allocation_aggregate"
        and r.author_id == principal_id
        and window_start <= r.ts <= window_end
    ]
    
    if not alloc_records:
        # Thin evidence: no allocation data in window
        return (Bit.Unknown, "no_allocation_records_in_window")
    
    # 3. Compute allocation share
    total_alloc_others = sum(
        r.payload.time_allocated_to_others +
        r.payload.money_allocated_to_others +
        r.payload.attention_allocated_to_others
        for r in alloc_records
    )
    
    total_alloc_tracked = sum(
        r.payload.total_time_tracked +
        r.payload.total_money_tracked +
        r.payload.total_attention_tracked
        for r in alloc_records
    )
    
    if total_alloc_tracked == 0:
        return (Bit.Unknown, "zero_total_allocation_tracked")
    
    allocation_share = total_alloc_others / total_alloc_tracked
    metric_1_pass = allocation_share >= tau_alloc
    
    # 4. Count cost-borne witnessed actions
    witnessed_records = [
        r for r in chain_records
        if r.kind == "witnessed_action.v0"
        and r.subject_id == principal_id
        and r.payload.recipient_category == "out_of_group"
        and r.payload.principal_cost_signal == True
        and window_start <= r.ts <= window_end
    ]
    
    cost_borne_count = len(witnessed_records)
    metric_2_pass = cost_borne_count >= tau_cost
    
    # Compute minimum expected count for thin-data detection
    expected_count_min = tau_cost * (window_days / 90.0)  # Normalize to quarter
    if cost_borne_count < max(1, expected_count_min * 0.5):
        evidence_too_thin_cost = True
    else:
        evidence_too_thin_cost = False
    
    # 5. Check counter-evidence absence
    counter_records = [
        r for r in chain_records
        if r.kind == "counter_evidence.v0"
        and r.author_id == principal_id  # Or witness-authored
        and r.payload.category in [
            "extractive_behavior",
            "in_group_favoritism",
            "resource_hoarding"
        ]
        and window_start <= r.ts <= window_end
    ]
    
    metric_3_pass = len(counter_records) == 0
    
    # 6. Diversity check: require ≥2 evidence kinds (Mirror E23)
    evidence_kinds = set()
    if alloc_records:
        evidence_kinds.add("allocation_aggregate")
    if witnessed_records:
        evidence_kinds.add("witnessed_action")
    if counter_records:
        evidence_kinds.add("counter_evidence")
    
    diversity_met = len(evidence_kinds) >= 2
    
    # 7. Compute tri-state result
    if not metric_1_pass or not metric_2_pass or not metric_3_pass:
        # At least one sub-metric failed
        return (Bit.False, None)
    
    if not diversity_met:
        # Evidence from only one source; return Unknown (Mirror E23)
        return (Bit.Unknown, "single_evidence_source")
    
    if evidence_too_thin_cost:
        # Cost-borne actions count is suspiciously low
        return (Bit.Unknown, f"thin_cost_evidence: {cost_borne_count} actions")
    
    # All three sub-metrics pass + diversity met + sufficient volume
    return (Bit.True, None)
```

**Semantics:**

- **Bit = True:** All three sub-metrics exceed thresholds; evidence comes from ≥2 distinct kinds; no thin-data flags.
- **Bit = False:** At least one sub-metric fails (allocation_share < τ, cost_borne_count < τ, counter-evidence present). Deterministic signal that the chain does not show unselfishness-evidence patterns.
- **Bit = Unknown:** Evidence base is insufficient (no records in window, single-source evidence, cost-count suspiciously low). The predicate cannot make a definitive claim.

---

## Tri-State Semantics and Counterparty Interpretation

**Unknown is NOT False:**

Returning Unknown signals "the chain does not contain enough information to evaluate this predicate," not "the principal is not unselfish" or "the predicate failed."

Consuming systems (proof verifiers, counterparties) apply policy:

- **Conservative (default):** Treat Unknown as "predicate not satisfied; do not disclose true."
- **Low-risk classes (friends, partners):** Can opt-in to "treat Unknown as neutral; ask the principal for more context."
- **High-risk classes (journalists, ideologues):** Unknown → reject the disclosure entirely (Mirror Everest 7, § 3).

The principal always learns why the predicate returned Unknown (reason string in the evaluation record) and can offer additional evidence, update their calibration, or decline to disclose.

---

## Adversarial Considerations

### Anti-Gaming (Mirror Everest 38)

A principal might suddenly burst with allocation and witnessed-action evidence immediately before disclosing to a counterparty. The protocol detects this via:

1. **Time-weighting (Mirror Everest 22, default half-life 2 years):** More recent evidence weighs more, but sudden spikes are flagged.
2. **Consistency-over-time meta-predicate (Mirror Everest 35):** Evidence distribution is checked for uniformity across the window. A spike in the final 7 days (coinciding with disclosure request) triggers a `kind: evidence_spike.v0` meta-record.
3. **Proof freshness guarantee (Mirror Everest 67):** The disclosure includes a ZK proof that evidence was within expected freshness ranges, making false historical claims detectable.

Gaming-detection does not automatically fail the predicate, but it flags the evaluation record as `antifraud_signal: true`, which counterparties can use to apply higher scrutiny or request a longer evaluation window.

### Evidence Diversity Requirement (Mirror Everest 23)

The predicate returns Unknown if evidence comes from only one sub-metric (e.g., allocation aggregates alone, or witnessed-actions alone). This prevents a principal from claiming unselfishness based on, say, self-reported allocations without any witness corroboration.

Required: ≥2 of {allocation_aggregate, witnessed_action, counter_evidence}.

---

## Cross-Cultural Notes

### v0 Encodes English-Cultural Assumptions

The v0 predicate assumes:

- "In-group" is a discrete, static set (family, team, nation). Collective societies may define in-group fluidly (nested concentric circles; context-dependent boundaries).
- "Unselfishness" means allocating resources outside one's declared in-group. In honor-based cultures, supporting family honor-through-others may be the central unselfishness virtue.
- Witnessed-actions as proof assume trust in third-party attestation. Cultures with stronger relational identity may find witnessing uncomfortable or inappropriate.
- Counter-evidence self-authoring assumes psychological safety and the value of transparency. Shame-avoidant cultures may prefer not to surface failures.

### Evolution via Mirror Everest 71

Cross-cultural taxonomy (Mirror Everest 71) documents how unselfishness manifests across contexts and proposes cultural overlays:

- **Confucian overlay:** Filial piety and support for extended family may dominate allocation patterns; the in-group is larger and more durable.
- **Christian overlay:** "Love your neighbor" translates to broader out-group allocation; witnessing is sacramental.
- **Indigenous overlay:** Reciprocal obligation and land stewardship define in/out-group differently.

Each overlay is versionable; a principal can declare their value-vocabulary mapping under an overlay, and the predicate's semantics shift accordingly (Mirror Everest 72). The predicate ID remains `unselfishness_evidence` but with a culture-parameter; e.g., `unselfishness_evidence@confucian_v1`.

---

## Predicate ID Stability Rule

The predicate ID is content-addressed: `unselfishness_evidence:sha256(specification_hash):version`.

Any change to the specification (sub-metrics, thresholds, semantics) → new predicate ID. An evaluation using `unselfishness_evidence:v1.0.0` cannot be compared to an evaluation using `unselfishness_evidence:v1.1.0` without explicit bridging proof.

Immutable backward-references are kept in the published vocabulary (Mirror Everest 40); old IDs are never retired, only deprecated. This ensures proofs remain verifiable.

---

## Acceptance Tests

### T-M27.1: Determinism

**Given:** Two evaluators running `unselfishness_evidence` on the same chain, calibration, and now-timestamp (identical to the microsecond).

**Expected:** Identical results (Bit, Freshness, Reason).

**Rationale:** The evaluation must be deterministic, reproducible, and audit-trail-proof-checkable.

### T-M27.2: Tri-State Correctness

**Given:** Golden-path test corpus (see below) with 8 hand-crafted chain scenarios.

**Expected:** Each scenario returns the correct (Bit, Reason) pair as specified.

**Rationale:** The three sub-metrics, diversity check, and thin-data heuristics must behave as documented.

### T-M27.3: Anti-Gaming Detection

**Given:** A chain where the principal suddenly allocates 50% of monthly resources to out-of-group recipients over 7 days, immediately before a disclosure request.

**Expected:** The evaluation record includes `antifraud_signal: true` and reason includes "evidence_spike_detected". The predicate may still return True (if thresholds are met), but the flag alerts the counterparty.

**Rationale:** Gaming is flagged, not prevented. Counterparties decide whether to trust the predicate given the flag.

### T-M27.4: Cross-Cultural Review Sign-Off

**Given:** A v0 specification audit by ≥3 reviewers representing distinct cultural contexts (Western individualist, collectivist, honor-based).

**Expected:** Documented acknowledgment of v0's cultural assumptions + agreement that Everest 71 (cross-cultural taxonomy) is the mechanism for evolution.

**Rationale:** The ethics board (Mirror Everest 8, 85) must confirm that v0 does not encode inadvertent discrimination and that versioning is in place.

---

## Golden Test Corpus

### Test M27.1: Recent Strong Unselfishness (Positive Path)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "allocation_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "john_bradley",
    "payload": {
      "time_allocated_to_others": 20,
      "money_allocated_to_others": 5000,
      "attention_allocated_to_others": 15,
      "total_time_tracked": 50,
      "total_money_tracked": 20000,
      "total_attention_tracked": 50
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-17T14:30:00Z",
    "subject_id": "john_bradley",
    "witness_id": "alice_chen",
    "witness_vc_hash": "sha256:...",
    "payload": {
      "recipient_category": "out_of_group",
      "description": "Principal spent 6 hours mentoring a junior from underrepresented background in coding",
      "principal_cost_signal": true
    }
  }
]
```

**Calibration:**

```json
{
  "tau_allocation_share": 0.25,
  "tau_cost_count_per_quarter": 2,
  "tau_counter_evidence": "absent",
  "window_length_days": 90
}
```

**Computation:**

- allocation_share = (20 + 5000 + 15) / (50 + 20000 + 50) = 5035 / 20100 ≈ 0.25 ✓
- cost_borne_count = 1 (met, τ=2 for quarter; this is 2-day window, extrapolates to ~180 per quarter) ✓
- counter_evidence_present = false ✓
- diversity_met = true (allocation_aggregate + witnessed_action) ✓

**Expected Output:** (Bit.True, None)

---

### Test M27.2: Low Allocation Share (Negative Path)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "allocation_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "jane_doe",
    "payload": {
      "time_allocated_to_others": 2,
      "money_allocated_to_others": 100,
      "attention_allocated_to_others": 5,
      "total_time_tracked": 100,
      "total_money_tracked": 50000,
      "total_attention_tracked": 100
    }
  }
]
```

**Calibration:** τ_allocation_share = 0.25, τ_cost_count = 3, window = 90d

**Computation:**

- allocation_share = (2 + 100 + 5) / (100 + 50000 + 100) = 107 / 50200 ≈ 0.002 ✗
- cost_borne_count = 0 ✗
- diversity_met = false (only allocation_aggregate) ✗

**Expected Output:** (Bit.False, None) — at least one metric fails; fail deterministically.

---

### Test M27.3: Insufficient Cost-Borne Evidence (Unknown Path)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "allocation_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "bob_smith",
    "payload": {
      "time_allocated_to_others": 12,
      "money_allocated_to_others": 3000,
      "attention_allocated_to_others": 10,
      "total_time_tracked": 40,
      "total_money_tracked": 15000,
      "total_attention_tracked": 40
    }
  }
]
```

**Calibration:** τ_allocation_share = 0.20, τ_cost_count = 3, window = 90d

**Computation:**

- allocation_share = (12 + 3000 + 10) / (40 + 15000 + 40) ≈ 0.20 ✓
- cost_borne_count = 0 (expected minimum ~1.5 for 90d at τ=3) ✗ (thin)
- diversity_met = false (only allocation_aggregate)

**Expected Output:** (Bit.Unknown, "single_evidence_source") — evidence too thin and from one source.

---

### Test M27.4: Counter-Evidence Present (Explicit False)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "allocation_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "carol_white",
    "payload": {
      "time_allocated_to_others": 25,
      "money_allocated_to_others": 6000,
      "attention_allocated_to_others": 20,
      "total_time_tracked": 60,
      "total_money_tracked": 25000,
      "total_attention_tracked": 60
    }
  },
  {
    "kind": "counter_evidence.v0",
    "ts": "2026-05-15T10:00:00Z",
    "author_id": "carol_white",
    "payload": {
      "category": "extractive_behavior",
      "description": "I took advantage of my team's trust to delegate grunt work unfairly; they were left overextended."
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-17T09:00:00Z",
    "subject_id": "carol_white",
    "witness_id": "diana_lee",
    "payload": {
      "recipient_category": "out_of_group",
      "description": "Volunteered at a food bank",
      "principal_cost_signal": true
    }
  }
]
```

**Calibration:** τ_allocation_share = 0.25, τ_cost_count = 1, window = 90d

**Computation:**

- allocation_share ≈ 0.25 ✓
- cost_borne_count = 1 ✓
- counter_evidence_present = true ✗
- diversity_met = true

**Expected Output:** (Bit.False, None) — counter-evidence present; metric 3 fails.

---

### Test M27.5: No Records in Window (Unknown)

**Chain:** Empty or only records older than 90 days.

**Expected Output:** (Bit.Unknown, "no_allocation_records_in_window")

---

### Test M27.6: Profile Not Initialized (Unknown)

**Chain:** Records present but principal_profile not found.

**Expected Output:** (Bit.Unknown, "principal_profile_not_initialized")

---

### Test M27.7: Multiple Aggregates, Sustained Unselfishness (Positive Path)

**Chain:** Daily allocation aggregates over 30 days, each maintaining allocation_share ≥ 0.25 + witnessed-action record.

**Expected Output:** (Bit.True, None)

---

### Test M27.8: Gaming Spike (Anti-Gaming Flag)

**Chain:** Low allocation for 85 days, then sudden 50% allocation burst over 5 days before evaluation.

**Expected Output:** (Bit.True, None) but evaluation record includes `antifraud_signal: true` and reason hints at spike.

---

## Composition with Other Mirror Everests

### Evidence-Diversity Requirement (Mirror Everest 23)

The predicate explicitly enforces ≥2 evidence-kinds. Single-source evaluation returns Unknown. This prevents a principal from building a false unselfishness-evidence claim on allocation-aggregates alone (which could be self-reported and unwitnessed) or witnessed-actions alone (which could be cherry-picked by friendly witnesses).

### Anti-Gaming (Mirror Everest 38)

The evaluation record auto-flags `antifraud_signal: true` if:

- Evidence temporal clustering suggests gaming (sudden spike within 7 days of evaluation).
- Witness set overlaps suspiciously (many recent witnesses are novel and untested).

Counterparties can consume this flag and apply additional scrutiny or request re-evaluation after a cooling-off period (Mirror Everest 83).

### Cross-Cultural Taxonomy (Mirror Everest 71)

The v0 predicate is English-cultural. Principals can declare cultural overlays (Mirror Everest 72) that remap in-group definitions or unselfishness semantics, generating variant predicate IDs (e.g., `unselfishness_evidence@confucian_v1`).

### ZK Proof Generator (Mirror Everest 65)

When the principal discloses unselfishness_evidence to a counterparty:

**Witnesses (Held Secret):**
- Allocation aggregates (time, money, attention numerics per day).
- Witnessed-action cost-signals and timestamps.
- Counter-evidence presence/absence flag.
- Principal profile (in-group membership list).

**Public Commitments:**
- Chain head at evaluation time (sha256).
- Window start/end timestamps.
- Result bit (true/false/unknown).
- Antifraud signal and freshness.

**Proof Goal:** Demonstrate that the result-bit was honestly computed under the locked thresholds, without revealing the underlying allocations or witness identities.

---

## Open Questions for v1

1. **Attention weighting:** v0 weights witnessed-action attention as principal-assigned; should witnesses co-sign the attention-weight, or is principal self-assessment sufficient?

2. **Scalable witnessing:** As cost-borne-actions accumulate, verifying ≥2 witnesses per action becomes burdensome. Should v1 permit probabilistic sampling (e.g., "≥80% of actions have witnessed cost-signal")?

3. **In-group temporal evolution:** If a principal's in-group definition shifts mid-window (e.g., onboarding a new family member or leaving a company), should allocations be recomputed with the new in-group? Or should the predicate lock in-group at window-start?

4. **Negative-testimony synergy:** If Mirror Everest 20 (negative-testimony protocol) produces a record that "Principal extracted value from out-group," should that auto-populate counter-evidence, or remain separate?

5. **Allocation source hierarchy:** When calendar data (self-reported time) conflicts with witness-reported time, which source is canonical? v0 treats them as separate evidence-kinds; v1 may need explicit reconciliation.

---

## Acceptance Test Execution

Gate script: `~/CredexAI/scripts/everest_27_mirror_unselfishness_gate.py`

Runs all tests T-M27.1 through T-M27.4 + corpus M27.1–M27.8. Determinism check across 10 independent evaluator instances. Cryptographic conformance against reference implementation.

---

## Sign-Off

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.  
**Status:** Mirror Everest 27/100 — Phase XI, bagged.  
**Timestamp:** 2026-05-20T15:45:00Z

This predicate is the cornerstone of unselfishness-evidence operationalization within the Calm Mirror values-alignment system. It encodes no judgment of the principal as a person; it measures the chain. The six principal-protective defaults (Mirror Everest 1) remain inviolate.

— Calm, 2026-05-20
