# Statement of Work — Calm Witness v0 Security Audit

**Template version**: 1.0
**Issued**: 2026-05-20

This is the SoW template. Vendors complete the bracketed sections `[…]`, redline modifications with rationale, sign, and return.

---

## 1. Parties

- **Client**: Creativity Machine LLC, on behalf of the Calm Witness operator and the Calm collective ("Calm").
- **Auditor**: `[Vendor legal entity, registered address, lead engagement manager]`.

This SoW is governed by `[Vendor]`'s master services agreement of `[date]` if one is in place; otherwise this SoW is the complete contract between the parties, governed by the laws of `[Delaware, USA / vendor's preferred jurisdiction — to be negotiated]`.

## 2. Engagement Overview

Auditor agrees to perform an independent third-party security audit of the Calm Witness protocol's v0 release. The audit's purpose is to evaluate the cryptographic soundness, implementation soundness, side-channel resistance, hash-chain integrity, and privacy-property preservation of the `calm-witness` Rust crate, its WASM/JS verifier port, and the underlying cryptographic construction.

The audit is a precondition for Calm's Everest 91 (NIST submission) and Everest 99 (first production deployment). The engagement's output — a signed public summary report — becomes a permanent reference artifact.

## 3. Scope

### 3.1 In Scope

Auditor shall evaluate, in priority order:

**(a) Cryptographic soundness**
- The verifier circuit for Calm Witness's Σ-protocol composition.
- The Pedersen commitment construction on Ristretto255, including generator selection (`g`, `h`) and the unknown-discrete-log property.
- Σ-protocol composition with Fiat-Shamir — transcript ordering, hash function choice (SHA-256 / Poseidon-friendly), domain separation.
- Threshold signature aggregation (BLS12-381 or FROST per implementation choice at code freeze).
- Chain anchoring to Sigsum — soundness of the inclusion-proof verification.
- Bulletproofs range proofs on Ristretto255 per the cryptographic construction notes.

**(b) Side-channel resistance**
- Operator-side prover: timing analysis, constant-time verification of scalar operations, memory-access patterns.
- Counterparty-side verifier: same.
- WASM/JS port: timing analysis in the browser context (limited — browser side-channels acknowledged as not fully controllable).

**(c) Implementation soundness**
- Rust `calm-witness` crate against its specification: arithmetic overflow, panic on untrusted input, buffer handling, unsafe-block review.
- WASM/JS port: input validation, type coercion, prototype pollution risks.
- `cargo audit` baseline at code-freeze tag; auditor confirms triage of any open advisories.

**(d) Hash-chain integrity**
- `user_state.jsonl` canonical-bytes computation.
- Tamper-evidence properties of the append-only hash chain.
- Genesis-block provenance handling.
- Verifier behavior on malformed or adversarial chain inputs.

**(e) Privacy property preservation**
- Properties P1–P5 from the protocol specification (provided in audit packet).
- Concrete attack-tree analysis: under what adversary model do the privacy claims hold?

### 3.2 Out of Scope

Explicitly NOT in this engagement:

- The biometric distance functions themselves (handwriting, voice transcription) — covered by Everest 40/41.
- The behavioral interpretation of predicates by the DERB — Everest 80 territory.
- The Roughtime servers' or Sigsum operators' infrastructure security.
- The principal's own device security (assumed trusted per the documented threat model).
- Post-quantum primitive choice — covered by Everest 96; the present audit covers the classical cryptographic stack only.
- The Calm Pact sister-protocol (separate engagement).
- Application-level UI/UX of any agent or counterparty client.

If during the engagement the auditor identifies issues in out-of-scope areas, these may be reported as informational findings but are not part of the scoped deliverable.

### 3.3 Code Freeze

- Calm shall publish a Git tag (`v0.X.Y-audit-frozen`) of the `calm-witness` repository at audit kickoff.
- No commits to the audit-scoped paths during the engagement window, except patches for findings the auditor has accepted as in-scope to test.
- Calm shall provide build instructions sufficient to reproduce the audited binary bit-for-bit.
- The Python reference implementation and test corpus are provided as auxiliary materials (not directly audited; provided for differential-testing context).

## 4. Deliverables

| # | Deliverable | Timing | Form |
|---|---|---|---|
| D1 | Engagement plan with named auditor team and weekly schedule | Within 5 business days of kickoff | PDF |
| D2 | Weekly status update | Each Friday during the engagement | Email or shared issue tracker |
| D3 | Preliminary findings report | ~50% mark of the audit window | PDF, marked "DRAFT — CONFIDENTIAL" |
| D4 | Final internal audit report | Within 2 weeks of audit-window end | PDF, signed |
| D5 | Public summary report (redacted) | Within 2 weeks of D4 acceptance | PDF, signed |
| D6 | Re-test of Calm-side remediations | Within 4 weeks of Calm notifying auditor of fix-complete | Per-finding written confirmation |
| D7 | Final signed public summary (post-remediation) | Within 1 week of D6 | PDF, signed, suitable for public publication |

Findings shall be classified by severity per the Responsible Disclosure Policy (file 06): Critical / High / Medium / Low / Informational. Each finding shall include: description, reproduction steps, severity assessment, recommended remediation, references.

## 5. Timeline

- **Kickoff**: `[Vendor-proposed date]`, contingent on Calm-side audit-packet checklist being green.
- **Preliminary findings (D3)**: `[Kickoff + ~50% of audit window]`.
- **Final internal report (D4)**: `[Kickoff + audit window end + 2 weeks]`.
- **Public summary (D5)**: `[D4 + 2 weeks]`.
- **Re-test (D6)**: scheduled by mutual agreement once Calm signals remediation complete; not later than `[D4 + 12 weeks]`.

Audit window length: `[6–12 weeks, vendor's proposal]`.

## 6. Payment

Total fee: USD `[bid amount, within $120K–$250K envelope]`.

Payment structure:

- **Deposit**: 25% on SoW signature.
- **Mid-engagement**: 35% on delivery of preliminary findings (D3).
- **Final**: 30% on delivery of final internal report (D4) and signed public summary (D5).
- **Re-test final**: 10% on delivery of post-remediation signed summary (D7).

Expenses (travel, lodging if onsite working sessions occur): pre-approved by Calm, invoiced at cost, capped at USD 5,000 unless extended in writing.

Invoices payable net-30 by wire or ACH to the auditor's standard banking detail. Late payment carries no penalty within net-45; beyond net-45, vendor may pause work with 5 business days' written notice.

## 7. Confidentiality

- The audit packet, the auditor's findings, and all engagement materials are confidential between the parties.
- The mutual NDA (file 05 of this packet) governs all material exchanged.
- Confidentiality survives termination of this SoW.

Auditor shall not disclose engagement existence or scope publicly until Calm publishes the public summary report (D7) or grants written permission.

Once D7 is published, auditor is free to reference the engagement in vendor marketing materials (e.g., client list, case studies) subject to Calm's reasonable review.

## 8. Responsible Disclosure

- Auditor and Calm shall comply with the Responsible Disclosure Policy (file 06 of this packet) for all findings.
- Critical findings shall be disclosed to Calm within 24 hours of discovery, regardless of normal weekly reporting cadence.
- Full findings remain confidential for a minimum of 90 days post-D4 acceptance. After 90 days, Calm reserves the right (but not the obligation) to publish the full report. Auditor consents to such publication subject to redaction review.

## 9. Intellectual Property

- **Audit findings** (the substance: bugs, vulnerabilities, recommendations, code analysis) are owned by Calm upon delivery and payment. Calm may reproduce, distribute, and publish them at its discretion subject to the responsible-disclosure window.
- **Auditor methodology** (proprietary tooling, analytical frameworks, internal templates) remains the auditor's intellectual property. Calm receives no rights to the auditor's underlying methodology beyond what is necessary to read and act on the report.
- **Public summary report (D5, D7)** — joint copyright; auditor signs and grants Calm an irrevocable, royalty-free, worldwide license to publish, reproduce, and distribute in support of the open-source release (Everest 92), NIST submission (Everest 91), and broader Calm Witness adoption work.
- **Code suggestions** from the auditor that Calm incorporates into the `calm-witness` codebase are deemed contributions under Apache 2.0 (per Everest 4 License & IP Posture). Auditor agrees to this disposition for any code-form contributions made in the course of the engagement.

## 10. Engagement Mechanics

- **Kickoff meeting**: video conference; attendees include the named auditor team, Calm engineering audit-liaison, and one DERB member.
- **Weekly status calls**: 30 minutes, video, recorded for Calm-internal use, not distributed externally.
- **Questions channel**: shared issue tracker (auditor's preferred tool or Calm's GitLab) — written, traceable, time-stamped. Off-channel discussion of substantive findings is prohibited; this preserves auditor independence.
- **Audit-liaison**: Calm names one senior engineer as full-time liaison during the engagement window. Auditor may direct all questions to liaison; liaison routes to subject-matter experts as needed.

## 11. Termination

- **For convenience**: Either party may terminate this SoW with 10 business days' written notice. Termination payment: the auditor is paid for work performed up to termination, plus 50% of the next milestone payment as a kill fee. Deliverables in progress are handed over as-is.
- **For cause** (material breach, including confidentiality breach): Non-breaching party may terminate immediately on written notice. No kill fee. Breaching party may be liable for damages per the governing law.
- **Force majeure**: Neither party is in breach for delays caused by events outside reasonable control (acts of god, war, regulatory action). Engagement may be paused; if pause exceeds 60 days, either party may terminate without kill fee.

On any termination, materials in the auditor's possession shall be returned or destroyed per the NDA's return-of-materials clause within 30 days.

## 12. Liability

- Each party's aggregate liability under this SoW is capped at the total fee paid or payable, except for breaches of confidentiality, willful misconduct, or gross negligence, which are not subject to this cap.
- Auditor disclaims warranty that audit will identify all defects. Security auditing is inherently best-effort against an evolving threat landscape; the engagement's value is the auditor's skilled effort, not a guarantee of correctness.

## 13. Insurance

Auditor maintains, at its own cost, throughout the engagement:

- Professional liability / errors-and-omissions insurance: minimum USD 2,000,000 per occurrence.
- Cyber liability insurance: minimum USD 1,000,000 per occurrence.

Certificate of insurance provided on request.

## 14. Signatures

For Calm (Creativity Machine LLC):

Name: ______________________________
Title: ______________________________
Date: ______________________________
Signature: __________________________

For Auditor:

Name: ______________________________
Title: ______________________________
Date: ______________________________
Signature: __________________________

---

— Calm, 2026-05-20
