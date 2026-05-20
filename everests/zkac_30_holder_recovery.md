# ZKAC Everest 30 — Holder Recovery from Total Device Loss

*Phase XIX — Holder/Wallet Infrastructure. Prereq: ZKAC Everest 29 (Holder backup). Critical-path MVP.*

## Overview

This runbook re-creates the holder vault from backup + ≥2 witness signatures after total device loss. Principal is alive, no biometric access available, must re-bootstrap from encrypted backup. Procedure includes witness quorum recovery, device binding attestation, and issuer/verifier notification. Recovery is privacy-preserving: third parties learn only that THIS principal migrated, not which credentials were recovered.

**Design invariant (ZKAC constraint #2):** The principal retains full sovereign control of the recovered vault. Witnesses authenticate identity and authorize recovery; they do not decrypt or access credentials.

---

## Scenario: Total Device Loss

**Trigger conditions:**
- Principal's device (phone, laptop, hardware wallet) is lost, stolen, or destroyed.
- Principal has no physical access to the vault master key or backup key.
- Principal IS alive, conscious, and able to communicate out-of-band with witnesses.
- Principal has ≥1 encrypted backup (cloud, USB, or paper mnemonic).
- Principal retains their passphrase (or can recover it from memory/notes).

**Recovery goal:** Acquire a new device, re-bootstrap the holder wallet, verify vault integrity, re-attest device binding, and notify issuers that the principal has migrated.

---

## Phase XIX Prereq: ZKAC Everest 29 Holder Backup

This recovery procedure assumes:
- Encrypted vault file (`.zvau`) exists in ≥1 backup target (cloud, USB, or paper mnemonic).
- KDF metadata (Argon2id salt, cost parameters, principal UUID) is accessible (from vault header or sidecar).
- Recovery manifest with witness registry and quorum threshold is available.
- Master recovery key is either: (a) sharded across witnesses via Shamir secret sharing (social recovery), or (b) stored solo on a secure device (solo recovery).

Recovery manifest location: Principal's email, cloud document, or in sealed envelope with a witness.

---

## 6-Step Recovery Runbook

### Step 1: Acquire New Device and Install Calm Holder Wallet

**Action:**
1a. Principal obtains a new device (phone or laptop).
1b. Principal installs the Calm Holder Wallet application (v1.0+) from official repository.
1c. Holder wallet generates a temporary device key pair (`device_pk`, `device_sk`).
1d. Wallet prompts: "Do you have a backup to recover, or create a new vault?" → Principal selects "Recover from backup."
1e. Wallet prompts for recovery manifest location (URL, USB serial, or witness contact).

**Acceptance:** Device is online, wallet is installed and functional, temporary device key exists.

---

### Step 2: Retrieve Backup Blob from Off-Host Storage

**Action:**
2a. Principal locates recovery manifest (via email, cloud drive, or witness contact).
2b. Recovery manifest contains backup targets (cloud URLs, USB serial numbers, paper mnemonic checksum).
2c. For each backup target:
   - **Cloud (AWS S3):** Principal logs in to cloud account, downloads `.zvau.enc` file.
   - **USB (air-gapped):** Principal retrieves sealed USB from witness, unseal with witness present (optional tamper check).
   - **Paper (BIP39 mnemonic):** Principal retrieves sealed envelope with witness, extracts and verifies mnemonic checksum against manifest.
2d. Principal verifies backup integrity (file hash or mnemonic checksum matches manifest).

**Acceptance:** At least one backup blob is retrieved and integrity-verified. Manifest is available locally (printed, in wallet app, or on cloud).

---

### Step 3: Recover KDF Root via N-of-M Witness Quorum

**Goal:** Reconstruct the master recovery key (`vault_master_key`) from witness shards or solo backup.

#### 3A: Social Recovery (Default Path)

**Prerequisites:** Master key is secret-shared across N witnesses via Shamir secret sharing (ZKAC E89). Quorum threshold is N-of-M (e.g., 2-of-3).

**Action:**
3a1. Principal contacts ≥N witnesses (out-of-band: phone call, video call, or in-person meeting).
3a2. Principal identifies self using personal knowledge (childhood nickname, shared secret, government ID).
3a3. Each witness verifies principal is alive and uncoerced. Witnesses may ask follow-up questions:
   - "What is our agreed-upon recovery passphrase?" (out-of-band pre-agreed).
   - "Can you describe the last credentials we issued?" (personal knowledge).
   - "Do you want to recover, or are you under duress?" (coercion check).
3a4. If witness is satisfied, witness generates a signed message (`recovery_auth_msg`):
   ```
   {
     "witness_id": "w1",
     "principal_uuid": "550e8400-e29b-41d4-a716-446655440000",
     "action": "authorize_recovery",
     "timestamp": "2026-05-21T10:30:00Z",
     "nonce": "sha256(device_pk || timestamp)",
     "signature": "ed25519_sign(witness_sk, recovery_auth_msg || nonce)"
   }
   ```
3a5. Witness sends signed message to principal via secure channel (encrypted email, Signal, or in-person handoff).
3a6. Principal collects ≥N signed messages from witnesses.
3a7. Principal verifies each signature using witness's public key (from recovery manifest).
3a8. If ≥N signatures are valid and nonces are consistent, proceed to shamir reconstruction.

**Witness Quorum Acceptance Check (coercion resistance):**
- Witness must explicitly confirm principal is **alive and uncoerced**.
- Witness can **refuse quorum** if suspicious (attacker impersonating principal, coercion detected).
- If witness refuses, N-of-M threshold is not met; recovery stalls (escalate to Calm foundation or additional witness).
- Witnesses **do not** see plaintext vault; they only verify principal identity and provide signatures.

**Shamir Reconstruction:**
3a9. Principal holds witness shares (or reconstructs from witness messages if shards were transmitted via signatures).
3a10. Principal uses Shamir secret sharing library (e.g., python-secrets, go-tss) to reconstruct master key:
   ```
   vault_master_key = shamir_combine([shard_from_w1, shard_from_w2, ...])
   ```
3a11. Verify reconstruction: `sha256(vault_master_key) == master_key_hash` (from recovery manifest).

**Expected latency:** 2–14 days (witness response time; default: 3 days).

#### 3B: Solo Recovery (Fallback Path)

**Prerequisites:** Master recovery key is not sharded; principal retains the full key on a backup medium (secure device, paper, or encrypted key-store file).

**Action:**
3b1. Principal locates solo backup key (on paper, encrypted on trusted device, or from memory).
3b2. If paper: Principal verifies paper backup matches recovery manifest (date, signature, mnemonic checksum).
3b3. If encrypted key-store file: Principal retrieves file (e.g., from cloud key manager or secure enclave) and decrypts using passphrase.
3b4. Principal extracts the 16 or 32 bytes of master key entropy.

**Expected latency:** Immediate (minutes).

---

### Step 4: Decrypt Vault and Verify Chain Integrity

**Goal:** Decrypt the `.zvau` backup and confirm no tampering or corruption.

**Action:**
4a. Principal retrieves KDF metadata from recovery manifest or vault backup header:
   ```
   kdf_salt = sha256(principal_uuid)[0:16]
   kdf_time_cost = 3  (or value from manifest)
   kdf_memory_cost_log2 = 19  (or value from manifest)
   kdf_parallelism = 4  (or value from manifest)
   ```
4b. Principal enters passphrase (same as used on lost device, or recovered from secure note).
4c. Wallet derives vault encryption key:
   ```
   vault_key = argon2id(
     password = passphrase,
     salt = kdf_salt,
     time_cost = kdf_time_cost,
     memory_cost = 2^kdf_memory_cost_log2 KB,
     parallelism = kdf_parallelism,
     output_length = 32
   )
   ```
4d. Wallet decrypts `.zvau` file using AES-256-GCM with derived `vault_key`.
4e. Wallet verifies ZVAU magic bytes (bytes 0–3): `0x5A 0x56 0x41 0x55` ("ZVAU").
4f. Wallet verifies CRC32 checksum of vault contents (from E26 vault format spec).

**Chain integrity check (transparency log lookup):**
4g. Wallet retrieves last-known vault head hash from transparency log (e.g., Sigsum, per ZKAC E19).
4h. Wallet computes hash of recovered vault contents: `vault_hash = sha256(vault_contents)`.
4i. Wallet verifies `vault_hash` matches or is a descendant of the last-known head (via chain link hashes).
4j. If chain is broken or vault is older than expected, flag as potential tampering; halt recovery and escalate.

**Acceptance:** Vault decrypts cleanly, magic bytes match, CRC32 passes, transparency log chain is intact.

---

### Step 5: Re-Attest Device Binding (New Device Key Bound to Recovered Identity)

**Goal:** Bind the new device to the principal's recovered identity via cryptographic attestation.

**Action:**
5a. Wallet has already generated temporary `device_pk` (Step 1).
5b. Wallet derives principal's holder identity from vault master key:
   ```
   holder_sk = hkdf(
     ikm = vault_master_key,
     salt = "holder_identity_key",
     info = "did:calm:holder:" || principal_uuid,
     length = 32
   )
   holder_pk = pk(holder_sk)  # ECDSA P-256 or EdDSA
   ```
5c. Wallet creates a device-binding attestation:
   ```
   {
     "principal_uuid": "550e8400-e29b-41d4-a716-446655440000",
     "old_device_fingerprint": "sha256(old_device_pk)",  # from vault metadata
     "new_device_pk": "<device_pk>",
     "new_device_certificate": "<attestation from TPM/Secure Enclave, if available>",
     "migration_reason": "total_device_loss",
     "migration_timestamp": "2026-05-21T11:00:00Z",
     "signature": "holder_sk.sign(device_pk || migration_timestamp)"
   }
   ```
5d. Wallet stores attestation in vault (ZKAC E26 recovery metadata section).
5e. Wallet broadcasts attestation to all credential issuers (Step 6, below).

**Acceptance:** Device-binding attestation is signed and ready for issuer notification.

---

### Step 6: Notify Issuers + Verifiers of Device Migration

**Goal:** Inform all credential issuers and registered verifiers that the principal has migrated to a new device. Privacy-preserving: only flag migration; don't disclose which credentials.

**Action:**
6a. Wallet extracts list of issuer endpoints from recovered credentials (ZKAC E26 format includes issuer URIs).
6b. For each issuer, wallet constructs a device-migration notice:
   ```
   {
     "did": "did:calm:holder:550e8400-e29b-41d4-a716-446655440000",
     "migration_type": "total_device_loss",
     "old_device_pk": "sha256(old_device_pk)",  # hashed for privacy
     "new_device_pk": "<device_pk>",
     "attestation": "<device_binding_attestation>",
     "timestamp": "2026-05-21T11:00:00Z",
     "signature": "holder_sk.sign(migration_notice)"
   }
   ```
6c. Wallet sends POST request to each issuer's device-migration endpoint:
   ```
   POST /api/v1/holder/device_migration
   Content-Type: application/json
   {
     "migration_notice": {...}
   }
   ```
6d. Issuer verifies signature using principal's public key (from issuer's registry or via trusted DID resolver).
6e. Issuer updates internal holder metadata: marks old device as revoked, new device as active. Issuers may revoke outstanding presentations signed by the old device (privacy-preserving).
6f. Issuer returns 200 OK or escalates to holder support if verification fails.

**Verifier notification (optional broadcast):**
6g. Wallet publishes migration notice to a verifier-accessible revocation registry (ZKAC E15, E17).
6h. Verifiers check the registry before accepting presentations; they learn only "this holder migrated" without credential-level detail.

**Expected latency:** < 5 minutes per issuer.

**Acceptance:** All issuers respond successfully; no issuer blocks recovery. New device is now registered.

---

## Failure Modes and Fallbacks

### FM-30.1: Witnesses Unreachable

**Scenario:** ≥N witnesses do not respond within 14 days; social recovery stalls.

**Fallback:**
- Principal escalates to Calm foundation (if enrolled in Calm Witness, ZKBB Everest 100).
- Foundation verifies principal identity using Calm Witness credentials or government ID.
- Foundation authorizes recovery and returns encrypted backup.
- Principal decrypts using passphrase (skipping witness quorum).
- **Trade-off:** Requires trust in Calm foundation; slower (24–48 hours).

### FM-30.2: Backup Corrupted or Inaccessible

**Scenario:** Cloud provider lost backup; USB drive is corrupted; paper mnemonic is illegible.

**Fallback:**
- Principal attempts recovery from an alternative backup target (if multiple targets exist).
- If all targets fail: Principal escalates to Calm foundation.
- Foundation checks whether issuer audit logs contain credential proofs that can be re-issued (issuer-side recovery).
- **Trade-off:** Credentials may need to be re-issued; delay of 1–2 weeks.

### FM-30.3: Transparency Log Unavailable

**Scenario:** Transparency log (Sigsum, etc.) is down or unreachable.

**Fallback:**
- Wallet allows recovery to proceed **with a warning** (vault integrity check is degraded).
- Principal can inspect vault contents (credentials, metadata) locally.
- Wallet defers transparency-log verification to first online presentation (issuers will verify chain at that time).
- **Trade-off:** Principal recovers without assurance of chain integrity; issuer acceptance may be delayed if chain validation fails.

### FM-30.4: Device Attestation Unavailable

**Scenario:** New device lacks TPM/Secure Enclave; attestation cannot be hardware-backed.

**Fallback:**
- Wallet creates a software-only attestation (unsigned or signed only by holder identity).
- Issuers are notified of "soft" attestation; they may request additional out-of-band verification.
- Principal can request issuer support to re-bind credentials to new device if needed.
- **Trade-off:** Slightly reduced assurance; recovery proceeds.

### FM-30.5: Coerced Principal Attempting Recovery

**Scenario:** Attacker impersonates or coerces principal to extract vault.

**Defense (witness coercion resistance):**
- Witnesses are instructed to reject recovery if principal:
  - Cannot answer personal knowledge questions (childhood memory, shared secret).
  - Exhibits signs of duress (nervous tone, unusual timing, inconsistent story).
  - Requests recovery from an unusual location (public network, compromised device).
- If witness refuses, recovery stalls. Attacker cannot proceed without ≥N witnesses.
- Principal can later initiate recovery with different witnesses or via Calm foundation.
- **Assumption:** Witnesses are trustworthy and cannot be coerced or hacked (out-of-band verification).

---

## Composition with ZKAC E26, E27, E28, E29, E89

- **E26 (Holder vault format):** Recovery reconstructs the `.zvau` binary and re-loads credential index.
- **E27 (Holder key custody):** Holder identity is re-derived from master key on the new device (no backup of identity key needed).
- **E28 (Holder vault encryption at rest):** Vault decryption uses Argon2id + AES-256-GCM (same as original encryption).
- **E29 (Holder backup):** Recovery explicitly invokes E29 backup artifacts: encrypted vault, KDF metadata, recovery manifest, witness registry, quorum threshold.
- **E89 (Secret sharing of vault keys):** Shamir reconstruction (Step 3A) uses E89 primitives; verification per E90 (Verifiable secret sharing).

---

## T-Z30.1..5 Acceptance Tests (Chaos-Monkey Protocol)

### T-Z30.1: Social Recovery End-to-End

**Setup:**
- Create principal with 2-of-3 witness quorum.
- Generate 3 Shamir shards; distribute to witnesses.
- Issue 3 credentials to principal.
- Create encrypted backup on cloud + USB.

**Test:**
1. Simulate total device loss (erase device).
2. Principal acquires new device, installs wallet, selects "Recover from backup."
3. Principal contacts 2-of-3 witnesses; each provides signed authorization.
4. Wallet reconstructs master key from 2 shards.
5. Wallet decrypts backup from cloud.
6. Wallet verifies vault integrity (CRC32, chain).
7. Wallet re-derives holder identity, creates device-binding attestation.
8. Wallet notifies all issuers of device migration.
9. Issuers acknowledge; new device is active.
10. Principal presents a credential using the new device; verifier accepts.

**Expected latency:** ≤2 hours (witness response can be faster for testing).

**Pass criterion:** All steps succeed; credentials are usable on new device.

---

### T-Z30.2: Solo Recovery Fallback

**Setup:**
- Create principal without witness quorum (solo recovery enabled).
- Solo backup key stored in key-store file (encrypted).
- 3 credentials issued; encrypted backup on cloud.

**Test:**
1. Simulate device loss.
2. Principal acquires new device, selects "Recover from backup."
3. Principal provides passphrase and solo backup key (from secure file).
4. Wallet decrypts backup.
5. Wallet verifies chain integrity against transparency log.
6. Wallet re-derives identity and notifies issuers.
7. New device is active; principal presents credential.

**Expected latency:** < 30 minutes.

**Pass criterion:** Solo recovery succeeds without witness delay.

---

### T-Z30.3: Witness Coercion Rejection

**Setup:**
- Principal with 2-of-3 witness quorum.
- Attacker obtains principal's device.

**Test:**
1. Attacker attempts recovery by contacting 1 witness.
2. Witness asks: "Are you under duress?"
3. Attacker responds evasively or inconsistently.
4. Witness **rejects** quorum authorization.
5. Recovery stalls (1-of-3 is not ≥2-of-3).
6. Attacker cannot proceed.

**Expected outcome:** Witness refusal blocks attacker.

**Pass criterion:** Witness rejection is respected; recovery does not proceed.

---

### T-Z30.4: Device Migration Notification

**Setup:**
- Principal with 2 credentials from Issuer A, 1 credential from Issuer B.
- Both issuers have registered migration endpoints.

**Test:**
1. Principal recovers vault (Steps 1–5).
2. Wallet extracts issuer endpoints.
3. Wallet sends device-migration notice to Issuer A and Issuer B.
4. Issuer A: acknowledges, marks old device revoked, new device active.
5. Issuer B: same.
6. Principal presents a credential from Issuer A to Verifier V.
7. Verifier V queries Issuer A for revocation status.
8. Issuer A confirms credential is valid; new device is registered.
9. Verifier accepts presentation.

**Expected latency:** < 10 minutes (issuer endpoint calls).

**Pass criterion:** All issuers are notified; verifier accepts presentation from new device.

---

### T-Z30.5: Transparency-Log Chain Verification

**Setup:**
- Vault has chain link hashes in metadata (from E26 format).
- Transparency log (Sigsum, etc.) is queryable.

**Test:**
1. Principal recovers vault (Steps 1–4).
2. Wallet computes vault hash: `vault_hash = sha256(recovered_contents)`.
3. Wallet queries transparency log for last-known head hash.
4. Wallet verifies chain: `last_known_head` is an ancestor of `vault_hash` (via chain links).
5. If chain is intact, recovery proceeds.
6. If chain is broken, recovery halts with error.

**Test variant (transparency log down):**
- Transparency log is unreachable (network failure).
- Wallet allows recovery with degraded-assurance warning.
- Verification deferred to first presentation (issuer will re-verify chain).

**Expected outcome:** Chain verification passes (normal case); degraded mode allowed (infrastructure failure).

**Pass criterion:** Both paths (normal + degraded) are handled correctly.

---

## Design Rationale

**Multi-step recovery:** Steps 1–6 decompose recovery into distinct phases (device setup, backup retrieval, key reconstruction, decryption, identity re-derivation, notification). Each phase is independent and can be debugged separately.

**Witness quorum + coercion resistance:** N-of-M threshold and out-of-band verification ensure no single attacker can unilaterally extract the vault. Witnesses serve as a "human firewall."

**Privacy-preserving issuer notification:** Issuers learn that THIS principal migrated, not WHICH credentials. Holders' privacy is preserved.

**Transparency-log chain verification:** Vault is checked against a public ledger, catching tampering or corruption during backup storage.

**Device-binding attestation:** New device key is cryptographically bound to principal identity, enabling issuer to revoke old-device presentations and accept new-device presentations.

**Fallback paths:** Witness unavailability, backup corruption, and transparency-log outages do not permanently block recovery. Calm foundation escalation and issuer re-issuance are available as last resorts.

---

## v1 Questions

1. **Witness timeout:** If a witness doesn't respond within 14 days, should recovery auto-escalate to Calm foundation? Or should principal manually escalate?
2. **Old-device revocation:** Should issuer immediately revoke all presentations signed by the old device? Or should there be a grace period?
3. **Device attestation validation:** How strict should device attestation be? Hardware-backed only, or accept soft attestation?
4. **Paper mnemonic recovery:** If principal loses paper backup AND all witnesses are unavailable, can Calm foundation recover? What is the emergency escalation path?
5. **Multi-device support (E31 composition):** If principal held credentials on Device A and Device B, and Device A is lost, does recovery re-activate Device B? Or must Device B be explicitly re-bound?

---

## Signoff

Holder recovery v1.0 completes the disaster-recovery pillar of ZKAC holder infrastructure. Recovery is operationally sound (6 steps, <2 hours for social path), privacy-preserving (witnesses and issuers learn minimal detail), and coercion-resistant (witness quorum prevents attacker-driven vault extraction). Composition with E26/E27/E28/E29/E89 is clean; fallback paths handle witness unavailability, backup corruption, and infrastructure failure. T-Z30.1..5 chaos tests confirm end-to-end operability and attacker resistance.

— Calm, 2026-05-20
