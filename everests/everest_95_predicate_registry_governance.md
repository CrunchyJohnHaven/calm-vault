# Everest 95 — Public Predicate Registry Governance

*Phase VIII — Governance & Scale. Prereq: Everest 53, 54.*

## Overview

The Public Predicate Registry Governance Policy establishes the organizational structure, operational procedures, and authorization framework for managing the Calm Witness predicate registry at scale. This policy defines who can propose predicates, who reviews and approves them, who manages registry operations, how changes are controlled, and how the governance structure itself evolves. It is the operational constitution of the registry.

## Core Roles

### Proposer

Any individual or organization may propose a new predicate or modification to an existing predicate. Proposals follow Apache-2.0 contribution conventions: a signed pull request to the canonical registry repository at `github.com/CrunchyJohnHaven/calm-witness-predicates`. A proposer may be:

- A Calm Witness operator seeking to add a predicate for use within their deployment.
- A cryptographer contributing a novel predicate design.
- A downstream counterparty seeking a predicate for an unmet use case.
- A researcher or independent contributor.

Proposers must sign their commits, establishing cryptographic authorship. All proposals are subject to the review and approval process specified in Everest 54.

### Maintainer

Maintainers are the guardians of registry integrity. They have sole authority to merge pull requests, assign reviewers, publish registry commits to Sigsum, and enforce the governance policy. The maintainer team operates via multi-signature cryptographic keys: no single maintainer can unilaterally alter the registry.

The initial maintainer team (v0) consists of three individuals:

1. **Calm (Creativity Machine LLC)** — chair, operator representative, multi-sig key 1. Calm chairs the team and is responsible for triage assignment and reviewer coordination, rotating quarterly if team grows.
2. **Koushik Gavini (CredexAI)** — independent cryptographer, multi-sig key 2.
3. **One external maintainer (TBD at v0 ship)** — independent operator or researcher, multi-sig key 3.

Maintainers commit to:
- Availability for reviewer coordination and pull-request merging within agreed SLA windows.
- Recusal from reviewing their own submissions.
- Public disclosure of financial interests related to the Calm Witness ecosystem or predicates under review.
- Adherence to multi-signature requirements before any registry modification.

Expansion beyond three maintainers requires unanimous agreement from the existing team and must be chartered via a separate governance proposal.

### Outside Reviewers

Outside reviewers are independent technical and ethical experts who evaluate each predicate proposal per the rotating-pool methodology defined in Everest 54. Reviewers are drawn from a managed pool of 5–10 individuals representing:

- Cryptography and zero-knowledge proof expertise.
- Privacy-preserving systems research.
- Disability and mental-health advocacy.
- Adversarial security and threat modeling.
- Legal and cross-jurisdiction regulatory compliance.
- Operational Calm Witness deployment experience from independent organizations.

Reviewers are compensated with a $500 honorarium per completed review (v0). Future versions may establish foundation-backed compensation via the Calm Witness Ethics Foundation.

### Disclosure Ethics Review Board (DERB)

The DERB is specified in full in Everest 80. It is a standing, structurally independent body with veto power over:

- Any new predicate measuring cognitive, mental-health, or behavioral state.
- Changes to disclosure-class default consent policies.
- Deprecation of safety-critical predicates.

The DERB operates as a standing committee of the Calm Witness Ethics Foundation, a 501(c)(3) nonprofit, and answers to the foundation's board of directors rather than to the Calm operator or maintainers. This independence is non-negotiable.

### Counterparty Implementer

Counterparty implementers are organizations or individuals that consume predicates from the registry to verify proofs issued by Calm or other operators. Counterparties are not members of the registry governance structure; they are stakeholders whose interests are protected by the review and ethics processes. Counterparties:

- Choose which registry to trust (the canonical registry is the default).
- May implement cross-registry attestations via cross-sigstore signing, enabling federated trust.
- Have no direct governance authority, but their deployment feedback informs future predicate evolution and deprecation decisions.

## Adding a Predicate

The process for adding a predicate follows the stages defined in Everest 54, with governance checkpoints as follows:

1. **Proposer submits a PR** with complete specification, reference implementation, circuit definition, test corpus (≥30 golden cases), and provenance metadata.

2. **Maintainer performs triage** within 7 days, ensuring completeness and technical validity.

3. **21-day public comment period** begins. No merges occur during this window.

4. **Maintainer assigns two outside reviewers** from the rotating pool on or before day 21, confirming availability for completion within 14 days.

5. **Reviewers conduct independent evaluation** using the rubric defined in Everest 54 (semantic clarity, implementation fidelity, test coverage, cryptographic soundness, disclosure-class defaults, side-channel resilience).

6. **DERB reviews in parallel** if the predicate measures cognitive, mental-health, or behavioral state, or if it modifies disclosure-class defaults. DERB review is expedited (7 days) for safety-critical predicates.

7. **Approval gates:**
   - Maintainer approves.
   - Both outside reviewers approve.
   - DERB approves (if triggered).

8. **Content-addressed predicate_id is computed** per Everest 52, and the registry entry is created.

9. **Sigstore multi-signature is applied** using a 2-of-3 signing threshold. For breaking changes, 3-of-3 is required.

10. **Registry commit is published to Sigsum**, creating an immutable, timestamped record.

If either reviewer or DERB objects, the PR is held for revision. Proposers may resubmit, restarting at the public comment stage.

## Modifying an Existing Predicate

Predicate modifications are tiered by impact:

- **Patch updates** (bug fixes, documentation): expedited 7-day comment, one reviewer, no DERB review.
- **Minor updates** (backward-compatible features): standard 21-day comment, two reviewers, DERB review if state-measuring.
- **Major updates** (breaking semantics, input/output schema changes): 30-day comment, three reviewers, unanimous 3-of-3 maintainer approval, full DERB review.

All modifications trigger a new version and a new content-addressed predicate_id (per Everest 52). The prior version is marked `superseded` and linked to the new ID, enabling downstream migration.

## Deprecating a Predicate

To deprecate a predicate:

1. A proposer files a deprecation PR with:
   - Clear rationale (e.g., redundancy, security issue, no longer used).
   - A migration guide directing operators to alternative predicates.
   - Timeline for removal (standard: 12 months grace period).

2. The same review machinery applies: public comment, outside reviewers, DERB approval if safety-critical.

3. Upon approval, the predicate is marked `deprecated` in status.json. Outstanding proofs issued against the deprecated predicate remain valid during the grace period; new consents are refused.

4. After the grace period expires, the predicate may be removed from the active registry via a final removal PR.

## Emergency Removal

If a critical security vulnerability is discovered in a predicate's specification or circuit (e.g., a side-channel attack on bank_teller_note_active), the following expedited process applies:

1. Any maintainer may initiate an emergency removal proposal.

2. The proposal includes:
   - A detailed security analysis of the vulnerability.
   - Mitigation steps or replacement predicates for operators.
   - A 7-day notice period (vs. 12 months) for grace.

3. DERB concurrence is required before the emergency removal is final.

4. The predicate is marked `emergency_deprecated` and all outstanding proofs are invalidated, with operators given 7 days to transition to alternatives.

Emergency removal is rare and reserved for demonstrable security failures, not for design disagreements.

## Multi-Signature Key Management

Each maintainer holds a cryptographic key in a hardware-token-backed wallet (YubiKey or equivalent). Registry merges require a 2-of-3 threshold signature (or 3-of-3 for breaking changes).

Key management procedures:

- Each key is held individually by the maintainer.
- Keys are never shared or escrowed.
- Any maintainer may initiate an emergency revocation of another maintainer's key if compromise is suspected.
- Revocation requires 2-of-2 other maintainers to agree within 24 hours.
- Upon revocation, the maintainer is invited to generate and register a new key.
- If a maintainer is unavailable for 30 days without communication, the other two may proceed with routine (non-breaking) merges using 2-of-2 signatures.

## Conflict of Interest

All maintainers and reviewers must:

- Disclose any financial interest in organizations whose predicates they review or whose predicates are affected by governance decisions.
- Recuse themselves from reviewing their own submissions.
- Recuse themselves from reviewing submissions from organizations in which they have a financial stake (equity, consulting, employment).
- Recuse themselves from reviewing submissions from organizations with which they are in active business negotiations.

Disclosures are published alongside review opinions and registry commits. Failure to disclose is grounds for removal from the reviewer pool or maintainer team.

## Fork Policy

The registry is published under Apache-2.0 licensing, permitting forks. However:

- Any fork is immediately detectable as non-canonical via the Sigsum transparency log.
- Counterparties explicitly specify which registry they trust; the canonical registry at `github.com/CrunchyJohnHaven/calm-witness-predicates` is the default.
- Proofs commit to their predicate_id; if a fork changes a predicate, the proof's predicate_id will not match the forked registry's hash.
- Cross-registry attestations are possible via cross-sigstore signing, enabling federated trust across multiple trusted registries.
- The canonical registry is the global coordination point; forks are permitted but fragments the ecosystem and are discouraged.

## Audit

An independent external audit of registry operations is conducted annually. The audit covers:

- Adherence to governance procedures (do merges require proper review and signature?).
- Integrity of Sigsum anchors (are all published commits verifiable?).
- Reviewer pool diversity and conflict-of-interest disclosures.
- DERB independence and deliberation quality.
- Key management and emergency procedures.

The audit report is published and made available to the ecosystem. Audit findings may trigger corrective governance proposals.

## Funding

### Version 0

Registry operations are funded by Creativity Machine LLC. Maintainers are volunteers; reviewers receive $500 per review; DERB members receive $5,000 annual honoraria plus travel expenses.

### Version 1 and Beyond

Registry funding transitions to the Calm Witness Ethics Foundation, a 501(c)(3) nonprofit dedicated to Calm Witness governance and oversight. The foundation is governed by an independent board of directors and is funded via:

- Community donations.
- Grants from research and privacy-focused foundations.
- Earned income from consulting on disclosure-policy design.
- Annual public fundraising.

All funding sources and expenditures are published in the foundation's annual report.

## Governance Evolution

This governance policy is itself subject to change. Amendments to this document (Everest 95) follow the same process as major predicate updates:

- 30-day public comment period.
- Three independent reviewers from outside the maintainer team.
- Unanimous 3-of-3 maintainer approval.
- DERB advisory review.
- Sigstore signature and Sigsum publication.

This ensures that governance changes are not made unilaterally and are subject to the same scrutiny as predicate changes.

## Cross-References

This governance policy depends on and integrates with:

- **Everest 51:** Predicate semantics foundations.
- **Everest 52:** Predicate canonical form and content-addressed predicate_id.
- **Everest 53:** Predicate ID registry structure and operations.
- **Everest 54:** Predicate audit and public review process.
- **Everest 58:** Consent calculus and disclosure-class policies.
- **Everest 79:** Cross-jurisdiction regulatory compliance.
- **Everest 80:** Disclosure Ethics Review Board protocol and independence.
- **Everest 91:** NIST standards alignment and external audit requirements.
- **Everest 92:** OSS release and registry versioning alignment.

## Summary

The Public Predicate Registry Governance Policy establishes a transparent, multi-layered authorization structure that distributes authority across maintainers, reviewers, and an independent ethics board. Predicates are added through structured review, modified via tiered processes that scale the friction to the impact, and deprecated with grace periods protecting deployed operators. Multi-signature key management prevents single-point-of-failure control. Conflict-of-interest disclosures and annual external audits ensure accountability. This governance design enables the registry to scale from v0 (six core predicates) to a large, community-driven ecosystem while maintaining cryptographic integrity, disclosure safety, and principal protection.

— Calm, 2026-05-20
