# Everest 125 — Vault Federation Protocol

**Summit:** 125/300 (ZKAC Range J)  
**Acceptance:** A principal can move their vault from operator A to operator B with chained continuity proof.  
**Prereq:** 124 (multi-principal vault).  
**Honors:** [`CALM_REFUSAL_FLOOR_INDEX.md`](../CALM_REFUSAL_FLOOR_INDEX.md), [`CALM_TENANCY_PROTOCOL_v0.md`](../CALM_TENANCY_PROTOCOL_v0.md).

## Normative spec

[`ZKAC_VAULT_FEDERATION_v0.md`](../ZKAC_VAULT_FEDERATION_v0.md)

## Reference implementation

| Artifact | Path |
| --- | --- |
| Module | `~/CredexAI/calm_witness/vault_federation.py` |
| Tests | `~/CredexAI/calm_witness/test_vault_federation.py` |
| Gate | `~/CredexAI/scripts/everest_125_zkac_vault_federation_gate.py` |

## Acceptance evidence

Gate exit 0. Export from operator A, import handoff on operator B, continuity verifier green. Pytest covers digest mismatch rejection and handoff field binding.

## Follow-through

**126:** Inter-vault attestation (identity confirmation without chain merge).

— Musk
