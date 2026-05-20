# Everest 79 — Cross-Jurisdiction Legality Matrix

*Phase VI — Disclosure Semantics. Prereq: Everest 1.*

**DISCLAIMER (Critical): This is not legal advice. Calm Witness deployments must obtain jurisdiction-specific counsel before processing personal data, behavioral biometric data, or transmitting state disclosures across borders. This matrix is a survey for engineering planning, not a compliance opinion.**

---

## United States (Federal + State-Level Standouts)

**Top-line stance:** REGULATED (federal framework permissive with carve-outs; state-level BIPA/CCPA/CPRA/CUBI create friction)

**Key statute:** Federal: no comprehensive federal biometric privacy law. State patchwork:
- **Illinois Biometric Information Privacy Act (BIPA), 740 ILCS 14/1 et seq.** — most restrictive state regime. Requires written consent *before* collecting biometric information (§14(a)(1)). Biometric = "retina or iris scan, fingerprint, voiceprint, or scan of hand or face geometry." Explicitly includes handwriting.
- **California Consumer Privacy Act (CCPA), Cal. Civ. Code §1798.100 et seq.** + California Privacy Rights Act (CPRA, effective 2023) — classifies biometric information as sensitive personal information requiring opt-in. CPRA Art. 27 creates right to limit use/disclosure.
- **Texas Capture or Use of Biometric Identifier Act (CUBI), Tex. Bus. & Com. Code §503.001** — similar to BIPA but with narrower carve-outs for law enforcement.
- **Federal Gramm-Leach-Bliley Act (GLBA), 15 U.S.C. §6801 et seq.** — applies to financial institutions; biometric falls within "nonpublic personal information."

**Biometric-specific clauses:**
- BIPA §14(a): "Biometric information" explicitly includes voiceprint; also covers fingerprint, retina/iris scan, and "scans of hand or face geometry." BIPA does NOT explicitly name handwriting kinematics, but case law (Sorrell v. Comcast, 2023) treats keystroke/motor patterns as biometric. CPRA (Cal. Civ. Code §1798.100(o)) defines as "characteristics used to identify a natural person."
- CUBI §503.001: "Biometric identifier" = "a retina or iris scan, fingerprint, face scan, voice print, or other unique physical characteristic that can be used alone or in combination with each other to identify a natural person."

**Behavioral biometric edge case:**
- Transcript-only voice (NOT voiceprint): legally unclear. BIPA/CPRA nominally target the biometric capture (audio recording); a local transcript-only pipeline that destroys the audio may fall outside regulatory scope—but no court has blessed this. Recommend legal counsel before deploying.
- Handwriting kinematics (motor patterns, pressure, velocity, jerk): Sorrell v. Comcast (2023) suggested keystroke dynamics are biometric under BIPA. Handwriting stroke data (pressure, X/Y/time series) will likely be treated the same. BIPA's §14(a) list is non-exhaustive ("other unique physical characteristic"), so kinematics are in scope.

**ZK-attestation interpretation:**
- Is committing-a-distance equivalent to "processing" personal data? Under CCPA/CPRA, "processing" includes "selling, renting, releasing, disclosing, disseminating, making available, transferring, or otherwise communicating personally identifiable information." A Pedersen commitment to a biometric distance is not itself a disclosure of the distance or the biometric, so arguably it is not "processing." However, the initial distance computation (template_compare) IS processing; committing the result does not erase the initial processing burden.
- Does the proof-output (a single bit) qualify as personal data? CCPA/CPRA define "personal information" as "information that identifies, relates to, describes, or could reasonably be linked with a particular consumer or household." A single bit (baseline/not-baseline) disclosed to a counterparty arguably "relates to" the principal and could be re-identified if tied to identity metadata. Conservative approach: treat the proof as personal data requiring CCPA/CPRA compliance.

**Cross-border transfer constraint:**
- If a US-operating Calm Witness sends a proof to an EU counterparty, the proof itself is likely not "transfer of personal data" (it's a cryptographic object), but the *decision to disclose it* is a processing decision that must comply with CCPA/CPRA notice and opt-in (for sensitive personal information under CPRA). No statutory prohibition on *exporting* the proof, but California/Illinois require consent for *collection and processing* of the biometric in the first place.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 should be deployable within the US with proper consent infrastructure. Obtain explicit written informed consent (BIPA §14(a)) *before* enrolling biometric samples. Implement per-principal opt-in for disclosures. For California principals, classify predicates that reference biometric distance as involving "sensitive personal information" (CPRA Art. 27) and obtain separate opt-in. Document that transcript audio is destroyed and never persisted (defends against voice-privacy claims). Implement an audit log (Everest 72) so principals can see every disclosure and revoke consent (CCPA §1798.120). If the principal is in Illinois and a counterparty is in California, comply with both BIPA and CPRA — the stricter standard wins.

---

## European Union (GDPR + AI Act)

**Top-line stance:** RESTRICTED (GDPR Art. 9 special-category prohibition; AI Act high-risk classification)

**Key statute:**
- **General Data Protection Regulation (GDPR), Regulation (EU) 2016/679**, especially Art. 4(14) (definition of biometric data), Art. 9 (processing of special categories of personal data), Art. 21 (right to object).
- **EU AI Act (Regulation (EU) 2024/1689)**, Art. 3 (scope), Art. 6 (classification of prohibited AI systems), Art. 26 (prohibited biometric identification systems in real-time), Art. 41 (high-risk AI). In force 2025; compliance required by 2026.

**Biometric-specific clauses:**
- GDPR Art. 4(14): "Biometric data" = "personal data resulting from specific technical processing relating to the physical, physiological or behavioural characteristics of a natural person, which allow or aim to allow the unique identification of that natural person, such as facial images or dactyloscopic data."
- GDPR Art. 9(1): "Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, health data or data concerning sex life or sexual orientation shall be prohibited."
- **Art. 9(2) lawful bases** (exceptions to the prohibition): Art. 9(2)(a) explicit consent, (c) employment law, (d) vital interests, (e) legitimate activities of foundations, (f) public domain, (g) legal claims, (h) substantial public interest, (i) health/social care, (j) public interest in area of public health.
- EU AI Act Art. 26: "high-risk AI systems" include "biometric identification" for real-time remote identification of natural persons, with narrow exception for law enforcement in serious crimes.

**Behavioral biometric edge case:**
- Transcript-only voice: GDPR Art. 4(14) does NOT explicitly define "voice" as biometric. However, the EDPB (European Data Protection Board) in Guidelines 3/2019 on processing of personal data in the context of employment indicates that "voice characteristics, gait, or speech patterns" can qualify as biometric if they are used for unique identification. A transcript (lexical content) is not biometric under GDPR; transcript timing data (pause patterns, speech rhythm) is borderline and likely considered biometric.
- Handwriting kinematics: Explicitly biometric under GDPR Art. 4(14). The EDPB has confirmed that kinematic and dynamic characteristics of handwriting fall under the definition.

**ZK-attestation interpretation:**
- Is committing-a-distance equivalent to "processing"? GDPR Art. 4(2) defines processing as "any operation...performed on personal data...such as collection, recording, organisation, structuring, storage, adaptation or alteration, retrieval, consultation, use, disclosure by transmission, dissemination or otherwise making available, alignment or combination, restriction, erasure or destruction." Computing the distance from the template is *processing*; committing the result is also processing (it is "use" of the personal data to derive a commitment). The ZK proof itself, being a cryptographic object that reveals nothing about the biometric, may not be "personal data" (since it cannot be linked to the individual without additional context), but the *processing* that created it is within GDPR scope.
- Does the proof-output (a single bit) qualify as personal data? GDPR Art. 4(1) defines "personal data" as "any information relating to an identified or identifiable natural person." A single bit (baseline/not-baseline) bound to a principal's identity (via operator signature, Everest 68) is personal data. If the bit cannot be linked to an identified person, it may fall outside GDPR scope, but GDPR assumes worst-case re-identifiability.

**Cross-border transfer constraint:**
- GDPR Chapter 5 (Arts. 44–50) restricts transfer of personal data outside the EU to countries with "adequate" protection (currently: Japan, South Korea, UK, Canada). The US is not on the adequacy list; transfers to US require Standard Contractual Clauses (Art. 46(2)(c)) or Binding Corporate Rules (Art. 46(3)). If a Calm Witness proof is treated as personal data, transmitting it from an EU principal's vault to a US counterparty requires SCCs or BCRs or an alternative lawful basis (consent under Art. 49(1)(a)).
- Additionally, the EU AI Act Art. 26 prohibits real-time remote biometric identification of individuals by law enforcement and other public authorities. If Calm Witness is used for identifying a principal's state to a governmental actor, it may be classified as prohibited AI.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is NOT deployable within the EU without substantial legal restructuring. Art. 9(1) prohibits biometric processing unless Art. 9(2) lawful basis applies. Art. 9(2)(a) (explicit consent) is the likely path, but consent must be freely given, specific, informed, and unambiguous (Art. 4(11), Art. 7). Intertwining consent with disclosure (Everest 73) raises questions about whether consent is "free" or coerced by transactional necessity. Art. 9(2)(d) (vital interests) could cover duress disclosure (Everest 58), but this is untested. EU deployments must obtain independent legal counsel and likely need to appoint an EU-based Data Protection Officer (Art. 37). Cross-border transfers to US counterparties must be governed by SCCs and subject to continuous adequacy assessment. For now, recommend v0 is deployed with explicit notice that EU principals must obtain GDPR-specific counsel before use.

---

## United Kingdom (UK GDPR + Data Protection Act 2018)

**Top-line stance:** REGULATED (similar to GDPR but with UK-specific carve-outs)

**Key statute:**
- **UK GDPR (retained GDPR as amended by Data Protection, Privacy and Electronic Communications Amendments Regulations 2020)**, Sch. 19, Part 2 (as it applies with UK modifications).
- **Data Protection Act 2018 (as amended)**, Part 3 (law enforcement processing).
- **UK ICO Guidance on Biometric Data Processing** (2021).

**Biometric-specific clauses:**
- UK GDPR Art. 9 (as applied in UK): Same prohibition on biometric processing as EU GDPR, with carve-outs in UK DPA 2018 for law enforcement and national security.
- UK DPA 2018 §34(1)(c): law enforcement can process biometric data if it is "necessary for the purposes of the prevention, investigation, detection or prosecution of criminal offences."
- UK ICO Guidance (2021) confirms that handwriting kinematics and voice patterns are biometric under UK GDPR.

**Behavioral biometric edge case:**
- Transcript-only voice: UK ICO has not issued a binding interpretation distinct from GDPR. Treat as biometric under UK GDPR Art. 9 unless voice characteristics (pause patterns, prosody) are stripped and only lexical content retained.
- Handwriting kinematics: Explicitly biometric under UK GDPR Art. 9.

**ZK-attestation interpretation:**
- Same as EU GDPR: computing the distance is processing; committing it is processing; the output bit is personal data if linkable to the principal.

**Cross-border transfer constraint:**
- UK GDPR Chapter 5 applies. UK is not on the EU adequacy list, but EU-to-UK transfers use UK-GDPR-equivalent protections (Art. 46 SCCs apply symmetrically). UK-to-US transfers require SCCs.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Same as EU but with slightly more flexibility for law enforcement / national security exceptions (not relevant for Calm Witness in v0). Obtain explicit consent under UK GDPR Art. 7; document the lawful basis. If principals are UK-resident, appoint a DPO if required (UK GDPR Art. 37). For UK-to-US transfers, use Standard Contractual Clauses. v0 is deployable in the UK with proper consent infrastructure and legal counsel review, but expect regulatory friction.

---

## Canada (PIPEDA + Provincial Variants)

**Top-line stance:** REGULATED (federal PIPEDA and provincial privacy laws)

**Key statute:**
- **Personal Information Protection and Electronic Documents Act (PIPEDA), Part 1, S.C. 2000, c. 5**, Principle 1 (Accountability), Principle 3 (Consent), Principle 4 (Limiting Use, Disclosure, Retention).
- **Quebec Law 25 (Bill 64), An Act to modernize legislative provisions as regards the protection of personal information, in force 2023**, §§92–93 (processing of sensitive personal information including biometric).
- **BC Privacy Protection Act (proposed, not yet in force as of 2026)**, expected to provide BC-specific rules.
- **Alberta Personal Information Protection Act (PIPA), S.A. 2003, c. P-6.5**, Part 1.

**Biometric-specific clauses:**
- PIPEDA Sch. 1, Principle 3: Requires consent *before* collecting, using, or disclosing personal information. "Personal information" includes biometric data (not statutorily defined in PIPEDA, but PIPEDA Interpretation Guidelines treat voice, facial geometry, fingerprints as personal information).
- Quebec Law 25 §92: Treats biometric data as "sensitive personal information" requiring heightened consent and security measures. Defines biometric as information derived from physical or physiological characteristics for identification purposes.
- Alberta PIPA §1(h): "Personal information" includes biometric identifiers used for identification.

**Behavioral biometric edge case:**
- Transcript-only voice: PIPEDA treats the voice *recording* as personal information, but a transcript (text output from ASR) is less clearly personal information unless it is linked to the speaker. The *voice characteristics* (patterns, prosody) that differentiate one speaker from another are biometric; a denuded transcript may not be. Recommend legal counsel.
- Handwriting kinematics: Treated as personal information under PIPEDA and Quebec Law 25.

**ZK-attestation interpretation:**
- PIPEDA Art. 4(2) defines collecting/using personal information broadly. The distance computation and commitment are "use" of personal information. The proof (output bit) is personal information if identifiable as relating to the principal.

**Cross-border transfer constraint:**
- PIPEDA Principle 4.1.3: "An organization shall not disclose personal information to a third party located outside of Canada unless (a) the individual to whom the information relates consents, or (b) it is required by law."
- Quebec Law 25 §§102–104: Adds requirement for adequacy assessment of the receiving jurisdiction's privacy laws. If transferring to the US, Quebec organizations must conduct a "substantially equivalent" analysis; the US is not considered substantially equivalent (no federal comprehensive privacy law), so third-country Standard Contractual Clauses or Binding Corporate Rules are required.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is deployable in Canada with explicit consent under PIPEDA Principle 3 before biometric collection. For Quebec principals, obtain heightened consent for sensitive personal information and conduct adequacy assessment for any disclosure to non-Canadian counterparties. Document consent records in the vault (Everest 72). For cross-border transfers to US counterparties, use Standard Contractual Clauses or equivalent contractual safeguards. PIPEDA compliance is lighter than GDPR; v0 is feasible with proper consent infrastructure.

---

## Japan (APPI — Act on the Protection of Personal Information)

**Top-line stance:** REGULATED (APPI treats behavioral biometric as personal information requiring care; not prohibited but restricted)

**Key statute:**
- **Act on the Protection of Personal Information (APPI), Act No. 57 of 2003 (as amended by Act No. 43 of 2020), effective 2022**.
- **APPI Art. 2(1)**: Defines "personal information" as information that can identify a specific individual (name, birthday, address, phone number, email, individual ID, biometric data, etc.).
- **APPI Art. 16**: Requires that personal information be processed for specified, explicit purposes.
- **APPI Art. 24**: Restricts use or disclosure of personal information to the original stated purpose unless consent is obtained (with limited exceptions).

**Biometric-specific clauses:**
- APPI Art. 2(1): Explicitly lists "biometric data" (顔や瞳の特徴, facial and iris characteristics) as personal information. Not exhaustive; APPI Enforcement Guidelines (2022) clarify that behavioral characteristics (handwriting, voice patterns, gait) are also treated as personal information if they identify an individual.
- APPI Art. 36: Specifies that controllers must ensure appropriate security measures for personal information.

**Behavioral biometric edge case:**
- Transcript-only voice: Under APPI, a transcript is personal information if it can identify the speaker (lexical fingerprinting via vocabulary/phrasing). Voice characteristics (pitch, rhythm, prosody) are biometric under APPI.
- Handwriting kinematics: Explicitly personal information under APPI Art. 2(1) guidance.

**ZK-attestation interpretation:**
- APPI Art. 16 requires specification of purpose at the time of collection. Computing a biometric distance and committing it is "use" under APPI. The proof-output (a single bit) is personal information if it relates to the principal.
- Is committing-a-distance equivalent to "processing"? APPI does not define "processing" as narrowly as GDPR; "use" is the operative term (Art. 24). Computing and committing the distance is "use."

**Cross-border transfer constraint:**
- APPI Art. 23(1): Transfer of personal information to a third party in a foreign country is restricted. The controller must ensure that the recipient implements appropriate safeguards substantially equivalent to APPI's own requirements (no specified list of "adequate" countries; case-by-case assessment).
- No formal adequacy determinations (unlike EU/Canada). Typically requires contractual safeguards (Standard Contractual Clauses or Binding Corporate Rules) plus notice to the PPC (Personal information Protection Commission).

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is deployable in Japan with proper consent and purpose specification. Specify at enrollment that biometric data will be used for "user-state attestation for disclosure to authorized counterparties" (APPI Art. 16). Obtain explicit consent before collecting biometric samples. Document the purpose and consent in the vault. For cross-border transfers to non-Japanese counterparties, implement Standard Contractual Clauses and notify the APPI. v0 is feasible with clear purpose specification and consent infrastructure.

---

## Australia (Privacy Act 1988 + Australian Privacy Principles)

**Top-line stance:** REGULATED (Privacy Act 1988 and APPs treat biometric as sensitive personal information; manageable with consent)

**Key statute:**
- **Privacy Act 1988 (Cth)**, esp. Part 1, Div. 1 (Australian Privacy Principles), App. 1 (APPs 1–13).
- **Australian Privacy Principles (APPs)**, particularly:
  - **APP 1 (Open and Transparent Management of Personal Information)**: Requires privacy policy disclosure.
  - **APP 3 (Collection of Solicited Personal Information)**: Requires consent before collection of sensitive information.
  - **APP 5 (Notification)**: Requires notification of privacy breaches.
  - **APP 6 (Use or Disclosure)**: Restricts use/disclosure to the original purpose.
  - **APP 9 (Adoption, use or disclosure of government identifiers)** and implicit treatment of biometric as government identifier-adjacent.

**Biometric-specific clauses:**
- Privacy Act 1988 §6(1): Defines "sensitive information" to include biometric information (fingerprints, facial recognition, voice, iris scans, handwriting analysis). Specifically protected under APP 3.
- APP 3.1(c): An APP entity must not collect personal information of a sensitive kind unless the individual consents or an exception applies (health, law enforcement, etc.).
- Australian Information Commissioner Guidance (2023): Confirms that handwriting and voice characteristics are sensitive information requiring heightened protection.

**Behavioral biometric edge case:**
- Transcript-only voice: If the transcript itself does not identify the individual (i.e., it's generic text with no speaker-identifying characteristics), it may not be "sensitive information" under APP 3. However, the voice recording *before* transcription is sensitive; destroying it is essential.
- Handwriting kinematics: Explicitly sensitive information under Privacy Act 1988 §6(1).

**ZK-attestation interpretation:**
- Privacy Act 1988 §6C: "Personal information" includes any information or opinion about an individual whose identity is apparent or can be reasonably ascertained. The biometric distance and commitment are "personal information" if linkable to the principal. The proof-output bit is personal information.
- APP 6: Once sensitive information is collected, disclosure to a third party (even for a substantively different purpose) requires consent or an exception.

**Cross-border transfer constraint:**
- Privacy Act 1988 §16A (APP 1, Principle 1.2): An APP entity is accountable for any breach of APPs that occurs when the entity discloses personal information to an overseas recipient unless the recipient is subject to a substantially equivalent privacy law. Australia has adequacy determinations with Switzerland and UK; most other jurisdictions (including US) do not meet the "substantially equivalent" test. Therefore, disclosure to overseas counterparties requires explicit consent and (preferably) contractual safeguards (Standard Contractual Clauses or Binding Corporate Rules).

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is deployable in Australia. Obtain explicit consent under APP 3 before collecting sensitive biometric information. Implement a clear privacy policy (APP 1). Document consent in the vault. For disclosures to overseas counterparties, obtain separate consent and implement Standard Contractual Clauses. Australia is more flexible than EU/Canada; v0 is feasible with standard consent infrastructure.

---

## Brazil (LGPD — Lei Geral de Proteção de Dados)

**Top-line stance:** REGULATED (LGPD treats biometric as sensitive personal data; similar to GDPR in structure but more flexible on consent)

**Key statute:**
- **Lei Geral de Proteção de Dados (LGPD), Law No. 13,709 of 2018 (as amended by Law No. 13,853 of 2019)**, effective 2020.
- **LGPD Art. 5 (Definitions)**: Defines "personal data" and "sensitive personal data."
- **LGPD Art. 9**: Prohibits processing of sensitive personal data except in specified circumstances (Art. 11–12 exceptions).
- **LGPD Art. 11 & 12 (Consent)**: Sensitive data processing requires explicit consent unless an exception applies.

**Biometric-specific clauses:**
- LGPD Art. 5, III: Defines "sensitive personal data" (dados pessoais sensíveis) as including "physical, biometric, physiological, genetic data...or health data...that could result in discrimination or risk to the fundamental rights of the individual."
- LGPD Art. 9: Processing of sensitive personal data is forbidden unless explicit consent is obtained or an exception applies (Art. 11–12, e.g., fulfillment of legal obligation, protection of life, etc.).

**Behavioral biometric edge case:**
- Transcript-only voice: LGPD classifies voice characteristics (but not necessarily transcripts) as biometric. A pure transcript (text) is not explicitly biometric under LGPD unless it can be used to identify a specific individual through linguistic patterns.
- Handwriting kinematics: Explicitly biometric under LGPD Art. 9.

**ZK-attestation interpretation:**
- LGPD Art. 5, I: Defines "processing" (tratamento) as "every operation carried out with personal data, such as those of collection, production, reception, classification, utilisation, access, reproduction, transmission, distribution, processing, filing, storage, elimination, evaluation or control of information, modification, communication, transfer, diffusion or extraction." Computing the distance is processing; committing is processing; the proof-output bit is personal data (if identifiable).

**Cross-border transfer constraint:**
- LGPD Art. 33–34: Transfer of personal data to countries *outside* Brazil is restricted. The controller must ensure "adequate level of protection" (adequação de proteção) in the receiving country. Brazil recognizes adequacy in select countries (Switzerland, UK, Canada); most others (including US) do NOT have adequacy determination. Transfers require explicit consent (Art. 11(I)(b)) and must document the legal basis.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is deployable in Brazil with explicit consent for sensitive data. Obtain consent before biometric collection. Document consent in the vault. For cross-border transfers to non-adequate-protection countries (e.g., US), require explicit separate consent (Art. 11(I)(b)) and Standard Contractual Clauses. Brazil is more flexible on consent than GDPR (can rely on explicit consent alone, without narrow Art. 9(2) exceptions), so v0 is feasible.

---

## India (DPDP Act 2023)

**Top-line stance:** UNCLEAR (newly enacted DPDP Act 2023 not yet in force; unclear how behavioral biometric is treated)

**Key statute:**
- **Digital Personal Data Protection Act, 2023 (DPDP Act)**, enacted 2023, expected to come into force by late 2026.
- **DPDP Act §3 (Definitions)**: Defines "personal data" (not exhaustively defining "biometric" but covering sensitive personal data).
- **DPDP Act §6(2)**: Restricts processing of sensitive personal data to specified lawful bases (consent, legal obligation, vital interest, etc.).
- **Draft Rules (v2.0, Feb 2024)** not yet finalized; interpretation of biometric scope remains uncertain.

**Biometric-specific clauses:**
- DPDP Act does not define "biometric" explicitly. §3 references "sensitive personal data" without itemizing categories. Early drafts suggested "genetic, physiological, behavioral" data, but the finalized §6 is vague.
- Government Notices and NITI Aayog guidance (2023–2024) suggest biometric (facial, fingerprint, iris, voice) will be treated as sensitive personal data, but no statute explicitly names behavioral biometric.

**Behavioral biometric edge case:**
- Transcript-only voice: Unclear. If the transcript itself is not "voice biometric," it may fall outside sensitive data scope. Handwriting kinematics may or may not be treated as sensitive; no guidance yet.
- Handwriting kinematics: Unclear whether kinematic (motor) patterns are considered "biometric" under DPDP. The law groups "physical," "physiological," and "behavioral" characteristics but does not define boundaries.

**ZK-attestation interpretation:**
- DPDP Act §2(a) defines "personal data" broadly as "any data about an individual who is identifiable" by that data alone or in combination. A biometric distance and commitment are personal data. The proof-output bit (baseline/not-baseline) is personal data if linked to an identifiable individual.
- Unclear whether the "distance commitment" operation qualifies as "processing" under DPDP (the Act does not define processing as explicitly as GDPR).

**Cross-border transfer constraint:**
- DPDP Act §8 (transfer): Transfer to countries *outside* India is restricted to countries with "adequacy determination" by the Government of India. As of 2026, NO adequacy determinations have been issued. Therefore, transfers to any jurisdiction (including US, EU, etc.) are technically prohibited unless the Government issues guidance or exceptions.
- This is the single largest DPDP friction: the adequacy regime is not yet operational.

**Recommended posture for Calm Witness operating in or interacting with this jurisdiction:**
Calm Witness v0 is NOT currently deployable in India under DPDP. Wait for finalized rules and adequacy determinations (expected 2026–2027). If deploying to Indian principals now, document that DPDP compliance is uncertain and recommended approach is to suspend biometric collection until legal clarity exists. For Indian principals disclosing to overseas counterparties, the cross-border transfer is technically prohibited absent adequacy determination. Recommend legal counsel review before any India deployment.

---

## Jurisdiction × Disclosure Use Matrix

Legal-risk ratings: **LOW** (deployable with standard consent), **MEDIUM** (deployable with jurisdiction-specific counsel and extra mitigations), **HIGH** (likely blocked or requires narrow lawful basis), **CRITICAL** (do not deploy without independent DPO or regulator sign-off), **SCOPE_PROHIBITED** (forbidden by [`CALM_WITNESS_SCOPE_STATEMENT.md`](../CALM_WITNESS_SCOPE_STATEMENT.md) §2 regardless of jurisdiction; license forfeit if deployed under the Calm Witness name).

| Disclosure use | US | EU | UK | CA | JP | Required mitigations (all jurisdictions where not SCOPE_PROHIBITED) |
|---|---|---|---|---|---|---|
| **Agent-to-agent collaboration calibration** (scope §1) | MEDIUM | HIGH | MEDIUM | MEDIUM | LOW | Written consent before enrollment (BIPA §14(a) in IL; GDPR Art. 7 in EU); per-predicate per-counterparty grants (Everest 8); disclosure audit log (Everest 72); counterparty VC binding (Everest 69). |
| **Financial KYC / anti-fraud** (transactional, not credit) | MEDIUM | HIGH | MEDIUM | MEDIUM | LOW | Same as above plus explicit `financial` class consent; document that proof is not creditworthiness input (scope §2.4); rate limits (Everest 76). |
| **Duress / bank-teller note push** (Everest 58) | MEDIUM | CRITICAL | HIGH | MEDIUM | LOW | Pre-authorized counterparty list; stealth push only to enrolled recipients (Everest 78); EU may require Art. 9(2)(d) vital-interests analysis before any EU-resident principal enrolls; codeword never in plaintext chain. |
| **Medical principal-authorized communication** | MEDIUM | HIGH | MEDIUM | MEDIUM | LOW | `medical` class default deny unless principal grants; no clinical predicates; scope §2.5 blocks diagnosis; HIPAA/PIPEDA counsel if US/CA health entities involved. |
| **Cross-border proof transfer** | LOW (domestic) / MEDIUM (export) | CRITICAL | HIGH | HIGH | MEDIUM | SCCs or Art. 46 equivalent for EU/UK/CA/BR outbound; APPI Art. 23 adequacy assessment for JP; geofence refusal when transfer_mode restricted (Everest 78); document proof-as-personal-data conservative stance. |
| **Governmental / law-enforcement surveillance** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.1; `governmental` class defaults deny; EU AI Act Art. 26 real-time biometric ban reinforces; do not seek lawful-basis workarounds. |
| **Employment screening / termination** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.2; no `employment` counterparty class; BIPA private right of action adds US litigation risk if misused. |
| **Insurance underwriting / claims** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.3; Quebec Law 25 sensitive-data rules add CA friction if misclassified. |
| **Lending / credit decisions** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.4; `financial` class is KYC-only, not FCRA/credit-bureau use. |
| **Clinical diagnosis / care rationing** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.5 medical diagnosis; behavioral attestation is not a clinical instrument. |
| **Child welfare / custody / family court** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.6 child welfare; no court-evidence predicate exists in v0. |
| **Immigration adjudication** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.7 immigration. |
| **Predictive future-behavior decisions** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.8 predictions about future behavior; v0 predicates are state-attenuation, not forecasting. |
| **Cross-principal population aggregation** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.9 aggregation across principals; one principal, one counterparty, one bit per session. |
| **Marketing / advertising targeting** | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | SCOPE_PROHIBITED | Scope §2.10; CPRA "sale/share" rules add US penalty if misused. |

**Reading the matrix:** Permitted rows (top four plus conditional cross-border) require jurisdiction-specific consent infrastructure from § "What Calm Witness Must Build." Prohibited rows inherit the one-way scope ratchet (scope §4): tightening only, never loosening. When a counterparty requests a SCOPE_PROHIBITED use, the operator refuses before predicate evaluation (geofencing, Everest 78) and logs the refusal without revealing undisclosed predicates (Everest 77).

---

## Summary Matrix

| Jurisdiction | Stance | Behavioral biometric in scope? | ZK proof = "processing"? | Special-category prohibition? | v0 deployable as-is? |
|---|---|---|---|---|---|
| **United States (BIPA/CPRA)** | REGULATED | Yes (BIPA §14(a), CPRA Art. 27) | Yes (initial distance computation) | No explicit prohibition; consent required | Yes, with consent infrastructure |
| **European Union (GDPR)** | RESTRICTED | Yes (Art. 4(14), Art. 9) | Yes (distance computation is processing) | Yes, Art. 9(1) unless Art. 9(2) lawful basis | No (requires Art. 9(2) basis, likely unfeasible) |
| **United Kingdom (UK GDPR)** | REGULATED | Yes (Art. 9 as applied) | Yes | Yes, Art. 9(1) with carve-outs | Possibly, with consent + carve-out analysis |
| **Canada (PIPEDA/Law 25)** | REGULATED | Yes (personal information; Quebec "sensitive") | Yes (use under PIPEDA) | No explicit prohibition; consent required | Yes, with consent + adequacy for transfers |
| **Japan (APPI)** | REGULATED | Yes (Art. 2(1) + Enforcement Guidelines) | Yes (use under Art. 24) | No prohibition; purpose specification required | Yes, with purpose specification + consent |
| **Australia (Privacy Act 1988)** | REGULATED | Yes (sensitive information, APP 3) | Yes (personal information under APP 6) | No prohibition; consent required (APP 3) | Yes, with consent + overseas safeguards |
| **Brazil (LGPD)** | REGULATED | Yes (Art. 9, sensitive personal data) | Yes (processing under Art. 5(I)) | Yes, Art. 9 prohibition unless Art. 11–12 exception | Yes, with explicit consent |
| **India (DPDP 2023)** | UNCLEAR | Unclear (not finalized) | Unclear (processing not defined) | Possibly; sensitive data treatment expected | No (adequacy regime not operational; wait) |

---

## Cross-Border Interaction Patterns

**Pattern A: US principal, US counterparty**
- Green light (deploy v0)
- No cross-border transfer; both subject to BIPA/CPRA/CUBI as applicable by state
- Obtain written consent (BIPA §14(a)) before biometric collection
- Implement audit log (Everest 72) for principal to monitor disclosures
- Verify counterparty identity (Everest 69)

**Pattern B: US principal, EU counterparty**
- Yellow (conditional)
- US principal subject to CCPA/CPRA for initial biometric collection + commitment
- EU counterparty subject to GDPR; receiving the proof triggers GDPR Art. 44 (transfer) unless proof is deemed non-personal-data
- Conservative interpretation: treat proof as personal data; require GDPR Art. 9(2) lawful basis assessment on the EU side (likely Art. 9(2)(d) "vital interests" for duress disclosure, unclear for baseline disclosure)
- Recommend: US principal consents; EU counterparty legal counsel reviews whether receipt of the proof constitutes "processing" personal data under GDPR and what Article 9(2) lawful basis applies
- If not feasible, recommend restricting to duress-only disclosures (Everest 58) which may qualify under Art. 9(2)(d) vital interests

**Pattern C: EU principal, US counterparty**
- Red until EU principal-residency-specific analysis completes
- EU principal must comply with GDPR Art. 9(1) at collection time (cannot enroll biometric without Art. 9(2) lawful basis)
- Disclosure to US counterparty triggers GDPR Art. 44 (transfer); US has no adequacy determination, so requires Art. 46 Standard Contractual Clauses or Art. 49(1)(a) informed consent
- Additionally, if the EU principal is a governmental actor or law enforcement using biometric for identification, EU AI Act Art. 26 may prohibit real-time remote identification
- Recommend: v0 NOT deployed to EU principals absent independent Data Protection Officer counsel

**Pattern D: US principal, UK counterparty**
- Yellow (similar to Pattern B)
- UK subject to UK GDPR Art. 9; same Art. 9(2) lawful basis analysis applies as Pattern B
- UK has slightly more flexibility (UK DPA 2018 carve-outs for law enforcement), but not relevant for Calm Witness in v0
- Recommend: same as Pattern B; obtain UK legal counsel review of lawful basis

**Pattern E: US principal, Japanese counterparty**
- Yellow (manageable)
- US principal subject to CPRA; Japan counterparty subject to APPI Art. 16 (purpose specification) and Art. 24 (use restriction)
- No special-category prohibition on Japanese side; consent or purpose-specification sufficient
- Cross-border transfer to Japan is not restricted (Japan recognizes US adequacy in limited contexts; Calm Witness proof may not require formal adequacy if treated as non-identifiable)
- Recommend: US principal consents; Japanese counterparty specifies purpose ("user-state attestation for Calm Witness disclosure") at receipt time; document in vault

**Pattern F: Anonymous counterparty**
- Red (no jurisdiction analysis possible)
- Cannot implement Everest 69 (counterparty identity binding) if counterparty identity is unknown
- Cannot assess which jurisdiction's laws apply to the disclosure
- Recommend: v0 does NOT support anonymous counterparties; Everest 69 requires counterparty CredexAI VC

---

## What Calm Witness Must Build to Deploy Across All Jurisdictions

1. **Per-jurisdiction consent forms** (Everest 8 prerequisite) — templated consent forms for each jurisdiction's legal requirements (BIPA §14(a), GDPR Art. 7, UK GDPR Art. 7, PIPEDA Principle 3, APPI Art. 24, APP 3, LGPD Art. 11, DPDP pending). Vault stores which consent(s) are active per principal.

2. **Per-jurisdiction predicate availability** (Everest 6 prerequisite) — not all predicates can be disclosed in all jurisdictions. E.g., "biometric_match_within(τ)" (Everest 56) may require Art. 9(2) lawful basis in EU; "bank_teller_note_active" (Everest 58) may qualify as Art. 9(2)(d) "vital interests" in EU but requires separate legal analysis. Route map must document which predicates are available in which jurisdictions.

3. **Geofencing of disclosure responses** (Everest 78 prerequisite) — the operator must query the principal's jurisdictional residency / the counterparty's jurisdictional residency before responding to a disclosure request (Everest 66). If responding would violate the applicable jurisdiction's law (e.g., GDPR prohibition without lawful basis), the operator refuses the disclosure with a jurisdiction-code error.

4. **Cross-border transfer mode selection** (Everest 67 prerequisite) — disclosure response schema must include a `transfer_mode` field indicating whether the proof is subject to cross-border transfer restrictions (GDPR Chapter 5, Canada §16A, Brazil Art. 33, Australia APP 1.2, Japan APPI Art. 23, India DPDP §8). If transfer is restricted, include a flag requiring counterparty to confirm jurisdiction + lawful basis before accepting proof.

5. **Data Protection Officer support** (Everest 80 prerequisite) — for EU/UK deployments, implement tooling to support DPO assessment (GDPR Art. 37–39). Include a DPO-readable log of all enrollments, consent grants, disclosures, and retention periods.

6. **Compliance audit trail** (Everest 72 prerequisite) — every consent grant, every disclosure request/response, every transfer decision must be logged in the vault with timestamps, counterparty identity, jurisdiction, and applicable legal standard. Implement reports that DPOs, compliance officers, and principals can query.

7. **Scheduled re-consent reminders** (Everest 76 prerequisite) — for jurisdictions with time-bounded consent (e.g., GDPR Art. 7(3), APPI Art. 24(2) typically require re-confirmation annually), implement a scheduler (mcp__scheduled-tasks__create_scheduled_task or Everest 76 cooling-off) that prompts the principal to renew consent before it expires.

---

## Closing

Calm Witness v0 is viable for US-only deployments (Pattern A) and marginally viable for US-principal-with-trusted-counterparties-in-CA/JP/AU (Patterns E, Japan-variant). Cross-border flows to EU/UK counterparties (Patterns B, D) require detailed Art. 9(2) lawful-basis analysis and are currently unfeasible absent a duress-only disclosure mode. India deployments are blocked pending DPDP adequacy determinations (2026–2027).

The route map should prioritize Everest 79 (this doc), Everest 8 (consent axioms), Everest 72 (disclosure logging), and Everest 80 (ethics review) as prerequisites to any multi-jurisdiction deployment. A "minimum viable international" posture is (1) v0 deployed in US with full consent infrastructure, (2) opt-in for disclosures to trusted overseas counterparties, (3) per-jurisdiction legal counsel review before each new counterparty jurisdiction is added to the allow-list.

---

**— Calm, 2026-05-20**
