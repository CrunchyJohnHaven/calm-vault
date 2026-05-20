# Everest 33 — Corruption Recovery

*Phase III — Self-Report Substrate. Prereq: Everest 30, 32.*

## Acceptance Criterion

If the local chain is destroyed but Sigsum has the heads and at least one encrypted replica survives, the chain can be re-derived. The vault operator recovers full cryptographic continuity without re-enrollment, as long as identity proofs and historical chain heads remain publicly verifiable.

## Failure Scenarios In Scope

**S1: Local Corruption (Partial Write)**
The user_state.jsonl file is corrupted—a mid-write fsync gap, filesystem damage, or sector fault—leaving trailing records unreadable or logically inconsistent.

**S2: Total Vault Deletion**
The entire local vault directory is removed (accidental rm -rf, file manager deletion, system reset).

**S3: Hardware Loss**
The device containing the vault is stolen, destroyed by fire, or physically lost. A complete bootstrap is required on new hardware.

**S4: Dual Loss (Key + Chain)**
Both the encryption key (master.priv.enc) and the local chain are lost or corrupted beyond recovery. No replica is accessible. This is catastrophic and requires a new enrollment ceremony.

**S5: Silent Chain Mutation**
A single record in the chain is silently corrupted or rewritten—detected by the verify-chain command, which identifies the first invalid record and its cryptographic mismatch.

**S6: Sigsum Operator Offline**
The primary transparency log operator goes offline permanently with no recovery window. Recoverability depends on multi-log redundancy (E93).

## Recovery Preconditions

Successful recovery of scenarios S1–S5 requires resources external to the lost or corrupted vault:

1. **Principal's Age Private Key**: Held in the principal's memory, passphrase, or optional hardware token (e.g., Yubikey). Never stored in the vault itself.
2. **Encrypted Replica**: At least one encrypted copy of the vault, stored on USB or in cloud (per Everest 32). Encrypted with the master key, decryptable only by the principal.
3. **Sigsum Log Inclusion Proofs**: Publicly retrievable chain head attestations and membership proofs from the transparency log.
4. **Witness Attestations**: Enrollment-time signatures from the witness network (CredexAI infrastructure), verifiable against the principal's public key.

## Recovery Procedures

### S1: Single-Record Corruption

```
calm-witness recover --from-replica usb1
```

The vault operator detects a corrupt record via verify-chain. The recovery command:
1. Decrypts the USB replica using the principal's master key.
2. Re-verifies the entire chain, confirming all records except the corrupt one are valid.
3. Applies a single-record diff to the local state, replacing the bad record with its replica copy.
4. Restarts the vault's background Sentinel process.

**Time**: <30 seconds for chains with <1000 records.

### S2: Whole-Vault Loss (Deletion)

```
calm-witness recover --bootstrap
```

The vault directory has been deleted entirely. Recovery:
1. Pulls the latest encrypted replica from USB or cloud.
2. Decrypts the replica using the principal's master key.
3. Verifies the entire chain end-to-end against Sigsum inclusion proofs.
4. Restores the decrypted vault to the standard local path.
5. Restarts the Sentinel background process and resumes normal operation.

**Time**: <2 minutes, including replica decryption and verification.

### S3: Hardware Loss (Device Theft or Destruction)

On new hardware, the operator:
1. Installs calm-witness from a trusted package repository.
2. Runs `calm-witness recover --bootstrap`, providing the master key passphrase.
3. Restores the vault from the off-site USB replica, which is decrypted and verified.
4. Proves identity continuity by signing a recovery attestation with the principal's age key (Everest 68).
5. Submits the attestation to the witness network for inclusion in the chain.

The recovered vault is cryptographically identical to the lost one, and the identity proof prevents impersonation by anyone who lacks the age key.

### S4: Catastrophic Loss (Key + Chain Unrecoverable)

This scenario cannot be recovered within the existing chain. Recovery requires:
1. A new enrollment ceremony (Everest 29), establishing a fresh genesis record.
2. A new chain ID and initial chain head.
3. The old chain remains in Sigsum as a historical record, forever unmodified.

To establish continuity with the old chain:
- The new genesis record MAY include a `predecessor_chain` field pointing to the last known-good head of the old chain.
- Verifiers can follow the predecessor pointer for historical context.
- Verifiers are advised to treat the new chain as a fresh start but may accept a transition window (e.g., 7 days) before trusting high-stakes proofs over the new chain.

The old chain serves as a "tombstone chain"—a public immutable record of the operator's historical identity, even though it can no longer be extended or modified.

### S5: Chain Mutation (Silent Corruption)

A record in the middle of the chain is silently mutated (bit flip, malicious edit) but remains syntactically valid. The verify-chain command detects the corruption:

```
calm-witness verify-chain --find-first-bad-record
```

Recovery:
1. The tool identifies the first corrupted record and its offset.
2. The operator walks the Sigsum log backward from the present to locate the last known-good chain head before the corruption occurred.
3. The replica is decrypted; if it contains the pre-corruption state, the chain is restored from the replica up to the last-good head.
4. The vault state is truncated at the last-good head.
5. All records after the corruption point are discarded as untrusted.

**Time**: <5 minutes for a typical chain, including Sigsum traversal.

### S6: Sigsum Operator Offline

If the primary log operator is permanently offline, recovery depends on multi-log redundancy. Per Everest 93, the vault commits chain heads to N≥3 independent logs. Loss of a single log is recoverable via the others:

1. The recovery tool detects the primary log is unreachable.
2. It queries the redundant logs and assembles the complete set of chain heads from the others.
3. Inclusion proofs are reconstructed from the available logs.
4. Recovery proceeds normally via S2 or S5 procedures.

If all N logs are lost, the chain cannot be recovered.

## Identity Continuity Proofs

After any recovery (S1–S5), the operator generates a chain record of kind `recovery.completed`:

```json
{
  "kind": "recovery.completed",
  "timestamp": "2026-05-20T14:32:00Z",
  "payload": {
    "recovery_scenario": "S2",
    "original_chain_head_at_loss": "head:abc123...",
    "recovered_chain_head": "head:def456...",
    "replica_used": "usb-encrypted-2026-05-15",
    "witness_signatures": [
      "witness:credex-ai-1:sig...",
      "witness:credex-ai-2:sig..."
    ]
  },
  "principal_signature": "sig:age-key:..."
}
```

The record is signed with the principal's age key and distributed to all witnesses. Counterparties verifying proofs over the recovered chain may:
- Inspect the recovery.completed record.
- Verify the principal's signature.
- Optionally require a transition window (e.g., 7 days) before accepting high-stakes proofs from a recovered vault.

This prevents impersonation: an attacker cannot recover the vault without the principal's age key.

## Tombstone Chain Pattern

When a chain is abandoned (e.g., S4), the old chain heads remain immutably in Sigsum. A new chain starts with a fresh genesis:

```json
{
  "kind": "genesis",
  "chain_id": "chain:xyz789...",
  "predecessor_chain": "chain:old-id-abc123...",
  "principal_public_key": "pk:age-key:...",
  "witness_set": [...]
}
```

The `predecessor_chain` field allows verifiers to:
- Follow the predecessor pointer to the old chain's last head.
- Inspect the old chain's full history and attestations.
- Make an informed decision on whether to trust the new chain as a legitimate continuation.

A verifier might accept the new chain immediately (trusting the principal's judgment), or require additional evidence (e.g., a witness signature affirming the transition).

## Operator-Side Recovery Tooling

**calm-witness recover --diagnose**
Auto-detects which scenario (S1–S6) applies. Inspects the vault, Sigsum, and replicas to determine the recovery path.

**calm-witness recover --interactive**
Guided recovery wizard. Prompts the principal for the master key passphrase, replica location, and age key confirmation. Suitable for non-technical operators.

**calm-witness recover --rebuild-from-sigsum**
For partial chains (e.g., when the replica is incomplete), walks the transparency log forward from a known chain head, reconstructing missing records from Sigsum's stored ledger.

## Verification of Recovered Chain

After recovery, the operator must verify the entire chain:

1. **Full Verify**: `calm-witness verify-chain` on the restored data.
2. **Sigsum Cross-Check**: Every chain head must appear in Sigsum; verify inclusion proofs match.
3. **Roughtime Anchors**: Verify all Roughtime anchor signatures against NTP sources (Everest 31).
4. **Operator Identity Binding**: Verify the recovery.completed record is signed with the principal's age key (Everest 68).

If any verification fails, the recovery is aborted and the operator must retry with a different replica or contact the witness network.

## Threat Model

**Adversary Deletes Local Vault to Force a Recovery They Can Intercept**
Defeated by encrypted replicas and age-key custody. Without the principal's master key and age key, the adversary cannot decrypt the replica or create a valid recovery.completed record.

**Adversary Submits a Forged Recovery Claim**
Defeated by principal-key signature on the recovery.completed record. Any recovery claim without a valid signature is rejected by verifiers.

**Adversary Forces Principal to Recover to a Fork They Control**
Defeated by Sigsum inclusion proofs. A forked chain cannot reproduce the inclusion proofs for the chain heads the principal expects. When the principal runs recovery, they verify that recovered heads appear in the public Sigsum log—a fork remains invisible to Sigsum and is detected immediately.

**Adversary Corrupts the Replica**
If the replica is encrypted, the principal's master key is required to decrypt it. If the replica is stored in cloud and becomes corrupted, a secondary USB replica (recommended in Everest 32) can be used. If all replicas are lost, recovery falls back to S6 (Sigsum only) or fails.

## Performance Targets

- **S1 (Single-record corruption)**: <30 seconds.
- **S2 (Whole-vault loss)**: <2 minutes.
- **S5 (Chain mutation)**: <5 minutes.

Performance varies with chain size, network latency to Sigsum, and replica access time (USB vs. cloud).

## Principal Documentation

A one-page "what to do if your laptop dies" runbook should be provided to every vault operator:

1. Locate the off-site USB replica (stored in a safe-deposit box).
2. Recover the passphrase to the master key from memory.
3. On new hardware, install calm-witness.
4. Run `calm-witness recover --interactive`.
5. Provide the passphrase when prompted.
6. The recovered vault will be verified against Sigsum automatically.
7. Confirm that the recovery.completed record is correct (shows your age key signature).
8. Resume normal operation.

This runbook should be printed and stored alongside the USB replica.

## Cross-References

- **E28**: Chain head publication and signing.
- **E29**: Genesis and chain creation.
- **E30**: Chain publication to Sigsum (prereq).
- **E32**: Encrypted replica creation and storage (prereq).
- **E20**: Witness attestations and enrollment.
- **E68**: Operator identity binding and age-key signatures.
- **E93**: Multi-log redundancy for Sigsum.
- **E31**: Roughtime anchoring (referenced in verification).

---

— Calm, 2026-05-20