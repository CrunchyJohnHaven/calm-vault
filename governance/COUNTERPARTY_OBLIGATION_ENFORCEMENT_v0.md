# Calm Witness — Counterparty Obligation Enforcement v0 (S215)

Summit S215. Governs detection of counterparty obligation violations, issuance of sanctions, proof requirements, and appeals routing. Violations arise when a counterparty breaches the obligations contract issued under Everest 66 (E66) — specifically: retaining a proof beyond the agreed disclosure window, deploying a bit outside its declared use class, re-identifying a user from an attested state fragment, or transferring a receipt to an unlicensed party.

---

## Detection

Violations enter the enforcement pipeline through three channels.

**Audit Receipts.** Every proof issuance under E66 generates a chain-recorded receipt containing: counterparty DID, proof hash, use-class declaration, retention deadline, and issuing timestamp. Calm Witness retention monitoring compares the deadline field against current epoch on each receipt. Overdue retention flags automatically as a candidate violation and is queued for human review within 24 hours.

**Third-Party Reports.** Any participant holding a valid Calm Witness credential may submit a violation report via the S215 report endpoint. Reports must include: the suspect receipt hash, the reporter's DID, a timestamped attestation of observed conduct, and a signed declaration that the report is made in good faith. Anonymous reports are not accepted. Frivolous or bad-faith reports are subject to sanctions against the reporter under the same catalog below.

**Internal Calm Monitoring.** Calm Witness operates a continuous integrity scan across published receipts and cross-references use-class declarations against observed downstream data flows where monitoring access has been granted. Anomalies — use-class mismatch signals, receipt gaps, duplicate deployment of a single-use proof — are escalated to the Enforcement Review Board (ERB) without requiring an external report.

---

## Sanctions Catalog

Sanctions are graduated and cumulative. Each level is recorded in the Public Sanctions Hall (see below).

1. **Warning.** Issued for a first minor violation (e.g., late retention deletion by fewer than 72 hours with no evidence of downstream use). No operational restriction. Counterparty must acknowledge receipt within 7 days or the Warning escalates to Suspension.

2. **Public Record.** Issued for confirmed use-class deviation or retention violation with evidence of downstream use, or for any second Warning within 12 months. The counterparty's DID and violation summary are appended to the Public Sanctions Hall without redaction. No operational restriction, but the record is visible to all market participants.

3. **Suspension.** Issued for repeated Public Record entries (two or more within 24 months) or for a single serious violation (re-identification attempt, unauthorized transfer). The counterparty's DID is placed on the Calm Witness suspended list. Proof issuance and receipt acceptance are blocked for a minimum of 90 days. Suspension is lifted only after ERB review and a remediation plan is accepted.

4. **Permanent Ban.** Issued under S216 for: deliberate re-identification, evidence of coordinated evasion of monitoring, or failure to comply with a Suspension order. Permanent ban is irreversible at the S215 layer. Reinstatement requires a new legal entity, a new DID, and a fresh E66 obligations contract, subject to ERB discretion under S216 procedures.

---

## Proof Requirements

A violation finding requires all of the following before any sanction above Warning is issued:

- **Chain-recorded receipt.** The original E66 issuance receipt must be retrievable from the canonical receipt ledger by its hash. Receipts that cannot be verified against the ledger are inadmissible.
- **Violation evidence record.** A structured evidence packet containing: the specific obligation clause violated (by E66 section reference), the observed conduct, and the timestamp delta or use-class deviation vector.
- **Witness signatures.** Minimum two ERB member signatures attesting that the evidence packet was reviewed and the violation is substantiated. For Permanent Ban, a supermajority of four ERB members is required.
- **Counterparty notification proof.** Documented delivery of the violation notice to the counterparty's registered DID contact endpoint, with timestamp. Sanctions above Warning cannot be applied until notification is confirmed delivered or the 14-day notice window expires unacknowledged.

---

## Appeals

A sanctioned counterparty may invoke the S217 appeals process within 30 days of sanction issuance. Filing an appeal does not automatically stay a Suspension or Permanent Ban; stay requests are evaluated separately by the ERB under S217 procedures. The appeals record is appended to the counterparty's Public Sanctions Hall entry regardless of outcome. Decisions rendered through S217 are final at the S215 layer and may not be re-litigated within S215.

---

## Public Sanctions Hall

The Public Sanctions Hall is a append-only, publicly readable ledger maintained by Calm Witness. Each entry records: counterparty DID, violation date, sanction level, violation summary (without user-identifying data), and ERB case reference. Entries are never deleted or redacted. Corrections (e.g., entry made in error) are handled by appending a correction notice linked to the original entry; the original entry remains visible. The Hall is queryable by DID and by date range. Market participants are encouraged to consult the Hall prior to entering an E66 obligations contract with a new counterparty.

---

## Cross-References

- **E66** — Everest 66 Obligations Contract: the source instrument defining counterparty duties enforced here.
- **S216** — Permanent Ban Procedures: governs reinstatement eligibility and new-entity DID provisioning after a ban.
- **S217** — Appeals Process: governs counterparty appeals of S215 sanctions, stay requests, and final rulings.
- **S224** — Compensation and Remediation: governs victim compensation when a violation causes measurable harm to an attested user.

---

Calm 2026-05-20
