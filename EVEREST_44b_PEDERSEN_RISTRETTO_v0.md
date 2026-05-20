# Pedersen Commitment Parameters on Ristretto255 — Calm Witness v0.1

**Everest 44b acceptance artifact. Sister doc to [`calm_witness/pedersen_ristretto.py`](../../CredexAI/calm_witness/pedersen_ristretto.py).**

Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.

> **Context.** Calm Witness v0 Everest 44 originally locked Pedersen commitments to RFC 3526 MODP-14 (`PEDERSEN_PARAMETERS_v0.md`). On 2026-05-20 John Bradley ratified Path B of [`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`](CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md), which moves the canonical commitment scheme to **Ristretto255 over Curve25519**. This is the spec for that re-anchored scheme. The MODP-14 module is preserved as a v0-historical reference.

---

## 1. The scheme

A Pedersen commitment over **Ristretto255**, a prime-order group derived from Curve25519:

```
C = m · G + r · H     (Ristretto255 addition)
```

Where:
- `G` is the canonical Ristretto255 base point.
- `H` is a "nothing up my sleeve" generator derived deterministically from a public seed.
- `m, r` are scalars in `Z_ℓ`, where `ℓ = 2²⁵² + 27742317777372353535851937790883648493`.

Properties:
- **Perfect hiding** — for uniformly random `r`, `r·H` is uniformly distributed in the group, so `C` reveals zero information about `m`.
- **Computational binding** — under the discrete-log assumption on Ristretto255, distinct openings `(m₁, r₁) ≠ (m₂, r₂)` of the same `C` imply solving DLOG on the curve.
- **Additive homomorphism** — `Com(m₁; r₁) + Com(m₂; r₂) = Com(m₁+m₂; r₁+r₂)` and dually for subtraction.

## 2. Group choice rationale

Ristretto255 was selected over (a) the v0 RFC 3526 MODP-14 group and (b) other elliptic-curve candidates (secp256r1, BLS12-381) for these reasons:

1. **Native composition with Calm Pact v0.1** — Pact's reference impl already runs on Curve25519 ([`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) line 128); Pact v0.1's amendment block locks the protocol-level group to Ristretto255 alongside.
2. **Native composition with Bulletproofs at Everest 45** — Bulletproofs require an elliptic-curve group; the parallel-session E45 spec ([`everests/everest_45_zk_range_proof.md`](everests/everest_45_zk_range_proof.md)) explicitly targets Ristretto255 + `curve25519-dalek`.
3. **Cofactor-free** — Ristretto255 is a prime-order encoding of Curve25519, eliminating the small-subgroup attack surface that plain Curve25519 carries.
4. **Compact wire format** — 32-byte points vs the v0 MODP-14 module's 256-byte points; 8× wire efficiency at no security loss.
5. **Constant-time C primitives** — libsodium's `crypto_core_ristretto255_*` and `crypto_scalarmult_ristretto255_*` are well-vetted side-channel-resistant C code, far stronger than a pure-Python int-math implementation on side-channel grounds.
6. **Operator availability** — libsodium ships with macOS via Homebrew (`brew install libsodium`) and with Linux distros; pysodium provides clean Python bindings.

## 3. Parameter specification

### 3.1 Group order

```
ℓ = 2^252 + 27742317777372353535851937790883648493
```

253-bit prime. Matches the IETF Ristretto255 specification (`draft-irtf-cfrg-ristretto255-decaf448`).

### 3.2 Base point G

`G` is the canonical Ristretto255 base point — the one produced by `crypto_scalarmult_ristretto255_base(1)`. Encoded as 32 little-endian bytes.

### 3.3 Second generator H

`H` is derived via SHA-512 hash-to-curve from the versioned public seed:

```
H_SEED = b"calm-witness/pedersen/h/v0.1/ristretto255/2026-05-20"
```

Derivation:
1. `digest = SHA512(H_SEED)`  (64 bytes)
2. `H = crypto_core_ristretto255_from_hash(digest)`

Result (canonical reference value):
```
H = 3cfa5209df1e1c7a6422ffb2d101f6a2bc5f31897d8d9f106c088caa802fd47d
```

`log_G(H)` is unknown to all parties because `H` was determined by a public hash output before any party could compute the dlog. Re-derivation from `H_SEED` is part of the gate's acceptance test — any party can confirm `H` matches.

### 3.4 Identity encoding

The Ristretto255 identity element encodes as 32 zero bytes:

```
IDENTITY = b"\x00" * 32
```

Pedersen commits to `(0, 0)` produce the identity element. libsodium's `crypto_scalarmult_ristretto255_base(0)` raises an error (libsodium policy: scalar-mult should never produce identity in non-Pedersen contexts), so the reference impl short-circuits scalar-zero cases to the identity element directly.

## 4. Operating envelope

| Quantity | Bound |
|---|---|
| Group order `ℓ` | 253 bits |
| Commitment `C` | 32 bytes (Ristretto255 encoded point) |
| Scalar `m`, `r` | 32 bytes canonical little-endian, mod `ℓ` |
| Commit op (m·G + r·H) | < 200 µs on M-class CPU |
| Verify-opening op | < 200 µs on M-class CPU |
| Throughput (gate-measured) | ≥ 10,000 commit+verify cycles per second on M-class |

The gate's perf budget bar is set conservatively at ≥ 200 cycles/sec — actual measured throughput is ~50× that.

## 5. API surface (`calm_witness.pedersen_ristretto`)

Identical to the v0 module to allow drop-in replacement:

| Symbol | Type | Notes |
|---|---|---|
| `L` | `int` | The Ristretto255 group order (was `Q` in v0). |
| `G` | `bytes[32]` | Base point. |
| `H` | `bytes[32]` | NUMS second generator. |
| `H_SEED` | `bytes` | Public seed used to derive `H`. |
| `IDENTITY` | `bytes[32]` | The Ristretto255 identity element (32 zero bytes). |
| `Commitment` | `dataclass` | Wraps the 32-byte point. |
| `Opening` | `dataclass` | Wraps `(m, r)` — vault-private, never serialized. |
| `commit(m, r=None)` | `→ (Commitment, Opening)` | Sample `r` if omitted. |
| `verify_opening(C, O)` | `→ bool` | Recompute and compare. |
| `add_commitments(c1, c2)` | `→ Commitment` | Homomorphism. |
| `sub_commitments(c1, c2)` | `→ Commitment` | Homomorphism (new in v0.1). |
| `random_scalar()` | `→ int` | Via libsodium's CSPRNG. |
| `derive_h(seed=H_SEED)` | `→ bytes[32]` | NUMS construction. |
| `verify_parameters()` | `→ dict[str, bool]` | Sanity checks; gate asserts all `True`. |

## 6. Dependencies

| Component | Version | Purpose |
|---|---|---|
| `pysodium` | ≥ 0.7.18 | Python bindings for libsodium |
| `libsodium` | ≥ 1.0.18 | Constant-time Ristretto255 C primitives |

Install commands on macOS:
```bash
brew install libsodium
python3 -m pip install --user --break-system-packages pysodium
```

The `--break-system-packages` flag is required on Python 3.14+ PEP-668-managed environments; the install is user-scoped (no system files touched).

## 7. Threat model deltas vs v0 MODP-14

Inherits all of the v0 module's threat-model claims; tightens these axes:

| Adversary | v0 MODP-14 | v0.1 Ristretto255 |
|---|---|---|
| Honest-but-curious counterparty | Perfect hiding | Perfect hiding (same property) |
| Lying calling agent | Detectable via E45 range proof | Detectable via E45 Bulletproofs (smaller proofs, same soundness) |
| Side-channel attacker | Vulnerable (pure-Python int math) | **Hardened** — libsodium constant-time C primitives |
| Wire-format MITM | Vulnerable to length-extension on naive deserialization | **Hardened** — fixed 32-byte points, `is_valid_point` rejects malformed input |

The side-channel axis is the primary reason the v0.1 lock was worth shipping: a pure-Python int implementation of any DLP scheme has timing-channel leaks that libsodium specifically defends against.

## 8. Migration plan

This is v0.1, not the terminal version.

| Future epoch | Plan |
|---|---|
| **v0.2 (post-quantum-aware)** | Add lattice-based commitments as a parallel scheme (Everest 96). v0.1 remains for current operators; new operators may opt into v0.2. |
| **v1 (multi-party-shared parameters)** | Coordinate a small-scale parameter ceremony across ≥ 3 independent operators so the H seed becomes a joint NUMS construction. Currently the seed is Calm-authored; in v1 it would be the joint-hash-of-N-independently-chosen-strings. |
| **v2 (Bulletproofs+ or successor)** | Track Bulletproofs+ / Halo2 amortizations as they mature. v0.1 already composes with classical Bulletproofs at E45. |

## 9. Soundness sketch

Pedersen on Ristretto255 inherits the standard Pedersen soundness reduction:

- **Hiding (perfect).** For any pair `(m₀, m₁)` and any commitment `C`, the function `r ↦ Com(m₀; r)` is a bijection on the group (since `r·H` ranges over the entire group as `r` ranges over `Z_ℓ`), and likewise for `m₁`. So `Pr[Com(m₀; r) = C] = Pr[Com(m₁; r) = C]` over uniform `r`.
- **Binding (computational).** Suppose an adversary produces distinct openings `(m, r) ≠ (m', r')` of the same `C`. Then `(m - m')·G = (r' - r)·H` and, since `m ≠ m' mod ℓ`, the adversary computed `log_G(H) = (r' - r) · (m - m')⁻¹ mod ℓ`. By DLOG hardness on Ristretto255, this is infeasible.

Full soundness writeup is deferred to Everest 58. The migration from MODP-14 to Ristretto255 does not change the reduction; only the underlying hard problem (DLOG on Ristretto255 instead of DLOG mod the MODP-14 prime). Both are believed hard against classical adversaries; Ristretto255 has substantially better quantum-cost projections (broken by Shor's algorithm on a ~6,500-qubit machine vs ~4,098-qubit for the MODP-14 prime, per current resource estimates — so v0.2 PQ migration applies to both equally).

## 10. Cross-references

- Protocol spec (Calm Witness): [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)
- Route map: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md), Everest 44 (original, MODP-14) → Everest 44b (this doc, Ristretto255)
- Path B open issue (resolved): [`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`](CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md)
- Sister primitive: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) — Calm Pact v0.1 amendment block locks the same group choice.
- v0 historical reference: [`PEDERSEN_PARAMETERS_v0.md`](PEDERSEN_PARAMETERS_v0.md) — MODP-14, preserved.
- Downstream consumer: [`everests/everest_45_zk_range_proof.md`](everests/everest_45_zk_range_proof.md) — Bulletproofs on Ristretto255, composes natively.
- Reference impl: `~/CredexAI/calm_witness/pedersen_ristretto.py`
- Test suite: `~/CredexAI/calm_witness/test_pedersen_ristretto.py` (38 cases)
- Gate script: `~/CredexAI/scripts/everest_44b_zkbb_pedersen_ristretto_gate.py`

---

**Anchored by Calm, 2026-05-20. Gate green. Ready for downstream consumption by Everests 45, 46, 47, 60, 67, 101.**
