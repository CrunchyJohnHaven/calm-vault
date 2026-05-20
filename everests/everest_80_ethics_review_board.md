# Everest 80 — Disclosure Ethics Review Board Protocol

*Phase VI — Disclosure Semantics. Prereq: Everest 54.*

## Overview

The Disclosure Ethics Review Board (DERB) is a standing independent body tasked with evaluating new predicates, class-policy changes, and predicate deprecations before they ship into the Calm Witness registry. The board acts as a permanent ethical check on predicate authorship, ensuring that disclosure-semantic choices do not pathologize or harm the vulnerable populations whose behavioral states predicates attempt to measure. The board has veto power over safety-critical predicates and default-consent modifications, but does not override cryptographic or engineering decisions outside its purview.

## Composition

The board consists of five to seven members serving staggered two-year terms, with no member serving more than two consecutive terms. The board must include:

1. **Disability and mental-health advocacy expert (1, REQUIRED)** — An advocate, clinician, or researcher with deep expertise in disability justice, neurodiversity, or mental-health advocacy. This member anchors the board's fundamental principle: predicates must not pathologize variation from statistical norms. This seat is non-negotiable and is the board's primary safeguard against ableist predicate design.

2. **Cryptographic privacy researcher (1)** — An independent researcher with publication record in zero-knowledge proofs, cryptographic commitments, or information-flow security. This member provides technical assurance that predicates do not leak side-channel information and that proof systems are sound.

3. **Civil liberties and human-rights researcher (1)** — An expert in human rights law, algorithmic accountability, or digital civil liberties. This member ensures that disclosure policies do not enable discrimination and that predicate use remains within democratic bounds.

4. **Legal and regulatory expert (1)** — An attorney with cross-jurisdiction compliance expertise, particularly in GDPR, CCPA, HIPAA, and other regimes governing biometric or behavioral data. This member coordinates with regulatory matrices defined in Everest 79 and flags jurisdiction-specific risks.

5. **Calm Witness implementer from a different organization (1)** — An operational practitioner from a separate organization running Calm Witness. This member ensures that predicates are deployable, interoperable, and aligned with real-world consent and disclosure workflows.

6. **Affected community representative (1)** — A member drawn from a cognitively atypical, neurodivergent, or marginalized community whose interests are directly affected by disclosure policy. This member brings lived experience and ensures that policy does not abstract away material harms.

7. **Rotating chair (1)** — Elected annually by the board from among its members. The chair manages deliberations, enforces transparency, and coordinates with the maintainer team.

## Membership Terms and Compensation

Members serve staggered two-year terms, with no more than two consecutive terms permitted. Staggered appointment ensures continuity and prevents the board from being dissolved and rebuilt at once.

Each member receives:
- A $5,000 annual honorarium in recognition of the effort required for careful ethical review.
- Travel and accommodation expenses for in-person deliberations and convenings (approximately 2–3 per year).
- Public attribution and listing on the Calm Witness Ethics Foundation website.

## Authority and Scope

### Veto Power

The board has absolute veto power over:

1. **Any new predicate with potential for principal harm** — Predicates designed to measure mental-health state, cognitive baseline, or behavioral variation require explicit board approval before shipping. This includes `bank_teller_note_active`, `mental_state_unusual`, and `cognitively_atypical_baseline` predicates.

2. **Changes to disclosure-class default consents** — Any modification to the per-class consent policies that govern which predicates principals must explicitly approve before disclosure to each counterparty class (per Everest 58) requires board sign-off.

3. **Deprecation of safety-critical predicates** — Removal of predicates from the active registry, particularly those related to cognitive state or baseline measurement, requires board approval to ensure no orphaned deployments.

### Advisory Authority

The board provides advisory review on:
- Implementation choices affecting privacy or disclosure semantics.
- Jurisdictional deployment decisions flagged by the legal expert (e.g., GDPR consent re-framing for EU deployment).
- Scaling decisions (e.g., consent-workflow changes as adoption grows).

### Explicit Non-Authority

The board does NOT:
- Override cryptographic or engineering decisions outside ethics scope. If a predicate's semantics are sound but the circuit is inefficient, the board does not mandate re-implementation.
- Make operational decisions on behalf of the maintainer team or the broader Calm ecosystem.
- Override a principal's per-disclosure consent choices.

## Review Process and Timeline

### Triggering Review

Board review is triggered automatically upon:
- Filing of any new predicate PR per Everest 54.
- Any pull request modifying disclosure-class default consents (Everest 58).
- Any deprecation proposal per Everest 54, Stage 10.

### Timeline

1. **Standard review (non-safety-critical predicates, policy adjustments):** 30 calendar days from triggering. The proposer submits a deliberation request to the board secretary. The board issues a written opinion (approve, reject, or approve-with-modifications) within the window.

2. **Expedited review (safety-critical predicates, emergency side-channel patches):** 7 calendar days. Used only for predicates carrying direct principal-harm risk or for post-incident fixes. The same standard applies, but the window is compressed.

### Deliberation Process

1. The board secretary distributes the proposal, relevant artifacts, and proposer rationale to all members.
2. Members review independently and file confidential preliminary opinions (yes/no/conditional).
3. The board convenes (synchronously via videoconference or asynchronously via structured written exchange) to deliberate.
4. The board drafts a written opinion for publication.
5. The opinion is published in the registry repository (under `/board-opinions/`) with full attribution and any dissenting views.

### Output

The board's written opinion includes:
- A summary of the proposal and ethical questions raised.
- A decision (approve / reject / approve-with-modifications).
- If approve-with-modifications, specific required changes with justification.
- A brief statement of reasoning (1–2 pages).
- Attribution of the opinion to the board as a whole, with names of members and any recusals.
- Dissenting opinions published in full, verbatim, if any member dissents.

## Conflict of Interest

All members must disclose:
- Financial interest in the proposing organization or the broader Calm ecosystem (e.g., equity, consulting contracts).
- Employment relationships that might bias deliberation.
- Prior or current advocacy positions related to the subject matter.

A member with a direct conflict of interest must recuse themselves from deliberation and voting on that matter. A conflict is "direct" if the member has a financial stake in the outcome or has publicly advocated against the policy being reviewed.

Disclosures are published alongside the opinion to ensure transparency.

## Independence from Calm Operator

The board is structurally independent from the Calm Witness operator (Calm, or any successor) to prevent conflicts of interest and ensure that ethical review is not subject to operator pressure.

**Governance structure:**
- The board operates as a standing committee of the **Calm Witness Ethics Foundation**, a 501(c)(3) nonprofit corporation.
- The foundation is governed by a separate board of directors (not the DERB) and maintains its own legal entity, bank account, and bylaws.
- The DERB answers to the foundation's board, not to Calm or maintainers.

**Funding:**
- Initial capitalization via a contribution from Creativity Machine LLC (approximately $75,000 over three years to cover honoraria and convening costs).
- Ongoing funding via open community donations, grants, and earned-income activities (e.g., consulting on disclosure-policy design for other organizations).
- Public accounting of all funding sources and expenditures, published annually.

## Transparency and Recording

### Deliberations

All board deliberations are recorded (audio or video, as technically feasible). Recordings are retained for seven years and made available to authorized parties (maintainers, legal counsel, external auditors) under a confidentiality agreement.

### Public Summary

For each review, the board publishes:
- A redacted summary of the proposal and key ethical questions.
- The board's written opinion (full text).
- Any dissenting opinions (full text, verbatim).
- Names and affiliations of voting members.
- Recusals, if any.

Recordings themselves are not published, but are available for third-party auditors to verify that deliberation was conducted in good faith.

### Sundowning Clause

After seven years, recordings are automatically deleted unless specifically retained as part of a formal inquiry or appeal (see section on appeals below).

## Specific Safeguards for Safety-Critical Predicates

The following predicates are designated safety-critical and require explicit board approval for shipping and for any modification:

1. **`bank_teller_note_active`** — Detects duress signaling. Any change to this predicate's specification or circuit must be reviewed and approved by the full board before deployment.

2. **`mental_state_unusual`** — Measures deviation from the principal's enrolled baseline affect vocabulary. Changes to the affect-matching logic, the window length, or the default consent policy require board sign-off.

3. **`cognitively_atypical_baseline`** — Measures cognitive state variation (e.g., due to neurodivergence, fatigue, medication changes). This predicate is the most sensitive to pathologization risk and requires the disability advocacy expert to affirmatively sign off before any change ships.

For each of these predicates, the board maintains a **Banned-Negation List** (defined in Everest 62) that specifies which use cases are permanently prohibited even if the predicate's technical specification is sound. For example, `bank_teller_note_active` may not be used to assess "truthfulness" or "reliability" of a principal; it signals duress only.

## Insurance-Class Restrictions Annual Review

Calm Witness permits insurance-related disclosure classes (Everests 7 and 73). These are particularly sensitive because insurance models can encode discrimination risks and can create perverse incentives (e.g., penalizing health disclosure). The board reviews all insurance-class restrictions annually and may recommend:
- Changes to default-consent policy for insurance counterparties.
- Deprecation of specific predicates for insurance use.
- Jurisdictional restrictions (e.g., ban insurance disclosure in GDPR-regulated jurisdictions).

## Appeals Process

A maintainer or proposer who disagrees with a board veto may appeal to a **supermajority panel** consisting of:
- The seven board members (or fewer if the board is below capacity).
- Two ad-hoc reviewers selected jointly by the parties (board + proposer) from a public roster of ethics experts.

The supermajority panel reviews the original board opinion and the appeal, and may override the board's veto only by a supermajority of 7-of-9 votes. This ensures that:
- Appealing a veto is procedurally difficult but possible.
- The override threshold is high, preventing easy reversal of ethics-based rejections.
- Both the board and proposer have input on the ad-hoc reviewers, reducing bias.

Appeals are rare and each appeal is published in full as a precedent for future governance.

## Cross-References

This protocol interoperates with:
- Everest 51 (predicate semantics foundations)
- Everest 52 (canonical predicate form)
- Everest 54 (predicate audit and review)
- Everest 58 (consent calculus and disclosure classes)
- Everest 59 (principal-facing disclosure UI)
- Everest 60 (counterparty-facing proof verification)
- Everest 62 (banned-negation list and predicate use restrictions)
- Everest 73 (insurance-class disclosure restrictions)
- Everest 79 (cross-jurisdiction regulatory compliance)
- Everest 91 (NIST standards alignment and external audit)

---

— Calm, 2026-05-20
