# Everest 118 — Values Evolution Policy

*Phase IX — Values Vocabulary. Prereq: Everest 117.*

## Overview

This document specifies the governance process by which new dimensions enter the Calm Values Registry. The process balances principled scrutiny with cultural pluralism: dimensions are normative commitments, not technical artifacts, and therefore demand broader community participation than predicates. The process mirrors Everest 54 (Predicate Audit & Public Review Process) with extensions tailored to values' foundational role in identity and culture.

## The Process

### 1. Proposal

A principal-author files a Pull Request to github.com/CrunchyJohnHaven/calm-values-registry with a full dimension specification. The PR must include:

- Dimension name and scope
- Cultural grounding and examples
- Relationship to existing dimensions
- Use cases and expected scale
- Any known tensions with other dimensions
- Proposed dimension_id (provisional)

### 2. Initial Triage (7 days)

A maintainer reviewer conducts completeness and admissibility review. The triage phase is the enforcement gate for the "refusal floor" (see below). If the proposed dimension touches protected categories as defined in Everest 113, the PR is rejected at triage with published rationale. All triage decisions (acceptance and refusal) are published to maintain transparency.

Dimensions passing triage move to public comment.

### 3. Public Comment Period (60 days)

The proposal is open for community feedback. The 60-day window is substantially longer than the 14-day predicate comment period, reflecting that values are more foundational and culturally situated than predicates. Comments address:

- Cultural interpretation and appropriateness
- Potential misuse or overreach
- Alignment with existing dimensions
- Missing nuance or omitted communities
- Deprecation concerns (if replacing an existing dimension)

### 4. Outside Reviewer Assignment

The maintainer assigns at least three independent reviewers. Reviewer composition is mandatory:

- At least one researcher with expertise in cross-cultural psychology or anthropology
- At least one scholar in disability rights or cognitive liberties
- At least one specialist in civil society, philosophy of values, or applied ethics

At least one reviewer must be from a non-WEIRD (Western, Educated, Industrialized, Rich, Democratic) cultural context. The reviewer pool is maintained as an ongoing cohort, not selected ad-hoc for individual PRs. All reviewers disclose conflicts of interest.

### 5. Reviewer Reports (21 days)

Each reviewer files a written report addressing:

- Clarity and coherence of the dimension
- Cultural validity and applicability across contexts
- Risks of misuse or discrimination
- Consistency with Calm values and ethics
- Recommendation (approve, request revision, reject)

Reports are published in full.

### 6. Resolution

The maintainer (in consultation with all three reviewers) makes the final decision:

- Approve: dimension is registered and assigned a canonical dimension_id
- Revision requested: dimension is revised and re-submitted; full process repeats
- Reject: PR is closed with published rationale

Approval requires consensus among at least three reviewers and the maintainer. The bar is higher than predicate approval: dimensions shape identity, and their governance must reflect that weight.

### 7. Cryptographic Registration

Upon approval, the dimension specification is hashed (SHA-256) to derive a canonical dimension_id. The dimension record is signed using Sigstore and published to Sigsum, creating a cryptographic anchor in public infrastructure. The registry commit hash and Sigsum anchor are published.

### 8. Adding to the v0 Set

If a new dimension is added to the frozen v0 set (per Everest 107), it enters SEALED v0 status immediately upon registration. No stealth updates to v0 are permitted; v0 dimensions are immutable once published. Subsequent updates to that dimension (semantic changes, new data) require a new dimension_id versioned as v1.

### 9. Deprecation Flow

A dimension author or maintainer may propose deprecation of an existing dimension by filing a deprecation PR. The PR must include:

- Rationale for deprecation
- Migration guide (mapping to successor dimensions, if applicable)
- Grace period: 18 months (longer than the 90-day predicate grace period, because dimensions are foundational)

During the grace period, outstanding proofs over the deprecated dimension remain Valid. After grace expiration, the dimension is removed from the registry; proofs referencing it retroactively degrade to Invalid.

### 10. Emergency Deprecation

If a dimension is discovered to enable discrimination, cause harm, or violate Calm ethical commitments, the maintainer team (3-of-3 multi-sig) may deprecate it without the standard grace period, pending ethics board concurrence.

- Notice: 30 days for safety-relevant deprecations
- Proof degradation: immediate. Existing proofs over the emergency-deprecated dimension degrade to Invalid (not Deprecated)

### 11. The "principal_authored_other" Special Case

Each principal maintains the right to author local dimensions specific to their identity and context. These dimensions do not enter the global registry. Their evolution is entirely principal-private and governed by that principal's own protocols. Only dimensions proposed for public registry entry pass through this governance process.

### 12. Maintainer Team Composition

Extends Everest 95. The maintainer team comprises:

- Calm (author)
- Koushik Gavini (values semanticist)
- At least one external maintainer (TBD)

Approval of new dimensions requires 3-of-3 multi-signature consensus—a higher bar than predicate approval. All maintainers must disclose conflicts of interest. The external maintainer role rotates or refreshes every 18 months to maintain independence.

### 13. Versioning

Dimensions follow semantic versioning:

- **Major version** (e.g., v1 to v2): breaking change to dimension semantics, scope, or cultural grounding. Requires new dimension_id and full re-review.
- **Minor version** (e.g., v1.1 to v1.2): backward-compatible additions, such as new cultural calibration data, extended examples, or refined guidance. Reviewers and maintainer approve via expedited review (14 days).
- **Patch** (e.g., v1.0 to v1.0.1): documentation clarifications, typo fixes, or curation updates. Single maintainer approval sufficient.

### 14. Cross-Cultural Review Safeguard

At least one reviewer in every approval cohort must come from a non-WEIRD population. This safeguard prevents dimensions from being designed and validated solely through Western academic and cultural lenses. The reviewer pool is actively maintained over time; ad-hoc recruitment for individual PRs is insufficient.

### 15. Public Artifacts at Each Stage

Transparency is non-negotiable:

- PR and full proposal: public from day 1
- Triage decision (accept or refuse): published with rationale
- All reviewer reports: published in full
- Maintainer decision: published with summary reasoning
- Registry commit hash and Sigsum anchor: published
- Annual audit report (see below): public

### 16. Annual Values-Registry Audit

Per Everest 80 (ethics board), the Calm ethics board conducts an annual audit of the values registry. The audit reviews:

- Are existing dimensions still well-calibrated across cultural contexts?
- Has cultural context shifted such that existing dimensions are now misaligned?
- Do any dimensions, in practice, enable or facilitate discrimination?
- Are there gaps in dimension coverage?

The audit results and recommendations are published. Dimensions flagged as miscalibrated or harmful enter the deprecation process (standard or emergency, as warranted).

## The "Refusal Floor" Gate

Dimensions proposed under protected categories as defined in Everest 113 are rejected at triage without proceeding to public comment. The triage gatekeeper publishes refused dimensions in full, with clear rationale. This prevents bad-faith proposals from occupying community attention and clarifies boundaries.

Protected categories include (by reference to E113): dimensions designed to essentialize or stigmatize individuals based on nationality, ability status, gender identity, or sexual orientation; dimensions intended to codify discriminatory social hierarchies; dimensions conflating value-holding with innate traits.

## Cross-References

- **Everest 54**: Predicate Audit & Public Review Process (sister governance framework)
- **Everest 80**: Ethics Board Charter (annual values-registry audit)
- **Everest 95**: Maintainer Roles and Conflict of Interest (extended for values)
- **Everest 107**: v0 Freezing and Versioning (immutability of v0)
- **Everest 113**: Protected Categories and Refusal Floor (discrimination safeguard)
- **Everest 115**: Cultural Calibration Framework (validation process)
- **Everest 117**: Values Registry Specification (normative dimensions)

## Rationale

Values are not technical predicates. They are normative commitments that individuals and communities make about what matters. A dimension poorly designed or culturally tone-deaf has downstream effects not just on proof verification, but on how principals understand and act. The governance framework for values therefore requires:

1. **Longer deliberation**: 60 days vs. 14 days for predicates
2. **Broader expertise**: mandatory cross-cultural and disability-rights representation
3. **Higher approval bar**: 3-of-3 consensus vs. simple majority
4. **Longer deprecation grace**: 18 months vs. 90 days (dimension retirement is high-stakes for principals)
5. **Annual audit**: systematic review of whether dimensions remain fit for purpose

This framework is demanding. It is intended to be.

---

— Calm, 2026-05-20
