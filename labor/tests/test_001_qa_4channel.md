# test_001 — qa_read_through, 4 channels parallel

> **Thesis (John, 2026-05-11 22:55 ET):**
> *"With offshore labor we can do 10x more I bet. Maybe 100x. We must cast a wide net and test carefully for throughput and maximize."*
>
> This is the first concrete test of that thesis: same QA-read-through brief, same budget, fired in parallel to four channels. Whichever channel wins on `$/quality-point` gets scaled 10x in week 2.

## Test ID

`test_001_qa_4channel`

## Hypothesis

For QA read-through of a short technical document, **at least one offshore channel will deliver a quality score ≥7/10 for under $25, within 48 hours**. We don't yet know which channel that is — the test exists to find out.

We expect a priori (with low confidence):
- **Onlinejobs.ph** to win on raw $/hr because Filipino market rates are lowest.
- **Upwork** to win on speed-to-first-applicant.
- **Fiverr** to deliver mid-quality on a fixed turnaround but cap revisions.
- **Reddit r/forhire** to be a wild card — best-case excellent, worst-case nobody bites.

## Setup

| field | value |
|---|---|
| task_type | `qa_read_through` |
| channels | `onlinejobs_ph` (already posted), `upwork`, `fiverr`, `reddit_forhire` |
| budget per channel | **$25** |
| total budget | **$100** |
| target turnaround | **48 hours** from contract acceptance |
| brief | `~/AllData/labor/QA_BUG_FIND_v1.md` (a single ~8-15 page technical doc) |
| salted bugs | **8** of known severity, pre-planted |

The brief is identical across channels. The only thing that varies is the channel.

## Postings (paste-ready)

| channel | template | posted-as id |
|---|---|---|
| onlinejobs_ph | [`labor/postings/qa_read_through/onlinejobs_ph.md`](../postings/qa_read_through/onlinejobs_ph.md) | **1644305** (in moderation as of 2026-05-11 22:55 UTC) |
| upwork | [`labor/postings/qa_read_through/upwork.md`](../postings/qa_read_through/upwork.md) | to post |
| fiverr | [`labor/postings/qa_read_through/fiverr.md`](../postings/qa_read_through/fiverr.md) | to message 3-5 sellers |
| reddit_forhire | [`labor/postings/qa_read_through/reddit_forhire.md`](../postings/qa_read_through/reddit_forhire.md) | to post |

To re-emit the paste-ready bodies:

```bash
labor/orc post \
    --task qa_read_through \
    --channels upwork,fiverr,reddit_forhire,onlinejobs_ph \
    --budget 100 \
    --test-id test_001_qa_4channel
```

## Metrics

| metric | definition |
|---|---|
| time-to-first-qualified-applicant | wall-clock hours from posting (or post-moderation, for `onlinejobs_ph`) to first applicant whose response **includes the required pull-quote** |
| time-to-delivery | hours from `accepted_at` to `delivered_at` per work row |
| quality score | 0..10. Formula: `salted_bugs_correct_severity (+1 each, max +8) - false_positives (-1 each) + non_salted_real_defects (+0.5 each)`, clipped to [0, 10]. |
| total cost | sum of `total_paid_usd` for the awarded contract (excluding platform fees on John's side; record fees in `notes` if material) |
| **headline:** $/quality-point | `mean_cost_per_hr / mean_quality`. Lower is better. |

## Process

1. **t=0** — Post brief on all four channels in parallel. Onlinejobs.ph is already in moderation (post id 1644305); fire the other three as soon as the postings.jsonl is committed.
2. **t=0..t+24h** — Run `orc inbox` whenever new applicants arrive. Shortlist anyone whose reply contains the required pull-quote.
3. **t=24h or first 2 shortlists per channel, whichever first** — Award **one** contract per channel. Send brief.
4. **t=48h** — Collect deliverables. For each, manually grade against the salted-bug ground truth; record via `orc score`.
5. **t=72h** — Run `orc leaderboard --write` and `orc dashboard --write`. Identify winner.
6. **Week 2** — Cast 10x the volume of QA work to the winner. Hold the other channels in reserve.

## Stop conditions

- A channel returns **zero qualified applicants** by **t+36h** → mark that channel as `dead` in postings.jsonl, do not award.
- A worker fails to deliver by **t+72h** → record `quality=0`, do not pay.
- Aggregate burn exceeds **$110** before all four deliveries land → stop the test, score what we have.

## Recording results

Use the CLI for everything; do not hand-edit JSONL.

```bash
# When an applicant replies (typically from ~/AllData/inbox/listener.jsonl):
labor/orc inbox

# When a worker delivers (one command per worker):
labor/orc score worker_upwork_anya \
    --test test_001_qa_4channel \
    --channel upwork \
    --task qa_read_through \
    --quality 8.5 \
    --hours 2.5 \
    --paid 25.00 \
    --accepted-at "2026-05-12T01:10:00Z" \
    --delivered-at "2026-05-13T14:00:00Z" \
    --notes "8/8 salted bugs caught, 0 false positives, 3 real non-salted defects"

# After all four deliver:
labor/orc leaderboard --write
labor/orc recommend --task qa_read_through
labor/orc dashboard  --write
```

## Decision rule for "winner"

The winning channel is the one with **lowest $/quality-point** AND **quality ≥ 7.0**. If no channel hits quality ≥ 7.0, the test result is `null` — we tighten the brief and rerun rather than scaling a mediocre channel.

## Sample-size caveat

n=1 per channel is not statistically meaningful — it's a screening test. Channels that pass screening get a second test (n=3-5 each) before we 10x them. The leaderboard treats every cell honestly: it shows `n` and we visually penalize anything with `n<3`.
