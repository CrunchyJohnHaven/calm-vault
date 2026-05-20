# Calm Witness — Principal Onboarding Animation v0 (S249)

**REVIEW-NEEDED FLAG:** This script requires review by ≥2 non-technical reviewers before final production. Reviewer sign-off blocks must be completed prior to storyboard lock.

**Total target runtime:** ≤90 seconds  
**Voiceover word count:** ~175 words  
**Reading level target:** 8th grade or lower (Flesch-Kincaid; see note at end)  
**Forbidden voiceover terms:** cryptographic, Pedersen, Sigma-protocol, zero-knowledge proof, hash (in technical sense)  
**Signed:** CALM 2026-05-20

---

## Scene 1 — Introduction [0:00–0:12]

**Visual:** A simple room. A person sits at a desk, looking at a tablet. The screen glows softly. No faces shown — silhouette style, calm color palette (slate blue, warm white).

**Voiceover:**
"You're about to enroll in something called Calm Witness. Before you do, we want to show you exactly what it does — and what it doesn't do."

**On-screen text:** "Calm Witness — What you're signing up for."

---

## Scene 2 — What Gets Recorded [0:12–0:30]

**Visual:** A small journal appears on screen. The person writes a short line in it — a daily check-in. The journal snaps shut and floats into a locked box labeled "Your Vault." The box stays on the principal's side of the screen. No wire, no upload arrow.

**Voiceover:**
"You keep a short daily record — just a few sentences about how you're doing. That record lives in your vault, on your side. No one else can read it. You can also add a writing sample once, so your own voice is on file. That part is optional."

**On-screen text:**
- "Your daily check-in"
- "Stays in your vault"
- "Optional: one writing sample"

---

## Scene 3 — What the Other Side Sees [0:30–0:52]

**Visual:** The locked box is on the left. A counterparty — a business figure, faceless — stands on the right. A thin wire runs between them. Along the wire, a single small card travels: one side shows "Yes" or "No." Nothing else crosses the wire. The journal and box never move.

**Stage direction:** The "card" is a Pedersen commitment opening to a single bit; the Sigma-protocol proof travels alongside but is rendered as a sealed envelope, invisible to the counterparty panel. Do not label these in the animation.

**Voiceover:**
"Think of a bank teller passing a note through a slot. The note says one thing: 'Yes, this person meets the condition' — or 'No, they don't.' The teller never hands over your file. The other side only ever gets that one answer. Not your words. Not your records. Just: yes or no."

**On-screen text:**
- "The other side receives: one answer"
- "YES or NO — nothing else"

---

## Scene 4 — How You Opt In or Out [0:52–1:07]

**Visual:** A simple toggle switch on the tablet screen. The person taps it on — a green checkmark appears. Then taps it off — the checkmark disappears, the wire dissolves. The vault stays put, unchanged.

**Stage direction:** Opt-out revokes the commitment key for that counterparty; vault records are retained locally per retention policy unless principal also triggers full purge (separate flow, not shown here).

**Voiceover:**
"You choose to enroll — and you can stop at any time. Turning it off means no more answers go out. Your records stay in your vault either way. You're in control."

**On-screen text:**
- "Enroll anytime"
- "Opt out anytime"
- "Your vault is yours"

---

## Scene 5 — What You Can Audit [1:07–1:22]

**Visual:** The person opens the vault on the tablet. A clean log appears: date, what answer was sent, to whom. Each row is readable at a glance. The person scrolls through calmly.

**Voiceover:**
"You can review a log of every answer that was ever sent on your behalf — who asked, what the answer was, and when. Nothing hidden on your end."

**On-screen text:**
- "Your audit log"
- "Every answer, every date, every recipient"

---

## Scene 6 — Close [1:22–1:30]

**Visual:** Vault closes gently. Title card fades in on clean background.

**Voiceover:**
"That's Calm Witness. Your record, your vault, one answer at a time."

**On-screen text:** "Calm Witness — Your record. Your control."

---

## Reading-Level Note

Target: Flesch-Kincaid Grade 8 or below. Voiceover draft scores approximately FK Grade 6.8 (estimated). Sentence length kept under 20 words on average. All technical terms confined to stage directions. "Bank-teller-note" analogy used in Scene 3 as the primary lay bridge concept. Final voiceover must be re-scored after any edits.

---

## Review-Needed Flag

**Status: OPEN — production blocked pending reviewer sign-off.**

| Reviewer | Role | Date Reviewed | Approved |
|---|---|---|---|
| [Reviewer 1] | Non-technical stakeholder | | |
| [Reviewer 2] | Non-technical stakeholder | | |

Reviewers: confirm (a) voiceover is clear without prior knowledge, (b) no jargon survives, (c) bank-teller analogy lands, (d) opt-out flow is unambiguous.
