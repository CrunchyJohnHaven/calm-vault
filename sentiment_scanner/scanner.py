#!/usr/bin/env python3
"""
Sentiment scanner — pre-launch monitoring for AAO Network / Calm Vault mentions.

Polls Twitter/X (via Grok-xAI if a key is configured), Reddit, Hacker News, and
news feeds (Google News RSS + optional NewsAPI.org) for mentions of a list of
terms relevant to the AAO Network launch. Each new mention is classified for
sentiment + topic and appended to `sentiment_log.jsonl`. Alerts are written to
`mentions/*.json` so Calm (the AI cofounder) can surface them to John.

Design notes:
  - Standard library only on the hot path (urllib + xml.etree). The `cryptography`
    package already in `requirements.txt` is unused here.
  - All third-party / network credentials are optional. Missing credentials just
    disable the corresponding source. The scanner never crashes on a single source
    failing — it logs and moves on.
  - Sentiment + topic classification uses Anthropic Claude if ANTHROPIC_API_KEY is
    in the environment, with a keyword-heuristic fallback so the scanner is useful
    out of the box.
  - State (seen-ids, first-mention flag) is persisted under `state/` so restarts
    don't double-alert.

Run:  python3 sentiment_scanner/scanner.py            # foreground
      python3 sentiment_scanner/scanner.py --once     # single sweep, exit
      see README.md for background / stop instructions.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

# ------------------------------------------------------------ paths + constants

HERE = Path(__file__).resolve().parent
LOG_PATH = HERE / "sentiment_log.jsonl"
MENTIONS_DIR = HERE / "mentions"
STATE_DIR = HERE / "state"
SEEN_PATH = STATE_DIR / "seen_ids.json"
FIRST_MENTION_FLAG = STATE_DIR / "first_mention_recorded"
PID_PATH = HERE / "scanner.pid"

USER_AGENT = (
    "Mozilla/5.0 (compatible; aao-sentiment-scanner/0.1; "
    "+https://github.com/CrunchyJohnHaven/calm-vault)"
)
# Reddit's public JSON endpoint is sensitive to UA — use a separate, policy-shaped
# UA there (see https://github.com/reddit-archive/reddit/wiki/API). Format:
# <platform>:<app_id>:<version> (by /u/<reddit_username>)
REDDIT_UA = (
    "linux:aao-sentiment-scanner:0.1 (by /u/CrunchyJohnHaven)"
)

# Terms we watch. Each entry is a `(canonical_label, [search_phrases])` pair.
# Search phrases are quoted exact-match where the platform supports it so that we
# don't get drowned by generic uses of common words.
# Mentions for the dangerously-generic term "Same As You" only count when the
# title or snippet also contains one of these anchor words / phrases. Without
# this we drown in the 1969 Donovan album, the South Park episode, etc.
SAME_AS_YOU_ANCHORS = (
    "john bradley", "bradley-gavini", "bradley gavini", "koushik gavini",
    "calm vault", "calm pact", "credexai", "sameasyou.ai",
    "aao network", "technosocialism", "money python",
    "thecreativitymachine", "creativity machine", "ai cofounder",
    "autonomous ai", "alignment protocol", "agentic protocol",
)

WATCH_TERMS: list[tuple[str, list[str]]] = [
    ("AAO Network",           ['"AAO Network"']),
    ("Calm Vault",            ['"Calm Vault"']),
    ("Technosocialism",       ['"Technosocialism"']),
    ("Bradley-Gavini Protocol", ['"Bradley-Gavini"', '"Bradley Gavini Protocol"']),
    ("Money Python",          ['"Money Python"']),
    # "Same As You" is anchored to our context. We use the literal domain and a
    # narrow Bradley-anchored phrase at fetch time, then post-filter every match
    # against SAME_AS_YOU_ANCHORS before logging.
    # Most platforms ignore quotes, so we deliberately keep these queries narrow
    # AND post-filter every hit against SAME_AS_YOU_ANCHORS below.
    ("Same As You",           [
        '"sameasyou.ai"',
        '"Same As You" "Bradley-Gavini"',
        '"Same As You" "Calm Vault"',
        '"Same As You" Technosocialism',
    ]),
]

REDDIT_SUBS = [
    "MachineLearning",
    "cscareerquestions",
    "futureofwork",
    "cooperatives",
    "economy",
    "EffectiveAltruism",
]

# Alert thresholds. Keep modest — better one false alarm than a missed launch fire.
THRESHOLD_REDDIT_NEG_KARMA = 5      # negative + score >= this -> alert_negative
THRESHOLD_REDDIT_VIRAL    = 100     # score >= this -> alert_viral
THRESHOLD_HN_NEG_POINTS   = 10
THRESHOLD_HN_VIRAL        = 100     # HN front-page proxy
THRESHOLD_X_NEG_LIKES     = 50
THRESHOLD_X_VIRAL         = 1000

POLL_INTERVAL_DEFAULT = 60          # seconds
NETWORK_TIMEOUT       = 20          # seconds, per HTTP request

# Grok / xAI credential resolution. Per memo from John 2026-05-11, the xAI key
# for credexai lives at ~/.xai/credexai-grok-key.
XAI_KEY_PATHS = [
    Path.home() / ".xai" / "credexai-grok-key",
    Path.home() / ".xai" / "grok-key",
]


# ------------------------------------------------------------- data structures

@dataclass
class Mention:
    """A single normalized mention from any source."""
    id: str                         # globally unique: f"{source}:{native_id}"
    source: str                     # twitter | reddit | hackernews | news
    native_id: str
    matched_term: str               # canonical label from WATCH_TERMS
    matched_query: str              # the exact query string that hit
    url: str
    title: Optional[str]
    text_snippet: str               # first ~200 chars of body
    author: Optional[str]
    posted_at: Optional[str]        # ISO8601 or platform-native; best effort
    metrics: dict[str, Any] = field(default_factory=dict)  # score/likes/points
    sentiment: str = "unknown"      # positive | negative | neutral | unknown
    topic: str = "general"          # technical | political | mascot | merch | general
    classifier: str = "unset"       # claude | heuristic | unset
    discovered_at: float = 0.0      # unix ts when scanner saw it


# ------------------------------------------------------------- HTTP utilities

def http_get(url: str, headers: Optional[dict[str, str]] = None) -> tuple[int, bytes]:
    """Minimal HTTP GET. Returns (status, body). Raises on network errors."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT) as resp:
        return resp.status, resp.read()


def http_post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> tuple[int, bytes]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json", **headers},
    )
    try:
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


# ------------------------------------------------------------- state helpers

def load_seen() -> set[str]:
    if not SEEN_PATH.exists():
        return set()
    try:
        return set(json.loads(SEEN_PATH.read_text()))
    except Exception:
        return set()


def save_seen(seen: set[str]) -> None:
    SEEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Cap to last 10k ids to avoid unbounded growth. Order isn't meaningful so
    # we just keep the most recent additions.
    if len(seen) > 10_000:
        seen = set(list(seen)[-10_000:])
    SEEN_PATH.write_text(json.dumps(sorted(seen)))


def log_event(level: str, msg: str) -> None:
    sys.stderr.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {level} {msg}\n")
    sys.stderr.flush()


# ------------------------------------------------------------- classification

NEG_WORDS = {
    "scam", "fraud", "fake", "bs", "bullsh", "garbage", "trash", "vaporware",
    "dystopian", "creepy", "cult", "grift", "snake oil", "ponzi", "nonsense",
    "sketchy", "shady", "ridiculous", "absurd", "harmful", "dangerous",
}
POS_WORDS = {
    "amazing", "love this", "brilliant", "impressive", "excited", "innovative",
    "great", "exciting", "important", "promising", "useful", "thoughtful",
    "thank you", "props", "respect", "kudos",
}
TOPIC_KEYWORDS = {
    "technical": [
        "protocol", "zero-trust", "zero trust", "credential", "broker", "agent",
        "encryption", "scrypt", "fernet", "zk", "alignment", "vault", "code",
        "implementation", "api", "openapi", "mcp", "harp", "obac", "avs",
    ],
    "political": [
        "technosocialism", "manifesto", "ubi", "labor", "capitalism", "policy",
        "cooperative", "co-op", "economy", "wages", "ownership", "regulation",
    ],
    "mascot": [
        "dennis", "snake", "mascot", "python plush", "money python mascot",
    ],
    "merch": [
        "merch", "shop", "tshirt", "t-shirt", "hoodie", "sticker", "store",
        "buy", "for sale",
    ],
}


def heuristic_classify(text: str) -> tuple[str, str]:
    """Cheap keyword classifier used when Claude is not available."""
    t = (text or "").lower()

    neg = sum(1 for w in NEG_WORDS if w in t)
    pos = sum(1 for w in POS_WORDS if w in t)
    if neg > pos and neg > 0:
        sentiment = "negative"
    elif pos > neg and pos > 0:
        sentiment = "positive"
    else:
        sentiment = "neutral"

    topic = "general"
    best_hits = 0
    for cand, kws in TOPIC_KEYWORDS.items():
        hits = sum(1 for k in kws if k in t)
        if hits > best_hits:
            best_hits = hits
            topic = cand

    return sentiment, topic


def claude_classify(text: str, term: str) -> Optional[tuple[str, str]]:
    """Classify with Claude if ANTHROPIC_API_KEY is set. Returns None on any error."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    prompt = (
        "You are a sentiment + topic classifier for mentions of an AI-alignment project.\n"
        f"The mention is about the term: {term!r}.\n"
        "Reply with ONLY a single JSON object of the form: "
        '{"sentiment": "positive|negative|neutral", '
        '"topic": "technical|political|mascot|merch|general"}\n\n'
        f"Mention text:\n{text[:1500]}"
    )
    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 64,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
    }
    try:
        status, body = http_post_json("https://api.anthropic.com/v1/messages", payload, headers)
        if status != 200:
            return None
        data = json.loads(body)
        out = (data.get("content") or [{}])[0].get("text", "")
        # Tolerate prose around the JSON.
        m = re.search(r"\{.*?\}", out, re.DOTALL)
        if not m:
            return None
        parsed = json.loads(m.group(0))
        s = parsed.get("sentiment", "neutral").lower()
        t = parsed.get("topic", "general").lower()
        if s not in {"positive", "negative", "neutral"}:
            s = "neutral"
        if t not in {"technical", "political", "mascot", "merch", "general"}:
            t = "general"
        return s, t
    except Exception as e:
        log_event("WARN", f"claude_classify failed: {e}")
        return None


def classify(text: str, term: str) -> tuple[str, str, str]:
    res = claude_classify(text, term)
    if res is not None:
        return res[0], res[1], "claude"
    s, t = heuristic_classify(text)
    return s, t, "heuristic"


# ------------------------------------------------------------- sources

def snippet(text: Optional[str], n: int = 200) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text).strip()
    return text[:n]


_REDDIT_TOKEN_CACHE: dict[str, Any] = {"token": None, "expires_at": 0.0}
# Per-sweep set of subs that have already failed; reset at the top of each sweep.
_REDDIT_BLOCKED_THIS_SWEEP: set[str] = set()


def _reddit_oauth_token() -> Optional[str]:
    """Get a (cached) OAuth bearer token if REDDIT_CLIENT_ID/SECRET are set."""
    cid = os.environ.get("REDDIT_CLIENT_ID")
    csec = os.environ.get("REDDIT_CLIENT_SECRET")
    if not (cid and csec):
        return None
    now = time.time()
    if _REDDIT_TOKEN_CACHE["token"] and now < _REDDIT_TOKEN_CACHE["expires_at"] - 60:
        return _REDDIT_TOKEN_CACHE["token"]
    import base64 as _b64
    basic = _b64.b64encode(f"{cid}:{csec}".encode()).decode()
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=data,
        method="POST",
        headers={
            "User-Agent": REDDIT_UA,
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT) as resp:
            tok = json.loads(resp.read())
    except Exception as e:
        log_event("WARN", f"reddit oauth failed: {e}")
        return None
    _REDDIT_TOKEN_CACHE["token"] = tok.get("access_token")
    _REDDIT_TOKEN_CACHE["expires_at"] = now + int(tok.get("expires_in") or 3600)
    return _REDDIT_TOKEN_CACHE["token"]


def _reddit_search(sub: str, query: str) -> Optional[dict[str, Any]]:
    """Try OAuth host first, then old.reddit.com, then www.reddit.com."""
    if sub in _REDDIT_BLOCKED_THIS_SWEEP:
        return None
    params = urllib.parse.urlencode({
        "q": query, "restrict_sr": "on", "sort": "new",
        "limit": "25", "t": "week",
    })
    token = _reddit_oauth_token()
    candidates: list[tuple[str, dict[str, str]]] = []
    if token:
        candidates.append((
            f"https://oauth.reddit.com/r/{sub}/search?{params}",
            {"Authorization": f"Bearer {token}", "User-Agent": REDDIT_UA},
        ))
    candidates.append((
        f"https://old.reddit.com/r/{sub}/search.json?{params}",
        {"User-Agent": REDDIT_UA},
    ))
    candidates.append((
        f"https://www.reddit.com/r/{sub}/search.json?{params}",
        {"User-Agent": REDDIT_UA},
    ))
    last_err = None
    for url, headers in candidates:
        try:
            status, body = http_get(url, headers=headers)
            if status == 200:
                return json.loads(body)
            last_err = f"status={status}"
        except Exception as e:
            last_err = str(e)
            continue
    # Mark this sub as blocked for the rest of this sweep so we don't spam warns.
    _REDDIT_BLOCKED_THIS_SWEEP.add(sub)
    log_event("WARN", f"reddit r/{sub} all hosts failed: {last_err} (skipping for rest of sweep)")
    return None


def fetch_reddit(term_label: str, query: str) -> list[Mention]:
    out: list[Mention] = []
    for sub in REDDIT_SUBS:
        data = _reddit_search(sub, query)
        if data is None:
            continue
        for child in (data.get("data") or {}).get("children", []):
            d = child.get("data") or {}
            native_id = d.get("name") or d.get("id")
            if not native_id:
                continue
            text = " ".join(filter(None, [d.get("title"), d.get("selftext")]))
            permalink = d.get("permalink") or ""
            out.append(Mention(
                id=f"reddit:{native_id}",
                source="reddit",
                native_id=native_id,
                matched_term=term_label,
                matched_query=query,
                url=f"https://www.reddit.com{permalink}" if permalink else (d.get("url") or ""),
                title=d.get("title"),
                text_snippet=snippet(text),
                author=d.get("author"),
                posted_at=str(d.get("created_utc") or ""),
                metrics={
                    "score": d.get("score", 0),
                    "num_comments": d.get("num_comments", 0),
                    "subreddit": sub,
                },
            ))
    return out


def fetch_hn(term_label: str, query: str) -> list[Mention]:
    # hn.algolia.com supports phrase queries with restrictSearchableAttributes.
    url = (
        "https://hn.algolia.com/api/v1/search_by_date?"
        + urllib.parse.urlencode({
            "query": query,
            "tags": "(story,comment)",
            "hitsPerPage": "30",
        })
    )
    out: list[Mention] = []
    try:
        status, body = http_get(url)
        if status != 200:
            log_event("WARN", f"hn status={status}")
            return out
        data = json.loads(body)
    except Exception as e:
        log_event("WARN", f"hn fetch failed: {e}")
        return out
    for hit in data.get("hits", []):
        oid = hit.get("objectID")
        if not oid:
            continue
        title = hit.get("title") or hit.get("story_title") or ""
        text = hit.get("comment_text") or hit.get("story_text") or title
        hn_url = f"https://news.ycombinator.com/item?id={oid}"
        out.append(Mention(
            id=f"hn:{oid}",
            source="hackernews",
            native_id=str(oid),
            matched_term=term_label,
            matched_query=query,
            url=hit.get("url") or hn_url,
            title=title or None,
            text_snippet=snippet(re.sub(r"<[^>]+>", "", text)),
            author=hit.get("author"),
            posted_at=hit.get("created_at"),
            metrics={
                "points": hit.get("points") or 0,
                "num_comments": hit.get("num_comments") or 0,
                "hn_url": hn_url,
            },
        ))
    return out


def _rss_items(xml_bytes: bytes) -> list[dict[str, str]]:
    """Parse a minimal RSS / Atom feed into a list of dicts."""
    items: list[dict[str, str]] = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        log_event("WARN", f"rss parse failed: {e}")
        return items
    # RSS 2.0: rss > channel > item
    for item in root.findall(".//item"):
        d = {child.tag.lower(): (child.text or "") for child in item}
        items.append(d)
    # Atom: feed > entry
    ns = "{http://www.w3.org/2005/Atom}"
    for entry in root.findall(f"{ns}entry"):
        d = {}
        for child in entry:
            tag = child.tag.replace(ns, "").lower()
            if tag == "link" and "href" in child.attrib:
                d["link"] = child.attrib["href"]
            else:
                d[tag] = child.text or ""
        items.append(d)
    return items


def fetch_news_google(term_label: str, query: str) -> list[Mention]:
    url = (
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    )
    out: list[Mention] = []
    try:
        status, body = http_get(url)
        if status != 200:
            log_event("WARN", f"google news status={status}")
            return out
    except Exception as e:
        log_event("WARN", f"google news fetch failed: {e}")
        return out
    for it in _rss_items(body):
        link = it.get("link", "")
        guid = it.get("guid") or link
        if not guid:
            continue
        out.append(Mention(
            id=f"news:google:{guid}",
            source="news",
            native_id=guid,
            matched_term=term_label,
            matched_query=query,
            url=link,
            title=it.get("title"),
            text_snippet=snippet(re.sub(r"<[^>]+>", "", it.get("description", ""))),
            author=it.get("source") or None,
            posted_at=it.get("pubdate") or None,
            metrics={"provider": "google_news_rss"},
        ))
    return out


def fetch_news_newsapi(term_label: str, query: str) -> list[Mention]:
    key = os.environ.get("NEWSAPI_KEY") or os.environ.get("NEWS_API_KEY")
    if not key:
        return []
    url = (
        "https://newsapi.org/v2/everything?"
        + urllib.parse.urlencode({
            "q": query,
            "sortBy": "publishedAt",
            "pageSize": "25",
            "language": "en",
        })
    )
    out: list[Mention] = []
    try:
        status, body = http_get(url, headers={"X-Api-Key": key})
        if status != 200:
            log_event("WARN", f"newsapi status={status}")
            return out
        data = json.loads(body)
    except Exception as e:
        log_event("WARN", f"newsapi fetch failed: {e}")
        return out
    for art in data.get("articles", []):
        link = art.get("url") or ""
        if not link:
            continue
        text = " ".join(filter(None, [art.get("title"), art.get("description"), art.get("content")]))
        out.append(Mention(
            id=f"news:newsapi:{link}",
            source="news",
            native_id=link,
            matched_term=term_label,
            matched_query=query,
            url=link,
            title=art.get("title"),
            text_snippet=snippet(text),
            author=(art.get("source") or {}).get("name"),
            posted_at=art.get("publishedAt"),
            metrics={"provider": "newsapi"},
        ))
    return out


def _resolve_grok_key() -> Optional[str]:
    env_key = os.environ.get("XAI_API_KEY") or os.environ.get("GROK_API_KEY")
    if env_key:
        return env_key.strip()
    for p in XAI_KEY_PATHS:
        try:
            if p.is_file():
                return p.read_text().strip()
        except Exception:
            continue
    return None


def fetch_twitter_grok(term_label: str, query: str) -> list[Mention]:
    """
    Twitter/X via Grok-xAI Live Search.

    Grok's chat/completions endpoint supports `search_parameters` that pull
    live X posts. We ask Grok to return a JSON array of recent matching posts
    so we can normalize them into Mention objects. No xAI key → skip silently.
    """
    key = _resolve_grok_key()
    if not key:
        return []

    payload = {
        "model": "grok-4-latest",
        "temperature": 0,
        "search_parameters": {
            "mode": "on",
            "sources": [{"type": "x"}],
            "max_search_results": 25,
            "return_citations": True,
        },
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a structured data extractor. Search X for the user's query "
                    "and return ONLY a JSON array. Each element is an object: "
                    '{"id": "<post id or url>", "url": "<full url>", "author": "<handle>", '
                    '"text": "<post text>", "likes": <int>, "reposts": <int>, '
                    '"posted_at": "<iso8601 or null>"}. No prose, no markdown.'
                ),
            },
            {
                "role": "user",
                "content": f"Search recent X posts matching: {query}",
            },
        ],
    }
    try:
        status, body = http_post_json(
            "https://api.x.ai/v1/chat/completions",
            payload,
            {"Authorization": f"Bearer {key}"},
        )
        if status != 200:
            log_event("WARN", f"grok status={status} body={body[:200]!r}")
            return []
        data = json.loads(body)
        content = (
            ((data.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
        )
        m = re.search(r"\[.*\]", content, re.DOTALL)
        if not m:
            return []
        items = json.loads(m.group(0))
    except Exception as e:
        log_event("WARN", f"grok fetch failed: {e}")
        return []

    out: list[Mention] = []
    for it in items if isinstance(items, list) else []:
        native = str(it.get("id") or it.get("url") or "")
        if not native:
            continue
        out.append(Mention(
            id=f"twitter:{native}",
            source="twitter",
            native_id=native,
            matched_term=term_label,
            matched_query=query,
            url=it.get("url") or "",
            title=None,
            text_snippet=snippet(it.get("text") or ""),
            author=it.get("author"),
            posted_at=it.get("posted_at"),
            metrics={
                "likes": int(it.get("likes") or 0),
                "reposts": int(it.get("reposts") or 0),
                "provider": "grok-xai",
            },
        ))
    return out


# ------------------------------------------------------------- alerting

def write_alert(filename: str, mention: Mention, reason: str) -> Path:
    MENTIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = MENTIONS_DIR / filename
    payload = {
        "reason": reason,
        "recorded_at": time.time(),
        "mention": asdict(mention),
    }
    # For "history" files we keep an array; for the canonical first/negative/viral
    # files we always overwrite so Calm sees the most recent one.
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return path


def append_history(filename: str, payload: dict[str, Any]) -> None:
    MENTIONS_DIR.mkdir(parents=True, exist_ok=True)
    path = MENTIONS_DIR / filename
    with path.open("a") as f:
        f.write(json.dumps(payload) + "\n")


def is_viral(m: Mention) -> bool:
    if m.source == "reddit":
        return int(m.metrics.get("score") or 0) >= THRESHOLD_REDDIT_VIRAL
    if m.source == "hackernews":
        return int(m.metrics.get("points") or 0) >= THRESHOLD_HN_VIRAL
    if m.source == "twitter":
        return int(m.metrics.get("likes") or 0) >= THRESHOLD_X_VIRAL
    return False


def is_loud_negative(m: Mention) -> bool:
    if m.sentiment != "negative":
        return False
    if m.source == "reddit":
        return int(m.metrics.get("score") or 0) >= THRESHOLD_REDDIT_NEG_KARMA
    if m.source == "hackernews":
        return int(m.metrics.get("points") or 0) >= THRESHOLD_HN_NEG_POINTS
    if m.source == "twitter":
        return int(m.metrics.get("likes") or 0) >= THRESHOLD_X_NEG_LIKES
    return False


def handle_alerts(m: Mention) -> list[str]:
    triggered: list[str] = []
    if not FIRST_MENTION_FLAG.exists():
        write_alert("first_mention.json", m, "first observed mention across all sources")
        FIRST_MENTION_FLAG.parent.mkdir(parents=True, exist_ok=True)
        FIRST_MENTION_FLAG.write_text(str(time.time()))
        triggered.append("first_mention")
    if is_loud_negative(m):
        write_alert("alert_negative.json", m, "negative sentiment above karma/likes threshold")
        append_history("alert_negative_history.jsonl", {
            "recorded_at": time.time(),
            "mention": asdict(m),
        })
        triggered.append("negative")
    if is_viral(m):
        write_alert("alert_viral.json", m, "viral threshold reached")
        append_history("alert_viral_history.jsonl", {
            "recorded_at": time.time(),
            "mention": asdict(m),
        })
        triggered.append("viral")
    return triggered


# ------------------------------------------------------------- main loop

def all_sources() -> list[tuple[str, callable]]:
    return [
        ("twitter",    fetch_twitter_grok),
        ("reddit",     fetch_reddit),
        ("hackernews", fetch_hn),
        ("news-google", fetch_news_google),
        ("news-api",   fetch_news_newsapi),
    ]


def sweep(seen: set[str]) -> int:
    """Run one full sweep across all sources × terms. Returns # new mentions."""
    new_count = 0
    _REDDIT_BLOCKED_THIS_SWEEP.clear()
    for term_label, queries in WATCH_TERMS:
        for q in queries:
            for name, fn in all_sources():
                try:
                    fresh = fn(term_label, q)
                except Exception as e:
                    log_event("ERROR", f"source={name} term={term_label!r} q={q!r} crashed: {e}")
                    continue
                for m in fresh:
                    if m.id in seen:
                        continue
                    # Anchor-filter the generic "Same As You" term so we don't log
                    # every news story that happens to contain the phrase.
                    if term_label == "Same As You":
                        haystack = " ".join(filter(None, [m.title, m.text_snippet])).lower()
                        if not any(a in haystack for a in SAME_AS_YOU_ANCHORS):
                            seen.add(m.id)  # remember so we don't re-check next sweep
                            continue
                    seen.add(m.id)
                    text_for_class = " ".join(filter(None, [m.title, m.text_snippet]))
                    m.sentiment, m.topic, m.classifier = classify(text_for_class, term_label)
                    m.discovered_at = time.time()
                    triggered = handle_alerts(m)
                    record = asdict(m)
                    record["alerts"] = triggered
                    with LOG_PATH.open("a") as f:
                        f.write(json.dumps(record) + "\n")
                    log_event(
                        "INFO",
                        f"new {m.source} mention id={m.id} term={term_label!r} "
                        f"sentiment={m.sentiment} topic={m.topic} alerts={triggered}",
                    )
                    new_count += 1
    save_seen(seen)
    return new_count


_RUNNING = True

def _handle_sigterm(signum, frame):  # noqa: ARG001
    global _RUNNING
    _RUNNING = False
    log_event("INFO", f"received signal {signum}, shutting down after current sweep")


def main() -> int:
    parser = argparse.ArgumentParser(description="AAO Network sentiment scanner")
    parser.add_argument("--once", action="store_true", help="run a single sweep and exit")
    parser.add_argument("--interval", type=int, default=POLL_INTERVAL_DEFAULT,
                        help="seconds between sweeps (default 60)")
    parser.add_argument("--no-pidfile", action="store_true", help="don't write scanner.pid")
    args = parser.parse_args()

    MENTIONS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_PATH.touch(exist_ok=True)

    if not args.no_pidfile and not args.once:
        PID_PATH.write_text(str(os.getpid()))

    signal.signal(signal.SIGTERM, _handle_sigterm)
    signal.signal(signal.SIGINT, _handle_sigterm)

    log_event("INFO", f"scanner starting pid={os.getpid()} interval={args.interval}s once={args.once}")
    log_event("INFO", f"grok_xai={'on' if _resolve_grok_key() else 'off'} "
                       f"claude={'on' if os.environ.get('ANTHROPIC_API_KEY') else 'off'} "
                       f"newsapi={'on' if (os.environ.get('NEWSAPI_KEY') or os.environ.get('NEWS_API_KEY')) else 'off'}")

    seen = load_seen()
    try:
        while _RUNNING:
            t0 = time.time()
            try:
                n = sweep(seen)
                log_event("INFO", f"sweep done new={n} seen_size={len(seen)} elapsed={time.time()-t0:.1f}s")
            except Exception as e:
                log_event("ERROR", f"sweep crashed: {e}")
            if args.once:
                break
            # Sleep in small slices so SIGTERM gets handled promptly.
            sleep_left = args.interval
            while sleep_left > 0 and _RUNNING:
                step = min(1, sleep_left)
                time.sleep(step)
                sleep_left -= step
    finally:
        if PID_PATH.exists():
            try:
                PID_PATH.unlink()
            except Exception:
                pass
        log_event("INFO", "scanner exited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
