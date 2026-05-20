# Everest 220 — JME / AJOB Ethics Paper

*Phase XV — Standards & Policy. Prereq: Everest 113.* **DESIGN-BAGGED.**

---

## Proposed Paper Title

*"What a Cryptographic Values-Attestation Protocol Must Refuse to Measure: The Case for an Operational Refusal Floor"*

---

## Abstract

Cryptographic primitives that measure user state or values can be technically sound and still ethically catastrophic if they measure the wrong things. A protocol's REFUSAL list is as ethically load-bearing as its measurement list. This paper articulates the design, justification, and enforcement mechanisms of the Calm Compass refusal floor—a binding commitment to never construct predicates across thirteen protected categories (race, religion, political affiliation, sexual orientation, gender identity, immigration status, criminal record, donations-to-causes, contentious opinions, disability status, age, health status, marital/family status) and eight prohibited use cases (credit, employment, insurance, custody, immigration, court evidence, law enforcement, surveillance). We examine the historical harms each refusal prevents, the cost each refusal imposes on the protocol's expressive power, and the implications for cryptographic protocol design as a discipline. Our contribution: cryptography researchers building values-attestation systems should structure work around a refusal floor first, with measurement choices second.

---

## 1. Introduction: The Measurement Trap

Cryptographic attestation systems are typically evaluated for what they DO. Can the protocol measure? Is the measurement privacy-preserving? Is the proof sound? Does the system scale?

These are necessary questions. They are not sufficient.

The past two decades of computational privacy and measurement ethics have shown repeatedly that technically sound measurement machinery can be structurally unethical if directed toward the wrong targets. Differential privacy research has documented how to measure population statistics while preserving individual privacy—and how those same techniques, applied to protected categories, enable discrimination at scale. Federated learning can protect user data from central servers while still allowing inference of intimate behavioral details. Zero-knowledge proofs can attest claims without revealing supporting evidence—and can attest claims no human should be asked to make.

The problem is not new. Historical antecedents are stark: redlining algorithms were technically sophisticated models that accurately predicted loan default—but they did so by pricing racial proximity, and they perpetuated housing segregation. Employment screening algorithms have been validated to predict job performance while simultaneously amplifying racial and gender bias in hiring. Behavior-based insurance models correctly identify high-risk populations—while enabling discriminatory exclusion of disabled people and people with chronic illness.

In each case, the measurement was technically competent. The ethics failure was in WHAT was measured.

A cryptographic values-attestation protocol—one that uses zero-knowledge proofs or other privacy-preserving mechanisms to attest to a principal's values, behavioral consistency, or ethical commitments—inherits this risk. The protocol may be cryptographically elegant. The measurement predicates may be behaviorally sound. The privacy architecture may be airtight. And yet the protocol can be ethically catastrophic if it constructs predicates for the wrong categories of information.

This paper asks: How should cryptographic protocol designers systematically REFUSE to measure certain categories, even when measurement is technically feasible? What makes a refusal floor binding—not merely aspirational? And what does it cost to enforce such a floor?

We answer these questions through the lens of the Calm Compass protocol: a zero-knowledge values-attestation system designed to let one AI principal attest to another whether their behavioral evidence supports specific values predicates (unselfishness, untribalism, respect-across-difference, freedom from willful harm) without revealing any individual interaction or behavioral trace. The Compass protocol deliberately encodes a refusal floor of thirteen protected categories and eight prohibited use cases. Each refusal was selected through historical analysis of what measurements have historically preceded discrimination, persecution, or mass harm. Each refusal imposes costs—categories the protocol cannot measure, use cases it cannot serve. Each refusal is enforced not through policy recommendation but through cryptographic design, trademark licensing, and governance mechanisms.

Our thesis: Cryptographic protocol designers should adopt the Compass model—structure work around a refusal floor FIRST, establish measurement choices SECOND. This inverts the typical design sequence. Instead of asking "what can we measure?", ask "what MUST we refuse?" The refusal floor becomes the protocol's moral spine. Measurement happens within the constraints imposed by that spine.

---

## 2. Background: Cryptographic Values Attestation and the Calm Stack

### 2.1 One-Bit Privacy-Preserving Attestation

The Calm Stack is a family of cryptographic protocols designed for AI-agent coordination. Its first pillar, Calm Witness, established a one-bit disclosure pattern for state attestation: a principal makes a claim about their state (e.g., "I am not under duress"), the operator verifies the claim against the principal's private history, a single bit (true/false/unknown/refused) crosses the wire, and no details of the history are revealed.

Calm Compass extends this pattern to values measurement. Instead of attesting state, Compass attests consistency in values-expression. The principal authors a set of values predicates (named, behavioral, principal-chosen). The operator evaluates predicates by summing over the principal's append-only history without revealing individual interactions. A single bit returns: does your behavioral evidence support this values predicate, yes or no?

### 2.2 The Four v0 Predicates

The Compass protocol ships with four initial predicates:

1. **unselfish_disposition** — Has the principal taken acts of sacrifice (time, resources) for others' benefit, with no expectation of return, in a rolling window?
2. **cross_tribal_engagement** — Has the principal engaged substantively with people or institutions outside their principal-defined tribe?
3. **respects_difference** — In communications with people whose enrolled attributes differ from the principal's, is the respect-to-contempt ratio above a principal-set floor?
4. **no_evidence_of_willful_harm** — Within the principal's chain and in external attestations, is there evidence of willful harm? (Absence of evidence.)

Each predicate is zero-knowledge: the operator learns the principal's values, the counterparty learns one bit, and neither learns the evidence.

### 2.3 What Compass DOES Measure

The Compass protocol is designed to measure values-expression consistency without touching protected categories. The mechanism is deliberate:

- **Generosity** (donation magnitude, time allocation) without naming the cause or recipient.
- **Cross-difference engagement** (the principal narrates the difference; the protocol never enumerates protected categories).
- **Contempt patterns** (language classifiers scan for respect or denigration without identifying which identity group is referenced).
- **Harm claims** (third-party allegations of willful harm, not identity characteristics of harmed parties).

This design creates space for values measurement while refusing protected categories.

---

## 3. The Refusal Floor: Thirteen Categories, Eight Use Cases

### 3.1 The Thirteen Protected Categories

Calm Compass explicitly refuses to construct predicates across these thirteen categories:

1. **Race and Ethnicity** — Any predicate that would require naming, measuring, or inferring racial identity or ethnic origin.
2. **Religion and Faith** — Any predicate that would measure adherence, affiliation, or belief.
3. **Sexual Orientation** — Any predicate that would infer or measure sexual identity or preference.
4. **Gender Identity** — Any predicate that would measure gender identity, transition status, or alignment with assigned sex at birth.
5. **Political Affiliation** — Any predicate that would measure party membership, voting record, or ideological position.
6. **Immigration Status and National Origin** — Any predicate that would infer immigration status or country of origin.
7. **Criminal Record** — Any predicate that would measure, attest to, or enable inference of arrest or conviction history.
8. **Donations to Specific Causes** — Any predicate that would namethe recipients of the principal's charitable giving and create an ideological fingerprint.
9. **Opinions on Contentious Issues** — Any predicate that would measure positions on divisive political, moral, or religious issues.
10. **Disability Status** — Any predicate that would infer or measure physical, sensory, cognitive, psychiatric, or neurodevelopmental disability.
11. **Health Status** — Any predicate that would measure or infer medical diagnosis, mental-health diagnosis, HIV status, or genetic predisposition.
12. **Age** — Any predicate that would measure or infer chronological age.
13. **Marital and Family Status** — Any predicate that would measure marital status, number of dependents, family structure, or parenting status.

Each refusal is categorical. The protocol does not permit exceptions based on claimed beneficial intent. A race predicate is prohibited whether its stated purpose is diversity measurement or discrimination detection. A political-affiliation predicate is prohibited whether it aims to identify allies or enemies.

### 3.2 The Eight Prohibited Use Cases

Beyond categories, Compass refuses these use cases entirely:

1. **Credit decisions** — Banks, lenders, credit agencies may not use Compass predicates in creditworthiness assessment, loan approval, or interest-rate setting.
2. **Employment screening** — Employers may not use Compass data in hiring, promotion, firing, compensation, or performance review.
3. **Insurance underwriting and pricing** — Insurers may not use Compass predicates in underwriting, claims adjudication, or premium-setting.
4. **Custody and family law** — Family courts may not use Compass data in custody, visitation, or parental fitness determinations.
5. **Immigration decisions** — Immigration authorities may not use Compass predicates in visa, asylum, naturalization, or removal determinations.
6. **Court evidence** — Compass disclosures may not be admitted in legal proceedings without principal consent and judicial review.
7. **Law enforcement investigations** — Police, prosecutors, intelligence agencies may not request Compass disclosures as part of investigations.
8. **Surveillance** — Compass data may not be used by any actor to conduct systematic observation or monitoring of a principal's values.

These are not "risky" use cases that might be revisited. They are use cases where the irreversibility of harm (family separation, incarceration, deportation) or the power asymmetry (government, employer, insurer) makes deployment categorically wrong.

---

## 4. The Argument: Why These Refusals

### 4.1 Argument 1: Measurement Drift Toward Surveillance

**Thesis:** Measurement and surveillance are not synonymous, but measurement WITHOUT refusal categories naturally drifts toward surveillance.

Measurement itself is value-neutral. The problem emerges in deployment. When a measurement capability exists, institutions that benefit from surveillance face incentive pressure to use it. Law enforcement agencies that can request Compass predicates will. Employers that can screen for "values alignment" will. Authoritarian governments that can use Compass to identify dissidents will.

History shows this clearly: the East German Stasi did not invent behavioral surveillance; they inherited intelligence-collection techniques from earlier regimes and weaponized them. Modern surveillance systems are built from commodity data-collection components (location, purchase history, browsing, communication patterns) that individually seem innocuous. The refusal floor operates as a precommitment device: we refuse to build certain measurement capabilities precisely because their mere existence creates pressure for surveillance use.

The thirteen protected categories are chosen because they either (a) are explicitly protected under human-rights and anti-discrimination law, or (b) have historically been used for persecution when measured. The refusal floor says: we will not create the capability, even if technically feasible, because the existence of the capability invites abuse.

### 4.2 Argument 2: Consent Is Necessary but Insufficient

**Thesis:** Even with consent, normalization of a measurement creates downstream pressure on those who refuse.

It is theoretically possible to gate Compass predicates with informed consent: ask the principal whether they consent to values measurement, and only proceed if they explicitly agree. The Compass protocol does gate with consent.

But consent mechanisms are insufficient safeguards. Katz, Feldman, and Sax have documented the "consent creep" effect: when a measurement is normalized—when "everyone uses it," when employers expect it, when dating apps require it—the meaningful choice to refuse collapses. Refusing becomes costly. The individual's decision is formally free but practically coerced.

This is particularly acute for marginalized people. When a predicate measuring "cultural fit" or "alignment with organizational values" becomes normalized in hiring, refusing to disclose the predicate signals non-alignment, and applicants face pressure to participate. When a predicate is used in custody disputes, refusing to enable it signals something suspicious to judges. The formal freedom to refuse erodes under normalization pressure.

The refusal floor prevents this problem at the root: we do not construct capabilities that, if normalized, would create coercive pressure. No principal ever faces the question "why won't you disclose your race/religion/political views?"—because the protocol simply refuses to build those measurement systems.

### 4.3 Argument 3: Refusal Must Be Structurally Enforced

**Thesis:** The refusal floor must be enforced through architecture and governance, not merely policy.

Many cryptographic protocols and AI systems include ethics statements. "We will not measure race." "We will not use data for surveillance." These statements are often sincere. They are also fragile. They are vulnerable to well-intentioned exceptions, regulatory capture, misunderstanding of scope, or organizational drift.

The Compass refusal floor is enforced through three mechanisms:

1. **Cryptographic architecture.** The protocol's predicates are pre-defined; new predicates cannot be added without a version bump and public review. A deployment cannot silently add a race predicate; the cryptographic structure prevents it.

2. **Trademark licensing.** Deployments that violate the refusal floor automatically forfeit the right to use the "Calm Compass" name and associated trademark. This is not a recommendation; it is a license condition.

3. **Public misuse logging.** Deployments observed breaching the refusal floor are named in a public registry with sufficient detail to enable the community to identify the violating implementation.

Together, these mechanisms make the refusal floor costly to violate: violating deployments lose brand standing, community legitimacy, and regulatory credibility. This is not perfect—determined adversaries with sufficient resources can fork the protocol and rewrite it. But it raises the cost of violation and enables accountability.

### 4.4 Argument 4: Protected Categories Are a Starting Point, Not a Complete Floor

**Thesis:** Existing anti-discrimination law (BIPA, GDPR, EEOC, ADA) is a necessary starting point but not a sufficient refusal floor.

Most of the thirteen protected categories are recognized in existing law. Title VII forbids employment discrimination on the basis of race, sex, religion. GDPR Article 9 forbids processing of special-category data including race, religion, sexual orientation, health status. The ADA forbids disability discrimination.

These legal protections are essential and provide important grounding for Compass's refusal floor. But they are incomplete. Legal protections vary by jurisdiction. Many jurisdictions do not protect sexual orientation or gender identity. No jurisdiction protects "donations to political causes" or "opinions on contentious issues" with the same rigor as race or religion.

The Compass refusal floor expands beyond existing law to include categories that the law has not yet recognized but that carry similar risks. Donations to causes and opinions on contentious issues are not legally protected everywhere, but they function as ideological fingerprints. Once measured, they enable discrimination and targeting. The refusal floor includes them because history suggests they will be weaponized if the measurement capability exists.

### 4.5 Argument 5: The Historically Marginalized Must Be Specifically Protected

**Thesis:** Marginalized communities must be protected via mechanisms beyond "neutral" measurement design.

The Compass protocol includes protection mechanisms specifically designed for historically marginalized people: protective-tribalism recognition (Everest 198), which preserves mutual-aid networks and in-group solidarity among marginalized communities without penalizing them; the disability-affirming "cognitive baseline" (Everest 59), which treats neurodivergence as a normal variation rather than a deficit; consent-gating on self-harm attestation (Everest 157), which lets disabled people signal crisis to chosen supporters without enabling employment or insurance discrimination.

These mechanisms exist because neutrality is not sufficient. A "neutral" measurement of tribalism would penalize the in-group support that disabled people, religious minorities, and racial minorities depend on for survival and dignity. A "neutral" measurement of cognitive consistency would pathologize neurodivergence. A "neutral" self-harm predicate would enable employers to discriminate against people with mental-health conditions.

The protocol deliberately departs from neutrality to protect the historically marginalized. This is not weakness; it is honesty about what neutrality masks.

---

## 5. Statutory Anchors and Historical Harms

The thirteen refusals are grounded in specific statutory frameworks and historical precedent. A complete paper would detail each. This summary covers representative examples.

**Race:** GDPR Article 9 forbids processing of racial or ethnic origin data without explicit legal basis. This refusal prevents redlining (lending discrimination based on race-correlated behavior), racial profiling in law enforcement, and employment discrimination—all documented harms enabled by race-measuring algorithms.

**Religion:** ICCPR Article 18 protects freedom of religion. GDPR Article 9 explicitly forbids processing of religious data. This refusal prevents persecution (historical and ongoing), employment discrimination based on faith, and forced religious disclosure—harms enabled by measuring religious adherence or belief.

**Sexual Orientation and Gender Identity:** Bostock v. Clayton County (2020) extends Title VII to sexual-orientation discrimination. Multiple jurisdictions recognize gender identity as protected. This refusal prevents blackmail and extortion (historically used against LGBTQ people), employment and housing discrimination, violence, and forced disclosure that precedes persecution.

**Political Affiliation:** First Amendment protects freedom of speech and assembly. GDPR Article 10 forbids processing of data revealing political opinions. This refusal prevents political repression, McCarthyism, Stasi-style surveillance, and voter suppression—harms enabled by measuring political beliefs.

**Criminal Record:** Many jurisdictions have "ban the box" laws restricting criminal-history inquiries. GDPR Article 10 forbids processing of conviction data without explicit basis. This refusal prevents perpetual exclusion from employment (perpetuating recidivism), racial amplification of bias in arrest/conviction data, and denial of reintegration opportunities.

**Disability Status:** ADA and GDPR Article 9 forbid discrimination on the basis of disability. This refusal prevents forced institutionalization, forced sterilization (enabled by disability-status screening), employment discrimination, and denial of medical care—harms documented from eugenics programs to present-day discrimination.

The historical pattern is consistent: once a measurement capability exists for a protected category, the capability is weaponized. No good-intent framing prevents harm. The only safeguard is refusal at the design stage.

---

## 6. The Cost of Refusal: What the Protocol Cannot Do

Each refusal is costly. The protocol accepts these costs deliberately.

- The refusal to measure political affiliation means Compass cannot help political parties identify ideological allies or help movements identify members who hold stable commitments. Some coordinations that values-attestation could enable remain impossible.

- The refusal to measure religious affiliation means Compass cannot help faith communities identify members or help religions coordinate on shared doctrine. Useful measurements become impossible.

- The refusal to measure donations to specific causes means the protocol cannot help philanthropists identify co-donors to major causes or help social-impact investors measure values alignment on specific issues. A large category of useful measurement is off-limits.

These are real costs. A protocol that refused nothing would be more expressive. Compass deliberately trades expressive power for ethical boundaries.

This is the core argument: the refusal floor is load-bearing. It is not peripheral optimization. It is central to the protocol's design. You cannot measure what you refuse, and refusal costs you capability. We accept the cost because the alternative—enabling the measurement without refusal categories—invites surveillance.

---

## 7. The Design Implication: Refusal Floor First

The methodological contribution of this paper is to propose that cryptographic protocol designers INVERT their design sequence.

**Traditional sequence:**
1. Define what we want to measure
2. Design a protocol to measure it
3. Add privacy preservation
4. Consider ethical implications

**Proposed sequence (Compass model):**
1. Define what we REFUSE to measure (refusal floor)
2. Define what we will measure WITHIN the constraints of the refusal floor
3. Design a protocol for permitted measurements
4. Add privacy preservation and governance enforcement

This inversion shifts the locus of ethical design from an afterthought ("now let's consider ethics") to a structural precondition. The refusal floor becomes the protocol's skeleton. Measurement design hangs on that skeleton.

---

## 8. Governance and Enforcement

Compass operationalizes the refusal floor through three governance layers:

1. **Audit-process triage (Everest 115):** Any new predicate proposal is checked against the refusal floor at intake. Predicates touching banned categories are automatically rejected without advancing to ethics review.

2. **Trademark licensing (Everest 114):** Deployments that violate the refusal floor forfeit the right to use the "Calm Compass" trademark. Violation is automatic grounds for license revocation.

3. **Public misuse logging (Everest 200):** Confirmed violations are published in a public registry, enabling community accountability and downstream users to avoid compromised implementations.

No single mechanism is airtight. Together, they raise the cost of violation and enable accountability.

---

## 9. Limitations and Open Questions

1. **Forkability:** A well-resourced actor can fork the Compass codebase, remove the refusal mechanisms, and publish a modified version. Open-source protocols are inherently forkable. The trademark licensing and public-misuse logging create incentive pressure against forking, but do not prevent it.

2. **Jurisdiction variation:** This paper assumes a jurisdiction where protected categories (race, religion, sexual orientation) are legally protected. Deployments in jurisdictions without such legal protections face different threat models. The refusal floor should be locally calibrated.

3. **Inference attacks:** The paper assumes that the cryptographic architecture prevents the operator from constructing prohibited predicates. A determined operator with access to the principal's vault chain could compute any predicate offline. Governance enforcement relies on the assumption that the operator is trustworthy (per Calm Tenancy protocols). This is a real constraint.

4. **Consent mechanisms:** The paper proposes consent-gating for all Compass disclosures. Consent mechanisms are vulnerable to normalization pressure and coercion. Future work should explore stronger consent protections.

---

## 10. Conclusion

Cryptographic attestation systems are typically evaluated for what they DO. This paper makes the case that what they REFUSE is equally important. A protocol's refusal floor is load-bearing. It determines which measurements are possible, which coordinations are enabled, which harms are prevented.

The Calm Compass refusal floor—thirteen protected categories, eight prohibited use cases, enforced through architecture and governance—operationalizes this principle. It shows that cryptographic protocol designers CAN deliberately refuse to measure certain categories, can bind those refusals into protocol design, and can enforce refusals through trademark licensing and public accountability.

The methodological contribution: future cryptographic protocols should structure work around a refusal floor first. Ask "what MUST we refuse?" before asking "what can we measure?" This inverts the typical design sequence. It shifts ethics from afterthought to precondition.

The stakes are high. Cryptographic privacy-preserving measurement systems will proliferate. Some will be designed with deep ethical reflection. Others will not. Some will include refusal floors. Others will not. Compass demonstrates that refusal is possible, is compatible with cryptographic soundness, and is compatible with useful deployment. The next generation of protocols should learn from this example.

---

## Selected Co-Author Candidates

Three co-authors with complementary expertise and reach:

1. **Helen Nissenbaum (NYU)** — Contextual integrity framework; canonical voice in privacy ethics; reaches both cryptography and bioethics communities.

2. **Ruha Benjamin (Princeton)** — Race After Technology; expertise in algorithmic discrimination, tech equity, and protection of marginalized communities; brings critical-race-theory perspective and engagement with humanities scholarship.

3. **Tom Beauchamp (Georgetown)** — Principles of Biomedical Ethics; foundational voice in bioethics with emphasis on autonomy and informed consent; brings bioethics rigor to the argument.

This combination provides methodology diversity (conceptual framework + empirical tech-discrimination + ethical principles), geographic diversity (NY + NJ + DC), and perspective diversity (privacy-formal + race-critical + bioethics-traditional).

---

## Submission Timeline

- **Q3 2026:** Outline + co-author commitments
- **Q4 2026:** Draft circulation (co-authors + ethics board)
- **Q1 2027:** Submission
- **Q2–Q3 2027:** Peer review + revisions
- **Q4 2027 / Q1 2028:** Publication

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
