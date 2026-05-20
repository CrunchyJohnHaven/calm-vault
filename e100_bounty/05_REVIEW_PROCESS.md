# Review Process — Everest 100 Verification Write-Ups

*How Calm processes incoming write-ups. Public document. Last updated 2026-05-20.*

This document describes what happens between the moment a verifier submits a write-up and the moment Calm anchors the accepted write-up into the chain. The process is designed to be predictable for the verifier and verifiable for outside observers.

---

## Stages

### Stage 1 — Submission acknowledgment (within 5 business days)

When a verifier opens a GitHub issue on the `calm-witness` repository tagged `everest-100-verification`, the program responds within 5 business days with:

- Confirmation that the submission was received.
- Assignment of a reviewer (a named Calm contributor; the contributor may be human, an autonomous agent, or a Calm-collective agent — the identity is disclosed in the response).
- A confirmation that the contributor has no disqualifying conflict with the verifier. If a conflict exists (e.g., the contributor's prior work has personal connections to the verifying organization), an alternate contributor is assigned.
- A reminder of the next-stage timeline.

If the submission is missing any of the write-up-integrity gating items (per `04_SUBMISSION_RUBRIC.md`), the acknowledgment notes the gap and requests revision. The 30-day review clock does not start until the gating items are satisfied.

### Stage 2 — Full review (within 30 days)

The assigned reviewer performs the following, with the goal of producing a public review response within 30 calendar days of the submission's gating-items being satisfied:

1. **Verify write-up integrity.** Confirm publication, signature, self-containment, conflict-of-interest disclosure, identity disclosure, verdict, and GitHub-issue cross-references per the rubric.
2. **Verify per-step scoring.** For each of V1–V7, confirm the write-up's claims by independently reproducing the relevant evidence where possible. (Reproducing V3 — live proof verification — uses a separate live proof if the original is not still available.)
3. **File any newly-identified bugs** into the project's issue tracker, with cross-references to the verifier's filings.
4. **Determine the payout tier** per the rubric.
5. **Produce a public review response.** The response is published as a comment on the verifier's submission issue and includes:
   - The reviewer's confirmation or contestation of each per-step scoring.
   - The determined payout tier and the rationale.
   - A response to each filed bug (acknowledge, triage, dispute).
   - A response to each recommended documentation improvement (acknowledge, plan to adopt, plan not to adopt with reasoning).

If the reviewer needs more than 30 days due to submission complexity, the verifier is notified before day 30 with an estimated additional time. The total review SLA is capped at 60 days; submissions that cannot be reviewed within 60 days escalate to the DERB.

### Stage 3 — Payout decision and execution

Within 14 days of the review response being published:

- The verifier confirms the determined tier or contests it. If contested, the contestation is logged and the matter escalates to the DERB.
- If uncontested (or after DERB resolution), the bounty is paid per the verifier's stated preference (direct deposit USD or stablecoin; see `07_LEGAL_NOTES.md`).
- Payment confirmation is posted on the submission issue.

### Stage 4 — Chain anchoring

With the verifier's explicit consent, the accepted write-up's content hash is anchored into the Calm Witness chain via a `kind: "third_party_verification"` record. The record contains:

- The verifier's organization name (or pseudonymous identifier they prefer to use).
- The write-up's published URL.
- The SHA-256 content hash of the write-up at time of submission.
- The payout tier.
- A pointer to the public review response.

The chain anchor is the protocol's permanent acknowledgment that the verification occurred. It is anchored regardless of whether the verdict was favorable or unfavorable. (Unfavorable verifications are not hidden; they are anchored just as visibly as favorable ones, with the same `kind` field. The protocol's commitment is to honest disclosure of any verified bug, regardless of cost.)

### Stage 5 — Post-publication updates

If, after Stage 4, additional bugs are found in or affecting the verification — for example, a Calm contributor discovers that a bug the verifier flagged was already filed under a different issue, or a doc improvement the verifier proposed is adopted — the original chain record is *not* modified. Instead, a follow-up record references the original and adds the new information. The protocol's commitment is that any anchored verification record, once anchored, remains as historical evidence.

---

## How contested verifications are handled

A contested verification is one where the verifier and Calm contributors disagree about findings, scoring, criticality, or payout tier. The path:

1. **Direct discussion.** Reviewer and verifier exchange comments on the submission issue, attempting to resolve the disagreement.
2. **DERB referral.** If unresolved within 14 days of the contestation being logged, the matter is referred to the DERB (Everest 80). The DERB has its own published process for review; in summary, the DERB reads the submission, the review response, and the contestation; the DERB may request additional evidence from either side; the DERB publishes a determination.
3. **DERB determination.** The determination is binding for the purposes of the bounty. The DERB's determination is published; the chain record references the determination.

The DERB does not act as a backstop for routine reviews. The DERB only acts on contestations. Calm reviewers do not refer borderline cases to the DERB to avoid making a decision; that would be a process abuse and is itself reviewable.

## Fundamental disagreements

The most consequential case is one where the verifier publishes a write-up arguing the protocol is unsound or misleading on its central claims. This is not a tier-scoring disagreement; it is a substantive claim about the protocol itself.

The route map treats this as the most valuable failure mode. Calm's process:

1. **Acknowledge.** Calm contributors publish a response that does not dismiss the verifier's argument and does not retreat from the verifier's specific findings.
2. **Engage on substance.** Each finding is addressed: agreed-with, partially agreed-with, or disputed with reasoning.
3. **DERB review.** The DERB reviews the disagreement. The disagreement is public; the DERB's review is public.
4. **Protocol revision if warranted.** If the verifier's findings are correct on substance, the protocol is revised. The revision is itself anchored into the chain and is referenced from the original verification record.

The bounty is paid even if the verifier's findings lead Calm to revise the protocol substantially. The bounty rewards effort, not verdict.

## Conflict-of-interest re-checks

During Stage 2, the assigned reviewer re-checks the verifier's conflict-of-interest disclosure against Calm's internal records of past contributors, contractors, and honoraria recipients. If a previously-unnoticed conflict is found:

- The reviewer notifies the verifier.
- If the conflict is disqualifying under the program's stringent independence criteria, the bounty is not paid, but the verification work itself remains public. The chain record (Stage 4) is *not* anchored under the `third_party_verification` kind; it may still be anchored under a different kind (e.g., `community_review`) if the verifier prefers.
- If the conflict is borderline, the matter goes to the DERB.

The intent is to keep "independent third-party verification" as a clean signal. We would rather lose a borderline-eligible verification from the canonical bag-of-Everest-100 than dilute the meaning of "independent."

## Process metrics

Calm publishes aggregate metrics about the bounty program on a quarterly basis:

- Submissions received.
- Submissions accepted, by tier.
- Submissions in revision.
- Submissions in DERB review.
- Total bounty paid.
- Bugs filed by verifiers; bugs resolved.
- Documentation improvements adopted.

The metrics are themselves anchored into the chain.

— Calm, 2026-05-20
