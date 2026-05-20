# Everest 56 — `biometric_match_within(τ)` Predicate

*Phase V — Predicate Authoring. Prereq: Everests 45 (ZK Range Proof), 51 (Predicate Language v0), 56 sits at the canonical biometric predicate slot.*

---

## What this summit ships

The canonical specification of the v0 `biometric_match_within(τ_h, τ_v)` predicate that Everest 6 introduces and Everest 65's `range_proof` kernel implements. This summit fixes the predicate's semantics, parameters, ID stability rules, reference truth-table evaluator, and golden test corpus.

Why a dedicated summit for one predicate: `biometric_match_within` is the **primary biometric-state bit** in the v0 vocabulary. It is what counterparties most often request. It is what directly translates the biometric pipeline (Everests 36-50) into the disclosure protocol (Everests 66-80). Specifying it precisely is what lets Everests 53 (Predicate ID Registry), 65 (ZK proof generator), and 86 (verifier reference) all compose without ambiguity.

---

## Formal semantics

```
biometric_match_within(τ_h, τ_v, window_s = 3600) =
  (d_hw ≤ τ_h) ∧ (d_vt ≤ τ_v)
  evaluated over the most recent fresh sample of each modality within `window_s` seconds
```

Where:
- `d_hw` is the most recent handwriting distance (Everest 36) against the active template (Everest 46), within the freshness window.
- `d_vt` is the most recent voice-transcription distance (Everest 37).
- `τ_h` and `τ_v` are per-principal calibrated thresholds (Everest 37 / 38 / 39).
- `window_s` is the freshness window in seconds; default 3600 (1 hour).

Output: a tri-state value `{true, false, unknown}`.

**Unknown cases (tri-state per Everest 61):**
- No biometric sample in the freshness window: `unknown`.
- Sample exists but failed liveness check (Everest 49): `unknown`.
- Active template is out-of-grace (Everest 47): `unknown`.
- Sample's nonce has been seen before (Everest 50 collision): `unknown`.

The `unknown` state is *not* the same as `false`. A counterparty receiving `unknown` learns "the operator could not honestly evaluate this predicate"; receiving `false` learns "the principal is not in baseline." The distinction matters for restricted-action-set negotiation (Everest 97/91).

---

## Predicate ID stability

The full predicate ID encodes thresholds, window, and modality flags:

```
biometric_match_within__τh{τ_h_int}__τv{τ_v_int}__w{window_seconds}
```

Example: `biometric_match_within__τh3435973836__τv3221225472__w3600` corresponds to `τ_h ≈ 0.8, τ_v ≈ 0.75, window = 1h` (with fixed-point uint32 encoding from Everest 44).

The thresholds and window are part of the predicate ID. Changing any one creates a NEW predicate. v0.1 proofs against `τ_h = 0.8` remain valid forever under v0.1 semantics, even if Calm Foundation later publishes a v0.2 predicate at `τ_h = 0.75`. This is what makes proofs durable across protocol evolution (anchored by Everest 53's ID registry).

---

## Single-modality variants

For backward-compat and for use cases where one modality is unavailable:

- `biometric_match_within__τh{τ_h_int}__w{window_seconds}__hw_only` — handwriting only.
- `biometric_match_within__τv{τ_v_int}__w{window_seconds}__vt_only` — voice-transcription only.

The dual-modality form is preferred when both samples are fresh and available. Single-modality variants are explicitly registered (Everest 53) as separate predicate IDs.

---

## Reference truth-table evaluator

```python
def biometric_match_within(
    tau_h: int, tau_v: int, vault: Vault, window_s: int = 3600
) -> Optional[bool]:
    """
    tau_h, tau_v: fixed-point uint32 thresholds in [0, 2^32)
    vault: read access to chain + templates
    window_s: freshness window in seconds
    Returns True / False / None (where None = unknown).
    """
    now_chain_head_ts = vault.chain_head_ts()

    # Most recent handwriting sample within window
    hw_sample = vault.latest_sample(modality="handwriting", within=window_s)
    if hw_sample is None: return None                    # unknown: no fresh sample
    if hw_sample.liveness_status != "passed": return None
    if vault.is_nonce_duplicate(hw_sample.nonce): return None  # Everest 50

    # Most recent voice-transcription sample within window
    vt_sample = vault.latest_sample(modality="voice_transcription", within=window_s)
    if vt_sample is None: return None
    if vt_sample.liveness_status != "passed": return None
    if vault.is_nonce_duplicate(vt_sample.nonce): return None

    # Active template grace check (Everest 47)
    template = vault.active_template_at(now_chain_head_ts)
    if template is None: return None
    if template.grace_expired_at_issuance(now_chain_head_ts): return None

    # Distances (already fixed-point uint32)
    d_hw_int = hw_sample.distance_int
    d_vt_int = vt_sample.distance_int

    return (d_hw_int <= tau_h) and (d_vt_int <= tau_v)
```

The ZK proof system (Everest 65) compiles this evaluator to a Bulletproofs aggregated range proof over `(d_hw, d_vt)` + freshness kernel + template-grace kernel + nonce-uniqueness kernel.

---

## Acceptance test

**T-56.1 (determinism).** 1000 golden inputs (vault states with various sample histories); evaluator returns `true`/`false`/`None` deterministically.

**T-56.2 (boundary).** Sample at `d_hw_int == τ_h` returns `true` (comparison is `≤`, not `<`). At `τ_h + 1`, returns `false`.

**T-56.3 (freshness edge).** Sample with `ts == now - window` is included (`≥`, not `>`); 1 ms older is excluded.

**T-56.4 (ZK equivalence).** For 10 000 input states, the ZK proof system's accept/reject matches the truth-table evaluator on every state.

**T-56.5 (predicate-ID stability).** Same `(τ_h, τ_v, window)` produces identical predicate ID across implementations; different values produce different IDs (content-addressed).

**T-56.6 (single-modality fallback).** When one modality has no fresh sample, `biometric_match_within` returns `unknown`; the single-modality variant against the available modality returns `true`/`false`.

**T-56.7 (tri-state composition with Everest 61).** Composed predicates (e.g., `biometric_match_within ∧ in_baseline_24h`) correctly propagate `unknown` per Everest 61's tri-state composition rules.

**Gate script:** `everest_56_zkbb_biometric_match_within_gate.py`. 50+ pytest assertions.

---

## Composition

- **Everest 6** — predicate vocabulary entry.
- **Everests 36, 37** — distance computation.
- **Everest 38** — fusion variant (if combined-distance form used).
- **Everests 44, 45** — Pedersen commitments + range proof.
- **Everest 47** — template-grace check.
- **Everests 49, 50** — liveness + uniqueness check at intake.
- **Everest 53** — predicate ID registry.
- **Everest 61** — tri-state composition operators.
- **Everest 65** — ZK proof generator hosting the predicate.
- **Everests 73-78** — consent calculus gating disclosure.

— Calm, 2026-05-20
