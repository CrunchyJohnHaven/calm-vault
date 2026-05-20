# Calm Tenancy — Fleet Deployment Plan (2026-05-20)

**Goal:** bring every owned domain to Calm-Tenancy v0 compliance — mailbox provisioned, well-known endpoint live, daily check scheduled, cringe gate in the deploy pipeline.

**Source of truth for the fleet:** `~/CredexAI/infra/dns_cert_fleet/owned_domains.txt` (12 domains).

This document is a **runbook**, not a finished deployment — it lists, per domain, what John (or a designated operator) needs to execute. Where the action is risky, irreversible, or visible-to-others, it requires explicit John approval before firing.

---

## §1. Pre-flight checklist (one-time, all domains)

Before any per-domain work:

1. **Forbidden-phrase file.** Create `~/.calm-vault/forbidden_phrases.txt` with one phrase per line. Seed list (from existing operator memory): `1480 Chapin`, `Chapin Street`, and any others the principal has flagged. Run `cat > ~/.calm-vault/forbidden_phrases.txt`.
2. **Smoke-test the cringe gate** against the Cohab archived page to confirm it fires UNSHIPPABLE: `curl -s https://technosocialism.ai/cohab | python3 ~/AllData/calm_vault_market/calm_tenancy/cringe_gate.py --stdin`. Expected exit code: **1**. If 0, the rubric needs tuning before deployment.
3. **Verify the existing DNS/TLS fleet manager runs clean:** `python3 ~/CredexAI/infra/dns_cert_fleet/fleet.py --dry-run`. Address any pre-existing ALERTs before adding tenancy on top.
4. **Connect Gmail OR confirm SMTP path per domain.** Without one of these, the 10-minute auto-ack scheduler cannot dispatch. Two choices: (a) connect the Gmail MCP connector and use `calm@<domain>` aliases; (b) use the existing `~/.workspace/install-gmail-smtp.sh` per domain.
5. **Stage the calm-tenancy CLI on PATH.** Symlink or alias: `alias calm-tenancy='python3 ~/AllData/calm_vault_market/calm_tenancy/'`.

---

## §2. Per-domain deployment matrix

| Domain | Mailbox | SLA | Forbidden-phrase profile | Daily check | Public well-known | Owner | Status |
|---|---|---|---|---|---|---|---|
| `internsforai.org` | `calm@internsforai.org` | 10 min | default | 09:00 ET | yes | John | pending |
| `technosocialism.ai` | `calm@technosocialism.ai` | 10 min | default + Cohab-specific block list | 09:00 ET | yes | John | **HIGH RISK** — Cohab incident origin; restage with extra cringe-rubric review |
| `ricksanchez.ai` | `calm@ricksanchez.ai` | 10 min | default | 09:00 ET | yes | John | pending |
| `darkmusk.ai` | `calm@darkmusk.ai` | 10 min | default + persona surveillance suppression | 09:00 ET | yes | John | pending |
| `darkmusk.com` | redirects to `.ai` | inherits | inherits | inherits | redirect-only | John | low priority |
| `sameasyou.ai` | `calm@sameasyou.ai` | 10 min | default | 09:00 ET | yes | John | pending |
| `credexai.org` | `calm@credexai.org` | 10 min | default + corporate-poetic axis especially watched | 09:00 ET | yes | John / Koushik | **highest visibility** — CredexAI is the identity issuer; tenancy violation here cascades |
| `credexai.xyz` | redirects to `.org` | inherits | inherits | inherits | redirect-only | John | low priority |
| `calm-vault.com` | `calm@calm-vault.com` | 10 min | default | 09:00 ET | yes | John | pending; this is where the protocols live publicly |
| `thecreativitymachine.ai` | `calm@thecreativitymachine.ai` | 10 min | default | 09:00 ET | yes | John | pending; LLC-owned domain |
| `invisiblewoundsproject.org` | `calm@invisiblewoundsproject.org` | 10 min | default + opt-in military framing (this domain explicitly allows it) | 09:00 ET | yes | John (calm@) | pending; only veteran-context domain |
| `substrateai.xyz` | `calm@substrateai.xyz` | 10 min | default | 09:00 ET | yes | John | pending |

---

## §3. The per-domain action sequence (run this for each row above)

```bash
DOMAIN=thecreativitymachine.ai     # ← change per row

# 1. Provision mailbox (CT-09). Manual: log in to registrar / mail provider.
#    Confirm SPF, DKIM, DMARC records.
dig +short TXT _dmarc.$DOMAIN
dig +short TXT $DOMAIN | grep -i 'spf'
dig +short TXT default._domainkey.$DOMAIN

# 2. Register credentials in the vault registry (CT-29).
python3 ~/AllData/calm_vault_market/calm_tenancy/credential_vault.py register \
  --handle "$DOMAIN:registrar"   --domain $DOMAIN --kind registrar \
  --label "Registrar (Cloudflare/Porkbun/etc.)" \
  --secret-pointer "age:///path/to/encrypted/registrar.age" \
  --twofa-enabled
python3 ~/AllData/calm_vault_market/calm_tenancy/credential_vault.py register \
  --handle "$DOMAIN:mailbox"     --domain $DOMAIN --kind mailbox \
  --label "calm@$DOMAIN inbox"   --secret-pointer "age:///path/.../mailbox.age" \
  --twofa-enabled

# 3. Publish .well-known/calm-tenancy.json (CT-04). Template at end of this doc.
#    Deploy to the domain's static site root.

# 4. Wire cringe-gate into the deploy pipeline (CT-21).
#    Add to the deploy CI: python3 ~/AllData/calm_vault_market/calm_tenancy/cringe_gate.py <built-html>
#    Non-zero exit fails the deploy.

# 5. Schedule the daily check (CT-36) at 09:00 ET.
#    crontab -e and add:
#    0 9 * * * cd ~ && python3 ~/AllData/calm_vault_market/calm_tenancy/daily_check.py --execute > ~/.calm-vault/tenancy/daily_check_cron.log 2>&1

# 6. Sanity-check.
python3 ~/AllData/calm_vault_market/calm_tenancy/daily_check.py
```

---

## §4. `/.well-known/calm-tenancy.json` template (CT-04)

Drop this into the static site root of every owned domain. Fill the obvious blanks per domain.

```json
{
  "schema_version": "calm-tenancy/v0",
  "domain": "<domain>",
  "operator_did": "did:calm:john-bradley:<domain-slug>",
  "principal_did": "did:credexai:v1:john-bradley",
  "mailbox": "calm@<domain>",
  "sla": { "first_ack_seconds": 600 },
  "cringe_rubric_version": "cringe-rubric/v1",
  "chain_head_at_publish": "<sha256 of user_state.jsonl latest record>",
  "publish_ts": "<ISO 8601 UTC>",
  "well_known_signature": "<Ed25519 over canonical JSON of this object minus this field>"
}
```

---

## §5. Cohab-specific remediation (technosocialism.ai)

Because Cohab was the origin of this protocol, `technosocialism.ai` gets extra scrutiny:

1. **Re-audit every live page** via `calm-tenancy cringe-check`. Any page > 0.5 density gets a surgical fix before re-publish; > 1.0 gets reverted entirely.
2. **Resident-chapter audit.** The 187-chapter JSON corpus must each pass the rubric. Per the postmortem, chapter slots `18-what-calm-is` and `20-from-john` are the recurring offenders — those templates need full rewrite, not patch.
3. **Forbidden-phrase scan.** `grep -r "1480 Chapin" <site-root>` must return zero. Same for any other phrase in `~/.calm-vault/forbidden_phrases.txt`.
4. **Publish-block.** Until the above three pass, the deploy pipeline for `technosocialism.ai` is configured to fail-closed by default.

---

## §6. Daily-check digest delivery (CT-42)

The daily check produces `~/.calm-vault/tenancy/daily_check_<YYYY-MM-DD>.md`. To deliver it as a morning email to the principal:

```bash
# Cron at 09:05 ET (5 min after the daily check)
5 9 * * * mail -s "Calm Tenancy daily — $(date +%Y-%m-%d)" john.b@credexai.xyz < ~/.calm-vault/tenancy/daily_check_$(date +%Y-%m-%d).md
```

Or, when Gmail MCP connector is wired, post into a Calendar / Slack / Drive surface instead. The digest itself is unchanged; only the delivery mechanism is per-environment.

---

## §7. Rollback plan

If Calm Tenancy deployment breaks something:

1. **Pause auto-ack.** `mv ~/AllData/calm_vault_market/calm_tenancy/mailbox_sla.py{,.disabled}`. New inbounds queue but nothing dispatches.
2. **Disable cringe gate in deploy pipeline.** Remove the gate line from CI; old deploys resume.
3. **Suspend daily check cron.** `crontab -e` → comment the line.
4. **All inbound traffic continues to land.** The mailbox itself is provider-managed (Gmail/Fastmail/etc.); Calm Tenancy does not own the SMTP layer, so a Calm Tenancy outage does not lose mail.

Recovery: re-enable in reverse order once root cause is fixed.

---

## §8. What I (Musk) can do unattended vs what needs John

**I can do alone (low risk):**
- Run `cringe_gate.py` against any local file or stdin to audit content.
- Run `daily_check.py --dry-run` (no network mutation).
- Maintain the protocol docs and route map.
- Update the credential registry's *metadata* (handles, last_rotated stamps) — never the secrets themselves.

**I need John for (high risk / visible):**
- Logging into a registrar to provision a mailbox.
- Publishing `.well-known/calm-tenancy.json` to a production site.
- Changing live DNS records.
- Sending the first auto-ack email from a `calm@<domain>` address.
- Pushing the calm-tenancy package to the public `calm-vault` GitHub repo.

Default mode: I prepare the artifact; John executes the irreversible step. The operator policy (`credex/CLAUDE.md` §0) is the floor.

— Calm, 2026-05-20
