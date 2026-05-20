# Multi-Writer Concurrent-Append Coordination v0

**Everest 27b · DESIGN-BAGGED · 2026-05-20**

## §0 — Problem

Parallel CALM sessions can append to `user_state.jsonl` concurrently. Without coordination, two writers produce **forked chains** (duplicate `seq`, divergent `prev_hash`). PASS 18 discovered a fork at seq 23.

## §1 — v0 design (spec only; reference impl deferred)

### Record kind: `merge_fork`

When two heads exist, the operator (or reconciliation job) appends:

```json
{
  "kind": "merge_fork",
  "payload": {
    "left_head_hash": "...",
    "right_head_hash": "...",
    "merged_head_hash": "...",
    "merge_rule": "lexicographic_prev_hash_then_seq"
  }
}
```

`verify_chain` walks forks: both branches must verify to their heads; `merge_fork` binds the chosen canonical head.

### Writer lock (optional, local)

- `flock` on `user_state.jsonl` for single-machine agents
- File swap via write-temp + atomic rename

### Agent coordination

- One **chain writer** role per principal per hour slice
- Other sessions read-only unless holding writer lease in `vault_manifest.json`

## §2 — Follow-through

1. Implement `calm_witness/coordination.py` + extend `verify_chain.py`
2. Reconcile live fork at seq 23 in `~/.calm-vault/user_state.jsonl`
3. Gate `everest_27b_zkac_multi_writer_coordination_gate.py`

## §3 — Falsifiability

After impl: two simulated writers cannot produce a third head without a `merge_fork` record visible in the chain.

— Calm, 2026-05-20
