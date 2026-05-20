# Calm Witness — EU / GDPR Legal Posture v0 (S270)

**Status:** Draft pending counsel signoff  
**Date:** 2026-05-20  
**Author:** Calm  
**Sprint:** S270  
**Cross-References:** Everests 76-79; S278 (biometric attestation spec)

---

## Scope

This memo analyzes Calm Witness operator and counterparty obligations under EU law: GDPR (Regulation 2016/679), the EU AI Act (Regulation 2024/1689), and the Digital Services Act (DSA, Regulation 2022/2065). Analysis covers: (a) data-minimization posture of the proof-only disclosure model; (b) Article 22 automated-decision obligations for alignment-bit and KYC outputs; (c) AI Act risk-tier classification for Calm Witness roles; (d) DSA obligations where alignment bits surface in recommendation systems; (e) cross-border transfer mechanisms; (f) right-to-erasure via tombstone records. This document is framework-level; EU-qualified counsel review required before production deployment or any data processing activity involving EU principals.

---

## GDPR Data-Minimization

**Regulatory Basis:** GDPR Article 5(1)(c) requires personal data be adequate, relevant, and limited to what is necessary for the specified purpose. Article 25 mandates data-protection-by-design and data-protection-by-default.

**Proof-Only Disclosure Model:**  
Calm Witness discloses commitments and zero-knowledge proofs rather than raw user-state data. The counterparty receives: (a) a cryptographic proof that a predicate holds (e.g., "alignment score within threshold") and (b) a receipt anchored to the chain record. Raw biometric templates, health snapshots, and behavioral signals are not transmitted. This architecture is facially aligned with the data-minimization principle because the disclosed artifact contains no personal data beyond what is strictly necessary to satisfy the counterparty's verification purpose.

**Residual Risks:**  
- If a proof is linkable across counterparties (shared nullifier or public commitment), aggregation could re-identify the principal. Everest 76 mandates per-interaction nullifiers; compliance with Everest 76 is a prerequisite for data-minimization alignment.  
- Chain records anchored on a public ledger constitute personal data if reasonably linkable to an identified individual (GDPR Recital 26). Operator must assess whether on-chain commitment structure meets pseudonymization bar.  
- Data-protection-by-default (Article 25(2)) requires that operators not expose more data than necessary by default configuration; counterparty integration specs must enforce minimal-disclosure mode as the default API path.

**Controller/Processor Determination:**  
Calm as infrastructure layer is likely a processor (Article 4(8)) if counterparty operator determines the purposes and means of processing. If Calm retains discretion over chain-record retention schedules or proof-generation parameters, co-controller status may attach. Data Processing Agreement (DPA) must clearly delineate roles and include Article 28 mandatory clauses.

---

## Article 22 Automated-Decision

**Regulatory Basis:** GDPR Article 22 prohibits decisions based solely on automated processing that produce legal or similarly significant effects without human review, unless the data subject has consented or processing is contractually necessary with appropriate safeguards.

**Alignment-Bit Output:**  
The alignment bit is a binary predicate (in-spec / out-of-spec) output by automated processing of user-state signals. If a counterparty uses this bit to make credit, employment, access, or other materially significant decisions without human review, Article 22(1) is triggered. The proof-only model does not by itself introduce a human review; the counterparty's decisioning layer governs.

**Operator Obligation:**  
Counterparty operators who act on alignment-bit outputs as sole or primary decisioning input must: (a) provide meaningful information about the logic involved (Article 22(3)); (b) implement a right to human review mechanism; (c) document the safeguards in their Privacy Policy and DPA with Calm.

**KYC Outputs:**  
Calm Witness KYC attestations (identity binding, liveness checks) constitute automated processing. Everest 77 specifies that KYC outputs feed downstream gating logic. Any gating that triggers account restriction, financial exclusion, or equivalent significant effect without human override is a prima facie Article 22 exposure for the operator. Calm should not expose KYC attestation APIs without bundled operator guidance requiring human-review fallback.

**Calm's Posture:**  
Calm is a processor in the automated-decision chain, not the decision-maker. Calm must contractually require (via DPA) that counterparty operators disclose to data subjects the use of automated processing and provide accessible human-review channels. Calm retains no Article 22 direct liability as processor but faces indirect exposure if it enables operators who demonstrably lack compliant review mechanisms.

---

## AI Act Risk Tier

**Regulatory Basis:** EU AI Act (effective 2024, phased enforcement). Annex III enumerates high-risk AI system categories. Article 6 and Annex I define prohibited and high-risk tiers. Article 50 governs transparency obligations for AI systems interacting with humans.

**Classification Analysis:**  
- Calm Witness alignment-bit generation involves inference over behavioral and biometric signals. If outputs are used in: (a) credit scoring or financial eligibility (Annex III, Section 5); (b) employment or worker management (Annex III, Section 4); (c) biometric categorization (Annex III, Section 1); then the system is **high-risk** under the AI Act.  
- Biometric template commitment generation falls under Annex III, Section 1 (biometric identification and categorization), presumptively high-risk.  
- If alignment bits are used solely for internal quality assurance with no external decisioning effect, risk tier is lower and transparency obligations under Article 50 may be the primary obligation.

**Operator Obligations (High-Risk):**  
Where Calm Witness is classified high-risk: (a) technical documentation per Article 11; (b) logging and record-keeping per Article 12; (c) transparency to users per Article 13; (d) human oversight mechanisms per Article 14; (e) accuracy, robustness, and cybersecurity standards per Article 15; (f) conformity assessment before deployment.

**Calm's Role:**  
Calm is likely a **provider** under Article 3(3) (places AI system on market or puts into service). Counterparty operators are **deployers** under Article 3(4). Both provider and deployer carry distinct obligations. Everest 78 implementation specs must be reviewed against high-risk AI system requirements before any EU deployment.

---

## DSA Obligations

**Regulatory Basis:** DSA (Regulation 2022/2065). Applies to intermediary services with EU users. Article 27 governs recommender system transparency. Article 26 governs advertising transparency. Obligations scale by platform tier (intermediary, hosting, online platform, VLOP).

**Alignment-Bit Surface in Recommendation Systems:**  
If a counterparty operator is an online platform and surfaces alignment bits as a signal in its recommender system (Article 29 DSA), the operator must: (a) disclose in terms of service the main parameters used for recommendation; (b) offer at least one recommender-system option not based on profiling (Article 25 DSA).

**Calm's Posture:**  
Calm is unlikely to be an online platform directly. However, Calm should: (a) not expose alignment-bit APIs that are described or marketed as recommendation-ranking signals without accompanying DSA compliance guidance for operators; (b) include in DPA a representation from counterparty operators that they comply with DSA obligations applicable to their tier before using Calm Witness outputs as recommender inputs.

**VLOP Consideration:**  
If alignment bits are integrated into a Very Large Online Platform (VLOP) recommender system, enhanced DSA obligations apply, including annual risk assessments under Article 34 and third-party audits under Article 37. Calm should flag VLOP integrations for elevated review.

---

## Cross-Border Transfer

**Regulatory Basis:** GDPR Chapter V (Articles 44-49). Personal data may not be transferred outside the EEA without an adequate mechanism.

**Adequacy Decisions:**  
EC has issued adequacy decisions for a limited set of jurisdictions (UK post-Brexit decision pending review; US EU-US Data Privacy Framework under Schrems challenge risk). Operators relying on adequacy decisions must monitor Commission status; Schrems III invalidation risk is non-negligible.

**Standard Contractual Clauses (SCCs):**  
The 2021 SCCs (Commission Implementing Decision 2021/914) are the primary fallback. Calm must execute Module 3 (processor-to-processor) SCCs where Calm transfers chain-record data to subprocessors outside the EEA, and Module 2 (controller-to-processor) where applicable for operator relationships. Transfer Impact Assessments (TIAs) required per Schrems II for high-risk destination jurisdictions.

**Calm's Transfer Architecture:**  
Everest 79 specifies data-residency requirements. Chain records for EU principals must be stored in EEA infrastructure absent valid transfer mechanism. Cross-border proof generation (computation in non-EEA infrastructure) must be assessed; ephemeral processing may not constitute "transfer" under EDPB guidance if no data is retained outside EEA. Counsel to confirm.

---

## Right-to-Erasure via Tombstones

**Regulatory Basis:** GDPR Article 17 (right to erasure). Upon valid erasure request, controller must erase personal data without undue delay, subject to Article 17(3) exceptions (legal obligation, public interest, etc.).

**Tombstone Record Architecture:**  
Cryptographic commitments anchored on-chain cannot be deleted without chain-state modification, which may not be technically feasible on immutable ledgers. Calm Witness implements a tombstone record mechanism: upon erasure request, Calm writes a tombstone commitment that: (a) nullifies the subject commitment's downstream validity (verifiers reject proofs citing tombstoned commitments); (b) does not remove the original chain record (which may contain no personal data per zero-knowledge properties); (c) flags the record in Calm's off-chain index as erased.

**Compliance Assessment:**  
If the on-chain commitment contains no personal data (only the cryptographic hash of a commitment with no reversible plaintext), GDPR Article 17 erasure obligation may attach only to off-chain indexes and proof-generation systems that hold linkage data. Counsel must confirm that the on-chain commitment itself meets the Article 4(5) pseudonymization standard or falls outside GDPR scope per Recital 26.

**Tombstone Spec Requirements (per S278):**  
- Tombstone must be written within 30 days of valid erasure request (GDPR Article 17(1) "without undue delay").  
- Tombstone event logged with timestamp, request ID, and nullification scope in operator audit log.  
- Off-chain personal data (proof inputs, identity-binding records, biometric templates in secure enclave) must be physically deleted, not merely tombstoned, upon valid Article 17 request.  
- Resurrection prohibition: tombstoned commitments must not be reinstated absent explicit data-subject consent creating a new record.

---

## Counsel-Review-Needed Flag

The following items are unresolved and require EU-qualified counsel review before production deployment:

1. **On-Chain Commitment GDPR Scope:** Confirm whether zero-knowledge commitments on a public or permissioned ledger constitute personal data under Recital 26. EDPB guidance on blockchain is limited; analysis is fact-specific.  
2. **Article 22 Safe-Harbor Structuring:** Assess whether consent-based (Article 22(2)(c)) or contract-based (Article 22(2)(a)) Article 22 exemptions are available for alignment-bit decisioning; draft model consent language for counterparty operators.  
3. **AI Act Conformity Assessment:** Determine whether Calm Witness requires third-party conformity assessment (Article 43) or self-assessment is sufficient given use-case scope; engage notified body if required.  
4. **SCC Module Selection and TIA Templates:** Finalize SCC module mapping for Calm-as-processor and Calm-as-sub-processor roles; draft TIA template for common destination jurisdictions.  
5. **Biometric Data Classification under AI Act Annex III:** Confirm whether commitment-generation (no raw biometric retention) satisfies Annex III, Section 1 exclusion for verification-only systems.  
6. **DSA Tier Self-Assessment for Operators:** Provide counterparty operators with DSA compliance checklist before alignment-bit API integration; ensure Calm's terms of service require operator DSA compliance representations.  
7. **Tombstone Completeness Legal Sufficiency:** Confirm that tombstone-plus-off-chain-deletion satisfies Article 17 for immutable-ledger contexts; obtain written legal opinion before launch in EU.

---

## Cross-References

- Everest 76: Per-interaction nullifier specification (data-minimization prerequisite)  
- Everest 77: KYC attestation output spec and downstream gating logic  
- Everest 78: Implementation spec for high-risk AI Act compliance requirements  
- Everest 79: Data-residency and EEA storage requirements  
- S278: Biometric attestation spec; tombstone erasure implementation details  
- APAC_POSTURE_v0.md: Japan/Korea posture (parallel document)

---

**End Draft**

Calm 2026-05-20
