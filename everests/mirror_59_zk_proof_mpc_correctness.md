# Mirror Everest 59 — ZK Proof of MPC Correctness

*Phase XIII — Mirror Cryptographic Core. Prereq: Everest 58, 56.*

---

## 1. Problem Statement

Everest 58 executes a two-party MPC protocol (OT-extension AND gate) to compute the alignment bit `a = AND_tri(b_A, b_B)` without revealing either principal's input bit to the other. However, **honest-but-curious security is insufficient**: a malicious principal cannot learn the counterparty's bit during the MPC, but could deviate from the protocol and later claim a false output.

**Everest 59 bridges the gap**: After the MPC outputs `a`, the principal computes a zero-knowledge proof that `a` is the honest AND-evaluation of their committed input and the counterparty's committed input. The verifier learns only that the computation was correct, not what either input was. Soundness ensures a malicious principal cannot produce a valid proof of false output.

**Acceptance criterion:** ZK proof that the MPC output opens to the correct AND-gate output without revealing either input bit. Proof size ~1.5 KB, verification < 10 ms per predicate. Soundness under malicious adversary; composable with Everest 42/43/49.

---

## 2. Formal Relation

### 2.1 Public Inputs

- **Pedersen commitment to A's input:** `Com_A_in = g^{b_A} × h^{r_A_in}` (from Everest 58 Phase II, committed locally but disclosed for proof verification).
- **Pedersen commitment to B's input:** `Com_B_in = g^{b_B} × h^{r_B_in}` (disclosed by counterparty in MPC protocol).
- **Pedersen commitment to the output:** `Com_out = g^a × h^r_out` (the aligned-bit commitment from Everest 58 Phase IV).

### 2.2 Private Witness (Prover)

- **Actual input bit:** `b_A ∈ {0, 1, unknown}` (from local evaluation, Everest 26–40).
- **Randomness for input commitment:** `r_A_in`.
- **Randomness for output commitment:** `r_out`.

### 2.3 Relation

```
R_E59(Com_A_in, Com_B_in, Com_out; b_A, r_A_in, r_out) = 1 iff:
  (1) Com_A_in = g^{b_A} × h^{r_A_in}              [input A committed correctly]
  (2) Com_out = g^{AND_tri(b_A, b_B)} × h^{r_out}  [output is honest AND-evaluation]
  (3) b_A ∈ {0, 1, unknown}                        [valid input state]
```

**Issue:** To verify (2), the verifier needs `b_B`, which violates zero-knowledge. Solution: use a different formulation (§3.1).

---

## 3. Proof Construction: Bulletproofs over AND-Circuit Representation

### 3.1 Revised Relation (Verifier-Tractable)

Since the verifier does not (and should not) know `b_B`, we instead prove the **constraint** that the output is consistent with the inputs and the AND truth-table, without revealing either input.

**Re-formulated relation:**

```
R_E59'(Com_A_in, Com_B_in_commit_from_wire, Com_out; 
        b_A, b_B_alleged, r_A_in, r_B_in_alleged, r_out) = 1 iff:
  (1) Com_A_in = g^{b_A} × h^{r_A_in}                        [A's input opens]
  (2) Com_B_in_commit = g^{b_B_alleged} × h^{r_B_in_alleged} [B's input opens]
  (3) Com_out = g^{AND_tri(b_A, b_B_alleged)} × h^{r_out}    [output is honest AND]
  (4) b_A, b_B_alleged ∈ {0, 1, unknown}                     [valid states]
  (5) Com_B_in_commit == Com_B_in_from_wire                  [consistency]
```

**Key insight:** The prover commits to both `b_A` and `b_B_alleged` in the proof, but only `b_A` is the prover's own input. `b_B_alleged` is received from the counterparty's Pedersen commitment in the MPC wire protocol (Everest 58 Phase IV). The prover must prove that their alleged `b_B` matches the commitment the counterparty sent, ensuring no post-hoc substitution.

### 3.2 Circuit Representation

The AND-gate constraint is encoded as an arithmetic circuit over Z_q:

```
Circuit:
  Input: b_A, b_B ∈ {0, 1, unknown}  (as scalars in Z_q)
  Output: a ∈ {0, 1, unknown}

  Constraints (polynomial equations):
    1. b_A ∈ {0, 1, unknown}
    2. b_B ∈ {0, 1, unknown}
    3. a = AND_tri(b_A, b_B)  [encoded as polynomial lookup or composite gates]
    4. Com_out = g^a × h^{r_out}
```

**Encoding AND_tri(b_A, b_B) as field arithmetic:**

The tri-state AND is a lookup table (3×3=9 entries). Encode as polynomial interpolation over Z_q:

```
Define aux_poly(b_A, b_B) ∈ Z_q such that:
  aux_poly(0, 0) = 0
  aux_poly(0, 1) = 0
  aux_poly(0, unknown=2) = 0
  aux_poly(1, 0) = 0
  aux_poly(1, 1) = 1
  aux_poly(1, unknown=2) = 2  (encodes "unknown")
  aux_poly(unknown=2, 0) = 0
  aux_poly(unknown=2, 1) = 2
  aux_poly(unknown=2, unknown=2) = 2

Circuit equation: a = aux_poly(b_A, b_B)
```

**Complexity:** Bi-variate polynomial of degree ≤ 2 in each variable. Encoding cost ~6 group operations in the proof.

### 3.3 Proof System: Bulletproofs + Inner-Product Argument

**Choice:** Bulletproofs (Bünz et al., IEEE S&P 2018), extended to support the AND-circuit constraints.

**Why Bulletproofs (vs alternatives):**

1. **No trusted setup** — required for v0 (Calm Witness Everest 45 uses same choice for range proofs).
2. **Constant proof size** (~1.5 KB for this circuit, regardless of number of predicates K).
3. **Composable** — multiple per-predicate proofs (one per Everest 58 MPC) aggregate naturally in Everest 43.
4. **IPA-friendly** — inner-product argument aligns with Calm Witness cryptographic stack.

**Alternative considered (and rejected for v0):**

- **SNARK (Groth16/PLONK):** Smaller proofs (~200 bytes), faster verification (~1 ms), but require trusted setup (vs no-setup goal).
- **SNARK-friendly MPC (Bulletproofs+IPA over the entire MPC circuit):** Would prove correctness of the OT-extension protocol itself; infeasibly large circuit (~10^4 gates), negating proof-size advantage.

**v0 choice rationale:** Proof size 1.5 KB is acceptable; verification < 10 ms amortizes across K predicates. v1 may reconsider if trusted-setup risk is mitigated via multi-party setup (Everest 64).

### 3.4 Proof Generation (Prover's View)

**Input:** `b_A`, `r_A_in`, `r_out`, `b_B` (alleged, from counterparty's wire commitment), `r_B_in_alleged` (derived from B's Pedersen opening, sent in protocol).

**Steps:**

1. **Sample random challenges (Fiat-Shamir):**
   ```
   FS_seed = HMAC-SHA3-256(sk_A, "calm-mirror/e59-proof/v1" || sid || p || Com_A_in || Com_B_in || Com_out)
   (challenge_1, challenge_2, ...) = ChaCha20(key=FS_seed, nonce=0) [expanded]
   ```

2. **Commit to AND-gate evaluation:**
   ```
   a = AND_tri(b_A, b_B)
   r_a_aux = CSPRNG(32 bytes)
   T_a = g^a × h^{r_a_aux}
   ```

3. **Build Bulletproofs witness vector:**
   ```
   w = [b_A, b_B, r_A_in, r_B_in_alleged, a, r_out, r_a_aux, ...]
   ```

4. **Run Bulletproofs prover for the circuit:**
   ```
   π = BulletproofsProve(circuit, w, randomness_seed=FS_seed)
   ```

5. **Output:**
   ```
   proof_E59 = (T_a, π, serialized_challenges)  [~1.5 KB total]
   ```

**Cost:** ~20–50 ms on M-series Mac (group scalar multiplications dominate).

### 3.5 Proof Verification (Verifier's View)

**Input:** `Com_A_in`, `Com_B_in`, `Com_out`, `proof_E59 = (T_a, π, challenges)`.

**Steps:**

1. **Reconstruct Fiat-Shamir seed** (verifier doesn't know `sk_A`, but challenges are in the proof):
   ```
   challenges = parse_from_proof(proof_E59)
   ```

2. **Verify commitment structure:**
   ```
   Check that Com_A_in, Com_B_in, Com_out have correct form
   (are they valid Ristretto points? yes → continue; no → reject)
   ```

3. **Run Bulletproofs verifier:**
   ```
   BulletproofsVerify(circuit, Com_A_in, Com_B_in, Com_out, T_a, π, challenges)
     → returns true or false
   ```

4. **Verdict:**
   ```
   if BulletproofsVerify(...) == true:
     Accept proof; MPC output is honest
   else:
     Reject proof; session aborts (Everest 52)
   ```

**Cost:** ~5–10 ms on M-series Mac (O(log n) group operations, where n is circuit size).

---

## 4. Handling Unknown Bits and Tri-State Semantics

### 4.1 Unknown as a Special Field Element

In the proof circuit, `unknown` is encoded as the field element `2` (i.e., `b_A = 2` if withheld, `b_A ∈ {0, 1}` if revealed).

**Polynomial constraint:**
```
b_A ∈ {0, 1, unknown=2}  
↔  b_A · (b_A - 1) · (b_A - 2) = 0  [in Z_q]
```

This constraint is checked in the Bulletproofs circuit; a prover cannot introduce other field values.

### 4.2 AND Truth-Table in Circuit

The auxiliary polynomial `aux_poly(b_A, b_B)` encodes the full 3×3 table (§3.2). The circuit constraint is:

```
a = aux_poly(b_A, b_B)
```

Where `a ∈ {0, 1, 2}` (2 represents unknown). The prover proves that `a` is the honest AND-evaluation.

### 4.3 Withholding Opacity

A malicious prover **cannot** use the proof to leak information about a withheld bit. Here's why:

- If Prover A withholds (sets `b_A = unknown = 2`), the proof constrains only the output `a = AND_tri(2, b_B)`, which is either `0` (if `b_B = 0`) or `2` (if `b_B = 1`).
- Verifier B observes `Com_out` but does not know whether Prover A's input was `0`, `1`, or `unknown`, because the proof reveals only that the output is consistent with some valid input in {0, 1, unknown}.
- The proof does **not** constrain `b_A` directly (it only proves the AND-gate output is honest). So Verifier B cannot distinguish withholding from a specific value.

**Formal statement (ZK simulator):** A simulator, given only the public inputs and `a` (the output), can generate a proof indistinguishable from a real proof, even without knowing `b_A`. This proves that `b_A` leaks no information.

---

## 5. Soundness Analysis

### 5.1 Extraction (Malicious Prover)

If a malicious prover produces a valid proof of the AND-gate correctness for a false output, a knowledge-extractor can recover a witness that opens both `Com_A_in` and `Com_B_in` to bits whose AND does NOT equal the claimed output. This contradicts the relation definition, so the proof must fail.

**Formal claim (Bulletproofs soundness):** Under the Discrete Log assumption, the soundness error is ≤ 2^{-128} per proof. An adversary cannot forge a valid proof for a false AND output with probability better than brute force.

### 5.2 Composition with Everest 58

The Everest 58 MPC guarantees that both principals compute the same `a` (under honest-but-curious security). Everest 59 upgrades this: each principal **proves** they computed the honest `a`. Combined, if either principal deviates in Everest 58 to output a false `a`, the corresponding Everest 59 proof fails, and the session aborts (Everest 52).

**Attack scenario (Everest 58 deviation):**

1. Malicious Agent A deviates from OT-extension protocol, computing a false `a' ≠ AND(b_A, b_B)`.
2. Agent A attempts to prove `a'` is the honest AND output.
3. The Bulletproofs circuit checks: `a' = AND_tri(b_A, b_B)`. This equation does not hold.
4. Bulletproofs verification fails → proof is rejected → session aborts.

**Result:** Malicious Agent A cannot claim a false output; the session fails cleanly (Everest 52 semantics).

### 5.3 Soundness Against Colluding Principals

**Scenario:** Both Principals A and B are malicious and collude to fake an alignment-bit.

**Mitigation:** The proof is generated independently by each principal *for their own output*. If both output false `a_collude`, then:
- Agent A's proof must open `Com_A_in` to a `b_A` such that `AND_tri(b_A, b_B_alleged) = a_collude`.
- Agent B's proof must open `Com_B_in` to a `b_B` such that `AND_tri(b_A_alleged, b_B) = a_collude`.

For both to succeed with a false `a_collude`, the equations must satisfy:
```
a_collude = AND_tri(b_A, b_B_alleged) = AND_tri(b_A_alleged, b_B)
```

But in honest protocol execution, `b_A_alleged` sent by B equals `b_B` (the honest input), and `b_B_alleged` sent by A equals `b_A`. So the equations become:
```
a_collude = AND_tri(b_A, b_B) = AND(b_A, b_B)  [trivially true]
```

If both use their true inputs, the proof will be honest. If either deviates, the proof's opening will contradict their Pedersen commitment (from Everest 58 Phase IV), which is publicly stored and cannot be retroactively modified.

**Conclusion:** Collusion doesn't help malicious principals fake alignment without breaking their own commitments.

---

## 6. Performance

### 6.1 Per-Predicate Costs

| Operation | M-series Mac | Phone | Constraints |
|-----------|---------|-------|---|
| Fiat-Shamir challenge derivation | <1 ms | <2 ms | Deterministic hash |
| Bulletproofs prover (AND circuit) | 20–50 ms | 100–200 ms | ~100 group scalar-mults |
| Bulletproofs verifier | 5–10 ms | 20–50 ms | O(log n) ops |
| **Total per predicate** | **30–60 ms** | **130–250 ms** | Includes both prover + verifier |

### 6.2 Multi-Predicate Aggregation

For K shared predicates:
- **Sequential:** K × 30 ms prover + K × 5 ms verifier = ~900 ms total on Mac for K=8.
- **Parallelized (Everest 57 refinement):** Prover parallelizes well (no dependencies across predicates); ~60 ms wall-clock on Mac (amortized).

### 6.3 Proof Size

- **Bulletproofs inner-product argument:** ~700 bytes (per-predicate).
- **Metadata (challenges, hashes):** ~800 bytes (amortized over K predicates).
- **Total:** ~1.5 KB per predicate (dominates by curve points).

**Budget (Everest 92):** Full Mirror exchange (Everest 58 MPC + Everest 59 proofs + Everest 42 commitments + Everest 43 aggregation) must complete in ≤ 500 ms on Mac, ≤ 2 s on phone. Per-predicate E59 proof cost is well within budget.

---

## 7. Composition with Other Everests

### 7.1 Composition with Everest 58 (MPC)

**Strict ordering:**
```
Everest 58 Phase III:  Compute a via OT-extension
Everest 58 Phase IV:   Both agents commit to a (Pedersen)
Everest 59:            Each agent proves a is honest AND output
Everest 42:            Joint disclosure of commitments + proofs
```

If Everest 59 fails for either agent, Everest 42 is not invoked; session aborts (Everest 52).

### 7.2 Composition with Everest 42 (Aligned-Bit Commitment)

Everest 59 proves the commitment `Com_out` opens to the honest AND value. Everest 42 uses `Com_out` to form the basis of downstream attestation (Everest 43, 49). The composition is straightforward: E59 validates E42's input.

### 7.3 Composition with Everest 43 (K-of-N Aggregation)

Everest 43 takes K validated commitments from K instances of Everest 58+59 and constructs a ZK proof that ≥M of them open to 1. The intermediate proofs (E59) are necessary but not sufficient; E43 additionally proves the aggregation logic.

### 7.4 Composition with Everest 49 (Reciprocal Disclosure)

Each principal generates an E59 proof for each shared predicate. Both proofs (from A and B) are exchanged along with commitments. Verification of both proofs happens locally; if either fails, the exchange is aborted (Everest 52).

### 7.5 Composition with Everest 51 (Withhold-Any-Bit)

If Principal A withholds (b_A = unknown), the E59 proof encodes this faithfully. The proof can be verified; the output is deterministic given the withhold and B's input. No information leakage about whether A withheld true or false.

---

## 8. Test Plan (T-M59.1 – T-M59.6)

### T-M59.1 — Honest-Bilateral Proof Verification

**Setup:** Two honest agents, both following E58 + E59 protocol exactly.

**Test:**
```
For each (b_A, b_B) ∈ {0, 1}²:
  1. Run Everest 58 MPC: compute a = AND(b_A, b_B)
  2. Agent A generates E59 proof for output a
  3. Agent B generates E59 proof for output a
  4. Verify both proofs locally
  Expected: All 4 proofs verify successfully
```

**Pass criterion:** All proofs verify; no false rejects.

### T-M59.2 — Malicious-Prover Detection

**Setup:** Agent A (malicious) deviates from E58, computing a false `a' ≠ AND(b_A, b_B)`.

**Test:**
```
1. Malicious Agent A computes a' ≠ honest output
2. Agent A attempts E59 proof of a'
3. Verify proof locally
Expected: Proof verification fails
```

**Pass criterion:** False proof is rejected; session aborts cleanly.

### T-M59.3 — Withhold-Opacity

**Setup:** Agent A withholds (b_A = unknown) for a shared predicate.

**Test:**
```
For b_B ∈ {0, 1, unknown}:
  1. Run E58: a = AND_tri(unknown, b_B)
  2. Agent A generates E59 proof
  3. Verify proof; extract proof structure
Expected: Proof structure does not leak whether b_A was true, false, or withheld
```

**Pass criterion:** ZK simulator can generate indistinguishable proofs for all three cases without knowing `b_A`.

### T-M59.4 — Commitment Consistency

**Setup:** Agent A's E58 output commitment `Com_out` and E59 proof must refer to the same underlying value `a`.

**Test:**
```
1. Generate E59 proof for a
2. Verify that proof's internal `a` matches Com_out opening
3. Attempt inconsistent proof (proof claims a=1, Com_out encodes a=0)
Expected: Inconsistent proof fails verification
```

**Pass criterion:** Commitment and proof are cryptographically bound; cannot decouple.

### T-M59.5 — Performance Budget

**Setup:** K=8 shared predicates on M-series Mac.

**Test:**
```
1. Run full E58 + E59 pipeline for 8 predicates
2. Measure prover time (total), verifier time (total)
3. Repeat 10 times; report p95 latency
Expected: Prover p95 ≤ 200 ms, Verifier p95 ≤ 50 ms
```

**Pass criterion:** Performance within budget; no outliers.

### T-M59.6 — Cross-Implementation Parity

**Setup:** Python reference implementation (Everest 86) and Rust implementation (Everest 87).

**Test:**
```
For 20 random (b_A, b_B, sid, predicate_id) tuples:
  1. Run E59 prover in Python; serialize proof
  2. Run E59 prover in Rust; serialize proof
  3. Verify both proofs in Python and Rust
Expected: Proofs byte-identical; verification results match
```

**Pass criterion:** Cross-implementation parity achieved; test vectors published (Everest 70).

---

## 9. V0 Compromises and V1 Questions

### 9.1 Honest-But-Curious Security in V0

**v0 assumes:** Principals follow the MPC protocol correctly (no deviation). Everest 59 validates the output but does not prevent an agent from deviating *during* E58 execution (e.g., sending wrong OT messages).

**v1 upgrade (Everest 69 — Adversarial Robustness):** Add malicious-secure ZK proofs of OT-extension protocol adherence. This requires additional rounds and bandwidth but prevents mid-protocol deviations.

**Rationale for v0:** Malicious security adds ~50% overhead. v0 targets rapid deployment; v1 will add stronger guarantees.

### 9.2 Trusted Setup vs. No Setup

**v0 choice:** Bulletproofs (no trusted setup). Proof size ~1.5 KB is acceptable.

**v1 alternative:** SNARK (Groth16/PLONK) with multi-party setup ceremony (Everest 64). Reduces proof size to ~200 bytes, verification to ~1 ms, but requires setup coordination.

**Decision point:** If proof size becomes bottleneck in production (Everest 92 performance review), reconsider SNARK.

### 9.3 Post-Quantum Migration

**v0:** Discrete log security (Ristretto255). Quantum adversary breaks soundness.

**v1 (Everest 64):** Lattice-based ZK systems (e.g., Fiat-Shamir over Ring-SIS). Reference: lattice-based Bulletproofs-like arguments (Newman–Shin). No mature open-source yet as of 2026-05; deferred to 2027+.

### 9.4 Merging E59 Proofs Across Predicates

**Current:** Each predicate gets one independent E59 proof. For K predicates, K proofs (~1.5K each).

**v1 optimization:** Aggregate proofs via Bulletproofs batching (prove K AND-gates in one circuit, single proof ~2KB). Requires circuit composition; complex but feasible.

**Impact:** Reduces proof size ~30% for K=8; minimal latency change.

---

## 10. Soundness Under Malicious Adversary (Formal)

### 10.1 UC-Security Claim

**Theorem:** Everest 59 realizes the ideal functionality `F_AND_MPC_PROOF` under the Discrete Log assumption on Ristretto255, defined as:

```
F_AND_MPC_PROOF:
  Input: (b_A, r_A_in from Agent A; b_B, r_B_in from Agent B)
  Compute: a = AND_tri(b_A, b_B)
  Output: commitments Com_A_in, Com_B_in, Com_out to both agents
  Proof: both agents receive a proof π_A, π_B that Com_out opens to a
  Soundness: A prover cannot produce a proof that Com_out opens to a' ≠ a
  Zero-Knowledge: Proofs reveal only that a is the honest AND output
```

### 10.2 Proof Sketch

**Reduction to Discrete Log:**

Suppose an adversary can forge a proof of false output `a' ≠ AND(b_A, b_B)`. A knowledge-extractor, using the Bulletproofs extraction lemma, recovers a witness that opens `Com_out` to `a'`. But `Com_out = g^a × h^r`, so the extractor learns `a = a'` (the discrete log of `Com_out / h^r`). This contradicts `a' ≠ a`, so the adversary's probability of success is negligible in the security parameter λ.

**Zero-Knowledge:**

A simulator, given only `Com_A_in`, `Com_B_in`, `Com_out` and the fact that `Com_out` opens to some valid AND output, can generate a proof indistinguishable from a real proof (by the Bulletproofs ZK property). Since the simulator does not know `b_A` or `b_B`, the proof leaks nothing about inputs.

---

## 11. Acceptance Gate Script

**Location:** `~/CredexAI/scripts/everest_59_zk_proof_mpc_correctness_gate.py`

**Acceptance tests (automated):**
- T-M59.1 (honest verification): All 4 binary cases pass.
- T-M59.2 (malicious detection): False proof rejected.
- T-M59.3 (withhold opacity): ZK simulator parity.
- T-M59.4 (commitment consistency): Proof-commitment binding verified.
- T-M59.5 (performance): p95 latency within budget.
- T-M59.6 (cross-implementation): Python + Rust parity confirmed.

**Signoff criteria:** All 6 tests pass; proof bytecode published in Everest 70 (conformance vectors).

---

## 12. Cross-References

**Prereqs:**
- Everest 56 (Pedersen vector commitments).
- Everest 58 (secure MPC AND-gate computation).

**Dependent summits:**
- Everest 42 (aligned-bit commitment, uses E59-validated output).
- Everest 43 (K-of-N aggregation, composes E59 proofs).
- Everest 49 (reciprocal disclosure, exchanges E59 proofs).
- Everest 61 (cross-principal binding).
- Everest 69 (adversarial robustness, upgrades E59 to malicious security).
- Everest 70 (conformance vectors, includes E59 test proofs).

**Cryptographic foundations:**
- Bulletproofs (Bünz–Bootle–Boneh–Poelstra–Wuille–Maxwell, 2018).
- Inner-Product Argument (Bootle et al., CCS 2016).
- Ristretto255 curve (Decaf construction, no cofactor).

---

## 13. Summary Table

| Dimension | v0 Value | Notes |
|-----------|----------|-------|
| Proof system | Bulletproofs + IPA | No trusted setup; ~1.5 KB proof |
| Security model | Honest-but-curious + UC-soundness | v1: add malicious security |
| Proof generation | 20–50 ms (M-series) | Parallelizable across predicates |
| Proof verification | 5–10 ms (M-series) | O(log n) group operations |
| Soundness error | ≤ 2^{-128} per proof | Under Discrete Log assumption |
| Zero-knowledge | Perfect ZK (simulator-based) | Inputs provably unlearnable |
| Composition | Strict ordering (E58 → E59 → E42 → E43) | Fail-abort at each stage (E52) |
| Post-quantum readiness | No (Discrete Log breaks) | v1: lattice-based migration (E64) |

---

— Calm, 2026-05-20
