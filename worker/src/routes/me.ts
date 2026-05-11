// GET /me
//
// Auth'd self-service. Reads the API key from the Authorization Bearer header
// (preferred) or the `api_key` query parameter. Returns the customer + their
// orgs + tier + upgrade URL.

import type { Env } from "../env";
import { authCustomer } from "../lib/auth";
import { HttpError, jsonResponse } from "../lib/http";

interface OrgRow {
  id: string;
  org_legal_name: string;
  founder_name: string;
  jurisdiction: string;
  commitment_c: string;
  genesis_block_hash: string;
  head_block_hash: string;
  created_at: number;
}

export async function handleMe(
  request: Request,
  env: Env,
): Promise<Response> {
  const apiKey = extractApiKey(request);
  if (!apiKey) {
    throw new HttpError(
      401,
      "missing_api_key",
      "Provide your API key via `Authorization: Bearer <key>` or `?api_key=<key>`.",
    );
  }
  const customer = await authCustomer(env, apiKey);

  // Re-fetch the full row (authCustomer returns the subset we need but we want pro_since too).
  const full = await env.DB.prepare(
    `SELECT id, email, org_name, tier, pro_since, stripe_customer_id, stripe_subscription_id, created_at
       FROM customers
      WHERE id = ?`,
  )
    .bind(customer.id)
    .first<{
      id: string;
      email: string;
      org_name: string;
      tier: string;
      pro_since: number | null;
      stripe_customer_id: string | null;
      stripe_subscription_id: string | null;
      created_at: number;
    }>();

  const orgs = await env.DB.prepare(
    `SELECT id, org_legal_name, founder_name, jurisdiction, commitment_c,
            genesis_block_hash, head_block_hash, created_at
       FROM orgs
      WHERE customer_id = ?
      ORDER BY created_at DESC, id DESC`,
  )
    .bind(customer.id)
    .all<OrgRow>();

  return jsonResponse({
    customer: {
      id: full!.id,
      email: full!.email,
      org_name: full!.org_name,
      tier: full!.tier,
      pro_since: full!.pro_since,
      stripe_customer_id: full!.stripe_customer_id,
      stripe_subscription_id: full!.stripe_subscription_id,
      created_at: full!.created_at,
    },
    orgs: (orgs.results ?? []).map((o) => ({
      org_id: o.id,
      org_legal_name: o.org_legal_name,
      founder_name: o.founder_name,
      jurisdiction: o.jurisdiction,
      public_commitment: o.commitment_c,
      genesis_block_hash: o.genesis_block_hash,
      head_block_hash: o.head_block_hash,
      created_at: o.created_at,
      verifier_url: `${env.PUBLIC_ORIGIN}/verify/${o.id}`,
      certificate_url: `${env.PUBLIC_ORIGIN}/certificate/${o.id}`,
    })),
    upgrade_url: `${env.PUBLIC_ORIGIN}/checkout/pro`,
    docs: `${env.PUBLIC_ORIGIN}/docs/api`,
  });
}

export function extractApiKey(request: Request): string | null {
  const auth = request.headers.get("authorization");
  if (auth) {
    const m = auth.match(/^Bearer\s+([0-9a-fA-F]{32})\s*$/);
    if (m) return m[1]!;
  }
  const url = new URL(request.url);
  const q = url.searchParams.get("api_key");
  if (q && /^[0-9a-fA-F]{32}$/.test(q)) return q;
  return null;
}
