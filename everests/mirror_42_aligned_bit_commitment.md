# Mirror Everest 42 — Aligned-Bit Commitment Scheme

*Phase XII — Mirror Disclosure Semantics. Prereq: Everest 41, [Witness Everest 44].*

---

## 1. The Primitive: Pedersen Commitment to Joint Alignment Bit

The alignment computation (Everest 41) determines whether two principals both hold `true` on a shared value predicate `p`. This bit—the joint alignment—is sensitive. If either principal's individual bit leaks to an eavesdropper, the entire value-alignment protocol collapses.

Everest 42 solves this using a Pedersen commitment scheme adapted from Calm Witness Everest 44, anchored to Ristretto255 to ensure composability with Witness-E44 and future Bulletproofs (Everest 45/49/51/58).

**Definition**: An aligned-bit commitment is the group element:

```
Com(a; r) = g^a × h^r
```

where:
- `g` is the Ristretto255 basepoint (shared with Calm Witness).
- `h` is the hash-to-curve generator `Ristretto_map_to_group(SHA3-256("calm-mirror/h/v1"))`.
- `a ∈ {0, 1}` is the alignment bit (0 = mismatch, 1 = both true, unknown = withheld).
- `r ∈ Z_q` is uniformly random blinding scalar.
- `×` denotes group multiplication.

The commitment `Com(a; r)` is a 32-byte compressed Ristretto point. No principal reveals their own input bit individually; both the alignment bit and blinding emerge from the joint two-party computation.

Critical properties:
- **Hiding**: Knowing only `Com(a; r)` reveals nothing about `a ∈ {0, 1}` (Discrete Log assumption).
- **Binding**: Once committed, neither principal can later claim the commitment opens to a different alignment value.

---

## 2. Ristretto255 Group: Inheritance from Witness

This everest reuses the group-choice decision from Calm Witness Everest 44. The same generators `g` and `h` are used across Witness and Mirror to enable composition at disclosure time (Everest 49, Everest 55).

**Why the same group:**
1. **Composability**: A session that runs Calm Pact (directive equality), then Calm Witness (user-state), then Calm Mirror (values alignment) uses a single elliptic-curve group. Shared generators reduce key material and cryptographic surface.
2. **Interoperability**: Witness Everest 44 locks `h` via `SHA3-256("calm-witness/h/v1")`. Mirror inherits this. Version numbering allows future divergence if needed.
3. **Bulletproofs composition**: Everest 45 (range proofs, unselfishness-index bounds) composes seamlessly with Witness Everest 45 (distance threshold proofs) because both use Ristretto255 commitments under the same group.
4. **Security**: Ristretto255 provides ~126 bits of classical security, sufficient for 128-bit security target across all primitives.

**Generator h construction (cross-reference from Witness E44 §2.2):**
```
h_raw = SHA3-256("calm-witness/h/v1")
h = Ristretto_map_to_group(h_raw)  # RFC 9496 / RFC 7748 uniform hash-to-point
```

This is fixed and public; the same `h` is used in all Mirror sessions.

---

## 3. Two-Party MPC: AND-of-Bits Without Input Leak

Unlike Witness Everest 44 (a unilateral commitment to one principal's distance), Mirror Everest 42 commits to a *joint* boolean function: the AND of two principals' bits.

### 3.1 The Protocol Phase (Input Preparation)

Each principal, via their agent, holds:
- `p`: a shared value-predicate identifier (e.g., "unselfishness_evidence").
- `b_A ∈ {0, 1, unknown}`: Principal A's evaluated boolean on predicate `p` (unknown = withheld or not yet disclosed).
- `b_B ∈ {0, 1, unknown}`: Principal B's evaluated boolean on predicate `p`.

**Per-counterparty consent (Everest 46):** Each principal consents separately to whether their `b_X` is evaluable and disclosable to the other side.

### 3.2 The AND Function (Tri-State Extension)

The joint alignment `a` is defined as:

```
a = AND_tri(b_A, b_B) where:
  AND_tri(1, 1)       = 1       (both true → alignment)
  AND_tri(0, x)       = 0       (A false → no alignment)
  AND_tri(x, 0)       = 0       (B false → no alignment)
  AND_tri(unknown, x) = unknown (A withheld → unknown)
  AND_tri(x, unknown) = unknown (B withheld → unknown)
  AND_tri(1, unknown) = unknown (A true, B unknown → unknown)
  AND_tri(unknown, 1) = unknown (A unknown, B true → unknown)
```

The tri-state extension prevents collapse of withheld bits to false. If either principal withholds or returns `unknown`, the result is `unknown`—not a "mismatch" leaking that one side said true.

### 3.3 Two-Party MPC Construction (OT-Extension Sketch)

The actual computation of `a` happens via secure two-party computation:

1. **OT-based approach** (recommended for v0):
   - Principal A commits to `b_A` (via local Salt encoding, see Sect 5).
   - Principal B commits to `b_B` (via local Salt encoding).
   - Both agents run an oblivious-transfer (OT) extension protocol (e.g., Keller–Orsini–Scholl or iknp) with one side computing the AND gate, the other side blind.
   - The gate output is the aligned-bit `a`.
   - Neither side sees the other's raw bit; only the gate output.

2. **Garbled-circuit alternative** (fallback):
   - Fewer rounds (one round vs. two for OT).
   - Higher concrete overhead (garbling cost scales with circuit depth).
   - For a single AND gate, OT is preferred.

**Selection rule for v0:** OT-extension is the default. Everest 57 (framework selection) confirms this choice at the Mirror-level decision point.

### 3.4 Commitment to AND-Output

Once the MPC outputs `a ∈ {0, 1, unknown}`, both agents:

1. **Sample randomness** `r ∈ Z_q` uniformly (each agent samples independently; see Sect 6).
2. **Commit to a** via `Com_A = g^a × h^r_A` (Principal A's commitment).
3. **Commit to a** via `Com_B = g^a × h^r_B` (Principal B's commitment).
4. **Store commitments** in the session record (see Sect 4.2).

Both commitments commit to the *same* bit `a` (the joint output), but with independent randomness. This ensures:
- Neither principal can unilaterally change the claimed alignment.
- Both parties have cryptographic evidence that they agreed on `a`.
- Cross-principal binding (Everest 61) is enabled.

---

## 4. Session Storage and Ledger Format

### 4.1 Pre-MPC: Salt Commitment (Local Phase)

Before the MPC runs, each principal's agent stores a *commitment to their own input bit* locally (not shared).

**Salt commitment (per principal):**
```json
{
  "kind": "mirror.salt_commitment.v0",
  "timestamp": "2026-05-20T14:45:00Z",
  "principal_id": "p_alice_xxxx",
  "session_id": "s_mirror_001",
  "predicate_id": "unselfishness_evidence",
  "salt_commitment": "<base64-encoded 32-byte salt-hash>",
  "salt_commitment_version": "1"
}
```

**Computation** (happens locally before any network communication):
```
salt = CSPRNG(32 bytes)
salt_commitment = SHA3-256(b_A || salt)
  where || is concatenation and b_A ∈ {0x00, 0x01}
```

Storage location: principal's mlocked vault (similar to Witness E44 §5). The salt is never transmitted; only the salt_commitment is stored locally.

**Purpose**: If an adversary later claims Principal A said `b_A = 0` when A actually said `b_A = 1`, Principal A can prove this by revealing the salt and the original input bit. The verifier checks: does `SHA3-256(claimed_b_A || salt) == stored_salt_commitment`?

This is a local audit-trail mechanism, not transmitted during the Mirror exchange.

---

### 4.2 Post-MPC: Aligned-Bit Commitment (Shared Session Record)

After MPC completes and both agents commit to `a`, the session record is created:

```json
{
  "kind": "mirror.alignment_committed.v0",
  "timestamp": "2026-05-20T14:45:10Z",
  "session_id": "s_mirror_001",
  "predicate_id": "unselfishness_evidence",
  "shared_vocabulary_size": 12,
  "principals": [
    {
      "principal_id": "p_alice_xxxx",
      "commitment": "<base64-encoded 32-byte RistrettoPoint Com_A>",
      "agent_signature": "<Ed25519 signature by p_alice's agent>"
    },
    {
      "principal_id": "p_bob_xxxx",
      "commitment": "<base64-encoded 32-byte RistrettoPoint Com_B>",
      "agent_signature": "<Ed25519 signature by p_bob's agent>"
    }
  ],
  "mpc_framework": "ot_extension_v1",
  "commitment_version": "1"
}
```

**Fields:**
- `principals[0,1].commitment`: The two independent commitments `Com_A` and `Com_B`. Both commit to the same bit `a`.
- `principals[0,1].agent_signature`: Each agent signs the commitment with their agent key (a sub-key derived from the principal's Calm Witness credentials).
- `mpc_framework`: Identifies the MPC protocol used ("ot_extension_v1", "garbled_circuit_v1", etc.). Allows future variants.
- `shared_vocabulary_size`: The number of predicates in the principals' intersection vocabulary (for accounting).

**Ledger anchor**: The entire record is appended to the principal's immutable behavior-evidence chain (Everest 11) and anchored to a Sigsum transparency log (similar to Witness E44, but a separate Mirror transparency log).

---

## 5. Randomness Separation: Independent Blinding per Principal

A key design choice: the randomness `r_A` (used in Com_A) and `r_B` (used in Com_B) are sampled independently by each principal's agent.

**Why:**
1. **No collusion through shared randomness**: If `r_A == r_B`, an adversary colluding with both principals could compute `Com_A / Com_B = (g^a × h^r_A) / (g^a × h^r_B) = h^(r_A - r_B) = h^0 = identity`. This would leak that both commitments are to the same value. Independent randomness prevents this.
2. **Post-disclosure deniability (limited)**: Principal A cannot later claim "B chose our randomness, so B's commitment could be fake." Both randomnesses are sampled independently before the exchange.
3. **Fault tolerance**: If one principal's RNG fails, the other's randomness is unaffected. Binding still holds per commitment.

**Storage and lifecycle:**
- `r_A` is stored in Principal A's mlocked vault, indexed by `session_id`.
- `r_B` is stored in Principal B's mlocked vault, indexed by `session_id`.
- Both are ephemeral: discarded 24–48 hours post-session (or upon explicit revocation, per Everest 52).
- On session abort (Everest 52), randomnesses are zeroed before termination.

**Use in ZK proofs (Everest 43, 45):**
In subsequent proofs (e.g., "we both have ≥ K true bits," Everest 43), each principal uses their own randomness to construct their portion of the proof. The proofs are composed but do not reveal the individual randomnesses.

---

## 6. Tri-State Handling: Unknown Bits

The tri-state extension (Sect 3.2) is critical for principal-protective default #1 (any bit can be withheld).

### 6.1 Unknown Representation

When `a = unknown`, no meaningful commitment exists (we cannot commit to `unknown` as a scalar in Z_q).

**Handling:**
```json
{
  "kind": "mirror.alignment_committed.v0",
  "principals": [
    {
      "principal_id": "p_alice_xxxx",
      "commitment_status": "unknown",
      "commitment": null,
      "unknown_reason": "principal_withheld"
    },
    ...
  ]
}
```

**Reasons for unknown:**
- `"principal_withheld"`: Principal A or B declined to disclose their bit for this predicate.
- `"consensus_unknown"`: The MPC framework determined one side's input was marked `unknown` (e.g., insufficient evidence for the predicate evaluation).
- `"mpc_abort"`: The two-party computation failed before producing a definitive result (Everest 52).

### 6.2 Unknown-Bit Composition Rule

When composing multiple alignment bits (Everest 43: "≥ K of N"), the AND function becomes an OR-of-ANDs:

```
score = count of predicate_i where AND_tri(b_A_i, b_B_i) == 1
unknown_count = count of predicate_i where AND_tri(b_A_i, b_B_i) == unknown
```

The proof (Everest 43) then proves `score ≥ K` *without revealing which* K predicates were true or how many were unknown. This ensures:
- A principal cannot infer partial vector information by observing which bits returned `unknown`.
- The final alignment-score is robust to strategic withholding.

---

## 7. Soundness and Binding

### 7.1 Binding Guarantee

Once both principals' agents commit to the alignment bit `a` (Sect 4.2), neither can later credibly claim a different bit.

**Formal claim**: If Principal A's agent later reveals `(a', r_A')` claiming to open `Com_A` to bit `a' ≠ a`, a verifier can detect the fraud.

**Proof:**
```
Suppose Com_A = g^a × h^r_A and Principal A later claims Com_A = g^a' × h^r_A'.

If both are true:
  g^a × h^r_A = g^a' × h^r_A'
  g^(a - a') = h^(r_A' - r_A)
  log_g(h) = (r_A' - r_A) / (a - a')

Since a, a' ∈ {0, 1}, the denominator is non-zero.
But h was derived via hash-to-curve (SHA3-256), so no adversary knows log_g(h) without solving DLP.
Contradiction.
```

Thus, Principal A cannot produce two valid openings.

### 7.2 Correctness of MPC Output

The committed bit `a` is the correct AND-output of the two input bits.

**Mechanism**: Everest 59 (ZK proof of MPC correctness) provides a formal proof that the MPC gate evaluation was honest. This proof is constructed after the alignment commitment and is published alongside the disclosure (Sect 8).

---

## 8. Hiding Property and Secrecy of Individual Bits

### 8.1 Hiding of `a`

Knowledge of either `Com_A` or `Com_B` alone reveals nothing about the value of the alignment bit `a`.

**Sketch**: By the same argument as Witness E44 §6.1, an adversary with two candidate bits `a_1, a_2 ∈ {0, 1}` cannot distinguish which was committed under a uniformly random blinding `r`.

### 8.2 Secrecy of Individual Input Bits

Neither the MPC protocol nor the commitments leak information about Principal A's input bit `b_A` or Principal B's input bit `b_B` to the other principal.

**MPC protocol requirement**: The choice of OT-extension or garbled circuits must be semantically secure. Standard protocols (e.g., iknp / keller-orsini-scholl) provide this.

**Commitment-level secrecy**: The commitments `Com_A` and `Com_B` are both to the *same* bit `a` (the joint output). An eavesdropper cannot infer `b_A` from `Com_A` or `b_B` from `Com_B`, because both commitments encode the AND output, not the inputs.

**Corollary**: If Principal A withholds their bit (b_A = unknown), Principal B observes `alignment_status: unknown` in the session record, but learns nothing about whether A's input was true, false, or absent.

---

## 9. Composition with Everest 41, 43, 49, 55

### 9.1 Input from Everest 41 (Pairwise Alignment Computation)

Everest 41 computes the intersection vocabulary:
```
shared_predicates = {p_1, p_2, ..., p_K} ⊆ Vocabulary_A ∩ Vocabulary_B
```

For each `p_i ∈ shared_predicates`, Everest 42 commits to the AND-output bit.

Result: A set of `K` aligned-bit commitments (one per shared predicate).

### 9.2 Output to Everest 43 (ZK Proof: Shared K-of-N Values)

Everest 43 constructs a zero-knowledge proof that "of the K alignment commitments, ≥ M are opening to 1."

**Input to E43**:
```
[Com_A_1, Com_A_2, ..., Com_A_K]  (Principal A's commitments)
[Com_B_1, Com_B_2, ..., Com_B_K]  (Principal B's commitments)
threshold K, target M             (publicly known)
```

**E43 output:**
```
π_count = ZK proof that ∑_i [Com_A_i opens to 1] ≥ M
          without revealing which i or the value M
```

Both principals can verify this proof independently (Everest 55, triadic composition with Pact + Witness).

### 9.3 Composition with Everest 45 (Range Proofs for Evidence Indices)

Everest 45 uses Pedersen commitments (same group, same generators) to prove unselfishness-score bounds. The Ristretto255 group-choice ensures that commitments from Everest 42 and Everest 45 compose seamlessly in multi-predicate proofs.

### 9.4 Integration with Everest 49 (Reciprocal Disclosure)

Everest 49 orchestrates the full Mirror exchange:
1. Both principals' agents run Everest 42 commitments.
2. Both agents construct Everest 43 proofs.
3. Both agents exchange commitments, proofs, and consent attestations.
4. Both verify each other's proofs.

The reciprocal exchange is atomic: if any proof fails verification, the session aborts (Everest 52).

### 9.5 Composition with Everest 55 (Calm Pact + Witness + Mirror)

Everest 55 specifies the strict ordering:
```
Stage 1: Calm Pact (directive equality) — agree on the exchange format
Stage 2: Calm Witness (user-state) — exchange biometric state + consent
Stage 3: Calm Mirror (values alignment) — exchange aligned-bit commitments + proofs
```

All three stages use Ristretto255 and the same generator set. A single session binds proof-state across all three primitives (cross-principal binding, Everest 61).

---

## 10. Soundness and Security Analysis

### 10.1 Adversarial Model

**Threat 1: Eavesdropper.**
- Observes network traffic (commitments, MPC transcripts, proofs).
- Cannot access principals' local vaults.
- **Defense**: Commitments hide the bits; MPC protocol hides individual inputs; proofs are ZK.

**Threat 2: Malicious Principal A.**
- Controls their own agent; can deviate from protocol.
- Cannot access Principal B's local vault.
- **Defense**: Binding guarantees that A cannot later claim a different opening. Consensus proof (E59) proves A's MPC gate was honest. Cross-principal binding (E61) proves A cannot retroactively deny consent.

**Threat 3: Malicious Principal A + B collude.**
- Together, can run an arbitrary protocol.
- **Defense**: Even with collusion, neither can prove the other's input bit. The alignment `a` is only meaningful to them; any third party (judge, audit) sees commitments and proofs without leaking individual bits. Per-counterparty consent (E46) limits blast radius.

**Threat 4: Principal A coerces Principal B.**
- Uses duress to force B to disclose or lie about values.
- **Defense**: Witness-E54 (stealth disclosure) surfaced coercion-flags to counterparties even without consent. Mirror extends this: if B's chain contains a `kind: safety_trigger.v0`, the Mirror exchange aborts or surfaces the trigger (Everest 54).

### 10.2 Cryptographic Hardness Assumptions

1. **Discrete Logarithm Problem (DLP)**: Finding `x` given `g^x` is hard in Ristretto255. This underpins binding and hiding.
2. **Decisional Diffie-Hellman (DDH)**: Cannot distinguish `g^(ab)` from a random group element. Implicit in randomness-blinded commitments.
3. **Semantic security of MPC**: The OT-extension or garbled-circuit protocol leaks no information beyond the function output. Standard assumption for iknp and similar.

---

## 11. Performance Targets and Budgets

Per-predicate commitment cost (single AND bit):

| Operation | Time (M-series Mac) | Time (Phone) | Notes |
|-----------|------------------|----------|-------|
| Sample `r_A`, `r_B` | <0.2 ms | <1 ms | Two independent RNG calls |
| MPC AND (OT-extension) | 10–50 ms | 50–200 ms | Depends on concrete implementation |
| Encode `a` as scalar | <0.01 ms | <0.01 ms | Trivial (0 or 1) |
| Commit `g^a × h^r_A`, `g^a × h^r_B` | <2 ms | <5 ms | Two scalar multiplications |
| **Total per predicate** | **<60 ms** | **<250 ms** | OT-extension dominates |

For K shared predicates:
- K commitments: `< K × 60 ms` on Mac, `< K × 250 ms` on phone.
- Typical K ≈ 4–8 (common values in v0 vocabulary).
- Per-exchange cost: **<500 ms on Mac, <2 s on phone** (within Everest 92 budget for full Mirror exchange).

---

## 12. Acceptance Tests (T-M42.1 through T-M42.5)

**T-M42.1 — Commitment Creation and Storage.**
- For a given input bit `a ∈ {0, 1}` and random `r`, compute `Com = g^a × h^r`.
- Verify that `Com` is a valid, compressed Ristretto point.
- Verify that the session record is correctly formatted and appended to the ledger.
- **Acceptance**: Ledger contains the commitment; no plaintext `a` or `r` in stored record.

**T-M42.2 — Binding Property.**
- Create a commitment `Com = g^a × h^r`.
- Attempt to create two valid openings: `(a, r)` and `(a', r')` with `a ≠ a'`.
- Verify that the second opening fails verification (i.e., `g^a' × h^r' ≠ Com`).
- **Acceptance**: Cannot produce two valid openings for different bits.

**T-M42.3 — Hiding Property.**
- Sample two random bits `a_0, a_1 ∈ {0, 1}` and randomnesses `r_0, r_1`.
- Compute both `Com_0 = g^a_0 × h^r_0` and `Com_1 = g^a_1 × h^r_1`.
- Run a distinguisher that attempts to guess which is which (given only the commitments, not the openings).
- Verify that the distinguisher succeeds with probability ≈ 0.5 (no better than random guess).
- **Acceptance**: Commitments are computationally indistinguishable.

**T-M42.4 — Tri-State Unknown Handling.**
- For a predicate where Principal A returns `unknown`, verify that:
  - No commitment is created (commitment_status = "unknown").
  - The session record contains the `unknown_reason` field.
  - Downstream proofs (E43) correctly skip this predicate.
- **Acceptance**: Unknown bits are handled gracefully without false true/false claims.

**T-M42.5 — Cross-Principal Binding (with Everest 61).**
- Create two commitments `Com_A` and `Com_B` to the same alignment bit `a`.
- Both agents sign the session record (agent_signature fields).
- Verify that:
  - Both principals' signatures are valid.
  - Neither signature can be forged without access to the agent's private key.
  - Removing or modifying either signature invalidates the entire session record.
- **Acceptance**: Both principals are cryptographically bound to the aligned-bit commitment.

---

## 13. V1 Questions and Evolution

1. **Post-quantum commitments**: Pedersen commitments have no known post-quantum lattice analogs with the same efficiency. Everest 64 and Everest 96 address migration to Ring-LWE or similar.

2. **Garbled-circuit performance**: If concrete OT-extension overhead becomes prohibitive on low-bandwidth networks, should garbled-circuit fallback be automatic or explicit user choice?

3. **Multi-predicate parallelization**: Can commitments to K predicates be batched into a single MPC call? Everest 57 will refine.

4. **Unknown-bit leakage via repetition**: If a principal withholds the same predicate in many sessions, does the pattern of `unknown` responses leak information? Everest 82 (anonymous warning channel) will detect and warn.

5. **Commitment recycling**: Can a commitment from one session be replayed in another? Everest 68 (anti-replay) prevents this via session binding.

---

## 14. Signoff and Dependencies

**Direct prereqs:** Everest 41 (pairwise intersection computation), [Witness Everest 44] (Pedersen commitment machinery).

**Dependent on this everest:**
- Everest 43 (ZK proof: shared K-of-N values).
- Everest 49 (reciprocal disclosure / Mirror exchange).
- Everest 59 (ZK proof of MPC correctness).
- Everest 61 (cross-principal binding proof).

**Cross-protocol composition:**
- Calm Witness E44 (same group, same generators).
- Calm Pact §4.1 (Ristretto255 lock).
- Calm Witness Everest 51 (withhold-any-bit guarantee adapted to Mirror context).

**Acceptance gate script:** `~/CredexAI/scripts/everest_42_mirror_aligned_commitment_gate.py`
- Unit tests for commitment creation, binding, hiding.
- Integration test with Everest 41 (reading shared vocabulary).
- Cross-implementation conformance vector (Sect 8 format).
- Fuzz testing of the tri-state AND function.

---

— Calm, 2026-05-20
