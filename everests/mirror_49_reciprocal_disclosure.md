# Mirror Everest 49 — Reciprocal Disclosure (the Mirror Exchange)

**Phase XII — Mirror Disclosure Semantics.** *Prereq: Everest 42 (aligned-bit commitment), 46 (per-counterparty consent), 97 (Pact + Witness composition structure).*

*Acceptance:* the canonical two-party exchange where both principals' agents jointly compute alignment and both receive the same disclosure.

---

## 1. Overview

The Mirror exchange is the wire-level protocol two agents run to jointly establish whether two principals' values align — without either agent revealing individual value-bits, without a central authority, and with cryptographic guarantee that both parties learn equivalent information.

The protocol sits at Phase 3 of the composition stack (Everest 97 §1):
1. **Phase 1:** Calm Pact verifies directive equality.
2. **Phase 2:** Calm Witness establishes user-state attestation.
3. **Phase 3:** Calm Mirror (this everest) jointly computes values alignment.
4. **Phase 4:** Both agents record disclosure outcomes to their chains.

The Mirror exchange produces a *symmetric disclosure bundle*: both principals receive identical cryptographic evidence that their values either align or do not, across the shared vocabulary they both consent to evaluate.

---

## 2. Pre-Flight Checks (Both Sides Must Pass Before Exchange Begins)

Before any message is exchanged, both agents verify prerequisites:

### 2.1 Calm Pact Succeeded
- Both agents' Pact proofs (from Everest 97 Phase 1) verified.
- Directive equality is confirmed.
- If Pact failed, abort with reason `pact_failed`; zero Mirror protocol bytes transmitted.

### 2.2 Calm Witness Succeeded
- Both agents' Witness disclosure responses (Everest 97 Phase 2) verified.
- Each principal is in baseline state OR explicitly disclosed not-in-baseline with consent (bank-teller-note or equivalent).
- If Witness verification fails, abort with reason `witness_failed`; zero Mirror protocol bytes transmitted.

### 2.3 Consent Records Exist
- Agent A has an active `kind: consent.v0` record for (counterparty-class-of-B, predicate-set-requested, B's-principal-identity).
- Agent B has reciprocal consent record.
- Per-predicate consent bits are matched: if A withholds `unselfishness_evidence` (Everest 51), consent record explicitly encodes this.
- If consent is missing or expired, abort with reason `consent_not_found`; both agents log abort silently.

### 2.4 Vocabulary Intersection Computed (Everest 41)
- Both agents publish their value-vocabulary commitments from enrollment (Everest 21-25).
- Intersection is computed locally: `shared_vocab = A.vocabulary ∩ B.vocabulary`.
- Both agents independently compute the same shared_vocab set (deterministic given public commitments).
- If intersection is empty, abort with reason `no_shared_vocabulary`; no exchange occurs.

**Abort semantics:** Any pre-flight failure triggers silent abort. No partial disclosures, no error messages that reveal which side failed. Both agents log the abort reason internally but do not transmit it.

---

## 3. The Eight-Step Exchange Protocol

Once pre-flight checks pass, the exchange follows strict ordering:

### Step 1: A→B Predicate-Set Request

**Agent A sends:**
```json
{
  "message_type": "mirror_request",
  "session_id": "<session_id from Pact phase>",
  "requester_id": "<A's principal DID>",
  "requested_predicates": [
    "unselfishness_evidence",
    "tribal_neutrality_evidence",
    "respect_for_difference_evidence",
    "non_harm_evidence"
  ],
  "consent_reference": "<A's consent record hash>",
  "timestamp": "<ISO 8601>",
  "nonce_a": "<32-byte random nonce>"
}
```

**Validation (B's side):**
- `session_id` matches the ongoing session from Pact/Witness.
- `requested_predicates` ⊆ shared_vocab.
- `consent_reference` matches B's local copy of A's consent record (both sides hold symmetric consent records).
- Timestamp is within ±5 minutes of B's clock.

### Step 2: B→A Predicate-Set Acceptance, Counter-Proposal, or Decline

**Option 2a: Acceptance**
```json
{
  "message_type": "mirror_accept",
  "session_id": "<session_id>",
  "responder_id": "<B's principal DID>",
  "accepted_predicates": [
    "unselfishness_evidence",
    "tribal_neutrality_evidence",
    "respect_for_difference_evidence",
    "non_harm_evidence"
  ],
  "nonce_b": "<32-byte random nonce>",
  "timestamp": "<ISO 8601>",
  "consent_reference": "<B's consent record hash>"
}
```

**Option 2b: Counter-Proposal** (B wants to exclude a predicate)
```json
{
  "message_type": "mirror_counter_propose",
  "session_id": "<session_id>",
  "responder_id": "<B's principal DID>",
  "proposed_predicates": [
    "unselfishness_evidence",
    "respect_for_difference_evidence",
    "non_harm_evidence"
  ],
  "excluded_predicates": ["tribal_neutrality_evidence"],
  "reason_code": "withhold_unilateral",
  "nonce_b": "<32-byte random nonce>",
  "timestamp": "<ISO 8601>"
}
```

**Option 2c: Decline**
```json
{
  "message_type": "mirror_decline",
  "session_id": "<session_id>",
  "responder_id": "<B's principal DID>",
  "reason_code": "withhold_all | consent_revoked | no_alignment_expected",
  "timestamp": "<ISO 8601>"
}
```

**On Decline:** Exchange terminates cleanly. Both agents log the decline and record `kind: mirror_disclosure_declined.v0` to their chains (Everest 75). No partial disclosure occurs.

### Step 3: Agreement on Predicate Set

If Step 2 was counter-proposal, A responds with either:
- **Mirror-accept-counter** (agrees to B's narrower set)
- **Mirror-decline** (walks away)

Once both sides agree on a predicate set `P_agreed`, proceed to Step 4. If no agreement is reached within 2 rounds of proposal/counter-proposal, the exchange aborts with reason `negotiation_timeout`.

### Step 4a: Both Compute Per-Predicate Bits Locally

Each agent independently evaluates their principal's value-predicates:

**Agent A computes:**
For each `p ∈ P_agreed`:
```
bit_a[p] = evaluate_predicate(p, A.behavior_evidence_chain)
           ∈ {true, false, unknown}
```

**Agent B computes:**
For each `p ∈ P_agreed`:
```
bit_b[p] = evaluate_predicate(p, B.behavior_evidence_chain)
           ∈ {true, false, unknown}
```

Each agent commits to their bit vector:
```
commitment_a = Pedersen_commit(bit_a, randomness_a)
commitment_b = Pedersen_commit(bit_b, randomness_b)
```

Per Everest 42, neither agent reveals `bit_a` or `bit_b` individually. Only commitments are transmitted.

### Step 4b: Exchange Commitments

**A→B:**
```json
{
  "message_type": "mirror_bit_commitment",
  "session_id": "<session_id>",
  "committer_id": "<A's principal DID>",
  "commitment_a": "<Pedersen commitment (hex)>",
  "commitment_freshness_proof": "<ZK proof that commitment uses recent evidence>",
  "chain_head_a": "<hash of A's behavior-evidence chain head>",
  "timestamp": "<ISO 8601>",
  "signature_a": "<operator-signed>"
}
```

**B→A:** (symmetric)

Both agents verify that the Pedersen commitment is well-formed and the freshness proof is valid (Everest 67).

### Step 5: Two-Party Secure Computation (Everest 58)

Both agents invoke a two-party MPC (garbled circuits or SPDZ, per Everest 57 selection):

```
For each p ∈ P_agreed:
  MPC_INPUT_A: bit_a[p], randomness_a
  MPC_INPUT_B: bit_b[p], randomness_b
  
  MPC_COMPUTATION:
    aligned[p] := (bit_a[p] == bit_b[p]) AND (bit_a[p] == true)
    (only if both bits are *true* do they align; false-to-false is "not aligned")
  
  MPC_OUTPUT_BOTH:
    both agents receive aligned[p]
    neither agent learns the other's bit_a[p] or bit_b[p]
```

The MPC protocol ensures:
- **Correctness:** The output `aligned[p]` is the honest evaluation over the committed bits.
- **Privacy:** Each agent learns only the alignment bits, not the other's individual bits.
- **Symmetry:** Both agents receive identical outputs.

The MPC transcript is kept in memory; it is not serialized to the wire. Only the outputs and proofs of correctness (Step 6) are exchanged.

### Step 6: Produce ZK Proofs Binding MPC Contributions to Chain Heads

**Each agent produces a bundle:**

```json
{
  "message_type": "mirror_mpc_proof_bundle",
  "session_id": "<session_id>",
  "prover_id": "<principal DID>",
  "mpc_contribution_proof": {
    "kind": "mpc_correctness_proof",
    "zkp_circuit": "align_bit_batch_ristretto",
    "committed_bits": "<commitment_a (or _b)>",
    "aligned_bits_openings": "[true, false, true, unknown, ...]",
    "proof": "<ZK proof that committed bits → aligned outputs>"
  },
  "chain_binding_proof": {
    "kind": "behavior_evidence_chain_anchor",
    "chain_head": "<hash of principal's behavior-evidence chain at evaluation time>",
    "chain_head_timestamp": "<ISO 8601>",
    "anchor_proof": "<proof binding chain_head to a transparency log (e.g., Sigsum)>"
  },
  "consent_binding_proof": {
    "kind": "consent_record_binding",
    "consent_record_hash": "<hash of consent record>",
    "consent_window": "[start_timestamp, end_timestamp]",
    "consent_signature": "<principal's signature on consent record>"
  },
  "operator_signature": "<operator's VC-backed signature>",
  "timestamp": "<ISO 8601>"
}
```

Per Everest 61, the proof binds both principals' chain heads to the disclosure, preventing post-hoc chain-swapping.

### Step 7: Exchange and Verify Bundles

**A sends bundle_A to B; B sends bundle_B to A.**

Each agent runs an independent clean-room verifier:

```
verify_bundle(bundle, expected_prover_id, session_id):
  1. Check bundle.session_id == session_id
  2. Check operator_signature is valid (VC credential check)
  3. Verify mpc_contribution_proof (ZK proof of correctness)
  4. Verify chain_binding_proof (chain_head is immutable post-disclosure)
  5. Verify consent_binding_proof (principal consented to this exchange)
  6. Check timestamp is within ±5 minutes of local clock
  7. If all checks pass: return (bundle, verification_success)
     else: return (bundle, verification_failed)
```

**On verification failure:** The agent does NOT abort unilaterally. Instead, it records the verification failure (Step 8) and returns status `verification_failed` locally. The failed disclosure is logged but does not prevent future exchanges with the counterparty.

### Step 8: Both Record Disclosure Event to Their Chains

Regardless of outcome, both agents record to their behavior-evidence chains (an extension of `user_state.jsonl` per Everest 11):

**On successful verification:**
```json
{
  "kind": "mirror_disclosure.v0",
  "timestamp": "<ISO 8601>",
  "session_id": "<session_id>",
  "counterparty_principal_id": "<B's DID (from A's perspective)>",
  "counterparty_class": "peer_ai_collective | employer | partner | journalist | ideologue | ...",
  "predicate_set": ["unselfishness_evidence", "tribal_neutrality_evidence", ...],
  "alignment_bits": {
    "unselfishness_evidence": true,
    "tribal_neutrality_evidence": false,
    "respect_for_difference_evidence": true,
    "non_harm_evidence": true
  },
  "bundle_hash_a": "<hash of A's bundle received>",
  "bundle_hash_b": "<hash of B's bundle received>",
  "verification_status": "both_verified",
  "operation": "disclosure_completed",
  "chain_head_at_disclosure": "<hash of chain before this record>"
}
```

**On verification failure (either side):**
```json
{
  "kind": "mirror_disclosure.v0",
  "timestamp": "<ISO 8601>",
  "session_id": "<session_id>",
  "counterparty_principal_id": "<B's DID>",
  "predicate_set": ["unselfishness_evidence", ...],
  "verification_status": "verification_failed",
  "failed_proof": "mpc_contribution_proof | chain_binding_proof | consent_binding_proof",
  "operation": "disclosure_rejected",
  "reason": "cryptographic verification failed"
}
```

**On abort (pre-flight or during exchange):**
```json
{
  "kind": "mirror_disclosure.v0",
  "timestamp": "<ISO 8601>",
  "session_id": "<session_id>",
  "counterparty_principal_id": "<B's DID>",
  "operation": "disclosure_aborted",
  "abort_reason": "pact_failed | witness_failed | consent_not_found | no_shared_vocabulary | negotiation_timeout | decline_received",
  "chain_head_at_abort": "<hash of chain before this record>"
}
```

Each record is signed by the agent's operator identity and hash-chained to the previous record in the principal's chain.

---

## 4. Wire Format (JSON Envelope)

All messages conform to this outer envelope:

```json
{
  "version": "mirror.v0",
  "session_id": "<Fiat-Shamir-bound session ID from Pact phase>",
  "message_id": "<UUID>",
  "sender_id": "<sender's principal DID or operator identity>",
  "message_type": "mirror_request | mirror_accept | mirror_counter_propose | mirror_decline | mirror_bit_commitment | mirror_mpc_proof_bundle",
  "payload": { ... },
  "timestamp": "<ISO 8601>",
  "signature": "<sender's operator VC signature over (version, session_id, message_id, payload, timestamp)>"
}
```

**Transport:** HTTPS + DIDComm (DidKey), with operator mutual TLS authentication (operator identity cert is the TLS DN). Replay protection via (session_id, message_id, timestamp).

---

## 5. Fail Semantics Matrix

| Scenario | Outcome | Chain Record | Exchange Bytes |
|----------|---------|--------------|-----------------|
| Pre-flight: Pact failed | Abort, reason=pact_failed | `kind: mirror_disclosure` / abort | 0 bytes post-pact |
| Pre-flight: Witness failed | Abort, reason=witness_failed | `kind: mirror_disclosure` / abort | 0 bytes post-witness |
| Pre-flight: Consent missing | Abort, reason=consent_not_found | Logged internally, not chained | 0 bytes |
| Pre-flight: No shared vocab | Abort, reason=no_shared_vocabulary | `kind: mirror_disclosure` / abort | 0 bytes |
| Step 2: Counter-proposal, then decline | Decline, reason=negotiation_timeout | `kind: mirror_disclosure` / declined | Request + counter-proposal only |
| Step 4: MPC fails (corrupt input) | Abort (both sides) | `kind: mirror_disclosure` / abort | Commitments + abort signal |
| Step 6: Proof verification fails | Rejection (local, not transmitted) | `kind: mirror_disclosure` / verification_failed | Bundle + rejection (logged, not sent) |
| Step 8: Either verifier rejects | No partial trust | `kind: mirror_disclosure` / verification_failed | Full exchange, both record reject |
| Happy path: Both verify | Disclosure recorded | `kind: mirror_disclosure` / disclosure_completed | Full 8-step exchange |

**Key invariant:** Neither agent ever transmits a rejection signal to the other after bundling is complete. Both record the outcome locally and cease interaction.

---

## 6. Symmetry Guarantee

The protocol enforces cryptographic symmetry:

1. **Identical outputs:** Both agents compute identical `aligned[]` bits via MPC (no information asymmetry).
2. **Identical bundles:** Each agent receives the other's full proof bundle. Verification is deterministic given public parameters.
3. **Identical chain records:** Each agent records the same `session_id`, `predicate_set`, `alignment_bits` (if verified) or same `verification_failed` reason.
4. **No side channels:** The MPC architecture (Everest 58) is chosen to prevent timing/communication leakage of individual bits.

If A learns that B has `unselfishness_evidence=true`, then B is guaranteed to also learn that A has `unselfishness_evidence=true` (or that the evaluation revealed `unknown`). No asymmetric information leakage is possible.

---

## 7. Withhold-Any-Bit Integration (Everest 51)

If principal A unilaterally withholds the `unselfishness_evidence` predicate:

1. **Consent record:** A's consent record for this exchange explicitly marks `unselfishness_evidence: withheld`.
2. **Step 1:** A requests only the remaining predicates: `["tribal_neutrality_evidence", "respect_for_difference_evidence", ...]`.
3. **Step 3:** If B accepts the narrower set, the exchange proceeds over that set.
4. **Alignment computation:** The withheld predicate does not appear in the alignment bits.
5. **Chain record:** The `predicate_set` in the mirror_disclosure record shows only the agreed predicates. B's chain record shows the same `predicate_set`.

**Withhold opacity:** B learns only that `unselfishness_evidence` was not evaluated. B does NOT learn whether A withheld it unilaterally or whether A lacked the predicate in their enrolled vocabulary. This is enforced by having both reasons produce identical protocol behavior.

---

## 8. Stealth Disclosure Integration (Everest 54)

If principal A's behavior-evidence chain contains a `kind: safety_trigger.v0` record (e.g., coercion, duress), the Mirror exchange surfaces this to B even without explicit consent:

1. **During Step 4a:** A's evaluator checks A's chain for active `safety_trigger.v0` records.
2. **If triggered:** A includes a `safety_trigger_active` flag in the MPC bundle (Step 5).
3. **B's verifier (Step 7):** B's clean-room verifier checks for the flag and surfaces it in the disclosure record:
```json
{
  "kind": "mirror_disclosure.v0",
  "...": "...",
  "safety_trigger_active": true,
  "safety_trigger_kind": "coercion_suspected",
  "chain_head_safety_record": "<hash linking to safety_trigger record>"
}
```
4. **Policy layer:** B's operator (not the Mirror protocol) decides whether to abort, escalate, or proceed with restricted actions (per Everest 53).

The protocol itself does not enforce the policy; it surfaces the signal and lets the operator's policy layer decide.

---

## 9. Restricted-Action-Set Handoff (Everest 53)

If either principal's Witness disclosure indicates not-in-baseline (Everest 97 Phase 3), the Mirror exchange still proceeds but gates the scope of actions the alignment bits can authorize:

1. **From Pact phase:** Both agents agreed on a `restricted_action_set` (e.g., "single-signature approval only, no fund movements").
2. **Disclosure record:** The mirror_disclosure record includes:
```json
{
  "action_set_applied": "full | restricted",
  "action_set_scope": {
    "restricted_reason": "witness_not_in_baseline",
    "authorized_actions": ["joint_commitment_signing", "research_collaboration"],
    "denied_actions": ["unilateral_fund_movement", "external_party_signaling"]
  }
}
```
3. **Cross-protocol:** Mirror does not enforce action restrictions; it records them. The operator's action layer enforces the scope.

---

## 10. Acceptance Tests

### T-M49.1: Happy Path (Bilateral Full Disclosure)

**Setup:** Both principals in baseline, consent on full predicate set, directives equal, Pact verified, Witness verified.

**Execution:**
- Both agents exchange requests and accept.
- Both compute their bits locally.
- Both commit and exchange commitments.
- MPC computes alignment bits: `[true, true, false, true]` (for the four example predicates).
- Both agents produce and exchange proof bundles.
- Both verifiers pass all checks.
- Both record `kind: mirror_disclosure` / `verification_status: both_verified` with alignment_bits.

**Expected:** Both principals' chains record identical alignment results. No asymmetry in what each learns.

### T-M49.2: One-Side Decline

**Setup:** A requests disclosure. B declines (reason: "withhold_all").

**Execution:**
- A sends mirror_request (Step 1).
- B responds with mirror_decline (Step 2c).
- Exchange terminates.
- Both agents record `kind: mirror_disclosure` / `operation: disclosure_declined` in their chains.

**Expected:** Neither agent transmits partial disclosure. Session ends cleanly. B's consent record is not advanced; A respects the decline and does not retry in this session.

### T-M49.3: Pre-Flight Pact-Fail Abort

**Setup:** Pact phase failed (directives not equal). Mirror exchange is not invoked.

**Execution:**
- Pre-flight check 2.1 fails: Pact verification returned false.
- Agent aborts immediately with reason `pact_failed`.
- Zero bytes of any Mirror protocol message are transmitted.
- Both agents record `kind: mirror_disclosure` / `operation: disclosure_aborted` / `abort_reason: pact_failed`.

**Expected:** Witness phase is never reached. Information does not leak across the Pact abort boundary.

### T-M49.4: Symmetry (Both Sides Learn Equivalent Info)

**Setup:** Happy path bilateral disclosure (T-M49.1).

**Assertion:** For every `aligned[p]` bit in A's chain record, B's chain record contains the identical bit. The alignment results are byte-for-byte symmetric.

**Verification:** Third party retrieves both chains and computes hash(alignment_bits_A) == hash(alignment_bits_B).

**Expected:** True (symmetric by MPC construction).

### T-M49.5: Withhold Opacity (Withhold-Which-Bit Not Leaked)

**Setup:** A withholds `unselfishness_evidence` (reason unknown to B: either unilateral withhold or A doesn't have the predicate enrolled).

**Assertion:** B's disclosure record shows `predicate_set` = `[tribal_neutrality_evidence, respect_for_difference_evidence, non_harm_evidence]`. B cannot distinguish whether A withheld unilaterally or lacks the predicate in their vocabulary.

**Verification:** Both scenarios (withhold vs. missing) produce identical protocol flow from B's perspective.

**Expected:** True (per Everest 51 opacity).

### T-M49.6: Chain-Record Correctness Post-Exchange

**Setup:** Happy path (T-M49.1).

**Assertions:**
- Both `kind: mirror_disclosure` records have identical `session_id`, `predicate_set`, `alignment_bits`, `counterparty_principal_id`.
- Both records are properly hash-chained (each record.chain_head_at_disclosure == previous record.hash).
- Both operator signatures are valid.
- Timestamp skew between A and B's records is ≤ 5 seconds.

**Verification:** Parse both chains, extract the disclosure record, verify all invariants.

**Expected:** All pass.

---

## 11. Composition with Related Everests

**Everest 41 (Pairwise Alignment Computation):** Vocabulary intersection is precomputed here; Mirror 49 uses the intersection as the maximum feasible predicate set.

**Everest 42 (Aligned-Bit Commitment Scheme):** The Pedersen commitment scheme that prevents bit-revelation is invoked in Step 4b.

**Everest 46 (Per-Counterparty Consent):** Consent records must exist and match before pre-flight passes.

**Everest 51 (Withhold-Any-Bit):** Step 1 request can exclude predicates; B can counter-propose exclusions in Step 2; protocol ensures no revelation of which side withheld.

**Everest 53 (Restricted-Action-Set):** The outcome of Mirror disclosure is gated by action-set scope negotiated in Pact phase (Everest 97).

**Everest 54 (Stealth Disclosure):** Safety triggers override consent and surface to counterparty during Step 5.

**Everest 58 (Secure Computation of Intersection Bits):** The MPC primitive in Step 5.

**Everest 61 (Cross-Principal Binding Proof):** Chain-head binding in Step 6 prevents post-hoc chain-swapping.

**Everest 97 (Composition with Calm Pact + Witness):** Mirror 49 is Phase 3 of the two-handshake; Pact failure (Phase 1) aborts Mirror pre-flight.

---

## 12. Open Questions for v1

1. **MPC framework selection:** Everest 57 must choose between garbled circuits (lower latency, larger communication) vs. SPDZ (higher latency, lower communication). This affects Step 5 performance and p95 bounds (Everest 92).

2. **Withhold-reason opacity:** Can we hide the reason for a counter-proposal exclusion (e.g., "B excluded X for privacy" vs. "B excluded X because their principal withheld unilaterally")? Current protocol produces identical behavior; may need additional ZK machinery in v1 to prove opacity.

3. **Multi-round negotiation:** Current protocol allows up to 2 rounds (Step 2 counter-proposal + A's response). Should v1 allow N-round negotiation? Risk: complexity explosion; benefit: fine-grained predicate negotiation.

4. **Cross-cultural value predicates:** The four v0 predicates (unselfishness, tribal-neutrality, respect-for-difference, non-harm) are Western-centric. Do alignment bits computed over these predicates fairly represent alignment in non-Western cultural contexts? Everest 71 (cross-cultural value taxonomy) must inform v1 predicate expansion.

5. **Growth-bit inclusion rule (Everest 34):** Should Mirror 49 enforce that any disclosure including `non_harm_evidence` must also offer `growth_arc_evidence` if B requests it? Current design allows per-bit withholding; normative rule enforcement may require protocol-level gates in v1.

6. **Partial-agreement disclosure:** If A and B negotiate down to 2 predicates from an original 4, but only 1 aligns, is the disclosure meaningful? Should v1 require a minimum aligned-predicate threshold (e.g., ≥2 aligned) to record a positive disclosure?

---

## 13. Sign-Off

— Calm, 2026-05-20
