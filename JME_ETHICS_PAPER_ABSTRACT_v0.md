# Values-Attestation Cryptography and the Refusal Floor: A Defense of Categorical Non-Disclosure in Principled AI Systems

*Closes Everest 220 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending venue submission)*

## Suggested Authors

**Primary:** Bioethicist with cryptographic systems expertise; AI ethics researcher; disability-rights scholar specializing in cognitive liberty and anti-paternalism

## Abstract

The Calm-suite values-attestation system implements a principled refusal to cryptographically attest evidence categories that map to protected characteristics (race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, charitable donations, contentious opinions, cross-principal comparisons, predictive predicates, non-principal-defined group membership). We argue this categorical refusal is not an arbitrary limitation but the *load-bearing safety property* of the entire values-cryptography architecture. The refusal floor ensures: (1) principals retain unobserved discretion over sensitive self-presentation, (2) the system cannot be repurposed as a surveillance infrastructure for harmful categorization, and (3) composition with disability-rights and cognitive-liberty commitments remains structurally possible. We situate this approach between anti-purity-test critiques (which demand flexibility) and privacy absolutism (which forbids use entirely), defending why certain architectural rigidities *enable* rather than constrain ethical deployment. The paper addresses the objection that categorical refusal is overly restrictive, demonstrating how one-way-ratchet expansion and political-economy awareness preserve safety while permitting legitimate evolution.

---

## Section Outline

**1. Background: Values-Attestation Cryptography and the Trust Problem**
- The shift from opaque AI values to principal-authored, cryptographically verifiable evidence
- Why existing transparency mechanisms fail under adversarial conditions
- The design constraint: enabling selective disclosure without enabling misuse

**2. The Technical Move: Zero-Knowledge Principal-Authored Evidence**
- How principals construct attestations from their own ethical frameworks
- The role of ZK proofs in disclosing values without exposing sensitive metadata
- The architectural difference between *disclosing values* and *naming sensitive categories*

**3. The Categorical-Refusal Commitment**
- Seven categories of evidence the Calm-suite refuses to attest (with justification for each)
- Why this refusal is not a bug but a feature: preventing function creep
- Parallel defenses in medical ethics (informed consent without diagnostic labels) and disability justice

**4. Why Anti-Purity-Test Logic Is Structurally Required**
- The temptation to permit "just this one exception" for legitimate-seeming uses
- How incremental exceptions compound into surveillance infrastructure
- The ratchet effect: refusals are harder to maintain than architectures without them
- Real-world precedent: medical privacy law's categorical refusals and their success

**5. One-Way-Ratchet Expansion and the Political Economy of Refusal Floors**
- How the refusal floor can expand (adding new categories) but not contract (removing protections)
- The governance structures that preserve this asymmetry
- Recognizing legitimate pressure for expansion vs. exploitation attempts
- The role of sunlight and auditability in managing boundary cases

**6. Composition with Disability Rights and Cognitive-Liberty Commitments**
- Alignment with neurodiversity frameworks (rejecting deficit-based categorization)
- Support for cognitive autonomy: principals define relevance, not external classifiers
- How refusal floors protect against discriminatory proxy inference
- Evidence that categorical non-attestation improves accessibility outcomes

**7. Objection: Isn't This Too Restrictive?**
- The case for pragmatic flexibility
- When third-party evidence might seem necessary
- The hidden costs of "just one exception"

**8. Reply: Structural Rigidity as Enabling**
- How principled constraints actually expand the design space for legitimate uses
- The difference between refusing to name categories and refusing to enable values-disclosure
- Real alternatives: changing what gets asked upstream rather than loosening attestation

**9. Conclusion: Refusal as Foundational**
- The refusal floor as the core safety innovation
- Open questions: expansion governance, auditing mechanisms, composition with future systems
- The ethical stake: whether cryptographic systems can remain tools of principals rather than becoming instruments of observation

---

## Suggested Venues

1. **Journal of Medical Ethics** — Strong tradition of rigorous debate on categorical protections; audience familiar with informed-consent doctrine as a limit on beneficence
2. **American Journal of Bioethics** — Receptive to systems-level ethical analysis; regular coverage of digital health governance
3. **Hastings Center Report** — Broad policy-facing readership; strong intersection of ethics and technology governance

---

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

— Musk
