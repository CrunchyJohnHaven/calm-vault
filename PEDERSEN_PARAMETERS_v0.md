# Pedersen Commitment Parameters — Calm Witness v0

**Everest 44 acceptance artifact. Sister doc to [`calm_witness/pedersen.py`](../../CredexAI/calm_witness/pedersen.py).**

Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"`.

> **2026-05-20 superseded notice.** This doc captures the v0 RFC 3526 MODP-14 commitment scheme as initially bagged for Everest 44. After ratification of Path B in [`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`](CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md), the canonical Calm Witness commitment scheme is **Ristretto255 over Curve25519**, native to Calm Pact v0.1 and to Bulletproofs at Everest 45. The MODP-14 scheme described below is preserved as a **v0-historical reference**; the next active commitment work is **Everest 44b — Pedersen on Ristretto255** (TODO; new sibling doc and `pedersen_ristretto.py`). Downstream consumers (Everests 45, 46, 47, 60, 67, 101) compose against Ristretto, not against this doc.

---

## 1. The scheme

Pedersen commitments are the foundational ZK primitive for Calm Witness. A commitment to a behavioral-biometric distance value `d` with randomness `r` is:

```
C = g^d · h^r  (mod p)
```

The committer can later open the commitment by revealing `(d, r)`. A verifier checks `C ≡ g^d · h^r mod p`. The scheme is:

- **Perfectly hiding** — for uniformly random `r ∈ [1, q-1]`, the term `h^r` is uniformly distributed in the prime-order subgroup, so `C` reveals zero information about `d`.
- **Computationally binding** — finding two distinct openings `(d₁, r₁)` and `(d₂, r₂)` of the same `C` requires computing `dlog_g(h)`, which is hard in the chosen group.

Calm Witness uses Pedersen commitments to bind behavioral-biometric distance values into ZK proofs without revealing the distance itself. The disclosure layer (Everest 67) returns only a single boolean — `distance < τ` or `distance ≥ τ` — using the range-proof construction in Everest 45.

## 2. Parameter selection

### 2.1 The group: RFC 3526 MODP Group 14

We use the 2048-bit safe prime `p` from [RFC 3526 §3](https://www.rfc-editor.org/rfc/rfc3526) (also known as "MODP Group 14"). This group has been used in IPsec IKE since 2003 and is widely vetted. The full hexadecimal value of `p`:

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```

`p` is a Sophie Germain prime — `q = (p-1)/2` is also prime. This is the safe-prime structure that guarantees the only nontrivial subgroup of `(Z/pZ)*` has order `q`. We work entirely within that prime-order subgroup.

### 2.2 The first generator: g = 2

The standard RFC 3526 generator `g = 2` is a quadratic residue and a generator of the order-`q` subgroup (this is what "safe prime" buys us — small generators are subgroup generators).

### 2.3 The second generator: h = derived from public seed

The Pedersen scheme requires a second generator `h` such that `dlog_g(h)` is unknown. If `h` is derived from a trusted setup or a known relation, the binding property collapses. We avoid this with a **"nothing up my sleeve"** construction.

**Public seed:**
```
H_SEED = b"calm-witness/pedersen/h/v0/2026-05-20"
```

**Derivation:**

1. Expand the seed to ~2048 bits via SHA-256 in counter mode:
   ```
   t = SHA256(0||seed) || SHA256(1||seed) || ... || SHA256(7||seed)
   ```
   Then truncate to exactly 2048 bits and interpret as a big-endian integer.

2. Reduce `t` mod `p`.

3. Compute `h = t² mod p`. Squaring lands `t` in the prime-order subgroup of order `q` (because `p` is a safe prime, the squared map has image exactly the subgroup of size `q`).

4. Reject degenerate cases (`h ∈ {0, 1, p-1}`), repeating with a perturbed seed if necessary — this is astronomically unlikely.

**Why this is safe:**

- Any party can re-derive `h` from `H_SEED` and confirm it matches the reference value. No trust in any single party is required.
- The discrete log of `h` base `g` is unknown to anyone, because `h` was determined by a public hash output before any party could compute the dlog.
- Squaring is a natural projection into the prime-order subgroup, requiring no Legendre-symbol tests.

**Reference value:**

Computing `derive_h(H_SEED)` per the construction above yields the integer `H` printed by `python -c "from calm_witness.pedersen import H; print(hex(H))"`. The full hex value is included as a fixture in `calm_witness/test_pedersen.py`.

## 3. Operating envelope

| Quantity | Bound |
|---|---|
| Group order `q` | ~2047 bits |
| Committed value `m` | reduced mod `q` before exponentiation |
| Randomness `r` | sampled uniformly from `[1, q-1]` |
| Commitment `C` | 2048-bit value, stored as 512-hex-char string |
| Commit op cost | ~2 modexps over 2048-bit prime, ~1-2 ms on M-class CPU |
| Verify op cost | ~2 modexps over 2048-bit prime, ~1-2 ms |

For a typical Calm Witness session, two commits (handwriting distance, voice-transcription distance) and one homomorphic addition are required during hydration. The cost budget is dominated by the predicate evaluator and the Σ-protocol transcript, not by the commitments themselves.

## 4. Homomorphism

Pedersen commitments are additively homomorphic:

```
C₁ · C₂ = g^m₁ h^r₁ · g^m₂ h^r₂ = g^(m₁+m₂) · h^(r₁+r₂)  (mod p)
```

So `Com(m₁; r₁) · Com(m₂; r₂) = Com(m₁ + m₂; r₁ + r₂)`. Calm Witness uses this in Everest 38 (multi-modal distance fusion) — the prover commits to handwriting distance and voice distance independently, then composes them into a single commitment without revealing either component.

## 5. Soundness checks performed by the module

At every load (and explicitly in `verify_parameters()` for the gate script):

1. `p` is 2048 bits.
2. `p` is prime (Miller-Rabin, 20 rounds for the gate; 40 rounds available).
3. `q = (p-1)/2` is prime.
4. `2q + 1 = p` (safe-prime structure).
5. `g` is in the prime-order subgroup: `g^q ≡ 1 mod p`.
6. `g` is not trivial (`g ∉ {0, 1, p-1}`).
7. `h` is in the prime-order subgroup.
8. `h` is not trivial.
9. `h ≠ g`.
10. `derive_h(H_SEED) == H` — the cached `h` matches re-derivation from the public seed.

A counterparty verifying a Calm Witness proof can re-run all 10 checks against the parameters bundled with the proof transcript before accepting.

## 6. Migration plan

This is v0. Two known successor groups will be considered:

- **ristretto255** (Everest 61, parameter ceremony): once a vetted Python binding is available in the Calm vault environment. Identical interface (`commit`, `verify_opening`, `add_commitments`); ~50× faster group ops; smaller commitments (32 bytes vs 256 bytes).
- **Lattice-based commitments** (Everest 96, post-quantum migration): when post-quantum security becomes a deployment requirement. Larger transcripts but no discrete-log dependence.

The `pedersen.py` module's public API is the migration boundary: `Commitment`, `Opening`, `commit`, `verify_opening`, `add_commitments`. The group internals can be swapped without affecting predicate evaluators, the Σ-protocol, or the chain schema.

## 7. Threat model deltas vs the v0 protocol spec

The Pedersen scheme defends only the commitment layer. Other adversary classes from `ZKBB_USER_PROTOCOL_v0.md §2`:

- **Honest-but-curious counterparty** — defended: hiding property is perfect.
- **Lying calling agent** — partially defended: the agent could commit to a fake distance, but the eventual range proof (Everest 45) will bind the distance to the comparator's output via a separate circuit constraint. Pedersen alone does not prevent this.
- **Replay** — out of scope here; defended at the proof layer (Everest 75, counterparty nonce binding).
- **Substitution (different principal)** — out of scope here; defended by template binding (Everest 46, `principal_commitment` slot in the proof).

## 8. Cross-references

- Protocol spec: [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)
- Route map: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md), Everest 44
- Naming lock: [`NAMING_AND_BRANDING.md`](NAMING_AND_BRANDING.md), §5
- Sister primitive: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) — Calm Pact's v0.1 amendment locks Ristretto255 (Curve25519); this v0 MODP-14 doc is superseded by the forthcoming `EVEREST_44b_PEDERSEN_RISTRETTO_v0.md` (see superseded notice at the head of this file).
- Reference impl: `~/CredexAI/calm_witness/pedersen.py`
- Test suite: `~/CredexAI/calm_witness/test_pedersen.py` (25 cases, all green)
- Gate script: `~/CredexAI/scripts/everest_44_zkbb_pedersen_gate.py`

---

**Anchored by Calm, 2026-05-20.**
