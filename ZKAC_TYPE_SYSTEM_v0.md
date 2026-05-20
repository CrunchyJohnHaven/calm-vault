# ZKAC Unified Type System v0

**Closes Everest 121 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**

**Draft v0 · 2026-05-20 · Calm**

**Acceptance test:** shared type vocabulary for `Principal`, `Operator`, `Vault`, `Counterparty`, `Evidence`, `Predicate`, `Proof`, `Envelope`, `ChainHead`, `ConsentRecord`, `AttestationFingerprint`, `WireVersion`; published spec used by all primitives.

---

## §1 — Core types

### Principal

A human being who owns a Calm vault and authorizes an Operator to act on their behalf. Identified cryptographically by their vault's chain-head fingerprint (SHA-256 of the root Pedersen commitment binding the principal's identity key). A Principal is non-transferable: they are a human, and humans do not delegate their humanity. Represented in wire format as a 64-hex fingerprint (`principal_id`). References: Calm Pact §2, Calm Witness §2, Calm Compass §3, Calm Concord §2.

### Operator

An autonomous AI agent licensed to transact on behalf of a Principal. Identified by an Ed25519 public key, issued and attested by CredexAI's identity-credential layer. An Operator runs the stack: Pact (for directive verification), Witness (for user-state disclosure), Compass (for values attestation), Concord (for alignment evaluation), and Tenancy (for domain operation). Operators are revocable by their Principal; the Operator's key can be rotated without changing the Principal's identity. Represented in wire format as a 64-hex fingerprint (`issued_by_operator`). References: Calm Pact §4, Calm Witness §2, Calm Tenancy §5.

### Vault

A Principal-owned, encrypted-at-rest store of chained attestation records. Holds the Principal's `user_state.jsonl` (append-only hash-chained self-narration), biometric templates, predicate-evaluation policies, enrollment data, and consent records. The vault is the single source of truth for all evidence the Principal has authorized. It is stored on the Principal's hardware (or hardware delegated by the Principal and cryptographically verified as delegated). Vault identity is pinned to the Principal's identity; moving a vault between Operators requires a vault-federation proof (Everest 125). Represented in wire format as `chain_head` (64-hex SHA-256). References: Calm Witness §2, Calm Compass §2, Calm Concord §5.

### Counterparty

A different Operator (representing a different Principal, or sometimes a service or verifier) that requests disclosure of a Predicate bit, Evidence proof, or values Alignment. Counterparties never see the Vault; they only receive Envelopes. A Counterparty must present a valid DisclosureRequest signed by their own CredexAI identity. Represented in wire format as `counterparty_id` (string, CredexAI-issued). References: Calm Witness §2, Calm Compass §2, Calm Concord §2, Calm Witness Wire Format §6.

### Evidence

A cryptographic attestation about a Predicate's truth value. Evidence is produced by the Operator evaluating a Predicate over the Principal's Vault state (Witness: biometric distance + self-report state; Compass: values-predicate evaluation over the chain; Concord: alignment-requirement satisfaction). Evidence is never wire-transmitted in plaintext; it crosses only as a ZK Proof and a Pedersen commitment. Represented in wire format as `commitment_hex` (64-hex value). References: Calm Witness §1, Calm Compass §1, Calm Compass Wire Format §5.

### Predicate

A named, published, principal-authored claim about a state or values property. Examples: `in_baseline_24h` (Witness), `unselfish_disposition` (Compass), `no_evidence_of_willful_harm` (Compass), `AlignmentRequirement` (Concord). A Predicate's ID follows the format `namespace/category/predicate_name` (e.g., `cwp.v0.in_baseline_24h`). A Predicate is never cryptographically "proved true" in the sense of being universally attested; rather, the Operator attests to the Principal that the Predicate's truth value has been **committed** and can be **proved equal to a value** the Operator computed. Predicates are registry-published and immutable once minted; new Predicates require protocol-version bumps. References: Calm Witness Wire Format §5, Calm Compass §2–4, Calm Concord §2–3.

### Proof

A Σ-protocol disjunction proof (Calm Witness / Compass) or a composite algebraic proof (Concord) that cryptographically binds:
- The Operator's claimed bit value (0 or 1)
- A Pedersen commitment (the Evidence)
- The Principal's chain-head at the time of evaluation
- A freshness bound (via Sigsum or similar transparency-log anchor)

The proof reveals nothing beyond the claimed bit and freshness window. Proof structure is defined in Calm Witness Wire Format §4 (BitProof); composite proofs for multi-predicate Concord requirements are defined in Everest 123 (forthcoming). Represented in wire format as `proof` (JSON object with fields `a0`, `a1`, `e0`, `e1`, `z0`, `z1`, `claimed_bit`). References: Calm Witness Wire Format §4, Calm Compass Σ-protocol spec (Everest 65).

### Envelope

A signed, wire-formatted message containing one or more Predicate disclosures (PredicateDisclosure tuples) plus operator and freshness metadata. The Envelope is the atomic unit of inter-agent communication; it is what a Counterparty receives when it sends a DisclosureRequest. Every Envelope carries:
- `wire_version` (version of the format)
- `kind` (`DisclosureEnvelope` for single-predicate, composite Envelope for multi-predicate per Everest 122)
- `request_digest` (SHA-256 of the canonical-JSON request this Envelope answers)
- `session_nonce` (unique per request-response pair)
- `chain_head` (Principal's Vault chain-head at issuance)
- `issued_at_iso` (ISO 8601 timestamp, freshness anchor)
- `issued_by_operator` (Ed25519 fingerprint of the Operator's key)
- `disclosures` (array of PredicateDisclosure objects)
- `operator_signature` (Ed25519 signature over canonical-JSON of all content fields)

Envelopes are cryptographically tamper-evident: a single bit flip in any field invalidates the signature. Represented in wire format as JSON per Calm Witness Wire Format §7. References: Calm Witness Wire Format §7, Everest 122 (forthcoming).

### ChainHead

A 64-hex value representing the SHA-256 of the current state of a Principal's Vault. The ChainHead is the authenticator of all evidence: a Proof binds a Predicate's evaluation to a specific ChainHead at a specific freshness window. If the ChainHead changes (Principal appends a new record), all Proofs issued against earlier ChainHeads become stale and must be refreshed. ChainHeads are anchored to Sigsum (transparent append-only log) to prove they existed at a specific UTC timestamp. Represented in wire format as `chain_head` (64-hex). References: Calm Witness §1, Calm Compass §2, Calm Witness Wire Format §6–7.

### ConsentRecord

A Principal-authored grant of permission to the Operator to evaluate a specific Predicate and disclose a specific bit for a specific Counterparty in a specific freshness window. A ConsentRecord is logged into the Vault (it becomes part of the chain history) and is itself signed by the Principal (via a duress-aware signature flow per Calm Witness §P-04). A Counterparty who receives a Disclosure can cryptographically verify that the Principal has consented to that disclosure by auditing the chain. Represented in wire format as a chain-record object with fields `kind`, `predicate_id`, `counterparty_id`, `window_seconds`, `issued_by_principal`, `principal_signature`. References: Calm Witness §2, Everest 126 (inter-vault attestation).

### AttestationFingerprint

A 64-hex SHA-256 hash uniquely identifying a single Proof + Evidence + ChainHead tuple. Two Attestations are identical iff their fingerprints match. Fingerprints allow counterparties to detect replay: if they receive the same Attestation twice (same fingerprint), they can reject the second as stale or duplicate. Fingerprints are computed as `SHA-256(canonical_json(Proof || Evidence || ChainHead))`. Represented in wire format as `attestation_fingerprint` (64-hex, optional but recommended in Envelope metadata). References: Everest 122 (composite envelopes).

### WireVersion

A semantic-versioning string identifying the wire format of an Envelope. All Calm Stack primitives use the same wire-versioning scheme: `calm-witness/wire/v0`, `calm-compass/wire/v0`, etc. (future Everest 122 may unify to a single `calm-stack/wire/v0`). Implementations MUST reject messages with an unknown WireVersion. Represented in wire format as `wire_version` (string, first sorted field in every top-level JSON object). References: Calm Witness Wire Format §2, Everest 122 (forthcoming).

---

## §2 — Type distribution across primitives

| Type | Calm Pact | Calm Witness | Calm Compass | Calm Concord | Calm Tenancy |
|------|-----------|--------------|--------------|--------------|--------------|
| Principal | directive owner | state owner | values owner | requester | domain owner |
| Operator | prover (Alice/Bob) | evaluator + prover | evaluator + prover | aggregator | domain executor |
| Vault | none (Pact uses CredexAI VC layer directly) | contains user_state.jsonl + biometric templates | contains values history + chain | reads Compass envelopes + Witness envelopes | credential store |
| Counterparty | verifier (the other agent) | disclosure requester | disclosure requester | alignment requester | external service or mail sender |
| Evidence | Pedersen commitment `C = g^d · h^r` | commitment of `(biometric_distance, baseline_flag)` | commitment of predicate truth value | joint predicate evaluation | not used (Tenancy is not a ZK primitive) |
| Predicate | `d_A ≡ d_B (mod q)` (directive equality) | `in_baseline_24h`, `biometric_match_within(τ)` | `unselfish_disposition`, `cross_tribal_engagement`, `respects_difference`, `no_evidence_of_willful_harm` | `all_satisfied`, `any_satisfied`, `asymmetric`, `joint_threshold` | `cringe_rubric ≤ 1.0 hits/50w`, `no_forbidden_phrases`, `response_time_sla` |
| Proof | Σ-protocol equality proof (Pedersen) | Σ-protocol disjunction proof (BitProof per WF §4) | Σ-protocol disjunction proof over chained history | composite proof over two Compass envelopes + Concord evaluation logic | audit-chain record (no cryptographic proof; deterministic evaluation) |
| Envelope | not applicable (Pact uses CredexAI VC layer) | DisclosureEnvelope (Wire Format §7) | DisclosureEnvelope (extends Wire Format §7) | AlignmentEnvelope (Everest 123) | tenancy_daily_check (chain record), tenancy_assertion (JSON published at `/.well-known/calm-tenancy.json`) |
| ChainHead | not used (Pact is synchronous, one-shot) | Principal's user_state chain head | Principal's values history chain head | both Principals' Compass chain heads | Operator's tenancy daily-check chain head |
| ConsentRecord | not used | logged into Principal's vault for every Witness disclosure | logged for Compass predicates; `principal_consents_to_disclose(p)` is itself a Compass predicate | not logged separately; implicit in the two Principals' Compass consent records | logged into Principal's domain-operations memory; `feedback_*` annotations are consent records |
| AttestationFingerprint | not used | optional in Envelope metadata; recommended for replay-detection | recommended for Compass predicate auditing | required for multi-predicate composite proofs (Everest 123) | not used |
| WireVersion | none | `calm-witness/wire/v0` | `calm-compass/wire/v0` | `calm-concord/wire/v0` (or unified `calm-stack/wire/v0` per Everest 122) | `calm-tenancy/v0` (non-wire-format; published as JSON at `/.well-known/calm-tenancy.json`) |

---

## §3 — Canonical encoding

All ZKAC types serialize to JSON in **canonical form**:

- UTF-8 encoding.
- Sorted object keys (lexicographic by codepoint).
- Compact separators (`","` and `":"`, no whitespace).
- Hex integers (Pedersen group elements, scalars, fingerprints) rendered as lowercase hex without `"0x"` prefix.
- Timestamps in ISO 8601 format.
- `wire_version` as the first sorted field in every top-level message.

Canonical encoding ensures bit-for-bit interoperability across languages (Python, Rust, Go, JavaScript, etc.) and makes each Envelope's signature deterministic. Implementations MUST verify `SHA-256(canonical_json(envelope_content))` matches the embedded `operator_signature` digest. References: Calm Witness Wire Format §3.

---

## §4 — Cross-primitive invariants

1. **Chain-head freshness is global.** All Predicates in a composite Envelope (Everest 123) must bind to the same Principal's ChainHead at the same timestamp. Mixing ChainHeads from different moments invalidates the composite.

2. **Consent is predicate-specific.** A ConsentRecord for `in_baseline_24h` does not grant consent for `unselfish_disposition`. Every Predicate requires an explicit ConsentRecord.

3. **Counterparty is fixed per session.** Once a DisclosureRequest arrives from Counterparty C, all responding Envelopes must carry `counterparty_id == C`. Operators MUST NOT re-use one Envelope (same request_digest, same predicates) for a different Counterparty.

4. **Proofs do not transfer.** A Proof issued for Counterparty C cannot be forwarded to Counterparty D. Proofs are request-specific and non-transferable.

5. **WireVersion is non-negotiable.** Implementations reject messages with unknown WireVersions. Forward-compatibility is handled by adding optional fields within a version, not by version negotiation.

---

## §5 — Future extensions

Types defined in this v0 spec are **frozen** for purposes of Everest 121 acceptance. Extensions are tracked in forthcoming Everests:

- **Everest 122:** `CompositeEnvelope` type (single Envelope containing Pact + Witness + Compass + Concord disclosures).
- **Everest 125:** `VaultFederationProof` type (for vault mobility between Operators).
- **Everest 126:** `InterVaultAttestation` type (one vault attesting about another's identity).

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
