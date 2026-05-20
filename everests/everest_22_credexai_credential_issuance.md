# Everest 22 — CredexAI Credential Issuance

*Phase II — Capture & Enrollment. Prereq: Everest 16 (Template Encryption), Everest 20 (Enrollment Witness Protocol).*

## Executive summary

Upon completion of enrollment (Everest 11), template encryption (Everest 16), and witness attestation (Everest 20), the Calm operator submits a credential issuance request to CredexAI. CredexAI validates the enrollment package and issues a **CalmWitnessPrincipalCredential**, a W3C Verifiable Credential (VC) v2 that cryptographically binds:

- The principal's legal identity (from CredexAI's identity attestation)
- The principal's master public key (Ed25519)
- Pedersen commitments to the enrolled biometric templates
- The enrollment ceremony's attestation hash
- All witness signatures and attestations
- Issuance timestamp (anchored via Roughtime)
- The Calm operator's identity

The VC is the enrollment's canonical proof: counterparties can verify the principal's identity and biometric commitment offline using CredexAI's public keys. The principal stores the VC at `~/.calm-vault/credentials/principal.vc.json`. All subsequent biometric proofs (disclosure, re-enrollment, key rotation) reference this VC.

**Acceptance (verbatim):** a successful enrollment produces a CredexAI-issued VC binding the templates' commitments to the principal's legal identity.

---

## 1. Why Verifiable Credentials, not raw signatures

The enrollment ceremony produces witness signatures and key material. A counterparty might accept a raw signature from the principal's master key, but that leaves three problems:

1. **Counterparty must know the master public key.** Raw signatures do not encode identity. The counterparty needs to trust that `master.pub` truly belongs to the principal claiming it. CredexAI's identity attestation solves this.

2. **Revocation is not built-in.** If the principal's enrollment was coerced (discovered later), there is no standardized way for the principal to revoke the raw signatures. VCs have revocation infrastructure (CRL, OCSP-style checks).

3. **Interoperability is weak.** Raw signatures are proprietary to the principal's key type (Ed25519) and ceremony format. VCs are a W3C standard; counterparties using any standard VC-compatible verifier can check them without custom code.

A VC solves all three: it packages the principal's identity, master public key, commitments, witness attestations, and revocation information in a standard format. The Calm operator never reveals the principal's templates or master private key; the VC commits only to the templates via Pedersen commitments.

---

## 2. Issuance ceremony

The issuance ceremony is the bridge between the local enrollment chain (Everest 11, 20) and CredexAI's identity layer. It runs **after** witness signatures are collected and **before** genesis attestation (Everest 29).

### 2.1 Preconditions

| Gate | Source | Failure mode |
|------|--------|--------------|
| Templates encrypted under master public key | Everest 16 | FM-51: commitments cannot be verified |
| Witness attestations signed on Pedersen commitment | Everest 20 | Issuance rejected at step 3.3 |
| Principal identity proof current | Everest 11 | Issuance rejected at step 3.1 |
| Operator CalmOperatorCredential valid | Calm Pact | Issuance rejected at step 3.5 |
| Refusal floor scan clean | §9 below | Hard refuse; no VC issued |

### 2.2 Ceremony steps (operator-facing)

1. **Package assembly.** The operator constructs the issuance request (§3) from the enrollment chain head, witness JSONL, and Pedersen commitments computed at enrollment time.
2. **Local preflight.** `calm-witness credential preflight` validates JSON schema, commitment count matches modality map, and no protected-category fields appear in claims (§9).
3. **Submit to CredexAI.** The operator calls the CredexAI Issuer API via the `koushik-credexai-inspect` SDK (§8). API keys and pickup tokens remain server-side configuration; they are never written to the vault chain or VC payload.
4. **CredexAI validation.** Five checks (§4) run at the issuer. On success, CredexAI signs the VC and returns a pickup token or direct credential payload.
5. **Retrieval and storage.** The operator retrieves the VC and writes `~/.calm-vault/credentials/principal.vc.json`.
6. **Chain anchor.** A `kind: "credential.issued"` record and, when Everest 29 is active, a `kind: "genesis_attestation"` record with `credexai_vc_hash = sha256(canonicalised(VC))` are appended to `user_state.jsonl`.
7. **Witness confirmation.** Optional: witnesses receive a commitment-only receipt (Pedersen hash of VC, not the VC itself) for their records.

The ceremony is idempotent: duplicate submissions with the same `ceremony_record_root_hash` are rejected by CredexAI collision detection.

---

## 3. The enrollment package: what the operator submits to CredexAI

When the enrollment ceremony concludes (Everest 11) and witness signatures are collected (Everest 20), the operator prepares a structured issuance request:

```json
{
  "credential_type": "CalmWitnessPrincipalCredential",
  "version": "1.0",
  "subject": {
    "principal_legal_name": "Alice Chen",
    "principal_legal_id_proof": "<CredexAI identity proof from E11>",
    "principal_did": "did:example:alice-calm-123",
    "principal_jurisdiction": "US-CA"
  },
  "master_key": {
    "algorithm": "Ed25519",
    "public_key_hex": "ed25519_pub_32bytes_hex",
    "fingerprint": "sha256(public_key)[:16]"
  },
  "template_commitments": [
    {
      "modality": "handwriting:calm",
      "commitment_hex": "g^template_id_hash * h^randomness_hex",
      "commitment_method": "Pedersen-Ristretto255",
      "randomness_blinded": true
    },
    {
      "modality": "voice_transcription:focused",
      "commitment_hex": "g^template_id_hash * h^randomness_hex",
      "commitment_method": "Pedersen-Ristretto255",
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
    }
  ],
  "operator_identity": {
    "calm_operator_name": "Calm Witness Operator Instance #1",
    "operator_credexai_vc_id": "vc_operator_uuid",
    "operator_jurisdiction": "US-CA"
  },
  "protocol": "calm-witness/v0"
}
```

The operator never reveals:

- The plaintext templates themselves
- The principal's master private key
- The randomness values `r` in the Pedersen commitments
- The principal's biometric scores or distance thresholds
- Any protected-category attribute (§9)

---

## 4. CredexAI validation flow

When CredexAI receives the issuance request, it performs five validation steps before issuing the VC:

### 4.1 Principal identity proof

CredexAI verifies the `principal_legal_id_proof`. The proof must match `principal_legal_name`, not be revoked or expired, and be issued by a trusted identity provider. If identity verification fails, the request is rejected.

### 4.2 Master public key integrity

CredexAI confirms the public key is valid Ed25519, has not been previously issued under a different principal's identity, and the fingerprint matches the operator's claim.

### 4.3 Witness signature verification

For each witness attestation, CredexAI verifies tier-appropriate signatures (notary commission, family VC, institutional VC). Any failure rejects the request.

### 4.4 Ceremony record root hash

CredexAI checks the `ceremony_record_root_hash` is valid SHA-256, unique, and signed by the operator credential. This ensures the ceremony record existed when the operator computed the hash.

### 4.5 Operator credential validation

CredexAI verifies the operator's CalmOperatorCredential is current, not revoked, and signed the issuance request.

### 4.6 Refusal floor gate (issuer-side)

CredexAI rejects any issuance request whose claims map, directly or by proxy, to the thirteen protected categories in Everest 113. This is a hard gate, not a warning.

---

## 5. VC issuance: credential structure and binding fields

If all validations pass, CredexAI constructs the CalmWitnessPrincipalCredential in W3C VC v2 format:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://credexai.org/contexts/calm-witness/v0"
  ],
  "type": [
    "VerifiableCredential",
    "CalmWitnessPrincipalCredential"
  ],
  "issuer": "did:credexai:v1:<issuer-key-thumbprint>",
  "issuanceDate": "2026-05-20T14:40:00Z",
  "expirationDate": "2028-05-20T14:40:00Z",
  "credentialSubject": {
    "id": "did:calm:<principal-stable-id>",
    "name": "Alice Chen",
    "principal_jurisdiction": "US-CA",
    "calmWitness": {
      "masterPubKey": "ed25519_pub_32bytes_hex",
      "masterPubKeyFingerprint": "sha256(key)[:16]",
      "templateCommitments": [
        {
          "modality": "handwriting:calm",
          "commitment": "g^h1 * h^r1",
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
        }
      ],
      "operatorIdentity": {
        "operatorName": "Calm Witness Operator Instance #1",
        "operatorVCId": "vc_operator_uuid",
        "operatorJurisdiction": "US-CA"
      },
      "protocol": "calm-witness/v0"
    }
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:credexai:v1:<issuer-key>",
    "proofPurpose": "assertionMethod",
    "proofValue": "<base64 Ed25519 sig over canonicalised credential>"
  }
}
```

### 5.1 What each binding field attests

| Field | Binds to | Why |
|-------|----------|-----|
| `credentialSubject.name` | Principal legal identity | Establishes legal accountability for issued disclosures |
| `principal_jurisdiction` | Applicable law | Gates cross-jurisdiction predicate eligibility (Everest 79) |
| `masterPubKey` | Enrollment master key | Counterparties verify proofs under this key |
| `templateCommitments` | AEAD-wrapped templates in vault | Operator cannot substitute templates after enrollment |
| `enrollmentCeremony.ceremonyRecordRootHash` | Enrollment chain entry | Proves the ceremony happened |
| `witnessAttestations` | Human witness signatures | Substitution resistance (FM-10, Everest 21) |
| `operatorIdentity` | Calm operator instance | Different operator cannot impersonate without re-enrollment |

Pedersen commitments bind template content without revealing templates or randomness. Legal identity binding comes from CredexAI's issuer signature over the subject block, not from self-asserted name alone.

### 5.2 What the VC explicitly does not contain

- Plaintext biometric templates or feature vectors
- Master private key or template encryption keys
- Pedersen randomness `r`
- Biometric scores, thresholds, or distance metrics
- Self-report mood content
- Principal street address (only optional salted commitment in ceremony metadata, never in VC)
- **Any protected-category claim** (§9)

---

## 6. Storage and chain records

Once CredexAI issues the VC, the operator stores it locally:

```bash
mkdir -p ~/.calm-vault/credentials
calm-witness credential retrieve \
  --vc-id vc_uuid_alice \
  --output ~/.calm-vault/credentials/principal.vc.json
```

The VC is appended to `~/.calm-vault/user_state.jsonl` as `kind: "credential.issued"`:

```json
{
  "kind": "credential.issued",
  "credential_type": "CalmWitnessPrincipalCredential",
  "credential_id": "vc_uuid_alice",
  "issuer": "did:credexai:v1:<issuer>",
  "issuance_timestamp": "2026-05-20T14:40:00Z",
  "expiration_timestamp": "2028-05-20T14:40:00Z",
  "master_pub_fingerprint": "sha256_key[:16]",
  "witness_count": 2,
  "credexai_vc_hash": "sha256_canonical_vc_hex"
}
```

Everest 29 genesis attestation uses the same `credexai_vc_hash` to bridge structural chain integrity and legal identity.

---

## 7. Verification

Counterparties verify in three layers:

1. **Structural validation.** Required VC fields present; type includes `CalmWitnessPrincipalCredential`.
2. **Signature verification.** CredexAI issuer key validates `proof.proofValue` over canonicalised credential (offline-capable with published issuer key).
3. **Revocation and expiry.** Online check against CredexAI status list (§8.3).

Calm Witness additionally computes `operator_id_hash = sha256(canonicalised(VC))` for disclosure response binding (Everest 68).

---

## 8. CredexAI SDK integration (`koushik-credexai-inspect`)

Implementation uses the vendored CredexAI Python SDK at:

`~/CredexAI/koushik-credexai-inspect/credexai/sdks/python/credexai/`

No secrets appear in client bundles, vault chain records, or this specification. Issuer API keys load from environment or operator-controlled secret stores only.

### 8.1 Issue path (operator)

```python
import os
from credexai.client import CredexaiIssuerClient
from credexai.types import IssuerClientConfig

env_cfg = {
    "base_url": os.environ["CREDEXAI_ISSUER_BASE_URL"],
    "api_key": os.environ["CREDEXAI_ISSUER_API_KEY"],
}
config = IssuerClientConfig(**env_cfg)
client = CredexaiIssuerClient(config)

# Map CalmWitnessPrincipalCredential package to issuer permissions envelope
issue_response = await client.issue_credential(
    agent_name=package["subject"]["principal_legal_name"],
    agent_public_key=package["master_key"]["public_key_hex"],
    permissions={
        "calmWitnessEnrollment": {
            "ceremonyRecordRootHash": package["enrollment_ceremony"]["ceremony_record_root_hash"],
            "templateCommitments": package["template_commitments"],
            "witnessAttestations": package["witness_attestations"],
            "protocol": "calm-witness/v0",
        }
    },
    expires_in_days=730,
)
pickup_token = issue_response["pickupToken"]
vc = await client.pickup_credential(pickup_token)
```

### 8.2 Verify path (counterparty)

```python
from credexai.verifier import verify_credential, VerificationResult

result: VerificationResult = await verify_credential(
    authorization_header=f"CredexaiVC {vc_jwt}",
    issuer_public_key=published_issuer_ed25519_key,
)
assert result.success
```

The SDK's `verify_credential` performs Ed25519 JWT verification suitable for embedded/local use. Full DID resolution and status-list checking use the gateway in production deployments.

### 8.3 Revocation path

```python
await client.revoke_credential(jti=vc["jti"])
```

Revocation propagates to CredexAI's status list. Calm Witness blocks proof generation when status is `revoked`.

---

## 9. Refusal floor: no protected categories in VC claims

Everest 22 inherits the Compass refusal floor (Everest 113) for **all VC claims**, not only predicates. A CalmWitnessPrincipalCredential must never encode, directly or by behavioral proxy, any of the thirteen protected categories:

1. Race / ethnicity
2. Religion / faith
3. Sexual orientation
4. Gender identity
5. Political affiliation
6. Immigration status / national origin
7. Criminal record
8. Donations to specific causes (ideological fingerprinting)
9. Opinions on contentious issues
10. Disability status
11. Health status
12. Age
13. Marital / family status

### 9.1 Allowed vs forbidden in VC claims

| Allowed | Forbidden |
|---------|-----------|
| Legal name (identity accountability) | Race, ethnicity, or national origin |
| Jurisdiction code (`US-CA`) | Religion or faith affiliation |
| Pedersen template commitments | Sexual orientation or gender identity |
| Witness role metadata (notary, family) | Political party or voting history |
| Ceremony timestamp and location city | Immigration status |
| Operator DID | Criminal arrests or convictions |
| Protocol version string | Health or disability status |
| Master public key fingerprint | Age or date of birth |
| | Marital status or family structure |

### 9.2 Enforcement

- **Preflight scanner:** `calm-witness credential preflight` rejects packages containing forbidden claim keys or known proxy patterns before network submit.
- **Issuer gate:** CredexAI rejects non-conforming packages (§4.6).
- **Audit:** Everest 115 triage treats protected-category VC claims as automatic trademark violation.

The refusal floor is load-bearing: identity binding serves consent accountability, not demographic profiling. If a counterparty needs a protected-category attribute, Calm Witness does not provide it; the request fails closed.

---

## 10. Revocation

The principal may request revocation when enrollment was coerced, templates or master key were compromised, or the principal withdraws from Calm Witness.

**Revocation flow:**

1. Principal or operator submits revocation to CredexAI with VC id, reason, and principal signature bound to the VC master key or identity key.
2. CredexAI verifies signature and appends to status list.
3. Operator appends `kind: "credential.revoked"` to `user_state.jsonl`.
4. `calm-witness proof generate` returns error when credential is revoked.

Counterparties querying revocation status reject proofs that depend on a revoked VC.

**Key rotation** issues a new VC referencing the prior id; the old VC is not retroactively revoked unless compromised (§11 in prior drafts).

**Renewal** before `expirationDate` extends lifetime without re-enrollment when master key and commitments are unchanged.

---

## 11. Threat model (selected)

| Threat | Mitigation |
|--------|------------|
| Forged VC | CredexAI signature verification fails |
| Template substitution post-enrollment | Commitments in VC must match vault; FM-51 |
| Protected-category smuggling in claims | Refusal floor preflight + issuer gate |
| Coerced enrollment discovered later | Revocation + Everest 23 recovery |
| CredexAI issuer compromise | Out of Calm scope; operator monitors issuer key rotation announcements |

---

## 12. Cross-references

- **Everest 11:** Enrollment ceremony produces the issuance package.
- **Everest 16:** Template encryption and key rotation prerequisites.
- **Everest 20:** Witness protocol signatures included in VC.
- **Everest 23:** Recovery after total enrollment loss.
- **Everest 29:** Genesis attestation bridges VC hash to chain.
- **Everest 68:** Operator identity binding uses VC hash in disclosures.
- **Everest 113:** Refusal floor taxonomy inherited by VC claims.

---

## 13. Implementation: calm-witness CLI

```bash
calm-witness credential preflight --package issuance.json
calm-witness credential issue \
  --package issuance.json \
  --credexai-endpoint "$CREDEXAI_ISSUER_BASE_URL"
calm-witness credential retrieve --vc-id vc_uuid_alice \
  --output ~/.calm-vault/credentials/principal.vc.json
calm-witness credential verify \
  --vc-file ~/.calm-vault/credentials/principal.vc.json
calm-witness credential revoke --vc-id vc_uuid_alice --reason "compromise"
```

---

## 14. Acceptance test

This Everest is complete when:

1. Enrollment ceremony (Everest 11) completes with witness attestations (Everest 20).
2. Operator constructs issuance request per §3 with Pedersen commitments and identity proof.
3. Refusal floor preflight passes; no protected-category fields present.
4. CredexAI validates all checks (§4) and issues CalmWitnessPrincipalCredential (§5).
5. VC stored at `~/.calm-vault/credentials/principal.vc.json`.
6. `kind: "credential.issued"` appended to `user_state.jsonl`.
7. Offline verifier confirms CredexAI signature via `koushik-credexai-inspect` SDK pattern without network secrets.
8. Online verifier confirms non-revoked status.
9. Principal references VC in subsequent proofs (Everest 68); counterparties verify identity and template commitments.

Gate: `~/CredexAI/scripts/everest_22_zkbb_credexai_credential_gate.py` (exit 0 = green).

---

— Calm, 2026-05-20
