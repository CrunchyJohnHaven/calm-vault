# ZKAC Everest 26 — Holder Vault Format Spec

*Phase XIX — Holder/Wallet Infrastructure. Prereq: ZKAC Everests 5 (W3C VC compatibility), 6 (did:calm method). Critical-path MVP.*

## Overview

A versioned binary format for the holder's local credential store. The vault is the single source of truth for all credentials held by a principal. It is encrypted at rest using Argon2id + AES-256-GCM, signed with HMAC-SHA256 for tampering detection, and designed for sovereign control, portable backup, multi-device synchronization, and forward-compatible schema evolution.

**Design invariant (ZKAC constraint #2):** Credentials live in the principal's vault. Issuers and verifiers see only what the principal has explicitly authorized to be disclosed. The vault format enforces holder sovereignty: no issuer, verifier, or third party ever observes the vault structure or contents.

## Top-Level Container

### Magic bytes and version

| Offset | Bytes | Field | Type | Notes |
|--------|-------|-------|------|-------|
| 0 | 4 | Magic | ASCII | `"ZVAU"` (Zero-Knowledge Vault AU, phase XIX) |
| 4 | 2 | Format version | uint16 LE | Current version: 1; enables breaking changes to vault layout |
| 6 | 2 | Flags | uint16 LE | Bit 0: compression enabled; Bit 1–15 reserved |
| 8 | 4 | Container size | uint32 LE | Total bytes in this file, excluding this header |
| 12 | 1 | Key derivation algorithm | uint8 | 0 = Argon2id; others reserved |
| 13 | 3 | KDF parameters | uint8 × 3 | `[time_cost, memory_cost_log2, parallelism]` |

**Total fixed header: 16 bytes.**

### Encryption envelope

| Offset | Bytes | Field | Type | Notes |
|--------|-------|-------|------|-------|
| 16 | 16 | Encryption nonce (IV) | bytes | Random nonce for AES-256-GCM |
| 32 | 4 | Encrypted payload size | uint32 LE | Bytes in the encrypted block (excludes MAC) |
| 36 | 32 | MAC tag (HMAC-SHA256) | bytes | Computed over (header + nonce + encrypted_payload_size + encrypted_payload); holder can detect tampering without decryption |

**Total envelope overhead: 52 bytes.**

**MAC order:** `HMAC-SHA256(key=derived_mac_key, msg=(header[0:16] || nonce[16:32] || encrypted_payload_size[32:36] || encrypted_payload))`

### Encrypted payload schema

After AES-256-GCM decryption (key derived via Argon2id from principal's passphrase), the plaintext payload contains:

| Offset (within payload) | Bytes | Field | Type | Notes |
|--------|-------|-------|------|-------|
| 0 | 16 | Principal UUID | bytes | Bound to credential issuances; changes invalidate entire vault |
| 16 | 1 | Encoding | uint8 | 1 = MessagePack (chosen for binary compactness + backward compat); 2 = CBOR; 3 = FlatBuffers |
| 17 | 3 | Reserved | uint8 × 3 | Future schema extensions |
| 20 | 4 | Metadata map offset | uint32 LE | Byte offset to metadata map within payload |
| 24 | 4 | Index offset | uint32 LE | Byte offset to credential index within payload |
| 28 | 4 | Credentials offset | uint32 LE | Byte offset to credentials array within payload |
| 32 | 4 | Checksum (CRC32) | uint32 LE | Checksum of plaintext (excluding this field); catch bitflips post-decryption |

**Payload header: 36 bytes. All subsequent offsets are relative to plaintext start (byte 0 of decrypted data).**

#### Metadata map (MessagePack)

```json
{
  "schema_version": 1,
  "vault_created_at": "2026-05-20T14:30:00Z",
  "last_backup_at": "2026-05-20T14:31:00Z",
  "last_write_at": "2026-05-20T14:30:15Z",
  "credential_count": 7,
  "index_version": 1,
  "migration_chain": [
    { "from_version": 0, "to_version": 1, "migration_date": "2026-05-20T14:30:00Z", "hash": "sha256(...)" }
  ]
}
```

#### Credential index

A sorted array of credential headers for O(log N) lookups and concurrency coordination:

```
[
  {
    "id": "cred_uuid_0",
    "issuer_did": "did:calm:issuer:abc123",
    "holder_did": "did:calm:holder:xyz789",
    "type": ["VerifiableCredential", "ZKACCredential"],
    "issuer_class": "professional",
    "issued_at": "2026-01-15T10:00:00Z",
    "expires_at": "2027-01-15T10:00:00Z",
    "status_list_ref": "https://issuer.example/status/2026#12345",
    "offset": 1024,
    "size": 2048,
    "subkey_salt": "hex(16 bytes)",
    "subject_claim_hash": "sha256(...)"
  },
  ...
]
```

**Invariant:** Index must be sorted by `id` to enable binary search. Entries are immutable once written; new credentials append; revoked credentials are marked with `revoked_at` timestamp (see Revocation section).

#### Credential blob array

Raw CBOR or MessagePack-encoded credentials, positioned at offsets given by the index. Each credential is self-contained and can be individually encrypted with a per-credential subkey (see Key Derivation below).

**Inline optional encryption:** Issuer-sensitive or high-value credentials may be double-encrypted:
- The blob starts with a 1-byte encryption flag (0 = plaintext within vault, 1 = encrypted with subkey).
- If encrypted: next 16 bytes are the subkey nonce; remaining bytes are the ciphertext.
- Subkey is derived via `HKDF-SHA256(prk=vault_key, info="cred:" || cred_id, length=32)`.

## Key Derivation

### Vault master key

Derived from the holder's passphrase using Argon2id:

```
vault_key = Argon2id(
  password=principal_passphrase,
  salt=fixed_salt_derived_from_principal_uuid (sha256(principal_uuid)[0:16]),
  time_cost=KDF[0] (default: 3),
  memory_cost=2^KDF[1] KiB (default: 2^19 = 512 MiB),
  parallelism=KDF[2] (default: 4),
  hash_length=64,
  type=Argon2id
)
```

Output: 64 bytes (32 for AES-256, 32 for HMAC-SHA256).
- `aes_key = vault_key[0:32]`
- `mac_key = vault_key[32:64]`

**Why Argon2id:** Memory-hard, resistant to GPU/ASIC attacks, standards-track (IETF RFC 9106), audited implementations available (libargon2).

### Per-credential subkey derivation

For credentials requiring isolation (e.g., high-privilege agent credentials):

```
subkey = HKDF-SHA256(
  ikm=vault_key[32:64],  // MAC key as PRF input
  salt=cred_subkey_salt (from index entry, random per credential),
  info="zvau:cred:" || cred_id || ":v1",
  L=32
)
```

Used for per-credential AES-256-GCM encryption within the vault payload.

## Concurrency Model

**Single writer, multi-reader.**

Holders (on a single device or across synchronized devices) must coordinate writes to avoid vault corruption. The format uses a write-lock file:

1. **Lock file:** `~/.calm-vault/holder.lock` (advisory lock, read via `flock` on Unix or equivalent).
2. **Write discipline:** Before modifying the vault, a writer must acquire an exclusive lock. After modification (add credential, revoke, rotate key), release the lock.
3. **Read discipline:** Readers do not require a lock; they read the latest immutable vault file. Between releases, the file is never mutated in place — new credentials or revocations trigger a vault repack (see Compaction below).
4. **Multi-device sync:** A secondary device holding the same principal's vault syncs by:
   - Requesting the latest vault file from the primary (encrypted, over TLS or Calm Pact channel).
   - Verifying the MAC before decryption.
   - Loading the index and comparing `last_write_at` to detect freshness.
   - Never overwriting a newer vault with an older one.

## Backup and Portability

The entire vault is a single binary blob. Backup is straightforward:

1. **Encrypted backup:** The `.zvau` file itself is the backup artifact. Encrypt it once more (e.g., with age to a backup key) if backing up to untrusted storage.
2. **Metadata-only backup:** The metadata.json sidecar (cleartext) enables vault discovery and key-rotation coordination without decryption. Store alongside the vault for reference.
3. **Portability:** The vault can be moved to any device. The Argon2id KDF is deterministic: same passphrase + principal_uuid always regenerate the same key, enabling decryption on any platform that implements Argon2id.

## Schema Evolution and Migration

The vault supports versioning without requiring re-issuance of credentials:

### Format version bumps (breaking changes)

If the magic bytes remain `"ZVAU"` but format_version increments (e.g., 1 → 2), parsers at version N must either:
- Accept format version ≤ N (read backward), or
- Reject and prompt for migration.

Breaking changes warrant a major version bump and trigger a migration record in the chain (Everest 26 schema).

### In-chain migration record

A migration is logged as a Calm Witness record:

```json
{
  "seq": 42,
  "ts": "2026-06-01T10:00:00Z",
  "kind": "schema_migration",
  "payload": {
    "from_format_version": 1,
    "to_format_version": 2,
    "migration_type": "vault_repack",
    "old_vault_sha256": "deadbeef...",
    "new_vault_sha256": "cafebabe...",
    "action": "holder repacked vault to v2 format; old backup retained"
  },
  "principal": "John Bradley",
  "operator": "CALM"
}
```

This record serves as a tamper-evident log: if the vault was migrated, the Calm Witness chain proves the date and hash of both versions.

## Compaction and Revocation

### Append-only design with periodic repack

To avoid vault bloat, revoked credentials are not deleted in place; instead, they are marked with `revoked_at` in the index and kept (for audit and grace-period queries per Everest 34). Periodically, a writer triggers a **vault repack**:

1. Load the vault, decrypt, read the index.
2. Remove index entries marked `revoked_at` (older than grace period, typically 30 days).
3. Rewrite all remaining credentials to a new vault file in format order.
4. Recompute all offsets, MAC, and write the new vault file atomically (write to temporary file, fsync, rename).
5. Log the migration in Calm Witness.

**Invariant:** Repack never changes credential content, only removes stale revocations and closes gaps in the file.

## Index Structures and Fast Lookup

The credential index enables three query patterns:

1. **By ID:** Binary search on sorted `id` field → O(log N) lookup.
2. **By issuer_did:** Secondary index (optional, stored in metadata) mapping issuer_did → [cred_id, ...] → O(log N) + linear per issuer.
3. **By type predicate:** Traverse the index linearly; filter by type array membership. O(N), but typically small (< 100 credentials per holder).

**Index version:** Incremented when index structure changes (e.g., new secondary indexes added). Helps with incremental sync.

## Acceptance Tests (T-Z26.1..5)

### T-Z26.1: Binary format round-trip

- Generate a vault with 3 credentials.
- Serialize to disk.
- Decrypt, verify MAC, deserialize.
- Assert all credentials match.
- Assert CRC32 of plaintext matches.

### T-Z26.2: Key derivation determinism

- Derive `vault_key` from passphrase + principal_uuid twice.
- Assert both keys are identical.
- Decrypt the same vault with both keys; assert success.

### T-Z26.3: Encryption and tampering detection

- Encrypt a vault.
- Flip a bit in the ciphertext.
- Attempt to decrypt; assert MAC validation fails and decryption is aborted.

### T-Z26.4: Schema evolution

- Create a vault at format version 1.
- Read it with a version-1 parser; assert success.
- Migrate to version 2 (simulated); re-serialize.
- Attempt to read version-2 vault with version-1 parser; assert rejection.

### T-Z26.5: Concurrency under lock

- Spawn two writers; first acquires lock and appends 5 credentials.
- Second writer blocks on lock acquisition.
- First writer releases; second acquires, appends 3 more.
- Verify final vault has 8 credentials in correct order, no corruption.

## Composition with ZKAC E5/27/28/29/30/31/35

- **E5 (W3C VC compatibility):** Credentials stored in the vault conform to W3C VC data model + ZKAC extensions. The index's `type` field is the VC `type` array.
- **E27 (Holder key custody):** Keypairs for the principal (did:calm:holder:xyz) are derived from the vault_key via HKDF; stored in a separate key-store file encrypted with the same vault_key.
- **E28 (Holder vault encryption at rest):** This spec; AES-256-GCM + Argon2id.
- **E29 (Holder backup):** The entire vault (binary + metadata sidecar) is the portable backup artifact.
- **E30 (Recovery from device loss):** Backup + passphrase + ≥2 witness signatures restore the vault on a new device.
- **E31 (Multi-device holder):** The metadata sidecar includes `last_write_at`; secondary devices compare to detect freshness and avoid rollback.
- **E35 (Multi-credential simultaneous proof):** The index enables fast discovery of all credentials matching a presentation request.

## Design Rationale

**Binary format over JSON:** Credentials are large (5–20 KB each, especially with embedded proofs). MessagePack + optional per-cred encryption reduces size by 40–60% vs. JSON and enables granular encryption.

**Argon2id:** GPU-resistant, memory-hard, RFC 9106. Raises the bar for offline brute-force attacks by requiring 512 MiB memory per attempt.

**Single-writer, multi-reader:** Avoids merge conflicts and corruption on multi-device sync. The holder (principal) is always the single writer; secondary devices read and cache.

**Append-only index with periodic repack:** Balances efficiency (no in-place mutation) and storage footprint (periodic cleanup).

**Per-credential subkeys:** Issuers or compromised vault readers cannot correlate credential metadata across the vault; each credential is independently encryptable.

**HMAC-SHA256 outer MAC:** Detects tampering without decryption; useful for offline vault integrity checks.

**MessagePack encoding:** Compact, mature, simpler than FlatBuffers for variable-length arrays and dynamic maps. Supports forward compatibility via unknown-field tolerance.

## v1 Questions

1. **GC semantics for revoked credentials:** Grace period before deletion? Configurable per principal?
2. **Rate limiting on unlock attempts:** How many Argon2id iterations (roughly, cost in CPU time) before rate-limiting per session?
3. **Multi-issuer delegation flow:** If a primary issuer revokes a credential, how quickly must secondary devices learn? (Addressed in E17/E34.)
4. **Backup encryption:** Should the backup artifact itself be re-encrypted, or is the vault's own encryption sufficient?

## Signoff

Holder vault format v1.0 is ready for integration into ZKAC Phase XIX infrastructure. The spec enforces sovereign key control, enables portable backup, and composes cleanly with E27–E35.

— Calm, 2026-05-20
