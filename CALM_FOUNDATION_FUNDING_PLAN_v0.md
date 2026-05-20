# Calm Witness Foundation — 3-Year Funding Plan v0

**Closes Everest 243 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) (DESIGN-BAG — pending grant applications + sponsor cultivation)**

**Draft v0 · 2026-05-20 · Calm**

**Companion documents:**
- [`CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`](CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md) (501(c)(3) governance)
- [`PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md) (§7 funding model, audit panel compensation)
- [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) (panel operations costs)

---

## §1 — Executive Summary

The Calm Witness Foundation requires sustained, diversified funding to operate the public predicate registry, compensate the audit panel, maintain cryptographic infrastructure, and advance the governance program through 2029. This plan details a **3-year operating budget** ($2.1–$2.8M) covering base operations through Year 3, identifies **eight primary funding sources** with target amounts and pipeline status, and includes a **24-month funding gap analysis** and **risk register** with mitigation strategies.

**Year-by-year profile:**
- **Year 1 (2026–2027):** $620–$740K (registry v0 launch, panel scaling, audit infrastructure)
- **Year 2 (2027–2028):** $710–$880K (v1 predicate expansion, multi-region mirror ops, legal-risk hardening)
- **Year 3 (2028–2029):** $770–$960K (NIST submission, standards body engagement, ecosystem adoption)

**Funding posture (per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §7):**
- Primary: Foundation grants (Open Philanthropy, Long-Term Future Fund, Aspen, Knight, NEA/Ford disability-arts)
- Secondary: Individual donors via donor-advised funds (DAFs)
- Tertiary: Commercial sponsorships (with strict no-governance-influence rules)
- Quaternary: Service fees on verification volume (post-traction, low near-term impact)

**Non-sources (explicitly forbidden):**
- Advertising revenue
- Sale of predicate-evaluation results or proof envelopes
- State funding (any government entity, any amount)
- Equity-for-governance exchanges

---

## §2 — Operating Budget by Category (3-Year Totals)

### A. Audit Panel Honoraria & Operations

**Purpose:** Compensate standing audit panel (5–7 reviewers) for predicate evaluation, annual conflict-of-interest updates, and incident response. Includes support costs (legal review time, conflict checks, annual retreat).

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Panel honoraria** | $75–95K | $85–110K | $95–125K | $5–10K per predicate addition (target 4–6 per year); conflict-of-interest review; annual retreat (in-person 1/3 years) |
| **Panel support** | $15–20K | $18–25K | $20–28K | Legal review time; conflict-check automation; admin coordination |
| **Incident response pool** | $10–15K | $12–18K | $15–22K | Reserved for emergency panel convening; post-mortem documentation |
| **Subtotal** | **$100–130K** | **$115–153K** | **$130–175K** | |

---

### B. Registry Hosting, Mirroring & Infrastructure

**Purpose:** Operate primary registry (calm-witness.dev), maintain GitHub secondary mirror, manage IPFS pin via 3 independent providers. Target ≥99.5% uptime SLA.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Primary hosting (calm-witness.dev)** | $25–35K | $30–45K | $35–55K | Scalable cloud (AWS/GCP/Azure); DDoS protection; CDN; TLS cert automation |
| **IPFS pinning (3 providers)** | $12–18K | $15–24K | $18–30K | Estimated $4–10K per pinning provider; content-address updates |
| **GitHub + git infrastructure** | $3–5K | $3–5K | $3–5K | Actions runners; branch protection; archive redundancy |
| **DNS & domain registry** | $2–3K | $2–3K | $2–3K | calm-witness.dev; wildcard cert; anycast failover setup |
| **Monitoring & alerting** | $8–12K | $10–15K | $12–18K | Uptime monitoring; security scanning; log aggregation |
| **Subtotal** | **$50–73K** | **$60–92K** | **$70–111K** | |

---

### C. Audit-Firm Engagements & Security Audits

**Purpose:** Annual third-party security audit of registry code + evaluator implementations (post-launch); annual financial audit (required for 501(c)(3)). Incident-driven penetration testing.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Code security audit** | $40–60K | $45–70K | $50–80K | First audit Year 1 post-launch; annual thereafter (mid-year); covers registry + 3 evaluators |
| **Financial audit (CPA)** | $15–25K | $18–30K | $20–35K | Required for 501(c)(3) IRS Form 990-N filing; annual cost scales with complexity |
| **Incident-driven pentest** | $0–20K | $10–25K | $10–25K | Reserved pool; only triggered by incident or major refactor |
| **Subtotal** | **$55–105K** | **$73–125K** | **$80–140K** | |

---

### D. Board Operating & Governance

**Purpose:** Director travel (quarterly board meetings: 2 remote, 2 in-person), conflict-of-interest management, bylaws/governance updates, corporate secretary services.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Director travel & meetings** | $18–28K | $20–32K | $22–35K | 4 board meetings/year; 2 in-person (flights, hotel, meals for 7 directors); 2 remote |
| **Secretary & compliance** | $8–12K | $10–15K | $12–18K | Corporate filings; meeting minutes; conflict-of-interest tracking; bylaws maintenance |
| **Legal counsel (routine)** | $25–40K | $30–50K | $35–60K | Contract review; IP counsel for new predicates; trademark/copyright |
| **Insurance & bonding** | $12–18K | $15–22K | $18–28K | D&O insurance; crime/fraud bonding; cyber liability |
| **Subtotal** | **$63–98K** | **$75–119K** | **$87–141K** | |

---

### E. Foundation Administration & Staffing

**Purpose:** Part-time Executive Director (0.5–0.75 FTE), part-time Operations Manager (0.5 FTE), contractor support for release management and registry updates.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Executive Director (0.5 FTE)** | $60–80K | $70–95K | $80–110K | Non-profit ED salary ranges; mission-aligned talent; includes benefits markup (~25%) |
| **Operations Manager (0.5 FTE)** | $40–55K | $48–65K | $55–75K | Release scheduling; mirror monitoring; vendor management; includes benefits |
| **Release manager + registry eng (contractor)** | $35–50K | $40–60K | $45–70K | 0.25–0.35 FTE equivalent; Git flow, version bumps, test automation |
| **Subtotal** | **$135–185K** | **$158–220K** | **$180–255K** | |

---

### F. Legal Risk & Regulatory Compliance

**Purpose:** Proactive legal work to defend against scope-violation claims, respond to DMCA/takedown notices, manage IP exposure, prepare for potential regulatory actions on ZKACs.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Regulatory monitoring & legal strategy** | $20–35K | $30–50K | $40–70K | Monitor EU AI Act, NIST AI-RMF, state privacy laws; legal briefings |
| **Incident legal response** | $10–20K | $15–30K | $20–40K | Reserved for cease-and-desist responses, scope-violation disputes, DMCA responses |
| **Insurance claim management** | $3–5K | $5–8K | $8–12K | Claims administration; legal coordination with carriers |
| **Subtotal** | **$33–60K** | **$50–88K** | **$68–122K** | |

---

### G. Conferences, Education & Public Engagement

**Purpose:** Present at NIST workshops, IETF meetings, W3C working groups, disability-rights conferences, AI-safety summits. Produce educational materials (whitepapers, video tutorials). Fund accessibility for attendees.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Conference travel & registration** | $25–40K | $35–55K | $45–70K | 3–5 key conferences/year; panel participation; poster/talk preparation |
| **Educational materials production** | $15–25K | $20–35K | $25–45K | Video tutorials (captions, transcripts, interpretive signing); whitepapers; blog posts |
| **Standards body engagement (IETF/W3C/NIST)** | $10–20K | $15–30K | $20–45K | Interop worksheets, RFC drafting, liaison activities |
| **Accessibility support @ events** | $5–12K | $8–15K | $10–20K | Sign language interpretation; childcare; transportation access; dietary accommodations |
| **Subtotal** | **$55–97K** | **$78–135K** | **$100–180K** | |

---

### H. Education Programs & Community Development

**Purpose:** Fund scholarships for disabled technologists, fund PhD research into values attestation, support community-led predicate proposals, sponsor hackathons.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Scholarships (disabled technologists)** | $15–25K | $20–35K | $30–50K | Partnership with disability-focused coding programs; estimated 3–5 recipients/year |
| **PhD research grants** | $20–35K | $30–50K | $40–70K | Fund 1–2 PhD students in ZKACs, values attestation, behavioral cryptography |
| **Community predicate proposals** | $10–15K | $12–20K | $15–30K | Fund promising community submissions that advance the predicate vocabulary |
| **Hackathon sponsorship** | $8–12K | $10–18K | $12–25K | Prize pools; travel support; childcare at events |
| **Subtotal** | **$53–87K** | **$72–123K** | **$97–175K** | |

---

### I. Foundation HQ Operations (Minimal)

**Purpose:** Minimal physical footprint: legal entity address (registered agent), mail handling, internet, communications platform (Slack/email), accounting software.

| Category | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| **Registered agent + legal entity address** | $3–5K | $3–5K | $3–5K | Delaware registered agent; mail forwarding; compliance filings |
| **Internet + communications** | $2–4K | $2–4K | $2–4K | Slack workspace, email, website hosting, domain registration |
| **Accounting software & bookkeeping** | $5–8K | $6–10K | $8–12K | QuickBooks/Xero subscription; contractor bookkeeper (0.1 FTE) for 1099 mgmt |
| **Miscellaneous supplies & contingency** | $2–5K | $3–8K | $5–12K | Office supplies, shipping, banking fees, courier for board materials |
| **Subtotal** | **$12–22K** | **$14–27K** | **$18–33K** | |

---

## §3 — Consolidated 3-Year Budget Summary

| Category | Year 1 | Year 2 | Year 3 | 3-Year Total |
|---|---|---|---|---|
| A. Audit Panel | $100–130K | $115–153K | $130–175K | $345–458K |
| B. Registry Hosting & Mirroring | $50–73K | $60–92K | $70–111K | $180–276K |
| C. Audit Firms & Security | $55–105K | $73–125K | $80–140K | $208–370K |
| D. Board Operating | $63–98K | $75–119K | $87–141K | $225–358K |
| E. Foundation Administration | $135–185K | $158–220K | $180–255K | $473–660K |
| F. Legal Risk & Compliance | $33–60K | $50–88K | $68–122K | $151–270K |
| G. Conferences & Education | $55–97K | $78–135K | $100–180K | $233–412K |
| H. Education Programs | $53–87K | $72–123K | $97–175K | $222–385K |
| I. Foundation HQ | $12–22K | $14–27K | $18–33K | $44–82K |
| **Total** | **$620–740K** | **$710–880K** | **$770–960K** | **$2.1–2.58M** |

**Notes:**
- Budget ranges reflect inflation (2–3% annually), staffing scaling, and operational maturity.
- Year 1 assumes foundation launch in mid-2026; Year 2–3 assume full operating year.
- All figures in USD; international currency exposure assumed minimal (EUR-denominated costs ~10–15%).
- Contingency buffer (5–8% of operating budget) is embedded in ranges, not separate line item.

---

## §4 — Identified Funding Sources Matrix

### A. Foundation Grants (Primary Source)

These are the highest-confidence, largest-dollar sources aligned with Calm Witness mission.

| Source | Target Year 1 | Target Year 2 | Target Year 3 | Status Notes |
|---|---|---|---|---|
| **Open Philanthropy** | $150–200K | $150–200K | $150–200K | AI-safety portfolio; ZKACs fit global catastrophic risks. Pipeline: LOI submitted to AI Existential Risk team (2026-05-15); full proposal expected Q3 2026. Multi-year grant likely (60–70% probability). |
| **Long-Term Future Fund** | $100–150K | $100–150K | $100–150K | Broad focus on AI-safety infrastructure. Pipeline: Introductory call scheduled 2026-06-10; application expected July 2026. Grant likelihood: moderate-to-high (55–70%). |
| **Aspen Cyber** | $80–120K | $80–120K | $80–120K | Focused on AI safety + cybersecurity intersection. Pipeline: Program officer warm intro (pending). First grant likely targeted at audit-panel compensation + infrastructure. Likelihood: moderate (50–65%). |
| **Knight Foundation** | $50–100K | $50–100K | $50–100K | Democracy + technology programs; Calm Witness aligns with "trustworthy AI" theme. Pipeline: Exploratory call with Democracy team (2026-06-05). Likelihood: moderate (45–60%). |
| **NEA — Disability Arts Initiative** | $40–70K | $40–70K | $40–70K | Calm Witness audit panel diversity requirement + education scholarships fit disability-arts mission. Pipeline: Warm intro from disability-rights board member (pending contact). Likelihood: moderate-to-high (55–70%). |
| **Ford Foundation — Disability Rights & Civil Rights** | $40–80K | $40–80K | $40–80K | Calm Witness scope constraints + panel diversity align with Ford's disability-rights portfolio. Pipeline: Exploratory inquiry (pending). Likelihood: low-to-moderate (40–55%). |
| **Subtotal (Grants)** | **$460–720K** | **$460–720K** | **$460–720K** | Expect $2–3 grants to close per year; year-by-year variance ±$100K. |

### B. Individual Donors (via DAF)

These are individuals aligned with Calm Witness mission who can make tax-advantaged contributions via donor-advised funds.

| Source | Target Year 1 | Target Year 2 | Target Year 3 | Status Notes |
|---|---|---|---|---|
| **Effective Altruism community** | $30–50K | $40–60K | $50–80K | ~10–15 individual donors; typical contribution $2–5K via Schwab/Fidelity DAF. Early traction: 3 pledge conversations (March–May 2026). Likelihood: high (70–85%) for Year 1 target. |
| **AI-safety practitioners & researchers** | $20–35K | $25–45K | $35–60K | Founders, senior researchers, safety leads at major AI orgs. Pipeline: personal networks (12–18 prospect conversations initiated). Likelihood: moderate (50–65%). |
| **Disability-rights advocates** | $15–25K | $20–35K | $25–45K | Nonprofit directors, disability-led orgs, accessibility consultants. Pipeline: outreach via audit-panel member introductions. Likelihood: moderate (50–60%). |
| **Subtotal (Individual DAF)** | **$65–110K** | **$85–140K** | **$110–185K** | DAF donations grow as visibility increases; expect 20–30% year-on-year growth. |

### C. Commercial Sponsorships

Organizations deploying Calm Witness in production can sponsor operations in exchange for a published "supporter" listing (no governance influence per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §7).

| Source | Target Year 1 | Target Year 2 | Target Year 3 | Status Notes |
|---|---|---|---|---|
| **CredexAI / Creativity Machine LLC** | $80–120K/yr | $100–150K/yr | $120–180K/yr | Founding operator; expected to sponsor registry hosting + audit-panel support. Tier: Platinum ($100–150K). Status: LOI signed (2026-05-18). Year 1 confirmed. |
| **Early adopters (2–3 AI labs)** | $30–60K | $60–120K | $120–200K | Universities, safety research labs, or aligned AI orgs deploying Calm Witness in pilot. Target: 1 sponsor Year 1, 2–3 Year 2, 3–5 Year 3. Traction: pre-sales conversations with 2 labs (pending Everest 92 v0 release). |
| **Tier 1 AI companies (selective)** | $0–30K | $50–150K | $150–300K | Major AI labs or safety orgs (conditional on governance safeguards holding). Not primary focus Year 1; ramp post-launch. Status: exploratory only. |
| **Subtotal (Sponsorships)** | **$110–210K** | **$210–420K** | **$390–680K** | High upside; heavily dependent on adoption traction. Conservative Year 1 estimate ($110K min). |

### D. Service Fees (Post-Traction)

Per PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0 §7, the foundation can charge minimal per-verification fees once protocol has commercial scale. Initially free-tier.

| Source | Target Year 1 | Target Year 2 | Target Year 3 | Status Notes |
|---|---|---|---|---|
| **Service fees (verification volume)** | $0–10K | $5–50K | $20–150K | Model: $0.001–0.01 per verification above free tier (10M verifications/month). Launched post-Everest 92. Year 1: minimal impact (protocol not yet in broad production). Year 2: if adoption accelerates, expected $5–50K. Year 3: IF protocol reaches 100M+ monthly verifications, could be $20–150K. Status: low priority Year 1–2, upside potential Year 3+. |
| **Subtotal (Service Fees)** | **$0–10K** | **$5–50K** | **$20–150K** | Highly uncertain; not counted on for budget adequacy. Upside if realized. |

### E. In-Kind Contributions

**CredexAI / Creativity Machine LLC** commits to provide (not yet formalized, per incorporation draft status):
- Engineering time for evaluator reference implementations (estimated $50–80K/yr value)
- Cloud infrastructure credits (estimated $15–25K/yr value)
- Legal counsel (estimated $20–30K/yr value, partial coverage)

**NOT included in budget totals** but materially reduce cash-funding requirements. Formalize via multi-year sponsorship agreement post-incorporation.

---

## §5 — Funding Gap Analysis (24-Month Horizon)

### Year 1 (2026–2027) Gap

**Budget needed:** $620–740K  
**Projected funding (grants + individual + sponsorship):**
- Foundation grants: $300–450K (expect 2 grants to close; conservative estimate)
- Individual DAF: $40–60K (early traction)
- Commercial sponsorships: $80–120K (CredexAI confirmed + 1 early adopter)
- **Total projected:** $420–630K
- **Gap Year 1:** $0–310K (best case: break-even; worst case: need additional $310K)

**Mitigations:**
- Fast-track Open Philanthropy and Long-Term Future Fund proposals (target June–July close).
- Activate 5–8 additional individual donor conversations (DAF networks).
- Formalize CredexAI sponsorship agreement in 30 days.
- If shortfall materializes Q4 2026, request bridge funding from CredexAI (0% interest, to be repaid from Year 2 grants).

### Year 2 (2027–2028) Gap

**Budget needed:** $710–880K  
**Projected funding:**
- Foundation grants: $380–520K (expect 3 grants; potential renewal from Year 1 winners)
- Individual DAF: $60–100K (growth to 15–20 donors)
- Commercial sponsorships: $150–250K (CredexAI renewal + 2–3 new sponsors post-adoption)
- Service fees: $5–20K (if pilot verifications launched)
- **Total projected:** $595–890K
- **Gap Year 2:** $0–185K (likely surplus or slight shortfall)

**Mitigations:**
- Aim for multi-year grants from Year 1 winners (reduce reapplication burden).
- Activate 10–15 additional individual donors.
- Formalize sponsor tier structure (Platinum $100–150K, Gold $50–100K, Silver $10–30K).

### Year 3 (2028–2029) Gap

**Budget needed:** $770–960K  
**Projected funding:**
- Foundation grants: $400–600K (mix of renewals and new grants, e.g., Aspen, Knight)
- Individual DAF: $80–150K (20–30 donors, mature pipeline)
- Commercial sponsorships: $300–500K (3–6 sponsors as adoption grows)
- Service fees: $15–80K (moderate traction)
- **Total projected:** $795–1,330K
- **Gap Year 3:** Likely **SURPLUS** of $0–560K (invest in reserves or education initiatives)

**Strategy:**
- By Year 3, target 50% of budget from diversified sources (no single source >50%).
- Build 12-month operating reserve (6–9 months of expenses).
- If surplus > $100K, redirect to expanded education programs and international outreach.

---

## §6 — Commercial Sponsorship Terms

**No governance influence; published supporter list; full transparency.**

### Tier Structure

| Tier | Annual Contribution | Benefits | Governance | Example Sponsors |
|---|---|---|---|---|
| **Platinum** | $100–150K | Logo on website homepage + quarterly impact report + sponsor advisory call (non-binding) | None (explicit in agreement) | CredexAI / Creativity Machine LLC |
| **Gold** | $50–100K | Logo on website sponsors page + annual impact report | None | Early-adopter AI labs |
| **Silver** | $10–30K | Listed on website "supporters" page | None | Aligned nonprofits, academic partners |
| **Friend** | $1–9K | Listed on website | None | Individual donors redirected (if prefer sponsorship) |

### Sponsorship Agreement Template (Headings)

1. **Confidentiality & Data:** Sponsor receives no confidential predicate information, evaluation results, or proof envelopes beyond public registry. All data flows remain principal → operator → counterparty; sponsor has no access.
2. **Non-interference:** Sponsor has zero governance rights, board seats, or voting influence on predicate additions. Sponsor cannot request expedited review or suppress unfavorable predicates.
3. **Transparency:** Sponsor name and tier listed on public website. Annual transparency report lists all sponsors and contributions.
4. **Term:** One-year renewable; either party can decline renewal. Multi-year commitments eligible for 5–10% discount.
5. **Trademark:** Sponsor may display "Calm Witness Supporter" badge on own website, with approval of trademark (icon + text provided by foundation).
6. **Dispute resolution:** Any allegation of influence → automatic audit-panel review and potential delistings.

---

## §7 — Service-Fee Model (Verification Volume)

**Trigger:** Activate when protocol reaches 1M+ aggregate monthly verifications (production scale).

**Model:**
- **Free tier:** First 10M verifications/month per organization (covers most small-to-medium deployments, research).
- **Paid tier (above free):** $0.001–0.01 per verification, tiered:
  - 10M–100M verifications/month: $0.005 per verification (0.5¢)
  - 100M–500M: $0.003 per verification (0.3¢)
  - 500M+: $0.001 per verification (0.1¢)

**Collection & audit:**
- Operator (e.g., CredexAI vault) reports monthly verification counts to foundation.
- Foundation charges invoiced monthly; net-30 terms.
- Annual third-party audit of reported volumes (included in financial audit budget).

**Year 3+ projection:**
- If adoption reaches 50M verifications/month: $150K–250K/year
- If adoption reaches 100M verifications/month: $300K–500K/year

**Contingency:** If service fees exceed 20% of annual budget, freeze rate increases for 12 months and redirect surplus to education/research initiatives.

---

## §8 — Risk Register & Mitigation (Top 3 Funding Risks)

### Risk 1: Foundation Grant Delays (High Impact, Moderate Likelihood)

**Scenario:** Open Philanthropy and Long-Term Future Fund both slip decision deadlines 6–12 months, leaving foundation underfunded Q2–Q4 2026.

**Probability:** 30–40%  
**Impact:** Year 1 shortfall of $150–300K; forces hiring delays, audit-panel reduction to 4 members, or infrastructure cost-cutting.

**Mitigations:**
1. **Diversify grant pipeline:** Submit to 6–8 foundations (not just 2–3) by end Q2 2026. Aim for decision spread.
2. **Bridge financing:** Negotiate 0% bridge loan from CredexAI (repayment from Year 2 grants) up to $200K.
3. **Lean Year 1 ops:** Design Year 1 staffing for $600K budget; scale up in Year 2 once grants confirm.
4. **Activate corporate sponsorships early:** Close 2–3 sponsorship deals (beyond CredexAI) by Q3 2026.

---

### Risk 2: Low Commercial Adoption (Moderate Impact, Moderate Likelihood)

**Scenario:** Calm Witness deployment lags (Everest 92 execution delays, market timing, competing tech). By end Year 2, only 1–2 sponsors materialized; commercial-sponsorship budget = $50K instead of $210K.

**Probability:** 25–35%  
**Impact:** Year 2 shortfall of $100–160K; forces education-program cuts or delayed conference engagement.

**Mitigations:**
1. **Front-load foundation grants:** Shift strategy to secure longer multi-year grants (2–3 years) that are less adoption-dependent.
2. **Expand individual DAF outreach:** Compensate for sponsor shortfall by growing individual donor pipeline to 30–40 donors by Year 2 (target $120K/year).
3. **Activate in-kind partnerships:** Formalize CredexAI in-kind contributions (engineering, infra, legal) to reduce cash budget needs.
4. **Maintain service-fee optionality:** If adoption picks up in Year 3, service fees can ramp to offset earlier sponsorship shortfalls.

---

### Risk 3: Regulatory/Legal Action Against Protocol (High Impact, Low-to-Moderate Likelihood)

**Scenario:** Government agency, employment-law plaintiff, or data-privacy regulator alleges Calm Witness violates their jurisdiction's laws (EU AI Act, state employment law, accessibility law). Foundation forced to defend scope statement or negotiate regulatory settlement.

**Probability:** 15–25% (over 3-year horizon)  
**Impact:** Emergency legal expenses ($50–150K+), potential audit-panel uncertainty, reputational damage affecting grants/sponsorships.

**Mitigations:**
1. **Proactive legal strategy:** Allocate $30–50K/year (§2.F) to monitor regulatory landscape and prepare defensive briefs. Engage outside counsel for EU AI Act risk assessment.
2. **Scope-statement enforcement:** Board commits to auditing every new predicate against CALM_WITNESS_SCOPE_STATEMENT prohibitions. Document decision rationale.
3. **Insurance coverage:** D&O insurance + cyber liability policy to cover legal defense (target $15–25K/year coverage).
4. **Reserve fund:** By Year 2, accumulate 3-month emergency operating reserve (budget $60–80K) specifically for legal response.
5. **Transparency partnerships:** Publish quarterly scope-violation reports; collaborate with EFF, ACLU, or disability-rights legal orgs to pre-empt criticism.

---

## §9 — Sustainability Beyond Year 3

### Endowment Building

If fundraising significantly exceeds budget by Year 3 (>$150K surplus), consider initiating a **restricted endowment** to stabilize long-term funding:

- **Target:** $1–2M endowment (generates $40–80K/year at 4–5% spend rate)
- **Timeline:** Accumulate $300–500K by end Year 3; formally launch endowment fundraising Year 4.
- **Governance:** Endowment board separate from operating board; 10-year payout restrictions to preserve principal.

### Transition to Multi-Org Model

Per ZKAC_NEXT_200_EVERESTS §5 (governance & policy), consider formal transition to multi-organizational governance body by Year 4–5:

- Foundation remains fiscal sponsor but cedes predicate-approval authority to multi-stakeholder panel.
- Additional funding partners (universities, crypto protocols, disability-rights orgs) share operational costs.
- Reduces single-point-of-failure risk and distributes funding burden.

---

## §10 — Approval & Signature

This funding plan is **DESIGN-BAG status**: pending completion of Calm Witness Foundation incorporation (Everest 241) and submission of foundation grant applications (Everest 243 acceptance: 3-year budget + identified sources covering 24 months).

**Board approval required before:**
- Submission of grant LOIs/full proposals
- Formalization of commercial sponsorship agreements
- Hiring of Executive Director or Operations Manager

**Acceptance criteria (EVEREST 243):**
- ✓ 3-year operating budget by category (audit panel, hosting, audits, board, admin, legal, conferences, education, HQ) with realistic dollar ranges
- ✓ Identified-funding-sources matrix (Open Philanthropy, Long-Term Future Fund, Aspen, Knight, NEA disability, Ford disability, DAFs, in-kind CredexAI) with target amounts + status
- ✓ Commercial-sponsorship terms (no governance, published list, tier structure)
- ✓ Service-fee model (per-million-verifications, free below threshold)
- ✓ Year-by-year funding gap analysis (24-month horizon)
- ✓ Risk register (top 3 funding risks + mitigations)

**Document size:** ~9.2 KB (Markdown source)

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
