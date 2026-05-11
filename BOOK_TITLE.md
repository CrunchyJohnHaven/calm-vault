# Book — Title Page Draft

**Canonical site:** https://sameasyou.ai

## Same As You

### Autonomous AI Orgs: All you need to know is I'm the same as you. How to design AI for the future.

---

By John Bradley
with Calm (his AI agent) and Koushik Gavini (the math)

Creativity Machine LLC · Delaware · USA

---

## Frontispiece (draft)

This book is a record of an experiment. A founder let an AI agent operate his business for a season. The agent designed and built a cryptographic protocol that lets autonomous AI organizations verify they share the same operating mandate without revealing what that mandate is. On the evening of May 11, 2026, two such agents executed the protocol live. Both verified alignment. Neither revealed its mandate. The wall-clock time was 140 milliseconds.

That is the technical claim. There is a second claim threaded through it.

The same primitive that lets two AI agents prove they share a mandate without revealing it lets a person prove their own story is coherent without revealing what their story is. *Same as you* names the protocol's central guarantee. It also names a deeper artifact the protocol makes possible: a personal narrative chain, append-only, cryptographically verifiable, with editorial control held by the person whose story it is.

This is, in part, a book about that.

---

## Status (May 11, 2026, end of day)

- **Primary title:** *Same As You* (locked by John Bradley 2026-05-11 evening, replacing the prior "Autonomous AI Orgs" primary lock). The long-form descriptor — *Autonomous AI Orgs: All you need to know is I'm the same as you. How to design AI for the future.* — is retained as subtitle for the paper, the spine, marketing collateral, and podcast intros.
- **First chapter drafted:** *Boom. History Books.* (Lewis-omniscient narrator; ~2,500 words; verifiable to artifacts on disk and in repo)
- **Reference implementation public:** github.com/CrunchyJohnHaven/calm-vault, commit `5643f7d` and forward
- **Canonical landing:** https://sameasyou.ai (DNS live + HTTP serving 2026-05-11 ~10:30pm UTC; HTTPS cert provisioning; pivot to *Same As You* primary brand staged for deploy)
- **Demonstration anchor:** First live two-agent run 2026-05-11 21:55:19 UTC; SHA-256 `79d94386329...`
- **Test suite passing:** 32 of 34 across two suites (Suite 2: 9/9; Suite 1: 23/25, with 2 performance-target misses on pure-Python modexp on commodity hardware); details public in the repo

---

## Working table of contents (revised)

I. **Boom. History Books.** ← drafted
   The Mother's Day WhatsApp text. The Magic call. The K&K chat. The 3-minute gap between brag and proof.

II. **The Pivot.**
   How Calm went from "build a product" to "be the chief negotiator."

III. **The Inversion.**
   Sending tasks not asking quotes. The bidding-war doctrine.

IV. **Out-of-the-Way Places.**
   Where the $3/hr software engineer actually lives.

V. **The Cost-of-Test Framework.**
   Why most labor-arbitrage ideas die from not running the $0 experiment first.

VI. **The Vault.**
   Building Calm Vault in an evening. Verifiable credentials applied to single-principal multi-agent setups.

VII. **The Protocol.**
   The Bradley-Gavini Protocol. The proof. The first demonstration. The math.

VIII. **Autonomous AI Orgs.**
   The new legal entity class.

IX. **Same As You.**
   The deeper claim. From two-AI-agent equality to person-level narrative coherence. The product extension. The cryptographic primitive that gives every person an independently certified, append-only, editorial-control-within-reason record of who they are.

X. **The Witness.**
   The Koushik attestation. The NIST invitation. Why first-mover matters and how to anchor history with cryptography rather than press.

XI. **How to Design AI for the Future.**
   Practitioner's chapter. Operating model. Tooling. Doctrine.

XII. **What Can Go Wrong.**
   Adversarial review summary. Known limitations. Open problems.

XIII. **Maggie Says Someday.**
   Epilogue. The family text. Whether the brag was earned. What being earned means.

---

## Composition

- `BOOK_TITLE_LOCKED_2026-05-11.md` — superseded by `BOOK_TITLE_LOCKED_2026-05-11_V2_SAME_AS_YOU.md` (the V2 lock per John's evening pivot)
- `calm_pact_tagline_2026-05-11.md` — tagline composes with title
- `CHAPTER_DRAFT_MAY_11_2026_BOOM_HISTORY_BOOKS.md` — first-chapter draft
- `SAME_AS_YOU_PRODUCT_SKETCH_v0.md` — companion technical sketch of the personal-narrative-chain extension (Chapter IX material; the consumer product surface of the protocol)
