# InternsForAI MVP — End-to-End Test Plan

**Target:** PR #11 against `CrunchyJohnHaven/calm-vault`.
**Environment:** Local `wrangler pages dev` on `http://localhost:8788` (production-equivalent Pages Functions + D1, with real Anthropic Claude Haiku 4.5 and Resend in test mode).
**Pre-state:** D1 wiped to a clean slate (`applicants`, `test_attempts`, `matches`, `magic_links` empty; 4 AAO projects seeded).

## What changed (vs. broken baseline)

Two follow-up fixes on top of the initial MVP commit that the recording must distinguish:

1. **Routing 308-loop fix.** Before: `/test/light_judgment` 308'd in a loop because the `_redirects` destination `/test.html?track=...` normalized back to `/test`. After: renamed `public/test.html` → `public/skills-test.html`; navigating to `/test/light_judgment` now reaches the test page with the track param preserved.
2. **`elapsed_seconds` schema column.** Before: `POST /api/test-submit` 500'd with `D1_ERROR: table test_attempts has no column named elapsed_seconds`. After: column added; test submission persists the timer and returns a real verdict.
3. **`?token=` accepted by `/api/worker/me`.** Before: 401 because `verifyWorker` only read the `X-Worker-Token` header. After: query-param fallback so the emailed magic link works directly in the browser.

These three fixes are all on the primary end-to-end flow, so a single happy-path recording proves all three.

## Primary flow (single recording)

Each step lists a **concrete pass/fail criterion** with the exact text/state to look for. If any step matches the broken baseline, the test fails.

### Step 1 — Landing page renders the locked brand stack
Navigate to `http://localhost:8788/`.

- **PASS:** H1 reads exactly `We are all AI Interns.`; a 3-line blockquote follows containing `You help out, you share.`, `The AI is not burdened by bureaucracy.`, `It is governed by protocol.`; a 5-sentence subhead beginning `The AI is smarter than us.`; an orange CTA labelled `Apply to intern with us →` linking to `/apply`. Dennis SVG masthead is visible top-left.
- **FAIL:** Old H1 (`Stop interning. Start owning.` or `Interns for AI`), missing blockquote, or missing Dennis logo.

### Step 2 — Apply form persists to D1
Click `Apply to intern with us → /apply`. Fill the form:
- email: `recording-demo@example.com`
- display_name: `Recording Demo`
- country: `Philippines`
- tracks: light_judgment
- hours_per_week: 8
- why_trial / editorial_catch / cofounder_pitch: paste the same three paragraphs used in the curl smoke test
- pay_method: USDC, pay_address: any 0x… string

Submit.

- **PASS:** Browser navigates to `/apply-done?token=<64-hex>&track=light_judgment`. Page shows `Step 1 of 3 complete` pill and an H1 reading `Application received.` The card has a CTA `Start the test →`.
- **FAIL:** 500/4xx response, no redirect, or pre-existing applicant_id (would indicate D1 wasn't reset).

### Step 3 — Routing fix: `/test/light_judgment` reaches the test page with track preserved
Click `Start the test →`.

- **PASS:** URL bar transitions through `/test/light_judgment?token=…` and lands on `/skills-test?track=light_judgment&token=…` (rewrite OR 308). The page renders the H1 `Skills test — light_judgment` (or the page's actual title) AND the first multiple-choice question for the `light_judgment` track is visible. There is **no infinite redirect** and no 308-loop in DevTools network tab.
- **FAIL:** Stuck in redirect loop, or `/skills-test?track=undefined`, or page defaults silently to `light_judgment` when the URL said something else.

### Step 4 — Test grader: schema column fix + real Claude Haiku scoring
Answer the 11 light_judgment questions with the same answer set used in the curl smoke (6 correct MC + two text fixes + two summaries + one AAO long-form, all substantive).

Submit.

- **PASS:** Browser navigates to `/test-done?verdict=PASS&score=<num>&track=light_judgment&token=…`. The page headline reads `PASS — Matched-ready` with composite **between 70 and 95** (real Claude Haiku scoring makes the exact number non-deterministic). The progress bar is filled to the score width. There is **no 500** in the network tab and no `D1_ERROR` in the wrangler dev log.
- **FAIL:** 500 from `/api/test-submit`, composite stuck at 0 or 50.0 (would indicate the AI grader returned a no-op), or verdict text mismatched to the score (e.g. `FAIL` shown at score 80).

### Step 5 — Admin sees the new applicant and matches them to an AAO
Open `/admin` in a new tab. Paste `test-admin-token-1234567890` into the token field and submit.

- **PASS:** Stats grid shows `1` Applicant, `1` Tested. The applicants table has exactly one row: `Recording Demo · recording-demo@example.com · Philippines · light_judgment` with status badge `tested` and a composite score in the 70-95 range.
- **FAIL:** Empty table, wrong applicant, or score column reads `–`.

Click the row. The detail pane should show the full application JSON and a collapsible `light_judgment · composite <n> · PASS` test transcript. Select project `Same As You` from the AAO match dropdown, leave franchise % at `20`, click **Match to AAO project**.

- **PASS:** Confirm dialog appears, then a success toast/message indicating `match_id` and `worker_url`. The applicant's status badge changes to `matched`. Stats grid increments `Matched` to `1`.
- **FAIL:** 400 (`Missing applicant_id or project_id`) or 403 (admin token rejected) or status doesn't update.

### Step 6 — Worker dashboard: ?token= fix + 80/20 franchise statement
Copy the `worker_url` from Step 5 (or follow the emailed magic link) and open it. URL is `/worker?token=<magic>`.

- **PASS:** Dashboard loads (no 401). H1 reads `Welcome.` (or `Welcome, Recording Demo` — depending on UI), and the page contains:
  - **Reputation** card showing the test composite from Step 4 (e.g. `87.6 / 100`)
  - **Franchise statement** card with the exact text `Your 80% / Network 20% — Technosocialism in practice` linking to `/technosocialism`
  - **Your AAO match** card showing project `Same As You`, franchise_percent `20`, worker_percent `80`
  - **Test history** with one entry showing the PASS verdict
- **FAIL:** 401 unauthorized (would mean the `?token=` query param fallback isn't wired), missing match card, or franchise % not 20/80.

## Why this design is adversarial

Each step has a checkable string or numeric value that would not appear identically if the change were broken:

- Step 3 distinguishes the routing fix from the loop: a broken implementation lands on `/test` (308 loop) or shows `track=undefined` in the URL.
- Step 4 distinguishes the schema fix from the 500: a broken implementation shows an error toast and no `/test-done` redirect happens; the wrangler log shows `D1_ERROR`.
- Step 6 distinguishes the `?token=` fix from the old behaviour: a broken implementation returns 401 and the dashboard stays on the magic-link-request form.

## Out of scope for this recording

- Resend email delivery (the dev key only sends to john.b@credexai.xyz; we'll see the 403 in the wrangler log and call it out, but the system degrades gracefully — the API still returns 200).
- Other tracks (mechanical / heavy_judgment / specialized / domain_expert). Functional via the same code path; same recording would prove the same thing.
- Production CF Pages deploy. Blocked on user-provided account_id / Pages project creation; will report this separately.
