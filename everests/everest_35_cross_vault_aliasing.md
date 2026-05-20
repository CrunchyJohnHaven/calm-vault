# Everest 35 — Cross-Vault Aliasing

**Summit:** 35/100 (ZKBB Phase III)  
**Acceptance:** If the principal moves to a new operator, the new vault can prove continuity with the old via signed handover without breaking chain continuity.  
**Prereq:** Everest 22 (CredexAI VC), Everest 29 (genesis block).  
**Normative federation base:** [`VAULT_FEDERATION_PROTOCOL_v0.md`](../VAULT_FEDERATION_PROTOCOL_v0.md).

## Overview

Cross-vault aliasing is the ZKBB-User track name for operator migration with cryptographic continuity. When a principal leaves operator A for operator B, counterparties must still verify that Vault B is the legitimate successor to Vault A: same principal, authorized transition, tamper-evident link from the old chain head to the new genesis.

The wire format, `continuity_proof` digest, and replay rules are defined in [`VAULT_FEDERATION_PROTOCOL_v0.md`](../VAULT_FEDERATION_PROTOCOL_v0.md). This Everest adds ZKBB-specific bindings from Everest 22 and Everest 29: CredexAI VC identifiers on both sides, Ed25519 operator and principal signatures over the handoff payload, and an optional `predecessor_handover` block on the new vault genesis record.

## Relationship to vault federation v0

| Layer | Document / kind | Role |
| --- | --- | --- |
| Federation wire | `vault.federation.handoff.v0` | Canonical handoff record; `continuity_proof` binds exported head to target operator |
| ZKBB alias sent | `vault.alias.handover_sent.v0` | Operator A appends federation handoff plus `source_operator_sig` |
| ZKBB alias received | `vault.alias.handover_received.v0` | Operator B appends the same handoff body plus import attestation |
| Genesis link | Everest 29 `genesis.payload.predecessor_handover` | New vault genesis points at old chain head without duplicating payloads |

Implementers MUST treat [`VAULT_FEDERATION_PROTOCOL_v0.md`](../VAULT_FEDERATION_PROTOCOL_v0.md) as authoritative for export bundle shape, `handoff_nonce` single-use semantics, and hash-only export mode. ZKBB signatures and VC fields are additive; verifiers that understand only federation v0 still validate `continuity_proof`.

## Handover payload (composed)

The federation handoff payload (§1 of federation v0) is extended for ZKBB:

```json
{
  "kind": "vault.federation.handoff.v0",
  "payload": {
    "principal_id": "<64-hex fingerprint of master.pub>",
    "source_operator_id": "<64-hex operator fingerprint>",
    "target_operator_id": "<64-hex operator fingerprint>",
    "exported_chain_head": "<64-hex record_hash of Vault A tip>",
    "exported_record_count": 42,
    "handoff_nonce": "<uuid>",
    "continuity_proof": "<64-hex>",
    "source_credexai_vc_id": "vc:credexai:operator-a:2026-05-20:…",
    "target_credexai_vc_id": "vc:credexai:operator-b:2026-05-20:…",
    "principal_continuity_proof": "ed25519:<sig_hex>",
    "source_operator_signature": "ed25519:<sig_hex>"
  }
}
```

**`continuity_proof`** remains exactly federation v0:

`SHA-256(canonical JSON of {exported_chain_head, target_operator_id, handoff_nonce, principal_id})`.

**`principal_continuity_proof`** is an Ed25519 signature by the principal's master private key (Vault A) over canonical bytes:

`SHA-256("calm-witness/cross-vault-aliasing/v0" || target_operator_id || exported_chain_head || new_master_pub_fingerprint)`.

Only the holder of the old master key can authorize the new vault's master binding.

**`source_operator_signature`** is an Ed25519 signature by operator A's signing key over the federation payload fields excluding both signature fields. Binds operator A to releasing the exported head.

## Ceremony

1. **Export at A.** Principal authorizes local export. Operator A emits `exported_chain_head` and record-count metadata. Export bundle is hash-only by default (federation v0 §3).
2. **Principal continuity.** Principal signs `principal_continuity_proof` with Vault A master key, naming Vault B's `master_pub_fingerprint` and target operator.
3. **Handoff construction.** Operator A builds `vault.federation.handoff.v0`, signs `source_operator_signature`, appends as `vault.alias.handover_sent.v0` on Vault A.
4. **Genesis at B.** Operator B creates Everest 29 genesis with `predecessor_handover`:

```json
"predecessor_handover": {
  "exported_chain_head": "<64-hex>",
  "source_operator_id": "<64-hex>",
  "handoff_nonce": "<uuid>",
  "continuity_proof": "<64-hex>"
}
```

5. **Import at B.** Operator B appends `vault.alias.handover_received.v0` (same handoff body) as the first operational record after genesis, linking `prev_hash` to genesis `record_hash`.
6. **Anchoring.** Both chains publish Sigsum heads (Everest 30) so temporal order of sent versus received is externally auditable.

## Counterparty verification

A counterparty verifying Vault B for the first time after migration:

1. Read genesis `predecessor_handover` (if present).
2. Fetch the matching `vault.federation.handoff.v0` from Vault A (or trust a cached copy whose hash matches).
3. Recompute `continuity_proof` per federation v0.
4. Verify `source_operator_signature` against operator A's published key or CredexAI VC (Everest 22, 68).
5. Verify `principal_continuity_proof` against the master public key committed in Vault A's genesis or principal VC.
6. Confirm Vault B's chain verifies from genesis forward (Everest 28) and that the handoff record's `prev_hash` links correctly.

If all checks pass, disclosures from Vault B inherit the principal's pre-migration history for policy purposes; consent records remain vault-scoped unless explicitly imported (see below).

## Consent and templates

**Consent.** Consent grants are operator-scoped. Migration does not auto-copy consent. Optional `calm-witness handover --import-consents` may copy prior grants marked `consent.imported_from_prior_vault` with provenance to the handoff nonce.

**Templates.** Biometric templates bind to master key material, not operator identity. If Vault B decrypts under the same master key, templates may carry over. Re-enrollment remains recommended when operator trust posture changes.

## Security

| Threat | Defense |
| --- | --- |
| Forged handover without old keys | Requires `principal_continuity_proof` and valid `source_operator_signature` |
| Replay of handoff to wrong target | `target_operator_id` and `handoff_nonce` are single-use (federation v0 §3) |
| Chain fork after migration | Old head is frozen at `handover_sent`; new chain genesis links explicitly |
| Export bundle leaks PII | Hash-only export default; no template bodies in federation bundle |

## Reference implementation

| Artifact | Path |
| --- | --- |
| Module | `~/CredexAI/calm_witness/cross_vault_aliasing.py` |
| Federation dependency | `~/CredexAI/calm_witness/vault_federation.py` |
| Tests | `~/CredexAI/calm_witness/test_cross_vault_aliasing.py` |
| Gate | `~/CredexAI/scripts/everest_35_zkbb_cross_vault_aliasing_gate.py` |

## Acceptance evidence

Gate exit 0. Export from operator A, signed handoff, genesis with `predecessor_handover` on operator B, continuity verifier green. Pytest covers digest mismatch rejection, signature cross-failure, and chain head linkage.

## Follow-through

**Everest 125 (ZKAC):** Multi-principal vault federation reuses the same handoff kind at scale.  
**Everest 126:** Inter-vault attestation for identity confirmation without chain merge.

**One-line result:** Everest 35 cross-vault aliasing is BAGGED; federation v0 handoff plus signed principal and operator proofs and genesis `predecessor_handover` preserve chain continuity across operator moves.

— Musk
