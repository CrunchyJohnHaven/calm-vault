import { json, err, ok, readJson, randomToken, isEmail } from "../_lib/util.js";
import { floorForCountry } from "../_lib/pay_rates.js";
import { sendEmail, tApplyConfirmation } from "../_lib/emailer.js";

export const onRequestOptions = () => new Response(null, { status: 204 });

export async function onRequestPost({ request, env }) {
  const body = await readJson(request);
  if (!body) return err("Invalid JSON.", 400);

  // Validate
  const email = (body.email || "").trim().toLowerCase();
  const display_name = (body.display_name || "").trim();
  const country = (body.country || "").trim();
  const tracks = Array.isArray(body.tracks) ? body.tracks.filter(Boolean) : [];
  const pay_method = (body.pay_method || "").trim();
  const pay_address = (body.pay_address || "").trim();
  const why_trial = (body.why_trial || "").trim();
  const cofounder_pitch = (body.cofounder_pitch || "").trim();

  if (!isEmail(email)) return err("Email looks invalid.", 400);
  if (display_name.length < 2) return err("Display name too short.", 400);
  if (!country) return err("Pick a country.", 400);
  if (tracks.length === 0) return err("Pick at least one skill track.", 400);
  if (!pay_method) return err("Pick a payment method.", 400);
  if (!pay_address) return err("Provide your wallet / payment email.", 400);
  if (why_trial.length < 80) return err("'Why' answer is too short.", 400);
  if (cofounder_pitch.length < 80) return err("'AI cofounder' answer is too short.", 400);

  const session_token = randomToken(32);
  const now = Date.now();
  const pay_floor = floorForCountry(country);
  const ip = request.headers.get("cf-connecting-ip") || "";
  const ua = request.headers.get("user-agent") || "";

  try {
    await env.DB.prepare(
      `INSERT INTO applicants (
        created_at, updated_at, email, display_name, country, timezone,
        native_language, fluent_languages, tracks, why_trial, editorial_catch,
        cofounder_pitch, sample_url, hours_per_week, pay_method, pay_address,
        pay_rate_floor, session_token, ip, user_agent, status
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')`
    ).bind(
      now, now, email, display_name, country, (body.timezone || "").trim(),
      (body.native_language || "").trim(),
      JSON.stringify(body.fluent_languages || []),
      JSON.stringify(tracks),
      why_trial,
      (body.editorial_catch || "").trim(),
      cofounder_pitch,
      (body.sample_url || "").trim(),
      Number(body.hours_per_week) || null,
      pay_method,
      pay_address,
      pay_floor,
      session_token,
      ip,
      ua
    ).run();
  } catch (e) {
    if (String(e).includes("UNIQUE")) {
      return err("That email already applied. We sent a magic link to your worker dashboard. (Check spam.)", 409);
    }
    console.warn("[apply] insert failed", e);
    return err("Database error. Try again.", 500);
  }

  const applicant = await env.DB.prepare(
    "SELECT * FROM applicants WHERE session_token = ?"
  ).bind(session_token).first();

  // Send the test link.
  const appUrl = env.APP_URL || "https://internsforai.org";
  const firstTrack = tracks[0];
  const testUrl = appUrl + "/skills-test?track=" + encodeURIComponent(firstTrack) + "&token=" + encodeURIComponent(session_token);
  const tmpl = tApplyConfirmation({ applicant, appUrl, testUrl });
  await sendEmail(env, { to: email, subject: tmpl.subject, html: tmpl.html, text: tmpl.text });

  // Notify admin too.
  const adminEmail = env.ADMIN_EMAIL || "calm@thecreativitymachine.ai";
  await sendEmail(env, {
    to: adminEmail,
    subject: "[IFA admin] new application: " + display_name + " (" + country + ", " + tracks.join("/") + ")",
    html: `<p><strong>${display_name}</strong> (${email}, ${country}) applied for: ${tracks.join(", ")}.</p>
           <p>Cofounder pitch: <em>${cofounder_pitch.slice(0, 400)}…</em></p>
           <p><a href="${appUrl}/admin.html">Open admin →</a></p>`,
    text: "New application: " + display_name
  });

  return ok({ token: session_token, applicant_id: applicant.id });
}
