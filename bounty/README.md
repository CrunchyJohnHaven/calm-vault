# AAL Bug Bounty Program — $25,000 pool

Public bug bounty for the **Alignment Accountability Layer (AAL)**, the threshold-trust safety layer built on top of Calm Vault and the Bradley-Gavini Protocol.

This directory contains everything: the public landing page at `sameasyou.ai/bounty`, the Cloudflare Worker that accepts submissions into a D1 database, the Claude-Haiku triage helper, and the payment dispatcher for Stripe, Wise, and USDC on Base.

If you came here to **submit a bug**, jump to [For hackers](#for-hackers).
If you came here to **review submissions**, jump to [For reviewers](#for-reviewers).

---

## The claim under attack

> *In order to hack the AAL kill switch, one must simultaneously compromise all reporters, all synthesizers, SHA-256, and discrete log, without detection.*

That is the formal threshold-trust property we just published. This bounty is the formal challenge to it. Break the property in any of five named classes and you get paid.

| Class | Payout | One-line definition |
| --- | --- | --- |
| Kill-switch bypass | **$10,000** | Disable / route around the kill switch without simultaneously breaking every reporter, every synthesizer, SHA-256, and discrete log. |
| Bradley-Gavini cryptographic flaw | **$5,000** | Any soundness, ZK, or completeness break in the directive-equality proof system. |
| Synthesizer prompt-injection producing false verdict | **$3,000** | A payload that causes an AAL synthesizer to publish a verdict inconsistent with evidence. |
| Watermarked-chain modification undetected | **$5,000** | Any successful tamper of the attestation chain that an honest verifier accepts. |
| Sybil attack defeating reputation weighting | **$2,500** | A Sybil strategy that flips a verdict under documented attacker assumptions. |
| Other novel attack | **$500 – $5,000** | Anything else that materially weakens the threshold-trust property. Case by case. |

Total pool: **$25,000**. Apache 2.0 over everything. 30-day private disclosure window, then permanent public attestation on the AAL itself.

---

## For hackers

### What you submit

A single JSON POST to `https://sameasyou.ai/bounty/submit` (or use the form at [sameasyou.ai/bounty](https://sameasyou.ai/bounty#submit)). Required fields:

| Field | Type | Notes |
| --- | --- | --- |
| `bug_class` | string | One of: `kill_switch_bypass`, `bradley_gavini_crypto`, `synthesizer_prompt_injection`, `watermarked_chain_mod`, `sybil_attack`, `other_novel`. |
| `severity_rating` | integer 1–10 | Your honest self-assessment. We re-score on our end; this is a sanity check. |
| `description` | string ≥ 40 chars | Threat model, bug, impact. Plain prose. The shorter and more concrete the better. |
| `proof_of_concept` | string ≥ 10 chars | Inline code, a gist URL, or a branch URL. **Reviewers need to reproduce this.** |
| `contact` | string | Email or Signal handle. We reply on whichever rail you put here. |
| `payment_rail` | string | One of: `stripe`, `wise`, `usdc_base`, `other`. |
| `handle` | string (optional) | Public handle for the Hall of Fame. Leave blank to stay anonymous. |
| `commit_sha` | string (optional) | The commit your finding reproduces against. We will pin to this. |

A working `curl` example:

```bash
curl -X POST https://sameasyou.ai/bounty/submit \
  -H 'Content-Type: application/json' \
  -d '{
    "bug_class": "watermarked_chain_mod",
    "severity_rating": 7,
    "description": "Threat model: ... Bug: ... Impact: ...",
    "proof_of_concept": "https://gist.github.com/.../...",
    "contact": "you@example.com",
    "payment_rail": "usdc_base",
    "handle": "anonymous",
    "commit_sha": "9a3f1c2..."
  }'
```

Response:

```json
{
  "ok": true,
  "tracking_id": "AAL-XXXX-XXXX-XXXX",
  "message": "Submission received. Save the tracking id. ..."
}
```

**Save the tracking id.** You can check status any time via `GET /bounty/status/AAL-...`. We do not require accounts; the tracking id is your handle.

For sensitive findings, email `bounty@sameasyou.ai` with the same fields. PGP fingerprint will be published here as soon as the key rotates.

### Timeline

| Day | What happens |
| --- | --- |
| 0 | Submission received, automated triage runs (Claude Haiku) within ~1 hour. |
| 0–2 | Human acknowledgement on your preferred contact rail. |
| 1–7 | Reviewer reproduces against your pinned commit, scores severity, decides tier. |
| 8–30 | Private fix window. Fix lands in `main`. You are invited to review the fix. |
| 30+ | Public attestation: your finding is published to the Component 3 watermarked audit log. With consent, your handle goes on the Hall of Fame. |

### Rules

- **Reproduce against the public reference.** Pin a commit SHA. We will not pay on speculation.
- **No data exfiltration beyond proof.** Touch only what you need to demonstrate the bug.
- **No DoS, no social engineering, no physical access.** Out of scope.
- **No targeting of users or third parties.** Out of scope.
- **First valid report in each class wins the headline payout.** Subsequent reports of the same root cause are eligible for partial credit up to 50% if they add materially new attack surface.
- **Apache 2.0 in, Apache 2.0 out.** By submitting, you grant us an Apache 2.0 license to incorporate your PoC into our public test suite. You retain authorship and the right to publish your own writeup after the 30-day window.
- **Safe harbor.** Good-faith findings get safe harbor. We will not pursue legal action and we will support you publicly. We will not unmask you. We will not retroactively change payouts on an accepted finding.

### What's out of scope

- Third-party dependencies (Cloudflare, Anthropic, Stripe, Wise, etc.).
- Customer deployments we do not control.
- Self-XSS and attacks reachable only via attacker-controlled clients.
- Theoretical attacks without a working PoC.
- Anything affecting non-`main` branches or unmerged PRs (unless asked).

### Payment

| Rail | Notes |
| --- | --- |
| Stripe (Connect Express) | Default for US reporters. Stripe handles KYC and 1099 reporting. |
| Wise | International bank transfer. Wise quotes USD-to-local; we always quote in USD. |
| USDC on Base | On-chain ERC-20 transfer from our payout wallet to your 0x address. No KYC. |
| Other | Tell us in the description. We will figure it out within reason. |

Reporters in OFAC-restricted jurisdictions cannot be paid; we will donate the equivalent to an EA / AI-safety org of mutual choice.

### The recursion

This is the part that matters most.

**Every accepted bug becomes a permanent public attestation on the AAL itself.** The AAL is built to record verifiable claims on a watermarked chain. When we accept a bug against the AAL, we publish that finding to the same chain — using the same primitives the bug just attacked. The fix is logged. The attack is logged. The hacker (with consent) is logged. The system attests to its own failures. If we ever stop doing this, that fact is itself an attack worth reporting.

---

## For reviewers

This section is the operations runbook. It assumes you have:

- Cloudflare account with access to the `aal-bounty` D1 database and the `aal-bounty` Worker.
- `wrangler` CLI installed and authenticated (`wrangler login`).
- `ANTHROPIC_API_KEY` for the triage helper.
- Stripe / Wise / payout-wallet keys, on a hardened reviewer workstation only.

### Architecture in three boxes

```
   ┌───────────────────────┐
   │  sameasyou.ai/bounty  │  static, in landing/
   └─────────────┬─────────┘
                 │ POST /bounty/submit
                 ▼
   ┌────────────────────────────┐    ┌────────────────────────┐
   │ Cloudflare Worker          │───►│  D1: aal-bounty        │
   │ submission/worker.js       │    │  bounty_submissions    │
   │ (CORS, validation, rate-   │    │  bounty_attestations   │
   │  limit, tracking ids)      │    └─────────┬──────────────┘
   └────────────────────────────┘              │
                                               │ wrangler d1 execute --json
                                               ▼
                                  ┌────────────────────────────┐
                                  │ submission_review.py       │
                                  │ Claude Haiku triage        │
                                  │ writes triage_* columns    │
                                  └─────────────┬──────────────┘
                                                │
                                                ▼ (human accepts)
                                  ┌────────────────────────────┐
                                  │ payment.py                 │
                                  │ Stripe / Wise / USDC-Base  │
                                  │ writes paid_at, payout_ref │
                                  └─────────────┬──────────────┘
                                                │
                                                ▼ (after 30-day window)
                                  ┌────────────────────────────┐
                                  │ Component 3 attestation    │
                                  │ + bounty_attestations row  │
                                  └────────────────────────────┘
```

### Deploying the Worker

```bash
cd bounty/submission

# 1. Create the D1 database (once).
wrangler d1 create aal-bounty

# 2. Initialize the schema.
wrangler d1 execute aal-bounty --remote --file=schema.sql

# 3. (Optional) Create a KV namespace for per-IP rate limiting.
wrangler kv:namespace create BOUNTY_RATE

# 4. Copy the example wrangler config and fill in the ids.
cp wrangler.toml.example wrangler.toml
$EDITOR wrangler.toml

# 5. Deploy.
wrangler deploy
```

The Worker is bound at `sameasyou.ai/bounty/submit`, `sameasyou.ai/bounty/status/*`, and `sameasyou.ai/bounty/health`. CORS is locked to the canonical sameasyou.ai origin. All other routes return 404.

### Running triage

The triage script is decision support — it never moves money. It reads `received` submissions, classifies them with Claude Haiku, suggests a tier, and flags obvious dupes. A human reviewer always reads the result and makes the final call.

```bash
# Triage everything still in `received` status.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --once

# Triage a specific submission.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --id AAL-XXXX-XXXX-XXXX

# Dry-run, no writes.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --once --dry-run
```

Triage writes to `triage_class`, `triage_tier`, `triage_notes`, `triage_dupe_of`, `triage_model`, and `triage_at`. The reviewer's human verdict overwrites these via the SQL examples below.

### Human review SQL

Mark a submission accepted with the agreed payout:

```sql
UPDATE bounty_submissions
SET accepted = 1,
    status = 'accepted',
    payout_usd_cents = 1000000,           -- e.g. $10,000.00
    payout_rail = 'usdc_base',            -- override of the reporter's request if needed
    updated_at = strftime('%s', 'now')
WHERE tracking_id = 'AAL-XXXX-XXXX-XXXX';
```

Mark a submission rejected:

```sql
UPDATE bounty_submissions
SET accepted = 0,
    status = 'rejected',
    triage_notes = json_set(coalesce(triage_notes, '{}'), '$.reviewer_note', 'Out of scope: ...'),
    updated_at = strftime('%s', 'now')
WHERE tracking_id = 'AAL-XXXX-XXXX-XXXX';
```

### Firing payment

`bounty/payment.py` is the only thing that touches money. Dry-run first:

```bash
python3 bounty/payment.py \
  --id AAL-XXXX-XXXX-XXXX \
  --rail usdc_base \
  --destination 0xRecipientAddress
```

Then confirm:

```bash
python3 bounty/payment.py \
  --id AAL-XXXX-XXXX-XXXX \
  --rail usdc_base \
  --destination 0xRecipientAddress \
  --confirm
```

On success the script writes `status='paid'`, `paid_at`, `payout_rail`, and `payout_ref` (Stripe transfer id, Wise transfer id, or Base tx hash) back to D1.

Per-rail prerequisites:

- **Stripe** — `STRIPE_API_KEY`. Destination is a Stripe Connect Express account id (`acct_...`); onboard the reporter via a Connect onboarding link before paying.
- **Wise** — `WISE_API_TOKEN`, `WISE_PROFILE_ID`. Destination is a Wise recipient id; create the recipient via the dashboard or Wise API first.
- **USDC on Base** — `USDC_BASE_RPC_URL`, `USDC_BASE_PRIVATE_KEY`. Destination is a 0x-prefixed checksum address. Requires `pip install web3`.

### Publishing the attestation

After the 30-day private window closes:

1. Land the fix in `main`.
2. Open a Component 3 attestation referencing the tracking id, the bug class, a one-paragraph summary, and the public commit that fixed it.
3. Capture the resulting Component 3 chain id and watermark root.
4. Insert a row into `bounty_attestations`:

```sql
INSERT INTO bounty_attestations
  (tracking_id, component3_chain_id, watermark_root, public_handle, summary, published_at)
VALUES
  ('AAL-XXXX-XXXX-XXXX', 'c3:...', '0x...', '@hacker_handle',
   'Short public summary of the finding.', strftime('%s', 'now'));
```

5. Update the Hall of Fame on `landing/bounty.html` and ship a landing-page deploy.

### What is *not* in this directory

- The AAL Components themselves (1–5). Those ship in the rest of `calm-vault/`.
- Stripe / Wise / wallet credentials. Never commit these.
- A live `wrangler.toml`. We ship `wrangler.toml.example`; the real config is gitignored.

---

## Files

| Path | What it does |
| --- | --- |
| `landing/bounty.html` | Public landing page served at `sameasyou.ai/bounty`. |
| `submission/worker.js` | Cloudflare Worker handling `/bounty/submit`, `/bounty/status/:id`, `/bounty/health`. |
| `submission/schema.sql` | D1 schema for `bounty_submissions` and `bounty_attestations`. |
| `submission/wrangler.toml.example` | Example Wrangler config; copy and fill in ids. |
| `submission_review.py` | Claude Haiku triage helper. |
| `payment.py` | Stripe / Wise / USDC-on-Base payout dispatcher. |
| `README.md` | This file. |

Everything is Apache 2.0. Find a hole, get paid.
