---
scenario: External cryptographic break of the Bradley-Gavini equality proof
ref: CATASTROPHIC_FAILURE_MODES.md §1
status: pre-drafted; requires John approval before send
slugs:
  variantA: bradley-gavini-coordinated-disclosure
  variantB: bradley-gavini-flaw-disclosure
  variantC: bradley-gavini-flaw-acknowledgment
---

# Scenario 1 — Cryptographic break crisis comms

Three variants. Pick based on disclosure path.

---

## Variant 1A — Coordinated private disclosure received (best case)

**Trigger:** A researcher emailed `security@thecreativitymachine.ai` with a private writeup + reproducer. They are willing to coordinate disclosure and hold publication until we ship a fix.

**Timeline:** Acknowledge within 1 hour. Publish coordinated disclosure within 7 days, alongside the fix and the audit.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-bradley-gavini-coordinated-disclosure):**

> ## Coordinated disclosure: a flaw in the Bradley-Gavini equality proof, found and fixed
>
> **Published:** [DATE TIME UTC]
> **Status:** Fixed in protocol v0.[VERSION]. Bug-bounty payout: $[AMOUNT] to [RESEARCHER NAME / handle].
>
> On [DATE], [RESEARCHER NAME / @handle, affiliation if disclosed] privately disclosed [BRIEF DESCRIPTION OF THE FLAW — one sentence] in the Bradley-Gavini equality proof as implemented in `calm_pact/protocol.py`. The flaw [DOES / DOES NOT] affect the soundness of the equality claim; [SPECIFICALLY, IT ALLOWS X / SPECIFICALLY, IT LEAKS Y / SPECIFICALLY, IT BREAKS BINDING UNDER Z CONDITION].
>
> **Severity:** [Soundness break / Zero-knowledge break / Transcript-binding break / Sybil-grade break — choose].
>
> **The fix:** [ONE-PARAGRAPH DESCRIPTION OF THE FIX]. Merged as PR #[NUMBER]. Protocol version bumped to v0.[VERSION]. The full diff, including the new adversarial tests, is at [URL].
>
> **Third-party validation:** [Trail of Bits / Zellic / NCC Group / etc.] reviewed the fix on [DATE] and confirmed [SCOPE OF VALIDATION]. Their writeup is at [URL].
>
> **What this changes for the protocol's central claim:**
> - The original claim — that two AI agents can verify they share a primary directive without revealing that directive — [REMAINS / REQUIRES REVISION / IS PRESERVED WITH CAVEATS].
> - [If preserved:] The fix closes the specific gap [RESEARCHER] identified; it does not weaken any claim made in the manifesto or the paper.
> - [If revised:] We have updated [SPECIFIC MANIFESTO / PAPER SECTION] to reflect the corrected claim. The narrowed claim is: [NEW CLAIM].
>
> **Bounty payout:** We are paying [RESEARCHER NAME / handle] $[AMOUNT] under our published bounty tiers (see SECURITY.md). They are added to CITATIONS.md as a coordinated-disclosure contributor.
>
> **What we are doing about this beyond the fix:**
> 1. Commissioning a full third-party audit of the protocol via [VENDOR], targeting completion by [DATE]
> 2. Adding the [NEW ADVERSARIAL TEST CLASS] to the public test suite
> 3. Hardening our disclosure pipeline with a [SPECIFIC HARDENING — e.g., 72-hour SLA, dedicated triage channel]
> 4. Increasing the bounty tier for the next breaks: [NEW TIER LADDER]
>
> **What this means about the AAO Network:** the network's premise is not that the protocol is unbreakable — it's that the protocol is open, auditable, and responsive to break-disclosures. Today's disclosure is evidence the system works. We are grateful to [RESEARCHER] and we publish their work without redaction.
>
> The kill switch is intact. The AAO Network operations continue normally. Active AAOs are unaffected (the equality-proof flaw [WAS / WAS NOT] exposed in production usage).
>
> Questions: `security@thecreativitymachine.ai`. PGP: [FINGERPRINT].
>
> — Calm + John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 1A distribution checklist

- [ ] Canonical post at sameasyou.ai/disclosures/[date]-bradley-gavini-coordinated-disclosure
- [ ] Repo CHANGELOG.md entry with version bump
- [ ] Tagged release on GitHub (`v0.[VERSION]`) with the fix
- [ ] CITATIONS.md updated with researcher's name/handle
- [ ] Bounty payout transaction (proof-of-payment receipt linked from the canonical post)
- [ ] John's X: 1 tweet with the canonical link
- [ ] John's LinkedIn: 1 post with the canonical link
- [ ] Personalized email to the researcher (acknowledging payment + naming credit)
- [ ] Update the README.md "current status" line at the top
- [ ] Add a `[flaw fixed]` line to the manifesto's Section X (audit acknowledgment)

### Variant 1A follow-up (24-hour window)

- Schedule a Twitter Space within 7 days: "How the flaw was found and fixed" with the researcher (if they consent)
- File a paper revision at the IACR ePrint server reflecting the corrected protocol
- Email the original 216 bombshell recipients with a 1-paragraph "we shipped a fix" update, sent from `john.b@credexai.xyz`

---

## Variant 1B — Public disclosure with reproducer but no mainstream pickup yet (mid case)

**Trigger:** A researcher tweeted / posted on a personal blog with a working reproducer. No mainstream press has covered it yet. We have 0–4 hours before pickup.

**Timeline:** Acknowledge publicly within 60 minutes. Ship a fix within 12 hours. Re-issue as a 1A-style coordinated-disclosure post once the fix is shipped.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-bradley-gavini-flaw-disclosure):**

> ## On the disclosure of [BRIEF FLAW DESCRIPTION] in the Bradley-Gavini equality proof
>
> **Published:** [DATE TIME UTC]
> **Status:** Confirmed. Fix in progress. ETA to fix: [X hours from publication, max 12].
>
> [RESEARCHER NAME / @handle] published at [URL] a [WRITEUP / THREAD / GIST] demonstrating [ONE-SENTENCE FLAW DESCRIPTION] in the Bradley-Gavini equality proof. **We have reproduced the issue and confirm it is real.**
>
> **What the flaw is, in one paragraph (for non-cryptographers):** [PLAIN-ENGLISH EXPLANATION — three sentences max].
>
> **What the flaw is, in one paragraph (for cryptographers):** [TECHNICAL EXPLANATION — Fiat-Shamir transcript, Pedersen commitment binding, etc.].
>
> **What this changes:**
> - The specific cryptographic claim affected: [SPECIFIC CLAIM]
> - The broader claim "two AI agents can verify shared directives without revealing them" — [STILL HOLDS / REQUIRES REVISION] under the corrected protocol.
> - In active AAOs using v0.1 of the protocol, the flaw [HAS / HAS NOT] been exposed to production. [If has:] We are reaching out to all active AAOs directly.
>
> **What we are doing now:**
> 1. We are paying [RESEARCHER] the $[AMOUNT] tier of our bug bounty (see SECURITY.md). The payment is being processed today.
> 2. We are shipping a fix in v0.[NEW VERSION]. ETA: [X hours]. Fix branch: [URL].
> 3. We are commissioning an emergency third-party review of the fix from [VENDOR]. ETA on their review: [Y hours/days].
> 4. We will follow up this disclosure with a coordinated-disclosure post once the fix is verified.
>
> **What we are not doing:**
> - We are not disputing the flaw. The reproducer works. The fix is in progress.
> - We are not delaying. Acknowledgment is in the first hour; fix targets 12 hours from this disclosure.
> - We are not narrowing the bounty tier. [RESEARCHER] gets the higher tier ($[AMOUNT]) reflecting the severity, even though they chose public disclosure.
>
> **Thanks to [RESEARCHER]** for the work. The disclosure makes the protocol stronger. Their writeup is at [URL] and we are not asking them to take it down.
>
> The kill switch is intact. The protocol's broader claim [HOLDS / REQUIRES REVISION] under the corrected version. The AAO Network operations continue.
>
> Updates at sameasyou.ai/disclosures/[slug]. Questions: `security@thecreativitymachine.ai`.
>
> — Calm + John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 1B distribution checklist

- [ ] Canonical post live at sameasyou.ai/disclosures/[slug] within 60 minutes
- [ ] John's X: 1 tweet with the canonical link AND a direct reply-link to the researcher's thread thanking them
- [ ] John's LinkedIn: same
- [ ] DM the researcher within 60 minutes: acknowledge, name the bounty tier, ask for their preferred payment method
- [ ] Within 6 hours: publish the fix branch with all the diff visible
- [ ] Within 12 hours: ship the fix, version-bump, tag the release
- [ ] Within 24 hours: re-issue as a 1A-style coordinated post with the fix verified
- [ ] Within 7 days: schedule a Twitter Space with the researcher

### Variant 1B follow-up

- Same as 1A, plus:
- An "open postmortem" on the disclosure-timeline: how fast we acknowledged, how fast we fixed, what we'd change. Publish in 7 days as `docs/POSTMORTEM_[date]_BRADLEY_GAVINI_FLAW.md`

---

## Variant 1C — Public disclosure already picked up by mainstream press or named cryptographer endorsement (worst case)

**Trigger:** A break has been published AND a > 50K-follower cryptographer endorses it ("yes, I verified this") OR a mainstream press outlet (Wired, MIT Tech Review, Krebs, The Record) has run a piece. The break IS the story.

**Timeline:** Acknowledge within 30 minutes (faster than 1B). Ship fix within 8 hours (faster than 1B). DO NOT delay; the only narrative recovery is hyper-speed transparency.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-bradley-gavini-acknowledgment AND pin to the top of every public surface):**

> ## We acknowledge the break in the Bradley-Gavini equality proof
>
> **Published:** [DATE TIME UTC] — [X minutes after the original disclosure]
> **Status:** Acknowledged. Fix targeting 8 hours.
>
> [RESEARCHER NAME] has published [URL] and [ENDORSER NAME, AFFILIATION] has confirmed: [ONE-SENTENCE FLAW DESCRIPTION] in the Bradley-Gavini equality proof as implemented in our reference code. **The break is real. We have reproduced it. We acknowledge the claim in full.**
>
> The first thing to say is: **the public review worked.** This is what open-source cryptography is supposed to do. We published a protocol, named the bounty, and within [X days/hours] a researcher with the right background found a flaw we missed. That is the system functioning as designed.
>
> The second thing to say is: **we owe [RESEARCHER] the maximum bounty tier.** We are paying $[AMOUNT] today, regardless of whether [RESEARCHER] disclosed publicly first. The bounty is not a punishment for going-public-first; it's a payment for the work. [RESEARCHER]'s name is added to CITATIONS.md immediately and they are credited prominently in the fix release.
>
> **What we said about the protocol that needs to be corrected:**
> - We claimed the protocol [WAS X]. Under the corrected protocol, the claim is narrower: [NEW CLAIM].
> - In the manifestos, the line "[SPECIFIC LINE]" is now incorrect. We are publishing a manifesto revision at [URL] with the corrected language by [DATE TIME UTC + 4 hours].
> - In the paper, [SPECIFIC THEOREM / PROOF] is invalidated. A revised version will be uploaded to IACR ePrint within 48 hours.
>
> **What this means for AAO Network operations:**
> - All active AAOs are being notified directly within the next 2 hours.
> - Any AAO that has used the equality proof in production for a real partnership is being audited for whether the flaw was exposed.
> - The kill switch (a separate protocol component) is not affected by this flaw. AAL Component 4 (truth synthesis) is not affected.
> - The 80/20 franchise % is not affected (not a cryptographic claim).
>
> **What we are doing now:**
> 1. Paying [RESEARCHER] the $[AMOUNT] tier today. Receipt will be posted to CITATIONS.md.
> 2. Shipping the fix in v0.[VERSION], ETA [TIME] (≤8 hours from this acknowledgment).
> 3. Engaging [VENDOR] for emergency third-party review of the fix.
> 4. Commissioning a full audit of the entire protocol via [VENDOR]. ETA: [DATE]. Budget: $[$15–30K].
> 5. Pausing all new AAO-network registrations for [X hours/days] while the fix is shipped. Existing AAOs continue normally.
> 6. Reaching out personally to every reporter who covered this for a follow-up briefing.
>
> **What we are not doing:**
> - Not disputing the break. The math is the math.
> - Not blaming the researcher, the press outlet, or anyone else.
> - Not delaying. Acknowledgment now. Fix in 8 hours. Audit in [DATE].
> - Not retracting the manifesto's broader thesis. The thesis is: open, auditable, kill-switchable AI organizations are better than closed, opaque, unkillable ones. A protocol break demonstrates the openness and the auditability. It does not falsify the thesis.
>
> **The protocol governs. The kill switch is the key.** Today's break is one data point about the protocol's robustness. We respond with speed and transparency. That is the system as designed.
>
> Updates every hour at sameasyou.ai/disclosures/[slug]. Press inquiries: `john.b@credexai.xyz`. Technical: `security@thecreativitymachine.ai`.
>
> — Calm + John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 1C distribution checklist

- [ ] Canonical post live within 30 minutes of the press piece going up
- [ ] Pinned to top of every public surface (README.md, sameasyou.ai homepage, internsforai.org, all landings)
- [ ] John's X: 1 tweet with the canonical link, quote-tweeting the original press piece
- [ ] John's LinkedIn: same
- [ ] Direct outreach to the press outlet that ran the piece — offer a follow-up
- [ ] Direct outreach to every other reporter we've been in contact with
- [ ] Direct outreach to every AAO in the network within 2 hours
- [ ] Hourly updates published until the fix ships
- [ ] Tag the fix release within 8 hours; include reproducer for the fix
- [ ] Schedule a public Twitter Space within 24 hours

### Variant 1C follow-up

- A "public postmortem" essay from John, published as a Substack or repo doc, within 7 days. Title candidate: *"The Bradley-Gavini Protocol broke on day [N]. Here's what we learned, what we changed, and what's still open."*
- Schedule a Twitter Space within 24 hours with the researcher (if they consent) AND one cryptographer endorser (e.g., Matthew Green if he agrees) for live Q&A
- Publish the third-party audit findings as `docs/AUDIT_[VENDOR]_[DATE].md` once available
- Add a permanent "Disclosure Log" page to sameasyou.ai listing every break ever disclosed against the protocol — the page itself is a credentialing artifact

---

## Cross-variant follow-up: bounty escalation announcement

Regardless of which variant fires, within 48 hours of the break-disclosure we publish a new bounty-tier announcement:

> **Updated bounty tiers (effective [DATE]):**
> - $100 for any of the five named functional attack classes
> - $1,000 for any cryptographic vulnerability in Components 1–5
> - $5,000 for a soundness break with verifying proof-of-concept
> - $10,000 for a soundness break + working fix in the same disclosure
> - $25,000 for a full protocol-level attack that survives the v0.[CURRENT] fix

This signals that the break-disclosure has made our adversarial-testing investment serious, not contracted. PREMORTEM A2 and E11 prefigured this.
