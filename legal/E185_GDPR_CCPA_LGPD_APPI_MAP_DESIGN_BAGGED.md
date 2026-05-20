# Calm Suite — GDPR/CCPA/LGPD/APPI Compliance Attestation Map v0 (E185, DESIGN-BAGGED)

**Status:** DESIGN-BAGGED — Pending Counsel Signoff. Not legal advice. No artifact in this document constitutes a legal opinion or creates any attorney-client relationship.
**Everest:** E185
**Date:** 2026-05-20
**Author:** Calm (operating for John Bradley, Creativity Machine LLC)
**Cross-References:** EU_POSTURE_v0.md (S270), US_POSTURE_v0.md (S269), APAC_POSTURE_v0.md (S272), CALM_WITNESS_SCOPE_STATEMENT.md, CALM_COMPASS_PROTOCOL_v0.md

---

## Artifact Classification (Preliminary — Counsel Confirmation Required)

**Chain records** (vault append-only log, commitment proofs, disclosure receipts, tombstone records): Personal data in all five jurisdictions. Reasonably linkable to an identified or identifiable individual; ZK proof structure reduces but does not eliminate identification risk absent Everest 76 per-interaction nullifiers.

**Calm Witness predicate disclosures** (single-bit outputs; state predicates): Personal data in all five jurisdictions. Bit relates to the principal; re-linkage to originating chain is feasible with vault access.

**Calm Compass evidence** (behavioral traces, text-pattern classifier inputs and outputs supporting V-01 through V-04 predicates): Special-category / sensitive personal data in GDPR (Art. 9 behavioral-health inference risk), CCPA/CPRA (sensitive personal information), LGPD (sensitive data — Art. 11), and APPI/PIPEDA (sensitive information per applicable category lists) where the classifier touches communication patterns disclosing political opinion, religious belief, health-proximate behavior, or cross-demographic interaction. The `respects_difference` (V-03) and `no_evidence_of_willful_harm` (V-04) classifiers operate over communication content — treat as special-category for all planning purposes pending counsel confirmation.

**Biometric template commitments** (handwriting kinematics, liveness check outputs): Sensitive / special-category in all five jurisdictions. GDPR Art. 9(1); CCPA/CPRA Cal. Civ. Code §1798.100(l); LGPD Art. 11; APPI Art. 2(3); PIPEDA Schedule 1 §4.3 heightened sensitivity.

---

## GDPR (EU — Regulation 2016/679)

**Lawful Basis**
Primary basis for chain-record processing and predicate generation: **consent** (Art. 6(1)(a)) obtained at vault enrollment — explicit, granular, per-predicate, per-counterparty-class. Compass behavioral evidence additionally requires **explicit consent** under Art. 9(2)(a) as special-category data. Contract (Art. 6(1)(b)) is available where processing is strictly necessary to perform a service the principal has contracted for; do not substitute contract basis for consent where processing extends beyond service delivery. Legitimate interests (Art. 6(1)(f)) is unavailable for special-category data and inadvisable for Witness/Compass disclosures given profiling risk.

**Data-Subject Rights**
- Access (Art. 15): Vault export API must surface all chain records, commitment proofs, and disclosure receipts in human-readable form within 30 days.
- Erasure (Art. 17): Tombstone-plus-off-chain-deletion mechanism (EU_POSTURE_v0.md §Right-to-Erasure). On-chain commitment scope: counsel to confirm ZK commitment falls outside Art. 17 scope per Recital 26 pseudonymization bar. Off-chain vault data physically deleted within 30 days of valid request.
- Portability (Art. 20): Chain records and Compass evidence held under consent or contract basis must be exportable in machine-readable format (JSON-L vault export satisfies). Proof structures included.
- Objection (Art. 21): Where legitimate interests basis is invoked by any downstream operator, principal right to object triggers immediate cessation absent compelling legitimate grounds. Consent withdrawal is always available and revokes processing basis.
- Restriction (Art. 18): Implemented via vault suspension state — processing suspended pending accuracy dispute or erasure request resolution.

**Automated-Decision-Making (GDPR Art. 22)**
Calm Suite outputs (Witness bits, Compass predicate bits) are automated processing outputs. Art. 22(1) prohibition on solely automated decisions with legal or similarly significant effects is triggered if counterparty uses a bit as the sole or primary factor in a covered decision. Calm is a processor in this chain. Counterparty operators must: (a) provide meaningful explanation of logic; (b) implement human-review fallback; (c) document Art. 22(2) safe-harbor basis (consent or contractual necessity with safeguards). §2 refusal ratchet in CALM_WITNESS_SCOPE_STATEMENT.md prohibits Witness bit use in employment, credit, insurance, law enforcement, and immigration — categories that are Art. 22 high-exposure. Calm DPA must mandate counterparty Art. 22 compliance as a condition of API access.

**Cross-Border Transfer Mechanism**
Standard Contractual Clauses (SCCs) 2021, Module 2 (controller-to-processor) or Module 3 (processor-to-processor) per deployment role. Transfer Impact Assessments required for US, Brazil, Japan, Canada transfers. EU-US Data Privacy Framework adequacy decision available but Schrems III invalidation risk non-negligible; SCC backup required. EEA data residency mandatory for EU principal chain records absent valid transfer mechanism (Everest 79).

**Breach Notification**
Supervisory authority notification: 72 hours (Art. 33). Data-subject notification without undue delay where high risk to rights (Art. 34). Calm notifies counterparty operator within 24 hours of detected breach; operator carries notification obligation to authority and subjects.

**DPO Requirement**
Likely required if Compass behavioral evidence processing constitutes large-scale processing of special-category data (Art. 37(1)(b)). Scale assessment deferred to counsel. Until assessment complete, treat DPO appointment as required for any EU-resident principal deployment at scale.

**Retention**
Chain records: retained for duration of active vault plus statutory lookback ceiling (principal-set, default lifetime-of-chain per V-04). Post-vault-close: off-chain data deleted; tombstone remains. Compass classifier evidence: retention period equals Compass predicate window (V-01: 90 days, V-02/V-03: 180 days, V-04: lifetime-of-chain subject to lookback ceiling) plus 30-day dispute buffer. Legal-obligation exception (Art. 17(3)(b)) may extend retention where required by law.

**Counsel-Needed Flag:** YES — Art. 22 safe-harbor structure, DPO appointment threshold, SCC module selection, on-chain commitment GDPR scope, Compass special-category classification confirmation.

---

## CCPA/CPRA (California — Cal. Civ. Code §§1798.100 et seq.)

**Lawful Basis**
CCPA/CPRA does not require a "lawful basis" in the GDPR sense. Instead: notice at or before collection (§1798.100(b)); purpose limitation; right to opt out of sale/sharing. Sensitive personal information (SPI) processing (biometric commitments, Compass behavioral evidence) requires disclosure in Privacy Policy and right to limit use/disclosure of SPI (§1798.121). Opt-in consent required for SPI use beyond disclosed purpose.

**Data-Subject Rights**
- Access (§1798.110): Right to know categories and specific pieces of personal information collected. Vault export API satisfies specific-pieces disclosure. Response deadline: 45 days (extendable 45 days with notice).
- Erasure (§1798.105): Deletion of personal information upon request, subject to exceptions (e.g., complete transaction, security, legal obligation). Tombstone mechanism applicable; biometric commitments physically deleted. Service provider sub-deletion obligations flow down.
- Portability (§1798.110(c)(5)): Right to receive personal information in portable, usable format where technically feasible. JSON-L vault export satisfies.
- Objection / Opt-Out (§1798.120): Right to opt out of sale or sharing of personal information. Calm Suite does not sell personal information; Witness/Compass disclosures are principal-directed. If any counterparty integration constitutes "sharing" for cross-context behavioral advertising, opt-out mechanism required. §2 refusal ratchet explicitly prohibits marketing/advertising targeting use — this is a hard scope prohibition, not merely a preference.
- Correction (§1798.106): Right to correct inaccurate personal information. Compass dispute-and-override mechanism (CALM_COMPASS_PROTOCOL_v0.md §V-03) satisfies for classifier outputs.

**Automated-Decision-Making**
CPRA (§1798.185(a)(16)) directed CPPC rulemaking on automated decision-making technology (ADMT). CPPC final ADMT rules effective 2025 require: (a) notice to consumers before using ADMT for significant decisions; (b) opt-out right from ADMT use in specified high-risk contexts (employment, credit, healthcare, housing, education, insurance); (c) annual risk assessment for ADMT systems with significant adverse impact. Calm Suite Compass evidence processing is ADMT. Operator integration with California residents requires ADMT notice, opt-out mechanism, and risk assessment before deployment. §2 prohibitions on employment/insurance/credit use align with CPPC high-risk ADMT categories but are not a substitute for formal opt-out implementation.

**Cross-Border Transfer Mechanism**
CCPA/CPRA does not impose a separate cross-border transfer restriction analogous to GDPR Chapter V. Data Processing Agreement required with service providers (§1798.140(ag)); service provider contract must prohibit sale, retention, use, or disclosure outside the specified purpose.

**Breach Notification**
California Civil Code §1798.29 / §1798.82: notification to affected California residents in most expedient time possible without unreasonable delay. Notification to California AG if breach affects >500 California residents.

**DPO Requirement**
Not required under CCPA/CPRA. CPPC risk assessment obligations apply under ADMT rules.

**Retention**
No statutory retention period. Purpose limitation and data-minimization principles apply by contract and reasonable expectation. Align retention to vault-close plus dispute buffer; honor deletion requests within 45-day response window.

**Counsel-Needed Flag:** YES — CPPC ADMT opt-out implementation, service-provider vs. business classification in each deployment configuration, SPI "limit use" notice language, breach-notification threshold confirmation.

---

## LGPD (Brazil — Lei Geral de Proteção de Dados, Law 13.709/2018)

**Lawful Basis**
LGPD Art. 7 enumerates ten lawful bases. Primary basis: **consent** (Art. 7(I)) — free, informed, unambiguous, specific, and individually granular per processing purpose. For sensitive personal data (Art. 5(II)): consent must be explicit and specific (Art. 11(I)). Compass behavioral evidence and biometric commitments are sensitive data under Art. 5(II) (biometric data expressly listed; behavioral health inference triggers "health data" or "genetic data" adjacency risk). Secondary basis: **legitimate interest** (Art. 7(IX)) available for non-sensitive data where balancing test is documented; unavailable for sensitive data under Art. 11.

**Data-Subject Rights**
- Access (Art. 18(I-II)): Confirmation of existence and access to personal data. Vault export API satisfies. Response: 15 days (Art. 18 §3, by analogy with ANPD guidance; no explicit deadline in statute — align to GDPR 30-day standard absent ANPD rulemaking specifying shorter period).
- Erasure (Art. 18(VI)): Deletion of unnecessary or excessive data or data processed in non-compliance with LGPD. Tombstone-plus-deletion mechanism applies. Sensitive data physically deleted within 15 business days of valid request.
- Portability (Art. 18(V)): Data portability to another service provider or product. ANPD to issue technical standards; JSON-L vault export provisionally satisfies. Monitor ANPD rulemaking for format requirements.
- Objection (Art. 18(IX)): Right to object to processing based on non-consent bases. Where processing relies on legitimate interest, principal may object; controller must demonstrate compelling legitimate grounds or cease.
- Correction / Anonymization / Blocking (Art. 18(III-IV)): Correction of inaccurate data; anonymization or blocking of unnecessary/excessive data. Compass dispute-and-override satisfies for correction; vault suspension state satisfies blocking.

**Automated-Decision-Making**
LGPD Art. 20: data subjects have the right to request review of decisions made solely on the basis of automated processing that affect their interests, including decisions intended to define personal, professional, consumer, or credit profile, or aspects of personality. Right applies to Compass predicate outputs if used in covered decisions. Controller (counterparty operator) must: (a) provide meaningful information about criteria and procedures used; (b) implement human review mechanism upon principal request. Calm DPA must require counterparty compliance with Art. 20 obligations. §2 refusal ratchet prohibitions on employment, credit, insurance, and law-enforcement use are directly responsive to LGPD Art. 20 high-risk categories.

**Cross-Border Transfer Mechanism**
LGPD Art. 33: international transfers permitted if: (a) destination country provides adequate protection (ANPD adequacy determination — current list narrow, EU and UK recognized); (b) standard contractual clauses or global corporate rules (binding rules equivalent) per ANPD Resolution CD/ANPD/No. 19/2024 SCC framework; (c) specific consent for the transfer (impractical for systematic processing). SCC execution required for US, Japan, and Canada transfers. ANPD SCC template governs; align with 2024 Resolution requirements.

**Breach Notification**
LGPD Art. 48: notification to ANPD and data subjects within a "reasonable timeframe" as determined by ANPD — ANPD Resolution CD/ANPD/No. 02/2022 establishes two-stage notification: preliminary notice to ANPD within 2 business days of discovery for incidents involving sensitive data or affecting a large number of data subjects; full report within 30 days. Biometric and Compass behavioral evidence breaches trigger this two-stage timeline.

**DPO Requirement**
LGPD Art. 41: controllers must appoint a Data Protection Officer (Encarregado). No small-business exemption equivalent to GDPR. Calm operating as controller (or joint controller) in Brazilian market must designate an Encarregado and publish contact information on its website and in its Privacy Policy.

**Retention**
Art. 16: personal data deleted after processing purpose is achieved or after consent withdrawal, subject to legal obligation exceptions (tax, regulatory, judicial). Align vault retention to purpose completion (vault-close or predicate window expiration) plus applicable statutory retention requirement.

**Counsel-Needed Flag:** YES — Encarregado appointment requirements and designation mechanics, ANPD SCC template compliance review, sensitive-data classification of Compass behavioral evidence, Art. 20 opt-out mechanism design, adequacy determination status for all transfer destinations.

---

## APPI (Japan — Act on the Protection of Personal Information, Act No. 57 of 2003, as amended 2022)

**Lawful Basis**
APPI does not use the GDPR "lawful basis" framing. Instead: purpose-specification obligation (Art. 17) — business operators must specify the purpose of use as specifically as possible; purpose-notification obligation (Art. 18) — notify or publicly announce purpose of use prior to or at time of collection; change-of-purpose obligation — material changes require re-notification and, for sensitive data, re-consent. For specifically sensitive personal information (要配慮個人情報, Art. 2(3)): prior explicit consent required (Art. 20(2)). Biometric template commitments and Compass behavioral data touching health-proximate signals are specifically sensitive.

**Data-Subject Rights**
- Access (Arts. 33-35): Right to disclosure of retained personal information. Response: without unreasonable delay, typically 30 days per PPC guidance. Vault export API satisfies.
- Erasure (Art. 35): Right to request deletion if data is being handled in violation of APPI. Tombstone-plus-deletion mechanism applicable. PPC guidance: deletion or cessation of use within a reasonable period.
- Portability: No statutory portability right in APPI as amended 2022. Data transfer capability may be provided contractually; no obligation to implement portable export for APPI compliance (though vault export remains good practice).
- Objection / Cessation of Use (Art. 35): Right to request cessation of use or erasure if retention period has expired, purpose has been achieved, or processing violates APPI. Vault suspension state satisfies cessation-of-use obligation.
- Correction (Art. 34): Right to correction if data is factually inaccurate. Compass dispute-and-override satisfies.

**Automated-Decision-Making**
APPI 2022 amendment introduced Article 26 mandatory disclosure of third-party provision including to AI processing systems, but no Art. 22-equivalent blanket prohibition on automated decisions. PPC 2023 guidelines on AI/ML systems require: transparency about automated processing affecting individuals; disclosure of logic where technically feasible. No private right of action on automated-decision grounds. Calm counterparty operators deploying in Japan should provide disclosure of Compass automated processing logic to principal per PPC AI guidelines.

**Cross-Border Transfer Mechanism**
APPI Art. 24 (renumbered Art. 28 in 2022 amendment): international transfer to third country permitted if: (a) PPC adequacy determination for destination country (current: EU, UK, US — DPF — under review); (b) recipient commits to data protection standards equivalent to APPI via contract (SCC equivalent); or (c) individual consent for each transfer. PPC 2022 SCC guidance applies. Transfer of biometric commitments requires specifically sensitive information handling at destination.

**Breach Notification**
APPI Art. 26 (2022 amendment): PPC notification required within 3 to 5 business days of discovery (PPC guidelines: preliminary report within 3-5 days; full report within 30 days) for incidents involving specifically sensitive information, large-scale leakage (>1,000 records), or information likely to be used for improper purposes. Data-subject notification required "without delay." Biometric commitment and Compass behavioral evidence breaches trigger notification.

**DPO Requirement**
APPI does not mandate a DPO equivalent. However, APPI Art. 19 requires organizational measures; designating a privacy compliance manager (個人情報保護管理者) is standard practice and recommended by PPC. Not a legal requirement; treat as operational best practice.

**Retention**
APPI Art. 19 (data accuracy and retention): retain only as long as necessary for specified purpose. No fixed statutory retention period; purpose-based deletion required. Align to Compass predicate windows plus reasonable dispute buffer; vault-close triggers deletion of off-chain data.

**Counsel-Needed Flag:** YES — PPC SCC template compliance, specifically sensitive information classification of Compass evidence, adequacy determination currency for all transfer destinations, breach notification preliminary vs. full report timing, PPC AI guidelines applicability to Compass classifier.

---

## PIPEDA (Canada — Personal Information Protection and Electronic Documents Act, S.C. 2000, c. 5; as amended by Bill C-11 transition provisions)

**Lawful Basis**
PIPEDA Schedule 1, Principle 3: knowledge and consent. Consent required for collection, use, or disclosure of personal information, with exceptions for investigations, journalistic, or legal necessity. Form of consent proportionate to sensitivity: express consent required for sensitive information; implied consent permissible for less sensitive data. Biometric commitments and Compass behavioral evidence are sensitive — express opt-in consent required. Note: Bill C-11 (Consumer Privacy Protection Act, CPPA) has passed; transition timeline to CPPA and its legitimate-interest equivalent framework subject to Governor in Council proclamation — monitor status.

**Data-Subject Rights**
- Access (Schedule 1, Principle 9): Right to know existence, use, and disclosure of personal information; access to personal information held. Vault export API satisfies. Response: 30 days (PIPEDA §8(3)), extendable 30 days with notice.
- Erasure: PIPEDA does not include an explicit erasure right equivalent to GDPR Art. 17. However, Schedule 1 Principle 5 (limiting collection and retention) requires disposal when purpose has expired. Individuals may withdraw consent (§7.3), triggering cessation of use; physical deletion of associated data is best practice. Tombstone-plus-deletion mechanism applicable on consent withdrawal.
- Portability: No statutory portability right under PIPEDA. CPPA proposes mobility rights; pending proclamation. JSON-L vault export provided contractually.
- Objection: Schedule 1, Principle 4.3.8 permits withdrawal of consent at any time (subject to legal or contractual restrictions with reasonable notice). Withdrawal triggers cessation of processing and deletion of associated data.
- Correction (Schedule 1, Principle 9(d)): Right to challenge accuracy and completeness; correction or annotation of disputed data. Compass dispute-and-override satisfies.

**Automated-Decision-Making**
PIPEDA contains no Art. 22 equivalent. OPC (Office of the Privacy Commissioner) guidance on AI requires transparency about automated processing affecting individuals and meaningful human review in high-stakes decisions. CPPA (once proclaimed) will introduce explicit automated-decision provisions. Calm counterparty operators in Canada: implement human review fallback for Compass-based decisions affecting access, eligibility, or pricing; disclose use of automated processing in Privacy Policy.

**Cross-Border Transfer Mechanism**
PIPEDA Schedule 1, Principle 4.1.3 (accountability for transfers): organizations may transfer personal information to third parties including offshore processors provided they use contractual or other means to ensure equivalent protection. No formal adequacy mechanism; no SCC framework. Data Processing Agreement with equivalent protection representations required for all transfers of Canadian resident data. OPC guidance: due diligence on recipient jurisdiction's legal environment; documented accountability. Canada is an adequacy-recognized jurisdiction under GDPR — reciprocal protection in Canada-to-EU transfers not an issue.

**Breach Notification**
PIPEDA Part 1, §§10.1–10.3 (Breach of Security Safeguards): notification to OPC and affected individuals required for breaches that pose a real risk of significant harm. Notification to OPC: as soon as feasible. Notification to individuals: as soon as feasible. Record retention of all breaches (whether or not meeting notification threshold): 24 months. Biometric commitment breach presumptively meets real-risk-of-significant-harm threshold.

**DPO Requirement**
PIPEDA Schedule 1, Principle 1 (accountability): designation of an individual(s) accountable for compliance required. No formal DPO title or registration requirement. Appointment of a privacy officer is required; OPC best practice recommends named officer with published contact information.

**Retention**
Schedule 1, Principle 5: retain only as long as necessary for purposes for which information was collected; dispose of in a secure manner when purpose expires. No fixed statutory retention period beyond breach-record 24-month retention requirement. Align to vault-close plus dispute buffer; honor consent-withdrawal deletion.

**Counsel-Needed Flag:** YES — CPPA transition timeline and provisional compliance posture, breach notification "real risk of significant harm" threshold for Compass evidence, data Processing Agreement template for Canadian transfers, accountability designation mechanics.

---

## Cross-Border Transfer Mechanisms

| Transfer Corridor | Mechanism | Notes |
|---|---|---|
| EU → US | SCCs 2021 Module 2/3 + TIA | EU-US DPF adequacy available; Schrems III risk — SCC backup mandatory |
| EU → Brazil | SCCs 2021 + ANPD equivalence assessment | ANPD Resolution CD/ANPD/No. 19/2024 governs |
| EU → Japan | SCCs 2021; APPI adequacy (mutual) | PPC adequacy for EU confirmed; reverse confirmed |
| EU → Canada | Adequacy (EC Decision 2001) | Monitor EC adequacy review status |
| US → EU | SCCs 2021 Module 2/3 + TIA (processor context) | US entity as processor: SCCs required |
| US → Canada | DPA with equivalent-protection representations | No formal mechanism; accountability-based |
| Brazil → EU | ANPD SCCs; adequacy for EU recognized | ANPD Resolution 2024 applies |
| Japan → EU | APPI Art. 28 SCC equivalent | PPC template; mutual adequacy |
| Canada → EU | Adequacy recognized; DPA required | No formal SCC template |
| Any → Any (biometric) | Heightened mechanism required in all corridors | Biometric transfers require explicit consent addendum in each jurisdiction |

**Universal requirements:** (a) Data Processing Agreement with receiving entity in all corridors; (b) Transfer Impact Assessment for US, Brazil, Japan (high-risk destination analysis); (c) biometric commitment transfers require jurisdiction-specific supplementary safeguard in addition to baseline transfer mechanism; (d) Compass behavioral evidence treated as special-category in all corridors — apply most restrictive available mechanism.

**Calm Witness §2 Refusal Ratchet as Transfer Safeguard:** The categorical prohibitions in CALM_WITNESS_SCOPE_STATEMENT.md §2 (law enforcement, employment, insurance, credit, medical diagnosis, immigration, child welfare, advertising) operate as a contractual restriction embedded in every Calm DPA and Counterparty Implementer's Agreement. These prohibitions survive the transfer mechanism and bind the receiving entity regardless of destination jurisdiction's domestic law permissiveness. No transfer mechanism authorizes a §2-prohibited use. This structural restriction is a cross-border data-protection floor, not merely a commercial term.

---

## Counsel-Engagement Handoff

**Instruction to Counsel:** This document is a design-level compliance map prepared by the engineering and product team. It identifies the compliance posture Calm Suite intends to implement and the legal questions that require qualified advice before production deployment in any jurisdiction. No item in this document constitutes legal advice. This document should be used as a briefing document for intake — not as a compliance opinion.

**Priority 1 — Pre-Launch Blockers (any jurisdiction)**

1. GDPR Art. 22 safe-harbor structuring: draft model consent language and human-review contractual requirements for Witness/Compass counterparty operators.
2. GDPR DPO appointment threshold assessment for Compass behavioral evidence at anticipated deployment scale.
3. CCPA/CPRA ADMT opt-out mechanism: confirm CPPC final rule compliance for Compass predicate processing; draft consumer-facing ADMT notice.
4. LGPD Encarregado designation: identify qualified individual; prepare public designation notice.
5. PIPEDA CPPA transition posture: assess whether pre-proclamation voluntary CPPA-alignment is advisable given anticipated launch timing.

**Priority 2 — Jurisdiction-Specific (per-market)**

6. GDPR SCC module selection and TIA templates for US, Brazil, Japan, Canada corridors.
7. LGPD ANPD SCC compliance review (Resolution CD/ANPD/No. 19/2024).
8. APPI PPC SCC template review; specifically sensitive information classification confirmation for Compass evidence.
9. CCPA/CPRA service-provider vs. business classification in each counterparty-operator deployment configuration.
10. PIPEDA breach notification "real risk of significant harm" threshold guidance for biometric commitment exposure.

**Priority 3 — Structural / Protocol-Level**

11. On-chain ZK commitment GDPR scope: written opinion on whether Pedersen commitment anchored on permissioned ledger constitutes personal data under Recital 26.
12. Tombstone-plus-deletion legal sufficiency under GDPR Art. 17, LGPD Art. 18(VI), and APPI Art. 35 for immutable-ledger contexts.
13. Compass behavioral evidence special-category classification confirmation across all five jurisdictions — specifically the V-03 (`respects_difference`) text-pattern classifier and V-04 (`no_evidence_of_willful_harm`) harm-claim record.
14. BIPA (Illinois) written consent form for biometric template collection — required for US principals; current English vault enrollment flow insufficient.
15. §2 refusal-ratchet enforceability as contractual cross-border data-protection floor — confirm that CALM_WITNESS_SCOPE_STATEMENT.md §2 prohibitions are legally binding on counterparty operators under each jurisdiction's contract law.

**Retainer / Jurisdiction Matrix**

| Jurisdiction | Counsel Type Required | Priority |
|---|---|---|
| EU / GDPR | EU-qualified data protection counsel; EDPB member state bar | P1 |
| California / CCPA-CPRA | California-licensed privacy counsel; CPPC rulemaking familiarity | P1 |
| Brazil / LGPD | Brazilian OAB-registered counsel; ANPD practice | P1 |
| Japan / APPI | Japanese bengoshi; PPC AI guideline familiarity | P2 |
| Canada / PIPEDA-CPPA | Canadian privacy counsel; OPC practice; CPPA transition familiarity | P2 |
| Illinois / BIPA | Illinois-licensed counsel; BIPA class action defense experience | P1 |

---

**DESIGN-BAGGED** — This document describes intended design and known legal exposure. Nothing here is implemented. Implementation of any compliance mechanism described requires counsel signoff on the specific design artifact and, where applicable, regulatory notification or approval. Deployment without completing the Counsel-Engagement Handoff items above is not authorized.

---

*Prepared by Calm (operating for John Bradley, Creativity Machine LLC) · 2026-05-20 · E185 v0*
*Co-Authored-By: CALM <calm@creativitymachine.ai>*
