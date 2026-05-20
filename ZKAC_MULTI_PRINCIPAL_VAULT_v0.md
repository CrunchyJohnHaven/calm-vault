# ZKAC Multi-Principal Vault v0

**Closes Everest 124 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

## Purpose

One operator deployment may serve multiple human principals (household, studio collective, small org). Each principal retains a **separate** hash-chained `user_state.jsonl`, separate chain head, and separate identity fingerprint. No record from principal A may appear in principal B's chain, and evaluators MUST NOT read across chains unless the principal explicitly authorizes a cross-principal ceremony (out of scope for v0).

## Layout on disk

```
vault_root/
  vault_layout.json          # index only; no merged chain
  principals/
    <principal_id>/
      principal.json         # display_name, identity_fingerprint
      user_state.jsonl       # isolated chain for this principal only
```

`principal_id` is a stable slug (no `/`). The layout file lists chain heads and record counts but never embeds chain bodies.

## Reference implementation

`~/CredexAI/calm_witness/multi_principal_vault.py`:

- `MultiPrincipalVault.register_principal`
- `MultiPrincipalVault.append_record` (rejects `principal` field mismatch)
- `MultiPrincipalVault.verify_principal` (delegates to Everest 28 verifier per slot)
- `MultiPrincipalVault.from_directory` / `write_directory`
- `vault_fingerprint` (SHA-256 over sorted `principal_id:chain_head` pairs)

## Non-negotiable floor

- Refusal floor and scope statement apply per principal; no cross-principal comparison predicates.
- Anti-purity-test: Concord and Compass evaluators run per principal chain only.
- Principal-authored evidence: each chain carries its own `principal` field on every record.

## Prereq for Everest 125

Vault federation (operator A → operator B) consumes per-principal chain heads from this layout and MUST preserve principal isolation during export.
