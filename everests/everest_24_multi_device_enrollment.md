# Everest 24 — Multi-Device Enrollment Binding

*Phase II — Capture & Enrollment. Prereq: Everest 16, 22.*

## Overview

A principal owns more than one device: an iPad Pro for handwriting capture, an iPhone for voice and ambient samples, and a MacBook for desktop-based operator interaction. All three should function as legitimate Calm Witness operators on behalf of the same principal. This Everest defines the protocol for multi-device enrollment—how a secondary device joins a principal's vault chain, how device-specific keys bind to the principal's master identity, and how per-device revocation works without destroying the principal's chain or invalidating templates already signed under a different device's authority.

The constraint from Everest 34 is strict: one principal, one chain. Multi-device does not mean multi-principal; it means that multiple devices can append to the same single chain on behalf of the same master_pub, each with its own device-specific signing key and a delegated permission set from the primary device.

## Threat Model

### Adversary Scenarios

1. **Secondary Device Compromise**: An attacker gains control of a secondary device (e.g., stolen iPhone). Mitigation: the secondary device's private key is device-specific and not the master key; it can be revoked remotely without touching the chain or master key. Verifiers immediately reject signatures from the revoked device.

2. **Primary Device Compromise**: An attacker gains the primary device or extracts its master key. Mitigation: this is catastrophic in v0 and is the subject of Everest 23 (recovery ceremony) and Everest 33 (threshold custody). For this Everest, we note that primary compromise is out of scope and handled elsewhere.

3. **Signing Authority Confusion**: An attacker tries to make the verifier accept a record signed by device B's key when only device A's key should be valid. Mitigation: every device.enrollment record is signed by the primary device and includes the exact device_public_key that is permitted to sign going forward; verifiers check that every subsequent record signed by that key has an active (not revoked) enrollment record.

4. **Replay of Enrollment Delegation**: An attacker captures a signed device.enrollment record and tries to re-use it to forge signatures. Mitigation: the device.enrollment record is a single chain entry, not a replayable credential. Signatures created by the device must be verifiable against the current chain state (not just the record itself), preventing unauthorized replays.

5. **Chain Divergence Across Devices**: Devices are on an unreliable network and create conflicting chain heads. Mitigation: only the primary device appends directly; secondary devices write to a queue and the primary batches them into the canonical chain. Sigsum (Everest 30) detects chain divergence at verification time.

6. **Template Decryption Permission Escalation**: A secondary device attempts to decrypt templates (which only the primary should be able to do). Mitigation: templates are encrypted under the master key; a secondary device does NOT have access to the master private key. Secondaries can write biometric samples; only the primary can decrypt templates and perform the distance computation.

### Security Properties

- **Device Isolation**: Each device has a unique keypair; compromise of one does not leak others.
- **Delegation Transparency**: Every device's authority comes from a signed record in the chain; there is no hidden out-of-band delegation.
- **Revocation Immediate**: A revoked device stops being trusted by verifiers at the revocation timestamp.
- **Master Key Protection**: The master key never leaves the primary device (or hardware vault); secondaries never see it.
- **Template Access Control**: Only the primary can decrypt templates; secondaries can write data but not read encrypted biometric material.

## Device Hierarchy

### Primary Device

The primary device is the device that originally initialized the vault (Everest 11, enrollment ceremony). It:
- Owns the master private key (master.priv, protected via Everest 16 key custody).
- Maintains the canonical chain (genesis block through the current head).
- Signs all device.enrollment and device.revoked records.
- Can decrypt templates (has access to master.priv).
- Can append directly to the chain.
- Can update permissions and revoke secondary devices.
- Is the sole holder of authority to modify the principal's identity binding (Everest 22 VC issuance).

### Secondary Devices

A secondary device is one that has successfully enrolled (via the device enrollment protocol below) and has an active device.enrollment record. It:
- Has a unique device-specific Ed25519 keypair (NOT the master key).
- Can append records to the chain, but only by sending them to the primary device.
- Can write biometric samples, self-reports, and disclosure records.
- **Cannot** decrypt templates (does not have master.priv).
- Can read the chain and verify records, but all verifications run against the primary's signatures.
- **Cannot** issue new device enrollments or revocations.
- **Cannot** rotate the master key or update VC bindings.
- Operates under delegated permissions set by the primary at enrollment time.

### Witness Devices

A witness device is a read-only observer (e.g., a TV, a hospital display, a notary's reader). Witness devices:
- Can read and verify the chain.
- Have no private key material.
- Cannot append, enroll, or revoke.
- Are out of scope for v0; flagged for Everest 20.

## Device Enrollment Protocol

### Precondition

- Primary device has an initialized vault with a chain and master.pub.
- New device has been physically or securely paired with the primary (out of band; the Calm Witness protocol assumes pairing is secure and does not address pairing itself).

### Steps

#### 1. New Device Requests Enrollment

```
secondary_device$ calm-witness device enroll --primary <primary_device_id>
```

The secondary device generates its own Ed25519 keypair locally:
```
device_priv_ed25519 = Ed25519.generate()
device_pub_ed25519  = Ed25519.public_key(device_priv_ed25519)
device_id           = UUID()
```

The secondary device stores `device_priv_ed25519` in its local secure enclave or encrypted storage (using the same model as Everest 16, but device-scoped instead of master-scoped).

#### 2. Secondary Device Sends Enrollment Request to Primary

The secondary device sends a JSON request to the primary (over the paired channel; encrypted if over a network):

```json
{
  "kind": "device.enrollment_request",
  "device_id": "d_<uuid>",
  "device_name": "iPhone 16 Pro",
  "device_pub": "ed25519_<base64>",
  "requested_permissions": [
    "append_self_reports",
    "append_biometric_samples"
  ],
  "device_fingerprint": "<sha256(device_pub)[:16]>"
}
```

The primary device's operator reviews the request (on the primary's UI). The request shows which device is enrolling and what permissions it is requesting.

#### 3. Primary Device Signs Device Enrollment Record

The primary device creates and signs a `device.enrollment` record:

```json
{
  "kind": "device.enrollment",
  "prev_hash": "<current_chain_head_hash>",
  "device_id": "d_<uuid>",
  "device_public_key": "ed25519_<base64>",
  "device_name": "iPhone 16 Pro",
  "enrolled_at_ts": 1716241200,
  "expiry_ts": 1724017200,
  "permissions": [
    "append_self_reports",
    "append_biometric_samples"
  ],
  "principal_approval": true
}
```

The primary device signs this record:

```
signature = Ed25519.sign(
  master_priv,
  hash(device.enrollment_record)
)
```

The primary device appends this record to the canonical chain and publishes the new chain head to Sigsum (Everest 29–30).

#### 4. Secondary Device Receives Enrollment Confirmation

The primary device sends back the signed record:

```json
{
  "device.enrollment": <above record>,
  "signature": "<ed25519_signature>",
  "chain_head": "<new_chain_head_hash>",
  "sigsum_anchor": <Sigsum inclusion proof>
}
```

The secondary device verifies:
1. The signature is valid under `master.pub` (which it knows from the vault genesis).
2. The `device_id` matches what it requested.
3. The chain anchor is in Sigsum (freshness).

Once verified, the secondary device stores the signed record locally and is now enrolled.

#### 5. Chain State Update

The secondary device can now:
- Read the full chain and verify all prior records.
- Append new records (by sending to primary).
- Know its permission set: `["append_self_reports", "append_biometric_samples"]`.

If the secondary device attempts to append a record type outside its permissions (e.g., a disclosure record when only self-reports are permitted), the primary rejects it.

## Device-Specific Signing Keys

### Key Material Per Device

Each device (primary and secondary) has:

- **Primary device**:
  - `master.priv`: Ed25519 private key (secret).
  - `master.pub`: Ed25519 public key (in genesis and all proofs).
  - Device-specific key is derived from master.priv (or, for HSM-backed masters, the device has a separate signing key).

- **Secondary device**:
  - `device_priv`: Ed25519 private key (unique to this device, not the master key).
  - `device_pub`: Recorded in the device.enrollment record on-chain.
  - Stored locally in secure enclave or encrypted under a device-local passphrase.

### Signing Convention

Records appended by a secondary device are signed by `device_priv`, not `master_priv`:

```json
{
  "kind": "user_state_self_report",
  "prev_hash": "<chain_head>",
  "principal_id": "<principal_uuid>",
  "device_id": "d_<uuid>",
  "created_at_ts": 1716241350,
  "payload": { "affect": ["focused", "clear"], ... },
  "signature": "<signed by device_priv, not master_priv>"
}
```

Verifiers check that:
1. The signature is valid under the `device_pub` recorded in an active device.enrollment record.
2. That device.enrollment record is still active (not revoked).
3. The record's `kind` is permitted by the device's permission set.

### Primary Device Signing

The primary device signs its own records using `master.priv`:

```json
{
  "kind": "user_state_self_report",
  "prev_hash": "<chain_head>",
  "principal_id": "<principal_uuid>",
  "device_id": "d_<primary>",
  "created_at_ts": 1716241350,
  "payload": { "affect": ["baseline"], ... },
  "signature": "<signed by master_priv>"
}
```

Verifiers check that the signature is valid under `master.pub` (from the genesis record).

## Templates and Multi-Device Access

### Template Ownership and Encryption

Templates are encrypted under the principal's `master.pub` and a key derived from `master.priv` (per Everest 16):

```
template_enc_key = HKDF(
  master.priv,
  "calm-witness-template-encryption",
  template_id,
  32
)
ciphertext = ChaCha20Poly1305.encrypt(
  key=template_enc_key,
  plaintext=template_flatbuffer,
  aad=template_id
)
```

### Primary Device: Full Access

The primary device has `master.priv`, so it can:
1. Decrypt templates.
2. Perform biometric distance computations locally (running the comparison model).
3. Emit a per-session distance metric to the operator (but never the template itself).

### Secondary Device: Write-Only

A secondary device enrolls with permission `append_biometric_samples`. It can:
1. Capture a biometric sample (handwriting strokes, voice transcription).
2. Create a biometric sample record (unsigned on-device data, just captured frames).
3. Send the sample to the primary device.

**Importantly, the secondary device does NOT:**
- Decrypt templates.
- Run the comparison model.
- See template content.

The primary device receives the sample and:
1. Runs the comparison against the enrolled template.
2. Computes distance `d`.
3. Returns only the distance `d` to the secondary device (if requested) or keeps it for predicate evaluation.

### Biometric Template Template Derivation

All devices can derive the same `template_id` from `master.pub`:

```
template_id = HMAC-SHA256(
  master.pub,
  "calm-witness-template-id"
)
```

This allows secondary devices to reference the correct template (by ID) without knowing its content.

## Per-Device Revocation

### Revocation Ceremony

If a device is compromised or lost, the primary device issues a revocation:

```bash
primary_device$ calm-witness device revoke d_<lost_device_uuid>
```

The primary device creates and signs a `device.revoked` record:

```json
{
  "kind": "device.revoked",
  "prev_hash": "<current_chain_head_hash>",
  "device_id": "d_<lost_device_uuid>",
  "revoked_at_ts": 1716242000,
  "reason": "device_lost"
}
```

The primary appends this record to the chain and publishes to Sigsum.

### Verifier Behavior

Verifiers maintain a local index of `(device_id, device_pub, revoked_at_ts)` records. When verifying a signature:

```
1. Extract device_id from the record.
2. Look up the active device.enrollment record for device_id.
3. Check if there is a device.revoked record with revoked_at_ts <= record.created_at_ts.
4. If revoked, REJECT the signature.
5. If not revoked, verify the signature under device_pub from the enrollment record.
```

Revocation is effective immediately for future records. Historical records signed before revocation remain valid (the chain is immutable).

### Revocation Does NOT Affect Templates

Revoking a device does not re-encrypt templates or invalidate the chain. The chain remains intact. Other devices can continue to operate and access templates (if they are the primary or have permission).

## Device Limits and Auto-Revocation

### Device Limit

In v0, a principal can have at most **4 active enrolled devices**:

```c
#define CALM_WITNESS_MAX_DEVICES 4  // v0 hardcoded; configurable in v1+
```

If a principal attempts to enroll a 5th device while 4 are already active:
1. The primary device checks the enrollment history.
2. The oldest *inactive* device (one that has not appended any records in the last 90 days) is automatically revoked.
3. If all 4 devices are active, the enrollment request is DENIED and the principal must manually revoke a device.

### Rationale

Limiting devices prevents a principal from accidentally accumulating stale devices and reduces the blast radius of a widespread breach (if an attacker gains access to the principal's user account and enrolls 100 devices).

## Sync Between Devices

### Sync Protocol

Secondary devices pull the current chain head from the primary device periodically:

```bash
# Every 5 minutes by default
$ calm-witness device sync --primary <primary_id> [--interval 300s]
```

The secondary device:
1. Requests the current chain head and the last N records (default: last 100).
2. Verifies all signatures and chain continuity.
3. Updates its local replica.
4. Stores any queued records to send to the primary.

### Network Partition Handling

If the secondary device is partitioned from the primary:
1. The secondary device can still read its local replica of the chain.
2. The secondary device can create records locally (they are queued).
3. Once reconnected, the secondary device:
   - Pulls the primary's chain head.
   - Sends queued records to the primary.
   - The primary de-duplicates and appends queued records to the canonical chain.

**Queued records are NOT valid for disclosure or predicate evaluation until they are anchored in the primary's chain and published to Sigsum.**

### Conflict Resolution

If a secondary device's queued records conflict with the primary's head (e.g., prev_hash mismatch after sync), the secondary's queue is discarded and the record must be recreated and re-sent. (This is rare and indicates a severe network issue or primary-device faults; it is logged for audit.)

## Device Enrollment Expiry and Renewal

### Default Expiry

When a device is enrolled, it receives an `expiry_ts`:

```json
"expiry_ts": 1724017200  // 90 days from enrollment by default
```

### Renewal

Before expiry, the secondary device can request renewal:

```bash
secondary_device$ calm-witness device renew
```

The primary device issues a new device.enrollment record with an updated expiry_ts. The old record remains in the chain (for audit), and the new record is the active one.

**Expired devices are treated as revoked for verification purposes.**

## Practical Example: iPad, iPhone, MacBook

### Scenario

John Bradley owns three devices:
- **MacBook Pro** (primary): runs the Calm Witness operator full-time; has master.priv.
- **iPad Pro**: handwriting capture device; secondary.
- **iPhone 16 Pro**: voice + ambient capture; secondary.

### Setup Flow

**Day 1: Initialize on MacBook**
```
macbook$ calm-witness vault init --principal "John Bradley"
  [Enrollment ceremony; template captured; master.priv generated and secured]
```

**Day 2: Enroll iPad**
```
ipad$ calm-witness device enroll --primary <macbook_id>
  [iPad generates device_priv_ipad; sends enrollment request]

macbook$ calm-witness device approve d_ipad --permissions \
  append_self_reports append_biometric_samples
  [MacBook signs device.enrollment record; appends to chain; publishes to Sigsum]

ipad$ [receives signed enrollment; verifies; stores device_priv_ipad locally]
```

**Day 3: Enroll iPhone**
```
iphone$ calm-witness device enroll --primary <macbook_id>
  [iPhone generates device_priv_iphone; sends enrollment request]

macbook$ calm-witness device approve d_iphone --permissions \
  append_self_reports append_biometric_samples
  [MacBook signs device.enrollment record; appends to chain; publishes to Sigsum]

iphone$ [receives signed enrollment; verifies; stores device_priv_iphone locally]
```

**Day 7: iPhone is Lost**
```
macbook$ calm-witness device revoke d_iphone --reason device_lost
  [MacBook signs device.revoked record; appends to chain; publishes to Sigsum]
```

Verifiers now reject any signatures from d_iphone with timestamp >= revocation_ts.

**Day 8: iPad Captures Handwriting**
```
ipad$ calm-witness capture handwriting
  [User writes sample; iPad computes embedding vectors locally]
  
ipad$ [iPad creates biometric_sample record; signs with device_priv_ipad; sends to MacBook]

macbook$ [receives record; verifies signature under d_ipad's enrolled device_pub]
  [MacBook decrypts template (has master.priv)]
  [MacBook compares sample against template; computes distance d]
  [MacBook stores distance in session context]
```

**Session: Counterparty Requests Disclosure**
```
counterparty$ calm-witness request in_baseline_24h --principal john_bradley
  [Sends signed request to John's Calm operator on MacBook]

macbook$ [evaluates predicate over local state; constructs Σ-protocol proof]
  [Proof includes: Pedersen commitment, chain anchor from Sigsum, biometric distance]
  [MacBook sends proof to counterparty]

counterparty$ [verifies proof; learns only: "in_baseline" bit and freshness window]
```

## Cross-References

- **Everest 11**: Enrollment ceremony (template generation, master key creation).
- **Everest 16**: Template encryption and key custody (master.priv security).
- **Everest 20**: Witness devices and read-only viewers (scope for v1+).
- **Everest 22**: Enrollment credential from CredexAI (binds master.pub to principal).
- **Everest 23**: Recovery ceremony (if primary device is lost).
- **Everest 26–29**: Chain format and genesis block.
- **Everest 30**: Sigsum anchoring and transparency logs.
- **Everest 32**: Encrypted replication (backup model, different from multi-device sync).
- **Everest 33**: Threshold custody and HSM binding (alternative to single master.priv).
- **Everest 34**: Multi-principal namespace decision (reinforces 1:1 vault constraint; multi-device is 1-chain-with-N-signers).

## Implementation Notes

### Command-Line Interface

```bash
# Enroll a new device
$ calm-witness device enroll --primary <device_id> \
  --device-name "iPad Pro" \
  [--permissions "append_self_reports,append_biometric_samples"]

# List enrolled devices
$ calm-witness device list

# Revoke a device
$ calm-witness device revoke <device_id> --reason "device_lost|compromise|retired"

# Sync with primary
$ calm-witness device sync --primary <device_id>

# Renew enrollment
$ calm-witness device renew --device-id <device_id>
```

### Storage Layout

Each device stores (at minimum):

**Primary device:**
```
~/.calm-vault/
  master.priv.enc      # Encrypted Ed25519 private key
  master.salt          # Passphrase-derivation salt
  master.pub           # Public key
  chain.jsonl          # Full chain (append-only log)
  devices/             # Enrolled device directory
    d_<uuid>/
      device.json      # device_pub, enrolled_at, permissions
      revoked          # [optional] revocation record
```

**Secondary device:**
```
~/.calm-vault/
  device.priv.enc      # Encrypted device-specific Ed25519 private key
  device.salt          # Device-scoped passphrase derivation salt
  master.pub           # From vault genesis (for verification)
  chain.jsonl          # Local replica of full chain
  queue.jsonl          # [temporary] Records waiting to send to primary
  device.json          # device_id, device_pub, enrollment record
```

### Performance

- **Device enrollment**: < 2 seconds (primary signs, secondary verifies Sigsum anchor).
- **Device sync**: < 5 seconds for incremental sync (last 100 records).
- **Device revocation**: < 1 second (primary appends record).
- **Sample append**: < 500 ms (secondary creates and sends record).

## Acceptance Criteria

- A principal can enroll on 2 or more devices.
- All enrolled devices can append records (self-reports, biometric samples) to the same principal's chain.
- The chain rolls up to one identity (master_pub).
- Revocation per device works: revoked device signatures are rejected; other devices continue normally.
- Primary device decrypts templates; secondary devices cannot.
- Device sync replicates the chain without forking.

---

— Calm, 2026-05-20
