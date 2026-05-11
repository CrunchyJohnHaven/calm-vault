# Reddit r/forhire — qa_read_through — paste-ready

> **Subreddit:** r/forhire (primary). Optional secondary repost in r/HireaWriter after 24 hr if the r/forhire post is under-bid.
> **Required tag:** post title MUST start with `[Hiring]`. Without that tag the post is auto-removed by AutoModerator.
> **Account requirements:** posting account needs ≥10 comment karma and ≥30 day account age. John's main account qualifies. Check r/forhire rules before each post — they change.
> **Reposting rule:** r/forhire bans posting the same job within 7 days. After this test, do not re-post the same brief; instead rotate to a slightly different task.
> **No platform fees, no escrow.** Payment is direct (PayPal, Wise, Venmo-US-only, or crypto). Disputes are on us — Reddit will not refund.
>
> Onlinejobs.ph copy of this same brief is in moderation as record id **1644305**. Upwork and Fiverr copies are siblings of this file.

---

## Post title (paste exactly)

`[Hiring] QA read-through on a short technical document — $25 fixed, 48 hr turnaround (one of a 4-channel throughput test)`

## Post body (paste exactly)

Hi r/forhire,

I'm running a 4-channel throughput test on QA-read-through work. Same brief, same budget, fired in parallel to Reddit r/forhire, Upwork, Fiverr, and Onlinejobs.ph. Whichever channel delivers the highest-quality QA pass within 48 hours gets scaled 10x next week — recurring work at $35/pass for whoever proves out here.

**The work.** I will send you a ~8-15 page markdown technical document. You read it carefully and return a defect list. Defects we count:

- factual error (claim contradicts evidence cited in the doc)
- internal inconsistency (claim X on page 3 contradicts claim Y on page 9)
- broken cross-reference (e.g. "see §4.2" but there is no §4.2)
- sentence that is genuinely ambiguous in a way that matters
- typo or grammar error severe enough to change meaning (not nits)

Each defect in this format:

    LINE:           <line number>
    SEVERITY:       S0 (blocks publish) | S1 (must fix) | S2 (should fix) | S3 (nit)
    QUOTE:          "<exact text>"
    WHY IT'S WRONG: <one or two sentences>
    SUGGESTED FIX:  <only if obvious>

Deliverable is a single flat .md or .txt file, defects in line-number order. No PDFs, no Word.

**Budget.** $25 USD fixed. Half ($12.50) on contract acceptance, half on delivery. Payment via PayPal (Goods & Services, fees on me) or Wise. Venmo only if you're US-based.

**Turnaround.** 48 hours from when I send you the document.

**Scoring.** I have 8 salted bugs in the doc and I know exactly what they are and what severities. Your score is: salted bugs caught with correct severity (+1 each, max +8), minus false positives (-1 each), plus partial credit for non-salted real defects (+0.5 each). Top scorers get recurring $35/pass work.

**To apply, DM me with all four of these:**

1. One paragraph on why you read carefully — not "eye for detail," what *specifically* you do that makes you catch the things others miss.
2. One link to anything you've QA'd or edited that we can look at (a public doc, a PR review, anything).
3. Your time zone and a 4-hour window in the next 48 hours when you can guarantee uninterrupted work.
4. Paste exactly: *"I understand this is a fixed $25 / 48-hour QA test, payment via PayPal or Wise, scored against 8 salted bugs."*

I will respond to specific applications within 12 hours. I will not respond to template / portfolio-only DMs.

Cheers,
John

## After posting

- Save the Reddit post permalink into `labor/state/postings.jsonl`.
- Crosspost manually to r/HireaWriter at the 24 hr mark if r/forhire under-delivers. Do NOT crosspost via the Reddit button (that's flagged as spam in some subs); make a fresh post.
- Set Old Reddit messaging on so DMs route to your inbox, not chat.
- Log each DM applicant in `labor/state/applications.jsonl` via `orc inbox` (the listener.jsonl pipe).

## Reddit-specific gotchas

- **[Hiring] tag is mandatory** in r/forhire — without it AutoMod removes the post in <60 seconds.
- **No escrow.** This is the biggest channel-specific risk. Pay half up-front *only* for applicants you'd actually re-hire; reject applicants who insist on 100% up-front for this test.
- r/forhire prohibits crossposting the same job; if we want to retry, change the brief materially.
- Don't link your Cash App or wire transfer — Reddit's spam filters hit those. PayPal Goods & Services + Wise are the safe defaults.
- Read the current r/forhire rules in the sidebar before each post; they update them every few months and a single missing tag will get the post auto-removed.
