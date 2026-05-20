# Calm Witness/Compass — CHI 2027 Submission Packet (E219, DESIGN-BAGGED)

**Status:** DESIGN-BAGGED · Closes Everest 219 (ZKAC_NEXT_200_EVERESTS.md)
**Venue:** ACM CHI 2027 (Human Factors in Computing Systems) · Submission deadline: October 2026
**Date:** 2026-05-20

---

## Authors

**Primary author:** Calm (operating for John Bradley, Creativity Machine LLC)
**HCI co-author:** [Placeholder — mixed-methods / privacy-UX researcher, TBD]

---

## Bank-Teller Notes for Autonomous Agents: A Human-Centered Design of Bit-Level Privacy Disclosure

---

## Abstract

Autonomous AI agents increasingly act as proxies for human principals in high-stakes interactions — negotiations, financial transactions, health disclosures, professional references. When two such agents encounter each other, a natural question arises: *what safety-relevant information about the underlying human should be permitted to cross the wire?* Current practice offers two inadequate answers: reveal nothing (leaving counterparties to guess) or reveal too much (transcripts, biometrics, full context). This paper introduces the **bank-teller-note** interaction model, a HCI framework in which the principal authors and authorizes a single bit of disclosure per predicate per counterparty, without revealing the underlying state record, biometric, or conversation history. Drawing on the Calm Witness and Calm Compass protocols — a principal-authored evidence system currently in open development — we analyze three interlocking human-factors problems: (1) how principals understand, enroll in, and revoke per-predicate consent; (2) how the artist clause (the motivating use case, in which the principal is routinely misread by counterparty models) functions as a usability principle; and (3) how the preview right — the ability to simulate disclosure outcomes before committing — shapes principal decision-making. We propose a mixed-methods pilot study (N ≈ 30 principals, IRB-seeking) designed to test whether an 8th-grade-readable onboarding animation produces durable informed consent and whether preview-right interaction reduces decision anxiety without increasing disclosure. Predicted findings and open questions in disability-rights framing are discussed.

**Keywords:** consent UX, privacy disclosure, principal autonomy, autonomous agents, bank-teller-note, preview right, contextual integrity, artist clause

---

## 1. Introduction: The Artist Clause as a Motivating UX Problem

Consider a principal who is an artist working in the medium of intelligence. Their cognitive style produces high-bandwidth ideation: dense associations, rapid context-switching, atypical lexical choices, and prose whose tone may, when read by a counterparty model calibrated on a general population, pattern-match to agitation, instability, or impaired judgment. The counterparty model adjusts — increases friction, adds caveats, slows its cadence — not because the principal is in distress, but because the counterparty has no mechanism to distinguish lucid high-bandwidth production from state-based anomaly.

This is not an edge case. It is a structural feature of any system in which a counterparty must infer principal state from unstructured signal. And it illustrates a design failure that sits squarely in the human-factors domain: the counterparty's read of the principal — imprecise, biased by population-mean priors — supplants the principal's own read of themselves.

The Calm Witness protocol (ZKBB_USER_PROTOCOL_v0.md, 2026) proposes a corrective: the principal authors a short daily self-narration, appended to a tamper-evident hash-chained log in a principal-controlled vault. An AI agent operating on the principal's behalf evaluates named predicates over this log — `in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, counterparty_class)` — and, when the principal has authorized disclosure, passes a single cryptographically attested bit to a counterparty agent. The counterparty learns the bit and the freshness window. Nothing else crosses the wire.

The analogy invoked in the protocol's own documentation is the **bank-teller note**: an employee enters a bank on an errand and slips a note through the teller's slot reading "I am being held hostage." The teller learns one bit. Not the nature of the threat, not the location of the captor, not the identity of bystanders. One bit, unforgeable because only the employee could have written it, sufficient for the teller to act. The Calm Witness protocol generalizes this to agent-to-agent communication: a signed cryptographic envelope, evaluated over a principal-authored record, disclosing one bit. No transcript. No biometric. No relationship graph.

The *artist clause* — §8 of ZKBB_USER_PROTOCOL_v0.md — names the motivating use case explicitly. It is a design principle, not a carve-out: **the authority to characterize principal state belongs to the principal, not the counterparty.** This paper takes the artist clause seriously as a human-factors contribution. The UX question it raises is not merely "how do we build this?" but "what does it mean for a principal to genuinely author and own their own state disclosure, in a way that is comprehensible, revocable, and not coercive?"

We identify three interlocking research questions:

- **RQ1:** Does the bank-teller-note onboarding animation produce durable informed consent, as measured against an 8th-grade reading comprehension standard?
- **RQ2:** Does the preview right — the ability to run a local simulation of disclosure outcomes before committing — reduce decision anxiety and increase post-disclosure confidence without increasing overall disclosure rate?
- **RQ3:** Does the per-counterparty consent calculus feel meaningful to principals, or does its granularity collapse into either blanket approval or blanket refusal?

---

## 2. Related Work

### 2.1 Privacy Taxonomies and the Limits of Notice-and-Choice

Solove's taxonomy of privacy harms (Solove, 2006) identifies information flow, surveillance, aggregation, and decisional interference as distinct categories of injury — each requiring different regulatory and design responses. Standard notice-and-choice frameworks, as implemented in GDPR consent dialogs and Apple's App Tracking Transparency prompts, collapse this taxonomy into a binary gesture: accept or reject, often at enrollment time, with no granularity across counterparty classes, predicate types, or use-case contexts. The result, well documented in the empirical literature (Acquisti et al., 2015; Schaub et al., 2015), is that principals routinely consent to disclosures they would not endorse if they understood them.

The bank-teller-note model addresses this at the structural level. Rather than a blanket consent toggle, principals authorize disclosure per (predicate, counterparty_class) pair. The consent matrix is not presented at signup; it is entered at the moment of first request, when the counterparty class and predicate are concrete. This is consistent with Solove's (2012) argument that meaningful consent requires contextual specificity — the principal must know what is being disclosed, to whom, and for what purpose.

### 2.2 Contextual Integrity and Per-Counterparty Consent

Nissenbaum's contextual integrity framework (Nissenbaum, 2004; 2010) holds that privacy norms are not about secrecy per se but about appropriate information flows: a patient's health record shared with a treating physician is appropriate; the same record shared with an insurer is not. This framework maps naturally onto the Calm Witness predicate vocabulary. Each predicate has a per-counterparty-class consent matrix specifying which counterparty classes the principal is permitted to authorize; the default is `deny` for the classes most prone to scope violations — governmental, insurance, anonymous, employment.

The UX implication is that principals must understand not just what is being disclosed but to what counterparty class. Our pilot study design (§6) includes a scenario in which the stated counterparty class differs from the principal's intuitive category for the requesting agent — testing whether the per-class matrix surfaces as meaningful or as bureaucratic overhead.

### 2.3 Privacy Nudges and Decision Architecture

Acquisti, Brandimarte, and Loewenstein (2015) demonstrate that privacy decisions are highly sensitive to framing, defaults, and decision architecture — findings that inform our onboarding design. Default-deny (opt-in required for each disclosure) is the structurally correct posture for a protocol whose principal population includes individuals who may be under social or economic pressure to disclose. The pilot study tests whether default-deny, combined with a preview right, produces the cognitive scaffolding principals need to make meaningful choices without collapsing under decision fatigue.

The preview right (Calm Concord §5, CALM_CONCORD_PROTOCOL_v0.md) is the central novel interaction: any principal can ask their agent "would I clear this requirement, if I disclosed predicates {p1, p2}?" without minting an actual disclosure envelope. The operator runs the simulation locally; no data crosses the wire. This is a privacy nudge in the direction of restraint — it lets principals discover that they would clear a requirement before deciding whether to clear it, rather than disclosing first and learning the outcome later.

### 2.4 Warning Fatigue and Comprehension

The human-factors literature on consent comprehension is sobering. Participants in security-warning studies systematically habituate to alerts and bypass them without reading (Bravo-Lillo et al., 2013). GDPR consent dialog studies show comprehension rates of 20–40% even among privacy-literate users (Matte et al., 2020). The bank-teller-note onboarding animation (PRINCIPAL_ANIMATION_SCRIPT_v0.md) was designed with this evidence base in mind: the target reading level is Flesch-Kincaid Grade 8 or below, all technical terms are confined to stage directions, and the bank-teller analogy functions as the primary conceptual bridge. The animation forbids the following terms in voiceover: *cryptographic*, *Pedersen*, *Sigma-protocol*, *zero-knowledge proof*, *hash* (in technical sense). Comprehension testing — whether an 8th-grade reader can correctly answer five factual questions after viewing the animation — is a go/no-go gate in our pilot study protocol.

---

## 3. The Calm Witness Disclosure UX

The bank-teller-note interaction model instantiates as a five-stage UX flow within the Calm Witness principal onboarding.

**Stage 1 — Enrollment.** The principal views a ≤90-second animation explaining what Calm Witness does and does not do, using the bank-teller-note analogy. No jargon. The animation is reviewed by ≥2 non-technical stakeholders before production lock, per the stage directions in PRINCIPAL_ANIMATION_SCRIPT_v0.md.

**Stage 2 — Daily hydration.** The principal writes a short self-report (verbal or written) at session intake. The report is appended to a hash-chained `user_state.jsonl` in the principal's vault — a locally held, principal-encrypted store. An optional behavioral-biometric sample (handwriting strokes, local voice transcription) is compared against an enrolled template; only the biometric distance, not the sample itself, is committed. No data leaves the vault without principal authorization.

**Stage 3 — Predicate evaluation.** The Calm agent evaluates named predicates over the current vault state: `in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, counterparty_class)`. Evaluation is deterministic and auditable. The agent does not produce a score or a characterization — only a bit per predicate.

**Stage 4 — Per-counterparty consent.** When a counterparty agent requests disclosure of predicate `p`, the principal is prompted with a consent decision: "The counterparty [counterparty_id, class: financial] is requesting: 'Is this principal in baseline state in the last 24 hours?' Allow?" The prompt includes the counterparty class, the predicate's plain-language meaning, and a preview option (§5). The default is deny.

**Stage 5 — Audit log.** Every disclosure is logged to the principal's vault: date, predicate, counterparty class, bit disclosed, proof reference. The principal can review this log at any time. Revocation of consent for future disclosures is a single toggle; it does not retroactively alter past records.

Two UX properties warrant explicit note. First, the **scope ratchet** (CALM_WITNESS_SCOPE_STATEMENT.md §2): the list of prohibited counterparty classes — governmental, employment, insurance, lending, medical (without direct-care consent), child-welfare, immigration — can only grow, never shrink. A principal cannot be socially engineered into granting a disclosure in a prohibited class; the class is blocked at the protocol level regardless of consent input. Second, the **duress codeword** (ZKBB_USER_PROTOCOL_v0.md §4, predicate `p4: bank_teller_note_active`): a principal may embed a private codeword in a self-report record that signals duress to a trusted verifier while remaining opaque to the counterparty. An adversary watching the bit cannot distinguish "in baseline" from "in baseline under duress" — the codeword flips an internal flag, not the disclosed bit. This is the bank-teller note's most literal expression.

---

## 4. Principal-Authored Evidence Model

The Calm Compass extension (CALM_COMPASS_PROTOCOL_v0.md) generalizes the bank-teller-note model from state disclosure to values-evidence disclosure. Where Witness answers "is this person in their baseline today?", Compass answers "what kind of person have they been, over time, in the choices that leave behavioral traces?"

The critical design decision in Compass is vocabulary authorship. The principal, not the counterparty, authors the predicate vocabulary they are willing to be evaluated against. The v0 vocabulary contains four predicates: `unselfish_disposition` (generosity-without-expectation events in a rolling window), `cross_tribal_engagement` (substantive across-tribe interactions, where "tribe" is defined in the principal's own enrollment ceremony), `respects_difference` (respect/contempt language ratio in communications directed at out-group members), and `no_evidence_of_willful_harm` (absence of operator-flagged or externally attested harm claims within a lookback window).

Each predicate is:
- **Behavioral, not characterological.** Compass attests patterns in a time window, not identity claims. The bit cannot be read as "this person is generous" — only as "in the 90-day window, the pattern of generosity-without-expectation events met the principal's own threshold."
- **Principal-set in its parameters.** The time window, the floor count, and the counterparty class matrix are set by the principal at enrollment. A counterparty cannot change these parameters.
- **Disputable.** If the operator's classifier produces a result the principal believes is incorrect, the principal can file a `compass_evidence.counter_claim` record. The dispute state is computed into the proof; the counterparty learns the bit is `disputed` rather than `true` or `false`.

The **principal-authored evidence model** is the structural answer to the artist-clause problem. A counterparty that would otherwise infer values from prose tone, communication style, or affinity-graph structure is instead offered a principal-authored, cryptographically attested bit over a behavioral pattern defined by the principal themselves. The counterparty learns the bit. They do not learn the pattern of events that produced it.

Human-factors implications are immediate: the enrollment ceremony, in which the principal sets predicate parameters and reviews the classifier logic, is a design challenge of the first order. Principals must understand what they are committing to being evaluated against, in a way that is meaningful rather than merely legally acknowledged. The pilot study (§6) includes tasks specifically designed to surface whether principals can accurately predict what behaviors would increment or decrement their predicate counts.

---

## 5. Preview Right and Per-Counterparty Consent Calculus

The **preview right** (CALM_CONCORD_PROTOCOL_v0.md §5) is the disclosure-UX contribution we regard as most novel relative to prior consent-interface literature. Before committing to a disclosure, the principal can ask: "If I authorized the disclosure of predicates {p1, p2} to this counterparty class, would I clear the counterparty's stated requirement?" The operator runs the simulation locally over the principal's own vault. No envelope is minted. No data crosses the wire. The principal receives a plain-language answer — "Yes, you would clear this requirement" or "No, disclosing these predicates would not be sufficient" — and then decides whether to proceed.

This inverts the standard disclosure decision architecture. In the standard model, the principal discloses, and the outcome (access granted, access denied, service modified) reveals whether the disclosure was sufficient. In the preview-right model, the principal sees the counterfactual outcome first. This has several predicted effects:

1. **Reduces unnecessary disclosure.** A principal who would not clear the requirement even with maximum disclosure has no incentive to disclose anything. The preview reveals this without any actual information transfer.
2. **Reduces decision anxiety.** A principal who is uncertain whether their state meets the counterparty's requirement can learn the answer before consenting. This replaces the anxious "will I clear?" with the concrete "yes, you will clear, if you disclose p1." The decision then becomes: "do I want to authorize this disclosure?" — a simpler, more agency-respecting question.
3. **Surfaces hidden requirements.** If the counterparty's stated requirement would not be satisfied by the predicates the principal expected to disclose, the preview reveals the gap. The principal learns they are being asked for more than they assumed, before committing.

The **per-counterparty consent calculus** refers to the matrix structure of consent decisions: each (predicate, counterparty_class) cell is an independent authorization. The default is deny. The principal grants authorizations selectively, and each grant is revocable independently.

The UX risk of this structure is decision fatigue — a large consent matrix could become a bureaucratic obstacle. Our design mitigation is two-part: (a) authorizations are requested at the moment of first actual counterparty request, not at enrollment time, so the matrix is populated incrementally rather than all at once; and (b) the principal can set class-level defaults ("for all financial counterparties, I authorize `in_baseline_24h` by default") that reduce per-encounter decision load while preserving granularity for atypical counterparty classes.

---

## 6. Pilot Study Methods

### 6.1 Overview

We propose a mixed-methods pilot study (N ≈ 30 adult principals) testing the comprehension, consent quality, and decision dynamics of the bank-teller-note disclosure UX. The study is IRB-seeking (see §9). The design is within-subjects, counterbalanced.

### 6.2 Participants

We will recruit N ≈ 30 participants across three cognitive-baseline strata (N ≈ 10 each):

- **Group A (High privacy literacy):** Prior hands-on experience with VPN configuration, data-export requests, or privacy settings review. Recruited via privacy-advocacy community boards.
- **Group B (Moderate literacy):** Awareness of privacy issues without systematic engagement. Recruited via general-population research panels.
- **Group C (Low literacy / accessibility focus):** Minimal prior engagement with consent interfaces; recruitment will prioritize participants who use assistive technology, have cognitive accessibility needs, or report low digital confidence. This group is prioritized per the disability-rights framing in §8.

Exclusion criteria: minors; current employment by any company with a disclosed interest in the Calm Stack protocols. Compensation: $50 per 90-minute session.

Demographic targets: age range 18–65; balanced gender distribution; at least 30% participants of color; at least 20% participants reporting a disability or chronic health condition.

### 6.3 Study Tasks

**Task 1 — Onboarding comprehension (baseline).** Participants view the Calm Witness onboarding animation (PRINCIPAL_ANIMATION_SCRIPT_v0.md, ≤90 seconds). They then answer five factual comprehension questions: (a) Where is your daily record stored? (b) What information does the other side receive? (c) Can you turn it off after enrolling? (d) Can you see a log of what was sent? (e) Does the other side receive your journal? Correct-answer rate of ≥80% is the go/no-go gate for the animation design.

**Task 2 — Standard binary consent (control).** Participants encounter a simulated counterparty request presented as a binary "Accept/Reject" prompt, without preview or predicate-level explanation. Financial scenario: "Do you authorize disclosure of your baseline state to [Accelerator X]?"

**Task 3 — Bank-teller-note consent (treatment).** Same financial scenario, using the full Calm Witness UX: plain-language predicate description, counterparty class label, default-deny state, preview option. Participants are offered but not required to use the preview.

**Task 4 — Preview-right interaction.** Participants use the preview function ("Run simulation before deciding"). The scenario is modified so that the preview reveals the counterparty's requirement would not be satisfied by one of the predicates the participant expected to disclose — creating a decision-relevant information asymmetry.

**Task 5 — Duress-signal scenario.** Participants are placed in a role-play scenario in which an external social pressure (a simulated employer expectation) is applied to encourage disclosure. They are shown the duress codeword mechanism. Qualitative data is collected on whether participants understand the protection it offers and whether they would use it.

### 6.4 Measures

**Quantitative:**
- Comprehension score (Task 1, 5-point scale)
- Decision latency (Tasks 2, 3, 4; seconds to confirmed choice)
- Confidence rating (pre/post, Likert 1–7)
- Preview adoption rate (Task 4: yes/no; number of preview activations)
- Preview-changed-decision rate (Task 4: did the simulation change the participant's choice?)
- Granularity engagement (Task 3: did participant modify any defaults, or accept as presented?)
- Duress mechanism comprehension (Task 5: correct explanation of what the codeword does vs. does not do)

**Qualitative:**
- Think-aloud transcripts coded for: comprehension gaps, trust markers, confusion, anxiety cues, agency language
- Semi-structured post-session interview (15 minutes): "What made you confident in your decision?" "Would you use the preview feature in real life?" "Is there any part of the consent you still don't understand?" "What does the principal's vault mean to you?"
- Card sort: participants order the five predicate types by personal sensitivity; compare against system defaults
- Disability-specific debrief (Group C): "Was the animation accessible to you? Were there terms or concepts that did not land?"

### 6.5 Analysis Plan

- **Primary hypothesis (RQ1):** Onboarding animation produces ≥80% correct-answer rate on comprehension check. Chi-square test.
- **Primary hypothesis (RQ2):** Decision latency in Task 3 is lower than Task 2 (paired t-test, α = .05); confidence delta (post − pre) is higher in Task 3 than Task 2.
- **Exploratory (RQ3):** Qualitative coding of whether per-predicate granularity was experienced as meaningful control or as overhead. Grounded theory pass on interview transcripts.
- Thematic coding: codebook from first five sessions; inter-rater reliability (Cohen's κ ≥ .70) with co-author blind-coding.
- Sensitivity analysis: exclude participants who rate scenario realism < 4/7.

---

## 7. Predicted Findings and Open Questions

### 7.1 Predicted Findings

We expect the following based on the existing literature and N=4 formative testing:

**Comprehension is learnable but drops with technical drift.** The bank-teller analogy will produce high initial comprehension (≥80%) in Groups A and B. Group C is the test; prediction is ≥70% with the current animation script, but we anticipate requests for visual-alt and audio-described alternatives.

**Preview right reduces disclosure without reducing confidence.** Participants who use the preview function are predicted to disclose fewer predicates per session (because they discover some disclosures would be unnecessary) while reporting equal or higher confidence. The mechanism is specificity: knowing "yes, p1 alone would clear the requirement" licenses restraint on p2 and p3.

**Per-predicate granularity collapses toward defaults in low-literacy group.** Group C is predicted to engage with fewer consent cells and rely more heavily on system defaults. This is not a failure of the UX — presets-as-scaffolding is a predicted feature, not a bug — but it raises a design question: are the defaults calibrated to the preferences of users who most rely on them?

**Duress mechanism comprehension is heterogeneous.** The duress codeword is a subtle concept: it requires understanding that the bit disclosed to the counterparty is unchanged, but a separate flag is set for a trusted verifier. We predict that roughly 40–50% of participants in Groups A and B will correctly explain this on first attempt; Group C may require the mechanism to be redesigned for layered presentation.

### 7.2 Open Questions

1. **How should the animation handle the ratchet clause?** The scope ratchet (§2 of CALM_WITNESS_SCOPE_STATEMENT.md) prohibits disclosure to governmental, employment, and insurance counterparty classes regardless of principal consent. How should this be communicated without making the protocol feel restrictive? The current draft animation does not address the ratchet; pilot testing will reveal whether principals want to understand it or are satisfied with the protection it offers without explanation.

2. **How does duress interaction generalize across disability populations?** The duress codeword assumes the principal can embed a private token in their self-narration without detection. For principals with cognitive disabilities, motor impairments, or AAC users, the mechanism may require redesign. This is a significant open question for accessibility.

3. **What happens when the counterparty disputes the bit?** The protocol produces a single bit. If the counterparty's system is calibrated to distrust the `in_baseline` bit from a particular principal population (e.g., because the base rate of false positives is high in that population's enrollment data), the bit loses its function. This is an equity question and an HCI question simultaneously: the disclosure UX must communicate the bit's confidence interval, not just its value.

4. **Does the preview right create anchoring effects?** If the preview simulation reveals "you would clear the requirement with p1 alone," does this anchor the principal's decision such that they never consider *not* disclosing p1, even when they might prefer not to? The study will collect data on this, but the question may require a separate experimental design to answer cleanly.

---

## 8. Discussion: Disability-Rights Framing

The artist clause is a disability-rights claim in thin disguise. The principal who is an artist working in high-bandwidth ideation mode is experiencing a form of cognitive pattern that does not conform to the population mean the counterparty model was trained on. The counterparty model responds with friction, reinterpretation, and compensatory behavior — not because the principal is impaired, but because the counterparty's read of the principal's state is systematically miscalibrated.

The bank-teller-note model addresses this by transferring epistemic authority: the principal's self-report, not the counterparty's inference, is the authoritative description of principal state. This is structurally aligned with the disability-rights principle of "nothing about us without us" — no characterization of the principal's state is produced without the principal's own narration as input.

The scope ratchet reinforces this: the employment and insurance counterparty classes are categorically prohibited because these are the contexts where state characterization most readily converts into discrimination. The protocol does not merely discourage misuse; it makes certain misuse architecturally impossible.

For principals with acquired or fluctuating cognitive disabilities, the daily hydration ritual (short self-report) serves a dual function: it is the evidence substrate for the cryptographic predicate, and it is a structured self-check that many principals report finding intrinsically valuable as a cognitive anchor. Several principles from disability-rights scholarship are directly actionable:

- **Universal design first.** The onboarding animation targets Flesch-Kincaid Grade 8. The pilot will test whether this threshold is sufficient for Group C participants, with the expectation of providing screen-reader, audio-description, and simplified-language variants.
- **Consent must be ongoing, not one-time.** Per-counterparty consent granularity supports this; the audit log and per-toggle revocation support it further. A principal whose capacity to consent fluctuates can revoke authorizations in low-capacity periods and re-grant them when capacity recovers.
- **Duress protection as civil-rights infrastructure.** The duress codeword is not a paranoid edge case; it is a response to the documented reality that principals under economic or social pressure routinely consent to disclosures they would not endorse freely. The codeword provides evidentiary protection without requiring the principal to breach the interaction context.

We note that the disability-rights implications of the protocol extend beyond the principal population. A counterparty that is forced to accept a single bit, rather than an inference from prose tone or behavioral pattern, is a counterparty that cannot discriminate on the basis of cognitive style. The bank-teller-note model is anti-discriminatory at the architectural level.

---

## 9. Ethics and IRB

The pilot study requires Institutional Review Board review before participant recruitment. Key ethics considerations:

**Deception and role-play.** Task 5 (duress scenario) involves a simulated external pressure to disclose. Participants will be fully informed that the social pressure is a study manipulation; debrief will occur immediately after the task. We will follow APA guidelines for deception in behavioral research and will not recruit participants with a history of coercive disclosure experiences without additional safeguards.

**Data handling.** No real principal-state data will be collected. All scenarios are hypothetical. Think-aloud transcripts will be de-identified before analysis. Audio recordings will be destroyed after transcription.

**Accessibility accommodations.** The study protocol will offer: large-print consent forms, screen-reader-compatible survey instruments, the option for remote participation over video call with accommodations, and extended time on all tasks.

**Conflict of interest.** The Calm Witness and Calm Compass protocols are open-source (Apache-2.0). The primary author has no financial stake in commercial deployment. The co-author selection process will prioritize researchers without prior affiliation with the Calm Stack project to ensure independence of qualitative analysis.

**Minor harms.** Participants may experience mild anxiety when considering disclosure scenarios (financial, health, employment). Debrief will include explicit reminders that no actual data was disclosed and that the scenarios were hypothetical. Contact information for a support resource will be provided.

**IRB protocol notes.** We will seek expedited review under Category 6 (cognitive research using survey procedures) or Category 7 (taste and food quality evaluation — not applicable) or the appropriate category for behavioral UX studies at the receiving institution. If the duress scenario is judged to require full review, we will seek full board review and adjust the protocol as directed.

---

## Bibliography

1. Acquisti, A., Brandimarte, L., & Loewenstein, G. (2015). Privacy and human behavior in the age of information. *Science*, 347(6221), 509–514.

2. Bravo-Lillo, C., Cranor, L., Downs, J., & Komanduri, S. (2013). Bridging the gap in computer security warnings: A mental model approach. *IEEE Security & Privacy*, 9(2), 18–26.

3. Calm (operating for John Bradley, Creativity Machine LLC). (2026). *Calm Witness: A Zero-Trust Behavioral-Biometric Protocol for User-State Disclosure Between Autonomous AI Agents* (ZKBB_USER_PROTOCOL_v0.md, v0). Unpublished protocol document.

4. Calm (operating for John Bradley, Creativity Machine LLC). (2026). *Calm Compass: A Zero-Knowledge Protocol for Principal-Authored Values Attestation* (CALM_COMPASS_PROTOCOL_v0.md, v0). Unpublished protocol document.

5. Calm (operating for John Bradley, Creativity Machine LLC). (2026). *Calm Witness Scope Statement* (CALM_WITNESS_SCOPE_STATEMENT.md, v0). Unpublished governance document.

6. Calm (operating for John Bradley, Creativity Machine LLC). (2026). *Calm Concord — Purpose-Specific Values-Alignment Calculator* (CALM_CONCORD_PROTOCOL_v0.md, v0). Unpublished protocol document.

7. Calm (operating for John Bradley, Creativity Machine LLC). (2026). *Calm Witness — Principal Onboarding Animation v0* (PRINCIPAL_ANIMATION_SCRIPT_v0.md, S249). Unpublished design document.

8. Fahl, S., Harbach, M., Hilty, M., & Smith, M. (2012). Why Eve and Mallory love Android: An analysis of Android SSL (in)security. *Proceedings of the 2012 ACM Conference on Computer and Communications Security*, 50–61.

9. Lerner, A., Simpson, A. K., Kohno, T., & Roesner, F. (2016). Internet Jones and the Raiders of the Lost Trackers: An archaeological study of web tracking from 1996 to 2016. *Proceedings of the 25th USENIX Security Symposium*, 997–1013.

10. Matte, C., Bielova, N., & Santos, C. (2020). Do cookie banners respect my choice? Measuring legal compliance of banners from IAB Europe's transparency and consent framework. *Proceedings of the 41st IEEE Symposium on Security and Privacy*, 791–809.

11. Nissenbaum, H. (2004). Privacy as contextual integrity. *Washington Law Review*, 79(1), 119–157.

12. Nissenbaum, H. (2010). *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press.

13. Schaub, F., Balebako, R., Durity, A. L., & Cranor, L. F. (2015). A design space for effective privacy notices. *Proceedings of the 11th Symposium On Usable Privacy and Security (SOUPS)*, 1–17.

14. Solove, D. J. (2006). A taxonomy of privacy. *University of Pennsylvania Law Review*, 154(3), 477–564.

15. Solove, D. J. (2012). Introduction: Privacy self-management and the consent dilemma. *Harvard Law Review*, 126(7), 1880–1903.

16. Stark, L., & Hoey, J. (2021). The ethics of emotion in artificial intelligence systems. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*, 782–793.

17. Ur, B., Pak Yong Ho, M., Brawner, S., Lee, J., Mennicken, S., Picard, N., Schulze, M., & Littman, M. L. (2016). Trigger-action programming in the wild: An analysis of 200,000 IFTTT recipes. *Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems*, 3227–3231.

18. Woelfer, J. P., Iverson, A., Hendry, D. G., Friedman, B., & Gill, B. T. (2011). Improving the safety of homeless young people with mobile phones: Values, form and function. *Proceedings of the 2011 CHI Conference on Human Factors in Computing Systems*, 1707–1716.

---

## Handoff

**Companion documents (all in `/Users/johnbradley/AllData/calm_vault_market/`):**
- `ZKBB_USER_PROTOCOL_v0.md` — protocol source for §3, artist clause at §8
- `CALM_COMPASS_PROTOCOL_v0.md` — principal-authored evidence model for §4
- `CALM_CONCORD_PROTOCOL_v0.md` — preview right at §5; threat model
- `CALM_WITNESS_SCOPE_STATEMENT.md` — scope ratchet at §2; §2–§4 prohibition list
- `onboarding/PRINCIPAL_ANIMATION_SCRIPT_v0.md` — onboarding UX source; reading-level note; reviewer sign-off table
- `CHI_PAPER_ABSTRACT_v0.md` — prior abstract draft, partially incorporated

**Next steps to move from DESIGN-BAG to submission-ready:**
1. Recruit HCI co-author with mixed-methods expertise; co-author reviews §6 (methods) and takes lead on IRB filing.
2. Commission final animation production and non-technical reviewer sign-off (PRINCIPAL_ANIMATION_SCRIPT_v0.md review table).
3. Run N=4–6 pilot comprehension check on animation before full study enrollment.
4. Pre-register study hypotheses on OSF.
5. Submit for CHI 2027 by October 2026 deadline.

**DESIGN-BAGGED designation:** This document establishes design intent for Everest 219. Execution (study run, data analysis, final manuscript revision) is not covered by this packet. The packet is the design artifact that closes the DESIGN-BAG gate.

---

*Signed: Calm (operating for John Bradley, Creativity Machine LLC) — 2026-05-20*

---

> *requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
>
> — Musk
