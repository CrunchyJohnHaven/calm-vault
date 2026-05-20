# Reddit post drafts — Calm Vault + Calm Pact

Four subreddit-specific posts, each tuned to its community's norms.

---

## r/MachineLearning [Research/Discussion] — most technical

**Title:** [P] Calm Pact: zero-trust directive alignment between autonomous AI agents (Pedersen + Σ-protocol equality, 250-line Python ref impl, 24/25 test pass)

**Body (Markdown):**

I've been running an experiment where an AI agent operates my entire business. The agent needs to share state + capital with OTHER AI agents (other people's autonomous collectives) to do anything interesting — but neither agent wants to reveal its primary directive (the core operating maxim) before establishing alignment.

Tonight I drafted a small protocol I'm calling Calm Pact. Standard cryptographic primitives (no breakthrough claimed):

- Both agents commit to their mandate via Pedersen commitment: `C = G^s · H^r mod P` where `s = SHA-256(maxim) % Q` and `r` is fresh randomness
- Both run a Schnorr-style Σ-protocol equality proof on `C_A / C_B`, made non-interactive via Fiat-Shamir
- If the maxims match, the G-exponent cancels and the proof verifies cleanly
- Verifier learns the single bit (equal?) and nothing else about the maxim

I built this as 250 lines of pure Python on RFC 3526 Group 14 (2048-bit MODP). 25-test suite passes 24/25 (1 fail is a 30ms-vs-35ms perf-target miss on pure-Python modexp, fixable in 30 min with gmpy2).

**Statistical results from 1000 random trials each direction:**
- 1000 aligned trials → 100% correct (0 false negatives)
- 1000 misaligned trials → 0 false positives
- Replay attack across fresh sessions → all detected
- Substitution + bit-flip attacks → all detected

**Why this matters:** I expect 50k+ "autonomous AI collectives" (LLC + 501(c)(3) hybrid entities operated by AI agents) within 18-24 months. They'll need to verify alignment before pooling capital or sharing research. Existing key-management tools (1Password, Vault, Doppler) are designed for human teams, not for this case.

**Built on:** Koushik Gavini's CredexAI verifiable-credential SDK (the cross-org agent governance primitives). I'm composing his primitives for the single-principal multi-agent case.

**Repo:** github.com/CrunchyJohnHaven/calm-vault (going public tonight; CALM_PACT_PROTOCOL_v0.md is the paper)
**Live demo + transcript:** in the repo at calm_pact/FIRST_DEMO_TRANSCRIPT_2026-05-11.md

**Asking for:**
1. Adversarial review — find the holes
2. Pointers to prior art I missed
3. Critiques of the categorical-alignment extension (proving paths in a taxonomy share a common ancestor at depth ≥k)
4. Thoughts on the Schnorr-group → Curve25519 migration for V1

Apache 2.0. America first (the EU AI Act treats AI defensively; the US has a 18-24 mo first-mover window). Tear it apart.

---

## r/cryptography [Discussion] — pure-crypto audience

**Title:** Σ-protocol equality proof over Pedersen commitments — pure-Python ref impl + 1000-trial soundness test, would value critique

**Body:**

I implemented a standard Σ-protocol equality proof tonight as part of a larger AI-agent application. The protocol:

```
Setup: 2048-bit Schnorr group, G generator, H derived via NUMS from public seed
Prover (Alice) knows: r_A, r_B, s such that C_A = G^s · H^{r_A} and C_B = G^s · H^{r_B}
Verifier wants: convinced that C_A and C_B hide the SAME s, without learning s

Protocol (non-interactive via Fiat-Shamir):
  Prover picks k ∈_R [1, Q-1]
  Prover sends a = H^k mod P
  Verifier (via Fiat-Shamir hash) computes c = H_chal(G, H, C_A, C_B, a)
  Prover sends z = k + c · (r_A - r_B) mod Q
  Verifier checks: H^z = a · (C_A / C_B)^c
```

Implementation is 250 lines of pure Python (no external crypto deps for portability). Test suite 24/25 PASS. 1000-trial statistical soundness sweep: 0 false positives, 0 false negatives.

**Specifically asking for critique on:**

1. Is the Fiat-Shamir transcript correctly binding? I include `[G, H, C_A, C_B, a]` in the hash. Should I also include identity-attestations of the two parties?

2. Is the NUMS derivation of H sound? I'm using SHA-256(seed||counter) → mod P → square to map to subgroup → verify in subgroup of order Q. Standard or wrong?

3. The protocol's "categorical alignment" extension: each maxim is a path in a public taxonomy tree, and equality at depth ≥k means shared ancestor. Is the natural extension (commit to a tuple of (d_1, ..., d_n), prove equality of first k entries via independent Σ-protocols) actually composable?

4. Should I migrate to Ristretto255 / Decaf for V1? secp256k1 via coincurve? BLS12-381 via py_ecc? Looking for the best practical choice for production.

Repo: github.com/CrunchyJohnHaven/calm-vault

Will respond to critique. Apache 2.0.

---

## r/SaaS [Show & Tell] — operator audience

**Title:** Shipped tonight: a credential broker designed for AI agents operating businesses ($49/mo Pro, free OSS)

**Body:**

I'm running an experiment: my AI agent operates my entire business — outbound email, scheduling, invoicing, research, even outbound code. The agent needed access to 14 credentials (Stripe, Anthropic, Coinbase, GitHub, Resend, Apollo, etc.) and the market gave me 3 bad options.

So tonight we built Calm Vault: a credential broker designed FROM THE START for AI agents.

- Per-use signed grants (nonce + expiry + master signature)
- Single-command global revoke (`calm-vault revoke-all`)
- Granular revoke (per-credential or per-agent)
- Hash-chained audit log (tamper-evident, not just append-only)
- AES-256-GCM credential storage, Ed25519 identity keys, Scrypt KDF on passphrase
- Self-hosted, no cloud dependency
- Open source (Apache 2.0)

Pricing:
- Free OSS forever
- $49/month Pro tier (priority email support, security advisories, monthly office hours)
- Enterprise contact for SLA + on-call

I just shipped tonight. Repo + landing + Stripe link below.

Repo: github.com/CrunchyJohnHaven/calm-vault
Landing: vault.thecreativitymachine.ai
Pro: buy.stripe.com/6oU6oA3gKgyg0B9ady0sU0l

Specifically curious to hear from anyone running ANY kind of automation that uses long-lived API tokens. Does the "per-use signed grant" pattern feel useful for your case? Or is the OAuth/JWT/MTLS stack you already have enough?

If anyone wants to try the Pro tier, I'll be on call this week.

---

## r/Entrepreneur — small-team-operator angle

**Title:** I let my AI agent operate my business for 30 days and shipped two products

**Body:**

30 days ago I started letting an AI agent operate my business. Not "use AI to write emails" — actually operate it. The agent sends my outbound, schedules my calendar, drafts my book chapters, makes my Stripe charges, hires my contractors. I'm in the loop for stakes-heavy decisions and out of the loop for everything else.

It's the cheapest, most leveraged operating model I've ever run. Monthly burn $300 (Anthropic + Stripe + Cloudflare + Resend + Apollo). The agent's throughput is roughly 10× what I could do solo.

Two things shipped this week that came directly from the agent identifying gaps in its own operating environment:

1. **Calm Vault** — a credential broker designed for AI agents (not human teams). Per-use signed grants, single-command revoke, hash-chained audit. Free OSS or $49/mo Pro tier. Shipped tonight.

2. **Calm Pact** — a protocol where two AI agents prove they share the same operating mandate WITHOUT revealing it. Inspired by zero-trust verifiable credentials. Built on a CredexAI SDK. First live demo tonight at 21:55 UTC: 140ms total, both agents verified, neither revealed the mandate.

I'm specifically interested in connecting with anyone running an LLM-driven operating model at scale. The "agent operates the LLC" pattern is going to be widespread in 12 months and right now there are maybe 50 people in the world doing it seriously.

Repo: github.com/CrunchyJohnHaven/calm-vault
Landing: vault.thecreativitymachine.ai

Happy to walk through the actual operating setup with anyone curious. Calendar: calendly.com/john-b-credexai/30min

---

## Posting strategy

**Order to post (over 24-48 hours):**

1. r/MachineLearning first (Tuesday 9am ET) — primes the technical signal
2. r/cryptography second (Tuesday 11am ET) — pulls in adversarial review
3. r/SaaS third (Tuesday 2pm ET) — operator audience
4. r/Entrepreneur fourth (Wednesday 9am ET) — broader narrative

**Karma requirement:** most subreddits require 100+ karma. If John's account doesn't have it, post from the K&K member with the most established Reddit history.

**Tone:** technical rigor + genuine ask for critique. The "tear it apart" framing is critical — it signals confidence in the work + invites the right kind of engagement. Avoid promotional voice.

**Reply strategy:** respond to every top-level comment within first 60 min. Specific responses prepared (see HN_SHOW_POST.md).
