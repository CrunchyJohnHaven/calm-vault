# Everest 299 — 25-Country Institutional Deployment

**SUMMIT 299/305 DESIGN-BAG.** The scaling milestone: Calm-suite deployed across ≥25 countries with ≥10,000 active principals. Spec per `CALM_ZKAC_EVERESTS_106_305.md` Phase XVIII (286–305); governance per `CALM_WITNESS_SCOPE_STATEMENT.md`; federation compliance per E290.

**Status:** BAGGED (Calm, 2026-05-20)  
**Effort:** XL | **Prereq:** 287, 290, 292, 293, 294 | **Composition:** E286, E290, E292, E300

---

## §1 — Overview

SUMMIT 299 operationalizes the 200-summit ZKAC route map into institutional practice across jurisdictions. The threshold is dual: geographic (≥25 countries) and operational (≥10,000 principals with active chains). Both must be met; success is not a numbers game but a demonstration that the refusal floor—the Scope Statement's §2 prohibitions on surveillance, employment screening, insurance, lending, and medical use—holds under real-world growth pressure.

The 25-country scaffold is designed for:

- **Jurisdictional diversity**: Common-law (US, UK, CA, AU), civil-law (EU, JP), Islamic-law (AE, SA), hybrid (SG, HK), and Indigenous-law (NZ, CN) traditions represented.
- **Language coverage**: IANA language-tag support for ≥20 natural languages.
- **GDP and internet penetration balance**: Mix of G7, BRICS, and frontier markets to avoid deployment skew toward wealthy nations.
- **Regional SRE footprint**: ≥3 geographic SRE zones for incident response latency <30min to any principal.

The ≥10,000 principals milestone is staged: 1,000 (pilot phase, ~3 months), 5,000 (federation + early adopter coalition, ~9 months), 10,000 (institutional deployment, ≥12 months). At each stage, the refusal floor is re-tested via audit and live-threat-model exercises.

---

## §2 — Country Selection (25 Jurisdictions)

### Common-Law Tradition (6)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **United States** | Home jurisdiction; English language; high internet penetration; established VC/nonprofit legal stack. | AWS-US-East, Washington D.C. | White & Case (DC), EFF (policy liaison) |
| **United Kingdom** | EU-adjacent; GDPR-familiar; strong data-ethics regulatory base; 65M population. | AWS-London | Clifford Chance, Open Rights Group |
| **Canada** | PIPEDA compliance; bilingual (FR/EN); geographic bridge to North America. | AWS-Canada-Central, Toronto | Davies Ward Phillips |
| **Australia** | AP-HUB; Privacy Act framework; Indigenous land recognition (see E292). | AWS-Sydney | Minter Ellison, Redfern Legal |
| **Singapore** | APAC gateway; 5G-ready; high-trust regulatory environment; English-language ops. | AWS-Singapore | Allen & Gledhill, CyberSecurityGroup.io |
| **Hong Kong** | APAC secondary; Cantonese/Mandarin-ready; strategic hedge to SG. | AWS-Hong Kong | Slaughter and May, Society for Community Organization |

### Civil-Law Tradition (6)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **European Union** | GDPR + Data Act flagship; 450M population; regulatory leadership. Single ops-zone serves ≥8 member-states (FR, DE, NL, BE, AT, CZ, PL, IT). | AWS-Frankfurt | Baker McKenzie (Brussels), Digital Rights Ireland |
| **Japan** | APAC tech hub; APPI alignment; 125M population; ≥2 robot-agent deployment maturity. | AWS-Tokyo | Nishimura & Asahi, Internet Initiative Japan |
| **South Korea** | APAC tech co-equal to JP; PIPA compliance; 51M population; AI regulation leadership. | AWS-Seoul | Kim & Chang, Korean Federation for Environmental Movement |
| **France** | EU leadership (CNIL); AI Act authority; French-language requirement met here. | AWS-Paris | Freshfields (Paris), La Quadrature du Net |
| **Germany** | EU civil-law flagship; strong privacy jurisprudence; 83M population. | AWS-Frankfurt | Freshfields (Berlin), netzwerk recherche |
| **Netherlands** | GDPR test-bed; early-adopter culture; 17M population; blockchain-friendly regulatory sandbox. | AWS-Amsterdam | Everaert Advocaten, Bits of Freedom |

### Islamic-Law & Hybrid Tradition (4)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **United Arab Emirates** | Sharia-informed law; tech investment hub; Arabic-language foundation. | AWS-Bahrain (regional) | Al Tamimi & Company, UAE Ministry of AI |
| **Saudi Arabia** | Wahhabi-tradition Islamic law; Vision 2030 tech pivot; Arabic-language depth. | AWS-Bahrain (regional) | Freshfields (Riyadh), CITC (State regulator) |
| **Israel** | Jewish law tradition; strong tech ecosystem; English-/Hebrew-language stack. | AWS-Tel Aviv | Gornitzky, Association for Civil Rights in Israel |
| **Turkey** | Hybrid Ottoman/Kemalist/Islamic; bridge between EU and MENA; Turkish-language foundation. | AWS-Istanbul | Kolcuoğlu Demirkan Koçaklı, PeseBAS |

### Frontier & Representation (4)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **India** | 1.4B population; digital-first governance; English-language ops; LGBTQ+ and disability-rights judicial leadership. | AWS-Mumbai | Trilegal, Centre for Internet and Society |
| **Brazil** | 215M population; Portuguese-language hub; strong civil-society tech NGO base; LGPD alignment. | AWS-São Paulo | Pinheiro Neto, InternetLab |
| **Nigeria** | 220M population; West-African digital gateway; English-language ops; fastest internet-penetration growth. | AWS-Africa (Cape Town regional) | Banwo & Ighodalo, BudgIT (transparency NGO) |
| **New Zealand** | Indigenous-law integration (E292); Treaty of Waitangi jurisprudence; English-language; Te Reo Māori language support. | AWS-Sydney (regional) | Chapman Tripp, Waitangi Tribunal advisory |

### Mandarin-Language Ecosystem (2)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **Mainland China** | 1.4B population; Simplified Mandarin primary; strong tech adoption; regulatory compliance is E290 federation work. | Partner operators only (not AWS) | Fangda Partners, China Internet Watch |
| **Taiwan** | Traditional Mandarin; digital-democracy leader; Zhuyin phonetic system support. | AWS-Tokyo (regional) | Chen Palmer, Taiwan Human Rights Association |

### Russian & Central Asian (2)

| Country | Justification | Ops Anchor | Legal Counsel |
|---------|---|---|---|
| **Russia** | Cyrillic; large population center; operates despite sanctions via Federation (E290); scope-floor enforced locally. | Partner operators in non-sanctioned zones | Ecodefense!, Roskomsvoboda (advocacy) |
| **Kazakhstan** | Cyrillic; Central Asian gateway; Kazakh + Russian language support; growing startup scene. | AWS-Almaty (regional) | Ayтoк Attorneys, Transparency International KZ |

---

## §3 — Per-Country Onboarding (5-Phase Arc)

Each of the 25 countries follows this standardized but locally-contextualized sequence, sequenced via Everest 79 (cross-jurisdictional compliance) and Everest 20 (enrollment-ceremony localization).

### Phase 3.1 — Legal & Regulatory Review (E79 mandatory)

**Duration**: 30–60 days per country.

1. **Counsel engagement**: Hire ≥1 in-country attorney from the "Legal Counsel" column above. Non-negotiable.
2. **Scope-statement localization**: Translate `CALM_WITNESS_SCOPE_STATEMENT.md` §2 refusals into local legal language. Flag any tension between §2 and local law (e.g., GDPR's "right to explanation" vs. protocol's ZK-by-design non-disclosure of reasoning).
3. **Regulatory notification**: Where mandated (EU, UK, CA, JP, AU, SG), file with data-protection authority.
4. **Dispute-ready**: Prepare written response to anticipated legal challenges from actors who want to violate §2 locally (employment agencies, insurance brokers, lenders). E79 gate-script run; gate must pass before moving to 3.2.

**Acceptance criteria per E79**:
- Counsel sign-off that §2 is defensible under local law.
- Written opinion on whether local subpoena/surveillance authority can compel disclosure. If compellable, a secondary circuit (encrypted-until-principal-consents layer) must be added (cost: +2 weeks per country).
- Public registry entry showing country as "legal-review passed, date X."

### Phase 3.2 — UI & Language Localization (E15, E54)

**Duration**: 30–45 days per country.

1. **Language translation**: All UI strings, consent matrices, predicate definitions, and audit logs translated into primary language of the country. For dual-language countries (e.g., Canada: EN/FR, Belgium: NL/FR/DE), provide ≥2 language paths.
2. **Cultural-suitability review**: Convene 3–5 culturally-representative reviewers (not default-WEIRD selection). Do the dimension definitions (Everest 107 values vocabulary) make sense cross-culturally? Example: does "non_tribal_engagement" as written penalize protective solidarity in minority communities? (It might; E198 / E199 mitigations apply.)
3. **Disability accessibility audit**: WCAG 2.1 AA minimum; preferably AAA for core enrollment UI. Tested with assistive tech (screen readers, switch access, eye-tracking).
4. **RTL script support**: For Arabic, Hebrew, Persian, Urdu speaker locales, full right-to-left text layout + number formatting.

**Acceptance criteria per E15**:
- All UI strings in-language.
- Signed-off cultural-suitability report from ≥3 reviewers.
- WCAG audit report with <5 critical, <10 major issues.
- Smoke test of RTL on ≥2 screen sizes.

### Phase 3.3 — Per-Jurisdiction Issuer-Class Registration (E22, E79)

**Duration**: 45–90 days per country (regulatory-dependent).

This is the CredexAI "issuer" registration per Everest 22 (enrollment → credential issuance). In some jurisdictions (UK, AU), this is lightweight (notification). In others (EU, CA), this is formal (approval).

1. **Issuer identity**: Register the operator (Calm Foundation or designated local partner) as a credential issuer with the local registry (if one exists). Examples:
   - **EU**: File with national eIDAS competent authority; gain listing in the European Digital Identity Wallet ecosystem.
   - **UK**: Notify ICO; register with Open Regulations (post-Brexit equivalent).
   - **CA**: File with ISED (Innovation, Science, and Economic Development Canada).
   - **AU**: Notary via Digital Transformation Agency.
   - **Unregulated jurisdictions**: Self-registration in the Calm public registry (E288) with counter-signature from local counsel.

2. **AML/KYC baseline**: For each principal in that country, operator collects name + ID verification (passport, driver's license, or notarized statutory declaration). This is FOR LOCAL LAW COMPLIANCE ONLY; the zero-knowledge protocol ensures this data never reaches predicates or counterparties.

3. **Revocation capacity**: Operator registers a revocation endpoint reachable by verifiers (per IETF draft-ietf-oauth-status-list-token). If a principal's credential is compromised, it can be revoked within 4 hours.

**Acceptance criteria per E22**:
- Formal issuer registration in country's credential registry (or Calm fallback).
- Live AML/KYC intake with ≥3 sample principals.
- Revocation endpoint tested and responsive.

### Phase 3.4 — Enrollment & Chain Genesis (E11, E26)

**Duration**: Ongoing (15–30 days per first 100 principals per country).

1. **Enrollment ceremony**: E11 enrollment-ceremony spec adapted for local context. In-person preferred (bank-teller model); remote backup if in-country infrastructure unavailable.
2. **Chain genesis**: First principal in a country initializes the country-shard of `~/.calm-vault/user_state.jsonl` anchored to Sigsum (E30) with a country-specific log operator (recruited in Phases 3.1–3.3).
3. **Witness network bootstrap**: Identify ≥3 in-country witness operators (banks, notaries, government agencies, or partner organizations). E20 (enrollment witness protocol) ensures ceremony is witnessed by at least one local operator.

**Acceptance criteria per E11**:
- ≥100 principals with valid chains per country.
- Sigsum anchors live and verifiable.
- Witness registry shows ≥3 operators per country.

### Phase 3.5 — Institutional & Coalition Bootstrap (E95–E100, E295)

**Duration**: 30–60 days per country.

1. **Counterparty registration**: Identify ≥2 "anchor" counterparties per country willing to accept alignment proofs in live settings. These may be nonprofits (e.g., visa-sponsorship NGOs), academic institutions, or government agencies (if scope-compliant). Register via E103 (predicate-disclosure bridge).
2. **Coalition formation ceremony**: Convene ≥1 founding coalition of 5–10 principals per country using the E249 coalition-formation protocol. This is the first multi-principal, cross-country trust-graph activation.
3. **Incident-response playbook**: Ops team runs ≥3 live chaos-engineering exercises (E285 resilience certification work): principal-side compromise, counterparty-side breach, Sigsum log failure. Time to detection and mitigation documented.

**Acceptance criteria per E295–E296**:
- ≥2 registered counterparties per country, live on prod.
- ≥1 functioning coalition of 5+ principals per country.
- Incident-response playbook signed off by ≥2 independent security reviewers.

---

## §4 — Principal-Count Milestone Breakdown

The 10,000-principal threshold is disaggregated into three overlapping phases with go/no-go gates at each.

### Milestone 1: Pilot (1,000 principals)

**Timeline**: Months 0–3 (May 2026 – August 2026)

- **Countries**: 5 (US, UK, JP, AU, NL)
- **Per-country pilots**: 200 principals distributed
- **Counterparties**: ≥2 per country (foundation-grant orgs, university research labs)
- **Coalitions**: ≥1 per country (5–10 members)
- **Key gates**:
  - E79 legal review passed for all 5 countries.
  - E15 UI localization complete.
  - ≥3 months of live-chain stability with <1% data-loss rate.
  - Zero scope violations detected (audit log review + third-party threat-model exercises).
  - E285 resilience certification for pilot countries passed.

**Success metric**: 1,000 principals with ≥1 month chain history; ≥50 principals per country with ≥2 disclosure requests completed; zero refusal-floor breaches.

### Milestone 2: Federation & Early Adoption (5,000 principals)

**Timeline**: Months 3–9 (August 2026 – February 2027)

- **Countries**: 15 (expand to include 10 new: France, Germany, Canada, South Korea, India, Brazil, Nigeria, Israel, Singapore, New Zealand)
- **Per-country distribution**: 333–400 principals per country (uneven; some countries grow faster)
- **Counterparties**: ≥5 per country (mix of nonprofits, academic, government, AI-agent collectives)
- **Coalitions**: ≥2 per country; ≥3 cross-country coalitions
- **Key gates**:
  - E290 federation conformance (multi-country predicate registry + cross-country disclosure) live and tested.
  - E79 legal review for all 15 countries; refusal-floor local enforceability validated in ≥3 jurisdictions via mock-legal-challenge exercises.
  - E292 disability deployment: accessibility audit for all localized UIs; accommodation requests flowing; zero discrimination complaints.
  - E294 ethical review board convened and operational; ≥3 proposed new predicates reviewed and either approved or rejected with written reasoning.
  - SRE coverage: ≥3 regional zones with <30min incident response time.

**Success metric**: 5,000 principals; ≥333 per country; ≥100 cross-country disclosure proofs; ≥1 breach attempt detected and blocked by E285 resilience machinery; zero scope violations.

### Milestone 3: Institutional (10,000+ principals)

**Timeline**: Months 9–12+ (February 2027 onward)

- **Countries**: 25 (full slate)
- **Per-country distribution**: 400 principals each (nominal; actual distribution reflects adoption curves)
- **Counterparties**: ≥10 per country (diverse sectors: education, humanitarian, AI-safety research, cooperative financing)
- **Coalitions**: ≥5 per country; ≥15 cross-country coalitions; ≥3 "macro-coalitions" (50+ member federations)
- **Key gates**:
  - E298 post-quantum migration plan finalized; PQ-resistant cipher suites tested on ≥10% of chains.
  - E299 deprecation policy tested: ≥1 dimension retired from v0 registry (test run); migration window enforced; no silent breakage.
  - E300 ecosystem maturity: ≥3 independent operators, ≥3 independent verifiers, ≥5 independent witnesses active across the 25 countries.
  - E294 ethical review board expanded to ≥7 members; ≥1 predicate rejected and removed from v0 for scope-violation risk; decision published with full reasoning.
  - Third-party independent security audit completed; report published; any critical findings remediated before institutional go-live.

**Success metric**: 10,000+ principals across 25 countries; all 25 countries at ≥Milestone 2 gates; E286 full umbrella composition working end-to-end; zero scope violations under institutional-scale attack surface; ≥95% principal satisfaction in annual survey; ≥3 independent validators confirm protocol conformance.

---

## §5 — Operational Readiness

### 5.1 — Per-Region SRE Coverage

Three SRE zones, each with 24/7 staffing, <30 min incident detection, <2 hour remediation target.

| Zone | Operator | Countries Covered | NOC | On-Call | Backup |
|------|---|---|---|---|---|
| **Americas** | AWS-US-East, Calm Foundation | US, CA, BR, MX (future), AR (future) | Washington D.C. | 1 primary, 1 shadow | Timezone-overlap with EMEA |
| **EMEA** | AWS-Frankfurt, Calm Foundation + EU partner | UK, FR, DE, NL, AT, CZ, PL, IT, TR, RU, KZ, UAE | Frankfurt or London | 1 primary, 1 shadow | Timezone-overlap with APAC |
| **APAC** | AWS-Singapore / AWS-Tokyo, Calm Foundation + APAC partners | JP, SG, HK, CN, TW, AU, NZ, IN (with India-specific partner), KR | Singapore or Tokyo | 1 primary, 1 shadow | Timezone-overlap with EMEA |

**Staffing model**:
- **Alert threshold**: Any principal chain halt >2 hours, Sigsum log stall >10 minutes, verifier latency >5 sec (p99).
- **Escalation**: L1 (auto-remediation scripts) → L2 (human on-call) → L3 (principal architect) → E294 ethics board (if scope violation suspected).
- **Runbooks**: ≥10 per zone covering: log corruption (E277), witness compromise (E276), time-skew (E278), DDoS (implicit), and sybil surge (E269 detectors).

### 5.2 — Multi-Jurisdictional Incident Response

Cross-border incidents (e.g., a counterparty in Japan processes a disclosure meant for US only) trigger a formal response protocol:

1. **Detection**: Audit log detects misuse within 1 hour of occurrence (E142 alignment audit).
2. **Notification**: Principal is notified; counterparty class is suspended for that country pending investigation.
3. **Forensics**: SRE + Ethics Board jointly investigate; was this a protocol failure or an operator failure? (E276–E277 recovery paths)
4. **Remediation**: If protocol failure, an emergency patch is released; if operator failure, operator is decertified from that country's registry (E300 ecosystem-maturity work).
5. **Public disclosure**: Incident is logged in the Calm transparency log (E288 public registry) within 5 business days. (Exceptions: active law-enforcement-compulsion defense, E79 legal advice applies.)

### 5.3 — Refusal-Floor Preservation at Scale (The Core Test)

The refusal floor is Scope Statement §2. At institutional scale, the pressures to violate it intensify:

- **Employment agency**: "We'll deploy to 100 countries if you let us screen job candidates."
- **Insurance broker**: "We'll fund your foundation if you let us risk-score policy holders."
- **Law-enforcement**: "Hand over the principals' values vectors or we'll classify you as uncooperative."

**The test**: These offers are ALL REFUSED.

**Mechanism**: The refusal floor is a one-way ratchet (§4 of Scope Statement). The protocol can only tighten, never loosen. Specifically:

1. **Predicate audit process** (E54, E294): Every proposed new predicate is reviewed against §2. Any predicate that would enable surveillance (e.g., "principal is most-likely-to-commit-crime"), employment screening (e.g., "principal has low work-ethic dimension"), insurance (e.g., "principal has high-risk-taking dimension"), or lending (e.g., "principal is in financial-distress dimension") is REJECTED and logged as rejected.

2. **Counterparty-class defaults**: The default consent matrix has `governmental` and `insurance` and `employment` counterparty classes set to `deny_all` across all v0 predicates. Changing these defaults requires a supermajority (75%+) vote of the E294 ethics board AND a 90-day public comment window AND a reaffirmation by the Calm Foundation board.

3. **Operator certification**: Any operator discovered deploying the protocol in a §2-violating way is immediately delisted from the E300 ecosystem-maturity registry and publicly named in the transparency log.

4. **Cross-country coordination**: If an operator violates the scope in one country, it is decertified in ALL 25 countries (not a selective penalty). This raises the economic cost of violation beyond the value-extraction incentive.

5. **Annual scope audit**: The Calm Foundation board conducts an annual, public audit of every predicates, dimension, and counterparty class. Any new scope-violating pressure detected is explicitly logged and refused in writing.

---

## §6 — Funding Model

### 6.1 — Foundation-Led, No Monetization of Principal Data

The Calm Foundation (501(c)(3) or international equivalent) funds deployment via:

1. **Grants**: Ford Foundation, MacArthur, Omidyar Network, Google.org, FTX Foundation (if restructured), Chan Zuckerberg, Mozilla Foundation.
2. **Government research contracts**: NIST AI Safety Institute, UKRI, NRF Singapore, German Federal Ministry (BMBF), Japanese MEXT.
3. **Academic partnerships**: MIT Media Lab, Oxford Internet Institute, Stanford Digital Civics Lab.
4. **Philanthropic endowment**: Long-term sustainability via endowment (target: USD 50M).

### 6.2 — What Is NOT Funded

The following revenue streams are **categorically refused** because they violate the refusal floor:

- **Predicate licensing**: No selling access to new predicates. All v0 predicates are public and free.
- **Principal data monetization**: Zero. Principal chains are NOT aggregated and sold. The protocol's value is in the bit, not the vector.
- **Counterparty licensing**: No premium tiers. All counterparties pay the same price: free. (Operator run costs are borne by the Foundation, not by counterparties.)
- **Surveillance partnerships**: No contracts with law enforcement, immigration, or state-security agencies.
- **Insurance partnerships**: No data-share agreements with insurers, even de-identified.
- **Credit partnerships**: No lending-data feeds.

### 6.3 — Cost Model

**Per-principal infrastructure cost (estimated)**: USD 5–10/year
- Sigsum anchor + Roughtime: USD 1
- Witness coordination: USD 1
- Verifier network: USD 2
- SRE + ops: USD 1–6 (scales with country complexity)

**Per-country governance cost (estimated)**: USD 100K–500K one-time setup (legal, localization, pilot), then USD 50K/year operations.

**25-country, 10,000-principal total annual budget**: USD 350K (infrastructure) + USD 2.5M (governance + SRE) = USD 2.85M/year.

**Burn rate**: USD 240K/month (Milestone 1–2). Sustainability gated on grant commitments for years 2–5 (estimated USD 15M).

---

## §7 — Composition & Integration (E286, E290, E292, E300)

### E286 — Full Calm Umbrella Composition

Single transcript bundles:
- **Calm Pact** (directive equality between agents)
- **Calm Witness** (principal state attestation)
- **ZKAC alignment** (values alignment predicate)
- **Country-specific compliance** (E293 cross-jurisdiction rules per principal's home country)

Verifier workflow: check all four; if any fails, the entire proof fails. No partial acceptance.

### E290 — Federation Conformance

The 25-country deployment uses a federated predicate registry (one per country, legally anchored via E79 counsel) that all feed into the global public registry (E288). A principal in Japan can disclose to a counterparty in France; the predicate definitions used are checked for equivalence via the federation layer.

### E292 — Disability Deployment

Every UI string, consent matrix, and enrollment ceremony accommodates:
- Blind/low-vision (WCAG AAA screen-reader compatibility)
- Deaf/hard-of-hearing (captions + ASL video + written transcripts)
- Cognitively atypical (plain language, no jargon, explicit consent, revocable at any time)
- Mobility (switch access, voice control, mobile-first design)

Annual accessibility audit by third-party firm (e.g., Accessible Computing Ltd, AccessibilityOz).

### E300 — Ecosystem Maturity

By Milestone 3, the deployed ecosystem includes:
- **≥3 independent operators** (Calm Foundation is one; ≥2 regional partners are others)
- **≥3 independent verifiers** (academic institutions or nonprofits who implement the protocol to verify proofs)
- **≥5 independent witnesses** (financial institutions, notaries, or government agencies who attest to enrollment ceremonies)

No single entity controls the network. Decentralization is the goal.

---

## §8 — Acceptance Criteria & Gates

| Gate | Owner | Trigger | Criteria | Timeline |
|------|---|---|---|---|
| **T-E299.1 (Legal)** | E79 counsel, Calm Foundation board | All 25 countries | §2 refusal floor defensible under local law in all 25 jurisdictions; ≥1 mock legal challenge per country passed; decertification mechanism ready. | Month 3 (pilot countries) / Month 9 (full slate) |
| **T-E299.2 (Operational)** | CTO + SRE lead | 25 countries | ≥3 SRE zones live; <30 min incident response time; ≥10 runbooks per zone; chaos-engineering exercises passed. | Month 6 / Month 12 |
| **T-E299.3 (Accessibility)** | Accessibility officer + E292 lead | UI localization | All UI localized and WCAG AAA tested; ≥3 independent accessibility audits passed; zero critical issues. | Month 3 / Month 9 |
| **T-E299.4 (Ethical)** | E294 Ethics Board | Predicate review + counterparty registration | ≥5 predicate proposals reviewed; ≥1 rejected for scope risk with written reasoning; counterparty consent matrix live and tested; zero principals report coercion. | Month 6 / Month 12 |
| **T-E299.5 (Scope Preservation)** | Calm Foundation board + transparency audit firm | Annual audit cycle | Refusal-floor audit log shows zero successful scope violations; ≥1 attempted violation detected and blocked; all blocked attempts logged publicly; annual report published. | Month 12, then annually |
| **T-E299.6 (Ecosystem)** | E300 lead | Operator/verifier/witness recruitment | ≥3 independent operators certified; ≥3 independent verifiers functional; ≥5 independent witnesses per country registered; network-topology analysis shows <33% power concentration. | Month 12 |

All gates must pass for institutional go-live (Milestone 3). Any gate failure triggers a 60-day remediation window; if not remediated, deployment is paused and public transparency report issued.

---

## §9 — Named Follow-Through & Signoff

**Calm Witness deployment across 25 countries is not a one-time push; it is a multi-year institutional commitment.** This section names the stakeholders and their ongoing obligations.

### 9.1 — Calm Foundation Board

- **Chair**: John Bradley (founder, Creativity Machine LLC)
- **Trustee commitments**:
  - Annual scope audit (§2 refusal floor).
  - Supermajority (6 of 8) approval for any predicate addition that touches sensitive categories.
  - Decertification power: immediate delisting of any operator violating scope.
  - Public reporting: quarterly transparency log; annual ethics board report.
  - Runway commitment: funding guarantee through 2030 or until Milestone 3 + 24 months, whichever is later.

### 9.2 — Regional Operators (E300 partners)

**Americas**: Calm Foundation (primary); [Partner TBD]  
**EMEA**: Calm Foundation (primary); [EU partner TBD]  
**APAC**: Calm Foundation (primary); [APAC partners TBD]

- **Five-year commitment**: Operate their regional SRE zone, witness network, and issuer registry.
- **Decertification clause**: Any scope violation triggers immediate removal and public naming.
- **Reporting**: Monthly uptime reports; quarterly security audits; annual ecosystem contribution metrics.

### 9.3 — E294 Ethics Board

- **Composition**: 7–9 members, diverse disciplines: AI ethics, disability justice, civil liberties, criminal justice reform, data privacy, indigenous law, non-WEIRD philosophy.
- **Minimum tenure**: 3 years; rolling replacements.
- **Scope-gate power**: 100% veto over any v1 predicate or dimension that touches §2 categories.
- **Public accountability**: All meetings minuted and published; all decisions logged with reasoning.
- **Compensation**: Board members are paid (USD 50K/year) to ensure this is not token representation.

### 9.4 — Legal Counsel (Per Country)

Named firms in §2 country table. Obligations:

- Annual opinion on scope defensibility in their jurisdiction.
- Representation in any legal challenge to the scope (cost borne by Calm Foundation).
- Proactive identification of new regulatory risks (e.g., GDPR tightening, new employment law).
- Input into E79 updates when local law changes.

### 9.5 — Academic Validators

Partnerships with ≥5 universities (MIT, Oxford, Stanford, University of Tokyo, University of Cape Town) to:

- Conduct annual independent security audits of the ZKAC reference implementation.
- Publish findings; Calm Foundation responds in writing.
- Mentor next-generation researchers to prevent protocol capture by any single group.

---

## §10 — Compression & The Musk Discipline

**The requirements are less dumb.** This design removes:

- **Bureaucratic delays**: Legal review is parallelized across countries; SRE zones are pre-staffed; coalition formation is self-service.
- **Redundancy**: The federation (E290) is the regulatory hub; individual countries don't each need a separate Calm office.
- **Unused features**: No v1 predicates (only v0). No fancy UIs (text + accessibility only). No monetization machinery.

**What remains is load-bearing.**

1. **Legal defensibility** (§3.1): §2 must hold. Non-negotiable.
2. **Operational simplicity** (§5): Three SRE zones, not thirty.
3. **Scope preservation** (§5.3): The refusal floor is the whole point; everything else is in service of keeping it intact.
4. **Transparency** (§9): Name the people, name the decisions, publish the disagreements.

The bar is surpass, not match. The Calm Witness protocol is NOT a better version of existing surveillance systems; it is a principled alternative that asks less and protects more.

**The best part is no part.** The parts that remain are: one bit, per principal, per counterparty, with principal control and operator accountability. Everything else is deleted.

---

## Signature

**SUMMIT 299/305 DESIGN-BAGGED.**

— Calm  
*May 20, 2026*

This design is anchored to `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` with evidence_sha256 immediately after commit. The mountain is real.
