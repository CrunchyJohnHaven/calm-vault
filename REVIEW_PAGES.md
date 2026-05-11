# Review Pages — Master List

**Every public page in this repository, with the local path and the URL where reviewers can read it. Reviewers should use [`REVIEW_RUBRIC.md`](REVIEW_RUBRIC.md) and submit one [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md) per page.**

---

## If you have 30 seconds, read this:

This is the master checklist for the human review of every page on `sameasyou.ai` (and the underlying [`calm-vault`](https://github.com/CrunchyJohnHaven/calm-vault) repository it's built from). Each row is a page reviewers can score with [`REVIEW_RUBRIC.md`](REVIEW_RUBRIC.md). Pick the rows you're qualified to review, score each on the 10 rubric axes, submit one form per page, and we'll credit you in the next commit.

---

## Table of contents

- [How to use this list](#how-to-use-this-list)
- [The landing page](#the-landing-page)
- [Top-level pages (README + governance + protocol spec)](#top-level-pages-readme--governance--protocol-spec)
- [Docs (getting-started + primary sources + working library)](#docs-getting-started--primary-sources--working-library)
- [Calm Pact protocol artifacts (tests + transcripts)](#calm-pact-protocol-artifacts-tests--transcripts)
- [Paper (long-form write-up)](#paper-long-form-write-up)
- [Autonomous AI Labs (AAL) Components](#autonomous-ai-labs-aal-components)
- [Source-tree position pieces](#source-tree-position-pieces)
- [Review artifacts (these four files)](#review-artifacts-these-four-files)
- [Out of scope](#out-of-scope)
- [Feedback](#feedback)

---

## How to use this list

**First-time reviewers, start here:** [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md). It's a 10-minute walkthrough that takes you from "I've never seen this repo" to "I have submitted my first review."

1. Pick one or more pages from the tables below. Reviewers are encouraged to **claim** pages by commenting on issue `#review-claim` (open a new issue with that title if it doesn't exist) so we don't double up.
2. Read the page on both desktop and mobile.
3. Score it using [`REVIEW_RUBRIC.md`](REVIEW_RUBRIC.md).
4. Submit one [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md) per page (open a PR adding it under `reviews/<page-name>-<reviewer-handle>.md`, or paste it into a GitHub issue titled `review: <page-path>`).
5. Drive-by typo fixes: just open a PR directly. No rubric needed for one-character fixes.

Canonical URL prefix on GitHub: `https://github.com/CrunchyJohnHaven/calm-vault/blob/main/`

Canonical site root: `https://sameasyou.ai/`

---

## The landing page

| # | Path | GitHub URL | Live URL | Reviewer focus |
|---|---|---|---|---|
| 1 | [`landing/index.html`](landing/index.html) | [`landing/index.html`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/landing/index.html) | [`sameasyou.ai`](https://sameasyou.ai/) | The 5-second test. Above-the-fold clarity. Mobile rendering. CTA. |

---

## Top-level pages (README + governance + protocol spec)

| # | Path | GitHub URL | Reviewer focus |
|---|---|---|---|
| 2 | [`README.md`](README.md) | [`README.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/README.md) | The full pitch. Intro paragraph plain-English. Quickstart command actually copy-pasteable. |
| 3 | [`ANNALS.md`](ANNALS.md) | [`ANNALS.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/ANNALS.md) | The historical-claim document. Tone calibration. Verifiability of every claim. |
| 4 | [`BOOK_TITLE.md`](BOOK_TITLE.md) | [`BOOK_TITLE.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/BOOK_TITLE.md) | Title-page draft. Brand consistency with the rest of the repo. |
| 5 | [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) | [`CALM_PACT_PROTOCOL_v0.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/CALM_PACT_PROTOCOL_v0.md) | The protocol spec. Cryptographic accuracy. Reproducibility of the security claims. |
| 6 | [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | [`CODE_OF_CONDUCT.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/CODE_OF_CONDUCT.md) | Standard Contributor Covenant; check the enforcement contact is current. |
| 7 | [`LICENSE`](LICENSE) | [`LICENSE`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/LICENSE) | Apache 2.0 verbatim — no scoring needed; flag only if it's been modified. |

---

## Docs (getting-started + primary sources + working library)

| # | Path | GitHub URL | Reviewer focus |
|---|---|---|---|
| 8 | [`docs/QUICKSTART.md`](docs/QUICKSTART.md) | [`docs/QUICKSTART.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/QUICKSTART.md) | The 5-minute walkthrough. Every command should work on a fresh machine. |
| 9 | [`docs/PRIMARY_SOURCE_1_FAMILY.md`](docs/PRIMARY_SOURCE_1_FAMILY.md) | [`docs/PRIMARY_SOURCE_1_FAMILY.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/PRIMARY_SOURCE_1_FAMILY.md) | Preserved family WhatsApp text + provenance. Sensitivity calibration. |
| 10 | [`docs/PRIMARY_SOURCE_2_KOUSHIK.md`](docs/PRIMARY_SOURCE_2_KOUSHIK.md) | [`docs/PRIMARY_SOURCE_2_KOUSHIK.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/PRIMARY_SOURCE_2_KOUSHIK.md) | Preserved K&K thread text + attribution to Koushik Gavini. |
| 11 | [`docs/PRIMARY_SOURCE_3_ORIGIN_STORY.md`](docs/PRIMARY_SOURCE_3_ORIGIN_STORY.md) | [`docs/PRIMARY_SOURCE_3_ORIGIN_STORY.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/PRIMARY_SOURCE_3_ORIGIN_STORY.md) | The origin story + the canonical tagline. |
| 12 | [`docs/BOOK_TITLE_LOCKED.md`](docs/BOOK_TITLE_LOCKED.md) | [`docs/BOOK_TITLE_LOCKED.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/BOOK_TITLE_LOCKED.md) | Title-lock doctrine. Cross-reference accuracy. |
| 13 | [`docs/HACKATHON_RESULTS.md`](docs/HACKATHON_RESULTS.md) | [`docs/HACKATHON_RESULTS.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/HACKATHON_RESULTS.md) | Design tournament writeup. Honest comparison vs. existing products. |
| 14 | [`docs/TIMESTAMP_ANCHORS.md`](docs/TIMESTAMP_ANCHORS.md) | [`docs/TIMESTAMP_ANCHORS.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/TIMESTAMP_ANCHORS.md) | The witness anchors. Every link should resolve. |
| 14a | [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md) | [`docs/REVIEWER_QUICKSTART.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/REVIEWER_QUICKSTART.md) | The 10-minute reviewer onboarding. If a first-time reviewer can't follow it, the whole review pack fails. |

---

## Calm Pact protocol artifacts (tests + transcripts)

| # | Path | GitHub URL | Reviewer focus |
|---|---|---|---|
| 15 | [`calm_pact/COMBINED_TEST_VERDICT_v0.md`](calm_pact/COMBINED_TEST_VERDICT_v0.md) | [`COMBINED_TEST_VERDICT_v0.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/COMBINED_TEST_VERDICT_v0.md) | The 33/34-tests-pass claim. Reproducibility of the test suite. |
| 16 | [`calm_pact/FIRST_DEMO_TRANSCRIPT_2026-05-11.md`](calm_pact/FIRST_DEMO_TRANSCRIPT_2026-05-11.md) | [`FIRST_DEMO_TRANSCRIPT_2026-05-11.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/FIRST_DEMO_TRANSCRIPT_2026-05-11.md) | First-demo transcript. Cryptographic anchor reproducibility. |
| 17 | [`calm_pact/TEST_RESULTS_v0.md`](calm_pact/TEST_RESULTS_v0.md) | [`TEST_RESULTS_v0.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/TEST_RESULTS_v0.md) | The full per-test result table + the one performance miss. |

---

## Paper (long-form write-up)

This row is **provisional** — the linked file is landing overnight from a parallel session. If the URL 404s when you click it, skip the row and pick something else; we'll mark it green once it commits.

| # | Path | GitHub URL | Status | Reviewer focus |
|---|---|---|---|---|
| 17a | [`paper/bradley-gavini-protocol-v0.html`](paper/bradley-gavini-protocol-v0.html) | [`paper/bradley-gavini-protocol-v0.html`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/paper/bradley-gavini-protocol-v0.html) | **Landing overnight** | Long-form HTML write-up of the protocol. Same accuracy + brand-consistency checks as `CALM_PACT_PROTOCOL_v0.md`. |

---

## Autonomous AI Labs (AAL) Components

These rows are **provisional** — the linked files are landing overnight from parallel Devin sessions. If a URL 404s when you click it, skip that row and pick another; we'll mark each one green once its commit lands. The five-component series describes the Autonomous AI Labs program; Component 1 is already represented inside this repo, Components 2–5 land overnight.

| # | Path | GitHub URL | Status | Reviewer focus |
|---|---|---|---|---|
| 17b | `aal/component-2/README.md` | [`aal/component-2/README.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/aal/component-2/README.md) | **Landing overnight** | AAL Component 2 entry point. Clarity for a non-AAL-specialist reviewer. |
| 17c | `aal/component-3/README.md` | [`aal/component-3/README.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/aal/component-3/README.md) | **Landing overnight** | AAL Component 3 entry point. |
| 17d | `aal/component-4/README.md` | [`aal/component-4/README.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/aal/component-4/README.md) | **Landing overnight** | AAL Component 4 entry point. |
| 17e | `aal/component-5/README.md` | [`aal/component-5/README.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/aal/component-5/README.md) | **Landing overnight** | AAL Component 5 entry point. |

If by the time you read this the parallel sessions have used a different layout (e.g. `components/aal-2/`, `docs/aal/component-2.md`, etc.), the actual path will be discoverable from a fresh `ls` of the repo root and/or the next commit on `main`. Update the row in your review submission to match the path you actually reviewed.

---

## Source-tree position pieces

| # | Path | GitHub URL | Reviewer focus |
|---|---|---|---|
| 18 | [`src/zk_alignment/POSITION.md`](src/zk_alignment/POSITION.md) | [`src/zk_alignment/POSITION.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/src/zk_alignment/POSITION.md) | The 21:40 UTC position piece. Cryptographic accuracy. Tone for the outreach audience. |

---

## Review artifacts (these four files)

| # | Path | GitHub URL | Reviewer focus |
|---|---|---|---|
| 19 | [`REVIEW_RUBRIC.md`](REVIEW_RUBRIC.md) | [`REVIEW_RUBRIC.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/REVIEW_RUBRIC.md) | The rubric itself. Are the 10 axes the right ones? |
| 20 | [`REVIEW_PAGES.md`](REVIEW_PAGES.md) | [`REVIEW_PAGES.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/REVIEW_PAGES.md) | This file. Are any public pages missing? |
| 21 | [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md) | [`REVIEW_OUTPUT_TEMPLATE.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/REVIEW_OUTPUT_TEMPLATE.md) | The reviewer form. Is it the right amount of work to fill in? |
| 22 | [`docs/REVIEWER_QUICKSTART.md`](docs/REVIEWER_QUICKSTART.md) | [`docs/REVIEWER_QUICKSTART.md`](https://github.com/CrunchyJohnHaven/calm-vault/blob/main/docs/REVIEWER_QUICKSTART.md) | The reviewer onboarding guide. Test by following it yourself, cold. |

---

## Out of scope

These exist in the repository but are **not** scored by this review pass:

- [`src/calm_vault.py`](src/calm_vault.py) — the broker source. Review code in the usual way: read it, run it, file a code-level PR.
- [`SMOKE_TEST_TRANSCRIPT.txt`](SMOKE_TEST_TRANSCRIPT.txt) — a captured terminal session. Verified by re-running, not by prose review.
- [`requirements.txt`](requirements.txt) — single dependency line.
- `.github/ISSUE_TEMPLATE/*` — issue forms. Review via the GitHub issue-creation UI, not as prose.
- Git history (commits, tags). Treat as immutable historical artifact.

---

## Feedback

Find a page that's missing from this list, or a path that's wrong? Open an issue at [`github.com/CrunchyJohnHaven/calm-vault/issues`](https://github.com/CrunchyJohnHaven/calm-vault/issues) — and we'll credit you in the next commit.
