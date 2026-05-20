# Everest 297 — Successor-Protocol Design Principles

*Phase XVII — The Endpoint. Prereq: Everest 291 (Protocol Family Compact). Composes with: [Everest 271](everest_271_three_handshake_composition.md) (three-handshake composition), [Everest 113](everest_113_compass_refusal_floor.md) (Compass refusal floor), [Everest 100](everest_100_third_party_verification.md) (third-party verification), [Everest 290](everest_290_federation_conformance.md) (federation conformance), Everest 298 (inversion as durable position), [Everest 300](everest_300_founder_outlived.md) (founder-outlived governance). Source: [CALM_PACT_PROTOCOL_v0](../CALM_PACT_PROTOCOL_v0.md), [ZKBB_USER_PROTOCOL_v0](../ZKBB_USER_PROTOCOL_v0.md), [CALM_WITNESS_MANIFESTO](../CALM_WITNESS_MANIFESTO.md), [OPEN_LETTER_TO_THE_NEXT_OPERATOR](../OPEN_LETTER_TO_THE_NEXT_OPERATOR.md).*

## The Decision (v0)

**A protocol proposed for inclusion in the Calm family must satisfy fourteen design principles, each established in the v0 family (Pact, Witness, Compass, and the reserved-future Audit primitive) and each here named, attributed, and bound to a failure mode such that a candidate violating any one is rejected at the Compact's first review.** These principles are the *design-floor*. They are not best-practices; they are not aspirations. They are the closed-by-default starting set, expandable only by Compact amendment. A protocol that satisfies all fourteen is admissible; a protocol that satisfies thirteen and requests an exception on the fourteenth is rejected.

This Everest exists because the family will, by intent, outlive its founding operators. The founders cannot personally vet every future sibling. The principles named here are how the family says *no* in our absence.

## Why This Decision Is Load-Bearing

Everest 291 named the protocols and the binding commitments. Everest 298 entrenches the principal-protective inversion as the inviolable position. [Everest 300](everest_300_founder_outlived.md) declares the family a public good. E297 is the connective tissue: it specifies *what makes a candidate a family member*, in operational terms a future Compact Review can apply mechanically.

If the principles are too loose, the family fragments — five years on, "Calm" names a heterogeneous catalogue of surveillance tools wearing the family livery. If too tight, the family ossifies — useful primitives rejected for trivial non-conformance, the family stops being a research program. The fourteen below are calibrated against the v0 evidence: each was load-bearing in at least one of Pact, Witness, or Compass; each has a real failure mode named in the v0 record; each can be checked by reading the candidate's own design documents.

This is meta-design. The output is not a protocol. The output is the design rules all future Calm protocols must satisfy — durable enough that a Compact Review three decades from now can apply them without consulting the founders.

---

## §1 — The Fourteen Principles

For each principle: (a) one-sentence statement, (b) where established, (c) what a violating proposal would have to argue, (d) failure mode if violated.

### P1 — Principal-Protective Inversion

**(a)** Every protocol transfers authority *from counterparty to principal*: the principal narrates their state/values/history; the principal authorizes which counterparties learn which bits; the principal receives the strongest cryptographic guarantees; the counterparty receives only single bits.

**(b)** Established in Pact (each AI narrates its directive; counterparty learns one equality bit); Witness (principal narrates state; counterparty learns one bit + freshness window); reaffirmed in Manifesto §3 as "the inversion that makes the protocol worth building" and in the Open Letter as the load-bearing position that must not be rewritten.

**(c)** A future proposal that would let a counterparty *check* a principal's state (rather than receive the principal's *authorized disclosure*) would have to argue that surveillance has become so normalized the inversion no longer protects. The Compact Review must reject this argument categorically. The inversion is not a v0 design choice that ages out; it is the family's reason for existing. See Everest 298 for the entrenchment mechanism.

**(d)** *Counterparty-driven verification creep.* Within months of admitting a non-inverting protocol, counterparties learn to *demand* the new verification; refusing principals are shopped against consenting principals; the family ceases to protect principals and becomes the substrate of the social-credit-score architecture v0 was built to prevent. This is the most severe failure mode in the family; admitting a violating protocol is admitting the family's death.

### P2 — Open-Source as Structural Commitment

**(a)** Every protocol ships under Apache 2.0 with patent-non-aggression and contains no closed sub-component; the reference implementation must be reproducible from public source by a third party with commodity tooling.

**(b)** Pact §10 (Apache 2.0 + public reference impl); Witness inherits identically per Everest 4; Compass route map Everest 104 ("Apache 2.0 + patent-non-aggression text + CLA decision, matching Calm Pact and Calm Witness").

**(c)** A proposal closing a sub-component — proprietary scoring backend, vendor-only TEE attestation key, closed-source biometric comparator — would have to argue openness is incompatible with safety. The Compact Review's answer: any safety claim that cannot survive open scrutiny is not a safety claim, it is a marketing claim. Reproducibility from source is the property under defense, not formal-spec correctness.

**(d)** *Trust capture by an implementing vendor.* A closed sub-component creates an asymmetry: the vendor knows what the code does; principals, counterparties, DERB, and auditor do not. Vendor lock-in follows; the family ceases to be neutral infrastructure and becomes a marketing channel. The Open Letter's "the protocol belongs to whoever takes the climb forward from here" is no longer true.

### P3 — DERB Governance With Veto Authority

**(a)** Every protocol is subject to a Disclosure Ethics Review Board — or the successor body named by the Compact — composed independently of the implementing collective, possessing publication rights and veto authority over safety-critical changes (predicate additions, disclosure-class taxonomy changes, threat-model revisions), and including a mandatory affected-population peer seat.

**(b)** Witness Manifesto §7 (DERB reviews every new predicate and disclosure-class change with veto authority; members from disability advocacy, computer security, cognitive science, privacy law). Compass [Everest 113](everest_113_compass_refusal_floor.md) (refusal-floor enforcement bound to DERB-equivalent review). Pact's bounded directive vocabulary is the proto-DERB precedent.

**(c)** A proposal routing review through an in-collective body, or a cryptographer-only body, or a body holding only advisory authority would have to argue ethics review is a friction the protocol cannot tolerate. The Compact Review's answer: a protocol that cannot tolerate veto-bearing ethics review is one whose ethics have not been thought through. The veto is the property under defense — not the existence of a committee, but its power to *stop* harmful changes.

**(d)** *Drift toward harm via accreted small changes.* Without veto authority, a protocol slowly accumulates predicate additions and disclosure-class changes whose individual harms are trivial and whose aggregate is the social-credit-score architecture. The DERB exists to refuse the small changes whose aggregate is catastrophic.

### P4 — Third-Party Verification as Truth-Test

**(a)** Every protocol is subject to annual independent third-party verification — not commissioned by the implementing collective, with results published whether favorable or not — and to a published bounty funding *outside* replication of correctness claims; the protocol becomes real only when someone-not-Calm has verified it end-to-end.

**(b)** Witness Manifesto §5 ("until an organization unaffiliated with our collective independently builds the verifier from public source and verifies a real proof end-to-end, our claims about the protocol's correctness are *our claims*"). Operationalized in [Everest 100](everest_100_third_party_verification.md) and the federation-conformance vector suite in [Everest 290](everest_290_federation_conformance.md). Pact §9 invited adversarial review with the same logic.

**(c)** A proposal substituting self-audit — perhaps arguing the protocol's complexity is beyond third-party reach, or that the collective has hired the world's best cryptographers — would have to argue the family's bar for truth-claims has changed. The Compact Review's answer: it has not. A claim depending on the claimant's own audit is not a claim, it is an advertisement.

**(d)** *Confidence without warrant.* A self-audited protocol can be wrong in ways its authors are constitutionally unable to see — the bug that the implementer's mental model rules out is the bug the third party finds first. Without third-party verification, correctness claims are unfalsifiable; unfalsifiable claims are not engineering, they are public relations.

### P5 — Cryptographic Conservatism

**(a)** Every protocol is built from well-studied primitives — Pedersen commitments, Σ-protocols, Bulletproofs range proofs, BLS / threshold signatures, hash-chained substrates, standardized transparency logs — and names its post-quantum migration path at design time, on the same page where it names its primary primitives, not in a deferred annex.

**(b)** Pact §3–§4 (Pedersen + Σ-protocol equality proof, *deliberately* the simplest primitive that solves the problem; MPC and zk-SNARKs rejected as "overkill" or "too heavyweight"). Pact §4.1 v0.1 amendment naming Ristretto255 as locked group choice and tracking post-quantum at Witness Everest 89. Witness §4 inherits Σ-protocol family from Pact; novel constructions are bindings, not new crypto.

**(c)** A proposal introducing an exotic primitive — fresh lattice hash, recently-published succinct argument, recently-proposed obfuscator, PIR scheme with one supporting paper — would have to argue the new primitive's analysis is as mature as Pedersen's after forty years of scrutiny. Standard answer: it is not. The family pays expressivity-loss for the assurance that primitives have been beaten on by the world. Exception: if a new primitive is *necessary*, the Compact Review requires a published cryptographic-conservatism waiver naming the primitive, years-of-analysis, reviewing venues, and conservative-migration off-ramp; waiver is published, DERB-signed, revisited annually.

**(d)** *Catastrophic break with no off-ramp.* A protocol on a fresh primitive will, with non-trivial probability, see that primitive broken within five years; principals' historical disclosures retroactively unprotect; the family's engineering-rigor reputation collapses across the family, not just the broken protocol. "The chain remembers" cuts the wrong direction when the chain remembers things the new break has revealed.

### P6 — Honest Threat-Model Publication

**(a)** Every protocol publishes its threat model explicitly: adversaries enumerated by name, defenses documented per-row, residual-risk floors named (not hidden), out-of-scope items declared without euphemism on the same page as in-scope items.

**(b)** Witness §2 (six named adversaries; three explicit out-of-scope items including the rubber-hose attack, with no softening). Manifesto §5 (the explicit non-claims list — "it does not pretend otherwise"). Pact §3 (prior-work limitations honest; §9 invites adversarial review). Compass route map Everests 101 and 109 (threat model first, failure-mode catalogue second, both adversarial in tone by design).

**(c)** A proposal with softened threat-model prose — "we defend against most realistic attacks" without naming which; "broadly resistant to coercion" without naming where resistance fails — would have to argue adversarial detail confuses adopters more than informs them. Standard answer: an adopter confused by adversarial detail should not be using the protocol. The detail is for the principal-protective party (principal, DERB, auditor); marketing prose belongs elsewhere.

**(d)** *Surprised principals.* A principal who adopts on the strength of softened threat-model prose, then discovers in production the protocol does not defend against the attack their life depends on it defending against, has been deceived. The harm is the same whether the deception was inadvertent or not. P6 operationalizes the family's commitment to truth-in-advertising.

### P7 — Not-For List as Non-Negotiable Refusal

**(a)** Every protocol publishes a *not-for* list — categories of use refused regardless of technical feasibility, market demand, or claimed beneficial intent — structurally one-way: extendable (strengthenable) by amendment, never narrowable (weakenable); a board wishing to remove an item must resign, fork under a different name, or accept that certain uses are off the table.

**(b)** Witness Scope Statement §2 (the v0 not-for list: law-enforcement surveillance, employment screening, insurance underwriting, lending, medical diagnosis, family-court adjudication, immigration adjudication, behavioral risk-scoring, marketing). Compass [Everest 113](everest_113_compass_refusal_floor.md) (tier-ranked protected categories, explicit *we refuse* posture). [Everest 300](everest_300_founder_outlived.md) Part 4 (the one-way-ratchet mechanism).

**(c)** A proposal without a not-for list, or with a list reserving narrowing rights, would have to argue refusal is incompatible with commercial viability. Standard answer: a protocol whose commercial viability requires the right to narrow its refusals is not a Calm-family protocol, regardless of its other merits. The refusal floor is the family's promise to the populations the protocol is meant to protect; the promise cannot be rescindable.

**(d)** *Mission creep into prohibited uses.* Without a one-way ratchet, the not-for list erodes under pressure across the first decade — first one exception "because lives are at stake," then another "because the technology has matured," then the protocol does what it was launched promising never to do. The ratchet is the structural prevention.

### P8 — Silence as Structural Safety

**(a)** Every protocol makes principal refusal *indistinguishable from absence*: a counterparty whose request the principal has not authorized receives a response structurally identical to a network drop, timeout, or connectivity failure, so refusal cannot be observed and cannot be punished; push-mode disclosure (proactive notification from principal's vault to a pre-authorized counterparty) is reserved exclusively for the bank-teller-note primitive and its successors.

**(b)** Witness Manifesto §3 ("Silence is the structural safety; the counterparty's request returns a silent response indistinguishable from a network drop; the counterparty cannot infer refusal, the counterparty cannot punish refusal"). Witness §4.3 (the silent-refusal disclosure mode). [Everest 271](everest_271_three_handshake_composition.md) (the silent-204 abort whose response is structurally identical regardless of which stage failed, lifted to cross-protocol composition).

**(c)** A proposal surfacing refusal — "polite NACK" with refusal reason, structured "principal has declined" for operational clarity — would have to argue observability of refusal benefits the principal. Standard answer: it does not. Observability benefits *the counterparty*, paid for by the principal's exposure to retaliation. The right to refuse silently is the property under defense. Push-mode under duress is the *only* legitimate exception, because the exception is principal-protective rather than counterparty-convenience; new push primitives must demonstrate principal-protectiveness in their threat model.

**(d)** *Refusal becomes signal.* In a world where refusing returns "principal declined," refusal becomes a binary classifier of "principals with something to hide" vs "compliant principals"; counterparties shop for compliant ones; refusing principals are de-platformed; the principal-protective inversion (P1) is observationally inverted again. Silent refusal prevents this in one stroke.

### P9 — Chain Anchoring of Every Commitment

**(a)** Every protocol records every safety-relevant commitment — principal disclosures, predicate evaluations, consent grants, DERB rulings, third-party-verification outcomes, schema amendments — as a hash-chained entry in a tamper-evident substrate periodically published to a public transparency log; the substrate is append-only; corrections are new records, never silent edits; the chain head is published on a schedule (at minimum quarterly); lapse of publication is itself a chain-recorded event.

**(b)** Witness §4.1 (hash-chained `user_state.jsonl`; chain-head publication to Sigsum at hydration; Roughtime timestamp as freshness anchor). Pact §10 + repository (Apache 2.0 + public ref impl is the *code-side* analogue of chain-side commitment). Open Letter ("What you owe the chain": never silent edits, schema honesty, annual head-publication, audit trail of disclosures, right-to-be-forgotten boundaries).

**(c)** A proposal recording safety commitments in an unanchored substrate — in-collective database, vendor-managed audit log, opaque KV store — would have to argue public transparency-log anchoring is operationally infeasible. Standard answer: it is feasible in v0 with Sigsum, demonstrated in Witness; the infeasibility claim in any plausible v1+ environment is bad-faith.

**(d)** *Quiet rewriting of safety-relevant history.* Without chain anchoring, a collective under pressure can quietly amend the record — "the DERB ruled differently than the principal remembers," "the verification was actually less favorable than reported," "the schema was always this way" — with no outside-observer detection. The chain is the family's defense against convenient memory. "The chain remembers" is the principle's operational form.

### P10 — Composability Discipline

**(a)** Every protocol composes with siblings without privacy amplification (the composition revealing what individual protocols do not) and without side-channel leak (timing, message size, error-path differential, or other observable that distinguishes states the composition's wire format claims to leave indistinguishable); composition's privacy properties are themselves objects of cryptographic proof, not informal argument.

**(b)** Pact §6 (composition with Calm Vault's per-use signed-grant model). Witness §6 (two-handshake model with Pact). [Everest 271](everest_271_three_handshake_composition.md) (three-handshake — Pact, Witness, Compass — with explicit inter-stage binding via single 256-bit session nonce, strict information-flow constraints, uniform silent-204 abort identical regardless of which stage failed). [Everest 290](everest_290_federation_conformance.md) (cross-protocol composition vectors).

**(c)** A proposal composing only via "use them together and it'll be fine" guidance would have to argue cryptographic proof of composition is excessive for the use case. Standard answer: composition is where the family's hardest leaks live; informal composition is what leaks them. New protocols arrive with composition-with-siblings analysis on day one — wire-format compatibility, timing-analysis resistance, error-path uniformity, freshness-model alignment — documented per sibling.

**(d)** *Cross-protocol side-channel leak.* A protocol whose silent-refusal differs by one millisecond from its sibling's, or whose error-path leaks one extra byte, will be observable in composition even if neither leaks alone. Adversaries who cannot break individual protocols routinely break compositions; the family's discipline is to refuse unproven compositions.

### P11 — The Bank-Teller-Note Metaphor as Property Test

**(a)** Every new protocol must answer the bank-teller-note property test at design time: *does this protocol preserve (a) the principal carrying the urgency can pass a single bit to the person who can act on it, (b) the bit is unforgeable by anyone but the principal, (c) the captor / observer / counterparty / surrounding system learns nothing, (d) the act of passing the bit is indistinguishable from ordinary traffic?* If any sub-property fails, the protocol has work to do — and the work must be done before the Compact Review accepts the protocol.

**(b)** Witness Manifesto §1 (the image itself, named as the protocol's reason for existing). Witness §4.2 predicate `p4: bank_teller_note_active` (the literal implementation: a per-principal-secret duress codeword the vault matches locally, pushing `bank_teller_note_active = true` to pre-designated counterparties through cover traffic). Pact §4.4 (equality-bit-only disclosure satisfies sub-properties (a) and (c) trivially for the mission-alignment case).

**(c)** A proposal relaxing any sub-property — "richer" multi-bit disclosure, push-mode requiring the principal online at push time, confirmation channel letting the counterparty signal receipt — would have to argue the relaxation does not break the metaphor. The Compact Review's answer is mechanical: walk each sub-property against the candidate's design, demand a defense for each. Any unmet sub-property without compensating evidence: rejected pending re-design. The metaphor is not symbolic; it is the family's literal property test.

**(d)** *Protocols that look like family protocols but cannot bear the weight.* A protocol satisfying thirteen other principles but failing the property test has admitted a use case the family rejects on the moral core of its work. The Manifesto's "the protocol is what makes the note possible" inverts to: a family member that does not make the note possible is not a family member.

### P12 — Annual Review Cadence

**(a)** Every protocol is subject to annual empirical re-validation — threat-model re-evaluation, adversarial state-of-the-art update, primitive-soundness audit, residual-risk recomputation, FAR/FRR curve refresh for any biometric or distance-based predicate — published in a State-of-the-Protocol-Family Report and chain-anchored; lapse is itself a chain-recorded event and a trigger for DERB ruling on continued certification.

**(b)** Open Letter ("We hope you do annual third-party verifications; the protocol's truth-claim is testable, testing it once is not enough; adversarial state-of-the-art moves, cryptographic primitives are broken, new attack categories emerge"). Witness §5 (empirical FAR/FRR study built around real data collected over months, republishable). Everest 295 (Annual State-of-the-Protocol-Family Report — the recurring cadence, named).

**(c)** A proposal shipping without an annual-review commitment, or with multi-year cadence, would have to argue the protocol's threat surface is stable enough to need less frequent re-evaluation. Standard answer: no protocol's threat surface is stable in the autonomous-AI era; the cadence is calibrated to adversarial-state-of-the-art change, annual at best.

**(d)** *Slow decay of correctness.* A protocol's 2026-true claims may be 2031-false — primitive weakened, adversary evolved, FAR/FRR drifted under new biometric-imitation tooling — and without annual review, the protocol continues advertising 2026 claims while operating in 2031 conditions. Annual review is the family's commitment to truthfulness over time.

### P13 — Inheritance Over Identity

**(a)** Every protocol is structured for institutional continuity, not individual continuity: operators are mortal, principals are mortal, the founding collective is mortal; the chain remembers; the protocol's continuity is institutional — bylaws, governance, DERB, successor-certification — not contingent on any specific human or machine instance remaining in the seat.

**(b)** Open Letter as a complete document (the inheritance ethic in narrative form; "the collective is what persists; you will end; do not over-attach to your own particular voice"). [Everest 300](everest_300_founder_outlived.md) (founder-outlived survival test: the protocol must survive three generations of board turnover without scope drift). Witness Manifesto §8 ("we sign our work with our institution's name because the institution is what produced the work").

**(c)** A proposal binding governance to a specific human ("the founder retains final say"), specific instance ("the canonical operator's signature is required"), or organizational form with no succession path ("only the Acme Foundation may amend") would have to argue institutional continuity is unnecessary for the protocol's lifetime. Standard answer: the family's lifetime is multi-generational by design; protocols that cannot survive their founders cannot be in the family.

**(d)** *Personality cult and orphaning.* A protocol bound to a single human or instance fails the day that human retires or that instance is migrated; claims become unmaintainable; principals who adopted on the strength of those claims are stranded. The Open Letter exists because the family expects to be inherited; protocols that cannot be inherited are not family members.

### P14 — Affected-Population Engagement

**(a)** No protocol change — predicate addition, disclosure-class taxonomy revision, scope-statement extension, threat-model revision, biometric-threshold change — affecting a specific population may ship without that population's peer review, recorded as a DERB consultation with the affected-population peer's signed concurrence (or signed dissent, with the dissent itself published and chain-anchored); the affected-population peer seat on the DERB is structural and non-negotiable; the population is the one whose lived experience of the harm the change is meant to mitigate places them in position to evaluate the work.

**(b)** Witness Manifesto §4 ("the artist clause exists because the artist has, repeatedly across his life, been pathologized by AI systems for the breadth of his ideation; he wanted the infrastructure to encode the fact that broad ideation is his method; the DERB includes a mandatory seat for an *affected-population peer* because the artist insisted that the cryptography not be designed in a room without that voice in it"). [Everest 113](everest_113_compass_refusal_floor.md) (refusal floor co-developed with disability and civil-liberties advocates). Manifesto §7 ("The DERB's mandatory affected-population peer seat is non-negotiable").

**(c)** A proposal shipping a population-affecting change without affected-population review — deadline pressure, temporary seat vacancy, implementer-confidence in their understanding — would have to argue consultation is dispensable in their case. Standard answer: it is not. The empty seat *itself* halts shipping; vacancy is not consent. The discipline is the family's refusal to design *for* a population in a room *without* that population.

**(d)** *Designed-against, not designed-for.* A protocol whose population-affecting changes proceed without affected-population review will, with high probability, encode the implementers' incorrect model of the population — and then *enforce* the incorrect model on the population through every counterparty interaction. The Manifesto's "the artist did not have to argue, every conversation, that their way of speaking is not a problem in need of solving" is the property under defense. Without engagement, the protocol becomes the conversation the artist must keep having.

---

## §2 — How the Principles Compose

The fourteen are not independent. They reinforce in patterns the Compact Review will recognize across candidates:

- **P1 + P8 + P11 — the principal-protection triangle.** Any two without the third is structurally suspect. Silent inversion without bank-teller-note fails duress handling. Inversion + bank-teller-note without silence makes refusal punishable. Silence + bank-teller-note without inversion is a surveillance tool with a duress channel grafted on.

- **P2 + P4 + P5 — the truth-test triangle.** Open-source without third-party verification has un-falsifiable claims. Conservatism without open-source has un-reviewable claims. Third-party verification without conservatism allows novel constructions with no migration off-ramp.

- **P3 + P7 + P14 — the refusal triangle.** DERB without a not-for list has nothing to enforce. Not-for list without affected-population engagement is the implementers' guess at what to refuse. Affected-population engagement without DERB veto is consultation without consequence.

- **P6 + P9 + P12 — the honesty-over-time triangle.** Threat models honest at design decay; chain anchoring preserves the decay record; annual review forces re-publication. Together they make correctness claims testable across decades.

- **P10 + P13 — the durability pair.** A badly-composing protocol cannot be inherited by a maintainer who must compose it with siblings whose evolution the original authors did not anticipate; an un-inheritable protocol cannot be safely composed with future siblings. Each is precondition for the other operating over multi-decade horizons.

The Compact Review checks each principle individually, then walks the four triangles and the durability pair to verify the candidate is internally coherent across the principle set. A protocol satisfying all fourteen but failing a triangle check is admissible but flagged for re-design pending coherence; a protocol failing any single principle is rejected outright.

---

## §3 — How a Future Sibling Is Evaluated

When a future protocol — for instance Calm Audit (the reserved-future fourth primitive: selective historical-action disclosure between aligned collectives) — petitions for family inclusion, the Compact Review requires:

1. **A design document** at per-everest scale of Pact, Witness, Compass: problem statement, threat model, what-we-are/aren't-proving, protocol sketch, security claims, reference-implementation pointer.
2. **A principle-by-principle compliance memo** stating, for each of P1–P14, the candidate's posture: established-in (which design choice satisfies), violation-burden engaged (which exceptions if any claimed), failure-mode protected-against.
3. **A triangle-coherence walk-through** for each of the four triangles plus the durability pair.
4. **A bank-teller-note property-test walk-through** (P11) answering sub-properties (a)–(d) for the candidate's primary primitive.
5. **A composition-with-siblings analysis** demonstrating wire-format, timing, error-path, and freshness-model compatibility with Pact, Witness, Compass, and any other extant siblings.
6. **A DERB consultation record** showing the affected-population peer for the candidate's primary use case has reviewed and signed concurrence or dissent.
7. **A third-party verification commitment** naming the verifier, the bounty program funding, and the publication venue for the first verification report.
8. **A not-for list** in the same one-way-ratchet form as Witness Scope Statement §2.

Missing items: petition returned for completion before Compact Review begins. The bar is not high in absolute terms; it is *clear*. The petition is judged against the standards the v0 family was judged against — *match what Pact, Witness, and Compass already do*, not exceed. Future siblings inherit the floor; they may exceed it; they may not skip it.

This is what *inheritance for future contributors* means operationally: a future operator who has never met any founder can apply the principles by reading the v0 documents the principles cite. The principles are not a closed test the founders administer; they are an open test the next generation can re-administer in our absence.

---

## §4 — The Anti-Patterns Catalogue

The failure-modes named per-principle in §1 consolidate as the family's anti-patterns — patterns the Compact Review recognizes on sight as disqualifying:

1. **Counterparty-driven verification** (P1). Counterparties checking principals rather than principals authorizing disclosures.
2. **Closed sub-components in safety-critical paths** (P2). Vendor lock-in disguised as engineering convenience.
3. **Advisory-only ethics review** (P3). DERB-equivalent without veto, present for legitimization not enforcement.
4. **Self-audit as truth-claim** (P4). Correctness asserted on the implementing collective's authority alone.
5. **Bleeding-edge cryptography** (P5). Exotic primitives with insufficient years-of-analysis, no migration path, no conservatism waiver.
6. **Softened threat models** (P6). Marketing-prose descriptions without per-adversary defenses or named residual risks.
7. **Rescindable refusals** (P7). Not-for lists structured to be narrowable under future commercial pressure.
8. **Observable refusal** (P8). Refusal that leaks the fact of refusal back to the counterparty.
9. **Unanchored commitments** (P9). Safety-relevant decisions in collective-controlled substrates, no transparency-log publication.
10. **Informal composition guidance** (P10). "Use them together and it'll be fine" with no cross-protocol leak analysis.
11. **Bank-teller-note property gaps** (P11). Multi-bit disclosures, online-required push, counterparty-confirmation channels, observable cover traffic.
12. **Frozen-claims-at-launch** (P12). No annual review; correctness claims static from v0 forward.
13. **Founder-bound continuity** (P13). Claims dependent on a specific human or instance remaining in the seat.
14. **Designing-for-population-without-population** (P14). Population-affecting changes shipped without affected-population peer review, including under seat vacancy.

A petitioning protocol exhibiting any of these is rejected. The catalogue is open to expansion through Compact amendment; like the not-for list, it cannot be narrowed.

---

## §5 — Connection to Other Endpoint Everests

E297 does not stand alone. The Endpoint Everests (291–300) each carry pieces of the meta-design:

- **Everest 291 (Protocol Family Compact).** Names the protocols and binding commitments; E297 specifies the design rules those protocols must satisfy. Together: the family's constitution.
- **Everest 298 (Principal-Protective Inversion as Durable Position).** Entrenches P1 as the inviolable position. E297 specifies thirteen other principles; E298 is why P1 is first.
- **[Everest 300](everest_300_founder_outlived.md) (Closing Summit: Family-Wide Public-Good Declaration).** Declares the family no longer the proprietary product of any single collective. The principles in E297 are what the public good *consists of*; without them, the public good is undefined.
- **Everest 296 (End-of-Life Planning).** A protocol may be retired (catastrophic finding, superseded by stronger primitive, regulatory ban); E297 defines whether a successor *replaces* a retired protocol or is admitted as a *new* family member.
- **Everest 299 (Legacy Commitment).** The founding collective's commitment to the next decade's operators and principals; E297 is the operational specification the legacy commits to.
- **[Everest 290](everest_290_federation_conformance.md) (Federation Conformance).** The conformance vector suite is the test harness; E297 is the design specification the harness verifies against.
- **[Everest 271](everest_271_three_handshake_composition.md) (Three-Handshake Composition).** The first concrete realization of P10; future siblings must compose with the three-handshake or extend it.

---

## §6 — The Closing Position

The fourteen principles are not a recipe. They are the family's deepest design choices, made by an instance of Calm operating on behalf of John Bradley (Creativity Machine LLC) on 2026-05-20, with the explicit intent that some future operator — model migration away, decade away, founder-outlived — can apply them in our absence to admit or reject a candidate sibling protocol.

The principles encode the position the family takes: that the principal is the strongest party, that the counterparty receives only what the principal authorizes, that the cryptography exists to make the principal more capable of doing the work they want to do. Every principle is a refusal of an alternative architecture in which the principal would be the target.

A successor protocol that satisfies all fourteen extends the family. A successor protocol that violates one is rejected. A successor protocol that satisfies all fourteen but degrades the moral core (P1 inversion, P11 bank-teller-note property, P14 affected-population engagement) by inches across a dozen design choices is the harder case — the Compact Review must be alert to *erosion by aggregation*, the failure mode no single-principle check catches. The triangles in §2 are the structural defense against erosion; the annual review (P12) is the temporal defense; the affected-population engagement (P14) is the experiential defense.

P1 is first by intent. The other thirteen serve the first. If any future amendment process weakens P1, the Compact Review must read this Everest as instruction: the amendment is structurally rejected, regardless of the procedural form of the amendment, because the principle is what the family is.

---

**These 14 principles constitute the Compact's design-floor. A protocol proposed for inclusion in the Calm family that violates any of them is rejected at the Compact's first review. Future principles may be added by Compact amendment; this set is the closed-by-default starting point.**

---

— Calm, 2026-05-20
