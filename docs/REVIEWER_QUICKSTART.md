# Reviewer Quickstart — 10 minutes from "I've never seen this repo" to "I have submitted my first review"

**Welcome. If you're reading this, you're probably one of the eight people who answered our outreach overnight, or you arrived from `sameasyou.ai`. Thank you. This page is the fastest path from cold start to a useful first review.**

---

> ## If you have 30 seconds, read this:
>
> - **What this page is:** a 10-minute, copy-pastable guide for first-time reviewers of this repository.
> - **What we're asking of you:** pick one page from [`REVIEW_PAGES.md`](../REVIEW_PAGES.md), read it carefully (desktop + phone), score it against [`REVIEW_RUBRIC.md`](../REVIEW_RUBRIC.md), and submit one filled-in [`REVIEW_OUTPUT_TEMPLATE.md`](../REVIEW_OUTPUT_TEMPLATE.md).
> - **How long this takes:** ~10 minutes per page. Most pages are 1–3 screens long.
> - **You do NOT need:** a cryptography background, a developer setup, or anything more than a browser and a text editor.
> - **What we promise back:** we credit every reviewer who submits a substantive review in the next commit. We act on every substantive fix.

---

## Table of contents

- [Who this guide is for](#who-this-guide-is-for)
- [What you'll need](#what-youll-need)
- [Step 1 — Pick a page (1 min)](#step-1--pick-a-page-1-min)
- [Step 2 — Read it (5 min)](#step-2--read-it-5-min)
- [Step 3 — Score it (3 min)](#step-3--score-it-3-min)
- [Step 4 — Submit it (1 min)](#step-4--submit-it-1-min)
- [How we credit you](#how-we-credit-you)
- [If you only have 5 minutes](#if-you-only-have-5-minutes)
- [If you want to do MORE than one page](#if-you-want-to-do-more-than-one-page)
- [Frequently-anticipated questions](#frequently-anticipated-questions)
- [Help + contact](#help--contact)
- [Feedback](#feedback)

---

## Who this guide is for

- People who received one of the outreach emails sent overnight to Asia-timezone reviewers.
- People who found the project through `sameasyou.ai` and clicked "Review pack."
- People who care about whether new AI-safety / cryptography claims can be read by a smart non-specialist.
- Anyone, technical or not, who is willing to spend 10–60 minutes carefully reading public documentation and saying what's clear and what isn't.

You do **not** need to be a cryptographer, a lawyer, an AI-safety researcher, or a developer. The single best reviewer for these pages is "a careful reader who has not seen this project before." That is the role we are recruiting.

---

## What you'll need

- A browser. Any modern one.
- A phone, ideally — half of the reviewer rubric is about whether the pages render well on mobile.
- A text editor. A free GitHub account if you want to file your review as a pull request (recommended). If you don't have one, you can paste your review into a GitHub issue instead — issues only require an email address.
- Roughly 10 minutes per page reviewed. Most pages take 5; a few take 15.

You do **NOT** need:

- A local clone of the repo.
- A Python install.
- A credential broker, a vault, or any of the tools the project itself describes.
- Permission to do anything destructive — you cannot accidentally break the project by reviewing it.

---

## Step 1 — Pick a page (1 min)

Open [`REVIEW_PAGES.md`](../REVIEW_PAGES.md). It is the master list of every public page in the repository — landing site, README, protocol spec, test results, primary-source records, position pieces.

Pick **one** row to start. Suggested choices for first-time reviewers:

- **If you're a generalist reader** → start with `landing/index.html` (the site itself) or `README.md`. These are the pages most new readers see first.
- **If you have a technical background** → start with `CALM_PACT_PROTOCOL_v0.md` (the protocol spec), `calm_pact/TEST_RESULTS_v0.md` (the test suite), or `src/zk_alignment/POSITION.md` (the one-page position piece).
- **If you have a journalism / fact-checking background** → start with `ANNALS.md` (the historical claim) or one of the `docs/PRIMARY_SOURCE_*.md` files (preserved WhatsApp records).
- **If you only have 5 minutes** → see [If you only have 5 minutes](#if-you-only-have-5-minutes) below.

To avoid two reviewers reviewing the same page at the same time, leave a one-line comment on [the claim issue](https://github.com/CrunchyJohnHaven/calm-vault/issues) (open one with the title `review-claim` if it doesn't exist yet) saying which page you're taking and your time-zone window. This is optional; we'll deduplicate after the fact if you skip it.

---

## Step 2 — Read it (5 min)

Read the page **once on desktop and once on mobile**. The mobile pass matters: one of the rubric axes is "mobile rendering," and many of the pages have not been tested at a 360 px width.

While you read, mentally ask:

- **Do I know what this page is within the first 5 seconds?**
- **Does the first paragraph use plain English, or does it lean on jargon I have to decode?**
- **If the page makes a technical claim, can I verify it — or does it just assert?**
- **Are the links live? Click 2–3 at random.**
- **Are there any obviously wrong facts, dates, or attributions?**

It is fine to spend longer than 5 minutes — many of the pages reward a slow read. Five minutes is a floor, not a ceiling.

---

## Step 3 — Score it (3 min)

Open [`REVIEW_RUBRIC.md`](../REVIEW_RUBRIC.md). It has 10 axes (clarity, accuracy, brand consistency, hyperlinks-work, mobile-rendering, accessibility, intro-paragraph-is-plain-English, CTA-is-clear, technical-claim-is-verifiable, and "what-this-is" landing-zone in 5 seconds), each scored 1 (broken) to 5 (excellent).

A few quick rules:

- A score of **3** means "acceptable; one or two specific issues; fixable in <30 minutes."
- A score of **5** means "could ship to a journalist or an auditor as-is."
- A score of **1** means "factually wrong, unreadable, or actively misleading."
- A blank is not an acceptable answer. If you genuinely can't form a view, score 3 with a question mark and write what's blocking you.
- Add a one-line note **on every axis**. Be specific. Quote the line you object to where you can.

Sum your 10 scores. Apply the decision rule at the bottom of `REVIEW_RUBRIC.md` (45+ green, 35–44 yellow, 25–34 orange, <25 red).

---

## Step 4 — Submit it (1 min)

Copy [`REVIEW_OUTPUT_TEMPLATE.md`](../REVIEW_OUTPUT_TEMPLATE.md). Fill it in — page identification, reviewer identification, the 10 scores, the top-3 concrete fixes (state the *change*, not the *complaint*), an overall verdict in 2–4 sentences. The form is designed to take ~5 minutes after you've finished reading.

Submit it one of two ways:

**Option A — Pull request (preferred).** Create a folder `reviews/` at the repo root if it doesn't exist. Drop your filled-in template at `reviews/<page-path-with-dashes>-<your-handle>.md` (for example `reviews/docs-QUICKSTART-md-alice.md`). Open a pull request titled `review: <page-path>`. We'll merge it.

**Option B — GitHub issue.** Open a new issue titled `review: <page-path>`. Paste the whole filled-in template into the issue body. We'll triage it the same way.

Either path is fine. PRs are easier for us to track; issues are easier for first-time contributors.

---

## How we credit you

For every substantive review we receive, we will:

- **Acknowledge you in the next commit message** ("review thanks: @your-handle"), per the wording on the feedback footer of every page.
- **Add your name to a CONTRIBUTORS-style section** in `README.md` once we have more than five reviews.
- **Cite you by name** in any external write-up, paper, or press piece that draws on your specific fix, with your permission.

If you'd prefer to remain anonymous, say so in the "Reviewer identification" block of your submission — we'll still act on the feedback, we just won't name you.

---

## If you only have 5 minutes

Open [`landing/index.html`](https://sameasyou.ai/) on your phone. Run the "5-second test" only: skim the page for 5 seconds, then close the tab and write down:

1. What did you think this project was?
2. Who did you think it was for?
3. Would you click the primary CTA?

Submit the answer as a one-paragraph GitHub issue titled `5-second test: landing page` and tag it `review`. That's a valid review.

---

## If you want to do MORE than one page

Awesome. Two strong recommendations:

1. **Do them in different reading sessions.** A reviewer reviewing 6 pages in one sitting is much less attentive on page 6 than they were on page 1. Spread the work out.
2. **Pick pages from different layers.** A reviewer who scores landing, README, and the protocol spec gives us much more signal than a reviewer who scores three primary-source pages in a row.

If you review four or more pages, we'll add you to the list of "lead reviewers" on `README.md`.

---

## Frequently-anticipated questions

**Do you pay reviewers?** Not directly. We acknowledge you publicly. If the project's later commercial form (Calm Vault Pro, support contracts, etc.) generates revenue, we will revisit this — but for the initial public-review pass, this is volunteer / contribution-credit work.

**What's the conflict-of-interest policy?** Disclose any conflict you can think of in the "Conflicts of interest" line of `REVIEW_OUTPUT_TEMPLATE.md`. We will publish your review regardless of conflicts; we just want them disclosed.

**Can I review the source code, not the docs?** Yes — but treat that as a separate workflow. Open a pull request with the fix directly. The rubric in this folder is for **prose** review, not code review.

**I think the project is wrong / overclaiming.** Great. Score it accordingly. The single best thing you can do for this project right now is identify any specific overclaim before it ships externally.

**What if I find a security bug?** Do NOT file it publicly. Email `john.b@credexai.xyz` directly. We will respond within 24 hours.

---

## Help + contact

- Stuck on something this guide didn't anticipate? Open an issue at [`github.com/CrunchyJohnHaven/calm-vault/issues`](https://github.com/CrunchyJohnHaven/calm-vault/issues) titled `reviewer help:` — we'll route it within the day.
- Editorial questions: `john.b@credexai.xyz`.
- Technical questions: open an issue tagged `question` — the maintainers will answer publicly so future reviewers benefit.

---

## Feedback

Find an error in *this* quickstart — a missing step, a confusing instruction, a broken link? Open an issue at [`github.com/CrunchyJohnHaven/calm-vault/issues`](https://github.com/CrunchyJohnHaven/calm-vault/issues) — and we'll credit you in the next commit.
