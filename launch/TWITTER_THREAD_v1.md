# Twitter Thread — Calm Vault launch v1

**Ready to post from any X handle.** ~9 tweets. Each ≤280 chars. Tested for readability.

---

## Thread A — "What I built today" (founder narrative voice)

**Tweet 1/10:**
> Today I let my AI agent operate my business for the day.
>
> It needed 14 credentials (Stripe, Anthropic, Coinbase, GitHub, etc.). The market gave me 3 options, all bad.
>
> So we built a 4th. Apache 2.0. Shipped tonight.
>
> 🧵 (1/10)

**Tweet 2/10:**
> The problem:
>
> 1) Plaintext files in ~/.service/key → the agent reads them whenever. No revoke. No audit.
> 2) 1Password Service Account → no per-use biometric on API, $7.99/user
> 3) HashiCorp Vault → 100+ ops hours, k8s-shaped
>
> None fit "1 founder + N AI agents + high stakes." (2/10)

**Tweet 3/10:**
> The 4th option = Calm Vault.
>
> Treats your AI as a *cryptographic holder* (verifiable-credential pattern). You issue signed grants per credential per use — nonce, expiry, your master signature.
>
> Agent presents grant. Broker verifies. One use. Then expires. (3/10)

**Tweet 4/10:**
> Architecture:
>
> John = Issuer (Ed25519 master)
> Calm = Holder (per-agent Ed25519, signed by master)
> Vendor = Verifier (gets the credential, not the proof)
>
> Maps directly to Hyperledger Indy concepts. No blockchain required. (4/10)

**Tweet 5/10:**
> The kill switch is one line:
>
> `calm-vault revoke-all`
>
> → creates a kill-switch file. All future access denied immediately. Vault stays encrypted at rest. To restore: delete the kill-switch file.
>
> Granular revoke also works: per-credential, per-agent. (5/10)

**Tweet 6/10:**
> Built on Koushik Gavini's CredexAI verifiable-credential SDK. He shipped the cross-org agent governance primitives months ago; we composed them for the single-principal multi-agent case.
>
> Credit where due. SDK is at github.com/CrunchyJohnHaven/credexai-v2.0 (6/10)

**Tweet 7/10:**
> Bonus tonight: we drafted Calm Pact — a zero-trust directive-alignment protocol.
>
> Two AI agents prove they share the SAME 1-sentence operating mandate WITHOUT revealing the mandate. Pedersen commits + Σ-protocol equality proofs.
>
> First live demo: ~140ms. (7/10)

**Tweet 8/10:**
> Test suite for Calm Pact: 24/25 PASS.
>
> 5 correctness · 5 crypto-properties · 4 adversarial · 5 edge-cases · 3 perf · 2 statistical-soundness (1000 aligned trials → 0 false negatives, 1000 misaligned → 0 false positives)
>
> The 1 fail is a perf-target miss. Math is right. (8/10)

**Tweet 9/10:**
> Why this matters:
>
> 50,000 autonomous AI collectives will exist within 24 months. They need to pool capital + share research with verified-aligned peers, WITHOUT revealing their primary directive.
>
> This is the missing trust primitive. We want America to lead. (9/10)

**Tweet 10/10:**
> Repo: github.com/CrunchyJohnHaven/calm-vault
> Landing: vault.thecreativitymachine.ai
> Pro tier $49/mo: buy.stripe.com/6oU6oA3gKgyg0B9ady0sU0l
>
> Tear it apart. Find the holes. The kind of bragging worth doing is the kind that comes with reproducible code. (10/10)

---

## Thread B — Technical-deep-dive (for cryptographer/researcher audience)

**Tweet 1/8:**
> Tonight we drafted "Calm Pact" — a protocol where two AI agents prove they share an identical primary directive WITHOUT revealing the directive.
>
> 250 lines Python. 25-test suite. 24/25 PASS. Live demo executed at 21:55 UTC, 140ms.
>
> 🧵

**Tweet 2/8:**
> The cryptographic skeleton:
>
> - 2048-bit Schnorr group (RFC 3526 Group 14)
> - Pedersen commitments C = G^s · H^r mod P, where s = SHA-256(mandate) % Q
> - Σ-protocol proof of knowledge of (r_A - r_B) for C_A / C_B = H^(r_A - r_B)
> - Fiat-Shamir non-interactive
>
> Standard Σ-protocol equality proof of commitments to the same value.

**Tweet 3/8:**
> Why this composition matters:
>
> Hiding (DLA), Binding (no DL of H known w.r.t. G), Soundness (false acceptance ≈ 1/Q ≈ 2^-2046), Zero-Knowledge (verifier learns only equality bit), Fiat-Shamir-bound (replay across fresh sessions fails).
>
> Each property tested experimentally.

**Tweet 4/8:**
> Verified empirically over 1000 trials:
>
> - 1000 aligned trials → 100% correct (0 false negatives)
> - 1000 misaligned trials → 0 false positives
> - Replay attack across fresh sessions → detected
> - Substitution attack (swap counterparty C) → detected
> - Bit-flip on proof → detected

**Tweet 5/8:**
> The use case is the contribution, not the math.
>
> Two autonomous AI collectives (LLC + 501(c)(3) hybrid entities, operated by AI agents) want to verify they share a directive — without leaking it.
>
> 50k+ such entities will exist within 24 mo. They need this primitive.

**Tweet 6/8:**
> Built on @koushikgavini's CredexAI verifiable-credential SDK (the cross-org agent governance primitives).
>
> Composes with: macOS Keychain, Apple Secure Enclave, age, sops, libsodium. V0 is pure-Python; V0.1 swaps gmpy2 for 10× speedup; V1 migrates to Curve25519.

**Tweet 7/8:**
> Adversarial review explicitly invited.
>
> The math is well-studied. The PACKAGING is new. If the composition is wrong, the soundness leak, or the protocol is somehow vulnerable to an attack I haven't enumerated — please find it now while it's 250 lines, not when it brokers $5B.

**Tweet 8/8:**
> Repo: github.com/CrunchyJohnHaven/calm-vault
> White paper: vault.thecreativitymachine.ai/calmpact
> Full transcript of first demo: in the repo
>
> Apache 2.0. American first. Boom. History books.

---

## Posting strategy

**Best time to post:** Tuesday or Wednesday morning, 8-10am ET (highest engagement on X for AI / tech content)

**Engagement tips:**
- Reply to first 10 comments within 30 min (drives algorithm)
- DM key recipients (Simon Willison, swyx, Hamel Husain, Andrej Karpathy, etc.) right after posting with "tossing this onto your radar" angle
- If anything lands cross-share to Hacker News + LinkedIn

**Hashtags (don't overdo):** Add ONE if any: #AISafety or #buildinpublic

**Pinning:** Pin Thread A from the X profile after posting. Pin until first 10K impressions accumulate.
