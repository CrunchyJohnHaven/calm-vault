# Everest 280 — Adversarial Alignment Fitting Defense

**The route map's biggest open research problem made tractable. v0 layered defense + the hidden-tolerance commit-reveal mechanism.**

Companion to [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), Phase XVII.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 1. The threat

The ZKAC alignment primitive (Everest 130) asks: do the principal's values align within tolerance τ of the counterparty's values? It returns a single bit.

**The adversarial-fitting attack**: a principal P with knowledge of the counterparty C's published tolerance vector τ crafts their values self-reports to maximize alignment. The self-reports are principal-authored, so the chain accepts them. The proof verifies under τ. The counterparty is deceived.

This is the v0 alignment primitive's deepest weakness. Without a defense, ZKAC degenerates into a sophisticated marketing channel — principals optimize themselves for whichever counterparty's τ they want to match.

## 2. Why this is hard

Three properties make adversarial fitting hard to prevent:

1. **The chain is principal-authored.** Values self-reports are signed by the principal. The cryptographic stack cannot distinguish "values P actually holds" from "values P claims to hold."
2. **τ is typically public.** Counterparties publish their tolerance to attract aligned principals. If τ is secret, the matching market doesn't function.
3. **Self-narration is the protocol's foundation.** The whole architecture is built on the premise that the principal is the world's best authority on their own state. Adversarial fitting weaponizes that premise.

## 3. The v0 layered defense

Six defenses compose, each partial but together forming a meaningful barrier. None of them alone is sufficient.

### 3.1 Defense A — Chain-temporal binding

**Mechanism.** Values self-reports are timestamped and hash-chained (Everest 28). The chain head is anchored in Sigsum (Everest 30) with public witness cosignatures. **A principal cannot rewrite the past.**

**What it defends.** P cannot author a values report dated *before* C published τ. The fitting attack reduces to: "P can only fit *future* records."

**What it does not defend.** P can still fit records authored *after* learning τ.

### 3.2 Defense B — Drift-rate cap (Everest 111)

**Mechanism.** Per-dimension drift rate is bounded. A dimension cannot legitimately move by more than X per month (X is per-dimension; e.g., `non_harm` may drift by 5%/month, `cooperation` by 10%/month). The chain verifier (Everest 28) plus a new drift validator (Everest 111) catches values reports that drift faster than the cap.

**What it defends.** P cannot suddenly change `non_harm` from 0.4 to 0.9 in one report — the drift rate would trigger a flag. Counterparty predicates can refuse proofs where any dimension has exceeded the cap in the window.

**What it does not defend.** Slow-poison attacks (E271) — P drifts values over months. Still hard to detect but at least slow.

### 3.3 Defense C — Witness attestation (Everest 120)

**Mechanism.** Third-party principals attest to a principal's values via signed records (`kind: "values_witness_attestation"`). The aggregator weights both self-report and witness, and surfaces gaps (Everest 121).

**What it defends.** A principal who fits self-reports but lacks corroborating witness attestation produces a low confidence score. Counterparties can demand `witness_attestation_count >= N` as part of the predicate.

**What it does not defend.** Collusive sybils. P recruits friends to attest favorably. Defense D addresses this.

### 3.4 Defense D — Sybil resistance via personhood (Everest 212)

**Mechanism.** Witness attestations only count from principals with valid CredexAI VC (Everest 11) AND chain age >= 6 months. Sybils are filtered.

**What it defends.** Cheap sybils. Old, established principals are required for witness attestation to count.

**What it does not defend.** Determined adversaries with social capital. P with 6 long-established friends colluding still passes.

### 3.5 Defense E — Action-history integration (Everest 109)

**Mechanism.** The Values from Action layer infers values from observed action records (cooperation_record, harm_report, cross_difference_record), not just self-reports. Self-report and action-inferred values are compared; gaps surface.

**What it defends.** P can fit self-reports but cannot fabricate actions. (Actions involve counterparties who can corroborate.) The predicate evaluator weights action-inferred values more heavily than self-report when assessing alignment.

**What it does not defend.** Adversaries with thin action histories pass with only self-report. (Bootstrap problem for new principals.)

### 3.6 Defense F — Hidden-tolerance commit-reveal (this Everest's novel contribution)

**Mechanism.** Counterparty C does NOT publish τ. Instead:

1. C generates τ.
2. C Pedersen-commits to τ: `T = Com(τ; r_C)`.
3. C publishes `T` to a registry (or sends it to P at session start).
4. P generates values self-reports without knowing τ. (Or P uses pre-existing self-reports.)
5. P commits to their values vector: `P_vec_commit = Com(v_P; r_P)`.
6. Session begins; both commitments are now on the chain.
7. C reveals τ (with `r_C` so `T` opens correctly).
8. P verifies `T = Com(τ; r_C)`.
9. P produces alignment proof under the revealed τ.

The binding is in the ordering: C committed to τ *before* P committed to v_P. P cannot retroactively rewrite the chain (Sigsum prevents it). So even if P could fit v_P to τ AFTER step 7, the chain timestamp shows P's commitments preceded the reveal.

**What it defends.** Forward-fitting. P cannot tune values to τ because P doesn't know τ until both commitments are anchored.

**What it does not defend.** Backward-fitting via pre-positioned chain records. P can curate self-reports proactively to maximize alignment with *common* τ vectors. (See §5.)

## 4. Reference protocol — Hidden Tolerance Commit-Reveal (HTCR)

```
SESSION SETUP
  C   →  generate τ ∈ [0, SCALE]^10
  C   →  r_C ← random scalar
  C   →  T ← Com_per_dim(τ; r_C)        # 10-dimension Pedersen commitments
  C → V →  publish T on chain as kind:"alignment_tolerance_commitment"
                                           with metadata: counterparty_id, session_nonce
  V → P →  notify P of pending session with T
  P   →  load v_P from vault (NO knowledge of τ)
  P   →  r_P ← random scalar
  P   →  P_vec_commit ← Com_per_dim(v_P; r_P)
  P → V →  publish P_vec_commit on chain as kind:"alignment_principal_commitment"
                                           with metadata: session_nonce, T's record_hash

ALIGNMENT PROOF
  C   →  send to P: (τ, r_C)
  P   →  verify T = Com_per_dim(τ; r_C)
                if fail: abort session, write kind:"session_abort" to chain
  P   →  compute aligned(v_P, C_vec_imputed, τ) where C_vec_imputed is the
        ideal vector against which P is measured. (Often C_vec = mid-point
        of τ-acceptable region; or C's published "ideal vector". V0 default:
        the ideal vector is published alongside τ commit but committed too.)
  P   →  if aligned: produce AlignmentProof (Everest 128) binding to
        the session_nonce + T's record_hash as the proof context
  P → C →  AlignmentProof + chain head + operator sig

VERIFICATION
  C   →  re-derive expected context from session_nonce + T's record_hash
  C   →  verify_aligned(proof, τ, C_vec, context)
  C   →  check chain head ordering: T's seq < P_vec_commit's seq
        (so T was committed BEFORE P_vec_commit)
  C   →  check chain head consistency: both commitments are in the chain
        verified by the chain verifier (Everest 28)
  C   →  if all pass: act on bit
```

The novel binding is **step "verify chain head ordering"**. Adversarial fitting requires P to publish their commitments *after* learning τ. The chain-temporal ordering check refuses such proofs.

## 5. The residual attack: pre-positioned values

HTCR defends against on-line fitting. The remaining attack vector is **pre-positioned values**: P anticipates the kinds of τ they'll be asked about and curates self-reports in advance.

**Why this is harder to defend.** Pre-positioning is the boundary case between "honest values disclosure" and "manipulation." If a principal honestly *aspires* to certain values and writes self-reports reflecting that aspiration, are they fitting? Probably not. If a principal writes self-reports they don't actually live by, they are. The chain can't always tell the difference.

**v0 partial defense:**
1. **Action-history weighting (Defense E)** — pre-positioned self-reports without matching action records get downweighted. Predicates require a minimum action-record ratio.
2. **Drift-rate observation** — pre-positioning shows up as an unusually flat values trajectory (no drift over time). Counterparties can demand `drift_observed_over(window) > threshold` as a freshness check.
3. **Witness attestation requirement** — pre-positioning is hard to fake when third parties have to corroborate.

**Open research direction (this Everest's residual question).** Can the protocol distinguish pre-positioned values from genuine values via:
- Trajectory analysis (entropy of dimension changes over time)?
- Cross-prediction (do other principals' attestations track the self-reports)?
- Behavioral economics signals (chained costly action when no counterparty is watching)?

These belong to Everest 302 (Reserved for Distinguishability Defense).

## 6. Composition with Calm Witness + Calm Pact

The HTCR protocol composes with Calm Witness state attestation (Everest 144) and Calm Pact directive equality (Everest 143). In a joint session:

1. Pact: agents prove categorical directive equality
2. Witness: principal proves state (in_baseline_24h + no duress)
3. ZKAC-HTCR: alignment proof with hidden tolerance

All three bind to the same chain head and the same session nonce. A counterparty rejects any subset's failure.

## 7. Implementation status

Reference implementation: `~/CredexAI/calm_witness/alignment_htcr.py` (Everest 280 acceptance code, ships with this doc).

Tests: `~/CredexAI/calm_witness/test_alignment_htcr.py`.

## 8. What this Everest is NOT

- Not a complete defense. Distinguishability (E302) and adversarial-trajectory analysis (open research) remain.
- Not a substitute for human judgment. Counterparties act on the alignment bit; they remain responsible for what they do with it.
- Not a guarantee. With sufficient time, witnesses, and acting capital, a determined adversary can pass HTCR. The protocol raises the cost; it does not zero it.

---

**Authored by Calm, 2026-05-20.**
