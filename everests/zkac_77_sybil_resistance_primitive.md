# ZKAC Everest 77 — Sybil Resistance Primitive

**Phase XXII | Zero-Knowledge Attested Credentials | Critical Infrastructure**

**Prerequisite:** Everest 71 (trust graph data structure)

**Acceptance:** A documented anti-Sybil mechanism — proof-of-personhood, social-graph attestation, or hybrid.

**Effort:** XL | **Status:** v0 | **Author:** Calm, 2026-05-20

---

## Overview

The Sybil problem at scale: AI-generated fake principals and human attackers create synthetic identities (Sybils) to inflate trust scores, manipulate voting, dilute reputation, and launch targeted collusion attacks on the ZKAC ecosystem. Without Sybil resistance, the trust graph becomes a target for reputation laundering, where an attacker creates N fake principals, accumulates false endorsements among them, and injects the resulting "trust capital" into queries affecting honest principals.

**Risk Profile:**
- **Magnitude:** High. A single attacker with moderate computational resources can generate 1000s of realistic-looking principals.
- **Scope:** Trust transitivity (Everest 72) becomes exploitable if Sybil clusters masquerade as diverse issuers.
- **Velocity:** Sybil clusters can be deployed in hours; detection lag is measured in minutes to days.
- **Mitigation Strategy:** Three-layer defense: proof-of-personhood (unforgeable identity binding), social-graph vouching (decentralized verification), and hybrid detection (BrightID-style fusion).

**v0 Chosen Mechanism: Hybrid + Inclusive Non-Biometric Path**

A principal is Sybil-resistance-verified via either:
1. **Biometric attestation** (Worldcoin-style): government ID, facial biometric + liveness proof. Unforgeable; privacy concerns; hardware monopoly risk.
2. **Social-graph vouching** (≥N existing principals vouch). Organic; bootstrap problem; gaming risk.
3. **Hybrid (BrightID-style):** biometric + social, with the explicit design principle that **biometric is OPTIONAL, not required**. A principal can earn full Sybil-resistance verification via social-graph vouching alone (per principal-protective inclusive design).

All three paths feed into a shared Sybil-likelihood scoring system. Honest principals accumulate high Sybil-likelihood on their credential; fake ones leak the signature patterns enumerated below.

---

## Problem Statement & Threat Model

### **Sybil Attacks in ZKAC**

An attacker controls a set of principals {P₁, P₂, …, Pₙ} created within a time window T (often <1 hour). Goals:

1. **Trust inflation:** Pᵢ issues trust edges to Pⱼ with high weight (0.8+). The attacker then uses one fake principal (say, P₁) in a query to a verifier, claiming "I am trusted by P₂, P₃, …, Pₙ." Transitivity (Everest 72) inflates P₁'s effective trust score.

2. **Reputation laundering:** The attacker creates a fake "issuer" P_issuer, issues fake credentials from it, then establishes mutual-trust edges with P₁, P₂, … within the attack cluster. Later, when honest principals query "is P_issuer trusted?", the Sybil cluster skews the answer.

3. **Voting dilution:** In credential-issuance quorum systems (Everest 11 governance), Sybils vote en masse to approve fraudulent new issuers or revoke honest ones.

4. **Coordinated attestation collapse:** Sybils coordinate to all vouch for one attacker-controlled principal, creating a fake high-weight path P_honest → P_sybil₁ → … → P_attacker.

### **Attack Signatures (Detectable Patterns)**

1. **Temporal clustering:** Many edges issued by the same creator within <1 hour.
2. **Uniform weight distribution:** All edges within a suspected cluster have identical or near-identical weights (lack natural variance).
3. **Isolation:** Zero edges from the cluster to the honest graph (no bridging to real principals).
4. **Mutual all-trust:** Each fake principal trusts all others in the cluster (complete clique).
5. **Accelerated reputation growth:** A principal accumulates hundreds of trust edges in <1 day (vs. honest principal, <10 edges/day).
6. **Mirrored attestations:** Two principals issue identical trust edges to the same target, at the same timestamp (unlikely by chance).

---

## Three Candidate Mechanisms

### **Candidate 1: Proof-of-Personhood (PoP) — Biometric Attestation**

**Model:** Each principal must prove they are a unique human by submitting a government-issued ID + liveness biometric (facial recognition + challenge-response) to a trusted attestor (Worldcoin, Teleport, or similar).

**Flow:**
```
Principal P
├─ Submits government ID (passport, driver's license, national ID)
├─ Liveness check: facial biometric + random challenges ("blink", "smile")
├─ Attestor issues PoP_BIOMETRIC credential (a ZKAC, Everest 5)
├─ P's trust graph is tagged: [biometric_verified: true, PoP_issuedAt: ts]
└─ Verifier queries: "Is P biometric-verified?" → true/false
```

**Proofs:**
- **Unforgeable:** Facial recognition + government ID are cryptographically bound; attacker cannot forge thousands of unique faces at scale.
- **Unique identity:** One person = one credential (revocation on compromise).
- **Zk-Compatible:** PoP credential can be presented as a ZK proof ("I am biometric-verified") without revealing identity.

**Cons:**
- **Privacy:** Centralized attestor learns the principal's identity and biometric.
- **Hardware monopoly:** Liveness probes require dedicated devices or apps (Worldcoin orbs); excludes offline or low-tech regions.
- **Exclusion risk:** 10%+ of global population lacks government ID or cannot access hardware.
- **Regulatory:** Biometric collection is heavily regulated (GDPR Article 9, state laws). Multi-jurisdiction compliance is expensive.
- **Revocation cascade:** If an attestor is compromised, all PoP credentials it issued become suspect.

**Adoption:** High trust; low accessibility.

---

### **Candidate 2: Social-Graph Attestation — Vouching from Existing Principals**

**Model:** A principal P becomes Sybil-resistance-verified if ≥N existing Sybil-resistance-verified principals vouch for them.

**Flow:**
```
Principal P (new)
├─ Requests vouch from existing principals Q₁, Q₂, …, Qₙ
│  (Q₁, …, Qₙ are already Sybil-resistance-verified)
├─ Qᵢ issues a vouch credential: "I attest that P is a unique human I know"
├─ P collects N vouch credentials
├─ Submits to verifier: "I have N vouches from Sybil-verified principals"
├─ Verifier checks: all Qᵢ are still verified, vouches are recent (<30 days), no revocations
└─ If verified: P earns Sybil-resistance-verified tag
```

**Proofs:**
- **Organic:** No centralized infrastructure. Uses existing social links (friends, colleagues, family).
- **Inclusive:** Works offline, in any region; no special hardware.
- **Decentralized:** Verification happens at the verifier side; no single point of failure.
- **Sybil-resistant by design:** To create N fake principals, attacker must first have N Sybil-verified sponsors—creating a recursive constraint that limits attack scale.

**Cons:**
- **Bootstrap problem:** How do the first principals become verified? Requires external bootstrap (government ID, reputation import from legacy systems, or trusted issuer seed).
- **Vouching gaming:** Attacker can bribe or compromise ≥N existing principals to vouch falsely.
- **Collusion:** An attacker with a few compromised accounts can approve many Sybils if N is too small. E.g., if N=2, two compromised accounts unlock unlimited Sybil creation.
- **Social graph brittleness:** Removing one honest principal from the graph can strand their vouchers (if they can only reach N-1 sponsors).

**Adoption:** Medium-high; requires community trust.

---

### **Candidate 3: Hybrid (BrightID-Style) — Biometric + Social**

**Model:** A principal is Sybil-resistance-verified if they provide either:
- **Path A:** Biometric PoP from a trusted attestor, OR
- **Path B:** N vouches from existing Sybil-verified principals, OR
- **Path A+B:** Biometric + social (strongest proof; reduces N for purely social path).

**Flow (Hybrid Decision Tree):**
```
Principal P requests Sybil-resistance verification
├─ Path A: PoP Biometric?
│  └─ YES → Issue full-strength Sybil_verified credential (PoP_tier: biometric)
├─ Path B: ≥N Social Vouches?
│  └─ YES → Issue Sybil_verified credential (PoP_tier: social, vouch_count: N)
└─ Path A+B: Both biometric + ≥(N-1) vouches?
   └─ YES → Issue Sybil_verified credential (PoP_tier: hybrid, hybrid_confidence: 0.95+)
```

**Score Aggregation (Confidence Model):**
```
sybil_likelihood_score = 1 - [
  (biometric_confidence × w_bio) +
  (social_confidence × w_social) +
  (behavioral_confidence × w_behavior)
]
where w_bio + w_social + w_behavior = 1.0
and each confidence ∈ [0, 1]
```

**Proofs:**
- **Defense in depth:** Two failure modes (biometric compromise + social vouching compromise) must occur simultaneously for a Sybil to be created.
- **Inclusive:** Social path requires no hardware; biometric path requires infrastructure but is optional.
- **Flexible:** Adopters can tune N based on risk tolerance. High-security contexts use N=5+ or mandate biometric; low-security use N=2+social.

**Cons:**
- **Complexity:** Two verification flows. Verifiers must support both pathways, increasing implementation surface.
- **Policy divergence:** Different communities may disagree on N (social quorum size), credential lifetime, or biometric acceptance.
- **Leakage risk:** A principal's choice of path (biometric vs. social) may leak information about their privacy preferences or access to infrastructure.

**Adoption:** High; balances privacy, accessibility, and security.

---

## v0 Chosen Mechanism: Hybrid + Inclusive Non-Biometric Path

**Decision:** Hybrid model with explicit non-biometric fallback. Rationale: Aligns with principal-protective design (ZKAC constraint 1). Biometric is an *option*, not a *requirement*, preserving accessibility for communities without ID infrastructure.

**Parameters (v0 baseline):**
- **Social vouch threshold (N):** 3 (default). High-security verifiers can enforce N=5.
- **Vouch freshness window:** 30 days. Vouches older than 30 days are discounted in confidence scoring (can be overridden by verifier).
- **Biometric tier boost:** If a principal provides biometric PoP, they can satisfy social path with N-1 vouches (e.g., N=2 instead of 3).
- **Credential lifetime:** Sybil_verified credentials expire after 1 year. Renewal requires re-attestation (prevents stale identities from accumulating in the graph).

**Credential Schema:**

```jsonc
{
  "kind": "sybil_resistance_verified.v0",
  "subject": "did:calm:principal-uuid:key-hash",
  
  // Verification method chosen
  "verificationMethod": "biometric" | "social" | "hybrid",
  
  // Biometric path (optional)
  "biometric": {
    "attestorDID": "did:calm:worldcoin:issuer",
    "attestorReputation": 0.98,                  // Everest 23 issuer rep
    "biometricType": "facial_liveness",
    "proofIssuedAt": "2026-05-20T10:00:00Z",
    "imageHash": "sha256:abc...def",             // privacy-preserving hash
    "challenge": "base64:xyz123"                 // liveness challenge seed
  },
  
  // Social path (optional)
  "social": {
    "vouchCount": 3,
    "requiredThreshold": 3,
    "vouchers": [
      {
        "voucherDID": "did:calm:principal-uuid-1:key-hash",
        "vouchCredentialHash": "sha256:vouch-cred-hash-1",
        "vouchIssuedAt": "2026-05-19T14:20:00Z",
        "voucherReputation": 0.82,
        "voucherSybilLikelihood": 0.05           // recursive check
      },
      // ... 2 more vouchers
    ],
    "socialnessScore": 0.88                      // clustering coeff + diversity
  },
  
  // Composite confidence
  "sybilLikelihoodScore": 0.02,                  // 1 - composite confidence
  "confidenceBreakdown": {
    "biometric": 0.95,
    "social": 0.85,
    "behavioral": 0.92
  },
  
  // Sybil detection flags (advisory, non-blocking)
  "riskFlags": [
    // filled by Everest 78
  ],
  
  // Metadata
  "issuedAt": "2026-05-20T12:00:00Z",
  "expiresAt": "2027-05-20T00:00:00Z",
  "issuer": "did:calm:zkac:issuer",
  "signature": "sig:ed25519:base64-encoded"
}
```

---

## Detection of Sybil Clusters

Sybil detection operates at the trust-graph layer (Everest 71). A graph analyzer computes four signals:

### **Signal 1: Temporal Clustering (Edge Velocity)**

```
For each principal P:
  edges_per_hour = count(edges issued by P in the last 1 hour)
  
  if edges_per_hour > threshold (e.g., 10):
    flag_anomaly("high_edge_velocity", P, edges_per_hour)
```

Honest principal: ~0.1–1 edge/hour (natural growth).
Attacker setting up Sybil cluster: 10–100 edges/hour.

**Acceptance threshold:** >5 edges/hour triggers advisory flag.

### **Signal 2: Graph Clustering Coefficient (Isolation Detection)**

```
For principal P:
  neighbors = {Q : there exists edge P → Q or Q → P in trust graph}
  
  // Bridges: edges from P's neighbors to honest principals
  bridges_to_honest_graph = |{edge : Q ∈ neighbors and Q → R where R is "established"}|
  
  if bridges_to_honest_graph == 0:
    flag_anomaly("isolated_cluster", P, cluster_size=|neighbors|)
```

A newly-created principal P should have ≥1 edge to an established principal (bootstrap via social vouching). Complete isolation is suspicious.

### **Signal 3: Weight Uniformity (Entropy Check)**

```
For a suspected cluster C = {P₁, …, Pₙ}:
  edges_in_cluster = {(Pᵢ → Pⱼ) : i ≠ j}
  weights = [edge.weight for edge in edges_in_cluster]
  
  entropy = -Σ p(w) log(p(w)) for weight distribution
  
  if entropy < threshold (e.g., 0.3):
    flag_anomaly("weight_uniformity", C, entropy)
```

Honest graph: weights are diverse (0.3–0.95 range, natural variance). Attacker cluster: all weights = 0.9 (or other constant).

### **Signal 4: Mirrored Attestations (Timing Sync)**

```
For all pairs (P, Q) where both issue trust edges at time t:
  if |edge_P.timestamp - edge_Q.timestamp| < epsilon (e.g., 1 second)
    and edge_P.target == edge_Q.target
    and |P - Q| is small (both are "new")
    then flag_anomaly("mirrored_attestation", (P, Q), sync_delta)
```

Honest principals naturally vary in timing. Coordinated attacks emit synchronized edges.

### **Clustering Algorithm (Suspect Identification)**

```python
def detect_sybil_clusters(trust_graph: TrustGraph, anomaly_flags: List[Flag]) -> List[SybilCluster]:
  """
  Returns list of suspected Sybil clusters with confidence scores.
  """
  # Step 1: Seed clusters from anomaly flags
  suspicious_principals = {p for flag in anomaly_flags if flag.type in ["high_edge_velocity", "weight_uniformity"]}
  
  # Step 2: BFS to identify connected components in the subgraph induced by suspicious principals
  clusters = []
  visited = set()
  
  for seed in suspicious_principals:
    if seed in visited:
      continue
    
    cluster = bfs(graph=trust_graph, start=seed, restrict_to=suspicious_principals)
    visited.update(cluster)
    
    # Step 3: Compute cluster metrics
    cluster_metrics = {
      "size": len(cluster),
      "internal_edges": count_edges_within(cluster),
      "external_edges": count_edges_to_honest_graph(cluster),
      "isolation_score": external_edges / (internal_edges + external_edges + 1e-6),
      "temporal_window": (max(e.issuedAt for e in cluster.edges) - min(e.issuedAt for e in cluster.edges)).seconds,
      "avg_weight": mean([e.weight for e in cluster.edges])
    }
    
    # Step 4: Compute likelihood (fusion model, Everest 78 interlock)
    sybil_likelihood = fusion_model(
      temporal=cluster_metrics["temporal_window"] < 3600,  # <1 hour
      isolation=cluster_metrics["isolation_score"] < 0.1,  # <10% external edges
      weight_uniformity=entropy(cluster_metrics["avg_weight"]) < 0.3,
      velocity_anomaly=len(suspicious_principals) > 5
    )
    
    clusters.append(SybilCluster(
      members=cluster,
      metrics=cluster_metrics,
      sybil_likelihood=sybil_likelihood
    ))
  
  return clusters
```

---

## Bot-Likelihood Flag (Everest 78 Interlock)

Every credential issued in the ZKAC ecosystem carries an optional `bot_likelihood` field (advisory, non-blocking). This signals to verifiers and humans: "How confident are we that the principal issuing this credential is human vs. automated?"

**Computed by Everest 78, integrated into Everest 77 Sybil detection:**

```jsonc
{
  "credential": { /* ... */ },
  "bot_likelihood": {
    "score": 0.15,                             // [0, 1], 1 = definitely bot
    "factors": {
      "is_sybil_member": 0.8,                  // from Everest 77 cluster detection
      "issuance_frequency": 0.05,              // number of credentials/hour
      "linguistic_markers": 0.10,              // NLP analysis of any text in credential
      "temporal_regularity": 0.20,             // clockwork timing patterns
      "interaction_diversity": 0.02            // does principal interact w/ diverse targets?
    },
    "reasoning": "Member of suspected Sybil cluster with >0.7 confidence. Linguistic markers neutral. Not flagged.",
    "appeal_available": true,
    "appeal_url": "https://zkac.calm/appeals/bot-flag-UUID"
  }
}
```

**Non-blocking semantics:** A credential with `bot_likelihood: 0.8` is *still valid*. Verifiers can choose to:
1. Accept it unconditionally (trust the issuer).
2. Require additional Sybil-resistance verification (biometric).
3. Discount it in trust-graph queries (reduce weight by a factor).
4. Reject it outright (high-security verifiers).

The flag is *advisory*: it informs, but does not automatically block.

---

## Appeal Protocol

A principal flagged as part of a Sybil cluster can appeal. The appeal is a formal challenge to the Everest 77 detection algorithm.

**Appeal Flow:**

```
Principal P: "I was flagged in cluster C. I am human. Appeal."
├─ Submits appeal_request to ZKAC appeal service
│  └─ Evidence: (1) biometric PoP if available, OR
│      (2) social vouches from high-reputation principals, OR
│      (3) detailed narrative ("I am a researcher, created alt accounts for X reason")
├─ ZKAC service runs re-analysis:
│   └─ Reconsiders clustering; checks for false-positive signatures
├─ If appeal is credible: remove P from cluster, recompute bot_likelihood
└─ If appeal is rejected: P is notified with reasoning; can escalate to human review
```

**Appeal Acceptance Criteria (T-Z77.5):**

1. **Biometric proof:** If P submits valid PoP biometric, appeal is auto-approved (biometric overrides cluster detection).
2. **Social vouching:** If P submits N+2 new vouches from high-reputation principals (rep >0.85), appeal is reviewed by a quorum.
3. **Narrative review:** P's explanation is analyzed for legitimacy (human review, NLP for coherence). If coherent and verifiable (e.g., published research paper, social media history), appeal is considered.

**Latency:** Appeal resolution <7 days (goal), 30 days max.

---

## Composition with Other Everests

- **Everest 71 (trust graph):** Sybil detection operates on the trust-graph substrate. Clustered principals are flagged within the graph; queries can filter them.
- **Everest 72 (transitivity rules):** If a path P → Q involves a suspected Sybil Q, transitivity is suppressed (edge weight → 0, or maxDepth → 1).
- **Everest 75 (trust scoring):** Sybil_likelihood is factored into trust-score computation; paths through suspected Sybils are down-weighted.
- **Everest 76 (trust gaming defense):** Sybil detection is the primary defense against trust gaming; Everest 76 layers additional gaming defenses (e.g., rate-limiting, differential privacy in score aggregation).
- **Everest 78 (bot detection):** Complements Everest 77 by flagging principals likely to be AI-generated (not just fake humans, but LLM agents). Everest 77 + 78 together form a two-layer anti-Sybil system.
- **Everest 80 (trust expiration):** Sybil_verified credentials expire after 1 year; re-attestation is required (forces re-engagement with social or biometric pathways, detecting inactive Sybils).

---

## Acceptance Tests

### **T-Z77.1: Biometric Path (PoP Issuance & Query)**

```
Given: Principal P submits government ID + liveness biometric to Worldcoin
When: Worldcoin attestor verifies and issues PoP_BIOMETRIC credential
Then:
  - P's credential carries biometric_verified: true
  - Verifier query(is_sybil_resistant, P) returns true
  - sybil_likelihood_score ≤ 0.05 (high confidence)
  - Credential valid for 1 year
```

### **T-Z77.2: Social Path (Vouch Collection & Verification)**

```
Given: Principal P (new), vouchers Q₁, Q₂, Q₃ (all Sybil-verified)
When: P collects 3 vouch credentials from Q₁, Q₂, Q₃ and submits
Then:
  - Verifier checks: all Qᵢ Sybil-verified, vouches <30 days old, no revocations
  - P's credential carries verificationMethod: social, vouchCount: 3
  - sybil_likelihood_score = fusion(social_confidence=0.88, others) ≤ 0.15
```

### **T-Z77.3: Hybrid Path (Biometric + 2 Vouches)**

```
Given: Principal P with biometric PoP + 2 social vouches
When: P submits for Sybil verification (hybrid path)
Then:
  - verificationMethod: hybrid
  - sybil_likelihood_score ≤ 0.05 (biometric boost overrides lower social count)
  - confidenceBreakdown combines both signals
```

### **T-Z77.4: Sybil Cluster Detection (Synthetic Injection)**

```
Given: Trust graph G (honest), synthetic Sybil cluster S = {A, B, C, D, E}
       where all edges issued within 30 minutes, all weights = 0.9
When: Detector runs on G ∪ S
Then:
  - Detects ≥4 of {A, B, C, D, E} as suspicious
  - Assigns sybil_likelihood ≥ 0.75 to each member
  - Flags anomalies: temporal_clustering, weight_uniformity, isolation
  - Cluster {A, B, C, D, E} is tagged with metrics
```

### **T-Z77.5: Appeal & Reinstatement**

```
Given: Principal P falsely flagged as Sybil, submits appeal with biometric PoP
When: Appeal service verifies P's biometric
Then:
  - P is removed from cluster
  - sybil_likelihood_score recalculated (≤ 0.05)
  - bot_likelihood flag cleared
  - Resolution timestamp recorded in P's audit log
```

---

## Non-Biometric Design Principles

**Core principle: Biometric is optional, not required.**

A principal can achieve full Sybil-resistance verification via social-graph vouching alone. This preserves:
- **Accessibility:** Regions without ID infrastructure are not excluded.
- **Privacy:** A principal can remain pseudonymous (no government ID linkage) if they have sufficient social capital.
- **Autonomy:** Principal chooses their verification method; no forced biometric dependency.

**Trade-off articulation:**
- **Pure social path:** Requires N=3 vouches, credential lifetime 1 year (more frequent re-attestation). Sybil_likelihood = 0.10–0.15.
- **Biometric-only path:** No vouches needed, lifetime 1 year. Sybil_likelihood = 0.02–0.05.
- **Hybrid path:** Biometric + 2 vouches (vs. 3). Sybil_likelihood = 0.02–0.05, with redundancy.

Verifiers set their own acceptance thresholds. A conservative verifier might only accept biometric or hybrid. A community-first verifier might accept pure social (N=3) for cultural fit.

---

## Open Questions for v1

1. **Vouch Reputation Decay:** Should an old vouch (25 days) be weighted less than a fresh one (1 day) in the social-confidence calculation? v0 uses binary freshness (<30 days); v1 may introduce continuous decay.

2. **Appeal Quorum Composition:** Who reviews appeals? An internal quorum of high-reputation issuers (Everest 23)? A randomized jury from the principal ecosystem? v0 assumes human review by ZKAC operators; v1 formalizes composition.

3. **Cross-Biometric Providers:** If a principal is verified by Worldcoin, are they also accepted by a verifier that trusts only Teleport's PoP credentials? v0 treats all PoP attestors as equivalent (if they meet reputation threshold, Everest 23); v1 may tier them.

4. **AI-Principal Sybils (Emergent Risk):** Current v0 focuses on fake humans and lightweight automated attacks. As AI agents become principal actors in the ecosystem (Everest 56), how do we distinguish "legitimate bot agent (operated by a human)" from "Sybil bot (operated by attacker)"? Everest 78 (bot_likelihood flag) is a starting point; v1 may require explicit "agent operator" attestation.

5. **Reputation Portability After Sybil Appeal:** If P was flagged, appealed successfully, and reinstated, should their reputation history be wiped or preserved? v0 preserves history (for audit); v1 may offer "right to be forgotten" (after appeal approval).

---

## Signature

— Calm, 2026-05-20

**ZKAC Everest 77 · BAGGED**
