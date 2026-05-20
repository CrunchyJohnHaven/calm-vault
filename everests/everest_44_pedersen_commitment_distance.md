# Everest 44 — Pedersen Commitment to Distance Value

*Phase IV — Biometric Distance Machinery. Prereq: Everest 38.*

---

## 1. The Primitive: Hiding Distance Under Commitment

The combined distance `d_joint ∈ [0, 1]` computed in Everest 38 is the cryptographic materialization of whether the principal's current biometric sample (handwriting + voice) matches their enrolled template. This distance is sensitive. Disclosing it to a counterparty agent reveals the principal's biometric state vector with enough fidelity for an eavesdropper to infer enrollment weakness, detect fatigue or stress patterns, or extract behavioral signatures.

Pedersen commitments solve this by binding `d_joint` into a single elliptic-curve point that reveals nothing about the distance, while maintaining the property that once committed, the operator cannot later change the claimed distance without detection.

**Definition**: A Pedersen commitment to distance value `d` is the group element:

```
Com(d; r) = g^d × h^r
```

where:
- `g` is a standard generator of the group (the Ristretto255 basepoint).
- `h` is a second, independent generator (produced via hash-to-curve, see Section 2).
- `d ∈ [0, 1]` is the distance (scaled to a fixed-point integer as described in Section 3).
- `r` is a uniformly random element of Z_q, the scalar field.
- `×` denotes group multiplication.

The commitment `Com(d; r)` is a 32-byte compressed Ristretto point. Knowledge of `(d, r)` allows the operator to "open" the commitment by revealing both values; a counterparty can verify that the opening is correct by re-computing `g^d × h^r` and checking equality to the stored commitment.

The critical properties are:
- **Hiding**: Knowing only `Com(d; r)` reveals nothing about the numerical value of `d` (under the Discrete Logarithm Hypothesis).
- **Binding**: The operator cannot reveal two different distance values `d` and `d'` for the same commitment (under the Discrete Log assumption, this is computationally hard).

---

## 2. Group Choice and Generator Setup: Ristretto255 over Curve25519

Calm Pact (CALM_PACT_PROTOCOL_v0.md, v0.1 amendment) has locked the cryptographic group to **Ristretto255** — a prime-order subgroup construction derived from Curve25519. This choice is inherited by Everest 44 for consistency across the Calm Witness protocol suite.

### 2.1 Why Ristretto255

1. **Prime-order subgroup guarantee**: Curve25519 has cofactor 8 (small torsion subgroup). Ristretto255 quotients the full curve by the torsion, yielding a prime-order group of order `ℓ = 2^252 + 27742317777372353535851937790883648493` ≈ 2^252. This is essential for Pedersen commitments: if the group has composite order, hiding properties weaken.

2. **Established library support**: The Rust crate `curve25519-dalek` provides production-grade Ristretto255 arithmetic with constant-time implementation (side-channel resistant).

3. **Performance on commodity hardware**: Ristretto255 scalar multiplication runs in ~1–5 milliseconds on M-series ARM and <5 ms on phone processors (Snapdragon, A17 Pro). Acceptable for per-session commitment.

4. **Interoperability with Calm Pact**: Same curve choice allows key material and generator parameters to be shared across Calm Witness everests. The directory-level identity credentials in Everest 46 reuse the same group.

5. **Upgrade path**: Pedersen commitments generalize to post-quantum lattice-based groups (e.g., Kyber-derived rings) in v1+. Ristretto255 is a smooth starting point.

### 2.2 Generator Setup: g and h

**Generator g (the basepoint):**
- `g` is the standard Ristretto255 basepoint, publicly known.
- Used in Calm Pact as well; no new parameter.
- In `curve25519-dalek`, accessed via `RISTRETTO_BASEPOINT_POINT`.

**Generator h (hash-to-curve):**
- A second independent generator whose discrete-log relationship to `g` is unknown to all parties (including the protocol designers).
- Produced by hashing a fixed string through a cryptographic hash function, then mapping to Ristretto255.
- **Construction**: 
  ```
  h_raw = SHA3-256("calm-witness/h/v1")
  h = Ristretto_map_to_group(h_raw)
  ```
- The string `"calm-witness/h/v1"` is fixed, public, and immutable across all deployments.
- The mapping `Ristretto_map_to_group()` is the Ristretto255 uniform hash-to-point function (defined in RFC 9496, RFC 7748 specifications, and implemented in `curve25519-dalek` as `RistrettoPoint::from_uniform_bytes()`).
- The same `h` is used globally across all principals and all sessions; recomputing from the hash string yields identical results.

**Why "nothing-up-my-sleeve":**
- If the protocol designer chose `h` via random sampling or special selection, skeptics could hypothesize a hidden relationship `h = g^λ` for some secret `λ`.
- Deriving `h` from a hash of a publicly known string that contains the protocol name and version number makes this hypothesis unfalsifiable: any hidden relationship would require pre-computing a collision in SHA3-256, which is computationally infeasible.
- The version number `v1` allows future protocol versions to use different `h` if needed (Everest 96+).

---

## 3. Distance Encoding: Fixed-Point Representation

The distance `d ∈ [0, 1]` is a floating-point value (IEEE 754 double). Pedersen commitments operate over scalar fields (Z_q), not floating-point reals. A conversion is required.

**Fixed-point encoding:**
```
d_int = round(d × 2^32)
```

where `round()` is banker's rounding (round half to even) to minimize bias. This maps:
- `d = 0.0` → `d_int = 0`
- `d = 0.5` → `d_int = 2^31 = 2147483648`
- `d = 1.0` → `d_int = 2^32 = 4294967296`

The integer `d_int` is then interpreted as an element of Z_q (the scalar field of Ristretto255) by reducing modulo `q` if necessary. Since `d_int ≤ 2^32` and `q ≈ 2^252`, reduction is never needed in practice.

**Precision loss:**
- Floating-point `d` has ~53 bits of precision (IEEE 754 double).
- Fixed-point representation uses 32 bits.
- Maximum quantization error: `1 / 2^33 ≈ 1.16 × 10^-10`.
- Negligible for distance-threshold decisions (thresholds are typically chosen at ~0.01 or 0.05 precision).

**Reversibility (for debugging only):**
To recover `d` from `d_int` for logging or analysis:
```
d_recovered = d_int / 2^32
```

This is only used offline; the commitment itself stores no reversible mapping.

---

## 4. Commitment Construction and Storage

### 4.1 Per-Session Commitment Creation

When the principal's biometric samples are collected and fused (Everest 38), the operator computes the combined distance `d_joint ∈ [0, 1]`. The operator then:

1. **Encodes the distance** as `d_int = round(d_joint × 2^32)`.
2. **Samples randomness** `r ∈ Z_q` uniformly at random from a cryptographically secure RNG (e.g., `OsRng` from the `rand` crate).
3. **Computes the commitment** `Com = g^d_int × h^r` using constant-time scalar multiplication (via `curve25519-dalek`).
4. **Stores the randomness** `r` in the operator's volatile, mlocked memory (see Section 5).
5. **Compresses the commitment** to 32 bytes and stores it in the ledger (see Section 4.2).

The computation `g^d_int × h^r` is performed via a multi-scalar multiplication:
```rust
let commitment = (Scalar::from(d_int) * RISTRETTO_BASEPOINT) 
               + (Scalar::from(r) * H_GENERATOR);
```

This takes ~1–2 milliseconds on M-series hardware.

### 4.2 Ledger Entry Format

The commitment is stored in Calm Witness's append-only ledger as a new record of kind `biometric.distance_committed`:

```json
{
  "kind": "biometric.distance_committed",
  "timestamp": "2026-05-20T14:32:45Z",
  "principal_id": "p_john_bradley_xxxx",
  "session_id": "s_abc123",
  "sample_id_set": ["sw_0001", "sv_0002"],
  "d_committed_bytes": "<base64-encoded 32-byte compressed RistrettoPoint>",
  "template_id": "t_enroll_20260115",
  "commitment_version": "1"
}
```

**Fields:**
- `d_committed_bytes`: The 32-byte compressed representation of `Com(d_joint; r)`. Stored in base64 for JSON serializability.
- `template_id`: Reference to the enrolled biometric template used for distance computation. Binds the commitment to a specific enrollment ceremony (Everest 14).
- `session_id`: Unique identifier for the current session. Used to associate the commitment with the self-report and any other session data.
- `sample_id_set`: Array of identifiers for the handwriting and voice samples used (cross-reference to Everest 36 and 37 outputs).
- `commitment_version`: Version number of the commitment scheme. Currently `1` (Ristretto255). Used for future upgrades.

The entire record is appended to the immutable, cryptographically hashed ledger. A Sigsum transparency-log anchor is published (as per Everest 19), so any later tampering can be detected.

---

## 5. Randomness Management: mlocked Operator Vault

The randomness `r` used in the commitment **must never be disclosed to an untrusted party in plaintext**. However, `r` is essential for the zero-knowledge proofs in Everest 45 (proving `d < tau`) and other disclosure protocols.

**Storage:**
- The operator maintains a per-principal mlocked memory region (memory-locked by the `mlock()` syscall, preventing OS swap and unauthorized memory reads).
- Each session's `r` is stored in this vault, indexed by `session_id`.
- The vault is ephemeral: `r` is discarded 24–48 hours after the session ends (configurable per deployment policy).
- On graceful shutdown, the operator zeroes all `r` values via `volatile_zeroize()` before releasing memory.

**Disclosure in ZK proofs:**
- In Everest 45, the operator constructs a Σ-protocol proof that demonstrates `d_joint < tau` without revealing `d_joint` numerically.
- The proof uses `r` to construct challenge-response pairs (Schnorr-style).
- The proof is computed inside the operator's enclave and transmitted; `r` itself is never sent.

**Cryptographic binding:**
- An adversary who compromises the operator's process after the commitment is disclosed but before the session ends could extract `r`.
- With knowledge of both `Com` and `r`, the adversary could attempt to recover `d` by brute-force search (trying all `d ∈ [0, 2^32)` and checking if `g^d × h^r = Com`).
- This attack is computationally hard under standard assumptions; nonetheless, short-lived `r` storage and immediate zeroing reduce the window.
- For high-stakes principals, operator security policy may enforce withdrawal of `r` before disclosure of any proof (accepting weaker proofs in exchange for lower compromise risk).

---

## 6. Privacy Guarantees: Hiding and Binding

### 6.1 Hiding Property

**Claim**: Knowledge of the commitment `Com(d; r)` reveals nothing about the distance `d` to a polynomial-time adversary.

**Proof sketch (informal):**
- Suppose an adversary has two candidate distances `d₁` and `d₂` and observes a single commitment `Com = g^d × h^r` for unknown `d ∈ {d₁, d₂}` and unknown `r`.
- The adversary's task: distinguish which distance `d` was committed.
- For any fixed `r`, the adversary would need to solve the discrete log: recover `d` from `Com / h^r = g^d`.
- Under the DLP (discrete-log problem) in Ristretto255, this is intractable.
- Equivalently, the set `{g^d₁ × h^r : r ∈ Z_q}` and `{g^d₂ × h^r : r ∈ Z_q}` are computationally indistinguishable (both are uniform distributions over the group under a uniformly random `r`).

**In the Calm Witness context:**
- A counterparty receiving the commitment learns only that *some* distance was committed.
- The counterparty learns nothing about whether the distance was 0.1 (strong match) or 0.8 (weak match).
- Combined with the transparency-log anchor proving *when* the commitment was created, the counterparty can only infer freshness, not biometric state.

### 6.2 Binding Property

**Claim**: The operator cannot "open" a commitment `Com` to two different distances `d` and `d'` without being detected.

**Proof sketch:**
- Suppose an operator creates a commitment `Com = g^d × h^r`.
- Later, the operator claims `Com` opens to a different distance `d'`, revealing `(d', r')`.
- A verifier checks: is `g^d' × h^r' = Com`?
- If `d' ≠ d` but the check succeeds, then:
  ```
  g^d' × h^r' = g^d × h^r
  g^(d' - d) = h^(r - r')
  log_g(h) = (r - r') / (d' - d)
  ```
- This would reveal the discrete-log relationship between `g` and `h`.
- But `h` was chosen via hash-to-curve precisely so that no adversary can know `log_g(h)` without solving SHA3-256 preimage or the DLP itself.
- Therefore, the operator cannot produce two valid openings.

---

## 7. Composition with Everest 38 and Everest 45

### 7.1 Input from Everest 38

Everest 38 (Combined Distance Fusion) produces:
```
d_joint ∈ [0, 1]       (sigmoid-normalized likelihood-ratio fusion result)
d_joint_margin         (optional: margin to threshold, τ - d_joint)
```

Everest 44 receives `d_joint` as input and commits to it.

### 7.2 Output to Everest 45

Everest 45 (Distance Threshold Proof: `d < tau`) receives:
```
Com(d_joint; r)        (the commitment from E44)
template_id            (to recover per-principal threshold τ)
```

Everest 45 then constructs a Σ-protocol proof that:
```
∃ (d_int, r) such that:
  Com = g^d_int × h^r
  AND
  d_int < τ_scaled     (where τ_scaled = round(τ × 2^32))
```

The proof reveals neither `d_int` nor `τ_scaled` numerically; it only proves the inequality under commitment. The randomness `r` is used to construct the proof's challenge-response but is not disclosed.

---

## 8. Constant-Time Implementation

All arithmetic on `Com` must be constant-time to resist side-channel attacks (timing, power analysis, cache timing):

1. **Scalar multiplication**: Use Dalek's `RistrettoPoint::mul(scalar)`, which is constant-time with respect to the scalar's bits (Montgomery ladder or similar).
2. **Point addition**: Use constant-time group law (Dalek's point addition is constant-time on the curve model).
3. **Compression**: The `RistrettoPoint::compress()` operation in Dalek is constant-time.
4. **Field arithmetic**: All Z_q operations (scalar addition, reduction) are performed via constant-time field arithmetic (Dalek's `Scalar` type).

**No timing leaks on `d_int` or `r`:**
- The scalar multiplication `g^d_int × h^r` does not depend on the bits of `d_int` or `r` in a way that leaks them via timing.
- The randomness `r` is sampled from a cryptographically secure RNG and used only once per commitment; no reuse or dependent operations expose `r`.

---

## 9. Performance

**Per-session commitment cost:**

| Operation | Time (M-series Mac) | Time (iPhone 15 Pro) | Time (Android Snapdragon) |
|-----------|------------------|----------------|-------|
| Sample `r` from RNG | <0.1 ms | <0.5 ms | <0.5 ms |
| Fixed-point encode `d_int` | <0.01 ms | <0.01 ms | <0.01 ms |
| Scalar mult `g^d_int` | 0.5–1 ms | 1–2 ms | 1–2 ms |
| Scalar mult `h^r` | 0.5–1 ms | 1–2 ms | 1–2 ms |
| Point addition + compress | <0.1 ms | <0.2 ms | <0.2 ms |
| **Total per-commitment** | **<2 ms** | **<5 ms** | **<5 ms** |

This is negligible relative to the E36 and E37 inference time (handwriting distance ~50–100 ms, voice-transcript distance ~100–200 ms on phones). The commitment is a sub-1% overhead on per-session compute.

---

## 10. Security Parameters and Assumptions

**Security target (v0):** 128 bits of security (strength equivalent to AES-128).

- Ristretto255 provides 2^126 group order, yielding ~126 bits of classical security.
- This meets the 128-bit target for near-term deployments.

**Cryptographic assumptions:**
1. **Discrete Logarithm Problem (DLP)**: Finding `x` given `g^x` is hard in Ristretto255.
2. **Computational Diffie-Hellman (CDH)**: Given `g`, `g^a`, `g^b`, computing `g^(ab)` is hard.
3. **Hiding under DDH (Decisional Diffie-Hellman)**: The commitment perfectly hides `d` when `r` is uniformly random and `log_g(h)` is unknown.

**Assumptions NOT made:**
- We do not assume `h` was chosen with a secret relationship to `g`. The hash-to-curve construction rules out any efficient precomputation.
- We do not assume perfect randomness; a weaker RNG (e.g., system entropy with bias) would degrade binding slightly, but hiding remains intact under reasonable noise assumptions.

**Post-quantum security (v1+):**
- Pedersen commitments have no known post-quantum generalization with the same efficiency.
- Everest 96 will specify lattice-based alternatives (e.g., Ring-LWE variants) for v1+.
- For v0 (this document), post-quantum migration is out of scope.

---

## 11. Cross-References

- **Everest 14**: Enrollment protocol (template creation, per-principal calibration). Commitment strategy must match enrollment workflow.
- **Everest 15**: Template format spec. Stores baseline thresholds `τ_p` and calibration tables referenced by commitments.
- **Everest 36**: Handwriting distance function. Provides `d_h`, input to Everest 38.
- **Everest 37**: Voice-transcript distance function. Provides `d_v`, input to Everest 38.
- **Everest 38**: Combined Distance Fusion. Outputs `d_joint`, input to Everest 44 (this document).
- **Everest 45**: Distance Threshold Proof (`d < tau`). Uses commitment from E44 and randomness `r` to construct ZK proof.
- **Everest 46**: Template Identity Commitment. Commits to the `template_id` using the same Ristretto255 group.
- **Everest 56**: Biometric Match Predicate Evaluation. Consumes the commitment and threshold proof to decide `biometric_match_within(τ)`.
- **Everest 65**: Consent Record Commitment. Composes Pedersen commitments across multiple predicates.
- **Everest 96**: Post-Quantum Migration. Lattice-based successor to Pedersen (v1+).
- **Calm Pact §4.1**: Cryptographic group choice (Ristretto255 locked in v0.1). Generators `g` and protocol constants inherited from Pact.
- **ZKBB_USER_PROTOCOL_v0.md**: Master protocol specification. Section 4.2 describes the Σ-protocol family reused in E45.

---

— Calm, 2026-05-20
