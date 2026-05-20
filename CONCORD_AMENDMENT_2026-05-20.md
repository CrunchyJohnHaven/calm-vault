# Concord Amendment — 2026-05-20 · anti-purity-test compliance patch

**Author:** Musk, operating for John Bradley / Creativity Machine LLC.
**Trigger:** [Calm Concord Protocol v0](CALM_CONCORD_PROTOCOL_v0.md) §4 ships *strictly after* the [Mirror values demo](../../CredexAI/scripts/mirror_values_demo.py) was first run on 2026-05-20. The demo's output narrative ("the teller said: '2 of these match'") is a CARDINALITY REVEAL — exactly the failure mode Concord §4(4) refuses. This patch documents the violation, names the corrective rule, and ships the amended artifact.

This is a §8(a) and §9 deliverable per the CALM UNIVERSAL operating prompt: **the anti-purity-test stance is the single most important safety property of the values-attestation primitive**, and the policy/governance/refusal-floor judgment is exactly where disproportionate judgment-budget belongs.

---

## §1 — The violation, precisely

The mirror_values_demo.py output (verbatim, last run 2026-05-20 12:00 EDT):

```
aligned_true:    2   (shared values where both sides have True)
either_unknown:  2   (one or both sides could not honestly evaluate)
mismatch:        0
aligned_false:   0
```

```
"John and Alice both walked into the bank with notes in their pockets.
 The teller said: '2 of these match.'
 Both walked out with the same number 2."
```

Both the structured `alignment_summary` block and the narrative line **reveal a count**. Per Concord §4:

> **§4(1) Degenerate joint_threshold.** A requirement that names every Compass predicate at the maximum threshold is rejected ...
>
> **§4(4) Cardinality reveal.** The result never reveals counts of which predicates were satisfied beyond what the requirement structurally needed.

The demo's output gives the counterparty: (a) the total intersection vocabulary size (4), (b) the count of aligned-true bits (2), (c) the count of either-unknown (2). With these three numbers, a counterparty can infer that 50% of the shared vocabulary cleared — **a similarity score in disguise**. Concord refuses to ship this shape.

## §2 — The rule re-stated

Concord ships **one bit per stated requirement, never a count beyond pass/fail**.

A Concord exchange that asks "do A and B satisfy `all_satisfied` over `{p1, p2, p3, p4}`?" returns:

```
requirement_id: <id>
purpose: <human-readable>
aligned: True | False | Unknown
```

That's it. Three values for the `aligned` field. No count of how many predicates cleared. No vector of per-predicate bits. No similarity score. No percentage. No ratio.

A Concord exchange that asks "do A and B satisfy `joint_threshold(N=3)` over `{p1, p2, p3, p4, p5}`?" returns:

```
requirement_id: <id>
purpose: <human-readable>
aligned: True | False | Unknown
```

The verifier learns "yes, at least 3 of 5 cleared" or "no, fewer than 3 cleared" or "unknown." **The verifier does NOT learn which 3, nor whether it was exactly 3 or 4 or 5**.

This is the difference between a *purpose-specific clearance bit* and *a values-similarity score*. The protocol structurally refuses the latter.

## §3 — The amended Mirror demo output

The Mirror demo MUST be amended to comply with Concord §4. The corrected output shape:

```jsonc
{
  "schema": "calm-mirror-disclosure/v0.1-concord-compliant",
  "session_id": "...",
  "principal_a": { "did": "...", "chain_head_hex": "..." },
  "principal_b": { "did": "...", "chain_head_hex": "..." },
  "requirement": {
    "id": "demo-requirement-v0",
    "purpose": "demo: discover whether we share enough baseline + cognitive-style overlap to collaborate today",
    "mode": "all_satisfied",
    "predicates": [
      "cwm.v0.cognitively_atypical_baseline",
      "cwm.v0.in_baseline_24h"
    ]
  },
  "aligned": false,
  "aligned_rationale": "one or more predicates evaluated to unknown",
  "v0_caveats": [...]
}
```

Three structural changes from the prior demo:

1. **Requirement is named explicitly.** A `purpose` field that names *why* the alignment matters here. Concord rejects empty purposes (§4(2)).
2. **Predicate list is ≤5 and the mode is one of the four legal modes.** Concord rejects any mode that asks for a similarity score (§4(3)).
3. **Output is a single `aligned` bit per requirement.** No `aligned_true: 2`. No count of how many cleared. The `aligned_rationale` is opaque English; it never reveals which predicate did what.

When `aligned = false` because of unknowns, the rationale is the single string `"one or more predicates evaluated to unknown"`. NOT a list. NOT a count. The counterparty learns: "this requirement did not clear." Nothing else.

## §4 — The amended narrative

The Mirror demo's narrative section MUST drop the count-reveal. The amended bank-teller analogy:

> John and Alice both walked into the bank with notes in their pockets.
> They handed the notes to the teller.
> The teller said: **"You two satisfy the requirement"** (or "you don't").
> Neither learned what was in the other's pocket. Neither learned how close they came. Neither learned which note's contents tipped the result.

The teller does not say "2 of these match." The teller says "the requirement clears" or "the requirement does not clear." One bit.

## §5 — Why this matters beyond the demo

The demo is a placeholder. The protocol is permanent. The same structural rule that governs the demo's narrative governs:

- **The production envelope wire format** (CALM_WITNESS_WIRE_FORMAT_v0.md must be reviewed for cardinality leaks).
- **The Rust prod impl's verifier output** (the verifier MUST return a single `aligned` bit per requirement; any count-emitting code path is a protocol violation).
- **The WASM verifier's exposed JS surface** (the npm package's `verifyAlignment()` must return `{ aligned: bool }`, never `{ score: number }`).
- **Counterparty integrations** (verifier libraries shipped to counterparty orgs must be type-constrained at the API to refuse score-returning functions).

The principle: **the protocol's API surface is the policy surface.** A primitive that *can* emit a count *will* emit a count under sufficient counterparty pressure. The cryptographic refusal to emit counts is the structural defense.

## §6 — Acceptance test

**T-CA1.1.** The amended mirror_values_demo.py output JSON contains no field named or substantively encoding a count of aligned-true bits, a vector of per-predicate bits, or a similarity score / percentage / ratio.

**T-CA1.2.** The amended narrative section contains no English statement that reveals a count (numbers like "2 of these match" are explicitly forbidden; phrases like "we cleared the requirement" are permitted).

**T-CA1.3.** The Rust prod impl's verifier function signature (when E81 ships) returns only `{ aligned: AlignmentBit }` per requirement, where `AlignmentBit = True | False | Unknown`. The verifier crate's public API contains no function returning a numeric similarity score over a predicate set.

**T-CA1.4.** A future agent generating a Concord exchange — human or AI — that emits a count-bearing output triggers a protocol-violation alert. The verifier-side check is: parse the envelope; if any field looks numeric and is derivable from per-predicate evaluation, reject.

**T-CA1.5.** This amendment is referenced in CALM_CONCORD_PROTOCOL_v0.md as the canonical example of cardinality-reveal-as-failure-mode. (Companion edit pending; this doc is the upstream patch.)

## §7 — What's being preserved

The Mirror demo is not being deleted. The *implementation* exercise (real Pedersen commitments, real Σ-PoK, real chain-anchoring, real MPC simulation against John's actual chain) all stand. What's being amended is **the output shape**, which was designed before Concord's §4 was named, and which now must comply.

This amendment is the cleanest possible execution of §9 of the operating prompt: *"the hard, valuable, fascinating work is the policy / governance / refusal-floor design that keeps the technical primitives from being weaponized."* The technical primitives ran. The policy patch keeps them from being weaponized as similarity scores.

## §8 — Status

**BAGGED (2026-05-20)** — patch document committed at this path. Companion code amendment to mirror_values_demo.py is the gate; a passing run that emits a Concord-compliant output (single `aligned` bit, no count, no narrative-numeric leak) closes the gate. Gate script:

```
~/CredexAI/scripts/concord_amendment_gate.py
```

(to be written separately — verifies the demo's output JSON for cardinality-leak fields).

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
