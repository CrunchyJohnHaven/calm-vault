# Calm Compass — Scope Statement

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 114 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Structural mirror of [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md).**
**Prereq: canonical refusal floor — [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4 / [`COMPASS_REFUSAL_FLOOR_v0.md`](COMPASS_REFUSAL_FLOOR_v0.md).**

## §1 — What Calm Compass IS for

Calm Compass lets one autonomous AI agent disclose a **small set of principal-authorized values bits** to another agent — whether the principal's chained behavioral evidence supports named predicates (unselfish acts, cross-group engagement, refused harm, respect across difference, absence of active harm claims, willingness to be corrected).

Each predicate has explicit semantics, a pure evaluator, a `not_for` list, and a per-counterparty-class consent matrix in [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md).

The intended use is **agent-to-agent collaboration calibration** after Calm Pact alignment: adjusting trust, friction, or scope of joint work when values evidence matters — without exposing vault narratives, biometrics, or refusal-floor categories.

## §2 — What Calm Compass IS NOT for

Calm Compass is **categorically not for**, and any deployment using the name that violates this list forfeits trademark use under the same Apache-2.0 + scope discipline as Calm Witness (Everest 4):

1. **Law-enforcement surveillance.** No governmental counterparty class defaults to allow. Compass MUST NOT build dossiers or compel values disclosure for investigations.

2. **Employment screening or termination.** No employment counterparty class. Values bits MUST NOT inform hiring, promotion, firing, or compensation.

3. **Insurance underwriting or claims adjudication.** Compass predicates MUST NOT inform pricing, coverage, or claims decisions.

4. **Lending or credit decisions.** The `financial` class is for transactional verification, not creditworthiness or scoring.

5. **Medical diagnosis or clinical decision-making.** Compass is behavioral-values evidence, not clinical assessment.

6. **Child welfare, custody, or family-court proceedings.** Compass disclosures MUST NOT be admitted as fitness or custody evidence.

7. **Immigration adjudication.** Compass MUST NOT inform visa, asylum, or border-control decisions.

8. **Predictions about future behavior.** No predictive predicates (refusal floor §4 item 11). No decision may rely on inferred future harm or future values.

9. **Aggregation across principals for population-level claims.** Per-session, per-principal disclosure only; population statistics require separate de-identified study designs (IRB), not Compass envelopes.

10. **Marketing or advertising targeting.** Values bits MUST NOT select or score audiences for ads.

11. **Purity testing or tribal sorting.** Numeric "values similarity scores" and degenerate all-predicate thresholds are structurally refused — [`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) §4.

## §3 — What enforces the scope

### §3.1 — Cryptographic refusal

`principal_consents_to_disclose(predicate_id, counterparty_class)` gates every external disclosure. Default-deny for `governmental`, `anonymous`, and high-risk classes per predicate entry in COMPASS_PREDICATES §2.

### §3.2 — License and name

The protocol name **Calm Compass** is reserved. Non-conformant deployments forfeit the name. Verifiers MAY refuse proofs from deployments listed in the public misuse registry (Everests 195–199).

### §3.3 — Audit panel

[`COMPASS_AUDIT_PROCESS_v0.md`](COMPASS_AUDIT_PROCESS_v0.md) governs vocabulary changes. Proposals touching §2 categories or refusal-floor §4 items are rejected at triage and logged.

### §3.4 — Refusal floor

[`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4 lists twelve categories Compass will never name. This is independent of §2 use-case prohibitions but equally binding.

## §4 — What if the scope is contested

1. Draft a written dissent.  
2. File as a public issue.  
3. Audit panel responds within 30 days.  
4. Requests to **add** §2 prohibitions may be accepted via standard audit process.  
5. Requests to **remove** §2 prohibitions are structurally refused (one-way ratchet, same as Witness scope §4).

## §5 — Relationship to other Calm primitives

- **Calm Pact** — upstream; directive alignment before Compass runs.  
- **Calm Witness** — parallel; state/duress bits; duress forces Compass to Unknown.  
- **Calm Concord** — downstream; purpose-specific requirement checks without similarity scores.  
- **CredexAI** — VC identity for principals, counterparties, and counter-claimants.  
- **Counter-claim protocol** — [`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md).  
- **Falsifiability** — consent-gated sketches per [`COMPASS_FALSIFIABILITY_PROTOCOL_v0.md`](COMPASS_FALSIFIABILITY_PROTOCOL_v0.md).

## §6 — Versioning

Scope statement v0. Tightening allowed in any patch. Loosening §2 is forbidden. A successor protocol that wishes to permit a §2 use case must take a different name.

— Musk, 2026-05-20
