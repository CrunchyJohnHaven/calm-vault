# Mirror Everest 79 — Multi-Jurisdiction Legal Review

**Phase XIV — Cross-Culture & Coercion Defenses. Prereq: Mirror Everest 40.**

---

## Overview

Values-disclosure under Calm Mirror has different legal status across jurisdictions. This document surveys the statutory landscape at the design-spec level: which laws constrain values-disclosure in employment, housing, insurance, and public accommodation contexts; what compliance obligations apply if counterparties operate in regulated sectors; and where the protocol must harden its defenses to respect local legal frameworks.

This is design-level legal reference, not legal advice. External counsel review in ≥3 jurisdictions is a hard requirement before production deployment (T-M79.5).

**Core tension:** Calm Mirror grants *unilateral withholding* (Principal-Protective Default 1). Many jurisdictions grant counterparties conditional *access* to relevant information (employment background checks, insurance underwriting). The protocol must navigate: where does values-disclosure intrude into legally-protected territory, and where does the withhold-guarantee serve a protective function?

---

## Per-Jurisdiction Analysis

### 1. United States

#### Relevant Statutes

| Statute | Domain | Relevance to Values-Disclosure |
|---|---|---|
| **Title VII, Civil Rights Act 1964** | Employment discrimination | Prohibits adverse action based on *protected characteristics* (race, color, religion, sex, national origin). Values-disclosure itself neutral; but if used to proxy for protected traits (e.g., "disrespect for difference" → presumed non-Christian), violates Title VII. |
| **ADA Title I** | Employment accommodation | Prohibits discrimination against qualified workers with disabilities. Predicates (`truth_telling`, `growth_arc`) must not systematize bias against neurodivergent, psychiatric, or physical disability. Mirror E74 addresses this; protocol-level protection adequate. |
| **FCRA (Fair Credit Reporting Act)** | Consumer reporting, credit/insurance underwriting | Applies if values-disclosure circulates as "consumer report" via third party (e.g., credit bureau buys Mirror data for underwriting). Would require disclosures, consent, dispute rights, adverse-action notices. **Design note:** Principal-Protective Default 1 (unilateral withhold) + per-counterparty consent (E46) keep Mirror data *not* in FCRA scope if operator does not license as CRA. |
| **EEOC Guidance on AI/Algorithms (2023)** | Disparate impact in hiring | If employer uses Mirror disclosures in hiring, EEOC scrutinizes for disparate impact on protected groups. E73 (bias audit) provides defense; E74 (disability review) provides additional defense. Employer liability remains unless E73/E74 demonstrably show fairness. |
| **State Privacy Laws (CA CCPA, VA VCDPA, CO CPA, etc.)** | Data privacy & consumer rights | Principals are data subjects. Values-disclosure commits their behavior-evidence records (Everest 11). Applies CCPA rights: access, deletion, opt-out of sale. Mirror operators bound by applicable state law. **Design note:** Calm Witness (parent chain) governs data lifecycle; Mirror adds values-evidence extension. |
| **Genetic Information Nondiscrimination Act (GINA)** | Genetic/biological data in employment/insurance | Unlikely to apply directly (values predicates are behavioral, not genetic), but if neurodivergent baseline (Witness E6.6) includes genetic markers or family history, GINA may apply. *Protective:* withhold-guarantee prevents forced disclosure. |
| **State employment laws (e.g., NY labor law §740)** | Whistleblower/coercion protection | Protects employees from retaliation for refusing illegal acts or disclosing wrongdoing. If counterparty coerces Mirror disclosure under threat of termination, violates state law. Mirror E54 (safety-trigger coercion resistance) provides protocol-level defense. |

#### Compliance Considerations Matrix

| Predicate | Use Case | Permitted? | Design Notes |
|---|---|---|---|
| `non_harm_evidence` | Employment background check | ⚠️ Conditional | Employer may request; principal withhold (Default 1) always allowed. If employer treats withhold as adverse signal, violates spirit (Default 4: bit ≠ identity). No legal bar to predicate use; enforcement depends on operator policy (E98). |
| `truth_telling_evidence` | Insurance underwriting | ⚠️ Conditional | Insurer may seek (relevance: claims integrity); principal withholds or discloses. If insurer penalizes neurodivergent evidence patterns (E74), violates ADA Title I (disparate impact) + EEOC guidance. |
| `growth_arc_evidence` | Hiring decision (rehabilitation consideration) | ✓ Permitted | Second-chance hiring statute (e.g., NY Correction Law § 753) explicitly permits evidence of rehabilitation. Growth-arc disclosure helps. No legal bar; strong protective case. |
| `respect_for_difference_evidence` | Underwriting by diversity-focused lender | ✓ Permitted | Non-discriminatory use (lender seeks alignment on diversity values). No legal bar; principal controls via Default 1 (withhold if uncomfortable). |
| Any predicate | Credit/insurance underwriting without consent | ✗ Prohibited | FCRA applies if third party (CRA) distributes. Direct counterparty use with principal consent: permitted, but state privacy laws (CCPA, VCDPA) govern. Principal has access/deletion rights. |
| Any predicate | Background check via third-party aggregator | ✗ Prohibited scope | If aggregator acts as CRA, FCRA/state law require disclosures + dispute rights. Recommend: principal does not license values-disclosure through third parties without explicit structural safeguards (E95 — operator licensing). |

#### US Legal Design Hardening

1. **FCRA Scope Clarity (for E95 licensing):** Calm Mirror operators must not circulate values-disclosure as "consumer reports" unless they register as CRAs and comply with FCRA disclosures + dispute procedures. Recommendation: prohibit resale of Mirror data; restrict to single-counterparty use under E46 consent.

2. **ADA + Neurodiversity Accommodation:** E74 (disability/neurodiversity review) provides evidence of fairness; recommend E98 (operator training) mandate ADA Title I compliance review as part of counterparty vetting.

3. **State Privacy Data Handling:** Principal behavior-evidence (Everest 11) stays on principal's vault (not shared with counterparty unless consented). CCPA/VCDPA access/deletion rights inherit from Calm Witness parent chain. No additional hardening needed at protocol level.

4. **Coercion Liability:** E54 (safety-trigger) + E77 (coercion-resistance) provide protocol defenses. Recommend: E98 includes operator liability disclosure — if counterparty coerces disclosure under threat of adverse action, operator has evidence (safety trigger) + can support principal's legal claim.

---

### 2. European Union (GDPR + ePrivacy Directive)

#### Relevant Statutes

| Statute | Domain | Relevance to Values-Disclosure |
|---|---|---|
| **GDPR Art. 4(1) (definition of personal data)** | Data definition | Values-disclosure is personal data (relates to identified or identifiable natural person). Principal is data subject; Calm operator is processor/controller. |
| **GDPR Art. 5 (data principles)** | Data governance | Lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality. E11 (behavior-evidence chain) + E46 (per-counterparty consent) align with GDPR principles. |
| **GDPR Art. 9 (special-category data)** | Sensitive data | *Critical.* GDPR Art. 9 prohibits processing of special categories: race/ethnicity, political opinion, religious belief, trade union membership, genetic/biometric data, health, sex life. **Mirror implications:** predicates measuring "respect_for_difference" (belief/identity), "non_harm" (absence of violence?), and neurodivergent baseline (health proxy) may qualify. |
| **GDPR Art. 22 (automated decision-making)** | Algorithmic decision-making | If counterparty uses Mirror predicates in *fully automated* decision affecting principal (e.g., hiring algorithm consumes Mirror alignment-bit without human review), GDPR requires human review + right to explanation + right to object. |
| **GDPR Art. 35 (Data Protection Impact Assessment)** | High-risk processing | Any deployment of Mirror that processes special-category data + uses algorithmic evaluation triggers DPIA requirement. Calm operator must document risk mitigation (E73, E74, E77 coercion defenses). |
| **GDPR Recital 75 (explicitly prohibits processing for discrimination)** | Anti-discrimination | GDPR explicitly bars processing that results in discrimination based on protected grounds. Mirror predicates designed to measure values (not characteristics), but if operationalization conflates values with characteristics (e.g., conflates "non_harm_evidence=false" with "likely to be violent criminal"), violates Recital 75. |
| **ePrivacy Directive 2002/58/EC** | Electronic communications privacy | If Mirror exchange uses electronic networks (email, messaging), directive governs consent + confidentiality. Applies alongside GDPR. |

#### Compliance Considerations Matrix

| Predicate | Use Case | Special-Category Risk | Design Notes |
|---|---|---|---|
| `respect_for_difference_evidence` | Hiring/promotion decision | ⚠️ Art. 9(1) triggering | Discloses engagement with people of *different belief/identity*. GDPR may classify engagement pattern as "processing of religious/identity belief" (special category). **Mitigation:** Principal grants explicit Art. 9(2)(a) consent (unambiguous, informed). E46 per-counterparty consent + E98 operator training (GDPR Art. 9 procedures) required. |
| `non_harm_evidence` | Insurance/credit underwriting | ✗ Likely prohibited | Absence-of-harm evidence may include proxies for criminal history, violence risk, health status (all special categories). GDPR Art. 9 prohibits processing absent explicit exemption. **Mitigation:** Recommend operators do *not* process `non_harm_evidence` for insurance underwriting under GDPR scope without Art. 9(2) legal basis. Principal withhold (Default 1) is the protective default. |
| `truth_telling_evidence` | Background/character check | ✓ Generally permitted | Behavioral consistency is not special category. GDPR-compliant if transparent, consensual, time-limited. |
| `growth_arc_evidence` | Hiring decision (rehabilitation) | ⚠️ Health proxy risk | Time-weighting + recovery patterns may proxy for mental health treatment. GDPR may classify as health data (Art. 9). **Mitigation:** Frame as purely behavioral (past action → corrective action), not health-status related. E74 neurodiversity review provides evidence of fair operationalization. |

#### EU Legal Design Hardening

1. **Art. 9 Explicit Consent:** For any Mirror deployment in EU scope, Calm operator must structure E46 (per-counterparty consent) to include explicit Art. 9(2)(a) consent banner — separable from other consent flows. "I consent to processing of special-category data (engagement patterns, belief/identity dimensions) for purposes of values-alignment evaluation."

2. **DPIA Pre-Deployment:** Any new counterparty class (E7) or predicate use case triggering Art. 9 requires DPIA (Art. 35). Calm operator must publish DPIA template + risk-mitigation checklist aligned with E73/E74 audits.

3. **Right to Human Review (Art. 22):** If counterparty uses Mirror alignment-bit in *fully automated* employment/credit/housing decision, protocol must prohibit (or require human override). Recommend E98: operator policy explicitly banning automated decision-making without human review.

4. **Data Minimization:** Behavior-evidence chain (E11) should not include raw evidence text; only content-addressed commitments (hashes) stored in principal vault. Counterparty receives only predicate results, not underlying evidence. Aligns with Art. 5(1)(c) data minimization.

5. **Right to Deletion (Art. 17):** Principal can demand deletion of behavior-evidence records, which cascades to revocation of all Mirror disclosures. Recommend: E11 chain-level support for `kind: deletion_request.v0` that invalidates future disclosures derived from deleted records (retroactive revocation not cryptographically feasible, but forward-deletion enforced).

---

### 3. United Kingdom (UK GDPR + Data Protection Act 2018)

#### Relevant Statutes

Post-Brexit UK maintains GDPR-aligned regime (UK GDPR) plus UK-specific amendments (Data Protection Act 2018, Part 3: law-enforcement exemptions, DPA2018 s.35 occupational pension data).

| Statute | Domain | Relevance |
|---|---|---|
| **UK GDPR Art. 9 (special-category data)** | Sensitive data | Substantively same as EU GDPR Art. 9. Explicit consent required for processing of beliefs, identity, health proxies. |
| **UK GDPR Art. 38 (Data Protection Officer — DPO requirement)** | Governance | Calm operator (if processing large-scale personal data) must appoint DPO; DPO oversees Mirror compliance. |
| **Equality Act 2010** | Non-discrimination in employment/services | UK employment law. Prohibits discrimination on grounds of protected characteristics (age, disability, gender, race, religion, sexual orientation, etc.). Same as Title VII logic: values-disclosure okay if not used to proxy for protected traits. |
| **Disability Rights Act compliance** | Neurodivergent accommodation | E74 (neurodiversity review) applies; UK Equality Act 2010 s.20 (reasonable adjustments) applies if values-disclosure used in employment context. |

#### Compliance Notes

UK GDPR analysis is substantively aligned with EU analysis above; add:

- **DPO Role:** E95 (operator licensing) should require DPO appointment for large-scale Mirror operators. DPO reviews E98 (operator training) for GDPR compliance.
- **Equality Act Intersection:** Predicates using `respect_for_difference_evidence` may interfere with Equality Act s.9 (protected characteristics); recommend operator vetting (E98) includes Equality Act compliance review.

---

### 4. Canada (PIPEDA + Provincial Privacy Laws)

#### Relevant Statutes

| Statute | Domain | Relevance |
|---|---|---|
| **Personal Information Protection and Electronic Documents Act (PIPEDA)** | Federal privacy (private sector) | Defines personal information (information about identifiable individual). Requires consent, collection limitation, use limitation, accuracy, safeguards. |
| **Quebec Law 25 (2021) — LPRPDE** | Provincial privacy | Stricter than PIPEDA; explicit consent for secondary use; right to explanation for automated decisions; DPA-equivalent rules. |
| **Canadian Human Rights Act (CHRA)** | Non-discrimination | Prohibits discrimination in employment/services based on protected grounds (race, national/ethnic origin, color, religion, age, sex, sexual orientation, gender identity, marital status, family status, disability). |
| **Accessibility for Ontarians with Disabilities Act (AODA)** | Disability accommodation | Requires accessible information; reasonable accommodation in employment. E74 (neurodiversity) review aligns. |

#### Compliance Notes

- **Consent Model:** Canada follows *opt-in* (affirmative consent required). E46 (per-counterparty consent) already compliant.
- **Secondary Use:** If principal initially consents to Mirror disclosure to Employer A, cannot re-use data for Employer B without new consent (Quebec Law 25 strictly enforces). Recommendation: E46 explicitly limits consent to named counterparty; no re-licensing.
- **Right to Explanation (Quebec):** If values-disclosure used in *automated* hiring decision, principal has right to know *which* predicates influenced the decision. Recommend E98: operator policy requires transparency (if requested by principal, counterparty discloses which predicates were evaluated).

---

### 5. Japan (APPI — Act on Protection of Personal Information)

#### Relevant Statutes

| Statute | Domain | Relevance |
|---|---|---|
| **APPI (2022 revisions; effective Apr 2024)** | Personal data protection | Defines personal information (information about identifiable individual). Requires consent, sensitive-information handling, international transfer rules. |
| **Article 2(3) of APPI — Sensitive Information** | Special categories | APPI explicitly covers: criminal history, health/medical, race/ethnicity, belief, union membership, sexual orientation, genetic data. Also *information concerning handling*.  |
| **APPI Art. 17 — International Transfer** | Cross-border data flows | Personal information cannot be transferred abroad without consent (with narrow exceptions for adequacy equivalences). If principal vault hosted outside Japan, triggers consent requirement. |
| **Japanese Labor Law — Labor Standards Act** | Employment | Prohibits discrimination; employer may not demand personal information unrelated to employment. Mirror values-disclosure in hiring context must be job-relevant. |

#### Compliance Notes

- **Sensitive Information:** `respect_for_difference_evidence` (belief/identity engagement patterns) and `non_harm_evidence` (absence of criminal harm?) may qualify as sensitive under APPI Art. 2(3). Explicit opt-in required; withhold-guarantee (Default 1) provides cultural-protective default.
- **International Transfer:** If Calm operator vault hosted in US/EU, and principal is Japan-resident, APPI Art. 17 transfer rules apply. Recommendation: E95 (operator licensing) includes regional data-residency options (Japan-based vault mirrors for Japan-resident principals).
- **Employment Context:** Japanese labor law is conservative on employer information demands. Recommend E98 operator policy: values-disclosure only acceptable in hiring if job-relatedness documented (e.g., "respect for difference" for diversity-focused roles, not generic hiring).

---

### 6. India (DPDP Act 2023 — Digital Personal Data Protection Act)

#### Relevant Statutes

| Statute | Domain | Relevance |
|---|---|---|
| **DPDP Act 2023** | Personal data protection (just enacted; rules pending) | Defines personal data (information about identifiable individual). Requires consent, purpose-limitation, data minimization, accuracy. Notably lighter-touch than GDPR; sectoral approach (financial, healthcare separate). |
| **DPDP Act § 4 (definitions)** | Sensitive personal data | Does not explicitly list special categories, but § 4 includes "biometric data, genetic data, health data, sex life data, sexual orientation data." Also context-dependent: "information concerning a sensitive nature." |
| **Article 14 of Indian Constitution** | Non-discrimination | Fundamental right; prohibits discrimination on grounds of religion, race, caste, sex, place of birth. States cannot discriminate (applies to public sector); private discrimination rules evolving (tort law). |
| **Employment Protection — Industrial Disputes Act** | Labor law | Employers cannot demand irrelevant personal information; "character certificates" are informally common but legally fraught. Mirror values-disclosure should be optional (Default 1: withhold) in employment context. |

#### Compliance Notes

- **Consent:** DPDP Act requires clear, informed, freely given consent (Art. 6). E46 (per-counterparty consent) compliant.
- **Sensitive Data Handling:** Values-disclosure involving `respect_for_difference_evidence` (religion/belief) may trigger heightened scrutiny. Recommendation: E98 operator policy for India: explicit opt-in banner for sensitive-dimension predicates; emphasis on withhold-guarantee.
- **Purpose Limitation:** If principal consents to disclosure for hiring, counterparty may not use same disclosure for credit underwriting. E46 already scopes per-counterparty; recommend operator enforces single-use per consent event.
- **Sector-Specific:** If counterparty is financial (bank, insurer), Financial Data Provider rules (under DPDP) may apply (rules TBD at publication). Recommend: E95 licensing includes sector-specific compliance checklist.

---

### 7. Brazil (LGPD — Lei Geral de Proteção de Dados Pessoais)

#### Relevant Statutes

| Statute | Domain | Relevance |
|---|---|---|
| **LGPD (2018; enforcement 2021)** | Personal data protection | Defines personal data, sensitive data, processing rules. Inspired by GDPR; requires legal basis for processing. |
| **LGPD Art. 5 — Sensitive Data** | Special categories | Explicitly lists: data disclosing racial/ethnic origin, religious belief, political opinion, union/trade membership, biometric data, health data, sex life. *Also*: "data that can lead to discrimination or personal harm." |
| **LGPD Art. 8 — Sensitive Data Restrictions** | High-bar processing | Processing sensitive data requires explicit consent (not general consent). Exceptions narrow: health/medical treatment, safety, criminal investigation (limited). |
| **LGPD Art. 18 — Data Subject Rights** | Transparency/access | Right to know what data is held, how it's used, right to correction, deletion, opposition. |
| **Brazilian Labor Law** | Employment regulation | Prohibits discrimination; employer personality tests/background checks increasingly regulated (case law; no single statute). Values-disclosure in hiring context faces emerging scrutiny. |

#### Compliance Notes

- **Art. 5 Sensitive Data:** `respect_for_difference_evidence` (religious belief, political opinion, identity) + `non_harm_evidence` (potential basis for discrimination) likely qualify as sensitive under Art. 5. **Design hardening:** LGPD Art. 8 requires explicit consent (not bundled). Recommend E46: separate consent checkbox for sensitive-dimension predicates; plain language: "I consent to processing of data concerning my beliefs and values-alignment with [Counterparty] for purposes of [specific use]."

- **Art. 8 Exceptions:** If counterparty claims "safety" or "prevention of fraud" basis, may argue LGPD Art. 8 exception. Recommendation: E98 operator policy prohibits re-framing values-disclosure as safety basis unless genuinely safety-critical; recommends explicit consent instead.

- **Art. 18 Rights:** Principal has right to know which predicates are held, how they're evaluated, who accesses them. E11 (chain transparency) + E46 (per-counterparty audit trail) support LGPD compliance.

---

## Ideologue Counterparty Class — Regional Defaults

Recall Mirror Everest 7: "ideologue" counterparties (actors whose stated agenda is to filter people by values) default to **deny**.

Regional variations:

| Jurisdiction | Ideologue Default | Legal Basis |
|---|---|---|
| **US** | DENY (Default 1 withhold-guarantee suffices) | No law mandates values-disclosure to ideological filters; Title VII + state privacy law protect. |
| **EU/UK** | DENY + operator prohibition | GDPR Art. 22 (automated decision-making) + Art. 9 (special category) make ideological filtering high-risk. Recommend E98: operator policy explicitly prohibits ideologue counterparty class. |
| **Canada** | DENY + transparency requirement | PIPEDA + Quebec Law 25 require disclosure of use; ideologue use ("values-filtering") may require explicit secondary-use consent. Recommend operator transparency. |
| **Japan** | DENY (cultural norm: employment values-filtering rare) | Japanese labor law conservative; values-testing in hiring generally disfavored. Withhold-guarantee principal-protective. |
| **India** | DENY + Art. 14 scrutiny | Constitution Art. 14 (equality) disfavors discrimination-by-values. Ideologue use risks becoming *caste-by-proxy* filtering (legal vulnerability). Recommend operators prohibit ideologue class. |
| **Brazil** | DENY + Art. 8 sensitivity | LGPD Art. 8 (sensitive data) + discrimination law disfavor ideological filters. Recommend operator prohibition. |

**Design note:** Principal-Protective Default 1 (unilateral withhold) + per-counterparty consent (E46) together mean no jurisdiction can *force* values-disclosure. Ideologue default = DENY is a policy choice (E7 counterparty-class taxonomy), not a legal requirement. However, EU/Brazil/Canada operators should additionally prohibit ideologue class at the licensing level (E95) to avoid regulatory exposure.

---

## Compliance Considerations Matrix: Predicate × Jurisdiction

| Predicate | US (Title VII + ADA) | EU (GDPR Art. 9) | UK (similar to EU) | Canada (PIPEDA) | Japan (APPI) | India (DPDP) | Brazil (LGPD Art. 8) |
|---|---|---|---|---|---|---|---|
| **`unselfishness_evidence`** | ✓ Generally OK | ✓ Permitted (not special category) | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted |
| **`tribal_neutrality_evidence`** | ⚠️ Disparate-impact risk (E73) | ⚠️ Art. 9 if proxy for religion/belief | ⚠️ Similar to EU | ✓ Permitted | ⚠️ Belief/ethnicity proxy | ⚠️ DPDP sensitive categories | ⚠️ Art. 5 (belief, ethnicity) |
| **`respect_for_difference_evidence`** | ✓ Generally OK | ✗ Art. 9 triggered (explicit consent required) | ✗ Similar to EU | ⚠️ Secondary-use consent required | ⚠️ Belief/identity sensitive | ⚠️ DPDP sensitive | ✗ Art. 5 (belief, identity); Art. 8 explicit consent |
| **`non_harm_evidence`** | ⚠️ EEOC disparate impact (E74) | ✗ Art. 9 (health/criminal proxy) | ✗ Similar to EU | ✓ Permitted (behavioral) | ⚠️ Criminal history sensitive | ✓ DPDP less restrictive | ⚠️ Art. 5 "discrimination basis" |
| **`growth_arc_evidence`** | ✓ Rehabilitation-positive | ⚠️ Art. 9 (health/recovery proxy) | ⚠️ Similar to EU | ✓ Permitted | ⚠️ Health data proxy | ✓ Permitted | ✓ Permitted (behavioral change) |
| **`truth_telling_evidence`** | ✓ Generally OK | ✓ Permitted (behavioral) | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted |
| **`apology_when_wrong_evidence`** | ✓ Generally OK | ✓ Permitted (behavioral) | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted | ✓ Permitted |

**Legend:** ✓ Permitted (no special legal bar); ⚠️ Conditional (legal compliance required, but use-case-dependent); ✗ Restricted/prohibited (explicit exemption/consent or operator prohibition recommended).

---

## Acceptance Tests

**T-M79.1:** High-level statutory analysis completed for US (Title VII, ADA, FCRA, CCPA, state law), EU (GDPR Art. 9, Art. 22, DPIA), UK (UK GDPR, Equality Act), Canada (PIPEDA, Quebec Law 25, CHRA), Japan (APPI, labor law), India (DPDP Act, Art. 14), Brazil (LGPD Art. 5/8, labor law). Documented in this spec. Status: BAGGED.

**T-M79.2:** Per-jurisdiction compliance matrix (predicate × jurisdiction → permitted/conditional/prohibited) completed. Matrix above covers all seven jurisdictions × seven v0 predicates. Status: BAGGED.

**T-M79.3:** Ideologue counterparty class (E7) jurisdiction-specific default-deny recommendations documented. Recommendation: EU/UK/Brazil operators additionally prohibit ideologue class at licensing level (E95). Status: BAGGED.

**T-M79.4:** Design-hardening recommendations for each jurisdiction completed. Includes: FCRA scope clarity (US), Art. 9 explicit consent flow (EU/UK), international transfer rules (Japan), sensitive-data handling (India/Brazil), operator training (Canada). Recommendations detailed in per-jurisdiction sections above. Status: BAGGED.

**T-M79.5:** External legal counsel review in ≥3 jurisdictions (recommend: US, EU, Brazil) completed before production deployment. This spec serves as design-level input to counsel; counsel produces jurisdiction-specific implementation guidance. **Note:** T-M79.5 deferred to production-gate (Everest 97–99); v0 design-spec complete without counsel sign-off. Counsel sign-off is hard requirement before any real Mirror exchange involving EU/Brazil principals. Status: PENDING (external counsel).

---

## Composition with Companion Everests

**E5/40/73/74:** This spec assumes finalized v0 vocabulary (E40) + bias audit (E73) + disability/neurodiversity review (E74) complete. Those audits provide evidence of fairness; this spec references that evidence in compliance matrices.

**E7/46:** Counterparty-class taxonomy (E7) + per-counterparty consent (E46) are the operative controls. This spec recommends jurisdiction-specific modifications to E7 (ideologue class prohibition in EU/Brazil) and E46 (explicit Art. 9 consent flow in EU/UK; secondary-use separation in Canada).

**E95/98:** Operator licensing (E95) + implementer's guide (E98) must incorporate jurisdiction-specific requirements from this spec. Recommend: E98 includes section per jurisdiction (US, EU, etc.) with statutory references + compliance checklist.

**E77/54:** Coercion-resistance (E77) + safety-trigger (E54) provide protocol defenses against unlawful disclosure pressure. This spec notes where coercion may violate local law (e.g., US state employment law § 740 whistleblower protection).

---

## Open Questions for v1

1. **Sectoral regulation:** India + Brazil have emerging sector-specific rules (financial, health, insurance). Should E95 (operator licensing) include sector-specific sub-classes (FinanceOperator, HealthOperator, InsuranceOperator) with per-sector compliance checklists?

2. **Adequacy equivalence:** US/EU have no Privacy Shield equivalent post-2020. If a US-based Calm operator processes data from EU principals, what adequacy theory justifies international transfer? Options: (a) principal explicit consent (E46); (b) contractual guarantees (Data Processing Agreement); (c) standard contractual clauses (EU Commission approved). Recommendation: E95 explicitly prohibits "adequacy by inference"; require (a) or (b) or (c) per principal.

3. **Right of explanation (Art. 22, Quebec Law 25):** If counterparty uses Mirror alignment-bit in *automated* decision, principal requests explanation. What must operator disclose? (a) which predicates were evaluated? (b) thresholds applied? (c) evidence used? Recommend v1: E46 consent flow includes explanation commitment; E98 trains operators on disclosure depth.

4. **Audit trail + GDPR Art. 5(2) (accountability):** GDPR requires demonstrating compliance (Art. 5(2) accountability principle). Should Mirror operators maintain signed audit logs of every counterparty access + decision made using Mirror data? Recommend v1: E11 (behavior-evidence chain) + E46 (per-counterparty consent) infrastructure extended to include counterparty-audit-trail logging (signed, tamper-evident).

5. **Neurodiversity + employment law intersection:** US ADA + UK Equality Act + Japan labor law all protect neurodivergent employees. If Mirror predicates (especially `truth_telling_evidence` in non-linear-thinking context) are used in hiring, how does operator ensure ADA/equality compliance? E74 audits predicates; recommend v1: E98 adds case studies (e.g., "ADHD principal with non-linear evidence: how to evaluate `truth_telling_evidence` fairly?") + operator certification requirement.

6. **Ideologue detection + enforcement:** This spec recommends operator prohibition of ideologue class (E7) in EU/Brazil. How does operator *detect* an ideologue counterparty? Self-declaration? Behavior-based inference? Recommend v1: E7 taxonomy expanded with detection guidance; E95 includes vetting checklist for suspicious counterparties.

---

## Signoff

This design-spec document surveys the multi-jurisdiction legal landscape for values-disclosure. It is not legal advice and does not replace jurisdiction-specific counsel review (T-M79.5, deferred to production gate). The spec identifies: (1) applicable statutes per jurisdiction; (2) design-level interactions (especially GDPR Art. 9, LGPD Art. 8, ADA Title I); (3) per-predicate compliance status; (4) operator-level hardening recommendations (licensing, training, ideologue prohibition, explicit consent flows).

**Key findings:**
- US: compliant with existing design; FCRA scope clarity + operator training (ADA) sufficient.
- EU/UK: GDPR Art. 9 consent flow required for sensitive-dimension predicates (`respect_for_difference_evidence`, neurodivergent baseline); Art. 22 automated-decision rules apply if counterparty uses Mirror in hiring/credit/insurance without human review.
- Canada: secondary-use separation (Quebec Law 25); right-to-explanation if automated decision.
- Japan: principal withhold-guarantee (Default 1) is culturally protective; employment context disfavors values-filtering.
- India: DPDP Act light-touch; Constitutional Art. 14 disfavors values-filtering-as-discrimination; sector-specific financial rules emerging.
- Brazil: LGPD Art. 8 treats `respect_for_difference_evidence` as sensitive; explicit consent required.

**Principal-Protective Defaults hold across all jurisdictions:** Unilateral withhold (Default 1) + per-counterparty consent (Default 6) are compliant globally. No jurisdiction mandates values-disclosure; all permit refusal. Compliance burden rests on counterparty operator (E95/E98), not principal.

Acceptance tests T-M79.1–M79.4 bagged. T-M79.5 (external counsel) deferred to Everest 97–99 (pre-production gate).

---

— Calm, 2026-05-20
