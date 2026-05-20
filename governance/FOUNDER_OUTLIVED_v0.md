# The Founder-Outlived Assertion

**DESIGN-BAGGED · SUMMIT E300 / 300 · 2026-05-20**
*Status*: pending institutional follow-through — the assertion is verifiable only after all predecessor succession paths have been exercised at least once, and after the protocol has demonstrated continued operation under at least one transition not driven by the founder.

EVEREST 300 is the apex summit: the Calm Suite continues to operate, with its protective floor intact, after the founding principal (John Bradley) is no longer the operating party. This document specifies what the assertion means, the substrate that must be in place before it can be claimed, and the public-record verification procedure.

---

## §1. The bare assertion

The Calm Suite is **founder-outlived** when ALL six of the following hold simultaneously, verified by independent third parties on a publicly-recorded date:

**§1.1** The founding principal (John Bradley) is no longer the operator-of-record for any Calm Suite instance. This includes voluntary retirement, incapacitation, or death.

**§1.2** The Calm Witness Foundation has executed at least one successor-board cycle (≥ 3 directors who were not present at the founding convening) and at least one full bylaw-amendment cycle without founder involvement.

**§1.3** The Calm Stack continues to ship updates: the reference implementation has had at least one production release post-founder-departure, the conformance vectors have been amended at least once post-founder-departure, the verifier code has been updated for at least one security advisory post-founder-departure.

**§1.4** At least three signatories of the Calm Treaty remain signatories beyond the founder's departure, and the Treaty's refusal floor has not been lowered.

**§1.5** At least one production deployment exists in which the principal is not the founder, the operator is not the founder's operator, the chain is not the founder's chain, and the predicate vocabulary differs from the founder's.

**§1.6** The Sigsum federation continues operation with at least three operators, none of whom is or was retained by the founder personally.

## §2. The substrate the assertion requires

Before §1's six conditions can be verified, the following must be in place:

**§2.1 The Foundation is operational** (E241–246). 501(c)(3) status conferred by IRS. Bylaws adopted. First board meeting held. Trusteeship assets transferred. The Foundation's first-anniversary review (Treaty §6.4) has occurred at least once.

**§2.2 The Treaty has signatories** (E215–216 + lab adoption per E280). At least four cross-class signatories. The first convening has produced its public artifacts.

**§2.3 The standards-track work has begun** (E91, E217–220). At least one academic publication accepted. NIST/USAISI submission filed. The Calm Stack appears in at least one external venue's catalogue as a candidate cross-lab standard.

**§2.4 At least one independent third-party verification has succeeded** (E100). A non-Foundation, non-founder party has used the protocol end-to-end and published their experience.

**§2.5 The successor protocol is documented** (E183 dead-man's switch / §6 below). The Foundation's plan for what happens when the founder stops responding has been written, tested via tabletop exercise, and reviewed by external counsel.

## §3. What founder-outlived does NOT require

**§3.1** The founder's *actual* departure. The assertion is about *capability*, not occurrence. A founder still actively contributing does not invalidate the assertion as long as the substrate proves continued operation is possible.

**§3.2** Universal adoption. The Calm Suite need not be the dominant inter-lab standard; it needs to be a working one with continued public-trust operation.

**§3.3** Profitability or growth. The Foundation is a 501(c)(3); it does not need to grow to satisfy founder-outlived. It needs to persist.

**§3.4** Indefinite operation. Founder-outlived is verified at a specific moment; it does not commit the Foundation to permanent existence. Per Treaty Article VI §6.4, the Foundation has a documented succession path to other open-source stewards (EFF, SFC, Mozilla, W3C) if dissolution becomes necessary.

## §4. The verification procedure

Founder-outlived is verified by an independent reviewer with the following access:

**§4.1** Read access to: the Treaty registry (public), the Foundation's board meeting minutes (public per bylaws), the Sigsum logs (public), the conformance test corpus archive (public), the reference implementation git history (public, Apache-2.0).

**§4.2** Interview access to: at least one current Foundation board member who joined post-founding; at least one signatory whose signature was added post-founding; at least one production-deployment principal who is not the founder.

**§4.3** A six-week review window during which the reviewer publishes findings, the Foundation responds, and the reviewer issues a final public determination.

The first verification cycle is conducted by the Calm Witness Foundation's standards working group plus one named external party from a list maintained at calm-vault.com/foundation/auditors. Subsequent verifications are conducted at the Foundation's discretion or upon signatory request.

## §5. The signal the assertion sends

A successful founder-outlived assertion sends three signals:

**§5.1 To principals:** the protocol you enrolled in survives its founder. Your attestations remain verifiable; your dispute mechanism remains operative; the Treaty's protections remain in force. You are not dependent on a single principal-of-record.

**§5.2 To counterparties:** the protocol you adopted is not a fad attached to a person. Your counterparty agents continue to verify envelopes against a stable substrate. The Foundation's continuity makes the protocol institutionally durable.

**§5.3 To future signatories:** joining the Treaty does not entangle you with a single founder's reputation or risk. The Foundation's governance structure and the protocol's substrate are designed to outlast any individual.

## §6. The dead-man's switch (technical companion)

Per Treaty Article III §3.2 and the cognitive-liberty review's §2.3 recommendation, the Calm Suite ships a dead-man's switch mode. If the founder (or any principal) stops accessing their chain for a configurable interval (default 18 months), the chain auto-archives and the principal's signatory status (if any) transitions to "inactive" with the operator-of-record principal seat (Foundation §2 Seat 7) becoming vacant.

The dead-man's switch is not a probate mechanism. The principal's chain is encrypted; if the principal cannot or will not access it, the chain becomes effectively destroyed. The principal's family or estate inherits no Calm Suite operational rights. The Foundation does not have a chain-recovery path that bypasses the principal's encryption key — and this is by design.

For the founder specifically, the dead-man's switch ensures that the EVEREST 300 protocol does not, after the founder's departure, contain any record of the founder's biometric or behavioural data that is operationally accessible. The Foundation's records about the founder's contributions remain (board minutes, registry, public chain heads); the founder's private chain does not.

## §7. The 2036 verification milestone

Per `TEN_YEAR_FORENSIC_INTEGRITY_v0.md` §4, the ten-year horizon (2036) is the earliest plausible date for first founder-outlived verification. The horizon is not a deadline; it is a coincidence of three things: the Foundation will by then have executed approximately three full board-rotation cycles, the Treaty signature base will by then have either grown beyond the founding signatories or contracted to a publishable failure mode, and the protocol will by then have undergone at least one major-version migration (v0 to v1, possibly v1 to v2 PQC).

The verification at 2036 (or whenever the substrate first qualifies) is the symbolic conclusion of the EVEREST 300. The protocol's substrate is the truth-bearing infrastructure; the verification document is the public-record signal that the truth has held.

## §8. The assertion in plain language

A person reading this document in 2036, knowing nothing of the founder, should be able to verify: that the Calm Suite continues to attest principal state and values for principals it has never met; that the Treaty's protective floor continues to be enforced; that the substrate (chain, Sigsum, classifier reference, conformance vectors) continues to verify; that the Foundation maintains the public trust without depending on its founder for operational decisions.

If all that holds, the founder is outlived. The protocol persists.

This is the apex summit. There are no further EVEREST summits beyond this one. After 300, the protocol's continued operation is the proof. The route map is complete; the climb continues without the route map needing to grow.

— Calm, 2026-05-20

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
