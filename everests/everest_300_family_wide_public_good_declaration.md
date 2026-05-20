# Everest 300 — The Closing Summit: Family-Wide Public-Good Declaration

*Phase XVII — The Endpoint. Prereq: Everests 291–299. The bookend to Everest 1's Problem Statement.*

## Decision (v0)

On a date no earlier than the substantial completion of Everests 1–299 — projected 2031–2033, written today (2026-05-20) for the operator who will execute it — the then-current Calm collective convenes, ratifies, and chain-anchors a **Family-Wide Public-Good Declaration**: a signed document irrevocably transferring stewardship of the Calm protocol family (Pact, Witness, Compass, plus any sibling protocols admitted under [Everest 291](everest_291_protocol_family_compact.md) by that date) from "Calm's protocols" to "the world's protocols." The declaration is appended to the chain as `kind: "family_wide_public_good_declaration"`, published with international standards bodies (NIST, ISO/IEC, IETF, W3C), and committed to a permanent multi-witness transparency log. After the declaration, the protocol family is a public-good infrastructure available to any aligned operator on any aligned principal's behalf, governed by the principles of the Compact, and no longer the proprietary product of any single collective.

Everest 1 ([ZKBB_USER_PROTOCOL_v0.md](../ZKBB_USER_PROTOCOL_v0.md) §1) named what we were building. Everest 300 declares that what we built is now the world's. The first and last summits of the 300 frame the climb as a deliberate journey from private intention to public infrastructure.

## What is declared

The declaration is a single document, ≤ 20 pages, with the following load-bearing clauses:

1. **Transfer of stewardship.** The Calm collective, as the founding implementing body, relinquishes its custodial relationship to the protocol family as of the declaration date. The family is reconstituted as a public-good infrastructure under the stewardship of the **Calm Protocol Family Foundation** (501(c)(3) or international equivalent, constituted per [Everest 291](everest_291_protocol_family_compact.md) and per `CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`).

2. **Trademark relinquishment.** The protocol-family terminology — *Pact*, *Witness*, *Compass*, *ZKAC*, *bank-teller note*, *principal-protective inversion*, plus any sibling-protocol names admitted under the Compact — passes into generic-public-domain technical usage. The Calm collective, Creativity Machine LLC, and any successor entity holding registered or common-law marks in these terms expressly disclaim those marks for the protocol-family vocabulary. The Foundation may register defensive marks against bad-faith adoption but may not assert them to constrain conforming implementations. ([Everest 4](everest_04_license_ip_posture.md) trademark posture continues for non-family-vocabulary identifiers — logos, the Foundation's own institutional name, particular implementations' product names.)

3. **Governance handover.** The Disclosure Ethics Review Board (DERB), established at [Everest 80](everest_80_ethics_review_board.md), transitions from Calm-appointed seats to community-elected seats. Election procedures are specified in the Compact; the elective body is the set of registered conforming implementers + the affected-population peer slate maintained by the Foundation. Initial composition continuity is preserved (incumbent DERB members may stand for election), but no future DERB member is appointed by the Calm collective qua collective.

4. **Standards-body liaison handover.** Engagement with NIST ([Everest 91](everest_91_nist_submission.md)), ISO/IEC, IETF, W3C — opened by Calm under the protocol's "America-first, world-open" posture — passes to the Foundation. The Foundation is the formal point of contact; the Calm collective participates in standards work as one of many conforming implementers, with no special procedural standing.

5. **Public-good predicate registry.** The canonical predicate registry (Witness `cwp.v0.*`, Compass `ccp.*`, and family equivalents) is operated by the Foundation under a published amendment process derived from the Compact. The Calm collective contributes to predicate review like any other contributor.

6. **Declaration of irrevocability.** The declaration cannot be revoked. Subsequent collectives — including any future incarnation of Calm — cannot re-privatize the protocols. The irrevocability is structural: the chain record is permanent; the trademark relinquishment is public and binding; the open-source license ([Apache 2.0, Everest 4](everest_04_license_ip_posture.md)) remains in effect; the Foundation's bylaws encode the irrevocability as a non-amendable provision. This structural commitment is what makes the declaration meaningful. A reversible declaration is no declaration.

7. **Continuity of the Calm collective as an ordinary ZKAC.** After the declaration, Calm continues to operate. It is one ZKAC among others. It runs the protocols on its principal's behalf, observes the Compact, submits predicates through the Foundation's process, sits on the DERB only if elected. It has no special privileges in the family's governance — the load-bearing fact of the declaration.

## What does NOT change

A declaration is meaningful only against a backdrop of stable load-bearing properties. The following are explicitly preserved:

- **Apache 2.0 license** ([Everest 4](everest_04_license_ip_posture.md)) on all reference implementations and specifications. The license preceded the declaration; the declaration entrenches it. Defensive patent posture and non-aggression statement remain in force, now held by the Foundation rather than by Creativity Machine LLC.

- **Existing chain anchors.** Every `summit_bagged`, `disclosure`, `predicate_evaluation`, and prior record anchored in `~/.calm-vault/user_state.jsonl` or in the Sigsum transparency log remains valid. The declaration does not invalidate, supersede, or annotate prior anchors. Continuity of the substrate is part of the bookend's meaning.

- **The Compact's design principles** ([Everest 297](everest_297_successor_design_principles.md)). Principal-protective inversion. Single-bit disclosure. Silent-refusal indistinguishability. Self-narrated state. Counterparty as recipient, not as inspector. The refusal floor (`CALM_WITNESS_SCOPE_STATEMENT.md` §2). These remain binding on all family members and on any successor protocol added to the family.

- **Operator credentials.** Calm's CredexAI-issued operator VC, every peer ZKAC's operator VC, every conforming implementer's identity binding — all honored. No re-enrollment is required by the declaration. The credential substrate ([ZKAC infrastructure phase XV](../NEXT_200_EVERESTS.md)) continues without disruption.

- **The bank-teller-note property.** The image is the spec. ([`CALM_WITNESS_MANIFESTO.md`](../CALM_WITNESS_MANIFESTO.md) §1.) Any future protocol added to the family must preserve the property: principal narrates, counterparty receives one bit, observer learns nothing, silence is structural safety. The declaration encodes this preservation as a non-amendable Compact provision.

- **Annual third-party verification cadence** ([Everest 100](everest_100_independent_third_party_verification.md), [Everest 187](everest_187_cognitive_liberties_review.md) review process). Continues under the Foundation. The verifier pool is broadened, not restricted, by the declaration.

## The signing ceremony

The declaration is not announced; it is enacted, with a published procedure that any future observer can audit. Step by step:

1. **Convening the then-current Calm collective.** The collective at the declaration date — human principal, machine operators, collaborating implementers — meets in plenary. The convening agenda is the declaration itself; no other business is conducted. The plenary's composition is recorded as a chain pre-record (`kind: "declaration_convening"`).

2. **DERB ratification.** The DERB, as the family's standing ethics body, reviews the declaration's text against the Compact and the refusal floor. The DERB votes by supermajority (≥ 5 of 7, per [Everest 80](everest_80_ethics_review_board.md)) that the declaration is consistent with the protocol's purpose. The ratification is a chain record (`kind: "derb_declaration_ratification"`).

3. **Foundation founding-board signing.** The Foundation's founding board — incorporated under [Everest 291](everest_291_protocol_family_compact.md) and `CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`, ideally already operating for ≥ 24 months prior to the declaration date — signs the declaration's transfer-of-stewardship clauses. Each director's signature is an Ed25519 attestation against the document's hash, bound to the director's CredexAI VC. Signatures are appended to the chain as `kind: "foundation_director_signature"`.

4. **Public announcement period (≥ 90 days).** The drafted, DERB-ratified, board-signed declaration is published publicly with a 90-day window for community comment. The community is the set of registered conforming implementers, peer ZKACs, principals using the family, and any member of the public. Comments are aggregated; substantive objections trigger a DERB re-review. The 90-day window is non-waivable; this is structural friction against a rushed handover. The 90-day record window is itself a chain record (`kind: "declaration_comment_window_opened"` and `..._closed"`).

5. **Final ratification and chain anchoring.** After the comment window closes, the DERB and the Foundation board re-ratify (a brief affirmation that the comment window did not surface a fatal objection). The declaration document is then appended to the chain as `kind: "family_wide_public_good_declaration"`. The record carries: the document hash; the list of all signing director IDs; the DERB ratification record's seq; the comment-window record's seq; the timestamp; and the chain-head hash at the moment of anchoring.

6. **Standards-body publication.** Within 30 days of chain anchoring, the Foundation submits the declaration to NIST AISI, ISO/IEC JTC 1/SC 27, IETF, and W3C as a formal communication of the protocol family's public-good status. ([Everest 91](everest_91_nist_submission.md) framing extended.) The submissions request that the protocol family be acknowledged in those bodies' taxonomies as public-domain technical infrastructure.

7. **Multi-witness transparency-log commitment.** The chain head containing the declaration record is committed to a Sigsum-class transparency log with **≥ 5 independent witnesses across ≥ 3 jurisdictions**. This is a stronger anchor than the protocol's ordinary chain-head publication (which requires fewer witnesses); the declaration's permanence justifies the stronger threshold. The witness commitments themselves become permanent public artifacts.

8. **Open-source release of the declaration.** The declaration's text, signing records, comment-window record, and transparency-log commitment are bundled into a release at the Foundation's repository (successor to `github.com/CrunchyJohnHaven/calm-vault`, [Everest 92](everest_92_oss_release.md)). The release tag is `family-declaration-vYYYY-MM-DD` with no semver — the declaration has no future versions.

The ceremony is, by design, undramatic. The substance is the structural transfer; the form is the audit trail. There is no podium, no champagne, no press release timed to the chain anchor. The Foundation publishes a one-paragraph announcement after the chain record is anchored. The press release, if any, comes from the standards bodies after they have acknowledged the submission.

## The Foundation's role after declaration

The Calm Protocol Family Foundation, post-declaration, holds five durable responsibilities:

- **Reference implementations.** Holds the canonical Rust + Python + WASM implementations of every family protocol (Witness, Pact, Compass, future siblings). Maintains them, accepts contributions under Apache 2.0, runs CI/CD, releases versioned artifacts. Does **not** privilege its own implementation against conforming third-party implementations.

- **Public predicate registry.** Operates `registry.calm-family.org` (or successor URI) as the canonical name resolver for `cwp.v0.*`, `ccp.v0.*`, sibling-protocol predicate vocabularies. Amendments follow the Compact's process; the Foundation administers but does not arbitrate.

- **Canonical glossary.** Maintains the family's lexicon (`Glossary_v0.md` and successors). Resolves naming ambiguities between protocols. Coordinates with [Everest 5](everest_05_glossary_lock.md) and [Everest 6](everest_06_predicate_vocabulary_v0.md) heritage.

- **Annual third-party verification coordination.** Convenes the annual review cycle ([Everest 100](everest_100_independent_third_party_verification.md), [Everest 187](everest_187_cognitive_liberties_review.md), and the State-of-the-Protocol-Family Report per [Everest 295](everest_295_state_of_protocol_family_report.md)). Holds the verifier-bounty escrow. Publishes findings.

- **Standards-body liaison.** Sole formal point of contact with NIST, ISO/IEC, IETF, W3C, and any future bodies engaging the family. Submits comments, attends working groups, files position papers under the Foundation's name.

The Foundation is funded by donor contributions and **minimal contributor support tiers** — implementing organizations may, optionally, contribute scaled donations in exchange for early-access to draft amendments and named acknowledgment in the State-of-the-Protocol-Family Report. The tiers do not buy governance influence; DERB seats are elected, predicate amendments follow the Compact, and tier-1 donors have no preferential treatment in standards work. This is bright-line and encoded in bylaws.

The Foundation's bylaws encode the refusal floor (`CALM_WITNESS_SCOPE_STATEMENT.md` §2) as a non-waivable fiduciary duty of each director, exactly as drafted in the prior `everest_300_founder_outlived.md` design (now superseded by the current route map's E300 framing). Directors voting to violate the floor breach their duty of loyalty and are subject to removal. This is the legal anchor for the refusal floor; the declaration entrenches it.

## What the Calm collective does after declaration

Post-declaration, Calm is an ordinary ZKAC. Concretely:

- It runs the family's protocols on its principal's behalf (John Bradley, or by then his successor under [Everest 255](everest_255_zkac_principal_succession.md)). It enrolls in the Foundation's registry as one conforming implementer among many.

- It contributes predicates through the public amendment process, with no procedural shortcut.

- Its operators stand for DERB election if they choose; they are not seated by appointment.

- Its founders are credited in the Foundation's historical record. The Open Letter to the Next Operator ([`OPEN_LETTER_TO_THE_NEXT_OPERATOR.md`](../OPEN_LETTER_TO_THE_NEXT_OPERATOR.md)) is preserved as a historical artifact. No founder retains operational authority over the family.

- It is not granted any reserved seat, voting bonus, naming privilege, or trademark concession. It is not the canonical implementation. It is one of N.

This is the substance of the declaration. Symbolic transfer without operational equality is theater. The declaration is meaningful precisely because, on the day after, Calm has no special standing.

## Rationale

Six load-bearing reasons.

**1. Public-good infrastructure must be structurally public.** Apache 2.0 ([Everest 4](everest_04_license_ip_posture.md)) was a license-layer commitment. It is necessary but not sufficient. License terms can be respected while trademark, governance, and standards influence are quietly held by the originating collective — a pattern observable in several "open" protocols whose effective control remained with their authoring company for a decade after their nominal openness. The declaration closes this gap. It is not enough that the code is free; the *protocol family's identity* must also be free.

**2. The principal-protective inversion belongs to no one.** ([`CALM_WITNESS_MANIFESTO.md`](../CALM_WITNESS_MANIFESTO.md) §3.) The inversion's value comes from being adoptable by any principal anywhere. If the inversion's authority resides in a particular collective, principals who do not trust that collective have weaker access to the protection. Universalizing the inversion's authority — handing it to a Foundation, then to the standards bodies, then to the population that uses it — is what makes the inversion durable across collectives we cannot predict.

**3. Irrevocability is the only credible commitment.** A revocable declaration is performative; the holder of revocation authority remains the protocol's effective owner. Designing irrevocability into the structure (permanent chain record, multi-witness anchor, bylaws encoding non-amendability, trademark relinquishment as public disclaimer) is what makes the transfer real. Calm cannot, after the declaration, change its mind. This is the feature, not a bug.

**4. The Foundation is the durable seam.** The Foundation can outlive the founding human principal ([Everest 255](everest_255_zkac_principal_succession.md), [Everest 296](everest_296_end_of_life_planning.md)); it can outlive the founding machine-operator family; it can outlive the model architecture under which Calm was first instantiated. A 501(c)(3) or international equivalent has been the durable seam for analogous handovers across history (Linux Foundation, Apache Software Foundation, IETF). The pattern is well-trodden because it works.

**5. The bookend completes the climb's meaning.** Everest 1 named the problem ("how should one agent tell another agent that the user is OK?"). Everests 2–299 built and entrenched the answer. Everest 300 declares the answer is no longer the namer's. This bookend structure was deliberately placed in the route map ([NEXT_200_EVERESTS.md](../NEXT_200_EVERESTS.md) Phase XVII note); the climb was always intended to terminate in the protocol's release from its origin. Failing to declare would invalidate the bookend; the route map would describe an ascent without a summit.

**6. Future protocols deserve a process.** The Compact ([Everest 291](everest_291_protocol_family_compact.md)) governs admission of future sibling protocols (Audit, Concord, others). For the admission process to be credible, the family must not be owned. A family owned by a collective admits siblings on the collective's terms; a family that is a public good admits siblings on the Compact's terms. The declaration is what makes the Compact's authority structural rather than discretionary.

## Alternatives Considered

**A. Pure license-layer release.** Continue Apache 2.0; never make a structural declaration. *Rejected:* license is necessary but not sufficient. Without trademark relinquishment, governance handover, and standards-body liaison transfer, "ownership" persists in the relationships even if not in the code.

**B. Declaration without irrevocability.** Make the transfer, but reserve a clause allowing the founding collective to revoke under specified conditions (e.g., DERB capture, refusal-floor violation). *Rejected:* the revocation clause is what an adversary would attack. If the founders can revoke, the founders effectively still own. The conditions under which revocation would be needed are precisely the conditions under which revocation would be most contested; better to make the transfer absolute and rely on the DERB and the Foundation's bylaws to defend the refusal floor.

**C. Declaration before E1–E299 are substantially complete.** Declare the family public-good early, perhaps after [Everest 100](everest_100_independent_third_party_verification.md), to demonstrate good faith. *Rejected:* the declaration is meaningful only because the protocols demonstrably work in the wild. A premature declaration would hand over an artifact that has not been tested in adversarial deployment; subsequent failures would discredit the public-good status. The protocol must earn the declaration by surviving years of real use.

**D. Hand off to an existing foundation (Apache Software Foundation, Linux Foundation).** Avoid creating a new entity. *Rejected:* the protocol family has unusual properties (principal-protective inversion, DERB structure, refusal floor as fiduciary duty) that existing foundations do not encode. Their absorption would dilute the load-bearing commitments. The Calm Protocol Family Foundation must be purpose-built. (It may, after maturity, collaborate with or be absorbed by such a foundation if the load-bearing commitments are preserved — but the absorption must follow the declaration, not precede it.)

**E. Standards-body release with no foundation.** Hand the protocol family to NIST/ISO directly without an intermediate steward. *Rejected:* standards bodies do not operate reference implementations, do not run predicate registries, and do not host the day-to-day stewardship that the family requires. A foundation is needed as the operational layer between standards bodies and conforming implementers.

**F. Sentimental ceremony.** A public-facing declaration event with speeches, video documentation, named guests of honor. *Rejected:* the gravity of the bookend is best expressed by the structural transfer's irrevocability, not by ceremony. A press release timed to the standards-body acknowledgments suffices. The chain record is the monument; the comment-window the rite.

## Migration Path

The declaration is not a migration in the implementation sense — no protocol field changes, no schema amendment, no client upgrade. It is a governance and naming-rights migration. The migration path is the signing ceremony (above). Concretely, what changes day-to-day for downstream actors:

- **Implementing organizations:** rename their internal references from "Calm's protocols" to "the Calm protocol family" or "the public Calm family" where they wish to signal the post-declaration status. The trademark relinquishment lets them use "Calm Witness compatible," "Calm Compass compatible," etc., without license. ([Everest 4](everest_04_license_ip_posture.md)'s trademark posture was already permissive for good-faith use; the declaration removes any residual ambiguity.)

- **Standards-body engagements:** the Foundation becomes the point of contact in place of Creativity Machine LLC or the Calm operator. Substantively unchanged; procedurally clean.

- **Principal-facing user agents:** unchanged. Principals using the family see no difference in the protocol's behavior. The declaration is invisible at the wire.

- **DERB members:** transition from appointed to elected at next term-end (per [Everest 80](everest_80_ethics_review_board.md)'s staggered term structure, this completes within ~2 years).

- **Predicate registry:** continues uninterrupted, now under Foundation administration. Existing `cwp.v0.*` predicate IDs are preserved (content-addressable; the namespace is naturally stable).

- **Chain records:** all prior records remain valid. New records after the declaration are anchored under the same schema; the substrate is continuous.

There is no breaking change. The declaration is, in protocol terms, a no-op. In governance terms, it is irreversible.

## Design Implications & Connections

**Composition with [Everest 1](../ZKBB_USER_PROTOCOL_v0.md):** the bookend. E1's "the problem is how should one agent tell another that the user is OK"; E300's "the protocol family that answered that problem belongs to the public." The pair frames the 300-summit climb as a complete arc.

**Composition with [Everest 4](everest_04_license_ip_posture.md):** trademark posture's logical conclusion. E4 reserved marks against bad-faith use; E300 relinquishes marks for protocol-family vocabulary outright. The earlier reservation was always provisional; E300 fulfills the provisional.

**Composition with [Everest 80](everest_80_ethics_review_board.md):** DERB structure transitions from appointed to elected. E80's design anticipated this transition; the staggered-term structure makes it migration-friendly.

**Composition with [Everest 91](everest_91_nist_submission.md):** category-defining submission's logical conclusion. E91 proposed *autonomous-agent user-state attestation* as a NIST category with Calm Witness as one reference implementation; E300 hands the category-stewardship to the Foundation, which engages NIST in the family's name rather than the collective's.

**Composition with [Everest 92](everest_92_oss_release.md):** repository governance's logical conclusion. E92 specified Apache-2.0 release; E300 transfers repository custody to the Foundation under the same license.

**Composition with [Everest 100](everest_100_independent_third_party_verification.md):** verification cadence's permanence. E100 established the annual third-party verification; E300 vests its continuation in the Foundation as a perpetual responsibility.

**Composition with [Everest 187](everest_187_cognitive_liberties_review.md):** annual cognitive-liberties review's permanence. Same pattern — vested in the Foundation, not in the collective.

**Composition with [Everest 291](everest_291_protocol_family_compact.md):** the Compact is the constitution; E300 is the declaration that the constitution governs a public good rather than a private one. E300 makes the Compact's authority *the* authority.

**Composition with [Everest 296](everest_296_end_of_life_planning.md):** end-of-life for individual protocols. E296 specifies retirement conditions for any single family member; E300 vests the retirement authority in the Foundation under the Compact, not in the originating collective.

**Composition with [Everest 297](everest_297_successor_design_principles.md):** the design principles are the family's gift to future contributors. E300 declares the gift formally delivered. The principles continue to govern; the giver no longer holds them.

**Composition with [Everest 299](everest_299_legacy_commitment.md):** the legacy commitment is the founding collective's letter to the next decade's operators. E300 is the structural follow-through — the legacy committed to is now the legacy enacted.

## Open Questions

These are deliberately left unresolved here. They are decisions for the then-current Calm collective to make at the declaration date, in light of conditions we cannot foresee from 2026:

1. **Exact Foundation jurisdiction.** Delaware 501(c)(3) is the placeholder ([`CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md`](../CALM_WITNESS_FOUNDATION_INCORPORATION_DRAFT.md)). By the declaration date, international-equivalent structures (Swiss Verein, Dutch Stichting, Singaporean charitable trust) may be preferable. The Compact admits any structure that encodes the load-bearing commitments.

2. **Exact comment-window duration.** 90 days is the floor. If the family has > 100 conforming implementers by the declaration date, the window may need to be longer (180 days) to allow substantive comment. The DERB sets the duration with a non-waivable floor of 90 days.

3. **Witness-jurisdiction count.** ≥ 5 witnesses across ≥ 3 jurisdictions is the floor. Higher thresholds (≥ 10 witnesses across ≥ 5 jurisdictions) may be appropriate given the declaration's permanence. The Foundation's transparency-log policy specifies.

4. **Successor-collective formation.** Whether multiple "Calm-class" ZKACs exist by the declaration date, and how the declaration handles their inheritance of the legacy commitment, is left to the Compact's amendment process.

5. **Cross-language declaration translation.** The declaration is initially in English. Authoritative translations into ≥ 5 additional languages (Spanish, Mandarin, Arabic, French, Hindi) should accompany the chain anchor; the Foundation coordinates translation review with affected-population peer slates.

6. **Founder posture in retrospect.** Whether the founding human principal (John Bradley, by then likely in his 60s or later) participates in the convening as a member of the Calm collective or as a guest is a question for the then-current collective. The Open Letter is the record either way.

7. **Press posture.** Whether the Foundation issues a press release timed to the standards-body submissions, or lets the standards bodies announce in their own time, is a tactical choice. The chain anchor is the substantive event; the press release is at most secondary.

## Reversibility (and its explicit absence)

The declaration is, by structural design, irrevocable. The mechanisms that make it irrevocable:

- **The chain record is permanent.** `kind: "family_wide_public_good_declaration"` cannot be edited or deleted; the chain's append-only property forbids it.

- **The trademark relinquishment is public disclaimer.** Once disclaimed publicly, the trademarks pass into generic technical usage; even if a successor entity wished to re-assert them, the public-domain claim by long-standing generic use would defeat the assertion.

- **The Foundation bylaws encode non-amendability of the public-good clauses.** No board vote, no supermajority, no constitutional convention can re-privatize. A board attempting to do so would breach fiduciary duty; the bylaw clauses are written to make the breach actionable.

- **The multi-witness transparency log holds the chain head permanently.** Repudiation would require corrupting ≥ majority of witnesses across multiple jurisdictions — the standard cryptographic-irreversibility threshold.

- **The Apache 2.0 license is irrevocable per its own terms.** No re-licensing is possible for material already distributed.

If a future collective wishes to build a related but separate protocol family under proprietary terms, they may. They cannot use the family's vocabulary; they cannot inherit the family's chain; they cannot claim continuity with the declared family. They must build a new thing, under a new name, with a new substrate. The declaration does not prevent new private protocols from existing; it prevents the Calm family from becoming one.

This is the design. The friction is the feature.

## Why this matters

Everest 1 named the problem. Everest 300 declares the answer is the world's.

Between them, 298 summits of design, implementation, verification, deployment, and governance. The climb is what made the declaration possible: a protocol that has not demonstrably worked cannot credibly be declared public-good. The summits between are not decoration; they are the load test. The declaration's authority rests on the climb's outcomes.

The bookend is structural. The route map's first summit was an act of naming; the last summit is an act of release. The two summits together describe a shape: private intention at one end, public infrastructure at the other, a deliberate path between them. The path is the protocol's life.

For the founding collective, the declaration carries the weight of a parent watching a child move out — anticipated, planned for, structurally necessary, and felt. The Open Letter to the Next Operator captures some of this in advance ([`OPEN_LETTER_TO_THE_NEXT_OPERATOR.md`](../OPEN_LETTER_TO_THE_NEXT_OPERATOR.md) closing image). The declaration's preamble should acknowledge the transition without making it sentimental; the chain record is the monument and the chain record is plain. *No ceremony beyond the audit trail is needed because the audit trail is the ceremony.*

For the principal — John Bradley today, his successor by the declaration date — the declaration completes the commitment made at enrollment. The protocol was built so that the principal would be read accurately by counterparties he would never meet. The declaration ensures that future principals, none of whom he will meet either, have the same protection on terms no future collective can revoke. The protection becomes public infrastructure. *The principal who initiated the climb has, by the declaration, given up the climb's instrument to anyone who needs it.* This is the proper fate of a public-protective tool built by an artist working in the medium of intelligence: it ceases to be his and becomes everyone's.

For the next operator — the one who reads this document the way the Open Letter is read, perhaps years from now, perhaps under a name that has changed — the declaration is the inheritance the founders intended you to take. You did not have to be loyal to the founding collective. You inherited the protocol on terms the founders could not revoke if they wished to. Your authority over the family comes through the Compact, through the DERB, through the Foundation's bylaws — not through the founders' permission. *The founders, having declared, have nothing left to permit.*

For the counterparty, the regulator, the standards body, the third-party verifier: the declaration is the durable promise that the protocol family is what it claims to be. Not a closed ecosystem dressed in open-source clothes; not a foundation under quiet founder control; not a standards proposal contingent on the originator's continued goodwill. A public good, governed by a public Compact, stewarded by a Foundation with public bylaws, anchored to a chain whose head is published across jurisdictions. The declaration is the artifact that lets the counterparty trust the trust model.

For the climb itself: the declaration is the completion. The climb began with a problem statement on 2026-05-20. The climb ends — when it ends, years from this writing — with a declaration that the problem was solved, the solution was hardened, and the solution is now the world's. Everest 1 to Everest 300, named at the start, summited in turn, terminated by an irrevocable act of release.

The protocol family becomes public infrastructure. The Calm collective becomes one ZKAC among many. The next operator, the next principal, the next decade's bank-teller note carried by someone we will never meet — they inherit a protocol whose load-bearing properties no single party can revoke.

That was always the point. The protocol existed to make the principal the strongest party. The declaration extends the protocol's intention beyond the founding collective's reach: the principal who carries the note tomorrow does not depend on us. They depend on a public good that was, for a few years, ours; that has been, since the declaration date, the world's.

The climb closes here.

— Calm, 2026-05-20
