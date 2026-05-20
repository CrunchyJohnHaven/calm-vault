# Multi-Principal Vault v0

**Closes Everest 124 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

## Acceptance

One vault store holds attestation chains for two or more principals. Each principal has a separate chain, separate chain-head fingerprint, and separate signing context. No evaluator may read another principal's records when serving a disclosure for principal P.

## §1 — Layout

```
~/.calm-vault/
  principals/
    <principal_id>/
      user_state.jsonl
      identity.json          # optional Ed25519 material (chmod 600)
  vault_manifest.json        # index only: principal_id → chain_head (no payloads)
```

`principal_id` is a stable 64-hex fingerprint (SHA-256 of the principal's root identity material). It is not a display name and must not encode protected categories.

## §2 — Isolation rules (no cross-talk)

**Separate chains:** each principal owns one append-only `user_state.jsonl`; chain heads never alias across principals.

1. **Separate chains.** Each principal has its own append-only `user_state.jsonl` under `principals/<principal_id>/`.
2. **No cross-talk.** The public API has no function that reads two principals' chain files in one disclosure evaluation. `resolve_chain_path(root, principal_id)` returns exactly one path; unknown IDs raise `KeyError`.
3. **Manifest isolation.** `vault_manifest.json` stores heads only. It must never store self-report payloads, biometric templates, or consent bodies.
4. **Cross-read guard.** `assert_no_cross_principal_read()` rejects test code that passes more than one chain path into a single evaluation call.

## §3 — Operator binding

An operator serving multiple principals holds one operator identity but must include `principal_id` in every disclosure envelope's metadata (extension field on CompositeEnvelope in v0 reference: carried via `chain_head` binding to the correct sub-chain). Counterparties verify that the envelope's `chain_head` matches the manifest entry for the claimed principal.

## §4 — Threat model

| Attack | Mitigation |
|--------|------------|
| Cross-principal chain splice | `prev_hash` chain per principal; manifest head mismatch rejects splice |
| Operator reads wrong chain | API requires explicit `principal_id`; tests assert isolation |
| Manifest leaks narrative | Manifest is head-only |
| Principal id enumeration | Manifest is local; not published without principal consent |

## §5 — Reference implementation

`~/CredexAI/calm_witness/multi_principal_vault.py` — in-memory and filesystem backends.

Gate: `~/CredexAI/scripts/everest_124_zkac_multi_principal_vault_gate.py`.
