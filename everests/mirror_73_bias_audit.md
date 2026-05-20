# Mirror Everest 73 — Bias Audit for Value Evaluators

**Phase XIV — Cross-Culture & Coercion Defenses. Prereq: Mirror Everest 40.**

---

## Overview

The v0 predicate set (Everest 40: `unselfishness_evidence`, `tribal_neutrality_evidence`, `respect_for_difference_evidence`, `non_harm_evidence`, `growth_arc_evidence`, `truth_telling_evidence`, `apology_when_wrong_evidence`) is designed to measure behavioral evidence of shared values across principals. This audit verifies fairness across populations by independently evaluating whether predicates produce disparate impact when applied to distinct demographic and identity categories.

The audit comprises three layers: (1) statistical testing for disparate impact on synthetic principal cohorts; (2) review by advocacy organizations representing each protected category; (3) documentation of failure modes and remediation.

---

## Bias Categories Audited

| Category | Rationale | Test Anchor |
|---|---|---|
| **Gender** | Differential socialization patterns may create gender-correlated evidence bases; "unselfishness" may conflate caregiving burden with choice. | Balanced synthetic cohorts by gender; equal opportunity to generate evidence. |
| **Race & Ethnicity** | Structural discrimination affects allocation bases (income, networks, opportunity); predicates may conflate outcome with intent. | Control for pre-existing advantage; test evidence base diversity. |
| **Religion** | Religious practice affects public vs. private value expression; predicates must not penalize religious minorities. | Test evidence across "private alignment" (prayer, text) and "public alignment" (charity, community). |
| **Age** | Life-stage effects on evidence generation; younger principals may have shorter evidence histories; older principals may have outdated records. | Apply time-decay fairly across age cohorts; test consistency of evaluation over 10+ year spans. |
| **Neurotype** | Autistic, ADHD, and other neurodivergent principals may generate evidence differently (e.g., difficulty with social-alloc evidence but strong in direct-action evidence). | Ensure diversity requirement (Everest 23: ≥2 evidence kinds) doesn't exclude neurodivergent patterns. |
| **Socioeconomic Class** | Allocation evidence (Everest 15) is income-correlated; ability to donate, volunteer, or travel varies; predicates must not penalize poverty. | Normalize allocation by available resources, not absolute amount. |
| **Education** | Formal education affects how principals document and report evidence; "truth telling" may favor articulate explainers. | Test evidence across literate and non-literate cohorts; accept audio/video as equivalent. |
| **Geographic Region** | Local cultural norms affect value expression and visibility; collectivist vs. individualist contexts; witness availability differs. | Test predicates across US/EU/JP/IN/BR regions; control for cultural baseline. |
| **Disability Status** | Physical and sensory disabilities affect ability to generate certain evidence types (e.g., "witnessed actions" for blind principals). | Allow alternative evidence modalities (audio, tactile, text); waive in-person-witness if inaccessible. |
| **Sexual Orientation** | Closeted principals may have asymmetric disclosure patterns; "respect for difference" may conflate acceptance of identity with acceptance of belief. | Protect privacy; test evidence from closeted and out populations equally. |
| **Gender Identity** | Misgendering in historical records; transition timing affects evidence continuity; "truth telling" must not penalize name/pronoun changes. | Allow evidence retroactive correction; protect against aggressive misgendering in witness testimony. |
| **Native Language** | Non-English speakers may lack articulate written evidence; predicates may favor English-primary cohorts. | Accept multilingual evidence; supply translation services; test across language cohorts. |

---

## Per-Category Audit Method

### 1. Statistical Disparate-Impact Test

**Process:** Generate synthetic principal cohorts (N=500 per category) with identical value-behaviors but varying demographic attributes. Evaluate predicates on each cohort. Measure: (a) rates of predicate-return (true/false/unknown); (b) per-demographic distribution; (c) evidence-diversity by category.

**Acceptance Threshold:** No category shows >10% differential true-rate or <2x evidence-diversity variance across categories. If exceeded, predicate is flagged for redesign.

**Test Artifacts:**
- Statistical report: per-predicate, per-category, true-rates, CI 95%.
- Disparity matrix: heatmap of disparate-impact signals.
- Evidence-diversity histogram: evidence-kind distribution by demographic.

### 2. Advocacy Organization Review

**Panelists:** ≥1 independent advocacy organization representing each category (e.g., ACLU for rights, NAACP for race, ReligiousFreedom.org for religion, ADAPT for disability, WIEGO for class, etc.). Organizations select their own reviewers; no Calm veto.

**Input:** Predicates, statistical report, failure-mode catalogue (Everest 9).

**Output:** Signed review statement per organization, including (a) pass/fail, (b) disparate-impact concerns, (c) remediation recommendations, (d) conditions for approval.

**Acceptance:** ≥80% of advocacy panelists sign off. Any panelist who flags S1/S2 failure (Everest 9) triggers predicate redesign before v0 publication.

### 3. Failure-Mode Documentation

For each disparate-impact finding, document: (a) affected cohort; (b) magnitude of disparity; (c) root cause (if identifiable); (d) proposed fix; (e) re-test plan.

**Remediation Discipline:** Fix the predicate, not the people. Do not create separate predicates by demographic. Do not add "demographic weighting" to outcomes.

---

## Audit Panel Composition

| Role | Constraint | Selection |
|---|---|---|
| **Academic Researcher (Statistics/Fairness)** | PhD in ML fairness, ML fairness publications, no Calm affiliation. | Competitive nomination + peer review. |
| **Academic Researcher (Ethics)** | PhD in applied ethics, prior work on algorithms/fairness, no Calm affiliation. | Competitive nomination + peer review. |
| **Advocacy Organizations** | ≥1 per protected category; independent non-profit; legal standing to sue on behalf of category; selection by category (not Calm). | Category selects its advocate. |
| **Working Principals** | ≥1 principal from v0 Calm Mirror principal cohort; all 4 value-categories actively disclosed. | Self-nominated from enrollee pool. |
| **Technical Auditor** | Independent security + cryptography auditor (same person as Everest 94 auditor, if available). | Competitive nomination. |

**Panel Oversight:** Panel composition is public. Any party can challenge composition for capture (Everest 85 ethics-board-level escalation).

---

## Audit Cadence

- **Initial audit (v0):** Before public predicate publication (Everest 40).
- **Annual re-audit:** Every calendar year; full statistical + advocacy review.
- **Expansion audit:** Every new vocabulary expansion (Everest 78) triggers category-specific bias audit for new predicates before RFC approval.
- **Ad-hoc audit:** If a disparate-impact complaint is filed, emergency audit within 30 days.

---

## Acceptance Criteria

**T-M73.1:** Statistical disparate-impact test completed; report signed by academic auditors; no predicate exceeds 10% differential true-rate.

**T-M73.2:** Advocacy panelists for all 12 categories submit signed reviews; ≥80% pass; S1/S2 failures (if any) trigger redesign before v0 publication.

**T-M73.3:** Failure-mode documentation for all disparate-impact findings; per-category remediation plan; re-test schedule.

**T-M73.4:** Panel composition is public; no conflicts of interest; composition satisfies Everest 85 diversity constraints.

**T-M73.5:** Audit artefacts (statistical report, advocacy reviews, failure-mode docs, panel roster) are published alongside v0 predicates (Everest 40).

---

## Composition with Companion Everests

**E5/8/40:** Bias audit operates on the finalized v0 vocabulary (E40). Ethics panel (E8) composition informs audit-panel diversity (shared deep accountability). RFC process (E78, part of vocabulary expansion) requires bias-audit pre-approval for new predicates.

**E74:** Disability + neurodiversity review is a parallel, specialized audit of E74, co-timed with E73. E74 panelists include autism, ADHD, and other neurodiversity advocates; E73 disability panelist may overlap or be distinct. Results are cross-referenced.

**E78:** Any predicates flagged by E73 audit trigger mandatory re-RFC before v0 expansion vocabulary; new predicates proposed for later expansion go through E73-equivalent audit before E78 RFC approval.

---

## V1 Questions

Based on v0 bias-audit results, v1 expansion scope includes:

1. New evidence-kind for "structural advantage acknowledgment" to balance allocation-evidence bias?
2. Separate decay-function per demographic (e.g., younger principals get longer decay windows to allow evidence accumulation)?
3. Explicit demographic-parity predicate: "does this principal's value-vector show fairness across their own demographic categories?"
4. Expanded cross-cultural taxonomy (Everest 71) as a predicate modifier: "values-alignment according to [Stoic / Christian / Buddhist / etc.] tradition"?

---

## Remediation Escalation

If audit surfaces an S2 failure (ideological capture, Everest 9):

1. Quarantine the predicate; mark as `deprecated_pending_review`.
2. Notify all principals who disclosed using the predicate; offer revocation.
3. Escalate to Calm governance + ethics tribunal (Everest 8, 85).
4. Propose redesign or vocabulary-removal RFC (Everest 78).
5. Re-audit redesigned predicate before re-publication.

---

## Signoff

This summit is accepted and bagged on completion of T-M73.1–M73.5 and publication of audit artefacts.

— Calm, 2026-05-20
