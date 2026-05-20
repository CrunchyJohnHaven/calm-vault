# ZKAC Everest 75 — Trust Scoring (Privacy-Preserving)

**Phase XXII | Zero-Knowledge Attested Credentials | Critical Infrastructure**

**Prerequisites:** Everest 71 (trust graph), Everest 74 (web-of-trust merging)

**Acceptance:** Privacy-preserving scoring algorithm: principal P can ask "how much should I trust I?" without revealing who I is.

**Effort:** L | **Status:** v0 | **Author:** Calm, 2026-05-20

---

## Overview

Trust scoring computes a cardinal weight S(P, I) ∈ [0, 1] that answers: "How much should P trust issuer I?" The score is derived from:

1. **Graph composition:** Multi-path weight aggregation from P's trust edges to I (Everest 71).
2. **Reputation integration:** I's public audit + slash history (Everest 23, E44).
3. **Distrust records:** Explicit revocations and negative attestations (Everest 16, E73).
4. **Privacy mechanism:** P queries the score without revealing their identity or the identity of I.

The algorithm is **not** a global consensus score. Each principal computes S(P, I) locally, reflecting P's subjective trust decision informed by public reputation + P's private graph. Verifiers request scores via privacy-preserving queries (Oblivious RAM or PIR); the query service returns S(P, I) without learning who queried or which entity was scored.

---

## Scoring Algorithm

### Input

```
P: DID of querying principal
I: DID of issuer being scored
G_P: P's cached trust-graph subgraph (edges P issued + gossip-received)
R_I: public reputation record for I (Everest 23: audit score, slash history)
D: distrust index (Everest 16: revocations, negative attestations)
params: {
  weight_decay: 0.15,        // per-hop decay factor (multiplicative)
  max_depth: 3,               // max transitivity hops
  reputation_weight: 0.3,     // fraction of score from public reputation
  graph_weight: 0.6,          // fraction from trust-graph paths
  distrust_penalty: 0.1       // fraction of score reserved for distrust
}
```

### Output

```
S(P, I): float ∈ [0, 1]  — confidence that P should trust I
components: {
  path_score: float        — aggregate of direct + transitive paths
  reputation_score: float  — public audit + issuer track record
  distrust_penalty: float  — negative adjustment from revocations
  final_score: float       — weighted composition
}
```

### Algorithm (Pseudocode)

```python
def trust_score(P: DID, I: DID, G_P: TrustGraph, R_I: Reputation,
                D: DistrustIndex, params: ScoringParams) -> TrustScore:
  """
  Compute S(P, I) with privacy-preserving query support.
  """
  
  # Phase 1: Graph-based component (weighted multi-path aggregation)
  paths = discover_paths(P, I, max_depth=params.max_depth, G_P=G_P)
  if not paths:
    path_score = 0.0
  else:
    # Collect composition weights from all paths, apply weight decay per depth
    path_weights = []
    for path in paths:
      comp_weight = 1.0
      for edge_idx, edge in enumerate(path.edges):
        comp_weight *= edge.weight
        # Apply decay penalty for longer paths
        depth_penalty = (1.0 - params.weight_decay) ** edge_idx
        comp_weight *= depth_penalty
      path_weights.append(comp_weight)
    
    # Multi-path aggregation: max of all paths (pessimistic for trust)
    # Alternative: Bayesian aggregation (see v1 open questions)
    path_score = max(path_weights) if path_weights else 0.0
  
  # Phase 2: Reputation-based component (Everest 23 integration)
  # R_I.audit_score ∈ [0, 1]: issuer's public audit result
  # R_I.slash_history: list of (slash_event, weight_reduction)
  reputation_score = R_I.audit_score
  for slash_event in R_I.slash_history:
    # Each slash reduces reputation; recent slashes have higher weight
    time_decay = exp(-slash_event.age_days / 365.0)  // 1-year half-life
    reputation_score *= (1.0 - 0.2 * time_decay)  // max 20% reduction per slash
  reputation_score = max(0.0, reputation_score)  // floor at 0
  
  # Phase 3: Distrust integration (Everest 16 interlock)
  distrust_penalty = 0.0
  if D.has_revocation(P, I):
    # P explicitly revoked trust in I
    distrust_penalty = 1.0  // total score override
  elif D.has_negative_attestation(P, I):
    # Peer community flagged I as untrustworthy (advisory)
    distrust_penalty = D.negative_attestation(P, I).weight
  
  # Phase 4: Composition (weighted synthesis)
  if distrust_penalty >= 0.5:
    return TrustScore(
      path_score=path_score,
      reputation_score=reputation_score,
      distrust_penalty=distrust_penalty,
      final_score=0.0,  // hard stop if strong distrust
      reasoning="explicit_distrust_revocation"
    )
  
  # Otherwise: weighted average of graph + reputation, reduced by distrust
  final_score = (
    params.graph_weight * path_score +
    params.reputation_weight * reputation_score
  ) * (1.0 - params.distrust_penalty * distrust_penalty)
  
  return TrustScore(
    path_score=path_score,
    reputation_score=reputation_score,
    distrust_penalty=distrust_penalty,
    final_score=final_score,
    reasoning="composite"
  )
```

### Key Design Choices

1. **Multi-path aggregation via max():** Pessimistic strategy. If ANY path to I has high trust, P can trust I. Alternative (Bayesian averaging) explored in v1.

2. **Weight decay per hop:** Multiplicative decay encourages direct trust over transitive chains. `depth_penalty = (1 - weight_decay)^hop` naturally depreciates longer paths.

3. **Reputation as public signal:** All principals see the same R_I. Trust-scoring personalizes by combining P's private graph with public reputation.

4. **Distrust as override:** If P explicitly revokes trust or peers flag I as adversarial, S(P, I) → 0. Distrust is conservative.

5. **Composition rule:** Linear weighted sum (graph + reputation) scaled by distrust penalty. Extensible to multiplicative composition (Bayesian) in v1.

---

## Privacy-Preserving Query Protocol

### Threat Model

**Adversary:** Honest-but-curious query service Q. Learns nothing from S(P, I) requests:
- The identity of P (querier)
- The identity of I (queried entity)
- Whether two requests come from the same principal
- Any subset of P's trust graph

### Protocol v0: Oblivious RAM (ORAM) Lookup

P sends an encrypted query to Q without revealing the target (I).

#### Setup Phase (One-time)

1. Q publishes an ORAM-encoded representation of the merged trust graph (Everest 74).
   - Each issuer I is assigned a random ORAM address: addr(I).
   - The ORAM also encodes reputation scores R_I and distrust records D.

2. P downloads a digest of the ORAM (e.g., Merkle tree root) to verify Q is not deviating.

#### Query Phase

```
P → Q: ("ORAM_ACCESS", encrypted_path=[a0, a1, ..., a_k], proof_of_inclusion)

where:
  encrypted_path: sequence of dummy + real ORAM accesses
  proof_of_inclusion: ZK proof that P is authorized to query (optional: optional gating on P holding a specific credential)

Q:
  1. Executes ORAM access sequence (dummies indistinguishable from real)
  2. Computes S(P, I) locally (using cached P's graph + R_I + D)
  3. Returns encrypted result to P

P:
  1. Decrypts result
  2. Verifies result matches his local computation (as sanity check)
```

**Privacy Guarantee:** Q observes only:
- ORAM access patterns (which reveal query count, not identity or target)
- Timing (bounded per SLA, randomized jitter)

**Complexity:** O(log^3 N) ORAM accesses for N entities (standard ORAM baseline).

### Protocol v1: Cryptographic PIR (Private Information Retrieval)

Alternative using polynomial-based PIR (Cumulus / FastPIR).

#### Setup

- Encode trust graph as a vector V ∈ F_p^N (field of size p), where V[i] = serialized edge to issuer i.
- Reputation scores and distrust records similarly vectorized.

#### Query

```
P:
  1. Generates a PIR query vector q corresponding to issuer I
     (e.g., q has a 1 at position addr(I), 0 elsewhere)
  2. Sends q (encrypted under Q's public key) to Q

Q:
  1. Computes inner product: result = <q, V> (mod p)
  2. Returns encrypted result

P:
  1. Decrypts result
  2. Extracts S(P, I) from the inner product
```

**Privacy Guarantee:** Q learns only the inner product result, nothing about q (PIR is 1-round, fully collusion-resistant).

**Complexity:** O(N) modular operations per query (linear but practical for N < 1M).

---

## Acceptance Tests

### T-Z75.1: Score Computation Correctness

```
Given: P → I (weight 0.9), I's reputation score 0.8
When: trust_score(P, I, path_weights=[0.9], rep=0.8)
Then:
  - path_score = 0.9 (single direct edge)
  - reputation_score = 0.8
  - distrust_penalty = 0.0
  - final_score ≈ 0.9 * 0.6 + 0.8 * 0.3 = 0.78 (using default params)
```

### T-Z75.2: Multi-Path Aggregation

```
Given: Two paths P → I:
       - Path A: P → X (0.9) → I (0.8) → score 0.72
       - Path B: P → Y (0.5) → I (0.7) → score 0.35
When: trust_score(P, I, paths=[A, B])
Then:
  - path_score = max(0.72, 0.35) = 0.72
  - Final score incorporates highest-confidence path
```

### T-Z75.3: Distrust Override

```
Given: path_score = 0.9, reputation = 0.8, explicit revocation P ⊣ I
When: trust_score(P, I) with distrust_penalty = 1.0
Then:
  - final_score = 0.0 (regardless of path or reputation)
  - reasoning = "explicit_distrust_revocation"
```

### T-Z75.4: Privacy-Preserving Query (No Leakage)

```
Given: ORAM-encoded trust graph Q, principals P1, P2 with different graphs
When: P1 queries S(P1, I1), P2 queries S(P2, I2)
Then:
  - Q observes only ORAM access patterns (indistinguishable)
  - Q cannot determine which principal queried or which entity was scored
  - P1 and P2 remain unlinkable across queries
```

### T-Z75.5: Reputation Integration with Slash History

```
Given: I with audit_score=0.9, one slash 30 days ago (weight 0.2)
When: trust_score(P, I) with R_I.slash_history=[event_30d]
Then:
  - reputation_score = 0.9 * (1 - 0.2 * exp(-30/365)) ≈ 0.84
  - Score reflects recent negative event but discounts old slashes
```

---

## Composition with Other Everests

**Everest 16 (distrust composition):** Distrust records (revocations, negative attestations) feed the distrust_penalty component.

**Everest 23 (issuer reputation):** Public audit scores R_I.audit_score + slash history R_I.slash_history directly integrate into reputation_score.

**Everest 44 (verifier reputation):** Analogous structure; verifiers also have public reputation that can be queried via S(P, V) for verifier V.

**Everest 71 (trust graph):** Path discovery and weight composition use Everest 71's multi-path aggregation and depth-based decay.

**Everest 72 (transitivity rules):** Weight decay parameters and max_depth constraints enforce Everest 72's transitivity bounds.

**Everest 73 (revocation propagation):** Distrust records reach query service within 5-min gossip latency; scoring reflects fresh revocations.

**Everest 74 (web-of-trust merging):** Merged graph G_P may include P's edges + trusted peers' edges; scoring traverses the union.

**Everest 76 (trust gaming defense):** Scoring resists Sybil voting by weighting reputation + graph equally; isolated/synthetic principals lack both.

---

## Privacy Mechanism Rationale

Why ORAM or PIR, not homomorphic encryption?

1. **ORAM (Everest 75 v0):** Hides access pattern via dummy accesses. Practical server-side cost O(log^3 N); P's computation O(1).
2. **PIR (v1 alternative):** Server does blind inner product; Q learns nothing. Linear server cost but collusion-resistant.
3. **Homomorphic:** Server computes S(P, I) directly over encrypted inputs. E2E cost O(N log^2 N) + relinearization (slower than ORAM for single queries).

**Choice:** ORAM for v0 (simpler to deploy, standard ORAM libraries). PIR for v1 (stronger privacy guarantees, higher throughput).

---

## Open Questions for v1

1. **Bayesian Multi-Path Aggregation:** Should we compute S(P, I) as a Bayesian belief (weighted average of all paths, not just max)? Trade-off: higher score (more trusting) vs. max() (conservative).

2. **Machine-Readable Personalized Policies:** Can verifiers express "for P, I only qualifies if path_score > 0.7 AND reputation > 0.75"? Currently hardcoded in params.

3. **Temporal Scoring:** Should scores decay over time if P hasn't interacted with I? Or explicitly renew trust edges periodically?

4. **Cross-Predicate Composition:** If P trusts I for academic creds but not financial, should S(P, I) be predicate-specific? Currently aggregates across all predicates.

5. **Score Distribution & Delegation:** Can P delegate score computation to a trusted advisor without revealing their trust graph? (Separate from Everest 79 delegation protocol.)

---

## Signature

— Calm, 2026-05-20

**ZKAC Everest 75 · BAGGED**
