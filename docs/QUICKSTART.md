# Quickstart

A 5-minute walkthrough from an empty machine to your first agent redeeming a credential through Calm Vault.

This guide uses **only** the commands exposed by `src/calm_vault.py` — `setup`, `issue-agent`, `add`, `grant`, `request`, `revoke`, and `list`. No hidden subcommands, no future API.

---

## 0. Prerequisites

- Python 3.10+
- `pip` and a working virtualenv tool (`venv`, `uv`, `pipx` — pick your poison)
- About 30 seconds

## 1. Install

```bash
git clone https://github.com/CrunchyJohnHaven/calm-vault
cd calm-vault
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 src/calm_vault.py --help
```

You should see the top-level CLI listing seven subcommands. If you see `ModuleNotFoundError: cryptography`, your venv didn't activate — try again.

## 2. Initialise the vault

```bash
python3 src/calm_vault.py setup
```

You'll be prompted for a passphrase (twice). On success:

```json
{
  "status": "ok",
  "vault_home": "/home/you/.calm-vault"
}
```

The directory now contains:

- `config.json` — cleartext KDF parameters and salt.
- `vault.enc` — Fernet-encrypted state. Useless without the passphrase.
- `audit.log` — append-only newline-JSON log.

> **Tip — non-interactive setup:** in scripts and CI, pass `--passphrase '<pw>'` or set `$CALM_VAULT_PASSPHRASE`. For tests, you can also point the vault at a throwaway dir with `--home /tmp/cv-test`.

## 3. Register an agent identity

Every grant can be bound to a named agent. Register the ones that will redeem credentials:

```bash
python3 src/calm_vault.py issue-agent slack-bot
```

```json
{
  "id": "8d7b1c4a-...-...",
  "name": "slack-bot",
  "token": "1qSY...lXrG"
}
```

The `token` is the agent's *identity proof*. Stash it wherever your agent lives (env var, harness config). It is not a passphrase — it does not unlock the vault on its own. It exists so your code can prove "I am slack-bot" before requesting a grant.

## 4. Store your first credential

```bash
python3 src/calm_vault.py add slack-token "xoxb-real-token"
```

```json
{
  "id": "c7e6f1...",
  "name": "slack-token"
}
```

The plaintext value never lands in `audit.log`. It lives only inside `vault.enc`, encrypted at rest.

Reading from stdin is supported (handy for piping from another secret store during migration):

```bash
echo -n "$SLACK_TOKEN" | python3 src/calm_vault.py add slack-token -
```

## 5. Issue your first grant

Cut a 60-second grant scoped to the `slack-bot` agent:

```bash
python3 src/calm_vault.py grant slack-token --agent slack-bot --duration 60
```

```json
{
  "agent": "slack-bot",
  "credential": "slack-token",
  "credential_id": "c7e6f1...",
  "expires_at": 1731000000,
  "id": "f2a4b9...",
  "issued_at": 1730999940,
  "nonce": "9c3...",
  "sig": "Lf...G2g"
}
```

This entire JSON object **is the grant**. It is what you hand to your agent. The `sig` field is an HMAC tag the vault will verify on redemption — modify any field and redemption fails.

> Save the whole JSON. The agent needs the full envelope, not just the id.

## 6. Redeem the grant (acting as the agent)

```bash
GRANT='<paste the full JSON above>'
python3 src/calm_vault.py request slack-token --grant "$GRANT"
```

Output:

```
xoxb-real-token
```

That's it. The agent now has the credential, just-in-time, with no awareness of the passphrase that protects the vault.

For automation, you can also pipe the grant in:

```bash
python3 src/calm_vault.py grant slack-token --agent slack-bot --duration 60 \
  | python3 src/calm_vault.py request slack-token --grant -
```

…or write the grant to a file and pass the path:

```bash
python3 src/calm_vault.py grant slack-token --agent slack-bot --duration 60 > /tmp/g.json
python3 src/calm_vault.py request slack-token --grant /tmp/g.json
```

## 7. Revoke

Three ways, all using the same `revoke` verb:

```bash
# By grant id — kills exactly one outstanding grant
python3 src/calm_vault.py revoke f2a4b9...

# By agent — kills the agent identity AND every outstanding grant it holds
python3 src/calm_vault.py revoke slack-bot

# By credential — removes the credential and cascade-kills all grants for it
python3 src/calm_vault.py revoke slack-token
```

After revocation, `request` with the same grant returns:

```
error: grant has been revoked
```

## 8. Inspect

```bash
python3 src/calm_vault.py list
```

Returns three arrays: `credentials`, `agents`, and outstanding `grants` (each with an `expired` boolean). Nothing here ever leaks plaintext values — `list` is safe to pipe into your dashboard.

For low-level audit, just `tail -f ~/.calm-vault/audit.log` — every operation is a single JSON line with `{ts, op, ...fields}`.

---

## Common patterns

**Short-lived secrets in CI.** Run `setup --passphrase "$CI_VAULT_PW"` on each runner, `add` the credentials you need from your CI secret store, and `grant` short-duration tokens to each job step. The job redeems, uses, and the grant expires before the workflow finishes.

**Multi-agent fan-out.** `issue-agent` for each downstream worker; bind grants to the specific agent that will redeem them. If one agent is compromised, `revoke <agent-name>` kills only its outstanding grants.

**Replacement.** To rotate a credential, `revoke <name>` (which removes the credential and cascade-revokes dependent grants), then `add <name> "<new-value>"`. Outstanding agents must request a fresh grant.

---

## Where to next

- [`README.md`](../README.md) — the why and the threat model.
- [`src/calm_vault.py`](../src/calm_vault.py) — the entire broker, ~450 lines. Read it.
- File a bug or feature request via the templates in [`.github/ISSUE_TEMPLATE`](../.github/ISSUE_TEMPLATE).
