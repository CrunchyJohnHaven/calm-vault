# Everest 33: Corruption Recovery Procedure

**Status:** BAGGED 2026-05-20  
**Author:** Musk  
**Tag:** E33: corruption-recovery — chain-recovery-from-sigsum-heads  

---

## Executive Summary

Everest 33 defines a complete recovery protocol for blockchain chain corruption scenarios. When local chain state is destroyed or corrupted but Sigsum transparent log heads remain intact and at least one replica survives, the chain can be authoritatively re-derived. This document specifies the end-to-end recovery procedure, cryptographic verification, and failure mode handling.

**Acceptance Criterion:** Local chain destroyed but Sigsum has heads and one replica survives → chain can be re-derived with cryptographic proof of correctness.

---

## 1. Recovery Architecture Overview

### 1.1 System Components

| Component | Role | Criticality |
|-----------|------|-------------|
| **Sigsum Heads** | Transparent log append-only heads (commitment to chain history) | Critical |
| **Replica Storage** | Surviving blockchain state (JSONL format) | Critical |
| **Inclusion Proofs** | Merkle/commitment proofs linking replica to Sigsum head | Critical |
| **Verification Engine** | Reconstructs chain and validates against proofs | Critical |
| **Recovery Orchestrator** | Coordinates extraction, verification, rebuild | Supporting |

### 1.2 Recovery Workflow

```
Corruption Detected
    ↓
Checkpoint Sigsum Head (T_head)
    ↓
Query Replica (JSONL snapshot)
    ↓
Generate Inclusion Proofs
    ↓
Rebuild Chain State
    ↓
Verify Against Proofs
    ↓
Integrate & Resume
```

---

## 2. Sigsum Head Extraction & Commitment

### 2.1 Head Retrieval Protocol

**Sigsum Head Structure:**
```json
{
  "timestamp": "2026-05-20T12:49:00Z",
  "tree_size": 487923,
  "root_hash": "0x7f3a9c8e2d5b1f4a9e3c7d2f1a8b5c3d9e7f1a8b",
  "signature": "ed25519_signature_hex",
  "key_hash": "0xabcdef123456",
  "signer_id": "sigsum-witness-primary"
}
```

**Extraction Steps:**
1. Connect to Sigsum witness nodes (minimum 3 quorum)
2. Request latest STH (Signed Tree Head) for chain namespace
3. Validate signature chain: witness → aggregate → threshold (2-of-3)
4. Extract tree_size and root_hash as recovery checkpoint
5. Archive head with metadata for audit trail

**Pseudo-Code:**
```python
def fetch_sigsum_head():
    heads = []
    for witness in SIGSUM_WITNESSES:
        head = fetch_from_witness(witness)
        if validate_signature(head.signature, head.key_hash):
            heads.append(head)
    
    # Consensus: all heads must match (tree_size, root_hash)
    canonical_head = deduplicate_and_validate(heads)
    return {
        "tree_size": canonical_head.tree_size,
        "root_hash": canonical_head.root_hash,
        "timestamp": canonical_head.timestamp,
        "checkpoint_id": hash(canonical_head)
    }
```

### 2.2 Head Commitment Guarantees

- **Append-Only:** tree_size cannot decrease
- **Cryptographic Binding:** root_hash commits to all historical entries
- **Witness Consensus:** Multiple independent signers attest to identical state
- **Timestamp Lock:** No retroactive modifications to historical heads

---

## 3. Replica State Extraction

### 3.1 Replica Identification & Validation

**Replica Criteria:**
- JSONL format (one JSON object per line, newline-delimited)
- Timestamps within chain's operational window
- Transaction signatures valid under active keys
- No logical gaps in sequence numbers
- Consistent merkle path to root hash

**Extraction Procedure:**
```python
def extract_replica_state():
    replica_candidates = []
    
    # Scan all backup locations
    for location in REPLICA_LOCATIONS:
        snapshot = load_jsonl(location)
        
        # Validate structure
        if validate_jsonl_format(snapshot):
            entry_count = count_entries(snapshot)
            last_entry = snapshot[-1]
            
            replica_candidates.append({
                "location": location,
                "entry_count": entry_count,
                "last_hash": last_entry["state_root"],
                "timestamp": last_entry["timestamp"],
                "validation_score": score_replica(snapshot)
            })
    
    # Select highest-quality replica
    best_replica = max(replica_candidates, key=lambda x: x["validation_score"])
    return load_jsonl(best_replica["location"])
```

### 3.2 Replica Consistency Checks

**Pre-Recovery Validation:**

1. **Sequence Integrity:**
   - No missing sequence numbers
   - No duplicates
   - Monotonic timestamp increase (allow ≤1s clock skew)

2. **Cryptographic Continuity:**
   - Each entry's `parent_hash` matches previous entry's `state_hash`
   - All transaction signatures validate
   - Merkle tree rooted at final entry

3. **Cardinality Bounds:**
   - Entry count ≤ Sigsum tree_size
   - Timestamp of last entry ≤ Sigsum checkpoint timestamp
   - Entry count ≥ 80% of Sigsum tree_size (≥80% coverage)

---

## 4. Inclusion Proof Generation & Verification

### 4.1 Merkle Proof Structure

**Proof Components:**
```json
{
  "entry_index": 487822,
  "leaf_hash": "0xf8d7a3c2b1e9f4d3a2c1b8e9f7d6c5b4a3e2f1d0",
  "tree_size": 487923,
  "merkle_path": [
    "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
    "0x0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9",
    "0x9b8a7c6d5e4f3a2b1c0d1e2f3a4b5c6d7e8f9a0"
  ],
  "tree_size_at_proof_generation": 487923,
  "leaf_node_type": "transaction_entry"
}
```

### 4.2 Proof Generation Algorithm

**For each replica entry:**

```python
def generate_inclusion_proof(entry_index, tree_size, entries):
    """
    Generate a Merkle inclusion proof for entry at entry_index
    in a tree of size tree_size.
    """
    leaf_hash = merkle_hash(entries[entry_index])
    merkle_path = []
    
    # Compute path from leaf to root
    node_index = entry_index
    subtree_size = 1
    
    while subtree_size < tree_size:
        if node_index % 2 == 0:
            # Left child: sibling is right
            sibling_index = node_index + subtree_size
            if sibling_index < tree_size:
                merkle_path.append(compute_subtree_hash(sibling_index, subtree_size))
        else:
            # Right child: sibling is left
            sibling_index = node_index - subtree_size
            merkle_path.append(compute_subtree_hash(sibling_index, subtree_size))
        
        node_index //= 2
        subtree_size *= 2
    
    return {
        "entry_index": entry_index,
        "leaf_hash": hex(leaf_hash),
        "merkle_path": [hex(h) for h in merkle_path],
        "tree_size": tree_size
    }
```

### 4.3 Inclusion Proof Verification

**Verification Steps:**

```python
def verify_inclusion_proof(proof, sigsum_root_hash, entries):
    """
    Verify that proof.entry_index is included in sigsum_root_hash.
    """
    # Step 1: Recompute leaf hash
    computed_leaf = merkle_hash(entries[proof["entry_index"]])
    if computed_leaf != proof["leaf_hash"]:
        return False, "Leaf hash mismatch"
    
    # Step 2: Verify merkle path to root
    current_hash = computed_leaf
    node_index = proof["entry_index"]
    subtree_size = 1
    
    for sibling_hash in proof["merkle_path"]:
        if node_index % 2 == 0:
            current_hash = merkle_combine(current_hash, sibling_hash)
        else:
            current_hash = merkle_combine(sibling_hash, current_hash)
        
        node_index //= 2
        subtree_size *= 2
    
    # Step 3: Compare with Sigsum root
    if current_hash == sigsum_root_hash:
        return True, "Proof verified"
    else:
        return False, "Root hash mismatch"
```

---

## 5. Chain Reconstruction from Replica

### 5.1 Reconstruction Pipeline

**Input:** Validated replica JSONL + Inclusion proofs  
**Output:** Reconstructed blockchain state ready for integration

**Process:**

```python
def reconstruct_chain(replica_entries, inclusion_proofs, sigsum_head):
    """
    Reconstruct blockchain state from replica entries and proofs.
    """
    reconstructed_chain = {
        "entries": [],
        "state_root": None,
        "merkle_proofs": {},
        "recovery_metadata": {
            "source": "replica",
            "recovery_timestamp": now(),
            "sigsum_head_checkpoint": sigsum_head.checkpoint_id,
            "replica_entry_count": len(replica_entries),
            "verification_status": "pending"
        }
    }
    
    # Phase 1: Load and canonicalize entries
    for idx, entry in enumerate(replica_entries):
        canonical_entry = {
            "sequence": entry.get("sequence", idx),
            "timestamp": entry["timestamp"],
            "transactions": entry["transactions"],
            "parent_hash": entry.get("parent_hash", "0x0"),
            "state_hash": merkle_hash(entry),
            "signature": entry.get("signature")
        }
        
        # Validate entry structure
        if not validate_entry(canonical_entry):
            return None, f"Entry {idx} failed validation"
        
        reconstructed_chain["entries"].append(canonical_entry)
    
    # Phase 2: Link entries
    for i in range(1, len(reconstructed_chain["entries"])):
        reconstructed_chain["entries"][i]["parent_hash"] = \
            reconstructed_chain["entries"][i-1]["state_hash"]
    
    # Phase 3: Compute final state root
    final_entry = reconstructed_chain["entries"][-1]
    reconstructed_chain["state_root"] = final_entry["state_hash"]
    
    # Phase 4: Attach proofs
    for proof in inclusion_proofs:
        reconstructed_chain["merkle_proofs"][proof["entry_index"]] = proof
    
    return reconstructed_chain, "Reconstruction complete"
```

### 5.2 State Consistency Validation

**Checks:**

1. **Merkle Tree Integrity:**
   - All parent_hash → state_hash links valid
   - Final root matches Sigsum root_hash

2. **Transaction Validity:**
   - All transaction signatures valid
   - No double-spends
   - Account balances consistent

3. **Timeline Consistency:**
   - No timestamp reversions (except clock corrections ≤1s)
   - No future timestamps beyond system clock + 5s

---

## 6. Verification Steps

### 6.1 Multi-Layer Verification

**Layer 1: Cryptographic Verification**
```python
def verify_cryptographic_integrity(chain, sigsum_head):
    # Verify Sigsum commitment
    final_root = chain["state_root"]
    if final_root != sigsum_head.root_hash:
        return False, "Root hash mismatch vs Sigsum"
    
    # Verify all inclusion proofs
    for idx, proof in chain["merkle_proofs"].items():
        is_valid, msg = verify_inclusion_proof(proof, sigsum_head.root_hash, chain["entries"])
        if not is_valid:
            return False, f"Proof failed for entry {idx}: {msg}"
    
    return True, "Cryptographic verification passed"
```

**Layer 2: State Machine Validation**
```python
def verify_state_machine(chain):
    # Rebuild state by applying all transactions
    state = {}
    
    for entry in chain["entries"]:
        for tx in entry["transactions"]:
            state = apply_transaction(state, tx)
            if state is None:
                return False, f"Invalid transaction in entry {entry['sequence']}"
    
    return True, "State machine validation passed"
```

**Layer 3: Consensus Verification**
```python
def verify_consensus_formation(chain):
    # Verify BFT consensus signatures on critical checkpoints
    consensus_checkpoints = [e for e in chain["entries"] if e.get("is_checkpoint")]
    
    for checkpoint in consensus_checkpoints:
        if not verify_multisig(checkpoint["signatures"], checkpoint["signers"]):
            return False, "Consensus signature verification failed"
    
    return True, "Consensus verification passed"
```

### 6.2 Verification Report

**Template:**
```json
{
  "verification_timestamp": "2026-05-20T13:00:00Z",
  "recovery_id": "rec-487923-a3f8",
  "results": {
    "cryptographic_integrity": { "status": "PASS", "details": "..." },
    "state_machine": { "status": "PASS", "details": "..." },
    "consensus_formation": { "status": "PASS", "details": "..." },
    "replica_completeness": { "status": "PASS", "percentage": 99.8 },
    "sigsum_head_alignment": { "status": "PASS", "details": "..." }
  },
  "overall_status": "APPROVED_FOR_INTEGRATION",
  "signed_by": "recovery_verifier_node_1",
  "signature": "..."
}
```

---

## 7. Integration & Resumption

### 7.1 Safe Resumption Protocol

**Pre-Resumption Checklist:**

- [ ] All verification layers pass
- [ ] Recovery ID registered in audit log
- [ ] Backup of corrupted state archived
- [ ] Peer nodes notified of recovery state
- [ ] Consensus checkpoint created
- [ ] Emergency rollback snapshot preserved

**Integration Steps:**

```python
def integrate_recovered_chain(recovered_chain, verification_report):
    """
    Atomically integrate recovered chain state.
    """
    if verification_report["overall_status"] != "APPROVED_FOR_INTEGRATION":
        raise RecoveryRejected("Verification failed")
    
    # Step 1: Atomic state swap
    with atomic_transaction():
        backup_current_state()
        load_chain_state(recovered_chain)
        update_recovery_metadata(verification_report)
        increment_recovery_epoch()
    
    # Step 2: Notify network
    broadcast_recovery_event({
        "recovery_id": verification_report["recovery_id"],
        "new_head": recovered_chain["state_root"],
        "chain_height": len(recovered_chain["entries"])
    })
    
    # Step 3: Resume consensus
    resume_consensus()
    
    return {"status": "INTEGRATED", "recovery_id": verification_report["recovery_id"]}
```

---

## 8. Failure Modes & Recovery Actions

### 8.1 Failure Mode Catalogue

| Failure Mode | Trigger | Mitigation | Outcome |
|--------------|---------|-----------|---------|
| **Sigsum Head Mismatch** | Witness disagreement >50% | Escalate to witness oversight committee | Halt recovery; manual intervention |
| **Replica Corruption** | >20% entries fail validation | Query additional replicas; use consensus pick | Try next-best replica |
| **Merkle Path Invalid** | Inclusion proof verification fails | Check proof generation algorithm | Mark entry as unverifiable; audit trail |
| **Root Hash Divergence** | Reconstructed root ≠ Sigsum root | Verify replica completeness; check timestamp alignment | Reject recovery; require manual audit |
| **State Machine Violation** | Transaction validity check fails | Isolate offending transaction; inspect logs | Quarantine transaction; escalate |
| **Consensus Signature Missing** | Cannot verify BFT signatures | Check signer availability; retry with time window | Accept with reduced consensus confidence |
| **Timeline Inconsistency** | Timestamp reversions detected | Apply clock correction heuristics | Flag for manual review |
| **Replica Incompleteness** | Entry count <80% of Sigsum tree_size | Attempt multi-replica fusion | Defer recovery; wait for full replica |

### 8.2 Failure Recovery Logic

```python
def handle_recovery_failure(failure_type, context):
    """
    Route failures to appropriate escalation path.
    """
    escalation_map = {
        "SIGSUM_HEAD_MISMATCH": escalate_to_witness_committee,
        "REPLICA_CORRUPTION": query_additional_replicas,
        "MERKLE_PATH_INVALID": create_audit_trail,
        "ROOT_HASH_DIVERGENCE": reject_and_escalate,
        "STATE_MACHINE_VIOLATION": quarantine_and_escalate,
        "CONSENSUS_SIGNATURE_MISSING": reduce_confidence_flag,
        "TIMELINE_INCONSISTENCY": apply_clock_correction,
        "REPLICA_INCOMPLETENESS": defer_and_notify
    }
    
    handler = escalation_map.get(failure_type, escalate_to_witness_committee)
    return handler(context)
```

### 8.3 Manual Recovery Procedures

**When Automated Recovery Fails:**

1. **Witness Committee Review:** Present all recovery data to committee
2. **Replica Forensics:** Deep analysis of replica corruption pattern
3. **Sigsum Head Audit:** Verify witness signatures and quorum
4. **Consensus Reconstruction:** Manual consensus round with node majority
5. **Rollback Decision:** Decide between rollback or staged recovery

---

## 9. Audit Trail & Compliance

### 9.1 Recovery Event Log

**Required Entries:**
```json
{
  "event_type": "RECOVERY_INITIATED",
  "timestamp": "2026-05-20T13:00:00Z",
  "recovery_id": "rec-487923-a3f8",
  "sigsum_head": { "tree_size": 487923, "root_hash": "0x7f3a..." },
  "replica_source": "/data/blockchain/backup_20260520.jsonl",
  "entry_count": 487923,
  "verification_results": { ... },
  "integration_status": "APPROVED",
  "signed_by": "recovery_verifier_1",
  "signature": "ed25519_hex"
}
```

### 9.2 Compliance Checkpoints

- Recovery audit trail immutable for 7 years
- All verification reports retained with signatures
- Rollback decision logs maintained
- Sigsum head attestations archived

---

## 10. Testing & Validation

### 10.1 Recovery Simulation

**Test Scenarios:**
1. Corrupt 10%, recover, verify
2. Corrupt 50%, recover, verify
3. Corrupt with Sigsum head divergence, verify rejection
4. Recover with only 80% replica coverage
5. Recovery with consensus signature gaps

**Test Harness:**
```python
def test_recovery_scenario(corruption_level, sigsum_divergence=False):
    # Generate baseline chain
    baseline = generate_chain(tree_size=100000)
    
    # Corrupt state
    corrupted = corrupt_chain(baseline, corruption_level)
    
    # Initiate recovery
    recovered = recovery_from_sigsum_and_replica(
        sigsum_head=baseline.sigsum_head,
        replica=corrupted
    )
    
    # Verify
    assert recovered.state_root == baseline.state_root
    return "PASS"
```

---

## Appendix: Configuration Reference

**Environment Variables:**
```bash
SIGSUM_WITNESSES="witness1.example.com,witness2.example.com,witness3.example.com"
SIGSUM_QUORUM_SIZE=2
REPLICA_LOCATIONS="/data/blockchain/primary,/data/blockchain/backup,/data/blockchain/cache"
RECOVERY_TIMEOUT_SECONDS=300
MERKLE_PROOF_DEPTH_MAX=32
REPLICA_COVERAGE_MIN_PERCENT=80
CONSENSUS_CONFIDENCE_THRESHOLD=0.66
```

---

**End of Recovery Procedure**

*This specification is locked at 2026-05-20 and requires CALM consensus for any updates.*
