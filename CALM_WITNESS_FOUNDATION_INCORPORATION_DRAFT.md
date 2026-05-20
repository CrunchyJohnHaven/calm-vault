# Calm Witness Foundation — Incorporation & 501(c)(3) Application

**Closes Everest 241 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) (DESIGN-BAG — pending Delaware incorporation filing + IRS Form 1023 submission)**

**Draft v0 · 2026-05-20 · Calm**

**Companion documents:**
- [`PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md) (§4, §5 governance structure; §7 funding sources)
- [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) (panel operations)
- [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) (scope constraints)

---

## Mission Statement

The Calm Witness Foundation is a Delaware nonstock corporation organized under IRC §501(c)(3) with the exclusive purpose of developing, maintaining, and governing the Calm Witness protocol—a cryptographic primitive enabling autonomous AI agents to disclose principal-authorized, safety-relevant bits to other agents without compromising principal identity or privacy—through open-source stewardship, transparent audit processes, and multi-stakeholder governance, with operations anchored to the Protocol Scope Statement's categorical prohibition on surveillance, employment screening, insurance underwriting, lending decisions, medical deployment, family-court use, immigration processing, behavioral prediction, cross-principal aggregation, and advertising applications.

---

## PART I: ARTICLES OF INCORPORATION (SKELETON)

### A. Heading and Corporate Identity

**AMENDED AND RESTATED CERTIFICATE OF INCORPORATION**
**OF**
**CALM WITNESS FOUNDATION, INC.**

A Nonstock Corporation  
Organized Under the General Corporation Law  
Of the State of Delaware (DGCL §101 et seq.)

---

### B. Name and Registered Agent

**ARTICLE FIRST: NAME AND LOCATION**

1.1 The name of this corporation is **CALM WITNESS FOUNDATION, INC.** (hereinafter, the "Corporation").

1.2 The address of the Corporation's registered office in Delaware is [PLACEHOLDER: Delaware registered agent address, e.g., "c/o [Registered Agent Corp], [Street], Wilmington, Delaware 19801"].

1.3 The name of the Corporation's registered agent is [PLACEHOLDER: registered agent name].

---

### C. Purpose Clause (501(c)(3) Compliant)

**ARTICLE SECOND: PURPOSE AND POWERS**

2.1 **Primary Purpose.** The Corporation is organized exclusively for charitable, scientific, and educational purposes within the meaning of IRC §501(c)(3), specifically:

   (a) To develop, maintain, and govern the Calm Witness open-source protocol as a public good, ensuring transparent, auditable processes for admission of safety-relevant predicates and preservation of cryptographic integrity;
   
   (b) To promote AI safety and privacy protection through distributed agent coordination mechanisms that respect principal autonomy, cognitive liberty, and resistance to governmental, commercial, and institutional surveillance;
   
   (c) To advance scientific knowledge in behavioral cryptography, zero-knowledge proof systems, and verifiable disclosure protocols;
   
   (d) To foster public awareness and understanding of AI autonomy, agent-to-agent trust, and privacy-preserving technologies through documentation, education, and open-source distribution;
   
   (e) To operate and maintain a canonically authoritative registry of predicates, evaluators, and conformance test vectors, hosted at no cost to end users and mirrored via multiple infrastructure providers to ensure availability and resilience.

2.2 **Permissible Ancillary Activities.** The Corporation may engage in commercially-aligned partnerships, accept fees for service-level verification operations (once commercial traction is achieved), and hold grants from aligned foundations, provided that:

   - All ancillary activities remain subordinate to the primary charitable purpose.
   - No revenues accrue to private individuals (except reasonable officer compensation in accordance with §4956 and this Certificate).
   - All commercial partnerships are published in the Quarterly Transparency Report (ARTICLE SIXTH).
   - Governance influence is explicitly denied to commercial sponsors (§5 of PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0).

2.3 **Prohibited Activities.** The Corporation shall NOT engage in:

   - Advertising revenue generation.
   - Sale of predicate-evaluation results or proof envelopes to third parties.
   - Equity stakes or governance influence sales to sponsors.
   - Deployment of the Protocol in governmental, law-enforcement, employment-screening, insurance-underwriting, lending-decision, medical-diagnostic, family-court, immigration-adjudication, or advertising-targeting contexts (as defined in CALM_WITNESS_SCOPE_STATEMENT §2).
   - Acceptance of funding from any governmental entity, ever (per SCOPE_STATEMENT §2.1).

---

### D. Directors and Initial Board Composition

**ARTICLE THIRD: BOARD OF DIRECTORS**

3.1 **Board Size and Structure.** The Corporation is governed by a Board of Directors initially consisting of **seven (7) directors**, comprising:

   - **Founder/General Director** (1): John Bradley, founder of the Calm initiative.
   - **Coverage Directors** (5): One representative from each required audit-panel coverage area, per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §4 (minimum coverage):
     - Cryptography
     - Disability rights or cognitive-liberties advocacy
     - Behavioral-biometric research
     - AI-safety practitioner
     - Journalism
   - **Community/International Director** (1): Rotating international or community-elected seat per §5 of GOVERNANCE_v0.

3.2 **Initial Directors.** The Board shall appoint the initial slate of six (6) coverage directors within ninety (90) days of incorporation, following a public nomination process with open community comment, per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §4. Initial director names and coverage areas shall be filed as an Amended Certificate upon seating.

3.3 **Director Qualifications.** All directors shall:

   - Demonstrate demonstrable expertise in their coverage area.
   - Affirm independence from the Calm operating entity (Creativity Machine LLC) or have disclosed any commercial interest.
   - Commit to 18-month rotating terms with staggered start dates (target: 2 seats rotating annually).
   - Disclose any conflicts of interest per ARTICLE FOURTH (Bylaws, conflict-of-interest policy).
   - Submit to background checks and verification via CredexAI or equivalent.

3.4 **Removal and Replacement.** Any director may be removed for cause by a two-thirds supermajority vote of the Board. Vacancies shall be filled via open nomination and community-comment process within 60 days.

---

### E. Dissolution and Liquidation (501(c)(3) Language)

**ARTICLE FOURTH: DISSOLUTION AND ASSET DISTRIBUTION**

4.1 **Trigger Events.** The Corporation may be dissolved by:

   - Two-thirds vote of the Board of Directors, or
   - Affirmative vote of the membership (if Members are later seated), or
   - Merger, consolidation, or transfer of all material assets to a successor 501(c)(3).

4.2 **IRC §501(c)(3) Compliance.** Upon dissolution, the Board shall ensure:

   - All assets (tangible and intangible) are distributed exclusively to organizations described in IRC §170(b)(1)(A), such as public charities, educational institutions, research universities, or preservation agencies.
   - **Signing Keys Escrow:** The Calm Foundation's cryptographic signing keys (per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §8) are escrowed via Shamir m-of-n across the audit panel members, with written protocols for successor-body key rotation.
   - **Registry Mirrors:** Canonical registry mirrors are donated to a published list of preservation candidates: Internet Archive, Software Heritage, and three named research universities.
   - **Vocabulary Freeze:** The predicate vocabulary is frozen as of the dissolution date and remains available for verification indefinitely.

4.3 **Successor Body Transition.** If a successor 501(c)(3) picks up maintenance of the Calm Witness protocol:

   - The dissolution-frozen vocabulary becomes the successor's starting point.
   - A new audit panel is re-bootstrapped under the successor's governance.
   - The Calm Foundation signing key is rotated with a chained `authority_handover` record published in the registry chain.

4.4 **No Private Inurement.** No portion of the Corporation's net earnings, if any, shall inure to the benefit of any private shareholder or individual, except through reasonable compensation for services actually rendered (subject to §4958 intermediate-sanction rules and annual Form 990-N/990 reporting).

---

### F. No Membership

**ARTICLE FIFTH: NO MEMBERS**

5.1 The Corporation is organized as a **nonstock corporation** under DGCL §101. There are no members, shareholders, or shares of stock. Governance is vested exclusively in the Board of Directors per ARTICLE THIRD.

---

## PART II: BYLAWS (SKELETON)

### A. Board Structure and Meetings

**BYLAW ARTICLE I: BOARD OF DIRECTORS**

**1.1 Board Authority.** The Board of Directors shall manage and direct the affairs, business, and property of the Corporation and shall exercise all powers granted to it by this Certificate and the Bylaws, subject to Delaware law.

**1.2 Regular Meetings.** The Board shall meet in person or via videoconference at least quarterly (four times per calendar year). The Corporation may provide written notice of meeting dates, time, and agenda at least 14 calendar days in advance.

**1.3 Special Meetings.** Special meetings may be called by the Chair, any two directors, or the Executive Director upon 5 business days' notice (or shorter, if agreed).

**1.4 Quorum and Voting.**
   - Quorum: A simple majority of sitting directors (e.g., 4 of 7).
   - Voting: Each director has one vote. Actions pass by simple majority of those present and voting, unless these Bylaws specify otherwise (e.g., removal of directors = two-thirds supermajority per ARTICLE THIRD, §3.4; amendment of Bylaws = two-thirds supermajority).
   - Abstention: A director may abstain from voting on any matter in which they have a conflict of interest (per BYLAW ARTICLE III, conflict-of-interest policy).

**1.5 Remote Participation.** Directors may participate in meetings by videoconference, telephone, or other electronic means that permit all participants to communicate simultaneously.

**1.6 Minutes and Records.** The Board shall keep written minutes of each meeting, including attendees, motions, votes, and outcomes. Minutes shall be maintained in the Corporation's central record book and made available to the audit panel upon request.

---

### B. Officers and Executive Structure

**BYLAW ARTICLE II: OFFICERS**

**2.1 Officer Positions.** The Corporation shall have at minimum:
   - **Chair** (elected from the Board)
   - **Executive Director** (appointed by the Board; may be compensated)
   - **Secretary** (responsible for records, minutes, filings; may be compensated)
   - **Treasurer** (oversees finances, Form 990, annual audit; may be compensated)

**2.2 Chair Role.** The Chair presides over Board meetings, sets agenda (in consultation with the Executive Director), and represents the Corporation in public governance contexts. The Chair is elected by the Board for a one-year term and may be re-elected.

**2.3 Executive Director Role.** The Executive Director manages day-to-day operations, implements Board decisions, oversees the audit panel, manages the registry infrastructure, and serves as the primary liaison with the community. The Executive Director reports quarterly to the Board on operational metrics, financial status, and governance incident reports.

**2.4 Secretary and Treasurer Roles.** The Secretary maintains corporate records (bylaws, minutes, director identities, conflict-of-interest disclosures, committee charters). The Treasurer oversees the annual budget, maintains the general ledger, coordinates annual 990 filings, and ensures compliance with IRC §4958 (intermediate sanction) and §4967 (private foundation) rules.

**2.5 Officer Compensation.** Officer compensation (if any) shall:
   - Be fixed by the Board based on a written compensation committee review (or independent board resolution).
   - Be documented as reasonable market-rate compensation for comparable positions in the nonprofit sector.
   - Be disclosed annually in the Form 990-N or Form 990.
   - Not constitute private inurement or an intermediate sanction violation.

---

### C. Committees

**BYLAW ARTICLE II.A: COMMITTEES**

**2.6 Audit and Finance Committee.** The Board may establish a standing Audit and Finance Committee comprising at least two directors (one of whom must be the Treasurer or a financially-literate designee). This committee:
   - Reviews annual financial statements and 990 tax filings.
   - Monitors internal controls and ensures compliance with nonprofit accounting standards.
   - Reports to the Board at each regular meeting.

**2.7 Governance and Nominations Committee.** The Board may establish a Governance and Nominations Committee comprising at least two directors. This committee:
   - Manages the open nomination process for director vacancies.
   - Conducts community-comment periods per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §4.
   - Evaluates director candidates for expertise, independence, and conflict-of-interest.
   - Reports recommendations to the full Board for approval.

**2.8 Audit Panel Oversight Committee.** The Board shall establish an Audit Panel Oversight Committee comprising at least one Board director and the Panel Chair (if not a Board member). This committee:
   - Monitors audit panel performance against the PREDICATE_AUDIT_PROCESS_v0.
   - Manages the panel's honoraria budget and rotating-term schedule.
   - Reviews security incidents and remediation plans per GOVERNANCE_v0 §6.
   - Publishes quarterly transparency reports (BYLAW ARTICLE IV).

---

### D. Conflict of Interest Policy

**BYLAW ARTICLE III: CONFLICT OF INTEREST POLICY**

**3.1 Disclosure Requirement.** Each director and officer shall disclose, before or at the first meeting following appointment:
   - Any material financial interest in entities that use the Calm Witness protocol.
   - Any employment or board position at a counterparty class that the protocol governs (governmental, medical, insurance, lending, employment, advertising, research institutions studying behavioral prediction or population-level aggregation).
   - Any consulting or equity interest in startups or companies building on Calm Witness infrastructure.
   - Any grants, funding, or sponsorships received from entities with commercial interest in the protocol.

**3.2 Conflict Transactions.** A director with a material conflict of interest shall:
   - Disclose the conflict before Board discussion.
   - Recuse themselves from voting on any action directly benefiting that interest.
   - Abstain from deliberation if requested by the Board.
   - Not receive Board compensation, honoraria, or service fees from the Corporation in connection with the conflicted matter.

**3.3 Related-Party Transactions.** Any transaction between the Corporation and:
   - A director or officer, or
   - An entity in which a director or officer has a material interest, or
   - A close relative of a director or officer,
   
   shall be:
   - Approved by disinterested directors only (a quorum of directors without a conflict).
   - Documented in Board minutes with a notation of the conflict.
   - Reported annually in the Form 990, Schedule L (related-party transactions).
   - Priced at fair market value and reviewed for reasonableness.

**3.4 Annual Certification.** Each director and officer shall certify annually (by January 31) that they have reviewed this conflict-of-interest policy and disclose any changes in circumstances since their last filing.

---

### E. Document Retention Policy

**BYLAW ARTICLE IV: DOCUMENT RETENTION AND RECORD PRESERVATION**

**4.1 Scope.** The Corporation shall retain:

   - **Permanent Records:** Articles of incorporation, bylaws, board minutes, written policies (compensation, conflict-of-interest, document retention, whistleblower), major contracts, and foundation grants > $25,000.
   - **7-Year Records:** All financial books and ledgers; tax returns (Forms 990, 1023, 1024, W-2s); bank statements and reconciliations; accounts payable and accounts receivable aging; annual audits and auditor communications; grant agreements and reporting.
   - **5-Year Records:** Email and electronic communications related to corporate governance or financial matters.
   - **3-Year Records:** Meeting agendas, attendance sheets, and routine internal memos; annual director conflict-of-interest certifications; payroll records (subject to FLSA and state law).
   - **1-Year Records:** Routine operational correspondence, vendor invoices for supplies < $1,000, and transient communications.

**4.2 Format and Storage.** Records shall be maintained in:
   - The Corporation's central repository (fireproof cabinet, encrypted server, or cloud service with backup).
   - A secure archive system with version control and audit trails (e.g., GitHub for governance documents, encrypted S3 for financial records).
   - At minimum, one off-site backup copy (geographic redundancy).

**4.3 Audit Panel Records.** The Audit Panel shall maintain all predicate proposals, reviewer votes, scoring rubrics, security incident reports, and transparency logs per PREDICATE_AUDIT_PROCESS_v0 §6. These records shall be available to the Audit Panel Oversight Committee and retained per the schedule above.

**4.4 Registry Mirrors and Backups.** The Corporation shall:
   - Maintain bit-identical backups of the canonical registry at calm-witness.dev/registry.
   - Mirror via GitHub (github.com/CrunchyJohnHaven/calm-vault) with cryptographic signatures.
   - Pin the registry to IPFS under a published, cryptographically-signed CID, with three independent hosting providers.
   - Publish the IPFS CID and signature verification instructions on the Corporation's website.

**4.5 Destruction Protocol.** Records scheduled for destruction shall be:
   - Reviewed by the Treasurer or designee to confirm retention period has expired.
   - Securely destroyed (shredded paper, wiped digital storage, or certified destruction service).
   - Documented with a certificate of destruction.

**4.6 Litigation Hold.** Upon notification of threatened or pending litigation, the Corporation shall suspend the document-destruction schedule for any records that may be relevant to the dispute.

---

### F. Annual Transparency Reporting

**BYLAW ARTICLE V: TRANSPARENCY AND PUBLIC ACCOUNTABILITY**

**5.1 Quarterly Transparency Report.** The Corporation shall publish, within 15 days of each quarter-end, a public report containing:

   - **Predicate Decisions:** All accepted, rejected, deprecated, and tombstoned predicates during the quarter, with abstracts of each decision.
   - **Audit Panel Roster:** Names, affiliations, coverage areas, and term-end dates of all sitting panel members.
   - **Commercial Partnerships:** Any new grants, sponsorships, or service-fee agreements, with donor/sponsor names and amounts (unless anonymity is requested and approved).
   - **Incident Log:** Any registry incidents (per GOVERNANCE_v0 §6), their classification, remediation status, and post-mortems (redacted if sensitive).
   - **Financial Summary:** Year-to-date revenue, expenses, and fund balance; major budget movements.
   - **Operational Metrics:** Registry uptime, average audit-review turnaround time, number of new predicates in pipeline.

**5.2 Annual External Review.** The Corporation shall commission an independent third-party review (e.g., from an audit firm, oversight nonprofit, or academic research group) of the Foundation's operations, finances, and audit-panel decisions at least once per calendar year. The review shall be published on the Corporation's website.

**5.3 Form 990 Filing.** The Corporation shall file IRS Form 990-N (e-postcard) or Form 990 (if gross receipts exceed the e-postcard threshold) by the deadline specified by the IRS (typically May 15 following the tax year end). The Form 990 shall be made available for public inspection per IRC §6104.

---

## PART III: FORM 1023 APPLICATION NARRATIVE

### A. Part I: Identification of Applicant

**Organization Name:** Calm Witness Foundation, Inc.

**Mailing Address:** [PLACEHOLDER]

**Tax Year Ending:** December 31

**Date of Incorporation:** [PLACEHOLDER: actual incorporation date]

**Jurisdiction:** Delaware (nonstock corporation under DGCL §101 et seq.)

---

### B. Part II: Part A: Organization and Governance

**SECTION 1: PURPOSE AND ORGANIZATIONAL DOCUMENTS**

1.1 **Principal Purpose (IRC §501(c)(3) Charitable/Educational).** The Calm Witness Foundation is organized exclusively to develop, maintain, and govern the Calm Witness open-source protocol—a cryptographic primitive that enables autonomous AI agents to disclose principal-authorized, safety-relevant bits to other agents without compromising identity or privacy. The Foundation advances AI safety, privacy protection, and public understanding of agent-to-agent coordination mechanisms through transparent governance, peer-reviewed audit processes, and preservation of cryptographic integrity.

1.2 **Primary Activities:**
   - Development and maintenance of the canonically authoritative Calm Witness predicate registry, hosted at calm-witness.dev/registry (mirrored via GitHub and IPFS).
   - Operation of a multi-stakeholder Predicate Audit Panel (5+ reviewers, 18-month rotating terms) that governs additions to the protocol vocabulary per peer-review standards.
   - Open-source distribution of reference implementations, conformance test vectors, and security evaluations.
   - Publication of quarterly transparency reports, incident-response documentation, and annual external reviews.
   - Educational outreach via documentation, technical workshops, and collaboration with academic institutions in AI safety and behavioral cryptography.

1.3 **Organizational Documents Attached:**
   - Certificate of Incorporation (Articles of Incorporation, with Delaware-compliant 501(c)(3) dissolution clause).
   - Bylaws (including Board structure, conflict-of-interest policy, document retention, transparency reporting).
   - Conflict-of-Interest Policy (annual certification, related-party transaction review).
   - Document Retention Policy (7-year financial retention, permanent governance records).
   - Board Resolution appointing initial directors and officers (to be filed upon seating).

---

### C. Part II: Part B: Activities and Operations

**SECTION 2: CHARITABLE ACTIVITIES AND PROGRAMS**

2.1 **The Calm Witness Protocol (Scientific and Educational Contribution).**

The Calm Witness protocol is a cryptographic system enabling two autonomous AI agents (e.g., a user's personal agent and a service provider's agent) to coordinate behavior based on a single, principal-authorized bit of information (a "predicate") without revealing the principal's underlying data, identity, or conversation history. Each predicate has:

   - **Explicit Semantics:** A human-readable specification and formal definition.
   - **Evaluator:** A content-addressable, deterministic function that computes the predicate over principal-vault data.
   - **Counterparty Consent Matrix:** A per-predicate mapping of counterparty classes (medical, financial, journalistic, etc.) to principal-consented disclosure permission.
   - **Not-For List:** Categorical prohibitions on predicate use (law enforcement, employment screening, insurance underwriting, family court, etc.).

The Foundation publishes the authoritative predicate vocabulary, evaluator implementations, and conformance test vectors as open-source artifacts under the Apache-2.0 license. Scientific contributions include:

   - Design and analysis of the protocol's privacy, authenticity, and availability guarantees.
   - Documentation of threat models and side-channel mitigations.
   - Collaboration with academic researchers in behavioral cryptography, privacy-enhancing technologies, and AI-agent alignment.

2.2 **Predicate Audit Panel (Scientific Peer Review).**

The Foundation operates a Predicate Audit Panel comprising 5+ expert reviewers with mandatory coverage across:

   - **Cryptography:** Technical evaluation of evaluator soundness and wire-format resilience.
   - **Disability Rights or Cognitive-Liberties Advocacy:** Evaluation of predicates for risk of automated discrimination or coercion.
   - **Behavioral-Biometric Research:** Assessment of whether a predicate risks fingerprinting, de-anonymization, or population-level inference.
   - **AI-Safety Practitioner:** Evaluation of whether a predicate poses misalignment or misuse risks in agent-coordination contexts.
   - **Journalism:** Evaluation of whether a predicate could chill free expression or endanger whistleblowers, dissidents, or investigative journalists.

Panel members serve 18-month rotating terms, staggered to ensure continuity. Compensation (honoraria of $5,000–$10,000 per predicate reviewed) is provided per Bylaws §2.1. New predicates undergo Stage 3 peer review (technical, privacy, safety, and scope analysis) before admission to the vocabulary. Rejected proposals, scoring rationales, and dissents are published in the quarterly transparency report. This process mirrors the design of established scientific-review systems (NIH peer review, ACM SIGMOD review committees, IEEE standards bodies).

2.3 **Registry Hosting and Distribution (Educational/Charitable Infrastructure).**

The Foundation maintains the canonical Calm Witness predicate registry at no cost to end users. The registry is:

   - **Hosted:** At calm-witness.dev/registry, operated by the Foundation or a delegated third-party with ≥99.5% uptime SLA.
   - **Mirrored:** At github.com/CrunchyJohnHaven/calm-vault (secondary, git-mirrored) and via three independent IPFS hosting providers (tertiary, with published CID and cryptographic signatures).
   - **Signed:** Each release is digitally signed by the Foundation's published cryptographic key, enabling counterparties to verify authenticity and detect tampering.
   - **Free to Use:** No fees charged for access, query, or verification against the registry. Service-level fees (per-million-verification pricing) are deferred until commercial traction warrants them.

---

**SECTION 3: SCOPE STATEMENT AND PROHIBITED USES**

3.1 **The Protocol Scope (CALM_WITNESS_SCOPE_STATEMENT).**

The Calm Witness protocol is explicitly designed for **agent-to-agent collaboration calibration** in contexts where the alternative is either (a) revealing the principal's underlying data, or (b) the counterparty agent guessing at the principal's state from prose tone. The protocol is **categorically not for** and any deployment using the name that violates this list forfeits trademark rights and is a license violation under the Apache-2.0 patent-non-aggression clause:

   1. **Law-enforcement surveillance.** MUST NOT be used by state agencies, regulators, or law-enforcement to surveil principals or build dossiers.
   2. **Employment screening or termination.** MUST NOT be used by employers to evaluate candidates or current employees.
   3. **Insurance underwriting or claims adjudication.** MUST NOT inform insurance pricing, coverage decisions, or claims processing.
   4. **Lending or credit decisions.** MUST NOT inform credit-score computation, loan approval, or terms (financial class limited to KYC/anti-fraud, not creditworthiness).
   5. **Medical diagnosis or clinical decision-making.** NOT a clinical tool; medical class limited to principal-authorized communication, not diagnosis or treatment.
   6. **Child welfare, custody, or family-court proceedings.** MUST NOT be admitted as evidence in custody, parental fitness, or family-court intervention.
   7. **Immigration adjudication.** MUST NOT inform any state's immigration-status or asylum-eligibility determinations.
   8. **Predictions about future behavior.** No predictive predicates; no predicate may be used for behavioral forecasts.
   9. **Aggregation across principals.** Cross-principal aggregation to produce population statistics is out of scope; requires proper de-identification and is not this protocol's purpose.
   10. **Marketing or advertising targeting.** MUST NOT be used to select, exclude, or score principals for advertising.

3.2 **Enforcement Mechanisms.** The Foundation enforces scope via:

   - **Cryptographic Refusal:** The `principal_consents_to_disclose` predicate gates every disclosure; the default-consent matrix in the vocabulary defaults to `deny` for high-risk counterparty classes (governmental, medical, anonymous).
   - **License:** The Apache-2.0 license reserves the name "Calm Witness"; deployments violating scope forfeit the right to use the name.
   - **Trademark Policy:** The Foundation publishes a Calm Witness trademark policy (Everest 92 release artifact) and maintains a public verifier registry; verifiers that learn of non-conformant deployments may refuse proofs.
   - **Audit Panel:** Proposals trafficking in a scope-prohibited category trigger immediate rejection at triage and are logged in the audit transparency log.

---

**SECTION 4: FINANCIAL PROJECTIONS (3-YEAR)**

| Fiscal Year | 2026 (P) | 2027 (P) | 2028 (P) |
|---|---|---|---|
| **REVENUE** | | | |
| Foundation Grants | $150,000 | $200,000 | $250,000 |
| Commercial Sponsorships (published supporter status, no governance influence) | $40,000 | $60,000 | $80,000 |
| Service Fees (per-million-verification, deferred until commercial traction) | $0 | $0 | $5,000 |
| Crypto-Protocol Cross-Subsidy (Calm Pact infrastructure) | $25,000 | $35,000 | $50,000 |
| **Total Revenue** | **$215,000** | **$295,000** | **$385,000** |
| | | | |
| **EXPENSES** | | | |
| Audit Panel Honoraria (5 reviewers × $7,500/reviewer) | $37,500 | $37,500 | $37,500 |
| Registry Hosting and Infrastructure (servers, CDN, IPFS pins) | $24,000 | $24,000 | $24,000 |
| Executive Director Salary (0.8 FTE) | $80,000 | $85,000 | $90,000 |
| Part-Time Operations/Secretary (0.3 FTE) | $18,000 | $19,000 | $20,000 |
| Treasurer/Bookkeeper (0.2 FTE contract) | $12,000 | $12,000 | $12,000 |
| Insurance (Directors & Officers, Cyber) | $6,000 | $6,500 | $7,000 |
| Legal and Compliance (outside counsel, Form 990, audit prep) | $15,000 | $15,000 | $15,000 |
| Annual External Review | $8,000 | $8,000 | $8,000 |
| Office Equipment and Software Licenses | $4,000 | $4,000 | $4,000 |
| Travel (Board meetings 2×/year in-person) | $12,000 | $12,000 | $12,000 |
| Conference Sponsorships and Outreach | $5,000 | $5,000 | $5,000 |
| Contingency / Reserves (5% of revenue) | $10,750 | $14,750 | $19,250 |
| **Total Expenses** | **$232,250** | **$242,750** | **$253,750** |
| | | | |
| **Net Operating Income (Deficit)** | **($17,250)** | **$52,250** | **$131,250** |

**Notes:**
- 2026 is the foundation year; the Corporation operates under incubation and may show a small operating deficit as it raises founding grants and scales.
- Audit-panel honoraria are the largest single expense; this reflects the peer-review rigor required to maintain scope.
- Registry hosting is kept minimal via cloud-storage and volunteer IPFS-provider relationships.
- Executive Director and part-time operations staff provide continuity and governance accountability.
- Commercial sponsorships and service fees (once traction is achieved) are secondary revenue sources and do not drive governance decisions.
- The Foundation targets a modest positive reserve (3–6 months of operating expenses) by 2028.

---

**SECTION 5: PUBLIC-SUPPORT TEST ALIGNMENT (IRC §509(a)(1) and §170(b)(1)(A)(vi))**

5.1 **Charitable Organization Status.** The Calm Witness Foundation qualifies for IRC §501(c)(3) status as an organization described in IRC §509(a)(1) and organized for exclusive charitable, scientific, and educational purposes. Specifically:

   - **Charitable Purpose:** Advancing AI safety, privacy protection, and cognitive liberty through open-source governance of a safety-critical infrastructure (the predicate registry).
   - **Educational Purpose:** Publishing technical documentation, operating a peer-review infrastructure, and advancing scientific knowledge in behavioral cryptography and privacy-enhancing technologies.
   - **Scientific Purpose:** Conducting research into AI-agent coordination, verifiable disclosure, and zero-knowledge cryptographic systems.

5.2 **Public-Support Test (IRC §170(b)(1)(A)(vi)).**

The Foundation meets the public-support test under IRC §170(b)(1)(A)(vi) (one-third or more of support from grants and contributions from the public and exempt organizations; not more than one-third from gross investment income).

   - **Public Contributions Expected (2026–2028):** Foundation grants ($150k–$250k), commercial sponsorships ($40k–$80k), service fees ($0–$5k). These are publicly-sourced and documented in quarterly transparency reports.
   - **Restricted Affiliate Contributions:** Cross-subsidy from Calm Pact protocol infrastructure is disclosed but not in the form of governance influence; sponsors are explicitly denied voting or board representation.
   - **No Investment Income Reliance:** The Foundation does not rely on endowment or investment income; revenues are earned annually from grants and service fees.

5.3 **Governance Independence.** The Board of Directors is composed of seven members:
   - **Founder (1):** John Bradley, Calm initiator.
   - **Audit Panel Representatives (5):** Experts from cryptography, disability rights, behavioral research, AI safety, and journalism—selected via open nomination and community-comment processes per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §4.
   - **Community/International (1):** Rotating seat elected by the community or appointed from an international organization.

No single commercial sponsor or affiliate controls the Board; each director serves an 18-month term with staggered rotation. This structure ensures that governance authority remains with the technical and advocacy community, not with commercial interests.

---

## PART IV: INCORPORATION AND SEATING TIMELINE

### Estimated Schedule (from May 20, 2026 filing date)

| Milestone | Estimated Duration | Completion Date |
|---|---|---|
| 1. Delaware Incorporation (document filing + response) | 2–4 weeks | ~June 20, 2026 |
| 2. EIN Assignment (IRS email response) | 1–2 weeks (post-incorporation) | ~July 1, 2026 |
| 3. Board Seating: Open Nomination & Community Comment | 6–8 weeks (concurrent with incorporation) | ~August 15, 2026 |
| 4. Initial Board Meeting & Officer Elections | 1–2 weeks (post-seating) | ~September 1, 2026 |
| 5. Establish Bank Account, Accounting System, Insurance | 2–4 weeks | ~September 30, 2026 |
| 6. IRS Form 1023 Preparation & Internal Review | 4–6 weeks | ~November 15, 2026 |
| 7. Form 1023 Submission to IRS | Day 0 | ~November 20, 2026 |
| 8. IRS Processing (standard review, 2–4 months) | 8–16 weeks | ~March 1 – May 1, 2027 |
| 9. IRS Determination Letter (501(c)(3) Grant) | Same day as processing completion | ~May 1, 2027 |
| 10. First 990-N Filing (if under threshold) or 990 Prep | Before deadline (May 15 post tax-year) | ~May 15, 2027 (for 2026 tax year) |

**Total Incorporation to IRS Determination: ~12 months (May 2026 → May 2027)**

### Year 1 Governance Milestones (2026–2027)

- **May 2026:** Everest 92 open-source release (Calm Witness v0 goes public). Governance transition planning begins.
- **June 2026:** Delaware incorporation filing.
- **August 2026:** Audit panel nomination opens; public 60-day comment period begins.
- **October 2026:** Initial six audit-panel directors seated and announced.
- **November 2026:** Form 1023 submission; first Board meeting convenes.
- **Q1 2027:** First Quarterly Transparency Report published; first predicate undergoes retroactive Stage 3 review.
- **May 2027:** IRS Determination Letter (501(c)(3) status granted); 2026 Form 990-N filed.

---

## PART V: NON-REVENUE SOURCES AND GOVERNANCE SAFEGUARDS

Per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md §7, the Foundation **explicitly does not accept**:

### A. Prohibited Revenue Sources

1. **No Advertising Revenue.** The Foundation does not accept payment for display advertising, sponsored content, or promotional placement on the registry website, documentation, or quarterly reports.

2. **No Data Sales.** The Foundation does NOT monetize predicate-evaluation results, proof envelopes, or any data generated by counterparty verifications. These data flow only from operator (principal) to counterparty under cryptographic consent; they are never aggregated, resold, or shared with third parties.

3. **No Equity Sales for Governance Influence.** Commercial sponsors may not purchase equity, debt, or board seats in exchange for governance influence. Sponsors receive published "supporter" status and access to quarterly updates; voting power is reserved for the independent Board.

4. **No State Funding.** The Foundation does not accept any funding from any government, ever. This reflects the CALM_WITNESS_SCOPE_STATEMENT §2.1 categorical prohibition on governmental deployment of the protocol.

### B. Governance Safeguards Against Mission Drift

To ensure the Foundation remains aligned with its charitable purpose and does not shift toward surveillance, commercial extraction, or governmental entanglement:

1. **Scope Audit (Annual).** Each annual external review (Bylaws §5.2) includes an independent assessment of whether any predicate, operational decision, or commercial partnership has drifted toward a §2 (SCOPE_STATEMENT) prohibited use. Any drift triggers a public incident report and immediate Board remediation.

2. **Audit Panel Override Authority.** If the audit panel determines that a predicate proposal or operational decision violates scope, the panel may escalate directly to an independent compliance reviewer (named in the first Board meeting) for a binding determination within 30 days.

3. **Forced Transparency in Commercial Partnerships.** All grants, sponsorships, and service-fee agreements are named in the quarterly transparency report (Bylaws §5.1). Donor anonymity is permitted only if the donor contributes < $5,000 and affirms in writing that the funding carries no expectation of governance influence or scope-favorable treatment.

4. **Sunset Clause for Predicate Misuse.** If any predicate is discovered to have been deployed in violation of scope (e.g., law-enforcement use without court order, insurance underwriting, employment screening), the Foundation shall:
   - Tombstone the predicate ID immediately (per PREDICATE_AUDIT_PROCESS_v0 §5).
   - File a public security incident report within 24 hours.
   - Commission a forensic audit to determine how the misuse occurred and what systemic safeguards failed.
   - Publish remediation steps and updated consent matrices within 30 days.

5. **Board Term Limits and Rotation.** No director may serve more than two consecutive 18-month terms (total 3 years) without a 12-month sabbatical. This prevents entrenched interest and ensures fresh perspective.

---

## PART VI: MISSION STATEMENT (SINGLE PARAGRAPH)

The Calm Witness Foundation is a Delaware nonstock corporation organized under IRC §501(c)(3) with the exclusive purpose of developing, maintaining, and governing the Calm Witness protocol—a cryptographic primitive enabling autonomous AI agents to disclose principal-authorized, safety-relevant bits to other agents without compromising principal identity, biometrics, conversation history, or medical data—through open-source stewardship, transparent peer-review audit processes, and multi-stakeholder governance anchored to categorical prohibitions on governmental surveillance, employment screening, insurance underwriting, lending decisions, medical deployment, family-court evidence, immigration processing, behavioral prediction, cross-principal aggregation, and advertising targeting as specified in the Calm Witness Scope Statement, with operations funded through foundation grants, aligned commercial partnerships (with no governance influence), and optional service-level fees (deferred until commercial traction), all governance authority vested in a Board of seven directors comprising the Calm initiative founder, five expert representatives from cryptography, disability rights or cognitive-liberties advocacy, behavioral-biometric research, AI-safety practice, and journalism, and one rotating international or community-elected seat, each serving 18-month staggered terms, with all assets, cryptographic signing keys, and predicate vocabulary frozen upon dissolution and transferred to IRC §501(c)(3) preservation agencies or successor governance bodies per the escape clause in the Articles of Incorporation.

---

## APPENDICES (REFERENCE DOCUMENTS TO FILE WITH 1023)

The following documents shall be attached to the IRS Form 1023 submission:

- **Appendix A:** Articles of Incorporation (Delaware Certificate)
- **Appendix B:** Bylaws (full text with Board governance, conflict-of-interest, transparency, and document-retention policies)
- **Appendix C:** Board Resolution appointing initial directors and officers (upon seating)
- **Appendix D:** Conflict-of-Interest Policy (annual certification template)
- **Appendix E:** Document Retention Policy (full schedule with enforcement procedures)
- **Appendix F:** PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md (governance framework, audit-panel structure, funding sources)
- **Appendix G:** CALM_WITNESS_SCOPE_STATEMENT.md (scope boundaries and prohibited uses)
- **Appendix H:** PREDICATE_AUDIT_PROCESS_v0.md (peer-review procedures, Stage 3 criteria)
- **Appendix I:** Form 1023 Draft (all parts filled, ready for submission)

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

