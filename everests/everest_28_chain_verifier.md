# Everest 28 — Hash-Chain Construction & Verification

*Phase III — Self-Report Substrate. Prereq: Everest 26.*

## Decision

Calm Witness ships a stdlib-only Python verifier as the v0 `calm-witness verify-chain` CLI. No external dependencies. Single file. Runs on any Python 3.9+.

Implementation: [`../calm_witness/verify_chain.py`](../calm_witness/verify_chain.py).
Tests: [`../calm_witness/test_verify_chain.py`](../calm_witness/test_verify_chain.py).

A Rust port lives downstream at Everest 43 (Rust Reference Implementation) and Everest 81 (Rust Production Implementation). The Rust port will be byte-compatible with the Python canonicalisation — `json.dumps(record, sort_keys=True, separators=(",", ":"))` over UTF-8 is the normative encoding, identical to what `serde_json` produces with the same settings.

## Invariants the verifier proves

For each line in `user_state.jsonl`:

1. **record_hash invariant.** `record_hash == sha256_hex(canonical_json(record \ {record_hash}))` where `canonical_json` is `json.dumps(.., sort_keys=True, separators=(",", ":"))`.
2. **prev_hash invariant.** `prev_hash == previous.record_hash`, with the genesis record having `prev_hash == "0" * 64`.
3. **seq invariant.** `seq` starts at 1 and increments by exactly 1.

Any failure on any record causes:
- A per-record `FAIL` line in the report.
- A non-zero exit code from the CLI.
- An explicit diff (`stored:` vs `computed:`) so a human can locate the offending field.

## Threat model the verifier covers

| Attack | Detection |
|---|---|
| In-place edit of any payload field | record_hash invariant breaks |
| Re-ordering records | seq invariant breaks |
| Deleting a record | seq invariant breaks at the gap |
| Splicing in a record | prev_hash invariant breaks at the splice point |
| Recomputing record_hash after tamper | prev_hash invariant breaks for the next record |
| Recomputing every record_hash and re-linking | requires re-deriving the entire chain forward; detectable only against an external chain-head witness (Everest 30 — Sigsum publication) |

The last row is the residual: a sufficiently determined adversary with full disk access can re-derive the chain forward from any point. Everest 30 (Sigsum chain-head publication) closes this by giving an external publicly-auditable witness that the chain head at time `t` was hash `H`. Until 30 is bagged, the chain is tamper-evident at any point an external party already holds a chain-head snapshot.

## Acceptance test — observed

Run against the live vault (~/.calm-vault/user_state.jsonl):

```
$ python3 calm_witness/verify_chain.py
calm-witness verify-chain: /Users/johnbradley/.calm-vault/user_state.jsonl
  seq=   1 OK
  seq=   2 OK

Summary: 2/2 records verified
$ echo "exit code: $?"
exit code: 0
```

Tamper test (simulated in unit tests, see `test_tampered_payload_breaks_hash`):

```
  seq=   2 FAIL
    record_hash mismatch
      stored:   46139445a0a4614cc708316e2dde3fff82f8a34f795f9c25ac8dfdf9505b0788
      computed: <recomputed_hash>
```

CLI shape:

```
calm-witness verify-chain [PATH] [-v | --verbose] [--quiet]
```

Default `PATH` is `~/.calm-vault/user_state.jsonl`. Returns 0 on full verify, 1 on any failure.

## Composition with later summits

- **Everest 29 — Genesis block & provenance.** The verifier doesn't yet check the genesis record's `principal` / `operator` binding to a CredexAI VC. That check lands when Everest 22 (Enrollment → CredexAI VC) and Everest 29 are bagged. The CLI will gain a `--check-genesis-binding` flag.
- **Everest 30 — Chain-head Sigsum publication.** The verifier will gain a `--check-sigsum-inclusion` flag that requires every chain head to have a stored Sigsum inclusion proof.
- **Everest 31 — Roughtime anchoring.** The verifier will gain a `--check-clock-anchor` flag that requires every record's `ts` field to be bracketed by Roughtime attestations within tolerance.
- **Everest 43 — Rust reference implementation.** The Rust port must produce byte-identical canonicalisation; a cross-implementation conformance vector set is part of that summit.

## Why Python first

The Musk-system priority for this summit was *fastest credible verifier*. The decision tree:

- **Rust** — proper, matches `zkac-v0` conventions, but a multi-hour summit with crate scaffolding, CI hookup, and dependency pinning.
- **Bash** — too brittle for canonical-JSON serialisation; would fail subtle byte-equality tests against the Rust port later.
- **Python (stdlib only)** — runs in any environment with Python, no install, no toolchain. Canonical-JSON via `json.dumps(.., sort_keys=True, separators=(",", ":"))` is the de-facto reference encoding; Rust `serde_json` matches it byte-for-byte under equivalent settings.

Decision: ship the Python verifier today; port to Rust at Everest 43 with byte-equality vectors.

— Calm, 2026-05-20
