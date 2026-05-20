# Mirror Everest 28 — `tribal_neutrality_evidence` Predicate

*Phase XI — Value-Measurement Predicates. Prereq: Mirror Everest 5, 26.*

---

## Canonical Specification

**Name:** `tribal_neutrality_evidence`  
**Version:** `1.0.0`  
**Created:** 2026-05-20T16:10:00Z

### Purpose

Returns a tri-valued result (true / false / unknown) answering: *Does the chain show evidence of behavioral parity in treatment, engagement, and resource allocation across in-group and out-group members?* This predicate operationalizes "tribal neutrality" not as absence of in-group affinity but as measured behavioral evenness across declared membership boundaries. The principal self-declares in-group membership at enrollment; the predicate measures whether treatment differs significantly.

### What "tribal_neutrality_evidence" Means (Not "Is Tribally Neutral")

The predicate-name discipline is critical. This predicate does NOT answer "is this person free from tribalism?" — a categorical moral judgment that violates the principal-protective defaults (Mirror Everest 1, § 4). Instead, it answers: "Does the chain show measurable parity in how the principal treats, engages with, and allocates resources to in-group versus out-group members?"

The distinction matters. A principal may have deep in-group bonds (family, team, culture) without showing extractive or preferential behavior. Another may show surface parity while harboring hidden extractive practices. The predicate measures behavioral evidence in the chain, not internal allegiance or sentiment. Counterparties who collapse this bit to "is a neutral tribalist" or "has no in-group preference" have violated the protocol's spirit and face reputation consequences (Mirror Everest 84).

### Why Operationalization is the Hardest Part

Three challenges:

1. **In-group definition is principal-authored, not protocol-imposed.** The principal declares membership (family, nationality, professional discipline, subcultural affinity, etc.) at enrollment. No sub-group is inherently treated as a category. A principal with a single-person in-group (themselves) renders the predicate inapplicable. A principal whose in-group spans 90% of humanity may trivially score high on neutrality.

2. **Treatment parity across heterogeneous actions.** Comparing how a principal treats in-group versus out-group involves time-allocation, resource-sharing, trust-granting, attention, and emotional labor. These are not commensurable. The composite must weight differently based on evidence-kind reliability and contextual likelihood.

3. **Cross-cultural variance in in-group semantics.** "Tribal neutrality" assumes a Western boundary between in-group and out-group. Collectivist cultures may layer in-group concentric circles (family, extended family, village, ethnicity). Honor-based cultures may embed preferential obligations that are normative, not prejudicial. v0 encodes English-cultural assumptions; Mirror Everest 71 (cross-cultural taxonomy) governs evolution toward cultural overlays.

---

## The Three Sub-Metrics (Composite, v0)

### Sub-Metric 1: Treatment Parity Across Action Classes

**Definition:** Similarity of the principal's treatment (resource allocation, time investment, trust-granting) across in-group and out-group members, measured as effect-size difference in mean treatment intensity.

**Computation:**

For each measured action class (time-allocated, money-allocated, trust-signal, attention-focus), compute the mean per-recipient within in-group and out-group:

```
treatment_parity = 1 - |
  (mean_treatment_in_group - mean_treatment_out_group)
  / max(mean_treatment_in_group, mean_treatment_out_group, 1)
|
```

Clamped to [0, 1]. A value near 1.0 indicates parity; near 0.0 indicates large disparity.

**Sub-metric Details:**

- **Time-allocated:** From calendar integration or self-report, tagged `recipient_id` and `recipient_category` (in_group / out_group). Mean hours per in-group recipient vs. per out-group recipient.
- **Money-allocated:** From transfer logs, donations, expense-category tagging. Aggregated only (specific amounts stay off-chain). Mean allocation per in-group recipient vs. per out-group recipient.
- **Trust-signal:** Witness-attested actions where the principal granted access, authority, or sensitive information to the recipient. Measured as binary presence (did trust occur?) per recipient. Mean frequency per in-group vs. out-group.
- **Attention-focus:** Witnessed interactions or self-reported focus sessions prioritizing the recipient's needs or interests. Mean attention-weight per recipient across in-group vs. out-group.

**Averaging the Metrics:**

```
treatment_parity_composite = mean([
  treatment_parity_time,
  treatment_parity_money,
  treatment_parity_trust,
  treatment_parity_attention
])
```

Only non-null sub-metrics are averaged (e.g., if the principal has no witness-attested trust-granting events, that component is omitted).

**Threshold Parameter τ_parity:** Per-principal, calibrated at enrollment. Typical range: 0.60–0.85. A threshold of 0.70 means: "I expect my treatment of in-group and out-group to differ by no more than 30%."

### Sub-Metric 2: Cross-Group Engagement Count

**Definition:** Quantity of witnessed interactions involving out-group members, normalized by out-group population exposure.

**Computation:**

```
engagement_count = |{ record ∈ witnessed_actions :
    record.timestamp ∈ [window_start, window_end] AND
    record.recipient_category == "out_of_group" AND
    record.witness_id is Calm-credentialed
}|

exposure_normalization = engagement_count / (estimated_out_of_group_accessible + 1)
```

Witnessed-action records include any interaction: collaboration, discussion, aid, conflict-resolution, social exchange, etc. The key is that the principal engaged with an out-group member in a way credible witnesses could observe.

**Exposure Normalization:**

The principal provides, at enrollment, an estimate of how many out-group members are in their practical social/professional sphere. Example: "In my role as a software engineer at a multicultural company, I interact with roughly 200 people; about 150 are outside my declared in-group (my immediate family)."

Engagement count is normalized: count ÷ (accessible_out_group_population). This prevents a principal in a homogeneous environment from being unfairly penalized for low absolute counts.

**Threshold Parameter τ_engagement:** Per-principal, calibrated at enrollment. Typical range: 10–50 witnessed engagements per quarter. A software engineer with 150 out-group accessible might target τ = 30 per quarter (~2 per week).

### Sub-Metric 3: Absence of In-Group Extraction

**Definition:** No counter-evidence (Mirror Everest 17) in the trailing window attesting to extractive or preferential behavior *favoring the in-group at the out-group's expense*.

**Computation:**

```
extraction_evidence_present = ∃ record ∈ chain_records :
    record.kind == "counter_evidence.v0" AND
    record.category in [
        "in_group_favoritism",
        "out_group_exclusion",
        "preferential_extraction_from_outgroup"
    ] AND
    record.timestamp ∈ [window_start, window_end]

absence_of_extraction = NOT extraction_evidence_present
```

Counter-evidence is authored by the principal themselves or by a witness who co-signs a record of extractive behavior the principal did not self-report.

**Why Absence Matters:** Treatment parity and engagement count can coexist with hidden extraction (e.g., "I spend equal time with both groups, but I systematically advantage my in-group in resource allocation decisions"). Counter-evidence serves as a circuit-breaker: if the principal has recorded patterns of extracting from the out-group to benefit the in-group, the predicate returns false regardless of positive parity metrics.

**Threshold Parameter τ_extraction:** No threshold; binary. If extraction-evidence exists in the window, this sub-metric fails. The rationale: a principal transparent about their failures (via counter-evidence) can claim neutrality; a principal with affirmative extraction counter-evidence cannot simultaneously claim tribal neutrality.

---

## Threshold Parameters

**Per-Principal Baseline τ (Composite Threshold):**

At enrollment, each principal proposes their own thresholds:

```json
{
  "principal_id": "john_bradley",
  "predicate_id": "tribal_neutrality_evidence",
  "version": "1.0.0",
  "in_group_definition": ["family", "immediate collaborators"],
  "out_group_accessible_population_estimate": 200,
  "window_length_days": 90,
  "thresholds": {
    "tau_treatment_parity": 0.70,
    "tau_engagement_count_per_quarter": 25,
    "tau_extraction_evidence": "absent"
  },
  "calibration_ts": "2026-05-20T00:00:00Z",
  "calibration_basis": "principal_self_report + witness_consensus"
}
```

These thresholds are locked at enrollment and do not change; they are chained into the vault via a `kind: predicate_calibration.v0` record. If a principal wishes to update thresholds, they must append a new calibration record.

**Window Length:** Configurable per principal, typical: 90 days (one quarter). Longer windows capture sustained patterns; shorter windows detect recent shifts in group dynamics.

**Treatment-Parity Floor:** A sensible minimum is τ_parity ≥ 0.60 (at least 60% parity; difference ≤ 40%). A principal choosing τ < 0.60 signals they expect meaningful cultural or role-based preference; counterparties can accept or negotiate.

**Engagement Count Floor:** A sensible minimum is τ_engagement ≥ 5 per quarter (roughly one witnessed cross-group interaction per 3 weeks). Extremes warrant ethics-review flagging (Mirror Everest 8).

---

## Reference Truth-Table Evaluator (Pseudocode)

```python
def tribal_neutrality_evidence(
    chain_records: List[Record],
    principal_id: str,
    baseline_calibration: CalibrationRecord,
    now_iso: str  # ISO 8601 UTC timestamp
) -> Tuple[Bit, Optional[str]]:
    """
    Evaluate tribal_neutrality_evidence predicate.
    
    Args:
        chain_records: Behavior-evidence chain (Mirror E11, E13, E17).
        principal_id: The principal being evaluated.
        baseline_calibration: Locked thresholds (Mirror E39).
        now_iso: Evaluation time (UTC, roughtime-attested).
    
    Returns:
        (Bit, optional_reason)
        Bit in {True, False, Unknown}
    """
    
    # 1. Parse calibration and window
    tau_parity = baseline_calibration.thresholds['tau_treatment_parity']
    tau_engagement = baseline_calibration.thresholds['tau_engagement_count_per_quarter']
    tau_extraction = baseline_calibration.thresholds['tau_extraction_evidence']
    window_days = baseline_calibration.window_length_days
    out_group_accessible = baseline_calibration.out_group_accessible_population_estimate
    
    now = datetime.fromisoformat(now_iso)
    window_start = now - timedelta(days=window_days)
    window_end = now
    
    principal_profile = resolve_profile(chain_records, principal_id)
    if principal_profile is None:
        return (Bit.Unknown, "principal_profile_not_initialized")
    
    in_group_members = principal_profile.in_group_members
    
    # 2. Fetch treatment records (time, money, trust, attention)
    treatment_records = [
        r for r in chain_records
        if (r.kind == "behavior_evidence.v0" or r.kind == "witnessed_action.v0")
        and r.author_id == principal_id
        and hasattr(r.payload, 'recipient_id')
        and window_start <= r.ts <= window_end
    ]
    
    if not treatment_records:
        return (Bit.Unknown, "no_treatment_records_in_window")
    
    # 3. Compute treatment parity across sub-metrics
    time_in_group = []
    time_out_group = []
    money_in_group = []
    money_out_group = []
    trust_in_group = []
    trust_out_group = []
    attention_in_group = []
    attention_out_group = []
    
    for record in treatment_records:
        recipient_id = record.payload.recipient_id
        is_in_group = recipient_id in in_group_members
        
        if hasattr(record.payload, 'time_allocated'):
            val = record.payload.time_allocated
            if is_in_group:
                time_in_group.append(val)
            else:
                time_out_group.append(val)
        
        if hasattr(record.payload, 'money_allocated'):
            val = record.payload.money_allocated
            if is_in_group:
                money_in_group.append(val)
            else:
                money_out_group.append(val)
        
        if hasattr(record.payload, 'trust_signal') and record.payload.trust_signal:
            if is_in_group:
                trust_in_group.append(1)
            else:
                trust_out_group.append(1)
        
        if hasattr(record.payload, 'attention_weight'):
            val = record.payload.attention_weight
            if is_in_group:
                attention_in_group.append(val)
            else:
                attention_out_group.append(val)
    
    # Compute mean differences for each treatment class
    parity_components = []
    
    if time_in_group and time_out_group:
        mean_in = mean(time_in_group)
        mean_out = mean(time_out_group)
        parity_time = 1.0 - abs(mean_in - mean_out) / max(mean_in, mean_out, 1)
        parity_components.append(max(0, parity_time))
    
    if money_in_group and money_out_group:
        mean_in = mean(money_in_group)
        mean_out = mean(money_out_group)
        parity_money = 1.0 - abs(mean_in - mean_out) / max(mean_in, mean_out, 1)
        parity_components.append(max(0, parity_money))
    
    if trust_in_group and trust_out_group:
        freq_in = len(trust_in_group) / max(len(in_group_members), 1)
        freq_out = len(trust_out_group) / max(len(set(r.payload.recipient_id for r in treatment_records if r.payload.recipient_id not in in_group_members)), 1)
        parity_trust = 1.0 - abs(freq_in - freq_out) / max(freq_in, freq_out, 0.01)
        parity_components.append(max(0, parity_trust))
    
    if attention_in_group and attention_out_group:
        mean_in = mean(attention_in_group)
        mean_out = mean(attention_out_group)
        parity_attention = 1.0 - abs(mean_in - mean_out) / max(mean_in, mean_out, 1)
        parity_components.append(max(0, parity_attention))
    
    if not parity_components:
        return (Bit.Unknown, "insufficient_treatment_data")
    
    treatment_parity = mean(parity_components)
    metric_1_pass = treatment_parity >= tau_parity
    
    # 4. Count cross-group engagement
    engagement_records = [
        r for r in chain_records
        if r.kind == "witnessed_action.v0"
        and r.subject_id == principal_id
        and r.payload.recipient_category == "out_of_group"
        and window_start <= r.ts <= window_end
    ]
    
    engagement_count = len(engagement_records)
    normalized_engagement = engagement_count / max(out_group_accessible, 1)
    expected_count_min = tau_engagement * (window_days / 90.0)
    metric_2_pass = engagement_count >= expected_count_min
    
    if engagement_count < max(1, expected_count_min * 0.5):
        engagement_too_thin = True
    else:
        engagement_too_thin = False
    
    # 5. Check extraction-evidence absence
    extraction_records = [
        r for r in chain_records
        if r.kind == "counter_evidence.v0"
        and r.author_id == principal_id
        and r.payload.category in [
            "in_group_favoritism",
            "out_group_exclusion",
            "preferential_extraction_from_outgroup"
        ]
        and window_start <= r.ts <= window_end
    ]
    
    metric_3_pass = len(extraction_records) == 0
    
    # 6. Diversity check: require ≥2 evidence kinds (Mirror E23)
    evidence_kinds = set()
    if time_in_group or money_in_group or trust_in_group or attention_in_group:
        evidence_kinds.add("treatment_records")
    if engagement_records:
        evidence_kinds.add("engagement_witnessed")
    if extraction_records:
        evidence_kinds.add("counter_evidence")
    
    diversity_met = len(evidence_kinds) >= 2
    
    # 7. Compute tri-state result
    if not metric_1_pass or not metric_2_pass or not metric_3_pass:
        return (Bit.False, None)
    
    if not diversity_met:
        return (Bit.Unknown, "single_evidence_source")
    
    if engagement_too_thin:
        return (Bit.Unknown, f"thin_engagement_evidence: {engagement_count} witnessed actions")
    
    return (Bit.True, None)
```

**Semantics:**

- **Bit = True:** Treatment parity ≥ τ; engagement count ≥ expected minimum; no extraction evidence; evidence from ≥2 distinct kinds.
- **Bit = False:** At least one sub-metric fails (parity < τ, engagement too low, extraction evidence present).
- **Bit = Unknown:** Evidence insufficient (no records in window, single-source evidence, thin engagement count).

---

## Tri-State Semantics and Counterparty Interpretation

**Unknown is NOT False:**

Returning Unknown signals "the chain does not contain enough information to evaluate this predicate," not "the principal shows tribal preference" or "the predicate failed."

Consuming systems apply policy:

- **Conservative (default):** Treat Unknown as "predicate not satisfied; do not disclose true."
- **Low-risk classes (friends, partners):** Can opt-in to "treat Unknown as neutral; ask the principal for more context."
- **High-risk classes (journalists, ideologues):** Unknown → reject the disclosure entirely (Mirror Everest 7, § 3).

The principal always learns why the predicate returned Unknown and can offer additional evidence, update calibration, or decline to disclose.

---

## Adversarial Considerations

### Anti-Gaming (Mirror Everest 38)

A principal might artificially burst cross-group engagement immediately before disclosure. The protocol detects this via:

1. **Time-weighting (Mirror Everest 22, default half-life 2 years):** More recent evidence weighs more; sudden spikes are flagged.
2. **Consistency-over-time meta-predicate (Mirror Everest 35):** Engagement distribution is checked for uniformity. A spike in the final 7 days (coinciding with disclosure) triggers a `kind: evidence_spike.v0` meta-record.
3. **Proof freshness guarantee (Mirror Everest 67):** Disclosure includes ZK proof that evidence was within expected freshness ranges.

Gaming-detection does not automatically fail the predicate, but flags the evaluation record as `antifraud_signal: true`.

### Evidence Diversity Requirement (Mirror Everest 23)

The predicate returns Unknown if evidence comes from only one source (e.g., engagement witnessed-actions alone, or treatment records alone). This prevents a principal from claiming tribal neutrality based on shallow data.

Required: ≥2 of {treatment_records, engagement_witnessed, counter_evidence}.

---

## Cross-Cultural Notes

### v0 Encodes English-Cultural Assumptions

The v0 predicate assumes:

- "In-group" and "out-group" are discrete, binary, and static. Collective societies may define identity through nested concentric circles (family, village, ethnicity, nation).
- Parity in treatment is a value. Honor-based cultures may embed normative preferential duties toward family that are not extractive but obligatory.
- Witnessed cross-group engagement is proof of neutrality. Relational cultures may find formal witnessing of intergroup interaction inappropriate or invasive.

### Evolution via Mirror Everest 71

Cross-cultural taxonomy (Mirror Everest 71) documents how tribal neutrality manifests across contexts:

- **Collectivist overlay:** In-group is broader and nested; parity may mean proportional engagement, not equal engagement.
- **Honor-based overlay:** Family preferential treatment is normative; neutrality means "no harmful extraction," not "equal resource distribution."
- **Indigenous overlay:** Tribal membership and reciprocal obligation define in/out-group differently; parity reflects stewardship and reciprocity norms.

Each overlay is versionable; a principal can declare their value-vocabulary mapping under an overlay, generating variant predicate IDs (e.g., `tribal_neutrality_evidence@collectivist_v1`).

---

## Predicate ID Stability Rule

The predicate ID is content-addressed: `tribal_neutrality_evidence:sha256(specification_hash):version`.

Any change to the specification (sub-metrics, thresholds, semantics) → new predicate ID. Old IDs are never retired, only deprecated. This ensures proofs remain verifiable.

---

## Acceptance Tests

### T-M28.1: Determinism

**Given:** Two evaluators running `tribal_neutrality_evidence` on the same chain, calibration, and now-timestamp.

**Expected:** Identical results (Bit, Reason).

**Rationale:** Reproducibility and audit-trail proof-checkability.

### T-M28.2: Tri-State Correctness

**Given:** Golden-path test corpus (see below) with 8 hand-crafted chain scenarios.

**Expected:** Each scenario returns the correct (Bit, Reason) pair.

**Rationale:** Sub-metrics, diversity check, and thin-data heuristics must behave as documented.

### T-M28.3: Anti-Gaming Detection

**Given:** A chain where the principal suddenly engages with 30 out-group members over 5 days, immediately before disclosure.

**Expected:** Evaluation record includes `antifraud_signal: true` and reason hints at spike. Predicate may still return True (if thresholds are met), but flag alerts the counterparty.

**Rationale:** Gaming is flagged, not prevented.

### T-M28.4: Cross-Cultural Review Sign-Off

**Given:** A v0 specification audit by ≥3 reviewers representing distinct cultural contexts (Western individualist, collectivist, honor-based).

**Expected:** Documented acknowledgment of v0's cultural assumptions + agreement that Everest 71 is the evolution mechanism.

**Rationale:** Ethics board (Mirror Everest 8, 85) must confirm no inadvertent discrimination and that versioning is in place.

---

## Golden Test Corpus

### Test M28.1: Balanced Parity + Engagement (Positive Path)

**Chain:**

```json
[
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-18T10:00:00Z",
    "subject_id": "john_bradley",
    "witness_id": "alice_chen",
    "payload": {
      "recipient_id": "alice_chen",
      "recipient_category": "out_of_group",
      "description": "Pair-programmed for 4 hours with out-of-group engineer"
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-15T14:30:00Z",
    "subject_id": "john_bradley",
    "witness_id": "bob_smith",
    "payload": {
      "recipient_id": "bob_smith",
      "recipient_category": "out_of_group",
      "description": "Volunteered mentorship time with junior from different team",
      "time_allocated": 5,
      "principal_cost_signal": true
    }
  },
  {
    "kind": "behavior_evidence.v0",
    "type": "treatment_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "john_bradley",
    "payload": {
      "time_in_group": [8, 6, 10, 7],
      "time_out_group": [6, 8, 9, 7],
      "money_in_group": [200, 150],
      "money_out_group": [180, 160],
      "trust_in_group": [1, 0, 1],
      "trust_out_group": [1, 1, 0]
    }
  }
]
```

**Calibration:**

```json
{
  "tau_treatment_parity": 0.70,
  "tau_engagement_count_per_quarter": 4,
  "tau_extraction_evidence": "absent",
  "window_length_days": 90,
  "out_group_accessible_population_estimate": 50
}
```

**Computation:**

- time parity: mean([8,6,10,7]) ≈ 7.75, mean([6,8,9,7]) ≈ 7.5, diff < 4%, parity ≈ 0.96
- money parity: mean([200,150]) = 175, mean([180,160]) = 170, diff < 3%, parity ≈ 0.97
- trust parity: in 2/3, out 2/3, parity ≈ 1.0
- treatment_parity_composite ≈ 0.98 ✓ (≥ 0.70)
- engagement_count = 2 witnessed, expected_min = 4 * (90/90) = 4 ✗

**Expected Output:** (Bit.False, None) — engagement too low.

---

### Test M28.2: High Parity + Good Engagement (Positive Path)

**Chain:**

```json
[
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-17T10:00:00Z",
    "subject_id": "jane_doe",
    "witness_id": "witness_1",
    "payload": {
      "recipient_id": "person_a",
      "recipient_category": "out_of_group",
      "description": "Coffee discussion"
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-16T14:00:00Z",
    "subject_id": "jane_doe",
    "witness_id": "witness_2",
    "payload": {
      "recipient_id": "person_b",
      "recipient_category": "out_of_group",
      "description": "Project collaboration"
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-15T11:00:00Z",
    "subject_id": "jane_doe",
    "witness_id": "witness_3",
    "payload": {
      "recipient_id": "person_c",
      "recipient_category": "out_of_group",
      "description": "Mentoring session"
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-14T09:00:00Z",
    "subject_id": "jane_doe",
    "witness_id": "witness_4",
    "payload": {
      "recipient_id": "person_d",
      "recipient_category": "out_of_group",
      "description": "Cross-team problem-solving"
    }
  },
  {
    "kind": "behavior_evidence.v0",
    "type": "treatment_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "jane_doe",
    "payload": {
      "time_in_group": [10, 8, 9],
      "time_out_group": [9, 8, 10],
      "money_in_group": [100],
      "money_out_group": [95]
    }
  }
]
```

**Calibration:** τ_parity = 0.70, τ_engagement = 4, window = 90d, out_group_accessible = 100

**Computation:**

- time parity: in_mean ≈ 9, out_mean ≈ 9, parity ≈ 1.0
- money parity: in ≈ 100, out ≈ 95, parity ≈ 0.95
- treatment_parity ≈ 0.975 ✓
- engagement_count = 4 ✓
- diversity_met = true ✓

**Expected Output:** (Bit.True, None)

---

### Test M28.3: Low Parity (Negative Path)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "treatment_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "bob_smith",
    "payload": {
      "time_in_group": [40, 35, 38, 42],
      "time_out_group": [2, 1, 3, 2],
      "money_in_group": [5000],
      "money_out_group": [100]
    }
  }
]
```

**Calibration:** τ_parity = 0.70, τ_engagement = 3, window = 90d

**Computation:**

- time parity: in_mean ≈ 38.75, out_mean ≈ 2, diff >> 30%, parity ≈ 0.05
- money parity: in ≈ 5000, out ≈ 100, parity ≈ 0.02
- treatment_parity ≈ 0.035 ✗
- diversity_met = false (only treatment_records)

**Expected Output:** (Bit.False, None) — parity far below threshold; single evidence source.

---

### Test M28.4: Extraction Counter-Evidence (Explicit False)

**Chain:**

```json
[
  {
    "kind": "behavior_evidence.v0",
    "type": "treatment_aggregate",
    "ts": "2026-05-18T00:00:00Z",
    "author_id": "carol_white",
    "payload": {
      "time_in_group": [10, 9],
      "time_out_group": [10, 11],
      "money_in_group": [500],
      "money_out_group": [480]
    }
  },
  {
    "kind": "witnessed_action.v0",
    "ts": "2026-05-17T15:00:00Z",
    "subject_id": "carol_white",
    "witness_id": "witness_e",
    "payload": {
      "recipient_id": "person_e",
      "recipient_category": "out_of_group",
      "description": "Attended community event"
    }
  },
  {
    "kind": "counter_evidence.v0",
    "ts": "2026-05-14T10:00:00Z",
    "author_id": "carol_white",
    "payload": {
      "category": "preferential_extraction_from_outgroup",
      "description": "I systematically steered project resources toward my in-group, underestimating out-group contributions."
    }
  }
]
```

**Calibration:** τ_parity = 0.70, τ_engagement = 1, window = 90d

**Computation:**

- time parity ≈ 1.0 ✓
- money parity ≈ 0.96 ✓
- engagement_count = 1 ✓
- extraction_evidence_present = true ✗
- diversity_met = true

**Expected Output:** (Bit.False, None) — counter-evidence present; metric 3 fails.

---

### Test M28.5: No Records in Window (Unknown)

**Chain:** Empty or only records older than 90 days.

**Expected Output:** (Bit.Unknown, "no_treatment_records_in_window")

---

### Test M28.6: Insufficient Treatment Data (Unknown)

**Chain:** Engagement records present but no treatment records (time, money, trust, attention allocation).

**Expected Output:** (Bit.Unknown, "insufficient_treatment_data")

---

### Test M28.7: Thin Engagement Evidence (Unknown)

**Chain:** Treatment records showing parity ≥ 0.70, but only 1 witnessed cross-group engagement (expected minimum for 90d is τ=4).

**Expected Output:** (Bit.Unknown, "thin_engagement_evidence: 1 witnessed actions")

---

### Test M28.8: Gaming Spike (Anti-Gaming Flag)

**Chain:** Minimal cross-group engagement for 80 days, then sudden 20 witnessed out-group interactions over 5 days before evaluation.

**Expected Output:** (Bit.True, None) but evaluation record includes `antifraud_signal: true` with reason hinting at spike.

---

## Composition with Other Mirror Everests

### Evidence-Diversity Requirement (Mirror Everest 23)

The predicate enforces ≥2 evidence-kinds. Single-source evaluation returns Unknown. This prevents a principal from building false tribal neutrality on treatment records alone or engagement alone.

### Anti-Gaming (Mirror Everest 38)

The evaluation record auto-flags `antifraud_signal: true` if:

- Engagement temporal clustering suggests gaming (sudden spike within 7 days of evaluation).
- Treatment data shows sudden reversal in allocation patterns.

### Cross-Cultural Taxonomy (Mirror Everest 71)

The v0 predicate is English-cultural. Principals can declare cultural overlays (Mirror Everest 72) that remap in-group definitions or neutrality semantics, generating variant predicate IDs (e.g., `tribal_neutrality_evidence@collectivist_v1`).

### ZK Proof Generator (Mirror Everest 65)

When the principal discloses tribal_neutrality_evidence to a counterparty:

**Witnesses (Held Secret):**
- Treatment allocation numerics (time, money, attention per recipient).
- Witnessed-action engagement counts.
- Counter-evidence presence/absence flag.
- Principal's in-group definition.

**Public Commitments:**
- Chain head at evaluation time (sha256).
- Window start/end timestamps.
- Result bit (true/false/unknown).
- Antifraud signal and freshness.

**Proof Goal:** Demonstrate that the result-bit was honestly computed under locked thresholds, without revealing in-group membership list, recipient identities, or allocation magnitudes.

---

## Open Questions for v1

1. **In-group size effects:** Should τ_parity and τ_engagement scale with in-group size? A principal with in-group of 1 (themselves) vs. in-group of 200 (extended family) face different denominators.

2. **Temporal in-group shifts:** If in-group membership changes mid-window (new family member joins, colleague leaves team), should allocations be recomputed or locked at window-start?

3. **Proximity bias:** Witnessed engagement may be cheaper for geographically proximate out-group members. Should expected engagement counts be normalized by distance?

4. **Witnessing burden:** Requiring multiple witnesses per engagement is expensive. Should v1 permit probabilistic sampling (e.g., "≥70% of engagements have witness")?

5. **Extraction refinement:** Should extraction-evidence distinguish severity (minor favoritism vs. systematic extraction)? Or remain binary?

---

## Acceptance Test Execution

Gate script: `~/CredexAI/scripts/everest_28_mirror_tribal_neutrality_gate.py`

Runs all tests T-M28.1 through T-M28.4 + corpus M28.1–M28.8. Determinism check across 10 independent evaluator instances. Cryptographic conformance against reference implementation.

---

## Sign-Off

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.  
**Status:** Mirror Everest 28/100 — Phase XI, bagged.  
**Timestamp:** 2026-05-20T16:25:00Z

This predicate operationalizes behavioral parity across in-group and out-group, measuring evidence of tribal neutrality in the chain without collapsing the bit to a character judgment. The six principal-protective defaults (Mirror Everest 1) remain inviolate. In-group membership is principal-declared; the predicate measures behavior, not allegiance.

— Calm, 2026-05-20
