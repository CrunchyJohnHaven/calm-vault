// Shared helpers for InternsForAI Pages Functions.

export function json(data, init = {}) {
  return new Response(JSON.stringify(data), {
    status: init.status || 200,
    headers: Object.assign({
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store"
    }, init.headers || {})
  });
}

export function err(message, status = 400) {
  return json({ ok: false, error: message }, { status });
}

export function ok(extra = {}) {
  return json(Object.assign({ ok: true }, extra));
}

export function cors(headers = {}) {
  return Object.assign({
    "access-control-allow-origin": "*",
    "access-control-allow-methods": "GET,POST,OPTIONS",
    "access-control-allow-headers": "content-type,x-admin-token,x-worker-token"
  }, headers);
}

export async function readJson(request) {
  try { return await request.json(); }
  catch (_e) { return null; }
}

// Cryptographically random token (hex). 32 bytes ~ 64 hex chars.
export function randomToken(bytes = 32) {
  const u = new Uint8Array(bytes);
  crypto.getRandomValues(u);
  return Array.from(u).map(b => b.toString(16).padStart(2, "0")).join("");
}

export function isEmail(s) {
  return typeof s === "string" && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

export function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

// Verify the admin token from header against env.ADMIN_TOKEN.
// Returns true/false. Uses timing-safe comparison via subtle crypto.
export async function verifyAdmin(request, env) {
  const provided = request.headers.get("x-admin-token") || "";
  const expected = env.ADMIN_TOKEN || "";
  if (!expected || provided.length === 0) return false;
  // constant-time compare via SHA-256
  const enc = new TextEncoder();
  const [a, b] = await Promise.all([
    crypto.subtle.digest("SHA-256", enc.encode(provided)),
    crypto.subtle.digest("SHA-256", enc.encode(expected))
  ]);
  const ua = new Uint8Array(a), ub = new Uint8Array(b);
  if (ua.length !== ub.length) return false;
  let diff = 0;
  for (let i = 0; i < ua.length; i++) diff |= ua[i] ^ ub[i];
  return diff === 0;
}

// Verify a worker session/magic-link token. Returns applicant row or null.
// Accepts either an X-Worker-Token header (preferred for mutating ops) or
// a ?token= query parameter (used by GET /api/worker/me which is reached
// via emailed magic links).
export async function verifyWorker(request, env) {
  let provided = request.headers.get("x-worker-token") || "";
  if (!provided) {
    try {
      const u = new URL(request.url);
      provided = u.searchParams.get("token") || "";
    } catch (_e) { /* ignore */ }
  }
  if (!provided) return null;
  // (1) session_token directly on applicants
  let row = await env.DB.prepare(
    "SELECT * FROM applicants WHERE session_token = ?"
  ).bind(provided).first();
  if (row) return row;
  // (2) one-time magic link
  const ml = await env.DB.prepare(
    "SELECT * FROM magic_links WHERE token = ? AND (used_at IS NULL OR used_at = 0)"
  ).bind(provided).first();
  if (!ml) return null;
  if (Number(ml.expires_at) < Date.now()) return null;
  // promote: mark used, fetch applicant
  await env.DB.prepare(
    "UPDATE magic_links SET used_at = ? WHERE id = ?"
  ).bind(Date.now(), ml.id).run();
  row = await env.DB.prepare(
    "SELECT * FROM applicants WHERE id = ?"
  ).bind(ml.applicant_id).first();
  return row;
}

export function safeJSONParse(s, fallback) {
  if (typeof s !== "string" || !s) return fallback;
  try { return JSON.parse(s); } catch { return fallback; }
}

// Convert an applicant row from D1 into a JSON-friendly object.
export function decodeApplicant(row) {
  if (!row) return null;
  return Object.assign({}, row, {
    tracks_arr: safeJSONParse(row.tracks, []),
    fluent_languages_arr: safeJSONParse(row.fluent_languages, []),
  });
}
