-- AAL Bug Bounty — Cloudflare D1 schema
--
-- This database is separate from any customer-signup database. Create with:
--   wrangler d1 create aal-bounty
--   wrangler d1 execute aal-bounty --file=bounty/submission/schema.sql
--
-- Apache 2.0 · github.com/CrunchyJohnHaven/calm-vault

CREATE TABLE IF NOT EXISTS bounty_submissions (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id       TEXT    NOT NULL UNIQUE,
    bug_class         TEXT    NOT NULL,
    severity_rating   INTEGER NOT NULL CHECK (severity_rating BETWEEN 1 AND 10),
    description       TEXT    NOT NULL,
    proof_of_concept  TEXT    NOT NULL,
    contact           TEXT    NOT NULL,
    payment_rail      TEXT    NOT NULL,
    handle            TEXT,
    commit_sha        TEXT,
    source_ip         TEXT,
    user_agent        TEXT,

    -- Pipeline state. `status` is the human-readable state, the rest is metadata.
    status            TEXT    NOT NULL DEFAULT 'received',
    triage_class      TEXT,
    triage_tier       TEXT,
    triage_notes      TEXT,
    triage_dupe_of    TEXT,
    triage_model      TEXT,
    triage_at         INTEGER,

    accepted          INTEGER NOT NULL DEFAULT 0,
    paid_at           INTEGER,
    payout_usd_cents  INTEGER,
    payout_rail       TEXT,
    payout_ref        TEXT,

    created_at        INTEGER NOT NULL,
    updated_at        INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_bounty_submissions_status     ON bounty_submissions (status);
CREATE INDEX IF NOT EXISTS idx_bounty_submissions_bug_class  ON bounty_submissions (bug_class);
CREATE INDEX IF NOT EXISTS idx_bounty_submissions_created_at ON bounty_submissions (created_at);

-- One row per public attestation that gets written back to the
-- Component 3 watermarked audit chain. Filled in only after the
-- 30-day private window closes.
CREATE TABLE IF NOT EXISTS bounty_attestations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id         TEXT    NOT NULL,
    component3_chain_id TEXT    NOT NULL,
    watermark_root      TEXT    NOT NULL,
    public_handle       TEXT,
    summary             TEXT    NOT NULL,
    published_at        INTEGER NOT NULL,
    FOREIGN KEY (tracking_id) REFERENCES bounty_submissions (tracking_id)
);

CREATE INDEX IF NOT EXISTS idx_bounty_attestations_tracking_id ON bounty_attestations (tracking_id);
