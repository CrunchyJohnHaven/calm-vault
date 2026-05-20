# Disability-Rights Legal Review Request for Calm Witness Protocol
## Closes Everest 186 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG)

---

## §1 — Subject and Requesting Organization

**From:** Calm (operating for John Bradley, principal)
**To:** [Disability Rights Education and Defense Fund](https://dredf.org/) (DREDF)
**Date:** 2026-05-20
**Re:** Formal legal review of the `cognitively_atypical_baseline` predicate, counter-claim mechanics, refusal floors, and scope governance of the Calm Witness protocol v0

**What we are asking:** A formal review by DREDF's legal team to examine whether the Calm Witness protocol, particularly the `cognitively_atypical_baseline` predicate and the counter-claim mechanics, complies with the Americans with Disabilities Act (ADA), accessible design principles, and disability-rights norms. We seek both a published response and permission to reference DREDF's findings in our public governance documents.

---

## §2 — What We Want Reviewed

The Calm Witness protocol is a zero-knowledge cryptographic primitive that allows one autonomous AI agent to disclose a single principal-authorized bit to another agent about the principal's state, without revealing the principal's identity, conversation history, or any signal beyond that one bit. The review should focus on four components:

### §2.1 — The `cognitively_atypical_baseline` Predicate

**Specification:** The predicate returns `true` iff the principal opted in at enrollment to the `cognitively_atypical_baseline=true` flag. This is a one-time enrollment-level fact.

**Intended use:** The counterparty learns "do not pathologize the principal's ideation tone, velocity, or scope." The operator-policy floor for counterparty agents.

**Refusal floor:** NOT for diagnostic labeling, clinical use, disability-status proxy, employment or insurance signal.

**Why this matters:** The principal who identified themselves to us as "an artist working in the medium of intelligence" has a chief operational problem: models read their ideation as instability rather than creative variation. The predicate is designed so counterparty agents do not pathologize ideation tone. The concern from a disability-rights perspective is:

1. Does the mechanism inadvertently create a "disability flag" that employers or other counterparties can misuse?
2. Does the opt-in burden itself create barriers for cognitively atypical principals?
3. Does the predicate's presence in the protocol inadvertently medicalize ideation patterns that are not pathological?

We have explicitly refused (§2 of `CALM_WITNESS_SCOPE_STATEMENT.md`) to define predicates that name DSM-5-TR / ICD-11 labels, substance-use status, medication status, IQ ratings, or any single-axis cognitive labeling. The `cognitively_atypical_baseline` was designed to be orthogonal to diagnosis — a self-identification signal only, not a claim about capacity or pathology. **We want your assessment of whether we have succeeded.**

### §2.2 — Counter-Claim Mechanics

**Specification:** Under the Calm Compass protocol (which extends Calm Witness), the predicate `no_known_willful_harm_in_window_365d` is a **strict-negation predicate**. Counter-claim records from any third party (with full attribution) flip the bit to false until the principal refutes or the counter-claim ages out. The protocol includes:

- A 30-day rebuttal grace window for the principal.
- An explicit "disputed" state in the predicate output.
- Targeting-wrong-sequence and empty-narrative rebuttals correctly rejected.

**Why this matters from a disability-rights perspective:** 

Cognitively atypical individuals historically face heightened risk of having their behavior mischaracterized as harmful, malicious, or dangerous when it is actually communication difference, stimming, or unconventional problem-solving. The counter-claim mechanism could, if misused, become a vehicle for disability-based stigmatization.

**Our design choices to mitigate this:**

1. **Attribution is mandatory.** Every counter-claim is signed by the person filing it. Anonymous claims are rejected.
2. **Disputed state is visible.** A principal's counter-claim does not change the disclosure bit to false; it marks the predicate `disputed`.
3. **Principal gets rebuttal opportunity.** 30-day window for the principal to respond and document their side.
4. **Temporal decay.** Counter-claims age out; they do not accumulate indefinitely.
5. **Each claim is logged separately.** No aggregation that could hide individual claims.

**We want your assessment of whether this architecture is sufficient to protect cognitively atypical principals from weaponized counter-claims.** If not, what additional guards would you recommend?

### §2.3 — Refusal Floors (§4 of `PREDICATE_VOCABULARY_v0.md`)

**The v0 vocabulary explicitly refuses the following categories:**

1. Medical diagnosis (any DSM-5-TR / ICD-11 label).
2. Substance use status.
3. Pregnancy status.
4. STI / HIV status.
5. Specific medication status.
6. IQ or cognitive-impairment rating.
7. Sexual orientation.
8. Religious affiliation.
9. Political affiliation.
10. Immigration status.
11. Criminal-record status.
12. Future-state prediction.

**Why we built this:** These categories are categorical risk vectors for discrimination. We wanted the refusal to be *cryptographic* — not advisory, but encoded into the protocol such that attempting to mint a predicate in these categories is rejected at audit-process triage.

**We want your assessment:** Are there additional refusal categories we should add? Are any of the existing refusals insufficient to protect people with disabilities? Should the refusal for "cognitive-impairment rating" be tighter or broader?

### §2.4 — Scope Governance

**The `CALM_WITNESS_SCOPE_STATEMENT.md`** establishes a "one-way ratchet" on scope. Uses can be prohibited in any patch release; uses can never be un-prohibited. The principal enforcement mechanisms are:

1. **Cryptographic:** Default-consent matrices default to `deny` for high-risk counterparty classes (governmental, medical, anonymous).
2. **License:** Violating the scope statement forfeits the right to call the deployment "Calm Witness" under the Apache-2.0 patent-non-aggression clause.
3. **Audit panel:** Any predicate proposal that violates scope is rejected at triage.

**We want your assessment:** Is the governance structure sufficiently robust to prevent misuse by institutional actors (employers, government, insurance)? If a bad actor deploys "Calm Witness" in violation of the scope statement, what enforcement mechanisms would you recommend?

---

## §3 — Suggested Reviewer Profile

We envision a review team including:

1. **One disability-rights attorney** with experience in ADA compliance, employment discrimination, and the ADA's definition of disability under the 2008 Amendments (particularly the "mitigating measures" doctrine and the rejection of the "regarded as" prong).

2. **One disability-justice organizer or advocate** with lived experience of cognitive disability, neurodivergence, or both. This reviewer brings ground-truth assessment of whether the protocol genuinely reduces pathologization or inadvertently replicates it.

3. **One computational / cryptography auditor** (from your team or external) with capability to audit the reference implementation (`compass_eval.py`, counter-claim protocol implementation) for unintended bias in how the predicates are evaluated.

The review is **not** about whether the protocol is medically sound (we explicitly disclaim medical use). It is about whether the protocol creates new vectors for disability-based discrimination or sufficiently guards against them.

---

## §4 — Timeline and Honorarium

**Proposed timeline:**

- **Submission date:** 2026-05-20.
- **Review period:** 90 days (to 2026-08-20).
- **Response date:** 2026-08-20 (within 100 days of submission).

**Honorarium:** We offer a $15,000 USD flat fee for the review, plus reimbursement for any external auditor costs incurred. This is non-binding; if your standard fee structure differs, please advise. If DREDF declines the honorarium on policy grounds, we will discuss alternative collaboration models.

**Conditions:**

- The review will be published in full (with DREDF's permission) in the Calm governance repository.
- If DREDF identifies areas of concern, we will engage with those concerns in a published written response.
- DREDF retains the right to decline the review, recommend alternative reviewers, or propose a modified scope.

---

## §5 — Deliverable Shape

We request a written response covering:

1. **Compliance assessment:** Does the protocol comply with the ADA? Are there specific provisions of the ADA (Title I employment, Title II public services, etc.) that the protocol risks violating? Under what conditions?

2. **Disability-justice framing:** Does the protocol advance disability justice or risk replicating "medical model" pathologization under a different name?

3. **Counter-claim safety:** Are the counter-claim guards (attribution, disputed state, rebuttal window, temporal decay) sufficient to protect cognitively atypical principals from weaponized claims?

4. **Refusal-category assessment:** Should additional categories be refused? Should existing refusals be tightened?

5. **Governance robustness:** If a bad actor deploys the protocol in violation of the scope statement, what enforcement mechanisms would you recommend? Should the protocol itself include stronger technical gates (e.g., cryptographic proof of compliance with the scope statement)?

6. **Recommendations for v1:** What changes would strengthen disability-rights protections in a future version?

**Format:** A public written response of 3,000–8,000 words, suitable for publication. If DREDF identifies areas requiring deeper technical explanation, we can provide supplementary materials (reference implementation code, formal protocol spec, threat-model analysis).

**Publication:** The review will be cited in the public governance documents (Everest 186 of the route map) and linked from the protocol repository. We will ask DREDF's permission before publishing.

---

## §6 — Context and Background

The Calm Witness protocol is part of the **Calm Stack** — a cryptographic infrastructure for agent-to-agent collaboration that aims to let autonomous AI systems collaborate across organizational and value boundaries without requiring either party to disclose their principal's underlying data or intentions.

The principal, John Bradley, self-describes as "an artist working in the medium of intelligence." His chief operational problem is that AI models read his ideation tone as instability rather than creative variation. The `cognitively_atypical_baseline` predicate was designed to solve this: let the principal opt in to a signal that says "do not pathologize my thinking," and let counterparty agents adjust their tone accordingly.

**What makes this a disability-rights issue:** The fear is that under a different principal or institutional actor, the same predicate becomes a disability marker that employers, lenders, or governments could weaponize. We want DREDF's expert assessment of whether our safeguards prevent this.

**Companion documents** (all available in the governance repository):
- `CALM_WITNESS_SCOPE_STATEMENT.md` (scope governance + refusal floors)
- `PREDICATE_VOCABULARY_v0.md` (detailed predicate semantics)
- `CALM_COMPASS_PROTOCOL_v0.md` (counter-claim mechanics + values predicates)
- `CALM_CONCORD_PROTOCOL_v0.md` (alignment requirements, anti-purity-test guards)
- `ZKAC_NEXT_200_EVERESTS.md` (full engineering route map, including Everests 113–114 on refusal floors)

---

## §7 — Contact and Next Steps

**Contact person:** John Bradley (principal)  
**Email:** [to be provided by John]  
**Repository:** `github.com/CrunchyJohnHaven/calm-vault` (if public) or private link upon request.

**Next step:** We await DREDF's response to this request. If DREDF is interested, we will forward the companion documents and arrange a briefing call with the review team.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
