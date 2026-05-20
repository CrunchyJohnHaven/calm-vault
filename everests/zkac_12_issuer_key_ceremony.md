# Everest 12 — Issuer Key Ceremony Spec

*Phase XVIII — Issuer Infrastructure. Prereq: Everest 11.*

An issuer's keypair is the trust root of every credential they sign. If key generation is compromised, every downstream credential is forged. This summit specifies the one-time, physical, witnessed, multi-party ceremony that produces the issuer's signing and attestation keypairs. The ceremony is the **trust origin** of the issuer; everything downstream — issuance, revocation, rotation — rides on the unfalsifiability of keys produced here.

## §0. One-line spec

> A reproducible, scriptable, air-gapped, multi-party, witness-signed session in which ≥2 issuer principals jointly generate and seal a signing keypair using mixed entropy sources and hardware attestation, terminating with encrypted key storage in a Hardware Security Module and a witness-signed ceremony record published to Sigsum transparency log.

## §1. Operating principles (non-negotiable)

1. **Air-gap.** No network-connected device in the room except the HSM/YubiKey and attestation logger (if separate), both in air-gap mode. Verified physically and logged.
2. **Multi-party entropy mixing.** No single party controls entropy. ≥2 issuer principals + 1 entropy witness independently contribute entropy sources; no mixing without ≥2 principals present.
3. **Hardware attestation.** The generation device (HSM or Secure Enclave) produces a signed attestation of the entropy consumed, the key generated, and the sealing operation. Attestation is archived.
4. **No plaintext export.** The keypair never leaves the HSM/YubiKey unencrypted. All key material is sealed to the hardware before any principal departs.
5. **Witness independence.** ≥2 attesting witnesses with no operational stake in the issuer; each signs the ceremony record independently with their own hardware token.
6. **Principal authority.** Each issuer principal participating in the ceremony must state aloud their consent to generate this key and bind it to the issuer's public identity. No proxy.
7. **Reproducible.** A reasonably-trained third party with this document and the ceremony rig can execute the ceremony without further instruction.
8. **Transparency log publication.** The ceremony record is appended to a public Sigsum log within 24h; the tree hash is published to the issuer's public directory.

## §2. Roster

| Role | Required | Notes |
|---|---|---|
| **Issuer Principal (≥2)** | yes | Each participates in entropy mixing + witness consensus. Ideally ≥2 geographically separated principals. |
| **Entropy Witness** | yes | A trusted third party who contributes independent entropy (hardware RNG or physical dice source). No commercial relationship to issuer. |
| **Attesting Witness (≥2)** | yes | Independent observers, ideally with ≥5 years familiarity with issuer; each signs ceremony record with hardware token. |
| **Notary** | optional | Licensed notary attests to physical ceremony location, date, and principal identities per government ID. |
| **Ceremony Operator (Calm Witness-like automation)** | yes | Air-gapped host running `calm-issuer keygen --ceremony` CLI; does not control entropy; logs all operations. |
| **HSM/YubiKey Custodian** | yes | The individual responsible for HSM physical security during and after ceremony. May be one of the issuer principals or a designated officer. |
| **Bystanders** | NONE | If a bystander enters the room, the ceremony aborts and reschedules in a different location. |

## §3. Required equipment

- **HSM (production) or YubiKey (pilot):** FIPS 140-2 Level 3+ HSM (ThalesHSM, Gemalto, YubiHSM 2) or YubiKey 5 Series for pilot deployments. Firmware version locked to reviewed build before ceremony. Must support ECDSA (P-256) and EdDSA.
- **Entropy sources (≥2):**
  1. OS entropy pool (`/dev/urandom` or equivalent) from air-gapped host, seeded with fresh entropy from the machine's HW RNG.
  2. Independent hardware RNG (e.g., ChaosKey, TrueRNG) or physical dice (20d20 or higher) operated by entropy witness.
  3. Optional tertiary: time-bound entropy (ceremony-start nanoseconds + entropy witness's hardware token nonce).
- **Generation host:** Air-gapped laptop running `calm-issuer keygen` CLI. Filesystem encrypted. No WiFi, cellular, Bluetooth. USB-only connectivity for HSM.
- **Attestation device:** A second air-gapped laptop (or the same host after keygen completes) running the attestation logger. Connects to HSM read-only to verify attestation proofs.
- **Witness signing tokens:** Each attesting witness brings a YubiKey or equivalent hardware token with their existing CredexAI VC + signing key. Required for post-ceremony signature.
- **Sigsum logger:** HSM or witness operator has write-access to the Sigsum API endpoint (whitelisted IP, no TLS cert validation at generation time; validated retroactively). Air-gapped via dedicated leased line or manual batching.
- **Power:** Wall power for both hosts; ceremony exceeds 90 minutes. UPS backup for HSM if ceremony spans any power grid uncertainty.
- **Paper + pens:** For ceremony log (handwritten backup). Shredded at end-of-session.

## §4. Disallowed items

- Smartphones — left in separate, locked room.
- Smart watches — left outside ceremony space.
- Networked laptops other than attestation logger (and only after keygen is sealed).
- Cameras of any kind; physical opaque tape on any device-built-in camera.
- Recording devices (audio or video) other than the ceremony operator's logger.
- External USB drives or cloud-sync folders.
- Smart-home microphones; power-cut at breaker if present.
- Pre-printed key material or "backup" keys; key generation is the only source.

## §5. Pre-ceremony preparation (≤7d before)

1. **Issuer governance:** Issuer's board (or equivalent) formally authorizes this ceremony and names the participating principals.
2. **Witness confirmation:** All principals + entropy witness + ≥2 attesting witnesses confirm attendance, review this spec, and obtain their hardware tokens.
3. **Location:** Secure physical room with locked door, no shared HVAC, no windows facing public spaces. Recorded address and GPS coordinates in ceremony manifest.
4. **HSM initialization:** Fresh HSM is unboxed, firmware hash verified against published checksum, and initialized to blank state. PIN known only to HSM custodian; backup PIN held in sealed envelope by one attesting witness (to be opened only in key-loss recovery per Everest 89).
5. **Host bring-up:** `calm-issuer keygen --dry-run` on generation host; verify all entropy sources produce bits, HSM responds to test commands, and airplane mode is locked. Attestation logger also dry-runs.
6. **Network audit:** Air-gap is verified with a spectrum analyzer or RF sniffer; no WiFi or cellular baseline detected in the room.
7. **Ceremony rehearsal:** Principal 1 and operator rehearse the script (§6) without consuming entropy or touching HSM; timing is confirmed at ≤90 min.

## §6. Ceremony script (~90 minutes total)

### A — Room sweep and network audit (~10 min)

Ceremony operator walks the room calling out every electronic device. Entropy witness checks each against a printed list. Any networked device is powered off at the wall or removed. Ceremony operator runs a spectrum analyzer or RF sniffer to confirm no cellular / WiFi baseline. Result is logged.

### B — Principal affirmation (~5 min)

Each issuer principal (≥2) states aloud:
- Full legal name and issuer title.
- Their relationship to the issuer organization.
- That they are present voluntarily and authorize this key ceremony.
- That they understand the key will be sealed in the HSM and is non-exportable.

Operator logs each affirmation verbatim.

### C — Witness affirmation (~5 min)

Each attesting witness (≥2) states aloud:
- Full legal name.
- Years of familiarity with the issuer or its principals.
- That they are present voluntarily.
- That they have read and understand this spec.

Operator logs each affirmation verbatim.

### D — Entropy witness statement (~3 min)

Entropy witness states aloud:
- Full legal name.
- Source(s) of entropy they will contribute (HW RNG model, dice, etc.).
- That the entropy source is not connected to any network and has been in their sole custody since procurement.

Operator logs statement.

### E — HSM custody and initial state (~5 min)

HSM custodian:
1. Removes HSM from secure envelope, displays serial number and firmware version hash aloud.
2. Powered on; responds to `status` command.
3. PIN-authenticated (custodian enters PIN off-camera).
4. `keygen` command is pre-staged but not executed.

Each witness visually confirms HSM state matches the expected factory image.

### F — Entropy gathering (~15 min)

Operator invokes: `calm-issuer keygen --entropy-phase`.

**Sub-step F.1 — OS entropy seeding (~5 min):**
- Operator loads generation host's `/dev/urandom` into the entropy pool via the HSM's RNG-mixing interface.
- HSM attestation object logs: `entropy_source_1: os_pool, bits_consumed: N, timestamp: T, attestation_signature: SIG1`.

**Sub-step F.2 — Independent hardware entropy (~5 min):**
- Entropy witness produces entropy using their contributed source (HW RNG produces bits; operator reads them aloud; attestation logger records count and bitstream SHA-256 hash).
- OR entropy witness rolls dice (20d20) N times; operator reads each result aloud and records; operator computes entropy from die rolls.
- HSM attestation logs: `entropy_source_2: hw_rng | dice, bits_consumed: M, witness: [name], timestamp: T, attestation_signature: SIG2`.

**Sub-step F.3 — Entropy mixing (~5 min):**
- Operator invokes `calm-issuer keygen --entropy-mix --sources 2 --thresholds 2`.
- HSM mixes the two entropy streams using a cryptographic combiner (XOR + HMAC-SHA-256 to avoid either source dominating).
- HSM attestation logs the mix operation: `entropy_mixed: [hash of combined stream], bits_final: K, threshold: 2_of_2, timestamp: T, attestation_signature: SIG3`.

Each principal and witness confirms aloud that the entropy-mix hash matches the display on the generation host.

### G — Keypair generation (~10 min)

Operator invokes: `calm-issuer keygen --generate --alg=ecdsa-p256 --name=[issuer_id]`.

HSM performs:
1. Draw K bits from the mixed entropy pool.
2. Generate ECDSA private key `sk_issuer`.
3. Derive public key `pk_issuer`.
4. Optionally derive secondary EdDSA key for attestation signing (`sk_attest`, `pk_attest`).
5. Compute attestation object: `keygen_proof = Attest(alg, pk_issuer, pk_attest, mixed_entropy_hash, timestamp, nonce)`.
6. Sign attestation with HSM's internal key: `attestation_signature = HMAC(hsm_internal_key, keygen_proof)`.

Operator displays to all parties:
- Public key (`pk_issuer`) in hex and QR code format.
- Attestation hash (SHA-256 of `keygen_proof`).
- Timestamp of generation.

Each principal and witness records these values on their copy of the ceremony checklist.

### H — Key sealing (~5 min)

Operator invokes: `calm-issuer keygen --seal --hsm-pin=[PIN] --wrapping-key=[issuer_master_secret]`.

HSM performs:
1. Encrypt `sk_issuer` under a key-wrapping-key (KWK) derived from the issuer's master secret (Everest 13). KWK is stored only in HSM persistent memory.
2. Seal `sk_issuer` with a HMAC-based commit: `sealed_key_commit = HMAC(hsm_key, sk_issuer)`.
3. Write to HSM persistent storage a key object: `{ key_id, pk_issuer, sealed_key_commit, generation_timestamp, ceremony_id }`.
4. Wipe all plaintext `sk_issuer` from HSM volatile memory.
5. Return a seal confirmation signed by the HSM's attestation key: `seal_proof = HMAC(hsm_attest_key, sealed_key_commit || timestamp)`.

Operator displays seal confirmation hash to all parties. Each principal and witness acknowledges.

### I — Attestation record finalization (~5 min)

Attestation logger (running on second host or after keygen completes) assembles the ceremony record:

```json
{
  "ceremony_id": "issuer_[name]_keygen_[timestamp]_[nonce]",
  "issuer_name": "...",
  "ceremony_type": "issuer_keypair_generation",
  "generation_timestamp": "2026-05-20T14:30:00Z",
  "hsm_model": "...",
  "hsm_firmware_version": "...",
  "hsm_firmware_hash": "...",
  "hsm_serial": "...",
  "location_address": "...",
  "location_gps": "[lat, lon]",
  "ceremony_duration_minutes": 87,
  "principals": [
    {
      "name": "...",
      "title": "...",
      "affirmation_timestamp": "...",
      "affirmation_hash": "..."
    }
  ],
  "entropy_witnesses": [
    {
      "name": "...",
      "entropy_source": "hw_rng | dice | ...",
      "bits_contributed": 512,
      "entropy_source_hash": "..."
    }
  ],
  "attesting_witnesses": [
    {
      "name": "...",
      "credexai_vc_id": "...",
      "affirmation_timestamp": "...",
      "witness_signature": "..." 
    }
  ],
  "entropy_operations": [
    {
      "phase": "entropy_source_1",
      "bits_consumed": 512,
      "hsm_attestation": "..."
    },
    {
      "phase": "entropy_source_2",
      "bits_consumed": 512,
      "entropy_witness": "...",
      "source_hash": "..."
    },
    {
      "phase": "entropy_mix",
      "bits_final": 512,
      "threshold": "2_of_2",
      "mixed_entropy_hash": "..."
    }
  ],
  "keygen_proof": {
    "algorithm": "ecdsa-p256",
    "public_key": "pk_issuer_hex",
    "public_key_qr": "...",
    "attestation_hash": "...",
    "hsm_attestation_signature": "...",
    "generation_timestamp": "2026-05-20T14:30:42Z"
  },
  "sealing_proof": {
    "sealed_key_commit": "...",
    "seal_proof_hash": "...",
    "timestamp": "2026-05-20T14:30:47Z"
  },
  "notary_seal": {
    "notary_name": "...",
    "notary_license": "...",
    "notary_signature": "..."
  }
}
```

Operator computes `ceremony_record_hash = SHA-256(canonical_json)` and displays to all parties.

### J — Witness signatures (~10 min)

Each attesting witness (≥2) independently:
1. Reviews the ceremony record on screen.
2. Inserts their YubiKey / hardware token.
3. Signs the `ceremony_record_hash` with their existing CredexAI signing key.
4. Records the signature in the ceremony record under `witness_signature_[n]`.
5. Operator appends a `kind: "witness_signature"` record to the ceremony log.

All parties confirm that ≥2 witness signatures are present and valid before proceeding.

### K — Transparency log publication (~5 min)

Operator (or designated witness with Sigsum credentials) invokes:

```
calm-issuer keygen --publish-sigsum \
  --log-endpoint [sigsum_api_endpoint] \
  --ceremony-record [ceremony_record_hash]
```

Sigsum appends the ceremony record to its append-only log. Operator displays the Sigsum tree-hash and leaf index to all parties. Each principal and witness records these values as proof of publication.

If network access is unavailable (air-gap strictness), the ceremony record is staged in a sealed envelope to be published within 24h by a designated witness with network access. The delayed-publication timestamp and witness attestation are recorded in the record.

### L — HSM secure storage and key backup (~10 min)

1. HSM custodian verifies the sealed key is stored in HSM persistent memory with a test operation: `calm-issuer keygen --test-seal --key-id=[key_id]`. The test operation invokes the key for a dummy signature and confirms it works; HSM never exports the key.
2. One attesting witness takes custody of the sealed backup PIN envelope (generated during pre-ceremony phase). This envelope is to be opened only per Everest 89 (recovery procedure) with ≥N principal signatures (N ≥ 2).
3. A second copy of the ceremony record (paper form, handwritten) is signed by both principals and all witnesses, placed in a sealed envelope, and stored in a secure archive.
4. HSM is powered down and returned to secure storage (HSM custodian's vault or bank safe).

### M — Close-out (~5 min)

- Operator shreds the handwritten ceremony log paper.
- Attestation logger is powered down.
- Principals, entropy witness, and all attesting witnesses state aloud that the ceremony is complete and they have no outstanding concerns.
- Operator confirms all artifacts are accounted for: ceremony record (digital), Sigsum proof, paper backup (sealed), HSM (secured).

## §7. Artifacts produced

- One canonical ceremony record (JSON) with all principals' affirmations, entropy logs, keygen proofs, sealing proofs, and ≥2 witness signatures.
- HSM-sealed issuer keypair (`sk_issuer`, `pk_issuer`) stored only in HSM persistent memory, never exported unencrypted.
- Sigsum transparency log entry: `ceremony_record_hash` appended with tree-hash and leaf-index proof.
- Paper backup of ceremony record (handwritten summary), signed by all principals and witnesses, stored in sealed envelope in secure archive.
- Sealed backup PIN envelope held by one attesting witness (to be opened only for key recovery per Everest 89).
- Ceremony attestation proof from HSM (signed by HSM's internal attestation key).

## §8. Abort conditions (any one triggers full restart at a later date)

- Bystander entry into ceremony room.
- Network device detected mid-ceremony (spectrum analyzer alert).
- HSM hardware malfunction (fails self-test, responds with error).
- Entropy witness's source produces unexpected bitstream or fails entropy quality test.
- Any principal expresses hesitation or declines to affirm.
- Entropy mixing fails validation (operator rejects mix due to threshold not met).
- Keygen produces invalid public key or attestation proof fails verification.
- Sealing operation fails or seal confirmation is rejected.
- Any attesting witness is unable or unwilling to sign the ceremony record.
- Sigsum publication fails (grace period: 24h to publish with witness attestation of delay reason).
- HSM loses power during key generation (before seal completes).

On abort: the ceremony record is not finalized; the HSM is reset to blank state (under multi-principal control); all parties are notified; new ceremony is scheduled with fresh entropy and amended risk mitigations.

## §9. Threat coverage (forward references to dedicated Everests)

| Attack | Where it lives |
|---|---|
| Single-principal entropy control | Multi-principal entropy mixing (§F) + ≥2 issuer principals present. Everest 13 for KWK custody model. |
| Compromised entropy source | Two independent entropy sources (OS + HW RNG or dice) + entropy witness attestation. Everest 9 (Failure Modes Z22, Z24). |
| Replay of ceremony | Sigsum transparency log anchors ceremony_record_hash; tamper-evident. Everest 19 (Audit Log). |
| HSM firmware compromise | Pre-ceremony firmware verification (hash check) + attestation object signed by internal HSM key. Everest 13 (HSM Attestation Requirements). |
| Key export after ceremony | HSM does not support export operation; only key-wrapping and signing. Everest 13 (Key Custody Options). |
| Principal coercion (forced to generate unwanted key) | Voluntary affirmation (§B) + witness attestation at ceremony time. Everest 19 (Slashing for issuer misbehavior). |
| Witness collusion (colluding witnesses sign false ceremony record) | ≥2 independent witnesses + Sigsum transparency log publish. Everest 23 (Issuer Reputation: ceremony record is public). |
| Lost key (HSM destroyed) | Everest 89 (Recovery via N-of-M threshold keying of backup PIN). |
| Stale key after rotation | Everest 14 (Key Rotation Protocol) anchors old key to chain; verifiers accept pre-rotation credentials. |
| Stolen HSM | Physical security and multi-principal PIN required to access key. Backup PIN sealed + witnessed. |

## §10. Open questions for v0 → v1

1. **Notary mandate.** v0 says "optional"; v1 should mandate notary for production-grade issuers in regulated jurisdictions (financial, legal, healthcare).
2. **Remote ceremony.** Strictly disallowed in v0. v2 may explore tele-presence with hardware-attested cameras + air-gapped local HSM, but trust model is degraded vs. in-person.
3. **HSM-less backup keygen.** For pilot deployments, can we support Secure Enclave-only (no external HSM)? Requires additional attestation support (Everest 13).
4. **Entropy escrow.** Should entropy sources be escrowed (bits signed by entropy witness and published to Sigsum) to prove they were independent? v0 default: no escrow (entropy bits are destroyed post-mix); v1 may mandate escrow for financial issuers.
5. **Ceremony record TTL.** How long should ceremony records be retained? v0 default: ≥7 years (aligned with financial audit), published to Sigsum indefinitely.
6. **Multi-HSM co-keying.** Can N principals each hold an HSM with a share of the issuer master secret (KWK)? Requires E89 threshold-key machinery; deferred to v1.
7. **Quantum-safe keygen.** v0 uses ECDSA-P256 + EdDSA; post-quantum migration (E94) requires new ceremony procedure for secondary post-quantum keys.

## §11. Acceptance test

This document is the acceptance artifact. A reasonably-trained operator with this document, the `calm-issuer keygen` CLI, an HSM + YubiKey stack, ≥2 issuer principals, and ≥2 independent attesting witnesses can execute the ceremony end-to-end. A successful run:

1. Produces a valid ceremony record (per §7) with ≥2 witness signatures.
2. Seals an issuer keypair in the HSM (test invocation succeeds: `calm-issuer keygen --test-seal`).
3. Publishes the ceremony record to a Sigsum transparency log (leaf index + tree-hash are retrievable).
4. Produces sealed backup PIN envelope (testable via Everest 89 recovery, but not executed in v0 acceptance run).

The issuer can then proceed to Everest 13 (Key Custody) to select final custody model (HSM-only, HSM + KMS, or multi-sig threshold).

— Calm, 2026-05-20
