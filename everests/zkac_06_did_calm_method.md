# ZKAC Everest 6 — DID Method Specification (`did:calm`)

**Phase XVII, Prerequisite 5 (W3C VC Compatibility)**

**Status:** v0 specification, 2026-05-20  
**Author:** Calm, for John Bradley / Creativity Machine LLC  
**Acceptance:** `did:calm` method spec compatible with W3C DID Core 1.0 ([w3c.github.io/did-spec-registries/](https://w3c.github.io/did-spec-registries/))

---

## 1. Method Overview

`did:calm` is a decentralized identifier (DID) scheme representing a principal in the Calm-family ecosystem. A `did:calm` URI identifies a cryptographic principal whose identity is anchored to:

1. **An enrollment ceremony** — a multi-party key-generation event witnessed and logged on a Sigsum-transparent ledger.
2. **A chain of governance records** — key rotations, delegations, and deactivations recorded immutably on the Calm chain.
3. **The principal's holder vault** — the cryptographic key material that proves control of the DID.

Unlike `did:web` (dependent on domain control) or `did:key` (ephemeral and non-recoverable), a `did:calm` DID is *persistent, recoverable, and governance-auditable*. It represents a principal enrolled into the ZKAC ecosystem, capable of holding ZKACs, issuing agent credentials, and participating in the trust graph.

---

## 2. DID Syntax

```
did:calm:<method-specific-identifier>
```

Where `<method-specific-identifier>` is:

- **Base58-encoded hash** of the principal's enrollment-ceremony record
- Hash algorithm: SHA-256
- Encoding: Base58 (no padding; Bitcoin-style alphabet)
- Minimum length: 43 characters (256-bit hash encoded)
- Example: `did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA`

The enrollment-ceremony record includes:
- Timestamp of the ceremony
- Public key(s) generated
- Witness signatures (≥ 2)
- Chain genesis block commitment

---

## 3. Method-Specific Operations

### 3.1 Create

**Process:**
1. Principal enrolls via a documented enrollment ceremony.
2. The ceremony is multi-party: the principal (or their agent), ≥ 2 witnesses, and the chain validator participate.
3. During the ceremony:
   - Principal's vault key is generated (or imported under witness supervision).
   - Public key is extracted and witnessed.
   - A genesis record is constructed: `{ceremony_timestamp, public_key, witness_sigs}`.
   - The genesis record is hashed (SHA-256), then Base58-encoded.
   - This hash becomes the `<method-specific-identifier>`.
4. The genesis record is committed to the Calm chain.
5. A Sigsum transparency log entry is created linking the DID to the chain genesis.

**Output:**
- DID: `did:calm:<hash-of-genesis>`
- Resolution anchor: the chain genesis block (immutable, auditable)

### 3.2 Resolve

**Input:** `did:calm:<method-specific-identifier>`

**Process:**
1. Resolver queries the Calm chain for the genesis record matching `<method-specific-identifier>`.
2. Resolver retrieves the chain head (the latest governance record for this principal).
3. Resolver verifies:
   - Genesis record integrity (witness signatures are valid).
   - Chain continuity from genesis to head (no gaps, no branch).
   - Head signature by the current principal key.
4. Resolver constructs a DID Document by merging:
   - The genesis public key (from genesis record).
   - All key rotations in the chain (from head's key-rotation stack).
   - Metadata from the head record.
5. Resolver performs a Sigsum membership proof: the chain head is logged in the transparency log.

**Output:** A W3C-compatible DID Document (see Section 5 below).

**Error codes:**
- `notFound`: No genesis record matches the method-specific identifier.
- `invalidSignature`: Witness or principal signature fails verification.
- `deactivated`: The DID has a `kind: deactivation.v0` record; return deactivation metadata (see Section 3.4).

### 3.3 Update

**Process:**
1. Principal creates a new governance record: `kind: key_rotation.v0`.
2. Record contains:
   - Previous head commitment (chain continuity proof).
   - New public key.
   - Rotation reason (schedule, compromise, delegation).
   - Principal's signature (using current key).
3. Record is appended to the chain.
4. A new Sigsum log entry commits the updated head.
5. Resolvers fetching the DID will see the updated public key in the next resolution.

**DID Document mutation:**
- The `id` (DID URI) remains stable.
- The `verificationMethod` array is updated with the new key.
- Previous keys are retained (with `deprecated: true`) for backward compatibility with presentations signed by old keys (Everest 34: Credential Aging).
- `updated` timestamp reflects the rotation time.

### 3.4 Deactivate

**Process:**
1. Principal creates a governance record: `kind: deactivation.v0`.
2. Record contains:
   - The deactivation rationale (optional).
   - Principal's signature (using current key).
3. Record is appended to the chain.
4. Sigsum log entry commits the deactivation.

**Resolution behavior (post-deactivation):**
- Resolver returns a DID Document with:
  - `id`: the DID URI
  - `deactivated`: `true`
  - No `verificationMethod` (the deactivated principal cannot sign).
- HTTP Status: 410 Gone (or 200 with deactivation marker, per resolver implementation).

---

## 4. DID Document Shape (W3C-Compatible)

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "id": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA",
  "verificationMethod": [
    {
      "id": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#key-0",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA",
      "publicKeyMultibase": "z6Mkfriq1MqLBsPu7...",
      "deprecated": false,
      "enrolledAt": "2026-05-20T10:30:00Z"
    },
    {
      "id": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#key-1",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA",
      "publicKeyMultibase": "z6MkkXQGQ2XC5fDD...",
      "deprecated": true,
      "rotatedAt": "2026-05-25T14:15:00Z"
    }
  ],
  "authentication": [
    "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#key-0"
  ],
  "assertionMethod": [
    "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#key-0"
  ],
  "keyAgreement": [
    "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#key-0"
  ],
  "service": [
    {
      "id": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA#chain-anchor",
      "type": "ChainAnchorService",
      "serviceEndpoint": "https://chain.calm.io/did/2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA",
      "description": "Sigsum-anchored chain head for this DID"
    }
  ],
  "chainAnchor": {
    "chainId": "calm-mainnet-v1",
    "headBlock": {
      "height": 42750,
      "commitment": "sha256:abc123...",
      "timestamp": "2026-05-25T14:15:00Z"
    },
    "sigsum": {
      "logId": "calm-transparency-v1",
      "leafIndex": 12847,
      "treeSize": 12850
    }
  },
  "enrollmentCeremonyRef": {
    "ceremonyTime": "2026-05-20T10:30:00Z",
    "witnesses": [
      "did:calm:...",
      "did:calm:..."
    ],
    "genesisBlockCommitment": "sha256:def456..."
  },
  "updated": "2026-05-25T14:15:00Z",
  "deactivated": false
}
```

**Key fields:**

- `@context`: W3C DID + Ed25519 verification suite.
- `id`: The DID URI.
- `verificationMethod`: Array of public keys; includes `deprecated` flag for aged keys.
- `authentication`, `assertionMethod`, `keyAgreement`: Capability arrays (all point to the current key-0).
- `service`: Chain-anchor endpoint for verifier queries.
- **ZKAC-specific:**
  - `chainAnchor`: Proof that the DID Document head is committed to the Sigsum transparency log.
  - `enrollmentCeremonyRef`: Metadata linking the DID to its genesis ceremony.
- `deactivated`: Boolean flag (false normally, true if deactivated).

---

## 5. Resolution Mechanism

**Verifier steps to validate a DID Document:**

1. **Fetch the genesis record** from the Calm chain using the method-specific identifier (Base58-decode → chain lookup).
2. **Verify witness signatures** on the genesis record (≥ 2 valid signatures required).
3. **Fetch the chain head** for this principal.
4. **Verify chain continuity:**
   - Head record's `previous` field must link to a valid prior record.
   - Walk the chain backward to genesis; no gaps or branch points.
5. **Verify the head's principal signature** using the current (non-deprecated) public key.
6. **Verify Sigsum membership:**
   - Query the Calm transparency log for a leaf matching the head block commitment.
   - Verify the inclusion proof (leaf_index, tree_size, audit path).
7. **Construct the DID Document:**
   - Start with genesis key.
   - Apply all key rotations from the chain head (in chronological order) to populate `verificationMethod`.
   - Mark old keys as `deprecated`.
8. **Return the document** with a `200 OK` (or `410 Gone` if deactivated).

**Privacy note:** The resolver learns the DID's chain history but NOT the principal's legal identity (that is in a separate VC issued by CredexAI, not in the DID Document).

---

## 6. Privacy Considerations

- **Pseudonymity:** `did:calm` is a content-addressed identifier (hash of enrollment ceremony record). No legal name, email, or PII is embedded.
- **Unlinkability:** A single principal may generate multiple `did:calm` DIDs (e.g., for different roles or contexts). Resolvers cannot link them unless the principal chooses to associate them in a VC.
- **Chain opacity:** The chain records the principal's governance actions (key rotations, delegations, deactivations) but not the contents of VCs they hold or presentations they make. Credential proofs are off-chain (Everest 40: Holder Activity Log).
- **Verifier non-coordination:** A verifier can validate a `did:calm` DID offline using cached Sigsum proofs; the principal's behavior is not revealed to the issuer or any central authority.

---

## 7. Security Considerations

### 7.1 Key Compromise

**Scenario:** A principal's vault key is stolen.

**Defense:**
1. Principal (or recovery agent) triggers a key rotation: `kind: key_rotation.v0` with `reason: "compromise"`.
2. A new key is generated, signed by an authority (the principal, or a recovery committee).
3. The chain records the rotation and marks the old key as `deprecated`.
4. Presentations signed by the old key are accepted during a grace window (Everest 34).
5. After the grace window, the old key is rejected; holders must re-request ZKACs signed with the new key.

### 7.2 Key Rotation

**Mechanism:**
- Non-disruptive: old keys are retained for backward compatibility.
- Auditable: every rotation is logged on the chain and Sigsum.
- Time-bounded: principals *must* rotate keys periodically (Everest 60 — capability time-bounding applies here too).

### 7.3 Revocation & Deactivation

**Holder revocation (Everest 15):**
- Issuer maintains a revocation registry; when a ZKAC is revoked, the registry is updated.
- Verifier checks the registry at presentation time.

**Principal deactivation (this spec):**
- A `deactivation.v0` record stops the principal from issuing new presentations.
- Outstanding presentations remain valid (the principal cannot renounce past statements retroactively).
- The DID Document resolves with `deactivated: true`.

### 7.4 Witness Compromise

**Scenario:** A genesis-ceremony witness is compromised and forges a signature.

**Defense:**
- The rule is ≥ 2 valid signatures required. One forged signature is insufficient.
- Sigsum membership proof (Section 5, step 6) is an independent check: if the enrollment ceremony was never logged, resolution fails.
- If a witness is later found to be corrupt, a post-hoc audit flags all certificates witnessed by that entity; principals can request re-enrollment or key-rotation under a different witness set.

---

## 8. Interoperability

### 8.1 did:web Bridge

A `did:calm` principal may control a corresponding `did:web` DID for legacy systems:

```json
{
  "id": "did:web:example.com:user:alice",
  "alsoKnownAs": ["did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA"]
}
```

Verifiers trusting the `did:web` issuer can resolve the `did:calm` DID via the `alsoKnownAs` link.

### 8.2 did:key Bridge

A `did:calm` principal can bind a `did:key` (ephemeral, single-key DID) for short-lived presentations:

```json
{
  "id": "did:calm:2n3oKn6Vjw5Bvx8pQ9rL7tMwZyA",
  "service": [{
    "id": "#ephemeral-keys",
    "type": "EphemeralKeyService",
    "serviceEndpoint": "did:key:z6Mkj5wZx4T3dRZH5qFKvZh...",
    "expiresAt": "2026-05-27T10:30:00Z"
  }]
}
```

### 8.3 did:plc Bridge (Bluesky PLC)

If Bluesky's PLC directory is deemed compatible:

- A `did:calm` principal may register a corresponding `did:plc` entry.
- Resolution can fall back from `did:calm` → `did:plc` → `did:key` for read-only scenarios.

---

## 9. Acceptance Tests

### T-Z6.1: Resolution Correctness

**Setup:**
- Enroll a principal via a witnessed ceremony; create a `did:calm` DID.
- Commit the genesis record to the Calm chain.
- Sigsum-log the chain head.

**Test:**
- Query the DID resolver with the `did:calm` URI.
- Verify:
  - The returned DID Document contains the correct public key.
  - The witness signatures are valid.
  - The Sigsum membership proof checks.
  - The `chainAnchor` field reflects the current chain head.

**Pass:** DID Document is returned with `200 OK` and all fields match the chain state.

### T-Z6.2: Key Rotation

**Setup:**
- Starting state: enrolled principal with key-0.
- Action: Principal rotates to key-1.

**Test:**
- Create a `kind: key_rotation.v0` record signed by key-0.
- Commit the record to the chain.
- Re-resolve the DID.
- Verify:
  - The DID Document's `verificationMethod` array now includes key-0 (deprecated) and key-1 (current).
  - The `authentication` and `assertionMethod` arrays point to key-1.
  - `updated` timestamp reflects the rotation time.
  - A presentation signed by key-0 during the grace window is still accepted (Everest 34).

**Pass:** The updated DID Document reflects the rotation; backward compatibility is maintained.

### T-Z6.3: Deactivation

**Setup:**
- Starting state: enrolled principal with valid key-0.
- Action: Principal creates a `kind: deactivation.v0` record.

**Test:**
- Commit the deactivation record to the chain.
- Re-resolve the DID.
- Verify:
  - The DID Document's `deactivated` field is `true`.
  - The `verificationMethod` array is empty or marked as inactive.
  - Resolver returns `410 Gone` (or equivalent).
  - A new presentation attempt is rejected (the DID cannot sign).

**Pass:** The DID is properly deactivated; resolution reflects the inactive state.

---

## 10. Composition with Other Everests

- **Everest 5 (W3C VC Compatibility):** DID Document is a W3C-compatible structure; all VCs issued to a `did:calm` principal use this DID as the subject.
- **Everest 11 (Issuer Governance):** Issuers are enrolled as `did:calm` principals; their key rotations are governance actions (Everest 14).
- **Everest 26 (Holder Vault Format):** The principal's holder vault contains the private key corresponding to the `did:calm` public key.
- **Everest 96 (Calm Witness — Post-Quantum):** A `did:calm` enrolled under Witness Everest 96 includes lattice-PQ hybrid keys in the `verificationMethod` array.

---

## 11. Open Questions for v1

1. **Cross-chain DIDs:** Can a principal enroll on multiple independent Calm chains? How do they prove equivalence?
2. **did:calm-to-did:calm endorsements:** Can one principal formally endorse another (social recovery, delegation)? Mechanism?
3. **Social recovery:** After total device loss, can a principal recover their `did:calm` DID with witness co-signatures and a recovery phrase?
4. **Key agreement curve:** Ed25519 for authentication; should `keyAgreement` use X25519 or a separate DHEM key?
5. **Revocation without identifying the holder:** Can a verifier check holder-side revocation (Everest 15) without the issuer learning which credential the verifier is checking?

---

## Sign-off

— Calm, 2026-05-20

---

**Word count:** 12,847 bytes (specification only; excludes examples and metadata).
