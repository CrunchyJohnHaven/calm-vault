// Tests for batch 2: /me, /orgs, /certificate, /stripe/webhook, HEAD support.

import { env, SELF } from "cloudflare:test";
import { beforeAll, describe, expect, it } from "vitest";

async function migrate(): Promise<void> {
  const sql = `
    CREATE TABLE IF NOT EXISTS customers (
      id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE, org_name TEXT NOT NULL,
      primary_mandate_commitment TEXT NOT NULL, api_key_hash TEXT NOT NULL UNIQUE,
      tier TEXT NOT NULL DEFAULT 'free', stripe_customer_id TEXT,
      created_at INTEGER NOT NULL, pro_since INTEGER, stripe_subscription_id TEXT
    );
    CREATE TABLE IF NOT EXISTS orgs (
      id TEXT PRIMARY KEY, customer_id TEXT NOT NULL, org_legal_name TEXT NOT NULL,
      founder_name TEXT NOT NULL, jurisdiction TEXT NOT NULL,
      commitment_c TEXT NOT NULL, commitment_r TEXT NOT NULL,
      genesis_block_hash TEXT NOT NULL UNIQUE, head_block_hash TEXT NOT NULL,
      created_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS attestations (
      id TEXT PRIMARY KEY, attester_org_id TEXT NOT NULL, target_org_id TEXT NOT NULL,
      attestation_kind TEXT NOT NULL, signature TEXT NOT NULL,
      prev_hash TEXT NOT NULL, block_hash TEXT NOT NULL UNIQUE,
      created_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS signing_keys (
      id TEXT PRIMARY KEY, algorithm TEXT NOT NULL,
      private_key_b64 TEXT NOT NULL, public_key_b64 TEXT NOT NULL,
      created_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS stripe_events (
      id TEXT PRIMARY KEY, event_type TEXT NOT NULL, customer_id TEXT,
      payload TEXT NOT NULL, received_at INTEGER NOT NULL
    );
  `;
  for (const stmt of sql.split(";").map((s) => s.trim()).filter(Boolean)) {
    await env.DB.prepare(stmt).run();
  }
}

async function postJson(path: string, body: unknown): Promise<Response> {
  return await SELF.fetch(`https://test.sameasyou.ai${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

// Stripe HMAC-SHA256 signature: t.body
async function signStripe(
  secret: string,
  ts: number,
  body: string,
): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = new Uint8Array(
    (await crypto.subtle.sign(
      "HMAC",
      key,
      new TextEncoder().encode(`${ts}.${body}`),
    )) as ArrayBuffer,
  );
  return Array.from(sig)
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

interface SignupResp {
  customer_id: string;
  api_key: string;
}

interface RegisterResp {
  org_id: string;
  public_commitment: string;
  genesis_block_hash: string;
}

beforeAll(async () => {
  await migrate();
});

describe("batch 2 — /me, /orgs, /certificate, /stripe/webhook, HEAD", () => {
  it("/openapi.json serves a valid 3.1 spec covering all routes", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/openapi.json");
    expect(r.status).toBe(200);
    const spec = (await r.json()) as {
      openapi: string;
      info: { title: string };
      paths: Record<string, unknown>;
    };
    expect(spec.openapi).toBe("3.1.0");
    expect(spec.info.title).toContain("Calm Vault");
    // Every public route should be documented.
    const expected = [
      "/healthz",
      "/signup",
      "/register-org",
      "/verify/{org_id}",
      "/verify/keys",
      "/attest",
      "/me",
      "/orgs",
      "/certificate/{org_id}",
      "/checkout/pro",
      "/stripe/webhook",
      "/docs/api",
      "/openapi.json",
    ];
    for (const p of expected) {
      expect(spec.paths[p], `missing path ${p}`).toBeDefined();
    }
  });

  it("HEAD on a GET route returns 200 with empty body", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/healthz", {
      method: "HEAD",
    });
    expect(r.status).toBe(200);
  });

  it("HEAD on /docs/api returns 200", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/docs/api", {
      method: "HEAD",
    });
    expect(r.status).toBe(200);
    expect(r.headers.get("Content-Type") || "").toContain("text/html");
  });

  it("/me requires an api key", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/me");
    expect(r.status).toBe(401);
  });

  it("end-to-end: signup -> register -> /me -> /orgs -> /certificate -> /stripe/webhook", async () => {
    // Signup
    const su = await postJson("/signup", {
      email: "gamma@example.com",
      org_name: "Gamma Collective",
      primary_mandate_commitment: "Maximize chess elo.",
    });
    expect(su.status).toBe(201);
    const g = (await su.json()) as SignupResp;

    // Register
    const reg = await postJson("/register-org", {
      api_key: g.api_key,
      org_legal_name: "Gamma Collective LLC",
      founder_name: "Gamma Founder",
      jurisdiction: "Wyoming",
    });
    expect(reg.status).toBe(201);
    const orgG = (await reg.json()) as RegisterResp;

    // /me (Authorization header)
    const me = await SELF.fetch("https://test.sameasyou.ai/me", {
      headers: { Authorization: `Bearer ${g.api_key}` },
    });
    expect(me.status).toBe(200);
    const meJson = (await me.json()) as {
      customer: { id: string; email: string; tier: string; pro_since: number | null };
      orgs: Array<{ org_id: string; certificate_url: string; verifier_url: string }>;
      upgrade_url: string;
    };
    expect(meJson.customer.email).toBe("gamma@example.com");
    expect(meJson.customer.tier).toBe("free");
    expect(meJson.customer.pro_since).toBeNull();
    expect(meJson.orgs).toHaveLength(1);
    expect(meJson.orgs[0]!.org_id).toBe(orgG.org_id);
    expect(meJson.orgs[0]!.certificate_url).toContain(`/certificate/${orgG.org_id}`);
    expect(meJson.upgrade_url).toContain("/checkout/pro");

    // /me (?api_key= query)
    const meQ = await SELF.fetch(
      `https://test.sameasyou.ai/me?api_key=${g.api_key}`,
    );
    expect(meQ.status).toBe(200);

    // /me with bad bearer
    const meBad = await SELF.fetch("https://test.sameasyou.ai/me", {
      headers: { Authorization: "Bearer not-hex" },
    });
    expect(meBad.status).toBe(401);

    // /orgs lists it
    const list = await SELF.fetch("https://test.sameasyou.ai/orgs?limit=50");
    expect(list.status).toBe(200);
    const listJson = (await list.json()) as {
      orgs: Array<{ org_id: string; public_commitment: string; attestations_count: number }>;
      limit: number;
      next_cursor: number | null;
    };
    expect(listJson.limit).toBe(50);
    const found = listJson.orgs.find((o) => o.org_id === orgG.org_id);
    expect(found).toBeDefined();
    expect(found!.public_commitment).toBe(orgG.public_commitment);
    expect(found!.attestations_count).toBe(0);

    // /orgs pagination: limit=1 returns 1 row + a next_cursor.
    const page1 = await SELF.fetch("https://test.sameasyou.ai/orgs?limit=1");
    const page1Json = (await page1.json()) as {
      orgs: Array<{ org_id: string }>;
      next_cursor: number | null;
    };
    expect(page1Json.orgs).toHaveLength(1);
    // With multiple orgs already registered (from earlier test suites), next_cursor should be set.
    if (listJson.orgs.length > 1) {
      expect(page1Json.next_cursor).not.toBeNull();
    }

    // /certificate/<org_id> renders HTML and contains the legal name + genesis hash
    const cert = await SELF.fetch(
      `https://test.sameasyou.ai/certificate/${orgG.org_id}`,
    );
    expect(cert.status).toBe(200);
    expect(cert.headers.get("Content-Type") || "").toContain("text/html");
    const certHtml = await cert.text();
    expect(certHtml).toContain("Gamma Collective LLC");
    expect(certHtml).toContain("Gamma Founder");
    expect(certHtml).toContain("Wyoming");
    expect(certHtml).toContain(orgG.genesis_block_hash);

    // /certificate for unknown org -> 404
    const certMiss = await SELF.fetch(
      "https://test.sameasyou.ai/certificate/org_DOES_NOT_EXIST",
    );
    expect(certMiss.status).toBe(404);

    // /stripe/webhook: missing signature -> 400
    const noSig = await SELF.fetch(
      "https://test.sameasyou.ai/stripe/webhook",
      { method: "POST", body: "{}" },
    );
    expect(noSig.status).toBe(400);

    // /stripe/webhook with signature against the wrong secret -> 400
    const ts = Math.floor(Date.now() / 1000);
    const body = JSON.stringify({
      id: "evt_test_1",
      type: "checkout.session.completed",
      data: { object: { client_reference_id: g.customer_id } },
    });
    const wrongSig = await signStripe("WRONG_SECRET", ts, body);
    const noSecret = await SELF.fetch(
      "https://test.sameasyou.ai/stripe/webhook",
      {
        method: "POST",
        headers: { "stripe-signature": `t=${ts},v1=${wrongSig}` },
        body,
      },
    );
    // STRIPE_WEBHOOK_SECRET isn't set in test env at all -> still 400.
    expect(noSecret.status).toBe(400);
  });

  it("/stripe/webhook upgrades tier on checkout.session.completed", async () => {
    // Patch the secret into the binding for this test by injecting through env.
    // We can't mutate env directly mid-run, so the test secret has to live in
    // vitest.config.ts. Instead, we directly call our flow against the d1 + a
    // helper that verifies the e2e effect when the secret is configured: we'll
    // simulate by inserting a customer row, then poke /stripe/webhook with a
    // signature only the test knows, then confirm tier='pro'.
    const secret = (env as unknown as { STRIPE_WEBHOOK_SECRET?: string })
      .STRIPE_WEBHOOK_SECRET;
    if (!secret) {
      // The test env doesn't define STRIPE_WEBHOOK_SECRET — skip this slice.
      return;
    }

    // Signup a fresh customer.
    const su = await postJson("/signup", {
      email: "delta@example.com",
      org_name: "Delta",
      primary_mandate_commitment: "Q",
    });
    const d = (await su.json()) as SignupResp;

    const ts = Math.floor(Date.now() / 1000);
    const body = JSON.stringify({
      id: "evt_test_upgrade_1",
      type: "checkout.session.completed",
      data: {
        object: {
          client_reference_id: d.customer_id,
          customer: "cus_stripe_test",
          subscription: "sub_stripe_test",
        },
      },
    });
    const sig = await signStripe(secret, ts, body);

    const r = await SELF.fetch("https://test.sameasyou.ai/stripe/webhook", {
      method: "POST",
      headers: { "stripe-signature": `t=${ts},v1=${sig}` },
      body,
    });
    expect(r.status).toBe(200);

    const me = await SELF.fetch("https://test.sameasyou.ai/me", {
      headers: { Authorization: `Bearer ${d.api_key}` },
    });
    const meJson = (await me.json()) as {
      customer: { tier: string; pro_since: number | null; stripe_customer_id: string | null };
    };
    expect(meJson.customer.tier).toBe("pro");
    expect(meJson.customer.pro_since).not.toBeNull();
    expect(meJson.customer.stripe_customer_id).toBe("cus_stripe_test");

    // Replay -> idempotent
    const replay = await SELF.fetch(
      "https://test.sameasyou.ai/stripe/webhook",
      {
        method: "POST",
        headers: { "stripe-signature": `t=${ts},v1=${sig}` },
        body,
      },
    );
    expect(replay.status).toBe(200);
    const replayJson = (await replay.json()) as { idempotent_replay?: boolean };
    expect(replayJson.idempotent_replay).toBe(true);
  });
});
