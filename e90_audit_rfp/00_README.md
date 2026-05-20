# Calm Witness — Third-Party Security Audit RFP Packet

*Everest 90 deliverable. Issued by the Calm Witness operator on behalf of the Calm collective.*

This directory contains the complete Request for Proposals (RFP) packet for the Calm Witness v0 third-party security audit. It is intended for two audiences:

1. **External vendors** evaluating whether to bid on the engagement (files 01, 02, 06, 07).
2. **Calm contributors and the DERB** running the procurement process (files 00, 03, 04, 05, 07).

The packet is staged and finalized before invitations go out. Once finalized, files 01, 02, 05, 06 are transmitted to candidate vendors over an encrypted channel; files 00, 03, 04, 07 are internal-only.

---

## Index

| # | File | Audience | Purpose |
|---|------|----------|---------|
| 00 | `00_README.md` | Internal | This index. Procurement overview. |
| 01 | `01_RFP_COVER_LETTER.md` | External | Cover letter inviting bids. |
| 02 | `02_STATEMENT_OF_WORK_TEMPLATE.md` | External | Draft SoW; vendor edits and returns. |
| 03 | `03_VENDOR_LIST.md` | Internal | Ranked candidate list with rationale. |
| 04 | `04_AUDIT_PACKET_CHECKLIST.md` | Internal | Pre-kickoff readiness checklist. |
| 05 | `05_NDA_TEMPLATE.md` | External | Mutual NDA covering proposal phase. |
| 06 | `06_RESPONSIBLE_DISCLOSURE_POLICY.md` | External | Disclosure policy auditors must accept. |
| 07 | `07_PROPOSAL_EVALUATION_RUBRIC.md` | Internal | Scoring rubric for incoming proposals. |

---

## Engagement Summary

- **Protocol audited**: `calm-witness` (open-source autonomous-agent user-state attestation under Apache 2.0)
- **Audit scope**: Rust reference crate, WASM/JS verifier port, cryptographic construction
- **Budget envelope**: USD 120,000 – 250,000 (vendor fee); total session budget ~USD 250,000 with buffer
- **Engagement window**: 6–12 weeks audit + 4–6 weeks preparation
- **Target audit kickoff**: ~6 weeks after vendor signature on SoW
- **Target public-summary publication**: 2–4 weeks after final report

## Vendor-Selection Process

1. **Long-list distribution (week 0)** — Cover letter (file 01) + SoW template (file 02) + NDA (file 05) + responsible-disclosure policy (file 06) sent to the six candidate vendors in `03_VENDOR_LIST.md`.
2. **NDA execution (week 1)** — Mutual NDA signed before audit-packet detail is shared. Vendors who decline the NDA exit the process.
3. **Audit-packet preview (week 1–2)** — Under NDA, vendors receive the audit-packet preview (per `04_AUDIT_PACKET_CHECKLIST.md`) so they can size the work. Full packet is delivered only at kickoff.
4. **Bid submission (week 3)** — Vendors return: signed SoW with their pricing and timeline, team CVs, three references for similar prior audits, and a statement of independence from Calm contributors.
5. **Evaluation (week 4)** — Selection committee scores bids using `07_PROPOSAL_EVALUATION_RUBRIC.md`.
6. **Selection and signature (week 5)** — Top-ranked bid is selected; SoW countersigned; deposit released.
7. **Kickoff (week 6–8)** — After Calm's audit-packet checklist (file 04) is fully green, kickoff occurs.

## Decision Criteria (summary)

The full rubric is in `07_PROPOSAL_EVALUATION_RUBRIC.md`. The five weighted axes are:

- **Public track record** (40%) — Published audits of similar-shape cryptographic protocol work.
- **Primitive expertise** (25%) — Demonstrated familiarity with Bulletproofs, Pedersen commitments, BLS/FROST, Σ-protocols, Fiat-Shamir.
- **Capacity for window** (15%) — Ability to staff a 6–12 week engagement in the requested timeframe.
- **Cost** (10%) — Within envelope.
- **Willingness to publish public summary** (10%) — Vendor will sign and publish a redacted summary report.

**Tie-breaker**: Independence from Calm contributors and Everest 80 DERB members.

## Timeline (calendar)

| Phase | Calendar weeks | Deliverable |
|---|---|---|
| RFP issuance | Week 0 | Packet sent to six candidates |
| NDA + bid window | Weeks 1–3 | Proposals received |
| Evaluation + signature | Weeks 4–5 | Vendor selected, SoW signed |
| Calm-side prep | Weeks 5–8 | Audit packet finalized per file 04 |
| Audit engagement | Weeks 9–20 (6–12 wk) | Preliminary findings + final report |
| Remediation | Weeks 21–25 | Bug fixes; auditor re-test |
| Public summary | Weeks 26–27 | Signed public summary published |

Total elapsed: 26–27 weeks from RFP to public report.

## Coordination with Other Everests

- **Everest 80 (DERB)** — DERB member on selection committee. DERB reviews remediation completeness before public summary publication.
- **Everest 91 (NIST submission)** — Audit report attached as submission-credibility artifact. NIST submission cannot proceed until audit complete.
- **Everest 92 (Open-source release)** — Public summary published alongside the release.
- **Everest 99 (First production deployment)** — No real principal state is recorded before Critical/High findings are remediated.
- **Everest 100 (Third-party verification)** — Independent verifiers cite the audit report as foundation.

## Procurement Owner

- **Procurement owner**: Calm operations (Creativity Machine LLC member-manager)
- **Technical liaison**: Designated senior engineer (named at SoW signature)
- **DERB liaison**: Named at SoW signature

Send vendor questions during the bid window to the procurement owner. Do not contact engineering directly during the bid window; this preserves auditor independence and avoids prejudicing the bid.

---

— Calm, 2026-05-20
