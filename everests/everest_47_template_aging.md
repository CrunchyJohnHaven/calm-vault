# Everest 47 — Template Aging Without Breaking Proofs

*Phase IV — Biometric Distance Machinery. Prereq: Everest 46, 39.*

## Problem Statement

When a principal's template rotates (per E17 migration protocol), the rotation invalidates the template_id references embedded in all outstanding proofs issued against the old template. Without a grace mechanism, verifiers immediately reject these cached proofs, forcing principals to re-issue all in-flight disclosures and breaking long-lived counterparty verification chains. This creates operational friction and undermines the utility of template migrations as a security response mechanism.

Everest 47 introduces template aging: a grace window during which new template v_n+1 coexists with retiring template v_n, allowing verifiers to accept proofs from either template without rejection. This preserves proof validity across rotation boundaries while ensuring eventual migration to the new template.

## Grace Window Architecture

### Default and Configurable Windows

Each template rotation establishes a grace period: the span during which both old and new templates are treated as valid by verifiers. The grace window defaults to 30 days from migration timestamp but is configurable per principal and per rotation context:

- **Low-stakes principals** (e.g., public disclosure operators with high proof volume): grace extends to 90 days, allowing time for cached proofs to age naturally through the ecosystem.
- **Standard principals**: 30 days is the baseline.
- **Highest-stakes principals** (e.g., immediate post-incident rotations following a suspected compromise or vulnerability patch): grace shrinks to 24 hours, forcing rapid re-issuance and minimizing the attack surface.

Configuration occurs at migration time via an operator parameter; this choice is recorded in the grace registry for audit transparency.

### Grace Registry

The grace registry is a monotonic append-only log of aging records, anchored to Sigsum and published by the operator. Each record follows:

```
kind: "template.aging"
payload: {
  old_template_id: <hash>,
  new_template_id: <hash>,
  migration_ts: <unix_timestamp>,
  grace_until_ts: <unix_timestamp>,
  principal_id: <identifier>,
  grace_window_days: <integer>
}
```

Verifiers query this registry (either via the operator's published API endpoint or directly from Sigsum gossip/chain) to determine whether a proof referencing an old template_id falls within an active grace window. If the current timestamp is before grace_until_ts and the template_id matches old_template_id, verification proceeds; after grace_until_ts, the old template_id is unconditionally rejected.

## Concurrent Template Validity

### Dual-Template State During Grace

During the grace window, both old and new templates are cryptographically active. A principal may generate proofs against either template:

- **New template proofs**: used for fresh disclosures and satisfy the forward-looking ecosystem.
- **Old template proofs**: replay-of-cached scenarios, where a counterparty possesses a cached proof binding and asks the principal to re-sign or re-validate against the same template to maintain chain consistency.

Predicates (e.g., liveness checks, age checks, distance thresholds) are always evaluated against the NEW template during the grace window. This ensures that security properties flow to the newer template immediately upon rotation, even if backward-compatible proofs reference the older one.

### Proof Construction During Grace

When a principal re-issues a proof that was originally derived from the old template (e.g., to refresh a long-cached counterparty cache), the principal re-issues against the new template and includes a binding to the old disclosure event. The counterparty updates its cache reference to the new template_id, and future re-validations use the new template.

This lazy migration pattern avoids forced re-issuance at rotation time while ensuring drift toward the new template over the grace period.

## Verifier Workflow

Verifiers adopt the following proof-validation procedure:

1. **Extract template_id from proof**: Deserialize the proof's Pedersen commitment (E46) or explicit template_id field.
2. **Query grace registry**: Check whether an aging record exists mapping this template_id to a new template, and whether current_timestamp < grace_until_ts.
3. **Conditional acceptance**:
   - If the template_id is current (not aging): proceed with standard verification using the current template parameters.
   - If an active aging record exists: verify the proof against the OLD template, permitting the proof to remain valid.
   - If the template_id has aged out (current_timestamp >= grace_until_ts): reject the proof and require re-issuance against the new template.
4. **Sigsum anchor check**: Both template_id values (old and new) appear in the operator's Sigsum tree; verifiers can audit the creation and aging timeline.

## Interaction with Template ID Commitment

Everest 46 introduces Pedersen commitments linking proofs to specific templates: C_t = g^template_id × h^r, with equality proofs confirming the commitment matches the proof's template_id. Template aging does not weaken this binding; instead, the grace registry provides verifiers with the authority to accept both old and new template_ids within their respective validity windows.

When a principal constructs a proof against the old template during grace, the Pedersen commitment reflects the old template_id, and the aging record provides verifiers with the necessary authorization to accept it.

## Drift Modeling and Security Incidents

Template rotation is triggered by drift conditions (E39) or security incidents (E15). Aging windows are calibrated to the rotation's urgency:

- Drift-triggered rotations: standard 30-day grace allows the ecosystem to naturally transition to the new template without operational shock.
- Security incident rotations: 24-hour grace forces rapid re-issuance, reducing the window during which both templates are simultaneously in use and limiting the blast radius of a compromise.

Operators publish rotation reasons in the grace registry payload (e.g., "drift threshold exceeded" vs. "suspected compromise"), enabling auditors to assess risk and verifiers to apply heightened scrutiny to aging records tagged as incident-driven.

## Cross-Template Consistency and CredexAI VC

Everest 22 defines CredexAI Verifiable Credentials with template_id metadata. When a template ages, operators must issue updated VC metadata reflecting both the old and new template_ids for the duration of the grace window. Counterparties holding cached VCs against the old template can re-fetch updated VCs and refresh their template_id bindings.

VC issuance during grace windows includes a note on the VC's face (in metadata, not the credential itself) indicating the grace period and the new template_id, signaling to counterparties that proofs will eventually require re-validation against the new template.

## Multiple Concurrent Active Templates

In high-velocity rotation scenarios (e.g., monthly security patches), an operator may have multiple aging records simultaneously active. The grace registry design accommodates this through principal-keyed lookups: a verifier queries all aging records for a given principal and checks if the proof's template_id matches any old_template_id with an active grace window.

Predicate evaluation uses the CURRENT (newest) active template, not the oldest. This ensures that security posture flows forward with each rotation and is not degraded by the availability of older template options.

## Sigsum Anchoring and Auditability

Grace registry entries are published in the operator's Sigsum log, enabling:

- **Temporal audit**: The Sigsum timestamp tree shows when each template rotation occurred and when each grace period expired.
- **Template history**: A complete trace of template evolution for any principal, with Sigsum's witness-based proofs of publication.
- **Verifier transparency**: Verifiers can independently verify that an aging record was published by the operator and was active at the time of proof validation.

Operators include a hash of the previous aging record in each new rotation, creating a chain; this enables verifiers to detect deletions or reordering in the grace registry.

## Implementation Notes

Operators implement aging via a grace registry service, exposed as:

- **GET /grace/{principal_id}**: Returns all active and expired aging records for the principal, with grace_until_ts.
- **POST /grace/check**: Takes (principal_id, template_id, current_ts) and returns whether the template is valid, along with the new template_id if aging.

Verifiers cache grace registry results for brief windows (e.g., 5 minutes) to avoid per-proof API calls; cache invalidation occurs on Sigsum refresh.

Operators with high proof volume shard the grace registry by principal_id to improve query performance.

## Cross-References and Dependencies

- **E15**: CredexAI VC template_id must be updated when template ages.
- **E17**: Template version migration protocol; aging coexists with migration.
- **E22**: CredexAI VC metadata includes template_id; VC issuance reflects aging windows.
- **E39**: Drift modeling triggers template rotation; aging window calibrated to drift severity.
- **E46**: Pedersen commitment to template_id; aging records provide verifier authorization.
- **E48**: Cross-template consistency proofs (separate everest); aging enables concurrent template use.

## Conclusion

Template aging decouples template rotation from proof invalidation, reducing operational friction while maintaining forward-moving security posture. Configurable grace windows align aging windows with rotation urgency, and the grace registry provides verifiers with clear, auditable authority to accept proofs across template boundaries. This design preserves the utility of template migrations as both a security mechanism and an evolution tool.

— Calm, 2026-05-20
