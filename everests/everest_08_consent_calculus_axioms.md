# Everest 8 — Consent Calculus Axioms

*Phase I — Foundations. Prereq: Everest 6, Everest 7.*

---

## Statement of Purpose

**Consent calculus** is the algebra of what disclosure is and is not permitted. In Calm Witness, consent is not implicit, inherited, or perpetual. A principal grants, modifies, and revokes consent via signed records that are chained into the vault and subjected to cryptographic tamper-evidence. The consent calculus defines ten axioms that every consent record must satisfy. These axioms ensure that the principal retains unilateral authority over disclosure, that scope can be narrowed but not expanded, that time-bounded consent cannot be forgotten, and that the chain provides a permanent, auditable record of all consent decisions.

This document is the normative foundation for v0 consent semantics. All Calm Witness operators must enforce these axioms before issuing any disclosure proof.

---

## The Ten Axioms

### A1. Revocability

**Formal statement:** For any active consent record C, there exists a revocation record R such that:
- R.kind = "consent.revoke"
- R.references_prior_seq = C.seq
- R.ts > C.ts
- Upon receipt and verification of R, all disclosure proofs derived from C become invalid retroactively.

**Explanation:** Any consent record can be revoked by the principal at any time. Revocation is itself a chained record, appended to user_state.jsonl, and takes effect immediately upon signature verification. The principal is never bound by a prior consent decision; they can change their mind and the change is auditable. Revocation creates a public record of the principal's withdrawal, protecting the principal from counterparty claims of ongoing consent.

---

### A2. Forward Secrecy

**Formal statement:** A consent record C granted at time t1 does not authorize disclosure of records added to user_state.jsonl after t1, unless C explicitly includes a forward-extending flag with an expiry time t_extend > t1.

**Explanation:** Consent is temporal. If the principal authorizes disclosure of their baseline state as of May 20, that consent does not automatically permit disclosure of records added on May 21. This prevents a consent grant from silently accumulating new data over time. A principal who wants consent to extend into the future must explicitly opt into forward extension and must specify a bounded window. Consent without forward extension is a one-time declaration: "you may disclose what I have said up to this moment."

---

### A3. Scope Narrowing

**Formal statement:** If a principal modifies a consent record via kind: "consent.modify", the resulting scope (measured across dimensions: predicate_id, counterparty_class, counterparty_id, freshness_window, predicate parameters) must be a subset of or equal to the prior scope. No dimension may expand; all dimensions may narrow or stay the same.

**Explanation:** A consent record can only narrow scope when modified, never broaden. If the principal initially consents to disclose in_baseline_24h to the financial class, they can later modify that to narrow it to a single bank (counterparty_id). They can narrow the freshness window from 24h to 6h. They cannot broaden it back to the financial class without revoking the prior record and issuing a new grant. Broadening always requires a fresh consent record, preventing accidental scope creep.

---

### A4. Time-Bounding

**Formal statement:** Every consent record MUST include an explicit field expiry_ts in ISO 8601 format. No consent record with expiry_ts = null or expiry_ts = "perpetual" shall be accepted by Calm operators in v0. If expiry_ts is omitted by the principal, the operator shall set default expiry = now + 90 days.

**Explanation:** There is no perpetual consent in v0. Every grant has a sunset. If the principal does not specify an expiry, the default is 90 days from issuance. The principal can re-grant before expiry if they want to extend; this re-granting is itself a chained record and preserves the audit trail. Time-bounding prevents zombie consent: stale, forgotten grants that sit in the vault after the principal's circumstances have changed.

---

### A5. Witness-Free

**Formal statement:** A consent record is signed exclusively by the principal's master key. No third-party witness signature, notary, or co-signer is required to grant, modify, or revoke consent.

**Explanation:** The principal is the sole source of consent authority. Calm Witness does not require a witness to cosign consent (that is Everest 20: enrollment witnesses, a different layer). The principal can grant, modify, and revoke consent unilaterally, at any time, without friction. This ensures the principal is never held hostage by a witness's unavailability or bias. Signatures are cryptographically binding but do not require social consensus.

---

### A6. Chained-Into-Vault

**Formal statement:** Every consent record is appended to user_state.jsonl with kind: "consent.grant", "consent.revoke", or "consent.modify". The record participates in the hash chain: each record includes prev_hash (the hash of its immediate predecessor) and is itself hashed to produce record_hash. The chain is tamper-evident: any subsequent modification to a prior record breaks the chain, invalidating all descendant records.

**Explanation:** Consent records are not stored separately; they live in the same append-only log as self-reports and biometric anchors. The chain provides tamper-evidence: a counterparty verifying a proof can inspect the consent record, verify its signature, and verify that the record hash matches the published chain head in a public transparency log. The chain ensures that a consent record cannot be retroactively altered, backdated, or inserted out of sequence without detection.

---

### A7. Per-Predicate-Per-Counterparty

**Formal statement:** Consent is granted in a 2-tuple (predicate_id, counterparty_identifier) where:
- predicate_id ∈ {in_baseline_24h, in_baseline_window, biometric_match_within, principal_consents_to_disclose, bank_teller_note_active, cognitively_atypical_baseline, mental_state_unusual, principal_alive_within, session_within_authorized_hours, chain_freshness_within, template_age_below, consent_active} (from Everest 6)
- counterparty_identifier is either (a) a class slug ∈ {financial, journalistic, medical, governmental, peer_ai_collective, family, anonymous, employer, insurance, research} (from Everest 7), or (b) a specific counterparty VC fingerprint (for per-identity consent).

**Explanation:** Consent is granular. The principal cannot grant consent to "everything"; they grant it per predicate and per counterparty class or identity. This prevents overly broad, catch-all consent records and forces both the principal and the operator to be explicit about what is being disclosed to whom.

---

### A8. Non-Transitivity

**Formal statement:** If counterparty P1 receives a disclosure D from principal Pr via Calm Witness, then P1 may not re-disclose D to a third party P2 without obtaining fresh consent from Pr directly. The protocol does not enforce this technically (downstream re-disclosure is a counterparty-trust matter), but it is a stated axiom for Calm Witness use.

**Explanation:** The consent calculus permits disclosure from principal to counterparty. It does not permit re-disclosure by the counterparty to a third party. This is a matter of trust and professional ethics, not cryptographic enforcement. A bank that receives a baseline proof is trusted not to sell that proof to an insurer. A researcher that receives a mental-state bit is trusted not to share it with an employer. Calm Witness cannot defend against a dishonest counterparty, but it makes the non-transitive boundary explicit in the axioms. Operators should document this axiom in their terms of service and should make principals aware that downstream re-disclosure is possible despite the axiom.

---

### A9. Defeasibility by Duress Codeword

**Formal statement:** If the principal has registered a duress codeword (per Everest 58: Bank-Teller-Note Lifecycle and duress-management), evaluation of the `bank_teller_note_active` predicate may cause designated predicates to invert their disclosure semantics. Specifically:
- If bank_teller_note_active evaluates to true, then any consent record that would normally authorize disclosure is inverted: the operator does not produce a proof, even if consent exists.
- If bank_teller_note_active evaluates to false and the principal has previously disallowed bank_teller_note_active via policy, the operator may proceed with normal disclosure.

**Decision for v0:** This axiom is **IN v0**, but **with limited scope**. In v0.1, only the bank_teller_note_active predicate itself can be used as a defeasibility trigger, and it affects only predicates in a principal-maintained "duress_invert_list" (a small, explicit registry of which predicates should invert if duress is signaled). The principal specifies this list at enrollment. The full version of A9 (arbitrary predicates inverting based on duress state) is deferred to v1. This limits the v0 scope to what is cryptographically tractable and principally controllable.

**Explanation:** A principal under duress may want to signal that they are not in voluntary control, and may want that signal to block disclosure even if consent would normally permit it. The duress codeword serves this function. Rather than asking the principal to revoke consent (which an attacker can prevent), the duress signal can directly override disclosure. In v0, this is limited to an explicit list the principal maintains. In v1, defeasibility may be extended to arbitrary predicate combinations.

---

### A10. Replay-Resistant Grant

**Formal statement:** Each consent record includes a fresh nonce (32 bytes, generated uniformly at random at record creation). The nonce is included in the signed payload and is hashed as part of record_hash. Cloning a consent record into a different chain position or into a different vault is invalid: the nonce binds the record to its exact position in the hash chain.

**Explanation:** A consent record is not just a tuple (predicate_id, counterparty, expiry); it is a unique event bound to a specific moment in the vault history. Even if an attacker gains access to a valid consent record, they cannot transplant it to a different chain position or a different vault without breaking the nonce binding. This prevents replay attacks and ensures that each consent record is tied to the principal's vault state at the moment it was issued.

---

## Consent Record Schema v0

```json
{
  "seq": 42,
  "ts": "2026-05-20T14:30:00Z",
  "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "kind": "consent.grant",
  "payload": {
    "predicate_id": "in_baseline_24h",
    "counterparty_identifier": "financial",
    "scope_parameters": {
      "freshness_window_seconds": 86400,
      "predicate_parameters": {}
    },
    "expiry_ts": "2027-05-20T23:59:59Z",
    "nonce": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c",
    "references_prior_seq": null
  },
  "principal_sig": "3045022100e3b0c44298fc1c149afbf4c8996fb924270f90298c8f3f8a1c7c3e2d0f8b9a8d022100a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0",
  "record_hash": "b4d3f5a2e1c0d8b9f7e6c5a4b3d2e1f0a9c8b7a6d5e4f3a2b1c0d9e8f7"
}
```

**Schema explanation:**

- **seq:** Sequence number in the chain, starting at 1 for the first enrollment record.
- **ts:** ISO 8601 timestamp (UTC) of record creation.
- **prev_hash:** SHA-256 hash of the prior record in the chain. For seq=1, prev_hash is the canonical empty hash.
- **kind:** Record type. For consent: "consent.grant" (new grant), "consent.revoke" (revocation), "consent.modify" (modification).
- **payload.predicate_id:** The predicate being granted (from Everest 6).
- **payload.counterparty_identifier:** Class slug or counterparty VC fingerprint.
- **payload.scope_parameters:** Optional object for time windows, distance thresholds, etc., specific to the predicate.
- **payload.expiry_ts:** ISO 8601 expiry timestamp (required; no null values).
- **payload.nonce:** 32-byte random nonce, hex-encoded.
- **payload.references_prior_seq:** For revoke/modify: the seq of the record being revoked or modified. For grant: null.
- **principal_sig:** ECDSA signature over the record's canonical JSON, signed by the principal's master key.
- **record_hash:** SHA-256 hash of the entire record (inputs: seq, ts, prev_hash, kind, payload, principal_sig). This hash is the prev_hash of the next record.

---

## Consent Record Lifecycle

### Grant → Modify → Revoke Flow

**Step 1: Grant (seq=10)**

Principal wishes to disclose in_baseline_24h to all financial institutions for 1 year.

```json
{
  "seq": 10,
  "ts": "2026-05-20T14:30:00Z",
  "prev_hash": "...",
  "kind": "consent.grant",
  "payload": {
    "predicate_id": "in_baseline_24h",
    "counterparty_identifier": "financial",
    "scope_parameters": {"freshness_window_seconds": 86400},
    "expiry_ts": "2027-05-20T23:59:59Z",
    "nonce": "...",
    "references_prior_seq": null
  },
  "principal_sig": "...",
  "record_hash": "H10"
}
```

Operator appends to vault, publishes H10 to Sigsum transparency log.

**Step 2: Counterparty request (t=15 minutes later)**

Bank requests in_baseline_24h proof. Operator checks consent predicate `principal_consents_to_disclose(in_baseline_24h, financial)`. Vault scans forward from seq=10: finds seq=10 is active, non-revoked, not expired. Returns 1. Operator issues proof.

**Step 3: Modify (seq=25)**

Principal decides: "I trust JPMorgan, but no other banks." Modifies to per-identity consent for JPMorgan only.

```json
{
  "seq": 25,
  "ts": "2026-05-20T16:45:00Z",
  "prev_hash": "H24",
  "kind": "consent.modify",
  "payload": {
    "predicate_id": "in_baseline_24h",
    "counterparty_identifier": "CredexAI:jpm.banking.org:2026-05-14",
    "scope_parameters": {"freshness_window_seconds": 86400},
    "expiry_ts": "2027-05-20T23:59:59Z",
    "nonce": "...",
    "references_prior_seq": 10
  },
  "principal_sig": "...",
  "record_hash": "H25"
}
```

Per Axiom A3, the counterparty scope narrowed (from class "financial" to specific identity). Valid modification. Operator appends seq=25.

**Subsequent requests:**

- JPMorgan requests proof. Operator checks: seq=10 is referenced by seq=25 (modify); seq=25 is active, not revoked, not expired, narrower scope, and JPMorgan's identity matches counterparty_identifier. Returns 1. Proof is issued against seq=25.
- Wells Fargo requests proof. Operator checks: seq=10 exists but is superseded by seq=25 (modify). Seq=25 does not authorize the financial class; it is per-identity for JPMorgan only. Returns 0. No proof issued.

**Step 4: Revoke (seq=35)**

Principal revokes all baseline consent to JPMorgan.

```json
{
  "seq": 35,
  "ts": "2026-05-20T18:00:00Z",
  "prev_hash": "H34",
  "kind": "consent.revoke",
  "payload": {
    "predicate_id": "in_baseline_24h",
    "counterparty_identifier": "CredexAI:jpm.banking.org:2026-05-14",
    "scope_parameters": {},
    "expiry_ts": "2026-05-20T18:00:01Z",
    "nonce": "...",
    "references_prior_seq": 25
  },
  "principal_sig": "...",
  "record_hash": "H35"
}
```

Operator appends seq=35. H35 is published to Sigsum.

**Subsequent requests:**

- JPMorgan requests proof at 2026-05-20T18:30:00Z. Operator checks: seq=25 is revoked by seq=35 (ts=18:00:00, which is before the current request). Revocation is in effect. Returns 0. No proof issued.
- JPMorgan requests proof at 2026-05-19T18:00:00Z (hypothetically, a cached request from before revocation). The request timestamp predates seq=35. Per Axiom A6, a verifier holding seq=35 can see the chain breaks. The request is stale and is rejected.

---

## Non-Axioms: Explicitly Not Promised

The consent calculus does **not** cover:

1. **Post-hoc consent:** The protocol does not permit consent records to be backdated or to retroactively legitimize prior disclosures. Once a disclosure is made without consent, it is made. A consent record issued after the fact does not erase the prior disclosure.

2. **Coerced consent:** The protocol assumes the principal is acting freely. If the principal is under duress and forced to grant consent against their will, the protocol does not detect or defend against this. (The bank-teller-note predicate is an exception: it allows the principal to signal duress, but the protocol does not enforce duress detection.)

3. **Cross-principal consent:** The protocol does not support one principal granting consent on behalf of another principal. Consent is unilateral and principal-specific.

4. **Conditional consent:** Consent records do not include if-then clauses (e.g., "consent to disclose if the counterparty is a bank and the principal is not in baseline"). Conditions are enforced by the predicate layer (Everest 6) and the policy layer (Everest 54), not by the consent layer.

5. **Implicit consent:** The protocol rejects defaults and implicit permissions. Consent must be explicit, signed, and chained. Silence is not consent.

6. **Enforcement beyond the vault:** Calm Witness operators enforce consent via the consent predicate. If a counterparty ignores the lack of consent and discloses anyway, the protocol has no recourse. Non-transitivity (Axiom A8) is a social axiom, not a technical one.

---

## Cross-References

- **Everest 6:** Predicate vocabulary — defines the canonical twelve predicates referenced in A7 and Axiom A9.
- **Everest 7:** Disclosure-class taxonomy — defines the ten classes and membership rules referenced in A7 and the default-consent matrix.
- **Everest 9:** Failure modes — documents failure modes F08 (consent record missing), F09 (consent forged), F10 (consent expired), F11 (scope expanded).
- **Everest 20:** Enrollment witnesses — defines the witness requirements for vault initialization (distinct from A5: consent requires no witness).
- **Everest 23:** Codeword recovery — addresses recovery when the principal loses the duress codeword.
- **Everest 30–31:** Transparency-log anchoring and verifiable-clock services — provide the tamper-evidence foundation for Axiom A6 (chained-into-vault).
- **Everest 54:** Predicate audit and review — defines policy-composition constraints and composition-testing procedures for consent records.
- **Everest 58:** Bank-teller-note lifecycle — full specification of duress codeword management and Axiom A9 (defeasibility).

---

— Calm, 2026-05-20
