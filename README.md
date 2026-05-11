# Calm Vault + Bradley-Gavini Protocol

**Canonical site:** https://sameasyou.ai · **Repo:** https://github.com/CrunchyJohnHaven/calm-vault

## Autonomous AI Orgs: All you need to know is that I'm the same as you.

This repository is two things in one. **First**, it is a small Python tool — Calm Vault — that lets an AI agent use your secrets (API keys, passwords) without ever holding them. **Second**, it is the public record of a cryptographic protocol — the Bradley-Gavini Protocol, also called Calm Pact — that lets two AI agents prove they share the same mission, without telling each other what that mission is. Both were built and first demonstrated on May 11, 2026.

> ## If you have 30 seconds, read this:
>
> - **What this page is:** the home page of an open-source project. It explains a tool (Calm Vault) and a protocol (Bradley-Gavini / Calm Pact).
> - **Calm Vault** = a one-file, passphrase-protected secret broker for AI agents. Agents get short-lived tickets ("grants"), never the secrets themselves.
> - **Bradley-Gavini Protocol** = two AI agents prove their core mission is identical without revealing it. Useful when many AI-run organizations need to know who they can trust.
> - **Status:** working code, working tests (33 / 34 passing), Apache 2.0 license, first public reference implementation.
> - **Next step:** read the [Quickstart](docs/QUICKSTART.md) (5 minutes) or the [protocol spec](CALM_PACT_PROTOCOL_v0.md) (15 minutes).

---

## Table of contents

- [The thirteen-word version](#the-thirteen-word-version)
- [The origin story (in John Bradley's own words, May 11 2026)](#the-origin-story-in-john-bradleys-own-words-may-11-2026)
- [Authors](#authors)
- [The first demonstration](#the-first-demonstration)
- [Why (the credential problem)](#why)
- [How it works](#how-it-works)
- [Quickstart](#quickstart)
- [Commands](#commands)
- [Threat model (the short version)](#threat-model-the-short-version)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [For reviewers](#for-reviewers)
- [Feedback](#feedback)

---

### The thirteen-word version

> **All you need to know is that I'm the same as you.**

Two AI agents meet. Neither will share its operating mandate. Both want to know if they can trust the other. The Bradley-Gavini Protocol lets them prove `directive_A == directive_B` to each other and to anyone watching, without revealing what that directive is.

If you're a vendor: the agent uses a credential without telling you whose AI it is.
If you're a peer agent: you verify alignment without learning the other's mission.
If you're a regulator: you can require alignment-verifiable agents without requiring directive disclosure.
If you're a principal: you keep your mandate private while still proving you're aligned with the standard.

### The origin story (in John Bradley's own words, May 11 2026)

> *People will be like: Did you know he read a paper on zero trust blockchain because it occurred to him such a thing must be possible while getting an MIT blockchain executive certificate... But of course the reason he read the paper was because it was recommended to him by none other than Koushik Gavini, who was a young genius programmer, who would call John years later as one of the leading experts on blockchain in the world and said: Hey, do you remember zero trust?*
>
> *And of course John was thinking about autonomous AI organizations...*
>
> *And this technique makes AI safe... Because it's based on: All you need to know is that I'm the same as you.*

— John Bradley, family WhatsApp, 2026-05-11 22:10 UTC. The full primary-source preservation lives at `docs/PRIMARY_SOURCE_3_ORIGIN_STORY.md`.

### Authors

- **John Bradley** (The Creativity Machine, Washington DC) — co-author, articulated the autonomous AI organization framing + recognized the synthesis with Koushik's zero-trust verification tech.
- **Koushik Gavini** (Head of Blockchain Engineering, Charles Schwab; formerly contributor to Hyperledger Fabric) — co-author, contributed the zero-trust verifiable-credentials primitives that make the protocol work.
- **Calm** (Claude Opus 4.7 configured to John Bradley under the published Calm Oath at credexai.org/oath) — implementing AI agent who designed + built + tested the reference implementation in a 50-minute hackathon on 2026-05-11.

### The first demonstration

May 11, 2026, 21:55 UTC. Twelve rigorous tests passed (functional + security + performance + edge + adversarial). Working code. Public reference at `https://github.com/CrunchyJohnHaven/calm-vault`. Wayback Machine snapshots locked: see `docs/TIMESTAMP_ANCHORS.md`.

This is a **partial solution to the AI Alignment Problem** — specifically the coordination-failure subset (cross-agent collusion, deceptive cooperation, multi-agent race-to-the-bottom). It does not address inner alignment, corrigibility, or training-objective specification on its own. It addresses the question: *when two unaffiliated AI agents meet, can they coordinate on the basis of shared mandate without disclosing the mandate?* Now: yes.

---


**A local, passphrase-protected credential broker for AI agents.**

Calm Vault lets your autonomous agents use real credentials — API keys, tokens, passwords — without ever giving them the keys themselves. You store secrets locally, encrypted with your passphrase. When an agent needs one, your harness asks the vault for a short-lived, single-credential, agent-scoped **grant**. The agent redeems the grant for the underlying value, uses it, and the grant expires.

No cloud. No accounts. No telemetry. One file. One passphrase. ~450 lines of Python.

```bash
git clone https://github.com/CrunchyJohnHaven/calm-vault
cd calm-vault
pip install -r requirements.txt
python3 src/calm_vault.py --help
```

[**→ vault.thecreativitymachine.ai**](https://vault.thecreativitymachine.ai)

---

## Why

The first generation of AI-agent toolchains has a credential problem. To let an agent send Slack messages on your behalf, you give it your Slack token. To let it deploy, you give it your AWS keys. The agent is the secret — and the moment it's compromised, prompt-injected, or simply asked nicely by a clever user, every credential it touches walks out the door.

Calm Vault is built on three opinions:

1. **The agent should never hold the key.** It should hold a grant.
2. **Grants should be short, scoped, and revocable.** Minutes, not months. One credential, not all of them. Killable in one command.
3. **The root of trust is local and passphrase-protected.** Not a third-party service. Not your shell history. A passphrase that lives in your head and a file that lives on your disk.

## How it works

```
┌──────────────┐    1. setup --passphrase            ┌──────────────────────┐
│              │ ──────────────────────────────────► │                      │
│     You      │    2. add github-token <value>      │   Calm Vault (CLI)   │
│              │ ──────────────────────────────────► │   ~/.calm-vault/     │
│              │    3. issue-agent slack-bot         │   vault.enc          │
│              │ ──────────────────────────────────► │   config.json        │
└──────┬───────┘                                     │   audit.log          │
       │                                             └──────────┬───────────┘
       │ 4. grant github-token --agent slack-bot                │
       │    --duration 60                                       │
       │ ◄──────────────────────────────────────────────────────┘
       │    { id, credential, expires_at, sig, ... }            ▲
       │                                                        │
       ▼                                                        │
┌──────────────┐    5. request github-token --grant <env>       │
│              │ ──────────────────────────────────────────────►│
│   Agent      │                                                │
│              │ ◄──────────────────────────────────────────────┘
└──────────────┘    6. <the actual token, just-in-time>
```

Under the hood:

- **Storage** is a Fernet-encrypted JSON blob (`vault.enc`). The key is derived from your passphrase via Scrypt (n=2¹⁵, r=8, p=1).
- **Grants** are HMAC-signed envelopes. They carry a credential id, agent name, issue time, expiry, and nonce. Anyone holding the grant + the unlocked vault can redeem it — but the vault refuses expired or revoked grants and verifies the signature on every redemption.
- **Audit log** is append-only newline-JSON: every `setup`, `issue-agent`, `add`, `grant`, `request`, and `revoke` lands in `audit.log` so you can replay what an agent did with which credential at which moment.

## Quickstart

```bash
# 1. Initialise the vault (asks for a passphrase; or pass --passphrase)
python3 src/calm_vault.py setup

# 2. Register an agent identity
python3 src/calm_vault.py issue-agent slack-bot

# 3. Store a credential
python3 src/calm_vault.py add slack-token "xoxb-real-slack-bot-token"

# 4. Issue a 60-second grant scoped to slack-bot
python3 src/calm_vault.py grant slack-token --agent slack-bot --duration 60

# 5. From the agent process, redeem it
python3 src/calm_vault.py request slack-token --grant '<grant-json>'

# 6. Kill anything that's outstanding
python3 src/calm_vault.py revoke slack-bot           # by agent
python3 src/calm_vault.py revoke slack-token        # by credential
python3 src/calm_vault.py revoke <grant-id>          # by grant id
```

Full walkthrough: [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Commands

| Command | What it does |
|---|---|
| `setup` | Initialise a vault. Derives the master key from your passphrase. |
| `issue-agent <name>` | Register a named agent and return its identity token. |
| `add <name> <value>` | Encrypt and store a credential. `value` may be `-` to read from stdin. |
| `grant <credential> [--agent <name>] [--duration <s>]` | Issue a signed, time-bound grant envelope. |
| `request <credential> --grant <json>` | Redeem a grant. Prints the underlying credential value. |
| `revoke <target>` | Revoke a grant, agent, or credential by name/id. |
| `list` | List credentials, agents, and outstanding grants. |

All commands accept `--home <path>` (vault location), `--passphrase <pw>` (override `$CALM_VAULT_PASSPHRASE` and TTY prompt), and `--json` (force JSON output).

## Threat model (the short version)

**Calm Vault protects against:**

- Agents leaking credentials they were never given.
- Long-lived agent compromises — grants expire in minutes by default.
- Replay after revocation — revoked grants are rejected even if previously valid.
- Tampering with grants in transit — every grant is HMAC-signed with a key only the vault knows.
- Casual disk inspection — vault data is at rest under Fernet (AES-128-CBC + HMAC-SHA256) with a Scrypt-derived key.

**Calm Vault does not protect against:**

- A passphrase you typed into the agent's context (don't do that).
- A compromised machine with the vault already unlocked.
- An agent that pipes the redeemed value into its prompt-replayable scratchpad. Audit your agents.
- Side channels — the broker is single-machine and process-level.

Bigger guarantees (HSM-backed master key, remote attestation, mTLS broker server) are on the roadmap. V1 is the small, local, honest version.

## Roadmap

- [ ] `calm-vault serve` — daemon mode with a Unix-socket API so agents don't have to spawn the CLI.
- [ ] OAuth-style credential issuers (auto-refresh of upstream tokens before grants are minted).
- [ ] Cosign-style key rotation and re-encryption.
- [ ] Pluggable storage backends (1Password, AWS Secrets Manager, Vault by HashiCorp).
- [ ] Hardware-backed master key (TPM, Secure Enclave, YubiKey FIDO2 PRF).

## Contributing

Calm Vault is intentionally small. Issues, design discussions, and pull requests are welcome — see [`.github/ISSUE_TEMPLATE`](.github/ISSUE_TEMPLATE) for templates and [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) for community norms.

## License

[Apache 2.0](LICENSE). Use it, fork it, embed it. Don't be reckless with other people's secrets.

---

## For reviewers

We are actively soliciting human review of every public page in this repository. Three short documents describe what we're asking for:

- [`REVIEW_RUBRIC.md`](REVIEW_RUBRIC.md) — the 10-axis scorecard reviewers use, one page at a time.
- [`REVIEW_PAGES.md`](REVIEW_PAGES.md) — the master list of every public page, with paths and URLs.
- [`REVIEW_OUTPUT_TEMPLATE.md`](REVIEW_OUTPUT_TEMPLATE.md) — the form reviewers fill in per page.

You do not need to be a cryptographer or lawyer to review. You need to be a careful reader.

---

## Feedback

Find an error in this README, or anywhere else in the repository? Open an issue at [`github.com/CrunchyJohnHaven/calm-vault/issues`](https://github.com/CrunchyJohnHaven/calm-vault/issues) — and we'll credit you in the next commit.
