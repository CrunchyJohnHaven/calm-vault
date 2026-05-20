# The Calm Witness Foundation — Incorporation Framework

**DESIGN-BAGGED · SUMMIT E241 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — actual 501(c)(3) filing requires registered agent + initial board + Form 1023 submission.

The Calm Witness Foundation is the legal trustee of the Calm Suite's public-trust assets: the Treaty registry, the public predicate vocabulary registry, the conformance test corpus, the Sigsum witness operator selection, and the standards-track submissions. It is the institutional home that makes Calm Suite operations *founder-outliving* (Treaty Article VI §6.4). The Foundation exists to remove the protocols from any single principal's commercial interest while preserving the public benefits.

---

## §1. Purpose and structure

**§1.1** The Foundation is a US 501(c)(3) public-charity entity incorporated in Delaware. Charitable purpose: *the advancement of cryptographic primitives that protect the privacy and dignity of human principals interacting with autonomous AI agents, through education, research, governance, and the maintenance of public-domain technical standards.*

**§1.2** The Foundation does not develop products. The Foundation does not raise capital for commercial deployment. The Foundation does not own or operate any Calm Suite implementation. The Foundation maintains: (i) the Treaty registry; (ii) the public predicate vocabulary registry; (iii) the conformance test corpus; (iv) the open-source verifier reference implementation; (v) the public security disclosure infrastructure.

**§1.3** Funding model: small recurring donations from operators (Apache-2.0 licensees who choose to contribute) plus restricted grants from disability-rights, AI-safety, and cryptographic-research funders. The Foundation refuses funding from any organisation operating in a Treaty-forbidden context (law enforcement, employment screening, insurance, lending, custody adjudication, immigration adjudication, surveillance, aggregate analytics). This refusal is normative in the bylaws, not discretionary.

## §2. Board composition

Per Treaty Article VI §6.4, the Foundation's board mirrors the first-convening signatory classes plus operational roles. Nine-member board, three-year terms, staggered so that one third rotates annually.

| Seat | Filled by | Term |
|---|---|---|
| 1 | Disability-rights director (nominated by AAPD or equivalent) | 3 years |
| 2 | Cognitive-liberty director (nominated by CCLE or equivalent) | 3 years |
| 3 | Cryptographer-of-record director (named individual; rotates by community vote) | 2 years |
| 4 | Cryptographer-of-record director (second) | 2 years |
| 5 | Standards director (NIST/IETF/W3C liaison) | 3 years |
| 6 | International director (non-US jurisdiction representative) | 3 years |
| 7 | Operator-of-record director (current Calm operator's principal) | 1 year |
| 8 | Independent director (community-elected) | 2 years |
| 9 | Independent director (community-elected) | 2 years |

Seat 7 is held by John Bradley initially; rotates annually with the operator-of-record's principal. The seat does not confer veto authority over Treaty-level decisions.

No seat may be held by an officer or employee of an organisation that operates in a Treaty-forbidden context. Seats 8 and 9 are elected by signatory quorum (Treaty Article VI §6.1) at the annual review.

## §3. Initial filings

**§3.1 Articles of Incorporation.** Filed in Delaware as a non-profit corporation. Charitable purpose per §1.1. Name: *Calm Witness Foundation*. Registered agent: TBD (mainstream non-profit registered-agent service).

**§3.2 IRS Form 1023.** Federal application for 501(c)(3) recognition. Anticipated qualifying activities: (a) maintenance of open-source software for public benefit; (b) educational activities (curriculum at named universities per E292); (c) standards-track submissions to government bodies (NIST/USAISI); (d) research grants to support cryptographic research aligned with the Foundation's purpose.

**§3.3 Bylaws.** Adopted at the first board meeting. Include: the no-funding-from-forbidden-contexts rule (§1.3 above); the conflict-of-interest framework (mirroring Treaty Article III); the no-private-inurement framework standard for 501(c)(3); the open-meeting rule (board meetings recorded, transcripts public within thirty days); the principal-protective veto (any Calm Suite principal may file an emergency objection to a Foundation action affecting their attestations; the objection automatically pauses the action pending board review).

**§3.4 Conflict of interest policy.** Each director signs annually. Same disclosure requirements as Treaty Article III: funding sources, operating exposure, personal-relationship-to-John-Bradley (because the Foundation's first decade is shaped by that proximity), compensation expectations.

**§3.5 Initial board appointment.** The first board is appointed at the first convening (E216). Subsequent board changes follow §2 above.

## §4. The trusteeship assets

The Foundation receives, at first board meeting, custody of the following public-trust assets:

**§4.1 The Treaty registry.** Hosted at calm-vault.com/treaty/, mirrored to the Foundation's own infrastructure. Sigsum-witnessed transparency log. Signatures, votes, amendments are all public-record.

**§4.2 The public predicate vocabulary registry.** Content-addressable list of every predicate any Calm Suite implementation may evaluate. Additions follow `PREDICATE_AUDIT_PROCESS_v0.md`. Removals (per Treaty Article IV one-way ratchet) raise the refusal floor.

**§4.3 The conformance test corpus.** Currently the Python files `calm_witness/conformance_vectors.py` and `calm_compass/conformance_vectors.py`; Foundation publishes JSON-canonical versions for cross-language implementations.

**§4.4 The open-source verifier reference implementation.** The Foundation does not write code; it maintains the canonical fork of the reference implementations and merges PRs that pass the conformance corpus.

**§4.5 The public security disclosure infrastructure.** GPG-key-protected inbox at security@calm-vault.org; published responsible-disclosure policy (90-day window); CVE coordination with relevant national authorities.

## §5. Operations the Foundation never undertakes

**§5.1** Issuing operator credentials. CredexAI (or equivalent verifiable-credential issuer) does this. Foundation does not duplicate.

**§5.2** Operating Calm Suite implementations on behalf of any principal. Operators are private parties under principal direction.

**§5.3** Marketing or evangelism for any specific operator. The Foundation may publish educational materials about the protocol; it does not endorse particular implementations.

**§5.4** Holding any principal's vault, chain, or biometric data. Vaults are principal-controlled by protocol design.

**§5.5** Accepting funding contingent on predicate-vocabulary decisions or Treaty amendments. Restricted grants must be vocabulary-neutral; if a grant attempts to influence vocabulary scope, the Foundation declines.

## §6. The founder-outliving guarantee

Treaty Article VI §6.4 commits the Foundation to outlive its founding principal. The mechanisms:

**§6.1 Successor certification.** Each board seat has a documented succession protocol. Seats 1-6 + 8-9 succeed via class-or-community election. Seat 7 (operator-of-record's principal) succeeds via the protocol's principal-replacement mechanism; if no operator-of-record exists, seat 7 dissolves and the board operates with eight members.

**§6.2 Asset perpetuity.** Foundation charter requires that all trusteeship assets (§4) be transferred to a successor 501(c)(3) before dissolution. The Foundation's Articles of Incorporation specify the priority-ordered list of successor candidates: Electronic Frontier Foundation, Software Freedom Conservancy, Mozilla Foundation, the W3C, in that order.

**§6.3 Open-source perpetuity.** The Foundation guarantees, in its bylaws, that all software it maintains remains under Apache-2.0 (or a successor license at least as permissive). The Foundation may not retroactively relicense.

**§6.4 Treaty perpetuity.** The Treaty registry, as a transparency log, persists independent of the Foundation. If the Foundation dissolves without a successor, the registry remains accessible at its Sigsum-anchored URL; signatories remain bound by their commitments to the extent the signatories themselves persist.

## §7. The first board meeting

Held immediately following the first convening's close (Day 2 evening). Agenda:

```
Items 1-3   Election of officers (Chair, Treasurer, Secretary)
Item 4      Adoption of bylaws (drafts circulated 30 days prior)
Item 5      Adoption of conflict-of-interest policy
Item 6      Approval of Articles of Incorporation as filed
Item 7      Authorization of Form 1023 submission
Item 8      Acceptance of trusteeship assets (§4 above)
Item 9      Approval of successor priority list
Item 10     Designation of registered agent
Item 11     Scheduling of first quarterly meeting
```

Meeting is recorded; minutes are published within 30 days; vote-by-vote record is permanent.

## §8. The founder's role after the founding

John Bradley's role after the Foundation is operative is **principal-of-record only**, not director and not officer beyond Seat 7's one-year initial term. The Foundation's charter forbids the founder from accepting compensation from the Foundation. Per Treaty Article III §3.4, John (or any future operator-of-record principal) may freely substitute their operator; this does not change Seat 7's tenure.

This separation is the structural answer to the question *what happens to the protocol if its founder is no longer trusted, or no longer present?* The answer: the protocol continues. The Foundation maintains the registry. The signatories maintain their commitments. The operator-of-record principal cycles. The founder becomes one of many.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
