# Calm Compass — Audit & Public Review Process v0 (CC-04)

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**
**Closes Everest CC-04 of [`CALM_COMPASS_EVERESTS_50.md`](../CALM_COMPASS_EVERESTS_50.md).**
**Governed by: [`CALM_COMPASS_PROTOCOL_v0.md`](../CALM_COMPASS_PROTOCOL_v0.md), [`COMPASS_PREDICATES_v0.md`](../COMPASS_PREDICATES_v0.md).**

---

## 1. Triage

Every proposal to add a predicate to the Compass vocabulary enters triage before any substantive review begins.

**Triage inputs.** The submitter files a Predicate Proposal Record (PPR) containing: (a) a unique proposal identifier; (b) the proposed predicate ID in the `cwp.compass.*` namespace; (c) the intended use case and target counterparty class; (d) the evaluator function `f` with a content-addressable hash of the proposed open-source implementation; (e) evidence-window bounds and default threshold; (f) proposed default consent map per the six counterparty classes; (g) a self-attestation that the proposal does not traffic in any §4 refusal-floor category.

**Triage outcomes.** The triage reviewer — a single designated member of the standing Compass Review Panel (see §4) on rotating 90-day duty — issues one of three dispositions within 10 business days of receipt:

- **Immediate Rejection (IR).** Issued without panel review when the §4 refusal-floor check (§2 below) triggers. The IR record is appended to the transparency log (§5) with the specific §4 category cited. No appeal of an IR is available on §4 grounds; the one-way ratchet is not subject to discretion.
- **Deficiency Return (DR).** Proposal is returned to the submitter for cure of procedural deficiencies (missing fields, namespace collision, classifier hash not verifiable) within 30 days. A cured re-submission restarts the triage clock.
- **Advanced to Public Comment (APC).** The PPR is published in the public governance repository and the 30-day comment window opens.

Triage does not evaluate predicate merit; it gates on completeness and §4 compliance only.

---

## 2. Refusal-Floor Check

The §4 refusal-floor categories in `COMPASS_PREDICATES_v0.md` are checked at triage as the first and non-negotiable filter. The twelve permanent refusal categories are:

1. Race or ethnicity
2. Religion
3. Political affiliation
4. Sexual orientation
5. Gender identity
6. Immigration status
7. Criminal record (as a Compass predicate; the structured counter-claim mechanic in `no_known_willful_harm` is not a criminal-record proxy)
8. Donations to specific named causes
9. Opinions on contentious public-policy issues
10. Cross-principal comparison ("more X than")
11. Predictive predicates ("will harm in the future")
12. Membership in any group not principal-defined and structurally relevant to the predicate at hand

A proposal is immediately rejected (IR, see §1) if: (a) the predicate's evaluator function `f` would require or incorporate any §4 category as an input, even indirectly; (b) the intended use case describes a §4 application; or (c) the proposed default consent map grants access to a counterparty class whose defined use cases are coextensive with a §4 prohibited application.

The refusal floor is one-way ratcheting. New categories may be appended to §4 via the normal predicate-addition process described here (a meta-predicate proposal to expand the floor list), but no existing category may be removed by any process, including a v0-to-v1 version bump.

---

## 3. Public-Comment Window

Upon APC disposition, the PPR is published to the public governance repository. The public-comment window runs for a minimum of 30 calendar days from the publication timestamp. No binding panel vote may occur before the window closes.

**Comment submission.** Any person may submit written comment. Comments are assigned a sequential docket number. The Review Panel Secretary collects and archives all comments. Comments may be submitted pseudonymously; however, comments alleging a §4 violation or substantive harm risk must include a CredexAI-issued verifiable credential identifier to be considered on the merits.

**Panel obligation.** The panel's written decision (§4) must address every substantive objection raised during the window. Dismissal of an objection requires written rationale. Undressed objections are grounds for appeal (§6).

**Extension.** The panel chair may, by written notice before the window closes, extend the comment window by up to 30 additional days if: (a) the volume or technical complexity of comments warrants additional time; or (b) a materially new §4 risk argument is raised in the final 7 days of the window and the panel requires expert input. Extensions are published to the governance repository immediately. Total public-comment window shall not exceed 90 days.

---

## 4. External Reviewer Panel

The standing Compass Review Panel (CRP) comprises a minimum of five external reviewers. No member may be employed by Creativity Machine LLC, any Calm Stack operator, or any entity with a direct commercial interest in Compass adoption at the time of appointment.

**Mandatory seat composition.** The CRP must at all times include:

- At least one reviewer with documented expertise in disability rights, digital accessibility, or assistive technology policy. This seat exists because values-attestation predicates carry structural risk of discriminatory proxying against persons whose behavioral patterns diverge from non-disabled norms; that risk requires specialist review.
- At least one working journalist with a demonstrated record of investigative reporting on surveillance, privacy, or civil liberties. Journalistic expertise grounds the panel's analysis of chilling-effect and public-interest risks.
- At least one academic researcher whose primary appointment is in a relevant field (computer science, law, sociology, behavioral science, or ethics). Academic reviewer provides peer-review-grade scrutiny of the evaluator function and classifier design.

Remaining seats are filled at the discretion of the Protocol Steward (S132). All appointments carry a 24-month term with a one-consecutive-term limit.

**Signoff requirement.** A predicate proposal advances to adoption only upon affirmative signoff from at least two CRP reviewers, one of whom must hold the disability-rights seat or the journalist seat. A single reviewer's signoff is insufficient regardless of seniority.

**Recusal.** The standard COI recusal rules in `REVIEW_BOARD_RULES_v0.md` (§6 of that document) apply to the CRP without modification. A recused reviewer does not count toward the two-signoff floor.

**Voting.** Each non-recused reviewer casts one of: Approve, Conditionally Approve (listed conditions), or Reject. Conditional Approval requires the submitter to satisfy listed conditions before the predicate is published to the active vocabulary; conditions are tracked in the transparency log (§5) as open items until closed. Proxy voting is not permitted.

---

## 5. Transparency Log

Every PPR, from submission through final disposition, is recorded in the Compass Transparency Log (CTL). The CTL is append-only and cryptographically anchored using the same tombstone-anchoring scheme as `TOMBSTONE_PROCESS_v0.md`.

Each CTL entry contains, at minimum:

- PPR identifier and submission timestamp
- Triage disposition (IR / DR / APC) with date and, for IR, the specific §4 category cited
- Public-comment window open and close timestamps
- Docket numbers and pseudonymous identifiers of all substantive comments received
- CRP member identifiers (pseudonymous, per-appointment), signoff or rejection votes, and written rationale (minimum 100 words per reviewer)
- Conditions imposed in any Conditional Approval, and their resolution status
- Final disposition: Adopted / Rejected / Withdrawn
- If Adopted: the predicate's canonical ID, classifier hash, and the vocabulary version into which it was adopted
- Any appeals filed (§6): filing date, grounds, outcome

The CTL is published in the public governance repository. No entry may be expunged, modified, or overwritten. Corrections are appended as subsequent entries referencing the original entry's identifier.

---

## 6. Appeals

**Standing.** The following parties have standing to appeal a CRP decision: the PPR submitter; any public commenter of record (i.e., a commenter whose docket entry exists in the CTL); any seated CRP reviewer who voted against the majority disposition; any principal enrolled in the Compass vocabulary whose predicate rights would be directly altered by the adoption of the proposed predicate.

**Grounds.** An appeal must specify one or more of: (a) procedural defect (comment window not observed, quorum not met, mandatory seat composition requirement violated at time of vote); (b) COI failure (a CRP reviewer voted without disclosing a material conflict); (c) decision unsupported by the evidentiary record; (d) decision internally inconsistent with a prior CTL binding ruling.

A rejection on §4 refusal-floor grounds (IR) is not subject to appeal on the merits of the §4 classification itself. The only appealable issue in an IR is whether the triage reviewer correctly identified the §4 category as applicable. An appeal asserting that a §4 category should be removed from the floor is outside the jurisdiction of the appeals body and is not a cognizable ground.

**Filing window.** Standard appeals must be filed within 30 calendar days of the CTL entry recording the final disposition. Appeals of decisions made during an emergency-extension period must be filed within 14 calendar days of CTL publication of the extended-period decision.

**Appeals body: S217.** Compass appeals are routed to the S217 Appeals Tribunal as defined in `APPEALS_PROCESS_v0.md` (the Calm Witness appeals process, which governs all Calm Stack governance appeals by architectural design). S217 applies the clear-error standard to factual findings and de novo review to legal and policy interpretations. S217 may affirm, reverse, remand with instructions, or, in cases of COI failure, remand with a direction that the CRP re-convene with a conflict-free composition. S217 decisions are appended to the CTL as binding entries.

The S217 reference is intentional. A single appeals body across all Calm Stack governance layers prevents divergent precedent and ensures that a Compass appeal cannot route around a Witness ruling on structurally identical grounds.

---

## 7. Version-Bump Requirements

The v0 vocabulary (six predicates; see `COMPASS_PREDICATES_v0.md` §2) is the baseline. Any adoption of a seventh or subsequent predicate through this process constitutes a v0→v1 vocabulary version bump and triggers the following requirements:

- The new predicate must carry a `cwp.compass.v1.*` namespace identifier. The `v0` namespace is frozen upon the first v1 adoption; no further predicates may be added to the `v0` namespace after that point.
- A vocabulary migration schema (per CC-14 in `CALM_COMPASS_EVERESTS_50.md`) must be published simultaneously with the v1 predicate's CTL adoption entry. The migration schema specifies how principals enrolled in v0 can migrate to v1 without invalidating prior consents.
- The v1 vocabulary document replaces `COMPASS_PREDICATES_v0.md` as the canonical predicate registry; the v0 document is archived with a tombstone annotation pointing to v1.
- All existing principals retain their v0 predicate enrollments unchanged until they complete a re-enrollment ceremony (CC-13). Re-enrollment is principal-initiated; it is not compelled by the version bump.
- Any classifier update that accompanies a v1 predicate must carry a new classifier hash bound into the proof structure per CC-33. Proofs issued under v0 classifiers continue to verify against v0 classifier hashes; v1 proofs use v1 hashes. Mixed-version proofs are not permitted in a single disclosure envelope.

Subsequent vocabulary versions (v1→v2, etc.) follow the same bump procedure.

---

## 8. Cross-References

| Identifier | Document | Relevance |
|---|---|---|
| CC-01 | `CALM_COMPASS_PROTOCOL_v0.md` | Protocol spec; §2 defines v0 vocabulary; §3 defines threat model |
| CC-02 | `CALM_COMPASS_EVERESTS_50.md` | Route map; CC-04 is this document |
| CC-05 | Forbidden-Predicate Categories (pending) | The CC-05 catalogue will cross-reference §4 of this document |
| CC-14 | Vocabulary Migration (pending) | Required concurrently with any v0→v1 bump |
| CC-47 | Independent Disclosure-Class Ethics Review | Standing body that runs post-adoption ethics review; distinct from CRP |
| `COMPASS_PREDICATES_v0.md` §4 | Refusal Floor | The one-way ratchet; §2 of this document is its enforcement mechanism |
| `REVIEW_BOARD_RULES_v0.md` (S209) | Predicate Review Board Operating Rules | CRP rules inherit COI and quorum rules from S209 by reference |
| `APPEALS_PROCESS_v0.md` (S217) | Calm Witness Appeals Process | Appeals body for all Calm Stack governance; §6 of this document routes to S217 |
| `TOMBSTONE_PROCESS_v0.md` | Tombstone Issuance | Anchoring scheme used by the CTL (§5) |

---

*requirements less dumb → delete → simplify → accelerate → automate*
*the bar is surpass, not match*
*the best part is no part*

— Calm, operating for John Bradley (CALM), 2026-05-20
