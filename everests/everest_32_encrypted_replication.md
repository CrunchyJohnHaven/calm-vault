# Everest 32 — Encrypted Replication of Chain

*Phase III — Self-Report Substrate. Prereq: Everest 28.*

## Decision

Calm Witness v0 requires the principal's canonical chain (`~/.calm-vault/user_state.jsonl`) to be replicated to a minimum of two independent locations, encrypted at rest with keys the principal controls. The principal selects replica locations; the protocol provides default replication pathways and synchronization semantics.

The canonical chain lives in `~/.calm-vault/user_state.jsonl` on the operator's machine. Replicas are encrypted archives (using the `age` asymmetric cipher) stored in locations the principal chooses, from which the principal can recover the full chain if the canonical vault is destroyed or inaccessible.

## Replication architecture

### Replica locations — default profile for v0

**Replica 1: Removable encrypted USB-C drive.** A USB drive, encrypted at the device level via `age`, stored in a physically separate location (off-site — trusted family member's home, safe-deposit box, geographically distant dwelling). The principal connects the drive only when explicitly synchronizing replicas, ensuring it is offline by default and therefore immune to remote compromise of the operator's network.

**Replica 2: Encrypted object store.** An S3-compatible bucket under the principal's own account (e.g., Backblaze B2, Tigris, or AWS S3). Each sync operation appends a versioned, encrypted snapshot. Retention policy keeps the last N=12 snapshots; older snapshots are garbage-collected by lifecycle rules. Because each snapshot is a complete chain copy (not a delta), any single snapshot suffices for full recovery.

**Replica 3 (optional): Paper backup of genesis.** A printed record of the genesis block (the first record in the chain) plus the current chain head hash plus the most recent Sigsum inclusion anchor. Stored in a safe-deposit box or with a trusted third party. This is a last-ditch recovery aid if both electronic replicas are lost; it cannot recover the full chain but can prove to a future observer that a chain with that genesis and head did exist at that anchor time.

### Encryption layer

Each replica's contents are encrypted using `age` (https://age-encryption.org), the modern, audited asymmetric encryption scheme. The principal's age recipient key (public) is stored in `~/.calm-vault/recipients.txt`. The private key is never stored unencrypted on disk; it is encrypted with the principal's passphrase and stored as `~/.calm-vault/master.priv.enc` (composed with Everest 16 — key custody).

The principal can encrypt data to their own recipient key without needing the private key — this is the asymmetric property. The operator's CLI encrypts the chain archive using the principal's public key; decryption always requires the principal's private key and passphrase.

Encryption is per-file. Two files are encrypted:

- `user_state.jsonl.age` — the encrypted chain itself.
- `anchors.tar.age` — a TAR archive of the `anchors/` directory (Sigsum inclusion proofs, Roughtime attestations, and related chain-head anchor records).

Each replica is encrypted; the object-store provider's at-rest encryption is defense-in-depth but not the authoritative layer. Even if the provider or an adversary with object-store credentials is subpoenaed or breached, they hold only ciphertext. The principal's age encryption is the binding security boundary.

## Sync protocol — Replica 1 (USB drive)

**Precondition:** Replica 1 is a removable USB drive. The principal physically plugs it into the operator's machine when they wish to sync.

### Step-by-step

1. **Verify the canonical chain.** The operator runs `calm-witness verify-chain` against `~/.calm-vault/user_state.jsonl`. The chain must be valid (all hashes linked correctly, no tampering) before replication proceeds. If verification fails, sync aborts with an error and does not proceed to encryption.

2. **Encrypt and archive.** The operator encrypts both `user_state.jsonl` and the `anchors/` directory as two separate age-encrypted files:
   ```
   age --recipient $(cat ~/.calm-vault/recipients.txt) -o <usb-mount>/replicas/v0/<sync-ts>.user_state.jsonl.age < ~/.calm-vault/user_state.jsonl
   tar czf - ~/.calm-vault/anchors/ | age --recipient $(cat ~/.calm-vault/recipients.txt) -o <usb-mount>/replicas/v0/<sync-ts>.anchors.tar.age
   ```
   The `sync_ts` is a timestamp (e.g., ISO 8601 with microsecond precision, e.g., `2026-05-20T14:23:45.123456Z`) and serves as the sync version key.

3. **Compute and store manifest.** The operator writes a manifest file (JSON) to the USB drive:
   ```json
   {
     "sync_id": "<uuid>",
     "sync_ts": "2026-05-20T14:23:45.123456Z",
     "source_chain_head": "the sha256 hash of the last record in user_state.jsonl",
     "source_record_count": 42,
     "encryption_recipient_fingerprint": "age public key fingerprint (e.g., age1...)",
     "replica_id": "usb1",
     "encryption_algorithm": "age-v1"
   }
   ```

4. **Append to canonical chain.** The operator appends a new record to `~/.calm-vault/user_state.jsonl` (following the hash-chain invariants from Everest 28):
   ```json
   {
     "seq": 43,
     "ts": "2026-05-20T14:23:45.123456Z",
     "kind": "replica.sync_completed",
     "replica_id": "usb1",
     "manifest_hash": "<sha256 of the manifest JSON>",
     "encryption_recipient": "age1...",
     "prev_hash": "...",
     "record_hash": "..."
   }
   ```

5. **Publish chain head (optional at this stage, required before disclosure).** The operator publishes the new chain head to Sigsum (Everest 30). The Sigsum inclusion proof is stored in `~/.calm-vault/anchors/`.

### Sync cadence for Replica 1

USB syncing is manual and infrequent — typically weekly, monthly, or on-demand by the principal. The USB drive is kept offline at all times when not actively syncing, minimizing its exposure surface.

## Sync protocol — Replica 2 (cloud object store)

**Precondition:** Replica 2 is an S3-compatible bucket. The principal has configured credentials in their local environment (e.g., `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` or equivalent for Backblaze B2 / Tigris).

### Step-by-step

Same as Replica 1 steps 1–4, but instead of writing to USB:

1. Verify the canonical chain.
2. Encrypt and archive the same two files (`.age` format).
3. Compute the manifest.
4. PUT both `.age` files to the object store:
   ```
   s3 put-object \
     --bucket <vault_bucket> \
     --key "<vault_uuid>/v0/<sync_ts>.user_state.jsonl.age" \
     --body <encrypted-file>
   ```
   Versioning and path structure allow recovery of any prior snapshot.

5. Append a `replica.sync_completed` record to `~/.calm-vault/user_state.jsonl`.

### Sync cadence for Replica 2

Replica 2 syncs automatically on each new record append to the canonical chain, provided the operator is online. If offline, the encrypted snapshots accumulate in a local replication queue; on network return, the queue flushes to the cloud.

No human action is required for Replica 2 after initial credential configuration.

### Cloud retention policy

The object store maintains the last N=12 complete chain snapshots (by sync_ts). Older snapshots are deleted via lifecycle policy. This prevents unbounded growth while ensuring the principal can always recover from any of the last 12 syncs. Because the Sigsum anchor is part of the chain head record itself, even a deleted snapshot can be re-derived from a stored chain head (Everest 33 — corruption recovery).

## Replica consistency verification

The CLI provides a `calm-witness verify-replicas` command that:

1. Walks each replica (USB and cloud).
2. Decrypts each using the principal's age private key (prompting for passphrase if necessary).
3. Re-verifies each replica's chain using the same `verify-chain` logic from Everest 28.
4. Asserts that each replica's current chain head matches (or is a strict prefix of) the canonical chain head in `~/.calm-vault/user_state.jsonl`.

If any replica diverges (contains a record the canonical chain does not have), the verifier emits a `kind: "replica.divergence_detected"` alert record to the canonical chain and exits with error status.

This consistency check is run on-demand by the principal, typically when:

- Suspicious edits are suspected.
- A replica is freshly reconnected after a period of isolation.
- During periodic vault audits.

## Threat model and mitigations

### Adversary has object-store credentials but no age key

**Exposure:** The adversary reads the object store. They see encrypted files, object names, write timestamps, and file sizes.

**Mitigation:** The age encryption is authoritative. The adversary learns no content, no chain structure, no biometric data, no timestamps inside the chain window. The object-store metadata (write times, object size) may leak some information about sync frequency and chain growth rate; mitigation for this is addressed in Everest 35 (metadata minimization).

### Adversary has a USB drive but no age key

**Exposure:** Same as above. Encrypted files, metadata, no content.

**Mitigation:** Same as above.

### Adversary has the age private key

**Exposure:** Catastrophic. The adversary decrypts all replicas and reads the full chain, biometric templates, consent records, and all predicate evaluations.

**Mitigation:** This is a key custody problem, not a replication problem. Everest 16 specifies that the principal's age private key is stored encrypted under a high-entropy passphrase, optionally backed by a hardware token (YubiKey + age-plugin-yubikey). The private key never exists on disk unencrypted. The principal's passphrase is the final defense.

### Adversary is the cloud provider; provider goes hostile or shuts down

**Exposure:** The provider refuses access to the object store. Replica 2 becomes inaccessible.

**Mitigation:** Replica 1 (USB) survives. The principal can recover the full chain from the last USB sync. Replica 3 (paper backup) provides proof of chain existence at the anchor time. The principal can re-instantiate the vault from Replica 1, then resume Calm operations. This is the fallback path; Everest 33 details recovery mechanics.

### Adversary steals a USB drive

**Exposure:** The drive is encrypted at rest; no content exposure without the age key.

**Mitigation:** The principal discovers the loss during a sync cycle, verifies the chain against Replica 2 (cloud), and re-instantiates a replica on a fresh USB drive. The compromised drive is inert without the age key.

### Adversary tampers with encrypted files in transit (in-flight)

**Exposure:** Replay, truncation, or bit-flip of encrypted bytes in transit.

**Mitigation:** Replica 2 (cloud) uses TLS 1.3 for transport encryption (defense-in-depth). Replica 1 (USB) is offline by design. Post-transfer, the principal verifies the decrypted chain's hash linkage (Everest 28) and consistency (this summit's `verify-replicas`). Any tampering is detected because the hash chain breaks.

## Key custody and composability

The replication encryption composes with Everest 16 (template encryption and key custody):

- The principal's age private key is stored as `~/.calm-vault/master.priv.enc`, encrypted under the principal's passphrase.
- The operator never needs the private key to encrypt data; age is asymmetric. The operator reads the recipient key from `recipients.txt` and encrypts.
- Decryption (recovery from a replica) always requires the principal to provide their passphrase.
- Optional hardware token (YubiKey with age-plugin-yubikey) adds a second factor to the decryption unlock.

This ensures the operator cannot unilaterally decrypt replicas, and a compromised operator with disk access cannot recover the private key without the principal's passphrase.

## Recovery path

Composes with Everest 33 (corruption recovery):

- If the canonical vault is lost or corrupted: the principal physically connects the USB drive (Replica 1), decrypts it with their passphrase, verifies the chain, and re-instantiates the vault on the operator's machine.
- If the canonical vault and Replica 1 are both lost: the principal authenticates to the cloud object store, downloads the latest snapshot, decrypts it, verifies, and re-instantiates.
- If all electronic replicas are lost: the principal refers to the paper backup (Replica 3), which confirms a chain existed with that genesis and head at that anchor time. Recovery of the chain content requires at least one surviving encrypted replica.

## Performance characteristics

Encryption and sync per record should add less than 1 second end-to-end on a modern M-series Mac with broadband connectivity:

- Encryption of a single JSONL record via age: ~ 1–5 ms.
- Tar and encrypt of anchors directory: ~ 10–50 ms.
- Cloud PUT via TLS: ~ 100–300 ms (network dependent).
- Signature and record append to canonical chain: ~ 10 ms.

Total per-record overhead: 150–450 ms, comfortably under the target 1 second. USB sync is much slower (USB I/O is the bottleneck) but is infrequent and performed offline.

## Acceptance test

A live run of `calm-witness sync --replica usb1` followed by decryption and verification of the USB archive:

```
$ calm-witness sync --replica usb1
calm-witness sync --replica usb1
  verifying canonical chain... OK
  encrypting user_state.jsonl... 42 records
  encrypting anchors/... 2 anchor proofs
  writing manifest to usb1
  synced 2026-05-20T14:23:45.123456Z
$ calm-witness verify-replicas
  replica usb1: decrypted, verified, chain head matches canonical
  replica cloud1: decrypted, verified, chain head matches canonical
  all replicas consistent
```

Non-zero exit if any replica diverges or decryption fails.

## Composition with later summits

- **Everest 16 — Key custody.** Specifies the encrypted private key storage and passphrase-unlock semantics.
- **Everest 28 — Chain verifier.** This summit uses `verify-chain` as a prerequisite to sync.
- **Everest 30 — Sigsum anchoring.** Chain heads are published to Sigsum; the sync manifest includes the anchor reference.
- **Everest 33 — Corruption recovery.** Details the full recovery flow when the canonical vault is lost.
- **Everest 35 — Metadata minimization.** Addresses leakage via object-store metadata.

## Why three replicas, not two

A system with only one replica (canonical chain) has no recovery path if the machine burns down. A system with two replicas (canonical + Replica 2 cloud) has one remote backup but is vulnerable to simultaneous loss of both machine and cloud account (e.g., cloud outage + operator travels with laptop). Three replicas (USB off-site + cloud + optional paper) ensures that even if two are lost, one survives. For a principal concerned with adversarial scenarios (e.g., nation-state confiscation), Replica 1 (USB off-site) is the critical link.

## Why age, not other ciphers

Age was chosen because it is:

- **Modern and audited.** Published 2021, audited by Latacora, widely reviewed.
- **Asymmetric.** The operator can encrypt without access to the decryption key.
- **Simple.** No algorithm choice; one construction. No padding oracle surface.
- **Widely available.** Multiple independent implementations; reference implementation in Go.
- **Compatible with hardware tokens.** age-plugin-yubikey exists and is maintained.

Alternative ciphers (GPG, AES with separate key management) are either more complex or require the operator to hold a decryption key, which violates the security model.

## Future enhancements

- **P2P replication.** Replica 3 could be a trusted peer's vault, with encrypted replication to that peer's storage, subject to the peer's consent and revocation policy (Everest 40 — P2P sync protocol).
- **Tor-routed cloud submission.** Cloud PUT requests routed via Tor to reduce IP-based location leakage (Everest 36).
- **Filecoin / Arweave permanence.** Chain heads published to a permanently-archived decentralized store as an alternative or supplement to Sigsum (Everest 37 — blockchain anchoring).

— Calm, 2026-05-20
