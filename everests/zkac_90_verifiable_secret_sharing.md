# ZKAC Everest 90 — Verifiable Secret Sharing

*Phase XXIII — Multi-Party Computation & Threshold Crypto. Prereq: ZKAC E89.*

---

## 1. The Primitive: VSS Without Reconstruction Risk

Secret sharing of vault keys (E89) splits a key across N trustees so any M-of-N can reconstruct it. Without verifiability, a malicious dealer distributes inconsistent shares: one trustee receives a share for key K₁, another for K₂. At reconstruction, the "recovered" key is gibberish, and nobody knows who cheated.

Verifiable Secret Sharing (VSS) makes this impossible. Each share recipient can independently verify: "My share is consistent with what the dealer claims to have shared." If any share fails verification, the ceremony aborts and the dealer is disqualified without revealing the secret.

**Definition**: A VSS scheme allows a dealer to distribute shares of a secret such that (1) any M-of-N shareholders can reconstruct the secret, (2) any shareholder can verify their share's correctness against public commitments, (3) fewer than M shareholders learn nothing about the secret, and (4) the dealer cannot equivocate (cannot later claim a different secret was shared).

---

## 2. Construction Options: Feldman vs. Pedersen

### 2.1 Feldman VSS

**Mechanism**: The dealer commits to polynomial coefficients using discrete-log commitments.

Dealer chooses polynomial `f(x) = a₀ + a₁·x + ... + a_{M-1}·x^{M-1}` (mod r), where `a₀` is the secret.

Commitments (public):
```
C_j = g^{a_j}    for j = 0, 1, ..., M-1
```

Shareholder i receives `s_i = f(i)` and verifies:
```
g^{s_i} =? C₀ · C₁^i · C₂^{i²} · ... · C_{M-1}^{i^{M-1}}
```

**Pros**:
- Standard, deployed in BLS threshold signing (E87).
- Compact commitments: M small group elements.
- Shares are small scalars.

**Cons**:
- Commitment reveals the secret's discrete log (in the exponent). An adversary with discrete log oracle could recover the secret, though no such oracle exists classically.
- Computationally hiding only, not information-theoretically hiding.

### 2.2 Pedersen VSS

**Mechanism**: The dealer commits to polynomial coefficients using blinded discrete-log commitments, hiding the actual coefficients.

Dealer commits via two polynomials: `f(x) = a₀ + a₁·x + ...` (secret polynomial) and `g(x) = r₀ + r₁·x + ...` (random mask).

Commitments (public):
```
C_j = g^{a_j} · h^{r_j}    for j = 0, 1, ..., M-1
```

where `h` is a second generator (h = g^ρ for some secret ρ known only in the exponent).

Shareholder i receives `(s_i, t_i) = (f(i), g(i))` and verifies:
```
g^{s_i} · h^{t_i} =? C₀ · C₁^i · C₂^{i²} · ... · C_{M-1}^{i^{M-1}}
```

**Pros**:
- Information-theoretically hiding: commitments reveal no information about the secret, even to an oracle that solves discrete log.
- Same reconstruction guarantees as Feldman.

**Cons**:
- Requires two values per share: `(s_i, t_i)`.
- Commitments are 2M group elements (double Feldman).
- Slightly more bandwidth at distribution.

---

## 3. V0 Chosen Mechanism: Pedersen VSS over Ristretto255

ZKAC E90 mandates **Pedersen VSS** for v0:

**Rationale**:
- E89 (vault-key secret sharing) is the critical-path use case: if a dealer is malicious, trustees discover it before any decryption attempt fails.
- Information-theoretic hiding aligns with ZKAC design constraint 2 (holder vault sovereignty): even if the dealer's commitment is observed by an adversary, the secret remains unconditionally hidden.
- Composes cleanly with E87 (BLS threshold signing). Both use the same curve.

**Curve: Ristretto255**
- Ristretto255 is a prime-order group built on Curve25519 (255-bit prime field), with optimized group operations for constant-time arithmetic.
- 128-bit security against classical attackers.
- Widely implemented (libsodium, Dalek, etc.).
- Resists timing side channels via curve-native constant-time operations.

**Generators**:
```
g = Ristretto255::basepoint()          (standard generator)
h = HASH_TO_GROUP("ZKAC-E90-H", g)    (derived via RFC 9380 adaptation for Ristretto)
```

The ZKAC infrastructure publishes `g` and `h` at v0 launch; they are fixed and immutable (stored on the chain, E15 audit log).

---

## 4. Pedersen VSS Algorithm Steps

### 4.1 Dealer Setup

1. **Secret & polynomials**: Dealer chooses secret `s ∈ Z_r` and M-1 random values.
   - Polynomial 1: `f(x) = a₀ + a₁·x + ... + a_{M-1}·x^{M-1}` where `a₀ = s`.
   - Polynomial 2: `b(x) = r₀ + r₁·x + ... + r_{M-1}·x^{M-1}` where `r₀` is random.

2. **Commitments**: Compute and publish:
   ```
   C_j = g^{a_j} · h^{r_j}    for j = 0, 1, ..., M-1
   ```
   Store `C = [C₀, C₁, ..., C_{M-1}]` in the ledger (immutable).

3. **Share distribution**: For shareholder i ∈ [1, N]:
   - Compute: `s_i = f(i) mod r` and `t_i = b(i) mod r`.
   - Send `(s_i, t_i)` to shareholder i via authenticated, encrypted channel (per E27 holder key custody).
   - Do NOT broadcast; point-to-point only.

### 4.2 Shareholder Verification

Shareholder i receives `(s_i, t_i)` and verifies against the public commitment:

```
Check: g^{s_i} · h^{t_i} =? C₀ · C₁^i · C₂^{i²} · ... · C_{M-1}^{i^{M-1}}
```

Expand RHS using `C_j = g^{a_j} · h^{r_j}`:
```
RHS = (g^{a₀} · h^{r₀}) · (g^{a₁} · h^{r₁})^i · (g^{a₂} · h^{r₂})^{i²} · ...
    = g^{a₀ + a₁·i + ... + a_{M-1}·i^{M-1}} · h^{r₀ + r₁·i + ... + r_{M-1}·i^{M-1}}
    = g^{f(i)} · h^{b(i)}
    = g^{s_i} · h^{t_i}   = LHS  ✓
```

If verification fails: shareholder i broadcasts a complaint. The dealer is disqualified. The ceremony aborts without reconstructing s or revealing b(x).

### 4.3 Commitment Publication

Commitments `C` are stored on the ZKAC chain (E15 audit log, immutable). This enables:
- Any verifier to later audit that a given share was consistent with the published commitments.
- Disputes to be resolved cryptographically: if a shareholder claims a share was inconsistent, a verifier can check the math.
- Privacy: verifiers never learn `s_i` values; they only check commitments.

---

## 5. Reconstruction: Any M-of-N Shareholders

Any M shareholders (indices i₁, i₂, ..., i_m) collaborate to recover the secret:

1. **Lagrange interpolation**: Compute coefficients:
   ```
   λ_j = ∏_{k≠j} (0 - i_k) / (i_j - i_k)   (mod r)
   ```

2. **Reconstruct secret**:
   ```
   s = ∑_{j=1}^{M} λ_j · s_{i_j}
   ```

3. **Why it works**: `s = ∑_{j=1}^{M} λ_j · f(i_j) = f(0) = a₀ = s` (via Lagrange polynomial properties).

**Information-theoretic security**: Fewer than M shareholders hold shares `s_i` but NOT the mask values `t_i`. To them, each `s_i` is a uniform random element of Z_r; any secret and any subset of < M shares are consistent. They learn zero bits about s.

---

## 6. Composition with ZKAC E89 (Secret Sharing of Vault Keys)

E89 applies Shamir secret sharing (the polynomial-reconstruction component of VSS) to split a holder's vault encryption key across N trustees.

E90 wraps E89 with verifiability:

```
[E89: Dealer generates polynomial, computes shares]
                    ↓
[E90: Dealer publishes commitments, shareholders verify shares]
                    ↓
[Verified shares stored in trustees' secure enclaves]
                    ↓
[On recovery: M-of-N trustees submit verified shares, reconstruct key]
```

The chain ledger (per E15) stores the commitment transcript `C`. In a dispute—e.g., a trustee claims their share was incorrect—any party can audit:
```
g^{disputed_share} · h^{disputed_mask} =? C₀ · C₁^{trustee_index} · ... ?
```

If NO, the trustee is lying. If YES, the trustee's claim is substantiated, and the dealer is liable.

---

## 7. Composition with ZKAC E87 (Threshold Signatures)

E87 uses Feldman VSS (discrete-log commitments) for share verification during a BLS DKG ceremony.

E90 is compatible but orthogonal:
- E87 is for signing-key VSS (where equivocation is instantly detectable: a bad signature fails verification).
- E90 is for encryption-key VSS (where equivocation is discovered only at reconstruction, E89).

Both share the same polynomial-reconstruction mathematics. A unified Ristretto255 curve library can implement both, saving implementation and audit cost.

---

## 8. Composition with ZKAC E86/E87/E88/E89

```
[E86: MPC framework provides authenticated channels for E90 share distribution]
        ↓
[E87: BLS threshold signing uses Feldman VSS (variant of E90 commitments)]
        ↓
[E88: Threshold decryption uses same curve + group operations as E90]
        ↓
[E89: Shamir secret sharing of vault keys (polynomial backbone)]
        ↓
[E90: Pedersen VSS adds verifiability + information-theoretic hiding]
        ↓
[Result: Joint principal recovery with tamper-proof key shares]
```

---

## 9. T-Z90.1–T-Z90.5 Acceptance Tests

**T-Z90.1: Commitment Consistency**
- Dealer distributes shares `{(s_1, t_1), ..., (s_N, t_N)}` and publishes commitments `C`.
- Each shareholder i verifies: `g^{s_i} · h^{t_i} = ∏_{j=0}^{M-1} C_j^{i^j}`.
- Acceptance: All N shareholders' verifications pass.

**T-Z90.2: Reconstruction Correctness**
- M shareholders reconstruct the secret `s' = ∑_{j=1}^{M} λ_j · s_{i_j}`.
- Verify `g^{s'} = C₀` (the original public commitment to the secret).
- Acceptance: Reconstructed value matches the commitment.

**T-Z90.3: Cheating Dealer Detection**
- Dealer deliberately distributes an inconsistent share to shareholder k.
- Shareholder k verifies and fails: `g^{s_k} · h^{t_k} ≠ ∏_{j=0}^{M-1} C_j^{k^j}`.
- Acceptance: Mismatch is detected; ceremony aborts; s is never reconstructed.

**T-Z90.4: Fewer-Than-M Shareholders Learn Nothing**
- M-1 shareholders hold shares but not the mask polynomial `b(x)`.
- Adversary observes any M-1 shares and all commitments C.
- Adversary cannot predict the next share `s_M` with probability > 1/r.
- Acceptance: Information-theoretic bound is tight (formal proof via polynomial interpolation).

**T-Z90.5: Ristretto255 Constant-Time Operations**
- Implementation verifies shares and reconstructs secrets in constant time (no branch on secret values).
- Timing measurements confirm ≤ 1% variance across random secret inputs.
- Acceptance: No timing side-channel leakage of shares or secrets.

---

## 10. Privacy & Auditability

**Shareholder Privacy**:
- Commitments C are public; shares `(s_i, t_i)` are private to shareholder i.
- Verifiers do NOT learn which shares exist or belong to whom.
- Only the dealer (who is disqualified if they cheat) knows all shares and mask values.

**Dispute Resolution**:
- If a shareholder claims their share was incorrect, the ZKAC chain publishes a cryptographic proof:
  - Shareholder submits their `(s_i, t_i)`.
  - Chain verifies: `g^{s_i} · h^{t_i} =? ∏_{j=0}^{M-1} C_j^{i^j}`.
  - If YES: shareholder's claim is upheld; dealer is slashed (E21).
  - If NO: shareholder is lying; shareholder is slashed.

**Revocation**:
- Shares can be revoked (E33, credential expiration). On revocation, the commitment set C is marked as stale on the chain. New shares can be issued under a fresh ceremony.

---

## 11. Post-Quantum Migration

Ristretto255 is elliptic-curve based. Shor's algorithm breaks discrete log in polynomial time on quantum computers.

**Lattice-based VSS (v1+)**:
- Secret sharing over lattice problems (Learning With Errors, Ring-LWE) offers post-quantum security.
- Pedersen-like commitment schemes exist over lattices (e.g., Fiat-Shamir commitments via module-LWE).
- **Timeline**: E90 v0 uses Ristretto255; migration to lattice VSS begins after NIST standardization completes (2024). E94 specifies the v1 timeline.

---

## 12. Implementation Notes

**Ristretto255 Libraries**:
- **libsodium** (C): Stable, audited, widely deployed.
- **Dalek** (Rust): High-performance Ristretto255 with constant-time guarantees.
- **CIRCL** (Go): Production-grade with side-channel resistance.

**Checklist (v0)**:
1. Generators `g`, `h` fixed and published in ZKAC registry.
2. Commitment publication to immutable ledger (E15).
3. Shareholder verification logic (constant-time scalar multiplication + group addition).
4. Lagrange interpolation over Z_r.
5. Reconstruction via polynomial evaluation.
6. Dispute resolution via chain audit (commitments + claimed shares).
7. Test vectors for deterministic cryptographic reproducibility.

---

## 13. Composition with E86, E87, E88, E89

- **E86**: Authenticated channels for share distribution.
- **E87**: BLS DKG uses Feldman VSS (special case of E90 with single generator).
- **E88**: Threshold decryption uses same curve operations + Lagrange interpolation.
- **E89**: Shamir secret sharing (polynomial evaluation); E90 adds verifiable commitments.

---

## 14. Version and Signoff

**Version**: E90 v0.1, 2026-05-20.
**Status**: Specification complete. Ready for implementation (E89 dependency required).

**Acceptance**: T-Z90.1–T-Z90.5 pass.

**Signoff Dependencies**:
- E89 (secret sharing backbone): prereq.
- E87 (BLS threshold signing): informative reference.
- E86 (MPC framework): authenticated channels required.
- E15 (issuer audit log): commitment publication required.

Approved for v0 implementation. Ristretto255 Pedersen VSS is information-theoretically hiding, composable with E87/E88/E89, and resistant to timing side channels. Migration to lattice VSS will begin post-NIST standardization (E94).

— Calm, 2026-05-20
