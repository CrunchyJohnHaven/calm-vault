# Calm Compass — Counter-Claim Protocol v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 111 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §2.4, [`COMPASS_EVIDENCE_CEREMONY_v0.md`](COMPASS_EVIDENCE_CEREMONY_v0.md) §4.**

## §1 — Purpose

Third parties may allege that a principal committed **willful harm** within a named window. The counter-claim protocol governs how those allegations enter the principal's vault chain, how the principal may rebut them, and how the `cwp.compass.v0.no_known_willful_harm_in_window_365d` predicate exposes a **disputed** state without turning Compass into a criminal-record proxy.

Counter-claims are **attributed**, **time-bounded**, and **refutable**. Anonymous harm allegations are rejected at intake.

## §2 — Actors

| Actor | Role |
|-------|------|
| **Principal P** | Subject of the allegation; may author `principal_rebuttal` records on their own chain. |
| **Claimant Q** | Third party filing `compass_evidence.counter_claim`; MUST hold a CredexAI-issued VC ID used as `claimant_id`. |
| **Operator (P's)** | Stores P's chain; surfaces active counter-claims to P; never suppresses attributed claims. |
| **Operator (Q's)** | Accepts Q's counter-claim submission via audit-mediated channel; signs Q's record on Q's chain (not P's). |
| **Audit panel** | Mediates intake, adjudicates substantiation after rebuttal window (Everest 115); outcome may be logged as panel record. |
| **Verifier** | Reads predicate bit + `disputed` annotation from a Compass disclosure envelope; never sees full narratives unless P consents (Everest 112). |

## §3 — Record shapes (v0)

Defined in [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §3:

- `compass_evidence.counter_claim` — authored by Q (via Q's operator), references P in narrative only; chained on a channel that links to P's vault head via audit process.
- `compass_evidence.principal_rebuttal` — authored by P on P's chain; `targets_counter_claim_seq` MUST match an in-window claim.

Mandatory counter-claim fields:

- `claimant_id` — non-empty CredexAI VC ID (full attribution).
- `alleged_harm_narrative` — non-empty string.
- `alleged_harm_window` — ISO `from` / `to` bounds.
- `submitted_via` — MUST be `audit-process-mediated` for v0.

## §4 — Filing flow

1. **Intake.** Q submits allegation through the audit-panel counter-claim channel (not direct write to P's chain). Panel triages for refusal-floor violations (Everest 113) and spam patterns.
2. **Publication.** On accept, Q's operator appends a signed `counter_claim` record; P's operator ingests a **notification pointer** (seq, claimant_id hash, window) into P's vault metadata — the full narrative is visible to P, not to verifiers by default.
3. **Grace window.** For `rebuttal_window_days` (default **30**), an unrebutted claim does **not** flip the harm bit. P may author `principal_rebuttal` at any time during grace.
4. **Activation.** After grace, if no substantive rebuttal targets the claim seq, the claim becomes **active** and the predicate returns `bit=false`, `disputed=true`.
5. **Rebuttal.** A substantive rebuttal (`rebuttal_narrative` non-empty, correct `targets_counter_claim_seq`) removes the claim from the active set immediately — no panel wait required for deactivation.
6. **Adjudication (optional).** Panel may later mark claims substantiated / not substantiated; v0 evaluator uses chain records only; panel records are reserved for v1 policy hooks.

## §5 — Predicate semantics (reference implementation)

The normative evaluator is:

`~/CredexAI/calm_witness/compass_eval.py`

- `no_known_willful_harm(chain_records, now_iso) -> HarmStatus`
- `no_known_willful_harm_bit(...) -> bool` (convenience wrapper)

`HarmStatus` fields:

| Field | Meaning |
|-------|---------|
| `bit` | `True` iff zero active unrebutted counter-claims in the 365d window |
| `disputed` | `True` iff at least one active unrebutted counter-claim exists |
| `active_counter_claim_seqs` | Sorted seq ids of active claims |

**Active claim** = in 365d window + mandatory attribution present + past rebuttal grace + no matching substantive `principal_rebuttal`.

Claims without `claimant_id`, outside the window, or inside grace are ignored. Wrong-target or empty-narrative rebuttals do not clear a claim.

Golden tests: `~/CredexAI/calm_witness/test_compass_eval.py` (Everest 109 + 117 corpora).

## §6 — Disclosure to counterparties

- Default: verifiers receive the **boolean harm bit** and, when `disputed`, a `disputed: true` annotation — not Q's narrative, not P's rebuttal text.
- Under principal consent, a **redacted evidence sketch** may be released per [`COMPASS_FALSIFIABILITY_PROTOCOL_v0.md`](COMPASS_FALSIFIABILITY_PROTOCOL_v0.md).
- If Calm Witness duress bit is active in the same envelope, Compass predicates downgrade to **Unknown** (composition rule in COMPASS_PREDICATES §6).

## §7 — Abuse controls

- **Anonymous claims** rejected (no `claimant_id`).
- **Refusal floor** rejects predicates or evidence kinds that proxy race, religion, criminal record, etc. (canonical list: COMPASS_PREDICATES §4).
- **Rate limits** on Q filings per principal per rolling year (operator policy; default max 3 accepted intakes).
- **Anti-purity-test:** counter-claims MUST NOT be used to enforce "values similarity" requirements; see [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) §4.

## §8 — Versioning

v0 grace window = 30 days; claim window = 365 days. Tightening may add fields; loosening attribution requirements is forbidden.

— Musk, 2026-05-20
