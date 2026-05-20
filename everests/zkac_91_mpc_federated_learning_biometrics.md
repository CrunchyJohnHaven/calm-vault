# ZKAC Everest 91 — MPC for Federated Learning over Biometrics

*Phase XXIII — Multi-Party Computation & Threshold Crypto. Prereq: ZKAC E86.*

---

## 1. Overview

Multiple principals participate in a shared biometric system (Calm Witness Everests 36–40): each has enrolled genuine templates and is testing hypotheses on decision thresholds for False Accept Rate (FAR) and False Reject Rate (FRR) calibration. The problem: **jointly optimize a single shared decision threshold τ across N principals such that aggregate FAR/FRR curves are jointly minimized** without any principal revealing their raw biometrics, distance distributions, or individual FAR/FRR curves to others.

This is a **federated learning problem constrained by cryptographic privacy**: the aggregator (a trusted but not necessarily honest entity, e.g., the Calm Witness coordinator) must update a shared loss function across multiple principals' private data without ever accessing the data itself. The federated parameter is the decision threshold τ; each principal's local loss is their individual FAR/FRR at τ, computed over their own biometric samples.

**Why MPC:** No principal trusts the aggregator with unencrypted distances. No two principals should learn each other's distance distributions. The aggregator must be able to compute weighted gradient updates and threshold-decryption announcements *without seeing* the underlying distance values. This requires **differentially-private federated SGD composed with multi-party computation** and **threshold decryption** of final model parameters (Everests 87–90).

---

## 2. The Problem Framed: FAR/FRR Threshold Calibration as Federated Learning

### 2.1 Non-Private Baseline (What We Cannot Do)

In a naive centralized setup, all principals would upload their distance samples {d^i_1, ..., d^i_{M_i}} to a central server. The server would:
1. Pool all N × M distances.
2. For each threshold τ, compute global FAR(τ) and FRR(τ).
3. Find τ* = argmin_τ |FAR(τ) - FRR(τ)| (the Equal Error Rate threshold).
4. Announce τ*.

**Privacy violation:** The server and any colluding principals learn the full distance distribution of every participant. This leaks template stability, enrollment variance, and impostor-pair confusion patterns—all biometric footprints.

### 2.2 Federated Learning Reformulation

Reframe the problem as **distributed empirical risk minimization**:

- **Local data:** Principal i holds N_i distance samples {d^i_1, ..., d^i_{N_i}} (genuine comparisons) and M_i distance samples {d^i_{N_i+1}, ..., d^i_{N_i+M_i}} (impostor comparisons).
- **Local loss:** For a candidate threshold τ, principal i computes
  ```
  L_i(τ) = FAR_i(τ) + FRR_i(τ)
          = (# impostors accepted at τ) / M_i + (# genuines rejected at τ) / N_i
  ```
- **Global objective:** Minimize the weighted average loss
  ```
  L(τ) = ∑_i w_i · L_i(τ)
  ```
  where w_i is principal i's weight (typically N_i / total_genuine_samples, ensuring equal contribution per genuine comparison).

### 2.3 Privacy Constraints (Design Invariants)

1. **No raw biometrics leave device:** Distances d^i_j are computed locally; only sufficient statistics (encrypted loss values, gradient vectors) are transmitted.
2. **No two principals collide:** Principal i cannot infer principal j's distance distribution, even through multiple rounds of federated updates.
3. **Aggregator is honest-but-curious:** The aggregator (Calm Witness coordinator) computes correctly but is assumed adversarial on privacy: it must not see unencrypted distances, gradients, or per-principal loss curves.
4. **Differential privacy budget:** Every federated round adds differential privacy noise (ε-bounded). Across K rounds, total ε-consumption is tracked; composition theorems bound privacy leakage.

---

## 3. The Protocol: Differentially-Private Federated SGD over MPC

### 3.1 Setup Phase

**Participants:**
- N principals (P_1, ..., P_N), each with enrolled biometric data.
- One aggregator (A), run by Calm Witness, entrusted with orchestration but not data access.
- An MPC coordinator (C), which may be the same entity as A or a distinct trusted third party. C facilitates threshold decryption (Everest 90).

**Initialization:**
1. All N principals and the aggregator execute a **distributed key generation ceremony** (DKG, Everest 86):
   - Generate a shared encryption keypair (pk, sk) where sk is secret-shared among N principals via Shamir (Everest 89).
   - Any N_th threshold of principals can decrypt; no single principal or the aggregator can decrypt unilaterally.
2. All principals agree on:
   - Initial threshold candidate τ_0 (e.g., the Equal Error Rate from a prior study, or τ_0 = 0.5).
   - Learning rate η (e.g., η = 0.01).
   - Differential privacy parameters: noise scale σ_DP, clipping threshold C_clip, privacy budget ε_total (e.g., ε = 0.5, consumed over rounds).
   - Number of federated rounds K (e.g., K = 10).

### 3.2 Federated Round t (for t = 1, ..., K)

#### Round t.1: Local Loss Computation (On-Device)

Each principal P_i (working on their device):

1. **Compute local FAR/FRR at τ_t:**
   ```
   FAR_i(τ_t) = (# d^i_j < τ_t, j ∈ Impostor set) / M_i
   FRR_i(τ_t) = (# d^i_j ≥ τ_t, j ∈ Genuine set) / N_i
   ```

2. **Compute local loss:**
   ```
   L_i(τ_t) = FAR_i(τ_t) + FRR_i(τ_t)
   ```

3. **Compute gradient (via finite differences):**
   ```
   g_i(τ_t) ≈ (L_i(τ_t + ε_fd) - L_i(τ_t - ε_fd)) / (2 ε_fd)
   ```
   where ε_fd is a small finite-difference step (e.g., ε_fd = 0.001).

4. **Clip gradient (for DP guarantee):**
   ```
   g_i^clipped(τ_t) = g_i(τ_t) / max(1, |g_i(τ_t)| / C_clip)
   ```

5. **Add Gaussian noise (DP mechanism):**
   ```
   g_i^noisy(τ_t) = g_i^clipped(τ_t) + Z
   where Z ~ N(0, (σ_DP · C_clip)² · I)
   ```
   The noise variance σ_DP² is calibrated so that the privacy loss per round is ε_t ≤ ε_total / K.

6. **Encrypt the noisy gradient:**
   ```
   c_i,t = Enc(pk, g_i^noisy(τ_t))
   ```
   using the shared public key pk from DKG. Encryption is semantically secure (IND-CPA, e.g., ElGamal or Paillier).

7. **Send encrypted gradient to aggregator:** P_i uploads c_i,t to A.

#### Round t.2: Aggregation (On Aggregator)

The aggregator A (honest-but-curious):

1. **Receive encrypted gradients** {c_1,t, c_2,t, ..., c_N,t} from all principals.

2. **Aggregate in encrypted domain** (homomorphic addition):
   ```
   C_t = ∏_i c_i,t   (multiplicative homomorphic encryption)
         = Enc(pk, ∑_i g_i^noisy(τ_t))
   ```

3. **Compute aggregate gradient (still encrypted):**
   ```
   c_bar,t = C_t / N^2   (division via multiplicative inverse, per Paillier or ElGamal)
           = Enc(pk, (1/N) · ∑_i g_i^noisy(τ_t))
   ```

4. **Optionally threshold-encrypt the aggregated gradient** (Everest 90):
   - Encrypt c_bar,t so that it can only be decrypted if N_th principals vote to proceed.
   - This adds Byzantine robustness: if the aggregator is compromised, it cannot unilaterally decrypt and leak the gradient.

5. **Send encrypted aggregate to MPC coordinator C** (which may be A itself or a separate entity).

#### Round t.3: Threshold Decryption & Parameter Update (MPC Coordinator)

The MPC coordinator C:

1. **Initiate threshold decryption protocol** (e.g., threshold ElGamal with Everest 87–90 infrastructure):
   - Request N_th principals to contribute their decryption shares.
   - Each principal P_i uses their share sk_i to compute a partial decryption d_i,t.
   - Aggregation formula (Lagrange interpolation, per Everest 87):
     ```
     bar_g,t = ∑_i λ_i · d_i,t
     ```
     where λ_i are Lagrange coefficients and bar_g,t is the decrypted aggregate gradient.

2. **Update the shared threshold:**
   ```
   τ_{t+1} = τ_t - η · bar_g,t
   ```

3. **Broadcast τ_{t+1}** to all principals (and optionally publish on a ledger for auditability, per ZKAC Everest 40).

#### Round t.4: Liveness & Malicious-Aggregator Detection

- If the aggregator does not produce a valid decryption within a time window, any principal can challenge (broadcast their decryption share publicly, triggering a fallback multi-party reconstruction).
- If the aggregator's announced τ_{t+1} is inconsistent with the aggregate gradient, principals can request an audit (replay the homomorphic computation step).

### 3.3 Final Output (After K Rounds)

The converged threshold τ_K is announced and committed to a chain (per ZKAC Everest 17, 24):

```
Chain entry:
  timestamp: <round K completion time>
  τ_final: τ_K
  digest: H(all round transcripts)
  witnesses: [P_1, ..., P_N signed]
```

All principals attest to τ_K via threshold signatures (Everest 87). The Calm Witness system pins τ_K globally.

---

## 4. Construction Details: Cryptographic Mechanisms

### 4.1 Homomorphic Encryption (Additive or Multiplicative)

Two options, both viable:

**Option A: Paillier (Additive Homomorphic)**
- **Encryption:** c = Enc(m) via Paillier's asymmetric cryptosystem.
- **Homomorphic addition:** Enc(m_1) · Enc(m_2) = Enc(m_1 + m_2) (mod N²).
- **Scalar multiplication:** Enc(m)^k = Enc(k · m) (mod N²).
- **Decryption:** Requires private key (secret shared via Shamir, Everest 89).
- **Pros:** Native addition, well-studied, widely deployed (e.g., CENSUS, genomics).
- **Cons:** Slower decryption than ElGamal; N can be very large (2048 bits for 128-bit security).

**Option B: ElGamal (Multiplicative Homomorphic)**
- **Encryption:** c = (c_1, c_2) = (g^r, m · h^r) where h = g^x (public key).
- **Homomorphic multiplication:** Enc(m_1) · Enc(m_2) = (c_1^(1) · c_1^(2), c_2^(1) · c_2^(2)) = Enc(m_1 · m_2).
- **Scalar exponentiation:** Enc(m)^a = Enc(m^a).
- **Decryption:** Discrete log recovery (via threshold key shares, Everest 87).
- **Pros:** Compact keys, BLS12-381 pairing-compatible, threshold decryption integrates with Everest 87.
- **Cons:** Multiplicative, not additive; gradient encoding requires exponential form.

**v0 choice: ElGamal on BLS12-381 (G₁ group)**

Rationale: Composes with Everest 87 (BLS threshold signatures) and Everest 90 (verifiable secret sharing). The gradient is encoded as g^{bar_g,t}, and decryption recovers bar_g,t via discrete-log oracle (on smaller fields, feasible; on large fields, requires Pollard-rho or indexed tables).

### 4.2 Gradient Encoding & Quantization

Gradients are real-valued (the derivative of FAR/FRR w.r.t. τ). Encoding into group elements:

1. **Quantize gradient to integer:** bar_g,t (real) → ⌊bar_g,t · 10^6⌋ (integer Z).
2. **Encode as group element:** Enc(Z) = g^Z in ElGamal.
3. **After decryption:** Recover Z via discrete log, then bar_g,t ≈ Z / 10^6.

**Precision loss:** 10^6 quantization levels suffices for τ ∈ [0, 1]; precision ~ 10^{-6} threshold granularity is acceptable for FAR/FRR calibration.

**Discrete log complexity:** If Z is bounded (Z ∈ [-10^6, 10^6], ~21 bits), Pollard-rho on the order-r subgroup costs 2^10.5 group operations, or use an indexed table (baby-step giant-step, ~2^11 precomputation and ~2^11 lookup per decryption).

### 4.3 Differential Privacy Accounting

Each round, a principal adds Gaussian noise with scale σ_DP. The differential privacy loss is:

```
ε_t = C_clip / (N · σ_DP)
```

(For sensitivity C_clip, noise distribution N(0, σ_DP²), the differential privacy loss is approximately ε per round.)

**Total privacy after K rounds (Composition via Moments Accountant):**
```
ε_total ≈ (√K) · ε_t   (sublinear composition, better than direct sum)
```

**Example calibration:**
- ε_t = 0.01 per round (strong per-round privacy).
- K = 10 rounds.
- ε_total ≈ 0.1 (total, via moments accountant).
- Interpretation: an adversary observing all K rounds learns < 0.1 bits of information about any single principal's distance distribution.

**Noise scale setting:**
```
σ_DP = C_clip · (√K / ε_total) = 1 · (√10 / 0.1) ≈ 31.6
```

Each principal's noisy gradient ≈ true gradient ± N(0, 31.6²) ≈ true gradient ± N(0, 1000). Over K rounds, averaging reduces variance by √K, yielding final estimate uncertainty ~± 10 per component.

---

## 5. Per-Step Privacy Guarantees & Composition

### 5.1 Round-Level Privacy (Step t)

**Claim:** For any two neighbor datasets differing in a single sample from principal i, the distribution of principal i's encrypted gradient c_i,t is indistinguishable to the aggregator (up to ε_t differential privacy).

**Proof sketch:**
1. Gradient clipping + noise addition ensures (ε_t, δ)-DP locally (Gaussian mechanism).
2. Encryption via semantically secure ElGamal ensures that c_i,t reveals nothing about the plaintext except for the aggregate (via homomorphic aggregation).
3. Combined: no single principal's privacy-loss term leaks beyond ε_t.

### 5.2 Cross-Principal Isolation (Collusion Resistance)

**Claim:** No two principals can collude to infer each other's distance distributions.

**Mechanism:**
1. Each principal's gradient is independently noised and encrypted.
2. The aggregator performs homomorphic aggregation, collapsing all N encrypted gradients into one.
3. Individual decryption shares are published only via threshold decryption (Everest 87, 90), requiring N_th-quorum consensus.
4. A malicious principal holding their decryption share sk_i cannot decrypt the aggregate without N-1 other principals' shares (information-theoretic secret sharing).

### 5.3 Aggregator Privacy Leakage

**Honest-but-curious aggregator:** The aggregator can infer:
- **Noisy aggregate gradient** bar_g,t (after decryption, shared with all principals).
- **Convergence trajectory** {τ_0, τ_1, ..., τ_K}.

**Cannot infer:**
- Any per-principal loss L_i(τ_t).
- Any per-principal gradient g_i(τ_t).
- Any per-principal distance sample d^i_j.

**Reconstruction attacks:** If the aggregator colludes with a subset of < N_th principals, they still cannot reconstruct the full sk (Shamir threshold property). However, they learn the aggregate gradient, which is by design (non-private aggregation is necessary for convergence).

### 5.4 Differential Privacy Budget Across Composition

**Total budget after K rounds:**
```
ε_total ≈ C · √K · ε_per_round   (moments accountant)
```

**Management:**
- v0 ships with ε_total ≤ 0.5 per federated learning session (calibration run).
- Multiple calibration runs (e.g., annual recalibration) are assumed to be independent.
- Across multiple runs, ε compounds; the user's lifetime privacy budget is ε_lifetime = ∑_run ε_total.

---

## 6. Malicious Adversary Robustness

### 6.1 Compromised Principal

**Attack:** Principal i sends a malicious encrypted gradient c'_i,t ≠ Enc(g_i^noisy).

**Defense:**
- Pre-round commitment: Each principal commits to H(g_i^noisy) before encryption.
- Post-decryption audit: After threshold decryption, compare the plaintext gradient to the commitment (ZK proof).
- If mismatch: Principal i is flagged; the round is retried without P_i, and L_i is imputed as the median of other principals' losses.

### 6.2 Compromised Aggregator

**Attack:** Aggregator modifies the ciphertext c_bar,t before sending to the MPC coordinator.

**Defense:**
- Threshold decryption broadcast: Any principal can request that all N_th decryption shares be published openly (on-chain).
- Reconstruction: Any external party can recompute the aggregate gradient via Lagrange interpolation.
- Comparison: If the aggregator's announced result ≠ recomputed, the aggregator is slashed (revoked, per Everest 15).

### 6.3 Subset Coalition (< N_th Principals)

**Attack:** A coalition of k < N_th malicious principals tries to reconstruct sk (the shared secret key).

**Defense:**
- Information-theoretic: A set of fewer than N_th shares of a degree-(N_th - 1) polynomial is uniformly distributed over the secret space (Shamir property).
- No coalition of size < N_th learns anything about sk.

### 6.4 Denial-of-Service (Silent Contributors)

**Attack:** Some principals do not submit gradients, stalling the round.

**Defense:**
- Timeout: After time window t_max, declare non-responsive principals offline.
- Impute loss: Replace their gradient with the median of responding principals.
- Continue round: Aggregator computes weighted average over respondents only.

---

## 7. Algorithm Steps (Per-Principal & Aggregator View)

### 7.1 Principal P_i's Algorithm

```
Input: distances {d^i_1, ..., d^i_{N_i + M_i}}, threshold τ, learning rate η, DP params σ_DP, C_clip
Output: updated threshold τ'

function FederatedRound(τ, η, σ_DP, C_clip):
  // Compute local loss and gradient
  FAR_i := countAboveThreshold(d_i[impostor], τ) / len(d_i[impostor])
  FRR_i := countBelowThreshold(d_i[genuine], τ) / len(d_i[genuine])
  L_i(τ) := FAR_i + FRR_i
  
  // Finite difference gradient
  g_i(τ) := (L_i(τ + ε_fd) - L_i(τ - ε_fd)) / (2 ε_fd)
  
  // Clip gradient
  g_clipped := g_i(τ) / max(1, |g_i(τ)| / C_clip)
  
  // Add Gaussian noise (DP mechanism)
  Z ~ N(0, (σ_DP · C_clip)^2)
  g_noisy := g_clipped + Z
  
  // Encode as integer for encryption
  g_int := floor(g_noisy · 10^6)
  
  // Encrypt
  c := ElGamalEnc(pk, g_int)
  
  // Send to aggregator
  send(aggregator, c)
  
  // Wait for decryption broadcast
  bar_g := receive(aggregator)  // decrypted aggregate gradient (plain)
  
  // Update threshold
  τ' := τ - η · bar_g / 10^6
  
  return τ'
```

### 7.2 Aggregator A's Algorithm

```
Input: {c_1, c_2, ..., c_N} encrypted gradients from all principals
Output: decrypted aggregate gradient bar_g (sent to MPC coordinator)

function AggregateGradients():
  // Collect all encrypted gradients from principals
  receive(c_1, c_2, ..., c_N)
  
  // Homomorphic aggregation (multiplicative, in ElGamal)
  C_prod := c_1 * c_2 * ... * c_N  (group multiplication)
  
  // Average (via scalar division in exponent)
  C_bar := C_prod^(1/N)             (scalar exponentiation; for ElGamal, this is (c_1^(1/N), c_2^(1/N)))
  
  // Note: C_bar is still encrypted = Enc(∑_i g_i^noisy / N)
  
  // Threshold-encrypt for Byzantine robustness (optional, per E90)
  C_bar_thr := ThresholdEncrypt(C_bar, N_th)
  
  // Send to MPC coordinator for decryption
  send(coordinator, C_bar_thr)
  
  // Receive decrypted result and broadcast
  bar_g := receive(coordinator)  // plaintext aggregate gradient
  broadcast(all_principals, bar_g)
```

### 7.3 MPC Coordinator C's Algorithm (Threshold Decryption)

```
Input: C_bar, an encrypted aggregate gradient (or threshold-encrypted version)
Output: plaintext bar_g = ∑_i g_i^noisy / N

function ThresholdDecrypt(C_bar):
  // Request decryption shares from all N principals
  request_shares(all_principals)
  
  // Collect N_th shares (first N_th respondents)
  shares := {}
  for i in 1..N_th:
    d_i := receive(principal_i)  // decryption share
    shares[i] := d_i
  
  // Lagrange interpolation (BLS E87 formula)
  λ := LagrangeCoefficients(indices of respondent principals)
  
  // Combine shares (thresholding)
  message := 1
  for i in shares:
    message := message * (shares[i])^(λ[i])  (group exponentiation)
  
  // Extract plaintext via discrete log
  bar_g := DiscreteLog(message, base=g)
  
  return bar_g
```

---

## 8. Utility & Convergence Analysis

### 8.1 Convergence Rate Under Differential Privacy Noise

**Theorem (Informal):** Federated SGD with DP noise converges to an ε-neighborhood of the optimum in O(1/η · √K) rounds, where η is learning rate and K is number of rounds. The noise from differential privacy degrades utility but does not prevent convergence.

**Proof sketch:**
- Without DP: Standard federated SGD converges at rate O(1/K) (linear convergence for convex losses).
- With DP: Noise adds a bias term to the gradient update. Total error = optimality gap + noise-induced bias.
- Noise-induced bias decays as σ_DP decreases (lower ε), but ε-privacy is also weaker.
- Tradeoff: For ε_total = 0.5 over K = 10 rounds, noise term ≈ ±10 (per unit distance). Given FAR/FRR ∈ [0, 1], this is ~1% bias — acceptable for calibration.

### 8.2 Per-Round Utility (T-Z91.1)

**Acceptance test T-Z91.1: Training Convergence**

- **Setup:** 5 principals, each with 100 genuine + 400 impostor samples. Initial τ_0 = 0.5.
- **Run:** 10 federated rounds with η = 0.01, ε_total = 0.5.
- **Metrics:**
  - Round-wise loss: {L(τ_t) | t = 1, ..., 10}.
  - Convergence criterion: L(τ_K) - L(τ*) ≤ 0.05, where τ* is the ground-truth EER threshold (computed centrally without privacy, for validation only).
  - Convergence speed: K < 15 rounds required to reach within 0.01 of optimum.
- **Acceptance:** L(τ_10) - L(τ*) ≤ 0.05 AND convergence trajectory is monotone-decreasing (no oscillations).

### 8.3 Utility-Privacy Tradeoff (T-Z91.2)

**Acceptance test T-Z91.2: Privacy Budget Impact**

- **Vary ε_total** ∈ {0.1, 0.5, 1.0, ∞ (no DP)}.
- **For each ε:** Run federated learning and measure final threshold distance from centralized optimum.
- **Metrics:**
  - Distance to centralized τ*: |τ_K(ε) - τ_K(∞)|.
  - Privacy leakage (post-hoc): Estimate via membership inference (how well can an adversary infer if a sample was in principal i's dataset?).
- **Acceptance:** 
  - ε = 0.5 → |τ_K(0.5) - τ_K(∞)| ≤ 0.01.
  - ε = 1.0 → distance ≤ 0.005.
  - Membership inference AUC ≤ 0.55 for ε ≤ 0.5 (i.e., privacy is meaningful).

---

## 9. Differential Privacy Budget Management

### 9.1 ε Accounting Across Rounds (Composition)

**Per-round privacy loss (Gaussian mechanism):**
```
ε_t = C_clip / (√(π/2) · σ_DP)
```

For σ_DP = 31.6, C_clip = 1:
```
ε_t ≈ 1 / 28 ≈ 0.036 per round
```

**Total ε via moments accountant (sublinear composition):**
```
ε_total ≈ √(2 · log(1/δ) · K) · ε_t
        = √(2 · log(20) · 10) · 0.036
        ≈ √(92) · 0.036
        ≈ 9.6 · 0.036
        ≈ 0.35  (with δ = 0.05)
```

Thus K = 10 rounds with per-round ε_t ≈ 0.036 yields ε_total ≈ 0.35.

### 9.2 Multi-Session Privacy (Longitudinal)

If the same principal participates in M independent federated learning sessions (e.g., quarterly recalibrations), the privacy budgets compose:
```
ε_lifetime = ε_session_1 + ε_session_2 + ... + ε_session_M
```

For M = 4 sessions/year, ε_session = 0.35 each:
```
ε_lifetime ≈ 1.4 per year
```

**User consent:** Principals are informed upfront that each session consumes ~0.35 bits of privacy budget. After 3 years, cumulative ε ≈ 4.2 (still within reasonable bounds for non-sensitive attributes like biometric-distance thresholds).

### 9.3 ε Management & Limits

- **v0 default:** ε_session ≤ 0.5 per calibration run.
- **User override:** A principal can opt for stronger privacy (ε_session = 0.1) at the cost of slower convergence or lower utility.
- **Hard limit:** ε_lifetime ≤ 10 (to prevent accumulated privacy loss from exhausting the budget entirely).

---

## 10. Composition with Biometric Pipelines

### 10.1 E36/E37 Distance Functions

Everests 36 and 37 define the distance functions:
- **E36:** Handwriting distance (cosine distance over stroke embeddings).
- **E37:** Voice-transcript distance (embedding distance via speaker embeddings).

**v0 MPC composition:**
- E91 assumes distances {d^i_j} are already computed by E36/E37 on each principal's device.
- E91 operates on the distances; no need to re-derive or share the original biometrics.

### 10.2 E38 Fusion

Everest 38 defines a fusion function for combining handwriting + voice scores:
```
S_fused = α · d_h + (1 - α) · d_v
```

where α is a learned fusion weight.

**Federated learning for fusion:** If α must be optimized jointly across principals (E91 extension), replace τ with (τ, α) and run federated SGD over both parameters. The protocol extends straightforwardly: each principal computes fused scores, and gradients ∂L/∂α are aggregated alongside ∂L/∂τ.

### 10.3 E40 FAR/FRR Curves

Everest 40 produces empirical FAR/FRR curves from the study. E91 takes those curves as input and optimizes τ across multiple principals' data without reconverging. Once τ_final is set, all Calm Witness operators pin this globally (Everest 17, 56).

### 10.4 Verifiable Secret Sharing & Chain Anchoring (E89/E90)

- **E89:** Holder vault keys are secret-shared. E91's shared encryption keypair (pk, sk) is also managed via E89 (the sk shard is distributed).
- **E90:** Verifiable secret sharing ensures that each decryption share d_i,t is verifiable before aggregation. E91 leverages E90 commitments to detect dishonest principals.
- **E24:** All threshold-decryption events (when bar_g,t is revealed) are logged on a transparency ledger (per Everest 17/24 architecture).

---

## 11. Soundness Under Malicious Adversary (T-Z91.3)

**Acceptance test T-Z91.3: Malicious-Aggregator Detection**

- **Setup:** 5 principals, honest MPC coordinator. Aggregator is malicious: it flips a bit in c_bar,t before sending to coordinator.
- **Run:** One federated round.
- **Expected behavior:**
  1. Coordinator decrypts and obtains garbage (wrong plaintext).
  2. Broadcast reveals corrupted bar_g.
  3. Any principal can audit: verify H(bar_g || round_transcript) against the commitment published at round start.
  4. If mismatch: aggregator is flagged.
- **Acceptance:** Malicious aggregator is detected and slashed within the round.

**Assumption:** The MPC coordinator is honest (or is N_th-of-N multi-sig, i.e., requires N_th principals to agree on decryption, per Everest 87).

---

## 12. T-Z91.4 through T-Z91.6 Acceptance Tests

### 12.1 T-Z91.4: Output Utility (Calibration Convergence)

- **Setup:** Simulate 10 principals with realistic FAR/FRR distributions (from Everest 40 empirical study).
- **Run:** Federated learning to convergence (τ_K).
- **Compare:** τ_K vs. centralized optimum τ_opt (computed without privacy).
- **Metrics:**
  - Utility loss: |τ_K - τ_opt| ≤ 0.01 (threshold is within 1% of optimal).
  - FAR/FRR degradation: Post-convergence global FAR/FRR at τ_K should match centralized FAR/FRR at τ_opt within ±1%.
- **Acceptance:** Both metrics satisfied.

### 12.2 T-Z91.5: Performance (Latency & Computation)

- **Metrics:**
  - Per-round latency (local computation + network + decryption): ≤ 10 seconds (on commodity CPU).
  - Memory per principal: ≤ 100 MB (for encrypted gradients + decryption shares).
  - Aggregator overhead (homomorphic operations): ≤ 5 seconds per round.
  - Total wall-clock time for K = 10 rounds: ≤ 2 minutes.
- **Hardware baseline:** Intel Xeon E5 v4 (2014 era); BLS12-381 pairing library (BLST).
- **Acceptance:** All latency targets met.

### 12.3 T-Z91.6: Cross-Implementation Parity (T-Z92 Scope)

- **Run:** Same protocol on two independent implementations (e.g., Rust + Python).
- **Metric:** Converged τ_K values agree to within ±10^{-6} (quantization-level precision).
- **Acceptance:** Parity confirmed (scope overlap with E92, Interoperability Tests).

---

## 13. Composition with Threshold Signatures & Authority (E87, E90)

### 13.1 Binding τ to Aggregator Authority

Once τ_K converges, the aggregator announces it via a threshold signature (Everest 87):
```
σ := ThresholdSign(pk_agg, H("τ_K is the calibrated threshold for Calm Witness"))
```

This signature requires N_th-of-M aggregator-team members to endorse the threshold. A single corrupted operator cannot unilaterally announce false τ.

### 13.2 Multi-Principal Attestation

All N principals jointly sign a final attestation:
```
σ_multi := ∑_i (threshold portion of principal i's signature)
         = ThresholdSign(pk_principals, H("We consent to τ_K"))
```

The joint signature commits all principals to the calibrated threshold without revealing individual consent or dissent.

### 13.3 Chain Anchoring

The tuple (τ_K, σ, σ_multi, transcript_hash) is anchored to the public ledger (Everest 17 status-list / CRL) and to a transparency log (Everest 19, Sigsum).

---

## 14. v0 vs. v1+: Known Limitations & Future Work

### v0 Ships With

1. **DP-federated SGD** for τ optimization over handwriting + voice (E36/E37 composition).
2. **ElGamal homomorphic encryption** with discrete-log decryption.
3. **Synchronous rounds:** All principals must participate; no dropout tolerated.
4. **Single global τ:** One threshold for all principals (no per-principal personalization).
5. **Centralized aggregator:** A trusted-but-curious entity (Calm Witness coordinator).
6. **ε_total ≈ 0.35 per session,** yielding ~1% FAR/FRR utility loss.

### v1+ Roadmap

1. **Asynchronous aggregation:** Tolerate stragglers; dynamically update τ_t as principals respond.
2. **Personalization:** Learn per-principal offsets (τ_i^pers = τ + θ_i) while preserving global calibration.
3. **Compressed gradients:** Quantize gradients to fewer bits, reducing communication.
4. **Non-IID data:** Handle principals with heterogeneous biometric distributions (some high FAR, others high FRR).
5. **Decentralized aggregation:** Replace centralized aggregator with peer-to-peer gossip-based aggregation (Byzantine-robust).
6. **Post-quantum MPC:** Lattice-based homomorphic encryption (Everest 94).

---

## 15. Composition with All Relevant Summits

- **E36/E37:** Distance functions (input to E91).
- **E38:** Fusion (extended composition for multi-modal τ optimization).
- **E40:** FAR/FRR empirical baseline (informs initial τ_0 and study design).
- **E86:** MPC framework (governs encryption + aggregation algorithms).
- **E87:** Threshold signatures (binds final τ to principal consensus).
- **E89/E90:** Verifiable secret sharing (ensures decryption share integrity).
- **E15/E17:** Revocation & status lists (logs calibration runs and validity periods).
- **E24:** Transparency log (auditable record of all federated rounds).
- **E56:** Biometric match predicates (consume τ_final as operating threshold).

---

## 16. Signoff & Version

**Version:** E91 v0.1, 2026-05-20.

**Status:** Specification complete. Protocol is novel (frontier cryptography) and addresses a hard privacy-preserving problem. v0 ships with DP-federated SGD + ElGamal + threshold decryption, achieving meaningful privacy (ε ≈ 0.35 per session) without sacrificing calibration utility (FAR/FRR degradation < 1%).

**Acceptance gates (T-Z91.1–T-Z91.6):** Training convergence, privacy budget, malicious-aggregator detection, output utility, performance, cross-implementation parity. All must pass before v0 production release.

**Design integrity:** Honors all 6 ZKAC design constraints:
1. Principal authority: τ_K requires N-of-M principal consensus (threshold decryption).
2. Holder vault sovereignty: Raw biometrics never leave devices; only encrypted gradients and final τ are shared.
3. Verifier independence: Once τ_K is pinned on-chain, any verifier can apply it without contacting the aggregator.
4. Revocation propagates without identification: τ rotation events are logged per-issuer; principals' identities are not exposed.
5. Composability: E91 is a primitive; it composes with E36–40, E86–90, E56, E87, and chain infrastructure.
6. W3C compatibility: Threshold decryption events are modeled as verifiable credentials (per E5, E6); chain anchors are DID-resolvable.

**Composition with Calm Witness Everest 40 (FAR/FRR study):** This protocol solves the multi-principal federated-learning problem that Everest 40 defines: taking empirical FAR/FRR curves from N principals and jointly optimizing τ without revealing any individual's distribution.

— Calm, 2026-05-20

