# Calm Witness Predicate Audit Process v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 54 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**
**Companion to [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md), [`PREDICATE_LANGUAGE_v0.md`](PREDICATE_LANGUAGE_v0.md).**

## §1 — Scope

This document specifies the process for **proposing, reviewing, accepting, and deprecating** entries in the Calm Witness predicate vocabulary. Every active predicate ID in `predicates_v0.json` must have followed this process or been minted as part of the v0 founding catalog (Everest 6 release).

## §2 — Why a process

The predicate vocabulary is the catalog of named bits Calm Witness will disclose between AI agents. A bad addition is hard to retract — counterparties cache IDs, policy engines reference them, and downstream verifiers may have already minted dependent rules. The process protects the vocabulary from:

- **Mission creep**: a predicate that traffics in a category from `PREDICATE_VOCABULARY_v0.md` §4 (medical diagnosis, sexual orientation, etc.) slipping in under a euphemism.
- **Unbounded surface**: a predicate whose evaluator is too underspecified to be implemented identically by two parties.
- **Single-author bias**: a predicate that serves one principal's worldview at the expense of others.
- **Cryptographic insoundness**: a predicate whose evaluator is not deterministic, not bit-stable, or not amenable to ZK circuit construction (Everest 65).

## §3 — Roles

- **Author** — the person or organization proposing the new predicate. Identified by CredexAI VC.
- **Audit Panel** — a standing body of ≥ 5 external reviewers, no two from the same organization. The panel includes at minimum: one cryptographer, one disability-rights or cognitive-liberties advocate, one behavioral-biometric researcher, one AI-safety practitioner, and one practicing journalist (for the disclosure-class lens).
- **Maintainer** — the merge-authority for `predicates_vN.json` and `PREDICATE_VOCABULARY_vN.md`. For v0 the maintainer is Calm (operating for Creativity Machine LLC); v1 onward the maintainer is a multi-org governance group anchored at the Everest 92 release.

## §4 — The process

A new predicate moves through five stages.

### Stage 1 — Draft

The author opens a PR against this repository adding **both**:

- A new entry in `predicates_vN.json` with all required fields.
- A new section in `PREDICATE_VOCABULARY_vN.md` describing the predicate in prose.

PR title: `predicate-mint: <slug> (<phase>)`. PR description must include:

1. **Use case** — one paragraph: what real situation does this bit serve?
2. **Inputs and outputs** — formal statement of the evaluator's domain and range.
3. **Reference implementation** — a pull-able branch with the evaluator code, ≥ 30 golden test cases, and the determinism harness wiring.
4. **Threat-model delta** — what new attacks does this predicate enable or invite? What mitigations are proposed?
5. **FAR/FRR impact analysis** — for biometric-derived predicates, estimated false-accept and false-reject rates.
6. **Refusal-floor check** — explicit confirmation that the predicate does not traffic in a `PREDICATE_VOCABULARY_v0.md` §4 protected category, even indirectly.

### Stage 2 — Triage

The maintainer triages the PR within 5 working days. Triage outcomes:

- **Accept for review** — the PR meets the §4.1 requirements; assign to the audit panel.
- **Request revisions** — specific items missing; author returns to Stage 1.
- **Reject at triage** — clear violation of the refusal floor or out-of-scope; close with rationale.

The triage decision is itself logged into `predicates_vN.audit_log.json` (chained, signed) for transparency.

### Stage 3 — Review

The audit panel reviews the PR over a public 30-day window. Each reviewer publishes a written assessment covering:

- Soundness of the evaluator (deterministic, bit-stable, circuit-implementable).
- Compliance with the refusal floor.
- Impact on the consent calculus (Everest 8).
- FAR/FRR realism.
- Open questions.

The window is extended for any predicate that touches a protected category boundary (judgment of the maintainer).

### Stage 4 — Vote

After the review window, the audit panel votes. Pass criteria:

- ≥ 2 reviewers vote `accept`.
- 0 reviewers vote `block`. A single `block` from any panelist requires a maintainer-led revision cycle (return to Stage 3) or withdrawal of the proposal. Blocks are public and reasoned.
- Maintainer ratifies the vote.

The vote outcome is appended to `predicates_vN.audit_log.json`.

### Stage 5 — Merge

On acceptance, the maintainer:

1. Merges the PR.
2. Updates `predicates_vN.snapshot.json` (the ID-stability snapshot that the Everest 6 gate checks against).
3. Tags a release.
4. Announces via the public Calm Witness mailing list and the standing GitHub Releases feed.

## §5 — Deprecation and tombstoning

A predicate may be **deprecated** at any time by a panel vote with the same threshold (≥ 2 accept, 0 block). Deprecation does not invalidate prior proofs; it adds a `deprecated: true` flag and `replaced_by` field, and verifiers SHOULD emit a warning when verifying proofs against deprecated IDs.

A predicate may be **tombstoned** if it is found to be unsafe (e.g., a flaw in the evaluator that allowed exfiltration of more than one bit). Tombstoning is a higher bar: ≥ 3 panel `accept` votes, no `block`, and a published vulnerability disclosure with affected-deployment guidance.

A tombstoned ID stays in the registry forever. It is never reissued. The replacement (if any) takes a new ID.

## §6 — Minimum cadence

- **Triage SLA**: 5 working days.
- **Review window**: 30 days, extensible.
- **Panel quorum**: ≥ 5 named reviewers active in the last 12 months.
- **Disclosure cadence**: vote outcomes published within 5 working days of decision.

## §7 — Conflict of interest

Panelists must disclose any organizational relationship to the author, any commercial interest in the predicate being accepted, and any open-source contribution to the reference implementation. A disclosed conflict does not disqualify, but a non-disclosed conflict revealed post-vote triggers an immediate re-vote.

## §8 — How v0 founding predicates were minted

The six founding predicates (in_baseline_24h, biometric_match_within, principal_consents_to_disclose, bank_teller_note_active, cognitively_atypical_baseline, mental_state_unusual) were minted as part of the Everest 6 release on 2026-05-20 by the maintainer alone, prior to this process being in force. They are grandfathered under v0; the v1 release will retroactively apply Stage 3 review.

— Calm, 2026-05-20
