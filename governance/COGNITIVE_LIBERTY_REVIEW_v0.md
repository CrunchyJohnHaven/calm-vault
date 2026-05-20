# Cognitive-Liberty Review of the Calm Suite

**DESIGN-BAGGED · SUMMIT E187 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — named endorsement required from at least one of: Center for Cognitive Liberty and Ethics (CCLE), Open MIND, Centre for the Study of Existential Risk's cognitive-rights program, ACLU Speech, Privacy & Technology Project, or equivalent. Companion to `DISABILITY_RIGHTS_REVIEW_v0.md` (E186).

Where the disability-rights review (E186) asked *does the protocol protect cognitively-atypical principals against the discrimination that motivated its design*, this review asks the structurally adjacent question: *does the protocol protect the principal's right to mental privacy, mental self-determination, and freedom from mental coercion — independently of any disability framing*?

The cognitive-liberty review is concerned with three things the disability framing alone doesn't fully cover: (1) the principal's right to keep their cognitive processes opaque; (2) the principal's right to be the sole authority on their own internal experience; (3) the principal's right to revise their own self-understanding without that revision being weaponized.

---

## §1. The protocol-level cognitive-liberty protections

**§1.1 — No predicate names a mental process.** Per `PREDICATE_VOCABULARY_v0.md` §4, the v0 vocabulary names *behavioural patterns over a window*, never mental processes. The protocol cannot return `is_planning_X`, `is_considering_Y`, `believes_Z`, or `experiencing_W`. The cognitive interior is not the protocol's surface.

**§1.2 — Principal-authored vocabulary.** The principal authors the predicate vocabulary; counterparties cannot add. This guarantees that no third party — government, employer, lab, family member, romantic partner — can introduce a predicate that interrogates the principal's mental state. The vocabulary is fixed at enrollment and amendable only by the principal.

**§1.3 — Refusal indistinguishability.** Per Treaty Article V §5.1, a principal's refusal of any specific disclosure is wire-indistinguishable from non-enrollment. A coercer cannot tell whether the principal is refusing or has simply never enrolled.

**§1.4 — Bank-teller-note for mental coercion.** The duress predicate (`bank_teller_note_active`) addresses physical coercion at the moment of attestation. The cognitive-liberty extension: the duress codeword can be flipped not just under physical threat but under any context the principal has *pre-armed it for*, including manipulative interpersonal contexts, psychiatric institutionalisation against principal's will, etc.

**§1.5 — Self-revision is first-class.** Per the disability review §2.3 recommendation, v1 of the Compass protocol adds `kind: "baseline_revision"` records. The principal's right to revise their own self-understanding — through reading, therapy, life change, simple aging — is built into the chain semantics. Earlier records do not pull against the corrective disclosure.

**§1.6 — No psychiatric labels.** The same refusal floor (Treaty Article IV) that excludes race / religion / etc. excludes DSM-aligned mental-health labels. The protocol explicitly cannot be used to attest psychiatric diagnoses, fitness-for-duty, civil-commitment-eligibility, or any related framing.

## §2. The cognitive-liberty risks the protocol does NOT close

**§2.1 — Inference-by-pattern.** A counterparty receiving a Compass `respects_difference = true` attestation can, over time, infer features of the principal's communication style that the predicate did not directly disclose. The principal's mental privacy is reduced by aggregate use even though no single disclosure leaks more than the bit.

*Treaty mitigation:* Article II §2.3 forbids aggregate analytics over principal cohorts. The cognitive-liberty review's specific recommendation: the Treaty's prohibition should extend to *intra-principal* aggregate inference across multiple disclosures by the same counterparty. We recommend v1 add CC-A3: per-counterparty cumulative disclosure cap — a counterparty receiving more than N disclosures from the same principal in any rolling year is itself rate-limited regardless of consent records.

**§2.2 — Mental coercion via consequence-attachment.** Even where the protocol refuses to attest a predicate that targets mental state, a counterparty can attach consequence to *whether the principal chose to enroll* in a specific predicate at all. A landlord requiring `no_evidence_of_willful_harm` as a precondition of tenancy creates indirect coercion to enroll.

*Treaty mitigation:* Article II §2.2 forbids signatories from requiring Calm Suite attestation in forbidden contexts (Treaty Article I, which we recommend expanding to include tenancy). The cognitive-liberty review's specific recommendation: extend Treaty Article I's forbidden contexts to also include *tenancy, residency, club/association membership, social-platform reputation, and dating-platform vetting*.

**§2.3 — Chain-as-self-archive risk.** The principal's chain is, by design, a complete behavioural record under the principal's control. A principal who is later compelled to surrender chain access (e.g., by family pressure, by employer demand, by court order in a non-forbidden-context jurisdiction) loses the cognitive-liberty floor the protocol provides.

*Mitigation:* the chain-deletion-as-key-destruction option (Compliance §2.5) is the existing route. The cognitive-liberty review's recommendation: the protocol should ship a *dead-man's switch* mode where the chain auto-destructs if not accessed for a principal-set interval, requiring the principal to remain actively engaged to retain access. We propose this as v1 SUMMIT E183b.

## §3. The four cognitive-liberty rights

Following the framework of the UN Human Rights Council's emerging guidance on neurorights and the academic literature on cognitive liberty (Bublitz, Boire), we identify four cognitive-liberty rights the Calm Suite must respect.

**§3.1 Right to mental privacy.** The principal's mental processes are not knowable to any other party except as the principal chooses to disclose. The Calm Suite respects this by attesting *behavioural patterns*, never *mental states*. The protocol does not infer.

**§3.2 Right to mental self-determination.** The principal is the sole authority on their own mental experience. The Calm Suite respects this through the principal-authored vocabulary. No counterparty defines what the principal's mental states are.

**§3.3 Right to mental integrity.** The principal's mental life is not subject to involuntary alteration. The Calm Suite is a passive attestation primitive; it does not alter mental state. The protocol does not introduce risk here.

**§3.4 Right to psychological continuity.** The principal's right to a coherent psychological identity over time, including the right to revise. The Calm Suite respects this through the dispute mechanism, the baseline-revision record kind, and the chain-deletion-as-key-destruction option.

The Calm Suite satisfies all four. The protocol's design intent was structural; the cognitive-liberty framing confirms the structure is right.

## §4. Required commitments from cognitive-liberty endorsers

Beyond what the protocol and the treaty already provide, the cognitive-liberty review requires the following commitments from any endorsing organisation:

**§4.1** A published commitment that the organisation will not advocate for any policy that requires Calm Suite attestation in any context, full stop. The cognitive-liberty position is stricter than the disability-rights position: any required attestation, even in non-forbidden contexts, is a cognitive-liberty concern.

**§4.2** A published commitment that the organisation will, in any jurisdictional context where Calm Suite attestation is being introduced as a legal instrument, file commentary asserting the cognitive-liberty framework's primacy over any specific predicate-level utility argument.

**§4.3** Commitment to public-interest litigation, where applicable, against any private or public party that conditions access to fundamental services on Calm Suite attestation.

**§4.4** Annual review of the Calm Suite's predicate vocabulary against the four cognitive-liberty rights (§3 above) with published opinion.

## §5. The disability-rights / cognitive-liberty tension

A subtle tension between the two reviews merits direct address. The disability-rights review (E186 §3) is permissive about the artist-clause framing being supplemented with disabled-principal framings. The cognitive-liberty review is more cautious: any framing of the principal's cognitive style — artistic, atypical, disabled, neurodivergent, etc. — risks becoming a category that counterparties demand attestation against.

The reviews resolve as follows: the predicate's *technical* surface (a one-bit attestation drawn from a principal-authored vocabulary) is acceptable to both reviews. The predicate's *naming* (`cognitively_atypical_baseline`) is acceptable to both. The predicate's *use in documentation* (the artist clause as motivating example, with disabled-principal framings appended) is acceptable to both, with the caveat that the documentation must not slide into prescribing how principals should self-describe.

In practice: the protocol ships the predicate; the principal chooses whether to enroll; the principal chooses how to describe themselves to the operator at enrollment; the documentation surfaces multiple framings so no principal feels obligated to adopt any particular one.

## §6. The cognitive-liberty non-claim

This review does not claim that the Calm Suite is or could become a substitute for the broader legal and ethical protections cognitive-liberty advocates have spent decades arguing for: protections against involuntary commitment, against forced psychiatric medication, against coercive interrogation techniques, against the criminalisation of altered mental states. The Calm Suite cannot adjudicate any of these. The Calm Suite is one cryptographic input that, under the treaty, must not be turned against the rights the broader framework asserts.

The cognitive-liberty framework is the protection. The Calm Suite is one input that, under the treaty, must not be weaponized against it.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
