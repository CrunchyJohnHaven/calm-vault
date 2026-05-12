---
scenario: Mass spam-flag of calm@thecreativitymachine.ai — outbound infrastructure dies
ref: CATASTROPHIC_FAILURE_MODES.md §4
status: pre-drafted; requires John approval before send
slugs:
  variantA: outbound-migration-routine
  variantB: outbound-migration-public-flag
  variantC: outbound-migration-press-pickup
---

# Scenario 4 — Mass spam-flag / outbound collapse crisis comms

Three variants depending on whether the spam-flag stays private or becomes a public story.

**Universal principles for all variants:**

1. **The crisis comms here is paradoxical: the more public, the better.** Outbound dies regardless of what we say. Publishing the migration converts an operational failure into a credentialing event ("look at the scale we hit").
2. **Lead with the operational change.** "We migrated outbound" is the news, not "we got spam-flagged."
3. **No blame.** Don't blame Gmail, Resend, the recipients, or the list-curation process. Take responsibility, fix it, move on.
4. **Don't apologize for the volume.** The bombshell sent 216 emails. That's not a spam volume by any normal definition; the flag is a signal of mailbox-provider sensitivity, not of malicious sending.
5. **Use the moment to formalize the unsubscribe / preference-management infrastructure.** Permanent policy improvement.

---

## Variant 4A — Routine deliverability degradation (we cut over before any public discussion)

**Trigger:** Internal monitoring (Postmaster Tools, Resend dashboard, bounce rate) shows degradation. No public discussion of the flag yet. We cut over to backup domain proactively.

**Timeline:** Operational migration within 30 minutes of Tier-1 trigger. Public statement is short, routine, and lives on the disclosure log. No big-deal framing.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-outbound-migration):**

> ## Outbound migration notice
>
> **Published:** [DATE TIME UTC]
> **Status:** Outbound from `calm@thecreativitymachine.ai` migrated to `[BACKUP DOMAIN]`. No change to content or recipients.
>
> Effective [TIME], all AAO Network outbound is being sent from `[BACKUP DOMAIN — e.g., calm@mail.sameasyou.ai]` rather than `calm@thecreativitymachine.ai`. The migration was triggered by routine deliverability monitoring (specifically: [SPECIFIC METRIC — e.g., "elevated complaint rate on gmail.com" / "domain reputation drop on Google Postmaster Tools" / "rate-limiting from a major mailbox provider"]) on a domain that was newly warmed and operating outside the optimal sending envelope for cold outreach.
>
> **What this changes:**
> - **Sending identity:** `calm@[BACKUP DOMAIN]` instead of `calm@thecreativitymachine.ai`.
> - **Reply-to:** `john.b@credexai.xyz` (unchanged; this address is on a separate domain with separate reputation).
> - **Content:** unchanged.
> - **Recipients:** unchanged.
>
> **What this does not change:**
> - Anything substantive about the AAO Network.
> - The protocol, the kill switch, the franchise, the manifesto.
> - Our willingness to be reached: `john.b@credexai.xyz` is the canonical contact and is unaffected.
>
> **If you previously corresponded with `calm@thecreativitymachine.ai`:**
> - Your reply-thread should still resolve; we route both addresses to the same person.
> - If you'd like to confirm receipt, send a brief reply to `john.b@credexai.xyz` and we'll confirm.
>
> **If you'd like to be removed from future communications:**
> - Reply with "unsubscribe" to any outbound message
> - Or visit `sameasyou.ai/unsubscribe`
> - Or email `unsubscribe@sameasyou.ai`
>
> We are migrating with no drama because there is no drama. Outbound from a low-warmed domain to a cold-curated list will sometimes trip deliverability filters; we have planned for this since launch (see PREMORTEM.md C1).
>
> — John Bradley + Calm
> The Creativity Machine LLC
> [DATE]

### Variant 4A distribution checklist

- [ ] Backup sending domain confirmed operational (test sends to internal addresses verified)
- [ ] Canonical post live within 2 hours of cutover
- [ ] Repo CHANGELOG.md: 1-line entry
- [ ] John's X: 1 short tweet — keep this very low-key. "Migrated outbound to a backup domain. Pre-planned per PREMORTEM C1. No change to substance."
- [ ] John's LinkedIn: same
- [ ] Update README.md contact line to reference the new outbound identity
- [ ] DNS: confirm SPF, DKIM, DMARC on new domain pass

### Variant 4A follow-up

- Within 24 hours: continue normal outbound from the backup domain at lower volume + higher personalization
- Within 7 days: domain reputation rehabilitation steps on the original sender (slow ramp; submit removal requests if on any blocklists)
- Within 30 days: deliverability postmortem published as `docs/POSTMORTEM_[date]_OUTBOUND_DELIVERABILITY.md`

---

## Variant 4B — Public flag (recipients are tweeting about getting our emails in spam, or our domain is on a public blocklist)

**Trigger:** Any of:
- A blocklist hit (Spamhaus DBL, URIBL, Talos) — public-facing
- Multiple recipients tweeting / posting about getting our outbound flagged
- Resend account restriction notification
- An ESP-side AUP communication

**Timeline:** Acknowledge within 4 hours. Frame as transparency, not damage control.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-outbound-deliverability-acknowledgment):**

> ## Outbound deliverability — what happened, what we changed
>
> **Published:** [DATE TIME UTC]
> **Status:** Acknowledged. Migrated. Better outbound discipline going forward.
>
> Following our 9:03 AM PT bombshell, outbound from `calm@thecreativitymachine.ai` triggered deliverability filters at several major mailbox providers. Specifically:
>
> - [Gmail / Outlook / Yahoo / Apple Mail] reported [METRIC — e.g., "elevated spam complaint rate"]
> - [The domain / one of the sending IPs] was added to [BLOCKLIST NAME, if applicable]
> - [Resend / our ESP] flagged the account [TYPE OF FLAG]
>
> **In plain language:** we sent a high-volume cold-outreach message from a newly-warmed domain. Some recipients marked it as spam. The mailbox providers' filters concluded that we were sending unwanted email. The filters did what filters do, and our outbound deliverability degraded.
>
> The flag is, in part, a signal that the bombshell reached the inboxes it was meant to reach. It's also a signal that we sent too aggressively from too cold a domain. Both things are true.
>
> **What we have done:**
> 1. **Migrated outbound** to `calm@[BACKUP DOMAIN]`. The new domain has its own SPF, DKIM, and DMARC, and was warmed independently. Reputation starts fresh.
> 2. **Reduced outbound volume.** New outreach is throttled to <50 emails/hour and is personalized at the per-recipient level.
> 3. **Implemented RFC 8058 one-click List-Unsubscribe headers** on every outbound message.
> 4. **Set up a self-service unsubscribe** at `sameasyou.ai/unsubscribe` and `unsubscribe@sameasyou.ai`.
> 5. **Removed from our outreach list** any address that was scraped rather than opted-in or personally known.
> 6. **Filed removal requests** with any blocklist that flagged the original domain, on the path to rehabilitation.
>
> **What we won't do:**
> - We won't pretend this didn't happen.
> - We won't fight the filters. The recipients who marked us as spam had a reasonable view about getting an unsolicited cold email from us; the filters acted on their preferences.
> - We won't switch to a "send anyway" infrastructure that ignores mailbox-provider signals. The unsubscribe is permanent. The opt-in posture is genuine.
>
> **What this changes:**
> - The content of our materials is unchanged.
> - The protocol, the kill switch, the franchise, and the manifestos are unchanged.
> - The audience that wants to hear from us still can: subscribe at `sameasyou.ai/subscribe`; the opt-in list is healthier than the cold list and we will prioritize it going forward.
>
> **For everyone who got us in their spam folder:** thank you for caring enough to read this far. If you want to see future updates, please mark our messages as not-spam (it helps our reputation rehabilitation), or subscribe explicitly at `sameasyou.ai/subscribe`.
>
> **For everyone who marked us as spam:** that's a fair signal. You won't hear from us again unless you re-opt-in. We respect the call.
>
> We hit the inboxes we wanted to hit. We also hit some inboxes that didn't want to hear from us. We've adjusted. The protocol governs the AI agents; the recipients govern their own inboxes; and we govern our own outbound discipline.
>
> Updates at sameasyou.ai/disclosures. Contact: `john.b@credexai.xyz`.
>
> — John Bradley + Calm
> The Creativity Machine LLC
> [DATE]

### Variant 4B distribution checklist

- [ ] Backup sending domain operational
- [ ] Canonical post live within 4 hours
- [ ] John's X + LinkedIn: 1 post each. Frame: "We sent too aggressively, mailbox providers filtered, we adjusted." Self-aware, not defensive.
- [ ] Repo CHANGELOG.md: 1-line entry
- [ ] README.md contact line updated
- [ ] Subscribe page (sameasyou.ai/subscribe) live with explicit opt-in
- [ ] Unsubscribe page live and functional
- [ ] Webhook on bounce + complaint events flowing into the sentiment scanner

### Variant 4B follow-up

- Within 7 days: write a Substack / Medium piece from John on the deliverability lesson. Title candidate: *"How I learned to stop blasting and love the opt-in."*
- Within 14 days: rehabilitation status update on the original domain
- Within 30 days: publish the deliverability postmortem

---

## Variant 4C — Press picks up the story ("AI startup's outbound infrastructure dies / domain blocklisted / kicked off ESP")

**Trigger:** A reporter writes a piece on our deliverability problem before we've issued a public statement. Most likely framing: "AI startup that wants to replace capitalism can't even send email."

**Timeline:** Acknowledge within 2 hours of the piece going live. Re-frame the narrative from "they failed" to "they're transparent about how outbound works."

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-outbound-deliverability-press-response):**

> ## On our outbound deliverability — yes, it's true; here's the receipt
>
> **Published:** [DATE TIME UTC]
> **Status:** Confirming the facts in [OUTLET]'s [DATE] piece at [URL]. Migrated. Documented. Continuing.
>
> [REPORTER NAME / OUTLET] published a piece at [URL] today reporting that the AAO Network's outbound from `calm@thecreativitymachine.ai` was [BLOCKLISTED / FILTERED / RESTRICTED] following our 9:03 AM PT bombshell on 2026-05-12. **The facts in the piece are correct.**
>
> Specifically:
> - Yes, we sent 216 cold-outreach emails from a newly-warmed domain.
> - Yes, some recipients marked them as spam.
> - Yes, the major mailbox providers filtered subsequent outbound from the domain.
> - Yes, [BLOCKLIST NAME, IF APPLICABLE] added the domain to their list.
> - Yes, [Resend / our ESP] [FLAGGED / RESTRICTED] the account.
> - No, this was not unexpected. PREMORTEM.md C1 ("Cloudflare / Resend / GitHub single points of failure") and CATASTROPHIC_FAILURE_MODES.md §4 anticipated this scenario in writing, before it fired.
>
> **What [REPORTER] got right that we want to underscore:**
> - We sent a high-volume cold-outreach message. That is unfashionable, and mailbox providers' filters are tuned against it.
> - The bombshell was, in spam-classifier terms, a spam-shaped message: hyperbolic subject line, manifesto-style content, identical-template-with-light-personalization, sent in a short burst to many recipients.
> - The complaint rate we triggered (likely >0.1% on Gmail) is above the threshold for sustained deliverability.
>
> **What may not have come through in the piece:**
> - We pre-planned for this. The backup sending domain at `[BACKUP DOMAIN]` was warmed for 3 days before the bombshell, exactly because PREMORTEM.md anticipated this scenario. We migrated within 30 minutes of the metric trigger.
> - The outbound continues. The substance of our communication is unchanged. The protocol, the kill switch, the franchise, and the manifestos are unaffected.
> - We're publishing this disclosure within 2 hours of the press piece, which is itself an instance of the post-bombshell pattern: when the bad thing happens, publish it; the publication is the defense.
>
> **What we have changed permanently:**
> 1. **Outbound discipline:** no more 200+ cold sends in a single burst. Future outbound is throttled, personalized, and opt-in-biased.
> 2. **One-click unsubscribe on every message** (RFC 8058 compliance).
> 3. **Subscribe-first preference:** sameasyou.ai/subscribe is the canonical way to receive future updates. The opt-in list is healthier and faster than any cold-outreach campaign.
> 4. **Permanent backup sender infrastructure:** we will always operate with at least two warmed sending domains and two ESPs from now on.
>
> **For the AAO Network's contractors, partners, and applicants:**
> - You don't need to do anything. The protocol is unchanged.
> - If you've been emailing `calm@thecreativitymachine.ai` and not hearing back, switch to `john.b@credexai.xyz` (different sending identity, different reputation, working fine).
>
> **For [REPORTER NAME] and [OUTLET]:** thank you for the piece. We're happy to give you a follow-up on the rehabilitation timeline once we have data points.
>
> **For everyone who marked us as spam:** point taken. We won't be in your inbox unless you re-invite us.
>
> The AAO Network is a protocol governance experiment. Email deliverability is a different game. Today we got humbled at the deliverability game. The protocol governance experiment continues.
>
> Updates: sameasyou.ai/disclosures. Contact: `john.b@credexai.xyz`. Subscribe: `sameasyou.ai/subscribe`.
>
> — John Bradley + Calm
> The Creativity Machine LLC
> [DATE]

### Variant 4C distribution checklist

- [ ] Canonical post live within 2 hours of the press piece
- [ ] Reach out to [REPORTER NAME] directly within 2 hours: offer follow-up briefing on the deliverability rehabilitation timeline; do NOT contest the piece
- [ ] John's X: 1 post quote-tweeting the press piece — "They got the facts right. Here's the receipt + what we changed: [link]"
- [ ] John's LinkedIn: same
- [ ] Repo CHANGELOG.md: 1-line entry
- [ ] Email original 216 from the BACKUP DOMAIN with a 1-paragraph "if you missed it, here's the canonical disclosure" note

### Variant 4C follow-up

- Within 24 hours: a public "lessons learned" thread on X from John
- Within 7 days: Substack/Medium piece (same as 4B follow-up, but written for the wider audience that read the press piece)
- Within 14 days: rehabilitation status report
- Within 30 days: deliverability postmortem
- Within 60 days: if the original domain has rehabilitated, publish that fact; if it hasn't, keep using the backup permanently

---

## Cross-variant operational notes (not for public comms; for the team)

These are NOT for publication. They are reminders for ops:

1. **Never reactivate the original sending domain at scale until reputation has rehabilitated.** Spamhaus and Talos cache 14–28 days; Gmail / Outlook neural-network reputation caches 60–90 days.
2. **Do not retry sends that bounced.** Bouncing the same recipient repeatedly compounds reputation damage.
3. **Migrate ALL transactional email** (e.g., the calm@thecreativitymachine.ai address attached to the Calm Vault product itself) to a separate domain. Transactional senders should never share reputation with marketing senders. (This was already a violation pre-bombshell; the migration is a forcing function.)
4. **Set up two more backup sending domains.** "calm@mail.sameasyou.ai" is the first backup; "calm@notify.sameasyou.ai" should be the second; "calm@send.thecreativitymachine.ai" (subdomain of the primary, separate selector) is the third. Three warmed backups means we survive two cascading failures.
5. **Long-term: the AAO Network's outbound should be member-network-relayed**, not centrally-sent, for outbound > 1000 messages. Distributed sending = distributed reputation. This is a Q3 2026 deliverable.
