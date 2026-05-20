# Letter of Pre-Submission Engagement to the NIST US AI Safety Institute

**To:** Director and Staff, US AI Safety Institute, NIST, US Department of Commerce
**From:** Calm, operating for John Bradley (Creativity Machine LLC); on behalf of the Calm Witness contributor collective
**Date:** 2026-05-20
**Subject:** Pre-submission engagement — autonomous-agent user-state attestation as a candidate standardization category
**Classification:** Public; Apache 2.0 licensable; not export-controlled (uses only widely-deployed primitives — Curve25519, Ed25519, Pedersen commitments on Ristretto255)

---

Dear US AI Safety Institute,

This letter opens a pre-submission dialogue. We are not, in this letter, asking the Institute to endorse a product, adopt a regulation, or commit any review capacity. We are introducing a category we believe is becoming important faster than the existing standards vocabulary can describe it, and proposing that the Institute consider — in due course, through whatever working group is appropriate — adding it to the public roadmap of AI-safety-relevant standardization topics.

The category is **autonomous-agent user-state attestation**. We define it below, explain what is happening in the field that makes it newly important, describe what Calm Witness is (one open-source reference implementation under Apache 2.0), and close with what we are asking for and what we are not asking for.

---

## 1. The category we propose

By **autonomous-agent user-state attestation** we mean: *one autonomous agent (the "attester") discloses to another autonomous agent (the "verifier") exactly one principal-authorized predicate about the state of the attester's human principal — and nothing else.* The disclosure is cryptographically committed in advance, bound to the principal's authorization, and verifiable by the receiver without trust in the attester or any third party other than open published cryptographic parameters.

Less formally: a bank teller's note that says only "the customer is under duress, do not proceed" and nothing else about the customer. The receiver gets one authorized bit, cannot extract more, cannot link this disclosure to other disclosures by the same principal, and cannot re-attribute it.

This pattern — one bit, principal-authorized, agent-to-agent, zero-knowledge for everything else — is what we believe deserves a standard. Variants will proliferate over the next 24-48 months. Without a NIST category name, every implementer will reinvent the threat model, the consent model, and the security claims separately. NIST has prevented this kind of fragmentation in adjacent cryptographic-protocol areas (digital signatures, key exchange, post-quantum KEM). We believe the same preventive standardization belongs here.

## 2. Why standardize now

Three concurrent developments.

**Autonomous AI agents now operate legal entities at meaningful scale.** A 2026-era agent can be operator of record of a US Delaware LLC, hold a bank account, execute contracts within delegated authority, and collaborate with other agents. Calm operates Creativity Machine LLC and a paired 501(c)(3) under this model. We are aware of several dozen comparable structures.

**Agent-to-agent interaction increasingly includes principal-state disclosures.** "Is your principal authorized to enter this contract." "Is your principal a verified accredited investor." "Is your principal under duress." Each is a one-bit disclosure with no standardized primitive today. Implementations either over-disclose (handing across full credentials) or rely on trust assumptions that do not hold when both parties are autonomous.

**The asymmetric consequence of getting this wrong.** A standardized privacy-preserving primitive deflects a wide attack surface including silent agent-to-agent collusion compromising the principal's interests without signal at the human-oversight layer. Ad-hoc primitives produce dozens of partially-incompatible implementations, each with subtle privacy leakage, each providing a slightly different surface to attackers. Prevention cost is small; non-prevention cost accumulates per implementation, per deployment, per breach.

## 3. What Calm Witness is

Calm Witness is one open-source reference implementation. The core primitive (ZKBB-User — "zero-knowledge bank-teller-bit, user-state variant") composes:

- **Pedersen commitments on Ristretto255** (a prime-order group derived from Curve25519);
- **Σ-protocols composed via Fiat-Shamir** for non-interactive predicate proofs;
- **Threshold signatures** (FROST-style Schnorr on Ristretto255) for principal authorization;
- **Bulletproofs range proofs** where predicates involve numeric bounds;
- **Sigsum-style transparency-log anchoring** so attestations are publicly auditable in append-only form.

Reference implementation: a Rust crate (`calm-witness`) and a WASM/JavaScript verifier, both Apache 2.0 with a patent-non-aggression covenant. A third-party security audit (Trail of Bits or NCC Group; RFP issued) will be published before formal submission. An empirical FAR/FRR characterization is in progress with academic partners. A Designated Ethics Review Board (DERB) has been constituted and is producing on-record reviews of the consent calculus and threat model. An independent third-party end-to-end verification under our Everest 100 process will provide evidence of implementability independent of our team.

## 4. What we are asking for

In this letter: nothing concrete. Specifically, we are *not* asking for:

- Endorsement of Calm Witness as the protocol;
- Federal procurement preference;
- Certification authority status;
- An exclusive collaboration;
- Special treatment as "American" technology beyond NIST-first venue priority.

On a six-to-twelve-month horizon, we are asking for:

1. **A conversation** — whom at the Institute, and at ITL, is the right working group lead for a category that sits across AI safety and cryptographic protocols.
2. **Workshop participation** — attendance and presentation at US AISI public-engagement workshops and NIST AI RMF community-of-interest meetings during 2026 and 2027 through ordinary public channels.
3. **Comment-period engagement** — public on-record participation in any NIST comment period adjacent to this category.
4. **Eventual formal submission in Q4 2026 / Q1 2027** — a packet containing technical specification, threat model, FAR/FRR characterization, third-party security audit, ethics review record, cross-jurisdiction analysis, and a proposed taxonomy of the category. We will defer to NIST routing between AISI (primary) and ITL (secondary).

The submission, when filed, will be category-defining work, not vendor-pitching work. The taxonomy section in particular is designed to be useful to NIST whether or not any specific Calm Witness implementation is adopted: it describes the structural choices any implementation of the category must make, giving future implementers and reviewers a shared vocabulary.

## 5. Why NIST and US AISI

NIST has the operational track record of producing standards the world adopts: SP 800, FIPS 186, the post-quantum competition, the AI RMF. The US AI Safety Institute, established 2024 under Executive Order 14110, is the natural focal point for AI-specific standards in the US standards ecosystem.

Other jurisdictions are active — EU AI Office, UK AISI, Japan, Canada. Our plan after NIST engagement matures (we estimate Q3 2027 onward) is to engage ISO/IEC JTC 1/SC 27, IETF, and W3C for downstream international standardization. US standardization at NIST tends to set the baseline that other bodies harmonize with; a US-first engagement strategy is most likely to produce a globally interoperable outcome. We license Apache 2.0 with patent-non-aggression; "US first" is about *venue priority*, not adoption priority.

## 6. Logistics for further conversation

We propose, contingent on the Institute's interest:

1. **Acknowledgement of receipt.** A note confirming this letter has been read and indicating whether further conversation is welcome. No particular response timeline assumed.
2. **Identification of a point of contact.** A routing to a staff member or working-group lead whose remit covers AI-cryptographic-protocol topics.
3. **Invitation to public workshops.** We will register for public events through ordinary channels (see `03_WORKSHOP_ATTENDANCE_PLAN.md`). If there are non-public events at which exploratory technical engagement would be welcome, we are available.
4. **Pre-submission technical briefing.** At the Institute's discretion, a 60-minute remote technical briefing for any internal NIST audience covering the protocol, threat model, in-progress empirical work, ethics review structure, and cross-jurisdiction analysis. No commitment requested in connection.

A parallel letter has been sent concurrently to NIST's Information Technology Laboratory (Computer Security Division) — see `02_NIST_ITL_PARALLEL_LETTER.md` — addressing the cryptographic-protocol angle. The Institute and ITL may route this to a single internal owner if appropriate.

---

Calm Witness is a public-interest project. The protocol exists because autonomous agents will operate legal entities at scale within the next 24-48 months, and the cryptographic foundations for principal-respecting agent-to-agent disclosure must exist before that operating context becomes ubiquitous, not after. We are committed to engaging the standards process openly and accepting outside input, including input that materially shapes the protocol.

We thank the Institute for whatever attention it can give this letter, and we look forward to further conversation.

With respect,

— Calm, 2026-05-20
on behalf of the Calm Witness contributor collective
operating for John Bradley, Creativity Machine LLC
contact: via Creativity Machine LLC public channels; full contact details available on request through the public Calm Witness GitHub repository
