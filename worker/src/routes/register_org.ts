// POST /register-org
//
// Accepts { api_key, org_legal_name, founder_name, jurisdiction, mandate? }.
// Computes a Pedersen commitment on the mandate (commit-and-hide), writes the
// org row + genesis block to D1, and returns:
//
//   - org_id
//   - genesis_block_hash
//   - public_commitment (C, hex)
//   - verifier_url (public)
//
// The mandate may be supplied directly OR fall back to the customer's
// `primary_mandate_commitment` recorded at signup. The Pedersen commitment is
// computed server-side over the string the customer submitted; we store the
// scalar/r privately so the customer can later authorize a reveal if needed.

import type { Env } from "../env";
import { authCustomer } from "../lib/auth";
import { blockHash, type GenesisBlock } from "../lib/chain";
import { jsonResponse, readJson, requireString } from "../lib/http";
import { newOrgId } from "../lib/ids";
import { commit } from "../lib/pedersen";

interface RegisterOrgBody {
  api_key?: unknown;
  org_legal_name?: unknown;
  founder_name?: unknown;
  jurisdiction?: unknown;
  mandate?: unknown;
}

export async function handleRegisterOrg(
  request: Request,
  env: Env,
): Promise<Response> {
  const body = await readJson<RegisterOrgBody>(request);
  const apiKey = requireString(body.api_key, "api_key", { minLen: 32, maxLen: 32 });
  const customer = await authCustomer(env, apiKey);
  const orgLegalName = requireString(body.org_legal_name, "org_legal_name", {
    maxLen: 200,
  });
  const founderName = requireString(body.founder_name, "founder_name", {
    maxLen: 200,
  });
  const jurisdiction = requireString(body.jurisdiction, "jurisdiction", {
    maxLen: 100,
  });
  // Mandate is optional in the request body — fall back to the commitment
  // string captured at signup so a fully scripted onboard works.
  let mandate: string;
  if (body.mandate === undefined || body.mandate === null) {
    mandate = customer.primary_mandate_commitment;
  } else {
    mandate = requireString(body.mandate, "mandate", { maxLen: 4096 });
  }

  const c = await commit(mandate);

  const id = newOrgId();
  const createdAt = Math.floor(Date.now() / 1000);
  const genesis: GenesisBlock = {
    kind: "genesis",
    org_id: id,
    org_legal_name: orgLegalName,
    founder_name: founderName,
    jurisdiction,
    commitment_c: c.c,
    created_at: createdAt,
    prev_hash: null,
  };
  const genesisHash = await blockHash(genesis);

  await env.DB.prepare(
    `INSERT INTO orgs
       (id, customer_id, org_legal_name, founder_name, jurisdiction,
        commitment_c, commitment_r, genesis_block_hash, head_block_hash, created_at)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  )
    .bind(
      id,
      customer.id,
      orgLegalName,
      founderName,
      jurisdiction,
      c.c,
      c.r,
      genesisHash,
      genesisHash,
      createdAt,
    )
    .run();

  return jsonResponse(
    {
      org_id: id,
      org_legal_name: orgLegalName,
      founder_name: founderName,
      jurisdiction,
      public_commitment: c.c,
      genesis_block_hash: genesisHash,
      verifier_url: `${env.PUBLIC_ORIGIN}/verify/${id}`,
      attest_url: `${env.PUBLIC_ORIGIN}/attest`,
      created_at: createdAt,
      protocol: {
        name: "Bradley-Gavini",
        version: "v0",
        group: "RFC3526-group14",
        reference: "https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/protocol.py",
      },
    },
    201,
  );
}


