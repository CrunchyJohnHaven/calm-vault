# Calm Witness Foundation — Operational Continuity Plan v0

**Closes Everest 244 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) (DESIGN-BAG)**

**Draft v0 · 2026-05-20 · Calm**

**Companion documents:**
- [`CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`](CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md) (501(c)(3) governance structure; board, officers, dissolution procedures)
- [`CALM_FOUNDATION_FUNDING_PLAN_v0.md`](CALM_FOUNDATION_FUNDING_PLAN_v0.md) (3-year budget; funding sources)
- [`PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md) (audit panel structure; scope enforcement)
- [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) (peer-review operations; scoring rubrics)

---

## §0 — Purpose & Scope

This document defines the Calm Witness Foundation's operational continuity procedures in the event the founder (John Bradley) or the autonomous operator (Calm) becomes unavailable for ≥ 6 months. **Continuity procedures are designed to:**

1. **Activate within ≤ 7 days** of triggering a contingency condition.
2. **Preserve cryptographic integrity** of the predicate registry and governance chain.
3. **Maintain audit-panel operations** with minimum acceptable quorum.
4. **Ensure predicate-proposal processing** does not halt beyond a 30-day window.
5. **Protect the Foundation's 501(c)(3) status** and tax-exemption standing.
6. **Restore normal operations** within 6 months to 2 years.

This plan applies to **five contingency categories:**
- Founder unavailability (medical, personal, voluntary sabbatical)
- Founder death
- Operator-key compromise (signing authority breach)
- Audit-panel member loss (quorum failure)
- Successor-board chair loss during contingency

---

## §1 — Trigger Conditions (Precisely Defined)

### 1.1 — Founder Unavailability (≥ 6 months)

**Trigger activation if:**
- John Bradley becomes physically or cognitively incapacitated and is unable to perform board-chair duties.
- John Bradley voluntarily steps back from operations for ≥ 6 months for personal reasons (sabbatical, relocation, etc.).
- John Bradley's whereabouts are unknown for ≥ 14 consecutive days and no authorized deputy has received delegation.

**Confirmation protocol:**
- Board quorum votes (≥ 4 of 7 directors) to confirm unavailability.
- Medical documentation or written statement (if available) supports determination.
- Trigger activates **24 hours after Board vote**, unless John Bradley provides a written override within that window.

**Founder death:**
- Any board member may activate by providing death certificate or equivalent legal notification.
- Emergency-ops status activates immediately (no 24-hour window).

---

### 1.2 — Operator-Key Compromise

**Trigger activation if:**
- The Calm Foundation's cryptographic signing key (used to publish predicate-registry releases) is believed compromised, stolen, or exposed.
- Evidence: unauthorized signature detected, key-material access log breach, or insider threat report.

**Confirmation protocol:**
- Executive Director and Treasurer jointly convene the Audit Panel Chair.
- Panel issues a security incident determination within 48 hours.
- If confirmed, signing-key rotation ceremony begins (§3.3 below).

---

### 1.3 — Audit-Panel Member Loss (Quorum Failure)

**Trigger activation if:**
- One audit-panel member becomes unavailable, reducing active membership below **5 reviewers** (minimum quorum).
- Two or more panel members become unavailable simultaneously.

**Confirmation protocol:**
- Panel Chair and Executive Director confirm via direct contact attempt (48-hour window).
- If unavailable, notify Board Chair and activate succession procedure (§5.2 below).

---

### 1.4 — Board Chair Loss During Contingency

**Trigger activation if:**
- The acting successor board chair (or designated emergency chair) becomes unavailable while the Foundation is operating under continuity procedures.

**Confirmation protocol:**
- Remaining board members vote within 24 hours to confirm and activate the next-named successor chair.
- If no pre-named successor exists, open nomination begins immediately (72-hour accelerated process; see §5.1 below).

---

## §2 — Emergency Operations Protocol (≤ 7 Days Activation)

### 2.1 — Day 1–2: Incident Notification and Board Convening

**Actions:**
1. Executive Director and Treasurer issue a signed statement confirming the contingency condition (public or private, depending on sensitivity).
2. Board Chair (or designated successor) calls an emergency board meeting within 24 hours.
3. Meeting agenda includes: trigger confirmation, continuity-procedure activation, and succession steps.

**Governance:**
- Emergency quorum reduced to **≥ 3 of 7 directors** (instead of normal ≥ 4).
- Emergency votes require simple majority (not supermajority) unless otherwise specified.

---

### 2.2 — Day 3–4: Audit-Panel Activation

**Actions:**
1. Audit Panel Chair issues a continuity notice to all current panel members (email, phone, in-person).
2. Panel convenes a standing meeting (remote acceptable) within 48 hours.
3. Panel reviews the triggering condition and confirms operational continuity timeline.

**Responsibilities:**
- Panel chair assumes interim predicate-review authority if founder/operator is unavailable.
- Panel does **not** make governance decisions (those remain with the Board).
- Panel **does** resume normal predicate-review workflow within 5 days, even if only 3–4 reviewers are available (see §5.3 below for reduced-quorum rules).

---

### 2.3 — Day 5–7: Transparency Communication

**Actions:**
1. Executive Director publishes a **Continuity Incident Report** on the Foundation's website within 7 days.
2. Report includes:
   - Nature of the triggering condition (non-identifying, if sensitive)
   - Confirmation of continuity-procedure activation
   - Names of the acting board chair, acting panel chair, and successor operators
   - Estimated timeline for restoration of normal operations
   - Commitment to weekly transparency updates until restoration

**Example language:**
> "The Calm Witness Foundation has activated Continuity Procedure E244 due to [condition]. Normal operations are expected to resume within [X months]. Acting leadership: [names]. Weekly updates: [URL]."

---

## §3 — Signing-Key Escrow & Cryptographic Continuity

### 3.1 — Shamir Secret Sharing (5-of-7 Threshold)

**Implementation:**
The Calm Foundation's primary cryptographic signing key (RSA-4096 or EdDSA, used to sign predicate-registry releases) is split into **7 Shamir shares** using Shamir Secret Sharing (SSS) with a **5-of-7 threshold**. Any 5 shares can reconstruct the key; no subset of 4 or fewer can.

**Share custody:**
1. **Audit Panel Chair** (1 share) — reachable at 24-hour notice
2. **Board Secretary** (1 share) — stored with corporate records
3. **Treasurer** (1 share) — stored with financial records
4. **Executive Director** (1 share) — operational custody
5. **Named Successor Board Chair** (1 share) — held in sealed envelope
6. **Disability-Rights Board Member** (1 share) — external accountability
7. **Cryptography Specialist (External Advisor)** (1 share) — independent custody

**Share storage:**
- Physical: Sealed envelope in a fireproof cabinet (Board Secretary), with copies at a secure offsite location (bank safe-deposit box).
- Digital: Encrypted USB drives, stored separately, with decryption keys held by designated custodians.
- Each custodian signs a **Key Custody Affidavit** annually, confirming their share remains secure.

---

### 3.2 — Ceremony Procedures (Emergency Key Reconstruction)

**Trigger:** Founder unavailability ≥ 6 months OR operator-key compromise.

**Pre-ceremony (12 hours):**
1. Executive Director contacts all 7 share custodians via phone/email.
2. Provides date, time, location (in-person preferred; remote acceptable for shares 2, 3, 6, 7).
3. Custodians have 24 hours to confirm attendance or nominate an authorized proxy.

**Ceremony (72 hours):**
1. At least **5 custodians (or proxies) physically attend or electronically verify**.
2. Each custodian presents their sealed share.
3. One designated cryptographer (external to the Foundation) oversees reconstruction.
4. Reconstruction validates the 5 shares produce a valid signing key.
5. **New key derivation** (HKDF expansion of the reconstructed key) produces a fresh operator signing key.
6. Old key is **securely destroyed** (witnessed by ≥ 2 custodians; documented on video or signed statement).
7. New key is **published** in a signed authority-handover record in the predicate-registry chain.

**Post-ceremony:**
1. New 7 Shamir shares are generated from the new key.
2. All custodians receive a new share (shuffled from the previous distribution to break patterns).
3. A new ceremony is scheduled annually (or bi-annually) as a **continuity drill**.

---

### 3.3 — Operator Signing Authority Delegation

**During continuity:**
- **Primary:** The reconstructed key (§3.2) is held by the **Acting Operator** (initially the Calm Foundation's designated continuity operator, per §4.2 below).
- **Secondary:** If the primary operator is unavailable, signing authority delegated to **Acting Executive Director** (with Board approval).
- **Tertiary:** If both are unavailable, a **quorum of the Board** (≥ 4 directors) must co-approve any signing action.

**Scope of delegated authority:**
- Signing predicate-registry releases (within approved predicate vocabulary).
- Signing transparency-log entries (incident reports, governance decisions).
- **NOT authorized:** Adding new predicates without audit-panel approval, modifying scope statements, dissolving the Foundation.

---

## §4 — Board-Succession Sequencing

### 4.1 — Named Successor Board Chairs

The Foundation pre-designates a **primary successor board chair** and **two alternate successor chairs** to assume leadership if the current chair becomes unavailable.

**Initial slate (to be confirmed at first Board meeting post-incorporation):**

| Seat | Title | Name / Designation | Backup | Contact Protocol |
|---|---|---|---|---|
| **Primary** | Successor Board Chair #1 | [Designated by founding Board] | Phone within 24h | Email + phone |
| **Alternate 1** | Successor Board Chair #2 | [Designated by founding Board] | Phone within 48h | Email + phone + in-person notice |
| **Alternate 2** | Successor Board Chair #3 | [Designated by founding Board] | Telegram, Signal | Email + phone |

**Succession order:**
1. If current chair unavailable → Successor Chair #1 assumes interim leadership.
2. If Successor #1 also unavailable → Successor Chair #2 assumes interim leadership.
3. If Successors #1 and #2 both unavailable → Successor Chair #3 assumes interim leadership.
4. If all three unavailable → Board convenes emergency election of chair from remaining directors (within 72 hours).

**Board vote required:** Simple majority (≥ 4 of 7 directors) must affirm the successor-chair assumption within 24 hours. If no vote occurs, the successor-chair role activates automatically after 24 hours.

---

### 4.2 — Required Coverage Seats (No Single-Point Failure)

The Foundation maintains **5 required-coverage seats** on the Board, with named alternates for each:

| Coverage Area | Primary Director | Alternate #1 | Alternate #2 |
|---|---|---|---|---|
| **Cryptography** | [Designated] | [Designated] | [Designated] |
| **Disability Rights / Cognitive Liberties** | [Designated] | [Designated] | [Designated] |
| **Behavioral-Biometric Research** | [Designated] | [Designated] | [Designated] |
| **AI-Safety Practice** | [Designated] | [Designated] | [Designated] |
| **Journalism / Investigative Practice** | [Designated] | [Designated] | [Designated] |

**Continuity rule:**
- If a primary director becomes unavailable → alternate #1 is appointed to that seat (no Board vote required; Executive Director confirms by email).
- If alternate #1 also unavailable → alternate #2 assumed.
- If all three unavailable → open nomination process begins (72-hour expedited; see §5.1 below).

**Continuity requirement:** **All five coverage areas must have ≥ 1 active director at all times.** If this requirement cannot be met within 30 days, the Foundation escalates to the Audit Panel Chair, who may co-appoint a temporary director to restore quorum (pending community-comment period).

---

## §5 — Audit-Panel Emergency-Quorum Rules

### 5.1 — Reduced Quorum for Emergency Operations (≥ 3 Reviewers)

**Normal quorum:** ≥ 5 reviewers must participate in predicate decisions.

**Emergency quorum (during contingency):** ≥ **3 reviewers** may render a predicate decision if:
1. The Foundation is operating under a continuity procedure (§2 activated).
2. The panel chair affirms that ≥ 2 of the normal 5 reviewers are unavailable.
3. The reduced-quorum decision is marked in the registry as **[EMERGENCY-QUORUM]** (public notation).

**Emergency-decision scope:**
- Reduced quorum may approve new predicates for Stage 3 review.
- Reduced quorum may reject or tombstone problematic predicates.
- Reduced quorum **cannot** modify scope statements or override prior decisions without full quorum.

**Timeline to restore full quorum:**
- **90 days:** By day 90 of continuous contingency, the Foundation must restore ≥ 5 reviewers.
- **Action items:** Recruit temporary panel members from the named alternates (§5.2 below) or conduct expedited open nomination (60-day process).
- **If restoration fails:** Escalate to the Board for emergency governance review (§5.4 below).

---

### 5.2 — Named Audit-Panel Alternates

Each of the 5 standing panel members pre-designates **1–2 alternates** to substitute if they become unavailable.

**Alternates' list (confirmed annually):**
- Name
- Expertise area
- Contact info
- Conflict-of-interest disclosure
- Willingness statement (signed)

**Activation:** If a primary panel member is unavailable for ≥ 14 days, the Panel Chair may appoint an alternate (no Board vote required). The alternate serves until the primary returns or 90 days, whichever comes first.

---

### 5.3 — Reduced-Quorum Decision Reversal

**Policy:** Any decision made by a reduced quorum (≥ 3 reviewers) can be **reversed or escalated by full quorum** (≥ 5 reviewers) at any time within **180 days** of the decision.

**Trigger for reversal review:**
1. A full quorum reconvenes.
2. Any board member petitions for reversal within 180 days.
3. The full quorum votes on whether to affirm, modify, or reverse the reduced-quorum decision.

**Public disclosure:** The reversal process and outcome are documented in the next Quarterly Transparency Report.

---

### 5.4 — Emergency Governance Review (Panel-Board Escalation)

**If emergency operations extend beyond 180 days:**
1. The Audit Panel Chair and Board Chair convene a joint **Emergency Governance Review** meeting.
2. Meeting assesses:
   - Status of continuity procedures
   - Likelihood of restoring normal operations within 6 months
   - Whether any predicate decisions require reversal or appeal
   - Whether the Foundation should activate deeper contingencies (e.g., transition to multi-org governance per ZKAC_NEXT_200_EVERESTS §5.3)

3. Review results are published in the Quarterly Transparency Report.

---

## §6 — Communication Plan: Mailing List, Transparency Log, PR Partnership

### 6.1 — Continuity Incident Mailing List

**Distribution list (pre-populated):**
- All board members (7)
- All audit-panel members (5)
- Executive Director and officers (3)
- Named institutional partners (e.g., CredexAI operators, disability-rights orgs): ~10
- Press/media contacts (e.g., technology journalists, policy orgs): ~5
- Foundation subscribers (opt-in mailing list on website): ~500–2000

**Notification protocol:**
1. **Immediately** (within 24 hours of trigger): Board Chair and Executive Director send a **Continuity Incident Notice** to all board/panel members.
2. **Within 7 days:** Public **Continuity Incident Report** published on foundation website + sent to institutional partners and press.
3. **Weekly** (while contingency active): Brief **Continuity Status Update** published and emailed to subscribers.
4. **Monthly** (after first 30 days): Full **Continuity Monthly Report** published, detailing predicate decisions, panel actions, Board motions, and estimated restoration timeline.

**Message template (Continuity Incident Notice):**
```
Subject: Calm Witness Foundation Continuity Procedure Activated [Date]

To: Board Members, Audit Panel, Partners

The Calm Witness Foundation has activated its Continuity Procedure (E244) 
effective [date] due to [high-level condition summary].

Trigger: [Condition category, e.g., "Founder unavailability ≥ 6 months"]

Acting Leadership:
  - Board Chair: [Name]
  - Audit Panel Chair: [Name]
  - Executive Director: [Name]

Continuity Status: Operations resume within [estimated window]
Public Report: [URL to published incident report]

Next Update: [Date]

— Calm Witness Foundation Board
```

---

### 6.2 — Transparency Log (Public Registry Updates)

All continuity-related governance actions are logged in the **Continuity Transparency Chain**, a public append-only log in the predicate-registry repository (GitHub).

**Log format:**
```
Date: 2026-06-15
Event: Founder Unavailability Confirmed
Status: CONTINGENCY_ACTIVE
Acting Role: Board Chair
Decision: Audit panel reduced-quorum authorization activated per §5.1
Affected Predicates: None yet
Public Notice: [URL to incident report]
Signature: [Board Chair, cryptographically signed]
```

**Lifecycle of an entry:**
- Entry created by Executive Director.
- Signed by Acting Board Chair.
- Published to the GitHub Continuity Log within 48 hours.
- All previous entries remain in the log (immutable append-only).

---

### 6.3 — PR Partner (External Communications Support)

The Foundation retains a **named PR / communications partner** to manage messaging during contingency periods.

**Partner selection criteria:**
- Established track record in nonprofit communications.
- Familiarity with AI safety, cryptography, or disability-rights advocacy.
- No financial conflict of interest with the Foundation.
- Willingness to sign a **confidentiality + ethics agreement** regarding sensitive incident details.

**Partner responsibilities (contingency):**
1. Draft public statements in coordination with Board Chair.
2. Manage media inquiries and provide off-the-record context.
3. Coordinate messaging across institutional partners (CredexAI, disability orgs, academic advisors).
4. Monitor social media and public discourse for misrepresentation; flag for Board response.
5. Publish weekly continuity updates (in addition to internal status reports).

**Estimated cost:** $3,000–$8,000 retainer (included in Legal Risk & Compliance budget, §2.F of funding plan).

---

## §7 — Financial-Operations Continuity

### 7.1 — Signature Authority Delegation

**Normal operations:**
- **Primary:** Treasurer approves expenditures ≤ $25K.
- **Secondary:** Board Chair co-signs expenditures $25K–$100K.
- **Tertiary:** Full Board (≥ 4 directors) votes on expenditures > $100K.

**Contingency operations:**
- **Primary:** Acting Treasurer may approve expenditures ≤ $50K (increased threshold to allow operational flexibility).
- **Secondary:** Acting Board Chair co-signs expenditures $50K–$150K.
- **Tertiary:** Emergency-quorum Board (≥ 3 directors) votes on expenditures > $150K.

**Emergency spending authority (expedited):**
- The Executive Director may authorize **emergency operational expenditures ≤ $10K** without prior approval, provided they are necessary to maintain:
  - Registry uptime and security
  - Audit-panel operations
  - Insurance and compliance obligations
- All emergency expenditures must be documented and reported to the Board within 5 days.

---

### 7.2 — Banking Relationships & Pre-Documentation

**Pre-documented banking relationships:**
The Foundation maintains a **Banking Continuity Memo** (updated annually) listing:
- Primary bank, account number, authorized signatories.
- Wire-transfer routing number and instructions.
- Emergency access procedures (24-hour support line, escalation contacts).
- Backup bank (secondary account for geographic redundancy).

**Signatories (pre-authorized with the bank):**
1. Board Chair
2. Treasurer
3. Executive Director
4. Successor Board Chair #1

All signatories sign **banking authorization forms** annually, confirming their signature authority and delegation procedures.

**Continuity procedure:** If the primary treasurer is unavailable, the Acting Treasurer (designated by Board) contacts the primary bank, provides the Banking Continuity Memo, and confirms their authorization to conduct transactions on behalf of the Foundation.

---

### 7.3 — Funding Sourcing During Contingency

**Critical funding commitments (pre-negotiated):**
1. **CredexAI / Creativity Machine LLC** commits to continue sponsorship payments on schedule, even if Foundation is under contingency (formalized in sponsorship agreement, see FUNDING_PLAN §6).
2. **Major foundation grants** (Open Philanthropy, Long-Term Future Fund) include contingency language, allowing grantee to redirect funds to operational continuity if needed (without requiring prior approval for discretionary redirects ≤ 10% of annual grant).

**Actions during contingency:**
- Treasurer prioritizes preservation of **essential operational expenses** (panel honoraria, registry hosting, insurance).
- Non-essential expenses (travel, conferences, education programs) are deferred ≤ 90 days pending funding review.
- Board may request emergency funding support from CredexAI (formalized 0%-interest bridge-loan agreement, repayment from next grant tranche).

---

## §8 — Decision-Rights Matrix (Who Decides What During Continuity)

| Decision | Normal Authority | Continuity Authority | Quorum / Vote |
|---|---|---|---|---|
| **Predicate admission (Stage 3)** | Audit panel (5+) | Audit panel (3+) with [EMERGENCY-QUORUM] notation | ≥ 3 reviewers (vs. normal ≥ 5) |
| **Predicate rejection / tombstone** | Audit panel (5+) | Audit panel (3+) | ≥ 3 reviewers |
| **Scope-statement interpretation** | Board + Audit panel (joint) | Acting Board Chair + Audit Panel Chair (written memo) | 2 voices; escalate if disagreement |
| **Signature-key rotation** | Board Chair + Treasurer + Audit Panel Chair | Shamir ceremony custodians (≥ 5 of 7) | 5 shares reconstruct key |
| **Board chair succession** | Current Board Chair | Remaining board (≥ 3) affirm successor within 24h | Simple majority of ≥ 3 directors |
| **Emergency director appointment** | Board vote (≥ 4 of 7) | Acting Board Chair + Executive Director nominate; ≥ 3 directors affirm | Simple majority of available ≥ 3 |
| **Expenditures ≤ $10K** | Treasurer | Executive Director (emergency only) | Single authority |
| **Expenditures $10K–$50K** | Treasurer | Acting Treasurer | Single authority |
| **Expenditures $50K–$150K** | Board Chair + Treasurer | Acting Board Chair + Acting Treasurer | Joint co-signature |
| **Expenditures > $150K** | Full Board (≥ 4 of 7) | Emergency quorum (≥ 3 of 7) | Simple majority |
| **Audit-panel member replacement (primary→alternate)** | Board vote | Audit Panel Chair + Executive Director (no vote) | 2 voices, Executive Director notifies |
| **Transparency report publication** | Executive Director | Acting Executive Director + Acting Board Chair | Joint approval |
| **Foundation dissolution** | Board (supermajority 5+ of 7) | **NOT AUTHORIZED during contingency** | N/A |

---

## §9 — 6-Month, 12-Month, 24-Month Restoration Milestones

### 9.1 — 6-Month Milestone: Return to Normal Quorum & Board Composition

**Target:** By month 6 of contingency, the Foundation has restored:
- ≥ 5 active audit-panel members (full quorum)
- All 5 required-coverage board seats (≥ 1 director per area)
- Founder or designated successor has resumed primary leadership role

**Actions required:**
1. Recruit 2–3 panel members (from alternates or expedited nomination) to reach 5+.
2. Fill any empty board seats via open nomination (if required).
3. Executive Director documents restoration status in a **6-Month Continuity Review** memo (signed by Board Chair and Panel Chair).
4. Board votes (simple majority) to officially **EXIT EMERGENCY OPERATIONS** and return to normal governance (if all restoration targets met).

**If restoration incomplete:**
- Continue reduced-quorum operations.
- Escalate to Emergency Governance Review (§5.4).
- Extend restoration timeline to 12 months with revised milestones.

---

### 9.2 — 12-Month Milestone: Full Operational Normalization

**Target:** By month 12 of contingency:
- All continuity procedures are deactivated.
- All governance decisions made under reduced quorum have been reviewed by full quorum.
- Any retroactive reversals of emergency decisions are completed.
- Audit-panel and Board have returned to normal term schedules (no backlog of nominations).

**Actions required:**
1. Conduct full Audit Panel review of all **[EMERGENCY-QUORUM]** decisions made months 0–6.
   - Full quorum votes to affirm, modify, or reverse each decision.
   - Results documented in Continuity Transparency Log.
2. Executive Director publishes a **12-Month Continuity Final Report** (public), including:
   - Summary of trigger condition
   - Timeline of restoration actions
   - List of all decisions made under emergency quorum
   - Outcome of full-quorum review
   - Lessons learned and governance improvements
3. Board votes (simple majority) to officially **CLOSE CONTINGENCY** and exit all continuity procedures.

**If restoration incomplete:**
- Continue operational review and board/panel restoration.
- Publish 12-month interim report and revised restoration timeline.

---

### 9.3 — 24-Month Milestone: Governance Lessons-Learned & Structural Improvements

**Target:** By month 24 post-contingency:
- The Foundation has formally incorporated lessons learned from the contingency period.
- Governance structures and continuity procedures are updated based on experience.
- A post-mortem report is published (anonymized if sensitive) to benefit other similar organizations.

**Actions required:**
1. Board + Audit Panel conduct a **Continuity Lessons-Learned Review** (closed meeting, with notes published summary).
   - What went well?
   - What failed or was inefficient?
   - How should continuity procedures evolve?
2. Proposed amendments to bylaws, continuity plan, or governance framework are drafted.
3. Board votes (supermajority ≥ 5 of 7) to adopt amendments.
4. A **Governance Improvement Report** is published (with anonymized case study) for public distribution.

---

## §10 — Appendices & Implementation

### 10.1 — Pre-Continuity Checklist (To Confirm Before Contingency Occurs)

The Foundation must complete the following before contingency is triggered:

- [ ] Shamir Secret Sharing ceremony completed; 7 shares distributed and acknowledged by custodians.
- [ ] Successor board-chair names and contact info confirmed and publicly listed.
- [ ] Required-coverage alternate directors identified for all 5 coverage areas.
- [ ] Audit-panel alternates confirmed (with willingness statements).
- [ ] Named PR partner identified and agreement signed.
- [ ] Banking Continuity Memo completed and provided to all signatories + primary bank.
- [ ] Continuity Incident Mailing List populated and tested (email to all members).
- [ ] Continuity procedures document (this plan) reviewed by Board and published.
- [ ] Annual Shamir ceremony conducted (as governance drill) to validate procedures.

---

### 10.2 — Immediate Actions Upon Contingency Activation

**Day 0–1:**
1. [ ] Board Chair or designated person confirms contingency condition (phone/email).
2. [ ] Executive Director drafts Continuity Incident Notice and sends to all board + panel members.
3. [ ] Treasurer places Foundation accounts on "continuity alert" status (notify bank).

**Day 2–3:**
1. [ ] Emergency Board meeting convened (remote acceptable); quorum = ≥ 3 directors.
2. [ ] Board votes to formally activate continuity procedures.
3. [ ] Audit Panel Chair convenes panel and reviews continuity responsibilities.

**Day 4–7:**
1. [ ] Executive Director drafts public Continuity Incident Report.
2. [ ] PR partner reviews and provides media guidance.
3. [ ] Report published on Foundation website and sent to mailing list.
4. [ ] First weekly Continuity Status Update scheduled for day 14.

---

### 10.3 — Signatories & Effective Date

This Continuity Plan is adopted by the Calm Witness Foundation Board of Directors and Audit Panel on **[TBD: date of Board vote, post-incorporation]**. The plan becomes effective immediately upon adoption.

**Board approval:** [To be completed after first Board meeting post-incorporation]

---

## §11 — Governance Doctrine: Continuity as Resilience

The Calm Witness Foundation's continuity plan is an expression of a **governance doctrine**: that a healthy institution **must survive the loss or incapacity of any single person**, including the founder. This plan is designed to make the Foundation **fail-safe, not fragile**.

The seven-person Board with rotating terms, the five-person Audit Panel with staggered alternates, and the Shamir-share escrow of the signing key all reflect a single operating principle:

> **No predicate vocabulary, no governance decision, and no cryptographic authority shall depend on the permanent presence of any one individual.**

When this continuity plan is triggered, it is not a sign of failure. It is the Foundation *working as designed*.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
