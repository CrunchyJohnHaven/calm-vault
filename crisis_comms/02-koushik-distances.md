---
scenario: Koushik Gavini publicly distances himself from the Bradley-Gavini Protocol and/or technosocialism framing
ref: CATASTROPHIC_FAILURE_MODES.md §2
status: pre-drafted; requires John approval before send
slugs:
  variantA: koushik-distance-personal
  variantB: koushik-distance-schwab-corporate
  variantC: koushik-distance-press-first
---

# Scenario 2 — Koushik Gavini distances himself crisis comms

Three variants depending on whose statement comes first.

**Universal principles for all variants:**

1. **Gratitude first.** Koushik's contribution to the zero-trust verification primitives stands. Lead with thanks.
2. **No grudge, no spin.** Whatever Koushik or Schwab says, accept the surface meaning. Do not litigate "was he really co-author?" in public.
3. **Preserve the protocol name as a technical convention.** "Bradley-Gavini Protocol" is mathematical literature naming; consent is not required for technical-name precedent (cf. RSA, ECDSA, Diffie-Hellman). The public-association rebrand is for marketing surfaces, not for the math.
4. **Remove Schwab affiliation immediately and irreversibly.** Even with Koushik's verbal consent, the public-employer-name has to go.
5. **Attribute the technosocialism framing solely to John.** The framing is John's; the math is collaborative. Separate them cleanly.

---

## Variant 2A — Koushik personally posts a distancing statement (LinkedIn / X / personal site)

**Trigger:** Koushik publishes a public statement — LinkedIn post, X tweet, personal site, or signed correction email forwarded to press — distancing himself from co-authorship, the technosocialism framing, or both.

**Timeline:** Acknowledge within 60 minutes of the distancing post going up. Edit the public materials within 6 hours. The acknowledgment + the edit are the entire crisis comms.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-koushik-statement-acknowledgment):**

> ## On Koushik Gavini's statement regarding the Bradley-Gavini Protocol
>
> **Published:** [DATE TIME UTC]
> **Status:** Acknowledging Koushik's statement at [URL]. Affiliation removed from public materials.
>
> Koushik Gavini published a statement at [URL OF HIS POST] [today / on DATE]. He [SUMMARIZE IN ONE NEUTRAL SENTENCE — e.g., "wishes to clarify that he did not co-author the technosocialism manifesto," or "wishes to clarify that his contribution was to zero-trust verifiable-credentials primitives and not to the broader AAO Network framing"].
>
> Koushik is right to publish this. We respect his decision and we are correcting our public materials accordingly within the next 6 hours.
>
> **What we are changing:**
> 1. **The README and the manifestos** are being updated. The authorship line now reads: "John Bradley (The Creativity Machine) and Calm (Claude Opus 4.7 configured under the Calm Oath). The mathematical underpinnings draw on zero-trust verifiable-credentials work that Koushik Gavini contributed to in 2021 and discussed with John at that time. The technosocialism framing, the AAO Network operational design, and the manifesto's political claims are John's alone — Koushik has not endorsed them and we are not asking him to."
> 2. **The "Head of Blockchain Engineering, Charles Schwab" affiliation is removed.** This was always a courtesy reference; we should not have included an employer affiliation without explicit consent, and we are removing it from all public materials.
> 3. **The protocol name "Bradley-Gavini Protocol" persists** as a literature convention — the same way "Diffie-Hellman" persists as a literature convention separate from its authors' employment. Koushik retains naming credit for the technical primitive; he is not associated with the technosocialism manifesto, the franchise structure, or the AAO Network operational entity.
> 4. **Primary-source documents in `docs/PRIMARY_SOURCE_*.md`** are historical record and not edited; they reflect what was communicated on [original dates] and they include a contemporaneous annotation linking to this disclosure.
>
> **What we want Koushik to know:**
> - The technical work he contributed is real, it is foundational to the protocol, and it remains credited.
> - The framing decisions that he didn't endorse are John's; the public record now clearly reflects that.
> - We are grateful for his willingness to discuss this publicly rather than through lawyers. The clarity is a gift to both projects.
>
> **What this changes about the AAO Network:**
> - The protocol's cryptographic properties are unchanged. The math is the math.
> - The 80/20 franchise structure is unchanged.
> - The technosocialism framing is unchanged but is now correctly attributed to John alone.
> - The "first demonstration" timestamp (May 11, 2026, 21:55 UTC) is unchanged.
>
> Public-facing rewrites land at [URL OF UPDATED README + MANIFESTOS] by [DATE TIME UTC + 6 hours]. The diff is at PR #[NUMBER] in the public repo.
>
> The protocol governs. The collaboration that produced the math was real and is honored. The framing that surrounds it is now correctly attributed.
>
> — John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 2A distribution checklist

- [ ] Canonical post live within 60 minutes
- [ ] PR opened in the repo with the rewrites (the pre-staged `koushik-distance-prep` branch); merged within 6 hours
- [ ] README, manifestos, landing pages, and `paper/bradley-gavini-protocol-v0.html` updated
- [ ] `CO-AUTHOR-CONSENT.md` created at repo root documenting the new attribution
- [ ] Reply (one short, respectful reply) to Koushik's original post linking the canonical disclosure
- [ ] John's X: 1 tweet thanking Koushik for the work + linking the canonical disclosure
- [ ] John's LinkedIn: 1 post, same
- [ ] Direct email to Koushik (NOT public, NOT pressuring) confirming the changes are made + offering to discuss further
- [ ] Email the original 216 bombshell recipients with a 1-paragraph "we updated our authorship attribution" note, sent from `john.b@credexai.xyz`
- [ ] Press: respond to any inquiry with the canonical-post link only; do not editorialize beyond it

### Variant 2A follow-up

- John writes a Substack/Medium post within 14 days reflecting on the experience and on the lesson about co-author consent ("I should have called him before publishing the manifestos. I didn't. He clarified. We corrected.")
- The `koushik-distance-prep` branch was already staged; merging it is the heavy-lift, and that's done within 6 hours

---

## Variant 2B — Schwab corporate communications issues a statement (not Koushik personally)

**Trigger:** Charles Schwab's corporate communications, legal, or IR team issues a statement — directly to press, on Schwab's own channels, or via legal notice to us — disclaiming any connection between Schwab and the AAO Network and instructing us to remove the employer affiliation.

**Timeline:** Acknowledge within 60 minutes of Schwab's statement. Remove "Charles Schwab" from every public material within 2 hours.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-schwab-statement-acknowledgment):**

> ## On Charles Schwab's statement regarding the AAO Network
>
> **Published:** [DATE TIME UTC]
> **Status:** Schwab affiliation removed from all public materials. No further use of the Schwab name.
>
> Charles Schwab's [communications / legal / IR] team [issued a statement / contacted us] today regarding the inclusion of "Head of Blockchain Engineering, Charles Schwab" as an affiliation for Koushik Gavini in our public materials.
>
> **The short version:** Schwab is right, and we have already corrected it.
>
> We included Koushik's employer affiliation as a courtesy reference in our README and manifestos. We did so without obtaining Schwab's permission and without considering the brand-safety implications for Schwab. That was a mistake on our part. The 80/20 franchise model + the technosocialism manifesto are not associated with Charles Schwab, were never authorized by Charles Schwab, and never should have been linked to Schwab's brand in any way.
>
> **What we have changed (as of [TIME]):**
> 1. Every reference to "Charles Schwab," "Head of Blockchain Engineering, Charles Schwab," and any Schwab-related descriptor is removed from: README.md, CALM_PACT_PROTOCOL_v0.md, END_OF_CAPITALISM_MANIFESTO.md, TECHNOSOCIALISM_MANIFESTO.md, the landing pages, the paper HTML, the site at sameasyou.ai, and the press kit.
> 2. The author line in our materials now references Koushik Gavini by name only, with no employer reference, until or unless he chooses to add one.
> 3. The historical primary-source documents in `docs/` are not edited (they are factual records of communications at specific times), but each has been annotated with a link to this disclosure.
> 4. We are not contesting any of Schwab's requested changes. If anything else needs to be removed, we will remove it on request.
>
> **What we want Schwab to know:**
> - We respect the brand-safety concern. It is a reasonable one.
> - The work being done at the AAO Network is John Bradley's framing, and the political claims are John's. None of that was Schwab's view, and we should not have suggested otherwise by listing the employer name.
> - We are not seeking to restore the Schwab affiliation. The work proceeds without it.
>
> **What this changes about the AAO Network:**
> - The cryptographic protocol is unchanged.
> - The 80/20 franchise is unchanged.
> - The author of the technosocialism framing is, and was always, John Bradley.
>
> The protocol governs. We made an attribution mistake and we are correcting it without dispute. Schwab is not part of the AAO Network in any way.
>
> — John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 2B distribution checklist

- [ ] Canonical post live within 60 minutes
- [ ] Schwab affiliation REMOVED from every file in the repo (search for "Schwab" and confirm zero matches in non-historical files)
- [ ] PR opened + merged within 2 hours (faster than Variant 2A because the change is mechanical)
- [ ] Direct reply to Schwab's legal/IR contact confirming receipt + showing the diff
- [ ] No public dispute, no clever rebuttal — accept and move on
- [ ] John's X + LinkedIn: 1 tweet/post each thanking Schwab for the prompt clarification (yes, thank them; turns the encounter into a credentialing artifact for our responsiveness)
- [ ] Press: any inquiry gets the canonical-post link only

### Variant 2B follow-up

- John publishes a 14-day reflection essay ("On the importance of asking before naming"). Frame as a humility piece, not a justification.
- Update the repo's `CO-AUTHOR-CONSENT.md` to include a "Process for crediting external contributors" section as a permanent policy

---

## Variant 2C — Press story first (a reporter publishes "Koushik Gavini was not consulted on technosocialism" before Koushik or Schwab publish anything)

**Trigger:** A reporter (most likely covering Schwab from CNBC, Bloomberg, WSJ, or covering AI-startup-controversy from TechCrunch, Information, Wired) publishes a story whose lede is "the named co-inventor of the AI-safety protocol was not consulted on the manifesto framing."

**Timeline:** Acknowledge within 60 minutes of the press piece. Press-first scenarios are higher risk because:
- We don't know what Koushik will say next
- Schwab now has external pressure to respond
- Other press outlets pile on

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-koushik-attribution-clarification):**

> ## On Koushik Gavini's involvement with the AAO Network — a clarification
>
> **Published:** [DATE TIME UTC]
> **Status:** Clarifying our authorship attribution following [REPORTER NAME / OUTLET]'s [DATE] piece at [URL].
>
> [REPORTER NAME] published a story at [OUTLET URL] today raising whether Koushik Gavini consented to being named as co-author of the Bradley-Gavini Protocol and to the framing of the technosocialism manifesto.
>
> The reporter raised a fair concern. The honest answer is:
>
> 1. **Koushik contributed to zero-trust verifiable-credentials primitives that were discussed in 2021 and that are foundational to the equality-proof component of our protocol.** That contribution is real and is credited.
> 2. **John Bradley wrote the manifestos and chose the technosocialism framing.** The framing is John's alone. Koushik did not author the framing, was not consulted on the framing, and has not endorsed the framing.
> 3. **The co-author line in our README listed Koushik with employer affiliation as a courtesy reference**, based on John's recollection of the 2021 conversation. We did not seek Koushik's explicit consent for the way the technosocialism manifesto was framed because John, in his haste during a 16-hour sprint, did not understand that the manifesto's framing required separate consent from the technical primitives' attribution. That was a mistake.
>
> **Changes effective immediately:**
> - "Head of Blockchain Engineering, Charles Schwab" is removed from all public materials.
> - The README author line is updated to clearly separate (a) Koushik's contribution to the cryptographic primitive (credited) from (b) John's framing of the manifesto (sole author).
> - We are reaching out to Koushik directly to confirm whether he wants the "Bradley-Gavini Protocol" name preserved as a literature convention or replaced. We will respect his decision. (If he prefers a renaming, the protocol can be called "Calm Pact" or "ZK Alignment Equality Proof" without affecting the math.)
> - The pre-staged PR with these changes is at [URL] and is being merged now.
>
> **What we are not doing:**
> - We are not disputing [REPORTER NAME]'s framing.
> - We are not waiting for Koushik's response before correcting our materials. We are correcting them on our side.
> - We are not asking Koushik to publicly endorse anything.
>
> **What we want the public to know:**
> - The protocol's math is real. The break-glass kill switch is real. The 33/34 tests pass. None of that depends on co-authorship attribution.
> - The framing of the manifesto — that the age of human-run capitalism is ending — is John Bradley's framing. It is not Koushik's. It is not Charles Schwab's. It is not anyone else's. It is one person's argument, and one person's risk.
> - The AAO Network proceeds. The protocol governs. The authorship attribution is corrected.
>
> Updated public materials live at [URL] within 4 hours of this disclosure.
>
> — John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 2C distribution checklist

- [ ] Canonical post live within 60 minutes of the press piece
- [ ] Pre-staged PR merged within 4 hours
- [ ] Reach out to the reporter directly within 60 minutes: offer follow-up briefing
- [ ] Reach out to Koushik directly within 60 minutes (phone first, then email): "Press just published [link]. We've already corrected our materials. We're not asking you to do anything publicly; we just want you to know how we responded."
- [ ] Reach out to Schwab IR proactively (NOT defensively) with the canonical-post link
- [ ] John's X + LinkedIn: 1 short post each, link to canonical, no editorial flourish
- [ ] Email to original 216 with the canonical link

### Variant 2C follow-up

- Within 24 hours, if Koushik DOES post a statement (Variant 2A pathway), that becomes the canonical record; we link from this disclosure to his.
- Within 7 days, a longer reflection essay from John on the structural lesson (the 14-day reflection essay from 2A/2B).
- Add a permanent FAQ entry to sameasyou.ai: "Is Koushik Gavini a co-author of the AAO Network?" with the clear answer.

---

## Cross-variant follow-up: the protocol-name decision

Regardless of which variant fires, within 14 days we ask Koushik (via private email, with no public pressure):

> Koushik — would you like the protocol to retain the name "Bradley-Gavini Protocol" as a literature convention (similar to "Diffie-Hellman" or "Pedersen commitments"), or would you prefer it renamed? Either is fine on our side. If renamed, "Calm Pact" or "ZK Alignment Equality Proof" are our preferred replacements.

If he says preserve: we keep "Bradley-Gavini" in the math and the academic paper, but the AAO Network's marketing surfaces shift to "Calm Pact" as the primary brand for the protocol.

If he says rename: we rename. The math is unchanged. The brand is recoverable.

This conversation is private. The outcome is published.
