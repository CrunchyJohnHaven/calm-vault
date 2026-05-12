import { err, ok, verifyAdmin } from "../../_lib/util.js";

export async function onRequestGet({ request, env }) {
  if (!(await verifyAdmin(request, env))) return err("Forbidden.", 403);
  const rs = await env.DB.prepare("SELECT * FROM aao_projects WHERE status = 'open' ORDER BY id ASC").all();
  return ok({ projects: rs.results || [] });
}
