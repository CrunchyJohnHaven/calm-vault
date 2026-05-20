# Everest 29 — Genesis Block & Provenance

*Phase III — Self-Report Substrate. Prereq: Everest 28.*

## Overview

Every Calm Witness chain has exactly one **Genesis Record** (seq=0, kind: "genesis"). The genesis record locks three bindings at the moment of vault creation:

1. **Principal-identity binding** — the legal name of the principal, committed via Pedersen (the name itself does not appear in the record).
2. **Operator-identity binding** — the software version, configuration, and CredexAI identity credential of the Calm operator.
3. **Protocol version** — the version of this specification (e.g., "0.1.0") and a hash of the protocol document itself at creation time.

Additionally, the genesis record anchors:
- **Enrollment ceremony artifacts** — the ceremony ID, witness attestations, and the set of biometric templates enrolled at that ceremony.
- **Vault identity** — a UUIDv4 unique to this vault instance, preventing confusion if a principal ever operates multiple vaults.
- **Future anchoring infrastructure** — identifiers for the Sigsum transparency log and Roughtime verifiable-clock servers that will anchor this vault's chain heads.

## The retroactive-migration case

The current live vault (`~/.calm-vault/user_state.jsonl`) contains 8 records (seq=1–8 as of 2026-05-20) that were bootstrapped under v0 protocol **without** a seq=0 genesis record. To maintain chain continuity while documenting provenance retroactively, this Everest introduces a **kind: "genesis.retroactive"** record mechanism:

1. The existing chain from seq=1 forward remains unchanged and valid.
2. A new **kind: "genesis.retroactive"** record is appended (as seq=9 or higher, following the existing prev_hash chain).
3. This retroactive record contains all the genesis payload fields that **would have been** written at vault creation time.
4. Verifiers reading the chain from seq=1 forward see no structural break.
5. Verifiers checking provenance read the genesis.retroactive record to recover protocol version, principal/operator bindings, and enrollment ceremony context.

This approach trades off raw cryptographic strength (a real seq=0 genesis is stronger) for **non-destructive migration**. Forward-deployed vaults (created after this Everest ships) must write a real seq=0 genesis at vault bootstrap; only legacy vaults use the retroactive form.

## Genesis Record Schema (kind: "genesis", seq: 0)

```json
{
  "seq": 0,
  "ts": "2026-05-20T10:15:00-04:00",
  "ts_source": "ceremony_local_clock",
  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "kind": "genesis",
  "payload": {
    "protocol_version": "0.1.0",
    "protocol_spec_hash": "04972dbdeff0f8bc1cb91c02c6b217b724c48514ead66cda5ed3b43b94bce7c1",
    "principal": {
      "legal_name_commitment": "pedersen:7a2f9b1c8e3d5f2a9b4c7e1f3a5c8d0e",
      "credexai_vc_id": "vc:credexai:john-bradley:2026-05-20:abc123def",
      "jurisdiction": "US"
    },
    "operator": {
      "operator_name": "CALM",
      "operator_credexai_vc_id": "vc:credexai:calm-op:2026-05-20:xyz789uvw",
      "operator_sw_version": "calm-witness 0.1.0",
      "operator_sw_hash": "b1e5f3d0a7c2f4e9b6d1a8f3c5e7a0d2"
    },
    "vault": {
      "vault_uuid": "550e8400-e29b-41d4-a716-446655440000",
      "vault_path_hash": "abc1234567890fedcba0987654321abc",
      "master_pub_fingerprint": "5f8e3d1f7c2b9a4e6d0f1c8a3b5e7f0a"
    },
    "ceremony": {
      "ceremony_id": "enrollment_ceremony:2026-05-20:ceremony_001",
      "ceremony_attestation_hash": "3e1f9c2a7d4b6e8f0a1c3d5f7b9e1f3a",
      "witness_attestations_root": "merkle_root_sha256:2f7a1b5c9e3f0d6a8c1e4f7b9a2d5c7e"
    },
    "anchors": {
      "sigsum_log_id": "sigsum-log-poc:credex",
      "roughtime_servers": [
        "roughtime.cloudflare.com",
        "roughtime.int08h.com",
        "roughtime.ntp.org"
      ]
    },
    "extension_field": null
  },
  "operator_sig": "ed25519_sig:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d",
  "principal_sig": "ed25519_sig:abcdef0123456789fedcba9876543210",
  "record_hash": "sha256:0123456789abcdef0123456789abcdef"
}
```

## Field specifications

### Top-level fields

| Field | Type | Notes |
|---|---|---|
| `seq` | int | Must be 0 for genesis. Increments by 1 for all subsequent records. |
| `ts` | ISO 8601 string | Moment of vault creation, with timezone (e.g., `-04:00` for EDT). MUST be before or equal to ts of seq=1. |
| `ts_source` | enum | One of: `"ceremony_local_clock"` (human-local time at enrollment), `"ceremony_witness_attested"` (witnessed and signed by a notary), `"roughtime_anchored"` (anchored post-hoc to Roughtime). For v0, typically `ceremony_local_clock`. |
| `prev_hash` | string | Exactly 64 hex zeros (`"0" * 64`). Explicit genesis anchor. |
| `kind` | string | Exactly `"genesis"`. |
| `payload` | object | See below. |
| `operator_sig` | string | Ed25519 signature by the operator's private key over the canonical serialization of all fields EXCEPT `operator_sig`, `principal_sig`, and `record_hash`. Binding: proof that the operator authored the genesis record. |
| `principal_sig` | string | Ed25519 signature by the principal's master.priv over the same canonical serialization. Binding: proof that the principal authorized this vault creation. |
| `record_hash` | string | SHA-256 (hex) of the canonical JSON of all fields EXCEPT `record_hash` itself (see Canonicalization rule below). |

### Payload fields

#### protocol_version (string, semver)
The protocol version at vault-creation time, e.g., `"0.1.0"`. This pins the semantics by which the chain was created. Future verifiers can use this to select the correct parser / verification logic.

#### protocol_spec_hash (string, hex)
SHA-256 hash of the canonical specification document (`ZKBB_USER_PROTOCOL_v0.md`) at the time the vault was created. Prevents later reinterpretation: if the spec document changes, a new hash is recorded in new vaults, and verifiers can detect which version of the spec was in effect.

#### principal (object)

| Field | Type | Notes |
|---|---|---|
| `legal_name_commitment` | string | A Pedersen commitment to the principal's legal name. Format: `"pedersen:<pedersen_commitment_hex>"`. The name itself does NOT appear in this record; only the commitment. Prevents the genesis record from leaking PII. |
| `credexai_vc_id` | string | The CredexAI Verifiable Credential ID for the principal. Issued by CredexAI at enrollment (Everest 22). Format: `"vc:credexai:<principal_id>:<iso_date>:<random_suffix>"`. Binding: proof that CredexAI has verified the principal's legal identity. |
| `jurisdiction` | string | ISO 3166-1 alpha-2 country code (e.g., `"US"`, `"GB"`, `"DE"`) where the principal resides. Used by Everest 79 (Cross-Jurisdiction Legality Matrix) to determine applicable laws and consent requirements. |

#### operator (object)

| Field | Type | Notes |
|---|---|---|
| `operator_name` | string | E.g., `"CALM"`. Free-form identifier for the AI operator. |
| `operator_credexai_vc_id` | string | The CredexAI VC ID of the Calm operator. Issued at operator enrollment. Binding: proof that CredexAI has verified the operator's identity and authorization. |
| `operator_sw_version` | string | Semantic version of the operator software, e.g., `"calm-witness 0.1.0"`. |
| `operator_sw_hash` | string | SHA-256 hash (hex) of the operator's binary at creation time. Enables detection of operator-binary tampering after the fact. |

#### vault (object)

| Field | Type | Notes |
|---|---|---|
| `vault_uuid` | string | UUIDv4 generated at vault creation. Globally unique identifier for this vault instance. Prevents confusion if the principal ever creates multiple vaults. |
| `vault_path_hash` | string | SHA-256 hash (hex) of the canonicalized vault directory path (e.g., `/Users/johnbradley/.calm-vault`), NOT the path itself. Prevents leakage of filesystem locations in the genesis record while allowing verifiers to confirm this record belongs to a specific vault location they already know. |
| `master_pub_fingerprint` | string | SHA-256 hash (hex) of the master public key (`master.pub`). Binding: enables verifiers to confirm that the principal signatures in this record were made with the correct key. |

#### ceremony (object)

| Field | Type | Notes |
|---|---|---|
| `ceremony_id` | string | Reference to the enrollment ceremony (Everest 11) artifacts, e.g., `"enrollment_ceremony:2026-05-20:ceremony_001"`. Enables auditors to cross-reference enrollment ceremony documents (photos, witness signatures, ceremony script evidence). |
| `ceremony_attestation_hash` | string | SHA-256 hash (hex) of the canonical ceremony attestation document. Prevents post-hoc rewriting of what the ceremony was. |
| `witness_attestations_root` | string | Merkle root (as hex SHA-256) over all witness signatures from Everest 20 (Enrollment Witness Protocol). If no witnesses participated, this is the zero hash. |

#### anchors (object)

| Field | Type | Notes |
|---|---|---|
| `sigsum_log_id` | string | Identifier of the Sigsum transparency log to which this vault will publish its chain heads (Everest 30). E.g., `"sigsum-log-poc:credex"`. Allows verifiers to know in advance where to check for chain-head inclusion proofs. |
| `roughtime_servers` | array of strings | List of Roughtime server identifiers (domain names or server IDs) that will provide verifiable timestamps for chain heads (Everest 31). E.g., `["roughtime.cloudflare.com", "roughtime.int08h.com"]`. Allows verifiers to validate the freshness of chain-head timestamps without relying on the local clock. |

#### extension_field (null or object)
Reserved for future protocol versions. In v0, always `null`. In v1+, may contain version-specific extensions without breaking the v0 verifier.

## Canonicalization rule for record_hash

The `record_hash` is computed as follows:

1. **Create a copy of the record object.**
2. **Remove the `record_hash`, `operator_sig`, and `principal_sig` fields.**
3. **Serialize to JSON using:** `json.dumps(record, sort_keys=True, separators=(",", ":"))`
   - Sorted keys (alphabetical order).
   - No whitespace around separators.
   - UTF-8 encoding.
4. **Compute:** `record_hash = sha256_hex(canonical_bytes)`

The canonical serialization is the same algorithm used in Everest 28 (Hash-Chain Construction & Verification) and USER_STATE_PROTOCOL.md, ensuring byte-stability across Python, Rust, and other implementations.

## Signature rules

### Operator signature (operator_sig)

The operator signs the canonical JSON (without `operator_sig`, `principal_sig`, `record_hash`) using the operator's Ed25519 private key:

```python
canonical = json.dumps(record_minus_sigs, sort_keys=True, separators=(",", ":"))
operator_sig = nacl.signing.SigningKey(operator_priv).sign(canonical.encode()).signature.hex()
```

Verification: a Calm Witness verifier can verify this signature using the operator's public key (obtained from the CredexAI VC).

### Principal signature (principal_sig)

The principal signs the same canonical JSON using their master private key (master.priv):

```python
canonical = json.dumps(record_minus_sigs, sort_keys=True, separators=(",", ":"))
principal_sig = nacl.signing.SigningKey(principal_master_priv).sign(canonical.encode()).signature.hex()
```

Verification: a verifier can verify this signature using the principal's master public key (master.pub).

### Why two signatures

The dual-signature requirement prevents two categories of attack:

1. **Rogue operator attack:** An operator whose credentials are compromised cannot unilaterally create a "legitimate" genesis record binding a principal without the principal's key. The principal signature is proof of authorization.
2. **Principal-impersonation attack:** An attacker with access to the operator's key cannot forge a genesis record for a different principal without also having that principal's master key. The operator signature is proof of authorship.

Both signatures MUST verify for the genesis record to be accepted.

## Genesis record validation rules

The verifier (calm-witness verify-chain, with a new --check-genesis flag) applies these rules:

1. **Uniqueness:** The chain contains at most one record with kind matching `"genesis*"` (i.e., `"genesis"` or `"genesis.retroactive"`).
2. **Sequence:** If seq=0 record exists, it must be the first record in the chain. If no seq=0 record exists, the chain must contain a kind: "genesis.retroactive" record.
3. **Signature verification:**
   - Compute the canonical JSON (without sigs and record_hash).
   - Verify operator_sig against the operator's Ed25519 public key (from CredexAI VC).
   - Verify principal_sig against the principal's master.pub.
   - Both must verify for the genesis record to be accepted.
4. **Hash chain integrity:** Record_hash is consistent with the canonical JSON (same as Everest 28).
5. **prev_hash validation:** For seq=0, prev_hash must be exactly 64 hex zeros.
6. **Jurisdiction validation:** The jurisdiction code is a valid ISO 3166-1 alpha-2 code.

## Retroactive genesis (kind: "genesis.retroactive")

For legacy vaults that were created before this Everest shipped, a retroactive genesis record is appended as a normal JSONL line (following the hash chain, with appropriate prev_hash binding). The record is identical to a regular genesis record except:

- `kind = "genesis.retroactive"` (instead of `"genesis"`).
- `seq` is NOT 0; it appears at the logical point after all existing records, as part of the normal append sequence.
- **Acknowledged limitation:** Retroactive genesis records are cryptographically weaker than native seq=0 records. Counterparties verifying the chain may choose to downgrade their trust level accordingly (e.g., "this genesis was retroactively added" as a footnote in the disclosure bit).

### Retroactive migration for the current vault

The live vault at `~/.calm-vault/user_state.jsonl` was bootstrapped on 2026-05-20 at 10:20 UTC (seq=1) without a genesis record. To migrate it:

1. **Recover metadata:** Extract principal name, operator name, protocol version (0.1.0), and vault UUID from existing records and Calm operator configuration.
2. **Generate ceremonies artifacts:** Coordinate with Everest 11 (Enrollment Ceremony Spec) to retroactively document what the ceremony would have been (date, location, witness list, biometric templates).
3. **Construct the genesis.retroactive record:**
   - Set `seq` to the next available sequence number (seq=9 in the current chain as of 2026-05-20).
   - Set `kind = "genesis.retroactive"`.
   - Populate all payload fields as if the genesis were being written at vault creation (2026-05-20T10:15:00-04:00, for example).
   - Set `prev_hash` to the record_hash of the previous record (seq=8).
   - Compute operator and principal signatures over the canonical JSON.
   - Compute record_hash.
4. **Append to chain:** Write the genesis.retroactive record as a new line to user_state.jsonl.
5. **Verify integrity:** Run `calm-witness verify-chain --check-genesis` to confirm the entire chain validates.

## Example Genesis Record (canonical JSON)

Below is a concrete example of a genesis record as it would be serialized in the JSONL file. The record binds John Bradley (principal) to the CALM operator, protocol v0.1.0, vault UUID 550e8400-e29b-41d4-a716-446655440000, and enrollment ceremony 2026-05-20.

```json
{
  "kind": "genesis",
  "operator": {
    "operator_credexai_vc_id": "vc:credexai:calm-op:2026-05-20:xyz789uvw",
    "operator_name": "CALM",
    "operator_sw_hash": "b1e5f3d0a7c2f4e9b6d1a8f3c5e7a0d2",
    "operator_sw_version": "calm-witness 0.1.0"
  },
  "operator_sig": "ed25519_sig:operator_signature_hex_string_here",
  "payload": {
    "anchors": {
      "roughtime_servers": [
        "roughtime.cloudflare.com",
        "roughtime.int08h.com",
        "roughtime.ntp.org"
      ],
      "sigsum_log_id": "sigsum-log-poc:credex"
    },
    "ceremony": {
      "ceremony_attestation_hash": "3e1f9c2a7d4b6e8f0a1c3d5f7b9e1f3a",
      "ceremony_id": "enrollment_ceremony:2026-05-20:ceremony_001",
      "witness_attestations_root": "merkle_root_sha256:2f7a1b5c9e3f0d6a8c1e4f7b9a2d5c7e"
    },
    "extension_field": null,
    "operator": {
      "operator_credexai_vc_id": "vc:credexai:calm-op:2026-05-20:xyz789uvw",
      "operator_name": "CALM",
      "operator_sw_hash": "b1e5f3d0a7c2f4e9b6d1a8f3c5e7a0d2",
      "operator_sw_version": "calm-witness 0.1.0"
    },
    "principal": {
      "credexai_vc_id": "vc:credexai:john-bradley:2026-05-20:abc123def",
      "jurisdiction": "US",
      "legal_name_commitment": "pedersen:7a2f9b1c8e3d5f2a9b4c7e1f3a5c8d0e"
    },
    "protocol_spec_hash": "04972dbdeff0f8bc1cb91c02c6b217b724c48514ead66cda5ed3b43b94bce7c1",
    "protocol_version": "0.1.0",
    "vault": {
      "master_pub_fingerprint": "5f8e3d1f7c2b9a4e6d0f1c8a3b5e7f0a",
      "vault_path_hash": "abc1234567890fedcba0987654321abc",
      "vault_uuid": "550e8400-e29b-41d4-a716-446655440000"
    }
  },
  "prev_hash": "0000000000000000000000000000000000000000000000000000000000000000",
  "principal_sig": "ed25519_sig:principal_signature_hex_string_here",
  "record_hash": "sha256_hex_of_canonical_json_here",
  "schema_version": 0,
  "seq": 0,
  "ts": "2026-05-20T10:15:00-04:00",
  "ts_source": "ceremony_local_clock"
}
```

## Threat model

### Backdated genesis (Everest 21 threat EF16)
**Mitigation:** If `ts_source = "roughtime_anchored"`, the genesis timestamp is anchored to independent Roughtime servers and cannot be backdated undetectably. If `ts_source = "ceremony_local_clock"` or `ceremony_witness_attested`, the ceremony documentation serves as the anchor. A verifier holding a copy of the genesis record and the ceremony attestation can confirm they are temporally consistent.

### Forked chain (Everest 21 threat EF17)
**Mitigation:** Each genesis record contains a unique `vault_uuid`. If two chains claim to represent the same principal but have different `vault_uuid` values in their genesis records, they are forks. Counterparties can detect this by comparing genesis records and alert the principal that their vault has been cloned.

### Rogue operator unilaterally creating a chain
**Mitigation:** The principal signature is required. The operator alone cannot create a genesis record without the principal's private key.

### Operator-signed-but-not-principal-signed record
**Mitigation:** Validation requires BOTH signatures to be present and valid. A single-signed record is rejected.

## Implementation references

- **Everest 22** (Enrollment → CredexAI Credential Issuance) supplies the credexai_vc_id values and VC objects for signature verification.
- **Everest 20** (Enrollment Witness Protocol, BAGGED) supplies the witness_attestations_root Merkle root.
- **Everest 11** (Enrollment Ceremony, BAGGED) supplies ceremony_id and ceremony_attestation_hash.
- **Everest 30** (Chain-Head Publication to Sigsum) supplies the sigsum_log_id and handles future chain-head publication.
- **Everest 31** (Roughtime Anchoring) supplies roughtime_servers and provides verifiable-timestamp backing for the genesis ts.

## Acceptance test

A genesis record is accepted if:

1. The calm-witness CLI runs with `--check-genesis` flag and exits 0.
2. The principal-identity binding (credexai_vc_id + legal_name_commitment) round-trips correctly in tests.
3. The operator-identity binding is verifiable against the operator's Ed25519 public key from their CredexAI VC.
4. Both principal and operator signatures verify over the canonical JSON.
5. The record_hash invariant holds (canonical JSON hash == stored record_hash).
6. The retroactive migration of the existing vault validates cleanly: a genesis.retroactive record is appended, and the entire chain (seq=1 through seq=9) verifies without errors.

— Calm, 2026-05-20
