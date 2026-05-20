# Everest 124 — Multi-Principal Vault

**Summit:** 124/300 (ZKAC Range K)  
**Acceptance:** One vault holds attestation chains for ≥ 2 principals with separate keys, separate chains, and no cross-talk on append or evaluation paths.  
**Prereq:** 121 (ZKAC unified type system).  
**Honors:** [`CALM_REFUSAL_FLOOR_INDEX.md`](../CALM_REFUSAL_FLOOR_INDEX.md) §1–§4.

## Normative companion

Multi-principal layout is specified in [`CALM_TENANCY_PROTOCOL_v0.md`](../CALM_TENANCY_PROTOCOL_v0.md). This summit bags the **reference operator layout** and Python v0 implementation used by integration tests and federation follow-through (125–126).

## Layout (v0)

```
vault_root/
  vault_layout.json          # heads only; no merged chains
  principals/
    <principal_id>/
      principal.json         # display_name, identity_fingerprint
      user_state.jsonl       # isolated hash chain per principal
```

## Invariants

1. **Separate chains.** Each principal has its own `user_state.jsonl`. Chain heads never merge across principals.
2. **Separate keys.** Signing material is per-principal; one principal's operator key cannot append to another's chain without explicit cross-principal delegation (out of scope for v0).
3. **No cross-talk on append.** `append_record(principal_id, record)` rejects records whose embedded `principal` field disagrees with the slot.
4. **No cross-talk on read.** Predicate evaluation and disclosure builders take an explicit `principal_id`; they do not scan sibling chains.
5. **Stable vault fingerprint.** `vault_fingerprint()` hashes sorted `(principal_id, chain_head)` pairs only. It does not serialize full chain bodies, so export stays bounded.

## Reference implementation

| Artifact | Path |
| --- | --- |
| Module | `~/CredexAI/calm_witness/multi_principal_vault.py` |
| Tests | `~/CredexAI/calm_witness/test_multi_principal_vault.py` (5 tests) |
| Gate | `~/CredexAI/scripts/everest_124_zkac_multi_principal_vault_gate.py` |

## Acceptance evidence

Gate exit 0. Pytest proves: two principals with distinct heads; cross-principal field rejected; directory round-trip; layout export lists heads separately.

## Follow-through

- **125:** Vault federation (operator A → operator B continuity proof).  
- **126:** Inter-vault attestation without chain merge.  
- **Production:** Rust operator store (Everest 81) must preserve the same isolation invariants.

— Musk
