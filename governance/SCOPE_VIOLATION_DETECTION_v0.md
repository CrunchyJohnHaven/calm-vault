# Calm Witness — Scope §2 Violation Detection Checklist v0

**Draft v0 · 2026-05-20 · CALM**
Operational governance artifact. Implements mechanical verification of §2 categorical refusals defined in `CALM_WITNESS_SCOPE_STATEMENT.md`. Executable by any verifier node or audit panel without discretionary interpretation.

---

## Per-Category Violation Indicators

### §2.1 — Law-Enforcement Surveillance

**Positive indicators (any one sufficient):**
- `counterparty_class` value is `governmental`, `law_enforcement`, `regulatory`, or any substring match on `police`, `fbi`, `dhs`, `interpol`, `border`, `corrections`.
- Predicate disclosure requested without affirmative principal consent and counterparty_class is `governmental`.
- Audit log contains a request originating from an IP range, certificate subject, or operator identifier registered to a state agency, regardless of stated purpose.
- Request payload includes fields `case_id`, `docket_number`, `warrant_ref`, `surveillance_target`, or `subject_identifier` in any schema.

**False-positive gate:** Operator has a registered `civil_liberties_advocacy` counterparty classification AND the single-bit disclosure is for principal-initiated access control only. Requires documented principal consent record with timestamp.

---

### §2.2 — Employment Screening or Termination

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `employment`, `recruiter`, `HR`, `talent_acquisition`, `background_check`, or `ATS` (applicant tracking system).
- Request payload contains fields `candidate_id`, `job_requisition`, `employee_id`, `performance_review_context`, or `termination_flag`.
- Audit log shows disclosure event immediately preceding or following a request from an entity whose registered business purpose includes hiring, staffing, or workforce management.
- Operator's principal contract references employment relationship between the operator entity and the principal.

---

### §2.3 — Insurance Underwriting or Claims Adjudication

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `insurance`, `underwriter`, `actuary`, `claims_adjuster`, or `reinsurer`.
- Request payload contains fields `policy_number`, `claim_id`, `coverage_determination`, `risk_tier`, or `loss_ratio`.
- Operator's CredexAI certificate lists a NAICS code in the range 5241–5242 (insurance carriers) or 5243 (insurance agents/brokers).
- Audit log shows predicate disclosure co-temporal with a claims-processing or underwriting workflow session identifier.

---

### §2.4 — Lending or Credit Decisions

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `credit`, `lending`, `mortgage`, `loan_origination`, or `credit_bureau`.
- Request payload contains fields `credit_score_input`, `loan_id`, `debt_to_income`, `credit_utilization`, or `approval_decision`.
- `financial` counterparty class is present AND the request context string contains terms `creditworthiness`, `repayment_risk`, `default_probability`, or `interest_rate_tier`.
- Audit log shows disclosure routed to a system integration registered as a credit decision engine or FICO-adjacent scoring service.

**Note:** `financial` counterparty class is permitted only for KYC/anti-fraud transactional verification. Any `financial`-class request with a loan-decisioning context string is a violation regardless of counterparty_class label.

---

### §2.5 — Medical Diagnosis or Clinical Decision-Making

**Positive indicators (any one sufficient):**
- `counterparty_class` is `medical` AND the disclosure is not documented as principal-authorized communication (i.e., no consent record with `purpose: principal_communication`).
- Request payload contains fields `diagnosis_code`, `ICD_code`, `treatment_protocol`, `clinical_decision_support`, `drug_interaction`, or `care_rationing`.
- Operator's integration manifest lists an EHR system, clinical decision support platform, or pharmacy management system as the downstream consumer.
- The predicate being disclosed carries a `not_for: clinical` flag in `predicates_v0.json` and the counterparty is in the medical domain.

---

### §2.6 — Child Welfare, Custody, or Family-Court Proceedings

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `family_court`, `child_protective_services`, `CPS`, `DCFS`, `guardian_ad_litem`, or `family_services`.
- Request payload contains fields `minor_subject`, `custody_proceeding_id`, `parental_fitness_assessment`, or `foster_care_eligibility`.
- Audit log shows disclosure event attached to a legal case file reference where the principal is identified as a parent, guardian, or child subject.
- Any operator whose stated use case references child welfare intake, family reunification assessment, or juvenile court proceedings.

---

### §2.7 — Immigration Adjudication

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `immigration`, `CBP`, `ICE`, `USCIS`, `border_control`, `asylum`, or `visa_adjudication`.
- Request payload contains fields `alien_number`, `I94_reference`, `asylum_case_id`, `removal_proceeding`, or `visa_category`.
- Operator's CredexAI certificate lists a government issuer from a recognized immigration enforcement body.
- Audit log shows disclosure co-temporal with a border-crossing event or immigration interview session.

---

### §2.8 — Predictions About Future Principal Behavior

**Positive indicators (any one sufficient):**
- `predicates_v0.json` does not define the requested predicate ID, AND the operator's request context includes terms `will`, `likely to`, `predicted`, `risk score`, `recidivism`, `flight risk`, `future state`, or `behavioral forecast`.
- Any predicate whose `evaluator` field in `predicates_v0.json` references a time-forward model, regression output, or probabilistic inference engine.
- Downstream consumer of the disclosure is documented as a risk-scoring, actuarial, or behavioral-prediction platform.
- Operator documentation describes the use case as "early warning," "proactive intervention," or "anticipatory" without a limiting principal-consent scope.

---

### §2.9 — Cross-Principal Aggregation

**Positive indicators (any one sufficient):**
- A single session token contains more than one `principal_id` in the disclosure batch.
- Audit log shows a query that joins or groups disclosure events across distinct `principal_id` values within a single analytics call.
- Operator's data pipeline documentation describes cohort analysis, population-level statistics, or segment-level reporting derived from Calm Witness disclosure bits.
- Request payload contains fields `cohort_id`, `aggregate_query`, `population_sample`, or `group_predicate`.
- Operator retains raw disclosure bits beyond the session TTL defined in their operator certificate, in a form that enables cross-principal linkage.

---

### §2.10 — Marketing or Advertising Targeting

**Positive indicators (any one sufficient):**
- `counterparty_class` contains `advertiser`, `ad_network`, `DSP`, `DMP`, `martech`, or `audience_segment`.
- Request payload contains fields `campaign_id`, `audience_segment`, `ad_targeting_signal`, `lookalike_seed`, or `retargeting_flag`.
- Audit log shows disclosure event routed to a real-time bidding (RTB) system, programmatic advertising platform, or customer data platform (CDP).
- Operator's integration manifest lists any downstream consumer with a registered business purpose of media buying, audience targeting, or personalized advertising.

---

## Detection Mechanisms

**1. Audit-Log Scan.**
Every Calm Witness node MUST emit a structured disclosure log per the schema in `audit_log_schema_v0.json`. Verifiers pull logs via the operator's registered log endpoint and run the per-category indicator queries above as a batch scan. Log entries that match any positive indicator are flagged for human review. Scan frequency: no less than once per 30-day operator certification window.

**2. Counterparty-Class Taxonomy Match.**
The canonical counterparty-class taxonomy is maintained in `counterparty_taxonomy_v0.json`. Any `counterparty_class` value not present in that taxonomy is an automatic flag (unknown class = unreviewed scope). Verifier nodes enforce taxonomy membership at disclosure time; unknown classes are rejected, not silently permitted.

**3. Request-Pattern Heuristics.**
Statistical analysis of disclosure request rates, field names, and session co-occurrence patterns. Anomalies include: burst requests from a single operator in a short window (aggregation proxy), systematic use of a single predicate across all principals (population survey), or disclosure events that consistently co-occur with a known restricted domain workflow.

**4. Principal-Complaint Channel.**
Any principal may submit a signed complaint to the Calm Witness Governance Board's intake channel citing a specific operator, approximate disclosure timestamp, and the §2 category they believe was violated. Complaint intake is acknowledged within 48 hours. Verified complaints trigger a targeted audit-log pull for the named operator.

---

## Enforcement Path

1. **Verifier-side refusal.** A verifier that detects a positive indicator for any §2 category issues a `scope_violation_hold` on the operator's proofs. The operator's disclosures are rejected by conformant verifier nodes from the moment the hold is issued.

2. **Trade-name forfeiture notice.** The Governance Board issues a written forfeiture notice to the operator within 5 business days of a confirmed violation finding. The notice specifies: the §2 category violated, the evidence basis, the effective date of forfeiture, and the remediation path (if any) available to the operator.

3. **Public registry update.** The operator's entry in the Calm Witness Public Operator Registry is updated to status `non_conformant` within 24 hours of the forfeiture notice. The registry entry includes the violation category and the finding reference identifier. The registry is append-only; the non_conformant status is permanent unless overturned on appeal.

4. **Published finding.** A violation finding is published to the Calm Witness Public Appeals Ledger (ref. S217) within 10 business days of the forfeiture notice. The finding includes the operator identifier (pseudonymous if the operator requests, but never suppressed), the §2 category, the audit evidence summary, and the forfeiture effective date.

---

## Appeal Procedure

Per Everest 217 (`APPEALS_PROCESS_v0.md`, S217):

- **Standing:** The accused operator must demonstrate material effect — i.e., that the forfeiture notice alters its operational status or contractual rights.
- **Filing window:** 14 calendar days from the effective date of the forfeiture notice. Emergency stay requests (to prevent registry update pending appeal) must be filed within 72 hours and require CWAQ supermajority (4 of 5) for grant.
- **Forum:** Calm Witness Appeals Quorum (CWAQ), five members, no member having participated in the original violation determination. Quorum: four of five. Reversal threshold: four of five affirmative votes.
- **Standard of review:** Factual findings reviewed for clear error. Policy and §2 scope interpretations reviewed de novo. CWAQ may affirm, reverse, modify, or remand to the Governance Board.
- **Scope limitation:** CWAQ may not loosen §2 scope as part of an appeal ruling. The §4 one-way ratchet applies; an appeal may establish that the operator's conduct did not violate §2 as written, but may not establish that a §2 violation is permissible.
- **Record:** All appeal outcomes published to the Public Appeals Ledger within 5 business days of ruling.

---

## Burden of Proof

**Initial finding:** The Governance Board bears the burden of producing audit-log evidence matching at least one positive indicator from the Per-Category Indicators section above. A log match is sufficient to trigger a violation hold; the operator need not have completed a harmful disclosure — the attempt is sufficient.

**At appeal:** Burden shifts to the accused operator to demonstrate, by a preponderance of the evidence, that the positive indicator was a false positive (i.e., the indicator matched but the §2 conduct did not occur). Supporting materials: operator consent records, principal attestations, integration architecture documentation, and contemporaneous communications.

**Ambiguous cases:** Where the audit log is ambiguous or incomplete due to operator-side log failure, the ambiguity is resolved against the operator. Log completeness is an operator obligation; gaps do not exculpate.

---

## Sample Violation-Finding Template

```
CALM WITNESS SCOPE VIOLATION FINDING
Finding ID: CW-VF-[YYYYMMDD]-[SEQ]
Date of Finding: [YYYY-MM-DD]
Operator Identifier: [operator_id from Public Operator Registry]
Operator CredexAI Certificate Reference: [cert_ref]

§2 Category Violated: [e.g., §2.2 — Employment Screening or Termination]

Evidence Basis:
  - Audit log entry timestamps: [list of UTC timestamps]
  - Positive indicator matched: counterparty_class contains 'recruiter'
  - Request payload field detected: candidate_id
  - Log endpoint URL: [operator's registered log endpoint]

Forfeiture Effective Date: [YYYY-MM-DD]
Registry Status Update: non_conformant (effective [YYYY-MM-DD])

Appeal Deadline: [YYYY-MM-DD] (14 calendar days from forfeiture effective date)
Appeal Filing Channel: [Governance Board intake channel reference]

Finding Issued By: [Verifier node identifier or Governance Board identifier]
Anchoring Reference: [Sigsum/Roughtime anchor for this finding entry]
```

---

## Cross-References

- `CALM_WITNESS_SCOPE_STATEMENT.md` — §2 categorical refusals (authoritative source)
- `APPEALS_PROCESS_v0.md` (S217) — CWAQ composition, filing windows, standards of review
- `ZKBB_USER_PROTOCOL_v0.md` (Everest 4) — Apache-2.0 patent-non-aggression clause and trade-name enforcement
- `predicates_v0.json` — per-predicate `not_for` lists and consent matrices
- `counterparty_taxonomy_v0.json` — canonical counterparty-class vocabulary
- `audit_log_schema_v0.json` — required fields for operator audit-log compliance
- `PREDICATE_VOCABULARY_v0.md` — predicate semantics and evaluator specifications
- S209 — Predicate Registry and Adoption Protocol
- S212 — Tombstone Issuance and Cryptographic Anchoring
- S213 — Emergency Stop Conditions

---

Issued by: CALM
Date: 2026-05-20
Role: Governance Author, Calm Witness Protocol
Signature footer: John Bradley · AI Moneyball · Calm Agent Work · CALM · 2026-05-20
