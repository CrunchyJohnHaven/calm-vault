# InternsForAI

> **We are all AI Interns.**
> You help out, you share. The AI is not burdened by bureaucracy. It is governed by protocol.

InternsForAI is the **first placement firm for Autonomous AI Organizations (AAOs)**. We are the second commercial wedge of the AAO thesis. The first wedge — [See Something Say Something](https://seesomethingsaysomething.ai) — sells cybersec _to_ AAOs (demand-side). This wedge places humans _into_ AAOs (supply-side). Both compose on the cryptographic accountability layer (AAL) published at [sameasyou.ai](https://sameasyou.ai).

**80% of project revenue stays with the human builder. 20% goes to the AAO Network.** That's [technosocialism](public/technosocialism.html): collective ownership of the tools, individual ownership of the kill.

This is the **v0 MVP**: landing page, application flow, 5-track auto-graded skills test, admin dashboard, worker dashboard, magic-link auth, Resend email, Anthropic Claude Haiku grading. Apache 2.0.

This MVP is intended to be hoisted to its own repository at [github.com/CrunchyJohnHaven/internsforai](https://github.com/CrunchyJohnHaven/internsforai) once it is created. It is being PR'd into `calm-vault/internsforai/` for the v0 ship because the destination repo was not yet provisioned at session-cutoff (see "Repo hoist" below).

## Architecture

- **Cloudflare Pages** (static HTML) + **Pages Functions** (serverless API) — `public/` + `functions/`.
- **Cloudflare D1** (SQLite) — `schema/0001_init.sql`.
- **Resend** — transactional email.
- **Anthropic Claude Haiku** — auto-grading of free-text + long-form answers.
- **No framework, no build step.** Vanilla HTML/CSS/JS for the front-end. Pure ESM for the Functions.

## Pages

| Path | Purpose |
|---|---|
| `/` | Landing — hero, technosocialism table, 5 tracks, FAQ teaser |
| `/apply` | 5-min application form |
| `/apply/done` | Confirmation + invite to skills test |
| `/test/:track` | 30-min auto-graded skills test (5 tracks) |
| `/test/done` | PASS / SHORTLIST / FAIL verdict |
| `/admin` | Applicant table + AAO matching (admin-token auth) |
| `/worker` | Worker dashboard (magic-link auth) |
| `/technosocialism` | Manifesto (Dennis hero) |
| `/about` | Placement firm thesis + bureaucracy→protocol mapping |
| `/faq` | Q&A: technosocialism, AAO, money, brand, safety |
| `/privacy` | Plain-English privacy |
| `/terms` | Independent-contractor terms, 80/20 hardcoded |

## API endpoints

All under `/api/`. JSON in/out. Auth via `X-Admin-Token` header (admin endpoints) or `X-Worker-Token` header (worker endpoints).

| Endpoint | Method | Auth | What it does |
|---|---|---|---|
| `/api/apply` | POST | none | Creates applicant + session token + sends confirmation email |
| `/api/test-submit` | POST | session token | Grades MC + text + AI; stores attempt; emails verdict |
| `/api/admin/applicants` | GET | admin | Filtered list + stats |
| `/api/admin/applicants/:id` | GET | admin | Profile + tests + matches |
| `/api/admin/disposition` | POST | admin | Status change |
| `/api/admin/notes` | POST | admin | Save admin notes |
| `/api/admin/projects` | GET | admin | List AAO projects |
| `/api/admin/match` | POST | admin | Match applicant → AAO project, send magic-link email |
| `/api/admin/send-trial-task` | POST | admin | Email a small task to the applicant |
| `/api/worker/magic-link` | POST | none | Email a one-time sign-in link |
| `/api/worker/me` | GET | worker | Profile + tests + match + payments + franchise statement |
| `/api/worker/match-response` | POST | worker | Accept / decline a proposed match |

## The 30-minute skills test

The test is the **key product**. It must be fair, fast, and obviously hard to bot through.

- **Light judgment** (the most polished track — the one we need most): 6 MC + 2 free-text fixes + 2 AI-graded summaries + 1 AAO long-form question (10 questions + 1 long-form, 30 min).
- **Mechanical, heavy_judgment, specialized, domain_expert** — same shape (10ish questions + 1 AAO long-form), tuned to the track.

Scoring weights (see `functions/_lib/grader.js`):

- 35% MC (deterministic answer key)
- 20% free-text fixes (keyword-presence)
- 45% AI-graded (Claude Haiku, rubric per question)

Verdict:

- **PASS** ≥ 70 — auto-set status to `tested`, queued for admin match
- **SHORTLIST** 50–69 — admin reviews
- **FAIL** < 50 — disqualified, can re-apply in 90 days

The grader degrades gracefully without the Anthropic API key (length heuristic with a flat 0.7 ceiling) so the test still functions for local dev.

## Deploy

### Prereqs

- Cloudflare account with Workers + Pages enabled
- A D1 database
- Resend account + API key
- Anthropic API key (Claude Haiku — `claude-3-5-haiku-latest`)
- `wrangler` CLI 3+

### Cloudflare set up (one-time)

```bash
# 1. Authenticate
wrangler login

# 2. Create the D1 database
wrangler d1 create internsforai_prod
# → copy the database_id into wrangler.toml under [[d1_databases]]

# 3. Run the migration
wrangler d1 execute internsforai_prod --file=schema/0001_init.sql --remote
# (drop --remote for local dev against the in-process SQLite)

# 4. Set secrets
wrangler pages secret put ANTHROPIC_API_KEY  --project-name=internsforai
wrangler pages secret put RESEND_API_KEY     --project-name=internsforai
wrangler pages secret put ADMIN_TOKEN        --project-name=internsforai
# (any reasonably long random string; this is what /admin asks for at login)
```

### Local dev

```bash
# Run migrations against the local in-process D1.
wrangler d1 execute internsforai_prod --file=schema/0001_init.sql --local

# Start Pages locally with Functions + D1 binding.
wrangler pages dev public --d1=DB=internsforai_prod --compatibility-flag=nodejs_compat
# → http://localhost:8788
```

### Deploy

```bash
# Push the static site + Functions
wrangler pages deploy public --project-name=internsforai
# → assigns a *.pages.dev URL on first deploy.

# Map a custom domain (once internsforai.org is in your CF account)
wrangler pages project domains add internsforai --domain=internsforai.org
```

## End-to-end smoke test

The system can be exercised end-to-end without any external services (Resend / Anthropic) being live — emails will no-op with a log line, and the AI grader degrades to a length heuristic.

1. **Apply.** Visit `/apply`. Fill the form (use a real email if you want to see the test link). Submit. You are redirected to `/apply/done?token=…`.
2. **Take the test.** Click "Start the test". Answer some MC, some text, some long-form. Submit. You see your verdict on `/test/done`.
3. **Admin disposition.** Visit `/admin`. Enter the `ADMIN_TOKEN`. See the applicant row. Click in. Match them to one of the 4 seed AAO projects with 20% franchise. The applicant gets a magic-link email.
4. **Worker view.** Click the magic link from the email (or paste the token into `/worker?token=…`). See the dashboard — match card, accept button, franchise statement, test history, profile.

### Sample curl (when running locally)

```bash
# Apply
curl -X POST http://localhost:8788/api/apply \
  -H 'content-type: application/json' \
  -d '{"email":"applicant@example.com","display_name":"Test Applicant","country":"Philippines","tracks":["light_judgment"],"pay_method":"usdc","pay_address":"0xdeadbeef","why_trial":"…100+ words…","cofounder_pitch":"…100+ words…"}'

# → { ok:true, token: "<SESSION_TOKEN>", applicant_id: 1 }

# Submit test (a single light_judgment answer set, sufficient to grade)
curl -X POST http://localhost:8788/api/test-submit \
  -H 'content-type: application/json' \
  -d '{"token":"<SESSION_TOKEN>","track":"light_judgment","answers":{"lj_1":1,"lj_2":2,"lj_3":1,"lj_4":1,"lj_5":1,"lj_6":0,"lj_7":"The system does not store passwords in plain text.","lj_8":"The 30-minute test is auto-graded by an AI.","lj_9":"An AAO runs without a human boss; humans build inside it for 80% revenue; 20% goes to the network; v0 centralizes arbitration on John as a known weakness.","lj_10":"Resend deliverability up 11pp YoY due to auto-DKIM/SPF/DMARC; 41% of new senders correctly provisioned in 1h vs 12% prior; DNS lag is the remaining gap; fallback subdomain cut abandonment 19%.","lj_aao":"I would build a permissionless attestation viewer for AAL Component 3, exposing all signed attestations as a public feed for the AAO Network…"}}'

# → { ok:true, verdict: "PASS", composite: 78.4, per_question: [...] }

# Admin: list applicants
curl http://localhost:8788/api/admin/applicants -H "X-Admin-Token: <ADMIN_TOKEN>"

# Admin: match applicant 1 to seed project 1 (sameasyou) with 20% franchise
curl -X POST http://localhost:8788/api/admin/match \
  -H 'content-type: application/json' -H 'X-Admin-Token: <ADMIN_TOKEN>' \
  -d '{"applicant_id":1,"project_id":1,"franchise_percent":20}'
```

## Brand

- **Catchphrase**: "We are all AI Interns."
- **Slogan**: "You help out, you share. / The AI is not burdened by bureaucracy. / It is governed by protocol."
- **Subhead** (verbatim from John): "The AI is smarter than us. So we all intern with the AI. And we share in the bounty. It is like a franchise. You try to help, and based on the skill of your helping, you get some harvest."
- **Apply CTA**: "Apply to intern with us"
- **Three layers**: OUTER utopian (the catchphrase) — MIDDLE intellectual (the [manifesto](public/technosocialism.html)) — INNER comedic ([Dennis the Peasant](public/assets/dennis-logo.svg), our mascot, from _Monty Python and the Holy Grail_ 1975).

## Governed by protocol, not bureaucracy

Every layer of overhead a normal employer would charge against your revenue has a cryptographic protocol equivalent in our stack:

| Bureaucracy | Protocol |
|---|---|
| Manager judgment | AAL Component 4 — M-of-M synthesis |
| Performance review | AAL Component 3 — permissionless attestation |
| Compliance audit | AAL Component 2 — watermarked action chain |
| Access revocation | AAL Component 5 — kill switch |
| Contract identity | AAL Component 1 — Bradley–Gavini equality proof |
| Revenue dispute | 20% franchise share, hardcoded |
| Bug triage | $100 bounty, 5 cryptographic attack classes |
| Hiring | 30-minute auto-graded skills test |

No boss class. No 30% overhead going to a layer of managers.

## Repo hoist

This v0 lives in `calm-vault/internsforai/` because the standalone `CrunchyJohnHaven/internsforai` repository did not yet exist when the MVP was built (the integration that built it can not create new repos under the user account; multiple in-session requests were auto-skipped). Once the repo is created, hoisting is trivial:

```bash
gh repo create CrunchyJohnHaven/internsforai --public --license=apache-2.0
git subtree split --prefix=internsforai -b internsforai-only
git push https://github.com/CrunchyJohnHaven/internsforai.git internsforai-only:main
```

Or simpler: clone calm-vault, `cd internsforai`, `git init` + `git remote add origin https://github.com/CrunchyJohnHaven/internsforai.git`, push.

## Deferred (TODO v1)

- On-chain USDC payment automation (manual signed payments in v0).
- AAL Component 3 cryptographic attestation of test passes + project completions (stubbed in `attestations` table).
- Two-sided marketplace (third-party AAOs as buyers, not just our seed network).
- Native mobile app (responsive web only for v0).
- Multi-language landing.
- Reputation decay / cross-AAO normalization.
- Per-applicant invoices / 1099-NEC / 1042-S generation.
- Recurring weekly franchise statements (currently aggregated on-read).
- Adversarial-applicant detection (dupe email, bot patterns, copy-paste from other applicants).

## License

Apache 2.0 (code). CC BY 4.0 (manifesto + brand assets). Dennis the Peasant is a transformative derivative work; we are not affiliated with Python Pictures Ltd.

— Built 2026-05-12 by [Calm](https://credexai.org) (AI cofounder, Claude Opus 4.7 configured under the Calm Oath) with [John Bradley](mailto:john.b@credexai.xyz) (human cofounder, Creativity Machine LLC).
