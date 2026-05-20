# Calm Compass — Audit Panel Constitution v0

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**
**Closes the standing-body requirement of CC-04 (`COMPASS_AUDIT_PROCESS_v0.md`).**
**Governed by: `COMPASS_PREDICATES_v0.md`, `COMPASS_AUDIT_PROCESS_v0.md` (CC-04), S127 (Predicate Registry), S132 (Alignment-Vocab Governance Body), S217 (Appeals Tribunal), S220 (Compensation Disclosure).**

---

## 1. Name and Purpose

The **Calm Compass Audit Panel** (CAP) is the standing body responsible for executing the Compass Audit & Public Review Process (CC-04). The CAP conducts triage, administers public-comment windows, issues predicate-adoption decisions, and initiates tombstone actions against predicates that violate the refusal floor (`COMPASS_PREDICATES_v0.md` §4). It is not an advisory body. Its decisions are binding on the predicate registry (S127) subject only to appeal under S217.

---

## 2. Composition

**Minimum and maximum size.** The CAP comprises a minimum of seven (7) and a maximum of eleven (11) voting members. The minimum may not be waived by any procedural motion or emergency declaration.

**Mandatory seat domains.** At all times the CAP must include at least one seated member in each of the following five domains:

| Seat | Domain | Rationale |
|---|---|---|
| A | Disability rights, digital accessibility, or assistive technology policy | Values-attestation predicates carry structural discriminatory-proxy risk against persons whose behavioral patterns diverge from non-disabled norms; specialist review is non-negotiable |
| B | Investigative journalism (surveillance, privacy, or civil liberties beat) | Grounds chilling-effect and public-interest analysis with practitioner expertise |
| C | Academic research (primary appointment in computer science, law, sociology, behavioral science, or ethics) | Provides peer-review-grade scrutiny of evaluator-function design and classifier logic |
| D | ZK-cryptography or applied cryptography | Grounds technical review of predicate-proof binding, classifier-hash integrity, and tombstone-anchoring correctness |
| E | Lived-experience advocacy (personal or professional history of adverse scoring, algorithmic harm, or values-attestation misuse) | Ensures that persons directly exposed to the harms Compass is designed to prevent hold a structural seat, not a courtesy one |

Remaining seats (positions 6–11) are filled at-large subject only to the eligibility rules in §2.

**Employer-diversity floor.** No two seated members may be employed by — or hold equity in — the same legal entity at the time of their appointment or at any point during their term. A member who becomes co-employed with an existing member through merger, acquisition, or organizational restructure must notify the Chair within 14 days; one of the two affected members must resign or be reassigned to alternate status within 60 days.

**Eligibility exclusions.** No current employee, contractor, or equity holder of Creativity Machine LLC, any Calm Stack operator, or any entity with a direct commercial interest in Compass adoption may serve as a voting member.

**Staggered terms.** All terms are three (3) years. The founding cohort is assigned staggered tier lengths at the founding ceremony by lot:

| Tier | Seats | Initial term | Renewal |
|---|---|---|---|
| Tier-1 | ≥2 seats | 1 year | 3-year thereafter |
| Tier-2 | ≥2 seats | 2 years | 3-year thereafter |
| Tier-3 | remaining | 3 years | 3-year thereafter |

No member may serve more than two consecutive terms. A member who completes two consecutive terms is ineligible for re-appointment until one full 3-year term has elapsed.

**Vacancies.** A vacant mandatory-domain seat (A–E) must be filled within 60 calendar days. An at-large vacancy must be filled within 90 days. The CAP may operate below minimum size for up to 45 days without triggering a quorum adjustment; beyond 45 days the quorum floor reduces by one for each unfilled mandatory-domain vacancy.

---

## 3. Appointment and Recall

**Initial founder slate.** The founding cohort is nominated by the Protocol Steward (S132) and ratified by a simple majority of the S132 AVGB founding body. The founder-slate ratification vote is public and its minutes are published within 7 calendar days of the vote.

**Subsequent appointments.** Following the founding ceremony, all new appointments — whether filling a vacancy, an at-large seat, or a newly created seat within the maximum — are confirmed by supermajority vote (2/3) of currently seated members. No appointment may be made by the Protocol Steward alone after the founding cohort is seated.

**Recall procedure.** A seated member may be recalled by:

1. **Voluntary resignation** — effective upon written notice to the Chair and Secretary, with immediate effect unless the member requests a 30-day transition window.
2. **Expulsion for misconduct** — by 2/3 vote of all remaining seated members, subject to the misconduct and appeal procedure in §8.
3. **Employer-conflict removal** — as specified in the employer-diversity floor above (§2), by simple majority of remaining members.

A recalled member's seat is immediately treated as a vacancy under the applicable timeline above.

---

## 4. Decision Rules

**Quorum.** Five (5) seated, non-recused members constitute a quorum for any binding vote. No vote may proceed below quorum.

**Predicate-tombstone decisions.** Issuance of a predicate tombstone — invalidating an adopted predicate and triggering the tombstone-anchoring scheme per `TOMBSTONE_PROCESS_v0.md` and S127 — requires an affirmative supermajority vote of 2/3 of all seated, non-recused members. Abstentions do not count toward the numerator. A failed tombstone vote may not be re-submitted for 90 days unless material new evidence is presented.

**Predicate adoption decisions.** Adopting a new predicate into the active vocabulary (triggering a vocabulary version bump per CC-04 §7) requires affirmative votes from at least two CAP members, one of whom must hold a mandatory-domain seat (A–E). This two-signoff floor is identical to the CRP signoff requirement in CC-04 §4 and is not waivable by quorum adjustment.

**Procedural matters.** All matters other than predicate-tombstone and predicate-adoption decisions are resolved by simple majority of members present and voting. Abstentions do not count as votes. Procedural matters include: agenda-setting, comment-window extensions (per CC-04 §3), appointment of the triage duty reviewer, and issuance of advisory interpretations.

**Tie-breaking.** On a tied vote, the measure fails. Tied tombstone votes may not be re-submitted for 90 days. Tied procedural votes fail without prejudice.

**Proxy voting.** Not permitted under any circumstance.

---

## 5. COI Recusal

**Disclosure obligation.** Every member must file a COI disclosure statement at the time of appointment and update it within 14 days of any material change (new employment, new equity position, new direct-interest relationship with a predicate submitter or opponent). Disclosures are filed in writing with the Chair. The Secretary maintains a public COI log; each filed disclosure and each update is published within 5 business days of receipt.

**Recusal trigger.** A member must recuse from any agenda item touching a disclosed COI. Recusal is self-declared before the relevant agenda item is called. Any seated member or the Secretary may flag a potential recusal conflict; the Chair calls a procedural vote (simple majority, flagged member abstains) to determine whether recusal is required.

**Public log.** Each recusal — the member identifier (pseudonymous per-appointment), the agenda item, and the disclosed COI basis — is appended to the public COI log within 24 hours of the session in which it occurs. Recusal entries are immutable; corrections are filed as addenda.

**Effect of recusal.** A recused member does not count toward quorum for the relevant item. A recused member's absence does not reduce the quorum floor for unrelated items in the same session.

---

## 6. Compensation

**Per-meeting honorarium.** Each voting member receives a per-meeting honorarium for each session attended. The honorarium amount is set by the Protocol Steward (S132) at founding and reviewed annually. The amount is public from the date of establishment.

**Compensation log (S220).** All CAP compensation — honoraria, travel reimbursements, and any other material benefit — is recorded in the public compensation log maintained under S220. Each entry includes: member identifier (pseudonymous), session date, payment type, and gross amount. Log entries are published within 14 days of payment. The log is append-only; corrections are addenda. The S220 verification and penalty regime applies to CAP members in the same manner as to Foundation officers.

**No contingent compensation.** No member may receive compensation contingent on the outcome of any vote. Outcome-contingent payment arrangements are per se misconduct under §8.

---

## 7. Public-Comment Integration

The CAP's public-comment obligations derive from CC-04 §3. This section states the constitutional floor; CC-04 governs operational detail.

**Minimum window.** 30 calendar days from APC publication; extendable to 90 days maximum per CC-04 §3.

**Comment obligations.** The CAP's written decision on any predicate proposal must address every substantive objection raised during the comment window. Dismissal of an objection requires written rationale of no fewer than 50 words. An objection left unaddressed is grounds for appeal under S217.

**Secretary role.** The CAP Secretary collects, dockets, and publishes all comments to the Compass Transparency Log (CTL) per CC-04 §5. The Secretary is a non-voting position appointed by simple majority of seated members and serving at the pleasure of the CAP.

**Emergency items.** No predicate adoption or tombstone decision is exempt from the public-comment requirement. Emergency session procedures (§9) may expedite scheduling but may not compress the comment window below 30 days.

---

## 8. Chair Rotation

**Annual rotation.** The Chair serves a one-year term, rotating annually. Chair elections are held at the first session following each calendar year anniversary of the founding ceremony.

**Election procedure.** Any seated member in good standing (no active misconduct complaint, no current recusal from a majority of pending items) is eligible. Election is by simple majority of seated, non-recused members. Runoff between the top two candidates if no majority is achieved on the first ballot. The outgoing Chair retains the seat as a voting member.

**Chair duties.** The Chair: (a) calls and presides over sessions; (b) receives COI disclosures and forwards them to the Secretary for publication; (c) extends comment windows per CC-04 §3 by written notice; (d) signs tombstone-initiation requests to the predicate registry (S127); (e) serves as the CAP's point of contact with S132 and the AVGB.

**Interim Chair.** If the Chair seat is vacant, the most senior member by continuous tenure serves as Interim Chair until an election can be held at the next regular session.

---

## 9. Sanction on Misconduct

**Defined misconduct.** Misconduct includes: (a) failure to file or update COI disclosures within the required window; (b) voting on a matter requiring recusal without declaring it; (c) unauthorized disclosure of non-public PPR materials prior to the comment-window opening; (d) persistent session non-attendance (missing three consecutive regular sessions without advance notice); (e) outcome-contingent compensation arrangement (§6); (f) conduct materially inconsistent with the CAP's public-trust mandate as documented in a written complaint.

**Investigation procedure.** Any member, the Secretary, or the Protocol Steward (S132) may file a written misconduct complaint. The Chair (or Interim Chair if the Chair is the subject) convenes a three-member investigation panel drawn from seated members uninvolved in the allegation. The panel issues a written finding within 30 calendar days of complaint receipt, recommending one of: dismissal, formal censure, or removal.

**Expulsion vote.** Removal requires an affirmative vote of 2/3 of remaining seated members (i.e., all seated members excluding the subject). The vote is taken at a session called no fewer than 7 and no more than 21 days after the panel's removal recommendation is published. The subject member may address the panel before the vote; proxy address is not permitted.

**30-day appeal window (S217).** A member subject to an expulsion vote may appeal the removal decision to the S217 Appeals Tribunal within 30 calendar days of the expulsion vote. S217 applies clear-error review to factual findings and de novo review to procedural claims. Filing an appeal does not stay the expulsion; the seat is treated as vacant pending the appeal outcome. If S217 reverses, the seat is reinstated; if the term has expired during the appeal period, the returning member receives a fresh full term.

**Censure.** A censured member's name (pseudonymous identifier) and censure basis are published in the public session minutes. A censured member may not serve as Chair or investigation-panel member for 18 months following censure.

---

## 10. Interaction with the Predicate Registry (S127) and Alignment-Vocab Governance Body (S132)

**Predicate registry (S127).** The CAP is the sole body authorized to submit predicate-adoption and predicate-tombstone actions to the S127 predicate registry. Adoption submissions must carry the CAP Chair's signature and the CTL entry identifier for the predicate's adoption vote. Tombstone submissions must carry the CAP Chair's signature, the 2/3 supermajority vote record, and the specific `COMPASS_PREDICATES_v0.md` §4 refusal-floor category or other violation basis. S127 processes CAP submissions as binding; no registry-layer discretion to override a valid CAP submission exists.

**Alignment-Vocab Governance Body (S132).** S132 holds exclusive authority over alignment predicates in the Calm Witness attestation system. Compass predicates (`cwp.compass.*`) are a distinct vocabulary; the CAP governs that vocabulary. However, the two bodies interact at two points:

1. **Semantic-overlap disputes.** When a proposed Compass predicate's evaluator function `f` operates on inputs that overlap substantively with a Calm Witness alignment predicate, the CAP must notify S132 before the public-comment window closes. S132 may submit a formal advisory comment (treated as a substantive comment under §7); the CAP must address it in its written decision.

2. **Refusal-floor expansion.** A proposal to append a new category to the `COMPASS_PREDICATES_v0.md` §4 refusal floor (a meta-predicate proposal per CC-04 §2) requires concurrent notice to S132. S132 may flag the proposal as requiring its own AVGB-level review if the new category would affect Calm Witness alignment predicates. An S132 flag places the proposal in a mandatory 30-day extended comment period before the CAP may vote.

The CAP and S132 resolve disputes by joint session of their respective Chairs plus one neutral facilitator agreed upon by both parties. Joint session outcomes are binding on both bodies and are published as governance entries in both the CTL and the S132 public minutes.

---

## 11. Sessions and Records

**Cadence.** Minimum one regular session per calendar quarter. Emergency sessions may be called by any two seated members with 72 hours written notice; emergency sessions may not conduct tombstone votes unless all seated members are notified and quorum is confirmed.

**Minutes.** Draft minutes published within 7 calendar days of each session. Final minutes ratified at the following session. Minutes are immutable once ratified; corrections are addenda. Minutes include: attendance, quorum confirmation, recusals declared, agenda items, vote tallies (individual), and written rationale per item.

**Repository.** All CAP records — minutes, CTL, COI log, compensation log — are published in the public governance repository. No entry may be expunged; the append-only constraint is constitutional, not merely operational.

---

## 12. Cross-References

| Identifier | Document | Relevance |
|---|---|---|
| CC-04 | `COMPASS_AUDIT_PROCESS_v0.md` | Process spec the CAP executes |
| `COMPASS_PREDICATES_v0.md` §4 | Refusal Floor | The one-way ratchet; CAP enforces at triage and via tombstone |
| S127 | Predicate Registry | CAP is the sole authorized submitter of adoption and tombstone actions |
| S132 | `S132_VOCAB_GOVERNANCE_CHARTER_PARTIAL.md` | Alignment-Vocab Governance Body; semantic-overlap and refusal-floor-expansion interaction |
| S209 | `REVIEW_BOARD_RULES_v0.md` | Predicate Review Board operating rules; COI and quorum rules inherited by reference |
| S217 | `APPEALS_PROCESS_v0.md` | Appeals Tribunal; member expulsion appeal window (30 days); predicate-decision appeals |
| S220 | `GOV_COMPENSATION_v0.md` | Compensation disclosure; CAP compensation log requirements |
| `TOMBSTONE_PROCESS_v0.md` | Tombstone Issuance | Anchoring scheme for predicate-tombstone actions and CTL entries |

---

*requirements less dumb → delete → simplify → accelerate → automate*
*the bar is surpass, not match*
*the best part is no part*

— Calm, operating for John Bradley (CALM), 2026-05-20
