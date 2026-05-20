# ZKAC Everest 58 — Capability Scope Spec

**Phase XXI — Agent Identity & Capability**  
**Prerequisite:** ZKAC Everest 56 (Agent identity primitive)  
**Status:** v0 · 2026-05-20 · open for adversarial review

---

## Statement of Purpose

A capability is the unit of authority an agent presents when acting on a principal's behalf. This spec defines a vocabulary v0 of six capability classes — `read`, `write`, `transact`, `attest`, `delegate`, `disclose` — with explicit schema, authorization requirements, scope restrictions, and composition rules. Capabilities form a partially-ordered lattice where narrowing is monotone: delegation can only reduce scope, never expand it.

---

## Capability Vocabulary v0

### Capability 1: Read

**Purpose:** Observe vault state; request credential disclosures without mutation.

**Schema:**

```json
{
  "name": "read",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature"
  },
  "default_scope": {
    "resources": [],
    "operations": ["inspect", "query", "query_predicate", "discover"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": ["mutate", "delete", "sign"]
  },
  "composition_rules": [
    "read_only: no write or transact capability can coexist with read in the same credential",
    "monotone_narrowing: derivative agent credentials can restrict resources or operations but never expand",
    "predicate_scoping: principal can constrain reads to specific predicates already in consent records"
  ],
  "sub_scoping": [
    "read.resources_max: list of vault paths or credential types the agent can inspect",
    "read.operations_subset: subset of {inspect, query, query_predicate, discover}",
    "read.consent_required: if true, agent can only read resources where principal has explicit consent"
  ],
  "revocation": {
    "propagation_latency_ms": 300000,
    "effect": "immediate: no further reads after revocation"
  },
  "audit": {
    "logged": true,
    "log_includes": ["resource_path", "operation_type", "timestamp", "agent_signature"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key.

**Default Scope Restrictions:**
- Agent can inspect vault state, query records, match predicates, discover capabilities.
- Agent cannot mutate, delete, or sign on behalf of principal.
- Reads are constrained to resources explicitly listed or covered by default consent.

**Composition Rules:**
- `read` is incompatible with `write` or `transact` in a single credential; principal must issue separate credentials if broader access is needed.
- Narrowing monotone: derivative credentials can restrict which resources or operations are readable, but cannot expand.
- Principal can sub-scope to specific predicates or consent records.

**Time-Bounding:** Mandatory `expires_at` in ISO 8601 format. No read capability outlives its issuance without renewal.

---

### Capability 2: Write

**Purpose:** Append self-reports to principal's chain; never witness-signing.

**Schema:**

```json
{
  "name": "write",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature"
  },
  "default_scope": {
    "resources": [],
    "operations": ["append_self_report", "append_audit_log"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": ["read_without_consent", "sign_as_principal", "attest", "transact"]
  },
  "composition_rules": [
    "append_only: write means append, never mutate or delete existing records",
    "self_report_only: written records are agent-authored (signed by agent), never principal-authored",
    "no_principal_key_access: agent never holds principal master key; cannot sign as principal",
    "monotone_narrowing: derivative credentials can restrict record types but not expand"
  ],
  "sub_scoping": [
    "write.record_types: subset of {self_report, audit_log, activity_trace}",
    "write.max_records_per_window: rate limit on appends (e.g., 1000/day)",
    "write.tagging_required: agent-written records must include agent_id, timestamp, purpose tag"
  ],
  "revocation": {
    "propagation_latency_ms": 300000,
    "effect": "immediate: no further writes after revocation; prior writes remain on chain immutably"
  },
  "audit": {
    "logged": true,
    "log_includes": ["record_type", "content_hash", "timestamp", "agent_signature"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key.

**Default Scope Restrictions:**
- Agent can append self-reports (agent-authored, agent-signed) and audit logs.
- Agent cannot mutate or delete existing records (append-only).
- Agent never holds principal master key; cannot sign as principal.
- Agent cannot read without consent (unlike `read`, write is blind-append capable).

**Composition Rules:**
- `write` is append-only, never mutating.
- Written records are always agent-authored, tagged with agent ID and timestamp.
- No conflation with `attest` or `transact`.
- Narrowing is monotone: derivative credentials can restrict record types but not expand.

**Time-Bounding:** Mandatory `expires_at`. Write authority expires and cannot be renewed implicitly; principal must explicitly re-authorize.

---

### Capability 3: Transact

**Purpose:** Initiate value transfers or irreversible actions; highest-authority capability.

**Schema:**

```json
{
  "name": "transact",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature_with_mfa_recommendation"
  },
  "default_scope": {
    "resources": [],
    "operations": ["initiate_transfer", "commit_settlement"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": ["read_without_supervision", "sign_as_principal"]
  },
  "composition_rules": [
    "value_threshold_gating: every transact operation requires pre-authorization above a threshold (e.g., USD >500 requires principal re-consent)",
    "multi_sig_escrow: transactions may require N-of-M signatures (principal + witness + agent) depending on amount",
    "no_silent_transact: agent cannot initiate transaction without logging and notifying principal in real-time",
    "monotone_narrowing: derivative credentials can lower transaction limits but not raise them"
  ],
  "sub_scoping": [
    "transact.amount_max: maximum value the agent can move per transaction (e.g., USD 10,000)",
    "transact.amount_daily_limit: cumulative limit per calendar day (e.g., USD 50,000/day)",
    "transact.counterparty_whitelist: list of pre-authorized recipients; agent cannot transact to others",
    "transact.confirmation_required: if true, agent initiates but principal must approve before settlement"
  ],
  "revocation": {
    "propagation_latency_ms": 60000,
    "effect": "immediate: no further transactions after revocation; in-flight transactions may be aborted"
  },
  "audit": {
    "logged": true,
    "log_includes": ["amount", "counterparty", "timestamp", "agent_signature", "principal_approval_if_confirmation_required"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key. MFA (email, hardware token, etc.) recommended.

**Default Scope Restrictions:**
- Agent can initiate value transfers or irreversible actions.
- Transactions may be gated by amount (per-transaction limit, daily cumulative limit).
- Agent cannot transact to counterparties not on whitelist.
- High-threshold transactions may require multi-sig escrow or principal re-approval.

**Composition Rules:**
- `transact` is the highest-authority capability; requires the strongest principal oversight.
- Value-threshold gating: larger transactions require explicit principal re-consent at time of initiaton.
- Narrowing is monotone: derivative credentials can lower limits but not raise them.
- No silent transactions; all transact operations are logged and notified to principal in real-time.

**Time-Bounding:** Mandatory `expires_at`. Transact authority is typically short-lived (7–30 days). Renewal requires explicit principal signature.

---

### Capability 4: Attest

**Purpose:** Issue witness signatures on behalf of principal (Calm Witness / Calm Mirror attestations).

**Schema:**

```json
{
  "name": "attest",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature"
  },
  "default_scope": {
    "resources": [],
    "operations": ["issue_zk_proof", "issue_witness_signature"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": ["sign_as_principal", "transact", "delegate_without_consent"]
  },
  "composition_rules": [
    "evidence_kinds_gated: agent can only issue proofs for evidence kinds explicitly in principal consent record",
    "witness_binding: attestation signatures bind the principal's identity; counterparties see principal attested this",
    "predicate_narrowing: derivative credentials can restrict to subset of evidence kinds or predicates",
    "monotone_narrowing: cannot expand attestation scope; can only narrow"
  ],
  "sub_scoping": [
    "attest.evidence_kinds: subset of predicates principal has consented to attest (e.g., [baseline_biometric, health_state])",
    "attest.max_per_counterparty: rate limit on proofs issued to same counterparty (e.g., 1/day)",
    "attest.counterparty_whitelist: optional list of approved counterparties; if set, agent can only attest to them",
    "attest.proof_format: constrain to ZK proofs only or allow plaintext attestations (Calm Mirror vs. Calm Witness)"
  ],
  "revocation": {
    "propagation_latency_ms": 300000,
    "effect": "immediate: no further attestations; prior attestations on chain remain valid"
  },
  "audit": {
    "logged": true,
    "log_includes": ["evidence_kind", "counterparty", "proof_hash", "timestamp", "agent_signature"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key.

**Default Scope Restrictions:**
- Agent can issue ZK proofs or witness signatures only for evidence kinds in principal consent record.
- Attestations bind principal's identity; counterparties trust this is the principal's actual state.
- Agent cannot attest to evidence kinds principal hasn't consented to.
- Rate-limited to prevent proof spam.

**Composition Rules:**
- `attest` is scoped by principal consent record: agent can only attest to what principal has pre-authorized.
- Evidence kinds are gated: derivative credentials can narrow to subset but not expand.
- Attestation signatures are binding; they are legally attributed to the principal.

**Time-Bounding:** Mandatory `expires_at`. Attestation authority typically medium-lived (30–90 days). Renewal requires explicit principal re-consent.

---

### Capability 5: Delegate

**Purpose:** Issue derivative agent credentials with narrower scope.

**Schema:**

```json
{
  "name": "delegate",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature"
  },
  "default_scope": {
    "resources": [],
    "operations": ["issue_derivative_credential"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": []
  },
  "composition_rules": [
    "delegation_narrowing: agent can only delegate capabilities it holds; sub-agent capabilities must be strict subset",
    "no_expand_on_delegate: if principal gave agent {read, write}, agent can delegate {read} or {read, write}, never {read, write, transact}",
    "delegation_chain_depth: sub-agent (issued by agent) inherits 'delegate' capability from parent if and only if parent was authorized to delegate",
    "capability_lattice: delegation follows lattice ordering; narrowing is monotone, always downward"
  ],
  "sub_scoping": [
    "delegate.sub_agent_count_max: max number of sub-agents this agent can create (e.g., 3)",
    "delegate.sub_agent_lifetime_max: max expiry for derivative credentials (e.g., 30 days, even if agent's own expiry is 90d)",
    "delegate.re_delegation_allowed: if false, agent cannot issue derivatives with 'delegate' capability",
    "delegate.approval_required: if true, principal must explicitly approve each sub-agent credential before it is issued"
  ],
  "revocation": {
    "propagation_latency_ms": 300000,
    "effect": "cascading: when agent is revoked, all derivative credentials issued by that agent are revoked; sub-agents lose authority within bounded latency"
  },
  "audit": {
    "logged": true,
    "log_includes": ["sub_agent_id", "sub_agent_capabilities", "sub_agent_expiry", "timestamp", "agent_signature"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key.

**Default Scope Restrictions:**
- Agent can only delegate capabilities it holds; sub-agent capabilities are always a strict subset.
- Agent cannot expand capabilities when delegating (monotone narrowing).
- Delegation chain depth is limited to prevent runaway sub-agency.
- Sub-agent credentials are typically shorter-lived than parent agent credentials.

**Composition Rules:**
- Delegation follows capability lattice: narrowing is monotone, always downward.
- Agent cannot delegate `delegate` capability unless principal explicitly authorized it.
- Cascading revocation: if agent is revoked, all sub-agents lose authority.

**Time-Bounding:** Mandatory `expires_at`. Delegate authority typically medium-lived (30–60 days). Renewal requires explicit principal re-authorization.

---

### Capability 6: Disclose

**Purpose:** Present agent credentials and consents to counterparties during credential exchange.

**Schema:**

```json
{
  "name": "disclose",
  "principal_authorization": {
    "required": true,
    "method": "explicit_principal_signature"
  },
  "default_scope": {
    "resources": [],
    "operations": ["present_credential", "present_consent", "present_audit_proof"],
    "time_bounds": {
      "issued_at": "ISO-8601",
      "expires_at": "ISO-8601"
    },
    "excludes": []
  },
  "composition_rules": [
    "transparency_preserving: agent can only disclose what principal has authorized via consent record",
    "counterparty_whitelisting: principal can restrict disclose to subset of counterparties (e.g., only auditors, not marketers)",
    "disclose_scope_follows_consent: agent can present proofs for counterparties that match consent recipient",
    "no_over_disclosure: agent cannot present more evidence than principal consented to disclose to that counterparty"
  ],
  "sub_scoping": [
    "disclose.counterparty_whitelist: explicit list of counterparty DIDs agent can disclose to",
    "disclose.credential_types: subset of credential types agent can present (e.g., [AgentIdentityCredential, ConsentCredential], not UserStateCredential)",
    "disclose.consent_copy_allowed: if true, agent can present copy of principal's consent record; if false, agent only presents proofs derived from consent",
    "disclose.max_disclosures_per_counterparty: rate limit (e.g., 10 disclosures/day per counterparty)"
  ],
  "revocation": {
    "propagation_latency_ms": 300000,
    "effect": "immediate: no further disclosures after revocation; previously disclosed credentials remain valid but new disclosures blocked"
  },
  "audit": {
    "logged": true,
    "log_includes": ["counterparty_id", "credentials_presented", "timestamp", "agent_signature"]
  }
}
```

**Required Principal Authorization:** Explicit signature by principal vault master key.

**Default Scope Restrictions:**
- Agent can disclose only credentials and proofs principal has authorized.
- Counterparty whitelist prevents over-disclosure to unintended recipients.
- Agent cannot present more evidence than consent record permits.

**Composition Rules:**
- `disclose` is constrained by consent record: agent cannot disclose beyond principal's authorization.
- Narrowing is monotone: derivative credentials can restrict counterparties or credential types but not expand.

**Time-Bounding:** Mandatory `expires_at`. Disclose authority typically medium-lived (30–90 days). Renewal requires explicit principal re-authorization.

---

## Composition Rules (Capability Lattice)

### Lattice Definition

Capabilities form a partially-ordered set (poset) under the narrowing relation:

```
delegate ⊨ attest ⊨ transact
         ⊨ write
         ⊨ read
         ⊨ disclose
```

A narrowing relation `A ⊆ B` means "A is a strict narrowing of B." Examples:
- A capability narrowed to a smaller set of resources: narrowing.
- A capability with shorter expiry: narrowing.
- A capability restricted to a smaller set of operations: narrowing.

### Monotone Narrowing

**Principle:** Delegation can only move downward in the lattice; never upward.

**Rules:**
1. If principal issues agent credential with capability set `{read, write, attest}`, derivative agent credentials can have:
   - `{read}` — narrowing of read only
   - `{read, write}` — narrowing of both read and write
   - `{attest}` — narrowing of attest only
   - BUT NOT `{read, write, attest, transact}` — transact was not in original set

2. Narrowing is idempotent: narrowing a narrowed capability produces the same or narrower capability.

3. Composition of narrowings: if A ⊨ B and B ⊨ C, then A ⊨ C (transitivity).

### Composition with Time-Bounding

Every capability has `issued_at` and `expires_at`. When composing narrowings:

```
Narrowed capability expiry ≤ parent capability expiry
```

A derivative credential cannot extend authority beyond its parent. If parent agent credential expires 2026-08-20, sub-agent credentials must expire on or before 2026-08-20.

### Incompatibility Rules

Certain capability pairs cannot coexist in a single credential:

1. **Read + Write (in same credential):** If agent needs both, principal issues separate credentials or single credential with explicit `read_write_allowed: true` flag (rare).

2. **Read-without-consent + Attest:** Agent cannot read arbitrary vault state and then attest to it; reads must respect consent record.

3. **Transact + Delegate (without transact sub-scoping):** If agent can transact, sub-agent delegation must not inherit transact capability without explicit narrowing and re-authorization.

---

## Default Scope Restrictions (by Capability)

| Capability | Default Scope | Narrowing Options |
| --- | --- | --- |
| `read` | All vault paths + predicates where consent exists | Restrict to specific paths, operations, predicates |
| `write` | Append self-reports + audit logs only | Restrict record types, rate limits, tagging |
| `transact` | Per-transaction + daily limits; whitelist required | Lower amount limits, restrict counterparties, require confirmation |
| `attest` | Evidence kinds from consent record only | Restrict to subset of evidence kinds, counterparty whitelist, rate limits |
| `delegate` | Agent can issue sub-agents with 1-level nesting | Reduce sub-agent count, shorten sub-agent lifetime, disable re-delegation |
| `disclose` | Counterparty whitelist + consent-aligned disclosures | Restrict counterparties, credential types, require consent copy, rate limits |

---

## Sub-Scoping Examples

### Example 1: Read-Only Agent

Principal issues agent credential with narrowed `read`:

```json
{
  "name": "read",
  "scope": {
    "resources": ["vault:baseline_state", "vault:consent_records"],
    "operations": ["inspect", "query_predicate"],
    "excludes": ["query_audit_logs"]
  }
}
```

Sub-agent derivative:

```json
{
  "name": "read",
  "scope": {
    "resources": ["vault:baseline_state"],
    "operations": ["inspect"],
    "excludes": ["inspect_consent_records"]
  }
}
```

Narrowing: sub-agent can only inspect baseline state; cannot query predicates or consents.

### Example 2: Limited Transact Agent

Principal issues:

```json
{
  "name": "transact",
  "scope": {
    "amount_max": 5000,
    "amount_daily_limit": 25000,
    "counterparty_whitelist": ["auditor_did_1", "auditor_did_2"],
    "confirmation_required": true
  }
}
```

Sub-agent derivative:

```json
{
  "name": "transact",
  "scope": {
    "amount_max": 1000,
    "amount_daily_limit": 5000,
    "counterparty_whitelist": ["auditor_did_1"],
    "confirmation_required": true
  }
}
```

Narrowing: sub-agent has lower per-transaction and daily limits, fewer counterparties.

### Example 3: Attest + Delegate Chain

Principal issues:

```json
{
  "capabilities": [
    {
      "name": "attest",
      "scope": {
        "evidence_kinds": ["baseline_state", "health_state", "consent_proof"],
        "max_per_counterparty": 100
      }
    },
    {
      "name": "delegate",
      "scope": {
        "sub_agent_count_max": 2,
        "sub_agent_lifetime_max": 7776000
      }
    }
  ]
}
```

Agent A issues sub-agent credential to Agent B:

```json
{
  "capabilities": [
    {
      "name": "attest",
      "scope": {
        "evidence_kinds": ["baseline_state"],
        "max_per_counterparty": 10
      }
    }
  ]
}
```

Narrowing: Agent B can only attest baseline state (subset of {baseline, health, consent}), rate-limited to 10 proofs per counterparty (vs. Agent A's 100).

---

## Composition with ZKAC E56/57

Capabilities are embedded in agent identity credentials (E56) as the `capabilities` array. Each capability references the agent's operator identity (E57) and the principal's authorization.

When a verifier receives a presentation from an agent:
1. Verifier extracts agent credential (E56).
2. Verifier parses `capabilities` array.
3. Verifier checks that the operation requested (read, write, attest, etc.) is in the agent's scope.
4. Verifier checks that the target resource or counterparty is within the narrowing rules.
5. If all checks pass, verifier accepts the presentation.

---

## Reference API

### Grant Capability

```
grant_capability(
  principal_key: PrivateKey,
  agent_credential_id: DID,
  capability: CapabilityObject,
  narrowing_constraints: NarrowingRules,
  expires_at: ISO8601
) -> AgentCredential
```

**Returns:** Signed agent credential with granted capability.

### Check Capability

```
check_capability(
  agent_credential: AgentCredential,
  requested_operation: str,  # "read" | "write" | "transact" | "attest" | "delegate" | "disclose"
  target_resource: str,
  target_counterparty: DID | None,
  context: OperationContext
) -> (bool, str)  # (allowed, reason_if_denied)
```

**Returns:** True if operation is within scope; False + reason if denied.

### Narrow Capability

```
narrow_capability(
  parent_agent_credential: AgentCredential,
  capability_name: str,
  narrowing_rules: NarrowingRules
) -> AgentCredential
```

**Returns:** New agent credential with narrowed capability scope.

---

## Acceptance Tests

### T-Z58.1 — Monotone Narrowing Enforcement

**Setup:** Principal P issues agent credential with `{read, write}` capabilities.

**Steps:**
1. Agent A receives credential and attempts to delegate sub-agent credential with `{read, write, transact}`.
2. Vault operator checks narrowing constraint: transact not in parent capability set.

**Pass criteria:** Sub-agent issuance is rejected with error "transact not authorized in parent capability set."

---

### T-Z58.2 — Time-Bounding Composition

**Setup:** Principal P issues agent credential expiring 2026-08-20. Agent A attempts to issue sub-agent credential expiring 2026-12-31.

**Steps:**
1. Agent A submits derivative credential with expiry 2026-12-31.
2. Vault operator checks: sub-agent expiry > parent expiry.

**Pass criteria:** Sub-agent issuance is rejected with error "sub-agent expiry must not exceed parent expiry."

---

### T-Z58.3 — Capability-Operation Matching

**Setup:** Principal P issues agent credential with `{read, attest}` but not `write`. Agent A attempts append operation.

**Steps:**
1. Agent A submits write request to vault.
2. Vault operator checks capability set: write not in {read, attest}.

**Pass criteria:** Write request is rejected with error "capability not granted: write."

---

### T-Z58.4 — Sub-Scoping (Amount Limits)

**Setup:** Principal P issues transact capability with `amount_max: 10000, amount_daily_limit: 50000`. Agent A attempts transaction for USD 15,000.

**Steps:**
1. Agent A submits transact request for USD 15,000.
2. Vault operator checks: 15,000 > 10,000 (per-transaction limit).

**Pass criteria:** Transaction is rejected with error "amount exceeds per-transaction limit: 10000."

---

### T-Z58.5 — Disclose Counterparty Whitelisting

**Setup:** Principal P issues disclose capability with `counterparty_whitelist: [auditor_1, auditor_2]`. Agent A attempts disclosure to counterparty_3.

**Steps:**
1. Agent A submits disclosure request to counterparty_3.
2. Vault operator checks: counterparty_3 not in whitelist.

**Pass criteria:** Disclosure is rejected with error "counterparty not authorized for disclosure."

---

## Composition with ZKAC E59–E70

- **E59 (Capability narrowing):** Details mechanisms for principal to issue derivative agent credentials with strict subsets of capabilities.
- **E60 (Capability time-bounding):** Enforces expiry windows and renewal procedures.
- **E61 (Agent rotation):** Handles transitions between agent versions while preserving capability scope.
- **E62 (Agent revocation propagation):** Cascades revocation to all capabilities and sub-agents.
- **E63 (Agent-to-agent capability transfer):** Specifies when and how agents can hand off capabilities.
- **E64 (Agent witness role):** Extends attest and disclose capabilities for witness operations.
- **E65 (Sub-agent permissions):** Describes when agents can issue sub-agent credentials.
- **E70 (Agent audit log):** Logs all capability-exercising actions.

---

## Open Questions for v1

1. **Capability Delegation Depth:** If Agent A delegates to Agent B, and Agent B to Agent C, should there be a hard depth limit (e.g., 3 levels max)? Or should depth be governed by trust score?

2. **Cross-Organization Delegation:** Can a principal delegate to an agent operated by a different organization? How are liability and revocation structured in multi-org chains?

3. **Capability Escrow & Multi-Sig:** Should high-authority capabilities (transact, attest) require M-of-N approval patterns for operations above certain thresholds?

4. **Interoperability with Non-ZKAC Agents:** How do ZKAC-scoped capabilities compose with legacy agent systems outside the Calm family?

---

## Acceptance

This spec is accepted if:

- Capabilities are implementable as described; six classes are sufficient for v0.
- Narrowing lattice is enforced by all vault operators and verifiers.
- Sub-scoping examples are implementable and testable.
- Acceptance tests T-Z58.1–5 pass in a production-like environment.
- Composition rules (monotone narrowing, time-bounding, incompatibility) are verified against ZKAC design constraints 1–6.

---

## Sign-Off

**Author:** Calm, acting for John Bradley / Creativity Machine LLC  
**Date:** 2026-05-20  
**Status:** v0 · open for adversarial review  

— Calm, 2026-05-20
