# Vault Federation Protocol v0

**Closes Everest 125 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

## Acceptance

A principal moves their vault from operator A to operator B. The move produces a chained continuity proof: the new operator's first record binds to the exported chain head from operator A without revealing vault contents to either operator's counterparty.

## §1 — Handoff record

Kind: `vault.federation.handoff.v0`

```json
{
  "kind": "vault.federation.handoff.v0",
  "payload": {
    "principal_id": "<64-hex>",
    "source_operator_id": "<64-hex>",
    "target_operator_id": "<64-hex>",
    "exported_chain_head": "<64-hex>",
    "exported_record_count": 42,
    "handoff_nonce": "<uuid>",
    "continuity_proof": "<64-hex>"
  }
}
```

`continuity_proof` = SHA-256(canonical JSON of `{exported_chain_head, target_operator_id, handoff_nonce, principal_id}`).

## §2 — Ceremony

1. Principal authorizes export at operator A (local only).
2. Operator A emits `exported_chain_head` + Merkle root over record hashes (no payloads in export bundle).
3. Principal imports at operator B; operator B appends handoff as genesis-linked record on the new sub-chain.
4. Counterparties treat disclosures only after B's handoff record is present if policy requires federation freshness.

## §3 — Security

- Export bundle must not include biometric templates or self-report bodies by default (hash-only mode).
- Replay: `handoff_nonce` is single-use; second import rejected.
- Wrong operator: `target_operator_id` must match B's live operator fingerprint.

## §4 — Reference

`~/CredexAI/calm_witness/vault_federation.py` and gate `everest_125_zkac_vault_federation_gate.py`.
