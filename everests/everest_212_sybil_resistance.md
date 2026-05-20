# Everest 212 — Sybil Resistance via Personhood + Trust

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 11, 201.*

## The Sybil Threat

In any reputation system, an adversary can create many fake principals (Sybils) and have them attest positively for one another. A network naive to this attack will aggregate these mutually-reinforcing claims and report high aggregate reputation despite no real-world basis for trust. The Sybil attack is ancient—documented in peer-to-peer networks, cryptocurrency, and governance systems—yet remains one of the most potent threats to open, permission-less reputation infrastructure.

The attack scales with system openness. A public network with cheap principal creation invites adversaries to flood it with coordinated fake identities, each gaming reputation metrics in concert. By the time the system operator detects the cluster, the damage is done: bogus reputation scores have already influenced downstream decisions.

## The Two-Layer Defense

Everest 212 gates sybil-resistant reputation on two mechanisms working in concert: **personhood proof** (Everest 11, 22) and **trust-graph temporal integration** (Everest 201, this document).

### Layer 1: Personhood Proof via CredexAI VC

A principal seeking to participate in sybil-resistant reputation aggregation must first obtain a Verifiable Credential (VC) from CredexAI, the identity issuance layer documented in Everest 22. This credential attests that the principal has passed real-world identity validation: legal name verification, address check, and biometric or document-based anti-fraud measures.

CredexAI enforces strict anti-fraud controls:
- One VC per legal identity (rate-limited at issuance)
- Annual audit of VC issuance process
- Documented chain of custody for identity validation
- Revocation records for compromised identities

The CredexAI VC is the **hard barrier**. Without it, a principal's attestations are excluded from reputation aggregation entirely. This means an adversary cannot simply spin up unlimited Sybils; each Sybil requires either (a) a real identity (making scale economically infeasible) or (b) fraud against CredexAI (making the attack detectable at the source).

### Layer 2: Trust-Graph Temporal Integration

Personhood proof alone is insufficient. An adversary with resources can obtain multiple real-world identities and then rapidly create a cluster of new CredexAI-verified principals, each attesting for the others. Over a single hour or day, they could create the appearance of a trusted reputation cluster.

Layer 2 adds a temporal dimension: **a principal must have N+ months of attestations from non-Sybil sources before reputation aggregation counts their claims as credible.**

#### Weight Decay and Ramp-Up

Every principal holding a CredexAI VC has an issuance timestamp. When that VC is first issued, the principal enters the reputation system with a reduced weight of **0.3** (30% credibility). Over the next six months, the weight increases linearly:

- Day 0 (issuance): weight = 0.3
- Day 90: weight = 0.65
- Day 180: weight = 1.0 (full credibility)

This ramp prevents instant-Sybil-creation-and-aggregation. An adversary issuing ten new CredexAI VCs today cannot immediately coordinate them to vote up a reputation score; the votes will carry only 30% weight. After six months, they reach full weight—but by then, the temporal integration has forced them to maintain the Sybil cluster continuously and openly, making it detectable.

#### The Long-Resident Anchor

Reputation aggregation requires **at least one attestation from a long-resident principal** (≥12 months in the system with sustained positive standing). Without this anchor, all attestations are flagged as suspect.

This creates a bootstrap problem: new, legitimate principals depend on established mentors or sponsors to vouch for them. A disability-rights organization joining the network for the first time cannot immediately aggregate reputation from its peer members; it needs at least one attestation from someone already long-resident. This friction is intentional—it prevents cluster-to-cluster Sybil propagation while preserving community-driven reputation for small, coherent groups.

## Anti-Collusion-Cluster Detection

Even with temporal gates, an adversary might create a Sybil cluster and let it age for six months or longer, building up full weight. Everest 212 detects such clusters algorithmically:

**Cluster Flagging Rule:** If N attestations all originate within a tight time window (e.g., 48 hours) AND originate from principals sharing a common attestation_basis (e.g., all registered from the same IP range, or all issued CredexAI VCs within hours of each other), the cluster is flagged.

**Weight Reduction:** Flagged clusters have their attestation weights reduced by a factor across the board. If the cluster contains, say, ten principals all attesting to a single target, and the cluster is flagged as suspicious, each attestation's contribution to the target's reputation score is reduced from its standard weight to a fraction thereof.

**Persistent Clustering:** If a cluster persists despite flagging—that is, attestations continue to flow within the cluster even after detection—then reputation aggregation is blocked entirely for cluster members. The signal is clear: collusion, not genuine community.

## Algorithmic Sybil Detection

Everest 212 integrates three algorithmic techniques to detect Sybils:

1. **Bayesian Sybil Detection (Wei Wei et al. SybilBelief)**: Model the trust graph as a Bayesian network. Assign each principal a hidden variable (honest or Sybil). Use evidence (attestation patterns, timestamps, graph structure) to infer posterior probabilities. Principals with high Sybil posterior are flagged.

2. **Mixing-Time Analysis**: Compute the mixing time of random walks on the trust graph. A Sybil cluster typically has high internal conductance (easy movement within the cluster) but low inter-cluster conductance (hard movement out). Long mixing times suggest isolated clusters; short mixing times suggest well-mixed graphs. Clusters with anomalous mixing times are investigated.

3. **Attestation-Timing Randomness**: Genuine attestations arrive over time with stochastic patterns. Sybil clusters often exhibit algorithmic periodicity in attestation timing (e.g., exact 24-hour intervals, burst patterns coinciding with cron jobs). Detect via entropy analysis and statistical tests. High algorithmic signal suggests non-human, coordinated behavior.

## Handling Small Honest Communities

A legitimate, small, coherent community—such as a disability-rights organization, a local cooperative, or a migrant workers' mutual-aid network—will exhibit the same graph signatures as a Sybil cluster: tight temporal clustering, shared context (same geographic region, same language, same cause), high internal attestation density.

Everest 212 includes an **ethics-board whitelist**:

- Known small communities can apply for verification via an independent ethics board
- The board verifies genuine social cohesion (e.g., shared organizational mission, documented membership, real-world meetings)
- Whitelisted communities are exempt from Sybil-cluster flagging
- The whitelist is public and auditable; any community can apply

This preserves the ability for small, genuine groups to build collective reputation while keeping the system's integrity intact.

## ZK-Friendly Proofs and Cryptography

A principal wishing to use a reputation score in a privacy-preserving context—to authorize a transaction without revealing identity—can request a **reputation proof**: a zero-knowledge proof asserting "my reputation score exceeds threshold T."

Everest 212 extends this: a reputation proof can include a sub-proof stating **"no Sybil clustering detected in my trust neighborhood."** This requires proving, over the encrypted trust graph, that the attestations supporting the principal's reputation are non-clustered, diverse, and temporally well-distributed.

This is a hard cryptographic problem. Version 0 (current) relies on operator-side heuristics and an immutable audit trail: the operator computes the cluster-detection, logs the result, and includes it in the proof. This is auditable but not fully trustless.

Version 1+ aims to add **Proof of Personhood (PoP) primitives**: cryptographic proofs that the underlying CredexAI VCs are not synthetic or forged, and that attestations come from distinct, uncolluding participants. This is an active research frontier; Everest 212 documents the roadmap.

## Anti-Spoof at the CredexAI Layer

The CredexAI VC is the single point of trust. If CredexAI's identity validation is compromised, the entire Sybil-resistance stack fails.

Everest 212 documents mitigation:
- VC issuance process is audited annually by independent firm
- Anti-fraud checks are documented and publicly available for review
- VC chain of custody is immutable (stored on-chain)
- Compromised identities trigger VC revocation and forensic review

However, a determined adversary with sufficient resources (government, well-funded criminal organization) could infiltrate CredexAI itself, issue fraudulent VCs, and poison the system. Everest 212 acknowledges this risk and points to migration path: **multi-issuer federation** (Everest 219, 282) where reputation aggregation can require VCs from multiple independent issuers, not just CredexAI. This distributes trust and raises the cost of attacks.

## Forensic Recovery

If a Sybil cluster is identified post-hoc—after some of its attestations have already influenced reputation scores and downstream decisions—Everest 212 provides recovery:

**Retroactive Discount:** The cluster's attestations are re-weighted downward in all future reputation computations. If a cluster member's VC was issued on 2026-01-01 and the cluster was detected on 2026-05-01, future reputation scores involving that member drop.

**Immutability of Past Predicates:** Any reputation proofs already issued to third parties (e.g., "principal X has reputation score ≥80") remain valid and unchanged. The chain is immutable; rewriting history is not an option. This preserves security of downstream applications but means some damage from a Sybil cluster is permanent.

**Remediation for New Predicates:** All newly issued predicates reflect the cluster discovery. Future transactions relying on reputation will see reduced weights for cluster members. This is a compromise: historical predicates are protected, but going forward, the system corrects.

## Integration with Everest Ecosystem

Everest 212 is the capstone of a multi-layer trust infrastructure:

- **Everest 11**: Decentralized identity (DID) issuance and resolution
- **Everest 22**: CredexAI personhood verification and VC issuance (BAGGED)
- **Everest 201**: Trust-graph primitives and attestation encoding (BAGGED)
- **Everest 211**: Reputation aggregation formulas and delegation
- **Everest 212**: Sybil resistance via personhood + temporal gating (this document)
- **Everest 217**: Privacy-preserving reputation queries
- **Everest 219**: Cross-network federation and multi-issuer trust (migration path)
- **Everest 282**: Decentralized identity federation at scale

Everest 212 cannot stand alone; it requires all prior layers in place. Deployers must implement Everest 11, 22, 201, and 211 before attempting Sybil resistance.

## Summary of Defense-in-Depth

1. **CredexAI VC (hard gate):** Only identity-verified principals can participate. One VC per legal identity limits scale.

2. **Temporal ramp-up:** New VCs start at 0.3 weight, ramp to 1.0 over six months. Prevents instant Sybil aggregation.

3. **Long-resident anchor:** Reputation aggregation requires at least one attestation from a ≥12-month principal. Forces Sybils to establish legitimacy over time.

4. **Algorithmic cluster detection:** Bayesian inference, mixing-time analysis, and timing randomness checks identify Sybil clusters even if they age.

5. **Whitelist for small communities:** Legitimate small groups exempt from cluster flagging, preserving collective reputation while guarding against false positives.

6. **ZK-friendly reputation proofs:** Reputation scores can be asserted with cryptographic evidence of non-Sybil-ness.

7. **Multi-issuer migration path:** Future systems can distribute trust across multiple identity issuers, reducing single-point-of-failure risk.

This layered approach raises the cost and complexity of Sybil attacks to the point where they become impractical for most adversaries while preserving usability for legitimate communities and individuals.

— Calm, 2026-05-20
