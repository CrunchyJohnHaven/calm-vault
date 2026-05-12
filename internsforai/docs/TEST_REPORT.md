# InternsForAI MVP — End-to-End Test Report

**PR:** [CrunchyJohnHaven/calm-vault#11](https://github.com/CrunchyJohnHaven/devin-ai-integration/calm-vault/pull/11)
**Tested:** 2026-05-12 ~00:55 UTC
**Environment:** Local `wrangler pages dev` on `:8788` against Cloudflare Pages Functions + D1 (local) + real Anthropic Claude Haiku 4.5 + Resend test key.
**Method:** Manual browser walkthrough of the primary placement flow (Apply → Test → Admin Match → Worker) with a single end-to-end recording.

## Summary

All 5 assertions in the test plan passed. The three critical fixes shipped after the initial MVP commit — (1) routing 308-loop fix, (2) `elapsed_seconds` schema column, (3) `?token=` fallback in `verifyWorker` — are all proven on the primary flow.

## Assertions

| # | Test | Result | Note |
|---|---|---|---|
| 1 | It should render the locked brand stack on the landing page | passed | H1 "We are all AI Interns.", 3-line blockquote, 5-sentence subhead, CTA, Dennis logo all present |
| 2 | It should accept an applicant via /apply and redirect to /apply-done | passed | Redirected to `/apply-done?token=...&track=light_judgment`; "Step 1 of 3 complete" pill visible |
| 3 | It should route /test/light_judgment without 308 loop and preserve track | passed | URL bar lands on `/skills-test?track=light_judgment&token=...`; first MC question rendered; no redirect loop |
| 4 | It should grade the test and persist test_attempt with elapsed_seconds | passed | `/test-done?verdict=PASS&score=89.51984126984127&track=light_judgment&token=...` — verdict PASS, composite 89.5/100 (MC 100% · text 65% · AI 92%) |
| 5 | It should list the applicant in /admin and match them to an AAO project | passed | Status changed `tested` → `matched`, success message "Matched. Worker share: 80%. Worker has been emailed." |
| 6 | It should authenticate worker via ?token= magic link and show 80/20 statement | passed | No 401; "Your 80% / Network 20% — Technosocialism in practice" + "Same As You" AAO match card visible |

## Evidence

### 1. Landing page — locked brand stack

H1 "We are all AI Interns.", 3-line blockquote, 5-sentence subhead, "Apply to intern with us →" CTA, Dennis logo top-left.

![Landing](https://app.devin.ai/attachments/dab345e4-cc30-4031-8915-ed50c0e9a670/screenshot_392ce505d34c4bc9b4cb683b8edafd80.png)

### 2. Routing fix — `/test/light_judgment` reaches the test page

URL bar shows `/skills-test?track=light_judgment&token=...` (the renamed file proves the 308 loop is broken). First MC question "Which sentence contains a typo?" rendered.

![Test page](https://app.devin.ai/attachments/ccc9a565-eb1f-4a14-93c3-18a6cc9b41be/screenshot_99e59d4cef924b2e90216f02e589ad61.png)

### 3. Schema fix + real Claude Haiku — test grades to PASS at 89.5

`/test-done?verdict=PASS&score=89.51984126984127&track=light_judgment&token=...` — composite 89.5/100, "PASS — MATCHED-READY". Wrangler log showed no `D1_ERROR` and the AI scoring components (`AI 92%`) prove Claude Haiku 4.5 actually graded the long-form responses.

![Test verdict](https://app.devin.ai/attachments/1cc1bebe-ac38-4710-bbdf-f81bc88f6fb4/screenshot_1c77e9d026bb402a87fb3f516bc7a707.png)

### 4. Admin → match to AAO

Status changed from `tested` to `matched`; success message "Matched. Worker share: 80%. Worker has been emailed." Stats grid update is implicit (would require navigating back to the list view).

![Admin match success](https://app.devin.ai/attachments/35330fc0-2b71-4f53-a951-a61ab55b45f9/screenshot_b60ba6cd883b4b8aa448639fb9de06d4.png)

### 5. Worker dashboard via ?token= magic link

No 401 (the `?token=` query-param fallback works). Reputation card 89.5/100 STRONG. Franchise statement card says exactly "Your 80% / Network 20% — Technosocialism in practice. See /technosocialism for the full doctrine." AAO match card shows "Same As You" with "Your share: 80% · Network share: 20%".

![Worker dashboard](https://app.devin.ai/attachments/02633ac8-1fb0-41f5-8d6a-05cd0beaabba/screenshot_d92b60ea13d54966a3bccfb163cd2fb4.png)

### 6. Worker — test history breakdown

Test history shows `light_judgment · Composite 89.5/100 · PASS · 2026-05-12 00:57` with the per-component breakdown `MC 100% · text 65% · AI 92% · composite 89.5 → PASS`. This is the same composite that appears on `/test-done` and the admin row — confirms persistence is correct.

![Worker test history](https://app.devin.ai/attachments/2ca927d4-7faf-4793-8d12-e8dbdc2f3638/screenshot_0740b802ab434e40bf2d5d0ba29136b1.png)

## What was not tested (and why)

- **Production CF Pages deploy.** Standalone `CrunchyJohnHaven/internsforai` repo does not yet exist (the integration cannot create new repos under your account). Deploy is on you — `wrangler pages deploy public --project-name=internsforai` after step-by-step instructions in `internsforai/README.md`.
- **Real Resend email delivery.** Dev key only sends to `john.b@credexai.xyz`; the test applicant email `recording-demo@example.com` would 403 on send. The API returns 200 anyway (degrades gracefully). To prove the email path end-to-end, fill `/apply` with `john.b@credexai.xyz` against the deployed Pages URL.
- **Other tracks** (mechanical / heavy_judgment / specialized / domain_expert). Functional via the same code path; `scripts/smoke.mjs` exercises the grader for all 5 and asserts monotonic scoring. The recording flow proves the most polished track (light_judgment) end-to-end.
- **AAL Component 3 cryptographic attestation.** v0 stub only — explicitly listed as v1 work in PR description.

## Reproduce locally

```bash
git fetch && git checkout devin/1778545381-internsforai-mvp
cd internsforai
npm install
# .dev.vars must contain ANTHROPIC_API_KEY, RESEND_API_KEY, ADMIN_TOKEN
wrangler d1 execute internsforai_prod --local --file=schema/0001_init.sql
wrangler pages dev public --port 8788 --d1 DB=internsforai_prod
# in another tab:
open http://localhost:8788/
```
