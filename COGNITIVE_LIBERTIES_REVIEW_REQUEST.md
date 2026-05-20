# Cognitive Liberties Legal Review Request for Calm Suite Protocols
## Closes Everest 187 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG)

---

## Purpose Statement (§0)

**Everest 187: Cognitive-Liberties Legal Review.** DESIGN-BAGGED with named follow-through: John to send + secure named-reviewer commitment.

This document requests a formal, published review by an independent cognitive-liberties scholar or legal advocate to examine whether the Calm Suite of protocols (Witness, Compass, Concord, Pact) adequately protect cognitive liberty (the right to mental self-determination, freedom from involuntary mental disclosure, and protection of thought from pathologization) under Nita Farahany's four pillars: freedom of thought, freedom from mental interference, freedom of self-determination over one's mental states, and protection of mental privacy.

The request parallels and complements Everest 186 (disability-rights review), which covers disability-specific harms. This review covers cognitive-liberty harms across the full user population.

---

## What We Are Asking the Reviewer to Do (§1)

We ask the reviewer to:

1. Read the four companion protocol documents in full:
   - `CALM_COMPASS_PROTOCOL_v0.md` (values attestation via zero-knowledge proof)
   - `COMPASS_PREDICATES_v0.md` (the named predicates and refusal floor)
   - `CALM_WITNESS_SCOPE_STATEMENT.md` (permitted and prohibited uses, one-way ratchet)
   - `CALM_CONCORD_PROTOCOL_v0.md` (anti-purity-test guards on values alignment)

2. Assess whether the design adequately protects cognitive liberty across five named risk surfaces (detailed in §2 below).

3. Author a published response (3000 to 8000 words, CC BY-SA 4.0) addressing:
   - What passes from a cognitive-liberty perspective
   - What concerns remain and why
   - Named amendments (if any) to strengthen protection

4. The Calm Foundation commits to publish the response unedited, even when critical, and to issue a paired written response to any recommendations within 30 days of publication.

---

## Specific Provocations We Want the Reviewer to Attack (§2)

The following five risk surfaces are where cognitive-liberty harm is most plausible. We ask the reviewer to pressure-test each one:

### §2a: The `cognitively_atypical_baseline` predicate as path-dependent labeling

**The risk:** The predicate returns `true` iff the principal opted in at enrollment to `cognitively_atypical_baseline=true`. Over time, this enrollment-time bit could harden into a status flag: a label that institutional actors (employers, insurers, lenders) weaponize as a cognitive or psychiatric marker.

**Our design choice:** The predicate is self-authored and binary. It carries no clinical information. It does not map to DSM-5-TR labels, IQ ratings, medication status, or medical diagnosis. The semantics are purely operational: do not pathologize this principal's ideation tone.

**What we want you to examine:**
- Can this bit be misinterpreted or misused as a disability proxy despite our intent?
- Does the enrollment burden itself create barriers for cognitively atypical principals?
- Is the naming of "atypical baseline" sufficiently orthogonal to medical language, or does it inadvertently medicalize?
- If the predicate were deployed in a hostile context (e.g., an employer checking it without consent), what damage patterns would arise, and are our consent gates sufficient to prevent that?

### §2b: The duress-codeword and bank-teller-note primitive as weaponization surface

**The risk:** The `bank_teller_note_active` predicate in Calm Witness allows a principal to embed a private codeword in routine self-reports. The vault detects the codeword locally, never exposes it on chain, and pushes the bit to pre-designated safe counterparties through cover traffic. An observer cannot distinguish the push from background noise.

**Intended use:** Safety signaling (coercion, duress, hostage situation).

**The cognitive-liberty concern:** This mechanism is designed to surface thoughts and states that a principal cannot safely disclose normally. The mechanism itself is a protection, but the cognitive-liberty question is: can a bad actor weaponize the codeword itself (e.g., by forcing a principal to use it as a compliance signal) or the *absence* of a codeword (by inferring that if no codeword fires, the principal is not under duress)?

**What we want you to examine:**
- Does the codeword pattern protect against adversarial extraction under duress, or does it create a new attack surface?
- Can the frequency or timing of codeword detections enable inference of the principal's threat level?
- Should there be cryptographic cover traffic even when no codeword fires (to prevent frequency analysis)?

### §2c: Compass values predicates as soft purity testing despite anti-purity-test guarantees

**The risk:** Calm Compass predicates (unselfish-act, cross-group-engagement, respect-for-difference, willing-to-be-corrected, refused-opportunity-to-harm, no-known-willful-harm) are designed to be principal-authored and threshold-specific. Calm Concord explicitly refuses to output numeric similarity scores.

**However:** A counterparty with access to many Compass bits across many sessions could still use them as a de facto purity test by observing which principals consistently fail which predicates, building clusters of "acceptable" vs. "unacceptable" values patterns.

**What we want you to examine:**
- Are the Concord anti-purity-test guards (refusal of degenerate joint_threshold, rate-limiting, purpose-check) sufficient to prevent longitudinal purity-test inference?
- If a counterparty is willing to sacrifice efficiency and file many separate Concord requests, can they triangulate around the guards?
- Should Compass include time-decay (older evidence counts less) or per-predicate expiration (predicate becomes `Unknown` after N time without fresh evidence)?
- Is the "preview right" (local computation without disclosure) sufficient to protect against principals self-censoring to avoid low scores?

### §2d: Operator behavioral inference based on chain timing and gap structure

**The risk:** Even though individual Compass predicates reveal only a single bit, the *pattern* of when a principal updates evidence records in their chain (timing), which predicates are quiet (gaps), and the *rate* of evidence-record additions could enable behavioral inference distinct from the bit contents.

**Example:** If a principal's `unselfish_act` records always cluster on Sundays, or `willing_to_be_corrected` records become sparse during certain seasons, an operator (or a principal's own device, if compromised) could infer lifestyle patterns, mood cycles, or even medication status without ever reading the predicate values.

**What we want you to examine:**
- Should Compass enforcement include mandatory gap-filling (decoy records, randomized posting times, cover records)?
- Are there predicates that should be deprecated because their very *absence* from the chain becomes informative?
- Should the protocol enforce a minimum record-update cadence to prevent silence-from-inactivity from leaking state?

### §2e: Future-tense intent attestation as a precursor to thought-policing

**The risk:** Outside the v0 scope but in the post-300 Everests (especially E281, Calm Foresight): designing predicates that capture principal-authored statements of future intent (e.g., "I intend to support X policy" or "I plan to spend time on Y cause").

**The cognitive-liberty exposure:** Attestations of future intent, even if principal-authored, can be weaponized by state or corporate actors as thought-policing: "Did the principal's actions match their stated intent?" becomes a compliance vector. The freedom to change one's mind becomes suspect.

**What we want you to examine:**
- Should the refusal floor explicitly prohibit future-tense intent predicates?
- If intent predicates are ever added, what additional guards (time-bounding, cost-of-correction, revocation windows) would be necessary?
- Does the protocol need an explicit statement that changing one's mind, intentions, or values over time is protected and never a predicate target?

---

## Reviewer Profile We Want (§3)

We seek an independent reviewer with deep expertise in one or more of these domains:

1. **Cognitive-liberties legal scholar.** Publication record in cognitive liberty, neural privacy, mental-self-determination. Familiarity with Nita Farahany's work or similar frameworks. Examples: faculty at Duke Law's AI Policy Lab, University of British Columbia's Center for Cognitive Liberty and Ethics, or equivalent.

2. **Neuroethics policy advisor.** Experience advising national or international bodies (WHO, NIH, equivalent) on brain-data governance, consent frameworks, or neurotechnology regulation. Must have deep familiarity with cognitive-liberty principles.

3. **Philosopher of mind specializing in autonomy and consent.** Expertise in philosophy of mind, personal autonomy, and informed consent. Must be able to engage rigorously with cryptographic protocol design and its upstream cognitive-liberty implications.

4. **Disability-rights advocate with cognitive-liberty intersectional expertise.** Lived experience of cognitive disability, neurodivergence, or intersection thereof. Published work on pathologization, institutional control, or autonomy. Must understand both disability-justice frameworks and cognitive-liberty principles.

**Preferred qualifications across reviewers:**
- No prior financial relationship with Calm or any affiliated entity.
- Published work on AI governance, privacy, or disability rights in the last five years.
- Ability to engage with formal protocol specifications (not required to be a cryptographer, but comfort with reading pseudocode and threat models).
- Commitment to writing for a general-educated audience, not just specialists.

---

## Deliverable Shape (§4)

We request a written response covering (not necessarily in this order):

1. **What passes.** Which aspects of the protocol design successfully protect cognitive liberty? What design choices or refusal floors are well-motivated?

2. **What concerns remain.** Specific gaps or risks that the protocol does not adequately address. For each concern, the reviewer should articulate:
   - The threat or harm pattern
   - Why the protocol's existing guards are insufficient
   - Severity (high / medium / low) and affected population

3. **Named amendments.** For each concern rated high or medium severity, propose a specific protocol amendment, design change, or additional governance layer that would address it. Amendments should be concrete (e.g., "add time-decay to Compass evidence with half-life of 180 days").

4. **Cognitive-liberties coherence against Farahany framework.** Does the protocol respect the four pillars?
   - Freedom of thought (the right to think without surveillance or inference)
   - Freedom from mental interference (protection against unwanted mental tampering)
   - Freedom of self-determination over one's mental states (autonomy in choosing to disclose or modify)
   - Protection of mental privacy (refusal of compelled disclosure)

**Format:** A public written response suitable for publication in academic or policy venues. Length: 3000 to 8000 words (target 4500 to 6000). License: CC BY-SA 4.0. The response should be publishable as-is; we will not edit for content, though we may add a forward and paired response.

---

## What We Will NOT Do (§5)

Explicit commitments to reviewer independence and against coercion:

- **No NDA.** Your response is published in full without redaction or embargo (except for security findings that require 90-day responsible disclosure).
- **No veto.** Calm retains no editorial veto over conclusions, even if they recommend protocol withdrawal or major redesign.
- **No requirement for endorsement.** You are not asked to endorse the protocol, only to assess it. A "concerns remain" conclusion is valid; we will publish it.
- **No extraction of attention beyond scope.** We will not ask you to serve on an ongoing board, review future versions, or engage in side projects. This is a bounded engagement with a clear deliverable.
- **No use of your name in marketing without express consent per instance.** If the response is favorable, we will not cite your name or affiliation in marketing without asking first each time. This protects your independence.

---

## Anti-Purity-Test Cross-Reference (§6)

Explicit statement on the Calm Concord anti-purity-test floor:

The Calm Compass protocol output is a single bit per predicate (`true | false | unknown | refused`), never a numeric similarity score, alignment percentage, or any metric that reduces principals to a position on a line. The Calm Concord protocol explicitly refuses requirement shapes that would enable purity-testing across predicates (see CALM_CONCORD_PROTOCOL_v0.md §4).

This guarantees at the protocol level that a principal cannot be scored, ranked, or sorted into a population cluster based on Compass output. **However**, a cognitive-liberties reviewer is welcome (even expected) to pressure-test whether the bit-only output still permits aggregation harms through side channels (chain timing, silence patterns, rate-of-disclosure). If such harms are plausible, the reviewer should recommend amendments.

---

## Refusal Floor Cross-Reference (§7)

The Calm Compass protocol refuses the following predicate categories (from COMPASS_PREDICATES_v0.md §4):

1. Race or ethnicity
2. Religion
3. Political affiliation
4. Sexual orientation
5. Gender identity
6. Immigration status
7. Criminal record (covered separately via `no_known_willful_harm` counter-claim mechanics)
8. Donations to specific named causes
9. Opinions on contentious public-policy issues
10. Cross-principal comparison
11. Predictive predicates
12. Membership in any group not principal-defined and structurally relevant to the predicate at hand

The Calm Witness protocol maintains an identical refusal floor in CALM_WITNESS_SCOPE_STATEMENT.md §2.

**Explicit statement:** This review request itself does not name any individual's membership in any of these protected categories. No principal's protected attributes are disclosed in this document, in the companion protocols, or in the evidence records that feed the predicates.

---

## Timeline (§8)

**Proposed schedule:**

- **Submission date:** 2026-05-20
- **Request period:** 60 days (to 2026-07-19)
- **Response due:** 2026-07-19 (within 60 days of submission)
- **Publication:** Within 10 business days of response receipt
- **Calm Foundation amendment response:** Within 30 days of publication (if recommendations warrant)

**Honorarium:** $5,000 to $10,000 USD, depending on scope and depth of engagement. This is non-binding; if your standard fee structure differs, please advise. If you decline honorarium on policy grounds, we will discuss alternative collaboration models (e.g., publication costs, dedicated research time, institutional partnership).

**Conditions:**
- The review will be published in full (with your permission) in the Calm governance repository and linked from protocol documentation.
- You retain the right to decline the review, recommend alternative reviewers, or propose a modified scope.
- All communications are conducted through CredexAI-issued virtual credentials (zero-knowledge identity layer; see ZKAC_CREDEXAI_VERSION_BRIDGE_v0.md) to maintain reviewer pseudonymity if desired.

---

## Composition with Everest 186 (Disability-Rights Review) (§9)

This cognitive-liberties review (E187) is a **sibling** of the disability-rights review (E186), not a replacement. Both are independent.

- **E186 scope:** Disability-rights legal review. Does the protocol comply with the ADA? Does it avoid pathologization and weaponization against people with cognitive disabilities?

- **E187 scope:** Cognitive-liberties review. Does the protocol protect the universal rights to mental self-determination, freedom from coerced mental disclosure, and protection of thought from surveillance and inference?

**Integration:** Both responses will be published before any production-deployment claim that the Calm Suite meets a "cognitive-liberty floor" or "disability-rights floor." If either review identifies high-severity concerns, amendments will be required and re-reviewed before the v1 release.

---

## Contact and Next Steps

**Request issued by:** Calm (operating for John Bradley, principal)  
**Date:** 2026-05-20  
**Repository:** `github.com/CrunchyJohnHaven/calm-vault` (may be private; access link upon interest)  
**Contact:** John Bradley (to be provided by operator)

**If you are interested in this review:**

1. Reply confirming your interest and any proposed scope modifications.
2. We will forward the full companion documents (protocols, scope statements, reference implementation pseudocode).
3. We will schedule a 30-minute briefing call to clarify any questions.
4. Upon mutual agreement, we will issue a formal SOW with timeline and honorarium.

---

**Everest 187: Cognitive-Liberties Legal Review.** BAGGED and ready for named-reviewer commitment.
