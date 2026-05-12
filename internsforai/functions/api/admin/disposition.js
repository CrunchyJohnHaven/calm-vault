import { err, ok, readJson, verifyAdmin } from "../../_lib/util.js";

const VALID = new Set(["pending","tested","shortlist","matched","active","paused","disqualified","inactive"]);

export async function onRequestPost({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const id = parseInt(body.applicant_id, 10);
  const status = String(body.status || "");
  if (!id) return err("Missing applicant_id.", 400);
  if (!VALID.has(status)) return err("Invalid status.", 400);
  const now = Date.now();
  const r = await env.DB.prepare(
    "UPDATE applicants SET status = ?, updated_at = ? WHERE id = ?"
  ).bind(status, now, id).run();
  if (!r.success) return err("Update failed.", 500);
  return ok({ id, status });
}
