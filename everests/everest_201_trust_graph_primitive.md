# Everest 201 — Trust Graph Primitive

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 120.*

## Overview

TRUST_GRAPH defines a directed weighted graph where principals are nodes and trust attestations are edges. This primitive forms the foundation for reputation aggregation (E211), sybil resistance (E212), and privacy-preserving reputation queries (E217). Unlike the bilateral cooperation graph (E184), the trust graph captures unilateral assertions of trust in other principals, anchored to witness attestations (E120) and identities (E11).

## Graph Definition

The trust graph G = (N, E, W, M) comprises:

- **Nodes (N)**: Principals identified by CredexAI VC fingerprints. Each node represents a unique, cryptographically verified identity on the network.
- **Edges (E)**: Directed weighted trust attestations. An edge A → B represents principal A's attestation of trust in principal B.
- **Weights (W)**: Each edge carries a weight w ∈ [0, 1] normalized, internally stored as fixed-point integers in [0, 10000] for arithmetic precision. Weights aggregate multiple attestations and decay over time according to configurable decay_rate parameters.
- **Metadata (M)**: Each edge carries relationship_class (from E120 enumeration such as colleague, mentor, peer, organization), basis (how the trust assertion was formed), timestamp, and decay_rate.

From principal P's perspective, their LOCAL trust graph contains:
- All nodes P has issued attestations about (out-edges from P).
- All nodes that have issued attestations about P (in-edges to P).
- The GLOBAL trust graph is the union of all local views, though in practice each principal sees only their slice for privacy reasons.

## Trust Attestation Record

All trust assertions in the network are captured as immutable attestation records:

```
{
  "kind": "trust_attestation",
  "payload": {
    "target_principal_vc": "vc:fingerprint:...",
    "dimension": "general" | "trust_honesty" | "trust_competence" | ...,
    "weight": 0-10000,
    "basis": "direct_observation" | "attested" | "indirect" | "joint_history" | "professional_reference",
    "context": "Free-text narrative explaining the basis for trust assertion",
    "expiry_ts": null | <ISO8601 timestamp>
  },
  "signer": "<principal-private-key signature>",
  "timestamp": "<ISO8601 creation timestamp>"
}
```

**Field semantics:**

- **target_principal_vc**: The VC fingerprint of the principal being trusted. Immutable and verifiable against E11 identity registry.
- **dimension**: Allows multi-dimensional trust assessment. "general" is the default; specific dimensions allow fine-grained trust modeling (e.g., honesty vs. technical competence vs. reliability). Aggregation is per-dimension.
- **weight**: Fixed-point integer [0, 10000] representing trust strength. 0 = no trust; 10000 = maximum trust. Multiple attestations to the same target and dimension are aggregated by weighted average or specified aggregation function.
- **basis**: Explains how the trust was derived. "direct_observation" indicates first-hand experience; "attested" indicates hearsay from a trusted intermediary; "indirect" indicates inferred from prior interactions; "joint_history" indicates shared collaborative work; "professional_reference" indicates formal reference or certification.
- **context**: Narrative justification. Enables human review and downstream reputation algorithms to weight attestations by reasoning quality.
- **expiry_ts**: Optional timestamp after which the attestation becomes stale. Enables time-bounded trust and automatic cleanup.

Each attestation is signed by the asserting principal's private key, making it non-repudiable and verifiable.

## Per-Principal Trust Views

Each principal maintains a LOCAL trust view:

- **Outbound view**: All attestations issued by the principal about others.
- **Inbound view**: All attestations received about the principal.
- **Aggregated view**: Per-target, per-dimension trust summary computed from all inbound attestations using weighted aggregation and decay functions.

The principal can query their own aggregated trust in target P as:

```
trust_score(target, dimension) = 
  sum(weight_i * decay(age_i) * credibility_i for all i in attestations_about_target) 
  / sum(decay(age_i) * credibility_i for all i)
```

where decay(age) decreases trust linearly or exponentially with time, and credibility_i is a function of the attester's reputation.

## Privacy Guarantees

Trust attestations are **PRINCIPAL-PRIVATE by default**:

- Each principal controls visibility of their attestations. Attestations are stored in the principal's user_state.jsonl and not broadcast to the global state by default.
- **Selective disclosure**: A principal may selectively reveal attestations to specific counterparties (e.g., to establish trust during a transaction or negotiation).
- **Aggregate publishing**: Principals may publish aggregate trust scores (e.g., "I have high trust in X") without revealing individual attestations or their signers.
- **Zero-knowledge aggregation** (E209, E211): The network can compute aggregate reputation scores over the trust graph without disclosing individual attestations or graph structure. Pedersen commitments to edge weights enable ZK proofs of reputation properties (e.g., "this principal has >90% inbound trust").

## Trust Graph Operations

The trust graph supports the following operations:

### add_attestation(source, target, weight, basis, dimension)
Issues a new attestation from source to target. The attestation is signed by source's private key and appended to source's user_state.jsonl. If an existing attestation exists for the same (target, dimension) pair, the new attestation is added; aggregation logic determines the final weight.

### remove_attestation(attestation_id)
Removes an attestation record. Only the source principal can remove their own attestations. Removal appends a cancellation marker rather than deleting, preserving chain integrity.

### update_weight(attestation_id, new_weight)
Updates the weight of an existing attestation. Only the source principal can update. Updates append a new weight entry with timestamp.

### query_local_trust(target, dimension)
Returns the aggregated trust score for target from the querying principal's local view, optionally filtered by dimension. Applies decay functions to older attestations.

### aggregate_global_trust(target, dimension)
Computes global trust in target across the network. Requires aggregating inbound attestations from multiple sources, subject to privacy constraints. Typically performed in ZK to avoid revealing graph structure.

## Cross-References with Cooperation Graph (E184)

The cooperation graph (E184) and trust graph serve complementary roles:

- **Cooperation graph (E184)**: Bilateral, symmetric. Both parties agree they have cooperated. Stored in shared state.
- **Trust graph (E201)**: Unilateral, asymmetric. One principal asserts trust in another. Private by default.
- **Relationship**: Cooperation history feeds into trust assessment. Joint work (basis = "joint_history") strengthens trust attestations. Both graphs inform reputation aggregation (E211).

## Storage

Trust attestation records are chain-resident:

- **Primary storage**: Each principal's user_state.jsonl (append-only). Attestations are immutable once recorded.
- **Commitment storage**: Pedersen commitments to attestation weights are optionally stored on-chain or in a side-car commitment tree for ZK aggregation (E209).
- **Index storage**: Bloom filters or other indexes enable fast lookups of inbound/outbound attestations without full graph traversal.

## Implementation

### Rust: calm-zkac-trust-rs crate
Native ZK-enabled trust graph with:
- Fixed-point arithmetic for weight aggregation.
- Pedersen commitment generation for privacy.
- Graph traversal and query optimization.
- Integration with CredexAI identity (E11) and witness attestations (E120).

### Python: calm_witness/trust.py
Reference implementation providing:
- Attestation record serialization/deserialization.
- Aggregation and decay functions.
- Local graph operations.
- Query APIs for reputation systems.

### Persistence: Append-only chain
All operations append to principal user_state.jsonl. No deletions; only cancellation markers. Enables non-repudiation and auditability.

## Performance

- **Adding attestation**: <5ms (cryptographic signing + append to local state).
- **Local trust query**: <50ms for typical local graph (100-1000 nodes, aggregation with decay).
- **Global aggregation**: Requires ZK proofs (E209), latency depends on proof size; typical proofs < 1 second.
- **Graph traversal**: Transitive trust queries (E202) are O(k) in path length; pruning and memoization keep k small in practice.

## Validation and Integrity

All attestations must satisfy:

1. **VC fingerprint validity**: target_principal_vc must correspond to a registered principal in E11.
2. **Cryptographic signature**: Attestation must be signed by source's private key, verifiable against their public key.
3. **Weight bounds**: weight must be in [0, 10000].
4. **Timestamp validity**: timestamp must be <= current time; expiry_ts (if present) must be > timestamp.
5. **Basis validity**: basis must be a recognized enum value.

Validation occurs at ingestion time. Invalid attestations are rejected and logged.

## Security Considerations

- **Non-repudiation**: Cryptographic signatures ensure a principal cannot deny issuing an attestation.
- **Timestamp ordering**: Attestations are timestamped to prevent replay attacks and enable decay functions.
- **Private-by-default**: Attestations are not broadcast to global state, reducing inference attacks on graph structure.
- **Selective disclosure**: Principals control who sees their attestations, mitigating targeted sybil attacks based on graph analysis.
- **Decay and freshness**: Time-decaying weights ensure old attestations don't indefinitely inflate reputation, addressing long-term sybil strategies.

## Integration with E202 (Transitivity)

Transitive trust queries leverage the trust graph: "Is there a trust path from A to C?" The transitivity engine traverses the graph respecting weight decay and privacy boundaries. Typical transitive trust considers paths of length 2-3 to avoid noise.

## Integration with E211 (Reputation Aggregation)

The reputation system (E211) ingests both cooperation edges (E184) and trust edges (E201) to compute per-principal reputation scores. Trust graph edges are weighted by basis quality and attester reputation, creating a feedback loop.

## Integration with E212 (Sybil Resistance)

Sybil defense (E212) leverages the trust graph to detect cliques of mutually-attesting principals with suspiciously uniform weights. Graph clustering and anomaly detection flag potential sybil attacks.

## Integration with E217 (Privacy)

Privacy guarantees (E217) enforce selective disclosure: a principal may prove aggregated trust properties in ZK without revealing individual attestations.

---

— Calm, 2026-05-20
