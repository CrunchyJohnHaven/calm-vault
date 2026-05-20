# ZKAC Counterparty SDK v0

**Everest 128 · 2026-05-20 · Calm**
**Verify-only counterparty SDKs: Go, JavaScript/TypeScript**
**Python reference:** `~/CredexAI/calm_witness/zkac_verify.py::verify_zkac`

## Status

**DESIGN-BAGGED (Summit 128/300) 2026-05-20**

Specification, conformance vectors, Python reference verifier, and a minimal JavaScript composite stub ship in this bag. Full Go package and production-grade JS npm module are follow-through for Everest 129 integration. Gate: `~/CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py` exit 0.

Normative detail lives in [`ZKAC_COUNTERPARTY_SDK_SPEC_v0.md`](ZKAC_COUNTERPARTY_SDK_SPEC_v0.md). This document is the counterparty-facing API surface and parity contract.

## Scope

Counterparty SDKs verify ZKAC envelopes only. They do not mint proofs, hold operator keys, or send data to third-party services.

Supported envelope kinds:

| Kind | Wire version | Python entry |
| --- | --- | --- |
| `DisclosureEnvelope` | `calm-witness/wire/v0` | `verify_zkac` → Witness path |
| `CompositeEnvelope` | `zkac-stack/envelope/v0` | `verify_zkac` → composite path |

Wire formats: [`CALM_WITNESS_WIRE_FORMAT_v0.md`](CALM_WITNESS_WIRE_FORMAT_v0.md), [`ZKAC_CROSS_PRIMITIVE_ENVELOPE_v0.md`](ZKAC_CROSS_PRIMITIVE_ENVELOPE_v0.md).

## Public API surface

### Python reference (authoritative)

```python
from calm_witness.zkac_verify import verify_zkac, verify_zkac_json, ZkacVerificationResult

result = verify_zkac(envelope_dict, request=request_dict)
result = verify_zkac_json(envelope_json, request_json=request_json)
```

`ZkacVerificationResult` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `ok` | `bool` | All checks passed |
| `envelope_kind` | `str` | `DisclosureEnvelope` or `CompositeEnvelope` |
| `pact_equality_bit` | `0 \| 1 \| None` | Present only for composite with pact section |
| `witness_bits` | `dict[str, int]` | Predicate ID → claimed bit |
| `compass_bits` | `dict[str, int]` | Compass predicate ID → claimed bit |
| `reasons` | `tuple[str, ...]` | Diagnostic failures (empty when `ok`) |

Optional `operator_verifying_fn(payload_bytes, sig_string) -> bool` skips or enforces Ed25519 operator signature verification.

### Go SDK (DESIGN-BAGGED)

Package path (planned): `github.com/calmwitness/zkac/counterparty`.

```go
type VerificationResult struct {
    OK              bool
    EnvelopeKind    string
    PactEqualityBit *int
    WitnessBits     map[string]int
    CompassBits     map[string]int
    Reasons         []string
}

func Verify(envelopeJSON, requestJSON string, operatorVerifyingFn func([]byte, string) bool) VerificationResult
func VerifyWitnessOnly(envelopeJSON, requestJSON string, operatorVerifyingFn func([]byte, string) bool) VerificationResult
func VerifyComposite(envelopeJSON, requestJSON string, operatorVerifyingFn func([]byte, string) bool) VerificationResult
```

Follow-through: implement under `~/CredexAI/calm_witness/sdk-go/` using the same conformance vectors as Python before any registry publish.

### JavaScript / TypeScript SDK

Shipped stub (composite pact section only): `~/CredexAI/calm_witness/sdk-js/verify_envelope.mjs`.

Production surface (specified; full package follow-through):

```typescript
export interface VerificationResult {
  ok: boolean;
  envelope_kind: string;
  pact_equality_bit?: 0 | 1;
  witness_bits: Record<string, 0 | 1>;
  compass_bits: Record<string, 0 | 1>;
  reasons: string[];
}

export interface ZkacClient {
  verify(envelopeJSON: string, requestJSON?: string | null, operatorVerifyingFn?: (payload: Uint8Array, sig: string) => boolean): VerificationResult;
  verifyWitnessOnly(...): VerificationResult;
  verifyComposite(...): VerificationResult;
}

export function createClient(): ZkacClient;
```

## verify_zkac parity rules

Go and JS implementations MUST match Python reference semantics on every conformance vector in `~/CredexAI/calm_witness/schema/conformance/counterparty_sdk_v0.json`.

| Check | Parity requirement |
| --- | --- |
| Dispatch | `kind` selects Witness vs composite path (same as Python `_detect_envelope_kind`) |
| Wire version | Reject unknown versions before proof work |
| Request digest | `SHA-256(canonical_json(request_fields))` must match envelope |
| Session nonce | Must match request when request is supplied |
| Predicate smuggling | Disclosed IDs ⊆ requested IDs (Witness) or section lists (composite) |
| Bit proofs | Fiat-Shamir + MODP-2048 checks per wire spec §4 |
| Operator signature | Optional callback; never log payload bytes |
| Result shape | Same keys and bit maps as `ZkacVerificationResult` |

Reason strings may differ in prefix wording (`predicate_id_not_requested` vs `unrequested_predicate`) but MUST encode the same failure class. Conformance gate accepts substring match on keywords listed per vector.

Canonical JSON: sorted keys, compact separators, lowercase hex, UTF-8. Match `~/CredexAI/calm_witness/wire.py::canonical_json`.

## No PII in logs

Mandatory for all SDK languages:

1. **Never** log envelope JSON, request JSON, proof fields, commitments, or operator signatures.
2. **Never** ship telemetry, APM, or analytics to third-party SaaS.
3. **May** log predicate IDs, envelope kind, wire version, and reason strings (no hex payloads).
4. **May** write diagnostics to operator-controlled local files or syslog only.
5. Default logging level for verification failures: one line per rejection with reason keywords only.

Rationale: envelopes can imply sensitive predicate values. Self-hosted verification only.

## Conformance vectors

Location: `~/CredexAI/calm_witness/schema/conformance/counterparty_sdk_v0.json`

Six vectors cover Witness structure, smuggling, nonce mismatch, composite pact+witness, and unknown wire version. Gate runs Python `verify_zkac` and JS composite stub against applicable vectors.

Legacy copy: `~/CredexAI/calm_witness/schema/test_vectors_e128.json` (same content; prefer `schema/conformance/` path).

## Acceptance (Everest 128)

**PASS (design bag):**

- [x] `ZKAC_COUNTERPARTY_SDK_v0.md` published (this file)
- [x] Python `verify_zkac` reference exports stable result type
- [x] Conformance vectors under `schema/conformance/`
- [x] Gate exit 0
- [x] JS composite stub matches Python on pact vectors
- [x] No PII logging policy documented

**Follow-through (Everest 129+):**

- [ ] Go package with full Witness + composite verify
- [ ] JS npm module with `verifyWitnessOnly` and bit-proof verification
- [ ] Byte-identical canonical JSON tests vs Python

---

**Gate:** `~/CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py`

**Musk tagline:** *Software always works. The trick is shipping it.*

— Calm, 2026-05-20
