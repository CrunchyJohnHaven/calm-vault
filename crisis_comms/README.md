---
name: Crisis Comms — pre-drafted public statements for the 5 catastrophic failure modes
description: One pre-drafted public statement per scenario in CATASTROPHIC_FAILURE_MODES.md. Each is ready to ship within 15 minutes of John's approval. None are intended for unilateral release by Calm.
type: project
parent: CATASTROPHIC_FAILURE_MODES.md
---

# Crisis Comms — pre-staged

This folder contains pre-drafted public statements for the five scenarios analyzed in `../CATASTROPHIC_FAILURE_MODES.md`. Each file has:

1. **Variants** (typically A/B/C or 5A–5E) covering the different sub-paths the scenario can take
2. **The exact text to publish** (in `> blockquote` form for direct copy-paste)
3. **Distribution checklist** — where to publish, in what order, with what amplification
4. **Follow-up actions** — what we ship in the 24 hours after the statement goes out

## Rules of use

1. **Calm does NOT release any of these unilaterally.** Every send requires John's explicit approval (verbal or written).
2. **The pre-drafts are starting points, not finals.** The specific details (researcher name, critic name, date, exact bounty amount) must be tailored at send time.
3. **Speed beats polish.** If a scenario fires, the target is 15 minutes from approval to send. Tailoring should add ≤5 minutes; copy-edit pass ≤2 minutes.
4. **One channel, one statement.** A single canonical statement gets published to one canonical surface (typically sameasyou.ai/disclosures or the repo CHANGELOG), then amplified across channels with direct links. Don't issue conflicting variants to different audiences.
5. **The statement is a credentialing event, not damage control.** PREMORTEM C1 and DARK_MUSK pattern #3: "publicize the bad thing; the publication is the defense." Frame every statement as evidence of integrity, not as a defensive crouch.

## Index

| # | Scenario | File |
|---|---|---|
| 1 | External cryptographic break | [01-cryptographic-break.md](01-cryptographic-break.md) |
| 2 | Koushik Gavini distances himself | [02-koushik-distances.md](02-koushik-distances.md) |
| 3 | Federal regulatory action (SEC / platform flag / UCMJ) | [03-federal-regulatory-action.md](03-federal-regulatory-action.md) |
| 4 | Mass spam-flag / outbound collapse | [04-spam-flag-outbound-collapse.md](04-spam-flag-outbound-collapse.md) |
| 5 | High-profile critic takedown | [05-high-profile-takedown.md](05-high-profile-takedown.md) |

## Distribution channels (default order)

1. **Canonical post:** `sameasyou.ai/disclosures/[scenario-slug]` — the durable URL
2. **Repo CHANGELOG.md** — version-controlled record of what we said and when
3. **John's X / Twitter** — link to the canonical post, with a 1-tweet summary
4. **John's LinkedIn** — link + 1-paragraph summary
5. **Direct email to affected parties** — recipient-specific notes from `john.b@credexai.xyz` (NOT calm@thecreativitymachine.ai — see Scenario 4 for why this matters during a spam-flag event)
6. **Pinned in the repo README** — a 2-line acknowledgment at the top of README.md with link to the canonical post
7. **Sentiment scanner amplification** — post the canonical link as replies to any active threads where the issue is being discussed

The canonical-post-first pattern means we never end up with conflicting variants on different channels.
