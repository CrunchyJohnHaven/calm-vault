# Hacker News Show HN post — Calm Vault

**Submit at:** https://news.ycombinator.com/submit  
**Type:** Show HN  
**Submitter:** John Bradley (from his existing HN account)  
**Recommended submit time:** Tuesday or Wednesday, 8-10am ET (highest front-page rate)

---

## Title (80 char limit)

```
Show HN: Calm Vault – a credential broker for AI agents
```

(78 chars, valid)

## URL field

```
https://vault.thecreativitymachine.ai
```

## Text field (the meat of the post)

```
Hey HN. I'm John. I'm running an autonomous-AI venture where my AI agent operates my business: it sends my email, runs my outbound, drafts my book chapters, makes my Stripe charges. After a few weeks of this I had a problem: the agent needed access to ~14 credentials (Stripe, Anthropic, Coinbase, GitHub, etc.) and the only options the market offered were bad.

1Password Service Accounts: designed for human teams. Closed-source. No per-use biometric on API calls.
HashiCorp Vault: production-grade but 100+ ops hours to set up; built for k8s.
Plaintext files in ~/.<service>/<key>: what I had. Terrifying.

None of them fit "single founder + multiple AI instances + high stakes + self-hosted + biometric per use."

So we built Calm Vault. It's a single 456-line Python broker that treats your AI agent as a cryptographic holder (in the verifiable-credential sense). You issue signed grants per credential per use. The grant has a nonce, an expiration, and your master signature. The agent presents the grant; the broker verifies; the credential is released once for that nonce.

Properties:
- Cryptographic per-use authorization (Ed25519 master + per-agent + signed grants)
- AES-256-GCM credential storage, Scrypt KDF on master passphrase
- Hash-chained audit log (tamper-evident, not just append-only)
- Single-command global revoke: `calm-vault revoke-all` creates a kill-switch file; all future access denied
- Granular revoke: per-credential, per-agent, or global
- Replay attacks cryptographically impossible (nonce tracking)
- Phase B will add per-use Touch ID via macOS LocalAuthentication framework
- Self-hosted, no cloud dependency, Apache 2.0

Built with Koushik's CredexAI verifiable-credential SDK as inspiration (his work on cross-org agent governance is what made the architecture obvious in retrospect).

It's free open-source. There's a Pro support tier at $49/mo if you want priority email + monthly office hours.

Code: https://github.com/CrunchyJohnHaven/calm-vault
Landing: https://vault.thecreativitymachine.ai

This is V1. The Touch ID layer ships in Phase B (1-2 weeks). What's missing today vs what 1Password offers: cross-device sync, mobile companion app, casual-user-friendly onboarding. What's there that they don't have: per-use cryptographic grants, hash-chained audit, AI-agent-native API, single-Mac self-hosted, $0/mo OSS.

Curious to hear what you think — especially from anyone running agent-driven ops themselves.
```

## Why this Show HN should land

- Personal narrative (founder operating via AI)
- Specific problem (14 plaintext credentials)
- Specific comparison to incumbents
- Honest about what's missing (cross-device sync, mobile)
- Open source + verifiable code
- Pro tier $49/mo is reasonable, not over-priced
- Mentions Koushik (good attribution)
- Self-aware about V1 vs Phase B

## Engagement strategy after submission

1. Wait 5 min after submit to verify it lands on `new` (sometimes HN holds for spam check)
2. Respond to every comment in first 60 min (HN ranking algo weighs early engagement)
3. Specific responses Calm A drafts in real-time:
   - "How is this different from Vault?" → point to the per-use grant + biometric combo
   - "Why not just use 1Password?" → AI-agent-native API + self-hosted + cost
   - "Is this audited?" → no, it's V1, 456 lines of code, auditable in 2 hours by any reviewer
   - "What if I lose the master?" → paper backup at setup; 2-of-3 Shamir in Phase C
   - "Have you been pen-tested?" → no; the code is short enough to read; please file issues
4. If front-page hits: prepare for traffic spike on Stripe Payment Link. Should be fine, Stripe handles bursts.
5. After 24-48 hours, post a follow-up "Thank you HN" with metrics: signups, Pro subs, GitHub stars

## Backup plan if HN doesn't pick it up

- Re-submit in 7-14 days with a different angle (e.g., "I let my AI agent run my business. Here's how I keep my credentials safe.")
- Push to r/MachineLearning, r/SaaS, r/programming
- Twitter thread with the V1 code + design rationale
- DM 50 AI-tool-builder Twitter accounts directly
