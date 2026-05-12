import { err, ok, readJson, randomToken, isEmail } from "../../_lib/util.js";
import { sendEmail, tMagicLink } from "../../_lib/emailer.js";

export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const email = String(body.email || "").trim().toLowerCase();
  if (!isEmail(email)) return err("Email looks invalid.", 400);
  const a = await env.DB.prepare("SELECT * FROM applicants WHERE email = ?").bind(email).first();
  if (!a) {
    // Don't leak whether the email exists.
    return ok({ sent: true });
  }
  const tok = randomToken(32);
  const expires = Date.now() + 7 * 24 * 60 * 60 * 1000;
  await env.DB.prepare(
    "INSERT INTO magic_links (created_at, applicant_id, token, expires_at) VALUES (?, ?, ?, ?)"
  ).bind(Date.now(), a.id, tok, expires).run();
  const appUrl = env.APP_URL || "https://internsforai.org";
  const magicUrl = appUrl + "/worker.html?token=" + encodeURIComponent(tok);
  const tmpl = tMagicLink({ applicant: a, magicUrl });
  await sendEmail(env, { to: email, subject: tmpl.subject, html: tmpl.html, text: tmpl.text });
  return ok({ sent: true });
}
