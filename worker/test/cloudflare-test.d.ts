// Type stubs for the `cloudflare:test` module exposed by
// `@cloudflare/vitest-pool-workers` at runtime. The package ships its own
// types but the resolution path requires this declaration when the test
// runner is launched via the standard tsc compiler.

declare module "cloudflare:test" {
  import type { D1Database, Fetcher } from "@cloudflare/workers-types";

  // Generated per `vitest.config.ts`; we only care about the bindings we use.
  export const env: {
    DB: D1Database;
    PUBLIC_ORIGIN: string;
    FROM_EMAIL: string;
    STRIPE_PRO_PAYMENT_LINK: string;
    RESEND_API_KEY?: string;
    ANTHROPIC_API_KEY?: string;
    STRIPE_WEBHOOK_SECRET?: string;
  };

  export const SELF: Fetcher;
}
