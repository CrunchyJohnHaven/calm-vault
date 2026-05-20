# Everest 22 — Enrollment → CredexAI Credential Issuance

*Phase II — Capture & Enrollment. Prereq: Everest 16, 20.*

## Executive summary

Upon completion of enrollment (Everest 11), template encryption (Everest 16), and witness attestation (Everest 20), the Calm operator submits a credential-issuance request to CredexAI. CredexAI validates the enrollment package and issues a **CalmWitnessPrincipalCredential**, a W3C Verifiable Credential (VC) v2 that cryptographically binds:

- The principal's legal identity (from CredexAI's identity attestation)
- The principal's master public key (Ed25519)
- Pedersen commitments to the enrolled biometric templates
- The enrollment ceremony's attestation hash
- All witness signatures and attestations
- Issuance timestamp (anchored via Roughtime)
- The Calm operator's identity

The VC is the enrollment's canonical proof: counterparties can verify the principal's identity + biometric commitment offline using CredexAI's public keys. The principal stores the VC at `~/.calm-vault/credentials/principal.vc.json`. All subsequent biometric proofs (disclosure, re-enrollment, key rotation) reference this VC.

---

## 1. Why Verifiable Credentials, not raw signatures

The enrollment ceremony produces witness signatures and key material. A counterparty might accept a raw signature from the principal's master key, but that leaves three problems:

1. **Counterparty must know the master public key.** Raw signatures do not encode identity. The counterparty needs to trust that `master.pub` truly belongs to the principal claiming it. CredexAI's identity attestation solves this.

2. **Revocation is not built-in.** If the principal's enrollment was coerced (discovered later), there's no standardized way for the principal to revoke the raw signatures. VCs have revocation infrastructure (CRL, OCSP-style checks).

3. **Interoperability is weak.** Raw signatures are proprietary to the principal's key type (Ed25519) and ceremony format. VCs are a W3C standard; counterparties using any standard VC-compatible verifier can check them without custom code.

A VC solves all three: it packages the principal's identity + master public key + commitments + witness attestations + revocation information in a standard format. The Calm operator never needs to reveal the principal's templates or master private key; the VC commits only to the templates (via Pedersen commitments).

---

## 2. The enrollment package: what the operator submits to CredexAI

When the enrollment ceremony concludes (Everest 11) and witness signatures are collected (Everest 20), the operator prepares a structured issuance request:

```json
{
  "credential_type": "CalmWitnessPrincipalCredential",
  "version": "1.0",
  "subject": {
    "principal_legal_name": "Alice Chen",
    "principal_legal_id_proof": "<CredexAI identity proof from E11>",
    "principal_did": "did:example:alice-calm-123"
  },
  "master_key": {
    "algorithm": "Ed25519",
    "public_key_hex": "ed25519_pub_32bytes_hex",
    "fingerprint": "sha256(public_key)[:16]"
  },
  "template_commitments": [
    {
      "modality": "handwriting",
      "commitment_hex": "g^template_id_hash * h^randomness_hex",
      "randomness_blinded": true
    },
    {
      "modality": "voice_transcription",
      "commitment_hex": "g^template_id_hash * h^randomness_hex",
      "randomness_blinded": true
    }
  ],
  "enrollment_ceremony": {
    "ceremony_id": "cer_uuid_20260520",
    "ceremony_timestamp": "2026-05-20T14:30:00Z",
    "ceremony_location": "Berkeley, CA",
    "ceremony_record_root_hash": "sha256(all_ceremony_records)"
  },
  "witness_attestations": [
    {
      "tier": 1,
      "witness_role": "notary",
      "witness_legal_name": "Maria Gonzalez",
      "witness_commission_id": "CA-12345678",
      "commitment_signature_hex": "notary_signed_pedersen_commitment",
      "attestation_timestamp": "2026-05-20T14:35:00Z"
    },
    {
      "tier": 2,
      "witness_role": "family",
      "witness_legal_name": "Bob Chen",
      "witness_credexai_vc_id": "vc_witness_bob_uuid",
      "relationship_to_principal": "spouse",
      "commitment_signature_hex": "witness_signed_pedersen_commitment",
      "attestation_timestamp": "2026-05-20T14:37:00Z"
    }
  ],
  "operator_identity": {
    "calm_operator_name": "Calm Witness Operator Instance #1",
    "operator_credexai_vc_id": "vc_operator_uuid",
    "operator_jurisdiction": "US-CA"
  },
  "cognitive_baseline_optional": {
    "declared_atypical": false
  }
}
```

The operator never reveals:
- The plaintext templates themselves
- The principal's master private key
- The randomness values `r` in the Pedersen commitments
- The principal's biometric scores or distance thresholds

---

## 3. CredexAI validation flow

When CredexAI receives the issuance request, it performs five validation steps before issuing the VC:

### 3.1 Principal Identity Proof

CredexAI verifies the `principal_legal_id_proof` — typically a photo ID scan or a prior CredexAI identity attestation issued during Everest 11. The proof must:
- Match the `principal_legal_name` in the request.
- Not be revoked or expired.
- Be issued by a trusted identity provider (government ID, CredexAI identity SDK, equivalent).

If identity verification fails, the request is rejected; no VC is issued.

### 3.2 Master Public Key Integrity

CredexAI confirms:
- The public key is valid Ed25519 (32 bytes, no encoding errors).
- The key has not been previously issued under a different principal's identity (collision detection).
- The fingerprint matches the operator's claim (trivial check: `SHA256(key)[:16]`).

### 3.3 Witness Signature Verification

For each witness attestation, CredexAI verifies:
- **Tier 1 (Notary):** The notary's signature is valid under the notary's public key. The notary's commission is current in the CA Secretary of State database (or equivalent jurisdiction). The `commitment_signature` was signed by the notary's commission key.
- **Tier 2 (Family / Designated):** The witness's CredexAI VC is current and not revoked. The witness's signature is valid under the witness's VC-binding key.
- **Tier 3 (Institutional):** The institutional witness's VC is current. The signature is valid under the organization's key.

If any signature fails verification, the request is rejected. An operator may resubmit with corrected signatures or additional witnesses.

### 3.4 Ceremony Record Root Hash

CredexAI does not receive the full ceremony record (templates, self-reports, etc.) — those remain encrypted in the principal's vault. Instead, CredexAI checks:
- The `ceremony_record_root_hash` is a valid SHA-256 hash (64 hex chars, no encoding errors).
- The hash is unique (not a reused ceremony from a prior issuance request).
- The operator signs the hash with their operator credential (Everest 68 — operator identity binding).

This ensures that the ceremony record existed and was complete when the operator computed the hash.

### 3.5 Operator Credential Validation

CredexAI verifies the operator's CredexAI VC:
- The VC is of type `CalmOperatorCredential` (or equivalent).
- The VC asserts that the operator is a valid Calm Witness instance licensed by Calm Pact.
- The VC is current and not revoked.
- The operator's signature on the issuance request is valid under the operator's VC-binding key.

This prevents a rogue operator (or malware) from issuing credentials on behalf of legitimate operators.

---

## 4. VC issuance: the credential structure

If all five validations pass, CredexAI constructs the CalmWitnessPrincipalCredential in W3C VC v2 format:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2",
    "https://calm.vault.thecreativitymachine.ai/context/v1"
  ],
  "type": [
    "VerifiableCredential",
    "CalmWitnessPrincipalCredential"
  ],
  "issuer": "did:example:credexai-issuer",
  "issuanceDate": "2026-05-20T14:40:00Z",
  "expirationDate": "2028-05-20T14:40:00Z",
  "credentialSubject": {
    "id": "did:example:alice-calm-123",
    "name": "Alice Chen",
    "calmWitness": {
      "masterPubKey": "ed25519_pub_32bytes_hex",
      "masterPubKeyFingerprint": "sha256(key)[:16]",
      "templateCommitments": [
        {
          "modality": "handwriting",
          "commitment": "g^h1 * h^r1",
          "commitmentMethod": "Pedersen-Ristretto255"
        },
        {
          "modality": "voice_transcription",
          "commitment": "g^h2 * h^r2",
          "commitmentMethod": "Pedersen-Ristretto255"
        }
      ],
      "enrollmentCeremony": {
        "ceremonyId": "cer_uuid_20260520",
        "ceremonyTimestamp": "2026-05-20T14:30:00Z",
        "ceremonyRecordRootHash": "sha256_ceremony_root",
        "location": "Berkeley, CA"
      },
      "witnessAttestations": [
        {
          "tier": 1,
          "witnessRole": "notary",
          "witnessName": "Maria Gonzalez",
          "witnessCommissionId": "CA-12345678",
          "attestationTimestamp": "2026-05-20T14:35:00Z",
          "signatureVerified": true
        },
        {
          "tier": 2,
          "witnessRole": "family",
          "witnessName": "Bob Chen",
          "witnessVCId": "vc_witness_bob_uuid",
          "relationship": "spouse",
          "attestationTimestamp": "2026-05-20T14:37:00Z",
          "signatureVerified": true
        }
      ],
      "operatorIdentity": {
        "operatorName": "Calm Witness Operator Instance #1",
        "operatorVCId": "vc_operator_uuid",
        "operatorJurisdiction": "US-CA"
      },
      "cognitivelyAtypicalBaseline": null
    }
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:example:credexai-issuer#key-1",
    "signatureValue": "credexai_signature_over_credential_hex"
  }
}
```

Key fields:

- **@context:** W3C standard context + Calm Witness extension context (published at calm.vault.thecreativitymachine.ai/context/v1).
- **type:** Standard VC type plus Calm-specific credential type.
- **issuer:** CredexAI's DID (decentralized identifier).
- **issuanceDate / expirationDate:** Roughtime-anchored (for tamper-evident timestamping). 24-month lifetime; renewal required before expiration.
- **credentialSubject.id:** Principal's DID (derived from legal identity).
- **credentialSubject.calmWitness:** All Calm Witness specific data:
  - **masterPubKey:** 32-byte Ed25519 public key (hex).
  - **templateCommitments:** Pedersen commitments to each template modality. Randomness is blinded (not revealed even to CredexAI).
  - **enrollmentCeremony:** Ceremony metadata (ID, timestamp, location, record root hash).
  - **witnessAttestations:** Array of all witness signatures and metadata. Each attestation is verified before inclusion.
  - **operatorIdentity:** The Calm operator instance that conducted the ceremony.
  - **cognitivelyAtypicalBaseline:** Optional; only populated if the principal declared cognitive atypicality in Everest 59.
- **proof:** CredexAI's Ed25519 signature over the entire credential (excluding the proof object itself).

---

## 5. Storage and availability

Once CredexAI issues the VC, the operator retrieves it and stores it locally:

```bash
mkdir -p ~/.calm-vault/credentials
curl https://credexai.example.com/vc/vc_uuid_alice \
  -H "Authorization: Bearer operator_token" \
  -o ~/.calm-vault/credentials/principal.vc.json
```

The principal can also retrieve the VC independently (with operator consent via a bearer token):

```bash
calm-witness credential retrieve \
  --credexai-token <token> \
  --output ~/.calm-vault/credentials/principal.vc.json
```

The VC is appended to `~/.calm-vault/user_state.jsonl` as a `kind: "credential.issued"` record:

```json
{
  "kind": "credential.issued",
  "credential_type": "CalmWitnessPrincipalCredential",
  "credential_id": "vc_uuid_alice",
  "issuer": "did:example:credexai-issuer",
  "issuance_timestamp": "2026-05-20T14:40:00Z",
  "expiration_timestamp": "2028-05-20T14:40:00Z",
  "master_pub_fingerprint": "sha256_key[:16]",
  "witness_count": 2
}
```

---

## 6. Verification: how counterparties trust the credential

A counterparty receiving the VC verifies it in three steps:

### 6.1 Structural Validation

The VC must:
- Be valid JSON or JSON-LD.
- Include all required fields (issuer, issuanceDate, credentialSubject, proof).
- Have type `["VerifiableCredential", "CalmWitnessPrincipalCredential"]`.

### 6.2 Signature Verification

The counterparty verifies CredexAI's proof:

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
import json

# Load CredexAI's public key (published, auditable)
credexai_public_key = ed25519.Ed25519PublicKey.from_public_bytes(
  bytes.fromhex("credexai_pub_key_hex")
)

# Remove proof object and canonicalize the credential
credential_copy = vc.copy()
del credential_copy["proof"]
credential_json = json.dumps(credential_copy, sort_keys=True)

# Verify signature
signature_bytes = bytes.fromhex(vc["proof"]["signatureValue"])
credexai_public_key.verify(signature_bytes, credential_json.encode())
```

If the signature verifies, the credential has not been tampered with and was issued by CredexAI.

### 6.3 Revocation Check

The counterparty queries CredexAI's revocation list (CRL or OCSP-style endpoint):

```bash
curl https://credexai.example.com/revocation/vc_uuid_alice
```

If the response is "not revoked," the credential is active. If "revoked," the credential is invalid for generating new proofs.

---

## 7. Key rotation and VC re-issuance

If the principal rotates their master key (Everest 16, Key Rotation), the new master public key must be bound to a new VC.

**Rotation workflow:**

1. Principal generates a new Ed25519 keypair and changes their passphrase (or YubiKey binding).
2. All templates are re-encrypted under the new public key.
3. The operator computes new Pedersen commitments to the (newly encrypted) templates and their new public key.
4. The operator submits an issuance request to CredexAI with:
   - The new master public key.
   - New Pedersen commitments.
   - A rotation attestation: "The prior VC (vc_uuid_alice_v1) was superseded on [date]. New VC binds the rotated key."
   - The prior VC's ID (for audit traceability).
5. CredexAI validates the rotation request and issues a new VC (vc_uuid_alice_v2).
6. The principal archives the old VC and begins using the new one.

The old VC is **not revoked** (it was valid at issuance time). The new VC explicitly references the rotation for audit. Counterparties checking the principal's identity can verify both VCs and determine which key is current (by issuance date).

---

## 8. Revocation: when and how

The principal can request revocation if:

- The enrollment was coerced (discovered later).
- The templates were compromised.
- The master private key was compromised.
- The principal withdraws from Calm Witness entirely.

**Revocation flow:**

1. The principal (or operator on their behalf) submits a revocation request to CredexAI:

```json
{
  "vc_id": "vc_uuid_alice",
  "revocation_reason": "Master private key compromised",
  "revocation_attestation": "Principal signed: [timestamp] [signature]"
}
```

2. CredexAI verifies the request:
   - The principal's signature is valid under a key bound to the VC (e.g., the master public key or an identity key).
   - The VC has not already been revoked.

3. CredexAI appends the revocation to its CRL:

```json
{
  "vc_id": "vc_uuid_alice",
  "revocation_timestamp": "2026-06-01T10:00:00Z",
  "revocation_reason": "Master private key compromised"
}
```

4. The operator appends a `kind: "credential.revoked"` record to `user_state.jsonl`.

5. Any subsequent attempt by the principal to generate a proof is blocked:

```bash
calm-witness proof generate --ceremony-id ... 
# Error: credential revoked on 2026-06-01; proof generation denied
```

**Counterparties also detect revocation:**

When a counterparty checks the VC's revocation status and receives a "revoked" response, they reject any proof that depends on the VC.

---

## 9. Renewal: before expiration

The VC expires 24 months after issuance (field `expirationDate`). The principal should renew the VC **at least 60 days before expiration** to avoid gaps.

**Renewal flow:**

1. The operator detects that `expirationDate` is within 60 days:

```bash
calm-witness credential check-expiry
# Output: VC expires in 45 days; renewal recommended
```

2. The operator submits a renewal request to CredexAI:

```json
{
  "prior_vc_id": "vc_uuid_alice",
  "renewal_reason": "24-month expiration approaching",
  "current_master_pub": "ed25519_pub_hex",
  "current_template_commitments": [...]
}
```

3. CredexAI validates:
   - The prior VC exists and is within 90 days of expiration.
   - The current master public key and template commitments are valid.
   - No intervening revocations or compromises are recorded.

4. CredexAI issues a new VC with a new issuance date and 24-month expiration.

5. The operator stores the new VC and archives the expired one.

**Important:** Renewal does **not** require re-enrollment. The principal does not need to repeat the biometric ceremony or gather new witness attestations. Renewal extends the credential's lifetime but does not update the witness records or ceremony details.

---

## 10. Composition with disclosure and proof generation

Once the VC is issued, all subsequent interactions with counterparties reference it:

- **Calm Witness Proof Generation (Everest 68):** The principal generates a biometric proof and includes a reference to the VC (or the entire VC, if the counterparty requests). The proof asserts: "My identity and master public key are bound to vc_uuid_alice (issued by CredexAI on [date])."

- **Counterparty Verification (Everest 70):** The counterparty verifies the proof by:
  1. Checking the VC's signature (CredexAI signed it).
  2. Checking the VC's expiration and revocation status.
  3. Verifying the proof's biometric signature under the master public key named in the VC.

- **VC Cross-Reference (Everest 79):** In multi-modal disclosures (handwriting + voice), the principal includes the same VC once, and both modal proofs reference it. This ensures the counterparty knows that the same person (same master key, same identity) produced both proofs.

---

## 11. Privacy: what the VC does and does not contain

**The VC contains:**
- Principal's legal name (necessary for identity).
- Principal's master public key (necessary for counterparties to verify proofs).
- Pedersen commitments to templates (privacy-preserving; does not leak template content).
- Witness attestations (public for auditability; witness names and role, not their full biometric data).
- Enrollment ceremony metadata (date, time, location; public for auditability).
- Operator identity (public; auditable).

**The VC does not contain:**
- Plaintext biometric templates.
- Master private key.
- Randomness used in Pedersen commitments.
- Template encryption keys.
- Biometric scores, thresholds, or distance metrics.
- Self-report content or mood-state declarations (these remain in the vault, encrypted).

**At rest:** The VC is stored unencrypted at `~/.calm-vault/credentials/principal.vc.json` (world-readable, it is a public credential). The principal can optionally encrypt it if they prefer.

**In transit:** The VC is transmitted over HTTPS (TLS) when the operator retrieves it from CredexAI or shares it with a counterparty.

---

## 12. Threat model and mitigations

| Threat | Impact | Mitigation |
|--------|--------|-----------|
| Adversary forges a VC | Claims to be the principal without proof | Counterparty verifies CredexAI's signature; forgery fails |
| CredexAI is subverted | Issues VCs to imposters | Catastrophic; defense is CredexAI's own audit, code review, and key custody. Calm does not mitigate CredexAI compromise. |
| Adversary obtains the VC | Learns principal's identity + master.pub | Not a problem; the VC is public. But adversary cannot generate proofs without master.priv. |
| Adversary revokes the VC | Principal cannot prove identity | Principal can request CredexAI un-revoke if revocation was fraudulent (requires proof of identity). Calm Witness Everest 23 defines recovery. |
| Witness signs under coercion | Witness attestation is invalid | Witness can later revoke their attestation (Everest 20, §7). Counterparties require non-revoked witnesses. |
| Enrollment was coerced | VC binds coerced principal | Principal revokes the VC immediately. Calm Witness Everest 23 (Recovery From Total Enrollment Loss) defines re-enrollment path. |

---

## 13. Cross-references and composition

- **Everest 11 (Enrollment Ceremony Spec):** The ceremony produces the enrollment package submitted in §2.
- **Everest 16 (Template Encryption & Key Custody):** Template encryption keys and master key rotation are prerequisites.
- **Everest 20 (Enrollment Witness Protocol):** Witness signatures are validated and included in the VC.
- **Everest 23 (Recovery From Total Enrollment Loss):** Describes re-enrollment and VC reissuance if the principal needs to recover after compromise.
- **Everest 59 (Baseline Assessment & Self-Report):** Baseline state is optional in the VC (cognitive atypicality flag).
- **Everest 68 (Biometric Proof Generation):** Proofs reference and depend on the VC.
- **Everest 70 (Verification & Proof Integrity):** Counterparty verification logic checks VC validity.
- **Everest 79 (Cross-Jurisdiction Legality):** Defines which jurisdictions accept VCs as evidence.
- **Calm Pact (Operator Identity Binding):** The operator's VC (CalmOperatorCredential) is validated as part of issuance.

---

## 14. Implementation: calm-witness CLI

The operator interacts with VC issuance via the CLI:

```bash
# Initiate issuance after witness signatures are collected
calm-witness credential issue \
  --principal-identity-proof <file> \
  --witness-attestations <jsonl_file> \
  --operator-vc-id <vc_uuid> \
  --credexai-endpoint https://credexai.example.com

# Retrieve issued VC
calm-witness credential retrieve \
  --vc-id vc_uuid_alice \
  --output ~/.calm-vault/credentials/principal.vc.json

# Check expiration
calm-witness credential check-expiry

# Initiate renewal
calm-witness credential renew \
  --prior-vc-id vc_uuid_alice

# Request revocation
calm-witness credential revoke \
  --vc-id vc_uuid_alice \
  --reason "Master private key compromised"

# Verify a VC locally (offline)
calm-witness credential verify \
  --vc-file ~/.calm-vault/credentials/principal.vc.json \
  --credexai-pubkey <file>
```

---

## 15. Acceptance test

This Everest is complete when:

1. The enrollment ceremony (Everest 11) completes with witness attestations (Everest 20) recorded.
2. The operator constructs the issuance request per §2, including principal identity proof, template commitments, ceremony metadata, and witness signatures.
3. CredexAI validates all five checks (§3) and issues a CalmWitnessPrincipalCredential VC (§4).
4. The operator retrieves the VC and stores it at `~/.calm-vault/credentials/principal.vc.json`.
5. A record of kind `"credential.issued"` is appended to `user_state.jsonl`.
6. An offline verifier (with CredexAI's public key) can verify the VC's signature without network access.
7. An online verifier can check the VC's revocation status by querying CredexAI.
8. The principal can reference the VC in subsequent proofs (Everest 68) and counterparties can verify the principal's identity and biometric commitments via the VC.

---

— Calm, 2026-05-20
