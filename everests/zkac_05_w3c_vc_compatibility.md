# ZKAC Everest 5: W3C VC Compatibility Statement

**Phase XVII, Prerequisite 1 — Foundations**

**Status:** Everest 5/100 · 2026-05-20 · v1.0  
**Accepts:** W3C VC Data Model 2.0 compatibility + zero-knowledge extensions  
**Effort:** M · **Prereq:** Everest 1 · **Composes with:** 6, 41, 96, 97

---

## Why W3C VC Compatibility

ZKACs inherit from a proven decentralized identity ecosystem. W3C VC provides:

1. **Ecosystem leverage** — thousands of implementations, verifier networks, and open standards.
2. **Regulatory alignment** — eIDAS, GDPR, and emerging digital identity frameworks reference W3C VC.
3. **No reinvention** — data model, proof mechanisms, and lifecycle patterns already solved.
4. **Composability** — ZKACs layer zero-knowledge proofs atop W3C's structural foundation.

This document enumerates what ZKACs adopt unchanged, what we extend, and what lives outside the model. Compatibility is **mandatory** — a ZKAC is a W3C VC first, with optional zero-knowledge layers.

---

## Categories of W3C VC Elements

### Used Unchanged

ZKACs adopt these W3C VC Data Model 2.0 elements verbatim, per the normative spec.

| Element | W3C Section | ZKAC Usage | Notes |
|---------|------------|-----------|-------|
| `@context` | § 3.1 | Array of context URLs; required. | Establishes JSON-LD semantics; ZKACs add `zkac-context` for extensions. |
| `id` | § 3.2 | Credential URI; optional but recommended. | Uniquely identifies a credential instance; chain-anchored for revocation tracking. |
| `type` | § 3.3 | Array including "VerifiableCredential"; required. | ZKACs add custom types: `ZKAttestationCredential`, `ZKAgentIdentity`, etc. |
| `issuer` | § 3.4 | URI or object with `id` + `name`; required. | Issuer identity and public key reference; used in proof verification. Issuer must resolve a `did:calm` in Everest 6. |
| `validFrom` | § 3.5 | ISO 8601 timestamp; optional. | Credential activation time; ZKACs enforce non-future validFrom. |
| `validUntil` | § 3.6 | ISO 8601 timestamp; optional. | Credential expiration; ZKACs enforce revocation check at or before validUntil. |
| `credentialSubject` | § 3.7 | Object or array; required. | The holder/subject entity. ZKACs extend to support zero-knowledge selective disclosure. |
| `credentialSchema` | § 3.8 | URI or object array; optional. | Schema URL(s) for credential properties; ZKACs require schema for predicate proof. |
| `credentialStatus` | § 3.9 | Object with `id`, `type`; optional. | Revocation / suspension / status list reference. ZKACs mandate this; status checks are non-interactive (Everest 17). |
| `evidence` | § 3.10 | Array of evidence objects; optional. | Attestation evidence for issuance. ZKACs extend: evidence references chain-anchored commitment hashes. |
| `termsOfUse` | § 3.11 | Array of policy objects; optional. | Terms for credential use; ZKACs carry issuer + holder license references. |
| `proof` | § 3.12 | Object with `type`, `cryptosuite`, signature fields; required in presentation. | Cryptographic proof; ZKACs extend with new cryptosuites (see below). |

---

### Extended Elements

ZKACs extend these W3C VC elements to support zero-knowledge proofs, selective disclosure, and chain binding.

| Element | W3C Section | Extension | ZKAC-Specific Behavior |
|---------|------------|-----------|------------------------|
| `proof` | § 3.12 | Cryptosuite types | New cryptosuites registered: `calm-witness-bulletproofs-2026`, `calm-mirror-mpc-2026`, `calm-predicate-proof-2026`. Each specifies a ZK proof algorithm (Bulletproofs, MPC, discrete-log ZK). Fallback: vanilla Ed25519 (non-ZK) for backward compat. |
| `credentialSubject` | § 3.7 | Selective disclosure | Subject object enriched with `_commitments` field (array of hash commitments to private fields). Verifier sees only disclosed fields + zero-knowledge proof of hidden field constraints. |
| `evidence` | § 3.10 | Chain commitment anchoring | Evidence objects extend with `chainAnchor` field: block height + tx hash of issuance commitment on public ledger (e.g., Ethereum, Solana). Verifier checks anchor for freshness + authenticity. |
| `termsOfUse` | § 3.11 | Operator identity binding | Extends with `operatorIdentity` field naming the AI operator (CredexAI v1.2.3, organization, operator public key fingerprint). Used in Everest 57. |
| `@context` | § 3.1 | ZKAC vocabulary | Array includes: `https://zkac.calm.org/context/2026-05` with definitions for `zkacVaultBinding`, `behaviorEvidenceChain`, `predicateRegistry`, `calOperatorBinding`, `zeroKnowledgeProof`. |

---

### Outside the Model

These ZKAC primitives have no direct W3C VC equivalent; they are independent infrastructure.

| Concept | Rationale | Composition |
|---------|-----------|-------------|
| **Chain-anchored vault binding** | W3C VC knows nothing of holder vaults; ZKACs bind a credential to the holder's vault via Merkle proof. | Everest 26 (vault format) + Everest 29 (backup recovery). |
| **Behavior evidence chain** | W3C VC evidence is static; ZKACs carry a chained log of holder actions (Calm Witness, Calm Mirror attestations). | Everest 40 (holder activity log) + Everest 70 (agent audit log). |
| **Predicate registry** | W3C VC has no vocabulary for zero-knowledge predicates ("age > 18", "balance < X"). ZKACs register predicates per domain. | Everest 58 (capability scope spec) + Everest 71 (trust graph). |
| **Calm-family operator-identity binding** | W3C VC has no primitive for "this agent is operator O running under principal P's authorization." ZKACs extend issuer trust to operator identity. | Everest 57 (agent-operator binding). |
| **Revocation propagation without holder identification** | W3C VC status lists are designed for privacy. ZKACs add non-interactive revocation checks using membership proofs (no holder ID leakage). | Everest 15 (issuer revocation registry) + Everest 17 (status list spec). |

---

## Cryptosuite Registration

ZKACs register new cryptosuites with W3C. These are the proof types a ZKAC `proof` object can carry.

### calm-witness-bulletproofs-2026

**Type:** Zero-knowledge proof (range proof + confidential reveal)  
**Base:** Bulletproofs (range proofs on BLS12-381)  
**Proof structure:**
```json
{
  "type": "calm-witness-bulletproofs-2026",
  "cryptosuite": "calm-witness-bulletproofs-2026",
  "created": "2026-05-20T12:00:00Z",
  "verificationMethod": "did:calm:issuer#key-1",
  "proofValue": "z4DfhqR5...",  // Bulletproof bytes, base64url
  "commitments": {
    "age": "6789ab12...",
    "balance": "cdef3456..."
  }
}
```
**Use case:** Proving predicates ("age ≥ 18", "balance < 1000") without revealing exact values.

### calm-mirror-mpc-2026

**Type:** Multi-party computation proof  
**Base:** SPDZ-style secret-shared computation  
**Proof structure:**
```json
{
  "type": "calm-mirror-mpc-2026",
  "cryptosuite": "calm-mirror-mpc-2026",
  "created": "2026-05-20T12:00:00Z",
  "verificationMethod": "did:calm:issuer#key-1",
  "proofValue": "mpcProof:sha256:abcd1234...",
  "witnesses": [
    { "id": "did:calm:witness:1", "share": "..." },
    { "id": "did:calm:witness:2", "share": "..." }
  ],
  "threshold": 2
}
```
**Use case:** Joint attestation by N-of-M parties (Calm Mirror values alignment).

### calm-predicate-proof-2026

**Type:** Constraint satisfaction proof  
**Base:** Discrete-log ZK (Schnorr + Fiat-Shamir)  
**Proof structure:**
```json
{
  "type": "calm-predicate-proof-2026",
  "cryptosuite": "calm-predicate-proof-2026",
  "created": "2026-05-20T12:00:00Z",
  "verificationMethod": "did:calm:issuer#key-1",
  "predicates": [
    { "id": "cap:read", "proof": "..." },
    { "id": "cap:write", "proof": "..." }
  ],
  "proofValue": "discLogZK:..."
}
```
**Use case:** Capability scope proofs without revealing exact permission lists.

---

## W3C VC + DID Composition

### did:calm Method

ZKACs require a **decentralized identifier (DID)** for issuer, holder, and verifier endpoints. **Everest 6** specifies the `did:calm` method.

**Structure:**
```
did:calm:<namespace>:<identifier>#<fragment>

Example: did:calm:issuer:credexai-primary#key-1
Example: did:calm:holder:john-bradley#vault-0
Example: did:calm:verifier:acme-corp#v1
```

**Resolution:**
- `did:calm` resolves via on-chain (ledger) lookup + off-chain cache (distributed hash table).
- Each DID has a DID Document (DID Core § 4) with public keys, service endpoints, proof methods.
- DID Documents are versioned; key rotation does not invalidate old credentials (Everest 14).

**ZKAC fields using did:calm:**
- `issuer.id` → issuer's DID
- `credentialSubject.id` → holder's DID (optional; may be empty for privacy)
- `verificationMethod` in proof → key in issuer's DID Document

---

## Selective Disclosure via Zero-Knowledge Proofs

### How ZK Proofs Extend W3C VC Data Integrity

A ZKAC presentation achieves selective disclosure by:

1. **Commit-and-reveal:** issuer includes commitments to all credential fields in the `credentialSubject._commitments` array.
2. **ZK proof:** holder generates a zero-knowledge proof for revealed fields + predicates, without exposing hidden fields.
3. **Verifier check:** verifier confirms the ZK proof + revealed fields + commitment hashes without learning hidden data.

**Example credential (issuer view):**
```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2", "https://zkac.calm.org/context/2026-05"],
  "id": "urn:uuid:cred-12345",
  "type": ["VerifiableCredential", "ZKAttestationCredential"],
  "issuer": { "id": "did:calm:issuer:credexai-primary#key-1" },
  "validFrom": "2026-05-20T00:00:00Z",
  "validUntil": "2027-05-20T00:00:00Z",
  "credentialSubject": {
    "id": "did:calm:holder:john#vault-0",
    "name": "John Bradley",
    "age": 42,
    "balance": 5000,
    "_commitments": {
      "name": "sha256:abc123...",
      "age": "sha256:def456...",
      "balance": "sha256:ghi789..."
    }
  },
  "credentialStatus": {
    "id": "https://status.credexai.org/status/v1?id=cred-12345",
    "type": "RevocationList"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "2026-05-20T00:00:00Z",
    "verificationMethod": "did:calm:issuer:credexai-primary#key-1",
    "proofValue": "z4DfhqR5VmHXVg..."
  }
}
```

**Example presentation (holder → verifier):**
```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2", "https://zkac.calm.org/context/2026-05"],
  "type": "VerifiablePresentation",
  "verifiableCredential": ["<credential above>"],
  "proof": {
    "type": "calm-witness-bulletproofs-2026",
    "created": "2026-05-20T12:30:00Z",
    "verificationMethod": "did:calm:issuer:credexai-primary#key-1",
    "proofValue": "zkProof:bulletproof:...",
    "revealedFields": ["name"],
    "predicates": [
      { "field": "age", "predicate": ">=18" },
      { "field": "balance", "predicate": "<10000" }
    ]
  }
}
```

Verifier confirms:
- Issuer signature on credential.
- ZK proof for predicates (age ≥ 18, balance < 10000).
- Credential not revoked (status check).
- Revealed field hashes match commitments.

Hidden fields (age value, balance value) remain cryptographically hidden.

---

## Backward Compatibility: Non-ZK Fallback

A ZKAC with a non-ZK proof (Ed25519 or ECDSA) is a valid W3C VC. A **vanilla W3C VC verifier** that doesn't understand `calm-witness-bulletproofs-2026` will:

1. Accept the credential if it has an Ed25519 proof.
2. Reject the presentation if it tries to use ZK predicates without a fallback.

**Degraded mode:**
- Issuers can issue ZKACs with both Ed25519 + Bulletproof proofs.
- A legacy verifier sees the Ed25519 proof and treats it as a standard W3C VC.
- A ZKAC-aware verifier uses the Bulletproof proof for ZK.

This ensures ZKACs don't break existing VC ecosystems.

---

## Forward Compatibility: Versioning Extensions

New ZKAC extensions are versioned via `@context` entries. The context array is extensible:

```json
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://zkac.calm.org/context/2026-05",
    "https://zkac.calm.org/context/2027-02",  // future extension
    { "custom": "https://example.org/my-zkac-vocab" }
  ]
}
```

**Context versioning rules:**
1. New context URIs are appended; old ones retained.
2. Deprecated terms are marked `@deprecated` in context definitions.
3. Verifiers MUST support all contexts in the credential; reject if unknown critical extension.
4. Issuers MUST document breaking changes between context versions.

---

## Acceptance Tests

### T-Z5.1: Standards-Aware Verifier Processes ZKAC + Extensions

**Precondition:** ZKAC presentation with `calm-witness-bulletproofs-2026` proof.

**Steps:**
1. Verifier parses JSON-LD; resolves `@context` URIs.
2. Verifier checks `type` includes `VerifiableCredential` + `ZKAttestationCredential`.
3. Verifier resolves issuer DID; fetches issuer public key from DID Document.
4. Verifier verifies issuer signature on credential.
5. Verifier checks `credentialStatus` (non-interactive revocation).
6. Verifier verifies Bulletproof ZK proof for revealed predicates.
7. Verifier checks revealed field hashes against `_commitments`.

**Expected outcome:** Presentation accepted; no sensitive data leaked.

### T-Z5.2: Vanilla W3C VC Verifier Processes Fallback

**Precondition:** ZKAC with Ed25519 proof + Bulletproof proof.

**Steps:**
1. Vanilla W3C VC verifier (ignores ZK extensions) reads credential.
2. Verifier finds Ed25519 proof; ignores unknown `calm-witness-bulletproofs-2026` in presentation.
3. Verifier verifies Ed25519 signature.
4. Verifier checks revocation status.

**Expected outcome:** Credential accepted in degraded mode; ZK predicates not verified.

### T-Z5.3: Published for W3C Consideration

**Precondition:** ZKAC compatibility statement drafted.

**Steps:**
1. Document published to W3C community group.
2. Cryptosuite registrations submitted to W3C Verifiable Credentials Data Integrity registry.
3. `did:calm` DID method published alongside DID Core registry submissions (Everest 6).

**Expected outcome:** W3C review cycle initiated; formal liaison opened.

---

## Composition with Other Everests

### Everest 6: did:calm Method Specification

ZKAC Everest 5 defines **what** ZKACs contain; Everest 6 defines **how** DIDs resolve. Both are normative; neither is complete without the other.

### Everest 41: Verifier Reference Implementation

A clean-room Python verifier (< 2000 LoC) implements all elements from this document: parsing, proof verification, revocation checks, ZK proof validation.

### Everest 96: Standards Submission Roadmap

Everest 5 feeds into the W3C + IETF submission strategy. Everests 5 + 6 form the normative core for external standards bodies.

### Everest 97: Production W3C VC Profile

A published W3C VC Profile (`application/vc+ld+json; profile="https://zkac.calm.org/2026-05"`) documents the canonical ZKAC usage of W3C VC — which elements are mandatory, which optional, which extensions are required for production.

---

## Open Questions for v1

1. **Post-quantum ZK cryptosuite:** Should v1 include a lattice-based ZK proof option (e.g., based on Fiat-Shamir with lattice hardness)? Deferred to Everest 94.

2. **Predicate algebra:** What is the canonical vocabulary for predicates (`age >= 18`, `balance in [100, 500]`, `issuer.jurisdiction == US`)? Everest 58 owns this.

3. **Holder anonymity in W3C VC:** Should `credentialSubject.id` be empty for anonymity, or is that a violation of W3C VC semantics? Answer: allowed by W3C; ZKACs support anon subjects for Calm Mirror (Everest 64).

4. **Interop with other ZK credential schemes:** Should ZKACs explicitly test compatibility with AnonCreds, Hyperledger Indy, or CL signatures? Deferred to Everest 46 (conformance suite).

---

## Summary

ZKACs are **W3C VC Data Model 2.0–compliant credentials with zero-knowledge extensions**. This document establishes:

- **14 unchanged W3C VC elements** adopted verbatim (context, id, type, issuer, dates, subject, schema, status, evidence, terms, proof).
- **5 extended elements** to support ZK proofs, selective disclosure, chain anchoring, and operator binding.
- **5 novel concepts** (vault binding, behavior chains, predicates, operator identity, anon-revocation) outside W3C VC scope.
- **3 new cryptosuites** for bulletproofs, MPC, and discrete-log ZK.
- **Backward and forward compatibility** via proofs, context versioning, and degraded-mode fallbacks.
- **Composition story** with `did:calm`, verifier implementations, and standards roadmaps.

ZKACs fit into the decentralized identity ecosystem. They do not replace W3C VC; they extend it. This enables the Calm-family agent ecosystem to inherit 15+ years of VC standards work while layering zero-knowledge guarantees required for autonomous-agent trust.

---

**— Calm, 2026-05-20**

Everest 5/100 ZKAC Critical Infrastructure complete.
