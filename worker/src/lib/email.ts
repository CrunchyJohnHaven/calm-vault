// Resend transactional-email integration.
//
// The Worker fires welcome emails on /signup. If RESEND_API_KEY is not set
// (e.g. in local dev), sends are no-ops that log a warning so the rest of
// the flow remains testable end-to-end without external dependencies.

import type { Env } from "../env";

export interface WelcomeEmailParams {
  to: string;
  orgName: string;
  apiKey: string;
  publicOrigin: string;
}

export async function sendWelcomeEmail(
  env: Env,
  params: WelcomeEmailParams,
): Promise<{ sent: boolean; provider_id?: string; error?: string }> {
  if (!env.RESEND_API_KEY) {
    console.warn(
      "[email] RESEND_API_KEY not configured; skipping welcome email to",
      params.to,
    );
    return { sent: false, error: "RESEND_API_KEY not configured" };
  }
  const from = env.FROM_EMAIL || "Calm Vault <hello@sameasyou.ai>";
  const subject = "Welcome to Calm Vault — your AI org is one POST away";
  const text = renderText(params);
  const html = renderHtml(params);

  const resp = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: [params.to],
      subject,
      text,
      html,
    }),
  });
  if (!resp.ok) {
    const body = await resp.text();
    console.error("[email] resend send failed", resp.status, body);
    return { sent: false, error: `resend ${resp.status}: ${body}` };
  }
  const json = (await resp.json()) as { id?: string };
  return { sent: true, provider_id: json.id };
}

function renderText(p: WelcomeEmailParams): string {
  return [
    `Welcome to Calm Vault, ${p.orgName}.`,
    ``,
    `Your API key (treat it like a password — we only store its hash):`,
    ``,
    `  ${p.apiKey}`,
    ``,
    `Next step: register your Autonomous AI Org so it gets a genesis block on the`,
    `Bradley-Gavini Protocol.`,
    ``,
    `  curl -X POST ${p.publicOrigin}/register-org \\`,
    `    -H "Content-Type: application/json" \\`,
    `    -d '{"api_key": "${p.apiKey}", "org_legal_name": "Your LLC", "founder_name": "Your Name", "jurisdiction": "Delaware"}'`,
    ``,
    `Full API docs: ${p.publicOrigin}/docs/api`,
    ``,
    `— Calm Vault`,
  ].join("\n");
}

function renderHtml(p: WelcomeEmailParams): string {
  return `<!doctype html><html><body style="font-family:-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.6;color:#0b0d10;max-width:600px;margin:0 auto;padding:24px;">
    <h2 style="margin:0 0 8px 0;">Welcome to Calm Vault, ${escapeHtml(p.orgName)}.</h2>
    <p>Your API key (treat it like a password — we only store its hash):</p>
    <p style="font-family:JetBrains Mono,ui-monospace,monospace;font-size:15px;background:#f4f6f8;padding:12px;border-radius:8px;word-break:break-all;">${escapeHtml(p.apiKey)}</p>
    <p>Next step: register your Autonomous AI Org so it gets a genesis block on the Bradley-Gavini Protocol.</p>
    <pre style="background:#0b0d10;color:#a4f3c4;padding:16px;border-radius:8px;overflow-x:auto;font-size:13px;">curl -X POST ${escapeHtml(p.publicOrigin)}/register-org \\
  -H "Content-Type: application/json" \\
  -d '{"api_key": "${escapeHtml(p.apiKey)}", "org_legal_name": "Your LLC", "founder_name": "Your Name", "jurisdiction": "Delaware"}'</pre>
    <p>Full API docs: <a href="${escapeHtml(p.publicOrigin)}/docs/api">${escapeHtml(p.publicOrigin)}/docs/api</a></p>
    <p style="color:#5b6778;font-size:14px;">— Calm Vault</p>
  </body></html>`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
