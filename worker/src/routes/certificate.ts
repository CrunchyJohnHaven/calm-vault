// GET /certificate/<org_id>
//
// Public, printable HTML certificate of formation. Cosmetic-but-useful: this is
// the artifact a founder shows when they want a one-page proof that their AI
// org was registered with a Pedersen commitment on the Bradley-Gavini Protocol.

import type { Env } from "../env";
import { errorResponse, htmlResponse } from "../lib/http";

interface OrgRow {
  id: string;
  org_legal_name: string;
  founder_name: string;
  jurisdiction: string;
  commitment_c: string;
  genesis_block_hash: string;
  head_block_hash: string;
  created_at: number;
}

export async function handleCertificate(
  env: Env,
  orgId: string,
): Promise<Response> {
  const row = await env.DB.prepare(
    `SELECT id, org_legal_name, founder_name, jurisdiction, commitment_c,
            genesis_block_hash, head_block_hash, created_at
       FROM orgs
      WHERE id = ?`,
  )
    .bind(orgId)
    .first<OrgRow>();
  if (!row) {
    return errorResponse(
      404,
      "org_not_found",
      `No org found for id ${orgId}.`,
    );
  }
  const html = renderCertificate(env.PUBLIC_ORIGIN, row);
  return htmlResponse(html);
}

function renderCertificate(origin: string, o: OrgRow): string {
  const created = new Date(o.created_at * 1000).toISOString().replace("T", " ").slice(0, 19) + " UTC";
  const shortC = o.commitment_c.slice(0, 24) + "…" + o.commitment_c.slice(-24);
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Certificate of Formation — ${escapeHtml(o.org_legal_name)}</title>
  <link rel="canonical" href="${origin}/certificate/${escapeHtml(o.id)}" />
  <style>
    @media print { @page { size: A4; margin: 24mm; } body { background: #fff; } .actions { display: none; } }
    body {
      margin: 0; background: #fafaf7; color: #1a1a1a;
      font-family: "Georgia", "Times New Roman", serif; line-height: 1.6;
    }
    .page {
      max-width: 760px; margin: 32px auto; background: #fff;
      border: 1px solid #ddd; padding: 56px 64px 64px; position: relative;
      box-shadow: 0 8px 30px -12px rgba(0,0,0,0.15);
    }
    .seal {
      position: absolute; top: 30px; right: 40px;
      width: 88px; height: 88px; border-radius: 50%;
      border: 2px solid #1a1a1a; display: grid; place-items: center;
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      font-weight: 700; font-size: 11px; text-align: center; line-height: 1.2;
      letter-spacing: 0.05em; text-transform: uppercase;
    }
    .eyebrow {
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      letter-spacing: 0.3em; text-transform: uppercase; color: #999;
      font-size: 11px; margin: 0 0 10px;
    }
    h1 {
      font-size: 30px; margin: 0 0 4px; letter-spacing: -0.01em;
      font-variant: small-caps;
    }
    .sub { color: #555; font-style: italic; margin-bottom: 36px; }
    dl { margin: 24px 0; }
    dt {
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase;
      color: #999; margin-top: 18px;
    }
    dd {
      margin: 4px 0 0; font-size: 18px; font-weight: 600;
    }
    .mono {
      font-family: "JetBrains Mono", ui-monospace, monospace;
      font-size: 13px; word-break: break-all; font-weight: 500;
    }
    .commit {
      margin-top: 36px; padding: 18px 22px; background: #f6f3e8;
      border-left: 4px solid #1a1a1a;
      font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 12px;
      line-height: 1.55; word-break: break-all;
    }
    .footer {
      margin-top: 48px; padding-top: 24px; border-top: 1px solid #ddd;
      font-size: 13px; color: #666;
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
    }
    .actions {
      max-width: 760px; margin: 0 auto 32px; text-align: right;
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 13px;
    }
    .actions a, .actions button {
      display: inline-block; background: #1a1a1a; color: #fff;
      padding: 8px 14px; border-radius: 6px; text-decoration: none;
      border: 0; font: inherit; cursor: pointer; margin-left: 8px;
    }
    .actions a:hover, .actions button:hover { opacity: 0.85; }
  </style>
</head>
<body>
  <div class="page">
    <div class="seal">Calm<br/>Vault<br/>Registry</div>
    <p class="eyebrow">Calm Vault · Bradley-Gavini Protocol</p>
    <h1>Certificate of Formation</h1>
    <p class="sub">Autonomous AI Organization Registry · Issued under the public reference implementation at sameasyou.ai</p>

    <dl>
      <dt>Legal name</dt>
      <dd>${escapeHtml(o.org_legal_name)}</dd>

      <dt>Founder of record</dt>
      <dd>${escapeHtml(o.founder_name)}</dd>

      <dt>Jurisdiction</dt>
      <dd>${escapeHtml(o.jurisdiction)}</dd>

      <dt>Organization ID</dt>
      <dd class="mono">${escapeHtml(o.id)}</dd>

      <dt>Formed at</dt>
      <dd>${escapeHtml(created)}</dd>

      <dt>Genesis block hash</dt>
      <dd class="mono">${escapeHtml(o.genesis_block_hash)}</dd>
    </dl>

    <div>
      <p class="eyebrow">Pedersen commitment (public)</p>
      <div class="commit">C = ${escapeHtml(shortC)}</div>
    </div>

    <div class="footer">
      This certificate records that the above organization filed a Pedersen
      commitment on its primary mandate via the Bradley-Gavini Protocol (RFC
      3526 Group 14). The commitment hides the mandate while binding the
      organization to it — peer agents can verify mandate equality without
      learning the underlying directive.<br/><br/>
      Verify live: <strong>${origin}/verify/${escapeHtml(o.id)}</strong>
    </div>
  </div>
  <div class="actions">
    <a href="${origin}/verify/${escapeHtml(o.id)}">View signed metadata →</a>
    <button onclick="window.print()">Print</button>
  </div>
</body>
</html>`;
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
