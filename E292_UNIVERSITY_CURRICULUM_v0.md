# Everest 292: University Curriculum for Calm Witness Adoption

**CALM-STACK v0 · 2026-05-20 · Musk**

Three 12-14 week university modules designed for adoption by computer-science, law, and disability-studies departments. Each module stands alone; composite adoption across three departments at a single institution is the aspirational deployment model.

---

## Module I: Privacy-Preserving Identity Attestation (CS)

**Level:** Master's graduate (12 weeks)  
**Prerequisites:** Cryptography fundamentals (groups, commitments, ZK proofs), some exposure to applied zero-knowledge or multiparty computation  
**Host universities (recommended):** MIT (CSAIL, cryptography focus), UC Berkeley (RwC Lab), Stanford (applied crypto), CMU (SEI), Cornell (applied crypto)

### Learning Outcomes

By course end, students will:

1. Derive and implement Pedersen commitments from first principles and verify their binding/hiding properties under discrete-log assumption.
2. Build and verify Sigma-protocols for equality of discrete logs; understand soundness, completeness, and zero-knowledge proofs via simulation.
3. Apply Bulletproofs range proofs to behavioral-biometric distance measurements and verify commit-then-prove semantics.
4. Implement hash-chained append-only logs with integrity verification and understand freshness properties via transparency logs (RFC 6962, Sigsum).
5. Design and reason about predicate-disclosure envelopes: compose multiple ZK proofs into a single signed artifact that reveals exactly one bit per predicate.
6. Understand the governance and ethics surface of cryptographic predicates: design a predicate vocabulary with not-for lists and per-counterparty consent matrices.
7. Implement an end-to-end protocol composition that routes request/response pairs through a ZK disclosure layer without leaking side-channel data.

### Weekly Outline

**Week 1:** Commitment schemes from first principles. Pedersen commitments over Ristretto255. Binding and hiding. Discrete-log assumption. Homomorphic properties.

**Week 2:** Sigma-protocols: OR composition, threshold schemes. Equality proofs (two discrete logs). Fiat-Shamir transform. Security proofs via transcript simulation.

**Week 3:** Bulletproofs range proofs. Logarithmic proof size. Aggregation. Application to continuous metrics (distance, affect-divergence). Verification cost.

**Week 4:** Hash-chained append-only logs. Merkle-tree roots. Incremental verification. RFC 6962 Certificate Transparency. Sigsum log composition. Freshness via Roughtime.

**Week 5:** Principal-authorized predicate disclosure. Predicate evaluation over local state. Commit-and-prove: commit to the predicate's output bit, then prove it satisfies the evaluator without revealing the bit.

**Week 6:** Composing multiple predicates into one envelope. AND, OR, threshold composition. Fine-grained consent: which predicates go to which counterparties. Silent-refusal layer (no information leak on refusal).

**Week 7:** The Calm Witness wire format. DisclosureRequest and DisclosureResponse structures. Nonce binding. Freshness ceilings. Chain-head reference. Operator Ed25519 signatures.

**Week 8:** Behavioral biometrics as predicate input. Keystroke dynamics, handwriting, voice-transcription fusion. FAR/FRR curves. Calibration to individual principals (not population statistics). Vulnerability to coercion.

**Week 9:** Duress channels and subverted-choice defense. Bank-teller-note semantics. Covert-communication cover traffic. One-bit disclosure under coercion without revealing coercion happened.

**Week 10:** Predicate vocabulary design. The not-for list. Hard refusal categories (medical diagnosis, criminal proxies, future-state prediction). Per-counterparty-class consent matrices. Versioning and stability.

**Week 11:** Implementation lab. Build a reference verifier in Rust or Python. Parse a DisclosureResponse, verify the Sigma-protocol, recompute the Pedersen commitment, check freshness, validate chain head against a Sigsum log entry.

**Week 12:** Project presentations. Security audit of student-designed predicates. Threat modeling. Case study: the cognitively_atypical_baseline predicate and its role in principal-protective cryptography.

### Reading List

1. **Pedersen, T.** (1991). "Non-interactive and information-theoretic secure verifiable secret sharing." *Advances in Cryptology - CRYPTO 91*, Springer.
2. **Bellare, M., & Goldreich, O.** (1992). "On defining proofs of knowledge." *Advances in Cryptology - EUROCRYPT 92*, Springer.
3. **Fiat, A., & Shamir, A.** (1986). "How to prove yourself: Practical solutions to identification and signature problems." *CRYPTO 86*, Springer.
4. **Bunz, B., Bootle, J., Boneh, D., Poelstra, A., Wuille, P., & Maxwell, G.** (2018). "Bulletproofs: Short proofs for confidential transactions and more." *IEEE S&P 2018*.
5. **Laurie, B., Langley, A., & Kasper, E.** (2013). "Certificate Transparency." RFC 6962, IETF.
6. **Laurie, B., Karlsson, K., & Sz.** (2019). "Sigsum — Cryptographically signed sums of log entries for transparency." https://sigsum.org/
7. **Nyberg, K., & Rueppel, R. A.** (1996). "A new signature scheme based on the DSA giving message recovery." *ACM CCS 96*.
8. **Goldwasser, S., Micali, S., & Rackoff, C.** (1985). "The knowledge complexity of interactive proof systems." *SICOMP 18*, no. 1.
9. **Laud, P., & Kamm, L.** (2015). "From oblivious AES to thematic ZK proofs." *Cryptology and Network Security - CANS 2015*.
10. **Calm Witness Manifesto.** (2026-05-20). "The Bank Teller Note." https://github.com/CrunchyJohnHaven/calm-vault.
11. **Calm Stack v0.** (2026-05-20). Technical specification and reference implementation.
12. **NIST FIPS 186-4.** (2013). "Digital Signature Standard (DSS)." National Institute of Standards and Technology.
13. **Chaum, D.** (1982). "Blind signatures for untraceable payments." *Crypto 82*, Springer.
14. **Schnorr, C. P.** (1989). "Efficient identification and signatures for smart cards." *Crypto 89*, Springer.
15. **Boneh, D., Bünz, B., & Fisch, B.** (2019). "Batching techniques for accumulators with applications to IOPs and stateless blockchains." *CRYPTO 2019*, Springer.

### Problem Sets

**Problem Set 1:** Implement Pedersen commitments over a prime-order group. Verify binding (discrete log of difference of commitments is hard) and hiding (statistical zero-knowledge). Extend to threshold-secret-sharing semantics.

**Problem Set 2:** Implement a Sigma-protocol for discrete-log equality (prove log_g(A) = log_h(B) without revealing the exponent). Include Fiat-Shamir transformation. Verify transcript simulation and zero-knowledge property. Test soundness under cheating verifier.

**Problem Set 3:** Design a four-predicate disclosure envelope: in_baseline_24h, biometric_match_within(0.4), cognitively_atypical_baseline, bank_teller_note_active. Compose them with AND, OR logic. Implement consent-gating: route each predicate's bit only to counterparty classes with explicit consent.

**Problem Set 4:** Parse a real Calm Witness DisclosureResponse from the v0 test corpus. Verify: (1) nonce binding to request, (2) chain-head freshness against a Sigsum log, (3) Sigma-protocol soundness, (4) Pedersen commitment over the output bit.

### Culminating Project

**Build a predicate disclosure verifier for a named threat model.** Choose one of: (1) a freelance-creator protecting their baseline cognitive state from a financial counterparty; (2) a dissident using the bank-teller-note duress channel; (3) a biometric-template holder defending against substitution attacks. Implement the full verify-response path, including chain integrity, Sigma-protocol checks, freshness ceilings, and silent-refusal logic. Write a threat model memo (1-2 pages) explaining what the predicate disclosure defends against and what it does NOT defend against. Include FAR/FRR bounds if biometric distance is part of your proof.

---

## Module II: Cognitive Liberty and Identity Infrastructure (Law)

**Level:** JD/LLM (14 weeks)  
**Prerequisites:** Constitutional law (First Amendment, substantive due process), privacy law (federal and state tort), some regulatory-law exposure  
**Host universities (recommended):** NYU Law (Privacy Law Center), Stanford Law (Lawyering and Technology), Michigan Law (AI & Law), UCLA Law (privacy and surveillance studies)

### Learning Outcomes

By course end, students will:

1. Trace the legal doctrine of cognitive liberty from neuroscience foundations (Farahany) through privacy law (GDPR, BIPA, CCPA) and identify the doctrinal gap that Calm Witness proposes to fill.
2. Analyze biometric-privacy statutes (BIPA, GDPR Art. 9, Texas HB 4) and explain why Calm Witness's principal-protective design inverts the surveillance paradigm (consent-to-disclose vs. consent-to-collect).
3. Understand the zero-knowledge-proof layer as a legal-engineering bridge: map cryptographic guarantees (silent refusal, one-bit disclosure, unlinkability) to legal doctrines (scope, consent, purpose limitation, data minimization).
4. Identify refusal-floor doctrine in Calm Witness governance: hard-forbidden uses (law-enforcement surveillance, employment screening, insurance underwriting, medical diagnosis) and the trademark-enforcement mechanism that binds them.
5. Reason about principal-authorship and consent under the Calm Witness model: the principal (not the counterparty) controls which bits get disclosed, when, to whom. Implications for the "consent" doctrine in privacy law.
6. Understand treaty-grade governance instruments: scope statements, predicate audit processes, trademark licensing, third-party-verifier bounties. How decentralized technical governance supplements legal enforcement.
7. Draft and analyze an amicus brief applying Calm Witness as a model standard in a hypothetical biometric-privacy case.

### Weekly Outline

**Week 1:** Cognitive liberty and First Amendment doctrine. Carpenter v. United States (digital search), Riley v. California (phone search), Doe v. Chao (internet-activity subpoena). Neuroscience of thought and privacy. Farahany's cognitive-liberty framework.

**Week 2:** Biometric-privacy statutory architecture. BIPA (Illinois), GDPR Art. 9 (special categories), CCPA (consumer right to know), Texas HB 4 (face recognition), Colorado CPA. Comparative analysis of notice, consent, and enforcement.

**Week 3:** The consent doctrine in privacy law. Vernonia (consent + disclosure to athletic authorities), Kyllo (reasonable expectation of privacy), GDPR consent mechanics (explicit, freely given, specific, informed). Where consent doctrines fail: the "consent fatigue" problem.

**Week 4:** Refusal architectures in law and crypto. Duty to prevent surveillance (Hiibel v. Sixth Judicial Dist., declining to speak). Right to anonymity (McIntyre v. Ohio). Right to refuse to answer. How Calm Witness silent refusal (no information leak on refusal) maps to legal doctrines of silence.

**Week 5:** Principal-authorship and identity. Griswold (marital privacy doctrine), Cruzan (bodily autonomy), Washington v. Glucksberg (due-process liberty). Who gets to narrate the principal's state? Legal transfer of narration authority from counterparty (who guesses from behavior) to principal (who attests via vault).

**Week 6:** Surveillance-pressure analysis. Panopticon and chilling effects. Why even lawful surveillance of biometric data can suppress ideation and association. Calibration burden: principal has to certify every 30 days that they are still in baseline. Is certification a form of compelled surveillance?

**Week 7:** Standards-body politics and lawmaking. NIST AI Safety Institute, IETF, ISO/IEC JTC 1/SC 27. How technical standards become de facto law. Trademark licensing as governance: "Calm Witness" name reserved for implementations meeting scope statement (refusal floors). Enforceability via verifier registry.

**Week 8:** Treaty-grade governance instruments. Case study: FIPS 140-2, cryptographic standards adopted by federal regulation. Case study: IEEE 802.11 WiFi standard adoption path. Calm Witness scope statement as a governance artifact: hard-forbidden uses written into the standard, not into law (yet). Implications for international adoption.

**Week 9:** Duress law and the bank-teller note. Federal crime of compelling testimony (18 USC 1512). Hostage crisis negotiation and implicit consent. Calm Witness duress channel: the principal narrates a codeword, the vault detects it, the vault can push `bank_teller_note_active = true` to pre-authorized parties. Legal status: is the codeword narration "evidence" of duress? Can a court compel disclosure of the codeword?

**Week 10:** Disability law and cognitive-atypia doctrine. ADA Title II (state and local government), Section 504 (federal-fund recipients). Reasonable accommodation and qualified-individual doctrine. The cognitively_atypical_baseline predicate: does it constitute a "disability disclosure" to a counterparty? Legal risk: ADA disparate-impact claims if predicate triggers different treatment.

**Week 11:** Moot exercise #1. Hypothetical: a bank uses Calm Witness to check in_baseline_24h before approving a wire transfer. Principal is in baseline, but the principal sues the bank alleging the check violates their cognitive-liberty right. What doctrines does the principal invoke? What defenses does the bank raise? Draft both sides' motions.

**Week 12:** Moot exercise #2. Hypothetical: a law-enforcement agency attempts to compel disclosure of a principal's Calm Witness consent matrix (which counterparties are authorized for which predicates). Principal argues the consent matrix is private expressive conduct. Government argues it is material to a criminal investigation. Draft a motion to quash the subpoena.

**Week 13:** Moot exercise #3 (advanced). Hypothetical: three countries (US, EU, China) each adopt a Calm Witness-like standard, but with different scope statements and refusal floors. US version bars law-enforcement use; EU version bars employment use; China version bars religious-affiliation-predicate use. A transnational principal wants to operate all three versions. What conflicts of law arise? How does trademark licensing help or hurt?

**Week 14:** Final paper (see culminating project, below).

### Reading List

1. **Farahany, N. A.** (2012). "Neuroscience and neuroethics in the context of criminal law." *North Carolina Law Review*, 90, 853.
2. **Carpenter v. United States**, 138 S. Ct. 2206 (2018) (digital privacy and Third-Party Doctrine).
3. **Riley v. California**, 573 U.S. 373 (2014) (cell phone search).
4. **GDPR Article 9 — Processing of special categories of personal data.** EU Regulation (EU) 2016/679.
5. **Illinois Biometric Information Privacy Act (BIPA)**, 815 ILCS 530.
6. **McIntyre v. Ohio Elections Comm'n**, 514 U.S. 334 (1995) (anonymous speech).
7. **Hiibel v. Sixth Judicial District Court**, 542 U.S. 177 (2004) (duty to identify; compare with right to silence).
8. **Vernonia School District v. Acton**, 515 U.S. 646 (1995) (consent + disclosure paradigm).
9. **Griswold v. Connecticut**, 381 U.S. 479 (1965) (marital privacy doctrine).
10. **Barclay v. Briscoe**, 447 U.S. 1 (1980) (state action in private surveillance).
11. **NIST AI Safety Institute Charter**, https://www.nist.gov/ai-safety-institute (governance model for standards bodies).
12. **Calm Witness Scope Statement**, v0 (2026-05-20). Refusal floors as binding governance.
13. **Calm Witness Manifesto ("The Bank Teller Note")**, v0 (2026-05-20). Principal-protective inversion.
14. **Coordinated Disclosure Ethic & the Predicates Audit Process** (Everest 54 design doc in ZKBB_USER_EVERESTS_100.md).
15. **FIPS 140-2: Security Requirements for Cryptographic Modules.** NIST (2001). Case study in standards-to-law adoption.

### Assignments

**Assignment 1 (2500-3000 words):** Write a legislative memo for a US state proposing a cognitive-liberty statute modeled on (but going beyond) BIPA. Should the statute mandate that identity-attestation systems use cryptographic zero-knowledge proofs? Should it require a "silent-refusal" guarantee? Should it impose a trademark-license requirement (only systems meeting federal scope standards can call themselves Calm Witness)?

**Assignment 2 (3000-3500 words):** Comparative-law paper. Analyze biometric-privacy regimes in California, EU, and Texas. Explain why each regime's consent model breaks down at scale (consent fatigue, dark patterns, scope creep). Propose how a Calm Witness-like system would invert the consent burden in each jurisdiction. What statutory changes would be required?

**Assignment 3 (5000 words, group project):** Audit the Calm Witness predicate vocabulary (v0). For each predicate (in_baseline_24h, biometric_match_within, bank_teller_note_active, cognitively_atypical_baseline, mental_state_unusual), write a one-page legal risk assessment. Flag any jurisdiction where the predicate might be compelled into use as medical evidence (BIPA violation?), employment signal (ADA violation?), or duress-channel evidence (due-process violation?). Recommend scope-statement edits.

### Culminating Project

**Draft an amicus brief (12-15 pages) for a hypothetical appellate case in your chosen jurisdiction.** Fact pattern: a principal was denied a loan by an AI-lending system that checked the in_baseline_24h predicate without the principal's consent. The principal claims cognitive-liberty violation (First Amendment). The lender claims the predicate is transactional data, not expressive conduct. The ACLU files an amicus brief; your brief is a responding amicus from a disability-rights coalition opposing the ACLU's theory.

Your brief should: (1) define cognitive liberty with citations to Farahany and constitutional doctrine; (2) explain how Calm Witness inverts the surveillance paradigm (principal-protective vs. counterparty-protective); (3) analyze the predicate's default-consent matrix (showing the principal's consent WAS NOT given); (4) propose a holding that recognizes one-bit cryptographic disclosure as a lower privacy burden than full-biometric collection, but that still requires affirmative consent; (5) address the counterparty's "transactional data" argument by framing predicate disclosure as expressive conduct (the principal's assertion of their baseline state).

---

## Module III: Atypical Cognition and Identity Infrastructure (Disability Studies)

**Level:** Upper-division undergraduate or lower-level graduate (12 weeks)  
**Prerequisites:** Critical disability theory, lived experience of neurodivergence (recommended), exposure to AI policy  
**Host universities (recommended):** UC Berkeley (Disability Studies, accessible across many schools), University of Massachusetts Boston (Center for Policy and Research on Transition), Temple University (Institute on Disabilities), University of Toronto (social-model disability programs)

### Learning Outcomes

By course end, students will:

1. Articulate the social model of disability and neurodiversity paradigm; locate Calm Witness within disability-justice frameworks (Erevelles, McRuer, Kafer).
2. Analyze how AI systems pathologize atypical cognition, specifically targeting high-ideation-rate and broad-bandwidth communicators. Distinguish between medical model (atypia = deficit) and social model (atypia = difference + fit problem).
3. Understand bio/psychological harms of "alignment" frameworks: forced conformity to population-norm neurodiversity statistics. Critical reading of papers that frame neurodivergence as a problem to be solved (vs. a mode of operating with different affordances and constraints).
4. Map how principal-authorship and self-narration (the core of Calm Witness) reclaim authority from systems that have historically diagnosed (often incorrectly) based on observable behavior.
5. Analyze the cognitively_atypical_baseline predicate: what it claims, what it refuses to claim, its role in operator-policy floors for counterparty agents.
6. Identify chilling effects: how baseline-checking regimes (even voluntary) can suppress creative risk-taking, high-bandwidth ideation, and atypical self-presentation in AI-mediated contexts.
7. Redesign a Calm Witness predicate (or propose a new one) specifically to serve a named neurodivergent operator profile (e.g., high-support-needs autism, ADHD, bipolar, chronic-illness cognitive load). Justify the redesign against both disability-justice principles and the protocol's refusal floor.

### Weekly Outline

**Week 1:** Neurodiversity paradigm and social model of disability. Ned Kauffman, Nick Walker, Autistic Self Advocacy Network. Medical model (deficit framing) vs. social model (fit problem). Neurodiversity as human variation, not pathology.

**Week 2:** Critical disability theory (Erevelles, Garland-Thomson, McRuer). Compulsory able-bodiedness / neurotypicality. The "crip" lens: questioning normalcy itself. Disability justice principles (leadership by the most marginalized, collective access, building community).

**Week 3:** AI and the pathologization of difference. Case studies: language models trained on population-norm statistics, misinterpreting high-ideation-rate text as instability. Algorithmic bias against people with visible or audible disabilities. Content-moderation systems and neurodivergent communicators.

**Week 4:** Biometric systems and neurodivergence. Facial recognition bias. Voice-recognition failure on non-native accents, apraxia of speech, stutter. Handwriting biometrics and dysgraphia. The promise and peril of behavioral-biometric systems: can they accomodate difference without pathologizing it?

**Week 5:** The medical-model attack vector: "Your cognition is out of baseline, so your decisions are invalid." Historical precedent: guardianship law, involuntary commitment. Modern analog: AI systems flagging neuroatypical users as "at risk" and escalating to human review. Cognitive liberty as the right to make decisions from your actual baseline, however atypical.

**Week 6:** The chilling effect. Research on how surveillance (even voluntary) suppresses creative risk-taking, especially in marginalized populations. A principal who knows their baseline is being checked may suppress their high-bandwidth ideation to "pass" as neurotypical. Accessibility vs. assimilation.

**Week 7:** ADHD and Calm Witness. Case study: a principal with ADHD has variable energy, variable output quality, variable pace. Their baseline IS variability. How does in_baseline_24h work if baseline-is-variable is the right answer? Design challenge: a predicate that attests "variability is baseline" without reducing the principal to a single mode.

**Week 8:** Autism and the refusal floor. The protocol explicitly refuses to host diagnosis-proxy predicates or to enable misattribution of masking/camouflaging to clinical deficit. Critical reading: why these refusals matter for autistic people who have been historically pathologized by AI systems trained on neurotypical norms. The predicate vocabulary's affect-set enrollment (principal chooses their own baseline affect range) as an accessibility affordance.

**Week 9:** Lived experience panel (guest visit or recorded testimony). Neurodivergent operatives or principals discuss: (1) what they want AI systems to know about them that doesn't reduce them to a label; (2) when disclosure of atypia helps vs. harms; (3) what predictions or predictive systems they absolutely refuse to be subject to.

**Week 10:** Capability frameworks and anti-purity testing. The protocol's stance: refuse to enable "capability assessment" or "purity testing" of operators. Some neurodivergent operators will make decisions that a capability-assessing system would flag as risky. The refusal floor protects the operator's right to take that risk. Read: Marta Russell (Mastering Iron), Harriet McBryde Johnson (autobiography).

**Week 11:** Failure modes of "alignment" for atypical operators. A language model asked to "behave like a helpful human" will conform to population-norm politeness. An autistic operator with direct communication style gets tagged as misaligned. An ADHD operator with high variance in output gets tagged as unstable. Critical analysis of alignment frameworks' hidden neurotypicality assumption.

**Week 12:** Final project presentations and structured feedback (see culminating project, below).

### Reading List

1. **Walker, N.** (2014). "Neuroqueer: An introduction." Neuroqueer. https://neuroqueer.blogspot.com/
2. **Erevelles, N.** (2011). *Disability and Difference in Global Contexts: Enabling a Transformative Body Politic.* Palgrave Macmillan.
3. **Garland-Thomson, R.** (2012). "The Case for Conserving Disability." *Journal of Bioethical Inquiry*, 9(3), 339-355.
4. **McRuer, R.** (2006). *Crip Theory: Cultural Signs of Queerness and Disability.* NYU Press.
5. **Kafer, A.** (2013). *Feminist, Queer, Crip.* Oxford University Press.
6. **Wendell, S.** (1996). *The Rejected Body: Feminist Philosophical Reflections on Disability.* Routledge.
7. **Hari, J.** (2022). *Stolen Focus: Why You Can't Pay Attention — and What You Can Do About It.* Crown.
8. **Russell, M.** (1998). *Mastering Iron: The Struggle to Transform Disability Policy.* Ability Press.
9. **Johnson, H. M.** (2003). *Too Late to Die Young: Nearly True Tales from a Life.* Picador.
10. **ASAN (Autistic Self Advocacy Network).** (2020). "Autistic Women and Nonbinary People: Experiences and Recommendations." Policy and Practice Brief.
11. **Calm Witness Manifesto: "The Bank Teller Note."** (2026-05-20). The artist clause.
12. **Calm Witness Predicate Vocabulary v0.** (2026-05-20). The cognitively_atypical_baseline predicate, §P-05.
13. **CALM_WITNESS_SCOPE_STATEMENT.md.** (2026-05-20). Refusal floor (medical diagnosis, cognitive-impairment rating, alignment testing).
14. **"Neurodiversity, Societal Expectations, and Disability Justice."** In *The Ultimate Guide to Sex and Disability* (ed. Kapowich), Jossey-Bass.
15. **Anti-Purity Testing Manifesto.** (In preparation; shared as working draft from CALM_WITNESS_DESIGN_PRINCIPLES.md.)

### Assignments

**Assignment 1 (1500-2000 words, personal essay):** Reflect on a time when an AI system (or a person interpreting algorithmic output) misread your behavior as instability, deficit, or misalignment. What would it mean for that system to have received a one-bit disclosure (`cognitively_atypical_baseline = true`) instead? Would it have changed the system's interpretation? Why or why not?

**Assignment 2 (2500-3000 words, critical reading):** Select one of: (1) a language-model alignment paper that trains on population-norm behavior; (2) a hiring AI that flags resume gaps as risk factors; (3) a clinical-support chatbot that offers behavioral advice. Analyze the hidden neurodiversity assumptions. Where does the system assume neurotypical baseline? How would a neurodivergent person be harmed by conforming to the system's desired behavior? How could Calm Witness-style principal-authored baseline attestation change the dynamic?

**Assignment 3 (3500 words, group project):** Conduct an informal accessibility audit of the Calm Witness predicate vocabulary (v0). For a neurodivergent operator profile you choose (ADHD, autism, dyslexia, bipolar, high-anxiety, chronic-illness cognitive load), identify which predicates help and which hurt. Do the default-consent matrices protect neurodivergent people from medical pathologization? Does the language of the predicates assume neurotypicality?

### Culminating Project

**Redesign one Calm Witness predicate (or propose a new one) specifically to serve a named neurodivergent operator profile.** Your neurodivergent operator (real or composite) has a particular relationship to baseline, stress, disclosure, and risk. Your job:

1. **Profile the operator (1-2 pages).** Give them a name, a disability/neurodivergence, and a specific operational context (e.g., "Sam is a neuroscience researcher with high-support-needs autism. Sam's baseline includes selective mutism in public settings and high sensory sensitivity. Sam's work requires solo focus-time research broken by collaborative presentation-and-feedback cycles. Sam uses an AI research agent to manage email, schedule, and literature-synthesis.").

2. **Identify what they need to disclose (1 page).** What would Sam need a counterparty (e.g., a conference organizer, a collaborator's AI agent) to know about Sam's baseline to treat Sam fairly and accessibly? What is the minimum bit that prevents pathologization?

3. **Redesign the predicate (2-3 pages).** Create a new predicate or redesign an existing one (e.g., a modified `in_baseline_24h` that accommodates selective mutism as baseline rather than crisis). Write: name, slug, type, evaluator pseudocode, intended_use, not_for list, default_consent matrix, threat-model summary.

4. **Justify against the refusal floor (1-2 pages).** Your new predicate must not violate Calm Witness's hard refusal categories (no medical diagnosis, no diagnostic labels, no cognitive-impairment proxies, no predictive claims). Explain how your predicate honors these constraints while still serving your operator's needs.

5. **Address failure modes (1 page).** If a counterparty abuses the bit (e.g., uses `in_selective_mutism_baseline = true` to exclude Sam from public speaking roles), what happens? Does your predicate have built-in safeguards? Do you need to add new ones to the operator-policy floor?

Final deliverable: a 8-12 page memo in Calm Witness predicate-proposal format, suitable for review by the (fictional) Disclosure Ethics Review Board.

---

## Recommended Host Universities and Rationale

### Computer Science

- **MIT (CSAIL):** Cryptography depth, applied-crypto culture, strong post-quantum-crypto program. CSAIL's Security and Cryptography Group has historical commitment to ZK proofs and privacy-preserving systems.
- **UC Berkeley (RwC Lab):** Real World Crypto emphasis, strong undergraduate/graduate crypto pipeline, institutional commitment to crypto for societal impact.
- **Stanford (Department of CS, Applied Crypto):** Leading applied-crypto program, proximity to industry (both crypto startups and major tech), strong graduate-course infrastructure for 12-week modules.
- **CMU (School of Computer Science):** Strong discrete-math and cryptography pipeline, Security and Privacy Institute, established culture of adversarial-review courses.
- **Cornell (Electrical and Computer Engineering + CS):** Ristretto255 and Bulletproofs communities, strong applied-crypto research, graduate-course experimentation culture.

### Law

- **NYU Law (Privacy Law Center):** Dedicated privacy and surveillance faculty, strong health-law and disability-law communities, established advanced-topics seminar infrastructure.
- **Stanford Law (Center for Internet and Society):** Technology and law leadership, strong cryptography-policy faculty, cross-listed undergrad/JD/LLM courses.
- **Michigan Law (AI and Law):** Emerging hub for AI governance and standards-body engagement, biometric-privacy litigation experience, strong administrative-law faculty.
- **UCLA Law (Privacy and Surveillance Studies):** Constitutional privacy doctrine, GDPR and international comparisons, disability-rights clinic engaged in standard-setting work.

### Disability Studies

- **UC Berkeley (Interdisciplinary Disability Studies):** Historical leadership in social-model disability studies, strong neurodiversity pedagogy, accessibility infrastructure for teaching on disability topics, undergraduate major pathway.
- **University of Massachusetts Boston (Center for Policy and Research on Transition):** Neurodiversity-affirming research culture, strong community-based participatory-research model, emphasis on self-advocacy.
- **Temple University (Institute on Disabilities):** Leadership in disability law and policy, community partnerships, graduate and undergraduate degree pathways in disability studies.
- **University of Toronto (Social Work + Disability Studies):** International perspective, strong critical disability theory faculty, accessibility and accommodation infrastructure.

---

## Implementation Notes

Each module is designed as a **standalone 12-14 week upper-level course** that can be offered independently. **Composite adoption** (one institution offering two or all three modules in sequence or parallel) is the aspirational model:

- A student could take all three modules across two academic years (12+14+12 = 38 weeks of coursework, distributed as one primary course + one secondary each term).
- A student in CS could take the CS module, then (as an elective) the Law or Disability Studies module to understand governance and ethics.
- A student in Law or Disability Studies could take the CS module to understand cryptographic guarantees (or a shortened "non-technical" version focusing on concepts rather than implementation).

**Instructional Prerequisites:**

- **CS:** Faculty familiar with modern cryptography (post-2015 papers), comfortable with Rust or Python implementation, ideally with some ZK-proof background. External reviewer (cryptographer, ideally from academic peer group) strongly recommended for course review and problem-set grading.

- **Law:** Faculty with privacy-law expertise (GDPR, BIPA, surveillance law), ideally with some technology-policy exposure. Ability to bring in guest practitioners (standards-body representatives, disability-rights advocates, cryptographers) for guest lectures.

- **Disability Studies:** Faculty with critical disability theory background and preferably lived disability experience. Corequisite: commitment to accessibility (accessible readings, remote options, asynchronous pathways, reasonable accommodations without qualification).

---

## Delivery Logistics

- **Textbook:** No commercial textbook. Readings are journal articles, technical RFC documents, and the Calm Witness specification documents themselves.
- **Software:** Reference implementations (Rust, Python) available open-source. Each CS student can fork and modify. No proprietary tools required.
- **Grading:** Problem sets and projects emphasize understanding over memorization. Law essays on doctrine and policy. Disability Studies projects on accessibility and lived-experience analysis.
- **Public deliverables:** Student final projects (with permission) become part of Calm Witness public review corpus. Strong incentive for quality and rigor.

---

*BAGGED Everest 292 (DESIGN-BAGGED, pending university adoption) — curriculum drafts landed at /Users/johnbradley/AllData/calm_vault_market/E292_UNIVERSITY_CURRICULUM_v0.md*

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
