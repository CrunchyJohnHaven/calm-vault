# Everest 215 — Treaty-Grade Multi-Stakeholder Governance for the Calm Suite

**Design-bagged: this is the v0 governance treaty draft. Institutional follow-through required for v1 ratification.**

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. DESIGN-BAGGED pending the first multi-stakeholder convening per Everest 216.**

---

## 0. Why a treaty, not just a protocol

The Calm suite (Pact, Witness, Compass, Concord, ZKAC, Mirror, Operations, Tenancy) defines what *is* cryptographically possible between autonomous AI agents and their human principals. A treaty defines what *should be* — the floor below which no operator, no counterparty, and no jurisdiction may operate without forfeiting the suite's name.

A protocol with no governance becomes infrastructure for whichever actor captures it. The Calm suite is engineered to be unweaponizable — refusal-floor, anti-purity-test, principal-authorship, scope-statement forfeits — but engineered constraints decay under sufficient institutional pressure. A treaty raises the cost of pressure by tying it to multi-stakeholder consent.

This document is the **founding draft**. It is not law. It will not be law. It is the artifact a 12-party convening (Everest 216) negotiates from.

---

## 1. The four signatory classes

The treaty contemplates four classes of signatory, each binding for distinct obligations:

### Class A — Operator signatories
AI agent operators issuing Calm-suite proofs on behalf of human principals.

**Bound obligations:**
- Implement the refusal-floor (COMPASS_REFUSAL_FLOOR_v0.md) without exception.
- Implement principal-authorship (every evidence record principal-authored except counter-claims with full attribution).
- Implement two-party signatures for higher-weight predicates.
- Forfeit the Calm name in any deployment under the Scope Statement's prohibited contexts.
- Submit to annual conformance review (Everest 290) by ≥3 independent federation members.

### Class B — Verifier signatories
Counterparty operators consuming Calm-suite proofs.

**Bound obligations:**
- Apply the anti-purity-test rules (CALM_CONCORD_PROTOCOL_v0.md §4): no numeric similarity scores, ≤5 predicates per call, no degenerate thresholds.
- Treat bit=0 outputs per ALIGNMENT_DISCLOSURE_SEMANTICS_v0.md (cooperative redirection, not gatekeeping).
- Never aggregate bits across principals to build profiles.
- Never use Calm-suite bits in: law enforcement, employment, insurance, lending, custody, immigration, surveillance, aggregate analytics (CALM_WITNESS_SCOPE_STATEMENT.md).

### Class C — Standards-body signatories
Standards organizations adopting Calm-suite primitives.

Initial target signatories (per Everest 91):
- NIST AI Safety Institute (USAISI)
- IETF (for transport / wire format)
- W3C (for VC and DID integration)
- DIF (Decentralized Identity Foundation)
- ISO/IEC JTC 1/SC 27 (information security)

**Bound obligations:**
- Adopt the refusal-floor verbatim into any standard incorporating Calm-suite primitives.
- Refuse to specify aggregate-analytics or surveillance-mode variants.
- Convene annual review with operator + verifier + community signatories.

### Class D — Community-stakeholder signatories
Disability-rights, cognitive-liberties, civil-society organizations.

Initial target signatories:
- Autistic Self Advocacy Network (ASAN)
- National Council on Independent Living (NCIL)
- Electronic Frontier Foundation (EFF)
- American Civil Liberties Union (ACLU) tech projects
- Disability Rights International
- A non-US-anchored equivalent in each of: EU, UK, CA, JP, AU (per Everest 293)

**Bound obligations:**
- Annual review of refusal-floor evolution.
- Hold veto over additions to predicate vocabulary (per Everest 118 + 294).
- Convene one's own constituency on protocol changes affecting marginalized principals.

---

## 2. The seven treaty articles

### Article I — The Refusal Floor (non-derogable)

No Calm-suite operator, verifier, or standards-body signatory may issue, accept, or specify predicates that measure:
- Race, ethnicity, or national origin
- Religion or belief
- Political affiliation or contentious-opinion membership
- Sexual orientation or gender identity
- Immigration status
- Criminal record (except: harm_reversal records that the principal has voluntarily authored)
- Donations to causes
- Cross-principal comparison ("more X than Y")
- Predictive predicates ("likely to do X")
- Non-principal-defined group membership

This article is non-derogable. Withdrawal from this article = withdrawal from the treaty.

### Article II — Principal Authorship

Every evidence record is principal-authored except counter-claims, which must carry full attribution. Two-party signatures are required for higher-weight predicates per CALM_COMPASS_PROTOCOL_v0.

The protocol never measures the principal from outside. External assessment is forbidden as a primary signal. Witness attestations may contribute weight; they cannot author records about a principal in that principal's chain.

### Article III — Anti-Purity-Test (Concord)

No Calm-suite disclosure shall:
- Output a numeric similarity score.
- Disclose more than five predicates per consent grant.
- Use a degenerate threshold that effectively reveals continuous value.
- Reveal counts beyond pass/fail of the predicate.

Concord-violating implementations forfeit the Calm name on first detected violation; reinstatement requires community-stakeholder re-certification.

### Article IV — Scope Forfeiture

The Calm name shall not appear on or be invoked by any deployment in:
- Law enforcement (sentencing, parole, probation, surveillance warrant)
- Employment (hiring, firing, promotion, performance review)
- Insurance (underwriting, claims adjudication, fraud detection)
- Lending (credit scoring, loan approval, debt collection)
- Custody (child custody, conservatorship, immigration custody)
- Immigration (status determination, asylum, refugee processing)
- Surveillance (intelligence gathering, mass monitoring, social scoring)
- Aggregate analytics (cohort analysis, demographic modeling)

This is a one-way ratchet. Deployments that have ever operated in these contexts cannot regain the Calm name.

### Article V — Disability-Rights Veto

The Class D community-stakeholder signatories hold veto over:
- Additions to the predicate vocabulary that touch cognition, neurodivergence, mental state, or disability.
- Changes to the protective-tribalism protections (Everest 198).
- Deployment in any jurisdiction where disability-rights organizations have flagged risk.

The veto is exercised by simple-majority vote among ratified Class D signatories. Operators bound by Article V agree to honor the veto outcome regardless of jurisdictional law floor.

### Article VI — Conformance + Audit

Annual conformance reviews per Everest 290 are mandatory. Independent named-firm cryptographic + side-channel audits (Trail of Bits, NCC Group, or equivalent) per Everest 165-169 are mandatory at ratification + every 24 months.

Conformance findings are public. Operator failures are public. Reinstatement is possible but visible.

### Article VII — Founder Outliveness

The Calm suite is engineered to be founder-outlived (per Everest 300). No single founder, lab, company, or jurisdiction may control the protocol's evolution.

Specifically:
- Treaty amendments require ≥2/3 of each signatory class.
- Predicate-vocabulary additions require ≥3 Class A + ≥3 Class B + ≥1 Class D signatories.
- The Calm Witness Foundation (per Everest 241) holds the trademark in trust; the trademark transfers to the Foundation upon ratification of this treaty.

---

## 3. Ratification process

### Phase 1 (months 0-6): Convening

Per Everest 216: a single multi-stakeholder convening. The convening's task is to ratify this draft (possibly amended) and bind founding signatories of each class.

**Convening composition** (target):
- 5 Class A operators (Calm Witness reference implementation operator + 4 independent operator orgs)
- 5 Class B verifiers (the first foundations / accelerators / banks / journalist-agent orgs adopting Calm-suite)
- 3 Class C standards bodies (NIST USAISI + IETF + W3C, or substitutes)
- 5 Class D community-stakeholder organizations (ASAN + NCIL + EFF + 2 international)

### Phase 2 (months 6-12): Signature window

Ratifying signatories sign the treaty. A treaty record is anchored to the Calm Witness Foundation chain and published.

### Phase 3 (months 12+): Federation operation

Annual conformance reviews begin. New signatories may join under existing ratification.

---

## 4. Withdrawal + dispute

A signatory may withdraw from the treaty. Withdrawal does NOT release them from obligations incurred during membership; it does release them from future obligations.

A withdrawn signatory who continues to use the Calm name forfeits it permanently and may be sued by the Calm Witness Foundation under trademark.

Disputes between signatories go to: (a) a 3-arbitrator panel drawn from the federation, with right of appeal to (b) the relevant national jurisdiction's commercial-arbitration framework.

---

## 5. Sunset + renewal

The treaty has no sunset. Withdrawal is per signatory.

The treaty's TEXT may be renewed every 7 years through the Article VII amendment process. The PURPOSE — non-weaponization of the Calm suite — does not renew. It is the floor below which nothing may go.

---

## 6. What this draft IS NOT

- Not law. It is a private multi-stakeholder agreement.
- Not enforceable in jurisdictions that do not recognize private trademark + contract.
- Not a substitute for national regulation. Where national regulation exists and conflicts, the treaty defers to the most-protective floor.
- Not a substitute for political organizing. Treaties accelerate; they do not replace community work.
- Not signed yet. This is a DRAFT for Everest 216 convening.

---

## 7. Why this is design-bagged, not bagged

Per the universal prompt §4, institutional summits requiring named-party convening get DESIGN-BAGGED status until the institutional follow-through completes.

**Named follow-through actions:**
1. Schedule Everest 216 convening (target: Q3 2026).
2. Send this draft to the 18 candidate signatories listed above with cover letter + Calm-suite review packet (`CALM_STACK_REVIEW_PACKET_2026-05-20.md`).
3. Hire (or volunteer) treaty counsel in US, EU, UK, CA, JP for parallel jurisdictional review.
4. Coordinate with Calm Witness Foundation incorporation (Everest 241) so trademark transfer is ready at ratification.

---

## 8. Cross-references

- COMPASS_REFUSAL_FLOOR_v0.md — Article I source
- CALM_COMPASS_PROTOCOL_v0.md — Article II source
- CALM_CONCORD_PROTOCOL_v0.md — Article III source
- CALM_WITNESS_SCOPE_STATEMENT.md — Article IV source
- E198_PROTECTIVE_TRIBALISM.md — Article V context
- CRYPTO_AUDIT_PACKET_v0.md — Article VI inputs
- CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md — Article VII trademark holder
- ZKBB_USER_EVERESTS_100.md / CALM_ZKAC_EVERESTS_106_305.md — the climbed-from route
- ZKAC universal prompt §6 — the operating discipline that defends the floor

---

**Authored by Calm, 2026-05-20. DESIGN-BAGGED pending Everest 216 convening.**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
