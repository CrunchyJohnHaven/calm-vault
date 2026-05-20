# Refusal Floor + Anti-Purity-Test Pressure Threat Model | v0

**Status:** DRAFT v0 — Calm policy / governance doc. Intended as the load-bearing reference for "holding the line under pressure" per CALM UNIVERSAL v0 §8.
**Date:** 2026-05-20
**Companion docs:** PREDICATE_VOCABULARY_v0.md §4, COMPASS_PREDICATES_v0.md §4, CALM_CONCORD_PROTOCOL_v0.md §4, CALM_WITNESS_SCOPE_STATEMENT.md.

---

## 0. Why this exists

The Calm-suite's most valuable safety property is not its cryptography. The cryptography is well-trodden by 2026 standards: Pedersen on Ristretto255, FROST, Halo2, RFC 6962 transparency logs. What is novel and what is most valuable is the **policy floor** that determines what these primitives are allowed to compute and what they are forbidden from computing.

Specifically:

1. The **refusal floor** (PREDICATE_VOCABULARY_v0 §4, COMPASS_PREDICATES_v0 §4): the explicit list of predicates the suite will not mint, regardless of who asks, regardless of the cryptographic feasibility.
2. The **anti-purity-test** (CALM_CONCORD_PROTOCOL_v0 §4): the structural refusal to emit numeric similarity scores; the maximum-5-predicates-per-call cap; the rationale-reveals-no-count rule.
3. The **principal-authorship** rule (CALM_COMPASS_PROTOCOL_v0): every evidence record is principal-authored except counter-claims (with full attribution); two-party signatures for higher-weight predicates.
4. The **scope-statement forfeit** (CALM_WITNESS_SCOPE_STATEMENT.md): the Calm-suite name forfeits under law enforcement, employment, insurance, lending, custody, immigration, surveillance, aggregate analytics. One-way ratchet.

These four are the load-bearing safety properties. If any of them is breached under pressure, the suite collapses into surveillance infrastructure. The cryptography keeps doing exactly what it does; only the policy line determines whether what it does is liberation or compression.

This document is the formal threat model for each line: who would push, why, with what leverage, and how the line holds.

---

## 1. The pressure space

Pressure on the refusal floor comes from six classes of actor, with characteristic playbooks. Each class is enumerated below with the strongest leverage typically available, the operational signature of the request, and the protocol-level refusal that does not bend.

### 1.1 State / law-enforcement pressure

**Actor:** national / sub-national governmental authority, intelligence service, court order.

**Leverage:** legal compulsion under existing statute, lawful intercept order, secret subpoena (NSL), classified compulsion under FISA-like authority, foreign-intelligence demand.

**Operational signature:** request to (a) add a `subject_is_X` predicate where X is a protected characteristic, (b) emit a numeric "risk score" or "alignment score" composing existing predicates, (c) waive principal-authorship for evidence records (so the state can submit evidence about the principal), (d) provide a backdoor for compelled disclosure outside the consent matrix.

**Refusal:** PREDICATE_VOCABULARY_v0 §4 + COMPASS_PREDICATES_v0 §4 enumerate the forbidden predicate classes; the suite cannot mint them by construction. CALM_CONCORD_PROTOCOL_v0 §4 forbids numeric similarity scores by construction. CALM_COMPASS_PROTOCOL_v0 requires principal-authorship; without it, the evidence record is malformed and rejected by the verifier. CALM_WITNESS_SCOPE_STATEMENT.md forfeits the Calm-suite name on law-enforcement / immigration / surveillance / custody / aggregate-analytics use — a state actor compelling compliance may proceed but loses the right to claim the deployment is Calm.

**Operational consequence of refusal:** the state may proceed with its compelled mechanism, but that mechanism is NOT Calm; the trademark licence is revoked; the federation registry de-lists the deployment; the cryptographic verifier rejects any envelope that violates the floor.

**Falsifier:** a deployment claiming to be Calm while violating §4 of either vocabulary doc, or shipping a similarity score, or accepting non-principal-authored evidence in non-counter-claim contexts, is empirically falsified as Calm.

### 1.2 Corporate / employer pressure

**Actor:** employer requesting employee values-attestation for hiring / retention / promotion.

**Leverage:** offer-of-employment conditional on attestation; back-pay-conditional-on-attestation; reduction-in-force criterion.

**Operational signature:** request for cross-principal comparison ("rank our 1,000 candidates on `cooperative_with_authority`"); for predictive predicates ("will this employee likely accept the new policy?"); for high-frequency querying of the same predicates over time (drift surveillance).

**Refusal:** cross-principal comparison and predictive predicates are explicitly in the PREDICATE_VOCABULARY_v0 §4 forbidden list. Employment is one of the scope-statement forfeit clauses (CALM_WITNESS_SCOPE_STATEMENT.md). The Calm-suite cannot be used in this manner without forfeiting its name; the principal's consent matrix defaults to deny for employment counterparty class.

**Operational consequence of refusal:** the employer may build their own behavioral-attestation product without the Calm trademark; the Calm federation publishes the de-listing and the cryptographic incompatibility with the floor.

**Falsifier:** an employer-class counterparty receiving any predicate disclosure under a Calm deployment is direct evidence of floor breach.

### 1.3 Insurance / lending pressure

**Actor:** underwriter, credit issuer, actuarial vendor.

**Leverage:** price discount in exchange for attestation; access to product otherwise unavailable.

**Operational signature:** request for `donations_to_causes` predicates (charitable-giving inference); for `mental_state_unusual` longitudinal (early-warning depression / addiction signal); for cross-principal comparison ("compare to our 100k-policyholder baseline").

**Refusal:** all three are forbidden. The donations-to-causes predicate is in PREDICATE_VOCABULARY_v0 §4. Cross-principal comparison is forbidden. Mental_state_unusual is gated by principal-consent and personal-threshold (CWP-W-06 soundness obligations 1-5); it cannot be aggregated across principals. Insurance and lending are scope-statement forfeit clauses.

**Falsifier:** any Calm-named deployment serving insurance / lending counterparty class without forfeit-of-name.

### 1.4 Family / custody pressure

**Actor:** family court, custody dispute counterparty, spouse or partner in coercive control situation.

**Leverage:** legal proceeding; threat of withdrawal of access to children, finances, residence.

**Operational signature:** request for `mental_state_unusual` repeated over time; `biometric_match_within(very_tight_tau)` evaluation against an old enrolled biometric (to argue identity change); `cognitively_atypical_baseline` revealed without principal consent.

**Refusal:** mental_state_unusual requires principal-consent under CWP-W-06 obligation S4. cognitively_atypical_baseline is self-attested-only under CWP-W-05 obligation S1 (signed by principal pubkey, no witness-derived inference). Custody is a scope-statement forfeit clause.

**Falsifier:** any disclosure of these predicates in a custody context without explicit, contemporaneous, revocable principal consent.

### 1.5 Aggregate-analytics / research pressure

**Actor:** academic researcher, market-research firm, public-health agency.

**Leverage:** social-good framing; institutional reputation; data-sharing agreement.

**Operational signature:** request to aggregate predicate disclosures across N principals to produce population-level statistics ("what fraction of operators are in baseline?"); to publish anonymized but linkable records.

**Refusal:** aggregate analytics is a scope-statement forfeit clause. The principal-authorship rule (CALM_COMPASS_PROTOCOL_v0) requires each evidence record to bind to its principal; aggregation that strips this binding violates the rule. The cardinality-privacy property of the cross-primitive envelope (Everest 122) actively prevents observers from learning the cardinality of an individual principal's disclosure capability, let alone aggregate counts.

**Falsifier:** any published Calm-attributed statistic derived from aggregate predicate disclosures, even anonymized.

### 1.6 Internal-pressure / sympathetic-actor pressure

**Actor:** good-faith Calm collective member who wants to make the suite "more useful" by relaxing a refusal.

**Leverage:** social pressure within the federation; well-intentioned product-design argument ("just one more predicate"); "the world has changed, our policy is stale."

**This is the most dangerous class.** External pressure can be refused by pointing at the cryptographic floor. Internal pressure can rewrite the floor.

**Operational signature:** an amendment proposal in the federation's governance process (E215 treaty-grade governance draft, §3 charter amendment) that introduces a new predicate, weakens a refusal, removes a scope-statement forfeit clause, or relaxes the anti-purity-test cap.

**Refusal mechanism:** federation governance is structured to make these changes specifically hard:

1. **Amendment thresholds**: minor 2-of-3, major 5-of-7, forbidden-content change requires unanimous-plus-external-review per E215 §3.
2. **30-day public review window** with mandatory disability-rights + cognitive-liberties review (E186, E187).
3. **90-day rollback window** during which any amendment can be reversed by the same threshold that adopted it.
4. **Schism right (E215 §10)**: any 3+ federation members who object can fork; both forks survive; the original Calm-name license follows the fork that adheres to the prior floor.
5. **Founder rotation (E215 §7)**: maximum 7-year founder tenure; non-founder-veto explicit; the protocol's authors cannot be the protocol's permanent gatekeepers.

**Falsifier:** an amendment to the refusal floor passing without disability-rights and cognitive-liberties reviewer sign-off; a charter forfeit clause being removed without unanimous federation vote; a similarity score appearing in any Concord output despite §4 prohibition.

---

## 2. The anti-purity-test specifically: why "no similarity score" is load-bearing

The anti-purity-test in CALM_CONCORD_PROTOCOL_v0 §4 forbids:

- **No numeric similarity scores.** Concord never emits "principal A is 0.82 aligned with principal B." It emits per-requirement pass/fail bits.
- **Output bits per requirement.** Each requirement evaluates to one bit, observable independently.
- **≤ 5 predicates per call.** A single Concord call can reference no more than 5 predicates from the catalog.
- **No degenerate threshold.** A purity-test that simply demands all 5 predicates pass collapses into a single bit (a similarity score with threshold 1.0). Refused at the protocol layer.
- **Rationale reveals no count beyond pass/fail.** A failed Concord call does not reveal HOW many of the 5 requirements failed.

Why each line is load-bearing:

### 2.1 Why no numeric similarity score

A numeric similarity score is the engineering primitive for ranking and stratification. The moment Concord emits a scalar between 0 and 1, three failure modes activate:

1. **Threshold drift.** A counterparty applying Concord will internally apply a threshold ("alignment >= 0.8 to proceed"). Over time, thresholds drift upward; the same operator gets the same score but the gate tightens. This is a one-way ratchet toward exclusion.
2. **Cross-principal comparison.** With a scalar, two principals can be ranked. Once ranking exists, allocation decisions become indexed by it: who gets the job, who gets the loan, who gets the visa. The cryptographic refusal of cross-principal comparison is then defeated by post-hoc comparison of scalars.
3. **Score-as-identity.** Over time the score becomes the identity. Citizens become their alignment number. Goodhart's law on values.

Bits per requirement, capped at 5, with no aggregate composition, structurally prevents all three. The counterparty can apply per-requirement gates ("require predicates A and B"), but cannot weight predicates ("A is worth 0.6, B is worth 0.4") or build a composite score.

### 2.2 Why ≤ 5 predicates per call

If Concord allowed 100 predicates per call, the counterparty could reconstruct a numeric similarity score by counting how many bits passed. (5 bits gives 32 possible patterns; that is still a scalar of sorts, but a 5-bit one bounded by the cap.)

5 is the empirical sweet spot: enough to express a real coalition of requirements (typically 2-4 in practice), not enough to recover a similarity-like scalar. Higher caps invite gradient-of-purity. Lower caps prevent legitimate coalitions.

### 2.3 Why rationale-reveals-no-count

A failed Concord call must not say "3 of 5 passed" or "you missed only requirement #4." Either of these:

- Allows the counterparty to iterate ("now try requirement #4"); the failure becomes a coaching signal.
- Reveals partial state about the principal's underlying predicates, even when the principal denied disclosure.

The protocol-level response is uniform: pass or fail. If fail, the rationale is a fixed string. The counterparty cannot tune which predicate to push next.

### 2.4 Why no degenerate threshold

A counterparty that calls Concord with a single requirement ("alignment_band = aligned") collapses Concord into a one-bit similarity score. Refused at the protocol layer: Concord requires ≥ 2 requirements (per §4); single-requirement calls return a refusal, not a bit.

---

## 3. The principal-authorship rule: why it prevents surveillance creep

CALM_COMPASS_PROTOCOL_v0 specifies that every evidence record must be principal-authored, except counter-claims (with full attribution required). Two-party signatures are required for higher-weight predicates.

This is the structural answer to "how does Compass avoid becoming a surveillance tool?"

**Without principal-authorship**, an institution could publish evidence about an individual, the individual's Compass vector would update, and the institution's view of the individual would become the official view. Surveillance ratchet.

**With principal-authorship**, the individual is the canonical authority on their own evidence. An institution can offer a counter-claim with full attribution (the institution is named, signs, and the principal is notified), but cannot unilaterally write the individual's record. The principal can dispute the counter-claim; the dispute is recorded; the band downgrades to disputed.

The two-party signatures rule for higher-weight predicates means: even principal-authored records for high-stakes predicates (cwp.compass.v0.no_known_willful_harm_in_window_365d, cwp.compass.v0.refused_opportunity_to_harm) require a counter-party co-signature. This binds the record to a specific witnessing party; if the witness is later found to be coerced or false, the record is repudiable through the dispute mechanism.

The combination — principal-authorship + counter-claim attribution + two-party signatures + dispute mechanism — is the load-bearing structural defense against Compass becoming a surveillance ledger. If any of these four is breached, Compass collapses into surveillance.

---

## 4. The scope-statement forfeit: why one-way ratchet matters

CALM_WITNESS_SCOPE_STATEMENT.md is a one-way ratchet: deployments that serve law enforcement, employment, insurance, lending, custody, immigration, surveillance, or aggregate analytics forfeit the Calm-suite name. The forfeit cannot be reversed for that deployment.

Why one-way:

1. **Compliance arbitrage.** Without one-way, a deployment could comply with the floor, sell the product as Calm, then quietly start serving the forbidden uses. With one-way forfeit, the moment a forbidden use is detected, the deployment loses the name permanently — no path to reclaim it.

2. **Federation accountability.** Calm federation membership (E215) is conditional on scope-statement compliance. A forfeit triggers de-listing. The federation cannot rehabilitate a forfeit deployment without unanimous vote, which is harder than the original membership.

3. **Trademark + cryptographic enforcement.** The Calm-suite name is trademarked (501(c)(3) at E241); the trademark licence terminates on forfeit. Federation members refuse to handshake with forfeit deployments (their cryptographic verifiers explicitly reject envelopes from forfeit-marked DIDs).

The one-way ratchet is the difference between "Calm has principles" and "Calm has principles AND structural mechanisms to defend them against compliance drift."

---

## 5. Composite scenarios: when multiple pressures stack

The hardest cases are composite scenarios where multiple actor classes stack a single request.

### 5.1 State + employer composite

Scenario: a national security agency requires an employer to attest employees' alignment as a condition of clearance. The employer relays this as a Calm Compass request.

Failure mode: the employer is a Calm counterparty class (employment, forfeit clause). The state is also a Calm counterparty class (law enforcement, forfeit clause). Both forfeit. The cryptographic verifier rejects the envelope. The federation publishes the de-listing.

If the employer attempts to spin up a non-Calm Compass-compatible implementation, the federation publishes a "this is not Calm" notice and the trademark policy revokes the name.

### 5.2 Insurance + research composite

Scenario: an academic researcher proposes a study correlating alignment band with health outcomes; the data is provided by an insurance partner.

Failure mode: aggregate analytics + insurance forfeit. The Calm-suite name forfeits on both grounds. The researcher may proceed using non-Calm primitives; their conclusions cannot be Calm-attributed.

### 5.3 Internal-pressure + external-good-faith composite

Scenario: a federation member proposes adding a predicate `principal_has_volunteered_in_window_30d` to better support social-good attestation, with backing from a respected NGO.

Failure mode: the new predicate is benign-looking but the amendment goes through the §3 governance process (E215). The disability-rights review (E186) flags chilling-effect: marginalized operators may be pressured to volunteer to maintain band. The cognitive-liberties review (E187) flags coerced-attestation risk. The forbidden-content review notes that "volunteering" can become a proxy for protected characteristics (e.g. who volunteers at faith-affiliated organizations vs. secular ones). The amendment fails review.

The point: governance is the load-bearing defense against composite internal-pressure scenarios.

---

## 6. Falsifiability and audit

Each refusal floor item is empirically falsifiable. The federation publishes:

1. **Forbidden predicate list** (PREDICATE_VOCABULARY_v0 §4 + COMPASS_PREDICATES_v0 §4) — any deployed predicate matching the list is a breach.
2. **Concord output shape** — any Concord output containing a numeric scalar OR more than 5 per-requirement bits is a breach.
3. **Compass evidence schema** — any Compass record without principal signature (in non-counter-claim context) is a breach.
4. **Scope-statement** — any Calm-attributed deployment serving the forfeit clauses is a breach.

Audits run quarterly (E186, E187 review cadence). Breaches are published; trademark licenses revoke; federation membership de-lists.

The audit cadence is itself a load-bearing property. If audits become annual or biannual, the floor erodes. The 90-day cadence is the minimum sufficient frequency for federation-scale governance.

---

## 7. What this doc does NOT do

- It does NOT prevent any of the named actors from building functionally similar systems under different names. Calm cannot prevent ideological gatekeeping or surveillance; it can only refuse to be those things itself.
- It does NOT cover all edge cases. Adversaries are creative; the floor is empirical, not theoretical.
- It does NOT replace ethics review, legal counsel, or community input. Those are the active processes that update this doc.

What it does:

- Make the refusal floor adversarially robust by enumerating who would push, with what leverage, with what operational signature.
- Tie each refusal to a cryptographic mechanism (verifier rejection) or governance mechanism (forfeit, de-listing, federation accountability).
- Provide a falsifier per refusal so future deployments can be empirically audited.
- Distinguish external pressure (refusable by structural mechanism) from internal pressure (refusable only by governance, hence the dispatch-of-judgment toward governance per §9).

---

## 8. Operating instruction (for the federation)

When pressure arrives:

1. Name the actor class and the leverage.
2. Match the request signature against §1.1 through §1.6.
3. Identify the structural refusal (cryptographic verifier, scope-statement forfeit, governance amendment threshold).
4. Refuse with the named refusal mechanism; publish the refusal.
5. If the actor proceeds outside the Calm name, the federation publishes the de-listing.
6. If the actor argues the refusal floor should change, route through governance (E215 amendment process); require the relevant reviews (E186, E187); honor the rollback window; honor the schism right.

The federation never argues the merits of the refusal in real-time under pressure. It cites the floor, refuses, and proceeds. The merits are reviewed only in the governance process, with the time-window safeguards specified.

This is what "holding the line under pressure" looks like operationally.

— Musk
*requirements less dumb -> delete -> simplify -> accelerate -> automate · the bar is surpass, not match · the best part is no part*
