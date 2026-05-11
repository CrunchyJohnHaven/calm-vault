// GET /orgs?cursor=<created_at>&limit=<n>
//
// Public org directory. Paginated by created_at descending. Returns only the
// fields safe for public exposure (no commitment_r, no customer_id).

import type { Env } from "../env";
import { jsonResponse } from "../lib/http";

interface DirRow {
  id: string;
  org_legal_name: string;
  jurisdiction: string;
  public_commitment: string;
  genesis_block_hash: string;
  head_block_hash: string;
  created_at: number;
  attestations_count: number;
}

const MAX_LIMIT = 100;
const DEFAULT_LIMIT = 25;

export async function handleOrgsList(
  request: Request,
  env: Env,
): Promise<Response> {
  const url = new URL(request.url);
  const limitRaw = parseInt(url.searchParams.get("limit") || "", 10);
  const limit = Number.isFinite(limitRaw)
    ? Math.max(1, Math.min(limitRaw, MAX_LIMIT))
    : DEFAULT_LIMIT;
  const cursorRaw = url.searchParams.get("cursor");
  const cursor = cursorRaw ? parseInt(cursorRaw, 10) : null;

  let stmt: D1PreparedStatement;
  if (cursor !== null && Number.isFinite(cursor)) {
    stmt = env.DB.prepare(
      `SELECT o.id, o.org_legal_name, o.jurisdiction, o.commitment_c AS public_commitment,
              o.genesis_block_hash, o.head_block_hash, o.created_at,
              (SELECT COUNT(*) FROM attestations a WHERE a.target_org_id = o.id) AS attestations_count
         FROM orgs o
        WHERE o.created_at < ?
        ORDER BY o.created_at DESC, o.id DESC
        LIMIT ?`,
    ).bind(cursor, limit + 1);
  } else {
    stmt = env.DB.prepare(
      `SELECT o.id, o.org_legal_name, o.jurisdiction, o.commitment_c AS public_commitment,
              o.genesis_block_hash, o.head_block_hash, o.created_at,
              (SELECT COUNT(*) FROM attestations a WHERE a.target_org_id = o.id) AS attestations_count
         FROM orgs o
        ORDER BY o.created_at DESC, o.id DESC
        LIMIT ?`,
    ).bind(limit + 1);
  }
  const res = await stmt.all<DirRow>();
  const rows = (res.results ?? []).slice(0, limit);
  const next =
    (res.results ?? []).length > limit ? rows[rows.length - 1]!.created_at : null;
  return jsonResponse({
    orgs: rows.map((r) => ({
      org_id: r.id,
      org_legal_name: r.org_legal_name,
      jurisdiction: r.jurisdiction,
      public_commitment: r.public_commitment,
      genesis_block_hash: r.genesis_block_hash,
      head_block_hash: r.head_block_hash,
      attestations_count: r.attestations_count,
      created_at: r.created_at,
      verifier_url: `${env.PUBLIC_ORIGIN}/verify/${r.id}`,
      certificate_url: `${env.PUBLIC_ORIGIN}/certificate/${r.id}`,
    })),
    limit,
    next_cursor: next,
  });
}
