---
scenario: Federal regulatory action — SEC franchise % review, federal platform content flag, or UCMJ Article 134 inquiry
ref: CATASTROPHIC_FAILURE_MODES.md §3
status: pre-drafted; requires John approval AND counsel review before send
slugs:
  variantA: sec-inquiry-statement
  variantB: federal-content-flag-statement
  variantC: ucmj-article-134-statement
---

# Scenario 3 — Federal regulatory action crisis comms

**Important:** Unlike the other scenarios, comms in this scenario should be reviewed by counsel before publication. The pre-drafts below establish the public *posture* — what we want to say at a high level — but specific legal language must be cleared by securities / labor / military-law counsel as appropriate.

Three sub-variants for three sub-scenarios. Pick based on which agency / mechanism is in play.

**Universal principles for all variants:**

1. **Posture: "We welcome the inquiry."** Adversarial framing here loses. Transparent cooperation, on the record, is the only winning move.
2. **Do not concede legal positions in public comms.** "We are open to dialogue with the regulator" ≠ "we admit we did X." Counsel reviews every sentence.
3. **Operations continue unless and until formally enjoined.** Public messaging emphasizes "the AAO Network is operating normally" so contractors and partners don't panic.
4. **Move the press story from "AI startup investigated" to "AI startup welcomes oversight and publishes everything."** DARK_MUSK §3 pattern: convert opposition into substantive public forums.
5. **Never publicly speculate on the regulator's motivations or processes.**

---

## Variant 3A — SEC / state securities regulator inquiry (franchise % alleged to be unregistered security)

**Trigger:** Receipt of any of:
- Formal SEC subpoena, voluntary production request, or Wells notice
- State securities regulator inquiry (NY DFS, CA DFPI, MA Securities Division, TX State Securities Board)
- Press inquiry referencing a regulator-side investigation we haven't yet been notified of

**Timeline:** No public statement until securities counsel has reviewed. Counsel review target: 4 hours from receipt. Public statement target: 8 hours from receipt. **Do not skip counsel review on this one.**

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-securities-inquiry — AFTER counsel review):**

> ## On the regulatory inquiry into the AAO Network's franchise structure
>
> **Published:** [DATE TIME UTC]
> **Status:** Cooperating with [REGULATOR NAME]'s inquiry. AAO Network operations continue normally. Outside counsel: [LAW FIRM NAME].
>
> On [DATE], the AAO Network received [DESCRIBE FORMAL DOCUMENT — "a voluntary information request" / "an examination notice" / "an inquiry from"] from [REGULATOR NAME]. The inquiry [REQUESTS INFORMATION ABOUT / CONCERNS] the 80/20 revenue-share structure between independent contractors and The Creativity Machine LLC.
>
> We welcome the inquiry. We have engaged [LAW FIRM NAME] as outside counsel. We are providing the requested information on the timeline [REGULATOR NAME] has set. Our position, supported by counsel:
>
> **The 80/20 structure is a service agreement between independent contractors and a service provider. It is not a securities offering.**
>
> Specifically:
> - **No money is invested.** Independent contractors provide labor; they do not purchase ownership, equity, or any claim on future profits beyond their direct revenue share for their own work.
> - **Profits accrue from the contractor's own labor**, not from the efforts of a promoter. The "common enterprise" element of Howey applies only to the shared infrastructure (the AAL, the kill switch, the protocol), which is open-source and free; the LLC's role is service provision, not investment management.
> - **Members have no equity in The Creativity Machine LLC.** John Bradley is the sole owner; the LLC has not issued securities of any kind.
> - **Our securities-disclaimer page** at sameasyou.ai/legal/securities-disclaimer (published [DATE]) sets out this analysis in detail.
>
> **What we are doing:**
> 1. Producing requested documents on [REGULATOR]'s timeline.
> 2. Continuing to onboard new contractors under the existing 80/20 structure, with the disclaimer prominently linked from every signup flow.
> 3. Inviting [REGULATOR]'s staff to publicly examine the open-source protocol, the operational documents, and the disclosed financial structure. All of it is at github.com/CrunchyJohnHaven/calm-vault.
> 4. Offering [REGULATOR] a courtesy briefing from our counsel + our technical team if helpful.
>
> **What we are not doing:**
> - We are not pausing operations. Contractors who have signed agreements continue to work and to be paid under those agreements.
> - We are not retracting any public materials. The manifestos, the protocol, the franchise structure, and the published documentation are unchanged.
> - We are not characterizing [REGULATOR]'s inquiry beyond saying we welcome it. Specific responses are submitted directly to the regulator and are not being litigated in public.
>
> **For affected parties:**
> - **Current contractors:** Your 30-day agreements remain in force. Payments continue on schedule. You are not under any inquiry.
> - **Prospective applicants at internsforai.org:** Onboarding continues. The application flow now includes a confirmation that you have read the securities disclaimer.
> - **Partner AAOs:** No action required on your part.
> - **Press:** [LAW FIRM NAME] is the primary contact for legal questions. John is the primary contact for everything else.
>
> The protocol governs. The 80/20 split stands. We welcome regulatory scrutiny because the structure is documented, transparent, and counsel-vetted.
>
> Press inquiries: `john.b@credexai.xyz`. Legal: `[LAW FIRM CONTACT]`.
>
> — John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 3A distribution checklist (counsel-reviewed)

- [ ] Securities counsel has reviewed and approved the exact text of this statement
- [ ] Canonical post live within 8 hours of receipt of the regulator notice
- [ ] Repo CHANGELOG.md updated with a 1-line entry (no legal interpretation; just timestamp + link)
- [ ] Securities disclaimer at sameasyou.ai/legal/securities-disclaimer is live and accurate (this should already be live from pre-bombshell mitigation §3.4)
- [ ] John's X: 1 short tweet linking the canonical post. No legal interpretation in the tweet. No bravado.
- [ ] John's LinkedIn: same
- [ ] Email to all active contractors within 4 hours of public statement: "Here's what's happening; your agreement is unchanged; here's where to read more"
- [ ] Email to all partner AAOs: same
- [ ] Update internsforai.org application flow to include a securities-disclaimer checkbox

### Variant 3A follow-up

- Within 7 days: a long-form explainer essay from John (or a press interview) on the difference between a franchise service agreement and a securities offering. Make this educational, not defensive.
- Within 14 days: publish the response we submitted to the regulator (redacted as needed) as a public document. Transparency is the credential.
- Within 30 days: if the inquiry resolves favorably, publish that resolution. If it doesn't, publish the next step.
- Add a permanent "Regulatory disclosures" page to sameasyou.ai with every regulatory contact, dated, documented.

---

## Variant 3B — Federal-platform content flag (calm@thecreativitymachine.ai blocked at .gov mail filters, federal content-moderation flag)

**Trigger:** Any of:
- Bounce reports from .gov addresses indicating policy-violation rejection
- Federal mailbox-provider blocklist hit (Microsoft Government Cloud filter, Mimecast .gov plan)
- Federal cybersecurity center (CISA, FBI IC3) automated-flag notification
- Reporter inquiry referencing federal content flag

**Timeline:** Acknowledge within 2 hours. Cut over to backup sending domain within 30 minutes (operational, not comms). Public statement focuses on the operational change, not the flag itself.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-deliverability-and-content-review):**

> ## On deliverability and content review of AAO Network communications
>
> **Published:** [DATE TIME UTC]
> **Status:** Outbound from `calm@thecreativitymachine.ai` was experiencing deliverability issues with [SPECIFIC DOMAIN CLASS — e.g., .gov mailbox providers / specific federal-agency filters]. Outbound has been migrated to `[BACKUP DOMAIN]`. The content of our communications is unchanged.
>
> On [DATE], we received [DESCRIBE — bounce reports / a notification / a press inquiry] indicating that messages sent from `calm@thecreativitymachine.ai` were [BEING QUARANTINED / RETURNED / FLAGGED] by [SPECIFIC RECIPIENT-SIDE INFRASTRUCTURE — e.g., "the federal-agency mailbox provider used by .gov accounts"].
>
> We have not received notice of any formal federal investigation, blocklist, or restriction. The signals we have observed are consistent with **automated content-filtering by recipient-side infrastructure**, not with directed regulatory action. We are treating this as a deliverability and content-review issue, not a regulatory issue.
>
> **What we have done (effective [TIME]):**
> 1. Migrated outbound from `calm@thecreativitymachine.ai` to `[BACKUP DOMAIN — e.g., calm@mail.sameasyou.ai]`. The backup domain has separate SPF, DKIM, and DMARC. Public-facing sender is identical; the underlying domain is new.
> 2. Reviewed our outbound copy for language that automated filters flag — specifically, words like "kill switch," "weapon," and militarized framing. We have softened these in upcoming sends without changing the substance of our claims.
> 3. Added the recipients who experienced quarantine to a private contact list for direct outreach via more deliverable channels (LinkedIn message, John's personal email).
> 4. Filed deliverability-restoration requests with [SPECIFIC MAILBOX PROVIDERS — e.g., Microsoft Postmaster / Google Postmaster Tools].
> 5. Reached out to [SPECIFIC INFRASTRUCTURE OWNER, IF KNOWN] to understand the flag and request review.
>
> **What we have not done:**
> - We have not been contacted by any federal agency or law-enforcement entity about our communications.
> - We have not retracted any public materials.
> - We have not stopped publishing the manifestos, the protocol, the press kit, or any other public artifacts.
> - We have not characterized this as a "federal block" because we have no evidence that's what it is. Automated mail filtering is not regulation.
>
> **What this means for you:**
> - **If you received a message from us in your spam/quarantine folder:** please mark it as not-spam if you want to see the rest of our outbound. The content is unchanged.
> - **If you've been trying to reply to us and we haven't responded:** check your sent folder for bounce notifications. We are also reachable at `john.b@credexai.xyz` (a different sending identity that's unaffected).
> - **If you are a federal employee who wants to receive our materials but can't through your work address:** reply from a personal address. We will route appropriately.
>
> **The protocol governs.** The AAO Network operates without dependence on any single mailbox provider, sending domain, or content-filter regime. Outbound has been migrated. The substance of what we say is unchanged. The story is the migration, not the flag.
>
> Updates at sameasyou.ai/disclosures. Questions: `john.b@credexai.xyz` (working) or `[NEW CONTACT FROM BACKUP DOMAIN]`.
>
> — John Bradley + Calm
> The Creativity Machine LLC
> [DATE]

### Variant 3B distribution checklist

- [ ] Backup sending domain operational + reputation-warmed BEFORE public statement (operational has to lead comms by ≥30 minutes)
- [ ] Canonical post live within 2 hours
- [ ] John's X + LinkedIn: 1 post each. Frame: "deliverability migration," not "blocked by feds."
- [ ] Email to original 216 from the BACKUP DOMAIN with a 1-paragraph note: "If you didn't get our previous message from calm@thecreativitymachine.ai, here it is from the new address."
- [ ] Direct reach-out to any .gov contact via personal email or LinkedIn
- [ ] No combative framing toward any federal agency, ever

### Variant 3B follow-up

- Within 7 days: a deliverability postmortem essay. Frame as iteration data: "we sent too aggressively, recipient-side filters caught it, we migrated."
- Document the content-review changes in a public CONTENT_GUIDE.md so future outbound (ours or third-party) avoids the same flags.
- If specific federal infrastructure is the source, file an FOIA request for the relevant content-moderation policy.

---

## Variant 3C — UCMJ Article 134 inquiry (service member affected)

**Trigger:** Any of:
- Direct contact from a JAG officer, military command, or service member's chain-of-command referencing Article 134
- News piece referencing a service member who replied to / was affected by our outreach
- A service member personally informing us they are facing Article 15 NJP or court-martial related to our communications
- A press inquiry specifically asking about military recipients

**Timeline:** **Do not publish a public statement before consulting military-law counsel.** Internal acknowledgment to the service member or their JAG within 1 hour. Public statement target: 24 hours, with counsel review.

**Canonical statement (publish at sameasyou.ai/disclosures/[date]-military-recipient-clarification — AFTER military-law counsel review):**

> ## On AAO Network communications to military recipients — a clarification
>
> **Published:** [DATE TIME UTC]
> **Status:** Reviewing all outreach to .mil addresses. Halting any further sends to military email infrastructure until review complete. Military-law counsel: [LAW FIRM / ATTORNEY NAME].
>
> The Creativity Machine LLC has become aware that one or more of its outreach emails may have reached active-duty service members at their official `.mil` email addresses. We are issuing this statement to clarify three points.
>
> **1. The Creativity Machine LLC is operated by civilians.** Our company has no military authority of any kind. We do not represent any military command, branch, or service. Our communications are civilian commercial and editorial communications, not military communications.
>
> **2. We did not intend our outreach to reach official military inboxes.** Our outreach was targeted at a list of civilian recipients — researchers, journalists, technologists, and AI-safety community members. To the extent any recipient was contacted at a `.mil` email address, that was an oversight in our list curation. **We are halting all outbound to `.mil` addresses immediately.** Existing contacts at `.mil` addresses can reach us at `john.b@credexai.xyz`; we will not initiate further contact at any `.mil` address.
>
> **3. The framing in our outreach is editorial commentary, not direction or command.** Phrases such as "the protocol governs" refer to a software protocol governing autonomous AI agents; they are not directives to any human reader, and they are not intended to communicate authority over any person — civilian or military.
>
> **For any service member who received our outreach:**
> - You did not consent to receive our communications; we apologize for the unsolicited email at your official address.
> - We have no expectation that you respond, engage with, or take any action regarding our materials in your official capacity.
> - We will not initiate further contact at your `.mil` address.
> - If you are facing any questions from your command regarding our outreach, please have your JAG contact our military-law counsel at [LAW FIRM CONTACT]; we will cooperate fully and provide any documentation needed to demonstrate that the recipient bore no responsibility for our list-curation oversight.
>
> **For any commander, JAG, or service investigator:**
> - We will produce any documentation requested.
> - We will confirm in writing for any specific service member that they did not solicit our outreach and that we initiated contact in error.
> - Our counsel at [LAW FIRM CONTACT] is the primary point of contact.
>
> **Operational changes effective immediately:**
> 1. A hard filter in our outbound dispatcher rejects all `.mil` addresses with logging. No `.mil` send can occur from any AAO Network outbound, period.
> 2. Our content is being reviewed for any language that could be construed as invoking military authority or threatening communications, and we are softening the specific phrases that contributed to this oversight (specifically: "the protocol governs," "we are notifying you," and "kill switch" framing).
> 3. We are publishing a permanent policy at sameasyou.ai/policies/military-recipients: "The AAO Network does not solicit, initiate, or maintain unsolicited communications with active-duty military email addresses. This is a permanent operational policy."
>
> **The protocol governs.** It governs software; it does not govern people, and especially not service members in their official capacity. We regret the list-curation oversight and we have eliminated the conditions that created it.
>
> Press: `john.b@credexai.xyz`. Military-law: `[LAW FIRM CONTACT]`.
>
> — John Bradley
> The Creativity Machine LLC
> [DATE]

### Variant 3C distribution checklist (counsel-reviewed)

- [ ] Military-law counsel has reviewed and approved the exact text
- [ ] Hard filter rejecting `.mil` addresses is deployed and tested BEFORE the canonical statement goes live
- [ ] Canonical post live within 24 hours of becoming aware of the issue
- [ ] Permanent policy at sameasyou.ai/policies/military-recipients live
- [ ] Direct outreach within 1 hour of awareness to any specific service member affected (via JAG if their JAG has contacted us; otherwise via the most-deliverable channel that does not re-touch a .mil address)
- [ ] Documentation package prepared for any JAG-side request: the recipient list, the date, the source of the address inclusion, the absence of consent on our side, the operational fix
- [ ] John's X + LinkedIn: 1 short post each linking the canonical post, no editorial flourish, no defensiveness
- [ ] No statement to press beyond the canonical post unless counsel approves

### Variant 3C follow-up

- Within 7 days: publish a "How we curate recipients" document at sameasyou.ai/policies/outreach-list-curation, including the .mil-exclusion hard filter, the role-account exclusion, and the opt-out mechanism.
- Within 14 days: confirm with counsel that the matter is resolved on the service member's side. If it is, publish a brief update. If not, work with counsel on next steps.
- Permanent policy: no AAO Network outbound to `.mil` addresses, ever.

---

## Cross-variant federal-action follow-up

For any of 3A / 3B / 3C, within 30 days we publish a "Regulatory Engagement Log" at sameasyou.ai/policies/regulatory-engagement. Entries:

- Date of contact
- Agency or infrastructure owner
- Type of contact (formal subpoena / informal inquiry / automated flag / etc.)
- Our response (linked)
- Resolution status

The log itself is a credentialing artifact — DARK_MUSK pattern #3, "publicize the bad thing." Treating regulatory contact as a public record converts it from a hidden vulnerability into transparent civic engagement.
