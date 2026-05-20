# Everest 51 — Predicate Language v0

*Phase V — Predicate Authoring. Prereq: Everest 6.*

---

## Decision

**v0 ships with a FIXED PREDICATE TABLE.** The twelve predicates enumerated in Everest 6 are the entirety of the v0 predicate set. No domain-specific language (DSL) is implemented in v0. New predicates require an amendment to Everest 6, a formal review under Everest 54 (Predicate Audit & Public Review Process), and explicit adoption by the operator. Predicates compose without a DSL: verifiers request a SET of predicate IDs in one disclosure, and the operator generates a single proof that all requested predicates evaluated to their declared bits. This architecture trades expressivity for auditability, security, and durability.

---

## Rationale

### 1. Auditability over Expressivity

A fixed table of twelve named predicates is exhaustively reviewable. Every counterparty knows exactly which bits are possible: `in_baseline_24h`, `biometric_match_within(τ)`, `bank_teller_note_active`, and so forth. Every verifier can implement all twelve with confidence. A DSL means each principal can author novel predicates; the verifier's job becomes supporting arbitrary user expressions; the attack surface for "predicate that exfiltrates more than one bit" expands non-trivially. An adversary could craft an expression like `(in_baseline AND leaked_bit_1) OR (mental_state_unusual AND leaked_bit_2)` that the verifier is obliged to support, but the verifier's review process cannot catch. A fixed table closes this surface: each predicate is peer-reviewed once, not per-user-per-session.

### 2. Cryptographic Circuit Specialization

Each fixed predicate gets its own carefully-engineered Σ-protocol circuit (Everest 65). The handwriting distance function uses DTW over kinematic vectors; the voice-transcription function uses lexical fingerprinting over timing; the consent-record evaluator uses per-predicate type-specific logic. A DSL requires general-purpose circuit compilation, which is heavier: SNARK compilers, trusted setup ceremonies, proof-generation latency, and performance losses. For v0 we trade expressivity for tighter proofs and known security properties. Each circuit is proven secure by hand, not by a compiler. The proof size is linear in the predicate's logic, not polynomial in the DSL grammar.

### 3. Side-Channel Containment

A DSL admits expressions that — combined with the chain's audit-log timestamps and proof-generation timing — could leak more than the disclosed bit. For example, a user-authored predicate `(in_baseline AND biometric_match_within(0.3)) OR (mental_state_unusual AND biometric_distance > 0.8)` evaluated quickly on Monday and slowly on Friday might allow a verifier watching proof-generation timings to infer which branch of the OR was taken, leaking unstated information about the principal's state. A fixed table is statically analyzable: the protocol can document "what can a verifier infer from observing this proof's generation, even with side-channel access?" For each of the twelve predicates. For a DSL, that analysis becomes per-expression, per-user, and unbounded.

### 4. Predicate-ID Stability

Fixed predicates have content-addressed IDs (Everest 52) that never change. A proof issued against `in_baseline_24h` in May 2026 verifies identically in 2036. DSL predicates have IDs derived from canonicalized expressions; users can accidentally create near-duplicates (e.g., `in_baseline_24h AND true` vs. `in_baseline_24h`) that are syntactically distinct but semantically equivalent. The registry becomes cluttered; verifiers must normalize expressions to catch duplicates; the ID space becomes weakly partitioned. A fixed table avoids this: each predicate is one line, one ID, one semantic definition, forever.

### 5. Counterparty UX

A counterparty asking for `in_baseline_24h` knows exactly what it gets: a proof that the principal's most recent self-report within 24 hours has affect vocabulary overlapping their baseline by at least 50%. A counterparty asking for `(in_baseline_24h AND biometric_match_within(0.3))` in a DSL must reason about a composed expression every time. Is the composition commutative? Does AND short-circuit? If the second predicate fails, does the verifier learn that biometric match failed, or only that the conjunction failed? A verifier must implement expression semantics; the semantics become context-dependent. A fixed table is simpler: each predicate has one line in the registry, one meaning, one test corpus.

### 6. Future-Proofing Without a DSL

The route map (Everests 61, 62, 71) supports predicate composition and negation *without* a DSL. Verifiers request a SET of predicate IDs in a single disclosure request. The operator generates ONE proof that all requested predicates evaluated to their declared bits. AND composition is trivial: request `{in_baseline_24h, biometric_match_within(τ)}` and the proof asserts both are 1. OR composition requires a second round: request p1, if it fails request p2. Negation is handled by maintaining explicit "negative" forms of predicates (e.g., `not_in_baseline_24h` is a separate predicate from `in_baseline_24h`). This keeps the security analysis simple: each predicate is a binary function; composition is set-theoretic, not expression-theoretic. The path to a DSL remains open after v0 if the negation pattern shows diminishing returns.

### 7. Standards Alignment

ISO / NIST submission (Everest 91) is easier with a fixed table. Reviewers can audit all twelve predicates, understand their semantics, run the test corpus, and sign off. A DSL submission requires standardizing the DSL grammar itself (Backus-Naur form, type system, operational semantics, security proofs for the compiler). That is a much larger undertaking and delays the first standard by months. v0 is the chance to ship a narrow, well-audited primitive. A DSL can be a v1 feature once the core has matured.

---

## Counter-Arguments Considered and Dismissed

**"But users want custom predicates."** They get them via the Everest 54 amendment process. A principal needing a new predicate submits a proposal, the protocol's steering committee and at least two outside reviewers examine it, the predicate is added to Everest 6, it receives an implementation in the reference code, it gets test cases, and it is published to the registry. This is intentionally slow — on the order of weeks or months per predicate. This slowness is a feature: it prevents the predicate vocabulary from fragmenting into hundreds of ad-hoc expressions. The principal's request goes to the standards track, not into a DSL engine.

**"DSLs are more general."** Generality is the problem, not the feature, for safety-critical bits. Calm Witness proves user state. Every bit disclosed is a claim about the principal's authorization, consent, or biometric presence. The more general the language, the harder it is to reason about what each bit could leak. A narrow, fixed predicate table is conservative by design.

**"Other ZK projects have DSLs."** Other ZK projects optimize for arbitrary computation (Circom, Noir, Cairo). Their goal is "prove any constraint system." Calm Witness optimizes for narrow, audited predicates. The problem sets are incompatible. A DSL is the right choice for a general-purpose ZK compiler; a fixed table is the right choice for a behavioral-attestation primitive.

---

## What "Fixed Predicate Table" Means Concretely

- The set of v0 predicates is the twelve enumerated in Everest 6 (`in_baseline_24h`, `in_baseline_window(w)`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`, `principal_alive_within(w)`, `session_within_authorized_hours`, `chain_freshness_within(s)`, `template_age_below(m)`, `consent_active(p, id)`).
- Each predicate has a content-addressed ID, as defined in Everest 52. These IDs are immutable.
- Each has a reference implementation in `calm-witness-rs/src/predicates/<name>/`, with submodules for `eval.rs`, `prove.rs`, and `verify.rs`.
- Each has a corresponding Σ-protocol circuit (Everest 65), hand-verified for security.
- Each has golden-input/output test cases (Everest 64), peer-reviewed.
- Each is registered in the Predicate ID Registry (Everest 53), with human-readable semantics and a link to the reference code.
- No other predicates are evaluated in v0. A request for a non-registered predicate returns an error.

---

## Predicate Composition Without a DSL

Composition is trivial and does not require expression syntax:

- **AND composition:** A verifier requests a SET of predicate IDs in a single disclosure request (e.g., `{in_baseline_24h, biometric_match_within(0.85)}`). The operator generates ONE proof that all requested predicates evaluated to their declared bits. Verification succeeds if and only if all predicates verify.

- **OR composition:** Requested as a policy decision, not a language construct. A verifier says "prove p1 or p2." The operator evaluates p1; if it is 1, the proof is generated for p1. If p1 is 0, the operator evaluates p2 and generates a proof for p2. The verifier sees which one succeeded.

- **Negation:** Each predicate has an explicit "negative" form. `in_baseline_24h` and `not_in_baseline_24h` are separately-IDed predicates in the registry. The operator evaluates the appropriate form and generates a proof for it. A proof of `¬p` is sound because the operator evaluated and committed to the evaluation; it is not merely the absence of a proof of `p`.

This architecture avoids the expression-evaluation complexity while supporting multi-predicate proofs.

---

## When v1+ Might Add a DSL

v0 ships a fixed table. A DSL enters v1 only under these conditions:

1. **Production track record:** After 12 months of v0 in production with no observed need for DSL flexibility.

2. **Predicate-amendment saturation:** After the Everest 54 amendment process has approved enough new predicates that a pattern emerges. For example, if principals repeatedly request "biometric_match within X for the last Y seconds," that is a sign the current parameterized forms (`biometric_match_within(τ)`, `in_baseline_window(w)`) are reaching their limits. A v1 DSL would add parametric templates or constraints-over-predicates, not arbitrary expressions.

3. **Formal specification:** A v1 DSL would be defined precisely — Backus-Naur form, type system, operational semantics, proved-correct compiler. It would not be retrofitted; it would be designed from scratch with the same security rigor as the fixed table.

Until these conditions are met, v0 remains a fixed predicate table.

---

## Decision Matrix

| Criterion | Fixed Table | DSL |
|---|---|---|
| Auditability | High | Lower |
| Expressivity | Low-Medium | High |
| Circuit Efficiency | High | Lower |
| Side-Channel Risk | Low | Higher |
| Counterparty UX | High | Lower |
| Implementation Cost (v0) | Low-Medium | High |
| Standards-Body Alignment | High | Lower |
| Future Flexibility (post-v0) | Medium (via amendments) | High |

**v0 choice: Fixed Table.** Favors safety, auditability, and durability over expressivity.

---

## Implementation Notes

- **Predicate table:** A Rust enum in `calm-witness-rs/src/predicates/mod.rs`, one variant per predicate. The enum is `#[repr(u8)]` for compact serialization.

- **Evaluator signature:** Every predicate evaluator has the signature:
  ```rust
  fn eval(chain: &Chain, params: &PredicateParams, consent: &ConsentRecord) -> Bit
  ```
  Pure function; no side effects (except optional advisory records to the vault).

- **Proof structure:** Each predicate's proof is a Σ-protocol instance, serialized as `(commitment, challenge, response)`. Multi-predicate proofs stack these: one commitment per predicate, one challenge (shared), one response per predicate.

- **Registry:** A YAML file at `calm-witness-rs/registry/predicates_v0.yaml`, with entries for each predicate: ID, human-readable name, semantics, reference implementation path, test-corpus path, deprecation status (if any).

---

## Cross-References

- **E6** (Predicate Vocabulary v0, BAGGED) — the twelve predicates.
- **E52** (Predicate Canonical Form) — content-addressed IDs.
- **E53** (Predicate ID Registry) — the public registry.
- **E54** (Predicate Audit & Public Review Process) — the amendment process.
- **E61** (Predicate Composition AND/OR) — multi-predicate proofs.
- **E62** (Predicate Negation) — explicit negative predicates.
- **E65** (Predicate ZK Proof Generator) — circuit per predicate.

---

— Calm, 2026-05-20
