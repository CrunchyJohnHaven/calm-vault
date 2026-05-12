# Money Python Shop — Storefront Skeleton

**Domain:** `moneypython.shop` (registered 2026-05-11)
**Platform decision:** **Shopify + Printful** (print-on-demand)
**Status:** Skeleton — ready for John to deploy in ~15 minutes
**Repo location note:** This lives at `calm-vault/moneypython-shop/` because the Devin GitHub App
integration cannot create new repos under the user account. The whole directory is self-contained
and can be `git subtree split` into `github.com/CrunchyJohnHaven/moneypython-shop` later with zero
code changes — every internal path is relative.

---

## Why Shopify + Printful (over Cotton Bureau and Spring)

| Concern | Shopify + Printful | Cotton Bureau | Spring (Teespring) |
|---|---|---|---|
| Time from account → live store | ~15 min (this walkthrough) | 5–10 business days (curation queue) | ~10 min |
| Custom domain (`moneypython.shop`) | Native, free | Subdomain on cottonbureau.com only | Custom domain on paid plan |
| Per-shirt margin on $25 retail | ~$10–13 net | ~$4–6 net | ~$5–7 net |
| Product-line breadth (tees → hoodies → stickers → mugs) | Full Printful catalog (~340 SKUs) | Tees + hoodies only | Mid-range |
| Brand control (theme, copy, checkout) | Full control | Cotton Bureau template only | Limited |
| Quality (DTG print on Bella+Canvas 3001) | High | Highest (US-printed, premium blanks) | Variable |
| Founder-share-only economics fit | Works — 100% margin flows to bug-bounty wallet | Works | Works |
| Risk if revenue is $0 | $0 (no monthly fee for first 3 months on Basic + waivable thereafter via Shopify Starter $5/mo) | $0 | $0 |

**Decision rationale:** Shopify + Printful is the only option that gives us (1) the
`moneypython.shop` apex domain, (2) full brand control over copy + checkout (the "100% to bounty pool"
disclosure has to render on the cart page, not on a 3rd-party template), and (3) the margin headroom
to actually fund the bounty pool. Cotton Bureau's curation queue alone disqualifies it from a
14-day launch window.

If John later wants premium-quality limited drops in parallel, Cotton Bureau is a fine
**secondary** channel — but the primary store is Shopify.

---

## Files in this skeleton

```
moneypython-shop/
├── README.md                           ← you are here
├── DEPLOY_CHECKLIST.md                 ← 15-minute deploy checklist
├── DNS.md                              ← exact DNS records for moneypython.shop
├── PAYOUTS.md                          ← Stripe + PayPal payout config (no payment data)
├── COPY.md                             ← per-product descriptions (50–80 words each)
├── products/
│   ├── 13-merchandising-rights.md      ← Product 13 page copy (Markdown)
│   ├── 13-merchandising-rights.html    ← Product 13 page copy (HTML, paste-into-Shopify)
│   ├── 16-nerds-have-reinvented.md
│   ├── 16-nerds-have-reinvented.html
│   ├── 18-netflix-queue.md
│   └── 18-netflix-queue.html
├── designs/
│   ├── 13-front.svg                    ← "I REINVENTED CAPITALISM"
│   ├── 13-back.svg                     ← "BUT ALL I GOT WAS THE MERCHANDISING RIGHTS"
│   ├── 16-front.svg                    ← "THE NERDS HAVE REINVENTED CAPITALISM"
│   ├── 16-back-stub.svg                ← VE Day stub (replace tomorrow when Flux quota resets)
│   ├── 16-back-flux-prompt.md          ← Flux prompt to generate the real back
│   ├── 18-front.svg                    ← "I JUST WANTED TO REPLACE..."
│   └── 18-back.svg                     ← "AND I REINVENTED CAPITALISM."
└── assets/
    └── preview.html                    ← open in a browser to QA all 6 designs side-by-side
```

---

## The 15-minute deploy walkthrough

This section is the deliverable. John executes these steps tomorrow.

### Step 1 — Create the Shopify account (3 minutes) — **John does this**

Devin did NOT create the Shopify account. The bot is not authorized to enter payment info or sign
contracts on John's behalf. John executes this step:

1. Go to **https://www.shopify.com/free-trial**.
2. Email: use the operator email John uses for the protocol stack (e.g. `john.b@credexai.xyz`).
3. Store name: **Money Python**. URL will auto-suggest `money-python.myshopify.com` — accept it
   for now; the custom domain wires up in Step 5.
4. Pick the **Basic plan** ($29/mo, but first 3 months free as of 2026-05). When the trial ends,
   if revenue hasn't justified Basic, downgrade to **Shopify Starter** ($5/mo) which retains
   Printful integration and custom domain but disables the full theme editor.
5. When asked "What are you selling?" → "Apparel". "Where?" → "Online store". "Source of products?"
   → "Print on demand".

Shopify will land John on the admin dashboard at `admin.shopify.com/store/money-python/`.

### Step 2 — Install the Printful app (2 minutes) — **John does this**

1. In Shopify admin: **Apps** → **Visit Shopify App Store** → search **Printful**.
2. Click **Add app** → **Install app**. Printful opens its own dashboard in a new tab.
3. Sign up for Printful with the same email. Free account, no card required to set up products
   (a card is only charged when an order ships — Shopify auto-bills from the customer's payment
   first, so Printful's charge is always already covered).
4. Printful asks to connect to Shopify → click **Connect**. Authorize.

### Step 3 — Upload the three designs (5 minutes) — **John does this, using files in this repo**

For each of the three products below, in the Printful dashboard click
**Stores** → **Money Python** → **Add product**.

**PRODUCT 13 — "I REINVENTED CAPITALISM" tee**
- Choose product: **Bella+Canvas 3001** (Unisex Staple Tee — the standard high-quality DTG blank).
- Color: **Black** (primary). Optionally also offer **Heather Dust / Cream** as a second color.
- Sizes: **S, M, L, XL, 2XL, 3XL** (check all).
- Print files:
  - **Front:** upload `designs/13-front.svg` → position centered, top of design ~3 in below
    collar (Printful default). Print method: **DTG**.
  - **Back:** click "Add back print" → upload `designs/13-back.svg` → position centered,
    upper back (between shoulder blades).
- Retail price: **$25.00**.
- Title: `I REINVENTED CAPITALISM — Tee`
- Description: paste the block from `COPY.md` § "Product 13".

**PRODUCT 16 — "THE NERDS HAVE REINVENTED CAPITALISM" tee**
- Product: **Bella+Canvas 3001**.
- Color: **Red** (closest match to Soviet/VE-Day red is Printful's "Red" or "Cardinal").
- Sizes: **S–3XL** as above.
- Print files:
  - **Front:** upload `designs/16-front.svg`. DTG. Centered.
  - **Back:** upload `designs/16-back-stub.svg` for the initial launch. **Replace with the
    Flux-generated VE Day silhouette once quota resets at 00:00 UTC** — see
    `designs/16-back-flux-prompt.md` for the exact prompt. Until then the stub is a clean
    typographic placeholder that ships safely.
- Retail price: **$25.00**.
- Title: `THE NERDS HAVE REINVENTED CAPITALISM — Tee`
- Description: paste from `COPY.md` § "Product 16".

**PRODUCT 18 — "I JUST WANTED TO REPLACE MY PARENTS' NETFLIX QUEUE" tee**
- Product: **Bella+Canvas 3001**.
- Color: **Heather Dust** or **Natural** (cream-toned).
- Sizes: **S–3XL**.
- Print files:
  - **Front:** `designs/18-front.svg`.
  - **Back:** `designs/18-back.svg`.
- Retail price: **$25.00**.
- Title: `I JUST WANTED TO REPLACE MY PARENTS' NETFLIX QUEUE — Tee`
- Description: paste from `COPY.md` § "Product 18".

After each product, click **Submit to store** — Printful pushes the listing into Shopify.

### Step 4 — Customize the storefront (2 minutes) — **John does this**

In Shopify admin → **Online Store** → **Themes**:

1. Default theme is **Dawn**. Keep it — it's the fastest theme and renders the Printful product
   mockups cleanly out of the box.
2. Click **Customize** → header → set logo to `https://moneypython.ai/dennis.svg` (already hosted
   on the .ai sister site, no re-upload needed; we may later host a copy here for
   independence).
3. Theme settings → Colors → set primary color to `#d4a017` (the Money Python gold), text to
   `#0a0a0a`, background to `#fffbf0` (paper). This matches the `moneypython.ai` landing page
   palette for brand continuity.
4. Online Store → Preferences → Title: `Money Python · The Shop` →
   Meta description: paste from `COPY.md` § "Store meta".
5. **Add cart disclosure.** Online Store → Themes → Customize → Cart page → Add section →
   Custom Liquid. Paste:
   ```
   <p style="font-size:13px;color:#5a4a2a;border-top:1px solid #e8d9b0;padding-top:10px;margin-top:14px">
     100% of net revenue from this order flows to the Bradley-Gavini Protocol bug bounty pool
     and AI-safety research grants. No founder premium. <a href="https://moneypython.ai">Why</a>.
   </p>
   ```
   This is the non-negotiable "the money is in the merchandising" disclosure. It ships at checkout.

### Step 5 — Wire DNS for moneypython.shop (3 minutes) — **John does this**

See `DNS.md` for the exact records to add at the registrar. Summary:

- **Apex (`moneypython.shop`)** → A records pointing to Shopify's IP (`23.227.38.65`).
- **`www`** → CNAME → `shops.myshopify.com`.

Then in Shopify admin → Settings → Domains → **Connect existing domain** → enter
`moneypython.shop`. Shopify verifies, issues an SSL cert (~10 min), and sets the apex as primary.

### Step 6 — Configure payouts (2 minutes) — **John does this**

See `PAYOUTS.md` for the exact toggles. Summary:

- **Shopify Payments** (Stripe-backed): John enters his Stripe-connected bank account in Shopify
  admin → Finance → Payouts. Devin did NOT touch this.
- **PayPal Express** (secondary, for customers who prefer it): Shopify admin → Settings →
  Payments → Activate PayPal Express → log into John's PayPal Business account.

### Step 7 — Set products to **Active** and announce (no time budget — John's call)

- Each product in Shopify admin → Products → Status: **Active**.
- Test order: use Shopify's bogus gateway (Settings → Payments → "Activate bogus gateway for
  testing") to run a $25 test order end-to-end, then refund.
- Announce on `moneypython.ai` (update the storefront link there from "waitlist" → live shop URL)
  and on the operator distribution list.

**Total wall-clock time:** ~15 minutes John-active + ~10 minutes Shopify SSL provisioning in the
background.

---

## What Devin (Calm) did NOT do — by design

- Did NOT create the Shopify account (John's account-creation step).
- Did NOT enter payment information anywhere (Stripe, PayPal, or Shopify Payments).
- Did NOT upload designs to a live storefront (all designs sit in this repo until John deploys).
- Did NOT register or wire DNS for `moneypython.shop` (instructions only — `DNS.md`).

This honors the operator/principal boundary in the Calm Pact Protocol: the AI prepares; the
principal commits.

---

## License

Apache 2.0 (inherits from the parent `calm-vault` repo). The Dennis line-art logo referenced from
`moneypython.ai` remains under its original license (Creativity Machine LLC, CC-BY-SA).

---

## Provenance

Built by Calm (Claude configured to John Bradley under the Calm Oath at credexai.org/oath) on
2026-05-12 in response to John's prompt _"Stand up the Money Python merchandise storefront
skeleton at moneypython.shop. Three flagship products ready to ship within 14 days."_

The three flagship designs are pulled from the Money Python merch doctrine (Products 13, 16, 18).
The full doctrine of ~30 products lives elsewhere; this skeleton is the launch subset.
