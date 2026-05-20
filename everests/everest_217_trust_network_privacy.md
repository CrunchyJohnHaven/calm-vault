# Everest 217 — Trust-Network Privacy

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 209, 124.*

## The Hard Rule

Trust-graph topology is NEVER PUBLISHED. Only aggregate zero-knowledge predicates are evaluable within the protocol.

This is the sister rule to Everest 124 (values vector publication policy). Where E124 forbids publishing the principal's full values vector, E217 forbids publishing the principal's (or any actor's) trust-graph structure. The reasoning is identical in shape but distinct in scope: trust graphs reveal social topology, and social topology—once exposed—enables targeting, surveillance, and the cascade of chilling effects that destroys the protocol.

## What Is Allowed

The following operations are permitted because they preserve the privacy boundary:

1. **Per-attestation Pedersen commitments** (E201). Each attestation A→B is cryptographically committed without revealing the identity of B or the weight of the edge. The commitment is published; the content is not.

2. **Aggregate reputation scores via ZK proofs** (E211, E212). A principal may prove "my aggregate trust score from long-term residents exceeds threshold T" without revealing which residents trust them, how much they trust them, or what the total is.

3. **Trust-tier predicates returning bits** (E214). A predicate such as `cwp.v0.is_trusted_by_at_least_N_verifiers(N)` returns a single boolean, eliminating all information except the outcome of a binary test.

4. **Cross-aggregate composition** (E210). Multiple aggregate proofs may be composed (e.g., "I am trusted by long-term residents AND rated high for cooperation") without exposing the underlying graph.

## What Is Never Allowed

The following outputs are strictly forbidden:

- The list of who-trusts-whom (any enumeration of principals or their trust relationships)
- The trust-graph adjacency matrix (sparse or dense representation)
- Individual edge weights or confidence scores
- Per-attestation identities without dual-principal consent
- Network visualizations, "social map" modes, or friendship-graph UI
- Derived structures that leak the graph (e.g., "common attestors," "network distance," "social radius")

## Why This Rule Is Absolute

### Social Structure as Attack Surface

A trust graph is not merely a technical object; it is a social map. It reveals:

- Who is socially connected to whom
- Informal status hierarchies (degree, centrality)
- Community structure and subgraph clustering
- Influence pathways

Once this topology is exposed, it becomes immediately actionable for:

- **Advertiser targeting**: identify high-influence nodes, market to them, and observe cascade effects
- **Government surveillance**: map dissidents, activists, and organized opposition
- **Abuser tactics**: locate isolation targets, identify support networks to disrupt
- **Reputation attacks**: find the connectors between a principal and their network, sever them strategically
- **Sybil and collusion**: use the structure to cluster fake accounts and coordinate inauthentic behavior

### The Cascade Effect

The moment a principal realizes their trust network may be exposed, rational behavior changes:

- Attestations drop precipitously (chilling effect)
- Principals become risk-averse, only attesting obvious or trusted actors
- The diversity and reach of the trust network collapses
- The protocol's utility declines to near-zero

This is not a theoretical concern. It has been observed repeatedly in social networks, academic collaboration graphs, and leaked datasets. Once the topology becomes public, the network itself dies.

## Enforcement Mechanisms

### Operator Software Layer

Operator software **must refuse** any request of the form "dump my trust network," "show me my trust graph," "list all principals I have attested," or any variant that would expose the full topology. The request must be rejected at the API boundary, not returned with "restricted" fields.

Error response example:
```
Error: graph_query_not_permitted
Reason: Trust-graph topology is not queryable. Use aggregate predicates instead.
Permitted alternatives: cwp.v0.aggregate_trust_score_proof, cwp.v0.trust_tier_bit
```

### Graph Operations

All operations that touch the trust graph must return only:
- Aggregate proofs (ZK commitments to aggregate functions)
- Predicate results (single bits or short vectors)
- Batch cryptographic commitments (no identities)

No query may return a list of principals, a subgraph, or a partial adjacency matrix.

### Rate Limiting and Commitment Hiding

Repeated aggregate queries (e.g., "trust score greater than X" with many different values of X) could be combined to infer individual edge weights. Rate limiting on per-principal predicate queries, paired with commitment hiding (storing only the hash, not the proof), prevents inference attacks.

## The Local Principal Exception

A principal may view their **own** local trust graph: the set of attestations they have created AND the set of attestations created about them (their in-degree neighbors). This view is:

- **Principal-private**: stored locally and not transmitted except under explicit user action
- **Boundary-respecting**: never crosses into the broader network topology
- **User-controlled**: the principal can inspect it whenever they choose, delete their own attestations, but cannot unilaterally delete edges directed toward them

This exception is essential for usability and accountability. A principal must know whom they have attested and who has attested them; otherwise, they cannot manage their own reputation or correct errors.

## Bilateral Disclosure Consent

A single attestation A→B is created by A and concerns B. If a third party C wishes to learn about this edge (e.g., through an introduction or a reputation query), **both A and B must consent**.

Default rule: **neither consents**. Consent is affirmative, explicit, and cannot be assumed or inherited.

### Asymmetric Consent Insufficient

If A says "I want to disclose my attestation in B to C" but B does not consent, the disclosure does not occur. B's privacy is implicated; B's attestation record includes the fact that they are the object of A's trust. They have a right to control whether that fact becomes known.

### The Introducer Pattern

When A explicitly introduces B to C (a social act, not a protocol act), A's act of introduction implicitly discloses to C that "A trusts B enough to introduce them." This is:

- **One-time and directional**: C learns only about the A→B edge, not about B's other attestors
- **Social convention**: the act of introduction is understood to carry this signal
- **Exception to the bilateral rule**: A's act of introduction counts as A's affirmative consent, and the introducer pattern is understood as B's implicit consent to be introduced (B can refuse to engage with C after introduction, but the introduction itself may occur)

Beyond this narrow exception, bilateral consent is required.

## Network-Level Privacy via Differential Privacy

Aggregate statistics on the global trust graph (graph density, average degree, degree distribution shape) are valuable for protocol health monitoring. These may be computed and published, but only via the differential privacy layer (E185):

- Noise is added to all published statistics
- Privacy budget is tracked and exhausted carefully
- Individual principal contribution is plausibly deniable
- Population-level facts are revealed; individual facts are protected

A principal's individual network topology is **never** published in aggregate form, even under DP guarantees, because:

1. The aggregate statistics contain information about a principal's network size, which is linked to identity
2. Network size + demographic information = re-identification
3. It violates the spirit of the rule: the topology should not be knowable, even probabilistically

## Allowed ZK Predicates

The following predicate types are permitted:

- `cwp.v0.trusted_by_N_long_residents(N)` — Boolean: true if at least N long-term residents have attested the principal. Returns the count via ZK proof; identities not revealed.
- `cwp.v0.trust_aggregate_in_range(low, high)` — Boolean: true if the principal's aggregate trust score falls in [low, high]. Returns the bit; the exact score is not revealed.
- `cwp.v0.trusts_at_least_one_in_set(set_of_VCs)` — Boolean: true if the principal has attested at least one member of the provided set. Returns the bit; does not reveal which member.
- `cwp.v0.attestation_density_threshold(threshold)` — Boolean: true if the principal's out-degree (number of principals they have attested) exceeds a threshold. Threshold is principal-chosen; the exact degree is not revealed.
- `cwp.v0.mutual_trust_with_specific_principal(other, consent_token)` — Boolean: true if A and B have mutually consented to reveal the A↔B edge to a third party holding a consent token. Requires bilateral cryptographic tokens.

All predicates return a single bit or a short fixed-length vector. None return enumerations, lists, or rankings.

## Privacy Attacks and Defenses

### Network Correlation

**Attack**: A principal C observes that X and Y both attest to Z. C infers that X and Y are connected (via Z) and uses this to map out the network.

**Defense**: Each attestation is individually committed (E201). The fact that X and Y have both attested Z is revealed (batch commitments are necessary for protocol function), but the identities are blinded via commitment. Cross-correlation requires the principal to hold separate consent tokens from X and Y, which they do not have.

### Side-Channel Timing

**Attack**: By observing the timestamps of batch commitments, a principal can infer which attestations were created near each other, inferring clustering or collusion.

**Defense**: Attestations are batched on a fixed schedule (e.g., once per epoch), and batches are padded with dummy commitments. This eliminates timing signals.

### Inference from Aggregate Queries

**Attack**: A principal repeatedly queries `trust_aggregate_in_range` with many different ranges, then uses binary search to narrow down the exact aggregate score. This allows inference of the underlying degree.

**Defense**: Per-principal rate limiting on predicate queries (e.g., max 10 queries per week). Additionally, predicates are pinned to commitment hashes rather than live proofs, forcing precommitment before querying.

## Deletion and Accountability

A principal may remove their own attestations (only). If A attests B and later deletes the attestation, the deletion is itself recorded as a chain event:

```
Event: Attestation deleted
Attester: A
Target: B (blinded)
Timestamp: T
Hash-of-deletion: H
```

This prevents silent deletion and ensures that downstream systems can flag suspicious deletion patterns (e.g., principal A repeatedly attests and deletes, creating noise).

The principal cannot delete attestations directed at them; only A can delete A's own edges. This preserves the integrity of B's reputation record.

## Design Rationale: Why Not Publish a Sanitized Graph?

A common alternative proposal is to publish the graph with sensitive attributes removed: "release the edges, but not the identities." This approach fails because:

1. **Graph fingerprinting**: Even unlabeled graphs can often be re-identified via structural properties (degrees, clustering coefficients, shortest paths). A trust graph with known node counts and edge counts is highly identifying.
2. **Auxiliary information**: A principal's demographic data (joined date, geographic region, language, stated interests) is often available elsewhere. Combined with an unlabeled graph, it re-identifies edges.
3. **Partial knowledge attacks**: An attacker who knows B's degree can enumerate B's inbound attestors; knowing B's out-degree and a few of B's explicit trust relationships narrows it down further.
4. **No principled stopping point**: If the graph is published, every additional piece of information (even aggregate statistics) becomes a new vulnerability.

The only safe approach is to not publish the topology at all.

## Implementation Notes

Trust-graph operations must be implemented in the operator software, not delegated to user code or external services. The operator **must**:

- Validate every query before execution
- Reject topology-revealing queries outright
- Log and alert on policy violations
- Audit the audit logs for breach patterns

No user-facing API exposes raw graph data. All graph access goes through the predicate layer.

## Cross-References

- **E124**: Values vector publication policy (sister rule; never publish a principal's full values vector)
- **E201**: Per-attestation Pedersen commitments (required for trust-graph privacy)
- **E209**: ZK trust proof primitives (foundational to aggregate proofs)
- **E210**: Cross-aggregate composition (necessary for complex predicates)
- **E211, E212**: Aggregate reputation scores via ZK (allowed operations)
- **E214**: Trust-tier predicates (allowed bit-returning queries)
- **E216**: Trust under coercion (related edge case)
- **E185**: Differential privacy for population-level statistics

---

— Calm, 2026-05-20
