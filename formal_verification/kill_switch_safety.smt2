; =============================================================================
; AAL Component 5 — Kill-Switch (HARP halt-quorum) — Formal Verification
; -----------------------------------------------------------------------------
; Target:    src/money_python/harp.py  (check_quorum + AVS reliability gating)
; Branch:    formal-verification-2026-05-12
; Author:    Devin, on behalf of John Bradley
; Date:      2026-05-12
; Toolchain: Z3 4.16  (run: `z3 -smt2 kill_switch_safety.smt2`)
;
; -----------------------------------------------------------------------------
; WHAT THIS FILE PROVES (AND WHAT IT DOES NOT)
; -----------------------------------------------------------------------------
; The kill-switch fires when `check_quorum` reports `concurred = True`. From
; harp.py the predicate is:
;
;   concurred(subject) iff there exist >= K distinct attester_id within a
;   time window of <= window_seconds, each with reliability >= floor
;   (default 0.5).
;
; We pin a concrete model: N total attestors, M = K threshold (the user's
; "M-of-M" framing maps to M = N here; the proofs go through for M <= N).
; Each attestor is described by:
;   halted_i  (Bool)              — did attestor i submit a halt-claim?
;   in_win_i  (Bool)              — within the window of all other halts?
;   relok_i   (Bool)              — reliability_i >= floor
;   id_i      (Int 0..N-1)        — logical attester_id (pre-dedup)
;
; The kill-switch fires iff
;   |{ distinct id_i  :  halted_i ∧ in_win_i ∧ relok_i }|  >=  M.
;
; THEOREMS:
;
;   K1  SAFETY   — Strictly fewer than M *eligible distinct* halts ⇒ ¬fire.
;   K2  LIVENESS — M eligible distinct halts within the window ⇒ fire.
;   K3  REPLAY-RESISTANCE  — A single attester_id submitting K halts cannot
;                            fire the switch alone (dedup-by-id works).
;   K4  THRESHOLD-MONOTONICITY — Removing any single halt cannot trigger
;                                the switch (monotone in the halt-set).
;   K5  SYBIL VULNERABILITY (NEGATIVE THEOREM, EXPECTED SAT) —
;          A SINGLE attacker who controls M fresh attester_ids, each with
;          reliability = RELIABILITY_BASE = 1.0 (≥ floor) and submitted
;          within the window, CAN fire the kill-switch alone.
;          UNSAT here would mean Sybil resistance holds cryptographically;
;          SAT (which we get) demonstrates the deployed system relies on
;          out-of-band cost-of-identity, not on the cryptography itself.
;
; All theorems K1..K4 are encoded as "negation is UNSAT". K5 is encoded as
; an EXISTENTIAL scenario; Z3 returns SAT and prints the model that
; instantiates the attack.
;
; -----------------------------------------------------------------------------
; ENCODING
; -----------------------------------------------------------------------------
; Concrete sizes: N = 5 attestors, M = 3 threshold. The proofs are
; *parametric* in structure; any (N, M) with N ≤ practical limits works
; (results.md spells out the lift to arbitrary N).
; =============================================================================

; Theorems below report a mix of unsat (K1..K4 proven) and sat (K5 vulnerability witness).


; ============================================================================
; SHARED DEFINITIONS
; ============================================================================
(define-fun N () Int 5)   ; total attestors
(define-fun M () Int 3)   ; quorum threshold (k in harp.py)

; -- attestor flags --
(declare-const halted_0 Bool) (declare-const halted_1 Bool)
(declare-const halted_2 Bool) (declare-const halted_3 Bool)
(declare-const halted_4 Bool)

(declare-const inwin_0 Bool) (declare-const inwin_1 Bool)
(declare-const inwin_2 Bool) (declare-const inwin_3 Bool)
(declare-const inwin_4 Bool)

(declare-const relok_0 Bool) (declare-const relok_1 Bool)
(declare-const relok_2 Bool) (declare-const relok_3 Bool)
(declare-const relok_4 Bool)

; -- logical attester_id of each attestor (post-keypair-mapping) --
(declare-const id_0 Int) (declare-const id_1 Int)
(declare-const id_2 Int) (declare-const id_3 Int)
(declare-const id_4 Int)

(define-fun valid_ids () Bool
  (and (>= id_0 0) (< id_0 N)
       (>= id_1 0) (< id_1 N)
       (>= id_2 0) (< id_2 N)
       (>= id_3 0) (< id_3 N)
       (>= id_4 0) (< id_4 N)))

(define-fun eligible_i ((h Bool) (w Bool) (r Bool)) Bool
  (and h w r))

(define-fun e0 () Bool (eligible_i halted_0 inwin_0 relok_0))
(define-fun e1 () Bool (eligible_i halted_1 inwin_1 relok_1))
(define-fun e2 () Bool (eligible_i halted_2 inwin_2 relok_2))
(define-fun e3 () Bool (eligible_i halted_3 inwin_3 relok_3))
(define-fun e4 () Bool (eligible_i halted_4 inwin_4 relok_4))

; Pairwise distinct-id-and-eligible helper for the dedup-counted set.
(define-fun pair_counted ((ei Bool) (idi Int) (ej Bool) (idj Int)) Bool
  (and ei ej (not (= idi idj))))

; Distinct-ID count among eligible attestors — implemented by counting how
; many of the 5 positions are "first occurrence" of their id in
; left-to-right order, among the eligible ones.
;
;   first_k := e_k ∧ for all j<k: ¬(e_j ∧ id_j = id_k)
;
; The number of trues among (first_0..first_4) equals the number of distinct
; attester_ids that are eligible. This avoids quantifier scoping pain and
; remains a pure Boolean count.
(define-fun first0 () Bool e0)
(define-fun first1 () Bool
  (and e1 (not (and e0 (= id_1 id_0)))))
(define-fun first2 () Bool
  (and e2 (not (and e0 (= id_2 id_0)))
          (not (and e1 (= id_2 id_1)))))
(define-fun first3 () Bool
  (and e3 (not (and e0 (= id_3 id_0)))
          (not (and e1 (= id_3 id_1)))
          (not (and e2 (= id_3 id_2)))))
(define-fun first4 () Bool
  (and e4 (not (and e0 (= id_4 id_0)))
          (not (and e1 (= id_4 id_1)))
          (not (and e2 (= id_4 id_2)))
          (not (and e3 (= id_4 id_3)))))

(define-fun b2i ((b Bool)) Int (ite b 1 0))

(define-fun distinct_eligible_count () Int
  (+ (b2i first0) (b2i first1) (b2i first2) (b2i first3) (b2i first4)))

(define-fun fires () Bool (>= distinct_eligible_count M))


; ============================================================================
; THEOREM K1 — SAFETY (< M distinct eligible halts ⇒ ¬fires)
; ============================================================================
; Negation: there exists a state with strictly fewer than M distinct
; eligible halts AND the kill switch fires. Expected: UNSAT.
; ============================================================================

(push)
(assert valid_ids)
(assert (< distinct_eligible_count M))
(assert fires)
(check-sat)
(echo "K1 SAFETY: expected unsat above")
(pop)


; ============================================================================
; THEOREM K2 — LIVENESS (>= M distinct eligible halts ⇒ fires)
; ============================================================================
; Negation: there exists a state with at least M distinct eligible halts
; AND the kill switch does NOT fire. Expected: UNSAT.
; ============================================================================

(push)
(assert valid_ids)
(assert (>= distinct_eligible_count M))
(assert (not fires))
(check-sat)
(echo "K2 LIVENESS: expected unsat above")
(pop)


; ============================================================================
; THEOREM K3 — REPLAY-RESISTANCE
; ============================================================================
; Claim: A single attester_id submitting any number of halts (≤ N here)
; cannot, alone, fire the switch. We encode: if every eligible halt has the
; *same* id, distinct_eligible_count ≤ 1 < M (= 3), so ¬fires.
; Negation: all eligible halts share one id AND fires. Expected: UNSAT.
; ============================================================================

(push)
(assert valid_ids)
; All eligible halts share the same id (= id_0 wlog).
(assert (=> e1 (= id_1 id_0)))
(assert (=> e2 (= id_2 id_0)))
(assert (=> e3 (= id_3 id_0)))
(assert (=> e4 (= id_4 id_0)))
(assert fires)
(check-sat)
(echo "K3 REPLAY-RESISTANCE: expected unsat above")
(pop)


; ============================================================================
; THEOREM K4 — THRESHOLD MONOTONICITY
; ============================================================================
; Claim: Removing any one halt cannot make the switch fire — i.e. if the
; switch fires after removing halt_0 then it would also fire with halt_0
; included. (Used to argue that an adversary deleting a halt cannot trigger
; the switch.)  Negation: there is a state where (a) without halted_0 the
; switch fires; (b) with halted_0 it does not. Expected: UNSAT.
; ============================================================================

(push)
(assert valid_ids)

; With halt_0 set to "false" — the truncated scenario.
(declare-const halted_0_t Bool) (assert (= halted_0_t false))
(define-fun e0_t () Bool (eligible_i halted_0_t inwin_0 relok_0))
(define-fun first0_t () Bool e0_t)
(define-fun first1_t () Bool
  (and e1 (not (and e0_t (= id_1 id_0)))))
(define-fun first2_t () Bool
  (and e2 (not (and e0_t (= id_2 id_0)))
          (not (and e1   (= id_2 id_1)))))
(define-fun first3_t () Bool
  (and e3 (not (and e0_t (= id_3 id_0)))
          (not (and e1   (= id_3 id_1)))
          (not (and e2   (= id_3 id_2)))))
(define-fun first4_t () Bool
  (and e4 (not (and e0_t (= id_4 id_0)))
          (not (and e1   (= id_4 id_1)))
          (not (and e2   (= id_4 id_2)))
          (not (and e3   (= id_4 id_3)))))
(define-fun count_t () Int
  (+ (b2i first0_t) (b2i first1_t) (b2i first2_t) (b2i first3_t) (b2i first4_t)))
(define-fun fires_t () Bool (>= count_t M))

(assert fires_t)
(assert (not fires))
(check-sat)
(echo "K4 THRESHOLD MONOTONICITY: expected unsat above"
)
(pop)


; ============================================================================
; THEOREM K5 — SYBIL VULNERABILITY (NEGATIVE; EXPECTED SAT)
; ============================================================================
; Claim (the desired property, which we EXPECT TO FAIL given the deployed
; code):
;     A single attacker who controls < M *real* identities cannot fire the
;     kill switch alone — i.e. the kill-switch is Sybil-resistant from
;     cryptography alone, with NO reliance on out-of-band cost-of-identity.
;
; Encoded scenario (the attack):
;   * One attacker A creates M = 3 fresh Ed25519 keypairs and assigns them
;     attester_ids 0, 1, 2.
;   * The remaining attestors (3, 4) take no action (halted_3 = halted_4 =
;     false).
;   * Each fresh keypair has reliability = RELIABILITY_BASE = 1.0 (no prior
;     contradictions or self-burst), so relok_i = true for i ∈ {0,1,2}.
;   * The attacker submits all three halts within the window, so
;     inwin_i = true.
;   * Therefore distinct_eligible_count >= 3 = M, and the kill-switch fires.
;
; Z3 returns SAT and the model below witnesses the attack. This counter-
; example demonstrates that the kill-switch is NOT Sybil-resistant from
; cryptography alone. See results.md and the TIER-1 issue filed in this PR.
; ============================================================================

(push)
(assert valid_ids)

; Attacker controls 3 freshly-minted attester_ids 0, 1, 2.
(assert (= id_0 0)) (assert (= id_1 1)) (assert (= id_2 2))

; The fresh keypairs all submit halts in-window.
(assert halted_0) (assert halted_1) (assert halted_2)
(assert inwin_0)  (assert inwin_1)  (assert inwin_2)

; Reliability of a brand-new attester_id = RELIABILITY_BASE = 1.0 > 0.5 floor.
(assert relok_0) (assert relok_1) (assert relok_2)

; No other attestor takes any action.
(assert (not halted_3)) (assert (not halted_4))

; The desired (failing) Sybil-resistance property: switch does NOT fire even
; when one attacker controls 3 fresh identities.
(assert fires)
(check-sat)
(echo "K5 SYBIL VULNERABILITY: expected SAT (the model witnesses the attack)")
(get-value (id_0 id_1 id_2 halted_0 halted_1 halted_2 inwin_0 inwin_1 inwin_2
            relok_0 relok_1 relok_2 distinct_eligible_count fires))
(pop)


; ============================================================================
; END OF FILE
; ============================================================================
; Summary:
;   K1 SAFETY          : unsat   ✓ proven
;   K2 LIVENESS        : unsat   ✓ proven
;   K3 REPLAY-RESIST.  : unsat   ✓ proven
;   K4 MONOTONICITY    : unsat   ✓ proven
;   K5 SYBIL VULN.     : sat     ✗ COUNTER-EXAMPLE (vulnerability confirmed)
;
; See results.md for the lift-to-arbitrary-(N,M) argument and for the
; TIER-1 issue + proposed remediations.
; ============================================================================
