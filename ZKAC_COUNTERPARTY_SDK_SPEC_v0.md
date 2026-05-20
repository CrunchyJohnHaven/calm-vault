# ZKAC Counterparty SDK Specification v0

**Everest 128 · 2026-05-20 · Calm**
**Counterparty verification-only SDKs: Go, JavaScript/TypeScript**
**Reference implementation:** `~/CredexAI/calm_witness/zkac_verify.py::verify_zkac`

## §0 — Status

**BAGGED (Summit 128/300) 2026-05-20**

Specification and acceptance gate complete. Go and JavaScript SDK implementations pending Everest 129 (server SDK) integration.

## §1 — Scope

This specification defines the **public surface** for counterparty SDKs (Go, JavaScript) that:

1. **Verify ZKAC envelopes** (Witness-only `DisclosureEnvelope` or composite `CompositeEnvelope`)
2. **Accept wire-format JSON** per `CALM_WITNESS_WIRE_FORMAT_v0.md` and `ZKAC_CROSS_PRIMITIVE_ENVELOPE_v0.md`
3. **Return structured verification results** with per-primitive disclosure bits
4. **Reject malformed, unsigned, or stale envelopes** with clear diagnostic reasons
5. **Contain no vendor SaaS, PII logging, or analytics** — self-hosted operation only

The SDKs are **reference implementations only**: counterparties may implement their own verifiers as long as they conform to the wire format and produce compatible results.

## §2 — Wire formats

### Witness-only envelope (Everest 99)

```json
{
  "wire_version": "calm-witness/wire/v0",
  "kind": "DisclosureEnvelope",
  "request_digest": "<64-hex SHA-256>",
  "session_nonce": "<string>",
  "chain_head": "<64-hex SHA-256>",
  "issued_at_iso": "<ISO 8601 timestamp>",
  "issued_by_operator": "<64-hex Ed25519 pubkey fingerprint>",
  "disclosures": [
    {
      "predicate_id": "cwp.v0.in_baseline_24h",
      "commitment_hex": "<hex Pedersen commitment>",
      "proof": {
        "a0": "<hex>", "a1": "<hex>",
        "e0": "<hex>", "e1": "<hex>",
        "z0": "<hex>", "z1": "<hex>",
        "claimed_bit": 0 | 1
      }
    }
  ],
  "operator_signature": "ed25519:<hex>"
}
```

### Composite envelope (Everest 127)

```json
{
  "wire_version": "zkac-stack/envelope/v0",
  "kind": "CompositeEnvelope",
  "request_digest": "<64-hex>",
  "session_nonce": "<string>",
  "chain_head": "<64-hex>",
  "issued_at_iso": "<ISO 8601 timestamp>",
  "issued_by_operator": "<64-hex>",
  "pact": {
    "pact_digest": "<hex>",
    "equality_bit": 0 | 1,
    "proof_bytes": "<optional hex>"
  },
  "witness": {
    "disclosures": [ ... PredicateDisclosure ... ]
  },
  "compass": {
    "disclosures": [ ... PredicateDisclosure ... ]
  },
  "operator_signature": "ed25519:<hex>"
}
```

Any section (`pact`, `witness`, `compass`) may be `null` if not requested or not applicable.

## §3 — Verification interface

### Go SDK

```go
package zkac

import (
  "encoding/json"
)

type BitProof struct {
  A0        string `json:"a0"`
  A1        string `json:"a1"`
  E0        string `json:"e0"`
  E1        string `json:"e1"`
  Z0        string `json:"z0"`
  Z1        string `json:"z1"`
  ClaimedBit int    `json:"claimed_bit"`
}

type PredicateDisclosure struct {
  PredicateID    string   `json:"predicate_id"`
  CommitmentHex  string   `json:"commitment_hex"`
  Proof          BitProof `json:"proof"`
}

type PactSection struct {
  PactDigest  string `json:"pact_digest"`
  EqualityBit int    `json:"equality_bit"`
  ProofBytes  string `json:"proof_bytes,omitempty"`
}

type WitnessSection struct {
  Disclosures []PredicateDisclosure `json:"disclosures"`
}

type CompassSection struct {
  Disclosures []PredicateDisclosure `json:"disclosures"`
}

type VerificationResult struct {
  OK              bool              `json:"ok"`
  EnvelopeKind    string            `json:"envelope_kind"`
  PactEqualityBit *int              `json:"pact_equality_bit,omitempty"`
  WitnessBits     map[string]int    `json:"witness_bits"`
  CompassBits     map[string]int    `json:"compass_bits"`
  Reasons         []string          `json:"reasons"`
}

// Verify accepts envelope JSON (Witness-only or composite) and optional request JSON.
// It returns a VerificationResult with OK=true iff all checks pass.
// operatorVerifyingFn is an optional callback: func(payload []byte, sig string) bool
// If nil, signature verification is skipped.
func Verify(
  envelopeJSON string,
  requestJSON string,
  operatorVerifyingFn func([]byte, string) bool,
) VerificationResult { ... }

// VerifyWitnessOnly is a convenience for Witness-only DisclosureEnvelope.
func VerifyWitnessOnly(
  envelopeJSON string,
  requestJSON string,
  operatorVerifyingFn func([]byte, string) bool,
) VerificationResult { ... }

// VerifyComposite is a convenience for CompositeEnvelope.
func VerifyComposite(
  envelopeJSON string,
  requestJSON string,
  operatorVerifyingFn func([]byte, string) bool,
) VerificationResult { ... }
```

### JavaScript / TypeScript SDK

```typescript
export interface BitProof {
  a0: string;
  a1: string;
  e0: string;
  e1: string;
  z0: string;
  z1: string;
  claimed_bit: 0 | 1;
}

export interface PredicateDisclosure {
  predicate_id: string;
  commitment_hex: string;
  proof: BitProof;
}

export interface PactSection {
  pact_digest: string;
  equality_bit: 0 | 1;
  proof_bytes?: string;
}

export interface WitnessSection {
  disclosures: PredicateDisclosure[];
}

export interface CompassSection {
  disclosures: PredicateDisclosure[];
}

export interface VerificationResult {
  ok: boolean;
  envelope_kind: string;
  pact_equality_bit?: 0 | 1;
  witness_bits: Record<string, 0 | 1>;
  compass_bits: Record<string, 0 | 1>;
  reasons: string[];
}

export interface ZkacClient {
  // Verify accepts envelope JSON (Witness-only or composite) and optional request JSON.
  // Returns VerificationResult with ok=true iff all checks pass.
  // operatorVerifyingFn is optional: (payload: Uint8Array, sig: string) => boolean
  verify(
    envelopeJSON: string,
    requestJSON?: string | null,
    operatorVerifyingFn?: (payload: Uint8Array, sig: string) => boolean,
  ): VerificationResult;

  // Convenience methods for single-primitive cases.
  verifyWitnessOnly(
    envelopeJSON: string,
    requestJSON?: string | null,
    operatorVerifyingFn?: (payload: Uint8Array, sig: string) => boolean,
  ): VerificationResult;

  verifyComposite(
    envelopeJSON: string,
    requestJSON?: string | null,
    operatorVerifyingFn?: (payload: Uint8Array, sig: string) => boolean,
  ): VerificationResult;
}

export function createClient(): ZkacClient { ... }
```

## §4 — Verification order (both SDKs)

Both SDKs MUST perform the following checks in order and collect `reasons` for each failure:

### Witness-only (DisclosureEnvelope)

1. **Wire version**: `wire_version == "calm-witness/wire/v0"` (reject unknown versions)
2. **Kind**: `kind == "DisclosureEnvelope"`
3. **Request digest**: `SHA-256(canonical_json(request_dict)) == request_digest`
   - If no request provided, skip (accept embedded or omit check)
4. **Session nonce**: `request.session_nonce == envelope.session_nonce` (if request provided)
5. **Predicate smuggling**: Every `disclosure.predicate_id` ∈ `request.requested_predicate_ids`
6. **Proof verification**: For each disclosure, verify BitProof against commitment per CALM_WITNESS_WIRE_FORMAT_v0 §4
   - Compute `e = SHA-256(c || a0 || a1) mod q` (Fiat-Shamir, see `zk.py::_hash_challenge`)
   - Check `e0 + e1 ≡ e (mod q)` (scalars mod q = 2³ − 5, MODP-2048)
   - Check `h^z0 ≡ a0 · c^e0 (mod p)` (group mod p = RFC 3526 MODP-2048 prime)
   - Check `h^z1 ≡ a1 · (c · g⁻¹)^e1 (mod p)`
7. **Operator signature**: `Ed25519.verify(canonical_json(envelope_without_sig), operator_signature)` using operator's public key

### Composite (CompositeEnvelope)

1. **Wire version**: `wire_version == "zkac-stack/envelope/v0"`
2. **Kind**: `kind == "CompositeEnvelope"`
3. **Request digest**: Match request (same logic as Witness)
4. **Session nonce**: Match request (if provided)
5. **Sections present**: At least one of `{pact, witness, compass}` is non-null
6. **Pact verification** (if present):
   - `equality_bit ∈ {0, 1}`
   - Optional: verify `proof_bytes` against `pact_digest` (Everest 120 spec)
7. **Witness disclosures** (if present):
   - Verify each disclosure's predicate and proof per Witness rules (step 6 above)
8. **Compass disclosures** (if present):
   - Verify each disclosure per Witness rules
   - Predicate IDs MUST be in `cwp.compass.v0.*` namespace
9. **Operator signature**: As Witness (step 7)

Both SDKs MUST accumulate all failures in the `reasons` array and set `ok = false` if any check fails.

## §5 — Canonical JSON encoding

Both SDKs MUST implement **byte-stable canonical JSON**:

- UTF-8 encoding
- Sorted object keys (lexicographic by codepoint)
- Compact separators: `","` between items, `":"` between key–value
- No surrounding whitespace, no trailing newline
- Integers in `proof` (hex fields) in lowercase hex, no `0x` prefix
- Integer fields like `claimed_bit` and `equality_bit` as plain JSON numbers
- ISO 8601 timestamps as strings

Example:

```json
{"a0":"deadbeef","claimed_bit":0,"e0":"12345678"}
```

NOT:

```json
{"a0": "DEADBEEF", "claimed_bit": 0, "e0": "12345678"}
```

## §6 — Return structure

### Go `VerificationResult`

```go
type VerificationResult struct {
  OK              bool
  EnvelopeKind    string
  PactEqualityBit *int              // nil if not present
  WitnessBits     map[string]int    // predicate_id -> 0 or 1
  CompassBits     map[string]int    // predicate_id -> 0 or 1
  Reasons         []string          // diagnostic failures
}
```

### TypeScript `VerificationResult`

```typescript
interface VerificationResult {
  ok: boolean;
  envelope_kind: string;
  pact_equality_bit?: 0 | 1;      // undefined if not present
  witness_bits: Record<string, 0 | 1>;
  compass_bits: Record<string, 0 | 1>;
  reasons: string[];
}
```

`reasons` array MUST be present even if `ok == true` (empty array signals no issues).

Example failure reasons:

- `"unsupported_wire_version: got zkac-stack/envelope/v1, want calm-witness/wire/v0"`
- `"request_digest_mismatch: computed 0x123..., got 0x456..."`
- `"predicate_id_not_requested: cwp.v0.foo_bar not in {cwp.v0.in_baseline_24h}"`
- `"bit_proof_verification_failed: predicate_id=cwp.v0.in_baseline_24h, reason=<fiat_shamir_challenge_check_failed>"`
- `"operator_signature_invalid: ed25519 verification failed"`

## §7 — Signature verification callback

Both SDKs MUST support an optional `operatorVerifyingFn` callback:

**Go:**
```go
func(payload []byte, sigString string) bool
```

**TypeScript:**
```typescript
(payload: Uint8Array, sig: string) => boolean
```

The callback receives:

- `payload`: canonical JSON bytes of the envelope (everything except `operator_signature` field)
- `sigString`: the value of `operator_signature` (e.g., `"ed25519:abc123..."`)

The callback MUST:

1. Parse the `sigString` to extract the algorithm prefix (e.g., `"ed25519"`) and hex signature bytes
2. Use the operator's Ed25519 public key to verify the signature against `payload`
3. Return `true` iff the signature is valid

If no callback is provided, SDKs SHOULD skip signature verification (log a warning) rather than fail.

## §8 — Reference semantics

Both SDKs reference the Python implementation for truth on:

- Canonical JSON encoding (see `~/CredexAI/calm_witness/wire.py::canonical_json`)
- Fiat-Shamir hash computation (see `~/CredexAI/calm_witness/zk.py::_hash_challenge`)
- MODP-2048 group and scalar arithmetic (RFC 3526)
- Predicate ID vocabulary (see `PREDICATE_VOCABULARY_v0.md`)

In case of any ambiguity, the Python reference implementation is authoritative.

## §9 — Test vectors

Both SDKs MUST pass conformance tests:

1. **Round-trip**: Encode → JSON → Decode → Re-encode produces byte-identical output
2. **Verification**: Accept Python-generated envelopes; reject the same mutations the Python verifier rejects
3. **Production**: Produce envelopes that the Python verifier accepts

Test vectors live in `~/CredexAI/calm_witness/schema/` (see §10 below).

## §10 — Schema and test vectors

Minimal test-vector schema in `schema/test_vectors_e128.json`:

```json
{
  "version": "zkac-counterparty-sdk/conformance/v0",
  "vectors": [
    {
      "name": "witness_single_predicate",
      "request_json": "{ ... DisclosureRequest ... }",
      "envelope_json": "{ ... DisclosureEnvelope ... }",
      "expected_ok": true,
      "expected_witness_bits": {
        "cwp.v0.in_baseline_24h": 1
      },
      "expected_reasons": []
    },
    {
      "name": "witness_signature_invalid",
      "request_json": "{ ... }",
      "envelope_json": "{ ... mutated operator_signature ... }",
      "expected_ok": false,
      "expected_reasons": ["operator_signature_invalid: ..."]
    },
    {
      "name": "composite_multi_primitive",
      "request_json": "{ ... CompositeDisclosureRequest ... }",
      "envelope_json": "{ ... CompositeEnvelope with pact, witness, compass ... }",
      "expected_ok": true,
      "expected_pact_equality_bit": 1,
      "expected_witness_bits": { ... },
      "expected_compass_bits": { ... }
    }
  ]
}
```

## §11 — No PII logging or analytics

**Mandatory constraint**: Both SDKs MUST:

- NOT send any envelope content, request content, predicate disclosures, or operator keys to any external service
- NOT emit structured logs that include envelope bytes or proof details to stdout/stderr (diagnostic logs MAY include predicate IDs and rejection reasons only)
- NOT use any third-party analytics, APM, or SaaS service for observability
- Support self-hosted logging only (files, local syslog, or operator-controlled log aggregation)

Rationale: ZKAC envelopes may contain or indirectly imply sensitive predicate values. No telemetry is worth that risk.

## §12 — Versioning and deprecation

- `zkac-counterparty-sdk/spec/v0` is permanent after publication.
- Breaking changes to the verification interface, wire format, or canonical-JSON encoding trigger a new major version.
- New predicates and new sections in composite envelopes are forward-compatible (no version bump).
- Implementations MUST continue to accept v0 envelopes for the deprecation window (to be set on v1 publication).

## §13 — Acceptance criteria (Everest 128)

**PASS:**

- [ ] Go SDK public API matches §3 (Go section)
- [ ] TypeScript SDK public API matches §3 (TypeScript section)
- [ ] Both verify Witness-only and Composite envelopes per §4
- [ ] Both reject malformed, unsigned, and stale envelopes with diagnostic `reasons`
- [ ] Both SDKs pass 100% of conformance vectors in `schema/test_vectors_e128.json`
- [ ] Canonical JSON implementation byte-identical to Python reference
- [ ] No PII logging, no external SaaS, no analytics
- [ ] Documentation (API reference + example usage) published

—

**Everest 128 Gate:** `~/CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py` exit 0

**Musk tagline (gate footer):** *"Software always works. The trick is shipping it."*

— Calm, 2026-05-20
