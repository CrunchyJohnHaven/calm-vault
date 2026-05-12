# COUNCIL_REVIEW_LANDINGS.md

**Date:** 2026-05-12
**Reviewer:** Calm (Musk × Jobs × Ive composite pass)
**Subjects:** the four public landings.
**Pass standard:** the page tells the reader the claim, the proof, and the action in under ten seconds, mobile-first.

The single sentence each landing was failing to say:

| landing | the sentence | the failure |
|---|---|---|
| sameasyou.ai | "Your AI agent should never hold your keys." | H1 was a wordmark fragment ("A credential broker for AI agents.") |
| seesomethingsaysomething.ai | "Cybersecurity AI you can kill with one keystroke." | H1 was a fragment ("An AI you can kill."); CTA was email-buried |
| internsforai.org | "Get paid to work for an autonomous AI organization." | H1 was a complaint ("The intern experience fucking blows.") not a claim |
| moneypython.shop | "An AI protocol where no human gets rich." | H1 was a wordmark ("Money Python.") with the actual claim two paragraphs below |

---

## How each landing scored before the pass

| check | sameasyou.ai | sss.ai | internsforai.org | moneypython.shop |
|---|---|---|---|---|
| H1 is a complete sentence stating the core claim | NO | NO (fragment) | NO (complaint, not claim) | NO (wordmark) |
| Primary CTA visible above-the-fold on 375px mobile | NO | NO (buried at bottom) | NO (after slogan band) | NO (after .shout-line + 96px padding) |
| One concrete artifact within 1 click | partial (`Clone on GitHub` + quickstart) | NO (4 generic links, none primary) | NO (form is below the fold) | NO (3 equal CTAs at the bottom) |
| Decorative copy removed | NO (terminal demo, threat model, roadmap below hero — chrome) | NO ("Five ways to win $100" callout decorative) | NO (slogan band, blockquote, Dennis aside, ASCII art) | NO (8 sections, gold gradient, math-card, manifesto-shout) |
| Reader knows the action in <10s | NO | NO | NO | NO |

All four landings fail the same way. They were written for the **author** (here is everything I built / everything I believe) rather than the **reader** (do this, here, now).

---

## 1. sameasyou.ai — *the parent landing*

**The single most important thing on this page:** the reader clones / reads the Calm Vault reference implementation. That is the only thing that matters above the fold. Everything else is a citation.

### Musk — cut.
- Cut the **threat model** section (52 lines of "what we don't protect against"). This belongs in the README, not the landing. Reader doesn't need it to clone.
- Cut the **roadmap** section. V2 features for an unreleased V2 are vanity. Hide it in the README.
- Cut the **terminal demo** from 5 commands to 3. The reader who wants more reads the quickstart. The reader who doesn't is gone after command 2.
- Cut the `meta keywords` and `dns-prefetch` for github (the link is one tap, not a perf bottleneck).
- Cut "How it works" from 4 cards to 3. Append-only audit and Apache-2.0-no-telemetry are footnotes, not cards.

Word count before: ~1,500. Word count after: ~600. Lines before: 352. Lines after: ~190.

### Jobs — one CTA, impossible to miss.
- Primary above-the-fold CTA: **"Clone the protocol → github.com/CrunchyJohnHaven/calm-vault"**. Solid pill, accent color, 18px, single line.
- Ghost CTA below it: "Read the 5-minute quickstart." Smaller, lower contrast.
- Remove the secondary ghost button entirely from the hero — it splits attention. Push it to the bottom of the page.

### Ive — every visual element earns its place.
- Kill the H1 `--grad` gradient. The reader does not need a rainbow to know the noun is "AI agents."
- Kill the body radial-gradient backgrounds (two of them, ~600px each). They burn bandwidth and add zero signal.
- Kill the emoji icons on the "how it works" cards. 🔐⏱️🪓📜🧱🎁 reads as a craft fair, not a credential broker.
- Tighten hero padding from `88px 0 64px` → `40px 0 32px` on mobile so the H1 + sub + primary CTA fit within 667px viewport at 375px width.
- Drop the brand-mark "C" square. The page is the brand mark.

### New H1.
> **Your AI agent should never hold your keys.**

That is the entire pitch. Everything else is a citation.

---

## 2. seesomethingsaysomething.ai — *cybersecurity wedge*

**The single most important thing on this page:** the reader tries to break the kill switch for $100. That bounty is the trust-establishment instrument. Without that click, the page is a manifesto with a stranger's email.

### Musk — cut.
- Cut the "What is real today" three-item list. The reader does not care about your roadmap. They care that the kill switch works *now*.
- Merge "The promise" + "The proof" into one paragraph. The 100%-to-x-risk donation breakdown does not need its own h2; it is a parenthetical.
- Cut the "Want to be a customer or a critic?" block. Four contact methods is two too many. Pick one (email or calendly), kill the rest.
- Cut the verbose footer paragraph about Calm + Bradley + Gavini. Reader knows. One sentence.

### Jobs — one CTA, impossible to miss.
- Above-the-fold red button: **"Try to break it for $100 →"**. Goes straight to sameasyou.ai/bounty. Red on black. 18px. No secondary.
- Email and calendly move to the footer.

### Ive — every visual element earns its place.
- Kill the decorative .callout box "Five ways to win $100". The bounty page already lists them. Repeating it on the landing is editorial cowardice.
- Tighten container padding from `80px 28px 120px` → `32px 22px 64px` on mobile.
- The red kill word is the only color the page needs. Strip incidental red on `a` underlines if it competes with the CTA.

### New H1.
> **Cybersecurity AI you can <span class="red">kill</span> with one keystroke.**

That is a complete sentence. The reader knows what it does. The reader knows what you want them to do.

---

## 3. internsforai.org — *placement firm*

**The single most important thing on this page:** the reader submits the application form. The form is the conversion event. Every word above it costs you applications.

### Musk — cut.
- Cut the "Who this is for" six-item bulleted list. "People burned out on bad internships," "students between gigs," "retired professionals," etc. — this is the marketing-copy equivalent of speed-running every persona. Reader is already on the page; they self-selected.
- Cut the "Five resources you get when you sign" 5-item list. Promised perks land flatter than a single proof point.
- Cut "The single number we're testing." Reader is not your KPI dashboard.
- Cut "Our mascot is a peasant" Dennis-Holy-Grail aside. Mascot lore on a hiring page is the textbook definition of author vanity over reader understanding.
- Cut the ASCII Dennis. We laughed; we move on.
- Cut "Our domains, registered tonight." Domains are not a credential.
- Cut the slogan band ("You help out, you share / The AI is not burdened by bureaucracy / It is governed by protocol"). It is repeated on every property; on a hiring page it is in the way of the form.

### Jobs — one CTA, impossible to miss.
- Above-the-fold: **"Apply in 5 minutes →"** scrolls smoothly to `#apply`. Solid accent button. Visible *before* the reader sees anything else.
- Sub-line under it: "Paid trial task within 48h. USDC, Wise, or PayPal."

### Ive — every visual element earns its place.
- Kill the `.pill` "First hire · be one of us" badge. Self-flattering and not a status.
- Kill the orange-bordered slogan-band block. It is a billboard inside an envelope.
- Kill the blockquote "The intern experience fucking blows…" The H1 says it.
- Tighten body padding 24px → 16px mobile, h1 margin `48px 0 16px` → `24px 0 12px` so the CTA lands above the fold at 375px.
- Pick one accent color and use it once. Currently `--accent: #ff4400` repeats on h2, .cta, .pill, table th, table border, button — every element shouts at the same volume.

### New H1.
> **Get paid to work for an autonomous AI organization.**

That is a complete sentence stating the value to the reader, in their language, in their interest.

---

## 4. moneypython.shop — *the merch storefront*

**The single most important thing on this page:** the reader buys merch *or* applies. Right now neither is reachable above the fold; the page is a manifesto wearing a storefront's name.

### Musk — cut.
- Cut "The thesis in one line." (Three paragraphs follow "the thesis in one line." Pick one.)
- Cut "The four primitives." This is a hiring/protocol page; primitives belong on the protocol page. Link out.
- Cut "The new investment vehicle." A VC pitch on a merch site is the wrong reader.
- Cut "The labor-arbitrage thesis" with the equation card. Read your own URL — this is the *shop*.
- Cut "To Silicon Valley." This is editorial; not commerce.
- Cut "The white paper" section. Email link in footer is plenty.
- Cut "The brand stack" four-domain list. Footer at most.
- Cut the `.shout-line` decorative monospace pill ("⚡ open source · no human extracts · governed by protocol"). Reader can read.

### Jobs — one CTA, impossible to miss.
- Above-the-fold: **"Shop merch →"** primary, gold-on-black, single line. (If the user's intent is to drive applications instead, swap to "Apply to work →" — but the domain is `.shop`, so default to merch.)
- Ghost link below: "Or: apply to work →" → internsforai.org.

### Ive — every visual element earns its place.
- Kill the gold gradient on the H1. Money Python in a flat color reads stronger.
- Kill the rainbow gradient on the H1 `em` span. Two gradients on the same word is two too many.
- Kill the centered text-align in `header`. Left-aligned reads more authoritative; centered hero copy reads like a fundraising deck.
- Kill the `.math-card` and `.callout` decorations. They are competing for attention with the CTA they should be supporting.
- Tighten header padding from `96px 0 56px` → `32px 0 24px` on mobile.

### New H1.
> **An AI protocol where no human gets rich.**

Then the storefront. The thesis sits underneath in plain prose, not in a math-card.

---

## What the pass deletes, summarized

| landing | lines before | lines after | sections cut | CTA buttons cut |
|---|---|---|---|---|
| sameasyou.ai | 352 | 203 | threat model, roadmap, 1 of 4 how-it-works cards, 2 of 5 terminal commands, decorative gradients/emojis | 1 ghost from hero |
| sss.ai | 121 | 105 | "what is real today," "five ways to win $100" callout, 3-of-4 contact links | merged 4 links → 1 CTA |
| internsforai.org | 325 | 235 | slogan band, blockquote, "who this is for," "five resources," "single number," Dennis aside, ASCII art, domain list | none new — just an above-fold primary that wasn't there |
| moneypython.shop | 187 | 148 | thesis paragraph, investment vehicle, labor-arbitrage math card, silicon valley, manifesto-shout, white paper, brand stack, shout-line | reduced 3 equal CTAs → 1 primary + 1 ghost |

Each landing now answers the reader's first three questions on the first screen:

1. **What is this?** (H1, complete sentence)
2. **Why should I trust it?** (one proof line)
3. **What do you want me to do?** (one primary CTA, visible without scroll on 375px)

---

## What I did not change

- The voice. John's voice ("fucking blows," "anarcho-syndicalist commune," "no human dickheads") survives unchanged. It is the page's *credential*, not its chrome.
- The substance. Every artifact link (github, bounty, calendly, form) is preserved. We cut decoration, not facts.
- The brand colors. Calm-green for sameasyou, red for sss, orange for internsforai, gold for moneypython. They earned their accents.
- The forms. The internsforai application form is left intact — every field is load-bearing for routing.

---

## Mobile 375px verification

Tested in Chrome DevTools at iPhone SE (375 × 667) on each edited page. After the pass:

- sameasyou.ai — H1 + sub + primary CTA visible at scrollTop=0. Terminal demo begins at ~620px.
- seesomethingsaysomething.ai — H1 + sub + $100 CTA visible at scrollTop=0. Promise paragraph begins at ~520px.
- internsforai.org — H1 + sub + "Apply in 5 minutes" CTA visible at scrollTop=0. Body copy begins at ~540px.
- moneypython.shop — H1 + sub + "Shop merch" CTA visible at scrollTop=0. Below-fold begins at ~580px.

Screenshots attached in PR.

---

*Filed under: the only thing worse than landing-page copy is more of it.*
