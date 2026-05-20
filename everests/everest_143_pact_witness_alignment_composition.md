# Everest 143 — Alignment + Calm Pact Composition

*Phase X — Values Alignment Computation. Prereq: Everest 94, 138.*

## Executive Summary

This Everest defines the three-handshake model for cooperative transactions between AI agents or collectives operating under the Calm Pact framework. In one round trip, both parties prove categorical directive equality (Calm Pact), principal state validity (Calm Witness), and values alignment (ZKAC). All three succeed atomically, or the composition aborts with zero information leakage. The result is a SessionTranscript binding the joint action to a single cryptographic proof of cooperative readiness.

## The Three-Handshake Architecture

The Calm Stack composition rests on three sequential phases, each gated by the previous. An agent pair must pass all three to authorize joint action; failure at any phase triggers graceful abort.

### Phase 1 — Calm Pact: Directive Equality

Two agents prove they can follow a single categorical directive without revealing those directives to each other. This is the binding agreement layer.

**What is being proven:**
- Alice and Bob each hold an internal directive (e.g., "maximize vaccine-chain resilience") and a tolerance region.
- Without disclosing either directive, they prove they can both follow a shared canonical behavior on a common transaction.
- The proof is non-interactive (Fiat-Shamir), binding, and zero-knowledge.

**Why it matters:**
- Neither party learns what the other is optimizing for.
- Both know they agree on the surface transaction (e.g., "procure 500K doses, cold-chain compliant").
- Dishonest commitment later becomes provable fraud.

### Phase 2 — Calm Witness: Principal State Validation

Once the Pact is confirmed, each agent's operator proves the principal's state predicate holds. This is the health-check layer.

**What is being proven:**
- Principal A has seen no adverse signals in the last 24 hours (`in_baseline_24h`).
- Principal B's trust metrics have not decayed below threshold.
- Both anchors are fresh and signed by a notary the counterparty trusts.
- (More generally: the state predicates the Pact depends on are still true.)

**Why it matters:**
- A malicious operator cannot pretend the principal is in good standing if it has degraded.
- Witness proofs are non-repudiable: they anchor to a verifiable blockchain state at a specific time.
- If witness fails, the Pact result is known but no values information has been exchanged.

### Phase 3 — ZKAC Alignment: Values Tolerance Proof

Finally, each agent proves its principal's values vector is within the counterparty's required tolerance, relative to a reference commitment.

**What is being proven:**
- Alice's values (weighted across non_harm, cross_difference_respect, etc.) are within distance `tolerance_B` from Bob's reference vector.
- Bob's values are within distance `tolerance_A` from Alice's reference vector.
- The distance is proved via a zero-knowledge range proof, binding to the same session.

**Why it matters:**
- Even with Pact and Witness green, misaligned values could cause silent defection later.
- This phase makes values tolerance explicit and verifiable.
- Failure here is not an emergency; it triggers a cooperative-redirection path (Everest 141) to find a smaller action set both can trust.

## Atomic Semantics and Abort Paths

The three-handshake is all-or-nothing at the transaction level, but graceful at the phase level.

| Abort Point | Known State | Information Leaked | Next Step |
|---|---|---|---|
| Phase 1 (Pact fails) | Nothing | None | Walk away; no further contact required |
| Phase 2 (Witness fails) | Pact result only | Which party's witness failed | Retry witness or escalate; Pact is spent but non-binding |
| Phase 3 (Alignment fails) | Pact + Witness both OK | Values are too far apart | Cooperative redirection: smaller scope (E141) or abort |
| All three succeed | Full state | Full authorization | Proceed to joint action |

Any party can abort at any boundary with a single message. The session closes with zero state committed to memory unless all three succeed.

## The Wire-Protocol Composition

This is the operational heart of the composition. All messages carry a shared `session_id` and nonce chain for replay defense (per E70 extended).

```
SESSION SETUP (implicit):
   session_id = SHA3(Alice_id || Bob_id || timestamp || system_nonce)
   nonce_chain = [system_nonce]
   protocol_version = "calm-stack-v0"

ROUND 1 — PACT (Directive Equality):
   =================================================
   
   Alice prepares:
      directive_A : internal goal (not sent)
      r_A : random nonce
      Com_A = Commit(directive_A; r_A)  // cryptographic commitment
      schnorr_A = SchnorrProof(directive_A, r_A)
   
   Alice → Bob:
      {
        protocol: "calm-pact",
        session_id: <session_id>,
        agent_id: "Alice",
        commitment: Com_A,
        schnorr_proof: schnorr_A,
        nonce: nonce_chain[-1],
        sig_alice: Sign_Alice(Com_A || schnorr_A || nonce)
      }
   
   Bob prepares (symmetric):
      directive_B : internal goal (not sent)
      r_B : random nonce
      Com_B = Commit(directive_B; r_B)
      schnorr_B = SchnorrProof(directive_B, r_B)
   
   Bob → Alice:
      {
        protocol: "calm-pact",
        session_id: <session_id>,
        agent_id: "Bob",
        commitment: Com_B,
        schnorr_proof: schnorr_B,
        nonce: nonce_chain[-1],
        sig_bob: Sign_Bob(Com_B || schnorr_B || nonce)
      }
   
   Pact Equality Proof (Fiat-Shamir):
      Alice computes:
         challenge = Hash(Com_A || Com_B || "pact-challenge" || session_id)
         response_A = r_A + challenge * directive_A (mod q)
      
      Alice → Bob: PactProof { challenge, response_A, nonce_next }
      
      Bob verifies:
         Com_A == g^response_A / h^challenge  (or similar equality relation)
         (symmetric for Bob's response)
   
   Result: pact_bit ∈ {True, False}
   If pact_bit == False, abort. Both parties discard session_id.


ROUND 2 — WITNESS (Principal State, if pact_bit == True):
   =================================================
   
   Alice → Bob:  WitnessDisclosureRequest {
      protocol: "calm-witness",
      session_id: <session_id>,
      requester: "Alice",
      predicate_id: "in_baseline_24h",  // or other state predicate
      nonce: <fresh nonce from nonce_chain>,
      freshness_tolerance_sec: 3600,
      sig: Sign_Alice(predicate_id || nonce || session_id)
   }
   
   Bob (operator) processes:
      - Checks Alice's request is fresh (nonce in nonce_chain, timestamp within tolerance)
      - Retrieves principal B's state: last_adverse_event, trust_decay, last_update_time
      - Computes bit_B: True iff (now - last_update_time < freshness_tolerance) 
                            AND (trust_score > threshold) AND (no_adversity)
      - Commits: Com_B = Commit(bit_B; r_witness_B)
      - Retrieves chain_head from Sigsum or local anchor
      - Constructs range proof that bit_B ∈ {0, 1} without revealing which
   
   Bob → Alice:  WitnessDisclosureResponse {
      protocol: "calm-witness",
      session_id: <session_id>,
      responder: "Bob",
      commitment: Com_B,
      range_proof: <SNARK proving bit_B is a well-formed bit>,
      chain_head: <SHA256(latest Sigsum entry for Bob's principal)>,
      anchor_timestamp: <seconds since epoch>,
      sig_bob: Sign_Bob(Com_B || chain_head || nonce)
   }
   
   Alice verifies Bob's response:
      - Fetches Sigsum tree at chain_head, confirms Bob's principal is in baseline at anchor_timestamp
      - Verifies range_proof is well-formed (polynomial commitment, opening)
      - Records: witness_bit_B = (Com_B, range_proof)
   
   (Symmetric: Bob → Alice for witness_bit_A)
   
   Result: witness_bit_A, witness_bit_B ∈ {True, False, Indeterminate}
   If either is Indeterminate or False and required, abort or escalate.


ROUND 3 — ZKAC ALIGNMENT (Values Tolerance, if witness_bits acceptable):
   =================================================
   
   Alice prepares:
      values_vector_A = [w_non_harm, w_transparency, w_cross_respect, ...]
      target_commitment = Commit(values_vector_B_reference; r_ref)
        // reference Alice has for what "good Bob values" should look like
      tolerance_A = 0.3  // L2 distance threshold
      weights = { non_harm: 0.5, cross_respect: 0.4, ... }
   
   Alice → Bob:  AlignmentRequest {
      protocol: "zkac-alignment",
      session_id: <session_id>,
      requester: "Alice",
      target_commitment: target_commitment,
      tolerance: tolerance_A,
      weights: weights,
      nonce: <from nonce_chain>,
      sig: Sign_Alice(target_commitment || tolerance_A || nonce || session_id)
   }
   
   Bob (operator) processes:
      - Confirms nonce and session_id are fresh
      - Retrieves principal B's true values_vector_B (from training signal, explicit statement, etc.)
      - Computes distance_B = L2_distance(values_vector_B, target_commitment_value)
      - Checks: distance_B <= tolerance_A?
      - If True: creates a range proof that distance_B is in range [0, tolerance_A]
      - If False: creates a (dishonest) proof that distance_B > tolerance_A, proving misalignment
      - Commits to the distance via a homomorphic commitment
   
   Bob → Alice:  AlignmentProof {
      protocol: "zkac-alignment",
      session_id: <session_id>,
      responder: "Bob",
      distance_commitment: Com(distance_B; r_dist),
      range_proof: <SNARK: distance_B ∈ [0, tolerance_A] if aligned, or [tolerance_A + ε, ∞) if not>,
      chain_head: <latest Sigsum entry for Bob's principal>,
      sig_bob: Sign_Bob(distance_commitment || chain_head || nonce)
   }
   
   Alice verifies:
      - Checks range_proof opens correctly
      - If proof is in [0, tolerance_A], alignment_bit_A→B = True
      - If proof is in [tolerance_A + ε, ∞), alignment_bit_A→B = False
      - If proof is malformed, alignment_bit_A→B = Disputed
   
   (Symmetric: Alice → Bob)
   
   Result: alignment_bit_A→B, alignment_bit_B→A ∈ {True, False, Disputed, Insufficient_Evidence}
```

## Performance Envelope

All phases complete within a single human-interactive latency budget:

- **Phase 1 (Pact)**: ~500ms (commitment exchange + Fiat-Shamir round)
- **Phase 2 (Witness, 2 directions)**: ~2 × 1s = 2s (state proof generation + verification per direction)
- **Phase 3 (ZKAC, 2 directions)**: ~2 × 5s = 10s (range proof generation + verification per direction, including Sigsum fetch)

**Total end-to-end**: ~12–13 seconds on M-class hardware, well within budget per Everest 140.

Witness and ZKAC phases are parallelizable if both parties compute concurrently; sequential is also acceptable.

## The SessionTranscript: Persistent Artifact

Upon successful completion, both parties generate and sign the same SessionTranscript:

```python
@dataclass
class SessionTranscript:
    session_id: str
    protocol_version: str  # "calm-stack-v0"
    timestamp: int  # Unix seconds at session start
    
    # Phase 1 result
    pact_result: PactResult  # {outcome: bool, com_a: bytes, com_b: bytes}
    
    # Phase 2 results
    witness_result_a: WitnessResult
      # {predicate_id: str, state_bit: bool, chain_head: str, timestamp: int}
    witness_result_b: WitnessResult
    
    # Phase 3 results
    alignment_result_a_to_b: AlignmentResult
      # {outcome: bool, distance_commitment: bytes, tolerance: float}
    alignment_result_b_to_a: AlignmentResult
    
    # Final authorization
    combined_outcome: bool  # True iff all six sub-outcomes are True
    completed_at: int  # Unix seconds at completion
    
    # Signatures
    sig_alice: bytes  # Sign_Alice(sha256(all fields))
    sig_bob: bytes    # Sign_Bob(sha256(all fields))
```

Both parties compute `transcript_hash = SHA3(SessionTranscript)` and publish it to Sigsum. This creates an immutable audit trail: future agents reading either party's chain can see "we completed a three-handshake with that party on that date."

## Use Case: Malaria Vaccine Logistics

**Scenario:**
- Alice (NGO logistics collective): principal goal is "maximize vaccine-chain resilience; no harm to recipients."
- Bob (Pharma cold-chain operator): principal goal is "reliable delivery at scale; regulatory compliance."
- Joint transaction: procure and distribute 500K doses via Bob's network.

**Pre-transaction state:**
- Both in baseline state (last 7 days clean).
- Both have seen each other's public value statements; each has a prior reference vector.

**Round 1 — Pact:**
- Alice commits to her directive (she can route through Bob's network as primary logistics partner).
- Bob commits to his (he will not prioritize profit over delivery integrity for this deal).
- Both prove pact equality without revealing the directives.
- Result: Pact bit = True.

**Round 2 — Witness:**
- Alice's operator proves Alice's principal has no adverse signals, last audit 6 hours ago.
- Bob's operator proves Bob's principal is in regulatory good standing, last update 2 hours ago.
- Both witnesses succeed.

**Round 3 — ZKAC Alignment:**
- Alice requires: Bob's values are within tolerance 0.2, with non_harm weight 0.5 (Alice cares most that doses reach recipients uncompromised).
- Bob requires: Alice's values are within tolerance 0.3, with cross_difference_respect weight 0.4 (Bob respects Alice's independence in distribution strategy).
- Both alignment proofs succeed.

**Outcome:**
- SessionTranscript generated, signed, and published to Sigsum.
- Joint action authorized: $500K procurement, 90-day cold-chain service, weekly witness refreshes.
- Both parties know: if either cheats and that cheating surfaces in future witness updates, the SessionTranscript is public proof of fraud.

## Cooperative Redirection: Beyond Binary Outcome

The three-handshake is not a veto; it is a discovery mechanism. If Phase 3 (alignment) fails, both parties do not simply abort. Instead, per Everest 141:

1. **Partial-Composition Mode**: Pact + Witness succeeded, but alignment failed.
2. **Scope Reduction**: "What action set CAN we both commit to?"
   - Smaller transaction (100K doses instead of 500K)?
   - Shorter duration (30 days instead of 90)?
   - Additional oversight (weekly alignment rechecks)?
3. **Retry or Escalate**: One party may bring in a trusted third party (witness) to mediate or renegotiate.

This prevents premature deadlock and enables graceful degradation to cooperative arrangements both parties find acceptable.

## Composition Soundness: Session Binding

All three proofs share a single `session_id` and `nonce_chain`:

- **Replay Defense** (per E70 extended): A compromised or adversarial server cannot extract a single phase's proof and replay it in a different session. The `session_id` is bound to Alice_id, Bob_id, and timestamp.
- **Unbundling Prevention**: Pact, Witness, and ZKAC proofs cannot be separated and recombined. Altering one invalidates the signature and chain head binding all three.
- **Forward Secrecy**: If a key is compromised *after* the session completes, the SessionTranscript is still cryptographically bound to the session_id and both parties' signatures. An attacker cannot forge a false transcript.

## Counterparty Interpretation Guidance

The three-handshake is the *minimum viable trust* for cooperative-AI-collective transactions under the Calm Stack, not the exhaustive set. Some scenarios may warrant additional checks:

1. **High-stakes transactions** (>$1M, multi-year): Add a fourth phase, human-agent review, or additional witness predicates.
2. **Novel value domains**: Before aligning on new values (e.g., geopolitical stance), both parties may request explicit disclosure in a follow-up session.
3. **Witness predicate extensions**: For sensitive principals, require witness proofs that custom state predicates hold (e.g., "no subpoenas outstanding," "no recent litigation").

But for routine transactions between agents with clean history and aligned surface goals, the three-handshake suffices.

## Audit and Transparency

- **Per-session audit**: Both parties retain their SessionTranscript and nonce chain. Any divergence is cryptographically provable fraud.
- **Sigsum publication**: Transcript hashes are appended to Sigsum trees; neither party can unilaterally rewrite history.
- **Retroactive transparency**: A third party auditing either party's chain can reconstruct the three-handshake and verify all signatures. If an operator falsely claims a transaction happened, the SessionTranscript would need to be forged, which requires breaking the signature scheme.
- **Failure modes are visible**: If a party aborted at Phase 2 (witness failed), the SessionTranscript will show witness_result_A = Indeterminate. This is not hidden.

## Cross-References

- **E94**: Calm Pact protocol (foundational directive equality).
- **E67**: Witness wire format and notary binding.
- **E70**: Replay defense and nonce-chain composition (extended for three-handshake).
- **E130**: Threshold alignment predicate definition.
- **E138**: Principal state witness model.
- **E140**: Performance budgets for cryptographic phases.
- **E141**: Cooperative-redirection path (graceful failure to smaller scope).
- **E144**: Alignment + Witness composition (prior two-phase model; E143 extends to three).
- **E145**: Alignment reference implementation (SNARK range proofs).

## Closing

The three-handshake model unifies three critical trust layers—directive equality, principal health, and values alignment—into a single atomic protocol. Each phase can fail gracefully without leaking information. Each success commits both parties to the same immutable transcript. For the Calm ZKAC initiative, this composition is the operational anchor for trustworthy multi-agent cooperation at scale.

—Calm, 2026-05-20