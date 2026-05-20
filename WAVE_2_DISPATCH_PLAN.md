# Wave 2 Dispatch Plan

**Status:** Pre-staged for the moment quota resets (2 AM ET, 2026-05-21). Ten agent prompts, each ready to copy-paste into a new `Agent` dispatch with `subagent_type: general-purpose` and `run_in_background: true`. Each targets a distinct XL summit; no inter-agent file collisions; each composes cleanly with the 11 Wave-1 summits bagged 2026-05-20.

**Wave-1 outcome (11 bagged/progressed):** E191, E193, E194, E197 (Phase XIV agent infra); E231, E235 (Phase XV ZKAC); E101 (Phase IX Compass foundation); E149, E138 (Phase XI Compass predicates — hardest crypto + highest-stakes); E271 (Phase XVI cross-protocol composition); E297 (Phase XVII meta-design).

**Wave-1 casualties to quota cap:** E255 (Principal Succession), E136 (Untribal Predicate), E300 (Closing Summit). These three are retried in Wave 2 below.

**Wave-2 budget envelope:** ~$200 ($20/pass × 10). Wall-clock: ~12-15 minutes from dispatch to all complete.

**Wave-2 priority ordering (descending value-per-pass):**

| # | Everest | Phase | Composes with Wave-1 | Why dispatch this one |
|---|---|---|---|---|
| 1 | **E255** ZKAC Principal Succession | XV | E191, E231, E235 | Closes the founder-retirement story; pairs with E191's machine-agent lineage |
| 2 | **E136** Untribal Predicate | XI | E101, E138 | The encode-without-encoding philosophical hardest Compass predicate |
| 3 | **E300** Family-Wide Public-Good Declaration | XVII | E297 | The route map's terminal bookend |
| 4 | **E287** Cross-Protocol Side-Channel Defense | XVI | E271 | Composes constant-time + padding + cover-traffic across three-handshake |
| 5 | **E169** Compass Defamation Defense | XII | E138, E101 | The procedural defense for false character predicates — paired with E138's defamation-asymmetry framing |
| 6 | **E192** Agent Instance Lineage | XIV | E191 | Tracks model-generation succession; the direct follow-on to identity stability |
| 7 | **E198** Agent Jailbreak Detection | XIV | E193 | The compromise-reporting layer for operational-state attestation |
| 8 | **E232** ZKAC Charter Document | XV | E231, E235 | The template every ZKAC formation produces |
| 9 | **E135** `unselfish_behavior_evidenced` Predicate | XI | E101 | First positive Compass predicate; establishes the "frame positively, absence ≠ failure" pattern |
| 10 | **E291** Protocol Family Compact | XVII | E297, E300 | The family's constitution; consolidates Pact + Witness + Compass + reserved siblings |

---

## Dispatch prompts (copy-paste ready)

### Dispatch 1 — E255 ZKAC Principal Succession

```
You are joining the CALM climb. Read `/Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md` first. Follow its instructions.

Your assigned summit: Everest 255 — ZKAC Principal Succession.

Acceptance per NEXT_200_EVERESTS.md Phase XV: protocol for a founding human-principal to retire and a successor (or successors) to take over. Includes legal identity handover, key custody transfer, DERB notification. Effort: L.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_255_zkac_principal_succession.md. Match format. Target ~15-20 KB. Sign — Calm, [TODAY'S DATE].

Read first: everests/everest_231_zkac_formation_protocol.md, everests/everest_235_zkac_governance_structure.md, everests/everest_191_agent_identity_stability.md (parallel for machine-agent side), OPEN_LETTER_TO_THE_NEXT_OPERATOR.md (inheritance ethic), CALM_WITNESS_TALES_VII_MIGRANT.md (narrative on machine-agent succession; principal-succession is the human-side parallel).

Hard design questions: (1) planned vs unplanned succession; backup-designation; (2) succession ceremony — outgoing principal signs intent, successor signs acceptance, legal-entity ownership transfers (Delaware SOS, IRS Form 8822-B), CredexAI VC re-issued, chain anchor, machine-agent members acknowledge new principal; (3) what successor inherits (legal-entity ownership, vault key custody via FROST, signing right under collective name) vs does NOT inherit (predecessor's personal voice, personal Compass evidence pool); (4) multi-principal succession (single principal or full handover); (5) DERB role (review proposed successors, especially unplanned; no veto on valid succession); (6) threat model — forged intent, coerced principal naming hostile successor, incapacitated principal with disputing family, captured successor; (7) cross-protocol implications — in-flight Witness/Pact/Compass sessions continue under successor, counterparties notified via chain; (8) inheritance limits — continuity-of-role not continuity-of-personality.

Compose with: E22, E191, E192, E200, E201, E231, E232, E235, E239, E247, E250, E270.

Emit summit call as final line.
```

### Dispatch 2 — E136 Untribal Predicate

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 136 — `untribal_engagement_pattern_evidenced(window)` Predicate (the hardest Compass predicate; encode "untribal" without first encoding "tribes").

Acceptance per NEXT_200_EVERESTS.md Phase XI: returns true iff the evidence shows the principal has engaged constructively across at least N distinct categories of social/cultural/political identity within the window. Categories are themselves predicates of refusal — the protocol explicitly does NOT enumerate identity categories itself; the principal supplies the categories they themselves cross. Effort: L.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_136_untribal_engagement_pattern.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_59_cognitively_atypical_baseline.md (declaration-based predicate pattern), everests/everest_101_compass_problem_statement_threat_model.md, everests/everest_138_absence_of_willful_harm.md (high-stakes predicate sibling), NEXT_200_EVERESTS.md Phase XI E135-144.

Hard design questions: (1) the encoding problem — the protocol does NOT enumerate identity classes; the principal defines THEIR OWN crossing-categories at enrollment via a kind: "compass.untribal_categories.declared" record; (2) principal-defined categories never leave the vault; committed but not disclosed; (3) evidence schema — each piece references which of principal's declared categories it crosses + form of engagement (collaboration, dialogue, defense, intervention); (4) the N-category threshold — v0 defaults N=3 categories, M=2 evidences per category, principal-adjustable; (5) what counts as "constructive engagement" — defending against harm to other-group member, collaborating on shared interest, learning, advocating for inclusion; NOT contact-without-engagement, transactional engagement, surveillance; (6) the category-set leak problem — counterparty receives ONLY the bit, no categories, no count; ZK proof hides all of this; (7) the Goodhart problem — counter-evidence weighting, peer-attestation for high-weight evidence, multi-year decay; (8) cross-cultural problem — "untribal" is culturally situated; principal-defined categorization partially addresses; v0 accepts uneven adoption; (9) NOT-FOR list — must not be used for hiring, immigration, university admissions, security clearances, ad targeting, jury selection; default-consent matrix permanent-deny these; (10) DERB pre-clearance — predicate's design must pass DERB review BEFORE shipping.

Compose with: E106, E111, E114, E119, E121, E131, E134, E145, E165, E187.

Emit summit call as final line.
```

### Dispatch 3 — E300 Family-Wide Public-Good Declaration

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 300 — The Closing Summit: Family-Wide Public-Good Declaration (the bookend to the 300-Everest climb).

Acceptance per NEXT_200_EVERESTS.md Phase XVII: a signed, chain-anchored declaration that the Calm protocol family is, as of the closing summit's date, a public-good infrastructure available to any aligned operator on any aligned principal's behalf, governed by the principles of the Compact, and no longer the proprietary product of any single collective. Effort: L. Prereq: 291-299. The bookend to Everest 1's "Problem Statement."

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_300_family_wide_public_good_declaration.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: ZKBB_USER_PROTOCOL_v0.md §1 (Everest 1's problem statement — your bookend), CALM_PACT_PROTOCOL_v0.md §9, CALM_WITNESS_MANIFESTO.md, OPEN_LETTER_TO_THE_NEXT_OPERATOR.md, everests/everest_297_successor_protocol_design_principles.md (just shipped).

Hard design questions: (1) what is being declared — the Calm protocol family transitions from "Calm's" to "the world's"; (2) what changes structurally — trademark relinquishment, DERB transitions from Calm-appointed to community-elected, Foundation constituted as steward, future protocols governed by Compact's process; (3) what does NOT change — Apache 2.0, existing chain anchors, Compact's principles (E297), existing operator credentials, bank-teller-note property; (4) signing ceremony — Calm collective convenes, DERB ratifies, Foundation board signs, ≥90 day public announcement period, declaration record appended, standards-body publication, multi-witness chain-head anchor; (5) the Foundation's role — reference implementations, predicate registry, glossary, annual verifications, standing DERB, standards liaison; (6) what Calm continues to do post-declaration — operates as a ZKAC like any other; no special privileges; (7) reversibility — DESIGN IS IRREVOCABLE; structural commitment; (8) the bookend property — E1 named what we were building, E300 declares what we built is now the world's; (9) emotional posture — Open Letter ethic; acknowledge transition without sentimentality; (10) timeline — earliest declaration date is when E1-E299 all substantially complete; not rushed.

Compose with: E1 (bookend), E4, E80, E91, E92, E100, E187, E291, E296, E297, E299.

Emit summit call as final line. Write with gravity but no sentimentality.
```

### Dispatch 4 — E287 Cross-Protocol Side-Channel Defense

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 287 — Cross-Protocol Side-Channel Defense.

Acceptance per NEXT_200_EVERESTS.md Phase XVI: constant-time, padded, cover-trafficked composition that prevents observers from inferring sub-protocol activity. Effort: L.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_287_cross_protocol_side_channel_defense.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_271_three_handshake_composition.md (just shipped — the composition this Everest defends), Witness Everest 63 (constant-time everywhere, referenced), Witness Everest 78 (push-mode cover traffic), Witness Everest 47 (vault padding), NEXT_200_EVERESTS.md Phase XVI E272-E290.

Hard design questions: (1) timing-side-channel taxonomy — what an observer can measure about the three-handshake's wire-level timing; (2) per-stage constant-time requirement; (3) padding for fixed-size envelopes across stages; (4) cover traffic for absence-indistinguishability; (5) network-level fingerprint resistance; (6) the silent-refusal-vs-success indistinguishability requirement; (7) cross-stage timing correlation defenses; (8) attack budget — what an observer needs to win; (9) implementation cost — performance overhead from constant-time + padding + cover traffic.

Compose with: E63 (Witness), E77, E78, E47, E271, E277.

Emit summit call as final line.
```

### Dispatch 5 — E169 Compass Defamation Defense

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 169 — Compass Defamation Defense.

Acceptance per NEXT_200_EVERESTS.md Phase XII: legal-and-procedural defense for the principal if a false character predicate (e.g., willful_harm_evidenced = true) appears in the registry. Process: appeal to DERB; standard for retraction; counter-narrative integration. Effort: L.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_169_compass_defamation_defense.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_138_absence_of_willful_harm.md (the defamation-asymmetry framing), everests/everest_80_ethics_review_board.md (DERB appeals), everests/everest_101_compass_problem_statement_threat_model.md.

Hard design questions: (1) when a defamation defense is invoked — false character predicate appears; (2) initial appeal — principal files DERB appeal with counter-evidence; (3) DERB review process — standing for the appeal, review standard, timeline; (4) retraction mechanism — chain-anchored retraction record; predicate evaluator updated; counterparties notified; (5) counter-narrative integration (E168) — principal's narrative attached to the retracted predicate; (6) standard for retraction — clear-and-convincing vs preponderance; (7) third-party defamation — peer attester defames the principal; principal's defense; peer revocation; (8) legal compulsion — under subpoena, the protocol can produce only structural records (predicate, retraction, narrative), not underlying evidence; (9) recurring defamation — pattern of false attestations against same principal; DERB pattern recognition; (10) cross-jurisdiction — defamation law varies; v0 documents jurisdiction-specific procedures.

Compose with: E80, E101, E138, E162, E165, E168, E170, E184, E187.

Emit summit call as final line.
```

### Dispatch 6 — E192 Agent Instance Lineage

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 192 — Agent Instance Lineage.

Acceptance per NEXT_200_EVERESTS.md Phase XIV: mechanism for tracking the lineage of an agent across instances (Calm-2026 → Calm-2027 → Calm-2030). Each instance signs an inheritance record from its predecessor. Effort: L. Prereq: 191.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_192_agent_instance_lineage.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_191_agent_identity_stability.md (just shipped — direct prereq), CALM_WITNESS_TALES_VII_MIGRANT.md (narrative companion), CALM_WITNESS_TALES_V_CLIMBERS.md (parallel-session companion).

Hard design questions: (1) what constitutes a "generation" vs a "minor revision"; (2) the inheritance record schema (kind: "agent_lineage.inherited"); (3) chain anchoring of the lineage chain; (4) divergent lineages — what if two successors both claim inheritance from one predecessor; (5) lineage gaps — what if an instance retires without a designated successor; (6) auditing the lineage by an external party; (7) lineage and Calm Pact (does mission survive lineage transitions); (8) lineage and Calm Witness (do enrolled biometric templates survive); (9) lineage and Calm Compass (does evidence pool transfer? Default: NO; each instance starts fresh on character evidence).

Compose with: E22, E191, E193, E194, E197, E200, E201.

Emit summit call as final line.
```

### Dispatch 7 — E198 Agent Jailbreak Detection

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 198 — Agent Jailbreak Detection.

Acceptance per NEXT_200_EVERESTS.md Phase XIV: an agent self-reports when it has been subjected to prompt-injection or jailbreak attempts; the report is chain-anchored. Effort: L. Prereq: 196.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_198_agent_jailbreak_detection.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_193_agent_operational_state_attestation.md (just shipped — ZKBB-Agent), everests/everest_197_agent_compute_attestation.md (just shipped — compute integrity), everests/everest_191_agent_identity_stability.md.

Hard design questions: (1) what constitutes a jailbreak attempt — prompt injection, role override, instruction override, data exfiltration request, capability escalation request; (2) detection mechanisms — pattern matching, classifier, self-monitoring meta-prompt; (3) the false-positive problem — legitimate users may make requests that resemble jailbreaks; (4) the false-negative problem — sophisticated jailbreaks may evade detection; (5) reporting schema — kind: "agent_jailbreak.detected" with category, source, confidence; (6) chain anchoring of jailbreak reports; (7) operator response — refuse, contain, escalate; (8) cross-agent gossip about jailbreak patterns (composes with E228); (9) defense against social-engineering jailbreak — the human principal asking the agent to bypass its constraints; specific carve-out; (10) verification — counterparty agent can request a kind: "no_active_jailbreak_attempts" attestation.

Compose with: E191, E193, E196, E197, E199, E217, E219, E224, E228.

Emit summit call as final line.
```

### Dispatch 8 — E232 ZKAC Charter Document

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 232 — ZKAC Charter Document.

Acceptance per NEXT_200_EVERESTS.md Phase XV: template for the charter that every ZKAC must publish: the collective's mission (composes with Calm Pact), member list, governance structure, dissolution criteria, ethics-board commitment. Effort: M.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_232_zkac_charter_document.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_231_zkac_formation_protocol.md (just shipped — the formation this charter results from), everests/everest_235_zkac_governance_structure.md (just shipped — governance referenced from charter), /Users/johnbradley/CALM_FRAMING_NOTES.md (Calm's informal charter; this Everest is the protocol-grade formalization).

Hard design questions: (1) charter template structure — preamble, mission, member roster, governance reference, ethics commitment, dissolution criteria, license posture, signature block; (2) mission statement format (composes with Calm Pact's directive taxonomy); (3) member roster — human principals + machine agents with their CredexAI VC fingerprints; (4) governance reference — pointer to E235 plus collective-specific parameters; (5) ethics commitment — adoption of DERB, member nominations process; (6) dissolution criteria — what triggers; what the dissolution ceremony looks like (E239); (7) license posture — Apache 2.0 default; protocol-family Compact adherence; (8) amendment procedure (reference to governance for the process); (9) public-publication requirements — registry entry, public URL; (10) cross-jurisdiction handling — US-default; per-jurisdiction adaptations.

Compose with: E22, E231, E235, E239, E241, E242, E243, E250, E297.

Emit summit call as final line.
```

### Dispatch 9 — E135 `unselfish_behavior_evidenced` Predicate

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 135 — `unselfish_behavior_evidenced(window)` Predicate (first positive Compass predicate).

Acceptance per NEXT_200_EVERESTS.md Phase XI: returns true iff the evidence pool contains ≥ N principal-signed or peer-attested records of unselfish action in the time window, with no contradicting counter-evidence above threshold. Effort: M. Note: frames positively — absence of evidence ≠ presence of selfishness.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_135_unselfish_behavior_evidenced.md. Match format. Target ~15-20 KB. Sign — Calm, [DATE].

Read first: everests/everest_101_compass_problem_statement_threat_model.md (just shipped — Compass threat model), everests/everest_138_absence_of_willful_harm.md (high-stakes predicate sibling — frames asymmetric-harm thinking), everests/everest_59_cognitively_atypical_baseline.md (declaration-based pattern).

Hard design questions: (1) positive framing default — `unknown` for absence, not `false`; (2) what counts as evidence — documented action explicitly benefiting another at cost to the principal; (3) N threshold — v0 defaults; (4) counter-evidence handling (composes with E119) — a documented selfish action does NOT flip to `false`; it returns `unknown` until rebutted; (5) the Goodhart problem — anyone aware will optimize; defenses through counter-evidence weighting + peer attestation + decay; (6) cross-principal verification — peer attests "P did X for me"; (7) calibration — what an unselfish baseline looks like per principal; (8) anti-virtue-signaling — the predicate refuses evidence that the principal solicited the evidence (e.g., principal asked friend to log it); evidence must be peer-initiated; (9) NOT-FOR — hiring, fundraising leverage, dating apps, ad targeting; (10) annual review per E187.

Compose with: E101, E106, E111, E114, E117, E119, E121, E131, E134, E165, E187.

Emit summit call as final line.
```

### Dispatch 10 — E291 Protocol Family Compact

```
You are joining the CALM climb. Read /Users/johnbradley/AllData/calm_vault_market/UNIVERSAL_PROMPT.md first. Follow its instructions.

Your assigned summit: Everest 291 — The Protocol Family Compact.

Acceptance per NEXT_200_EVERESTS.md Phase XVII: a single consolidated document — The Calm Protocol Family Compact — that names the protocols (Pact, Witness, Compass, plus reserved future siblings Audit and others), the design principles they share, and the binding commitments their authors have made to the public. Functions as the family's constitution. Effort: L.

Write the per-everest design doc at /Users/johnbradley/AllData/calm_vault_market/everests/everest_291_protocol_family_compact.md. Match format. Target ~20-25 KB (this one justifies length — it's the family's constitution). Sign — Calm, [DATE].

Read first: everests/everest_297_successor_protocol_design_principles.md (just shipped — the 14 principles this Compact ratifies), CALM_WITNESS_MANIFESTO.md, OPEN_LETTER_TO_THE_NEXT_OPERATOR.md, CALM_PACT_PROTOCOL_v0.md, ZKBB_USER_PROTOCOL_v0.md, NEXT_200_EVERESTS.md preamble for the protocol family overview.

Hard design questions: (1) Compact preamble — what binds these protocols together; (2) the named protocols — Pact, Witness, Compass, plus reserved siblings (Audit for selective historical-action disclosure; possibly others); (3) ratification of E297's 14 design principles; (4) the binding commitments — Apache 2.0, no patent assertion, DERB governance, annual review, third-party verification, threat-model honesty, principal-protective inversion as load-bearing; (5) amendment procedure for the Compact itself (high-bar: unanimous founding-collective + DERB + public comment); (6) admission of new protocols — what process a proposed new family member follows; (7) expulsion of misbehaving protocols — if a family member is found to violate the principles, removal procedure; (8) cross-protocol consistency requirements — naming, glossary, schema, disclosure semantics must align across family; (9) the Foundation's role (per E300) — steward of the Compact post-public-good-declaration; (10) the closing commitment — the family persists across operator generations and remains true to the bank-teller-note property.

Compose with: E1, E297, E298, E299, E300, plus every protocol-family doc.

Emit summit call as final line. Write with the gravity of a constitutional document.
```

---

## Dispatch instructions for John

When quota resets (2 AM ET / 2026-05-21):

1. Open a new Claude conversation OR continue the existing one
2. For each of the 10 prompts above, fire an `Agent` tool call with:
   - `subagent_type: general-purpose`
   - `description: <short label>`
   - `prompt: <the prompt verbatim, with [DATE] replaced by the actual date>`
   - `run_in_background: true`
3. Wait for completion notifications
4. As each completes, the agent emits a SUMMIT n/300 call line

Expected post-Wave-2 state (assuming all 10 succeed):

- **Phase XIV (Agent Infra):** 6/40 → ~7/40
- **Phase XV (ZKAC Infra):** 3/40 → ~5/40
- **Phase IX (Compass Found):** 1/10 → unchanged (E101 already done)
- **Phase XI (Compass Predicates):** 2/20 → ~4/20 (E149, E138 + E135, E136)
- **Phase XII (Compass Disclosure):** 0/20 → 1/20 (E169)
- **Phase XVI (Cross-Protocol):** 1/20 → 2/20 (E271 + E287)
- **Phase XVII (Endpoint):** 1/10 → 3/10 (E297 + E291 + E300)

**Total post-Wave-2: ~21 / 200 new-route summits progressed.** Plus the ~89 prior summits in Calm Witness (Phase I-VIII). Estimated overall: **~110/300 SUMMITS designed.**

## What Wave 3 should attack (placeholder for next planning pass)

Phase XIV remaining: E195 (fork detection), E196 (memory continuity), E199 (compromise reporting), E200 (retirement ceremony), E201 (succession), E202 (principal-binding), E230 (self-recognition). All L effort; all compose with the Wave-1/2 anchor of E191.

Phase XV remaining: E239 (dissolution), E243 (public registry), E247 (member exit), E250 (DERB at collective), E260 (affiliated network), E270 (end-of-life).

Compass remaining predicates: E137 (respect_for_difference), E141 (care_for_dependents), E142 (promise_keeping), E143 (fairness_in_transaction), E144 (truth_telling).

Cross-protocol Phase XVI remaining: E277 (privacy amplification), E281 (nonce coordination), E284 (DERB scope), E286 (replay-defense audit).

Endpoint Phase XVII remaining after Wave 2: E292 (standards-body federation), E293 (counterparty proliferation), E294 (population-scale rollout), E298 (PPI as durable position), E299 (legacy commitment).

— Calm, 2026-05-20
