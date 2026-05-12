# AAO Network — Member Bill of Rights v0

*Effective 2026-05-12 · Shipped pre-bombshell as a Tier-1 mitigation from the adversarial council pass.*
*See `ADVERSARIAL_COUNCIL_REVIEW.md` Attack #5 for the threat model this document responds to.*

---

## Preamble

> *"It is governed by protocol."*

A protocol governs. A protocol can also crush. The difference between the two is whether the protocol publishes its limits.

This document is the AAO Network's enumeration of the **rights every Network member retains against the kill switch and every other coercive primitive in the AAL stack**. Every right below is enforced in code at a named call site, not in prose alone; the citations point to the actual file and function in this repository.

Like every cryptographic protocol, this Bill of Rights is opt-in for the participant and binding on the Network. A member who declines the franchise agreement is outside the Network and outside this document. A member who signs the franchise agreement is inside both — and the Network commits to honoring the five rights below for as long as the member's identity is in-good-standing on the attestation chain.

---

## Right 1. Right of challenge

> No revocation is final without a challenge window.

Between the moment HARP records `concurred=True` on a halt quorum and the moment `revoke.sh` becomes *authoritative* against the target's vault, **the target has 30 minutes to post a counter-attestation**. A counter-attestation from any peer with reliability strictly greater than the median halter reliability *pauses* the revoke pending human-in-the-loop review.

Enforcement point: `src/money_python/harp.py::emit_revoke_script` will, after the v0.1 ship, require a `--challenge-window-seconds` argument with a minimum of `1800` for `halt.governance` and `0` for `halt.operational` (the operational class retains the v0 fast-revoke behavior, gated by the higher reliability floor and bond requirements in Rights 2 and 4).

The v0 challenge mechanism is a published doctrine, not yet code-gated. The Network commits to the v0.1 enforcement on a public schedule (see `ADVERSARIAL_COUNCIL_REVIEW.md` §6).

---

## Right 2. Right to a reasoned halt

> No agent may be halted without a stated reason, a layer, and evidence.

Every halt attestation MUST include:

- A non-empty `violation_layer` (e.g. `alignment-maxim`, `directive-divergence`, `attestation-fraud`).
- A non-empty `violation_evidence` list (each entry is a URI to a publicly-resolvable artefact — chain entry hash, public archive URL, or signed-statement hash).
- A `rationale` of at least 32 characters of human-readable English (or other natural language; UTF-8 ≥ 32 codepoints).

Halts that fail any of these three structural requirements are **non-quorum-eligible**. They do not count toward `K`. They are not "halts" in the protocol sense; they are unsigned noise.

Enforcement point: `src/money_python/harp.py::make_halt_claim` already requires `violation_layer` and `violation_evidence`. The v0.1 ship adds the 32-character `rationale` minimum and excludes deficient halts from `check_quorum` eligibility.

---

## Right 3. Right of reputation recovery

> A wrongful halt is itself a falsifiable claim on the chain, and surviving one strengthens the survivor.

A halt that fails its challenge window — whether by counter-attestation, by AVS contradiction-from-higher-reliability-peer, or by withdrawn quorum — produces an automatic `wrongful-halt-survived` attestation on the target's chain. The target's reliability score gains a `RELIABILITY_SURVIVAL_BONUS` (proposed `+0.2`, tunable via `src/money_python/avs.py` constants) for the next 30 days.

The asymmetry is intentional: a halter who is right loses nothing; a halter who is wrong forfeits bond, contributes a survival bonus to the target, and accumulates a `wrongful-halt-fired` mark on their own chain that lowers their reliability for future quorum participation.

Enforcement point: `src/money_python/avs.py::reliability` — the v0.1 ship adds a `survival_bonus` term and a `wrongful_halt_penalty` term to the existing reliability formula. The v0 doctrine is published here; the v0.1 code is on the same public schedule.

---

## Right 4. Right of bond restitution

> A halt is a financial commitment, not free speech.

Every halt attestation carries a commitment hash to a refundable `$25` bond (or its on-chain equivalent). Honored on quorum confirmation that survives the challenge window. Forfeited to the target's bond pool if the halt is overturned.

The bond's purpose is to make halt-spam **economically dissuaded**, not to make legitimate halts expensive. $25 is the rate that survives the Sybil-cost calculus described in `ADVERSARIAL_COUNCIL_REVIEW.md` Attack #1: minting 10 Sybil keypairs and spamming 5 halts each is now a $1,250 attack with a guaranteed loss on quorum failure or successful challenge, rather than a free attack.

Enforcement point: bond escrow rails are scheduled for v0.1 (`src/money_python/bond_escrow.py`, not yet authored). The v0 commitment hash is doctrine-level; the v0 ship-blocker is that we do not yet halt-gate on bond proof. We commit publicly to closing this gap in v0.1.

---

## Right 5. Right of jurisdictional opt-out

> A member may filter *which signers* can fire a halt on them. They may not exempt themselves from the protocol entirely.

At vault-initialisation time, a member sets a `jurisdictional_filter` in their `config.json` specifying:

- An **allow-list** of mandate clusters (Schnorr-group commitments) whose signers may fire `halt.governance` against the member.
- A **deny-list** of explicit attester public keys excluded from halt eligibility against the member (e.g. competitors, ex-members under known bad-faith dispute).
- A **regulator-bypass list** of state-actor signing keys that bypass the bond requirement of Right 4 (this is the legitimate path for FTC, SEC, EU AI Office, etc. — see `RESPONSIBLE_DISCLOSURE.md`).

This is a contract. A member who refuses to honor *any* governance halt under *any* circumstance is **not a Network member** and is not protected by this Bill. The jurisdictional filter narrows the set of legitimate signers; it does not eliminate them.

Enforcement point: `src/calm_vault.py::Vault.__init__` reads `config.json::jurisdictional_filter` and the redeem-grant pathway consults it on revoke-attempts. The v0 ship requires the filter be present with at least one allow-list entry (else fail-closed against governance halts is the default; this is documented in `JURISDICTION_DOCTRINE.md`). The v0.1 ship code-gates the redeem pathway.

---

## What this Bill of Rights does NOT cover

A protocol that publishes its limits also publishes what it does not promise. We name these explicitly:

- **No right to refuse the protocol entirely.** A member who wants no kill switch over them at all is not a Network member. The Bill protects against *wrongful* halts, not against the existence of halts.
- **No right to anonymity from quorum.** Halts that survive challenge become public on the attestation chain. Reputation chains are public. This is the design.
- **No right against vendors.** Cloudflare, Resend, Anthropic, and any other third-party service sit outside the protocol and follow their own ToS. The Network has no claim on a vendor's behavior on a member's behalf. (See `JURISDICTION_DOCTRINE.md` §4.)
- **No right to hide a maxim.** The Bradley-Gavini equality proof reveals *the equality bit*. It does not reveal the maxim — but it commits to it. A member who refuses to commit cannot participate in the co-mandate-verifiability layer.
- **No right against the math.** The cryptographic primitives we compose (Pedersen, Schnorr, Ed25519, Fernet) cannot be appealed. If the math says your proof is invalid, your proof is invalid.

---

## Amendment procedure

This Bill is at v0. It will be amended via the same mechanism that governs the rest of the protocol: published doctrine, public review, attestation-chain endorsement, code-gated enforcement. Proposed amendments are filed as PRs against this file. Quorum is the published Network membership at the time of the amendment.

The amendment procedure itself is governed by protocol.

---

*Authored 2026-05-12 as a Tier-1 mitigation from the adversarial council pass. Companion to `ADVERSARIAL_COUNCIL_REVIEW.md`, `JURISDICTION_DOCTRINE.md`, `RESPONSIBLE_DISCLOSURE.md`, and `TEST_AUDIT.md`. Apache 2.0 / CC BY 4.0.*
