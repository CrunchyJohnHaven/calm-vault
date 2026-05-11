// POST /signup
//
// Accepts { email, org_name, primary_mandate_commitment }, generates a 32-hex
// API key, writes the customer row to D1, and fires a welcome email via Resend.
// Returns the raw API key exactly once.

import type { Env } from "../env";
import { generateApiKey, apiKeyHash } from "../lib/api_key";
import { sendWelcomeEmail } from "../lib/email";
import { HttpError, jsonResponse, readJson, requireString } from "../lib/http";
import { newCustomerId } from "../lib/ids";

interface SignupBody {
  email?: unknown;
  org_name?: unknown;
  primary_mandate_commitment?: unknown;
}

// Cheap RFC-5321-ish syntax check; full validation lives at the email provider.
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function handleSignup(
  request: Request,
  env: Env,
): Promise<Response> {
  const body = await readJson<SignupBody>(request);
  const email = requireString(body.email, "email", { maxLen: 254 }).toLowerCase();
  if (!EMAIL_RE.test(email)) {
    throw new HttpError(400, "invalid_field", "Field 'email' is not a valid email.");
  }
  const orgName = requireString(body.org_name, "org_name", { maxLen: 200 });
  const commitment = requireString(
    body.primary_mandate_commitment,
    "primary_mandate_commitment",
    { maxLen: 4096 },
  );

  const existing = await env.DB.prepare(
    "SELECT id FROM customers WHERE email = ?",
  )
    .bind(email)
    .first<{ id: string }>();
  if (existing) {
    throw new HttpError(
      409,
      "email_taken",
      "An account already exists for this email.",
    );
  }

  const apiKey = generateApiKey();
  const hash = await apiKeyHash(apiKey);
  const id = newCustomerId();
  const createdAt = Math.floor(Date.now() / 1000);

  await env.DB.prepare(
    `INSERT INTO customers
       (id, email, org_name, primary_mandate_commitment, api_key_hash, tier, created_at)
     VALUES (?, ?, ?, ?, ?, 'free', ?)`,
  )
    .bind(id, email, orgName, commitment, hash, createdAt)
    .run();

  const emailResult = await sendWelcomeEmail(env, {
    to: email,
    orgName,
    apiKey,
    publicOrigin: env.PUBLIC_ORIGIN,
  });

  return jsonResponse(
    {
      customer_id: id,
      email,
      org_name: orgName,
      api_key: apiKey,
      tier: "free",
      next_step: `${env.PUBLIC_ORIGIN}/register-org`,
      docs: `${env.PUBLIC_ORIGIN}/docs/api`,
      upgrade_url: `${env.PUBLIC_ORIGIN}/checkout/pro`,
      welcome_email: emailResult.sent
        ? { delivered: true, provider_id: emailResult.provider_id }
        : { delivered: false, reason: emailResult.error ?? "unknown" },
    },
    201,
  );
}
