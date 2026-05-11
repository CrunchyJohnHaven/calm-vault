// Look up a customer by raw API key (sha-256 hashed before DB lookup).

import type { Env } from "../env";
import { apiKeyHash } from "./api_key";
import { HttpError } from "./http";

export interface CustomerRow {
  id: string;
  email: string;
  org_name: string;
  primary_mandate_commitment: string;
  tier: string;
  stripe_customer_id: string | null;
  created_at: number;
}

export async function authCustomer(
  env: Env,
  apiKey: string,
): Promise<CustomerRow> {
  if (!/^[0-9a-fA-F]{32}$/.test(apiKey)) {
    throw new HttpError(
      401,
      "invalid_api_key",
      "API key must be 32 hex characters.",
    );
  }
  const hash = await apiKeyHash(apiKey.toLowerCase());
  const row = await env.DB.prepare(
    `SELECT id, email, org_name, primary_mandate_commitment, tier, stripe_customer_id, created_at
       FROM customers
      WHERE api_key_hash = ?`,
  )
    .bind(hash)
    .first<CustomerRow>();
  if (!row) {
    throw new HttpError(401, "invalid_api_key", "Unknown API key.");
  }
  return row;
}
