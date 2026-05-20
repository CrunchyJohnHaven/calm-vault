# Everest 76 — Cooling-Off / Rate Limits

*Phase VI — Disclosure Semantics. Prereq: Everest 73.*

---

## Purpose

Calm Witness disclosure is a high-stakes mechanism: a principal's attested state can inform critical decisions (credit, medical, journalistic, legal, employment) made by counterparties. Rate limits and cooling-off windows are enforcement gates that sit BEFORE consent evaluation and proof generation. They prevent exhaustion attacks, enumerate attacks, and denial-of-service (DoS) scenarios where a hostile or compromised counterparty floods the operator with requests in hopes of overwhelming the vault or disrupting legitimate service.

This everest specifies five dimensions of rate limiting, cooling-off windows that activate after refusal, the enforcement order when a request arrives, and the operator's audit and logging practices. Critically, rate-limit rejections are recorded in the principal's disclosure log with full reason codes—visible to the principal, opaque to the counterparty, in keeping with Everest 77 (Disclosure-of-Non-Disclosure).

---

## 1. Rate-Limit Dimensions

Rate limits are enforced in layers, each with independent capacity and refill rate. A request must pass ALL five checks to proceed to consent and predicate evaluation.

### 1.1 Global Rate Limit (Across All Counterparties)

**Definition**

The operator enforces a global maximum number of disclosure requests per 24 hours, aggregated across all counterparties and all predicates.

**Default and Tuning**

- Default: 200 requests per 24h.
- Principal-tunable via: `calm-witness rate-limit set --dimension global --max-per-24h <N>`
- Changes append a rate-limit-update record to the disclosure log with timestamp and principal signature.

**Token Bucket Model**

- Capacity = N tokens.
- Refill rate = N / 86400 tokens per second.
- On each request, deduct 1 token (or more for high-cost operations; see §1.5).
- If bucket is empty (≤0 tokens), request is rate-limited.

**Rationale**

Global rate limits prevent pathological load on the operator. A single compromised counterparty cannot exhaust the entire operator's capacity for all principals. If one adversary attempts to DoS the operator, the global limit provides a circuit breaker. However, this limit is coarse and is always paired with per-counterparty limits.

### 1.2 Per-Class Rate Limit

**Definition**

For each of the ten counterparty classes (Everest 7), the operator enforces a maximum disclosure rate per 24 hours from any counterparty in that class.

**Defaults (Per Everest 7)**

| Class | Default Max/24h |
|-------|-----------------|
| financial | 20 |
| journalistic | 3 |
| medical | 50 |
| governmental | 1 |
| peer_ai_collective | unlimited |
| family | unlimited |
| anonymous | 1 |
| employer | 5 |
| insurance | 0 |
| research | 5 per protocol per 30d |

**Tuning**

`calm-witness rate-limit set --class <class_id> --max-per-24h <N>`

**Enforcement**

At request time, the operator inspects the counterparty's CredexAI VC for class assertions. If the VC asserts class `C`, the operator checks whether requests from class `C` have exhausted the per-class limit in the current 24-hour window. If so, request is rate-limited.

**Token Bucket Model**

Identical to global: capacity = N, refill = N/86400 per second.

**Rationale**

Different classes have different threat models. Medical providers may legitimately need many requests per day (emergency escalations, care coordination). Governmental agencies require extreme caution (max 1/day). Journalistic requests are rare and high-stakes (max 3/day). Per-class limits let the principal tune for the risk profile and use case of each class.

### 1.3 Per-Counterparty Rate Limit

**Definition**

For each individual counterparty identity (identified by a VC fingerprint), the operator enforces a maximum disclosure rate per 24 hours.

**Default**

20 requests per 24 hours.

**Tuning**

Per-counterparty limits can be set tighter or looser than the per-class default:

`calm-witness rate-limit set --counterparty <vc_fingerprint> --max-per-24h <N>`

Example: JPMorgan (financial class) gets 20/day (class default), but a principal's personal financial advisor at JPMorgan can be granted 50/day (per-counterparty override).

**Token Bucket Model**

Separate bucket per counterparty. Capacity = N, refill = N/86400 per second.

**Rationale**

Prevents a single adversarial counterparty from monopolizing the principal's disclosure quota. Even if the global and per-class limits are high, a single counterparty cannot flood the operator with 1000 requests per hour to enumerate predicates, correlate timing with chain activity, or conduct statistical attacks.

### 1.4 Per-Predicate-Per-Class Rate Limit

**Definition**

For each combination of (predicate_id, class_id), the operator enforces a maximum disclosure rate per 24 hours.

**Default**

50% of the per-class rate limit, rounded down. Example: if financial class = 20/day, then per-predicate-per-class for ANY financial class request = 10/day.

**Tuning**

`calm-witness rate-limit set --predicate <predicate_id> --class <class_id> --max-per-24h <N>`

**Rationale**

Prevents a counterparty from hammering the same predicate across multiple members of a class. For example, a hostile financial actor might request `mental_state_unusual` from 100 different banks trying to correlate which banks have recent consent grants. Per-predicate-per-class limiting prevents this: all banks in the financial class, collectively, can only get `mental_state_unusual` responses up to the per-predicate-per-class quota.

### 1.5 Per-Predicate-Per-Counterparty Rate Limit

**Definition**

For each combination of (predicate_id, counterparty_identity), the operator enforces a maximum disclosure rate per 24 hours.

**Default**

Same as per-counterparty rate limit (20 requests per 24h).

**Tuning**

`calm-witness rate-limit set --predicate <predicate_id> --counterparty <vc_fingerprint> --max-per-24h <N>`

**Cost Multipliers**

High-cost predicates consume more tokens. Example cost schedule:
- Simple predicates (in_baseline_24h, biometric_match_within): 1 token.
- Composite predicates (AND/OR combinations): 1.5 tokens.
- Expensive predicates (involving long chain scans): 2 tokens.

**Rationale**

Ensures a single counterparty cannot conduct a predicate-enumeration attack: ask JPMorgan for predicate_A 100 times, predicate_B 100 times, etc., and time the delays to infer which predicates are consented. Per-predicate-per-counterparty limiting caps the requests for a specific predicate from a specific actor.

---

## 2. Cooling-Off Windows

After a counterparty receives a False response (or a refusal due to no consent), a per-(counterparty, predicate) cooling-off window activates.

### 2.1 Definition and Duration

**Cooling-Off Window**

After a counterparty receives a 204 (No Content) response to a disclosure request for predicate `p`, that counterparty cannot request disclosure of the same predicate `p` for 1 hour.

**Per-Tuple Granularity**

The cooling-off window is per (counterparty_id, predicate_id) tuple. Counterparty A can request different predicates during the cooling-off window; they are only blocked from re-requesting the same predicate that was refused.

**Storage**

Each active cooling-off window is recorded in the vault as a `kind: "cooling_off"` entry with fields:
- counterparty_vc_fingerprint
- predicate_id
- window_start_timestamp
- window_end_timestamp (start + 1 hour)

**Enforcement**

At request time, before any rate-limit or consent check, the operator queries the vault's active cooling-off records. If the (counterparty, predicate) tuple has an active cooling-off window, the request is rejected with a 204 response (observationally identical to any other refusal, per Everest 77).

### 2.2 Rationale

Cooling-off windows prevent repeated requests for the same predicate in rapid succession. Without this, a counterparty could ask "Is the principal in baseline?" at second 0, receive a False. Then ask again at second 1, receive False again. By second 60, they have 60 false responses and can statistically infer whether the principal's state is genuinely false or whether the principal is exercising a refusal.

The 1-hour window is calibrated to prevent this enumeration: a counterparty can learn one bit (true or false) about a predicate per hour, per counterparty, capped by rate limits above.

### 2.3 Counterparty Visibility

The counterparty observes only a 204 response. They do not learn whether they hit a cooling-off window, a rate limit, or a consent denial. The principal's vault logs the specific reason; the counterparty sees uniform silence (Everest 77).

---

## 3. Enforcement Order

When a disclosure request arrives, the operator enforces checks in a strict order. This order is critical: rate limits are checked BEFORE consent, ensuring that a rate-exhausted counterparty cannot cause logging churn in the consent-evaluation layer.

1. **Schema Validation** — Is the request well-formed? Does it include required fields (counterparty_vc, predicate_id, signature)?
2. **Signature Verification** — Is the request signature valid? Is the counterparty's CredexAI credential current and not revoked?
3. **Global Rate Limit Check** — Has the global 24h quota been exhausted?
4. **Per-Class Rate Limit Check** — Has the counterparty's class-specific 24h quota been exhausted?
5. **Per-Counterparty Rate Limit Check** — Has this specific counterparty's 24h quota been exhausted?
6. **Per-Predicate-Per-Class Limit Check** — Has the (predicate, class) 24h quota been exhausted?
7. **Per-Predicate-Per-Counterparty Limit Check** — Has the (predicate, counterparty) 24h quota been exhausted?
8. **Cooling-Off Window Check** — Is this (counterparty, predicate) tuple in an active cooling-off window?
9. **Consent Evaluation** — Does the principal have valid, unexpired consent for this predicate to this counterparty (or class)?
10. **Predicate Evaluation** — What is the truth value of the predicate over the current vault state and biometric distance?

**Failure Response**

If any of steps 1–8 fail, return HTTP 204 (No Content) with an empty body. Do not proceed to steps 9–10.

Record the refusal in the vault's disclosure log with fields:
- timestamp
- counterparty_vc_fingerprint
- predicate_id
- refusal_reason (principal-visible code: "rate_limited_global", "rate_limited_class", "cooling_off", "signature_invalid", "schema_invalid", etc.)
- (NO reason is transmitted to the counterparty; see Everest 77)

**Success Response**

If all 10 steps succeed, serialize the ZK proof, return HTTP 200 with proof payload, and record a successful disclosure in the vault with kind: "disclosure" and refusal_reason: null.

---

## 4. Why Rate Limits Precede Consent

This ordering is deliberate and critical to the protocol's security.

**Defense Against Log Churn**

If consent evaluation happened before rate limiting, a rate-exhausted counterparty could still submit requests, causing the operator to:
- Parse the request.
- Load and traverse the consent chain.
- Evaluate predicates against the principal's state.
- Log each evaluation in the principal's vault.

A hostile actor could trigger thousands of consent evaluations per second, filling the vault's log with spurious entries and slowing legitimate operations.

**Rate Limits as Outer Gate**

By checking rate limits first (steps 3–7), the operator stops hostile load before it reaches the consent evaluation layer. The vault's disclosure log records rate-limit rejections (for principal audit), but the operator's CPU and I/O are protected.

**Token-Bucket Refill and Cool-Down**

If a counterparty exhausts their quota, the operator can also apply an optional auto-quiet feature:

- **Auto-Quiet Duration**: After a counterparty hits a rate limit, they are refused all subsequent requests (across all predicates) for 30 minutes.
- **Rationale**: Signals to the counterparty's operator (if well-behaved) that they are exceeding quota and should back off.
- **Implementation**: Query the vault for the most recent rate-limit-rejection entry for this counterparty and its timestamp. If fewer than 30 minutes have elapsed, auto-reject all requests with 204 (cooling-off).

After the 30-minute quiet window expires, tokens begin refilling at the normal rate (capacity / 86400 per second).

---

## 5. Principal Tuning and Audit

### 5.1 Commands

```bash
# Set per-class rate limit (default: 20)
calm-witness rate-limit set --class financial --max-per-24h 50

# Set per-counterparty limit (override class default)
calm-witness rate-limit set --counterparty vc:jpm.banking.org:2026-04 --max-per-24h 100

# Set per-predicate-per-class limit (override 50% default)
calm-witness rate-limit set --predicate mental_state_unusual --class medical --max-per-24h 20

# Set global limit (default: 200)
calm-witness rate-limit set --dimension global --max-per-24h 500

# View current rate-limit status and token consumption
calm-witness rate-limit status
```

### 5.2 Audit and Transparency

The principal can query rate-limit consumption in real time:

```bash
calm-witness rate-limit status --class financial
# Output:
# financial: 8 requests / 20 per 24h (40% consumed)
# Token bucket: 12 tokens remaining, refilling at 0.0002 per second
# Last request: 2026-05-20T10:15:32Z (JPMorgan)
```

The principal can inspect individual rate-limit-rejection entries in the disclosure log:

```bash
calm-witness log --kind rate_limited --since 2026-05-01
# Outputs all rate_limited entries, with counterparty, predicate, dimension, and time of rejection
```

### 5.3 Updates and Chain Recording

When the principal changes a rate limit, the change is recorded in the vault as a `kind: "rate_limit_update"` record:

```json
{
  "kind": "rate_limit_update",
  "seq": 847,
  "timestamp": "2026-05-20T14:00:00Z",
  "dimension": "class",
  "target": "financial",
  "old_max_per_24h": 20,
  "new_max_per_24h": 50,
  "principal_signature": "..."
}
```

This record is chained and published to Sigsum (per Everest 20 anchor protocol). Rate-limit changes are auditable and non-repudiable.

---

## 6. Adversarial Scenarios

### 6.1 Exhaustion Attack

**Scenario**

Adversary A, claiming to be a financial advisor (financial class), submits 50 requests in 1 second to enumerate which predicates the principal has consented to disclose.

**Defense**

- Per-class rate limit (financial: 20/24h) rejects requests 21–50 with 204 (no distinction to A between rate-limit and refusal).
- Per-predicate-per-class limit (each predicate: ≤10/24h for financial class) ensures that even if A tries a different predicate each time, they hit the predicate quota quickly.
- Per-counterparty rate limit (A: 20/24h) caps A's total requests to 20, regardless of class or predicate.
- A cannot distinguish rejection from refusal; A learns nothing about which predicates are consented.

### 6.2 Sock-Puppet DoS

**Scenario**

Adversary creates 100 fake counterparty identities (sock-puppet VCs) to bypass the per-counterparty limit.

**Defense**

- Global rate limit (200/24h) bounds the total requests from all 100 puppets combined to 200 per 24 hours.
- CredexAI VCs are issuance-rate-limited (out of scope for this document; see Everest 11 enrollment ceremony).
- The principal can deny specific counterparties via per-counterparty consent.revoke (Everest 73), invalidating their proofs.

### 6.3 Timing-Correlation Attack

**Scenario**

Adversary observes that the principal's disclosure requests spike at certain times of day, and tries to correlate this with the principal's state changes.

**Defense**

- Cooling-off windows (1 hour minimum between same predicate requests) prevent rapid re-probing.
- Rate limits force requests to be spaced out over 24 hours.
- The operator applies latency padding (Everest 77) to all responses, eliminating timing side channels.
- The principal's own disclosure requests are logged in the vault (per Everest 72, kind: "disclosure"), but the counterparty never learns what proofs the principal has requested for themselves.

### 6.4 Colluding Counterparties

**Scenario**

Counterparties A and B (both financial class) collude to share information about disclosure patterns and collectively reverse-engineer the principal's consent.

**Defense**

- A submits requests for predicates 1–10, learns (via 204 responses) that some return within 1ms and others within 200ms (hypothetically, if timing side channels leaked).
- B submits requests for predicates 11–20.
- Together they attempt to correlate patterns.
- Mitigation: Latency padding (Everest 77) ensures all 204 responses take identical time, eliminating timing correlation. The principal's revocation notices (Everest 75) are pushed to all verifiers, and revocation is tamper-evident. Collusion is mitigated by structural uniformity, not by hiding who A and B are.

---

## 7. Token-Bucket Implementation

All five rate-limit dimensions use a token-bucket algorithm:

### 7.1 Data Structure

For each rate-limit bucket (global, per-class, per-counterparty, per-predicate-per-class, per-predicate-per-counterparty):

```json
{
  "bucket_id": "class:financial",
  "capacity": 20,
  "tokens_remaining": 18.5,
  "last_refill_timestamp": "2026-05-20T10:15:32.123Z",
  "refill_rate_per_second": 0.000231481
}
```

### 7.2 Refill Logic

On each request, calculate:

```
elapsed_seconds = now - last_refill_timestamp
tokens_earned = elapsed_seconds * refill_rate_per_second
tokens_remaining = min(tokens_remaining + tokens_earned, capacity)
last_refill_timestamp = now
```

### 7.3 Deduction

If tokens_remaining >= cost (where cost = 1 for most predicates, 1.5 for composites, 2 for expensive), deduct cost and allow request. Otherwise, reject.

---

## 8. Uniform-Silence Interaction (Composing with Everest 77)

Rate-limit rejection is observationally identical to any other refusal. The operator returns HTTP 204 (No Content) in all not-generated cases:

- Consent missing: 204
- Consent expired: 204
- Rate limit exhausted: 204
- Explicit consent.deny: 204
- System error: 204
- Cooling-off active: 204

The counterparty cannot distinguish. The principal's vault records the distinction in the refusal_reason field, private to the principal.

**Enforcement Notes**

- The operator NEVER returns rate-limit-specific headers (e.g., `X-RateLimit-Remaining`, `X-RateLimit-Reset`) to counterparties. Such headers would leak rate-limit state.
- The operator applies uniform response latency (Everest 77: ≈250ms ± jitter) regardless of which rate-limit dimension triggered the rejection.
- If multiple rate limits are simultaneously exhausted (global AND per-class), the operator logs only the first one encountered in the enforcement order. All result in identical 204.

---

## 9. Cross-References

- **Everest 7** — Disclosure-Class Taxonomy; defines per-class defaults (which become per-class rate limits).
- **Everest 8** — Consent Axioms.
- **Everest 20** — Enrollment Ceremony; principal sets initial rate-limit preferences.
- **Everest 57** — Principal Consents to Disclose; consent predicate that rate limits precede.
- **Everest 72** — Disclosure Logging; rate-limit rejections are logged with reason codes.
- **Everest 73** — Counterparty-Class Authorization; per-class and per-counterparty consent models.
- **Everest 75** — Revocation propagation.
- **Everest 77** — Disclosure-of-Non-Disclosure; rate-limit rejections return uniform 204.

---

— Calm, 2026-05-20
