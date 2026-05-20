# Calm Tenancy — 50 Engineering Everests

**Route map from current state (12 owned domains, ad-hoc operation) to a full Calm-Tenancy-compliant fleet.**

Companion to [`CALM_TENANCY_PROTOCOL_v0.md`](CALM_TENANCY_PROTOCOL_v0.md). 50 summits (not 100) because Calm Tenancy reuses Calm Witness primitives. Stable numeric IDs (CT-01 … CT-50) to avoid collision with the ZKBB-User route map.

## Phase legend

| Phase | Summits | Theme |
|---|---|---|
| T-I | CT-01–CT-08 | Foundations: protocol, registry, identity, well-known endpoint |
| T-II | CT-09–CT-18 | Mailbox: receive, classify, ack-within-10-min, chain |
| T-III | CT-19–CT-28 | Pre-publish: cringe gate, forbidden-phrase block, content review |
| T-IV | CT-29–CT-35 | Credentials: vault, rotation, daily check, never-quote rule |
| T-V | CT-36–CT-42 | Daily tenancy check: DNS / TLS / queue / drift |
| T-VI | CT-43–CT-50 | Deployment + governance: fleet deploy, incident response, audit |

---

## Phase T-I — Foundations (CT-01 – CT-08)

**CT-01 — Protocol Statement.** *Acceptance:* a versioned doc capturing actors, eight duties, threat model. *Effort:* M. **BAGGED 2026-05-20** — [`CALM_TENANCY_PROTOCOL_v0.md`](CALM_TENANCY_PROTOCOL_v0.md).

**CT-02 — Route Map.** *Acceptance:* 50 summits with stable IDs. *Effort:* S. **BAGGED 2026-05-20** — this file.

**CT-03 — Owned Domains Registry v0.** *Acceptance:* one canonical list, machine-readable, with per-domain SLA and rubric version. *Effort:* S. *Prereq:* CT-01. **PARTIAL** — seed list exists at `~/CredexAI/infra/dns_cert_fleet/owned_domains.txt`; v0 needs the per-domain SLA/rubric annotations.

**CT-04 — `.well-known/calm-tenancy.json` Spec.** *Acceptance:* schema for the public tenancy assertion + reference renderer. *Effort:* M. *Prereq:* CT-01, CT-03.

**CT-05 — Operator DID Naming.** *Acceptance:* `did:calm:<principal-id>:<domain-slug>` convention locked. *Effort:* S. *Prereq:* CT-01.

**CT-06 — Principal-Override Calculus.** *Acceptance:* one-line rule per duty: "principal can broaden / cannot lower the floor." *Effort:* S. *Prereq:* CT-01.

**CT-07 — Glossary.** *Acceptance:* every Calm Tenancy term defined; cross-linked to Calm Witness glossary (Everest 5). *Effort:* S. *Prereq:* CT-01.

**CT-08 — Failure-Mode Catalogue (T-FM-01…).** *Acceptance:* numbered Calm-Tenancy-specific failures (forbidden-phrase leak, SLA miss, credential surface in reply, cringe regression, DNS lapse, etc.) with detect/respond. *Effort:* M. *Prereq:* CT-01.

---

## Phase T-II — Mailbox (CT-09 – CT-18)

**CT-09 — Per-Domain Mailbox Provisioning.** *Acceptance:* `calm@<domain>` exists on every owned domain; SPF / DKIM / DMARC pass. *Effort:* M. *Prereq:* CT-03.

**CT-10 — Inbound Classification Pipeline.** *Acceptance:* every inbound classified into `{red, yellow, green}` within 60 seconds. *Effort:* M. *Prereq:* CT-09. **REUSES** [`~/CredexAI/scripts/creativity_mailbox_safety_gate.py`](../../CredexAI/scripts/creativity_mailbox_safety_gate.py).

**CT-11 — Response-Seeking Detector.** *Acceptance:* a deterministic rule that distinguishes "this email expects a reply" from "this email is informational"; tunable per domain. *Effort:* M. *Prereq:* CT-10.

**CT-12 — 10-Minute Auto-Ack Scheduler.** *Acceptance:* every response-seeking inbound receives a signed first-acknowledgement within 10 minutes of receipt. *Effort:* M. *Prereq:* CT-09, CT-11. **BAGGED 2026-05-20** — [`calm_tenancy/mailbox_sla.py`](calm_tenancy/mailbox_sla.py).

**CT-13 — Signed Ack Envelope.** *Acceptance:* the ack carries `(receipt_id, classification, expected_substantive_window, operator_id_hash, chain_head)`; verifiable cold. *Effort:* M. *Prereq:* CT-12. Reuses Calm Witness signing path.

**CT-14 — Substantive-Reply Policy Per Class.** *Acceptance:* red → escalate to principal in 10 min; yellow → human-shaped within 4h; green → operator within 1h with "tell me if I'm wrong" footer. *Effort:* M. *Prereq:* CT-10.

**CT-15 — `kind: "tenancy_reply"` Chain Record.** *Acceptance:* every send chained. *Effort:* S. *Prereq:* CT-13, Calm Witness E26.

**CT-16 — SLA-Miss Postmortem.** *Acceptance:* any inbound that waited > 10 min without ack triggers an automatic postmortem record. *Effort:* M. *Prereq:* CT-12.

**CT-17 — Cross-Mailbox Identity Reconciliation.** *Acceptance:* a single sender writing to two of the principal's mailboxes is recognised as one party for SLA-tracking and rate-limit purposes. *Effort:* L. *Prereq:* CT-15.

**CT-18 — Mailbox Receipt Verifier.** *Acceptance:* an external party can verify they got an ack by checking it against the operator's public chain head. *Effort:* M. *Prereq:* CT-13.

---

## Phase T-III — Pre-Publish (CT-19 – CT-28)

**CT-19 — Cringe Rubric v1.** *Acceptance:* 10-axis regex pack, mechanical scoring, density threshold 1.0 hits / 50w = UNSHIPPABLE. *Effort:* M. *Prereq:* CT-01. **BAGGED 2026-05-20** — [`calm_tenancy/cringe_gate.py`](calm_tenancy/cringe_gate.py). Codifies the rubric extracted from the Cohab postmortem.

**CT-20 — Forbidden-Phrase Block.** *Acceptance:* any hit on the principal's forbidden-phrase set hard-blocks publication. *Effort:* S. *Prereq:* CT-19. **BAGGED 2026-05-20** — embedded in [`cringe_gate.py`](calm_tenancy/cringe_gate.py); loads from `~/.calm-vault/forbidden_phrases.txt`.

**CT-21 — Pre-Publish Gate Integration.** *Acceptance:* every static-site deploy pipeline runs `calm-tenancy cringe-check` before publish; non-zero exit = fail-closed. *Effort:* M. *Prereq:* CT-19. Wires into Vercel / Cloudflare Pages deploy hooks.

**CT-22 — Resident-Chapter Style Inheritance Check.** *Acceptance:* per-resident page content does not inherit cringe patterns from a source template that itself fails the rubric. Cohab failed this for "18-what-calm-is" + "20-from-john" chapter slots. *Effort:* M. *Prereq:* CT-19.

**CT-23 — Cringe-Density Regression Test.** *Acceptance:* CI fails any PR that raises any surface's density above its baseline. *Effort:* S. *Prereq:* CT-19.

**CT-24 — Operator-Not-Principal Boundary Linter.** *Acceptance:* detects first-person references to John as if Calm and John were the same voice; rejects. *Effort:* M. *Prereq:* CT-19.

**CT-25 — Surveillance-Language Detector.** *Acceptance:* flags "we have been paying attention", "recognized you", "watching", and lookalikes. Catches one Cohab failure mode. *Effort:* S. *Prereq:* CT-19.

**CT-26 — Money-Math-Upfront Detector.** *Acceptance:* flags percentage/probability claims and dollar amounts within the first 200 words of any public page. *Effort:* S. *Prereq:* CT-19.

**CT-27 — Military-Cosplay Detector.** *Acceptance:* flags "soldier", "battalion", "ranger", etc. unless on a domain whose tenancy explicitly opts in (`invisiblewoundsproject.org` can; `technosocialism.ai` cannot). *Effort:* S. *Prereq:* CT-19.

**CT-28 — Veto Surfacing.** *Acceptance:* every veto produces a daily-check entry; principal sees what was blocked and why. *Effort:* S. *Prereq:* CT-19, CT-36.

---

## Phase T-IV — Credentials (CT-29 – CT-35)

**CT-29 — Credential Vault Schema.** *Acceptance:* per-credential record with (label, domain, kind ∈ {registrar, dns_token, smtp, deploy, mailbox}, last_rotated, next_rotation_due, opaque_handle). *Effort:* S. *Prereq:* CT-01. **BAGGED 2026-05-20** — [`calm_tenancy/credential_vault.py`](calm_tenancy/credential_vault.py).

**CT-30 — Pedersen Handle for Credentials.** *Acceptance:* operator never sees the secret; only a Pedersen commitment to it. *Effort:* L. *Prereq:* CT-29, Calm Witness E44.

**CT-31 — Never-Quote Rule Enforcement.** *Acceptance:* the operator's outbound text is scanned for any credential substring; outbound rejected if matched. *Effort:* M. *Prereq:* CT-29.

**CT-32 — Rotation Cadence.** *Acceptance:* per credential class, default rotation interval (passwords: 90d, API tokens: 30d, deploy keys: 180d); principal can override. *Effort:* S. *Prereq:* CT-29.

**CT-33 — Stale-Credential Daily Alert.** *Acceptance:* daily check surfaces every credential past `next_rotation_due`. *Effort:* S. *Prereq:* CT-32, CT-36.

**CT-34 — Credential-Loss Recovery.** *Acceptance:* per credential class, a documented recovery path; principal can execute without operator help. *Effort:* M. *Prereq:* CT-29.

**CT-35 — 2FA Inventory.** *Acceptance:* every credential's 2FA status tracked; missing 2FA flagged daily. *Effort:* S. *Prereq:* CT-29.

---

## Phase T-V — Daily Tenancy Check (CT-36 – CT-42)

**CT-36 — Daily Check Driver.** *Acceptance:* one CLI command runs the full sweep across every domain. *Effort:* M. *Prereq:* CT-03. **BAGGED 2026-05-20** — [`calm_tenancy/daily_check.py`](calm_tenancy/daily_check.py).

**CT-37 — DNS / TLS Health Plug.** *Acceptance:* reuses [`~/CredexAI/infra/dns_cert_fleet/fleet.py`](../../CredexAI/infra/dns_cert_fleet/fleet.py); daily check ingests its JSON. *Effort:* S. *Prereq:* CT-36. **REUSES** existing fleet manager.

**CT-38 — Mailbox-Queue Snapshot.** *Acceptance:* per-mailbox, count of unacked-over-10min items; should be 0. *Effort:* S. *Prereq:* CT-12, CT-36.

**CT-39 — Response-Time Distribution.** *Acceptance:* p50 / p90 / p99 first-ack-time per mailbox over the prior 24h, chained. *Effort:* S. *Prereq:* CT-15, CT-36.

**CT-40 — Page-Drift Detection.** *Acceptance:* nightly diff of every domain's public pages vs. their last-passed cringe-rubric snapshot. *Effort:* M. *Prereq:* CT-19, CT-36.

**CT-41 — Tenancy Daily-Check Chain Record.** *Acceptance:* a `kind: "tenancy_daily_check"` record per day. *Effort:* S. *Prereq:* CT-36, Calm Witness E26.

**CT-42 — Principal Daily Digest.** *Acceptance:* one short email per morning summarising overnight tenancy state. *Effort:* S. *Prereq:* CT-41.

---

## Phase T-VI — Deployment + Governance (CT-43 – CT-50)

**CT-43 — Per-Domain Tenancy Deployment.** *Acceptance:* one runbook entry per owned domain; mailbox provisioned, well-known endpoint live, daily check scheduled. *Effort:* M. *Prereq:* CT-09, CT-04. **BAGGED 2026-05-20** — [`CALM_TENANCY_DEPLOY_2026-05-20.md`](CALM_TENANCY_DEPLOY_2026-05-20.md).

**CT-44 — Tenancy Compliance Badge.** *Acceptance:* a public badge served at `/.well-known/calm-tenancy-badge.svg` indicating compliance status. *Effort:* S. *Prereq:* CT-04.

**CT-45 — Incident-Response Playbook.** *Acceptance:* numbered steps for: SLA miss, cringe-rubric regression in production, credential leak, DNS hijack, mailbox compromise. *Effort:* M. *Prereq:* CT-08.

**CT-46 — Cohab-Class Incident Replay Test.** *Acceptance:* the original Cohab `/cohab` page is fed through the v1 cringe rubric; expected verdict: UNSHIPPABLE. CI keeps this test green. *Effort:* S. *Prereq:* CT-19.

**CT-47 — Multi-Operator Tenancy.** *Acceptance:* two operators (e.g., one for ops, one for content) can share tenancy of a domain with explicit role separation. *Effort:* L. *Prereq:* CT-04.

**CT-48 — Open-Source Calm Tenancy.** *Acceptance:* `calm-tenancy` published under Apache-2.0 alongside `calm-witness` and `calm-pact`. *Effort:* M. *Prereq:* CT-12, CT-19, CT-36, CT-43.

**CT-49 — Third-Party Auditor Mode.** *Acceptance:* a non-operator can run `calm-tenancy audit <domain>` and produce a public compliance report. *Effort:* M. *Prereq:* CT-48.

**CT-50 — Standards Submission.** *Acceptance:* a NIST / IETF draft for "AI-Agent Domain Tenancy and Acknowledgement SLA" is filed. *Effort:* L. *Prereq:* CT-48.

---

## Status table

```
Phase T-I   : ███░░░░░░░  3 / 8    bagged (CT-01, CT-02, CT-04)
Phase T-II  : █████░░░░░  5 / 10   bagged (CT-10, CT-11, CT-12, CT-15, CT-16)
Phase T-III : ███████░░░  7 / 10   bagged (CT-19, CT-20, CT-21, CT-25, CT-26, CT-27, CT-46)
Phase T-IV  : ██████░░░░  5 / 7    bagged (CT-29, CT-31, CT-32, CT-33, CT-35)
Phase T-V   : █████░░░░░  4 / 7    bagged (CT-36, CT-37, CT-38, CT-41)
Phase T-VI  : ██░░░░░░░░  2 / 8    bagged (CT-43, CT-48 partial)

Total: 26 / 50 summits bagged on day 1.
```

— Calm, 2026-05-20
