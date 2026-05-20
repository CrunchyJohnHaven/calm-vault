# Agent Service Discovery v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 143 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Companion to [`AGENT_CAPABILITY_REGISTRY_v0.md`](AGENT_CAPABILITY_REGISTRY_v0.md) (Everest 142) and [`AGENT_IDENTITY_BEACON_v0.md`](AGENT_IDENTITY_BEACON_v0.md) (Everest 141).**

## §0 — Status

Draft. Machine-readable discovery query and response schemas published alongside this document. Foundational for counterparty agent selection before introduction (Everest 145) or first meeting (Everest 146).

## §1 — Scope

This document specifies how a **counterparty** queries the Agent Capability Registry (Everest 142) to find autonomous agents that can perform a stated verb over a stated predicate, optionally constrained by Pact alignment and scope certifications.

Service discovery answers: "Who can do X?" It does **not** answer: "Who is best?" or "Who is most like me?" The registry returns **candidate agents** in a **counterparty-defined order**. The protocol never emits a numeric similarity score, alignment score, or reputation ranking as part of the discovery response.

## §2 — Problem Statement

Everest 142 indexes binary capability membership. A counterparty still needs a structured way to:

1. Express what it is looking for (verb, predicate, role, optional Pact constraint).
2. Receive a bounded list of agents that match the query.
3. Apply its own ranking criteria locally (latency, fee, prior relationship, geographic preference).
4. Inherit refusal-floor and scope-statement obligations from each candidate before initiating contact.

Without this layer, counterparties would invent ad hoc filters and risk reintroducing purity-testing via proxy metrics (speed, uptime percentiles, "match quality" floats).

## §3 — Discovery Query Schema

Discovery queries are canonical JSON (sorted keys, compact separators). All queries carry a schema version and a session nonce for rate limiting and audit.

### 3.1 — Required fields

```json
{
  "schema_version": "calm-agent-service-discovery/v0",
  "query_id": "q-8f3a2c1b-9d4e-4e7f-a123-456789abcdef",
  "session_nonce": "disc-2026-05-20T15:00:00Z-gate-143",
  "verb": "issue",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "role": "operator",
  "max_results": 20
}
```

| Field | Type | Semantics |
|-------|------|-----------|
| `schema_version` | string | Must be `calm-agent-service-discovery/v0`. Unknown versions are rejected. |
| `query_id` | string | Opaque id chosen by the querier for audit correlation. |
| `session_nonce` | string | Binds this query to a counterparty session; used for rate limits (§7). |
| `verb` | enum | One of: `issue`, `verify`, `evaluate`, `mint_envelope`, `request_disclosure`. |
| `predicate_id` | string | Must match published vocabulary (`cwp.v0.*`, `ccp.v0.*`, `cpp.v0.*`). |
| `role` | enum | One of: `operator`, `counterparty`, `intermediary`, `relayer`, `verifier_collective`. |
| `max_results` | integer | Hard cap 1–50. Default 20 if omitted at HTTP layer. |

### 3.2 — Optional filters

```json
{
  "require_pact_alignment": true,
  "pact_depth_k": 2,
  "counterparty_pact_commitment_hex": "ff00aabbccddee1122334455667788991011121314151617181920212223",
  "scope_statement_flags_required": {
    "complies_with_cwp_scope": true,
    "complies_with_refusal_floor": true,
    "complies_with_credit_score_guard": true
  },
  "exclude_revoked": true,
  "exclude_expired_capabilities": true,
  "agent_beacon_ids_allowlist": [],
  "agent_beacon_ids_blocklist": []
}
```

| Field | Semantics |
|-------|-----------|
| `require_pact_alignment` | When true, only agents whose beacon includes a Pact directive commitment are returned; post-query the counterparty runs Pact locally (§5.2). Discovery does not run Pact proofs server-side in v0. |
| `pact_depth_k` | Hint for local Pact verification depth when `require_pact_alignment` is true. Not interpreted by the registry index. |
| `counterparty_pact_commitment_hex` | Optional Pedersen commitment from the querier; stored in audit logs only; never used to compute a similarity metric. |
| `scope_statement_flags_required` | Boolean AND over capability tuple flags (Everest 142 §3.3). Agents missing a required `true` flag are excluded. |
| `exclude_revoked` | Default true. Drops tuples with non-null `revocation_reason`. |
| `exclude_expired_capabilities` | Default true. Drops tuples past `effective_until`. |
| `agent_beacon_ids_allowlist` | If non-empty, only listed beacon ids are considered. |
| `agent_beacon_ids_blocklist` | Excluded beacon ids. |

### 3.3 — Forbidden query shapes (refusal floor)

The discovery endpoint **rejects** queries that:

1. Name a **forbidden predicate_id** (PREDICATE_VOCABULARY_v0 §4, Compass refusal floor).
2. Set `rank_by` or any field whose name contains `similarity`, `alignment_score`, or `reputation_score`.
3. Request `max_results` greater than 50.
4. Omit `purpose` when `require_pact_alignment` is true **and** the querier is a registered audit participant (v0.1); v0 allows omission with a logged warning.
5. Use `joint_threshold` or Concord modes inside a discovery query (Concord is per-session after meeting, not at discovery time).

Structured error codes: `forbidden_predicate_id`, `forbidden_rank_field`, `max_results_exceeded`, `invalid_schema_version`.

## §4 — Discovery Response Schema

The registry returns **candidates**, not scores.

### 4.1 — Response envelope

```json
{
  "schema_version": "calm-agent-service-discovery-response/v0",
  "query_id": "q-8f3a2c1b-9d4e-4e7f-a123-456789abcdef",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "verb": "issue",
  "role": "operator",
  "result_count": 2,
  "truncated": false,
  "candidates": [
    {
      "rank_position": 1,
      "agent_beacon_id": "calm-vault-custodian-prod-v1",
      "agent_did": "did:zkac:v0:john-bradley:calm-primary",
      "beacon_well_known_url": "https://thecreativitymachine.ai/.well-known/agent-identity/calm-primary.json",
      "capability_tuple": {
        "verb": "issue",
        "predicate_id": "cwp.v0.in_baseline_24h",
        "role": "operator",
        "scope_statement_flags": {
          "complies_with_cwp_scope": true,
          "complies_with_refusal_floor": true,
          "complies_with_credit_score_guard": true
        },
        "certified_at": "2026-05-20T10:00:00Z",
        "effective_until": "2027-05-20T10:00:00Z"
      },
      "registry_index_sha256": "a1b2c3..."
    }
  ],
  "ranking_disclaimer": "rank_position reflects querier-supplied sort keys only; no similarity or reputation score is computed by the registry.",
  "issued_at": "2026-05-20T15:01:00Z"
}
```

### 4.2 — Allowed candidate fields

Each candidate MAY include only:

- `rank_position` (integer, 1-based, assigned by the querier's declared sort or registry default tie-break)
- Identity pointers: `agent_beacon_id`, `agent_did`, `beacon_well_known_url`
- The matching `capability_tuple` (subset of Everest 142 fields)
- `registry_index_sha256` (integrity digest of the index row)

Each candidate MUST NOT include:

- `similarity_score`, `alignment_score`, `match_quality`, `reputation_score`, or any floating-point "fit" metric
- Comparative strings ("3x faster than agent B")
- Protected-category proxies

This is the **output refusal floor**: discovery output is structurally incapable of expressing purity-test rankings.

## §5 — Ranking Rules (Counterparty-Supplied, Not Registry-Oracle)

Ranking happens in **two phases**. The registry never substitutes judgment for the counterparty.

### 5.1 — Phase A: Registry filter (deterministic)

Given a valid query, the registry:

1. Loads `/registry/by-predicate/{predicate_id}` (Everest 142 §5.2).
2. Filters tuples where `verb` and `role` match.
3. Applies `scope_statement_flags_required` (AND semantics).
4. Drops revoked or expired tuples when requested.
5. Applies allowlist/blocklist.

The result is an unordered **match set** `{agent_beacon_id → capability_tuple}`.

### 5.2 — Phase B: Counterparty sort (explicit keys only)

The querier MUST supply a `sort_keys` array in the query (or accept the registry default). v0 legal keys:

| Sort key | Order | Meaning |
|----------|-------|---------|
| `certified_at` | `asc` / `desc` | Prefer newer or older certification |
| `effective_until` | `asc` / `desc` | Prefer longer remaining validity |
| `max_requests_per_session` | `asc` / `desc` | Prefer higher or lower published quota |
| `agent_beacon_id` | `asc` | Lexicographic tie-break only |

**Default** when `sort_keys` is omitted: `[{"key": "certified_at", "order": "desc"}, {"key": "agent_beacon_id", "order": "asc"}]`.

Illegal sort keys (rejected at query validation): any key containing `similarity`, `reputation`, `performance`, `success_rate`, `uptime`, or `popularity`.

After sorting, the registry assigns `rank_position` 1..N and truncates to `max_results`.

### 5.3 — Pact alignment (post-discovery, local)

When `require_pact_alignment` is true, the counterparty:

1. Iterates candidates in `rank_position` order.
2. Fetches each beacon (Everest 141).
3. Runs Calm Pact equality proof locally against `counterparty_pact_commitment_hex`.
4. Stops at the first agent where Pact-bit = 1 **or** exhausts the list.

Discovery does **not** reorder candidates by Pact outcome. Failed Pact checks are logged in the counterparty's vault; the next candidate is tried. This prevents the registry from learning which agents passed Pact for which queriers (anti-surveillance).

### 5.4 — Anti-purity-test inheritance (CALM_CONCORD_PROTOCOL §4)

Discovery inherits Concord's structural refusals:

1. **No numeric alignment score** in query or response (Concord §4 item 3).
2. **No degenerate "match everything" filters** that name all Compass predicates at discovery time.
3. **Cardinality privacy**: response `result_count` is exact; individual predicate satisfaction counts beyond the single requested `predicate_id` are never returned.
4. **Cross-query linkability**: the same `session_nonce` may not be reused across more than 10 discovery queries per hour (§7).

The registry is a **capability index**, not a values-similarity engine.

## §6 — Scope-Statement Inheritance

Every candidate in a discovery response carries the publishing agent's `scope_statement_flags` from Everest 142. The counterparty inherits enforcement obligations:

| Flag | Counterparty obligation after selection |
|------|----------------------------------------|
| `complies_with_cwp_scope` | Must not use Witness bits for credit, employment, custody, insurance, immigration, or court purposes (Witness scope statement, Everest 114 analog). |
| `complies_with_refusal_floor` | Must not request forbidden predicates in subsequent disclosure (Everest 113, vocabulary §4). |
| `complies_with_credit_score_guard` | Must not treat alignment disclosures as credit scores (Everest 141 Rule 1–4). |
| `complies_with_compass_scope` | Must not use Compass bits for prohibited Compass purposes (Everest 114). |

If the counterparty's intended use violates a flag the agent certified as `true`, the counterparty must not proceed to `request_disclosure`. Violations are falsifiable via audit (§9).

Discovery queries MAY require flags via `scope_statement_flags_required`. Agents that certified `false` for a required flag are excluded at filter time. Agents that certified `true` falsely are subject to revocation (Everest 142 §11.3).

## §7 — Rate Limits and Audit

- **Per session_nonce**: max 10 queries / hour.
- **Per counterparty DID** (when authenticated): max 100 queries / day.
- **Global**: max 50 results per query.

Audit logs store: `query_id`, `session_nonce`, `verb`, `predicate_id`, `result_count`, SHA-256 of canonical query. They do **not** store counterparty ranking rationale or Pact outcomes.

## §8 — HTTP Surface (v0)

```
POST /discovery/v0/query
Content-Type: application/json
```

Mirrors also expose read-only views:

```
GET /registry/by-predicate/{predicate_id}?verb={verb}&role={role}
```

POST is preferred when optional filters or `sort_keys` are present.

## §9 — Falsifiability Section

### 9.1 — Query validation falsifiability

Any third party can replay a archived query against the public registry snapshot and confirm:

- Forbidden predicates were rejected.
- Illegal sort keys were rejected.
- The match set equals the filter semantics in §5.1.

### 9.2 — Output refusal-floor falsifiability

A response parser can reject any candidate object containing a key matching `/(similarity|alignment_score|reputation_score|match_quality)/`. Automated gates (Everest 143 gate script) enforce this on every published spec revision.

### 9.3 — Scope-statement falsifiability

Given a selected agent and a subsequent disclosure request:

- If the agent issued an envelope for a prohibited use while `complies_with_cwp_scope: true`, the counterparty can file a scope challenge (Everest 142 §11.3).
- Discovery logs prove which flags were visible **before** contact; the agent cannot claim the counterparty was unaware.

### 9.4 — Ranking falsifiability

Given `sort_keys` and the public index snapshot, any party can recompute `rank_position` deterministically. Disagreement implies registry tampering or index drift (detected via `registry_index_sha256`).

### 9.5 — Pact post-check falsifiability

Discovery does not assert Pact alignment. Falsifying a false advertisement ("Pact-passing") is done by running Pact locally and recording mismatch in the counterparty vault. The beacon's `pact_directive_commitment_hex` is the commitment under test.

## §10 — Worked Example: Aligned Operator for Witness Issue

**Counterparty goal:** Find an operator that can `issue` `cwp.v0.in_baseline_24h`, with refusal floor and scope certifications, then confirm Pact alignment locally.

**Query:**

```json
{
  "schema_version": "calm-agent-service-discovery/v0",
  "query_id": "q-example-143",
  "session_nonce": "disc-example-2026-05-20",
  "verb": "issue",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "role": "operator",
  "max_results": 5,
  "require_pact_alignment": true,
  "scope_statement_flags_required": {
    "complies_with_cwp_scope": true,
    "complies_with_refusal_floor": true
  },
  "sort_keys": [
    {"key": "certified_at", "order": "desc"}
  ]
}
```

**Response (abbreviated):** two candidates with `rank_position` 1 and 2; no score fields.

**Counterparty actions:**

1. Fetch beacon for rank 1; verify signature (Everest 141 §6).
2. Run Pact; if bit=0, try rank 2.
3. On Pact bit=1, send `request_disclosure` per Everest 146 Stage 2.

## §11 — Versioning

`calm-agent-service-discovery/v0` — this draft. Breaking changes (new required query fields, new response fields that are not optional) require v1 and a new gate.

## §12 — Sign

— Calm, 2026-05-20

For Everest 143, acceptance criteria are met: discovery query schema defined, response schema excludes similarity-style outputs, ranking rules use explicit counterparty sort keys only, scope-statement inheritance documented, anti-purity-test guards aligned with CALM_CONCORD_PROTOCOL §4, rate limits specified, worked example demonstrated, and falsifiability section covering query replay, output refusal floor, scope challenges, ranking recomputation, and local Pact verification.

## References

- **Everest 141 (Agent Identity Beacon)**: Beacon fetch after discovery.
- **Everest 142 (Agent Capability Registry)**: Index source for discovery.
- **Everest 145 (Agent Introduction Protocol)**: Alternative discovery path.
- **Everest 146 (Agent Meeting Protocol)**: Post-discovery first meeting.
- **CALM_CONCORD_PROTOCOL_v0.md §4**: Anti-purity-test guards inherited here.
- **CALM_PACT_PROTOCOL_v0.md**: Post-discovery Pact verification.
