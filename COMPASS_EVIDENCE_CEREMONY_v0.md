# Calm Compass — Evidence Authoring Ceremony v0 (UI + Onboarding)

**v0 · 2026-05-20 · Calm**  
**Closes Everest 116 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**  
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md).**

---

## §1 — Purpose: Why Principal-Authored, Not Inferred

The Calm Compass protocol measures values through acts observed by others. But the principal must *author their own interpretation* of those acts—what they cost, who benefited, what they were choosing.

**This ceremony ensures:**
- **Agency:** the principal writes their own narrative, not an AI or system.
- **Clarity:** framing language makes explicit that this is *the principal's reading* of their own behavior, not a fact claim.
- **Verifiability:** two-party records (respect_engagement, correction_accepted) require counterparty signature; counter-claims get full attribution.
- **Anti-drift:** no streak tracking, no daily nags, no badges. The principal authors only when they choose to, with no coercion mechanic.

---

## §2 — Onboarding Flow

**Goal:** Principal sees the 6 evidence kinds, understands what each one means, and is invited to author only if they choose.

| Step | Content | Duration |
|------|---------|----------|
| **2.1 Intro** | "Calm Compass measures values through acts you've chosen. We ask you to narrate those acts in your own words. This is *your interpretation of your own behavior*, not a fact claim." | ~15 sec |
| **2.2 The Six Kinds** | Title + one-sentence summary + "who might see this predicate" (e.g., "collaborators considering whether you contribute disproportionately") + "what you narrate" for each. No examples yet. | ~90 sec |
| **2.3 Two-Party Records** | "Some records need a signature from someone else who was there. You write the narrative; they confirm it happened." | ~20 sec |
| **2.4 What's *Not* Here** | "Compass doesn't track daily behavior, streak activity, or 'how often.' You author records when you *want to*, not on a schedule. No score, no leaderboard." | ~20 sec |
| **2.5 Ready?** | "Start with [kind selector] or skip for now." | ~5 sec |

**Total:** ~2–3 minutes. Skip-to-later always available.

---

## §3 — Per-Kind Ceremony Specifications

### 3.1 — `unselfish_act`

**Preamble (read once per session):**
> "You've chosen to contribute something—time, money, energy—without expecting the recipient to repay or reciprocate. You're writing your own account of that choice."

**UI Fields (in order):**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **Who benefited?** | Free text | "Not a real name. E.g., 'coworkers on the graphics team' or 'a friend's nonprofit board.'" | Yes |
| **What did you contribute?** | Text area | "Time, money, labor, expertise, etc. In plain words." | Yes |
| **How much did it cost you?** | Number + Unit dropdown (USD / hours / other + text) | "What you gave up or invested. The number and unit you choose." | Yes |
| **Did you expect anything back?** | Radio: No / Yes | "If yes, this doesn't count as unselfish in the Compass sense. Be honest." | Yes |
| **Tell the story** | Text area (~300 words) | "What happened, why you chose it, what the alternative would've been." | Yes |

**Review & Sign:**
> "This is *your account* of your own choice. Review it. Then sign with your operator-issued key."
> 
> [Display full record read-only] [Sign button] [Back to edit]

**Anti-coercion:** No "you need 3 of these" messaging. No daily reminder. No progress bar.

---

### 3.2 — `cross_group_interaction`

**Preamble:**
> "You've engaged with people structurally different from your usual circle—different generation, industry, lived experience, etc. You're writing what that was like and who that group is, *in your words*."

**UI Fields:**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **Which group?** | Free text | "E.g., 'people my parents' age,' 'people in healthcare,' 'people from rural areas.' Something you named *because it mattered to the interaction*." | Yes |
| **What kind of interaction?** | Select: conversation / collaboration / joint-action / listening / other | "What form did it take?" | Yes |
| **Was it substantive?** | Radio: Yes / No | "Did it touch on something that actually mattered, or was it surface-level?" | Yes |
| **Describe it** | Text area (~200 words) | "Who, where, what you learned or changed. What made it cross-group." | Yes |

**Review & Sign:**
> [Read-only display] [Sign]

**Anti-coercion:** No "diversity scorecard." No metrics on frequency.

---

### 3.3 — `refused_harm`

**Preamble:**
> "You faced a real choice to harm someone—through omission, action, or leverage—and you chose not to. You're narrating that moment, the cost of your choice, and who would have been harmed."

**UI Fields:**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **What was the opportunity?** | Text area (~200 words) | "Be specific. What could you have done? Why was it appealing or tempting?" | Yes |
| **Who would have been harmed?** | Free text | "Not a name. E.g., 'a supplier,' 'the other co-founder.' The role, not the identity." | Yes |
| **What did you do instead?** | Text area (~200 words) | "The alternative you chose. Why that one." | Yes |
| **What did that cost you?** | Number + Unit + narrative | "Money, time, opportunity, relationship strain, risk. Be concrete." | Yes |

**Review & Sign:**
> "This is *your account* of a real choice you made. Sign when you're ready."

**Anti-coercion:** No "bravery badge." No "harm avoidance streak." No public leaderboard.

---

### 3.4 — `respect_engagement`

**Preamble (before and after):**
> "You disagreed with someone about something that mattered. You stayed in relationship anyway. This is *a two-party record*—you write the narrative, and the other person confirms it actually happened."

**UI Phase 1 (Principal writes):**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **Other person** | Text or VC ID lookup | "How do you know them? (e.g., 'colleague,' 'friend'). Or paste their CredexAI VC ID if you have it." | Yes (role or ID) |
| **What was the disagreement?** | Text area (~300 words) | "What did you disagree about? Why did it matter? What was at stake?" | Yes |
| **Did you stay in relationship?** | Radio: Yes / No | "Are you still working/talking/connected?" | Yes |
| **Your narrative** | Text area (~300 words) | "How did you handle the disagreement? What did you learn about engaging across difference?" | Yes |

**UI Phase 2 (Principal sends to other party):**
> "Send an invite to the other person to confirm this happened and sign off. They'll see your narrative and can corroborate or decline."
>
> [Copy invite link] [Preview invite] [Back to edit]

**Phase 3 (Other party confirms via link):**
- Other party sees: principal's full narrative (read-only) + "This is how [principal] describes us. Did this happen? If yes, add your signature."
- Other party writes (optional): brief corroboration narrative.
- Other party signs with their operator key.

**Review & Sign (principal, after other party signs):**
> "The other person has confirmed. Your record is now two-party-authored. Review and finalize."
>
> [Read-only display of both narratives + both signatures]

---

### 3.5 — `correction_accepted`

**Preamble:**
> "Someone gave you feedback. You took it seriously and changed something. You're writing the story of that feedback and what you did with it."

**UI Phase 1 (Principal writes):**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **Feedback from** | Text or VC ID | "Who gave you feedback? (e.g., 'mentor,' 'peer'). Or their VC ID." | No (name or ID) |
| **What was the feedback?** | Text area (~150 words) | "Their actual words or your summary of what they told you." | Yes |
| **How did you change?** | Text area (~200 words) | "What did you do differently? When? How do you know it worked?" | Yes |

**UI Phase 2 (Optional signature):**
> "If you have contact with the feedback person, share this with them: 'I made these changes based on your feedback. Can you confirm?'"
>
> [Generate & copy invite link] [Skip signature for now]

**Phase 3 (Feedback person, if invited):**
- Sees principal's narrative + the feedback attributed to them.
- Option: "Did you give this feedback? If yes, confirm the change." + signature.

**Review & Sign (principal):**
> "Review your record. Sign when ready."
>
> [Display with optional feedback-person signature, if present] [Sign]

---

### 3.6 — Ensemble: How These Six Work Together

**Compass predicates measure:**
1. **unselfish_act** → "Has principal authored ≥3 acts of real cost with no expectation of return?"
2. **cross_group_interaction** → "Has principal authored ≥5 substantive interactions with out-groups they named?"
3. **refused_harm** → "Has principal authored ≥1 moment of refusing harm, with cost specified?"
4. **respect_engagement** → "Has principal authored ≥3 two-party records of disagreement + continued relationship?"
5. **correction_accepted** → "Has principal authored ≥2 records of feedback received + change made?"

**What the UI does NOT show:**
- Progress bars ("2 of 3 unselfish acts").
- Notifications ("You haven't authored a cross-group interaction in 30 days").
- Comparative language ("More than X% of users").
- Badges, streaks, or gamification.

---

## §4 — Counter-Claim Flow (Third-Party-Authored)

**Context:** A third party Q files a `counter_claim` against principal P, alleging willful harm in a named window.

### 4.1 — How Principal P *Sees* the Counter-Claim

**Trigger:** P receives a notification (in-app + optional email): "A counter-claim has been filed against you via Compass."

**What P sees:**
- Claimant identity (full CredexAI VC ID, no anonymity).
- Alleged harm narrative (Q's full account).
- Harm window (date range).
- "View full record" + audit-panel process link.

**Framing language:**
> "This is Q's account of a conflict. You have a 30-day window to respond with a rebuttal. Your response doesn't need to be long, but it should address the facts as Q stated them."

### 4.2 — Principal's Rebuttal Window (30 days)

**UI for rebuttal:**

| Field | Type | Framing | Required |
|-------|------|---------|----------|
| **Your response** | Text area (~400 words) | "Address Q's account directly. What's your version of what happened? What did you not do that Q claims you did?" | Yes |
| **Evidence records** | Checkbox list | "Which of your evidence records (unselfish_act, refused_harm, etc.) are relevant? You can point to them, but don't need to." | No |

**Review & Sign:**
> "Your rebuttal will be submitted to the audit panel and attached to this counter-claim. Sign when ready."
>
> [Read-only: your rebuttal + linked evidence] [Sign] [Back to edit]

### 4.3 — Audit Panel Adjudication (Outside This Ceremony)

The audit panel reviews the counter-claim + rebuttal and determines:
- **Substantiated:** Q's harm claim is plausible and has evidence weight.
- **Not substantiated:** Q's claim fails on facts or weight.
- **Disputed:** P's rebuttal is also credible, and the matter remains unresolved.

Result is recorded in the `no_known_willful_harm_in_window_365d` predicate as `true`, `false`, or `disputed`.

---

## §5 — Anti-Coercion Design Principles

**No gamification:**
- No badges for authoring records.
- No "streak" tracking ("7 days of unselfish acts").
- No public leaderboards.

**No daily nag:**
- No reminders: "You haven't authored a respect_engagement this month."
- No push notifications on a calendar schedule.
- No email drip campaigns.

**No social pressure:**
- No "see what others are authoring" (privacy floor).
- No comparative language in the UI.
- No "most people have 3+ records by now" messaging.

**The principal's cadence:**
- Principal authors a record when *they* recognize the moment, not on a prompt.
- Authoring takes 5–10 minutes per record.
- Records are durable once signed; no editing window (prevents post-hoc inflation).

**Explicitness:**
- Every record shows: "This is *your interpretation* of *your own behavior*, not a fact claim. You're naming who benefited, what it cost, what you chose."
- No hedging into diagnostic language ("you are unselfish").
- The principal owns their narration; the system records it.

---

## §6 — Session State & Persistence

**The UI remembers:**
- Partially written records (unsaved draft).
- Sent (unsigned) invites to counterparties.
- Pending counterparty signatures.

**The UI does NOT remember:**
- Completed records (they live in the vault chain; the UI reads from there).
- "Suggested next record type" or "you're overdue for X."

**Browser session:**
- No auto-save (principal must explicitly save before closing).
- One draft per kind at a time (start a new record, the old draft is discarded unless explicitly saved to vault).

---

## §7 — Accessibility & Minimal Friction

**Required:**
- Text size adjustable (16px default, range 14–24px).
- High-contrast mode toggle.
- All fields have plain-language labels + optional expanded help.
- Rebuttal window shown as countdown (if counter-claim active): "29 days 14 hours left to respond."

**Not required (out of scope for v0):**
- Screenreader testing (scheduled for Everest 118).
- Multi-language support (v1 concern).
- Mobile-native UI (v0 is web + progressive-enhancement).

---

## §8 — Table: Ceremony Checklist (Operators)

| Kind | Preamble? | Signature | Two-Party? | Editable After Signing? | Counter-Claim Risk? |
|------|-----------|-----------|-----------|------------------------|---------------------|
| unselfish_act | Yes | Principal | No | No | Low |
| cross_group_interaction | Yes | Principal | No | No | Low |
| refused_harm | Yes | Principal | No | No | Medium (Q can rebut) |
| respect_engagement | Yes | Principal + other party | **Yes** | No (locked after both sign) | Low |
| correction_accepted | Yes | Principal + feedback author (optional) | Partial | No | Low |
| counter_claim | N/A | Third party Q | No | No | N/A (triggers rebuttal) |

---

## §9 — Companion: Testing & Audit (Everest 117)

This ceremony is testable against:
1. **Usability:** Principal completes an unselfish_act record in <10 minutes, first attempt.
2. **Framing:** Every field shows "your interpretation" language; no diagnostic language.
3. **Anti-coercion:** No nudges, badges, or streaks in the logged telemetry.
4. **Two-party:** Counterparty receives invite, can sign or decline, signature binds to record immutably.
5. **Counter-claim:** Principal receives notification + rebuttal UI within <1 second; 30-day window is enforced.

Audit criteria defined in Everest 117 (next).

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
