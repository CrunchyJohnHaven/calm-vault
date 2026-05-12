-- InternsForAI v0 schema
-- D1 (SQLite-compatible). Run with: wrangler d1 execute internsforai_prod --file=schema/0001_init.sql

-- =========================
-- applicants
-- =========================
CREATE TABLE IF NOT EXISTS applicants (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  updated_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),

  email             TEXT NOT NULL UNIQUE,
  display_name      TEXT NOT NULL,
  country           TEXT NOT NULL,                  -- ISO-2 or free text
  timezone          TEXT,
  native_language   TEXT,
  fluent_languages  TEXT,                           -- JSON array
  tracks            TEXT NOT NULL,                  -- JSON array of track keys
  why_trial         TEXT,                           -- "why would you be a great trial worker"
  editorial_catch   TEXT,                           -- "most thoughtful editorial catch you've made"
  cofounder_pitch   TEXT,                           -- "what would you build with AI cofounder + free infra"
  sample_url        TEXT,                           -- optional portfolio link
  hours_per_week    INTEGER,                        -- 1,2,4,8,16,24,40
  pay_method        TEXT,                           -- 'usdc' | 'wise' | 'paypal'
  pay_address       TEXT,                           -- wallet/email/paypal
  pay_rate_floor    REAL,                           -- computed jurisdictional floor (USD/hr)
  session_token     TEXT NOT NULL UNIQUE,           -- post-apply continuation token (also doubles as magic-link)
  ip                TEXT,                           -- audit
  user_agent        TEXT,                           -- audit
  status            TEXT NOT NULL DEFAULT 'pending',-- pending|tested|shortlist|matched|active|paused|disqualified|inactive
  admin_notes       TEXT
);
CREATE INDEX IF NOT EXISTS idx_applicants_status ON applicants(status);
CREATE INDEX IF NOT EXISTS idx_applicants_country ON applicants(country);
CREATE INDEX IF NOT EXISTS idx_applicants_created ON applicants(created_at);

-- =========================
-- test_attempts
-- =========================
CREATE TABLE IF NOT EXISTS test_attempts (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id) ON DELETE CASCADE,
  track             TEXT NOT NULL,
  raw_answers       TEXT NOT NULL,                  -- JSON of question_id -> answer
  per_question      TEXT NOT NULL,                  -- JSON of per-question scoring
  mc_score          REAL NOT NULL DEFAULT 0,        -- 0..1 weighted multiple-choice
  text_score        REAL NOT NULL DEFAULT 0,        -- 0..1 weighted free-text
  ai_score          REAL NOT NULL DEFAULT 0,        -- 0..1 weighted AI-graded
  composite         REAL NOT NULL DEFAULT 0,        -- 0..100 composite
  verdict           TEXT NOT NULL,                  -- PASS|SHORTLIST|FAIL
  ai_feedback       TEXT                            -- short rationale for John
);
CREATE INDEX IF NOT EXISTS idx_test_applicant ON test_attempts(applicant_id);

-- =========================
-- aao_projects
-- =========================
CREATE TABLE IF NOT EXISTS aao_projects (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  slug              TEXT NOT NULL UNIQUE,           -- e.g. sameasyou, sss, calm-vault
  name              TEXT NOT NULL,
  brief             TEXT NOT NULL,
  url               TEXT,
  status            TEXT NOT NULL DEFAULT 'open',   -- open|paused|closed
  tracks            TEXT NOT NULL,                  -- JSON array of compatible tracks
  franchise_percent REAL NOT NULL DEFAULT 20.0
);

-- =========================
-- matches (applicant -> AAO project, with franchise terms)
-- =========================
CREATE TABLE IF NOT EXISTS matches (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id) ON DELETE CASCADE,
  project_id        INTEGER NOT NULL REFERENCES aao_projects(id),
  franchise_percent REAL NOT NULL DEFAULT 20.0,     -- override per match if needed
  worker_percent    REAL NOT NULL DEFAULT 80.0,
  status            TEXT NOT NULL DEFAULT 'proposed',-- proposed|accepted|active|completed|declined|terminated
  brief_override    TEXT,
  admin_notes       TEXT
);
CREATE INDEX IF NOT EXISTS idx_matches_applicant ON matches(applicant_id);

-- =========================
-- franchise_statements (per-period earnings + 80/20 split)
-- =========================
CREATE TABLE IF NOT EXISTS franchise_statements (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id),
  match_id          INTEGER REFERENCES matches(id),
  period_start      INTEGER NOT NULL,
  period_end        INTEGER NOT NULL,
  gross_revenue     REAL NOT NULL DEFAULT 0,
  worker_share      REAL NOT NULL DEFAULT 0,        -- 80% by default
  network_share     REAL NOT NULL DEFAULT 0,        -- 20% by default
  notes             TEXT
);

-- =========================
-- payments
-- =========================
CREATE TABLE IF NOT EXISTS payments (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id),
  match_id          INTEGER REFERENCES matches(id),
  amount_usd        REAL NOT NULL,
  method            TEXT NOT NULL,                  -- 'usdc'|'wise'|'paypal'
  reference         TEXT,                           -- txn id, USDC hash, etc
  status            TEXT NOT NULL DEFAULT 'pending',-- pending|sent|confirmed|failed
  notes             TEXT
);

-- =========================
-- attestations (AAL stub for v0; real cryptographic attestation lands later)
-- =========================
CREATE TABLE IF NOT EXISTS attestations (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id),
  kind              TEXT NOT NULL,                  -- 'test_pass'|'project_complete'|'kill_switch'|'dispute_resolved'
  score             REAL,
  payload           TEXT,                           -- JSON of underlying evidence
  signature_stub    TEXT                            -- placeholder for AAL component 3
);

-- =========================
-- magic_links (for /worker passwordless auth)
-- =========================
CREATE TABLE IF NOT EXISTS magic_links (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at        INTEGER NOT NULL DEFAULT (strftime('%s','now') * 1000),
  applicant_id      INTEGER NOT NULL REFERENCES applicants(id),
  token             TEXT NOT NULL UNIQUE,
  expires_at        INTEGER NOT NULL,
  used_at           INTEGER
);
CREATE INDEX IF NOT EXISTS idx_magic_applicant ON magic_links(applicant_id);

-- =========================
-- Seed: AAO projects
-- =========================
INSERT OR IGNORE INTO aao_projects (slug, name, brief, url, tracks, franchise_percent) VALUES
  ('sameasyou', 'Same As You', 'Parent AAO + Bradley-Gavini Protocol reference + Alignment Accountability Layer outreach, docs, demo translation.', 'https://sameasyou.ai', '["light_judgment","heavy_judgment","specialized"]', 20.0),
  ('sss',       'See Something Say Something', 'Demand-side cybersec wedge: triage incident reports, QA Calm outputs, copy-edit weekly comms.', 'https://seesomethingsaysomething.ai', '["light_judgment","heavy_judgment","domain_expert"]', 20.0),
  ('calm-vault','Calm Vault',                  'Zero-trust credential broker docs, integration tutorials, audit-log triage.', 'https://github.com/CrunchyJohnHaven/calm-vault', '["specialized","domain_expert"]', 20.0),
  ('ifa-ops',   'InternsForAI Ops',            'Recruiting outreach, applicant pipeline QA, technosocialism doctrine refinement, FAQ maintenance.', 'https://internsforai.org', '["mechanical","light_judgment","heavy_judgment"]', 20.0);
