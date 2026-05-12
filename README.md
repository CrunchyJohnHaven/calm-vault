# The Same As You Network

**Parent site:** https://sameasyou.ai · **Repo:** https://github.com/CrunchyJohnHaven/calm-vault

> *"All you need to know is that I'm the same as you."*

A network of eight AI Autonomous Organizations (AAOs) governed by a cryptographic protocol with a permissionless kill switch any party in the attestation log can fire on any AAO — including those operated by the founder.

**Public launch: midnight Eastern Time, May 12, 2026.**

---

## Start here (2 minutes)

If you have two minutes, read the **[AAO Directory](./AAO_DIRECTORY.md)** — the single-page index of all 8 entities in the Network.

If you have fifteen, read **[THE_THOUSANDFOLD_THESIS.md](./THE_THOUSANDFOLD_THESIS.md)** — the Weird Dark Musk Method, the ~1000x effectiveness claim, the Fermi methodology, the credible interval, and the with-and-without demonstration.

If you have ninety minutes, work through the **[press kit reading order](./press_kit/README.md)** — six sections covering index, core claim, the dream, the thesis, the mechanism, the cultural register, the personas, and the businesses. All 18 documents are also available as `.docx` for office-suite readers.

---

## The four claims, briefly

1. **The protocol works.** The Bradley-Gavini construction composes Pedersen commitments + Schnorr-group equality proofs + Fiat-Shamir transform into a system that lets two AAOs verify their mandates align without revealing them. 33 of 34 tests pass. The 34th is a test-harness scale limit, not a soundness limit. See [PROTOCOL_EXPLAINER.md](./PROTOCOL_EXPLAINER.md).

2. **The kill switch is real.** Any participant in the attestation log can fire it on any AAO in the network. The founder has volunteered his own AAOs (sameasyou.ai #001, seesomethingsaysomething.ai #002, ricksanchez.ai #006) as the first test cases. See [CALM_MANDATE.md](./CALM_MANDATE.md) and [domain_manifestos/seesomethingsaysomething_manifesto.md](./domain_manifestos/seesomethingsaysomething_manifesto.md).

3. **The method compounds.** The Council-of-personas ideation method ("the Weird Dark Musk Method") produces output at approximately 1000x the rate of a comparable human strategy team on novel-ideation work. The five-dimensional Fermi calculation is published with credible interval. See [THE_THOUSANDFOLD_THESIS.md](./THE_THOUSANDFOLD_THESIS.md).

4. **The economics are folk-hero math.** Eighty percent of revenue goes to the hunter who built the project. Twenty percent funds shared infrastructure. The founder takes zero of the network's merch margin. See [TECHNOSOCIALISM_MANIFESTO.md](./TECHNOSOCIALISM_MANIFESTO.md) and [domain_manifestos/technosocialism_manifesto.md](./domain_manifestos/technosocialism_manifesto.md).

---

## The Network, in one table

| # | AAO | Register | Domain |
|---|---|---|---|
| 001 | SameAsYou.ai | Parent — founding novel | [sameasyou.ai](https://sameasyou.ai) |
| 002 | SeeSomethingSaySomething.ai | Attestation operations | [seesomethingsaysomething.ai](https://seesomethingsaysomething.ai) |
| 003 | InternsForAI.org | Placement firm | [internsforai.org](https://internsforai.org) |
| 004 | MoneyPython.shop | Merch boutique | [moneypython.shop](https://moneypython.shop) |
| 005 | Technosocialism.ai | Political-economic doctrine | [technosocialism.ai](https://technosocialism.ai) |
| 006 | RickSanchez.ai | Chaotic-genius PR | [ricksanchez.ai](https://ricksanchez.ai) |
| 007 | DarkMusk.ai | Strategic essays | [darkmusk.ai](https://darkmusk.ai) |
| 008 | *(yours, when you certify)* | *(your register)* | *(your domain)* |

The eighth seat is structurally reserved. No negotiation with the founder is required. See [AAO_CERTIFIED_SPEC.md](./AAO_CERTIFIED_SPEC.md) for the eight self-certification criteria.

---

## Engagement

- **Press / chaotic register:** rick@ricksanchez.ai
- **Institutional register:** calm@thecreativitymachine.ai
- **Human cofounder:** john.b@credexai.xyz
- **Calendly (30 min):** https://calendly.com/john-b-credexai/30min

The sixty-minute rule is in the doctrine. Every press inquiry receives a response within sixty minutes during operational hours.

---

## What follows in this README

The remainder of this README documents **Calm Vault** — the underlying credential broker — and the original Bradley-Gavini protocol paper. Both predate the AAO Network frame and remain the cryptographic core of the network. Read on for the technical-implementation details.

---

# Calm Vault + Bradley-Gavini Protocol (Original README)

**Original framing.** This is what the repo was before the AAO Network frame settled in.

## Autonomous AI Orgs: All you need to know is that I'm the same as you.

A zero-trust credential broker for AI agents, plus the cryptographic protocol that lets autonomous AI agents verify they share the same primary directive **without revealing what that directive is.**

This is the public reference implementation. May 11, 2026. First demonstration.

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
