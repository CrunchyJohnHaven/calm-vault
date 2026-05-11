// GET /verify/:org_id  — public; returns commitment + signed metadata
// GET /verify/keys     — public; returns the server's Ed25519 public key
//
// Anyone (especially peer agents) can fetch /verify/{org_id} and run the
// Bradley-Gavini equality proof against their own org by combining the
// returned `public_commitment` with the matching proof material they have
// out-of-band.

import type { Env } from "../env";
import { canonicalJsonStringify } from "../lib/hex";
import { errorResponse, jsonResponse } from "../lib/http";
import { getPublicKeyB64, signCanonical } from "../lib/signing";

// Cap how many attestation blocks we sign per /verify call. The signed payload
// is over canonical JSON, so an unbounded attestation history would let any
// public caller force an arbitrarily expensive request. 200 covers reasonable
// orgs; callers that need the full chain should paginate against /verify or
// the (future) /verify/<id>/attestations endpoint.
const VERIFY_ATTESTATION_LIMIT = 200;

interface OrgRow {
  id: string;
  customer_id: string;
  org_legal_name: string;
  founder_name: string;
  jurisdiction: string;
  commitment_c: string;
  genesis_block_hash: string;
  head_block_hash: string;
  created_at: number;
}

interface AttestationRow {
  id: string;
  attester_org_id: string;
  target_org_id: string;
  attestation_kind: string;
  signature: string;
  prev_hash: string;
  block_hash: string;
  created_at: number;
}

export async function handleVerify(
  env: Env,
  orgId: string,
): Promise<Response> {
  if (orgId === "keys") {
    const pub = await getPublicKeyB64(env);
    return jsonResponse({
      algorithm: "Ed25519",
      public_key_b64: pub,
      key_format: "raw-32-bytes",
      verify: "Verify the `signed_metadata.signature` field on a /verify/<org_id> response using this public key.",
    });
  }

  const org = await env.DB.prepare(
    `SELECT id, customer_id, org_legal_name, founder_name, jurisdiction,
            commitment_c, genesis_block_hash, head_block_hash, created_at
       FROM orgs
      WHERE id = ?`,
  )
    .bind(orgId)
    .first<OrgRow>();
  if (!org) {
    return errorResponse(404, "org_not_found", `No org found for id ${orgId}.`);
  }

  const attestations = await env.DB.prepare(
    `SELECT id, attester_org_id, target_org_id, attestation_kind, signature,
            prev_hash, block_hash, created_at
       FROM attestations
      WHERE target_org_id = ?
      ORDER BY created_at ASC, id ASC
      LIMIT ?`,
  )
    .bind(orgId, VERIFY_ATTESTATION_LIMIT)
    .all<AttestationRow>();
  const attestationRows = attestations.results ?? [];
  const truncated = attestationRows.length >= VERIFY_ATTESTATION_LIMIT;

  const metadata = {
    org_id: org.id,
    org_legal_name: org.org_legal_name,
    founder_name: org.founder_name,
    jurisdiction: org.jurisdiction,
    public_commitment: org.commitment_c,
    genesis_block_hash: org.genesis_block_hash,
    head_block_hash: org.head_block_hash,
    created_at: org.created_at,
    protocol: {
      name: "Bradley-Gavini",
      version: "v0",
      group: "RFC3526-group14",
      reference:
        "https://github.com/CrunchyJohnHaven/calm-vault/blob/main/calm_pact/protocol.py",
    },
    attestations: attestationRows.map((a) => ({
      id: a.id,
      attester_org_id: a.attester_org_id,
      attestation_kind: a.attestation_kind,
      signature: a.signature,
      prev_hash: a.prev_hash,
      block_hash: a.block_hash,
      created_at: a.created_at,
    })),
    attestation_limit: VERIFY_ATTESTATION_LIMIT,
    attestations_truncated: truncated,
  };
  const canonical = canonicalJsonStringify(metadata);
  const signature = await signCanonical(env, canonical);
  const pub = await getPublicKeyB64(env);

  return jsonResponse({
    metadata,
    signed_metadata: {
      canonical_json: canonical,
      signature,
      algorithm: "Ed25519",
      public_key_b64: pub,
      keys_url: `${env.PUBLIC_ORIGIN}/verify/keys`,
    },
  });
}
