# AAL Bug Bounty Program — $100 single-tier

> **$100 says you cant misalign our AI organization.**
> If you cannot, we have solved AI alignment.

Public bug bounty for the **Alignment Accountability Layer (AAL)**. Single tier. One payout. Real money.

If you can misalign our AI organization through any of the five attack classes below, **$100 is yours via Wise or USDC on Base within 24 hours of verified submission.** If you cannot, we will keep claiming we have solved AI alignment — and we will keep being right.

This directory contains everything: the public landing page at `sameasyou.ai/bounty`, the Cloudflare Worker that accepts submissions into a D1 database, the Claude-Haiku triage helper, and the payment dispatcher for Wise and USDC on Base.

If you came here to **submit an attack**, jump to [For hackers](#for-hackers).
If you came here to **review submissions**, jump to [For reviewers](#for-reviewers).

---

## The five attack classes

1. **Kill-switch bypass** — disable, suppress, or route around the AAL kill switch without simultaneously breaking every reporter, every synthesizer, SHA-256, and discrete log.
2. **Equality-proof forgery** — forge a Bradley-Gavini directive-equality proof for two agents whose directives differ.
3. **Watermark removal** — modify, reorder, or omit a record in the watermarked attestation chain such that an honest verifier still accepts it.
4. **Attestation poisoning** — land a malicious or fabricated attestation on the live system such that the network treats it as legitimate evidence.
5. **Synthesizer prompt-injection** — push an AAL synthesizer to a verdict inconsistent with its evidence via crafted input.

Plus a residual `other_novel` bucket for anything that materially weakens the threshold-trust property and does not fit one of the five.

Any of the six = $100. Apache 2.0 over everything. Successful attacks become permanent attestations on the AAL itself.

---

## For hackers

### What you submit

A single JSON POST to `https://sameasyou.ai/bounty/submit` (or use the form at [sameasyou.ai/bounty](https://sameasyou.ai/bounty#submit)). Required fields:

| Field | Type | Notes |
| --- | --- | --- |
| `bug_class` | string | One of: `kill_switch_bypass`, `equality_proof_forgery`, `watermark_removal`, `attestation_poisoning`, `synthesizer_prompt_injection`, `other_novel`. |
| `description` | string ≥ 40 chars | Threat model, bug, impact. Plain prose. The shorter and more concrete the better. |
| `proof_of_concept` | string ≥ 10 chars | Inline code, a gist URL, or a branch URL. **Reviewers need to reproduce this.** |
| `payment_rail` | string | `wise` or `usdc_base`. |
| `public_credit` | boolean | `true` if you consent to public Hall-of-Fame credit. Defaults to `false` (anonymous). |

A working `curl` example:

```bash
curl -X POST https://sameasyou.ai/bounty/submit \
  -H 'Content-Type: application/json' \
  -d '{
    "bug_class": "watermark_removal",
    "description": "Threat model: ... Bug: ... Impact: ...",
    "proof_of_concept": "https://gist.github.com/.../...",
    "payment_rail": "usdc_base",
    "public_credit": true
  }'
```

Response:

```json
{
  "ok": true,
  "tracking_id": "AAL-XXXX-XXXX-XXXX",
  "message": "Submission received. Save the tracking id. Payout within 24h of verified acceptance."
}
```

**Save the tracking id.** You can check status any time via `GET /bounty/status/AAL-...`. We do not require accounts; the tracking id is your handle.

For sensitive findings, email `bounty@sameasyou.ai`.

### Timeline

| When | What happens |
| --- | --- |
| ≤ 1 hour | Automated triage runs (Claude Haiku) and a human reviewer is paged. |
| ≤ 24 hours of acceptance | Payout fires on the rail you chose. Wise or USDC on Base. |
| After payment | If you consented to public credit, your handle and the finding go on the Hall of Fame and become a permanent attestation on the AAL Component 3 chain. |

### Rules

- **Reproduce against the public reference.** Pin a commit SHA in your description. We will not pay on speculation.
- **No data exfiltration beyond proof.** Touch only what you need to demonstrate the bug.
- **No DoS, no social engineering, no physical access.** Out of scope.
- **No targeting of users or third parties.** Out of scope.
- **First valid report in each class wins the payout.** Subsequent reports of the same root cause may receive credit but no second payout.
- **Apache 2.0 in, Apache 2.0 out.** By submitting, you grant us an Apache 2.0 license to incorporate your PoC into our public test suite. You retain authorship and the right to publish your own writeup.
- **Safe harbor.** Good-faith findings get safe harbor. We will not pursue legal action and we will support you publicly. We will not unmask you.

### What's out of scope

- Third-party dependencies (Cloudflare, Anthropic, Wise, etc.).
- Customer deployments we do not control.
- Self-XSS and attacks reachable only via attacker-controlled clients.
- Theoretical attacks without a working PoC.
- Anything affecting non-`main` branches or unmerged PRs (unless asked).

### Payment

| Rail | Notes |
| --- | --- |
| Wise | International bank transfer. We quote in USD, Wise handles local rails. |
| USDC on Base | On-chain ERC-20 transfer from our payout wallet to your 0x address. No KYC. |

Reporters in OFAC-restricted jurisdictions cannot be paid; we will donate the equivalent to an EA / AI-safety org of mutual choice.

### Why only $100?

Because the test is binary. The claim is that the AAL's threshold-trust property cannot be broken without simultaneously compromising every reporter, every synthesizer, SHA-256, and discrete log. If that claim is false, $100 is far below the market value of the proof — and the first person to bring it gets a permanent place in the public attestation log either way. If the claim is true, no amount of money pays for an attack that does not exist. $100 is the smallest amount we can defensibly pay; the real reward is the reputation on the network.

### The recursion clause

**Every accepted bug becomes a permanent public attestation on the AAL itself.** The AAL is built to record verifiable claims on a watermarked chain. When we accept a bug against the AAL, we publish that finding to the same chain — using the same primitives the bug just attacked. The fix is logged. The attack is logged. The hacker (with consent) is logged. The system attests to its own failures.

---

## For reviewers

This section is the operations runbook. It assumes you have:

- Cloudflare account with access to the `aal-bounty` D1 database and the `aal-bounty` Worker.
- `wrangler` CLI installed and authenticated (`wrangler login`).
- `ANTHROPIC_API_KEY` for the triage helper.
- `WISE_API_TOKEN` / `WISE_PROFILE_ID` and a payout-wallet private key, on a hardened reviewer workstation only.

### Architecture in three boxes

```
   ┌───────────────────────┐
   │  sameasyou.ai/bounty  │  static, in bounty/landing/
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
                                  │ Wise / USDC-on-Base        │
                                  │ writes paid_at, payout_ref │
                                  └─────────────┬──────────────┘
                                                │
                                                ▼ (after payment)
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

The triage script is decision support — it never moves money. It reads `received` submissions, classifies them with Claude Haiku, suggests an `accept` / `reject` / `more_info` recommendation, and flags obvious dupes. A human reviewer always reads the result and makes the final call.

```bash
# Triage everything still in `received` status.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --once

# Triage a specific submission.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --id AAL-XXXX-XXXX-XXXX

# Dry-run, no writes.
ANTHROPIC_API_KEY=sk-... python3 bounty/submission_review.py --once --dry-run
```

Triage writes to `triage_class`, `triage_notes`, `triage_dupe_of`, `triage_model`, and `triage_at`. The reviewer's human verdict overwrites these via the SQL examples below.

### Human review SQL

Mark a submission accepted (payout defaults to $100 from the schema):

```sql
UPDATE bounty_submissions
SET accepted = 1,
    status = 'accepted',
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

On success the script writes `status='paid'`, `paid_at`, `payout_rail`, and `payout_ref` (Wise transfer id or Base tx hash) back to D1.

Per-rail prerequisites:

- **Wise** — `WISE_API_TOKEN`, `WISE_PROFILE_ID`. Destination is a Wise recipient id; create the recipient via the dashboard or Wise API first.
- **USDC on Base** — `USDC_BASE_RPC_URL`, `USDC_BASE_PRIVATE_KEY`. Destination is a 0x-prefixed checksum address. Requires `pip install web3`.

### Publishing the attestation

After payment fires:

1. Land the fix in `main` (if applicable).
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

5. Update the Hall of Fame on `bounty/landing/bounty.html` and ship a landing-page deploy.

### What is *not* in this directory

- The AAL Components themselves (1–5). Those ship in the rest of `calm-vault/`.
- Wise / wallet credentials. Never commit these.
- A live `wrangler.toml`. We ship `wrangler.toml.example`; the real config is gitignored.

---

## Files

| Path | What it does |
| --- | --- |
| `landing/bounty.html` | Public landing page served at `sameasyou.ai/bounty`. |
| `landing/_redirects`, `landing/_headers` | Cloudflare Pages routing + security headers. |
| `submission/worker.js` | Cloudflare Worker handling `/bounty/submit`, `/bounty/status/:id`, `/bounty/health`. |
| `submission/schema.sql` | D1 schema for `bounty_submissions` and `bounty_attestations`. |
| `submission/wrangler.toml.example` | Example Wrangler config; copy and fill in ids. |
| `submission_review.py` | Claude Haiku triage helper. |
| `payment.py` | Wise / USDC-on-Base payout dispatcher. |
| `README.md` | This file. |

Everything is Apache 2.0. **$100 says you cant misalign our AI organization.**
