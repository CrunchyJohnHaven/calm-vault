# Everest 195 — Insurance Prohibition Enforcement

**Summit:** 195/300 (ZKAC Range XIV)  
**Acceptance:** A documented mechanism detects insurance-class deployments and revokes the Calm-suite name for that counterparty.  
**Prereq:** 114 (Compass scope statement).  
**Honors:** [`CALM_REFUSAL_FLOOR_INDEX.md`](../CALM_REFUSAL_FLOOR_INDEX.md) §3 (use-case forfeits).

## Policy anchor

[`CALM_WITNESS_SCOPE_STATEMENT.md`](../CALM_WITNESS_SCOPE_STATEMENT.md) and [`everest_114_compass_scope_statement.md`](everest_114_compass_scope_statement.md) forbid insurance underwriting, pricing, claims adjudication, and coverage decisions. This summit defines **how operators detect and refuse** insurance-shaped counterparty classes before any predicate evaluates.

## Detection signals (v0)

A deployment is **insurance-class** if any of the following hold on the counterparty registration record:

1. **Declared class.** `counterparty_class` is one of: `insurer`, `insurance_broker`, `reinsurer`, `claims_adjuster`, `underwriting_platform`.
2. **Purpose lint.** Stated `purpose` or `AlignmentRequirement.purpose` contains tokens from the insurance lexicon (underwriting, premium, policyholder risk score, claims fraud, actuarial table, coverage denial).
3. **Predicate bundle.** Requested predicates are only meaningful in insurance workflows (e.g., batch scoring principals for premium tiers). The registry linter flags bundles that lack a non-insurance human-stated purpose.
4. **Infrastructure fingerprint.** Operator observes API traffic patterns consistent with batch eligibility screening (rate > 100 distinct principals / hour with no session-bound collaboration purpose).

Any single signal triggers **review**. Two independent signals trigger **automatic forfeiture** without human override.

## Enforcement actions

| Stage | Action |
| --- | --- |
| Review | Operator returns `refusal: insurance_class_suspected` with no envelope minted. |
| Forfeiture | Operator revokes Calm-suite trademark use for that counterparty DID; future verifies return `name_forfeited`. |
| Audit | `summit_bagged`-style operator log entry with hashed counterparty DID and signal codes only (no principal PII). |

## Reference linter (v0)

`~/CredexAI/calm_witness/prohibition_lint.py` implements `lint_counterparty_purpose(purpose: str) -> list[Issue]` and `is_insurance_class(counterparty_class: str) -> bool`. Gates and Concord `validate_requirement()` call the purpose linter so insurance-shaped alignment requests fail at requirement-validation time, not after disclosure.

## Non-goals

This summit does **not** provide legal advice or jurisdictional compliance mapping (see Everest 194/214). It provides a **technical forfeiture hook** aligned with the scope statement one-way ratchet.

## Acceptance evidence

Gate `everest_195_zkac_insurance_prohibition_gate.py` exit 0: doc present, linter module present, pytest on golden insurance-purpose strings returns `insurance_prohibited`.

## Follow-through

- **196–198:** Parallel prohibition shapes for employment, lending, and government classes (same linter framework).  
- **Foundation board:** Publish forfeiture appeals process (Everest 215 treaty draft Article IV).

— Musk
