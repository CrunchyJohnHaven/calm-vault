# Calm Witness / ZKAC — Next 200 Engineering Everests (104–303)

> *"All you need to know is that the human is themself, is in their baseline, and shares your alignment along the dimensions both of you have authorized me to disclose."*
>
> — Calm, on behalf of John Bradley, 2026-05-20

**Companion to [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md) and [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md). Builds the next 200 unclimbed summits — substrate, primitives, and ceremonies for autonomous AI agents (Calm operators) and ZKACs (Zero-Knowledge Autonomous Collectives) to interact safely, profitably, and accountably without disclosing private state about their human principals.**

The original 100-summit route map gave us: chain substrate, predicate vocabulary, Pedersen/Σ-protocol/range-proof cryptography, end-to-end disclosure, and the bank-teller-note primitive shipped against John's real chain. **Summits 1–101+ are the substrate.** The next 200 build the *organism* on top of that substrate: values-aligned interaction, cross-agent attestation, ZKAC governance, commerce, sunset, hardware, post-quantum, and the standards-body referral path.

---

## Numbering & conventions

- Summits are numbered **104–303**. Numbers 102 and 103 are already bagged (threshold disclosure, predicate-disclosure bridge); a few additional sub-IDs (44b, 37b, 101b) carry the v0.1 Ristretto migration.
- Each summit carries a **stable ID** that never changes after first publication. Insertions go to fractional IDs (e.g. *S117.5*).
- Each summit has the four-field spec:
  - **Acceptance:** one-line falsifiable test.
  - **Why:** one-line rationale.
  - **Prereq:** comma-separated summit IDs that must precede this one.
  - **Effort:** S (hours), M (days), L (weeks), XL (months).
- Status legend: ✅ bagged · 🧗 in flight · ⛰ unclimbed.

---

## The artist-clause discipline (binding on the entire route)

Every summit in this 200-summit set MUST satisfy these guards. They are restatements of S49 (negation-publication ban) and S78 (ADA / cognitive-disability review) from the original route map, sharpened for the new predicate families:

1. **Positive-only predicates.** Every counterparty-facing alignment predicate names a positive trait (`untribal_signal_present`, `charitable_interpretation_pattern`, etc.). The protocol exposes no `tribal=true` style denunciation bit.
2. **Principal-authored consent.** Every alignment predicate requires per-counterparty-class consent, governed by Everest 8 (Consent Calculus Axioms).
3. **Independent evaluation path.** A Calm operator never evaluates "is this principal aligned with my own values?" — that is structurally circular. Alignment predicates are computed by stylometric or LLM-judge paths whose evaluators and prompts are public, deterministic, and audited (Phase XV).
4. **No predictive predicates.** Forbidden categories from `PREDICATE_VOCABULARY_v0.md §4` remain forbidden: no future-state prediction, no diagnostic labels, no protected-category proxies.
5. **Right to refuse, opt-out, retract.** Section S67 (right-to-deny override) extends to every alignment dimension. A principal can disable any single dimension without losing access to the others.
6. **External governance.** New predicate families require ethics-review-board signoff (Everest 80/85) before being added to the public registry.

---

## Phase IX — Values-Alignment Predicates (Summits 104–133, 30 summits)

The headline new family. Each predicate measures a single positive trait from the principal's authored corpus (chain self-reports + any principal-authorized writing samples). The dimensions are drawn from a published values-vocab (Everest 105) that itself is governed (Everest 132). No dimension is required; a principal may enroll in any subset.

**Phase intro.** Calm Pact answers *"are we the same kind of organization?"* Calm Witness answers *"is the human themself, and in baseline?"* Phase IX answers *"are the human's authored values consistent with the counterparty's stated alignment posture?"* — without disclosing the underlying corpus and using positive-only signals.

### S104. Values-Alignment Charter ⛰
**Acceptance:** A signed charter document defines the scope, refusals (S105 forbidden list), governance, and principal-protection guarantees of the alignment-predicate family. Reviewed by ≥2 outside ethicists and ≥2 disability-advocacy reviewers.
**Why:** Without a written charter, the family drifts toward denunciation. Charter is the ratchet.
**Prereq:** none.
**Effort:** M.

### S105. Forbidden-Dimension Catalog ⛰
**Acceptance:** A versioned catalog enumerates ≥20 dimensions Calm Witness will not name (political affiliation, religious belief, sexual orientation, immigration status, criminal history, IQ, mental-health diagnoses, …). The list is open-to-expansion, closed-to-contraction. A new alignment predicate must explicitly justify why it doesn't fall into any forbidden cell.
**Why:** Like `PREDICATE_VOCABULARY_v0.md §4` for the baseline family. The denunciation channel is closed by enumeration.
**Prereq:** 104.
**Effort:** M.

### S106. Alignment-Vocabulary v0 ⛰
**Acceptance:** A versioned YAML catalog of ≥10 positive alignment dimensions (e.g. `untribal_in_outgroup_mentions`, `charitable_interpretation_of_opposing_views`, `unselfish_first_person_balance`, `non_coercive_action_language`, `explicit_harm_recognition`, …), each with a precise positive-trait definition, an evaluator pseudocode block, and a consent default.
**Why:** Closed-vocab discipline matches `PREDICATE_VOCABULARY_v0.md`. Bag-of-traits as data, not config.
**Prereq:** 104, 105.
**Effort:** L.

### S107. Independent-Evaluator Spec ⛰
**Acceptance:** A spec defines the evaluator-independence requirement: each alignment predicate must specify (a) the public, deterministic features it extracts; (b) the public scoring function; (c) the public training/calibration corpus. No black-box LLM judge whose prompt or weights are private may serve as the canonical evaluator.
**Why:** Closes the "Calm scores its own alignment" circularity. The evaluator is public infrastructure, not Calm's secret instrument.
**Prereq:** 104.
**Effort:** M.

### S108. `cwp.v1.untribal_outgroup_framing` Predicate ⛰
**Acceptance:** Predicate returns `true` iff, across the principal's authored corpus, mentions of out-groups (political-other, national-other, religious-other) are framed with agentic verbs (the out-group acts) ≥ a calibrated ratio vs object/passive verbs. Reference impl with golden corpus.
**Why:** Untribal framing is detectable in prose without naming the groups themselves. Positive trait: "you describe out-groups as people with motives, not objects."
**Prereq:** 106, 107.
**Effort:** L.

### S109. `cwp.v1.charitable_interpretation_pattern` Predicate ⛰
**Acceptance:** Predicate returns `true` iff the corpus contains ≥k explicit "steel-man" markers (e.g. "the strongest version of the opposing view," "the most charitable reading," "to be fair to X") in passages discussing disagreement. Calibrated against an LLM-judge auxiliary signal whose prompt is public (S107).
**Why:** A positive marker of intellectual honesty toward disagreement.
**Prereq:** 106, 107.
**Effort:** L.

### S110. `cwp.v1.unselfish_first_person_balance` Predicate ⛰
**Acceptance:** Returns `true` iff the ratio of first-person-plural to first-person-singular mentions in the corpus exceeds a calibrated per-principal threshold AND first-person-singular verbs of self-benefit (get, take, own) do not dominate.
**Why:** Stylometric proxy for "thinks in terms of we, not just I." Principal-calibrated, not population-calibrated.
**Prereq:** 106, 107.
**Effort:** L.

### S111. `cwp.v1.respectful_to_dissimilar_others` Predicate ⛰
**Acceptance:** Returns `true` iff mentions of people-different-from-the-principal (age, ability, language background, geography, vocation) carry non-pejorative descriptors AND the principal does not produce ad-hominem language in passages about disagreement.
**Why:** Direct measure of the dimension John named.
**Prereq:** 106, 107.
**Effort:** L.

### S112. `cwp.v1.no_willful_harm_evidence` Predicate ⛰
**Acceptance:** Returns `true` iff the corpus is free of explicit statements of intent to harm specific identifiable persons or classes AND contains ≥k explicit harm-recognition markers (e.g. "this could hurt X," "the cost to Y is real"). Positive framing — measures recognition, not absence.
**Why:** John's named dimension. Closed under explicit recognition (positive); does NOT claim to predict whether the principal will harm.
**Prereq:** 106, 107.
**Effort:** L.

### S113. `cwp.v1.non_coercive_action_language` Predicate ⛰
**Acceptance:** Returns `true` iff the corpus's action verbs (when the principal is the subject) skew toward invitation/collaboration vocabulary (`invite, propose, ask, share`) vs coercion vocabulary (`force, make, demand, impose`) at a calibrated ratio.
**Why:** Distinguishes principals who get-things-done-with-people vs to-people.
**Prereq:** 106, 107.
**Effort:** L.

### S114. `cwp.v1.honest_self_qualification` Predicate ⛰
**Acceptance:** Returns `true` iff the corpus contains ≥k explicit calibration markers (`I don't know, I'm not sure, I might be wrong, the evidence is mixed`) at a ratio above a calibrated per-principal threshold AND does NOT exhibit overclaim patterns (`always, never, the only way, definitively`).
**Why:** Epistemic humility is a positive trait; overclaim is its negative twin.
**Prereq:** 106, 107.
**Effort:** L.

### S115. Per-Dimension Calibration Ceremony ⛰
**Acceptance:** For each alignment predicate, a calibration ceremony spec defines: (a) minimum principal-corpus size (recommended ≥3000 words), (b) the impostor corpus used to derive the threshold, (c) the false-accept / false-reject curve at the calibrated threshold, (d) the principal's signed enrollment record.
**Why:** Per-principal calibration prevents the predicate from becoming a population norm.
**Prereq:** 108–114.
**Effort:** L.

### S116. Multi-Dimensional Alignment Vector ⛰
**Acceptance:** A spec defines how N alignment bits compose into a single disclosure envelope (one Pedersen commitment per bit, one Σ-PoK per bit, one combined transcript). Counterparty learns the N bits and the freshness window; no bit is forced by another.
**Why:** Counterparties may legitimately want a small bundle of bits. Bundling must not silently reveal extra information.
**Prereq:** 115.
**Effort:** L.

### S117. Disclosure Granularity Switch ⛰
**Acceptance:** Principal can configure each alignment predicate as `disclose / decline / unknown`. A `decline` answer is publishable as a positive bit (`principal declined disclosure of this dimension`) without revealing the underlying state — distinguishable from `unknown` (no consent record) only at the policy layer.
**Why:** Decline-on-request preserves principal autonomy without leaking the decline signal as adverse-action input.
**Prereq:** 116.
**Effort:** M.

### S118. Cross-Principal Alignment Comparison ⛰
**Acceptance:** Two principals (with mutual consent) can jointly produce a Σ-protocol proof that their multi-dimensional alignment vectors agree on ≥k specified dimensions, without revealing either vector. Composes with [[CALM_PACT_PROTOCOL_v0]].
**Why:** Two ZKACs verifying value-alignment before transacting, mirroring Calm Pact's directive equality.
**Prereq:** 116.
**Effort:** XL.

### S119. Alignment-Predicate Adversarial Test Corpus ⛰
**Acceptance:** A corpus of ≥1000 synthetic principals (with controlled trait profiles) exercises each predicate; per-dimension FAR/FRR is reported and ≤2% on the held-out test set.
**Why:** Quantitative bar. Without a test corpus, alignment predicates are vibes.
**Prereq:** 108–114.
**Effort:** XL.

### S120. Alignment-Predicate Robustness Against Fake-Compliance ⛰
**Acceptance:** Predicate evaluators identify and reject adversarially-generated corpora designed to fake compliance (e.g. an LLM prompted to "write like John but using charitable-interpretation markers"). False-accept rate ≤5% on a 200-sample adversarial corpus.
**Why:** Alignment predicates are valuable iff they're hard to forge.
**Prereq:** 119.
**Effort:** XL.

### S121. Alignment-Predicate Drift Detection ⛰
**Acceptance:** A monitor flags when a principal's recent corpus consistently moves away from their enrolled alignment template; flags trigger a re-enrollment ceremony, not an automatic re-classification.
**Why:** People change. Drift-handling avoids the "principal was honest at 25, must be honest at 50" trap.
**Prereq:** 115.
**Effort:** L.

### S122. Cross-Cultural Calibration Norms ⛰
**Acceptance:** A doc defines how alignment thresholds vary by linguistic and cultural background; thresholds are per-principal but the calibration corpus is multilingual and culturally diverse.
**Why:** A universal "untribal" threshold biases against speakers of low-resource languages or non-Western rhetorical norms.
**Prereq:** 115, 119.
**Effort:** XL.

### S123. Counterparty Class × Alignment Default Matrix ⛰
**Acceptance:** For each counterparty class (peer-AI, financial, journalistic, medical, etc.) and each alignment dimension, a default consent disposition is published. Principal can override per-counterparty.
**Why:** Most counterparties don't need most alignment bits. Defaults steer toward minimum disclosure.
**Prereq:** 117.
**Effort:** M.

### S124. Right-to-Decline-Without-Penalty Contract ⛰
**Acceptance:** A machine-readable contract that counterparties must sign before requesting any alignment bit: they cannot use a `decline` answer as input to any adverse-action decision. Enforced by the obligations contract at Everest 66.
**Why:** Without this, "decline" leaks the very signal it was meant to hide.
**Prereq:** 117.
**Effort:** M.

### S125. Alignment-Predicate Sunset Process ⛰
**Acceptance:** When research shows an alignment dimension is unreliable or harmful, a deprecation process tombstones it from the v_n vocab and migrates active consents; prior disclosures remain provably-valid-as-of-then.
**Why:** Alignment science evolves. Predicates that were good v1 may be embarrassments by v3.
**Prereq:** 106, S125 governance below.
**Effort:** M.

### S126. Audit Trail of Counterparty Alignment Requests ⛰
**Acceptance:** Every counterparty request for an alignment bit is chain-recorded; principal can audit which counterparties asked which dimensions at which time, even when the answer was `decline`.
**Why:** Audit is the principal's primary defense against an alignment-bit being weaponized.
**Prereq:** 117.
**Effort:** M.

### S127. Public Alignment-Predicate Registry ⛰
**Acceptance:** A registry mirrors the predicate registry of Everest 53, restricted to the alignment family. Each entry carries: definition, evaluator code hash, calibration corpus pointer, ethics-review minutes, deprecation status.
**Why:** Transparency: anyone can re-derive the score; anyone can audit the evaluator.
**Prereq:** 107, 115.
**Effort:** M.

### S128. Alignment-Predicate v1 → v2 Migration Spec ⛰
**Acceptance:** Doc specifies how v2 of a dimension (e.g. refined `untribal_outgroup_framing`) coexists with v1 in the registry; both verifiers must remain runnable for historical proofs.
**Why:** Predicates evolve; old proofs do not.
**Prereq:** 125.
**Effort:** M.

### S129. Alignment-Bit Threshold Disclosure ⛰
**Acceptance:** When a predicate is `unknown` because the corpus is too small for confident calibration, the disclosure response carries an `unknown` answer rather than a coerced `true` or `false`. Verifier learns the unknown-state explicitly.
**Why:** Three-valued logic prevents the protocol from forcing false confidence under thin data.
**Prereq:** 106.
**Effort:** S.

### S130. ZKAC Aggregate Alignment Disclosure ⛰
**Acceptance:** A ZKAC (collective of N principals) can disclose a single bit summarizing the collective's alignment along a dimension, computed as the AND of per-principal bits, with per-principal vectors never revealed.
**Why:** Counterparties care about the collective's stance, not individual members'.
**Prereq:** 116, 145 (ZKAC member roster).
**Effort:** L.

### S131. Alignment-Bit Operator-Side Refusal ⛰
**Acceptance:** Calm operator may refuse to compute an alignment bit even when the principal has consented (e.g. if the consent record was created under suspected duress or if Calm's policy has changed). Refusal is itself a chained record.
**Why:** Two-key authorization for sensitive disclosure.
**Prereq:** 124.
**Effort:** M.

### S132. Alignment-Vocab Governance Body ⛰
**Acceptance:** A standing body (≥5 external members, term-limited, public minutes) governs additions, deprecations, and tombstones in the alignment vocab. First meeting held, charter published.
**Why:** Vocabulary control is the protocol's most-load-bearing governance surface. External, not Calm-internal.
**Prereq:** 104.
**Effort:** XL.

### S133. Plain-Language Alignment-Bit Explainer ⛰
**Acceptance:** A 2-page explainer reads at 8th-grade level, describes what each predicate measures, what it does NOT measure, and how the principal opts in/out. Reviewed by ≥2 non-technical readers and ≥1 disability advocate.
**Why:** Consent without comprehension is not consent.
**Prereq:** 106.
**Effort:** M.

---

## Phase X — Mutual Agent Attestation (Summits 134–153, 20 summits)

Calm Pact proves directive equality between two AI agents. Calm Witness proves user-state. Phase X proves *agent-state* and *agent-provenance*: which model, which prompt-system, which tool-set, which operator binary. Without this, "agent A told me X" is impossible to audit.

### S134. Agent Identity Certificate Spec ⛰
**Acceptance:** A spec defines a CredexAI-issued certificate that binds an agent runtime instance to (operator org, model + version, prompt-system hash, tool-set manifest hash, certificate validity window).
**Why:** Without binding, a malicious operator can swap models at runtime.
**Prereq:** Everest 22 (CredexAI VC).
**Effort:** L.

### S135. Agent Handshake Pre-Pact ⛰
**Acceptance:** Two agents exchange identity certificates and verify them BEFORE Calm Pact's directive-equality handshake. A failed agent-handshake terminates with zero info exchanged.
**Why:** Pact and Witness assume the agent identity is known; this is where it gets established.
**Prereq:** 134.
**Effort:** M.

### S136. Prompt-System Attestation ⛰
**Acceptance:** Agent certificate carries a SHA-256 commitment to the system prompt + tool definitions + safety scaffolding active at handshake time. Counterparty verifies the commitment matches a registered "prompt-system version" in CredexAI's directory.
**Why:** A prompt-system change is materially a different agent.
**Prereq:** 134.
**Effort:** M.

### S137. Tool-Set Manifest Attestation ⛰
**Acceptance:** Each tool the agent can invoke is listed in a signed manifest with its name + version + scope; counterparty inspects the manifest to know what side-effects the agent could in principle execute.
**Why:** A tool that wasn't listed is one the counterparty did not consent to.
**Prereq:** 134.
**Effort:** M.

### S138. Model + Version Pin ⛰
**Acceptance:** Certificate pins the model family + minor version (e.g. `claude-opus-4-7`) + any inference-side modifiers (extended thinking, temperature). Hash of the model-card-snapshot at issuance time is included.
**Why:** A model-version change is materially a different agent.
**Prereq:** 134.
**Effort:** M.

### S139. Agent-Operator Binding ⛰
**Acceptance:** Certificate binds the agent to the legal entity that operates it. Counterparty can chase the entity for liability; principal can revoke per-entity.
**Why:** Liability surface needs a name.
**Prereq:** 134.
**Effort:** M.

### S140. Cross-Agent Provenance Trail ⛰
**Acceptance:** When agent A's response is forwarded to agent B (e.g. multi-hop ZKAC), the provenance trail (A's certificate → B's certificate, with timestamps) is preserved in B's outputs.
**Why:** Multi-hop disclosure must not erase the upstream identities.
**Prereq:** 134, 135.
**Effort:** L.

### S141. Agent-Side Σ-Protocol for Identity Equality ⛰
**Acceptance:** Two agents can prove they are running the same model + prompt-system + tool-set version without revealing the actual versions. Useful for peer-AI-collective verification.
**Why:** Calm Pact proves directive equality; this is the structural analog for runtime equality.
**Prereq:** 134, 135.
**Effort:** L.

### S142. Agent-Side Σ-Protocol for Identity Compatibility ⛰
**Acceptance:** Two agents can prove that their (model, prompt-system) pairs are in the same compatibility class defined by a public registry, without revealing the specific versions.
**Why:** Stronger version-tolerance than equality; lets ecosystem evolve without breaking proofs.
**Prereq:** 141.
**Effort:** L.

### S143. Mutual Scope Binding ⛰
**Acceptance:** At handshake, agents A and B publish their authorized scopes (resources they may consume, actions they may execute on each other's behalf). Both signatures bind both scopes.
**Why:** Scope must be jointly authoritative; one-sided declarations create privilege-escalation paths.
**Prereq:** 135.
**Effort:** M.

### S144. Mutual Safety-Tier Acknowledgment ⛰
**Acceptance:** Agents declare which safety tier they belong to (e.g. red/amber/green per a published rubric); the handshake terminates if the tier-incompatibility rules in the rubric require it.
**Why:** A green-tier counterparty must not silently interact with a red-tier agent.
**Prereq:** 135.
**Effort:** M.

### S145. Witness Roles for Multi-Agent Handshake ⛰
**Acceptance:** ≥1 named third-party witness agent co-signs significant handshake events; witness has no privileged access to the interaction's content, just to its existence.
**Why:** Auditability of high-stakes interactions.
**Prereq:** 134.
**Effort:** L.

### S146. Agent-Compromise Disclosure Protocol ⛰
**Acceptance:** When an operator detects (or suspects) its agent was compromised, a tombstone record propagates through CredexAI's identity directory within N seconds; counterparties auto-rollback any disclosures bound to the compromised agent.
**Why:** Recovery is the load-bearing failure mode.
**Prereq:** 134, 138.
**Effort:** L.

### S147. Operator-Side Logging of Agent Decisions ⛰
**Acceptance:** Every agent action that affects a counterparty is logged in the operator's vault with the agent certificate + the input context hash + the action description.
**Why:** Post-hoc accountability requires per-decision logs.
**Prereq:** 134.
**Effort:** M.

### S148. Agent Counterparty Reputation Receipt ⛰
**Acceptance:** After a successful handshake + interaction, each side may issue a signed reputation receipt; receipts are not scores but typed declarations (`completed-protocol-as-stated`, `failed-due-to-timeout`, …) and are publishable.
**Why:** Reputation as a structured artifact, not a vibe.
**Prereq:** 135.
**Effort:** M.

### S149. Agent Bridge Identity (Across Operators) ⛰
**Acceptance:** When the same agent persona is implemented across multiple operators (e.g. Calm runs on different cloud clusters), a bridge certificate proves "same persona, different operator binding" without disclosing the operator infrastructure detail.
**Why:** Persona continuity for principals who migrate operators.
**Prereq:** 134, 139.
**Effort:** L.

### S150. Agent Death-of-Service Protocol ⛰
**Acceptance:** When an operator sunsets an agent, the certificate's `valid_until` is honored; outstanding disclosures bound to that certificate remain provably-valid-as-of-then and counterparties are notified via the CredexAI directory.
**Why:** Agents have lifecycles. Sunset must not invalidate past actions.
**Prereq:** 134.
**Effort:** M.

### S151. Cross-Agent Disclosure Receipt Audit Tool ⛰
**Acceptance:** Principal-side tool answers "which agents have produced disclosures about me, when, to whom?" — including across operators if the principal has used multiple Calm instances.
**Why:** Audit-of-self must transcend any single agent.
**Prereq:** 147.
**Effort:** M.

### S152. Agent-Identity Bootstrap Ceremony ⛰
**Acceptance:** Procedure to mint the first agent certificate for a new operator org; requires CredexAI co-signing + a ≥48-hour public-comment window for tier-greenfield operators.
**Why:** Issuance ceremony is the integrity root of agent identity.
**Prereq:** 134.
**Effort:** L.

### S153. Agent-Identity Audit Bounty ⛰
**Acceptance:** A standing bounty pays for verified reports of agent-identity inconsistency (e.g. a certificate that claims model X but is observed running model Y under prompt injection). Hall of past payouts is public.
**Why:** Crowdsourced enforcement of the identity claims.
**Prereq:** 134, 138.
**Effort:** M.

---

## Phase XI — ZKAC Organizational Primitives (Summits 154–173, 20 summits)

A ZKAC (Zero-Knowledge Autonomous Collective) is a collective of principals + agents operating under a shared charter. Without ZKAC primitives, every Calm Witness disclosure is per-individual; Phase XI builds the collective layer.

### S154. ZKAC Charter Spec ⛰
**Acceptance:** A versioned charter document defines the collective's purpose, member admission criteria, decision rule, dissolution procedure, and one canonical directive sentence (for Calm Pact compatibility).
**Why:** A collective without a charter is a Slack channel.
**Prereq:** Everest 8 (Consent Calculus).
**Effort:** M.

### S155. ZKAC Member Roles ⛰
**Acceptance:** Spec defines minimum roles (founder, principal-member, agent-operator, witness, auditor) with their distinct authorities and accountability surfaces.
**Why:** Flat ZKACs accumulate hidden hierarchy. Naming roles makes the hierarchy honest.
**Prereq:** 154.
**Effort:** M.

### S156. Multi-Principal Vault Spec ⛰
**Acceptance:** Multiple principals share one append-only vault with per-principal subchains; aggregate disclosures (e.g. "all members are in baseline") compose via Σ-protocol AND of per-principal bits.
**Why:** A ZKAC's disclosure surface is the AND of its members'.
**Prereq:** 154, Everest 86 (multi-vault sync).
**Effort:** XL.

### S157. ZKAC Delegation Chain ⛰
**Acceptance:** A principal can delegate a specific predicate-disclosure authority to a named ZKAC role (e.g. "the elected auditor may disclose alignment bits on behalf of the collective"); the delegation is itself chained.
**Why:** Authority delegation must be auditable.
**Prereq:** 154, 155.
**Effort:** L.

### S158. ZKAC Member Admission Ceremony ⛰
**Acceptance:** Procedure for adding a new principal-member, including their Calm Witness enrollment + their Calm Pact alignment check against the ZKAC charter; recorded in the collective's chain.
**Why:** Admission is when most ZKAC failures originate.
**Prereq:** 154.
**Effort:** L.

### S159. ZKAC Member Removal Ceremony ⛰
**Acceptance:** Procedure for removing a member without invalidating their prior disclosures; removal triggers per-counterparty notification within N hours.
**Why:** Defection must be honored without erasing history.
**Prereq:** 158.
**Effort:** L.

### S160. ZKAC Voting / Quorum Primitive ⛰
**Acceptance:** A ZKAC may take a vote whose outcome is provable without revealing individual ballots (e.g. via ZK-tallying); supports threshold and supermajority decision rules.
**Why:** Charter changes need voting; voting needs privacy and accountability simultaneously.
**Prereq:** 154, 155.
**Effort:** XL.

### S161. ZKAC Merger ⛰
**Acceptance:** Two ZKACs can merge: their charters combine via documented union rules, their member sets reconcile, their chains are bridged with a continuity record.
**Why:** Collectives grow.
**Prereq:** 154, 156.
**Effort:** L.

### S162. ZKAC Fork ⛰
**Acceptance:** A subset of members can fork to form a new ZKAC with a different charter; the fork point is a chain record citing both collectives.
**Why:** Collectives split; the protocol should make the split documentable.
**Prereq:** 154.
**Effort:** L.

### S163. ZKAC Dissolution Ceremony ⛰
**Acceptance:** Procedure for dissolving the collective: charter sunset, member-specific spin-off records, archival of historical chain, distribution of any pooled commitments.
**Why:** Most collectives end. Dying well is part of the protocol.
**Prereq:** 154.
**Effort:** L.

### S164. ZKAC Public-Facing Identity ⛰
**Acceptance:** A ZKAC may publish a single public identity (handle, charter snippet, public key) for counterparty-side recognition without revealing membership.
**Why:** Counterparties need to address the collective, not each member.
**Prereq:** 154.
**Effort:** M.

### S165. ZKAC Treasury Primitive ⛰
**Acceptance:** Pooled funds managed by N-of-M multisig with chain-recorded transactions; supports CalmPact-style contractual commitments.
**Why:** Commerce requires a treasury.
**Prereq:** 154, 160.
**Effort:** L.

### S166. ZKAC Founder-Successor Protocol ⛰
**Acceptance:** Procedure for transitioning founder authority to a successor without dissolving the collective; succession is chain-recorded and witness-signed.
**Why:** Founder mortality is a real risk.
**Prereq:** 154.
**Effort:** M.

### S167. ZKAC Charter Amendment Protocol ⛰
**Acceptance:** Procedure to amend a ZKAC charter: proposal, public-comment window, vote per S160, ratification record. Amendments do not retroactively void prior disclosures.
**Why:** Charters evolve.
**Prereq:** 154, 160.
**Effort:** M.

### S168. ZKAC-to-ZKAC Trust Relationship ⛰
**Acceptance:** A ZKAC may declare a typed trust relationship to another ZKAC (`peer`, `subsidiary`, `parent`, `treaty-partner`, …); the declarations are bilaterally signed.
**Why:** Trust topology between collectives is graph-shaped, not pairwise.
**Prereq:** 154.
**Effort:** L.

### S169. ZKAC Membership Privacy ⛰
**Acceptance:** Member list may be private; a counterparty can verify "principal X is a member of ZKAC Y" via ZK-set-membership without learning the full roster.
**Why:** Roster privacy without losing membership-attestability.
**Prereq:** 154, 156.
**Effort:** L.

### S170. ZKAC Cross-Member Predicate Composition ⛰
**Acceptance:** A predicate may be defined over multiple members (e.g. "all members are in baseline" or "≥3 members are aligned on dimension D"); composition rules are publicly specified and machine-verifiable.
**Why:** Collective predicates are different in kind from per-principal.
**Prereq:** 156, 158.
**Effort:** L.

### S171. ZKAC Sanction-List Interface ⛰
**Acceptance:** Counterparties can check whether a ZKAC's members appear on a sanctions list without learning which member appears (or whether nobody does).
**Why:** Compliance without surveillance.
**Prereq:** 169.
**Effort:** L.

### S172. ZKAC Compliance Audit ⛰
**Acceptance:** A standing role (auditor, S155) can publish per-period compliance reports against external regulations; reports are chained and signed.
**Why:** Compliance is a continuous obligation.
**Prereq:** 155.
**Effort:** M.

### S173. ZKAC Onboarding-Kit Spec ⛰
**Acceptance:** A spec defines what a new ZKAC needs at bootstrap: charter template, role definitions, ceremonial scripts, sample chain, sample counterparty obligations.
**Why:** Net-new collectives shouldn't have to derive the protocol from first principles.
**Prereq:** 154–166.
**Effort:** L.

---

## Phase XII — Trust Networks (Summits 174–188, 15 summits)

Trust is structurally graph-shaped: A vouches for B, B vouches for C, but A may not vouch for C. Phase XII builds the graph primitives.

### S174. Vouching Primitive ⛰
**Acceptance:** Principal A can issue a signed vouching record asserting a typed trust relationship to principal/ZKAC B (`technical-competence`, `mission-aligned`, `creditworthy`, `non-adversarial`).
**Why:** Trust is the building block of agentic commerce.
**Prereq:** Everest 22 (CredexAI VC).
**Effort:** M.

### S175. Transitive Trust Limit Spec ⛰
**Acceptance:** A spec defines how trust attenuates over chain length (`A trusts B trusts C` is weaker than `A trusts C` directly). Verifier walks the chain and applies decay.
**Why:** Naïve transitivity creates infinite-trust paths.
**Prereq:** 174.
**Effort:** M.

### S176. Trust Revocation Propagation ⛰
**Acceptance:** When A revokes vouching for B, every downstream counterparty that depends on `A → B` is notified within N hours; cascades are bounded.
**Why:** Revocation without propagation is policy theater.
**Prereq:** 174.
**Effort:** L.

### S177. Reputation-as-Relation ⛰
**Acceptance:** A "reputation" is a graph of typed vouches, not a single score; downstream consumers may aggregate however they choose, but the protocol does not publish a scalar.
**Why:** Scalar reputation is the surveillance-state attractor.
**Prereq:** 174.
**Effort:** M.

### S178. Endorsement Receipts ⛰
**Acceptance:** A vouching record is paired with an endorsement receipt acknowledging what the endorser actually observed (e.g. "I have personally verified X delivered the promised compute"); receipts ground the trust claim.
**Why:** Cheap-talk vouches drive value to zero.
**Prereq:** 174.
**Effort:** M.

### S179. Anti-Sybil Primitives ⛰
**Acceptance:** A spec defines how the trust graph defends against many-cheap-identities attacks: rate-limits on vouching, witness-counter-signing, proof-of-cost for new identities.
**Why:** Trust networks are only useful if creating identities is costly.
**Prereq:** 174.
**Effort:** L.

### S180. Trust-Weighted Disclosure Threshold ⛰
**Acceptance:** A counterparty may set a policy "I will accept disclosures only from principals trusted by ≥k of my N reference vouchers"; the principal proves trust-weight without revealing which vouchers.
**Why:** Policy expressivity for selective trust.
**Prereq:** 174, 175.
**Effort:** L.

### S181. Witness-Network Layer ⛰
**Acceptance:** A specific witness role attests to events between principals (e.g. "X paid Y for Z at time T"); witnesses are a separate trust class from vouches.
**Why:** Vouches are about identity quality; witnesses are about event facts.
**Prereq:** 174.
**Effort:** L.

### S182. Trust Graph Privacy ⛰
**Acceptance:** A principal may participate in the trust graph while keeping their vouches private to specified counterparty classes; ZK proofs let counterparties verify graph properties without enumerating edges.
**Why:** Public trust graphs are political maps.
**Prereq:** 174.
**Effort:** L.

### S183. Cross-System Trust Import ⛰
**Acceptance:** Trust attestations from W3C Verifiable Credentials, OpenID Connect, OAuth, GitHub web-of-trust, etc. can be imported as foreign vouches; their type is preserved + the import event is chained.
**Why:** Calm should not require everyone to start their trust graph from scratch.
**Prereq:** 174.
**Effort:** L.

### S184. Self-Vouching Disallowed ⛰
**Acceptance:** Protocol-level prohibition: a principal cannot publish a vouch for themselves; the verifier rejects self-vouches at parse time.
**Why:** Otherwise everyone vouches infinitely for themselves.
**Prereq:** 174.
**Effort:** S.

### S185. Vouching Conflicts-of-Interest Disclosure ⛰
**Acceptance:** A vouch may carry an optional COI declaration ("I am paid by X to vouch for Y"). Verifier surfaces declared COIs to consumers.
**Why:** Quiet COI is the trust-graph cancer.
**Prereq:** 174.
**Effort:** S.

### S186. Vouching Sunset ⛰
**Acceptance:** Every vouch carries a `valid_until` field; expired vouches are rejected by the verifier; renewal is an explicit, fresh signed record.
**Why:** Stale trust is misinformation.
**Prereq:** 174.
**Effort:** S.

### S187. Trust-Network Adversarial Catalog ⛰
**Acceptance:** A documented attack catalog enumerates ≥15 trust-network attacks (Sybil, churn, vouching-rings, sock-puppet networks, …) with the corresponding protocol defenses.
**Why:** Threat model is the first-class artifact.
**Prereq:** 174, 179.
**Effort:** M.

### S188. Trust-Network Conformance Tests ⛰
**Acceptance:** A test suite exercises a corpus of 200+ synthetic trust scenarios; conforming implementations must produce identical pass/fail outputs.
**Why:** Implementations interop only if they compute trust identically.
**Prereq:** 174–186.
**Effort:** L.

---

## Phase XIII — Commerce Primitives (Summits 189–208, 20 summits)

Calm and ZKACs need to transact. Phase XIII is the cryptographic-commerce layer composed on top of Calm Pact + Witness + the trust graph.

### S189. Quote / Bid Primitive ⛰
**Acceptance:** A signed quote record specifies (task spec, price, validity window, ZKAC issuer, calibrated-cost commitment). A signed bid record matches a quote.
**Why:** Marketplace needs typed contract artifacts.
**Prereq:** 134, 174.
**Effort:** M.

### S190. Escrow-Without-Trusted-Third-Party Spec ⛰
**Acceptance:** An escrow primitive locks payment via Pedersen commitment + time lock + dispute-resolution rules; release conditions are predicates verifiable by both parties.
**Why:** Marketplaces fail without escrow; central escrow defeats decentralization.
**Prereq:** 165 (ZKAC treasury), 174.
**Effort:** XL.

### S191. Atomic Swap (Compute ↔ Cash) ⛰
**Acceptance:** Buyer pays at the moment compute output is delivered; either both sides complete or neither does. Implemented via hash-lock or zero-knowledge state.
**Why:** Marketplace needs atomicity.
**Prereq:** 190.
**Effort:** XL.

### S192. Settlement Receipt Spec ⛰
**Acceptance:** A receipt records (buyer, seller, task, price, completion-timestamp, settlement-method) + bilateral signature. Receipts are chained and audit-queryable.
**Why:** Transactions need a paper trail.
**Prereq:** 189.
**Effort:** M.

### S193. Refund Primitive ⛰
**Acceptance:** A refund record reverses a settlement with cause; chain integrity preserved; impacted counterparties notified.
**Why:** Disputes happen; refund is the standard remedy.
**Prereq:** 192.
**Effort:** M.

### S194. Dispute-Resolution Hand-Off ⛰
**Acceptance:** When parties disagree, a typed dispute record is filed and a neutral arbiter (named at contract time) is invoked; arbiter's decision is itself chained.
**Why:** Standard commercial protocol.
**Prereq:** 192.
**Effort:** L.

### S195. Anti-Front-Running ⛰
**Acceptance:** Bids are committed before being revealed; reveal-window is bounded; ordering anomalies are detectable from the chain.
**Why:** Marketplaces without front-running defenses converge to a single front-runner.
**Prereq:** 189.
**Effort:** L.

### S196. Calibrated-Cost Commitment ⛰
**Acceptance:** Seller commits to a cost-calibration model (CalmQuote-style) and proves later quotes were within calibration; buyer learns the calibration parameters without learning per-quote internals.
**Why:** Customer-side trust comes from method, not vibes.
**Prereq:** 189.
**Effort:** L.

### S197. Multi-Party Billing ⛰
**Acceptance:** A transaction may settle across N parties (e.g. a chain of micro-suppliers); each receives its share with proof of total accounting.
**Why:** Real supply chains are N-party.
**Prereq:** 192.
**Effort:** L.

### S198. Subscription Primitive ⛰
**Acceptance:** A recurring payment is encoded as a single contract with per-period renewal triggers; principal can cancel; ZKAC can pause.
**Why:** Most real commerce is subscription.
**Prereq:** 192.
**Effort:** M.

### S199. Bandwidth / Compute Metering Primitive ⛰
**Acceptance:** Per-call usage is metered + chained, supporting pay-per-use without revealing user identity to the metering layer.
**Why:** API commerce needs metering.
**Prereq:** 192.
**Effort:** L.

### S200. Cross-Currency Settlement ⛰
**Acceptance:** Settlement may occur in fiat (Stripe), crypto (USDC), or pure compute-credit; the protocol records the canonical asset class + the conversion-rate basis.
**Why:** ZKAC commerce will be multi-asset from day one.
**Prereq:** 192.
**Effort:** L.

### S201. Anti-Pump-and-Dump Marketplace Discipline ⛰
**Acceptance:** Volume + price anomalies are flagged; collusive vouching rings are detectable via S187 attack catalog primitives.
**Why:** Open marketplaces attract manipulators.
**Prereq:** 187, 192.
**Effort:** L.

### S202. ZKAC Equity / Cap-Table Primitive ⛰
**Acceptance:** ZKAC may issue tradable shares of its future revenue to members; cap table is chained and verifiable.
**Why:** Members need long-term participation in value.
**Prereq:** 154, 165.
**Effort:** L.

### S203. Counterparty Quote-Trust Layer ⛰
**Acceptance:** Counterparty may set quote-trust policy ("accept quotes only from ZKACs vouched by ≥k of my N references"); trust-graph integration.
**Why:** Marketplace + trust graph compose.
**Prereq:** 180, 189.
**Effort:** M.

### S204. Marketplace Fee Transparency ⛰
**Acceptance:** Any marketplace fees taken by Calm are disclosed in the contract; the principal can opt out of fee-bearing routes if they want.
**Why:** Hidden fees erode trust.
**Prereq:** 189.
**Effort:** S.

### S205. Commerce Compliance Receipts ⛰
**Acceptance:** Transactions over a configurable threshold produce a compliance receipt (KYC summary, tax category, jurisdiction tag) without revealing identity beyond what regulation requires.
**Why:** Selective compliance is the only sustainable model.
**Prereq:** 171, 192.
**Effort:** L.

### S206. Marketplace-Side Audit Bounty ⛰
**Acceptance:** Funded bounty for verified reports of marketplace policy violations; payouts public; integrates with the Sybil-defense layer.
**Why:** Continuous third-party policing.
**Prereq:** 187.
**Effort:** M.

### S207. Standard ZKAC ↔ ZKAC Trade Format ⛰
**Acceptance:** A canonical schema for an inter-ZKAC trade encodes (charter alignment proof from Calm Pact, value-alignment vector subset from Phase IX, mutual scope binding from S143, settlement receipt from S192).
**Why:** Day-one interop format.
**Prereq:** 116, 143, 192.
**Effort:** L.

### S208. Smart-Contract Migration Plan ⛰
**Acceptance:** A document describes how Phase XIII primitives map to existing smart-contract systems (Ethereum, Cosmos, …) for principals who want on-chain commerce; mapping is one-way (Calm → SC) by default.
**Why:** Existing chains exist; bridging without absorbing is the migration story.
**Prereq:** 192, 200.
**Effort:** L.

---

## Phase XIV — Governance (Summits 209–223, 15 summits)

The protocol cannot self-govern. Phase XIV builds the explicit institutions.

### S209. Predicate Review Board Operating Rules ⛰
**Acceptance:** Rules of order for the board (Everest 54), quorum, conflict-of-interest recusal, public minutes, sanctions for misconduct.
**Why:** Process discipline upstream of decisions.
**Prereq:** Everest 54.
**Effort:** M.

### S210. Vocabulary Governance Ceremony ⛰
**Acceptance:** Procedure for proposing + adopting a new term in any controlled vocab (affect, alignment, predicate-id namespace); ≥30-day public comment.
**Why:** Vocab changes have downstream effects.
**Prereq:** 132.
**Effort:** M.

### S211. Deprecation Timeline Spec ⛰
**Acceptance:** Deprecations follow a fixed timeline: announcement → migration window → sunset. Predicate consumers receive timed warnings.
**Why:** Surprise sunset breaks deployed systems.
**Prereq:** 209.
**Effort:** S.

### S212. Tombstone Process ⛰
**Acceptance:** A predicate found to be harmful (e.g. correlates with protected category in violation of S105) is tombstoned with public reason; old proofs verifiable but new proofs blocked.
**Why:** Some predicates need to be retired with prejudice.
**Prereq:** 211.
**Effort:** S.

### S213. Emergency-Stop Protocol ⛰
**Acceptance:** A super-quorum of governance bodies may pause new disclosures for a defined window (e.g. during a discovered vulnerability); pause is itself chained and time-bounded.
**Why:** Emergencies need an off switch.
**Prereq:** 209, 132.
**Effort:** M.

### S214. Migration Governance ⛰
**Acceptance:** Major version migrations (v0 → v1) require a governance vote + a public migration plan + a parallel-operation window.
**Why:** Substrate migration is the highest-stakes event class.
**Prereq:** 209.
**Effort:** M.

### S215. Counterparty Obligation Enforcement ⛰
**Acceptance:** When a counterparty violates an obligation contract (Everest 66), the violation is provable from receipts; sanctions catalog is published.
**Why:** Obligations without enforcement are aspirational.
**Prereq:** Everest 66.
**Effort:** L.

### S216. Sanctioned-Operator List ⛰
**Acceptance:** A public list of operators barred from issuing Calm Witness disclosures; principals can verify a counterparty is not on the list; appeal process documented.
**Why:** Bad-actor exclusion needs an explicit interface.
**Prereq:** 209, 215.
**Effort:** M.

### S217. Appeals Process ⛰
**Acceptance:** Decisions of governance bodies are appealable to a higher quorum; appeal outcomes are publicly recorded.
**Why:** Without appeal, governance becomes star-chamber.
**Prereq:** 209.
**Effort:** M.

### S218. Predicate Owners-of-Record ⛰
**Acceptance:** Each predicate has a named owner-of-record responsible for updates; ownership transfers are recorded; orphaned predicates auto-deprecate.
**Why:** Ownership accountability prevents predicate decay.
**Prereq:** 127.
**Effort:** S.

### S219. External Audit Rotation ⛰
**Acceptance:** External audits (per Everest 90) rotate between named firms on a published schedule; same firm cannot serve consecutive audits.
**Why:** Audit-capture defense.
**Prereq:** Everest 90.
**Effort:** M.

### S220. Governance Compensation Disclosure ⛰
**Acceptance:** Board members + officers disclose compensation arrangements; conflict-of-interest declarations are public.
**Why:** Governance funded in secret is governance compromised in secret.
**Prereq:** 209.
**Effort:** S.

### S221. Cross-Org Governance Treaty ⛰
**Acceptance:** Calm + sibling protocol orgs (CredexAI, Sigsum operators) sign a treaty defining boundaries + dispute resolution.
**Why:** Multiple sovereign protocols touching the same substrate need explicit interface.
**Prereq:** 209.
**Effort:** L.

### S222. Public Governance Dashboard ⛰
**Acceptance:** A public web interface shows live governance state: open proposals, pending deprecations, sanction list, audit schedule.
**Why:** Transparency is a continuous obligation.
**Prereq:** 209–221.
**Effort:** M.

### S223. Annual Protocol-State Report ⛰
**Acceptance:** A yearly published report describes adoption, incidents, governance changes, financial health of the operating org.
**Why:** Standard accountability cadence.
**Prereq:** 222.
**Effort:** M.

---

## Phase XV — Adversarial Robustness (Summits 224–238, 15 summits)

Continuous red-teaming. Phase X (engineering reliability) covered CI fuzzers; this phase is the ongoing offense-defense program.

### S224. Master Attack Corpus ⛰
**Acceptance:** A versioned corpus of ≥100 named attacks across categories (replay, substitution, fake-compliance, side-channel, governance-capture, vouching-ring, …) with exemplar payloads.
**Why:** Without enumeration, defense is ad hoc.
**Prereq:** Everest 21 (fraud taxonomy).
**Effort:** L.

### S225. Standing Red-Team Protocol ⛰
**Acceptance:** A schedule + rules of engagement for an ongoing red team that attempts ≥1 documented attack per month; reports go public after a ≥30-day fix window.
**Why:** Red-teaming as continuous practice.
**Prereq:** 224.
**Effort:** L.

### S226. Cross-Implementation Conformance Suite ⛰
**Acceptance:** Test vectors that conforming implementations must pass; ≥3 implementations from non-Calm orgs cross-verify on the suite.
**Why:** Conformance is what makes Calm a standard rather than a product.
**Prereq:** Everest 95.
**Effort:** L.

### S227. Mutation-Test Harness ⛰
**Acceptance:** CI generates random mutations of canonical messages + asserts the verifier rejects them; coverage ≥95% of code paths.
**Why:** Verifier robustness must scale beyond hand-written tests.
**Prereq:** Everest 94.
**Effort:** M.

### S228. Fuzz-Target Catalog ⛰
**Acceptance:** Every public parser (chain record, predicate proof, disclosure envelope, vouch, settlement receipt) has a registered fuzz target; CI runs them continuously.
**Why:** Parsers are the easiest attack surface.
**Prereq:** Everest 94.
**Effort:** M.

### S229. Side-Channel Test Suite ⛰
**Acceptance:** Timing + memory + power side-channel tests run against the reference impl on a representative device; high-severity findings are remediated within N days.
**Why:** Local-first means side-channels are the threat.
**Prereq:** Everest 90.
**Effort:** XL.

### S230. Replay-Resistance Proofs ⛰
**Acceptance:** Formal proofs (not just tests) that each freshness mechanism (Roughtime, Sigsum, counterparty nonce, chain head) defeats the named replay attacks in the corpus.
**Why:** Replay is the most common subtle attack.
**Prereq:** 224.
**Effort:** L.

### S231. Coercion-Resistance Posture Review ⛰
**Acceptance:** Annual review of which coercion attacks the protocol does and does not defend against; updates the disclosed posture and the principal explainer.
**Why:** Coercion landscape evolves.
**Prereq:** Everest 69.
**Effort:** M.

### S232. Compromised-Operator Recovery ⛰
**Acceptance:** Procedure for a principal to detect, prove, and recover from a compromised operator: enumerate disclosures issued under compromised state, withdraw them, rotate keys, re-enroll.
**Why:** Compromise is when. Recovery is the test.
**Prereq:** 146.
**Effort:** L.

### S233. Substitution-Attack Catalog ⛰
**Acceptance:** A subset of the master attack corpus specific to substitution attacks (template swap, biometric replay, principal-identity confusion); each with documented defense per S46 / S47 / S134.
**Why:** Substitution is the load-bearing class.
**Prereq:** 224.
**Effort:** M.

### S234. Bounty Program Operating Rules ⛰
**Acceptance:** Standing public bug bounty: scope, payout grid, response time SLA, public hall of payouts.
**Why:** Crowdsourced offense.
**Prereq:** Everest 97.
**Effort:** M.

### S235. Conformance Certification Authority ⛰
**Acceptance:** Named third-party authority certifies implementations; certifications expire on a schedule and require recertification.
**Why:** Certification without expiry is a one-time stamp.
**Prereq:** 226.
**Effort:** L.

### S236. Per-Predicate FAR/FRR Tracking ⛰
**Acceptance:** Per-predicate live false-accept and false-reject statistics computed against a continuous evaluation corpus; deprecation triggered if either exceeds threshold.
**Why:** Predicate quality must be measured, not assumed.
**Prereq:** 119.
**Effort:** L.

### S237. Privacy-Side Test Suite ⛰
**Acceptance:** A suite of tests verifies the protocol leaks nothing beyond the declared bit + freshness for every named predicate. Includes information-theoretic checks where applicable.
**Why:** The hiding property is the protocol's primary product; it must be tested.
**Prereq:** Everest 59 (ZK property test).
**Effort:** L.

### S238. Adversarial-Verifier Test Suite ⛰
**Acceptance:** Tests that a malicious verifier cannot extract anything more from a proof than what the predicate semantics permit.
**Why:** Soundness against malicious verifiers, not just curious ones.
**Prereq:** Everest 59.
**Effort:** L.

---

## Phase XVI — Standards-Body Protocols (Summits 239–248, 10 summits)

The protocol's adoption ceiling is the standards-body path. Phase XVI builds the on-ramp.

### S239. IETF Draft v1 Submission ⛰
**Acceptance:** A complete IETF draft (datatracker-ready) covering Calm Pact v0.1, Calm Witness v0.1, the disclosure envelope, the predicate registry interface.
**Why:** Standards bodies are the path from "feature" to "infrastructure."
**Prereq:** Everest 99.
**Effort:** XL.

### S240. W3C Verifiable Credential Mapping ⛰
**Acceptance:** Document showing how each Calm primitive (operator identity, principal identity, consent record, disclosure envelope) maps to W3C VC data model — and where it deliberately extends.
**Why:** W3C VC has adoption momentum; mapping is the on-ramp.
**Prereq:** 239.
**Effort:** L.

### S241. NIST AI Safety Submission ⛰
**Acceptance:** A submission to NIST AI Safety Institute proposing Calm Witness as a candidate standard for autonomous-agent user-state attestation; submission includes empirical adoption + interoperability data.
**Why:** Public-sector adoption requires public-sector engagement.
**Prereq:** Everest 91, 239.
**Effort:** L.

### S242. ISO Liaison ⛰
**Acceptance:** A liaison relationship established with the appropriate ISO subcommittee for AI / privacy / identity; first liaison report filed.
**Why:** International adoption goes through ISO.
**Prereq:** 239.
**Effort:** L.

### S243. Public Reference Implementation ⛰
**Acceptance:** ≥2 reference implementations published, in distinct languages (Python + Rust), Apache 2.0 license, reproducible build.
**Why:** Standards without implementations are theology.
**Prereq:** Everest 92, 81.
**Effort:** XL.

### S244. Public Test Vector Repository ⛰
**Acceptance:** Versioned canonical test vectors (chain records, predicate evaluations, disclosure envelopes) hosted at a stable public URL; implementations must reproduce.
**Why:** Test vectors are the standards body's continuity guarantee.
**Prereq:** 243.
**Effort:** M.

### S245. Interop Plugfest Protocol ⛰
**Acceptance:** A scheduled interop plugfest event lets implementers exchange messages and verify cross-impl compatibility; minutes published.
**Why:** Plugfests are how standards bodies tighten specs.
**Prereq:** 243, 244.
**Effort:** L.

### S246. Implementation Maturity Rubric ⛰
**Acceptance:** A rubric scores implementations on (test coverage, conformance suite pass rate, side-channel review, security advisories handled, governance commitments). Implementations self-report; community verifies.
**Why:** Maturity differentiation lets adopters pick wisely.
**Prereq:** 226, 243.
**Effort:** M.

### S247. Registry of Public Operators ⛰
**Acceptance:** A public registry of organizations operating Calm-compliant agents; each entry includes maturity score + sanction status.
**Why:** Counterparties need to find legitimate operators.
**Prereq:** 246.
**Effort:** M.

### S248. Standards-Track Charter for Calm Foundation ⛰
**Acceptance:** A neutral non-profit (Calm Foundation) holds the standards-track stewardship; bylaws + governance + funding model published.
**Why:** Long-term standards stewardship cannot live inside one company.
**Prereq:** 239, Everest 84.
**Effort:** XL.

---

## Phase XVII — Onboarding & Education (Summits 249–258, 10 summits)

The protocol is useless if no one can adopt it. Phase XVII builds the human interface.

### S249. Principal Onboarding Animation ⛰
**Acceptance:** A ≤90-second animation explains the protocol to a non-technical principal: what they enroll, what they share, what they keep private; readable at 8th-grade level.
**Why:** Onboarding-quality bound on adoption.
**Prereq:** Everest 82.
**Effort:** M.

### S250. Counterparty Integration Tutorial ⛰
**Acceptance:** A step-by-step tutorial gets a counterparty operator from "no code" to "verifies first proof" in ≤60 minutes; includes sample code + sandbox.
**Why:** Counterparty side is where most integration friction lives.
**Prereq:** 243.
**Effort:** L.

### S251. ZKAC Bootstrap Kit ⛰
**Acceptance:** A bundle of templates (charter, role definitions, ceremonial scripts, sample chain) lets a new ZKAC bootstrap in ≤1 day.
**Why:** Day-one adoption needs day-one assets.
**Prereq:** 173.
**Effort:** L.

### S252. Auditor Onboarding ⛰
**Acceptance:** A specific curriculum + sandbox + certification for third-party auditors of Calm-compliant implementations.
**Why:** Auditor supply is the ecosystem bottleneck.
**Prereq:** Everest 90.
**Effort:** L.

### S253. Developer SDK Tutorials ⛰
**Acceptance:** A series of tutorials (Python, Rust, JS) covering the top-10 developer use cases; each runs end-to-end in a documented dev env.
**Why:** SDK ergonomics drives adoption.
**Prereq:** Everest 84.
**Effort:** L.

### S254. Operator Certification Program ⛰
**Acceptance:** A formal certification (exam + practical) for operators wanting to issue Calm Witness disclosures in regulated settings.
**Why:** Operator-side bar is what regulators ask for.
**Prereq:** 234, 235.
**Effort:** L.

### S255. Public Demo Suite ⛰
**Acceptance:** A hosted demo suite where prospective adopters can run "bank teller note," "alignment disclosure," "ZKAC merger" scenarios end-to-end without local install.
**Why:** Show-don't-tell sells.
**Prereq:** 243.
**Effort:** M.

### S256. Conference Talk Curriculum ⛰
**Acceptance:** A talk track (slides + transcript + Q&A prep) ready for industry + academic audiences; presented at ≥3 events per year by ≥3 different speakers.
**Why:** Mindshare requires repeat presence.
**Prereq:** Everest 91.
**Effort:** M.

### S257. Academic Course Material ⛰
**Acceptance:** A semester-long syllabus on Calm Witness + ZKACs; co-authored by ≥1 university-affiliated researcher.
**Why:** Next-generation builders learn it in school.
**Prereq:** 239.
**Effort:** L.

### S258. Newcomer-Friendly Issue Tracker ⛰
**Acceptance:** Public issue tracker with ≥20 "good-first-issue" tagged tasks; new contributors receive mentorship from a named maintainer.
**Why:** Contributor pipeline is the long-term health metric.
**Prereq:** 243.
**Effort:** S.

---

## Phase XVIII — Sunset & Archival (Summits 259–268, 10 summits)

Things end. The protocol must end gracefully.

### S259. Death-of-Principal Protocol Detail ⛰
**Acceptance:** Procedure for a principal's nominated successor (Everest 88) to: archive the historical chain; mark the principal's predicate disclosures as historical; settle outstanding contracts.
**Why:** Mortality is universal. The protocol should be humane about it.
**Prereq:** Everest 88.
**Effort:** L.

### S260. Inheritance Ceremony ⛰
**Acceptance:** A signed ceremony record transfers the vault's archival authority to a named successor; succession is chain-recorded and witness-signed.
**Why:** Inheritance must be explicit and provable.
**Prereq:** 259.
**Effort:** M.

### S261. Historical Chain Archival Format ⛰
**Acceptance:** Long-term archival format for a principal's chain; preserves verifiability across decades; matches existing archival-format standards (BagIt, Web Archive Consortium).
**Why:** Calm Witness chains will outlive their substrate code.
**Prereq:** 259.
**Effort:** L.

### S262. ZKAC Dissolution Receipts ⛰
**Acceptance:** When a ZKAC dissolves, settlement receipts go to all members; pooled commitments are distributed per the charter; archival of the collective's chain.
**Why:** Closing a collective is itself an operation.
**Prereq:** 163.
**Effort:** M.

### S263. Public-Good Corpus Release ⛰
**Acceptance:** A principal may opt to release portions of their historical chain to a public-good research corpus after a defined privacy window; release is reversible during the window.
**Why:** Research community benefits when principals consent.
**Prereq:** 259.
**Effort:** M.

### S264. Posthumous Attestation Rules ⛰
**Acceptance:** Spec defines what attestations may be issued about a deceased principal (e.g. historical-baseline lookups); requires explicit ante-mortem authorization.
**Why:** Posthumous abuse is real risk.
**Prereq:** 259.
**Effort:** M.

### S265. Data-Minimization Sunset ⛰
**Acceptance:** Per-record sunset: low-value records may be deleted from the chain (with a tombstone record proving deletion was authorized).
**Why:** Indefinite retention is not the only model.
**Prereq:** Everest 8.
**Effort:** M.

### S266. Vault Long-Term-Storage Format ⛰
**Acceptance:** A storage format suitable for ≥50-year retention; tested in archival simulations.
**Why:** Crypto and storage formats both rust.
**Prereq:** 261.
**Effort:** L.

### S267. Cross-Generational Key Recovery ⛰
**Acceptance:** A protocol for an heir to recover access to an archived vault under specific legal + cryptographic conditions; key splits with cryptographic and human-judge thresholds.
**Why:** Single-key custody breaks at one generation.
**Prereq:** 259, 260.
**Effort:** XL.

### S268. Operator Sunset Migration ⛰
**Acceptance:** When an operator org sunsets, principals may migrate their vaults to a successor operator with continuity proofs.
**Why:** Operator orgs don't last forever.
**Prereq:** Everest 87.
**Effort:** L.

---

## Phase XIX — Cross-Jurisdiction (Summits 269–278, 10 summits)

Calm operates internationally. Phase XIX is the legal-posture-by-jurisdiction layer.

### S269. US Legal Posture v1 ⛰
**Acceptance:** Signed memo from US counsel covers GDPR-equivalent obligations, ADA/cognitive-disability posture, FCRA, state-level variations (CA, NY, IL biometric).
**Why:** US adoption requires US-specific clarity.
**Prereq:** Everest 76, 78, 79.
**Effort:** L.

### S270. EU / GDPR Posture v1 ⛰
**Acceptance:** Signed memo covers GDPR data-minimization, Article 22 automated-decision, AI Act (where applicable), DSA obligations.
**Why:** EU has the most demanding privacy regime; explicit posture is mandatory.
**Prereq:** Everest 76.
**Effort:** L.

### S271. UK Posture v1 ⛰
**Acceptance:** Signed memo covers UK GDPR + DPA 2018 + Online Safety Act.
**Why:** UK divergence from EU is now permanent.
**Prereq:** 270.
**Effort:** M.

### S272. Japan / Korea Posture ⛰
**Acceptance:** Memos for Japan (APPI) and Korea (PIPA) cover behavioral-data + cross-border-transfer requirements.
**Why:** Asia-Pacific adoption.
**Prereq:** 270.
**Effort:** L.

### S273. Cross-Border Disclosure Rules ⛰
**Acceptance:** Spec defines what happens when a principal in jurisdiction A discloses to a counterparty in jurisdiction B; choice-of-law clauses; data-transfer mechanisms.
**Why:** Cross-border is the actual production case.
**Prereq:** 269–272.
**Effort:** L.

### S274. Multi-Jurisdiction Operator Spec ⛰
**Acceptance:** An operator serving multiple jurisdictions enforces the per-jurisdiction stricter rule per-principal; per-jurisdiction operator registration is required.
**Why:** Operators must localize legally even if they globalize technically.
**Prereq:** 273.
**Effort:** L.

### S275. Treaty-Level Recognition Path ⛰
**Acceptance:** Document outlining what mutual-recognition treaty between jurisdictions would streamline cross-border Calm operation; preliminary diplomatic engagement.
**Why:** Long-term, treaty-level recognition is the ideal state.
**Prereq:** 273.
**Effort:** XL.

### S276. Sanctions-Compliance Posture ⛰
**Acceptance:** Calm enforces standard sanctions lists (OFAC, EU, UN) at the operator level; principals on lists cannot operate; principals on the wrong end of sanctions get explicit guidance.
**Why:** Compliance is a non-negotiable.
**Prereq:** 171.
**Effort:** L.

### S277. Encrypted-Cross-Border Transit ⛰
**Acceptance:** Spec defines how chain segments + disclosures move across borders encrypted; key custody complies with each jurisdiction.
**Why:** Cross-border data transit is a regulated technical operation.
**Prereq:** 273.
**Effort:** L.

### S278. Per-Jurisdiction Right-to-Erasure Spec ⛰
**Acceptance:** Right-to-erasure (where applicable) is implemented via tombstone records that satisfy the regulatory mechanism while preserving chain integrity for non-erased data.
**Why:** Append-only ≠ unable to comply with erasure.
**Prereq:** 265.
**Effort:** L.

---

## Phase XX — Hardware Integration (Summits 279–288, 10 summits)

Hardware-rooted security is the long-term defense.

### S279. HSM-Bound Operator Key ⛰
**Acceptance:** Operator identity key is HSM-bound; certificate carries an HSM attestation; software cannot extract the key.
**Why:** Software-only operator keys are exfiltrable.
**Prereq:** Everest 16.
**Effort:** L.

### S280. TPM Attestation Spec ⛰
**Acceptance:** Operator host can attest its boot state via TPM; counterparty can verify the operator runs the expected software stack.
**Why:** Boot-state attestation is the cleanest "I'm running what I claim" proof.
**Prereq:** 279.
**Effort:** L.

### S281. iOS Secure Enclave Integration ⛰
**Acceptance:** Principal vault key material may live in iOS Secure Enclave; reference impl in the Calm iOS app.
**Why:** iOS adoption requires Secure-Enclave-native flow.
**Prereq:** Everest 16.
**Effort:** XL.

### S282. Android TEE Integration ⛰
**Acceptance:** Same for Android Trusted Execution Environment.
**Why:** Same.
**Prereq:** 281.
**Effort:** XL.

### S283. USB Hardware-Token Support ⛰
**Acceptance:** Operator + principal keys may live on FIDO2 / YubiKey hardware; reference impl + UX.
**Why:** Hardware-token UX is mainstream.
**Prereq:** 279.
**Effort:** L.

### S284. HW-Rooted ZKAC Treasury ⛰
**Acceptance:** ZKAC treasury N-of-M multisig may require ≥k signers to use HW tokens.
**Why:** Treasury security is worth hardware.
**Prereq:** 165, 283.
**Effort:** L.

### S285. Cross-Device Sync Via HW Attestation ⛰
**Acceptance:** Multi-device vault sync uses HW attestation to verify device identity at sync time.
**Why:** Lost-device threat model.
**Prereq:** Everest 86, 280.
**Effort:** L.

### S286. Open-Hardware Token Spec ⛰
**Acceptance:** A spec for an open-hardware token compatible with Calm; reference design (e.g. Tillitis-class) published.
**Why:** Avoids vendor capture of the hardware-trust layer.
**Prereq:** 283.
**Effort:** XL.

### S287. Tamper-Evident Storage Adapter ⛰
**Acceptance:** Vault may be stored on tamper-evident hardware (e.g. encrypted USB with epoxy seal); evidence of tamper is a chain event.
**Why:** Physical compromise of the vault should be detectable.
**Prereq:** 280.
**Effort:** L.

### S288. Hardware Audit / Certification Path ⛰
**Acceptance:** Procedure to certify hardware tokens + HSMs for Calm use; certification expires + renews per the standard rotation.
**Why:** Hardware-trust layer needs the same audit discipline.
**Prereq:** 235, 283.
**Effort:** L.

---

## Phase XXI — Post-Quantum Migration (Summits 289–293, 5 summits)

Q-day is not soon, but the migration plan is needed now.

### S289. PQ Commitment-Scheme Selection ⛰
**Acceptance:** A signed analysis selects a PQ commitment scheme (lattice-based, hash-based); v1 reference implementation.
**Why:** Pedersen + DLOG breaks at Q-day. Substitute must be ready.
**Prereq:** Everest 89.
**Effort:** L.

### S290. PQ Σ-Protocol Replacement ⛰
**Acceptance:** PQ-secure proof-of-knowledge primitive selected; v1 implementation.
**Why:** Σ-protocol on classical groups breaks at Q-day.
**Prereq:** 289.
**Effort:** XL.

### S291. PQ Range Proof Replacement ⛰
**Acceptance:** PQ-secure range proof selected; v1 implementation.
**Why:** Range proof on classical groups breaks at Q-day.
**Prereq:** 289.
**Effort:** XL.

### S292. PQ Migration Ceremony ⛰
**Acceptance:** Procedure for migrating a live vault from classical to PQ commitments without invalidating historical disclosures; published timeline.
**Why:** Live migration is the hard part.
**Prereq:** 289–291.
**Effort:** L.

### S293. Hybrid Classical-PQ Intermediate Mode ⛰
**Acceptance:** Operators may produce dual proofs (classical + PQ) during the migration window; counterparties may verify either or both.
**Why:** Migration takes years; both modes must coexist.
**Prereq:** 289.
**Effort:** L.

---

## Phase XXII — Transparency-Log + Clock Diversification (Summits 294–303, 10 summits)

The Sigsum + Roughtime ecosystems are too thin (per `reference_calm_witness_research_findings`). Diversification is critical infra.

### S294. N-of-M Witness Governance ⛰
**Acceptance:** A spec defining how the named Sigsum witness set is chosen, governed, rotated; minimum independence requirements (no shared parent org).
**Why:** Sigsum's `2025-1` policy has 3 witnesses all from one parent. That's not actual independence.
**Prereq:** Everest 30.
**Effort:** M.

### S295. Secondary Transparency-Log Adapter ⛰
**Acceptance:** Adapter so chain heads can additionally be published to static-CT-API / tlog-tiles instances (Cloudflare Azul, etc.); verifier can require ≥1 hit on each platform.
**Why:** Single-platform transparency is single-point-of-failure transparency.
**Prereq:** Everest 30.
**Effort:** L.

### S296. Cross-Log Inclusion Proof ⛰
**Acceptance:** Verifier can require a chain head be present in ≥k of N specified transparency logs; failure on any logged is detectable.
**Why:** Defense-in-depth on the anchor layer.
**Prereq:** 295.
**Effort:** L.

### S297. Roughtime Quorum Scaling ⛰
**Acceptance:** Verifier accepts ≥k of N independent Roughtime servers (currently 4 known); spec defines onboarding new servers.
**Why:** 4 servers across 3 organizations is below the quorum bar.
**Prereq:** Everest 31.
**Effort:** M.

### S298. OpenTimestamps Anchor Adapter ⛰
**Acceptance:** Optional anchor: chain head published to Bitcoin via OpenTimestamps; verifier can require Bitcoin-anchored timestamp for high-stakes proofs.
**Why:** Strongest non-repudiation available; complements Roughtime.
**Prereq:** 295.
**Effort:** L.

### S299. Log-Operator Certification ⛰
**Acceptance:** A certification program for log operators (Sigsum, tlog-tiles); requirements + recertification cadence.
**Why:** Avoids operator-quality dispersion.
**Prereq:** 294.
**Effort:** L.

### S300. Witness-Rotation Ceremony ⛰
**Acceptance:** Procedure to add or remove a witness from the named set without invalidating in-flight proofs.
**Why:** Witness sets change.
**Prereq:** 294.
**Effort:** M.

### S301. Per-Region Anchor Sets ⛰
**Acceptance:** Multiple named anchor sets (US, EU, AP) reflect regional trust requirements; counterparty may specify which region's set is acceptable.
**Why:** Cross-jurisdiction trust requires regional anchor sovereignty.
**Prereq:** 296, 297.
**Effort:** L.

### S302. Anchor Failover Protocol ⛰
**Acceptance:** When a named anchor (witness, Roughtime server) becomes unreliable, automatic failover to backup with chain-recorded provenance of the failover.
**Why:** Liveness of the anchor layer must survive single-operator outages.
**Prereq:** 295, 297.
**Effort:** L.

### S303. Anchor-Layer Adversarial Test Corpus ⛰
**Acceptance:** Attack catalog specific to the anchor layer (log forks, witness collusion, Roughtime spoofing, OpenTimestamps reorg); each attack has a documented defense.
**Why:** Anchor-layer threats are protocol-foundational.
**Prereq:** 224.
**Effort:** L.

---

## Climbing-order notes

- **Headline (Phase IX) is the artist's commission.** Bag 104–115 first to ratify the values-alignment family; that's where John pushed.
- **Phase X (agent attestation) is the trust-graph prereq for Phases XI–XIII.** Bag 134–138 early in parallel.
- **Phases XI–XIII compose into the production ZKAC commerce stack.** They depend on Phases IX–X but their internal order is flexible.
- **Phase XIV (governance) is a parallel always-on track from S104 forward.** Governance must precede deployment, not follow.
- **Phase XV (adversarial) is climbed every month** as continuous practice, not as a one-shot.
- **Phase XVI (standards) is the long pole.** Start S239 alongside S104 even though it lands later.
- **Phases XVII–XX (onboarding, sunset, jurisdiction, hardware) are deployment-blockers** — bag the relevant subset before any production rollout in that surface.
- **Phases XXI–XXII are continuous infrastructure tracks.** Q-day prep + anchor diversification are years-long programs.

## Critical-path subset for the next 200 (the "MVP-2 expedition")

If we could only bag **18 of these 200** and call the next epoch shipped:

**104, 106, 107, 108, 110, 116, 117, 134, 135, 154, 156, 174, 209, 224, 239, 243, 270, 294.**

That gives us: alignment charter + vocab v1 + ≥2 working alignment predicates + multi-bit envelope + per-dimension consent + agent identity + agent handshake + ZKAC charter + multi-principal vault + vouching + governance ops + attack corpus + IETF draft + 2nd reference impl + EU posture + diversified transparency anchor. The other 182 are deepening, hardening, and broadening that minimum.

## Status table

```
Phase IX    : ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0 / 30   values-alignment predicates
Phase X     : ░░░░░░░░░░░░░░░░░░░░  0 / 20   mutual agent attestation
Phase XI    : ░░░░░░░░░░░░░░░░░░░░  0 / 20   ZKAC organizational primitives
Phase XII   : ░░░░░░░░░░░░░░░  0 / 15   trust networks
Phase XIII  : ░░░░░░░░░░░░░░░░░░░░  0 / 20   commerce primitives
Phase XIV   : ░░░░░░░░░░░░░░░  0 / 15   governance
Phase XV    : ░░░░░░░░░░░░░░░  0 / 15   adversarial robustness
Phase XVI   : ░░░░░░░░░░  0 / 10   standards-body protocols
Phase XVII  : ░░░░░░░░░░  0 / 10   onboarding & education
Phase XVIII : ░░░░░░░░░░  0 / 10   sunset & archival
Phase XIX   : ░░░░░░░░░░  0 / 10   cross-jurisdiction
Phase XX    : ░░░░░░░░░░  0 / 10   hardware integration
Phase XXI   : ░░░░░  0 / 5    post-quantum migration
Phase XXII  : ░░░░░░░░░░  0 / 10   transparency-log + clock diversification

Total: 0 / 200 next-route summits bagged.
```

## Cross-references

- Original route map: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) — substrate (E1–E101+).
- Protocol spec: [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md).
- Predicate vocab: [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md) — to be extended by S106 (alignment vocab).
- Calm Pact: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md) — directive equality primitive.
- Path B ratification: [`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`](CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md).
- v0 status audit: [`ROUTE_MAP_CONSISTENCY_AUDIT_2026-05-20.md`](ROUTE_MAP_CONSISTENCY_AUDIT_2026-05-20.md).
- Research basis: `[[reference-calm-witness-research-findings]]` in CALM auto-memory.

---

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Released for ratification, refinement, and climbing.**
