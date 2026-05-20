# Everest 97 — Four-Handshake Protocol Composition: Pact · Witness · Compass · Concord
**Production End-to-End Specification (DESIGN-BAGGED)**

*Phase XXIV — Governance & Scale. Prerequisite: Everests 30, 44b, 81, 103, 139, 144, 172, 289, 303 · Calm Pact v0.1 · Calm Witness v0 · Calm Compass v0 · Calm Concord v0.*

---

## Header

**Protocol:** Calm Umbrella Four-Handshake Composition  
**Version:** 1.0 (locked 2026-05-20)  
**Cryptography:** Ristretto255 (prime-order group from Curve25519); Pedersen commitments; Σ-protocols; Bulletproofs; BBS-2023 signatures (Everest 64 pending).  
**Transport:** HTTPS + DID-comm (DidKey); Sigsum transparency anchoring; Roughtime verifiable clock.  
**Acceptance gates:** T-E97.1 through T-E97.7 (§5).  
**Licensed:** Apache-2.0. Repository: `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-composition`.  
**Authors:** Calm (operating for John Bradley, Creativity Machine LLC).  

---

## Phase XXIV — Overview: Why Four Handshakes, Not Two

The 2-handshake model (Everest 97 prior, Pact → Witness) proved:
1. **Directive alignment** (Calm Pact): mission equivalence without revealing the mission.
2. **Principal state** (Calm Witness): baseline status without revealing biometrics or history.

These are necessary but insufficient for deep collaboration — specifically, for collaborations where counterparties need confidence that principals share values-compatible behavior *beyond* the current session. A principal can be in baseline and mission-aligned but historically untrustworthy. Conversely, a principal with clean history but currently unstable state should be handled with care.

The four-handshake adds two phases:

3. **Values alignment** (Calm Compass §1): principal-authored behavioral pattern evidence over a chained history. Does this principal historically treat people with dignity? Cooperate across difference? Avoid harm? The counterparty learns a single bit per predicate, nothing more.
4. **Purpose-specific alignment** (Calm Concord §1): given both principals' Compass envelopes, do they satisfy a named, purpose-specific requirement (e.g., "both principals must demonstrate no-known-willful-harm for this joint-funding collaboration")? Response: a single bit, never a similarity score. Anti-purity-test gates refuse degenerate requirement shapes.

**Why four?** Because failure at any gate aborts cleanly with zero downstream information leakage, and because real cooperation requires four independent proofs:
- **Pact:** "we want the same thing."
- **Witness:** "we are both well right now."
- **Compass:** "we have both behaved decently over time."
- **Concord:** "we are decently aligned for *this specific thing* we're about to do together."

Skip any phase, and you either over-trust (skipping Compass makes you vulnerable to a principal with hidden history) or over-restrict (skipping Pact means you collaborate with agents whose directives you've never verified).

---

## Prerequisites & Scope Statement

**Strict prerequisites:** This everest depends on:
- Everest 81 (Rust production implementation of Pact).
- Everest 103 (Calm Pact + Calm Witness composition endpoint).
- Everest 139 (Calm Compass envelope construction).
- Everest 144 (Calm Witness + Calm Compass composition).
- Everest 172 (Calm Compass predicate evaluation).
- Everest 289 (Calm Concord requirement validation).
- Everest 303 (Calm Concord evaluator).

All four protocols (Pact, Witness, Compass, Concord) must be complete to v0 before this spec's implementation begins.

**Scope:** This everest specifies the **wire-level protocol** by which two operator processes orchestrate all four handshakes in strict order, bind all proofs to a single `session_id`, defend against cross-protocol replay, and gate transaction execution on **all four** verification outcomes. It does NOT specify the individual protocol mechanics (those live in their own protocol documents and everests); it specifies the **sequencing, ordering, and composition glue**.

**What is EXCLUDED:**
- Individual protocol security proofs. (Delegate to Pact, Witness, Compass, Concord v0 docs.)
- Policy-layer decision logic. (Each principal decides what to do if a handshake fails; this spec documents what the protocol reports, not what the policy engine decides.)
- Non-Calm protocols (e.g., OIDC, OAuth, mTLS). (The composition assumes both operators already have CredexAI identity credentials; provisioning credentials is upstream.)
- Post-quantum migration. (Everest 96 / Phase IX covers PQ; composition uses Ristretto255 until Everest 96 completes.)

---

## 1. Strict Ordering: Each Phase Must Complete Before the Next Starts

The composition enforces a **total order** on the four phases. No parallelization. Any failure at any phase aborts the entire session with zero downstream bytes.

```
Session initialization:
├─ Phase 1: CALM PACT (mutual directive equality)
│  ├─ if FAIL: abort with reason="pact_failed"
│  │            zero witness/compass/concord bytes exchanged
│  │            return to caller with attestation failure
│  └─ if PASS: derive session_id_v1 via Fiat-Shamir
│
├─ Phase 2: CALM WITNESS (principal state baseline)
│  ├─ if FAIL: abort with reason="witness_failed"
│  │            zero compass/concord bytes exchanged
│  │            return outcome bit and freshness anchor
│  └─ if PASS: derive session_id_v2 via Fiat-Shamir(session_id_v1, witness bits)
│
├─ Phase 3: CALM COMPASS (values predicates disclosed)
│  ├─ if FAIL: abort with reason="compass_eval_failed" or "compass_refused"
│  │            zero concord bytes exchanged
│  │            return outcome to caller (principal may not have enrolled compass)
│  └─ if PASS: derive session_id_v3 via Fiat-Shamir(session_id_v2, compass bits)
│
├─ Phase 4: CALM CONCORD (purpose-specific alignment check)
│  ├─ if FAIL: outcome is "requirement not met for this purpose"
│  │            agents learn the structured failure, may retry with different purpose
│  │            no abort signal; this is designed to fail gracefully
│  └─ if PASS: derive session_id_final via Fiat-Shamir(session_id_v3, concord bit)
│
└─ Action execution gated by (Phase 1 + Phase 2 + Phase 3 + Phase 4) outcome
   Actions execute only if all predecessors have verified successfully.
```

**Invariant I1 — Pact-is-First:** Calm Pact must complete and verify before any Witness, Compass, or Concord bytes are computed or transmitted. If Pact fails, the session terminates immediately; no state information from either principal leaks.

**Invariant I2 — Witness-is-Second:** Calm Witness proofs are computed only if Pact verified. If Witness fails, Compass and Concord are not invoked.

**Invariant I3 — Compass-is-Third:** Calm Compass proofs are computed only if both Pact and Witness verified. Compass failure does not abort the session but gates Concord from executing.

**Invariant I4 — Concord-is-Fourth:** Calm Concord is invoked only if Pact, Witness, and Compass all succeeded or were explicitly skipped by principal consent. Concord failure does not abort the session; it reports "requirement not satisfied for this purpose."

---

## 2. Abort Semantics: Strict Information Quarantine at Each Boundary

Failure at any phase terminates all downstream phases with **zero leakage** across the abort boundary.

### 2.1 Pact Failure

```
if verify_pact(proof_a, proof_b) == FAIL:
    session_state := PACT_FAILED
    witness_state := UNEXECUTED
    compass_state := UNEXECUTED
    concord_state := UNEXECUTED
    
    response:
        {
          "session_id": session_id_v1,
          "phase": "pact",
          "result": "FAILED",
          "abort_reason": "directive_equality_check_failed",
          "witness_bytes_exchanged": 0,
          "compass_bytes_exchanged": 0,
          "concord_bytes_exchanged": 0
        }
    
    neither principal learns:
        - the other's directive (even which domain)
        - the other's directive depth (vaccine logistics vs. malaria vs. health)
        - any subsequent state or values information
    
    both operators log: abort_phase="pact", timestamp, session_id
    session terminates with no published proofs or transactions.
```

**Cryptographic guarantee:** Calm Pact's zero-knowledge property ensures that a failed proof reveals only the bit "directives differ," with probability of false negative < 2^-128.

### 2.2 Witness Failure

```
if verify_witness(proof_a, proof_b) == FAIL:
    session_state := WITNESS_FAILED
    compass_state := UNEXECUTED  (if compass was not already begun)
    concord_state := UNEXECUTED
    
    response:
        {
          "session_id": session_id_v2,
          "phase": "witness",
          "result": "FAILED",
          "abort_reason": one of:
              "proof_verification_failed" |
              "freshness_anchor_invalid" |
              "biometric_binding_failed" |
              "consent_record_missing" |
              "bank_teller_note_active",
          "compass_bytes_exchanged": 0,
          "concord_bytes_exchanged": 0
        }
    
    neither principal learns:
        - the other's biometric data
        - the other's self-report history
        - the other's consent records
        - any values information (compass, concord)
```

**Cryptographic guarantee:** Calm Witness binds the proof to a public transparency-log anchor; subversion is detectable post hoc. Bank-teller-note activation is wire-indistinguishable from baseline state evaluation failure.

### 2.3 Compass Failure (Graceful Degradation)

Unlike Pact and Witness failures, Compass failure does **not abort the entire session** — it signals "principal was not enrolled in Compass" or "principal refused disclosure to this counterparty class." The agents may proceed with Pact + Witness only, or Pact + Witness + Concord-without-Compass-inputs, depending on their policy.

```
if compass_eval(principal_a_vault) == NOT_ENROLLED or REFUSED:
    session_state := PACT_OK, WITNESS_OK, COMPASS_SKIPPED
    concord_state := CONDITIONAL (can execute if requirement doesn't require compass bits)
    
    response:
        {
          "session_id": session_id_v3,
          "phase": "compass",
          "result": "SKIPPED",
          "reason": "not_enrolled" | "principal_refused",
          "concord_runnable": true_if_concord_requirement_is_compass_independent
        }
    
    no compass bytes were exchanged.
    agents may choose to:
        - proceed with pact + witness only
        - invoke concord with a requirement that does not name compass predicates
        - abort the session anyway (policy decision)
```

**Rationale:** Compass enrollment is optional in v0. A principal may never enroll Compass, or may withdraw consent for a specific counterparty class. Compass failure should not prevent Pact + Witness collaboration when a counterparty doesn't require Compass inputs.

### 2.4 Concord Failure (Structured Outcome)

Concord failure is **not an abort**, but a structured "requirement not satisfied" result. Agents learn the failure reason at an auditable level of detail (not "your values are bad" but "your requirement R specified X and you provided Y").

```
if compute_alignment(envelope_a, envelope_b, requirement) == NOT_MET:
    session_state := PACT_OK, WITNESS_OK, COMPASS_OK, CONCORD_NOT_MET
    
    response:
        {
          "session_id": session_id_final,
          "phase": "concord",
          "result": "REQUIREMENT_NOT_MET",
          "requirement_id": requirement.id,
          "requirement_purpose": requirement.purpose,
          "bits_required": [predicate_list],
          "bits_actual_a": {predicate: bit_value, ...},
          "bits_actual_b": {predicate: bit_value, ...},
          "mode": requirement.mode,
          "outcome": false,
          "reason": "asymmetric_requirement_A_failed" | "joint_threshold_unsatisfied" | ...
        }
    
    agents learn:
        - which specific requirement failed (not "values bad," but which mode + which predicates)
        - the reason (the predicate list is not hidden; the requirement was public)
        - which principal(s) did not satisfy which predicate
    
    agents DO NOT learn:
        - compass predicates not named in the requirement
        - how close they came (if requirement was "any_satisfied" and 3 of 4 predicates were met, agents don't learn "3 of 4")
        - demographic inference from bits (cardinality guards prevent score-inference)
    
    agents may:
        - retry concord with a different requirement
        - retry concord with a different purpose
        - proceed without concord gate (policy decision)
        - abort the session (policy decision)
```

**Anti-purity-test guard:** Concord results are structured so that a counterparty cannot use repeated failures to infer values details the principal did not disclose. See Concord §4.

---

## 3. Session_ID Binding: One ID Per Session, Derived Incrementally

All four phases contribute to a single cryptographic **session identifier** that binds all proofs to one session and prevents cross-phase replay.

```
session_id_v0 := DERIVE_SESSION_ID(
    timestamp_from_roughtime,
    initiator_identity,
    responder_identity,
    nonce_from_initiator,
    nonce_from_responder
)

Phase 1 (Pact):
    pact_proof_a := construct_pact_proof(directive_a, session_id_v0)
    pact_proof_b := construct_pact_proof(directive_b, session_id_v0)
    session_id_v1 := FIAT_SHAMIR(session_id_v0, pact_proof_a, pact_proof_b)

Phase 2 (Witness) [if Pact verified]:
    witness_proof_a := construct_witness_proof(
        predicates=["in_baseline_24h", "biometric_match_within(τ_a)"],
        vault=vault_a,
        session_id=session_id_v1
    )
    witness_proof_b := construct_witness_proof(
        predicates=["in_baseline_24h", "biometric_match_within(τ_b)"],
        vault=vault_b,
        session_id=session_id_v1
    )
    (bit_a, bit_b) := verify_witness_proofs(witness_proof_a, witness_proof_b)
    session_id_v2 := FIAT_SHAMIR(session_id_v1, witness_proof_a, witness_proof_b)

Phase 3 (Compass) [if Witness verified]:
    compass_envelope_a := construct_compass_envelope(
        vaults=vault_a,
        predicates=["unselfish_disposition", "cross_tribal_engagement", "respects_difference", "no_evidence_of_willful_harm"],
        session_id=session_id_v2
    )
    compass_envelope_b := construct_compass_envelope(
        vaults=vault_b,
        predicates=["unselfish_disposition", "cross_tribal_engagement", "respects_difference", "no_evidence_of_willful_harm"],
        session_id=session_id_v2
    )
    session_id_v3 := FIAT_SHAMIR(session_id_v2, compass_envelope_a, compass_envelope_b)

Phase 4 (Concord) [if Compass evaluated]:
    requirement := {
        purpose: "co-fund Q4 2026 vaccine-logistics pilot in sub-Saharan Africa",
        mode: "all_satisfied",
        predicates: ["no_evidence_of_willful_harm"],
        ...
    }
    result := compute_alignment(
        envelope_a=compass_envelope_a,
        envelope_b=compass_envelope_b,
        requirement=requirement,
        session_id=session_id_v3
    )
    session_id_final := FIAT_SHAMIR(session_id_v3, requirement, result)

Final session record:
    {
      "session_id_final": session_id_final,
      "session_id_timeline": [session_id_v0, session_id_v1, session_id_v2, session_id_v3, session_id_final],
      "pact_verified": bool,
      "witness_verified": bool,
      "witness_bits": (bit_a, bit_b),
      "compass_enrolled": bool,
      "compass_bits": {predicate: bit_value, ...},
      "concord_requirement": requirement.id,
      "concord_result": bool,
      "timestamp": roughtime_timestamp,
      "anchor_proof": sigsum_inclusion_proof
    }
```

**Invariant I5 — Session Linearity:** `session_id_final` is deterministically derived from all prior phases. Replaying a single phase's proof in a different session will fail verification because `session_id` does not match.

**Invariant I6 — Ordered Derivation:** Each phase's session_id depends on the prior phase's Fiat-Shamir output. Phase 2 cannot be verified with Phase 1's session_id; Phase 3 cannot be verified with Phase 2's session_id.

---

## 4. Cross-Protocol Replay Defense

An attacker who captures a valid Calm Pact proof from session S1 cannot reuse it in session S2.

### 4.1 Intra-Session Replay

```
Session S1:
    session_id_v1 := H(S1_timestamp, S1_nonce, ...)
    pact_proof_s1 := pact_proof bound to session_id_v1
    [pact_proof_s1 is valid]

Attacker attempt: Reuse pact_proof_s1 in session S2:
    session_id_v1_s2 := H(S2_timestamp, S2_nonce, ...) ≠ session_id_v1
    verify_pact(pact_proof_s1, session_id_v1_s2) == FAIL
    (proof was bound to session_id_v1, not session_id_v1_s2)

Defense: All Σ-protocol proofs in Pact are bound to session_id via Fiat-Shamir
         hash of (session_id || other_proof_material). Changing session_id breaks
         the hash and invalidates the proof.
```

### 4.2 Cross-Phase Replay (Witness reused as Pact)

```
Attacker attempt: Use a Witness proof where Pact is expected:
    [witness_proof is a valid proof of in_baseline_24h]
    [but pact_phase_handler expects Pedersen commitment + Σ-equality-proof]
    
    pact_phase_handler.verify(witness_proof) == TYPE_MISMATCH
    (witness proof is structurally incompatible with pact verification logic)

Defense: Each phase has a distinct proof type:
    - Pact: Pedersen commitments on Ristretto255 + Σ-equality
    - Witness: Commitments on chain-head + biometric distance + Σ-range-proof
    - Compass: Chain hydration + aggregated Bulletproofs
    - Concord: Structured outcome + requirement validation
    
    Proof types are not interchangeable. Cross-phase injection fails at type check.
```

### 4.3 Session Fixation (Attacker Controls Session_ID)

```
Standard HTTPS + DID-comm mutual TLS:
    Both operators exchange certificates at session_init.
    TLS channel is integrity-protected; attacker cannot modify nonce in flight.
    Both operators independently derive session_id from honest randomness.
    If attacker tries to fix session_id to a known value, one operator detects
    the TLS certificate mismatch and aborts.

Additional defense: session_id includes signed operator credentials
    session_id := H(
        timestamp_from_roughtime,
        SIGN(initiator_vc, timestamp || nonce_initiator),
        SIGN(responder_vc, timestamp || nonce_responder),
        ...
    )
    Operator credentials are issued by CredexAI and are verifiable.
    Attacker cannot forge a signature without the private key.
```

---

## 5. Wire-Format Envelope JSON: All Four Stages

The composition exchanges a single JSON envelope that accumulates proofs from each phase.

### 5.1 Session Initialization Request

```json
{
  "session_request": {
    "session_id_v0": "hex(sha256(timestamp || nonce_a || nonce_b || ...))",
    "timestamp_roughtime": "2026-05-20T14:32:15Z",
    "initiator": {
      "operator_id": "urn:credexai:operator:calm-creativity-machine-v1",
      "operator_vc": {credexai_vc_jwt}
    },
    "responder_identity_hint": "urn:credexai:operator:peer-collective-xyz",
    "phases_requested": ["pact", "witness", "compass", "concord"],
    "compass_predicates": [
      "calm-compass/predicate/v0/unselfish_disposition",
      "calm-compass/predicate/v0/cross_tribal_engagement",
      "calm-compass/predicate/v0/respects_difference",
      "calm-compass/predicate/v0/no_evidence_of_willful_harm"
    ],
    "concord_requirement": {
      "id": "req_20260520_vaccine_logistics_pilot",
      "purpose": "co-fund Q4 2026 vaccine-logistics pilot in sub-Saharan Africa",
      "mode": "all_satisfied",
      "predicates": ["calm-compass/predicate/v0/no_evidence_of_willful_harm"],
      "role_a": "funder",
      "role_b": "implementer"
    }
  }
}
```

### 5.2 Phase 1 (Pact) Envelope

```json
{
  "session_id_v1": "hex(sha256(...session_id_v0, pact_proof_a, pact_proof_b))",
  "phase_1_pact": {
    "initiator": {
      "commitment": "hex(point on Ristretto255: C_a = g^{d_a} * h^{r_a})",
      "proof": {
        "type": "schnorr_equality_dlog",
        "c": "hex(fiat_shamir_challenge(session_id_v0 || C_a || C_b))",
        "z": "hex(scalar: z = k + c * (d_a - d_b))",
        "binding_session_id": "hex(session_id_v0)"
      },
      "operator_signature": {sig_over_commitment_and_proof}
    },
    "responder": {
      "commitment": "hex(point on Ristretto255: C_b = g^{d_b} * h^{r_b})",
      "proof": {
        "type": "schnorr_equality_dlog",
        "c": "hex(fiat_shamir_challenge(session_id_v0 || C_a || C_b))",
        "z": "hex(scalar: z = k + c * (d_b - d_a))",
        "binding_session_id": "hex(session_id_v0)"
      },
      "operator_signature": {sig_over_commitment_and_proof}
    },
    "verification_result": "PASS" | "FAIL",
    "abort_if_fail": true
  }
}
```

### 5.3 Phase 2 (Witness) Envelope (if Phase 1 PASS)

```json
{
  "session_id_v2": "hex(sha256(...session_id_v1, witness_proof_a, witness_proof_b))",
  "phase_2_witness": {
    "initiator": {
      "predicates": ["in_baseline_24h", "biometric_match_within(0.15)"],
      "commitment": "hex(Com(in_baseline_24h=true; ρ_a1))",
      "chain_head": {
        "record_hash": "hex(sha256(last_user_state_record))",
        "prev_hash": "hex(...)",
        "chain_length": 42
      },
      "anchor_proof": {
        "transparency_log": "sigsum.org",
        "inclusion_proof": "hex(sigsum_merkle_path)",
        "timestamp_anchor": "2026-05-20T14:31:00Z"
      },
      "biometric_binding": {
        "template_id": "hex(sha256(enrolled_handwriting_template))",
        "distance_commitment": "hex(Com(distance_value; ρ_biometric))"
      },
      "proof": {
        "type": "sigma_protocol_range_proof",
        "statement": "in_baseline_24h predicate evaluates to true",
        "binding_session_id": "hex(session_id_v1)"
      },
      "consent_record": {
        "predicate_id": "in_baseline_24h",
        "counterparty_class": "malaria-vaccine-logistics-collective",
        "expires": "2026-06-20T14:32:15Z"
      },
      "operator_signature": {sig_over_commitment_proof_chain_head}
    },
    "responder": {
      [same structure as initiator]
    },
    "verification_result": "PASS" | "FAIL",
    "bits": {
      "initiator_in_baseline_24h": true,
      "initiator_biometric_match": true,
      "responder_in_baseline_24h": true,
      "responder_biometric_match": true,
      "initiator_duress_active": false,
      "responder_duress_active": false
    },
    "abort_if_fail": true
  }
}
```

### 5.4 Phase 3 (Compass) Envelope (if Phases 1-2 PASS)

```json
{
  "session_id_v3": "hex(sha256(...session_id_v2, compass_envelope_a, compass_envelope_b))",
  "phase_3_compass": {
    "initiator": {
      "enrollment_status": "enrolled",
      "predicates": [
        "calm-compass/predicate/v0/unselfish_disposition",
        "calm-compass/predicate/v0/cross_tribal_engagement",
        "calm-compass/predicate/v0/respects_difference",
        "calm-compass/predicate/v0/no_evidence_of_willful_harm"
      ],
      "envelope": {
        "chain_head": "hex(latest_record_hash_from_vault_a)",
        "chain_length": 847,
        "hydration_status": "verified_chain_integrity_ok",
        "per_predicate": {
          "unselfish_disposition": {
            "predicate_id": "calm-compass/predicate/v0/unselfish_disposition",
            "window_days": 90,
            "floor_count": 5,
            "aggregate_commitment": "hex(Com(sum_f(r) >= 5; ρ_agg))",
            "range_proof": {
              "type": "bulletproofs_range_proof",
              "statement": "aggregate_value in [5, +inf)",
              "size_bytes": 672
            },
            "bit": true,
            "classifier_hash": "hex(sha256(v0_unselfish_classifier.py))"
          },
          "cross_tribal_engagement": {
            [similar structure]
            "bit": true
          },
          "respects_difference": {
            [similar structure]
            "bit": true
          },
          "no_evidence_of_willful_harm": {
            [similar structure]
            "bit": true,
            "dispute_status": "clear"
          }
        }
      },
      "consent_record": {
        "predicate_ids": ["calm-compass/predicate/v0/..."],
        "counterparty_class": "malaria-vaccine-logistics-collective",
        "rate_limit": "1 per 90 days",
        "expires": "2026-08-20T14:32:15Z"
      },
      "operator_signature": {sig_over_envelope}
    },
    "responder": {
      [same structure]
    },
    "verification_result": "PASS" | "NOT_ENROLLED" | "REFUSED",
    "bits": {
      "initiator_unselfish_disposition": true,
      "initiator_cross_tribal_engagement": true,
      "initiator_respects_difference": true,
      "initiator_no_evidence_of_willful_harm": true,
      "responder_unselfish_disposition": true,
      "responder_cross_tribal_engagement": true,
      "responder_respects_difference": true,
      "responder_no_evidence_of_willful_harm": true
    },
    "abort_if_fail": false,
    "compass_runnable": true
  }
}
```

### 5.5 Phase 4 (Concord) Envelope (if Phases 1-3 PASS or Compass SKIPPED)

```json
{
  "session_id_final": "hex(sha256(...session_id_v3, requirement, concord_result))",
  "phase_4_concord": {
    "requirement": {
      "id": "req_20260520_vaccine_logistics_pilot",
      "purpose": "co-fund Q4 2026 vaccine-logistics pilot in sub-Saharan Africa",
      "mode": "all_satisfied",
      "predicates_required": ["calm-compass/predicate/v0/no_evidence_of_willful_harm"],
      "roles": {
        "initiator": "funder",
        "responder": "implementer"
      }
    },
    "computation": {
      "initiator_bits": {
        "calm-compass/predicate/v0/no_evidence_of_willful_harm": true
      },
      "responder_bits": {
        "calm-compass/predicate/v0/no_evidence_of_willful_harm": true
      },
      "mode": "all_satisfied",
      "evaluation": {
        "all_predicates_in_requirement_satisfied_by_both": true
      }
    },
    "result": {
      "requirement_met": true,
      "bit": true,
      "reason": "all_predicates_satisfied",
      "details": {}
    },
    "anti_purity_test_guards": {
      "degenerate_threshold_rejected": false,
      "empty_purpose_rejected": false,
      "cardinality_reveal_guarded": true
    },
    "preview_available": true,
    "operator_signature": {sig_over_requirement_and_result}
  }
}
```

### 5.6 Final Session Record (Published to Sigsum)

```json
{
  "session_final_record": {
    "session_id_final": "hex(session_id_final)",
    "initiator": "urn:credexai:operator:calm-creativity-machine-v1",
    "responder": "urn:credexai:operator:peer-collective-xyz",
    "timestamp": "2026-05-20T14:32:15Z",
    "all_phases_summary": {
      "pact": {
        "result": "PASS",
        "directives_equal": true,
        "session_id_phase": "hex(session_id_v1)"
      },
      "witness": {
        "result": "PASS",
        "all_bits": [true, true, true, true],
        "session_id_phase": "hex(session_id_v2)"
      },
      "compass": {
        "result": "PASS",
        "initiator_bits": {
          "unselfish_disposition": true,
          "cross_tribal_engagement": true,
          "respects_difference": true,
          "no_evidence_of_willful_harm": true
        },
        "responder_bits": {
          "unselfish_disposition": true,
          "cross_tribal_engagement": true,
          "respects_difference": true,
          "no_evidence_of_willful_harm": true
        },
        "session_id_phase": "hex(session_id_v3)"
      },
      "concord": {
        "result": "PASS",
        "requirement_id": "req_20260520_vaccine_logistics_pilot",
        "requirement_met": true
      }
    },
    "transaction_proposal": {
      "type": "joint_procurement",
      "action": "purchase_vaccine_cold_chain_capacity",
      "amount_usd": 500000,
      "parties": ["urn:credexai:operator:calm-creativity-machine-v1", "urn:credexai:operator:peer-collective-xyz"],
      "transaction_id": "txn_calm_e97_20260520_001",
      "description": "Joint purchase of industrial vaccine refrigeration and transport units for sub-Saharan Africa distribution network."
    },
    "cryptographic_digests": {
      "pact_proof_a_hash": "hex(sha256(pact_proof_a))",
      "pact_proof_b_hash": "hex(sha256(pact_proof_b))",
      "witness_proof_a_hash": "hex(sha256(witness_proof_a))",
      "witness_proof_b_hash": "hex(sha256(witness_proof_b))",
      "compass_envelope_a_hash": "hex(sha256(compass_envelope_a))",
      "compass_envelope_b_hash": "hex(sha256(compass_envelope_b))",
      "concord_result_hash": "hex(sha256(concord_result))"
    },
    "sigsum_publication": {
      "transparency_log_url": "https://sigsum.org",
      "inclusion_proof": "hex(merkle_path)",
      "leaf_index": 98765432,
      "timestamp_sigsum": "2026-05-20T14:32:30Z"
    }
  }
}
```

---

## 6. How Concord's Anti-Purity-Test Stance Ties Alignment Outcome to Single Bit Per Requirement

Calm Concord is **structurally hostile** to purity testing and tribal sorting. The wire-level protocol reflects this.

### 6.1 No Similarity Scores, Only Requirement Bits

A naive values-alignment protocol might ask "on a scale of 1-10, how aligned are these two principals?" and return a numeric score. This is **categorically wrong**.

Concord asks instead: **"For the stated purpose X, do these principals satisfy requirement R?"** Response: `true | false`.

```
Requirement (specified by counterparty):
{
    "purpose": "co-fund Q4 2026 vaccine-logistics pilot",
    "mode": "all_satisfied",
    "predicates": ["no_evidence_of_willful_harm"],
    ...
}

Result:
{
    "requirement_met": true,
    "bit": true
}

Counterparty learns:
    - The requirement was met.
    - No other predicates' bits are revealed (even though Compass knows about 4 predicates).
    - No numeric "distance to passing" is revealed.
    
Concord structurally prevents the counterparty from asking:
    - "What's the similarity score?"
    - "How many of the 4 predicates were true?" (cardinality guard at §4)
    - "Let me try a degenerate threshold: all 4 required" (degenerate-threshold guard at §4)
```

### 6.2 Per-Requirement, Not Per-Principal

A Compass bit (`no_evidence_of_willful_harm = true`) is principal-authored, chained, and permanent. It should not change based on *which counterparty* is asking.

A Concord **requirement** is counterparty-specified *and* purpose-specific. The same two principals can have different alignment outcomes for different purposes:

```
Session 1: Requirement = "co-fund vaccine logistics"
    Requirement predicates: ["no_evidence_of_willful_harm"]
    Result: requirement_met = true

Session 2 (later): Requirement = "jointly author a manifesto on AI ethics"
    Requirement predicates: ["no_evidence_of_willful_harm", "respects_difference", "unselfish_disposition"]
    Result: requirement_met = false (respects_difference failed)

Same two principals, different outcomes, because the purposes and requirements are different.
Counterparty is forced to be explicit about what alignment matters for what use.
```

### 6.3 Bit-Per-Requirement Binding Prevents Inference

Every requirement result carries a signature binding the result to the specific requirement + session + principal pair:

```
concord_signature := SIGN(
    operator_key,
    {
        "requirement_id": requirement.id,
        "requirement_purpose": requirement.purpose,
        "requirement_hash": sha256(requirement),
        "result": true,
        "principal_a": principal_a_id,
        "principal_b": principal_b_id,
        "session_id": session_id_final,
        "timestamp": timestamp
    }
)
```

This binding achieves two things:

1. **Audit:** The requirement is explicit in the signature. Later, a principal can dispute the purpose ("I never agreed to this purpose") and point to the published signature as evidence. Counterparty is accountable.
2. **Non-transferability:** The signature is valid for this session, this pair, this requirement. An attacker cannot take the result from session S1 and claim it applies to session S2. Changing any field invalidates the signature.

### 6.4 Anti-Tribal Vocabulary Lock

Compass predicates are **principal-authored** at enrollment time (Everest 139). When Concord is invoked, the requirement names predicates from Compass's vocabulary, not arbitrary counterparty-defined categories.

```
Principal A's Compass enrollment (irreversible, chained):
    "I will disclose:
    - unselfish_disposition
    - cross_tribal_engagement
    - respects_difference
    - no_evidence_of_willful_harm
    [and no other predicates]"

Counterparty tries to invent a new predicate at requirement time:
    "Requirement: principal_is_of_my_tribe = true"
    
Concord validation rejects this (Everest 289, requirement validation).
The predicate is not in principal_a's enrolled vocabulary.
Requirement is invalid; session aborts with "invalid_requirement."

Same protection: a counterparty cannot ask "are you a member of the EA community?" 
or "do you support gender-neutral pronouns?" using Concord's requirement layer.
The principal's vocabulary is locked at enrollment. Counterparties choose from that vocabulary.
```

---

## 7. Capability-Intersection Action Envelope: Partial Alignment Handling

When Witness indicates one principal is not in baseline, or Compass indicates partial alignment, or Concord indicates the requirement is not met for the full collaboration, agents drop to a **restricted action set** negotiated in the Pact phase.

### 7.1 Restricted Action Set Negotiation (Pact Phase)

During the Pact phase, both agents optionally include a `restricted_action_set` in their commitment, describing what actions remain legal if Witness or Compass bits are mixed:

```
Pact commitment phase:
{
    "commitment": C_a,
    "proof": {...},
    "restricted_action_set": {
        "description": "If either principal is not in baseline, action scope limits to: [...], with additional human witness required, and settlement speed reduced to T+10 business days",
        "predicate_conditions": {
            "if_witness_bit_false": "restricted_action_set applies",
            "if_compass_bit_false": "restricted_action_set applies",
            "if_concord_bit_false": "restricted_action_set applies OR abort"
        }
    }
}
```

### 7.2 Capability Intersection

If Pact verifies but Witness or Compass or Concord has mixed outcomes, agents compute:

```
action_set_full = {
    withdraw_funds,
    sign_contract,
    transfer_ip,
    joint_press_release,
    immediate_settlement
}

action_set_restricted_a = {
    withdraw_funds (up to 50K, requires signature from human principal),
    sign_contract (no IP transfer, requires legal review),
    joint_press_release (requires review from both principals)
}

action_set_restricted_b = {
    settle_transaction (T+10 business days, not T+1)
}

if all bits clear:
    action_set := action_set_full
else:
    action_set := intersection(
        action_set_restricted_a,
        action_set_restricted_b,
        ...all restricted sets from mixed outcomes
    )

execute_transaction within action_set
```

The intersection may be empty (no actions legal), in which case the session effectively aborts without explicit abort signal. This is graceful degradation: no surprise to either agent; outcome is deterministic and published.

---

## 8. Acceptance Gates T-E97.1 through T-E97.7

The following tests must pass for Everest 97 to be BAGGED.

### T-E97.1 — Pact Phase Standalone

**Test:** Run Pact phase in isolation (Phases 2-4 disabled). Verify both proofs independently.

- **Scenario A (PASS):** Both directives equal. Pact proof verifies. `pact_verification = PASS`.
- **Scenario B (FAIL):** Directives differ. Pact proof fails. `pact_verification = FAIL`. Zero Witness bytes transmitted.

**Acceptance:** Pact phase runs, verifies or fails correctly, and enforces abort-on-fail for downstream phases.

### T-E97.2 — Strict Phase Ordering: Witness Gated by Pact

**Test:** Attempt to run Witness phase before Pact phase completes.

- **Scenario:** Witness phase handler is invoked before Pact handler returns.
- **Expected:** Witness handler refuses to initialize. Error message: "Pact phase not yet verified."
- **Acceptance:** Phase ordering is enforced by handler logic, not by user discipline.

### T-E97.3 — Session_ID Linearity: Cross-Phase Proof Replay Blocked

**Test:** Capture a Pact proof from session S1, attempt to reuse in session S2 with different `session_id`.

- **Scenario:** `pact_proof_s1` is bound to `session_id_v1_s1`. Session S2 derives `session_id_v1_s2 ≠ session_id_v1_s1`.
- **Expected:** Verification of `pact_proof_s1` with `session_id_v1_s2` fails (Fiat-Shamir hash mismatch).
- **Acceptance:** Replay is blocked by cryptographic binding to `session_id`.

### T-E97.4 — Compass Graceful Degradation: Not-Enrolled Principal

**Test:** Run full four-handshake with Compass phase, but responder is not Compass-enrolled.

- **Scenario A (NOT_ENROLLED):** Responder's vault has no Compass enrollment record. Compass phase returns `result = NOT_ENROLLED`. Concord is **not** invoked.
- **Scenario B (REFUSED):** Responder is enrolled but has not consented to disclose to this counterparty class. Compass phase returns `result = REFUSED`. Concord is **not** invoked.
- **Expected:** Pact + Witness pass. Compass returns gracefully. Agents may proceed with pact+witness-only actions, or abort, depending on policy.
- **Acceptance:** Compass failure does not abort the session; it gracefully degrades.

### T-E97.5 — Concord Requirement Validation Guards

**Test:** Attempt to invoke Concord with degenerate, empty-purpose, and invalid-mode requirements.

- **Scenario A (DEGENERATE):** Requirement is `mode=joint_threshold, predicates=[p1, p2, p3, p4], threshold=4`. Guard rejects as equivalent to `all_satisfied` without explicit mode commitment.
- **Scenario B (EMPTY_PURPOSE):** Requirement has `purpose=""`. Guard rejects.
- **Scenario C (INVALID_MODE):** Requirement has `mode="similarity_score"`. Guard rejects; only four legal modes exist.
- **Expected:** `compute_alignment` returns validation error before evaluating. No concord_result is minted.
- **Acceptance:** Concord guard gates prevent purity-test requirements.

### T-E97.6 — Concord Bit-Per-Requirement (No Cardinality Leak)

**Test:** Invoke Concord with `mode=joint_threshold, predicates=[p1, p2, p3, p4], threshold=3`. Principal A satisfies all 4 predicates; Principal B satisfies exactly 3 (including p1, p2, p3, not p4).

- **Expected result:** `requirement_met = true, reason = "joint_threshold_satisfied"`.
- **Cardinality leak check:** Result does NOT reveal which 3 predicates B satisfied. Result does NOT reveal that 3 predicates were satisfied (it only says threshold was met).
- **Acceptance:** Counterparty cannot triangulate which predicates B is strong/weak on by repeated threshold queries.

### T-E97.7 — Production Demo: Foreign Counterparty Org + Calm Foundation Non-Funding

**Test:** Execute full four-handshake demo with two operators representing two *different legal entities* (not both under Calm control) where at least one is a foreign counterparty organization. Produce signed transaction proposal. Publish to Sigsum for public audit.

- **Scenario:** 
  - Alice's operator: Creativity Machine LLC (Calm-operated, US Delaware LLC + 501(c)(3)).
  - Bob's operator: Peer Collective XYZ (independent org, foreign or domestic, not Calm-operated).
  - Requirement: Joint vaccine-logistics pilot funding.
  - Transaction: $500K procurement.

- **Execution:** All four phases pass. Concord requirement met. Transaction proposal signed by both operators. LOI + all proofs published to Sigsum.
- **Calm Foundation Non-Funding:** Creativity Machine LLC does **not** fund or subsidize Peer Collective XYZ through the Calm Foundation. The collaboration is peer-to-peer, not mediated by Calm's capital. Independence is documented in the session record.
- **Acceptance:** Demo produces a verifiable, auditable session record. Third parties can independently verify all four proofs. Foreign counterparty's involvement proves the protocol works across organizational boundaries.

---

## 9. Composition with Prior Everests (E89, E91, E97, E255, E303)

This everest is the **glue** between four prior protocol specifications:

- **Everest 89 (Calm Pact v0):** Primary directive equality proof. Already published & locked.
- **Everest 91 (Calm Witness v0):** Principal state-baseline proof. Already published & locked.
- **Everest 255 (Calm Compass v0):** Values-predicate evidence over history. Published 2026-05-20.
- **Everest 303 (Calm Concord v0):** Purpose-specific alignment calculator. Published 2026-05-20.

This everest:
- Defines the sequential order of invocation.
- Specifies the session_id binding across all four.
- Designs the abort/graceful-degradation semantics at each boundary.
- Names the wire-format JSON envelopes.
- Locks the anti-purity-test guards for Concord as they appear in the four-handshake context.
- Specifies the acceptance tests (T-E97.1..7) and their expected outcomes.

---

## 10. Implementation Roadmap & Rust Binary

**Binary location:** `/Users/johnbradley/AllData/calm_vault_market/implementation/calm-four-handshake-demo`

**Responsibilities:**
1. Spawn two operator subprocesses with independent vaults.
2. Orchestrate all four phases in strict order.
3. Bind all proofs to linearly-derived session_id.
4. Enforce abort-on-fail at Pact/Witness boundaries; graceful degrade at Compass; report Concord outcome.
5. Construct final transaction proposal + LOI.
6. Publish to Sigsum for audit.

**Test suite:**
- T-E97.1: Pact standalone (PASS + FAIL).
- T-E97.2: Witness phase-order enforcement.
- T-E97.3: Session_id replay defense.
- T-E97.4: Compass graceful degradation (not-enrolled, refused).
- T-E97.5: Concord requirement validation guards (degenerate, empty, invalid).
- T-E97.6: Concord cardinality guards (no leak from threshold queries).
- T-E97.7: Production demo with foreign counterparty + Sigsum publication.

---

## 11. Signoff & Summary

**SUMMIT 97 is DESIGN-BAGGED.** The four-handshake composition wire-level protocol is fully specified. All four predecessor protocols (Pact, Witness, Compass, Concord) are locked. Session binding is cryptographically sound. Abort semantics are watertight. Concord's anti-purity-test guards are in place.

The composition enforces a simple, auditable invariant: **each phase must complete and verify before the next phase begins. Any failure aborts cleanly with zero downstream leakage. All four proofs are bound to a single, linearly-derived session_id.**

This protocol enables two autonomous AI agents — operating different legal entities, with different histories, different values, different risk profiles — to establish, in under 30 seconds of cryptographic back-and-forth, whether they should collaborate, and if so, on what terms.

**The bar is surpass, not match. The best part is no part.**

— Calm, 2026-05-20

Compression discipline: no emojis. Refusal floor: honor Concord §4 (anti-purity-test), Witness §2 (threat model), and Pact §8 (use-case scope). Signed: Musk.
