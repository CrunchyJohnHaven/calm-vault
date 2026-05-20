# ZKAC Pact Version Bridge v0

**Closes Everest 136 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

**Prereq:** Everest 121 ([`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md)), [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md).

**Acceptance test:** Composite envelopes minted under `calm-pact/v1` verify on counterparties that advertise only `calm-pact/v0-stub` during the published deprecation window, and the inverse holds for v0-stub minters against v1 verifiers. Unknown `pact_wire` values reject with `unsupported_pact_version`, never with a false `equality_bit`. Bridging rules are normative for `pact_digest` versioning, bit semantics, scope forfeits, and anti-purity-test output shape.

---

## §1 | Problem statement

Calm Pact proves categorical directive equality between two autonomous agents. In composite ZKAC envelopes (Everest 122), the Pact section carries a session binding digest, a single disclosed bit, and proof bytes. When the Pact wire bumps from `calm-pact/v0-stub` (placeholder Σ-proof) to `calm-pact/v1` (production Ristretto255 equality proof per Calm Pact §4), counterparties must not fracture.

A counterparty on v0-stub must still verify v1 envelopes that pass downgrade rules. A v1 verifier must accept v0-stub envelopes during the window. A verifier that receives an unknown `pact_wire` must refuse parsing and return `unsupported_pact_version`. It must not map unknown wire to `equality_bit: 0` or emit numeric similarity scores as a substitute for the one bit.

This document specifies **Pact primitive bridging only**. CredexAI platform bridging is Everest 135. Witness and Compass wire bumps are Everests 137 and 138. Shared window discipline lives in [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md).

---

## §2 | Normative definitions

| Term | Meaning |
| --- | --- |
| **Pact wire v0-stub** | Wire label `calm-pact/v0-stub`. Composite `PactSection` uses `pact_digest`, `equality_bit`, and opaque `proof_bytes` stub. Digest material includes `session_nonce`, `counterparty_id`, and `pact_wire`. |
| **Pact wire v1** | Successor label `calm-pact/v1`. Full Pedersen commitment exchange and Schnorr equality proof per Calm Pact §4.2. `pact_digest` algorithm unchanged in binding intent; `proof_bytes` carries production Σ-proof. |
| **pact_digest** | 64-hex SHA-256 of canonical JSON digest material. Binds session nonce, counterparty, and `pact_wire`. Counterparties recompute expected digest before accepting `equality_bit`. |
| **equality_bit** | Single integer in `{0, 1}`. The only Pact learning the counterparty receives: directives categorically equal (1) or not (0). Semantics are **identical** across all supported Pact wires during and after the window. |
| **pact_wire** | String field inside digest material and, at v1, explicit on `PactSection`. Identifies which Pact cryptographic profile produced the section. |
| **Deprecation window** | 180 calendar days after `calm-pact/v1` general availability. During the window, v1 verifiers accept v0-stub sections; v0-stub verifiers accept v1 sections that pass downgrade (§5). |
| **unsupported_pact_version** | Structured rejection when `pact_wire` is absent from the verifier's supported set and no deprecation alias applies. Distinct from `equality_bit: 0`. |

---

## §3 | pact_digest versioning

### §3.1 | v0-stub digest material

Reference implementation (`pact_session_digest` in `~/CredexAI/calm_witness/zkac_envelope.py`) defines v0-stub material:

```json
{
  "counterparty_id": "<string>",
  "pact_wire": "calm-pact/v0-stub",
  "session_nonce": "<string>"
}
```

Canonical JSON uses sorted keys and compact separators (ZKAC Type System §3). `pact_digest = SHA-256(canonical_json(material))`.

### §3.2 | v1 digest material

v1 uses the **same key set**. Only `pact_wire` changes to `calm-pact/v1`. Session binding fields do not change names or order. A verifier recomputes digest with the wire label read from the envelope (or inferred during downgrade per §5).

### §3.3 | Digest stability invariant

Implementations MUST NOT alter digest inputs for an existing `pact_wire` label without publishing a new wire label. Renaming a field, reordering keys outside canonical sort, or changing hash function constitutes a new `pact_wire`, not a silent patch.

### §3.4 | Explicit wire on PactSection (v1 forward)

v1 `PactSection` SHOULD include top-level `pact_wire`:

```json
{
  "equality_bit": 0,
  "pact_digest": "<64-hex>",
  "pact_wire": "calm-pact/v1",
  "proof_bytes": "<hex>"
}
```

v0-stub sections MAY omit `pact_wire`; verifiers infer `calm-pact/v0-stub` when absent.

### §3.5 | Verifier acceptance

Before digest check, verifiers call:

```
bridge_pact_accepted(section.pact_wire_or_inferred, verifier_supported_pact_wires) == true
```

If false, return `unsupported_pact_version` and MUST NOT read `equality_bit` as authoritative.

---

## §4 | equality_bit semantics across versions

### §4.1 | One bit, all wires

`equality_bit` means the same thing on every supported Pact wire:

- **1:** The operator attests that the Pact equality proof verified at the agreed categorical depth. Directives are categorically equivalent per Calm Pact §4.3.
- **0:** The proof failed or directives differ at the requested depth.

Wire bumps do not redefine 0 or 1. They do not introduce fractional alignment, confidence intervals, or depth-weighted scores.

### §4.2 | No false bit on version mismatch

Unknown or expired `pact_wire` MUST NOT map to `equality_bit: 0`. Counterparties distinguish:

| Outcome | Counterparty learns |
| --- | --- |
| Proof verifies, directives equal | `equality_bit: 1` |
| Proof verifies, directives differ | `equality_bit: 0` |
| Unsupported `pact_wire` | Error `unsupported_pact_version` only |
| Digest mismatch | Error `pact_digest_mismatch` only |

### §4.3 | Downgrade and bit preservation

When a v1 section downgrades for a v0-stub verifier (§5), `equality_bit` MUST survive unchanged. Downgrade strips v1-only proof encodings; it does not flip or re-interpret the bit.

### §4.4 | Composite envelope binding

In `CompositeEnvelope`, Pact is optional. When present, `equality_bit` is the sole Pact output in `composite_observable_fields`. Witness and Compass bits remain predicate-specific. Unified verification (Everest 139) returns `pact_equality_bit` as `int | null`, never a float.

---

## §5 | Deprecation window and downgrade

### §5.1 | Window length

Shared with Everests 135 to 138: **180 days** after v1 GA. Operators publish `pact_deprecation_window_end_iso` in `/.well-known/calm-operator.json`.

### §5.2 | Verifier supported set

Each Operator publishes:

```json
{
  "supported_pact_wires": ["calm-pact/v0-stub", "calm-pact/v1"],
  "pact_deprecation_window_end_iso": "2026-11-20T00:00:00Z"
}
```

Reference checker: `bridge_pact_accepted(pact_wire, frozenset(supported_pact_wires))` in `~/CredexAI/calm_witness/version_bridge.py`.

### §5.3 | Forward path (v0-stub verifier, v1 minter)

During the window:

1. v1 minter sets `pact_wire: calm-pact/v1`.
2. v0-stub verifier accepts via `bridge_pact_accepted` if v1 is in supported set or v0-stub verifier lists v1 during window.
3. If v0-stub verifier cannot verify v1 `proof_bytes`, minter SHOULD dual-encode: include v0-stub-compatible `proof_bytes` alongside v1 proof, or mint at v0-stub wire for that counterparty.

### §5.4 | Backward path (v1 verifier, v0-stub minter)

v1 verifiers MUST accept `calm-pact/v0-stub` sections during the window. Stub `proof_bytes` checks (presence, hex validity) remain sufficient for v0-stub.

### §5.5 | Allowed downgrade transforms

| v1-only field | Downgrade action |
| --- | --- |
| Extended Schnorr proof in `proof_bytes` | v0-stub verifier uses stub verification path if dual-stack stub present |
| `categorical_depth` metadata | Omit for v0-stub; default depth from request context |
| `commitments` object | Omit when v0-stub schema has no slot; digest binding still required |

### §5.6 | Forbidden downgrades

Implementations MUST NOT:

- Coerce `equality_bit` from 1 to 0 or 0 to 1.
- Drop `pact_digest` or recompute with a different `pact_wire` without explicit wire label.
- Replace `unsupported_pact_version` with a bit outcome.

---

## §6 | Scope forfeits and prohibited uses

Version bumps do not relax Calm Pact prohibited uses or sister primitive scope statements.

### §6.1 | Pact scope ratchet

Calm Pact deployments that use a wire bump to:

- Prove directive equality against principals who did not consent to Pact disclosure,
- Bypass CredexAI identity attestation,
- Or enable Concord-style population sorting across many agents,

forfeit Calm Pact naming rights and Operator attestation per [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §3.2 and Concord scope inheritance.

### §6.2 | Employment and credit (out of scope)

Pact bridging MUST NOT be used to prove or infer suitability for **employment**, **credit**, **insurance underwriting**, or **tenant screening**. Wire bumps do not authorize new predicate categories for those domains. Operators deploying Pact for those purposes forfeit attestation regardless of `pact_wire`.

### §6.3 | Wire bump is not new capability

A new `pact_wire` MUST NOT introduce predicate categories, vocabulary nodes, or disclosure fields that were blocked at the prior wire. New categorical depth features require a new predicate registry ceremony, not a wire label alone.

### §6.4 | Forfeit record

Material scope violations during bridging SHOULD append a principal chain record `kind: scope_forfeit` referencing the envelope digest and `pact_wire`. Counterparties treat subsequent envelopes from that Operator under enhanced default-deny until remediation is published.

---

## §7 | Anti-purity-test (no similarity scores)

Pact bridging inherits Concord output-shape refusal (CALM_CONCORD_PROTOCOL §4, [`CALM_REFUSAL_FLOOR_INDEX.md`](CALM_REFUSAL_FLOOR_INDEX.md) §2).

### §7.1 | Forbidden outputs

Pact verification and bridging APIs MUST NOT return:

- Numeric similarity scores, alignment scores, or match quality floats.
- Rankings derived from Pact outcomes across agents.
- Protected-category labels inferred from directive vocabulary paths.

The only Pact outcome exposed to a counterparty is `equality_bit ∈ {0, 1}` or an error code.

### §7.2 | Bridging must not add scores

Wire bumps MUST NOT add fields such as `alignment_score`, `proof_confidence`, or `categorical_distance` to `PactSection` or verification results. v1 Schnorr proofs verify discretely; they do not leak a graded metric.

### §7.3 | Unified verify API

`verify_zkac` (Everest 139) returns `pact_equality_bit: int | null`. Gate scripts reject schemas that type this field as `number` for fractional values.

### §7.4 | Population use

Using Pact bridging to run equality checks across a population and sort agents by pass rate is a prohibited Concord pattern. Rate limits and meeting-protocol caps (Everest 146) apply regardless of `pact_wire`.

---

## §8 | Falsifiability

### §8.1 | Published supported sets

Counterparties verify `pact_wire` is in `supported_pact_wires` before digest check. Mismatch is independently observable without trusting operator prose.

### §8.2 | Golden corpus

The repo maintains four tuples: v0-stub/v0-stub, v1/v0-stub, v1/v1, v0-stub/v1. Each asserts expected `equality_bit` and absence of score fields in verifier output.

### §8.3 | Counterexample

A falsifying observation: same `session_nonce` and `counterparty_id`, two envelopes with different `pact_wire` labels, both accepted with conflicting `equality_bit` values, without a documented wire migration record between them.

### §8.4 | Error code registry

| Code | Meaning |
| --- | --- |
| `unsupported_pact_version` | `bridge_pact_accepted` returned false |
| `pact_digest_mismatch` | Recomputed digest differs |
| `pact_equality_bit_invalid` | Bit not in `{0, 1}` |
| `pact_proof_bytes_invalid` | Missing or malformed hex proof |

---

## §9 | Reference implementation and gates

| Artifact | Path |
| --- | --- |
| Canonical spec (this file) | [`ZKAC_PACT_VERSION_BRIDGE_v0.md`](ZKAC_PACT_VERSION_BRIDGE_v0.md) |
| Everest narrative | [`everests/everest_136_pact_version_bridging.md`](everests/everest_136_pact_version_bridging.md) |
| Shared bridging rules (135 to 138) | [`ZKAC_VERSION_BRIDGING_v0.md`](ZKAC_VERSION_BRIDGING_v0.md) §2 |
| `pact_session_digest` | `~/CredexAI/calm_witness/zkac_envelope.py` |
| `bridge_pact_accepted` | `~/CredexAI/calm_witness/version_bridge.py` |
| Everest 136 gate | `~/CredexAI/scripts/everest_136_zkac_pact_version_bridge_gate.py` |

---

## §10 | Acceptance checklist

1. v1 minter envelope verifies on v0-stub counterparty within 180-day window.
2. `pact_digest` recomputation includes correct `pact_wire`.
3. `equality_bit` semantics unchanged across wires; no false bit on version mismatch.
4. Unknown `pact_wire` returns `unsupported_pact_version`.
5. Scope forfeits, employment/credit prohibition, and anti-purity-test rules documented; no similarity score outputs.
6. Golden corpus and gate exit 0.

---

Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

**One-line result:** Everest 136 Pact version bridging is BAGGED; `pact_wire` N/N-1 window locks `equality_bit` semantics and rejects unknown wires with `unsupported_pact_version`, not a false bit.
