# Review Rubric — Calm Vault + Bradley-Gavini Protocol

**One page. Ten axes. Score 1-5 on each. Target: every public page passes with a total of 35+ / 50 before we tell the world to read it.**

---

## If you have 30 seconds, read this:

This is a scoring sheet a reviewer uses for **one** page at a time. Open the page, score it on the ten axes below from 1 (broken) to 5 (excellent), write a one-line note per axis, and submit using [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md). The master list of pages is in [`REVIEW_PAGES.md`](REVIEW_PAGES.md). You do **not** need to be a cryptographer, lawyer, or AI researcher to use this rubric — you need to be a careful reader.

---

## Table of contents

- [How to use this rubric](#how-to-use-this-rubric)
- [The 10 axes](#the-10-axes)
- [Scoring scale (shared across all axes)](#scoring-scale-shared-across-all-axes)
- [Decision rules](#decision-rules)
- [Feedback](#feedback)

---

## How to use this rubric

1. Pick a page from [`REVIEW_PAGES.md`](REVIEW_PAGES.md).
2. Read it on **both** desktop and a phone (the mobile-rendering axis is real).
3. Score each of the ten axes from 1 to 5, using the shared scale below.
4. Add one short note per axis explaining the score. Be specific. Quote the line if you can.
5. Compute the total (out of 50). Apply the [decision rule](#decision-rules).
6. Submit using [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md), one file per page reviewed. Open a pull request adding your file to a `reviews/` directory, or paste it into a GitHub issue titled `review: <page-path>`.

A full review of one page should take 5–10 minutes.

---

## The 10 axes

| # | Axis | Score 1 (broken) | Score 5 (excellent) |
|---|---|---|---|
| 1 | **Clarity** | Reads like a wall of jargon; you can't tell what the page is about after two paragraphs. | Every paragraph has a single clear point; a smart non-specialist follows the whole page. |
| 2 | **Accuracy** | Contains a claim you know is wrong, a broken statistic, or a citation that doesn't say what it claims. | Every factual claim is either correct, sourced inline, or marked as opinion / draft. |
| 3 | **Brand consistency** | Conflicting names, taglines, dates, or numbers vs. the rest of the repo (e.g. *Bradley-Gavini* vs. *Calm Pact* used randomly). | The canonical names, dates, tagline, and authorship match the rest of the repo word-for-word. |
| 4 | **Hyperlinks work** | One or more links are dead, point to the wrong file, or `#` anchors don't resolve. | Every link resolves; every cross-reference points to the correct heading or file. |
| 5 | **Mobile rendering** | Tables overflow, headings clip, code blocks force horizontal scroll, dark-mode unreadable. | Page reads cleanly on a 360 px-wide phone in both light and dark mode. |
| 6 | **Accessibility** | No headings, no alt text, color is the only signal, links say "click here". | Heading levels are nested correctly, alt text is descriptive, links have meaningful text. |
| 7 | **Intro paragraph is plain English** | First paragraph leans on jargon (e.g. "Σ-protocol", "Fiat-Shamir", "509(a)(2)") without translating. | A high-school-graduate reader gets the gist from the first paragraph alone. |
| 8 | **CTA is clear** | You don't know what to do next: install? read? email? open an issue? | The page tells the reader exactly what to do next, with one obvious link or command. |
| 9 | **Technical claim is verifiable** | A claim like "X tests passed" or "this proves Y" appears with no way for a reader to reproduce it. | Every technical claim links to a file, a command, a test result, or a timestamped anchor. |
| 10 | **"What this is" landing-zone in 5 seconds** | After 5 seconds of skimming, you can't say what kind of document this is or who it's for. | The page declares its type (README, primary source, protocol spec, transcript, …) and audience above the fold. |

---

## Scoring scale (shared across all axes)

| Score | Meaning |
|---|---|
| **5** | Excellent. Could ship to a journalist or auditor as-is. |
| **4** | Solid. Minor polish, no blockers. |
| **3** | Acceptable. Has 1–2 specific issues; fixable in <30 min. |
| **2** | Weak. Multiple specific issues; a reader could form a wrong impression. |
| **1** | Broken. Either factually wrong, unreadable, or actively misleading. |

A blank (no score) is **not** an acceptable answer. If you can't form a view, leave a note explaining why and score 3 with a question mark.

---

## Decision rules

After computing the total per page:

- **45–50 / 50** — Page is review-ready. Mark it green in the master list.
- **35–44 / 50** — Page is acceptable. Open a single issue with the diff of suggested edits.
- **25–34 / 50** — Page needs a re-pass before we point anyone at it. Block the public-link share until fixed.
- **< 25 / 50** — Page should be temporarily hidden (move to a `drafts/` folder or add a `> ⚠️ draft — do not cite` banner) until rewritten.

Two reviewers must independently confirm a `< 25` score before a page is hidden. One reviewer is enough to flag a `25–34`.

---

## Feedback

Find an error in this rubric, or think an axis is missing? Open an issue at [`github.com/CrunchyJohnHaven/calm-vault/issues`](https://github.com/CrunchyJohnHaven/calm-vault/issues) — and we'll credit you in the next commit.
