// POST /attest
//
// Accepts { api_key, target_org_id, attestation_kind, signature }.
// Records a peer attestation block on the target org's chain. The attester is
// derived from api_key → customer → that customer's most-recently-registered
// org (or the org_id specified explicitly via `as_org_id`).

import type { Env } from "../env";
import { authCustomer } from "../lib/auth";
import { blockHash, type AttestationBlock } from "../lib/chain";
import { HttpError, jsonResponse, readJson, requireString } from "../lib/http";
import { newAttestationId } from "../lib/ids";

interface AttestBody {
  api_key?: unknown;
  target_org_id?: unknown;
  attestation_kind?: unknown;
  signature?: unknown;
  as_org_id?: unknown;
}

// Allow-list of attestation kinds. We deliberately keep this small so the
// public chain stays interpretable; new kinds can be added in later migrations.
const ATTESTATION_KINDS = new Set([
  "mandate_equality",   // I ran Bradley-Gavini and the equality proof verified.
  "mandate_alignment",  // I assert categorical alignment without a formal proof.
  "endorsement",        // Open-ended endorsement.
  "delegation",         // I delegated authority to the target org.
  "dispute",            // I dispute the target org's published commitment.
]);

export async function handleAttest(
  request: Request,
  env: Env,
): Promise<Response> {
  const body = await readJson<AttestBody>(request);
  const apiKey = requireString(body.api_key, "api_key", { minLen: 32, maxLen: 32 });
  const targetOrgId = requireString(body.target_org_id, "target_org_id", {
    maxLen: 64,
  });
  const kind = requireString(body.attestation_kind, "attestation_kind", {
    maxLen: 64,
  });
  if (!ATTESTATION_KINDS.has(kind)) {
    throw new HttpError(
      400,
      "invalid_attestation_kind",
      `attestation_kind must be one of: ${[...ATTESTATION_KINDS].join(", ")}`,
    );
  }
  const signature = requireString(body.signature, "signature", { maxLen: 4096 });
  const asOrgId =
    body.as_org_id === undefined || body.as_org_id === null
      ? undefined
      : requireString(body.as_org_id, "as_org_id", { maxLen: 64 });

  const customer = await authCustomer(env, apiKey);

  // Resolve the attester org: explicit as_org_id if provided + owned by this
  // customer, else the customer's most recent org.
  let attesterOrgId: string;
  if (asOrgId !== undefined) {
    const owned = await env.DB.prepare(
      "SELECT id FROM orgs WHERE id = ? AND customer_id = ?",
    )
      .bind(asOrgId, customer.id)
      .first<{ id: string }>();
    if (!owned) {
      throw new HttpError(
        403,
        "org_not_owned",
        "as_org_id is not owned by the authenticated customer.",
      );
    }
    attesterOrgId = owned.id;
  } else {
    const latest = await env.DB.prepare(
      `SELECT id FROM orgs WHERE customer_id = ? ORDER BY created_at DESC LIMIT 1`,
    )
      .bind(customer.id)
      .first<{ id: string }>();
    if (!latest) {
      throw new HttpError(
        409,
        "no_org_registered",
        "Register an org with POST /register-org before attesting.",
      );
    }
    attesterOrgId = latest.id;
  }

  if (attesterOrgId === targetOrgId) {
    throw new HttpError(
      400,
      "self_attestation",
      "An org cannot attest against itself.",
    );
  }

  // Look up the target org (must exist).
  const target = await env.DB.prepare(
    `SELECT id, head_block_hash FROM orgs WHERE id = ?`,
  )
    .bind(targetOrgId)
    .first<{ id: string; head_block_hash: string }>();
  if (!target) {
    throw new HttpError(
      404,
      "target_not_found",
      "target_org_id does not match any registered org.",
    );
  }

  const createdAt = Math.floor(Date.now() / 1000);
  const block: AttestationBlock = {
    kind: "attestation",
    attester_org_id: attesterOrgId,
    target_org_id: targetOrgId,
    attestation_kind: kind,
    signature,
    prev_hash: target.head_block_hash,
    created_at: createdAt,
  };
  const hash = await blockHash(block);
  const id = newAttestationId();

  // Append the attestation and advance the target's chain head atomically.
  // D1 batch() is transactional within a single call; the UPDATE's WHERE clause
  // also gives us optimistic concurrency in case two attestations race against
  // the same head_block_hash.
  const batchResult = await env.DB.batch([
    env.DB.prepare(
      `INSERT INTO attestations
         (id, attester_org_id, target_org_id, attestation_kind, signature, prev_hash, block_hash, created_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    ).bind(
      id,
      attesterOrgId,
      targetOrgId,
      kind,
      signature,
      target.head_block_hash,
      hash,
      createdAt,
    ),
    env.DB.prepare(
      `UPDATE orgs SET head_block_hash = ? WHERE id = ? AND head_block_hash = ?`,
    ).bind(hash, targetOrgId, target.head_block_hash),
  ]);
  // Defend against the racy case where the UPDATE matched zero rows because
  // another attestation slipped in between our SELECT and the batch. Callers
  // can safely retry.
  const updateMeta = batchResult[1]?.meta as
    | { changes?: number; rows_written?: number }
    | undefined;
  const updateChanges =
    updateMeta?.changes ?? updateMeta?.rows_written ?? undefined;
  if (updateChanges === 0) {
    throw new HttpError(
      409,
      "chain_head_advanced",
      "Target chain advanced concurrently; retry the attestation.",
    );
  }

  return jsonResponse(
    {
      attestation_id: id,
      attester_org_id: attesterOrgId,
      target_org_id: targetOrgId,
      attestation_kind: kind,
      prev_hash: target.head_block_hash,
      block_hash: hash,
      created_at: createdAt,
      verifier_url: `${env.PUBLIC_ORIGIN}/verify/${targetOrgId}`,
    },
    201,
  );
}
