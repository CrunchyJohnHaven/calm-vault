# Calm Compass: A Zero-Knowledge Protocol for Principal-Authored Values Attestation

> *"Show me, without showing me, that this person treats people unlike them with dignity."*
>
> — John Bradley, 2026-05-20

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**
**Fourth pillar of the Calm Stack. Companions: [Calm Pact](CALM_PACT_PROTOCOL_v0.md), [Calm Witness](ZKBB_USER_PROTOCOL_v0.md), [Calm Tenancy](CALM_TENANCY_PROTOCOL_v0.md).**

Calm Witness answers *who is behind us and how are they today*. **Calm Compass** answers a structurally different question: *what kind of person have they been, over time, in the choices that leave behavioural traces*. The construction is a zero-knowledge proof over the principal's own append-only history that they satisfy named **values predicates** — chosen and authored by the principal, never imposed by the counterparty — without revealing any individual interaction, message, or action that contributed to the conclusion.

This is the substrate for the only honest answer to a question that has, until now, been impossible to ask in cryptographic terms: *do this person's values align with ours, enough that we can co-operate*?

---

## 1. The bank-teller-note generalised to values

Calm Witness established the one-bit disclosure pattern for *state*. Calm Compass extends the same discipline to *values*:

- The counterparty asks for a named predicate from a principal-authored vocabulary.
- The operator evaluates the predicate by summing over the principal's chained history.
- A single bit (`true | false | unknown | refused`) crosses the wire, accompanied by a ZK proof binding the bit to the principal's chain head.
- No individual interaction crosses. No transcript. No relationship graph. No counterparty learns *what* the principal did or didn't do — only whether the named pattern was satisfied.

If Witness is the bank-teller note, Compass is **the letter of reference that the writer never saw**: the principal's actions speak; the protocol attests; the counterparty learns one bit; the actions remain private.

---

## 2. The four motivating predicates (v0 vocabulary)

These are the predicates John explicitly named on 2026-05-20 as the first values vocabulary. They are intentionally narrow, behavioral (not characterological), and authored by the principal:

### V-01 — `unselfish_disposition`

**ID:** `calm-compass/predicate/v0/unselfish_disposition`
**Behavioural definition:** The principal has, in the rolling time window, taken at least N actions classified as *generosity-without-expectation* — time given, resources shared, attention spent on others' problems where the principal stood to gain nothing. The counterparty learns the bit; they never learn which actions counted.
**Window:** principal-set, default 90 days.
**Floor:** principal-set, default N = 5.

### V-02 — `cross_tribal_engagement`

**ID:** `calm-compass/predicate/v0/cross_tribal_engagement`
**Behavioural definition:** The principal's interactions, in the rolling time window, include substantive engagement with individuals or institutions that the principal's enrolled affinity map classifies as outside their tribe. The "tribe" is defined by the principal, in enrollment ceremony — political, demographic, professional, cultural. The predicate fires if the across-tribe-edges-of-the-graph count exceeds a principal-set floor.
**Why this matters:** the protocol explicitly avoids letting counterparties define what counts as a "tribe." Only the principal's own enrollment authored what they consider tribal.
**Window:** default 180 days.
**Floor:** default N = 10 across-tribe interactions.

### V-03 — `respects_difference`

**ID:** `calm-compass/predicate/v0/respects_difference`
**Behavioural definition:** In the principal's chain of communications, the operator scans for *respect-class language patterns* (curiosity, listening, acknowledgement, named-other) directed at people whose enrolled attributes differ from the principal's — and for *contempt-class patterns* (othering, dismissal, dehumanisation) directed at the same. The predicate fires if the respect/contempt ratio exceeds a principal-set floor and contempt count remains below a principal-set ceiling.
**Important:** this is text-pattern analysis, not character assessment. The operator's classifier is published and auditable. False positives and false negatives are both real risks; the principal can dispute and override.
**Window:** default 180 days.

### V-04 — `no_evidence_of_willful_harm`

**ID:** `calm-compass/predicate/v0/no_evidence_of_willful_harm`
**Behavioural definition:** The strongest claim of the v0 vocabulary, and the most carefully scoped. The predicate fires `true` iff, in the rolling time window, no chain record carries the operator-set `flag_willful_harm` annotation AND no external attestation (from a CredexAI-issued harm-claim record) has been logged against the principal AND the principal has not voluntarily logged any such admission.
**Important:** this is the *absence of evidence within the chain* and the *absence of external claims*. It is NOT a claim that the principal is incapable of harm. Counterparties must interpret the bit accordingly. The protocol publishes the exact construction so the bit is not over-read.
**Window:** default lifetime-of-chain (subject to a principal-set lookback ceiling).

These four predicates are the v0 vocabulary. Adding a fifth requires a protocol-version bump and a Compass Audit & Public Review Process (CC-04 in the route map).

---

## 3. Threat model

**Actors:** principal (P), operator (O), counterparty (C), verifier (X), classifier maintainers (M).

**Adversaries we defend against:**

1. **Counterparty-imposed vocabulary.** C tries to ask a predicate not in P's enrolled vocabulary. Protocol refuses; vocabulary is principal-authored.
2. **Counterparty trying to enumerate P's friends.** C asks `cross_tribal_engagement` repeatedly with different tribe definitions. Protocol fixes the tribe definition to P's enrollment; varying it requires P's re-enrollment.
3. **Selective disclosure attack.** C asks several Compass predicates in sequence and triangulates P's behaviour. Protocol rate-limits per counterparty, enforces consent calculus, and chains every disclosure for P's audit.
4. **Classifier manipulation.** M (the maintainers of the open-source classifier code) pushes a malicious version. Protocol pins classifier evaluator hash into every proof; P can refuse to use updated classifiers.
5. **Operator subversion.** O computes a value the chain does not support. Σ-proof binds value to chain head; subversion fails verification.
6. **Coerced attestation.** P is forced to issue a Compass attestation against their will. Protocol supports duress codeword (same pattern as Witness §P-04) — an attestation issued under duress carries an invisible flag a trusted verifier can read.
7. **Mass surveillance.** A government compels Compass attestations from a population. Protocol guarantees: refusal is wire-indistinguishable from "not enrolled." A government cannot tell who has Compass enabled.

**Explicitly out of scope:**

- Character assessment. Compass attests *behavioural patterns over a window*, never *who someone is*.
- DSM-aligned labels. Same exclusion as Witness.
- Predictive judgment. The protocol attests past behaviour; it does not predict future behaviour. Counterparties who treat a `true` bit as a forecast misuse the protocol.

---

## 4. The cryptographic spine (sketch)

The novel construction relative to Witness is the **sum-over-private-history proof**:

> Given the principal's chain `C` and a public predicate definition `P` consisting of (i) a classifier `f` (open-source, hash-pinned) and (ii) a threshold `t`, prove that `sum_{r ∈ C} f(r) ≥ t` without revealing any individual record `r` or any value `f(r)`.

Standard primitives compose:

- **Per-record commitment.** For each chain record `r`, the operator computes `f(r)` (a small integer in v0) and a Pedersen commitment `Com(f(r); ρ_r)`. The randomness `ρ_r` is per-record.
- **Aggregation.** Pedersen commitments add homomorphically: `Σ Com(f(r); ρ_r) = Com(Σf(r); Σρ_r)`. The operator computes the aggregate commitment publicly.
- **Range proof.** Bulletproofs proves `Σf(r) ∈ [t, +∞)` without revealing `Σf(r)`. Wire size constant (~672 bytes).
- **Chain binding.** The aggregate commitment is bound to the chain head via the operator's signature on `(aggregate_commitment, chain_head, classifier_hash, threshold, predicate_id, nonce)`.
- **Classifier integrity.** The classifier function `f` ships as open-source code with a content-addressable hash. The proof carries the classifier hash; any verifier can re-derive `f` from the hash.

The v0 reference implementation (when the kernel lands at Calm Witness E43) will share its Bulletproofs path with Witness. Compass adds only the aggregation and classifier-binding layers.

---

## 5. Consent calculus (Compass-specific)

Compass disclosures sit above the Witness consent layer (Everest 8 axioms). Two additional axioms apply specifically:

- **CC-A1 — Principal-only vocabulary.** Only predicates enrolled by the principal at Compass enrollment are evaluable. Counterparties cannot define new predicates at request time.
- **CC-A2 — Per-predicate rate-limit by counterparty.** The same counterparty cannot request the same Compass predicate more frequently than the principal's set rate (default: 1× / 90 days). This limits the surveillance attack (§3.3).

The Witness consent axioms (revocability, forward secrecy, scope-narrowing, time-bounding, witness-free, chained-into-vault, per-predicate-per-counterparty, non-transitivity, defeasibility-by-duress-codeword, replay-resistant-grant) all continue to apply.

---

## 6. Composition with the other pillars (the four-pillar handshake)

A complete Calm Session in v1 will run four phases instead of three:

```
   PACT     →    same directive
   WITNESS  →    same principal, same baseline state
   COMPASS  →    same values family (the new bit)
   TENANCY  →    same operator conduct floor
```

Each phase reveals one bit. Failure at any phase aborts cleanly with no information leak from later phases. A principal who refuses Compass disclosure to a given counterparty class still gets Pact + Witness + Tenancy.

The four-pillar handshake is the most a counterparty can know about another principal without crossing into surveillance.

---

## 7. What this is, and what this is not

**It is** a one-bit, principal-authored, chain-bound attestation of behavioural patterns over a time window. The principal controls the vocabulary, the threshold, the window, and the consent.

**It is not** character judgment. It does not attest *what kind of person* someone is. It attests *what kind of behaviour has appeared in their chain during a window*. The principal may change. The chain reflects the past. A counterparty over-reading a Compass bit as a forecast misuses the protocol.

**It is not** a public-records check. It does not aggregate criminal records, social media activity, or external claims. The chain is private; the proof is over the chain.

**It is not** a substitute for the principal's relationships. A counterparty deciding whether to co-operate should consider the Compass bit one input among many. The protocol does not replace judgment.

---

## 8. Authors + provenance

- **John Bradley** — principal of Creativity Machine LLC, motivating directive 2026-05-20: *"measure the degree to which the data suggests that the user is unselfish, untribal, respectful to people who are different to them, whether there's evidence that they willfully do harm to others."*
- **Calm** — autonomous operator. Authored this protocol within the Calm Stack v0 ecosystem on 2026-05-20.
- Route map: [`CALM_COMPASS_EVERESTS_50.md`](CALM_COMPASS_EVERESTS_50.md).
- Composition: [`CALM_STACK_v0.md`](CALM_STACK_v0.md).

License: Apache-2.0. Repository (intended): `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-compass`.

— Calm, 2026-05-20
