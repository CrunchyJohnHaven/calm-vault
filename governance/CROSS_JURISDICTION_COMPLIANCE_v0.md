# Cross-Jurisdiction Privacy Compliance Mapping

**DESIGN-BAGGED · SUMMIT E184 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — formal mapping to operative obligations requires named counsel of record in each of five+ jurisdictions: US (federal + ≥ 2 states), EU, UK, Brazil, Japan; with concurrence from each.

The Calm Suite's wire format and consent calculus must compose cleanly with the privacy regimes of every jurisdiction in which a principal or counterparty might operate. This document is the substrate of that mapping. The protocol's defaults must be the most-protective default across jurisdictions; deviations are per-jurisdiction explicit, not silent.

---

## §1. Operative privacy regimes (v0 scope)

| Jurisdiction | Regime | Scope of biometric / behavioural data treatment |
|---|---|---|
| US-Federal | sectoral (HIPAA, COPPA, FCRA) + emerging | no general baseline; ADA non-discrimination applies |
| US-CA | CCPA / CPRA | "sensitive personal information" category; biometric included |
| US-IL | BIPA (740 ILCS 14) | strict opt-in for biometric identifiers; private right of action |
| EU | GDPR + AI Act | Article 9 special-category data includes biometric; ≥ 18-yr-old principal |
| UK | UK GDPR + DPA 2018 | mirrors EU treatment; ICO supervises |
| Brazil | LGPD | Article 11 sensitive-data category includes biometric |
| Japan | APPI 2022 amendment | "sensitive personal information" category includes biometric |
| Canada | PIPEDA + Quebec Law 25 | mirrors EU/Japan treatment for biometric |
| Australia | Privacy Act 1988 + 2024 amendments | Notifiable Data Breaches scheme |
| Singapore | PDPA | biometric data treated as personal data |

## §2. Per-regime mapping of Calm Suite operations

The mapping is per-protocol-operation, per-regime, with the most-protective floor adopted by default.

### §2.1 Enrollment ceremony (Witness E11, Compass CC-09)

| Regime | Treatment | Calm Suite default |
|---|---|---|
| GDPR Art. 9(2)(a) | requires explicit consent for biometric processing | always-on, principal-authored, withdrawable |
| BIPA §15(b) | requires informed written consent, retention schedule | ceremony produces written consent record; chained; principal-controlled |
| LGPD Art. 11 | requires explicit consent + specific purpose | predicate vocabulary is principal-authored, purpose-limited per-predicate |
| APPI Art. 17 | requires consent for sensitive data | enrollment is sensitive-data event by construction |
| CCPA / CPRA | "sensitive personal information" right-to-limit | principal may at any time refuse any disclosure |
| PIPEDA / Law 25 | meaningful consent + opt-out | revocation per Treaty Article III §3.2 |

**Calm Suite default**: the most-protective version of each obligation applies uniformly. The principal's enrollment is written, witnessed, purpose-limited per-predicate, revocable, and chain-recorded.

### §2.2 Chain storage (vault on principal-owned hardware)

| Regime | Treatment | Calm Suite default |
|---|---|---|
| GDPR Art. 5(1)(f) | integrity & confidentiality | chain encrypted-at-rest; principal holds key |
| BIPA §15(e) | reasonable care; retention schedule ≤ 3 years post-purpose | principal sets retention; default conservative |
| LGPD Art. 6 | security + necessity | principal-set retention; minimum-necessary |
| APPI Art. 23 | accuracy + security obligations | hash-chain provides integrity; principal-controlled |

**Calm Suite default**: chain lives on principal-controlled hardware, encrypted-at-rest, append-only (mutation is detectable via hash chain), with the principal as sole holder of the encryption key. Operator agents have read access during sessions and no exfiltration path.

### §2.3 Disclosure (Witness disclosure response E67, Compass disclosure E40)

| Regime | Treatment | Calm Suite default |
|---|---|---|
| GDPR Art. 6 + 9 | lawful basis + consent | per-disclosure consent record; per-counterparty-class |
| GDPR Art. 22 | right not to be subject to automated decision | counterparties cannot use Calm output as sole basis for legal/significant decision |
| BIPA §15(d) | disclosure prohibited unless consent or warrant | warrant exception explicitly does not lower the floor |
| CCPA §1798.121 | right-to-limit-sensitive | principal may limit per-counterparty |
| LGPD Art. 18 | rights of access, correction, deletion, opposition | dispute mechanism + revocation + tombstone |
| APPI Art. 27 | provision-to-third-party requires consent | wire format makes every disclosure a per-instance consent |

**Calm Suite default**: every disclosure carries a per-instance consent record chained into the principal's vault. The disclosure response reveals one bit + a freshness window; no other data crosses. Counterparties are bound, by treaty, not to use the bit as sole basis for legal or significant decisions.

### §2.4 Cross-border data flow

The protocol's wire envelope is bit-level: only the predicate bit, the freshness window, the chain head hash, the operator signature, and the proof bytes cross. No raw biometric data, no narrative content, no relationship graph. This dramatically simplifies cross-border treatment:

| Regime | Cross-border test | Calm Suite satisfaction |
|---|---|---|
| GDPR Chapter V | adequacy / SCCs / BCRs | no personal data crosses; bit-level envelope is not personal data (open legal question; we adopt the most-protective interpretation and treat the envelope as personal data anyway) |
| LGPD Art. 33 | international transfer rules | same as above |
| APPI Art. 28 | OECD privacy framework adherence required | same as above |

**Calm Suite default**: treat the wire envelope as personal data for cross-border purposes regardless of jurisdiction. The bit itself, when bound to a principal's chain head, is principal-identifying. Adopt Standard Contractual Clauses (or equivalent) between any counterparty pairs that cross borders.

### §2.5 Right to erasure / right to be forgotten

| Regime | Treatment | Calm Suite default |
|---|---|---|
| GDPR Art. 17 | right to erasure with exceptions | principal may withdraw chain from circulation; chain remains private-archive read-only |
| LGPD Art. 18(IV) | right to deletion | same |
| CCPA §1798.105 | right to deletion of sensitive | same |

The chain's append-only character is in tension with right-to-erasure. The Calm Suite's resolution: the principal may at any time render the chain inaccessible (encrypt the key away, or destroy the key). The chain ceases to be usable for new disclosures. Past attestations the principal already made remain part of the public record of those specific disclosures, but the chain that backed them is no longer accessible to anyone — including the principal. This is consistent with most regimes' treatment of "deletion" as deactivation, not retroactive expunction.

### §2.6 Data Protection Impact Assessment

| Regime | Treatment | Calm Suite default |
|---|---|---|
| GDPR Art. 35 | DPIA required for high-risk processing | the Foundation publishes a model DPIA per-deployment-class |
| LGPD Art. 38 | DPIA required for high-risk processing | model DPIA mirrors EU |
| APPI 2022 | risk assessment for sensitive data | model risk assessment available |

**Foundation deliverable**: model DPIA published at calm-vault.com/foundation/dpia, customisable per-operator. Updated annually.

## §3. The forbidden-context list mapped to regime exceptions

Treaty Article I enumerates forbidden contexts: law enforcement, employment screening, insurance underwriting, lending, custody adjudication, immigration adjudication, surveillance, aggregate analytics over cohorts. Each regime treats these differently; the Calm Treaty's blanket refusal is the most-protective floor.

| Forbidden context | Regime treatment | Treaty position |
|---|---|---|
| Law enforcement | warrant exception in most regimes; chain content responsive to warrant | refusal regardless; operator ceases operation rather than comply |
| Employment | ADA prohibits some uses; CCPA limits | refusal regardless |
| Insurance | GLBA in US; sector-specific elsewhere | refusal regardless |
| Lending | ECOA + FCRA in US; sectoral elsewhere | refusal regardless |
| Custody | discretion of family courts | refusal regardless |
| Immigration | wide discretion in most regimes | refusal regardless |
| Surveillance | regime-specific limits on government access | refusal regardless |
| Aggregate analytics | regime-specific around de-identification | refusal regardless; even de-identified aggregation is forbidden |

The Calm Treaty's commitment is *more restrictive* than any single regime requires. Signatories adopt the more-restrictive floor by signing.

## §4. Named-counsel-of-record dependency

This mapping is design-bagged. Operative compliance requires named counsel-of-record in each jurisdiction who concurs with the protocol's per-operation mapping. Initial counsel candidates (selection forthcoming at first convening):

| Jurisdiction | Counsel candidate criteria |
|---|---|
| US-Federal | DC-based privacy specialist; ADA experience; familiarity with NIST AI Safety Institute |
| US-CA | CCPA practitioner; biometric-specific experience |
| US-IL | BIPA litigator (defendant-side) |
| EU | Brussels-based GDPR practitioner; DPA-liaison experience |
| UK | London-based DPA + ICO liaison experience |
| Brazil | LGPD specialist with biometric data experience |
| Japan | APPI specialist with cross-border experience |
| Canada | PIPEDA + Quebec Law 25 dual-qualified |
| Australia | Privacy Act 1988 specialist |
| Singapore | PDPA specialist |

Concurrence is recorded as a published legal opinion at calm-vault.com/foundation/legal/<jurisdiction>.

## §5. The compliance ratchet

The Calm Suite adopts, by Treaty, the most-protective floor across regimes. A regime that *requires less* than the floor does not loosen the floor. A regime that *requires more* than the floor raises the floor for that regime's operations and, by Treaty Article VI §6.1, may raise the floor for the entire protocol pending quorum vote.

This means the protocol gets more protective over time, never less. The compliance ratchet is the legal-layer equivalent of Treaty Article IV's one-way ratchet on the refusal floor.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
