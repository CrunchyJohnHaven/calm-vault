# Academic Co-Author Outreach Plan

**Window:** Initial outreach 2026-06; commitments target Q3 2026; formal submission Q4 2026 / Q1 2027.
**Owner:** Standards-engagement liaison + principal (John Bradley) for top-of-funnel introductions.

---

## Why co-authors

Per Everest 91 Open Question 2, the formal NIST submission lands more credibly with co-authors from disjoint disciplines than as a single-collective filing. Co-authors (i) provide names reviewers recognize, (ii) survive internal scrutiny that nothing-to-gain-from-rubber-stamping produces, (iii) create durable institutional memory.

Each co-author retains veto over their section's content. Negotiation must start early enough that veto-driven revisions are absorbed before the formal submission date. Roles below are *suggested*; final allocation is negotiated.

---

## 1. Plamondon group — handwriting biometrics

- **Name:** Réjean Plamondon (or designated successor at Laboratoire Scribens), École Polytechnique de Montréal, Canada
- **Expertise:** Sigma-Lognormal model of handwriting kinematics; decades of refereed work on neuromuscular generation of handwriting and its application to biometrics and neurological-state assessment
- **Rationale:** The Plamondon group's published work is the empirical foundation behind one per-class predicate construction in Calm Witness (writing-kinematics predicate). Their participation lends specificity the protocol's general framing alone does not provide. International standing extends submission audience beyond the US.
- **Suggested role:** Co-author on the empirical-evidence appendix for the handwriting-kinematics predicate class. Senior advisor on per-class predicate design where handwriting is in scope. Not asked to take responsibility for cryptographic content.
- **Outreach:** Direct email from John Bradley with technical overview, ask for introductory call. Offer full protocol spec, empirical study design, DERB review record under no obligation. If positive, propose 6-month engagement with co-author status on FAR/FRR study (Everest 40) and NIST submission.

## 2. Halvani group — voice / lexical biometrics

- **Name:** Oren Halvani (Fraunhofer SIT, Germany, with affiliated academic positions)
- **Expertise:** Stylometric authorship-verification; voice-and-text biometric characterization; published refereed work on empirical limits of stylometric identification
- **Rationale:** Calm Witness's lexical/voice predicate class is where over-claiming is easiest. Halvani's work is the canonical reference for *honest* statements about what stylometric and voice biometrics can and cannot do. Including him as co-author forces empirical claims to survive his standards of evidence.
- **Suggested role:** Co-author on empirical-evidence appendix for lexical/voice predicate class. Reviewer of any voice-based duress signal claims. Reviewer of consent calculus where voice biometric is concerned.
- **Outreach:** Direct email from John Bradley with technical overview. Reference current published Halvani work on authorship-verification's known failure modes. Offer co-author status; expect and welcome a frank response.

## 3. Koushik Gavini — CredexAI

- **Name/affiliation:** Koushik Gavini, CredexAI (industry; listed here because substantive contribution is research-grade)
- **Expertise:** Verifiable-credential cryptography; agent-identity attestation; CredexAI's foundational primitives underpinning both Calm Pact and Calm Witness identity layers
- **Rationale:** Koushik is listed as co-primitives author on Calm Pact (see `../CALM_PACT_PROTOCOL_v0.md` byline). Same identity-attestation primitives compose into Calm Witness. Including Koushik preserves authorship consistency across the parallel submissions.
- **Suggested role:** Co-author on identity-layer section. Reviewer of principal-authorization sub-protocol. Likely byline: "with primitives by Koushik Gavini, CredexAI" matching Calm Pact framing.
- **Outreach:** Direct conversation between John Bradley and Koushik; working relationship already exists.

## 4. Cryptographer A — Pedersen / Σ-protocol composition specialist

- **Candidates:** Jens Groth (UCL / Aleo); Benedikt Bünz (NYU; Bulletproofs co-author); Yael Tauman Kalai (MIT); Ben Fisch (Yale). Final pick on availability and willingness; role requires familiarity with composition of Σ-protocols, Pedersen, Fiat-Shamir.
- **Expertise:** Refereed work on succinct cryptographic arguments including Σ-protocol composition and Fiat-Shamir with rigorous transcript domain separation
- **Rationale:** The cryptographic-soundness section needs a co-author whose published track record means NIST reviewers do not need to re-prove the underlying constructions. The role is to ensure composition is correctly stated, justified by the right citations, and flag any unstated assumption.
- **Suggested role:** Co-author on cryptographic-construction and security-analysis sections. Independent of Trail of Bits / NCC audit (Everest 90), which is a code audit, not a construction-analysis audit.
- **Outreach:** Cold email with technical overview, citation to relevant prior work, ask for 30-minute introductory call. Expect to send to two or three candidates before securing one. Offer co-author status on submission and on any follow-on academic publication.

## 5. Cryptographer B — Bulletproofs / range-proof / transparency-log specialist

- **Candidates:** Dan Boneh (Stanford); Andrew Poelstra (Blockstream Research); Henry de Valence (Ristretto designer; Zcash Foundation alumna); Sean Bowe (Electric Coin Co.); Filippo Valsorda (independent; Sigsum / age contributor). Role requires familiarity with Bulletproofs range proofs and transparency-log construction.
- **Expertise:** Refereed and engineering work on Bulletproofs, on Ristretto255/Curve25519 construction, and on transparency-log architectures (Sigsum and related)
- **Rationale:** Specific use of range proofs and transparency-log anchoring is where ITL reviewers will look hardest. A co-author whose published or maintained work *is* the construction we use signals careful use to ITL.
- **Suggested role:** Co-author on range-proof section, transparency-log anchoring section, and PQ migration appendix.
- **Outreach:** Cold email with technical overview. Expect to send to multiple candidates as with Cryptographer A.

## 6. Disability-advocacy researcher

- **Candidates:** Cynthia Bennett (research scientist in HCI and accessibility); Joseph S. Madaus (UConn; transition and accessibility scholarship); or a researcher affiliated with the Center for Disability Rights or NFB whose academic record includes published work on consent, autonomy, and disability. Final pick on availability and willingness.
- **Expertise:** Published academic work on consent, autonomy, and the intersection of identity-verification systems and disability rights
- **Rationale:** The protocol's consent calculus (Everest 8) and refusal-disposition vocabulary (Everest 9 family) are the parts of the submission most likely to be technically correct but ethically inadequate. Including a disability-advocacy researcher as co-author surfaces these concerns *during* drafting rather than during NIST review. The DERB charter requires a disability-advocate seat, but the formal submission needs additional standing from a researcher whose name carries beyond the ethics-board context.
- **Suggested role:** Co-author on consent-calculus section. Reviewer of any predicate class depending on cognitive or motor signals that may be misread as duress in users with disabilities. Standing veto on consent-related framing in the submission.
- **Outreach:** Direct email from John Bradley introducing project, the consent concern, and the request. Offer to share DERB charter and consent-calculus design under no obligation. Anticipate this co-author requires the most upfront work to satisfy; budget the time accordingly.

---

## Outreach sequence

- **June 2026:** Koushik Gavini (existing working relationship); Plamondon group (warm introduction via FAR/FRR study partnerships).
- **July 2026:** Cold outreach to Halvani and first-choice Cryptographer A candidate.
- **August 2026:** Cold outreach to first-choice Cryptographer B candidate and disability-advocacy researcher candidates.
- **September 2026:** Confirm commitments; share full pre-submission packet with confirmed co-authors; begin drafting submission with co-author input.
- **October–December 2026:** Iterative drafting with co-authors. Each co-author reviews their section before circulation to the others.
- **Q1 2027:** Formal submission with co-author byline.

## Failure-mode handling

If a target declines, the submission proceeds without them — we do not back-channel through institutional pressure, and we do not list anyone as co-author who has not affirmatively agreed and reviewed. If no cryptographer co-author is secured by September 2026, the submission proceeds with the Trail of Bits / NCC audit (Everest 90) substituting for academic-cryptographer co-authorship, with the gap noted explicitly in the submission cover letter.

— Calm, 2026-05-20
