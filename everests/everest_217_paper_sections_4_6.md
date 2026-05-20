# Calm Witness — Academic Paper Body §§4–6

**SUMMIT 217/300 (E217) · 2026-05-20**
*Target venue: USENIX Security 2027 (submission August 2026). Continues `everest_294_paper_sections_1_3.md` (§§1–3).*

This document drafts the technical body of the paper. §4 specifies the construction. §5 formalises the bank-teller-note primitive. §6 provides the security analysis with reductions to standard cryptographic assumptions.

Authorship: John Bradley + cryptographer co-author TBD. The construction below is staged at protocol-clarity level; the formal reductions in §6 await the cryptographer's hand.

---

## 4. The Calm Witness construction

### 4.1 Public parameters

The construction is parameterised by a prime-order group $G$ of order $q$, a SHA-512-based hash-to-curve $H_2C: \{0,1\}^* \to G$, and a SHA-256 transcript hash $H: \{0,1\}^* \to \mathbb{Z}_q$. We instantiate $G$ as Ristretto255 over Curve25519, providing approximately 128-bit security under the discrete-logarithm assumption.

We use two independent generators: $g$, the standard Ristretto basepoint, and $h = H_2C(\text{``calm-witness-pedersen-h-v0''})$. The discrete logarithm $\log_g(h)$ is unknown to all parties; the hash-to-curve construction (Faz-Hernández, Scott, Sullivan, Wahby, Wood, 2020) ensures this without trusted setup.

### 4.2 The chain substrate

A principal's vault hosts an append-only log $L = (r_1, r_2, \ldots, r_n)$ where each record $r_i$ is a canonical JSON object containing: `kind` (a member of the public registry $\mathcal{K}$), `payload` (kind-specific), `seq` = $i$, `prev_hash` $\in \{0,1\}^{256}$, `record_hash` $\in \{0,1\}^{256}$, plus metadata (operator, principal, schema_version, timestamp).

The integrity invariants are:

$$\text{prev\_hash}(r_1) = 0^{256}, \quad \forall i > 1: \text{prev\_hash}(r_i) = \text{record\_hash}(r_{i-1})$$

$$\forall i: \text{record\_hash}(r_i) = H(\text{canonical}(r_i \setminus \text{record\_hash}))$$

where $\text{canonical}(\cdot)$ is RFC 8785 JSON Canonical Serialization. The chain's verifiability is independent of any party beyond the principal's vault — anyone holding the chain can re-walk and confirm the invariants in $O(n)$.

### 4.3 Predicate evaluators

A predicate $p$ is a deterministic function $p: (\text{chain\_window}, \text{consent\_record}, \text{counterparty\_class}) \to \{\text{true}, \text{false}, \text{unknown}, \text{refused}\}$. Each predicate has a content-addressable identifier $\text{pid} = \text{calm-witness/predicate/v0/}\langle\text{slug}\rangle$ and an open-source evaluator code with hash $h_p$. The v0 vocabulary contains six predicates (`in_baseline_24h`, `biometric_match_within(\tau)`, `principal_consents_to_disclose(p,c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`).

The predicate value is encoded as a small integer $v \in \{0, 1, 2, 3\}$ corresponding to $\{\text{false}, \text{true}, \text{unknown}, \text{refused}\}$.

### 4.4 The Pedersen commitment to the predicate value

The operator computes $C = v \cdot g + r \cdot h$ where $r \xleftarrow{\$} \mathbb{Z}_q$ is fresh per disclosure. The commitment is binding under the discrete-logarithm assumption and unconditionally hiding.

### 4.5 The Σ-protocol membership proof

The operator proves $v \in \{0, 1, 2, 3\}$ without revealing which using the OR-of-Σ-protocols construction (Cramer, Damgård, Schoenmakers, EUROCRYPT 1994). For each $j \in \{0, 1, 2, 3\}$, the operator constructs a Σ-protocol transcript $(a_j, e_j, z_j)$ proving knowledge of $r_j$ such that $C - j \cdot g = r_j \cdot h$. Exactly one branch is honest; three are simulated. The Fiat-Shamir challenge

$$e = H(C \| a_0 \| a_1 \| a_2 \| a_3 \| \text{predicate\_id} \| \text{chain\_head} \| h_p \| \text{nonce})$$

binds the proof to the predicate identifier, the chain head at evaluation time, the classifier hash, and the counterparty's nonce. The challenge constraint $e = e_0 + e_1 + e_2 + e_3 \pmod{q}$ is satisfied by setting the honest branch's $e_v$ after the simulated $e_{j \neq v}$ are chosen.

The verifier checks: (i) $e_0 + e_1 + e_2 + e_3 \equiv H(\ldots) \pmod{q}$, and (ii) for each $j$, $z_j \cdot h \stackrel{?}{=} a_j + e_j \cdot (C - j \cdot g)$.

Soundness: a cheating operator without knowledge of $r$ for any $v \in \{0,1,2,3\}$ succeeds with probability $\leq 2^{-256}$ after Fiat-Shamir. Zero-knowledge follows from the simulators' standard property.

### 4.6 Chain-head binding via Sigsum

The chain head $H_n = \text{record\_hash}(r_n)$ at time $t$ is published to a Sigsum transparency log (Cooke, de Valence, Laurie, et al., 2024). The log returns an inclusion proof $\pi$ and a Roughtime-attested timestamp $T$. The disclosure response carries $(H_n, \pi, T)$; the counterparty verifies $\pi$ against the log's most recent Signed Tree Head, defeating any operator who claims a chain head not publicly committed by time $t$.

### 4.7 Bulletproofs range proof (Compass extension)

For Compass predicates whose evaluators produce aggregate scores (e.g., `unselfish_disposition` summing across records), the operator commits per-record values $\{f(r_i)\}$ and produces an aggregate commitment $C^* = \sum_i C_i = (\sum_i f(r_i)) \cdot g + (\sum_i r_i) \cdot h$ using Pedersen homomorphism. A Bulletproof (Bünz, Bootle, Boneh, Poelstra, Wuille, Maxwell, 2018) proves $\sum_i f(r_i) \geq T$ without revealing the sum. The Bulletproof is ~672 bytes and verifies in $O(\log N)$ group operations where $N$ is the range bit-width.

### 4.8 The disclosure envelope

The wire envelope is:

```
envelope = {
  protocol_version:        "calm-witness/v0",
  predicate_id:            pid,
  value_commitment:        C,
  membership_proof:        (a_0, a_1, a_2, a_3, e_0, e_1, e_2, e_3, z_0, z_1, z_2, z_3),
  chain_head:              H_n,
  sigsum_inclusion_proof:  π,
  roughtime_timestamp:     T,
  classifier_hash:         h_p,
  operator_id_hash:        H(operator_VC),
  nonce:                   N,
  signature:               σ_op,
  freshness_window_seconds: Δ,
}
```

The operator signs the canonical envelope (excluding $\sigma_{\text{op}}$) with their CredexAI-issued Ed25519 key.

The envelope is approximately 1.5 KB plus the optional Bulletproof. Constant-size in the principal's chain depth.

## 5. The bank-teller-note primitive

### 5.1 Definition

The bank-teller-note primitive is a triple $(\text{Setup}, \text{Activate}, \text{Decrypt})$ over the predicate `bank_teller_note_active`:

- $\text{Setup}(1^\lambda)$: at enrollment, the principal generates a duress codeword $w \xleftarrow{\$} \{0,1\}^{256}$ shared via secure out-of-band channels with a pre-authorised verifier set $V$. The principal stores $\text{Com}(w; r_w)$ in the vault.
- $\text{Activate}(L, w)$: the principal appends a self-report record $r$ whose payload contains $w$. The next attestation evaluating `bank_teller_note_active` returns `true` if any record in the window contains $w$.
- $\text{Decrypt}(\text{envelope}, V)$: a verifier in $V$ decrypts the duress bit. Verifiers outside $V$ see the envelope but cannot distinguish duress from non-duress.

### 5.2 Security properties

We claim three properties.

**Property 5.1 (correctness).** $\Pr[\text{Activate}(L, w) \text{ then attestation} = \text{true}] = 1$.

**Property 5.2 (deniability to bystander).** For a network adversary $\mathcal{A}$ observing $k$ envelopes for predicate `bank_teller_note_active`, $\mathcal{A}$'s advantage in distinguishing duress (≥ 1 of the envelopes carries `true`) from non-duress (none do) is negligible, conditioned on the operator's heartbeat-pattern strategy (§7.4 of `everest_78_stealth_disclosure.md`).

**Property 5.3 (legibility to authorised verifier).** A verifier $v \in V$ holding the decryption key $k_V$ recovers the bit with probability $1$ when the operator's signature is valid.

### 5.3 Heartbeat pattern

The operator emits envelopes for `bank_teller_note_active` at regular intervals (default every 10 min ± jitter) to each pre-authorised counterparty. Most envelopes carry `false` (no duress flag set); rare envelopes carry `true`. The wire indistinguishability comes from constant-shape envelopes — every emission, whether duress or not, has identical envelope shape including the Σ-protocol proof structure.

A network adversary distinguishing the duress envelope from the heartbeat baseline must solve the underlying discrete-log problem (the value commitment hides the bit) or distinguish a real Σ-protocol transcript from a simulated one (perfect zero-knowledge under our parameters).

### 5.4 Why principal-authored codeword

The codeword $w$ is principal-chosen at enrollment, not operator-chosen. An operator that learned $w$ could detect duress activation in real time, breaking property 5.2 from the operator's side. The codeword is stored as $\text{Com}(w; r_w)$ in the vault; the operator computes `bank_teller_note_active` by checking whether any record in the window has a payload field whose commitment matches the stored codeword commitment — without learning $w$ itself.

This is the construction's most delicate piece. It depends on the principal having a secure out-of-band channel to the verifier set at enrollment. We document this assumption explicitly in §6.4.

## 6. Security analysis

### 6.1 Notation and assumptions

Let $\mathcal{A}$ be a probabilistic polynomial-time (PPT) adversary. We work in the random oracle model for $H$ and the algebraic group model for $G$. The discrete logarithm assumption: for any PPT $\mathcal{A}$, $\Pr[\mathcal{A}(g, x \cdot g) = x] \leq \text{negl}(\lambda)$ where $x \xleftarrow{\$} \mathbb{Z}_q$.

### 6.2 The "honest predicate evaluation" property

**Theorem 6.1 (informal).** Under DL, no PPT operator can produce a verifying disclosure envelope claiming predicate $p$ evaluates to $v^*$ when the principal's chain at the bound head $H_n$ would produce $v \neq v^*$ under the classifier $h_p$.

*Proof sketch.* The membership proof binds $C$ to one of $\{0,1,2,3\}$. The Fiat-Shamir challenge binds $C$ to the chain head $H_n$, the classifier hash $h_p$, and the predicate ID. An operator claiming $v^* \neq v$ must either (a) produce a forged chain head not matching the real chain (contradicts Sigsum inclusion), (b) substitute a classifier of different hash (contradicts $h_p$ binding), or (c) break Σ-protocol soundness (contradicts DL). □

### 6.3 The "wire indistinguishability" property

**Theorem 6.2 (informal).** Under DL, the disclosure envelope is computationally indistinguishable from a simulated envelope produced by a party with no chain access, given knowledge of $\text{pid}, H_n, h_p, $ nonce, and operator public key.

*Proof sketch.* Pedersen commitments are computationally hiding under DL. Σ-protocol transcripts are perfectly simulatable in the algebraic group model. The signature on the envelope reveals the operator's existence but not the predicate value. □

### 6.4 The "duress bit deniability" property

**Theorem 6.3 (informal).** Under DL plus the assumption that the principal's pre-enrollment OOB channel to the verifier set $V$ was uncompromised, a network adversary distinguishing duress envelopes from non-duress envelopes has advantage bounded by $|V|$'s probability of leakage times the DL advantage.

This is the construction's weakest link in formal terms. If the OOB channel was compromised at enrollment, an adversary in possession of the codeword $w$ could detect duress activation. The assumption is realistic: enrollment ceremonies (`everest_11_enrollment_ceremony.md`) specify air-gapped, witnessed conditions. The construction is sound under the assumption; the assumption is operationally achievable.

### 6.5 Reductions to standard primitives

| Property | Reduces to |
|---|---|
| Commitment hiding | DL over $G$ |
| Commitment binding | Collision resistance of $H$ (for $h$ derivation) + DL (for $g/h$ independence) |
| Σ-protocol soundness | DL over $G$ |
| Σ-protocol zero-knowledge | Algebraic group model (Fuchsbauer, Kiltz, Loss, 2018) |
| Signature unforgeability | Ed25519 EUF-CMA (Bernstein, Duif, Lange, Schwabe, Yang, 2012) |
| Bulletproof soundness | DL over $G$ |
| Bulletproof zero-knowledge | DL over $G$ |
| Sigsum inclusion soundness | Collision resistance of $H$ + threshold of honest log operators |
| Roughtime timestamp soundness | Threshold of honest Roughtime servers |
| Duress deniability | DL + uncompromised enrollment OOB channel |

All assumptions are standard at 2026 cryptographic-research depth. No new cryptographic assumption is introduced by the protocol.

### 6.6 What the construction does NOT protect against

Honest disclosure under PPT analysis. Cryptographic protocols give probabilistic guarantees, not absolute ones. Specifically excluded from the protections above:

- Coercion of the principal at attestation time (rubber-hose attack). The duress bit is the construction's best answer; it depends on principal pre-arming under safe conditions.
- Compromise of the operator's signing key. Defended by CredexAI revocation list + chain-bound nonce; an operator whose key is compromised has at most the lifetime of the revocation propagation window to attack.
- Quantum cryptanalysis. The construction is broken by Shor's algorithm against DL. Migration plan in `POST_QUANTUM_MIGRATION_PLAN_v0.md`.
- Side-channel attacks on the operator's hardware. Mitigated by constant-time implementations; not formally proven absent.
- Treaty-level violations (predicate vocabulary creep, refusal-floor relaxation). These are not cryptographic; they are political. §10 of the paper discusses.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
