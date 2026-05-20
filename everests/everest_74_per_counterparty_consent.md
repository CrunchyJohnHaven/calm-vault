# Everest 74 — Per-Counterparty Consent

*Phase VI — Disclosure Semantics. Prereq: Everest 73.*

## Overview

A principal's consent decision need not be monolithic. While class-default consents (Everest 73) establish baseline authorization for entire counterparty classes, real relationships are granular. A principal may trust a specific journalist while distrusting the journalist class as a whole, or conversely, may grant broad access to peer networks except for one peer with whom trust has fractured. Per-counterparty consent records enable principals to override class defaults on a per-VC basis, providing the nuance required for sustainable disclosure governance.

Per-counterparty consents inherit the same cryptographic foundations as class-default consents (Everest 8, Everest 57) while introducing a precedence rule: a specific counterparty record always takes priority over the corresponding class-default record. The system applies a two-tier matcher that first checks for per-counterparty consent, then falls back to class-default consent, with a final implicit deny if neither applies.

## Semantics and Precedence

### Core Principle

Per-counterparty consent records target a specific counterparty identified by the SHA-256 fingerprint of their CredexAI VC public key. When a counterparty requests disclosure of a predicate, the evaluation engine walks the consent chain and applies a strict precedence rule:

1. **Per-counterparty match (priority 1):** If the consent record's `counterparty_identifier` matches the requesting counterparty's VC fingerprint exactly, that record takes absolute priority.
2. **Per-class match (priority 2):** If no per-counterparty match exists, the engine falls back to class-default records where `counterparty_identifier` is a class slug (e.g., `journalist`, `peer_ai_collective`) and the requesting counterparty's VC asserts membership in that class.
3. **Implicit deny:** If neither match succeeds, the engine returns false (disclosure denied).

The most-recent per-counterparty record (by chain position, per Everest 8's reverse-chain walk) overrides any class-default record. This ensures that a principal's specific decision always supersedes the aggregate decision.

### Override Semantics

A per-counterparty ALLOW can override a class-default DENY. Similarly, a per-counterparty DENY can override a class-default ALLOW. The direction of override is irrelevant; what matters is that the specific record, if present and active, always controls the outcome for that counterparty.

## Use Cases

### Case 1: Trust Exception Within a Distrusted Class

A principal's class-default policy DENYs the `journalist` class (perhaps due to concerns about breach exposure or misrepresentation). However, the principal has a long-standing relationship with Karen Hao, a trusted investigative reporter, and wishes to permit her to access certain predicates.

Solution: Create a per-counterparty ALLOW record targeting Karen Hao's VC fingerprint. The record specifies the predicate (e.g., `email_address`, `location_history`), an expiry timestamp, and an optional freshness window. When Karen Hao requests access, her per-counterparty ALLOW overrides the class-default DENY. Other journalists receive the DENY.

### Case 2: Distrust Within a Trusted Class

A principal grants broad access to the `peer_ai_collective` class by default (class-default ALLOW for collaborative predicates like `model_weights_delta`). Recently, the principal had a falling-out with one peer, Bob, and wishes to revoke his access while maintaining trust with the rest of the collective.

Solution: Create a per-counterparty DENY record targeting Bob's VC fingerprint for the affected predicate. Bob's DENY overrides the class-default ALLOW. Other peers in the collective continue to receive the ALLOW.

### Case 3: Narrower Scope for a Specific Counterparty

A principal permits the `vendor` class to access `transaction_metadata` with a standard freshness window of 24 hours. However, for a specific vendor with higher security posture, the principal wishes to grant access with a tighter freshness window of 12 hours (more recent data only, reducing replay-attack surface).

Solution: Create a per-counterparty record for that vendor specifying the same predicate but a narrower `freshness_window_seconds` (43200 seconds instead of 86400). The per-counterparty record takes precedence, narrowing the scope while maintaining the ALLOW decision.

## Record Schema

Per-counterparty consent records share the schema defined in Everest 8, with the critical distinction that `counterparty_identifier` contains a specific VC fingerprint rather than a class slug:

```
kind: "consent.grant" | "consent.modify" | "consent.revoke"
payload: {
  counterparty_identifier: <SHA-256 of counterparty VC public key bytes>,
  predicate_id: <predicate identifier per Everest 52>,
  scope_parameters: <predicate-specific parameters>,
  freshness_window_seconds: <optional override, integer>,
  expiry_ts: <required Unix timestamp>,
  nonce: <unique value per Everest 8 A10>
}
```

The `counterparty_identifier` must be the full SHA-256 fingerprint (64 hexadecimal characters). The system does not compress or truncate this value; the fingerprint serves as an unforgeable commitment to the specific counterparty's VC.

## Evaluation Algorithm

The consent evaluation engine extends the Everest 57 algorithm with a two-tier matcher:

```
fn principal_consents_to_disclose(chain, p, counterparty_vc) -> Bit {
    let counterparty_class = extract_class_from_vc(counterparty_vc);
    let counterparty_fingerprint = sha256(counterparty_vc.public_key);
    
    // First check: per-counterparty (priority 1)
    if let Some(record) = find_most_recent_consent_record(
        chain, p, counterparty_identifier=counterparty_fingerprint
    ) {
        return evaluate_active_grant(record);
    }
    
    // Second check: per-class (priority 2)
    if let Some(record) = find_most_recent_consent_record(
        chain, p, counterparty_identifier=counterparty_class
    ) {
        return evaluate_active_grant(record);
    }
    
    Bit::False  // implicit deny
}
```

The `find_most_recent_consent_record` function applies the standard Everest 8 chain walk: records are examined in reverse chronological order (most recent first), and the first matching record controls the result. The `evaluate_active_grant` function checks the record's `kind` (grant, modify, revoke), verifies the nonce has not been replayed, and confirms that the current time is within the record's `expiry_ts` window.

## Worked Examples

**Example 1: Class Default, No Per-Counterparty Override**

Class-default policy grants `peer_ai_collective` ALLOW for predicate `in_baseline_24h`. Peer Bob requests access. No per-counterparty record exists for Bob. The engine finds the class-default record, evaluates it as active, and returns ALLOW. Bob receives the data.

**Example 2: Per-Counterparty DENY Overrides Class ALLOW**

Class-default policy grants `peer_ai_collective` ALLOW for `model_weights_delta`. Principal adds a per-counterparty DENY record for Bob's VC fingerprint targeting the same predicate. Bob requests access. The engine first checks for a per-counterparty match (priority 1), finds the DENY record, and returns DENY immediately without consulting the class default. Bob is denied.

**Example 3: Per-Counterparty ALLOW Overrides Class DENY**

Class-default policy denies `journalist` DENY for `email_address`. Principal adds a per-counterparty ALLOW record for Karen Hao's VC fingerprint targeting `email_address`. Karen requests access. The engine finds the per-counterparty ALLOW record (priority 1), evaluates it, and returns ALLOW. Karen receives the email address; other journalists receive DENY.

**Example 4: Expired Per-Counterparty Record Falls Back to Class Default**

Class-default policy denies `journalist` DENY for `location_history`. Principal previously added a per-counterparty ALLOW for Karen Hao with an expiry timestamp of 2026-05-19. Today is 2026-05-20. Karen requests access. The engine finds the per-counterparty record but discovers that `evaluate_active_grant` returns false (expired). The engine then checks the class default (priority 2), finds the DENY record, and returns DENY. Karen is denied because her per-counterparty exception has expired.

**Example 5: Per-Counterparty Record with Narrower Scope**

Class-default policy grants `vendor` ALLOW for `transaction_metadata` with `freshness_window_seconds=86400` (24 hours). Principal adds a per-counterparty record for vendor Alice's VC fingerprint targeting the same predicate with `freshness_window_seconds=43200` (12 hours). Alice requests access at time T with data from time T-6h. The engine finds Alice's per-counterparty record (priority 1), evaluates it, and returns ALLOW because T-6h is within the 12-hour window. If the same request arrived for a data point from T-18h, the per-counterparty record would return DENY (outside the narrower window), and no class-default fallback would apply because the per-counterparty record was found.

## Consent UI

The operator interface extends the Everest 8 commands with per-counterparty variants:

- **Grant per-counterparty consent:** `calm-witness consent grant <predicate_id> --counterparty <vc_fingerprint> --expiry <ts>`
- **Revoke per-counterparty consent:** `calm-witness consent revoke <predicate_id> --counterparty <vc_fingerprint>`
- **List per-counterparty records:** `calm-witness consent list --counterparty <vc_fingerprint>` displays all per-counterparty records (across all predicates) for the specified VC fingerprint.
- **Evaluate effective consent:** `calm-witness consent effective <predicate_id> <vc_fingerprint>` returns the decision (ALLOW or DENY) that would apply if that counterparty requested access right now, taking precedence and expiry into account.

## Revocation and Composition

When a principal revokes a per-counterparty consent record (via `consent.revoke`), the revocation record itself becomes part of the chain. Per Everest 8's chain walk, the revocation record is the most recent entry, so it takes priority and the disclosure is denied.

However, revocation only affects the specific counterparty. Other counterparties (whether under per-counterparty records or the class default) continue to operate under their respective consents. After revocation, if a per-counterparty record is revoked and no newer per-counterparty record exists, the class-default consent applies (priority 2). If no class default exists, the implicit deny prevails.

## Privacy Guarantees

Counterparties cannot cryptographically distinguish whether they are operating under a per-counterparty consent or a class-default consent. The principal's response (grant or deny) is identical in both cases. The counterparty only knows that the principal has authorized (or denied) access to a specific predicate; the counterparty does not learn the internal structure of the principal's consent tree.

Per Everest 77, refusals are also uniform: a denial due to per-counterparty DENY is indistinguishable from a denial due to class-default DENY or implicit deny. This silence prevents information leakage and ensures that counterparties cannot probe the principal's consent policies.

## Cross-References and Future Work

Per-counterparty consents interact with the broader disclosure ecosystem as follows:

- **Everest 7:** Predicate definition and scope.
- **Everest 8:** Consent chain, nonce, and expiry semantics.
- **Everest 52:** Predicate identifiers and scope parameters.
- **Everest 57:** Principal consent evaluation and the base precedence rule.
- **Everest 73:** Class-default consents (the fallback mechanism).
- **Everest 75:** Revocation propagation and cache invalidation.
- **Everest 76:** Rate limiting and token refresh (apply identically to per-counterparty grants).
- **Everest 77:** Uniform silence on refusal and privacy preservation.

Per-counterparty consent records are a foundational mechanism for principals to exercise fine-grained control over disclosure without sacrificing operational simplicity or privacy. They are essential to the Calm Witness protocol's commitment to principal sovereignty and counterparty transparency.

---

— Calm, 2026-05-20