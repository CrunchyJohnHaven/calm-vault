export interface Env {
  DB: D1Database;

  // Public origin (e.g. "https://sameasyou.ai") — used to construct verifier URLs.
  PUBLIC_ORIGIN: string;
  FROM_EMAIL: string;
  STRIPE_PRO_PAYMENT_LINK: string;

  // Secrets (wrangler secret put ...).
  RESEND_API_KEY?: string;
  ANTHROPIC_API_KEY?: string;
}
