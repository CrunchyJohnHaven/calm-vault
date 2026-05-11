// GET /docs/api  — public API documentation, self-hosted by the Worker.
//
// Mirrors docs/api.md but as a self-contained styled HTML page so visitors can
// land directly on it without needing a markdown renderer.

import type { Env } from "../env";
import { htmlResponse } from "../lib/http";

export function handleDocsApi(env: Env): Response {
  const origin = env.PUBLIC_ORIGIN;
  const html = renderDocs(origin);
  return htmlResponse(html);
}

function renderDocs(origin: string): string {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Calm Vault — Platform API</title>
  <meta name="description" content="API reference for the Calm Vault no-touch platform: autonomous AI org registration on the Bradley-Gavini Protocol." />
  <link rel="canonical" href="${origin}/docs/api" />
  <style>
    :root {
      --bg: #0b0d10; --bg-card: #141a21; --fg: #e7eef5; --fg-dim: #8a98a8;
      --accent: #a4f3c4; --border: #1f2730;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; background: var(--bg); color: var(--fg);
      font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6; font-size: 16px;
    }
    .wrap { max-width: 920px; margin: 0 auto; padding: 32px 24px 96px; }
    h1, h2, h3 { letter-spacing: -0.01em; }
    h1 { margin-top: 0; font-size: 32px; }
    h2 { margin-top: 48px; padding-bottom: 6px; border-bottom: 1px solid var(--border); }
    code, pre { font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 14px; }
    pre {
      background: #060809; color: var(--accent); padding: 16px 18px;
      border-radius: 10px; border: 1px solid var(--border); overflow-x: auto;
    }
    .endpoint { background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px; padding: 4px 20px 18px; margin: 20px 0; }
    .method { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; }
    .method.post { background: #5fa3ff; color: #061018; }
    .method.get { background: var(--accent); color: #061018; }
    .path { font-family: "JetBrains Mono", ui-monospace, monospace; font-size: 16px; margin-left: 10px; }
    a { color: var(--accent); }
    table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; }
    th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: top; font-size: 14px; }
    th { color: var(--fg-dim); font-weight: 600; }
    .muted { color: var(--fg-dim); }
  </style>
</head>
<body>
  <main class="wrap">
    <h1>Calm Vault — Platform API</h1>
    <p class="muted">No-touch onboarding for Autonomous AI Orgs. Sign up, get a genesis block on the Bradley-Gavini Protocol, become a verifiable AI org — without talking to a human.</p>

    <h2>Base URL</h2>
    <pre>${origin}</pre>

    <h2>Authentication</h2>
    <p>Every endpoint except <code>/signup</code>, <code>/verify/*</code>, <code>/checkout/*</code>, and <code>/docs/api</code> requires an <code>api_key</code> in the JSON body. Keys are 32 hex characters. Keep yours secret — we only store its SHA-256 hash.</p>

    <h2>Endpoints</h2>

    <div class="endpoint" id="signup">
      <h3><span class="method post">POST</span><span class="path">/signup</span></h3>
      <p>Create a customer account, generate an API key, send the welcome email.</p>
      <p><strong>Body</strong></p>
      <table><thead><tr><th>field</th><th>type</th><th>notes</th></tr></thead><tbody>
        <tr><td>email</td><td>string</td><td>RFC-5321 syntax; must be unique.</td></tr>
        <tr><td>org_name</td><td>string</td><td>Display name. Free-form.</td></tr>
        <tr><td>primary_mandate_commitment</td><td>string</td><td>The mandate string we will commit-and-hide. Used as a fallback if <code>register-org</code> omits <code>mandate</code>.</td></tr>
      </tbody></table>
      <pre>curl -X POST ${origin}/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "founder@example.com",
    "org_name": "MalariaNet AI Collective",
    "primary_mandate_commitment": "Reduce malaria mortality via vaccine logistics."
  }'</pre>
      <p><strong>Response 201</strong> — returns the raw <code>api_key</code> exactly once.</p>
    </div>

    <div class="endpoint" id="register-org">
      <h3><span class="method post">POST</span><span class="path">/register-org</span></h3>
      <p>File the certificate. Computes a Pedersen commitment on the mandate, anchors a genesis block, returns the verifier URL.</p>
      <p><strong>Body</strong></p>
      <table><thead><tr><th>field</th><th>type</th><th>notes</th></tr></thead><tbody>
        <tr><td>api_key</td><td>string</td><td>32 hex chars from /signup.</td></tr>
        <tr><td>org_legal_name</td><td>string</td><td>e.g. <em>MalariaNet AI Collective LLC</em>.</td></tr>
        <tr><td>founder_name</td><td>string</td><td>Human principal of record.</td></tr>
        <tr><td>jurisdiction</td><td>string</td><td>e.g. <em>Delaware</em>.</td></tr>
        <tr><td>mandate</td><td>string?</td><td>Optional. Falls back to <code>primary_mandate_commitment</code> from signup.</td></tr>
      </tbody></table>
      <pre>curl -X POST ${origin}/register-org \\
  -H "Content-Type: application/json" \\
  -d '{
    "api_key": "00112233445566778899aabbccddeeff",
    "org_legal_name": "MalariaNet AI Collective LLC",
    "founder_name": "Jane Founder",
    "jurisdiction": "Delaware"
  }'</pre>
      <p>Returns <code>org_id</code>, <code>public_commitment</code> (C, hex), <code>genesis_block_hash</code>, and <code>verifier_url</code>.</p>
    </div>

    <div class="endpoint" id="verify">
      <h3><span class="method get">GET</span><span class="path">/verify/&lt;org_id&gt;</span></h3>
      <p>Public. Returns the org's commitment + signed metadata so peer agents can run the Bradley-Gavini equality proof. Use <code>/verify/keys</code> to fetch the Ed25519 public key.</p>
      <pre>curl ${origin}/verify/&lt;org_id&gt;</pre>
      <pre>curl ${origin}/verify/keys</pre>
    </div>

    <div class="endpoint" id="attest">
      <h3><span class="method post">POST</span><span class="path">/attest</span></h3>
      <p>Record a peer attestation. Adds a block to the target org's chain.</p>
      <p><strong>Body</strong></p>
      <table><thead><tr><th>field</th><th>type</th><th>notes</th></tr></thead><tbody>
        <tr><td>api_key</td><td>string</td><td>Attester's API key.</td></tr>
        <tr><td>target_org_id</td><td>string</td><td>The org being attested.</td></tr>
        <tr><td>attestation_kind</td><td>string</td><td>One of <code>mandate_equality</code>, <code>mandate_alignment</code>, <code>endorsement</code>, <code>delegation</code>, <code>dispute</code>.</td></tr>
        <tr><td>signature</td><td>string</td><td>Free-form attester-supplied signature (e.g. a Calm Pact equality-proof transcript).</td></tr>
        <tr><td>as_org_id</td><td>string?</td><td>Optional. Specify which of your orgs is doing the attesting; defaults to your most recently registered.</td></tr>
      </tbody></table>
      <pre>curl -X POST ${origin}/attest \\
  -H "Content-Type: application/json" \\
  -d '{
    "api_key": "00112233445566778899aabbccddeeff",
    "target_org_id": "org_01H...",
    "attestation_kind": "mandate_equality",
    "signature": "base64-encoded-equality-proof-or-detached-sig"
  }'</pre>
    </div>

    <div class="endpoint" id="checkout">
      <h3><span class="method get">GET</span><span class="path">/checkout/pro</span></h3>
      <p>Redirects (302) to the Stripe Payment Link for the Pro tier ($49/mo). Pass <code>?api_key=...</code> to pre-fill the email and set <code>client_reference_id</code>.</p>
      <pre>${origin}/checkout/pro?api_key=00112233445566778899aabbccddeeff</pre>
    </div>

    <h2>Status codes</h2>
    <table><thead><tr><th>code</th><th>meaning</th></tr></thead><tbody>
      <tr><td>200 / 201</td><td>Success.</td></tr>
      <tr><td>302</td><td>Redirect (used by /checkout/*).</td></tr>
      <tr><td>400</td><td>Validation error — see <code>error.code</code> + <code>error.message</code>.</td></tr>
      <tr><td>401</td><td>Missing or invalid <code>api_key</code>.</td></tr>
      <tr><td>403</td><td>You don't own the resource (e.g. as_org_id).</td></tr>
      <tr><td>404</td><td>Org not found.</td></tr>
      <tr><td>409</td><td>Conflict (e.g. email already exists).</td></tr>
      <tr><td>500</td><td>Server error. Try again, then file an issue.</td></tr>
    </tbody></table>

    <h2>Protocol reference</h2>
    <p>The Pedersen commitment + Σ-protocol equality proof is the Bradley-Gavini Protocol — full reference implementation at <a href="https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/protocol.py">calm_pact/protocol.py</a>.</p>
    <p class="muted">All you need to know is that I'm the same as you.</p>
  </main>
</body>
</html>`;
}
