# Onlinejobs.ph — qa_read_through — already posted

> **STATUS:** In Onlinejobs.ph moderation as of 2026-05-11.
> **Record id:** **1644305**
> **Channel:** onlinejobs_ph
> **Moderation window:** up to 48 hours before the post goes live.
> **This file is the source of truth** for what we posted, kept here so the 4-channel test is fully reproducible and the postings under `qa_read_through/` form one comparable set.

---

## Title (as posted)

QA read-through on a short technical document — fixed $25 (₱1,400), 48 hr turnaround — possible ongoing work

## Job description (as posted)

We're running a 4-channel throughput test on QA-read-through work. Same brief, same $25 budget, fired in parallel to Onlinejobs.ph, Upwork, Fiverr, and Reddit r/forhire. The channel that delivers the highest-quality QA pass within 48 hours gets scaled 10x next week — meaning the top performer here gets a recurring stream of similar work at $35/pass.

**The work.** We send you a ~8-15 page markdown technical document. You read it carefully and return a defect list. Defects we count:

- factual error (a claim that contradicts evidence cited in the doc)
- internal inconsistency (claim X on page 3 contradicts claim Y on page 9)
- broken cross-reference (e.g. "see section 4.2" but there is no 4.2)
- sentence that is genuinely ambiguous in a way that matters
- typo or grammar error severe enough to change meaning (not nits)

Each defect in this exact format:

```
LINE:           <line number>
SEVERITY:       S0 (blocks publish) | S1 (must fix) | S2 (should fix) | S3 (nit)
QUOTE:          "<exact text>"
WHY IT'S WRONG: <one or two sentences>
SUGGESTED FIX:  <only if obvious>
```

Deliverable is one flat .md or .txt file, defects in line-number order.

**Budget.** $25 USD (approximately ₱1,400) fixed for one pass. Payment via Wise or PayPal on delivery.

**Turnaround.** 48 hours from when we send the document.

**Scoring.** There are 8 salted bugs in the document — we know exactly where they are and what severities they should be. You earn +1 per salted bug caught with correct severity (max +8), minus 1 per false positive, plus 0.5 per real non-salted defect found. Score >7 means we hire you again next round at $35/pass.

**To apply, reply with all four of these:**

1. One paragraph on why you read carefully — what specifically you do that makes you catch things others miss (not "I have an eye for detail").
2. One link to anything you've QA'd or edited that we can look at — a doc, a PR comment thread, anything.
3. Your time zone and a 4-hour window in the next 48 hours when you can guarantee uninterrupted work.
4. Paste exactly: *"I understand this is a fixed $25 / 48-hour QA test, payment via Wise or PayPal, scored against 8 salted bugs."*

We will respond to specific applications within 12 hours. We will not respond to template / portfolio-only applications.

---

## Onlinejobs.ph-specific gotchas (for our reference)

- Posts go through 48hr moderation; track via record id 1644305.
- Free-tier accounts have a 2-active-posts/month limit. After this test, decide whether to upgrade or rotate.
- No built-in escrow — payment is out-of-band (Wise / PayPal / direct bank). Same risk profile as Reddit.
- Filipino applicants are usually English-fluent but ask for the pull-quote anyway to filter template responses.
- Onlinejobs.ph has no built-in time tracker; we evaluate purely on deliverable.
- Best applicants reply within 24 hours of the post going live (which is often 24-48 hours after submission). Don't panic if the first 12 hours after moderation clears are quiet.
