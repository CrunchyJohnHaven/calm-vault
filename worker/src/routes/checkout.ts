// GET /checkout/pro  — 302 redirect to the Stripe Payment Link for the Pro tier.
//
// The user wants one canonical $49/mo product. We keep that as a Stripe-hosted
// Payment Link (configured in STRIPE_PRO_PAYMENT_LINK) so we don't fragment the
// checkout surface. Optionally we pass `client_reference_id` (the customer id,
// when an api_key query parameter is supplied) so we can reconcile the Stripe
// session to a customer row after they pay.

import type { Env } from "../env";
import { apiKeyHash } from "../lib/api_key";
import { CORS_HEADERS } from "../lib/http";

export async function handleCheckoutPro(
  request: Request,
  env: Env,
): Promise<Response> {
  const target = new URL(env.STRIPE_PRO_PAYMENT_LINK);
  const url = new URL(request.url);
  const apiKey = url.searchParams.get("api_key");
  if (apiKey && /^[0-9a-fA-F]{32}$/.test(apiKey)) {
    const hash = await apiKeyHash(apiKey.toLowerCase());
    const row = await env.DB.prepare(
      "SELECT id, email FROM customers WHERE api_key_hash = ?",
    )
      .bind(hash)
      .first<{ id: string; email: string }>();
    if (row) {
      target.searchParams.set("client_reference_id", row.id);
      target.searchParams.set("prefilled_email", row.email);
    }
  }
  return new Response(null, {
    status: 302,
    headers: { Location: target.toString(), ...CORS_HEADERS },
  });
}
