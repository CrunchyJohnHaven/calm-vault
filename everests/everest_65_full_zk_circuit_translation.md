# Everest 65-full — Predicate ZK Circuit Translation (XL)

**Status:** DESIGN-BAGGED (pending proving-system toolchain integration) 2026-05-20  
**Canonical plan:** [`../E65_FULL_CIRCUIT_TRANSLATION_PLAN_v0.md`](../E65_FULL_CIRCUIT_TRANSLATION_PLAN_v0.md) — gate `~/CredexAI/scripts/everest_65full_zkac_circuit_plan_gate.py`  
**Follow-through:** Halo2 crate in `~/CredexAI/calm_witness/circuits/` + on-chain conformance vectors per predicate (not started; plan only).

## Acceptance (verbatim from route map)

Translate the twelve v0 Witness predicates (`cwp.v0.*` in `PREDICATE_VOCABULARY_v0.md`) to arithmetic circuits in Halo2 / PLONK / STARK with on-chain conformance vectors; reference semantics in `~/CredexAI/calm_witness/zk.py` and evaluators in `bridge.py` / `predicate_eval.py`.

## v0 reference already bagged

Everest 65 (reference) bags Pedersen + Σ-protocol bit proofs over operator-chosen bits. Everest 103 bags chain→evaluator→bit binding in Python. **65-full** is the step where the *evaluator itself* is inside the proof.

## Translation order (dependency-minimal)

| Order | Predicate ID | Circuit shape | Notes |
|---|---|---|---|
| 1 | `cwp.v0.bank_teller_note_active` | hash equality + window scan | Codeword hash only in witness |
| 2 | `cwp.v0.in_baseline_24h` | set overlap over affect tags | No biometrics |
| 3 | `cwp.v0.principal_consents_to_disclose` | consent matrix lookup | Composes with envelope |
| 4 | `cwp.v0.biometric_match_within` | range proof on distance | Composes Everest 45 |
| 5–12 | remaining v0 predicates | per `predicate_eval.py` | See vocabulary |

## Conformance vector format

Each predicate ships `circuits/conformance/<predicate_id>.json`:

```json
{
  "predicate_id": "cwp.v0.in_baseline_24h",
  "public_inputs": ["chain_merkle_root", "baseline_fingerprint"],
  "witness": ["redacted_chain_witness"],
  "expected_bit": 1
}
```

Gate `everest_65_full_zkbb_circuit_conformance_gate.py` runs: compile circuit → prove → verify → compare bit to Python `bridge.dispatch`.

## Refusal floor in circuits

Circuits MUST NOT introduce protected-category signals as public inputs. Any proposal that adds race/religion/political/etc. as witness fields is rejected at audit triage — same ratchet as `COMPASS_PREDICATES_v0.md` §4.

## Named follow-through

1. **CredexAI:** `cargo init calm_witness_circuits` with `halo2_proofs` (pinned rev).
2. **Conformance:** 12 vectors green in CI before mainnet/registry publication.
3. **External:** optional Trail of Bits review of circuit↔Python equivalence (Everest 165 family).

— Calm, 2026-05-20
