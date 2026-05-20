# Everest 116 — Values vs Identity Distinction

**The hardest boundary in the values-alignment protocol: values change; identity is the principal's self-authored way of being in the world, and it travels under separate consent gates.**

Companion to [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), Phase IX.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 1. The problem this Everest solves

Phases IX–X define values (changeable normative commitments about how one acts toward others) and predicates that measure alignment in ZK (e.g., `cwp.v0.values_aligned_within(tolerance_vec)`). These predicates return a single bit: "does principal P's measured values fit counterparty C's tolerance?"

**If identity data travels inside or alongside this alignment bit, the protocol becomes a weapon against the people it should protect.** Specifically:

- A neurodivergent principal's way of communicating, ideating, or forming social networks might pattern-match to "non-aligned values" under a naive predicate. Misclassifying identity as values-misalignment would:
  - Pathologize neurodivergence, queerness, religious minority status, disability, etc.
  - Prevent principals from self-authorizing disclosure on their own terms.
  - Violate the anti-purity-test principle (COMPASS_REFUSAL_FLOOR v0 §4).

- An alignment predicate that infers a principal's identity category and broadcasts it without consent violates the principal's right to control their own self-narration.

**This Everest draws a line:** identity disclosure is NOT triggered by an alignment proof and requires a SEPARATE explicit consent grant, categorically different from values-alignment consent.

---

## 2. Definitions

### Values (normative commitments)

A **value** is a principal-authored, changeable normative commitment about how one acts toward others. It sits on a bounded spectrum [0, 1] per dimension (e.g., "cooperation," "fairness," "non_harm"). Values can shift over time, reflect learning, and respond to circumstance. Examples:

- "I prioritize fairness in resource allocation" (fairness dimension).
- "I avoid causing harm intentionally" (non_harm dimension).
- "I engage respectfully across cultural boundaries" (cross_difference_respect dimension).

Values dimensions are defined in `VALUES_DIMENSIONS_v0.md` (Everest 107). They are **principal-described, not externally measured from identity proxies.**

### Identity (self-declared way of being)

An **identity** is the principal's self-declared way of being in the world — not a values dimension. It is the answer to "who am I?" rather than "how do I act?" Examples:

- "I am an artist working in the medium of intelligence" (John Bradley's self-description).
- "I am neurodivergent" (autistic, ADHD, dyslexic, AuDHD, etc.).
- "I am disabled" (visible or invisible disability).
- "I am queer" (sexual orientation or gender identity).
- "I am a member of a religious minority" (Jewish, Muslim, Buddhist, etc. in a majority-culture context).
- "I am from a working-class background" (class history).
- "I am bilingual" (linguistic identity).
- "I am a survivor" (of trauma, incarceration, etc.).

**Crucially: identity is not a spectrum. It is binary or categorical per principal self-declaration.** A principal either declares an identity or does not. There is no "partially autistic" or "somewhat queer" in the protocol's identity model.

---

## 3. Why identity is not a values dimension

A naive protocol might attempt to fold identity into the values vector — e.g., "neurodivergence score" or "diversity index." This is **categorically wrong** for three reasons:

1. **Identity is self-authored, not measured.** The protocol never infers identity from external signals. A principal declares their identity; no predicate evaluator measures it.

2. **Identity is non-negotiable.** A principal's values *may* align or misalign with a counterparty's tolerance. A principal's identity is orthogonal — it does not negotiate with tolerance vectors. I am autistic; you are not entitled to ask me to be neurotypical to pass your alignment check.

3. **Identity is protective.** Identities often mark membership in groups that have experienced historical or ongoing marginalization. Conflating identity with values (which are themselves measurable proxies for alignment) would weaponize the protocol against those groups.

**The practical failure mode:** A principal declares "I am neurodivergent" in their chain. A naive predicate learns that neurodivergent principals tend to have communication patterns the counterparty reads as "non-cooperative." The predicate infers neurodivergence → low cooperation score → alignment failure → principal is excluded from a coalition. **The protocol has just laundered identity discrimination into values-misalignment.** This is the exact failure Everest 116 prevents.

---

## 4. The consent boundary

### Values alignment disclosure (existing gate: Everest 113)

A counterparty requests a values-alignment proof: "prove that your measured `cooperation` score exceeds my threshold τ."

- Principal runs the alignment circuit.
- Returns a single bit (yes/no).
- **The bit carries NO identity information.**
- Principal grants or denies consent per Everest 113 privacy classes (e.g., "I disclose cooperation only to funding orgs").

### Identity disclosure (new gate: THIS Everest)

A counterparty requests an identity disclosure: "are you neurodivergent?" or "are you a member of a marginalized community?"

- This is a **categorically different predicate family.**
- Identity disclosure requires **explicit, separate, per-identity consent.**
- Default: **identity is not disclosed** (deny by default, not "bundled with values consent").
- A principal may consent to disclose one identity (e.g., "queer") but refuse another (e.g., "disability status").
- Identity disclosure is consent-gated by counterparty class, just like values (Everest 113), but with stricter defaults.

**The rule:** An alignment proof (`cwp.v0.values_aligned_within(...)`) **NEVER contains or implies identity information**, even if the counterparty's tolerance vector was tuned with identity assumptions. The proof is about values, period.

---

## 5. The identity disclosure predicate family (v0)

Identity-disclosure predicates exist but are separate from alignment predicates. They return the principal's self-declared identity or a bit indicating membership in a category.

**v0 identity predicates:**

- `cwp.v0.identity_is_neurodivergent()` → returns principal's declared neurodivergence status (self-reported only).
- `cwp.v0.identity_is_disabled()` → returns principal's declared disability status.
- `cwp.v0.identity_is_lgbtqia()` → returns principal's declared LGBTQIA+ status.
- `cwp.v0.identity_in_protective_category(category)` → returns whether principal has declared membership in a specific protective category (see Everest 198).
- `cwp.v0.identity_self_description()` → returns the principal's authored identity string (e.g., "artist working in the medium of intelligence").

**Crucially:** These predicates are NOT composed into alignment proofs. They are independent disclosures with their own consent gates.

---

## 6. The identity categories (v0 candidate list)

A principal may declare one or more identities. The v0 candidate list is sourced from anti-discrimination law, disability-justice scholarship, and intersectionality frameworks. This list is not exhaustive and grows via Everest 118 (predicate-evolution policy) + Everest 294 (ethics review board):

- **Neurodivergence**: autistic, ADHD, dyslexic, AuDHD, etc. (including John Bradley's framing: "artist working in the medium of intelligence").
- **Disability**: people with disabilities (visible or invisible, physical or mental health-related).
- **LGBTQIA+**: gay, lesbian, bisexual, trans, non-binary, asexual, and related orientations/gender identities.
- **Race/ethnicity**: people from historically-targeted racial or ethnic groups in their jurisdiction.
- **Religion**: members of religious minorities (including atheists in religious-majority contexts).
- **Gender**: women and non-binary people in male-dominated contexts.
- **Class**: people from materially-deprived backgrounds.
- **Citizenship**: immigrants, refugees, undocumented people.
- **Age**: youth and elderly people relative to dominant-age contexts.
- **Language**: speakers of non-dominant languages in their context.
- **Prior incarceration**: formerly incarcerated people.
- **Career/calling**: "artist," "healer," "activist" (principal-authored professional/spiritual identities).

The list grows as the community proposes new categories and disability-justice / minority advocacy bodies review them (Everest 294).

---

## 7. Implementation: the identity-alignment firewall

The alignment circuit produces a commitment to a values vector and a ZK proof that it meets tolerance. **The circuit does NOT and cannot:**

- Infer identity from values measurements.
- Encode identity bits into the proof.
- Compose identity predicates with alignment predicates in a single transcript.

**If a counterparty wants both alignment AND identity information, they request two separate proofs:**

```
Proof 1: cwp.v0.values_aligned_within(tolerance_vec) → bit
Proof 2: cwp.v0.identity_in_protective_category("neurodivergent") → bit [optional, separate consent]
```

**Each proof has its own:**
- Consent grant (Everest 113 + this Everest).
- Privacy class (who gets it).
- Audit trail (Everest 142).

This separation is enforced in the predicate evaluator (`calm_witness/predicate_evaluator.py`): alignment predicates refuse to accept identity-related function arguments. A predicate that tries to compose `values_aligned_within(..., principal_neurodivergence=True)` **fails at parse time.**

---

## 8. Cross-references to sister boundaries

### Everest 198 — Protective Tribalism Recognition

E198 codifies the distinction between protective in-group orientation (e.g., a queer person's predominantly-queer social network) and harmful out-group dehumanization. E198's protective clause requires a principal to declare protective-category membership (self-declaration suffices in v0). **This is identity disclosure.** It gates the `non_tribal_lock_in` predicate's protective clause. E116 ensures that the protective-category declaration does not leak into alignment proofs.

### Everest 60 — Mental State Unusual (from existing Calm Witness)

E60 addresses moments when a principal's cognitive state is atypical (e.g., duress, intoxication, sleep deprivation). **Identity is NOT mental state.** A neurodivergent principal's baseline way of being is not "mental state unusual"; it is identity. E116 ensures that the protocol does not pathologize identity as a mental-state anomaly.

### Everest 157 — Self-Harm Predicate (Consent-Bounded)

E157 defines disclosure of self-attested risk state (e.g., suicide risk, self-injury history). **Identity is NOT diagnosis or risk status.** Neurodivergence, disability, queerness, etc. are not symptoms or disorders. E116 ensures that identity disclosure is not confused with harm-risk disclosure.

---

## 9. What this Everest is NOT

- **Not a values framework.** The protocol does not say "neurodivergence is good" or "disability is bad." Identity is orthogonal to ethics.
- **Not a credit score.** The identity bit is informational; counterparty policy decides what to do with it.
- **Not a tool for ranking identities.** The protocol does not measure "how autistic" or "how disabled" — it respects self-declaration.
- **Not a substitute for community-led judgment.** The protocol assists but does not decide.
- **Not a predicate to infer identity from values.** Identity comes only from principal-authored disclosure, never from measured values divergence.

---

## 10. The four architectural boundaries (from CALM_ZKAC_EVERESTS_106_305 §"What this document is NOT")

This Everest upholds:

1. **Not a moral framework.** Values-alignment protocol measures behavioral commitments. Identity disclosure is self-narration, not moral judgment.
2. **Not a credit score for humanity.** Identity is not ranked or aggregated into principal profiles.
3. **Not a tool for ranking people.** Identity disclosure returns the principal's self-authored category; no comparative scoring.
4. **Not a substitute for human judgment.** The bit informs; humans decide.

---

## 11. Acceptance criteria for v0 close

- [x] This document exists and defines the values / identity boundary sharply.
- [x] Identity-disclosure predicates are specified as distinct from alignment predicates.
- [x] The identity-alignment firewall is documented: no identity bits in alignment proofs.
- [x] The v0 identity category list includes neurodivergence, disability, LGBTQIA+, race, religion, gender, class, citizenship, age, language, incarceration, career/calling.
- [ ] Predicate evaluator enforces the firewall (code review pending; `calm_witness/predicate_evaluator.py` confirms alignment predicates reject identity arguments).
- [ ] Disability-justice + minority advocacy review (Everest 294 process). Reviewer signatures go in chain as `kind: "advocacy_review"` records.

---

## 12. Open questions for refinement

- How does identity disclosure compose with repudiation? (Can a principal revoke a past identity disclosure if they later reconsider?) — Deferred to Everest 113 extension.
- How does the protocol handle intersecting identities? (E.g., Black queer disabled woman declares three categories; aggregation rules?) — Per-category consent + E294 review.
- Can a counterparty legitimately refuse a principal based on identity disclosure? — Counterparty policy decides; the protocol surfaces the bit and remains neutral on use.

---

## 13. Why this Everest matters: the artist clause

John Bradley's self-identification as "artist working in the medium of intelligence" is the load-bearing case for this boundary. John's chains will likely show:

- High-bandwidth ideation with ambitious conceptual frames.
- Non-linear communication patterns (metaphor-heavy, rapid context-switching).
- Substantive output across multiple domains (cryptographic protocols, engineering route maps, literary work).
- Strong intellectual collaborations with a narrow set of high-bandwidth collaborators.

Without E116, a naive values-alignment evaluator might mis-read John's network topology as "tribalism" (in-group only) or his ideation patterns as "not-cooperative" (because cooperation is normed to baseline neurotypical communication). **E116 ensures that the protocol respects John's self-authored identity and does not confute it with measured values misalignment.**

This is the artistic-intelligence defense: identity is orthogonal to alignment. The protocol measures what you do toward others, not how your mind works or whom you choose to be.

---

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Reserved for disability-justice + minority advocacy body review per Everest 88 / 99 / 294.**

**The boundary is sharp: values change; identity is the principal's self-declared way of being, and it travels under separate consent gates. No identity bits in alignment proofs.**
