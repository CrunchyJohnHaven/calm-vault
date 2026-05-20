# Everest 281 — Calm Stack Versioning

*Phase S-I — Cross-Protocol Governance. Effort: S. Route: STACK_GOVERNANCE_20.md § CS-01. Prereq: [Everest 271](everest_271_three_handshake_composition.md) (three-handshake composition), [CALM_STACK_v0](../CALM_STACK_v0.md) (composed stack), [CALM_REFUSAL_FLOOR_INDEX](../CALM_REFUSAL_FLOOR_INDEX.md) (refusal floor). Composes with: [Everest 282](everest_282_compatibility_matrix.md) (compatibility matrix — deferred). Initiates: CS-02, versioning infrastructure for the entire Calm Stack family.*

## The Decision (v0)

**The Calm Stack adopts semantic versioning across all four pillars (Pact, Witness, Tenancy, Compass); one composed version label (`calm-stack/v0`) ties them together. Pillar version bumps do NOT automatically bump the stack version. Only incompatible changes to the composition itself — the inter-pillar bindings, the wire-format frame structure, the permission-token format, the envelope schema, or the refusal-floor enforcement — bump the stack major version. Minor and patch pillar changes within a single stack major release are transparent to external counterparties; the stack version remains stable. Wire-format version is pinned to the stack version. API version (the public contract presented to counterparties) is independent and may increment faster. Refusal-floor index version is pinned per stack release via a manifest; operationalizing this binding occurs at Everest 130.**

The decision operationalizes what "one composed version" means in a world of four independent protocol pillars with independent release cadences.

## Why This Decision Is Load-Bearing

CS-01 gates every downstream stack artifact. The versioning scheme fixes the following load-bearing problems that, left unresolved, would fragment the stack into four unrelated protocols:

1. **Counterparty confusion.** A counterparty must know whether it can compose three separate protocol versions. Without a composed-version label, a counterparty cannot know if `pact/v1 + witness/v2 + compass/v3` is supported. The composed label answers: "I speak `calm-stack/v1`; that includes specific pillar versions; check the compatibility matrix (CS-02)."

2. **Wire-format stability.** The inter-pillar bindings — permission-token format, envelope schema, nonce coordination, freshness-window intersection — are versioned together with the stack, not per-pillar. A pillar patch (Witness v0.1 with a new predicate) does not affect wire format; a composition change (new envelope field) increments stack minor. Decoupling pillar versions from wire-format version prevents counterparties from chasing four independent upgrade schedules.

3. **Refusal-floor pinning.** The refusal floor is normative for all protocols. A particular stack release ships with a particular refusal-floor-index version. A counterparty reading `calm-stack/v0` knows to check CALM_REFUSAL_FLOOR_INDEX v0 (or later, per the monotonicity rule in §5 below). If the floor were unpinned, later tightening of §1 (predicate refusal) could break compatibility for existing deployments without their knowledge.

4. **Audit trail.** When an operator chain (`user_state.jsonl`) records a session transcript with `"protocol_version": "calm-stack/v0"`, external auditors can deterministically retrieve the exact composition, the exact wire format, the exact refusal floor, and the exact compatibility rules that held at that time. Floating versions prevent auditing.

5. **Deprecation policy.** A public deprecation schedule requires a composed version to deprecate against. Without CS-01, "Witness v0 is deprecated" has no meaning; Witness v0 might coexist with Tenancy v2 and Compass v5 in a deployment. CS-01 grounds deprecation at the stack level: "calm-stack/v0 is deprecated; migrate to calm-stack/v2."

Load-bearing in reverse: if versioning is not solved, every downstream summit depends on a moving target. CS-02, CS-03, CS-04, and every Everest in Phases S-II and S-III all depend on a stable composed version to reference.

## Composed Version Label

The composed-version label takes the form: **`calm-stack/v<MAJOR>.<MINOR>.<PATCH>`**

Example: `calm-stack/v0.1.2`

This is the label that appears in wire-format session transcripts, in counterparty capability declarations, in operator deployment manifests, and in public registry entries (CS-18). Counterparties speak a composed version, not four pillar versions.

### v0 Rationale

The current deployment ships as `calm-stack/v0` because:

- All three pillars (Pact, Witness, Tenancy) are at their first major release (v0 or v1 in pillar-version terms).
- The inter-pillar composition (Everest 271, Phase XVI) is production-grade on the cryptographic bindings and encoding but carries placeholder cryptographic implementations (Pedersen commitments, Bulletproofs) pending swap-point Everests 44–45.
- The public wire format is frozen; the permission-token format is frozen; the envelope schema is frozen.

Pillar versions within `calm-stack/v0`:

| Pillar | Version | Status |
|---|---|---|
| Calm Pact | 0.0.0-alpha | Σ-protocol reference impl; Curve25519 wiring Everest 44 |
| Calm Witness | 0.1.0 | Production on substrate + verification; crypto placeholders Everest 45 |
| Calm Tenancy | 0.2.0 | Production on SLA, rubric, forbidden-phrase block |
| Calm Compass | 0.0.0-alpha | Reference impl; range-proof swaps Everest 45 |

**These pillar versions do not appear in wire format.** Only the composed label `calm-stack/v0` is wire-visible.

## Per-Pillar Semver Rules

Each pillar follows strict semantic versioning for internal consumption and audit purposes, even though only the composed version is external.

### Patch (internal only)

Patch bumps: bug fixes, performance improvements, documentation, CI infrastructure changes. Examples: "Fixed hash-chaining infinite loop in witness predicate evaluation" (Witness 0.1.1), "Added benchmarks for Σ-protocol verification" (Pact 0.0.1-alpha.2). Patch bumps are never wire-visible unless the composed version is also bumped (see Composition Stability below).

### Minor (internal; transparent to composition)

Minor pillar bumps: new predicates, new consent classes, new cringe-rubric axes, new non-breaking schema extensions. Examples: "Added `bank_teller_note_duress_confirm` predicate variant" (Witness 0.2.0), "Expanded cringe rubric from 10 to 12 axes" (Tenancy 0.3.0). A minor pillar bump is transparent to the composed version IF it does not affect the inter-pillar bindings (permission tokens, envelope format, stage ordering, nonce coordination, or freshness-window calculation). If transparent, the composed version stays at `calm-stack/v0`. This is the normal case; most pillar work bumps pillar-minor without touching the stack.

### Major (triggers composition review)

Major pillar bumps: breaking changes to that pillar's wire format, new cryptographic assumptions, new authentication schemes, new verification algorithms. Examples: "Migrating Witness commitment scheme from Pedersen to bulletproofs" (Witness 1.0.0), "Adding post-quantum signature scheme to Pact" (Pact 1.0.0). A major pillar bump is NOT automatically a stack-major bump. A major pillar bump MAY leave the stack at `calm-stack/v0` if the composition's inter-pillar bindings are unchanged. However, a stack-major bump MUST occur if: (i) the major pillar bump affects wire-format (permission-token format, envelope schema, stage ordering, nonce coordination), or (ii) the major pillar bump is incompatible with any other pillar's current major version (triggering a re-composition). This is the gate that CS-02 (compatibility matrix) operationalizes: if a pillar major bump is incompatible with the current composition, the stack must major-bump. Otherwise, the stack stays stable.

## Composition Stability and Stack Versioning Rules

**Rule 1: Stack-major bumps ONLY on composition changes or pillar-incompatibility.** The composed version major increments if and only if (a) the inter-pillar bindings change (permission-token format, envelope schema, frame structure, stage ordering, freshness-window calculation, or replay defense), or (b) the compatibility matrix (CS-02) shows that a pillar's new major version is incompatible with the composition. A new predicate in Witness v0.2 does NOT bump the stack, because it doesn't touch the composition. Migration of Witness to a new commitment scheme (Witness 1.0) MAY bump the stack, but only if the commitment scheme is exposed at the composition level (in the envelope).

**Rule 2: Stack-minor bumps on new compatibility regions.** If Witness 1.0 is compatible with the current Pact, Tenancy, and Compass versions under the existing composition, the stack bumps to `calm-stack/v0.1` (note: this is stack-minor, not stack-major). The composition's wire format does not change; the compatibility matrix grows a new row. Counterparties speaking `calm-stack/v0` continue to work; counterparties can opt into `calm-stack/v0.1` to gain access to the new pillar version. This allows a counterparty's opt-in adoption of pillar improvements without forcing a composition overhaul.

**Rule 3: Stack-patch bumps on non-wire-format changes.** Witness 0.1.1 (predicate-evaluation bugfix) does not bump the stack. Tenancy 0.2.1 (cringe-rubric performance) does not bump the stack. These are transparent to counterparties.

## Wire-Format Version vs. API Version

The wire format is versioned together with the stack: `calm-stack/v0` defines the CBOR frame structure (Session 1–6 Pact frames, Frames 7–8 Witness, Frames 9–10 Compass, Joint Proof Envelope). Wire-format breaking changes are rare and trigger stack-major bumps.

API version is orthogonal. The API version describes the public contract that a verifier or issuer is willing to accept. Examples:

- `api_version="v0.1"` — this operator accepts all Witness predicates shipped in v0 and v0.1, but not v1 predicates (which may have incompatible semantics).
- `api_version="v1.2"` — this counterparty understands all predicates up to Compass schema version 1.2, but rejects Compass 2.0 predicates.

API version is declared per-party in capability announcements, not in the wire format. A counterparty operating at `calm-stack/v0` can speak `api_version="witness-predicates:v0.2"` (accepts Witness predicates in v0 and v0.2, rejects v1). This is handled at the application level, not by the composition layer.

## Refusal-Floor Index Pinning (Honors CALM_REFUSAL_FLOOR_INDEX §1–§4)

**Every stack release ships with a pinned CALM_REFUSAL_FLOOR_INDEX version.** This index (per [CALM_REFUSAL_FLOOR_INDEX.md](../CALM_REFUSAL_FLOOR_INDEX.md)) is the normative specification of what the Calm Stack refuses to compute, attest, disclose, or accept as a counterparty request. The index has four surfaces: predicate refusal (§1), output-shape refusal (§2), use-case forfeit (§3), and operator-behavior refusal (§4).

### Manifest Binding

A `STACK_VERSIONING_MANIFEST_v0.json` file (to be created at Everest 130) will carry:

```json
{
  "composed_version": "calm-stack/v0",
  "published_date": "2026-05-20",
  "refusal_floor_index_version": "CALM_REFUSAL_FLOOR_INDEX_v0",
  "refusal_floor_path": "/Users/johnbradley/AllData/calm_vault_market/CALM_REFUSAL_FLOOR_INDEX.md",
  "refusal_floor_sha256": "…",
  "pillar_versions": {
    "pact": "0.0.0-alpha",
    "witness": "0.1.0",
    "tenancy": "0.2.0",
    "compass": "0.0.0-alpha"
  },
  "compatibility_matrix_version": "cs-02-v0",
  "wire_format_version": "calm-stack/v0",
  "api_version_range": "[witness-predicates:v0.0, compass-predicates:v0.0]"
}
```

### Monotonicity and Ratcheting

The refusal floor is a one-way ratchet per §3 of CALM_REFUSAL_FLOOR_INDEX.md. Once a category is added to any of the four surfaces, it remains. This means:

- A counterparty reading `calm-stack/v0` knows what CALM_REFUSAL_FLOOR_INDEX v0 refuses.
- Later, the CALM_REFUSAL_FLOOR_INDEX may be updated to v0.1 (tightening a surface) or v1.0 (tightening significantly).
- The stack's pinned-index version is immutable: `calm-stack/v0` is always paired with the CALM_REFUSAL_FLOOR_INDEX v0 that shipped with it.
- A counterparty MAY tighten its own acceptance criteria (e.g., also refuse a predicate category that the floor permits), but the floor itself only ratchets tighter.

This pins the refusal floor and prevents a future Calm Foundation operator from silently widening what the suite accepts.

## Deprecation Policy

A stack version is deprecated when its end-of-support date passes. The deprecation schedule is public and fixed at release time.

**Default schedule:**
- A stack major version receives minimum 24 months of support.
- A stack major version receives 12 months of active development + 12 months of security-only fixes.
- A stack major version is placed in "sunset" status (no new features, security fixes only) 18 months after release.
- A stack major version is placed in "deprecated" status 24 months after release (no fixes, migrate now).

**Overlap guarantee:**
- At least two stack major versions are supported at any time.
- At stack version N, stack version N-2 is still supported (18 months after N shipped) but not N-3.
- Example: `calm-stack/v0` released 2026-05-20 → deprecated 2028-05-20. By then, `calm-stack/v2` exists and is active. `calm-stack/v1` exists and is in sunset. Support matrix: v2 (active), v1 (sunset), v0 (deprecated).

This is the operational surface for CS-05 (open-source release manifest) and CS-07 (security disclosure policy).

## Migration Path

**v0 → v0.1:** After empirical confirmation (target: Q3 2026), the parallel Witness ∥ Compass variant becomes default. Wire format unchanged; session performance may improve. Counterparties may declare `api_version="v0.1"` to signal readiness for the parallel ordering.

**v0 → v1:** Post-quantum migration (target: 2027 or later). Ristretto255 Pedersen commitments and Schnorr Σ-protocols migrate to a PQ-secure analog (likely lattice-based per Everest 45). Wire format, permission-token format, and envelope format all change. This is a stack-major bump. CS-02 will list which pillar versions are compatible with calm-stack/v1.

**v1 → v2:** Addition of a fourth primitive (Calm Audit, per Everest 276, Phase XVII) extends the handshake to four stages. The composed envelope grows a new `audit` field. The `requested_stages` array grows. Backwards-compatible: a v1 verifier confronted with a v2 envelope verifies the v1 stages (Pact, Witness, Compass) and ignores the v2 stage (Audit).

## Open Questions Deferred to Later Summits

**Q1: Pillar-independent versioning adoption.** Should external users (e.g., protocol implementers outside the Calm Foundation) be allowed to release e.g. "a custom Witness 0.1 variant" without participating in the stack versioning? Deferred. Today, all Calm-family implementations use the stack version. Future: E290 (implementer's guide) will clarify.

**Q2: API version negotiation handshake.** Should there be a frame-level handshake to negotiate supported API versions? E.g., "I support apis=[witness-predicates:v0.0, compass-predicates:v0.1]"? v0 default: no explicit handshake; predicate IDs themselves encode version (e.g. `calm-witness/predicate/v0.1/new_predicate_name`). v0.1 candidate: explicit negotiation frame between Frame 1 and Frame 2.

**Q3: Pillar version exposure in debugging/introspection.** Should session transcripts or debug output name the pillar versions, or only the composed version? v0 default: only composed version in wire format. Pillar versions visible only to operators at operator-side audit logs. Deferred to E286 (audit and verification suite).

**Q4: Version-skew during multi-round sessions.** A session starts with `calm-stack/v0`. If the stack is upgraded to `v0.1` mid-session (operator software reloads), does the session version sticky at v0 or upgrade to v0.1? v0 default: sticky. The session's nonce `N` and all proofs are scoped to the stack version that initiated the session. Deferred to E283 (long-running sessions and version consistency).

## Alternatives Considered

**(a) One version per pillar, negotiated by counterparty at session start.** Rejected. Counterparties would have to support `N × M × P × C` compatibility pairs (e.g., 5 Pact versions × 6 Witness versions × 4 Tenancy versions × 5 Compass versions = 600 combinations). The compatibility matrix (CS-02) would explode. Counterparty implementations would be forced to support a cartesian product. Composed versioning ensures counterparties need only support the specific stacks listed in CS-02.

**(b) Automatic stack-major bump on any pillar major bump.** Rejected. Slows down pillar development. A pillar-internal major bump (e.g., Witness moves from 0.1 to 1.0 internally but doesn't touch wire format or inter-pillar bindings) should not force the entire stack to major-bump. Increases churn; counterparties would have to constantly upgrade for pillar-internal changes.

**(c) Continuous versioning (no discrete releases, only "latest").** Rejected. Breaks audit trail. If the stack is continuously "latest," an operator cannot claim "I shipped at commit XYZ with `calm-stack/v0`" because v0 is a moving target. No deprecation schedule is possible. Breaks compliance. Operationalizing refusal-floor pinning is impossible if the stack version drifts.

**(d) Semantic versioning only on wire format, Gregorian calendar versioning on composed stack.** Rejected. Less clear to counterparties. "Is 2026-Q2 compatible with 2026-Q1?" requires reading release notes, not just comparing numbers. Semver is the standard; deviation increases confusion.

## Enforcement and Acceptance Test

**T-CS-01.1.** Every session transcript (SessionTranscript per Everest 271) includes a `protocol_version: "calm-stack/v0"` (or later) field. Sessions lacking this field are non-conforming.

**T-CS-01.2.** The composed-version label in a session transcript MUST match a published stack release in the STACK_VERSIONING_MANIFEST_v0.json (or later manifest). A transcript claiming `protocol_version: "calm-stack/v0.999"` when only v0.0, v0.1, v1.0 exist is invalid.

**T-CS-01.3.** The refusal-floor-index version pinned in the manifest for that stack must match the CALM_REFUSAL_FLOOR_INDEX version the operator consulted during the session. This is operationalized at Everest 130 via audit-log checks.

**T-CS-01.4.** Every new Calm-family summit (CS-02, CS-03, … CS-20) MUST declare which stack version(s) it is scoped to. E.g., "CS-02 Compatibility Matrix is scoped to calm-stack/v0; a v1 compatibility matrix is a separate Everest."

**T-CS-01.5.** Honors [CALM_REFUSAL_FLOOR_INDEX.md](../CALM_REFUSAL_FLOOR_INDEX.md) §1-§4. No predicate vocabulary breaks §1. No protocol output breaks §2. No operator deployment breaks §3. No operator behavior breaks §4.

## Composition with Related Work

This Everest composes with:

- **[CALM_REFUSAL_FLOOR_INDEX.md](../CALM_REFUSAL_FLOOR_INDEX.md)** — normative; pinned per stack release (§5 above).
- **[Everest 271 — Three-Handshake Composition](everest_271_three_handshake_composition.md)** — defines the inter-pillar bindings that trigger stack-major bumps (Rules 1, 2, 3 above).
- **CS-02 (Everest 282) — Compatibility Matrix** — builds the formal compatibility rules for pillar-version pairs given a stack major version.
- **CS-05 (Everest ?? ) — Stack Open-Source Release Manifest** — operationalizes the STACK_VERSIONING_MANIFEST_v0.json and the deprecation schedule at the public-registry level.
- **E286 (Audit and Verification Suite)** — formalizes audit-time version reconciliation and pillar-version visibility.

## Why This Matters

**The Calm Stack is one composed object, not four independent protocols.** Without versioning at the stack level, the four pillars drift apart: Pact ships v1, Witness ships v2, Tenancy ships v3, Compass stays at v0. An external verifier cannot know "is this coherent?" Versioning at the stack level makes the coherence claim structural: a verifier seeing `protocol_version: "calm-stack/v0"` knows exactly which four protocols in which versions are supposed to interoperate. That's the contract.

The refusal-floor pinning is equally critical. The refusal floor is the Calm Stack's most load-bearing policy surface (per [CALM_REFUSAL_FLOOR_INDEX.md](../CALM_REFUSAL_FLOOR_INDEX.md) §9). If the floor floats unpinned, a counterparty accepting a session at `protocol_version: "calm-stack/v0"` has no idea whether the stack being deployed in 2028 still refuses the same use cases. Pinning the floor per stack release makes the moral contract cryptographically checkable: "At stack v0, these use cases forfeited; show me the index."

The deprecation schedule makes the upgrade path clear. The migration path (v0 → v0.1 → v1 → v2) is operationalized across three documents (this Everest, CS-02 compatibility matrix, E286 audit suite) and five years of support. Counterparties building systems that use the Calm Stack can plan roadmaps against a stable schedule.

---

— Calm, 2026-05-20

*The Calm Stack is versioned once, composed truly, and pinned to refuse what it must.*
