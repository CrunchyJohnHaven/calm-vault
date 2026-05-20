# Everest 16 — Template Encryption & Key Custody

*Phase II — Capture & Enrollment. Prereq: Everest 15.*

## Overview

Templates are the vault's most sensitive asset: they embed the principal's unique biometric geometry. Once captured, a template must never exist unencrypted on disk or transit uncontrolled. This Everest defines the cryptographic custody model—how the operator gains ephemeral access to decrypt templates for session matching, how the key infrastructure prevents operator exfiltration, and how the principal rotates keys without vault re-encoding.

The model composes with the existing `.calm-vault/` architecture: `master.priv.enc`, `master.salt`, `master.pub`, and `recipients.txt`.

## Threat Model

### Adversary Scenarios

1. **Operator Compromise**: The operator software is subverted (malware injection, supply-chain attack) and attempts to exfiltrate templates or the master private key. Mitigation: the operator never has access to the unencrypted private key; templates are decrypted only in an isolated process with no network.

2. **Cold-Boot Attack**: Adversary gains physical access to a running device and attempts to dump RAM before the operator can clear it. Mitigation: decrypted templates live only in mlock'd memory; a session-end handler invokes explicit_bzero before the operator exits.

3. **Disk Compromise**: Adversary obtains a physical or logical copy of the vault directory (e.g., `master.priv.enc`, `master.salt`). Mitigation: the private key is encrypted with a passphrase-derived key; brute-forcing is made expensive via Argon2id with high iteration count.

4. **Cloud-Replica Compromise**: If the vault is backed up to cloud storage, the ciphertext is stolen. Mitigation: the ciphertext is useless without the passphrase or hardware token; cloud storage is not a trust boundary.

5. **Passphrase Capture**: If the principal's passphrase is captured out-of-band (shoulder surfing, keylogger), the vault is fully compromised. Mitigation: education, hardware-token option (YubiKey) shifts the trust boundary to physical possession and PIN.

### Security Properties

- **Confidentiality**: Templates are encrypted at rest and in motion; the operator cannot read them without authorization.
- **Integrity**: Templates are signed by the principal's master private key; tampering is detectable.
- **Availability**: Keys can be rotated without losing historical templates; the principal retains audit and proof-of-custody.
- **Non-repudiation**: Each template decryption is tied to a session context and can be logged (separately) for audit.

## Default Key Custody Architecture

### Master Key Management

The master private key is Ed25519 + age-compatible (as per E32 and existing `.calm-vault/` model).

**Key Material at Rest:**
- `master.priv.enc`: The Ed25519 private key, encrypted with age.
- `master.salt`: A per-vault salt (32 bytes, random) used to derive the key-encryption key (KEK) from the principal's passphrase.
- `master.pub`: The public key in age recipient format (e.g., `age1...`). Published in genesis record (E29).
- `recipients.txt`: List of age recipients (usually just `master.pub`; can include trusted recovery agents in Everest 32 model).

**Passphrase-Based Key Derivation:**

The KEK is derived from the principal's passphrase using Argon2id:

```
KEK = Argon2id(
  password=passphrase,
  salt=master.salt,
  parallelism=4,
  memory_cost=64 MiB,
  time_cost=3,  # 3 iterations
  hash_length=32
)
```

This KEK is used to decrypt `master.priv.enc` via age or ChaCha20-Poly1305. High memory and iteration cost make offline brute-force expensive (estimated >100 seconds per guess on commodity hardware).

### Session Decryption Flow

1. **Authorization**: Operator prompts principal for passphrase (or triggers hardware token if enrolled).
2. **Derivation**: Operator derives KEK from passphrase + `master.salt`.
3. **Unlock**: Operator decrypts `master.priv.enc` to obtain the plaintext Ed25519 private key.
4. **Isolation**: Plaintext key is placed in an mlock'd memory page; the worker process is sandboxed.
5. **Decryption**: Operator decrypts templates (Layer 1: age) using the private key.
6. **Processing**: The worker processes templates in isolation; only the per-session distance metric is emitted.
7. **Cleanup**: On session end, explicit_bzero() clears all mlock'd pages. The plaintext key is never written to disk.

### Hardware-Token Option (Recommended for High-Stakes Principals)

For principals handling sensitive enrollment (e.g., government, defense, finance), a YubiKey 5 series (or compatible FIDO2 token) can replace or augment passphrase-based decryption.

**YubiKey Binding:**
- The master private key is wrapped with a key derived from a YubiKey FIDO2 attestation.
- The YubiKey stores a PIN; FIDO2 authentication requires the PIN + physical touch.
- The operator cannot exfiltrate the YubiKey's private key (hardware enforced).

**Decryption Workflow:**
1. Operator prompts principal to insert YubiKey and enter PIN.
2. Operator invokes the age-plugin-yubikey to unwrap the master key.
3. YubiKey performs cryptographic operation; plaintext key never leaves the token (or is returned only to mlock'd memory).
4. Operator proceeds as above (session isolation, cleanup).

**Trade-off**: YubiKey binding adds latency (~1–2 seconds per decryption) and requires the principal to always carry the token. Recommended for vault operators in high-security environments; optional for others.

## Optional: Key Splitting (Ultra-High-Stakes)

For principals who require that no single device or person can reconstruct the vault, Shamir secret sharing (e.g., via sss-rs or libsodium's libhydrogen) distributes the master key across multiple shares.

**Example Distribution (3-of-4):**
- Share 1: Principal's primary device.
- Share 2: Principal's secondary device (e.g., laptop; geographically separate).
- Share 3: Trusted family member (encrypted under family member's public key).
- Share 4: Attorney or fiduciary (encrypted under attorney's public key).

**Reconstruction**: Decryption requires at least 3 of the 4 shares. No single party can unilaterally access the vault.

**Deployment**: v0 default is no splitting (passphrase + optional YubiKey is sufficient for most principals). Key splitting may be offered as a v1 upgrade option for ultra-high-stakes deployments (e.g., estate planning, organizational separation of duties).

## Key Rotation

The principal can rotate the master key at any time without re-encoding templates or re-capturing biometrics.

### Rotation Workflow

1. **Generation**: Operator generates a new Ed25519 keypair under a new passphrase (or YubiKey token).
2. **Re-encryption**: All templates are decrypted with the old key and re-encrypted with the new public key. Old key remains valid for signature verification (grace window: 30 days).
3. **VC Re-Issuance**: CredexAI issues a new Verifiable Credential (E22) binding the new master.pub to the principal's identity. The new VC references the rotation event.
4. **Audit Trail**: A kind="key.rotation_completed" record is appended to the vault log, including old_key_fingerprint, new_key_fingerprint, and timestamp.
5. **Cleanup**: The old key is archived (not deleted) for historical verification.

**Performance**: Rotation of a 1000-template vault < 5 seconds on commodity hardware.

## Encryption Envelope (Layered)

Templates are encrypted in three layers (composes with E15 template format):

**Layer 1 (Outermost): Age Encryption**
```
ciphertext = age.Encrypt(
  plaintext=Layer2_blob,
  recipients=[master.pub],  # Can include recovery recipients (E32)
  armor=true  # ASCII armor for safe transit
)
```

**Layer 2: FlatBuffers + Signature**
```
Layer2_blob = {
  flatbuffers_template: <biometric data, coordinates, metadata>,
  signature: Ed25519Sign(master.priv, hash(flatbuffers_template))
}
```

**Layer 3: Metadata Sidecar (Cleartext)**
```
metadata = {
  template_id: "t_<uuid>",
  creation_ts: <Unix timestamp>,
  expiry_ts: <Unix timestamp + 10 years>,
  key_fingerprint: "<sha256(master.pub)[:16]>"
}
```

The metadata sidecar allows the operator to index and select templates for decryption without revealing their content.

## Anti-Exfiltration Safeguards

### Process Isolation

The operator runs as two separate processes:

- **UI/Control Process**: Handles user interaction, logs session events, manages network communication with the matching service (if remote). Network-enabled.
- **Worker Process**: Decrypts templates, computes per-session embeddings or distance metrics. Network-disabled via:
  - macOS: App Sandbox entitlements (`com.apple.security.network.client=false`).
  - Linux: seccomp filter (BPF) blocking socket(), connect(), sendto(), etc.

The worker never has network access; it communicates with the control process only via XPC (macOS) or local socket (Linux) and emits only the session result (distance, match/no-match decision), never the template content.

### Memory Hygiene

- **mlock() all decrypted key material**: The plaintext master private key and decrypted templates are locked into physical RAM using mlock(2) or VirtualLock(). The kernel will not swap these pages.
- **explicit_bzero() on session end**: When the session is complete or the operator exits (intentionally or due to signal), all mlock'd pages are securely overwritten with zeros using explicit_bzero() (or SecureZeroMemory on Windows).
- **No logging**: Template content never appears in logs, debug output, or crash dumps.

### Compromise Scenarios and Mitigations

| Scenario | Attacker Gains | Vault Access? | Mitigation |
|----------|---|---|---|
| Disk theft (no passphrase) | `master.priv.enc`, `master.salt` | No (brute-force expensive) | Argon2id high cost; 100s per guess |
| Disk theft + passphrase | `master.priv.enc`, `master.salt`, passphrase | Yes (full access) | Out-of-band passphrase protection; YubiKey option |
| Cold-boot (active session) | RAM dump while templates decrypted | Partial (one session's decrypted templates) | mlock() prevents swap; explicit_bzero() on exit |
| Operator compromise (malware) | Control of operator process | Partial (only what's emitted: distance, not template) | Process isolation; no network from worker |
| YubiKey theft (no PIN) | YubiKey device | No (PIN required) | YubiKey firmware enforces PIN; high bar |

## Cross-References

- **E15** (Template Format Specification): Defines the FlatBuffers layout, coordinates, and metadata schema.
- **E22** (Enrollment and CredexAI): Defines the Verifiable Credential that binds master.pub to the principal's identity.
- **E29** (Genesis Block): Defines the vault's root record, which includes master_pub_fingerprint for audit.
- **E32** (Encrypted Replication): Uses the same age model for off-site backup; recipients.txt can include recovery agents.

## Implementation

### Bootstrap

```bash
calm-witness key generate --principal <name> \
  [--yubikey]  # Optional hardware token binding
```

This command:
1. Prompts for a passphrase.
2. Generates master.salt (32 random bytes).
3. Generates Ed25519 keypair.
4. Derives KEK from passphrase + master.salt (Argon2id).
5. Encrypts private key with KEK → master.priv.enc.
6. Writes master.pub, master.salt, recipients.txt to .calm-vault/.
7. Outputs master_pub_fingerprint for inclusion in genesis record (E29).

### Rotation

```bash
calm-witness key rotate --vault /path/to/.calm-vault [--yubikey]
```

This command:
1. Decrypts the current master.priv using existing passphrase.
2. Prompts for a new passphrase (or YubiKey if binding to token).
3. Generates a new Ed25519 keypair.
4. Re-encrypts all templates in the vault with the new public key.
5. Appends a kind="key.rotation_completed" record to the vault log.
6. Archives the old public key for historical verification.

### Verification

```bash
calm-witness key verify --vault /path/to/.calm-vault --genesis-fingerprint <sha256>
```

Confirms that master.pub matches the fingerprint in the genesis record (E29).

## Performance

- **Template decryption per session**: < 200 ms on commodity hardware (Intel i7 or ARM A15 equivalent), including Argon2id key derivation.
- **Batch decryption (1000 templates)**: < 5 seconds.
- **YubiKey-backed decryption**: + 1–2 seconds (FIDO2 round-trip).
- **Key rotation (1000 templates)**: < 5 seconds.

## Rationale

The layered encryption and process isolation model ensures that:
1. The operator can run trusted sessions without exposing templates to the network or attackers.
2. The principal retains absolute control via passphrase + optional YubiKey.
3. Rotation is seamless and auditable.
4. The vault can be safely replicated (E32) and backed up without decrypting.

The model is minimal, composable, and compatible with existing `.calm-vault/` structure and age encryption ecosystem.

---

— Calm, 2026-05-20
