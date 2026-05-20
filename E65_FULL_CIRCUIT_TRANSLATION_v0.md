# Everest 65-full — Predicate Circuit Translation (Halo2 / PLONK / STARK)

**Draft v0 · 2026-05-20 · Calm**
**Extends Everest 65 (v0 Python Σ-protocol reference in `~/CredexAI/calm_witness/zk.py`).**
**Executable scaffold:** `~/CredexAI/calm_witness_circuits/` (Halo2 over Pasta).

## §1 — What “full” means

v0 shipped **bit commitments + Σ-protocol proofs** without proving the predicate *evaluator* inside the circuit. A malicious operator could commit to a bit that disagrees with chain evaluation unless the **bridge** (Everest 103) binds evaluator semantics via `predicate_id`.

Everest 65-full closes that gap: each v0 predicate’s Python evaluator (`predicate_eval.py`, `compass_eval.py`, `bridge.py`) is translated to an arithmetic circuit; the proof attests **evaluation correctness** on committed inputs, not merely knowledge of a chosen bit.

## §2 — Source of truth (compile from these)

| Layer | Path |
|-------|------|
| Witness evaluators | `~/CredexAI/calm_witness/predicate_eval.py`, `bridge.py` |
| Compass evaluators | `~/CredexAI/calm_witness/compass_eval.py` |
| Golden corpora | `~/CredexAI/calm_witness/golden/*.json` |
| v0 bit-proof spec | `~/CredexAI/calm_witness/zk.py` |
| Architectural kernels | `everests/everest_65_predicate_zk_proof_generator.md` |
| Predicate IDs | `~/CredexAI/calm_witness/schema/predicates_v0.json`, `COMPASS_PREDICATES_v0.md` |

**Bit-stability rule:** for every conformance vector, the circuit public output must equal the Python reference on the same committed inputs.

## §3 — Predicate inventory (12 + 6)

### Witness (namespace `cwp.v0.*`)

1. `cwp.v0.in_baseline_24h` — set overlap on affect tags in 24h window (kernel: `set_membership` + `freshness`)
2. `biometric_match_within` — range proof on distance ≤ τ (kernel: `range_proof`)
3. `bank_teller_note_active` — hash equality to enrolled codeword commitment (kernel: `equality_to_commitment`)
4. `cognitively_atypical_baseline` — enrollment flag (kernel: `chain_record_lookup`)
5. `principal_consents_to_disclose` — consent matrix lookup (kernel: `signed_classification`, internal)
6. `novelty_not_substitution` — template drift bound (kernel: `range_proof` + `freshness`)

### Compass (namespace `ccp.v0.*`)

7. `unselfish_act_in_window_30d` — count ≥ N unselfish_act records
8. `cross_group_engagement_in_window_90d` — out-group interaction records
9. `refused_opportunity_to_harm` — paired opportunity + alternative narrative
10. `respect_for_difference_evidence` — two-party signature present
11. `no_known_willful_harm_in_window_365d` — negation + counter-claim state machine
12. `willing_to_be_corrected` — weighted correction records

## §4 — Proving system choice

| Track | Toolchain | Role |
|-------|-----------|------|
| **Primary** | Halo2 (PLONKish, Pasta) | In-circuit evaluators; dev-friendly; no trusted setup |
| **Conformance export** | JSON vectors → Solidity `verifyProof` stubs (future) | On-chain bit checks |
| **STARK fallback** | Winterfell / RISC Zero (deferred) | Long-horizon PQ-friendly replay |

v0 scaffold uses **Halo2 0.3** with `MockProver` for CI gates; production moves to `Params` + `ProvingKey` artifacts per predicate.

## §5 — Circuit shape (per predicate)

```
public_inputs:  [chain_head_hash, predicate_id_hash, counterparty_class_hash, ...params]
private_witness: [committed chain segment, openings, evaluator temporaries]
public_outputs: [bit]
constraints:
  1. Merkle inclusion of chain segment under chain_head_hash
  2. Evaluator arithmetic identical to Python reference
  3. Boolean output ∈ {0,1}
  4. Optional: link output to Pedersen bit commitment (compose with zk.py layer)
```

## §6 — Conformance vectors

Directory: `~/CredexAI/calm_witness_circuits/conformance/`

Each file lists ≥2 vectors per predicate: positive + negative, drawn from golden corpora. Schema in `conformance.rs` (`ConformanceVector`).

Gate: `~/CredexAI/scripts/everest_65_full_zkbb_circuit_halo2_gate.py`

## §7 — Migration from Python v0

1. **Phase A (this pass):** boolean scaffold circuit + toolchain compiles; vectors for `in_baseline_24h` stub.
2. **Phase B:** translate `in_baseline_24h` + `biometric_match_within` kernels; cross-check 35 + 15 golden cases.
3. **Phase C:** remaining Witness predicates; compose AND/OR in-circuit (Everest 61).
4. **Phase D:** six Compass predicates; composite envelope (Everest 122/123) verifies circuit bundle.

## §8 — Refusal floor in circuits

Circuits MUST NOT introduce witness wires for protected categories (PREDICATE_VOCABULARY_v0 §4, COMPASS_PREDICATES_v0 §4). Audit gate fails if circuit AST references prohibited attribute names.

## §9 — Status

**DESIGN-BAGGED + TOOLCHAIN-SCAFFOLD (Summit 65-full/300) 2026-05-20** — spec + `calm_witness_circuits` crate compiles; first `bit_commitment` MockProver path green; full 18-predicate translation is follow-through per §7 phases B–D.
