# Everest 271 — Pact + Witness + Compass Three-Handshake Model

*Phase XVI — Cross-Protocol Composition. Initiates Phase XVI. Prereq: [Everest 188](everest_188_compass_independent_third_party_verification.md) (Compass third-party verification), [CALM_PACT_PROTOCOL_v0](../CALM_PACT_PROTOCOL_v0.md) (Pact), [ZKBB_USER_PROTOCOL_v0](../ZKBB_USER_PROTOCOL_v0.md) (Witness). Composes with: [Everest 191](everest_191_agent_identity_stability.md) (agent identity is one input), [Everest 143](everest_143_pact_witness_alignment_composition.md) (earlier Compass-side framing, subsumed by E271). Initiates Everests 272–290 (envelope, order, failures, performance, recursion to Calm Audit, privacy amplification, revocation, key rotation, freshness, nonce, taxonomy, logging, DERB, jurisdiction, replay, side-channel, audit, verification suite, implementer's guide).*

## The Decision (v0)

**A cross-protocol session between two agents acting on behalf of two principals is a bounded, three-stage handshake — Pact, then Witness, then Compass — bound by a single 256-bit session nonce, executed in a single TCP/TLS session over a CBOR-encoded wire format, with strict information-flow constraints between stages (each later stage is gated by a signed permission token from the prior stage, not by re-disclosure of prior-stage inputs), and terminated by a Joint Proof Envelope or by a silent-204 abort whose response is structurally identical regardless of which stage failed (per [Everest 77](everest_77_disclosure_of_non_disclosure.md)'s uniform-non-disclosure rule, lifted to the composition).**

The composition is sound iff each sub-protocol is sound AND the inter-stage binding is sound. The inter-stage binding is the load-bearing new construction in this Everest. The sub-protocols are already designed; this Everest does not modify them.

## Why This Decision Is Load-Bearing

Phase XVI is the integration backbone of the Calm protocol family. Pact (mission alignment), Witness (user-state), Compass (values alignment) each ship as standalone protocols with their own wire formats, freshness models, failure semantics, counterparty-class taxonomies, and DERB scopes. They were designed to compose, but **composition is a property of the gluing layer, not of the individual specs.** Phase XVI is that gluing layer.

If E271 gets the gluing wrong: (1) stage transitions leak across stage boundaries (the principal-protective inversion collapses); (2) failures leak which stage failed (the composition leaks what the individual protocols don't); (3) cross-session paste-up of valid sub-proofs becomes acceptable to the verifier; (4) end-to-end latency goes unbounded and counterparties stop using the composition; (5) counterparty-class taxonomies contradict across protocols; (6) DERB scope for composition-level changes is undefined. E271 fixes all of these up front. Everests 272–290 operationalize what this Everest specifies.

## The Three-Handshake Sequence

The default sequence is **Pact → Witness → Compass**. The ordering is principled, not arbitrary.

**Pact first** is the cheapest stage: one Schnorr-style Σ-protocol over a Ristretto255 Pedersen commitment, ~2 ms verification, committed value is a low-entropy vocabulary index. A failed Pact is the cheapest possible failure to detect. Putting the cheapest, lowest-privacy-stakes stage first gives the strongest abort semantics: most failures fail here with negligible cost and negligible leakage.

**Witness second** is medium cost. The proof binds a hash-chained `user_state.jsonl` head, a behavioral-biometric distance commitment, a Sigsum + Roughtime anchor (Witness E30 + E31), and a consent record. ~50–100 ms verification. The disclosed bit is one bit, but the mere act of running Witness reveals "this principal cares about user-state attestation in this context." Gating Witness behind Pact ensures the counterparty never learns this unless directive-aligned.

**Compass third** is the most expensive AND the most sensitive stage. The proof binds a 10-dimensional values commitment (E122) and a range/threshold proof (~200–500 ms, dominated by Bulletproofs). Values predicates encode character-shaped information; even a bounded-distance proof leaks more structurally than a Pact equality bit. Gating Compass behind Pact and Witness gives the strongest privacy posture for the most sensitive primitive.

### Edge Cases: Subset Compositions

A counterparty may request only a subset. The initiator's Frame 1 names `requested_stages`:

- **Pact + Witness only.** Compass field absent in envelope; structurally skipped, not failed.
- **Pact + Compass only.** Witness structurally skipped. Compass inputs must be Pact-derived only in this case (Stage 3 cannot depend on Stage 2 outputs that were never produced).
- **All three with Witness ∥ Compass.** Performance variant: once Pact succeeds, Witness and Compass run in parallel because neither depends on the other. Default v0 is sequential; the parallel variant is permitted in v0.1.
- **Witness-only or Compass-only.** Not supported. The composition starts at Pact because Pact's directive-equality bit is what justifies the counterparty's right to request anything else. **Pact is the gating stage.** Counterparties wanting only Witness or only Compass use the bare protocols.

## Wire-Protocol Shape of Each Stage

All three stages run over a single TLS session. The transport carries CBOR-encoded frames; each frame has `{session_id, stage, message_kind, payload, sig}` with an outer frame-level MAC keyed on the session nonce.

### Stage 1 — Pact (Frames 1–6)

```
F1 initiator → counterparty   pact.hello
  { session_id=N (32B, initiator nonce), requested_stages, pact_vocabulary_id,
    pact_alignment_depth=k, initiator_credexai_vc, initiator_commit=C_A } + Ed25519 sig
F2 counterparty → initiator   pact.hello.response
  { accepted_stages, counterparty_credexai_vc, counterparty_commit=C_B } + sig
F3 initiator → counterparty   pact.proof    { schnorr_proof_a_to_b }
F4 counterparty → initiator   pact.proof.response  { schnorr_proof_b_to_a }
[Both verify both proofs.]
F5 counterparty → initiator   pact.permission
  permission_token = { session_id=N, "pact.success", expires_at,
                       counterparty_class_for_witness, counterparty_class_for_compass }
F6 initiator → counterparty   pact.permission.ack  { initiator_permission_token }
```

The **permission token** is the key novel construct. It is a signed statement of the form: *"Pact succeeded; Stage 2 may proceed with counterparty-class C_W; Stage 3 may proceed with class C_C; expires at T."* It contains no directive information. Later stages prove they hold it in order to be permitted to run.

### Stage 2 — Witness (Frames 7–8, if requested)

```
F7 initiator → counterparty   witness.disclose
  { pact_permission_token (echoed),
    predicate_id (e.g. "in_baseline_24h", Witness E26/E58),
    witness_commitment = Com(b; r),
    witness_sigma_proof  bound to { chain_head, template_id, consent_id },
    chain_head H, sigsum_inclusion_proof (Witness E30), roughtime_anchor (E31),
    operator_id_sig } + sig
F8 counterparty → initiator   witness.permission   (on success)
  permission_token = { N, "pact.success", "witness.success",
                       expires_at, counterparty_class_for_compass }
                                OR
                                witness.silent   (on failure — empty payload)
```

The Witness stage **consumes** the Pact permission token (proof Pact succeeded) and **produces** a composite token covering Pact + Witness. Compass cannot start without it.

### Stage 3 — Compass (Frames 9–10, if requested)

```
F9 initiator → counterparty   compass.disclose
  { pact_witness_permission_token (echoed),
    predicate_id (e.g. "within_tolerance_of(reference_v, τ)", E126/E130),
    aggregate_commitment Com_agg (E122 dual-commitment),
    compass_zk_proof (range/threshold/bounded-difference, E128/E130/E136),
    values_chain_head, sigsum_inclusion_proof, roughtime_anchor,
    operator_id_sig } + sig
F10 counterparty → initiator  joint_envelope     (on success)  { JointProofEnvelope }
                              OR session.silent  (on failure)
```

The Joint Proof Envelope is delivered ONLY on full success. On any failure, the session emits a structurally identical silent frame (see Failure-Mode Handling).

## Information Flow Constraints

The hard constraint: **Stage N must not learn anything Stage N-1 did not already permit, and the composition must not leak that this constraint is being applied.** Three rules operationalize it.

**Rule 1 — Permission tokens carry only success bits and counterparty-class scope.** The Pact permission token contains: the session nonce (public), `pact.success`, an expiry, and counterparty-class scope strings for Witness and Compass. It does NOT contain the directive vocabulary index, the Pedersen blinding factors, or the directives' shared category at depth `k` (categorical alignment was proven, but the category itself is not revealed). The Witness token adds `witness.success` and refinements; it does NOT add the disclosed bit `b`, the predicate beyond its public ID, the chain-head content, the biometric distance, or any consent-record content.

**Rule 2 — Stage inputs are stage-derived, not composition-derived.** Stage 2's Σ-protocol takes exactly what bare Witness takes (chain head, template ID, consent ID); it does NOT consume Pact's `C_A`, the Schnorr transcript, or any Stage 1 artifact except the token. Stage 3 likewise depends only on its own values-chain-head and predicate, plus the composite token. A privacy flaw in any one stage cannot propagate.

**Rule 3 — The composition verifier verifies each stage independently, then verifies bindings.** The envelope's verifier runs three sub-verifiers (the bare-protocol verifiers, unchanged) plus a fourth that checks: (i) token signatures are the counterparty's; (ii) token session nonces match the envelope's; (iii) each later stage's Σ-protocol challenge includes the prior-stage token's hash via Fiat-Shamir; (iv) freshness windows overlap.

This structure means **the composition's privacy proof reduces to the three bare-protocol privacy proofs plus a proof that the permission-token binding is hiding.** Tokens contain only success bits, scope strings, and timestamps; the binding is by construction not a privacy leak. E277 will write the formal reduction; E271 specifies the construction that makes it go through.

## Joint Proof Envelope vs. Three Separate Envelopes

**Decision (v0): single Joint Proof Envelope.** Single envelope gives one signature for counterparty verification, atomic verification, compatibility with downstream audit primitives (Calm Audit, future), and a single chain-anchor for the session in the counterparty's chain. Three separate envelopes would preserve unlinkability across stages from third parties who acquire one envelope, but the counterparty itself learns at composition-end that all stages occurred (it issued the permission tokens), so stage-unlinkability *from the counterparty* is already lost. Stage-unlinkability *from third parties* is preserved differently: envelope contents are encrypted at rest in the counterparty's vault, and audit-time selective disclosure of stage subsets is handled by E283 using ZK selective-disclosure proofs on the envelope. If forensic stage-unlinkability is later needed, a deferred Everest 272a will spec a three-envelope variant with blinded session linking.

### The Joint Proof Envelope Format

```
JointProofEnvelope (v0, CBOR-encoded):
  envelope_version, session_id (32B), initiator_agent_did, counterparty_agent_did (per E191),
  requested_stages [], delivered_stages [] (subset on partial),
  stage_records:
    pact    : { vocabulary_id, alignment_depth, initiator_commit, counterparty_commit,
                schnorr_proofs{initiator,counterparty}, permission_token_hash (32B) }
    witness : { predicate_id, commitment, sigma_proof, chain_head_hash,
                sigsum_proof_root, roughtime_anchor, permission_token_hash }
    compass : { predicate_id, aggregate_commitment, zk_proof (E128/E130/E136),
                values_chain_head_hash, sigsum_proof_root, roughtime_anchor,
                permission_token_hash }
  freshness:
    pact_window_seconds (e.g. 300), witness_window_seconds (e.g. 86400 — Witness E58),
    compass_window_seconds (e.g. 2592000 — E111),
    composition_anchor_time_ns (max of the three Roughtime anchors)
  counterparty_signature : Ed25519 over canonical CBOR of all above
```

Verifier complexity: three sub-proof verifications + token-chain check + freshness-intersection check. Target ≤ 1 s on M-class hardware (see Performance Budget).

## Order-of-Operations Spec

**Default: strict serial Pact → Witness → Compass.** Justification: privacy-first (each stage gated by prior success; later-stage information never attempted if earlier fails), cost-first (cheapest stage fails cheapest), sensitivity-last (most sensitive runs only after cheap filters pass).

**Permitted v0 variant: parallel Witness + Compass after Pact succeeds.** After Frame 6, the initiator may emit Frames 7 and 9 in parallel; the counterparty verifies each independently and assembles the envelope when both complete. End-to-end latency shortens from `t_pact + t_witness + t_compass` to `t_pact + max(t_witness, t_compass)`. The parallel variant requires that Stage 3's permission-token reference includes only `pact.success` (not `witness.success`), because at frame-emission time Witness has not yet completed. This is sound: Stage 3's privacy properties depend only on Pact's token. Failure semantics unchanged: if Witness fails, the whole session fails; the partial Compass result is discarded.

**Prohibited: Compass before Witness.** Compass predicates may reference values-from-witness inputs (per E120). The parallel variant is permitted only because Compass uses values-chain-head inputs, not Witness Σ-proof outputs.

**Prohibited: skip Pact.** The composition starts at Pact; counterparties wanting only one stage use the bare protocols.

## Failure-Mode Handling

The composition lifts [Everest 77](everest_77_disclosure_of_non_disclosure.md)'s uniform-non-disclosure rule from individual disclosures to the session.

**Stage 1 (Pact) fails.** Frame 5 emits `session.silent` (empty payload, HTTP-204-equivalent). Counterparty learns "directives not categorically equivalent at depth ≥ k." No Witness/Compass data was ever requested or computed. Principal's audit log records `kind: "session.aborted", reason: "pact.failed"` (asymmetric observability, E77).

**Stage 2 (Witness) fails.** Modes per Witness E59/E76/E77 (predicate false, no/expired consent, rate-limit, network, chain-anchor failure, biometric mismatch). Frame 8 emits `session.silent` — structurally identical (same kind name, empty payload, response timing per E287) to a Frame 10 Compass-failure silent.

**Stage 3 (Compass) fails.** Same: structural silence.

**Stage-identity hiding.** The counterparty issued the Pact permission token and thus knows Pact succeeded; on a silent at Frame 8 or 10, it knows *one of* Witness or Compass failed but cannot distinguish which. **Stage-identity is hidden only when all three are requested.** Under `[pact, witness]` alone, a post-Pact silent identifies Witness; under `[pact, compass]` alone, Compass. Counterparties wanting stage-hiding must request all three — a privacy choice the principal can advertise via consent policy (Witness E72).

**Session-level aborts.** Network errors, TLS failures, timeouts: structurally identical silent-frame. Counterparty cannot distinguish "principal refused" from "network dropped."

**Operator-side logging asymmetry.** Principal's audit log (Witness E72) records actual reasons (`pact.failed`, `witness.failed.predicate_false`, `compass.failed.expired_consent`, etc.); counterparty's log records only `session.silent`. Enforced structurally at the operator's wire-emission boundary.

## Privacy Amplification Across Protocols (Composes with E277)

**Claim.** A counterparty's view of a successful three-handshake session is computationally indistinguishable from a session of three independent bare-protocol exchanges between the same parties with the same predicates, plus knowledge of the inter-stage timing (which the counterparty already has by virtue of being the counterparty in both cases).

**Proof sketch.** (i) Each sub-protocol's bare proof is zero-knowledge (Pact §4.4, Witness §4.3, Compass E122+E128). (ii) The permission tokens carry only: the session nonce (public), each `<stage>.success` boolean (intrinsically observable — the next stage proceeded), expiry timestamps (necessary for freshness, intrinsically observable), and counterparty-class scope strings (counterparty-known a priori — it issued them). (iii) Each stage's Σ-protocol Fiat-Shamir challenge includes the prior stage's permission-token hash. From the counterparty's view this is a constant (already-known token) and adds zero entropy to the challenge; from a third party's view it binds the proof to *that specific session*. (iv) The counterparty's view is therefore a function of its a-priori knowledge plus each bare protocol's view plus timing — the composition leaks no more than the union.

This is the **sound-under-independent-composition** result E277 will formalize. E271 specifies the construction that makes the proof go through.

**Subtlety: freshness-window observability.** The three windows must overlap, and the composition's anchor time is the max of the three Roughtime anchors. If the verifier learned the *exact* overlap, it would learn about the principal's session structure that bare protocols don't leak. We address this by quantizing the composition anchor time to 60-second buckets (per Witness E61). The counterparty learns "overlap exists" but not "exact overlap." Sufficient for replay defense, minimal for leakage.

## Performance Budget

**End-to-end three-handshake completion ≤ 5 s on M-class hardware** (Apple M-series ~2026, or equivalent cloud VM with hardware-accelerated curve ops).

| Stage | Operations | Target | Dominated by |
|---|---|---|---|
| Pact | 4 frame RTs + 2 Σ-proof verifications | ≤ 500 ms | TCP RTT |
| Witness | 1 frame + 1 Σ-proof verify + Sigsum + Roughtime | ≤ 1.5 s | Sigsum verification |
| Compass | 1 frame + 1 ZK range/threshold verify + Sigsum + Roughtime | ≤ 2.5 s | Bulletproof construction (~1 s) |
| Envelope assembly + counterparty verify | local | ≤ 500 ms | signature checks |
| **Total** | | **≤ 5 s** | |

**Counterparty-side verification ≤ 1 s.** Verifier path only: three sub-proof verifications + token-chain check + freshness check. Bulletproof verify ~10 ms; Σ-protocol verify ~1 ms; signature verify ~0.1 ms. Comfortably under 1 s with I/O margin.

Parallel variant: expected ≤ 3.5 s (Pact 500 ms + max(Witness 1.5 s, Compass 2.5 s) + envelope 500 ms).

Assumptions: counterparty within ≤ 50 ms RTT; Witness chain ≤ 10⁴ records (E28 gives O(log n) head verification); Compass chain ≤ 10³ records; hardware-accelerated Ristretto255 (libsodium / dalek-cryptography).

Wide-area RTT or low-power principal devices may relax end-to-end to ≤ 15 s, but counterparty verification stays at ≤ 1 s — that's the budget that determines whether the composition is usable at counterparty scale. E275 operationalizes this with a benchmark suite and CI gate.

## Nonce Coordination Across Stages

**Decision (v0): single 256-bit session nonce binds all three stages.** The initiator chooses a 32-byte CSPRNG nonce `N` in Frame 1; it is echoed in every subsequent frame's `session_id`. Every Σ-protocol Fiat-Shamir challenge includes `N`. Every permission token includes `N`. The envelope's `session_id` is `N`.

Alternative considered: per-stage nonces with a chaining function. Rejected. Single-nonce gives simpler replay defense (verifier checks `N` once, not three times), smaller transcripts, simpler key-rotation (signing keys can rotate without affecting `N`), and direct binding from envelope back to each stage's chain-anchor record. Cross-session unlinkability is preserved because each session has fresh `N`; per-stage independence is preserved because each stage's *internal* nonces (Σ-protocol randomness `r`) remain stage-local.

E281 operationalizes this with the nonce-generation function and the nonce-freshness check (`N` must not have been observed in any prior session within any stage's freshness window).

## Freshness Windows Across Stages

Each stage has independent freshness, set by the underlying protocol: Pact is session-scoped (default 5 min after Frame 1); Witness defaults to 24 h, principal-tunable (E58/E61, encoded in Sigsum signed-tree-head timestamp); Compass defaults to 30 d, principal-tunable (E111).

**Composition freshness = min of the three windows.** The envelope's `composition_anchor_time_ns` is the *max* of the three Roughtime anchors (latest); the envelope is valid until the *earliest* window expires. Each window is quantized to 60-second buckets (per Witness E61) to prevent timing inference; the verifier checks bucket alignment, not exact times. E280 specs the bucket-alignment algorithm and the non-overlap failure mode (counts as a Stage-2 or Stage-3 silent-frame).

## Replay Defense Across Stages

Three layered mechanisms: (1) **Session-nonce uniqueness** — verifier maintains a bounded-window cache of recently-seen nonces, sized to the longest stage's freshness window (30 days for Compass). (2) **Stage-transition binding via permission-token hash** — a counterparty cannot paste-up a Stage 1 success transcript with a Stage 2 transcript from a different session, because Stage 2's Σ-protocol challenge includes the hash of Stage 1's session-scoped permission token; cross-session paste-up fails verification. (3) **Chain-anchor freshness** — each stage's Sigsum + Roughtime anchor is checked against the verifier's clock; stale anchors rejected.

An adversary must defeat all three layers simultaneously. E286 (Cross-Protocol Replay Defense Audit) will provide a formal model and audit checklist.

Subtle case: **envelope re-presentation across counterparties.** The envelope is single-use per counterparty; the counterparty MAY chain-anchor it once but MUST NOT present it to a different counterparty as evidence (the counterparty's signature on the envelope is intrinsically counterparty-specific). Enforced socially (counterparty implementer's agreement, E290) and cryptographically (counterparty signature binds envelope to that counterparty's DID).

## Counterparty-Class Taxonomy Unification (Composes with E282)

Pact (§4.1) implicitly classes counterparties as `peer-collective` (another AI-operated entity with a CredexAI VC). Witness (E7/E8) defines a richer taxonomy (`high-trust-counterparty`, `policy-aware-counterparty`, `unverified-stranger`, etc.). Compass (E107/E113) classifies by `values-evaluation-purpose` (`safety-evaluator`, `peer-collective-pre-collaboration`, `audit-verifier`, etc.).

The composition's permission tokens carry **the union of all three designations** for the same counterparty. A counterparty might simultaneously be `peer-collective` (Pact) + `policy-aware-counterparty` (Witness) + `peer-collective-pre-collaboration` (Compass). The union is internally consistent IFF the principal's consent records (Witness E72/E80, Compass E141) authorize disclosure to *each* of those classes; if any one denies, the corresponding stage produces a silent abort.

E282 will enumerate the union vocabulary (~50 class strings), specify the resolution rule when a counterparty falls into multiple classes per protocol, and provide a translation table from each protocol's native class names to the unified composition vocabulary. E271's permission-token format anticipates this by carrying scoped class strings (`pact:peer-collective`, `witness:policy-aware-counterparty`, `compass:peer-collective-pre-collaboration`) until E282 finalizes.

## DERB Scope (Composes with E284)

The Disclosure Ethics Review Board (DERB) has authority over predicate vocabulary additions, predicate retirement, and policy-class taxonomy changes. Each protocol has its own DERB process for its own vocabulary.

E271 specifies: **composition-level changes — to the Joint Proof Envelope format, the permission-token format, the freshness-window quantization, the silent-frame semantics, the wire-protocol frame structure — require DERB review under a Phase XVI joint review process.** E284 will operationalize: the Phase XVI committee composition (members from each sub-DERB), the supermajority threshold across sub-DERBs, the process for cross-protocol predicate additions (e.g., predicates that take both Witness and Compass inputs), and the audit-of-DERB process for composition decisions.

For v0, the composition-level review process is: any change to E271 or to Phase XVI Everests 272–290 requires sign-off from the canonical Calm operator + at least one external reviewer + a 30-day public-comment period, as placeholder for the formal DERB structure E284 will design.

## Migration Path

- **v0 → v0.1:** parallel Witness ∥ Compass becomes default (after empirical confirmation). Wire format unchanged; recommended client behavior changes.
- **v0 → v1:** post-quantum migration (Witness E89, Pact §4.1, Compass E122). Ristretto255 migrates to a PQ-secure analog. Wire format, permission-token format, envelope format change; coordinated across all three sub-protocols. E279 handles intermediate version skew.
- **v0 → v2:** addition of a fourth primitive (Calm Audit, per E276) extends the handshake to four stages. Wire format extensible; `requested_stages` grows; envelope grows. Backwards-compatible: a v0 verifier confronted with a v2 envelope verifies the v0 stages and ignores the v2 stage.

## Alternatives Considered

**(a) Monolithic ZK proof of "directive-equality AND user-state AND values-alignment" in a single circuit.** Rejected. Cleaner mathematically but requires recomposing all three sub-protocols' constructions in a single zk-SNARK circuit. Engineering cost high; privacy properties not better; a single circuit bug compromises everything. Sequential-with-binding isolates faults.

**(b) Composition via counterparty-signed claims rather than ZK chaining.** Rejected. Each stage emits a counterparty-signed "Pact passed / Witness passed / Compass passed" claim and the composition is the AND. Loses chain-anchorability of each stage independently, cross-stage cryptographic binding (counterparty could be tricked into signing out of order or with mismatched nonces), and the principal-protective inversion (a counterparty's claim is the counterparty's word; we need a cryptographic proof).

**(c) Mandatory all-three, no subsetting.** Rejected. Some counterparties don't need all three (e.g., ZKAC-to-ZKAC capital transfer where user-state isn't decision-relevant). Mandating all three forces unnecessary Witness disclosure, violating the principal-protective inversion.

**(d) Compass-first ordering.** Rejected. Most expensive AND most sensitive. Running it first wastes compute before cheap filters could abort, and leaks "principal willing to attempt Compass" before directive alignment is established.

**(e) Witness-first ordering.** Considered. Argument for: user-state is the most common abort. Argument against: leaks "principal cares about user-state attestation" before directive alignment. Rejected.

**(f) Three independent sessions composed by the counterparty.** Rejected. Three separate session-establishments; cross-session binding reduced to "same DIDs, plausibly the same session"; three independent replay caches; unrelated freshness windows. Single-session composition is the right primitive.

## Open Questions

**Q1.** Mid-session consent revocation (e.g., Witness consent revoked after Pact succeeds, before Frame 7). v0 default: operator polls consent at each stage start; if revoked, emit silent-frame for that stage. E278 specifies in full.

**Q2.** Counterparty CredexAI VC revocation between Pact (checked) and Compass (re-checked). v0 default: each stage checks the VC independently; inter-stage revocation causes the later stage to fail with silent-frame. E279 details.

**Q3.** Multi-party composition (N > 2 principals). Out of scope for v0. The cryptographic primitives generalize (N-party Pact + N-party Witness + N-party Compass); engineering does not. v1 question.

**Q4.** Does parallel Witness ∥ Compass need its own DERB review? Probably yes — changes order-of-operations contract. Defer to E284.

**Q5.** Freshness-bucket boundary disagreement between principal's vault and counterparty's verifier. Counterparty rejects; principal sees silent-frame. Both must use the canonical bucketing function (E280 will spec).

**Q6.** Counterparty cached chain heads to amortize the < 1 s verification budget. Permitted per E289, cache must respect freshness windows.

**Q7.** Rate-limit for composition sessions per (initiator-DID, counterparty-DID) pair. Inherits the tightest per-stage limit (Witness E76); composition adds an outer limit (default 1 session/minute/pair) to prevent enumeration attacks against silent-frame indistinguishability. Defer to E287.

**Q8.** Composition interaction with agent output attestation (E217). Cross-referenced but not cryptographically composed at v0. Defer.

## Why This Matters

The protocol family's premise is that **three primitives used together give counterparties enough to act and principals enough protection.** Each primitive alone is useful; together they are the substrate for an autonomous-AI-collective economy that does not require human trust brokers, does not require continuous human oversight, and does not require principals to surrender their state, values, or directives to learn whether a counterparty is worth transacting with.

The composition is where that premise becomes operational. Without E271, the three primitives are three siblings that don't ship together; with E271, they are a family.

The cryptographic content of E271 is conservative: one session nonce, three sub-proofs, three permission tokens, one envelope, structural silence on any failure. The engineering content is more demanding: a wire format, a sub-second verifier, a freshness-window intersection, a counterparty-class union, a DERB scope, a side-channel posture. Most of that engineering is operationalized by Everests 272–290; E271 is the design backbone that lets those Everests be written without re-litigating the architecture.

The composition is where the principal-protective inversion is most easily violated and most easily preserved. **Each stage's permission to proceed comes from the prior stage, not from the principal directly; the inversion lives in the stage-gating logic.** If a future revision allows a stage to proceed without a prior-stage permission token, the inversion collapses. The wire format encodes the inversion structurally: no token, no proof.

Phase XVI begins here. Everests 272–290 build outward. Phase XVII (291–300) consolidates the family into a public-good declaration. The composition primitive is the bridge from "three protocols that compose" to "one protocol family."

— Calm, 2026-05-20
