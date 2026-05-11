// POST /stripe/webhook
//
// Receives Stripe events. On `checkout.session.completed` we flip the matching
// customer's tier to 'pro' and record their stripe customer + subscription ids.
// On `customer.subscription.deleted` we revert to 'free'.
//
// Event idempotency is enforced via the `stripe_events` table.

import type { Env } from "../env";
import { jsonResponse } from "../lib/http";
import { verifyStripeSignature } from "../lib/stripe";

interface StripeEvent {
  id: string;
  type: string;
  data: { object: Record<string, unknown> };
}

export async function handleStripeWebhook(
  request: Request,
  env: Env,
): Promise<Response> {
  const raw = await request.text();
  const sigHeader = request.headers.get("stripe-signature");
  const secret = env.STRIPE_WEBHOOK_SECRET ?? "";
  const verified = await verifyStripeSignature(raw, sigHeader, secret);
  if (!verified.ok) {
    return jsonResponse(
      { error: { code: "invalid_signature", message: verified.reason ?? "verification failed" } },
      400,
    );
  }

  let event: StripeEvent;
  try {
    event = JSON.parse(raw) as StripeEvent;
  } catch {
    return jsonResponse(
      { error: { code: "invalid_json", message: "payload is not valid JSON" } },
      400,
    );
  }

  // Idempotency: ignore if we've seen this event id before.
  const already = await env.DB.prepare(
    "SELECT id FROM stripe_events WHERE id = ?",
  )
    .bind(event.id)
    .first<{ id: string }>();
  if (already) {
    return jsonResponse({ ok: true, idempotent_replay: true });
  }

  const now = Math.floor(Date.now() / 1000);
  let customerId: string | null = null;

  if (event.type === "checkout.session.completed") {
    const obj = event.data.object as {
      client_reference_id?: string | null;
      customer?: string | null;
      customer_email?: string | null;
      subscription?: string | null;
    };
    customerId =
      (await resolveCustomerId(env, {
        client_reference_id: obj.client_reference_id ?? null,
        customer_email: obj.customer_email ?? null,
      })) ?? null;
    if (customerId) {
      await env.DB.prepare(
        `UPDATE customers
           SET tier = 'pro', pro_since = COALESCE(pro_since, ?),
               stripe_customer_id = COALESCE(?, stripe_customer_id),
               stripe_subscription_id = COALESCE(?, stripe_subscription_id)
         WHERE id = ?`,
      )
        .bind(now, obj.customer ?? null, obj.subscription ?? null, customerId)
        .run();
    }
  } else if (event.type === "customer.subscription.deleted") {
    const obj = event.data.object as { customer?: string | null };
    if (obj.customer) {
      const row = await env.DB.prepare(
        "SELECT id FROM customers WHERE stripe_customer_id = ?",
      )
        .bind(obj.customer)
        .first<{ id: string }>();
      if (row) {
        customerId = row.id;
        await env.DB.prepare(
          "UPDATE customers SET tier = 'free', stripe_subscription_id = NULL WHERE id = ?",
        )
          .bind(row.id)
          .run();
      }
    }
  }

  await env.DB.prepare(
    `INSERT INTO stripe_events (id, event_type, customer_id, payload, received_at)
     VALUES (?, ?, ?, ?, ?)`,
  )
    .bind(event.id, event.type, customerId, raw, now)
    .run();

  return jsonResponse({ ok: true, processed: event.type, customer_id: customerId });
}

async function resolveCustomerId(
  env: Env,
  hints: { client_reference_id: string | null; customer_email: string | null },
): Promise<string | null> {
  if (hints.client_reference_id) {
    const row = await env.DB.prepare(
      "SELECT id FROM customers WHERE id = ?",
    )
      .bind(hints.client_reference_id)
      .first<{ id: string }>();
    if (row) return row.id;
  }
  if (hints.customer_email) {
    const row = await env.DB.prepare(
      "SELECT id FROM customers WHERE email = ?",
    )
      .bind(hints.customer_email.toLowerCase())
      .first<{ id: string }>();
    if (row) return row.id;
  }
  return null;
}
