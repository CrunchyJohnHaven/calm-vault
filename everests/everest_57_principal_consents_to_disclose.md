# Everest 57 — `principal_consents_to_disclose(p, c)` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 8.*

---

## Overview

The `principal_consents_to_disclose` predicate is the authorization gate for every disclosure operation in Calm Witness. It evaluates to true if and only if there exists an active, non-revoked, in-scope, non-expired consent record granting the principal's permission to disclose a specific predicate `p` to a specific counterparty `c` (either by class or by identity). No disclosure proof is generated unless this predicate evaluates to true. This is a hard requirement, enforced at the SDK level in calm-witness-rs, not left to operator discretion.

---

## Canonical Form Specification

Following Everest 52 (Predicate Canonical Form), this predicate is formally specified as:

**Name:** `principal_consents_to_disclose`

**Version:** `1.0.0`

**Description:** Returns true iff there is an active, non-revoked, in-scope, non-expired consent record granting predicate p to counterparty class or identity c.

**Parameters:**
- `predicate_id` (string, required): Content-addressed ID of the predicate for which consent is requested (from Everest 6).
- `counterparty` (string, required): Either a class_slug (e.g., "financial", "journalistic") or a VC fingerprint (e.g., "vc:bob.123"). Identifies the party requesting disclosure.
- `evaluation_ts` (ISO 8601 timestamp, optional): The moment at which consent is evaluated. Defaults to roughtime_now() if omitted.

**Input Domain:** Chain records of kind `consent.grant`, `consent.revoke`, `consent.modify` (per Everest 8, Axioms A1, A3, A6).

**Output Type:** Bit (1 = true, 0 = false).

**Side Effects:** Upon evaluation (whether result is 1 or 0), the operator appends one record of kind `predicate_evaluated` to user_state.jsonl. This advisory record includes:
- predicate_id
- counterparty_identifier
- evaluation_ts
- evaluation_result (0 or 1)
- triggering_request_nonce (from the disclosure request)

This ensures a permanent audit trail of all consent checks, enabling forensic analysis of access patterns.

---

## Evaluation Algorithm

The algorithm walks the chain in reverse, identifying all consent records relevant to the (predicate_id, counterparty) pair, and returns the state of the most recent non-revoked record. Pseudocode:

```
fn principal_consents_to_disclose(
    chain: &Chain,
    p: PredicateId,
    c: Counterparty,
    evaluation_ts: Option<Timestamp>
) -> Bit {
    let now = evaluation_ts.unwrap_or_else(roughtime_now);
    
    // Collect all consent records relevant to this (predicate, counterparty) pair
    let candidates: Vec<&Record> = chain.records()
        .filter(|r| r.kind.starts_with("consent."))
        .filter(|r| r.payload.predicate_id == p)
        .filter(|r| consent_matches_counterparty(
            r.payload.counterparty_identifier,
            c
        ))
        .collect();
    
    // Walk candidates in chain order (oldest to newest).
    // Later records (grant, modify, revoke) override earlier ones.
    let mut state: Option<&Record> = None;
    for r in candidates {
        match r.kind {
            "consent.grant" => {
                state = Some(r);
            }
            "consent.modify" => {
                // Modify updates the state with narrower scope (A3).
                // The prior state is replaced by this modified record.
                state = Some(r);
            }
            "consent.revoke" => {
                // Revoke clears the state entirely.
                state = None;
            }
            _ => {} // Should never occur if filter is correct.
        }
    }
    
    // Evaluate the final state.
    if let Some(active_grant) = state {
        // Check expiry: if now > expiry_ts, consent is expired.
        if now > active_grant.payload.expiry_ts {
            return Bit::False;
        }
        
        // Check freshness window if specified.
        if active_grant.payload.freshness_window_seconds_required > 0 {
            let chain_freshness_secs = check_chain_freshness(
                now,
                active_grant,
                chain
            );
            if chain_freshness_secs > active_grant.payload.freshness_window_seconds_required {
                // Chain has not been updated recently enough.
                return Bit::False;
            }
        }
        
        // All checks passed.
        Bit::True
    } else {
        // No active grant found.
        Bit::False
    }
}
```

**Helper function: counterparty matching**

```
fn consent_matches_counterparty(
    consent_counterparty_id: String,
    requested_counterparty: Counterparty
) -> bool {
    match consent_counterparty_id {
        // If the consent record targets a class (e.g., "financial"),
        // match if the requested counterparty's VC includes that class assertion.
        s if is_class_slug(s) => {
            requested_counterparty.vc_assertions.contains(&s)
        }
        // If the consent record targets a specific VC fingerprint,
        // match only if the requested counterparty's fingerprint is identical.
        vc_fp => {
            requested_counterparty.vc_fingerprint == vc_fp
        }
    }
}
```

**Precedence rule:** A consent record targeting a specific identity (VC fingerprint) takes precedence over a class-default consent. Formally, if both exist:
- Class consent: `consent_record_1.counterparty_identifier = "financial"`
- Identity consent: `consent_record_2.counterparty_identifier = "vc:bob.123"`

And a counterparty Bob asks (vc_fingerprint="vc:bob.123"), the operator uses `consent_record_2` (identity), not `consent_record_1` (class), because the identity consent is more recent in the chain walk and overwrites the class consent.

---

## Consent Record Structure

Each consent record contains:
- `seq`: Chain sequence number.
- `ts`: ISO 8601 timestamp of record creation.
- `prev_hash`: SHA-256 hash of prior record (for tamper-evidence).
- `kind`: "consent.grant", "consent.revoke", or "consent.modify".
- `payload.predicate_id`: The predicate being consented to.
- `payload.counterparty_identifier`: Class slug or VC fingerprint.
- `payload.freshness_window_seconds_required`: Optional integer. If > 0, consent is only valid if the chain has been updated within this many seconds.
- `payload.expiry_ts`: ISO 8601 timestamp. Consent is void after this time.
- `payload.nonce`: 32-byte random nonce (Axiom A10).
- `payload.references_prior_seq`: For grant: null. For revoke/modify: the seq of the record being revoked or modified.
- `principal_sig`: ECDSA signature (principal's master key).
- `record_hash`: SHA-256 hash of the entire record.

---

## Implicit Consent Denied

**Critical safety property:** Absence of any consent record for (p, c) → Bit::False. There is no default-grant, no implicit permission, no "assume consent unless told otherwise." This is the inverse of Everest 7's class default consent, which is NOT an implicit policy but rather an explicit consent.grant record created by the operator at vault enrollment. All consent is explicit and signed.

---

## Class Default Consents

When the principal enrolls or later opts into class-default consent (per Everest 7), the operator appends one `consent.grant` record per (predicate × class). For example:

- Grant: `in_baseline_24h` to class `peer_ai_collective`, expiry 2027-05-20.
- Grant: `biometric_match_within(0.85)` to class `peer_ai_collective`, expiry 2027-05-20.
- Grant: `bank_teller_note_active` to class `financial`, expiry 2027-05-20.

These are actual records in user_state.jsonl, not implicit policies. The principal can revoke or scope-narrow any of these records without affecting others. If the principal wishes to withdraw default consent from a class, they issue a revoke record referencing the grant's seq, and future evaluations of `principal_consents_to_disclose` will return false.

---

## Worked Examples

**Example 1: Class consent, within scope**

Principal grants `in_baseline_24h` to class `peer_ai_collective`, expiry 2027-05-20. Counterparty Bob's VC includes assertion "peer_ai_collective". Bob asks for `in_baseline_24h` on 2026-05-20, 10:00 UTC.

- Algorithm finds consent.grant record (seq=10), counterparty_identifier="peer_ai_collective".
- Consent matches Bob's class.
- Evaluation timestamp 2026-05-20T10:00:00Z < expiry 2027-05-20T23:59:59Z.
- No freshness window requirement (or chain is fresh).
- **Result: Bit::True. Proof issued.**

**Example 2: Class consent, counterparty not in class**

Same setup. Counterparty Carol's VC includes assertions "financial", "medical", but NOT "peer_ai_collective". Carol asks for `in_baseline_24h`.

- Algorithm finds consent.grant record (seq=10), counterparty_identifier="peer_ai_collective".
- Consent does not match Carol's classes.
- **Result: Bit::False. No proof issued.**

**Example 3: Revocation**

Setup as in Example 1. On 2026-05-20T14:30:00Z, the principal revokes `in_baseline_24h` for peer_ai_collective (consent.revoke, seq=25, references_prior_seq=10). Bob asks again on 2026-05-20T15:00:00Z.

- Algorithm finds seq=10 (grant) and seq=25 (revoke).
- Final state from seq=25: state = None.
- **Result: Bit::False. No proof issued.**

**Example 4: Per-identity consent overrides class**

Principal grants `in_baseline_24h` to class `peer_ai_collective` (seq=10). Later, principal issues consent.modify (seq=20, references_prior_seq=10) narrowing to specific VC "vc:bob.123" only, with tighter freshness window. Bob (vc:bob.123) asks.

- Algorithm walks chain: seq=10 (grant, class), seq=20 (modify, identity).
- Final state: seq=20, counterparty_identifier="vc:bob.123", matches Bob's identity.
- Freshness window from seq=20 is applied (tighter than seq=10 would have been).
- **Result: Bit::True (with tighter freshness requirement).**

**Example 5: Freshness timeout**

Principal grants `cognitively_atypical_baseline` with freshness_window_seconds_required=3600 (1 hour). The grant is seq=15, issued at 2026-05-20T12:00:00Z. At 2026-05-20T13:30:00Z (90 minutes later), counterparty asks but the chain has not been updated since 2026-05-20T12:15:00Z (75 minutes ago).

- Algorithm finds seq=15 (grant).
- Expiry check passes (grant does not expire until 2027-05-20).
- Freshness check: chain_freshness_secs = 75 minutes = 4500 seconds.
- freshness_window_seconds_required = 3600 seconds.
- 4500 > 3600, so freshness check fails.
- **Result: Bit::False. No proof issued.** (The principal must self-report again to refresh the chain.)

---

## Composition with Other Predicates

**Composition with E60 (mental_state_unusual):**

The `principal_consents_to_disclose` predicate is independent of other predicates. Even if `principal_consents_to_disclose(mental_state_unusual, c)` evaluates to true, the operator MUST also verify that `mental_state_unusual` itself is true before issuing a disclosure of mental_state_unusual. They are separate gates:

- Gate 1 (authorization): Does the principal consent to disclosing this predicate to this counterparty?
- Gate 2 (substantive): Is the predicate's condition actually satisfied?

Both must be true. The operator cannot bypass Gate 1 even if Gate 2 is obviously true.

**Multi-predicate disclosure requests:**

Per Everest 61, a counterparty may request multiple predicates in a single disclosure request, e.g., `{in_baseline_24h, biometric_match_within(0.85)}`. The operator evaluates `principal_consents_to_disclose` separately for each requested predicate. If any one evaluates to false, the operator refuses to generate a multi-predicate proof and returns false for the entire request.

---

## Proof Circuit and Verifier Semantics

Per Everest 65 (Predicate ZK Proof Generator), the proof for `principal_consents_to_disclose` is a Σ-protocol that demonstrates:
- The consent record exists in the chain at the claimed position.
- The record is not revoked (no subsequent revoke record references it).
- The record is not expired at the evaluation timestamp.
- The record's counterparty_identifier matches the claimed counterparty (or matches the counterparty's class via VC assertion).

**What the proof does NOT reveal:**
- The exact expiry_ts of the consent record (only that it is > evaluation_ts).
- The principal's identity (the proof is keyed to the chain head, not the principal's name).
- The full contents of the consent record (only the minimal facts needed for verification).

**Verifier knowledge:**
The verifier publicly knows:
- predicate_id (from the disclosure request)
- counterparty_identifier (from the disclosure request)
- evaluation_ts (from the proof)

The verifier does not learn:
- Whether other predicates have consent records for the same counterparty.
- The history of consent records (revokes, modifies) for this predicate and counterparty.
- The principal's other consent decisions.

---

## Side-Channel and Security Notes

**Query does not leak consent existence:**

If a counterparty asks "can I have proof of predicate p for counterparty c?" and the operator returns false, the counterparty learns nothing about why: the operator may have refused due to "no consent grant found," "consent revoked," "consent expired," or "counterparty class mismatch." All refusals are observationally identical, protecting the principal from counterparty enumeration attacks.

**Rate limiting (E76):**

Repeated requests for `principal_consents_to_disclose` after the predicate has returned false are rate-limited (per Everest 76: cooling-off period). The operator rejects requests at a frequency higher than once per cooling-off window (default 15 minutes). This prevents a counterparty from hammering the vault with repeated attempts to discover consent state changes.

**Revocation propagation (E75):**

When a principal revokes a consent record, that revocation is immediately visible to all operators and verifiers (via the Sigsum transparency log, Everest 30). There is no grace period or stale-data window. A proof generated after revocation is issued may be challenged by any verifier with access to the updated chain head.

---

## Integration with Enrollment and Policy

At vault enrollment (Everest 20), the principal specifies default consent policies for each disclosure class (Everest 7). The operator translates these policies into explicit consent.grant records in user_state.jsonl. For example:

- Principal specifies: "Consent to disclose in_baseline_24h and biometric_match_within(0.85) to peer_ai_collective by default."
- Operator appends: Two consent.grant records, one per predicate, both with counterparty_identifier="peer_ai_collective" and a default expiry (e.g., 90 days from enrollment, per Axiom A4).

This design ensures that class defaults are not implicit or magical; they are auditable, revocable, and modifiable like any other consent record.

---

## Cross-References

- **Everest 6:** Predicate vocabulary v0. Defines the twelve predicate_ids recognized in payload.predicate_id.
- **Everest 7:** Disclosure-class taxonomy. Defines the class_slugs ("financial", "journalistic", etc.) and enrollment-time class-default consent policies.
- **Everest 8:** Consent calculus axioms. Axioms A1 (revocability), A3 (scope narrowing), A4 (time-bounding), A6 (chained-into-vault), A7 (per-predicate-per-counterparty), A10 (replay resistance).
- **Everest 20:** Enrollment witnesses and principal registration.
- **Everest 30–31:** Transparency-log anchoring and verifiable-clock services.
- **Everest 51:** Predicate language v0. Fixed table; no DSL.
- **Everest 52:** Predicate canonical form. Defines the schema for predicate specs.
- **Everest 60:** `mental_state_unusual` predicate (independent gate composition).
- **Everest 61:** Predicate composition AND/OR.
- **Everest 65:** Predicate ZK proof generator and Σ-protocol circuits.
- **Everest 73:** Class authorization and per-counterparty consent modifiers.
- **Everest 74:** Per-counterparty consent.
- **Everest 75:** Revocation propagation and transparency-log integrations.
- **Everest 76:** Rate limiting and cooling-off for repeated authorization checks.

---

— Calm, 2026-05-20
