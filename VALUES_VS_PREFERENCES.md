# Values vs Preferences — Calm ZKAC v0 Boundary

**Draft v0 · 2026-05-20 · Calm · Everest 110**

## Rule

**Preferences are not values.** Preferences (“I like chocolate”, “I prefer morning meetings”) must not enter `ValuesVector`, must not receive Pedersen commitments on the values path, and must not be exposed as alignment predicates.

**Values** are normative commitments about how one acts toward others — cooperation, fairness, honesty, non-harm, respect across difference, generosity, non-tribal engagement, repair, consistency under stress, and principal-authored extensions that pass the refusal floor.

## Why the fence exists

Without it, the values vector becomes a **personality and taste profile**. Counterparties would optimize for similarity scores (Concord §1), reintroduce tribal sorting, and incentivize over-disclosure. That is surveillance dressed as ethics.

## Enforcement

1. **Type system:** `ValuesVector` fields are fixed to the ten v0 dimension IDs; there is no `favorite_color` slot.
2. **Predicate vocabulary:** New predicate proposals that encode taste, aesthetics, or consumer preference are rejected at audit (PREDICATE_AUDIT_PROCESS_v0, Everest 54).
3. **Chain kinds:** `values_self_report` payloads list only `V0_DIMENSIONS`; preference-flavored keys in payload are schema-invalid.
4. **Concord:** Requirement patterns reference Compass/ZKAC predicates, not ad-hoc preference matching.

## Examples

| Claim | Classification |
|-------|----------------|
| “I prioritize not willfully harming others” | Value → `non_harm` dimension / harm-absence predicates |
| “I cooperate across cultural lines” | Value → `non_tribal_engagement`, `cross_difference_respect` |
| “I like spicy food” | Preference → out of scope |
| “I vote for party X” | Protected / contentious → **refused** (not preference) |

## Principal-authored other (Everest 117)

The tenth dimension is **not** a preference slot. It is a declared normative axis the principal names in prose (e.g., “truth-telling under oath”) subject to the same refusal floor as any new predicate.
