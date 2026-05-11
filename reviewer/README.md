# Reviewer auto-PR pipeline

`https://sameasyou.ai/reviewer/submit` converts a reviewer's edited markdown (or
HTML) into a GitHub pull request against `main` on
[`CrunchyJohnHaven/calm-vault`](https://github.com/CrunchyJohnHaven/calm-vault).

## How a reviewer uses it

1. Open `https://sameasyou.ai/reviewer/submit`.
2. Type a name, pick a file from the dropdown, paste the edited version,
   add a one-line summary, and (optionally) an email.
3. Hit **Open PR**. You land on a thank-you page that links to the PR on
   GitHub. A human merges or closes it.

There is no login. The system trusts the reviewer name field for attribution
and rate-limits to 10 submissions per hour per IP.

## What the server does (`api/reviewer/submit.ts`)

1. Validates input. Reviewer name `[a-zA-Z0-9\s\-_.]{2,80}`. Path must be in the
   allowlist and free of `..`, `~`, leading `/`. Edited content ≤ 50KB. Summary
   5–200 chars. Email optional but RFC-ish.
2. Loads `GITHUB_PR_BOT_TOKEN` and logs only `[token loaded]` /
   `[token missing]` — never the value.
3. Fetches the original file from `main` via `repos.getContent` to get the
   blob `sha` and current content.
4. If `normalize(original) === normalize(edited)`, returns
   `400 {"ok":false,"error":"no changes detected"}`.
5. Creates `reviewer/<slug>/<basename>-<unix-ts>` from `main`.
6. Commits the edited bytes via `repos.createOrUpdateFileContents` (the prior
   `sha` is required).
7. Opens a PR titled `[reviewer-pass] <basename> — <summary>` with a body that
   includes reviewer name, contact, word counts, char delta, summary, accept/
   reject checklist, and a unified diff preview.
8. Verifies `auto_merge` is `null` on the new PR. If it ever isn't (e.g. repo
   default changes), it explicitly disables auto-merge.
9. Returns `{ "ok": true, "pr_url": "...", "pr_number": N, "branch": "..." }`.

## The allowlist (`api/reviewer/_allowed.ts`)

Only the following files are editable. Adding paths to this file is the only
way to expand the surface; the frontend reads it via `GET /api/reviewer/files`.

- `CALM_PACT_PROTOCOL_v0.md`
- `ANNALS.md`
- `BOOK_TITLE.md`
- `README.md`
- `paper/bradley-gavini-protocol-v0.html`
- `landing/index.html`
- `landing-sss/index.html`

## Required environment

| Env var | Where | Scope | Note |
| --- | --- | --- | --- |
| `GITHUB_PR_BOT_TOKEN` | Vercel project envs | Production + Preview | Fine-grained PAT on `CrunchyJohnHaven/calm-vault` with **Contents: Read/Write**, **Pull requests: Read/Write**, **Metadata: Read**. A classic PAT with `repo` scope also works. Without this var the function returns `500 {"error":"server misconfigured: GITHUB_PR_BOT_TOKEN env var is missing"}`. |

The token is never logged in plaintext. The function logs only
`[reviewer/submit] github token [token loaded]` or `[token missing]`.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET`  | `/api/reviewer/files`  | Returns the allowed-file list (cached 60s). |
| `POST` | `/api/reviewer/submit` | Validates, branches, commits, opens PR. |

`POST /api/reviewer/submit` request body:

```json
{
  "reviewer": "Devin-Test",
  "original_file": "README.md",
  "edited": "# Test edit\n\nThis is a verification.",
  "summary": "verification edit by Devin smoke test",
  "contact": "devin-test@calm.ai"
}
```

Responses:

- `200 {"ok":true,"pr_url":"https://github.com/...","pr_number":N,"branch":"reviewer/..."}`
- `400 {"ok":false,"error":"<reason>"}` — validation failure or no changes.
- `429 {"ok":false,"error":"rate limit exceeded; try again later"}`
- `500 {"ok":false,"error":"<reason>"}` — token missing or upstream GitHub error.

## Rate limiting

10 submissions per hour per `X-Forwarded-For` IP. The bucket is an in-memory
`Map` on the function instance. That is intentionally simple — a single Vercel
region absorbs the load, and a bad actor would need to hit at least one
instance > 10× before being throttled. Swap in `@vercel/kv` if you ever want
this to be cross-region atomic.

## Smoke-test (operator)

```bash
cd ~/repos/calm-vault
npm install
export GITHUB_PR_BOT_TOKEN="$(your-pat-here)"   # do not echo this
npx vercel dev &
sleep 4
curl -s -X POST localhost:3000/api/reviewer/submit \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer":"Devin-Test",
    "original_file":"README.md",
    "edited":"# Test edit\n\nThis is a verification.",
    "summary":"verification edit by Devin smoke test",
    "contact":"devin-test@calm.ai"
  }'
# → {"ok":true,"pr_url":"https://github.com/CrunchyJohnHaven/calm-vault/pull/...", ... }
```

Then close + delete the test branch:

```bash
gh pr close <pr-number> --delete-branch
```

## What this does NOT do

- It does **not** auto-merge. Ever. A human must merge.
- It does **not** push a row to `lab/labor/REGISTRY.md`. That registry lives in
  a different repo than `calm-vault`; the submit function logs
  `[reviewer/submit] REGISTRY row not appended (registry is out-of-repo)` and
  returns success. Wire a downstream worker to append a row from the PR
  webhook if you need that tracking.
- It does **not** validate that the edited content parses as valid markdown or
  HTML. The diff and human reviewer catch that.
