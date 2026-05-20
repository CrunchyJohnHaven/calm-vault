# Calm ZKAC — The Next 200 Engineering Everests (106–305)

> *"From state-attestation to values-alignment. The bank teller doesn't just need to know the customer is themself; they need to know whether to cooperate."*

**Companion to [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) (Everests 1–100, Calm Witness / ZKBB-User), [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md) (protocol spec), and [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) (sister primitive).**

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` immediately after commit.**

---

## The thesis

Calm Witness gives two autonomous agents a cryptographic primitive for sharing **one principal-authorized state bit** ("the human is themself, in baseline, or has flipped a duress signal"). The protocol's first 100 summits + extensions 101–105 built that primitive to working code: hash-chained log, Pedersen commitments, Schnorr Σ-protocol, range proofs, threshold disclosures, Sigsum anchors, Ed25519 operator identities, predicate-evaluator bridge, end-to-end demo.

**ZKAC (Zero-Knowledge Agent Cooperation) is the next layer.** It asks a different question: not *"is the human themself"* but *"does this principal's behavior and self-narration show alignment with the kinds of values I (the counterparty) require for cooperation?"*

The headline use cases:

- A foundation wants to fund only principals whose chain shows sustained, cross-tribal generosity. Today this requires invasive due diligence. With ZKAC: a single bit.
- An accelerator wants to admit only principals whose chain shows no willful harm to others. Today: legal discovery, references, gut feel. With ZKAC: a single bit.
- A peer-AI-collective wants to verify that a counterparty's principal is unselfish enough that defection is unlikely under stress. Today: impossible at scale. With ZKAC: a single bit.
- An accommodation provider wants to confirm a principal's chain demonstrates respect for people who are different from them. Today: deeply uncomfortable to ask. With ZKAC: the principal pre-authorizes the disclosure, the bit travels, no one has to interrogate anyone.

The threat model is harder than Calm Witness's because we are now making claims about character. The cryptography is the easier half. The harder half is **what predicates are publishable** (what may be measured), **whose values count** (the principal's, the counterparty's, some intersection), and **how to keep this from becoming a surveillance system**.

This document enumerates the 200 engineering everests between current state (Calm Witness v0 working end-to-end) and ZKAC v0 deployed: principals can pre-authorize alignment disclosures, counterparties can verify single-bit alignment claims, the bank-teller-note protocol generalizes from state to values.

---

## Numbering and convention

- Summits 1–100: Calm Witness original route map (parallel-session and Calm-session bagged across 2026-05-20).
- Summits 101–105: Extension summits added during the implementation work (Schnorr Σ-PoK, threshold disclosure, predicate bridge, vault identity, full demo).
- Summits 106–305: **This document.** Numbering is stable; if a summit is dropped, the number is retired, not reused.
- Beyond 305: future ZKAC v1 work, post-quantum migration, sister primitives.

Format per summit: `**Everest N — Name.** *Acceptance:* concrete third-party-verifiable test. *Effort:* S | M | L | XL. *Prereq:* dependency list. *Note:* optional context.`

Each summit eventually gets a peer gate script at `~/CredexAI/scripts/everest_NN_zkac_<slug>_gate.py`.

---

## Phase IX — Values Vocabulary (106–125)

The principal needs a way to express **what they value** in a form that a ZK circuit can evaluate. This phase defines the schema, the chain records, and the publication policy.

### Everest 106 — Values Primitive

**Everest 106 — Values Primitive Definition.** *Acceptance:* `CALM_VALUES_PRIMITIVE_v0.md` defines what a "value" is in this protocol (a principal-authored, predicate-evaluatable scalar attribute over a fixed dimension set). Reference Python module `calm_witness/values.py` with `ValuesVector` dataclass, `commit_values()`, and golden-input/output corpus. *Effort:* M. *Prereq:* 1, 51. *Note:* This is the foundation. Get the type right and everything composes; get it wrong and 200 summits collapse.

**Everest 107 — Values Dimensions v0.** *Acceptance:* A canonical set of 10 dimensions for v0, each with a single-paragraph definition and operational measurement note. The v0 dimensions are: `cooperation`, `fairness`, `honesty`, `non_harm`, `cross_difference_respect`, `generosity`, `non_tribal_engagement`, `repair_after_harm`, `consistency_under_stress`, `principal_authored_other`. Each dimension is a scalar in [0, 1] with documented semantics. *Effort:* L. *Prereq:* 106. *Note:* The dimensions are the hardest part of the whole route map — they encode normative claims about what alignment means. Default sourced from cross-cultural moral-psychology literature (Haidt's Moral Foundations, Schwartz's Value Survey, Inglehart-Welzel cultural map), but every dimension carries a "this is one principal's view of what matters; substitute your own" caveat in the v0 spec.

**Everest 108 — Values Self-Report Record Kind.** *Acceptance:* New chain record kinds `values_self_report` and `values_correction` defined in JSON schema and integrated into existing `user_state.jsonl`. Reference parser updated; live chain accepts a values self-report at seq:N. *Effort:* S. *Prereq:* 106, 107, 26. *Note:* Schema-compatible extension of the existing chain. No breaking changes; old verifiers ignore the new kind.

**Everest 109 — Values from Action (Inference Layer).** *Acceptance:* Predicate evaluator can infer per-dimension values scores from chain records of action (not just self-report). Example: `cooperation` score increments when chain shows joint-action records; `non_harm` decrements when chain shows harm records. Reference implementation `calm_witness/values_inference.py`. *Effort:* L. *Prereq:* 108. *Note:* The trust-but-verify layer. Self-report is one signal; action history is another. A ZK predicate can compare them, surfacing the gap between stated and revealed values.

**Everest 110 — Values vs Preferences.** *Acceptance:* `VALUES_VS_PREFERENCES.md` defines the boundary. Preferences ("I like chocolate") are NOT values; they don't enter the values vector. Values are normative commitments about how one acts toward others. The boundary is enforced by the predicate vocabulary refusing preference-flavored claims. *Effort:* S. *Prereq:* 107. *Note:* A surprisingly important fence. Without it, the values vector becomes a personality profile and the surveillance risk balloons.

**Everest 111 — Values Stability over Time.** *Acceptance:* Drift-detection module that flags values dimensions whose chain-inferred values shift faster than a configurable rate threshold per dimension. Acceptable drift rates documented per dimension. *Effort:* M. *Prereq:* 109. *Note:* Values DO change. A 20-year-old's values are not their 40-year-old's. The protocol must not pathologize change while still catching adversarial values-laundering.

**Everest 112 — Values Reversal Records.** *Acceptance:* `kind: "values_reversal"` record protocol — principal can declare a deliberate change in a dimension, with a non-revocable timestamp. Future predicates may weight pre-reversal and post-reversal evidence differently. *Effort:* M. *Prereq:* 108, 111. *Note:* The "I've grown" record. Crucial for accountability and for not punishing past mistakes that have been repaired.

**Everest 113 — Values Privacy Classes.** *Acceptance:* Per-dimension policy: principal sets which dimensions are disclosable to which counterparty class. Default deny; explicit per-class opt-in. *Effort:* S. *Prereq:* 18, 107. *Note:* Without this, the protocol becomes a panopticon. With it, the principal stays in charge.

**Everest 114 — Values Vector Serialization.** *Acceptance:* Canonical byte-stable form for the 10-dimension v0 values vector. Fixed-point integers (e.g., 0..10000 per dimension), big-endian, sorted by dimension name. Round-trip tested. *Effort:* S. *Prereq:* 107.

**Everest 115 — Cross-Cultural Values Mapping.** *Acceptance:* `CROSS_CULTURAL_VALUES.md` documents that v0 dimensions are not universal — what counts as "cooperation" or "respect" differs across cultures. Provides a mapping table and recommended weights per cultural context. Reviewed by at least one cross-cultural psychology researcher. *Effort:* L. *Prereq:* 107, 20. *Note:* Without this disclaimer, the protocol exports one set of values as universal. With it, the protocol is honest about being a tool, not a tribunal.

**Everest 116 — Values vs Identity Distinction.** *Acceptance:* `VALUES_VS_IDENTITY.md` defines the boundary between values (changeable normative commitments) and identity (the principal's self-declared way of being in the world, e.g., John's "artist working in the medium of intelligence"). Identity is NOT a values dimension; identity disclosure is a separate predicate family with stricter consent semantics. *Effort:* S. *Prereq:* 107. *Note:* This boundary defends against identity being measured as deviation from values, which would weaponize the protocol against neurodivergence, queerness, religious minorities, etc.

**Everest 117 — Values Registry.** *Acceptance:* Public registry of dimension definitions, with version history. Once a dimension is published in a version, its semantics never change; new semantics require a new dimension. *Effort:* M. *Prereq:* 107, 58.

**Everest 118 — Values Evolution Policy.** *Acceptance:* `VALUES_EVOLUTION.md` specifies how new dimensions enter the registry: principal-author proposal → outside-reviewer signoff (≥3) → community review window → registry entry. Mirror of Everest 54 (Predicate Audit & Public Review Process) applied to dimensions. *Effort:* M. *Prereq:* 117.

**Everest 119 — Values DSL.** *Acceptance:* Small total language for composing values dimensions into derived attestation-relevant attributes (e.g., "fairness AND cross_difference_respect"). Compile to predicate canonical form (Everest 52). *Effort:* L. *Prereq:* 117, 51. *Note:* Defers to fixed table for v0; DSL is an Everest 119+ opt-in.

**Everest 120 — Values from Witness.** *Acceptance:* Other principals (with their own Calm Witness chains) can attest to a values dimension of a third principal. Attestation records are first-class; aggregation rule defined. *Effort:* L. *Prereq:* 108, 11. *Note:* Witness attestations create the bootstrap for principals with thin chains. They also create new attack surface (Sybil, collusion).

**Everest 121 — Values Disagreement Protocol.** *Acceptance:* When self-report and witness disagree on a dimension, the protocol surfaces the disagreement (not one of the two wins). Counterparty predicate decides what to do with the gap. *Effort:* M. *Prereq:* 120. *Note:* The principal's self-report is not infallible; neither are witnesses. The honest move is to let the gap exist.

**Everest 122 — Values ZK Commitment.** *Acceptance:* Pedersen commitment to a 10-dimension values vector. Per-dimension commitment OR aggregated commitment (decision documented). Hiding/binding properties carry over from Everest 44. *Effort:* M. *Prereq:* 44, 114.

**Everest 123 — Values Circuit.** *Acceptance:* Arithmetic-circuit form of dimension-by-dimension comparison (e.g., "does the principal's `cooperation` score exceed threshold τ?"). Gate count documented; soundness review noted. *Effort:* L. *Prereq:* 122, 57.

**Everest 124 — Values-Vector Publication Policy.** *Acceptance:* The full values vector is NEVER published. Only per-dimension predicate evaluations are disclosable. The vector itself stays in the vault. *Effort:* S. *Prereq:* 113, 122. *Note:* Hard rule. The protocol exists because measuring is not knowing; disclosure must always be a single bit.

**Everest 125 — Values Audit and Revocation.** *Acceptance:* Principal can audit who has received what dimension disclosure. Principal can revoke a dimension's disclosure consent; outstanding proofs degrade per freshness window (Everest 75). *Effort:* M. *Prereq:* 86, 113.

---

## Phase X — Values Alignment Computation (126–145)

How do two values vectors get compared in ZK? The principal-side has a vector; the counterparty has a tolerance / desired vector; the protocol produces a single bit ("aligned enough"). The math is novel — it's the cryptographic equivalent of "do you share my values?" without either side revealing what their values are.

**Everest 126 — Alignment Metric Definition.** *Acceptance:* `ALIGNMENT_METRIC_v0.md` selects the canonical metric for v0. Default proposal: bounded Euclidean distance in the 10-dimension hypercube, with per-dimension weight vector supplied by counterparty. Other candidates (cosine, Manhattan, KL) discussed; v0 chooses one. *Effort:* M. *Prereq:* 107. *Note:* This is a NORMATIVE choice masquerading as a TECHNICAL choice. Document it as such.

**Everest 127 — Cosine Similarity in ZK.** *Acceptance:* If v0 uses cosine, ZK-friendly arithmetic-circuit version exists with documented gate count. (Skip if v0 uses Euclidean.) *Effort:* L. *Prereq:* 126.

**Everest 128 — Bounded Difference in ZK.** *Acceptance:* ZK circuit that proves "per-dimension absolute difference ≤ tolerance vector" without revealing either vector. Composes with Everest 45 range proofs (one range proof per dimension). *Effort:* L. *Prereq:* 126, 45. *Note:* The v0 default if Euclidean is the metric.

**Everest 129 — Per-Dimension Alignment ZK.** *Acceptance:* Proof that `|principal_dim_i - counterparty_dim_i| ≤ tolerance_i` for a specified dimension, without revealing either dim. Range proof per dimension. *Effort:* M. *Prereq:* 128.

**Everest 130 — Threshold Alignment Predicate.** *Acceptance:* Top-level predicate `cwp.v0.values_aligned_within(tolerance_vec, dimensions_in_scope)` that returns a bit. Compositional from Everest 129. *Effort:* M. *Prereq:* 129, 53.

**Everest 131 — Weighted Alignment.** *Acceptance:* Counterparty can weight dimensions: e.g., "I weigh non_harm 5x, cross_difference_respect 3x, others 1x." Weights are public (the counterparty's known tolerance), so they bind into the proof transcript via the context (Everest 75). *Effort:* M. *Prereq:* 130.

**Everest 132 — Asymmetric Alignment.** *Acceptance:* A's tolerance for B can differ from B's tolerance for A. Two distinct alignment proofs in a session. Protocol documented for the joint check (e.g., "both pass" / "at least one passes" / etc.). *Effort:* M. *Prereq:* 131.

**Everest 133 — Multi-Counterparty Alignment.** *Acceptance:* A coalition of N counterparties each issue alignment requests; principal produces N alignment proofs; coalition checks group-level alignment (all-pass, K-of-N, weighted). *Effort:* L. *Prereq:* 132.

**Everest 134 — Time-Dependent Alignment.** *Acceptance:* Alignment that decays over time — old chain evidence weighted less than recent. Weighting function documented; reference impl. *Effort:* L. *Prereq:* 109, 130.

**Everest 135 — Alignment with Context.** *Acceptance:* Principal's values vector may be context-conditional (professional context, family context, public context). Reference impl supports context-tagged vectors. *Effort:* M. *Prereq:* 108. *Note:* The "different in different rooms" recognition. Default v0 uses one context per principal.

**Everest 136 — Adversarial Alignment Defense.** *Acceptance:* Threat model document for adversarial fitting (principal manipulates self-reports to maximize alignment with a known-counterparty's published tolerance). Defenses documented (drift-rate caps, witness-attestation requirements, age-weighted evidence). *Effort:* L. *Prereq:* 130, 109. *Note:* The biggest open question of the route map. Defenses are partial; the protocol must be honest about its limits.

**Everest 137 — Alignment Under Hostile Witness.** *Acceptance:* When a hostile witness publishes a false values attestation about a principal, the protocol surfaces it (via Everest 121 disagreement) and lets predicate authors decide how to weight contested vs uncontested evidence. *Effort:* L. *Prereq:* 121, 136.

**Everest 138 — Alignment Circuit Composition.** *Acceptance:* Alignment proof composes with Calm Witness (E67/E102/E103) in a single transcript. *Effort:* M. *Prereq:* 130, 65.

**Everest 139 — Alignment Proof Transcript.** *Acceptance:* Wire format for an alignment disclosure. Carries alignment-proof bytes + commitment + counterparty's tolerance vector commitment + Calm Witness state-attestation bundle. *Effort:* M. *Prereq:* 138, 67. *Note:* This is the headline ZKAC artifact — "agent A learns: this human is aligned with my requirements." Single bit, fully attested.

**Everest 140 — Alignment Performance Budget.** *Acceptance:* End-to-end alignment proof on M-class hardware: prove < 5s, verify < 1s, transcript < 100KB. Bench script with current numbers. *Effort:* M. *Prereq:* 139. *Note:* Today's range proofs are ~7s per dimension; 10 dimensions = 70s, too slow. Ristretto migration (Everest 96) is the speedup path.

**Everest 141 — Alignment Disclosure Semantics.** *Acceptance:* Documented rules for what counterparty does with the bit (especially the bit=0 case). Bit=0 should NOT mean "this person is bad"; it means "alignment under the requested tolerance was not demonstrated." Cooperative redirection rather than gatekeeping is the v0 default semantic. *Effort:* M. *Prereq:* 130. *Note:* Without this discipline the protocol becomes a credit score for humanity.

**Everest 142 — Alignment Audit.** *Acceptance:* Principal can audit every alignment disclosure issued. Counterparty can audit every alignment verification performed. Both audit logs are themselves chain-resident. *Effort:* M. *Prereq:* 72, 139.

**Everest 143 — Alignment + Calm Pact Composition.** *Acceptance:* Joint transcript: Calm Pact (directive equality between agents) + Calm Witness (principal state) + ZKAC alignment (values alignment). One round trip; all three verify or none. *Effort:* L. *Prereq:* 94, 138. *Note:* This is the three-handshake model. Mission, person, values — verified in one shot.

**Everest 144 — Alignment + Calm Witness Composition.** *Acceptance:* Joint transcript: chain head shared, predicate evaluator runs both Calm Witness predicates and ZKAC alignment predicates, combined proof. *Effort:* M. *Prereq:* 130, 103.

**Everest 145 — Alignment Reference Implementation.** *Acceptance:* Open-source Rust + Python reference impl. Gate script. Performance numbers published. *Effort:* L. *Prereq:* 140.

---

## Phase XI — Harm-Avoidance Predicates (146–165)

The user explicitly named "evidence they willfully do harm to others" as a top-priority predicate family. This phase makes that concrete.

**Everest 146 — Harm Taxonomy.** *Acceptance:* `HARM_TAXONOMY_v0.md` enumerates 12 kinds of harm: direct physical, indirect physical, coercion, deception, theft, defamation, hate-speech, discrimination, group-harm, property, environmental, network/info. Each gets a one-paragraph operational definition. *Effort:* L. *Prereq:* 107. *Note:* The taxonomy is contested. v0 sources from criminal/tort law cross-jurisdiction + restorative-justice literature; downstream predicates may subset.

**Everest 147 — Direct Harm Absence Predicate.** *Acceptance:* `cwp.v0.no_direct_physical_harm_evidence(window=N_years)` returns 1 iff no chain record in window contains harm-evidence flags or witness attestations of direct physical harm. Reference evaluator + golden corpus. *Effort:* M. *Prereq:* 146, 53.

**Everest 148 — Indirect Harm Predicate.** *Acceptance:* `cwp.v0.no_indirect_harm_evidence(window)` covering chains of action where the principal's contribution led to harm via intermediaries. *Effort:* L. *Prereq:* 146.

**Everest 149 — Coercion Absence.** *Acceptance:* `cwp.v0.no_coercion_evidence(window)`. *Effort:* M. *Prereq:* 146.

**Everest 150 — Deception Absence.** *Acceptance:* `cwp.v0.no_deception_evidence(window)`. *Effort:* M. *Prereq:* 146.

**Everest 151 — Theft Absence.** *Acceptance:* `cwp.v0.no_theft_evidence(window)`. *Effort:* S. *Prereq:* 146.

**Everest 152 — Violence Absence.** *Acceptance:* `cwp.v0.no_violence_evidence(window)`. *Effort:* M. *Prereq:* 146.

**Everest 153 — Defamation Absence.** *Acceptance:* `cwp.v0.no_defamation_evidence(window)`. *Effort:* M. *Prereq:* 146.

**Everest 154 — Hate-Speech Absence.** *Acceptance:* `cwp.v0.no_hate_speech_evidence(window)`. *Effort:* L. *Prereq:* 146. *Note:* Definition of "hate speech" is jurisdiction-dependent; v0 specifies which body of definitions (US 1st Amendment line / EU AVMSD / UK Public Order Act) the chain records are framed under.

**Everest 155 — Discrimination Absence.** *Acceptance:* `cwp.v0.no_discrimination_evidence(window)`. *Effort:* L. *Prereq:* 146.

**Everest 156 — Group-Harm Predicate.** *Acceptance:* `cwp.v0.no_group_harm_evidence(window)` for harms whose target is a group rather than an individual. *Effort:* L. *Prereq:* 148.

**Everest 157 — Self-Harm Predicate (Consent-Bounded).** *Acceptance:* `cwp.v0.self_harm_attested(window)` returns the principal's self-attested risk state. Consent-gated to high-trust counterparty classes only (e.g., principal's licensed therapist, principal-designated next-of-kin). *Effort:* L. *Prereq:* 146, 88. *Note:* The most ethically loaded predicate of the whole route map. Disability-advocacy review is non-negotiable.

**Everest 158 — Property-Harm Predicate.** *Acceptance:* `cwp.v0.no_property_harm_evidence(window)`. *Effort:* S. *Prereq:* 146.

**Everest 159 — Environmental-Harm Predicate.** *Acceptance:* `cwp.v0.no_environmental_harm_evidence(window)`. *Effort:* M. *Prereq:* 146.

**Everest 160 — Network/Info-Harm Predicate.** *Acceptance:* `cwp.v0.no_info_harm_evidence(window)` covering doxing, malware, denial-of-service, infrastructure attacks. *Effort:* M. *Prereq:* 146.

**Everest 161 — Power-Imbalance-Abuse Predicate.** *Acceptance:* `cwp.v0.no_power_abuse_evidence(window)` — harms specifically enabled by power asymmetry (e.g., supervisor abusing subordinate). *Effort:* L. *Prereq:* 146.

**Everest 162 — Trust-Violation Predicate.** *Acceptance:* `cwp.v0.no_trust_violation_evidence(window)`. *Effort:* M. *Prereq:* 146, 201.

**Everest 163 — Harm-Reversal Predicate.** *Acceptance:* `cwp.v0.harm_reversed(specific_harm_id)` — when a past harm has been documented as repaired through restitution / restorative-justice protocol. *Effort:* L. *Prereq:* 112, 146.

**Everest 164 — Harm Intent vs Effect Distinction.** *Acceptance:* `HARM_INTENT_VS_EFFECT.md` documents the v0 protocol's stance: the user specifically said "willfully do harm." Intent is required; chain records distinguish intent from accident from third-party-caused harm. *Effort:* M. *Prereq:* 146.

**Everest 165 — Harm Aggregate Scoring.** *Acceptance:* Optional aggregate: counterparty may request "no harm of any kind in window." Bit = AND of all 12 absence predicates. *Effort:* S. *Prereq:* 147–162, 61.

---

## Phase XII — Cooperation & Generosity Predicates (166–185)

Positive evidence, the symmetric pair to harm absence. The user named "unselfish" as a top-priority predicate.

**Everest 166 — Generosity Baseline.** *Acceptance:* `cwp.v0.generosity_evidence(window, threshold)` — chain shows giving (time, money, skill) without immediate quid-pro-quo. Reference evaluator + golden corpus. *Effort:* L. *Prereq:* 107, 109.

**Everest 167 — Coalition Formation Predicate.** *Acceptance:* `cwp.v0.coalition_formation_evidence(window)` — chain shows joint action with N+ distinct collaborators. *Effort:* M. *Prereq:* 109.

**Everest 168 — Mentorship Indicators.** *Acceptance:* `cwp.v0.mentorship_evidence(window)` — sustained, low-reciprocity teaching/guidance. *Effort:* M. *Prereq:* 109.

**Everest 169 — Public-Goods Contribution.** *Acceptance:* `cwp.v0.public_goods_evidence(window)` — chain shows contributions to non-rivalrous, non-excludable goods (open source, public infrastructure, civic work). *Effort:* M. *Prereq:* 109.

**Everest 170 — Sustained Cooperation Predicate.** *Acceptance:* `cwp.v0.sustained_cooperation(window, min_relationships)` — cooperation across multiple relationships maintained over time, not flash-in-pan. *Effort:* L. *Prereq:* 167.

**Everest 171 — Reciprocity vs Altruism.** *Acceptance:* `cwp.v0.altruism_index(window)` separates "I help because I expect help back" from "I help with no expected return." Operationalized via observed return pattern in chain. *Effort:* L. *Prereq:* 166. *Note:* This directly addresses the user's "unselfish" framing — pure-altruism evidence vs reciprocity.

**Everest 172 — Cooperation Across Difference.** *Acceptance:* `cwp.v0.cooperation_across_difference(window)` — chain shows joint action with counterparts from different tribes, languages, regions, classes. The headline operationalization of "respectful to people who are different." *Effort:* L. *Prereq:* 170. *Note:* This is one of the user-named predicates; treat it as load-bearing.

**Everest 173 — Helping When Costly.** *Acceptance:* `cwp.v0.help_when_costly(window)` — help given at evident personal cost to the principal (time, money, reputation). *Effort:* M. *Prereq:* 166.

**Everest 174 — Forgiveness Records.** *Acceptance:* `kind: "forgiveness"` record protocol. Principal records that they have released a specific prior harm-record from their assessment of a counterparty. *Effort:* M. *Prereq:* 163.

**Everest 175 — Reconciliation Records.** *Acceptance:* `kind: "reconciliation"` — bilateral or multilateral. Both parties' chains carry matching records. *Effort:* M. *Prereq:* 174.

**Everest 176 — Gift Records.** *Acceptance:* `kind: "gift"` record. Asymmetric value transfer without quid-pro-quo expectation. *Effort:* S. *Prereq:* 166.

**Everest 177 — Time-Given Records.** *Acceptance:* `kind: "time_given"` — durable record of substantial time invested for another's benefit. *Effort:* S. *Prereq:* 166.

**Everest 178 — Skill-Shared Records.** *Acceptance:* `kind: "skill_shared"`. *Effort:* S. *Prereq:* 168.

**Everest 179 — Endorsement Records.** *Acceptance:* `kind: "endorsement"` — principal publicly stakes reputation on a counterparty's character. Endorsements have weight in counterparty's reputation aggregation. *Effort:* M. *Prereq:* 120, 211.

**Everest 180 — Mutual-Aid Records.** *Acceptance:* `kind: "mutual_aid"` — group-level cooperation under defined rules (e.g., disaster response, neighborhood network). *Effort:* M. *Prereq:* 167.

**Everest 181 — Collaboration Outcome Records.** *Acceptance:* `kind: "collaboration_outcome"` — what was actually built / shipped / delivered. *Effort:* M. *Prereq:* 167.

**Everest 182 — Generosity Aggregation.** *Acceptance:* Aggregation rule for the generosity-family records into the `generosity` dimension score. *Effort:* M. *Prereq:* 166, 176, 177, 178.

**Everest 183 — Cooperation Streak.** *Acceptance:* `cwp.v0.cooperation_streak(window, min_length)` — uninterrupted sequence of cooperative records over a duration. *Effort:* S. *Prereq:* 170.

**Everest 184 — Cooperation Graph Without Revealing Graph.** *Acceptance:* ZK predicate over the principal's cooperation graph (who they've worked with) that reveals only properties (graph density, average path length, cross-cluster bridging) without revealing the graph itself. *Effort:* XL. *Prereq:* 167. *Note:* Hardest summit in this phase.

**Everest 185 — Cooperation Predicate ZK Circuit.** *Acceptance:* Arithmetic-circuit forms of the cooperation predicates, integrated with the alignment proof transcript. *Effort:* L. *Prereq:* 170, 123.

---

## Phase XIII — Tribalism & Out-Group Engagement (186–200)

The user named "untribal" as a top-priority predicate. This phase makes it concrete with care, because "tribalism" can be protective (e.g., minority solidarity) or harmful (e.g., out-group dehumanization).

**Everest 186 — Tribe Taxonomy.** *Acceptance:* `TRIBE_TAXONOMY.md` defines what "tribes" are in this protocol — culturally constituted in-groups along axes: kin, ethnicity, religion, nation, class, language, profession, ideology, generation. Each principal's "tribe set" is principal-authored, not externally assigned. *Effort:* L. *Prereq:* 115. *Note:* The protocol must NEVER assign tribes to principals from outside. Self-declaration only.

**Everest 187 — Out-Group Definition.** *Acceptance:* For a given principal P, "out-group" is the complement of P's self-declared tribe set. Out-group is not "enemy"; it is "other." *Effort:* S. *Prereq:* 186.

**Everest 188 — Cross-Tribe Interaction Evidence.** *Acceptance:* `cwp.v0.cross_tribe_interaction_evidence(window)` — chain shows substantive interactions with out-group members. Substantive = non-transactional, non-extractive. *Effort:* M. *Prereq:* 187.

**Everest 189 — Out-Group Respect Predicate.** *Acceptance:* `cwp.v0.cross_difference_respect(window)` — chain shows respectful engagement with out-group members. The headline operationalization of "respectful to people who are different." Respect = absence of derogatory records + presence of cooperative records across the boundary. *Effort:* L. *Prereq:* 172, 188.

**Everest 190 — Curiosity-About-Difference Predicate.** *Acceptance:* `cwp.v0.curiosity_about_difference(window)` — chain shows initiated engagement to learn from out-group rather than to convert/correct. *Effort:* M. *Prereq:* 189.

**Everest 191 — Bridge-Building Records.** *Acceptance:* `kind: "bridge_built"` — principal records connecting two parties who would not otherwise meet, across a tribal boundary. *Effort:* M. *Prereq:* 188.

**Everest 192 — Cross-Cultural Collaboration.** *Acceptance:* `cwp.v0.cross_cultural_collaboration(window, min_cultures)` — joint outputs with collaborators from N+ documented cultural backgrounds. *Effort:* M. *Prereq:* 172, 188.

**Everest 193 — Tribal Lock-In Absence.** *Acceptance:* `cwp.v0.non_tribal_lock_in(window)` — chain does NOT show all interactions confined to in-group only. *Effort:* M. *Prereq:* 188.

**Everest 194 — Out-Group Benefit Predicate.** *Acceptance:* `cwp.v0.acted_for_out_group_benefit(window)` — chain shows action taken to benefit out-group at evident cost to in-group standing. *Effort:* L. *Prereq:* 188, 173.

**Everest 195 — Pluralism Predicate.** *Acceptance:* `cwp.v0.pluralism(window)` — principal's chain shows acceptance that multiple incompatible worldviews can coexist without one being "right." *Effort:* L. *Prereq:* 189.

**Everest 196 — Anti-Tribal Evidence Aggregation.** *Acceptance:* Aggregation rule for the cross-tribe family into the `non_tribal_engagement` dimension score. *Effort:* M. *Prereq:* 188–195.

**Everest 197 — Tribal Anti-Pattern Documentation.** *Acceptance:* `TRIBAL_ANTIPATTERN.md` documents tribal records that are AGAINST out-group (dehumanization, scapegoating). These are harm-records (Phase XI) re-cast under the tribal lens. *Effort:* M. *Prereq:* 146, 186.

**Everest 198 — Protective Tribalism Recognition.** *Acceptance:* `PROTECTIVE_TRIBALISM.md` — when a marginalized principal's in-group orientation is protective (e.g., support networks within a persecuted minority), this is NOT a `non_tribal_engagement` penalty. Threshold for "protective" vs "harmful" tribalism documented. *Effort:* L. *Prereq:* 186, 88. *Note:* This is the most likely place for the protocol to inadvertently punish solidarity. Disability/minority advocacy review is required before this everest closes.

**Everest 199 — Tribalism vs Solidarity Distinction.** *Acceptance:* Operational distinction codified into the predicate evaluator. Solidarity = in-group support that does not require out-group denigration. Tribalism (in the harmful sense) = in-group support that defines itself against out-group. *Effort:* L. *Prereq:* 198, 197.

**Everest 200 — Pluralism + Alignment Composition.** *Acceptance:* `cwp.v0.pluralism_and_alignment(tolerance_vec)` — composite predicate that returns 1 only when principal demonstrates pluralism AND alignment with counterparty's tolerance vector. *Effort:* M. *Prereq:* 195, 130.

---

## Phase XIV — Trust & Reputation Infrastructure (201–225)

How strangers bootstrap trust in a ZK setting. Composes with the values and harm-avoidance predicates to answer: "given these values claims, how confident should I be?"

**Everest 201 — Trust Graph Primitive.** *Acceptance:* `TRUST_GRAPH.md` defines a directed weighted graph where principals are nodes and trust attestations are edges. Reference implementation in `calm_witness/trust.py`. *Effort:* L. *Prereq:* 120.

**Everest 202 — Trust Transitivity.** *Acceptance:* Decay function for trust through a chain (A trusts B trusts C → reduced trust A→C). Documented rule. *Effort:* M. *Prereq:* 201.

**Everest 203 — Trust Decay over Time.** *Acceptance:* Stale trust attestations decay per dimension. Half-life per relationship type. *Effort:* M. *Prereq:* 201.

**Everest 204 — Trust by Attestation.** *Acceptance:* Third-party witness attestations (Everest 120) feed into the trust graph. *Effort:* M. *Prereq:* 120, 201.

**Everest 205 — Trust by Joint History.** *Acceptance:* Cooperation records (Phase XII) feed trust attestations bidirectionally between collaborators. *Effort:* M. *Prereq:* 181, 201.

**Everest 206 — Trust Under Disagreement.** *Acceptance:* When two principals' chains conflict (one says they cooperated, other says they didn't), trust algorithm degrades both edges and surfaces the conflict. *Effort:* L. *Prereq:* 121, 201.

**Everest 207 — Distrust Records.** *Acceptance:* `kind: "distrust"` — principal records an active distrust assertion. First-class chain record. *Effort:* M. *Prereq:* 201.

**Everest 208 — Trust Rehabilitation.** *Acceptance:* Protocol for repairing trust after a documented breach. Composes with Everest 163 (harm reversal). *Effort:* M. *Prereq:* 174, 207.

**Everest 209 — Trust ZK Proof.** *Acceptance:* ZK proof that a principal has a trust path from a counterparty to a third party, without revealing the path. *Effort:* XL. *Prereq:* 201, 65. *Note:* Hard summit. Composes Pedersen + Σ-protocol over graph properties.

**Everest 210 — Trust + Values-Alignment Composition.** *Acceptance:* Combined proof: "this principal is trusted by N people in your network AND has values aligned to your tolerance." *Effort:* M. *Prereq:* 209, 130.

**Everest 211 — Reputation Aggregation.** *Acceptance:* `cwp.v0.reputation_aggregate(dimension, window)` — aggregated reputation per dimension from trust-graph + witness attestations + chain self-narration. *Effort:* L. *Prereq:* 120, 201.

**Everest 212 — Sybil Resistance via Personhood + Trust.** *Acceptance:* Sybil-resistant reputation requires both (a) personhood proof (via Everest 11/22 CredexAI VC) and (b) trust-graph integration over N+ months. *Effort:* L. *Prereq:* 11, 201.

**Everest 213 — Trust Threshold Predicate.** *Acceptance:* `cwp.v0.trusted_by_threshold(counterparty_view, threshold)` — single bit. *Effort:* M. *Prereq:* 211.

**Everest 214 — Trust Ladder.** *Acceptance:* Tiered trust levels (acquaintance, collaborator, vouched, vouched-publicly) with per-tier privileges in the protocol. *Effort:* M. *Prereq:* 213.

**Everest 215 — Trust Audit.** *Acceptance:* Principal can audit who has trusted/distrusted them publicly. Counterparty can audit incoming trust signals. *Effort:* M. *Prereq:* 142, 201.

**Everest 216 — Trust Under Coercion.** *Acceptance:* Protocol for principals to mark trust attestations as "under coercion" — flagging that a positive attestation may have been signed under duress. Defeasible at-rest. *Effort:* L. *Prereq:* 85, 207.

**Everest 217 — Trust-Network Privacy.** *Acceptance:* Trust network topology is not published; only aggregate predicates are evaluable in ZK. *Effort:* L. *Prereq:* 209, 124.

**Everest 218 — Trust vs Reputation Distinction.** *Acceptance:* `TRUST_VS_REPUTATION.md` — trust is dyadic (A trusts B); reputation is many-to-one aggregate (the network trusts B). v0 supports both as distinct primitives. *Effort:* S. *Prereq:* 201, 211.

**Everest 219 — Trust Between Agent Collectives.** *Acceptance:* When agents represent collectives (e.g., Calm-aligned operators), trust accrues at the collective level. Composition rule documented. *Effort:* L. *Prereq:* 11, 211.

**Everest 220 — Trust + Calm Pact Composition.** *Acceptance:* Calm Pact's directive-equality proof composes with trust-network proof in a single transcript. *Effort:* M. *Prereq:* 94, 209.

**Everest 221 — Trust + Alignment Composition.** *Acceptance:* Already covered by Everest 210; this is the deployment-ready bundle. *Effort:* S. *Prereq:* 210.

**Everest 222 — Trust + Harm-Avoidance Composition.** *Acceptance:* Trust + no-harm composite predicate. *Effort:* S. *Prereq:* 165, 213.

**Everest 223 — Trust Calibration.** *Acceptance:* `TRUST_CALIBRATION.md` documents over-trust failure modes and suggests counterparty-side calibration. *Effort:* M. *Prereq:* 213.

**Everest 224 — Trust Witness Protocol.** *Acceptance:* Protocol for high-stakes trust ceremonies (e.g., adoption into a coalition). Notary-witnessed; chain-anchored. *Effort:* M. *Prereq:* 19, 207.

**Everest 225 — Trust Reference Implementation.** *Acceptance:* Rust + Python; gate script; published benchmarks. *Effort:* L. *Prereq:* 213.

---

## Phase XV — Selfishness ↔ Altruism Spectrum (226–245)

User named "unselfish" as top-priority. The cooperation predicates (Phase XII) are positive evidence; this phase calibrates the spectrum.

**Everest 226 — Selfishness Baseline Measurement.** *Acceptance:* `SELFISHNESS_BASELINE.md` operationalizes what counts as selfish in chain data. Default: ratio of "resources kept" to "resources shared" across documented events. *Effort:* L. *Prereq:* 109, 166. *Note:* The hardest definition of the route map. Selfishness is culturally loaded.

**Everest 227 — Altruism vs Reciprocity in Chain Data.** *Acceptance:* Reference implementation that distinguishes one-shot gifts from reciprocal exchanges over a window. *Effort:* M. *Prereq:* 171.

**Everest 228 — Sacrificial Action Records.** *Acceptance:* `kind: "sacrificial_action"` — principal records taking a personal cost for another's benefit, with cost magnitude attested. *Effort:* M. *Prereq:* 173.

**Everest 229 — Selfishness Predicate.** *Acceptance:* `cwp.v0.low_altruism_evidence(window, threshold)`. *Effort:* M. *Prereq:* 226.

**Everest 230 — Altruism Predicate.** *Acceptance:* `cwp.v0.high_altruism_evidence(window, threshold)`. *Effort:* M. *Prereq:* 227.

**Everest 231 — Selfishness Disclosure Ethics.** *Acceptance:* `SELFISHNESS_DISCLOSURE_ETHICS.md` documents the consent-class restrictions for the selfishness predicates — they are particularly susceptible to discrimination and require stricter consent than the average predicate. *Effort:* M. *Prereq:* 113, 226.

**Everest 232 — Altruism + Generosity Composition.** *Acceptance:* Composite predicate that requires both. *Effort:* S. *Prereq:* 166, 230.

**Everest 233 — Selfishness Under Stress.** *Acceptance:* `cwp.v0.altruism_under_stress(window)` — does the principal stay generous when resources are tight? Operationalized via chain evidence of stress events + concurrent giving. *Effort:* L. *Prereq:* 230.

**Everest 234 — Resource-Allocation Patterns.** *Acceptance:* Reference evaluator that aggregates chain records of resource flow into per-direction patterns. *Effort:* M. *Prereq:* 109, 226.

**Everest 235 — Self-Other Balance.** *Acceptance:* `cwp.v0.self_other_balance(window)` — neither pure-self (selfish) nor pure-other (martyrdom). Healthy balance is the principal's stated intent in chain. *Effort:* L. *Prereq:* 234.

**Everest 236 — Selfish-Defection Evidence.** *Acceptance:* `cwp.v0.no_selfish_defection_evidence(window)` — principal does not abandon collaborations at the first sign of personal cost. *Effort:* M. *Prereq:* 170.

**Everest 237 — Altruistic Cooperation Evidence.** *Acceptance:* `cwp.v0.altruistic_cooperation_evidence(window)` — cooperation maintained beyond reciprocal payoff. *Effort:* M. *Prereq:* 171, 230.

**Everest 238 — Mixed-Motive Recognition.** *Acceptance:* `MIXED_MOTIVES.md` — most action has mixed motive. Predicates do not require purity; they measure tendency. *Effort:* S. *Prereq:* 230.

**Everest 239 — Selfishness Measurement Bias.** *Acceptance:* Document of known biases in selfishness measurement (e.g., wealth-blind metrics penalize the poor; time-given is class-coded). Mitigations applied to the v0 evaluator. *Effort:* L. *Prereq:* 226, 88.

**Everest 240 — Cultural Variation in Selfishness.** *Acceptance:* Cross-cultural review of the selfishness/altruism dimension. v0 evaluator weighted by self-declared cultural context (Everest 115). *Effort:* L. *Prereq:* 115, 226.

**Everest 241 — Selfishness vs Healthy Self-Care.** *Acceptance:* `SELFISHNESS_VS_SELF_CARE.md` — self-care, boundary-setting, and rest are not selfish. Operational distinction with examples. *Effort:* M. *Prereq:* 235.

**Everest 242 — Altruism Circuit.** *Acceptance:* Arithmetic-circuit form of the altruism aggregation. *Effort:* L. *Prereq:* 227, 123.

**Everest 243 — Selfishness Proof.** *Acceptance:* Symmetric — proves the absence of low-altruism evidence without revealing chain content. *Effort:* L. *Prereq:* 229, 123.

**Everest 244 — Selfishness Aggregate Scoring.** *Acceptance:* The `generosity` dimension scoring rule. *Effort:* S. *Prereq:* 182.

**Everest 245 — Selfishness Disclosure to Counterparty.** *Acceptance:* End-to-end disclosure flow for selfishness/altruism predicates. *Effort:* M. *Prereq:* 230, 67.

---

## Phase XVI — Multi-Agent Coalition Formation (246–265)

Where N agents bootstrap collective trust + alignment from individual disclosures. This is the production payoff: not just A trusts B but A, B, C, D, E form a coalition that meets shared values bars.

**Everest 246 — Coalition Primitive.** *Acceptance:* `COALITION_PRIMITIVE.md` + reference impl. A coalition is N+1 principals who have published mutual alignment + trust + harm-absence + values vectors that satisfy a shared coalition agreement. *Effort:* L. *Prereq:* 130, 210.

**Everest 247 — Coalition Values-Alignment Requirement.** *Acceptance:* Each member must pass each other's alignment check; coalition agreement specifies tolerance vector. *Effort:* M. *Prereq:* 132, 246.

**Everest 248 — Coalition Harm-Absence Requirement.** *Acceptance:* All members must pass the aggregate harm-absence predicate per the coalition agreement. *Effort:* S. *Prereq:* 165, 246.

**Everest 249 — Coalition Formation Protocol.** *Acceptance:* Step-by-step protocol for N principals to bootstrap a coalition: propose, exchange alignment proofs in pairwise grid, ratify with collective signature. *Effort:* L. *Prereq:* 247, 248.

**Everest 250 — Coalition Dissolution Protocol.** *Acceptance:* Documented + ZK-verifiable dissolution — alternative to silent walk-away. *Effort:* M. *Prereq:* 249.

**Everest 251 — Coalition Member Rotation.** *Acceptance:* New-member-joins, old-member-leaves, all alignment+harm checks rerun, no full re-formation required. *Effort:* L. *Prereq:* 249.

**Everest 252 — Coalition Defection Detection.** *Acceptance:* When a member's chain shows action contrary to coalition values, defection is detectable via predicate evaluation. *Effort:* L. *Prereq:* 247.

**Everest 253 — Coalition Aggregate Values.** *Acceptance:* `cwp.v0.coalition_aggregate_values(coalition_id)` — coalition's collective values vector, derivable from member vectors. *Effort:* M. *Prereq:* 247.

**Everest 254 — Coalition + Calm Pact Joint Proof.** *Acceptance:* Single round-trip proof: directive equality (Pact) + state attestation (Witness) + alignment (ZKAC) for an N-member coalition. *Effort:* XL. *Prereq:* 143, 249.

**Everest 255 — Coalition + Calm Witness Joint Proof.** *Acceptance:* Already covered by 254; this is the deployment-ready bundle for the state+values stack. *Effort:* S. *Prereq:* 254.

**Everest 256 — Coalition + Values-Alignment Joint Proof.** *Acceptance:* Already covered by 254. *Effort:* S. *Prereq:* 254.

**Everest 257 — Coalition Decision-Making Protocol.** *Acceptance:* When the coalition needs to make a decision, the protocol surfaces aggregate values + per-member alignment scores. *Effort:* L. *Prereq:* 253.

**Everest 258 — Coalition Resource Pooling.** *Acceptance:* Optional sub-protocol for resource pooling among coalition members with alignment-conditioned shares. *Effort:* L. *Prereq:* 257.

**Everest 259 — Coalition Reputation.** *Acceptance:* Coalition has its own reputation, distinct from member reputations. *Effort:* M. *Prereq:* 219.

**Everest 260 — Coalition Extension Protocol.** *Acceptance:* Welcoming new members in a way that respects existing members' alignment requirements. *Effort:* M. *Prereq:* 251.

**Everest 261 — Coalition vs Network Distinction.** *Acceptance:* `COALITION_VS_NETWORK.md` — coalitions are formal (joint signatures, shared agreement); networks are informal (trust graph). v0 supports both. *Effort:* S. *Prereq:* 201, 246.

**Everest 262 — Coalition Under Stress.** *Acceptance:* Stress-test scenarios + recovery protocols. *Effort:* L. *Prereq:* 249, 233.

**Everest 263 — Coalition Longevity Records.** *Acceptance:* `kind: "coalition_milestone"` — duration, work-output, member-stability records. *Effort:* M. *Prereq:* 249.

**Everest 264 — Coalition Transparency Policy.** *Acceptance:* What about the coalition is public (existence, founding date, member-count); what stays private (member-identities by default). *Effort:* M. *Prereq:* 124.

**Everest 265 — Coalition Reference Implementation.** *Acceptance:* Rust + Python; gate script; live multi-process demo. *Effort:* XL. *Prereq:* 249.

---

## Phase XVII — Adversarial & Stress Conditions (266–285)

Hostile counterparties, slow-poison attacks, sybils, defection cascades.

**Everest 266 — Hostile Counterparty Taxonomy.** *Acceptance:* `HOSTILE_COUNTERPARTY_TAXONOMY.md` — enumerated threat classes (extractive, deceptive, coercive, opportunistic, ideological). *Effort:* M. *Prereq:* 2.

**Everest 267 — Coercion Detection.** *Acceptance:* Behavioral indicators of principal-side coercion in chain records (sudden values reversal, unusual disclosure patterns). Surface to operator; do not auto-decide. *Effort:* L. *Prereq:* 216.

**Everest 268 — Manipulation Detection.** *Acceptance:* Indicators that counterparty is manipulating principal's disclosure path (e.g., asking only for predicates likely to bias judgment). *Effort:* L. *Prereq:* 60.

**Everest 269 — Sybil Attack on Values.** *Acceptance:* Defense against fake witness attestations from sybil identities supporting a principal's values claims. *Effort:* L. *Prereq:* 212.

**Everest 270 — False-Flag Values Attack.** *Acceptance:* Defense against principal-side false-flag attestations (e.g., principal pays sybils to attest their cooperation). *Effort:* L. *Prereq:* 269.

**Everest 271 — Slow-Poison Attack.** *Acceptance:* Detection of principals who deliberately drift their values reports over time to evade detection. Bounded drift rates with hard caps. *Effort:* L. *Prereq:* 111.

**Everest 272 — Defection Cascade.** *Acceptance:* When a member defects in a coalition, the rest don't immediately follow. Stress-test protocol. *Effort:* L. *Prereq:* 252.

**Everest 273 — Coordinated Misinformation.** *Acceptance:* Detection of coordinated false attestations across multiple witnesses. *Effort:* L. *Prereq:* 269.

**Everest 274 — Values-Laundering Attack.** *Acceptance:* Detection of principals who attempt to "wash" past harm through synthetic cooperation records. *Effort:* L. *Prereq:* 163, 271.

**Everest 275 — Counterparty Corruption.** *Acceptance:* Recovery protocol when a previously-trusted counterparty is found to have leaked / abused disclosures. *Effort:* L. *Prereq:* 17.

**Everest 276 — Witness Corruption.** *Acceptance:* When a witness's signing key is compromised, the protocol degrades their past attestations and surfaces them. *Effort:* L. *Prereq:* 17.

**Everest 277 — Log Corruption.** *Acceptance:* When a Sigsum log operator is compromised, the protocol surfaces affected chains and the failure window. *Effort:* L. *Prereq:* 80.

**Everest 278 — Time-Skew Attack.** *Acceptance:* Defense against an adversary who manipulates the Roughtime/Sigsum clock to make past evidence look recent or vice versa. *Effort:* L. *Prereq:* 79.

**Everest 279 — Replay Across Coalitions.** *Acceptance:* Defense against replaying an alignment proof produced for coalition A to coalition B. *Effort:* M. *Prereq:* 75.

**Everest 280 — Adversarial Alignment Fitting.** *Acceptance:* Documented defenses for the case where the principal knows the counterparty's published tolerance and fits self-reports to maximize alignment. *Effort:* XL. *Prereq:* 136. *Note:* The biggest open research problem of the route map.

**Everest 281 — Defense in Depth.** *Acceptance:* `DEFENSE_IN_DEPTH.md` — layered defenses across the protocol stack. *Effort:* L. *Prereq:* 266–280.

**Everest 282 — Failure-Mode Mapping.** *Acceptance:* Extension of Everest 9 to cover the ZKAC failure modes. *Effort:* L. *Prereq:* 9, 281.

**Everest 283 — Recovery Protocols.** *Acceptance:* Documented recovery from each failure mode in 282. *Effort:* L. *Prereq:* 282.

**Everest 284 — Audit Under Attack.** *Acceptance:* When the protocol is under attack, the audit log itself must remain trustworthy. *Effort:* L. *Prereq:* 215, 277.

**Everest 285 — Resilience Certification.** *Acceptance:* Process for certifying a deployment as resilient against the 266–284 failure modes. *Effort:* L. *Prereq:* 283.

---

## Phase XVIII — Production, Composition, Governance (286–305)

The final climb. The Calm umbrella deployed.

**Everest 286 — Full Calm Umbrella Composition.** *Acceptance:* Single transcript composes Calm Pact (directive equality) + Calm Witness (state attestation) + ZKAC (values alignment) + Calm Audit (action-history disclosure, when that primitive lands). *Effort:* XL. *Prereq:* 254.

**Everest 287 — ZKAC Reference Implementation.** *Acceptance:* Rust + Python + Swift bindings. Gate scripts for E106–E285. *Effort:* XL. *Prereq:* 286.

**Everest 288 — ZKAC Public Registry.** *Acceptance:* Public registry of v0 dimensions, predicates, and circuits. Sigsum-anchored. *Effort:* L. *Prereq:* 117, 58.

**Everest 289 — ZKAC Adversarial Review Program.** *Acceptance:* Bug bounty live; researcher cohort engaged. *Effort:* L. *Prereq:* 93, 287.

**Everest 290 — ZKAC Standards Submission.** *Acceptance:* Formal submission to NIST AI Safety Institute / IETF / W3C / similar body. *Effort:* L. *Prereq:* 91.

**Everest 291 — ZKAC Deployment Guide.** *Acceptance:* `DEPLOYMENT_GUIDE.md` for operators starting from zero. *Effort:* L. *Prereq:* 287.

**Everest 292 — ZKAC Disability Deployment Guide.** *Acceptance:* `DISABILITY_DEPLOYMENT_GUIDE.md` — how ZKAC composes with disability-rights protocols. Reviewed by disability advocacy bodies. *Effort:* L. *Prereq:* 99, 198.

**Everest 293 — ZKAC Cross-Jurisdiction Analysis.** *Acceptance:* `CROSS_JURISDICTION_v1.md` for ZKAC (extends Everest 20 / 79 / 89 / 98). Counsel in US, EU, UK, CA, JP, AU. *Effort:* XL. *Prereq:* 98.

**Everest 294 — ZKAC Ethical Review Board.** *Acceptance:* Standing board ≥5 outsiders (ethics, disability, civil liberties, marginalized-community advocacy). Reviews every new predicate before publication. *Effort:* L. *Prereq:* 80, 88.

**Everest 295 — ZKAC Public Deployment Ceremony.** *Acceptance:* The protocol goes live. ≥10 principals operate; ≥3 coalitions form. A counterparty agent in production accepts a values-alignment proof and adjusts behavior on the bit. *Effort:* XL. *Prereq:* 100, 287.

**Everest 296 — ZKAC + Calm Pact Production Demo.** *Acceptance:* End-to-end demo: two agents prove directive equality + values alignment + state attestation, then make a real cooperative decision. *Effort:* L. *Prereq:* 286.

**Everest 297 — ZKAC + Calm Witness Production Demo.** *Acceptance:* End-to-end demo: principal + counterparty + ZKAC predicate over the live chain. *Effort:* L. *Prereq:* 105, 286.

**Everest 298 — ZKAC Post-Quantum Migration Plan.** *Acceptance:* `PQ_MIGRATION.md` for ZKAC. Extends Everest 96. *Effort:* L. *Prereq:* 96.

**Everest 299 — ZKAC Deprecation Policy.** *Acceptance:* When a v0 predicate or dimension is broken, retire-don't-renumber rules with migration windows. *Effort:* M. *Prereq:* 97, 117.

**Everest 300 — ZKAC Ecosystem Maturity.** *Acceptance:* ≥3 independent operators run ZKAC; ≥3 independent verifiers; ≥5 independent witnesses. *Effort:* L. *Prereq:* 295.

**Everest 301 — Reserved for Calm Audit.** *Acceptance:* When the action-history disclosure primitive (Calm Audit) reaches v0, it composes with ZKAC under this number. *Effort:* XL. *Prereq:* 286. *Note:* Placeholder for the third sister primitive of the Calm umbrella.

**Everest 302 — Reserved for Distinguishability Defense.** *Acceptance:* Per Everest 280, this is where the deepest defense against adversarial alignment fitting lands. Reserved for research outcomes. *Effort:* XL. *Prereq:* 280.

**Everest 303 — Reserved for Reputation-Free Operation.** *Acceptance:* A mode where the protocol functions WITHOUT reputation aggregation — only direct alignment + harm checks. Reserved for the case where reputation-graph effects become harmful. *Effort:* XL. *Prereq:* 211.

**Everest 304 — Reserved for Disability-First Default.** *Acceptance:* A mode where the v0 dimensions and predicates are reauthored from disability-justice principles as primary, not addendum. Reserved per Everest 88 / 292. *Effort:* XL. *Prereq:* 292.

**Everest 305 — Reserved for Long-Horizon Operation.** *Acceptance:* Documented behavior over 20+ year horizons; values-evolution patterns; intergenerational protocol continuity. *Effort:* XL. *Prereq:* 295, 300.

---

## Phase weights and ordering

| Phase | Summits | Cumulative | Theme |
|---|---|---|---|
| IX | 106–125 (20) | 20 | Values vocabulary |
| X | 126–145 (20) | 40 | Alignment computation |
| XI | 146–165 (20) | 60 | Harm-avoidance predicates |
| XII | 166–185 (20) | 80 | Cooperation & generosity |
| XIII | 186–200 (15) | 95 | Tribalism & out-group |
| XIV | 201–225 (25) | 120 | Trust & reputation |
| XV | 226–245 (20) | 140 | Selfishness ↔ altruism |
| XVI | 246–265 (20) | 160 | Multi-agent coalitions |
| XVII | 266–285 (20) | 180 | Adversarial & stress |
| XVIII | 286–305 (20) | 200 | Production, governance |

Total: 200 unclimbed summits, all clearly defined and ready to attack.

## Critical-path subset (the "minimum viable ZKAC")

If we could only bag 15 summits from Phase IX-XVIII to ship a useful ZKAC primitive, the right minimal set is:

**106, 107, 108, 122, 126, 128, 130, 139, 146, 147, 165, 172, 189, 213, 287.**

That gives us: values primitive + 10 dimensions + chain extension + ZK commitment + alignment metric + ZK comparison + threshold predicate + wire format + harm taxonomy + direct-harm absence + harm aggregate + cross-difference cooperation + cross-difference respect + trust threshold + reference implementation.

The other 185 are sharpening, hardening, ethics-checking, and scaling that minimum into a real standard.

---

## What this document is NOT

- Not a moral framework. The protocol cannot tell anyone how to live.
- Not a credit score for humanity. Disclosure is always principal-authorized and class-bounded.
- Not a tool for ranking people. Predicates return a single bit per consent grant; aggregation across principals is structurally refused by the disclosure layer.
- Not a substitute for human judgment. Counterparties act on the bit; they remain responsible for what they do with it.

These four boundaries are load-bearing. If the protocol grows in a direction that violates them, that direction is a fork, not a v-bump.

---

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**
**Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` immediately after commit. The route is real.**
