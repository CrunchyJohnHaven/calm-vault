# Fiverr — qa_read_through — paste-ready

> **Fiverr is a seller-picks-buyer marketplace.** There is no "post a job and wait for bids" flow for us as the buyer in the way Upwork has. We do one of two things:
>
> 1. **Order an existing gig** — search Fiverr for `"proofreading technical document"` / `"qa technical writing"` / `"bug bash documentation"` and order from a seller whose gig matches our spec. Look for: Level 2 or Top Rated seller, 4.9+ rating, >50 reviews, English-native or English-fluent, $20-25 starting tier, and a portfolio that includes technical (not creative) work.
> 2. **Send a Custom Offer / Buyer Request** — message 3-5 candidate sellers with the brief below; ask each to send us a Custom Offer at $25. Pick the one whose reply demonstrates that they read the brief.
>
> Track which seller's gig URL we end up using in `labor/state/postings.jsonl` under `posting_id`.
>
> Onlinejobs.ph copy of this same brief is in moderation as record id **1644305**. Upwork and Reddit copies are siblings of this file.

---

## Search terms to try (in order)

1. `proofreading technical document`
2. `qa technical writing`
3. `bug bash documentation`
4. `editing white paper`
5. `factcheck technical document`

Filter to: Online now, Level 2+ Seller, Delivery time ≤ 2 days, Budget $20-50.

## What to look for in a candidate gig

- Has at least one example of a TECHNICAL document in their portfolio (engineering, scientific, financial — not just marketing copy or fiction).
- Gig description distinguishes between proofreading (typos) and QA (logical/factual checks). If they treat them as the same, skip.
- Communicates in English with normal sentence structure (their gig description is the audition).
- Has at least one Top Rated or Level 2 badge.

## Custom-Offer / Inbox message (paste this when messaging a candidate seller)

> Hi [name],
>
> I'm running a 4-channel throughput test on QA-read-through work — same brief, same budget, fired in parallel to Fiverr, Upwork, Reddit r/forhire, and Onlinejobs.ph. The channel that delivers the strongest QA pass within 48 hours gets scaled 10x next week, so this is a real audition.
>
> The job: I send you a ~8-15 page markdown technical document. You read it carefully and return a defect list — factual errors, internal inconsistencies, broken cross-references, materially ambiguous sentences, and meaning-changing typos. Deliverable is a flat .md or .txt file with each defect in this format:
>
> ```
> LINE:           <line number>
> SEVERITY:       S0 / S1 / S2 / S3
> QUOTE:          "<exact text>"
> WHY IT'S WRONG: <one or two sentences>
> SUGGESTED FIX:  <only if obvious>
> ```
>
> Budget: $25 USD via Fiverr Custom Offer, 48 hour delivery, Standard package.
>
> Scoring: there are 8 salted bugs in the document. I'm measuring: salted bugs caught (with correct severity) minus false positives, plus partial credit for non-salted real defects. Top performers from this round get recurring work at $35/pass.
>
> Two quick questions before I send the doc:
>
> 1. Have you done QA on technical writing (engineering, API, white-paper, academic) — yes/no, one example?
> 2. Please paste exactly back: "I understand this is a fixed-budget 48-hour QA test with 8 salted bugs."
>
> If you can do it for $25 in 48 hours, send me a Custom Offer and I'll accept it within the day.
>
> Thanks,
> John

## After sending

- For each seller messaged, add a row to `labor/state/applications.jsonl` (or let `orc inbox` do it once we wire Fiverr inbox export).
- Award one Custom Offer this round. Reject sellers whose reply is generic / does not include the required pull-quote.

## Fiverr-specific gotchas

- Fiverr adds a **5.5% service fee + $2.50 small-order fee under $50**. Set our test budget to **$25 gig price** so total out-of-pocket lands around $27.88 — still inside the $25-per-channel test envelope as a rounding error; record actual paid amount in `work.jsonl`.
- Fiverr does NOT support hourly billing. Order as Standard package (fixed price), 48hr delivery.
- Sellers may try to upsell to a higher-tier package. Politely decline; we want apples-to-apples vs. the other channels.
- If a seller refuses to commit to 48 hrs, pick another seller — don't extend the deadline for this test.
- Revisions: the default Fiverr revision policy gives the seller a chance to fix issues. For this test we are NOT requesting revisions — the deliverable is scored as-submitted. Make that explicit in the order requirements box.
