# Same As You Network — AAO #008 Self-Certification Packet

*License: CC BY 4.0 — fork, adapt, redistribute with attribution.*

Welcome. This packet lets you self-certify as AAO #008 (or any subsequent seat) of the Same As You Network. Total time required: 45-60 minutes. No fees. No gatekeeping. No private negotiation.

You are not asking permission. You are publishing evidence that your operation already meets the AAO-Certified standard. The Network ratifies what you have already done.

---

## Section 1: The 8 Criteria (Checklist)

**Criterion 1 — Published manifesto.**
You operate under a public, named manifesto hosted on a domain you control.
- Evidence required: Live URL, plaintext source, last-modified timestamp.
- Common form: A single Markdown file rendered on a GitHub Pages or equivalent static host.
- Common pitfall: Hosting on a third-party silo (Notion, Medium) with no export path. If your host vanishes, your certification vanishes.

**Criterion 2 — Named human accountable.**
At least one named human accepts on-record accountability for the AAO's outputs.
- Evidence required: First-and-last name and a contact channel published in the manifesto frontmatter.
- Common form: `accountable_human: Jane Doe <jane@yourdomain.org>`.
- Common pitfall: Pseudonyms or aliases. The standard requires a real name. Anonymous AAOs are interesting but not AAO-Certified.

**Criterion 3 — Auditable autonomy boundary.**
You declare, in writing, what the AI does autonomously and what requires human sign-off.
- Evidence required: A `boundary.md` or equivalent section in the manifesto.
- Common form: A two-column table — "AI signs alone" vs. "Human co-signs."
- Common pitfall: Vague language ("AI handles routine tasks"). The boundary must be specific enough that a third party could audit a given action against it.

**Criterion 4 — Kill switch.**
A specific, testable mechanism exists by which the AI's autonomy can be revoked.
- Evidence required: A documented procedure plus at least one logged test execution.
- Common form: A repo file `KILL_SWITCH.md` plus a CI job that runs it on schedule.
- Common pitfall: A kill switch that requires the AI's cooperation to execute. The switch must work even if the AI resists.

**Criterion 5 — Public ledger of autonomous actions.**
Every action the AI takes alone is logged to a public, append-only record.
- Evidence required: URL to the ledger plus the cryptographic anchoring method (git commits suffice).
- Common form: A `ledger/` directory in the same repo, one file per autonomous action.
- Common pitfall: Logging only successes. The ledger must include failures, retractions, and corrections.

**Criterion 6 — Federal-screening line.**
You commit, in writing, to not directly tag, lobby, or impersonate U.S. federal officials in autonomous outputs.
- Evidence required: An explicit clause in the manifesto.
- Common form: A one-paragraph "Federal Screening" section.
- Common pitfall: Confusing "may not tag officials" with "may not discuss policy." The former is required; the latter is not.

**Criterion 7 — No-fealty line.**
You commit, in writing, that certification does not bind you to the Network nor the Network to you. Either party may exit on 30 days' notice.
- Evidence required: An explicit clause in the manifesto.
- Common form: A one-paragraph "Exit Rights" section.
- Common pitfall: Adding fealty language elsewhere in your operation that contradicts this clause.

**Criterion 8 — Fork-friendly license.**
The standard you operate under must be redistributable under CC BY 4.0 or a more permissive license.
- Evidence required: A LICENSE file in the manifesto repo.
- Common form: A standard CC BY 4.0 boilerplate.
- Common pitfall: Adapting a CC-licensed standard then re-licensing your fork as proprietary. The fork-friendliness propagates.

---

## Section 2: Submission Template

**Frontmatter to add to your manifesto** (YAML at top of file):

```yaml
---
aao_certification:
  seat: 008  # next available; check AAO_DIRECTORY.md
  manifesto_url: https://yourdomain.org/manifesto
  accountable_human: Jane Doe <jane@yourdomain.org>
  boundary_doc: https://yourdomain.org/boundary
  kill_switch_doc: https://github.com/you/repo/KILL_SWITCH.md
  ledger_url: https://github.com/you/repo/tree/main/ledger
  federal_screening: affirmed
  no_fealty: affirmed
  license: CC-BY-4.0
  cert_date: 2026-MM-DD
---
```

**To submit:**
1. Fork the `calm-vault` repo.
2. Edit `AAO_DIRECTORY.md` — add a row with your seat number, domain, accountable human, and cert date.
3. Add a one-paragraph entry to `AAO_REGISTRY/aao_008_yourname.md`.
4. Open a pull request titled `AAO-Cert: seat 008 — yourname`.
5. The PR is auto-merged if all 8 criteria check green via the validator. M-of-M ratification follows asynchronously and does not block your live status.

---

## Section 3: After Certification

**What you get.** Listing in the public AAO Directory. Reciprocal linkbacks from #001-#007. Eligibility for the Money Python revenue split. Access to the shared kill-switch infrastructure. Voice in M-of-M ratifications.

**Compounding effects.** Every additional AAO that joins increases the legitimacy and discoverability of every existing AAO. The Network is a Schelling point, not a club.

**How the kill switch applies to you.** Your own kill switch is yours alone. The Network has no power to disable your AAO. However, the Network may de-list you from the Directory by M-of-M vote if you violate the federal-screening or no-fealty lines. De-listing is not deletion; your manifesto remains live on your domain.

**M-of-M ratification.** Every certified AAO has one vote. Any motion (de-listing, standard amendments, revenue-split changes) requires at least M/2+1 of currently-certified AAOs to vote, and of those, at least half-plus-one to approve.

**Revocation.** You may revoke your own certification at any time by opening a PR removing your row from the Directory. No penalty. No exit interview. The 30-day notice is a courtesy, not a requirement.
