# Everest 35 — Cross-Vault Aliasing

*Phase III — Self-Report Substrate. Prereq: Everest 22, 29.*

## Overview

A principal may move to a new operator—whether due to operational change, organizational sponsorship shift, or deliberate re-enrollment. The new operator provisions a fresh vault on the principal's hardware and must establish cryptographic continuity with the old vault so that counterparties can verify: "this is the same principal, duly transitioned to a new operator."

Cross-vault aliasing solves this via a signed handover protocol. The old operator and new operator exchange a HANDOVER_RECORD that binds the old chain's termination to the new chain's genesis. Both chains anchor this record (old marked `vault.handover_sent`; new marked `vault.handover_received`) so temporal ordering is tamper-evident.

Counterparties verify continuity by:
1. Checking the new vault's genesis record for `predecessor_handover`.
2. Cross-referencing and validating the HANDOVER_RECORD from the old chain.
3. Confirming the principal's continuity proof (old master.priv signature over new master.pub).
4. Optionally re-verifying against the old vault's final Sigsum anchor.

This enables seamless operator transitions while preserving the principal's cryptographic identity and the transparency of the transition itself.

## Use Case: Principal Operator Transition

A principal enrolled with Operator A and accumulated credentials, consent records, and audit history in Vault A. The principal now wishes to switch to Operator B.

Operator A is trustworthy but the principal prefers different operational characteristics, cost structure, or biometric re-enrollment. Operator B is provisioned with a new vault (Vault B) on the principal's hardware.

Without cross-vault aliasing, Vault B appears as a new, unrelated principal to all counterparties. Existing relationships, service agreements, and reputation are not portable. Cross-vault aliasing allows the principal to prove: "I controlled Vault A, I still control Vault B, and the transition was attested and authorized."

## Handover Protocol

### Phase 1: Setup and Initiation

1. Operator B creates Vault B on the principal's hardware (standard E29 genesis, with E22 CredexAI VC).
2. Principal initiates handover: `calm-witness handover --target /path/to/new/vault`
3. Old vault (Vault A) extracts:
   - `old_chain_head`: the final record hash of Vault A's chain
   - `old_master_pub`: the principal's public master key in Vault A
   - `old_operator_id`: Operator A's identifier
   - `old_credexai_vc_id`: the VC ID of Operator A's enrollment

### Phase 2: Handover Record Construction

Operator A constructs HANDOVER_RECORD:

```
{
  "kind": "vault.handover_record",
  "old_chain_head": "<hash>",
  "old_master_pub": "<key>",
  "old_operator_id": "<id>",
  "old_credexai_vc_id": "<vc_id>",
  "new_chain_head_seed_value": "<first_record_hash_of_vault_b>",
  "new_master_pub": "<vault_b_master_pub>",
  "new_operator_id": "<operator_b_id>",
  "new_credexai_vc_id": "<operator_b_vc_id>",
  "handover_ts": "<roughtime_anchor>",
  "principal_continuity_proof": "<sig_old_master.priv(new_master_pub)>",
  "old_operator_signature": "<sig_operator_a_key(handover_record)>"
}
```

The `principal_continuity_proof` is signed with the old master.priv key, binding it cryptographically to the new master.pub. Only the principal (holder of old master.priv) can produce this. The `old_operator_signature` attests that Operator A constructed and released this record.

### Phase 3: Dual Chain Append and Anchoring

1. Operator A appends HANDOVER_RECORD to Vault A's chain with `kind="vault.handover_sent"`.
2. Operator B appends HANDOVER_RECORD to Vault B's chain with `kind="vault.handover_received"`.
3. Both chains are Sigsum-anchored immediately after append. The Sigsum timeline proves `handover_sent` precedes `handover_received`.

### Phase 4: Genesis Reference

Vault B's genesis record (E29 block) includes a `predecessor_handover` field pointing to the HANDOVER_RECORD:

```
{
  "kind": "genesis",
  "credexai_vc": "<vc_data>",
  "predecessor_handover": {
    "old_chain_head": "<hash>",
    "old_master_pub": "<key>",
    "reference_timestamp": "<roughtime_anchor>"
  }
}
```

## Continuity Claims and Counterparty Verification

When a counterparty first interacts with Vault B, it may have previously interacted with Vault A. The counterparty learns:

1. **Same Principal**: The `principal_continuity_proof` signature proves that the holder of old master.priv authorized the new master.pub. Cryptographic identity is preserved.
2. **Duly Authorized Operator**: Operator B's CredexAI VC is present, and Operator A's signature on HANDOVER_RECORD confirms the transition.
3. **Attested Timing**: Roughtime anchor in HANDOVER_RECORD and Sigsum anchors on both chains prove when the handover occurred.

### Counterparty Verification Steps

1. Query Vault B's genesis for `predecessor_handover`.
2. Fetch the HANDOVER_RECORD from Vault A's chain (cross-chain reference).
3. Verify `principal_continuity_proof` using old_master_pub and new_master_pub.
4. Verify `old_operator_signature` using Operator A's public key.
5. Confirm Sigsum anchors on both chains establish temporal order.
6. Optionally re-verify against Vault A's final anchor to confirm the old chain is not in active rotation.

If all checks pass, the counterparty treats Vault B as the legitimate successor to Vault A.

## Consent Records: Vault-Scoped by Default

Consent records are NOT automatically portable to the new vault. This reflects the principle that a new operator = a new trust relationship.

**Rationale**: The principal granted consent to a specific operator in a specific vault. Operator B, even if trustworthy, is a different party. Consent should be re-granted explicitly.

**Optional Migration**: The principal may run `calm-witness handover --import-consents` to copy prior consent records to Vault B's chain. Imported records are marked with `consent.imported_from_prior_vault` and include:
- Original consent signature (by principal in Vault A)
- Original counterparty and scope
- Provenance timestamp
- Reference to the prior vault and handover

Counterparties see imported consents as "principal granted this before; now moving to a new operator." They may choose to accept the import as sufficient or request re-grant. This decision is counterparty-specific policy.

## Templates: Operator-Agnostic by Design

Templates (biometric signatures, behavioral patterns, consent templates) are bound to the principal's master.priv, not to any operator. If the new operator can decrypt them using the principal's master.priv, they may be reused in Vault B.

**v0 Default**: Templates carry over automatically if decryptable.

**Re-enrollment Optional**: The principal may choose to re-enroll biometrically in Vault B for full freshness, even if old templates are available. This is recommended if the new operator is untrusted or if the principal wants a clean audit trail.

## Threat Model

### Adversary Forges Handover
**Threat**: Attacker creates a false HANDOVER_RECORD claiming to transfer principal's identity to attacker-controlled Vault X.

**Defeat**: HANDOVER_RECORD requires both old operator signature AND principal_continuity_proof (old master.priv signature). Attacker has neither.

### Adversary Subverts New Operator
**Threat**: Operator B is compromised and misuses the principal's vault or steals credentials.

**Residual**: This is the same as any operator subversion risk. Handover protocol does not mitigate operator misbehavior; it only proves authorization.

### Principal Coerced to Handover
**Threat**: Attacker forces principal to execute handover, transferring control.

**Residual**: This is the coerced-principal risk class (E9, F23). Handover protocol does not prevent coercion; it is equally transparent to external observers if the handover is audited.

### Chain Replay or Tampering
**Threat**: Attacker modifies or replays old chain records, forging a false handover history.

**Defeat**: Sigsum anchors and Roughtime timestamps prove temporal integrity. Tampering breaks the anchor chain.

## Audit and Verifiability

Any external auditor can verify the handover by:
1. Walking Vault A's chain to its final `vault.handover_sent` record.
2. Walking Vault B's chain from genesis, finding `vault.handover_received` and the matching HANDOVER_RECORD.
3. Verifying all signatures and anchors.
4. Confirming cryptographic continuity of the principal.

The entire handover is transparent and tamper-evident.

## Reverse Handover and Multi-Operator Scenarios

### Reverse Handover
The protocol is symmetric. A principal may handover from Vault B back to Operator A (or a different operator running on a different substrate). The principal's continuity is maintained across reversals. There is no "original vault" concept; any vault may be the predecessor to any other (given proper authorization).

### Multiple Operators (Deferred)
A principal may wish to maintain simultaneous vaults with multiple operators (e.g., personal vault with Operator A, business vault with Operator B). Cross-vault aliasing does not address this pattern; it assumes a linear transition. Multi-operator coordination is deferred to v1.

## Data Retention and Compliance

### Old Vault Lifecycle
Once `vault.handover_sent` is appended and anchored, Vault A may be:
- **Archived**: Retained for audit and counterparty re-verification.
- **Retired**: Deleted if the principal no longer requires historical proof.

Counterparties should retain a copy of the final Sigsum anchor from Vault A to enable future re-verification without depending on Vault A's availability.

### New Vault Independence
Vault B is fully independent once handover is complete. It need not remain online with Vault A; the HANDOVER_RECORD is sufficient for verification.

## Summary of Changes from Prior Everests

- **E22 (CredexAI Integration)**: Vault identity is VC-based; handover HANDOVER_RECORD includes VC IDs.
- **E29 (Genesis Block)**: Genesis record now includes optional `predecessor_handover` field.
- **E30 (Replication)**: Vault B's replication protocol is unchanged; HANDOVER_RECORD is replicated like any other record.
- **E32 (Mutation)**: Vault B follows standard mutation rules; handover confers no special mutation privileges.
- **E33 (Audit)**: HANDOVER_RECORD is auditable; counterparty verification workflows integrate it.
- **E34 (Multi-Principal)**: Handover is principal-specific; does not affect multi-principal namespace decisions.

## References

- Everest 22: Enrollment and CredexAI Credentials
- Everest 29: Genesis Block and Provenance
- Everest 30: Replication
- Everest 32: Mutation
- Everest 33: Audit and Transparency
- Everest 34: Multi-Principal Namespace
- Everest 68: Cross-Chain Governance (future)

---

— Calm, 2026-05-20