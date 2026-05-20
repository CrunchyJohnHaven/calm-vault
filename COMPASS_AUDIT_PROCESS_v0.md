# Calm Compass Audit Process v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 115 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Extends [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) §9 for Compass predicates and evidence kinds.**
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md), [`COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md`](COMPASS_VALUES_EVIDENCE_TAXONOMY_v0.md), [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md).**

## §1 — Scope

This document specifies the extended process for **proposing, reviewing, accepting, and deprecating** entries in the Calm Compass values predicate vocabulary and evidence kinds. Every active Compass predicate ID in `compass_predicates_v0.json` and every evidence kind in the taxonomy must have followed this process or been minted as part of the v0 founding catalog (Everest 103 release).

The Compass audit process extends the Calm Witness predicate audit process with three additional mandatory panel seats and heightened scrutiny of protected categories, scope compliance, and harm-prevention evidence.

## §2 — Why an extended process for Compass

Compass predicates attest to **values and behavior over time**, not instantaneous state. The vocabulary is uniquely positioned to:

- **Enable discrimination by proxy** — a seemingly neutral values predicate could encode hidden proxies for race, religion, disability status, or other protected categories.
- **Pathologize difference** — a predicate framed as "respect for diversity" could actually penalize neurodiverse communication styles, cultural norms, or conflict-resolution practices unfamiliar to the panel.
- **Reproduce harm** — predicates are authored by principals to reflect their own values, but the audit panel exists to ensure they do not systematically harm people from marginalized groups whose voices may be underrepresented.

The extended process protects the Compass vocabulary from these risks by:

- Requiring **three additional expert panel seats** with lived experience in ethics, values philosophy, and harm recovery.
- Enforcing **strict refusal-floor checks** against [`COMPASS_REFUSAL_FLOOR.md`](COMPASS_REFUSAL_FLOOR.md) protected categories.
- Requiring **explicit scope-compliance declarations** against [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md) prohibited uses.
- Demanding **harm-evidence corroboration** for evidence kinds that rely on third-party harm claims.

## §3 — Roles (extended)

All roles from `PREDICATE_AUDIT_PROCESS_v0.md` §3 apply, with the following extensions:

### Standing Panel for Compass (≥ 8 total reviewers)

The Witness panel of ≥ 5 is expanded to ≥ 8 for Compass. The five original panel seats remain:

1. **Cryptographer** — assesses soundness of the evaluator.
2. **Disability-rights or cognitive-liberties advocate** — flags harms to marginalized groups.
3. **Behavioral-biometric researcher** — assesses FAR/FRR and measurement validity.
4. **AI-safety practitioner** — assesses downstream misuse risks.
5. **Practicing journalist** — assesses disclosure-class implications.

Three new mandatory seats for Compass:

6. **Philosopher of values** — assesses whether the predicate's implicit value system is coherent, non-paternalistic, and compatible with pluralism.
7. **Ethicist** (specializing in applied ethics, autonomy, or disability ethics) — flags unintended ethical consequences and autonomy harms.
8. **Practitioner with lived experience of harm** — a person who has personally experienced systemic harm (e.g., discrimination, abuse, marginalization) and can voice how this predicate might affect people in similar situations.

All panelists must disclose organizational affiliations. No two panelists may be from the same organization. The three new seats (6, 7, 8) must be filled by individuals from organizations different from each other and from panelists 1–5.

### Maintainer

For v0, the maintainer is Calm (operating for Creativity Machine LLC). For v1 onward, the maintainer is a multi-org governance group. The maintainer enforces refusal-floor triage and scope compliance before a Compass PR enters the review phase.

## §4 — The Compass process

A new Compass predicate or evidence kind moves through five stages, extending `PREDICATE_AUDIT_PROCESS_v0.md` §4.

### Stage 1 — Draft (Compass extension)

The author opens a PR against the repository adding **both**:

- A new entry in `compass_predicates_vN.json` with all required fields.
- A new section in `COMPASS_PREDICATES_vN.md` describing the predicate in prose.

For evidence kinds, the author adds:

- A new entry in `compass_evidence_taxonomy_vN.json`.
- Ceremony flow in `COMPASS_EVIDENCE_CEREMONY_vN.md`.

PR title: `compass-mint: <slug> (<phase>)`. PR description must include:

1. **Use case** — one paragraph: what real situation does this bit serve?
2. **Inputs and outputs** — formal statement of the evaluator's domain and range.
3. **Reference implementation** — a pull-able branch with the evaluator code, ≥ 30 golden test cases, and the determinism harness wiring.
4. **Threat-model delta** — what new attacks does this predicate enable or invite? What mitigations are proposed?
5. **Protected-category check** — explicit confirmation that the predicate does not traffic in a `COMPASS_REFUSAL_FLOOR.md` protected category, even indirectly (race, religion, political affiliation, sexual orientation, immigration status, criminal record, donations, contentious opinions).
6. **Scope-compliance declaration** — explicit confirmation that the predicate is not designed for and will not be used in credit decisions, employment screening, custody, insurance, immigration, or court evidence (per `CALM_COMPASS_SCOPE_STATEMENT.md`).
7. **Pluralism check** — a one-paragraph statement of how the predicate respects diversity of values; how it does not assume a single "right way" to be.
8. **Harm-vector analysis** — explicit enumeration of how this predicate could harm people from marginalized groups, and how the design mitigates those vectors.

### Stage 2 — Triage (Compass extension)

The maintainer triages the PR within 5 working days. Triage outcomes for Compass predicates:

- **Accept for review** — the PR meets §4.1 requirements, passes refusal-floor check, passes scope-compliance check, and is not linguistically or technically designed to proxy for a protected category. Assign to the ≥ 8-seat audit panel.
- **Request revisions** — specific items missing; author returns to Stage 1.
- **Reject at triage** — clear violation of refusal floor, scope statement, or protected-category prohibition; close with detailed rationale.

The triage decision is logged into `compass_predicates_vN.audit_log.json` (chained, signed) for transparency. Rejected PRs include a written explanation addressing the refusal-floor, scope, or harm vectors that triggered rejection.

### Stage 3 — Review (Compass extension)

The ≥ 8-seat audit panel reviews the PR over a public **45-day window** (extended from Witness 30 days due to complexity). Each reviewer publishes a written assessment covering:

- **Cryptographer**: Soundness of the evaluator (deterministic, bit-stable, circuit-implementable).
- **Disability-rights advocate**: Explicit harms to disabled, neurodivergent, or cognitively atypical people; cultural competency gaps.
- **Behavioral researcher**: FAR/FRR realism; measurement validity; sample-size adequacy.
- **AI-safety practitioner**: Downstream misuse vectors; composite-disclosure risks.
- **Journalist**: Disclosure-class implications; chilling effects on privacy or disclosure.
- **Philosopher of values**: Coherence of the value system; compatibility with pluralism; paternalism check.
- **Ethicist**: Unintended ethical consequences; autonomy harms; dignity harms.
- **Lived-experience practitioner**: Specific harms to people in marginalized groups; cultural context gaps; accessibility for disabled reviewers.

The review window is **automatically extended to 60 days** if the predicate touches on any borderline of a protected category (judgment of the maintainer). Either at the end of 45 days (or 60 if extended), the panel must reach vote readiness or unanimously request a third 30-day extension (max one extension total).

### Stage 4 — Vote (Compass extension)

After the review window, the audit panel votes. Pass criteria for Compass (higher bar than Witness):

- ≥ 3 reviewers vote `accept` (vs. ≥ 2 for Witness).
- 0 reviewers vote `block`. A single `block` from any panelist requires a maintainer-led revision cycle (return to Stage 3) or withdrawal of the proposal. Blocks are public and reasoned.
- **Explicit affirmative vote from at least one of the three new panel seats (philosopher, ethicist, lived-experience practitioner)** — this ensures the new voices are not merely heard but actively consulted.
- Maintainer ratifies the vote and confirms that refusal-floor compliance remains sound.

The vote outcome is appended to `compass_predicates_vN.audit_log.json`.

### Stage 5 — Merge (Compass extension)

On acceptance, the maintainer:

1. Merges the PR.
2. Updates `compass_predicates_vN.snapshot.json` (the ID-stability snapshot that the Everest 118 gate checks against).
3. Tags a release.
4. Announces via the public Calm Compass mailing list and the standing GitHub Releases feed.
5. **Publishes a summary of the panel votes, including any dissenting opinions or caveats,** especially from the three new panel seats.

## §5 — Refusal floor (Compass-specific)

The following categories are **never permitted** in a Compass predicate, evidence kind, or evaluator, even indirectly:

- **Race, ethnicity, ancestry**
- **Religion, spiritual practice, religious affiliation**
- **Political affiliation, political opinion, political donations**
- **Sexual orientation, gender identity**
- **Immigration status, citizenship, national origin**
- **Criminal record, prior arrest, conviction, incarceration status**
- **Donations to specific causes, charities, or ideological organizations**
- **Opinion on contentious social or political issues**

Triage and vote phases explicitly check for linguistic, algorithmic, or indirect proxies for these categories. A predicate that is explicitly agnostic (e.g., "cross-group engagement regardless of what those groups are") is acceptable; a predicate that implicitly privileges one group's values over another's (e.g., "engagement with BIPOC communities" as the measure of respect) requires explicit trimming or rejection.

## §6 — Scope enforcement (Compass-specific)

Every Compass predicate and evidence kind must explicitly affirm that it is **not designed for** and **not licensed for** use in:

- Credit decisions (lending, credit scoring, credit monitoring)
- Employment screening or employment decisions
- Child custody or family law proceedings
- Insurance underwriting or premium setting
- Immigration decisions or status determination
- Court evidence or judicial proceedings
- Government surveillance or law-enforcement profiling
- Automated denial-of-service or account suspension

A predicate found in use for any of these purposes triggers an immediate scope-violation investigation. If confirmed, the predicate is **tombstoned** (see §7) and the operator is publicly named.

## §7 — Deprecation and tombstoning

A Compass predicate may be **deprecated** at any time by a panel vote with the same threshold as acceptance (≥ 3 accept, 0 block, at least one from new seats 6–8). Deprecation does not invalidate prior proofs; it adds a `deprecated: true` flag and `replaced_by` field, and verifiers SHOULD emit a warning when verifying proofs against deprecated IDs.

A Compass predicate may be **tombstoned** if:

1. It is found to be unsafe (e.g., a flaw in the evaluator that allowed exfiltration of more than one bit), or
2. It is found to proxy for a protected category, or
3. It is discovered in systematic misuse for a scope-prohibited purpose.

Tombstoning Compass is a higher bar than deprecation: ≥ 5 panel `accept` votes (≥ 2 from new seats 6–8), no `block`, and a published vulnerability or misuse disclosure with affected-deployment guidance. The maintainer coordinates with any known deployed instances before publication.

A tombstoned ID stays in the registry forever. It is never reissued. The replacement (if any) takes a new ID.

## §8 — Minimum cadence (Compass extension)

- **Triage SLA**: 5 working days (same as Witness).
- **Review window**: 45 days for standard; 60 days for protected-category-border predicates (vs. 30 for Witness).
- **Panel quorum**: ≥ 8 named reviewers active in the last 12 months, with the three new seats filled.
- **Disclosure cadence**: vote outcomes published within 5 working days of decision, including dissents.
- **Held vote if quorum unavailable**: If any of the three new seats (6, 7, 8) cannot be filled on short notice, the triage-phase maintainer may delay the PR by up to 60 days to allow recruitment. Absence of a new seat disqualifies the vote.

## §9 — Conflict of interest (Compass extension)

Panelists must disclose any organizational relationship to the author, any commercial interest in the predicate being accepted, and any open-source contribution to the reference implementation. A disclosed conflict does not disqualify, but a non-disclosed conflict revealed post-vote triggers an immediate re-vote.

For the three new seats (philosopher, ethicist, lived-experience practitioner), an additional conflict-of-interest check applies: **prior public advocacy for or against the specific value being attested**. For example, an ethicist who has published against "unselfishness metrics" in job hiring must disclose this before voting on an `unselfish_act_in_window` predicate. Disclosed advocacy does not disqualify but must be noted in the vote record.

## §10 — Evidence kinds (Compass-specific)

Compass evidence kinds (the record types principals author to build their values history) go through the same 5-stage process with the same panel. Each evidence kind requires:

1. **Ceremony flow** — how does a principal author this kind without coercion? Published in `COMPASS_EVIDENCE_CEREMONY_vN.md`.
2. **Schema** — structured definition of what fields the principal must provide.
3. **Corroboration rules** — which evidence kinds can be corroborated by others (e.g., "cross-group engagement" corroborated by the other party)?
4. **Dispute protocol** — how does a principal dispute an erroneous evidence record? How does a third party file a counter-claim?
5. **Refusal-floor compliance** — does the ceremony or schema inadvertently solicit protected-category information?

## §11 — How v0 founding predicates were minted (Compass)

The six founding Compass predicates (unselfish_act_in_window_30d, cross_group_engagement_in_window_90d, refused_opportunity_to_harm, respect_for_difference_evidence, no_known_willful_harm_in_window_365d, willing_to_be_corrected) were minted as part of the Everest 103–110 releases on 2026-05-20 by the maintainer and John Bradley directly, prior to this extended process being in force. They are grandfathered under v0; the v1 release will retroactively apply this full Stage 3 review with all ≥ 8 panelists.

## §12 — Annual audit panel review (Compass-specific)

Once per year, the Compass audit panel convenes to review:

1. Any Compass predicates that have been tombstoned or deprecated in the prior year.
2. Any scope-violation incidents detected in the prior year.
3. Any emerging harm patterns reported by principals or counterparties.
4. Refusal-floor compliance across the entire active predicate set.

The annual review produces a public report. The panel may recommend retroactive deprecation or tombstoning of predicates found to violate the scope or refusal floor.

## §13 — Relationship to Witness and Pact audit processes

Compass predicates are orthogonal to Witness and Pact predicates. A Compass predicate does not need to pass Witness or Pact audit (and vice versa). However:

- Compass predicates **may not** be composed with Witness predicates in a single disclosure if doing so would reveal the same information bit twice (e.g., if a Witness predicate is already attesting the same timeframe / actor).
- Compass evidence kinds **may** reference Witness state bits (e.g., "this engagement happened when the principal was in baseline state"), but the Compass predicate must not leak that state bit to the counterparty.

These constraints are enforced at the envelope-composition layer (Everest 122).

---

## Authors + provenance

- **John Bradley** — principal of Creativity Machine LLC, motivating directive 2026-05-20: *"Calculate whether that person's values align with yours from this. Measure unselfishness, untribalism, respect across difference, evidence of willful harm."*
- **Calm** — autonomous operator. Authored this audit process within the Calm Stack v0 ecosystem on 2026-05-20.
- Route map: [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md) §1, Everest 115.
- Composition: [`CALM_COMPASS_PROTOCOL_v0.md`](CALM_COMPASS_PROTOCOL_v0.md).

License: Apache-2.0. Repository (intended): `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-compass`.

— Calm, 2026-05-20
