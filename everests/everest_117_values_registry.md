# Everest 117 — Values Registry

*Phase IX — Values Vocabulary. Prereq: Everest 107, 58.*

## Overview

The Values Registry is a public, append-only Git repository that serves as the authoritative source of truth for dimension definitions within the Calm ZKAC protocol. Once a dimension is published in a version, its semantics are immutable; new semantics require a new versioned dimension. This registry extends the governance and stability patterns established in Everest 52 (canonical form) and Everest 53 (predicate registry), applying them to the values and cultural-ethical dimensions that constitute the protocol's semantic foundation.

The registry is maintained at `github.com/CrunchyJohnHaven/calm-values-registry` under the Apache-2.0 license.

## Repository Structure

Each dimension occupies a versioned directory structure:

```
dimensions/
  cooperation/
    v0/
      spec.md                    # human-readable specification
      semantics.json             # formal definition
      inference_function.py      # the f_cooperation algorithm
      golden_corpus/
        case_001.json
        case_002.json
        ...
      cross_cultural_notes.md    # regional context and nuances
      cultural_calibration.yaml  # calibration data per cultural zone
    v1/
      # published only if semantics evolve
  fairness/
    v0/
      spec.md
      semantics.json
      inference_function.py
      golden_corpus/
        ...
      cross_cultural_notes.md
      cultural_calibration.yaml
  [other dimensions]
```

Each dimension name is canonical within its version. The directory hierarchy mirrors the logical organization of the values vocabulary.

## Dimension Identification and Immutability

Dimensions are identified by a deterministic ID:

```
dimension_id = "calm-values/" + name + "/" + version + "/" + sha256(canonical_spec)[0:16]
```

The canonical spec is the concatenation of semantics.json and the inference function, serialized in a fixed canonical form (per Everest 52 rules).

**Immutability rules:**

- Once v0 is published, v0 NEVER CHANGES. No corrections, clarifications, or refinements are made in-place.
- If a dimension's semantics require revision—whether due to discovered ambiguity, cross-cultural feedback, or evolved understanding—a new version (v1, v2, etc.) is published as a distinct dimension.
- Each version has its own unique dimension_id; proofs scoped to v0 do not automatically transfer to v1.
- Dimension names may be reused across versions, but the version suffix ensures uniqueness and prevents collision.

This strict versioning prevents the subtle corruption that arises when definitions drift over time while stakeholders assume they reference the same semantics.

## Stability and Deprecation

Dimensions may enter a DEPRECATED state if they are no longer recommended for new use, yet they are never deleted from the registry.

**Deprecation mechanics:**

- A deprecated dimension remains queryable and remains valid for backward compatibility.
- Proofs generated over deprecated dimensions do not lose validity.
- Deprecated dimensions are marked clearly in the registry metadata and in the CLI output.
- Deprecation is published as a registry commit and anchored to Sigsum (per Everest 30).
- The deprecation record includes a rationale and, where applicable, a recommendation for a newer dimension.

This ensures that systems that relied on a dimension do not break; they simply become aware that the dimension is no longer maintained for new development.

## Principal-Authored Custom Dimensions

Principals may author their own custom dimensions via the `principal_authored_other` field in the values object. These custom dimensions are scoped to the principal's local vault and do NOT enter the public registry.

**Governance of custom dimensions:**

- Each principal who uses `principal_authored_other` defines their own local dimension.
- Custom dimension specs follow the same canonical form and versioning rules as public dimensions.
- Custom dimensions are NOT subject to multi-sig or external review.
- They may be shared privately with counterparties, but their inclusion in any shared proof must be explicitly disclosed.
- Counterparties who receive proofs referencing custom dimensions may inspect the full spec but are not obligated to accept them.

This separation preserves the integrity of the public registry while allowing flexibility for specialized use cases that do not require consensus.

## Governance and Multi-Signature

The Values Registry is maintained by a **Maintainer Team** comprising:

- Calm (Creativity Machine LLC) — primary steward
- Koushik Gavini — values framework architect
- One external member (to be selected; role: cultural diversity advocate)

**Approval thresholds:**

- **Routine operations** (metadata updates, documentation fixes, release orchestration): 2-of-3 multi-sig
- **New dimension additions**: 3-of-3 multi-sig (consensus required)

**External review requirements:**

- Every new dimension must be reviewed by at least 3 independent external reviewers.
- At least 1 external reviewer must have cross-cultural expertise relevant to the dimension's domain.
- Reviewers are selected from an open panel maintained in the repository.
- Review feedback is published and archived in the dimension directory.

**Public comment periods:**

- New dimensions: 30-day public comment window before final publication
- Deprecations: 60-day public comment window before finalization

These mechanisms ensure that the registry remains trustworthy across diverse stakeholder groups and resistant to unilateral control.

## Anti-Fragmentation and Canonical Authority

The public registry at `github.com/CrunchyJohnHaven/calm-values-registry` is the single source of truth for dimension definitions.

- The Apache-2.0 license permits forking, but forked registries are not authoritative.
- Counterparties who encounter proofs referencing custom registries must explicitly specify which registry they trust.
- The canonical registry is the presumed authority unless a counterparty opts into an alternative.
- All dimension_ids reference the canonical registry by default.

This design prevents registry fragmentation while respecting the legal right to fork.

## Cryptographic Anchoring and Verification

Every merge to the registry is anchored to Sigsum (per Everest 30), creating an immutable timeline of registry state.

**Verification mechanics:**

- Each registry commit hash is published to the Sigsum log.
- Release tags are signed with Sigstore certificates.
- The CLI command `calm-values verify-registry` fetches the commit timeline from Sigsum and validates Sigstore signatures.
- Stakeholders can independently verify that a dimension was present in the registry at a specific point in time.

This cryptographic chain ensures that dimensions cannot be retroactively modified and provides non-repudiation for all registry changes.

## Command-Line Interface

The Calm protocol CLI includes a `calm-values` command suite:

```bash
calm-values list                    # List all registered dimensions with status
calm-values show <dimension>        # Display full spec for a dimension (all versions)
calm-values pull                    # Update local snapshot of the registry
calm-values verify-registry         # Verify Sigsum anchoring and Sigstore signatures
```

These commands provide programmatic and human access to the registry without requiring direct Git or GitHub interaction.

## Integration with Everest Ecosystem

The Values Registry is positioned within the broader Everest architecture:

- **Everest 52** — Canonical Form: defines the serialization rules used to compute dimension_ids
- **Everest 53** — Predicate Registry: sister registry for predicates; shares governance and anchoring patterns
- **Everest 54** — Audit Process: audit framework applied to dimension reviews and registry operations
- **Everest 107** — Values Dimensions v0: the first set of published dimensions (cooperation, fairness, transparency, etc.)
- **Everest 118** — Evolution Policy: governance of backward-incompatible changes to the protocol
- **Everest 165** — Cultural Localization: methodology for cross-cultural calibration of dimensions

These cross-references ensure that the Values Registry is embedded in a coherent, mutually reinforcing system of canonical governance.

## Expected Dimensions in v0

The initial v0 release includes the core values vocabulary:

- **cooperation** — the propensity to align interests and coordinate action with other principals
- **fairness** — the commitment to equitable treatment and transparent rules
- **transparency** — the tendency to disclose intentions, constraints, and outcomes
- **reciprocity** — the inclination to honor mutual obligation over time
- **autonomy** — the respect for self-determination and freedom from coercion

Each dimension is accompanied by a golden corpus of cases, cross-cultural notes, and calibration data specific to major cultural zones (Western individualistic, East Asian relational, sub-Saharan communal, etc.).

## Success Metrics

The Values Registry is considered successful when:

- At least 3 counterparties have published proofs using the v0 dimensions
- No dimension has required emergency correction (indicating stable semantics)
- External reviewers report high inter-rater agreement on dimension inferences
- The registry commit log shows regular maintenance and community engagement
- Sigsum and Sigstore verification succeeds for all published commits

---

— Calm, 2026-05-20
