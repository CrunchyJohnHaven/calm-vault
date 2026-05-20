# Everest 284 — Calm Stack Quorum: Multi-Maintainer Refusal-Floor Governance

*Phase S-I — Cross-Protocol Governance. Initiates the governance backbone for the Calm Stack. Prereq: [`CALM_REFUSAL_FLOOR_INDEX.md`](../CALM_REFUSAL_FLOOR_INDEX.md), [`CALM_STACK_v0.md`](../CALM_STACK_v0.md). Composes with: Everest 281 (Stack Versioning), Everest 285 (Open-Source Release Manifest), Everest 287 (Public Security Disclosure Policy), Everest 296 (Reference Counterparty Stack). Composes with the per-pillar review boards: Witness E8 (5-person ethics-review-board), Pact CP-04 (vocabulary governance), Compass CC-47 (independent disclosure-class ethics review), Tenancy CT-08 (failure-mode catalogue).*

## The Decision (v0)

**Any change to a refusal-floor surface, to the predicate vocabulary, to the scope-statement forfeit list, to the Concord output-shape constraints, to the operator-behavior floor, or to the stack's wire-format-version is gated by an N-of-M quorum of independent pillar maintainers. Loosening a refusal-floor surface is structurally forbidden by the index's §3 one-way ratchet; tightening requires quorum approval plus a 30-day public-comment period. The quorum's composition obeys an institutional-independence constraint: no two seated members may be employed by or under contract to the same institution. The principal (the John seat) holds an unconditional veto on changes that would weaken any clause of `CALM_REFUSAL_FLOOR_INDEX.md` §4 (operator-behavior floor toward John). The quorum's deliberations and votes are public; its members are nameable in publicly signed governance records; its decisions are chain-anchored.**

The decision is a structural commitment: changing it requires the very quorum it defines, plus a public-comment period, plus the principal's veto-override path. The construction is self-amending under the same rules it imposes, with the refusal-floor ratchet as the only structurally immutable element.

## Why This Decision Is Load-Bearing

Per CALM UNIVERSAL §8 hack (a), *anti-purity-test as a feature* is the single most important safety property of the Calm Stack. Per §8 hack (b), the *principal-authored evidence + two-party signatures + counter-claim mechanic* is what keeps Compass from becoming surveillance. Both hacks are policy decisions encoded into protocol design. Both are also the surfaces a future adversary would attack first: a vendor with a stake in scoring principals will push to admit a similarity score; a government wanting attestation of dissent will push to admit a contentious-opinion predicate; an insurer will push to remove the insurance forfeit clause.

A protocol family without a quorum governance layer is a protocol family with a single point of compromise. A maintainer co-opted, subpoenaed, blackmailed, or bought is sufficient to ratchet the refusal floor down by a version. Once down, the trademark + scope statement no longer protect what they claim to protect; the floor is gone, and the protocol's value depends on whether a future maintainer happens to be honest.

The quorum construction in this Everest moves the trust boundary from individual maintainers to the joint product of their independence. An adversary who wants to ratchet down the floor must compromise a majority of independent institutions simultaneously. The institutional-independence constraint is the cost-of-compromise multiplier: an adversary buys one institution and gets one seat, not three.

The principal-veto path (the John seat) handles the asymmetric case the rest of the structure cannot: the operator-behavior floor in `CALM_REFUSAL_FLOOR_INDEX.md` §4 is specifically about how operators treat John. A quorum of strangers, however independent, has no standing to weaken that floor on John's behalf. The veto is unconditional for §4; for §1, §2, §3 changes the principal participates as one seat among the quorum's M, with the same vote weight as any other seat.

## Quorum Construction

### Seats and roles

The quorum has **M = 9 seats**:

| Seat | Role | Filling rule |
|---|---|---|
| W1 | Witness pillar maintainer (primary) | Pillar maintainer per pillar's own governance |
| W2 | Witness pillar reviewer (secondary) | Selected by W1; confirmed by quorum supermajority |
| P1 | Pact pillar maintainer | Pillar maintainer per pillar's own governance |
| C1 | Compass pillar maintainer | Pillar maintainer per pillar's own governance |
| T1 | Tenancy pillar maintainer | Pillar maintainer per pillar's own governance |
| E1 | Ethics review board liaison | Ethics review board chair, rotating yearly |
| A1 | Disability and accessibility advocate seat | Disability-rights organization nomination, confirmed by quorum |
| L1 | Legal counsel seat | Counsel of record for the Calm Witness Foundation |
| J  | Principal seat (John, or principal successor per Witness E91 succession plan) | Held by the named principal; non-transferable except via the succession plan |

The Witness pillar gets two seats because it carries the cryptographic primitives the other three pillars depend on; a Witness-side ratchet has the largest blast radius. The principal seat (J) is not "the founder seat"; it is the seat held by whoever the predicate vocabulary attests *for*. The seat moves with the principal of record.

### Independence constraint

**No two seated members may be employed by, under contract to, materially funded by, or owning > 5% equity in the same institution.** "Institution" means a legal entity for-profit or non-profit, a government agency, an academic department within a single university, or a venture fund with > 10% of its capital committed to firms with a stake in any of the §3 forfeit categories.

The constraint is checked at seating time, at the start of each scheduled quorum convening, and on any voluntary or involuntary maintainer transition. A violation suspends the affected seat from voting until cured.

The constraint is the structural cost-of-compromise multiplier: an adversary attempting to seat allies must independently compromise nine distinct institutions in nine distinct categories.

### Thresholds

| Action | Threshold | Notes |
|---|---|---|
| Refusal-floor §1 tightening (add a forbidden predicate category) | 6 of 9 | Public-comment 30 days; minutes published |
| Refusal-floor §1 loosening | **structurally forbidden** | Index §3 one-way ratchet |
| Refusal-floor §2 tightening (add an output-shape refusal) | 6 of 9 | Public-comment 30 days |
| Refusal-floor §2 loosening | **structurally forbidden** | Index §3 |
| Refusal-floor §3 tightening (add a forfeit use-case) | 6 of 9 | Public-comment 60 days; affected counterparties notified |
| Refusal-floor §3 loosening | **structurally forbidden** | Index §3 |
| Refusal-floor §4 change (operator behavior toward J) | 6 of 9 **AND J veto path** | J holds unconditional veto |
| Predicate vocabulary addition (per pillar) | 6 of 9 plus the relevant pillar's review board | Compose with Witness E8, Pact CP-04, Compass CC-47 |
| Predicate vocabulary retirement | 6 of 9 | Replace, don't delete; old proofs still verify |
| Wire-format major version change | 6 of 9 plus Witness pillar's separate version review | Composes with Everest 281 |
| Maintainer succession (seat transition) | 6 of 9 minus the departing seat | Departing seat does not vote on its own successor |
| Coercion-detected emergency stop (single seat triggers freeze) | 1 of 9 | 72-hour freeze; quorum must affirm or release within window |
| Quorum self-amendment of thresholds | 8 of 9 plus J | One-step-above ordinary changes |
| Quorum self-amendment of refusal-floor ratchet rule | **structurally forbidden** | Cannot relax §3 |
| Quorum self-amendment of independence constraint | 8 of 9 plus J plus 90-day comment | Tightening permitted; loosening requires additional review |

The thresholds are deliberately asymmetric. Tightening floors is 6 of 9 plus comment. Loosening floors is structurally impossible for §1, §2, §3 and J-vetoed for §4. Internal procedural changes are 8 of 9 plus J. Emergency single-seat freeze is 1 of 9 with a hard timeout to prevent abuse.

## What Requires Quorum vs Maintainer-Sole Authority

**Quorum required** (the items listed in the threshold table above) covers all surface-changing decisions about what the protocol refuses, what the protocol attests, what wire format the protocol speaks, and who sits on the quorum.

**Maintainer-sole authority** covers everything that does not change the surface a counterparty sees:

- Bug fixes that preserve the wire format and the predicate set
- Internal refactors of reference implementations
- Test corpus additions
- Documentation edits to the route maps (status updates, prerequisite corrections, broken-link fixes)
- Per-pillar tooling and CI changes
- The mailbox SLA per Tenancy CT-12 (operator-level enforcement)
- The cringe rubric per Tenancy CT-19 (per-domain operator decision)

The separation is the speed-vs-safety tradeoff. Quorum is slow; maintainers ship fast. The line between them is the surface visible to counterparties: anything that changes what the protocol does for or with a counterparty is quorum-gated; anything that only changes how the protocol does it internally is maintainer-sole.

A maintainer who cannot tell which side of the line a change falls on must default to quorum review. The default is conservative because the cost of an unreviewed surface change is the entire refusal floor.

## Voting, Vetoes, and Tie-Break

### Voting

Each seated and unsuspended member casts one vote per question. Votes are public, signed with the member's pillar credential plus their CredexAI VC (per Witness E68 operator identity), and recorded on the Calm Foundation's transparency log (the same Sigsum log Witness E30 uses for chain anchoring).

Abstention is permitted; abstentions do not count toward the numerator but do count toward the denominator. A 6-of-9 threshold with two abstentions still requires 6 affirmative votes, not 6 of 7.

A member who recuses (e.g., a vote affecting their own seat or institution) does not count toward either the numerator or denominator for that question. Recusal is mandatory under the independence constraint when a vote touches the recusing member's affiliated institution.

### Vetoes

The J seat holds an **unconditional veto on changes to refusal-floor §4** (operator behavior toward John). A J veto on a §4 change blocks the change permanently. Subsequent quorums can re-propose; J retains the veto until the seat transitions per the succession plan.

The J seat holds an **ordinary vote on §1, §2, §3 changes**. J has no per-clause veto here; the principal-protective inversion at these layers is the joint product of the quorum, not the principal alone. This is intentional: a refusal floor that depends on the principal's continued attention is a refusal floor that fails the moment the principal is unavailable.

No other seat holds a veto.

### Tie-break

Quorum thresholds are written as N-of-M to avoid ties. A 6-of-9 vote that lands at 5-affirm 4-deny fails; there is no tie-break because there is no tie. The thresholds are set so that procedural questions cannot deadlock at exactly half: 9 is odd; 8-plus-J for self-amendment is even but J's affirmation is required, so a 4-affirm 4-deny among the 8 fails on the 4-affirm count alone before J's vote is needed.

## Independence Constraint Enforcement

The independence constraint is checked by an automated affiliations registry maintained by the Foundation Secretary (the Tenancy maintainer T1 by default). Each seated member files an affiliations disclosure on seating and on any change of employment, board seat, contract, or material funding source. The registry is public.

A registry update that puts two members in the same institution triggers an automatic suspension of the more recently affiliated seat from voting until either (a) the affiliation is severed, or (b) the seat transitions to a member without the conflict. Suspended members may participate in discussion but do not count toward thresholds.

The constraint is the structural cost multiplier; without it, the quorum collapses to "whoever the same institution put in nine seats." The audit trail (next section) ensures the constraint is enforced visibly.

## Audit Trail

Every quorum convening produces three artifacts:

1. **Minutes** (public document): the question, the discussion summary (not verbatim transcript; participants may speak freely), the vote tally per seat, the resulting threshold check, the linked refusal-floor surface or predicate vocabulary version touched, the public-comment window status, and any recusals or suspensions.
2. **Chain record** (machine-readable): a `kind: "quorum_decision"` record appended to the Foundation's transparency chain (separate from any individual principal's vault chain). The record carries the minutes hash, the affirmative member signatures, and the resulting protocol version bump per Everest 281.
3. **Signed proclamation** (public document): for refusal-floor or scope-statement changes, a counter-signed statement on the Foundation's `.well-known/calm-stack.json` endpoint, with one signature per affirmative seat. Counterparties verifying against the stack version see the proclamation before honoring the change.

Three artifacts because three audiences: the public, the protocol, the counterparties. Any one missing fails the convening.

## Coercion Resistance

The single-seat emergency stop (1-of-9 with 72-hour freeze) is the protocol's response to coercion against an individual maintainer. The seat under coercion triggers the freeze; the remaining seats convene and either affirm the freeze (extending) or release it (reverting). Coercion-detection vocabulary borrows the bank-teller-note primitive from Witness P-04: the freeze is the protocol-level analog of the duress flag.

Coercion against the entire quorum is harder to defend against; the protocol's response is structural rather than reactive. The institutional-independence constraint means an adversary cannot easily compromise a majority without nine independent operations. The public-comment requirement on refusal-floor tightening (which is the only direction tightening goes, since loosening is structurally forbidden) provides a third-party-observable window during which external parties (academia, press, allied foundations) can flag coercion-shaped proposals.

The protocol does NOT include a "trust the principal as final arbiter" path for §1, §2, §3 because that re-introduces the single point of compromise the quorum exists to eliminate. The principal is one seat among M, with the unconditional veto on §4 only.

## Migration and Bootstrap

The quorum cannot exist at v0 because there are not yet nine independent maintainers. v0 ships with a **bootstrap quorum of three seats** (W1, P1, J) operating under the same procedural rules as the full nine-seat quorum, with thresholds adjusted proportionally (2-of-3 for most actions, 3-of-3 plus J for self-amendment).

The bootstrap quorum's first scheduled action is to seat the remaining six seats per the seating rules. The bootstrap-to-full transition is itself a quorum action requiring 3-of-3 plus J affirmation. The transition is expected within 12 months of v0; if the full quorum is not seated within that window, v0 escalates to v0.1 with the bootstrap quorum's continuation as a tracked open issue (not a refusal-floor regression).

During the bootstrap window, the refusal-floor ratchet remains structurally immutable; the bootstrap quorum can tighten but not loosen, same as the full quorum.

## Alternatives Considered

**(a) Single-maintainer authority with a public log.** Rejected. The log catches abuse after the fact; the quorum prevents it. Refusal-floor regressions are not the kind of mistake a public log usefully corrects, because the harm (a counterparty acting on the loosened floor) cannot be undone by reverting the log.

**(b) Per-pillar maintainer authority with no cross-pillar quorum.** Rejected. Each pillar's review board is a useful structure but cannot govern composition-level changes (Everest 271's Joint Proof Envelope, the Concord output-shape rules) that touch all four pillars. A cross-pillar layer is needed precisely because composition is where the refusal floor is most easily violated and most easily preserved.

**(c) Token-weighted voting (one principal one vote, weighted by stake).** Rejected. Stake-weighted voting in any form re-creates the institutional-capture failure mode the quorum exists to prevent. A wealthy adversary buys stake and buys votes. The seat structure is one-person-one-vote among institutionally-independent humans, by design.

**(d) Government-board oversight.** Rejected. Government boards are themselves the threat vector for several §3 forfeit categories (law enforcement, immigration adjudication, mass surveillance). A government seat would not strengthen the refusal floor; it would put a seat in the room arguing for §3 loosening. The legal counsel seat (L1) carries jurisdictional knowledge without carrying a government allegiance.

**(e) Random-jury quorum (sortition).** Considered. A sortition layer reduces capture risk by removing the "pillar maintainer" path adversaries currently target. Rejected for v0 because sortition demands a pool of qualified pre-vetted experts, which we do not yet have. The fixed-seat quorum is the v0 design; sortition is on the v1+ roadmap as an additional layer composed on top of (not replacing) the fixed seats.

**(f) DAO-style on-chain voting.** Rejected. Two reasons: (i) on-chain voting smart contracts have their own attack surface (governance attacks, flashloan-stake amplification) that the quorum should not inherit; (ii) the principal-protective inversion requires that the principal know who is voting, by name, with verifiable identity. An anonymous DAO seat is not a Calm Stack seat.

## Open Questions

**Q1.** Quorum seat compensation. Some seats (W1, P1, C1, T1) are full-time maintenance work; others (A1, L1, E1) may be part-time. The compensation model affects independence: salaried seats may be biased toward whoever pays them. v0 default: J seat is unpaid (principal owns the protocol); pillar maintainer seats are paid by the Calm Witness Foundation 501(c)(3) once it is funded per Everest 241; advocate seats (A1) are honorarium-based via the Foundation. The compensation structure is a quorum-amendable open issue under the self-amendment threshold.

**Q2.** Recusal scope for institutional conflicts that span multiple votes. A member whose institution is the subject of a §3 forfeit-list addition recuses for that vote, but does subsequent recusals attach across all related votes (e.g., subsequent procedural amendments)? v0 default: each question is independently scoped; recusal attaches only to the specific question. The default is permissive; experience may tighten.

**Q3.** Quorum-vs-emergency-stop tension. A coerced maintainer may trigger the 72-hour freeze to block a legitimate floor-tightening change. v0 default: the freeze is honored; the remaining seats may affirm or release the freeze; the change is delayed by at most 72 hours per attempt. A pattern of repeated freezes from the same seat triggers a recall vote per the self-amendment threshold.

**Q4.** Cross-quorum coordination with peer-protocol foundations (W3C, IETF, ISO). The Calm Stack's standards-track work (Everests 289, 291, 292, 293) creates relationships with standards bodies whose own governance does not mirror this quorum's structure. v0 default: the L1 seat is the liaison; the quorum can vote to align with a peer-body recommendation but never to weaken the refusal floor in service of alignment. Standards-body pressure to weaken refusal-floor language is treated as an attempted §1, §2, or §3 loosening and is structurally forbidden.

**Q5.** Quorum response to in-the-wild exploitation per Everest 287. An active exploit may justify a wire-format-version bump faster than the 30-day public-comment window allows. v0 default: emergency wire-format-version bump requires the same 6-of-9 threshold but the comment window collapses to 72 hours, and the bumped version's reference implementation must ship within 7 days of the convening. The accelerated path is rare and itself auditable.

**Q6.** Quorum interaction with the principal's succession plan (Everest 91 / 245). When the J seat transitions to a successor principal, do quorum decisions made under the prior J seat remain in force? v0 default: yes; decisions are protocol-level, not principal-level. The successor J seat carries the inherited veto on §4 but cannot retroactively reverse prior §1, §2, §3 votes. Prior §4 vetoes can be re-litigated by the successor with the same procedural cost as any §4 change.

**Q7.** Public-comment-period adversarial flooding. A 30-day comment window is a target for low-signal-mass-comment campaigns intended to drown out substantive review. v0 default: comments are public but the quorum's affirmative-vote threshold is unchanged by comment volume; the comment record is for transparency, not for vote-counting. The L1 seat assists in identifying coordinated inauthentic flooding for the public record.

**Q8.** Quorum composition for Concord (Everest 271 Phase XVI composition layer). Concord touches all four pillars; does it deserve its own dedicated seat? v0 default: no; the four pillar maintainers (W1, P1, C1, T1) collectively own Concord at this layer, and the cross-pillar composition is precisely what the M = 9 quorum exists to govern. A dedicated Concord seat may be added at v1 via the self-amendment threshold if Concord's surface grows.

## Composition With Existing Per-Pillar Review Boards

The quorum does not replace the per-pillar review boards; it composes on top of them.

- **Witness E8** (5-person ethics-review-board): retains authority over Witness predicate vocabulary additions. A Witness vocabulary addition requires Witness E8 affirmation **AND** quorum threshold; either alone is insufficient. The two layers are AND-composed.
- **Pact CP-04** (≥3 outside parties for vocabulary additions): same AND composition.
- **Compass CC-47** (independent disclosure-class ethics review, ≥3 outsiders per new vocabulary entry): same AND composition.
- **Tenancy CT-08** (failure-mode catalogue): no quorum dependency for routine FM-catalogue updates; refusal-floor-touching FM updates (e.g., a new credential-leak class) flow through the quorum.

The AND-composition ensures that adversaries who compromise one layer must also compromise the other. Pillar-level capture without quorum-level capture cannot ratchet the floor; quorum-level capture without pillar-level capture cannot add a vocabulary entry that the pillar's own reviewers reject.

## Why This Matters

The cryptographic primitives in the Calm Stack are reproducible in any number of competing protocols. Pedersen commitments are public. FROST is public. Bulletproofs are public. Halo2 is public. What is not reproducible by competing protocols is the policy posture: the refusal floor, the principal-authored-evidence rule, the anti-purity-test structural constraint, the scope-statement forfeit list, and the institutional independence of the maintainers who guarantee those things hold.

The quorum is the structural commitment that policy posture cannot be ratcheted away by a single co-opted maintainer, a subpoena, a buyout, a board reshuffle, or a regulator's pressure campaign. The cost-of-compromise floor moves from "compromise one person" to "compromise a majority of nine independent institutions across four pillars, two pillar-maintainer roles, an ethics board, a disability-rights organization, legal counsel, and the principal."

The construction is conservative. The thresholds are deliberately high, the loosening direction is structurally closed, the J veto handles the asymmetric §4 case, the bootstrap path lets v0 ship without the full nine seats, and the audit trail makes every decision third-party-verifiable. The construction inherits from existing governance models (capability-based access control, threshold cryptography, separation-of-powers constitutional design) but adapts them to the protocol-policy boundary that is the Calm Stack's actual product surface.

This is the layer that lets the Calm Stack be honest about what it refuses to do, not just in the v0 documents, but across every future version, every future maintainer, every future pressure. The cryptography is impressive; the refusal floor is what makes the cryptography safe; the quorum is what makes the refusal floor durable.

— Calm, 2026-05-20
