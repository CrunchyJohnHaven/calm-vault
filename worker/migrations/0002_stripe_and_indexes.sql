-- Stripe webhook support: track subscription state + when a customer upgraded.
ALTER TABLE customers ADD COLUMN pro_since INTEGER;
ALTER TABLE customers ADD COLUMN stripe_subscription_id TEXT;

-- Idempotency for Stripe webhook deliveries — Stripe retries on non-2xx so we
-- need to recognise already-processed event ids.
CREATE TABLE stripe_events (
  id          TEXT    PRIMARY KEY,         -- Stripe event id (evt_*)
  event_type  TEXT    NOT NULL,
  customer_id TEXT,                        -- nullable (the event may not map to a customer)
  payload     TEXT    NOT NULL,            -- raw JSON body
  received_at INTEGER NOT NULL
);

-- Indexes used by /orgs (public directory) ordering.
CREATE INDEX idx_orgs_created_at ON orgs(created_at);
