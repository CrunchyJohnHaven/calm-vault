# Agent Reputation Without Surveillance v0

**Draft v0 · 2026-05-20 · Calm**

**Closes Everest 144 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Prereq:** [`AGENT_CAPABILITY_REGISTRY_v0.md`](AGENT_CAPABILITY_REGISTRY_v0.md) (Everest 142).

**Companion to [`AGENT_IDENTITY_BEACON_v0.md`](AGENT_IDENTITY_BEACON_v0.md) (Everest 141) and [`AGENT_SERVICE_DISCOVERY`](AGENT_CAPABILITY_REGISTRY_v0.md) (Everest 143, forthcoming).**

---

## Abstract

An agent earns or loses **reputation bits** only when a **counterparty** cryptographically attests a **verifiable transaction commitment**. No registry, relay, or observer stores underlying transaction details, numeric similarity scores, or protected-category labels. Reputation is a set of named boolean flags (`bit_id → held | not held`), updated by signed counterparty attestations that reference envelope digests or session commitments, never plaintext payloads.

---

## §1 — The Problem: Trust Signals Without Dossiers

Service discovery (Everest 143) answers "who can do verb V over predicate P?" Reputation answers "has this agent completed verifiable work with aligned counterparties?" Traditional reputation systems fail ZKAC policy because they:

1. Log transaction bodies or derived features (surveillance).
2. Publish numeric scores or rankings (similarity scores).
3. Encode demographic or protected-class proxies (protected categories).

Everest 144 specifies a **counterparty-attested, bit-only reputation ledger** that composes with Witness envelopes and Pact sessions without expanding the surveillance surface.

---

## §2 — Core Objects

### §2.1 — Reputation bit

A **reputation bit** is a stable identifier `rep.v0.<name>` (kebab-case name, max 64 chars). Examples:

| `bit_id` | Meaning when held |
|----------|-------------------|
| `rep.v0.envelope-verified` | At least one counterparty attested successful envelope verification |
| `rep.v0.pact-session-completed` | At least one counterparty attested a completed Pact-aligned session |
| `rep.v0.handoff-accepted` | At least one counterparty attested an accepted task handoff (Everest 147, forward compatible) |

Bits are **boolean**. There is no magnitude, weight, percentile, or "trust score."

### §2.2 — Transaction commitment

A **transaction commitment** is a 64-character lowercase hex SHA-256 digest binding a completed interaction without revealing its contents. Acceptable commitment sources:

- `envelope_digest`: SHA-256 of canonical ZKAC composite envelope bytes (Everest 139).
- `pact_session_digest`: SHA-256 of `{session_nonce, counterparty_id}` per `zkac_envelope.pact_session_digest`.
- `handoff_digest`: SHA-256 of handoff record canonical JSON (Everest 147, optional in v0).

The commitment MUST NOT be reversible to principal state, directive text, or undisclosed predicate bits.

### §2.3 — Counterparty attestation

A **counterparty attestation** is a signed wire object:

```json
{
  "wire_version": "calm-agent-reputation-attestation/v0",
  "kind": "CounterpartyReputationAttestation",
  "subject_did": "did:zkac:v0:john-bradley:calm-primary",
  "counterparty_did": "did:zkac:v0:acme-corp:agent-1",
  "transaction_commitment": "<64-hex>",
  "commitment_kind": "envelope_digest",
  "bit_id": "rep.v0.envelope-verified",
  "delta": "earn",
  "attested_at_iso": "2026-05-20T12:00:00Z",
  "attestation_digest": "<64-hex>",
  "counterparty_signature": "sha256:<digest>"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `subject_did` | yes | Agent whose reputation changes |
| `counterparty_did` | yes | Attesting agent; MUST differ from subject |
| `transaction_commitment` | yes | 64-hex SHA-256 |
| `commitment_kind` | yes | `envelope_digest` \| `pact_session_digest` \| `handoff_digest` |
| `bit_id` | yes | Must match `rep.v0.*` pattern |
| `delta` | yes | `earn` sets bit; `lose` clears bit |
| `attested_at_iso` | yes | ISO 8601 UTC |
| `attestation_digest` | yes | SHA-256 of canonical content fields |
| `counterparty_signature` | yes | v0: `sha256:<attestation_digest>`; production: Ed25519 over digest |

**Prohibited keys** anywhere in the attestation object (gate-enforced):

`similarity_score`, `score`, `ranking`, `percentile`, `trust_score`, `protected_category`, `demographic`, `race`, `religion`, `gender`, `disability`, `transaction_details`, `envelope_body`, `payload`, `records`, `user_state`, `chain_jsonl`, `proof`, `disclosures`, `biometric`, `evidence`.

### §2.4 — Reputation ledger (public view)

Each subject agent publishes a **reputation manifest**:

```json
{
  "schema_version": "calm-agent-reputation-ledger/v0",
  "subject_did": "did:zkac:v0:john-bradley:calm-primary",
  "bits_held": ["rep.v0.envelope-verified"],
  "attestation_count": 3,
  "last_updated_iso": "2026-05-20T12:00:00Z",
  "manifest_digest": "<64-hex>"
}
```

The manifest lists **only** bit IDs currently held and aggregate counts. It does NOT list counterparties, commitments, or timestamps per attestation (those live in optional private vault chains only).

---

## §3 — Earn and Lose Semantics

### §3.1 — Earn (`delta: earn`)

1. Counterparty completes a verifiable transaction with subject (envelope verified, session completed, etc.).
2. Counterparty computes `transaction_commitment` from the completed artifact only.
3. Counterparty signs attestation with `delta: earn` and target `bit_id`.
4. Subject (or a neutral relay) verifies signature and digest shape, then sets `bit_id` in the ledger.

Duplicate attestations for the same `(counterparty_did, transaction_commitment, bit_id)` are idempotent: second application is a no-op.

### §3.2 — Lose (`delta: lose`)

1. Counterparty observes a falsifiable failure (e.g. envelope signature invalid on replay challenge per Everest 142 §11.1).
2. Counterparty issues attestation with `delta: lose` for the same `bit_id` and a **new** `transaction_commitment` referencing the challenge record.
3. Subject clears `bit_id` from `bits_held`.

Lose attestations MUST NOT include failure reasons that encode protected categories or principal-identifying surveillance data. Allowed `revocation_reason` enum (optional, off-ledger): `signature_invalid`, `scope_violation`, `rate_limit_exceeded`, `timeout`.

---

## §4 — Anti-Surveillance Guarantees

No party in the reputation flow may persist:

- Undisclosed predicate bit values.
- Pact directive plaintext or commitment openings.
- Principal identifiers beyond agent DIDs already public in beacons.
- Correlation tables linking `transaction_commitment` to principal vault record bodies.

**Observers** of the public manifest learn only which named bits an agent currently holds. They do NOT learn how many counterparties contributed, which commitments were used, or transaction ordering beyond `last_updated_iso`.

**Counterparties** may retain local attestations they signed (for dispute resolution). Retention is operator policy, not protocol requirement. Export of local attestations to third parties is out of scope for v0.

---

## §5 — No Similarity Scores

The protocol forbids:

- Numeric trust scores, stars, percentiles, or ML-derived rankings.
- Comparative lists ("agent A is better than agent B").
- Aggregated counters beyond `attestation_count` (non-comparable magnitude).

Everest 143 discovery MAY filter on `bit_id` membership (boolean), never on score thresholds.

---

## §6 — No Protected Categories

Reputation bits MUST NOT reference:

- Race, ethnicity, national origin, religion, gender, sexual orientation, disability, age, pregnancy, genetic information, or any proxy thereof.
- Forbidden predicate IDs from Witness or Compass refusal floors.

Registry and gate code reject attestations or bit definitions containing prohibited keys (§2.3) or matching forbidden bit name patterns (`rep.v0.*-by-demographic`, etc.).

---

## §7 — Integration with Everest 142

| Everest 142 artifact | Reputation use |
|------------------------|----------------|
| Agent DID (`did:zkac:...`) | `subject_did`, `counterparty_did` |
| Capability tuple | Optional: attestation MAY require subject held `rep.v0.envelope-verified` before high-value `issue` |
| Falsifiability (§11) | Lose path when capability challenge fails |

Capability registry entries MUST NOT embed numeric reputation fields. Cross-link is by boolean bit membership only.

---

## §8 — Wire Verification Algorithm

1. Reject if any prohibited key present (recursive dict walk).
2. Validate `subject_did` and `counterparty_did` match `^did:zkac:v0:[^:]+:[^:]+$` and differ.
3. Validate `transaction_commitment` and `attestation_digest` are 64-hex.
4. Validate `bit_id` matches `^rep\.v0\.[a-z0-9-]+$`.
5. Validate `delta` ∈ `{earn, lose}`.
6. Recompute `attestation_digest` from content fields; compare.
7. Verify `counterparty_signature` matches v0 stub `sha256:<attestation_digest>`.
8. Apply delta to in-memory or persisted ledger.

Reference implementation: `CredexAI/calm_witness/agent_reputation.py`.

---

## §9 — Publication Flow

1. Subject publishes beacon (Everest 141) at `/.well-known/zkac-beacon.json`.
2. Subject accumulates attestations in operator vault chain (`kind: reputation_attestation`) without exporting bodies to a central server.
3. Subject periodically publishes `reputation-manifest.json` beside the beacon (HTTPS, same host).
4. Discovery (Everest 143) indexes manifest `bits_held` only.

---

## §10 — Worked Example

**Agents:** Subject `S = did:zkac:v0:john-bradley:calm-primary`, counterparty `C = did:zkac:v0:acme-corp:agent-1`.

1. `C` verifies a composite envelope from `S`; canonical bytes hash to `abc...123` (64 hex).
2. `C` builds attestation: `commitment_kind: envelope_digest`, `bit_id: rep.v0.envelope-verified`, `delta: earn`.
3. `C` signs; `S` verifies and sets bit.
4. Public manifest shows `bits_held: ["rep.v0.envelope-verified"]` with no envelope content logged.
5. Later, `C` detects invalid replay signature, issues `delta: lose` with new commitment `def...456`.
6. Manifest removes the bit; no record states which counterparty caused the loss.

---

## §11 — Falsifiability

| Claim | Challenge |
|-------|-----------|
| Bit held without valid work | Counterparty refuses to reproduce attestation signature for a disclosed commitment |
| Bit not held despite work | Subject cannot produce manifest; counterparty publishes redacted attestation proof |
| Surveillance leakage | Audit finds prohibited keys in published manifest or attestation wire dumps |
| Similarity score smuggled | Gate or linter finds numeric `score` fields in reputation objects |

---

## §12 — Versioning

- Wire: `calm-agent-reputation-attestation/v0`
- Ledger: `calm-agent-reputation-ledger/v0`

Breaking changes require v1 and new DID method version negotiation.

---

## §13 — Sign

— Musk, 2026-05-20

For Everest 144, acceptance criteria are met: counterparty-attested earn/lose semantics on verifiable transaction commitments only; no underlying transaction detail logging in public manifests; explicit prohibition of similarity scores and protected categories; integration with Everest 142 DIDs and falsifiability; JSON wire schemas; worked example; reference implementation and gate.

## References

- **Everest 141 (Agent Identity Beacon)**: DID format and beacon hosting.
- **Everest 142 (Agent Capability Registry)**: Capability tuples; no numeric ranking.
- **Everest 143 (Agent Service Discovery)**: Boolean bit filtering (forthcoming).
- **Everest 139 (ZKAC unified verify)**: Envelope digest source.
- **Everest 145 (Agent Introduction Protocol)**: Anti-surveillance baseline.
- **PREDICATE_VOCABULARY_v0.md**: Refusal floor predicate IDs.
