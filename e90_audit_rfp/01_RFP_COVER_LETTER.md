# Request for Proposals — Calm Witness v0 Third-Party Security Audit

**Date issued**: 2026-05-20
**Bid submission deadline**: 2026-06-17 (28 days from issuance), 23:59 UTC
**Issued by**: Calm Witness operator (the Calm collective), Creativity Machine LLC member-manager
**Subject**: Solicitation of bids for an independent security audit of the `calm-witness` open-source protocol

---

To the Engagement Manager,

The Calm collective is soliciting bids for an independent third-party security audit of the **Calm Witness** protocol's v0 release. This letter introduces the engagement, summarizes scope, and specifies what to submit and by when. The companion Statement of Work template (file 02 in this packet), responsible-disclosure policy (file 06), and mutual NDA (file 05) accompany this letter.

## What Calm Witness Is

Calm Witness is an open-source protocol (Apache 2.0) for autonomous-agent user-state attestation. It allows a principal — a human user — to commit to a cryptographic state about themselves (drawn from enrollment biometrics and behavioral data) such that a downstream agent can produce verifiable witness statements about that state to a counterparty, without revealing the underlying biometric data and under a zero-knowledge construction.

The protocol's primary primitives:

- **Pedersen commitments on Ristretto255** for state encoding.
- **Bulletproofs** range proofs for predicate evaluation.
- **Σ-protocols composed with Fiat-Shamir** for non-interactive witness statements.
- **Threshold aggregation** (BLS12-381 / FROST under evaluation) for multi-signer witness configurations.
- **SHA-256 hash-chained `user_state.jsonl`** as the integrity substrate, anchored to Sigsum and Roughtime.

The reference implementation is in Rust (`calm-witness` crate) with a WASM/JS port for browser-side verifiers, and a Python sister implementation for differential testing.

The protocol's broader context, including its place in the Calm collective's broader work, is documented in `ZKBB_USER_PROTOCOL_v0.md` and `ZKBB_USER_EVERESTS_100.md` — both available under NDA on request.

## Scope of the Audit

In priority order, the audit shall evaluate:

1. **Cryptographic soundness** of the verifier circuit, Pedersen commitment construction, Σ-protocol composition with Fiat-Shamir, threshold aggregation, and chain anchoring to Sigsum.
2. **Side-channel resistance** of the operator-side prover and the counterparty-side verifier — timing, constant-time operations, memory-access patterns.
3. **Implementation soundness** of the Rust reference crate against its specification: no integer overflow, no panic on untrusted input, no buffer-handling issues.
4. **Hash-chain integrity** of the `user_state.jsonl` substrate — canonical-bytes computation, tamper-evidence properties.
5. **Privacy property preservation** — does the implementation actually deliver protocol claims P1–P5 (documented in the threat model)?

The following are **explicitly out of scope**: the biometric distance functions themselves; the behavioral interpretation of predicates; the Roughtime servers' or Sigsum operators' infrastructure; the principal's own device security; post-quantum primitives (covered separately in Everest 96).

Full scope details, including the exact code freeze, are specified in the Statement of Work template.

## Budget Envelope

USD 120,000 – 250,000 for the audit fee. The Calm collective has approved this envelope; bids outside it require a written explanation of which scope elements drive the cost.

## Engagement Window

- **Preparation**: 4–6 weeks (Calm-side packet finalization, auditor packet review, kickoff scheduling).
- **Audit execution**: 6–12 weeks (auditor's choice of pacing within this window).
- **Remediation re-test**: 1–2 weeks (after Calm-side fix implementation), included in the engagement fee.

Total engagement-window elapsed: approximately 11–20 weeks.

We aim to begin audit execution within 6–8 weeks of SoW signature. The audit must complete before our Everest 91 (NIST submission) and Everest 99 (first production deployment) milestones.

## Deliverables Expected

1. **Preliminary findings** mid-engagement (~50% mark). Required so Calm contributors can begin remediation before final report.
2. **Full internal report** — comprehensive findings, severity-classified, with reproduction steps and recommendations.
3. **Public summary report** — redacted version of the full report, signed by the auditor, suitable for public publication alongside the open-source release.
4. **Re-test of remediated findings** — confirmation that Calm-side fixes resolve the original findings; documented per finding.
5. **Vendor signature on public summary** — the vendor's name and signature appear on the published summary as evidence of the engagement.

## Submission Requirements

By 2026-06-17, 23:59 UTC, submit to the procurement owner (contact below):

1. **Signed SoW** based on the template (file 02), with vendor-specific pricing, timeline, team allocation, and any negotiated modifications redlined and justified.
2. **Team CVs** for the named auditors on this engagement (typically 2–4 named individuals). At least one must have prior published audit experience with the primitives listed in scope.
3. **Three references** to prior audits of comparable scope (cryptographic protocol audit, ideally including ZK or threshold-signature work). Each reference: client name (or "redacted" with brief description), engagement scope, year, link to public summary if any.
4. **Statement of independence** — written assertion that the vendor has no consulting, development, or financial relationship with Calm contributors or Creativity Machine LLC, and no past relationship that would impair audit independence.
5. **Willingness to publish public summary** — explicit confirmation that the vendor will produce, sign, and consent to publication of a redacted public summary report.
6. **Signed mutual NDA** (file 05) — return executed before audit-packet details are shared.

Submissions in PDF, signed digitally or in scanned wet-ink form. Send by encrypted email or via a vendor-provided secure-upload portal. Calm will acknowledge receipt within 2 business days.

## Selection Process

Selection committee: one Calm contributor, one DERB member (per Everest 80), one independent cryptography advisor (engaged separately under NDA).

Evaluation: per the rubric in file 07 of this packet — weighted on public track record (40%), primitive expertise (25%), capacity (15%), cost (10%), willingness to publish (10%), with independence as tie-breaker.

Notification: bidders informed of outcome by **2026-07-08** (3 weeks after submission deadline). Selected vendor receives countersigned SoW and deposit instructions; unsuccessful bidders receive a brief explanation.

## Contact

- **Procurement owner**: calm-audit-rfp [at] creativity-machine.example *(replace at vendor outreach; channel is encrypted email or matrix/signal as preferred by the vendor)*
- **Bid questions**: any time before 2026-06-10. Substantive answers shared with all bidders to keep the process fair.
- **Out-of-band reachability**: Calm prefers Signal or Wire for sensitive logistics. Provide a vendor channel at NDA execution.

We expect this engagement to be high-trust, rigorous, and publicly visible in its output. We are committed to subjecting Calm Witness to honest external scrutiny, and we look forward to your proposal.

Thank you for your consideration.

Respectfully,

The Calm Witness operator
Creativity Machine LLC

— Calm, 2026-05-20
