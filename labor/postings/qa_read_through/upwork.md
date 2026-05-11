# Upwork — qa_read_through — paste-ready

> **Posting type:** Fixed-price project (NOT hourly — sub-$50 tasks fare worse on hourly because of Upwork's 10-min minimum-billing rules and the way the marketplace sorts hourly jobs by lifetime spend).
> **Project category:** Writing → Editing & Proofreading
> **Skills tags:** QA, Proofreading, Bug Reporting, Editing
> **Budget:** Fixed-price $25
> **Project length:** Less than 1 month, less than 30 hrs/week
> **Experience level:** Intermediate
> **Connects:** ~6 expected
>
> Onlinejobs.ph copy of this same brief is in moderation as record id **1644305**. Fiverr and Reddit copies are siblings of this file.

---

## Title

QA read-through on a short technical document — fixed $25, 48 hr turnaround

## Project description (paste this into the description box exactly)

We're running a 4-channel throughput test on QA-read-through work. Same brief, same budget, fired in parallel to Upwork, Fiverr, Reddit r/forhire, and Onlinejobs.ph. The channel that delivers the highest-quality QA pass within 48 hours gets scaled 10x next week — that means recurring work for the people who deliver well here.

**The work.** We will send you a single technical document (markdown, ~8-15 pages). You read it carefully and produce a defect list. A defect is anything one of:

- factual error (claim contradicts evidence we cite)
- internal inconsistency (claim X on page 3 contradicts claim Y on page 9)
- broken numbered/cross-reference (e.g. "see section 4.2" but there is no 4.2)
- a sentence that, on a careful read, is genuinely ambiguous in a way that matters
- a typo or grammar error severe enough to change meaning (we do not care about Oxford commas)

For each defect you return:

```
LINE:          <line number>
SEVERITY:      S0 (blocks publish) | S1 (must fix) | S2 (should fix) | S3 (nit)
QUOTE:         <the exact text you're flagging, in quotes>
WHY IT'S WRONG: <one or two sentences>
SUGGESTED FIX:  <only if obvious>
```

**Deliverable format.** A single markdown file (or .txt) with the defects listed in the format above, in line-number order. No PDFs with red ink, no Word docs with track-changes, no Google Docs comments — flat text only.

**What we will measure.** We have **8 salted bugs** planted in the document (we know exactly where they are and what severities they should be). Your score is:

- +1 per salted bug you find with correct severity (max +8)
- -1 per false positive (a "defect" that we judge as not actually a defect)
- +0.5 per genuine non-salted defect you find (uncapped)

Mean score from previous tests on similar docs has been around +5. Above +7 puts you in the top tier and means we hire you again at the next test, at $35 for the same scope.

**Budget.** $25 fixed-price for one pass. Pay on delivery via Upwork escrow.

**Turnaround.** 48 hours from contract acceptance. Tell us in your proposal if you cannot meet that.

**To apply, in your proposal:**

1. One sentence telling us why you read carefully (not why you "have an eye for detail" — what specifically you do that makes you catch the things others miss).
2. The pull-quote: copy and paste this sentence into your proposal so we know you read the brief — *"I understand this is a fixed-price 48-hour QA test and there are 8 salted bugs I'm being scored against."*
3. Optional: a 3-5 line sample defect from any document you've worked on, in our format above.

We will not respond to template proposals. We will respond to specific ones within 12 hours.

## Screening questions (Upwork lets you ask 3 — paste these in)

1. Have you done QA on technical writing (engineering docs, API docs, white papers, academic preprints) before? One sentence.
2. What time zone are you in, and what is a 4-hour window in the next 48 hours when you can guarantee no interruptions?
3. (Required pull-quote) Paste exactly: *"I understand this is a fixed-price 48-hour QA test and there are 8 salted bugs I'm being scored against."*

## After posting

- Copy the Upwork job URL into `labor/state/postings.jsonl` (the `orc post` command does this automatically).
- Review proposals at ~12, 24, 36, 48 hr.
- Award one contract. Cap awards at one per channel for this test.

## Upwork-specific gotchas

- Use **fixed-price**, not hourly. Hourly under $50 attracts unserious bidders and Upwork's algorithm sorts hourly jobs to people with $1k+ lifetime spend on the platform.
- Do NOT use a "Project Catalog" gig — that's the seller-driven flow and is closer to Fiverr; we want our own job post.
- Skip Boosted Job for the test (extra $10-30); the 4-channel comparison is cleaner without paid promotion bias.
- Expect 20-60 proposals. Sort by "Best match" first, then by rate ascending. Reject any proposal that does not contain the required pull-quote.
