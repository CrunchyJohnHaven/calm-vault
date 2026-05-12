import { json, err, ok, verifyAdmin, decodeApplicant } from "../../../_lib/util.js";

export async function onRequestGet({ params, request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const id = parseInt(params.id, 10);
  if (!id) return err("Bad id.", 400);
  const row = await env.DB.prepare("SELECT * FROM applicants WHERE id = ?").bind(id).first();
  if (!row) return err("Not found.", 404);
  const tests = await env.DB.prepare(
    "SELECT * FROM test_attempts WHERE applicant_id = ? ORDER BY created_at DESC"
  ).bind(id).all();
  const matches = await env.DB.prepare(
    "SELECT m.*, p.name AS project_name, p.brief AS project_brief, p.slug AS project_slug, p.url AS project_url FROM matches m JOIN aao_projects p ON p.id = m.project_id WHERE m.applicant_id = ? ORDER BY m.created_at DESC"
  ).bind(id).all();
  return ok({
    applicant: decodeApplicant(row),
    tests: tests.results || [],
    matches: matches.results || []
  });
}
