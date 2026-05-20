# Calm Witness — Inter-Agent Wire Format v0 (RFC)

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 99 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**
**Reference impl:** [`~/CredexAI/calm_witness/wire.py`](../../CredexAI/calm_witness/wire.py)

## §0 — Status

Draft. Open for cross-language review. Comments via PR to this repository.

## §1 — Scope

This RFC specifies the **on-the-wire JSON encoding** for the two top-level message types Calm Witness counterparties exchange:

1. `DisclosureRequest` — a counterparty asks the operator to disclose one or more predicate bits.
2. `DisclosureEnvelope` — the operator responds with a signed envelope containing the disclosed bits and their ZK proofs.

Plus the building blocks they embed:

- `PredicateDisclosure` — one (predicate_id, commitment, proof) tuple.
- `BitProof` — the Σ-protocol disjunction proof of a bit-commitment (per Everest 65).

The wire format is what makes implementations in Python (Everest 82), Rust (Everest 81), WASM/JS (Everest 83), and any future language **interoperable bit-for-bit**. Two implementations using this spec must produce byte-identical encodings for the same message and accept each other's bytes without modification.

## §2 — Wire version

```
wire_version = "calm-witness/wire/v0"
```

Every top-level message carries `wire_version` as the first sorted field. The version is bumped only on breaking changes (semantic-version semantics: 1.x compatible additive changes stay on `v1`; semantic divergence forces `v2`).

Implementations MUST reject messages with an unknown `wire_version`.

## §3 — Canonical encoding

All Calm Witness JSON is **canonical**:

- UTF-8.
- Sorted object keys (lexicographic by codepoint).
- Compact separators: `","` between items, `":"` between key and value. No surrounding whitespace.
- No trailing whitespace, no comments, no trailing newline.
- All integers serialized in lowercase hex with `"0x"`-less form (`"deadbeef"`, not `"0xDEADBEEF"`) **only when the field is a Pedersen-group element, an integer modulo p, or a Σ-protocol component**. Everything else uses standard JSON number encoding.

Two implementations producing two `canonical_json(obj)` strings for the same object MUST produce identical bytes. Any deviation is a bug in the implementation, not in the format.

## §4 — `BitProof`

The Σ-protocol disjunction proof per Everest 65. Six group-element / scalar fields plus the claimed bit:

```json
{
  "a0": "<hex>",
  "a1": "<hex>",
  "e0": "<hex>",
  "e1": "<hex>",
  "z0": "<hex>",
  "z1": "<hex>",
  "claimed_bit": 0 | 1
}
```

The fields `a0, a1` are group elements in `(Z/pZ)*` (RFC 3526 MODP-2048 for v0). The fields `e0, e1, z0, z1` are scalars in `Z/qZ`. `claimed_bit` is the bit the proof asserts (0 or 1).

A verifier computes:
- `e = SHA-256(c || a0 || a1) mod q` (Fiat-Shamir)
- Check `e0 + e1 ≡ e (mod q)`
- Check `h^z0 ≡ a0 · c^e0 (mod p)`
- Check `h^z1 ≡ a1 · (c · g⁻¹)^e1 (mod p)`

The big-endian length-prefixed integer encoding used in the Fiat-Shamir hash is defined in [`~/CredexAI/calm_witness/zk.py`](../../CredexAI/calm_witness/zk.py) `_hash_challenge`. Implementations MUST match it byte-for-byte.

## §5 — `PredicateDisclosure`

One predicate's contribution to an envelope:

```json
{
  "predicate_id": "cwp.v0.in_baseline_24h",
  "commitment_hex": "<hex>",
  "proof": { ... BitProof ... }
}
```

`predicate_id` MUST match a published entry in the predicate vocabulary (Everest 6). The `commitment_hex` is the Pedersen commitment value, hex-encoded.

## §6 — `DisclosureRequest`

A counterparty's signed request:

```json
{
  "wire_version": "calm-witness/wire/v0",
  "kind": "DisclosureRequest",
  "counterparty_id": "<string>",
  "session_nonce": "<string>",
  "requested_predicate_ids": ["cwp.v0.in_baseline_24h", ...],
  "chain_head_at_request": "<64-hex>",
  "freshness_window_seconds": <int>,
  "counterparty_signature": "<string, opaque to format>"
}
```

`counterparty_id` and `counterparty_signature` are coordinated with the CredexAI identity layer (Everest 22). The `request_digest` (SHA-256 of canonical-JSON minus the signature) is what an operator binds into its envelope.

## §7 — `DisclosureEnvelope`

The operator's response:

```json
{
  "wire_version": "calm-witness/wire/v0",
  "kind": "DisclosureEnvelope",
  "request_digest": "<64-hex>",
  "session_nonce": "<string>",
  "chain_head": "<64-hex>",
  "issued_at_iso": "<ISO 8601 timestamp>",
  "issued_by_operator": "<64-hex fingerprint of Ed25519 pubkey>",
  "disclosures": [ ... PredicateDisclosure ... ],
  "operator_signature": "ed25519:<hex>"
}
```

The `operator_signature` covers the canonical-JSON serialization of the envelope's content fields (everything except `operator_signature`). v0 uses Ed25519 (per Everest 68); the prefix `"ed25519:"` is required to allow future algorithm migration.

## §8 — Verification order

A receiving counterparty MUST verify, in this order:

1. `wire_version` matches the version this counterparty supports.
2. `kind == "DisclosureEnvelope"`.
3. `request_digest` matches `SHA-256(canonical_json(request_dict))`.
4. `session_nonce` matches the request's `session_nonce`.
5. Every disclosure's `predicate_id` is in the request's `requested_predicate_ids` (no smuggling).
6. Every disclosure's `proof` verifies against its `commitment_hex` per §4.
7. `operator_signature` verifies against the envelope digest using the operator's public key.

A failure at any step rejects the envelope. Implementations SHOULD return a structured `reasons` list so the counterparty can log specifically what failed.

## §9 — Forward-compatibility rules

- New top-level fields MAY be added in v0 if their absence does not change semantics. Implementations MUST ignore unknown fields.
- New predicate IDs MAY be added to the registry without bumping `wire_version` — predicate IDs are the namespacing mechanism.
- Any change to the canonical-JSON encoding, the hashing rule, or the verification order requires bumping to `wire_version = "calm-witness/wire/v1"`.

## §10 — Cross-language conformance

A second-implementation conformance test suite ships under `~/CredexAI/calm_witness/test_wire_cli.py`. Every alternative implementation (Rust, JS, Go, etc.) is expected to:

- Round-trip every test vector through encode → decode → re-encode and produce byte-identical output.
- Verify a Python-produced envelope and reject the same mutations the Python verifier rejects.
- Produce envelopes that the Python verifier accepts.

The Calm Witness reference verifier — Python today, Rust on Everest 81 landing — is the authoritative implementation for resolving any encoding-edge ambiguity.

## §11 — Test vectors

The reference test vectors live in `~/CredexAI/calm_witness/test_wire_cli.py`. Each vector is a `(message_object, canonical_bytes_expected)` pair. Implementations under conformance review are run against the same vectors.

For v1, conformance vectors will be hosted at a public URL and a multi-implementation interop matrix will be published.

## §12 — Versioning + deprecation

The wire format follows the [Predicate Vocabulary v0 ID-stability rules](PREDICATE_VOCABULARY_v0.md#2--id-format-and-stability-rules) as inspiration:

- `calm-witness/wire/v0` is permanent. Its semantics never change after publication.
- Breaking changes mint `calm-witness/wire/v1`. v0 remains in the registry forever; verifiers MUST continue to accept v0 envelopes for as long as v0 keys are in active rotation.
- Implementations MAY emit a warning when handling deprecated versions but MUST NOT reject for deprecation alone.

— Calm, 2026-05-20
