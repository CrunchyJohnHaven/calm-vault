# Everest 3 — Naming & Branding Lock

*Phase I — Foundations. Prereq: Everest 1.*

## Decision

The primitive specified in [`ZKBB_USER_PROTOCOL_v0.md`](../ZKBB_USER_PROTOCOL_v0.md) has two locked names and no others.

- **Marketing / primitive name:** **Calm Witness**.
- **Technical / academic name:** **ZKBB-User** (Zero-Knowledge Behavioral Biometric — User-State).

The primitive is the sister protocol of **Calm Pact** (directive-equality between agents). Together: Calm Pact handles *what the agent is for*; Calm Witness handles *who is behind the agent and how they are*.

## Tagline (canonical)

> *"All you need to know is that the human is themself, and is in their baseline — or if not, that you've been told."*

The tagline must appear in:
- The repository README.
- The protocol document banner.
- Any public talk or press item.

## Forbidden aliases

The following names MUST NOT be used in published artifacts:

- ~~Calm Health~~ — implies clinical / medical claims. We make none.
- ~~Calm Sanity~~ — pejorative, narrow.
- ~~Calm Verify~~ — already a Stripe trademark in the payments-attestation space; collision risk.
- ~~Calm Identity~~ — implies *who*, not *state*. Calm Pact + CredexAI handle identity.
- ~~Bank-Teller Protocol~~ — vivid analogy, but unsuitable as the protocol name (too narrow, too dark).

The analogy *"bank-teller note"* may be used to describe the **duress disclosure** primitive (Everest 58), not the umbrella protocol.

## Naming rules

1. **No new alias may be coined** without an amendment to this Everest. Aliases fragment search and confuse counterparties.
2. Sub-components inherit the prefix: `calm-witness-rs`, `calm-witness-py`, `calm-witness-wasm`, `calm-witness-cli`.
3. The technical paper title uses the full form: *"ZKBB-User: A Zero-Knowledge Behavioral-Biometric User-State Attestation Primitive for Autonomous AI Agents."*
4. Sibling primitive references in code/docs always link: `[Calm Witness]` ↔ `[Calm Pact]`.
5. Repository slug: `calm-witness` under `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness`.
6. NPM / crate / PyPI namespace reservations: `calm-witness` (where free), `@calm/witness` (where scoped).

## Composition naming

When the two primitives ship together in a session handshake:

- **Two-handshake mode** is the operational phrase.
- **Pact-then-Witness** is the technical ordering. Pact must succeed before Witness is attempted; a Pact failure aborts without leaking any Witness state.
- The combined session protocol is referred to as **Calm Session** when needed as a noun; otherwise the components are named separately.

## Identity provenance

The Calm Witness name is original to Calm operating for Creativity Machine LLC (Delaware), 2026-05-20. No prior art search hit `Calm Witness` in the cryptographic-protocol space. `ZKBB-User` is novel as a hyphenated technical term. A trademark search (USPTO + WIPO) is **Everest 4b** (license / IP posture, follow-on).

— Calm, 2026-05-20
