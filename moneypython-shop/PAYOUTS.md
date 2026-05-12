# Payouts — Stripe + PayPal + (optional) crypto

**Devin (Calm) did NOT enter any payment information.** This document is instructions for John.

## The economics

Money Python operates on the operator-share-only doctrine:

- **Net revenue** (revenue − Printful cost − Shopify fees − payment processor fees) flows to the
  Bradley-Gavini Protocol bug bounty pool and AI-safety research grants.
- **Founder premium:** zero. John takes operator share only, which for the storefront is
  effectively the time John spends operating it (≈ minimum wage equivalent, capped at
  $X/month — see the Calm Pact Protocol economics doc).
- **Cost stack on a $25 tee** (representative — actual depends on Printful's quote at order time):
  - Retail: $25.00
  - Printful production + shipping: ~$11–13
  - Shopify Payments / Stripe fee: 2.9% + $0.30 = ~$1.03
  - **Net to bounty pool: ~$10–13 per tee**

## Step 1 — Shopify Payments (Stripe-backed, primary)

In Shopify admin → **Settings → Payments → Activate Shopify Payments**:

1. Business type: **Sole proprietor** or **Single-member LLC**, whichever entity John holds the
   shop under. (If unsure, sole proprietor is fine for launch; can convert later.)
2. EIN / SSN: John enters.
3. Bank account: John enters routing + account.
4. Statement descriptor: `MONEYPYTHON*SHOP` (helps customers recognize the charge).
5. Payout schedule: **Daily** (default) or weekly. Daily is fine for low volume.

Shopify Payments uses Stripe under the hood — no separate Stripe account needed for the
common case. If John wants a separate Stripe account (e.g., to connect to the same Stripe org as
other CredexAI projects), use **Settings → Payments → Add payment method → Stripe** instead of
Shopify Payments.

## Step 2 — PayPal Express (secondary)

About 15–25% of shoppers prefer PayPal. Add it:

1. Settings → Payments → **PayPal** → Activate.
2. Sign in with John's **PayPal Business** account (not personal — personal accounts can't accept
   commercial transactions above a low threshold).
3. Currency: USD.
4. Done. Shopify and PayPal handle the rest.

## Step 3 — (Optional) Coinbase Commerce for crypto

If John wants the bounty pool to receive crypto directly without conversion:

1. Settings → Payments → **Add payment method** → Coinbase Commerce (third-party gateway).
2. Sign in / sign up at commerce.coinbase.com.
3. Connect a wallet (Coinbase, Metamask, hardware — Coinbase Commerce supports many).
4. Activate in Shopify.

This is optional; skip for launch and add later if there's demand.

## Step 4 — Auto-route net revenue to the bounty pool

The bounty pool wallet address lives in `calm_pact/economics/bounty_pool_wallet.md` (or wherever
John has it documented — Devin did not look up the wallet address). To auto-route:

**Option A (simplest):** Manual monthly transfer. John reconciles Shopify payouts vs. Printful
charges + Shopify fees at end of month, transfers net to the bounty pool wallet, logs the transfer
in the public ledger.

**Option B (automated):** Shopify Flow + a webhook to the credex-treasury endpoint
(if it exists) — `Settings → Notifications → Webhooks → Order paid`. On each paid order,
fire a webhook to a treasury endpoint that holds the net amount in escrow and sweeps to the
bounty pool wallet weekly. This is out of scope for the launch skeleton; build it once volume
justifies it.

For launch: **Option A** is fine.

## Step 5 — Tax setup (US, basic)

1. Shopify admin → **Settings → Taxes and duties**.
2. United States → **Manage** → add the states where John has nexus (at minimum, John's home
   state). For a brand-new store with no other nexus, this is just one state.
3. Shopify Tax (free under $100k revenue/year) auto-calculates sales tax for that state.

Printful handles its own production-side sales tax in the states where it has a printing facility
— this is invisible to the customer.

## Step 6 — Refunds policy

- **Defective / wrong item shipped:** Printful reprints at no cost. Customer keeps the original
  (Printful's policy). Shopify admin → Orders → Refund → Issue refund or replacement.
- **Buyer's remorse:** Money Python's policy (set this in Shopify → Settings → Policies →
  Refund policy) is **no refunds for opened/worn merchandise** but **size exchange within 30 days
  at customer's cost.** This protects margin (and therefore the bounty pool) while staying
  consumer-friendly.

Sample refund policy text is in `COPY.md` § "Policies".

## What John needs to have on hand

- [ ] EIN (or SSN for sole prop)
- [ ] Business legal name + address
- [ ] Bank routing + account number
- [ ] PayPal Business login
- [ ] (Optional) Coinbase Commerce account
- [ ] (Optional) Bounty pool wallet address for routing

## What Devin will never touch

- Any of the above. Payment information stays exclusively in John's hands. The Calm Pact Protocol
  forbids the AI from taking custody of operator funds; this is a hard rule, not a guideline.
