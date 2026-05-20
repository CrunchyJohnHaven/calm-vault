# Calm Witness — Values-Alignment Charter v0

Date: 2026-05-20
Status: Draft v0, binding on predicate family Sxxx 104-133
Signatory: Calm

## Scope

The values-alignment predicate family (Sxxx 104-133) extends Calm Witness Phase IX with attestations over a principal's authored corpus. Predicates in this family return a three-valued result (`true`, `false`, `unknown`) regarding whether positive traits are observable in the principal's writing, code, messages, and other authored artifacts admitted to the vault under existing ingestion controls.

The family is restricted to *positive-trait detection*: `unselfish_signal_present`, `untribal_signal_present`, `respect_for_difference_signal_present`, `growth_orientation_signal_present`, and the ratified successors enumerated by the S132 vocab governance body. The family does NOT emit denunciatory predicates. There is no `tribal=true`, no `selfish=true`, no `closed_minded=true` channel. Absence of a positive signal returns `unknown`, never a negative label.

Intended use is counterparty-initiated trust negotiation: an agent acting for a third party may, with the principal's per-counterparty consent, query whether a positive signal is present at a calibrated threshold. The output is a zero-knowledge attestation; the underlying corpus is not disclosed.

Population norms are forbidden as calibration substrate. Each predicate is calibrated against the principal's own historical baseline (per-principal calibration), so a signal reports a deviation from the principal's own prior distribution, not a ranking against any group.

## Refusals

This family refuses any predicate touching the S105 forbidden catalog. The catalog includes, without limitation: political affiliation, religion, race, ethnicity, national origin, sexual orientation, gender identity, criminal history, clinical diagnosis (mental or physical), IQ or cognitive ranking, immigration status, union membership, and any other protected class enumerated under applicable jurisdiction.

Proposals that infer membership in any forbidden category — directly, by proxy, or by composition of otherwise-permitted predicates — are rejected at intake by S132 and may not be re-proposed under a renamed wrapper. The composition rule binds: a values-alignment predicate that, in conjunction with any other admitted predicate, would permit a counterparty to derive a forbidden inference is itself forbidden.

The family also refuses any predicate whose positive form encodes a negative judgement of an out-group. `respect_for_difference_signal_present` is admissible; `hostility_toward_X_absent` is not, because absence-of-hostility predicates re-introduce the denunciation channel by inversion.

## Governance

The S132 vocab governance body holds ratification authority over the Sxxx 104-133 namespace. No predicate enters the family without S132 ratification, and no calibration method enters production without S132 sign-off on the methodology. S132 maintains the public registry of admitted predicates, deprecated predicates, and rejected proposals with reasons.

S132 convenes review on a fixed cadence and on petition. Petitions may originate from any principal, any counterparty under active consent, or any external reviewer holding standing per the External Review section below. S132 decisions are recorded in the governance log and are themselves auditable.

## Principal Protections

The principal retains per-dimension decline rights under S117: any individual predicate in this family may be disabled by the principal at any time, with effect on all future queries from all counterparties. Decline is silent — counterparties learn `unknown`, not "declined".

The principal holds the right-to-deny override under E67: even a previously consented predicate, for a previously consented counterparty, may be retroactively denied at the moment of query. The override is unappealable and does not require justification.

Every query, every attestation, every consent grant, and every decline is recorded in the principal's audit trail per S126. The audit trail is principal-readable in full and counterparty-readable only for queries that counterparty itself issued.

Consent is per-counterparty and per-predicate. Blanket consent across the family is not offered. A counterparty granted access to `unselfish_signal_present` does not thereby gain access to `growth_orientation_signal_present`.

## External Review

No new dimension enters the Sxxx 104-133 family without external review. External reviewers are drawn from a roster maintained by S132, with rotation to prevent capture. The roster MUST include at least one reviewer with civil-liberties standing, one with ML-fairness standing, and one principal-advocate seat held by a randomly selected principal who has opted into the review pool.

The external review examines: (i) whether the proposed dimension respects the positive-only discipline; (ii) whether per-principal calibration is feasible without leaking population norms; (iii) whether composition with existing predicates risks forbidden-category inference; (iv) whether the proposed predicate survives adversarial re-naming tests. A unanimous reviewer veto blocks ratification.

## Cross-References

- S105 — Forbidden categories catalog (refusal substrate)
- S117 — Per-dimension principal decline
- S126 — Audit trail specification
- S132 — Vocab governance body and ratification process
- E67 — Right-to-deny override at query time
- Phase IX charter — parent document

— Calm, 2026-05-20
