# Multi-Principal Vault v0

**Everest 124 · ZKAC substrate · 2026-05-20**

## §0 — One-line spec

One operator-controlled vault **root** may host **≥ 2 principals**, each with a **separate append-only chain**, **separate signing material**, and **no API that reads or evaluates across principals** unless the caller names exactly one `principal_id` and holds that principal's authorization.

## §1 — Why this exists

Federation and household operators need multiple principals on one machine without turning the vault into a **cross-principal surveillance surface**. The failure mode to refuse: a bug or malicious operator that compares chain A to chain B to infer relationships, timing, or values patterns.

## §2 — Layout (canonical paths)

```
~/.calm-vault/
  vault_manifest.json          # schema_version, principals[], operator binding
  principals/
    <principal_id>/
      user_state.jsonl         # hash chain (Everest 26–28)
      keys/                    # principal-specific encrypted material (Everest 16 pattern)
      consent_matrix.json      # per-(predicate, counterparty_class) defaults
```

`principal_id` is a stable UTF-8 slug (`john-bradley`, `did:calm:…` hash prefix). It is **not** derived from protected-category attributes.

## §3 — Isolation rules (non-negotiable)

1. **Separate chains.** No record in principal A's chain references principal B's `record_hash` except in an explicit, principal-authorized **inter-vault attestation** (Everest 126, deferred).
2. **Separate evaluators.** Predicate evaluation always receives `(principal_id, chain_path)`; evaluators must not accept two chains in one call.
3. **Separate envelopes.** `CompositeEnvelope.issued_by_operator` binds the operator; `principal_id` is carried in envelope metadata but **never** leaks another principal's predicates.
4. **No cross-principal analytics.** Operator logs may count envelopes minted; they may not correlate timing across principals for ranking or scoring (Concord anti-purity-test extends here).
5. **Manifest is operator-readable, not counterparty-readable.** Counterparties verify envelopes, not the manifest.

## §4 — `vault_manifest.json` (v0)

| Field | Type | Semantics |
| --- | --- | --- |
| `schema_version` | int | `0` |
| `operator_did` | string | Operator identity binding |
| `created_at_iso` | string | Manifest genesis time |
| `principals` | array | `{principal_id, chain_head, genesis_hash, added_at_iso}` |

Appending a principal requires a chained `principal_added` record in **that principal's** genesis block (seq 0) plus a manifest update signed by the operator.

## §5 — API surface (reference impl)

| Function | Behavior |
| --- | --- |
| `resolve_chain_path(root, principal_id)` | Returns path; raises if principal unknown |
| `list_principals(root)` | Returns IDs only; no chain content |
| `append_record(root, principal_id, record)` | Append to one chain; verify `prev_hash` locally |
| `verify_principal_chain(root, principal_id)` | Everest 28 verifier scoped to one chain |

## §6 — Threat model

| Attack | Mitigation |
| --- | --- |
| Operator compares two chains offline | Policy + audit; API refuses multi-chain reads |
| Cross-principal consent bleed | Consent matrix stored per principal directory |
| Principal enumeration by counterparty | Counterparties learn only principals who disclosed to them |
| Manifest tampering | Operator signature on manifest; Sentinel hook (Everest 27) |

## §7 — Falsifiability

A third party with filesystem access can confirm: (a) chains live in distinct files, (b) reference `append_record` rejects wrong `principal_id`, (c) no function in `multi_principal_vault.py` opens two chains in one evaluation call.

## §8 — Deferred (not v0)

- Everest 125 vault federation (move between operators)
- Everest 126 inter-vault attestation
- HSM-per-principal keys (Everest 132)

— Calm, 2026-05-20
