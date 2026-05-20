# Everest 88 — Performance Budget

*Phase VII — Engineering Reliability. Prereq: Everest 81 (production impl).*

Hot paths in Calm Witness are bounded by published budgets. The benchmark harness ships at [`../calm_witness/bench.py`](../calm_witness/bench.py); CI eventually runs it and fails any commit that regresses by >20%.

## §1. v0 budget table (pure-Python reference)

| Hot path | Target (µs) | Hardware |
|---|---|---|
| `verify_chain` per record, no schema | < 100 | Apple M-series |
| `verify_chain` per record, with schema | < 200 | Apple M-series |
| `validate_record` (per record) | < 50 | Apple M-series |
| `in_baseline_24h` (one self-report) | < 50 | Apple M-series |
| `respond` + `build_disclosure_record` | < 200 | Apple M-series |

These are pure-Python budgets. The Pedersen and Σ-protocol paths are stubbed in v0 (`proof.py`); their real cryptographic costs are tracked separately below.

## §2. v0.1 budget table (Rust kernel via PyO3)

| Hot path | Target (µs) | Notes |
|---|---|---|
| Pedersen commit | < 50 | one Ristretto multiplication |
| Σ-protocol membership proof (4-value OR) | < 200 | four group ops |
| Σ-protocol verification | < 100 | three group ops |
| Bulletproof range proof (64-bit) | < 5,000 | ~5 ms; matches published curve25519-dalek bench |
| Bulletproof verification | < 1,000 | ~1 ms |
| End-to-end disclosure (sign + commit + prove) | < 10,000 | 10 ms wall-clock |

The 10 ms end-to-end budget is the operational ceiling — a Calm Witness disclosure round-trip must be fast enough that an agent transport's network latency dominates, not the cryptography.

## §3. Mobile budget (v1)

When the package ports to iOS / Android (E89):

| Hot path | Target (µs) | Notes |
|---|---|---|
| Pedersen commit | < 200 | A-series mobile silicon |
| Bulletproof range proof | < 20,000 | 20 ms; acceptable for human-interactive sessions |
| End-to-end disclosure | < 40,000 | 40 ms; below perceptual threshold |

Battery budget (E89): less than 5% battery per hour of *continuous* disclosure activity. Real usage is intermittent — < 0.1% battery per active session is the lived experience target.

## §4. Wire-size budget

| Field | v0 placeholder | v0.1 real |
|---|---|---|
| `pedersen_commitment_hex` | 32 bytes (zero hex) | 32 bytes (compressed Ristretto) |
| `sigma_proof_hex` | 96 bytes | 96 bytes (3 × 32) |
| Total response envelope | < 1 KB JSON | < 1 KB JSON |
| Total request envelope | < 512 bytes JSON | unchanged |

Wire shape stays constant from v0 to v0.1 — only the field interpretation tightens.

## §5. Regression policy

A benchmark regression > 20% on any single row in §1 blocks the merging PR. Regression > 10% triggers a warning. Improvements are unbounded.

The benchmark harness produces a deterministic, machine-readable line per case:

```
case                                            min (µs)   median (µs)
----------------------------------------------------------------------------
verify_chain (10 records, no schema)              45.12         48.31
verify_chain (10 records, with schema)           117.40        122.66
validate_record (per record)                       8.91          9.20
in_baseline_24h (one self-report)                 22.05         23.41
respond + build_disclosure_record                 87.12         91.84
```

(Numbers above are illustrative — current machine + current code combine to give the actual measurement.)

## §6. Acceptance test

```bash
python3 calm_witness/bench.py
```

Produces a numerical report on the running machine. The targets in §1 are checked against the *median* column; the min column is informational (peak-of-cache).

— Calm, 2026-05-20
