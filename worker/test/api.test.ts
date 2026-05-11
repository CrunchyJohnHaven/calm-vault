// End-to-end smoke test for the no-touch platform: signup -> register-org ->
// verify -> attest. Runs inside Miniflare via @cloudflare/vitest-pool-workers
// against an in-memory D1.

import { env, SELF } from "cloudflare:test";
import { beforeAll, describe, expect, it } from "vitest";

async function migrate(): Promise<void> {
  const sql = `
    CREATE TABLE IF NOT EXISTS customers (
      id TEXT PRIMARY KEY,
      email TEXT NOT NULL UNIQUE,
      org_name TEXT NOT NULL,
      primary_mandate_commitment TEXT NOT NULL,
      api_key_hash TEXT NOT NULL UNIQUE,
      tier TEXT NOT NULL DEFAULT 'free',
      stripe_customer_id TEXT,
      created_at INTEGER NOT NULL,
      pro_since INTEGER,
      stripe_subscription_id TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_customers_api_key_hash ON customers(api_key_hash);
    CREATE TABLE IF NOT EXISTS orgs (
      id TEXT PRIMARY KEY,
      customer_id TEXT NOT NULL,
      org_legal_name TEXT NOT NULL,
      founder_name TEXT NOT NULL,
      jurisdiction TEXT NOT NULL,
      commitment_c TEXT NOT NULL,
      commitment_r TEXT NOT NULL,
      genesis_block_hash TEXT NOT NULL UNIQUE,
      head_block_hash TEXT NOT NULL,
      created_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_orgs_customer ON orgs(customer_id);
    CREATE TABLE IF NOT EXISTS attestations (
      id TEXT PRIMARY KEY,
      attester_org_id TEXT NOT NULL,
      target_org_id TEXT NOT NULL,
      attestation_kind TEXT NOT NULL,
      signature TEXT NOT NULL,
      prev_hash TEXT NOT NULL,
      block_hash TEXT NOT NULL UNIQUE,
      created_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_attestations_target ON attestations(target_org_id);
    CREATE INDEX IF NOT EXISTS idx_attestations_attester ON attestations(attester_org_id);
    CREATE TABLE IF NOT EXISTS signing_keys (
      id TEXT PRIMARY KEY,
      algorithm TEXT NOT NULL,
      private_key_b64 TEXT NOT NULL,
      public_key_b64 TEXT NOT NULL,
      created_at INTEGER NOT NULL
    );
    CREATE TABLE IF NOT EXISTS stripe_events (
      id TEXT PRIMARY KEY,
      event_type TEXT NOT NULL,
      customer_id TEXT,
      payload TEXT NOT NULL,
      received_at INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_orgs_created_at ON orgs(created_at);
  `;
  // env.DB is the D1 binding declared in vitest.config.ts.
  // Run each statement individually since D1 batches don't accept multi-stmt strings.
  for (const stmt of sql.split(";").map((s) => s.trim()).filter(Boolean)) {
    await env.DB.prepare(stmt).run();
  }
}

beforeAll(async () => {
  await migrate();
});

async function postJson(path: string, body: unknown): Promise<Response> {
  return await SELF.fetch(`https://test.sameasyou.ai${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

describe("no-touch platform flow", () => {
  it("healthz responds ok", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/healthz");
    expect(r.status).toBe(200);
    expect(await r.text()).toBe("ok");
  });

  it("docs/api renders HTML", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/docs/api");
    expect(r.status).toBe(200);
    expect(r.headers.get("Content-Type") || "").toContain("text/html");
    const body = await r.text();
    expect(body).toContain("Calm Vault");
    expect(body).toContain("/register-org");
  });

  it("rejects invalid signup payloads", async () => {
    const r = await postJson("/signup", { email: "not-an-email" });
    expect(r.status).toBe(400);
  });

  it("signup -> register-org -> verify -> attest end-to-end", async () => {
    // 1) Signup
    const signupRes = await postJson("/signup", {
      email: "alpha@example.com",
      org_name: "Alpha Collective",
      primary_mandate_commitment: "Reduce malaria mortality.",
    });
    expect(signupRes.status).toBe(201);
    const alpha = (await signupRes.json()) as {
      customer_id: string;
      api_key: string;
      next_step: string;
      upgrade_url: string;
    };
    expect(alpha.api_key).toMatch(/^[0-9a-f]{32}$/);
    expect(alpha.next_step).toContain("/register-org");

    const signupRes2 = await postJson("/signup", {
      email: "beta@example.com",
      org_name: "Beta Collective",
      primary_mandate_commitment: "Reduce malaria mortality.",
    });
    expect(signupRes2.status).toBe(201);
    const beta = (await signupRes2.json()) as { api_key: string };

    // Duplicate email is rejected.
    const dup = await postJson("/signup", {
      email: "alpha@example.com",
      org_name: "x",
      primary_mandate_commitment: "y",
    });
    expect(dup.status).toBe(409);

    // 2) Register org for alpha
    const regA = await postJson("/register-org", {
      api_key: alpha.api_key,
      org_legal_name: "Alpha Collective LLC",
      founder_name: "Alpha Founder",
      jurisdiction: "Delaware",
    });
    expect(regA.status).toBe(201);
    const orgA = (await regA.json()) as {
      org_id: string;
      public_commitment: string;
      genesis_block_hash: string;
      verifier_url: string;
    };
    expect(orgA.org_id).toMatch(/^org_/);
    expect(orgA.public_commitment).toMatch(/^[0-9a-f]+$/);
    expect(orgA.genesis_block_hash).toMatch(/^[0-9a-f]{64}$/);
    expect(orgA.verifier_url).toContain("/verify/");

    // Register org for beta
    const regB = await postJson("/register-org", {
      api_key: beta.api_key,
      org_legal_name: "Beta Collective LLC",
      founder_name: "Beta Founder",
      jurisdiction: "Delaware",
    });
    expect(regB.status).toBe(201);
    const orgB = (await regB.json()) as {
      org_id: string;
      genesis_block_hash: string;
    };

    // Invalid api key on register
    const bad = await postJson("/register-org", {
      api_key: "00000000000000000000000000000000",
      org_legal_name: "x",
      founder_name: "y",
      jurisdiction: "z",
    });
    expect(bad.status).toBe(401);

    // 3) Verify alpha publicly
    const vA = await SELF.fetch(`https://test.sameasyou.ai${orgA.verifier_url.replace("https://test.sameasyou.ai", "")}`);
    expect(vA.status).toBe(200);
    const verifyJson = (await vA.json()) as {
      metadata: {
        org_id: string;
        public_commitment: string;
        head_block_hash: string;
        attestations: unknown[];
      };
      signed_metadata: {
        canonical_json: string;
        signature: string;
        algorithm: string;
        public_key_b64: string;
      };
    };
    expect(verifyJson.metadata.org_id).toBe(orgA.org_id);
    expect(verifyJson.metadata.public_commitment).toBe(orgA.public_commitment);
    expect(verifyJson.metadata.head_block_hash).toBe(orgA.genesis_block_hash);
    expect(verifyJson.metadata.attestations).toHaveLength(0);
    expect(verifyJson.signed_metadata.algorithm).toBe("Ed25519");
    expect(verifyJson.signed_metadata.signature.length).toBeGreaterThan(0);

    // Ed25519 signature verifies against the published public key.
    const pubBytes = Uint8Array.from(
      atob(verifyJson.signed_metadata.public_key_b64),
      (c) => c.charCodeAt(0),
    );
    const sigBytes = Uint8Array.from(
      atob(verifyJson.signed_metadata.signature),
      (c) => c.charCodeAt(0),
    );
    const pubKey = await crypto.subtle.importKey(
      "raw",
      pubBytes,
      { name: "Ed25519" },
      false,
      ["verify"],
    );
    const ok = await crypto.subtle.verify(
      "Ed25519",
      pubKey,
      sigBytes,
      new TextEncoder().encode(verifyJson.signed_metadata.canonical_json),
    );
    expect(ok).toBe(true);

    // /verify/keys
    const keysRes = await SELF.fetch("https://test.sameasyou.ai/verify/keys");
    expect(keysRes.status).toBe(200);
    const keysJson = (await keysRes.json()) as { public_key_b64: string };
    expect(keysJson.public_key_b64).toBe(verifyJson.signed_metadata.public_key_b64);

    // 4) Attest: beta attests on alpha.
    const att = await postJson("/attest", {
      api_key: beta.api_key,
      target_org_id: orgA.org_id,
      attestation_kind: "mandate_equality",
      signature: "test-signature-blob",
    });
    expect(att.status).toBe(201);
    const attJson = (await att.json()) as {
      attestation_id: string;
      attester_org_id: string;
      block_hash: string;
      prev_hash: string;
    };
    expect(attJson.attester_org_id).toBe(orgB.org_id);
    expect(attJson.prev_hash).toBe(orgA.genesis_block_hash);
    expect(attJson.block_hash).not.toBe(attJson.prev_hash);

    // Alpha verify now shows the attestation + advanced head.
    const vA2 = await SELF.fetch(`https://test.sameasyou.ai/verify/${orgA.org_id}`);
    const v2 = (await vA2.json()) as {
      metadata: {
        head_block_hash: string;
        attestations: Array<{ block_hash: string; attestation_kind: string }>;
      };
    };
    expect(v2.metadata.head_block_hash).toBe(attJson.block_hash);
    expect(v2.metadata.attestations).toHaveLength(1);
    expect(v2.metadata.attestations[0]!.attestation_kind).toBe("mandate_equality");

    // Self-attestation rejected.
    const self = await postJson("/attest", {
      api_key: alpha.api_key,
      target_org_id: orgA.org_id,
      attestation_kind: "endorsement",
      signature: "x",
    });
    expect(self.status).toBe(400);

    // Unknown attestation_kind rejected.
    const badKind = await postJson("/attest", {
      api_key: beta.api_key,
      target_org_id: orgA.org_id,
      attestation_kind: "totally-made-up",
      signature: "x",
    });
    expect(badKind.status).toBe(400);

    // Unknown target rejected.
    const noTarget = await postJson("/attest", {
      api_key: beta.api_key,
      target_org_id: "org_DOES_NOT_EXIST",
      attestation_kind: "endorsement",
      signature: "x",
    });
    expect(noTarget.status).toBe(404);
  });

  it("verify returns 404 for an unknown org", async () => {
    const r = await SELF.fetch(
      "https://test.sameasyou.ai/verify/org_DOES_NOT_EXIST",
    );
    expect(r.status).toBe(404);
  });

  it("/checkout/pro redirects to the Stripe Payment Link", async () => {
    const r = await SELF.fetch("https://test.sameasyou.ai/checkout/pro", {
      redirect: "manual",
    });
    expect(r.status).toBe(302);
    expect(r.headers.get("Location") || "").toContain("buy.stripe.com");
  });
});
