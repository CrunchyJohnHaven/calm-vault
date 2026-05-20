# ZKAC Everest 29 — Holder Backup

*Phase XIX — Holder/Wallet Infrastructure. Prereq: ZKAC Everest 28 (Holder vault encryption at rest). Critical-path MVP.*

## Overview

A documented backup procedure that preserves credentials across device loss; off-host encrypted. The holder backup protocol enables recovery of the entire credential vault (ZKAC E26 vault format) using cryptographic shards distributed to trusted witnesses. Backups are encrypted at rest, event-triggered (credential issuance/revocation), time-triggered (weekly minimum), and verified quarterly via restore drills.

**Design invariant (ZKAC constraint #2):** The backup contents remain under the principal's sovereign control. Off-host backup targets are either end-to-end encrypted (cloud storage), air-gapped (USB, paper), or delegated to a Calm-foundation backup service (opt-in). No third party observes the vault plaintext or the master recovery key.

## Backup Contents

### Primary artifact: Encrypted vault file

The complete `.zvau` file (ZKAC E26 binary format) is the core backup payload. It contains all holder credentials, metadata, index, and revocation state.

**Format:** Binary, ZVAU magic bytes + encrypted payload.  
**Size:** Typically 50–500 KB (7 credentials @ ~50 KB each + overhead).  
**Encryption:** AES-256-GCM with Argon2id-derived key (E28 spec).

### Secondary artifact: KDF salt + parameters

Argon2id is deterministic; to decrypt a backup on a fresh device, the holder needs the KDF salt and cost parameters. These are extracted from the vault header (bytes 13–15) and the principal's UUID (which seeds the Argon2id salt via `sha256(principal_uuid)[0:16]`).

**Stored:** KDF metadata sidecar (JSON plaintext or in backup manifest).  
```json
{
  "principal_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "kdf_salt": "hex(sha256(principal_uuid)[0:16])",
  "kdf_time_cost": 3,
  "kdf_memory_cost_log2": 19,
  "kdf_parallelism": 4
}
```

### Tertiary artifact: Recovery quorum manifest

Social recovery requires ≥ N-of-M trusted witnesses to collaborate in restoring the backup. A recovery manifest encodes:

- **Witness registry:** 5–7 designated witnesses (names, contact info, public keys).
- **Quorum threshold:** N-of-M (e.g., 3-of-5). Default: 2-of-3.
- **Quorum public keys:** ECDSA P-256 or EdDSA (for witness signature verification).
- **Recovery ceremony timeline:** How long witnesses have to respond (e.g., 14 days before quorum expires).
- **Backup location manifest:** Pointers to encrypted backups (cloud URLs, USB serial numbers, paper backup locations).

**Manifest structure (JSON, signed):**
```json
{
  "principal": "John Bradley",
  "principal_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "backup_id": "bak_2026_05_20_v1",
  "created_at": "2026-05-20T15:00:00Z",
  "quorum_threshold": "2-of-3",
  "witnesses": [
    {
      "witness_id": "w1",
      "name": "Alice Chen",
      "role": "Family Member",
      "contact": "alice@example.com",
      "public_key_pem": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
    },
    {
      "witness_id": "w2",
      "name": "Bob Smith",
      "role": "Legal Advisor",
      "contact": "bob@law.example.com",
      "public_key_pem": "..."
    },
    {
      "witness_id": "w3",
      "name": "Carol Davis",
      "role": "Technical Guardian",
      "contact": "carol@tech.example.com",
      "public_key_pem": "..."
    }
  ],
  "backup_targets": [
    {
      "target_id": "cloud_aws_s3",
      "type": "aws_s3_encrypted",
      "location": "s3://calm-vault-backups/johnbradley/bak_2026_05_20_v1.zvau.enc",
      "encryption_key_fingerprint": "sha256(...)",
      "last_synced": "2026-05-20T15:01:00Z"
    },
    {
      "target_id": "usb_sealed",
      "type": "usb_drive",
      "serial": "USB_SEALED_20260520",
      "location": "Stored with Alice (backup designated)",
      "last_synced": "2026-05-20T15:01:00Z"
    },
    {
      "target_id": "paper_mnemonic",
      "type": "bip39_mnemonic",
      "location": "Sealed envelope, stored at Carol's office",
      "checksum": "sha256(...)",
      "last_synced": "2026-05-20T15:01:00Z"
    }
  ],
  "ceremony_deadline": "2026-06-03T15:00:00Z",
  "manifest_signature": "sig(...)"
}
```

## Backup Target Options

### Cloud storage with end-to-end encryption

The encrypted vault file (`.zvau`) is uploaded to cloud storage (AWS S3, Google Cloud Storage, Azure Blob) with additional encryption at the application layer.

**Flow:**
1. Generate a random 32-byte backup key (independent from vault key).
2. Encrypt `.zvau` using AES-256-GCM with this backup key.
3. Upload the encrypted blob to cloud storage.
4. Store the backup key in one of: (a) a separate encrypted key-store file on a trusted device, (b) a recovery quorum shard (secret-shared across witnesses), or (c) a paper backup.

**Threat model:** Cloud provider cannot read backup; cloud infrastructure failures do not block recovery (assuming key is preserved elsewhere).

### USB drive or air-gapped storage

A physical backup on portable media, typically sealed and stored with a trusted contact.

**Flow:**
1. Encrypt `.zvau` + KDF metadata to a USB drive.
2. Seal the drive in a tamper-evident envelope with witness signatures.
3. Designate a custodian (e.g., family member or lawyer).
4. Record the USB serial number in the recovery manifest.

**Threat model:** Air-gapped; no network access required at recovery time. Custodian must be trusted not to access or destroy the drive.

### Paper backup of BIP39 mnemonic phrase

A 12 or 24-word BIP39 mnemonic phrase encoding the KDF root (vault master key entropy). The principal writes the mnemonic to paper, signs/seals it, and stores it with a witness.

**Flow:**
1. Extract 128 or 256 bits of entropy from the vault master key (first 16 or 32 bytes).
2. Convert to BIP39 mnemonic phrase (12 or 24 words).
3. Write to paper; principal signs and dates it.
4. Seal in an envelope; store with designated witness(es).
5. Record mnemonic checksum (SHA-256 of the mnemonic string) in the backup manifest.

**Threat model:** Physical media; resistant to digital compromise. Witness must safeguard the paper. Mnemonic is useless without the principal's passphrase and KDF parameters.

### Off-host Calm-foundation backup service (opt-in)

A delegated backup service run by the Calm foundation. The principal grants the service read-only access to encrypted backups; the foundation never observes the plaintext vault or the master recovery key.

**Flow (Calm-foundation-managed recovery):**
1. Principal enrolls in Calm Witness (ZKBB Everest 100).
2. Calm foundation attestation service stores encrypted backups on the principal's behalf.
3. Recovery requires:
   - Principal provides passphrase (or passphrase shards via recovery quorum).
   - Calm foundation verifies principal identity (via Calm Witness identity credentials).
   - Foundation returns encrypted backup.
   - Principal decrypts locally using Argon2id + passphrase.

**Threat model:** Calm foundation is trusted not to delete backups and to honor recovery requests. Foundation never sees plaintext or master key. Recovery remains under principal's control.

## Backup Cadence

### Event-triggered backups

A new backup is generated and synced immediately after:
- Credential issuance (holder receives a credential from an issuer).
- Credential revocation (issuer revokes or holder deletes a credential).
- Key rotation (ZKAC E27 key ceremony or compromise response).
- Vault migration (format upgrade, ZKAC E26 repack).

**Sync latency:** < 30 seconds for local backups (USB); < 2 minutes for cloud backups; paper mnemonic updated manually (within 7 days of the event).

### Time-triggered backups

A backup is generated and verified at minimum every 7 days, even if no credentials changed. This ensures:
- Backup infrastructure (cloud access, key store) is still functional.
- Metadata (witness contact info, quorum definition) remains current.
- Recovery manifest timestamps reflect holder's current state.

**Cadence:** Weekly, at a holder-configured time (default: Sunday 02:00 UTC).

## Verify-Restore Drill Cadence

The holder conducts a quarterly recovery drill to confirm backups are usable.

**Drill procedure (T-Z29.3):**
1. **Select a backup target** (rotate across targets: cloud → USB → paper-mnemonic).
2. **Retrieve the backup** (download from cloud, decrypt locally; or retrieve USB/paper from custodian).
3. **Attempt decryption** using the principal's passphrase and KDF parameters.
4. **Verify vault integrity** (check magic bytes, decrypt, validate CRC32, load index).
5. **Spot-check credentials** (verify ≥ 3 credentials decrypt and deserialize cleanly).
6. **Record drill results** (log timestamp, backup target, outcome, any issues). Store log in Calm Witness.
7. **Notify witnesses** (if social recovery path is tested, witnesses acknowledge receipt of recovery request).

**Expected frequency:** Every 90 days. Failure → escalation (repair backup, contact Calm foundation, or re-key).

## Recovery Quorum

### Witness roles and duties

A recovery quorum consists of N-of-M trusted witnesses who collaborate to reconstruct the master recovery key or authorize recovery.

**Witness types:**

1. **Family witness** (personal trust): typically a spouse, adult child, or sibling. Role: store a backup copy or quorum shard; respond to recovery requests within 14 days.
2. **Legal witness** (institutional trust): attorney, notary, or trust administrator. Role: verify identity via legal documentation; release backup or shard on written request.
3. **Technical witness** (operational trust): cybersecurity professional, DevOps engineer, or sys admin. Role: verify cryptographic signatures; assist in multi-device recovery.

Each witness is assigned a public key (ECDSA P-256 or EdDSA). During recovery, the principal collects ≥ N signed messages from witnesses confirming authorization.

### Social recovery vs. solo recovery

**Social recovery (default):**
- Backup is sharded across ≥ 3 witnesses using Shamir secret sharing (ZKAC E89).
- Each shard is useless alone; ≥ 2-of-3 shards are required to reconstruct the master key.
- Principal + witness collaboration ensures no single party can unilaterally restore.
- Witness consensus prevents the principal from recovering a vault that was compromised or stolen (guards against attacker impersonation).
- **Recovery flow:** Principal requests recovery → witnesses verify principal identity (out-of-band) → witnesses provide signed consent messages → principal combines shards → decrypts backup.

**Solo recovery (fallback):**
- The principal retains a complete, unshareded backup key (encrypted on a trusted device or paper).
- No witness coordination required.
- Faster recovery (minutes, not days).
- **Trade-off:** Single point of failure; theft or coercion of the solo key enables undetected recovery.
- **When used:** Principal has no trusted witnesses; principal prefers speed over collusion resistance; temporary (pending enrollment of witnesses).

## Composition with ZKAC E26, E27, E28, E30, E89

- **E26 (Holder vault format):** The `.zvau` binary file is the primary backup artifact.
- **E27 (Holder key custody):** The keypair for the principal's did:calm:holder identity is re-derived from the vault master key on each device using HKDF (E27 spec). No separate key backup needed.
- **E28 (Holder vault encryption at rest):** Vault is encrypted with Argon2id + AES-256-GCM. Backup targets are encrypted with the same or derived keys.
- **E30 (Holder recovery from device loss):** Recovery runbook explicitly invokes this E29 backup procedure and calls out witness authentication steps.
- **E89 (Secret sharing of vault keys):** Recovery quorum shards are generated via Shamir secret sharing of the vault master key, with verification per E90.

## T-Z29.1..5 Acceptance Tests

### T-Z29.1: Event-triggered backup

- Holder receives a credential.
- Trigger backup generation.
- Assert a new `.zvau` file is created with updated metadata and index.
- Assert new backup is synced to ≥ 1 target (cloud, USB, or Calm foundation).
- Assert backup timestamp is within 30 seconds of trigger time.

### T-Z29.2: Time-triggered backup

- Set backup cadence to 1 minute (for testing).
- Wait 1 minute.
- Assert a backup is generated automatically, even though no credentials changed.
- Verify metadata `last_backup_at` is updated.

### T-Z29.3: Verify-restore drill (quarterly)

- Execute a full restore drill (see Verify-Restore Drill Cadence section).
- Assert vault decrypts successfully.
- Assert all credentials in the index are accessible.
- Assert drill log is recorded in Calm Witness with timestamp and outcome.

### T-Z29.4: Social recovery with witness quorum

- Set up a 2-of-3 witness quorum.
- Generate Shamir shards of the vault master key; distribute to 3 witnesses.
- Simulate a device loss scenario.
- Initiate recovery: principal requests ≥ 2 witnesses to provide signed consent.
- Collect signatures.
- Reconstruct vault master key from 2 shards.
- Decrypt backup using reconstructed key.
- Assert vault integrity (CRC32, index, credentials).

### T-Z29.5: Solo recovery fallback

- Set up a solo recovery backup (principal retains unshareded key on secure device).
- Simulate device loss.
- Principal provides passphrase + backup key.
- Decrypt backup locally.
- Assert vault is usable (all credentials accessible, ready for presentation).

## Design Rationale

**Event + time triggered:** Event-triggered backups react to credential changes; time-triggered backups ensure backup infrastructure is regularly exercised.

**Multiple target types:** Cloud is convenient; USB is air-gapped; paper mnemonic is human-readable and doesn't require software. No single target is ideal; diversification increases resilience.

**Quorum + sharding:** Shamir secret sharing (E89) ensures no single witness can restore the vault unilaterally. Principal can set quorum to 1-of-1 (solo) for speed or 3-of-5 (high security) for collusion resistance.

**Quarterly drills:** Regular verification catches silent failures (cloud access revoked, USB degraded, paper lost). Drills are low-cost; failures are detected early.

**Witness roles:** Family, legal, technical witnesses have different strengths. Diversifying witness types reduces correlated failure (e.g., all family members absent, or single lawyer compromised).

## v1 Questions

1. **Shard expiration:** If a witness doesn't respond within 14 days, should the recovery attempt time out? Should quorum threshold be relaxed (2-of-3 → 2-of-2)?
2. **Backup redundancy:** How many targets must be kept in sync? Required minimum: cloud + one offline (USB or paper)?
3. **Witness enrollment:** How are witnesses vetted? Must they undergo a ceremony to confirm public keys? (Addressed in witness-enrollment subprotocol.)
4. **Paper mnemonic refresh:** BIP39 phrases degrade over time (fading ink, water damage). Refresh cadence? Once per year?
5. **Calm foundation SLA:** If principal recovers via Calm foundation, what is the SLA for foundation to return encrypted backups? (Proposed: < 24 hours.)

## Signoff

Holder backup v1.0 bridges E28 (vault encryption) and E30 (recovery). Backup procedure is backward-compatible with E26 vault format, composable with E27/E89 for key custody, and operationally sound with quarterly drills and multi-target resilience.

— Calm, 2026-05-20
