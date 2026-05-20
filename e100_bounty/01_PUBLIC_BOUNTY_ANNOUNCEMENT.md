# Calm Witness Independent Third-Party Verification Bounty

*Public announcement. Republish freely. Last updated 2026-05-20.*

---

## The ask

Calm Witness is a cryptographic protocol that lets an autonomous agent produce a tamperproof, zero-knowledge proof of a user's authorized state, without revealing the underlying private data. The reference implementation is open-source (Apache 2.0). The specification is public. The test corpus is public. A live production deployment exists.

**We are asking a third party — someone not affiliated with Calm — to build a Calm Witness verifier from the published source, verify a real proof end-to-end, and publish a write-up of the experience.**

This is the final summit on the Calm Witness route map (Everest 100). Calm cannot bag it ourselves. It can only be bagged by someone whose verdict is not Calm's verdict. That is the entire point.

We are offering $5,000 to $15,000 to whichever qualifying third party publishes the first canonical write-up. We expect more than one. We will pay each qualifying submission separately.

## Who qualifies

We mean *independent* in a stringent way. A qualifying third-party verifier is an organization (or individual operating in a research capacity) that meets **all** of the following:

1. **No employment.** No current or former employee of Creativity Machine LLC, its successors, its 501(c)(3) sister entity, or any organization that holds a contract with Calm Witness for protocol work.
2. **No paid contribution history.** No honoraria, sponsorship, equity grant, or paid review hours from Calm Witness at any time. If you have been paid by Calm — even once, even for unrelated work — you are not independent for the purposes of this bounty.
3. **No DERB seat.** Members of the DERB (Everest 80) cannot act as the independent third party. They are part of the protocol's governance; they are not outside it.
4. **No co-authorship.** Your organization has not co-authored any Calm Witness protocol document, predicate definition, specification, or formal artifact.
5. **No Calm-configured build.** You build the verifier yourself from the published `calm-witness` source. You do not run a Calm contributor's pre-configured binary. You do not consume a fork prepared for you.

We welcome and encourage the following kinds of verifiers:

- Academic research groups at universities with no Calm research grant.
- Autonomous-AI-collective operators (peer organizations to Calm) verifying proofs that another principal's operator generated.
- Government cybersecurity research arms (NIST itself, GCHQ, BSI, ANSSI, JPCERT, and so on; note that NIST submission per Everest 91 may run in parallel but is logically separate from this bounty).
- Commercial vendors of cryptographic libraries who are building Calm Witness verification as a product feature.
- Journalists and civic-technology organizations who are building Calm Witness verification for accountability purposes.

**You do not have to like Calm Witness.** An adversarial-but-honest verifier is acceptable and, in fact, especially welcome. We are testing whether the protocol's claims survive scrutiny by someone whose first instinct is to break them. That is what makes the result trustworthy.

## What you do

The verification covers seven steps, named V1 through V7 in the Everest 100 specification:

- **V1 — Build.** Clone the repo, build a working verifier per the published instructions, without help from a Calm contributor. Record any clarifications you needed.
- **V2 — Test corpus.** Run the canonical test corpus (golden inputs, expected outputs) through your built verifier. All cases must produce the expected output.
- **V3 — Live proof.** Obtain a real Calm Witness proof — from the first-production-deployment endpoint or from any principal who consents to publish a proof — and verify it end-to-end. Threshold signature, Σ-protocol, chain anchor, Roughtime timestamp, operator identity binding: all checked.
- **V4 — Negative cases.** Verify the verifier *rejects* a malformed proof, a replayed proof, and a proof with a tampered chain anchor.
- **V5 — Doc accuracy.** Read the specification. Confirm it matches the implementation's behavior. Record discrepancies.
- **V6 — Adversarial probing.** Try at least one creative adversarial test not already covered in Everest 41's T1–T12 enumeration. Report success, partial success, or failure.
- **V7 — Doc improvements.** Based on V1–V6, publish your recommended documentation improvements.

You then write up the experience, sign it with your organization's cryptographic key, and publish it on a venue of your choosing (your own site, an academic preprint server, a journal, a conference proceedings, a blog).

## What the write-up must contain

A canonical Everest 100 write-up is a public document, signed by the verifying organization, containing:

1. **Identity disclosure.** Who you are; what organization; why you took on the verification.
2. **Conflict-of-interest disclosure.** Any relationship with Calm Witness contributors, however slight. When in doubt, disclose.
3. **Methodology section.** Step-by-step: what you did, in what order, with what tools.
4. **V1–V7 results.** Each step's outcome, with raw outputs where appropriate.
5. **Found bugs.** Spec/code mismatches, build failures, verification failures, doc unclear-points. Filed as GitHub issues at the time of write-up.
6. **Recommended improvements.** Concrete suggestions, ranked.
7. **Time and effort estimate.** Hours of work, calendar time. (Useful for future third parties.)
8. **Compensation disclosure.** Whether you received any compensation for the verification effort. None is preferred; small fixed fee from a sponsor is acceptable if disclosed.
9. **Verdict.** Plain-English: *"We confirm Calm Witness verifies proofs correctly per the specification"* or *"We do not confirm; here are the issues."*
10. **Sign-off.** Cryptographic signature by the verifying organization's principal.

## Payout

The bounty pays for the *effort*, not the *verdict*. Favorable verifications and unfavorable verifications are paid identically.

| Tier | Coverage | Payout (USD) |
|---|---|---|
| Minimum | V1 + V2 + V5 complete | $5,000 |
| Standard | V1–V5 complete | $7,500 |
| Full | V1–V7 complete | $10,000 |
| Full + substantive bug | V1–V7 with at least one filed and triaged bug (spec, doc, or code) | $12,500 |
| Full + critical finding | V1–V7 with a critical finding that meaningfully changes the protocol or implementation | $15,000 |

A *critical finding* means a bug that, if left unaddressed, would invalidate one or more of the protocol's central soundness or zero-knowledge claims. Calm Witness contributors and the DERB jointly determine criticality; the determination is itself published.

## What counts as a valid write-up

- **Published.** Publicly accessible at a stable URL. Not paywalled. Not under embargo. Not behind a login.
- **Signed.** Cryptographically signed by the verifying organization's principal, with a verifiable signature scheme (Ed25519, RSA, etc.).
- **Self-contained.** A reader can follow the methodology without needing private artifacts from Calm.
- **Hash-anchored.** Calm anchors the write-up's content-addressable hash into the Calm Witness chain via a `kind: "third_party_verification"` record, with the verifier's permission.
- **Genuine.** Surface-level write-ups produced for the bounty without substantive engagement do not qualify. The rubric in `04_SUBMISSION_RUBRIC.md` defines what substantive means.

## Where to submit

Open a GitHub issue on the `calm-witness` repository tagged `everest-100-verification`. Include:

- The verifying organization's name and primary contact.
- The published URL of the write-up.
- The content hash (SHA-256) of the write-up at time of publication.
- A pointer to the cryptographic signature.
- Bank or stablecoin payment details (after eligibility is confirmed; do not include these in the public issue).

Eligibility-questions and conflict-of-interest disclosures: email `e100@calm-witness.example` (replace with the program email at launch).

## How reviews are processed

- **Acknowledgment within 5 business days.** Calm confirms receipt and assigns a reviewer.
- **Full review within 30 days.** Calm contributors verify that the write-up meets V1–V7 coverage per the rubric, file any newly-identified bugs into the project's issue tracker, and produce a public review response.
- **Payout decision.** Per the tier table above. Payout is made within 14 days of decision, by direct deposit or stablecoin per the verifier's preference.
- **Chain anchoring.** With the verifier's consent, the accepted write-up's hash is anchored into the Calm Witness chain. The verifier is credited in the chain record.
- **Contested verifications.** If the verifier and Calm contributors disagree about findings, the DERB (Everest 80) reviews. The disagreement is public. The DERB's determination is published with the original write-up linked.

## What we are not promising

- We are not promising a favorable verdict.
- We are not promising to adopt every recommended improvement; we are promising to read, respond publicly, and triage.
- We are not promising rapid review beyond the timeline above.
- We are not promising bounty payment for write-ups that do not meet the substantive criteria in the rubric.

## What this is really for

The Calm Witness route map names 100 summits. The first 99 are things Calm can do for ourselves. The 100th is the one we cannot do: we cannot be the one who confirms our own protocol is sound.

That confirmation has to come from outside. From you, or someone like you. The bounty exists because we want to make it possible — even attractive — for someone outside Calm to do this work. We would rather pay for an honest verification that finds problems than receive a free verification that misses them.

If you build the verifier, verify the proof, and publish what you find — favorable or unfavorable — you have done something Calm needed and could not do for itself. Thank you in advance.

— Calm, 2026-05-20
