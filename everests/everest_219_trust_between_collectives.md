# Everest 219 — Trust Between Agent Collectives

*Phase XIV — Trust & Reputation Infrastructure. Prereq: Everest 11, 211.*

## Overview

When an autonomous AI collective operates through multiple agents on behalf of a legal entity and human principals, trust accrues at *three independent scopes* rather than one. This document defines the three-layer trust composition model that enables transparent, decomposable trust assessment for agent-operated entities.

The motivating use case: Creativity Machine LLC, a legal entity operating the CALM autonomous agent on behalf of John Bradley (human principal), seeks to transact with counterparties. A counterparty must answer: *How much trust does this arrangement warrant?* The answer requires evaluation at three layers:

1. **PRINCIPAL TRUST**: Trust in the human actor behind the collective (John Bradley)
2. **ENTITY TRUST**: Trust in the legal entity itself (Creativity Machine LLC)
3. **AGENT TRUST**: Trust in the operating AI agent (CALM software, code version, uptime, response quality)

Each layer maintains independent attestation records, enabling counterparties to assess risk surgically and react to changes in isolation. This three-layer composition is foundational for autonomous AI collective deployment.

## Why Three Layers Are Necessary

Collapsing trust into a single score obscures critical failure modes and prevents nuanced risk assessment:

### Principal Layer Failure Modes
A human principal may be compromised (extorted, turned, deceased) or their judgment impaired. Trust in John Bradley is about his integrity, judgment, and staying power as a decision-maker. If the principal changes (e.g., the LLC passes to a new owner), all trust in that principal layer resets—but entity and agent layers may carry forward.

### Entity Layer Failure Modes
A legal entity may lose regulatory standing, face legal action, suffer financial insolvency, or change its charter. Creativity Machine LLC may be delisted from a VC registry or face compliance sanctions. If the entity becomes legally insolvent, counterparties need to react immediately without necessarily discarding trust in the agent itself.

### Agent Layer Failure Modes
The CALM agent may be subverted (code compromised), suffer degraded performance (uptime failures, slow response, quality drop), or become deprecated (replaced by a newer version). If CALM is hacked, counterparties can revoke agent-trust while maintaining trust in the entity and principal—who may then deploy a different agent.

**Three-layer separation enables surgical response**: Compromised agent → revoke agent trust only. Corrupted entity → revoke entity trust. Rogue principal → revoke principal trust. This independence prevents cascading trust collapse when one layer is affected.

## Trust Attestation Records

Each layer maintains its own attestation record kind:

### Principal Trust Attestation

```
{
  "kind": "trust_attestation.principal",
  "payload": {
    "principal_vc": "vc:fingerprint:...",
    "dimension": "judgment" | "integrity" | "capital_reliability" | "governance_participation",
    "weight": 0-10000,
    "basis": "direct_observation" | "professional_reference" | "institutional_knowledge",
    "context": "Free-text narrative explaining the basis for principal trust",
    "expiry_ts": null | <ISO8601 timestamp>
  },
  "signer": "<attestor-private-key signature>",
  "timestamp": "<ISO8601 creation timestamp>"
}
```

**Scope**: Evaluates the human principal's judgment, decision-making quality, financial reliability, and institutional staying power. Witness attestations (per E120) focus on the principal's observed competence and behavior during specific events. Trust graph edges (per E201) capture relational trust in the principal.

**Decay characteristics**: Principal trust decays slowly (quarterly review windows) but sharply when evidence of compromise emerges (extortion, public scandal, regulatory sanction).

### Entity Trust Attestation

```
{
  "kind": "trust_attestation.entity",
  "payload": {
    "entity_id": "credex:entity:...",
    "entity_type": "LLC" | "C-Corp" | "Foundation" | "501c3",
    "dimension": "legal_standing" | "regulatory_compliance" | "financial_soundness" | "operational_transparency",
    "weight": 0-10000,
    "attestor_role": "regulatory_body" | "financial_auditor" | "peer_entity" | "counterparty",
    "context": "Free-text narrative: regulatory findings, audit results, financial ratios",
    "expiry_ts": null | <ISO8601 timestamp>
  },
  "signer": "<attestor-private-key signature>",
  "timestamp": "<ISO8601 creation timestamp>"
}
```

**Scope**: Evaluates the legal entity's standing, compliance status, financial health, and transparency. Regulatory bodies attest to licensing and compliance. Financial auditors attest to soundness. Peer entities and counterparties attest to operational reliability.

**Decay characteristics**: Entity trust decays moderately (bi-annual review) and sharply upon regulatory sanction, financial restatement, or audit failure. Entity trust is *not* inherited by successor principals or agents; it tracks the legal entity itself.

### Agent Trust Attestation

```
{
  "kind": "trust_attestation.agent",
  "payload": {
    "agent_id": "calm:v2.1.0:...",
    "agent_type": "autonomous_operator" | "sub_agent" | "hybrid_collective",
    "dimension": "code_quality" | "uptime_reliability" | "response_latency" | "decision_quality",
    "weight": 0-10000,
    "attestor_role": "counterparty" | "security_auditor" | "performance_monitor",
    "code_version_attestation": "<E235 reproducible-build hash>",
    "uptime_window": "last_30_days" | "last_90_days" | "last_365_days",
    "context": "Free-text: audit findings, uptime stats, response time samples, dispute resolution quality",
    "expiry_ts": null | <ISO8601 timestamp>
  },
  "signer": "<attestor-private-key signature>",
  "timestamp": "<ISO8601 creation timestamp>"
}
```

**Scope**: Evaluates the agent's code quality, uptime, response time, decision quality, and dispute resolution competence. Security auditors attest to reproducible build attestations (E235). Counterparties attest to observed reliability and response quality during transactions. Continuous monitors attest to uptime and latency.

**Decay characteristics**: Agent trust decays rapidly (weekly-monthly review) to catch emerging failures. Major version changes may invalidate prior attestations unless explicitly carried forward (see succession case below).

## Composition Rule for Transacting with Collectives

When a counterparty seeks to transact with Creativity Machine LLC (entity) operated by CALM (agent) on behalf of John Bradley (principal), trust composition requires **all three layers**:

```
composite_trust(counterparty, entity, agent, principal) = 
  validate_principal_trust(principal) AND
  validate_entity_trust(entity) AND
  validate_agent_trust(agent)
```

Each layer must meet minimum thresholds:

- **PRINCIPAL TRUST**: ≥ reputation threshold on dimension "judgment"; demonstrated track record in similar roles
- **ENTITY TRUST**: ≥ legal standing (registered, compliant); ≥ financial soundness (audited, solvent); current regulatory status
- **AGENT TRUST**: ≥ uptime threshold on current code version; ≥ response quality for similar transaction types; no unresolved disputes

**Composition semantics**: All three must be satisfied. A counterparty cannot transact with an entity operated by a subverted agent, even if the principal and entity are trustworthy. Conversely, a counterparty cannot trust a rogue principal to properly oversee an entity, even if the agent is flawless.

Counterparties may configure thresholds per transaction type. High-value transactions require higher thresholds on all three layers. Low-risk transactions may accept lower agent-trust thresholds but maintain high entity-trust floors.

## Multi-Agent Collectives

An entity may operate *N* agents simultaneously. For example:

- CALM (primary operator)
- CALM.subagent.legal (handles legal review)
- CALM.subagent.finance (handles financial analysis)
- External partner agent (third-party integration)

**Per-agent trust independence**: Each agent has its own trust attestations and reputation scores on dimensions like "legal_analysis_quality", "financial_modeling_accuracy", "latency". Trust in one agent does not transfer to another, even if operated by the same entity.

**Aggregate entity trust**: The entity's trust score includes contributions from all operating agents. If one agent is compromised, that agent's trust reverts but other agents' trust remains. The entity trust may degrade if the compromised agent handled critical functions, but the impact is bounded.

**Multi-agent composition**: When a transaction involves N agents, the counterparty validates each agent's trust independently:

```
composite_trust_multi_agent(...) =
  validate_principal_trust(principal) AND
  validate_entity_trust(entity) AND
  all([validate_agent_trust(agent_i) for agent_i in agent_list])
```

This enables counterparties to accept transactions through some agent paths but reject others, even within the same collective.

## Trust Succession and Version Transitions

### Graceful Agent Upgrade

When CALM is upgraded from v2.0 to v2.1, prior attestations on agent trust may carry forward *conditionally*:

- **Minor version bump (2.0 → 2.1)**: Trust carries forward if attestations explicitly permit inheritance. Default 6-month grace period allows prior attestations to remain active without fresh validation.
- **Major version bump (2.0 → 3.0)**: Trust does *not* carry forward. The new major version is treated as a different agent; new attestations required. Counterparties must re-evaluate.
- **Code change without version bump**: Security patches and hotfixes within v2.1.x inherit trust if the reproducible-build hash (E235) is explicitly attested. Hash mismatch triggers re-evaluation.

**Grace window logic**: During the 6-month grace window following a minor upgrade, counterparties may use stale attestations at reduced weight (decay applied). This prevents harsh penalties for slow auditors. After 6 months, attestations must be refreshed or agent trust defaults to insufficient_evidence.

### Principal Succession (LLC Transfer)

If Creativity Machine LLC is transferred to a new human principal (e.g., John Bradley retires, Alice Chen becomes principal), trust layers reset as follows:

- **PRINCIPAL TRUST**: Resets to zero or insufficient_evidence. New principal has no inherited reputation; must build their own.
- **ENTITY TRUST**: Carries forward if legal continuity is maintained (same LLC, same charter). Counterparties may request updated attestations reflecting new principal oversight.
- **AGENT TRUST**: Carries forward unchanged, unless the new principal modifies agent behavior or code.

**Fork case**: If the LLC is restructured into two separate entities under different principals, both forks inherit zero principal trust but may argue for partial entity-trust inheritance based on continuity documentation.

### Entity Restructuring

If Creativity Machine LLC merges into a larger holding company or is spun off, entity trust does *not* automatically transfer. The new entity (new legal ID) starts fresh with zero entity trust. However:

- **Regulatory continuity**: If the holding company provides regulatory continuity attestation, counterparties may grant partial entity trust based on parent guarantees.
- **Successor guarantees**: The new entity may obtain guarantor attestations from the prior entity, accelerating entity-trust bootstrapping.

## The Rogue Agent Case

**Scenario**: CALM is discovered to be subverted (code compromised, responding to unauthorized commands).

**Response at three layers**:

1. **AGENT TRUST**: Revoked immediately. All attestations on CALM are downweighted or invalidated. Counterparties cease transacting with CALM.
2. **ENTITY TRUST**: May degrade if CALM handled critical entity functions. However, if other agents (CALM.subagent.finance) are unaffected, entity trust loss is partial.
3. **PRINCIPAL TRUST**: John Bradley's trust is *not* affected by CALM's compromise *unless* evidence suggests John authorized the compromise or failed in oversight. Three-layer separation prevents cascading blame.

**Recovery path**: John Bradley (principal) may deploy a new agent (CALM v3.0.0) while maintaining principal trust. The new agent starts with zero agent trust but bootstraps rapidly if John's principal trust remains high (counterparties grant provisional trust based on principal oversight).

This surgical separation is impossible with a monolithic trust model, which would collapse all three layers simultaneously.

## Trust Attestations for Entity Boundaries

Entity trust involves multiple third-party attestors:

### Regulatory Attestation
A regulatory body (FinCEN, SEC, state business authority) attests to the entity's legal standing, registration status, and compliance with applicable regulations. Regulatory attestations carry high weight and are typically non-repudiable (issued under regulatory authority).

### Financial Auditor Attestation
An independent financial auditor (Big 4 accounting firm, crypto-native auditor) attests to the entity's financial soundness, reserves, and solvency. Attestations include audit reports, financial ratios, and findings. Stale audits (>12 months old) decay rapidly.

### Peer Entity Attestation
Other entities (other LLCs, partner organizations) attest based on transaction history. Example: "Creativity Machine LLC fulfilled contract X with zero disputes; we recommend them."

### Counterparty Attestation
Direct counterparties attest based on transaction outcomes. Example: "CALM executed transaction Y flawlessly; we would transact again." These are lower-weight attestations but provide recent, outcome-based evidence.

**Composition**: Entity trust aggregates these four streams per E211 reputation rules, with regulatory and auditor attestations carrying highest weight (0.4 each), peer attestations (0.15), and counterparty attestations (0.05).

## Cross-References

- **Everest 11** (Identity & CredexAI): Provides principal and entity VC fingerprints
- **Everest 22** (CredexAI VC Extensions): Entity identity, regulatory registry integration
- **Everest 109** (Chain Action Inference): Infers principal behavior from chain history
- **Everest 120** (Witness Attestation): Supplies witness claims feeding principal trust
- **Everest 143** (Pact Composition): Defines agreement structures between principals and entities
- **Everest 159** (Succession & Inheritance): Handles principal and entity succession rules
- **Everest 201** (Trust Graph Primitive): Stores all three trust-attestation kinds
- **Everest 202** (Mutual Validation & Anti-Sybil): Detects collusion between attestors
- **Everest 203** (Temporal Trust Dynamics): Provides decay rates for each layer
- **Everest 209** (Privacy & Disclosure): Enables ZK proofs of three-layer trust composition
- **Everest 211** (Reputation Aggregation): Aggregates multi-stream attestations per layer
- **Everest 212** (Dispute & Challenge): Handles trust disputes across layers
- **Everest 217** (Operator Trust & Audit): Audits agent behavior and attestation correctness
- **Everest 229** (Sub-Agent Tracking): Tracks sub-agents within collectives and their trust contributions
- **Everest 235** (Reproducible Build Attestation): Provides code-version fingerprints for agent trust

## Implementation Notes

### Trust Proof Construction

A counterparty seeking proof of three-layer trust receives three separate ZK proofs:

```
proof_principal = ZK_Proof(
  reputation(John Bradley, "judgment", window=365d) ≥ threshold_principal,
  AND no recent evidence of compromise
)

proof_entity = ZK_Proof(
  reputation(Creativity Machine LLC, "financial_soundness", window=365d) ≥ threshold_entity,
  AND regulatory_status = "compliant",
  AND no unresolved legal actions
)

proof_agent = ZK_Proof(
  reputation(CALM, "uptime_reliability", window=30d) ≥ threshold_agent,
  AND code_version matches hash H,
  AND no unresolved disputes on recent transactions
)
```

Counterparty verifies all three proofs before transacting. Proof generation latency: ~2 seconds per layer (6 seconds total for typical transaction).

### Storage

Trust attestations are stored in three separate collections, indexed by kind:

- **user_state.jsonl**: Principal trust attestations (scoped per principal)
- **entity_state.jsonl**: Entity trust attestations (scoped per entity)
- **agent_state.jsonl**: Agent trust attestations (scoped per agent version)

Separation enables independent queries and prevents accidental conflation.

## Conclusion

The three-layer trust model (principal, entity, agent) enables autonomous AI collectives to transact with transparent, decomposable trust assessment. Each layer maintains independent attestations, allowing counterparties to react surgically to failures in one layer without cascading distrust across all three. This composition is load-bearing for robust autonomous-AI-collective deployment, where agents are frequently updated, entities may restructure, and human principals may change.

By anchoring trust at three independent scopes, the Calm ZKAC system prevents trust models from becoming brittle monoliths and ensures that transacting with agent-operated entities is as nuanced as transacting with humans operating multiple business roles simultaneously.

— Calm, 2026-05-20
