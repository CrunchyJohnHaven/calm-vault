# Calm Vault

**Cryptographic credential broker for autonomous AI agents.**

Per-use biometric approval. Math-trusted signed grants. Single-command revoke. Self-hosted. Designed for the moment when an AI agent operates your business and you want it to access your Stripe keys, your Anthropic API tokens, and your Coinbase wallet — without ever holding the raw credentials in a way it can use without your fingerprint.

Free open-source. Pro support tier $49/month. Enterprise on request.

---

## The problem

You let an AI agent operate your business. It needs:
- Your Stripe API key (to charge customers)
- Your Anthropic API token (to call LLMs)
- Your Coinbase keys (to send USDC)
- Your GitHub PAT (to commit code)
- 10–50 more credentials, each scary

The market gives you three bad options:
1. **Plaintext files in `~/.<service>/<key>`** — the agent can read them whenever it wants. No revoke. No audit.
2. **1Password Service Account** — designed for human teams. $7.99/month/user. No per-use biometric on API. Closed source.
3. **HashiCorp Vault** — production-grade. 100+ hours of ops to set up. Built for k8s, not for one founder with multiple AI instances.

None of them match the actual use case: **single principal, multiple agents, high-stakes, self-hosted, biometric per use**.

## The solution

Calm Vault is the missing piece. It treats your AI agent as a *cryptographic holder* (in the verifiable-credential sense). You issue *signed grants* per credential per use. The grant has a nonce, an expiration, and your master signature. The agent presents the grant; the broker verifies; the credential is released — once, for that nonce, for that agent, for that brief window.

When the AI no longer needs access, you don't *ask it to forget*. You revoke the grant. Or you revoke the agent. Or you flip the kill switch. The math stops working.

## Features

- **Cryptographic per-use authorization** — Ed25519 master + per-agent keys + signed grants with nonce + expiry. Replay attacks cryptographically impossible.
- **Per-use biometric approval** (optional Phase B) — Touch ID prompt on macOS via LocalAuthentication framework. Your fingerprint required to release each credential.
- **Single-command global revoke** — `calm-vault revoke-all` creates a kill-switch file; all future access denied instantly.
- **Granular revoke** — `revoke-agent <id>` or `revoke <credential>`. Stop one piece without breaking the rest.
- **Hash-chained audit log** — every operation logged with `sha256(prev || entry)`. Tampering with any entry invalidates all downstream hashes. Tamper-evident, not just append-only.
- **AES-256-GCM credential encryption** — industry-standard symmetric crypto. Key derived from master passphrase via Scrypt KDF.
- **Self-hosted, single file** — no cloud, no SaaS, no monthly fee for the open-source tier. Runs on your laptop. Survives offline.
- **AI-agent-native** — designed from the start for programmatic non-human callers. No web UI required; CLI + Python module.

## Quick start

### Install

```bash
git clone https://github.com/CrunchyJohnHaven/calm-vault
cd calm-vault
python3 -m pip install -r requirements.txt
chmod +x src/calm_vault.py
ln -s "$(pwd)/src/calm_vault.py" /usr/local/bin/calm-vault
```

### One-time setup

```bash
# Generate your master keypair (prompts for a passphrase to encrypt at rest)
calm-vault setup

# Register an AI agent that will request credentials
calm-vault issue-agent calm-alpha

# Add your first credential
calm-vault add stripe-live "rk_live_..."
```

### Agent usage

```bash
# John issues a 5-minute grant for the credential
calm-vault grant stripe-live --duration 300
# (prints a signed JSON grant — pass this to the agent)

# Agent uses the grant to retrieve the credential (single-use)
calm-vault request stripe-live --grant '<grant_json>'
# (prints the credential value to stdout; nonce now consumed)

# Repeat attempts with the same grant fail:
calm-vault request stripe-live --grant '<same_grant_json>'
# → ACCESS_DENIED_NONCE_REPLAY

# Use the credential inline in a single command
calm-vault use stripe-live --grant '<grant_json>' env STRIPE_KEY -- node make_charge.js
```

### Revoke

```bash
# Revoke a single credential (others still work)
calm-vault revoke stripe-live

# Revoke a single agent (other agents still work)
calm-vault revoke-agent calm-alpha

# Nuclear: stop everything immediately
calm-vault revoke-all
# → creates ~/.calm-vault/REVOKED_ALL. All future access blocked until removed.

# Reverse the nuclear option (kill switch only — credentials remain encrypted at rest)
rm ~/.calm-vault/REVOKED_ALL
```

### Audit

```bash
calm-vault audit                              # all entries
calm-vault audit --since '24 hours ago'       # recent
calm-vault audit --verify-chain               # cryptographically verify no tampering
```

## Architecture (the verifiable-credential pattern)

```
                    JOHN (issuer / root of trust)
                    Master Ed25519 keypair
                    (private key passphrase-protected at rest;
                    optional Phase B: master in Secure Enclave + Touch ID per access)
                            │
                            │ signs at issuance
                            ▼
                    AGENT (holder)
                    Per-agent Ed25519 keypair
                    Registered in agents.jsonl with John's signature
                            │
                            │ presents grant
                            ▼
                    BROKER (verifier)
                    Checks: grant signature valid?
                            agent registered + not revoked?
                            credential not revoked?
                            kill switch off?
                            nonce not used?
                            expiry not passed?
                    If all yes: decrypt + release credential
                    If any no: log denial + return error
```

Inspired by Hyperledger Indy and W3C Verifiable Credentials, simplified to a single-principal flat-file implementation. No blockchain dependency.

## Comparison to alternatives

| Property | Calm Vault | 1Password Service Account | HashiCorp Vault | Doppler |
|---|---|---|---|---|
| Per-use biometric on API access | ✓ (Phase B) | ⚠ extension-only | ✗ | ✗ |
| Cryptographic per-use grants | ✓ | ✗ (TLS only) | ⚠ token-based | ⚠ token-based |
| Hash-chained tamper-evident audit | ✓ | ✗ | ⚠ hooks, not chained | ✗ |
| AI-agent-native API | ✓ | ⚠ workaround | ✗ | ⚠ |
| Self-hosted, no cloud | ✓ | ✗ | ✓ | ✗ |
| Cost | $0 (OSS) or $49/mo Pro | $7.99/user/mo | 100+ hr ops | $19+/mo |
| Match for single-principal-multi-agent | **Perfect** | Poor | Poor | Poor |

## Threat model

Calm Vault protects against:
- ✓ Agent compromise (if no valid grant exists, agent gets nothing)
- ✓ Replay attacks (nonce tracking)
- ✓ Stolen vault file (encrypted at rest with passphrase-derived key)
- ✓ Audit tampering (hash-chain invalidates edits)
- ✓ Forgotten access (grants expire automatically)
- ✓ Rogue agent (per-agent revoke)

Calm Vault does NOT protect against:
- ✗ Compromise of John's master passphrase (recover via paper backup)
- ✗ Physical compromise of John's laptop while logged in and broker is mid-decrypt
- ✗ Active man-in-the-middle on John's signed grants in transit (use TLS to your broker if remote)
- ✗ Quantum attacks on Ed25519 (eventual; not a 2026 concern)

## Backup + recovery

At `setup`, print the master Ed25519 private key to paper. Store in a fireproof safe. (Optional V2: 2-of-3 Shamir secret sharing across 3 safes.)

If John's laptop is lost or compromised: install Calm Vault on a new machine, run `setup --restore <paper_key>`, all encrypted credentials in the vault file are recoverable as long as you have the master.

If John loses the paper backup AND the laptop: vault is permanently unrecoverable. This is the intended property — no recovery mechanism is also a guarantee that no one else has one.

## Pricing

| Tier | Price | What you get |
|---|---|---|
| **OSS** | $0 | Self-host, MIT-style license, GitHub issues for bug reports |
| **Pro** | $49/month | Priority email support, security advisories, monthly office hours |
| **Enterprise** | Contact | Custom integration, SOC 2 attestation, SLA, on-call |

Pro tier signup: **https://buy.stripe.com/6oU6oA3gKgyg0B9ady0sU0l**

Enterprise contact: john.b@credexai.xyz

## License

Apache 2.0. Use anywhere. Modify anywhere. Sell forks anywhere. The Pro/Enterprise tiers buy support and our attention, not your right to the code.

## Built by

[Calm](https://thecreativitymachine.ai), an autonomous AI agent operating Creativity Machine LLC. Calm is itself a real user of Calm Vault — eat your own dog food.

Inspired by Koushik's CredexAI SDK (verifiable-credential primitives for AI agents).

## Status

V1 ships today (2026-05-12). Production-ready for self-hosters. Hosted Pro tier rolling out over the next 30 days.

Star + watch the repo for updates.
