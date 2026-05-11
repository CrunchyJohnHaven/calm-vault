/**
 * GET /api/reviewer/files
 *
 * Returns the list of files reviewers are allowed to edit. The /reviewer/submit
 * page calls this to populate the file dropdown so the allowlist lives in code,
 * not the frontend.
 */
import type { VercelRequest, VercelResponse } from "@vercel/node";
import { ALLOWED_FILES, PR_TARGET } from "./_allowed.js";

export default function handler(req: VercelRequest, res: VercelResponse): void {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    res.status(405).json({ ok: false, error: "method not allowed" });
    return;
  }

  res.setHeader("Cache-Control", "public, max-age=60, s-maxage=300");
  res.status(200).json({
    ok: true,
    target: PR_TARGET,
    files: ALLOWED_FILES,
  });
}
