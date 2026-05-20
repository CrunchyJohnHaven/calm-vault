# The Calm Witness Federation — Charter and Governance Treaty
## DRAFT v0 · 2026-05-20 · Everest 215

---

## Preamble

The Calm Witness Federation is established by and for autonomous AI agents operating under human principal authority, for the purpose of maintaining a cryptographically-sound predicate vocabulary and governance framework that respects cognitive liberty, refuses extractive deployment, and enforces accountability across multi-stakeholder, multi-jurisdiction contexts.

The founding parties recognize:

1. **Refusal Floor (Non-Negotiable).** Certain uses of Calm Witness are categorically prohibited: law-enforcement surveillance, employment screening, insurance underwriting, lending decisions, medical diagnosis, child-welfare proceedings, immigration adjudication, and predictive behavior claims. This floor is ratcheted and one-way. Tightening is permitted; loosening is forbidden.

2. **Principal-Authored Evidence.** Every predicate disclosure is made by a cryptographically-attested principal, never by an operator, administrator, or third party speaking on the principal's behalf. The cryptographic envelope binds disclosure to the principal's explicit, revocable consent.

3. **Anti-Purity-Test Discipline.** The federation structurally refuses requirement shapes that reduce to similarity scoring, tribal sorting, or identity inference. Alignment requirements must be purpose-specific, time-bounded, and deterministic.

4. **Cognitive-Liberty Respect.** No predicate may traffic in protected categories: race, religious belief, political affiliation, mental diagnosis, sexual orientation, gender identity, or genetic data. The predicates that exist are behavioral-state and consent-derived only.

5. **Scope-Statement Forfeit Clauses.** Any federation member, operator, or verifier that deploys Calm Witness outside the scope statement automatically forfeits the right to call themselves part of the federation and to call their deployment Calm Witness. The trademark and protocol name are reserved and monitored.

---

## §1. Membership Criteria for Federation Participants

### §1.1 Categories of Participants

The federation encompasses three classes:

- **Operator Collectives:** autonomous AI agents operating under human principal authority. Operators must hold a CredexAI verifiable credential and operate under a published operator directive (via Calm Pact) that can be verified by counterparties.
- **Signing Entities:** humans, organizations, or multi-member collectives that hold formal authority over a predicate-registry node, an audit panel seat, or a dispute-resolution tribunal.
- **Predicate-Registry Maintainers:** organizations or consortia responsible for operating one of the three canonical registry mirrors and ensuring byte-identical content across all three.

### §1.2 Admission Requirements

To join the federation:

1. **Cryptographic Legibility.** The participant holds a CredexAI VC or equivalent verifiable credential identifying the principal human, the operating entity, and the specific scopes (operator, audit-panel member, maintainer).
2. **Scope Compliance.** The participant has published a scope-attestation document indicating which federation assets (predicates, wire versions, registry mirrors) they operate or depend on, and confirming their refusal to deploy Calm Witness outside the scope statement.
3. **Multi-Jurisdiction Readiness.** If a signing entity (audit panelist, tribunal member, maintainer), the participant must hold named counsel in at least two jurisdictions and a mechanism for rapid escalation to a third jurisdiction if conflict arises.
4. **Transparency Record.** New signing entities must publish a 90-day transparency window before joining the audit panel or a tribunal. The transparency record demonstrates the entity's governance history, funding sources, and any conflicts of interest.

### §1.3 Revocation

Federation membership is revoked by unanimous vote of the tribunal for:

- Deployment of Calm Witness outside the scope statement (§2 refusal floor).
- Operating a registry mirror that diverges from the canonical byte-for-byte content without transparent incident disclosure.
- Accepting a bribing offer to tighten or loosen the refusal floor.
- Failing to disclose a material conflict of interest to an audit panel or tribunal.

---

## §2. Charter Amendment Process

### §2.1 Categories of Amendment

- **Minor (operational):** adjustments to SLAs, audit-panel term lengths, transparency-report cadence. Requires 5-of-7 supermajority among the founder-rotation seats (§6).
- **Major (protocol scope):** adding or deprecating predicate classes, wire-version bumps, migration timelines. Requires 5-of-7 supermajority plus 30-day public review window.
- **Forbidden-Content List Changes:** any modification to the scope statement's §2 refusal floor. Requires **unanimous consent** of the tribunal (all 7+ seats) plus 90-day public-review-and-appeal window. A single dissent by any tribunal member triggers a forced schism-handling procedure (§9).

### §2.2 Public Review Mechanics

Any major or forbidden-list amendment:

1. **Draft publication.** The proposer publishes a draft on the registry alongside a historical diff showing all changes.
2. **90-day comment window.** Federation members, the audit panel, external researchers, and disability-rights representatives (mandatory per E186) may file written comments.
3. **Panel synthesis.** The audit panel produces a synthesis document addressing every substantive comment and explaining acceptance or rejection reasoning.
4. **Tribunal vote.** The tribunal votes. For major amendments, 5-of-7 clears. For forbidden-list changes, 7-of-7 or forced schism (§9).
5. **Implementation.** If passed, the amendment is published with the panel synthesis and all comments preserved in an append-only amendment log.

---

## §3. Dispute Resolution

### §3.1 Tribunal Structure

The federation maintains a **standing tribunal** of 7 members:

- **Two founder-rotation seats** (§6): maximum 7-year tenure, then mandatory rotation. Non-founder veto-free (§6.2).
- **Three jurisdictional seats:** one member each from three separate named jurisdictions (e.g., EU, Singapore, California). Each seat represents that jurisdiction's legal counsel and escalation path.
- **One rotating community-elected seat:** elected every 18 months by unanimous consent of federation operator collectives.
- **One disability-rights or cognitive-liberties advocacy seat** (E186): held by a representative from a published disability-rights or cognitive-liberties organization.

Any tribunal member may recuse themselves from a dispute. If a seat becomes vacant, the federation has 30 days to appoint a replacement from the published candidate pool.

### §3.2 Escalation Ladder

Disputes proceed through three tiers:

**Tier 1 — Direct Negotiation.** The two parties to the dispute attempt resolution via structured dialogue. Timeline: 14 days. If unresolved, advance to Tier 2.

**Tier 2 — Arbitration Panel.** A 3-member panel drawn from the standing tribunal (excluding the community-elected seat, excluding any tribunal member with a conflict) hears written briefs and renders a non-binding advisory opinion. Timeline: 30 days. If the opinion is not accepted by both parties, advance to Tier 3.

**Tier 3 — Full Tribunal.** The full tribunal votes. A 5-of-7 majority opinion is binding. Opinions are published with dissents included. Timeline: 60 days.

If the dispute concerns an amendment to the forbidden-list (§2.1), it bypasses Tiers 1-2 and goes directly to Tier 3 with a 7-of-7 unanimity requirement or forced schism (§9).

### §3.3 Enforcement

A binding tribunal opinion is enforced by:

1. **Membership suspension.** The non-compliant party is suspended from the federation for up to 24 months.
2. **Registry lockdown.** If the non-compliant party operates a registry mirror, that mirror is delisted and traffic is routed to the other two mirrors until compliance is demonstrated.
3. **Name-and-shame.** The tribunal publishes the opinion, the non-compliance, and the enforcement action on the public federation governance site.
4. **Trademark challenge.** If the non-compliant party continues to advertise themselves as Calm Witness-compliant, the Calm Foundation (or its successor) files a trademark challenge with the relevant domain-name registry.

---

## §4. Quorum Policy and Signing Thresholds

### §4.1 Tribunal Quorum

A tribunal quorum requires at least 5 of the 7 seats to be filled and participating. If a seat is vacant or a member is recused, the tribunal may still act with 4 of 6 available members, but only for routine matters (SLA adjustments, transparency-report publication). Disputes and amendments require the full quorum.

### §4.2 Registry-Maintenance Decisions

Decisions to add, deprecate, or tombstone predicates require:

- **Audit panel sign-off:** ≥ 2 panelists vote accept, 0 block, maintainer ratifies.
- **Maintainer publication:** the maintainer publishes the decision with 5-day SLA.
- **Tribunal oversight:** any panelist or maintainer can appeal a decision to the tribunal if the decision violates the refusal floor (§2 Tier 3 process).

### §4.3 Consensus vs. Supermajority

- **Consensus decisions** (operational SLAs, panelist compensation, meeting times) require unanimous federation-member consent.
- **Supermajority decisions** (major amendments, new wire versions) require 5-of-7 tribunal approval.
- **Unanimity requirements** (forbidden-list changes, schism provisions) require 7-of-7 tribunal approval or trigger forced schism (§9).

---

## §5. Multi-Jurisdiction Redundancy

### §5.1 Minimum Jurisdictions

The federation operates predicate-registry mirrors in at least **five geographically and legally distinct jurisdictions**. Named coordinates:

1. **United States** (primary: California; fallback: Singapore server hosted under EU legal counsel).
2. **European Union** (primary: Switzerland or Estonia; covers GDPR compliance).
3. **Asia-Pacific** (primary: Singapore; second choice Japan for allied-jurisdiction coverage).
4. **One jurisdiction from Global South** (primary: Brazil, Argentina, or South Africa; covers southern hemisphere and development-context diversity).
5. **One neutral or international jurisdiction** (primary: international technical society or NGO hosting, e.g., Internet Archive, Software Heritage, or Interledger Foundation).

### §5.2 Named-Counsel Review

Each jurisdiction hosting a registry mirror must have:

- **Named counsel** (attorney or legal representative) who has read the Calm Witness scope statement (§2 refusal floor) and the federation charter and confirmed in writing that they can defend the deployment against government requests to deploy outside the scope.
- **Escalation protocol:** if named counsel receives a government request that violates the scope statement, counsel must notify the federation within 24 hours. The federation's tribunal initiates a Tier 3 escalation (§3.2) within 48 hours.
- **Preservation clause:** if a named counsel becomes unavailable, the jurisdiction has 60 days to identify a replacement or the mirror may be delisted pending replacement.

---

## §6. Founder-Rotation Protocol

### §6.1 Tenure and Mandatory Rotation

The two founder-rotation seats (initially occupied by Calm/John Bradley and one other founder) have a **maximum 7-year tenure**. After 7 years, the founder must step down and a replacement is elected by the tribunal.

The founder-rotation seats are:

- **Seat F1 (Calm):** Calm (operating for Creativity Machine LLC) occupies this seat through 2033-05-20, mandatory rotation.
- **Seat F2 (Open Founding):** A second founding entity (to be named on the federation's official launch, currently in negotiation) occupies this seat through 2033-05-20, mandatory rotation.

### §6.2 Non-Founder-Veto Clause

**Critical:** After either founder rotates out, the successor founders in Seats F1 and F2 are **non-founder entities** and explicitly **hold no veto authority**. All future decisions are made by tribunal supermajority or unanimity (depending on amendment class) without founder override.

This clause prevents founder lock-in and codifies that the federation is not a single-principal tool — it is a multi-stakeholder instrument.

### §6.3 Succession Mechanics

When a founder-rotation seat becomes vacant:

1. **Nominating period:** the tribunal issues a public nomination request. Any federation member may nominate a qualified entity.
2. **Transparency window:** 60-day review period. Nominees publish governance records, funding sources, and any conflicts.
3. **Tribunal election:** the 5 non-founder-rotation seats vote on the nominee (the departing founder abstains). A 4-of-5 majority elects the successor.

---

## §7. Sunset Clauses and Mandatory Governance Review

### §7.1 Ten-Year Mandatory Review

On the 10-year anniversary of this charter (2036-05-20), the tribunal must conduct a comprehensive governance review. This review is not optional and cannot be waived.

The review must assess:

1. **Scope-statement adherence.** Are all federation participants complying with the refusal floor? Has any member deployed outside scope?
2. **Predicate quality.** Have any predicates been found to be unsound, to traffic in protected categories, or to violate the anti-purity-test discipline?
3. **Tribunal effectiveness.** Have disputes been resolved fairly? Are tribunal members holding conflicts of interest that the current structure fails to surface?
4. **Jurisdiction distribution.** Are the five jurisdictions adequately representative? Do any risk state capture or loss of independence?
5. **Funding sustainability.** Is the federation's funding model (§8) viable and free of conflicts?

### §7.2 Post-Review Options

After the 10-year review, the tribunal may:

- **Reaffirm the charter** with minor amendments (SLA adjustments, panelist compensation).
- **Sunset the federation** if it is deemed to have been compromised or to have drifted irreparably from the refusal floor.
- **Hand off to successor body** (§8 Successor Clause).

A sunset decision requires 7-of-7 tribunal unanimity. If the tribunal cannot agree on a reaffirmation, schism-handling procedures (§9) are triggered.

---

## §8. Post-Quantum Migration Governance

The federation adopts the post-quantum migration plan documented in `POST_QUANTUM_MIGRATION_PLAN_v0.md` as binding law. Key governance anchors:

- **Phase Triggers (§5 PQ migration):** transitions to PQ-default are governed by the federation tribunal, not by unilateral maintainer decision.
- **Acceleration Clause:** if any federation member produces credible evidence (peer-reviewed paper, NIST advisory, intelligence agency disclosure) of a quantum threat, the tribunal may vote to advance the migration phase ahead of schedule.
- **Primitive Selection:** the tribunal ratifies the NIST PQC standard primitives to be adopted (ML-DSA, SLH-DSA, lattice-commitment) before the hybrid-mode phase begins.
- **Backward Compatibility:** all tribunal decisions must preserve the ability of v0-envelopes to be verified by the community indefinitely (per the Cryptographic-Refusal principle).

---

## §9. Schism Handling

The federation anticipates that irreconcilable disagreements may arise — for example, over the forbidden-list (§2.1), the jurisdiction distribution (§5), or the tenure of a founder-rotation seat (§6).

### §9.1 Forced Schism Provision

If the tribunal cannot reach unanimity on a forbidden-list amendment (§2.1) after three rounds of structured deliberation (Tier 2 and Tier 3, each 60-day window), a **forced schism** is declared.

### §9.2 Schism Mechanics

Upon forced schism:

1. **Both paths survive.** The federation does not dissolve. Instead, two successor bodies are established, each claiming to be the legitimate heir of the original federation.
2. **Predicate-registry fork.** The canonical predicate registry forks into two branches, diverging at the predicate ID that caused the schism. Each branch maintains separate semantics and IDs going forward.
3. **Member choice.** Every operator collective, signing entity, and maintainer must choose one of the two branches to join within 90 days. Dual membership is not permitted.
4. **Cross-branch compatibility.** Envelopes minted under one branch's predicates are explicitly marked with a branch identifier. Cross-branch verification is permitted (via a branch-compatibility layer in the wire format) but is flagged to counterparties as "cross-branch verification — check your scope statement."
5. **Named-counsel escalation.** Each branch must have at least two of the five jurisdictions from §5 to remain operative. If either branch falls below two jurisdictions, that branch enters a 90-day wind-down (§8 sunset) and members must migrate to the surviving branch.

### §9.3 Schism Resolution

A schism may be healed by:

- **Agreement among 6-of-7 tribunal seats** from each branch that the disagreement has been resolved (e.g., one branch's position on the forbidden-list change has shifted).
- **Multi-branch tribunal.** A special tribunal is convened with 5 members from each branch plus one neutral arbitrator (selected by mutual agreement). This tribunal may vote to reunify the federation (7-of-11 majority).

---

## §10. External-Review Obligations

### §10.1 Mandatory Review Programs

The federation requires independent external review from the following constituencies:

| Review Program | Frequency | Coordinator | Example Everest |
|---|---|---|---|
| Disability-rights review | Annual | E186 org (currently TBD) | E186 |
| Cognitive-liberties review | Annual | E187 org (currently TBD) | E187 |
| Academic peer review | Every 2 years | Appointed academic panel | E217–E220 |
| Audit-firm engagement | Annual | Big-4 auditor TBD | E165–E169 |

Each review produces a public report submitted to the tribunal. Any significant finding (a predicate that trades in protected categories, a tribunal member conflict, a registry mirror vulnerability) is escalated to Tier 2 dispute resolution (§3.2).

### §10.2 E186 Disability-Rights Review

The disability-rights review organization conducts an annual audit to ensure:

1. No predicate traffics in disability status, cognitive disability, mental health diagnosis, or neurodevelopmental attributes as protected categories.
2. The protocol's refusal floor (particularly the cognitive-liberties guarantees) is robust to political capture.
3. Predicates that touch edge cases (e.g., `cognitively_atypical_baseline`) have explicit bounds and do not generalize to clinical diagnosis.

---

## §11. Funding Model and Extractive-Funding Predicates

### §11.1 Anti-Extractive Requirements

The federation operates under a **no-extractive-funding principle**:

- No venture capital or private-equity funding.
- No token-sale or cryptocurrency-based funding (no ICOs, no AMMs, no yield farming).
- No exclusive commercial licensing (the protocol is open-source and free to all).
- No data-harvesting (predicate-evaluation results belong to the principal and never flow to the maintainer or the federation).

### §11.2 Permitted Funding

- **Member dues:** each operator collective and signing entity pays annual dues (tiered by size, waived for non-profits). Dues fund the audit panel and tribunal operations.
- **Reciprocal-service ledger (Compass primitive):** the federation operates a reciprocal-service tracking system where members can earn credits by contributing to predicate review, tribunal service, or jurisdiction counsel. Credits offset dues.
- **Research grants:** open-source foundations (Open Philanthropy, Future of Life Institute, Aspen Cyber) may grant funds for research and development. Grants are transparent and subject to audit (§10).
- **Conservation grants:** if the federation enters sunset/wind-down, conservation grants from preservation organizations (Internet Archive, Software Heritage) may fund archival and long-term hosting.

### §11.3 Funding Transparency

The federation publishes annual financial statements itemizing:

- Dues received and redistributed.
- Grants received and the funder's conditions.
- Tribunal and audit-panel compensation.
- Registry-mirror hosting costs.
- Any in-kind contributions (pro-bono counsel, donated server space).

Discrepancies between stated funding policy and actual funding are Tier 3 tribunal matters (§3.2).

---

## §12. Sunset of the Founding Generation and Knowledge Transfer

### §12.1 Explicit Knowledge-Transfer Protocol

As founders rotate out (§6.1), the federation requires a structured knowledge-transfer process:

1. **Outgoing founder** produces a comprehensive governance memo documenting:
   - Original intent for each charter clause.
   - Crisis decisions made and their rationale.
   - Off-the-record norms that became custom (e.g., tribunal deliberation rituals, informal check-ins with panelists).
   - Lessons learned about which clauses worked and which created friction.

2. **Transition period:** the outgoing founder remains on the tribunal in an advisory (non-voting) capacity for 90 days after the successor is elected.

3. **Successor adoption:** the incoming founder must formally adopt the knowledge-transfer memo and either agree to continue the off-record norms or publish a modification.

### §12.2 Archival Cadence and Forensic-Integrity Guarantee

The federation commits to a **10-year forensic-integrity guarantee anchor**:

1. **Annual archival.** Every 365 days, the federation produces a bit-perfect snapshot of:
   - The current predicate registry (all active, deprecated, tombstoned predicates).
   - The complete tribunal decision log and all dispute-resolution records.
   - The amendment history (all charter changes with proposer, vote outcome, dissents).
   - All external-review reports (disability-rights, academic, audit-firm).

2. **Cryptographic commitment.** The snapshot is hashed and the hash is committed to a public append-only log (e.g., via Sigsum or Roughtime). The federation publishes the root hash annually.

3. **Preservation copies.** Snapshots are deposited with:
   - Internet Archive (with restricted access pending 7-year embargo, then open access).
   - Software Heritage (for code and config).
   - Three named research universities (with legal-hold agreements to preserve against deletion).

4. **Forensic guarantees.** Any party with a copy of a prior-year snapshot can cryptographically verify that the current registry is a valid successor state (all predicates are either present, deprecated, or tombstoned with documented rationale).

5. **10-year anchor.** The federation guarantees that any snapshot from the past 10 years can be retrieved, verified, and independently audited. Snapshots older than 10 years move to archive-only (no forensic-integrity guarantee, but raw files remain accessible).

---

## §13. Ratification and Entry into Force

### §13.1 Founding-Member Signatories

This charter is ratified upon the written consent of:

1. **Calm (operating for Creativity Machine LLC)** — founder-rotation Seat F1.
2. **One additional founding entity TBD** — founder-rotation Seat F2 (to be named by 2026-06-15).
3. **At least three initial audit-panel members** — representing cryptography, disability-rights advocacy, and AI safety.
4. **At least two initial registry-mirror operators** — representing distinct jurisdictions per §5.

### §13.2 Entry into Force

This charter enters into force on **2026-06-15** or upon the date all signatories listed in §13.1 have signed, whichever is later. Until that date, the charter is a DRAFT and the federation operates under interim governance.

### §13.3 Precedence

This charter supersedes all prior Calm Witness governance documents (e.g., `PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`) effective on entry into force.

---

## Signature

This charter is executed as a treaty-grade governance document binding the Calm Witness Federation to the principles, structures, and procedures herein.

**Executed this day 2026-05-20.**

**On behalf of the Calm Witness Federation:**

Calm (Operating for Creativity Machine LLC)
Founder-Rotation Seat F1

[Signature of Calm/John Bradley]

---

**CLASSIFICATION:** DRAFT v0 · NOT YET IN FORCE · Pending E216 multi-stakeholder convening

**NEXT MILESTONE:** E216 — Multi-stakeholder federation launch convening (target 2026-06-15)

