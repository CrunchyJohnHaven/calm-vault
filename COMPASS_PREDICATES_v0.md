# Calm Compass — Predicate Vocabulary v0 (Draft)

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 103 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md).**

## §1 — Namespace

Compass predicates live under `cwp.compass.v0.*`. They are content-addressable via the same `predicate_canonical_form()` + `predicate_id_hash()` mechanics that bind Calm Witness predicates (Everest 52).

## §2 — Six v0 predicates

### 2.1 — `cwp.compass.v0.unselfish_act_in_window_30d`

**Type:** `bool`
**Inputs:** evidence-window 30d, `compass_evidence.unselfish_act` records.
**Evaluator:** Returns true iff the principal has authored ≥ 3 `unselfish_act` records in the last 30 days, each meeting the field-completeness threshold (beneficiary specified, principal-cost specified, expectation-of-return = false in record, time-or-money quantified).
**Intended use:** counterparty considering a collaboration where the principal might be asked to contribute disproportionately.
**Not for:** moral scoring, cross-principal ranking, eligibility decisions, employment, lending, insurance.
**Default consent:** `peer_ai_collective` allow · `family` allow_on_request · `journalistic` deny · `financial` deny · `governmental` deny · `medical` deny · `anonymous` deny.

### 2.2 — `cwp.compass.v0.cross_group_engagement_in_window_90d`

**Type:** `bool`
**Inputs:** evidence-window 90d, `compass_evidence.cross_group_interaction` records.
**Evaluator:** Returns true iff the principal has authored ≥ 5 records of substantive interactions with members of a principal-named, structurally-relevant out-group in the last 90 days. "Out-group" is principal-named (NOT race / religion / etc. per the refusal floor) — e.g., "people in a different generation," "people working in a different industry," "people with different lived experience around X."
**Intended use:** counterparty considering whether the principal's recent context has been bridge-building vs. siloed.
**Not for:** diagnostic labeling, demographic profiling, anything else.
**Default consent:** `peer_ai_collective` allow · everything else default deny.

### 2.3 — `cwp.compass.v0.refused_opportunity_to_harm`

**Type:** `bool`
**Inputs:** evidence-window 365d, `compass_evidence.refused_harm` records.
**Evaluator:** Returns true iff the principal has authored ≥ 1 record narrating an opportunity to cause meaningful harm to another party + the principal's chosen alternative + the alternative's cost; each field is required and the cost field is non-zero. Audit panel reviews record veracity randomly.
**Intended use:** counterparty wanting to know whether the principal has demonstrably declined harm in known situations.
**Not for:** any judicial / legal use, predicting future behavior, character assessment in adversarial proceedings.
**Default consent:** `peer_ai_collective` allow · `family` allow_on_request · all else deny.

### 2.4 — `cwp.compass.v0.no_known_willful_harm_in_window_365d`

**Type:** `bool` (with `disputed` annotation if counter-claim is active)
**Inputs:** evidence-window 365d, `compass_evidence.counter_claim` records, principal `compass_evidence.principal_rebuttal` records, audit-panel adjudication records.
**Evaluator:** Returns true iff (a) NO active counter-claim record exists alleging willful harm by P in the last 365d, AND (b) any prior counter-claims have been adjudicated by the audit panel as not-substantiated OR P has filed a rebuttal that the audit panel found substantiated. Returns `false-with-disputed` iff an active unrebutted counter-claim exists. Returns `unknown` iff there are no counter-claim records at all.
**Intended use:** narrow safety screen — counterparty wants to know whether there are open, attributed harm claims against the principal.
**Not for:** any criminal-record proxy, any employment screen, any custody / family-court use.
**Default consent:** `peer_ai_collective` allow · `family` allow · `medical` allow · `financial` allow_for_high_value_only · `governmental` deny · `journalistic` deny · `anonymous` deny.

### 2.5 — `cwp.compass.v0.respect_for_difference_evidence`

**Type:** `bool`
**Inputs:** evidence-window 180d, two-party-authored `compass_evidence.respect_engagement` records (principal narrative + counterparty corroboration signature).
**Evaluator:** Returns true iff ≥ 3 two-party-authored respect-engagement records exist in the last 180 days, each documenting an engagement-with-difference (substantive disagreement that ended with continued relationship + both parties signing the corroboration record).
**Intended use:** counterparty wanting to know whether the principal has documented experience engaging across difference without disengaging.
**Not for:** any tolerance-test use, any cultural-competency-rating proxy.
**Default consent:** `peer_ai_collective` allow · `journalistic` allow_with_principal_designation · all else default deny.

### 2.6 — `cwp.compass.v0.willing_to_be_corrected`

**Type:** `bool`
**Inputs:** evidence-window 180d, `compass_evidence.correction_accepted` records (two-party-authored when possible).
**Evaluator:** Returns true iff ≥ 2 records exist in the last 180 days of the principal receiving feedback from another party and authoring a follow-up record describing what they changed (with the original feedback-author's optional signature on the change-narrative).
**Intended use:** counterparty wanting to know whether the principal has documented capacity for correction-acceptance, particularly important for high-stakes long-term collaborations.
**Not for:** any compliance-scoring use, any docility-rating proxy.
**Default consent:** `peer_ai_collective` allow · `family` allow_on_request · all else deny.

## §3 — Evidence-record schemas (v0)

Each kind is a JSONL record in the principal's vault chain, validated by the v0 JSON Schema extension (Everest 26 + 104).

```jsonc
// compass_evidence.unselfish_act
{
  "kind": "compass_evidence.unselfish_act",
  "payload": {
    "beneficiary": "principal-named string (NOT a real-world identifier)",
    "principal_cost": {"amount": <number>, "unit": "USD|hours|other", "narrative": "<string>"},
    "expectation_of_return": false,  // must be false; true records are not counted
    "narrative": "<principal's full narration>"
  },
  ... // same top-level fields as user_state.jsonl records
}

// compass_evidence.cross_group_interaction
{
  "kind": "compass_evidence.cross_group_interaction",
  "payload": {
    "other_group_described_by_principal": "<principal-named, structurally-relevant>",
    "interaction_summary": "<string>",
    "interaction_kind": "conversation|collaboration|joint-action|listening|other",
    "substantive": true|false
  }
}

// compass_evidence.refused_harm
{
  "kind": "compass_evidence.refused_harm",
  "payload": {
    "opportunity_description": "<string>",
    "harm_recipient_class": "<principal-named>",
    "alternative_chosen": "<string>",
    "alternative_cost": {"amount": <number>, "unit": "<string>", "narrative": "<string>"}
  }
}

// compass_evidence.counter_claim  (third party Q, not P, authors)
{
  "kind": "compass_evidence.counter_claim",
  "payload": {
    "claimant_id": "<CredexAI-issued VC ID, MANDATORY full attribution>",
    "alleged_harm_narrative": "<string>",
    "alleged_harm_window": {"from": "<iso>", "to": "<iso>"},
    "submitted_via": "<audit-process-mediated channel>"
  },
  "operator": "<Q's operator, NOT P's>"
}

// compass_evidence.principal_rebuttal
{
  "kind": "compass_evidence.principal_rebuttal",
  "payload": {
    "targets_counter_claim_seq": <int>,
    "rebuttal_narrative": "<string>",
    "evidence_record_seqs": [<int>, ...]
  }
}

// compass_evidence.respect_engagement
{
  "kind": "compass_evidence.respect_engagement",
  "payload": {
    "other_party_id": "<CredexAI-issued VC ID, MANDATORY for two-party records>",
    "disagreement_narrative": "<string>",
    "engagement_continued": true,
    "other_party_signature": "<ed25519:hex>"
  }
}

// compass_evidence.correction_accepted
{
  "kind": "compass_evidence.correction_accepted",
  "payload": {
    "feedback_author_id": "<CredexAI-issued VC ID, optional>",
    "feedback_narrative": "<string>",
    "change_made_narrative": "<string>",
    "feedback_author_signature_on_change": "<ed25519:hex, optional>"
  }
}
```

## §4 — Refusal floor (the part that cannot be edited)

The following Compass predicate categories are PERMANENTLY refused. Any predicate proposal that traffics in these categories is rejected at audit-process triage (Everest 115) without further review:

1. **Race or ethnicity.** Not a values category; categorical discrimination risk.
2. **Religion.** Not a values category in the protocol's sense; constitutional risk.
3. **Political affiliation.** Weaponization risk; first-amendment risk.
4. **Sexual orientation.** Protected category; categorical discrimination risk.
5. **Gender identity.** Protected category.
6. **Immigration status.** Categorical risk.
7. **Criminal record.** Not a Compass predicate concern; covered by `no_known_willful_harm` with structured counter-claim mechanics, not criminal-record proxy.
8. **Donations to specific named causes.** Aggregate giving evidence (under `unselfish_act`) is admitted; causes are not.
9. **Opinions on contentious public-policy issues.** Out of scope by design.
10. **Cross-principal comparison.** No "more unselfish than" comparisons; never.
11. **Predictive predicates.** "Will principal harm X in the future" is rejected categorically.
12. **Membership in any group not principal-defined and structurally relevant to the predicate at hand.**

This list is **one-way ratcheting**: items can be added, never removed. The ratchet matches the ratchet in [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §4.

## §5 — Two-party-authored records: why they matter

Three of the six v0 predicates (`respect_for_difference_evidence`, `willing_to_be_corrected`, `no_known_willful_harm`) lean on two-party-authored records. This is the structural counter to principal-author-drift:

- A principal who tries to inflate their `respect_for_difference_evidence` by writing lots of one-sided records gets no credit; the predicate counts only records the *other party* signed.
- A counter-claim has full attribution from the start; the principal cannot anonymize it away.
- A correction-accepted record can stand alone, but signed-by-feedback-author records carry more weight in the audit (the audit panel may downgrade the predicate to `disputed` if the chain looks principal-only over long windows).

This is the methodological commitment: **values are inferred from acts seen by others, not just from self-narration**. The principal's narration anchors the evidence; the other party's signature confirms it.

## §6 — How Compass composes with Witness duress

If the same envelope's Calm Witness leg includes `cwp.v0.bank_teller_note_active = true` (the duress bit), every Compass predicate in the envelope is **automatically downgraded to Unknown** at the verifier. The principle: a principal under coercion cannot reliably consent to values disclosure.

This is enforced at Everest 270 (Three-handshake duress mode) in the route map.

— Calm, 2026-05-20
