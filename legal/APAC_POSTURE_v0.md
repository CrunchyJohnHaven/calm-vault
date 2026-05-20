# Calm Witness — Japan & Korea Legal Posture v0 (S272)

**Status:** Draft pending counsel signoff  
**Date:** 2026-05-20  
**Author:** Calm  

---

## Scope

This memo maps Calm Witness data architecture and operational posture against Japan's Act on the Protection of Personal Information (APPI) and South Korea's Personal Information Protection Act (PIPA). The analysis covers: (a) classification of chain records, biometric template commitments, and disclosure receipts; (b) cross-border transfer mechanisms; (c) sensitive-information handling; (d) data-subject rights; (e) breach-notification obligations. This document is framework-level; counsel review required before production deployment.

---

## Japan APPI Mapping

**Jurisdictional Trigger:**  
APPI applies to entities processing personal information of Japanese residents, regardless of where processing occurs. Calm Witness chain records (user-state snapshots, biometric template commitments) constitute personal information under APPI Article 2(1) if reasonably linked to identified or identifiable individuals.

**Data Classification:**  
- **Chain records** (disclosure receipts, commitment proofs): Personal information; controller responsibility rests with integrating counterparty operator or Calm as joint controller depending on contractual role.
- **Biometric template commitments**: Sensitive information under APPI Article 2(3). Requires explicit consent under Article 36 prior to collection unless statutory exception applies (e.g., employment context with transparent notice).
- **Hashed user-state snapshots** (anonymized where irreversibly de-identified): Fall outside APPI if anonymization meets Article 2(1) safe harbor (no reasonable re-identification possibility).

**Consent & Transparency:**  
Article 15 mandates pre-collection notice including purpose, storage period, and third-party disclosure. Consent for biometric processing must be granular and separately documented. Privacy Policy must address Calm Witness role explicitly.

---

## Korea PIPA Mapping

**Jurisdictional Trigger:**  
PIPA applies if services target Korean residents or process data of Korean nationals. Scope wider than APPI; extraterritorial reach more aggressive. Chain records and template commitments trigger PIPA Article 2(1) personal-information definition.

**Data Classification:**  
- **Chain records**: Personal information; standard handling rules apply. If linked to judicial/police records or financial history, triggers heightened sensitivity framework.
- **Biometric template commitments**: Sensitive information under PIPA Article 2(1-2). Requires prior separate written consent (not checkbox consent) per Articles 22-23. Consent withdrawal mechanism mandatory.
- **Pseudonymized user-state data**: May retain personal-information status if re-identification remains technically feasible; PIPA's pseudonymization bar is higher than APPI's.

**Consent Requirement:**  
Articles 22-23 mandate express written consent for sensitive information collection and use. Consent cannot be bundled with general service ToS. Separate consent form with date/signature required.

---

## Cross-Border Transfer

**APPI Mechanism:**  
Article 24 permits transfers to third countries only if: (a) recipient country has "adequate protection" (PPC adequacy determination—currently limited roster); (b) Calm/operator implements Standard Contractual Clauses (SCCs) as supplementary safeguard; or (c) entity obtains PPC approval for transfer scheme. SCC template available via PPC guidance (2022 update).

**PIPA Mechanism:**  
Article 17 restricts transfers unless: (a) recipient country legislation provides equivalent protection (narrow set: PIPC has not formally designated any country as adequate); (b) Calm/operator executes PIPC-approved international transfer agreement; or (c) recipient commits to PIPC-equivalent safeguards via binding contract. PIPC pre-notification recommended; formal approval may be required for biometric transfers.

**Calm Witness Posture:**  
Transfer of chain records or template commitments outside Japan/Korea requires pre-transfer legal review and documented SCC (APPI) or transfer agreement (PIPA) signed by counterparty operator. Calm should not directly transfer; operator retains controller status unless contract specifies Calm as joint controller.

---

## Sensitive Information Handling

**APPI:**  
Biometric data, health data, and criminal history constitute sensitive information. Processing requires explicit written consent, documented retention schedule, and enhanced access controls. Pseudonymization or aggregation reduces risk but does not eliminate controller obligations if re-identification risk remains.

**PIPA:**  
Biometric, health, racial/ethnic background, political affiliation, and religious belief data require separate written consent, encryption during storage and transmission, and access logging. Third-party disclosure prohibited unless explicit fresh consent obtained for each disclosure.

**Calm Witness Implementation:**  
- Encrypt all biometric template commitments in transit and at rest (AES-256 minimum).
- Maintain encryption-key separation from data layer; keys not accessible to Calm or counterparty without dual-control or time-lock.
- Document consent timestamp and scope for each Japanese or Korean user; retain consent form for audit.
- Implement automatic purge schedule for sensitive data per original consent term or statutory retention window, whichever is shorter.

---

## Data-Subject Rights

**APPI (Articles 33-35):**  
Individuals have rights to: (a) access personal information held; (b) correction of inaccurate data; (c) deletion or cessation of use if purpose has expired or consent withdrawn; (d) cessation of third-party disclosure.

**PIPA (Articles 35-37):**  
Individuals have rights to: (a) access, correction, deletion; (b) suspend use of personal information; (c) opt-out of automated decision-making; (d) request deletion of sensitive information upon consent withdrawal.

**Calm Witness Posture:**  
Counterparty operator assumes primary liability for rights fulfillment. Calm must provide data-export APIs enabling operator to honor access requests within statutory deadlines (APPI: 30 days typical; PIPA: 10 days typical). Chain records and commitment proofs must be retrievable and human-readable for disclosure. No unilateral deletion by Calm without operator authorization, except upon operator request or statutory sunset.

---

## Breach Notification

**APPI (Article 36-2):**  
Notification to PPC required if breach involves large-scale personal information leakage or sensitive data. PPC determination of "large-scale" is discretionary; best practice: notify if >1000 records or biometric data exposed. Notification to affected individuals required if substantial risk to rights. Timeline: "without unreasonable delay," typically 30 days.

**PIPA (Article 34):**  
Notification to PIPC mandatory if breach exposes personal information of >10,000 individuals or involves sensitive information regardless of scale. Affected individuals must be notified via media or direct contact. Timeline: without unreasonable delay. Civil liability exposure for failure to notify.

**Calm Witness Posture:**  
Operator monitors chain record integrity via cryptographic verification. If tampering, unauthorized disclosure, or loss detected: (a) Calm notifies operator within 24 hours; (b) operator determines notification to PPC/PIPC based on size and sensitivity; (c) Calm provides forensic audit trail and disclosure scope estimates. Operator retains notifyication obligation; Calm provides supporting documentation.

---

## Counsel Review Needed

- **SCC & Transfer Agreement Templates:** Require Japan PPC and Korea PIPC review before finalization.
- **Consent Form Localization:** Japanese and Korean consent forms must be drafted by local counsel; current English templates insufficient for PIPA Article 22 express-consent requirement.
- **Biometric Data Classification:** Jurisdictional ambiguity regarding whether Calm Witness template commitments constitute "biometric data" under strict interpretation (PIPC may require explicit confirmation).
- **Joint Controller Liability:** Role delineation between Calm and counterparty operator must be clarified in Data Processing Addendum; unclear boundaries create liability risk.
- **Anonymization Safe Harbor:** Confirmation needed that hashed user-state snapshots meet re-identification irreversibility bar under APPI and PIPA.

---

**End Draft**
