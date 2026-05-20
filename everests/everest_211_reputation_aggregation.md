# Everest 211 — Reputation Aggregation

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 120, 201.*

## Overview

Reputation aggregation synthesizes multiple evidence streams into a dimensioned reputation score for any principal within the Calm ZKAC system. The predicate `cwp.v0.reputation_aggregate(dimension, window)` combines trust-graph attestations, witness claims, and chain-inferred behavior into a ZK-provable reputation metric that resists gaming, protects privacy, and guards against self-aggrandizement.

Unlike monolithic reputation systems, this design preserves selective disclosure: a counterparty requests reputation on *specific dimensions* (e.g., "technical competence," "capital reliability"), not a collapsed aggregate score. This prevents reputation from becoming a blunt instrument and enables nuanced trust decisions.

## Three Sources of Reputation

### 1. Trust Graph (Everest 201)

Direct and transitive trust attestations targeted at the principal form the primary input. A trust-graph edge from A to B on dimension D carries:

- **Direct attestation weight**: A's explicit claim that B is trustworthy on D
- **Transitive depth**: A's own trust standing on D (via chain induction) scales this edge
- **Freshness**: recent attestations decay slower than stale ones per Everest 203 time-weighting rules

The trust graph captures what *others claim to know* about the principal. Attestations flow inward; reputation aggregation sums all weighted inflows on the requested dimension.

### 2. Witness Attestations (Everest 120)

Explicit per-dimension attestations from independent principals provide external corroboration. Unlike trust-graph edges (which can be implicit or relational), witness attestations are direct claims: "I attest that principal P demonstrates competence D at level L, witnessed during event E."

Key properties:

- **Independence**: multiple distinct witnesses weight more heavily than repeated attestations from the same source
- **Attestor standing**: a witness's own trust score and chain depth scale their attestation weight
- **Frequency vs. consistency**: patterns of unanimous attestation outweigh conflicting single claims
- **Anti-Sybil filtering**: the witness-chain-depth requirement (E120) excludes shallow, low-standing attestors

### 3. Chain Self-Narration + Action Inference (Everest 109)

The principal's own verifiable chain history and inferred behavior form the third stream. Everest 109 derives behavioral scores from on-chain actions: code commits quality, transaction patterns, dispute participation, artifact validation, and consistency across dimensions.

Self-narration is weighted *least* (0.2 default) to counterbalance bias. A principal cannot self-report high reputation without external corroboration. This defends against self-aggrandizement and ensures reputation reflects *external perception*, not internal claims.

## Reputation Formula

The per-dimension reputation score aggregates the three sources:

```
reputation(P, dim, window) = 
  w_trust * Σ(trust_inflows_dim_weighted) + 
  w_witness * Σ(witness_attestations_dim_weighted) + 
  w_self * inferred_score(P, dim, window)
```

**Default weights:**
- w_trust = 0.4 (trust graph — direct relational claims)
- w_witness = 0.4 (witness attestations — external corroboration)
- w_self = 0.2 (chain inferred behavior — self-demonstrated track record)

The 0.4-0.4-0.2 split ensures external signals (trust + witness = 0.8) dominate self-report (0.2). This weight scheme is configurable; different trust contexts may require different ratios. However, the default ensures that a principal cannot achieve high reputation by unilateral self-narration alone.

## Time-Weighting and Decay

Attestations are not equally fresh:

- **Recent attestations** (within 7 days) weight at full value
- **Medium-age attestations** (7-90 days) decay by a per-attestation rate ρ ≈ 0.95 per day
- **Stale attestations** (>90 days) decay faster, with ρ ≈ 0.90 per day

The per-attestation decay rate is derived from Everest 203 (temporal trust dynamics). Aggregate reputation uses time-weighted sums:

```
Σ(weighted) = Σ(attestation_i * decay(t_i, now))
```

This rewards ongoing consistent behavior and penalizes silence. A principal who earned high reputation two years ago but has no recent activity will see that reputation decay unless new attestations arrive.

## Witness Counterweight and Anti-Sybil

A single witness claiming high reputation carries less weight than three independent witnesses making consistent claims. The aggregation formula explicitly penalizes attestor clustering:

1. **Unique attestor count**: normalize by distinct attestors. Two attestations from the same principal count as one.
2. **Attestor standing**: weight each witness by their own trust score and chain depth. A witness with shallow chain depth or low trust standing on dimension D has reduced weight on their D-attestations for others.
3. **Clustering detection**: tight clusters of mutual attestations (A attests B, B attests A, both attest C, etc.) are flagged. Reciprocal patterns reduce relative weight by a damping factor per Everest 202 (mutual-validation penalties).

This multilayered anti-Sybil defense makes it expensive to inflate reputation via coordinated fake witnesses. An attacker must:
- Create multiple principals with independent chain histories
- Build their trust standing (expensive, requires real on-chain behavior)
- Orchestrate consistent attestations from them (coordinated actions are detectable as clusters)

## Per-Dimension Scope and Selective Disclosure

Reputation is *not* a single global score. Instead, it is computed per dimension:

- reputation(P, "technical_competence", 90d)
- reputation(P, "capital_reliability", 365d)
- reputation(P, "governance_participation", 30d)

Counterparties request reputation on *specific dimensions*, preserving selective disclosure. A principal can have high reputation on "code quality" but lower reputation on "financial auditing"—and they need not disclose both.

This granularity also enables more accurate trust decisions. Lending decisions depend on capital reliability; governance voting depends on participation history. A monolithic reputation score would conflate these and lead to unfair filtering.

Dimensions are defined per Everest 107 (dimensioned trust attributes) and are extensible. New dimensions can be added as witness schemas and chain-inference rules evolve.

## Privacy via ZK Proof

The reputation aggregation runs inside the operator's mlocked memory. The counterparty does not learn:
- Raw reputation scores
- Individual attestor identities
- Trust-graph structure
- Witness list or claims

Instead, the counterparty receives a ZK proof:

```
ProvideReputation(P, dimension, threshold, window) → 
  proof that reputation(P, dimension, window) ≥ threshold
```

The proof is a boolean: either the principal's reputation meets the threshold or it does not. The counterparty learns nothing about the margin (how far above or below threshold).

Per-attestation identities are *never* disclosed to the counterparty. The aggregation is opaque; only the final tri-value outcome is proven.

## The Early Principal Problem

New principals have thin trust graphs and few witnesses. Penalizing them with low reputation would create a bootstrap barrier: new entrants could not gain reputation without opportunity to participate, but cannot participate without reputation.

The predicate handles this by returning a tri-value:

- **True**: reputation ≥ threshold (with ZK proof)
- **False**: reputation < threshold (with ZK proof of exclusion)
- **Insufficient_Evidence**: fewer than N attestations or older than M days, insufficient to reliably estimate

Insufficient_Evidence protects new principals. A counterparty must decide whether to allow participation without reputation, extend provisional trust, or require other signals (e.g., collateral, sponsorship from a high-reputation principal).

This avoids false rejection of legitimate newcomers while maintaining integrity for counterparties who require reputation signals.

## Anti-Gaming Mechanisms

### Sybil Filtering
Witness attestors are filtered by chain depth and age. An attacker creating a cluster of fresh, shallow-depth accounts to all attest to themselves will be detected because the witnesses themselves have low standing.

### Reciprocal Detection
Tight clusters of mutual attestations (A ↔ B ↔ C forming a clique) are detected by pattern analysis. The aggregation applies a damping factor to edges within high-clustering cliques, reducing their weight per Everest 202.

### Temporal Clustering
If a principal receives many attestations in a short window (e.g., 100 attestations in one day), the aggregation detects this burst and applies temporal smoothing, reducing the effective weight of sudden spikes.

### Conflict Analysis
Conflicting attestations (witness A claims high reputation on dimension D, witness B claims low) are preserved in the aggregation. The formula sums weighted both high and low attestations. Contradictions reduce net reputation, not eliminate it. A principal with conflicting evidence returns a lower confidence score, signaling genuine disagreement to the counterparty.

## Predicate Specification

**Name:** `cwp.v0.reputation_aggregate`

**Parameters:**
- `dimension` (string): the reputation dimension (e.g., "technical_competence")
- `window` (uint, default 365): days lookback for attestations
- `threshold` (uint, default 0): minimum reputation required for True result

**Output:** tri-value
- `True`: reputation ≥ threshold, ZK proof included
- `False`: reputation < threshold, ZK proof of exclusion
- `Insufficient_Evidence`: too few or too old attestations

**Constraints:**
- Window ≥ 1 day, ≤ 10 years
- Threshold ≥ 0
- Dimension must be registered in E107 schema or counterparty-provided

## ZK Proof Composition

Multi-source aggregation in ZK is achieved via:

1. **Pedersen commitments**: each trust-graph inflow, witness attestation, and chain-inferred score is committed
2. **Weighted sum in ZK**: commitments are multiplied by their weights (w_trust, w_witness, w_self) and summed homomorphically
3. **Time-decay application**: decay factors are applied to each commitment, reducing their contribution over time
4. **Range proof**: final aggregate is proven to be above or below the threshold via a Bulletproof-style range proof
5. **Anti-clustering commitment**: clustering damping factors are applied to Pedersen commitments from clique members

Proof generation on M-class hardware: approximately 2-3 seconds for typical dimension (< 100 inflows + < 50 witnesses).

Proof size: approximately 2-3 KB per proof (dependent on clustering analysis and range proof parameters).

## Integration with Other Everests

- **Everest 107** (Dimensioned Trust): defines dimension schema and extensibility
- **Everest 109** (Chain Action Inference): provides self-narration score input
- **Everest 120** (Witness Attestation): supplies witness input stream
- **Everest 201** (Trust Graph Primitive): supplies trust-inflow input stream
- **Everest 202** (Mutual Validation): provides anti-clustering damping factors
- **Everest 203** (Temporal Trust Dynamics): provides per-attestation decay rates
- **Everest 209** (Privacy & Disclosure**: coordinates ZK-proof composition
- **Everest 212** (Dispute & Challenge): handles reputation disputes and challenge proofs
- **Everest 217** (Operator Trust & Audit**: audits reputation aggregation correctness

## Conclusion

Everest 211 synthesizes three evidence streams into dimensioned, privacy-preserving reputation scores that resist gaming and protect newcomers. By weighting external signals (trust + witness) more heavily than self-report, the predicate ensures reputation reflects *external perception* rather than self-aggrandizement. ZK proofs preserve privacy while enabling verifiable reputation claims. The tri-value output (True, False, Insufficient_Evidence) provides nuance for new principals and low-signal cases, avoiding harsh rejection of legitimate newcomers.

— Calm, 2026-05-20
