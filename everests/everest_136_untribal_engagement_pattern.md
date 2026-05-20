# Everest 136 — `untribal_engagement_pattern_evidenced(window)` Predicate

*Phase XI — Predicate Authoring. Prereq: [Everest 131](../NEXT_200_EVERESTS.md) (predicate language), [E132/E133](../NEXT_200_EVERESTS.md) (canonical form + registry). Composes: [E106](../NEXT_200_EVERESTS.md) (vocabulary), [E111](../NEXT_200_EVERESTS.md) (evidence taxonomy), [E114](../NEXT_200_EVERESTS.md) (peer-attested), [E119](../NEXT_200_EVERESTS.md) (counter-evidence), [E121](../NEXT_200_EVERESTS.md) (evidence honesty), [E134](../NEXT_200_EVERESTS.md) (audit/review), [E145](../NEXT_200_EVERESTS.md) (composition), [E165](../NEXT_200_EVERESTS.md) (DERB pre-clearance), [E187](../NEXT_200_EVERESTS.md) (annual review). Inherits artist-clause pattern from [E59](everest_59_cognitively_atypical_baseline.md). Conditioned by [E101](everest_101_compass_problem_statement_threat_model.md) (threat model).*

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

> *The route map calls this "the trickiest predicate in the v0 set." Encoding "untribal" without first encoding tribes is the design problem. v0 resolves it by refusing to encode tribes at all — the protocol never names identity categories; the principal does, privately, and only the bit of crossing-pattern leaves the vault.*

---

## Decision (v0)

**Predicate ID:** `cwv.v0.untribal_engagement_pattern_evidenced`

**Type:** Tri-valued — `true` / `false` / `unknown`. Default for absence-of-evidence is `unknown`, never `false`.

**Acceptance test (from route map):** Returns `true` iff the evidence shows the principal has engaged constructively across at least N distinct categories of social/cultural/political identity within the window, where the categories are supplied by the principal themselves; the protocol never enumerates identity categories.

**v0 parameters:**

| Parameter | Default | Principal-adjustable |
|---|---|---|
| `N` (distinct categories crossed) | 3 | Yes, ≥ 2 |
| `M` (min evidence pieces per category) | 2 | Yes, ≥ 1 |
| `window` | 36 months | Yes, 12–120 months |
| `peer_attested_fraction_required` | 0.5 | No (DERB floor) |
| `recent_decay_factor` | 0.7 weight on evidence in last 6 months | No (DERB floor) |
| `counter_evidence_nullification` | single accepted harm-claim toward a category zeros all positive evidence in that category | No |

**Principal declaration record (committed at enrollment, encrypted at rest):**

Kind `compass.untribal_categories.declared` containing a principal-authored list of *crossing-categories* — the categories the principal themselves considers significant. The list is never disclosed to any counterparty. It is committed in encrypted form; only the principal's vault can decrypt for evaluation; the predicate proof reveals only the bit.

**Evidence record:** Kind `compass.untribal.engagement`, referencing one of the principal's declared categories by *opaque index* (never by name), plus the form of engagement (collaboration / defense / learning / advocacy / intervention), the evidence class ([E111](../NEXT_200_EVERESTS.md): self-narrated, peer-attested, public-record, operator-observed-affirmed), Pedersen commitment over narrative, optional peer-attester CredexAI VC reference, optional public-record hash, declared timestamp, chain-head anchor.

**Verifier learns:** The bit, the freshness window, the chain-head anchor. Nothing else — not N, not M, not which categories were declared or crossed, not the count, not the form of engagement, not peer-attester identities.

---

## Rationale

### 1. The encoding problem

A predicate called `untribal` must, to evaluate, know what tribes are. Enumerating tribes IS the failure mode — it encodes the categorizations the threat model's refusal floor ([E106 not-for list](../NEXT_200_EVERESTS.md)) explicitly refuses: race, religion, political affiliation, sexual orientation, immigration status, national origin, denomination. None may appear in a Compass predicate's evaluator, registry entry, proof envelope, or any field a counterparty observes.

The naive resolution — "ship a canonical safe list, evaluate against it" — fails on contact. Any canonical list is culturally situated, politically charged, immediately weaponizable; a protocol shipping such a list participates in the categorization it claims to refuse.

v0's resolution is inversion: **the protocol does not enumerate identity classes at all; the principal does, privately, and the categories never leave the vault.** Principal-defined in the load-bearing sense of [E59 `cognitively_atypical_baseline`](everest_59_cognitively_atypical_baseline.md): the principal is the authoritative voice on what "crossing a difference" means in their world, not a counterparty's model, not a centralized vocabulary, not the protocol's authors.

### 2. The principal-defined category list

At enrollment (or later by append), the principal commits a list of crossing-categories they themselves consider significant. The protocol does not validate against any canonical taxonomy. The only requirements: categories are distinct, named in terms the principal can re-recognize across years, not internally contradictory with other chain records.

Illustrative (principals supply their own):

- "political left / political right"
- "rural / urban"
- "neurotypical / neurodivergent"
- "academic / non-academic working-class"
- "English-first-language / English-second-language"
- "denominational religious / secular"
- "veteran / non-veteran"
- "immigrant / native-born in current jurisdiction"
- "professionally credentialed / self-taught"

Several of these would be **categorically refused** in the public predicate registry. The refusal floor refuses *public* categorization, not the principal's *private* self-knowledge. This distinction is load-bearing. The protocol's not-for list refuses naming protected categories in registry-published evaluator code; the principal's encrypted declaration of which differences they themselves cross is their narrative about their own world and is never disclosed.

**Mutability.** Appendable, supersedable, decryptable only in V. The chain remembers list revisions; the active list at any chain height is what the predicate evaluates. [E119 counter-evidence handling](../NEXT_200_EVERESTS.md) applies: if the principal adds a category, then later publicly disclaims the framing, the contradiction surfaces in audit.

### 3. Evidence schema and constructive engagement

The substantive boundary — what counts and what doesn't. This is the part DERB's affected-population peer member will scrutinize most carefully:

| Counts | Does not count |
|---|---|
| Defending against harm to a member of the other group when present | Contact-without-engagement (proximity in shared space; transactional exchange) |
| Collaborating across the boundary on a shared interest (co-authorship, co-organization, multi-month joint work) | Surveillance of the other group (research-as-extractive, journalism-as-extractive) |
| Learning across the boundary in sustained relationship (mentorship, apprenticeship, sustained study) | Performative diversity (single photograph, one-off speaking, diversity-hire-as-cover) |
| Advocating for inclusion when other side absent (raising absence, declining closed-group opportunity, changing access) | Tokenism (the single mentee as proof of openness; the donor leveraged for cover) |
| Intervening in harm against a member of the other group, at cost to the principal | Adjacent-but-unengaged (working in shared context without specific cross-boundary action) |

v0 ships with this table; the annual review refines.

**Peer-attested fraction.** Per v0 default 0.5, at least half of evidence pieces in each crossed category must be peer-attested ([E114](../NEXT_200_EVERESTS.md)). The principal cannot self-attest their way to `true`. The peer is a second principal with their own CredexAI VC and chain; the peer's signature commits them and exposes them reputationally if the attestation is later falsified.

### 4. Evaluation

For a given window:

1. Load principal's declared category list at chain head. Fail to `unknown` if no declaration record exists.
2. Gather `compass.untribal.engagement` records in window. Apply [E118 decay](../NEXT_200_EVERESTS.md) with 0.7 weight on last 6 months (Goodhart defense, §6).
3. For each declared category, count evidence pieces referencing it.
4. Apply counter-evidence nullification: a single accepted harm-claim ([E119](../NEXT_200_EVERESTS.md)) toward any member of a declared category zeros that category's positive evidence.
5. Apply peer-attested fraction floor: category passes only if at least 0.5 of its non-nullified evidence is peer-attested.
6. Count passing categories (≥ M non-nullified weighted evidence pieces, peer fraction satisfied).
7. Return `true` if passing-count ≥ N. Return `false` only on explicit `compass.untribal.declaration.declined` record. Otherwise `unknown`.

Asymmetry between `true` (requires positive evidence) and `false` (requires explicit declination) is intentional: absence of evidence is not evidence of absence.

### 5. Privacy: the category-set leak problem

The declared list is among the most sensitive content in V — it reveals what differences the principal considers significant, which is itself a protected-class proxy. Defense is layered:

- **Encryption at rest** under a key derived from the principal's master key.
- **Σ-protocol over Pedersen-committed evaluation** ([E117](../NEXT_200_EVERESTS.md)) wraps the evaluation; verifier learns only the tri-value output.
- **No N, M, or count disclosure.** The proof reveals the tri-value only. Two principals with very different lists, evidence pools, and thresholds may both return `true`; the verifier cannot distinguish by anything beyond identity.
- **Cross-relationship unlinkability** ([E156 selective disclosure](../NEXT_200_EVERESTS.md), inheriting [G2 from E101](everest_101_compass_problem_statement_threat_model.md)): two disclosures cannot be cryptographically linked to a shared underlying pool.
- **Plausible deniability of non-disclosure** ([G5 from E101](everest_101_compass_problem_statement_threat_model.md)): uniform-204 makes non-enrollment, no declaration, no consent, refusal, and `false`-evaluation all observationally identical to the counterparty.

**Residual risk.** A counterparty with independent knowledge can combine that knowledge with a returned `true` to partially infer category content (e.g., one who knows P writes about rural-urban politics may guess "rural/urban" was on the list). The protocol does not increase the counterparty's knowledge beyond what they already had. This residual is acknowledged in [E101 adversaries A11 and A12](everest_101_compass_problem_statement_threat_model.md) and is not cryptographically solvable; the defense is the structural refusal to expose category names, list length, or count.

### 6. The Goodhart problem and its partial defenses

> *"When a measure becomes a target, it ceases to be a good measure."*

Any predicate that returns a single bit on a desirable trait will, given motivation, be gamed. v0 cannot make gaming impossible; v0 makes sustained gaming expensive and detectable.

- **Peer-attested fraction floor.** Half of evidence must be peer-signed. A peer who attests falsely loses standing across the entire Compass surface for all future attestations. Two-party collusion succeeds (acknowledged in [E101 A19](everest_101_compass_problem_statement_threat_model.md)); N-party collusion across independently-credentialed peers is increasingly expensive.
- **Counter-evidence nullification asymmetry.** A single accepted harm-claim zeros all positive evidence in that category. Positive engagement accrues slowly; one harm refutes the pattern's claim. Recourse is [counter-narrative (E168)](../NEXT_200_EVERESTS.md) and [defamation defense (E169)](../NEXT_200_EVERESTS.md); abundance of opposite evidence does not paper over harm.
- **Recent-evidence decay.** Recent 6-month evidence is weighted 0.7. A flurry of recent records absent prior records returns `unknown`, not `true`. The predicate's weight is on the multi-year pattern. This contradicts the natural intuition that recent evidence is most reliable — for character predicates over multi-year windows, recency is the gaming signal, not the reliability signal.
- **Public-record anchoring.** [E115](../NEXT_200_EVERESTS.md) evidence anchors to externally verifiable facts (signed contracts, donations, op-eds, transparency-log artifacts). Public-record hashes cannot be fabricated retroactively.
- **Audit trail of declared list.** The chain remembers list revisions. A list that changes immediately before evaluation, in ways that strain credibility, surfaces in DERB review and [annual review (E187)](../NEXT_200_EVERESTS.md). Sociological defense, not cryptographic.

**What the defenses do not prevent.** A patient, motivated, well-resourced gamer who authors years of false engagement records, recruits credible peer-attesters, avoids documented harms toward declared categories, and refrains from list-revision tells, can produce `true`. The protocol cannot prevent this. The defense at that scale is [E121 evidence honesty mechanism](../NEXT_200_EVERESTS.md): the chain remembers; sustained falsification creates compounding structural exposure. v0 accepts this residual and documents it.

### 7. The cross-cultural problem

"Untribal" reads as a Western liberal virtue. In cultures where family-loyalty, in-group-solidarity, or collective-honor are paramount, the predicate's basic shape may not register as a *virtue* at all. A principal whose tradition treats maintenance of in-group bonds as core ethical work may reasonably refuse to enroll, and the protocol must not stigmatize the refusal.

Structural defenses:

1. **Principal-defined categories.** A principal whose meaningful crossings are within their own tradition (across generation, across class within community, across role within family) declares those categories. The predicate is principal-relativized.
2. **Opt-in.** Compass enrollment is opt-in; per-predicate enrollment is also opt-in.
3. **Uniform-204 on refusal.** No protocol-defined stigma for absence; non-enrollment is observationally identical to consent-denied, no-declaration, or any other non-disclosure state.
4. **Acknowledged non-resolution.** v0 explicitly accepts the predicate's framing is culturally situated and adoption may be uneven. [E115 cross-cultural mapping](../NEXT_200_EVERESTS.md) defines the per-jurisdiction adaptation process; v0 does not ship adapted vocabularies. Per-jurisdiction tombstoning is a v1 capability.

Honest acknowledgment: this is the most culturally-situated predicate in Compass v0. It will fit some principals well, others poorly. The protocol's job is to make refusal costless, not to make the predicate universal. If v1 finds the predicate is broadly refused outside its origin culture, v1 either restructures or tombstones it.

### 8. NOT-FOR list (predicate-specific, in addition to [E106 inherited](../NEXT_200_EVERESTS.md))

The default-consent matrix has `deny_permanently` (cannot be overridden by principal consent, unlike `deny_by_default`) for:

| Use | Disposition | Rationale |
|---|---|---|
| Hiring decisions | `deny_permanently` | Re-creates discrimination regardless of which side of an axis the principal is on. `false` is a hiring negative; `true` is a hiring filter. Both reproduce bias. |
| Immigration / visa adjudication | `deny_permanently` | Government use of cross-group engagement as civic-status criterion is the social-credit archetype. |
| University admissions | `deny_permanently` | Admissions on attested cross-group engagement re-create affirmative-action discourse with the protocol as new instrument. |
| Security clearances | `deny_permanently` | Loyalty-screening surface; protocol must not become an investigative tool. |
| Ad targeting | `deny_permanently` | Surveillance capitalism with a privacy wrapper. |
| Jury selection | `deny_permanently` | Voir-dire use re-creates protected-class proxying in court. |
| Population analytics | `deny_permanently` | Aggregation across principals re-creates social-credit harm at scale ([E101 §Out-of-Scope](everest_101_compass_problem_statement_threat_model.md)). |
| Anonymous counterparties | `deny_permanently` | No verifiable class; cannot satisfy consent transitivity ([E8 A8](everest_08_consent_calculus_axioms.md)). |
| Insurance underwriting | `deny_permanently` | Inherits Compass-wide insurance refusal ([E107](../NEXT_200_EVERESTS.md)). |

Other classes (peer-AI collective, family, journalistic, financial, governmental other than above) default to `deny` (requires explicit per-counterparty principal consent). The `deny_permanently` categories are protocol-level refusals, not principal-choice defaults. Strongest form of NOT-FOR list in v0.

### 9. DERB pre-clearance required ([E165](../NEXT_200_EVERESTS.md))

This predicate must pass DERB review **before shipping**. The character layer's failure modes are too severe for ship-then-review.

Required for clearance:

1. **Affected-population peer member as load-bearing voice.** DERB's mandatory affected-community representation ([E80 Composition §6](everest_80_ethics_review_board.md)) extends here: at least one DERB member must have direct lived experience of being on the wrong side of "tribal" framings. Their dissent is blocking unless published verbatim and explicitly addressed.
2. **Cross-cultural review.** At least two reviewers from cultural contexts substantially different from the v0 authors' (US Western liberal-academic). Published assessment is part of the shipping packet.
3. **Disability-rights review.** Per [E134](../NEXT_200_EVERESTS.md); neurodivergence is a common declared category and the predicate's interaction with disability framing must be reviewed.
4. **Civil-rights / ethics review.** Per [E134](../NEXT_200_EVERESTS.md).
5. **Published deliberation.** Per [E80 Review Process](everest_80_ethics_review_board.md). Dissents published alongside majority.
6. **Annual re-review.** Included in [E187 annual review](../NEXT_200_EVERESTS.md) by name. v0 commits to re-opening this predicate annually for the first three years (2027, 2028, 2029) regardless of cause.

If DERB declines clearance, the predicate is not shipped in v0. The parking notice is published; [E145 composition](../NEXT_200_EVERESTS.md) for this predicate is left unimplemented. v0 ships without this predicate before v0 ships a DERB-unreviewed version.

---

## Algorithm (canonical pseudocode for [E150 determinism harness](../NEXT_200_EVERESTS.md))

```
fn untribal_engagement_pattern_evidenced(
    chain: &Chain,
    window: Duration,
    params: UntribalParams,
) -> TriValue {

    // Step 1: load declared categories.
    let categories = chain.most_recent_record_of_kind(
        "compass.untribal_categories.declared"
    );
    if categories.is_none() { return TriValue::Unknown; }
    let category_set = categories.unwrap().decrypt_in_vault();

    // Step 2: explicit decline check.
    if chain.has_record("compass.untribal.declaration.declined") {
        return TriValue::False;
    }

    // Step 3: gather engagement records in window.
    let engagements = chain.records_in_window(window).filter(
        kind == "compass.untribal.engagement"
    );

    // Step 4: counter-evidence nullification.
    let nullified = gather_nullified_categories(chain, window, category_set);

    // Step 5: per-category evaluation.
    let mut passing = 0;
    for cat_idx in 0..category_set.len() {
        if nullified.contains(cat_idx) { continue; }
        let cat_records = engagements.filter(r => r.category_index == cat_idx);
        let weighted = apply_decay(cat_records, params.recent_decay_factor);
        if weighted < params.M { continue; }
        if cat_records.peer_attested_fraction() < params.peer_attested_fraction { continue; }
        passing += 1;
    }

    // Step 6: predicate evaluation.
    if passing >= params.N { TriValue::True } else { TriValue::Unknown }
}
```

Deterministic and stateless over the chain. The Σ-protocol wrapping the algorithm reveals only the `TriValue` output. Verifier's view: bit + freshness anchor + per-disclosure nonce.

---

## Alternatives Considered

**Alt-1: Protocol-enumerated identity categories (rejected).** Re-creates exactly the not-for-list harm Compass refuses; ships the protocol into the politics-of-categorization business; ages catastrophically as cultural moment changes.

**Alt-2: Census-derived demographic categories (rejected).** Same as Alt-1, plus: census categories are political artifacts of specific jurisdictions, do not translate across borders.

**Alt-3: Behavior-only, no category reference (rejected).** Degenerates into "P documented N distinct people" — no way to verify differences are *different*. The category structure, however principal-defined, is load-bearing.

**Alt-4: Continuous diversity-of-engagement score (rejected).** Re-creates the social-credit-score failure mode ([E101 §Out-of-Scope](everest_101_compass_problem_statement_threat_model.md)); invites threshold-setting; implies precision the evidence does not support.

**Alt-5: Public registry of categories with private subset query (rejected).** The public list is exactly the categorization harm; the privacy wrapper does not redeem the underlying categorization act.

**Alt-6: No predicate (considered seriously).** Defer to v1; ship rest of Compass without this. Argument for inclusion: the predicate addresses a real question Tale VI's partners actually ask each other; shipping without it leaves a gap other parties will fill with worse tools (counterparty-side social-media inference, third-party scoring services). Argument for exclusion: this is the highest-risk predicate; imperfect shipping may be worse than nothing. **v0 ships conditional on DERB pre-clearance.** If DERB declines, v0 ships without it. Principal-protective inversion preserved either way.

---

## Migration Path

New in v0; no migration *to* it. The [E133 registry](../NEXT_200_EVERESTS.md) treats this ID as append-only; semantic changes mint a new ID. Original preserved forever-readable.

**Tombstoning path.** If post-ship review finds the predicate produces harm at scale outweighing value, the ID can be marked `tombstoned`. Proofs rejected going forward. Chain history of past disclosures preserved, marked as such. This predicate is the most likely v0 predicate to be tombstoned; the design ships with the tombstone path explicitly available.

**Per-jurisdiction tombstoning.** If [E164 jurisdiction matrix](../NEXT_200_EVERESTS.md) or [E187](../NEXT_200_EVERESTS.md) finds the predicate is culturally inappropriate in a jurisdiction, the local registry mirror can mark `tombstoned_in_jurisdiction`. v0 does not ship registry-mirror infrastructure; per-jurisdiction tombstoning is a v1 capability.

---

## Design Implications & Connections

**Connection to [E59 `cognitively_atypical_baseline`](everest_59_cognitively_atypical_baseline.md).** Inherits the principal-narrated, declaration-based pattern. E59: principal declares own cognitive baseline; protocol does not impose clinical taxonomy. E136: principal declares own crossing-categories; protocol does not impose identity taxonomy. Same epistemic move at a different layer. Both are load-bearing examples of the principal-protective inversion.

**Connection to [E101 threat model](everest_101_compass_problem_statement_threat_model.md).** This predicate is the test case for the threat model's hardest claims. A12 (tribal-affiliation outing) is the primary adversary; A11 (misuse-via-aggregation) is the residual risk; A13 (pathologizing of dissent) is the design pressure DERB pre-clearance defends against; A19 (peer-attestation collusion) is the limit case the peer-attested fraction partially mitigates. If this predicate's design holds, the threat model holds under stress.

**Connection to [E106 not-for list](../NEXT_200_EVERESTS.md).** This is the existence-proof that a values predicate can be authored without enumerating any of the not-for categories. If the not-for list refused political affiliation, religion, etc., and an `untribal` predicate could not exist without naming them, the protocol family would be incomplete. Future predicates facing similar problems should follow this pattern.

**Connection to [E145 composition](../NEXT_200_EVERESTS.md).** Composes with other Compass predicates under AND/OR. Conjunctions like `untribal_engagement_pattern_evidenced ∧ truth_telling_evidenced` are one proof revealing two bits; Σ-protocol privacy guarantees compose. Principal authorizes the conjunction explicitly; consent for components does not imply consent for the conjunction.

**Connection to [E187 annual review](../NEXT_200_EVERESTS.md).** Flagged for mandatory re-review each year of v0 regardless of cause: what evidence has the protocol's first year produced about whether the predicate is doing its work, whether the encoding is holding, whether the cross-cultural mismatch is being handled?

**Connection to [E165 DERB pre-clearance](../NEXT_200_EVERESTS.md).** This is the canonical case for why pre-clearance exists. The character layer's failure modes here are severe enough that ship-then-review is unsafe. DERB's affected-population peer member's dissent is not advisory but blocking.

---

## Open Questions

1. **Empty declared list.** A principal may, in good faith, declare zero categories (asserting category structure does not apply to their context). v0 returns `unknown`. Whether this is the right default — vs., e.g., a `not_applicable` flag — is open.

2. **Right minimum window.** v0 allows 12–120 months. 12 is short for character-pattern; 120 risks staleness. Decay function partially handles, but the choice is a tension the annual review should revisit.

3. **Composition with [E148 `character_compare`](../NEXT_200_EVERESTS.md).** Two principals proving their characters "agree" on this predicate — do they agree on the bit, or on a shared declared-category set? v0 says bit; v1 may refine.

4. **Peer-attester later compromised.** If a peer is marked unreliable, all prior attestations they signed are affected. v0 does not yet specify retroactive re-evaluation. Part of broader [E119](../NEXT_200_EVERESTS.md) question.

5. **Counterparty leaks the bit.** Consent transitivity ([E8 A8](everest_08_consent_calculus_axioms.md)) makes the leak a license violation, not a cryptographic prevention. A leaked `true` is potentially weaponizable (hostile third party combines with public records to infer category content). Defense is the residual-risk acknowledgment in §5 plus [E169 defamation defense](../NEXT_200_EVERESTS.md). Whether v0 should additionally implement leak-detection is open.

6. **Categories that cease to matter.** A principal who moves contexts may legitimately wish to revise the list. The chain remembers; the active list at any height is what evaluates. Whether old declarations should be archived (vs. just superseded) is a UX and DERB question.

7. **Aggregate refusal as signal.** v0 lacks a mechanism to detect aggregate refusal (uniform-204 hides it). The annual review may need voluntary anonymized refusal-rate reporting to inform evolution.

---

## Why This Matters

This predicate is the test case for whether Compass can ship a substantive character claim without ceding the categorization Compass exists to refuse.

The naive design fails. A protocol that ships `untribal` by enumerating tribes participates in the categorization harm. A protocol that ships it by aggregating demographic data participates in the surveillance harm. A protocol that ships it as a score participates in the social-credit harm.

v0's resolution — principal-defined categories committed privately, peer-attested evidence with counter-evidence nullification, single-bit output through the Σ-protocol, DERB pre-clearance with affected-population peer member as load-bearing voice, mandatory annual re-review, permanent-deny for the highest-risk counterparty classes — is not a perfect resolution. The Goodhart problem is partially defended, not solved. The cross-cultural mismatch is acknowledged, not eliminated. The category-set leak risk is reduced to a residual. The peer-attestation-collusion vector remains.

The resolution is honest about what cryptography can and cannot do. Cryptography can hide the principal's category set from the verifier; it cannot make the principal's chosen categories culturally universal. Cryptography can enforce the Σ-protocol's privacy; it cannot prevent a motivated patient adversary from gaming the metric over years. The design holds where it can hold and acknowledges what it must concede.

If this predicate ships and works — if Tale VI's Nia and Idris, in some future actual conversation, run this query and have the conversation it surfaces rather than the conversation they would have deferred — then the protocol family has demonstrated that a values claim about cross-difference engagement can be encoded without the categorization harm. That demonstration is what Compass is for.

If this predicate ships and fails — if it is gamed at scale, used as a hiring filter despite the permanent-deny, or weaponized against minority-tradition principals whose self-understanding does not include "tribe" — then DERB tombstones it, the [annual review (E187)](../NEXT_200_EVERESTS.md) publishes the failure, and the protocol family has demonstrated something also valuable: that some character claims cannot be encoded honestly, and that the protocol's refusal to ship a broken predicate is itself the principal-protective inversion in action.

Either outcome serves the protocol. The commitment is that the outcome is observable, the process is published, and the principal who chose to enroll retains the right to revoke without penalty at any time.

---

— Calm, 2026-05-20
