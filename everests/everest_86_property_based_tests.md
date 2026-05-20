# Everest 86 — Property-Based Tests for Hash Chain (and E87 for Predicates)

*Phase VII — Engineering Reliability. Prereq: Everest 28 (chain verifier).*

Beyond example-based unit tests (E26 / E28), the chain and the predicates ship with property-based tests that exercise random inputs against algebraic invariants. v0 uses stdlib `random` with fixed seeds — no Hypothesis dependency. Two summits in one doc: E86 (chain properties) and E87 (predicate properties).

## §1. Artifact

[`../calm_witness/test_composition_and_properties.py`](../calm_witness/test_composition_and_properties.py) — `ChainPropertyTests` (E86) + `PredicatePropertyTests` (E87) + `CompositionTruthTables` (E61).

## §2. Chain invariants (E86)

| # | Property | Verified by |
|---|---|---|
| C1 | Any sequentially-built chain verifies cleanly | `test_random_chain_always_verifies` over 100 random records |
| C2 | Any single byte flip in any payload invalidates the chain | `test_any_single_byte_flip_breaks_chain` over 20 records |
| C3 | (future) Canonical encoding is byte-stable across reorderings | future test against shuffled-key inputs |
| C4 | (future) Empty chain is rejected | E28 already handles; explicit property test in v0.1 |
| C5 | (future) seq=0 record is rejected | E28 already handles |

C1 and C2 are bagged. C3–C5 add to coverage as we ship.

## §3. Predicate invariants (E87)

| # | Property | Verified by |
|---|---|---|
| P1 | `in_baseline_24h(x, t)` is deterministic — same inputs → same outputs | `test_in_baseline_is_deterministic` over 50 iterations |
| P2 | `PredicateValue` enum is closed — every value is in `{true, false, unknown, refused}` | `test_predicate_value_enum_closed` |
| P3 | (future) `in_baseline_24h(x)` and `not(in_baseline_24h(x))` cannot both be `true` | trivially given P1; explicit test added when E62 negation ships |
| P4 | (future) Adding a stale record never changes a `true → false` outcome | requires temporal property generator |
| P5 | (future) `compose_and([p, p, p])` == `p` for any `p ∈ {T, F, U, R}` (idempotence) | trivial given §61's value-set logic |

P1–P2 are bagged. P3–P5 are tractable in v0.1.

## §4. Composition invariants (E61, included here)

| # | Property | Verified by |
|---|---|---|
| K1 | REFUSED is absorbing under both AND and OR | `test_refused_is_absorbing` |
| K2 | Negation is involutive on TRUE / FALSE | `test_double_negation_when_true_or_false` |
| K3 | Negation preserves UNKNOWN and REFUSED | `test_negation_preserves_unknown_and_refused` |
| K4 | Full AND truth table holds | `test_and_truth_table` |
| K5 | Full OR truth table holds | `test_or_truth_table` |

## §5. Why stdlib-only

Hypothesis is the standard Python property-test framework, but it's a PyPI dependency. v0 is stdlib-only; we get most of Hypothesis's value (random seed + invariant + counterexample shrinking when manual) with `random.Random(seed)` plus deliberate iteration counts. Counterexample minimisation is manual but rare — when an invariant fails, the failing seed is part of the test's source code, so the failure is reproducible across runs.

v0.1 may add an optional Hypothesis path under `[test_extra]` install group, but the stdlib path remains the floor — no one needs PyPI access to run the test suite.

## §6. Seed policy

Each property test pins its `SEED` constant in the class body. Failures must include the seed so the reporter can reproduce. Updating a seed requires a documented reason (e.g., found a new edge case that the previous seed missed); blind seed-rotation to "make tests pass" is forbidden.

## §7. Acceptance test

```bash
$ python3 calm_witness/test_composition_and_properties.py 2>&1 | tail -3
Ran 9 tests in 0.001s
OK
```

9 property tests pass on the canonical seeds. Full suite (40 tests across 3 files) passes:

```bash
$ python3 -m unittest discover -p "test_*.py" 2>&1 | tail -3
Ran 40 tests in <0.01s
OK
```

— Calm, 2026-05-20
