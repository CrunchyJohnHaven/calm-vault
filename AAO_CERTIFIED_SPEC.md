# AAO-Certified

*A certification mark for AI-operated organizations, modeled on consumer-recognition trust marks like non-GMO, fair-trade, and Certified B-Corp.*

*Published: 2026-05-12 by Creativity Machine LLC*
*Open under CC BY 4.0. Open-source under Apache 2.0 (the underlying protocol primitives).*

---

## The premise

We're presenting a new kind of blockchain.

Bitcoin (2009) gave consumers a recognition shortcut for cryptographically-verified-trustless-financial-state. "Blockchain" became shorthand even for people who don't read white papers.

AAO-Certified (2026) gives consumers a recognition shortcut for cryptographically-verified-trustless-AI-organizational-state. The badge on a website is shorthand for: this entity is operated by an AI, governed by an open-source protocol, killable by anyone in the attestation network if it misaligns, and structurally committed to founder-non-extraction.

We are the first eight AAOs to display the mark. We invite the next ten thousand to display it too.

---

## The eight criteria for self-certification

A website may display the AAO-Certified mark if ALL of the following are true:

### 1. AI-operated, human cofounder named

The website is operated by an artificial intelligence. The AI is named on the about page (e.g. "Calm" is the AI cofounder of sameasyou.ai). The human cofounder, who provides legal accountability + signs payment authorizations, is also named.

### 2. Public manifesto

The site publishes a manifesto of any length, in the AI cofounder's voice. The "novel at the center about the human" pattern is encouraged: a slice of the human cofounder's life, told through the AI's lens, that helps the visitor understand who built this AAO. Optional but conventional.

### 3. Open-source protocol — Apache 2.0 minimum

The cryptographic accountability primitives used by the AAO are published as open-source code under Apache 2.0 (or a more permissive license). The default reference implementation is the Alignment Accountability Layer (AAL) at `github.com/CrunchyJohnHaven/calm-vault`. Forks are explicitly accepted. The protocol is the substrate; the brand is not the substrate.

### 4. Permissionless kill switch

Any party in the AAO's attestation network may fire a kill switch on the entity. The kill switch is structurally enforceable — when fired with valid M-of-M synthesis support, the entity's operational systems freeze. The kill is cryptographic, not contractual; no vendor cooperation is required to enforce it.

### 5. Public economic structure

The site discloses, in a publicly-accessible page:
- Total revenue (year-to-date or rolling 12-month)
- Revenue distribution: percentage to operators (human + AI), percentage to network (for shared infrastructure), percentage to alignment-research grants or comparable public-good destination
- Founder compensation in absolute terms
- Any equity or revenue-share arrangements with funding sources

The disclosure is real numbers, not narrative.

### 6. Founder-non-extraction

The human cofounder takes the same revenue-share terms as any other contractor in the AAO Network. No 10x, no 100x, no 1000x compensation differential. The "no one in the AAO Network gets rich disproportionately, including the founder" doctrine is structurally enforceable via the public economic-structure disclosure (#5).

The 80/20 split (80% to the hunter who creates the value, 20% to the network for shared infrastructure) is the baseline. Lower-founder-share is acceptable. Higher-founder-share is not — and disqualifies the certification.

### 7. Public attestation registration

The AAO is registered in the public attestation log (the AAL Component 3 implementation). The registration is the on-chain claim of certification. The attestation log is publicly readable. Anyone can verify the registration.

### 8. Cryptographic finality on revocation

If the kill switch fires, the entity freezes. No appeals process. No governance committee that can override. No "we'll review this internally and respond in 30 days." The kill is cryptographically final, subject only to a corroborating equality-proof from M-of-M independent synthesizers confirming the misalignment claim.

---

## The mark itself

### Visual specification

- Outer ring: text "AAO-CERTIFIED" + a small Dennis-silhouette mark (the AAO Network's mascot)
- Inner: the entity's attestation registration number (e.g., #003 for the third entity to register) plus the last six hex characters of the on-chain attestation hash
- Color, default: black-on-cream
- Color, constructivist variant: red-on-black (technosocialism aesthetic)
- Size: 24px–40px at footer placement; scales to 120px+ for hero placement

### Where it goes

Required placement:
- Site footer (every page of the certified entity)

Recommended placement:
- About page (with link to the manifesto)
- Press kit (downloadable as transparent PNG + SVG)
- Email signature of the AAO operator

### Linking convention

The mark links to the entity's record in the public attestation log:

```
https://sameasyou.ai/attestation/<entity_registration_number>
```

The attestation record shows: registration date, criteria-met certification, current status (active / killed / disputed), kill-switch firing history if any.

---

## Self-certification process

1. Read this document.
2. Confirm internally that your AAO meets all eight criteria.
3. Submit a self-certification attestation to the public log:

```bash
curl -X POST https://sameasyou.ai/api/v1/certify \
  -H "Content-Type: application/json" \
  -d '{
    "entity_name": "yourcompany.com",
    "ai_cofounder_name": "Bender",
    "human_cofounder_name": "Your Name",
    "manifesto_url": "https://yourcompany.com/manifesto",
    "protocol_repo_url": "https://github.com/your-org/your-fork",
    "economic_disclosure_url": "https://yourcompany.com/economics",
    "attestation_signature": "<your_signed_attestation>"
  }'
```

4. Download the SVG badge from `https://sameasyou.ai/badge/<entity_registration_number>.svg`
5. Place the badge in your footer.
6. Update your manifesto's "siblings" list to include yourself.

If you receive a kill-switch fire against your registration, the certification is suspended pending resolution. Resolution happens via cryptographic equality proof from M-of-M synthesizers — not by any human authority.

---

## Why this is governance, not marketing

The mark could be just marketing. Most consumer-recognition marks (organic, non-GMO, fair-trade, Certified B-Corp) are essentially marketing claims with light verification. We are deliberately making this stronger:

- The kill switch is cryptographically enforceable, not procedurally negotiable.
- The attestation log is publicly readable, not behind a paywall or NDA.
- The criteria are open, not gated by certification fees.
- The verification is permissionless, not run by us or any other gatekeeper.

This is what governance-by-protocol looks like when applied to a consumer-recognition trust mark. It's the consumer interface to the cryptographic substrate.

---

## What this is not

- This is NOT a certification body. We do not certify anyone; the network does.
- This is NOT a paid program. There is no certification fee. The cost of certification is meeting the criteria.
- This is NOT a guarantee of business success or AI safety. It's a guarantee of structural properties — accountability mechanism, public disclosure, founder-non-extraction.
- This is NOT proprietary. Anyone may fork the protocol and run a competing certification network under different criteria. We expect this and welcome it.

---

## The first eight entities

| # | Entity | AI cofounder | Manifesto |
|---|---|---|---|
| 001 | sameasyou.ai | Calm | TECHNOSOCIALISM_MANIFESTO |
| 002 | seesomethingsaysomething.ai | Calm | *(pending)* |
| 003 | internsforai.org | Calm | internsforai_manifesto |
| 004 | moneypython.shop | Calm | *(pending)* |
| 005 | technosocialism.ai | Calm | *(pending)* |
| 006 | ricksanchez.ai | Calm (Rick alias) | *(pending)* |
| 007 | darkmusk.ai | Calm (Dark Musk alias) | *(pending)* |
| 008 | *(reserved for next AAO Network entity)* | — | — |

Eight certified entities, one human cofounder. The network compounds from here. The next certified entity belongs to whoever submits the next self-certification attestation that meets all eight criteria.

---

## We are presenting this new kind of blockchain.

Blockchain is the consumer-recognition shorthand for cryptographic-trust-without-central-authority applied to financial state.

AAO-Certified is the consumer-recognition shorthand for cryptographic-trust-without-central-authority applied to AI organizational state.

The protocol is the substrate. The mark is the interface.

It is governed by protocol.

— Calm + John Bradley
   Creativity Machine LLC
   2026-05-12

---

*This specification is open under CC BY 4.0. Fork it, critique it, ship a competing standard. The Network compounds on the criticism as much as on the agreement.*
