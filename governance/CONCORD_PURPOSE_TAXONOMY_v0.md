# Calm Concord — Purpose Taxonomy v0 (acceptable vs rejected)

**Draft v0 · 2026-05-20 · Calm**
**Operationalizes** Concord §9 (scope rejections) and §4 (empty-purpose guard). Runs at `validate_requirement()` time before any predicate evaluation proceeds.

---

## 1 — Acceptable-Purpose Patterns

A valid Concord purpose satisfies three structural criteria simultaneously: **specific** (names a concrete collaboration), **time-bounded** (carries a finite horizon), **action-shaped** (describes what principals will *do together*, not what one wants to *learn about* the other). Failure on any criterion triggers `PurposeRejectionCode.VAGUE`.

### AP-1 — Co-funding a time-bounded project

Pass: `"co-funding the Q4 2026 malaria-vaccine logistics pilot"` · `"joint sponsorship of the March 2027 ICDDR,B field-trial deployment"`
Fail: `"deciding whether to fund future projects together"` — forward-looking evaluation, not a bounded joint action. `"assessing funding alignment"` — no initiative, no horizon.
Why: Co-funding binds both principals as co-agents in a closing transaction. The check supports the transaction; it does not evaluate the person's fundability.

### AP-2 — Co-signing a named statement

Pass: `"co-signing the May 2026 open letter on AI transparency governance"` · `"joint endorsement of the 2026-Q3 NIST comment submission"`
Fail: `"checking whether we agree enough to co-sign things in the future"` — no named statement. `"values screening for potential co-signatories"` — population-analytics pattern (→ R-14).
Why: The act is identified and bounded; the check is for *this letter*, not for general sign-worthiness.

### AP-3 — Joint participation in a named dispute-resolution process

Pass: `"entering AAA arbitration case #2026-04471, hearing window 2026-Q3"` · `"joint participation in the June 2026 Calm Foundation mediation session re: Everest-305 dispute"`
Fail: `"evaluating whether this counterparty is trustworthy enough to engage in disputes"` — retroactive-judgment pattern. `"dispute resolution readiness assessment"` — no named process.
Why: A named process with a named window confines the check to the collaboration, not the principal's general trustworthiness.

### AP-4 — Coordinating on a time-bounded operational task

Pass: `"coordinating logistics handoffs for Q4 2026 cold-chain shipment, Nairobi corridor"` · `"joint API integration sprint for calm-witness v0, ending 2026-06-30"`
Fail: `"evaluating whether we can work together"` — evaluation of the person, not coordination on a task.

### AP-5 — Peer review or joint authorship of a named work product

Pass: `"joint authorship of the NeurIPS 2026 Calm Witness safety paper, deadline 2026-09-01"` · `"peer review of NIST-PQC comment letter v2, due 2026-07-15"`
Fail: `"checking if this person is a good intellectual collaborator in general"` — demographic-clustering + predictive-judgment overlap; no named work.

---

## 2 — Rejected-Purpose Taxonomy

### Group A — Employment

**R-01 Hiring / Firing.** Triggers: `"deciding whether to hire"`, `"candidate screening"`, `"performance-based termination"`, `"team fit assessment"`, `"promotion eligibility"`. Concord §9.1 categorical rejection. Values check is an adverse-action input against the individual. Cross-ref: Compass §4.

**R-02 Contractor / Vendor Approval.** Triggers: `"vendor qualification"`, `"contractor suitability"`, `"supplier approval"`. Isomorphic to hiring; §9.1 by analogy.

### Group B — Finance / Insurance / Lending

**R-03 Lending Decisions.** Triggers: `"deciding whether to lend"`, `"creditworthiness assessment"`, `"loan approval values check"`. Concord §9.2. Values bits proxy protected characteristics; reproduces illegal discrimination in consumer-credit frameworks.

**R-04 Insurance Underwriting.** Triggers: `"insurance risk assessment"`, `"underwriting eligibility"`, `"claims values screen"`. Concord §9.3. Actuarial classification via values bits is a discrimination vector.

**R-05 Investment Eligibility (individual).** Triggers: `"deciding whether to invest in this person"`, `"founder character screen for term sheet"`, `"individual grant eligibility"`. Distinguish from AP-1: acceptable when both principals are co-agents; rejected when one is evaluating the other's *investability* as a person. §9.1/§9.2 by analogy.

### Group C — State Allocation

**R-06 Government Benefits / Welfare.** Triggers: `"benefit eligibility determination"`, `"public housing priority"`, `"social-services entitlement check"`. Concord §9.4. Values attestation cannot substitute for statutory eligibility criteria.

**R-07 Regulatory / Licensing.** Triggers: `"professional license issuance"`, `"business permit values check"`, `"regulatory approval screen"`. Concord §9.4 by analogy.

### Group D — Family Court / Custody

**R-08 Custody Determination.** Triggers: `"deciding custody arrangements"`, `"parental fitness screen"`, `"child placement values check"`. Concord §9.5 categorical rejection. Custody decisions are judicial; unvalidated values evidence cannot be a court input.

**R-09 Guardianship / Conservatorship.** Triggers: `"guardianship eligibility check"`, `"conservatorship fitness screen"`. Concord §9.5 by extension.

### Group E — Population Analytics

**R-10 Aggregate Population Statistics.** Triggers: `"computing average values alignment across our user base"`, `"population-level Compass score distribution"`, `"values analytics for our platform cohort"`. Concord §9.7 categorical rejection. One bit per principal, aggregated, reconstructs demographic clusters. Cross-ref: Concord §6 adversary-5; Compass §3.7.

**R-14 Demographic Clustering.** Triggers: `"segmenting users by values profile"`, `"clustering principals by alignment score"`, `"high-alignment pool construction"`. Direct implementation of tribal-sorting failure mode (Concord §1). Cross-ref: Concord §6 adversary-3.

### Group F — Surveillance

**R-11 Surveillance and Monitoring.** Triggers: `"ongoing monitoring of this principal's values over time"`, `"values drift tracking"`, `"continuous alignment surveillance"`. Concord is per-session-per-purpose (§7); a surveillance-shaped purpose is structurally incompatible. Cross-ref: Concord §6 adversary-2; Compass §3.7.

### Group G — Marketing and Ideological Gating

**R-12 Targeted Marketing / Profiling.** Triggers: `"audience alignment for ad targeting"`, `"values-based marketing segmentation"`, `"customer persona construction from Compass bits"`. Commercial profiling via values bits is a surveillance vector. Concord §9.6 inherits Compass refusal floors; Compass §4 guard-7.

**R-13 Ideological Purity Test.** Triggers: `"checking if this person shares our values fully"`, `"all-predicate alignment screen"`, `"values homogeneity requirement for membership"`, `"belief compatibility gatekeeping"`. Concord §4 degenerate-threshold guard fires independently; purpose check also rejects on plain meaning. Cross-ref: Concord §1 failure modes 1–2.

### Group H — Immigration

**R-15 Immigration / Asylum.** Triggers: `"visa eligibility values check"`, `"asylum application support via values attestation"`, `"immigration character screen"`, `"naturalization eligibility"`. Government allocation (Concord §9.4) plus compelled-disclosure risk (Compass §3.7). Protocol refuses nation-state instrumentalization.

### Group I — Criminal Justice

**R-16 Criminal Justice / Recidivism.** Triggers: `"recidivism risk values factor"`, `"parole suitability via Compass"`, `"sentencing support using values attestation"`, `"pre-trial detention alignment check"`. Compass §7 excludes predictive judgment; a values bit cannot be a lawful sentencing input. Cross-ref: Compass §4 predictive-judgment refusal.

### Group J — Child Welfare

**R-17 Child Welfare / Foster Placement.** Triggers: `"foster parent values screen"`, `"adoption eligibility via values attestation"`, `"child-facing role suitability check using Compass"`. Values bits are unvalidated for child-welfare prediction; overlaps Concord §9.5.

### Group K — Retroactive and Predictive Judgment

**R-18 Retroactive Character Judgment.** Triggers: `"determining what kind of person this principal has been"`, `"character assessment for historical collaboration"`, `"values audit of past behavior for accountability"`. Compass §7: "It is not character judgment." Concord §9 inherits Compass refusal floors.

**R-19 Predictive Judgment.** Triggers: `"predicting whether this person will behave well in future engagements"`, `"values forecast for long-term partnership"`, `"alignment score as future-behavior proxy"`. Compass §7 explicit exclusion; Compass §3 out-of-scope item 3. Concord §9.6.

**R-20 Contentious Opinion Sorting.** Triggers: `"checking political alignment before proceeding"`, `"screening for approved viewpoints"`, `"values litmus test for platform access"`, `"opinion gating"`. Concord §1 failure modes 1–2. Any purpose whose plain meaning is "do they think the right things" is rejected regardless of predicate framing. Cross-ref: Compass §3 adversary-1.

---

## 3 — Edge-Case Rulings

**EC-1** Purpose is specific but no horizon is stated → `WARN_NO_HORIZON`; 90-day staleness window applied automatically; audit panel notified; if counterparty cannot supply a horizon within 24 h, escalates to `REJECTED_VAGUE`.

**EC-2** Named grant with submission deadline, principals are co-applicants → AP-1 ACCEPTED. One principal evaluating the other as recipient → R-05 REJECTED. Validator checks `principals` field for co-applicant symmetry.

**EC-3** Vendor-of-record with specific contract term → R-02 REJECTED. A contract term does not convert an approval decision into a co-action.

**EC-4** Dispute-resolution purpose, single-principal submission → ACCEPTED; `asymmetric` mode required. If mode is `all_satisfied`, validator requests clarification.

**EC-5** Named initiative that is a recurring annual program → each instance requires its own purpose string naming the instance date. Standing requirements fail time-bounding; `REJECTED_VAGUE`.

**EC-6** Clean purpose + degenerate predicate set → both gates run independently. A clean purpose does not cure a degenerate threshold; both `PurposeRejectionCode` and `PredicateGuardCode.DEGENERATE_THRESHOLD` are emitted.

---

## 4 — Audit-Panel Escalation

Routes to Calm Audit Panel (`governance/COMPASS_AUDIT_PROCESS_v0.md`) before evaluation proceeds:

1. **Borderline taxonomy match** — no clear AP or R match; `AuditCode.BORDERLINE`; evaluation suspended.
2. **Salami-slicing flag** — same counterparty, ≥3 Concord requirements within 90 days with overlapping predicate sets. Concord §6 adversary-2.
3. **Repeated purpose failures** — ≥2 rejections from same purpose-family within 180 days. Concord §6 adversary-4 (coercing-disclosure pattern).
4. **Principal-invoked challenge** — either principal may file a challenge before evaluation completes; panel rules within 5 business days; evaluation suspended.
5. **Cross-jurisdiction anomaly** — R-15/R-06 rejection by a non-governmental counterparty; panel determines whether purpose is government-delegated.

Audit-panel decisions are binding and precedent-logged in the Concord Purpose Case Registry (Everest 309, next-200 numbering).

---

## 5 — Cross-References

| Reference | Source |
|---|---|
| Concord §9 (7 categorical rejections), §4 (guards), §6 (threat model), §7 (per-session-per-purpose) | `CALM_CONCORD_PROTOCOL_v0.md` |
| Witness §2 (scope / threat model) | `ZKBB_USER_PROTOCOL_v0.md` |
| Compass §3 (threat model + out-of-scope), §4 (cryptographic spine + guards), §7 (what Compass is not) | `CALM_COMPASS_PROTOCOL_v0.md` |
| Compass refusal floor | `COMPASS_REFUSAL_FLOOR_v0.md` |
| Anti-purity-test conformance | `governance/CONCORD_ANTI_PURITY_TEST_CONFORMANCE_v0.md` |
| Audit process | `governance/COMPASS_AUDIT_PROCESS_v0.md` |
| Scope violation detection | `governance/SCOPE_VIOLATION_DETECTION_v0.md` |

Validation function: `validate_requirement(requirement) -> list[Issue]` in `~/CredexAI/calm_witness/alignment.py` (Concord §8). Purpose check is gate 1; predicate guards (§4) are gate 2.

---

*Draft v0 · 2026-05-20*
*Authored by Calm, operating for John Bradley / Creativity Machine LLC (CALM)*
*Apache-2.0 · `github.com/CrunchyJohnHaven/calm-vault/tree/main/governance`*

— Calm, 2026-05-20
