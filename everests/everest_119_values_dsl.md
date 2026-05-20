# Everest 119 — Values DSL

*Phase IX — Values Vocabulary. Prereq: Everest 117, 51.*

## Decision: Fixed Composition Table, Not Free DSL

Version 0 ships a **fixed enumeration of valid value-dimension compositions**, not a free Domain-Specific Language. This decision mirrors the architectural choice made in Everest 51 (predicate language), applied to the attestation plane where counterparties request proof that a subject embodies composed values.

The justification is the same: auditability, side-channel containment, and predicate-ID stability outweigh expressivity gains. A free DSL would create an unbounded request surface, require per-composition ZK circuit generation at runtime, and expose the system to probe attacks from counterparties seeking to reverse-engineer identity through novel combinations.

## Why Fixed Table Over DSL

**Auditability**: Each pre-built composition has a documented intent, ethics review, and test corpus. A free DSL invites auditors to ask: which compositions are valid? Why? Who approved each new one? A fixed registry answers these questions at glance.

**Circuit Specialization**: The ZK infrastructure generates a dedicated circuit for each composition. Fixed compositions allow circuit optimization, pre-compiled proofs, and cached verification. Dynamic DSL-driven composition would require just-in-time circuit synthesis, increasing operator latency and introducing compilation vulnerabilities.

**Side-Channel Containment**: Novel compositions could probe the system's tolerance boundaries—e.g., requesting "generosity AND harm_to_rivals" to discover which value dimensions conflict in the system's model. A fixed table prevents this by refusing unregistered requests outright.

**Predicate-ID Stability**: Each composition has a stable, content-addressed ID. Counterparties trust that requesting `unselfish_AND_untribal` means the same predicate this quarter and next. If compositions were dynamically synthesized, IDs would become semantic—fragile and difficult to version.

**Counterparty UX Simplicity**: Counterparties don't need to learn a DSL syntax. They query by name from a published list. This reduces friction and deployment risk.

## The v0 Composition Registry

The fixed table enumerates valid compositions across these categories:

### AND-Compositions (2 Dimensions, Conjunction)

From the 10-dimension value space (generosity, cooperation_across_difference, non_harm, cross_difference_respect, consistency_under_stress, willing_to_be_corrected, values_reversal_present, unselfish, untribal, fairness), there are theoretically 45 possible 2-element AND pairs. The v0 registry pre-builds 12-18 of the highest-utility ones:

- `unselfish_AND_untribal`: Subject demonstrates generosity AND non-tribal engagement above threshold.
- `respectful_across_difference`: cross_difference_respect AND cooperation_across_difference, both confirmed.
- `safe_collaborator`: non_harm AND consistency_under_stress.
- `growth_oriented`: willing_to_be_corrected AND values_reversal_present.
- `generous_under_difficulty`: generosity AND consistency_under_stress.
- `fair_and_cooperative`: fairness AND cooperation_across_difference.
- `principled_under_pressure`: cross_difference_respect AND consistency_under_stress.

Each composition specifies **tolerance thresholds**. Example: `unselfish_AND_untribal` may require both dimensions to exceed 0.75 on their respective scales.

### OR-Compositions (2 Dimensions, Disjunction)

Selected pairs where either dimension suffices:

- `cooperative_or_respectful`: cooperation_across_difference OR cross_difference_respect above 0.70.
- `helpful_or_principled`: generosity OR non_harm above 0.72.

### Weighted Combinations (Multi-Dimension, Scalar Aggregation)

Fixed weight schemes for combining 3+ dimensions:

- **Uniform**: Equal weight across all inputs. Example: (generosity + fairness + cooperation_across_difference) / 3 > 0.70.
- **Non-Harm-Emphasized**: non_harm gets 0.40; other dimensions 0.20 each. Models "above all, don't harm."
- **Cross-Respect-Emphasized**: cross_difference_respect gets 0.35; others 0.22 each. Models "diversity and dialogue first."
- **Generosity-Emphasized**: generosity gets 0.35; others 0.22 each. Models "abundance mindset."

### Negation-Pair Partners

Per Everest 62 (ban-list architecture), each dimension has a companion negation. Compositions may explicitly exclude negations:

- `genuinely_unselfish`: unselfish AND NOT jealousy_proxy.
- `true_cooperation`: cooperation_across_difference AND NOT tribal_enforcement.

Negation partners are pre-computed and included in the composition definition.

## Registration & Deployment

Each composition in the fixed table is a **first-class artifact**:

1. **Content-Addressed ID**: Derived from the composition definition, enabling stable references across versions.
2. **Dedicated ZK Circuit**: Compiled and optimized for that specific composition, not synthesized per-request.
3. **Test Corpus**: Curated examples and counterexamples for validation.
4. **Ethics Review**: Signed approval that the composition doesn't leak banned categories, doesn't create perverse incentives, and doesn't unfairly conflate unrelated values.
5. **Operator Documentation**: Guidance on when to offer the composition, tolerance defaults, and known failure modes.

### Request Format

A counterparty requests a composition proof via:

```
cwp.v0.values_composition("unselfish_AND_untribal", tolerance=0.75)
```

The operator:
1. Validates the composition name against the registry.
2. If registered, evaluates the subject's values against the composition's circuit.
3. Returns a proof bit (true/false) and metadata (confidence, circuit execution time).
4. If unregistered, returns `REQUEST_REFUSED` with a pointer to the published registry.

## v1+ DSL: Deferred

A Domain-Specific Language for values composition is **not shipped in v0**. It is **deferred until post-deployment evaluation**, with strict triggering criteria:

- At least 12 months of v0 deployment.
- Evidence that a fixed registry is insufficient (e.g., >15% of requests are unregistered queries).
- No loss of auditability in the proposed DSL.
- No introduction of side-channel risks.
- Formal grammar review by the ethics board and legal counsel.

If these criteria are met, a DSL might be designed with:
- Restricted grammar (only AND, OR, weighted aggregation; no nesting).
- Pre-compilation of all user-requested compositions before deployment.
- Per-composition ethics approval before circuit generation.
- Stable versioning of DSL syntax.

## Growth of the Registry

New compositions are added via the Everest 118 (Evolution Policy). Process:

1. **Proposal**: An operator, ethics stakeholder, or subject advocate proposes a new composition, documenting its use case and values intent.
2. **Review**: Ethics board, legal, and security audit the proposal.
3. **Circuit Generation**: If approved, a ZK circuit is compiled and tested.
4. **Registration**: The composition is added to the published registry.
5. **Announcement**: Operators are notified; counterparties gain access.

Individual ad-hoc compositions are **not available on demand**. Counterparties cannot request, "Create a proof for (generosity AND jealousy_rejection)"; instead, they must wait for a proposal-and-review cycle.

## Anti-Creativity-Leak

The fixed-registry design prevents counterparties from probing the system:

**Probe Attack Prevention**: A sophisticated counterparty could request novel compositions in sequence to reverse-engineer the dimensions' semantics or discover conflicts. E.g., "Can you prove fairness AND generosity? Now fairness AND jealousy? Now fairness AND non_tribal?" A fixed registry blocks this—unregistered queries are refused, and the attacker gains no information.

**Use-Case Anchoring**: Each registered composition has a documented purpose. This discourages frivolous additions and keeps the registry focused on real operational needs.

**Unregistered Query Handling**: When a counterparty requests an unregistered composition, the system:
1. Logs the request (for analytics and evolution policy input).
2. Returns `COMPOSITION_NOT_REGISTERED` with a link to the current registry.
3. Optionally: suggests similar registered compositions.

## Example Workflow

**Scenario**: A subject applies for a cross-tribal leadership role. The hiring counterparty requests proof of `respectful_across_difference`.

1. **Request**: `cwp.v0.values_composition("respectful_across_difference", tolerance=0.73)`.
2. **Validation**: Operator checks registry; composition exists with ID `cid:e119:resp_across_diff:v0.1`.
3. **Evaluation**: Operator runs the subject's evidence against the composition's ZK circuit.
4. **Output**: Proof = TRUE, confidence = 0.91, circuit_ms = 145.
5. **Counterparty Decision**: Uses the proof alongside other signals to make hiring decision.

In v1+, if evidence suggests a need for `respectful_across_difference_AND_adaptive_learning`, it would go through proposal-review-circuit-registration before becoming available.

## Constraints and Future Scope

This design intentionally favors **safety and auditability over expressivity**. Counterparties must choose from a curated set. This is a trade-off, and it is intentional. Over 12+ months, if the registry proves restrictive or if new use cases emerge, the decision to add a DSL can be revisited with full governance rigor.

Until then, v0 ships a fixed table. Each composition is auditable, verifiable, and resistant to probe attacks. The system prioritizes trust over convenience.

---

— Calm, 2026-05-20