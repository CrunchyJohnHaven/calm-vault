# Calm Witness — Tombstone Process v0 (S212)

**Status:** Draft  
**Spec:** S212  
**Date:** 2026-05-20  
**Author:** CALM

---

## 1. Trigger Conditions

A predicate enters tombstone review when any one of the following is established:

1. **Governance vote.** A supermajority (>= two-thirds) of seated Review Board members (S211) passes a retirement resolution, citing a specific predicate ID and recorded harm basis.

2. **Ethics-board referral.** The Ethics Oversight Panel issues a written referral asserting that continued use of the predicate creates an unacceptable risk of harm. Referrals bypass the supermajority threshold and trigger an expedited 48-hour review window.

3. **Demonstrated FAR/FRR violation.** Empirical audit confirms that the predicate's False Acceptance Rate or False Rejection Rate exceeds the threshold specified in S125 for the applicable assurance tier, and corrective calibration has failed or is infeasible within the remediation window.

4. **S105 forbidden-category match.** Any predicate found to correlate with, encode, or operationalize a protected attribute enumerated in S105 (race, sex, religion, national origin, disability, sexual orientation, or equivalent jurisdictional categories) is automatically elevated to tombstone review without requiring a vote. Elevation is immediate upon documented finding.

Any Review Board member, external auditor with standing, or the Ethics Panel may file a trigger notice. Notices are logged to the governance ledger within one business day of receipt.

---

## 2. Tombstone Record Schema

Each retired predicate is recorded as a tombstone entry. Required fields:

```
tombstone_id        : UUID v4, globally unique
predicate_id        : canonical predicate identifier (as registered in S216 registry)
predicate_version   : semver string of the retired version
trigger_type        : ENUM { GOVERNANCE_VOTE | ETHICS_REFERRAL | FAR_FRR | S105_MATCH }
trigger_ref         : reference to originating evidence artifact (vote record, referral doc ID, audit report hash)
effective_date      : ISO 8601 date, tombstone takes effect at 00:00 UTC
public_reason       : string (see Section 3)
retirement_severity : ENUM { SOFT | HARD | PREJUDICE }  -- PREJUDICE = no new proofs permitted
signed_by           : list of Review Board member identifiers who ratified
signature_hash      : SHA-256 of canonical record bytes
ledger_entry        : pointer to immutable governance ledger block (S217)
```

`retirement_severity` for S105 matches and ethics-board referrals is always `PREJUDICE`. Governance votes may specify `SOFT` (deprecation with sunset) or `HARD` where evidence does not meet the S105 threshold.

---

## 3. Public Reason

Every tombstone record must include a `public_reason` field. The field must:

- State the harm class in plain language, without exposing claimant PII or revealing confidential audit methodology.
- Identify the trigger type and, where possible, cite the specific rule or measurement that failed.
- Be written at a level sufficient for downstream implementors to make independent remediation decisions.

Deliberately vague or redacted public reasons are invalid and will be returned to the issuing board for revision. The public reason becomes part of the tamperproof ledger entry and cannot be amended after ratification; addenda may be appended as separate ledger blocks.

---

## 4. Consumer Notification

Upon tombstone ratification:

1. The governance ledger (S217) is updated immediately.
2. The S216 predicate registry marks the predicate as `TOMBSTONED` with a link to the tombstone record.
3. A notification is broadcast to all registered consumers of the predicate via the subscription channel they declared at registration. Notification must include: `predicate_id`, `effective_date`, `tombstone_id`, and a link to the `public_reason`.
4. Consumers are given a remediation window specified in the tombstone record (minimum 7 days for `HARD`, 30 days for `SOFT`; zero days for `PREJUDICE` — rejection is immediate at `effective_date`).
5. Non-responsive consumers lose standing to submit new proof requests after the effective date.

---

## 5. Verifier Rules for New Proofs

Reference verifiers (S211) enforce the following after a tombstone's `effective_date`:

- Any proof request that references a `TOMBSTONED` predicate is **rejected** unconditionally.
- Rejection response must include: `tombstone_id`, `effective_date`, and the URI of the `public_reason`.
- Verifiers must not expose claimant data in rejection responses.
- Verifiers may not be configured to bypass tombstone checks; any verifier configuration that suppresses rejection for a tombstoned predicate is itself a governance violation subject to S211 sanctions.
- Re-labeling or re-registering a tombstoned predicate under a new identifier without Review Board clearance is prohibited and treated as predicate forgery under S211.

---

## 6. Historical-Proof Retention

Proofs issued against a predicate **before** its tombstone `effective_date` remain cryptographically verifiable. Verifiers must:

- Accept historical proof verification requests with a `proof_timestamp` predating `effective_date`.
- Annotate verification responses with a `TOMBSTONED_PREDICATE` flag, the `tombstone_id`, and the `public_reason` URI.
- Not invalidate or delete pre-tombstone proof artifacts from the audit log.

Relying parties who receive an annotated historical verification must apply their own downstream policy; the Calm Witness system makes no representation about continued fitness of the claim, only that the proof was validly issued under the predicate at the time of issuance.

Audit logs containing pre-tombstone proofs are retained per the schedule in S125 and are accessible to credentialed auditors.

---

## 7. Cross-References

| Spec | Relevance |
|------|-----------|
| S105 | Forbidden categories; automatic escalation trigger |
| S125 | FAR/FRR thresholds; audit retention schedules |
| S211 | Review Board composition, verifier sanction authority |
| S216 | Predicate registry; tombstone status flag |
| S217 | Immutable governance ledger; tamperproof block structure |

---

*Calm 2026-05-20*
