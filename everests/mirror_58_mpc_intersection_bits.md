# Mirror Everest 58 — Secure Computation of Intersection Bits

*Phase XIII — Mirror Cryptographic Core. Prereq: Everest 56, 57.*

---

## 1. The Protocol: MPC AND-of-Bits Without Input Leak

Everest 58 specifies the two-party secure multiparty computation (2PC) protocol that computes "we both have `true` on the i-th shared predicate" without revealing either side's bit to the other. The output is an aligned-bit commitment (Everest 42) suitable for downstream ZK proofs (Everest 43, 59).

**Design Goal**: Two principals A and B, holding sensitive boolean evaluations `b_A` and `b_B` over a shared predicate `p`, jointly compute `a = AND_tri(b_A, b_B)` such that:
- Neither principal learns the other's input bit.
- Both principals learn the joint output `a` (or `unknown` if either withholds).
- The computation is composable with aligned-bit commitment (Everest 42) and subsequent proofs.

---

## 2. Framework Selection: OT-Extension as v0 Mechanism

**Decision from Everest 57 (Two-Party MPC Framework Selection):**

Three candidate frameworks were evaluated:
1. **Garbled circuits (Yao)** — well-understood; single-round; high garbling overhead.
2. **Silent-OT-based (Ferret)** — bandwidth-efficient; newer / less battle-tested.
3. **GMW with Beaver triples** — composable; requires offline phase; quadratic communication in circuit depth.

**v0 Choice: OT-Extension (iknp / Keller–Orsini–Scholl variant).**

**Rationale:**
- Concrete overhead for a single AND gate is well-characterized (10–50 ms on Mac, 50–200 ms on phone).
- Standard assumption (semantic security of OT) aligns with Witness-protocol cryptographic assumptions.
- Intermediate round complexity (≤ 3 rounds) balances latency vs. bandwidth.
- Software libraries (libOTe, EMP toolkit) are mature and open-source.
- Easier to add malicious-security upgrades (Everest 69) than garbled circuits.

**Fallback**: Garbled circuits permitted if OT bandwidth exceeds 10 MiB per predicate in production (Everest 92 performance review).

---

## 3. Protocol Phases

### 3.1 Phase I: Key Derivation and Setup

**Inputs:**
- Principal A's agent has Ed25519 agent-key pair `(sk_A, pk_A)` (bound to principal's Witness credentials).
- Principal B's agent has Ed25519 agent-key pair `(sk_B, pk_B)`.
- Session ID `sid` (unique per Mirror exchange, derived from both principals' nonces).
- Predicate identifier `p` (e.g., "unselfishness_evidence").

**Computation (both agents independently):**
```
# Shared randomness seed (KDF)
seed_A = HMAC-SHA3-256(sk_A, "calm-mirror/mpc-seed/v1" || sid || p)
seed_B = HMAC-SHA3-256(sk_B, "calm-mirror/mpc-seed/v1" || sid || p)

# Expand into random bytes for OT-extension masking
RNG_A = ChaCha20(key=seed_A, nonce=0)
RNG_B = ChaCha20(key=seed_B, nonce=0)
```

**OT-Extension Initialization (per principal):**
- Agent A samples 128-bit random OT-base seed `s_A` via `RNG_A`.
- Agent B samples 128-bit random OT-base seed `s_B` via `RNG_B`.
- Both agents run a base-OT protocol (e.g., DH-based, 128 instances) to establish initial OT correlations.

**Purpose**: Establish authenticated, independent randomness for the two parties. No shared secrets exchanged at this stage.

### 3.2 Phase II: Input Commitment (Local)

Before engaging in the MPC gate, each principal commits to their input bit locally (Everest 42 §4.1).

**Agent A:**
```
b_A ∈ {0, 1, unknown}  # Evaluated boolean on predicate p
salt_A = CSPRNG(32 bytes)
salt_commitment_A = SHA3-256(b_A || salt_A)
# Store locally: (sid, p, salt_commitment_A, salt_A) in mlocked vault
```

**Agent B (identically):**
```
b_B ∈ {0, 1, unknown}  # Evaluated boolean on predicate p
salt_B = CSPRNG(32 bytes)
salt_commitment_B = SHA3-256(b_B || salt_B)
# Store locally: (sid, p, salt_commitment_B, salt_B) in mlocked vault
```

**Purpose**: Create a local audit trail so that, if adversary later claims "Agent A said `b_A = 0`", Agent A can prove the truth via salt revocation.

### 3.3 Phase III: OT-Extension AND-Gate Computation

**High-level protocol (iknp / Keller–Orsinski–Scholl):**

1. **Agent A's role (OT receiver):**
   - Holds the AND gate's first input bit `b_A`.
   - Does NOT learn `b_B` during execution.

2. **Agent B's role (OT sender):**
   - Holds the AND gate's second input bit `b_B`.
   - Does NOT learn `b_A` during execution.

3. **OT-Extension Rounds:**
   ```
   Round 1: Agent A → Agent B
     Send: OT-receiver message (PRF-based, encodes choice bit b_A)
     Size: ~128 bytes
     
   Round 2: Agent B → Agent A
     Send: OT-sender message (encryptions of AND truth-table entries)
     Size: ~256 bytes
     
   Round 3: Agent A decrypts
     Recover: AND(b_A, b_B) without seeing b_B
   ```

4. **Tri-state Extension (Unknown-bit Handling):**
   - If `b_A = unknown`, Agent A sends a special OT-receiver message indicating "unknown".
   - Agent B's OT-sender response includes a flag `has_alignment = false` (prevents false alignment).
   - Result: `AND_tri(unknown, b_B) = unknown` (Everest 42 §6.1).
   - Identically for `b_B = unknown`.

5. **Output of Phase III:**
   ```
   Agent A computes: a ∈ {0, 1, unknown}
   Agent B computes: a ∈ {0, 1, unknown}  (same value)
   ```

**Security Claim**: Under semantic security of OT, neither party learns the other's input bit. Agent A learns only the AND-gate output and their own input; Agent B learns only the output and their own input.

### 3.4 Phase IV: Commitment Generation and Exchange

Once both agents have computed `a`, they independently commit (Everest 42):

**Agent A:**
```
r_A = CSPRNG(32 bytes)  # Sample randomness for Pedersen commitment
Com_A = g^a × h^r_A    # Ristretto255 commitment
# Store r_A locally (mlocked, indexed by sid, p)
# Sign session record with agent Ed25519 key
agent_sig_A = Ed25519.sign(sk_A, serialize(Com_A || sid || p))
```

**Agent B (identically):**
```
r_B = CSPRNG(32 bytes)
Com_B = g^a × h^r_B
# Store r_B locally
agent_sig_B = Ed25519.sign(sk_B, serialize(Com_B || sid || p))
```

**Exchange Protocol:**
1. Agent A → Agent B: `(Com_A, agent_sig_A)`
2. Agent B → Agent A: `(Com_B, agent_sig_B)`
3. Both agents verify the other's signature and store the session record (Everest 42 §4.2).

**Purpose**: Bind both principals to the alignment bit via cryptographic commitment + signature. Neither can later claim they meant a different bit.

---

## 4. Tri-State AND Semantics

### 4.1 Boolean Truth Table with Unknown

The tri-state AND extends classical binary AND:

| b_A | b_B | AND_tri(b_A, b_B) | Reason |
|-----|-----|---|---|
| 1 | 1 | 1 | Both true → alignment |
| 1 | 0 | 0 | A true, B false → no alignment |
| 0 | 1 | 0 | A false, B true → no alignment |
| 0 | 0 | 0 | Both false → no alignment |
| unknown | 1 | unknown | A withheld; result indeterminate |
| unknown | 0 | 0 | A withheld, B false → definitely no alignment |
| 1 | unknown | unknown | B withheld; result indeterminate |
| 0 | unknown | 0 | A false, B withheld → definitely no alignment |
| unknown | unknown | unknown | Both withheld → indeterminate |

**Key rule:** If either party withholds *and* the gate outcome depends on that unknown bit, the result is `unknown` (not collapsed to false).

### 4.2 Implementation in OT-Extension

**Agent B's Sender Role:**

For each possible OT-receiver choice (including the unknown flag), Agent B pre-computes the AND truth-table entry:

```python
def and_gate_entry(choice_bit, my_bit):
  if choice_bit == "unknown":
    if my_bit == 0:
      return 0  # unknown AND false = false (deterministic)
    else:
      return "unknown"  # unknown AND true = unknown
  elif my_bit == "unknown":
    if choice_bit == 0:
      return 0  # false AND unknown = false
    else:
      return "unknown"  # true AND unknown = unknown
  else:
    return choice_bit & my_bit  # both known → classical AND

# Encrypt both truth-table entry and status flag
for i in [0, 1, "unknown"]:
  result = and_gate_entry(i, b_B)
  ciphertext_i = Encrypt(ot_key_i, result)
  ciphertext_i.has_alignment = (result == 1)
  send(ciphertext_i)
```

**Agent A's Receiver Role:**

Agent A uses their OT-receiver secret to decrypt exactly one ciphertext (the one corresponding to `b_A`). Decryption reveals `a` and the `has_alignment` flag.

---

## 5. Zero-Knowledge Proof of Honest MPC Computation

This section sketches the proof that the MPC gate was evaluated correctly (Everest 59 relies on this framework).

### 5.1 Proof Goal

**Statement**: "The aligned-bit commitment `Com_A` (and `Com_B`) opens to the correct AND-output of the two input bits, without revealing either input bit."

### 5.2 Proof Construction (Sigma Protocol)

**Commit Phase (by Agent A):**
```
Sample random r_aux ∈ Z_q
Compute T_1 = g^(b_A * b_B) × h^r_aux  # Commitment to AND(b_A, b_B)
Send T_1 to Agent B
```

**Challenge Phase (by Agent B):**
```
Sample random c ∈ Z_q (via HMAC-based Fiat-Shamir)
Send c to Agent A
```

**Response Phase (by Agent A):**
```
Compute response z = b_A * b_B + c * (some function of a and r_A)
Send z to Agent B
```

**Verification Phase (by Agent B):**
```
Check that g^z × h^(-c * r_A) == T_1 × (Com_A)^(-c)
If valid, conclude that Com_A opens to the honest AND-output.
```

**Round complexity**: 3 rounds (commit, challenge, response). Can be made non-interactive via Fiat-Shamir hashing.

### 5.3 Security Property

Under the Discrete Log assumption, an honest Agent A cannot produce a false proof of MPC correctness. Agent B can verify that Agent A evaluated the AND gate faithfully.

**Soundness**: If the proof verifies, the probability that Agent A deviated from the protocol is ≤ 2^{-128} (via repeated challenges).

---

## 6. Composition with Aligned-Bit Commitment (Everest 42)

### 6.1 Input-Output Flow

**Input to Everest 58 (MPC):**
- Each principal's evaluated bit `b_A, b_B ∈ {0, 1, unknown}` (from Everest 26–40 predicate evaluation).
- Per-counterparty consent (Everest 46) for each predicate.

**Output from Everest 58:**
- Aligned-bit `a = AND_tri(b_A, b_B)` (computed jointly, verified via Everest 59 proof).

**Input to Everest 42 (Commitment):**
- Aligned-bit `a`.

**Output from Everest 42:**
- Pedersen commitments `Com_A`, `Com_B` (both to the same `a`).
- Session record with agent signatures.

### 6.2 Strict Ordering

Everest 58 must complete before Everest 42. The MPC must produce a definitive `a` (or abort) before commitment generation.

```
MPC Phase III (compute a) → Everest 59 proof generation → 
Everest 42 commitment → Everest 43 aggregation proof → disclosure
```

---

## 7. Composition with Everest 43 (ZK Proof: K-of-N Values)

### 7.1 Input Aggregation

Everest 58 is executed once per shared predicate in the principals' intersection vocabulary. For K shared predicates:

```
p_1: a_1 = AND_tri(b_A_1, b_B_1)
p_2: a_2 = AND_tri(b_A_2, b_B_2)
...
p_K: a_K = AND_tri(b_A_K, b_B_K)
```

### 7.2 Aggregation for Everest 43

Everest 43 constructs a ZK proof that "at least M of the K bits are `a_i = 1`" without revealing which M.

**Input to E43:**
```
[Com_A_1, ..., Com_A_K]  (Principal A's commitments to a_1, ..., a_K)
[Com_B_1, ..., Com_B_K]  (Principal B's commitments)
threshold K, target M
```

**E43 Output:**
```
π_count = ZK proof that ∑_i [a_i == 1] ≥ M
          without revealing the indices or the exact count
```

**Handling of unknown bits**: Everest 43 correctly excludes `unknown` bits from the count, so strategic withholding does not artificially inflate the score.

---

## 8. Withhold Handling (Everest 51)

### 8.1 Withholding Protocol

Any principal may unilaterally withhold their evaluation of a specific predicate (Principal-protective default #1).

**Mechanism:**
```
If Principal A withholds predicate p:
  Agent A sends: (b_A = unknown) to Agent B's MPC
  Agent B's MPC receiver sees "unknown" flag
  AND_tri(unknown, b_B) evaluates to:
    - 0 if b_B = 0 (false AND anything = false)
    - unknown if b_B = 1 (unknown AND true = unknown)
  Result: No alignment bit is committed; session record marks (p: "unknown", reason: "principal_withheld")
```

**Downstream effect:** The withheld predicate does not contribute to Everest 43 count. Both principals see `commitment_status: "unknown"` for that predicate; neither can infer the other's bit.

### 8.2 Withhold-Opacity

Principal B cannot determine whether Principal A withheld `true`, `false`, or genuinely did not evaluate the predicate.

**Why**: The MPC AND-gate output is indistinguishable from `unknown` in all three cases. Everest 51 guarantees this opacity.

---

## 9. Round Complexity and Communication

### 9.1 OT-Extension Rounds (Phase III)

Standard iknp / Keller–Orsinski–Scholl OT-extension:

| Round | Sender | Message | Size |
|-------|--------|---------|------|
| Setup | Both | Base-OT (Diffie–Hellman) | ~512 bytes total |
| 1 | Agent A | OT-receiver choice bits | ~128 bytes |
| 2 | Agent B | OT-sender encrypted values | ~256 bytes |
| **Total** | — | — | **~900 bytes per predicate** |

**Latency**: 3 round trips (setup + 2 extension rounds). Typical: 50–100 ms latency on WiFi.

### 9.2 Communication for Multiple Predicates

For K shared predicates, the protocol must be run K times (or parallelized).

**Sequential (safer):** K × 900 bytes = 7.2 KiB for K=8.
**Parallelized (Everest 57 refinement):** Can batch base-OT, reducing overhead.

---

## 10. UC-Security Analysis

### 10.1 Formal Security Definition

**Claim**: Everest 58 is universally composable (UC-secure) under the Decisional Diffie-Hellman (DDH) assumption and the semantic security of OT.

**Adversarial Model:**
1. Static corruption (one party is malicious, the other honest).
2. Eavesdroppers cannot access local vaults or cryptographic keys.

**Ideal Functionality (Canetti's UC framework):**
```
F_AND_MPC:
  Input: (b_A from Agent A, b_B from Agent B)
  Output: a = AND_tri(b_A, b_B) to both agents
  Secrecy: Neither agent learns the other's input bit
```

### 10.2 Concrete Protocol

The 3-round OT-extension protocol realizes `F_AND_MPC` under:
- Semantic security of OT (Naor–Pinkas, Chou–Orlandi, or later).
- DDH assumption on the group used for base-OT.

**Proof Sketch**: An adversary controlling Agent A can simulate the OT-sender's messages using the semantic security of OT; Agent A learns only the AND output. By symmetry, an adversary controlling Agent B learns only the output.

### 10.3 Malicious Adversary (Round Complexity Upgrade)

**Current (v0)**: Honest-but-curious agents (no malicious deviation).

**v1 (Everest 69)**: Malicious security adds 1 additional round (4 rounds total) for zero-knowledge proofs of protocol adherence. Bandwidth ~1.5 KiB per predicate.

---

## 11. Soundness Under Malicious Adversary

### 11.1 Attack Scenario

**Threat**: Malicious Principal A attempts to learn Principal B's bit `b_B` by deviating from the MPC protocol.

### 11.2 Defense Mechanism

**Everest 59 (ZK Proof of MPC Correctness)** provides the defense:
1. After the MPC outputs `a`, Agent A must prove that the AND gate was evaluated correctly.
2. The proof reveals no information about the inputs; only that the output is honest.
3. If Agent A cannot produce a valid proof, the session aborts (Everest 52).

**Combined defense (E58 + E59):**
- E58 ensures Agent A cannot learn `b_B` during MPC execution (by OT semantic security).
- E59 ensures Agent A cannot post-hoc claim a false output (by ZK soundness).

---

## 12. Performance Targets and Budgets

### 12.1 Per-Predicate Costs

| Operation | M-series Mac | Phone | Notes |
|-----------|---------|-------|-------|
| OT base setup | 5 ms | 20 ms | One-time per session |
| OT extension (1 AND) | 10–50 ms | 50–200 ms | Dominates cost |
| Salt commitment (local) | <0.1 ms | <0.5 ms | Deterministic |
| Pedersen commitment | <2 ms | <5 ms | Group scalar mult |
| ZK proof of correctness (E59) | 5–10 ms | 20–50 ms | Sigma-protocol |
| **Total per predicate** | **<80 ms** | **<300 ms** | Includes all phases |

### 12.2 Multi-Predicate Performance

For K=8 shared predicates (typical v0 vocabulary):
- **Sequential**: ~640 ms on Mac, ~2.4 s on phone.
- **Parallelized** (Everest 57 refinement): ~150–200 ms on Mac, ~600–800 ms on phone.

**Budget (Everest 92)**: Full Mirror exchange ≤ 500 ms p95 on Mac, ≤ 2 s on phone.

**Status**: v0 sequential is within budget for K ≤ 6. Everest 57 will confirm parallelization if needed.

---

## 13. Test Plan and Acceptance Tests (T-M58.1 through T-M58.6)

### T-M58.1 — Honest-Bilateral Execution

**Setup**: Two honest agents, both following protocol exactly.

**Test**:
1. Agent A: `b_A = 1`, Agent B: `b_B = 1` → expected `a = 1`.
2. Agent A: `b_A = 1`, Agent B: `b_B = 0` → expected `a = 0`.
3. Agent A: `b_A = 0`, Agent B: `b_B = 1` → expected `a = 0`.
4. Agent A: `b_A = 0`, Agent B: `b_B = 0` → expected `a = 0`.

**Verification:**
- Both agents compute the same `a`.
- Commitments `Com_A` and `Com_B` are created and stored.
- Session record is consistent.

**Pass criterion**: All 4 cases produce correct output and matching commitments.

### T-M58.2 — Malicious-Prover Detection (Everest 59)

**Setup**: Agent A (malicious) attempts to fool the protocol.

**Test Scenario A**:
1. Agent A deviates from the OT-extension protocol (e.g., sends wrong OT-receiver message).
2. Agent A's output `a'` is different from the honest AND-output.
3. Agent A attempts to produce a Everest-59 ZK proof of honest computation.

**Expected Failure**: The ZK proof fails verification (Soundness property).

**Verification**: Session aborts; both agents receive `abort_reason: "proof_verification_failed"`.

**Pass criterion**: Malicious proof is rejected; session aborts cleanly (Everest 52).

### T-M58.3 — Withhold-Opacity

**Setup**: Agent A withholds `b_A` for predicate `p` (sets `b_A = unknown`).

**Test**:
1. Run MPC with `b_A = unknown`, `b_B = 1`.
2. Verify that `AND_tri(unknown, 1) = unknown` in the session record.
3. Run MPC with `b_A = unknown`, `b_B = 0`.
4. Verify that `AND_tri(unknown, 0) = 0` (deterministic).

**Verification**: Agent B observes only the status (`unknown` or `0`), not the reason (withheld vs. not evaluated).

**Pass criterion**: Withhold semantics are correctly implemented; no information leakage about the withheld bit.

### T-M58.4 — Unknown-Propagation

**Setup**: Multiple predicates with mixed `unknown` and known bits.

**Test**:
```
p_1: a_1 = AND(1, 1) = 1
p_2: a_2 = AND(unknown, 1) = unknown
p_3: a_3 = AND(0, 1) = 0
p_4: a_4 = AND(unknown, unknown) = unknown
```

**Verification**: Everest 43 proof correctly counts alignment (≥ 1 for this set) while handling unknowns.

**Pass criterion**: Unknown bits do not contribute to the count; no false positives.

### T-M58.5 — Performance Budget

**Setup**: K=8 shared predicates.

**Test** (M-series Mac):
1. Run complete Everest 58 (MPC) + Everest 59 (ZK proof) for all 8 predicates.
2. Measure wall-clock time.
3. Repeat 10 times; report p95 latency.

**Expected**: p95 ≤ 500 ms (single-threaded) or ≤ 200 ms (parallelized).

**Pass criterion**: p95 latency within budget; no outliers > 1 second.

### T-M58.6 — Cross-Implementation Parity

**Setup**: Reference Python implementation (Everest 86) and Rust implementation (Everest 87).

**Test**: Run identical test vectors through both implementations.
- Identical input (same `b_A, b_B` for each predicate, same RNG seeds).
- Verify output commitment `Com_A` and `Com_B` are identical.
- Verify ZK proof output is identical.

**Pass criterion**: Bit-for-bit parity; test vectors published in Everest 70.

---

## 14. Composition with Everest 42, 43, 49, 51

### 14.1 Sequential Composition

```
Everest 41: Compute shared_predicates = Vocab_A ∩ Vocab_B
  ↓
Everest 58: For each p ∈ shared_predicates, compute a_p via MPC
  ↓
Everest 59: Generate ZK proof that each a_p is correct
  ↓
Everest 42: Commit to each a_p via Pedersen commitment
  ↓
Everest 43: Aggregate: prove ≥ M of K commitments open to 1
  ↓
Everest 49: Reciprocal disclosure; both agents exchange commitments + proofs
```

### 14.2 Data Flow Through Stages

**Input (E58)**: `(b_A_1, ..., b_A_K)` and `(b_B_1, ..., b_B_K)` from predicate evaluators.

**Output (E58)**: `a_1, ..., a_K` (joint bits, each verified by E59 proof).

**Consumed by (E42)**: `a_1, ..., a_K` are each committed via Pedersen.

**Consumed by (E43)**: Commitments `[Com_A_1, ..., Com_A_K]` and `[Com_B_1, ..., Com_B_K]`.

### 14.3 Fallback on Abort

**Everest 52 (Mirror-fail abort semantics)**: If Everest 58 aborts (MPC failure or proof failure), the session returns `unknown` for all affected predicates. Everest 42 is not invoked; no commitments are created.

---

## 15. V1 Questions and Open Items

1. **Parallelization via Batch OT**: Can the base-OT setup be shared across multiple AND gates? Likely yes; Everest 57 will specify.

2. **Garbled-Circuit Fallback**: If OT-extension bandwidth exceeds 10 MiB, should fallback be automatic or explicit? User choice preferred for v0; standardize by v1.

3. **Multi-party Threshold Variant**: Can ≥3 principals jointly compute AND in MPC? Yes, but complexity scales; out of scope for v0 (all Mirror exchanges are 2-party).

4. **Malicious Security**: Everest 69 adds malicious-secure proofs (1 extra round). Concrete bandwidth trade-off pending.

5. **Post-Quantum Migration**: Lattice-based MPC (e.g., Ring-LWE OT) has no standard library maturity yet. Everest 64 defers to 2027+.

---

## 16. Signoff and Dependencies

**Direct prereqs:** Everest 56 (Pedersen vector commitments), Everest 57 (framework selection).

**Dependent summits:**
- Everest 59 (ZK proof of MPC correctness).
- Everest 42 (aligned-bit commitment).
- Everest 43 (K-of-N aggregation).
- Everest 49 (reciprocal disclosure).
- Everest 61 (cross-principal binding).
- Everest 69 (adversarial robustness study).

**Cross-protocol composition:**
- Everest 26–40 (predicate evaluation that feeds `b_A, b_B`).
- Everest 46 (per-counterparty consent).
- Everest 51 (withhold-any-bit guarantee).
- Everest 52 (fail-abort semantics).

**Acceptance gate script:** `~/CredexAI/scripts/everest_58_mirror_mpc_intersection_gate.py`
- Unit tests for OT-extension (honest and malicious).
- Integration with salt commitment (E42 audit trail).
- Integration with ZK proof verification (E59).
- Tri-state AND truth table validation.
- Withhold opacity property test.
- Performance micro-benchmarks (per-predicate cost).
- Conformance vectors (Sect 13).

---

— Calm, 2026-05-20
