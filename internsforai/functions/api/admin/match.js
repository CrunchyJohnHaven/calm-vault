import { err, ok, readJson, verifyAdmin, randomToken } from "../../_lib/util.js";
import { sendEmail, tMatchInvite } from "../../_lib/emailer.js";

export async function onRequestPost({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const applicant_id = parseInt(body.applicant_id, 10);
  const project_id = parseInt(body.project_id, 10);
  const franchise_percent = Number(body.franchise_percent);
  const brief_override = String(body.brief_override || "").slice(0, 4000);

  if (!applicant_id || !project_id) return err("Missing applicant_id or project_id.", 400);
  if (!(franchise_percent >= 0 && franchise_percent <= 100)) return err("franchise_percent must be 0..100.", 400);

  const applicant = await env.DB.prepare("SELECT * FROM applicants WHERE id = ?").bind(applicant_id).first();
  if (!applicant) return err("Unknown applicant.", 404);
  const project = await env.DB.prepare("SELECT * FROM aao_projects WHERE id = ?").bind(project_id).first();
  if (!project) return err("Unknown project.", 404);

  const now = Date.now();
  const worker_percent = 100 - franchise_percent;
  const ins = await env.DB.prepare(
    "INSERT INTO matches (created_at, applicant_id, project_id, franchise_percent, worker_percent, brief_override, status) VALUES (?, ?, ?, ?, ?, ?, 'proposed')"
  ).bind(now, applicant_id, project_id, franchise_percent, worker_percent, brief_override).run();

  await env.DB.prepare("UPDATE applicants SET status = 'matched', updated_at = ? WHERE id = ?")
    .bind(now, applicant_id).run();

  // Magic-link for worker dashboard (one-time, 7 days)
  const magic = randomToken(32);
  const expires = now + 7 * 24 * 60 * 60 * 1000;
  await env.DB.prepare(
    "INSERT INTO magic_links (created_at, applicant_id, token, expires_at) VALUES (?, ?, ?, ?)"
  ).bind(now, applicant_id, magic, expires).run();

  const appUrl = env.APP_URL || "https://internsforai.org";
  const workerUrl = appUrl + "/worker?token=" + encodeURIComponent(magic);
  const tmpl = tMatchInvite({
    applicant, project,
    match: { franchise_percent, brief_override },
    workerUrl
  });
  await sendEmail(env, { to: applicant.email, subject: tmpl.subject, html: tmpl.html, text: tmpl.text });

  return ok({ match_id: ins.meta && ins.meta.last_row_id, worker_url: workerUrl });
}
