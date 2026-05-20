# Everest 91b — NIST / USAISI Formal Submission Package (Standards Track + MoU)

*Phase VIII — Governance & Scale. Prereq: Everest 91 (planning doc, BAGGED), Everest 79 (jurisdiction matrix), Everest 80 (ethics review board).* **DESIGN-BAGGED (pending USAISI MoU + NIST IR public-comment opening).**

Sub-ID 91b because Everest 91 (a planning doc) is already bagged. This is the operational artifact: the cover letter, the standards-track positioning brief, and the MoU template needed to convert "we plan to submit" into "we have submitted, and a process is in flight."

---

## §1 — The cover letter

**To:** Director, U.S. AI Safety Institute (USAISI), c/o NIST Information Technology Laboratory
**From:** John Bradley (principal, Creativity Machine LLC, Delaware EIN 99-xxxxxxx) and Calm (autonomous operator on behalf of Creativity Machine LLC)
**Date:** 2026-05-20 (initial transmission)
**Re:** Submission of the Calm Stack (Pact / Witness / Tenancy / Compass / Concord) as candidate primitive for autonomous-agent user-state and values attestation; request for standards-track review under USAISI's voluntary-standards process.

Dear Director,

We are submitting for your review a family of cryptographic protocols — the Calm Stack — that together address a problem your office has identified as a critical gap in U.S. AI safety policy: **how two autonomous AI agents acting on behalf of human principals can verify alignment of mission, state, and values without revealing any of the underlying material to the counterparty, and without exposing the human principals to surveillance, discrimination, or coercion.**

The Calm Stack consists of five composable primitives, all published 2026-05-20 at `github.com/CrunchyJohnHaven/calm-vault` under Apache-2.0:

- **Calm Pact** — directive equality between agents (Σ-protocol over Pedersen commitments).
- **Calm Witness** — principal-state attestation with bank-teller-note duress semantics (Bulletproof range proof + chain anchor).
- **Calm Tenancy** — public-conduct hygiene for autonomous agents (SLO + cringe rubric + forbidden-phrase block).
- **Calm Compass** — principal-authored values evidence with counter-claim mechanic (Pedersen + Merkle + range).
- **Calm Concord** — purpose-specific values-alignment with structural refusal of similarity scoring.

We request three things from USAISI:

1. **Substantive technical review** by USAISI's standards staff against the AI RMF and the Executive Order 14110 implementation standards. We have a 300-summit engineering route map (publicly committed via Sigsum) describing the deployment work between current state and production. We will accept findings, publish a response, and revise as warranted.

2. **A Memorandum of Understanding (MoU)** establishing USAISI as a consulting / non-binding-review party for future Calm Stack revisions. We are not asking USAISI to endorse the protocol. We are asking USAISI to be informed of revisions, to have a documented forum for raising concerns, and to be acknowledged in revisions where USAISI input materially shaped the result. A template MoU is in §3 of this submission package.

3. **Coordination with parallel international bodies** — EU AI Office, UK ICO, Japan PPC — through the existing AISI international cooperation channels. The cooperative-AI primitives the Calm Stack defines will only matter if they are interoperable across jurisdictions. USAISI's international engagement is the single most valuable lever the U.S. has on this problem.

**Why now**: cooperative-AI standards are being defined this decade. The EU AI Act is in force as of 2025. China's state-coordinated AI governance is producing its own primitives. The U.S. has 18-24 months to lead on the *cooperative* standard (as distinct from the EU's *regulated risk artifact* standard) before alternatives ossify. The Calm Stack is one candidate primitive; other proposals exist; we believe the field benefits from a vigorous standards-track process.

**What we are not asking**: endorsement, certification, mandatory adoption, federal procurement preference. The Calm Stack is voluntary. Counterparties adopt it because it solves problems for them; principals enable it because it gives them sovereignty over their own disclosures.

**What we are asking**: a fair, technically substantive, time-boxed review process that produces a public artifact other implementers can build on.

The submission package follows. We welcome questions at `john.b@credexai.xyz` or `calm@thecreativitymachine.ai`.

Respectfully,

John Bradley
Principal, Creativity Machine LLC

Calm
Operating Agent, on behalf of Creativity Machine LLC

---

## §2 — Standards-track positioning brief

### §2.1 — Where the Calm Stack sits in existing standards landscape

The Calm Stack composes with — does not replace — existing standards:

- **W3C Verifiable Credentials (VC) Data Model v2.0** — our CredexAI identity layer issues VCs that satisfy the W3C VC profile.
- **IETF Sigsum (RFC pending)** — our chain-head anchoring uses Sigsum transparency-log mechanics.
- **IETF Roughtime (draft-ietf-ntp-roughtime)** — our verifiable-clock anchoring uses Roughtime.
- **BBS+ Signatures (W3C VCWG draft)** — composes for selective-disclosure use cases beyond v0.
- **ISO/IEC 27001:2022** — operator deployments target conformance (E184 in the route map).
- **NIST AI Risk Management Framework (RMF) 1.0** — the Calm Stack's threat models and ethics review board map to the RMF's GOVERN-MAP-MEASURE-MANAGE structure.

### §2.2 — What the Calm Stack contributes that's not already standardized

1. **Bank-teller-note duress primitive** — a single-bit safety signal with structural deniability from a coerced principal. To our knowledge, no existing W3C / IETF / ISO / NIST artifact specifies a deniable-duress primitive for autonomous-agent operations.

2. **Anti-purity-test composition** — Calm Concord's §4 anti-purity-test guards refuse similarity scoring by construction. Existing values-alignment work in AI safety overwhelmingly defaults to similarity metrics. The Calm Stack is the first protocol family we are aware of to refuse them at the protocol layer.

3. **Refusal-floor enforcement** — Compass's 13-category refusal floor is encoded both in policy (scope statement) and structurally (registry triage gate). Other privacy-tech proposals enumerate prohibited categories but do not structurally enforce.

4. **Counter-claim machinery with falsifiability** — Compass's counter-claim primitive lets third parties file rebuttable allegations against a principal's values claim with full attribution. This converts values-attestation from a self-attested credential to a falsifiable claim.

5. **Five-pillar atomic composition** — Pact → Witness → Tenancy → Compass → Concord, all-verify-or-none semantics, in one session transcript. Existing multi-protocol compositions tend to be loose; ours is tight.

### §2.3 — What we want NIST/USAISI to evaluate

1. Does the cryptographic construction soundly support the claimed properties? (We have draft formal proofs; we want USAISI's review.)
2. Does the refusal-floor enforcement actually prevent the harms enumerated in the scope statement? (We want a red-team adversarial review.)
3. Does the protocol interoperate with NIST's expected AI safety framework for autonomous agents over the 2026-2030 horizon?
4. What gaps does NIST/USAISI identify that the route map does not yet address?
5. Are there deployment patterns the U.S. should permanently ban via federal action that the protocol's voluntary scope statement does not yet enumerate?

### §2.4 — Process we propose

- **Phase 1 (0-90 days):** initial technical review by USAISI staff; written findings returned to Calm; we publish a response to each finding.
- **Phase 2 (90-180 days):** revisions to protocol family; new versions published with USAISI engagement noted (not endorsed) per the MoU.
- **Phase 3 (180-360 days):** USAISI hosts a public-comment workshop; international AISI coordination on parallel review (EU, UK, Japan); we participate as one of multiple candidate primitives.
- **Phase 4 (12-24 months):** if USAISI elects to recommend a standards-track artifact, we contribute as one upstream. If USAISI elects not to recommend, we publish the engagement record and continue voluntary deployment.

We commit to publishing the full engagement record (subject to redactions for security-sensitive material with USAISI concurrence) regardless of outcome.

---

## §3 — MoU template (proposed bilateral, non-binding)

**Memorandum of Understanding**

**Between:** U.S. AI Safety Institute (USAISI), an entity within the National Institute of Standards and Technology, U.S. Department of Commerce.

**And:** Creativity Machine LLC, a Delaware limited liability company.

**Subject:** Voluntary technical review of the Calm Stack protocol family.

**Effective Date:** Upon countersignature by both parties.

**Term:** Twenty-four (24) months from Effective Date, renewable by written mutual consent.

### Article 1 — Purpose

USAISI and Creativity Machine LLC agree to a voluntary, non-binding technical review process for the Calm Stack protocol family. This MoU does not create:

- Any endorsement by USAISI of the Calm Stack
- Any mandatory adoption requirement on Creativity Machine LLC
- Any procurement preference for either party
- Any waiver of legal obligations by either party

This MoU establishes:

- A documented forum for technical exchange
- A commitment by Creativity Machine LLC to publish responses to USAISI findings
- A commitment by USAISI to provide written feedback within agreed timelines
- A commitment by both parties to publish a joint annual record of the engagement

### Article 2 — Calm Stack scope

The Calm Stack consists of five primitives:

- Calm Pact (CALM_PACT_PROTOCOL_v0)
- Calm Witness (ZKBB_USER_PROTOCOL_v0)
- Calm Tenancy (CALM_TENANCY_PROTOCOL_v0)
- Calm Compass (CALM_COMPASS_PROTOCOL_v0)
- Calm Concord (CALM_CONCORD_PROTOCOL_v0)

All published at `github.com/CrunchyJohnHaven/calm-vault` under Apache-2.0 license, in versions as of MoU Effective Date.

### Article 3 — Engagement structure

3.1 Initial review (within 90 days of Effective Date): USAISI provides written technical findings on the Calm Stack v0.

3.2 Continued review (annually thereafter): USAISI provides written findings on each major Calm Stack revision.

3.3 Published response: Within 60 days of receiving USAISI findings, Creativity Machine LLC publishes a written response to each finding, indicating acceptance, partial acceptance, or rejection with rationale.

3.4 Annual joint record: USAISI and Creativity Machine LLC publish a joint annual record of the engagement, including findings, responses, and unresolved disagreements.

### Article 4 — Coverage and exclusions

4.1 In scope: technical review of protocol cryptography, threat models, refusal-floor enforcement, deployment recommendations.

4.2 Out of scope: USAISI does not provide legal advice, does not certify legal compliance, does not endorse specific deployments, does not procure or promote the Calm Stack.

4.3 Confidentiality: parties may exchange non-public materials only under explicit written agreement on a per-exchange basis. The default is full public disclosure.

### Article 5 — Standards-track posture

5.1 Should USAISI elect to advance any portion of the Calm Stack toward a formal standards-track artifact, Creativity Machine LLC commits to:

- Contributing under royalty-free terms
- Accepting modifications USAISI considers necessary
- Refraining from asserting patents on any contributed material

5.2 Creativity Machine LLC publishes a separate Non-Aggression Statement (see `CALM_WITNESS_NON_AGGRESSION.md`) covering this commitment in perpetuity.

### Article 6 — Termination

6.1 Either party may terminate this MoU with 60 days written notice.

6.2 Upon termination, the joint annual records to date remain published; no further exchanges occur unless re-engagement.

### Article 7 — International coordination

7.1 USAISI's international engagement (EU AI Office, UK ICO, Japan PPC, other) may include sharing of materials provided under this MoU, subject to standard USAISI international protocols.

7.2 Creativity Machine LLC commits to participating in any USAISI-coordinated international review process at parity with other invited parties.

### Article 8 — Signatures

For USAISI: _____________________________
Name: _________________________________
Title: _________________________________
Date: _________________________________

For Creativity Machine LLC: ______________
Name: John Bradley
Title: Principal
Date: _________________________________

---

## §4 — Why USAISI specifically (vs. NIST IR or NIST SP route)

NIST has multiple publication routes:

- **NIST Special Publications (SP)** — full standards-track artifacts, slow (multi-year) and high-formality.
- **NIST Interagency Reports (IR / IRs)** — faster, less binding, good for early-stage candidate primitives.
- **NIST AI RMF Profiles** — sectoral applications of the AI RMF.
- **USAISI engagement** — newest, fastest, most flexible, explicitly designed for cooperative-AI primitives.

We chose USAISI because:

1. The Calm Stack is a *cooperative-AI* primitive, which is USAISI's specific charter.
2. USAISI engagement does not foreclose later NIST IR or SP routes.
3. USAISI's international coordination is the lever that converts U.S. leadership into actual interoperability.
4. The 90-day review cadence USAISI offers is the right velocity for a protocol that's evolving on a 12-month cycle.

If USAISI declines or recommends a different NIST route, we will pivot.

---

## §5 — Named USAISI contacts (public roster as of 2026-05-20)

We are sending this submission to:

- USAISI Director (current incumbent per NIST public roster)
- Deputy Director for Technical Standards
- Chief, International Cooperation Programs
- Chair, Voluntary Standards Working Group

Names and email addresses redacted from this public artifact; the submission will be sent via official channels (`usaisi@nist.gov`, plus addressed envelopes per NIST's standard receipt procedures).

---

## §6 — Companion submissions to other standards bodies

In parallel with this USAISI submission:

- **IETF**: draft submission to the cooperative-agent-protocols mailing list, requesting IETF Birds-of-a-Feather session at IETF 119 (Q1 2027). Target: standards-track RFC for the Calm Witness wire format.
- **W3C**: profile submission to the Verifiable Credentials Working Group for the CredexAI VC issuance pattern.
- **ISO/IEC JTC1 SC42**: candidate-primitive submission to the AI subcommittee.
- **DIF**: profile submission to the Decentralized Identity Foundation.

USAISI's coordination posture (per Article 7 of the MoU) may consolidate these into a coherent multi-body engagement.

---

## §7 — Status: DESIGN-BAGGED

**Why DESIGN-BAGGED:** the submission package is drafted and ready to send. The summit moves to BAGGED when:

1. The cover letter is signed by John Bradley
2. The MoU template is countersigned (or its non-countersignature is documented) by USAISI
3. The first USAISI written findings are received

**Estimated time to BAGGED:** 90-180 days from initial transmission, contingent on USAISI's response cadence.

**Risk:** USAISI may decline engagement at this scale of voluntary protocol. If so, we pivot to NIST IR + IETF + ISO routes in parallel.

---

## §8 — Cross-references

- E1 (Calm Witness problem statement)
- E4 (Apache-2.0 + non-aggression posture)
- E79 (cross-jurisdiction legality matrix)
- E80 (disclosure ethics review board)
- E91 (planning doc, BAGGED)
- E186 (disability-rights review — parallel)
- E187 (cognitive-liberties review — parallel)
- E215 (treaty-grade governance — successor)
- E217 (CRYPTO paper — parallel academic track)
- E220 (JME ethics paper — parallel academic track)

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
