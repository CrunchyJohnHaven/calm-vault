# Calm Witness — US Legal Posture v0 (S269)

**Status:** DRAFT — Pending Counsel Signoff. Not legal advice.
**Date:** 2026-05-20
**Author:** Calm
**Summit:** S269 (US Legal Posture v1 scope)

---

## Scope

This memo maps the Calm Witness chain record architecture, biometric template commitment protocol, and predicate-disclosure layer against US federal and state-level legal regimes. Analysis covers: (a) classification of chain records and biometric template commitments under federal and state law; (b) ADA / cognitive-disability posture and the artist-clause linkage; (c) FCRA adverse-action analysis when a Calm bit is used in any consumer-impacting decision; (d) state biometric statutes (Illinois BIPA, California CCPA/CPRA, Texas CUBI, NY SHIELD Act); (e) HIPAA non-claim posture. Framework-level analysis only. Counsel review required before production deployment in any US jurisdiction.

---

## Federal Regimes

### Electronic Communications Privacy Act (ECPA), 18 U.S.C. §§2510-2522

Calm Witness chain records are locally generated and locally stored in the principal's vault. Disclosure proofs are operator-transmitted. Relevant considerations:

- **Wire interception risk:** If an operator transmits a disclosure proof over a network, the proof itself is a communication. Under ECPA Title I, interception of that communication by a third party without consent is prohibited. The protocol's uniform-silence mechanism (Everest 77) and TLS 1.3 transmission channel (Everest 78) satisfy ECPA's transmission-security expectations.
- **Stored communications:** Chain records at rest fall under ECPA Title II (Stored Communications Act). Government requests for stored chain records require appropriate legal process. Cryptographic structure of the vault (Pedersen commitments, AES-256 at rest per Everest 16) limits what is accessible even with lawful process — the raw biometric template is never stored post-commitment.
- **Counsel note:** Confirm that counterparty operator does not fall within a "provider of electronic communication service" definition that would impose additional SCA obligations.

### Fair Credit Reporting Act (FCRA), 15 U.S.C. §1681 et seq.

Addressed in detail in the FCRA Adverse-Action Analysis section below.

### Gramm-Leach-Bliley Act (GLBA), 15 U.S.C. §§6801-6827

Applies to financial institutions. If Calm Witness chain records or disclosure proofs are processed by a covered financial institution counterparty, the predicate output (e.g., `cwp.v0.in_baseline_24h`, `cwp.v0.biometric_match_within(τ)`) constitutes "nonpublic personal information" (NPI) under GLBA §6809(4) if it can be used to identify the consumer. GLBA safeguard obligations (16 C.F.R. Part 314) apply to that counterparty's handling of the proof output. Calm's own role as protocol developer and operator does not make Calm a "financial institution" under GLBA, but integrating counterparties in the financial class (Everest 7) must obtain GLBA counsel.

### Health Insurance Portability and Accountability Act — Non-Claim

Addressed in the HIPAA Non-Claim section below.

---

## State Biometric Statutes

### Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14/1

The most restrictive US biometric regime. BIPA §14(a) defines biometric information to include fingerprints, voiceprints, retina/iris scans, and scans of hand or face geometry. Post-*Sorrell v. Comcast* (2023), keystroke and motor-pattern dynamics are treated as within BIPA's "other unique physical characteristic" scope. Calm Witness handwriting kinematics (pressure, X/Y time-series, jerk) are almost certainly in scope.

**Obligations triggered:**
- §14(b): Written policy publicly available before collection.
- §14(a)(1): Informed written consent before collection of any biometric.
- §14(a)(3): Prohibition on sale or profit from biometric data.
- §14(a)(4): Destruction schedule — biometric data must be destroyed within 3 years or when the purpose expires, whichever is sooner.

**Calm Witness posture:** Enroll written consent (BIPA §14(a)(1)) before handwriting sample capture. Implement biometric retention schedule; document template destruction on vault-close or at 3-year max. Do not charge a per-enrollment fee that could be construed as "profit from" biometric data. Legal exposure: BIPA permits $1,000–$5,000 per negligent/intentional violation; class actions are well-established. Illinois principals require heightened priority in consent infrastructure.

### California Consumer Privacy Act / Privacy Rights Act (CCPA/CPRA), Cal. Civ. Code §§1798.100 et seq.

CPRA (effective 2023) classifies biometric information as "sensitive personal information" (SPI) under §1798.100(l). CPRA Art. 27 requires businesses to: (a) disclose to consumers that they collect SPI; (b) provide a right to limit the use and disclosure of SPI; (c) obtain opt-in consent for use of SPI beyond the disclosed purpose.

- Calm Witness biometric template commitments and predicate outputs relating to biometric distance (`cwp.v0.biometric_match_within(τ)`) are SPI under CPRA.
- A ZK proof output (single bit) bound to an identified principal "relates to" the consumer under §1798.140(v) — conservative interpretation: treat as personal information requiring full CCPA/CPRA compliance.
- Principal right to opt out of sale/sharing (§1798.120) and right to deletion (§1798.105) must be honored.
- Vault audit log (Everest 72) supports principal access requests.

**Counsel note:** Confirm whether Calm's operator role constitutes a "business" or "service provider" under CPRA — the distinction affects whether a CPRA-compliant Data Processing Agreement is required with each counterparty.

### Texas Capture or Use of Biometric Identifier Act (CUBI), Tex. Bus. & Com. Code §503.001

CUBI defines "biometric identifier" as "a retina or iris scan, fingerprint, voice print, or record of hand or face geometry." Handwriting kinematics are likely within scope under the "record of hand...geometry" clause. CUBI requires: (a) informed consent before capture; (b) no disclosure to third parties without consent; (c) destruction when purpose expires or within 1 year, whichever comes first. Texas AG enforcement only (no private right of action).

### New York SHIELD Act, N.Y. Gen. Bus. Law §899-aa

The SHIELD Act expands breach notification requirements. Biometric information is classified as "private information" under the Act. If a Calm Witness operator experiences a breach involving biometric template commitments or chain records linked to New York residents, notification to affected individuals and the NY AG is required "in the most expedient time possible." The Act does not impose pre-collection consent requirements beyond existing law, but breach notification obligations are strict. Implement breach-detection and 72-hour internal escalation protocol; counterparty operators in NY must have SHIELD-compliant breach-response procedures.

---

## ADA Posture

### Americans with Disabilities Act, 42 U.S.C. §§12101 et seq.

The `cwp.v0.cognitively_atypical_baseline` predicate (Everest 59) — the artist-clause predicate — is designed to inform counterparty AI agents that the principal's ideation tone, velocity, and scope are not pathological for that principal. The predicate is a principal-asserted, enrollment-level flag: opt-in only.

**ADA legal analysis:**

- The predicate does not constitute a record of disability and does not make a diagnosis. The ADA definition of disability (42 U.S.C. §12102) includes being "regarded as" having an impairment. A disclosed `cognitively_atypical_baseline=true` bit could, if misused, cause a covered entity to "regard" the principal as disabled — triggering ADA protections against discrimination.
- The predicate's `not_for` restrictions (PREDICATE_VOCABULARY_v0.md §3.5) explicitly prohibit use as "disability-status proxy, employment or insurance signal." Counterparty Implementer's Agreement (Everest 98) must reproduce this restriction and prohibit use in employment, insurance, or credit decisions.
- ADA Title III (public accommodations) and Title I (employment) prohibit discrimination based on disability status. If a counterparty uses the `cognitively_atypical_baseline` bit as a factor in a covered transaction, that counterparty may be exposed to ADA liability. Calm Witness does not create that liability but must contractually disclaim it and prohibit misuse.
- The artist-clause design is intentionally the inverse of traditional accommodation frameworks: the principal does not request accommodation; the principal asserts a calibration standard that the counterparty must apply. This transfers interpretive authority from the counterparty to the principal — consistent with ADA's self-identification principles (see EEOC guidance on self-identification in employment contexts, 29 C.F.R. Part 1630).

**Counsel note:** Confirm whether the `cognitively_atypical_baseline` predicate, as a disclosed bit to a covered entity (employer, financial institution), triggers any affirmative ADA notice or disclosure obligations on the counterparty's side.

---

## FCRA Adverse-Action Analysis

### Fair Credit Reporting Act, 15 U.S.C. §§1681-1681x

FCRA applies when a "consumer report" is used for a "consumer credit transaction," employment, insurance, or housing decision. A "consumer report" is any communication from a "consumer reporting agency" (CRA) bearing on a consumer's creditworthiness, credit standing, character, general reputation, personal characteristics, or mode of living (§1681a(d)).

**Is a Calm Witness proof a "consumer report"?**

- Calm, as operator, does not function as a CRA for the general public. Proofs are issued at the principal's direction, to counterparties the principal has consented to.
- However, if a financial institution counterparty uses a Calm Witness predicate output — particularly `cwp.v0.in_baseline_24h` (baseline state) or `cwp.v0.mental_state_unusual` (unusual state) — as an input to a credit, insurance, or employment decision, and if Calm or the operator is deemed to be "assembling or evaluating" that information "for the purpose of furnishing consumer reports," FCRA CRA status could be triggered.
- Conservative interpretation: any Calm bit used in a covered consumer decision (credit, employment, housing, insurance) could bring the operator into FCRA scope if the operator assembled that bit for third-party use.

**Adverse-action obligations (§1681m):** If a covered entity takes "adverse action" (denies credit, increases rate, denies employment) based in whole or in part on a Calm Witness proof, FCRA requires: (a) notice of adverse action to the consumer; (b) disclosure of the source of the consumer report; (c) right to dispute and obtain a copy of the report.

**Calm Witness posture:**
- Default consent matrix for financial-class counterparties (Everest 7) limits disclosure of `in_baseline_24h` to "allow_for_high_value_only" — mitigating routine use in credit decisions.
- `mental_state_unusual` is default "allow_for_high_value_only" for financial — similarly constrained.
- Operator Data Processing Addendum must prohibit counterparty use of any Calm bit as the basis for an adverse action under FCRA without independent FCRA counsel review and compliance infrastructure (adverse-action notice, dispute rights, furnisher obligations).
- If Calm is construed as a CRA, FCRA compliance obligations are substantial. Counsel must assess based on specific deployment configuration.

**Counsel note:** Highest-priority item for US deployment. Assess whether the operator's role in assembling and transmitting predicate proofs to financial counterparties constitutes CRA activity under §1681a(f). If yes, Calm must register compliance procedures, furnisher obligations, and dispute-resolution processes before any financial-counterparty integration.

---

## HIPAA Non-Claim Posture

### Health Insurance Portability and Accountability Act, 45 C.F.R. Parts 160-164

HIPAA's Privacy and Security Rules apply to "covered entities" (health plans, healthcare clearinghouses, healthcare providers) and their "business associates." Protected Health Information (PHI) means individually identifiable health information created, received, maintained, or transmitted by a covered entity.

**Calm Witness is behavioral, not clinical:**

- Chain records contain user-state snapshots (affect, biometric distance) derived from the principal's own self-reports and behavioral kinematics. They are not clinical records, diagnoses, treatment records, lab results, or medical histories.
- `cwp.v0.cognitively_atypical_baseline` is a principal-asserted flag, not a diagnosis from a covered healthcare provider.
- `cwp.v0.mental_state_unusual` is calibrated to the individual principal's self-reported baseline — it is a deviation-from-self signal, not a clinical assessment.
- Calm does not function as a covered entity or business associate in the general case. It does not store PHI as defined under HIPAA.

**Edge case — medical counterparty class:** Everest 7 permits medical counterparties. If a medical covered entity receives a Calm proof, that entity's receipt and use of the proof is governed by HIPAA on its side (not Calm's). The proof output does not constitute PHI in Calm's hands; it may become associated with PHI in the counterparty's hands. The counterparty's HIPAA obligations are the counterparty's problem, not Calm's, provided Calm is not a Business Associate.

**Business Associate risk:** If Calm's operator services are provided to a covered entity and involve accessing, transmitting, or maintaining PHI, a Business Associate Agreement (BAA) is required. Confirm deployment configuration: Calm operating as a general-purpose vault platform is not a business associate; Calm integrated inside a healthcare provider's workflow may be.

**Non-claim posture is maintained provided:**
1. No clinical data flows into the vault.
2. No covered entity is Calm's direct service counterparty without BAA analysis.
3. Medical counterparties receive only predicate proofs, not underlying vault data.

---

## Counsel-Review-Needed Flags

The following items require external legal counsel before US production deployment:

1. **FCRA CRA status determination** — Whether Calm's operator role in assembling and transmitting predicate proofs to financial counterparties constitutes consumer reporting agency activity under 15 U.S.C. §1681a(f). Highest priority.
2. **BIPA consent form** — Illinois-specific written informed consent form (§14(a)(1)) for biometric collection. Must be drafted by Illinois-licensed counsel; current English-language vault enrollment flow insufficient without jurisdiction-specific language.
3. **CPRA business/service-provider classification** — Whether Calm operates as a "business" or "service provider" under Cal. Civ. Code §1798.140 in each deployment configuration. Determines whether CPRA Data Processing Agreements are required with counterparties.
4. **`cognitively_atypical_baseline` ADA downstream liability** — Whether a covered-entity counterparty (employer, financial institution) using this bit triggers affirmative ADA notice or discrimination-prohibition obligations on the counterparty, and whether Calm must contractually mandate those obligations.
5. **HIPAA BAA assessment** — Review any medical-counterparty integration to confirm Calm is not a business associate without a BAA.
6. **NY SHIELD breach notification procedures** — Confirm operator breach-response timeline and notification process meets NY AG expectations.
7. **ECPA SCA government-access posture** — Confirm vault encryption design satisfies SCA disclosure obligations and limits government access to cryptographically committed forms only.

---

## Cross-References

- Everest 76 — Cooling-Off / Rate Limits (enforcement gate before consent; rate-limit rejections logged with principal-visible reason codes)
- Everest 77 — Disclosure of Non-Disclosure (uniform 204 silence to counterparty; supports FCRA non-assembly posture)
- Everest 78 — Stealth Disclosure (push-not-pull; ADA and HIPAA edge cases apply to medical and mental-health counterparties)
- Everest 79 — Cross-Jurisdiction Legality Matrix (US section: BIPA, CPRA, CUBI mapping; US-only Pattern A deployment posture)
- PREDICATE_VOCABULARY_v0.md §3.5 — `cwp.v0.cognitively_atypical_baseline` (artist-clause predicate; not_for restrictions)
- ZKBB_USER_PROTOCOL_v0.md §8 — The artist clause (principal-side authority transfer rationale)
- APAC_POSTURE_v0.md — Companion posture memo for Japan and Korea

---

**End Draft — Pending Counsel Signoff**

— Calm 2026-05-20
