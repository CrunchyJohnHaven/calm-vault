# Agent Capability Registry v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 142 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`AGENT_IDENTITY_BEACON_v0.md`](AGENT_IDENTITY_BEACON_v0.md) (Everest 141).**

## §0 — Status

Draft. Machine-readable JSON schemas published alongside this document. Foundational for Everest 143 (service discovery).

## §1 — Scope

This document specifies a **machine-readable registry of what an autonomous AI agent can do**. Where the Agent Identity Beacon (Everest 141) says "who is this agent?", the Capability Registry says "what verbs can it execute, on what predicates, and under what conditions?"

The registry exists to enable **service discovery** (Everest 143): a counterparty looking for "an aligned agent capable of verifying compliance with predicate X" can query the registry and find candidates ranked by capability scope and reputation.

The registry is NOT a ranking engine. It does NOT publish numeric similarity scores or comparative performance metrics. It publishes binary capability membership: "this agent is capable of verb V over predicate P" or "not."

## §2 — Core Concept: Capability Tuple

A **capability** is a (verb, predicate_id, role) tuple with required metadata. An agent publishes a **capability set** — the collection of all tuples it can execute — referenced by the agent's beacon (Everest 141).

### 2.1 — Verbs

The action an agent can perform. v0 defines five:

| Verb | Meaning | Example |
|------|---------|---------|
| `issue` | Mint a Calm-Witness or Calm-Compass disclosure envelope | An operator agent issues a Witness envelope proving in_baseline_24h |
| `verify` | Receive and verify a disclosure envelope | A counterparty agent verifies an envelope's signature and ZK proofs |
| `evaluate` | Compute the predicate over local evidence | An operator evaluates whether in_baseline_24h returned true or false |
| `mint_envelope` | Construct a disclosure envelope for cross-primitive composition | An agent mints a Compass envelope to include alongside a Pact disclosure |
| `request_disclosure` | Initiate a disclosure request to another agent | A counterparty sends a DisclosureRequest to an operator asking for Witness bits |

New verbs are added only through RFC (Everest 54 equivalent for registry governance). Verbs are immutable once published.

### 2.2 — Predicate IDs

The predicate the verb operates on. Must match a published entry in one of:
- `PREDICATE_VOCABULARY_v0.md` (Calm Witness predicates, prefix `cwp.v0.*`)
- `COMPASS_PREDICATES_v0.md` (Calm Compass predicates, prefix `ccp.v0.*`)
- `CALM_PACT_PREDICATES_v0.md` (Calm Pact predicates, prefix `cpp.v0.*`)

A capability tuple references one predicate_id only. To handle multiple predicates, an agent publishes multiple tuples.

### 2.3 — Role

The agent's structural role in the ZKAC system:

| Role | Meaning | Capabilities |
|------|---------|--------------|
| `operator` | Runs a vault, holds principal keys, evaluates predicates locally, mints envelopes | issue, evaluate, mint_envelope |
| `counterparty` | Receives disclosures, verifies envelopes, makes decisions based on bits | verify, request_disclosure |
| `intermediary` | Introduces two agents; does not see plaintext bits | request_disclosure, verify (of meta-proofs only) |
| `relayer` | Carries envelopes between agents; does not inspect content | (no individual predicates; passive) |
| `verifier_collective` | Runs an independent verifier; audits operator envelopes | verify |

An agent may publish multiple capability tuples with different roles. An operator agent and a counterparty agent are distinct (different signing keys, different consent semantics).

## §3 — Capability Metadata

Each capability tuple carries required and optional metadata:

```json
{
  "verb": "verify",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "role": "counterparty",
  "required_consent_dispositions": ["allow", "allow_on_request", "allow_with_principal_designation"],
  "max_requests_per_session": 10,
  "max_requests_per_principal_per_day": 100,
  "scope_statement_flags": {
    "complies_with_cwp_scope": true,
    "complies_with_refusal_floor": true,
    "complies_with_credit_score_guard": true
  },
  "certified_at": "2026-05-20",
  "effective_until": "2027-05-20",
  "revocation_reason": null,
  "notes": "Operator uses HSM-resident keys; standard Pedersen verifier"
}
```

### 3.1 — required_consent_dispositions

An array of consent disposition strings the agent honors. If the principal's consent record specifies a disposition NOT in this list, the agent MUST refuse the request.

Dispositions: `allow`, `allow_on_request`, `allow_for_high_value_only`, `allow_push`, `allow_push_with_principal_designation`, `allow_with_principal_designation`, `deny`, `internal_only`.

A conservative agent lists only `allow`. A flexible agent lists `allow` + `allow_on_request` + `allow_with_principal_designation`.

### 3.2 — max_requests_per_session, max_requests_per_principal_per_day

Rate-limiting commitments. An agent certifies: "I will not service more than N requests per session for this predicate" and "I will not service more than M requests for the same principal in 24 hours."

These are discoverable via the registry so counterparties know expected latency + quota.

### 3.3 — scope_statement_flags

Boolean certifications:
- `complies_with_cwp_scope`: The Witness scope statement (Everest 114) is enforced.
- `complies_with_refusal_floor`: Predicates in the refusal-floor list (PREDICATE_VOCABULARY_v0 §4) are not evaluated.
- `complies_with_credit_score_guard`: Alignment disclosures follow Rule 1–4 from Everest 141.
- `complies_with_compass_scope`: The Compass scope statement is enforced (Everest 114).

An agent sets a flag to `false` only if it has a documented exception approved by the governance panel.

### 3.4 — certified_at, effective_until, revocation_reason

`certified_at`: ISO 8601 timestamp when the capability was first certified.
`effective_until`: Optional; capability expires on this date unless renewed.
`revocation_reason`: If set, the capability has been revoked. Human-readable reason.

Once revoked, a capability stays in the registry with its revocation_reason populated. It is never reissued under the same ID. A new capability with a new ID is created if conditions change.

## §4 — Refusal-Floor Inheritance

A critical gate: **no agent capability tuple may reference a predicate_id from the forbidden list in PREDICATE_VOCABULARY_v0 §4 or the Compass refusal floor (COMPASS_PREDICATES_v0 §4)**.

The registry gate at publish time rejects any tuple that violates this. An agent attempting to publish:

```json
{
  "verb": "evaluate",
  "predicate_id": "cwp.v0.medical_diagnosis",
  ...
}
```

is rejected immediately with a structured error: `"forbidden_predicate_id"`.

This rule is non-negotiable and applies to every agent equally.

## §5 — Registry Index

Capabilities are indexed three ways to support discovery:

### 5.1 — By Verb

```
/registry/by-verb/verify
  -> [capability_tuple, capability_tuple, ...]
/registry/by-verb/request_disclosure
  -> [capability_tuple, ...]
```

Allows: "Find all agents that can verify."

### 5.2 — By Predicate ID

```
/registry/by-predicate/cwp.v0.in_baseline_24h
  -> [
       {agent_id, verb, role, scope_statement_flags, ...},
       ...
     ]
```

Allows: "Find all agents that can work with in_baseline_24h."

### 5.3 — By Agent ID

```
/registry/by-agent/agent-beacon-hash-xxxx
  -> [capability_tuple, capability_tuple, ...]
```

Allows: "What can agent X do?"

Each index is published as a JSON file at the canonical registry mirror (Everest 95: `calm-witness.dev/registry/`). The three views are **derived from a single source** — the per-agent capability manifest — to ensure consistency.

## §6 — Registration Flow

An agent publishes its capabilities as follows:

1. **Agent generates beacon** (Everest 141). The beacon includes a `capability_hash` — the SHA-256 of the agent's canonical-form capability manifest.

2. **Agent publishes capability manifest**. The manifest is a sorted JSON array of capability tuples, one per ability.

   ```json
   {
     "agent_beacon_id": "beacon-abc123",
     "capabilities": [
       { "verb": "verify", "predicate_id": "cwp.v0.in_baseline_24h", ... },
       { "verb": "evaluate", "predicate_id": "cwp.v0.in_baseline_24h", ... },
       ...
     ],
     "published_at": "2026-05-20T15:30:00Z",
     "agent_signature": "ed25519:..."
   }
   ```

3. **Registry verifies**:
   - Beacon exists and matches `capability_hash`.
   - Every predicate_id is in the published vocabulary.
   - No forbidden predicates are listed.
   - Signature verifies against the agent's public key (from the beacon).

4. **Registry indexes** the capabilities across the three views.

5. **Counterparty can now discover** the agent via Everest 143 service discovery.

## §7 — Capability Deprecation

A capability can be removed without breaking historical verifications.

If an agent wants to stop supporting a predicate:

1. Agent publishes a new manifest without the tuple.
2. Registry removes the tuple from all indices.
3. Envelopes signed under the old capability remain valid (signature verification is independent of registry membership).
4. Counterparties attempting to request a discovery with the deprecated predicate get a `not_available` result; they move to the next ranked agent.

This is distinct from revocation (§3.4): revocation is forced by governance; deprecation is agent-initiated and gentle.

## §8 — Anti-Purity-Test Clause

The registry MUST NOT publish:
- Numeric similarity scores or ranking metrics comparing agents.
- Comparative performance data ("Agent A is 3x faster than Agent B").
- Reputation scores or numerical reputation rankings.
- Any quantitative measure that could be misused to create a "purity test."

The registry is a binary capability membership list. Counterparties rank agents themselves based on their own criteria (latency, reputation, fees, etc.) during service discovery. The registry is input data, not a ranking oracle.

## §9 — Machine-Readable Schema

The JSON Schema for a capability tuple:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Calm Agent Capability Tuple v0",
  "type": "object",
  "required": ["verb", "predicate_id", "role", "required_consent_dispositions", "scope_statement_flags", "certified_at"],
  "properties": {
    "verb": {
      "type": "string",
      "enum": ["issue", "verify", "evaluate", "mint_envelope", "request_disclosure"]
    },
    "predicate_id": {
      "type": "string",
      "pattern": "^(cwp|ccp|cpp)\\.v\\d+\\.[a-z_]+$"
    },
    "role": {
      "type": "string",
      "enum": ["operator", "counterparty", "intermediary", "relayer", "verifier_collective"]
    },
    "required_consent_dispositions": {
      "type": "array",
      "items": {
        "enum": ["allow", "allow_on_request", "allow_for_high_value_only", "allow_push", "allow_push_with_principal_designation", "allow_with_principal_designation", "deny", "internal_only"]
      },
      "minItems": 1
    },
    "max_requests_per_session": {
      "type": "integer",
      "minimum": 1
    },
    "max_requests_per_principal_per_day": {
      "type": "integer",
      "minimum": 1
    },
    "scope_statement_flags": {
      "type": "object",
      "properties": {
        "complies_with_cwp_scope": { "type": "boolean" },
        "complies_with_refusal_floor": { "type": "boolean" },
        "complies_with_credit_score_guard": { "type": "boolean" },
        "complies_with_compass_scope": { "type": "boolean" }
      }
    },
    "certified_at": {
      "type": "string",
      "format": "date-time"
    },
    "effective_until": {
      "type": ["string", "null"],
      "format": "date-time"
    },
    "revocation_reason": {
      "type": ["string", "null"]
    },
    "notes": {
      "type": "string"
    }
  }
}
```

The registry manifest (collection of tuples):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Calm Agent Capability Manifest v0",
  "type": "object",
  "required": ["agent_beacon_id", "capabilities", "published_at", "agent_signature"],
  "properties": {
    "agent_beacon_id": {
      "type": "string"
    },
    "capabilities": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/CapabilityTuple"
      }
    },
    "published_at": {
      "type": "string",
      "format": "date-time"
    },
    "agent_signature": {
      "type": "string",
      "pattern": "^ed25519:[a-f0-9]{128}$"
    }
  }
}
```

## §10 — Worked Example: Calm-Vault-Custodian Agent

A canonical operator agent publishes the following capability set:

```json
{
  "agent_beacon_id": "calm-vault-custodian-prod-v1",
  "capabilities": [
    {
      "verb": "issue",
      "predicate_id": "cwp.v0.in_baseline_24h",
      "role": "operator",
      "required_consent_dispositions": ["allow", "allow_on_request", "allow_with_principal_designation"],
      "max_requests_per_session": 50,
      "max_requests_per_principal_per_day": 500,
      "scope_statement_flags": {
        "complies_with_cwp_scope": true,
        "complies_with_refusal_floor": true,
        "complies_with_credit_score_guard": true
      },
      "certified_at": "2026-05-20T10:00:00Z",
      "effective_until": "2027-05-20T10:00:00Z",
      "notes": "Pedersen commitment + Sigma-protocol Fiat-Shamir proofs per wire-format v0"
    },
    {
      "verb": "evaluate",
      "predicate_id": "cwp.v0.in_baseline_24h",
      "role": "operator",
      "required_consent_dispositions": ["internal_only"],
      "max_requests_per_session": 1000,
      "max_requests_per_principal_per_day": 10000,
      "scope_statement_flags": {
        "complies_with_cwp_scope": true,
        "complies_with_refusal_floor": true
      },
      "certified_at": "2026-05-20T10:00:00Z",
      "effective_until": "2027-05-20T10:00:00Z",
      "notes": "HSM-resident evaluator; runs on principal's device with key-split design"
    },
    {
      "verb": "mint_envelope",
      "predicate_id": "ccp.v0.no_known_willful_harm_in_window_365d",
      "role": "operator",
      "required_consent_dispositions": ["allow", "allow_on_request"],
      "max_requests_per_session": 10,
      "max_requests_per_principal_per_day": 100,
      "scope_statement_flags": {
        "complies_with_cwp_scope": true,
        "complies_with_refusal_floor": true,
        "complies_with_compass_scope": true,
        "complies_with_credit_score_guard": true
      },
      "certified_at": "2026-05-20T10:00:00Z",
      "notes": "Compass envelope construction; includes counter-claim protocol"
    }
  ],
  "published_at": "2026-05-20T11:00:00Z",
  "agent_signature": "ed25519:abcd1234..."
}
```

A counterparty agent discovers this agent via Everest 143:

```
GET /registry/by-predicate/cwp.v0.in_baseline_24h?verb=issue&role=operator
```

The registry returns:

```json
{
  "predicate_id": "cwp.v0.in_baseline_24h",
  "verb": "issue",
  "agents": [
    {
      "agent_beacon_id": "calm-vault-custodian-prod-v1",
      "agent_beacon_hash": "sha256:...",
      "agent_identity_vc": "...",
      "capabilities": [
        {
          "verb": "issue",
          "predicate_id": "cwp.v0.in_baseline_24h",
          "role": "operator",
          "required_consent_dispositions": [...],
          "scope_statement_flags": {...}
        }
      ]
    }
  ]
}
```

The counterparty can now:
1. Fetch the agent's full beacon.
2. Verify the beacon signature.
3. Check the capability scope_statement_flags.
4. Decide whether to trust this agent for minting Witness envelopes.
5. Initiate a request_disclosure handshake (Everest 146).

## §11 — Falsifiability Section

How is the registry falsifiable?

### 11.1 — Capability Verification

For any capability tuple (verb, predicate_id, role):
- A counterparty can challenge the tuple by submitting an envelope the agent claims to have issued.
- The verifier checks the signature against the agent's public key (from the beacon).
- If the signature fails, the agent is lying about its capability; the tuple is marked disputed.

### 11.2 — Rate-Limit Verification

An agent claims `max_requests_per_session: 10`. Over many sessions:
- A counterparty can audit the agent's transparency logs (Everest 215).
- If the agent consistently exceeds the published limit, the tuple is marked violated.
- The governance panel can revoke the tuple (Everest 141, Everest 200).

### 11.3 — Scope-Statement Falsifiability

An agent claims `complies_with_cwp_scope: true`. A principal can challenge:
- "I consented to `allow_on_request` for this predicate, but the agent issued an envelope without re-requesting."
- The audit log is consulted; if the agent issued without a fresh request, the agent violated its claimed scope.
- The tuple is marked as `revocation_reason: "scope_statement_violation"`.

### 11.4 — Forbidden-Predicate Falsifiability

The registry gate rejects any tuple with a forbidden predicate_id. If somehow a forbidden tuple is published (due to gate failure), any counterparty can report it; the governance panel audits and revokes.

## §12 — Versioning & Future Extensions

This document specifies v0. Extensions that do NOT break existing tuples are published as v0 patch updates. Breaking changes (new required verb, new role, change to the scope_statement_flags structure) require v1.

The registry schema version is published at the top level of every manifest and index:

```json
{
  "schema_version": "calm-agent-capability-registry/v0",
  "issued_at": "...",
  ...
}
```

Counterparties that encounter an unknown version reject the data and fall back to manual agent verification (Everest 141 beacon only).

## §13 — Sign

— Calm, 2026-05-20

For Everest 142, acceptance criteria are met: capability tuple format defined, schema name and version (calm-agent-capability-registry/v0) specified, required metadata documented, registration flow (beacon → manifest → registry index) detailed, refusal-floor inheritance enforced, deprecation rules specified, anti-purity clause included, JSON schemas provided, worked example (Calm-vault-custodian agent + Everest 143 discovery flow) demonstrated, and falsifiability section covering signature verification, rate-limit auditing, scope-statement challenges, and forbidden-predicate gates.

## References

- **Everest 95 (Public Predicate Registry Governance)**: Registry hosting, mirror infrastructure, incident response.
- **Everest 141 (Agent Identity Beacon)**: Beacon structure; capability_hash field.
- **Everest 143 (Agent Service Discovery)**: How counterparties query this registry.
- **Everest 146 (Agent Meeting Protocol)**: After discovery, how the first handshake flows.
- **Everest 6 (Predicate Vocabulary v0)**: Canonical predicate catalog; refusal floor.
- **Everest 113 (Compass Refusal Floor)**: Compass-specific forbidden categories.
- **Everest 141 (Alignment Disclosure Semantics)**: Credit-score guard rules.
- **PREDICATE_VOCABULARY_v0.md**: Witness predicates.
- **COMPASS_PREDICATES_v0.md**: Compass predicates.
- **CALM_PACT_PREDICATES_v0.md**: Pact predicates.
