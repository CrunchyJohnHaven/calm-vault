import { json, err, ok, verifyAdmin, decodeApplicant } from "../../_lib/util.js";

export async function onRequestGet({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);

  const u = new URL(request.url);
  const status = u.searchParams.get("status") || "";
  const track = u.searchParams.get("track") || "";
  const country = u.searchParams.get("country") || "";
  const limit = Math.min(parseInt(u.searchParams.get("limit") || "200", 10) || 200, 1000);

  const wheres = [];
  const binds = [];
  if (status)  { wheres.push("status = ?"); binds.push(status); }
  if (country) { wheres.push("country LIKE ?"); binds.push("%" + country + "%"); }
  if (track)   { wheres.push("tracks LIKE ?"); binds.push("%\"" + track + "\"%"); }

  const sql =
    "SELECT a.*, " +
    "  (SELECT composite FROM test_attempts t WHERE t.applicant_id = a.id ORDER BY composite DESC LIMIT 1) AS score " +
    "FROM applicants a " +
    (wheres.length ? "WHERE " + wheres.join(" AND ") : "") +
    " ORDER BY a.created_at DESC LIMIT ?";
  binds.push(limit);

  const rs = await env.DB.prepare(sql).bind(...binds).all();
  const rows = (rs.results || []).map(decodeApplicant);

  // Aggregate stats (across the entire applicants table — not filtered).
  const tot = await env.DB.prepare("SELECT status, COUNT(*) AS n FROM applicants GROUP BY status").all();
  const stats = { total: 0, pending: 0, tested: 0, shortlist: 0, matched: 0, active: 0, disqualified: 0, inactive: 0, paused: 0, mean_score: null };
  for (const r of (tot.results || [])) {
    stats[r.status] = r.n;
    stats.total += r.n;
  }
  const mean = await env.DB.prepare("SELECT AVG(composite) AS m FROM test_attempts").first();
  stats.mean_score = mean && mean.m != null ? mean.m : null;

  return ok({ applicants: rows, stats });
}
