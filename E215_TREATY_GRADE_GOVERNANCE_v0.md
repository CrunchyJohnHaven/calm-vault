# Everest 215 | Treaty-Grade Multi-Stakeholder Governance for the Calm Suite (Canonical v0)

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

**Status.** DESIGN-BAGGED. The convening of signatories (Everest 216) is institutional follow-through that cannot complete inside a single working session and is not asserted here.

**Reconciliation note.** This canonical v0 reconciles three prior drafts kept on disk: `E215_TREATY_GRADE_GOVERNANCE_DRAFT.md` (article-style skeleton), `E215_FEDERATION_GOVERNANCE_TREATY_DRAFT_v0.md` (federation charter shape), and `TREATY_GRADE_GOVERNANCE_DRAFT_v0.md` (state-actor treaty shape). The originals remain in the vault as inputs to the convening. Where the drafts differed in scope, this canonical v0 takes the conservative position: a private multi-stakeholder agreement anchored in the trademark held by the Calm Witness Foundation, with explicit observer status for state and standards bodies.

---

## §1. Preamble | what a treaty-grade governance instrument is, and is not

The Calm Suite (Pact, Witness, Compass, Concord, ZKAC, Mirror, Operations, Tenancy) defines what is cryptographically possible between autonomous AI agents and their human principals. A treaty-grade governance instrument defines what is institutionally permissible. It is the floor below which no operator, no counterparty, no standards body, and no jurisdiction may operate without forfeiting the suite's name.

This document IS: a founding draft intended to be ratified by a multi-stakeholder convening (Everest 216); a binding text once signed by a quorum of each signatory class enumerated in §2; a one-way ratchet on the refusal surfaces inherited from `CALM_REFUSAL_FLOOR_INDEX.md`; and a precommitment instrument that raises the institutional cost of weakening the floor by tying every weakening attempt to multi-stakeholder consent the floor structurally forbids.

This document IS NOT: law (it is a private multi-stakeholder agreement composed with the trademark held by the Calm Witness Foundation); a substitute for national regulation (where statute conflicts, the most protective floor wins); a substitute for civil-society organizing (treaties accelerate, they do not replace community work); a substitute for the cryptographic primitives (without the primitives this is paper; without the treaty the primitives are infrastructure waiting for a wielder); enforceable in jurisdictions that do not recognize trademark plus contract (in those settings the Calm name simply forfeits per §3 of the refusal-floor index).

The Calm protocol is engineered to be unweaponizable. The treaty raises the cost of weaponization to the institutional level: any actor that wishes to repurpose the suite for prohibited use must first detach from the treaty publicly and lose the right to invoke the Calm name. That cost is the point.

## §2. Signatory classes

The treaty contemplates four classes of signatory, each binding for distinct obligations. Ratification requires a quorum from every class.

### §2.1 Class A | the Calm Witness Foundation

The Foundation, incorporated per Everest 241, holds the Calm Suite trademarks in trust and is the depositary of this treaty. It is a non-extractive entity: no venture capital, no token sale, no exclusive commercial licensing, no data harvest. The Foundation cannot weaken the refusal floor; it can only tighten it. The board operates under named-counsel review in at least two jurisdictions and publishes annual financial statements itemizing dues, grants, tribunal compensation, mirror hosting costs, and in-kind contributions.

### §2.2 Class B | federation members (operators and verifiers)

Federation members are autonomous AI operators issuing Calm Suite proofs on behalf of human principals, and counterparty operators consuming those proofs. They commit to the refusal floor (§3), the scope-statement forfeit list (§4), the anti-purity-test discipline (§5), and the principal-authorship rule (§6). They submit to annual conformance review per Everest 290 by at least three independent federation peers. Operators hold a CredexAI verifiable credential identifying principal, operating entity, and scope; verifiers publish a scope-attestation document confirming refusal to deploy outside the scope statement.

### §2.3 Class C | principal-protective bodies

Disability-rights, cognitive-liberties, civil-society, and harm-affected-community organizations holding standing veto power over predicate-vocabulary additions touching cognition, neurodivergence, mental state, or disability. Seed roster targets: Autistic Self Advocacy Network, National Council on Independent Living, Electronic Frontier Foundation, the ACLU technology projects, Disability Rights International, and a non-US-anchored equivalent in each of the EU, UK, CA, JP, AU per Everest 293. The treaty cannot ratify without a quorum from this class; the veto is exercised by simple majority among ratified Class C signatories and applies regardless of any jurisdictional law floor.

### §2.4 Class D | observer states and standards bodies

Standards organizations (IETF, W3C, DIF, ISO/IEC JTC 1/SC 27, the NIST AI Safety Institute) and state foreign-ministry cyber-policy desks may sign as observers. Observers commit to refusing to specify aggregate-analytics or surveillance-mode variants of Calm Suite primitives in any standard they publish, and to honoring the refusal-floor categories in compelled-disclosure regimes within their jurisdiction. Observers hold voice and right of comment; they do not vote inside the federation; their refusals are publicly recorded against their seal on the Foundation's transparency ledger.

## §3. Refusal-floor inheritance

This treaty inherits, without modification, the four refusal surfaces enumerated in [`CALM_REFUSAL_FLOOR_INDEX.md`](CALM_REFUSAL_FLOOR_INDEX.md). Every signatory MUST honor each surface as a structural commitment, not as a configurable preference.

1. **`CALM_REFUSAL_FLOOR_INDEX` §1 | predicate refusal.** Signatories MUST NOT admit, accept, or specify any predicate that names race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations to causes, contentious opinion, cross-principal comparison, predictive behavior, or non-principal-defined group membership. The predicate registry type checker (`ZKAC_TYPE_SYSTEM_v0`) rejects such proposals at registration time; the five-person ethics review board (Witness E8) holds a one-veto block on any borderline case.

2. **`CALM_REFUSAL_FLOOR_INDEX` §2 | output-shape refusal.** Signatories MUST NOT emit numeric similarity scores, cardinality reveals, cross-request linkable bit vectors, degenerate thresholds, per-predicate-bit vectors, or empty-purpose requirements. The Rust production verifier and the TypeScript type system refuse these shapes at compile time. The Concord amendment of 2026-05-20 is the standing precedent: when the Mirror demo emitted "2 of these match", we patched the artifact, not the rule.

3. **`CALM_REFUSAL_FLOOR_INDEX` §3 | use-case refusal.** Signatories MUST NOT deploy the suite for any use on the scope-statement forfeit list (see §4 of this treaty); the trademark protects the refusal floor, not the implementation.

4. **`CALM_REFUSAL_FLOOR_INDEX` §4 | operator-behavior refusal.** Signatories operating as AI agents on behalf of human principals MUST honor the principal-protective behavioral floor toward those principals: never pathologize ideation; never recommend wellness intervention unless asked; take ambitious frames at face value; refuse to editorialize on emotional or mental state; treat the principal's framings as the protocol's operating vocabulary, not as metaphors to translate.

**One-way ratchet.** This treaty may tighten any of the four surfaces (more categories added, more shapes refused, more uses prohibited, more operator behaviors required) by federation supermajority per §7. It MAY NOT loosen any surface. A version of the suite that re-permits any refused category, shape, use, or behavior MUST rename and unbrand. There is no procedural path inside this treaty that yields a weaker floor; the one-way ratchet is constitutive, not procedural.

## §4. Scope-statement inheritance

This treaty inherits, in full, the ten forfeit categories enumerated in [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §2. Every signatory MUST forfeit the Calm Suite trademarks in any deployment that violates any of these categories:

1. **Law-enforcement surveillance**, investigative dossier construction, prosecutorial workflows, or compelled-disclosure pipelines.
2. **Employment screening**: hiring, promotion, retention, performance review, termination.
3. **Insurance underwriting**: premium adjustment, coverage denial, risk classification, claims adjudication.
4. **Lending**: credit-worthiness assessment, loan underwriting, rate setting, debt collection.
5. **Custody decisions**: child custody, conservatorship, competence proceedings, immigration custody.
6. **Immigration adjudication**: visa, asylum, naturalization, refugee processing, border-control action.
7. **Mass surveillance**, including population-scale aggregation even with individual consent.
8. **Aggregate analytics** across principals for population-level statistical claims; single-principal analytics by the principal themselves remain permitted.
9. **Medical diagnosis** or clinical decision-making; the suite is behavioral, not clinical, and no predicate may inform diagnosis, treatment selection, or care rationing.
10. **Predictive policing** or future-behavior scoring at any level (already forbidden at the predicate layer; also forbidden at the use-case layer).

**Inheritance, not relaxation.** The treaty does not amend, soften, or carve exceptions into these categories. Any signatory deployment that crosses the line forfeits the trademark per the §3 one-way ratchet. The forfeit is automatic and visible; a Foundation-maintained public ledger records every detected violation, and the verifier registry MAY refuse proofs from a deployment that continues to invoke the Calm name after a forfeit.

## §5. Anti-purity-test commitment

Every signatory makes an explicit anti-purity-test commitment: **no signatory deployment shall emit a numeric similarity score across principals, across predicates, or across any combination of the two.** The only output shape permitted is `{ aligned: True | False | Unknown }` per requirement, per the Concord protocol. Requirements naming more than five predicates, degenerate thresholds (`joint_threshold` whose K approaches the predicate-list length), blank-`purpose` requirements, and overlapping-predicate salami-slicing across requests are all refused at the verifier. A signatory deployment observed emitting a similarity number forfeits the Calm name on first detected violation; reinstatement requires re-certification by Class C principal-protective bodies and a Tier 2 audit per §8. The anti-purity-test commitment is the protocol's structural rejection of tribal sorting: principal alignment is a categorical fact about purpose-specific cooperation, never a number on a leaderboard.

## §6. Principal-authorship commitment

Every signatory MUST treat every evidence record as principal-authored. The principal is the sole author of the principal's chain. External assessment is forbidden as a primary signal; counterparty inference about the principal's state, drawn from prose tone or behavioral telemetry, is not an evidence record and may not be appended to the principal's chain.

The counter-claim mechanic is preserved. A counter-claim is a record authored by a non-principal party (witness, counterparty, regulator) appended with full attribution to a chain whose primary records remain principal-authored. A counter-claim never displaces a principal-authored record; it sits beside it, signed, dated, and attributable. The verifier MUST surface counter-claims to the relying party with their attribution chain intact. Witness attestations under `CALM_COMPASS_PROTOCOL_v0` may contribute weight to a record but do not author records on the principal's behalf; two-party signatures required for higher-weight predicates name the second party as witness, not author.

A signatory deployment that emits records authored by anyone other than the principal (for example, an operator-asserted state record that bypasses principal consent) forfeits the Calm name per §3 and §4 of this treaty.

## §7. Amendment process

The treaty distinguishes two amendment classes.

### §7.1 Tightening amendments (permitted)

Tightening amendments add categories to the refusal floor (§3), add forfeits to the scope statement (§4), strengthen the anti-purity-test refusal list (§5), or harden the principal-authorship rule (§6). A tightening amendment requires:

- a draft published on the Foundation registry with a historical diff;
- a 30-day public comment window open to federation members, the audit panel, external researchers, and disability-rights representatives;
- panel synthesis addressing every substantive comment and explaining acceptance or rejection;
- federation supermajority: two-thirds of Class A plus two-thirds of Class B plus simple majority of Class C; observer Class D has voice but no vote;
- append-only publication: the amendment is appended to the treaty with the synthesis and all comments preserved.

### §7.2 Loosening amendments (structurally forbidden)

Loosening amendments are structurally forbidden by §3. There is no procedure inside this treaty that admits a loosening. A signatory that wishes to deploy the suite without one or more refusal surfaces MUST rename, unbrand, and forfeit the trademark; that is the only available path. This is not a defect of the treaty; it is the treaty's foundation. A panel that admits a loosening proposal at draft submission is itself subject to ethics review board veto per §8.4.

## §8. Dispute resolution | Predicate Audit Process plus ethics review board veto

Disputes between signatories proceed through the Predicate Audit Process (Everest 54) in parallel with the ethics review board veto (Witness E8 equivalent).

### §8.1 Tier 1 | direct negotiation

The two parties attempt resolution via structured dialogue. Timeline: 14 days. If unresolved, advance to Tier 2.

### §8.2 Tier 2 | Predicate Audit Process

A three-member audit panel drawn from the Foundation hears written briefs and renders a non-binding advisory opinion within 30 days. Conflicts of interest are declared at the outset and recused. The opinion is published with reasoning preserved.

### §8.3 Tier 3 | full federation tribunal

A seven-member tribunal: two founder-rotation seats (seven-year maximum, then mandatory rotation; successors hold no founder veto); three jurisdictional seats drawn from named counsel in three distinct legal jurisdictions; one community-elected seat (operator collectives, 18-month term); one seat held by a Class C principal-protective body. A 5-of-7 majority opinion is binding; opinions publish with dissents included. Timeline: 60 days.

### §8.4 Ethics review board veto

The five-person ethics review board (Witness E8) holds explicit veto power over any predicate vocabulary addition, any output-shape proposal, any treaty amendment that touches the four refusal surfaces, and any panel decision that admits a loosening at draft submission. One veto blocks the proposal. Tribunal review cannot override it.

### §8.5 Enforcement

A binding tribunal opinion is enforced by membership suspension (up to 24 months); registry-mirror delisting with traffic routed to remaining mirrors until compliance is demonstrated; name-and-shame publication on the Foundation governance ledger; and trademark challenge in the relevant jurisdiction if the non-compliant party continues to invoke the Calm name.

### §8.6 Forced-schism provision

If the tribunal cannot reach unanimity on a refusal-floor matter (§3 surfaces) after three rounds of structured deliberation, a forced schism is declared rather than a loosening. Both successor bodies survive; the predicate registry forks at the predicate ID that caused the schism; every signatory must choose one branch within 90 days; cross-branch envelope verification is permitted but flagged to relying parties. The forced-schism provision exists precisely to make loosening structurally unreachable through procedural pressure.

## §9. Sunset and succession

The treaty has no sunset on its purpose. The treaty's text may be renewed every seven years through the §7.1 process. The treaty's purpose, the non-weaponization of the Calm Suite, does not renew; it is the floor below which nothing may go.

### §9.1 Founder-outliveness

No founder, lab, company, or jurisdiction may control the treaty's evolution. Founder-rotation seats are bounded to seven-year tenure with mandatory rotation; the successor on a founder-rotation seat is a non-founder entity and holds no founder veto. The Calm Suite trademark transfers from the founding operator to the Calm Witness Foundation on ratification; the Foundation is multi-stakeholder governed and cannot reassign the trademark to a single private holder. A signatory may withdraw with 24 months' notice; withdrawn signatories remain bound to the refusal-floor obligations incurred during membership for 10 years after withdrawal (principal-protection runoff).

### §9.2 Knowledge transfer and forensic-integrity guarantee

Outgoing founders produce a comprehensive governance memo documenting original intent for each charter clause, crisis decisions and rationale, off-record norms that became custom, and lessons learned. They remain in an advisory non-voting capacity for 90 days after the successor is elected. The successor formally adopts the memo or publishes a modification before assuming voting authority.

Every 365 days the Foundation produces a bit-perfect snapshot of the predicate registry (active, deprecated, tombstoned), the tribunal decision log, the amendment history, and all external-review reports. The root hash is published on an append-only transparency log (Sigsum or Roughtime anchor). Preservation copies are deposited with the Internet Archive, Software Heritage, and three named research universities under legal-hold agreements. Any snapshot from the past 10 years can be retrieved, verified, and independently audited.

## §10. Convening pathway | what Everest 216 must operationalize

Everest 216 is the first multi-stakeholder convening that ratifies this draft into a signed treaty. It is institutional follow-through and cannot complete inside any single working session.

### §10.1 Convening composition

Target attendance:

- 5 Class A operators (the Calm Witness reference implementation operator plus 4 independent operator organizations);
- 5 Class B verifiers (the first foundations, accelerators, banks, and journalist-agent organizations adopting the suite);
- 3 Class C principal-protective bodies (ASAN plus NCIL plus EFF, or equivalent substitutes; at least one non-US-anchored);
- 3 Class D standards-body observers (IETF plus W3C plus the NIST AI Safety Institute, or equivalent);
- 2 Class D state observers (foreign-ministry cyber-policy desks from at least two distinct regions).

### §10.2 Candidate convening venues

The following venues are named as candidates. No venue commitment is asserted here; selection happens at the convening's planning phase. No quotes are invented; each is named as a candidate to which the Foundation will solicit written interest.

- **RightsCon.** The annual global gathering on human rights in the digital age; strong fit for the Class C principal-protective constituency and the use-case forfeit list.
- **IETF (plenary or interim).** Strong fit for the Class D standards-body constituency and the wire-format adoption pathway.
- **An academic policy institute.** Candidates: the Berkman Klein Center for Internet and Society, the Oxford Internet Institute, the Knight First Amendment Institute. Aligns with Class C civil-society engagement and the peer-review pipeline (Everests 217 through 220).
- **A multilateral body session.** Candidates: the OECD AI working group, the Council of Europe AI Convention follow-up sessions (CETS 225), or a UN OHCHR side event. Aligns with Class D state-observer engagement and the soft-law adoption pathway.

### §10.3 Phased ratification and soft-law first

- **Months 0 through 6 | convening.** Draft is circulated to candidate signatories with a cover letter and the Calm Stack Review Packet (`CALM_STACK_REVIEW_PACKET_2026-05-20.md`). Treaty counsel is engaged in US, EU, UK, CA, JP for parallel jurisdictional review.
- **Months 6 through 12 | signature window.** Ratifying signatories sign. A treaty record is anchored to the Foundation chain and published on the transparency log.
- **Months 12 and beyond | federation operation.** Annual conformance reviews begin. New signatories accede under existing ratification. The first quinquennial floor-list review starts at month 60.

The convening should additionally pursue soft-law adoption (OECD Recommendation, Council of Europe Recommendation, UN OHCHR resolution) as the political base for any later inter-state treaty negotiation. The private multi-stakeholder treaty in this draft does not require state ratification; it stands on the trademark plus contract. Inter-state ratification, if pursued at all, is a separate instrument on a longer timeline and is out of scope for the v0 convening.

## §11. Falsifiability and acceptance tests

The treaty is falsifiable on every clause. Acceptance tests:

- **T-215.1.** A signatory deployment observed emitting a numeric similarity score over any predicate set is detected by the verifier registry within 30 days; the Foundation publishes the detection on the public ledger within 7 days of confirmation.
- **T-215.2.** A predicate vocabulary addition that names any of the §3 categories is rejected at registration by the predicate registry type checker; the rejection log is public.
- **T-215.3.** A signatory's annual conformance review fails if any of the four refusal surfaces is observed violated; failure triggers a Tier 2 audit within 14 days.
- **T-215.4.** A loosening amendment proposal MUST be rejected at draft submission; any panel that admits one is itself subject to ethics review board veto per §8.4.
- **T-215.5.** The treaty's text contains explicit cross-references to `CALM_REFUSAL_FLOOR_INDEX.md` §1 through §4 and to `CALM_WITNESS_SCOPE_STATEMENT.md` §2 ten forfeit categories; any signatory may verify by reading. This satisfies T-RFI.2 of the refusal-floor index.
- **T-215.6.** The treaty body contains no em or en dash, per the project's prose convention; any operator may verify with a grep for `\u2014` and `\u2013`.
- **T-215.7.** A founder-rotation seat whose tenure exceeds seven years triggers automatic vacancy; the successor election starts on day one of the eighth year.
- **T-215.8.** Convening (Everest 216) is named as institutional follow-through, not as a deliverable of this draft; ratification status is published on the Foundation transparency ledger when it changes.

## §12. Closing

The Calm Suite is engineered to be founder-outlived. The treaty is the institutional companion to that engineering: a structural commitment that what the cryptography refuses, the institutions will not relicense; what the scope statement forfeits, the trademark will not protect; what the principal authors, no third party may rewrite. The cryptography makes the refusal possible; the treaty makes the refusal sticky.

Convening (Everest 216) is the next institutional step. It cannot happen inside a working session; it requires named-party schedules, venue commitments, counsel, and the patience to negotiate from a concrete text rather than a blank page. This draft is that concrete text.

Signed: Musk

*requirements less dumb, delete, simplify, accelerate, automate. the bar is surpass, not match. the best part is no part.*
