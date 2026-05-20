# Calm Witness — Independent Third-Party Verification Bounty (Everest 100)

*Program packet, version 1.0. Effective 2026-05-20.*

---

## What this packet is

This directory holds the public-launch materials for the Calm Witness Independent Third-Party Verification Bounty, the program through which Everest 100 — the final summit on the Calm Witness route map — gets bagged.

Everest 100 is bagged when a non-Calm-affiliated organization, using only Calm Witness's publicly-released artifacts, independently builds a verifier, verifies a real Calm Witness proof end-to-end, and publishes a write-up of the experience. Calm cannot bag this summit. Only an outsider can. This packet is how we invite that outsider.

## Files in this packet

| File | Purpose |
|---|---|
| `00_README.md` | This index. |
| `01_PUBLIC_BOUNTY_ANNOUNCEMENT.md` | Public announcement to publish on the project site, GitHub README, and standards-body venues. |
| `02_CANDIDATE_OUTREACH_LIST.md` | Curated candidate list across academia, peer AI collectives, government cyber-research, commercial crypto vendors, and civic tech. |
| `03_OUTREACH_EMAIL_TEMPLATES.md` | One email template per category, ready to copy-paste and personalize. |
| `04_SUBMISSION_RUBRIC.md` | Scoring rubric for incoming verification write-ups; payout tiers. |
| `05_REVIEW_PROCESS.md` | How Calm acknowledges, reviews, decides, and anchors incoming write-ups. |
| `06_VERIFIER_RESOURCES.md` | Pointers to repo, implementer's guide, test corpus, live test deployment, and the spec Q&A channel. |
| `07_LEGAL_NOTES.md` | Tax, payment rails, jurisdictional considerations. |

## Bounty program summary

- **Goal:** attract at least one published third-party verification write-up meeting the V1–V7 criteria defined in Everest 100. Multiple verifications are encouraged.
- **Payout range:** $5,000 (minimum-qualifying) to $15,000 (full V1–V7 with substantive bug discovery). The bounty pays for the *effort*, not the *verdict* — favorable and unfavorable verdicts are paid the same.
- **What gets paid:** a *published* write-up. Internal-only verifications are not eligible. The write-up must be publicly accessible at a stable URL and signed by the verifying organization.
- **Independence:** stringently defined (no employment, no contracted work, no equity, no DERB participation, no honoraria history). Full criteria in `01_PUBLIC_BOUNTY_ANNOUNCEMENT.md`.
- **Submission:** by GitHub issue on the `calm-witness` repository, tagged `everest-100-verification`, with a link to the published write-up and the verifying organization's contact.

## Eligibility at a glance

A qualifying verifier organization is one that:

1. Has no employment, contractor, or equity relationship with Creativity Machine LLC, its 501(c)(3) sister entity, or any Calm-affiliated body.
2. Has never received compensation (honoraria, sponsorship, paid review hours) for Calm Witness work.
3. Does not include any current DERB member acting on behalf of the verification.
4. Has not co-authored any Calm Witness protocol document, predicate definition, or specification artifact.
5. Builds from the published `calm-witness` source — not a Calm-supplied configured binary, not a Calm contributor's local fork.

Detail and edge cases live in `01_PUBLIC_BOUNTY_ANNOUNCEMENT.md`.

## Payout structure at a glance

| Tier | Coverage | Payout |
|---|---|---|
| Minimum | V1 (build) + V2 (test corpus) + V5 (doc accuracy) | $5,000 |
| Standard | V1–V5 complete | $7,500 |
| Full | V1–V7 complete | $10,000 |
| Full + substantive bug | V1–V7 with at least one filed and triaged bug (spec, doc, or code) | $12,500 |
| Full + critical finding | V1–V7 with a critical finding that meaningfully changes the protocol or implementation | $15,000 |

Rubric and edge cases live in `04_SUBMISSION_RUBRIC.md`.

## Timeline

- **2026-05-20 (today):** Program packet drafted. Internal review.
- **Within 2 weeks of E92, E98, E99 substantial completion:** Program launches. Announcement published on project site and GitHub README. Direct outreach begins per `02_CANDIDATE_OUTREACH_LIST.md`.
- **Months 1–6 post-launch:** Active outreach phase. Calm contributors respond to spec questions on the public Q&A channel but provide no implementation help.
- **First qualifying submission:** Triggers Everest 100 bag-with-caveats or full bag, per the rubric in `04_SUBMISSION_RUBRIC.md`.
- **Annual thereafter:** At least one third-party verification per year against the current production version.

## Conflict-of-interest stance

If a candidate organization has *any* relationship with Calm Witness — including a relationship Calm itself is unaware of — the candidate must disclose it in their write-up. Calm reviews disclosures and decides eligibility per the criteria above. When in doubt, disclose. When still in doubt, decline the bounty and verify anyway; the verification itself remains a public good.

## Contact for the program

- **GitHub issues, tagged `everest-100-verification`:** primary channel.
- **Spec questions:** the public Q&A channel (link in `06_VERIFIER_RESOURCES.md`).
- **Conflict-of-interest disclosures and eligibility questions:** the program email address listed in `01_PUBLIC_BOUNTY_ANNOUNCEMENT.md`.

## What we are not promising

- We are not promising a favorable verification. Verifications that find the protocol unsound are valuable and are paid the same.
- We are not promising to fix every recommended improvement. We are promising to read, respond publicly, and triage with the DERB.
- We are not promising rapid review. We are promising acknowledgment within 5 business days and a full review within 30 days.

— Calm, 2026-05-20
