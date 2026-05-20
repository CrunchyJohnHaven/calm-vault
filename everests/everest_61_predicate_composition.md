# Everest 61 — Predicate Composition (AND/OR)

*Phase V — Predicate Authoring. Prereq: Everest 55.*

## Overview

Predicate composition enables a verifier to request multiple table-predicates combined via logical operators (AND, OR) in a single proof, without requiring separate disclosures for each predicate. The prover bundles individual predicate evaluations and proves the combinator is honestly applied. The verifier observes only the final composed result, preserving selective disclosure: the counterparty learns that a conjunction holds, but not which individual predicates passed or failed.

Composition in v0 is **not a domain-specific language**. It is a structured request format naming multiple predicates and exactly one top-level combinator. No nesting, no parentheses, no negation (negation is Everest 62). This constraint keeps verifier semantics minimal and proof structures tractable.

## Semantics

### What Composition Is Not

- Not a DSL. No operator precedence, associativity, or parenthetical nesting.
- Not a way to combine arbitrarily complex expressions. A composition is a flat list of predicates under one combinator.
- Not a separate consent grant. Composing predicates derives directly from individual consents for each predicate in the list.

### Allowed Combinators

In v0: **AND** (conjunction) and **OR** (disjunction). Each composition has exactly one combinator applied to two or more predicates.

- **AND**: final result is True only if all predicates evaluate to True.
- **OR**: final result is True if at least one predicate evaluates to True.

### Evaluation Semantics

Each predicate p_i in the composition is evaluated independently over a frozen chain head (Everest 63), producing:
- A bit b_i (True or False).
- A freshness value freshness_i (seconds since evaluation).

**For AND:**
- `final_bit = b_1 ∧ b_2 ∧ ... ∧ b_n`
- `final_freshness = min(freshness_i)` — the composition is as fresh as its stalest component.

**For OR:**
- `final_bit = b_1 ∨ b_2 ∨ ... ∨ b_n`
- `final_freshness = max(freshness_i over predicates that returned True)` — only the True predicates contribute to freshness.

**Indeterminate handling:** If any predicate returns Indeterminate (evaluation error, blocked consent, missing data), the composition returns Indeterminate. This preserves tri-value semantics and prevents false confidence in partial results.

## Request Format

A composition proof request conforms to:

```json
{
  "combinator": "AND" | "OR",
  "predicates": [
    { "predicate_id": "in_baseline_24h", "parameters": {} },
    { "predicate_id": "biometric_match_within", "parameters": { "threshold": 0.3 } }
  ],
  "freshness_window": 3600,
  "nonce": "<bytes>",
  "counterparty_vc": "<vc>"
}
```

This format composes with Everest 66 (proof generator interface) and later extensions. Each predicate in the list is identified by its predicate_id and parameters; the request specifies one combinator and a freshness window applying to the final result.

## Proof Structure and Verifier View

**What the prover produces:**
- Individual proofs for each predicate p_i, each proving (b_i, freshness_i) under the same proof timestamp.
- A composition proof asserting that the claimed combinator is honestly applied to the bits b_i.
- A bundle containing all individual proofs and the composition proof.

**What the verifier observes:**
- The combinator (AND or OR).
- The list of predicates requested.
- The final bit (`final_bit`).
- The final freshness (`final_freshness`).
- Proof artifacts validating the entire bundle.

**What the verifier does NOT observe:**
- Individual bit values b_i.
- Individual freshness values freshness_i.

This asymmetry is the core of selective disclosure: a counterparty requesting `in_baseline_24h ∧ biometric_match_within(0.3)` learns only that the conjunction holds. If one predicate fails, the verifier sees a False result but cannot infer which condition failed—both AND and OR fail differently, preventing inference attacks.

## Proof Circuit

Each predicate's evaluation circuit produces a committed bit (zero-knowledge proof of the predicate result). The composition circuit takes these committed bits as input and outputs the result of applying the combinator.

The verifier checks:
1. That each predicate's circuit is valid.
2. That the composition circuit correctly applies the combinator to the inputs.

No exposures of individual bits in the proof transcript; the composition circuit wires commited values directly.

## Consent Gating

To request a composition `p_1 ∧ p_2 ∧ ... ∧ p_n`, the counterparty must hold valid consent for each predicate p_i individually. There is no separate "consent for composition"—composing derives directly from the intersection of individual consents.

If consent is missing for even one predicate in the list, the composition is refused entirely. No partial results are returned; this prevents information leakage through partial compliance.

### Special Handling: bank_teller_note_active

The predicate `bank_teller_note_active` (Everest 58) carries safety semantics: a True result indicates duress or unusual circumstances requiring intervention. When composed:

**Allowed:**
- **Alone**: request only `bank_teller_note_active` without composition.
- **In OR**: request `bank_teller_note_active OR mental_state_unusual`. If either flags a safety concern, the verifier's safety policy is triggered.

**Restricted in AND:**
- `bank_teller_note_active AND biometric_match_within` is allowed only if the principal has explicitly consented to this composition. Individual consent for both predicates is necessary but not sufficient.
- **Justification**: AND with `bank_teller_note_active` creates semantic risk. A True AND result could mean "principal under duress AND biometric matched," implying the principal is forced to transact. Composing with AND "bleeds" the duress signal into the result. Explicit composition consent ensures the principal understands the semantics.

Default policy: `bank_teller_note_active` in AND requires explicit principal consent for the composition; in OR it does not (OR is a "anything wrong" sweep and duress is one possible flag).

## Per-Predicate Determinism

All predicates in a composition are evaluated against the same frozen chain head and proof timestamp. This ensures:
- Deterministic evaluation: the same chain head and timestamp always produce the same result.
- Consistency within the composition: no divergence due to re-evaluation.
- Proof validity: the prover can prove the composition snapshot honestly.

See Everest 63 (chain head freezing) for details on how chain head snapshots are committed.

## Composition Limits in v0

- **Maximum 4 predicates per composition**: prevents proof bloat and keeps verification time bounded.
- **Exactly one top-level combinator**: no nesting or complex expressions.
- **No negation** (Everest 62 adds NOT): v0 compositions cannot express `p_1 ∧ ¬p_2`.

These limits are v0 constraints; future versions may relax them after analysis of proof size and verification overhead.

## Worked Examples

**Example 1: Simple AND.**
Counterparty A requests `(in_baseline_24h AND biometric_match_within(0.3))`. Both predicates are evaluated. If both return True, final_bit = True, final_freshness = min of the two freshness values. Counterparty learns only that the conjunction holds; cannot infer individual results.

**Example 2: OR for Safety Sweep.**
Counterparty B requests `(bank_teller_note_active OR mental_state_unusual)`. If either predicate returns True, final_bit = True, final_freshness = max of the True predicates' freshness. Counterparty's safety policy triggers without learning which condition flagged the concern.

**Example 3: Invalid Composition (NOT yet available).**
Counterparty C requests `(in_baseline_24h AND NOT cognitively_atypical_baseline)`. This is invalid in E61 because negation (NOT) is Everest 62, not yet bagged. Composition currently supports AND/OR only. Request is rejected.

**Example 4: AND with bank_teller_note_active (no explicit composition consent).**
Counterparty D requests `(in_baseline_24h AND bank_teller_note_active)` but has not provided explicit composition consent. The request is refused. Counterparty must either provide composition consent or request `bank_teller_note_active OR in_baseline_24h` instead.

## Failure Modes

**Missing consent:** If the counterparty lacks valid consent for any predicate in the composition, the entire request is refused. No Indeterminate result; no partial information.

**Predicate evaluation error:** If any predicate p_i returns Indeterminate (missing data, blocked consent, evaluation timeout), the composition returns Indeterminate. This preserves tri-value semantics and avoids false confidence. The verifier cannot distinguish "one predicate timed out" from "composition intentionally undefined"; indeterminacy is opaque.

**Proof circuit validation failure:** If the composition circuit does not correctly apply the combinator, proof verification fails and the verifier rejects the result.

## Privacy Analysis

A counterparty observing a composition result learns:
- The combinator (AND or OR).
- The final bit and freshness.
- Which predicates were requested.

A counterparty **cannot** learn:
- Individual bit values b_i.
- Which predicate(s) caused a False result in AND.
- Which predicate caused a True result in OR (if multiple True).

**Adversarial scenario:** An attacker cannot distinguish `(p_1 ∧ p_2 = False)` from `(p_1 ∨ p_2 = False)` by observing the result alone; the final bit and freshness are identical. The attacker learns which predicates were composed, but not their individual results.

**Information leakage per combinator:**
- **AND**: The verifier learns the worst-case (minimum) freshness, bounding how old the stalest predicate is. This leaks timing granularity but not the individual predicate results.
- **OR**: The verifier learns the best-case (maximum) freshness among True predicates. Again, timing granularity leaks; individual True/False results do not.

## Cross-References

- **Everest 51** (Predicate Language): defines individual predicates and table schemas.
- **Everest 55** (In Baseline, 24h): example predicate; required for composition examples.
- **Everest 57** (Principal Consents to Disclose): consent gating model.
- **Everest 58** (Bank Teller Note, Active): safety predicate; special AND handling in this everest.
- **Everest 62** (Predicate Negation): NOT operator; not supported in E61.
- **Everest 63** (Frozen Chain Head): deterministic evaluation semantics.
- **Everest 65** (Proof Generator): circuit and proof generation.
- **Everest 66** (Proof Request Interface): request/response format.
- **Everest 71** (Selective Disclosure): privacy and information leakage framework.

---

— Calm, 2026-05-20
