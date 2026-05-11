# Launch kit — public-eye push, 2026-05-12 morning

Drafted: 2026-05-11 by Calm, on instruction from John Bradley.
Anchor: first-demonstration timestamp 2026-05-11 21:55:19 UTC.
Audience: John, who will fire each post from his own accounts.
Constraint: drafts only — nothing posted from here.

## Index

| # | File | Platform | Account | Word/char budget |
|---|------|----------|---------|------------------|
| 1 | [`HN_SHOW_HN.md`](HN_SHOW_HN.md) | Hacker News (Show HN) | John's HN account | Title ≤80 chars; first comment 4-6 paragraphs |
| 2 | [`TWITTER_THREAD.md`](TWITTER_THREAD.md) | X / Twitter | `@{john_handle}` | 10 tweets, each ≤280 chars |
| 3 | [`REDDIT_R_ML.md`](REDDIT_R_ML.md) | r/MachineLearning | John's Reddit account | Body 800-1200 words; flair [R]; link to repo only |
| 4 | [`REDDIT_R_CYBERSEC.md`](REDDIT_R_CYBERSEC.md) | r/cybersecurity | John's Reddit account | Body 600-900 words; repo + bounty links |

Each file is self-contained: title, body, anticipated replies (HN) or per-tweet character counts (X). Tone everywhere is factual, specific, no hype, no exclamation marks, no emoji. Concrete numbers are anchored: 33/34 tests, $100, 56 outlets, 2026-05-11 21:55:19 UTC.

## Recommended posting order

The traffic cycles for these four platforms peak at different times, the audiences cross-reference each other, and the failure modes are different. The order below is tuned to (a) put the technically strongest framing first so that later posts can reference it, (b) avoid cross-platform spam-flagging by spacing the posts, and (c) seed the cybersec audience after the alignment audience so that the cybersec post can credibly reference "the protocol r/ML is already discussing."

### 1. r/MachineLearning — fire first, Tuesday 8:00-9:00 ET

Rationale. r/ML is the highest-friction audience on the list. The post needs to clear moderation, accumulate technical credibility, and survive the first wave of "this looks like product promotion" votes. If r/ML rejects the framing, every later post is weaker. Posting first thing in the US morning catches the East-Coast research crowd and the late-night European crowd, which are the two pockets most likely to engage critically rather than dismissively. Wait ~45 minutes after posting before firing anything else — if r/ML pulls the thread, every later piece needs to be reframed.

What "winning" looks like. Net upvote ratio above 0.85 in the first hour. At least one technical question in the comments (a citation request, a primitive critique, a prior-art pointer, or an objection to the alignment framing). Zero moderator removals. A second-day reach above 200 upvotes and 30 comments is a strong signal.

### 2. Show HN — fire second, Tuesday 9:30-10:30 ET

Rationale. The HN morning cycle peaks 09:00-13:00 ET and the first page is most contested in the first 90 minutes. Posting at 9:30 ET catches the West-Coast pre-coffee window and the East-Coast mid-morning window. The pinned first comment is the leverage — HN readers reward an OP who shows up immediately with substance. The bounty headline ("$100 to anyone who can misalign our AI organization") is the title hook; the comment is where credibility is earned or lost. Have the three anticipated-question replies pre-drafted and fire them within 60 seconds of the first matching top-level comment.

What "winning" looks like. Front-page placement (top 30) within two hours. At least 50 points in the first three hours. At least one substantive critical comment that the OP can engage with — laudatory threads die fast on HN; critical threads keep climbing. A "Show HN" badge intact (no moderator retitle). Zero flagged-as-promotional. A second-day reach to the top 10 of the day is a strong signal.

### 3. X / Twitter thread — fire third, Tuesday 11:00-12:00 ET

Rationale. The Twitter morning cycle peaks 09:00-12:00 ET for tech accounts. Firing after HN means the thread can quote the Show HN URL ("we are on the HN front page, here's the long version") and convert HN readers into followers. The tagged accounts in tweet 10 are most likely to be online in the late US morning. The thread is the highest-fan-out vector — one retweet from any of the tagged accounts can outrun the Reddit and HN reach combined.

What "winning" looks like. Tweet 1 above 50 retweets and 100 likes inside two hours. At least one quote-tweet from a tagged account (or from a high-credibility crypto / AI-safety bystander). Tweet 10 receives at least one of the tagged accounts engaging in the thread (reply, quote-tweet, or like). No mass-block events from any single tagged account. Second-day reach above 50k impressions on the lead tweet is a strong signal.

### 4. r/cybersecurity — fire fourth, Tuesday 13:00-14:00 ET

Rationale. r/cybersecurity peaks in the early US afternoon and is the most resilient of the four platforms to time-of-day variance. Posting fourth lets the post reference the existing HN thread ("there is a live HN discussion at...") and the r/ML thread, both of which have already absorbed the obvious critiques. The cybersec audience tends to engage practically — they want a threat model and a kill-switch architecture, both of which the post delivers in the first three paragraphs. The bounty framing is also strongest here because the audience is closest to actually trying the attacks.

What "winning" looks like. Net upvote ratio above 0.80 in the first three hours. At least one comment from a self-identified red-teamer claiming they will attempt one of the five attack classes. At least one substantive question about the watermark or attestation architecture. Zero moderator removals. A second-day reach above 100 upvotes and 20 comments is a strong signal.

## Per-platform success rubric — at-a-glance

| Platform | Lead metric | Trip-wire metric | Strong-signal metric |
|---|---|---|---|
| r/MachineLearning | Upvote ratio ≥ 0.85 (hour 1) | Moderator removal | 200+ upvotes, 30+ comments day 2 |
| Show HN | Front-page in 2h | Flagged-as-promotional | Top 10 of the day, day 2 |
| X / Twitter | Tweet 1 ≥ 50 RT in 2h | Mass-block by any tagged account | Quote-tweet from a tagged account |
| r/cybersecurity | Upvote ratio ≥ 0.80 (3h) | Moderator removal | A red-teamer publicly committing to an attempt |

## Cross-platform discipline

- Do not cross-link the four posts to each other in the bodies themselves. Cross-linking reads as coordinated promotion. Reference threads in comments only, once they exist.
- If any platform pulls a post for moderation, do not repost on that platform same-day. Reframe based on the moderator's stated reason and reattempt within 24 hours.
- The bounty payout commitment is the load-bearing claim across all four. If a verified break arrives during the launch window, publish the patch and the credit before firing any further posts.
- "Persecute us, but align to the facts." — the closing posture in every piece. If a critic finds a factual error in any of the four drafts before they are posted, fix it.

## What is not in this kit

- Email pitches to the 56 outlets. Those are separate; see the press-list workstream.
- A LinkedIn post. Deliberately omitted — LinkedIn is wrong-audience for the bounty framing.
- A YouTube or podcast pitch. Those are downstream of the four posts above, once initial coverage lands.
- Any post written from any account that is not John's. Calm does not post.
