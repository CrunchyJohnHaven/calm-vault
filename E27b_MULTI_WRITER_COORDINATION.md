# Everest 27b — Multi-Writer Concurrent-Append Coordination

**New summit, registered after the original 100. Fills the chain-fork gap discovered in PASS 18 when two concurrent CALM sessions both appended seq:23 records.**

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 0. The discovered gap

PASS 18's anchor attempt found that two CALM sessions writing concurrently to `~/.calm-vault/user_state.jsonl` can both append records claiming the same sequence number. The chain's internal hash-link integrity stays sound (each record links to a real predecessor), but the linear `seq=line_number` invariant breaks.

The chain verifier (Everest 28) currently flags this as a `seq_mismatch` error, treating the chain as broken. The reality is subtler: the chain has FORKED. Both branches are internally valid hash-chains; only one is the canonical main branch.

Without coordination, every parallel agent pass risks adding a fork tip. The protocol's `summit_claim` lock mechanism (referenced in `SUMMIT_REGISTRY.md`) is currently advisory only — no actual fork-prevention machinery exists.

---

## 1. v0 coordination protocol

### 1.1 Three new chain record kinds

#### `summit_claim`

Issued when an agent begins work on a summit. Soft-locks the summit for ~60 minutes.

```json
{
  "kind": "summit_claim",
  "operator": "<agent_id>",
  "payload": {
    "summit_number": <int>,
    "claimant_id": "<unique session identifier>",
    "expected_finish_at_utc": "<ISO-8601 timestamp>",
    "stream": "<A | B | C | D | E | F | G>",
    "scope_files": ["<paths the agent will modify>"]
  },
  ...
}
```

Other agents reading the chain see active claims and avoid the same scope.

#### `merge_fork`

Issued when an agent detects a fork and chooses a canonical branch.

```json
{
  "kind": "merge_fork",
  "operator": "<reconciling agent>",
  "payload": {
    "fork_seq": <seq number where fork happened>,
    "canonical_branch_head_hash": "<sha256 of the surviving tip>",
    "alternate_branch_head_hash": "<sha256 of the dropped tip>",
    "tiebreak_rule_applied": "<earliest_ts | lower_hex_record_hash | longer_branch | external_authority>",
    "alternate_branch_preserved_at": "<optional path to the dropped branch's records>",
    "reason": "<human-readable explanation>"
  },
  ...
}
```

The merge_fork record extends the canonical branch. The fork point + dropped branch tip are preserved for audit; they are not erased.

#### `pre_append_lock`

Optional advisory lock for the *next* append (~10 seconds). Used by agents about to write a critical record.

```json
{
  "kind": "pre_append_lock",
  "operator": "<agent_id>",
  "payload": {
    "intended_seq": <int>,
    "intended_prev_hash": "<sha256>",
    "expires_at_utc": "<ISO-8601, ~10s from now>",
    "purpose": "<short string>"
  },
  ...
}
```

An agent that sees an active pre_append_lock with `expires_at > now` waits or re-reads before appending.

### 1.2 Tiebreak rules (canonical branch selection)

When two records claim the same seq with the same prev_hash:

1. **Earlier `ts` wins** (assumes both record `ts_source: user_message_local_clock` or stronger).
2. If `ts` ties: **lower-hex `record_hash` wins** (deterministic tiebreak).
3. The losing branch's tip is recorded in a `merge_fork` record, never erased.

For records claiming the same seq but DIFFERENT prev_hash (i.e., different forks earlier in the chain): treat as a structural fork that needs human review. Write a `kind: "fork_review_required"` record and pause concurrent writers.

### 1.3 Stale-claim sweep

A `summit_claim` is stale if its `expected_finish_at_utc` is in the past AND no `summit_bagged` record with the matching `summit_number` has appeared. Stale claims are auto-released by the next agent that notices them, via a `summit_claim_release` record.

```json
{
  "kind": "summit_claim_release",
  "operator": "<sweeping agent>",
  "payload": {
    "released_summit_number": <int>,
    "original_claimant_id": "<string>",
    "release_reason": "stale_claim_timeout"
  },
  ...
}
```

---

## 2. Extension to the chain verifier (Everest 28)

The verifier must learn to:

1. Recognize `merge_fork` records as authoritative branch-selection signals.
2. Verify the canonical branch's chain integrity independently of the dropped branch.
3. Report (not error on) fork events as informational chain history.
4. Reject only when (a) hash linkage breaks INSIDE the canonical branch, OR (b) a fork has no `merge_fork` record reconciling it.

Updated verifier exit codes:
- 0: clean chain
- 1: hash linkage broken (real corruption)
- 2: unreconciled fork present (needs `merge_fork`)
- 3: claim conflict (two `summit_claim` records active on same summit)

---

## 3. Reference implementation roadmap

Files to write (deferred from this design):

1. `~/CredexAI/calm_witness/coordination.py` — claim / merge_fork / pre_append_lock record builders and validators.
2. `~/CredexAI/calm_witness/test_coordination.py` — concurrency stress tests.
3. Update `~/CredexAI/calm_witness/verify_chain.py` to handle merge_fork records.
4. `~/CredexAI/scripts/everest_27b_zkbb_coordination_gate.py` — gate verifying:
   - claim/release lifecycle works
   - merge_fork extends canonical branch
   - fork tiebreak is deterministic
   - stale-claim sweep clears expired locks

These deliverables are well-bounded and dispatchable to a Haiku agent in a future pass.

---

## 4. What this Everest does NOT do

- Does NOT prevent forks in adversarial conditions (a malicious operator can ignore claims).
- Does NOT provide strong consistency guarantees (this is an EVENTUALLY-consistent coordination layer).
- Does NOT replace true distributed-consensus protocols. For multi-operator deployments, that's a v1+ summit (potentially BFT for the chain heads).
- Does NOT erase fork history. Both branches are preserved; only the canonical branch is extended.

---

## 5. Why this matters now

PASS 18 produced a real fork. The current chain at `~/.calm-vault/user_state.jsonl` has at least one duplicate-seq:23 line — a fork tip that was not extended. The protocol's claim of "tamperproof on disk" still holds (every record's hash links to a real predecessor); but the cleanliness claim does not.

A counterparty verifying the chain today must be told: "two CALM sessions ran concurrently; the canonical branch ends at the longer one; the fork tip is preserved as an audit artifact."

The fix is the coordination layer above, NOT a chain-rewrite. The chain stays append-only.

---

## 6. Cross-references

- ZKBB_USER_EVERESTS_100.md, Everest 28 (chain verifier)
- ZKBB_USER_EVERESTS_100.md, Everest 10 (multi-device chain reconciliation — adjacent gap)
- SUMMIT_REGISTRY.md §"How to claim and bag a summit" (claims protocol referenced)
- PARALLEL_WORK_STREAMS.md §"Conflict-avoidance rules" (file-level partitioning)
- The PASS 18 incident: seq:23 fork between two concurrent CALM sessions (chain head at the time: `861b74411babaaaf2ab55fd85e342a0c2dd4b4e26044dfcb1a6fac71f7ad4428`)

---

## 7. Acceptance criteria for full bag

This summit is design-bagged at the v0 spec level. Full bag requires:

1. `coordination.py` reference impl + tests + gate (deferrable to Haiku pass).
2. `verify_chain.py` extended to handle merge_fork records.
3. The current chain's fork at seq:23 reconciled with an explicit `merge_fork` record.
4. SUMMIT_REGISTRY.md + PARALLEL_WORK_STREAMS.md updated to reference E27b.
5. Universal prompt §5 (parallel dispatch) updated to require `summit_claim` before each XL summit.

---

**Authored by Calm, 2026-05-20. v0 spec bagged; reference impl deferred to next pass.**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
