# Calm Witness — UK Legal Posture v0 (S271)

**Status:** DRAFT — pending counsel review. Do not treat as legal advice or final compliance determination.
**Summit:** S271
**Author:** Calm
**Date:** 2026-05-20
**Cross-references:** S270 (EU Legal Posture), S272 (Cross-Border Transfer Architecture)

---

## Scope

This memo addresses the UK legal posture for Calm Witness as a distinct regulatory environment from the EU regime. Post-Brexit, the UK operates under a parallel but divergent framework: UK GDPR (as retained and amended by the Data Protection, Privacy and Electronic Communications (Amendments etc.) (EU Exit) Regulations 2019), the Data Protection Act 2018 (DPA 2018), and — uniquely — the Online Safety Act 2023 (OSA). Where EU GDPR analysis appears in S270, this document addresses UK-specific deviations and additions only. Overlap is flagged but not duplicated.

Calm Witness processes user-state attestations ("alignment bits") comprising physiological, psychological, and behavioral signals. These signals trigger sensitive-category analysis under both UK GDPR and DPA 2018 Part 2. Any operator surfacing alignment bits to end users may additionally fall within OSA regulated service categories.

---

## UK GDPR Mapping

UK GDPR mirrors EU GDPR structurally but diverges in several operative areas relevant to Calm Witness.

**Data minimization (Article 5(1)(c), UK GDPR).** Alignment bits must be limited to what is strictly necessary for the attested purpose. The tamper-proof attestation architecture (see S270) operates on hashed or cryptographically committed state snapshots rather than raw signal streams. This reduces the processed dataset to the minimal representation required to satisfy verification. Counsel should confirm whether ZK-commitment outputs constitute "personal data" under the UK GDPR definition given the ICO's evolving position on pseudonymised and anonymised data post-Brexit divergence from EDPB guidance.

**Lawful basis.** For user-initiated attestation, explicit consent under Article 6(1)(a) combined with Article 9(2)(a) (for special category data) is the primary basis. Legitimate interests (Article 6(1)(f)) may apply to operator-side processing but requires a UK-specific legitimate interests assessment (LIA) given that UK GDPR Article 6(1)(f) no longer incorporates the EDPB's layered interpretation. The ICO's own LIA guidance diverges from EDPB Opinion 06/2014.

**Purpose limitation.** Attestation outputs must not be re-used for secondary purposes (e.g., profiling, commercial targeting) absent fresh lawful basis. The bank-teller-note bit architecture is designed to produce single-purpose attestations; this design constraint should be documented in the Records of Processing Activities (ROPA).

**Accuracy and storage limitation.** User-state snapshots appended to `.calm-vault/user_state.jsonl` are time-stamped and append-only. Retention schedules must be defined. Recommend a default 24-month active retention with archival policy, subject to user deletion rights under Article 17.

---

## DPA 2018

The DPA 2018 supplements UK GDPR and governs several areas of specific relevance.

**Schedule 1 — Sensitive category conditions.** Where alignment bits include health data, mental-state indicators, or inferred biometric data, processing requires a Schedule 1 condition in addition to Article 9(2) UK GDPR. Condition 1 (explicit consent) is available; however, if Calm Witness is positioned as a health-adjacent tool, Condition 2 (health or social care purposes) may apply and requires an appropriate policy document (APD) under Schedule 1, Part 4. Counsel should assess whether current product framing triggers Condition 2 obligations.

**Schedule 2, Part 1 — Exemptions.** Research and statistical purposes exemptions under Schedule 2 may apply to aggregated alignment-bit analysis. Conditions: processing for genuine research, results not used in decisions affecting individuals, and appropriate safeguards. Confirm applicability with counsel before relying on this exemption.

**DPA 2018 Part 3 (Law enforcement).** Not currently in scope; flagged for completeness in the event that Calm Witness attestations are used in any regulatory or enforcement-adjacent context.

**APD requirement.** If Schedule 1 Conditions 1, 2, or 3 are relied upon, a documented APD must be maintained. This is a UK-specific requirement with no direct EU GDPR equivalent and is a common compliance gap. Prepare APD template before any pilot launch.

---

## Online Safety Act

The Online Safety Act 2023 creates obligations for "user-to-user services" and "search services" regulated by Ofcom. Relevant obligations trigger if any operator integrates Calm Witness alignment-bit output into a surface that qualifies as a regulated service.

**Category threshold assessment.** Operators must self-assess whether they meet Category 1 (largest platforms) or Category 2 thresholds. Calm Witness as a backend attestation layer is unlikely to itself constitute a regulated service. However, any front-end product surfacing alignment bits to users in an interactive context may qualify.

**Safety duties.** OSA Section 9 (illegal content risk assessment) and Section 10 (children's risk assessment) apply to in-scope operators. If alignment bits include age-inference signals or are surfaced to potentially underage users, heightened duties apply.

**Transparency and accountability.** OSA imposes transparency reporting obligations on Category 1 services. Calm Witness should ensure that any operator agreement includes representations regarding OSA compliance status and indemnification for OSA-related failures attributable to operator-side implementation.

**Counsel note:** OSA secondary legislation and Ofcom Codes of Practice are still being finalized as of this writing. This section requires active monitoring and refresh as codes are published.

---

## Cross-Border Transfer

UK-to-EU transfers are governed by UK adequacy regulations (the EU has granted the UK adequacy under GDPR Article 45; the UK in turn has issued adequacy regulations for EEA states). This creates a functional bridge for Calm Witness data flows between UK and EU deployments, subject to the following.

**UK adequacy finding.** The EU adequacy decision for the UK (adopted June 2021) is time-limited and subject to periodic review. Counsel should calendar the next review date and establish contingency transfer mechanisms (standard contractual clauses under UK IDTA or UK Addendum to EU SCCs) in the event adequacy lapses.

**IDTA and UK Addendum.** The ICO's International Data Transfer Agreement (IDTA) and the UK Addendum to EU SCCs are the primary contractual mechanisms for UK-to-third-country transfers. S272 should specify which mechanism governs each data-flow leg. For UK-to-US transfers, IDTA is recommended given US adequacy uncertainty.

**Onward transfer restrictions.** UK GDPR Article 44 onward transfer restrictions apply. Any processor chain must be mapped and covered by appropriate transfer mechanisms. Reference S272 for the full processor register.

---

## ICO Interactions

**Registration.** Any controller processing personal data in the UK must register with the ICO under DPA 2018 Part 4, unless exempt. Confirm registration status for each Calm Witness operating entity with UK establishment.

**DPO appointment.** UK GDPR Article 37 DPO requirements mirror EU GDPR. If Calm Witness processing is large-scale special category data, DPO appointment is mandatory. Assess scale thresholds against pilot deployment scope.

**Proactive engagement.** ICO operates a sandbox and innovation hub for novel technology deployments. Consider early engagement to pre-clear the ZK-attestation architecture given absence of directly applicable precedent. ICO sandbox participation does not confer immunity but materially reduces supervisory risk.

**Breach notification.** UK GDPR Article 33 requires notification to ICO within 72 hours of becoming aware of a personal data breach. Incident response runbooks must reference ICO as the competent authority for UK-established operations.

---

## Counsel-Review-Needed Flag

The following items require qualified legal review before any operational decision:

1. Whether ZK-commitment outputs constitute "personal data" under UK GDPR given current ICO guidance.
2. Applicable Schedule 1 DPA 2018 condition and APD template.
3. OSA regulated-service classification for any operator front-end surface.
4. Status of EU adequacy decision for UK and IDTA vs. UK Addendum selection per flow.
5. DPO appointment threshold assessment against actual processing volumes.
6. ICO sandbox engagement strategy and timing.

**This document is a placeholder memo for counsel orientation only. It does not constitute legal advice. No compliance determination should be made on the basis of this document alone.**

---

## Cross-References

- S270: EU Legal Posture v0 — primary GDPR analysis; UK deviations addressed here.
- S272: Cross-Border Transfer Architecture — processor register, IDTA/UK Addendum assignments, transfer impact assessments.

---

*Calm 2026-05-20*
