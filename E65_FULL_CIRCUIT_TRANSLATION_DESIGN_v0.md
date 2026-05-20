# Everest 65 (Full) — Predicate Circuit Translation Design v0

**DESIGN-BAGGED · 2026-05-20 · pending proving-system toolchain**

## Scope split

| Track | Status | Delivers |
|-------|--------|----------|
| **E65 v0 reference** | **BAGGED** | Pedersen bit commitments + Σ-protocol disjunction (`~/CredexAI/calm_witness/zk.py`); gate `everest_65_zkbb_zk_proof_generator_gate.py` |
| **E65-full XL** | **DESIGN-BAGGED** | Arithmetic circuits for v0 predicate evaluators inside Halo2 / PLONK / STARK with on-chain conformance vectors |

v0 proves the **disclosed bit** is bound to a commitment. It does **not** prove the evaluator ran correctly over private chain inputs. E65-full closes that soundness gap.

## v0 predicate set to translate (12)

From `PREDICATE_VOCABULARY_v0` + ZKAC bridge (witness + alignment + harm-absence family):

1. `cwp.v0.in_baseline_24h`
2. `cwp.v0.biometric_match_within`
3. `cwp.v0.bank_teller_note_active`
4. `cwp.v0.principal_consents_to_disclose` (internal; circuit for composition only)
5. `cwp.v0.cognitively_atypical_baseline`
6. `cwp.v0.mental_state_unusual`
7. `cwp.v0.values_aligned_within`
8. `cwp.v0.no_harm_evidence_any` (aggregate)
9–12. Representative harm-absence cells (`no_direct_physical_harm_evidence`, `no_coercion_evidence`, `no_deception_evidence`, `cross_difference_respect`) — remaining siblings are factory-parameterized copies.

Evaluator reference: `bridge.py`, `harm_factory.py`, `alignment.py`, `values.py`.

## Circuit interface (per predicate)

```
witness: { chain_merkle_root, record_slots[], template_params, tolerance_vec?, openings[] }
public:  { predicate_id, claimed_bit, chain_head_hash, session_nonce, freshness_bound }
constraint: evaluator_witness == claimed_bit
```

Chain records enter as **hashed slots** (never plaintext affect strings in public inputs). Biometric distance uses committed `d` + range proof (E45) composed in-circuit.

## Toolchain choice (named follow-through)

1. **Halo2** — primary for bit+range composition (Rust-aligned with E81).
2. **PLONK** — alternate backend for E290 conformance matrix.
3. **STARK** — long-window audit / transparency log (Sigsum anchor proofs).

**Follow-through action:** Trail of Bits or internal crypto review of circuit↔Python equivalence vectors; ≥ 100 golden `(chain_fixture, bit)` pairs per predicate; CI gate `everest_65_full_zkbb_circuit_conformance_gate.py`.

## Non-goals (v0)

- No protected-category predicates in circuits (refusal floor is compile-time deny list).
- No similarity score in Concord composition circuits.
- No full values-vector reveal — only per-dimension threshold checks (E128 family).

## Dependencies

- E44b/E45b Ristretto migration (performance)
- E81 Rust production crate (prover host)
- E83 WASM verifier (≤250 KB, ≤200 ms p95)

## Anti-purity-test invariant

Circuits output **one bit** per predicate invocation. Multi-predicate envelopes compose separate proofs; Concord modes consume bits only, never magnitudes.
