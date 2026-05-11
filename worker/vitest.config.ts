import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
        miniflare: {
          d1Databases: ["DB"],
          bindings: {
            PUBLIC_ORIGIN: "https://test.sameasyou.ai",
            FROM_EMAIL: "Calm Vault <test@sameasyou.ai>",
            STRIPE_PRO_PAYMENT_LINK: "https://buy.stripe.com/test_link",
          },
        },
      },
    },
  },
});
