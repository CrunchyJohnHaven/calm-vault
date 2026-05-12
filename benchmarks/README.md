# benchmarks/

Per-decision throughput benchmarks for the Alignment Accountability Layer (AAL).
See [`BENCHMARKS.md`](../BENCHMARKS.md) at the repo root for methodology,
results, and the human-bureaucracy comparison.

## Quickstart

```bash
python3 -m pip install --user 'cryptography>=42.0.0'
python3 benchmarks/run_all.py
```

## Files

- `bench_c1.py` — AAL C1 (Bradley-Gavini equality proof), 1000 iters.
- `bench_c3.py` — AAL C3 (permissionless attestation log), 1000 iters.
- `bench_c5.py` — AAL C5 (permissionless kill switch), 100 iters.
- `aal_c3_attestation_log.py` — minimal in-process C3 reference implementation.
- `aal_c5_kill_switch.py` — minimal in-process C5 reference implementation.
- `run_all.py` — runs all three benchmarks and writes `data/summary.json`.
- `data/` — per-iteration CSVs + the consolidated summary (committed for
  reproducibility).
