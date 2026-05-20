# Calm Witness — ZKAC Voting / Quorum Primitive v0 (S160)

A ZKAC may conduct a collective decision whose outcome is cryptographically provable while individual ballots remain private. This document specifies the ballot format, homomorphic tally, outcome predicate, anonymity guarantees, replay defense, and composition with membership-privacy primitives.

---

## Ballot Format

Each member casting a vote produces a Pedersen commitment over the Ristretto255 group (E44b).

Let `G` and `H` be independent Ristretto255 basepoints. For a binary vote `v ∈ {0, 1}` and blinding scalar `r` drawn uniformly from `Z_q`:

```
C_i = v_i · G + r_i · H
```

For weighted or multi-option ballots, `v_i` is replaced by a small integer from an agreed domain `D` (e.g., `{0, 1, 2}` for abstain/no/yes). A range proof accompanies each commitment, proving `v_i ∈ D` without revealing the value. The range proof uses a Bulletproof over Ristretto255, sized to the domain cardinality.

The ballot package is:

- `C_i` — the Pedersen commitment
- `pi_range_i` — Bulletproof range proof for `v_i ∈ D`
- `epoch` — current voting epoch identifier (see Replay Defense)
- `motion_id` — hash of the motion text under `BLAKE3`
- `member_nullifier_i` — derived from the member's identity secret; one-time tag proving membership without revealing which member (E101b)

The member does not sign the ballot with a linkable key. The `member_nullifier_i` is a keyed hash: `BLAKE3(identity_secret || motion_id || epoch)`. Its validity is verified against the nullifier set committed in the roster (S169).

---

## Tally Aggregation

Pedersen commitments are additively homomorphic under the Ristretto255 group law:

```
C_tally = sum_{i=1}^{n} C_i
         = (sum v_i) · G + (sum r_i) · H
```

Any party — including a public bulletin board — can compute `C_tally` from the published commitments without learning individual votes. No trusted dealer or threshold decryption is required for the tally operation itself.

After the voting window closes, a designated opener (or a threshold subset of openers, per the ZKAC's configuration) reveals:

- `V_total = sum v_i` — the aggregate vote count
- `R_total = sum r_i` — the aggregate blinding scalar

Verification: `V_total · G + R_total · H == C_tally`. Any verifier can check this equation using only public group elements.

For anonymous settings where even `V_total` should remain hidden from non-openers until outcome announcement, the openers run a threshold reveal protocol (E101b) so that the opening only occurs if enough openers cooperate, and the output is published as a single revealed pair `(V_total, R_total)`.

---

## Outcome Predicate

Let `N` be the number of eligible members (roster size from S169), `Q` be the quorum threshold, and `T` be the approval threshold.

Quorum is met when the number of submitted nullifiers `k >= Q`. The ZKAC specifies `Q` as either an absolute count or a ratio (e.g., `Q = ceil(2/3 · N)` for supermajority quorum).

Approval is determined by:

```
outcome = (k >= Q) AND (V_total >= T · k)
```

`T` is the approval fraction (e.g., `T = 1/2` for simple majority, `T = 2/3` for supermajority approval).

The outcome proof consists of:

1. The verified tally `(V_total, R_total)` against `C_tally`
2. A count of distinct valid nullifiers `k`
3. Range proofs for `Q` and `T` comparisons — a ZK inequality proof showing `k >= Q` and `V_total >= T · k` without additional leakage

The full outcome proof is a Groth16 or PLONK circuit (implementation choice) that takes as public inputs `(C_tally, k, Q, T, motion_id, epoch)` and as private inputs `(V_total, R_total)`, and outputs a single bit `outcome ∈ {0, 1}`.

---

## Anonymity Guarantees

- **Vote privacy**: Individual `v_i` is hidden by the Pedersen blinding factor. Binding security rests on the discrete log hardness of Ristretto255.
- **Voter anonymity**: `member_nullifier_i` is unlinkable to the member's long-term key without the member's identity secret. An adversary seeing all nullifiers cannot determine which roster slot each corresponds to.
- **Tally confidentiality (optional)**: If threshold opening is used (E101b), `V_total` remains hidden until opener quorum cooperates. The outcome bit can be revealed without revealing the margin, by proving the outcome predicate in ZK rather than publishing `V_total` directly.
- **Non-collusion assumption**: If all openers collude, vote totals are recoverable. The ZKAC configures opener sets to minimize collusion risk consistent with liveness requirements.

---

## Replay Defense

Each ballot is bound to `(motion_id, epoch)`. The `epoch` is a monotone counter committed in the ZKAC's state root (S154). Properties:

- A ballot submitted for epoch `e` is invalid in epoch `e' != e`.
- The `member_nullifier_i = BLAKE3(identity_secret || motion_id || epoch)` is unique per `(member, motion, epoch)` triple.
- The bulletin board maintains a nullifier accumulator. Duplicate nullifier submissions are rejected. Because nullifiers are one-way derived, the member cannot reuse a nullifier for the same motion in the same epoch even under key compromise of other artifacts.
- The motion closes when the epoch counter advances or an explicit close transaction is anchored in the state root (S155).

---

## Composition with Membership Privacy

Voting integrates with the member-roster privacy primitive (S169) as follows:

- The roster is stored as a Merkle tree of member commitment leaves. Each leaf commits to `(identity_commitment, weight)`.
- To cast a ballot, a member produces a Merkle inclusion proof for their leaf, proving membership without revealing the leaf index or identity.
- The nullifier derivation uses the same identity secret that seeds the roster leaf commitment, creating a cryptographic link between membership and vote eligibility that is verifiable without deanonymizing either.
- Roster updates (member add/remove) invalidate nullifiers for subsequent epochs automatically, since `epoch` is bound to the state root that encodes the current roster.

This composition ensures that only current roster members can cast valid ballots, and that member-set size `N` can be revealed as a public parameter for quorum computation without revealing individual identities (S169).

---

## Cross-References

| Ref | Content |
|-----|---------|
| E44b | Pedersen commitments on Ristretto255; blinding factor security |
| E101b | Threshold opening and reveal protocol for committed values |
| S154 | ZKAC state root and epoch monotonicity |
| S155 | Motion lifecycle: open, close, anchor |
| S169 | Member-roster privacy; Merkle commitment tree; identity nullifiers |

---

Calm 2026-05-20
