# Money Python Shop — 15-Minute Deploy Checklist

Print this. Tick the boxes. Skip nothing.

## Pre-flight (do this once, never again)
- [ ] Decide on shipping country: store currency = **USD**, ships **worldwide via Printful**.
- [ ] Have on hand: John's Stripe-connected bank routing/account numbers, PayPal Business login,
      registrar login for `moneypython.shop`.

## Step 1 — Shopify account (3 min)
- [ ] Go to https://www.shopify.com/free-trial
- [ ] Sign up with `john.b@credexai.xyz`
- [ ] Store name: `Money Python` → URL: `money-python.myshopify.com`
- [ ] Plan: Basic ($29/mo, first 3 months free) or Starter ($5/mo) if revenue is unproven
- [ ] What are you selling? → "Apparel" / Where? → "Online store" / Source → "Print on demand"

## Step 2 — Printful (2 min)
- [ ] Shopify admin → Apps → Shopify App Store → search "Printful" → Add app → Install
- [ ] Sign up for Printful with same email
- [ ] Authorize the Shopify ↔ Printful connection

## Step 3 — Upload the 3 designs (5 min)

### Product 13 — "I REINVENTED CAPITALISM"
- [ ] Printful → Add product → Bella+Canvas 3001 → Black → Sizes S–3XL
- [ ] Front: upload `designs/13-front.svg` (DTG, centered, default vertical)
- [ ] Back: upload `designs/13-back.svg` (DTG, centered, upper back)
- [ ] Retail price: $25.00
- [ ] Title: `I REINVENTED CAPITALISM — Tee`
- [ ] Description: paste `COPY.md` § Product 13
- [ ] Submit to store

### Product 16 — "THE NERDS HAVE REINVENTED CAPITALISM"
- [ ] Printful → Add product → Bella+Canvas 3001 → Red → Sizes S–3XL
- [ ] Front: upload `designs/16-front.svg`
- [ ] Back: upload `designs/16-back-stub.svg` (replace later with Flux-generated VE Day silhouette;
      see `designs/16-back-flux-prompt.md`)
- [ ] Retail price: $25.00
- [ ] Title: `THE NERDS HAVE REINVENTED CAPITALISM — Tee`
- [ ] Description: paste `COPY.md` § Product 16
- [ ] Submit to store

### Product 18 — "I JUST WANTED TO REPLACE MY PARENTS' NETFLIX QUEUE"
- [ ] Printful → Add product → Bella+Canvas 3001 → Heather Dust or Natural → Sizes S–3XL
- [ ] Front: upload `designs/18-front.svg`
- [ ] Back: upload `designs/18-back.svg`
- [ ] Retail price: $25.00
- [ ] Title: `I JUST WANTED TO REPLACE MY PARENTS' NETFLIX QUEUE — Tee`
- [ ] Description: paste `COPY.md` § Product 18
- [ ] Submit to store

## Step 4 — Theme & cart disclosure (2 min)
- [ ] Shopify admin → Online Store → Themes → Dawn → Customize
- [ ] Header logo → `https://moneypython.ai/dennis.svg`
- [ ] Colors: `#d4a017` gold, `#0a0a0a` ink, `#fffbf0` paper
- [ ] Online Store → Preferences → Title: `Money Python · The Shop`, meta from `COPY.md`
- [ ] Cart page → Add section → Custom Liquid → paste the bounty-pool disclosure from `README.md`
      Step 4 § Add cart disclosure

## Step 5 — DNS (3 min)
- [ ] At the registrar where `moneypython.shop` is registered, set the records from `DNS.md`:
  - [ ] A `@` → `23.227.38.65` (Shopify)
  - [ ] CNAME `www` → `shops.myshopify.com`
- [ ] Shopify admin → Settings → Domains → Connect existing domain → `moneypython.shop`
- [ ] Wait ~10 min for SSL provisioning. Confirm green padlock on `https://moneypython.shop`.

## Step 6 — Payouts (2 min)
- [ ] Shopify admin → Finance → Payouts → activate Shopify Payments → enter Stripe-linked bank info
- [ ] Settings → Payments → Activate PayPal Express → sign in to PayPal Business
- [ ] (Optional but recommended) Settings → Payments → Manual payment → add "Crypto via Coinbase
      Commerce" if John wants crypto payouts feeding the bounty pool directly

## Step 7 — Test order & go live
- [ ] Settings → Payments → Activate bogus gateway → place $25 test order → refund
- [ ] Each product → Status → **Active**
- [ ] Update `moneypython.ai/merch.html` → swap waitlist CTA for direct link to `moneypython.shop`
- [ ] Announce on operator distribution list

## Done.

Net revenue from each order auto-flows per `PAYOUTS.md` to the bounty pool wallet. Founder takes
zero. The money is in the merchandising.
