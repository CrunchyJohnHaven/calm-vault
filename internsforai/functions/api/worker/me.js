import { err, ok, verifyWorker, decodeApplicant } from "../../_lib/util.js";

export async function onRequestGet({ request, env }) {
  const applicant = await verifyWorker(request, env);
  if (!applicant) return err("Unauthorized.", 401);

  const tests = await env.DB.prepare(
    "SELECT * FROM test_attempts WHERE applicant_id = ? ORDER BY created_at DESC"
  ).bind(applicant.id).all();
  const match = await env.DB.prepare(
    "SELECT m.*, p.name AS project_name, p.brief AS project_brief, p.url AS project_url FROM matches m JOIN aao_projects p ON p.id = m.project_id WHERE m.applicant_id = ? ORDER BY m.created_at DESC LIMIT 1"
  ).bind(applicant.id).first();

  const payRows = await env.DB.prepare(
    "SELECT * FROM payments WHERE applicant_id = ? ORDER BY created_at DESC"
  ).bind(applicant.id).all();
  const payments = payRows.results || [];

  // franchise statement aggregate
  let workerShare = 0, networkShare = 0, lastPaid = null;
  for (const p of payments) {
    workerShare += Number(p.amount_usd || 0);
    if (p.status === "paid" && (!lastPaid || (p.created_at > lastPaid))) lastPaid = p.created_at;
  }
  // network share = (worker share / 0.8) * 0.2 from gross
  const grossEst = workerShare > 0 ? workerShare / 0.8 : 0;
  networkShare = grossEst - workerShare;

  // reputation seed: best test composite (capped 100), v0 stub for AAL component 3
  const best = (tests.results || []).reduce((m, t) => Math.max(m, t.composite || 0), 0);
  const reputation = best;

  const out = decodeApplicant(applicant);
  let matchOut = null;
  if (match) {
    matchOut = {
      id: match.id,
      project_name: match.project_name,
      project_brief: match.project_brief,
      project_url: match.project_url,
      brief_override: match.brief_override,
      franchise_percent: match.franchise_percent,
      worker_percent: 100 - match.franchise_percent,
      status: match.status,
      created_at: match.created_at
    };
  }
  return ok({
    applicant: out,
    tests: tests.results || [],
    match: matchOut,
    payments,
    franchise: {
      worker_share: workerShare,
      network_share: networkShare,
      last_paid: lastPaid
    },
    reputation
  });
}
