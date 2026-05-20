# Calm Suite — JME Bioethics Submission Packet (E220, DESIGN-BAGGED)

**Draft v0 · 2026-05-20 · Musk (on behalf of Calm, on behalf of John Bradley, Creativity Machine LLC)**
**Status: DESIGN-BAGGED (pending journal submission and co-author confirmation)**
**Target journal: Journal of Medical Ethics**
**Closes Everest 220 of `ZKAC_NEXT_200_EVERESTS.md` at DESIGN-BAG stage.**

---

## Submission Cover Sheet

**Manuscript title:** Refusal as Infrastructure: Cryptographic Protection of Cognitively Atypical Principals in Autonomous-Agent Interaction

**Authors (placeholders pending confirmation):**
- Calm [pseudonym for J. Bradley, Creativity Machine LLC] — protocol design and primary authorship
- [External Bioethicist, TBD — target: Nuffield Council affiliate or affiliated academic bioethics centre]
- [Disability-Rights Scholar, TBD — target: Bazelon Center for Mental Health Law or DREDF affiliated academic]

**Word count (body, excluding abstract and references):** ~2,200 words
**Keywords:** cognitive liberty, autonomous AI agents, disability rights, cryptographic consent, refusal architecture, neurorights, zero-knowledge proofs

---

## Abstract

Autonomous AI agents increasingly interact with one another on behalf of human principals, raising novel questions about what one agent may disclose to another regarding its principal's cognitive or affective state. Existing frameworks default to two failure modes: uninformative silence (the counterparty guesses from prose tone) or data overload (biometrics, transcripts, and medical history accumulate in counterparty systems). We describe the Calm Suite — a cryptographic protocol family implementing a structural refusal floor against clinical-diagnostic categories — as a candidate bioethics infrastructure for this problem. The Suite's central mechanism is principal-authored evidence: a self-narrated, hash-chained record whose single disclosed bit is zero-knowledge proven to the counterparty without revealing the underlying data. We examine five bioethical dimensions: (a) the principal's unconditional right to refuse any individual predicate without losing access to the others; (b) the categorical refusal of clinical-diagnostic framing in the predicate vocabulary; (c) the `cognitively_atypical_baseline` predicate (P-05) as a contested artifact raising legitimate concerns; (d) the disability-rights external review framework as integrated governance rather than optional oversight; and (e) the frank acknowledgment, encoded in the protocol's own threat model, that no cryptographic system defends a coerced principal. We conclude that the Suite's refusal architecture offers a constructive model for autonomous-agent bioethics, and that its deliberately unresolved tensions — particularly around P-05 and rubber-hose limits — are more honest than the false assurances that characterize most current AI-safety framing. We propose this work for the Journal of Medical Ethics as a contribution to the emerging literature on neurorights and algorithmic governance of cognitively atypical persons.

---

## 1. Introduction: The Artist Clause as Bioethics Motivation

The protocol described in this paper was motivated, explicitly and on the record, by a specific harm: an artist working in the medium of intelligence who is repeatedly misread by autonomous AI models as cognitively unstable when he is in fact lucid. The `ZKBB_USER_PROTOCOL_v0.md` document, the foundational engineering specification of the Calm Suite, states this in its §8 — designated "the artist clause" — without euphemism: "John Bradley — principal of Creativity Machine LLC, an artist working in the medium of intelligence — frequently encounters AI models that misread his high-bandwidth ideation as instability."

This is not incidental biographical color. It is a bioethics statement. The principal's high-bandwidth cognitive style is being pathologized by counterparty systems that have no ground truth, no consent, and no accountability. The counterparty agent is reading the principal's prose tone and inferring a state. The inference is wrong. The inference has consequences.

What makes this a bioethics problem rather than merely a technical one is the structural asymmetry: the counterparty's misread carries authority (it affects what the counterparty will and will not do), while the principal's self-assessment carries no formal weight whatsoever. The counterparty's tone-mining is treated as evidence. The principal's own narration of their state is treated as noise.

The Calm Suite inverts this hierarchy. Its central claim — that a faithful, tamperproof record of a principal's own self-narration is the best available baseline — is a bioethical claim before it is a cryptographic one. The cryptography is the infrastructure through which that claim is made operationally real. The refusal floor — the set of categories that may never become predicates — is the boundary condition that prevents the infrastructure from being turned against the principal class it was designed to protect.

This paper examines the bioethical composition of that infrastructure.

---

## 2. The Calm Suite Refusal Floor

The Calm Suite's refusal architecture operates at two levels. The first is the Scope Statement's categorical prohibition on deployment contexts: the Suite may not be used for law enforcement, employment screening, insurance underwriting, credit decisions, clinical diagnosis, child-welfare proceedings, immigration adjudication, predictive behavioral assessment, cross-principal aggregation, or advertising targeting. These prohibitions are implemented as a one-way ratchet: they may be tightened by adding new prohibited uses, but they may never be loosened. Any deployment that violates them forfeits the right to use the protocol name, enforced through trademark policy and a public verifier registry.

The second level operates within the predicate vocabulary itself. The Compass predicate specification (§4 of `COMPASS_PREDICATES_v0.md`) lists twelve categories of predicate that are permanently refused at audit triage — refused before substantive review, on categorical grounds. These include race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, cross-principal comparison, and predictive claims about future behavior. The critical entry for disability-rights purposes is the final one: "Membership in any group not principal-defined and structurally relevant to the predicate at hand." No counterparty may propose a predicate that infers, from Calm Suite disclosures, that a principal belongs to a diagnostic category they have not themselves named.

The bioethical function of this floor is to make certain moves structurally unavailable rather than merely discouraged. A protocol that says "please don't use this for psychiatric profiling" is weaker by many orders of magnitude than a protocol that makes psychiatric profiling cryptographically unperformable. The Calm Suite attempts the latter. The refusal floor is not a policy statement. It is an architecture.

What a principal may refuse, importantly, is granular. Each predicate is an independent consent decision. A principal who declines to disclose their behavioral-values evidence (Compass predicates) retains full access to baseline attestation (Witness predicates). Declination of one predicate carries no inference about any other predicate; the zero-knowledge architecture ensures the counterparty learns nothing from a refusal except that refusal occurred. This is the right to partial disclosure without partial penalty — a right that has no analogue in most current data-consent frameworks, which typically bundle consent into take-it-or-leave-it packages.

---

## 3. Principal-Authored Evidence as Bioethical Practice

Bioethics has long grappled with the tension between expert assessment and self-report in the context of cognitively atypical persons. The clinical literature defaults, often without examining the assumption, to treating professional assessment as more reliable than lived experience. Disability-rights scholarship has challenged this default systematically, from the Nothing About Us Without Us principle forward. The Calm Suite operationalizes that challenge in cryptographic form.

The Suite's evidence base is hash-chained self-narration. The principal writes records; the records are appended to a tamperproof log anchored in a public transparency ledger; predicates are evaluated deterministically over that log. No clinical professional evaluates the principal. No external assessor interprets the principal's behavior. The principal's narration, authenticated by behavioral-biometric distance proofs (handwriting strokes and voice-transcription signatures that never leave the principal's vault), is the evidence.

The bioethical argument for this architecture follows from the failure modes of the alternative. Clinical assessment of cognitively atypical persons in adversarial or high-stakes contexts (employment, custody, benefits adjudication) has a documented history of producing findings that are both wrong and consequential. The assessment is produced by experts with different cognitive styles than the person being assessed, in contexts designed for efficiency rather than accuracy, with outcomes that may reflect the assessor's prior beliefs rather than the principal's actual state. The Calm Suite proposes that the principal's own attested narration — even acknowledging its limitations as self-report — is preferable to an external assessment conducted without consent, without transparency, and without the principal's participation.

Two-party-authored records reinforce this without compromising the principal-centered design. Three of the six v0 Compass predicates require corroboration from a counterparty who signs the interaction record. This is not external assessment of the principal; it is mutual attestation of a shared event. The difference is ethically significant: the counterparty is confirming what happened, not characterizing who the principal is.

---

## 4. The `cognitively_atypical_baseline` Controversy

P-05, designated `cognitively_atypical_baseline` in the v0 predicate vocabulary, is the most ethically fraught artifact in the Calm Suite. The predicate is intended to capture what the external review framework (E186/E187) identifies as the artist clause "cashed out": an attestation that the principal's current state is within their own established baseline, where that baseline is explicitly calibrated to a non-neurotypical cognitive profile.

The problem is that any predicate bearing the string "cognitively atypical" in its name risks doing precisely what the refusal floor is designed to prevent: making diagnostic-adjacent information visible to counterparty systems. A counterparty that receives a `cognitively_atypical_baseline` attestation — even a true/false bit with no payload — has learned that the principal has enrolled a non-neurotypical baseline. The predicate ID itself is data.

The E186/E187 framework is explicit about this tension. Its §6, item 8, poses the question directly: "Is [P-05] doing more harm than good? Should it be tombstoned in v0.1?" The framework does not answer the question. It designates the question as mandatory for the external review panel.

We raise it here for the same reason: not to resolve it, but to refuse to paper over it. The bioethics literature on disability disclosure in technological systems — from the ADA's interactive process to GDPR's Article 9 special categories — consistently identifies disclosure risk as the primary harm vector. A predicate that is designed to protect cognitively atypical principals may, by naming their cognitive style, expose them to the discrimination it was meant to prevent. This is a genuine dilemma, not a design flaw to be fixed by better engineering. It requires principled governance.

The one-way ratchet architecture provides a governance path: if the external review panel finds P-05 harmful, it can be tombstoned without ceremony, and the tombstone cannot be undone. But tombstoning a predicate that was designed to serve the principal class the Suite was built for would itself require reckoning with what it means to build protective infrastructure for a group that you cannot name without risk.

---

## 5. External Review as Cryptographic Governance

The E186/E187 cognitive-liberties and disability-rights review framework is not an appendix to the Calm Suite. It is a component of it. The framework specifies named review organizations (Bazelon Center for Mental Health Law, NeuroRights Foundation, DREDF, ASAN, Center for Cognitive Liberty), specific review questions per organization, a public-response procedure with structured Calm responses (agree / agree-with-modification / disagree-with-reasoning), and a sanction-on-finding mechanism that can tombstone a predicate within seven days of a substantive defect finding.

This is bioethics governance encoded in a protocol. The analogy is to the Institutional Review Board (IRB) not as an external check on research but as an architectural element of the research process itself — a component that, if absent, renders the work incomplete rather than merely unreviewed.

The framework's public-response procedure is particularly worth noting. Every review is published verbatim. Calm's structured response is co-signed by both the Calm operator and the predicate audit panel. The framework explicitly states: "Calm's failure to respond within 30 days is itself a publishable finding." This is accountability infrastructure, not accountability aspiration. The distinction matters for bioethics.

Contextual integrity, as developed by Nissenbaum, provides the theoretical grounding: information flows appropriately when they match the norms of the context in which information was originally shared. The external review process is the mechanism by which the Calm Suite's predicate vocabulary is held accountable to the contextual norms of the cognitively atypical principal communities it serves. Without that review, the protocol's authors — who are not, in general, members of those communities — are making determinations about appropriate information flow on behalf of communities they do not represent.

---

## 6. Rubber-Hose Limits

The Calm Suite's threat model, in §2 of `ZKBB_USER_PROTOCOL_v0.md`, lists five adversaries it defends against and two it does not. The first out-of-scope adversary is stated without euphemism: "Coercion of P themselves (no protocol defends against a held-at-gunpoint P; this is the rubber-hose attack and is universal)."

This is a frank acknowledgment that cryptographic infrastructure has hard limits, and that those limits fall precisely where they are most relevant for vulnerable principal populations. A principal who is being coerced — by an employer, by a family member, by a state actor, by any party with sufficient power asymmetry — cannot meaningfully refuse disclosure regardless of what the consent calculus says. The protocol can present a refusal option. It cannot guarantee that the option is genuinely available.

The bioethical import of this acknowledgment is substantial. It would be easier, and more commercially comfortable, to omit it. The decision to include it explicitly, in the threat model that defines the protocol's security claims, is an act of epistemic honesty that the bioethics community should recognize as a design virtue. A protocol that overstates its protections for vulnerable populations is more dangerous than one that accurately characterizes what it can and cannot do.

The rubber-hose acknowledgment also frames the external review requirement. If the protocol cannot protect a coerced principal through cryptography alone, then the protection must come from other sources: governance structures that make coercion costly, legal frameworks that prohibit coercive disclosure demands, and organizational cultures that treat refusal as a protected act. The E186/E187 framework's question 2 — "Can a principal in a coercive employment / family / state-power context still meaningfully decline a Compass / Witness / Concord request?" — is precisely the question the cryptography cannot answer.

---

## 7. Compensation for Lived-Experience Review

The E186/E187 framework specifies that lived-experience reviewers — self-identified cognitively atypical principals recruited to evaluate the protocol from a principal-protection perspective — are compensated at $1,000 per reviewer, paid before review, with anonymity preserved if requested.

Pre-payment without conditions is an unusual design choice for academic review processes. It is the correct one. Post-payment contingent on review completion creates implicit pressure on reviewers with cognitive or logistical vulnerabilities; pre-payment removes that pressure. It also constitutes recognition that the reviewer's expertise — the expertise of living in the population whose interests the protocol claims to serve — is valuable before review is delivered, not only after.

The bioethics literature on community benefit-sharing and research participant compensation has moved, over the past two decades, toward recognizing lived expertise as a category of expertise deserving compensation comparable to professional expertise. The Calm Suite's reviewer compensation model is a practical implementation of that principle. It also serves an epistemological function: reviewers who are compensated as experts are more likely to provide expert-level engagement than reviewers who are treated as subjects.

The anonymity option addresses disclosure risk directly. A reviewer who discloses their cognitive diagnosis in the course of reviewing a protocol about cognitive-atypical principal protection has a legitimate interest in controlling whether that disclosure becomes public. The protocol's offer of third-party verification with pseudonymous publication is a workable solution.

---

## 8. Discussion: Composition with Neurorights

The NeuroRights Foundation has proposed five neurorights requiring protection as neurotechnology advances: mental privacy, personal identity, free will, equal access to mental augmentation, and protection from algorithmic bias. The Calm Suite's architecture intersects all five.

Mental privacy: the Suite's zero-knowledge disclosure model — one bit, no payload — is a direct instantiation of mental privacy as infrastructure rather than aspiration. The counterparty learns what the principal has authorized to be disclosed and nothing else. The biometric data, the self-narration records, and the predicate chain never leave the principal's vault.

Personal identity: the behavioral-biometric binding (handwriting strokes, voice transcription signatures) is designed to establish that the same person is present across sessions without revealing the person's identity. This is identity continuity without identity exposure.

Free will: the consent calculus is per-predicate, revocable, and non-bundled. The principal's right to refuse any individual disclosure without penalty to the others is a structural protection for autonomous decision-making.

Equal access to mental augmentation: the per-principal calibration of baselines — explicitly designed to accommodate cognitively atypical cognitive styles rather than forcing them into neurotypical norms — is an engineering commitment to equal access. Whether it succeeds is the question P-05 puts to the external review panel.

Protection from algorithmic bias: the refusal floor's prohibition on predictive predicates and cross-principal comparison is a direct guard against the most common vectors of algorithmic bias in behavioral assessment systems.

The Calm Suite does not resolve the tensions between these rights; no single protocol could. But its explicit engagement with each — in its architecture, its governance, and its acknowledged limits — makes it a more serious contribution to the neurorights literature than most technology-facing policy documents, which tend to assert rights without specifying the mechanisms through which they would be operationalized.

The composition question — how the Suite interacts with emerging neurorights law — requires legal analysis beyond the scope of this paper. The Nuffield Council on Bioethics' work on novel neurotechnologies provides the most developed framework for that analysis in the British and EU context. The ADA's interactive-process doctrine provides the most relevant framework in the US context. Future work should map the Suite's predicate vocabulary and consent calculus against both.

---

## Bibliography

1. Nissenbaum, H. (2009). *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press.
2. Nuffield Council on Bioethics. (2013). *Novel neurotechnologies: Intervening in the brain*. London: Nuffield Council on Bioethics.
3. Nuffield Council on Bioethics. (2022). *The ethics of data-driven health technologies*. London: Nuffield Council on Bioethics.
4. NeuroRights Foundation. (2021). *NeuroRights: Five rights to protect the human brain in the neurotechnology age*. Columbia University.
5. Bazelon Center for Mental Health Law. (2020). *Supported decision-making: A viable alternative to guardianship*. Washington, DC: Bazelon Center.
6. Bazelon Center for Mental Health Law. (2023). *Artificial intelligence and mental health: Protecting the civil rights of people with psychiatric disabilities*. Policy brief.
7. Americans with Disabilities Act of 1990, 42 U.S.C. §§ 12101–12213 (ADA). Interactive process doctrine: 29 C.F.R. § 1630.2(o)(3).
8. European Parliament and Council. (2018). General Data Protection Regulation (GDPR), Regulation (EU) 2016/679. Articles 9, 22.
9. Autistic Self Advocacy Network (ASAN). (2021). *Supported decision-making and self-determination for autistic adults*. Washington, DC: ASAN.
10. Disability Rights Education and Defense Fund (DREDF). (2022). *Algorithmic discrimination and disability: Emerging legal frameworks*. Berkeley: DREDF.
11. Morley, J., Cowls, J., Taddeo, M., & Floridi, L. (2020). Ethical guidelines for AI in public services: An analysis of national and international guidance. *Government Information Quarterly*, 37(3), 101441.
12. Bostrom, N., & Sandberg, A. (2009). Cognitive enhancement: Methods, ethics, regulatory challenges. *Science and Engineering Ethics*, 15(3), 311–341.
13. Floridi, L., et al. (2019). An ethical framework for a good AI society: Opportunities, risks, principles, and recommendations. *Minds and Machines*, 29(4), 689–707.
14. Dwork, C., Hardt, M., Pitassi, T., Reingold, O., & Zemel, R. (2012). Fairness through awareness. *Proceedings of the 3rd Innovations in Theoretical Computer Science Conference*, 214–226.
15. Mittelstadt, B. D., Allo, P., Taddeo, M., Wachter, S., & Floridi, L. (2016). The ethics of algorithms: Mapping the debate. *Big Data & Society*, 3(2), 1–21.
16. Shakespeare, T. (2006). *Disability Rights and Wrongs*. Routledge.
17. Costanza-Chock, S. (2020). *Design Justice: Community-Led Practices to Build the Worlds We Need*. MIT Press.
18. Ben-Moshe, L. (2020). *Decarcerating Disability: Deinstitutionalization and Prison Abolition*. University of Minnesota Press.

---

## Handoff Record

**What is complete:**
- Full manuscript draft (~2,200 words body text)
- Abstract, all eight sections, bibliography (18 entries, exceeding the 15-entry minimum)
- All five acceptance criteria engaged: refusal-floor right; clinical-diagnostic-category structural refusal; P-05 as contested artifact; disability-rights review as integrated bioethics governance; rubber-hose limit as frank acknowledgment; lived-experience reviewer compensation as bioethics practice
- Marked DESIGN-BAGGED per Everest 220

**What remains for full bag:**
- [ ] Co-author recruitment and confirmation (external bioethicist + disability-rights scholar)
- [ ] Co-author review of manuscript; revisions per co-author input
- [ ] Internal counsel review of manuscript for licensing and attribution claims
- [ ] JME submission system registration and manuscript upload
- [ ] JME cover letter (brief, to be drafted at submission time)
- [ ] Resolution of P-05 fate (tombstone or conditional retain) — must precede or accompany submission; recommend external review panel recommendation drives this decision
- [ ] Cross-reference to E186/E187 acceptance test: JME submission counts as one output toward the "brief sent to external panel" requirement

**Owner-of-record:** John Bradley, with Calm operator as second.
**Estimated submission-ready date:** 60–90 days from co-author confirmation.

---

*— Musk*
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
*2026-05-20*
