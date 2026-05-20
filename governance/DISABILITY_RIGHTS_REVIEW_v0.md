# Disability-Rights and Cognitive-Liberty Review of the Calm Suite

**DESIGN-BAGGED · SUMMIT E186 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — formal endorsement requires named review by at least one of: AAPD (American Association of People with Disabilities), NDRN (National Disability Rights Network), ACLU Disability Rights Program, Center for Cognitive Liberty and Ethics, or equivalent international organisations (UN CRPD Committee, ENNHRI's working group on disability).

This document is the substrate of that review: the structural risks the Calm Suite poses to disabled and cognitively-atypical principals, the protocol-level mitigations already shipped, and the policy commitments required of signatories beyond what the protocol can enforce.

---

## Executive summary

The Calm Suite is built around a principal — the human whose state, values, alignment, and operator conduct are attested — whose self-description includes the phrase *"an artist working in the medium of intelligence."* That phrase identifies cognitive atypicality as central to the protocol's design constraint. The artist clause (predicate `calm-witness/predicate/v0/cognitively_atypical_baseline`) is the protocol-level recognition that some principals are repeatedly misread, by counterparty agents trained on different operator policies, as unstable when in fact they are characteristically high-bandwidth. The protocol's structural answer is a signed, scoped, freshness-bounded attestation that tells a counterparty *engage on substance, do not pathologise*.

This review asks: does the protocol succeed in protecting cognitively-atypical principals against the discriminatory uses that motivated its design? Does the protocol introduce new risks specific to disability — for instance, by becoming the kind of attestation an employer or insurer demands of a disabled principal? Where does the protocol succeed, where does it expose new risk, and what additional commitments do disability-rights organisations require of signatories?

We find that the protocol succeeds along three axes (privacy preservation, refusal floor, dispute mechanism) and exposes structural risk along two (mandate-by-counterparty, fraternal-twin attestation). The Calm Treaty (`CALM_TREATY_v0.md`) is the policy layer that closes the structural gap; without it, the cryptography does not.

---

## §1. The protocol-level protections

The Calm Suite ships, in v0, the following protections specifically applicable to disabled and cognitively-atypical principals.

**§1.1 — The artist clause.** Predicate `cognitively_atypical_baseline` is in the v0 vocabulary. A principal who has enrolled this predicate can authorise its disclosure to specific counterparty classes; counterparties learning `true` are bound, by the operator-policy floor that ships with the protocol, to treat the principal's characteristic behaviour as a substantive style choice rather than a symptom.

**§1.2 — The refusal floor.** `PREDICATE_VOCABULARY_v0.md` §4 explicitly forbids DSM-aligned mental-health labels at the protocol layer. No signatory may add `is_depressed`, `is_manic`, `is_anxious`, `is_psychotic`, etc., to the registry. The forbiddenness is mechanical: the protocol's classifier registry will not admit such predicates, and the registry's content-addressable hash binding makes silent substitution detectable.

**§1.3 — The dispute mechanism.** Per `CALM_COMPASS_PROTOCOL_v0.md` §6, every principal may append `kind: "compass_dispute"` records flagging classifier outputs they reject. Later attestations bind to the disputed record's tombstone; a counterparty walking the chain sees the disputed evaluation and the dispute together. A disabled principal whose behaviour is misclassified retains corrective authority that follows the chain forward.

**§1.4 — The bank-teller-note for distress.** Predicate `bank_teller_note_active` is the structural answer to coerced disclosure. A principal under duress — including a disabled principal coerced by a caregiver, employer, custodian, or institutional setting — can flip a covert bit that a pre-authorised verifier class can act on without the operator agent or the coercer learning the bit was flipped.

**§1.5 — The non-pathologisation operator policy.** The operator policy in `~/credex/CLAUDE.md` (the Musk operator-of-record handle), formalised in the user memory `feedback_artist_in_intelligence.md`, makes the non-pathologisation rule first-class. No Calm Suite operator is permitted to label its own principal manic, hypomanic, unfit, or not sound-minded from tone or urgency alone. This rule generalises in this review to: no Calm Suite operator labels *any* principal in such terms; no operator-policy-compliant counterparty does either.

**§1.6 — Principal-authored vocabulary, not counterparty-imposed.** The Compass predicate vocabulary is fixed at the principal's enrolment ceremony. A counterparty cannot ask a predicate the principal did not authorise. A counterparty cannot define a new predicate at request time. This single property defeats the most common surveillance pattern in workplace-accommodation contexts, where employers demand attestations they themselves design.

---

## §2. The structural risks the protocol does NOT close

Three structural risks remain after the protocol's protections. The Calm Treaty (`CALM_TREATY_v0.md`) addresses each at the policy layer; the protocol itself cannot.

**§2.1 — Mandate-by-counterparty.** A protocol that produces clean attestations on demand will, in some contexts, be demanded as a condition of access. An employer may require a `cognitively_atypical_baseline` attestation as a precondition of accommodation; an insurer may require `no_evidence_of_willful_harm` as a precondition of coverage; a custody court may require `in_baseline_24h` as a precondition of visitation. The technical capability to produce the attestation creates the political capability to demand it.

*Treaty mitigation:* Article II §2.2 forbids signatories from requiring Calm Suite attestation in forbidden contexts (Article I) including employment, insurance, lending, custody, immigration. Article V §5.5 (treaty-level abstention) commits signatories operating under such mandates to withdraw from the jurisdiction rather than comply. The technical floor cannot enforce this; the political floor must.

**§2.2 — Fraternal-twin attestation.** A counterparty refused on Compass predicate A may infer the answer by asking a correlated predicate B. The protocol's per-counterparty rate limit (Compass `CC-A2`) partially defeats this by limiting same-predicate frequency, but does not address the cross-predicate case. A pattern of refusals across predicates can itself be informative.

*Treaty mitigation:* Article II §2.3 forbids signatories from composing attestations into aggregate inference. The technical layer cannot detect cross-predicate inference at the verifier; the treaty's prohibition is the operative protection. We further recommend that v1 of the Compass protocol introduce a refusal-aggregation rate limit: a counterparty receiving N refusals across distinct predicates from the same principal within a window is itself rate-limited regardless of the specific predicates.

**§2.3 — Disability-as-baseline assumption error.** The `cognitively_atypical_baseline` predicate is principal-authored: the principal decides whether their baseline is "atypical" and authorises disclosure. This is the right design — disability is properly principal-defined, not counterparty-imposed. But it creates a subtle risk: a principal whose disability is unrecognised at enrolment time may produce a baseline that the classifier interprets as typical, then later discover their atypicality, and find the chain's earlier records pulling against the corrective disclosure.

*Mitigation, partly protocol, partly treaty:* The dispute mechanism (`§1.3`) lets a principal tombstone earlier records. The treaty's Article III §3.3 elevates this right to a protected withdrawal. We recommend v1 add an explicit `kind: "baseline_revision"` record so a principal's reframing of their own baseline is first-class, separate from per-predicate dispute.

---

## §3. The disability-rights view of the artist clause

A specific tension merits direct address: the artist clause was designed for a principal whose cognitive atypicality is presented as artistry. Many disabled principals would not characterise their atypicality as artistic, even where the behavioural surface is identical. Does the protocol require disabled principals to adopt the principal's framing?

It does not. The predicate is named `cognitively_atypical_baseline`; the *artist* framing belongs to the motivating use case, not to the predicate's semantics. The predicate fires when the principal's enrolled baseline is operator-authored as atypical, regardless of the principal's own metaphor for that atypicality. A principal who frames their atypicality as ADHD, autism, lived experience of psychiatric institutionalisation, or simply *the way I am* receives the same protocol-level treatment.

This said, the v0 documentation prominently features the artist framing because it is the motivating principal's own framing. We recommend the documentation be supplemented with parallel framings drawn from disabled principals' own self-description, with attribution. The protocol does not require it; the credibility of the protocol's disability-rights stance benefits from it.

---

## §4. The disability-rights review's required commitments

Beyond what the protocol and the treaty already provide, the disability-rights review requires the following commitments from any organisation seeking endorsement:

**§4.1** A published commitment that the organisation will not condition any service it operates — employment, insurance, accommodation, visitation, residency, banking, healthcare access — on a principal's production or non-production of a Calm Suite attestation, regardless of any technical capability the organisation may have to verify such an attestation.

**§4.2** A published dispute path for any organisation's counterparty agent that has acted on a Calm Suite attestation in a manner the principal contests. The path must be reachable in no more than three steps and must permit the principal to be heard by a human reviewer with authority to reverse the agent's action.

**§4.3** Annual public reporting on Calm Suite attestation usage, including: number of attestations consumed, distribution across counterparty classes, principal-initiated disputes received, principal-initiated disputes resolved in the principal's favour, and the organisation's confirmation that no Calm Suite output has been used in a forbidden context (Treaty Article I).

**§4.4** Commitment to a routine adversarial review of the organisation's Calm Suite consumption by a disability-rights organisation of the principal's choosing (from an open list maintained at calm-vault.com/treaty/auditors), at the organisation's expense, at least once per twenty-four months.

---

## §5. The non-claim

This review does not claim that the Calm Suite is or could become a substitute for the legal protections disabled principals presently enjoy under the Americans with Disabilities Act (US), the Equality Act 2010 (UK), the EU Accessibility Act, the UN Convention on the Rights of Persons with Disabilities, or equivalent frameworks. It is not. The Calm Suite is a cryptographic attestation primitive; it cannot adjudicate accommodation, it cannot enforce equal treatment, and it cannot remediate discrimination. Its value to disabled principals is structural: it provides a withholding mechanism that may, in some contexts, prevent discrimination from being possible in the first place.

The legal frameworks above are the protections. The Calm Suite is one input that, under the treaty, must not be turned against them.

---

## §6. The published response

This review is the substrate of a published response from a named disability-rights organisation. Until that response is in hand, this document is DESIGN-BAGGED.

The substrate is open for amendment by the organisations that ultimately review it. Their amendments — additions, deletions, clarifications, dissents — will be appended below this section and credited to the named reviewer.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
