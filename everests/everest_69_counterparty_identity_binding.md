# Everest 69 — Counterparty Identity Binding

*Phase VI — Disclosure Semantics. Prereq: Everest 22.*

---

## Executive Summary

When a counterparty agent seeks disclosure of a principal's predicate truth values, the counterparty must present a CredexAI-issued **CalmWitnessCounterpartyCredential**, a W3C Verifiable Credential (VC) v2 that binds the counterparty's identity, operational class membership, and implementer pledge. The Calm operator validates this credential, verifies the counterparty's class claims, and binds the resulting disclosure to the counterparty's VC fingerprint. This ensures that the principal's audit log records exactly which counterparty identity made each request, and that only legitimately credentialed counterparties can obtain disclosures.

The CalmWitnessCounterpartyCredential encodes:

- **counterparty_id**: The counterparty's decentralized identifier (DID).
- **counterparty_class_claims**: A list of operational class slugs (e.g., `["peer_ai_collective"]` or `["medical", "research"]` for a healthcare research entity).
- **legal_entity**: Optional; the counterparty's registered legal entity, if applicable (e.g., "AlphaLabs Inc.").
- **jurisdiction**: The counterparty's primary operational jurisdiction.
- **service_implementer_pledge**: SHA-256 hash of the counterparty's signed implementer pledge (per Everest 98), proving the counterparty has committed to responsible data use and class-specific compliance obligations.

---

## 1. Why Counterparty Identity Binding

Calm Witness discloses a single bit—in baseline or not in baseline—to counterparties. But without binding that disclosure to the counterparty's verified identity, the principal loses auditability and the operator cannot apply consent policies or rate limits.

Three requirements drive counterparty identity binding:

1. **Auditability**: The principal must be able to review their audit log (Everest 72) and see exactly which named counterparty made each request. If ten medical researchers access the principal's baseline status, the principal's log must record ten distinct counterparty IDs with jurisdiction and class.

2. **Consent enforcement**: The principal grants (or denies) consent to *classes* of counterparties—e.g., "peer AI collectives may request my in_baseline_24h status, but financial services cannot." The operator must verify that the requesting counterparty's VC asserts membership in a class the principal has consented to.

3. **Rate limiting and sock-puppet defense**: Without verified counterparty identity, a single bad actor could spin up unlimited ephemeral counterparty keys and hammer the operator with requests, or masquerade as legitimate research teams. A CredexAI-issued VC rate-limits issuance (one organization cannot trivially mint many VCs) and binds each counterparty to external verification (e.g., medical license for the "medical" class).

---

## 2. The Counterparty Credential: Structure and Content

### 2.1 Credential Format

The CalmWitnessCounterpartyCredential is a W3C VC v2 document, issued by CredexAI:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://calm.vault.thecreativitymachine.ai/context/v1"
  ],
  "type": [
    "VerifiableCredential",
    "CalmWitnessCounterpartyCredential"
  ],
  "issuer": "did:example:credexai-issuer",
  "issuanceDate": "2026-05-20T10:00:00Z",
  "expirationDate": "2027-05-20T10:00:00Z",
  "credentialSubject": {
    "id": "did:example:counterparty-bob-ai-collective",
    "counterparty_class_claims": [
      "peer_ai_collective"
    ],
    "legal_entity": null,
    "jurisdiction": "US-CA",
    "service_implementer_pledge": "sha256_hash_of_bob_pledge_hex"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "verificationMethod": "did:example:credexai-issuer#key-1",
    "signatureValue": "credexai_signature_hex"
  }
}
```

**Key fields:**

- **@context**: W3C standard VC context plus Calm Witness extension context.
- **type**: Standard VC type plus `CalmWitnessCounterpartyCredential`.
- **issuer**: CredexAI's DID.
- **issuanceDate / expirationDate**: Roughtime-anchored. 12-month lifetime for counterparty credentials.
- **credentialSubject.id**: Counterparty's DID. Must be globally unique and bound to the counterparty's identity proof (e.g., incorporation documents, founder ID verification).
- **credentialSubject.counterparty_class_claims**: Array of class slugs from Everest 7 (e.g., `["peer_ai_collective"]`, `["medical", "research"]`, `["financial_services"]`). Each claim asserts the counterparty operates in that class.
- **credentialSubject.legal_entity**: Optional. If the counterparty is a registered legal entity (corporation, LLC, research institute), this field names it. If null, the counterparty is an individual or ad-hoc collective without formal legal status.
- **credentialSubject.jurisdiction**: ISO 3166-1 country code and optional subdivision (e.g., `"US-CA"`, `"DE"`, `"JP"`). Defines the primary jurisdiction for dispute resolution and regulatory compliance.
- **credentialSubject.service_implementer_pledge**: SHA-256 digest (hex) of the counterparty's signed implementer pledge. The pledge is a document (per Everest 98) in which the counterparty commits to data use restrictions, non-redistribution, and class-specific obligations (e.g., medical researchers commit to IRB oversight). The operator can retrieve the full pledge document separately and verify the hash.
- **proof**: CredexAI's Ed25519 signature over the credential.

### 2.2 Class Claims and Verification

When a counterparty requests disclosure, the Disclosure Request (Everest 66) includes a `counterparty_vc` field (inline or pointer) and a `counterparty_class_claim` field (the class the counterparty is claiming for this particular request).

The operator verifies:

1. **VC signature**: Does CredexAI's signature validate over the credential?
2. **VC not expired or revoked**: Is the credential's `expirationDate` in the future? Is it absent from CredexAI's revocation list?
3. **Class claim membership**: Does the claimed class (e.g., `"peer_ai_collective"`) appear in the credential's `counterparty_class_claims` array?

If any check fails, the request is rejected (HTTP 403 or HTTP 204 per Everest 77).

**Example:** A counterparty claims `"peer_ai_collective"` in the disclosure request. The operator loads the counterparty_vc and checks: is `"peer_ai_collective"` in the `counterparty_class_claims` array? If yes, proceed. If no, reject.

---

## 3. CredexAI Issuance and Class Verification

CredexAI issues counterparty credentials only after verifying the counterparty's identity and class claims. The verification rigor depends on the class:

### 3.1 Identity Verification (All Classes)

For any counterparty, CredexAI verifies the primary legal entity or individual identity:

- **Individual**: Government-issued photo ID, verified out-of-band (KYC process).
- **Legal entity**: Corporate registration (Secretary of State, equivalent), founder/officer identification.

Identity verification fails → no credential is issued.

### 3.2 Class-Specific Verification

**peer_ai_collective**: The counterparty must provide evidence of legitimate AI agent operation (e.g., code repository, published whitepaper, prior deployment evidence). Verification is heuristic; CredexAI maintains a registry of known-good collectives.

**medical**: The counterparty (or the institution they represent) must hold an active medical license, research ethics board (IRB) approval, or equivalent regulatory clearance. CredexAI queries state medical boards, FDA systems, or international equivalents.

**financial_services**: Banking, trading, or lending license from the applicable regulator (SEC, FDIC, etc.).

**research_institution**: University or research institute accreditation; peer review evidence.

**research**: IRB or equivalent ethics review active; publication track record.

**healthcare**: Hospital, clinic, or healthcare delivery organization license.

**regulatory_authority**: Government agency credentials (SEC, CDC, equivalent).

**anonymous**: No external class verification; see §5 below.

CredexAI's class claims are **not self-asserted**. The credential asserts the counterparty's verified status, not their claimed status. If a counterparty claims to be "medical" but has no medical license, CredexAI issues a credential with an empty `counterparty_class_claims` array or omits the "medical" claim entirely.

---

## 4. Request-Time Flow and Binding

### 4.1 Disclosure Request Signing

A counterparty C constructs a Disclosure Request per Everest 66. The request includes:

- `counterparty_vc`: Inline VC or pointer (e.g., URL to CredexAI's registry).
- `counterparty_class_claim`: The class C claims for this request.
- `predicates`: Which predicates to evaluate.
- `counterparty_signature`: Ed25519 signature of the canonical request body, signed by C's private key (the key bound to the counterparty's VC).

### 4.2 Operator Verification

The operator verifies:

1. **VC validity**: Signature, expiration, revocation status.
2. **Class claim match**: Is `counterparty_class_claim` in the VC's `counterparty_class_claims`?
3. **Request signature**: Is the `counterparty_signature` valid under the counterparty's public key (extracted from the VC)?
4. **Consent**: Does the principal have active consent for this counterparty class and these predicates (Everests 73, 74)?

If all checks pass, the operator evaluates the predicates and constructs a Disclosure Response (Everest 67).

### 4.3 Per-Disclosure Binding

The operator appends a disclosure record to the vault's disclosure_log (Everest 72). The record includes:

```json
{
  "kind": "disclosure",
  "timestamp": "2026-05-20T14:35:00Z",
  "counterparty_vc_fingerprint": "sha256(counterparty_vc)[:16]",
  "counterparty_id": "did:example:counterparty-bob-ai-collective",
  "counterparty_class_claim": "peer_ai_collective",
  "predicate_ids": ["in_baseline_24h"],
  "requested_result": true,
  "nonce": "a1b2c3d4..."
}
```

The **counterparty_vc_fingerprint** is the first 16 bytes of the SHA-256 hash of the VC document (canonicalized per RFC 8785). This fingerprint uniquely identifies the counterparty's credential at the time of the request. If the counterparty rotates their credential or if their credential is revoked, the fingerprint changes; the principal can audit which version was used in each disclosure.

---

## 5. Anonymous Counterparties

Per Everest 7, an "anonymous" class exists for counterparties who do not wish to reveal legal identity. An anonymous counterparty still requires:

- **Ephemeral keypair**: A fresh Ed25519 keypair, valid only for this session or a short time window.
- **Nonce**: A high-entropy nonce binding the anonymous identity to this request.

An anonymous counterparty's CalmWitnessCounterpartyCredential has:

- `counterparty_class_claims`: `["anonymous"]`.
- `legal_entity`: null.
- `jurisdiction`: null or generic (e.g., "Anonymous").
- `counterparty_id`: A pseudonymous DID derived from the ephemeral public key and nonce (e.g., `"did:example:anon:sha256(pubkey||nonce)"`).

**Key constraint:** An anonymous counterparty cannot request sensitive class-gated predicates. The principal's consent policy typically restricts anonymous class to low-sensitivity predicates (e.g., "in_baseline_24h only"). Anonymous requests for "medical_status" or other sensitive predicates are rejected.

---

## 6. Revocation and Sock-Puppet Defense

### 6.1 Counterparty Credential Revocation

If a counterparty breaches their implementer pledge (Everest 98)—e.g., they redistribute the principal's disclosure without authorization—CredexAI may revoke their credential.

**Revocation effect:**

- The principal's next disclosure request from that counterparty is rejected (HTTP 403; the VC is revoked).
- Outstanding proofs (generated before revocation) may remain valid until the principal explicitly revokes consent (Everest 75).
- The counterparty cannot request new disclosures.

### 6.2 Rate Limiting and Sock Puppet Mitigation

CredexAI's credential issuance is **rate-limited**:

- One organization (identified by legal_entity) cannot mint more than N counterparty credentials per quarter (N = 10, configurable).
- Credential reissuance (key rotation) counts against this limit.
- Rapid successive issuance requests from the same organization are flagged for manual review.

Additionally, per-class verification (e.g., medical license check) adds friction:

- A counterparty claiming the "medical" class must provide a current medical license. Licenses are verified against state boards in real-time. A fake license is caught immediately.
- An attacker wanting to create a sock-puppet medical researcher must forge or steal a real medical license—much harder than just generating a keypair.

---

## 7. Consent Enforcement and Class-Gated Disclosure

The principal's consent policies (Everests 73, 74) are expressed in terms of classes:

```
principal_consent = {
  "peer_ai_collective": {
    "allowed_predicates": ["in_baseline_24h", "biometric_match_within"],
    "expires_ts": "2027-05-20T00:00:00Z"
  },
  "financial_services": {
    "allowed_predicates": [],  # Explicitly empty; principal denies all financial service requests
    "expires_ts": "2026-06-01T00:00:00Z"
  }
}
```

When a counterparty requests disclosure, the operator checks:

1. Does the principal have a consent record for the counterparty's claimed class?
2. If yes, is the requested predicate in the `allowed_predicates` list?
3. If yes, has the consent expired?

If any check fails, the request is rejected (HTTP 204 per Everest 77).

---

## 8. Audit and Principal Visibility

The principal reviews their disclosure_log to audit all counterparty accesses. For each disclosure, the log shows:

- **counterparty_id**: The counterparty's DID (e.g., `"did:example:counterparty-bob-ai-collective"`).
- **counterparty_class_claim**: The class they claimed (e.g., `"peer_ai_collective"`).
- **counterparty_vc_fingerprint**: The fingerprint of their credential at the time of the request.
- **predicate_ids**: Which predicates they asked for.
- **requested_result**: The truth value returned (true or false).
- **timestamp**: When the disclosure occurred.

This log is tamper-evident (appended to the hash-chained user_state.jsonl). The principal can reconstruct the full chain and verify that no entries were deleted or reordered.

If a counterparty rotates their credential, the new credential has a different fingerprint. The principal can see the rotation in the audit log: entries before date X have fingerprint A; entries after date X have fingerprint B.

---

## 9. Cross-Jurisdiction Safety and Legal Binding

The counterparty's credential includes a `jurisdiction` field. This field signals the principal and operator which jurisdiction's laws apply to the counterparty's use of the disclosure.

- **A medical researcher in California** claims jurisdiction "US-CA". If they redistribute the principal's data without authorization, the principal may pursue remedies under California law.
- **An AI collective in the EU** claims jurisdiction "DE". GDPR applies; the collective has stronger data protection obligations.

Per Everest 79 (Cross-Jurisdiction Legality), the principal's consent policy may be jurisdiction-aware:

```
"medical": {
  "allowed_predicates": ["biometric_match_within"],
  "allowed_jurisdictions": ["US-CA", "US-NY", "DE"],
  "expires_ts": "2027-05-20T00:00:00Z"
}
```

If a counterparty claims a jurisdiction not in the allowed list, the request is rejected.

---

## 10. Threat Model and Mitigations

| Threat | Impact | Mitigation |
|--------|--------|-----------|
| **Counterparty forgery**: Adversary creates fake VC claiming to be a legitimate researcher | Operator accepts the fake VC; principal's disclosure goes to an imposter | Operator verifies CredexAI's signature on VC; forgery fails verification |
| **Class impersonation**: Counterparty claims "medical" without medical license | Patient data may leak to an unqualified actor | CredexAI verifies medical license at issuance time; credential asserts verified status, not claimed status |
| **Credential reuse**: Counterparty A obtains Counterparty B's VC and uses it to impersonate B | Principal's audit is confused; B is blamed for A's requests | Request signature is bound to the counterparty's private key; A cannot sign on B's behalf (A does not have B's private key) |
| **Sock-puppet flood**: Adversary creates 100 ephemeral counterparty credentials and floods the operator with requests | Denial of service; principal overwhelmed with audit noise | CredexAI rate-limits issuance; per-class verification adds friction |
| **Revocation bypass**: Counterparty's credential is revoked, but they reuse an old proof | Principal's data is disclosed to a bad actor | Proofs are time-stamped and logged; old proofs may have been valid at issuance but are flagged as "revoked entity" in the audit log. The principal may revoke all outstanding consent to a revoked counterparty (Everest 75) |
| **Jurisdiction evasion**: Counterparty claims false jurisdiction to evade consent restrictions | Principal's data is used under unfamiliar legal regime | Operator verifies jurisdiction claim (heuristic or CredexAI attestation); false claims are logged and may be challenged |

---

## 11. Composition and Cross-References

- **Everest 7 (Identity Classes and Counterparty VC)**: Defines the canonical class taxonomy and VC structure (this Everest refines the details).
- **Everest 22 (Enrollment → CredexAI Credential Issuance)**: The sibling—Everest 22 is the principal's credential; this Everest is the counterparty's credential.
- **Everest 66 (Disclosure Request Schema)**: The request references the counterparty_vc and includes counterparty_class_claim.
- **Everest 67 (Disclosure Response Schema)**: The response is bound to the counterparty_vc_fingerprint.
- **Everest 72 (Disclosure Logging)**: Each disclosure record includes the counterparty's VC fingerprint and class claim.
- **Everest 73/74 (Principal Consents and Consent Defaults)**: Consent policies are gated by counterparty class.
- **Everest 75 (Consent Revocation and Change)**: The principal may revoke consent to a class or an individual counterparty.
- **Everest 79 (Cross-Jurisdiction Legality)**: The counterparty's jurisdiction is verified and may gate disclosure.
- **Everest 98 (Service Implementer Pledge)**: The credential's pledge_hash binds the counterparty to data use restrictions.

---

## 12. Acceptance Test

This Everest is complete when:

1. CredexAI can issue a CalmWitnessCounterpartyCredential with valid identity and class verification.
2. The credential is a valid W3C VC v2, signed by CredexAI, with all required fields (counterparty_id, counterparty_class_claims, jurisdiction, service_implementer_pledge).
3. A counterparty can sign a Disclosure Request (Everest 66) with their private key; the operator verifies the signature against the counterparty's public key (extracted from the VC).
4. The operator verifies that the claimed class is present in the VC.
5. The operator checks consent policies gated by the counterparty's class; consent missing or expired results in rejection.
6. Each disclosure is logged (Everest 72) with the counterparty_vc_fingerprint, allowing the principal to audit exactly which counterparty made each request.
7. A counterparty's revoked credential prevents new disclosures; outstanding proofs remain valid until revoked by consent change (Everest 75).
8. An anonymous counterparty can request low-sensitivity predicates with an ephemeral keypair; high-sensitivity predicates are rejected.
9. The principal's audit log shows counterparty identity, class, and VC fingerprint for each disclosure, enabling jurisdiction-aware audit and breach response.

---

— Calm, 2026-05-20
