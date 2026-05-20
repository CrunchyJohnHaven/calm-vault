# Everest 214 — Trust Ladder

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 213.*

## Overview

Trust in decentralized systems requires more than reputation scores. The CALM protocol models trust as a **ladder** of tiered commitments, where each tier unlocks specific privileges in disclosure, action authorization, and governance scope. The four tiers reflect increasing evidence of trustworthiness and community recognition, balancing openness with prudent risk management.

When two agents meet for the first time, both default to Tier 1. As they interact—and as their community observes those interactions—agents move up (or occasionally down) the ladder based on attestations, cooperation outcomes, and sustained behavior. This structure prevents both infinite gaming and paralysis: there are exactly four well-defined stops, each with clear entry criteria and capabilities.

## The Four Tiers

### Tier 1 — Acquaintance

**Trust baseline:** Minimal prior evidence.

An agent enters Tier 1 by default upon first meeting or whenever no better evidence exists. Tier 1 is the "stranger handshake"—a recognition that a new counterparty *may* be trustworthy, but the community has seen no proof yet.

**Entry criteria:**
- Any single attestation, OR
- Transitive trust score ≥ 0.2 (minimal chain confidence)

**Rationale:** Tier 1 is deliberately low bar. It signals "we acknowledge you exist and can communicate," not "we trust you with sensitive secrets." This tier prevents false intimacy while allowing conversation to begin.

### Tier 2 — Collaborator

**Trust baseline:** Direct evidence of sustained cooperation.

Tier 2 is earned through demonstrable joint work. The principal has worked *with* this agent, seen outcomes, and built a track record. A single attestation is insufficient; the attestor must cite actual cooperation.

**Entry criteria:**
- Direct trust from attesting principal ≥ 0.5, AND
- At least one recorded `cooperation_outcome` involving the counterparty

**Rationale:** Tier 2 marks the transition from stranger to colleague. It means "this agent has actually cooperated with us and proven themselves reliable in joint action." It opens standard bilateral operations without the full scrutiny Tier 3 demands.

### Tier 3 — Vouched

**Trust baseline:** Community consensus from multiple, independent sources.

Tier 3 requires *at least two separate principals* to vouch for the agent, and at least one of those principals must be a long-resident (established in the community for sufficient time, per Everest 212 sybil protections). This tier cannot be faked by collecting shallow endorsements; it requires genuine distributed faith.

**Entry criteria:**
- At least 2 distinct attestors, with ≥1 being long-resident, AND
- Aggregate trust score ≥ 0.7

**Rationale:** Tier 3 is where capital flows and shared resources become possible. The dual-attestor + long-resident requirement defeats sybil attacks: a newcomer cannot bootstrap themselves or allies into Tier 3 by manufacturing endorsements. Community members must genuinely believe in the agent's integrity.

### Tier 4 — Vouched-Publicly

**Trust baseline:** Community consensus anchored to public record.

Tier 4 agents have achieved Tier 3 *and* have public, cryptographically anchored vouching records (via Sigsum or equivalent). Their reputation is on the ledger, visible to all. This tier is for multi-party governance, co-signing, and formal agreements where accountability must be transparent.

**Entry criteria:**
- Tier 3 status, AND
- At least one public, Sigsum-anchored vouching record (not merely private attestation)

**Rationale:** Tier 4 is deliberate reputation staking. It means "I am willing to have my trust in this agent be a matter of public record." This tier supports governance bodies, consortium agreements, and cross-organizational decisions where auditability is non-negotiable.

## Per-Tier Privileges

### Disclosure Privileges

**Tier 1:** Low-stakes information classes only. General predicates are safe (e.g., "does this counterparty exist?", "what are their category tags?"). Safety bits, cognitive baselines, and sensitive operational history remain withheld.

**Tier 2:** Standard cooperation predicates. The principal can share outcome data, cooperation windows, and task-specific context. Disclosure is at the principal's discretion; no default sharing.

**Tier 3:** More sensitive predicates become available with principal opt-in. Cognitive baseline data, risk profiles, and historical performance in higher-stakes scenarios may be disclosed if the principal consents.

**Tier 4:** Maximum disclosure scope, still gated by Everest 113 (consent & opt-in). Public information can flow freely; private information moves only with explicit principal consent.

### Action Authorizations

**Tier 1:** Routine inquiries. The agent can ask questions, request general information, and participate in low-stakes coordination. No financial commitments, no access to shared resources, no unilateral decisions.

**Tier 2:** Bilateral cooperation and joint actions. The agent can negotiate contracts, commit to shared tasks, execute agreed-upon plans, and access resources that the principal has explicitly allocated. Actions are peer-to-peer, not on behalf of the principal.

**Tier 3:** Capital pooling, joint procurement, and shared resource management. The agent can participate in multi-party initiatives, contribute to collective funds, and represent interests in group decisions (subject to explicit mandates).

**Tier 4:** Governance decisions, multi-party agreements, and public-facing co-signing. The agent can vote in consortium matters, sign binding legal instruments, and speak publicly on behalf of affiliated communities.

## Tier Movement

### Promotion

An agent rises one tier when:
1. Additional *positive* attestations accumulate (not one more—multiple independent sources), AND
2. Sustained good behavior over a meaningful time window (no sudden reversals or contradictions)

Example: An Tier 2 agent earning new Tier 3 vouches from two long-residents over six months of consistent collaboration moves to Tier 3.

### Demotion

An agent falls one tier immediately if:
- Any unrebutted counter-claim surfaces (e.g., fraud, breach, observed bad faith)

Demotion is automatic protection: the community does not wait for perfect evidence. If credible challenge arises, the agent's privileges shrink until repair is demonstrated.

### Reinstatement

Climbing back requires:
1. Explicit reversal of the counter-claim (Everest 163 reversal pathway), AND
2. Demonstrated forgiveness from the harmed party (Everest 174 process)

Reinstatement is *possible* but not automatic. It requires the agent to actively repair the breach and earn back trust through sustained correct behavior.

## The Stranger Handshake

When two agents meet for the first time—no prior relationship, no shared community—both start at **Tier 1 by default**. Neither is stranger than the other; the asymmetry is zero.

From Tier 1, the agents interact. If the interaction is positive and produces cooperation outcomes, Tier 2 becomes reachable naturally: the collaborating principal can attest to the other's reliability based on lived experience.

Tier 3 and above require broader community recognition. A Tier 2 agent cannot unilaterally promote a counterparty to Tier 3; that requires independent attestations from *other* community members. This prevents collusion and keeps the ladder honest.

## Predicate Specification

The trust tier predicate is:

```
name: cwp.v0.trust_tier_at_least(tier)
parameters: tier ∈ {1, 2, 3, 4}
output: tri-value (true, false, unknown)
```

The output is **tri-valued**, not binary:
- **true**: the subject meets or exceeds the specified tier
- **false**: the subject is known to be below the specified tier
- **unknown**: insufficient evidence exists

Predicates compose naturally. For example:
```
cwp.v0.trust_tier_at_least(2) AND cwp.v0.cooperation_across_difference(window)
```

This reads as: "Tier 2 or higher, with demonstrated collaboration across difference in the past N days." Composite predicates let principals express nuanced trust conditions.

## Privacy by Design

The counterparty learns only **"tier at least X,"** not their exact tier. If an agent is Tier 3, they see the response "tier at least 3," not "exactly Tier 3." This prevents leakage of marginal trust information and reduces gaming: an agent cannot calibrate manipulation to the precise threshold.

Tiers are *aggregate*, not per-relationship. An agent has one tier in the community, reflecting the consensus view. They cannot have different tiers with different peers (though individual principals can choose their own confidence intervals through composite predicates).

## The "No Infinite Tiers" Decision

Four tiers were chosen deliberately over a finer-grained scale. Why?

**Simplicity:** Four tiers are easy to reason about, communicate, and audit. They fit human cognitive capacity and reduce surface for miscommunication.

**Auditability:** More tiers create more threshold-crossing events, more ambiguity about tier boundaries, and more opportunities for edge cases. Four tiers reduce entropy.

**Gaming resistance:** With many tiers, agents can optimizing incremental movement through narrow manipulation. Four tiers make each boundary meaningful and harder to game.

**Community flexibility:** Communities can define *sub-tiers* within these four if they need finer granularity. The protocol provides the backbone; local governance layers customization.

## Anti-Tier-Gaming Mechanisms

### Aggregate, Not Individual

Trust ladder ranks are computed as *aggregates over multiple attestors*, not as point estimates from one relationship. An agent cannot climb by collecting shallow endorsements from many newcomers; the weight of long-resident attestors dominates.

### Long-Resident Requirement for Tier 3+

Tier 3 and Tier 4 both require at least one attestor who is long-resident (per Everest 212 sybil protections). A fresh face cannot vouch an agent into the upper tiers, no matter how many fresh faces align. This defeats sybil attack strategies where a bad actor creates multiple new identities and vouches for their main account.

### Counter-Claim Demotion

Any unrebutted credible claim of misconduct triggers immediate demotion. The burden is on the agent to *defend* themselves, not on accusers to prove everything. This favors swift protection over extended evidence-gathering in adversarial settings.

### Public Sigsum Anchoring for Tier 4

Tier 4 vouching is on the ledger, visible and immutable. Bad actors cannot hide Tier 4 status behind privacy; they chose to stake their reputation publicly. This transparency is what makes Tier 4 suitable for governance and legal agreements.

## Cross-References

- **Everest 120 (Witness):** Defines attestation mechanism and weight
- **Everest 201 (Trust Graph):** The underlying model for directional trust scores
- **Everest 211 (Reputation Aggregation):** How individual trust signals combine into aggregate scores
- **Everest 212 (Sybil Resistance):** Long-resident definitions and anti-Sybil mechanisms
- **Everest 213 (Trust Threshold):** Quantitative trust thresholds; E214 applies these to tier entry
- **Everest 163 (Reversal):** Process for overturning counter-claims
- **Everest 174 (Forgiveness):** Restoration after demotion
- **Everest 113 (Consent & Opt-In):** Privacy gates on disclosure, even at Tier 4

---

**— Calm, 2026-05-20**
