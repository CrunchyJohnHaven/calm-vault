# Everest 218 — Trust vs Reputation Distinction

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 201, 211.*

## The Core Distinction

The cryptographic wallet protocol (CWP) v0 maintains two distinct primitives for how principals evaluate each other: **trust** and **reputation**. While often conflated in colloquial usage, they are structurally different, serve different discovery and decision-making purposes, and must be implemented as separate predicates in the proof system.

**Trust** is dyadic, asymmetric, and granular. When principal A trusts principal B, that trust is:
- Specific to A (the truster)
- Directional (A→B, not necessarily B→A)
- Dimensioned (A might trust B on technical competence but not financial management)
- Weighted (A assigns a confidence coefficient w to their trust)
- Temporal (the trust attestation carries a timestamp t)

**Reputation** is a network-aggregate and contextual. The reputation of principal B in dimension d is:
- Computed from the trust attestations of many principals toward B
- Agnostic to the identity of individual attestors (in disclosure semantics)
- Dimensional (distinct reputation scores per competency domain)
- Threshold-disclosable (B can prove aggregate reputation exceeds a threshold without revealing component votes)

In other words: trust is what I believe about you; reputation is what the network believes about you. These are different questions, asked in different contexts, requiring different proof structures.

## The Two Primitives

### TRUST PRIMITIVE (from Everest 201)

The trust primitive implements edges in a directed, weighted trust graph. Each edge is an attestation that principal A makes about principal B with respect to a dimension d:

```
edge(A, B, d, w, t, disclosure_mode) → VirtualCredential
```

This credential is principal-private: only A controls the attestation. When A chooses to disclose a trust proof to a third party, bilateral consent is typically required (A discloses that A trusts B, potentially revealing the existence of the relationship). The proof reveals:
- The attesting principal A (disclosed)
- The target principal B (disclosed)
- The dimension d (disclosed)
- Whether w meets a threshold (disclosed)
- The timestamp t (disclosed)

The full attestation is never revealed to unauthorized parties; only the specific claim (e.g., "A trusts B on technical competence above threshold T") is proven.

### REPUTATION PRIMITIVE (from Everest 211)

The reputation primitive computes an aggregate from many trust attestations. The reputation of B in dimension d is:

```
reputation(B, d, threshold) → AggregateProof
```

This is computed from all (or a sample of) the trust edges pointing to B in dimension d:

```
reputation(B, d) = aggregate([edge(A1, B, d, w1, t1), edge(A2, B, d, w2, t2), ...])
```

The aggregation function (typically a weighted sum or threshold count) is public and deterministic. However, the individual edges are not revealed. When B proves reputation, the proof discloses only:
- The target principal B (disclosed)
- The dimension d (disclosed)
- The aggregate score or its relationship to a threshold (disclosed)
- Optionally: the number of attestors (disclosed) or a privacy-preserving upper bound

Critically, the identities of individual attestors remain hidden in the reputation proof. This is the identity-shrouding property: the network knows B is well-regarded, but B's proof does not leak who specifically vouches for B.

## Why Both Primitives Are Needed

Consider the decision tree for two principals meeting for the first time (the "stranger handshake"):

1. **Pact Alignment Check (E143)**: Do both principals subscribe to compatible protocol rules?
2. **Reputation Threshold Check (E213)**: Does B have sufficient aggregate standing in relevant dimensions?
3. **Transitive Trust Check (E209)**: Does anyone A trusts transitively vouch for B?
4. **Bilateral Trust Establishment (E201)**: Once the stranger phase passes, A can attestify trust in B.

Steps 2 and 3 answer fundamentally different questions:

- "Does B have community standing?" → reputation aggregate (E211)
- "Does someone I personally trust vouch for B?" → transitive trust (E209), which chains bilateral trust edges

Reputation alone cannot answer whether A's trusted advisors endorse B. Bilateral trust alone cannot answer whether B is generally well-regarded. Both are needed.

## Disclosure Semantics

### Trust Proofs

A trust proof reveals a bilateral relationship:

```
cwp.v0.is_trusted_by(target_vc, threshold) → Bool
```

When A proves "I trust B above threshold T on dimension d," the counterparty (B or a mediator) learns:
- A specific principal A trusts this target
- The dimension is d
- The weight exceeds T
- The attestation was made at time t

Bilateral consent is implicit because both parties (A and B) typically participate in the handshake. However, in transitive scenarios (E209), A might selectively disclose trust in an intermediary to a third party; this still requires A's consent.

### Reputation Proofs

A reputation proof reveals aggregate standing without identifying constituent votes:

```
cwp.v0.reputation_aggregate(dimension, threshold) → AggregateProof
```

When B proves reputation in dimension d above threshold T, the counterparty learns:
- The aggregate score or its relationship to T
- The dimension d
- Optionally: the cardinality of votes or a privacy bound

Critically, the counterparty does not learn which principals voted. This is principal-side consent: B alone authorizes the reputation proof. No bilateral agreement with the network of attestors is needed.

## Privacy Properties

### Trust Privacy

Trust edges are identity-revealing in the limit. If A's complete trust graph (all edges A→*) were published, the graph itself would leak A's social structure: who A deems competent, trustworthy, or valuable in different domains. For this reason, trust attestations are principal-private, and disclosure requires A's explicit consent per relationship.

### Reputation Privacy

Reputation aggregates are identity-shrouding. When B proves reputation in dimension d, the aggregate hides individual attestors. An observer knows "B is trusted by N principals in domain d with aggregate weight W," but not which specific principals are the N attestors. This is especially valuable in competitive or sensitive domains (e.g., medical expertise, whistleblowing networks) where individual votes would reveal social patterns or create liability.

## Use Cases and Decision Points

### The "Stranger Handshake"

Two principals with no prior relationship meet. A wants to know:
- Does B have reputation in a dimension relevant to this transaction?
- Does someone I trust recommend B?

B can immediately prove reputation (E211) without asking anyone's permission; this is a low-friction reputation signal. A can optionally check transitive trust (E209) if A has trusted advisors in the same domain. Both signals inform A's decision independently.

### "Well-Known but Not Trusted by Me"

High reputation + low bilateral trust: B has strong community standing, but A has personal reasons to distrust B (prior bad experience, value mismatch, conflicting interests).

Both signals are captured separately. B's reputation proof stands independently; A's trust edge (or lack thereof) stands independently. A chooses what to weight. This is crucial: a general-purpose reputation system cannot overrule individual judgment.

### "Trusted by Me but Unknown to the Network"

High bilateral trust + no aggregate reputation: A trusts B based on prior interaction or reference, but B is new to the network and has not accumulated broad reputation yet.

This is how new principals are introduced into the network. A's trust attestation (E201) says "I vouch for B." When A transitively discloses this to third parties (E209), it becomes "someone established in the network trusts B." This chain propagates without requiring B to have independent reputation.

## Why Not Collapse Into One Metric

A tempting simplification would be to compute a single "trust score" that combines bilateral trust with aggregate reputation. This fails for several reasons:

1. **Aggregate masking**: A single score masks community diversity. B might have high reputation among one cohort and low reputation in another. Aggregating into one number loses the dimensional structure.

2. **Relationship asymmetry**: A→B trust may be high while B→A trust is low. A single metric cannot represent this asymmetry.

3. **Privacy leakage**: A single "overall trust" metric would require publishing both edges (bilateral relationships) and aggregates simultaneously, inflating the privacy surface.

4. **Decision conflation**: A stranger asking "is B trustworthy?" is asking a different question than "do I trust B?" The first is answered by reputation; the second by bilateral edges. Conflating them prevents nuanced decision-making.

## Composition with Other Everests

Everest 218 integrates with the broader trust infrastructure:

- **E143 (Pacts)**: Pacts establish protocol compatibility; reputation and trust predicates operate within compatible pact boundaries.
- **E201 (Trust Graph)**: Defines the trust edge primitive; E218 distinguishes this from reputation.
- **E202 (Transitive Trust)**: Chains bilateral trust edges; different from reputation aggregation (E211).
- **E209 (Trust Intermediaries)**: Selectively discloses trust edges to introduce third parties; uses bilateral trust, not reputation.
- **E210 (Trust Revocation)**: Allows A to revoke trust in B; does not directly affect B's reputation aggregate (other attestors' edges remain).
- **E211 (Reputation Aggregation)**: Computes network-wide reputation from trust edges; this document distinguishes it from bilateral trust.
- **E213 (Reputation Thresholds)**: Defines disclosure semantics for reputation proofs; this document motivates why separate predicates exist.
- **E120 (Capability Proofs)**: Reputation and trust proofs are subcategories of capability proofs; both can be chained to answer complex discovery questions.

## The Proof Predicates

The v0 proof system exposes two core predicates:

```
cwp.v0.is_trusted_by(target, dimension, threshold) → TrustProof
```
Prover: principal A (the truster). Verifier: B or a third party. Discloses: A's identity, B's identity, dimension, and that A's weight on B in dimension d exceeds threshold.

```
cwp.v0.reputation_aggregate(dimension, threshold) → ReputationProof
```
Prover: principal B (the target of reputation). Verifier: anyone. Discloses: B's identity, dimension, and that the aggregate reputation of B in dimension d exceeds threshold. Individual attestors' identities remain hidden.

These predicates are composable: a discovery engine can ask for both proofs from B and make decisions based on the union of signals.

## Conclusion

Trust and reputation are not interchangeable. Trust captures bilateral relationships; reputation captures network consensus. The CWP v0 implements both as distinct primitives, allowing principals to reason about their own trusted networks and the broader community standing of counterparties simultaneously. This dual-signal approach enables richer, more nuanced decision-making than either signal alone could provide.

— Calm, 2026-05-20
