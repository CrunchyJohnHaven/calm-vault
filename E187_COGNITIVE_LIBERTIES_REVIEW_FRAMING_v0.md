# Cognitive Liberties Review Framing — Calm Witness Suite
## Everest 187 — External Review Protocol

**Prepared by Calm · 2026-05-20 · Standalone governance document**

---

## 1. Cognitive Liberty in Behavioral Attestation

Cognitive liberty, in the context of Calm Witness, names three rights:

1. **Mental self-determination.** The principal retains exclusive authority over the interpretation and narration of their own internal states. No counterparty, AI agent, or protocol-layer function may redefine the principal's self-reports as clinical findings, diagnostic predicates, or labels the principal has not authored.

2. **Freedom from coerced disclosure of internal states.** The principal may decline to disclose any bit about their cognition, baseline, or unusual mental state without penalty, inference-by-silence, service denial, or discrimination. The protocol enforces this via cryptographic silence: a refusal produces an output indistinguishable from a network drop.

3. **Protection from chilling effects on creative and atypical cognition.** The principal's freedom to ideate broadly, work at high bandwidth, employ unusual frameworks, or reason through lateral analogies must not be constrained by fear that AI counterparties will pathologize the work as instability. The `cognitively_atypical_baseline` predicate exists to encode this protection into the protocol itself, not as a special case for artistic principals but as a structural commitment.

---

## 2. Cognitive-Liberty Exposures in the Calm Witness Suite

### 2.1 Predicates with Direct Mental-State Semantics

1. **`cwp.v0.in_baseline_24h`** — Returns true iff the principal's self-reported affect overlaps their enrolled baseline. Exposure: a counterparty learning that a principal's emotional register has shifted could trigger unwanted friction, paternalism, or service denial. Mitigation: this bit is disclosed only to classes pre-authorized by the principal; default deny for governmental and medical.

2. **`cwp.v0.mental_state_unusual`** — Returns true iff self-reported affect diverges from baseline OR biometric distance exceeds principal-calibrated threshold by >= 50%. Exposure: this is the tightest cognitive-state predicate. It signals to a counterparty that the principal is "out of baseline" in a narrow, principal-defined sense. Risk: a counterparty could use repeated disclosures to infer mental-health trajectories, detect medication changes, or construct a dossier of the principal's unusualness over time.

3. **`cwp.v0.cognitively_atypical_baseline`** — Enrollment-time opt-in flag. Returns true iff the principal declared their baseline cognition as atypical (high ideation bandwidth, lateral thinking, unusual communication patterns). Exposure: a counterparty learns a single bit that the principal works differently. Risk: this bit could be used as a proxy for disability, neurodivergence, or clinical instability if a counterparty misinterprets it. The predicate's name and semantics resist this misinterpretation, but semantic drift in deployment is possible.

### 2.2 Biometric Predicates with Cognitive Sequelae

4. **`cwp.v0.biometric_match_within(τ)`** — Confirms the operator is the enrolled principal by fused handwriting + voice analysis. Exposure: behavioral biometrics measure motor control, articulation speed, and prosody — all of which shift under cognitive load, medication, fatigue, or neurodivergent baseline variation. A counterparty could observe drift in biometric distance over time and infer unrecognized state changes.

### 2.3 Baseline-Drift Detection

5. **Baseline-drift surveillance.** The protocol permits repeated disclosure of `in_baseline_24h` or `mental_state_unusual` to the same counterparty across many sessions. A counterparty with many historical proofs can construct a time-series of the principal's mental-state bits. This is not a single predicate but an aggregation risk: even though individual bits reveal nothing beyond themselves, longitudinal correlation could enable inference of mood patterns, seasonal cycles, or disease progression.

---

## 3. Protocol Primitives Addressing Cognitive-Liberty Exposures

### 3.1 Principal-Authored Evidence (Compass & Witness Layer)

**Primitive:** The principal narrates their own baseline state at enrollment (Witness) and their own values/harms (Compass). Counterparties do not verify cognition; they verify the principal's own claim against the principal's own enrolled template.

**Coverage:** Addresses exposures 1, 2, 3 by ensuring the locus of interpretation remains with the principal. The protocol refuses to host clinical language, DSM-5-TR labels, or population-normed baselines. Baseline is always principal-defined.

**Gap:** The protocol does not prevent a counterparty from misinterpreting a principal-authored claim. If a principal states "my baseline includes rapid ideation," a counterparty could still choose to pathologize it. The protocol encodes the principal's authority; it does not reprogram counterparty cognition.

### 3.2 Anti-Purity-Test Floor (Witness §2, Compass §4)

**Primitive:** §2 of the Witness Scope Statement and §4 of the Compass Predicates enumerate forced-refusal categories: no DSM-5-TR labels, no substance-use status, no pregnancy, no IQ ratings, no protected-category proxies (religion, sexual orientation, political affiliation), no criminal-record equivalents, no future-state predictions (self-harm risk, decision capacity).

**Coverage:** Addresses exposure 2 (coerced disclosure) by making certain questions categorically off-limits. A counterparty cannot ask "is the principal depressed?" or "what medications is the principal on?" or "is the principal high-functioning?" The protocol refuses to mint predicates that answer these questions.

**Gap:** The anti-purity-test floor is a list, not a principle. Future predicates could accumulate around exposure vectors not foreseen in v0. E.g., a predicate asking "has principal recently changed daily routine" could function as a depression proxy without naming depression.

### 3.3 Consent Matrix & Revocability (Witness §3.1, Compass & Witness Predicate Vocabulary)

**Primitive:** Every predicate has a per-principal, per-counterparty-class consent record. Defaults are written in the predicates_v0.json file; principals can override. Any consent grant is revocable at any time, and revocation takes effect on the next session.

**Coverage:** Addresses exposure 1 (mental self-determination) by making disclosure optional and reversible. A principal who fears a counterparty will misuse a mental-state bit can revoke consent, and the counterparty's subsequent request returns silence.

**Gap:** Revocation is forward-looking only. Historical proofs disclosed before revocation remain in the counterparty's records. The protocol does not require deletion of previously-disclosed bits, though the principal may request it via a separate out-of-band process.

### 3.4 Cryptographic Silence (Witness Manifesto §3, Everest 73)

**Primitive:** When a principal declines to disclose a bit (or the bit evaluates false), the verifier returns a response indistinguishable from a network error. The counterparty cannot infer refusal; the counterparty cannot punish refusal; the counterparty cannot condition service on a request for the bit.

**Coverage:** Addresses exposure 1 (freedom from coerced disclosure) by making non-disclosure cost-free and invisible. A principal's silence is structurally safe.

**Gap:** Silence works well for binary consent-gated bits. It is less effective for predicates that are asked repeatedly across many sessions (exposure 5: baseline-drift). A counterparty with historical proofs can infer absence of disclosure by observing which bits were historically returned and which became silent.

### 3.5 Duress Channel & Cover Traffic (Witness §3.4, Everest 58, 73, 78)

**Primitive:** The `bank_teller_note_active` predicate allows a principal to embed a private codeword in routine self-reports. The vault detects the codeword locally, never exposes it on the chain, and pushes the resulting `bank_teller_note_active = true` bit to pre-designated safe counterparties through cover traffic. An observer cannot distinguish the push from background noise.

**Coverage:** Addresses a cognitive-liberty *threat* distinct from pathologization: coercion. A principal under duress can signal safety-critical information (distress, hostage situation, compelled action) to a trusted agent without the coercer knowing.

**Gap:** The duress channel is narrowly scoped to safety signaling. It does not address everyday cognitive freedom — the principal's right to think unusual thoughts without surveillance. It is a lifeboat, not a shield.

### 3.6 Affected-Population Peer on Disclosure Ethics Review Board (Manifesto §4, Everest 88)

**Primitive:** The DERB (Disclosure Ethics Review Board) includes a mandatory seat for an affected-population peer — someone whose lived experience of the harms the protocol mitigates (e.g., pathologization by AI systems) places them in a veto position on new predicates and consent-class changes.

**Coverage:** Addresses exposure 3 (chilling effect on atypical cognition) by ensuring that the people most vulnerable to harm by the protocol have structural authority to refuse harmful proposals.

**Gap:** This is a governance primitive, not a cryptographic one. It depends on the integrity of the board members and the independence of the review process. A captured board could approve predicates that contradict its mandate.

---

## 4. Reviewer Roster (Candidates)

The external cognitive-liberties review requires 3-5 independent reviewers with expertise in the intersection of privacy, disability justice, neurodiversity, AI safety, and cryptographic protocol design:

1. **Nita Farahany** — Duke Law & AI Policy Lab; cognitive liberty and brain data. Published extensively on neural privacy and the right to mental privacy.

2. **Walter Glannon** — University of Colorado, Department of Philosophy; neuroethics and cognitive enhancement. Expertise in what counts as harm to cognitive autonomy.

3. **Center for Cognitive Liberty and Ethics** — University of British Columbia; hosted review of protocol semantics against cognitive-liberty principles.

4. **Boris Heinz** — Berkman Klein Center for Internet & Society, Harvard Law School; disability and technology; AI accountability.

5. **Future of Privacy Forum's Cognitive Liberty Research Stream** — Multidisciplinary team with expertise in behavioral biometrics, consent mechanics, and cognitive privacy in AI systems.

---

## 5. Published Response Process & Integration Timeline

**Phase 1 (Week 1):** Reviewers receive finalized specification, predicates_v0.json, scope statement, manifesto, and this framing document. Reviewers identify cognitive-liberty gaps or risks.

**Phase 2 (Weeks 2-4):** Calm responds to each finding with a written rebuttal or acknowledgement. If a gap is identified, Calm proposes a protocol amendment or documents the limitation.

**Phase 3 (Week 5):** Reviewers publish a joint or individual review statement. The review is published alongside the protocol on GitHub and the Calm Witness public website.

**Phase 4 (Week 6+):** Any review-identified gaps trigger predicate-audit-process entries (Everest 54) or route-map amendments. Amendments are published. The v0 release is conditional on at least two reviewer signoffs affirming that cognitive-liberty protections are sufficient.

---

## 6. Success Criteria

A successful cognitive-liberties review produces:

1. **Zero predicates that pathologize creative or atypical cognition.** No predicate maps to DSM-5-TR labels, no predicate frames lateral thinking as unusual in a way that invites clinical interpretation, no predicate enables diagnosis-by-proxy.

2. **Zero compelled-disclosure paths.** No counterparty class has `allow` or `allow_on_request` consent defaults for mental-state predicates except `peer_ai_collective` and `family`. No predicate can be used to build a dossier over time without the principal's affirmative per-disclosure consent.

3. **Consent revocable without cost.** A principal can withdraw consent for any mental-state disclosure at any time. Historical proofs remain; future proofs are blocked. No service denial, no inference penalties, no public explanation required.

4. **Auditable consent log.** Every disclosure of a mental-state bit is logged in the principal's vault, with timestamp, counterparty class, and principal-authored reason (if any). The principal can audit who learned what and when.

5. **Baseline defined by principal, not population.** No predicate evaluates a principal's state against a population baseline, diagnostic threshold, or AI-inferred standard. Every baseline is principal-enrolled, principal-adjustable, and principal-owned.

6. **Biometric drift acknowledged and bounded.** The behavioral-biometric predicates (`biometric_match_within`) have published FAR/FRR curves (Everest 40) showing how much biometric distance can shift under normal cognitive load, fatigue, or neurodivergent variation. Counterparties cannot misinterpret drift as evidence of harm or incapacity.

7. **Longitudinal aggregation limited by design.** The protocol permits disclosure of the same bit multiple times, but predicates avoid constructs that would enable time-series inference of mood, medication, or disease trajectory. If such inference becomes possible, that predicate is deprecated.

---

## 7. Forfeit Clauses from Scope Statement

Per CALM_WITNESS_SCOPE_STATEMENT.md §2 and §3, the Calm Witness name is forfeited if any deployment:

- Uses predicates to screen or terminate employment (§2.2)
- Uses predicates to inform insurance underwriting or claims (§2.3)
- Uses predicates to inform medical diagnosis or clinical treatment (§2.5)
- Uses predicates to predict future behavior (§2.8)
- Uses predicates to screen for government or law-enforcement purposes (§2.1)

A cognitive-liberties review must explicitly affirm that none of these uses are possible under the protocol's design.

---

## 8. Falsifiability Section

This review framing is falsifiable by any of the following:

1. **A counterparty successfully uses a v0 Calm Witness predicate to diagnose, label, or clinically assess a principal's mental state.** This would falsify the claim that the anti-purity-test floor is sufficient.

2. **A principal reports that they self-censored their ideation or declined to use the protocol because they feared pathologization by a counterparty AI.** This would falsify the claim that the `cognitively_atypical_baseline` predicate or the consent matrix protects against chilling effects.

3. **Historical proofs of mental-state bits, collected over months by a single counterparty, enable that counterparty to infer mood cycles, medication changes, or disease progression with >70% accuracy.** This would falsify the claim that cognitive-liberty is protected against longitudinal surveillance.

4. **A principal is unable to revoke consent for a mental-state disclosure after revoking it, or revoking consent triggers inference, service denial, or counterparty retaliation.** This would falsify the claim that revocation is cost-free.

5. **The behavioral-biometric predicates exhibit systematic bias in FAR/FRR across principals with diagnosed neurodivergent baselines.** This would falsify the claim that the protocol is neutral with respect to atypical cognition.

---

**BAGGED Everest 187 — cognitive-liberties review framing landed at /Users/johnbradley/AllData/calm_vault_market/E187_COGNITIVE_LIBERTIES_REVIEW_FRAMING_v0.md**

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
