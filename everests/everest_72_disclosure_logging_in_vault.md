# Everest 72 — Disclosure Logging in Vault

*Phase VI — Disclosure Semantics. Prereq: Everest 26.*

---

## Statement of Purpose

Every Calm Witness proof that leaves the vault appends a record to the user_state.jsonl log. The principal can audit at any time: which counterparty asked, what predicate, when, what bit was returned, whether the disclosure was granted or denied. This is the principal's accountability tool and the foundation of voluntary disclosure transparency.

The disclosure log serves two purposes. First, it creates a complete audit trail within the principal's own vault, enabling the principal to detect unauthorized or suspicious requests and to monitor patterns of disclosure-seeking behavior (e.g., repeated fishing attempts from a particular counterparty). Second, it preserves a tamper-evident record that the principal can produce to a regulator, auditor, or court as evidence of what was disclosed, when, and to whom. Unlike a consent record (which lives in the same chain and binds what the principal authorized), a disclosure record captures what actually happened — whether the proof was issued, whether it was denied, and whether there were errors.

The acceptance test for Everest 72 is: every disclosure request, regardless of outcome, appends a record to the chain. There is no silent denial. If a counterparty asks, the request and response are logged.

---

## Disclosure Record Schema v0

Each disclosure record is appended to user_state.jsonl with kind: "disclosure" and the following structure:

```json
{
  "seq": 142,
  "ts": "2026-05-20T14:30:00Z",
  "prev_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "kind": "disclosure",
  "payload": {
    "disclosure_id": "550e8400-e29b-41d4-a716-446655440000",
    "request_ts": "2026-05-20T14:29:55Z",
    "response_ts": "2026-05-20T14:30:00Z",
    "counterparty_vc_fingerprint": "sha256:a7f9e3c2d1b8f4a6c5e7d9b1a3f5c8e0d2b4a6f8c0e2a4b6d8f0a2c4e6",
    "counterparty_class_at_disclosure": "financial",
    "predicate_id": "in_baseline_24h",
    "predicate_parameters": {},
    "freshness_window_seconds": 86400,
    "chain_head_at_disclosure": "b4d3f5a2e1c0d8b9f7e6c5a4b3d2e1f0a9c8b7a6d5e4f3a2b1c0d9e8f7",
    "disclosed_bit": true,
    "proof_hash": "sha256:3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c",
    "consent_record_referenced_seq": 10,
    "operator_sw_version": "calm-witness-0.1.0",
    "request_nonce": "f1e2d3c4b5a69798796a5b4c3d2e1f0",
    "notes": null
  },
  "principal_sig": "3045022100e3b0c44298fc1c149afbf4c8996fb924270f90298c8f3f8a1c7c3e2d0f8b9a8d022100a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0",
  "record_hash": "b4d3f5a2e1c0d8b9f7e6c5a4b3d2e1f0a9c8b7a6d5e4f3a2b1c0d9e8f7"
}
```

### Field Definitions

- **seq:** Sequence number in the user_state.jsonl chain.
- **ts:** ISO 8601 timestamp (UTC) when the disclosure record was appended to the vault.
- **prev_hash:** SHA-256 hash of the prior record in the chain (linking constraint per Everest 26).
- **kind:** Fixed value "disclosure".
- **payload.disclosure_id:** UUIDv4, unique identifier for this disclosure event.
- **payload.request_ts:** ISO 8601 timestamp when the counterparty's request was received by the operator.
- **payload.response_ts:** ISO 8601 timestamp when the operator sent the response (or decided to deny).
- **payload.counterparty_vc_fingerprint:** SHA-256 hash of the counterparty's CredexAI verifiable credential (or credential bundle). Hashed, not stored in plaintext, so the principal can later match it against their roster of known counterparties; outsiders cannot reverse it.
- **payload.counterparty_class_at_disclosure:** Class slug from Everest 7 (financial, journalistic, medical, governmental, peer_ai_collective, family, anonymous, employer, insurance, research).
- **payload.predicate_id:** The canonical predicate identifier (from Everest 6, e.g., in_baseline_24h, mental_state_unusual, biometric_match_within, etc.).
- **payload.predicate_parameters:** JSON object capturing parameters passed to the predicate. For example, if the predicate is biometric_match_within(0.3), this field contains {"distance_threshold": 0.3}. Empty object if no parameters.
- **payload.freshness_window_seconds:** The time window (in seconds) that the counterparty requested. Example: 86400 for 24 hours.
- **payload.chain_head_at_disclosure:** SHA-256 hash of the chain head referenced in the proof sent to the counterparty. Allows the principal to verify that the proof was about a specific chain state.
- **payload.disclosed_bit:** The boolean or ternary outcome. True if the predicate evaluated to true and consent was present. False if the predicate evaluated to false or consent was denied. Indeterminate if the predicate could not be evaluated (error, insufficient data).
- **payload.proof_hash:** SHA-256 hash of the proof bytes sent to the counterparty. Allows the principal to detect if the proof was tampered with in transit.
- **payload.consent_record_referenced_seq:** Sequence number of the consent.grant record in user_state.jsonl that authorized this disclosure. If no consent was granted (consent denied), this field is null.
- **payload.operator_sw_version:** Version of calm-witness software that generated the proof (for future debugging and auditing of software behavior).
- **payload.request_nonce:** The nonce provided by the counterparty to prevent replay attacks. Recorded here so the principal can verify that the request was not replayed.
- **payload.notes:** Optional free-form field for the operator to record unusual circumstances (e.g., "Consent expired, disclosure denied", "Predicate evaluation raised exception: division by zero", "Chain verification failed").
- **principal_sig:** ECDSA signature over the disclosure payload, signed by the principal's master key. (In v0, this may be deferred to v0.1 if signing all disclosure records creates I/O bottleneck; see implementation section below.)
- **record_hash:** SHA-256 of the entire record (canonical JSON, sorted keys, separators=(",",":"), excluding record_hash itself). Links this record into the chain.

---

## Disclosure Logging Semantics

### Atomicity

Disclosure proof generation and logging are atomic from the operator's perspective:

1. Counterparty sends request (predicate_id, parameters, freshness_window, nonce).
2. Operator checks consent via the principal_consents_to_disclose predicate (Everest 6).
3. Operator evaluates the target predicate (e.g., in_baseline_24h).
4. Operator generates the zero-knowledge proof.
5. Operator appends a disclosure record to user_state.jsonl.
6. Only after the record is successfully appended does the operator return the proof to the counterparty.

If step 5 fails (filesystem full, permission denied, corrupt file), the operator MUST NOT send the proof (step 6). The proof is destroyed (memory zeroed) before the function returns. This ensures that every proof seen by a counterparty has a corresponding, tamper-evident disclosure record in the vault.

### What Gets Logged

Every disclosure request appends a record, regardless of outcome:

- **Successful disclosure (True):** The disclosed_bit field is set to true. The proof_hash and proof bytes are recorded. The consent_record_referenced_seq points to the authorization.
- **Disclosure denied (False):** The disclosed_bit field is set to false. proof_hash is null. Notes field records the reason: "consent denied", "predicate evaluated false", "counterparty rate limit exceeded", etc.
- **Predicate evaluation error (Indeterminate):** The disclosed_bit field is set to null or a special "indeterminate" value. Notes record the error: "missing baseline data", "biometric matching service unavailable", "consent record signature verification failed", etc.

Even denied and erroneous disclosures are logged. This allows the principal to:

1. Detect fishing attempts — a counterparty repeatedly requesting data the principal has not consented to.
2. Identify system failures — predicates that consistently fail for certain counterparty classes.
3. Build evidence for revocation or regulatory action — if a counterparty is repeatedly trying to obtain sensitive predicates despite explicit consent denial.

### Privacy Within the Vault

The disclosure record is never itself disclosed to a counterparty. If a third party (P2) asks "has the operator disclosed predicate X to counterparty Y?", the operator does NOT answer. Answering this question would leak metadata: it would tell P2 about other counterparties' relationships with the principal. This is an out-of-band metadata-leakage risk and is blocked at the protocol level.

The counterparty VC fingerprint is a hash, not the VC content. The principal can later decode it by checking against their roster of known counterparties; an external attacker cannot.

### Counterparty Identity Obscuration

If the counterparty class is "anonymous" (no verifiable credential), the counterparty_vc_fingerprint is a hash of the counterparty's network characteristics (IP address, TLS certificate fingerprint, etc.). The principal can then audit disclosures to anonymous actors and can recognize repeat requests from the same opaque network endpoint.

---

## Audit Tooling

The operator provides CLI commands for the principal to audit disclosure records:

```
calm-witness audit disclosures
```

Lists all disclosure records in the vault, formatted as a table or JSON, sortable and filterable:

```
calm-witness audit disclosures [--counterparty <vc_fingerprint>] \
  [--predicate <predicate_id>] \
  [--from <ISO8601>] [--to <ISO8601>] \
  [--outcome true|false|indeterminate] \
  [--format table|json|csv]
```

Examples:

```
calm-witness audit disclosures --predicate in_baseline_24h --outcome false
```

Show all denied in_baseline_24h requests (potential fishing).

```
calm-witness audit disclosures --counterparty sha256:a7f9e3c2d1b8f4a6 --from 2026-05-01 --to 2026-05-20
```

Show all disclosures to a specific counterparty in the past 20 days.

```
calm-witness audit disclosures --rate
```

Emit a per-counterparty request-rate summary: how many requests per class per 24-hour window. Helps detect rate-limit violations and fishing patterns.

### Audit Query Performance

For a principal with <10,000 disclosure records (typical), audit queries are linear scans over the records and complete in <100 ms. For principals with >50,000 records, the operator may implement an indexed secondary index (keyed by counterparty_vc_fingerprint and predicate_id) to accelerate queries; the index is rebuilt whenever the vault is updated.

---

## Consent Reference and Traceability

Every disclosure record references the seq of the consent.grant record it relied upon (consent_record_referenced_seq). This creates a bidirectional audit trail:

1. Principal grants consent (seq=10, in_baseline_24h to financial class).
2. Counterparty requests proof; disclosure is logged (seq=142, disclosed_bit=true, consent_record_referenced_seq=10).
3. Later, a disclosure record and its authorizing consent record can be linked.
4. If the principal revokes consent (seq=100, referencing seq=10), the principal can audit all disclosures that relied on seq=10 and understand the impact of revocation.

This traceability also helps with Everest 75 (consent revocation propagation): when a consent is revoked, the disclosure log shows which counterparties received proofs under that consent, enabling the operator to notify those counterparties that the authorization is no longer valid.

---

## Retention and Rotation

Disclosure records are permanent — never deleted from the active vault. The principal's audit trail is preserved as long as the vault exists.

The principal can opt-in to per-predicate expiry for sensitive predicates. For example, if the principal wants to limit subpoena exposure for bank_teller_note disclosures, they can set a retention window (e.g., 30 days) for that predicate. After expiry, old bank_teller_note disclosure records are moved to an archived, encrypted-at-rest set (not deleted, but removed from the active log). The archived records are not accessible via the audit CLI unless the principal explicitly requests them.

When the principal rotates keys or migrates to a new vault (Everest 70), the disclosure log is carried forward in its entirety. No disclosure history is lost across rotations.

---

## Failure Modes and Edge Cases

### Operator Cannot Append

If the operator successfully generates a proof but cannot append the disclosure record (filesystem full, permission error, corrupt JSONL), the operator MUST destroy the proof and return an error to the counterparty. The counterparty may retry; the principal sees a retried request in the disclosure log and can investigate.

### Proof Hash Verification

If a counterparty claims they received a proof but the proof_hash in the disclosure record does not match the proof they hold, either:

1. The proof was tampered with in transit.
2. The operator generated and logged the proof incorrectly.

The principal can use this as evidence to dispute the counterparty's claim or to investigate a system compromise.

### Rate Limit Exceeded

If a counterparty exceeds a rate limit (e.g., the financial class is limited to 20 disclosures per 24h per Everest 7), the operator logs a disclosure record with disclosed_bit=false and notes: "rate limit exceeded for financial class". The principal can see the pattern and can further restrict the counterparty if desired.

### Consent Record Missing or Invalid

If the counterparty requests a proof but the referenced consent record is missing (e.g., the principal revoked it), the operator logs a disclosure with disclosed_bit=false and consent_record_referenced_seq=null, notes: "referenced consent record seq=10 does not exist or is revoked". This preserves evidence of the request.

---

## Cross-References

- **Everest 6:** Predicate vocabulary — defines the canonical predicates and their semantics.
- **Everest 7:** Disclosure-class taxonomy — defines counterparty classes and default rate limits.
- **Everest 8:** Consent calculus axioms — defines consent.grant, consent.revoke, consent.modify records and their traceability.
- **Everest 26:** JSONL schema and validators — defines the user_state.jsonl structure and chaining invariants that disclosure records must satisfy.
- **Everest 28:** Chain verifier — the calm-witness verify-chain CLI confirms that disclosure records are tamper-evident.
- **Everest 30:** Sigsum transparency logging — disclosure records can be anchored in a public transparency log for stronger tamper evidence.
- **Everest 75:** Consent revocation propagation — uses disclosure records to identify affected counterparties.

---

## Implementation Notes

In the initial deployment (calm-witness-rs v0.1), disclosure records are logged synchronously: the operator appends the record, fsync()s the file, then returns the proof. This ensures durability at the cost of slight latency (5–10 ms per disclosure). For high-throughput operators, an async logging variant may be deployed, with a background thread batching disclosure records and periodically fsync()-ing them in groups. The batching window must be <1 second to keep the audit trail fresh.

Principal signatures on disclosure records (principal_sig field) are optional in v0.1. If the principal's vault is encrypted at rest and the operator is trusted, the disclosure record's inclusion in the tamper-evident chain provides sufficient integrity. In v0.2 and later, principal signatures may be enabled to provide non-repudiation: proof that the principal saw the disclosure after the fact.

---

## Acceptance Criteria

1. **Every disclosure appends:** No silent denials. Counterparty requests yes/no/error → disclosure record appended.
2. **Disclosures are chained:** Each disclosure record is part of the hash chain in user_state.jsonl; tampering breaks the chain.
3. **Atomicity:** Proof generation and record append are atomic. If append fails, proof is destroyed.
4. **Auditability:** Principal can query disclosure records by counterparty, predicate, time window, and outcome.
5. **No metadata leakage to counterparties:** Disclosure records are never disclosed to counterparties; requests about other counterparties' relationships are rejected.
6. **Consent traceability:** Every disclosure record references the consent record (seq) that authorized it, enabling revocation audits.

---

— Calm, 2026-05-20
