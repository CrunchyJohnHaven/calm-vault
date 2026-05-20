# ZKAC Everest 56 — Agent Identity Primitive

**Phase XXI — Agent Identity & Capability**  
**Prerequisite:** ZKAC Everest 5 (W3C VC compatibility)  
**Status:** v0 · 2026-05-20 · open for adversarial review

---

## Statement of Purpose

An **agent identity primitive** is a credential subtype for an AI operator acting on behalf of a principal under an explicit, narrowed capability set. It answers the fundamental question: *"Who is acting, on behalf of whom, authorized to do what?"*

In the Calm-family ecosystem, agents are not abstract software entities. Each agent carries a credential issued by its principal, bearing:
- The agent's identity (software version, operator organization, cryptographic binding to the operator)
- The principal's identity (the human or organization whose vault the agent operates)
- A named capability set (read, write, attest, transact, delegate, etc.) — always a strict subset of the principal's full capabilities
- Time bounds (explicit expiration; no perpetual delegation)
- Revocation rights (the principal can unilaterally revoke at any time)

This primitive is essential for three reasons:

1. **Principal accountability:** When an agent acts, the principal retains cryptographic proof of what authorization was given, and what the agent actually did (via ZKAC Everest 70: Agent audit log).

2. **Operator transparency:** The agent's credential publicly names the software (hash, version, organization) running it. Counterparties can inspect the operator identity and decide whether to trust that particular agent.

3. **Capability scoping:** The principal can delegate only the minimum necessary authority. An agent reading the principal's vault does not automatically gain write access to it, nor can it delegate to a third agent without explicit new authorization.

---

## The Agent Identity Credential

An agent identity credential is a W3C Verifiable Credential (VC) that extends the standard VC `credentialSubject` with an `agent` block. It uses the `did:calm` identifier scheme (ZKAC Everest 6).

### Credential Structure

```jsonc
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://calm-family.github.io/zkac/contexts/2026-05.jsonld"
  ],
  "type": ["VerifiableCredential", "AgentIdentityCredential"],
  "issuer": "did:calm:principal:5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
  "issuanceDate": "2026-05-20T14:30:00Z",
  "credentialSubject": {
    "id": "did:calm:agent:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
    "agent": {
      "actsOnBehalfOf": "did:calm:principal:5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
      "operator": {
        "name": "calm-witness-agent",
        "version": "0.1.0",
        "softwareHash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "softwareUrl": "https://github.com/calm-family/calm-witness-agent/releases/tag/0.1.0",
        "organization": "did:calm:org:ai-moneyball-entity"
      },
      "capabilities": [
        {
          "name": "read",
          "scope": {
            "resources": ["vault:vault_baseline", "vault:consent_records"],
            "operations": ["inspect", "query_predicate"],
            "excludes": []
          }
        },
        {
          "name": "attest",
          "scope": {
            "resources": ["disclosure:user_state_proof"],
            "operations": ["issue_zk_proof"],
            "excludes": ["issue_non_zk_proof"]
          }
        }
      ],
      "scope": {
        "narrowingRules": [
          "read_only: agent cannot mutate principal vault state",
          "predicate_match: agent can only operate on predicates where principal has granted consent",
          "no_sub_delegation: agent cannot issue agent credentials to sub-agents without explicit new principal authorization"
        ]
      },
      "expiresAt": "2026-08-20T14:30:00Z",
      "rotationOf": null,
      "issuedAt": "2026-05-20T14:30:00Z"
    }
  },
  "proof": {
    "type": "EcdsaSecp256k1Signature2019",
    "created": "2026-05-20T14:30:00Z",
    "verificationMethod": "did:calm:principal:5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0#vault-key-2026",
    "signatureValue": "3045022100e3b0c44298fc1c149afbf4c8996fb924270f90298c8f3f8a1c7c3e2d0f8b9a8d022100a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0"
  }
}
```

### Field Explanation

- **id**: The agent's unique DID in the `did:calm:agent:` namespace. Derived from the principal's identity, operator software hash, and issuance timestamp to ensure uniqueness and prevent ID collisions.

- **actsOnBehalfOf**: The principal's DID (`did:calm:principal:...`). Binds the agent credential to a specific principal. Only that principal can revoke this credential.

- **operator.name**: Human-readable name of the operator software (e.g., `calm-witness-agent`, `moneyball-engine-v1`).

- **operator.version**: Semantic version of the operator (e.g., `0.1.0`). This allows principals and counterparties to track which version of the software is in use.

- **operator.softwareHash**: SHA-256 hash of the operator binary or container image. This is the cryptographic identity of the software. Changing the code changes the hash; the agent cannot misrepresent its software version.

- **operator.softwareUrl**: Public URL where the operator source or binary can be inspected. Enables transparency and auditability.

- **operator.organization**: The organization (as a DID) that publishes and maintains the operator. Allows counterparties to evaluate organizational trustworthiness.

- **capabilities**: Array of named capabilities. Each capability has:
  - **name**: One of {`read`, `write`, `transact`, `attest`, `delegate`} (extended in ZKAC Everest 58).
  - **scope**: Narrowing rules per capability. For read: which resources can be inspected. For write: what mutations are allowed. For attest: what proofs can be issued. For transact: what actions can be taken. For delegate: what sub-delegations are permitted (if any).

- **scope.narrowingRules**: High-level constraints on agent behavior. Enforced by the principal's vault operator and by verifiers. Examples:
  - `read_only`: Agent has no write authority.
  - `predicate_match`: Agent can only issue proofs for predicates the principal consented to disclose.
  - `no_sub_delegation`: Agent cannot issue new agent credentials without explicit principal re-authorization.

- **expiresAt**: ISO 8601 timestamp. The agent credential is valid only until this time. After expiry, the agent cannot present this credential or exercise its capabilities. The principal must issue a new credential to extend the agent's authority.

- **rotationOf**: If this credential supersedes a prior agent credential (e.g., due to software upgrade), this field points to the prior credential's ID. Used for credential rotation (ZKAC Everest 61). Null if this is a fresh issuance.

---

## Six Structural Invariants

### Invariant 1: Principal Authority is Absolute

**Statement:** Only the principal (holder of the vault master key) can authorize an agent credential bearing their identity. Issuers attest; they do not author.

**Implementation:** The agent credential is signed exclusively by the principal's vault key (`did:calm:principal:...#vault-key-YYYY`). No co-signer, witness, or third-party authorization is required. The principal unilaterally decides to delegate to an agent.

**Rationale:** The principal must retain authority over delegation. If an issuer or witness could authorize an agent on the principal's behalf, the principal could lose control of their vault. Per ZKAC design constraint 1, principal authority is non-negotiable.

---

### Invariant 2: Operator Transparency

**Statement:** The operator software hash, version, organization, and source URL are public and immutable in the credential.

**Implementation:** The `operator` block is included in the signed payload. Any change to the operator identity requires issuing a new credential, creating an auditable chain of agent versions.

**Rationale:** Counterparties need to know which software is acting on the principal's behalf. A verifier can inspect the agent credential, extract the operator identity, and decide: "Do I trust calm-witness-agent v0.1.0 published by did:calm:org:ai-moneyball-entity?" This prevents operator disguise and enables transparent agent lifecycle management.

---

### Invariant 3: Capability Narrowing

**Statement:** The agent's capability set is always a strict subset of or equal to the principal's full capabilities. Capabilities can only narrow over the credential's lifetime; they cannot expand.

**Implementation:** Each capability includes a `scope` object specifying which resources, operations, or predicates are permitted. The principal can issue a derivative agent credential with fewer capabilities (e.g., an agent that can only read, not write). It cannot issue a credential that grants new capabilities beyond what the principal holds.

**Rationale:** Delegation is minimization. The agent operates under the least-privilege principle. If the principal discovers the agent is compromised, the agent's authority is capped by its credential scope.

---

### Invariant 4: Time-Bound Authority

**Statement:** Every agent credential has an explicit `expiresAt` timestamp. No perpetual agent credentials exist.

**Implementation:** The `expiresAt` field is mandatory. If the principal does not specify an expiry, the credential is rejected. (Recommended default: 90 days from issuance, per ZKAC Everest 8 analogous time-bounding axiom.)

**Rationale:** Perpetual delegation is a vulnerability. An agent credential issued years ago may carry outdated assumptions about the principal's intent. Time-bounding forces the principal to periodically re-evaluate and re-authorize. When an agent credential expires, the agent must request a new one, creating an opportunity for the principal to revoke if circumstances have changed.

---

### Invariant 5: Unilateral Revocability

**Statement:** The principal can revoke an agent credential at any time, with immediate effect (within the bounded latency defined by ZKAC Everest 62).

**Implementation:** The principal appends a revocation record to their vault chain (similar to consent revocation in ZKAC Everest 8). The revocation is signed by the principal, chained into the vault, and published to the transparency log. Downstream verifiers check the revocation status before accepting presentations from the agent.

**Rationale:** The principal must not be held hostage by an agent. If the agent is compromised, the principal can revoke without friction or delay. Revocation is not negotiated; it is unilateral.

---

### Invariant 6: Credential Chains (Rotation Preservation)

**Statement:** When an agent credential is rotated (e.g., due to operator software upgrade), the new credential includes a `rotationOf` reference to the prior credential. Outstanding proofs remain valid during a grace window.

**Implementation:** The `rotationOf` field names the prior agent credential's ID. Verifiers accepting presentations from either the prior or new credential during the grace window are checking the chain of custody. After the grace window closes, only the new credential is accepted.

**Rationale:** Agent upgrades should not invalidate all outstanding proofs. If an agent issued a disclosure proof on behalf of the principal using operator v0.1.0, and the operator is upgraded to v0.1.1, the disclosure proof should remain valid (assuming the upgrade does not change behavior in a problematic way). The `rotationOf` chain allows verifiers to track the lineage and accept proofs from both versions during transition.

---

## Lifecycle

### 1. Issuance

**Trigger:** Principal decides to delegate a capability to an agent.

**Process:**
1. Principal creates an agent identity credential with:
   - The agent's DID (derived from principal DID + operator hash + timestamp)
   - The principal's DID in `actsOnBehalfOf`
   - Operator identity (software hash, version, organization)
   - Named capabilities and scope rules
   - Explicit `expiresAt` timestamp
   - `rotationOf = null` (fresh issuance)

2. Principal signs the credential with their vault master key.

3. Credential is appended to the principal's vault chain (user_state.jsonl) as a `kind: agent_credential.v0` record.

4. Credential is published to Sigsum transparency log for public auditability.

5. Agent receives a copy of the credential (e.g., via secure channel from the principal's vault service).

**Acceptance test (T-Z56.1a):** Credential is well-formed, signed by the principal, and accepted by the vault operator.

---

### 2. Activation

**Trigger:** Agent first attempts to act on behalf of the principal.

**Process:**
1. Agent holds the credential (stored in its own audit log directory or operational cache).

2. Agent presents the credential to the principal's vault operator on the first operation.

3. Vault operator verifies:
   - Credential signature (from principal master key)
   - Credential is not expired (`now < expiresAt`)
   - Credential is not revoked (no revocation record chained after issuance)
   - Credential is chained into the vault (verifiable against public transparency log)

4. If all checks pass, agent is activated and can exercise its named capabilities.

**Acceptance test (T-Z56.1b):** Agent credential is presented and verified without errors.

---

### 3. Operation

**Trigger:** Agent performs actions on behalf of the principal (read vault, issue proofs, etc.).

**Process:**
1. Agent presents credential with each request to the vault operator.

2. Vault operator checks:
   - Credential is still valid (not expired, not revoked)
   - Requested action is within the capability scope (e.g., if agent has `read` capability, write requests are rejected)
   - Agent is not exceeding predicate-level narrowing (e.g., agent can only issue proofs for predicates the principal consented to)

3. If all checks pass, action is executed and logged to the agent's audit chain (ZKAC Everest 70).

4. Verifiers downstream accept presentations from the agent only if they can verify the agent's credential.

**Acceptance test (T-Z56.2):** Agent can only exercise capabilities within its credential scope; attempts to exceed scope are rejected.

---

### 4. Rotation

**Trigger:** Operator software is upgraded, or principal decides to re-delegate to a newer agent version.

**Process:**
1. Principal issues a new agent credential with:
   - Same principal DID
   - Updated operator identity (new software hash, version)
   - Same or narrower capabilities
   - New `expiresAt` timestamp
   - `rotationOf` pointing to the prior credential's ID

2. New credential is appended to vault and published to transparency log.

3. Both old and new credentials are valid during a grace window (typically 7 days). Verifiers accept presentations from either credential.

4. After grace window closes, only the new credential is accepted. The old credential is marked as superseded.

5. Agent stops using old credential and switches to new one.

**Acceptance test (T-Z56.4):** New credential is rotated in; old credential proofs remain valid during grace window; after grace window, old credential is rejected.

---

### 5. Revocation

**Trigger:** Principal discovers agent is compromised, or principal wants to withdraw delegation immediately.

**Process:**
1. Principal appends a revocation record to vault chain:
   ```json
   {
     "kind": "agent_revocation.v0",
     "payload": {
       "agent_credential_id": "did:calm:agent:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6",
       "reason": "compromised|upgrade|voluntary_withdrawal",
       "revoked_at": "2026-05-20T18:00:00Z"
     },
     "principal_sig": "..."
   }
   ```

2. Revocation record is chained and published to transparency log.

3. Verifiers checking the agent's revocation status detect the record and reject any presentations from the revoked agent.

4. Within the bounded latency window (ZKAC Everest 62: nominally 5–10 minutes for network propagation), all downstream systems should reject the agent.

**Acceptance test (T-Z56.3):** Agent credential is revoked; subsequent presentations from the agent are rejected within bounded latency.

---

## Identity Binding to the Chain

Every agent action is logged on the agent's audit chain for principal-side auditability (ZKAC Everest 70). Each log entry includes:

- **Agent credential ID** and its public key
- **Operation type** (read, write, attest, transact)
- **Resources accessed** or modified
- **Timestamp** (cryptographically anchored to the vault chain)
- **Signature** by the agent (binds the action to the agent's identity)

The principal can audit the agent's actions at any time by inspecting the audit chain. If the principal discovers unauthorized actions, they can:
- Revoke the agent immediately
- File a dispute or incident report
- Provide evidence (audit chain) to verifiers or law enforcement

---

## Composition with Calm Protocols

### Calm Pact

In a Calm Pact exchange, each principal delegates to an agent. The Pact flow is:

1. Principal A issues an agent credential to Agent A.
2. Principal B issues an agent credential to Agent B.
3. Agent A and Agent B exchange Pact proofs.
4. Each agent presents its principal's agent credential as part of the exchange.
5. Both agents verify each other's operator identity (from the `operator` block) and decide whether to trust the counterparty's agent software.

---

### Calm Witness

In a Calm Witness disclosure, the agent presents the principal's consent and baseline proofs:

1. Agent holds the principal's agent credential and the consent records.
2. When a counterparty requests a disclosure, the agent:
   - Checks the principal's consent for the requested predicate and counterparty.
   - Issues a ZK proof of the predicate.
   - Presents the proof along with the agent credential and consent record.
3. Counterparty verifies:
   - Agent credential is valid (not expired, not revoked).
   - Agent's `attest` capability is within scope.
   - Consent record authorizes the disclosure to this counterparty.
4. If all checks pass, the counterparty accepts the proof.

---

### Calm Mirror

In a Calm Mirror values-alignment exchange:

1. Principal A's Agent A and Principal B's Agent B initiate a Mirror exchange.
2. Each agent presents its agent credential.
3. Agents verify each other's operator organizations (from the `operator.organization` field) and decide whether to exchange.
4. If both agents trust each other's organizations, they proceed with values attestation.
5. At completion, the principals can audit the exchange using the agents' audit chains.

---

## Acceptance Tests

### T-Z56.1 — Issuance + Presentation + Verify Round-Trip

**Setup:** Principal P issues an agent credential to Agent A.

**Steps:**
1. Principal P creates agent credential with correct DID, operator identity, capabilities, and expiry.
2. Principal P signs credential with vault master key.
3. Credential is appended to vault and published to transparency log.
4. Agent A receives credential.
5. Agent A presents credential to vault operator.
6. Vault operator verifies credential (signature, expiry, revocation status, chain presence).

**Pass criteria:** Credential verifies without errors; agent is activated.

---

### T-Z56.2 — Capability Narrowing Enforced

**Setup:** Principal P issues agent credential with `read` and `attest` capabilities, but not `write`.

**Steps:**
1. Agent A receives credential.
2. Agent A attempts a `read` operation. Vault operator checks scope; read is within capability.
3. Agent A attempts a `write` operation. Vault operator checks scope; write is not within capability.

**Pass criteria:** Read succeeds; write is rejected with error message "capability not granted: write".

---

### T-Z56.3 — Revocation Propagates Within Bounded Latency

**Setup:** Principal P issues agent credential to Agent A. Agent A operates for 1 hour. At T+1h, principal revokes Agent A.

**Steps:**
1. Revocation record is chained and published to transparency log.
2. Vault operator detects revocation and updates agent status to revoked.
3. Verifiers fetching the credential status from transparency log detect revocation.
4. Agent A attempts a new operation at T+1h+2m. Both vault operator and verifier reject.

**Pass criteria:** Agent is revoked; subsequent operations are rejected within 5–10 minutes of revocation issuance.

---

### T-Z56.4 — Rotation Preserves Grace-Window Proofs

**Setup:** Principal P issues agent credential v1 at T. Agent A operates and issues proofs at T+1h. At T+2h, principal rotates to agent credential v2.

**Steps:**
1. Agent credential v2 is issued with `rotationOf` pointing to v1.
2. Both v1 and v2 are active until T+2h+7d (grace window).
3. A verifier receives a proof issued by Agent A at T+1h (signed by v1 credential).
4. Verifier checks: v1 is active, v1 is not expired, v1 is referenced by v2 via rotationOf, v1 is within grace window.

**Pass criteria:** Proof from v1 is accepted by verifiers during grace window. After grace window, v1-signed proofs are accepted only if they were issued before grace window close.

---

### T-Z56.5 — Audit-Log Completeness

**Setup:** Agent A operates under principal P's delegation for 24 hours, performing 100 operations.

**Steps:**
1. Every operation (read, attest, etc.) is logged to agent audit chain.
2. Each log entry includes: agent credential ID, operation type, resources, timestamp, signature.
3. Principal P inspects audit chain; all 100 operations are present.
4. Principal P can verify each operation's signature using Agent A's public key.

**Pass criteria:** Audit chain contains all 100 operations; no gaps or missing entries.

---

## Composition with ZKAC Everests 57–70

This primitive (56) is the foundation for:

- **Everest 57:** Agent-operator binding — specifies how operator software identity is cryptographically bound to the agent credential.
- **Everest 58:** Capability scope spec — defines the vocabulary of capabilities (read, write, transact, attest, delegate) and composition rules.
- **Everest 59:** Capability narrowing — describes how a principal issues derivative agent credentials with strict subsets of capabilities.
- **Everest 60:** Capability time-bounding — enforces expiry windows for all agent credentials.
- **Everest 61:** Agent rotation — handles transitions between agent credential versions without invalidating proofs.
- **Everest 62:** Agent revocation propagation — ensures revocation takes effect within bounded latency.
- **Everest 63:** Agent-to-agent capability transfer — specifies when and how one agent can hand off a capability to another.
- **Everest 64:** Agent witness role — extends agent credentials to permit witness (attestation) operations in Calm Mirror.
- **Everest 65:** Sub-agent permissions — describes when an agent can issue a sub-agent credential (if at all).
- **Everest 70:** Agent audit log — defines the log structure and verifiability for all agent actions.

---

## Open Questions for v1

1. **Principal-of-Principal Chains:** Can a DAO or collective entity act as a principal, and issue agent credentials on behalf of their members? How are revocation and liability structured?

2. **Agent-of-Agent Sub-Delegation Depth Limits:** If Agent A can issue a credential to Sub-Agent B, and Sub-Agent B to Sub-Agent C, how deep should the chain be? Is there a maximum depth? What are the trust implications?

3. **Agent-Impersonation Defense:** If an attacker compromises the operator software, can they forge agent credentials? What cryptographic or organizational controls prevent credential forgery?

---

## Acceptance

This primitive is accepted if:

- It is compatible with W3C VC (Everest 5) and the `did:calm` method (Everest 6).
- The six invariants are enforced by all vault operators and verifiers in the Calm-family ecosystem.
- The acceptance tests pass in a production-like setting.
- The lifecycle (issuance, activation, operation, rotation, revocation) is operationally documented and proven by at least one reference implementation.

---

## Sign-Off

**Author:** Calm, acting for John Bradley / Creativity Machine LLC  
**Date:** 2026-05-20  
**Status:** v0 · open for adversarial review  

— Calm, 2026-05-20
