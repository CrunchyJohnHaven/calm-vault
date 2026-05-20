# Calm Witness Documentation Portal

> **Closes Everest 237 of [ZKAC_NEXT_200_EVERESTS.md](ZKAC_NEXT_200_EVERESTS.md)**

## Welcome

**Calm Witness** is a zero-knowledge behavioral-biometric channel by which one autonomous AI agent discloses one safety-relevant bit about its human principal to another autonomous AI agent without revealing the principal's identity, biometrics, or any other signal. The Calm Stack extends this primitive into a full cryptographic protocol suite for attested context (Pact, Witness, Tenancy, Compass, Concord) and is the infrastructure substrate for autonomous-agent coordination in the post-consent era.

---

## Documentation by Audience

### For Principals (Non-Engineers)

Start here if you are the human owner of a Calm vault and want to understand what is happening.

- **[SELF_HELP_FOR_PRINCIPALS_v0.md](SELF_HELP_FOR_PRINCIPALS_v0.md)** — Consent mechanics, evidence ownership, vault safety, how to revoke.
- **[CALM_WITNESS_SCOPE_STATEMENT.md](CALM_WITNESS_SCOPE_STATEMENT.md)** — What Calm Witness can and cannot do; prohibited uses (credit, employment, custody, insurance, immigration, evidence).
- **[NAMING_AND_BRANDING.md](NAMING_AND_BRANDING.md)** — Official names, glossary, trademark guidance.

### For Counterparty Implementers

Build a system that verifies Calm Witness envelopes and trusts the proofs.

- **[CALM_WITNESS_WIRE_FORMAT_v0.md](CALM_WITNESS_WIRE_FORMAT_v0.md)** — Envelope schema, message flow, serialization, verification constants.
- **[~/CredexAI/calm_witness/README.md](~/CredexAI/calm_witness/README.md)** — Python reference implementation; five quick-start patterns (verify chain, validate records, evaluate predicates, construct proofs, build envelopes).
- **[ZKBB_USER_PROTOCOL_v0.md](ZKBB_USER_PROTOCOL_v0.md)** — Complete protocol specification; threat model; biometric-distance machinery; consent calculus.

### For Predicate Authors

Author new named bits and evidence kinds for the principal to disclose.

- **[PREDICATE_VOCABULARY_v0.md](PREDICATE_VOCABULARY_v0.md)** — Enumerated v0 predicates with formal semantics, ID stability rules, protected-category floor.
- **[PREDICATE_AUDIT_PROCESS_v0.md](PREDICATE_AUDIT_PROCESS_v0.md)** — Peer-review committee composition, golden-corpus rules, falsifiability protocol, scope enforcement.
- **[COMPASS_PREDICATES_v0.md](COMPASS_PREDICATES_v0.md)** — Values-attestation predicates (unselfish, cross-group-engagement, refused-opportunity-to-harm, respect-for-difference, no-known-willful-harm, willing-to-be-corrected).

### For Cryptographers

Audit and extend the zero-knowledge proofs.

- **[~/CredexAI/calm_witness/zk.py](~/CredexAI/calm_witness/zk.py)** — Pedersen commitments, Σ-protocol bit proofs, range proofs, envelope signature.
- **[POST_QUANTUM_MIGRATION_PLAN_v0.md](POST_QUANTUM_MIGRATION_PLAN_v0.md)** — Lattice-based successor roadmap; FIPS 203 + 204 integration timeline; security assumptions.
- **[EVEREST_44b_PEDERSEN_RISTRETTO_v0.md](EVEREST_44b_PEDERSEN_RISTRETTO_v0.md)** — Pedersen parameters, Ristretto curve selection, commitment-strength proofs.

### For Policy & Standards Bodies

Integrate Calm Witness into law, regulation, and international standards.

- **[NIST_SUBMISSION_DRAFT.md](NIST_SUBMISSION_DRAFT.md)** — NIST cryptographic standards alignment; special publication reference; conformance checklist.
- **[CALM_WITNESS_SCOPE_STATEMENT.md](CALM_WITNESS_SCOPE_STATEMENT.md)** — Legal scope, liability, non-commercial licensing, jurisdiction constraints.
- **[PUBLIC_PREDICATE_REGISTRY_GOVERNANCE.md](PUBLIC_PREDICATE_REGISTRY_GOVERNANCE.md)** — Registry stewardship, predicate-naming authority, appeal process, sunset rules.

---

## The Calm Stack: Five Pillars

### 1. **Calm Pact** — Mission Equality

Proves that two autonomous agents share an explicit, written mission statement (the Pact). The principal drafts the Pact once, signs it once, and then any agent claiming to hold it must prove possession without revealing the Pact itself. Enables safe delegation.

- **[CALM_PACT_PROTOCOL_v0.md](CALM_PACT_PROTOCOL_v0.md)** — Full spec.
- **Status:** All 30 Everests in [CALM_PACT_EVERESTS_30.md](CALM_PACT_EVERESTS_30.md) are **BAGGED**.

### 2. **Calm Witness** — State Baseline

Proves that the principal's behavioral biometric (baseline affect, voice modulation, keystroke dynamics) remains in the observed range *right now*, within the last 24 hours. No identity leak. One bit: in-baseline-or-not. The bank-teller note for autonomous agents.

- **[ZKBB_USER_PROTOCOL_v0.md](ZKBB_USER_PROTOCOL_v0.md)** — Full spec.
- **[ZKBB_USER_EVERESTS_100.md](ZKBB_USER_EVERESTS_100.md)** — Route map from Phase I (foundations) through Phase VIII (governance & scale).
- **Status:** All 100 Everests in ZKBB_USER_EVERESTS_100.md are **BAGGED**.

### 3. **Calm Tenancy** — Multi-Principal Vaults

Extends Calm Pact and Witness to multi-principal operation: one vault holds attestation chains for multiple principals, with separate keys, separate evidence, and zero cross-talk. Enables shared operators and custody-free federation.

- **[CALM_TENANCY_PROTOCOL_v0.md](CALM_TENANCY_PROTOCOL_v0.md)** — Full spec.
- **Status:** 50 of 50 Everests in [CALM_TENANCY_EVERESTS_50.md](CALM_TENANCY_EVERESTS_50.md) are **BAGGED**.

### 4. **Calm Compass** — Values Attestation

Proves that the principal's behavioral evidence supports a small set of named values predicates: unselfish, untribal, respect-across-difference, no willful harm. Same protective floor as Witness. The principal authors evidence; a panel of philosophers, ethicists, and harm recipients audits the predicates; explicit refusal floor on protected categories.

- **[CALM_COMPASS_PROTOCOL_v0.md](CALM_COMPASS_PROTOCOL_v0.md)** — Full spec.
- **[COMPASS_PREDICATES_v0.md](COMPASS_PREDICATES_v0.md)** — Values vocabulary.
- **Status:** 50 of 50 Everests in [CALM_COMPASS_EVERESTS_50.md](CALM_COMPASS_EVERESTS_50.md) are **BAGGED**.

### 5. **Calm Concord** — Multi-Primitive Composition

Unifies Pact, Witness, Tenancy, and Compass into a single disclosure request/response flow. A counterparty asks: *"Pact == X AND Witness.in_baseline_24h AND Compass.no_known_harm_365d"*; receives a composite zero-knowledge proof; verifies once.

- **[CALM_CONCORD_PROTOCOL_v0.md](CALM_CONCORD_PROTOCOL_v0.md)** — Full spec.
- **Status:** 50 of 50 Everests in [CALM_CONCORD_EVERESTS_50.md](CALM_CONCORD_EVERESTS_50.md) are **BAGGED**.

---

## Route Maps

### User-Facing Everests (100 summits)

The first 100 engineering Everests build Calm Witness from foundations through governance & scale. Phase I covers problem statement, threat model, naming, glossary. Phase VIII covers standards, deployment, third-party verification.

- **[ZKBB_USER_EVERESTS_100.md](ZKBB_USER_EVERESTS_100.md)** — Complete route map with prerequisites, effort estimates, and acceptance tests.

### The Next 200 Engineering Everests (summits 101–300)

Extensions to Witness and the broader ZKAC programme. Ranges I–M cover Compass (101–120), cross-primitive substrate (121–200). Ranges N–R cover standards, ecosystem, and long-term sustainability (201–300).

- **[ZKAC_NEXT_200_EVERESTS.md](ZKAC_NEXT_200_EVERESTS.md)** — Complete route map and phase legend.

---

## Conformance & Testing

### Reference Implementation

The Python reference implementation is suitable for research, integration testing, and counterparty-side verification.

- **Path:** `~/CredexAI/calm_witness/`
- **Key modules:**
  - `verify_chain.py` — Chain validation against v0 schema.
  - `predicates.py` — Predicate evaluator loader and validator.
  - `zk.py` — Zero-knowledge proof primitives (Pedersen, Σ-protocol, range proofs).
  - `envelope.py` — Disclosure envelope construction and verification.
  - `cli.py` — Command-line interface for testing and scripting.

### Conformance Gates

Per Everest convention, each released summit has a peer gate script at `~/CredexAI/scripts/everest_NN_zkbb_<slug>_gate.py`. Run gates to verify reference-implementation conformance:

```bash
python ~/CredexAI/scripts/everest_06_zkbb_predicate_vocabulary_gate.py
python ~/CredexAI/scripts/everest_08_zkbb_consent_calculus_gate.py
# ... etc for all completed Everests
```

All v0 Everests green.

---

## Quick Links

- **[CALM_WITNESS_MANIFESTO.md](CALM_WITNESS_MANIFESTO.md)** — The vision: why autonomous agents need Calm Witness.
- **[CALM_STACK_v0.md](CALM_STACK_v0.md)** — High-level integration guide for the five pillars.
- **[CALM_WITNESS_TALES.md](CALM_WITNESS_TALES.md)** — Use-case narratives (financial coordination, multi-agent governance, trust cascades).
- **[HARM_TAXONOMY_v0.md](HARM_TAXONOMY_v0.md)** — Harms Calm Witness does and does not prevent; mitigations.
- **[V0_RELEASE_READINESS_ASSESSMENT.md](V0_RELEASE_READINESS_ASSESSMENT.md)** — Security audit status, test coverage, deployment readiness.

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
