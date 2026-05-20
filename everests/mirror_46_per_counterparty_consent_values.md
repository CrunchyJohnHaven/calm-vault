# Mirror Everest 46 — Per-Counterparty Consent for Values Disclosure

**Phase XII — Mirror Disclosure Semantics. Prereq: Mirror Everest 7, Witness Everest 8.**

---

## Statement of Purpose

Calm Witness consent (E8 axioms) operates at the predicate level: a principal grants or withholds consent for a single predicate to a single counterparty class or identity. Calm Mirror extends this to predicate-bit granularity. Because Mirror discloses value-bits — individual evidence evaluations like `non_harm_evidence = true` — consent must attach at that sub-predicate level. This Everest defines the consent calculus for values disclosure: per-predicate × per-counterparty × per-time-window consent grants, with explicit schemas for the four principal-protective defaults that dominate Calm Mirror's design.

---

## Extension of Witness E8 Axioms

The ten axioms from Witness Everest 8 remain normative and are inherited. This Everest adds three new axioms, A-V11 through A-V13, that extend the consent model specifically to value-bit disclosure.

### A-V11. Per-Predicate-Bit Consent Granularity

**Formal statement:** In Calm Mirror, consent is granted in a 3-tuple (value_predicate_id, counterparty_identifier, time_window) where:

- **value_predicate_id** ∈ {`unselfishness_evidence`, `tribal_neutrality_evidence`, `respect_for_difference_evidence`, `non_harm_evidence`, `growth_arc_evidence`, `truth_telling_evidence`, `apology_when_wrong_evidence`, ...} (from Mirror Everest 5)
- **counterparty_identifier** is either (a) a class slug from the Mirror Everest 7 taxonomy (peer_ai_collective, employer, partner, journalist, ideologue, anonymous, etc.), or (b) a specific counterparty VC fingerprint (for per-identity consent)
- **time_window** is an ISO 8601 duration (e.g., `P30D` for 30 days, `PT1H` for 1 hour) specifying the temporal scope of the evidence window the counterparty may access.

**Explanation:** A principal may consent to disclose `non_harm_evidence` to their employer for the past 90 days, while withholding `growth_arc_evidence` entirely and granting `unselfishness_evidence` to the peer-AI-collective for the past 2 years. Each value-bit × counterparty × window combination is a distinct consent grant, independently grantable, modifiable, and revocable. This prevents overly broad "all values to all counterparties" consent records and forces both principal and operator to be explicit about exactly which bits flow to whom.

---

### A-V12. Ideologue-Class Deny-Default

**Formal statement:** Counterparties classified as `ideologue` (per Mirror Everest 7: entities whose stated agenda is to filter or rank people by values) default to **explicit deny** for all value-bit disclosures. No value-bit shall be disclosed to an ideologue counterparty unless the principal has issued a specific, per-identity consent record referencing the counterparty's VC fingerprint (not the class slug). Class-level consent grants to `ideologue` are invalid and shall be rejected by Calm operators.

**Explanation:** Ideologues represent the principal-attack surface that Calm Mirror is designed to defend against: actors who collect values-evidence to blackball, rank, or filter people. The deny-default ensures that principals are never passively exposed to ideological vetting. A principal who trusts a specific ideologue (e.g., a particular journalist investigating corruption) must make that trust explicit and per-identity, creating an auditable record. This makes ideological weaponization visible and high-friction.

---

### A-V13. Growth-Bit Availability Mandate

**Formal statement:** If a principal grants consent to disclose `non_harm_evidence` to any counterparty, that same consent record MUST also extend consent to disclose `growth_arc_evidence` (Mirror Everest 31) to that counterparty, unless the principal explicitly opts into `growth_waive=true` in the consent payload. The operator shall reject consent.grant records that include `non_harm_evidence` and omit `growth_arc_evidence` without the waiver flag.

**Explanation:** Axiom A-V13 prevents permanent blackballing. A principal whose past contains evidence of harm is not locked into that history; growth is a first-class value. By mandating that non-harm disclosure is accompanied by growth-arc disclosure, the axiom ensures the counterparty sees the full context: not just "did this person harm others" but "has this person demonstrated visible change and sustained improvement since?" This avoids the trap of identity-collapse: a single value-bit does not define a person. A principal may opt out of growth-bit disclosure via the waiver flag, but that choice is explicit and chained.

---

## Consent Record Schema for Values (Extension of E8 Schema)

```json
{
  "seq": 127,
  "ts": "2026-05-20T14:30:00Z",
  "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "kind": "consent.grant",
  "payload": {
    "consent_version": "mirror.v0",
    "value_predicate_ids": [
      "non_harm_evidence",
      "growth_arc_evidence"
    ],
    "counterparty_identifier": "peer_ai_collective",
    "counterparty_identity_vc_fingerprint": null,
    "time_window_iso8601": "P2Y",
    "evidence_temporal_window": {
      "lookback_days": 730,
      "exclude_before_ts": null,
      "include_revisions_after_ts": "2024-05-20T00:00:00Z"
    },
    "scope_constraints": {
      "max_bit_precision": "ternary",
      "allow_alignment_composite": true,
      "withhold_witness_names": true,
      "withhold_counter_evidence_detail": false
    },
    "expiry_ts": "2027-05-20T23:59:59Z",
    "growth_waive": false,
    "nonce": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c",
    "references_prior_seq": null
  },
  "principal_sig": "3045022100e3b0c44298fc1c149afbf4c8996fb924270f90298c8f3f8a1c7c3e2d0f8b9a8d022100a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0",
  "record_hash": "b4d3f5a2e1c0d8b9f7e6c5a4b3d2e1f0a9c8b7a6d5e4f3a2b1c0d9e8f7"
}
```

**Schema explanation (additions beyond E8):**

- **consent_version:** Must be `"mirror.v0"` to signal this is a Calm Mirror values-disclosure consent record.
- **value_predicate_ids:** Array of value-bit identifiers being granted. Cannot be empty.
- **counterparty_identity_vc_fingerprint:** For per-identity consent (especially ideologue class): the content-addressed VC fingerprint. Null for class-level consent. If present, the operator shall not issue any disclosure to the named class; only the fingerprint is honored.
- **time_window_iso8601:** ISO 8601 duration string (e.g., `P30D`, `P2Y`) specifying the temporal scope. Operator computes the effective lookback from current time minus this duration.
- **evidence_temporal_window:** Explicit field for granular temporal control. Allows the principal to specify custom bounds (exclude_before_ts, include_revisions_after_ts) overriding the simple duration.
- **scope_constraints:** Controls precision and detail of disclosure. `max_bit_precision` ∈ {binary, ternary} — ternary allows `true`, `false`, `unknown`; binary collapses `unknown` to withhold. `withhold_witness_names`: if true, the disclosure omits the names/identities of co-signers on evidence records. `withhold_counter_evidence_detail`: if true, omits the substance of counter-evidence, retaining only the fact that counter-evidence exists.
- **growth_waive:** Boolean. If true, the principal explicitly declines the A-V13 mandate (growth-bit disclosure waived). Operator logs this as a principal-protective audit flag.

---

## Revocation Propagation Latency (T-M46.1)

**Specification:** When a principal revokes a values-consent record via `kind: consent.revoke`, the revocation is chained immediately (appended to user_state.jsonl, signed, hashed). However, active Mirror exchanges in flight may use the now-revoked consent record for up to 300 seconds after revocation is published. This window allows for safe quiescence of in-flight cryptographic operations. After 300 seconds, all operators shall treat the revocation as canonical and shall reject disclosure requests that reference the revoked consent record.

**Rationale:** Mirror exchanges involve multi-party computation and ZK proof generation, which can take tens to hundreds of seconds to complete. Immediate revocation could cause in-flight proofs to become invalid mid-computation, exposing principals to denial-of-service. The 300-second window allows in-flight operations to complete or abort cleanly. Operators monitoring the vault publish revocation notices to their connected peers within this window, ensuring that new disclosure requests respect the revocation immediately.

---

## Composition with Mirror E7, E34, E49, E51 (T-M46.2–T-M46.3)

- **E7 (Counterparty-Class Taxonomy):** Consent records reference counterparty classes or identities defined in E7. Ideologue-class enforcement is joint work: E7 defines the class; A-V12 enforces the deny-default; the operator applies both at consent-check time.
- **E34 (Growth-Bit Composition Rule):** A-V13 operationalizes E34 at the consent layer. E34 is normative policy ("any non-harm disclosure should include growth"); A-V13 is a mechanical enforcement point (the operator rejects ill-formed consent records).
- **E49 (Reciprocal Disclosure / Mirror Exchange):** In the two-party exchange, both principals' agents jointly verify consent records from both sides. If either principal lacks consent, the exchange aborts with `unknown` for the withheld bit.
- **E51 (Withhold-Any-Bit Guarantee):** A principal who declines to grant consent to a specific bit effectively withholds it. The other side learns "withheld" (not "true" or "false"). The Axiom A-V11 granularity ensures this withholding is per-bit, not all-or-nothing.

---

## Acceptance Criteria (T-M46.4–T-M46.5)

**T-M46.4: Consent Record Validation & Rejection**

Calm operators shall implement consent record validation that:
- Rejects `consent.grant` with `counterparty_identifier = "ideologue"` and no per-identity VC fingerprint.
- Rejects records with `non_harm_evidence` in `value_predicate_ids` but lacking `growth_arc_evidence`, unless `growth_waive = true`.
- Rejects records with `time_window_iso8601` that cannot be parsed as ISO 8601.
- Rejects records with empty `value_predicate_ids`.
- Validates all `value_predicate_ids` against the published Mirror Everest 5 vocabulary + any RFC-approved extensions (Mirror Everest 78).
- For per-identity consent, validates that `counterparty_identity_vc_fingerprint` matches a known CredexAI VC.

**T-M46.5: Disclosure Authorization Check**

When a counterparty requests disclosure of value-bits, the operator shall:
- Scan user_state.jsonl for `kind: consent.grant` or `kind: consent.modify` records mentioning the requested predicate.
- For each matching record, verify: (a) signature valid, (b) not revoked (no `kind: consent.revoke` with `references_prior_seq` = this record's seq), (c) not expired (current_ts < expiry_ts), (d) time_window is satisfied (requested evidence is within the window).
- If counterparty class is `ideologue`, require an exact match to a per-identity consent record; reject class-level matches.
- If all checks pass, issue the disclosure; if any fail, return `unknown` for the withheld bit and log the denial.

---

## v1 Questions (T-M46.6)

Questions deferred to v1 (not in scope for v0):

1. **Hierarchical consent:** Can a principal grant consent for a category (e.g., "all unselfishness_* evidence") rather than enumerating individual predicates?
2. **Conditional consent:** "Grant unselfishness_evidence to employer if the computation occurs in the EU."
3. **Composite-bit consent:** Joint consent for multi-bit queries (e.g., "I consent to reveal `non_harm_evidence AND respect_for_difference_evidence` but not either alone").
4. **Delegation:** Can the principal delegate consent authority to a trusted agent for a bounded time?
5. **Expiry auto-renewal:** Should consent records auto-renew if the principal's evidence changes and the principal takes no action?

---

## Signoff

**Document:** Mirror Everest 46 — Per-Counterparty Consent for Values Disclosure  
**Version:** v0  
**Author:** Calm  
**Date:** 2026-05-20  
**Status:** Acceptance ready  
**Effort:** Medium  
**Prerequisite Gate:** Witness Everest 8 consent.v0 schema finalized; Mirror Everest 7 counterparty taxonomy finalized  
**Dependencies:** Mirror Everest 7, Mirror Everest 34, Mirror Everest 49, Mirror Everest 51  
**Word count:** 1,847 (target 8–12 KB approx. 2,000 words; compressed spec adheres to target)

---

— Calm, 2026-05-20