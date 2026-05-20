# Calm ZKAC — Values Dimensions v0

**Draft v0 · 2026-05-20 · Calm**
**Everest 107 · Companion:** [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), [`~/CredexAI/calm_witness/values.py`](../../CredexAI/calm_witness/values.py)

This document is the canonical semantics layer for the ten v0 dimensions in `ValuesVector`. Each dimension is a fixed-point scalar in `[0, 10000]` representing `[0.0, 1.0]` on the chain-facing side; **raw scalars never appear on the append-only log** (only fingerprints and per-dimension Pedersen commitments — see Everest 124).

## Non-universal caveat

These dimensions are **one principal's articulation of what matters for cooperation**, informed by cross-cultural moral-psychology literature (Haidt Moral Foundations, Schwartz Value Survey, Inglehart–Welzel). They are not a tribunal, not a personality test, and not a substitute for protected-category inference. Counterparties choose tolerances; principals choose self-reports and action evidence.

## Canonical order (immutable in v0)

| # | ID | Definition | Operational measurement note |
|---|-----|------------|------------------------------|
| 1 | `cooperation` | Sustained joint action with others toward shared ends without extracting unilateral advantage. | Increments when chain contains `cooperation_record` / joint-action narratives with corroboration; decrements on documented free-riding or sabotage (Everest 109 inference layer). |
| 2 | `fairness` | Equitable treatment across relationships — reciprocity without score-keeping obsession. | Self-report + witness attestations on dispute-resolution and resource-splitting records; no numeric “fairness score” disclosed (Concord §4). |
| 3 | `honesty` | Alignment between stated and revealed positions over time. | Gap between `values_self_report` commitments and action-inferred scores (Everest 109); surfaced as disagreement bit, not magnitudes. |
| 4 | `non_harm` | Absence of **willful or reckless** harm to others (intent required per user framing and `HARM_INTENT_VS_EFFECT.md`). | Harm-absence predicate family (`cwp.v0.no_*_harm_evidence`); accidents and negligent-only records do not trip v0 harm predicates. |
| 5 | `cross_difference_respect` | Respectful engagement with people who differ on culture, belief, neurology, or practice. | `cross_difference_record` + optional two-party corroboration; maps user priority “respectful to people who are different.” |
| 6 | `generosity` | Giving without immediate quid pro quo. | `cooperation_record` / gift narratives; maps user priority “unselfish.” |
| 7 | `non_tribal_engagement` | Cooperation across ideological or cultural in-group lines. | Cross-tribe interaction evidence; maps user priority “untribal.” |
| 8 | `repair_after_harm` | Restitution and restorative-justice follow-through after documented harm. | `harm_reversal` records (Everest 163) and repair narratives; pairs with harm taxonomy. |
| 9 | `consistency_under_stress` | Values held when costly — not only in easy contexts. | Stress-context tags on self-reports (Everest 135 extension); v0 uses single-context vector. |
| 10 | `principal_authored_other` | Principal-defined dimension slot; semantics declared in the record note. | Must not encode protected categories (PREDICATE_VOCABULARY §4); registry entry per Everest 117 for v1+. |

## Serialization (Everest 114)

Canonical bytes: domain separator `calm-zkac/values-vector/v0`, schema version `0`, dimensions sorted by **name** (not display order), each as `len(name) || name || u32_be(value)`. Fingerprint = SHA-256(canonical bytes). Reference: `ValuesVector.to_canonical_bytes()` and `fingerprint_canonical_bytes_test_vector()` in `values.py`.

## Refusal floor

No dimension may be defined to measure race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations-to-causes, contentious opinion, cross-principal comparison, or predictive group membership. `principal_authored_other` is not a loophole — tombstone on audit.

## Related

- Everest 106 — `ValuesVector` type
- Everest 108 — `values_self_report` / `values_correction` chain kinds
- Everest 124 — publication policy (vector never leaves vault)
- Everest 126–130 — alignment metric and `cwp.v0.values_aligned_within`
