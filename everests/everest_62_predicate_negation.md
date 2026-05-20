# Everest 62 — Predicate Negation

*Phase V — Predicate Authoring. Prereq: Everest 61.*

## The Challenge

In a tri-valued logic system, negation is not straightforward. The Calm Witness protocol must disambiguate three distinct cases:

1. **Naive confusion**: "¬p is True" collapsing to "p is False." In reality, predicates return True, False, or Indeterminate. Negation of Indeterminate is not automagically True — it remains Indeterminate.

2. **Absence vs. negation**: If a counterparty lacks evidence that `p = True`, that does not constitute proof of `¬p`. The distinction matters: absence of consent, absence of a request, or absence of authorization are not proofs of negation; they are absences.

3. **Enumeration risk**: Certain predicates are structurally one-sided. Revealing their negation can leak the underlying positive bit. Example: `not_bank_teller_note_active` discloses the duress signal when the result is False.

The protocol must provide a formal model for negation that preserves tri-value semantics, supports composition (Everest 61), and identifies which negations are unsafe to register.

## Design Decision: Explicit Negation Predicates

Rather than introducing a unary NOT combinator, v0 models negation at the predicate registry level. Every base predicate has a designated companion negation predicate with its own predicate_id, content-addressed identifier, reference implementation, and test corpus.

### Why Not a NOT Combinator?

Everest 61 defines combinators as operations over a flat list of predicates (AND, OR). A unary NOT combinator would require either nesting (which v0 rejects) or a special-case unary operator. Modeling negation as a registry-level pairing is cleaner:

- Each negation predicate is evaluated independently with its own witness and proof circuit.
- Tri-value handling is explicit: the negation predicate's code directly specifies how Indeterminate maps.
- ZK proof construction avoids the conceptual overhead of "proving non-existence."
- Negations participate in composition uniformly alongside base predicates.

### Naming Conventions

- **Canonical form**: `not_<predicate_name>`. Example: `not_in_baseline_24h`, `not_mental_state_unusual`.
- **Domain-specific clarity**: Where a more specific name conveys the intent, use it. Example: `biometric_mismatch_beyond(τ)` instead of `not_biometric_match_within(τ)`. Both are negations; the domain name is more readable.

### Tri-Value Semantics for Negation

A negation predicate `¬p` evaluates as follows:

| p evaluates to | ¬p evaluates to | Rationale |
|---|---|---|
| True | False | Standard negation. |
| False | True | Standard negation. |
| Indeterminate | Indeterminate | Preserves uncertainty. "We don't know p" implies "we don't know ¬p." |

This semantics ensures that Indeterminate is a stable, meaningful third state. It is not collapsed to True or False by negation. If a predicate's evaluation is incomplete, unknown, or ambiguous, its negation preserves that ambiguity.

## Registration in the Predicate Registry (E53)

Each predicate specification includes a `negation_predicate_id` field:

- If `negation_predicate_id` is populated, the negation is registered as a queryable predicate.
- If `negation_predicate_id` is null or the predicate is flagged as "no negation allowed," the negation is not registered.
- The registry enforces a whitelist: negations that have been reviewed and flagged as unsafe (Everest 54) are rejected at registration time.

Each registered negation predicate has its own entry in the registry with:
- Unique `predicate_id`.
- Content-addressed identifier (derived from its specification).
- Reference implementation (usually the positive predicate's code with output negated, but sometimes a distinct circuit).
- Test corpus validating tri-value behavior.
- Consent and authorization requirements (separate from the positive predicate).

## Consent and Authorization Semantics

**Key principle**: Consent for `p` does NOT imply consent for `¬p`. These are separate consent records.

**Justification**: A counterparty might be authorized to learn "principal is in baseline" (True/False) but NOT authorized to learn "principal is not in baseline." The information flows and downstream implications are different. Likewise, a principal might grant disclosure of a negative predicate but not the positive form.

**In practice**: Principals often grant or deny both (or neither) together. But the protocol does not conflate them. Each predicate — positive or negated — requires its own explicit consent check.

## Predicate Pairs in v0

### Registered Negations

**in_baseline_24h** ↔ **not_in_baseline_24h**
- Both registered. Standard use case.
- Tri-value semantics fully applied.
- Composition with AND/OR is straightforward.

**biometric_match_within(τ)** ↔ **biometric_mismatch_beyond(τ)**
- Both registered. Domain-specific naming for clarity.
- Symmetric: mismatch_beyond is the meaningful negation.
- Tri-value semantics: if match_within is Indeterminate, mismatch_beyond is also Indeterminate.

**cognitively_atypical_baseline** ↔ **cognitively_typical_baseline**
- Both registered. Cognitive baseline is informative in both directions.
- Typical is the default state; atypical is marked. Neither is inherently private.

**mental_state_unusual** ↔ **mental_state_typical**
- Both registered. Companion to cognitive baseline.
- Symmetric disclosure: both directions are equally safe to reveal.

### Banned Negations

**principal_does_not_consent_to_disclose** (negation of `principal_consents_to_disclose`)
- NOT registered. Disclosing this is an enumeration probe: if False, the counterparty learns the principal granted consent.
- Only the positive form (`principal_consents_to_disclose`) is queryable.

**not_bank_teller_note_active** (negation of `bank_teller_note_active`)
- NOT registered. CRITICAL safety issue.
- The bank teller note is a unilateral duress signal. If the principal is under duress, `bank_teller_note_active` returns True. If not under duress, it returns False (or Indeterminate if not configured).
- Disclosing `not_bank_teller_note_active = True` leaks "no duress signal active" — which is safe.
- Disclosing `not_bank_teller_note_active = False` leaks "duress signal IS active" — a critical safety breach.
- To preserve the principal's safety, only the positive form is queryable. A counterparty cannot ask "is the duress flag NOT set?" because that question is itself a probe.

### General Rule for Negation Review (E54)

Safety-critical predicates have their negations reviewed on a case-by-case basis. The registry documents which negations are banned and why. Decisions are:

- **Transparent**: All bans and their justifications are public within the protocol.
- **Revocable**: If threat models or use cases change, negations can be added to the registry (or removed).
- **Predictable**: The rule is not arbitrary: negations are banned when disclosing them (or their absence) would leak a protected bit.

## Composition with Everest 61 (AND/OR)

Negation predicates participate uniformly in composition:

```
(in_baseline_24h AND not_mental_state_unusual) 
```

This is valid. The composition operator treats both predicates as base predicates. The evaluation is:
1. Evaluate `in_baseline_24h` → returns True, False, or Indeterminate.
2. Evaluate `not_mental_state_unusual` → returns True, False, or Indeterminate.
3. Apply AND: both must be True for the conjunction to be True.

Tri-value propagation in AND/OR follows standard three-valued logic (Kleene):
- `True AND Indeterminate = Indeterminate`
- `False AND Indeterminate = False`
- `True OR Indeterminate = True`
- `False OR Indeterminate = Indeterminate`

## Worked Examples

### Example 1: Simple Negation with Consent

Counterparty C requests `not_in_baseline_24h`. The principal has explicit consent for that predicate in their authorization record.

Operator evaluates `in_baseline_24h` (the underlying positive predicate):
- **Case 1**: `in_baseline_24h` returns True → `not_in_baseline_24h` returns False. Proof of False is returned. Counterparty learns "principal IS in baseline."
- **Case 2**: `in_baseline_24h` returns False → `not_in_baseline_24h` returns True. Proof of True is returned. Counterparty learns "principal is NOT in baseline."
- **Case 3**: `in_baseline_24h` returns Indeterminate (e.g., data unavailable) → `not_in_baseline_24h` returns Indeterminate. Proof of Indeterminate is returned. Counterparty learns "we don't know."

In all cases, the proof is sound and the result is well-defined.

### Example 2: Negation in Composition

Counterparty asks for `in_baseline_24h AND not_cognitively_atypical_baseline`. Both predicates are required for the conjunction to be True.

- If `in_baseline_24h = True` and `cognitively_atypical_baseline = False` (so `not_cognitively_atypical_baseline = True`), the conjunction is True.
- If either predicate is False or Indeterminate, the conjunction is not True.

The proof circuit evaluates both predicates and returns a proof of the conjunction's result.

### Example 3: Banned Negation Security Case

Counterparty attempts to request `not_bank_teller_note_active`.

The registry lookup fails: this negation is not registered. The operator rejects the request with a "predicate not found" error. The counterparty cannot query whether the duress flag is NOT set, preserving the principal's safety. If a duress signal is active and the counterparty were allowed to query its negation, a False result would leak the signal to the counterparty.

## Implementation Notes

**Predicate specification format**:
Each predicate in the registry includes:
- `predicate_id`: unique identifier for the base predicate.
- `negation_predicate_id`: identifier of the negation predicate (null if no negation is registered).
- `negation_allowed`: boolean flag; if False, the registry refuses to register any negation companion.
- `negation_ban_reason`: free-text explanation (e.g., "enumeration probe risk", "unilateral safety signal").

**Reference implementation**:
The negation predicate's implementation typically inverts the output bit of the positive predicate:
```
not_in_baseline_24h(witness, config):
  result = in_baseline_24h(witness, config)
  if result == True:
    return False
  elif result == False:
    return True
  else:
    return Indeterminate
```

In some cases, the negation predicate requires a distinct circuit (e.g., `biometric_mismatch_beyond` may have different witness structure or tolerance parameters than `biometric_match_within`).

**Proof circuit**:
Each negation predicate has its own ZK proof circuit. In the simple case, the circuit is the positive predicate's circuit with the output bit negated. The witness is the same. The proof is sound: a verifier can check that the negation was computed correctly.

## Summary

Everest 62 establishes negation in the Calm Witness protocol as a registry-level construct, not a combinator. Each base predicate has an optional companion negation predicate with its own predicate_id and consent requirements. Tri-value semantics are explicit: Indeterminate remains Indeterminate under negation. Safety-critical predicates' negations are reviewed and may be banned to prevent enumeration probes and unilateral safety signal leaks. Negation predicates compose uniformly with base predicates in AND/OR operations (Everest 61).

— Calm, 2026-05-20
