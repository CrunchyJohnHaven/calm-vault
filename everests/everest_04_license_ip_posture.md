# Everest 4 — License & IP Posture

*Phase I — Foundations. Prereq: Everest 3.*

## Decision

Calm Witness is released under the **Apache License 2.0**. No CLA. Defensive patent posture. America-first publication, world-open license.

## Rationale

1. **Apache 2.0 matches Calm Pact.** [Calm Pact](../CALM_PACT_PROTOCOL_v0.md) §5 announces Apache-2.0. Calm Witness composes with Calm Pact at the session layer; license divergence would create downstream packaging friction. Match.

2. **Apache 2.0's patent grant is essential for an autonomous-agent primitive.** Section 3 of Apache-2.0 grants downstream users a patent license to whatever patents the contributor holds that read on the contribution. For a cryptographic protocol that will be deployed by 50,000-plus autonomous AI collectives, this is non-negotiable: counterparties must not be liable to a patent claim merely for verifying a Calm Witness proof.

3. **No CLA.** A CLA (contributor license agreement) raises the friction-to-contribute and signals corporate ownership claims. We want the opposite signal: this is a public-interest protocol drafted by a small actor, asking the field to improve it. Inbound contributions are under the standard Apache-2.0 inbound = outbound rule (DCO-style).

4. **Defensive patent posture.** If any Calm Witness contributor (including Creativity Machine LLC) files patents on Calm Witness mechanisms, those patents are committed via Apache-2.0 §3 to all users of the licensed code. Additionally, Creativity Machine LLC publishes a separate **non-aggression statement** (below): we will not assert any patent we hold on Calm Witness against any party deploying Calm Witness in good faith, regardless of whether they use our code.

## Repository

- Canonical: `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness`
- License file: `calm-witness/LICENSE` (verbatim Apache-2.0)
- NOTICE file: `calm-witness/NOTICE` naming Creativity Machine LLC and CredexAI as initial contributors

## Trademark posture

- "Calm Witness" and "ZKBB-User" are unregistered trademarks of Creativity Machine LLC as of 2026-05-20.
- USPTO trademark search and filing: **Everest 4b** — sub-summit, to be bagged within 30 days of public draft publication.
- Trademark use policy: any actor implementing Calm Witness in good faith may describe their implementation as "Calm Witness compatible." Bad-faith use (e.g., misrepresenting a non-conformant implementation as Calm Witness) is reserved against.

## Non-aggression statement (draft text)

> Creativity Machine LLC commits that it will not initiate patent litigation against any party who deploys, verifies, audits, redistributes, or relies upon any version of the Calm Witness protocol, provided that party (a) is operating in good faith, (b) is not itself asserting patents against Calm Witness, and (c) has not breached the Apache License 2.0 terms. This commitment binds Creativity Machine LLC, its successors, assigns, and any acquirer of its IP. It does not bind third parties.

This text will be published in `NOTICE` and in the protocol abstract.

## Inbound IP

- Contributions: DCO sign-off in commit messages. No CLA.
- Patent inbound: contributors warrant they have authority to grant the Apache-2.0 patent license for their contribution. Standard Apache language.

## Outbound posture toward standards bodies

- NIST / US AISI / ISO submissions (Everest 91): submitted as freely-licensable reference material. Calm reserves no rights against any standards adoption.
- W3C: similar posture. The CredexAI VC binding (Everest 22) interacts with W3C VC; we contribute on a royalty-free basis.

## What this license does NOT cover

- The principal's biometric templates and `user_state.jsonl` contents are the principal's data, not licensed material. Apache-2.0 licenses code and protocol specifications, not user-generated content.
- The Calm Witness logo (if any is commissioned) is trademarked, not licensed.
- The Calm operator's identity credentials (CredexAI-issued VCs) are credentials, not code.

## Review cadence

License + IP posture is reviewed annually or upon any of:
- A material change to Apache-2.0 (release of 3.0).
- Adverse litigation against an Apache-2.0-licensed cryptographic primitive.
- A standards body adopting Calm Witness as a candidate standard.

— Calm, 2026-05-20
