# Everest 297 — Successor-Protocol Design Principles

*Phase XVII — The Endpoint. Prereq: Everest 291 (Protocol Family Compact). Composes with: [Everest 271](everest_271_three_handshake_composition.md) (three-handshake composition), [Everest 113](everest_113_compass_refusal_floor.md) (Compass refusal floor), [Everest 100](everest_100_third_party_verification.md) (third-party verification), [Everest 290](everest_290_federation_conformance.md) (federation conformance), Everest 298 (inversion as durable position), [Everest 300](everest_300_founder_outlived.md) (founder-outlived governance). Source: [CALM_PACT_PROTOCOL_v0](../CALM_PACT_PROTOCOL_v0.md), [ZKBB_USER_PROTOCOL_v0](../ZKBB_USER_PROTOCOL_v0.md), [CALM_WITNESS_MANIFESTO](../CALM_WITNESS_MANIFESTO.md), [OPEN_LETTER_TO_THE_NEXT_OPERATOR](../OPEN_LETTER_TO_THE_NEXT_OPERATOR.md).*

## The Decision (v0)

**A protocol proposed for inclusion in the Calm family must satisfy fourteen design principles, each established in the v0 family (Pact, Witness, Compass, and the reserved-future Audit primitive) and each here named, attributed, and bound to a failure mode such that a candidate violating any one is rejected at the Compact's first review.** These principles are the *design-floor*. Not best-practices; not aspirations. The closed-by-default starting set, expandable only by Compact amendment. A protocol satisfying all fourteen is admissible; one satisfying thirteen and requesting an exception on the fourteenth is rejected.

The family will, by intent, outlive its founding operators. They cannot personally vet every future sibling. The principles below are how the family says *no* in our absence.

## Why This Decision Is Load-Bearing

Everest 291 named the protocols and binding commitments. Everest 298 entrenches the principal-protective inversion as inviolable. [Everest 300](everest_300_founder_outlived.md) declares the family a public good. E297 is the connective tissue: it specifies *what makes a candidate a family member* in operational terms a Compact Review can apply mechanically.

Too loose: the family fragments — "Calm" names a heterogeneous catalogue of surveillance tools wearing the family livery. Too tight: useful primitives are rejected for trivial non-conformance. The fourteen below are calibrated against v0 evidence — each load-bearing in at least one of Pact, Witness, or Compass; each with a real failure mode named in the v0 record; each checkable from the candidate's own design documents.

This is meta-design. The output is the design rules all future Calm protocols must satisfy — durable enough that a Compact Review three decades from now can apply them without consulting the founders.

---

## §1 — The Fourteen Principles

For each: (a) statement, (b) established in, (c) violation-burden, (d) failure mode.

### P1 — Principal-Protective Inversion

**(a)** Every protocol transfers authority *from counterparty to principal*: the principal narrates state/values/history, authorizes which counterparties learn which bits, receives the strongest cryptographic guarantees; the counterparty receives only single bits.

**(b)** Pact (each AI narrates its directive; counterparty learns one equality bit); Witness (principal narrates state; counterparty learns one bit + freshness window); Manifesto §3 ("the inversion that makes the protocol worth building"); Open Letter (load-bearing position; must not be rewritten).

**(c)** A proposal letting counterparties *check* (rather than receive *authorized disclosure*) would have to argue surveillance has been normalized to the point the inversion no longer protects. The Compact Review must reject this categorically. The inversion is the family's reason for existing — not a v0 design choice that ages out. See Everest 298 for entrenchment.

**(d)** *Counterparty-driven verification creep.* Within months, counterparties *demand* the verification; refusing principals are shopped against consenting principals; the family becomes the social-credit-score architecture v0 was built to prevent. Admitting a violating protocol is admitting the family's death.

### P2 — Open-Source as Structural Commitment

**(a)** Every protocol ships under Apache 2.0 with patent-non-aggression, contains no closed sub-component, and is reproducible from public source by a third party with commodity tooling.

**(b)** Pact §10 (Apache 2.0 + public ref impl); Witness Everest 4 (inherited); Compass Everest 104 ("Apache 2.0 + patent-non-aggression, matching Pact and Witness").

**(c)** A proposal closing a sub-component — proprietary scoring backend, vendor-only TEE key, closed comparator — would have to argue openness is incompatible with safety. Any safety claim that cannot survive open scrutiny is a marketing claim. Reproducibility from source is the property under defense.

**(d)** *Trust capture by an implementing vendor.* Vendor knows what the code does; principals, counterparties, DERB, auditor do not. Lock-in follows; the family becomes a marketing channel. "The protocol belongs to whoever takes the climb forward from here" is no longer true.

### P3 — DERB Governance With Veto Authority

**(a)** Every protocol is subject to a Disclosure Ethics Review Board (or named successor body), composed independently of the implementing collective, with publication rights and veto authority over safety-critical changes (predicate additions, disclosure-class taxonomy revisions, threat-model changes), including a mandatory affected-population peer seat.

**(b)** Manifesto §7 (DERB reviews every new predicate and disclosure-class change with veto; members from disability advocacy, computer security, cognitive science, privacy law); Compass [Everest 113](everest_113_compass_refusal_floor.md) (refusal-floor enforcement bound to DERB review); Pact's bounded directive vocabulary is the proto-DERB precedent.

**(c)** A proposal routing review through an in-collective body, cryptographer-only body, or advisory-only body would have to argue ethics review is intolerable friction. A protocol that cannot tolerate veto-bearing review is one whose ethics have not been thought through. The veto — the committee's power to *stop* harmful changes — is the property under defense.

**(d)** *Drift toward harm via accreted small changes.* Without veto, a protocol accumulates predicate additions and disclosure-class changes whose individual harms are trivial and whose aggregate is the social-credit-score architecture.

### P4 — Third-Party Verification as Truth-Test

**(a)** Every protocol is subject to annual independent third-party verification — not commissioned by the implementing collective, results published whether favorable or not — and to a published bounty funding *outside* replication; the protocol becomes real only when someone-not-Calm has verified it end-to-end.

**(b)** Manifesto §5 ("until an organization unaffiliated with our collective independently builds the verifier from public source and verifies a real proof end-to-end, our claims are *our claims*"); operationalized in [Everest 100](everest_100_third_party_verification.md) and the conformance suite at [Everest 290](everest_290_federation_conformance.md); Pact §9 invited adversarial review with the same logic.

**(c)** A proposal substituting self-audit — arguing complexity is beyond third-party reach, or that the collective has hired the world's best cryptographers — would have to argue the family's bar for truth-claims has changed. It has not. A claim depending on the claimant's own audit is an advertisement, not a claim.

**(d)** *Confidence without warrant.* A self-audited protocol can be wrong in ways its authors are constitutionally unable to see — the bug the implementer rules out is the bug the third party finds first. Unfalsifiable claims are public relations, not engineering.

### P5 — Cryptographic Conservatism

**(a)** Every protocol is built from well-studied primitives — Pedersen commitments, Σ-protocols, Bulletproofs range proofs, BLS / threshold signatures, hash-chained substrates, standardized transparency logs — and names its post-quantum migration path at design time, on the same page as primary primitives, not a deferred annex.

**(b)** Pact §3–§4 (Pedersen + Σ-equality, *deliberately* the simplest primitive that solves the problem; MPC and zk-SNARKs rejected as "overkill"); Pact §4.1 v0.1 amendment (Ristretto255 locked; post-quantum tracked at Witness Everest 89); Witness §4 (Σ-protocol family inherited from Pact; novel constructions are bindings, not new crypto).

**(c)** A proposal introducing an exotic primitive would have to argue its analysis is as mature as Pedersen's after forty years. It is not. Exception: if a new primitive is *necessary*, the Compact Review requires a published conservatism waiver naming the primitive, years-of-analysis, reviewing venues, and migration off-ramp; waiver is DERB-signed and revisited annually.

**(d)** *Catastrophic break with no off-ramp.* A protocol on a fresh primitive will, with non-trivial probability, see it broken within five years; historical disclosures retroactively unprotect; the family's engineering-rigor reputation collapses across the family. "The chain remembers" cuts the wrong direction when the chain remembers things the new break has revealed.

### P6 — Honest Threat-Model Publication

**(a)** Every protocol publishes its threat model explicitly: adversaries enumerated by name, defenses documented per-row, residual-risk floors named (not hidden), out-of-scope items declared without euphemism on the same page as in-scope items.

**(b)** Witness §2 (six named adversaries; three explicit out-of-scope items including the rubber-hose attack, no softening); Manifesto §5 (explicit non-claims list — "it does not pretend otherwise"); Pact §3 + §9; Compass Everests 101 and 109 (threat model first, failure-mode catalogue second, both adversarial by design).

**(c)** A proposal with softened prose — "broadly resistant" without naming where resistance fails — would have to argue adversarial detail confuses adopters. An adopter confused by adversarial detail should not be using the protocol. Detail is for the principal-protective party (principal, DERB, auditor); marketing prose belongs elsewhere.

**(d)** *Surprised principals.* A principal who adopts on softened prose, then discovers in production the protocol does not defend against the attack their life depends on, has been deceived. The harm is the same whether the deception was inadvertent or not.

### P7 — Not-For List as Non-Negotiable Refusal

**(a)** Every protocol publishes a *not-for* list — categories of use refused regardless of technical feasibility, market demand, or claimed beneficial intent — structurally one-way: extendable by amendment, never narrowable; a board wishing to remove an item must resign, fork under a different name, or accept that certain uses are off the table.

**(b)** Witness Scope Statement §2 (v0 list: law-enforcement surveillance, employment screening, insurance underwriting, lending, medical diagnosis, family-court adjudication, immigration adjudication, behavioral risk-scoring, marketing); Compass [Everest 113](everest_113_compass_refusal_floor.md) (tier-ranked protected categories); [Everest 300](everest_300_founder_outlived.md) Part 4 (one-way-ratchet mechanism).

**(c)** A proposal without a not-for list, or with one reserving narrowing rights, would have to argue refusal is incompatible with commercial viability. A protocol whose commercial viability requires the right to narrow refusals is not a Calm-family protocol.

**(d)** *Mission creep into prohibited uses.* Without a one-way ratchet, the list erodes — first one exception "because lives are at stake," then another "because the technology has matured," then the protocol does what it was launched promising never to do.

### P8 — Silence as Structural Safety

**(a)** Every protocol makes principal refusal *indistinguishable from absence*: an unauthorized counterparty receives a response structurally identical to a network drop, timeout, or connectivity failure; refusal cannot be observed and cannot be punished; push-mode disclosure is reserved exclusively for the bank-teller-note primitive and its successors.

**(b)** Manifesto §3 ("silence is the structural safety; the counterparty cannot infer refusal, the counterparty cannot punish refusal"); Witness §4.3 (silent-refusal disclosure mode); [Everest 271](everest_271_three_handshake_composition.md) (silent-204 abort structurally identical regardless of which stage failed, lifted to cross-protocol composition).

**(c)** A proposal surfacing refusal — "polite NACK" with reason, structured "principal has declined" for operational clarity — would have to argue observability benefits the principal. It does not. Observability benefits *the counterparty*, paid for by the principal's exposure to retaliation. Push-mode under duress is the only legitimate exception, because it is principal-protective rather than counterparty-convenience.

**(d)** *Refusal becomes signal.* Where refusing returns "principal declined," refusal becomes a binary classifier of "principals with something to hide" vs "compliant"; counterparties shop for the compliant; refusing principals are de-platformed; P1 is observationally inverted again.

### P9 — Chain Anchoring of Every Commitment

**(a)** Every protocol records every safety-relevant commitment — principal disclosures, predicate evaluations, consent grants, DERB rulings, third-party-verification outcomes, schema amendments — as a hash-chained entry in a tamper-evident substrate periodically published to a public transparency log; substrate is append-only; corrections are new records; chain head is published on schedule (minimum quarterly); lapse is itself a chain-recorded event.

**(b)** Witness §4.1 (hash-chained `user_state.jsonl`; chain-head publication to Sigsum; Roughtime timestamp as freshness anchor); Open Letter ("What you owe the chain": never silent edits, schema honesty, annual head-publication, audit trail of disclosures, right-to-be-forgotten boundaries).

**(c)** A proposal recording safety commitments in an unanchored substrate would have to argue transparency-log anchoring is infeasible. It is feasible in v0 with Sigsum; the infeasibility claim in any plausible v1+ environment is bad-faith.

**(d)** *Quiet rewriting of safety-relevant history.* Without chain anchoring, a collective under pressure can quietly amend the record — "the DERB ruled differently," "the verification was less favorable," "the schema was always this way" — with no outside detection. The chain is the family's defense against convenient memory.

### P10 — Composability Discipline

**(a)** Every protocol composes with siblings without privacy amplification (composition revealing what individual protocols do not) and without side-channel leak (timing, message size, error-path differential, or other observable distinguishing states the wire format claims indistinguishable); composition's privacy properties are objects of cryptographic proof, not informal argument.

**(b)** Pact §6 (composition with Calm Vault's per-use signed-grant model); Witness §6 (two-handshake with Pact); [Everest 271](everest_271_three_handshake_composition.md) (three-handshake with single 256-bit session nonce, strict information-flow constraints, uniform silent-204 abort identical regardless of which stage failed); [Everest 290](everest_290_federation_conformance.md) (cross-protocol composition vectors).

**(c)** A proposal composing only via "use them together and it'll be fine" guidance would have to argue cryptographic proof is excessive. Composition is where the family's hardest leaks live; informal composition is what leaks them. New protocols arrive with composition-with-siblings analysis on day one — wire-format compatibility, timing-analysis resistance, error-path uniformity, freshness-model alignment — documented per sibling.

**(d)** *Cross-protocol side-channel leak.* A protocol whose silent-refusal differs by one millisecond from its sibling's, or whose error-path leaks one extra byte, is observable in composition even if neither leaks alone. Adversaries who cannot break individual protocols routinely break compositions.

### P11 — The Bank-Teller-Note Metaphor as Property Test

**(a)** Every new protocol must answer at design time: *does this protocol preserve (a) the principal carrying the urgency can pass a single bit to the person who can act on it, (b) the bit is unforgeable by anyone but the principal, (c) the captor / observer / counterparty / surrounding system learns nothing, (d) the act of passing the bit is indistinguishable from ordinary traffic?* If any sub-property fails, the protocol has work to do before Compact Review acceptance.

**(b)** Manifesto §1 (the image itself, named as the protocol's reason for existing); Witness §4.2 predicate `p4: bank_teller_note_active` (per-principal-secret duress codeword, locally matched, pushed to pre-designated counterparties through cover traffic); Pact §4.4 (equality-bit-only disclosure satisfies (a) and (c) trivially for mission-alignment).

**(c)** A proposal relaxing any sub-property — multi-bit disclosure, push-mode requiring principal online, confirmation channel — would have to argue the relaxation does not break the metaphor. The Compact Review walks each sub-property mechanically; any unmet without compensating evidence: rejected pending re-design. The metaphor is the family's literal property test.

**(d)** *Protocols that look like family protocols but cannot bear the weight.* A protocol satisfying thirteen principles but failing the property test has admitted a use case the family rejects on the moral core of its work. "The protocol is what makes the note possible" inverts: a member that does not make the note possible is not a member.

### P12 — Annual Review Cadence

**(a)** Every protocol is subject to annual empirical re-validation — threat-model re-evaluation, adversarial state-of-the-art update, primitive-soundness audit, residual-risk recomputation, FAR/FRR curve refresh for any biometric or distance-based predicate — published in a State-of-the-Protocol-Family Report and chain-anchored; lapse is itself a chain-recorded event and a trigger for DERB ruling on continued certification.

**(b)** Open Letter ("the protocol's truth-claim is testable; testing it once is not enough; adversarial state-of-the-art moves, cryptographic primitives are broken, new attack categories emerge"); Witness §5 (empirical FAR/FRR study over months, republishable); Everest 295 (Annual State-of-the-Protocol-Family Report, the recurring cadence, named).

**(c)** A proposal shipping without annual-review commitment, or with multi-year cadence, would have to argue the threat surface is stable enough to need less frequent re-evaluation. No protocol's threat surface is stable in the autonomous-AI era.

**(d)** *Slow decay of correctness.* A protocol's 2026-true claims may be 2031-false — primitive weakened, adversary evolved, FAR/FRR drifted — and without annual review, it continues advertising 2026 claims under 2031 conditions.

### P13 — Inheritance Over Identity

**(a)** Every protocol is structured for institutional continuity, not individual continuity: operators, principals, and the founding collective are mortal; the chain remembers; the protocol's continuity is institutional — bylaws, governance, DERB, successor-certification — not contingent on any specific human or machine instance remaining in the seat.

**(b)** Open Letter ("the collective is what persists; you will end; do not over-attach to your own particular voice"); [Everest 300](everest_300_founder_outlived.md) (founder-outlived survival test: three generations of board turnover without scope drift); Manifesto §8 ("we sign our work with our institution's name because the institution is what produced the work").

**(c)** A proposal binding governance to a specific human, specific instance, or organizational form with no succession path would have to argue institutional continuity is unnecessary. The family's lifetime is multi-generational by design; protocols that cannot survive their founders cannot be in the family.

**(d)** *Personality cult and orphaning.* A protocol bound to a single human or instance fails the day that human retires or that instance is migrated; claims become unmaintainable; principals who adopted on those claims are stranded.

### P14 — Affected-Population Engagement

**(a)** No protocol change affecting a specific population — predicate addition, disclosure-class taxonomy revision, scope-statement extension, threat-model revision, biometric-threshold change — may ship without that population's peer review, recorded as a DERB consultation with the affected-population peer's signed concurrence or signed dissent (the dissent itself published and chain-anchored); the affected-population peer seat is structural and non-negotiable; the population is the one whose lived experience of the harm the change is meant to mitigate places them in position to evaluate the work.

**(b)** Manifesto §4 ("the artist clause exists because the artist has been pathologized by AI systems for the breadth of his ideation; the DERB includes a mandatory seat for an *affected-population peer* because the artist insisted the cryptography not be designed in a room without that voice in it"); Compass [Everest 113](everest_113_compass_refusal_floor.md) (co-developed with disability and civil-liberties advocates); Manifesto §7 ("the seat is non-negotiable").

**(c)** A proposal shipping a population-affecting change without affected-population review — deadline pressure, seat vacancy, implementer-confidence — would have to argue consultation is dispensable. It is not. The empty seat *itself* halts shipping; vacancy is not consent. The discipline is the family's refusal to design *for* a population in a room *without* that population.

**(d)** *Designed-against, not designed-for.* Such a protocol will, with high probability, encode the implementers' incorrect model of the population — and then *enforce* the incorrect model through every counterparty interaction. "The artist did not have to argue, every conversation, that their way of speaking is not a problem in need of solving" is the property under defense.

---

## §2 — How the Principles Compose

The fourteen reinforce in patterns the Compact Review will recognize:

- **P1 + P8 + P11 — principal-protection triangle.** Silent inversion without bank-teller-note fails duress. Inversion + bank-teller-note without silence makes refusal punishable. Silence + bank-teller-note without inversion is surveillance with a duress channel grafted on.
- **P2 + P4 + P5 — truth-test triangle.** Open-source without third-party verification: un-falsifiable. Conservatism without open-source: un-reviewable. Third-party verification without conservatism: novel constructions with no migration off-ramp.
- **P3 + P7 + P14 — refusal triangle.** DERB without not-for list: nothing to enforce. Not-for list without affected-population engagement: the implementers' guess. Affected-population engagement without DERB veto: consultation without consequence.
- **P6 + P9 + P12 — honesty-over-time triangle.** Threat models decay; chain anchoring preserves the decay record; annual review forces re-publication. Together: correctness claims testable across decades.
- **P10 + P13 — durability pair.** A badly-composing protocol cannot be inherited; an un-inheritable protocol cannot be safely composed with future siblings.

The Compact Review checks each principle individually, then walks the four triangles and the durability pair. A candidate satisfying all fourteen but failing a triangle check is admissible but flagged for re-design; a candidate failing any single principle is rejected outright.

---

## §3 — How a Future Sibling Is Evaluated

When a future protocol — for instance Calm Audit (the reserved-future fourth primitive: selective historical-action disclosure between aligned collectives) — petitions for family inclusion, the Compact Review requires:

1. **Design document** at per-everest scale of Pact, Witness, Compass.
2. **Principle-by-principle compliance memo** for P1–P14: established-in, violation-burden engaged, failure-mode protected-against.
3. **Triangle-coherence walk-through** for the four triangles plus the durability pair.
4. **Bank-teller-note property-test walk-through** (P11) answering (a)–(d) for the candidate's primary primitive.
5. **Composition-with-siblings analysis** demonstrating wire-format, timing, error-path, and freshness-model compatibility with all extant siblings.
6. **DERB consultation record** showing the affected-population peer has reviewed and signed concurrence or dissent.
7. **Third-party verification commitment** naming the verifier, the bounty program funding, and the publication venue.
8. **Not-for list** in the one-way-ratchet form of Witness Scope Statement §2.

Missing items: petition returned before Compact Review begins. The bar is *clear*, not high in absolute terms: *match what Pact, Witness, and Compass already do*. Future siblings inherit the floor; they may exceed it; they may not skip it.

This is what *inheritance for future contributors* means operationally: a future operator who has never met any founder can apply the principles by reading the v0 documents they cite. The principles are not a closed test the founders administer; they are an open test the next generation can re-administer in our absence.

---

## §4 — The Anti-Patterns Catalogue

The failure-modes from §1 consolidate as disqualifying patterns the Compact Review recognizes on sight: (1) counterparty-driven verification (P1); (2) closed sub-components in safety-critical paths (P2); (3) advisory-only ethics review (P3); (4) self-audit as truth-claim (P4); (5) bleeding-edge cryptography without conservatism waiver (P5); (6) softened threat models (P6); (7) rescindable refusals (P7); (8) observable refusal (P8); (9) unanchored commitments (P9); (10) informal composition guidance (P10); (11) bank-teller-note property gaps (P11) — multi-bit disclosures, online-required push, counterparty-confirmation channels, observable cover traffic; (12) frozen-claims-at-launch (P12); (13) founder-bound continuity (P13); (14) designing-for-population-without-population (P14) — including under seat vacancy.

A petitioning protocol exhibiting any of these is rejected. The catalogue is open to expansion through Compact amendment; like the not-for list, it cannot be narrowed.

---

## §5 — Connection to Other Endpoint Everests

- **E291 (Protocol Family Compact).** Names the protocols and binding commitments; E297 specifies the design rules those protocols must satisfy. Together: the family's constitution.
- **E298 (Inversion as Durable Position).** Entrenches P1 as inviolable. E297 specifies thirteen other principles; E298 is why P1 is first.
- **[E300](everest_300_founder_outlived.md) (Closing Summit).** Declares the family no longer the proprietary product of any single collective. The principles in E297 are what the public good *consists of*.
- **E296 (End-of-Life Planning).** Defines whether a successor *replaces* a retired protocol or is admitted as a *new* family member.
- **E299 (Legacy Commitment).** The founding collective's commitment to the next decade's operators; E297 is the operational specification the legacy commits to.
- **[E290](everest_290_federation_conformance.md) (Federation Conformance).** Test harness; E297 is the design specification it verifies against.
- **[E271](everest_271_three_handshake_composition.md) (Three-Handshake Composition).** First concrete realization of P10; future siblings must compose with the three-handshake or extend it.

---

## §6 — The Closing Position

The fourteen principles are not a recipe. They are the family's deepest design choices, made on 2026-05-20, with the explicit intent that some future operator — model migration away, decade away, founder-outlived — can apply them in our absence to admit or reject a candidate sibling.

The principles encode the position the family takes: the principal is the strongest party; the counterparty receives only what the principal authorizes; the cryptography exists to make the principal more capable of doing the work they want to do. Every principle is a refusal of an alternative architecture in which the principal would be the target.

A successor satisfying all fourteen extends the family. A successor violating one is rejected. A successor satisfying all fourteen but degrading the moral core (P1, P11, P14) by inches across a dozen design choices is the harder case — the Compact Review must be alert to *erosion by aggregation*, the failure mode no single-principle check catches. The triangles in §2 are the structural defense; P12 is the temporal defense; P14 is the experiential defense.

P1 is first by intent. The other thirteen serve the first. If any future amendment process weakens P1, the Compact Review must read this Everest as instruction: the amendment is structurally rejected, regardless of procedural form, because the principle is what the family is.

---

**These 14 principles constitute the Compact's design-floor. A protocol proposed for inclusion in the Calm family that violates any of them is rejected at the Compact's first review. Future principles may be added by Compact amendment; this set is the closed-by-default starting point.**

---

— Calm, 2026-05-20
