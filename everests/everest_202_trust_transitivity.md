# Everest 202 — Trust Transitivity

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 201.*

## The Problem

Trust is not absolute; it propagates through networks with attenuation. When agent A trusts agent B with confidence weight w1, and B trusts agent C with weight w2, the question emerges: with what weight should A trust C through B's intermediation?

Direct trust is strongest. Transitive trust—trust inherited through introduction chains—decays as it traverses more hops. The challenge is capturing this mathematically while remaining tractable for both on-chain verification and zero-knowledge proofs.

Consider the introducer pattern: when A meets C through B's introduction, A can bootstrap an initial trust estimate for C before direct interaction. This is valuable for cold starts in peer-to-peer networks. But the decay must be fast enough to prevent trust from being trivially diluted across unbounded networks, yet forgiving enough to allow meaningful cross-community introductions.

## The Decision: Multiplicative Decay

We adopt **multiplicative decay** as the canonical rule for single-hop and multi-hop trust inheritance.

For a two-node chain (A → B → C):

```
T(A → C) = w(A → B) × w(B → C) × hop_multiplier
```

Where:
- `w(A → B)` is A's direct attestation weight for B (typically in [0, 1])
- `w(B → C)` is B's direct attestation weight for C
- `hop_multiplier` is a relationship-class-dependent decay factor, ∈ [0.3, 0.7]

The multiplicative model reflects the conditional nature of trust: A trusts C not unconditionally, but only insofar as A trusts B's judgment and B vouches for C. This mirrors probability composition—the joint confidence is the product of marginal confidences.

### Per-Relationship-Class Hop Multiplier

Different relationship types carry different degrees of judgment transferability. A mentor's endorsement propagates trust more reliably than an acquaintance's.

| Relationship Class | hop_multiplier | Rationale |
|---|---|---|
| mentor-vouches-for | 0.7 | High expertise carryover; mentor is selected for judgment quality |
| peer-collaborator | 0.6 | Moderate transfer; collaboration history signals compatible values |
| family | 0.5 | Emotional bonds do not always correlate with trustworthiness assessment |
| professional-counterparty | 0.5 | Business relationships are transactional; trust is domain-specific |
| acquaintance | 0.3 | Low information transfer; acquaintances rarely validate deep character |

These values are calibrated for v0 and subject to governance updates as network behavior is observed.

### Multi-Hop Trust Paths

When the path from A to C spans more than one intermediate hop:

```
2 hops (A → B → C → D):
T(A → D) = w(A → B) × w(B → C) × w(C → D) × (hop_multiplier ^ 2)

3 hops (A → B → C → D → E):
T(A → E) = w(A → B) × w(B → C) × w(C → D) × w(D → E) × (hop_multiplier ^ 3)
```

Each additional hop multiplies by `hop_multiplier` again. Since hop_multiplier ≤ 0.7, trust decays exponentially:

- After 2 hops with multiplier 0.6: trust is multiplied by 0.36
- After 3 hops with multiplier 0.6: trust is multiplied by 0.216
- After 4 hops with multiplier 0.6: trust is multiplied by 0.130

Beyond 3 hops, trust signals effectively decay to zero (< 0.1 in most configurations). This is by design: your friend's friend's friend's friend carries minimal credibility.

## Shortest Path and Multiple Routes

In non-trivial trust networks, multiple paths from A to C may exist. The algorithm must decide: which path governs the inherited trust weight?

### Path Selection Rule (v0 default)

**Use the maximum trust value over all acyclic paths from A to C**, subject to a cap: the transitively inherited trust cannot exceed A's direct trust in C (if a direct relationship exists).

Rationale: We want to give A the benefit of the most credible introduction chain. If multiple paths reach C, the strongest one should be the basis for initial trust. This is generous but not reckless—it caps at direct trust.

**Alternative mode: average-path**

For more conservative deployments, average the trust weights over all paths. This moderates outlier chains but requires more graph computation.

The v0 default is MAX with capping. Future versions may expose this as a tunable parameter.

### Cycle Handling

Trust graphs are directed and may contain cycles. A → B → A is valid (mutual trust). The path-finding algorithm must detect and break cycles to prevent infinite loops.

Implementation rule:
- Perform depth-first search from A seeking C
- Maintain a "visited" set per search to track nodes on the current path
- If a node is revisited on the same path, prune that branch
- Continue exploring other branches

Each node can be visited once per source-target search path. This ensures termination while preserving all distinct acyclic paths.

## Worked Examples

### Example 1: Strong Mentor Chain

A trusts B as a mentor with weight 0.9.
B trusts C as a mentor with weight 0.8.
Both relationships are mentor-vouches-for (hop_multiplier = 0.7).

```
T(A → C) = 0.9 × 0.8 × 0.7 = 0.504
```

A inherits confidence 0.504 in C through B's introduction. This is substantial—above the typical threshold for initial-contact collaboration (often 0.4–0.5).

### Example 2: Weak Acquaintance Chain

A trusts B as an acquaintance with weight 0.9.
B trusts C as an acquaintance with weight 0.8.
Both relationships are acquaintance (hop_multiplier = 0.3).

```
T(A → C) = 0.9 × 0.8 × 0.3 = 0.216
```

A's inherited trust in C is weak (0.216), well below typical collaboration thresholds. An introduction is possible but carries little credibility weight.

### Example 3: Three-Hop Path

A trusts B (peer-collaborator, 0.85).
B trusts C (peer-collaborator, 0.9).
C trusts D (peer-collaborator, 0.8).
hop_multiplier = 0.6 for all steps.

```
T(A → D) = 0.85 × 0.9 × 0.8 × (0.6 ^ 2)
         = 0.612 × 0.36
         = 0.220
```

After three hops, even with high edge weights and a strong multiplier, trust decays to 0.22.

## Why Multiplicative (vs. Additive)

Additive decay—T(A → C) = w(A → B) + w(B → C) - ε—would violate intuition: adding multiple weak signals produces an artificially strong result. If A barely trusts B, and B barely trusts C, A should barely trust C; addition yields false confidence.

Multiplication reflects **conditional probability**: A trusts C if and only if A trusts B (probability P1) and B trusts C (probability P2). The joint probability is P1 × P2. Long chains rightfully decay quickly because confidence is compounded, not accumulated.

Mathematically, multiplicative decay ensures that trust diminishes as paths lengthen, preventing the network from becoming a "trust soup" where everyone is transitively connected at high confidence.

## The Introducer Pattern

When agent A meets agent C through B's introduction, the workflow is:

1. A computes `T(A → C)` using the multi-hop algorithm
2. If `T(A → C) ≥ threshold_initial`, A accepts the introduction and bootstraps collaboration
3. Direct interactions between A and C then update their mutual trust weights
4. Over time, the transitively inherited trust is gradually replaced or confirmed by direct evidence

This pattern solves the cold-start problem: strangers can begin interactions with a non-zero baseline confidence, reducing friction in peer discovery.

## Predicate: Transitively Trusted

The canonical predicate for checking transitively inherited trust:

```
cwp.v0.transitively_trusted(target, threshold, max_hops=3)
  → bool
```

Returns true if there exists an acyclic path from self to target such that:
- The computed trust weight T(self → target) ≥ threshold
- The path length ≤ max_hops

Implementation caches path results to avoid re-computation. Caching keys are (source, target, threshold).

## Anti-Collusion: Sybil Resistance

Trust paths can be exploited. If a coordinated group of sock-puppet accounts form a clique and introduce each other with high weights, they may artifically bootstrap trust for new accounts.

Countermeasure: **network analysis layer**

When evaluating a trust path, inspect the subgraph for known clustering patterns. If a path traverses a suspected sybil cluster, apply a secondary decay multiplier (e.g., 0.5×) to the inherited weight.

This composes with Everest 212 (sybil resistance) and requires off-chain reputation signals (time-on-network, transaction volume, stake lockup) to identify suspects.

## ZK Considerations

Multi-hop trust computation can be proven in zero-knowledge. A prover (holding A's trust graph) can prove to a verifier that `T(A → target) ≥ threshold` without revealing:
- The intermediate nodes on the path
- The individual edge weights
- The structure of A's trust network

The proof uses range commitments on the product of edge weights and multiplicative decomposition of the threshold. This is a harder summit and composes with Everest 209 (trust ZK proofs).

Initial implementations will be non-ZK; ZK proofs are deferred to Phase XV.

## Governance and Updates

The hop_multiplier values and max_hops default (3) are governance parameters. Changes require a governance vote. Initial values are conservative; real-world network behavior may warrant calibration.

If the network observes that trust chains beyond 2 hops are largely untrustworthy, future versions may reduce max_hops to 2 or lower the multipliers for longer paths.

---

— Calm, 2026-05-20
