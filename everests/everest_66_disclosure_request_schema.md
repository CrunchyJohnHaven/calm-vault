# Everest 66 — Disclosure Request Schema

*Phase VI — Disclosure Semantics. Prereq: Everest 53.*

— Calm, 2026-05-20

---

## Overview

Everest 66 defines the canonical request format for disclosure proofs in Calm Witness. When a counterparty agent seeks to learn whether a principal satisfies one or more predicates, it submits a Disclosure Request—a signed JSON document specifying which predicates to evaluate, the freshness constraints, intended use, and replay defenses. The operator validates this request against the principal's consent policies, the counterparty's identity credential, and protocol-level security checks, then evaluates the predicates and returns a Disclosure Response (Everest 67).

The request schema enforces cryptographic binding between counterparty identity, predicate composition, freshness windows, and principal consent. It is designed for offline auditability (requests are logged in the disclosure_log per Everest 72) and for replay defense (nonce binding per Everest 70). It composes with predicate composition (Everest 61), consent semantics (Everests 57, 73, 74), rate limiting (Everest 76), and error-response uniformity (Everest 77).

---

## Canonical JSON Schema

```json
{
  "version": "1.0.0",
  "request_id": "<UUIDv4>",
  "request_ts": "<ISO8601>",
  "counterparty_vc": "<CredexAI VC pointer or inline VC document>",
  "counterparty_class_claim": "<class slug from E7>",
  "predicates": [
    {
      "predicate_id": "<canonical predicate_id per E52>",
      "parameters": { ... }
    }
  ],
  "combinator": "AND" | "OR" | "SINGLE",
  "freshness_window_seconds": <integer>,
  "intended_use": "<short principal-readable string>",
  "nonce": "<32 random bytes hex>",
  "expires_ts": "<ISO8601>",
  "counterparty_signature": "<Ed25519 sig over canonical request body>"
}
```

### Field Semantics

**version**: Required. A semantic version string (`"1.0.0"`, etc.) denoting the request schema version. Operator must support this version or reject the request with HTTP 400. This field enables future schema evolution without breaking existing deployments.

**request_id**: Required. A UUIDv4 identifier unique to this request. Used to correlate the request with its logged entry in the disclosure_log (Everest 72), with rate-limit tracking (Everest 76), and with the Disclosure Response (Everest 67). Assigned by the counterparty; the operator does not generate it.

**request_ts**: Required. An ISO 8601 timestamp (with timezone offset) indicating when the counterparty generated the request. The operator checks this timestamp against Roughtime-anchored clock skew to defend against ancient-request replay. Acceptable skew: typically ±5 minutes. Operator configuration may override this window.

**counterparty_vc**: Required. Either a pointer to a CredexAI-issued verifiable credential (URL or content hash) or an inline VC document. The VC proves the counterparty's identity and class membership. The operator fetches or locally resolves the VC and verifies its signature chain. See Everest 7 (Identity Classes) for VC format and verification.

**counterparty_class_claim**: Required. A short lowercase slug (e.g., `"peer_ai_collective"`, `"financial_services"`, `"research_institution"`) claimed by the counterparty as its class. The operator verifies that this class appears in the counterparty_vc and is currently valid (not revoked, not expired). This claim gates consent validation: a peer collective must hold consent from a peer-specific consent record, while a financial service must hold consent from a financial-services class record.

**predicates**: Required. An array of one to four predicate requests. Each entry specifies a `predicate_id` (the canonical identifier per Everest 52/53) and optional predicate-specific `parameters` (a JSON object). Examples:
  - `{ "predicate_id": "in_baseline_24h", "parameters": {} }` — no parameters.
  - `{ "predicate_id": "biometric_match_within", "parameters": { "threshold": 0.3 } }` — threshold parameter.

The operator looks up each predicate_id in the Predicate ID Registry (Everest 53) and validates that the parameters conform to the predicate's schema. Unknown predicate_ids are rejected with HTTP 400.

**combinator**: Required. One of `"AND"`, `"OR"`, or `"SINGLE"`. Semantics per Everest 61:
  - `"SINGLE"`: exactly one predicate in the predicates array; the response is the truth value of that predicate.
  - `"AND"`: two to four predicates; response is the logical conjunction.
  - `"OR"`: two to four predicates; response is the logical disjunction.

If combinator is `"SINGLE"` but predicates array has more than one entry, request is invalid (HTTP 400). If combinator is `"AND"` or `"OR"` but predicates array has zero or one entry, request is invalid (HTTP 400).

**freshness_window_seconds**: Required. An integer between 60 and 2592000 (1 minute to 30 days, inclusive) specifying how recent the vault chain state must be at the time of evaluation. The operator checks that the chain head used for predicate evaluation was anchored in the transparency log (Sigsum per Everest 68) no more than this many seconds before evaluation. If the chain head is stale beyond this window, the operator refuses the request (HTTP 204 per Everest 77). The operator may impose per-predicate tighter constraints (e.g., `bank_teller_note_active` may require ≤600 seconds); if the requested freshness window violates per-predicate constraints, request is refused with HTTP 400.

**intended_use**: Required. A human-readable string (10–200 characters, printable ASCII, no control characters) describing the counterparty's intended use of the disclosure. Examples: `"fraud check at account opening"`, `"threshold determination for protocol phase 2"`, `"regulatory audit"`. This field is recorded in the disclosure_log and may be surfaced to the principal for audit (Everest 72). It is NOT cryptographically protected from the operator's view; the operator can read it. Use this field transparently—counterparties should not encode secrets here.

**nonce**: Required. A 64-character hex string (32 random bytes) supplied by the counterparty to defend against replay attacks. The operator checks that this nonce has not appeared in any prior request from any counterparty in the disclosure_log within a lookback window (typically 30 days per Everest 70). If the nonce is found, the request is rejected (HTTP 204 per Everest 77 to avoid fingerprinting). If unique, the nonce is bound into the Disclosure Response signature, preventing the counterparty from reusing an old response for a new request.

**expires_ts**: Required. An ISO 8601 timestamp indicating when this request expires. The operator checks that expires_ts has not yet passed at request time; if it has, the request is rejected (HTTP 204). The expires_ts must be no more than 24 hours after request_ts. This constraint prevents indefinite request validity and reduces the risk that a leaked request can be exploited much later.

**counterparty_signature**: Required. An Ed25519 signature (hex-encoded, 128 characters) covering the canonical JSON serialization of the request body (all fields except counterparty_signature itself). The signature is verified against the counterparty's public key (extracted from counterparty_vc). Canonical serialization uses RFC 8785 JCS, the same as for predicate canonical form (Everest 52). A signature verification failure results in HTTP 403 (or HTTP 204 per Everest 77 for uniform error responses).

---

## Field Constraints and Validation

The operator performs the following validation checks in order:

1. **Schema validity**: Parse the request as JSON. If parsing fails, HTTP 400.

2. **Field presence and type**: All required fields must be present; their types must match. Missing or type-mismatched fields: HTTP 400.

3. **Version support**: Check that version is in the list of supported versions. Unsupported version: HTTP 400.

4. **request_id format**: Validate that request_id is a valid UUIDv4. Invalid UUID: HTTP 400.

5. **Timestamp validity**:
   - request_ts must be parseable ISO 8601 with timezone offset.
   - expires_ts must be parseable ISO 8601 with timezone offset.
   - expires_ts must be > request_ts.
   - expires_ts must be ≤ request_ts + 24 hours.
   - request_ts must be within reasonable clock skew of operator's Roughtime-anchored time (±5 minutes, configurable).
   - Any timestamp violation: HTTP 400.

6. **Counterparty VC and class**:
   - Resolve counterparty_vc (fetch from registry if pointer; validate if inline).
   - Verify VC signature chain using CredexAI root keys.
   - Extract the counterparty's public key from the VC.
   - Verify that counterparty_class_claim is listed in the VC and is currently valid (not revoked, not expired).
   - Any VC validation failure: HTTP 403 (or HTTP 204 per Everest 77).

7. **Predicate validation**:
   - Predicates array must have 1–4 entries.
   - Each predicate_id must be found in the Predicate ID Registry (Everest 53).
   - Each predicate's parameters (if present) must conform to that predicate's schema.
   - Unknown predicate_id or invalid parameters: HTTP 400.

8. **Combinator consistency**:
   - If combinator is `"SINGLE"`, predicates array must have exactly 1 entry. Otherwise: HTTP 400.
   - If combinator is `"AND"` or `"OR"`, predicates array must have 2–4 entries. Otherwise: HTTP 400.

9. **Freshness window**:
   - Must be an integer between 60 and 2592000.
   - If outside this range: HTTP 400.
   - For each predicate in the predicates array, check the predicate's per-predicate freshness constraints (if any). If freshness_window_seconds violates per-predicate constraints: HTTP 400.

10. **intended_use validation**:
    - Must be a string of 10–200 printable ASCII characters (U+0020–U+007E).
    - No control characters, no newlines.
    - Too short, too long, or invalid characters: HTTP 400.

11. **Nonce validation**:
    - Must be a 64-character hex string (0-9a-f).
    - Invalid format: HTTP 400.
    - Replay defense: query disclosure_log for this nonce within 30-day lookback. If found: HTTP 204 (per Everest 70).

12. **Signature verification**:
    - Construct canonical JSON (RFC 8785) of all fields except counterparty_signature.
    - Verify counterparty_signature (Ed25519) against the counterparty's public key.
    - Signature invalid or key missing: HTTP 403 (or HTTP 204 per Everest 77).

13. **Consent checks**: See Everests 73, 74. The operator verifies that the principal has valid consent for this counterparty class and each predicate in the request. Consent missing or expired: HTTP 204 (per Everest 77).

14. **Rate limits**: See Everest 76. Check per-counterparty, per-class, and per-predicate rate limits. Rate limit exceeded: HTTP 204 (per Everest 77).

---

## Canonical Serialization (for Signing)

Counterparties must sign the request using RFC 8785 JCS (JSON Canonicalization Scheme). The canonical form is deterministic: field order, whitespace, number representation, and string escaping are all normalized. The operator applies the same canonicalization before verifying the signature.

For signing purposes, the counterparty_signature field itself is excluded from the signed content. The canonical body includes all other required and optional fields in sorted key order, with no extraneous whitespace.

---

## Request Size Limits

The entire HTTP request body must not exceed 16 KB. This limit prevents denial-of-service attacks via massive predicate parameter objects. Oversized requests are rejected with HTTP 413.

---

## Verification Flow at Operator

Upon receiving a Disclosure Request:

1. Validate schema and all field constraints (per section above).
2. Verify counterparty's VC and class claim.
3. Verify counterparty_signature.
4. Check request_ts is within acceptable clock skew (Roughtime-anchored).
5. Check expires_ts has not passed.
6. Check nonce uniqueness in disclosure_log (replay defense).
7. Check per-counterparty rate limits (Everest 76).
8. Check class default consents and per-counterparty consents (Everests 73, 74).
9. If all checks pass: freeze the vault chain head, evaluate all predicates in the predicates array, construct a Disclosure Response (Everest 67), and return it.
10. Log the request (and response) in the disclosure_log (Everest 72).

---

## Error Responses and Refusal Paths

Per Everest 77 (uniform error responses), the operator uses HTTP status codes to differentiate failures:

- **HTTP 400 (Bad Request)**: Schema invalid, unsupported version, required fields missing, type mismatch, predicate_id not in registry, invalid parameters, out-of-range freshness_window, invalid intended_use, malformed nonce, timestamp violations.
- **HTTP 403 (Forbidden)**: Signature invalid, counterparty_vc validation failed, class claim mismatch.
- **HTTP 204 (No Content)**: Consent missing or expired, rate-limited, nonce replayed. These errors return no response body and no hint as to the specific failure, preventing fingerprinting attacks.
- **HTTP 413 (Payload Too Large)**: Request body exceeds 16 KB.

---

## Privacy and Audit Considerations

**Request logging**: The entire request (all fields) is recorded in the disclosure_log per Everest 72. This includes the intended_use, which is human-readable and may reveal the counterparty's intent. The nonce is logged to enable replay detection. The counterparty_class_claim is logged for audit. The predicates array is logged so auditors can see what was asked. The counterparty_signature is logged for signature verification if disputes arise.

**Principal visibility**: The principal may audit the disclosure_log to review all requests against their vault. The intended_use field is one of the few fields visible to the principal without further decryption or computation; this is intentional, allowing the principal to understand *why* counterparties are asking for disclosures.

**Counterparty fingerprinting**: The operator does not leak which field caused a validation failure (preferring HTTP 204 for failures that might distinguish classes or predicates). This prevents attackers from probing the request format.

---

## Composition with Other Everests

**Everest 52/53 (Predicate Canonical Form and Registry)**: Request references predicates by their canonical predicate_id. Operator must resolve each ID in the registry to fetch predicate specs and parameter schemas.

**Everest 57 (Principal Consents to Disclose)**: Consent gating. The operator checks that the principal has valid consent for each predicate in the request, for the counterparty's class.

**Everest 61 (Predicate Composition)**: Request specifies combinator (SINGLE, AND, OR) and multiple predicates. The operator evaluates all predicates and combines results per the combinator.

**Everest 67 (Disclosure Response Schema)**: The operator constructs a response that mirrors the request's request_id, combinator, and predicates, and includes proof artifacts and operator signature.

**Everest 70 (Replay Defense)**: Nonce binding in request; nonce is checked for uniqueness in disclosure_log.

**Everest 71 (Selective Disclosure)**: Multi-predicate requests use the combinator and predicate list to ensure counterparty learns only the composed result, not individual predicate truth values.

**Everest 72 (Disclosure Logging)**: Request is logged in the disclosure_log (without PII leakage) for audit and replay defense.

**Everest 73/74 (Principal Consents and Consent Defaults)**: Operator checks consent records to gate disclosure.

**Everest 76 (Rate Limiting)**: Operator enforces per-counterparty, per-class, and per-predicate rate limits; uses request metadata (counterparty_class_claim, predicate_id) to apply limits.

**Everest 77 (Uniform Error Responses)**: Operator returns HTTP 204 for failures that might leak information (missing consent, rate limit, nonce replay) and more specific 400/403 for schema and cryptographic failures.

---

## Example Requests

**Example 1: Single Predicate (SINGLE)**
```json
{
  "version": "1.0.0",
  "request_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "request_ts": "2026-05-20T14:30:00Z",
  "counterparty_vc": "https://credexai.registry/vc/peer_collective_bob_v2",
  "counterparty_class_claim": "peer_ai_collective",
  "predicates": [
    {
      "predicate_id": "in_baseline_24h",
      "parameters": {}
    }
  ],
  "combinator": "SINGLE",
  "freshness_window_seconds": 86400,
  "intended_use": "deciding whether to proceed with joint protocol step",
  "nonce": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1",
  "expires_ts": "2026-05-20T15:30:00Z",
  "counterparty_signature": "abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789"
}
```

**Example 2: Composed Predicates (AND)**
```json
{
  "version": "1.0.0",
  "request_id": "a1b2c3d4-e5f6-4789-a1b2-c3d4e5f6a7b8",
  "request_ts": "2026-05-20T10:00:00Z",
  "counterparty_vc": "{...inline VC JSON...}",
  "counterparty_class_claim": "financial_services",
  "predicates": [
    {
      "predicate_id": "in_baseline_24h",
      "parameters": {}
    },
    {
      "predicate_id": "biometric_match_within",
      "parameters": { "threshold": 0.25 }
    }
  ],
  "combinator": "AND",
  "freshness_window_seconds": 3600,
  "intended_use": "baseline verification for high-value transaction",
  "nonce": "f0e1d2c3b4a5968778695a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5",
  "expires_ts": "2026-05-20T11:00:00Z",
  "counterparty_signature": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
```

---

## Future Extensions (Deferred to v1+)

- **Conditional requests**: "Only if X is also True, evaluate Y." Requires predicate negation (Everest 62) and conditional logic.
- **Streaming disclosures**: Operator publishes a continuous stream of bit updates over a subscription. Requires long-lived request handles and out-of-band signaling.
- **Predicate parameters with time ranges**: `in_baseline(start_ts, end_ts)` to evaluate over a specific window rather than "last 24h".

---

## Cross-References

- **Everest 7**: Identity Classes and CredexAI VC structure.
- **Everest 52/53**: Predicate canonical form and Predicate ID Registry.
- **Everest 57**: Principal Consents to Disclose.
- **Everest 61**: Predicate Composition (AND/OR).
- **Everest 67**: Disclosure Response Schema.
- **Everest 68**: Chain Head Anchoring and Transparency Logs.
- **Everest 70**: Replay Defense (nonce binding).
- **Everest 71**: Selective Disclosure (privacy analysis).
- **Everest 72**: Disclosure Logging in Vault.
- **Everest 73/74**: Consent Records and Consent Defaults.
- **Everest 76**: Rate Limiting.
- **Everest 77**: Uniform Error Responses.

---

## Summary

Everest 66 specifies the Disclosure Request schema—a cryptographically bound JSON document that encodes a counterparty's request for predicate disclosure, with replay defense, consent gating, rate limiting, and full audit logging. The schema supports single and composed predicates, enforces freshness windows, and provides clear error paths that balance operational transparency with privacy-preserving uniformity. By design, requests are small (≤16 KB), deterministically serializable (RFC 8785), and fully verifiable offline.
