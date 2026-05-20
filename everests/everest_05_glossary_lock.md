# Everest 5 — Glossary Lock

*Phase I — Foundations. Prereq: Everest 1, Everest 3.*

---

**Affect** — A set of emotional or cognitive states (e.g., calm, alert, distressed) self-reported by the principal during hydration, used as baseline vocabulary for baseline-checking predicates.

**Append-Only** — A property of data structures (notably `user_state.jsonl`) that guarantees no prior record can be modified after creation; violations are cryptographically detectable via *hash chain* integrity.

**Baseline** — The principal's self-declared normal state (affect, biometric distance, behavior patterns), established at *enrollment ceremony* and used as the reference against which later samples are compared.

**Bank-Teller Note** — The core primitive of Calm Witness: an unforgeable, information-minimal message that one party (the operator) can pass to a counterparty conveying only one bit of safety-relevant state (e.g., "the human is in baseline") without revealing biometrics, transcripts, or other sensitive data.

**Biometric Distance** — A numerical score (typically 0–1) quantifying the dissimilarity between a current behavioral sample and an enrolled *biometric template*, computed by *handwriting* or *voice-transcription* comparators.

**Biometric Template** — An encrypted, principal-controlled summary of behavioral signatures (stroke kinematics, lexical patterns, timing) collected during *enrollment ceremony*, used as the reference against which session samples are compared.

**Calm Pact** — Sister protocol to Calm Witness (see *Calm Witness*); proves categorical directive equality between two autonomous AI agents without revealing the directives.

**Calm Session** — A bounded interaction during which the principal provides a self-report + optional behavioral samples to the operator, and the operator evaluates one or more *predicates* and optionally generates a *disclosure*.

**Calm Witness** — A zero-trust, behavioral-biometric protocol enabling a Calm operator to attest to a counterparty agent that the principal is in baseline (or not, if authorized) via cryptographic proof, without leaking biometrics, medical state, or self-narration. Technical name: *ZKBB-User*.

**Chain** — Short for *hash chain*. See *hash chain*.

**Chain Head** — The most recent *record* in a *hash chain*, whose `record_hash` serves as the cryptographic commitment to all prior history. Published to *Sigsum* for tamper-evidence.

**Commitment (Pedersen)** — A cryptographic binding: a public value `Com(x; r) = g^x · h^r` (on a group with generators `g, h` of unknown discrete-log relation) that hides `x` (hiding property) while committing the party to a specific value (binding property). Used throughout to commit *predicates*, *templates*, *distances*.

**Consent Record** — An append-only entry in `user_state.jsonl` (kind = `consent`) binding a principal's explicit authorization to disclose a specific *predicate* to a specific *counterparty class*, with time bounds and revocation semantics.

**Counterparty** — An autonomous AI agent (operated by another principal) requesting a *disclosure* from the Calm operator on behalf of its principal.

**Counterparty Class** — A categorical grouping of counterparties (e.g., financial, journalistic, medical, governmental, peer-AI-collective) to which the principal grants or withholds blanket consent for *disclosure* of specific *predicates*.

**CredexAI** — A verifiable-credential SDK and identity-attestation infrastructure used to issue and verify *verifiable credentials* binding operators and principals to registered legal entities.

**Disclosure** — The act of a Calm operator sending a *counterparty* a *bank-teller note* (a ZK proof + *commitment*) that the principal satisfies a named *predicate*, with freshness and operator-identity bindings, without leaking the underlying *record* or biometric.

**Disclosure Class** — See *counterparty class*.

**Drift** — Gradual, natural shift in behavioral signatures over time (handwriting style, speech patterns, affect vocabulary) that must be modeled to avoid false-reject errors; distinguished from *stale* samples or acute state change.

**Duress Codeword** — A per-principal-secret string that, when written into a self-report payload, flips the *bank_teller_note_active* *predicate* to true, signaling duress or coercion; opaque to any party other than the principal and the operator.

**Enrollment Ceremony** — A formal, witnessed session during which a principal provides N≥7 handwriting samples + N≥7 voice-transcription samples spanning multiple emotional states, producing an encrypted *biometric template* that will serve as the baseline for all later *biometric distance* evaluations.

**Fiat-Shamir** — A cryptographic technique that converts an interactive Σ-protocol (3-round commitment-challenge-response) into a non-interactive version by replacing the verifier's random challenge with a hash of the commitment; used in Calm Witness *proofs*.

**Genesis Record** — The first entry in a principal's `user_state.jsonl`, encoding the principal-identity binding, operator-identity binding, and protocol version at vault-creation time.

**Hash Chain** — An append-only linked list of records where each record contains the hash of the previous record in its `prev_hash` field; any tampering invalidates all downstream hashes, providing structural tamper-evidence.

**Hydration** — The session-intake phase of Calm Witness (§4.1) during which the operator collects a structured self-report and optional behavioral samples from the principal, appends them to `user_state.jsonl`, and publishes the *chain head* to *Sigsum*.

**JSONL** — JSON Lines: a text format where each line is a complete, independent JSON object (no array wrapper), used for `user_state.jsonl` to enable append-only, streaming log semantics.

**Liveness Detection** — A capture-time verification that a biometric sample (handwriting stroke, voice transcription) originates from live input in the current session, not replay or pre-recording; typically based on entropy (pressure variance, timing jitter) that would be expensive to spoof.

**Operator** — An autonomous AI agent (e.g., Calm) operating on behalf of a *principal*, holding the principal's vault, evaluating *predicates*, and generating *disclosures*. Distinct from and subordinate to the *principal*.

**Pedersen Commitment** — See *commitment (Pedersen)*.

**Predicate** — A deterministic boolean function over a *record* window, *biometric distance*, and *consent record* (e.g., `in_baseline_24h`, `principal_consents_to_disclose_p_to(counterparty_class)`) whose truth value is committed and proven without revealing the underlying data.

**Predicate ID** — A content-addressed identifier (cryptographic hash of canonical form) binding a *predicate* to a specific semantic definition, enabling verifiers to check that the predicate evaluated was the one requested.

**Predicate Vocabulary** — The enumerated set of all *predicates* that may be evaluated in Calm Witness v0, each with formal semantics, *predicate ID*, and a public registry entry.

**Principal** — The human (e.g., John Bradley) on whose behalf a Calm *operator* acts; owns and controls the vault, authorizes *disclosure*, retains revocation rights.

**Proof** — A zero-knowledge cryptographic proof (typically a Σ-protocol or SNARK) that a *commitment* opens to a value satisfying a *predicate*, without revealing the value itself.

**Range Proof** — A *proof* that a committed numeric value falls within a specified range (e.g., `biometric_distance < τ`) without revealing the value; used in *biometric_match_within(τ)* *predicate*.

**Record** — A single JSON object in `user_state.jsonl`, timestamped, hash-chained, containing a self-report payload, biometric distance (if sampled), or administrative data; immutable once appended.

**Roughtime** — A secure clock / verifiable-delay-function service that provides tamper-evident timestamps independent of a single operator; composed with *Sigsum* to anchor *chain heads* in a verifiable external clock.

**Schnorr** — A discrete-log-based signature and Σ-protocol scheme; Calm Witness uses Schnorr-style proofs of knowledge to bind *commitments* and validate *predicates*.

**Sigma (Σ) Protocol** — A three-round interactive cryptographic protocol (commit, challenge, response) with special soundness; Calm Witness uses Σ-protocols to prove predicates over committed values. Made non-interactive via *Fiat-Shamir*.

**Sigsum** — An append-only transparency log with N-of-M operator collusion resistance, used to publish *chain heads* so that tampering is detectable by any third party holding a prior *chain head*.

**Stale** — A *record* or *biometric template* whose timestamp exceeds a configured freshness window; stale data may be rejected by *predicate* evaluation or disclosed only with explicit freshness-caveat binding.

**Stealth Disclosure** — An (optional) mode where a Calm operator pushes a *bank-teller note* to a pre-authorized *counterparty* (e.g., an emergency contact or trusted AI collective) without waiting for a *disclosure* request; used for duress signaling.

**Template** — See *biometric template*.

**Transparency Log** — A publicly auditable, append-only log (e.g., *Sigsum* + *Roughtime*) to which *chain heads* are published, enabling detection of vault tampering by any external verifier.

**Two-Handshake Mode** — The composition pattern of Calm Pact + Calm Witness where agents first verify directive equality (Calm Pact), then verify user state (Calm Witness), proceeding only if both succeed; cleanly aborts on either failure with no information leak.

**Vault** — The principal's encrypted, append-only local store holding `user_state.jsonl`, *biometric templates*, consent policies, and cryptographic keys; owned and controlled by the principal, not the operator.

**Verifiable Credential (VC)** — A cryptographically signed attestation issued by a *CredexAI* or other authority, binding an identifier (agent, human, legal entity) to a set of properties (e.g., "is the operator of Creativity Machine LLC"); used to bind identity to *disclosures*.

**Verifier** — A third party (including a *counterparty* agent) that receives a *disclosure* and cryptographically checks that it is a valid *proof* of a *predicate* over a freshly-anchored *chain head*, without gaining any other information.

**Witness (cryptographic)** — A secret value (e.g., biometric distance, predicate evaluation) bound into a *Pedersen commitment* such that a *proof* can attest to its properties without revealing it.

**Witness (ceremony role)** — An optional external party (notary, family member, aligned organization) who observes and cryptographically signs an *enrollment ceremony*, strengthening tamper-evidence against substitution attacks.

**ZKBB-User** — Technical name for Calm Witness. *ZKBB* = Zero-Knowledge Behavioral Biometric. *User* = attested to the end user (principal), not to peers.

**Zero-Knowledge** — A property of cryptographic *proofs* where a verifier becomes convinced of a statement's truth without learning anything beyond the truth of that statement (and its freshness window).

---

## Disambiguation pairs

**Operator vs. Principal** — The operator is the autonomous AI agent (Calm) acting on behalf of; the principal is the human who owns and controls the vault and retains ultimate revocation authority. The two are distinct actors with different trust assumptions.

**Predicate vs. Predicate ID** — A *predicate* is a named boolean function with formal semantics; a *predicate ID* is a content-addressed cryptographic hash binding that specific predicate to a verifier, enabling verifiers to ensure they evaluated the intended predicate.

**Witness (cryptographic) vs. Witness (ceremony role)** — In the cryptographic sense, a *witness* is a secret value (e.g., biometric distance, randomness in a *commitment*) that proves knowledge of without revealing. In the ceremony sense, a *witness* is a human or organization that observes and signs an *enrollment ceremony*, attesting to its integrity.

**Calm Pact vs. Calm Witness** — *Calm Pact* proves two autonomous AI agents share a categorically equivalent primary directive without revealing the directives. *Calm Witness* proves a principal is in baseline (or authorized state) without leaking biometrics or self-narration. They compose in the *two-handshake model*: align mission first, verify state second.

**Baseline vs. Drift** — *Baseline* is the principal's self-declared stable state (affect, behavior patterns) established at *enrollment ceremony*, used as the reference. *Drift* is gradual, natural evolution of behavioral signatures over months or years, modeled as an expected property rather than an anomaly or attack.

**Consent Record vs. Disclosure** — A *consent record* is a binding, auditable entry in the vault where the principal authorizes specific *predicates* to be disclosed to specific *counterparty classes*, with time bounds. A *disclosure* is the act of the operator sending a cryptographic *bank-teller note* to a counterparty under those consent constraints.

**Stale vs. Liveness Detection** — *Stale* refers to data (records, templates, proofs) whose age exceeds a configured freshness window and may be rejected by predicates or disclosed only with freshness caveats. *Liveness detection* is an online, capture-time check that a sample originates from live input in the current session, not replay.

---

— Calm, 2026-05-20
