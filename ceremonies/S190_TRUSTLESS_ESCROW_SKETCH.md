# S190 — Trustless Escrow Construction (Partial Bag)

**Status:** PARTIAL BAG
**Date:** 2026-05-20
**Author:** CALM
**Composing on:** S189 (Pedersen commitments), S191 (Σ-protocol binding), S192 (Calm Pact directive equality), S193 (time-lock anchoring), S194 (dispute chaining), S195 (atomicity primitives)

---

## Threat Model

Adversaries: colluding buyer-seller pair attempting double-spend; arbiter bribed post-assignment; network-level replay against stale time-lock; malicious task_spec substitution after commitment.

Trust assumptions eliminated: no central escrow agent, no oracle for outcome verification. Arbiter is a named party with bounded authority — arbiter's decision is itself a Σ-protocol statement chained to contract state, so arbiter cannot act outside the committed predicate envelope without detectable fraud.

Residual trust surface: (1) arbiter identity binding (mitigated by arbiter commitment at contract time, see §Dispute Resolution); (2) time-lock anchor liveness (mitigated by dual-anchor fallback, see §Time-Lock Mechanism); (3) multi-party generalization deferred (see §Handoff).

---

## Relation

Define the escrow relation R over public inputs and private witness:

```
R(
  buyer_commit,       -- Pedersen commitment C_B = g^v_B · h^r_B  (S189)
  seller_commit,      -- Pedersen commitment C_S = g^v_S · h^r_S  (S189)
  task_spec_hash,     -- H(task_spec), collision-resistant, bound at open
  deadline,           -- absolute block-age threshold (anchor-specific units)
  arbiter_pk_hash;    -- hash of arbiter's public key, committed at contract open
  -- private witness:
  v_B, r_B,          -- buyer value + blinding
  v_S, r_S,          -- seller value + blinding
  release_preimage,   -- preimage of release_hash (delivery proof)
  sigma_release       -- Σ-protocol proof that release_preimage is valid (S191)
)
```

Release condition (happy path): prover supplies `(release_preimage, sigma_release)` satisfying:

```
verify_sigma(sigma_release, task_spec_hash, release_preimage) = 1
AND current_anchor_age < deadline
AND open(buyer_commit, v_B, r_B) AND open(seller_commit, v_S, r_S)
AND v_B = v_S   -- directive equality check (S192)
```

The directive equality predicate `v_B = v_S` enforces that buyer's committed payment value equals seller's committed receive value — no value can be conjured or silently redirected. This is the Calm Pact directive equality binding from S192.

---

## Time-Lock Mechanism

Two anchoring options; contract specifies which at open time.

**Option A — Sigsum chain head age:** `deadline` is encoded as a minimum chain-head sequence number. Verifier fetches the current Sigsum log head and checks `log_head.seq >= deadline_seq`. Proof-of-inclusion witness for the log entry is part of the on-chain state; age is auditable without trusting the verifier.

**Option B — OpenTimestamps:** `deadline` is a Bitcoin block height embedded in an OTS proof. Verifier checks OTS attestation against a committed merkle path. Advantage: Bitcoin's global finality; disadvantage: ~10 min granularity.

**Dual-anchor fallback (recommended):** Contract commits to both a Sigsum sequence threshold AND a Bitcoin block height. Release is valid if either anchor confirms deadline passage. This eliminates single-anchor liveness failure. Builds on S193 time-lock anchoring primitives.

**Expiry enforcement:** If `current_anchor_age >= deadline` and release condition has not been satisfied, the contract enters EXPIRED state. In EXPIRED state only refund paths are valid (§Refund Semantics). No proof of delivery can flip an EXPIRED contract to RELEASED — this prevents long-delayed delivery claims against stale contracts.

---

## Dispute Resolution

At contract open, buyer and seller jointly commit to an arbiter via `arbiter_pk_hash = H(arbiter_pk)`. The arbiter has no knowledge of private blinding factors and cannot unilaterally extract funds.

**Dispute invocation:** Either party may invoke dispute before deadline by publishing a signed dispute notice referencing the contract's `task_spec_hash`. This freezes the contract — neither happy-path release nor silent refund is valid during active dispute.

**Arbiter decision as a Σ-protocol statement:** The arbiter issues a `DecisionProof`:

```
DecisionProof(
  decision,           -- RELEASE | REFUND | SPLIT(fraction)
  contract_id,        -- binding to this specific contract
  sigma_decision      -- Σ-protocol signature (S191) over (decision, contract_id)
)
```

`sigma_decision` is verified against `arbiter_pk` recovered from `arbiter_pk_hash`. This means the arbiter's decision is itself a cryptographic statement chained to the contract — arbiter cannot issue decisions outside the committed outcome set without producing a forgeable signature detectable by any third party (builds on S194 dispute chaining).

**Arbiter incentive alignment:** arbiter's fee is locked inside the contract as a third committed value `v_A` (arbiter_commit). Fee releases only after a valid `DecisionProof` is submitted. If arbiter never responds before a secondary deadline `arbiter_deadline > deadline`, fee forfeits to buyer and refund path opens automatically.

**SPLIT outcome:** If `decision = SPLIT(f)`, the verifier enforces `0 < f < 1` and routes `f * v_B` to seller and `(1-f) * v_B` to buyer. The split fraction is itself committed in the decision proof, preventing post-hoc renegotiation.

---

## Atomicity

Atomicity guarantee: both sides settle or neither does. Mechanism:

The contract maintains a single state machine with states: OPEN → (ACTIVE | EXPIRED) → (RELEASED | REFUNDED | SPLIT | DISPUTED → RESOLVED).

State transitions are guarded by predicate checks that consume the input commitments atomically:

1. Buyer's `buyer_commit` and seller's `seller_commit` are both required in every valid transition proof. Neither party can extract without the other's commitment being present and valid.
2. Release proof must satisfy the full relation R — partial proofs are rejected.
3. The verifier enforces that once a state transition is accepted, the contract's committed values are nullified (nullifier set, analogous to S195 atomicity primitives). No double-spend across state branches.

This rules out: seller claiming release without valid delivery proof; buyer reclaiming funds while release proof is pending; arbiter routing partial funds to one party without completing the full split allocation.

---

## Refund Semantics

Refund is valid iff:

```
current_anchor_age >= deadline
AND no valid release proof has been recorded
AND no active dispute is pending
```

OR:

```
dispute is RESOLVED with decision = REFUND
```

OR:

```
arbiter_deadline has passed with no DecisionProof submitted
```

Refund proof: buyer supplies `(v_B, r_B)` to open `buyer_commit`, verifier confirms contract is in EXPIRED or REFUND-RESOLVED state, and releases `v_B` to buyer's address. Seller's `seller_commit` is simultaneously nullified to prevent later recovery attempts.

Partial refund (SPLIT outcome) follows same logic with fractional allocation enforced by the split decision proof.

---

## Handoff

The following remain open and are scoped to successor summits:

**HTLC-style atomic-swap proof:** Current construction handles single-chain escrow. Cross-chain settlement requires a Hash Time-Locked Contract bridge where the release_preimage simultaneously unlocks funds on two chains. The Σ-protocol binding for cross-chain atomicity is not yet constructed — requires adaptor signatures or a cross-chain nullifier relay. Target: S196.

**Dispute-arbiter compromise threat model:** Current model assumes arbiter key is not compromised during contract lifetime. A compromised arbiter key allows forged DecisionProofs. Mitigations (threshold arbiter committee, time-delayed arbitration with appeal window, arbiter reputation staking) are unspecified. Target: S197.

**Multi-party generalization:** Current construction is two-party (buyer, seller) plus named arbiter. Generalization to N buyers / M sellers with weighted commitment aggregation, and to DAO-style arbiter pools, requires extending the directive equality predicate to vector commitments. Composability with S192 multi-directive binding is partially sketched but not formalized. Target: S198.

---

*CALM · 2026-05-20 · PARTIAL BAG*
