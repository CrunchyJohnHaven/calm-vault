# Values Vector Publication Policy v0

**Hard rule · Everest 124 · 2026-05-20**

## Policy

The **full values vector never leaves the principal's vault.**

Counterparties receive only:

- Single-bit (or structured Concord requirement) predicate outcomes authorized by consent.
- Cryptographic bindings: fingerprints, per-dimension Pedersen commitments, Σ-protocol / range-proof artifacts that prove statements **without** revealing magnitudes.
- Chain-head and session nonces per Calm Witness wire format.

They do **not** receive:

- Raw dimension scalars in JSON, logs, transcripts, or analytics exports.
- Similarity scores, ranking percentiles, or “how aligned” numerics (Concord anti-purity-test).
- Cross-principal comparison vectors.

## Chain representation

`values_self_report` records carry `fingerprint`, `dimensions` (names only), `commitments`, and optional principal `note` — **not** scalar values. Openings `(m, r)` live in operator-local storage (`save_opening_to_vault`, mode `0600`).

## Corrections

`values_correction` records amend a prior self-report by seq reference; they carry a new fingerprint and commitment set, not retroactive plaintext edits.

## Violation response

Reference verifiers MUST reject envelopes that embed full vectors. Predicate registry MUST tombstone any ID that leaks magnitudes. Scope statement ratchet applies: uses in employment, lending, insurance, custody, immigration, or aggregate analytics forfeit the Calm-suite name.

## Implementation anchor

`~/CredexAI/calm_witness/values.py` — `to_chain_payload()`, `make_self_report_record()`, tests `test_self_report_record_does_not_leak_values`.
