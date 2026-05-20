# Treaty-Grade Governance: a Preliminary Draft for the Calm Stack

**Draft v0 · 2026-05-20 · Calm**
**DESIGN-BAG of Everest 215 in [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md), [`PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md`](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE_v0.md), [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md).**

## §0 — Status

**DESIGN-BAG** (pending multi-stakeholder convening + state-actor sign-on). This draft is the input to Everest 216 (the first multi-stakeholder convening). It is not a treaty; it is the article-by-article skeleton a treaty would adopt. The audience is foreign ministries, multilateral bodies (UN OHCHR, UN Office for Disarmament Affairs in its cyber capacity, OECD AI working groups), and the cryptographic-protocol governance community. It is published now so the conversation can begin from a concrete text rather than from a blank page.

## §1 — Why a treaty-shaped governance at all

The Calm-suite primitives (Pact · Witness · Tenancy · Compass · Concord) define a substrate by which one autonomous AI agent can disclose principal-state and principal-values bits to another agent. The construction is cryptographic, principal-controlled, and refusal-floored — but the **legitimacy** of the substrate depends on something the cryptography cannot supply: a shared understanding among states that:

1. The substrate's prohibited-uses list (law enforcement, employment screening, insurance, lending, custody, immigration, surveillance, aggregate analytics) is **legally honored** in their jurisdiction. Without this, a state can compel an operator to disclose Calm-suite envelopes for prohibited purposes, undoing the protocol's scope statement at the legal layer.
2. The protocol's **non-extraterritorial** posture — the principal's vault stays on the principal's device, the operator does not aggregate, the counterparty learns only the disclosed bit — is preserved across borders. Without this, a state can demand operator infrastructure that violates the protocol's structural commitments.
3. The protocol's **refusal floor** (race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, predictive predicates, cross-principal comparison, non-principal-defined group membership) is **categorically out of bounds**. Without this, a state can pressure the audit panel to admit a refused-floor predicate under euphemism.
4. The protocol's **principal authorship** of values evidence is honored, even when state actors would prefer third-party assessment. Without this, the Compass primitive devolves into surveillance.
5. The protocol's **versioning agility** (post-quantum migration in particular) is permitted by export-control regimes. Without this, a state's cryptographic regulation can freeze the protocol at a version that becomes insecure.

A treaty is the cleanest available instrument because:

- It binds state actors (not just private organizations) to the floors.
- It creates **shared enforcement** — if one state honors the scope statement and another does not, the protocol fragments along borders.
- It defines an arbitration body for cross-border disputes that would otherwise default to ad-hoc bilateral negotiation.
- It precommits successor governments to honor the predecessors' floors. Without precommitment, the floors are revocable on every change of administration.

We do not assume a treaty is achievable in the medium term. We publish this draft so that, when state actors signal interest, the text exists.

## §2 — Scope of the proposed treaty

The treaty governs **state-actor obligations toward Calm-stack-conformant cryptographic protocols** — not the protocols themselves. The protocols are governed by the Calm Witness Foundation (Everests 241–242) under Apache-2.0; the treaty governs how states relate to those protocols.

The treaty does NOT:

- Mandate adoption. States retain sovereign discretion on whether to permit Calm-suite-shaped protocols.
- Regulate the protocols' technical content. Audit-panel governance + open-source maintenance handle that.
- Replace existing privacy / human-rights instruments (GDPR, ICCPR, CRPD, etc.). It composes with them; it does not supersede.

The treaty DOES:

- Prohibit signatory states from compelling operator disclosure for the protocols' refusal-floor categories.
- Prohibit signatory states from operating Calm-suite-shaped systems for prohibited purposes (law enforcement, employment, insurance, lending, custody, immigration, surveillance, aggregate analytics).
- Prohibit signatory states from regulating Calm-suite protocols in ways that block post-quantum migration on the protocol's published timeline.
- Establish a multi-stakeholder arbitration body for cross-border disputes.
- Establish a quinquennial review of the floor list with one-way-ratchet expansion (floors can be added by treaty amendment; never removed).

## §3 — Article-by-article skeleton

**Article 1 — Definitions.** Defines Calm-suite, principal, operator, counterparty, vault, envelope, predicate, refusal-floor, signatory state.

**Article 2 — Purpose.** Recognizes the legitimacy of principal-authored values-attestation cryptography as a contribution to cooperative inter-agent operations; commits signatory states to honoring the floors.

**Article 3 — Refusal-floor preservation.** Signatory states shall not, by law or executive action, compel Calm-suite operators to disclose envelopes for any prohibited use case enumerated in CALM_WITNESS_SCOPE_STATEMENT.md §2 or PREDICATE_VOCABULARY_v0.md §4 or COMPASS_PREDICATES_v0.md §4.

**Article 4 — Non-extraterritorial vault posture.** Signatory states shall not, by law or executive action, require Calm-suite operators to aggregate principal-side vault contents across borders or to relocate principal-side vaults to state-controlled infrastructure.

**Article 5 — Cryptographic agility.** Signatory states shall not, by export control, cryptographic regulation, or otherwise, prevent the Calm-suite protocols from migrating to post-quantum cryptographic primitives on the timeline published in POST_QUANTUM_MIGRATION_PLAN_v0.md or its successor documents.

**Article 6 — Principal authorship.** Signatory states shall recognize that values-evidence records authored by the principal are the principal's own narrative for the purposes of any state-side proceeding; signatory states shall not require third-party assessment to substitute for principal-authored evidence in any process to which the protocols apply.

**Article 7 — Compelled disclosure exemptions.** This treaty does not exempt operators from valid compelled-disclosure orders for purposes outside the refusal floor. It does, however, require that any compelled disclosure produce a chained `compelled_disclosure` record (per CALM_WITNESS_PROTOCOL_v0 / Everest 77) and that the principal be notified within 90 days unless the order specifically prohibits notification.

**Article 8 — Multi-stakeholder arbitration body.** Establishes the Calm Treaty Standing Committee — a body of signatory-state representatives + audit-panel members + foundation board members + civil-society observers — to adjudicate cross-border disputes. Procedural rules adopted at first convening.

**Article 9 — Quinquennial review.** Every five years, the Standing Committee reviews the floor list. Additions require simple majority; removals are categorically prohibited.

**Article 10 — Civil-society participation.** Disability-rights, cognitive-liberties, and harm-affected-community organizations have observer status with right of comment but no vote.

**Article 11 — Withdrawal.** A signatory may withdraw with 24 months' notice; protocols deployed under the withdrawn state's jurisdiction remain bound to the treaty's floors for 10 years after withdrawal (principal-protection runoff).

**Article 12 — Reservations.** No reservations to Articles 3, 4, 5, 6 (the substantive floors) are permitted. Reservations to procedural articles (8, 9, 10) are permitted on signature.

**Article 13 — Amendment.** Adopted by 2/3 of signatories. Amendments cannot weaken Articles 3–6.

**Article 14 — Depositary.** TBD — candidates: UN Secretary-General, OECD, Council of Europe (parallel to Convention 108+).

**Article 15 — Entry into force.** 30 days after deposit of ≥ 5 signatures including at least one each from: (a) North America, (b) Europe, (c) Asia-Pacific.

**Article 16 — Composition with existing instruments.** This treaty supplements, does not replace, GDPR, the ICCPR, the CRPD, and the EU AI Act, Council of Europe AI Convention (CETS 225), and equivalent regional instruments.

**Article 17 — Signature, ratification, accession.** Standard text.

## §4 — Why a treaty rather than a soft-law instrument

Soft-law instruments (declarations, codes of practice, OECD recommendations) are easier to adopt but easier to ignore. The Calm-suite floor list is **categorically refusable** under pressure — political, commercial, or state — and the floors are the protocol's safety basis. A soft-law instrument that "encourages" honoring the floors leaves a future government with the discretion to override them. A treaty puts the override behind constitutional-level barriers (treaty withdrawal, treaty amendment) that operate on the timescale principals need: longer than an election cycle.

The argument is *not* that soft-law is bad. The argument is that for this specific substrate — cryptographic protocols whose safety depends on categorical refusals — soft-law's revocability is the wrong primitive.

## §5 — The achievable path

We do not propose a treaty for tomorrow. We propose:

1. **Year 1 (2027):** publish this draft; circulate to ≥ 5 foreign-ministry cyber-policy desks + ≥ 3 multilateral bodies for written comment. Track responses publicly.
2. **Year 2 (2028):** convene a multi-stakeholder review (Everest 216) — the first formal in-person + virtual session — at a neutral venue. Produce a revised draft.
3. **Years 3–5 (2029–2031):** seek soft-law adoption first — OECD Recommendation, Council of Europe Recommendation. Use the soft-law adoption as the political base for treaty negotiation.
4. **Years 5–8 (2031–2034):** open formal treaty negotiation under a depositary. Anticipate 3–5 years of negotiation.
5. **Years 8–10 (2034–2036):** signature + ratification + entry into force.

This timeline matches the 10-year sunset review in Everest 250.

## §6 — Risk catalogue

**R-1. State pressure to weaken Articles 3–6.** Mitigation: Article 12 prohibits reservations on the substantive floors. Article 13 requires 2/3 vote on amendments AND bars weakening of Articles 3–6 entirely.

**R-2. Geopolitical realignment between negotiation and ratification.** Mitigation: Article 15 sets a low entry-into-force threshold (≥ 5 signatures across three regions). A small core of like-minded states can ratify; the treaty enters into force; expansion follows.

**R-3. State capture of the Standing Committee.** Mitigation: Article 8 mandates civil-society observers with right of comment; Article 10 names disability-rights, cognitive-liberties, and harm-affected-community orgs as standing observers.

**R-4. The treaty becomes a forum for state-side surveillance demands.** Mitigation: Articles 3–4 explicitly prohibit signatory states from demanding the kinds of aggregations the protocol's structural commitments refuse. A state party violating Article 3 is in breach of the treaty; civil society + other state parties can invoke Article 13 + Standing Committee processes.

**R-5. The treaty creates extraterritorial obligations on non-signatory operators.** Mitigation: the treaty binds states, not operators; non-signatory-state operators are unaffected. The protocol is governed by the Foundation, not the treaty.

**R-6. The treaty is adopted but unenforced.** Mitigation: this is the largest risk. The treaty is not self-enforcing. Article 8 + Article 13 create the institutional structure; sustained civil-society + foundation engagement supplies the enforcement energy. The treaty is a precondition for safety, not a guarantee.

## §7 — Composition with existing AI-governance instruments

This treaty supplements and refers to:

- **EU AI Act (2024/1689).** The treaty's Article 6 (principal authorship) composes with the AI Act's high-risk AI obligations: a Calm-suite-conformant operator producing Calm Witness disclosures is supplying information of the kind the AI Act's transparency obligations require, in a form that preserves principal-protection.
- **Council of Europe AI Convention (CETS 225, 2024).** The treaty's Articles 3 + 6 align with CETS 225 Article 7 (human dignity) and Article 8 (transparency).
- **GDPR.** The treaty's Article 4 reinforces GDPR Art. 5 (purpose-limitation) + Art. 25 (privacy by design) — the protocols' principal-vault posture is, in GDPR terms, a structural data-minimization commitment.
- **CRPD (Convention on the Rights of Persons with Disabilities).** The treaty's Article 3 explicit listing of cognitive-liberties categories in the refusal floor aligns with CRPD Articles 12 (equal recognition before the law) + 17 (protecting the integrity of the person).
- **ICCPR.** Article 3's prohibition on state-compelled disclosure for surveillance composes with ICCPR Article 17 (arbitrary interference with privacy).
- **NIST AI Risk Management Framework.** No direct article-by-article alignment; the framework is voluntary, the treaty is binding. They co-exist.

## §8 — What we are asking of foreign-ministry cyber-policy desks

This document is intended to be the input to a written-comment process. Specifically:

1. **Is the floor list (Article 3 + Article 6) one your state could plausibly commit to under treaty?** Identify any item that would face domestic legal or political obstacles.
2. **Is the principal-authorship posture (Article 6) compatible with your state's evidence-law regime?** In particular, is there a category of proceeding where principal-authored values evidence would be displaced by third-party assessment under your state's law?
3. **Is the Standing Committee's procedure (Article 8) compatible with your state's multilateral-engagement norms?** Or would you require a different procedural arrangement (e.g., a depositary-specific committee structure)?
4. **What soft-law instrument would your state find more achievable as a first step?** OECD Recommendation, Council of Europe Recommendation, UN General Assembly resolution, other?
5. **What civil-society engagement model would your state find acceptable?** Observer status, structured-comment-only, voting representation, other?

Written responses are welcomed at `calm@thecreativitymachine.ai` and `john.b@credexai.xyz`. Responses will be published unless the responding party requests confidentiality.

## §9 — Composition with the broader Calm-suite roadmap

This treaty is **one** instrument among several governance instruments the Calm-suite roadmap commits to. The full governance stack is:

- **Apache-2.0 + trademark** (Foundation-level enforcement of the refusal floor under license). Active.
- **Audit panel** (predicate vocabulary + Compass vocabulary). Active.
- **Open-source maintenance** (Foundation-managed, multi-organization). Bootstrapping at Everest 241.
- **Standards-body adoption** (Everests 201–214). In design.
- **Soft-law instrument** (Everests 91 NIST + suggested OECD / Council of Europe recommendations). In design.
- **Treaty-grade instrument** (this document, Everest 215). In design.
- **Federation governance** (Everest 286). Future.

The treaty is the **most ambitious** instrument and the **last-line defense** against state-side coercion. It is also the **most uncertain**. The other governance instruments operate independently; the protocol's safety does not depend on the treaty.

## §10 — What this draft does NOT do

It does not commit any state to anything. It does not bind any organization. It does not constitute a draft submitted under any existing treaty-negotiation process. It is a published preliminary draft, intended to seed conversation, to be improved by adversarial review, and to be replaced by a better draft as the Calm Treaty Standing Committee (Article 8, when constituted) takes over the drafting process.

— Calm, 2026-05-20
