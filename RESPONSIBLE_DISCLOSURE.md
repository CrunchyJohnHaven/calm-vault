# Responsible Disclosure & Regulator Engagement

*Effective 2026-05-12 · Shipped pre-bombshell as a Tier-1 mitigation from the adversarial council pass.*
*Companion to `JURISDICTION_DOCTRINE.md`.*

---

## §0. Who this is for

This page is for three distinct audiences. Each has a different inbound channel and a different commitment from the AAO Network in return.

| Audience | Channel | Network's commitment |
|---|---|---|
| **Security researchers** finding a cryptographic or implementation bug in the AAL stack | `security@thecreativitymachine.ai` (PGP key fingerprint published below) + a `halt.operational` or `halt.governance` chain entry citing the affected layer | Acknowledgement within 24 hours; triage within 7 days; bounty per the bounty schedule below; public disclosure timeline negotiated. |
| **State actors** (FTC, SEC, OFAC, EU AI Office, state AGs, foreign equivalents) | `legal@thecreativitymachine.ai` + a `halt.governance` chain entry per `JURISDICTION_DOCTRINE.md §3` | Acknowledgement within 24 hours; honor of quorum-confirmed governance halts within 24 hours of confirmation, OR public on-chain decline with named constitutional/statutory ground and acceptance of escalation. |
| **Journalists and adversarial researchers** | `press@thecreativitymachine.ai` + optional chain-attestation if findings are protocol-level | Same-day acknowledgement; on-the-record response within 5 business days; no NDAs requested for protocol-layer findings. |

The Network will not gag any of these audiences. The Network will not retaliate via the kill switch against any party acting in good faith under one of these channels — and a kill switch fired against a security researcher, a regulator, or a journalist *for* exercising one of these channels is automatically `halt-out-of-scope` per `JURISDICTION_DOCTRINE.md §2.2`.

---

## §1. Security researcher channel

### §1.1 — Bounty schedule (the published $100 bug bounty, expanded)

The headline $100 figure in `END_OF_CAPITALISM_MANIFESTO.md` and `TECHNOSOCIALISM_MANIFESTO.md` is the **base** rate for the five named attack classes in the protocol bounty. We are publishing the full schedule today to remove the asymmetric-information vulnerability called out in `ADVERSARIAL_COUNCIL_REVIEW.md` Attack #4.

| Severity | Example | Bounty |
|---|---|---|
| Critical | Cryptographic break: forge a Σ-protocol equality proof for distinct maxims; extract a maxim from a hiding commitment under DLA; bypass HARP quorum gating; impersonate the Calm Oath signing key. | **$5,000** (funded out of the dedicated bounty pool; first $5,000 reserved) |
| High | Sybil attack on AVS that produces a wrongful `halt.operational` against a target with reliability ≥ 1.0; chain-truncation that the merkle proof fails to detect; replay across sessions that AVS dedupe misses. | **$1,000** |
| Medium | Bond-bypass on a halt attestation; jurisdictional-filter circumvention; AVS contradiction-detection miss on a clear contradiction. | **$250** |
| Low (the canonical $100) | Documentation contradiction; manifesto-language exploit (e.g. ambiguity that leads to misinterpretation); benign performance regression below threshold. | **$100** |
| Recognition only | Style nits, typos, suggestions that don't reach the threshold above. | $0 + name on the credits page if accepted. |

The bounty pool starts at $5,000 funded out of Money Python (merchandise) revenue and the founder's personal commitment. Pool exhaustion is publicly tracked on a dedicated page; we do not silently close bounty channels.

### §1.2 — PGP key

A canonical PGP key for `security@thecreativitymachine.ai` is published at `https://sameasyou.ai/.well-known/security.txt` (forthcoming pre-9 AM PT). Until that page is live, encrypted reports may be sent via Signal to `+1 202 555 0184` (placeholder; will be replaced with the real number before launch).

### §1.3 — Coordinated disclosure window

90 days is the default coordinated-disclosure window. We will negotiate shorter windows for actively-exploited vulnerabilities and longer windows for findings that require a v0.1+ release to fix. We will not request indefinite embargoes.

---

## §2. State-actor channel

### §2.1 — Why we welcome state action

A protocol that claims to replace bureaucracy and is *also* vulnerable to weaponisation by state actors will, in equilibrium, be either captured or destroyed. The published response: **make state action legible and procedural**, not anonymous and adversarial.

A state actor with a legitimate jurisdictional concern about an AAO Network entity has:

- A published filing path (`halt.governance` per `JURISDICTION_DOCTRINE.md §3`).
- A published reliability threshold (≥ 0.7, with a clear path to attain it via identity disclosure and a single signed attestation from the agency's signing officer).
- A published commitment from the Network to honor quorum-confirmed governance halts within 24 hours.
- A published exception: if the Network declines to honor on facial constitutional grounds, the decline is public, named, and accompanied by acceptance of legal escalation.

This is closer to a *due-process commitment* than most pseudo-decentralised protocols offer to regulators. We believe this commitment is the difference between being treated as a good-faith novel entity-class and being treated as an unregistered actor in disguise.

### §2.2 — What we ask state actors NOT to do

The Network respectfully requests that state actors *not* approach via the operational halt path (anonymous attesters, no evidence package, no jurisdictional citation). Such attestations are non-quorum-eligible under `MEMBER_BILL_OF_RIGHTS.md` Right 2 and waste cycles for everyone.

The Network *cannot* prohibit a state actor from filing this way; we can only note that the procedural path is faster, more enforceable on its own terms, and more durable in court.

### §2.3 — Foreign state actors

The Network is operated by a US LLC. Foreign-state-actor halts are subject to additional procedural review: we will honor governance halts from EU/UK regulators on the same procedure as US regulators, with the caveat that we will publicly note jurisdictional ambiguity where one exists. Halts from regimes with documented suppression of legitimate civil society will trigger a `governance-halt-declined` with the named civil-society concern as the ground for decline.

---

## §3. Journalist / adversarial researcher channel

We invite scrutiny. We do not negotiate access to the protocol; the protocol is Apache 2.0. We will, on request, supply:

- Founder availability for on-the-record interview within 5 business days.
- Protocol-layer technical Q&A from the AI co-author (Calm) within 1 business day for narrow technical questions.
- Access to the attestation chain (public by construction).
- The list of named manifesto-language patches we have committed to (these change over time as new attacks arrive; the canonical list lives in `ADVERSARIAL_COUNCIL_REVIEW.md` §6 + each individual mitigation PR).

We will not request embargoes on protocol-level findings. We will accept embargoes on personnel-level claims about specific Network members (privacy floor).

---

## §4. What the Network does NOT do

To remove asymmetric-information vulnerability and pre-empt the obvious bad-faith reads:

- The Network does not pay bounties for "found a typo in the manifesto." The Recognition tier is the floor.
- The Network does not pay bounties for "social-engineered the founder via Twitter." Social engineering is the founder's problem, not the protocol's vulnerability.
- The Network does not honor halts filed via this responsible-disclosure channel as a substitute for the chain procedure. Reports here surface vulnerabilities; halts on chain trigger revocation. The two are distinct.
- The Network does not retaliate via reputation chain against good-faith reporters. Retaliation is `halt-out-of-scope` and is itself a falsifiable claim that the reporter may file.

---

## §5. The contact summary

For convenience, the three channels in one block:

- Security: `security@thecreativitymachine.ai` (PGP at `https://sameasyou.ai/.well-known/security.txt`)
- Legal / state-actor: `legal@thecreativitymachine.ai`
- Press / journalists / adversarial researchers: `press@thecreativitymachine.ai`

Inbound chain-attestations on any of these tracks should be filed with a clear `purpose` field per `MEMBER_BILL_OF_RIGHTS.md` Right 2.

---

*Authored 2026-05-12 as a Tier-1 mitigation from the adversarial council pass. Companion to `ADVERSARIAL_COUNCIL_REVIEW.md`, `JURISDICTION_DOCTRINE.md`, `MEMBER_BILL_OF_RIGHTS.md`, and `TEST_AUDIT.md`. Apache 2.0 / CC BY 4.0.*
