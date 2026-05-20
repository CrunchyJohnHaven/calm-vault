# Calm Stack — University Curriculum Specification

**DESIGN-BAGGED · SUMMIT E292 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — adoption by ≥ 3 universities across three disciplines (computer science + law + disability studies) requires named faculty sponsorship at each.

The Calm Stack as a teaching object sits at the intersection of three undergraduate-or-graduate disciplines: applied cryptography (CS), privacy and information law (law), and disability and cognitive-liberty studies (disability studies / interdisciplinary). The protocols can be taught to students of any one discipline alone, but the deepest understanding emerges when all three are taught together. This summit specifies the curriculum across all three.

---

## §1. Why a curriculum

The Calm Suite is, by 2026 standards, an unusual artifact in three ways. First, it composes well-trodden cryptographic primitives in a new way for human-protective signalling. Second, it deliberately encodes a refusal floor at the protocol layer — a policy commitment expressed as code. Third, it is principal-authored at the vocabulary level — the cryptography itself does not foreclose the values discussion.

Students who understand the protocol but not the policy floor will build the cryptography without its protections. Students who understand the policy floor but not the protocol will demand protections the cryptography cannot deliver. Students who understand both can compose new primitives with the same protective discipline. The curriculum's purpose is the third outcome.

## §2. The CS module (12 weeks, undergraduate or early-graduate)

**Prereq:** undergraduate cryptography (Pedersen commitments, Σ-protocols, Bulletproofs concepts familiar at one course's depth); undergraduate distributed systems (Merkle trees, append-only logs).

**Week-by-week:**

```
W1   The agent-to-agent trust problem. Read: ZKBB_USER_PROTOCOL_v0 §§1-3.
W2   Pedersen commitments + Σ-protocols (refresher). Lab: implement commit/open.
W3   The bank-teller-note primitive. Read: everest_78_stealth_disclosure.md.
W4   Hash-chain integrity + Sigsum. Lab: extend verify_chain.py with new kind.
W5   Predicate vocabulary design. Read: PREDICATE_VOCABULARY_v0 §§1-4.
       Lab: propose a new predicate; trace forbidden-floor review.
W6   Bulletproofs range proofs. Lab: pure-Python Pedersen + range-proof toy.
W7   The Compass aggregator. Read: CALM_COMPASS_PROTOCOL_v0 §4.
W8   ZKML circuits in Halo2 (introduction only; depth optional).
W9   Composition: the four-pillar handshake. Lab: extend calm_stack/session.py.
W10  Adversarial review. Lab: write a new attack against a teammate's predicate.
W11  Conformance + cross-language ports. Lab: produce a Rust-bindings stub.
W12  Final project review. Each team has built either a new predicate, a
     classifier, a verifier, or an adversarial-review module.
```

**Grading:** 40% final project, 30% labs (10 of them), 20% adversarial review (W10), 10% protocol-design exercise (W5).

**Materials, all open-source:** the public github.com/CrunchyJohnHaven/calm-vault repository serves as the textbook. Lectures are slide-decks the Foundation publishes; lab assignments are forks of the reference implementation.

## §3. The law module (10 weeks, graduate)

**Prereq:** privacy law survey (GDPR / CCPA / BIPA basics familiar); some exposure to evidence law and constitutional principles.

**Week-by-week:**

```
W1   Privacy regimes survey. Read: governance/CROSS_JURISDICTION_COMPLIANCE_v0.md.
W2   The forbidden-context list. Read: CALM_WITNESS_SCOPE_STATEMENT.md.
W3   Principal-authorship as legal frame. Read: CALM_COMPASS_PROTOCOL_v0 §5.
W4   The refusal floor as one-way ratchet. Read: CALM_TREATY_v0 Article IV.
W5   Compelled disclosure and the bank-teller-note primitive.
W6   Cross-jurisdiction conflicts of law (the protocol's compliance ratchet).
W7   Evidence and admissibility. Discussion: when would a Calm Suite
       attestation be admissible? When would it be excluded?
W8   The Treaty as governance instrument. Read: CALM_TREATY_v0.
W9   The Foundation as 501(c)(3). Read: CALM_FOUNDATION_INCORPORATION_v0.md.
W10  Final paper: pick a hypothetical case where Calm Suite attestation is
     proposed in a litigation context; argue for or against admission under
     a chosen jurisdiction's rules.
```

**Materials:** governance docs + treaty + compliance mapping, plus a casebook of hypothetical fact patterns the Foundation maintains.

## §4. The disability studies module (8 weeks, undergraduate or graduate)

**Prereq:** introductory disability studies (social model of disability familiar) or cognitive-liberty (Bublitz, Boire familiar). Not all students arrive with this; the module's W1 includes a primer.

**Week-by-week:**

```
W1   The motivating case: the artist clause. Read: ZKBB_USER_PROTOCOL_v0 §1.
W2   Disability-rights review of the protocol. Read: DISABILITY_RIGHTS_REVIEW_v0.md.
W3   Cognitive-liberty review of the protocol. Read: COGNITIVE_LIBERTY_REVIEW_v0.md.
W4   Principal-authored vocabulary as resistance to imposed labels.
W5   The non-pathologisation operator policy (CredexAI/CLAUDE.md).
W6   Required commitments from endorsing organisations (review docs §4).
W7   Critical examination: where could the protocol still fail disabled
     principals? Where does its protection rely on the treaty and not
     the cryptography?
W8   Final project: propose an amendment to either review document, with
     supporting reasoning. The best amendments are merged into v1.
```

**Materials:** the two review documents (E186, E187), plus interview excerpts the Foundation publishes from disabled principals who have engaged with the protocol (with consent and attribution, contingent on first convening producing them).

## §5. The interdisciplinary capstone (8 weeks, cross-listed)

For students who have completed at least two of the three modules, an 8-week capstone with teams of three (one per discipline). The capstone produces a research artifact: a new predicate, a new classifier, a new policy commitment, or a critical paper. The artifact is reviewed by the Foundation; the best are merged into v1 of the protocol with student authorship credit.

**Capstone outputs (target distribution across 30+ student years):**

- 1–2 new principal-protective predicates added to v1
- 1–2 new operator-conduct duties added to the Tenancy floor
- 1–2 new refusal-floor categories proposed for treaty review
- 1 academic paper submission per year to a CHI / FAccT / USENIX adjacent venue
- 1 model litigation brief per year contributed to the Foundation's casebook

## §6. Three universities, three disciplines

The Foundation seeks adoption at a minimum of three universities, with each university hosting at least one of the three single-discipline modules and at least one hosting the interdisciplinary capstone. Adoption criteria:

**§6.1** A named faculty sponsor at the university whose research portfolio aligns with the discipline (e.g., a privacy cryptographer for the CS module; a privacy or evidence scholar for the law module; a disability-studies scholar for the disability module).

**§6.2** A commitment to teach the module at least twice (two academic years), preserving the syllabus's open-source character and the case-study content.

**§6.3** A commitment that student projects produced in the module are licensed under terms compatible with the Foundation's CC-BY-SA framework, so that the best work can be merged into v1.

**§6.4** Annual review by the Foundation's standards working group of the module's evolution: amendments, deletions, additions are public; faculty and Foundation deliberate jointly.

## §7. Cost and scale

The Foundation does not charge universities for the curriculum. The materials are open-source; the faculty teach for their existing institution's salary; the Foundation's contribution is the curriculum, the case studies, the reference implementations, and access to the Foundation's standards-working-group meetings as observer-status.

At three universities × three disciplines × ~30 students per discipline per year × 5 years = approximately 450 students over the first five years. The Foundation's marginal cost per student is approximately zero; the marginal benefit is the protocol's protective floor distributing into the next generation of practitioners.

## §8. Why this matters for the EVEREST 300

This summit (E292) is one of the founder-outliving mechanisms. The Calm Suite cannot outlive its founder if knowledge of the protocol's *protective intent* dies with the founder. The curriculum is the structural answer: students who understand the protocol's policy floor as well as its cryptography become its custodians independent of any specific operator-of-record.

The summit completes when three universities have published syllabi, have run the courses at least once, and the Foundation can demonstrate students producing capstone work that meets the standards-working-group's review.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
