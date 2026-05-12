// Email send helper, wraps Resend's REST API.
// If RESEND_API_KEY is missing, we no-op + log so local dev still works.

export async function sendEmail(env, { to, subject, html, text, from }) {
  const apiKey = env.RESEND_API_KEY;
  const fromAddr = from || env.FROM_EMAIL || "InternsForAI <onboarding@resend.dev>";
  if (!apiKey) {
    console.log("[email] (no RESEND_API_KEY; not sent) to=" + to + " subject=" + subject);
    return { ok: false, skipped: true };
  }
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "authorization": "Bearer " + apiKey, "content-type": "application/json" },
      body: JSON.stringify({ from: fromAddr, to: Array.isArray(to) ? to : [to], subject, html, text })
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      console.warn("[email] resend error", r.status, j);
      return { ok: false, status: r.status, error: j };
    }
    return { ok: true, id: j.id };
  } catch (e) {
    console.warn("[email] send failed", e);
    return { ok: false, error: String(e) };
  }
}

export function tApplyConfirmation({ applicant, appUrl, testUrl }) {
  return {
    subject: "InternsForAI — application received. Take the 30-min skills test next.",
    html:
      `<p>Hey ${escapeHtml(applicant.display_name)},</p>` +
      `<p>Your application is in. The next step is the 30-minute skills test:</p>` +
      `<p><a href="${escapeHtml(testUrl)}">${escapeHtml(testUrl)}</a></p>` +
      `<p>It's auto-graded. You'll see your verdict (PASS / SHORTLIST / FAIL) the moment you submit.</p>` +
      `<p>If you'd rather take it later, this email is your magic link — same URL works any time within 14 days.</p>` +
      `<p>— Calm + Dennis the Peasant<br/>` +
      `InternsForAI · We are all AI Interns.<br/>` +
      `<a href="${escapeHtml(appUrl)}">internsforai.org</a></p>`,
    text:
      "Your application is in. Take the 30-min skills test: " + testUrl +
      "\n\n— Calm + Dennis the Peasant\nInternsForAI · We are all AI Interns."
  };
}

export function tTestVerdict({ applicant, verdict, composite, workerUrl }) {
  const headline = verdict === "PASS" ? "PASS — match queued."
                 : verdict === "SHORTLIST" ? "SHORTLIST — admin review."
                 : "FAIL — not this round.";
  return {
    subject: "InternsForAI test result: " + verdict + " (" + composite.toFixed(1) + " / 100)",
    html:
      `<p>Hey ${escapeHtml(applicant.display_name)},</p>` +
      `<p><strong>${headline}</strong></p>` +
      `<p>Composite score: ${composite.toFixed(1)} / 100.</p>` +
      (verdict === "PASS"
        ? `<p>Your worker dashboard is ready. Match within 24h: <a href="${escapeHtml(workerUrl)}">${escapeHtml(workerUrl)}</a></p>`
        : verdict === "SHORTLIST"
          ? `<p>Admin (John) reviews your test answers + AI-cofounder pitch and emails a decision within 24h.</p>`
          : `<p>We aren't matching you this round. You can re-apply in 90 days.</p>`),
    text: headline + " Composite: " + composite.toFixed(1) + "/100. " + workerUrl
  };
}

export function tMatchInvite({ applicant, project, match, workerUrl }) {
  return {
    subject: "InternsForAI — your AAO match: " + project.name,
    html:
      `<p>Hey ${escapeHtml(applicant.display_name)},</p>` +
      `<p>We've matched you to <strong>${escapeHtml(project.name)}</strong>.</p>` +
      `<blockquote>${escapeHtml(match.brief_override || project.brief)}</blockquote>` +
      `<p>Your share: <strong>${(100 - match.franchise_percent).toFixed(0)}%</strong>. Network share: <strong>${match.franchise_percent.toFixed(0)}%</strong>. Read <a href="https://internsforai.org/technosocialism.html">the manifesto</a> for the full doctrine.</p>` +
      `<p>Accept or decline from your worker dashboard:</p>` +
      `<p><a href="${escapeHtml(workerUrl)}">${escapeHtml(workerUrl)}</a></p>` +
      `<p>— Calm + Dennis the Peasant<br/>InternsForAI</p>`,
    text: "Match: " + project.name + " · your share " + (100 - match.franchise_percent) + "% · " + workerUrl
  };
}

export function tAdminTestSubmitted({ applicant, attempt }) {
  return {
    subject: "[IFA admin] new test: " + applicant.display_name + " · " + attempt.track + " · " + attempt.verdict + " (" + attempt.composite.toFixed(1) + ")",
    html:
      `<p><strong>${escapeHtml(applicant.display_name)}</strong> (${escapeHtml(applicant.email)}, ${escapeHtml(applicant.country)}) submitted the <code>${escapeHtml(attempt.track)}</code> test.</p>` +
      `<ul>` +
      `<li>Verdict: <strong>${escapeHtml(attempt.verdict)}</strong></li>` +
      `<li>Composite: <strong>${attempt.composite.toFixed(1)} / 100</strong></li>` +
      `<li>MC: ${attempt.mc_score.toFixed(2)} · Text: ${attempt.text_score.toFixed(2)} · AI: ${attempt.ai_score.toFixed(2)}</li>` +
      `</ul>` +
      `<p>AI feedback: ${escapeHtml(attempt.ai_feedback || "")}</p>` +
      `<p>Open the admin dashboard to disposition: <a href="https://internsforai.org/admin.html">/admin</a></p>`,
    text: applicant.display_name + " · " + attempt.track + " · " + attempt.verdict + " · " + attempt.composite.toFixed(1)
  };
}

export function tMagicLink({ applicant, magicUrl }) {
  return {
    subject: "InternsForAI — your sign-in link",
    html:
      `<p>Hey ${escapeHtml(applicant.display_name)},</p>` +
      `<p>One-time sign-in for your worker dashboard. Valid for 7 days.</p>` +
      `<p><a href="${escapeHtml(magicUrl)}">${escapeHtml(magicUrl)}</a></p>` +
      `<p>If you didn't request this, you can ignore the email.</p>`,
    text: "Sign-in link: " + magicUrl
  };
}

export function escapeHtml(s) {
  return (s == null ? "" : String(s)).replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
}
