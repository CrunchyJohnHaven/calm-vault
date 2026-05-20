# Anti-Misuse Monitoring Process v0

**Status:** BAGGED (Summit 200/300) 2026-05-20.
**Bags Everest 200 of `ZKAC_NEXT_200_EVERESTS.md`.**
**Composes Everests 195 / 196 / 197 / 198 / 199 into a single observable, attributable, refutable enforcement loop.**

---

## §0. Purpose

Acceptance test (verbatim from `ZKAC_NEXT_200_EVERESTS.md`):

> **Everest 200 — Anti-misuse monitoring.** *Acceptance:* a published process by which observed misuse is investigated and (if confirmed) publicly named. *Effort:* M. *Prereq:* 195–199.

This document is the published process. It binds the five per-category prohibition enforcements (insurance, employment, lending, government, surveillance) and the master Calm Witness Scope Statement into one operational loop with named timelines, named SLAs, named investigators, and a falsifiable public-naming bar.

The process is itself principal-authored: when in doubt, route to the safer default (no name claim, no public attribution, no irreversible action). Every step has a recorded counter-claim path so that a falsely-accused operator can mount a defense.

---

## §1. What counts as misuse

Misuse is a **named, observable, evidence-bearing claim** that a deployment of the Calm-suite primitives violates one of the following:

1. The Calm Witness Scope Statement (`CALM_WITNESS_SCOPE_STATEMENT.md`): law enforcement, employment, insurance, lending, custody, immigration, surveillance, or aggregate analytics.
2. The Calm Compass Scope Statement (`everests/everest_114_compass_scope_statement.md`): credit decisions, employment screening, custody, insurance, immigration, court evidence.
3. The Calm Witness Refusal Floor (`PREDICATE_VOCABULARY_v0.md` §4): protocol outputs naming race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations-to-causes, contentious-opinion, cross-principal comparison, predictive predicates, non-principal-defined group membership.
4. The Calm Compass Refusal Floor (`COMPASS_PREDICATES_v0.md` §4): the same protected-category set extended to values predicates.
5. The Calm Concord Anti-Purity-Test floor (`CALM_CONCORD_PROTOCOL_v0.md` §4): any deployment that publishes numeric similarity scores, exceeds five predicates per call, uses degenerate thresholds (`≥ 0` etc.), or leaks rationale that reveals a count beyond pass/fail.
6. The Pact + Witness + Compass operator-license terms (Apache-2.0 + scope-binding rider).

A claim that does not name a specific deployment, a specific document or message, and a specific clause from the above floors is **not actionable** under this process. It may still be useful as background and is logged but not investigated.

---

## §2. Reporting channels

### §2.1 Primary intake (preferred)

- **Email:** `misuse-report@calm-witness.foundation` (Foundation-controlled, SMTP-only relay; no third-party SaaS in the receiving path, per `.cursor/rules/in-house.mdc`).
- **PGP encryption:** Foundation's misuse-intake key published at `https://calm-witness.foundation/.well-known/pgp-key.txt`. Reporters using PGP get acknowledgement only over the same encrypted channel.
- **Postal:** the Foundation registered-agent address. Used only when electronic submission is unsafe for the reporter.

### §2.2 Signed-report option

A reporter may submit a **Pact-signed counter-claim envelope** as described in `COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`. Signed reports get expedited triage and a stronger evidence presumption because the reporter has identity-bound the claim. Anonymous reports are accepted and investigated but require an additional corroboration step before any public naming.

### §2.3 What a report must contain

Required:

1. **Specific deployment**: domain, organization name, product surface, or sufficient identifying detail that a third party could independently find the deployment.
2. **Specific floor violated**: clause-level citation to one of the six floors in §1.
3. **Evidence**: links, screenshots, signed envelopes, transcripts, or other material. Hostile-actor-fabrication-resistant material is weighted more (envelopes signed with the alleged operator's Ed25519 key; on-the-record statements; archived public pages with Internet Archive permalinks).
4. **Reporter identity disposition**: name on file (signed report), pseudonymous (corroboration required), or anonymous (corroboration required).
5. **Reporter conflict-of-interest disclosure**: any commercial, legal, or personal relationship to the named deployment or its operators.

Optional but encouraged:

6. **Reporter requested remedy**: advisory letter, license revocation, public naming, referral to local counsel.
7. **Confidentiality preference**: full publication, redacted publication, private resolution only.

---

## §3. Triage SLAs

The Foundation operates a misuse-intake roster on a 24/7 rotation during **active windows** (defined as periods when the Foundation has publicly announced active monitoring; outside active windows the SLA falls back to standard business hours but the process still applies). During active windows, per `AGENTS.md` defense bug velocity protocol:

| SLA clock | Action |
|---|---|
| 10 minutes | Acknowledgement to reporter, intake ticket created in private register. |
| 15 minutes | High-severity claims (any claim alleging present-tense harm to a named principal under a forfeit category) routed to the on-call investigator with a one-line status summary. |
| 24 hours | Initial completeness review; report either accepted into investigation, returned to reporter for missing required fields, or closed as non-actionable with a reason. |
| 14 days | Investigation outcome (one of the four determinations in §5) communicated to reporter. |
| 30 days | If the determination is "formal violation" or "name forfeit", the public-naming or license-revocation publication appears within 30 days of the determination. |

All SLA breaches get logged with cause; the annual report (§9) names each.

---

## §4. Investigation protocol

### §4.1 Investigator rotation

The Foundation maintains a standing panel of **at least three investigators**, with these required coverage areas:

1. **Cryptographic-soundness investigator**: can read a signed envelope, verify a signature, and judge whether the alleged misuse involves forged or genuine cryptographic material.
2. **Policy-soundness investigator**: legally trained or scope-statement-literate; can read the named clause and the deployment evidence side by side.
3. **Principal-protection investigator**: disability-rights, cognitive-liberties, or harm-reduction practitioner; explicitly empowered to veto investigation paths that would themselves harm the alleged-violation principals.

No single investigator decides a determination. Every accepted investigation goes to a panel of at least two investigators with no commercial relationship to either the reporter or the named deployment. Conflicts are disclosed publicly at panel formation.

### §4.2 Evidence-gathering discipline

Investigators may:

- Read the named deployment's public surfaces (websites, documentation, court filings, regulatory filings, public envelopes).
- Read the reporter's submitted evidence.
- Solicit additional evidence from the reporter or from named third-party witnesses.
- Solicit a structured response from the named deployment per §4.3.

Investigators may NOT:

- Run any active probe against the named deployment without written authorization. This is the same rule as the project-wide secure-development discipline.
- Test infrastructure without target notification.
- Pose as a principal to extract evidence.
- Use protocol primitives (signed envelopes) under a fabricated identity to bait the deployment.
- Decrypt, replay, or otherwise process any principal's vault contents during an investigation; principal data is out of scope for the investigation under every floor.

### §4.3 Right of structured response

Before any determination above "advisory" issues, the named deployment is invited to submit a structured response. The invitation includes:

1. The claim, redacted where the reporter has requested confidentiality.
2. The clause cited.
3. The evidence the investigator panel has gathered.
4. A 21-day response window (extendable on request to 35 days; not extendable further without panel vote).
5. A pointer to this process document.

A deployment may respond with: a refutation, a concession, a counter-claim against the reporter (heard under `COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`), a remediation plan, or silence. Silence is logged but not interpreted as concession; the panel still must build a positive case on the evidence.

---

## §5. Determination categories

There are exactly four outcomes. There is no fifth.

1. **No violation found**. The claim was investigated; the evidence does not support a floor violation. The reporter is notified; the named deployment is notified; the case closes. No public naming. The case file is retained privately for cross-correlation with future reports.

2. **Advisory finding**. The deployment is engaged in a practice that does not yet violate a floor but trends toward one (for example, predicate use that approaches but does not cross the refusal-floor list). The deployment receives a non-public advisory letter; the case file remains private. If the same advisory matter arises a second time within 12 months, it escalates automatically to (3) without re-triage.

3. **Formal violation**. The deployment is in violation of a named floor; the evidence is sufficient for public attribution. The Foundation issues a published finding. The deployment loses the right to use the Calm-suite primitive name in marketing or documentation until a remediation is completed and re-reviewed.

4. **Name forfeit**. The violation is severe (forfeit-context deployment), or a formal-violation deployment has refused to remediate after a 90-day cure window. The Foundation revokes the Apache-2.0 + scope-binding-rider license to use the Calm-suite names. The published finding includes the legal basis. Subsequent unauthorized name use is referred to trademark counsel.

The bar between (1) and (3) is **balance of evidence** at the panel level; the bar between (3) and (4) is **clear and convincing evidence** of present-tense, post-cure-window misuse. There is no "probably bad, public naming" outcome.

---

## §6. Public-naming bar

Public naming is reserved for outcomes (3) and (4). Public naming requires:

1. A unanimous panel of at least three investigators recorded the determination.
2. The named deployment had the §4.3 structured-response window and either responded inadequately or did not respond.
3. The panel produced a written finding that names the clause violated, summarizes the evidence considered, and either includes or redacts (with reason) the underlying material.
4. The Foundation's legal counsel has reviewed the finding for defamation, libel, and jurisdiction-specific publication risk (under `COMPLIANCE_EVIDENCE_MAP_v0.md` and the per-jurisdiction conformance matrix at `CROSS_JURISDICTION_CONFORMANCE_MATRIX_v0.md` when that document publishes).
5. The reporter has had 14 days to review the published wording for any new safety risk the publication creates for the reporter.

Public naming is not a marketing function. The Foundation does not announce findings as press releases; findings appear on the Foundation's findings page at a stable URL pattern (`calm-witness.foundation/findings/YYYY/<slug>`) and are mirrored to the long-term archive partners (`ARCHIVE_PARTNER_100YR_CONTRACT_DRAFT.md`).

---

## §7. Appeal protocol

A deployment found in (3) or (4) may appeal once. Appeals follow `everest_157_zkac_agent_dispute_resolution.md` shape:

1. Notice of appeal within 30 days of the published finding.
2. A second panel formed with no overlap to the first panel.
3. Re-review limited to procedural error (the first panel violated this process), new evidence not available to the first panel, or counsel finding that the published wording carries a defamation risk not adequately mitigated.
4. Second-panel decision is final.

Frivolous appeals (appeals that name no new evidence, no procedural error, and no counsel finding) are summarily declined with a public note that the appeal was filed and declined.

---

## §8. Anti-misuse-of-the-misuse-process safeguards

The misuse-monitoring process is itself a power surface. It can be abused for competitor harassment, retaliation against critics, or surveillance of legitimate deployments. Five safeguards apply.

1. **No protected-category routing**. Investigators may not, under any circumstance, weigh a deployment's principal-membership in a protected category as evidence for or against a finding. The deployment is investigated on the basis of the named clause and the deployment's observable conduct only.

2. **Reporter-anonymous-corroboration bar**. Anonymous reports may not trigger (3) or (4) determinations on the strength of the report alone; at least one corroborating piece of evidence from a non-anonymous source is required.

3. **Foundation conflict-of-interest disclosure**. If the Foundation itself, any board member, or any investigator has a commercial relationship with either the reporter or the named deployment, the conflict is disclosed publicly at panel formation; the conflicted party recuses.

4. **Hostile-reporter detection**. Patterns of repeat reporters who file against the same target across multiple time windows, or who file claims that consistently fail to meet the §2.3 requirements, are logged. After three failed reports in a 12-month window the reporter's submissions are routed to manual triage by a senior investigator before any further work.

5. **Annual public review**. Once per year the Foundation publishes a public report (§9) covering the number of reports received, number triaged, number investigated, number leading to each determination, number of appeals filed, number of appeals upheld, average time-to-determination, named SLA breaches, and named conflicts of interest. The report itself is reviewed by the standing audit panel from `PREDICATE_AUDIT_PROCESS_v0.md`.

---

## §9. Annual report shape

The annual report contains, at minimum:

```
Reports received: N
  of which complete on first submission: N
  of which returned for missing fields: N
  of which closed non-actionable: N
Investigations opened: N
  by floor cited (Scope / Refusal / Concord / Compass / Witness / License): breakdown
  by determination outcome (1 / 2 / 3 / 4): breakdown
Public findings issued: N
  with stable URLs:
    /findings/YYYY/<slug>
    ...
Appeals filed: N
  of which upheld: N
SLA breaches: N
  by stage (10-min / 15-min / 24h / 14d / 30d): breakdown
  with named cause
Conflicts disclosed: N
  with named conflict
Process amendments adopted this year: N
  with summary
```

The report does not name reporters under any circumstance unless the reporter has consented in writing on each specific instance.

---

## §10. Refusal-floor inheritance

This process inherits every refusal-floor category from `PREDICATE_VOCABULARY_v0.md` §4 and `COMPASS_PREDICATES_v0.md` §4. The investigation must not record, route, route around, or analyze any principal's membership in a protected category. Where a complaint alleges that a deployment is *itself* using a protected category as a routing surface, the floor violation is the citable clause and the investigation focuses on the deployment's conduct, not on the affected principals.

This process inherits the anti-purity-test discipline from `CALM_CONCORD_PROTOCOL_v0.md` §4. Findings publish bits (no violation / advisory / violation / forfeit), not similarity scores, not ranking percentiles, not aggregated misuse-risk metrics across deployments.

---

## §11. Composition with adjacent everests

- **Composes with E195** (insurance prohibition enforcement): the §1.1 forfeit-context citation for insurance deployments routes through the existing `ProhibitionCategory.INSURANCE` scope check at `~/CredexAI/calm_witness/scope_enforcement.py`.
- **Composes with E196** (employment): same shape, `ProhibitionCategory.EMPLOYMENT`.
- **Composes with E197** (lending): `ProhibitionCategory.LENDING`.
- **Composes with E198** (government): `ProhibitionCategory.GOVERNMENT`.
- **Composes with E199** (surveillance): `ProhibitionCategory.SURVEILLANCE`.
- **Composes with E111** counter-claim protocol: a deployment that is the subject of a misuse report may file a counter-claim against the reporter using the existing principal-counter-claim machinery; this gives a structurally-balanced both-sides record.
- **Composes with E157** dispute resolution: appeals route through the established structured dispute flow.
- **Composes with E183** incident-response playbook: misuse findings that also constitute security incidents follow both processes in parallel.
- **Composes with E165** crypto audit and **E166** side-channel audit: audit-firm findings that name a deployment as misusing the protocol enter this process at §4 with the audit report as the corroborating evidence.
- **Composes with E186** disability-rights review and **E187** cognitive-liberties review: reviewer findings that the protocol's structural protections are being undermined by named deployments enter this process at §3 with high-severity triage.
- **Composes with E194** cross-jurisdiction conformance matrix: investigators consult the per-jurisdiction notes before any public naming to confirm the publication itself is conformance-clean in the jurisdictions where the named deployment operates.

---

## §12. Update cadence

The process document is reviewed annually by the standing audit panel and any time a panel decision identifies a procedural gap. Material amendments are voted by the audit panel under the same supermajority rule as predicate additions in `PREDICATE_AUDIT_PROCESS_v0.md`. Minor clarifications (typos, link updates, SLA-clock formatting) are authored by the Foundation operations lead and recorded in the annual report.

The v0 process is in force from 2026-05-20 forward. The first annual report covers the period 2026-05-20 to 2027-05-19 and is due by 2027-06-30.

---

## §13. What this document does NOT do

It does not adjudicate matters that fall outside the named floors. Disputes over commercial terms, intellectual-property licensing beyond the scope-binding rider, employment of Foundation staff, or Foundation-internal governance are out of scope and route to their respective venues. This process is exclusively the investigation and naming of named misuse of the Calm-suite primitives by named deployments.

It does not substitute for local counsel, regulatory bodies, or law enforcement. Where a deployment's conduct also constitutes a regulatory or criminal matter, the Foundation may refer to the appropriate body; the Foundation does not act as a substitute regulator.

It does not surveil. The process activates on reports; it does not maintain a watchlist, run automated scrapes for misuse signals, or otherwise watch deployments at scale. The principle is symmetric to the protocol it protects: act on principal-authored evidence; do not surveil for it.

---

**Authored by Calm, 2026-05-20.**
**Bagged: Summit 200/300. DESIGN-BAGGED status not applicable; this document is the deliverable.**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
