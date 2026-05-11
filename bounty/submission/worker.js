// AAL Bug Bounty submission endpoint.
//
// Deploys as a Cloudflare Worker bound to:
//   - D1 database `BOUNTY_DB` (separate from any customer-signup DB)
//   - KV namespace `BOUNTY_RATE` (optional, used for rate limiting)
//
// Exposes:
//   POST /bounty/submit       — accept a bug report (JSON body)
//   GET  /bounty/status/:id   — look up status of a tracking id (no PII returned)
//   GET  /bounty/health       — basic liveness
//
// All other routes 404. CORS is locked to the canonical sameasyou.ai origin
// plus localhost for dev. Schema is in schema.sql.
//
// Apache 2.0 · github.com/CrunchyJohnHaven/calm-vault

const ALLOWED_ORIGINS = new Set([
  "https://sameasyou.ai",
  "https://www.sameasyou.ai",
  "http://localhost:8787",
  "http://127.0.0.1:8787",
]);

const BUG_CLASSES = new Set([
  "kill_switch_bypass",
  "bradley_gavini_crypto",
  "synthesizer_prompt_injection",
  "watermarked_chain_mod",
  "sybil_attack",
  "other_novel",
]);

const PAYMENT_RAILS = new Set(["stripe", "wise", "usdc_base", "other"]);

const MAX_FIELD_LEN = {
  description: 16_000,
  proof_of_concept: 64_000,
  contact: 256,
  handle: 128,
  commit_sha: 128,
};

const SUBMIT_RATE_PER_HOUR = 5;
const SUBMIT_RATE_WINDOW_S = 3600;

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.has(origin) ? origin : "https://sameasyou.ai";
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function jsonResponse(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      "Referrer-Policy": "no-referrer",
      ...corsHeaders(origin),
    },
  });
}

function clientIp(request) {
  return (
    request.headers.get("CF-Connecting-IP") ||
    request.headers.get("X-Forwarded-For") ||
    "0.0.0.0"
  );
}

async function rateLimit(env, ip) {
  if (!env.BOUNTY_RATE) return { ok: true, remaining: SUBMIT_RATE_PER_HOUR };
  const key = `submit:${ip}`;
  const raw = await env.BOUNTY_RATE.get(key);
  const n = raw ? parseInt(raw, 10) : 0;
  if (n >= SUBMIT_RATE_PER_HOUR) {
    return { ok: false, remaining: 0 };
  }
  await env.BOUNTY_RATE.put(key, String(n + 1), {
    expirationTtl: SUBMIT_RATE_WINDOW_S,
  });
  return { ok: true, remaining: SUBMIT_RATE_PER_HOUR - (n + 1) };
}

function trackingId() {
  // 96-bit tracking id, base32-ish, no ambiguity chars.
  const bytes = new Uint8Array(12);
  crypto.getRandomValues(bytes);
  const alpha = "23456789ABCDEFGHJKLMNPQRSTVWXYZ";
  let out = "";
  for (const b of bytes) out += alpha[b % alpha.length];
  return `AAL-${out.slice(0, 4)}-${out.slice(4, 8)}-${out.slice(8, 12)}-${out.slice(12, 16)}-${out.slice(16, 20)}-${out.slice(20, 24)}`;
}

function validate(body) {
  if (!body || typeof body !== "object") return "Empty body.";
  if (!BUG_CLASSES.has(body.bug_class)) return "Unknown bug_class.";
  if (!PAYMENT_RAILS.has(body.payment_rail)) return "Unknown payment_rail.";

  const sev = Number(body.severity_rating);
  if (!Number.isFinite(sev) || sev < 1 || sev > 10) {
    return "severity_rating must be an integer 1-10.";
  }

  if (typeof body.description !== "string" || body.description.trim().length < 40) {
    return "description must be at least 40 characters.";
  }
  if (typeof body.proof_of_concept !== "string" || body.proof_of_concept.trim().length < 10) {
    return "proof_of_concept must be at least 10 characters.";
  }
  if (typeof body.contact !== "string" || body.contact.trim().length < 3) {
    return "contact is required.";
  }

  for (const [k, max] of Object.entries(MAX_FIELD_LEN)) {
    const v = body[k];
    if (v != null && typeof v !== "string") return `${k} must be a string.`;
    if (v && v.length > max) return `${k} exceeds ${max} characters.`;
  }
  return null;
}

async function handleSubmit(request, env) {
  const origin = request.headers.get("Origin") || "";
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse(400, { error: "Invalid JSON." }, origin);
  }

  const err = validate(body);
  if (err) return jsonResponse(400, { error: err }, origin);

  const ip = clientIp(request);
  const limit = await rateLimit(env, ip);
  if (!limit.ok) {
    return jsonResponse(
      429,
      { error: "Rate limit exceeded. Try again in an hour, or email bounty@sameasyou.ai." },
      origin,
    );
  }

  const id = trackingId();
  const now = Math.floor(Date.now() / 1000);
  const ua = request.headers.get("User-Agent") || "";

  try {
    await env.BOUNTY_DB.prepare(
      `INSERT INTO bounty_submissions
       (tracking_id, bug_class, severity_rating, description, proof_of_concept,
        contact, payment_rail, handle, commit_sha, source_ip, user_agent,
        status, created_at, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'received', ?, ?)`,
    )
      .bind(
        id,
        body.bug_class,
        Math.trunc(Number(body.severity_rating)),
        body.description.trim(),
        body.proof_of_concept.trim(),
        body.contact.trim(),
        body.payment_rail,
        (body.handle || "").trim() || null,
        (body.commit_sha || "").trim() || null,
        ip,
        ua.slice(0, 512),
        now,
        now,
      )
      .run();
  } catch (e) {
    return jsonResponse(
      500,
      { error: "Storage error. Email bounty@sameasyou.ai and reference the timestamp." },
      origin,
    );
  }

  return jsonResponse(
    200,
    {
      ok: true,
      tracking_id: id,
      message:
        "Submission received. Save the tracking id. Acknowledgement within 48h, verdict within 7 days.",
    },
    origin,
  );
}

async function handleStatus(request, env, id) {
  const origin = request.headers.get("Origin") || "";
  if (!/^AAL-[2-9A-Z-]{3,80}$/.test(id)) {
    return jsonResponse(400, { error: "Bad tracking id." }, origin);
  }
  try {
    const row = await env.BOUNTY_DB.prepare(
      `SELECT tracking_id, bug_class, status, triage_class, triage_tier,
              accepted, paid_at, created_at, updated_at
       FROM bounty_submissions WHERE tracking_id = ? LIMIT 1`,
    )
      .bind(id)
      .first();
    if (!row) return jsonResponse(404, { error: "Not found." }, origin);
    return jsonResponse(200, { ok: true, submission: row }, origin);
  } catch (e) {
    return jsonResponse(500, { error: "Lookup failed." }, origin);
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname === "/bounty/health" && request.method === "GET") {
      return jsonResponse(200, { ok: true, service: "aal-bounty", version: "1" }, origin);
    }

    if (url.pathname === "/bounty/submit" && request.method === "POST") {
      return handleSubmit(request, env);
    }

    const statusMatch = url.pathname.match(/^\/bounty\/status\/([A-Z0-9-]+)$/);
    if (statusMatch && request.method === "GET") {
      return handleStatus(request, env, statusMatch[1]);
    }

    return jsonResponse(404, { error: "Not found." }, origin);
  },
};
