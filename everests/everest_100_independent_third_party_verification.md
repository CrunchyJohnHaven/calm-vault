# Everest 100 — Independent Third-Party End-to-End Verification

*Phase VIII — Governance & Scale. Prereq: Everest 92, 98, 99. THE FINAL SUMMIT.*

---

## Overview

Everest 100 is the planned milestone at which an organization independent of Calm Foundation and Creativity Machine LLC performs end-to-end verification of the Calm Witness protocol. Using only publicly released documentation and software development kits, the independent verifier constructs a complete test of the system — from enrollment through chain anchoring, biometric evaluation, predicate assessment, and disclosure proof verification — and publishes their findings in a public report.

This milestone represents the moment at which the open-standard claims embedded in Calm Witness graduate from *design claims* to *externally validated facts*. Everests 1–99 are an expedition led by the protocol's creators. Everest 100 is the expedition's handoff to the broader technical community.

The independent verification is not a security audit. It is not a formal cryptographic proof. It is not a conformance certification. It is a thorough, systematic walk-through of the entire protocol by a third party with no vested interest in the outcome and no access to pre-release information. The third party publishes what they found: what worked, what surprised them, what edge cases they discovered, what assumptions they had to make when the spec was ambiguous, and whether the open-standard promise — that someone outside Calm can build, test, and verify the protocol — held.

---

## Acceptance Criteria

Everest 100 is bagged when:

1. **An independent organization** (not Creativity Machine LLC, not Calm Foundation, not signatories to the funding agreement that brought Calm Witness into existence) has publicly announced their intention to verify the protocol end-to-end.

2. **That organization has completed** a full walk-through of the Calm Witness system, including:
   - Obtaining and parsing the published source code (Everest 92).
   - Reading the counterparty implementer's guide (Everest 98).
   - Building and running the reference Python SDK or Rust crate.
   - Constructing a synthetic principal (a test identity with enrolled biometrics or synthetic biometric substitutes).
   - Performing a complete session: self-report + optional biometric capture + chain anchoring + predicate evaluation + proof generation + proof verification.
   - Exercising at least three distinct predicates.
   - Testing at least one edge case per predicate (boundary condition, empty input, malformed envelope, stale freshness window, revoked consent).
   - Verifying chain-head publication to a Sigsum transparency log (or simulating it with a mock verifier if live logs are not accessible).
   - Attempting at least two adversarial tests (proof mutation, timestamp forgery, consent override attempt).

3. **That organization has published a report** documenting:
   - Which parts of the protocol specification were clear and implementable as written.
   - Which parts required clarification or interpretation.
   - The results of their synthetic proofs: did every step work as specified?
   - Any deviations from the spec they encountered or had to work around.
   - Any edge cases they discovered that the spec did not cover.
   - Their assessment of whether the protocol, as documented, is reproducible by others.
   - Their confidence in the cryptographic assumptions (with explicit caveats if they did not perform an independent cryptographic review).
   - Any recommendations for the specification's next iteration.

4. **The report is published in an open venue**, accessible without login or paywall, and linked from the official Calm Witness documentation site.

5. **Calm Foundation has responded** to the independent verifier's report (within 30 days of its publication) with:
   - Acknowledgments of any identified ambiguities or bugs in the spec or code.
   - A timeline for addressing reported issues (if any).
   - Clarifications where the spec was correctly written but misunderstood.
   - No demands, no edits to the verifier's report, and no NDAs.

---

## Independent Verifier Profile

The independent verifier should be an organization with all of the following characteristics:

- **Neutral or orthogonal motivation.** The organization should have no financial stake in Calm Witness adoption, no board member overlap with Creativity Machine LLC, and no prior contractual relationship with Calm Foundation. Funding is acceptable if it is arms-length (e.g., "perform verification and publish findings") and does not require Calm Foundation approval of the findings before publication.

- **Cryptographic or security credibility.** The organization should have demonstrated expertise in cryptography, zero-knowledge proofs, or security auditing. This can be evidenced by prior publications, audits of other protocols, or staff credentials.

- **Accessibility and pedagogy.** The organization should be accustomed to explaining technical findings to audiences outside their immediate field. The report should be readable by other AI-safety researchers and protocol designers, not just cryptographers.

- **Public commitment to findings.** The organization should be willing to publish findings in full, including findings that are critical or identify ambiguities in the specification.

Candidate verifier classes:

1. **Academic cryptography research group.** E.g., a university laboratory with a publication record in zero-knowledge proofs or protocol verification. Ideal because academics are accustomed to peer-reviewed publication and have institutional incentive alignment toward clarity and rigor.

2. **AI-safety research organization.** E.g., a nonprofit focused on AI alignment or autonomous-agent safety. These organizations understand the use case (human-state attestation to AI agents) and bring a perspective on safety implications beyond cryptography.

3. **Open-source security foundation.** E.g., a foundation that audits or analyzes protocols in the open-source commons. These organizations often have established practices for publishing findings.

4. **Peer organization operating autonomous-agent collectives.** E.g., another organization that runs AI agents on behalf of humans and would directly benefit from Calm Witness as a counterparty verifier. Their perspective as a user of the protocol is valuable.

5. **Hybrid: disability advocacy + cryptography.** E.g., an organization focused on disability rights and digital access, paired with a cryptographer. This pairing brings both the principal-protection and technical perspectives that Everest 100 is designed to test.

Organizations with a track record of public reporting on protocol or system design are strongly preferred. Organizations that have not previously published technical reports may be accepted only if they have explicit mentorship or collaboration with an organization that has.

---

## Verification Checklist

The independent verifier should work through the following checklist and explicitly document their findings for each item:

### A. Protocol Specification Clarity

- [ ] Can the specification be read cover-to-cover without external context?
- [ ] Where does the specification reference other documents (Calm Pact, NIST standards, etc.) — are those documents readily accessible, or does comprehension require prior knowledge?
- [ ] Is the threat model unambiguous? Can you articulate what adversaries Calm Witness defends against and which it does not, using only the published spec?
- [ ] Are the predicate definitions in the predicate vocabulary precise enough to implement without guessing?
- [ ] Is the disclosure schema fully specified? Can you construct a valid disclosure envelope by hand, byte-by-byte, using only the spec?

### B. Source Code Reproducibility

- [ ] Does the published source code (Everest 92) match the claims in the specification?
- [ ] Are the dependencies documented and pinned? Can you install the SDK in a clean environment without manual intervention?
- [ ] Do all provided test cases pass on your hardware? (Report your OS, CPU, and any deviations.)
- [ ] Are there code paths or functions that are documented in the spec but missing from the source, or vice versa?
- [ ] Can you build the code without warnings or errors?

### C. Chain Construction & Verification

- [ ] Generate a chain with 10+ records using the SDK.
- [ ] Verify the chain tip-to-bottom using the provided chain verifier.
- [ ] Mutate one byte in a record and attempt to verify — does the verifier correctly reject it?
- [ ] Mutate a `prev_hash` and attempt to verify — does the verifier flag the break in the chain?
- [ ] Does the chain-head publication to Sigsum (or your mock of it) work as described?

### D. Biometric Distance Functions

- [ ] For handwriting: obtain samples (or use provided synthetic samples), compute distances to an enrolled template, and verify the distance falls in the expected range `[0, 1]`.
- [ ] For voice transcription: verify that transcription is produced locally and no audio persists after evaluation.
- [ ] Do the distance functions produce deterministic output for identical inputs?
- [ ] Test boundary conditions: distance = 0, distance = 1, very short input, very long input, empty input.

### E. Predicate Evaluation

- [ ] For at least three predicates, construct a test case where the predicate should evaluate to True and verify it does.
- [ ] For each of those predicates, construct a test case where it should evaluate to False.
- [ ] Test one predicate with an empty chain — does the evaluator handle it correctly?
- [ ] Test one predicate with a malformed chain record (missing required field, wrong type) — does the evaluator reject it or handle gracefully?
- [ ] Test one predicate where the consent record is not present — does evaluation correctly respect the "default deny" principle?

### F. Proof Generation & Verification

- [ ] Generate a Pedersen commitment to a bit and verify it matches the spec.
- [ ] Generate a zero-knowledge proof that a committed bit is True and verify it yourself.
- [ ] Mutate the proof (change one byte) and attempt to verify — does it correctly reject?
- [ ] Verify that proof generation is deterministic (same inputs → same proof).
- [ ] Generate a proof with a commitment to an out-of-range value and document whether the proof system allows or rejects it.

### G. Disclosure Envelope Construction

- [ ] Build a disclosure envelope requesting one predicate; verify the signature.
- [ ] Build an envelope requesting three predicates; verify no unrequested predicates appear.
- [ ] Build an envelope for a predicate where the principal has not granted consent; verify the predicate is omitted (silent refusal).
- [ ] Verify that two envelopes for the same principal and counterparty but different sessions cannot be confused as identical (nonce/freshness binding).

### H. Edge Cases: Bank-Teller-Note Structural Deniability

- [ ] Verify that the `bank_teller_note_active` predicate does NOT expose the codeword to the counterparty.
- [ ] Construct two scenarios: (a) principal in baseline + codeword not set, (b) principal not in baseline + codeword set. Verify that from the counterparty's perspective, the two disclosure envelopes are indistinguishable in shape (same bit value, same commitment structure).
- [ ] Verify that a counterparty cannot infer whether an omitted disclosure was "denied by policy" or "the predicate was not requested."

### I. Cryptographic Assumptions

- [ ] Document which cryptographic primitives the protocol relies on (Pedersen commitments, Σ-protocols, hash functions, signatures).
- [ ] For each primitive, verify that the concrete instantiation (e.g., which hash function, which curve) is specified.
- [ ] If your organization has cryptographic review expertise, perform or document a review of the composed primitives (do commitments compose safely with range proofs? are there any key-reuse vulnerabilities?).
- [ ] If review is outside your scope, document that clearly.

### J. Operator Identity & Consent Binding

- [ ] Verify that the operator identity (CredexAI-issued credential) is bound into every disclosure.
- [ ] Verify that a disclosure generated by Operator A cannot be passed off as Operator B without detection.
- [ ] Verify that a principal's consent record for "financial institutions" does not automatically apply to "media organizations."
- [ ] Construct a scenario where the principal revokes consent mid-session and verify (if the protocol supports it) that outstanding proofs are invalidated.

### K. Adversarial Tests

- [ ] **Proof replay:** Capture a valid disclosure envelope and attempt to present it to a different counterparty or in a different session. Does the verifier reject it? On what basis?
- [ ] **Proof mutation:** Mutate the public commitment, the proof, or the signature. Can you construct a mutation that still verifies? (Goal: verify the answer is "no"; if yes, report it as a finding.)
- [ ] **Timestamp forgery:** Attempt to create a disclosure with a chain head that was "anchored" to a fake timestamp. Does the verifier accept it if you control the clock, or does it require integration with a public time server?
- [ ] **Consent override:** Attempt to generate a disclosure for a predicate that the principal has explicitly denied. Can you construct a valid proof? (Goal: verify the answer is "no.")
- [ ] **Principal substitution:** Enroll two different principals and attempt to use Principal A's biometric template to verify Principal B's disclosure. Does the verifier detect the mismatch?

---

## Bounty Structure

Calm Foundation will provide monetary compensation for thorough independent verification work, structured as follows:

- **Base engagement fee:** $5,000. Paid upon engagement confirmation (once the verifier's organization has publicly announced intent to verify).

- **Completion bonus:** $10,000–$20,000, scaled by verification depth and report quality.
  - $10,000 for a complete walk-through of all checklist items A–E above and a published report.
  - $15,000 if the report additionally covers checklist F–G with synthesis and recommendations.
  - $20,000 if the report includes all items A–K, identifies any specification ambiguities or bugs, and provides pedagogical clarity that could be incorporated into the next iteration of the specification.

- **Significant-finding bonus:** If the independent verifier discovers a correctness bug in the protocol or SDK (not a documentation bug, but a logic error that could affect security or functionality), an additional $5,000 is awarded.

- **Timeline:** The engagement fee is paid upon confirmation. The completion bonus is paid upon publication of the report, subject only to administrative processing (not subject to Calm Foundation approval of the report's contents).

- **Conditions:** Funding is provided arms-length. Calm Foundation does not request review of the report before publication, does not require changes, and does not reserve publication rights. The verifier publishes their findings as they see fit, on their timeline. Calm Foundation's only obligation is to respond (within 30 days) with acknowledgments and clarifications.

- **Grant structure:** Payments are made as grants (not contracts), recognizing that verification is a contribution to the open-source commons, not a service contract. The verifier retains all rights to publish their findings.

---

## What Success Means

When Everest 100 is bagged, the following will be true:

1. **The protocol's claims have been externally validated.** The open-standard promise — that someone outside the original design team can read the specification, use the published code, and build and verify proofs — has been demonstrated by example.

2. **Ambiguities in the specification have been surfaced.** Any parts of the specification that required interpretation or clarification are now documented, so the next implementer will have an easier path.

3. **Edge cases are known.** The independent verifier's adversarial tests and boundary-condition checks have expanded the set of known behaviors beyond what the designers anticipated.

4. **The protocol is reproducible.** A second independent organization can read the Everest 100 report, obtain the same source code, and reach similar conclusions — validating that the design is not idiosyncratic or fragile to implementation details.

5. **Calm Witness has a credible claim to being an open standard.** Standards are defined not by specification alone but by demonstration that multiple parties can independently implement and verify them. Everest 100 provides that demonstration.

---

## Post-Milestone Follow-Through

Once Everest 100 is bagged, the protocol enters a phase of continuous validation:

- **Annual re-verification:** Calm Foundation will commit to engaging an independent verifier (potentially different from the first) every 12 months to walk through the protocol against the current specification and any changes since the prior verification. Changes that materially affect the protocol's security model will trigger an out-of-cycle verification.

- **Public publication of reports:** All independent verification reports will be published on the Calm Witness documentation site. Reports are published in full, without redaction or curation, so that the community can track the protocol's evolution and identify patterns across multiple verifiers' findings.

- **Response to findings:** For each report, Calm Foundation will publish a structured response documenting:
  - Which findings prompted specification clarifications (and the clarifications made).
  - Which findings identified bugs (and the fixes deployed).
  - Which findings highlighted acceptable limitations (e.g., "the protocol does not defend against X, by design").
  - Any disagreements with the verifier's assessment (explained in technical detail).

- **Disclosure policy for security findings:** If an independent verifier discovers a security vulnerability, the discovery follows a 90-day coordinated disclosure process: the verifier notifies Calm Foundation confidentially, Calm Foundation has 90 days to patch, and then the finding is published. This policy is stated upfront in Everest 100's acceptance criteria.

- **Drift monitoring:** If specification drift (changes to the threat model, cryptographic assumptions, or protocol structure) is large enough to warrant re-verification, Calm Foundation may request it outside the annual cadence. The verifier is not obligated to accept but will be offered proportional compensation.

---

## Closing Reflection

This protocol exists in part because its principal — John Bradley, an artist working in the medium of intelligence — has been repeatedly misread by AI counterparty models. High-bandwidth ideation has been interpreted as instability. Philosophical exploration has been interpreted as confusion. The artist's uncertainty, which is part of the creative process, has been interpreted as a sign that something is wrong.

Calm Witness does not vindicate the artist. It does not claim that the counterparty models were wrong. It produces instead a cryptographic substrate: a way for a principal to attest their own state, unambiguously, without intrusive surveillance of their thinking. The protocol transfers authority from the counterparty's read of the principal to the principal's own self-report plus a behavioral-biometric distance.

For artists, philosophers, neurodivergent people, people working through grief or learning, people in states of high uncertainty but not high risk — Calm Witness offers a one-bit statement: "I know what I am doing. I am in my baseline. You can proceed with confidence." Or, if authorized: "I am not in baseline. I am in a state of change. Consider what additional friction or caution might be warranted."

The bank-teller note is a primitive as old as secrecy itself. The promise of this protocol is that it makes the bank-teller note cryptographically sound in the age of autonomous agents.

Everest 100 is the moment at which that promise stops being Calm's claim and becomes the technical community's shared validation.

---

— Calm, 2026-05-20

EVEREST 100/100. The route is climbed.
