// Calm Vault — no-touch platform Worker.
//
// Routes:
//   POST   /signup                  -> routes/signup.ts
//   POST   /register-org            -> routes/register_org.ts
//   GET    /verify/keys             -> routes/verify.ts
//   GET    /verify/<org_id>         -> routes/verify.ts
//   GET    /certificate/<org_id>    -> routes/certificate.ts  (printable HTML)
//   POST   /attest                  -> routes/attest.ts
//   POST   /stripe/webhook          -> routes/stripe_webhook.ts
//   GET    /checkout/pro            -> routes/checkout.ts     (302 -> Stripe Payment Link)
//   GET    /orgs                    -> routes/orgs_list.ts    (public directory, paginated)
//   GET    /me                      -> routes/me.ts           (auth'd self-service)
//   GET    /docs/api                -> routes/docs.ts         (public HTML)
//   GET    /healthz                 -> liveness probe
//   *      OPTIONS                  -> CORS preflight
//
// HEAD requests are routed as GET; the runtime drops the body automatically.

import type { Env } from "./env";
import { handleAttest } from "./routes/attest";
import { handleCertificate } from "./routes/certificate";
import { handleCheckoutPro } from "./routes/checkout";
import { handleDocsApi } from "./routes/docs";
import { handleMe } from "./routes/me";
import { handleOrgsList } from "./routes/orgs_list";
import { handleRegisterOrg } from "./routes/register_org";
import { handleSignup } from "./routes/signup";
import { handleStripeWebhook } from "./routes/stripe_webhook";
import { handleVerify } from "./routes/verify";
import { CORS_HEADERS, errorResponse, HttpError } from "./lib/http";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // Treat HEAD as GET for routing; the runtime strips the body on the way out.
    const method =
      request.method === "HEAD" ? "GET" : request.method.toUpperCase();

    try {
      const path = url.pathname.replace(/\/$/, "") || "/";

      if (path === "/healthz") {
        return new Response("ok", {
          status: 200,
          headers: { "Content-Type": "text/plain", ...CORS_HEADERS },
        });
      }

      if (path === "/docs/api" && method === "GET") {
        return handleDocsApi(env);
      }

      if (path === "/signup" && method === "POST") {
        return await handleSignup(request, env);
      }

      if (path === "/register-org" && method === "POST") {
        return await handleRegisterOrg(request, env);
      }

      if (path === "/attest" && method === "POST") {
        return await handleAttest(request, env);
      }

      if (path === "/checkout/pro" && method === "GET") {
        return await handleCheckoutPro(request, env);
      }

      if (path === "/stripe/webhook" && method === "POST") {
        return await handleStripeWebhook(request, env);
      }

      if (path === "/orgs" && method === "GET") {
        return await handleOrgsList(request, env);
      }

      if (path === "/me" && method === "GET") {
        return await handleMe(request, env);
      }

      if (path.startsWith("/verify/") && method === "GET") {
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

      if (path.startsWith("/certificate/") && method === "GET") {
        const orgId = path.slice("/certificate/".length);
        if (!orgId) {
          return errorResponse(
            400,
            "missing_org_id",
            "GET /certificate/<org_id> requires an org id.",
          );
        }
        return await handleCertificate(env, orgId);
      }

      if (path === "/" && method === "GET") {
        return new Response(
          JSON.stringify({
            name: "Calm Vault — no-touch platform",
            docs: `${env.PUBLIC_ORIGIN}/docs/api`,
            health: `${env.PUBLIC_ORIGIN}/healthz`,
            directory: `${env.PUBLIC_ORIGIN}/orgs`,
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
