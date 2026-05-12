import { json, err, ok, readJson } from "../_lib/util.js";
import { gradeAttempt } from "../_lib/grader.js";
import { sendEmail, tTestVerdict, tAdminTestSubmitted } from "../_lib/emailer.js";

export const onRequestOptions = () => new Response(null, { status: 204 });

export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);
  const token = (body.token || "").trim();
  const track = (body.track || "").trim();
  const answers = body.answers || {};

  if (!token) return err("Missing token.", 400);
  if (!["mechanical", "light_judgment", "heavy_judgment", "specialized", "domain_expert"].includes(track)) {
    return err("Invalid track.", 400);
  }

  const applicant = await env.DB.prepare(
    "SELECT * FROM applicants WHERE session_token = ?"
  ).bind(token).first();
  if (!applicant) return err("Unknown session token.", 401);

  let graded;
  try {
    graded = await gradeAttempt(env, track, answers);
  } catch (e) {
    console.warn("[test-submit] grader failed", e);
    return err("Grading failed: " + String(e), 500);
  }

  const now = Date.now();
  await env.DB.prepare(
    `INSERT INTO test_attempts (created_at, applicant_id, track, raw_answers, per_question, mc_score, text_score, ai_score, composite, verdict, ai_feedback, elapsed_seconds)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(
    now, applicant.id, track,
    JSON.stringify(answers),
    JSON.stringify(graded.per_question),
    graded.mc_score, graded.text_score, graded.ai_score,
    graded.composite, graded.verdict, graded.ai_feedback,
    Number(body.elapsed_seconds) || null
  ).run();

  // Auto-disposition: PASS → tested, SHORTLIST → shortlist, FAIL → disqualified
  const newStatus = graded.verdict === "PASS" ? "tested"
                  : graded.verdict === "SHORTLIST" ? "shortlist"
                  : "disqualified";
  await env.DB.prepare(
    "UPDATE applicants SET status = ?, updated_at = ? WHERE id = ?"
  ).bind(newStatus, now, applicant.id).run();

  // Emails.
  const appUrl = env.APP_URL || "https://internsforai.org";
  const workerUrl = appUrl + "/worker.html?token=" + encodeURIComponent(applicant.session_token);
  const tmpl = tTestVerdict({ applicant, verdict: graded.verdict, composite: graded.composite, workerUrl });
  await sendEmail(env, { to: applicant.email, subject: tmpl.subject, html: tmpl.html, text: tmpl.text });

  const adminEmail = env.ADMIN_EMAIL || "calm@thecreativitymachine.ai";
  const att = Object.assign({ track }, graded);
  const adminTmpl = tAdminTestSubmitted({ applicant, attempt: att });
  await sendEmail(env, { to: adminEmail, subject: adminTmpl.subject, html: adminTmpl.html, text: adminTmpl.text });

  return ok({ verdict: graded.verdict, composite: graded.composite, per_question: graded.per_question });
}
