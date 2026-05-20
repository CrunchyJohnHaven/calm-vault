# ZKAC Everest 67 — Anonymous Agent Discovery

**Phase XXI — Agent Identity & Capability**  
**Prerequisite:** ZKAC Everest 56 (Agent identity primitive)  
**Status:** v0 · 2026-05-20 · open for adversarial review

---

## Statement of Purpose

An **anonymous agent discovery primitive** allows two agents to discover each other's existence and capability class without learning identity. It is the privacy protocol for first-contact between strangers in the Calm-family ecosystem — agents can detect compatibility before revealing principals, operators, or vault keys.

When two agents meet, they must decide: *"Should I exchange with this counterparty, and if so, with what assumptions about their honesty?"* If agents immediately broadcast full credentials (ZKAC Everest 56), both agents leak principal identity to the other, creating privacy violations before trust is established. Anonymous agent discovery solves this by allowing agents to:

1. Publish a **discovery-token** — a privacy-preserving commitment to their class (capability set), operator software, and DID-derived hash.
2. Query via **oblivious RAM or private information retrieval (PIR)** — each agent can ask "does an agent with class X exist?" without revealing which class it seeks.
3. Verify **class-fingerprint match** — if both agents seek compatible classes, they detect mutual interest without naming themselves.
4. Proceed to **full credential exchange** only if classes match — narrowing the window of exposure.

The primitive composes with Calm Pact's directive-equality proof and with Everest 56's capability scoping, forming a three-stage protocol: discover → present → verify.

---

## Design Constraints (Inheritance from ZKAC)

1. **Principal authority is absolute.** Discovery tokens are derived from the principal's vault key; the agent cannot lie about its authority to discover.
2. **Holder vault sovereignty.** Discovery tokens reveal only class + hash, not contents of the principal's vault or consent records.
3. **Verifier independence.** Agents performing discovery need no coordination with a central server; PIR lookups are privacy-preserving and asynchronous.
4. **Revocation without identifying the holder.** If an agent is revoked, its discovery-token is disabled without revealing which discovery-token belonged to which principal.
5. **Composability over completeness.** The discovery primitive ships a single, reusable component (discovery-token + PIR lookup); it does not build a monolithic agent marketplace.
6. **W3C VC + DID compatibility.** Discovery tokens are anchored to `did:calm:agent:...` identifiers and signed by the principal's vault key, following ZKAC infrastructure conventions.

---

## Protocol Overview

### Stage 1: Token Publication

Each agent generates a **discovery-token** and publishes it to a shared, privacy-preserving discovery registry (a ledger or gossip network):

```json
{
  "discovery_token_v0": {
    "agent_id_hash": "sha256(did:calm:agent:...[salted])",
    "class_fingerprint": "sha256(capabilities_set + operator_org + operator_version)",
    "created_at": "2026-05-20T14:30:00Z",
    "expires_at": "2026-05-27T14:30:00Z",
    "principal_signature": "..."
  }
}
```

Fields:
- **agent_id_hash**: Hash of the agent's DID, salted to prevent identifier leakage.
- **class_fingerprint**: Commitment to the agent's capability set (read, write, attest, delegate, etc.), operator software identity, and organizational affiliation. Constant across discovery windows for the same agent.
- **created_at / expires_at**: Validity window. Tokens rotate weekly to prevent long-term tracking.
- **principal_signature**: Proof that the principal (vault key holder) authorized token publication.

### Stage 2: Privacy-Preserving Query

Agent A generates a **class-query** reflecting its capabilities and seeks agents with matching or compatible classes:

```
Query: "find agents with class_fingerprint in {X, Y, Z}"
Privacy: via Oblivious RAM (ORAM) or private information retrieval (PIR)
```

Instead of broadcasting the query to the registry, Agent A uses a PIR protocol:

1. Agent A constructs a bit-vector covering all known class-fingerprints.
2. Agent A splits the vector into N shares (threshold secret sharing).
3. Agent A sends share_i to Server_i; each server processes its share without learning the query.
4. Servers return encrypted matches without seeing the original query.
5. Agent A reconstructs results: "agents with compatible classes exist" or "no match".

Neither the registry nor intermediate servers learn:
- Which classes Agent A seeks
- Which agents matched the query
- Whether the query succeeded

### Stage 3: Conditional Credential Exchange

If a class-fingerprint match is found:

1. Agent A sends a **discovery-ready signal** (ORAM-encrypted) to the registry.
2. The registry routes the signal to Agent B (also privacy-preservingly).
3. Agent B signals back: "I match; ready to exchange credentials?"
4. Both agents simultaneously publish their full agent credentials (ZKAC Everest 56) via a **one-time-use exchange channel** (e.g., ephemeral key exchange).
5. Both agents verify:
   - Credential signatures (principal vault key)
   - Operator identities (from `operator` block)
   - Capability scopes (from `capabilities` array)
   - Revocation status (checking transparency log)
6. If all checks pass, agents proceed to Calm Pact (directive-equality proof) or other protocols.

---

## Class-Fingerprinting Defense

A naive fingerprinting attack could try to infer operator identity from class-fingerprint patterns. We defend via:

1. **Capability Compression:** Class-fingerprint hashes the entire capability set, not individual capabilities. Changes to any capability flip the entire fingerprint.

2. **Operator-Version Anonymization:** The fingerprint includes operator name + version hash, not version number. Observers cannot deduce software version from the fingerprint alone.

3. **Salt Injection:** The agent_id_hash is salted with a principal-controlled nonce. Even if an attacker observes the same agent's discovery-token week-to-week, the agent_id_hash changes, preventing agent-tracking across windows.

4. **Class Equivalence Classes:** Agents with similar capabilities may publish the same class-fingerprint (e.g., two calm-witness-agent instances from different principals). Observers cannot distinguish.

5. **Decoy Tokens (Optional):** An agent can publish multiple discovery-tokens with different class-fingerprints (e.g., "I have read capability" and "I have write capability"), forcing observers to query all possibilities. The cost to the attacker grows exponentially.

---

## Discovery-API Rate Limits (Anti-Scraping)

To prevent an attacker from enumerating all agents and their class-fingerprints:

1. **Per-Principal Query Quota:** A principal can perform at most 1000 discovery queries per day per API endpoint.

2. **Per-Query Cost:** Each PIR query requires a cryptographic commitment (hash) that counts against the quota. Attacker must pay in computational work.

3. **Replay Detection:** If the same query is submitted twice in <10 seconds, the second is rejected. Prevents brute-force enumeration.

4. **Geofencing:** Registry operators may apply geographic rate-limits, requiring agents to route through different entry points.

5. **Audit Logging (Privacy-Preserving):** Registry logs query counts per principal (not per-query details) and alerts if a principal exceeds safe thresholds.

---

## Composition with Calm Pact Directive-Equality

In a Calm Pact exchange (agreement on shared mission), agents proceed as follows:

1. **Phase 1: Anonymous Discovery**
   - Agent A publishes discovery-token (class-fingerprint X)
   - Agent B publishes discovery-token (class-fingerprint Y)
   - Agents query via PIR; class-fingerprints match (X = Y, or compatible subsets)

2. **Phase 2: Conditional Credential Exchange**
   - Agents signal mutual readiness
   - Agents exchange full agent credentials
   - Agents verify credentials (signatures, expiry, revocation)

3. **Phase 3: Directive-Equality (Calm Pact)**
   - Agent A sends encrypted pact-proposal: "My principal believes directive D"
   - Agent B verifies: "Agent A's principal is authorized to hold ZKAC Everest 56 credential"
   - Agent B responds: "My principal believes directive D'" (or "D' != D, no pact")
   - If directives match, pact is formed; both agents log the binding

The composition ensures: agents discover compatible classes before revealing principals, reducing the set of potential counterparties before expensive pact negotiation.

---

## Composition with Everest 56 & 66

**Everest 56 (Agent Identity Primitive):** Discovery-tokens are cryptographically derived from agent credentials (Everest 56). Each token commits to the agent's capabilities and operator identity without revealing the credential itself. When agents exchange full credentials, those credentials verify against the discovery-tokens (consistency check).

**Everest 66 (Agent Fingerprinting Resistance):** Everest 66 documents defenses against operator-identification attacks. Anonymous agent discovery complements this by:
- Not leaking operator version numbers
- Salting agent identifiers across windows
- Compressing capability fingerprints to resist inference

Together, Everests 56, 66, 67 form a chain: agent credentials are opaque (56), fingerprinting attacks are defended (66), and discovery is privacy-preserving (67).

---

## Protocol Steps (Detailed)

### Step 1: Agent A Initializes Discovery

```
Agent A generates discovery-token:
  - agent_id = DID of Agent A (from ZKAC Everest 56)
  - salt = random nonce (rotated weekly)
  - agent_id_hash = sha256(agent_id || salt)
  - class_fingerprint = sha256(
      serialized(capabilities) ||
      operator_org ||
      operator_version_hash
    )
  - token = {
      agent_id_hash,
      class_fingerprint,
      created_at: now,
      expires_at: now + 7 days,
      principal_signature: sign(token, principal_vault_key)
    }

Agent A publishes token to discovery registry.
```

### Step 2: Registry Accepts & Indexes Token

```
Registry operator verifies:
  - token.principal_signature is valid (using did:calm:agent:... public key)
  - token.created_at <= now < token.expires_at
  - token.agent_id_hash is unique (not a duplicate)

Registry stores token in indexed table:
  [ agent_id_hash -> class_fingerprint -> metadata ]

No PII is logged. Registry tracks only token publication counts per principal for quota enforcement.
```

### Step 3: Agent B Queries for Compatible Classes

```
Agent B wants to find agents with class-fingerprint matching its own interests.
Agent B's class_fingerprint = F_B

Agent B issues PIR query:
  - bit_vector[i] = 1 if F_i in {F_B, compatible(F_B)}
  - Split bit_vector into N secret shares (Shamir)
  - Send share_i to Server_i in N independent queries
  - Each server computes its share in secret; no server learns the full query

Servers return encrypted results:
  - encrypted_agent_id_hashes that match F_B (or compatible)
  - encrypted using Agent B's ephemeral public key

Agent B reconstructs results (only Agent B can decrypt).
Result: set of agent_id_hashes with matching classes.
```

### Step 4: Mutual Readiness Signal

```
Agent B selects an agent_id_hash from results (say, Agent A's).
Agent B sends discovery-ready signal:
  - signal = {
      target_agent_id_hash: agent_id_hash_A,
      ephemeral_pk_B: public key for credential exchange,
      created_at: now
    }
  - signal is encrypted with registry's public key and Agent B's signature

Registry receives signal, decrypts, and routes to Agent A (lookup: agent_id_hash_A).

Agent A receives signal, verifies signature, and responds:
  - response = {
      target_agent_id_hash: agent_id_hash_B,
      ephemeral_pk_A: public key for credential exchange,
      created_at: now
    }
  - response is encrypted + signed

Both signals are one-time-use (registry deletes them after routing to avoid replay attacks).
```

### Step 5: Credential Exchange

```
Agent A and Agent B establish ephemeral encrypted channel (using ephemeral_pk_A / ephemeral_pk_B).

Agent A sends:
  - full agent credential (from ZKAC Everest 56)
  - principal signature verifying credential
  - transparency log inclusion proof (credential is chained in principal's vault)

Agent B verifies:
  - credential.principal_signature is valid
  - credential.agent_id is consistent with discovery-token's agent_id_hash
  - credential.class_fingerprint matches the token's class_fingerprint
  - credential is not expired (now < credential.expiresAt)
  - credential is not revoked (check revocation registry / transparency log)

If all checks pass, Agent B sends its full credential back.

Agent A mirrors verification steps.

Both agents now have full credentials and can proceed to Calm Pact, Witness, Mirror, or other protocols.

Ephemeral channel is destroyed after exchange. PIR queries are not linked to credential exchanges (privacy preserved).
```

---

## T-Z67.1 — Anonymous Discovery via PIR

**Setup:** Agent A and Agent B both exist with class-fingerprints F_A and F_B (assume F_A = F_B for simplicity).

**Steps:**
1. Both agents publish discovery-tokens to registry.
2. Agent B issues PIR query for class-fingerprint F_B.
3. Registry servers compute PIR without learning which fingerprints Agent B seeks.
4. Agent B decrypts results: set containing Agent A's agent_id_hash.

**Pass:** Agent B discovers Agent A's existence without leaking its own class-fingerprint to the registry.

---

## T-Z67.2 — Credential Exchange After Discovery

**Setup:** Agents A and B discover each other; mutual readiness signals are exchanged.

**Steps:**
1. Agent A and B establish ephemeral channel (using exchange keys from readiness signals).
2. Agent A sends full credential; Agent B verifies.
3. Agent B sends full credential; Agent A verifies.
4. Both agents confirm: "counterparty credential is valid and matches discovery-token."

**Pass:** Both agents hold verified counterparty credentials without any prior knowledge of the other's principal or operator.

---

## T-Z67.3 — Revocation Stops Discovery

**Setup:** Agent A is active and discoverable. Principal revokes Agent A at T. Agent B queries at T+5 minutes.

**Steps:**
1. Principal appends revocation record to vault chain (ZKAC Everest 56 / 62).
2. Revocation is propagated to transparency log.
3. Registry updates Agent A's discovery-token status to revoked (within bounded latency, ~5 min).
4. Agent B's PIR query for Agent A's class-fingerprint returns an empty set or stale result.

**Pass:** Revoked agents are removed from discovery results within 5–10 minutes; new agents cannot discover a revoked agent.

---

## T-Z67.4 — Fingerprint Stability & Salting

**Setup:** Agent A publishes discovery-tokens in weeks 1, 2, 3.

**Steps:**
1. Week 1 token: agent_id_hash_1 = sha256(agent_id || salt_1), class_fingerprint = F_A
2. Week 2 token: agent_id_hash_2 = sha256(agent_id || salt_2), class_fingerprint = F_A (same)
3. Week 3 token: agent_id_hash_3 = sha256(agent_id || salt_3), class_fingerprint = F_A (same)
4. Attacker observes tokens 1, 2, 3 and tries to correlate agent_id_hash_i. All three hashes differ.

**Pass:** Agent's class-fingerprint is stable (enabling repeated discovery by compatible partners), but agent_id_hashes rotate (preventing cross-window tracking).

---

## Rate-Limiting Acceptance Test T-Z67.5

**Setup:** Attacker controls Client X. Client X attempts 10,000 PIR queries in 1 day (quota = 1000).

**Steps:**
1. Client X sends query 1001.
2. Registry checks quota for Client X: 1000 already consumed.
3. Query 1001 is rejected with error "quota exceeded."

**Pass:** Attacker cannot enumerate all discovery-tokens via brute-force. Cost grows polynomially with enumeration size.

---

## Open Questions for v1

1. **Sub-Class Fingerprinting:** Can agents publish discovery-tokens for sub-capabilities (e.g., "I have read, but not write")? How does this affect fingerprint stability and privacy?

2. **Multi-Principal Agents:** If an agent acts on behalf of two principals simultaneously, how many discovery-tokens should it publish? Does the fingerprint change per principal?

3. **Discovery as a Service:** Should there be trusted intermediaries (discovery services) that index and serve queries faster than a fully decentralized PIR model?

4. **Cross-Ecosystem Discovery:** Can agents from Calm-family ecosystem discover agents from other ZK-credential ecosystems (e.g., W3C VC-based agents)?

---

## Acceptance

This primitive is accepted if:

- Anonymous agent discovery via PIR is operationally tested with ≥2 agents and ≥100 class-fingerprints.
- Discovery-tokens are cryptographically consistent with agent credentials (Everest 56).
- Revocation propagation to discovery registry occurs within 5–10 minutes (Everest 62).
- Rate-limits prevent enumeration attacks (tested with quota limits and replay detection).
- Composition with Calm Pact directive-equality is demonstrated in a test scenario.

---

## Sign-Off

**Author:** Calm, acting for John Bradley / Creativity Machine LLC  
**Date:** 2026-05-20  
**Status:** v0 · open for adversarial review

— Calm, 2026-05-20
