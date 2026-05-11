// Stripe webhook signature verification.
//
// Stripe sends a `Stripe-Signature` header of the form:
//   t=<unix_ts>,v1=<hex_hmac_sha256_signature>,v1=<another_signature>,...
//
// We verify with `HMAC-SHA256(secret, "${t}.${rawBody}")` against each `v1=`.
// We also enforce a 5-minute timestamp tolerance to make replay harder.

const TOLERANCE_SECONDS = 5 * 60;

export interface StripeVerificationResult {
  ok: boolean;
  reason?: string;
}

export async function verifyStripeSignature(
  rawBody: string,
  header: string | null,
  secret: string,
  now: number = Math.floor(Date.now() / 1000),
): Promise<StripeVerificationResult> {
  if (!header) {
    return { ok: false, reason: "missing Stripe-Signature header" };
  }
  if (!secret) {
    return { ok: false, reason: "STRIPE_WEBHOOK_SECRET not configured" };
  }
  const parts = header.split(",").map((p) => p.trim());
  let ts: number | null = null;
  const sigs: string[] = [];
  for (const p of parts) {
    const eq = p.indexOf("=");
    if (eq < 0) continue;
    const k = p.slice(0, eq);
    const v = p.slice(eq + 1);
    if (k === "t") ts = parseInt(v, 10);
    else if (k === "v1") sigs.push(v);
  }
  if (ts === null || sigs.length === 0) {
    return { ok: false, reason: "malformed Stripe-Signature header" };
  }
  if (Math.abs(now - ts) > TOLERANCE_SECONDS) {
    return { ok: false, reason: "timestamp outside tolerance window" };
  }

  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const expected = new Uint8Array(
    (await crypto.subtle.sign(
      "HMAC",
      key,
      new TextEncoder().encode(`${ts}.${rawBody}`),
    )) as ArrayBuffer,
  );
  const expectedHex = bytesToHex(expected);
  for (const sig of sigs) {
    if (constantTimeEqual(sig.toLowerCase(), expectedHex)) {
      return { ok: true };
    }
  }
  return { ok: false, reason: "no v1 signature matched" };
}

function bytesToHex(b: Uint8Array): string {
  let out = "";
  for (let i = 0; i < b.length; i++) {
    out += b[i]!.toString(16).padStart(2, "0");
  }
  return out;
}

function constantTimeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) {
    r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return r === 0;
}
