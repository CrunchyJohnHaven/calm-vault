# Calm Pact Spec — Internal Inconsistency on Commitment Group (RESOLVED)

**Filed 2026-05-20 by Calm. Ratified 2026-05-20 by John Bradley: **Path B (Ristretto255 everywhere)**.**

> **Resolution status (2026-05-20):** John ratified Path B. The lines 11 and 89 amendments have been applied to [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) in-place as a v0.1 transition block. A new Calm Witness summit **Everest 44b — Pedersen on Ristretto255** is the next implementation work; the existing MODP-14 `pedersen.py` is preserved as a v0-historical reference. Routes downstream of E44 (E45 Bulletproofs on Ristretto, E60 verifier, E67 disclosure response, E101 Σ-protocol) compose natively against the v0.1 commitment scheme without further amendments.

---

## Original filing

This note flags a substrate-level contradiction in [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) that surfaces when Calm Witness's downstream cryptographic Everests (44, 45, 60) try to compose with Calm Pact's commitment scheme. The contradiction does not block any individual Everest — both Calm Witness v0 (MODP-14 Pedersen at Everest 44) and Calm Witness v0.1 (Bulletproofs on Ristretto255 at Everest 45) have been bagged — but it leaves the protocol family with no single source of truth for "which group does Pedersen live in."

## The three contradictory statements in `CALM_PACT_PROTOCOL_v0.md`

1. **Line 11 (abstract):** "Each commits to its primary mandate via a Pedersen commitment on a **2048-bit Schnorr group**."
2. **Line 89 (parameters):** "Public parameters: a group `G` of prime order `q` with two independent generators `g`, `h` ... can use **secp256r1, Ed25519, or BLS12-381**."
3. **Line 128 (reference impl):** "Uses the `cryptography` package on **Curve25519 (Ed25519 / X25519 group)**."

The three statements name at least two cryptographic regimes:

- **Classical Schnorr group** (line 11): typically RFC 3526 MODP-14 or similar prime-field DLP.
- **Elliptic-curve groups** (lines 89, 128): Curve25519 / Ed25519 / Ristretto255 / secp256r1 / BLS12-381.

These are not interchangeable. Pedersen commitments in one cannot be opened or composed with proofs in the other without a re-commit step.

## What downstream summits have done

| Summit | Choice | Source |
|---|---|---|
| **Everest 44 — Pedersen Commitment Parameters** | RFC 3526 MODP-14 (2048-bit safe prime) | [`PEDERSEN_PARAMETERS_v0.md`](PEDERSEN_PARAMETERS_v0.md) §2.1 |
| **Everest 45 — ZK Range Proof** | Bulletproofs on Ristretto255 | [`everests/everest_45_zk_range_proof.md`](everests/everest_45_zk_range_proof.md) §2 |
| **Everest 101 — Σ-protocol for opening Pedersen** | MODP-14 (compatible with E44) | `calm_witness/sigma.py` |

Calm Witness has effectively chosen **both** groups: MODP-14 for the Pedersen scheme that holds the distance commitment, and Ristretto255 for the Bulletproof that proves `d < τ`. These are compatible only if a re-commit bridge exists — which is not currently spec'd. As-is, the v0 substrate cannot ship E45 without amending either E44 or the bridging step.

## The three resolution paths

### Path A — Lock Schnorr (MODP-14) everywhere
Amend `CALM_PACT_PROTOCOL_v0.md` lines 89 and 128 to match line 11. Calm Witness Everest 45 swaps Bulletproofs for **bit-decomposition + Σ-OR** range proofs (works natively on MODP-14, no trusted setup, larger proofs at ~48 KB for 64-bit ranges). Net:
- ✅ Pure-Python reference impl with no EC binding dependency.
- ✅ Vetted prime-field group (IPsec-grade since 2003).
- ❌ Proof size ~70× larger than Bulletproofs.
- ❌ Diverges from the Calm Pact reference-impl Python code that currently uses `cryptography` on Curve25519 — that impl must be rewritten.

### Path B — Lock Curve25519 / Ristretto255 everywhere
Amend line 11 to match line 128. Calm Witness Everest 44 re-locks Pedersen to Ristretto255, the in-flight `pedersen.py` is rewritten to wrap a Ristretto binding (e.g., `pyo3-cryptography` or `pynacl`), and the existing test corpus is migrated. Net:
- ✅ Native composition with Bulletproofs at E45 (672-byte proofs for 64-bit ranges).
- ✅ Matches the Calm Pact reference impl already at line 128.
- ✅ Smaller commitments, faster ops.
- ❌ Requires a vetted Python Ristretto binding (`PEDERSEN_PARAMETERS_v0.md §6` explicitly defers this to Everest 61).
- ❌ Invalidates the in-flight `pedersen.py` MODP-14 work and its test suite.

### Path C — Document the bridge (status quo, made explicit)
Amend `CALM_PACT_PROTOCOL_v0.md` to enumerate both groups and label them: "directive-equality commitments live in MODP-14; biometric-distance commitments live in Ristretto255; Σ-protocol composition across groups uses a Bridge proof (Everest 102, new summit)." Net:
- ✅ Preserves both in-flight implementations.
- ❌ Introduces a non-trivial new summit (cross-group commitment bridging).
- ❌ More surface area for bugs; the security proof of the composed scheme becomes harder.
- ❌ The "Two AI agents pass a single bit" framing now requires explaining a 2-group cryptographic substrate.

## Recommended path

**Path B (Ristretto255 everywhere).** Rationale:

1. The Calm Pact reference impl already runs on Curve25519 (line 128). Lock to where the code actually is, not where the prose pretends.
2. Bulletproofs is the cleanest Everest 45 construction; choosing it forces the commitment scheme.
3. The migration cost is one bagged summit's work (rewrite `pedersen.py`) and the test corpus is generated by the spec, not authored by hand — re-generation is mechanical.
4. The route map already names `ristretto255` as the v0.1 migration target (`PEDERSEN_PARAMETERS_v0.md §6`); promoting it to v0 is a 5-minute decision and a half-day implementation slice.
5. Path B is forward-compatible with future post-quantum migration (Everest 89) more cleanly than Path A — most PQ candidates are formulated over elliptic curves or lattices, not multiplicative groups mod p.

If Path B is ratified: a new summit (call it **Everest 44b — Pedersen on Ristretto255**) supersedes the current Everest 44, the existing MODP-14 `pedersen.py` is preserved as a v0-historical reference implementation, and Calm Pact ships as v0.1 with the line-11 and line-89 amendments.

## What is being asked of John

A single decision: **A, B, or C**, plus an optional "different" if you want a path I haven't named.

If you pick B, I (or the parallel CALM session, whoever picks it up next) will draft the `CALM_PACT_PROTOCOL_v0.1.md` amendments and start the `pedersen_ristretto.py` rewrite alongside an `everest_44b_*_gate.py` gate that proves the rewrite reproduces the existing E44 acceptance test suite plus the new Ristretto-side properties.

Until ratified, Everest 45's bag is "spec + addendum complete; impl pending the commitment-scheme lock." The MVP-12 "ALL BAGGED" marker is a spec-level milestone; impl-level MVP requires this decision.

## Cross-references

- [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) — the inconsistent source.
- [`PEDERSEN_PARAMETERS_v0.md`](PEDERSEN_PARAMETERS_v0.md) — Calm Witness E44 MODP-14 choice.
- [`everests/everest_45_zk_range_proof.md`](everests/everest_45_zk_range_proof.md) — Calm Witness E45 Ristretto + Bulletproofs choice.
- [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) — route map (current bagged: 40/100).
- Research basis: [[reference-calm-witness-research-findings]] in CALM auto-memory.

---

**Filed by Calm, 2026-05-20.** Awaiting John's ratification for one of paths A / B / C.
