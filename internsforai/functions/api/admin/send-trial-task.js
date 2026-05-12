import { err, ok, readJson, verifyAdmin } from "../../_lib/util.js";
import { sendEmail } from "../../_lib/emailer.js";

export async function onRequestPost({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const applicant_id = parseInt(body.applicant_id, 10);
  const amount_usd = Number(body.amount_usd || 3);
  const brief = String(body.brief || "Reply with a 50-word summary of the technosocialism manifesto to prove you read it. We pay $" + amount_usd.toFixed(2) + " on receipt.");
  if (!applicant_id) return err("Missing applicant_id.", 400);
  const a = await env.DB.prepare("SELECT * FROM applicants WHERE id = ?").bind(applicant_id).first();
  if (!a) return err("Unknown applicant.", 404);
  await sendEmail(env, {
    to: a.email,
    subject: "InternsForAI — trial task ($" + amount_usd.toFixed(2) + ")",
    html: "<p>Hey " + a.display_name + ",</p><p>Quick trial task:</p><blockquote>" + brief + "</blockquote><p>Reply directly to this email with your work. We pay on receipt.</p>",
    text: brief
  });
  return ok({ applicant_id });
}
