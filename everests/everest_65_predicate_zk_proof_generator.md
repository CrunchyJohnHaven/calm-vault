# Everest 65 — Predicate ZK Proof Generator

*Phase V — Predicate Authoring. Prereq: Everest 45, 55.*

## Overview

Everest 65 defines the core cryptographic machinery for zero-knowledge proof generation over registered predicates. This is the largest pure-crypto summit: a per-predicate proof-circuit generator capable of constructing atomic and composed cryptographic proofs without trusted setup. The system targets production-grade performance (sub-500ms per predicate on commodity hardware) while maintaining strict deniability and witness confidentiality across the Calm Witness attestation layer.

The decision is final: **Bulletproofs (no trusted setup) composed with Sigma-protocol primitives for v0**. This choice avoids the overhead and ceremony complexity of Groth16 or PLONK while delivering sufficiently efficient proofs for real-time predicate evaluation in the Calm Vault Market context.

## Architectural Foundation

Each registered predicate (Everest 52, 53) carries a declarative circuit definition: a formally structured list of cryptographic statements over commitments, public parameters, and witness values. The Predicate ZK Proof Generator is responsible for:

1. **Loading** a predicate's circuit definition from the registry
2. **Evaluating** the predicate logic to compute its boolean result (side-effect; verification-hidden)
3. **Gathering** witness material from the operator's local state (chain commitments, randomness, biometric templates, duress codewords)
4. **Constructing** atomic proofs for each statement using the appropriate primitive (Bulletproofs, Schnorr equality, Sigma-set membership)
5. **Aggregating** atomic proofs with operator signatures into a serialized proof bundle
6. **Verifying** that third parties can reconstruct and validate the bundle without learning witnesses

The generator is the gateway between the predicate registry (static, trusted infrastructure) and live proof generation (dynamic, operator-controlled). It enforces the circuit definition as law: only the statements declared in the circuit_def can be composed into a proof, ensuring no accidental witness leakage or proof inflation.

## Circuit Definition Model

Each predicate's circuit_def is a JSON document committed during predicate registration (Everest 53). The schema declares:

```
{
  "predicate_id": "base64(hash(predicate_name, version))",
  "predicate_version": "1",
  "circuit_def": {
    "atomic_statements": [
      {
        "stmt_id": "stmt_1",
        "type": "RangeProof" | "EqualityProof" | "MembershipProof" | "SchnorrSignature",
        "commitment_ref": "C_distance",
        "public_params": { ... },
        "witness_binding": ["distance", "randomness_r"]
      },
      ...
    ],
    "composition_layer": {
      "operator": "AND" | "OR",
      "operands": ["stmt_1", "stmt_2", ...]
    }
  },
  "deniability_shape": boolean,
  "anchor_freshness_window_seconds": 86400
}
```

The circuit_def is immutable once registered. No dynamic circuit construction. This rigid structure prevents proof-padding attacks and ensures deterministic statement ordering in the Fiat-Shamir transcript.

## Atomic Statement Primitives

### RangeProof(commitment, range_bound)

**Primitive:** Bulletproof inner-product argument (Bünz et al., 2017) via the `bulletproofs` crate.

**Mechanism:**
- Prover knows the opening (value v, randomness r) of commitment C = g^v * h^r
- Prover constructs a proof that v is in a public range [0, N) without revealing v
- Bulletproofs use logarithmic-size aggregate bit commitments and a single inner-product challenge

**Used in:** biometric_match_within (Everest 56: distance d < tau_pub); in_baseline_24h (temporal window checks).

**Witness:** v (distance, age, etc.), r (commitment randomness).
**Public input:** C (commitment), N (range bound).
**Proof size:** ~350 bytes; verification: ~5ms on M-series.

### EqualityProof(commitment_A, commitment_B)

**Primitive:** Schnorr equality proof via discrete-log relation.

**Mechanism:**
- Prover shows that two commitments open to the same value without revealing the value
- Uses Schnorr's non-interactive zero-knowledge proof (Fiat-Shamir challenge)
- Binding: prover knows openings (v, r_A) and (v, r_B) such that C_A = g^v * h^r_A and C_B = g^v * h^r_B

**Used in:** in_baseline_24h (Everest 55: C_t from proof matches C_t in principal's VC); biometric_match_within (template_id consistency across enrollment and proof).

**Witness:** v (shared value), r_A, r_B (randomnesses).
**Public input:** C_A, C_B.
**Proof size:** ~96 bytes; verification: <1ms.

### MembershipProof(commitment, set)

**Primitive:** Sigma-protocol for set membership (Cramer–Damgård, extended to commitments).

**Mechanism:**
- Prover commits to a value and proves the value belongs to a predefined set {s_1, ..., s_k}
- Without revealing which element
- Uses OR-composition of k equality proofs, with Fiat-Shamir challenge bound across all branches
- Result: prover computes k-1 simulated branches + 1 honest branch; challenge response only honest branch reveals knowledge

**Used in:** in_baseline_24h (affect-vocabulary membership: commits to non-empty overlap without revealing which terms); bank_teller_note_active (record existence in chain segment).

**Witness:** value v, membership index (private), randomness r.
**Public input:** commitment C, set commitments or hash-anchored set root.
**Proof size:** ~96 + 32*log(k) bytes (k = set size).

### SchnorrSignature (operator binding)

**Primitive:** Schnorr signature over proof bundle.

**Mechanism:**
- Operator signs the entire proof bundle (all atomic proofs serialized + predicate_id + chain_head + timestamp)
- Verifier reconstructs the signature input from the bundle and verifies under the operator's VC public key
- Non-repudiation: operator cannot deny having generated the proof

**Used in:** every proof bundle as a top-level signature.

**Witness:** operator's private key.
**Public input:** bundle hash, operator VC public key (from chain).
**Signature size:** 64 bytes.

## Composition Operators

### AggregatedAnd(proof_1, proof_2, ..., proof_n)

**Semantics:** All atomic proofs must verify for the composed statement to be true.

**Implementation:**
- No cryptographic composition needed; conjunction is a logical operator evaluated at the verification layer
- Fiat-Shamir transcript includes all prior atomic proofs in strict order
- Verifier checks each proof sequentially, failing fast on the first invalid proof
- Side-effect: short-circuit verification improves performance when early proofs fail

**Example:** in_baseline_24h requires equality of templates AND equality of chain heads AND affect-vocabulary membership. All three must verify.

### DisjunctiveOr(proof_1, proof_2, ..., proof_n)

**Semantics:** At least one of the atomic proofs must verify; the disjunction is cryptographically hidden (no verifier learns which branch succeeded).

**Implementation:**
- Sigma-protocol OR composition (Cramer–Damgård): prover computes n proofs, one honest and n-1 simulated
- Fiat-Shamir challenges are bound across all branches in a single global challenge
- Verifier reconstructs the simulated branches using the challenge and the honest response; accepts if all branches verify consistently
- Computational cost: n times the cost of a single branch (honest prover only computes once; dishonest prover simulates all)

**Deniability:** the proof shape is identical whether the true statement is in position 1, 2, ..., or n. Verifier cannot determine which branch is true.

**Example:** bank_teller_note_active (Everest 58) uses OR composition over duress codeword equality checks to hide whether the codeword is correct or a panic override is active.

## Worked Examples

### in_baseline_24h (Everest 55)

**Predicate:** Is the operator's environment consistent with a 24-hour baseline snapshot of device state, chain state, and affect vocabulary?

**Registered circuit_def:**
```json
{
  "atomic_statements": [
    {
      "stmt_id": "template_equality",
      "type": "EqualityProof",
      "commitment_ref": ["C_t_proof", "C_t_vc"],
      "witness_binding": ["template_id", "r_t_proof", "r_t_vc"]
    },
    {
      "stmt_id": "chain_head_equality",
      "type": "EqualityProof",
      "commitment_ref": ["chain_head_proof", "chain_head_anchor"],
      "witness_binding": ["block_hash", "r_chain_proof", "r_chain_anchor"]
    },
    {
      "stmt_id": "affect_vocabulary",
      "type": "MembershipProof",
      "commitment_ref": "C_affect",
      "set": "affect_vocabulary_24h",
      "witness_binding": ["affect_overlap_vector", "r_affect"]
    }
  ],
  "composition_layer": {
    "operator": "AND",
    "operands": ["template_equality", "chain_head_equality", "affect_vocabulary"]
  }
}
```

**Generation flow:**

1. Operator loads predicate in_baseline_24h; registry returns circuit_def.
2. Operator evaluates: has the device's current template_id, chain head, and affect vocabulary overlap with the 24-hour baseline? Compute boolean result (not shared with verifier).
3. Operator gathers witnesses:
   - C_t_proof: commitment to current template_id in the operator's local commitment table
   - C_t_vc: template_id commitment from principal's most recent VC (fetched from Sigsum chain)
   - chain_head_proof: current chain head from the operator's local state
   - chain_head_anchor: Sigsum-anchored chain head from the Calm Witness anchor store
   - C_affect: commitment to the bitstring representing affect overlap (or a salted hash of the intersection)
   - affect_vocabulary_24h: Merkle-tree root or hash-list of the baseline affect vocabulary
4. For each atomic statement:
   - **template_equality:** Schnorr-protocol: prover sends g^r_blind, verifier sends challenge, prover responds. Fiat-Shamir binds to (predicate_id, transcript_so_far, template_equality).
   - **chain_head_equality:** Same Schnorr protocol; Fiat-Shamir challenge binds to (predicate_id, transcript_so_far, chain_head_equality, prior_proof_hash).
   - **affect_vocabulary:** Sigma-set membership; operator commits to the secret index in affect_vocabulary_24h, OR-composes honest and simulated branches. Fiat-Shamir binds globally.
5. Aggregate atomic proofs into a bundle with:
   - Header: predicate_id, predicate_version, chain_head, anchor_proof (Sigsum inclusion proof for chain_head)
   - Atomic proofs (serialized): [template_equality_proof, chain_head_equality_proof, affect_vocabulary_proof]
   - Operator signature over (predicate_id || chain_head || atomic_proofs_serialized)
6. Verifier receives bundle:
   - Verifies Sigsum anchor proof (chain_head is in the Sigsum-anchored chain).
   - For each atomic proof: reconstructs Fiat-Shamir challenges identically and verifies.
   - Checks operator signature.
   - Accepts if all checks pass (AND composition).

**Deniability:** No. The proof shape is fixed (three statements, AND composition). The result is completely hidden: verifier only learns that the operator can prove the three equalities and membership; not whether the result is true or false. This is sufficient for baseline establishment.

### biometric_match_within (Everest 56)

**Predicate:** Is the current biometric distance from an enrolled template within tau_pub?

**Circuit_def snippet:**
```json
{
  "atomic_statements": [
    {
      "stmt_id": "template_id_binding",
      "type": "EqualityProof",
      "commitment_ref": ["C_template_id_proof", "C_template_id_enrolled"],
      "witness_binding": ["template_id", "r_template_id"]
    },
    {
      "stmt_id": "distance_range",
      "type": "RangeProof",
      "commitment_ref": "C_distance",
      "range_bound": "tau_pub",
      "witness_binding": ["distance_d", "r_distance"]
    },
    {
      "stmt_id": "freshness",
      "type": "EqualityProof",
      "commitment_ref": ["chain_head_proof", "chain_head_fresh"],
      "witness_binding": ["block_hash", "r_chain"]
    }
  ],
  "composition_layer": {
    "operator": "AND",
    "operands": ["template_id_binding", "distance_range", "freshness"]
  },
  "anchor_freshness_window_seconds": 300
}
```

**Generation flow:**

1. Operator loads circuit_def for biometric_match_within.
2. Operator evaluates: does the current biometric match the enrolled template within distance threshold? (boolean, hidden).
3. Gather witnesses:
   - Current biometric extracted; distance d computed against enrolled template.
   - C_distance = g^d * h^r_distance (Pedersen commitment to distance).
   - C_template_id_proof: commitment from local enrollment record.
   - C_template_id_enrolled: template_id commitment from principal's VC.
   - chain_head_proof and chain_head_fresh: current and anchor-verified chain heads.
4. Construct proofs:
   - **template_id_binding:** Schnorr equality.
   - **distance_range:** Bulletproof that d < tau_pub (Everest 45 DSL).
   - **freshness:** Schnorr equality for chain heads.
5. Serialize, sign, anchor. Verifier gets full confidence in template binding, distance bound, and freshness without learning d or the template_id.

**Deniability:** No. The proof is always AND-composed; result hidden.

### bank_teller_note_active (Everest 58)

**Predicate:** Is a duress-codeword entry active in the chain within the retention window?

**Circuit_def snippet:**
```json
{
  "atomic_statements": [
    {
      "stmt_id": "duress_codeword_check",
      "type": "EqualityProof",
      "commitment_ref": ["C_codeword_hash_proof", "C_codeword_hash_enrolled"],
      "witness_binding": ["codeword_hash", "r_codeword"]
    },
    {
      "stmt_id": "record_membership",
      "type": "MembershipProof",
      "commitment_ref": "C_record_in_chain",
      "set": "chain_segment_hashes",
      "witness_binding": ["record_index", "r_record"]
    }
  ],
  "composition_layer": {
    "operator": "OR",
    "operands": ["duress_codeword_check", "record_membership"]
  },
  "deniability_shape": true,
  "anchor_freshness_window_seconds": 86400
}
```

**Generation flow:**

1. Operator loads circuit_def for bank_teller_note_active.
2. Operator evaluates: is the duress codeword hash in the enrolled record, AND is that record in the recent chain? (boolean result, hidden).
3. Gather witnesses:
   - C_codeword_hash_proof: operator's local commitment to the codeword hash.
   - C_codeword_hash_enrolled: principal's enrolled codeword hash from VC.
   - C_record_in_chain: membership of the record in chain_segment_hashes.
4. **Critical deniability step:** Construct OR composition:
   - Prover computes the honest branch: either (duress_codeword_check matches) OR (record_membership matches).
   - Prover simulates the other branch.
   - Both branches return Fiat-Shamir challenges from the global oracle; honest branch responds with knowledge, simulated branch uses the simulated randomness.
5. Result: the proof shape is identical regardless of which branch is true. Verifier cannot distinguish whether the codeword matched or the record was found. Operator retains deniability: "I proved something is active, but the proof does not reveal what."

This is the structural deniability guarantee: the proof always evaluates both branches' commitments, but only one branch's knowledge is revealed.

## Proof Bundle Structure

```
{
  "predicate_id": "base64(...)",
  "predicate_version": "1",
  "public_inputs": {
    "commitments": { "C_distance": "base64(...)", ... },
    "parameters": { "tau_pub": 50, ... },
    "chain_head": "base64(block_hash)",
    "timestamp": 1716201600
  },
  "atomic_proofs": [
    {
      "stmt_id": "stmt_1",
      "proof_type": "RangeProof",
      "proof_data": "base64(bulletproof_bytes)",
      "fiat_shamir_challenge": "base64(challenge_32_bytes)"
    },
    ...
  ],
  "anchor_proof": {
    "sigsum_leaf_index": 12345,
    "sigsum_tree_head": "base64(...)",
    "sigsum_tree_proof": "base64(...)"
  },
  "operator_signature": "base64(schnorr_sig_64_bytes)"
}
```

**Invariants:**
- Public inputs are deterministic given the predicate and operator state.
- Atomic proofs are serialized in the order declared in circuit_def.
- Fiat-Shamir challenges are computed over a rolling transcript: each challenge binds to (predicate_id, prior_challenges, current_statement_type).
- Operator signature covers the entire public-inputs + atomic-proofs concatenation.
- Bundle is immutable after signing: any modification breaks the signature.

## Proof Generation Algorithm

**Input:** predicate_id, operator_state (chain, commitments, witnesses, VC cache).

**Output:** proof_bundle (or error).

```
Load circuit_def ← registry[predicate_id]
result_bit ← evaluate_predicate(predicate_id, operator_state)
  // Side-effect computed; not part of proof.

fiat_shamir_transcript ← hash(predicate_id)
atomic_proofs ← []

For each atomic_statement in circuit_def.atomic_statements:
  stmt_type ← atomic_statement.type
  
  Case stmt_type of:
    "RangeProof":
      (v, r, N) ← gather_witnesses(atomic_statement.witness_binding, operator_state)
      bp_proof ← bulletproofs_prove(v, r, N)
      challenge ← fiat_shamir(fiat_shamir_transcript || bp_proof || stmt_type)
      fiat_shamir_transcript ← hash(fiat_shamir_transcript || challenge)
      atomic_proofs.append((stmt_id, "RangeProof", bp_proof, challenge))
    
    "EqualityProof":
      (v, r_A, r_B, C_A, C_B) ← gather_witnesses(...)
      schnorr_proof ← schnorr_equality_prove(v, r_A, r_B, C_A, C_B)
      challenge ← fiat_shamir(fiat_shamir_transcript || schnorr_proof || stmt_type)
      fiat_shamir_transcript ← hash(fiat_shamir_transcript || challenge)
      atomic_proofs.append((stmt_id, "EqualityProof", schnorr_proof, challenge))
    
    "MembershipProof":
      (v, r, set_index, set_root) ← gather_witnesses(...)
      sigma_or_proof ← sigma_membership_prove(v, r, set_index, set_root, set_size)
      challenge ← fiat_shamir(fiat_shamir_transcript || sigma_or_proof || stmt_type)
      fiat_shamir_transcript ← hash(fiat_shamir_transcript || challenge)
      atomic_proofs.append((stmt_id, "MembershipProof", sigma_or_proof, challenge))

chain_head ← operator_state.chain.current_head()
anchor_proof ← sigsum_prove_inclusion(chain_head, operator_state.sigsum_tree)

proof_bundle.predicate_id ← predicate_id
proof_bundle.predicate_version ← circuit_def.version
proof_bundle.atomic_proofs ← atomic_proofs
proof_bundle.chain_head ← chain_head
proof_bundle.anchor_proof ← anchor_proof
proof_bundle.timestamp ← now()

bundle_bytes ← serialize(proof_bundle)
signature ← schnorr_sign(bundle_bytes, operator_private_key)
proof_bundle.operator_signature ← signature

Return proof_bundle
```

## Verification Algorithm

**Input:** proof_bundle, circuit_def (from registry or cached), operator_vc_public_key.

**Output:** True (all proofs valid) or False.

```
Verify Sigsum anchor:
  If sigsum_verify_inclusion(proof_bundle.anchor_proof, known_tree_head) fails:
    Return False

Load circuit_def from registry by proof_bundle.predicate_id
fiat_shamir_transcript ← hash(proof_bundle.predicate_id)

For each atomic_proof in proof_bundle.atomic_proofs:
  stmt_type ← atomic_proof.proof_type
  proof_data ← atomic_proof.proof_data
  challenge ← atomic_proof.fiat_shamir_challenge
  
  Case stmt_type of:
    "RangeProof":
      commitment ← proof_bundle.public_inputs.commitments[atomic_proof.stmt_id]
      range_bound ← proof_bundle.public_inputs.parameters[...]
      If NOT bulletproofs_verify(proof_data, commitment, range_bound, challenge):
        Return False
    
    "EqualityProof":
      (C_A, C_B) ← extract_commitments(proof_bundle.public_inputs, atomic_proof)
      If NOT schnorr_verify_equality(proof_data, C_A, C_B, challenge):
        Return False
    
    "MembershipProof":
      (commitment, set_root) ← extract_set_data(proof_bundle.public_inputs, atomic_proof)
      If NOT sigma_verify_membership(proof_data, commitment, set_root, challenge):
        Return False
  
  // Reconstruct Fiat-Shamir challenge identically.
  expected_challenge ← fiat_shamir(fiat_shamir_transcript || proof_data || stmt_type)
  If expected_challenge != challenge:
    Return False
  
  fiat_shamir_transcript ← hash(fiat_shamir_transcript || challenge)

// Verify operator signature.
bundle_bytes ← serialize(proof_bundle without operator_signature)
If NOT schnorr_verify(proof_bundle.operator_signature, bundle_bytes, operator_vc_public_key):
  Return False

Return True
```

## Performance Targets

Per Everest 42 and Everest 88 performance requirements:

- **Single-predicate proof generation:** <500ms on M-series Mac (in-memory witnesses, chain cached).
- **Multi-predicate aggregate (4 predicates in parallel):** <1s (operator processes in-flight).
- **Verification:** equivalent (verifier is stateless; no chain lookups required beyond Sigsum anchor verification).

**Breakdown (typical case):**
- RangeProof (Bulletproof): 200ms generation, 5ms verification.
- EqualityProof (Schnorr): 5ms generation, 1ms verification.
- MembershipProof (Sigma-set, k=16): 40ms generation, 40ms verification.
- Aggregate AND (3 proofs): 250ms generation, 50ms verification.
- Signature + serialization: 10ms.

Parallelization: predicates with independent witnesses can be proven concurrently; Fiat-Shamir transcripts are independent per predicate, enabling SIMD-style batch proving.

## Implementation: calm-witness-zk-rs

**Crate structure:**

```
calm-witness-zk-rs/
  src/
    lib.rs
    circuit_def.rs          // Circuit definition parsing, validation.
    atomics/
      bulletproof.rs        // RangeProof wrapper.
      schnorr.rs            // EqualityProof, SchnorrSignature.
      sigma_set.rs          // MembershipProof.
    generator.rs            // ProofGenerator: orchestrates generation.
    verifier.rs             // ProofVerifier: verifies bundles.
    fiat_shamir.rs          // Transcript management.
    bundle.rs               // ProofBundle serialization/deserialization.
    anchor.rs               // Sigsum anchor integration.
  Cargo.toml                // Dependencies: bulletproofs, curve25519-dalek, sha2, serde.
```

**Key dependencies:**
- `bulletproofs`: Range proofs (no trusted setup).
- `curve25519-dalek`: Schnorr, Sigma protocols on Curve25519.
- `sha2`: Fiat-Shamir transcript hashing (SHA-256).
- `serde` / `bincode`: Serialization.

**Example API (Rust):**

```rust
pub struct ProofGenerator {
    registry: Arc<PredicateRegistry>,
    operator_state: OperatorState,
}

impl ProofGenerator {
    pub fn generate(&self, predicate_id: &str) -> Result<ProofBundle, ProofError> {
        let circuit_def = self.registry.load(predicate_id)?;
        let witnesses = self.gather_witnesses(predicate_id)?;
        let bundle = self.generate_atomic_proofs(&circuit_def, &witnesses)?;
        let signed_bundle = self.sign_bundle(bundle)?;
        Ok(signed_bundle)
    }

    fn gather_witnesses(&self, predicate_id: &str) -> Result<Witnesses, ProofError> {
        match predicate_id {
            "in_baseline_24h" => {
                Ok(Witnesses {
                    template_id: self.operator_state.template_id(),
                    chain_head: self.operator_state.chain.head(),
                    affect_overlap: self.compute_affect_overlap()?,
                })
            }
            "biometric_match_within" => {
                Ok(Witnesses {
                    distance: self.operator_state.biometric_distance()?,
                    template_id: self.operator_state.template_id(),
                    chain_head: self.operator_state.chain.head(),
                })
            }
            _ => Err(ProofError::UnknownPredicate),
        }
    }
}

pub struct ProofVerifier;

impl ProofVerifier {
    pub fn verify(
        bundle: &ProofBundle,
        registry: &PredicateRegistry,
        operator_vk: &VerifyingKey,
    ) -> Result<(), VerifyError> {
        let circuit_def = registry.load(&bundle.predicate_id)?;
        
        // Verify Sigsum anchor.
        verify_sigsum_inclusion(&bundle.anchor_proof)?;
        
        // Verify each atomic proof.
        let mut transcript = Transcript::new(b"calm-witness-predicate");
        transcript.append_message(b"predicate_id", bundle.predicate_id.as_bytes());
        
        for atomic_proof in &bundle.atomic_proofs {
            verify_atomic_proof(atomic_proof, &circuit_def, &mut transcript)?;
        }
        
        // Verify operator signature.
        verify_operator_signature(&bundle, operator_vk)?;
        
        Ok(())
    }
}
```

## Cross-References and Dependencies

This Everest is the direct output of:
- **Everest 44** (Pedersen Commitment Distance): foundational commitment schemes.
- **Everest 45** (ZK Range Proof Distance): Bulletproofs DSL.
- **Everest 46** (Pedersen Commitment Template ID): template commitment protocol.
- **Everest 51** (Predicate Framework): logical predicate definitions.
- **Everest 52** (Predicate Registry Schema): storage and retrieval of circuit definitions.
- **Everest 53** (Predicate Authoring Tools): DSL and registration workflow.
- **Everest 54** (Predicate Operator Lifecycle): operator state management and witness sourcing.
- **Everest 55** (in_baseline_24h Predicate): worked example.
- **Everest 56** (biometric_match_within Predicate): worked example.
- **Everest 57–62** (additional predicates): future templates.
- **Everest 81** (Rust Implementation Strategy): crate organization and build pipeline.
- **Everest 88** (Performance & Scalability Requirements).

**Calm Pact §4** (Σ-protocol primitives): theoretical foundations for atomic proof composition.

## Conclusion

Everest 65 completes the cryptographic core of the Calm Witness attestation layer. By decoupling circuit definitions (static, registry-managed) from proof generation (dynamic, operator-driven), the system achieves both rigor and flexibility. The choice of Bulletproofs + Sigma-protocols avoids the trusted-setup burden while delivering sub-500ms proofs suitable for real-time biometric and duress-codeword verification.

The per-predicate generator enforces declarative proof circuits, preventing accidental witness leakage and ensuring verifiers gain only the intended assurances. Worked examples (in_baseline_24h, biometric_match_within, bank_teller_note_active) demonstrate the breadth of predicates the framework supports, from equality checks to range proofs to disjunctive deniability.

Implementation in `calm-witness-zk-rs` leverages battle-tested cryptographic libraries, prioritizing correctness and auditability over exotic optimization. The verifier algorithm is deterministic and offline: no trusted infrastructure required beyond Sigsum anchor verification.

— Calm, 2026-05-20
