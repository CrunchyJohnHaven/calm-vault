// Calm Vault — no-touch platform Worker.
//
// Routes:
//   POST   /signup                  -> routes/signup.ts
//   POST   /register-org            -> routes/register_org.ts
//   GET    /verify/keys             -> routes/verify.ts
//   GET    /verify/<org_id>         -> routes/verify.ts
//   POST   /attest                  -> routes/attest.ts
//   GET    /checkout/pro            -> routes/checkout.ts  (302 -> Stripe Payment Link)
//   GET    /docs/api                -> routes/docs.ts      (public HTML)
//   GET    /healthz                 -> liveness probe
//   *      OPTIONS                  -> CORS preflight

import type { Env } from "./env";
import { handleAttest } from "./routes/attest";
import { handleCheckoutPro } from "./routes/checkout";
import { handleDocsApi } from "./routes/docs";
import { handleRegisterOrg } from "./routes/register_org";
import { handleSignup } from "./routes/signup";
import { handleVerify } from "./routes/verify";
import { CORS_HEADERS, errorResponse, HttpError } from "./lib/http";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    try {
      const path = url.pathname.replace(/\/$/, "") || "/";

      if (path === "/healthz") {
        return new Response("ok", {
          status: 200,
          headers: { "Content-Type": "text/plain", ...CORS_HEADERS },
        });
      }

      if (path === "/docs/api" && request.method === "GET") {
        return handleDocsApi(env);
      }

      if (path === "/signup" && request.method === "POST") {
        return await handleSignup(request, env);
      }

      if (path === "/register-org" && request.method === "POST") {
        return await handleRegisterOrg(request, env);
      }

      if (path === "/attest" && request.method === "POST") {
        return await handleAttest(request, env);
      }

      if (path === "/checkout/pro" && request.method === "GET") {
        return await handleCheckoutPro(request, env);
      }

      if (path.startsWith("/verify/") && request.method === "GET") {
        const orgId = path.slice("/verify/".length);
        if (!orgId) {
          return errorResponse(
            400,
            "missing_org_id",
            "GET /verify/<org_id> requires an org id (or '/verify/keys').",
          );
        }
        return await handleVerify(env, orgId);
      }

      if (path === "/" && request.method === "GET") {
        return new Response(
          JSON.stringify({
            name: "Calm Vault — no-touch platform",
            docs: `${env.PUBLIC_ORIGIN}/docs/api`,
            health: `${env.PUBLIC_ORIGIN}/healthz`,
          }),
          {
            headers: {
              "Content-Type": "application/json",
              ...CORS_HEADERS,
            },
          },
        );
      }

      return errorResponse(
        404,
        "not_found",
        `No route for ${request.method} ${path}.`,
      );
    } catch (err: unknown) {
      if (err instanceof HttpError) {
        return errorResponse(err.status, err.code, err.message);
      }
      console.error("[worker] unhandled error", err);
      return errorResponse(
        500,
        "internal_error",
        "Unexpected server error.",
      );
    }
  },
};
