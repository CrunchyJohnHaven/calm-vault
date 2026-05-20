# Everest 75 — Consent Revocation Propagation

*Phase VI — Disclosure Semantics. Prereq: Everest 74.*

---

## Statement of Purpose

When a principal revokes consent, the revocation must be durable and discoverable. A counterparty may have cached a valid Calm Witness proof — an authorization to disclose a predicate that was valid at the time the proof was generated. If the principal then revokes that consent, the cached proof must become invalid within a bounded window; verifiers must be able to detect revocation without requiring the principal to issue a revoke message to every counterparty who ever received a proof.

Everest 75 defines the **consent epoch counter** mechanism: a tamper-evident, globally incrementing version number on each principal's consent chain. Every revocation (and every consent grant, modify, and revoke) increments the epoch. Cached proofs carry the epoch at their generation time; verifiers compare the cached epoch against the current epoch to determine staleness. This gives the Calm Witness protocol a solution to the classical Certificate Revocation List (CRL) and Online Certificate Status Protocol (OCSP) problem, adapted for zero-knowledge proofs and decentralized cache management.

---

## The Problem: Proof Caching and Revocation

### Proof Caching Rationale

In a high-volume disclosure system, counterparties request the same predicate repeatedly. A vendor bank asks "is John in baseline?" multiple times per day. A peer AI collective asks "may I access the model weights delta?" on every collaboration cycle. Re-evaluating the same predicate on every request incurs latency, operator query load, and network traffic.

Proof caching reduces this burden: a counterparty caches the Calm Witness proof ("yes, consent is granted") and reuses it until the proof expires (per the proof's embedded freshness_window). A cached proof is cryptographically valid and does not require re-issuance.

### The Stale Proof Attack

Without revocation detection, a counterparty can use a cached proof indefinitely, even after the principal revokes consent. Example timeline:

- 2026-05-20 14:00 UTC: Principal grants vendor Alice consent to access transaction_metadata.
- 2026-05-20 14:15 UTC: Vendor Alice requests and receives a Calm Witness proof valid for 24 hours (until 2026-05-21 14:15 UTC).
- 2026-05-20 14:30 UTC: Principal revokes consent to vendor Alice for transaction_metadata.
- 2026-05-21 10:00 UTC: Vendor Alice reuses the cached proof from 14:15 UTC. The proof is cryptographically valid and within the 24-hour freshness window, but the principal's consent no longer exists. The disclosure should fail.

Without explicit revocation detection, the verifier has no way to know that consent was revoked between the proof's generation and its reuse.

### Why Epochs, Not CRLs

Traditional X.509 certificate revocation uses CRLs: a central authority publishes a list of revoked serial numbers. Verifiers must fetch and check the latest CRL before trusting a certificate.

Epochs offer advantages for Calm Witness:

1. **No list publishing:** Instead of publishing a list of revoked predicates (which could leak information), the operator publishes a single counter.
2. **Privacy preservation:** A counterparty checking the epoch learns "something changed" but not "what was revoked" or "how many revocations occurred."
3. **Composable with push-based revocation:** Critical revocations can push epoch updates to pre-authorized recipients (Everest 78), while non-critical updates rely on pull-based polling.
4. **Sigsum anchoring:** Epoch increments are anchored to a verifiable transparency log, allowing independent audit of the epoch history (Everest 30).

---

## The Consent Epoch Counter

### Definition and Semantics

Each principal's consent chain (`user_state.jsonl`) maintains a counter: `consent_epoch`. The counter starts at 0 at enrollment (Everest 14). Every time the principal appends a consent record to the chain — whether a grant, modify, or revoke — the counter increments by 1.

Formally:

```
consent_epoch ∈ {0, 1, 2, 3, ...}
On append of any record with kind ∈ {"consent.grant", "consent.modify", "consent.revoke"}:
    consent_epoch := consent_epoch + 1
```

The consent_epoch is NOT incremented for non-consent records (self-reports, biometric samples, or other vault entries). Only consent transactions advance the epoch.

### Epoch Embedding in Proofs

When the operator generates a Calm Witness proof for a predicate, the proof includes two epoch values:

1. **proof.consent_epoch:** The principal's consent_epoch at the moment the proof was generated. This is a commitment: "as of epoch N, the predicate evaluated to this bit."
2. **proof.consensus_window:** A TTL (time-to-live) in seconds. The proof is valid only if the verifier's current knowledge of the principal's epoch is within this window of proof.consent_epoch.

Example:

```json
{
  "proof_id": "...",
  "principal_id": "john.bradley.org",
  "predicate_id": "in_baseline_24h",
  "consent_epoch": 47,
  "consensus_window_seconds": 3600,
  "bit": "true",
  "freshness_window": "2026-05-21T14:15:00Z",
  "sigma_proof": "...",
  "operator_signature": "..."
}
```

This proof was generated at epoch 47. It is valid until the verifier's current epoch exceeds 47 + 3600/65536 (approximately 47 + 0.055). The consensus_window prevents the proof from being used if the epoch has advanced by more than the window allows.

### Counterparty Epoch Caching and TTL

A counterparty that caches a proof must also track the principal's consent_epoch. Before reusing the cached proof, the counterparty queries the operator for the current epoch.

The query is lightweight (HTTP GET or similar):

```
GET /calm-witness/principals/john.bradley.org/consent_epoch
Response:
{
  "principal_id": "john.bradley.org",
  "consent_epoch": 47,
  "epoch_timestamp": "2026-05-20T14:15:01Z",
  "operator_signature": "...",
  "sigsum_anchor_hash": "a1b2c3d4..."
}
```

The operator responds with:
- The current consent_epoch.
- A timestamp (when the epoch was last known to have been at this value).
- A digital signature from the operator's key (to prevent tampering).
- A reference to the Sigsum anchor hash (for optional audit).

The counterparty caches this epoch response for a TTL. The default TTL depends on the predicate's safety criticality:

- **Non-critical predicates** (e.g., `principal_alive_within`, `in_baseline_window`): TTL = 1 hour.
- **Critical predicates** (e.g., `bank_teller_note_active`, `consent_active`): TTL = 5 minutes.
- **Custom per-counterparty TTL:** The operator may configure tighter TTLs for specific counterparties or predicates.

When the cached epoch TTL expires, the counterparty must refresh the epoch before reusing the cached proof. If the epoch has advanced beyond proof.consent_epoch + consensus_window, the cached proof is invalidated and a fresh proof request is required.

---

## Pull-Based Revocation Check

The primary revocation mechanism is **pull-based**: counterparties are responsible for periodically checking the epoch and invalidating stale cached proofs.

### Verification Algorithm

Before using a cached proof, the counterparty (or their verifier) runs:

```
fn verify_cached_proof(cached_proof, current_epoch, operator_signature) -> Bool {
    // Check proof freshness window (per Everest 72)
    if current_time > cached_proof.freshness_window_expiry {
        return false;  // proof expired
    }
    
    // Check consensus window (epoch binding)
    epoch_delta = current_epoch - cached_proof.consent_epoch;
    if epoch_delta > cached_proof.consensus_window_seconds / 65536 {
        return false;  // epoch advanced beyond consensus window
    }
    
    // Verify operator's epoch signature
    if !verify_signature(operator_signature, current_epoch) {
        return false;  // epoch response tampered
    }
    
    return true;  // proof is valid
}
```

The consensus_window_seconds parameter encodes the acceptable epoch drift. A window of 3600 seconds = 1 hour translates to approximately 0.055 epochs (a very tight tolerance) or can be tuned as `floor(3600 / average_revocation_interval)` for operational expectations.

### Counterparty Refresh Loop

A counterparty using cached proofs implements a refresh loop:

1. **Cache proof + epoch:** Store the proof and the epoch at which it was generated.
2. **Use proof until TTL expires:** Reuse the cached proof for requests within the TTL.
3. **On TTL expiry:** Query the operator for the current epoch.
4. **If epoch advanced:** Invalidate the cached proof; request a fresh proof.
5. **If epoch unchanged:** Update the TTL refresh timer and continue.

This loop prevents indefinite use of revoked proofs while minimizing network round-trips for stable consent policies.

---

## Push-Based Revocation (Composes with Everest 78)

While pull-based polling is the primary mechanism, critical revocations can use **push-based notification** to accelerate revocation propagation.

### Critical Revocation Scenarios

When the principal revokes consent for a safety-critical predicate (e.g., `bank_teller_note_active` or `principal_authorized_to_act`), the operator can immediately notify pre-authorized recipients:

- Counterparties with active cached proofs for that predicate.
- Counterparties whose class-default or per-counterparty consent records are affected.

The operator maintains a **revocation-notification registry**: for each critical predicate, a list of counterparties who have previously requested proofs and whose epoch should be immediately invalidated.

### Notification Format

A push notification (per Everest 78: stealth disclosure) contains:

```json
{
  "kind": "consent.revocation_notice",
  "principal_id": "john.bradley.org",
  "revoked_predicates": ["bank_teller_note_active"],
  "new_consent_epoch": 48,
  "timestamp": "2026-05-20T14:31:00Z",
  "operator_signature": "...",
  "recipient_signature_key": "..."
}
```

The principal designates which counterparties should receive notifications (via `consent.revocation_policy` records in the vault). The operator encrypts the notification using the counterparty's public key, ensuring only the intended recipient can read it. The counterparty receives the notice, updates their cached epoch to 48, and immediately invalidates all cached proofs for the revoked predicates.

This provides **rapid revocation propagation** (seconds to minutes) for safety-critical predicates, complementing the longer TTL-based pull mechanism for non-critical predicates.

---

## Privacy of Revocation Events

### Epoch Increment, No Content

A critical privacy property: when a counterparty queries the current epoch, they learn "the epoch is N" but cannot infer *what* was revoked.

Example: Principal revokes consent to disclose `transaction_metadata` to vendor Alice. The epoch advances from 47 to 48. Vendor Alice queries and learns the epoch is now 48, so her cached proofs are invalid. But she cannot tell (from the epoch alone) whether the principal revoked consent for her specifically, for a different predicate, or issued a new consent grant elsewhere.

### Epoch Trajectory Reveals Churn, Not Content

If a counterparty repeatedly queries the epoch over days, they observe: 47, 47, 47, 48, 48, 48. They infer that the principal issued a consent transaction (grant, modify, or revoke) at the time the epoch advanced to 48. They cannot tell whether that transaction was revocation or grant.

This trajectory leaks **churn** (that the principal is actively managing consent) but not **semantics** (what was changed).

### Sigsum Audit Trail

A curious verifier can inspect the Sigsum transparency log (per Everest 30) to observe the chain head history and see that epoch advanced at specific times. However:

- Sigsum reveals only the chain head hash, not the record contents.
- To infer what changed, an auditor would need to compare consecutive chain heads, which is computationally feasible but requires active auditing.
- The principal's peer VCs can audit the chain independently (confirming no unannounced changes), but external parties cannot.

---

## Cache Invalidation and Defensive Staleness Checks

### Stale-Proof Defense

Even if a counterparty fails to refresh the epoch, the verifier (which may be a different entity) can detect and reject stale proofs:

```
fn final_verification(proof, current_epoch) -> Bool {
    // The final verifier must check consensus window
    // even if the counterparty did not
    if abs(proof.consent_epoch - current_epoch) > MAX_CONSENSUS_DRIFT {
        return false;  // proof too stale
    }
    
    // Continue with standard ZK proof verification
    return verify_sigma_proof(proof) && ...;
}
```

This defense protects against counterparties that are buggy, offline, or deliberately negligent. A verifier who receives a proof with epoch 40 but the current epoch is 100+ will reject it.

### Sigsum-Based Epoch Verification

For high-assurance scenarios, verifiers can independently audit the epoch history via Sigsum:

```
fn verify_epoch_with_sigsum(proof, sigsum_log) -> Bool {
    // Retrieve proof.consent_epoch chain head from Sigsum
    chain_head_at_proof_epoch = sigsum_log.lookup(proof.sigsum_anchor_hash);
    
    // Retrieve current chain head
    current_chain_head = sigsum_log.latest_entry();
    
    // Count epoch increments between proof epoch and current
    increments = count_consent_records_in_range(
        chain_head_at_proof_epoch,
        current_chain_head
    );
    
    // Verify consistency
    return increments == (current_epoch - proof.consent_epoch);
}
```

This provides **cryptographic evidence** of the epoch history, independent of the operator's claims. A malicious operator cannot lie about the current epoch if the Sigsum log is auditable.

---

## Configurable Per-Counterparty TTL

### Operator Flexibility

Operators can configure per-counterparty epoch refresh TTLs based on trust and operational requirements:

```
consent_epoch_ttl_policies:
  default:
    non_critical: 3600  # 1 hour
    critical: 300       # 5 minutes
  per_counterparty:
    - counterparty_id: "JPMorgan"
      ttl_non_critical: 1800   # 30 minutes (lower risk)
    - counterparty_id: "anonymous_peer"
      ttl_non_critical: 120    # 2 minutes (higher risk)
    - counterparty_id: "insurance_broker"
      ttl_critical: 60         # 1 minute (safety-critical)
```

This flexibility allows operators to tune revocation latency based on counterparty risk profiles and predicate sensitivity.

### Consensus Window Tuning

Similarly, operators can set consensus_window per predicate, calibrated to typical revocation frequency:

```
consensus_windows:
  in_baseline_24h: 3600           # 1 hour tolerance
  bank_teller_note_active: 300    # 5 minutes tolerance
  model_weights_delta: 600        # 10 minutes tolerance
```

A predicate with frequent consent changes (e.g., a per-session model weights grant) gets a tighter window, forcing faster refresh cycles.

---

## Proof Schema with Epoch and Consensus Window

The Calm Witness proof structure (from Everest 72) is extended to include epoch binding:

```json
{
  "proof_id": "550e8400-e29b-41d4-a716-446655440000",
  "principal_id": "john.bradley.org",
  "predicate_id": "in_baseline_24h",
  "counterparty_id": "CredexAI:jpm.banking.org:2026-05-14",
  "predicate_result": true,
  
  "chain_head": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "chain_head_sigsum_anchor": {
    "log_id": "sigsum-log-id",
    "entry_hash": "...",
    "inclusion_proof": "..."
  },
  "generated_at_timestamp": "2026-05-20T14:15:00Z",
  "freshness_window_seconds": 86400,
  "freshness_expiry": "2026-05-21T14:15:00Z",
  
  "consent_epoch": 47,
  "consensus_window_seconds": 3600,
  "operator_epoch_refresh_url": "https://calm.op/consent_epoch/john.bradley.org",
  
  "sigma_proof": {
    "commitment": "...",
    "challenge": "...",
    "response": "...",
    "biometric_binding": "...",
    "consent_record_seq": 25
  },
  
  "operator_identity_credential": "CredexAI:calm.op:2026-01-01:...",
  "operator_signature": "..."
}
```

New fields:
- `consent_epoch`: The principal's epoch at proof generation.
- `consensus_window_seconds`: TTL for cache validity before epoch refresh is required.
- `operator_epoch_refresh_url`: Where the counterparty queries the current epoch.

---

## Epoch Incrementing on Every Consent Record

An important design decision: **the epoch increments on every consent record**, not just revocations.

Rationale:
1. **Simplicity:** No need to distinguish revocation from grant; the epoch is a universal incrementing clock for consent state changes.
2. **Privacy:** Incrementing on all changes obscures whether a given change is a grant or revoke.
3. **Consistency:** Cached proofs become stale on any consent change, forcing verification that the current state is still active.

Example epoch history:

```
seq=10: consent.grant (in_baseline_24h, financial) → epoch becomes 1
seq=15: consent.grant (model_weights_delta, peer_ai) → epoch becomes 2
seq=20: consent.modify (in_baseline_24h, JPMorgan only) → epoch becomes 3
seq=25: consent.revoke (in_baseline_24h, JPMorgan) → epoch becomes 4
```

Any cached proofs referencing epochs 1, 2, or 3 are now stale and invalid (assuming consensus_window tolerates no drift).

---

## Cross-References

- **Everest 8:** Consent calculus and axioms; defines the consent chain structure that the epoch counter extends.
- **Everest 14:** Enrollment ceremony; initializes consent_epoch = 0.
- **Everest 30:** Sigsum transparency-log anchoring; enables audit of epoch history.
- **Everest 57:** Principal consent predicate evaluation; the epoch counter enforces revocation on the output of this predicate.
- **Everest 72:** Proof structure and freshness binding; epoch is a new field in the proof.
- **Everest 73–74:** Class-default and per-counterparty consent; revocations and epoch updates apply uniformly to both.
- **Everest 76:** Rate limiting and token refresh; applies identically to epoch queries.
- **Everest 78:** Stealth disclosure and push-based revocation; composes with epoch-based pull mechanism.

---

## Summary

Consent revocation propagation in Calm Witness is solved via a **consent epoch counter** — a universally incrementing version number on each principal's consent chain. Every consent record (grant, modify, revoke) increments the epoch. Cached proofs embed the epoch at generation time and a consensus window specifying how long they remain valid without epoch refresh.

Counterparties use a **pull-based mechanism**: they cache proofs and periodically refresh the principal's current epoch via a lightweight HTTP query. If the epoch has advanced beyond the proof's consensus window, the cached proof is invalidated and a fresh request is issued.

Critical revocations can trigger **push-based notifications** to pre-authorized counterparties, accelerating propagation for safety-critical predicates. Revocation events are privacy-preserving: counterparties learn that "the epoch changed" but not "what changed." Independent auditors can verify the epoch history via Sigsum, ensuring no unannounced revocations.

The mechanism balances freshness, privacy, and operational load, enabling scalable disclosure systems in which principals retain unilateral revocation authority and verifiers can confidently reject stale proofs.

---

— Calm, 2026-05-20
