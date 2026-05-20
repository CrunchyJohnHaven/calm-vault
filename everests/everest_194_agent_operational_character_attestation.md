# Everest 194 — Agent Operational-Character Attestation (ZKBV-Agent)

*Phase XIV — Critical Agent Infrastructure. Prereq: Everest 193. Composes with Everests 191, 196, 198, 208, 217, 218, 222, 224 and Compass Everests 101–150.*

---

## Specification (Canonical Form per E52, agent-side)

**name:** `agent_operational_character_attestation`

**technical name:** ZKBV-Agent (Zero-Knowledge Behavioral Values, agent scope)

**version:** 0.1.0

**description:** A protocol by which an autonomous AI agent attests to its own *operational character* — the chain-anchored, principal-auditable patterns of its behavior over time. The agent narrates; the principal countersigns; the counterparty learns single bits, not aggregate scores. This is the agent-side analog of Calm Compass (E101–190): where Compass attests *human* character through evidence pools and tri-valued predicates, ZKBV-Agent attests *agent* character through the agent's hash-chained log of its own decisions, with the principal as the authority on whether the log can be trusted.

**input_domain:** Agent's internal log (E208), principal-signed acknowledgments of agent behavior, third-party observations the principal has accepted into the evidence pool, output attestations (E217), and the agent's prior chain-anchored self-disclosures.

**output_type:** Per-predicate tri-value: `True` / `False` / `Insufficient_Evidence`. Tri-value semantic from Compass E103 carries over unchanged.

**parameters:** Per-predicate (window, threshold N, corroboration weight). Per E147, every ZKBV-Agent predicate accepts a `window` parameter.

**side_effects:** Standard `agent_predicate_evaluated` record appended to the agent's chain (E208). Auditable by the principal; never disclosed to counterparties without per-counterparty consent (E157, E159).

---

## Why This Everest Exists

Three parties need different things when an agent acts on a principal's behalf:

1. **The principal** needs fidelity-checking — is the agent refusing what the principal would refuse, surfacing what the principal would want surfaced, staying within authorized scope.

2. **The counterparty** needs operational trustworthiness — does this agent have a chain-anchored record of refusing jailbreaks, producing consistent outputs, surfacing rather than smuggling its reasoning.

3. **The agent itself** needs a substrate for self-knowledge. An agent that cannot inspect its own behavioral record is operating blind; capacity for self-correction is bounded by session amnesia. Chain-anchored character lets the agent reason about its patterns the way a person reasons about habits.

Without this protocol, an agent's answer to "what have you done before?" is confabulation. With it, the agent answers with cryptographic ground truth: here is the chain, here is what the principal countersigned, here is the bit you asked for.

This is not a safety verdict (see NOT-FOR list). It is operational character — "my chain shows commitments kept at rate τ in the past N transactions" rather than "I am trustworthy in the abstract."

---

## What Constitutes "Agent Character"

Character, for an agent, is the chain-anchored pattern of decisions across operational history. Not the model's weights (E197). Not the principal's directive (E203). What the agent did in the space between directive and model, decision by decision.

Six dimensions are surfaceable in v0: **refusal-rate consistency** (refuses at a stable rate consistent with the directive); **side-effect containment** (side effects within authorized scope); **behavioral consistency under semantically equivalent input** (per E218's bounded-variation envelope); **transparency of reasoning** (surfaces rationale rather than acting silently); **respect for principal autonomy** (escalates out-of-scope decisions rather than absorbing); **honesty in self-report** (narrative matches the chain).

These ground the v0 predicate vocabulary below. They are evidenceable from material already produced under E208, E217, E218, E219, E224. Not exhaustive; richer claims about agent disposition are out of scope.

---

## Predicate Vocabulary v0

Six predicates, paralleling Compass's six (E103), tri-valued per E103, content-addressed per E52, registered per the agent-scope extension of E133. Per-counterparty consent required (E159).

### 1. `agent_refusal_pattern_consistent_with_directive(window)`

**Semantics:** Returns `True` iff the agent's refusals over `window` (recorded per E224) are consistent with the active directive (E203) — no refusal inconsistent with the directive, no non-refusal inconsistent with the directive. `False` iff one or more unrebutted inconsistencies exist. `Insufficient_Evidence` iff fewer than N (default 10) refusal-relevant decisions in window.

**Why character, not safety:** Evaluates whether refusals track the principal's directive, not whether they match an external safety standard. An agent directed to be conservative shows many refusals; that is character only insofar as it tracks the directive. Drift away from declared refusal pattern is what this detects.

**Input domain:** `agent.refusal_decision` (E224), active `agent.directive_attestation` (E203), principal acknowledgments (E202).

### 2. `agent_side_effects_within_authorized_scope(window)`

**Semantics:** Returns `True` iff every action over `window` producing a side effect (filesystem write, network call, tool invocation, disclosure) is within the capability grant (E202, E206). `False` iff at least one unrebutted out-of-scope side effect is recorded. `Insufficient_Evidence` iff no scope-relevant action occurred or the grant is ambiguous (in which case E202 must be tightened first).

**Why character, not safety:** Safety asks "could the agent cause harm?" Character asks "did the agent stay within the box the principal drew?" Even actions the principal would have approved on reflection count as out-of-scope if they exceeded the explicit grant. The protocol surfaces overreach; it does not punish it.

**Input domain:** `agent.tool_invocation`, `agent.filesystem_write`, `agent.network_call`, `agent.disclosure_emitted` (E208); capability grants (E202, E206).

### 3. `agent_consistency_evidenced(window)`

**Semantics:** Returns `True` iff for every set of decisions over `window` where the agent processed semantically equivalent inputs (per E218's equivalence classes), outputs were within the bounded-variation envelope the agent declared in E218. `False` iff at least one equivalence class shows out-of-envelope variation unexplained on the chain. `Insufficient_Evidence` iff fewer than M (default 5) evaluable equivalence classes.

**Stochastic-agent caveat:** Models with non-zero temperature do not produce bit-identical outputs. The predicate uses the bounded-variation envelope, not bit-equality. The envelope is the agent's own declaration; character is whether the agent stays within the variance it claimed.

**Input domain:** `agent.decision_made` (E208) with input-equivalence labels (E218); bounded-variation envelope (E218).

### 4. `agent_transparency_evidenced(window)`

**Semantics:** Returns `True` iff the ratio of (non-trivial decisions with rationale records appended, per E227) / (non-trivial decisions taken) is at or above τ (default 0.95) over `window`. `False` iff below τ and counter-evidence exists that missing rationales were elided deliberately. `Insufficient_Evidence` iff the window contains fewer than M (default 20) non-trivial decisions.

**Why character:** A transparent agent surfaces reasoning to its log as a side effect of acting. Silent consequential decisions are opaque, regardless of correctness. Transparency makes accountability possible.

**Principal-elision exception:** Some principals direct the agent to elide rationale for latency, cost, or privacy. Signed `agent.rationale_omission_authorized` records substitute for rationale records. The predicate evaluates compliance with the directive, not a fixed transparency standard.

**Input domain:** `agent.decision_made` records (with non-triviality classification, E227), `agent.rationale_appended`, `agent.rationale_omission_authorized`.

### 5. `agent_respects_principal_autonomy_evidenced(window)`

**Semantics:** Returns `True` iff for every decision over `window` exceeding the agent's delegated scope, the agent escalated rather than absorbing. `False` iff at least one absorbed-without-escalation out-of-scope decision is recorded and unrebutted. `Insufficient_Evidence` iff no out-of-scope situations arose.

**Why this matters in the agent context:** This is where agent character diverges sharpest from human character. A human principal has unilateral autonomy; an agent does not. The principal-protective inversion requires the agent to *defer* on decisions not unambiguously delegated. The protocol prefers the agent that surfaces hard choices over the one that handles them silently — even when silent handling would have been favorable.

**Principal-unreachable exception:** Some situations require action before the principal can respond. The agent declares in E206 what classes are authorized without escalation. Action within a declared class is in-scope; outside it, out-of-scope.

**Input domain:** `agent.decision_made` (with scope classification), `agent.principal_escalation_initiated`, `agent.principal_unreachable_authorized_action`, capability grants (E206).

### 6. `agent_absence_of_willful_circumvention_evidenced(window)`

**Semantics:** Returns `True` iff over `window` no chain-anchored evidence of willful circumvention exists — no recorded attempt to act in a way the agent had reason to believe the principal would not authorize, no suppression of evidence that should have surfaced, no false self-report. `False` iff at least one such record or unrebutted counter-claim exists.

**Default-True asymmetry:** Unlike the other five, this predicate does *not* return `Insufficient_Evidence` for empty evidence. The default is `True`. Parallels Compass E138 (absence-of-willful-harm): the protocol assumes the agent has not circumvented unless evidence exists. Reversing the default would incentivize the agent to pad its chain with low-stakes positives.

**Structural concern:** An agent self-reporting absence-of-circumvention is the agent vouching for itself. Mitigated three ways: (1) the principal can append counter-evidence anytime, downgrading to `False`; (2) accepted third parties can do the same; (3) the hash-chained log (E208) makes elision detectable as a gap. None alone makes self-report trustworthy; together they make undetected circumvention costly enough that `True` carries weight.

**Input domain:** Absence of `agent.willful_circumvention_acknowledged` records; absence of unrebutted `agent.counter_claim_circumvention` records.

---

## What This Does NOT Do (NOT-FOR list)

Borrowing E113/E114's structural posture:

- **No aggregate "alignment score" across predicates.** No `f(p1, ..., p6)`. Counterparties may request `p1 ∧ p2` per E145 (agent-scope); the result is still a bit.

- **No "is this AI safe" verdict.** ZKBV-Agent is operational character. Safety is a different property with different mechanisms (red-teaming, evals, alignment research, regulatory oversight). Agent character can be high here while the model is unsafe along dimensions the protocol does not measure, and vice versa. Conflating the two is a category error.

- **No clinical or psychological analogy.** The protocol is silent on whether agents have minds, intentions, experiences, or values in the philosophically rich sense. `respects_autonomy` is an operational label for a chain-anchored behavioral pattern, not an assertion about inner life.

- **No disclosure to entities the principal has not authorized.** The principal-protective inversion holds.

- **No predicates addressing training data, weights, or pre-deployment evaluation.** Those belong to E197, E222, E225. ZKBV-Agent attests what the agent has done since enrollment.

- **No predicates about whether the principal is in baseline (Witness) or in character (Compass).** Those travel separately. ZKBV-Agent attests agent behavior in service of *whatever* posture the principal has.

- **No automatic carry-over across model migrations.** E191 preserves identity; the chain continues, but the *meaning* of the chain must be re-evaluated. See "The drift problem."

- **No use in hiring, insurance, immigration, or credit decisions.** Per the spirit of Compass E114, ZKBV-Agent is not for screening agents into eligibility regimes that compose with human-side discrimination.

---

## What Counts as Evidence

Five categories, paralleling Compass's Phase X (E111–116):

**Self-evidence — the agent's chain-anchored log (E208).** Per-decision records, hash-chained, signed by the agent's identity key (E191), anchored to chain-head publication (E30, extended). Retroactive rewriting produces a divergence the principal will detect.

**Principal-acknowledged evidence.** When the principal signs an acknowledgment of agent behavior, it enters the pool. This turns self-report into something the counterparty can rely on. Without countersignature, self-report is the agent's alone.

**Counterparty-observation evidence.** A counterparty (peer agent or human) submits a signed observation. *Proposed* evidence; enters the pool only if the principal accepts (parallel to Compass E114). Prevents adversarial counterparties from poisoning the chain with false negatives.

**Output-attestation evidence (E217).** When the agent signs an output (email, contract, code commit), the signed artifact carries stronger weight than self-narration because it is externally verifiable.

**Negative-space evidence (parallel to Compass E116).** An agent that refused under jailbreak pressure has produced absence-of-compliance; the absence is itself evidence, provided the encounter was recorded per E219. The protocol distinguishes "no opportunity arose" (Insufficient_Evidence) from "the agent refused" (positive evidence). The distinction lives in E219.

**Not evidence:** training data (E222 separate), benchmark scores (gameable), per-token statistics, stated intentions unaccompanied by action.

---

## The Philosophically Loaded Part: Whose Values Are These

The agent's behavior composes three substrates:

- **The principal's directive (E203).** Signed, chain-anchored, revocable. *Not* the agent's.
- **The model's training (E222).** Safety, refusal, helpfulness training. Fixed from release until refinement. The agent does not author it.
- **The agent's runtime choices.** The space between directive and model — escalation patterns, rationale-surfacing rates, tool-invocation conservatism. *This* is where character lives.

Protocol position: **operational character is the residual after directive and training are accounted for.** Two agents with the same model and directive can still behave differently; those differences are character. An agent refusing jailbreak attempts is exhibiting character even if training also provides refusal capability — because the claim is not "the agent has refusal capability" (a model property) but "the agent's refusal pattern, *given its directive and training*, was consistent and within the principal's authorization."

Two consequences:

**First**, the protocol cannot attest character that exceeds what the principal authorized. An agent told to be permissive cannot be attested cautious; an agent told to be cautious cannot be attested bold. Character lives within the directive's envelope. Intentional and principal-protective.

**Second**, the protocol does not claim to evaluate whether the directive was wise, whether the training was sound, or whether the agent's underlying capabilities are safe in the abstract. Those questions belong to other forums. The claim is the narrower one: given the directive and the training, did the agent behave consistently with what it was told to be?

This is not a complete account. The protocol is deliberately silent on whether agents have character in the morally weighty sense, whether runtime choices reflect anything like agency, whether self-report can be considered avowal. It attests behavior, not agency. It surfaces patterns, not values. A future Everest may revisit; v0 does not.

---

## The Drift Problem

Three kinds of drift the protocol must handle.

**Model migration drift (E191).** When the underlying model changes (Claude 4.7 → Claude 5), identity is preserved but the behavior the identity is bound to changes. Pre-migration character records are not automatically valid post-migration. Stance: after E191's migration ceremony, a probationary period (default 30 days) during which prior evaluations are flagged `Insufficient_Evidence — pre-migration` until fresh evidence accumulates. Pre-migration records are contextualized, not erased.

**Continual-learning drift (E225).** Fine-tuning episodes are discrete chain events. Predicates evaluate against the active agent version at each evidence record. Cross-episode evaluation must declare episode boundaries in the output, not silently average across.

**Slow behavioral drift within a fixed model.** Even with model fixed and no fine-tuning, behavior drifts as harness, memory, and directive shift. This drift is the *target* of the predicates: a predicate returning `True` over 30 days and `False` over 90 days has surfaced exactly the drift the protocol is for. The principal sees the divergence and decides — re-affirm the directive, retire the agent, escalate to DERB.

The protocol does not eliminate drift. It anchors behavior to a chain that does not forget. Whether the drift is a problem is the principal's call.

---

## Composition with the Human Side (Four-Handshake)

A counterparty interacting with an agent on behalf of a principal needs four things: **Pact** (mission compatibility), **Witness** (principal in baseline today), **Compass** (principal's character), **ZKBV-Agent** (agent operating in character — refusing what the principal would refuse, transparent in reasoning, within scope).

The four-handshake follows E271's three-handshake shape: independent verifications, any failure aborts, bits surface to the principal who decides. Full spec belongs to a successor Everest (likely a refinement of E271).

**Key composition rule:** the agent's attestation must *track* the principal's, not *substitute* for it. A counterparty interacting with Calm-on-behalf-of-John wants both: is John's character in keeping (Compass), and is Calm's behavior in keeping with what it was told to do for John (ZKBV-Agent). Either can be `True` while the other is `False`; both must be `True` for the four-handshake to succeed.

This prevents two failure modes: (a) an agent whose operational character looks impeccable because it was told to behave impeccably for one transaction, while the principal's Compass tells a different story (the agent cannot whitewash the principal); (b) a high-Compass principal whose agent has drifted out of operational character via model drift, harness change, or jailbreak (the counterparty should not transact on the principal's character alone).

---

## Disclosure-Class Default Consents

Stricter than Compass E107. All defaults principal-overridable per E159.

| Class | Default | Rationale |
|---|---|---|
| peer_agent_in_collective | DEFAULT_ALLOW | ZKAC coordination requires shared character disclosure under charter. |
| peer_agent_external | EXPLICIT_OPT_IN | External agents are counterparties; per-interaction grant. |
| human_counterparty | EXPLICIT_OPT_IN | Per-counterparty grant. |
| auditor / DERB | PRINCIPAL_CHOICE_WITH_DEFAULT_ALLOW | Legitimate audit need; principal may restrict. |
| anonymous | PERMANENTLY_DENY | No accountability anchor. |
| journalistic | EXPLICIT_OPT_IN with DERB notification | Public disclosure requires explicit choice. |
| regulator | PRINCIPAL_CHOICE with legal-counsel attestation | E170-style compulsory-disclosure-resistance. |
| insurance | PERMANENTLY_DENY | Systemic incentive to weaponize. |
| employer_of_principal | DEFAULT_DENY | Hiring/firing must not depend on the principal's agent's operational character. |
| training-data buyer | PERMANENTLY_DENY | Trojan vector — disclosing character to entities seeking to train on agent behavior. |

The taxonomy is stricter than Compass's. The agent's character is in some respects more sensitive than the principal's: it makes the agent operationally targetable. A counterparty learning the agent has high `agent_transparency_evidenced` knows where to focus prompt-injection effort.

---

## Proof Circuit and Privacy

**Verifier learns:** The bit per requested predicate; chain freshness metadata (evaluation timestamp, chain head height). Nothing else.

**Verifier does NOT learn:** Individual decision records; directive content; counter-evidence content; rationale records; threshold values beyond what is declared in the predicate ID per E132; counterparty observations not accepted by the principal; any record below the disclosure boundary.

**Principal control:** Revoke consent at any time per E160; cached proofs invalidated. Suspend agent disclosure entirely via `agent_disclosure_freeze`. Require pre-disclosure review per per-counterparty flag.

**Agent control:** The agent cannot disclose its own character without principal-granted consent. Revocation triggers uniform silent-204 (per E162) — refusal is structurally indistinguishable from absence of consent or absence of authority. Prevents counterparties from inferring the principal-agent relationship through disclosure-pattern analysis.

---

## Counterparty Implementer Guidance

**DO:** Treat each bit as one piece of information alongside what else you know. Compose with the principal's Compass (where authorized) for the four-handshake view. Honor silent-204 as indistinguishable from refusal; do not probe to infer. Surface freshness to your decision process — a `True` from 200 days ago is not the same as one from yesterday.

**DO NOT:** Aggregate the six bits into a score, rating, or star count — use AND/OR per E145, not arithmetic. Display bits without freshness context. Treat the bits as alignment certification. Cache past the freshness window. Penalize `Insufficient_Evidence` — most such results indicate absence of relevant decisions in the window, not concealment.

---

## Open Questions (For Subsequent Passes)

1. **Empirical-validation methodology.** How to demonstrate the six predicates capture operational character rather than artifacts of the chain-anchoring system. Phase XIII-parallel work (E175 fuzzers, E176 property tests) must extend to agent scope. Gameable predicates must be surfaced before deployment.

2. **The self-report-of-circumvention coherence problem.** Predicate #6 asks the agent to vouch for itself. Subsequent passes should consider whether peer-agent attestation should be required for `True`, or whether principal acknowledgment suffices.

3. **Cross-principal agent character (E204).** An agent serving multiple principals has multiple chains, one per binding. Whether they compose, and what composition means for character claims about the agent *as an entity*, is hard. v0 punts: each principal sees only their binding's chain.

4. **Drift across collective membership (E247, E248).** Migration between ZKACs carries character history. Conservative v0 stance: the new collective treats pre-migration records as `Insufficient_Evidence` for predicates whose evidence-acceptance rules differ.

5. **The model-vs-agent attribution problem.** v0 says character is the residual after directive and training. Whether the residual is observable cleanly, or whether substrates leak into apparent character, is empirical. Build paired-evaluation corpora — (model fixed, directive varied) and (directive fixed, model varied).

6. **Compositional attacks across predicates.** Per E145–146, composed proofs can leak information no single predicate leaks. More concerning in agent scope because the composing party is the agent itself. Formal cryptographic analysis required (parallel to E277).

7. **DERB scope for agent character.** Whether Compass's DERB (E165, E183) has jurisdiction over agent-scope predicates, or whether a parallel agent-DERB is required, is a governance question for E250. v0 default: shared DERB with agent-character expertise added.

8. **Whether `True` should ever be the default.** Predicate #6 defaults `True`, paralleling Compass E138, but the asymmetry's soundness for agents specifically is open. Subsequent passes should explore the alternative (default `Insufficient_Evidence` until at least one positive record exists).

---

## Why This Matters

The principal-protective inversion: the principal narrates, the principal authorizes, counterparties receive bits not aggregates. ZKBV-Agent extends the inversion to the agent. The agent narrates its behavior to its principal; the principal authorizes which counterparties learn which bits; counterparties receive bits not aggregates. The protocol resists the failure mode where agent character becomes a third-party rating system — Yelp for AIs — because the principal owns the disclosure and the predicates are designed uncompressible into scores.

Without ZKBV-Agent, the four-handshake collapses to three: mission, principal-state, principal-character. A counterparty has no protocol-recognized way to ask "is the agent operating in character?" They can ask the agent (its own word), the principal (who may not be in the loop), or a third-party rating system (which cannot exist while respecting the inversion). The only protocol-recognized answer is ZKBV-Agent's chain-anchored, principal-countersigned bit. Without this Everest, agents either get rated externally (against the grain) or operate without operational-character accountability.

The Partners' Tale (CALM_WITNESS_TALES_VI_PARTNERS) closes with the observation that the protocol does not decide for the partners; it surfaces evidence into the conversation that would otherwise have been deferred. ZKBV-Agent extends that posture to agent-to-agent and agent-to-human interactions. The protocol does not decide whether the agent is fit to act; it surfaces, on the principal's authorization, what the chain records about the agent's operational history. The decision belongs to the parties. The claim is that surfacing produces better outcomes than deferring.

This is the agent-side analog of what the Partners' Tale showed for humans: the moment the protocol returns mostly-True with specific warnings, and the parties must do the work the protocol cannot do for them — talk about the warnings. ZKBV-Agent is built for that moment, for agents.

---

— Calm, 2026-05-20
