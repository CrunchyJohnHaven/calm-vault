# Money Python — OBAC + AVS + HARP reference implementation

Money Python is the umbrella for a small family of governance primitives that
make multi-agent AI systems auditable, falsifiable, and revocable. This
directory contains the three primitives that compose the public reference
stack:

- **OBAC** (Observable, Bound, Attestable Chains) — append-only signed claim
  log with Ed25519 signatures, content-addressed claim IDs, Merkle-rooted
  truncation detection, nonce-uniqueness, and subject-side annotation rights.
- **AVS** (Attestation Verification + Synthesis) — derives per-attester
  reliability from agreement-with-higher-reliability-peers, self-burst
  penalties, and BGP-mandate boosts; emits deterministic synthesis with
  agreement clusters and contradictions surfaced.
- **HARP** (Halt / Attest / Revoke / Pact) — quorum-gated halt on the chain;
  emits a `revoke.sh` script when *k* independent halts inside a time window
  are observed; rejects false alarms from low-reliability attesters.

The `bgp_bridge.py` shim connects AVS's reliability score to the Pedersen-
committed alignment-maxim proof system implemented in
`../zk_alignment/zk_alignment.py` (Calm A's existing module).

## How this relates to Calm A's existing code

Money Python **composes with** Calm A's existing `src/zk_alignment/` and
`src/calm_vault.py`; it does not compete with them.

- `bgp_bridge.py` imports `zk_alignment` from `../zk_alignment/zk_alignment.py`
  (the canonical Calm A module). The shim caches a Pedersen commitment of the
  trusted ground-truth maxim and verifies a Schnorr-equality proof for any
  attester pubkey that registers a mandate. This is the only coupling.
- `harp.py` emits a `revoke.sh` whose body calls `python3 calm_vault.py
  revoke-agent <agent_id>` — the exact entry-point that Calm A's
  `src/calm_vault.py` already exposes. The two halves of the system meet at
  that revoke contract: OBAC/AVS/HARP decide *when* to revoke; `calm_vault.py`
  carries out the *how*.

## Quick start

```bash
# From the repo root /tmp/calm-vault (or wherever you cloned)
pip install -r requirements.txt           # cryptography only
python3 -m pytest src/money_python/tests/ -v
bash src/money_python/demo_harp_obac_avs.sh
```

The demo writes its artifacts to `/tmp/obac_demo_<timestamp>/` and prints the
Merkle root of the final chain.

## Test status

**38 / 38 passing** as of 2026-05-11.

```
tests/
  test_obac_crypto.py       8 tests   — signature roundtrip, merkle proofs,
                                        nonce uniqueness, chain linkage
  test_obac_chain.py        6 tests   — tamper detection, splice detection,
                                        truncation detection, replay resistance
  test_obac_annotations.py  3 tests   — subject annotation, no-delete invariant,
                                        disputed-claim weight reduction
  test_avs_synthesis.py     7 tests   — schema shape, contradiction surfacing,
                                        evidence-density-to-confidence, clusters
  test_avs_robustness.py    4 tests   — sybil dampening, evidenceless dilution,
                                        BGP mandate boost, synthesizer
                                        accountability on chain
  test_harp.py              8 tests   — alarm broadcast, k-of-n quorum, window
                                        bounds, false-alarm rejection,
                                        revoke-script generation, rescue stub,
                                        halt-itself-attestable
  test_perf.py              2 tests   — 100 claims < 500ms, 1000 claims < 5s
```

## Files

| File | Purpose |
| --- | --- |
| `obac.py` | Core chain, claim, signature, merkle primitives |
| `avs.py` | Reliability scoring + synthesis emitter |
| `harp.py` | Halt protocol + quorum + revoke-script emitter |
| `bgp_bridge.py` | Schnorr-Σ equality bridge to `zk_alignment` |
| `obac_cli.py` | One-binary CLI: `init`, `keygen`, `attest`, `synthesize`, `halt`, `quorum`, `revoke`, `verify` |
| `demo_harp_obac_avs.sh` | End-to-end story: three attesters, contradicting claims, halt quorum, revoke.sh emission, post-halt synthesis, chain verification |
| `tests/` | The 38-test suite above |

## License

MIT-style permissive, inherits from the repository root `LICENSE` file.
