# Everest 13 — Issuer Key Custody

*Phase XVIII — Issuer Infrastructure. Prereq: Everest 12.*

After an issuer's signing keypair is generated in a witnessed ceremony (E12), it must be stored, accessed, and guarded for the issuer's operational lifetime. This summit specifies three custody models — Hardware Security Module (HSM), Cloud-managed KMS, and Multi-signature threshold — with explicit trust trade-offs per issuer class.

## §0. One-line spec

> Post-ceremony, the issuer's sealed keypair is held in custody according to the issuer's class: state issuers → HSM with witnessed key-wrapping; professional → multi-sig threshold; peer-collective → cloud-KMS acceptable; self-attested → Secure Enclave acceptable. Rotation discipline, backup, recovery compose with E89 (secret-sharing) and E14 (rotation). T-Z13.1..5 acceptance.

## §1. Custody models (overview)

At E12's conclusion, the issuer holds a keypair `(sk_issuer, pk_issuer)` sealed in an HSM or equivalent hardware token. Post-ceremony, the issuer must:

1. **Store** the sealed key durably (off-site backup, redundancy).
2. **Access** the key for issuance operations (sign credentials, revoke).
3. **Guard** against theft, compromise, or loss.
4. **Rotate** the key on schedule or emergency (E14).
5. **Recover** from key loss using threshold shares (E89).

Three models handle these requirements with different trust assumptions and operational complexity:

- **HSM Custody**: Single hardware security module holds the seal. Issuer or trusted custodian controls access via PIN.
- **Cloud-KMS Custody**: Cloud provider (AWS KMS, GCP KMS, Azure Key Vault) holds the seal and key material. Issuer delegates trust to provider.
- **Multi-sig Threshold Custody**: N issuer principals (or trusted co-signers) each hold a share of the key-wrapping key. M-of-N signatures required to unseal and use the issuer key.

## §2. Threat model composition

Key custody defends against:

| Threat | Custody Model | Defense |
|---|---|---|
| **Stolen HSM** | HSM | Physical security + multi-principal PIN. Backup PIN sealed + witnessed (E89). |
| **Insider theft** (issuer staff) | Cloud-KMS | Provider's audit log. Regulatory compliance (HIPAA, PCI-DSS). IAM + MFA required. |
| **Regional compromise** (cloud provider breached) | Cloud-KMS | Jurisdictional backup (e.g., US + EU co-signing). Dual-provider threshold. |
| **Single-principal coercion** | Multi-sig | Threshold requirement forces attacker to coerce M-of-N parties. |
| **Key material export** | HSM, Cloud-KMS | No export operation. Keys never leave custody unencrypted. |
| **Operational loss** | All models | Threshold-shared backup key (E89). Recovery ceremony with N-of-M witnesses. |

## §3. Custody models detailed

### 3a. Hardware Security Module (HSM)

**What it is:** A standalone hardware device (e.g., YubiHSM 2, AWS CloudHSM, Thales Luna) that generates, stores, and uses keys under physical and cryptographic protection.

**Trust assumptions:**
- Issuer trusts the HSM manufacturer (YubiHSM → Yubico; CloudHSM → AWS infrastructure).
- Issuer physically controls the device or entrusts it to a single custodian.
- Issuer's PIN is never shared except in sealed backup (E89).

**Pros:**
- **Tamper-resistant.** FIPS 140-2 Level 3 certification. Detecting physical tampering triggers key destruction.
- **No network trust.** The HSM is air-gapped or connected only to the issuer's isolated network.
- **Portable.** Can be moved to secure storage (bank safe, vault) between issuance sessions.
- **High assurance.** Manufacturer attestation + customer audit are standard.

**Cons:**
- **Physical custody risk.** Loss or theft requires recovery ceremony (E89); interim issuer is degraded.
- **Vendor trust.** Yubico firmware or AWS CloudHSM service team has implicit trust.
- **Operational overhead.** Accessing the key requires physical presence or secure remote access.
- **Single point of failure.** If HSM is destroyed and backup PIN is also lost, the issuer's key is unrecoverable.

**Recommended for:** State issuers, financial issuers, regulated healthcare. Highest assurance model.

**Setup:**
1. Fresh HSM unboxed at ceremony (E12 §5).
2. Key sealed to HSM persistent memory (E12 §H).
3. Backup PIN envelope held by ≥1 witness (E12 §L).
4. HSM stored in issuer's vault or bank safe.
5. Rotation and access use local PIN authentication (E14).

**Key-wrapping flow:**
```
Issuer requests signature of credential C.
  ↓
HSM requires PIN entry (or secure API token).
  ↓
HSM unseals sk_issuer from persistent storage.
  ↓
HSM signs C using sk_issuer.
  ↓
HSM returns signature.
  ↓
sk_issuer is re-sealed before HSM returns.
```

---

### 3b. Cloud-managed KMS (AWS KMS, GCP KMS, Azure Key Vault)

**What it is:** A cloud provider's key management service that stores and operates keys in their secure infrastructure. Keys are never exported to the issuer's control.

**Trust assumptions:**
- Issuer trusts cloud provider's infrastructure (AWS, GCP, Azure).
- Issuer trusts provider's IAM and audit logging.
- Issuer accepts jurisdictional risk (data residency, subpoena compliance).

**Pros:**
- **Managed redundancy.** Cloud provider handles multi-region failover and backup.
- **Audit trail.** Every key operation is logged and queryable.
- **Regulatory compliance.** Providers meet HIPAA, PCI-DSS, SOC 2 Type II.
- **Operational ease.** No physical device to secure; access via API + IAM.
- **Scalability.** High-throughput issuance without HSM bottlenecks.

**Cons:**
- **Cloud provider trust.** If AWS KMS is compromised, all keys stored there are at risk.
- **Jurisdictional exposure.** Cloud provider's country can subpoena issuer keys (e.g., US government under ECPA).
- **Dependency on provider uptime.** If AWS KMS region is down, issuer cannot sign.
- **Cost.** AWS KMS charges per operation + per key per month.
- **Less tamper-evident.** Provider attestation is weaker than FIPS 140-2 hardware.

**Recommended for:** Peer-collective issuers, informal credential systems (educational, hobby), startups with limited budget. Medium assurance.

**Setup:**
1. Create IAM role for issuer signing operations (least privilege).
2. Enable CloudTrail / Cloud Audit Logs for key access.
3. Set key rotation policy in provider (E14).
4. Multi-region failover: replicate key to secondary region (AWS KMS replication).
5. Backup: secret-share the KMS key name + ARN via E89.

**Key-wrapping flow:**
```
Issuer requests signature of credential C.
  ↓
Issuer authenticates to AWS KMS via IAM role + MFA.
  ↓
KMS unseals sk_issuer in provider's HSM (internal).
  ↓
KMS signs C using sk_issuer.
  ↓
KMS returns signature; sk_issuer never leaves KMS.
  ↓
CloudTrail logs: [timestamp, issuer_role, operation, key_id, result].
```

---

### 3c. Multi-signature Threshold Custody

**What it is:** N issuer principals (or co-signers) each hold a share of the key-wrapping key (KWK). To unseal and use the issuer key, M-of-N shares must be combined cryptographically (threshold signature or MPC).

**Trust assumptions:**
- Issuer trusts the threshold scheme (BLS, FROST, or MPC per E87).
- No single principal can unilaterally compromise the issuer key.
- At least M principals are present and honest.

**Pros:**
- **No single point of compromise.** Attacker must coerce M-of-N principals.
- **Distributes custody.** Each principal physically holds their share (on device or in Secure Enclave).
- **Geographic independence.** Shares can be held in different jurisdictions; no single provider.
- **Rotation flexibility.** Changing one principal triggers a new threshold ceremony (E14), not a hardware swap.

**Cons:**
- **Operational complexity.** M-of-N ceremony is slower and requires coordination.
- **Share recovery hard.** If one principal loses their share, threshold may drop below M.
- **No hardware guarantee.** Shares are software-encrypted (unless held in Secure Enclaves); more operational risk than HSM.
- **Ceremony dependencies.** Every key operation (access, rotation, recovery) requires M principals to participate.

**Recommended for:** Professional issuers, cooperatives, mutual-guarantee organizations. Medium-high assurance (operationally demanding).

**Setup (M=2, N=3 example):**
1. At E12 ceremony, issuer principals agree on M=2, N=3.
2. Threshold signing scheme is instantiated (E87): BLS or FROST.
3. KWK is split into shares: `KWK_share_1`, `KWK_share_2`, `KWK_share_3`.
4. Principal A holds share 1 (Secure Enclave on device or hardware wallet).
5. Principal B holds share 2 (separate device).
6. Principal C holds share 3 (bank safe or third-party custodian).
7. To sign a credential, any 2 principals must cooperate.

**Key-wrapping flow:**
```
Issuer requests signature of credential C.
  ↓
Principal A provides KWK_share_1.
  ↓
Principal B provides KWK_share_2.
  ↓
Threshold verification: combine shares using BLS threshold scheme.
  ↓
Reconstructed KWK is derived.
  ↓
KWK decrypts the sealed sk_issuer (from local storage).
  ↓
sk_issuer signs C.
  ↓
Signature is returned; sk_issuer is re-sealed.
```

---

## §4. Issuer class recommendations

| Issuer Class | Recommended Model | Rationale |
|---|---|---|
| **State issuer** (government, regulators) | HSM + witnessed ceremony | Highest assurance. Government can require FIPS 140-2 and independent audit. |
| **Professional issuer** (medical, legal boards) | Multi-sig (M=2, N=3) or HSM | Multi-sig distributes custody; no single custodian can be coerced. |
| **Employer issuer** (corporate credentials) | Cloud-KMS + IAM or HSM | Cloud-KMS is cost-effective and auditable. Backup via E89. |
| **Peer-collective** (university consortium, guild) | Cloud-KMS or Multi-sig | Cloud-KMS is simple; Multi-sig if on-prem preferred. |
| **Self-attested issuer** (personal, hobby) | Secure Enclave + E89 | Device Secure Enclave (iPhone, Android) is sufficient. Backup via E89. |

## §5. Key rotation (E14 composition)

Each custody model composes with E14 (key rotation):

**HSM rotation:**
1. Generate new keypair in HSM (new ceremony, abbreviated).
2. Old key signs a certificate binding new key: `old_key_signs(new_pk, rotation_timestamp)`.
3. Certificate is published to issuer's public directory.
4. Verifiers accept credentials signed with old key during grace window (E34).
5. After grace period, issuer retires old key; HSM is re-certified.

**Cloud-KMS rotation:**
1. Provider rotates key material internally (automatic or manual).
2. Key version is incremented; old versions remain queryable.
3. Verifiers track key version in credential metadata.
4. Rotation is chain-anchored (issuer publishes rotation event to Sigsum, E19).

**Multi-sig rotation:**
1. Principals agree on new threshold parameters (M', N').
2. New threshold ceremony is scheduled.
3. Old shares are destroyed in witnesses' presence.
4. New shares are distributed (E87 refresh protocol).

---

## §6. Backup and recovery (E89 composition)

All three models support recovery via E89 (secret sharing):

**HSM backup:**
- Sealed backup PIN envelope is held by a witness.
- If HSM is destroyed, the issuer schedules a recovery ceremony.
- ≥2 principals + witness produce a new key with the recovered PIN.

**Cloud-KMS backup:**
- The KMS key ARN + provider credentials are secret-shared via E89.
- Each principal holds a Shamir share of the password/token.
- If KMS key is inaccessible, M-of-N principals reconstruct the key name and re-authenticate.

**Multi-sig backup:**
- Each principal's share is already backed up via E89.
- If principal A loses their device, principal A's share can be reconstructed via E89.
- This requires M-of-N co-principals to cooperate (same threshold as normal use).

---

## §7. Acceptance requirements (T-Z13.1..5)

**T-Z13.1: HSM model specification.**
- Document must specify FIPS 140-2 Level 3+ device, firmware version locking, and attestation requirements.
- Pass: YubiHSM 2, AWS CloudHSM, Thales Luna, Gemalto all acceptable.

**T-Z13.2: Cloud-KMS model specification.**
- Document must specify provider (AWS, GCP, Azure), IAM policy template, and audit-log retention.
- Pass: AWS KMS with CloudTrail, GCP Cloud KMS with Cloud Audit Logs, Azure Key Vault with Azure Monitor.

**T-Z13.3: Multi-sig threshold specification.**
- Document must cite E87 (threshold signatures), provide BLS or FROST scheme reference, and M-of-N parameter bounds.
- Pass: BLS (M ≥ 1, N ≥ 2), FROST (M ≥ 1, N ≥ 2), MPC (per E86).

**T-Z13.4: Threat trade-offs table.**
- Document must enumerate which threats each model mitigates and which remain residual.
- Pass: Completeness (no blank cells); each entry either cites a defense or marks as residual risk.

**T-Z13.5: Issuer-class mapping.**
- Document must prescribe custody model per issuer class (E7), with rationale.
- Pass: All five issuer classes (state, professional, employer, peer, self-attested) have assigned model + footnote.

---

## §8. Composition with E12, E14, E19, E34, E87, E89

| Everest | Dependency | Integration |
|---|---|---|
| **E12** (Ceremony) | Prereq | Custody model is chosen at E12 pre-ceremony; sealed key handed to chosen model. |
| **E14** (Rotation) | Follows | E14 specifies rotation protocol per custody model; uses E13 model as input. |
| **E19** (Audit log) | Follows | Custody model logs key access to Sigsum; issuer's transparency log (E19) includes custody transitions. |
| **E34** (Aging proofs) | Follows | When issuer rotates key (E14), verifiers use E34 grace window to accept old-key signatures. |
| **E87** (Threshold signatures) | Input | Multi-sig custody model uses E87 BLS or FROST scheme; E87 must ship before E13 multi-sig is operational. |
| **E89** (Secret sharing) | Follows | Backup PIN (HSM), KMS credential (Cloud), or share recovery (Multi-sig) all use E89 Shamir scheme. |

---

## §9. Open questions for v0 → v1

1. **Hardware escrow.** Should issuer HSMs be escrowed with a neutral third party (e.g., bank, notary) during periods of issuer dormancy? v0: no. v1: consider for high-stakes issuers.

2. **Dual-custody for High-stakes issuers.** Should state issuers be required to hold two independent HSMs in geographically separated vaults? v0: optional; v1: consider mandate for financial regulators.

3. **Cloud provider diversity.** Can issuer distribute the same key across two cloud providers (AWS + GCP) with threshold access? v1 research: adds complexity but improves resilience against provider-wide compromise.

4. **Secure Enclave full spec.** v0 allows Secure Enclave for self-attested issuers; v1 should standardize which enclaves (iPhone Secure Enclave, Android Strongbox) are approved + attestation requirements.

5. **MPC custody.** Can issuer principals remotely participate in key operations via MPC (E86) without physical presence? v0: no (air-gap required); v1: explore with bounded latency guarantees.

6. **Key escrow for law enforcement.** How does issuer respond to lawful key-escrow requests (e.g., government subpoena)? v0: deferred to organizational policy; v1: publish a framework (Law Enforcement Request Protocol, per E22).

---

## §10. Acceptance test

An issuer successfully implements E13 when:

1. **Model selection is documented.** Issuer's governance doc specifies which of the three models it uses + rationale per this summit.

2. **Custody operations are auditable.** Every key access is logged. For HSM: attestation logs. For Cloud-KMS: CloudTrail + provider audit. For Multi-sig: ceremony record + threshold verification log.

3. **Backup + recovery are exercised.** In a low-stakes test, the issuer demonstrates backup (E89 secret-sharing) and recovery (reconstructing key or credential access).

4. **Rotation is rehearsed.** Issuer completes a dry-run of E14 key rotation within the chosen custody model.

5. **Threat model is signed off.** Issuer's audit confirms that the chosen model's threat coverage (§4, §8) meets the issuer's operational risk tolerance.

The issuer can then proceed to E14 (Key Rotation), E15 (Revocation Registry), and E19 (Audit Log) simultaneously.

---

— Calm, 2026-05-20
