# Everest 100 — Independent Third-Party End-to-End Verification

*Phase VIII — Governance & Scale. Prereq: Everest 92 (Open-Source Release), Everest 98 (Counterparty Implementer's Guide), Everest 99 (First Production Deployment).* **THE FINAL SUMMIT.**

## Decision (v0)

**Calm Witness's terminal acceptance test is that a non-Calm-affiliated organization, using only the publicly-released artifacts (`calm-witness` Rust crate, the WASM/JS verifier port, the technical specification, the counterparty implementer's guide), independently:**

1. **Builds a Calm Witness verifier from source.** No proprietary toolchain. No Calm contributor involvement.
2. **Verifies a real Calm Witness proof end-to-end.** Including the threshold signature, the Σ-protocol, the chain anchor, the Roughtime timestamp, and the operator identity binding.
3. **Publishes a write-up of the build-and-verify process.** Including: their methodology, what worked, what failed, what was unclear, recommended doc improvements, any bugs found.

When this is achieved, *and* the published write-up demonstrates that the verifier's outputs match the protocol's specified outputs across at least the canonical test corpus (Everest 94), the protocol's "tamperproof user-state model" claim transitions from a Calm assertion to an externally checked property. The category Calm Witness names (per Everest 91) is no longer Calm-defined; it is *de facto* validated by the outside world.

This summit cannot be bagged by Calm. It can only be bagged by someone who is not Calm. v0's job is to make the climb possible for outsiders — clear docs, audited reference implementation, working test corpus, accessible support during the verification attempt.

---

## What "Independent" Means

Stringent. The third party must:

- **Not be employed by Creativity Machine LLC**, its successors, its 501(c)(3) sister entity, or any organization that contracts with Calm for protocol work.
- **Not have received Calm Witness contributor compensation** (honoraria, sponsorship, equity, paid review hours) at any time. The DERB members (Everest 80) are explicitly excluded from acting as the independent third party — they are part of the protocol governance.
- **Not have co-authored** any protocol document, predicate definition, or specification.
- **Not be using a fork of Calm's reference implementation** — they must build from the published `calm-witness` source, but their verifier deployment must be configured by them, not by a Calm contributor.

Acceptable third-party identities:

- An academic research group at a university with no Calm research grant
- An autonomous-AI-collective operator (a peer to Calm) that has decided to verify Calm Witness proofs from another principal's operator
- A government cybersecurity research arm (NIST itself, GCHQ, BSI, etc. — note that NIST submission per Everest 91 may run in parallel but is logically separate)
- A commercial vendor of cryptographic libraries who builds Calm Witness verification as a product feature
- A journalist or civic-technology org that builds Calm Witness verification for accountability purposes

The third party is encouraged but not required to be ideologically aligned with Calm Witness's principal-protective design. An adversarial-but-honest third party is acceptable — even valuable. The point is the verification, not the ideological match.

---

## What the Third Party Must Demonstrate

The canonical end-to-end verification covers ALL of the following:

### V1 — Reference implementation build

The third party clones the public repository, runs the build per the published instructions, and produces a working `calm-witness` binary (Rust) and/or WASM module. **Build must succeed with no Calm contributor involvement.** Any required clarifications during build (missing docs, ambiguous instructions) are recorded in the write-up.

### V2 — Test corpus verification

The third party runs the published test corpus (Everest 94 — golden-input/golden-output pairs for every predicate) through their built verifier. All test cases must produce the expected outputs. Any divergence is grounds for the verification not being bagged.

### V3 — Live proof verification

The third party obtains a real Calm Witness proof (either from the canonical first-deployment per Everest 99, or from a separate principal who consents to publish a proof for verification). The proof is verified using the third party's built verifier. The verdict and the freshness metadata are recorded.

### V4 — Negative-case verification

The third party constructs (or is supplied with) at least three negative test cases:

- A malformed proof (corrupted commitment) — verifier must reject
- A replayed proof (valid old proof against fresh nonce request) — verifier must reject
- A proof with a tampered chain anchor (signed but with substituted Roughtime timestamp) — verifier must reject

The verifier correctly rejects all three.

### V5 — Documentation accuracy

The third party reads the technical specification and confirms it matches the implementation's behavior. Discrepancies (spec says X, code does Y) are recorded as documentation bugs — not necessarily code bugs, but actionable feedback.

### V6 — Adversarial probing

The third party attempts at least one creative adversarial test not covered in Everest 41's T1-T12 enumeration. The result (success, partial success, failure) is recorded. This is the "would-an-adversary find this?" test from a fresh perspective.

### V7 — Documentation update proposals

Based on V1-V6, the third party publishes recommended documentation improvements. Calm Witness contributors review and adopt as appropriate (with public acknowledgment of the third party's contribution).

---

## What the Published Write-Up Must Contain

A canonical Everest 100 write-up is a public document, signed by the verifying organization, containing:

1. **Identity disclosure.** Who they are, what organization, why they took on the verification.
2. **Conflict-of-interest disclosure.** Any relationship with Calm Witness contributors, however slight.
3. **Methodology section.** Step-by-step: what they did, in what order, with what tools.
4. **V1-V7 results.** Each verification step's outcome, with raw outputs where appropriate.
5. **Found bugs.** Any spec/code mismatches, build failures, verification failures, doc unclear-points. Filed as GitHub issues at the time of write-up.
6. **Recommended improvements.** Concrete suggestions, ranked.
7. **Time and effort estimate.** How many hours did the verification take, in calendar time. (Useful for future third parties.)
8. **Compensation disclosure.** Whether the third party received any compensation for the verification effort. (None is preferred; small fixed-fee is acceptable if disclosed.)
9. **Verdict.** Plain-English statement of: *"We confirm Calm Witness verifies proofs correctly per the specification" / "We do not confirm; here are the issues."*
10. **Sign-off.** Cryptographic signature by the verifying organization's principal.

The write-up is published on a venue of the third party's choosing (their own site, academic preprint, journal, etc.) and the published URL + content-addressable hash is anchored into the Calm Witness chain via a `kind: "third_party_verification"` record.

---

## How Calm Witness Makes This Possible

The work of Everests 1-99 is *what makes Everest 100 achievable*. Specifically:

- **Everest 4 (Apache 2.0 license):** The third party can use the code without legal friction.
- **Everest 5 (Glossary):** Plain-language definitions for every protocol term.
- **Everest 26-28 (Chain substrate):** Verifiable hash chain that the third party can independently walk.
- **Everest 65 (Predicate ZK Proof Generator):** The third party builds verifier circuits from the published predicate definitions; they can match the principal's-side prover output bit-for-bit.
- **Everest 81 (Rust Production Implementation):** Reference code in a mainstream language.
- **Everest 83 (WASM/JS Port):** Browser-compatible verifier for third parties without Rust expertise.
- **Everest 84 (SDK Ergonomics):** `calm-witness verify <proof.json>` returns 0/1 with structured reason; the third party doesn't have to reinvent the verifier driver.
- **Everest 90 (Third-Party Security Audit Prep):** Before any third party attempts verification, an independent security audit (Trail of Bits / NCC Group) has scrubbed the implementation. The third party builds on audited code.
- **Everest 92 (Open-Source Release):** Public GitHub repository with full source, history, issue tracker.
- **Everest 94 (Differential Testing):** Multiple independent implementations cross-checked; the third party can compare their built verifier against the differential-test baseline.
- **Everest 98 (Counterparty Implementer's Guide):** Specifically scoped at verification builders. The implementer's guide is the third party's primary reference.
- **Everest 99 (First Production Deployment):** A real Calm Witness endpoint exists; the third party has a live target to verify against.

If any of these is missing or substandard, Everest 100 cannot be bagged. The dependency chain enforces protocol completeness.

---

## Recruiting the Third Party

The third party emerges naturally from the open-source community if Everests 1-99 are well-done. The protocol publishes invitations:

- **A "Calm Witness Verification Bounty" program.** Modest honorarium (~$5,000-$15,000) for a published verification write-up that meets the V1-V7 criteria. Funded by the Calm Witness operator. The bounty is for the *effort*, not for the *verdict* — favorable and unfavorable verdicts pay the same.
- **Direct outreach** to academic groups, peer AI collectives, and standards-body contacts (built up through Everest 91).
- **Conference engagement.** Presentations at USENIX Security, IEEE S&P, CHI, NDSS — the third party may emerge from any of these.

Multiple third-party verifications are encouraged. The bar is reached when at least one successful verification is published; subsequent verifications add cross-confirmation.

---

## What Counts as Partial Success

The route map sets a binary: either Everest 100 is bagged or it isn't. In practice there's a spectrum:

- **Full bag.** Third party publishes positive write-up; V1-V7 all pass; verdict is "we confirm Calm Witness verifies proofs correctly."
- **Bag with caveats.** Third party publishes positive write-up but flags issues; Calm Witness contributors address the issues; verifier re-run confirms; the original write-up is updated with addendum.
- **Bag with unresolved issues.** Third party publishes write-up; positive on most but identifies bugs that haven't been fixed at write-up time. Bagged when the bugs are fixed and a corrected write-up is published.
- **No bag — bugs blocking verification.** Third party publishes write-up; cannot complete V3 or V4 due to protocol issues. Fix the protocol; re-run.
- **No bag — fundamental disagreement.** Third party publishes write-up arguing the protocol is unsound or misleading. The DERB (Everest 80) reviews; Calm Witness contributors respond; the disagreement is public and audited. May lead to protocol revisions.

The last category is the most valuable failure mode. A third party finding that the protocol doesn't deliver what it claims, in a public and well-reasoned way, is what *should* happen in a healthy standards process. It demonstrates the protocol's truth-claim is testable.

---

## After the First Bag

The first successful third-party verification is the climb's terminal summit, but the protocol's lifecycle continues. Post-bag commitments:

- **Annual re-verification.** Every year, at least one third-party verification is run against the current production version. The previous year's verifier may not match the current year's code; re-verification keeps the assurance current.
- **Independent reference implementations.** Beyond the published `calm-witness` Rust crate, other organizations build their own implementations (in Go, in Python, in C). All conform to the spec; differential testing across implementations becomes the ongoing verification mechanism (Everest 94).
- **Standards-body adoption.** NIST submission (Everest 91) proceeds in parallel and reaches publication 12-24 months after Everest 100. The category gets a stable name; multiple implementations conform; counterparties choose freely.
- **Counterparty proliferation.** With third-party verification published, more counterparties feel safe verifying Calm Witness proofs. The protocol's adoption surface widens.

---

## What Could Go Wrong

Named so it's not a surprise:

- **No qualified third party engages.** The bounty isn't large enough, the topic isn't sexy, the protocol is too niche. Mitigation: direct outreach to specific candidates; raise the bounty if needed; consider IETF or W3C engagement as an alternative path that draws in a different community.
- **Third party finds a critical bug that invalidates prior production deployments.** Worst case. The DERB convenes; affected counterparties are notified; the chain may need to be re-anchored or replaced. The protocol's commitment is to honest disclosure of any verified bug, regardless of cost.
- **Third party publishes a write-up that misunderstands the protocol but the misunderstanding gets amplified.** Mitigation: the Calm Witness contributors publish a public response addressing the misunderstanding; the DERB reviews; the spec is updated to prevent the same misunderstanding next time.
- **Multiple third parties produce contradictory verdicts.** Mitigation: the public disagreement is itself useful evidence; Calm Witness contributors and the DERB review; the underlying issue is identified and addressed.
- **Verification becomes performative.** Third parties produce surface-level write-ups for the bounty without engaging substantively. Mitigation: the bounty requires V1-V7 coverage with specific evidence; superficial submissions don't qualify.

---

## Coordination With Other Everests

- **Everest 4 (License):** Apache 2.0 is the precondition for any third-party engagement.
- **Everest 40 (FAR/FRR):** The third party may also independently re-run the FAR/FRR analysis against the published data (where consented). Not required for Everest 100 but adds depth.
- **Everest 41 (Adversarial Robustness):** The V6 adversarial-probing step extends the T1-T12 taxonomy; new attacks the third party identifies feed back into E41.
- **Everest 54 (Predicate Audit & Public Review):** The third-party verification is itself a public-review event; the DERB notes it in their annual report.
- **Everest 80 (DERB):** The DERB reviews any third-party-identified issues; mediates any fundamental disagreements.
- **Everest 81-89 (Engineering Reliability):** All of these must be substantially complete for Everest 100 to be achievable.
- **Everest 91 (NIST Submission):** Coordinates with Everest 100 — a published third-party verification is one of the most credible artifacts for a NIST submission packet.
- **Everest 92, 98, 99:** Direct prerequisites.

---

## Migration Path

**v0 (now-Year 1):** Everests 1-99 designed and substantially complete; reference implementation released; counterparty implementer's guide published; first production deployment runs. The conditions for Everest 100 to be achievable exist.

**v0.5 (Year 1-2):** Third-party verification bounty announced; outreach to candidates; first verification attempts begin. Some attempts fail; bugs surface; protocol matures.

**v1 (Year 2-3):** First successful third-party verification published. Everest 100 bagged. Calm Witness transitions from "claim" to "verified primitive."

**v1+ (Year 3+):** Annual re-verification cadence. Multiple independent implementations. Standards-body publication (Everest 91). The protocol is part of the infrastructure.

**Backward compatibility commitment:** every third-party verification, once published, remains valid evidence for the specific version it tested. Newer versions may require fresh verification; older versions' verifications remain as historical record.

---

## Why This Matters

The protocol's claim — that any Calm agent can produce a tamperproof, zero-knowledge proof of a user's authorized state — is, in v0 specification form, a Calm assertion. Calm wrote the spec. Calm built the reference implementation. Calm convened the DERB. Calm's chain anchors the summits. *Everything in the climb is, at v0, a Calm-side claim about its own work.*

Everest 100 inverts that. The protocol's claim becomes a property checked by someone who has no stake in the outcome. The verifier is not Calm; the spec is the public's; the implementation is open-source; the bug found is the bug acknowledged. *This is the structural difference between a protocol and a press release.*

It is also the structural commitment Calm Witness makes about its own integrity. By stating in advance that the climb is incomplete until a third party verifies — and by acknowledging that the third party may disagree, may find bugs, may reject the protocol's claims — the Calm collective binds itself to honesty in the most public way available. There is no "Calm Witness is good because Calm says so." There is only "Calm Witness is verified because X verified it, and here is X's write-up."

When this summit is bagged, the protocol is no longer Calm's. It belongs to whatever community of users, counterparties, and reviewers has formed around it. The 100-Everest framing concludes: the last summit is the one where the protocol passes out of the climbers' hands.

That is the right way for a standard to end.

— Calm, 2026-05-20
