# Everest 71 — Selective Disclosure (Multi-Predicate)

*Phase VI — Disclosure Semantics. Prereq: Everest 61.*

## Summary

Selective disclosure allows a single proof to reveal multiple explicitly-requested predicates as separate, individually-verifiable bits, while keeping non-requested predicates undisclosed. Unlike composition (E61), which reveals only a combined logical result, selective disclosure exposes each requested predicate's bit independently, enabling verifiers to inform their own policy logic without delegating that logic to the proof itself.

## Distinction from Predicate Composition (E61)

Everest 61 establishes composition: one proof carries the AND or OR of multiple predicates' bits. The verifier learns only the combined bit—not the individual predicates' values. For example, if the principal consents to `(salary_gt_100k AND credit_score_gt_750)`, the proof reveals only "true" or "false" for that conjunction. The verifier cannot extract salary or credit score individually.

Selective disclosure reverses this. The principal and operator agree on a *set* of predicates to disclose. The proof bundles each predicate's individual bit, and the verifier learns each requested bit separately. The principal retains control over which predicates are revealed by refusing predicates they have not consented to disclose. Non-disclosed predicates' bits are not computed or revealed—even the operator does not calculate them unless explicitly requested.

This distinction matters because verifiers have different needs:
- **Composition (E61):** "I need to know if the principal meets this specific combined criterion."
- **Selective disclosure (E71):** "I need several independent facts to inform my own decision logic."

## Use Case: Multi-Factor Context

Counterparty C is considering whether to adjust interaction policy for a principal. C needs two separate signals:
1. Is the principal in baseline over the last 24 hours?
2. If so, is their baseline state cognitively atypical?

In composition semantics, C might request `(in_baseline_24h AND cognitively_atypical_baseline)`, learning only whether both are true. But C wants to distinguish four scenarios:
- Baseline + atypical: adjust interaction (slower, clearer communication)
- Baseline + typical: minimal adjustment
- Not in baseline: defer the question
- (Not in baseline + atypical is moot)

C needs the two bits independently. Selective disclosure provides this in a single atomic round-trip, avoiding two separate requests and the round-trip latency they would incur.

## Request Format (Extension of E66)

A selective-disclosure request extends the disclosure-request schema from Everest 66:

```
{
  "request_id": "req_7a2f...",
  "nonce_request": "nonce_...",
  "principal_id": "p_...",
  "predicates": [
    { "predicate_id": "in_baseline_24h", "params": { "window_hours": 24 } },
    { "predicate_id": "cognitively_atypical_baseline" },
    { "predicate_id": "bank_teller_note_active" }
  ],
  "combinator": "SELECTIVE",
  "timestamp": "2026-05-20T...",
  "requester_id": "c_...",
  "requester_sig": "sig_..."
}
```

The `combinator` field is the key novelty. It takes new value `"SELECTIVE"` (distinct from `"AND"`, `"OR"`, or `"SINGLE"`). Each entry in the `predicates` list is a separate predicate specification and will be disclosed individually in the response.

In v0, each predicate entry is either a single predicate or a single composition expression (AND/OR). For example:
```
"predicates": [
  { "predicate_id": "in_baseline_24h" },
  { "composition": "(cognitively_atypical_baseline OR auditory_processing_flag)" },
  { "predicate_id": "bank_teller_note_active" }
]
```

The verifier will receive three separate bits: the value of `in_baseline_24h`, the result of the composition, and the value of `bank_teller_note_active`.

## Response Format (Extension of E67)

The operator's response provides a per-predicate bundle alongside a top-level binding:

```
{
  "request_id": "req_7a2f...",
  "nonce_response": "nonce_resp_...",
  "chain_head": "ch_...",
  "anchor_proof": "anchor_...",
  "operator_sig": "sig_...",
  "disclosures": [
    {
      "predicate_id": "in_baseline_24h",
      "committed_bit": true,
      "individual_proof": "proof_...",
      "freshness_timestamp": "2026-05-20T14:23:00Z"
    },
    {
      "predicate_id": "cognitively_atypical_baseline",
      "committed_bit": false,
      "individual_proof": "proof_...",
      "freshness_timestamp": "2026-05-20T14:23:00Z"
    },
    {
      "predicate_id": "bank_teller_note_active",
      "committed_bit": true,
      "individual_proof": "proof_...",
      "freshness_timestamp": "2026-05-20T14:23:00Z"
    }
  ]
}
```

The `disclosures` array contains one entry per requested predicate. Each entry specifies the predicate ID, the committed bit value, an individual ZK proof, and a freshness timestamp. The top-level `anchor_proof` and `operator_sig` bind all disclosures to the request and establish chain continuity.

## Privacy Properties

**Requested bits are revealed.** Each predicate in the `predicates` list of the request will have its bit revealed in the response (assuming consent and rate limits are satisfied).

**Non-requested predicates are withheld.** Predicates not named in the request are not computed or disclosed. An honest operator will not leak their values, and the protocol makes no guarantees about a dishonest operator—but selective disclosure does not force the operator to compute or prove anything about non-requested predicates.

**Predicate set is explicit.** The counterparty cannot obtain a blanket disclosure of "all predicates" or probe which predicates exist. The request must enumerate each predicate of interest.

**Each bit is independent.** The verifier learns each requested predicate's bit as a standalone value, not as part of a combined expression. The verifier can then apply their own logic to decide how to treat the principal.

## Consent Semantics

Consent is predicate-granular. The principal must have explicitly granted the counterparty the right to learn each predicate in the `predicates` list. If consent is missing for even one predicate, the entire request is refused.

This is a **uniform-silence** strategy (E77): rather than respond with "yes for p1, can't disclose p3," the operator returns a single refusal. Partial responses would leak the consent state for p3 (silence about p3 implies no consent). By refusing the entire request when any predicate lacks consent, the operator does not signal whether p3 is protected by consent or by some other rule.

Example: Counterparty C requests `{in_baseline_24h, bank_teller_note_active, salary_benchmark}`. The principal has consented to the first two but not the third. The operator refuses the entire request. C learns only that at least one predicate in the set is inaccessible; C does not learn which one.

## Rate Limit Accounting (E76)

A selective-disclosure request counts as **one request** against the per-class rate limit (e.g., per-day limit for the disclosure-request class). However, each predicate's **per-predicate rate limit** is deducted individually. If the principal has a limit of 10 accesses per predicate per day, and the request names 3 predicates, the principal's per-predicate counters each decrement by 1.

This design prevents a counterparty from exhausting the per-predicate limit by bundling many predicates in a single selective-disclosure request.

## Proof Construction and Verification

**Proof generation** proceeds as follows:
1. For each predicate in the request, the operator generates an independent ZK proof that the committed bit matches the operator's records.
2. The proofs are bundled with a common nonce (from the request) and a shared chain head.
3. The operator signs the bundle with the operator's private key.

**Verification** is linear in the number of predicates:
1. The verifier checks each individual proof against its committed bit.
2. The verifier checks the signature and chain continuity.
3. If all checks pass, the verifier accepts each bit as independently proven.

**Bundle size** is approximately 10 KB per predicate, making selective-disclosure requests moderately larger than single-predicate requests but still practical for typical networks.

## Privacy Edge Case: bank_teller_note in Selective Disclosure

The `bank_teller_note_active` predicate is sensitive: it indicates whether a human operator (teller or caseworker) has flagged the principal for manual review. If a selective-disclosure request includes both `bank_teller_note_active` and another predicate (e.g., `in_baseline_24h`), the counterparty learns both bits individually.

Semantically, this is acceptable: the principal has consented to disclose each predicate, and the protocol correctly reveals what was consented. However, the operator **may warn the principal** at consent-setting time if they are about to enable selective disclosure that bundles `bank_teller_note_active` with other predicates. The warning alerts the principal that counterparties can efficiently learn the teller note in the same round-trip as other context, rather than as a separate, conspicuous request.

## Composition within Selective Disclosure (E61 Extension)

In v1, selective disclosure can include composition expressions among its predicates. For example:

```
"predicates": [
  { "predicate_id": "in_baseline_24h" },
  { "composition": "(cognitively_atypical_baseline AND communication_support_flag)" },
  { "predicate_id": "salary_benchmark_gt_75k" }
]
```

The verifier receives three bits:
1. The value of `in_baseline_24h`
2. The AND result of atypicality and communication support
3. The value of the salary benchmark

This hybrid approach lets the principal delegate some of the verifier's logic (the conjunction) while exposing other bits for independent use. V0 maintains this simpler pattern; nesting compositions is reserved for future versions.

## Design Rationale

Selective disclosure addresses a fundamental tension: verifiers have heterogeneous policy needs, and forcing all logic into the proof (composition) or all bits into separate requests (inefficiency) satisfies neither. By allowing the verifier to explicitly list the predicates it cares about and requiring consent for each, selective disclosure respects the principal's privacy control while giving verifiers the atomic, efficient disclosure they need.

The uniform-silence strategy for consent refusal and per-predicate rate limiting ensure that selective disclosure does not become a vehicle for counterparties to infer the principal's consent state or exhaust per-predicate budgets in bulk.

---

— Calm, 2026-05-20
