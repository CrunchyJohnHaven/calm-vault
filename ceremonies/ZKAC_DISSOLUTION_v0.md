# Calm Witness — ZKAC Dissolution Ceremony & Receipts v0 (S262)

## Trigger Conditions

A ZKAC enters dissolution phase upon satisfaction of any trigger condition defined in the collective's charter. Standard triggers (per S160):

- **Membership supermajority vote**: ≥2/3 of members vote to dissolve, recorded on-chain within charter-specified voting window.
- **Charter expiration**: ZKAC operational period ends; dissolution executes automatically unless renewal quorum votes to extend (S154).
- **Founder-successor failure**: Designated successor (if any) fails to assume governance role within 30 days of founder departure; dissolution defaults unless alternate succession chain activates.
- **Insolvent pool state**: Pooled-asset commitments fall below operational minimum threshold; charter may allow emergency dissolution.

Trigger event must be signed by quorum-weighted authority (governance keypair or member threshold signature) and recorded as a dissolution-initiation record on the ZKAC's chain.

## Dissolution Event Record

The dissolution event establishes the immutable record of dissolution initiation and state at cutoff:

```
{
  "ceremony_type": "ZKAC_DISSOLUTION",
  "zkac_id": "<collective-identity-hash>",
  "trigger_condition": "<enum: vote|expiration|successor_failure|insolvency>",
  "trigger_timestamp": "<ISO8601-UTC>",
  "trigger_authority": "<quorum-signature>",
  "charter_ref": "<S160-charter-hash>",
  "final_member_roster": [<member-pubkeys>],
  "final_pool_state": "<commitment-snapshot-hash>",
  "settlement_cutoff": "<timestamp-of-finality>",
  "dissolution_record_hash": "<blake3-hash-of-this-record>"
}
```

This record is appended to the ZKAC's chain as the final non-archival entry. No further transactions post-dissolution.

## Settlement Receipts

Each member receives a per-member settlement receipt documenting their final stake, distributions, and exit proofs. Receipt schema (per S163):

```
{
  "receipt_id": "<blake3(member_pubkey || zkac_id || dissolution_timestamp)>",
  "member_pubkey": "<member's-ed25519-public-key>",
  "zkac_id": "<collective-identity-hash>",
  "member_entry_block": "<block-height-member-joined>",
  "member_exit_block": "<block-height-dissolution-finalized>",
  "commitment_stake_settled": "<commitment-amount-in-base-units>",
  "reward_share": "<earned-distribution-from-collective-pool>",
  "total_settlement": "<commitment_stake + reward_share>",
  "settlement_address": "<target-settlement-account-or-pubkey>",
  "settlement_proof": "<zero-knowledge-proof-of-correct-distribution>",
  "member_signature": "<member-attestation-of-receipt>",
  "issued_timestamp": "<ISO8601-UTC>",
  "receipt_hash": "<blake3-of-this-receipt>"
}
```

Member signs receipt after verification, proving acknowledgment and preventing disputes. Receipt is immutable once signed.

## Pooled-Asset Distribution

Pooled commitments are distributed per charter rules (S165), typically in order of priority:

1. **Operational debt settlement**: Liabilities, member loans, external obligations first.
2. **Pro-rata member return**: Remaining pool distributed proportionally to each member's stake-weighted commitment period.
3. **Charter-defined reserves**: If charter specifies retained reserves (e.g., insurance, successor fund), those are set aside before distribution.
4. **Residual charity or burn**: Any unallocated balance follows charter burn rule (e.g., public address, foundation donation, or destruction proof).

Distribution order and percentages are recorded in the dissolution event record and certified via the pooled-asset-distribution ledger, a secondary chain of settlement transactions keyed to each receipt_id.

## Chain Archival

Upon all members signing their settlement receipts (or timeout threshold), the ZKAC chain is archived per S166:

- **Chain state snapshot**: Final chain height, all committed blocks, state root hash.
- **Merkle commitment**: Recursive hash of all blocks from genesis to dissolution, committed to a read-only archive ledger (ZKAC Archive Register).
- **Archive storage**: Chain encoded as deterministic serialization (JSON-LD or CBOR), stored in immutable external registry (e.g., Arweave, timestamped Git tag).
- **Archive proof**: Cryptographic proof of chain integrity (e.g., Merkle tree root, timestamp certificate).

No new transactions can be posted to the archived chain. Archive location and hash are recorded in the public-identity tombstone.

## Public-Identity Tombstone

Upon successful archival, the ZKAC's public identity (its registered pubkey/handle) is marked with a tombstone record:

```
{
  "zkac_handle": "<collective-public-name>",
  "zkac_pubkey": "<collective-governance-keypair-public>",
  "status": "dissolved",
  "dissolution_timestamp": "<ISO8601-UTC>",
  "chain_archive_hash": "<blake3-of-archived-chain>",
  "chain_archive_location": "<URI-to-archive-storage>",
  "settlement_receipt_index": "<URI-to-member-receipt-registry>",
  "charter_final_hash": "<S160-charter-hash-at-dissolution>",
  "successor_collective": "<pubkey-of-successor-if-migrated>",
  "tombstone_hash": "<blake3-of-this-tombstone>"
}
```

Tombstone is published on the ZKAC's designated identity ledger (read-only after issuance), preventing resurrection or impersonation. All future inquiries about the ZKAC resolve to this tombstone.

## Cross-References

- **S154**: Charter and operational governance; expiration-renewal rules.
- **S160**: Voting semantics and supermajority quorum thresholds.
- **S163**: Member receipt format and cryptographic attestation.
- **S165**: Pooled-asset accounting and settlement distribution rules.
- **S166**: Chain archival, immutability proofs, and archive semantics.

---

**Ceremony author:** Calm  
**Date:** 2026-05-20  
**Version:** v0  
**Status:** Specification Draft
