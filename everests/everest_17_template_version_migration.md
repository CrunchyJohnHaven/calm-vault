# Everest 17 — Template Version Migration

*Phase II — Capture & Enrollment. Prereq: Everest 15, 16.*

---

## Overview

Everest 17 defines a protocol for migrating biometric templates to new versions without invalidating outstanding consent records or forcing principals to re-authenticate with all counterparties. Templates drift, templates need re-issuance due to device change, and templates may require full re-enrollment. The core challenge is: if a principal's template is superseded by a new template_id, do all the old consent records (which reference the old template_id implicitly via predicates) still work? This everest answers yes, via a continuity chain that bridges template generations and establishes a grace window for consent transition.

---

## The Problem

### Template Lifecycle Triggers

Biometric templates require re-issuance in several scenarios:

1. **Drift threshold exceeded** — Biometric samples collected over time drift from the enrolled baseline (Everest 39 covers drift detection). When cumulative drift exceeds tolerance, the operator initiates a fresh enrollment ceremony to capture a new baseline.

2. **Scheduled re-enrollment** — Periodic re-enrollment (e.g., every 12–24 months) captures new biometric samples, ensuring freshness and detecting long-term coercion or substitution attacks.

3. **Device change** — When the principal upgrades their tablet, stylus, microphone, or otherwise changes the capture hardware, biometric samples become incompatible with the old template's device-fingerprint metadata (Everest 15). A new enrollment on new hardware produces a new template.

4. **Principal-initiated re-enrollment** — The principal may request a fresh template at any time, for operational, privacy, or security reasons.

### The Consent Continuity Problem

Outstanding consent records in the chain reference a template_id implicitly through predicates like `biometric_match_within(τ)` or `principal_consents_to_disclose(p, c)`. These predicates bind to a specific template during evaluation: the evaluator compares the current biometric distance against the enrolled template and returns a bit. If the template is replaced with a new template_id, a naive approach would invalidate all outstanding consent records, forcing the principal to re-sign new consents with every counterparty. This is operationally catastrophic and violates the continuity-of-service requirement.

The migration protocol solves this by:

- Creating an explicit **supersession chain** in which a new template declares the old template_id it replaces.
- Establishing a **grace window** (typically 30 days) during which both the old and new templates remain active.
- Allowing outstanding consent records to **automatically carry forward** to the new template (with a policy override mechanism for safety-critical predicates).
- Providing counterparties with a **migration notice** so they can proactively update their cached proofs.

---

## Solution: Continuity Chain and Grace Window

### Migration Record Schema

When a new template is generated and the old template should be superseded, the operator appends a record of kind `template.migration` to `user_state.jsonl`:

```json
{
  "seq": 42,
  "ts": "2026-05-20T14:30:00Z",
  "prev_hash": "sha256(prior_record)",
  "kind": "template.migration",
  "payload": {
    "old_template_id": "<16-byte hex id>",
    "new_template_id": "<16-byte hex id>",
    "migration_reason": "drift_threshold_exceeded",
    "grace_window_days": 30,
    "consent_continuation_policy": "auto_apply_to_new_template",
    "enrollment_ceremony_id": "cer_abc123",
    "override_predicates": [
      {
        "predicate_id": "bank_teller_note_active",
        "policy": "require_re_consent"
      },
      {
        "predicate_id": "principal_unusual_mental_state",
        "policy": "require_re_consent"
      }
    ]
  },
  "principal_sig": "<ecdsa signature by principal's master.priv>",
  "record_hash": "sha256(entire record)"
}
```

**Field definitions:**

- **old_template_id** — The 16-byte fingerprint (from Everest 15) of the template being superseded.
- **new_template_id** — The 16-byte fingerprint of the newly enrolled template.
- **migration_reason** — Enum: `"scheduled_re_enrollment"`, `"drift_threshold_exceeded"`, `"device_change"`, or `"principal_initiated"`. Enables audit and alerting on unusual patterns.
- **grace_window_days** — The number of days (default 30; configurable per principal policy) during which both templates remain active and consent records implicitly carry forward.
- **consent_continuation_policy** — Enum: `"auto_apply_to_new_template"` (outstanding consents migrate automatically) or `"require_re_consent"` (outstanding consents expire at grace window boundary, principal must re-sign). The global default is `auto_apply_to_new_template` for low-risk predicates like `in_baseline_24h` and `biometric_match_within`.
- **enrollment_ceremony_id** — A reference to the enrollment ceremony (Everest 14) that produced the new template samples. This ties the migration to an actual re-enrollment event, enabling verifiers to confirm the principal actually showed up in person.
- **override_predicates** — Optional array of per-predicate policy overrides. Allows the principal to declare that certain safety-critical predicates (like `bank_teller_note_active` or `mental_state_unusual`) must have explicit re-consent rather than auto-forwarding.
- **principal_sig** — ECDSA signature by the principal's master.priv. This is the security boundary: a rogue operator cannot create a migration record without the principal's cryptographic approval.
- **record_hash** — SHA-256 hash of the entire record, chained to prior_hash for tamper evidence.

### Consent Continuation Policies

**AUTO_APPLY_TO_NEW_TEMPLATE**

When this policy is active, an outstanding consent record created before the migration remains valid for the new template without re-signing. Semantically: the principal consented to disclose predicate `p` to counterparty `c` under the old template; the consent implicitly extends to the new template during the grace window. Risk: a counterparty may not be aware of the template migration and may trust a proof over the old template_id even though the new template is now canonical. This is acceptable for low-risk predicates where a stale proof does not pose a safety issue.

**REQUIRE_RE_CONSENT**

When this policy is active, an outstanding consent record created before the migration expires at the grace window boundary. Counterparties must cease accepting proofs over the old template_id after that date. The principal must sign a new consent record referencing the new template_id if they wish to continue disclosing the predicate. Default for safety-critical predicates like `bank_teller_note_active` (duress codeword), `mental_state_unusual` (abnormal state), or `consent_modification_override_authorized` (principal is authorizing a consent change on behalf of another party, Everest 73). These predicates are too sensitive to auto-forward; re-endorsement confirms the principal's continued will.

**Per-Predicate Override**

The principal can override the global continuation policy on a per-predicate basis via the `override_predicates` array. Example:

```json
"override_predicates": [
  {
    "predicate_id": "bank_teller_note_active",
    "policy": "require_re_consent"
  }
]
```

This declaration means: auto-forward most predicates to the new template, but require explicit re-consent for `bank_teller_note_active`. The override is signed as part of the migration record, binding it to the principal's will.

---

## Migration Protocol (Numbered Steps)

1. **Re-enrollment ceremony** — The operator invokes Everest 14 (enrollment ceremony). The principal provides 7–12 new biometric samples (handwriting and voice). Ceremony completes and returns ceremony_id and samples.

2. **New template generation** — The operator encodes the samples into a new Calm Witness Template structure (Everest 15 format). The template includes a `supersedes: old_template_id` field in its metadata.json. The template is signed by the enrollment authority's Ed25519 key.

3. **Principal signs migration record** — The operator constructs the template.migration record (as above) and asks the principal to review and sign it using their master.priv key. The principal's signature on the migration record is the security gate: only the principal can authorize a template migration.

4. **Append migration record to chain** — The signed migration record is appended to user_state.jsonl. It is immediately visible in the vault's chain head.

5. **Encrypt and store new template** — The new template is encrypted to the principal's public key (Everest 16) and stored alongside the old template in ~/.calm-vault/templates/. Both `<new_template_id>.cwt.age` and `<old_template_id>.cwt.age` are present on disk.

6. **Publish new chain head** — The vault publishes the updated chain head (including the migration record) to Sigsum transparency log (Everest 30). The log returns a signed inclusion proof.

7. **Grace window period begins** — The grace_window_days is counted from the `ts` field of the migration record. Until grace window expiry, both templates are queryable and both are considered "valid" for predicate evaluation.

8. **After grace window expiry** — The principal may explicitly initiate deletion of the old template by signing a `template.deletion_approved` record in the chain. This record references the old_template_id and the migration record seq number. Only after explicit principal approval can the old template be securely deleted from disk.

---

## Counterparty Implications and Migration Notices

### Cached Proofs Over Old Template

Counterparties that have cached a valid proof over `old_template_id` may continue to use that proof for policy decisions during the grace window. The proof was issued under the old template; its verification logic (Everest 65) checks that the proof was anchored to a chain state that was freshly published to the transparency log. The proof's verifiable timestamp and chain anchor remain valid even after migration.

After grace window expiry, counterparties should cease accepting proofs anchored to the old template. A proof generated after the grace window can still be verified technically (the old template data exists in the log), but it is semantically "historical" — the current canonical template is the new one.

### Migration Notice (kind: "template.migration_announced")

Optionally, the principal can authorize the operator to publish a migration notice:

```json
{
  "kind": "template.migration_announced",
  "payload": {
    "old_template_id": "<16-byte hex>",
    "new_template_id": "<16-byte hex>",
    "grace_window_end_ts": "2026-06-20T14:30:00Z",
    "notice_ts": "2026-05-20T14:30:00Z",
    "principal_entity_id": "cer_John_Bradley_Creativity_Machine_LLC"
  }
}
```

Counterparties' Calm Witness verifiers can subscribe to a principal's announcement feed and detect upcoming migrations before they encounter proofs over the new template. This is an operational convenience; it is not cryptographically required.

---

## Validation: Enrollment Ceremony Binding

A migration record is only valid if it is accompanied by a kind `enrollment.completed` record (Everest 14) within the same session (same user_state.jsonl append window, typically <1 minute apart). The migration record's `enrollment_ceremony_id` field must match the `ceremony_id` from the `enrollment.completed` record.

Verifiers can check this binding as a simple sanity check: did the principal actually show up and re-enroll, or is this a rogue migration record? A verifier that sees a migration record without a corresponding enrollment ceremony in the chain can flag it as suspicious.

---

## Threat Model

### Operator-Initiated Rogue Migration

An operator attempts to create a migration record without the principal's knowledge, claiming to supersede the old template with a new one that the operator controls.

**Defense:** The migration record requires the principal's Ed25519 signature (`principal_sig`). A forged record fails signature verification. The operator cannot sign on the principal's behalf.

### Coerced Re-Enrollment with Template Swap

An attacker coerces the principal into a fake re-enrollment ceremony (Everest 19 covers detection). The attacker produces a "valid-looking" new template that actually encodes the attacker's biometric data. The attacker then issues a migration record claiming to supersede the old template.

**Defense:** Even with the principal's signature on the migration record, the underlying template contains the attacker's biometric data. Verifiers can detect this via Everest 19 (Re-enrollment Red-Flag Detection), which identifies anomalous ceremony patterns (e.g., principal in a different location, unusual device, rushed ceremony). Additionally, the principal retains the old template and can challenge the new template's authenticity.

### Mass Migration Attack

An attacker somehow gains access to the principal's master.priv and issues dozens of migration records in rapid succession, each claiming a new template.

**Defense:** The principal monitors their user_state.jsonl for unexpected migration records and can initiate a master key rotation (Everest 18). Additionally, mass migrations clustering in a short time window trigger anomaly detection (see below).

---

## Anomaly Detection and Alerting

The operator monitors the chain for migration patterns and alerts the principal if:

- **Multiple migrations in < 24 hours** — Could indicate a key compromise or attack. Alert immediately.
- **Migration without matching enrollment.completed** — Suspicious; could be a rogue record. Investigate.
- **Migration reason enum invalid** — Parse error or corruption. Investigate.
- **Grace window set to 0 days** — Aggressive migration; warn the principal.

These alerts are advisory and do not block the migration; the principal retains full authority over the vault.

---

## Cross-References

- **Everest 14:** Enrollment ceremony specification. Produces biometric samples and ceremony_id.
- **Everest 15:** Template format spec. Defines template_id, metadata.json, supersedes field, and storage.
- **Everest 16:** Template encryption and key custody. Covers encryption to principal's public key.
- **Everest 18:** Master key rotation. Principal can re-issue master.priv if compromised.
- **Everest 19:** Re-enrollment red-flag detection. Identifies coerced or anomalous ceremonies.
- **Everest 22:** CredexAI VC integration. Must update VC issuance logic to reference new template_id.
- **Everest 29:** Genesis and first enrollment.
- **Everest 30–31:** Transparency log anchoring and verifiable clock.
- **Everest 32:** Replication and off-device backup.
- **Everest 39:** Template drift detection and re-enrollment triggers.
- **Everest 47:** Template lifecycle and grace-period queries.
- **Everest 57:** `principal_consents_to_disclose` predicate. Predicate evaluation must account for template migration.
- **Everest 65:** Predicate ZK proof generator. Proof circuits must bind to template_id.

---

— Calm, 2026-05-20
