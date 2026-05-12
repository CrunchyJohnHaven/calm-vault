; =============================================================================
; Bradley-Gavini Equality Proof — Formal Verification (Z3 / SMT-LIB2)
; -----------------------------------------------------------------------------
; Target:    calm_pact/protocol.py  (branch formal-verification-2026-05-12)
; Author:    Devin, on behalf of John Bradley
; Date:      2026-05-12
; Toolchain: Z3 4.16  (run: `z3 -smt2 protocol_equality_proof.smt2`)
;
; -----------------------------------------------------------------------------
; WHAT THIS FILE PROVES
; -----------------------------------------------------------------------------
; The Bradley-Gavini equality proof (calm_pact/protocol.py) is a Schnorr-Σ
; proof of knowledge of delta_r := r_A - r_B such that
;   C_A / C_B  =  H^delta_r   (mod P)
; made non-interactive via Fiat-Shamir.
;
;   Prover :  k ←$ Z_q ;  a = H^k.
;   Verifier:  c = SHA256(G,H,C_A,C_B,a)  (Fiat-Shamir).
;   Prover :  z = k + c · delta_r   (mod q).
;   Verifier accepts iff  H^z  =  a · (C_A / C_B)^c   (mod P).
;
; SMT cannot reason about computational hardness (DLP, DDH) — those are
; *assumptions*, not theorems. SMT *can* discharge the algebraic identities
; in the exponent ring Z_q. Those identities are the substantive content of
; the standard textbook completeness / special-soundness / HVZK / binding
; proofs for Schnorr-Σ + Pedersen.
;
; THM-1 Completeness — honest prover convinces honest verifier.
; THM-2 Special soundness (2-transcript extractor) — extracts delta_r.
; THM-3 Verifier-equation uniqueness in z — bounds adversary success to 1/q.
; THM-4 HVZK simulator existence — simulator transcripts satisfy verifier.
; THM-5 Pedersen binding reduction — two distinct openings ⇒ break DLP(H/G).
;
; All five are encoded as "negation of the theorem is UNSAT".
;
; -----------------------------------------------------------------------------
; ENCODING
; -----------------------------------------------------------------------------
; Z3's QF_NIA fragment is undecidable; BIT-VECTORS are decidable and complete.
; We use bit-width W = 10 and prime Q = 23 — large enough that all
; intermediate sums and products stay strictly below 2^W (no overflow):
;   (Q-1)^2 = 484 < 2^10 = 1024, and 2(Q-1) = 44 < 2^10.
; Bit-vector arithmetic then faithfully represents arithmetic over Z, which
; we reduce mod Q via `bvurem`.
;
; Every property is a STRUCTURAL fact about Z_q (a field of prime order) —
; nothing depends on the specific Q. The same SMT script discharges with any
; small prime Q for which intermediate values stay below 2^W; for the
; production prime Q = (P-1)/2 with P the RFC 3526 group-14 prime, the same
; algebraic identities hold by the same arguments, but a finite SMT check
; requires a finite Q. (See results.md for the lift-to-arbitrary-prime
; argument.)
;
; * Group elements are represented by their discrete logs (exponents) in
;   Z_q under base H. This is faithful because H generates the prime-order
;   subgroup. For elements involving G we introduce an unknown bv constant
;   `dlog_H_G` representing log_H(G).
; * Modular subtraction is implemented as  msub(a, b) = (a + Q - b) mod Q,
;   which avoids the wrap-around-mod-2^W bug of raw `bvsub`.
; =============================================================================

(set-info :status unsat)


; ============================================================================
; SHARED DEFINITIONS — safe modular arithmetic in Z_Q over BV16
; ============================================================================
(define-fun Q    () (_ BitVec 10) (_ bv23 10))
(define-fun ZERO () (_ BitVec 10) (_ bv0  10))
(define-fun ONE  () (_ BitVec 10) (_ bv1  10))

(define-fun zmod ((x (_ BitVec 10))) (_ BitVec 10) (bvurem x Q))

(define-fun in_field ((x (_ BitVec 10))) Bool (bvult x Q))

; Safe modular ops — inputs MUST already be in_field (< Q).
;   madd(a,b) ≤ 2(Q-1) = 44      < 2^10
;   mmul(a,b) ≤ (Q-1)^2 = 484    < 2^10
;   msub(a,b) ≤ a + Q ≤ 2Q-1 = 45 < 2^10   (avoids underflow of bvsub)
(define-fun madd ((a (_ BitVec 10)) (b (_ BitVec 10))) (_ BitVec 10)
  (zmod (bvadd a b)))

(define-fun mmul ((a (_ BitVec 10)) (b (_ BitVec 10))) (_ BitVec 10)
  (zmod (bvmul a b)))

(define-fun msub ((a (_ BitVec 10)) (b (_ BitVec 10))) (_ BitVec 10)
  (zmod (bvadd a (bvsub Q b))))

(define-fun mcong ((a (_ BitVec 10)) (b (_ BitVec 10))) Bool
  (= (zmod a) (zmod b)))


; ============================================================================
; THEOREM 1 — COMPLETENESS
; ============================================================================
; Claim: For every honest prover whose two commitments hide the *same* maxim
; scalar (s_A = s_B), the verifier accepts.
;
; In the exponent under base H:
;   C_A_exp = s_A · log_H(G) + r_A          (mod q)
;   C_B_exp = s_B · log_H(G) + r_B          (mod q)
;   Q_exp   = C_A_exp - C_B_exp = (s_A - s_B)·log_H(G) + (r_A - r_B)
;
; If s_A = s_B then Q_exp ≡ r_A - r_B ≡ delta_r (mod q). The prover sets
; z = k + c · delta_r (mod q); the verifier checks z ≡ k + Q_exp · c (mod q).
; Substituting Q_exp = delta_r gives equality.
;
; Z3 attempts to find a counter-example with s_A = s_B but verifier rejects.
; Expected: UNSAT.
; ============================================================================

(push)

(declare-const sA       (_ BitVec 10))
(declare-const sB       (_ BitVec 10))
(declare-const rA       (_ BitVec 10))
(declare-const rB       (_ BitVec 10))
(declare-const k        (_ BitVec 10))
(declare-const c        (_ BitVec 10))
(declare-const dlog_H_G (_ BitVec 10))

(assert (in_field sA)) (assert (in_field sB))
(assert (in_field rA)) (assert (in_field rB))
(assert (in_field k))  (assert (in_field c))
(assert (in_field dlog_H_G))

; HONEST CASE: scalars equal.
(assert (= sA sB))

; Commitment exponents (under base H).
(define-fun CA_exp () (_ BitVec 10) (madd (mmul sA dlog_H_G) rA))
(define-fun CB_exp () (_ BitVec 10) (madd (mmul sB dlog_H_G) rB))

; Quotient exponent.
(define-fun Q_exp () (_ BitVec 10) (msub CA_exp CB_exp))

; delta_r the honest prover knows.
(define-fun delta_r () (_ BitVec 10) (msub rA rB))

; Honest response.
(define-fun z_honest () (_ BitVec 10) (madd k (mmul c delta_r)))

; Verifier equation in the exponent: z ≡ k + Q_exp · c   (mod Q).
(define-fun verifier_rhs () (_ BitVec 10) (madd k (mmul c Q_exp)))

; Negation: look for a counter-example.
(assert (not (mcong z_honest verifier_rhs)))

(check-sat)
(echo "THM-1 COMPLETENESS: expected unsat above")
(pop)


; ============================================================================
; THEOREM 2 — SPECIAL SOUNDNESS (KEY IDENTITY)
; ============================================================================
; Claim: Two accepting transcripts (a, c1, z1) and (a, c2, z2) sharing the
; same first move `a`, both from a prover using witness delta_r, satisfy
;
;   (z1 - z2)  ≡  (c1 - c2) · delta_r    (mod Q).
;
; Proof of full special soundness then follows by a META argument: since Q
; is prime, Z_Q is a field, so whenever c1 ≢ c2 (mod Q) the difference
; (c1 - c2) has a unique multiplicative inverse, and the extractor outputs
;
;   delta_r_extracted  :=  (z1 - z2) · (c1 - c2)^(-1)   (mod Q).
;
; SMT cannot search for the inverse efficiently (modular inverse over
; bit-vectors is nonlinear), so we split the proof: SMT discharges the
; algebraic identity below, and the "Z_Q is a field" step is documented in
; results.md as a one-line meta-lemma. Expected: UNSAT.
; ============================================================================

(push)

(declare-const k_s   (_ BitVec 10))
(declare-const dr_s  (_ BitVec 10))
(declare-const c1    (_ BitVec 10))
(declare-const c2    (_ BitVec 10))

(assert (in_field k_s))  (assert (in_field dr_s))
(assert (in_field c1))   (assert (in_field c2))

; Honest-protocol responses (the two transcripts the extractor sees).
(define-fun z1 () (_ BitVec 10) (madd k_s (mmul c1 dr_s)))
(define-fun z2 () (_ BitVec 10) (madd k_s (mmul c2 dr_s)))

; The key special-soundness identity:  z1 - z2 ≡ (c1 - c2) · delta_r (mod Q).
(assert (not (mcong (msub z1 z2)
                    (mmul (msub c1 c2) dr_s))))

(check-sat)
(echo "THM-2 SPECIAL SOUNDNESS IDENTITY: expected unsat above")
(pop)


; ============================================================================
; THEOREM 3 — VERIFIER-EQUATION UNIQUENESS IN z (1/q FORGERY BOUND)
; ============================================================================
; Claim: For any fixed (a, c, Q_exp), there is a UNIQUE z in Z_Q satisfying
; the verifier's equation z ≡ a + Q_exp · c (mod Q). So an adversary who
; has committed to `a` *before* learning the (Fiat-Shamir or random)
; challenge c can satisfy the verifier for that c with probability 1/Q.
;
; We verify uniqueness: z1 and z2 both accept against the SAME (a, c) ⇒
; z1 ≡ z2 (mod Q). Expected: UNSAT.
; ============================================================================

(push)

(declare-const a_exp (_ BitVec 10))
(declare-const Qe    (_ BitVec 10))
(declare-const ch    (_ BitVec 10))
(declare-const z1_   (_ BitVec 10))
(declare-const z2_   (_ BitVec 10))

(assert (in_field a_exp)) (assert (in_field Qe)) (assert (in_field ch))
(assert (in_field z1_))   (assert (in_field z2_))

(assert (mcong z1_ (madd a_exp (mmul Qe ch))))
(assert (mcong z2_ (madd a_exp (mmul Qe ch))))
(assert (not (= z1_ z2_)))

(check-sat)
(echo "THM-3 VERIFIER UNIQUENESS IN z: expected unsat above")
(pop)


; ============================================================================
; THEOREM 4 — HVZK SIMULATOR EXISTENCE
; ============================================================================
; Claim: For every challenge c and quotient exponent Q_exp, the simulator
; that picks z ←$ Z_q and sets a := z - Q_exp · c (in the exponent — i.e.
; H^z · (Q^(-c)) in the group) produces a transcript (a, c, z) accepted
; by the verifier. This is the standard HVZK simulator.
;
; We verify the algebraic identity. The distributional indistinguishability
; (perfect HVZK over uniform-random z) is OUTSIDE SMT and documented in
; results.md. Expected: UNSAT.
; ============================================================================

(push)

(declare-const z_sim   (_ BitVec 10))
(declare-const c_sim   (_ BitVec 10))
(declare-const Qe_sim  (_ BitVec 10))

(assert (in_field z_sim))
(assert (in_field c_sim))
(assert (in_field Qe_sim))

(define-fun a_sim () (_ BitVec 10) (msub z_sim (mmul Qe_sim c_sim)))

(assert (not (mcong z_sim (madd a_sim (mmul Qe_sim c_sim)))))

(check-sat)
(echo "THM-4 HVZK SIMULATOR: expected unsat above")
(pop)


; ============================================================================
; THEOREM 5 — PEDERSEN BINDING IDENTITY
; ============================================================================
; Claim: If an adversary opens the same Pedersen commitment C to distinct
; pairs (s, r) and (s', r'), the relation between (s, s', r, r') and
; log_G(H) is FORCED:
;
;   G^s · H^r  =  G^s' · H^r'    (in the prime-order subgroup)
; ⇒ s + log_G(H) · r  ≡  s' + log_G(H) · r'   (mod Q)
; ⇒ (s - s')  ≡  log_G(H) · (r' - r)   (mod Q).
;
; Proof of the full binding reduction follows by the same meta argument as
; THM-2: since Q is prime and r ≠ r' (which is forced when s ≠ s' and the
; commitments are equal), (r' - r) is invertible in Z_Q* and the reduction
; outputs  log_G(H) := (s - s') · (r' - r)^(-1) (mod Q). SMT discharges
; the algebraic identity. Expected: UNSAT.
; ============================================================================

(push)

(declare-const s     (_ BitVec 10))
(declare-const sp    (_ BitVec 10))
(declare-const r     (_ BitVec 10))
(declare-const rp    (_ BitVec 10))
(declare-const dlGH  (_ BitVec 10))

(assert (in_field s))    (assert (in_field sp))
(assert (in_field r))    (assert (in_field rp))
(assert (in_field dlGH))

(assert (not (= s sp)))                              ; distinct scalars
(assert (mcong (madd s  (mmul dlGH r))
               (madd sp (mmul dlGH rp))))            ; same commitment

; Theorem: the binding identity (s - s') ≡ dlGH · (r' - r)  (mod Q) holds.
(assert (not (mcong (msub s sp)
                    (mmul dlGH (msub rp r)))))

(check-sat)
(echo "THM-5 BINDING IDENTITY: expected unsat above")
(pop)


; ============================================================================
; END OF FILE
; ============================================================================
; All five theorems expected: unsat.
;
; Cryptographic-assumption boundary (NOT verified by SMT, documented in
; results.md):
;   * DLP in the (G, H) Schnorr subgroup is hard.
;   * SHA-256 acts as a random oracle (Fiat-Shamir transform soundness).
;   * H was derived via NUMS — log_G(H) is genuinely unknown.
; ============================================================================
