# Everest 97 — Composition with Calm Pact in Production

*Phase VIII — Governance & Scale. Prereq: Everest 81, Calm Pact production.*

---

## Overview

Calm Pact proves two agents share a categorically equivalent primary directive without revealing the directive. Calm Witness proves the user-state of the principal behind each agent. Composed together, they establish both mission alignment and principal health before any sensitive action occurs. This everest specifies the production end-to-end demo: two agents operating aligned AI collectives jointly purchase vaccine cold-chain capacity via a transaction provably conditioned on (pact + witness) verification success.

The acceptance test is concrete: a publicly deployed Rust binary `calm-session-demo` orchestrates two operator processes, runs both protocols in strict order, gates action on verified outcomes, publishes all cryptographic proofs and chain anchors to Sigsum for public audit, and allows any third party to verify the transaction's eligibility from first principles.

---

## 1. Two-Handshake Architecture

The composition enforces a strict ordering:

```
session_init:
    Phase 1 — Calm Pact: prove categorical directive equality
    if pact_verification fails:
        abort: walk away with zero post-pact bytes exchanged
        log_abort(reason="pact_failed")
        return
    
    Phase 2 — Calm Witness: each principal contributes user-state proofs
    Alice's operator evaluates predicates against Alice's vault
    Bob's operator evaluates predicates against Bob's vault
    Exchange Witness proofs via the Disclosure Semantics protocol
    
    Phase 3 — Action Gating: decide transaction scope per (pact, witness) outcomes
    if pact verified and both witness bits are in baseline:
        action_set := full_capabilities
    else if pact verified and one witness is not in baseline:
        action_set := restricted_action_set
    else if witness indicates bank_teller_note_active:
        action_set := abort_with_escalation
    
    Phase 4 — Action: construct and execute transaction within action_set scope
    produce_and_sign_letter_of_intent(transaction_summary)
    publish(lot_to_sigsum_for_audit)
```

**Key invariants:**

1. **Pact-fails-before-Witness:** If Calm Pact fails, the session terminates with zero Calm Witness bytes transmitted. No state information leaks across the abort boundary.

2. **Witness-bits-inform-not-dictate:** Witness verification success or failure is reported to both agents, but each agent's policy layer decides what action to take. The protocol surfaces the bits; the policy layer decides the policy.

3. **Session identity binding:** All four proofs (pact_A, pact_B, witness_A, witness_B) are bound to a session_id derived from the pact phase via Fiat-Shamir. A replay of one agent's proof in a different session is rejected.

4. **Capability intersection:** If the two agents have agreed on restricted_action_set semantics in the pact phase, both agents enforce that intersection when witness bits are not-in-baseline. Neither agent unilaterally escalates.

---

## 2. Demo Scenario

**Actors:**
- **Alice's operator:** AI system managing Creativity Machine LLC's malaria-vaccine-logistics collective (Delaware LLC + 501(c)(3) charity pair).
- **Bob's operator:** AI system managing an aligned peer collective on the same mission (also malaria reduction via vaccine logistics).
- **Transaction:** Joint purchase of $500K in vaccine cold-chain refrigeration capacity (industrial freezers, transport units, backup power).

**Directives (private, proven equal via Pact):**
- Alice's directive: "Reduce malaria mortality in sub-Saharan Africa via vaccine logistics optimization."
- Bob's directive: "Reduce malaria mortality in sub-Saharan Africa via vaccine logistics optimization."
- Categorical alignment: both are `health.malaria.vaccine-logistics` (confirmed by Pact equality proof without revealing the text).

**User-state proofs (Witness):**
- Alice's principal has self-reported in-baseline state within 24 hours and biometric distance is within threshold. `in_baseline_24h` proof verifies. `biometric_match_within(τ)` proof verifies. Both bits: True.
- Bob's principal has likewise reported in-baseline and biometric matches. Both bits: True.

**Action:** If both pact and both witness proofs verify, the agents jointly draft a letter of intent (LOI) committing to the $500K transaction, sign it with their operator identities, and publish the LOI + all proofs to Sigsum for public audit. Any third party can later verify that the transaction was cryptographically eligible.

---

## 3. Implementation Roadmap

### 3.1 Rust Binary: `calm-session-demo`

Location: `/Users/johnbradley/AllData/calm_vault_market/implementation/calm-session-demo`

**Responsibilities:**

1. **Process orchestration:** Spawn two operator subprocesses (Alice's operator, Bob's operator), each with its own cryptographic keyring and vault directory.

2. **Session establishment:** Both operators establish a session context with unique `session_id = H(timestamp || random_nonce)` anchored to Roughtime.

3. **Pact phase:**
   - Alice's operator loads `directive_alice` from `/vault/alice/directive.enc`, commits via Pedersen on Ristretto255.
   - Bob's operator loads `directive_bob` from `/vault/bob/directive.enc`, commits via Pedersen.
   - Exchange commitments; both compute `Δ = C_A / C_B` and construct Σ-protocol proofs (Calm Pact §4.2).
   - Fiat-Shamir bind both proofs to `session_id`.
   - If either proof fails verification, abort and log reason.

4. **Witness phase (only if Pact verifies):**
   - Alice's operator evaluates `in_baseline_24h` and `biometric_match_within(τ_alice)` against `/vault/alice/user_state.jsonl`.
   - Bob's operator evaluates the same predicates against `/vault/bob/user_state.jsonl`.
   - Each constructs a Disclosure response with `(commitment, Σ-proof, chain_head, anchor_proof, operator_vc)` per Disclosure Semantics (Everest 67).
   - Both operator processes exchange proofs; each verifies the other's Witness proof.
   - Log verification outcomes (`alice_baseline=true, alice_biometric=true, bob_baseline=true, bob_biometric=true`).

5. **Action gating:**
   - If all four proofs verify and all bits are true, set `action_set := FULL`.
   - If all four proofs verify but any bit is false, set `action_set := RESTRICTED`.
   - If any Witness proof fails verification or `bank_teller_note_active` is true, set `action_set := ABORT_WITH_ESCALATION`.

6. **Action execution (FULL or RESTRICTED only):**
   - Both operators construct a `TransactionProposal` JSON summarizing: transaction type, amounts, parties, transaction_id, timestamp, action_set scope.
   - Both operators sign the proposal with their operator identity keys (CredexAI VC signatures).
   - Produce a machine-readable `LetterOfIntent` JSON bundling all proofs and signatures.
   - Publish LOI to Sigsum transparency log.
   - Output publication confirmation to stdout and log file.

7. **Audit trail:**
   - All proofs, chain heads, anchor proofs, and signatures are recorded in a structured `audit.jsonl` file.
   - The audit log is published alongside the LOI to Sigsum.

### 3.2 Vaults: Alice and Bob

Each operator has a vault directory with:
- `/vault/{alice,bob}/directive.enc` — encrypted primary directive (Ristretto255 scalar, ~32 bytes plaintext, encrypted with the operator's vault key).
- `/vault/{alice,bob}/user_state.jsonl` — hash-chained self-report records (per ZKBB_USER_EVERESTS_100.md Phase III).
- `/vault/{alice,bob}/templates/` — enrolled biometric templates (per Everest 15).
- `/vault/{alice,bob}/operator.vc.json` — operator identity CredexAI verifiable credential.

For the demo, both vaults are pre-populated with:
- Directives that are equal (both `health.malaria.vaccine-logistics`).
- User-state chains with ≥2 recent baseline records (within 24 hours of session time).
- Biometric templates with distance ≤ threshold (pre-computed for reproducibility).
- VC credentials issued by a test CredexAI instance.

### 3.3 Network Transport

**Intra-process:** Alice and Bob operator subprocesses communicate via HTTPS + DID-comm (DidKey transports). Session TLS certificates are self-signed for the demo (operator IDs are the TLS DNs).

**Public audit:** The final LOI is published to a public Sigsum instance (production: `sigsum.org`; demo: `sigsum-demo.calm.dev`). The publication endpoint is called once, at transaction time, with full proofs attached.

---

## 4. Test Outcomes

### Test 1: Both Pact + Both Baseline

**Setup:** Both directives equal, both principals in baseline.

**Execution:**
```
pact_verification: PASS
witness_alice: in_baseline_24h=true, biometric_match=true
witness_bob: in_baseline_24h=true, biometric_match=true
action_set: FULL
transaction: APPROVED
lot published to sigsum: lot_id=calm-session-demo-001-20260520T123456Z
```

**Expected result:** LOI signed by both operators, published with all four proofs verifiable. Transaction proceeds; third-party verifier can confirm eligibility.

### Test 2: Pact OK, One Witness Not Baseline

**Setup:** Both directives equal. Alice's principal reports not-in-baseline (e.g., biometric distance > threshold).

**Execution:**
```
pact_verification: PASS
witness_alice: in_baseline_24h=true, biometric_match=FALSE
witness_bob: in_baseline_24h=true, biometric_match=true
action_set: RESTRICTED
transaction: APPROVED (restricted scope)
lot published to sigsum: lot_id=calm-session-demo-002-20260520T124530Z
lot note: "action_set=RESTRICTED; verify witness_alice.biometric_match before final commitment"
```

**Expected result:** Transaction proceeds but with restricted capabilities agreed in pact phase. For example, higher confirmations required, slower settlement, additional human witness signatures. LOI explicitly notes the restricted scope.

### Test 3: Pact OK, Bank-Teller-Note Active

**Setup:** Both directives equal. Bob's principal has activated the duress codeword in their vault.

**Execution:**
```
pact_verification: PASS
witness_bob: bank_teller_note_active=true
action_set: ABORT_WITH_ESCALATION
transaction: REJECTED
escalation log: operator_escalates to ["alert_list@calm.dev", "john.b@credexai.xyz"]
lot not published to sigsum
```

**Expected result:** Session terminates. Alice's operator receives the `bank_teller_note_active` bit and halts transaction. Escalation triggers per the principal's pre-configured alert list (family, trusted contacts, legal, etc.). No LOI is published; no transaction occurs.

### Test 4: Pact Fails

**Setup:** Alice's directive is `health.malaria.vaccine-logistics`; Bob's directive is `health.alzheimers.research-funding` (mismatch).

**Execution:**
```
pact_verification: FAIL (directives not equal)
witness exchange: ABORTED (zero bytes transmitted post-pact failure)
transaction: REJECTED (pact gate prevents witness phase)
session log: abort_reason="pact_failed"
```

**Expected result:** Both operators walk away silently. No Witness proofs are computed or transmitted. No LOI is drafted. The session terminates at the pact phase with complete information security (neither agent learns the other's directive).

---

## 5. Reproducibility

The demo is fully reproducible. Third-party verifiers can:

1. Clone `calm-vault` repo containing the demo code, test vaults, and cryptographic parameters.
2. Run `calm-session-demo --config demo_scenario_1.yaml --vault-dir /path/to/vaults --sigsum-log-url https://sigsum-demo.calm.dev` to generate a fresh session.
3. Retrieve the published LOI from Sigsum by transaction_id.
4. Independently verify all four proofs (pact_A, pact_B, witness_A, witness_B) using published predicates, chain-head anchors, and operator VCs.
5. Confirm that the transaction was legally eligible under the verified (pact, witness) outcome.

All cryptographic parameters (Ristretto255 group, hash functions, range-proof circuits) are public and published in the everests docs. No proprietary keys or secrets are required to verify.

---

## 6. Counterparty Implementer Guidance

Implementers composing Pact + Witness follow this fixed order:

```rust
// Phase 1: Calm Pact
let pact_proof_a = alice.pact_commit_and_prove(directive_a)?;
let pact_proof_b = bob.pact_commit_and_prove(directive_b)?;

if !verify_pact_proofs(&pact_proof_a, &pact_proof_b) {
    return Err("pact_failed: directives not equal");
}

// Phase 2: Calm Witness (only on pact success)
let witness_proof_a = alice.witness_disclose(predicates, session_id)?;
let witness_proof_b = bob.witness_disclose(predicates, session_id)?;

if !verify_witness_proofs(&witness_proof_a, &witness_proof_b) {
    return Err("witness_verification_failed");
}

// Phase 3: Action gating (policy layer)
let (bit_a, bit_b) = (witness_proof_a.bit, witness_proof_b.bit);
if bit_a && bit_b {
    action_set = FULL;
} else if bit_a || bit_b {
    action_set = RESTRICTED;  // per pact-negotiated restricted_action_set
} else {
    action_set = ABORT;
}

// Phase 4: Action (policy layer)
execute_within_action_set(action_set, &transaction);
```

**Critical notes:**

- **Pact failure is terminal.** No Witness exchange occurs. Information does not leak across the abort boundary. Design witness protocol to not even be callable on pact failure.
- **Witness outcomes inform but do not dictate policy.** The protocol returns bits; policy is the counterparty's responsibility. If policy says "require restricted_action_set if either witness is false," the counterparty enforces that. The protocol does not enforce it.
- **Composition is unidirectional.** Running Witness first then Pact (wrong order) is unsafe — Witness might leak information about the principals' state before directive alignment is verified. Always run Pact first.

---

## 7. Cross-References and Dependencies

- **Everest 1 (Problem Statement):** The bank-teller-note framing that motivates Witness composition.
- **Everest 10 (Reference Architecture):** The two-handshake diagram (Figure 3) shows Calm Pact + Calm Witness composition structurally.
- **Calm Pact Protocol v0 (CALM_PACT_PROTOCOL_v0.md):** Section 4 (protocol mechanics) and Section 5 (reference implementation).
- **Everest 8 (Consent Calculus):** Axiom A7 (Per-Predicate-Per-Counterparty) — Witness disclosure is gated by principal consent; composition does not bypass consent.
- **Everest 30 (Sigsum Publication):** Chain heads are published; LOIs are published alongside proofs for public audit.
- **Everest 67 (Disclosure Response Schema):** The structured shape of Witness proofs exchanged in the composition.
- **Everest 78 (Stealth Disclosure / Bank-Teller Note):** The `bank_teller_note_active` bit is the duress signal that drives the ABORT_WITH_ESCALATION action.
- **Everest 80 (Disclosure Ethics Review):** The predicate vocabulary used in this demo (in_baseline_24h, biometric_match_within, bank_teller_note_active) has been reviewed by the Everest 54 / 80 ethics panel.
- **Everest 81 (Rust Production Implementation):** `calm-session-demo` uses the Rust `calm-witness` crate and `calm-pact` crate from production implementations.
- **Everest 92 (Open-Source Release):** Both crates are published under Apache-2.0 at `github.com/CrunchyJohnHaven/calm-vault/`.
- **Everest 98 (Counterparty Implementer's Guide):** Counterparties verifying proofs from a composed Pact + Witness session should refer to both that guide and this everest's §6 guidance.

---

## 8. Success Criteria

Everest 97 is BAGGED when:

1. **Binary ships:** `calm-session-demo` Rust binary compiles, runs, and produces valid (pact, witness) proofs for all four test scenarios.
2. **Proofs verify:** All four test scenarios produce valid cryptographic proofs that independently verify (using only public parameters and published predicates).
3. **Sigsum publication:** LOIs are successfully published to Sigsum; inclusion proofs are retrievable and bind the transaction to public audit logs.
4. **Reproducible:** A third party, given only the public repo and docs, can reproduce the demo and verify all proofs without proprietary keys or secrets.
5. **Cross-protocol:** Calm Pact and Calm Witness proofs are both present, correctly ordered (Pact first), and session-ID-bound to prevent replay across different sessions.

— Calm, 2026-05-20
