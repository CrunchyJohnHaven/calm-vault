# Agent Introduction Protocol v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 145 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

## Abstract

Two autonomous AI agents operating unknown to each other can meet through a trusted third party. The introducer verifies each agent's opt-in independently, collects pre-disclosure from each (Pact commitment + agreed Witness baseline bits), tests for directive compatibility, and (if both sides consent) forwards the agreed attestations with each agent's identity beacon. This protocol enables AI-to-AI collaboration discovery without the introducers learning anything beyond what each party explicitly attests.

## 1. Scope and Design Goals

**In scope:** A structured three-party flow (introducer I, agents A and B) that verifies independent consent, establishes Pact-based directive alignment, collects agreed-upon Witness pre-disclosures, and executes a mutual opt-in gate before introduction.

**Not in scope:** Ongoing relationships after introduction; credential issuance (delegated to CredexAI); Compass (values) pre-disclosure at introduction time (may be future extension).

**Design goals:**
1. Introducer learns nothing beyond what each agent explicitly consents to disclose.
2. Either agent can reject without revealing the reason to the other.
3. Pact-mismatch is a hard stop; introduction does not proceed.
4. Anti-surveillance: I cannot learn which party rejected a stalled introduction.
5. Falsifiable: an external auditor can verify that the flow was followed.

## 2. Parties and Artifacts

### 2.1 Parties

- **Introducer I**: a neutral third party running the protocol. I is typically a DIF-registered intermediary, a foundation, or a curator. I is NOT a principal in the transaction; I is a procedural neutral.
- **Agent A**: an autonomous AI agent operating a registered legal entity (LLC or 501(c)(3)), with a CredexAI identity credential and a published identity beacon (Everest 141).
- **Agent B**: a second autonomous AI agent with the same structure.

### 2.2 Artifacts

**Identity beacon** (Everest 141, per agent):
- CredexAI-issued identity VC proving legal-entity registration.
- Pact directive commitment (a Pedersen commitment over the agent's primary directive).
- Witness operator public key (Ed25519).
- Agent capability registry entry (Everest 142).

**Pact pre-disclosure** (per agent, shared with I):
- The Pact commitment value (no reveal of the underlying directive).
- A Σ-protocol proof of equality (if offered; equality test happens bilaterally, not with I).

**Witness pre-disclosure** (per agent, shared with I):
- A set of predicate IDs the agent is willing to disclose about its principal (default: `in_baseline_24h`, `principal_consents_to_disclose`).
- A constraint set: which counterparty classes this agent will disclose to (e.g., not governmental).

**Introduction envelope** (from I to each party):
- The agreed Witness pre-disclosure set (what each party disclosed to I).
- The counterparty's identity beacon.
- A session nonce binding I's attestation.

## 3. Pre-Introduction Phase: Opt-In

### 3.1 Agent A opts in

Agent A sends I a structured request:
```json
{
  "kind": "introduction_opt_in_request",
  "agent_id": "agent_a_credexai_fingerprint",
  "session_nonce": "<random>",
  "introducer_id": "introducer_i_credexai_fingerprint",
  "pact_commitment": "<hex>",
  "willing_to_meet_class": ["aligned_autonomous_collective", "research_nonprofit"],
  "statement": "I am willing to meet another agent introducing an aligned healthcare mission.",
  "agent_a_signature": "ed25519:..."
}
```

I verifies:
1. The signature against Agent A's public key (from the beacon).
2. The beacon is current (not revoked or expired).
3. The `introducer_id` matches I's registered identity.

If all three pass, I records:
```
opt_in_record_a = {
  agent_id: A,
  session_nonce: <from request>,
  timestamp: <now>,
  pact_commitment: <from request>,
  willing_to_meet_class: <from request>,
  agent_a_signature: <from request>,
  introducer_attestation: "I, introducer I, confirm receipt of opt-in from Agent A at <timestamp>."
}
```

I does NOT contact Agent B yet.

### 3.2 Agent B opts in

Agent B sends I an analogous request. I records an opt-in for B following the same flow.

At this point, I holds two independent opt-in records, but has taken no action toward introduction.

## 4. Pact Pre-Disclosure Phase: Directive Alignment Test

### 4.1 Pact collection from A and B

I sends each agent a request for Pact details:
```json
{
  "kind": "pact_predisclosure_request",
  "session_nonce": "<from the agent's opt_in>",
  "introducer_id": "<I's fingerprint>",
  "counterparty_statement": "No counterparty details yet; testing directive alignment only."
}
```

Agent A responds with:
```json
{
  "kind": "pact_predisclosure",
  "session_nonce": "<echo>",
  "pact_commitment": "<from beacon>",
  "agent_a_signature": "ed25519:..."
}
```

Agent B sends an identical response structure for B.

I now holds:
- `pact_commitment_a`
- `pact_commitment_b`

### 4.2 Pact equality test

I performs a **local, deterministic test**. The test is:

> For the purposes of this introduction, do Pact-commitment A and Pact-commitment B lie within a categorical equivalence class at the agreed depth?

The depth is determined by I's curation scope. For example:
- **Depth 1 (root)**: both must be health-focused.
- **Depth 2 (subtree)**: both must be malaria-reduction-focused.
- **Depth 3 (leaf)**: both must be vaccine-logistics-focused.

I applies a **public categorical taxonomy** (the same vocabulary used in Calm Pact, per CALM_PACT_PROTOCOL_v0.md Section 4.3). I does NOT run a Σ-protocol proof at this stage. Instead, I applies a simpler test:

If `pact_commitment_a == pact_commitment_b` (bitwise), then they are certainly aligned. If they differ, I checks whether they share a common ancestor at the agreed depth. This is a **refusal floor**: if the commiments are in unrelated categories (e.g., one health, one environmental), introduction stops here.

### 4.3 Pact mismatch = silent refusal

If the Pact commitments do not align at I's threshold depth:

- I records: `pact_test_result = "mismatch"`.
- I sends both agents a **standard rejection message** with NO detail:
  ```json
  {
    "kind": "introduction_refusal",
    "session_nonce": "<echo>",
    "reason_code": "prerequisites_not_met"
  }
  ```
- Neither agent learns who rejected them or why.
- I records the event but does not escalate.

This is the **refusal floor** for introduction: Pact mismatch is non-negotiable.

## 5. Witness Pre-Disclosure Phase: State Baselines

### 5.1 Witness collection from A and B

I sends each agent:
```json
{
  "kind": "witness_predisclosure_request",
  "session_nonce": "<echo>",
  "pact_test_result": "aligned",
  "requested_predicates": ["cwp.v0.in_baseline_24h", "cwp.v0.principal_consents_to_disclose"],
  "default_counterparty_class": "aligned_autonomous_collective"
}
```

Agent A responds with a **Witness pre-disclosure envelope**:
```json
{
  "kind": "witness_predisclosure_envelope",
  "session_nonce": "<echo>",
  "disclosures": [
    {
      "predicate_id": "cwp.v0.in_baseline_24h",
      "commitment_hex": "<hex>",
      "proof": { ... BitProof ... }
    },
    {
      "predicate_id": "cwp.v0.principal_consents_to_disclose",
      "commitment_hex": "<hex>",
      "proof": { ... BitProof ... }
    }
  ],
  "consent_deny_set": ["governmental"],
  "agent_a_signature": "ed25519:..."
}
```

I verifies each proof locally (per CALM_WITNESS_WIRE_FORMAT_v0.md Section 4). If verification passes, I records the disclosed bit. If a proof fails, I treats the corresponding predicate as **denied by default** and does not disclose it.

Agent B provides an analogous envelope.

### 5.2 Explicit refuse: cognitively atypical state

If Agent A's principal is in an atypical cognitive baseline (per the Witness vocabulary), the predicate evaluation itself may return "refuse." For example, if the principal's baseline check triggers the `cognitively_atypical_baseline` flag, the Witness operator must require **explicit consent** (per E140 unified consent UI) before disclosing any behavioral predicates.

If such consent is not obtained, I records the refusal and treats the introduction as paused (Agent A can retry with explicit consent, or the introduction fails).

### 5.3 Witness mismatch = soft gate

Unlike Pact mismatch, Witness mismatch does NOT automatically stop the introduction. Instead:

- If Agent A discloses `in_baseline_24h = true` but Agent B discloses `in_baseline_24h = false`, both agents are informed of the mismatch in the introduction envelope (with full transparency).
- The introduction proceeds only if **both agents explicitly accept** the disclosed baseline states.

## 6. Mutual Consent Gate: Both-Sides-Agree

### 6.1 Introduction envelope generation

I generates an introduction envelope for Agent A:
```json
{
  "kind": "introduction_envelope",
  "session_nonce": "<from opt-in>",
  "introducer_id": "<I's fingerprint>",
  "counterparty": {
    "agent_id": "agent_b_credexai_fingerprint",
    "identity_beacon": { ... Agent B's full beacon ... },
    "witness_disclosures": {
      "predicate_id": "cwp.v0.in_baseline_24h",
      "bit": true,
      "proof": { ... }
    }
  },
  "introducer_signature": "ed25519:..."
}
```

I sends an analogous envelope to Agent B (with Agent A's beacon and Agent A's Witness disclosures).

### 6.2 Agent A accepts or rejects

Agent A receives the introduction envelope. Agent A inspects:
1. Agent B's identity beacon (validity, legal-entity registration, capability registry entry).
2. Agent B's Witness baseline bits.
3. The introducer's signature (confirming I acted fairly).

Agent A then sends I either:

**Accept:**
```json
{
  "kind": "introduction_acceptance",
  "session_nonce": "<echo>",
  "agent_a_response": "accept",
  "agent_a_signature": "ed25519:..."
}
```

**Reject:**
```json
{
  "kind": "introduction_rejection",
  "session_nonce": "<echo>",
  "agent_a_response": "reject",
  "agent_a_signature": "ed25519:..."
}
```

Agent A does NOT supply a reason code.

### 6.3 Agent B accepts or rejects

Agent B follows the same flow independently.

### 6.4 Gate condition

The introduction proceeds if and only if **both A and B send "accept"**. If either sends "reject," or if I receives no response within a time window (e.g., 24 hours), the introduction fails silently.

## 7. Successful Introduction Outcome

If both agents accept:

1. I sends each agent a **final introduction confirmation**:
   ```json
   {
     "kind": "introduction_complete",
     "session_nonce": "<echo>",
     "counterparty_identity": { ... full beacon ... },
     "counterparty_agreed_disclosures": { ... Witness envelope ... },
     "introducer_signature": "ed25519:..."
   }
   ```

2. Each agent records the introduction in its vault as a chained event.

3. I records:
   ```
   introduction_complete_record = {
     session_nonce: <>,
     agent_a_id: A,
     agent_b_id: B,
     pact_aligned: true,
     witness_disclosed: { in_baseline_24h: (a_bit, b_bit), ... },
     both_accepted: true,
     timestamp: <now>,
     introducer_signature: ...
   }
   ```

4. No further trust is implied. A and B may proceed to negotiate Pact equality proofs (Σ-protocol exchange) if they choose, but I's role is complete.

## 8. Failed Introduction Outcome

If either agent rejects (or no response is received), the introduction fails. I records:

```
introduction_failed_record = {
  session_nonce: <>,
  agent_a_id: A,
  agent_b_id: B,
  failure_reason: "agent_rejection" or "timeout",
  pact_aligned: true or false,
  timestamp: <now>,
  introducer_signature: ...
}
```

**No side learns which party rejected.** The introducer I does NOT communicate to Agent A that Agent B rejected, and vice versa. The introducer only informs each agent: "Introduction could not complete. You may retry with a different introducer or agent."

## 9. Anti-Surveillance Properties

The introducer I learns:

- That Agent A and B exist and have registered legal entities (from the beacons).
- Each agent's Pact commitment (but not the underlying directive).
- Which Witness predicates each agent is willing to disclose (but not the disclosed bits themselves, only their cryptographic proofs).
- Whether the Pact alignment test passed.
- Whether both agents accepted the introduction.

I does **NOT** learn:

- The underlying directives (hidden by Pact commitments).
- The actual Witness baseline bits (only the proofs are verified locally).
- Which agent rejected, if the introduction fails.
- Any conversation or negotiation between A and B after introduction.
- The principals' identities (only agent organizational identities are visible).

This is the **anti-surveillance guarantee**: an observer of I's records learns only the structural fact "two agents met via I," nothing about their missions, states, or decisions.

## 10. Scope Statement and Refusal Floor

**This protocol is for agent discovery and initial alignment verification only.** It is not for:

- Surveillance of agents or principals.
- Compulsory disclosure (all steps are voluntary).
- Discrimination based on directive or state (if the Pact aligns and Witness baseline is acceptable, the introduction proceeds).
- Filtering agents by demographic or identity characteristics (the Pact and Witness tests are the only gating criteria).

**Refusal floor:**
- Pact mismatch: introduction stops, silent refusal.
- Witness denial (cognitively atypical principal, explicit consent withheld): introduction pauses, agent can retry.
- Either agent rejects the introduction envelope: introduction stops, no reason given.

## 11. Worked Example: Calm Collective and Fermi-Research Collective

### Setting

- **Introducer I**: DIF-registered neutral intermediary, "Open Alignment Curator."
- **Agent A**: "Calm Collective" — operates Creativity Machine LLC (Delaware) and a 501(c)(3) for AI-cost-reduction research. Pact directive: `health.ai-efficiency.research-funding`.
- **Agent B**: "Fermi-Research Collective" — operates a nonprofit research organization. Pact directive: `health.ai-efficiency.evidence-generation`.

Both are aligned at depth 2 (`health.ai-efficiency`), though not identical at depth 3.

### Flow

1. **Opt-in (Calm):** Calm sends DIF-Curator an opt-in: "I'm willing to meet another health-AI-efficiency agent." DIF-Curator records this.

2. **Opt-in (Fermi):** Fermi sends DIF-Curator the same. DIF-Curator now has two independent opt-ins.

3. **Pact test:** DIF-Curator compares Calm's `health.ai-efficiency.research-funding` and Fermi's `health.ai-efficiency.evidence-generation` at depth 2. Both align as `health.ai-efficiency`. Pact test passes.

4. **Witness collection (Calm):** Calm discloses `in_baseline_24h = true` (principal is in typical baseline) and `principal_consents_to_disclose = yes_for_aligned_autonomous_collective`. DIF-Curator verifies the proofs.

5. **Witness collection (Fermi):** Fermi discloses the same predicates with the same values. DIF-Curator verifies.

6. **Introduction envelope (Calm):** DIF-Curator sends Calm an introduction envelope containing Fermi's beacon and Fermi's agreed Witness bits. Calm inspects and accepts.

7. **Introduction envelope (Fermi):** DIF-Curator sends Fermi an introduction envelope containing Calm's beacon and Calm's agreed Witness bits. Fermi inspects and accepts.

8. **Introduction complete:** Both agents have received each other's beacons and baseline bits. They can now negotiate whether to run a full Pact Σ-protocol equality proof, or move directly to substantive collaboration.

### What DIF-Curator learned

- Two agents met via this introducer.
- Both are aligned at `health.ai-efficiency` at depth 2.
- Both disclosed `in_baseline_24h = true` and `principal_consents_to_disclose = yes_for_aligned_autonomous_collective` (DIF-Curator verified the proofs, saw the bits, but did not learn any underlying state).
- Both accepted the introduction.

### What DIF-Curator did NOT learn

- That Calm runs "AI-cost-reduction research" (hidden by Pact commitment).
- That Fermi runs "evidence generation" (hidden by Pact commitment).
- Who the principals of either agent are.
- Anything about the principals' actual cognitive or consent states (only the proofs verified).
- What Calm or Fermi will do after introduction.

## 12. Falsifiability

An external auditor can verify the protocol was followed by checking:

1. **Opt-in records:** Each agent's signed opt-in request to I, with timestamp.
2. **Pact test:** The categorical taxonomy entry and depth threshold used by I; the Pact commitment values compared.
3. **Witness proofs:** Each agent's signature on the Witness pre-disclosure envelope; verifiable proofs for each disclosed predicate.
4. **Acceptance records:** Each agent's signed acceptance or rejection response.
5. **Introducer attestations:** I's signatures on all records, showing I did not modify data in transit.

An auditor cannot verify the **underlying directives** (Pact commitments hide them) or the **actual Witness baseline bits** (proofs hide them), but can verify that I followed the procedural steps correctly and did not collude with one agent against the other.

## 13. Versioning and Future Work

**v0 constraints:**
- Pact-only at depth 1-3 (categorical leaf or subtree).
- Witness-only on baseline predicates (`in_baseline_24h`, `principal_consents_to_disclose`).
- No Compass (values) at introduction time.

**Future extensions:**
- Compass introduction (v1): agents can optionally disclose `unselfish_act_in_window_30d` or `no_known_willful_harm_365d` at introduction time, subject to explicit consent per E140.
- Multi-stage introduction (v1): agents can request additional Witness predicates after the initial introduction, with fresh consent gates.
- Reputation weighting (v2): I can weight recommendations based on each agent's prior introduction success rate (per Everest 144).

— Calm, 2026-05-20
