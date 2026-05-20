# Everest 23 — Recovery From Total Enrollment Loss

*Phase II — Capture & Enrollment. Prereq: Everest 20, 22.*

## One-line spec

When the principal is alive and contactable but all devices are lost, inaccessible, or stolen, and the vault is unrecoverable, a tested procedure using witness re-attestation and optional encrypted replicas restores cryptographic identity continuity on new hardware.

---

## §1. Scenarios in scope

**S1: Hardware device destroyed.** The device containing the principal's vault is destroyed by fire, water, or physical damage, and no backup of the vault exists in the principal's possession.

**S2: Device stolen with encrypted vault.** The device is stolen by an adversary. The vault is encrypted at rest, but the principal fears the encrypted vault may be compromised and chooses not to decrypt it on new hardware.

**S3: Master key passphrase forgotten.** The principal has lost the passphrase to the master private key (age encryption key), making all encrypted replicas indecipherable even if they survive. The passphrase is not recoverable (not written anywhere, not with the witnesses, not in the principal's recovery kit).

**S4: Multiple device losses simultaneously.** The principal has suffered loss of multiple devices in a single incident (e.g., fire, accident, or theft affecting a home and office), and all backup media (USB, cloud credentials) were lost with them.

**Out of scope:** Principal deceased (covered separately under Everest 21, succession protocol v1+).

---

## §2. Preconditions for recovery

Successful recovery requires at least one of the following resource sets to exist outside the lost device:

### If S1 or S2 (device lost, replica survives)

- **Encrypted replica intact:** At least one copy of `user_state.jsonl.age` and `anchors.tar.age` survives on USB, cloud storage, or paper backup (per Everest 32).
- **Master key accessible:** The principal's age private key is recoverable — encrypted in the principal's head (passphrase + memory) or stored on a hardware token separate from the device.
- **Chain head in Sigsum:** The last chain-head anchor is retrievable from the public Sigsum transparency log, verifiable without the principal's private key.

### If S3 (passphrase lost)

- **Recovery catastrophic.** The encrypted replica cannot be decrypted; the old master key is inaccessible.
- **Requirement:** A fresh enrollment ceremony (Everest 11) must occur, establishing a new master key and new genesis block.
- **Identity continuity:** Proven only via witness re-attestation, not cryptographic continuity.

### If S4 (multiple losses)

- **If a replica survived + passphrase known:** Treat as S1/S2 recovery.
- **If no replica survived + passphrase known:** The principal's age key is in head only. A new chain can be started by recovering the public components (age recipient key, certificate) from witness attestations or CredexAI records.
- **If no replica survived + passphrase lost:** Catastrophic; fresh enrollment required.

---

## §3. Recovery decision tree

```
┌─ Principal reports loss (out-of-band channel)
│
├─ Can principal recall the master key passphrase?
│  │
│  NO → Catastrophic (S3): proceed to §5
│  │
│  YES ↓
│
├─ Does at least one encrypted replica exist and is it accessible?
│  │
│  NO → Check if public chain head in Sigsum and witness attestations recoverable
│  │     │
│  │     Recoverable → S4a: new chain with witness continuity (§6)
│  │     │
│  │     Not recoverable → Catastrophic: proceed to §5
│  │
│  YES ↓
│
├─ S1/S2 Recovery (decrypt replica, restore, continue chain) (§4)
│
└─ Proceed to procedural steps
```

---

## §4. S1/S2 recovery: device loss with surviving replica

**Scenario:** Hardware destroyed or stolen. Encrypted replica exists. Passphrase is known.

### Preconditions met
- Replica exists (USB, cloud, or paper reconstruction).
- Principal's age private key is accessible (passphrase in head).
- Chain head is recorded in Sigsum.

### Recovery steps

**Step 1: Principal initiates recovery via out-of-band channel.**

The principal contacts the Calm operator (or designated recovery coordinator) through a secure channel established during enrollment (e.g., voice call with identity verification, pre-agreed email address, hardware token contact). The principal provides:
- Assertion of identity (name, enrollment date, witness names, or biometric details not previously disclosed).
- Report of loss (scenario, date, approximate time last accessed).
- Availability of replica location (USB with friend, cloud bucket credentials, etc.).

**Step 2: Operator marks lost VC as revoked.**

The operator submits a revocation request to CredexAI with the principal's enrollment VC. The VC is added to the revocation chain, and a `kind: "enrollment.revoked"` record is appended to Sigsum (per Everest 78). This prevents any future proof over the old master key from being accepted by counterparties.

**Step 3: Principal decrypts replica and verifies chain.**

On new hardware, the principal:
- Installs `calm-witness` from a trusted package repository (gpg-verified signature).
- Retrieves the encrypted replica from USB or cloud.
- Decrypts the replica using the master key passphrase:
  ```
  age --decrypt -i ~/.calm-vault/master.priv.enc -o user_state.jsonl.age > user_state.jsonl
  ```
- Verifies the entire chain using `calm-witness verify-chain`, which checks:
  - All hash links are valid (no tampering).
  - The chain head matches the Sigsum inclusion proof.
  - The principal's identity credential is still valid (not revoked).

If any check fails, recovery aborts, and the principal must contact a recovery auditor.

**Step 4: Restore vault on new hardware.**

The operator places the decrypted chain at `~/.calm-vault/user_state.jsonl` on the new device. The biometric templates, recipient keys, and Sigsum anchors are restored from the replica. The vault is ready for normal operation.

**Step 5: Append recovery record to chain.**

A new record is appended to the chain:
```json
{
  "seq": <next_seq>,
  "ts": "2026-05-20T15:00:00Z",
  "kind": "identity.recovery_completed",
  "scenario": "s1",
  "old_device_lost_at": "2026-05-20T12:00:00Z",
  "recovery_performed_on": "new-device-hostname",
  "new_master_key": false,
  "old_vc_revoked": true,
  "recovery_witnessed": false,
  "notes": "Hardware destroyed in flood; replica decrypted successfully from USB backup.",
  "prev_hash": "...",
  "record_hash": "..."
}
```

**Step 6: Publish chain head to Sigsum.**

The operator publishes the recovery record's chain head to Sigsum (Everest 30) and stores the inclusion proof.

**Step 7: Notify counterparties (optional).**

The operator may send a `kind: "recovery.completed_alert"` disclosure notification to known counterparties (Everest 78), signed by the principal's master key, confirming that recovery has occurred and that the chain is still under the principal's control.

---

## §5. S3/S4 recovery: catastrophic (new enrollment required)

**Scenarios:** S3 (passphrase lost), S4 (multiple losses + replica lost), or vault entirely inaccessible.

**Precondition:** The old master key is unrecoverable. A fresh cryptographic identity must be created.

### Recovery steps

**Step 1: Principal requests new enrollment ceremony.**

The principal contacts the Calm operator and witnesses via the secure channels established at original enrollment. The principal provides:
- Identity assertion (sufficient to convince the witnesses they are the same human).
- Explanation of loss (passphrase forgotten, devices stolen, etc.).
- Request for new enrollment ceremony.

**Step 2: Witnesses re-attest under Everest 20 protocol.**

The original witnesses (Tier 1 notary and Tier 2 designated person) are recontacted. They re-perform the attestation ceremony:
- **Notary:** Re-verifies the principal's legal identity (photo ID) and notarizes a new declaration of presence and uncoercion.
- **Family/designated:** Re-attests to the principal's presence, identity, and voluntary participation.

Both witnesses sign a new attestation:
```json
{
  "kind": "enrollment.recovery_re_attestation",
  "original_enrollment_date": "2025-12-15",
  "original_enrollment_vc_id": "vc_...",
  "re_attestation_date": "2026-05-20",
  "recovery_scenario": "s3",
  "witness_declares": "I confirm this person is the same principal I attested to on [original date]. They remain uncoerced.",
  "witness_signature": "..."
}
```

**Step 3: New enrollment ceremony.**

A fresh enrollment ceremony (Everests 11, 14) occurs on new hardware:
- Principal produces new handwriting and voice-transcription templates.
- New master key pair (age asymmetric key) is generated.
- New `master.priv.enc` is encrypted with a newly chosen passphrase.

**Step 4: CredexAI issues new credential.**

The new enrollment package is submitted to CredexAI (Everest 22) with the witness re-attestations attached. CredexAI issues a new `CalmWitnessPrincipalCredential`, with the same principal identity but a new master public key and new template commitments.

**Step 5: New genesis block with predecessor reference.**

A new chain genesis block (Everest 29) is created on the new device. The genesis record includes:
```json
{
  "seq": 1,
  "ts": "2026-05-20T16:00:00Z",
  "kind": "genesis.recovery_restart",
  "principal_did": "did:example:alice-calm-123",
  "principal_legal_identity_unchanged": true,
  "new_master_key_fingerprint": "...",
  "predecessor_chain_id": "old_chain_id",
  "predecessor_chain_head": "sigsum_anchor_of_old_head",
  "recovery_scenario": "s3",
  "recovery_reason": "Passphrase lost; new enrollment required.",
  "witness_re_attestations": [
    { "notary": "..." },
    { "family": "..." }
  ],
  "record_hash": "..."
}
```

**Step 6: Publish new chain head; mark old chain as succeeded.**

The new chain's genesis block is published to Sigsum (Everest 30). The predecessor reference in the genesis block points back to the last known-good head of the old chain, creating an immutable historical record.

**Step 7: Notify counterparties of recovery.**

A `kind: "recovery.restart_alert"` notification is sent to known counterparties (Everest 78), disclosing:
- The old chain head (for historical reference).
- The new chain genesis block.
- Witness re-attestations (demonstrating continuity of human identity).
- A notice that the new chain is cryptographically independent from the old (new master key) but witness-continuous (same witnesses attest both).

Counterparties may downgrade trust levels during a transition period (e.g., 7 days) before fully accepting proofs over the new chain. Counterparties with high trust in the witness network may accept the new chain immediately.

---

## §6. Identity continuity claim

### In S1/S2 (replica recovery)

- **Cryptographic continuity:** Full. The master key has not changed. All proofs over the old chain remain valid. The recovered chain is a direct continuation of the old chain, anchored in Sigsum.
- **Witness continuity:** Unchanged. Original witnesses remain the attestants of record.
- **Counterparty trust:** No downgrade. Counterparties accept all proofs signed by the same master key.

### In S3/S4 (new enrollment)

- **Cryptographic continuity:** None. The old master key is replaced. Proofs signed by the old key are no longer bindable to the principal's current key.
- **Witness continuity:** Strong. The same witnesses attest both the original enrollment and the recovery re-attestation, affirming that this is the same human in both cases.
- **Proof validity:** Proofs over the *old* chain remain valid in Sigsum (the old chain is immutable). But going forward, all *new* proofs must be signed by the new master key. Counterparties can follow the predecessor reference to see the historical chain and judge trust accordingly.
- **Counterparty trust model:** Counterparties decide locally whether to accept the new chain. A reasonable policy:
  - **High trust in witnesses:** Accept the new chain immediately after verifying witness re-attestations.
  - **Medium trust:** Accept new proofs after a transition window (e.g., 7 days).
  - **Low trust:** Downgrade to requiring additional friction (e.g., a fresh biometric disclosure, or a live call with the principal).

---

## §7. Threat model and defenses

### Threat: Attacker fakes loss to force new enrollment and impersonate principal

**Attack vector:** An adversary with the principal's name and enrollment date claims the principal lost all devices and demands a new enrollment ceremony, hoping to create a new chain under their control.

**Defense:** The witness re-attestation protocol (Everest 20). The original witnesses know the principal's face, voice, and behavior. They attest that the person appearing for recovery is the same principal. An attacker cannot pass this check without physically impersonating the principal or coercing/impersonating the witnesses themselves.

### Threat: Adversary obtains an encrypted replica and tries to decrypt it

**Attack vector:** An adversary steals the USB replica or accesses cloud credentials and attempts to decrypt the vault.

**Defense:** The encrypted replica is protected by the master key passphrase, which lives only in the principal's head (not on any device). Without the passphrase, decryption is computationally infeasible (age is an audited, modern cipher). If the passphrase is weak, an offline brute-force attack is possible, but this is a principal-side weakness (Everest 16 covers passphrase guidance and hardware-token alternatives).

### Threat: Attacker forces principal and witnesses to sign false recovery attestations

**Attack vector:** An adversary uses coercion (kidnapping, threats) to force the principal and witnesses to sign a false re-attestation, creating a fake recovery chain.

**Defense:** This is a *rubber-hose* attack and is out-of-scope for v0. No cryptographic protocol defends against a coerced principal or witnesses. Everest 21 (coercion resilience) addresses long-term mitigations (e.g., deadman switches, decoy identities). For v0, the assumption is that the principal and their trusted witnesses are not simultaneously coerced in a way that allows undetected impersonation.

---

## §8. Testing and auditing

### Tabletop exercise

Every 6 months, the principal and operator perform a simulated S1 recovery:

1. The principal reports (via out-of-band) that a device has been lost.
2. The operator marks the old VC as revoked.
3. The operator retrieves the USB replica and decrypts it (principal provides passphrase over a side channel).
4. The operator verifies the chain against Sigsum and restores it on a test device.
5. The operator appends a recovery record and publishes to Sigsum.
6. The operator notifies a test counterparty with a recovery alert.
7. The test counterparty verifies the alert and confirms the new chain head.

**Acceptance:** Recovery from S1 to operational new chain in under 10 minutes.

### Documented runbook

A plaintext runbook is stored in `~/.calm-vault/runbooks/recovery_s1_s2.txt`, updated yearly, containing:

- Principal's secure contact channels (phone numbers, emails, emergency contacts).
- USB replica location(s) (e.g., "safe-deposit box at Bank X, San Francisco").
- Cloud storage credentials (encrypted).
- Witness contact information and re-attestation protocols.
- Operator recovery commands (exact CLI invocations).

---

## §9. Operator effort and automation

### Most common recovery (S1/S2)

```bash
calm-witness recover --scenario s1 --replica /mnt/usb/replicas/v0/latest.user_state.jsonl.age
```

The command:
1. Prompts for the master key passphrase.
2. Decrypts the replica.
3. Verifies the chain against Sigsum.
4. Restores the vault to `~/.calm-vault/`.
5. Appends a recovery record.
6. Publishes to Sigsum.

**Automated:** Fully; no manual intervention required after passphrase entry.

### Catastrophic recovery (S3/S4)

```bash
calm-witness recover --scenario s3 --no-old-key --new-enrollment --witnesses-confirmed
```

The command:
1. Initiates a new enrollment ceremony (Everests 11, 14).
2. Collects witness re-attestations (prompts for witness contact and confirmation).
3. Creates a new genesis block with predecessor reference.
4. Issues a recovery alert.

**Manual steps:** Witness coordination and re-attestation ceremonies require synchronous interaction (phone, video, or in-person).

---

## §10. Cross-references

- **Everest 11:** Enrollment ceremony spec (baseline biometric capture, identity verification).
- **Everest 14:** Baseline establishment (affect, vocabulary, behavioral norms).
- **Everest 16:** Key custody and passphrase protection.
- **Everest 20:** Enrollment witness protocol (notary and family attestations).
- **Everest 21:** Coercion resilience (out-of-scope for recovery, but related threat model).
- **Everest 22:** CredexAI credential issuance (VC revocation, reissuance).
- **Everest 29:** Genesis block and chain initialization.
- **Everest 30:** Sigsum publication and transparency-log anchoring.
- **Everest 32:** Encrypted replication (USB and cloud backup).
- **Everest 33:** Corruption recovery (local chain repair, different from enrollment loss).
- **Everest 78:** Stealth disclosure notifications (recovery.completed_alert, recovery.restart_alert).

---

— Calm, 2026-05-20
