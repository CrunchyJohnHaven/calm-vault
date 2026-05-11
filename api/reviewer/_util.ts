/**
 * Shared helpers for the /api/reviewer/* endpoints.
 *
 * No secrets are ever logged here. The GITHUB_PR_BOT_TOKEN env var is referenced
 * only by `loadGitHubToken()`, which returns the value or undefined and never
 * prints it.
 */

// Literal space only (not \s) — keeps tabs/newlines out of reviewer-attributed
// metadata that flows into commit authors, log lines, and PR bodies.
const REVIEWER_NAME_RE = /^[a-zA-Z0-9 ._-]{2,80}$/;
const PATH_TRAVERSAL_RE = /(^\/)|(\.\.)|(^~)|(\\)/;

export const MAX_EDITED_BYTES = 50 * 1024;
export const SUMMARY_MIN = 5;
export const SUMMARY_MAX = 200;
export const RATE_LIMIT_PER_HOUR = 10;

export function validateReviewerName(name: unknown): string {
  if (typeof name !== "string") throw badInput("reviewer name must be a string");
  const trimmed = name.trim();
  if (!REVIEWER_NAME_RE.test(trimmed)) {
    throw badInput(
      "reviewer name must be 2-80 chars and only contain letters, digits, spaces, dashes, underscores, dots (no tabs/newlines)",
    );
  }
  return trimmed;
}

export function validateOriginalFilePath(p: unknown, allowed: (s: string) => boolean): string {
  if (typeof p !== "string") throw badInput("original_file must be a string");
  if (PATH_TRAVERSAL_RE.test(p)) throw badInput("original_file path is not allowed");
  if (!allowed(p)) throw badInput(`original_file '${p}' is not in the allowlist`);
  return p;
}

export function validateEdited(edited: unknown): string {
  if (typeof edited !== "string") throw badInput("edited must be a string");
  // Length in bytes (UTF-8) — strings can be longer than chars when multibyte.
  const byteLen = Buffer.byteLength(edited, "utf8");
  if (byteLen === 0) throw badInput("edited content is empty");
  if (byteLen > MAX_EDITED_BYTES) {
    throw badInput(
      `edited content is ${byteLen} bytes; max allowed is ${MAX_EDITED_BYTES} bytes (50KB)`,
    );
  }
  return edited;
}

export function validateSummary(summary: unknown): string {
  if (typeof summary !== "string") throw badInput("summary must be a string");
  const trimmed = summary.trim();
  if (trimmed.length < SUMMARY_MIN || trimmed.length > SUMMARY_MAX) {
    throw badInput(`summary must be ${SUMMARY_MIN}-${SUMMARY_MAX} chars`);
  }
  return trimmed;
}

export function validateContact(contact: unknown): string | undefined {
  if (contact === undefined || contact === null || contact === "") return undefined;
  if (typeof contact !== "string") throw badInput("contact must be a string");
  const trimmed = contact.trim();
  if (trimmed.length === 0) return undefined;
  // Lightweight email regex — not RFC 5322 perfect but rejects obvious garbage.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed) || trimmed.length > 200) {
    throw badInput("contact must be a plausible email address");
  }
  return trimmed;
}

export function slugifyReviewer(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 40) || "anon";
}

export function basenameNoExt(p: string): string {
  const last = p.split("/").pop() ?? p;
  return last.replace(/\.[^.]+$/, "");
}

export function wordCount(s: string): number {
  const m = s.trim().match(/\S+/g);
  return m ? m.length : 0;
}

/** Stable error type so the handler can map to HTTP 400. */
export class BadInputError extends Error {
  readonly status = 400;
}
function badInput(msg: string): BadInputError {
  return new BadInputError(msg);
}

/** Token loader. Never logs the value — only "[token loaded]" / "[token missing]". */
export function loadGitHubToken(): { token: string | undefined; status: string } {
  const token = process.env.GITHUB_PR_BOT_TOKEN;
  if (!token) return { token: undefined, status: "[token missing]" };
  return { token, status: "[token loaded]" };
}

/* -------------------------------------------------------------------------- */
/* Rate limiting (in-memory; one Vercel function instance per region)         */
/* -------------------------------------------------------------------------- */

interface Bucket {
  count: number;
  resetAt: number;
}
const bucket: Map<string, Bucket> = (globalThis as unknown as { __reviewerRL?: Map<string, Bucket> })
  .__reviewerRL ??= new Map<string, Bucket>();

/** Returns true if the request is allowed. Hour-windowed. */
export function checkRateLimit(ip: string, limit = RATE_LIMIT_PER_HOUR): {
  allowed: boolean;
  remaining: number;
  resetAt: number;
} {
  const now = Date.now();
  const hour = 60 * 60 * 1000;
  // Evict stale entries when the bucket grows large so unique-IP traffic can't
  // grow memory unbounded on a warm Vercel instance.
  if (bucket.size > 5000) {
    for (const [k, v] of bucket) {
      if (v.resetAt <= now) bucket.delete(k);
    }
  }
  const existing = bucket.get(ip);
  if (!existing || existing.resetAt <= now) {
    const fresh = { count: 1, resetAt: now + hour };
    bucket.set(ip, fresh);
    return { allowed: true, remaining: limit - 1, resetAt: fresh.resetAt };
  }
  if (existing.count >= limit) {
    return { allowed: false, remaining: 0, resetAt: existing.resetAt };
  }
  existing.count += 1;
  return { allowed: true, remaining: limit - existing.count, resetAt: existing.resetAt };
}

export function clientIp(req: { headers: Record<string, string | string[] | undefined> }): string {
  const fwd = req.headers["x-forwarded-for"];
  if (typeof fwd === "string" && fwd.length > 0) return fwd.split(",")[0]!.trim();
  if (Array.isArray(fwd) && fwd.length > 0) return fwd[0]!.split(",")[0]!.trim();
  const real = req.headers["x-real-ip"];
  if (typeof real === "string") return real;
  return "unknown";
}
