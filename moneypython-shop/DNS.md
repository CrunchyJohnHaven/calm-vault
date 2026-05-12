# DNS wiring — moneypython.shop → Shopify

`moneypython.shop` was registered by John on 2026-05-11 at his usual registrar (Namecheap,
Cloudflare, or similar). The records below are registrar-agnostic — copy them into the registrar's
DNS panel exactly as written.

## Required records

| Type | Host | Value | TTL |
|---|---|---|---|
| A | `@` (apex / root) | `23.227.38.65` | Automatic / 3600 |
| CNAME | `www` | `shops.myshopify.com` | Automatic / 3600 |

**That's it.** Shopify uses a single IP (`23.227.38.65`) for all storefronts; the customer-facing
edge handles SNI-based routing to your specific store. The `www` CNAME flattens to that same edge.

## If the registrar is Cloudflare

1. Log into Cloudflare → select `moneypython.shop` zone.
2. DNS → Records → Add record:
   - Type **A**, Name `@`, IPv4 `23.227.38.65`, **Proxy status: DNS only** (gray cloud — Shopify
     will issue its own SSL cert, do not proxy through Cloudflare or you'll get a cert mismatch).
   - Type **CNAME**, Name `www`, Target `shops.myshopify.com`, **Proxy status: DNS only**.
3. Save.

## If the registrar is Namecheap

1. Domain List → `moneypython.shop` → Manage → Advanced DNS.
2. Add new record:
   - Type **A Record**, Host `@`, Value `23.227.38.65`, TTL Automatic.
   - Type **CNAME Record**, Host `www`, Value `shops.myshopify.com.`, TTL Automatic.
3. Remove any default parking records (the Namecheap parking page CNAME, if present).
4. Save (green check).

## If the registrar is Google Domains / Squarespace Domains

1. DNS → Default name servers → Custom records.
2. Add:
   - `@` / A / `23.227.38.65` / 1H
   - `www` / CNAME / `shops.myshopify.com` / 1H

## Verifying

After saving, in a terminal:

```bash
dig +short A moneypython.shop          # expect: 23.227.38.65
dig +short CNAME www.moneypython.shop  # expect: shops.myshopify.com.
```

Then in Shopify admin: **Settings → Domains → Connect existing domain** → enter
`moneypython.shop` → click **Verify connection**. Shopify will:

1. Confirm DNS is correct.
2. Issue a Let's Encrypt SSL cert (takes 5–15 minutes).
3. Set `moneypython.shop` as the **primary domain** (so the canonical URL is
   `https://moneypython.shop`, not `money-python.myshopify.com`).

Confirm the green padlock on `https://moneypython.shop` before announcing.

## SEO redirects

In Shopify admin → Settings → Domains, make sure all three resolve to the same canonical:

- `moneypython.shop` → primary
- `www.moneypython.shop` → redirect to primary
- `money-python.myshopify.com` → redirect to primary

Shopify handles all three automatically once the custom domain is set as primary.

## Email (optional, do later)

If John wants `hello@moneypython.shop` mail routing, add either:

- **Google Workspace** MX records (see workspace.google.com/dns); or
- **Cloudflare Email Routing** (free, forwards to John's existing inbox).

This is not required for launch. The Shopify order-notification emails go out from
`@notifications.shopify.com` by default.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Shopify says "DNS not configured" after 1 hour | TTL too long, propagation delay | Wait, or lower TTL to 300s and retry |
| Browser shows cert mismatch | Cloudflare proxy is ON (orange cloud) | Set proxy to DNS only (gray cloud) |
| `www.moneypython.shop` 404s | CNAME pointed to wrong target | Confirm CNAME points to `shops.myshopify.com.` (with trailing dot in some panels) |
| Apex resolves but SSL never provisions | CAA records blocking Let's Encrypt | Remove restrictive CAA records or add `letsencrypt.org` to the allowlist |
