# Everest 68 — Operator Identity Binding

*Phase VI — Disclosure Semantics. Prereq: Everest 22.*

## Executive summary

When a Calm operator generates a disclosure proof, it must bind the proof cryptographically to the operator's verified identity. The operator holds a **CalmOperatorCredential** — a W3C Verifiable Credential v2 issued by CredexAI that attests the operator's legal entity, software version, binary hash, and primary jurisdiction. At disclosure time, the operator signs the canonical serialization of the response with its Ed25519 private key bound to the VC, then includes the VC reference (or inline VC) so the counterparty can verify: (1) the signature against the operator's public key embedded in the VC, and (2) the VC itself against CredexAI's issuer key. If the VC is revoked or expired, the proof is rejected.

---

## 1. Why operator identity binding matters

A Calm operator is software. It might be:

- A service running on John Bradley's laptop.
- A containerized agent in Creativity Machine LLC's infrastructure.
- A third-party AI operator licensed to use Calm Witness on behalf of a principal.

From a counterparty's perspective, receiving a disclosure proof without knowing *which operator software* produced it introduces two problems:

1. **Attribution collapse.** If multiple principals use different operators, a counterparty cannot distinguish which operator was honest or compromised. Binding the proof to the operator's VC enables revocation per-operator (if Operator A is compromised, CredexAI revokes its VC; proofs from Operator B remain valid).

2. **Supply-chain evidence gap.** The disclosure proof attests that a biometric was evaluated over a committed vault state. But who evaluated it? A malicious operator could lie about the evaluation. The operator VC — signed by CredexAI — anchors the software version and binary hash, enabling auditors to determine if the operator was running a known-good build or a compromised one.

The operator identity binding is the structural link between "a proof was generated" and "the operator that generated it can be audited."

---

## 2. The CalmOperatorCredential

Before any disclosure can occur, the operator must obtain a VC from CredexAI. The operator initiates this at setup time (e.g., during deployment or container startup).

### 2.1 Operator registration with CredexAI

The operator submits a registration request to CredexAI:

```json
{
  "operator_type": "calm_witness_operator",
  "operator_name": "Calm Witness Op Instance #1",
  "legal_entity": "Creativity Machine LLC",
  "entity_jurisdiction": "US-DE",
  "operator_software_version": "calm-witness-0.1.0",
  "operator_software_hash": "sha256_of_binary_hex_64_chars",
  "operator_public_key": "ed25519_pub_32bytes_hex",
  "key_binding_method": "Ed25519Signature2020",
  "attestation_method": "sigstore_signature",
  "attestation_payload": "base64_encoded_sigstore_bundle"
}
```

Key fields:

- **operator_name:** Human-readable label for audit logs. Example: "Calm Witness Op deployed to us-west-2 on 2026-05-20."
- **legal_entity:** The entity responsible for operating the software. Can be an individual (as a legal entity under law) or a corporation. CredexAI verifies this against public records or a prior identity attestation.
- **entity_jurisdiction:** Primary jurisdiction (US-CA, US-DE, EU-IE, etc.). Used for compliance (Everest 79) and revocation authority.
- **operator_software_version:** Semantic version string. Example: "calm-witness-0.1.0".
- **operator_software_hash:** SHA-256 of the binary (executable, container image, or reproducible-build artifact). CredexAI will store this hash in the VC.
- **operator_public_key:** 32-byte Ed25519 public key, hex-encoded. The operator will use the corresponding private key to sign responses.
- **attestation_method:** How CredexAI should verify that the binary hash is correct. Options in v0: "sigstore_signature" (the operator's binary was signed by a Sigstore key infrastructure). v1 will add reproducible-build attestations.
- **attestation_payload:** The signed artifact (Sigstore bundle, or equivalent proof that the binary was built from known-good source).

### 2.2 CredexAI validation

CredexAI performs five checks before issuing the CalmOperatorCredential:

**Check 1: Legal Entity Verification**
- Verify that the `legal_entity` and `entity_jurisdiction` are valid under public records (Secretary of State, Companies House, equivalent).
- Verify that the entity is not sanctioned or known to operate maliciously.

**Check 2: Public Key Integrity**
- Confirm the Ed25519 public key is valid (32 bytes, no encoding errors).
- Confirm the key has not been previously issued under a different entity (collision detection).

**Check 3: Software Hash Validation**
- If `attestation_method` is "sigstore_signature," CredexAI verifies the Sigstore bundle:
  - The bundle is valid and not expired.
  - The bundle's hash matches `operator_software_hash`.
  - The Sigstore signing key is in CredexAI's trusted root (or an OIDC issuer CredexAI trusts).
- v0 does not require reproducible-build validation, but the hash is stored for future audit.

**Check 4: Version Consistency**
- Verify that `operator_software_version` is parseable semantic versioning.
- CredexAI logs this version to detect unexpected version jumps (e.g., 0.1.0 → 0.99.0 without intervening releases).

**Check 5: No Prior Revocation**
- Check that the operator (same legal entity + software version) has not been revoked before.
- If a prior VC for the same operator was revoked, require explicit re-authorization from the legal entity before issuing a new VC.

If all five checks pass, CredexAI issues the CalmOperatorCredential.

### 2.3 The CalmOperatorCredential structure

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2",
    "https://calm.vault.thecreativitymachine.ai/context/v1"
  ],
  "type": [
    "VerifiableCredential",
    "CalmOperatorCredential"
  ],
  "issuer": "did:example:credexai-issuer",
  "issuanceDate": "2026-05-20T10:00:00Z",
  "expirationDate": "2027-05-20T10:00:00Z",
  "credentialSubject": {
    "id": "did:example:calm-op-instance-1",
    "operatorName": "Calm Witness Op Instance #1",
    "legalEntity": "Creativity Machine LLC",
    "entityJurisdiction": "US-DE",
    "softwareVersion": "calm-witness-0.1.0",
    "softwareHash": "sha256_of_binary_hex",
    "publicKey": "ed25519_pub_32bytes_hex",
    "keyAlgorithm": "Ed25519",
    "keyBindingMethod": "Ed25519Signature2020"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:example:credexai-issuer#key-1",
    "signatureValue": "credexai_signature_hex"
  }
}
```

The VC is issued with a **12-month lifetime**. The operator must renew before expiration (similar to Everest 22, but operator renewal does not require re-enrollment).

---

## 3. Per-disclosure flow

Once the operator holds a valid CalmOperatorCredential, disclosure proceeds as follows:

### 3.1 Counterparty requests disclosure

The counterparty (C) sends a signed request to the operator (O):

```json
{
  "version": "1.0",
  "request_id": "req_uuid_20260520",
  "timestamp": "2026-05-20T15:00:00Z",
  "nonce": "random_hex_32bytes",
  "predicate_id": "in_baseline_24h",
  "freshness_window_hours": 24,
  "counterparty_vc_id": "vc_counterparty_uuid",
  "intended_use": "KYC compliance check",
  "signature": "counterparty_signed_request_hex"
}
```

The counterparty's signature proves that C authorized this request. The nonce is random and will be bound into the proof (Everest 70).

### 3.2 Operator evaluates the predicate and constructs the response

The operator:

1. Evaluates the predicate (`in_baseline_24h`) over the vault state.
2. Constructs a Pedersen commitment to the resulting bit.
3. Constructs a Σ-protocol proof that the commitment opens to the honest evaluation.
4. Obtains a fresh chain-head anchor from Sigsum and a Roughtime timestamp (Everests 30–31).
5. **Signs the canonical serialization of the response** with the operator's Ed25519 private key.

The response structure is:

```json
{
  "version": "1.0",
  "response_id": "resp_uuid_20260520",
  "request_id": "req_uuid_20260520",
  "nonce_echo": "random_hex_32bytes",
  "chain_head": "sha256_chain_head_hex",
  "chain_head_anchor_proof": {
    "sigsum_inclusion_proof": "...",
    "roughtime_attestations": [...]
  },
  "commitment": "g^h * h^r hex",
  "proof": {
    "type": "Sigma-Protocol-OR",
    "challenge": "...",
    "responses": [...]
  },
  "operator_vc_id": "vc_calm_op_instance_1",
  "operator_vc_inline": null,
  "timestamp": "2026-05-20T15:00:30Z"
}
```

### 3.3 Operator signs the response with its private key

The operator computes a canonical serialization (JSON, sorted keys, no whitespace):

```
canonical = json.dumps(
  {
    "chain_head": response["chain_head"],
    "chain_head_anchor_proof": response["chain_head_anchor_proof"],
    "commitment": response["commitment"],
    "nonce_echo": response["nonce_echo"],
    "operator_vc_id": response["operator_vc_id"],
    "proof": response["proof"],
    "request_id": response["request_id"],
    "response_id": response["response_id"],
    "timestamp": response["timestamp"],
    "version": response["version"]
  },
  sort_keys=True,
  separators=(',', ':')
)
```

The operator then signs:

```
signature_hex = operator_private_key.sign(canonical.encode('utf-8')).hex()
```

The signature is appended to the response:

```json
{
  ...response fields...,
  "operator_signature": "ed25519_signature_hex_128_chars"
}
```

### 3.4 Operator includes the VC reference or inline VC

The response includes either:

- **VC reference:** `"operator_vc_id": "vc_calm_op_instance_1"` (the counterparty already has the VC, or will fetch it from CredexAI).
- **Inline VC:** `"operator_vc_inline": {...full CalmOperatorCredential JSON...}` (the counterparty receives the VC without an extra round-trip).

For bandwidth-conscious scenarios, the operator uses the VC ID reference. For high-security scenarios (or if the counterparty is offline), the operator inlines the full VC.

---

## 4. Counterparty verification

The counterparty receives the response and verifies it in this order:

### 4.1 Obtain the operator's VC

If the response includes `operator_vc_inline`, use it directly. Otherwise, fetch the VC:

```bash
curl https://credexai.example.com/vc/vc_calm_op_instance_1 \
  -o operator_vc.json
```

### 4.2 Verify the VC's signature

The counterparty verifies CredexAI's signature over the VC:

```python
from cryptography.hazmat.primitives.asymmetric import ed25519

credexai_public_key = ed25519.Ed25519PublicKey.from_public_bytes(
  bytes.fromhex("credexai_pub_key_hex")
)

vc_copy = operator_vc.copy()
del vc_copy["proof"]
vc_canonical = json.dumps(vc_copy, sort_keys=True, separators=(',', ':'))
signature_bytes = bytes.fromhex(operator_vc["proof"]["signatureValue"])

credexai_public_key.verify(signature_bytes, vc_canonical.encode('utf-8'))
```

If the signature fails, reject the response: the operator's identity cannot be trusted.

### 4.3 Check VC validity

- **Expiration:** Verify `expirationDate > now()`. If expired, reject the response.
- **Revocation:** Query CredexAI's revocation endpoint:
  ```bash
  curl https://credexai.example.com/revocation/vc_calm_op_instance_1
  ```
  If the response is "revoked," reject. If "not revoked," continue.

### 4.4 Extract the operator's public key

From the VC:

```python
operator_public_key_hex = operator_vc["credentialSubject"]["publicKey"]
operator_public_key = ed25519.Ed25519PublicKey.from_public_bytes(
  bytes.fromhex(operator_public_key_hex)
)
```

### 4.5 Verify the response signature

Recompute the canonical serialization of the response (same order as step 3.3):

```python
response_canonical = json.dumps(
  {
    "chain_head": response["chain_head"],
    "chain_head_anchor_proof": response["chain_head_anchor_proof"],
    "commitment": response["commitment"],
    "nonce_echo": response["nonce_echo"],
    "operator_vc_id": response["operator_vc_id"],
    "proof": response["proof"],
    "request_id": response["request_id"],
    "response_id": response["response_id"],
    "timestamp": response["timestamp"],
    "version": response["version"]
  },
  sort_keys=True,
  separators=(',', ':')
)

signature_bytes = bytes.fromhex(response["operator_signature"])
operator_public_key.verify(signature_bytes, response_canonical.encode('utf-8'))
```

If the signature fails, reject the response: the operator did not sign it.

### 4.6 Verify the predicate proof

Once the operator identity is confirmed, verify the predicate proof (Everest 65) and check the chain-head anchor (Everests 30–31). These verifications confirm that the bit is honest and fresh.

---

## 5. Operator revocation

### 5.1 Principal-initiated revocation

If the principal discovers that an operator is compromised or malfunctioning, the principal can request that CredexAI revoke the operator's VC:

```json
{
  "vc_id": "vc_calm_op_instance_1",
  "revocation_reason": "Software vulnerability discovered; operator suspended from production",
  "principal_attestation": "Principal-signed attestation of operator compromise",
  "principal_signature": "..."
}
```

CredexAI verifies the principal's signature (using the principal's VC from Everest 22) and appends the revocation to its CRL.

### 5.2 CredexAI-initiated revocation

CredexAI may revoke an operator's VC if:

- The operator's binary hash does not match any known-good build (supply-chain compromise).
- The legal entity is sanctioned or known to operate maliciously.
- The operator's private key is leaked (last resort; revocation propagates to all principals using that operator).
- Law enforcement or court order requires it.

Revocation is **immediate and global**: all counterparties stop accepting proofs from the revoked operator.

---

## 6. Multi-operator scenarios

A single principal may operate multiple Calm instances (e.g., on laptop and phone):

- Each operator gets its own CalmOperatorCredential.
- The principal's VC (Everest 22) does not enumerate which operators it trusts; instead, each disclosure response carries the operator's own VC.
- A counterparty verifies each operator's VC independently.

Example: John Bradley runs Calm Witness on two devices. Device A's operator VC and Device B's operator VC are distinct. If Device A is compromised and revoked, Device B's operator continues to generate valid proofs.

---

## 7. Software-attestation extension (v1 feature)

In v0, the operator VC stores the binary hash but does not attest reproducibility. v1 will add:

- **Reproducible-build attestation:** The operator VC includes a Sigstore bundle proving that the binary can be built from a public source (GitHub tag, commit hash) and reproduces bit-for-bit.
- **Build metadata:** Compiler version, build flags, dependencies locked in a manifest.
- **Audit trail:** Links to CI/CD logs showing the build was triggered by a known deployment trigger, not random developer action.

This closes the loop on supply-chain security: a counterparty can verify not just that the operator is running software, but that the software was built from auditable source.

---

## 8. Cross-references

- **Everest 22 (Principal VC Issuance):** The principal's VC is orthogonal to the operator's VC. Both are issued by CredexAI; both are W3C VCs. A disclosure proof references both.
- **Everest 66 (Disclosure Request):** The counterparty's signed request initiates the flow.
- **Everest 67 (Disclosure Response):** The response structure embeds the operator's VC reference.
- **Everest 70 (Replay Defense):** The nonce in the request is bound into the response and verified via the operator's signature.
- **Everest 65 (Predicate Proof):** The operator signs the predicate proof; the operator VC binds the signature to an auditable software identity.
- **Calm Pact (Operator Identity):** If two operators (e.g., representing different principals) run Calm Pact, each carries an operator VC; the pact proof references both.

---

## 9. Implementation: calm-witness CLI

The operator manages its VC via CLI:

```bash
# Register operator with CredexAI (one-time setup)
calm-witness operator register \
  --legal-entity "Creativity Machine LLC" \
  --entity-jurisdiction "US-DE" \
  --software-version "calm-witness-0.1.0" \
  --credexai-endpoint https://credexai.example.com \
  --output ~/.calm-vault/operators/operator.vc.json

# Check VC validity
calm-witness operator check-vc

# Renew VC (before expiration)
calm-witness operator renew-vc

# Revoke VC (emergency only)
calm-witness operator revoke-vc \
  --reason "Private key compromised"

# Generate disclosure with operator signature
calm-witness disclosure generate \
  --request <request.json> \
  --include-operator-vc [inline|reference]
```

---

## 10. Acceptance test

This Everest is complete when:

1. The operator obtains a valid CalmOperatorCredential from CredexAI, signed by CredexAI's key.
2. The operator constructs a disclosure response and signs it canonically with the operator's Ed25519 private key.
3. The response includes either the VC's ID or the full inline VC.
4. A counterparty verifies the response signature using the operator's public key (from the VC).
5. A counterparty verifies the VC's signature using CredexAI's public key.
6. A counterparty checks the VC's expiration and revocation status.
7. If the VC is expired or revoked, the counterparty rejects the response.
8. If the VC is valid and the response signature verifies, the counterparty proceeds to verify the predicate proof.
9. If the operator revokes its VC (via principal or CredexAI request), new proofs are rejected and old cached proofs are flagged for re-verification.

---

— Calm, 2026-05-20
