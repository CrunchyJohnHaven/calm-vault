# Everest 93 — Sigsum Operator Selection

*Phase VIII — Governance & Scale. Prereq: Everest 30.*

## Overview

Everest 93 establishes the operator selection process and governance framework for Calm Witness chain head publication through independent Sigsum transparency logs. This everest defines the minimum viable set of operators required to achieve quorum protection, the criteria by which operators are evaluated, and the operational commitments they must honor to remain in the ecosystem.

The acceptance criterion is clear: at least three independently operated Sigsum witnesses must commit to publishing Calm Witness chain heads. This threshold provides defense-in-depth against corruption by requiring an attacker to compromise consensus across organizational boundaries and jurisdictions.

## Target: Three Independent Sigsum Log Operators

The v0 deployment targets a minimum of three operators with distinct organizational sponsorship and geographic footprint:

1. **Calm-operated Sigsum log** (sigsum.calm.thecreativitymachine.ai) — serves as the sovereignty anchor, ensuring the Calm Witness ecosystem maintains independent publication capability. This log is funded and operated by Creativity Machine LLC.

2. **Sigsum demo log** — operated by the Sigsum project itself, this instance serves as the community anchor and lowers barriers to entry for vault operators integrating Calm Witness. Its public-domain status and transparent operations provide a model for trustworthiness.

3. **Glasklar Teknik** — as the primary sponsor organization of the Sigsum project, Glasklar represents the institutional anchor. Their operational maturity and long-term commitment to transparency infrastructure provide continuity and credibility.

An aspirational fourth candidate is the NIST-operated transparency log, positioned as a government anchor that would accelerate U.S. federal adoption. This candidate is not required for v0 acceptance but represents a strategic future addition.

## Selection Criteria

Candidate operators must meet five core criteria before inclusion in the chain head publication quorum:

### Geographic Distribution
At least two distinct jurisdictions must be represented among the three selected operators. This prevents concentration of regulatory or geopolitical risk and ensures that no single nation's authorities can compel all logs simultaneously to misbehave or go offline. The current candidate pool satisfies this: Calm's U.S. presence, Sigsum project's mixed (international) footprint, and Glasklar's Swedish jurisdiction cover distinct regulatory domains.

### Organizational Independence
No two selected operators may share a parent organization or primary funder. This independence requirement prevents a single entity from controlling multiple logs and thereby circumventing quorum protections. Shared corporate ownership, government agency sponsorship, or substantial financial dependency violates this criterion. The three candidates are independently governed and funded.

### Operational Maturity
Each operator must have demonstrated at least six months of continuous transparency log operations with verified uptime (minimum 99% availability per calendar month). This threshold filters out experimental or pilot deployments and ensures operational muscle memory. Uptime must be publicly verifiable through published monitoring dashboards.

### Witness Cosignature Support
The operator must fully implement the Sigsum witness protocol, including the ability to cosign tree heads with tight latency (sub-24-hour SLO) and publish cosignatures in a format that allows third parties to verify inclusion. Partial implementations or custom fork deployments do not qualify.

### Open-Source Operator Stack
The log operator must deploy and maintain a fully open-source stack for production operations. This enables independent audit, root-cause analysis of incidents, and verification that the operator is not running undisclosed proprietary logic that could mask misbehavior. Source availability is a prerequisite for trustworthiness.

## Selection Process

The selection process is deliberately transparent and open to encourage competition and prevent capture:

1. **Open RFP** via the calm-witness-predicates GitHub repository invites candidate operators to submit expressions of interest. The RFP outlines all five criteria and the commitment expectations below.

2. **Public Commitment Period** of 60 days allows operators to submit proposals, ask clarifying questions, and engage with the community. This window also allows existing operators to demonstrate compliance with criteria through deployed evidence (uptime dashboards, protocol tests, etc.).

3. **Maintainer Review** evaluates proposals against the stated criteria. The maintainer review is public and posted as issues/discussions to allow community feedback.

4. **Public Announcement** of selected operators includes signed commitments from each operator and a summary of how they satisfied each criterion.

The entire process is conducted in the public repository to ensure that no operator is selected based on informal back-channel agreement or undisclosed relationships.

## Operator Commitments

Operators selected for the v0 quorum assume four operational commitments:

### Witness Cosignature SLO
The operator commits to cosign new Calm Witness chain heads with a service-level objective of less than 24 hours. This SLO ensures that vault proofs can be rotated quickly and that age-based revocation is responsive. Failures to meet the SLO are logged and publicly reported by vault operators that depend on the log.

### Public Monitoring Data
The operator publishes real-time or near-real-time dashboards showing tree size, cosignature latency, and uptime. These metrics are available to any third party and serve as early warning signals if the operator begins to degrade. The dashboard data is exempt from confidentiality claims and must remain accessible.

### Transparency for Maintenance and Incidents
The operator maintains a public issue tracker or mailing list where scheduled maintenance windows, security incidents, and protocol updates are announced with reasonable notice (minimum 7 days for routine maintenance, immediate disclosure for security issues). This allows vault operators to adjust their quorum policies or select alternative logs if an operator enters a high-risk window.

### Third-Party Audit
The operator consents to independent audit of its operational logs, certificate issuance, and tree-head consistency, conducted with reasonable notice (minimum 14 days for non-emergency audits). This audit right is nondelegable and applies to the full stack (hardware, software, networking, key management).

## Quorum Policy

The default quorum policy is **2-of-3 inclusion**: a chain head is considered well-witnessed if at least two of the three selected operators have published a cosignature. This design allows for a single operator outage or misbehavior without breaking the chain, while still requiring consensus across independent operators.

Quorum policies are adjustable on a per-principal basis. Vault operators managing high-stakes secrets (long-lived keys, HSMs, state machines) may elect to require **3-of-3 inclusion**, accepting the risk that a single operator outage causes chain stalling. Conversely, low-stakes vault operators may accept **any-of-3** inclusion, with the understanding that this degrades to weakest-link security (i.e., a vault is only as trustworthy as its least-secure operator).

## Failure Handling

Two failure modes require distinct handling:

**Operator Offline**: If an operator becomes unavailable (network outage, hardware failure, unplanned downtime), a principal may elect to add a replacement log to the quorum to restore redundancy. The original operator's prior signatures and tree heads remain part of the immutable chain; the operator is not retroactively removed, only replaced for future cosignatures.

**Operator Misbehavior**: If an operator is demonstrated to have published false tree heads, claimed inclusion of records that were not present, or exhibited split-view behavior (different clients see different trees), the operator is immediately removed from the quorum. A full audit of the operator's historical data is published to allow vault operators to assess contamination risk. Removal is not reversible for v0; only a subsequent everest can restore an operator after misbehavior.

## Funding Model

**v0 Funding**: Creativity Machine LLC funds the complete operational cost of the Calm-operated log (sigsum.calm.thecreativitymachine.ai) and contributes a modest operational subsidy to the Sigsum demo log and Glasklar's Sigsum operations. This ensures all three operators can sustain operations without extracting fees from vault operators.

**v1+ Funding**: Long-term sustainability is achieved through a transparent foundation or consortium structure that distributes operational costs across multiple stakeholders (vault operators, transparency enthusiasts, security researchers). The goal is to decouple operator incentives from any single commercial entity.

## Long-Term Roadmap

v0 is intentionally minimal: three operators provide sufficient quorum diversity for launch. However, Calm Witness aspires to grow to at least five operators by v2.0, enabling tighter quorum policies (e.g., 3-of-5 or 4-of-5) that further reduce the blast radius of operator misbehavior or outage.

This multi-operator ecosystem also aligns Calm Witness with broader transparency infrastructure evolution, particularly NIST's work on federating transparency logs across government and industry sectors (Everest 91).

## Cross-References

- **Everest 30**: Chain head publication protocol (prerequisite)
- **Everest 33**: Corruption recovery using Sigsum inclusion proofs
- **Everest 91**: NIST transparency log federation strategy
- **Everest 94**: Roughtime selection for clock-synchrony witness (sibling everest)
- **Everest 96**: Post-quantum migration of Sigsum witness signatures

---

— Calm, 2026-05-20
