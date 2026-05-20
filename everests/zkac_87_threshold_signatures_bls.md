# ZKAC Everest 87 — Threshold Signatures (BLS)

*Phase XXIII — Multi-Party Computation & Threshold Crypto. Prereq: ZKAC E86.*

---

## 1. The Primitive: N-of-M Threshold Signing

Joint principals—co-founders, families, DAOs, multi-signature authorities—require a cryptographic mechanism to authorize vault operations (issuance, key rotation, revocation) without any single party holding the complete signing key. Threshold signatures (N-of-M) solve this: a secret key is split into M shares, and any quorum of N shares suffices to produce a valid signature. No coalition smaller than N can sign; no single party reconstructs the full key.

BLS (Boneh-Lynn-Shacham) threshold signatures, deployed on pairing-friendly curves, provide this primitive with aggregate signatures—multiple partial signatures from different parties collapse into a single, compact signature verifiable against the threshold public key.

**Definition**: An (N, M) threshold signing scheme allows M shareholders to sign a message such that any N of them can generate a valid signature, and an attacker controlling fewer than N shares learns nothing about the secret key.

---

## 2. BLS Overview: Aggregate Signatures on Pairing-Friendly Curves

### 2.1 Why BLS

1. **Aggregate signatures**: Partial signatures from N signers merge into one compact signature (32–48 bytes, depending on the pairing). Traditional threshold schemes (e.g., Schnorr-based) require concatenating N signatures.
2. **Deterministic**: No randomness in signing. Reproducible signatures simplify auditability.
3. **Verifiable secret sharing**: BLS threshold construction (via Pedersen-Feldman VSS) allows shareholders to verify their share's correctness without revealing the secret.
4. **Pairing-based proofs**: Opens the door to zero-knowledge proofs over signatures (Everest 45–like constructions for signature predicates).
5. **Ethereum/Filecoin precedent**: BLS12-381 is deployed in Ethereum Proof-of-Stake consensus, proven under adversarial conditions.

### 2.2 Pairing-Friendly Curves: BLS12-381

**Curve selection**: BLS12-381 is a Barreto-Lynn-Scott (BLS) curve of embedding degree 12:

```
E: y² = x³ + 4       (over F_p)
r = 52435875175126190479447740508185965837690552500527637822603658699938581184513
p ≈ 2^255           (prime field modulus)
```

**Why BLS12-381:**

- **Efficiency on modern hardware**: Pairing computation on BLS12-381 runs in ~1–5 ms on commodity processors.
- **Standardization**: IETF draft (draft-irtf-cfrg-pairing-friendly-curves) has locked BLS12-381 as the canonical 128-bit-secure pairing curve.
- **Composability**: Filecoin, Ethereum, and many Cosmos chains use BLS12-381; ZKACs inherit existing infrastructure and audits.
- **Security**: The curve provides ~128 bits of security against known attacks (Pohlig-Hellman, MOV).

**Groups**:
- **G₁**: Points on E(F_p). Order r. Generator g₁.
- **G₂**: Points on the twist E'(F_p²). Order r. Generator g₂.
- **G_T**: The target group of the pairing, the multiplicative group of F_p¹² (or a subgroup). Isomorphic to Z_r (in terms of the group structure).

**Pairing**: A non-degenerate bilinear map:
```
e: G₁ × G₂ → G_T
e(aP, bQ) = e(P, Q)^(ab)
```

---

## 3. BLS Threshold Key Generation: Distributed Ceremony

### 3.1 The Ceremony Setup

Each participant `i ∈ [1, M]` is a principal in the joint vault. None of them ever see the complete signing key `sk`. Instead:

1. Each participant generates a secret polynomial over Z_r (degree N-1).
2. They share polynomial evaluations with each other.
3. Each participant aggregates all evaluations to form their own key share.
4. Verifiable commitments ensure no participant cheats.

### 3.2 Shamir Secret Sharing of the Secret Key

Let `sk ∈ Z_r` be the shared secret signing key (never constructed in plaintext). The dealer (or each participant acting as dealer simultaneously in a DKG variant) defines a polynomial:

```
f(x) = a₀ + a₁·x + a₂·x² + ... + a_{N-1}·x^{N-1}     (mod r)
```

where:
- `a₀ = sk` (the secret itself).
- `a₁, ..., a_{N-1}` are random coefficients.
- All arithmetic is in Z_r.

Each participant `i` receives their share:
```
sk_i = f(i)
```

**Property**: Any N evaluations of the polynomial f allow reconstruction via Lagrange interpolation. Fewer than N shares reveal nothing about `sk` (under the DLP).

### 3.3 Verifiable Secret Sharing (Feldman-VSS)

To prevent a dealer from distributing inconsistent shares, commitments are published:

```
C_j = g₁^{a_j}    for j = 0, 1, ..., N-1
```

where `g₁` is the G₁ generator. These commitments are public and immutable (appended to the ledger per Everest 15).

Participant `i` verifies their share `sk_i` by checking:
```
g₁^{sk_i} = C₀ · C₁^i · C₂^{i²} · ... · C_{N-1}^{i^{N-1}}
             = g₁^{a₀ + a₁·i + a₂·i² + ... + a_{N-1}·i^{N-1}}
             = g₁^{f(i)}
```

If the check fails, participant `i` broadcasts a complaint, the dealer is disqualified, and the ceremony restarts.

### 3.4 Public Key Construction

The shared public key (the threshold public key) is:
```
pk = sk · g₁ = a₀ · g₁ = C₀
```

This is publicly known from the ceremony. Any signature verifiable against `pk` proves that at least N shares participated.

---

## 4. BLS Threshold Signing Protocol

### 4.1 Partial Signature Generation

When a message `m` must be signed, a quorum of N participants (chosen from M) collectively sign:

1. **Participant `i` (if in quorum):**
   - Hash message to G₂: `H(m) ∈ G₂` (via hash-to-curve per RFC 9380).
   - Compute partial signature: `σ_i = sk_i · H(m)`.
   - Send `σ_i` to an aggregator (or each other, peer-to-peer).

2. **Aggregator** (or any quorum member):
   - Receive partial signatures `{σ_{i₁}, σ_{i₂}, ..., σ_{iₙ}}` from the N-quorum members.
   - Compute Lagrange coefficients over Z_r for the quorum indices:
     ```
     λ_i = ∏_{j∈quorum, j≠i} (0 - j) / (i - j)   (mod r)
     ```
   - Aggregate into a single signature:
     ```
     σ = ∑_{i∈quorum} λ_i · σ_i
       = ∑_{i∈quorum} λ_i · sk_i · H(m)
       = (∑_{i∈quorum} λ_i · sk_i) · H(m)
       = sk · H(m)                  (by Lagrange interpolation)
     ```

### 4.2 Signature Verification

Verification is identical to standard BLS:

```
Check: e(σ, g₂) = e(H(m), pk)
```

Equivalently:
```
e(sk · H(m), g₂) =? e(H(m), sk · g₂)
```

Both sides equal `e(H(m), g₂)^sk` by bilinearity. The verifier does not know which participants signed, how many, or the quorum configuration—only that a valid N-of-M quorum participated.

---

## 5. Composition with ZKAC E86 (MPC Framework) and ZKAC E88/E89

### 5.1 E86 Dependency

Everest 86 selects the MPC framework for ZKAC infrastructure. BLS threshold signing integrates as a concrete MPC application:

- **Silent OT (Oblivious Transfer)**: If E86 selects silent OT, the share-distribution phase leverages OT for secure point-to-point channels.
- **MPC ABY / GMW**: General-purpose MPC can verify partial signature correctness before aggregation.

E87 is a **high-level specification**; implementation specifics depend on E86's choice.

### 5.2 E88: Threshold Decryption

Everest 88 (threshold decryption) pairs with E87 for dual-key vaults:
- The vault's **encryption key** is split via E89 (Shamir secret sharing).
- The vault's **signing key** is split via E87 (BLS threshold signing).

Both share the same key-derivation root and the same quorum structure (N-of-M).

### 5.3 E89: Secret Sharing of Vault Keys

Everest 89 uses Shamir secret sharing (the polynomial-based component of E87) to distribute holder vault keys across N trusted parties (e.g., family members, trusted escrow agents). Upon recovery (Everest 30), N-of-M trustees collaboratively reconstruct the key via Lagrange interpolation, using the same mathematics as E87 share reconstruction.

### 5.4 E86/E87/E88/E89 Composition Flow

```
[E86: Choose MPC framework]
        ↓
[E87: BLS threshold signatures for vault operations]
        ↓
[E88: Threshold decryption of vault data]
        ↓
[E89: Shamir secret sharing of vault keys for recovery]
        ↓
[Composition: Joint principal vault with N-of-M signing + decryption + recovery]
```

---

## 6. Use Cases

### 6.1 Joint Founder Vault

Two co-founders of a startup establish a joint ZKAC vault. The signing key is split 2-of-2 (either founder alone cannot sign; both must participate). Both founders hold a share. Vault operations (issuing credentials, rotating issuer keys) require both signatures.

### 6.2 Family Principal Recovery

A principal designates 3 family members as trustees. The holder vault key is split 2-of-3 (any 2 of the 3 can collaboratively recover the vault if the principal loses their device). On recovery request, the principal proves their identity to the 2 trustees, and they collectively re-encrypt the vault key.

### 6.3 DAO Multi-Sig Issuer

A decentralized autonomous organization issues ZKACs. The issuer's signing key is split 4-of-7 (any 4 of the 7 governance members can authorize an issuance). New issues require a 4-of-7 quorum, providing Byzantine fault tolerance (tolerate up to 3 compromised or offline members).

### 6.4 Enterprise Master Key

A bank's Calm witness operator holds a master signing key split 3-of-5 across its security team. Any 3 members can sign witness attestations. This prevents a single employee from forging attestations while tolerating brief absences.

---

## 7. Post-Quantum Migration Plan

BLS12-381 pairing cryptography offers no known quantum-safe security (Shor's algorithm breaks discrete log and pairing problems in polynomial time).

**Migration to lattice-based threshold signing (v1+):**

- **CRYSTALS-Dilithium threshold variants**: Threshold versions of Dilithium (NIST post-quantum standard) support secret-sharing and multi-party signing over lattices.
- **Falcon threshold**: Lattice-based signatures with smaller keys and faster signing.
- **Timeline**: ZKAC v0.x uses BLS12-381; E96 specifies the lattice-based transition for v1.0+ deployments. Hybrid signing (both classical BLS and lattice schemes in parallel) may precede full migration.

---

## 8. Acceptance Tests: T-Z87.1–T-Z87.5

**T-Z87.1: DKG Ceremony**
- M=5 participants, N=3 threshold. Each participant generates a secret polynomial, publishes commitments, and verifies shares. Final public key `pk` is consistently computed by all participants. Acceptance: ceremony completes, all commitments match, `pk` is unique and deterministic.

**T-Z87.2: Signing Under Threshold**
- 3-of-5 quorum signs a message `m`. The aggregated signature `σ` is verifiable: `e(σ, g₂) = e(H(m), pk)`. Acceptance: signature verifies correctly. Attempting to sign with only 2 participants fails (aggregated signature does not verify).

**T-Z87.3: Lagrange Correctness**
- Lagrange interpolation for different quorum compositions (indices 1,2,3 vs. 2,3,4 vs. 1,3,5) all yield the same aggregated signature. Acceptance: all valid quorum compositions produce identical signatures.

**T-Z87.4: Dishonest Share Detection**
- A participant distributes an inconsistent share. Verification against the public commitments fails. The participant is disqualified. Acceptance: mismatch detected before aggregation; ceremony can restart without the dishonest participant.

**T-Z87.5: Post-Quantum Placeholder**
- Specification document for lattice-based threshold signing (Dilithium or Falcon threshold variants) is drafted and reviewed. Acceptance: v1 migration plan is clear and executable.

---

## 9. Composition with Everest Neighbors

- **E86**: MPC framework selection determines OT/SPDZ/circuit types used in E87 implementation.
- **E88**: Threshold decryption uses identical quorum structure and Shamir reconstruction.
- **E89**: VSS and polynomial evaluation are shared primitives.
- **E94**: Post-quantum MPC migration includes E87 lattice-based alternatives.

---

## 10. Security Parameters and Assumptions

**Security target**: 128 bits (classical).

- **BLS12-381 discrete log**: 2^128 operations to recover a scalar.
- **Pairing inversion**: Best known attacks are subexponential (Pohlig-Hellman on the curve order, which is 2^256, and the MOV reduction to discrete log in F_p¹², which is 2^128 equivalent after symmetry breaking).

**Assumptions**:
1. **Computational Diffie-Hellman (CDH)** in G₁ and G₂.
2. **Pairing inversion hardness**: Cannot compute sk from `g₁^sk` given access to the pairing.
3. **Discrete log problem** in Z_r.
4. **Secret sharing soundness**: Fewer than N shares are information-theoretically independent of sk.
5. **Hash-to-curve safety**: `H(m)` is uniformly distributed over G₂ (RFC 9380 construction).

**Assumptions NOT made**:
- No trusted dealer. The DKG ceremony (E86 MPC implementation) produces shares without any participant ever reconstructing the full key.

---

## 11. Specification and Implementation Notes

**Hash-to-curve**:
```
H(m) = hash_to_point_g2(m, "ZKAC-E87-BLS12381")
```
Using RFC 9380 (Hashing to Elliptic Curves), specifically the BLS12-381 suite from draft-irtf-cfrg-pairing-friendly-curves.

**Libraries**:
- **BLST** (Supranational): Production-grade BLS12-381 pairing library, used in Ethereum and Filecoin.
- **Zexe** (ZK + elliptic-curve): Rust library with threshold BLS implementations.
- **Herumi BLS**: Fast C/Rust BLS12-381 with SIMD optimizations.

**Implementation checklist** (v0):
1. DKG ceremony per E86.
2. Verifiable secret sharing (Feldman-VSS) with commitments stored on ledger.
3. Partial signature generation with Lagrange interpolation.
4. Signature aggregation and compression.
5. Verification via pairing check.
6. Serialization of public keys, commitments, and signatures in fixed-size byte formats.
7. Constant-time operations to resist timing side channels.

---

## 12. Version and Signoff

**Version**: E87 v0.1, 2026-05-20.
**Status**: Specification complete. Ready for v1 implementation (E86 framework selection required).

Composition dependencies: E86 (selected), E88 (parallel), E89 (parallel), E94 (future lattice migration).

— Calm, 2026-05-20
