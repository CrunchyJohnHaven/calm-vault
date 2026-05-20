# Everest 30 — Chain-Head Publication to Sigsum

*Phase III — Self-Report Substrate. Prereq: Everest 28.*

## Introduction

Everest 28 established the hash-chain verifier—a mechanism to prove that a record exists in a principal's append-only user_state.jsonl and has not been tampered with since insertion. That verifier, however, assumes a single copy of the chain stored on disk. An adversary with one-time physical access (or malware running with full process capability) can rewrite the disk, alter the chain, recompute hashes backward to the genesis block, and serve a forged chain that passes local verification. Everest 29 anchored the genesis block to a high-entropy external source. Everest 30 closes the gap by anchoring every new chain head to a cryptographically append-only transparency log, making the entire chain tamperproof under any single-disk attacker.

This document specifies chain-head publication to Sigsum—a minimalist, standards-based transparency log—and defines the architecture, failure modes, and verification protocol for Phase III of Calm Witness.

## What Is Sigsum

Sigsum is an open protocol standard (sigsum.org) for transparency logs. A Sigsum log maintains an append-only merkle tree of leaves (each leaf representing a submission). When a client submits a new leaf, the log produces a *signed tree head* (STH)—a cryptographic commitment to the tree at that moment—cosigned by independent *witnesses*. Clients verify inclusion by requesting an *inclusion proof* (path through the merkle tree from the new leaf to the current tree root) and checking that the proof is consistent with the STH. The log cannot retroactively remove or reorder leaves, and witnesses refuse to cosign conflicting STHs (e.g., two different tree roots at the same tree size), detecting split-view attacks where a malicious log tries to show different histories to different clients. Because witnesses are independent third parties with no operational stake in the log, they provide a strong tamper-evident signal: if the log ever tries to fork, at least one witness will publish a conflicting STH, creating cryptographic proof of misbehavior.

## Sigsum vs. Alternatives

**Certificate Transparency (CT).** CT is the de facto standard transparency log, used to detect mis-issued X.509 certificates. Its protocol is more complex, optimized for the certificate ecosystem (certificate chains, revocation, issuance timestamps). Sigsum strips away certificate-specific logic and offers a general-purpose tree-head submission model that fits any append-only log. For Calm Witness, Sigsum's simplicity is an advantage: we can implement the verifier in a few hundred lines of code.

**Trillian.** Google's Trillian is a reference implementation of a transparency log using the merkle tree construction that underpins both CT and Sigsum. Trillian is feature-rich and battle-tested, but it is an implementation, not a standard. Sigsum is the minimal spec that captures the essential security properties. For v0, we target the Sigsum spec and can use either the Trillian backend (via a Sigsum-compatible API) or other spec-compliant implementations.

**Blockchain Anchoring (Bitcoin OP_RETURN, Ethereum calldata, etc.).** Blockchain-based timestamping and anchoring has appeal because the ledger is globally distributed. However, it incurs per-anchor costs (transaction fees, gas), slower finality (confirmations), and long-term protocol dependence (what happens if Bitcoin changes its OP_RETURN rules?). Sigsum is purpose-built for transparency logs and requires only HTTPS connectivity; witnesses are cheap to run and operate independently.

## Architecture

### Submission Protocol

Each time a new record is appended to user_state.jsonl, the principal computes a new chain head H_n as the sha256 hash of the entire jsonl (or more precisely, the hash committed in the latest record's `chain_root` field, which is the hash of all prior records). The principal then submits H_n to one or more Sigsum logs:

1. **Construct the submission leaf.** The leaf includes:
   - The chain head H_n (32 bytes).
   - Metadata: principal public key, namespace (e.g., "calm.witness/v0"), timestamp.
   - Principal-key signature over the leaf.

2. **HTTPS POST to log.** The principal sends the leaf to the Sigsum log's submission endpoint (e.g., `POST https://log.example.com/add-leaf`).

3. **Receive STH + inclusion proof.** The log verifies the signature, appends the leaf, and returns:
   - A signed tree head (STH) containing the new root hash, tree size, and timestamp.
   - An inclusion proof: the path of hashes from the new leaf to the root.
   - The STH is cosigned by each witness that has observed it.

4. **Store the anchor record.** The principal appends an anchor record to user_state.jsonl:
   ```json
   {
     "kind": "anchor.sigsum",
     "timestamp": "2026-05-20T12:34:56Z",
     "payload": {
       "h_anchored": "abc123...",
       "log_id": "log.example.com",
       "log_namespace": "calm.witness/v0",
       "leaf_index": 42,
       "sth": {
         "timestamp": "2026-05-20T12:34:56Z",
         "tree_size": 43,
         "root_hash": "def456..."
       },
       "sth_signature": "...",
       "witness_cosignatures": [
         { "witness_name": "witness-a.example.com", "signature": "..." },
         { "witness_name": "witness-b.example.com", "signature": "..." }
       ],
       "inclusion_proof": ["hash1", "hash2", ...]
     }
   }
   ```

5. **Index for fast lookup.** Write the anchor to a parallel index file `~/.calm-vault/anchors/<h_anchored>.json` to enable O(1) lookup without scanning jsonl.

### Multi-Log Redundancy

Relying on a single Sigsum log introduces a single point of failure. If the log becomes unavailable or is compromised, new anchors cannot be obtained, and verifiers downstream may reject proofs. To mitigate, Calm Witness publishes each chain head to N independent Sigsum logs, operated by different entities.

**Quorum Policy.** An anchor is considered "confirmed" when at least 2 of N logs have returned valid STHs and the principal has verified the inclusion proofs. This 2-of-N quorum ensures that:
- A single log operator cannot unilaterally censor or forge an anchor.
- A single log operator going offline does not halt the principal.
- An attacker must compromise or control 2 of N logs to forge a new anchor and evade detection.

**Log Selection (Everest 93).** Everest 93 specifies the criteria for selecting community-operated Sigsum logs and auditing them quarterly for correctness, witness responsiveness, and uptime.

### Witness Cosignature Requirement

Each Sigsum STH must be cosigned by at least W independent witnesses (W ≥ 2 for Phase III). A witness is a third party that monitors the log, cryptographically verifies each new STH, and signs a cosignature confirming that the STH is authentic and consistent with prior STHs it has witnessed.

**Why witnesses prevent split-view attacks.** Suppose a malicious log tries to show Client A that the tree root is `root_A` at tree size 100, and shows Client B a different root `root_B` at size 100. If both clients verify that the STH is cosigned by witness W, one of the following must be true:
1. W cosigned both `(root_A, 100)` and `(root_B, 100)`. This is a signing error; W has violated its protocol and can be publicly identified as misbehaving (provable equivocation).
2. W cosigned only one of them. Then the other client's STH is missing W's cosignature—it does not meet the W ≥ 2 threshold and is rejected.

Thus, witnesses convert a split-view attack into either a provable equivocation (strong evidence of compromise) or a failed verification (rejection of the fake STH).

## Failure Modes and Handling

**Network Unavailable at Anchor Time.** If the principal's network is offline when a new record is appended, the anchor submission cannot proceed immediately. The principal queues the submission and retries when connectivity returns. The chain itself proceeds without the anchor, but downstream verifiers may reject proofs over unanchored records (per the Verification section below). This is acceptable because:
- The verifier has the option to accept or reject unanchored proofs based on policy.
- Once the network returns, the queue is drained and anchors are obtained retroactively.

**Sigsum Log Offline.** If one or more logs in the N-log set become unavailable, the principal automatically fails over to the remaining logs. If fewer than 2 logs remain reachable, the principal enters "pending" state: it continues to queue submissions and retries as logs recover. The chain proceeds, but verifiers will not accept proofs as "confirmed" until the quorum is re-established.

**Split-View Detection.** If a Sigsum log returns two different STHs for the same tree size and namespace (e.g., `(root_A, size=100)` and `(root_B, size=100)`), the principal detects this discrepancy when comparing STHs across logs or when a witness refuses to cosign a new STH because it is inconsistent with a prior one. The principal emits an alert record:
   ```json
   {
     "kind": "anchor.split_view_detected",
     "timestamp": "2026-05-20T12:34:56Z",
     "payload": {
       "log_id": "log.example.com",
       "sth_1": { "root_hash": "abc...", "tree_size": 100 },
       "sth_2": { "root_hash": "def...", "tree_size": 100 },
       "witness_signature_missing": "witness-a.example.com"
     }
   }
   ```
   This alert is appended to user_state.jsonl and serves as cryptographic evidence of the attack attempt.

## Verification Protocol

A downstream verifier (e.g., an auditor, compliance system, or Calm Witness library consumer) accepts a proof that a record R exists in a principal's user_state.jsonl if:

1. **Chain-head proof exists.** The record R has an associated chain-head hash H_R (computed from all records up to and including R). There exists a chain-head anchor record in the same user_state.jsonl that references H_R.

2. **Anchor is in user_state.jsonl.** The anchor record (kind: "anchor.sigsum") is present in user_state.jsonl and is cryptographically bound to the principal (via the principal's public key and signature).

3. **Inclusion proof verifies.** The inclusion proof in the anchor record is checked against the STH's root hash. The verifier recomputes the path from the leaf (H_R) through the inclusion proof and confirms it equals the STH's root_hash.

4. **STH has sufficient witness cosignatures.** The STH is signed by the log operator and cosigned by at least W independent witnesses. The verifier checks each witness signature against the witness's public key (retrieved out-of-band, e.g., from a witness announcement). If fewer than W signatures are valid, the anchor is rejected.

5. **Anchor recency (optional policy).** Some verifiers may impose a time-based policy: anchors older than T days are rejected to detect long-term log compromise. This is orthogonal to the protocol but recommended for high-assurance applications.

If all checks pass, the verifier accepts the proof as "anchored at Sigsum log X" and can provide that as evidence to downstream users.

## Implementation Strategy

### Phase A (v0.1)

- Single Sigsum log (operated by Calm Witness or a trusted partner).
- Single witness.
- Synchronous submission on each append (blocking, with timeout fallback to queue).
- Sigsum-go bindings invoked as a subprocess; the calm-witness Rust core spawns a small Go process for each submission and parses the JSON response.

### Phase B (v0.2)

- Three independent Sigsum logs (N=3).
- Two independent witnesses per log (W=2).
- Quorum-2-of-3: an anchor is confirmed when at least 2 logs have returned valid, cosigned STHs.
- Async submission queue to avoid blocking the append path.

### Phase C (v1.0)

- Full dynamic log selection via Everest 93.
- Enhanced witness reliability monitoring.
- Integrated split-view detection and alerting.
- Batch submission to reduce log traffic during high activity.

### Client Library

The verifier (calm-witness library consumer) is implemented in Rust using the `sigsum` crate (if available) or via sigsum-go subprocess. The verifier exposes a simple API:

```rust
fn verify_anchor(
    user_state: &str,  // path to user_state.jsonl
    chain_head: &[u8],  // 32-byte hash
    anchor_record: &Anchor,  // anchor record from jsonl
) -> Result<VerificationStatus, VerificationError>
```

For each anchor record, the verifier:
1. Parses the STH and inclusion proof.
2. Recomputes the merkle path.
3. Checks witness cosignatures.
4. Returns `Verified` or `Rejected` with reason.

## Privacy Analysis

**What goes on the public Sigsum log.** Only the 32-byte chain head H_n and the principal's namespace and public key fingerprint. No user data, record contents, or metadata beyond the timestamp is published.

**What an observer learns.** An observer watching the Sigsum log sees a sequence of 32-byte hashes submitted by Calm operators. Without additional context (e.g., a leaked mapping of principals to public keys), the observer cannot link two hashes to the same principal.

**Side channel: activity rate.** An observer can infer the principal's activity level by counting anchor submissions per day. If a principal submits 10 anchors per day, the observer knows the principal is appending roughly 10 records per day (or fewer, if some days have no appends). Mitigation strategies (deferred to Everest 32 or later):
- Chaff anchors: periodically submit random hashes to obscure true activity.
- Hourly batching: defer submission until an hourly boundary, reducing timing resolution.

For v0, we accept the activity-level side channel as out-of-scope and document it clearly to users.

## Cross-References

- **Everest 28 (Chain Verifier).** Defines the hash-chain proof structure; Everest 30 extends it with Sigsum anchors.
- **Everest 29 (Genesis Block Provenance).** Anchors the starting block; Everest 30 anchors every head thereafter.
- **Everest 31 (Roughtime).** Adds verifiable time to Sigsum anchor records, preventing time-squashing attacks.
- **Everest 33 (Corruption Recovery via Replica).** Uses Sigsum anchors to detect and recover from disk corruption.
- **Everest 93 (Sigsum Operator Selection).** Specifies criteria for selecting and auditing community-operated logs.

## Deployment and Operational Burden

A Sigsum log can be run on modest hardware (e.g., a t3.micro cloud instance) and requires minimal maintenance: TLS certificates, log rotation, and periodic backups. However, operating a log is not free. Calm Witness v0 defaults to using one or more community-operated logs (e.g., a log run by a transparency-log advocacy organization or a consortium of Calm users). In exchange, we commit to quarterly audits (Everest 93) and publish audit results to ensure log correctness.

If no suitable community logs exist, a fallback is to operate our own log, either self-hosted or via a managed service. This adds operational overhead but gives Calm Witness full control over witness policies and availability.

## Conclusion

Everest 30 graduates Calm Witness from a hash chain on a single disk to a tamperproof, externally auditable record via Sigsum transparency logs. By anchoring every chain head to an append-only log cosigned by independent witnesses, the principal's state becomes resistant to offline disk attacks and detectable under online attacks. Combined with Everest 28 (chain proof) and Everest 29 (genesis anchor), the user_state.jsonl becomes a comprehensive, cryptographically verifiable audit log of every state transition.

The architecture is conservative: it does not require consensus, blockchain, or complex distributed protocols. Instead, it leverages a well-scoped transparency-log spec (Sigsum) and independent witnesses—a proven approach in certificate transparency and emerging in other domains. This keeps the implementation simple, the attack surface small, and the verification cost low.

— Calm, 2026-05-20
