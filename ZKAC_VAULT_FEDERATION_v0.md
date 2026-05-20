# ZKAC Vault Federation v0

**Everest 125 · 2026-05-20**

A principal may move attestation custody from operator A to operator B without merging chains or leaking sibling principals. Continuity is proven by a hash-linked handoff record, not by operator trust alone.

## §0 — Actors

| Actor | Role |
| --- | --- |
| Principal | Authorizes export and accepts import |
| Source operator (A) | Holds chain until export; signs export manifest |
| Destination operator (B) | Receives bundle; mints handoff anchor on a fresh chain |
| Verifier | Checks `continuity_digest` against exported chain text |

## §1 — Export bundle (operator A)

`MigrationExport` fields:

- `schema`: `calm-vault/federation-export/v0`
- `principal_id`
- `source_operator_id`
- `source_chain_jsonl` (full verified chain at export time)
- `source_chain_head` (64-hex record hash)
- `continuity_digest`: SHA-256 over canonical chain bytes (UTF-8, LF-normalized)
- `exported_at` (RFC3339)

Export MUST run only after `verify_chain_text(source_chain_jsonl).ok`.

## §2 — Handoff record (operator B)

First record on the destination chain:

```json
{
  "kind": "vault_federation.handoff",
  "principal": "<principal_id>",
  "payload": {
    "from_operator": "operator-a",
    "to_operator": "operator-b",
    "source_chain_head": "<64-hex>",
    "continuity_digest": "<64-hex>",
    "migration_nonce": "<random 32-byte hex>"
  }
}
```

Subsequent records append on operator B with normal sequencing. The prior chain is not merged into the new file; verifiers recompute `continuity_digest` from the export artifact when disputing continuity.

## §3 — Continuity proof

`verify_migration_continuity(export, dest_chain_jsonl) -> bool`:

1. Re-verify exported chain.
2. Recompute `continuity_digest` and compare to export field.
3. Locate the first `vault_federation.handoff` on the destination chain.
4. Confirm handoff `source_chain_head` and `continuity_digest` match the export.

## §4 — Refusal floor

Federation does not relax scope statements, refusal categories, or Concord anti-purity-test rules. Operator B cannot infer other principals from a single-principal export bundle.

## §5 — Reference implementation

| Artifact | Path |
| --- | --- |
| Module | `~/CredexAI/calm_witness/vault_federation.py` |
| Tests | `~/CredexAI/calm_witness/test_vault_federation.py` |
| Gate | `~/CredexAI/scripts/everest_125_zkac_vault_federation_gate.py` |

## §6 — Follow-through

**Everest 126:** Inter-vault attestation without exporting full chain bodies.

— Musk
