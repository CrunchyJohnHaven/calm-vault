import { err, ok, readJson, verifyWorker } from "../../_lib/util.js";

const VALID = new Set(["accepted", "declined"]);

export async function onRequestPost({ request, env }) {
  const applicant = await verifyWorker(request, env);
  if (!applicant) return err("Unauthorized.", 401);
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const match_id = parseInt(body.match_id, 10);
  const status = String(body.status || "");
  if (!match_id || !VALID.has(status)) return err("Invalid match_id / status.", 400);

  const m = await env.DB.prepare("SELECT * FROM matches WHERE id = ? AND applicant_id = ?")
    .bind(match_id, applicant.id).first();
  if (!m) return err("Match not found.", 404);
  if (m.status !== "proposed") return err("Match no longer pending.", 409);

  const now = Date.now();
  await env.DB.prepare("UPDATE matches SET status = ? WHERE id = ?")
    .bind(status, match_id).run();
  if (status === "accepted") {
    await env.DB.prepare("UPDATE applicants SET status = 'active', updated_at = ? WHERE id = ?")
      .bind(now, applicant.id).run();
  }
  return ok({ match_id, status });
}
