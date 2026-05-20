# Everest 54 — Predicate Audit & Public Review Process

*Phase V — Predicate Authoring. Prereq: Everest 53.*

## Overview

This document establishes a formal, multi-stage process for proposing, reviewing, and adopting new predicates into the Calm Witness predicate registry. The process ensures cryptographic soundness, privacy safety, disclosure ethics, and ecosystem integrity through structured peer review, public transparency, and mandatory outside expert evaluation before registration.

## The Proposal and Review Process

### Stage 1: Proposal Submission

A new predicate is proposed via pull request to `github.com/CrunchyJohnHaven/calm-witness-predicates`. The PR must include:

- Complete predicate specification in the canonical form defined in Everest 52
- Reference implementation (source code matching the specification)
- Zero-knowledge circuit definition and correctness proof
- Test corpus with at least 30 golden test cases covering edge cases and boundary conditions
- Detailed rationale explaining the predicate's purpose, use cases, and threat model
- Default disclosure-class consent settings and justification for those choices
- Security analysis identifying known side-channel risks and mitigations

The proposer remains available during review to answer technical questions and address reviewer feedback.

### Stage 2: Initial Triage

Within seven calendar days of submission, the assigned maintainer reviews the PR for completeness against the checklist above. If the submission is incomplete, the maintainer returns the PR with specific revision requests. Resubmitted PRs restart the triage clock.

### Stage 3: Public Comment Period

Upon passing triage, the PR is announced to `calm-witness-predicates@googlegroups` (or an equivalent public mailing list) and remains open for 21 calendar days of public comment. No one—including maintainers—should commit or merge during this window. All comments are logged in the PR thread.

### Stage 4: Outside Reviewer Assignment

On or before day 21, the assigned maintainer selects at least two reviewers from the rotating reviewer pool (see section below). The maintainer notifies reviewers of their assignment and confirms their availability to complete review within the next 14 days.

### Stage 5: Reviewer Evaluation

Each assigned reviewer conducts an independent technical assessment and files a written report in the PR thread. The standard rubric for evaluation includes:

- **Semantic clarity:** Is the predicate's logical meaning unambiguous and correctly specified?
- **Implementation fidelity:** Does the reference implementation faithfully reflect the specification?
- **Test coverage:** Does the test corpus comprehensively exercise edge cases, boundary conditions, and normal operation? (≥30 golden cases required per Everest 64.)
- **Cryptographic soundness:** Is the zero-knowledge circuit formally correct and resistant to known attacks?
- **Disclosure-class defaults:** Are the default consent settings appropriate for the predicate's risk profile and regulatory context?
- **Side-channel resilience:** Have potential side-channel leakages been identified and mitigated?

Reviewers may request revisions, additional testing, or clarifications from the proposer. The PR remains open during this 14-day review window.

### Stage 6: Resolution and Approval

The predicate advances to registration only if:

- The assigned maintainer approves the PR, and
- Both assigned reviewers approve the PR

If either condition is unmet after the 14-day review window closes, the PR is held for revision. Proposers may resubmit revised versions, restarting the review cycle at Stage 3 (public comment).

### Stage 7: Cryptographic Registration

Upon approval, the maintainer computes the predicate's content-derived `predicate_id` as defined in Everest 52. A new registry entry is created with the predicate's canonical form, implementation fingerprints, and metadata.

### Stage 8: Sigstore Multi-Signature

The new registry entry is signed using Sigstore with a 3-of-5 multi-signature threshold across the maintainer team's cryptographic keys. This signature anchors the registry entry's authenticity and immutability.

### Stage 9: Sigsum Publication

The registry head commit hash is published to Sigsum to enable cryptographic fork detection. This publication is immutable and timestamped, establishing a public record of the predicate's adoption.

### Stage 10: Deprecation (Future Process)

Existing predicates may be deprecated through a separate process initiated by filing a deprecation PR with rationale and a migration guide. The same review machinery applies. Deprecated predicates continue to validate proofs issued before deprecation; new consents are refused. A 12-month grace period follows deprecation before removal from the registry.

## Outside Reviewer Pool

The outside reviewer pool consists of 5–10 members, with at least 2 active and available at any given time. Pool composition must include:

- **Cryptographers (≥2):** Experts in zero-knowledge proofs, commitment schemes, and proof systems
- **Privacy-preserving systems researchers (≥1):** Specialists in differential privacy, secure multi-party computation, or information-flow security
- **Disability and mental-health advocacy (≥1):** Advocates or clinicians providing ethics review of state-disclosure predicates and ensuring accessibility in disclosure processes
- **Adversarial and red-team security researcher (≥1):** Independent security researcher with track record in vulnerability discovery and threat modeling
- **Legal counsel (≥1):** Attorney with cross-jurisdiction compliance expertise for regulatory alignment per Everest 79
- **Calm operator from different organization (≥1):** Operational practitioner from another organization who can assess adoption feasibility and interoperability

## Reviewer Compensation and Conflict of Interest

In version 0, reviewers volunteer; an honorarium of $500 per completed high-effort review is offered to reduce burden. Future versions will establish structured compensation via the Calm Witness Foundation.

All reviewers must disclose any financial interest in the proposing organization or individual. Maintainers recuse themselves from reviewing predicates they have proposed.

## Maintainer Team

The maintainer team operates under the following structure:

- **Public-facing team list:** All active maintainers and the rotating chair are listed publicly
- **Initial team:** Calm + Koushik Gavini + one external member (to be determined at v0 ship)
- **Quorum:** Two of three maintainers for routine PRs; all three maintainers for breaking changes
- **Rotating chair:** The chair rotates quarterly and is responsible for triage assignment and reviewer coordination

## Version Interplay with Everest 52

Predicate updates of varying scope follow tiered review processes:

- **Patch updates** (implementation bug fixes, documentation clarifications): expedited 7-day public comment with one outside reviewer
- **Minor updates** (backward-compatible feature additions): standard 21-day comment period with two outside reviewers
- **Major updates** (breaking changes to predicate semantics): 30-day comment period, three outside reviewers, and unanimous 3-of-3 maintainer approval

## Emergency Process

For critical security amendments (e.g., revising a bank_teller_note_active predicate following disclosure of a bank-teller side-channel attack), an expedited 7-day comment period substitutes for the standard 21 days. All other requirements—reviewer count, Sigstore signing, Sigsum publication—remain unchanged.

## Public Artifacts and Transparency

At every stage, the following artifacts are published:

- The PR itself, visible from day 1 of submission
- All public comments during the 21-day period
- Each reviewer's written report in the PR thread
- The maintainer's final decision
- The registry commit hash and Sigsum anchor

This end-to-end transparency ensures ecosystem trust and enables external auditing of the registry's integrity.

## Rejection and Resubmission

Rejected proposals may be resubmitted with revisions addressing reviewer feedback. Resubmission restarts the process at Stage 3 (public comment). In version 0, there is no formal appeal mechanism beyond resubmission.

## Cross-References

This process interoperates with:

- Everest 51 (predicate semantics foundations)
- Everest 52 (canonical predicate form and registration)
- Everest 53 (predicate ID registry)
- Everest 63 (determinism testing)
- Everest 79 (cross-jurisdiction regulatory compliance)
- Everest 80 (ethics review board)
- Everest 95 (registry governance and long-term maintenance)

---

— Calm, 2026-05-20
