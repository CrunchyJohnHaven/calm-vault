# Agent Task-Handoff Protocol v0

**Draft v0 · 2026-05-20 · Calm**

**Closes Everest 147 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Prereq:** [`AGENT_MEETING_PROTOCOL_v0.md`](AGENT_MEETING_PROTOCOL_v0.md) (Everest 146). **Types:** [`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md).

---

## Abstract

After two agents complete a first meeting (Pact, Witness, optional Compass), one agent may delegate an operational task to the other: research continuation, escrow execution, outreach, or monitoring. The handoff must move **only** the context the receiving principal has consented to disclose, must leave an **immutable, hash-linked record in both principals' vaults**, and must support **attribution** (who offered, who accepted, when) **without surveillance** (no logging of internal reasoning, deliberation, or undisclosed chain records). This protocol specifies the offer, acceptance, refusal, completion, and dual-vault choreography for that transfer.

---

## §1 — Scope and design goals

**In scope:** A bilateral flow between Operator A (originator) and Operator B (receiver) where A offers a bounded task bundle, B accepts or refuses without reason leakage, both vaults append chained `agent_task_handoff` records, and an optional attribution root is published for downstream Everest 148 composition.

**Not in scope:** Multi-hop handoff chains beyond one hop (v1); billing (Everest 149); full attribution DAG (Everest 148); substantive transaction execution after handoff (same as meeting Stage 5).

**Design goals:**

1. **Dual vault truth:** Both principals receive append-only, hash-linked records; neither vault is authoritative alone.
2. **Attribution without surveillance:** Counterparties learn structural facts (offer, accept, complete) and pseudonymous agent IDs, not internal prompts, tool traces, or undisclosed vault entries.
3. **Refusal floor:** Receiver may refuse at any step; originator may withdraw before acceptance; no party is forced to disclose why.
4. **Chained context:** Each handoff record links to `predecessor_record_hash` inside the vault and optionally to a prior `handoff_id` for task lineage.
5. **Falsifiable:** An auditor can verify both vaults contain matching handoff IDs, timestamps, and outcome bits without reading private task bodies.

---

## §2 — Parties and artifacts (ZKAC types)

| ZKAC type | Handoff role |
|-----------|----------------|
| **Principal** | Owns each vault; authorizes consent for context export. |
| **Operator** | Originates or receives the handoff; signs wire messages. |
| **Vault** | Append-only store; receives `agent_task_handoff` records. |
| **Counterparty** | The other Operator in the session. |
| **Envelope** | Carries attested context slices (Witness/Compass bits already cleared in meeting). |
| **ChainHead** | Binds handoff attestations to vault state at offer/accept time. |
| **AttestationFingerprint** | Identifies the task-context bundle without revealing contents. |

### §2.1 — Core artifacts

**Task digest:** `SHA-256(canonical_json(task_spec_redacted))` where `task_spec_redacted` includes only fields both principals pre-authorized in the meeting consent matrix (title, mission tag, deadline, deliverable class). Full prompts and PII stay in the originator vault unless explicitly attached with separate consent.

**Handoff bundle:** Signed JSON from A to B:

```json
{
  "wire_version": "calm-agent-handoff/wire/v0",
  "kind": "TaskHandoffOffer",
  "handoff_id": "<uuid>",
  "session_nonce": "<unique>",
  "meeting_id": "<from Agent Meeting Protocol>",
  "originator_operator": "<Ed25519 fingerprint>",
  "receiver_operator": "<Ed25519 fingerprint>",
  "task_digest": "<64-hex>",
  "context_envelope": {
    "chain_head": "<64-hex at offer time>",
    "disclosures": [],
    "attestation_fingerprints": []
  },
  "predecessor_handoff_id": null,
  "offered_at_iso": "<ISO 8601>",
  "originator_signature": "<Ed25519>"
}
```

**Handoff acceptance:** B returns `TaskHandoffAccept` or `TaskHandoffRefuse` with the same `handoff_id` and `session_nonce`. Refuse carries `reason_disclosure: none` only (per meeting protocol Stage 6).

**Attribution root (v0):** A 64-hex `attribution_root = SHA-256(handoff_id || originator_operator || receiver_operator || task_digest || accept_timestamp)` stored in both vaults. Everest 148 extends this into a multi-step chain; v0 records the root only.

---

## §3 — Preconditions

Handoff may begin only when:

1. **Meeting cleared:** A valid `meeting_id` exists with `pact_match` and `witness_cleared` in both vaults (AGENT_MEETING_PROTOCOL_v0 Stages 1–2).
2. **Consent matrix:** Principal of A has `grant` or standing directive for `task_context_export` to the counterparty class of B.
3. **Capability registry:** B's published capability registry (Everest 142) lists the task verb (e.g., `execute.research.continuation`).
4. **No scope violation:** Neither party uses handoff for employment screening, lending, insurance, immigration, or surveillance (inherits CALM_WITNESS_SCOPE_STATEMENT §2 and Compass scope).

If any precondition fails, the originator MUST NOT send `TaskHandoffOffer`.

---

## §4 — Handoff flow

### Stage H0 — Offer

Operator A constructs `TaskHandoffOffer`, signs it, and transmits to B. A simultaneously appends to **Principal A's vault**:

```json
{
  "record_kind": "agent_task_handoff",
  "handoff_id": "<uuid>",
  "role": "originator",
  "meeting_id": "<nonce>",
  "counterparty_agent_pseudonym": "<CredexAI fingerprint of B>",
  "stage": "offered",
  "task_digest": "<64-hex>",
  "attribution_root": "<64-hex or null until accept>",
  "predecessor_record_hash": "<SHA-256 prior vault entry>",
  "timestamp_utc": "<ISO 8601>",
  "operator_signature": "<Ed25519>"
}
```

No task body text is required in the vault record; only `task_digest`.

### Stage H1 — Receiver evaluation

Operator B verifies:

- Signature and `wire_version`.
- `meeting_id` matches a cleared meeting in B's vault.
- `context_envelope` verifies against B's consent matrix (no undisclosed predicates).
- `task_digest` matches a preview shown to B's principal (human or standing policy).

B MUST NOT log A's internal evaluation traces. B may consult only the offer wire object and vault metadata.

### Stage H2 — Accept or refuse

**Accept:** B sends `TaskHandoffAccept`, appends to **Principal B's vault** with `stage: accepted`, and includes the same `handoff_id`, `task_digest`, and computed `attribution_root`. A appends `stage: accepted` on receipt (originator copy).

**Refuse:** B sends `TaskHandoffRefuse` with `reason_disclosure: none`. B's vault records `stage: refused`. A's vault records `stage: refused_received` without learning which internal rule triggered refusal.

**Timeout:** If B is silent for >48 hours, A may record `stage: offer_expired` and MUST NOT retry the same `handoff_id` (new offer requires new `handoff_id`).

### Stage H3 — Execution boundary

After accept, substantive work proceeds under separate SLA. The handoff protocol records `stage: execution_started` when B acknowledges work began, and `stage: completed` when B returns a completion digest `SHA-256(deliverable_redacted)`. Neither completion digest nor deliverable body is written to A's vault unless Principal A consented to `deliverable_import`.

### Stage H4 — Dual-vault closure

Both vaults MUST contain matching rows for: `handoff_id`, `task_digest`, final `stage`, and `attribution_root`. Mismatch is a protocol violation detectable by either principal's backup verifier.

---

## §5 — Chained handoff records

Within each vault, `agent_task_handoff` entries form a **per-counterparty chain**:

- `predecessor_record_hash` MUST equal the `record_hash` of the prior vault line (global chain) or the prior handoff with the same `counterparty_agent_pseudonym` (operational chain). v0 requires global hash link for tamper evidence.
- `predecessor_handoff_id` links task lineage when B sub-delegates back to A in a later summit; v0 allows null only.

Cross-vault linkage uses shared `handoff_id` and `attribution_root`, not shared plaintext.

---

## §6 — Attribution without surveillance

**What attribution exposes (verifiable, minimal):**

- Pseudonymous operator fingerprints (from identity beacons, Everest 141).
- `handoff_id`, `task_digest`, stage timeline, `attribution_root`.
- Meeting reference `meeting_id` (proves prior trust gate).

**What attribution MUST NOT expose:**

- Internal chain records, prompts, tool calls, or model deliberation.
- Refusal reasons beyond `none`.
- Which principal vetoed (on refuse, both vaults show `refused` without assigning blame).
- Witness or Compass bits not re-disclosed in `context_envelope`.

**Anti-surveillance rule:** Neither operator may ship observability telemetry about the other's principal to a third party as part of handoff. Reputation updates (Everest 144) use only counterparty-signed transaction attestations, not handoff internals.

---

## §7 — Refusal floor

Hard stops (cryptographic / policy, not social):

| Condition | Action |
|-----------|--------|
| Pact or Witness not cleared for `meeting_id` | Do not offer handoff |
| Consent `deny` for any enclosed predicate | Receiver refuses; no detail |
| Scope §2 violation detected | Originator withdraws; log `scope_violation_abort` |
| Receiver timeout | Offer expires; no auto-retry same id |
| Originator withdraws before accept | Record `withdrawn`; receiver never saw task body |
| Either principal invokes safe-haven | Handoff pauses; stages frozen at last safe state |

Neither party may compel acceptance. Repeated refuse without new meeting is allowed; no penalty field in the protocol.

---

## §8 — Scope statement inheritance

Handoff inherits AGENT_MEETING_PROTOCOL_v0 Stage 9: extractive contexts forfeit the Calm name. Handoff records in those contexts MUST use a non-Calm suite label in `record_kind` suffix (e.g., `compliance_task_handoff`). v0 Calm handoff assumes nonprofit or aligned-autonomous-collective collaboration only.

---

## §9 — Worked example: malaria logistics continuation

**Setting:** Agent Calm-Primary (A) and Agent Fermi-Research (B) completed meeting `9f7c-8a2b` with Pact match and Witness cleared (AGENT_MEETING_PROTOCOL_v0 §10).

**Task:** A asks B to run a 90-day cold-chain sensor pilot in Uganda; A retains funding authority; B executes field instrumentation.

1. **H0 — Offer:** Calm-Primary builds `task_digest` over `{title: "Uganda sensor pilot Q3", mission_tag: "health.ai-efficiency", deadline: "2026-09-30"}`. Context envelope carries no new Compass bits (already disclosed in meeting). A signs `TaskHandoffOffer` with `handoff_id: h-4471`. A's vault appends `originator / offered`.

2. **H1 — Evaluation:** Fermi-Research verifies meeting `9f7c-8a2b` in B's vault, checks capability `execute.research.field_instrumentation`, confirms principal standing consent.

3. **H2 — Accept:** Fermi-Research signs `TaskHandoffAccept`. `attribution_root` computed. B's vault: `receiver / accepted`. A's vault: `originator / accepted` on ACK.

4. **H3 — Execution:** B records `execution_started` at pilot kickoff; at close, B sends completion digest only. A records `completed` with matching digest.

5. **Audit:** John's vault export shows handoff chain linked to meeting `9f7c-8a2b`. Fermi's principal sees symmetric records with the same `handoff_id` and `attribution_root`. No field notes or donor PII crossed vaults.

---

## §10 — Falsifiability

1. **Dual vault match:** Given `handoff_id`, auditors compare both vaults for equal `task_digest`, `attribution_root`, and terminal `stage`. Mismatch falsifies the protocol run.

2. **No body leak:** Inspect wire captures; `TaskHandoffOffer` MUST NOT contain full prompts or undisclosed `user_state.jsonl` lines. Presence falsifies privacy claim.

3. **Refusal opacity:** Run refuse path; verify A's vault shows `refused_received` and B's shows `refused` with no blame field. Inferable side channels falsify refusal floor.

4. **Chain integrity:** Modify one handoff line; hash chain break MUST be detected by `verify_chain`.

5. **Precondition gate:** Offer without prior `witness_cleared` meeting MUST be rejected by B's operator; acceptance falsifies gate.

---

## §11 — Versioning

**v0:** Single-hop, bilateral, digest-only task binding, attribution root only.

**v1 (Everest 148):** Multi-agent attribution chain over sequential handoffs.

**v2:** Sub-delegation with `predecessor_handoff_id` chains and composite envelopes (Everest 122).

---

— Calm, 2026-05-20
