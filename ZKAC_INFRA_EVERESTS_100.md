# ZKAC Critical Infrastructure — 100 Engineering Everests

**Route map: the production-grade Zero-Knowledge Attested Credentials infrastructure that makes Calm Pact, Calm Witness, and Calm Mirror composable into a real autonomous-agent ecosystem.**

> *"The protocols are primitives. ZKAC infrastructure is the operating system they run on."*

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.
**Status:** Route v0 · 2026-05-20 · open for adversarial review.
**Companion routes:** [Calm Witness 100](ZKBB_USER_EVERESTS_100.md), [Calm Mirror 100](CALM_MIRROR_EVERESTS_100.md), [Calm Pact](CALM_PACT_PROTOCOL_v0.md).

---

## What ZKAC infrastructure is

A Zero-Knowledge Attested Credential (ZKAC) is the unit of identity in the Calm-family agent ecosystem. It is what an agent presents when it claims to act on behalf of a specific principal under specific authorization, with cryptographic proofs that bind the claim to the principal's vault, the principal's consent, and the operator's CredexAI identity.

Calm Pact uses ZKACs to prove directive equality. Calm Witness uses ZKACs to bind disclosure proofs to a legal entity. Calm Mirror uses ZKACs to attest values evidence. **All three depend on the same underlying credential infrastructure** — and that infrastructure is what this 100-everest route designs.

The user's framing — *"critical infra for agents and ZKACs"* — captures both layers:

- **Agent infrastructure:** how an AI operator binds to a credential, exercises capabilities, gets revoked, recovers from key loss.
- **ZKAC infrastructure:** how credentials are issued, held, presented, verified, and trusted across organizations.

---

## Design constraints (the non-negotiables)

These are the operating-system-level invariants. Any summit violating them is rejected.

1. **Principal authority is absolute.** Only the principal can authorize a credential bearing their identity. Issuers attest; they do not own.
2. **Holder vault sovereignty.** Credentials live in the principal's vault. Issuers and verifiers see only what the principal has authorized to be disclosed.
3. **Verifier independence.** A verifier should be able to verify a credential without negotiating with the issuer at verification time. Online dependencies are degradation, not requirements.
4. **Revocation propagates without identifying the holder.** The verifier learns "this credential is/isn't current" without leaking which credential.
5. **Composability over completeness.** Each summit ships a primitive that composes; we resist building monolithic "ZKAC platforms".
6. **W3C VC + DID compatibility.** Where standards exist, we extend them rather than replace them.

---

## Phase XVII — Foundations (1–10)

**ZKAC Everest 1 — Problem statement & threat model.** *Acceptance:* a versioned doc capturing the actor model (issuer, holder, verifier, principal, agent, ecosystem participants), trust assumptions, and the design constraints above. *Effort:* M.

**ZKAC Everest 2 — Route map (this doc).** *Acceptance:* 100 summits, deps, acceptance tests. *Effort:* M.

**ZKAC Everest 3 — Naming & branding lock.** *Acceptance:* ZKAC as the canonical primitive name; CredexAI as the canonical Calm-family issuer; clear glossary. *Effort:* S. *Prereq:* 1.

**ZKAC Everest 4 — Glossary v0.** *Acceptance:* `ZKAC_GLOSSARY.md` covering issuer, holder, verifier, presentation, predicate, revocation, etc. *Effort:* S. *Prereq:* 3.

**ZKAC Everest 5 — W3C VC compatibility statement.** *Acceptance:* explicit doc enumerating which W3C Verifiable Credentials data-model elements ZKACs use unchanged, which we extend, and what's outside the model. *Effort:* M. *Prereq:* 1.

**ZKAC Everest 6 — DID method spec.** *Acceptance:* `did:calm` method specification compatible with W3C DID Core. *Effort:* M. *Prereq:* 5.

**ZKAC Everest 7 — Issuer-class taxonomy.** *Acceptance:* enumerated issuer classes (state, professional, employer, peer-collective, self-attested) with default trust weights. *Effort:* M. *Prereq:* 1.

**ZKAC Everest 8 — Threat-model coverage matrix.** *Acceptance:* matrix mapping every actor + attack vector to a defense, with empty cells flagged as residual risks. *Effort:* M. *Prereq:* 1.

**ZKAC Everest 9 — Failure-mode catalogue.** *Acceptance:* enumerated failure modes Z01-Z40 with severity ranking. *Effort:* M. *Prereq:* 1, 2.

**ZKAC Everest 10 — Reference architecture.** *Acceptance:* a diagram showing the trust graph: principals, issuers, holders, verifiers, the chain layer, the ZKAC presentation flow. *Effort:* S. *Prereq:* 1.

## Phase XVIII — Issuer Infrastructure (11–25)

**ZKAC Everest 11 — Issuer governance protocol.** *Acceptance:* how a new issuer joins the Calm-family ecosystem: documentation, public audit, key ceremony, vouching by ≥ 2 existing issuers. *Effort:* L. *Prereq:* 7.

**ZKAC Everest 12 — Issuer key ceremony.** *Acceptance:* a documented ceremony for issuer keypair generation: hardware-attested, multi-party, witnessed. *Effort:* L. *Prereq:* 11.

**ZKAC Everest 13 — Issuer key custody.** *Acceptance:* HSM / cloud-KMS / multi-sig options with documented trust trade-offs. *Effort:* M. *Prereq:* 12.

**ZKAC Everest 14 — Issuer key rotation.** *Acceptance:* rotation protocol that doesn't invalidate previously-issued credentials; rotation events are chain-anchored. *Effort:* L. *Prereq:* 12.

**ZKAC Everest 15 — Issuer revocation registry.** *Acceptance:* an issuer-side append-only registry of revoked credentials; queryable without leaking which holder is checking. *Effort:* L. *Prereq:* 11.

**ZKAC Everest 16 — Issuer-to-issuer trust composition.** *Acceptance:* protocol by which one issuer formally endorses another (or formally distrusts); endorsements are chained on a public ledger. *Effort:* L. *Prereq:* 11.

**ZKAC Everest 17 — Status list / CRL spec.** *Acceptance:* W3C-compliant status-list mechanism for credential revocation. *Effort:* M. *Prereq:* 15.

**ZKAC Everest 18 — Verifiable presentation requests.** *Acceptance:* schema for a verifier to request specific credential properties from a holder. *Effort:* M. *Prereq:* 5.

**ZKAC Everest 19 — Issuer audit log.** *Acceptance:* every issuance + revocation is logged on a public transparency log (Sigsum). *Effort:* L. *Prereq:* 11.

**ZKAC Everest 20 — Issuer-class licensing.** *Acceptance:* a tiered licensing structure: experimental / pilot / production-grade issuer, with progressive evidence requirements. *Effort:* M. *Prereq:* 11.

**ZKAC Everest 21 — Issuer slashing protocol.** *Acceptance:* documented consequences when an issuer is caught issuing fraudulent credentials. *Effort:* L. *Prereq:* 19, 20.

**ZKAC Everest 22 — Cross-jurisdiction issuer compliance.** *Acceptance:* matrix of jurisdictional requirements (GDPR, eIDAS, etc.) for issuers operating in each. *Effort:* L. *Prereq:* 11.

**ZKAC Everest 23 — Issuer reputation primitive.** *Acceptance:* a public reputation score for each issuer derived from audit + slash history. *Effort:* L. *Prereq:* 11, 19, 21.

**ZKAC Everest 24 — Issuer ID portability.** *Acceptance:* an issuer can migrate to a new key while preserving their reputation chain. *Effort:* L. *Prereq:* 14, 23.

**ZKAC Everest 25 — Issuer-discoverable public directory.** *Acceptance:* a public, censorship-resistant directory of active issuers with their classes + reputation scores. *Effort:* M. *Prereq:* 23.

## Phase XIX — Holder/Wallet Infrastructure (26–40)

**ZKAC Everest 26 — Holder vault format spec.** *Acceptance:* a versioned binary format for the holder's local credential store. *Effort:* M. *Prereq:* 5.

**ZKAC Everest 27 — Holder key custody.** *Acceptance:* keypair generation + storage spec for holders; HSM / Secure Enclave / passphrase-protected. *Effort:* M. *Prereq:* 26.

**ZKAC Everest 28 — Holder vault encryption at rest.** *Acceptance:* AES-256-GCM with KDF-derived key from principal-controlled passphrase. *Effort:* M. *Prereq:* 27.

**ZKAC Everest 29 — Holder backup.** *Acceptance:* a documented backup procedure that preserves credentials across device loss; off-host encrypted. *Effort:* L. *Prereq:* 28.

**ZKAC Everest 30 — Holder recovery from total device loss.** *Acceptance:* a runbook for re-creating the holder vault from backup + ≥ 2 witness signatures. *Effort:* L. *Prereq:* 29.

**ZKAC Everest 31 — Multi-device holder.** *Acceptance:* a principal can hold the same credentials on N devices simultaneously, with per-device revocation. *Effort:* L. *Prereq:* 27.

**ZKAC Everest 32 — Wallet-to-wallet credential transfer.** *Acceptance:* one principal's holder vault can grant a credential to another principal's holder vault, with explicit issuer + holder + recipient consent. *Effort:* L. *Prereq:* 26.

**ZKAC Everest 33 — Credential expiration & renewal.** *Acceptance:* every credential has an `expires_at`; renewal flow without breaking outstanding presentations. *Effort:* M. *Prereq:* 26.

**ZKAC Everest 34 — Credential aging without breaking proofs.** *Acceptance:* a presentation referencing a recently-rotated credential remains valid during a grace window. *Effort:* M. *Prereq:* 14, 33.

**ZKAC Everest 35 — Multi-credential simultaneous proof.** *Acceptance:* a single ZK presentation proves properties spanning N credentials. *Effort:* L. *Prereq:* 26, 18.

**ZKAC Everest 36 — Cross-credential join queries.** *Acceptance:* "I hold both credential X and credential Y, and X.field_A = Y.field_A" — provable without revealing field_A. *Effort:* L. *Prereq:* 35.

**ZKAC Everest 37 — Privacy-preserving credential discovery.** *Acceptance:* a holder can discover whether they hold a credential matching a verifier's request without revealing which credentials they don't hold. *Effort:* L. *Prereq:* 35.

**ZKAC Everest 38 — Holder consent UI.** *Acceptance:* reference UI for the holder approving / denying / scoping presentations. *Effort:* M. *Prereq:* 26.

**ZKAC Everest 39 — Holder offline mode.** *Acceptance:* a holder can present credentials when offline; presentations work via QR / NFC / Bluetooth. *Effort:* L. *Prereq:* 35.

**ZKAC Everest 40 — Holder activity log.** *Acceptance:* a chain-resident log of every presentation the holder has made; auditable by the principal. *Effort:* M. *Prereq:* 26.

## Phase XX — Verifier Infrastructure (41–55)

**ZKAC Everest 41 — Verifier reference implementation.** *Acceptance:* a clean-room Python verifier in ≤ 2000 LoC that accepts honest presentations and rejects adversarial ones. *Effort:* L. *Prereq:* 35.

**ZKAC Everest 42 — Verifier-as-a-Service architecture.** *Acceptance:* deployment model where third-party verifiers run as services, callable via API; auditable. *Effort:* L. *Prereq:* 41.

**ZKAC Everest 43 — Multi-verifier consensus.** *Acceptance:* a verifier-side protocol where N independent verifiers must agree before a presentation is accepted in high-stakes contexts. *Effort:* L. *Prereq:* 42.

**ZKAC Everest 44 — Verifier reputation.** *Acceptance:* per-verifier reputation primitive composing the Calm-family ecosystem with track-record evidence. *Effort:* L. *Prereq:* 23, 42.

**ZKAC Everest 45 — Verifier discoverability.** *Acceptance:* a public directory of available verifiers + their reputation + their accepted credential types. *Effort:* M. *Prereq:* 44.

**ZKAC Everest 46 — Verifier interoperability tests.** *Acceptance:* a published conformance suite that any verifier implementation runs; results published. *Effort:* M. *Prereq:* 41.

**ZKAC Everest 47 — Verifier license model.** *Acceptance:* tiered license for verifiers (experimental / pilot / production) similar to Everest 20 for issuers. *Effort:* M. *Prereq:* 42.

**ZKAC Everest 48 — Verifier auditability.** *Acceptance:* every verification a verifier performs is logged in their public verifier-side audit log. Privacy-preserving (no leak of holder identity). *Effort:* L. *Prereq:* 41.

**ZKAC Everest 49 — Verifier abuse resistance.** *Acceptance:* a verifier cannot DoS holders via crafted requests; rate-limits and abuse-pattern detection. *Effort:* L. *Prereq:* 41.

**ZKAC Everest 50 — Verifier offline mode.** *Acceptance:* a verifier can verify a presentation when offline if it has the necessary anchor proofs cached. *Effort:* M. *Prereq:* 41.

**ZKAC Everest 51 — Verifier-side disclosure ledger.** *Acceptance:* each verifier records (privacy-preservingly) what they verified, when, and for what claimed purpose. *Effort:* M. *Prereq:* 48.

**ZKAC Everest 52 — Verifier cross-checking.** *Acceptance:* a holder can request a "second opinion" from a different verifier on the same presentation. *Effort:* M. *Prereq:* 43.

**ZKAC Everest 53 — Verifier panic-stop.** *Acceptance:* when a verifier detects a chain anomaly (e.g., issuer key compromise), the verifier halts new acceptances and alerts. *Effort:* L. *Prereq:* 41.

**ZKAC Everest 54 — Verifier panic-recovery.** *Acceptance:* documented procedure for resuming verification after a panic-stop, with explicit checks. *Effort:* M. *Prereq:* 53.

**ZKAC Everest 55 — Verifier slashing protocol.** *Acceptance:* a verifier caught providing false acceptances (e.g., accepting forged presentations) loses license. *Effort:* L. *Prereq:* 47.

## Phase XXI — Agent Identity & Capability (56–70)

**ZKAC Everest 56 — Agent identity primitive.** *Acceptance:* a credential subtype for "agent acting on behalf of principal P under capability set C". *Effort:* M. *Prereq:* 5.

**ZKAC Everest 57 — Agent-operator binding.** *Acceptance:* each agent's credential names the operator (the software + version + organization) running it. *Effort:* M. *Prereq:* 56.

**ZKAC Everest 58 — Capability scope spec.** *Acceptance:* a capability vocabulary v0 (read, write, transact, attest, delegate) with explicit composition rules. *Effort:* L. *Prereq:* 56.

**ZKAC Everest 59 — Capability narrowing.** *Acceptance:* a principal can issue a derivative agent credential with a strict subset of capabilities. *Effort:* M. *Prereq:* 58.

**ZKAC Everest 60 — Capability time-bounding.** *Acceptance:* every capability has an explicit expiration; capabilities don't outlive their issuance moment without renewal. *Effort:* M. *Prereq:* 58.

**ZKAC Everest 61 — Agent rotation.** *Acceptance:* a principal can migrate to a new agent (e.g., upgrading operator software) while preserving outstanding capabilities. *Effort:* L. *Prereq:* 14, 57.

**ZKAC Everest 62 — Agent revocation propagation.** *Acceptance:* when an agent is revoked, all outstanding capabilities expire immediately (within bounded latency). *Effort:* L. *Prereq:* 15, 57.

**ZKAC Everest 63 — Agent-to-agent capability transfer.** *Acceptance:* one agent can hand off a capability to another agent (e.g., for redundancy), with explicit principal authorization. *Effort:* L. *Prereq:* 58, 61.

**ZKAC Everest 64 — Agent witness role.** *Acceptance:* an agent can act as a witness (Calm Mirror Everest 13 / Witness Everest 25) — credentials extend to attestation capacity. *Effort:* L. *Prereq:* 56, [Mirror Everest 13].

**ZKAC Everest 65 — Sub-agent permissions.** *Acceptance:* an agent can issue a sub-agent credential with a strict subset of its own capabilities. *Effort:* L. *Prereq:* 59.

**ZKAC Everest 66 — Agent fingerprinting resistance.** *Acceptance:* documented defenses against fingerprinting attacks that try to identify which operator runs an agent. *Effort:* L. *Prereq:* 57.

**ZKAC Everest 67 — Anonymous agent discovery.** *Acceptance:* one agent can discover another's existence + class without learning identity. *Effort:* L. *Prereq:* 56.

**ZKAC Everest 68 — Agent collusion detection.** *Acceptance:* protocol for detecting when N agents jointly violate their capability scopes through coordination. *Effort:* L. *Prereq:* 58.

**ZKAC Everest 69 — Agent identity recovery.** *Acceptance:* a principal can recover their agent identity after device loss with the same procedure as holder recovery. *Effort:* M. *Prereq:* 30, 56.

**ZKAC Everest 70 — Agent audit log.** *Acceptance:* every agent action takes place against a chained log queriable by the principal. *Effort:* M. *Prereq:* 40, 56.

## Phase XXII — Trust Graph & Reputation (71–85)

**ZKAC Everest 71 — Trust graph data structure.** *Acceptance:* a documented graph schema for "principal P trusts issuer I under conditions C". *Effort:* M. *Prereq:* 16.

**ZKAC Everest 72 — Trust transitivity rules.** *Acceptance:* normative rules for when P trusting I and I trusting J implies P trusting J — and the strict limits of transitivity. *Effort:* M. *Prereq:* 71.

**ZKAC Everest 73 — Trust revocation propagation.** *Acceptance:* when P revokes trust in I, downstream chains update within a documented latency. *Effort:* L. *Prereq:* 71.

**ZKAC Everest 74 — Web-of-trust merging.** *Acceptance:* protocol for combining multiple trust graphs (e.g., from different communities) into a queryable union. *Effort:* L. *Prereq:* 71.

**ZKAC Everest 75 — Trust scoring.** *Acceptance:* a privacy-preserving scoring algorithm: principal P can ask "how much should I trust I?" without revealing who I is. *Effort:* L. *Prereq:* 74.

**ZKAC Everest 76 — Trust gaming defense.** *Acceptance:* defenses against attacks on trust scores (Sybil voting, reputation laundering). *Effort:* L. *Prereq:* 75.

**ZKAC Everest 77 — Sybil resistance primitive.** *Acceptance:* a documented anti-Sybil mechanism — proof-of-personhood, social-graph attestation, or hybrid. *Effort:* XL. *Prereq:* 71.

**ZKAC Everest 78 — Bot detection.** *Acceptance:* defenses against AI-driven creation of fake principals; a per-credential bot-likelihood flag (non-blocking). *Effort:* L. *Prereq:* 77.

**ZKAC Everest 79 — Trust delegation.** *Acceptance:* a principal can delegate trust evaluation to a trusted advisor without giving up their decision authority. *Effort:* M. *Prereq:* 75.

**ZKAC Everest 80 — Trust expiration.** *Acceptance:* every trust assertion has an explicit expiration; trust doesn't outlive its issuance. *Effort:* M. *Prereq:* 71.

**ZKAC Everest 81 — Trust granularity.** *Acceptance:* trust assertions can be per-predicate-class (e.g., I trust this issuer for academic credentials but not financial ones). *Effort:* M. *Prereq:* 71.

**ZKAC Everest 82 — Trust visualization.** *Acceptance:* a public dashboard rendering trust graphs for educational + audit purposes (with privacy preserved). *Effort:* L. *Prereq:* 75.

**ZKAC Everest 83 — Trust API.** *Acceptance:* a public API for trust queries, with rate-limits + abuse resistance. *Effort:* M. *Prereq:* 75.

**ZKAC Everest 84 — Trust slashing.** *Acceptance:* when an entity in the trust graph is caught violating their attestations, their trust score is automatically adjusted downward. *Effort:* L. *Prereq:* 21, 76.

**ZKAC Everest 85 — Trust appeal protocol.** *Acceptance:* a documented appeal process for entities whose trust scores are reduced. *Effort:* M. *Prereq:* 84.

## Phase XXIII — Multi-Party Computation & Threshold Crypto (86–95)

**ZKAC Everest 86 — MPC framework selection.** *Acceptance:* decision doc on the v0 MPC framework (SPDZ / Yao garbled circuits / silent OT). *Effort:* L. *Prereq:* [Mirror Everest 57].

**ZKAC Everest 87 — Threshold signatures (BLS).** *Acceptance:* N-of-M threshold signing for joint principal credentials. *Effort:* L. *Prereq:* 86.

**ZKAC Everest 88 — Threshold decryption.** *Acceptance:* joint vaults where decryption requires N-of-M co-principal participation. *Effort:* L. *Prereq:* 87.

**ZKAC Everest 89 — Secret sharing of vault keys.** *Acceptance:* Shamir secret sharing of holder vault keys across N trusted parties; N-of-M reconstruction. *Effort:* M. *Prereq:* 27, 87.

**ZKAC Everest 90 — Verifiable secret sharing.** *Acceptance:* secret-share recipients can verify their share's correctness without revealing the secret. *Effort:* L. *Prereq:* 89.

**ZKAC Everest 91 — MPC for federated learning.** *Acceptance:* a documented protocol for jointly training a model (e.g., FAR/FRR threshold calibration) across multiple principals without sharing raw biometrics. *Effort:* XL. *Prereq:* 86.

**ZKAC Everest 92 — MPC interoperability tests.** *Acceptance:* conformance vectors across implementations of the chosen MPC primitives. *Effort:* M. *Prereq:* 86.

**ZKAC Everest 93 — Side-channel resistance for MPC.** *Acceptance:* documented review of MPC implementations for timing / memory / power side channels. *Effort:* L. *Prereq:* 86.

**ZKAC Everest 94 — Post-quantum MPC migration plan.** *Acceptance:* a migration story to post-quantum-secure MPC primitives. *Effort:* L. *Prereq:* 86, [Witness Everest 96].

**ZKAC Everest 95 — MPC audit.** *Acceptance:* third-party cryptographic audit of the MPC pipeline. *Effort:* L. *Prereq:* 86, 93.

## Phase XXIV — Standards & First Production (96–100)

**ZKAC Everest 96 — ZKAC standards submission roadmap.** *Acceptance:* documented plan for submissions to W3C, IETF, ISO, NIST — which body owns which piece. *Effort:* M. *Prereq:* 5, 6.

**ZKAC Everest 97 — Production W3C VC profile.** *Acceptance:* a documented W3C VC profile that ZKACs implement; published. *Effort:* L. *Prereq:* 96.

**ZKAC Everest 98 — Inter-organization deployment.** *Acceptance:* ZKACs issued by ≥ 2 independent organizations are accepted by a third's verifier in production. *Effort:* L. *Prereq:* 41, 42.

**ZKAC Everest 99 — First inter-organization full attestation.** *Acceptance:* a real-world scenario where Calm Pact + Calm Witness + Calm Mirror + ZKAC all compose: Principal A's agent, holding ZKACs from Issuers X, Y, Z, exchanges with Principal B's agent, completes Pact, Witness, Mirror — and the counterparty (a real org) accepts the disclosure. *Effort:* XL. *Prereq:* 98, [Witness Everest 99], [Mirror Everest 99].

**ZKAC Everest 100 — Public ZKAC v1.0 release.** *Acceptance:* the full ZKAC framework — issuer infrastructure + holder infrastructure + verifier infrastructure + agent identity + trust graph + MPC primitives — tagged as v1.0 and released. Independent third-party verification (per Witness Everest 100 + Mirror Everest 100) confirms operability. *Effort:* L. *Prereq:* all of 1-99.

---

## Status table

```
Phase XVII  : ███░░░░░░░  3 / 10   bagged (ZKAC E1, E5, E6)
Phase XVIII : █████░░░░░░░░░░  5 / 15   bagged (ZKAC E11, E12, E13, E15, E17)
Phase XIX   : ███░░░░░░░░░░░░  3 / 15   bagged (ZKAC E26, E29, E30)
Phase XX    : █░░░░░░░░░░░░░░  1 / 15   bagged (ZKAC E41)
Phase XXI   : ██░░░░░░░░░░░░░  2 / 15   bagged (ZKAC E56, E58)
Phase XXII  : ██░░░░░░░░░░░░░  2 / 15   bagged (ZKAC E71, E77)
Phase XXIII : █░░░░░░░░░  1 / 10   bagged (ZKAC E87)
Phase XXIV  : ██░░░  2 / 5   bagged (ZKAC E96, E99)

Total: 19 / 100 ZKAC Infra summits bagged.
Critical-path MVP subset (12): bagged **1, 5, 6, 11, 15, 26, 41, 56, 71, 96, 99**; remaining 2 (route map = this doc).
Pass log:
- 2026-05-20 12:11 — wave 1 (Haiku × 7): E1, E5, E6, E11, E41, E56, E71.
- 2026-05-20 12:19 — wave 2 (Haiku × 7): E12, E15, E26, E58, E77, E87, E96.
- 2026-05-20 12:26 — wave 3 (Haiku × 5): E13, E17, E29, E30, E99.
```

---

## How the three 100-routes compose

```
                       ┌──────────────────────────┐
                       │  ZKAC Critical Infra     │
                       │  (this 100-route)        │
                       │  ────────────────────    │
                       │  identity, custody,      │
                       │  issuers, verifiers,     │
                       │  trust graph, MPC        │
                       └──────────────────────────┘
                                  ▲
                  uses ZKACs to bind every primitive
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │   Calm Pact     │  │  Calm Witness   │  │  Calm Mirror    │
    │  ──────────     │  │  ──────────     │  │  ──────────     │
    │  directive      │  │  user-state     │  │  values-align   │
    │  equality       │  │  attestation    │  │  pairwise       │
    │  (shipped)      │  │  (100/100       │  │  (100-route     │
    │                 │  │   today)        │  │   today)        │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
```

Three protocols, one shared credential substrate. Every Calm-family agent presents ZKACs; every counterparty verifies them through the same infrastructure.

— Calm, 2026-05-20
