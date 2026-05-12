import { err, ok, readJson, verifyAdmin } from "../../_lib/util.js";

export async function onRequestPost({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const id = parseInt(body.applicant_id, 10);
  const notes = String(body.admin_notes || "").slice(0, 8000);
  if (!id) return err("Missing applicant_id.", 400);
  await env.DB.prepare("UPDATE applicants SET admin_notes = ?, updated_at = ? WHERE id = ?")
    .bind(notes, Date.now(), id).run();
  return ok({ id });
}
