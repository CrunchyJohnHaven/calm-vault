# Everest 77 — Disclosure-of-Non-Disclosure

*Phase VI — Disclosure Semantics. Prereq: Everest 8.*

## The Decision

**v0 default: the operator returns a structurally-identical "no proof" response in ALL cases where a proof is not generated — refusal, error, consent absence, expired consent, rate-limit, network error.** The counterparty cannot distinguish refusal from any other not-generated reason.

This is the foundational choice that makes coercive-pressure resistance possible. A principal facing a counterparty that cannot determine WHETHER a refusal occurred will not face interrogation over WHY. Silence becomes structural safety.

## Rationale: Why Uniform Non-Disclosure

The threat model is direct: if a counterparty (insurance company, investigator, employer, creditor) can distinguish "the principal refused" from "we have no proof on file", the principal enters a coercive interrogation loop. The counterparty submits a disclosure request, observes a "refusal" response, and now knows that the principal made an ACTIVE CHOICE to withhold — not that consent was absent, not that a system error occurred, but that the principal *elected* not to provide proof.

Under interrogation, this distinction becomes devastating. "So you refused to show your bank records? What are you hiding?" The counterparty has moved from observing a null result to inferring agency. The principal can no longer claim ignorance, system unavailability, or technical delay. The principal has been caught choosing.

The bank-teller-note threat (Everest 58) is the canonical example: a bank teller knows that a customer either did or did not authorize disclosure. When the teller refuses a request, the customer sees refusal. But in the Calm Witness protocol, the inquirer sees only silence. The teller's refusal is structurally invisible to the counterparty. This invisibility is what permits the customer to deny knowledge of the inquiry, to refuse interrogation, and to resist coercion.

The operator's response must preserve this invisibility. The counterparty cannot be allowed to learn that a specific choice was made. The counterparty must instead operate in a state of permanent ambiguity: the no-proof response is uninformative. It could mean consent was missing. It could mean consent existed but was refused. It could mean the system was unavailable. It could mean rate limits applied. The counterparty cannot know.

This uniformity is the cost of safety. The principal trades observability for protection.

## The Uniform "No Proof" Response

The operator's disclosure handler responds to all not-generated cases with an identical HTTP surface:

- **Status code**: 204 (No Content) for all not-generated outcomes
- **Response body**: absent (empty payload)
- **Error messages**: none (no distinguishing text)
- **Operator-side logging to counterparty**: forbidden (the operator does not leak reason categories)

The counterparty's implementation must treat 204 as fully uninformative. Any attempt to infer principal state from this response violates the protocol's social contract (Everest 98, Counterparty Implementer's Agreement).

## Asymmetry: Principal Learns, Counterparty Does Not

The protocol creates a deliberate asymmetry in observability:

**The principal's audit trail (Everest 72) reveals full state:**
- kind: "disclosure" records capture the request predicate, timestamp, and counterparty identity
- refusal_reason field (principal-private) distinguishes: refused-no-consent, refused-expired-consent, refused-rate-limit, refused-explicit-deny, refused-error, refused-grace-period-exhausted
- The principal can always interrogate their own vault to understand why a disclosure did not generate a proof

**The counterparty observes only the response code:**
- 204 (No Content) means "I have no proof to return"
- No additional information is transmitted
- The counterparty cannot attribute the 204 to any specific cause

This asymmetry is intentional. The principal retains full knowledge of their own refusal behavior. The counterparty is structurally prevented from exploiting that knowledge.

## Blocking Side Channels

Three potential side channels exist and must be mitigated:

### Response Timing

If the operator returns "no consent" in 10ms and "explicit refusal" in 200ms, timing leaks the distinction. A sophisticated counterparty could submit a request and measure latency, inferring whether a refusal occurred.

Mitigation: pad all "no proof" responses to a uniform target latency (e.g., 250ms ± 50ms jitter). The operator sleeps or applies rate-controlled response buffering before returning the 204. The counterparty cannot distinguish causes by clock time.

### Rate-Limit Signals

If the operator applies rate limits per-counterparty and a 204 response is accompanied by rate-limit headers, the counterparty learns that they have been rate-limited. This does not leak refusal directly, but it reveals activity volume over time.

Mitigation: rate limits apply across the entire predicate space, not per-request. The counterparty cannot determine whether they have been rate-limited on a specific request or are simply within quota. All 204 responses are rate-limit-silent (no x-rate-limit-remaining headers exposed to counterparties).

### Aggregate Statistical Inference

Over 1000 requests across different principals and predicates, a counterparty will observe an aggregate success/no-proof ratio. They cannot infer individual principal state, but they learn the system's base rate.

Mitigation: this is accepted as inherent to the protocol. The aggregate signal does not enable coercion of any individual principal. The rate-limit design (Everest 76) ensures that a single counterparty cannot submit enough requests to reverse-engineer individual principal choices.

## What the Protocol Explicitly Does NOT Do

The operator never returns reason-specific error messages:

- "You don't have consent for this predicate" — forbidden (leaks consent state)
- "Consent expired on 2025-03-15" — forbidden (leaks that an active grant existed)
- "Rate limited after 47 requests" — forbidden (leaks activity volume)
- "System error: database unavailable" — forbidden (distinguishes error from refusal)

Each of these messages would provide the counterparty with information that, while individually small, collectively enables inference. The protocol opts for semantic silence instead.

## The Verifier Probe Attack (Rejected)

An adversarial counterparty might attempt to probe the consent space: request disclosure for predicate_A, observe 204; request disclosure for predicate_B, observe 204; iterate across 100 different predicates and correlate the pattern of 204 responses.

If different predicates returned different status codes or delays, the counterparty could infer which consents exist. But the protocol prevents this: all predicates that do not generate proofs return 204 with identical latency.

Defenses:
- Rate limits are global across the predicate space, not per-predicate. A probe attack exhausts the counterparty's quota quickly.
- The consent granularity (Everest 57) ensures that predicates are not independent; a counterparty cannot reason about individual predicate consent based on aggregate requests.

## Compromises Considered and Rejected

### Per-Class Disclosure of Refusal

One early proposal: allow certain counterparty classes (e.g., journalists, law enforcement) to opt into a "I can see refusal" mode.

Rejected because: a principal interacts with multiple counterparties across different classes. An employee faces both an employer and a journalist. If the journalist class gets refusal signals, the employer-class counterparty would eventually learn that the journalist had access to a different signal, creating class-based exploitation vectors. The uniform policy is safer than a differentiated one.

### Opt-In Disclosure of Refusal

Another proposal: the principal can opt into "tell counterparty X that I refused" for trusted relationships.

Rejected because: opt-in adds threat surface. A principal under duress might be coerced to opt in. A principal confused about the option might accidentally enable disclosure. A principal in a custody dispute might have their device manipulated to turn on opt-in. The v0 default is uniform silence. Opt-in can be re-evaluated in v1+ with additional safeguards (e.g., biometric confirmation, vault-server ceremony).

## Implementation Notes

The operator's disclosure handler has a unified "send no-proof response" code path:

1. Request arrives for disclosure of a proof
2. Handler evaluates: does a valid, unexpired, consented proof exist?
3. If NO (for any reason: no consent, expired, explicit deny, rate limit, error):
   - Route to unified no-proof handler
   - Apply timing padding (e.g., sleep to 250ms)
   - Return HTTP 204
   - Close connection
4. If YES:
   - Serialize proof
   - Return HTTP 200 with proof payload
5. Append audit record to vault (kind: "disclosure", with reason field for principal visibility)

The reason field in the vault audit record is never transmitted to the counterparty. The counterparty only sees the HTTP response.

## Counterparty Implementer's Guidance

For anyone building a system that receives 204 responses from a Calm Witness operator:

- A 204 response is informationally null. Do not log or infer the principal's internal state from it.
- Do not record in your system: "Principal refused disclosure" or "Principal withheld consent." Such logging violates the Counterparty Implementer's Agreement (Everest 98).
- Instead, log: "Disclosure request returned no proof" — which is factually accurate and does not presume the principal's choice.
- Do not change your behavior toward the principal based on receipt of a 204. You have no information.

## Relationship to Everest 78 (Stealth Disclosure)

Everest 77 and 78 are complementary safety mechanisms:

- **Everest 77 (this document)**: silence on inquiry. The operator returns nothing distinguishable when a refusal occurs.
- **Everest 78 (Stealth Disclosure)**: proactive speech without inquiry. The operator pushes a duress signal to pre-authorized counterparties in response to detected coercion, without waiting for a disclosure request.

E77 is defensive (hiding the principal's refusal). E78 is offensive (alerting the principal's defenders). Together they bracket the principal's safety.

## Edge Case: Principal Wants Counterparty to Know They Refused

Out of scope for the Calm Witness protocol. The protocol is not a communication channel for refusal announcements. If the principal wishes to inform a counterparty that they are refusing disclosure, they must do so via out-of-band means (email, phone, legal counsel).

The protocol's job is to prevent involuntary revelation. If the principal wants voluntary revelation, they can use any channel. This document does not constrain that choice.

## Cross-References

- **Everest 7, 8**: Consent axioms and foundational semantics
- **Everest 57**: Principal Consents to Disclose (consent predicate design)
- **Everest 58**: Bank Teller Note Active (canonical threat model)
- **Everest 66**: Request schema
- **Everest 67**: Response schema
- **Everest 72**: Disclosure logging and audit trails
- **Everest 76**: Rate limits and quotas
- **Everest 78**: Stealth disclosure (inverse mechanism)
- **Everest 98**: Counterparty Implementer's Agreement

---

## Addendum 2026-05-20 — Opt-In Semantics, Duress Composition, and Operator-Violation Closure

### Clarification: Opt-In Refusal Disclosure (Deferred to v1+)

The main document (§ "Compromises Considered and Rejected") explicitly rejects opt-in disclosure of refusal in v0 on threat-surface grounds: a principal under duress might be coerced into enabling the feature, or a principal in a custody dispute might have their device manipulated.

**v0 decision: No opt-in.** The principal cannot opt into per-(predicate, counterparty-class) "tell this counterparty that I refused" mode in v0.

**v1+ reopening:** Opt-in may be re-evaluated in v1+ if accompanied by safeguards such as biometric confirmation, vault-server ceremony, or a recovery-ceremony confirmation step. Any v1+ opt-in feature must be explicitly opt-in per (predicate_id, counterparty_class) pair—the principal cannot issue a blanket "disclose all refusals" grant—and must be revocable via the same ceremony. The principal's default remains uniform silence; refusal disclosure is always explicit, limited in scope, and requires affirmative principal action.

### Composition with Everest 8, Axiom A9 (Defeasibility by Duress Codeword)

Everest 8, Axiom A9 establishes that when `bank_teller_note_active` evaluates to true (principal has signaled duress), any consent record in the principal's "duress_invert_list" is inverted: the operator does not produce a proof, even if consent exists.

**Interaction with E77 (this document):**

- A principal under duress can invoke the bank-teller-note signal (E58) to flip `bank_teller_note_active = true`.
- This inverts consents for listed predicates (E8.A9), causing the operator to return 204 (no proof) even when the principal would normally consent.
- From the counterparty's perspective, the 204 is indistinguishable from any other refusal (no proof returned).
- The principal's vault logs the actual cause: `duress_invert_active` rather than `explicit_refuse` or `no_consent`.
- The operator applies uniform latency padding (§ "Response Timing") regardless of whether duress or explicit refusal triggered the 204.

This composition ensures that **duress is coercion-pressure-resistant by construction**: a counterparty cannot determine whether a 204 was caused by duress, refusal, missing consent, rate-limit, or system error. The indistinguishability is the safety mechanism.

### Composition with Everest 76 (Cooling-Off / Rate Limits)

Everest 76 § 8 ("Uniform-Silence Interaction") formalizes that rate-limit rejection is observationally identical to any other refusal. All five rate-limit dimensions (global, per-class, per-counterparty, per-predicate-per-class, per-predicate-per-counterparty) result in HTTP 204 (No Content) with no distinguishing headers, latency, or error text.

**Enforcement at E77 scope:**

- Rate-limit exhaustion: 204
- Consent missing: 204
- Consent expired: 204
- Explicit consent.deny: 204
- Cooling-off active: 204
- System error: 204
- Duress invert active: 204

The operator never leaks which rate-limit dimension was triggered. The principal's vault records the distinction in the refusal_reason field; the counterparty sees uniform silence. This uniformity is critical: if a counterparty could distinguish "rate-limited" from "refused," they could infer that the principal exists and is receiving requests, and could estimate request volume over time. The indistinguishable 204 prevents this inference.

### Operator-Violation Case: No Path to Refusal Distinguishability

**Structural closure:** There is no code path, operator configuration, or API surface that permits the operator to expose refusal-distinguishability to a counterparty.

**Enforcement mechanisms:**

1. **Unified response handler** (§ "Implementation Notes"): All not-generated cases route to a single `send_no_proof_response` code path. The operator computes `reason` (for principal audit), but this field is not serialized into the HTTP response.

2. **HTTP status code uniformity**: All not-generated cases return HTTP 204. Status codes 403, 401, 429, 503, or any other reason-specific code are forbidden in the v0 protocol.

3. **Response body emptiness**: 204 responses have no body. No error text, no JSON, no distinguishing content whatsoever.

4. **Header filtering** (E76): The operator never returns `X-RateLimit-*`, `X-Retry-After`, `X-Consent-State`, or any counterparty-visible metadata that would leak reason state.

5. **Latency padding** (§ "Response Timing"): All 204 responses are padded to a uniform target latency (≈250ms ± 50ms jitter), eliminating timing side channels.

**Scope Statement enforcement** ([CALM_WITNESS_SCOPE_STATEMENT.md](../CALM_WITNESS_SCOPE_STATEMENT.md) § 3.3): The predicate audit panel logs any proposal that would traffic in refusal-distinguishability and rejects it at triage.

**Violation response:** An operator that violates this closure (e.g., returns 403 for "consent denied" vs. 429 for "rate limited") is a scope-statement violator. Such an operator forfeits the right to call itself Calm Witness and is downgraded from CredexAI operator credential (CALM_REFUSAL_FLOOR_INDEX.md § 3).

---

— Calm, 2026-05-20
