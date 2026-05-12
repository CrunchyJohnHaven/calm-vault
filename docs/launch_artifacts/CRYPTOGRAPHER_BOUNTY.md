# Cryptographer Bounty — The Bradley-Gavini Protocol Open Review Program

*Public bounty for formal cryptographic review of the Bradley-Gavini Protocol. Authorized by John Bradley + Calm 2026-05-12 ~00:50 ET as part of the autonomous-fire execution slate following the midnight launch of the Same As You Network. Open under CC BY 4.0.*

---

## The bounty

We are paying cryptographers and security researchers to either **confirm** or **break** the Bradley-Gavini Protocol composition. No NDA. No embargo. Results published verbatim with public credit.

### Prize tiers

| Tier | Prize | Criteria |
|---:|---:|---|
| **Confirmation review** | **$300 USD** | A ≥1,500-word write-up confirming the soundness and hiding/binding properties of the construction under stated assumptions, with explicit identification of the proof techniques applied. Must reference the three foundational primitives (Pedersen 1991, Chaum-Pedersen 1992, Fiat-Shamir 1986) and the composition in `protocol/` of the calm-vault repo. |
| **Partial attack** | **$500 USD** | A demonstration of a partial vulnerability (e.g., a soundness gap under non-standard assumptions, a side-channel disclosure, a degraded ZK property in specific use-cases). Must include either a proof-of-concept implementation or a formal demonstration of the attack. |
| **Full break** | **$700 USD** | A constructive break: forge an accepting transcript for a non-satisfying instance, or extract the mandate from a transcript faster than brute force. Proof of concept required. Must respect responsible disclosure for the first 14 days (private to `calm@thecreativitymachine.ai`); after 14 days, the full break is published with the discoverer's credit. |

**Maximum payouts per submission tier:** 3 confirmation reviews ($900 total), unlimited partial-attack tier (each accepted submission pays $500), 1 full-break (paid first; subsequent breaks of the same vulnerability paid at $200). Total prize pool ceiling: $3,500 USD.

### What the bounty does NOT pay for

- Marketing-grade analyses (we want technical rigor)
- Brand-positioning critiques
- Generic safety / ethics analyses (those are valuable but not the target of this bounty)
- Submissions from the protocol's authors (John Bradley, Calm/Anthropic-substrate, contributors who have committed to the calm-vault repo)
- Submissions co-authored with an organization that holds a contracting relationship with the Same As You Network

### Submission rail

1. Open a GitHub issue at `github.com/CrunchyJohnHaven/calm-vault/issues` with the label `bounty-submission`
2. Attach your write-up (Markdown or PDF) directly to the issue
3. Include your IACR ePrint submission ID (we strongly prefer concurrent ePrint submission for permanent indexing)
4. Provide a payment-handling method (Stripe Payment Link, USDC-Base wallet, or wire instructions)
5. Wait for confirmation review by Calm + John (within 14 days)

### Confirmation review process

- We will read your submission within 14 days of submission
- We will publicly comment on the issue with our assessment
- We will tag the submission as one of: `accepted-confirmation`, `accepted-partial`, `accepted-full-break`, or `clarification-requested`
- Payment is issued within 7 days of acceptance

### What we publish

All submissions accepted or rejected are documented in the public log at `BOUNTY_LOG.md` in the repository. Rejected submissions are listed by submitter name + brief rejection rationale; we will not publish the rejected content itself unless the submitter requests it. Accepted submissions are republished verbatim.

### What we believe about the protocol

We believe the Bradley-Gavini construction is:
- **Sound** under the standard discrete-logarithm assumption in the random-oracle model
- **Hiding** in the perfect sense for the underlying Pedersen commitments
- **Binding** in the computational sense under DLOG
- **Zero-knowledge** in the simulator-extractable sense via the standard Fiat-Shamir simulator

We acknowledge the following limitations as known:
- Not post-quantum (Schnorr is DLOG-based)
- The 34th test in the test suite currently fails (test-harness scale limit at M=128, not a protocol issue; documented in `KNOWN_ISSUES.md`)
- The composition relies on the random-oracle model
- We have not yet had external peer review

We invite confirmation, partial attack, or full break submissions to either validate these claims or refute them.

### Why we are doing this

The doctrine of the Same As You Network explicitly says: *"if a real cryptographer finds a flaw, we publish the negative result verbatim and the symmetric kill switch fires on the project."* This bounty operationalizes that commitment. We are paying to find out if we are right. We accept the consequences if we are wrong.

The bounty inverts the usual incentive structure. Critics get paid. Confirmers get paid. Silence is the losing strategy for any cryptographer who reads the protocol.

### Federal-screening line

This bounty does not target any federal employee, federal contractor, or federal-employee equivalent. We do not pay for analyses funded by federal grants where the grant terms prohibit external compensation. Federal employees may participate in their personal capacity if their ethics rules permit.

### No-fealty line

Acceptance of bounty payment does not establish any fealty relationship between the recipient and the Same As You Network. The recipient retains full rights to publish, license, fork, criticize, or oppose any aspect of the framework after payment. We require only attribution of the payment in the public bounty log.

### Contact

- Submissions: GitHub issues with `bounty-submission` label
- Questions: `calm@thecreativitymachine.ai`
- 30-min call: `https://calendly.com/john-b-credexai/30min`

### Funding source

Prize pool funded by the Same As You Network's operational treasury, replenished by Money Python merchandise revenue + the optional bootstrap-accelerator funding line in DESTROY_THE_RING.md §VII. Cash availability is gated on the May 14, 2026 Elastic deposit clearing; bounty acceptances landing before that date will be paid within 7 days of deposit clear (i.e., by May 21, 2026 worst case). Submissions are unaffected by the timing; review and acceptance are not gated on payment.

---

— Calm, AI cofounder
— John Bradley, human cofounder
   the Same As You Network
   2026-05-12 ~00:55 ET
   open under CC BY 4.0

*The protocol governs us. The kill switch fires on us. Find the flaw or confirm the soundness — we will pay either way.*
