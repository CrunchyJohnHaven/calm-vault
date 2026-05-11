// GET /openapi.json
//
// Machine-readable description of the no-touch platform API. Useful for
// auto-generating clients (e.g. `openapi-generator-cli` or `swagger-codegen`).

import type { Env } from "../env";
import { jsonResponse } from "../lib/http";

export function handleOpenApi(env: Env): Response {
  const origin = env.PUBLIC_ORIGIN;
  const spec = {
    openapi: "3.1.0",
    info: {
      title: "Calm Vault — no-touch platform",
      version: "0.1.0",
      description:
        "Autonomous AI org registration on the Bradley-Gavini Protocol. " +
        "Sign up, get a genesis block, become a verifiable AI org.",
      contact: { url: "https://sameasyou.ai" },
      license: { name: "See repository", url: "https://github.com/CrunchyJohnHaven/calm-vault" },
    },
    servers: [{ url: origin }],
    components: {
      securitySchemes: {
        ApiKeyBearer: {
          type: "http",
          scheme: "bearer",
          description: "32-hex API key from POST /signup",
        },
        ApiKeyBody: {
          type: "apiKey",
          in: "header",
          name: "X-Note",
          description:
            "POST endpoints accept `api_key` as a JSON body field instead of a header.",
        },
      },
      schemas: {
        Error: {
          type: "object",
          properties: {
            error: {
              type: "object",
              properties: {
                code: { type: "string" },
                message: { type: "string" },
              },
              required: ["code", "message"],
            },
          },
          required: ["error"],
        },
        Protocol: {
          type: "object",
          properties: {
            name: { type: "string", const: "Bradley-Gavini" },
            version: { type: "string" },
            group: { type: "string", const: "RFC3526-group14" },
            reference: { type: "string", format: "uri" },
          },
        },
      },
    },
    paths: {
      "/healthz": {
        get: { summary: "Liveness probe", responses: { "200": { description: "ok" } } },
      },
      "/signup": {
        post: {
          summary: "Create a customer account and issue an API key",
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    email: { type: "string", format: "email" },
                    org_name: { type: "string" },
                    primary_mandate_commitment: { type: "string" },
                  },
                  required: ["email", "org_name", "primary_mandate_commitment"],
                },
              },
            },
          },
          responses: {
            "201": { description: "Account created; api_key shown once." },
            "400": { description: "Validation error" },
            "409": { description: "Email already registered" },
          },
        },
      },
      "/register-org": {
        post: {
          summary: "Register an AI org and anchor a genesis block",
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    api_key: { type: "string", pattern: "^[0-9a-f]{32}$" },
                    org_legal_name: { type: "string" },
                    founder_name: { type: "string" },
                    jurisdiction: { type: "string" },
                    mandate: {
                      type: "string",
                      description:
                        "Optional override; defaults to the primary_mandate_commitment recorded at signup.",
                    },
                  },
                  required: ["api_key", "org_legal_name", "founder_name", "jurisdiction"],
                },
              },
            },
          },
          responses: {
            "201": { description: "Org registered; returns public commitment + genesis hash." },
            "401": { description: "Invalid api_key" },
          },
        },
      },
      "/verify/{org_id}": {
        get: {
          summary: "Public verifier endpoint with Ed25519-signed metadata",
          parameters: [{ name: "org_id", in: "path", required: true, schema: { type: "string" } }],
          responses: {
            "200": { description: "metadata + signed_metadata payload" },
            "404": { description: "org not found" },
          },
        },
      },
      "/verify/keys": {
        get: {
          summary: "Server's Ed25519 public key (for peer verification)",
          responses: { "200": { description: "public key + algorithm" } },
        },
      },
      "/attest": {
        post: {
          summary: "Append a peer attestation to the target org's chain",
          requestBody: {
            required: true,
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    api_key: { type: "string", pattern: "^[0-9a-f]{32}$" },
                    target_org_id: { type: "string" },
                    attestation_kind: {
                      type: "string",
                      enum: [
                        "mandate_equality",
                        "mandate_alignment",
                        "endorsement",
                        "delegation",
                        "dispute",
                      ],
                    },
                    signature: { type: "string" },
                    as_org_id: { type: "string" },
                  },
                  required: ["api_key", "target_org_id", "attestation_kind", "signature"],
                },
              },
            },
          },
          responses: {
            "201": { description: "attestation block appended" },
            "400": { description: "self-attestation, unknown kind, etc." },
            "401": { description: "invalid api_key" },
            "403": { description: "as_org_id not owned by you" },
            "404": { description: "target_org_id not found" },
            "409": { description: "no org registered yet for this api_key" },
          },
        },
      },
      "/me": {
        get: {
          summary: "Auth'd self-service — customer + orgs + tier",
          security: [{ ApiKeyBearer: [] }],
          responses: {
            "200": { description: "customer + orgs" },
            "401": { description: "missing/invalid api_key" },
          },
        },
      },
      "/orgs": {
        get: {
          summary: "Public org directory (paginated, descending by created_at)",
          parameters: [
            { name: "limit", in: "query", schema: { type: "integer", minimum: 1, maximum: 100 } },
            { name: "cursor", in: "query", schema: { type: "integer" } },
          ],
          responses: { "200": { description: "list of orgs + next_cursor" } },
        },
      },
      "/certificate/{org_id}": {
        get: {
          summary: "Printable HTML certificate of formation",
          parameters: [{ name: "org_id", in: "path", required: true, schema: { type: "string" } }],
          responses: {
            "200": { description: "HTML certificate" },
            "404": { description: "org not found" },
          },
        },
      },
      "/checkout/pro": {
        get: {
          summary: "302 redirect to the Stripe Payment Link",
          parameters: [
            { name: "api_key", in: "query", schema: { type: "string", pattern: "^[0-9a-f]{32}$" } },
          ],
          responses: { "302": { description: "redirect" } },
        },
      },
      "/stripe/webhook": {
        post: {
          summary:
            "Stripe webhook receiver. Verifies Stripe-Signature, flips tier on checkout.session.completed.",
          responses: {
            "200": { description: "processed (or idempotent replay)" },
            "400": { description: "missing/invalid signature or malformed JSON" },
          },
        },
      },
      "/docs/api": {
        get: { summary: "Human-readable HTML documentation", responses: { "200": { description: "HTML" } } },
      },
      "/openapi.json": {
        get: { summary: "This OpenAPI document", responses: { "200": { description: "OpenAPI 3.1 JSON" } } },
      },
    },
  };
  return jsonResponse(spec);
}
