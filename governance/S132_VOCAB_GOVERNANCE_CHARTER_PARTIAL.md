# S132 — Alignment-Vocab Governance Body Charter (Partial Bag)

**Status: PARTIAL BAG** — constitutional draft complete; board not yet seated.
**Signed:** Calm 2026-05-20

---

## 1. Scope

The Alignment-Vocab Governance Body (AVGB) holds exclusive authority over the canonical set of alignment predicates used within the Calm Witness attestation system. Alignment predicates are the normalized vocabulary tokens embedded in tamperproof user-state attestations (see S104, S105). No predicate may be added to, modified in, or retired from the canonical vocabulary without an affirmative AVGB vote, except for emergency deprecations executed under the Deprecation Timeline protocol (S106), which require AVGB ratification within 30 calendar days.

Scope includes:

- Approving new predicate proposals submitted via the public-comment queue.
- Ratifying or vetoing emergency deprecations initiated by operators.
- Issuing binding semantic clarifications when predicate meaning is contested in an active attestation dispute.
- Maintaining the canonical predicate registry and its public changelog.

The AVGB does not hold authority over: attestation infrastructure (S105), appeals adjudication (S217), or ethics-layer review (S85). Those bodies receive AVGB outputs as binding inputs but govern their own procedures independently.

---

## 2. Composition

**Minimum size:** Five (5) voting members. No upper limit is set by this charter; the AVGB may expand by majority vote up to nine (9) members.

**Eligibility:**

- No current employee, contractor, or equity holder of any Calm operator entity may serve as a voting member.
- No individual may hold simultaneous voting seats on the AVGB and the Predicate Review Board (S209).
- Members with a financial or fiduciary interest in a specific predicate under active consideration must recuse (see Section 4).

**Conflict-of-Interest (COI) disclosure:** All members must file a disclosure statement at the time of appointment and update it within 14 days of any material change. Disclosures are public. The AVGB secretary maintains the disclosure register and flags potential conflicts before each agenda item.

**Founding cohort:** Nominated by the Calm operator, ratified by a simple majority of the S85 Ethics Review body. Subsequent appointments are made by the AVGB itself (majority vote of seated members), subject to the same eligibility rules.

---

## 3. Term Limits and Rotation Schedule

**Term length:** Three (3) years per term.

**Term limit:** Maximum two consecutive terms (6 years). A member who has served two consecutive terms may not be re-seated until at least one full term (3 years) has elapsed.

**Staggered rotation:** To prevent full-board turnover, the founding cohort is assigned staggered term lengths at the founding ceremony:

| Seat tier | Initial term | Renewal cycle |
|-----------|-------------|---------------|
| Tier A (≥2 seats) | 1 year | 3-year thereafter |
| Tier B (≥2 seats) | 2 years | 3-year thereafter |
| Tier C (remaining) | 3 years | 3-year thereafter |

Tier assignments are drawn by lot at the founding ceremony. All subsequent terms are 3 years.

**Vacancies:** A vacant seat must be filled within 90 calendar days. The AVGB may operate with one seat vacant without triggering a quorum adjustment for up to 60 days. Beyond 60 days, quorum calculations reduce by one.

---

## 4. Decision Rules

**Quorum:** A majority of seated, non-recused members. With five members and no recusals, quorum is three (3).

**Standard voting threshold:** Simple majority of members present and voting (abstentions do not count as votes).

**Supermajority threshold (two-thirds of all seated members):** Required for:

- Adding a new predicate to the canonical vocabulary.
- Retiring a predicate that is referenced in active attestations.
- Amending this charter.
- Removing a member for misconduct (see Section 7).

**Recusal:** A member must recuse when they have a direct financial interest in the outcome, when they are party to an active attestation dispute touching the predicate under review, or when their COI disclosure identifies a non-trivial relationship with a proponent or opponent. Recusal is self-declared; any seated member or the AVGB secretary may also flag a potential recusal conflict, triggering a procedural vote (simple majority, recusing member abstains).

**Tie-breaking:** On a tied standard vote, the measure fails. On a tied supermajority vote, the measure fails and may not be re-submitted for 90 days unless new material evidence is presented.

**Meeting cadence:** Minimum one regular session per calendar quarter. Emergency sessions may be called by any two members with 72 hours notice.

---

## 5. Public Comment and Public Minutes

**Public-comment queue:** All predicate proposals and semantic clarification requests must be posted to the public-comment queue no fewer than 21 calendar days before the AVGB votes on them. The queue is publicly readable. Written comments submitted during the open period become part of the permanent record.

**Public minutes:** Complete minutes of every AVGB session — including vote tallies, dissents, and recusal notices — must be published within 14 calendar days of the session. Minutes are immutable once published; corrections are filed as addenda.

**Emergency deprecations:** When an operator invokes the S106 emergency deprecation pathway, the AVGB must publish a ratification notice (or veto notice) within the 30-day ratification window. The ratification vote is subject to standard quorum and voting rules and its minutes are published within 7 calendar days of the vote.

**Changelog:** The canonical predicate registry includes a machine-readable changelog entry for every approved modification, referencing the session date, vote tally, and any linked public-comment submissions.

---

## 6. Interaction with Other Governance Bodies

**Predicate Review Board (S209):** The PRB performs technical feasibility and consistency review before a proposal reaches the AVGB vote. The PRB recommendation is advisory; the AVGB is not bound by it but must record its rationale if it departs from a PRB recommendation.

**Ethics Review (S85):** The Ethics Review body may flag a predicate proposal as raising ethical concerns. An S85 flag places the proposal in a mandatory 30-day extended comment period before the AVGB may vote. The AVGB may override an S85 flag by supermajority vote; the override rationale is published in the minutes.

**Appeals Board (S217):** When an attestation dispute triggers a semantic-clarification request, the Appeals Board routes the request to the AVGB. The AVGB's clarification is binding on the Appeals Board for the disputed attestation and is simultaneously published as a canonical interpretation in the predicate registry.

**Escalation protocol:** Disputes between the AVGB and another body that cannot be resolved by bilateral discussion are escalated to a joint session of the chairs of both bodies plus one neutral facilitator agreed upon by both parties. Joint session outcomes are binding on both bodies.

---

## 7. Misconduct Sanctions

**Defined misconduct:** Failure to file or update COI disclosures, voting on a matter requiring recusal, unauthorized disclosure of non-public predicate proposals prior to the comment period, persistent failure to attend sessions (missing three consecutive regular sessions without notice), or conduct materially inconsistent with the AVGB's public-trust mandate.

**Process:** Any member or the AVGB secretary may file a misconduct complaint. The complaint is reviewed by a panel of three members uninvolved in the allegation. The panel recommends one of: dismissal, formal censure, or removal. Removal requires a supermajority vote of all seated members excluding the subject.

**Censure:** Censure is published in the public minutes. A censured member may not chair a session or serve on a review panel for 12 months following censure.

**Removal:** A removed member's seat is treated as a vacancy under Section 3. The removed member is ineligible for re-appointment for five years.

---

## 8. Handoff — What Remains

This charter is constitutionally complete. The following work is not done and must be completed before the AVGB is operational:

1. **Nominee identification.** The Calm operator must identify and vet a founding cohort of five to nine individuals meeting Section 2 eligibility criteria. No nominees have been identified as of 2026-05-20.

2. **COI disclosure collection.** Each nominee must complete and submit a disclosure statement before the founding ceremony.

3. **S85 ratification of founding cohort.** The Ethics Review body (S85) must ratify the proposed founding members by simple majority.

4. **Founding ceremony.** Seat assignments, tier-lottery for staggered terms, election of inaugural chair and secretary, and adoption of this charter by the seated board.

5. **First vote.** The AVGB's first substantive action should be a ratification vote on the existing canonical predicate set, establishing a baseline registry with a dated changelog entry.

6. **Public infrastructure.** Standing up the public-comment queue, minutes repository, and predicate registry with changelog before the first session.

---

*References: S104 (attestation primitive), S105 (infrastructure layer), S106 (deprecation timeline), S209 (Predicate Review Board), S217 (Appeals Board), S85 (Ethics Review).*

**PARTIAL BAG — S132**
Calm 2026-05-20
