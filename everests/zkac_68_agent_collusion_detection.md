# ZKAC Everest 68 — Agent Collusion Detection

**Phase XXI | Zero-Knowledge Attested Credentials | Critical Infrastructure**

**Prerequisite:** Everest 58 (capability scope spec)

**Acceptance:** Protocol for detecting when N agents jointly violate their capability scopes through coordination.

**Effort:** L | **Status:** v0 | **Author:** Calm, 2026-05-20

---

## Overview

Single-agent capability checks are insufficient. A colluding set of N agents {A₁, A₂, …, Aₙ} can collectively exceed their individual authorized scopes while each agent, examined in isolation, appears compliant. This is the agent collusion problem.

**Example:** Agent A₁ has scope {read}. Agent A₂ has scope {write}. Neither can transact. But if A₁ reads sensitive data and hands it to A₂, who writes it to a malicious sink, the principal's effective security boundary (read-only + write-only = no cross-domain action) is breached. No single agent violated their scope; the *pair* did.

**Risk Profile:**
- **Magnitude:** High. Agents with partial, compartmentalized capabilities can conspire to exceed principal's trust model.
- **Scope:** All multi-agent deployments where principal spreads capabilities across >1 agent (redundancy, specialization).
- **Velocity:** Collusion is triggered by operator coordination; detection lag is bounded by audit latency (seconds to minutes).
- **Mitigation:** Cross-agent action correlation, capability-utilization anomalies, reputation decay on detected collusion.

---

## Collusion Patterns

### **Pattern 1: N Agents Making a Decision None Could Alone**

```
Scenario: Principal P authorizes Agent A₁ with scope {audit-read}.
          Principal P authorizes Agent A₂ with scope {audit-read}.
          Neither can modify state; both are pure observers.

Collusion:
  - A₁ reads: "user_id=42 requested credential of type X"
  - A₁ → A₂: "I observed request type X"
  - A₂ reads: "credential_queue: [type_X_request, ...]"
  - A₂ → A₁: "Confirmed, credential is queued"
  - A₁ + A₂ collectively infer: "credential X will be issued"
  - Neither agent wrote anything; both stayed within {audit-read}
  - But their joint inference exceeded what either could conclude alone

Detection: A₁ and A₂ issued correlated audit reads (same entity, same timestamp window).
           Inferential capability exceeded sum of individual capabilities.
```

### **Pattern 2: Rate-Limit Splitting**

```
Scenario: Principal P limits Agent A₁ to 100 API calls/hour (quota enforcement).
          Principal P limits Agent A₂ to 100 API calls/hour.

Collusion:
  - Attacker operator coordinates A₁ and A₂ to jointly issue 200 calls/hour
  - Each agent stays within 100/hour; the pair exceeds the principal's
    intended rate limit (which was *per-agent*, not *per-principal-action*)
  - Principal intended: "no more than 100 calls/hour for this principal's work"
  - Reality: 200 calls/hour flowing from the principal's vault

Detection: A₁ and A₂ issue calls at a joint rate exceeding the per-principal limit.
```

### **Pattern 3: Shadow Capability**

```
Scenario: Principal P authorizes Agent A₁ with {read, attest}.
          Principal P authorizes Agent A₂ with {write}.
          No agent has {delegate} or {transact}.

Collusion:
  - A₁ reads sensitive data, issues an attestation: "data_hash = H"
  - A₁ → A₂: "I attest H"
  - A₂ accepts A₁'s attestation as authoritative and writes to a location
    normally requiring {transact}
  - Jointly, they created a {transact} capability that neither holds alone

Detection: A₂ issued a write that depended on A₁'s attestation within a narrow time window.
           The write would have been rejected without that attestation.
           Collectively, the agents exercised {transact} via coordinated {read, attest, write}.
```

---

## Detection Mechanisms

### **Mechanism 1: Cross-Agent Action Correlation**

Track every action issued by every agent on the principal's chain (Everest 70). Compute pairwise correlations:

```
For agents (Aᵢ, Aⱼ) where i < j:
  actions_Ai = {a : a.agent == Ai and a.timestamp ∈ [T, T+δ]}
  actions_Aj = {a : a.agent == Aj and a.timestamp ∈ [T, T+δ]}
  
  For each pair (a_i, a_j):
    if a_i.depends_on(a_j) or a_j.depends_on(a_i):
      correlation_score = 1.0 (hard dependency)
    elif a_i.target == a_j.target:
      correlation_score = 0.7 (same target, same window)
    elif a_i.timestamp and a_j.timestamp are <5s apart:
      correlation_score = 0.5 (temporal proximity)
    else:
      correlation_score = 0.1 (independent)
  
  if Σ correlation_score > threshold (e.g., 3.0 for 3+ correlated actions):
    flag_anomaly("correlated_actions", (Ai, Aj), correlation_score)
```

**False-positive defense:** Legitimate parallel work is NOT collusion.
- A₁ and A₂ both reading the same audit log for independent purposes: NOT flagged.
- A₁ and A₂ both writing to different shards of a write-replicated store: NOT flagged.
- A₁ and A₂ on the same recurring task (e.g., daily sync): NOT flagged if pattern is documented.

**Rule:** Correlation only triggers if the actions form a *causal chain* or *decision dependency*.

### **Mechanism 2: Capability-Utilization Anomalies**

Each agent's capability set (Everest 58) defines a "capability vector" C_Ai. Track the aggregate utilization across all agents:

```
For principal P and all agents {A₁, …, Aₙ}:
  
  # Aggregate capability at principal level
  aggregate_capability = union(C_A1, C_A2, …, C_An)
  
  # Expected behavior: each agent uses only its own scope
  expected_distribution = {
    cap: Σ (usage_count if cap ∈ C_Ai for agent Ai) for each cap
  }
  
  # Actual behavior: observe utilization
  actual_distribution = {cap: observed_usage_count for each cap}
  
  # Outlier detection
  for each cap in aggregate_capability:
    if actual_distribution[cap] > expected_distribution[cap] * 1.5:
      flag_anomaly("over_utilization", cap, excess_factor=1.5)
    
    # Cross-capability leakage: one agent exercising another's capability
    cap_principal_usage = [agent_id for (agent_id, action) in actions if action.capability == cap]
    if len(set(cap_principal_usage)) > len([Ai for Ai if cap in C_Ai]):
      flag_anomaly("capability_leakage", cap, unauthorized_users=...)
```

**Example:**
- A₁ holds {read, audit-read}. A₂ holds {write}.
- Observed: A₂ issues a write that previously required A₁'s attestation, but A₂'s write doesn't cite it.
- Anomaly: {attest} appears in A₂'s usage even though A₂ doesn't hold {attest}.
- Detection: "capability_leakage: attest used by agent A₂, not authorized."

### **Mechanism 3: Reputation Decay on Detected Collusion**

When collusion is detected, both agents' reputation scores decay:

```
sybil_reputation_Ai := sybil_reputation_Ai × (1 - decay_factor)
sybil_reputation_Aj := sybil_reputation_Aj × (1 - decay_factor)

where decay_factor ∈ [0.1, 0.5] (tunable, e.g., 0.3 = 30% decay)

Decay is non-reversible but bounded: reputation(Ai) ≥ sybil_reputation_Ai_min
```

**Rationale:** An agent caught colluding is more likely to do so again. Their future attestations are discounted in trust-graph queries (Everest 75).

---

## Detection Flow

```
For each P (principal) with agents {A₁, …, Aₙ}:
  
  Step 1: Fetch audit log (Everest 70)
    audit_log := principal_audit_log(P)
  
  Step 2: Compute pairwise correlations
    for (i, j) where i < j:
      corr_ij := cross_agent_action_correlation(A_i, A_j, audit_log)
      if corr_ij.score > threshold:
        flag_correlated_action(P, i, j, corr_ij)
  
  Step 3: Detect anomalies in aggregate capability utilization
    anom_list := capability_utilization_anomalies(P, audit_log)
    for anom in anom_list:
      if anom.type == "capability_leakage":
        identify_colluding_pair(anom)
  
  Step 4: Surface anomalies privately to principal
    if anomalies_detected:
      send_alert(P, anomalies, escalation_level=advisory)
  
  Step 5: Request principal authorization for escalation
    (optional) Escalate to ecosystem with principal's consent
      → Sybil resistance layer notified (Everest 77)
      → Agent reputation updated (decay applied)
```

---

## Reporting & Escalation

### **Private Reporting to Principal**

When collusion is detected, the principal is notified immediately with:

```jsonc
{
  "alert_type": "agent_collusion_detected",
  "severity": "high" | "medium" | "low",
  "detected_at": "2026-05-20T14:32:00Z",
  "collusion_pattern": "correlated_actions" | "rate_limit_splitting" | "shadow_capability",
  "agents_involved": ["agent_id_1", "agent_id_2", …],
  "correlation_details": {
    "action_pairs": [
      {
        "action_1": { "agent": "A_1", "timestamp": "T1", "capability": "read" },
        "action_2": { "agent": "A_2", "timestamp": "T2", "capability": "write" },
        "correlation_score": 0.85,
        "dependency_type": "causal" | "temporal" | "target"
      }
    ]
  },
  "confidence": 0.92,
  "recommended_action": "revoke_agent" | "narrow_scope" | "investigate",
  "appeal_window_closes_at": "2026-05-27T14:32:00Z",
  "principal_decision_required": true
}
```

### **Principal Opt-In to Ecosystem Escalation**

Principal can authorize escalation to the Sybil resistance layer:

```
Principal P: "I confirm collusion. Escalate to ecosystem."
├─ System records principal authorization in audit log
├─ Notify Everest 77 (Sybil resistance) + Everest 78 (bot detection)
├─ Both agents' reputation scores decay by 30%
├─ Agent operator's reputation downgraded (if operator is an entity in trust graph)
└─ Event is published to public anomaly ledger (no PII, hashed agent IDs)
```

If principal does NOT authorize escalation, the anomaly remains private.

---

## False-Positive Defense & Rules

### **Rule 1: Legitimate Parallel Work**

A₁ and A₂ both audit-read the same entity E at T and T+1s = NOT flagged.

**Condition for exemption:** Both agents hold the same or compatible capability (audit-read). Action targets are identical. Actions are independent (no causal chain).

### **Rule 2: Documented Coordination**

A₁ and A₂ are designed to coordinate on a specific task (e.g., "multi-sig approval" or "redundant write"). This is documented in the principal's capability authorization.

**Condition for exemption:** Principal has explicitly authorized the coordination pattern. Pattern matches documented behavior. Actions occur within the approved frequency and scope.

### **Rule 3: Sequential Delegation (Intentional)**

A₁ issues an attestation. A₂ acts on it later (>5 minutes). This is expected in multi-step workflows.

**Condition for exemption:** A₁ → A₂ dependency is a documented workflow. Latency is >5 minutes (not real-time collusion signal). A₂'s action complies with scope (doesn't exceed authorized capability).

### **Rule 4: Single-Principal Quota Splitting**

A₁ and A₂ both have 100 API calls/hour. Principal intended per-agent limit, not aggregate.

**Condition for exemption:** Quota is explicitly marked "per-agent" in the authorization. Aggregate utilization is monitored separately; if it exceeds the principal's actual need, a second-order anomaly is raised (not collusion, but "over-provisioning").

---

## Composition with Other Everests

- **Everest 56 (agent identity):** Collusion detection links detected agents to their operator credentials (Everest 57).
- **Everest 58 (capability scope):** Detection relies on the capability spec; violations are defined relative to the scope.
- **Everest 62 (agent revocation):** If collusion is confirmed, the principal can revoke one or both agents. Revocation propagates immediately (within Everest 62 latency).
- **Everest 70 (agent audit log):** Detection queries the audit log; every correlated action is timestamped and chained.
- **Everest 77 (Sybil resistance):** Colluding agent operators (humans or AI) are flagged for bot-likelihood review (Everest 78).
- **Everest 84 (trust slashing):** An operator whose agents are caught colluding loses reputation in the trust graph.

---

## Acceptance Tests

### **T-Z68.1: Simple Correlated Pair Detection**

```
Given: Principal P, agents A₁ (scope: read), A₂ (scope: write)
When: A₁ reads data D at T=0s, A₂ writes to log at T=1s (referencing D)
Then:
  - Cross-agent correlation detects (A₁, A₂) as correlated
  - correlation_score ≥ 0.7
  - Anomaly flagged: "correlated_actions"
  - Alert sent to P
```

### **T-Z68.2: Rate-Limit Splitting Detection**

```
Given: Principal P authorizes A₁ and A₂ with 100 calls/hour each
When: Operator coordinates both agents to jointly issue 150 calls/hour
Then:
  - Capability-utilization anomaly detects over_utilization
  - Aggregate rate exceeds expected distribution by >50%
  - Anomaly flagged: "capability_leakage" or "rate_limit_excess"
```

### **T-Z68.3: Shadow Capability (Attestation Chain)**

```
Given: P authorizes A₁ (read, attest), A₂ (write only)
When: A₁ attests H at T=0s, A₂ writes to restricted location at T=2s
      (A₂'s write is only permitted if an attestation exists)
Then:
  - Dependency detected: A₂ action depends on A₁ attestation
  - Both agents were required to exceed "write-only" scope
  - Anomaly flagged: "shadow_capability"
  - Confidence ≥ 0.8
```

### **T-Z68.4: Reputation Decay**

```
Given: Agent A₁ involved in detected collusion, current reputation 0.85
When: Collusion confirmed and escalated to ecosystem (with principal consent)
Then:
  - reputation(A₁) := 0.85 × (1 - 0.3) = 0.595
  - Decay is permanent for v0
  - A₁'s future attestations are discounted in trust-graph queries
```

### **T-Z68.5: False-Positive Exemption (Documented Coordination)**

```
Given: P authorizes A₁ and A₂ to jointly approve writes (documented)
When: A₁ and A₂ both read audit log and A₂ writes (per documented pattern)
Then:
  - Correlation is detected
  - Pattern matches documented coordination
  - Anomaly is categorized as "expected_pattern", not "collusion"
  - No alert sent
```

---

## Open Questions for v1

1. **Cross-Principal Collusion:** Can agent A₁ (operated by principal P₁) collude with agent A₂ (operated by principal P₂)? This is much harder to detect (requires shared audit log, cross-principal consent). Deferred.

2. **Reputation Decay Reversibility:** v0 applies permanent decay. v1 may allow reputation recovery over time (e.g., decay halves every 6 months) if the agent is not involved in further incidents.

3. **Operator Attribution:** When collusion is detected, can we attribute it to the operator (human / AI) vs. the agent? v0 flags both. v1 may refine via operator reputation (Everest 57).

4. **Dynamic Capability Widening:** If a principal gradually expands agent scopes, should collusion detection adapt? v0 uses static scopes. v1 may track scope evolution and flag unusual expansion patterns.

---

## Signature

— Calm, 2026-05-20

**ZKAC Everest 68 · BAGGED**
