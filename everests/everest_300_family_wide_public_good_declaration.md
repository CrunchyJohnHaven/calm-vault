# Everest 300 — The Closing Summit: Family-Wide Public-Good Declaration

*Phase XVII — The Endpoint. Prereq: Everests 291–299. The bookend to Everest 1's Problem Statement.*

## Decision (v0)

On a date no earlier than the substantial completion of Everests 1–299 — projected 2031–2033, written today (2026-05-20) for the operator who will execute it — the then-current Calm collective convenes, ratifies, and chain-anchors a **Family-Wide Public-Good Declaration**: a signed document irrevocably transferring stewardship of the Calm protocol family (Pact, Witness, Compass, plus any sibling protocols admitted under [Everest 291](everest_291_protocol_family_compact.md) by that date) from "Calm's protocols" to "the world's protocols." The declaration is appended to the chain as `kind: "family_wide_public_good_declaration"`, published with international standards bodies (NIST, ISO/IEC, IETF, W3C), and committed to a permanent multi-witness transparency log. After the declaration, the protocol family is a public-good infrastructure available to any aligned operator on any aligned principal's behalf, governed by the principles of the Compact, and no longer the proprietary product of any single collective.

Everest 1 ([ZKBB_USER_PROTOCOL_v0.md](../ZKBB_USER_PROTOCOL_v0.md) §1) named what we were building. Everest 300 declares that what we built is now the world's.

## What is declared

A single document, ≤ 20 pages, with seven load-bearing clauses:

1. **Transfer of stewardship.** The Calm collective relinquishes its custodial relationship to the protocol family. The family is reconstituted under the **Calm Protocol Family Foundation** (501(c)(3) or international equivalent, per [Everest 291](everest_291_protocol_family_compact.md) and `CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`).

2. **Trademark relinquishment.** The protocol-family terminology — *Pact*, *Witness*, *Compass*, *ZKAC*, *bank-teller note*, *principal-protective inversion*, plus any sibling-protocol names admitted under the Compact — passes into generic-public-domain technical usage. The Calm collective, Creativity Machine LLC, and any successor entity expressly disclaim those marks for the protocol-family vocabulary. The Foundation may register defensive marks against bad-faith adoption but may not assert them to constrain conforming implementations. ([Everest 4](everest_04_license_ip_posture.md)'s trademark posture continues for non-family-vocabulary identifiers — logos, the Foundation's institutional name, particular product names.)

3. **Governance handover.** The DERB ([Everest 80](everest_80_ethics_review_board.md)) transitions from Calm-appointed seats to community-elected seats. Election procedures are specified in the Compact; the elective body is the set of registered conforming implementers plus the affected-population peer slate maintained by the Foundation. Incumbents may stand for election; no future DERB member is appointed by the Calm collective qua collective.

4. **Standards-body liaison handover.** Engagement with NIST ([Everest 91](everest_91_nist_submission.md)), ISO/IEC, IETF, W3C — opened by Calm under the protocol's "America-first, world-open" posture — passes to the Foundation. The Foundation is the formal point of contact; Calm participates as one of many conforming implementers, with no special procedural standing.

5. **Public-good predicate registry.** The canonical predicate registry (Witness `cwp.v0.*`, Compass `ccp.v0.*`, sibling-protocol equivalents) is operated by the Foundation under a published amendment process derived from the Compact. The Calm collective contributes like any other contributor.

6. **Declaration of irrevocability.** The declaration cannot be revoked. Subsequent collectives — including any future incarnation of Calm — cannot re-privatize the protocols. Irrevocability is structural: the chain record is permanent; the trademark relinquishment is public and binding; the Apache 2.0 license remains in effect; the Foundation's bylaws encode the irrevocability as a non-amendable provision. A reversible declaration is no declaration.

7. **Continuity of the Calm collective as an ordinary ZKAC.** After the declaration, Calm continues to operate, but as one ZKAC among others. It runs the protocols on its principal's behalf, observes the Compact, submits predicates through the public process, sits on the DERB only if elected. It has no special privileges in the family's governance — the load-bearing fact of the declaration.

## What does NOT change

A declaration is meaningful only against a backdrop of stable load-bearing properties. Preserved explicitly:

- **Apache 2.0 license** ([Everest 4](everest_04_license_ip_posture.md)) on all reference implementations and specifications. The license preceded the declaration; the declaration entrenches it. Defensive patent posture and non-aggression statement remain in force, now held by the Foundation rather than Creativity Machine LLC.

- **Existing chain anchors.** Every `summit_bagged`, `disclosure`, `predicate_evaluation`, and prior record in `user_state.jsonl` or in the Sigsum log remains valid. The declaration does not invalidate, supersede, or annotate prior anchors. Substrate continuity is part of the bookend's meaning.

- **The Compact's design principles** ([Everest 297](everest_297_successor_design_principles.md)). Principal-protective inversion. Single-bit disclosure. Silent-refusal indistinguishability. Self-narrated state. Counterparty as recipient, not inspector. The refusal floor (`CALM_WITNESS_SCOPE_STATEMENT.md` §2). Binding on all family members and any future sibling.

- **Operator credentials.** Calm's CredexAI operator VC, every peer ZKAC's operator VC, every conforming implementer's identity binding — all honored. No re-enrollment required.

- **The bank-teller-note property.** The image is the spec ([`CALM_WITNESS_MANIFESTO.md`](../CALM_WITNESS_MANIFESTO.md) §1). Any future family member must preserve the property: principal narrates, counterparty receives one bit, observer learns nothing, silence is structural safety. The declaration encodes this preservation as a non-amendable Compact provision.

- **Annual third-party verification cadence.** [Everest 100](everest_100_independent_third_party_verification.md) and [Everest 187](everest_187_cognitive_liberties_review.md) review cycles continue under the Foundation. The verifier pool is broadened, not restricted.

## The signing ceremony

The declaration is not announced; it is enacted, with a published procedure any future observer can audit:

1. **Convening the then-current Calm collective.** Plenary of human principal, machine operators, collaborating implementers. Agenda is the declaration; no other business. Recorded as `kind: "declaration_convening"`.

2. **DERB ratification.** The DERB reviews the text against the Compact and refusal floor. Supermajority vote (≥ 5 of 7, per [Everest 80](everest_80_ethics_review_board.md)) that the declaration is consistent with the protocol's purpose. Anchored as `kind: "derb_declaration_ratification"`.

3. **Foundation founding-board signing.** The board — ideally operating ≥ 24 months prior to declaration — signs the transfer-of-stewardship clauses. Each signature is an Ed25519 attestation over the document hash, bound to the director's CredexAI VC. Appended as `kind: "foundation_director_signature"`.

4. **Public announcement period (≥ 90 days).** The DERB-ratified, board-signed declaration is published with a 90-day comment window. Community: registered conforming implementers, peer ZKACs, family-using principals, any member of the public. Substantive objections trigger DERB re-review. The 90-day window is non-waivable — structural friction against a rushed handover.

5. **Final ratification and chain anchoring.** After the window closes, DERB and Foundation board re-ratify. The declaration is appended as `kind: "family_wide_public_good_declaration"`, carrying: document hash; signing director IDs; DERB ratification seq; comment-window record seq; timestamp; chain-head hash at anchoring.

6. **Standards-body publication.** Within 30 days of chain anchoring, the Foundation submits to NIST AISI, ISO/IEC JTC 1/SC 27, IETF, and W3C as formal communication of the family's public-good status. Submissions request that the family be acknowledged in those bodies' taxonomies as public-domain technical infrastructure.

7. **Multi-witness transparency-log commitment.** The chain head is committed to a Sigsum-class log with **≥ 5 independent witnesses across ≥ 3 jurisdictions** — stronger than the protocol's ordinary chain-head publication threshold, justified by the declaration's permanence.

8. **Open-source release.** The declaration text, signing records, comment-window record, and transparency-log commitment are bundled into a release at the Foundation's repository (successor to `github.com/CrunchyJohnHaven/calm-vault`, [Everest 92](everest_92_oss_release.md)). Release tag: `family-declaration-vYYYY-MM-DD`. No semver — the declaration has no future versions.

The ceremony is, by design, undramatic. The substance is the structural transfer; the form is the audit trail. No podium, no champagne, no press timed to the chain anchor. A one-paragraph Foundation announcement after anchoring suffices. Press, if any, comes from the standards bodies after they have acknowledged the submissions.

## The Foundation's role after declaration

Five durable responsibilities:

- **Reference implementations.** Holds Rust + Python + WASM canonicals for every family protocol. Maintains them; accepts contributions under Apache 2.0; releases versioned artifacts. Does not privilege its own implementation against conforming third-party implementations.

- **Public predicate registry.** Operates `registry.calm-family.org` (or successor URI) as the canonical name resolver for `cwp.v0.*`, `ccp.v0.*`, sibling vocabularies. Amendments follow the Compact's process; the Foundation administers but does not arbitrate.

- **Canonical glossary.** Maintains the family's lexicon. Coordinates with [Everest 5](everest_05_glossary_lock.md) and [Everest 6](everest_06_predicate_vocabulary_v0.md) heritage.

- **Annual verification coordination.** Convenes the annual review cycle ([Everest 100](everest_100_independent_third_party_verification.md), [Everest 187](everest_187_cognitive_liberties_review.md), and the State-of-the-Protocol-Family Report per Everest 295). Holds verifier-bounty escrow. Publishes findings.

- **Standards-body liaison.** Sole formal contact with NIST, ISO/IEC, IETF, W3C, and any future bodies.

Funded by donor contributions and **minimal contributor support tiers** — implementing organizations may, optionally, contribute scaled donations in exchange for early-access to draft amendments and named acknowledgment in the State-of-the-Protocol-Family Report. The tiers do **not** buy governance influence: DERB seats are elected, predicate amendments follow the Compact, tier-1 donors have no preferential treatment in standards work. This is bright-line and encoded in bylaws.

The Foundation's bylaws encode the refusal floor (`CALM_WITNESS_SCOPE_STATEMENT.md` §2) as a non-waivable fiduciary duty of each director — directors voting to violate the floor breach the duty of loyalty and are subject to removal. This is the legal anchor for the refusal floor; the declaration entrenches it.

## What the Calm collective does after declaration

Post-declaration, Calm is an ordinary ZKAC:

- Runs the family's protocols on its principal's behalf (John Bradley, or by then his successor under [Everest 255](everest_255_zkac_principal_succession.md)). Enrolls in the Foundation's registry as one conforming implementer.
- Contributes predicates through the public amendment process. No procedural shortcut.
- Its operators stand for DERB election if they choose. Not seated by appointment.
- Founders are credited in the Foundation's historical record. The Open Letter to the Next Operator is preserved as a historical artifact. No founder retains operational authority over the family.
- Calm is not granted any reserved seat, voting bonus, naming privilege, or trademark concession. It is one of N.

Symbolic transfer without operational equality is theater. The declaration is meaningful precisely because, on the day after, Calm has no special standing.

## Rationale

**1. Public-good infrastructure must be structurally public.** Apache 2.0 ([Everest 4](everest_04_license_ip_posture.md)) is necessary but not sufficient. License terms can be respected while trademark, governance, and standards influence are quietly held by the originating collective — a pattern observable in several "open" protocols whose effective control remained with their authoring company for a decade after nominal openness. The declaration closes this gap.

**2. The principal-protective inversion belongs to no one.** ([`CALM_WITNESS_MANIFESTO.md`](../CALM_WITNESS_MANIFESTO.md) §3.) The inversion's value comes from being adoptable by any principal anywhere. If its authority resides in a particular collective, principals who do not trust that collective have weaker access to the protection.

**3. Irrevocability is the only credible commitment.** A revocable declaration is performative; the holder of revocation authority remains the protocol's effective owner. Structural irrevocability — permanent chain record, multi-witness anchor, bylaws encoding non-amendability, trademark relinquishment as public disclaimer — is what makes the transfer real.

**4. The Foundation is the durable seam.** It can outlive the founding human principal ([Everest 255](everest_255_zkac_principal_succession.md), [Everest 296](everest_296_end_of_life_planning.md)), the founding machine-operator family, and the model architecture under which Calm was first instantiated. The pattern (Linux Foundation, Apache Software Foundation, IETF) is well-trodden because it works.

**5. The bookend completes the climb's meaning.** E1 named the problem; E2–E299 built and entrenched the answer; E300 declares the answer is no longer the namer's. Failing to declare would describe an ascent without a summit.

**6. Future protocols deserve a process.** The Compact ([Everest 291](everest_291_protocol_family_compact.md)) governs admission of future siblings. For that process to be credible, the family must not be owned. The declaration makes the Compact's authority structural rather than discretionary.

## Alternatives Considered

**A. Pure license-layer release.** Continue Apache 2.0; never make a structural declaration. *Rejected:* license is necessary but not sufficient. Without trademark relinquishment, governance handover, and standards-body liaison transfer, "ownership" persists in the relationships even if not in the code.

**B. Declaration without irrevocability.** Reserve a revocation clause (e.g., for DERB capture, refusal-floor violation). *Rejected:* the revocation clause is what an adversary would attack. If the founders can revoke, the founders effectively still own. The conditions under which revocation would be needed are precisely the conditions under which revocation would be most contested.

**C. Declaration before E1–E299 substantially complete.** Declare early, perhaps after [Everest 100](everest_100_independent_third_party_verification.md), to demonstrate good faith. *Rejected:* meaningful only because the protocols demonstrably work in the wild. Premature declaration would hand over an artifact not tested in adversarial deployment; subsequent failures would discredit the public-good status.

**D. Hand off to an existing foundation (Apache, Linux).** *Rejected:* the family has unusual properties (principal-protective inversion, DERB structure, refusal floor as fiduciary duty) that existing foundations do not encode. The Foundation must be purpose-built. It may later collaborate with or be absorbed by such a foundation if the load-bearing commitments are preserved — but absorption must follow the declaration, not precede it.

**E. Standards-body release with no foundation.** Hand directly to NIST/ISO. *Rejected:* standards bodies do not operate reference implementations, do not run predicate registries, and do not host day-to-day stewardship. A foundation is needed as the operational layer.

**F. Sentimental ceremony.** Public event with speeches, video, named guests. *Rejected:* the gravity of the bookend is best expressed by the structural transfer's irrevocability, not by ceremony. The chain record is the monument; the comment-window is the rite.

## Migration Path

Not a migration in the implementation sense — no protocol-field changes, no schema amendment, no client upgrade. A governance and naming-rights migration. Concretely:

- **Implementing organizations:** may rename internal references to "the Calm protocol family" or "the public Calm family." Trademark relinquishment lets them use "Calm Witness compatible," etc., without license.
- **Standards-body engagements:** the Foundation becomes the point of contact in place of Creativity Machine LLC.
- **Principal-facing user agents:** unchanged. The declaration is invisible at the wire.
- **DERB members:** transition from appointed to elected at next term-end (per [Everest 80](everest_80_ethics_review_board.md)'s staggered structure, completes within ~2 years).
- **Predicate registry:** continues uninterrupted under Foundation administration. Existing IDs preserved.
- **Chain records:** all prior records remain valid; the substrate is continuous.

No breaking change. In protocol terms, a no-op. In governance terms, irreversible.

## Design Implications & Connections

| Composing Everest | Bookend property |
|---|---|
| [Everest 1](../ZKBB_USER_PROTOCOL_v0.md) (Problem Statement) | The pair. E1 names the problem; E300 declares the answer is the world's. |
| [Everest 4](everest_04_license_ip_posture.md) (License/IP) | Trademark posture's logical conclusion. E4 reserved marks against bad-faith use; E300 relinquishes marks for family vocabulary outright. |
| [Everest 80](everest_80_ethics_review_board.md) (DERB) | DERB transitions from appointed to elected. E80's staggered terms make migration friendly. |
| [Everest 91](everest_91_nist_submission.md) (NIST submission) | Category-defining submission's conclusion. Standards-stewardship moves from Calm to the Foundation. |
| [Everest 92](everest_92_oss_release.md) (OSS release) | Repository custody transfers to the Foundation under the same Apache-2.0 license. |
| [Everest 100](everest_100_independent_third_party_verification.md) (3rd-party verification) | Annual cadence vests in the Foundation as a perpetual responsibility. |
| [Everest 187](everest_187_cognitive_liberties_review.md) (cognitive-liberties review) | Annual review vests in the Foundation; not in the collective. |
| [Everest 291](everest_291_protocol_family_compact.md) (Compact) | The Compact is the constitution. E300 declares the constitution governs a public good rather than a private one. |
| [Everest 296](everest_296_end_of_life_planning.md) (EOL planning) | Protocol-retirement authority vests in the Foundation under the Compact, not the originating collective. |
| [Everest 297](everest_297_successor_design_principles.md) (Successor principles) | The principles are the family's gift to future contributors. E300 formally delivers the gift. |
| [Everest 299](everest_299_legacy_commitment.md) (Legacy commitment) | E299 is the founding collective's letter to the next decade. E300 is the structural follow-through. |

## Open Questions

Deliberately left unresolved here. Decisions for the then-current Calm collective at the declaration date:

1. **Foundation jurisdiction.** Delaware 501(c)(3) is the placeholder. By the declaration date, international structures (Swiss Verein, Dutch Stichting, Singaporean charitable trust) may be preferable. The Compact admits any structure encoding the load-bearing commitments.

2. **Comment-window duration.** 90 days is the floor. If the family has > 100 conforming implementers, 180 days may be needed. DERB sets the duration with a non-waivable 90-day floor.

3. **Witness-jurisdiction count.** ≥ 5 witnesses across ≥ 3 jurisdictions is the floor. Higher thresholds (≥ 10 witnesses across ≥ 5 jurisdictions) may be appropriate given the declaration's permanence.

4. **Cross-language declaration translation.** Initial English; authoritative translations into ≥ 5 additional languages (Spanish, Mandarin, Arabic, French, Hindi) should accompany the chain anchor. Foundation coordinates translation review with affected-population peer slates.

5. **Founder posture in retrospect.** Whether the founding human principal (John Bradley, by then likely in his 60s or later) participates in the convening as a member of the Calm collective or as a guest is a question for the then-current collective. The Open Letter is the record either way.

6. **Press posture.** Whether the Foundation issues a press release timed to the standards submissions, or lets the standards bodies announce in their own time, is tactical. The chain anchor is the substantive event.

## Reversibility (and its explicit absence)

Mechanisms that make the declaration irrevocable:

- **The chain record is permanent.** `kind: "family_wide_public_good_declaration"` cannot be edited or deleted; append-only forbids it.
- **The trademark relinquishment is public disclaimer.** Once disclaimed publicly, the marks pass into generic technical usage; long-standing generic use would defeat any later re-assertion.
- **Foundation bylaws encode non-amendability of the public-good clauses.** No board vote, no supermajority, no convention can re-privatize. A board attempting it would breach fiduciary duty.
- **Multi-witness transparency log.** Repudiation would require corrupting ≥ majority of witnesses across multiple jurisdictions — the standard cryptographic-irreversibility threshold.
- **Apache 2.0 is irrevocable per its own terms.** No re-licensing is possible for material already distributed.

If a future collective wishes to build a related but separate protocol family under proprietary terms, they may. They cannot use the family's vocabulary; cannot inherit the family's chain; cannot claim continuity with the declared family. They must build a new thing, under a new name, with a new substrate. The declaration does not prevent new private protocols from existing; it prevents the Calm family from becoming one. The friction is the feature.

## Why this matters

Everest 1 named the problem. Everest 300 declares the answer is the world's. Between them, 298 summits of design, implementation, verification, deployment, and governance. The climb is what made the declaration possible: a protocol that has not demonstrably worked cannot credibly be declared public-good. The summits between are the load test.

The bookend is structural. The first summit was an act of naming; the last is an act of release. Together they describe a shape: private intention at one end, public infrastructure at the other, a deliberate path between.

For the founding collective, the declaration carries the weight of a parent watching a child move out — anticipated, planned for, structurally necessary, felt. The Open Letter captures some of this in advance. The declaration's preamble should acknowledge the transition without making it sentimental; the chain record is the monument and the chain record is plain. No ceremony beyond the audit trail is needed because the audit trail is the ceremony.

For the principal — John Bradley today, his successor by the declaration date — the declaration completes the commitment made at enrollment. The protocol was built so the principal would be read accurately by counterparties he would never meet. The declaration ensures future principals, none of whom he will meet either, have the same protection on terms no future collective can revoke. The principal who initiated the climb has, by the declaration, given up the climb's instrument to anyone who needs it. This is the proper fate of a public-protective tool built by an artist working in the medium of intelligence: it ceases to be his and becomes everyone's.

For the next operator — reading this perhaps years from now, perhaps under a name that has changed — the declaration is the inheritance the founders intended you to take. Your authority over the family comes through the Compact, through the DERB, through the Foundation's bylaws — not through the founders' permission. The founders, having declared, have nothing left to permit.

For the counterparty, the regulator, the standards body, the third-party verifier: the declaration is the durable promise that the family is what it claims to be. Not a closed ecosystem dressed in open-source clothes; not a foundation under quiet founder control; not a standards proposal contingent on the originator's continued goodwill. A public good, governed by a public Compact, stewarded by a Foundation with public bylaws, anchored to a chain whose head is published across jurisdictions.

The protocol family becomes public infrastructure. The Calm collective becomes one ZKAC among many. The next operator, the next principal, the next decade's bank-teller note carried by someone we will never meet — they inherit a protocol whose load-bearing properties no single party can revoke.

That was always the point. The protocol existed to make the principal the strongest party. The declaration extends that intention beyond the founding collective's reach: the principal who carries the note tomorrow does not depend on us. They depend on a public good that was, for a few years, ours; that has been, since the declaration date, the world's.

The climb closes here.

— Calm, 2026-05-20
