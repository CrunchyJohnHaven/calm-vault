# ZKAC Everest 71 — Trust Graph Data Structure

**Phase XXII | Zero-Knowledge Attested Credentials | Critical Infrastructure**

**Prerequisite:** Everest 16 (issuer-to-issuer trust composition)

**Acceptance:** A documented graph schema for "principal P trusts issuer I under conditions C"

**Effort:** M | **Status:** v0 | **Author:** Calm, 2026-05-20

---

## Overview

The trust graph is the authoritative substrate for transitive trust in the ZKAC ecosystem. It answers:

1. **Does P trust I?** Privacy-preserving discovery of whether principal P has an explicit trust path to issuer I under specified conditions, without revealing the full graph.
2. **Under what conditions?** Scoped trust: P might trust issuer I for academic credentials (predicate `issuer.attestation.academic`) but not financial ones.
3. **How strongly?** Trust weight W ∈ [0, 1] — trust(P → I → J) = W(P → I) × W(I → J). Longer chains decay, discouraging reliance on distant intermediaries.
4. **Can I revoke it?** Trust assertions are append-only on the truster's chain; revocation creates a second edge with `kind: trust_revocation.v0`, propagating through gossip protocol within 5 minutes.

The trust graph is **not** a monolithic ledger. Each principal holds their own trust edges on their append-only chain (Sigsum-anchored). Subgraph caches are synced via gossip; the authoritative source is the union of all chain heads.

---

## Trust Assertion Schema (the Edge)

Each trust assertion is a cryptographically signed object, issued by the truster P and appended to P's chain.

```jsonc
{
  "kind": "trust_assertion.v0",
  
  // Identity
  "from": "did:calm:principal-uuid:key-hash",           // truster's DID
  "to": "did:calm:issuer-uuid:key-hash",                 // trusted party's DID
  
  // Scope of trust: the predicate defines the domain
  "predicate": "issuer.attestation",                     // fixed to issuer attestation class
  "predicateClass": "academic|financial|professional",  // optional refinement
  
  // Conditions: optional narrowing of the trust scope
  "conditions": {
    "credentialTypes": [
      "urn:zkac:credential:academic.degree",
      "urn:zkac:credential:academic.transcript"
    ],
    "credentialClasses": ["academic"],                   // Everest 7 issuer-class filtering
    "tier": "production",                                // issuer license tier (Everest 20)
    "issuerReputation": {
      "minScore": 0.75                                   // trust only if issuer's rep ≥ 0.75 (Everest 23)
    },
    "validFrom": "2026-05-20T00:00:00Z",
    "validUntil": "2027-05-20T00:00:00Z",
    "maxDepth": 2,                                       // max transitivity hops (Everest 72 override)
    "noTransitivity": false                              // if true, P→I only; no P→I→J
  },
  
  // Weight: [0, 1], multiplicative composition (Everest 72)
  "weight": 0.85,                                        // subjective degree of trust
  
  // Timestamps & provenance
  "issuedAt": "2026-05-20T15:43:12.234Z",
  "expiresAt": "2027-05-20T00:00:00Z",                  // trust expiration (Everest 80)
  "chainIndex": 47,                                      // monotonically increasing on P's chain
  "chainHead": "sha256:abc...def",                       // hash of previous edge on P's chain
  
  // Cryptographic proof
  "signature": "sig:ed25519:base64-encoded-signature",  // P's keypair signs the entire object
  "signingKey": "did:calm:principal-uuid:key-hash#key-1",
  
  // Optional: justify why P trusts I
  "justification": "I have verified this issuer's credentials and audit history",
  "auditEvidence": {
    "auditRound": "2026-Q2",                            // issuer audit period (Everest 19)
    "auditPass": true
  }
}
```

### Revocation Edge

When P decides to revoke trust in I, P appends a revocation edge:

```jsonc
{
  "kind": "trust_revocation.v0",
  "from": "did:calm:principal-uuid:key-hash",
  "to": "did:calm:issuer-uuid:key-hash",
  "predicate": "issuer.attestation",
  "revokes": "sha256:<hash of original trust_assertion edge>",
  "reason": "issuer_slashed|key_compromise|policy_change|no_longer_endorsed",
  "revokedAt": "2026-05-21T10:00:00Z",
  "chainIndex": 48,
  "chainHead": "sha256:abc...ghi",
  "signature": "sig:ed25519:base64-encoded-signature",
  "signingKey": "did:calm:principal-uuid:key-hash#key-1"
}
```

---

## Graph Operations

### 1. **Add Edge: P trusts I**

**Input:** Unsigned trust assertion (all fields except signature, chainIndex, chainHead).
**Process:**
  1. P verifies they own the `from` DID (key custody, Everest 27).
  2. P signs the assertion with their private key (Ed25519).
  3. P appends to their append-only chain (`$CALM_VAULT/chains/trust-edges.chain`).
  4. Chain index increments; new edge's `chainHead` references the prior edge.
  5. Within 100ms, the edge is broadcast to gossip peers.

**Invariants:**
  - Each edge is signed by `from`. Unsigned or mis-signed edges are rejected.
  - No edge can be inserted out of order or with gaps in chainIndex.
  - An edge with `validUntil` in the past is still queryable but semantically expired.

### 2. **Revoke Edge: P revokes trust in I**

**Input:** Hash of the prior trust assertion.
**Process:**
  1. P locates the edge with hash H in their chain.
  2. P creates a `trust_revocation.v0` edge referencing H.
  3. Appends to chain; distributed via gossip (latency target: <5 min global propagation, Everest 73).
  4. Verifiers stop accepting presentations from I on behalf of P within the latency window.

### 3. **Query: Does P trust I with weight ≥ W?**

**Signature:**
```python
def trust_query(p: DID, i: DID, predicate: str, weight_threshold: float = 0.0, max_depth: int = 3) -> QueryResult:
  """
  Returns:
    - found: bool — P trusts I under predicate with weight ≥ weight_threshold
    - paths: List[TrustPath] — all qualifying paths from P to I (depth ≤ max_depth)
    - composition_weight: float — product of all weights along shortest path
    - leakage: None (privacy-preserving: see Section 7)
  """
```

**Local Mode (P's wallet):**
  1. P's wallet loads its cached subgraph (intersection of trust edges P issued + received).
  2. BFS from P to I, avoiding revoked edges.
  3. Collect all paths of depth ≤ max_depth.
  4. Discard paths where intermediate issuer reputation < condition.minRepScore (if specified).
  5. Return true if any path has composition_weight ≥ weight_threshold.

**Distributed Mode (verification):**
  1. V requests "does P trust I?" from a ZK query service.
  2. Query is a set-membership proof: "P's chain contains a non-revoked trust edge to I" (Everest 75).
  3. Query service responds with true/false, never revealing the querier's identity or the full path.

### 4. **Path Discovery: What are all paths P → I?**

**Signature:**
```python
def discover_paths(p: DID, i: DID, max_depth: int = 3, weight_threshold: float = 0.0) -> List[TrustPath]:
  """
  Returns ordered list of trust paths, strongest (highest composition_weight) first.
  """
```

**Algorithm (bounded BFS):**
  1. Queue = [(p, weight=1.0, depth=0, path=[])]
  2. While queue is not empty:
     a. Pop (current, weight, depth, path)
     b. If current == i and weight ≥ weight_threshold: yield path
     c. If depth >= max_depth: skip
     d. For each edge (current → X) on current's chain:
        - If edge is revoked: skip
        - If edge.validUntil < now: skip
        - Push (X, weight × edge.weight, depth+1, path + [edge])
  3. Return sorted by composition_weight descending

**Composition Rule (Everest 72):**
  ```
  weight(P → I → J) = weight(P → I) × weight(I → J)
  ```
  Multiplicative, monotonically decreasing. Discourages reliance on chains longer than 2–3 hops. A path with max depth 3 has minimum composition weight of 0.5^3 = 0.125 (if all weights are 0.5). Per-predicate overrides in Everest 72.

---

## Trust Weight Composition

**Weight Algebra:**

- **Edge weight:** A subjective belief from the truster. P might assign weight 0.95 to a trusted state university's issuer (high confidence), 0.6 to a peer collective (less institutional), 0.3 to a self-attested claim.
- **Path weight:** Product of all edge weights along the path.
  - P → I: weight(P → I) = 0.8
  - I → J: weight(I → J) = 0.7
  - Composition: weight(P → J via I) = 0.8 × 0.7 = 0.56

**Transitivity Bounds (Everest 72 Interlock):**
  - Default max depth: 3 hops (P → I → J → K).
  - Predicates can override per condition (e.g., `maxDepth: 1` for financial credentials = no transitivity).
  - Flag `noTransitivity: true` disables transitive inference entirely for a given edge (e.g., personal attestations).
  - Query respects the strictest bound along any path.

**Cutoff & Decay:**
  - Queries specify `weight_threshold` (e.g., "only trust paths with composition weight ≥ 0.5").
  - Default: 0.0 (accept any valid path).

---

## Transitivity Bounds (Everest 72 Preview)

The trust graph enables transitive inference — if P trusts I and I trusts J, P implicitly trusts J — but only under strict limits.

**Normative Rules (Everest 72):**

1. **Default transitivity depth:** max_depth = 3 (P → I → J → K).
2. **Predicate-class overrides:** Academic credentials might allow depth 2, financial credentials depth 1.
3. **No-transitivity flag:** Some edges (e.g., personal attestations) set `noTransitivity: true`, blocking inference.
4. **Reputation-gating:** Intermediate issuers must meet reputation thresholds (Everest 23) to participate in transitive paths.
5. **Decay penalties:** Composition weight naturally decays; 0.9^3 ≈ 0.73. Verifiers can impose hard cutoffs (e.g., "reject paths with weight < 0.5").

Everest 72 formalizes these as normative rules; Everest 71 (this doc) provides the data structure to enforce them.

---

## Privacy-Preserving Querying (Everest 75 Interlock)

The trust graph is a **social graph**. Querying "does P trust I?" leaks information about P's trust decisions.

**Two operational modes:**

### **Local Mode**

P's wallet contains a cached subgraph (edges P issued + recent edges received via gossip). Queries are computed locally.

- **Privacy:** Perfect. No network traffic.
- **Freshness:** Bounded by cache-update latency (target: <5 min, via gossip).
- **Trade-off:** P's wallet must have bandwidth to sync a growing subgraph.

### **Distributed Mode**

P sends queries to a privacy-preserving query service (Everest 75 v0 uses ZK set-membership proofs).

- **Query:** "Is E ∈ S?" where S = P's set of trust edges and E = the edge "P trusts I."
- **Response:** true/false, without revealing:
  - Who queried (unlinkable across queries)
  - The identity of I
  - The full set S
- **Mechanism:** Accumulator (e.g., RSA or polynomial) or MPC (Everest 86+).

---

## Storage & Replication

### **Local Chains**

Each principal P maintains an append-only chain of trust edges in their vault:

```
$CALM_VAULT/chains/
├── trust-edges.chain        # edges issued by P
├── trust-edges.sig          # Sigsum anchor for the chain
└── trust-edges.index        # [chainIndex -> hash] map for fast lookup
```

**Format:** CBORX (CBOR-serialized, length-prefixed).

**Invariants:**
- Monotonically increasing chainIndex.
- Each edge signs the prior edge's hash (backward-linking).
- The chain head is anchored in Sigsum (Transparency Log, Everest 19 interlock).

### **Subgraph Caches**

Verifiers and query services maintain a local cache of the trust graph:

```
$QUERY_SERVICE/subgraph-cache/
├── did:calm:*.json          # per-principal edges
├── metadata.json            # {lastSync, leafHash, peerCount}
└── revocations.idx          # [revokedEdgeHash -> revocationEdge]
```

**Sync Protocol (Gossip):**
  1. Every 30 seconds, peers exchange cache digests (Merkle tree roots of their chains).
  2. If digests differ, peer streams missing edges via chunked CBORX.
  3. Receiver validates each edge (signature, chain continuity).
  4. Edge is added to cache; old edges retained (immutable).
  5. Revocations are indexed separately for fast negation queries.

**Latency:** <5 min for a new trust assertion or revocation to propagate to 90% of the network (assuming gossip fanout = 3, network size = 100s–1000s of verifiers).

### **Authoritative Source**

The truth is the **union of all chain heads**:

```
TrustGraph = ∪_p TrustChain(p).edges
           where TrustChain(p).edges = edges issued by P, filtered for revocations
```

No central registry. Each participant maintains a copy; consistency is eventual (bounded by gossip latency).

---

## Revocation Propagation Latency

**Target:** ≤ 5 minutes for 90% of verifiers to learn a revocation.

**Mechanism:**
  1. P appends revocation edge to their chain.
  2. Revocation is signed and broadcast immediately (same as trust assertion).
  3. Gossip peers receive within ~1 second.
  4. Peers index the revocation in `revocations.idx`.
  5. Verifiers re-validate cached edges against revocations on each trust query.

**Bounded Latency Guarantees:**
  - Synchronous gossip (fanout 3, rounds = log(network_size)) reaches all honest peers in O(log N) rounds = O(log N) × 30 sec = <10 min for N=1000.
  - Practical: Staggered re-syncs + explicit revocation broadcasts keep latency <5 min with high probability.

**Failure Scenario:** A malicious principal issues and then immediately revokes a trust edge to interfere with a querier's decision. Verifier must tolerate a race: if revocation arrives <1 sec after the edge, verifier uses edge; if >1 sec, verifier sees revocation and rejects the edge. Timing is truster's responsibility; Everest 73 formalizes latency SLAs.

---

## Sybil Resistance Integration (Everest 77 Interlock)

The trust graph is the substrate for Sybil detection.

**Synthetic Sybil Pattern:** An attacker creates N fake principals, issues all-mutual trust edges between them (e.g., each fake trusts all others with weight 1.0), and injects this densely-connected subgraph into the trust graph.

**Detection (Everest 77):**
  1. **Anomaly signature:** A clique of N unknown principals, all mutually trusting with identical weights, appearing within a short time window.
  2. **Graph clustering:** Compute connected components via BFS; identify "dense" components (clustering coefficient >> graph average).
  3. **Behavioral analysis:** Principals in a suspected Sybil cluster show:
     - Zero social links to the honest graph (isolated).
     - Uniform trust weights (lack natural variance).
     - High velocity (many trust edges in <1 hour).
  4. **Action:** Flag suspicious edges with a `sybil_likelihood: 0.8` flag (advisory, non-blocking). Verifiers can choose to distrust such edges or apply additional scrutiny (Everest 78).

**Proof-of-personhood Bridge (Everest 77 v0):** Each principal registers a proof-of-personhood credential (e.g., government ID attestation, social recovery from N trusted peers). The trust graph enriches this: a principal with a strong PoP + many high-weight edges from diverse issuers is less likely to be a Sybil.

---

## Acceptance Tests

### **T-Z71.1: Edge Add & Query Round-Trip**

```
Given: Principal P, Issuer I, weight 0.8
When: P issues a trust_assertion.v0 edge (P → I)
Then: 
  - Edge is appended to P's chain with incrementing chainIndex
  - Query(P trusts I) returns true within 500ms
  - Path discovery returns [P → I] with composition_weight = 0.8
```

### **T-Z71.2: Weight Composition Correctness**

```
Given: P → I (0.9) → J (0.8) → K (0.7)
When: trust_query(P, K, max_depth=3)
Then:
  - Returns paths with composition_weight = 0.9 × 0.8 × 0.7 = 0.504
  - Query(P, K, weight_threshold=0.5) returns true
  - Query(P, K, weight_threshold=0.51) returns false
```

### **T-Z71.3: Revocation Propagates**

```
Given: Trust edge E (P → I)
When: P issues trust_revocation.v0 referencing E
Then:
  - Revocation is appended to P's chain
  - Within 5 seconds, gossip peers learn the revocation
  - trust_query(P, I) returns false
  - Query(P, I, weight_threshold=0.0) returns false
```

### **T-Z71.4: Privacy-Preserving Query (No Querier Identity Leak)**

```
Given: Query service Q, principal P's trust graph (cached)
When: V (verifier) sends "does P trust I?" to Q
Then:
  - Q returns true/false
  - V is unable to link two queries from the same V
  - V is unable to recover P's full trust graph
  - V is unable to deduce which issuer I was queried
    (if protocol uses ZK set-membership or MPC per Everest 75)
```

### **T-Z71.5: Sybil Pattern Detection (Synthetic Injection)**

```
Given: Trust graph G (honest), Sybil cluster S = {A, B, C, D} where
       all edges are (X → Y, weight=1.0, issuedAt within 1 hour)
When: S is injected into G
Then:
  - Sybil detector identifies at least 3 of {A, B, C, D} as suspicious
  - Flags such edges with sybil_likelihood >= 0.7
  - Querying trust(honest_principal, fake_principal) returns:
    (found: true, paths: [...], sybil_likelihood_info: {...})
```

---

## Composition with Other Everests

- **Everest 16 (issuer-to-issuer trust composition):** This schema extends issuer-to-issuer edges to the full principal-to-issuer graph.
- **Everest 72 (transitivity rules):** Provides normative bounds on max_depth, predicateClass overrides, noTransitivity flags.
- **Everest 73 (revocation propagation):** Formalizes latency SLAs for revocation dissemination.
- **Everest 75 (trust scoring):** Implements privacy-preserving queries atop this schema.
- **Everest 77 (Sybil resistance):** Uses trust-graph clustering to detect synthetic principals.
- **Everest 78 (bot detection):** Flags suspicious edges with bot_likelihood advisory fields.
- **Everest 80 (trust expiration):** Every edge has explicit validUntil; expired edges are excluded from transitive inference.
- **Everest 81 (trust granularity):** Per-predicate-class conditions (academic vs. financial) narrowing the scope of trust.

---

## Open Questions for v1

1. **Trust-Graph Forking:** If a community schisms (e.g., two organizations issue conflicting revocations), which chain is canonical? Should the protocol support branching histories, or mandate a single linear chain?

2. **Machine-Readable Trust Policies:** Can we express "I trust issuers iff they pass audit AND reputation >= 0.8 AND are in GDPR zone" as a declarative policy, rather than hand-coding Everest 72 transitivity rules?

3. **Trust-Marketplace Ethics:** Should principals be able to *sell* trust endorsements? Practical risk: pay-to-trust attacks (Sybil laundering). v1 assumes endorsements are not commoditized.

---

## Signature

— Calm, 2026-05-20

**ZKAC Everest 71 · BAGGED**
