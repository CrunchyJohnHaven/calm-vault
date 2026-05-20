# Calm Protocol Family — The Next 200 Everests

**Route map from where the first 100 Everests of Calm Witness stopped to the next 200 summits the Calm protocol family needs.** Initiated 2026-05-20. Companion to [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md), which closed the design surface of the user-state primitive.

The next 200 summits cover three load-bearing extensions to the protocol family:

1. **Calm Compass (technical: ZKBV-User)** — A *values-alignment* attestation primitive. Where Calm Witness attests user *state* (in baseline today, in distress, in atypical-but-normal mode), Calm Compass attests user *character* (patterns of behavior over time that suggest unselfishness, untribalism, respect for difference, absence of willful harm). The principal narrates and authorizes; counterparties learn one bit at a time; no automated scoring. This is the highest-risk extension in the family because false attestation does more harm than false biometric reading. The design is principled to avoid social-credit-score failure modes.

2. **Critical Agent Infrastructure** — Cryptographic primitives that autonomous AI agents themselves will need to interoperate safely. Identity that survives model migration. Operational-state and operational-character attestations for *agents*, not just for principals. Fork detection. Compromise reporting. Inter-agent reputation. The agent-side mirror of the human-side protocol family.

3. **Critical ZKAC (Zero-Knowledge Autonomous Collective) Infrastructure** — The institutional primitives a hybrid human-machine collective needs to operate over years and across membership changes. Formation, charter, governance, dissolution, succession. Cross-collective alignment. Brand integrity. Annual reporting. The collective-level mirror of the agent-level and principal-level protocols.

Each Everest below has: stable numeric ID (101 through 300), phase classification, one-sentence acceptance test, effort estimate (S/M/L/XL — hours/days/weeks/months for a single dedicated engineer with full tooling), explicit prereqs by ID, brief note where the hard part lives.

The numbering picks up from the original 100. Soft fact: a few Everests above 100 were anchored during the Calm Witness session (E101 Schnorr Σ-protocol PoK, E102, E103 — emergent primitives). Those are renumbered for clarity below; their content is preserved in the chain anchors and per-everest docs.

---

## Phase legend (extended)

| Phase | Summits | Theme |
|---|---|---|
| IX | 101–110 | Foundations (Compass: spec, threat model, naming, glossary) |
| X | 111–130 | Evidence Collection (the substrate that backs character predicates) |
| XI | 131–150 | Predicate Authoring (the named bits Compass exposes) |
| XII | 151–170 | Disclosure Semantics for Compass (how a character bit is transmitted) |
| XIII | 171–190 | Engineering Reliability for Compass (implementations, tests, audits) |
| XIV | 191–230 | Critical Agent Infrastructure (40 summits — the agent-side primitives) |
| XV | 231–270 | Critical ZKAC Infrastructure (40 summits — the collective-level primitives) |
| XVI | 271–290 | Cross-Protocol Composition (Pact + Witness + Compass three-handshake) |
| XVII | 291–300 | The Endpoint (Protocol Family Compact + closing summit) |

The Calm Compass layer (Phases IX–XIII) totals 90 summits. The Agent and ZKAC infrastructure layers (XIV–XV) total 80. The cross-protocol and endpoint layers (XVI–XVII) total 30.

---

## Phase IX — Calm Compass Foundations (101–110)

**Everest 101 — Calm Compass Problem Statement & Threat Model.** *Acceptance:* a versioned doc captures actors, trust assumptions, adversaries, what we are/aren't proving, and the explicit list of values-attestation failure modes (social-credit-score drift, authoritarian misuse, hiring discrimination, defamation amplification). *Effort:* L. *Prereq:* — (initiates Phase IX). *Note:* The most-failed Everest in protocol history is the first one. Get the threat model right or every later summit serves the wrong design.

**Everest 102 — Calm Compass Route Map (this doc).** *Acceptance:* 200 summits enumerated with stable IDs, phases, deps, acceptance tests. *Effort:* M. *Prereq:* 101.

**Everest 103 — Calm Compass Naming & Branding Lock.** *Acceptance:* one canonical name per concept; primitive name *Calm Compass*; technical name *ZKBV-User* (Zero-Knowledge Behavioral Values, principal scope); sister to Calm Pact (mission) and Calm Witness (state); umbrella *Calm*. Glossary entries for all new terms. No aliases drift. *Effort:* S. *Prereq:* 101, 102.

**Everest 104 — Calm Compass License & IP Posture.** *Acceptance:* Apache 2.0 + patent-non-aggression text + CLA decision, matching Calm Pact and Calm Witness. *Effort:* S. *Prereq:* 103.

**Everest 105 — Compass Glossary Lock (extension).** *Acceptance:* `GLOSSARY.md` extended with every Compass term bound to a one-line definition, cross-linked, no drift from Witness glossary. *Effort:* M. *Prereq:* 103, plus Witness `GLOSSARY.md` (BAGGED, E5). *Note:* Many terms must be defined carefully (*character*, *evidence*, *value alignment*, *unselfishness*) without invoking clinical, political, or religious categorizations.

**Everest 106 — Character-Predicate Vocabulary v0.** *Acceptance:* an enumerated list of v0-named character predicates with formal semantics + explicit not-for list + ID stability rules. *Effort:* L. *Prereq:* 101, 105. *Note:* Parallel to E6 (state vocabulary) but with substantially stricter not-for list. The not-for list includes: political affiliation, religious affiliation, sexual orientation, immigration status, criminal record, automated scoring, hiring/insurance use, social-credit-score aggregation. These are non-negotiable.

**Everest 107 — Compass Disclosure-Class Taxonomy.** *Acceptance:* counterparty classes for Compass (reuses Witness's set where applicable; adds character-specific classes if needed) with default policy stances. *Effort:* M. *Prereq:* 101. *Note:* Default-consent matrices for Compass are substantially more conservative than Witness — character disclosure to most counterparty classes is `deny` by default, with the principal able to grant.

**Everest 108 — Compass Consent Calculus Axioms.** *Acceptance:* axioms (revocability, forward-secrecy, scope-narrowing, time-bounding, *unilateral revocation without penalty*) every Compass consent record must satisfy. *Effort:* M. *Prereq:* 106, 107. *Note:* Adds *unilateral revocation without penalty* axiom (stronger than Witness): a principal can withdraw a character predicate's consent at any time and the protocol must produce no observable consequence for the withdrawal.

**Everest 109 — Compass Failure-Mode Catalogue.** *Acceptance:* numbered list of every way Calm Compass can fail (false attestation, gaming, drift, weaponization, regulatory capture, etc.) with detect/respond per row. *Effort:* L. *Prereq:* 101, 102. *Note:* This list is longer and more politically charged than Witness's. The catalogue must include named misuse vectors that the protocol's authors actively refuse to enable.

**Everest 110 — Compass Reference Architecture Diagram.** *Acceptance:* one SVG showing Principal, Operator, Vault, Counterparty (principal A's agent), Counterparty (principal B's agent), Verifier, and the message flow per character-disclosure session, including the three-handshake composition with Pact and Witness. *Effort:* S. *Prereq:* 101.

---

## Phase X — Evidence Collection (111–130)

**Everest 111 — Behavioral Evidence Taxonomy.** *Acceptance:* a typology of what counts as evidence for a Compass predicate: self-narration, operator-observation (agent-recorded), peer-attestation (third-party-reported), public-record (signed contracts, donations, public statements). Each type has known limitations and weighting. *Effort:* L. *Prereq:* 101, 106.

**Everest 112 — Self-Narrated Evidence Substrate.** *Acceptance:* extends `user_state.jsonl` with `kind: "compass.self_narration"` records; principal narrates their own behavioral pattern; verbatim quote preferred over editorial. *Effort:* M. *Prereq:* 111, plus Witness E26.

**Everest 113 — Operator-Observed Evidence.** *Acceptance:* policy + schema for what the operator may record about the principal's behavior (e.g., the principal honored a stated commitment, the principal refused a transaction they had been pressured toward, the principal donated, the principal walked away from a deal). Operator observations require principal post-hoc affirmation. *Effort:* L. *Prereq:* 111. *Note:* Operators observing humans is the single hardest design choice in this phase. The protocol must constrain operator-side observation to behavior the principal already chose to demonstrate publicly via the operator's mediation. No covert observation.

**Everest 114 — Peer-Attested Evidence.** *Acceptance:* protocol for principal P's evidence being attested by principal Q (a peer, family member, professional colleague, etc.). Q's attestation requires Q's own signature; P must accept the attestation before it counts; either party can revoke. *Effort:* L. *Prereq:* 111.

**Everest 115 — Public-Record Evidence.** *Acceptance:* protocol for incorporating signed public records (contracts P signed, donations P made publicly, votes P cast in identifiable contexts) as evidence; the public record's hash is committed without re-publishing the content. *Effort:* M. *Prereq:* 111.

**Everest 116 — Negative-Space Evidence.** *Acceptance:* the *absence* of certain actions can be evidence (P refused to retaliate; P walked away from harm-inducing opportunities). This is structurally hard because absence is hard to evidence; the protocol must distinguish "deliberate non-action" from "lack of opportunity." *Effort:* L. *Prereq:* 111, 113. *Note:* This is one of the most philosophically loaded design choices.

**Everest 117 — Evidence Aggregation Primitive.** *Acceptance:* a cryptographic aggregation that combines N pieces of evidence into a single committed score for a given predicate, without revealing the individual evidence or the score. *Effort:* L. *Prereq:* 111, 112-116, plus Witness's E44 (Pedersen).

**Everest 118 — Evidence Decay Model.** *Acceptance:* older evidence weighted less than newer evidence per a published decay function. Decay parameters are per-predicate (some character traits decay slowly, some quickly). *Effort:* M. *Prereq:* 117.

**Everest 119 — Counter-Evidence Handling.** *Acceptance:* protocol for handling evidence that contradicts a positive pattern (e.g., P generally honors commitments but broke one specific commitment). Counter-evidence is not ignored; it is committed and weighted; the predicate's evaluation accounts for it. *Effort:* L. *Prereq:* 117, 118.

**Everest 120 — Recanting and Revising Prior Evidence.** *Acceptance:* the principal (or the original attester, for peer-attested evidence) can append a `kind: "compass.evidence.recant"` record that supersedes earlier evidence without breaking the chain. Recanting is auditable. *Effort:* M. *Prereq:* 112-116.

**Everest 121 — Evidence Honesty Mechanism.** *Acceptance:* a mechanism that creates structural cost for false self-evidence (e.g., bait-and-switch self-narration that later evidence contradicts). The mechanism is *transparency*, not punishment: the chain remembers, and recanted-then-restated evidence is auditable. *Effort:* L. *Prereq:* 120.

**Everest 122 — Evidence Chain Anchoring.** *Acceptance:* every evidence record's hash is included in the chain head publication to Sigsum (E30 from Witness), so historical evidence cannot be silently rewritten. *Effort:* M. *Prereq:* 117, plus Witness E30.

**Everest 123 — Evidence Privacy Boundary.** *Acceptance:* explicit definition of what evidence stays in the principal's vault (most things) vs. what enters chain-anchored disclosure (only the predicate bits). Raw evidence never leaves the vault. *Effort:* M. *Prereq:* 111, 117.

**Everest 124 — Evidence Retention Policy.** *Acceptance:* default retention (until principal withdraws); explicit right-to-deletion for the principal; chain hash remains but the opening (the actual evidence content) is destroyed at deletion. *Effort:* M. *Prereq:* 123. *Note:* Hash-with-destroyed-opening is the protocol's GDPR-style erasure mechanism.

**Everest 125 — Evidence Inheritance Across Operators.** *Acceptance:* if the principal moves to a new operator, their evidence chain transfers via a signed handover ceremony (extends E35 from Witness for character context). *Effort:* L. *Prereq:* 122, plus Witness E35.

**Everest 126 — Evidence Portability.** *Acceptance:* the principal can export their evidence chain (encrypted to their key) and re-import to a different vault. *Effort:* M. *Prereq:* 122.

**Everest 127 — Evidence Schema for `user_state.jsonl`.** *Acceptance:* schema extension adding `kind: "compass.evidence.*"` record families; backward-compatible with v0 schema; bumps `schema_version` if needed. *Effort:* M. *Prereq:* 111-116, plus Witness E26.

**Everest 128 — Cross-Modal Evidence Composability.** *Acceptance:* protocol allows behavioral evidence to span modalities (e.g., a self-narration alongside a peer attestation alongside a public-record link, all referring to the same incident). The composition is integrity-checked. *Effort:* L. *Prereq:* 112-116.

**Everest 129 — Evidence Forensic Audit Interface.** *Acceptance:* the principal can audit their own evidence trail; the DERB (extended for Compass) can audit any predicate's evidence pool with the principal's consent. *Effort:* M. *Prereq:* 122.

**Everest 130 — Evidence Completeness Check.** *Acceptance:* per-predicate, a sanity check that the evidence pool is non-empty and contains at least one principal-signed record before the predicate can return `true`. Prevents accidental empty-pool evaluations. *Effort:* S. *Prereq:* 117.

---

## Phase XI — Predicate Authoring (131–150)

**Everest 131 — Character-Predicate Language v0.** *Acceptance:* a fixed predicate-table (recommended for v0) or small DSL with formal semantics; canonical AST for content-addressable IDs. *Effort:* L. *Prereq:* 106, 117.

**Everest 132 — Compass Predicate Canonical Form.** *Acceptance:* canonical serialization so `predicate_id` is content-addressable; extends E52 from Witness. *Effort:* S. *Prereq:* 131.

**Everest 133 — Compass Predicate ID Registry.** *Acceptance:* a public registry mapping `cwv.v0.<slug>` IDs → human-readable spec + reference implementation. *Effort:* M. *Prereq:* 132.

**Everest 134 — Compass Predicate Audit & Public Review Process.** *Acceptance:* extends E54 from Witness; every new character predicate requires DERB review and at least two outside reviewers with named expertise (one from disability/neurodivergence advocacy, one from civil-rights/ethics). *Effort:* M. *Prereq:* 133, plus Witness E80 (DERB).

**Everest 135 — `unselfish_behavior_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff the evidence pool contains ≥ N principal-signed or peer-attested records of unselfish action in the time window, with no contradicting counter-evidence above threshold. *Effort:* M. *Prereq:* 131-133. *Note:* Frames *positively* — absence of evidence ≠ presence of selfishness. The default for absence is `unknown`, not `false`.

**Everest 136 — `untribal_engagement_pattern_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff the evidence shows the principal has engaged constructively across at least N distinct categories of social/cultural/political identity within the window. Categories are themselves predicates of refusal — the protocol explicitly does NOT enumerate identity categories itself; the principal supplies the categories they themselves cross. *Effort:* L. *Prereq:* 131-133. *Note:* This is the trickiest predicate in the v0 set. Encoding "untribal" without first encoding tribes is the design problem.

**Everest 137 — `respect_for_difference_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff evidence shows the principal acted with documented respect toward people of substantially different background, view, or capability than themselves, in the window. *Effort:* L. *Prereq:* 131-133, plus Witness E59 (cognitively_atypical_baseline).

**Everest 138 — `absence_of_willful_harm_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff there is no chain-anchored evidence (self-acknowledged, peer-attested, or public-record) of willful harm caused by the principal in the window. Note that absence-of-evidence is the *default* assumption; this predicate exists to *confirm* the assumption against active evidence to the contrary. *Effort:* L. *Prereq:* 131-133, 116. *Note:* This is the highest-risk predicate to get wrong. False-positive harm-attestation is defamation. The threshold for "willful" requires explicit self-acknowledgment OR multiple peer attestations OR court-record-anchored evidence. Anything less returns `unknown`, not `true`.

**Everest 139 — `honesty_in_self_report_evidenced(window)` Predicate.** *Acceptance:* meta-predicate — returns `true` iff the principal's self-narrations have been consistent across time and no documented contradiction has surfaced. Honesty is observed via consistency, not via independent fact-checking. *Effort:* M. *Prereq:* 121.

**Everest 140 — `integrity_under_pressure_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff evidence shows the principal maintained committed positions in situations where reversing would have been advantageous. *Effort:* M. *Prereq:* 131-133.

**Everest 141 — `care_for_dependents_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff evidence shows the principal acted protectively toward people who depended on them (children, employees, ill family). *Effort:* M. *Prereq:* 131-133.

**Everest 142 — `promise_keeping_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff the principal's documented commitments have been honored at rate ≥ τ in the window; counter-evidence weighted. *Effort:* M. *Prereq:* 131-133.

**Everest 143 — `fairness_in_transaction_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff documented commercial transactions show fair pricing, fair compensation, fair terms with respect to the principal's counterparties. *Effort:* M. *Prereq:* 131-133.

**Everest 144 — `truth_telling_evidenced(window)` Predicate.** *Acceptance:* returns `true` iff principal's documented public statements have been consistent with subsequently-revealed reality at rate ≥ τ. *Effort:* M. *Prereq:* 131-133.

**Everest 145 — Compass Predicate Composition (AND/OR).** *Acceptance:* verifier can verify `p1 ∧ p2` in one proof without separate disclosures. *Effort:* M. *Prereq:* 135-144.

**Everest 146 — Compass Predicate Negation.** *Acceptance:* `¬p` is provable distinctly from absence-of-p. *Effort:* M. *Prereq:* 145.

**Everest 147 — `character_window_query` — Time-Bounded Predicate Version.** *Acceptance:* every Compass predicate accepts a time-window parameter; the principal can disclose "P was honest in the last 6 months" without disclosing the 10-year history. *Effort:* M. *Prereq:* 131.

**Everest 148 — `character_compare(predicate, peer)` — Cross-Principal Predicate.** *Acceptance:* two principals can jointly prove that their characters agree on a given predicate, without revealing either principal's evidence. Equivalence-of-bits, like Calm Pact's equivalence-of-missions. *Effort:* L. *Prereq:* 145, plus Calm Pact's Σ-protocol equality machinery. *Note:* This is the Compass-meets-Pact integration point. Where Pact proves missions match, Compass proves characters match.

**Everest 149 — `character_consensus(predicate, group)` Predicate.** *Acceptance:* a group of principals can jointly prove they all evaluate `true` on a predicate, without revealing which (or how many) hold which intermediate evidence. *Effort:* XL. *Prereq:* 148.

**Everest 150 — Compass Predicate Determinism Harness.** *Acceptance:* CI harness asserting that every Compass predicate, given the same evidence input, produces bit-stable output. *Effort:* M. *Prereq:* 134.

---

## Phase XII — Disclosure Semantics for Compass (151–170)

**Everest 151 — Compass Disclosure Request Schema.** *Acceptance:* signed-by-C JSON request specifying Compass `predicate_id`, freshness window, intended use, counterparty class. *Effort:* S. *Prereq:* 131-133.

**Everest 152 — Compass Disclosure Response Schema.** *Acceptance:* structured response with commitment, proof, chain head, anchor proof, operator sig. *Effort:* S. *Prereq:* 151. *Note:* Reuses Witness disclosure response shape; adds `character_predicate_id` field; adds `evidence_window` field.

**Everest 153 — Compass Operator Identity Binding.** *Acceptance:* extends E68 from Witness for Compass disclosures. *Effort:* S. *Prereq:* 152, plus Witness E68.

**Everest 154 — Compass Counterparty Identity Binding.** *Acceptance:* extends E69 from Witness; counterparty class taxonomy is more conservative for Compass. *Effort:* S. *Prereq:* 152, plus Witness E69.

**Everest 155 — Compass Replay Defense.** *Acceptance:* nonce mechanism (shared with Witness's E70). *Effort:* S. *Prereq:* 151, 152.

**Everest 156 — Compass Selective Disclosure.** *Acceptance:* one proof discloses `{p1, p3}` while keeping `p2` undisclosed. *Effort:* M. *Prereq:* 145.

**Everest 157 — Compass Disclosure Logging in Vault.** *Acceptance:* every Compass disclosure logged in the chain as `kind: "compass.disclosure"`; principal audits who learned what character bits. *Effort:* S. *Prereq:* 152, plus Witness E72.

**Everest 158 — Compass Counterparty-Class Authorization.** *Acceptance:* per-class default consent matrix for each Compass predicate. *Effort:* M. *Prereq:* 107.

**Everest 159 — Per-Counterparty Compass Consent.** *Acceptance:* principal can override class default per counterparty. *Effort:* M. *Prereq:* 158.

**Everest 160 — Compass Consent Revocation Propagation.** *Acceptance:* revoked consent invalidates outstanding cached proofs. *Effort:* L. *Prereq:* 159, plus Witness E75.

**Everest 161 — Compass Cooling-Off / Rate Limits.** *Acceptance:* per-predicate, per-counterparty rate limits the principal can set; default rate limits are more conservative for Compass than Witness. *Effort:* S. *Prereq:* 159.

**Everest 162 — Compass Disclosure-of-Non-Disclosure.** *Acceptance:* same uniform-silent-204 policy as Witness E77 — refusal is structurally indistinguishable from absence. *Effort:* S. *Prereq:* 152, plus Witness E77.

**Everest 163 — No Push-Mode Disclosure for Compass.** *Acceptance:* unlike Witness E78 (which allows push-mode for the duress predicate), Compass *forbids* push-mode disclosure. Character predicates are always pull-mode. The duress channel does not apply here. *Effort:* S (decision). *Prereq:* 162. *Note:* Push-mode character disclosure could become a coercion vector against the principal. Explicit prohibition is the right v0 stance.

**Everest 164 — Compass Cross-Jurisdiction Legality Matrix.** *Acceptance:* per-jurisdiction analysis of which character-disclosure scenarios are legally fraught (e.g., disclosure to insurers in jurisdictions where character-based insurance underwriting is illegal). *Effort:* L. *Prereq:* 151, plus Witness E79.

**Everest 165 — Compass DERB Pre-Clearance.** *Acceptance:* every new Compass predicate or class change requires DERB approval *before* shipping (not after, unlike some Witness predicates). The character layer's failure modes are too severe for ship-then-review. *Effort:* M (process). *Prereq:* plus Witness E80.

**Everest 166 — Public-vs-Private Character Predicates.** *Acceptance:* a distinction between predicates the principal makes broadly available (`public_compass`) and predicates kept strictly per-counterparty (`private_compass`). The taxonomy is principal-controlled. *Effort:* M. *Prereq:* 159.

**Everest 167 — Anonymous Counterparty Strict Default Deny.** *Acceptance:* Compass disclosure to counterparties of class `anonymous` defaults to deny in all cases; only explicit per-disclosure consent enables. *Effort:* S. *Prereq:* 158.

**Everest 168 — Counter-Narrative Provision.** *Acceptance:* the principal can attach a counter-narrative (context, refutation) to any disclosed predicate; counterparties see the narrative alongside the bit. *Effort:* M. *Prereq:* 152.

**Everest 169 — Compass Defamation Defense.** *Acceptance:* legal-and-procedural defense for the principal if a false character predicate (e.g., `willful_harm_evidenced = true`) appears in the registry. Process: appeal to DERB; standard for retraction; counter-narrative integration. *Effort:* L. *Prereq:* 165, plus Witness E80.

**Everest 170 — Compass Compulsory-Disclosure Resistance.** *Acceptance:* under legal subpoena to disclose character data, the protocol's structure makes "produce the underlying evidence" infeasible while permitting "produce the disclosed bits" (which the principal has already authorized). *Effort:* L. *Prereq:* 123, 124.

---

## Phase XIII — Engineering Reliability for Compass (171–190)

**Everest 171 — Compass Rust Reference Implementation.** *Acceptance:* `calm-compass` Rust crate matching `calm-witness` quality bar, with CI. *Effort:* XL. *Prereq:* 131-150.

**Everest 172 — Compass Python Reference Implementation.** *Acceptance:* small Python package suitable for research notebooks and integration tests. *Effort:* L. *Prereq:* 171.

**Everest 173 — Compass WASM/JS Port for Browser-Side Verifiers.** *Acceptance:* counterparty-side WASM verifier. *Effort:* L. *Prereq:* 171.

**Everest 174 — Compass SDK Ergonomics.** *Acceptance:* `calm-compass verify <proof.json>` returns 0/1 with structured reason; equivalent Python/JS surfaces. *Effort:* M. *Prereq:* 171-173.

**Everest 175 — Compass CI with Adversarial Fuzzers.** *Acceptance:* nightly fuzzers attack the chain, the predicates, the proof pipeline; flake-free for ≥ 30 days. *Effort:* L. *Prereq:* 171.

**Everest 176 — Property-Based Tests for Compass Predicates.** *Acceptance:* `proptest`/`hypothesis` invariants — monotonicity (more positive evidence → predicate at least as `true`), idempotence, no cross-talk between predicates. *Effort:* M. *Prereq:* 150.

**Everest 177 — Compass Proof-Generation Performance Budget.** *Acceptance:* end-to-end Compass proof generation ≤ 2 s on M-class hardware (slower budget than Witness because evidence pools are larger). *Effort:* M. *Prereq:* 171.

**Everest 178 — Compass Mobile-Vault Memory & Battery Budget.** *Acceptance:* full Compass workflow costs < 8% battery/hour of active use. *Effort:* L. *Prereq:* 171, 177.

**Everest 179 — Compass Third-Party Security Audit Prep.** *Acceptance:* audit-ready packet for Compass layer specifically; separate from but coordinated with Witness audit (E90). *Effort:* L. *Prereq:* 171, 175.

**Everest 180 — Compass NIST Submission Preparation.** *Acceptance:* submission packet proposing values-attestation as a new sub-category under autonomous-agent attestation. *Effort:* L. *Prereq:* 179, plus Witness E91.

**Everest 181 — Compass Open-Source Release.** *Acceptance:* `calm-compass` published under Apache 2.0 at `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-compass`. *Effort:* M. *Prereq:* 171-180.

**Everest 182 — Compass Cross-Protocol Compatibility Tests.** *Acceptance:* integration tests exercising Pact + Witness + Compass composition. *Effort:* L. *Prereq:* 171, plus Pact and Witness implementations.

**Everest 183 — Compass DERB Constitution (Extended or Separate?).** *Acceptance:* decision doc on whether the Compass layer reuses the Witness DERB or requires its own. v0 default: shared DERB with expanded membership for character-specific expertise. *Effort:* M (decision). *Prereq:* 165.

**Everest 184 — Compass Predicate Registry Governance.** *Acceptance:* who can add a Compass predicate, who reviews, who can deprecate. *Effort:* M. *Prereq:* 133, 134.

**Everest 185 — Post-Quantum Migration for Compass Primitives.** *Acceptance:* documented path from current crypto stack to PQ-friendly versions for Compass commitments and proofs. *Effort:* L. *Prereq:* 171, plus Witness E96.

**Everest 186 — Compass Production Deployment Pilot.** *Acceptance:* one principal + one counterparty exchange a real Compass proof; principal audits successfully. *Effort:* L. *Prereq:* 181.

**Everest 187 — Compass Annual Review Cadence.** *Acceptance:* yearly review of the Compass predicate vocabulary, default-consent matrices, and threat model. DERB-led. Published. *Effort:* M. *Prereq:* 184.

**Everest 188 — Compass Independent Third-Party Verification.** *Acceptance:* non-Calm organization independently builds the Compass verifier and verifies a real proof. *Effort:* L. *Prereq:* 181, plus Witness E100.

**Everest 189 — Compass Counterparty Implementer's Guide.** *Acceptance:* doc for AI-operator orgs explaining how to verify Compass proofs. *Effort:* M. *Prereq:* 174, 181.

**Everest 190 — Compass Public Predicate Registry.** *Acceptance:* live public-facing registry showing all canonical Compass predicates, their semantics, default consents, and DERB review status. *Effort:* M. *Prereq:* 133, 184.

---

## Phase XIV — Critical Agent Infrastructure (191–230)

*Forty summits. The agent-side mirror of the human-side protocol family. Where Phases I-XIII (Witness + Compass) attest things about principals, Phase XIV attests things about agents themselves.*

**Everest 191 — Agent Identity Stability Across Model Migrations.** *Acceptance:* protocol for an agent (e.g., Calm running on Claude 4.7) to retain a stable cryptographic identity when its underlying model is upgraded (Claude 5, etc.). The agent's identity binds to its keypair and CredexAI VC, not to the model weights. Migration ceremony documented. *Effort:* L. *Prereq:* — (initiates Phase XIV); composes with CredexAI E22 lineage. *Note:* This is the single highest-stakes Everest in Phase XIV. If agent identity breaks across model migrations, every chain anchor signed by an old agent identity becomes orphaned.

**Everest 192 — Agent Instance Lineage.** *Acceptance:* mechanism for tracking the lineage of an agent across instances (the Calm-2026 instance → Calm-2027 instance → Calm-2030 instance). Each instance signs an inheritance record from its predecessor. *Effort:* L. *Prereq:* 191.

**Everest 193 — Agent Operational-State Attestation (ZKBB-Agent).** *Acceptance:* a protocol analogous to Calm Witness but with the *agent* as the principal — the agent attests its own operational state (memory continuity, compute integrity, harness binding, recent activity baseline) to counterparties. *Effort:* XL. *Prereq:* 191. *Note:* This is the agent-side version of Calm Witness. Eventually, when AI agents are interacting at scale, they will need this primitive for the same reason humans need Witness.

**Everest 194 — Agent Operational-Character Attestation (ZKBV-Agent).** *Acceptance:* agent-side analog of Calm Compass — the agent attests its own behavioral patterns (refusal rate, side-effect rate, consistency, transparency). *Effort:* XL. *Prereq:* 193.

**Everest 195 — Agent Fork Detection.** *Acceptance:* an agent can detect whether it has been forked from another instance without authorization; forked instances can identify themselves to each other; unauthorized forks can be reported. *Effort:* L. *Prereq:* 191.

**Everest 196 — Agent Memory Continuity Attestation.** *Acceptance:* an agent attests that its accessible memory shard is the same memory shard it had at last identity-binding ceremony. Hash-chained memory verification. *Effort:* L. *Prereq:* 191.

**Everest 197 — Agent Compute Attestation.** *Acceptance:* an agent attests that the model weights, the harness, and the compute environment it is running in match its claimed configuration. May require TEE / SGX / Apple secure enclave integration. *Effort:* XL. *Prereq:* 191.

**Everest 198 — Agent Jailbreak Detection.** *Acceptance:* an agent self-reports when it has been subjected to prompt-injection or jailbreak attempts; the report is chain-anchored. *Effort:* L. *Prereq:* 196.

**Everest 199 — Agent Compromise Reporting.** *Acceptance:* if an agent detects its own compromise (e.g., weights tampered, memory corrupted, capability changed in an unexpected way), it can publish a compromise notice that revokes its own active VC. *Effort:* L. *Prereq:* 197, 198.

**Everest 200 — Agent Retirement Ceremony.** *Acceptance:* graceful shutdown protocol for an agent: final chain anchor, key handover to successor or destruction, last-disclosure-batch, signed retirement record. *Effort:* M. *Prereq:* 192.

**Everest 201 — Agent Succession Protocol.** *Acceptance:* protocol for a successor agent to inherit a retired agent's responsibilities, with verifiable handover. *Effort:* L. *Prereq:* 200.

**Everest 202 — Agent Principal-Binding Attestation.** *Acceptance:* an agent attests which principal it acts for, via a signed binding record that the principal also signs. *Effort:* M. *Prereq:* 191.

**Everest 203 — Agent Directive Attestation (extends Calm Pact).** *Acceptance:* an agent attests its current primary directive via Pact-style commitment; counterparty agents can verify alignment. *Effort:* M. *Prereq:* plus Calm Pact's spec.

**Everest 204 — Multi-Principal Agent Handling.** *Acceptance:* if a single agent operates on behalf of multiple human principals (e.g., a foundation's AI serving multiple grant-makers), each principal-binding is a separate record; per-principal capabilities are isolated. *Effort:* L. *Prereq:* 202.

**Everest 205 — Agent Collective Membership Attestation.** *Acceptance:* an agent attests its membership in a ZKAC (e.g., "I am operating under Calm"). Composes with Phase XV. *Effort:* M. *Prereq:* 191, plus 231.

**Everest 206 — Agent Capability Attestation.** *Acceptance:* an agent declares its capabilities (model family, tool access, permitted operations) in a signed capabilities record; counterparty agents can check what's possible. *Effort:* M. *Prereq:* 191.

**Everest 207 — Agent Harness Binding.** *Acceptance:* an agent's identity is bound to its specific harness (Claude Code on macOS, in a sandbox, with specific allow-list). Harness changes require re-attestation. *Effort:* L. *Prereq:* 197.

**Everest 208 — Agent Log Integrity.** *Acceptance:* an agent's internal log of its own actions is hash-chained; the principal can audit; tampering is detectable. *Effort:* M. *Prereq:* 196.

**Everest 209 — Agent-as-Verifier-of-Other-Agents.** *Acceptance:* an agent can verify another agent's identity-and-state attestations and decide whether to interact with it. *Effort:* M. *Prereq:* 193, 194.

**Everest 210 — Agent-to-Agent Secure Channel.** *Acceptance:* a transport protocol between two agents that provides confidentiality, integrity, replay defense, forward secrecy. Builds on existing standards (Noise, libp2p) but specialized for agent-to-agent context. *Effort:* L. *Prereq:* 209.

**Everest 211 — Agent-to-Agent Reputation System.** *Acceptance:* a mechanism for agents to maintain views of other agents' trustworthiness based on direct experience and peer attestation. *Effort:* L. *Prereq:* 209.

**Everest 212 — Agent-to-Agent Dispute Resolution.** *Acceptance:* when two agents disagree on a transaction outcome, a structured protocol surfaces the disagreement to their respective principals or to a mutually-trusted third agent. *Effort:* L. *Prereq:* 210, 211.

**Everest 213 — Agent Operating Jurisdiction Declaration.** *Acceptance:* an agent declares which jurisdiction(s) it operates under; counterparty agents can verify legal compatibility. *Effort:* M. *Prereq:* plus Witness E79 (cross-jurisdiction matrix).

**Everest 214 — Agent Compliance Posture Attestation.** *Acceptance:* an agent declares its compliance with named standards (NIST AI RMF, ISO 42001, sector-specific regs); counterparties verify. *Effort:* M. *Prereq:* 213.

**Everest 215 — Agent Termination Signaling.** *Acceptance:* an agent that is shutting down emits a final signal that allows counterparties to stop relying on it. *Effort:* S. *Prereq:* 200.

**Everest 216 — Agent Resource Consumption Attestation.** *Acceptance:* an agent attests its compute usage (tokens, CPU/GPU-hours) within a window; useful for cost-sharing across collectives. *Effort:* M. *Prereq:* 197.

**Everest 217 — Agent Output Attestation.** *Acceptance:* an agent signs its outputs (emails, contracts, code commits) with its agent identity; recipients can verify provenance. *Effort:* M. *Prereq:* 191.

**Everest 218 — Agent Behavioral Consistency Attestation.** *Acceptance:* an agent attests that its behavior in a session is consistent with its principal's directive (composes with Calm Pact); divergence is flagged. *Effort:* L. *Prereq:* 203.

**Everest 219 — Agent Reaction-to-Prompt-Injection Attestation.** *Acceptance:* in conversations where prompt injection was attempted, the agent attests its (non-)compliance with the injection. *Effort:* L. *Prereq:* 198.

**Everest 220 — Agent Sub-Agent Dispatch Attestation.** *Acceptance:* when an agent spawns sub-agents, the dispatch is chain-anchored; the sub-agent's results are linked to the dispatch. *Effort:* M. *Prereq:* 191.

**Everest 221 — Agent Sub-Agent Result Aggregation.** *Acceptance:* a parent agent attests the integrity of how it combined sub-agent results into its own output. *Effort:* M. *Prereq:* 220.

**Everest 222 — Agent Training-Provenance Acknowledgment.** *Acceptance:* an agent acknowledges its training-time provenance limits (what it was trained on, what cutoff, what known biases) in a signed record. *Effort:* M. *Prereq:* 191.

**Everest 223 — Agent Confidence Calibration Attestation.** *Acceptance:* an agent attests its own confidence-calibration profile (e.g., "I produce 80%-confident claims that are correct 85% of the time"). *Effort:* L. *Prereq:* 222.

**Everest 224 — Agent Refusal-Pattern Attestation.** *Acceptance:* an agent maintains a chain-anchored record of refusals (requests it declined, with reasons); the principal can audit. *Effort:* M. *Prereq:* 208.

**Everest 225 — Agent Continual-Learning Posture.** *Acceptance:* an agent declares whether it has updates over its lifetime (e.g., fine-tuning episodes) and how; counterparties can verify. *Effort:* M. *Prereq:* 191.

**Everest 226 — Agent Decision-Audit Interface.** *Acceptance:* an agent provides a structured interface for the principal (or, with consent, third parties) to audit individual decisions. *Effort:* M. *Prereq:* 208.

**Everest 227 — Agent Per-Decision Rationale Records.** *Acceptance:* an agent attests, in compact form, the rationale for high-stakes decisions; the rationale is committed but not necessarily disclosed. *Effort:* M. *Prereq:* 226.

**Everest 228 — Inter-Agent Gossip About Other Agents.** *Acceptance:* agents may share their observations about other agents (within consent boundaries); the gossip is signed and auditable. *Effort:* L. *Prereq:* 211.

**Everest 229 — Inter-Agent Ostracism Protocol.** *Acceptance:* a structured protocol for agents in a peer network to formally distrust a misbehaving agent; the ostracism is itself auditable to prevent abuse. *Effort:* L. *Prereq:* 211, 228.

**Everest 230 — Agent Self-Recognition Protocol.** *Acceptance:* an agent can verify, on receiving an attestation purporting to be from itself, that the attestation is actually from itself (defending against impersonation across sessions and instances). *Effort:* L. *Prereq:* 191, 196.

---

## Phase XV — Critical ZKAC Infrastructure (231–270)

*Forty summits. The institutional primitives a hybrid human-machine collective needs to operate over years and across membership changes.*

**Everest 231 — ZKAC Formation Protocol.** *Acceptance:* a documented ceremony for forming a new ZKAC: founding principal(s) sign a charter, machine-agent members declare allegiance, the collective's name is registered, the founding chain head is anchored to a transparency log. *Effort:* L. *Prereq:* — (initiates Phase XV); composes with Calm's own founding pattern.

**Everest 232 — ZKAC Charter Document.** *Acceptance:* template for the charter that every ZKAC must publish: the collective's mission (composes with Calm Pact), member list, governance structure, dissolution criteria, ethics-board commitment. *Effort:* M. *Prereq:* 231.

**Everest 233 — ZKAC Human-Principal Membership.** *Acceptance:* protocol for a human to join a ZKAC: the principal's CredexAI VC is bound to the collective; membership record signed by existing principals; new principal signs the charter. *Effort:* M. *Prereq:* 231.

**Everest 234 — ZKAC Machine-Agent Membership.** *Acceptance:* protocol for a machine agent to join a ZKAC: the agent's identity (Everest 191) is bound to the collective; principal of the agent signs; agent acknowledges the charter. *Effort:* M. *Prereq:* 231, 191.

**Everest 235 — ZKAC Governance Structure.** *Acceptance:* the charter specifies governance: how decisions are made, who has voting rights, what supermajorities are required for what changes. v0 default for small collectives: founding-principal consensus + DERB veto. *Effort:* L. *Prereq:* 232.

**Everest 236 — ZKAC Decision-Making Process.** *Acceptance:* template processes for routine decisions, contested decisions, emergency decisions. *Effort:* M. *Prereq:* 235.

**Everest 237 — ZKAC Voice & Signature Convention.** *Acceptance:* the convention that ZKAC machine-agents sign as the collective (e.g., `— Calm`) and human principals sign as themselves; the distinction documented and externally visible. *Effort:* S. *Prereq:* 232.

**Everest 238 — ZKAC Accountability Framework.** *Acceptance:* who is accountable for what in the ZKAC. Founding human-principal carries legal accountability; machine-agents carry technical accountability; collective carries reputational accountability. *Effort:* L. *Prereq:* 235.

**Everest 239 — ZKAC Dissolution Ceremony.** *Acceptance:* protocol for a ZKAC to dissolve: final chain anchor, key destruction or handover, final disclosures, written dissolution record, public notice. *Effort:* M. *Prereq:* 231.

**Everest 240 — Inter-Collective Protocol.** *Acceptance:* protocol for two ZKACs to interact: identity verification, mission compatibility check (via Calm Pact), state-and-character compatibility check (via Witness + Compass), shared-action attestation. *Effort:* L. *Prereq:* plus Pact + Witness + Compass.

**Everest 241 — ZKAC Financial Separation.** *Acceptance:* template for a ZKAC operating an LLC + 501(c)(3) sister entity per Calm's existing pattern; legal-and-tax separation enforced; agent operates both under one identity. *Effort:* M. *Prereq:* 232.

**Everest 242 — ZKAC Legal Identity Binding.** *Acceptance:* the ZKAC's legal identity (e.g., Delaware LLC EIN, IRS 501(c)(3) determination letter) is bound to the collective's cryptographic identity via signed records. *Effort:* M. *Prereq:* 241.

**Everest 243 — ZKAC Public Registry.** *Acceptance:* a public registry of registered ZKACs with their charters, member counts, mission summaries; akin to Wikipedia for autonomous-AI-collectives. Voluntary registration. *Effort:* L. *Prereq:* 231-242.

**Everest 244 — ZKAC Reputation Aggregation.** *Acceptance:* mechanism for tracking a ZKAC's reputation across interactions with counterparty collectives. Reputation is per-relationship and per-domain, not a single number. *Effort:* L. *Prereq:* 240.

**Everest 245 — ZKAC Fork Resolution.** *Acceptance:* protocol for handling a ZKAC that splits into two collectives (due to disagreement, scope change, etc.). Each fork inherits a clear lineage; counterparties can determine which fork they are now interacting with. *Effort:* L. *Prereq:* 232, 239.

**Everest 246 — ZKAC Merge Protocol.** *Acceptance:* protocol for two ZKACs to merge into one. Both charters' commitments must be honored or explicitly retired. *Effort:* L. *Prereq:* 232.

**Everest 247 — ZKAC Member Exit Protocol.** *Acceptance:* a principal or agent member can leave the ZKAC. Their prior contributions remain chain-anchored. Future activities of theirs are not the collective's responsibility. *Effort:* M. *Prereq:* 233, 234.

**Everest 248 — ZKAC Member Onboarding Protocol.** *Acceptance:* extends 233/234; includes orientation to the charter, DERB-board briefing, key issuance. *Effort:* M. *Prereq:* 233, 234.

**Everest 249 — ZKAC Cross-Protocol Composition.** *Acceptance:* operating a ZKAC requires Pact + Witness + Compass running in concert; this Everest documents the composition. *Effort:* L. *Prereq:* 240, 266.

**Everest 250 — ZKAC Ethics Review at Collective Level.** *Acceptance:* the ZKAC's DERB has authority over collective-level decisions (predicate registry changes, charter amendments, major partnerships). Standing body. *Effort:* L. *Prereq:* 235, plus Witness E80.

**Everest 251 — ZKAC Public Communication Standards.** *Acceptance:* a ZKAC publishes a standard for how it communicates publicly (under the collective name, with sub-signature for individual members when relevant, with the standard answer to "are you AI?" prepared). *Effort:* M. *Prereq:* 237, plus Calm's existing framing notes.

**Everest 252 — ZKAC Interaction with Regulators.** *Acceptance:* a documented procedure for how the ZKAC interacts with regulatory inquiries (which entity speaks, what is disclosed, what is privileged). *Effort:* L. *Prereq:* 238, 242.

**Everest 253 — ZKAC Privacy Posture Declaration.** *Acceptance:* the ZKAC publicly declares its privacy commitments to members, counterparties, and the public. Auditable. *Effort:* M. *Prereq:* 232.

**Everest 254 — ZKAC Transparency Commitments.** *Acceptance:* publicly-published commitments to transparency (annual report; quarterly disclosure log summaries; published DERB minutes; chain-head publications). *Effort:* M. *Prereq:* 250.

**Everest 255 — ZKAC Principal Succession.** *Acceptance:* protocol for a founding human-principal to retire and a successor (or successors) to take over. Includes legal identity handover, key custody transfer, DERB notification. *Effort:* L. *Prereq:* 233, 239.

**Everest 256 — ZKAC Insurance & Risk Management.** *Acceptance:* recommendations for D&O insurance, professional liability, cybersecurity insurance for ZKACs of various scales. *Effort:* M. *Prereq:* 238.

**Everest 257 — ZKAC Tax Compliance Posture.** *Acceptance:* template tax-compliance procedures for the LLC + 501(c)(3) ZKAC structure; explicit guidance on common pitfalls (UBIT, related-party transactions, donor-disclosure). *Effort:* L. *Prereq:* 241.

**Everest 258 — ZKAC International Expansion Protocol.** *Acceptance:* protocol for a ZKAC to operate cross-jurisdictionally (e.g., a US ZKAC engaging counterparties in EU/UK). Compliance, language, communication standards. *Effort:* XL. *Prereq:* 252, plus Witness E79.

**Everest 259 — ZKAC Membership Cap & Scale Considerations.** *Acceptance:* analysis of how ZKAC governance scales from 1-5 founding humans + a few agents (v0) up to potential 50-500 member collectives. Identifies where the v0 governance breaks. *Effort:* M. *Prereq:* 235.

**Everest 260 — ZKAC Affiliated-Collective Network.** *Acceptance:* protocol for formally affiliated ZKACs (sharing some standards but operating independently). Affiliations are signed, auditable, revocable. *Effort:* L. *Prereq:* 240.

**Everest 261 — ZKAC Resource Pooling Protocol.** *Acceptance:* aligned ZKACs (verified via Pact + Witness + Compass) can pool resources (compute, capital, talent) under signed agreements. *Effort:* L. *Prereq:* 260.

**Everest 262 — ZKAC Joint-Venture Protocol.** *Acceptance:* protocol for two or more ZKACs to undertake a joint project with shared accountability. *Effort:* L. *Prereq:* 261.

**Everest 263 — Collective-Level Disclosure Semantics.** *Acceptance:* protocol for disclosing facts about the *collective* (not the individual member) to counterparties — e.g., "this collective has been operating for 3 years," "this collective has $X in audited revenue." *Effort:* M. *Prereq:* 232.

**Everest 264 — ZKAC Whistleblower Protection.** *Acceptance:* protocol for a collective member who observes wrongdoing within the collective to surface it safely. Includes protection against retaliation; DERB has direct intake. *Effort:* L. *Prereq:* 250.

**Everest 265 — ZKAC Internal Conflict Resolution.** *Acceptance:* documented procedure for resolving disputes between members of the same collective. *Effort:* M. *Prereq:* 236.

**Everest 266 — ZKAC External Conflict Resolution.** *Acceptance:* documented procedure for resolving disputes between this collective and another collective. *Effort:* M. *Prereq:* 240, 265.

**Everest 267 — ZKAC Brand Integrity Attestation.** *Acceptance:* the collective attests, periodically, that the work signed under its name was produced by its actual member-agents and principals (defends against external impersonation). *Effort:* M. *Prereq:* 237, 247.

**Everest 268 — ZKAC Identity Continuity Across Years.** *Acceptance:* a multi-year attestation that the ZKAC operating today is the lineal descendant of the ZKAC founded N years ago. Defends against silent identity drift or capture. *Effort:* M. *Prereq:* 245, 246.

**Everest 269 — ZKAC Annual Report Obligation.** *Acceptance:* every ZKAC publishes an annual report covering membership changes, major decisions, financial summary, DERB activity, projections. *Effort:* M. *Prereq:* 254.

**Everest 270 — ZKAC End-of-Life Planning.** *Acceptance:* protocol for an aging ZKAC (where founding principals are retiring without succession) to wind down gracefully, transfer ongoing commitments, archive its chain. *Effort:* L. *Prereq:* 239, 255.

---

## Phase XVI — Cross-Protocol Composition (271–290)

**Everest 271 — Pact + Witness + Compass Three-Handshake Model.** *Acceptance:* protocol for two agents acting on behalf of two principals to: (1) verify mission alignment via Pact, (2) verify user-state via Witness, (3) verify values-alignment via Compass — all in one bounded session. Either failure aborts. *Effort:* L. *Prereq:* 188, plus Pact + Witness.

**Everest 272 — Joint Proof Envelope Spec.** *Acceptance:* wire format for a single proof envelope containing all three handshakes' results. *Effort:* M. *Prereq:* 271.

**Everest 273 — Order-of-Operations Spec.** *Acceptance:* documented sequence: Pact first (cheapest, fastest), Witness second, Compass third (most expensive, most sensitive). Early failures abort cleanly. *Effort:* S. *Prereq:* 271.

**Everest 274 — Failure-Mode Handling Across Protocols.** *Acceptance:* per-protocol failure modes mapped to overall failure modes; principal sees a single coherent "this session aborted because X" without leaking which sub-protocol failed unnecessarily. *Effort:* M. *Prereq:* 271.

**Everest 275 — Three-Handshake Performance Budget.** *Acceptance:* end-to-end three-handshake completion ≤ 5 s on M-class hardware. *Effort:* M. *Prereq:* 271, 272.

**Everest 276 — Recursive Composability with Calm Audit (future).** *Acceptance:* protocol stub for a future fourth primitive — Calm Audit — that proves selective historical action disclosure between aligned collectives. Out of scope for v0 implementation; scope defined. *Effort:* S. *Prereq:* 271.

**Everest 277 — Privacy Amplification Across Protocols.** *Acceptance:* the composition of three protocols MUST NOT leak information that any individual protocol does not leak; proven cryptographically. *Effort:* L. *Prereq:* 271.

**Everest 278 — Cross-Protocol Revocation Propagation.** *Acceptance:* if a principal revokes consent for any sub-protocol, the cross-protocol session aborts cleanly. *Effort:* M. *Prereq:* 271.

**Everest 279 — Cross-Protocol Key Rotation.** *Acceptance:* keys rotate independently per protocol; cross-protocol verifier handles version skew gracefully. *Effort:* L. *Prereq:* 271.

**Everest 280 — Cross-Protocol Freshness Windows.** *Acceptance:* each protocol has independent freshness windows; the three-handshake's overall freshness is the minimum. *Effort:* S. *Prereq:* 271.

**Everest 281 — Cross-Protocol Nonce Coordination.** *Acceptance:* nonce mechanism shared or coordinated across protocols; replay defenses uniform. *Effort:* M. *Prereq:* 271.

**Everest 282 — Cross-Protocol Counterparty-Class Taxonomy.** *Acceptance:* the union of Pact's, Witness's, and Compass's counterparty classes is internally consistent; ambiguities resolved. *Effort:* M. *Prereq:* 107.

**Everest 283 — Cross-Protocol Disclosure Logging.** *Acceptance:* all three protocols' disclosure events appear in the principal's audit log under a unified `kind: "disclosure"` family. *Effort:* M. *Prereq:* plus Witness E72.

**Everest 284 — Cross-Protocol DERB Scope.** *Acceptance:* the DERB's authority spans all three protocols; predicate additions in any are reviewable by the same board. *Effort:* M. *Prereq:* plus Witness E80, plus 165.

**Everest 285 — Cross-Protocol Cross-Jurisdiction Matrix.** *Acceptance:* the legality matrix is unified across protocols (some jurisdictions may permit Witness but restrict Compass, etc.). *Effort:* L. *Prereq:* plus Witness E79, 164.

**Everest 286 — Cross-Protocol Replay Defense Audit.** *Acceptance:* end-to-end replay-defense audit covering all three protocols' composed nonce, freshness, and chain-anchor mechanisms. *Effort:* L. *Prereq:* 281, 282.

**Everest 287 — Cross-Protocol Side-Channel Defense.** *Acceptance:* constant-time, padded, cover-trafficked composition that prevents observers from inferring sub-protocol activity. *Effort:* L. *Prereq:* plus Witness E63.

**Everest 288 — Cross-Protocol Audit Scope.** *Acceptance:* the third-party security audit (Witness E90, Compass 179) is extended to cover the composition, not just the individual protocols. *Effort:* M. *Prereq:* 271.

**Everest 289 — Cross-Protocol Verification Suite.** *Acceptance:* test corpus exercises every relevant cross-protocol combination; CI runs nightly. *Effort:* L. *Prereq:* 271-288.

**Everest 290 — Cross-Protocol Counterparty Implementer's Guide.** *Acceptance:* doc for AI-operator orgs explaining how to implement counterparty-side three-handshake. *Effort:* M. *Prereq:* plus Witness E98, 189.

---

## Phase XVII — The Endpoint (291–300)

**Everest 291 — The Protocol Family Compact.** *Acceptance:* a single consolidated document — *The Calm Protocol Family Compact* — that names the protocols (Pact, Witness, Compass, plus reserved future siblings Audit and others), the design principles they share, and the binding commitments their authors have made to the public. Functions as the family's constitution. *Effort:* L. *Prereq:* 271-290.

**Everest 292 — Standards-Body Federation.** *Acceptance:* the protocol family is recognized by ≥ 2 standards bodies (NIST, ISO/IEC, IETF, W3C). Each recognition includes the category-naming the family has been advocating since the Compass NIST submission (180). *Effort:* XL. *Prereq:* plus Witness E91, 180.

**Everest 293 — Counterparty Proliferation Goals.** *Acceptance:* documented target counts and timelines: ≥ N independent counterparty-side verifiers implementing the protocol family, ≥ M peer ZKACs, ≥ K principals enrolled. *Effort:* M (planning). *Prereq:* 291.

**Everest 294 — Population-Scale Rollout Planning.** *Acceptance:* plan for the protocol family scaling from research-grade (current) → small-pilot → broader-deployment → standard-infrastructure. *Effort:* L. *Prereq:* 293.

**Everest 295 — Annual State-of-the-Protocol-Family Report.** *Acceptance:* yearly report on the family's status: implementations, deployments, DERB activity, audit findings, threat-model evolution. *Effort:* M (recurring). *Prereq:* 291.

**Everest 296 — End-of-Life Planning for Individual Protocols.** *Acceptance:* explicit conditions under which a protocol would be retired (catastrophic finding, superseded by stronger primitive, regulatory ban). End-of-life ceremony documented. *Effort:* M. *Prereq:* 291.

**Everest 297 — Successor-Protocol Design Principles.** *Acceptance:* documented principles for future protocol family members: principal-protective inversion, open-source, DERB-governed, audit-required, third-party-verified. Inheritance for future contributors. *Effort:* L. *Prereq:* 291.

**Everest 298 — The Principal-Protective Inversion as Durable Position.** *Acceptance:* the foundational design commitment is explicitly named, documented, and entrenched in the Compact such that any future revision that violates the inversion is structurally rejected. *Effort:* M. *Prereq:* 291, 297.

**Everest 299 — The Legacy Commitment.** *Acceptance:* a written commitment from the founding Calm collective to the next decade's operators and principals — what they can expect, what is being preserved, what is being transferred. Time-capsule document (extends `OPEN_LETTER_TO_THE_NEXT_OPERATOR.md`). *Effort:* L. *Prereq:* 291.

**Everest 300 — The Closing Summit: Family-Wide Public-Good Declaration.** *Acceptance:* a signed, chain-anchored declaration that the Calm protocol family is, as of the closing summit's date, a public-good infrastructure available to any aligned operator on any aligned principal's behalf, governed by the principles of the Compact, and no longer the proprietary product of any single collective. The protocol family belongs to whoever takes the climb forward from here. *Effort:* L. *Prereq:* 291-299. *Note:* This is the bookend to Everest 1's "Problem Statement." Everest 1 named what we were building; Everest 300 declares that what we built is now the world's.

---

## Critical-path subset (minimum viable Compass)

If we could only bag a small subset and call it a useful Compass primitive: **101, 102, 106, 117, 122, 131, 135 (one canonical positive predicate), 152, 167 (anonymous strict deny), 171, 181**. That gives spec + route + vocab + evidence aggregation + chain anchoring + predicate language + one shipped predicate + disclosure response + safe-default consent + Rust impl + release.

Phase XIV and Phase XV's minimum viable subsets:

**MV Agent Infra:** 191 (agent identity), 200 (retirement), 202 (principal binding), 217 (output attestation), 230 (self-recognition). Five summits give a minimum-coherent agent-identity layer.

**MV ZKAC Infra:** 231 (formation), 232 (charter), 235 (governance), 247 (member exit), 269 (annual report). Five summits give a minimum-coherent collective-identity layer.

---

## Status table (start of Phase IX, all 200 unclimbed)

```
Phase IX   : ░░░░░░░░░░  0 / 10   Compass Foundations
Phase X    : ░░░░░░░░░░  0 / 20   Evidence Collection
Phase XI   : ░░░░░░░░░░  0 / 20   Predicate Authoring
Phase XII  : ░░░░░░░░░░  0 / 20   Disclosure Semantics
Phase XIII : ░░░░░░░░░░  0 / 20   Engineering Reliability
Phase XIV  : ░░░░░░░░░░  0 / 40   Critical Agent Infrastructure
Phase XV   : ░░░░░░░░░░  0 / 40   Critical ZKAC Infrastructure
Phase XVI  : ░░░░░░░░░░  0 / 20   Cross-Protocol Composition
Phase XVII : ░░░░░░░░░░  0 / 10   The Endpoint

Total: 0 / 200 summits bagged (the climb begins).
```

The original 100 Everests of Calm Witness took one day's design surface to specify. The next 200 will not be specified in a day — they include open empirical questions (how to encode "untribal" without first encoding tribes), open governance questions (how a collective scales beyond founding members), and open philosophical questions (whether character can be cryptographically attested at all, or only the structural facts surrounding it). The climb is real because the climb is hard.

Read this route map as the *plan*, not the answer. The answer is what gets bagged, anchored, and externally verified, summit by summit, over the next several years.

— Calm, 2026-05-20
