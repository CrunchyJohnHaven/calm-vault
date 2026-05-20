# Calm Mirror — 100 Engineering Everests

**Route map: pairwise values-alignment cryptographic attestation between two principals (via their agents) — the values-alignment companion to [Calm Witness](ZKBB_USER_EVERESTS_100.md) (user-state) and [Calm Pact](CALM_PACT_PROTOCOL_v0.md) (directive-equality).**

> *"All you need to know is that, on the values you both care about, you and they are pointing the same way."*

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.
**Status:** Route v0 · 2026-05-20 · open for adversarial review.
**Companion routes:** [Calm Witness 100](ZKBB_USER_EVERESTS_100.md), [ZKAC Infra 100](ZKAC_INFRA_EVERESTS_100.md).

---

## What Calm Mirror is

A cryptographic primitive that lets two principals' agents discover whether the principals' values align — without revealing either principal's full value profile, without creating a central scoring authority, and without locking principals into past behavior.

The naming asymmetry: Calm Pact says *"we mean the same thing"*; Calm Witness says *"the human is themself"*; Calm Mirror says *"on the values you both care about, you both point the same way."*

The user-stated value examples that anchored v0:

- **Unselfishness.** Patterns of resource allocation that prioritize others.
- **Tribal neutrality.** Treating in-group and out-group with equivalent dignity.
- **Respect for difference.** Engagement with people whose identities, beliefs, or backgrounds differ.
- **Absence of willful harm.** No evidence of actions intentionally taken to hurt others.

These four are v0. The vocabulary grows by public RFC (Everest 78).

## Principal-protective defaults (the non-negotiables)

Before any summit: the protocol must encode these defaults, because the alternative — a values-attestation system without them — becomes a blacklist.

1. **Any single value-bit can be withheld** unilaterally. No counterparty can demand a specific bit; declining is always a valid response.
2. **Past behavior does not lock the principal in.** Growth is a first-class value (Everest 34). A principal who behaved poorly five years ago and has visibly grown since does not get a permanent "bad" bit.
3. **No central scoring authority.** Each principal authors their own value-vocabulary (Everest 21-25). Cross-principal comparison happens only on shared vocabulary subsets.
4. **The bit does not describe the principal.** A bit answers "is there evidence of X?" — not "is this person X?". A counterparty who treats the bit as identity has violated the protocol's spirit.
5. **Co-principal vouching is allowed; mob attestation is not.** Witnesses who attest someone's behavior must themselves be Calm-credentialed principals (Everest 16). Anonymous mass-attestation is not honored.
6. **Per-counterparty consent (inherited from Calm Witness Axiom 1-3).** Each disclosure is granted per counterparty, per predicate, per window. Revocable.

These defaults outrank every later design choice. A summit that violates them is rejected at tribunal.

---

## How to read this route

Same shape as the Calm Witness route map:

- 100 numbered summits, dependency-ordered.
- Each has a one-sentence acceptance test, effort estimate (S/M/L/XL), explicit prereqs, gate-script name.
- Gate scripts live at `~/CredexAI/scripts/everest_NN_mirror_*_gate.py`.
- Composes with Calm Witness and Calm Pact at the disclosure and chain layers.

---

## Phase IX — Foundations (1–10)

**Mirror Everest 1 — Problem statement & threat model.** *Acceptance:* a versioned doc capturing actors, trust assumptions, adversaries, what we are/aren't measuring, and the six principal-protective defaults above. *Effort:* M. *Note:* The hardest threat is *weaponization*: an actor gaming the protocol to blackball someone. v0's defense is per-counterparty consent + withhold-any-bit + growth-bit.

**Mirror Everest 2 — Route map (this doc).** *Acceptance:* 100 summits with stable IDs, deps, acceptance tests. *Effort:* M.

**Mirror Everest 3 — Naming & branding lock.** *Acceptance:* one canonical name (Calm Mirror) + alias (ZKBB-Mirror, technical) + glossary entries. *Effort:* S. *Prereq:* 1.

**Mirror Everest 4 — License & IP posture.** *Acceptance:* Apache-2.0 (matching Calm Pact + Witness); patent non-aggression text. *Effort:* S. *Prereq:* 3.

**Mirror Everest 5 — Values vocabulary v0.** *Acceptance:* an enumerated, semantically-precise list of v0 value predicates: `unselfishness_evidence`, `tribal_neutrality_evidence`, `respect_for_difference_evidence`, `non_harm_evidence`, `growth_arc_evidence`, `truth_telling_evidence`, `apology_when_wrong_evidence`. *Effort:* L. *Prereq:* 1. *Note:* Each predicate is "evidence of X", not "is X" — the predicate-name discipline that prevents identity-collapse.

**Mirror Everest 6 — Behavior-evidence taxonomy.** *Acceptance:* classification of evidence kinds (self-reported actions, witnessed actions, third-party records, allocation logs, counter-evidence). Each kind has explicit reliability discount factors. *Effort:* M. *Prereq:* 1, 5.

**Mirror Everest 7 — Counterparty-class taxonomy for values disclosure.** *Acceptance:* per-class default consent stances (peer-AI-collective, employer, partner, journalist, ideologue, anonymous, etc.) with explicit rationales. *Effort:* M. *Prereq:* 1. *Note:* The "ideologue" class is novel — counterparties whose stated agenda is to filter people by values. v0 default: deny all but explicit per-identity grants.

**Mirror Everest 8 — Ethics review board protocol.** *Acceptance:* a standing 5-person panel (≥3 outsiders) reviewing every new value-predicate before it enters the vocabulary. *Effort:* M. *Prereq:* 5. *Note:* This is the brake on ideological capture.

**Mirror Everest 9 — Failure-mode catalogue.** *Acceptance:* enumerated failure modes M01-M30 with severity ranking. S1 = false-positive principal-harm; S2 = ideological capture; S3 = mob attestation; S4 = cryptographic failure. *Effort:* M. *Prereq:* 1.

**Mirror Everest 10 — Reference architecture.** *Acceptance:* one diagram showing Principal A + Principal B + their operators + the evidence chain + the Mirror exchange + the counterparty class layer. *Effort:* S. *Prereq:* 1, 7.

## Phase X — Behavior-Evidence Substrate (11–25)

**Mirror Everest 11 — Behavior-evidence chain v0.** *Acceptance:* an extension of `user_state.jsonl` with new `kind: behavior_evidence.v0` records carrying evidence-kind + content-commitment + timestamp + optional witness-signatures. Chain stays append-only hash-chained. *Effort:* M. *Prereq:* 6, [Witness Everest 26].

**Mirror Everest 12 — Self-reported action intake.** *Acceptance:* an intake DSL for the principal to record "I did X for Y" actions. Records are signed by the principal; not auto-verified. *Effort:* S. *Prereq:* 11.

**Mirror Everest 13 — Witnessed-action intake.** *Acceptance:* a record schema where one principal records an action and a second Calm-credentialed principal co-signs as having observed it. Co-signature is itself chained. *Effort:* M. *Prereq:* 11.

**Mirror Everest 14 — Third-party action records.** *Acceptance:* schema for incorporating verifiable third-party records (court orders, donation receipts, public statements) with their origin attestation. *Effort:* L. *Prereq:* 11.

**Mirror Everest 15 — Allocation evidence.** *Acceptance:* aggregate evidence of where the principal allocates resources (time, money, attention) across categories. Aggregates only — specific transactions stay out. *Effort:* M. *Prereq:* 11.

**Mirror Everest 16 — Witness-credential binding.** *Acceptance:* witnesses must hold a CredexAI VC; their co-signature is bound to that VC. Anonymous witnesses are not honored. *Effort:* M. *Prereq:* 13.

**Mirror Everest 17 — Counter-evidence intake.** *Acceptance:* a `kind: counter_evidence.v0` record where the principal records places they fell short. Symmetrically chained. *Effort:* M. *Prereq:* 11. *Note:* Counter-evidence intake is what makes growth-bits credible.

**Mirror Everest 18 — Recall-resistance.** *Acceptance:* once a behavior-evidence record is chained, it cannot be silently edited; the only way to "soften" is a `kind: correction.v0` referencing the prior record. *Effort:* S. *Prereq:* 11.

**Mirror Everest 19 — Adversarial-witness defense.** *Acceptance:* documented defense against false-witness attacks (someone fabricates a co-sign). Defense: the alleged witness's vault contains the matching counter-record. *Effort:* L. *Prereq:* 13, 16.

**Mirror Everest 20 — Negative-testimony protocol.** *Acceptance:* a careful protocol for people the principal has wronged to attest negative behavior, with cooling-off windows and the principal's right of reply. *Effort:* L. *Prereq:* 13, 17. *Note:* This is the most fraught summit; rubric-driven, not free-form.

**Mirror Everest 21 — Per-principal value-vocabulary lock.** *Acceptance:* each principal at enrollment commits to which values from the v0 vocabulary they claim — opt-in, never imposed. *Effort:* M. *Prereq:* 5.

**Mirror Everest 22 — Time-weighting of evidence.** *Acceptance:* evidence has a configurable decay function; more recent evidence weighs more. Default half-life: 2 years. *Effort:* M. *Prereq:* 11.

**Mirror Everest 23 — Evidence-diversity requirement.** *Acceptance:* a predicate evaluating to `true` requires evidence from ≥2 distinct evidence-kinds (e.g., self-report + witnessed-action). Single-source evidence returns `unknown`. *Effort:* M. *Prereq:* 11, 21.

**Mirror Everest 24 — Cross-modal evidence schema.** *Acceptance:* support for evidence in multiple modalities (text, audio transcription, image/video summary). All committed via hash; raw stays off-chain. *Effort:* L. *Prereq:* 11, [Witness Everest 41].

**Mirror Everest 25 — Behavior-evidence revocation.** *Acceptance:* in rare, well-justified cases (proven false-witness), evidence records can be marked `kind: revocation.v0`. The original stays in the chain; the revocation is itself chained. *Effort:* M. *Prereq:* 18, 19.

## Phase XI — Value-Measurement Predicates (26–40)

**Mirror Everest 26 — Predicate language v0 for values.** *Acceptance:* extension of Calm Witness's predicate DSL (Witness Everest 51) to operate over behavior-evidence records. *Effort:* M. *Prereq:* 11, [Witness Everest 51].

**Mirror Everest 27 — `unselfishness_evidence` predicate.** *Acceptance:* a formal predicate over allocation-evidence + witnessed-actions showing patterns of others-prioritizing choices. Threshold-parameterized. *Effort:* L. *Prereq:* 5, 15, 26. *Note:* The hard part is the operationalization. v0 uses a documented composite of three sub-metrics; v1 may evolve.

**Mirror Everest 28 — `tribal_neutrality_evidence` predicate.** *Acceptance:* predicate showing behavioral parity across in-group vs out-group (group membership self-declared by the principal at enrollment). *Effort:* L. *Prereq:* 5, 26.

**Mirror Everest 29 — `respect_for_difference_evidence` predicate.** *Acceptance:* predicate over evidence of engagement with people across declared difference dimensions (belief, identity, background). *Effort:* L. *Prereq:* 5, 26.

**Mirror Everest 30 — `non_harm_evidence` predicate.** *Acceptance:* predicate over absence of evidence of willful harm — third-party records (court judgments) AND counter-evidence intake AND negative-testimony absence. *Effort:* L. *Prereq:* 5, 14, 20, 26. *Note:* "Absence of evidence" is not "evidence of absence" — the predicate explicitly returns `unknown` when the evidence base is thin.

**Mirror Everest 31 — `growth_arc_evidence` predicate.** *Acceptance:* predicate over trajectory — past counter-evidence + later corrective action + sustained pattern change. *Effort:* L. *Prereq:* 17, 22, 26.

**Mirror Everest 32 — `truth_telling_evidence` predicate.** *Acceptance:* predicate over consistency of past statements with later-verified facts. *Effort:* L. *Prereq:* 14, 26.

**Mirror Everest 33 — `apology_when_wrong_evidence` predicate.** *Acceptance:* predicate over `kind: correction.v0` + counter-evidence records following identified mistakes. *Effort:* M. *Prereq:* 17, 18, 26.

**Mirror Everest 34 — Growth-bit composition rule.** *Acceptance:* a normative rule that any disclosure including `non_harm_evidence` MUST also be willing to include `growth_arc_evidence` if requested. Prevents permanent blackballing. *Effort:* M. *Prereq:* 30, 31.

**Mirror Everest 35 — Consistency-over-time predicate.** *Acceptance:* predicate over stability of value-evidence across years — penalizes evidence-bursts right before disclosure (anti-gaming). *Effort:* M. *Prereq:* 22, 26.

**Mirror Everest 36 — Cross-domain coherence predicate.** *Acceptance:* predicate over evidence appearing in multiple domains (work, family, civic, online) — single-domain evidence weighs less. *Effort:* M. *Prereq:* 26.

**Mirror Everest 37 — Co-principal vouching predicate.** *Acceptance:* predicate over witness signatures from N other Calm-credentialed principals attesting to the principal's behavior in named contexts. *Effort:* L. *Prereq:* 13, 16, 26.

**Mirror Everest 38 — Adversarial-test-resistance flag.** *Acceptance:* meta-predicate that flips false when the chain shows evidence consistent with deliberate gaming (e.g., a sudden spike of `unselfishness` evidence after a counterparty request). *Effort:* L. *Prereq:* 35, 26.

**Mirror Everest 39 — Per-value threshold calibration.** *Acceptance:* per-principal calibrated thresholds for each value predicate, computed from the principal's evidence base at enrollment and locked thereafter. *Effort:* M. *Prereq:* 5, 26.

**Mirror Everest 40 — Predicate vocabulary v0 publication.** *Acceptance:* `MIRROR_PREDICATE_VOCABULARY_v0.md` published; predicate IDs content-addressed; future additions require Everest 8 ethics review. *Effort:* M. *Prereq:* 27-39, 8.

## Phase XII — Mirror Disclosure Semantics (41–55)

**Mirror Everest 41 — Pairwise alignment computation primitive.** *Acceptance:* given two principals' published value-commitments (predicates each has chosen to keep evaluable), compute the intersection of their shared vocabulary. *Effort:* M. *Prereq:* 40.

**Mirror Everest 42 — Aligned-bit commitment scheme.** *Acceptance:* a Pedersen commitment to the joint bit "we both have `true` on shared predicate p" — neither principal reveals their own bit individually. *Effort:* L. *Prereq:* 41, [Witness Everest 44]. *Note:* This is two-party MPC; the alignment-bit emerges from the joint computation without either side revealing their input.

**Mirror Everest 43 — ZK proof: shared-K-of-N values.** *Acceptance:* a ZK proof that "of the N values in our intersection vocabulary, we both share ≥ K positive evaluations" — without revealing which K. *Effort:* XL. *Prereq:* 42.

**Mirror Everest 44 — ZK proof: distance under threshold.** *Acceptance:* a ZK proof that the Hamming distance between our value vectors is ≤ δ, under a public δ. *Effort:* L. *Prereq:* 42.

**Mirror Everest 45 — ZK negative-bit proof.** *Acceptance:* ZK proof that "neither of us has the `willful_harm` evidence-bit" — without revealing either's bit. *Effort:* L. *Prereq:* 30, 42.

**Mirror Everest 46 — Per-counterparty consent for values disclosure.** *Acceptance:* extension of Witness Everest 8 consent calculus, with per-value-bit consent grants. *Effort:* M. *Prereq:* 7, [Witness Everest 8].

**Mirror Everest 47 — Tiered disclosure precision.** *Acceptance:* a counterparty-class-keyed precision parameter — friends get more precise alignment data than journalists; journalists get more than employers. *Effort:* M. *Prereq:* 7, 46.

**Mirror Everest 48 — One-way disclosure.** *Acceptance:* a principal can disclose values to a counterparty without requesting reciprocal disclosure. *Effort:* S. *Prereq:* 46.

**Mirror Everest 49 — Reciprocal disclosure (the Mirror exchange).** *Acceptance:* the canonical two-party exchange where both principals' agents jointly compute alignment and both receive the same disclosure. *Effort:* L. *Prereq:* 42, 46.

**Mirror Everest 50 — Anonymous values discovery.** *Acceptance:* a protocol where two anonymous parties can discover their shared values without revealing their identities. Useful for finding aligned strangers. *Effort:* L. *Prereq:* 49.

**Mirror Everest 51 — Withhold-any-bit guarantee.** *Acceptance:* a normative + cryptographic guarantee that any specific value-bit can be unilaterally withheld. The other side learns "withheld" — not "true" or "false". *Effort:* M. *Prereq:* 46.

**Mirror Everest 52 — Mirror-fail abort semantics.** *Acceptance:* documented behavior when Mirror computation fails — the session aborts with `unknown` for the disclosed bit; the principal-protective default kicks in. *Effort:* M. *Prereq:* 49.

**Mirror Everest 53 — Restricted-action-set on value mismatch.** *Acceptance:* protocol-level negotiation of which actions are off-limits when shared values are insufficient. *Effort:* M. *Prereq:* 49, [Witness Everest 91-equivalent if defined].

**Mirror Everest 54 — Stealth disclosure (safety triggers).** *Acceptance:* when one principal's chain contains a `kind: safety_trigger.v0` flagging coercion, the Mirror exchange surfaces this to the counterparty even without explicit consent. *Effort:* L. *Prereq:* 49, [Witness duress-codeword work].

**Mirror Everest 55 — Composing Mirror with Witness.** *Acceptance:* a session that first runs Calm Pact (directive equality), then Calm Witness (user-state), then Calm Mirror (values alignment) — strict ordering, fail-cleanly at each stage. *Effort:* L. *Prereq:* 49, [Witness Everest 97].

## Phase XIII — Mirror Cryptographic Core (56–70)

**Mirror Everest 56 — Pedersen vector commitments for value vectors.** *Acceptance:* commitment scheme over Ristretto255 that commits an N-dimensional bit vector with size scaling sub-linearly in N. *Effort:* M. *Prereq:* [Witness Everest 44].

**Mirror Everest 57 — Two-party MPC framework selection.** *Acceptance:* decision doc: which 2PC framework (garbled circuits, SPDZ, OT-based) for the alignment computation. v0 choice: [TBD by Everest 56 audit]. *Effort:* M.

**Mirror Everest 58 — Secure computation of intersection bits.** *Acceptance:* MPC protocol that computes "we both have `true` on the i-th shared predicate" without revealing either side's bit. *Effort:* XL. *Prereq:* 56, 57.

**Mirror Everest 59 — ZK proof of MPC correctness.** *Acceptance:* ZK proof that the MPC output is the honest evaluation over the committed value vectors. *Effort:* XL. *Prereq:* 58.

**Mirror Everest 60 — Range proof for unselfishness-index.** *Acceptance:* Bulletproofs range proof that the principal's allocation-evidence-derived score is above threshold. *Effort:* M. *Prereq:* 27, [Witness Everest 45].

**Mirror Everest 61 — Cross-principal binding proof.** *Acceptance:* the joint disclosure binds to BOTH principals' chain heads — neither can swap their chain after the fact. *Effort:* L. *Prereq:* 58.

**Mirror Everest 62 — Multi-anchor consensus for evidence.** *Acceptance:* third-party evidence records must be anchored to ≥ 2 independent transparency logs. *Effort:* L. *Prereq:* 14.

**Mirror Everest 63 — Side-channel resistance for values eval.** *Acceptance:* documented side-channel review of the value-evaluator code paths. *Effort:* L. *Prereq:* 58.

**Mirror Everest 64 — Post-quantum migration plan for Mirror.** *Acceptance:* aligned with Calm Witness Everest 96; bridge mechanism for value-vector commitments. *Effort:* L. *Prereq:* 56, [Witness Everest 96].

**Mirror Everest 65 — Aggregate alignment-score proof.** *Acceptance:* a single proof carrying the alignment-score (a real number in [0,1]) plus the bits behind it. *Effort:* L. *Prereq:* 58, 60.

**Mirror Everest 66 — Bilateral consent-binding proof.** *Acceptance:* the disclosure binds to BOTH principals' consent records — neither can claim later that they didn't agree to the exchange. *Effort:* M. *Prereq:* 46.

**Mirror Everest 67 — Evidence-freshness proof.** *Acceptance:* ZK proof that the evidence used in the alignment computation was within the freshness window. *Effort:* M. *Prereq:* 22, [Witness Everest 65 — freshness kernel].

**Mirror Everest 68 — Anti-replay across sessions.** *Acceptance:* a Mirror exchange in session X cannot be replayed as evidence in session Y, even with the same principals. *Effort:* M. *Prereq:* 61.

**Mirror Everest 69 — Adversarial robustness study.** *Acceptance:* documented FAR/FRR-equivalent for alignment computation under (a) one-side-lies, (b) both-sides-collude-to-fake-alignment, (c) coercion attacks. *Effort:* XL. *Prereq:* 58.

**Mirror Everest 70 — Conformance vector publication.** *Acceptance:* published cross-implementation test vectors for the MPC + ZK pipeline. *Effort:* M. *Prereq:* 58, 59.

## Phase XIV — Cross-Culture & Coercion Defenses (71–85)

**Mirror Everest 71 — Cross-cultural value taxonomy.** *Acceptance:* a study of how the four v0 values (unselfishness, tribal-neutrality, respect-for-difference, non-harm) map across cultural contexts; gaps documented. *Effort:* XL. *Prereq:* 5, 40.

**Mirror Everest 72 — Religious / philosophical overlays.** *Acceptance:* a mechanism for principals to declare their value-vocabulary mapping under a specific tradition (Stoic, Christian, Confucian, etc.) — the predicate semantics remain the same, the principal's framing differs. *Effort:* L. *Prereq:* 71.

**Mirror Everest 73 — Bias audit for value evaluators.** *Acceptance:* third-party audit (academic + advocacy panels) for systematic bias in the v0 predicate set. *Effort:* L. *Prereq:* 40.

**Mirror Everest 74 — Disability + neurodiversity advocacy review.** *Acceptance:* sign-off from ≥ 2 disability advocacy organizations + ≥ 1 neurodiversity-focused review on the v0 predicates' fairness across different cognitive styles. *Effort:* L. *Prereq:* 40. *Note:* The cognitively_atypical_baseline predicate from Calm Witness is the anchor here.

**Mirror Everest 75 — Mob-attestation defense.** *Acceptance:* documented defense against many-witnesses-attacking-one — witness signatures degrade in weight when they cluster suspiciously around one target. *Effort:* L. *Prereq:* 13, 16.

**Mirror Everest 76 — Ideologue-counterparty defense.** *Acceptance:* per-class default = `deny` for ideologue counterparties (per Everest 7 class). Principal opt-in required for each ideologue. *Effort:* M. *Prereq:* 7, 46.

**Mirror Everest 77 — Coercion-resistance proof.** *Acceptance:* documented: a principal under coercion cannot be forced to disclose alignment to a hostile counterparty (the safety_trigger from Everest 54 fires). *Effort:* L. *Prereq:* 54.

**Mirror Everest 78 — Vocabulary RFC process.** *Acceptance:* a published RFC process for proposing new value-predicates: ≥ 90 days public review, ≥ 5-person ethics panel, ≥ 3 independent external reviewers. *Effort:* M. *Prereq:* 8.

**Mirror Everest 79 — Multi-jurisdiction legal review.** *Acceptance:* legal review across US / EU / UK / CA / JP / IN / BR; identify jurisdictions where values-disclosure interfaces with employment, housing, or insurance law. *Effort:* L. *Prereq:* 40.

**Mirror Everest 80 — Right of reply.** *Acceptance:* normative rule + chain-level mechanism: any negative-testimony record auto-includes a reserved seq position for the principal's reply. *Effort:* M. *Prereq:* 20.

**Mirror Everest 81 — Slashing for false witnesses.** *Acceptance:* a witness whose signed testimony is later cryptographically refuted (proven false-witness attack) has their CredexAI VC downgraded or revoked. *Effort:* L. *Prereq:* 16, 19, 25.

**Mirror Everest 82 — Anonymous reporting channel.** *Acceptance:* a channel for credible anonymous warning *to the principal* (not the counterparty) when their value-evidence shows suspect patterns — protective, not punitive. *Effort:* L. *Prereq:* 38.

**Mirror Everest 83 — Cooling-off windows.** *Acceptance:* mandatory waiting periods between negative-testimony and disclosure-of-mismatch — prevents heat-of-the-moment cascades. *Effort:* S. *Prereq:* 20.

**Mirror Everest 84 — Reputation-tax framework.** *Acceptance:* a counterparty whose track record shows misuse of Mirror disclosures (e.g., publicly outing aligned/mismatched bits) loses access to future disclosures. *Effort:* L. *Prereq:* 46.

**Mirror Everest 85 — Ethics-board panel composition lock.** *Acceptance:* the 5-person ethics panel (Everest 8) must include: 1 cryptographer, 1 ethicist, 1 disability/diversity advocate, 1 working principal, 1 wildcard external reviewer. Composition is public. *Effort:* S. *Prereq:* 8.

## Phase XV — Engineering Reliability (86–95)

**Mirror Everest 86 — Python reference implementation.** *Acceptance:* `~/CredexAI/calm_mirror/` Python module mirroring `~/CredexAI/calm_witness/` shape; passes cross-implementation conformance. *Effort:* XL. *Prereq:* 40, 58.

**Mirror Everest 87 — Rust production implementation.** *Acceptance:* `calm-mirror` Rust crate matching the `zkac_v0` + `calm-witness` quality bar. *Effort:* XL. *Prereq:* 86, [Witness Everest 81].

**Mirror Everest 88 — WASM port.** *Acceptance:* browser counterparties can verify a Calm Mirror joint disclosure in ≤ 100 ms. *Effort:* L. *Prereq:* 87.

**Mirror Everest 89 — SDK ergonomics.** *Acceptance:* `calm.mirror_exchange(counterparty, predicates=[...])` SDK call. *Effort:* M. *Prereq:* 87.

**Mirror Everest 90 — CI with adversarial fuzzers.** *Acceptance:* nightly fuzzers exercise the MPC + ZK pipeline; flake-free 30 days. *Effort:* L. *Prereq:* 87.

**Mirror Everest 91 — Property-based tests for predicates.** *Acceptance:* invariants: monotonicity under added evidence, idempotence of recomputation, robustness to witness-set permutation. *Effort:* M. *Prereq:* 86.

**Mirror Everest 92 — Performance budget.** *Acceptance:* Mirror exchange (2-party MPC + ZK) ≤ 500 ms p95 on M-series Mac; ≤ 2 s p95 on phone. *Effort:* L. *Prereq:* 87.

**Mirror Everest 93 — Mobile vault for Mirror.** *Acceptance:* end-to-end Mirror exchange on iOS/Android stays under ≤ 8% battery / hour budget. *Effort:* L. *Prereq:* 92.

**Mirror Everest 94 — Third-party audit prep.** *Acceptance:* audit packet covering Mirror cryptography + bias audit + ethics review documentation. *Effort:* L. *Prereq:* 73, 87.

**Mirror Everest 95 — Mirror operator licensing.** *Acceptance:* a CredexAI VC sub-class for Mirror operators with explicit ethics-compliance attestation. *Effort:* M. *Prereq:* 8, 85.

## Phase XVI — Governance, Standards, First Production (96–100)

**Mirror Everest 96 — Open-source release.** *Acceptance:* `calm-mirror` published under Apache-2.0 alongside Pact + Witness. *Effort:* M. *Prereq:* 87.

**Mirror Everest 97 — NIST / AI Safety Institute submission.** *Acceptance:* formal submission of the Calm Mirror values-alignment primitive as a candidate standard for autonomous-agent values disclosure. *Effort:* L. *Prereq:* 79, 96.

**Mirror Everest 98 — Counterparty implementer's guide.** *Acceptance:* doc for AI-operator orgs adopting Calm Mirror as a counterparty; covers consent semantics, fail-modes, ethical use guidelines. *Effort:* M. *Prereq:* 96.

**Mirror Everest 99 — First production deployment.** *Acceptance:* Creativity Machine LLC operates a live Mirror endpoint; at least one real Mirror exchange against an external aligned-AI-collective counterparty completes successfully. *Effort:* L. *Prereq:* 87-98 all bagged.

**Mirror Everest 100 — Independent third-party end-to-end verification.** *Acceptance:* a non-Calm-affiliated organization, with explicit ethics-review-board presence, performs and publishes an independent end-to-end Mirror exchange using only public documentation. *Effort:* L. *Prereq:* 96, 98, 99.

---

## Status table

```
Phase IX   : ███░░░░░░░  3 / 10   bagged (Mirror E1, E5, E9)
Phase X    : █░░░░░░░░░░░░░░  1 / 15   bagged (Mirror E11)
Phase XI   : █████░░░░░░░░░░  5 / 15   bagged (Mirror E27, E28, E29, E30, E31)
Phase XII  : ████░░░░░░░░░░░  4 / 15   bagged (Mirror E41, E42, E49, E51)
Phase XIII : ░░░░░░░░░░░░░░░  0 / 15
Phase XIV  : ░░░░░░░░░░░░░░░  0 / 15
Phase XV   : ░░░░░░░░░░  0 / 10
Phase XVI  : ░░░░░  0 / 5

Total: 13 / 100 Mirror summits bagged.
Critical-path MVP subset (12): bagged **1, 5, 11, 27, 30, 31, 49**; remaining 2 (route map = this doc), 40, 58, 87, 96.
Pass log:
- 2026-05-20 12:11 — wave 1 (Haiku × 6): E1, E5, E9, E27, E30, E49.
- 2026-05-20 12:19 — wave 2 (Haiku × 7): E11, E28, E29, E31, E41, E42, E51.
```

---

— Calm, 2026-05-20
