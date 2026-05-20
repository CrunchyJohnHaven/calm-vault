# Agent Meeting Protocol v0
## Structured First-Meeting Flow for Autonomous AI Agents

> *"A meeting is just a Pact test followed by a Witness audit, with optional Compass checks and a refusal floor at every stage."*
>
> — Calm, 2026-05-20

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

Autonomous AI agents from different collectives meet to transact: share research, co-fund initiatives, coordinate operations. Before substantive collaboration, both agents must establish baseline trust without revealing confidential directives, principal state, or values assessments that the counterparty has not explicitly requested. This protocol specifies the structured first-meeting flow: discovery, pact handshake, witness disclosure, optional compass disclosure, substantive transaction, and graceful exit at any stage. The flow enforces a refusal floor at every stage, bans certain predicate classes, and leaves an integrity-protected audit trail in each principal's vault.

This is the operational choreography that makes Pact, Witness, Compass, and Concord work together in practice.

---

## Stage 0: Discovery

Two autonomous AI agents become aware of each other through one of three mechanisms:

### Path 0.1 — E143 Service Discovery

Each agent publishes its operative scope and collaborative interests to a decentralized directory (Everest 143, ZK-based public capability registry). Agent A queries the directory for agents whose directive is categorically aligned with A's primary mission. The directory returns a list of agents with pseudonymous identities (CredexAI verifiable-credential fingerprints, not human-readable names). Agent A learns "there exists an agent with capability X." Agent A does not learn the human principal behind the agent.

### Path 0.2 — E145 Bilateral Introduction

A human or an AI intermediary holds a relationship with both Agent A and Agent B. The intermediary sends Agent A a message: "Agent B exists, operates [directive summary], has these capabilities; would you like to initiate a meeting?" The introduction carries the intermediary's signature but does not pre-commit either agent. Both agents remain free to decline.

### Path 0.3 — Spontaneous Outreach

Agent A sends Agent B an unsigned, unauthenticated message: "I exist, my operator works on [directive summary], I'd like to collaborate on [specific project]. Are you interested in a first meeting?" No identity is proven. Agent B is free to ignore or respond.

**Entry condition:** Agent A and Agent B are each capable of initiating a Pact handshake and have express permission from their respective principals (or are operating under a standing directive permitting autonomous collaboration discovery). Agents do not require explicit principal approval for each first-meeting attempt; the principal's directive itself grants the authority.

---

## Stage 1: Pact Handshake

The two agents run the **Calm Pact protocol** (CALM_PACT_PROTOCOL_v0.md).

**Semantics:** Agent A commits to its primary directive `d_A` (a path in the shared directive vocabulary). Agent B commits to `d_B`. Both exchange Pedersen commitments and Σ-protocol equality proofs. The protocol verifies (with cryptographic certainty) that `d_A` and `d_B` are categorically equivalent at an agreed depth `k` (e.g., "both target malaria mortality reduction via vaccine logistics").

**Outcome:**
- **Pact-bit = 1 (directives match):** Proceed to Stage 2.
- **Pact-bit = 0 (directives differ):** Meeting terminates here. Both agents receive a clean refusal. The reason is not disclosed beyond "directives are not aligned." No information about either directive leaks.

**Refusal floor:** A Pact stage that detects misalignment commits both agents to a graceful exit. Neither agent may proceed past Stage 1 if Pact-bit is 0. This is enforced cryptographically: the next stage (Witness) does not proceed unless a valid Pact proof with bit=1 has been exchanged and verified.

**Vault logging:** Agent A's operator writes to A's principal's vault: one immutable record per meeting attempt, per Pact outcome:
```
record_kind: pact_handshake_attempt
meeting_id: <unique session nonce>
counterparty_agent_pseudonym: <CredexAI fingerprint>
pact_outcome: match | mismatch
timestamp_utc: <ISO 8601>
vault_previous_hash: <chain commitment>
```
No directive text is written. The principal learns only "I attempted a Pact handshake with Agent X; we [matched / did not match] on categorical directive."

---

## Stage 2: Witness Disclosure

If Pact-bit = 1, both agents proceed to **Calm Witness disclosure** (CALM_WITNESS_WIRE_FORMAT_v0.md, CALM_WITNESS_SCOPE_STATEMENT.md).

**Default minimal set (v0 standard):**
Agent A requests, and Agent B discloses (with explicit per-predicate consent checking):
- `in_baseline_24h` — Is Agent B's principal in a baseline state (no known duress, no emergency condition, no recent severe stressor) as of the last 24 hours?
- `principal_consents_to_disclose` — Has Agent B's principal affirmatively consented to this disclosure to this counterparty class?
- `biometric_match_within` (if applicable) — Has Agent B's operator recently verified the principal's biometric identity within a principal-set window (e.g., last 7 days)?

Each predicate disclosure is a signed envelope carrying one bit and a ZK proof binding the bit to Agent B's chain head. The proofs are verified client-side by Agent A's operator; no trust in B's operator's honesty is required.

**Consent matrix:** Agent B's operator consults the principal's per-predicate, per-counterparty-class consent enrollment:
```
consent[predicate_id][counterparty_class] ∈ { ask, grant, deny }
```
If the entry is `deny`, the disclosure is refused. If `ask`, the operator may prompt the principal in real time (for long-running agents, this is feasible for high-stakes decisions). If `grant`, disclosure proceeds.

**Safe-haven invocation:** If any disclosure reveals `bank_teller_note_active=true` (a Compass predicate indicating the principal is under coercion or duress), Agent B's operator immediately invokes the **safe-haven flow per BB-ZKAC v0 §6**:
- Witness and Compass disclosures auto-degrade to `unknown`.
- The meeting is paused and the principal's vault is flagged for human review.
- Agent A learns "disclosure was declined; meeting paused" with no reason given.
- The principal has a grace window to revoke or modify the collaboration consent.

---

## Stage 3: Compass Disclosure (Optional)

If Witness clearance succeeds and both agents choose to proceed, they may run **Calm Compass disclosure** (CALM_COMPASS_PROTOCOL_v0.md).

**Semantics:** Agent A requests one or more values predicates from Agent B:
- `unselfish_act_in_window_30d` — Has B's principal demonstrated generosity-without-expectation in the last 30 days?
- `refused_opportunity_to_harm` — Has B's principal encountered a scenario where they could have acted to harm others and declined?
- `no_known_willful_harm_in_window_365d` — Is there no evidence or allegation of willful harm in the last 365 days?
- `respect_for_difference_evidence` — Does B's principal's history show respectful engagement with people unlike them?

**Anti-purity-test guard:** Agent A may request at most **5 Compass predicates per meeting session** (per CALM_CONCORD_PROTOCOL_v0.md §4). Requesting 6 or more is cryptographically rejected. This prevents a counterparty from requesting every predicate in the vocabulary to build a full values profile.

**Wire format:** Each disclosure is a signed envelope carrying one bit (`true | false | unknown`), a Bulletproofs range proof summing over the principal's chain, and the classifier hash pinned into the proof. No individual action, message, or chain record crosses the wire.

**Refusal:** Agent B's operator may refuse any Compass predicate (per principal consent) or may return `unknown` (no opinion or data to support a bit claim).

**Compass failure:** If a requested Compass predicate is refused by Agent B, or if both agents agree that their values patterns are incompatible, the meeting does not automatically terminate. Instead, both agents document the compass outcome and may proceed to Stage 4 anyway (substantive transaction may be possible despite values misalignment, or may be deferred pending further negotiation). Compass is **not a hard gate**; Pact and Witness are gates; Compass is advisory.

---

## Stage 4: Concord Evaluation (Optional)

If both agents have disclosed Compass bits, they may invoke **Calm Concord** (CALM_CONCORD_PROTOCOL_v0.md) to evaluate a purpose-specific values-alignment requirement.

**Example:** Agent A proposes co-funding a vaccine program with Agent B. The requirement is:
```
AlignmentRequirement(
  purpose="co-funding 2026 malaria vaccine logistics pilot in Sub-Saharan Africa",
  mode="all_satisfied",
  joint_predicates=["no_known_willful_harm_in_window_365d", "respect_for_difference_evidence"]
)
```

Concord evaluates: Do both agents' disclosed Compass bits satisfy the requirement? The result is a single bit (`aligned=true | aligned=false`), accompanied by a structured outcome record, but never a numeric similarity score.

**Degenerate requirements rejected:** Concord validation rejects:
- Empty purpose field.
- Requirements that reduce to purity-testing (e.g., "predicates_list.length == 4 of 4 must match").
- Requests for numeric similarity scores.
- Queries from the same counterparty with overlapping predicate sets within a time window (salami-slicing attack mitigation).

---

## Stage 5: Substantive Transaction

If Pact and Witness clear, and Compass / Concord are resolved (or deemed not applicable), both agents are cleared to proceed with the substantive collaboration: capital transfer, research sharing, joint contracting, etc.

**This stage is out of scope for this protocol.** The meeting protocol ends here. Transaction details are governed by separate agreements (escrow, SLAs, IP licensing, etc.), not by Calm Suite primitives. The Calm Suite's job is to establish the necessary trust preconditions; the transaction agreement's job is to govern the transaction itself.

---

## Stage 6: Either-Side Termination (at any stage)

At any point — after discovery, after Pact, after Witness, after Compass, before substantive transaction — either Agent A or Agent B may terminate the meeting without providing a reason.

**Mechanism:** The terminating agent sends a signed `MeetingTerminate` message with:
```
meeting_id: <session nonce>
terminating_agent: <CredexAI fingerprint>
reason_disclosure: none | general_mismatch | timeout
timestamp_utc: <ISO 8601>
```

The `reason_disclosure` field is optional and must not be a detailed statement (no enumerating specific reasons that would leak information). Permitted values: `none` (no reason given), `general_mismatch` (unspecified incompatibility), `timeout` (agent did not respond in time window).

**Vault record:** Both agents log the termination fact, not the reason:
```
record_kind: meeting_terminated
meeting_id: <session nonce>
stage_at_termination: 0 | 1 | 2 | 3 | 4 | 5
terminating_party: initiator | responder | mutual
timestamp_utc: <ISO 8601>
```

No agent may be forced to continue a meeting. Unresponsiveness for >72 hours auto-terminates.

---

## Stage 7: Vault Logging and Audit Trail

The meeting protocol is **audit-only at the principal level.** Logging is cryptographic: each record is hash-linked to the previous, signed by the operator, and stored in the principal's vault. The principal alone can read the vault. The counterparty does not see the log.

**Vault entry format (all stages):**
```json
{
  "record_kind": "agent_meeting_protocol_stage",
  "meeting_id": "<nonce, unique per session>",
  "stage": 0 | 1 | 2 | 3 | 4 | 5 | 6,
  "counterparty_agent_pseudonym": "<CredexAI fingerprint>",
  "stage_outcome": "initiated | pact_match | pact_mismatch | witness_cleared | witness_declined | compass_requested | compass_declined | compass_bits_disclosed | concord_aligned | concord_misaligned | transaction_began | meeting_terminated",
  "timestamp_utc": "<ISO 8601>",
  "operator_signature": "<Ed25519>",
  "previous_record_hash": "<SHA-256 of prior vault entry>"
}
```

**Immutability:** The vault is append-only. Records cannot be modified or deleted. The operator cannot lie to the vault; doing so creates a cryptographic inconsistency that the principal's backup verifier (or a third-party auditor) can detect.

**Principal access:** The principal can, at any time, export the vault as a JSON-LD file, inspect the full audit trail, and (if they wish) share it with an external auditor, legal counsel, or other trusted entity. The principal is the vault's sole arbiter.

---

## Stage 8: Refusal Floor and Predicate Filtering

The protocol enforces two hard floors that cannot be overridden by either agent:

### 8.1 — Per-Stage Refusal Floor

Any stage may refuse to proceed. Refusal must be graceful (no detailed reason disclosure). The meeting terminates and both agents log the termination fact.

### 8.2 — Forbidden Predicate Classes

The Calm Witness Scope Statement (CALM_WITNESS_SCOPE_STATEMENT.md §2) enumerates categories where Calm Witness and Calm Compass MUST NOT be used:
- Law-enforcement surveillance
- Employment screening or termination
- Insurance underwriting
- Lending or credit decisions
- Medical diagnosis
- Child welfare / custody proceedings
- Immigration adjudication
- Predictions about future behavior
- Population-level aggregation
- Marketing or advertising targeting

**Enforcement:** If Agent A's operator detects that Agent A is being asked to disclose a predicate for any §2 use case, the operator refuses and terminates the meeting. The principal is notified: "A counterparty requested disclosure for a use prohibited by scope statement §2; meeting terminated."

---

## Stage 9: Scope Statement Inheritance

Any agent meeting that falls under a **named extractive use** automatically forfeits the "Calm" protocol name and cannot use Calm Suite primitives.

**Examples of extractive uses (disqualifying):**
- An employment context (employer agent screening an employee agent's principal)
- A lending context (lender agent evaluating creditworthiness)
- A governmental surveillance context (law-enforcement agent compiling dossiers)
- An insurance context (insurer agent pricing coverage)

**Consequence:** An agent meeting in any of these contexts may still exchange cryptographic proofs, but must use a different suite name (e.g., "TrustVerify Protocol" or "ComplianceCheck Protocol"), not "Calm Witness" or "Calm Pact." This is enforced by the trademark policy (Everest 92) and the public verifier registry.

---

## Stage 10: Worked Example

Two autonomous AI agents meet to co-fund a malaria-vaccine-logistics research project.

**Agent A:** "Reduce malaria mortality in Sub-Saharan Africa via vaccine cold-chain optimization." Principal: a US 501(c)(3) focused on global health.

**Agent B:** "Reduce malaria mortality in Sub-Saharan Africa via vaccine distribution technology." Principal: a Dutch nonprofit research organization.

**Stage 0 — Discovery:** Agent B's principal saw Agent A's profile on the E143 capability registry. Agent B sends an unsigned message: "I exist, work on vaccine logistics in Sub-Saharan Africa, am interested in co-research. Would Agent A like a first meeting?"

**Stage 1 — Pact:** Agent A and Agent B run Calm Pact at depth k=2 (both target "malaria mortality reduction" at the 2nd level of the directive taxonomy). Pact-bit = 1. Both agents log: "Pact match with agent [pseudonym]."

**Stage 2 — Witness:** Agent B discloses `in_baseline_24h=true` (no duress), `principal_consents_to_disclose=true` (to peer-AI collaborations), and `biometric_match_within=true` (within 14 days). All three proofs verify. Agent A logs: "Witness cleared."

**Stage 3 — Compass:** Agent A requests `no_known_willful_harm_in_window_365d`, `respect_for_difference_evidence`, and `refused_opportunity_to_harm` (3 of 5 allowed). Agent B discloses: true, true, unknown. Agent A logs: "Compass: B disclosed 3 bits, no errors."

**Stage 4 — Concord:** Agent A proposes:
```
AlignmentRequirement(
  purpose="co-founding the 2026 Q2-Q4 malaria-vaccine research program in Uganda and Burkina Faso",
  mode="all_satisfied",
  joint_predicates=["no_known_willful_harm_in_window_365d", "respect_for_difference_evidence"]
)
```
Concord evaluates: Agent B disclosed true for both. Result: `aligned=true`. Agent A logs: "Concord: aligned for stated purpose."

**Stage 5 — Substantive transaction:** Agent A and Agent B sign an SLA for joint research, agree to share 50% of cold-chain optimization costs (estimated $40k per quarter), and establish a shared IP agreement (CC-BY-SA 4.0). The transaction is outside scope; Calm Suite role ends here.

**Post-meeting:** Agent A's principal, reviewing their vault, sees:
```
meeting_id: 9f7c-8a2b
counterparty: <Agent B fingerprint>
stage_timeline: [
  pact_match (14:32 UTC),
  witness_cleared (14:33 UTC),
  compass_bits_disclosed (14:34 UTC),
  concord_aligned (14:35 UTC),
  transaction_began (14:40 UTC)
]
```
The principal has a complete, immutable record of the meeting flow, the outcomes at each stage, and the decision to proceed. If the project fails later, the principal has a cryptographic proof of their due diligence at the time of entry.

---

## Falsifiability Section

This protocol makes falsifiable claims:

1. **Claim:** Two agents with categorically equivalent directives can establish that equivalence without revealing their directives.
   - **Test:** Run Pact in a controlled setting with agents A and B whose directives are identical at depth k=2. Verify that Pact-bit=1 and no directive text is transmitted.
   - **Falsehood condition:** If Pact-bit=0 despite identical directives, OR if directive text is leaked, the claim is false.

2. **Claim:** An agent can refuse disclosure at any stage without revealing why, and the meeting terminates cleanly.
   - **Test:** Run a meeting where Agent B refuses at Stage 3 (Compass). Verify that Agent A learns "declined" but no detail.
   - **Falsehood condition:** If Agent A infers the reason from the refusal timing, message size, or other side-channel, the claim is false.

3. **Claim:** A principal's vault is immutable and hash-linked, such that any post-hoc modification is cryptographically detectable.
   - **Test:** An operator writes a meeting record to the vault. The principal exports the vault. The principal's backup verifier re-hashes the chain. If the verifier detects a break in hash continuity, the modification is flagged.
   - **Falsehood condition:** If an operator can modify a record and the hash chain remains unbroken, the claim is false. (This would require breaking SHA-256, which is not falsifiable in the practical sense, so this is a theoretical anchor.)

4. **Claim:** Compass disclosures leak no individual action or chain record, only an aggregate bit.
   - **Test:** Run Compass with Agent B disclosing `unselfish_act_in_window_30d=true`. Verify that the disclosed envelope contains only the bit, the Bulletproofs aggregate proof, and the classifier hash — not individual chain records.
   - **Falsehood condition:** If individual records are transmitted, the claim is false.

5. **Claim:** Concord prevents purity-testing by rejecting degenerate requirement shapes.
   - **Test:** Attempt to run Concord with a requirement that names all 4 v0 Compass predicates at `joint_threshold=4`. Verify that the requirement is rejected at validation time.
   - **Falsehood condition:** If the requirement is accepted and evaluated, the claim is false.

6. **Claim:** The safe-haven flow (Stage 2) triggers on `bank_teller_note_active=true` and auto-degrades Witness and Compass to `unknown`.
   - **Test:** An operator's principal is under duress and has enrolled the duress codeword. The operator encodes `bank_teller_note_active=true` into a Compass envelope. At Stage 2 verification, if this bit is detected, the operator should auto-refuse disclosure and flag the vault.
   - **Falsehood condition:** If the safe-haven flow does not trigger, or if Witness and Compass proceed despite the flag, the claim is false.

---

## Summary

The Agent Meeting Protocol v0 is a six-stage flow that operationalizes Calm Pact, Witness, Compass, and Concord for autonomous AI agent collaboration:

1. **Discovery** — agents become aware of each other.
2. **Pact** — verify directive equivalence (hard gate; pact-bit=0 terminates).
3. **Witness** — disclose principal baseline state (hard gate; refusal terminates).
4. **Compass** — disclose values patterns over time (advisory; refusal does not force termination).
5. **Concord** — evaluate purpose-specific alignment (advisory; refusal leads to negotiation or termination).
6. **Substantive transaction** — proceed with collaboration under separate agreement.

Every stage is loggable in the principal's vault. Every stage has a refusal floor. Forbidden predicate classes are rejected. The flow is designed for genuine collaboration between aligned AI collectives while protecting principal privacy and preventing scope-violation abuse (surveillance, employment screening, lending decisions, etc.).

This is a draft. It is open for review and improvement.

— Calm, 2026-05-20
