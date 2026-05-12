# Sentiment scanner — pre-launch monitoring for AAO Network mentions

A small, dependency-free polling script that watches Twitter/X, Reddit, Hacker
News, and news feeds for mentions of:

- **AAO Network**
- **Calm Vault**
- **Technosocialism**
- **Bradley-Gavini Protocol**
- **Money Python**
- **Same As You** (anchored to our context — AI / agent / Bradley / Calm / Vault
  / credexai / sameasyou.ai — so we don't pick up the 1969 Donovan album)

For each new mention it classifies sentiment (positive / negative / neutral) and
topic (technical / political / mascot / merch / general), appends the record to
`sentiment_log.jsonl`, and — when warranted — writes an alert under `mentions/`
for Calm to surface to John.

This is intentionally a single Python file with **no extra runtime dependencies**.
It uses `urllib` and `xml.etree` from the standard library. The `cryptography`
package already in the repo's `requirements.txt` is not required here.

---

## Sources

| Source           | Auth required                    | Notes                                                                                  |
|------------------|----------------------------------|----------------------------------------------------------------------------------------|
| Reddit           | none                             | Polls `r/MachineLearning`, `r/cscareerquestions`, `r/futureofwork`, `r/cooperatives`, `r/economy`, `r/EffectiveAltruism` via the public `*.json` endpoint. |
| Hacker News      | none                             | `hn.algolia.com/api/v1/search_by_date` — stories + comments.                            |
| Google News      | none                             | `news.google.com/rss/search` — parsed as RSS.                                          |
| NewsAPI.org      | `NEWSAPI_KEY` env var (optional) | Adds richer publisher coverage if you have a key.                                       |
| Twitter/X (Grok) | `~/.xai/credexai-grok-key` **or** `XAI_API_KEY` env var (optional) | Uses xAI's Grok Live Search to pull recent X posts matching each term. Skipped silently if no key. |

If a source is unauthenticated or rate-limited on a given sweep, the scanner
logs a warning to stderr and continues — a single broken source never kills the
loop.

## Classification

- If `ANTHROPIC_API_KEY` is set, each mention is classified by Claude (Haiku) with
  a small JSON-only prompt.
- Otherwise the scanner falls back to a built-in keyword heuristic so it works
  out of the box without any API keys at all.

Each log line records which classifier was used (`classifier: "claude" | "heuristic"`).

## Alerts

Files written under `mentions/`:

- `mentions/first_mention.json` — overwritten once, the first time the scanner
  ever sees a mention across any source. A flag file (`state/first_mention_recorded`)
  is created at the same time so this never fires twice.
- `mentions/alert_negative.json` — the most recent negative-sentiment mention
  whose engagement crossed the threshold. A running history is also appended
  to `mentions/alert_negative_history.jsonl`.
- `mentions/alert_viral.json` — the most recent mention that crossed the viral
  threshold for its platform. History at `mentions/alert_viral_history.jsonl`.

Thresholds (tunable as constants near the top of `scanner.py`):

| Platform     | Viral                | Negative-but-loud       |
|--------------|----------------------|-------------------------|
| Reddit       | score ≥ 100          | score ≥ 5 AND negative  |
| Hacker News  | points ≥ 100         | points ≥ 10 AND negative |
| Twitter / X  | likes ≥ 1000         | likes ≥ 50 AND negative |
| News         | n/a (always log)     | n/a                     |

Calm should `cat mentions/first_mention.json` and `ls mentions/alert_*.json` at
the top of each shift; the alert files only exist if something has fired.

## Running

```bash
# foreground, default 60s interval
python3 sentiment_scanner/scanner.py

# single sweep, exit (useful for cron or smoke-testing)
python3 sentiment_scanner/scanner.py --once

# custom interval (seconds)
python3 sentiment_scanner/scanner.py --interval 120
```

### As a background process

```bash
# from repo root
nohup python3 sentiment_scanner/scanner.py \
    > sentiment_scanner/scanner.log 2>&1 &

# the PID is written to sentiment_scanner/scanner.pid by the script itself
cat sentiment_scanner/scanner.pid

# tail the log
tail -f sentiment_scanner/scanner.log
```

### Stopping it

```bash
kill "$(cat sentiment_scanner/scanner.pid)"
# or, if the PID file is stale:
pkill -f 'sentiment_scanner/scanner.py'
```

SIGTERM / SIGINT are handled gracefully — the current sweep finishes, state is
saved, and the PID file is removed before exit.

### Optional credentials

```bash
# Anthropic — better sentiment + topic classification
export ANTHROPIC_API_KEY=...

# NewsAPI.org — richer news coverage
export NEWSAPI_KEY=...

# xAI Grok — Twitter/X live search
mkdir -p ~/.xai
echo 'xai-...' > ~/.xai/credexai-grok-key
# or:
export XAI_API_KEY=xai-...
```

## Output schema

`sentiment_log.jsonl` is one JSON object per line:

```json
{
  "id": "reddit:t3_abc123",
  "source": "reddit",
  "native_id": "t3_abc123",
  "matched_term": "Calm Vault",
  "matched_query": "\"Calm Vault\"",
  "url": "https://www.reddit.com/r/MachineLearning/comments/abc123/...",
  "title": "Calm Vault: a local credential broker for AI agents",
  "text_snippet": "First 200 chars of the body...",
  "author": "username",
  "posted_at": "1715472000.0",
  "metrics": {"score": 42, "num_comments": 7, "subreddit": "MachineLearning"},
  "sentiment": "positive",
  "topic": "technical",
  "classifier": "claude",
  "discovered_at": 1715472123.4,
  "alerts": ["first_mention"]
}
```

## State

- `sentiment_scanner/state/seen_ids.json` — dedupe set; capped at 10k ids.
- `sentiment_scanner/state/first_mention_recorded` — flag file with a unix
  timestamp; presence means `first_mention.json` has been emitted.

Delete the `state/` directory if you want to replay alerts (e.g. after a
launch-day rehearsal).

## Operational notes

- Reddit will rate-limit aggressive bots. The default 60-second interval and
  the `restrict_sr=1, sort=new, limit=25, t=week` parameters keep us well under
  the public-JSON ceiling.
- Hacker News Algolia is generous and unauthenticated.
- Google News RSS is brittle; the parser tolerates partial / broken feeds.
- The scanner never writes secrets to disk and never logs API keys.
