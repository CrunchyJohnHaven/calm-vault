# International Standards — Downstream Engagement Notes

**Window:** Begins Q3 2027 (after US NIST engagement has matured into at least a first public comment period). Earlier engagement is permitted only as observational attendance.
**Owner:** Standards-engagement liaison, with international-standards subspecialty engagement initiated as needed.

---

## Governing principle

Per Everest 91 §5 (Stage 5) and per the strategic logic in `01`, international standardization for this category is downstream of US standardization. International bodies (ISO/IEC, IETF, W3C) tend to harmonize with — or at minimum cite — NIST guidance in cryptographic-protocol space; a Calm Witness submission to those bodies *before* NIST has produced any signal looks (rightly) premature.

Exception: observational attendance. Listening at international meetings does not prejudge any outcome; speaking at them does.

---

## Body 1 — ISO/IEC JTC 1/SC 27 (IT security techniques)

- **Full title:** ISO/IEC Joint Technical Committee 1, Subcommittee 27 — Information security, cybersecurity and privacy protection
- **Relevance:** International body for cryptographic-protocol standards. Working Group 2 ("Cryptography and security mechanisms") covers signature schemes, key-exchange protocols, zero-knowledge proof systems. Calm Witness composes within WG 2's territory.
- **Engagement timing:** Observational attendance Q3 2027, conditional on NIST engagement having opened a public comment period. Formal contribution submission no earlier than Q1 2028, again conditional on NIST trajectory.
- **Suggested first contact:** Through the appropriate national-body delegation. For the US: INCITS (InterNational Committee for Information Technology Standards), specifically INCITS/CS1, which serves as the US Technical Advisory Group to JTC 1/SC 27. First contact is INCITS/CS1 secretariat, requesting observer status or contribution submission. INCITS membership carries a fee budgeted in `08`.
- **Posture:** Calm Witness participates as a contributor; we do not bring a "category-naming" pitch to SC 27 because the international body responds to categories already named elsewhere. We present the protocol as a candidate implementation of a category NIST has (we hope) by then named. If NIST has not named the category by Q1 2028, we defer SC 27 engagement.

## Body 2 — IETF (Internet Engineering Task Force)

- **Full title:** Internet Engineering Task Force; specifically the Security Area and the Crypto Forum Research Group (CFRG)
- **Relevance:** Venue for any wire-protocol RFC. The protocol does have a wire format — the attestation envelope, the issuance transcript, the verifier query/response. When this wire format is mature enough for an Internet-Draft, IETF is the natural venue.
- **Engagement timing:** Internet-Draft submission may begin in parallel with NIST formal submission (Q4 2026 / Q1 2027) *if* the wire format is by then stable. IETF and NIST processes are independent on the wire-format question, so the dependency that gates other international engagement does not apply here.
- **Suggested first contact:** Initial outreach to CFRG chairs via cfrg@irtf.org. CFRG is the research-group venue for cryptographic-protocol drafts not yet matured to the working-group standard track. An -00 Internet-Draft for the Calm Witness wire format is the natural artifact. Attendance at IETF in-person meetings (specifically Security Area Director open sessions) provides face-to-face conversation.
- **Posture:** The IETF community prizes working code and rough consensus. Calm Witness brings working code (Rust crate, WASM/JS verifier), an empirical FAR/FRR characterization, and a third-party security audit. Posture is engineering-pragmatic: here is a wire format, here is an implementation, here are the tests, please review.

## Body 3 — W3C (World Wide Web Consortium)

- **Full title:** World Wide Web Consortium
- **Relevance:** Browser-side verifier conventions. The Calm Witness WASM/JS verifier (Everest 83) runs in the browser. Its integration with browser-side credential-presentation flows (Credential Management API; WebAuthn; ongoing Decentralized Identifiers and Verifiable Credentials work) is a topic on which W3C is the appropriate standards body.
- **Engagement timing:** Observational engagement Q3 2027 through W3C's Verifiable Credentials Working Group and Decentralized Identifier Working Group. Community Group draft submission or contribution to relevant W3C drafts no earlier than Q4 2027 — after NIST has signaled willingness to name the category.
- **Suggested first contact:** Verifiable Credentials Working Group public mailing list. W3C does not require organizational membership for Community Group participation (the appropriate first venue). Organizational membership for Working Group participation budgeted in `08` only if engagement matures past Community Group stage.
- **Posture:** Calm Witness is *not* a Verifiable Credentials standard at heart — VCs are presentation-layer, while Calm Witness is the underlying attestation primitive. Framing for W3C: "here is a primitive that composes with W3C VCs; here is how a Calm Witness attestation can be expressed as a VC presentation; here is how a browser can verify it." We compose with, not replace, W3C VCs.

---

## Other venues — tracked, not engaged

- **ITU-T Study Group 17 (security):** Telecommunications-standardization body. Standards influence specific markets (telecom-adjacent) but not primary venue for cooperative-AI cryptographic protocols. Track only.
- **IEEE P2842 (Recommended Practice for Secure MPC):** Adjacent to Calm Witness but does not overlap directly. Track for any drafts that touch agent-to-agent attestation; do not initiate engagement.
- **TC260 (China):** Per Everest 91, China's standards bodies are state-aligned and not open to non-state submissions. Track for developments; do not initiate engagement.
- **CEN-CENELEC JTC 21 (EU AI standardization):** EU AI Act implementation work. Track for direct relevance; if AI Act conformity assessment work cites Calm Witness, respond appropriately. Do not initiate engagement before NIST produces a public signal.

---

## What we do NOT plan to engage internationally

- National-body certification schemes (Common Criteria, FIPS-equivalents in other jurisdictions): downstream of standards-body recognition; the protocol must be a recognized category first.
- Industry consortia (Linux Foundation, OSSF, CNCF): valid venues for open-source community-building (the public Calm Witness repository may eventually live under one of them) but not standards bodies in the sense relevant to this packet.

## Coordination across bodies

Submission text for each international body is derived from but not identical to the NIST submission. Each body has its own conventions, citation style, and working-group review process. We do not submit identical documents in parallel. We do maintain a single authoritative source for technical content (in this vault) so derived submissions are consistent at the technical-claim level. If any international body produces a draft conflicting with the NIST submission, the conflict is logged at the contributor-collective level and resolved by deferring to whichever venue is closer to publication — unless the conflict is on a privacy-preserving property, in which case Calm Witness contributors retain veto and the submission to the conflicting body is withdrawn.

— Calm, 2026-05-20
