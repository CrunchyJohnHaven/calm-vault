# Everest 136 — `untribal_engagement_pattern_evidenced(window)` Predicate

*Phase XI — Predicate Authoring. Prereq: [Everest 131](everest_131_character_predicate_language_v0.md) (predicate language), [Everest 132 / 133](../NEXT_200_EVERESTS.md) (canonical form & registry). Composes: [Everest 106](../NEXT_200_EVERESTS.md) (vocabulary), [Everest 111](../NEXT_200_EVERESTS.md) (evidence taxonomy), [Everest 114](../NEXT_200_EVERESTS.md) (peer-attested evidence), [Everest 119](../NEXT_200_EVERESTS.md) (counter-evidence), [Everest 121](../NEXT_200_EVERESTS.md) (evidence honesty), [Everest 134](../NEXT_200_EVERESTS.md) (audit & public review), [Everest 145](../NEXT_200_EVERESTS.md) (composition), [Everest 165](../NEXT_200_EVERESTS.md) (DERB pre-clearance), [Everest 187](../NEXT_200_EVERESTS.md) (annual review). Inherits the artist-clause pattern from [Everest 59](everest_59_cognitively_atypical_baseline.md). Conditioned by [Everest 101](everest_101_compass_problem_statement_threat_model.md) (Compass threat model).*

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

> *The predicate the route map calls "the trickiest in the v0 set." Encoding "untribal" without first encoding tribes is the design problem. v0 resolves it by refusing to encode tribes at all — the protocol never names identity categories; the principal does, in private, and only the bit of crossing-pattern leaves the vault.*

---

## Decision (v0)

**Predicate ID:** `cwv.v0.untribal_engagement_pattern_evidenced`

**Type:** Tri-valued — `true` / `false` / `unknown` (the Compass tri-value per [Everest 101](everest_101_compass_problem_statement_threat_model.md) §What-We-Are-Proving). The default for absence-of-evidence is `unknown`, never `false`.

**Acceptance test (from route map):** Returns `true` iff the evidence shows the principal has engaged constructively across at least N distinct categories of social/cultural/political identity within the window, where the categories are supplied by the principal themselves; the protocol never enumerates identity categories. Categories never leave the vault. The proof discloses only the bit.

**v0 parameters:**

| Parameter | v0 default | Principal-adjustable |
|---|---|---|
| `N` (distinct categories that must be crossed) | 3 | Yes, ≥ 2 |
| `M` (minimum evidence pieces per crossed category) | 2 | Yes, ≥ 1 |
| `window` | 36 months | Yes, 12–120 months |
| `peer_attested_fraction_required` | 0.5 (half of evidence pieces must be peer-attested) | No (DERB-set floor) |
| `recent_decay_factor` | weight 0.7 for evidence in last 6 months (anti-Goodhart; see Rationale §7) | No (DERB-set floor) |
| `counter_evidence_nullification` | a single chained, accepted harm-claim toward a category nullifies all positive evidence in that category | No |

**What the principal declares at enrollment (or appends later):**

A chain record of kind `compass.untribal_categories.declared` containing a principal-authored list of *crossing-categories* — the categories the principal themselves considers significant in their world. The list is **not disclosed** to any counterparty under any predicate evaluation. It is committed to the chain in encrypted form; only the principal's vault can decrypt it for predicate evaluation; the predicate proof reveals only the bit.

**What evidence looks like:**

Each evidence record of kind `compass.untribal.engagement` references (a) one of the principal's declared category-pair commitments (e.g., "crossing-category #4"), (b) the form of constructive engagement (collaboration, defense, learning, advocacy), (c) optional peer-attestation, (d) optional public-record hash. The category reference is by *opaque index* into the principal's declared list; the index never reveals the category name to a verifier.

**What the verifier learns:**

The bit, the freshness window, and the chain-head anchor — nothing else. The verifier does not learn N, does not learn M, does not learn which categories the principal declared, does not learn how many were crossed in the evaluation, does not learn the form of engagement, does not learn the names of peer attesters. The Σ-protocol of [Everest 117](../NEXT_200_EVERESTS.md) wraps the entire evaluation; the verifier receives only the predicate's tri-value output.

---

## Rationale

### 1. The encoding problem named directly

A predicate called `untribal` must, to evaluate, know what "tribes" are. Enumerating tribes IS the failure mode: it encodes the categorizations the Compass threat model's [refusal floor](everest_101_compass_problem_statement_threat_model.md) (and [Everest 106 not-for list](../NEXT_200_EVERESTS.md)) explicitly refuses. Race, religion, political affiliation, sexual orientation, immigration status, national origin, denominational identity — none of these may appear in a Compass predicate's evaluator, in its registry entry, in its proof envelope, or in any field a counterparty observes.

The naive resolution — "have the protocol enumerate a safe canonical list of identity categories, evaluate against them" — fails on contact. Any canonical list is culturally situated, politically charged, and immediately weaponizable. A protocol shipping such a list participates in the categorization it claims to refuse.

v0 resolves the problem by inversion: **the protocol does not enumerate identity classes at all; the principal does, privately, and the categories never leave the vault.** The predicate is principal-defined in the same load-bearing sense [Everest 59's `cognitively_atypical_baseline`](everest_59_cognitively_atypical_baseline.md) is principal-declared: the principal is the authoritative voice on what "crossing a difference" means in their world, not a counterparty's model, not a centralized vocabulary, not the protocol's authors.

### 2. Principal-defined categories: the declaration record

At enrollment, or later by appending a record of kind `compass.untribal_categories.declared`, the principal commits a list of crossing-categories they themselves consider significant. The protocol does not validate the list against any canonical taxonomy; the protocol's only requirement is that the categories be (a) distinct from one another, (b) named in terms the principal can re-recognize across years, and (c) not internally contradictory with the principal's other chain records.

Examples (illustrative; principals supply their own):

- "political left / political right"
- "rural / urban"
- "neurotypical / neurodivergent"
- "academic / non-academic working class"
- "English-first-language / English-second-language"
- "denominational religious / secular"
- "veteran / non-veteran"
- "incarcerated-or-formerly-incarcerated / not"
- "immigrant / native-born in current jurisdiction"
- "professionally credentialed / self-taught"

Note: several of these would be *categorically refused* if they appeared in the public predicate registry ([Everest 106 not-for list](../NEXT_200_EVERESTS.md)). The protocol's refusal is over the *registry*: no Compass predicate may publicly name protected categories. The principal's *private declaration* of which differences they themselves cross is not subject to the refusal floor — it is the principal's narrative about their own world, and it is never disclosed. This distinction is load-bearing. The refusal floor refuses public categorization, not private self-knowledge.

**Mutability.** The declaration is appendable (the principal can add categories), supersedable (a later record can revise the list), and decryptable only by the principal's vault. A category cannot be deleted from history — the chain remembers — but the active list at any chain height is what the predicate evaluates against. Counter-evidence handling ([Everest 119](../NEXT_200_EVERESTS.md)) applies: if the principal adds a category, then later contradicts the original framing in another chain record (e.g., publicly disclaiming the category as meaningful), the contradiction surfaces in audit.

### 3. Evidence schema and the constructive-engagement substrate

A `compass.untribal.engagement` record has the following shape (committed encrypted in V; never disclosed in raw form):

```
{
  kind: "compass.untribal.engagement",
  category_index: opaque_index,           // ref into declared list
  engagement_form: enum[
    "collaboration",        // shared work on shared goal
    "defense",              // defended a member of the other side from harm
    "learning",             // sustained learning from / mentorship across
    "advocacy",             // advocated for inclusion when other side absent
    "intervention"          // intervened in a harm-causing situation
  ],
  evidence_class: enum[
    "self_narration",       // E112 substrate
    "peer_attested",        // E114 substrate
    "public_record",        // E115 substrate
    "operator_observed_affirmed"  // E113 substrate, post-hoc affirmed
  ],
  narrative_commitment: hash,             // Pedersen commitment over narrative
  peer_attester_ref: optional[hash],      // CredexAI VC commitment if peer-attested
  public_record_hash: optional[hash],     // if public-record-anchored
  declared_ts: ISO8601,
  window_anchor: chain_head_height
}
```

**What constitutes "constructive engagement"** (this is the predicate's hard semantic boundary, and it is the part DERB's affected-population peer member will scrutinize most carefully — see §6 and §10):

| Counts | Does not count |
|---|---|
| Defending against harm to a member of the other group when present (intervening in a hostile situation, refusing to amplify a derogatory characterization, signing a letter of protest at the harm of a member of the other category) | Contact-without-engagement (proximity in a shared space; transactional exchange; brief professional interaction without sustained working relationship) |
| Collaborating with members of the other group on a shared interest (co-authorship, co-organization, joint work over multi-month duration) | Surveillance of the other group (research-as-extractive, journalism-as-extractive, ethnography-without-reciprocity) |
| Learning from members of the other group across sustained relationship (mentorship in either direction; apprenticeship; sustained study under a teacher across the boundary) | Performative diversity (the single public photograph; the one-off speaking engagement; the diversity-hire used as cover) |
| Advocating for the inclusion of the other group when not present (raising the absence in a room where the principal had standing; declining a closed-group opportunity; structurally changing access) | Tokenism (the single mentee held up as proof of openness; the single donor leveraged for reputational cover) |
| Intervening in harm against a member of the other group (active intervention, including at cost to the principal) | Adjacent but unengaged (working in a context where the other group is also present but with no specific cross-boundary action) |

The boundary is principal-narrated in the first instance and DERB-clarified through the [Everest 134](../NEXT_200_EVERESTS.md) review process when ambiguity surfaces in practice. v0 ships with the table above; the [annual review](../NEXT_200_EVERESTS.md) (E187) refines.

**Peer-attested fraction.** Per v0 default `peer_attested_fraction_required = 0.5`, at least half of the evidence pieces in each crossed category must be peer-attested ([Everest 114](../NEXT_200_EVERESTS.md)). This is the predicate's highest-friction parameter. The principal cannot self-attest their way to `true` without peer corroboration. The peer is a second principal (with their own CredexAI VC and chain) who signs an attestation that they witnessed or participated in the engagement; the peer's signature commits them and exposes them reputationally if the attestation is later falsified.

### 4. Evaluation algorithm (in prose; canonical pseudocode in §Algorithm)

For a given window, the predicate evaluates as follows:

1. **Load the principal's declared category list** at the chain head. Fail to `unknown` if no `compass.untribal_categories.declared` record exists.
2. **Gather all `compass.untribal.engagement` records in the window.** Apply the [Everest 118](../NEXT_200_EVERESTS.md) decay function with `recent_decay_factor = 0.7` for evidence in the last 6 months (Goodhart defense — see §7).
3. **For each declared category**, count the evidence pieces referencing it.
4. **Apply counter-evidence nullification.** For each declared category, check the chain for any accepted harm-claim ([Everest 119 counter-evidence handling](../NEXT_200_EVERESTS.md)) directed at a member of that category, authored by the principal or peer-attested with the principal having declined to dispute within the rebuttal window. A single nullifying counter-evidence record zeros out the category's positive-evidence count.
5. **Apply the peer-attested fraction floor.** A category passes only if at least `peer_attested_fraction_required` of its non-nullified evidence pieces are peer-attested.
6. **Count categories that pass.** A category "passes" if (a) it has ≥ `M` non-nullified, decay-weighted evidence pieces, AND (b) the peer-attested fraction is satisfied.
7. **Evaluate the predicate.** Return `true` if `passing_category_count ≥ N`. Return `false` only if the principal has explicitly declared (via a chained `compass.untribal.declaration.declined` record) that they refuse the predicate. Otherwise return `unknown`.

The asymmetry between `true` (requires positive evidence) and `false` (requires explicit declination) is intentional: absence of evidence is not evidence of absence. A principal who has not authored evidence returns `unknown`, not `false`. The counterparty learns the principal does not currently attest the pattern; they do not learn the principal lacks the pattern.

### 5. Privacy: the category-set leak problem and its defense

A principal's declared category list is among the most sensitive content in V. It reveals what differences the principal considers significant in their world, which is itself often a protected-class proxy. A list including "denominational religious / secular" reveals the principal cares about that axis; a list including "rural / urban" reveals a different self-understanding; combinations reveal more.

The defense is layered:

**Layer 1 — Encryption at rest.** The declared list is encrypted under a key derived from the principal's master key. Even if V's storage is exfiltrated, the declared list is not recoverable without P's authentication.

**Layer 2 — Σ-protocol over Pedersen-committed evaluation.** The proof envelope's circuit ([Everest 117 evidence aggregation primitive](../NEXT_200_EVERESTS.md), inheriting the Witness Σ-protocol pattern) commits the principal's declared list as input to evaluation and outputs only the predicate's tri-value. The verifier learns the evaluation was performed honestly against *some* principal-declared list at the committed chain height, but learns nothing about the list's contents, length, or category names.

**Layer 3 — No N, M, or count disclosure.** The proof reveals the tri-value only. The verifier cannot learn `N`, `M`, the `passing_category_count`, the total evidence count, or which categories passed. Two principals with very different declared lists, very different evidence pools, and very different N/M thresholds may both return `true`; the verifier cannot distinguish them by anything other than identity (and the principal-protective inversion already gives the verifier identity through the CredexAI VC binding).

**Layer 4 — Cross-relationship unlinkability** ([Everest 156 selective disclosure](../NEXT_200_EVERESTS.md), inheriting [G2 from Everest 101](everest_101_compass_problem_statement_threat_model.md)). Two disclosures of the predicate to different counterparties cannot be cryptographically linked to a shared underlying evidence pool, even if both return `true`. Each proof is bound to a fresh nonce and a chain-head anchor; verifiers cannot triangulate across disclosures.

**Layer 5 — Plausible deniability of non-disclosure** ([G5 from Everest 101](everest_101_compass_problem_statement_threat_model.md)). A counterparty who receives uniform-204 cannot tell whether the principal is not enrolled, has not declared categories, has not authored evidence, has not consented to this counterparty class, has refused this specific request, or has had the predicate evaluate to `false`. The counterparty learns nothing about which kind of non-disclosure they are seeing.

**Residual risk:** A counterparty who already knows independent facts about the principal can combine those facts with a returned `true` to infer the principal's category set partially. (E.g., a counterparty who knows P writes about rural-urban politics and observes a `true` may guess "rural / urban" was on the declared list.) The protocol does not increase the counterparty's knowledge beyond what they already had; it only confirms a pattern. This residual risk is acknowledged in [Everest 101's threat model A11 (misuse-via-aggregation)](everest_101_compass_problem_statement_threat_model.md) and A12 (tribal-affiliation outing). It is not solvable cryptographically; the defense is the protocol's structural refusal to expose category names, count, or list length.

### 6. The Goodhart problem and its (partial) defenses

> *"When a measure becomes a target, it ceases to be a good measure."* — Goodhart's law, in the form Strathern restated.

Any predicate that returns a single bit on a desirable trait, given enough motivation, will be gamed by some principals. The defense is not to make gaming impossible — that is not achievable — but to make sustained gaming expensive and detectable.

**Defense 1 — Peer-attested fraction floor.** Half of evidence pieces must be peer-signed. A peer who attests falsely commits their own credibility on the chain; their attestations are auditable and revocable; a peer caught attesting falsely once loses standing for future attestations they sign across the entire Compass surface. Two-party collusion succeeds within the protocol (this is acknowledged in [Everest 101 A19](everest_101_compass_problem_statement_threat_model.md)); N-party collusion across N independently-credentialed peers is increasingly expensive.

**Defense 2 — Counter-evidence nullification asymmetry.** A single accepted harm-claim toward a member of a category zeros out all positive evidence in that category. The asymmetry is intentional: positive engagement accrues slowly across many records; a single harm refutes the pattern's claim. The principal's recourse is the [counter-narrative provision (Everest 168)](../NEXT_200_EVERESTS.md) and the defamation defense ([Everest 169](../NEXT_200_EVERESTS.md)); the harm-claim can be contested through DERB processes. But the predicate's evaluation does not paper over harm with abundance of opposite evidence.

**Defense 3 — Recent-evidence decay.** Evidence in the last 6 months is weighted 0.7. A principal who suddenly starts authoring engagement records at a high rate, perhaps in advance of a known Compass query, cannot inflate their way to `true` purely through recent activity; the predicate's weight is on the multi-year pattern. A flurry of recent records absent prior records returns `unknown`, not `true`. This contradicts the natural intuition that recent evidence is most reliable; the predicate's design accepts that for *character* predicates over multi-year windows, recency is the gaming signal, not the reliability signal.

**Defense 4 — Public-record anchoring.** The `public_record` evidence class ([Everest 115](../NEXT_200_EVERESTS.md)) anchors evidence to externally-verifiable facts (signed contracts, donations, public statements, op-eds, transparency-log-published artifacts) whose hashes are committed without the contents being re-published. Public-record evidence cannot be fabricated after the fact; if a principal claims advocacy via an op-ed, the op-ed's hash and publication metadata must reconcile with the public record.

**Defense 5 — Audit trail of the declared list.** A principal who manipulates their declared list to inflate apparent crossings (e.g., declaring categories that produce easy-pickings rather than the categories that matter) creates an audit trail. The chain remembers list revisions. A principal whose declared list changes immediately before evaluation, in ways that strain credibility, surfaces in DERB review and in [annual review (E187)](../NEXT_200_EVERESTS.md). This is a sociological defense, not cryptographic — it depends on someone bothering to audit — but it is structurally available.

**What the defenses do not prevent:** A patient, motivated, well-resourced gamer who is willing to author years of false engagement records, recruit peer-attesters who are themselves credible, avoid documented harms toward the declared categories, and refrain from list-revision tells, can produce a `true` result. The protocol cannot prevent this. The defense at that scale is the [evidence honesty mechanism (E121)](../NEXT_200_EVERESTS.md): the chain remembers; later contradicting evidence is auditable; sustained falsification creates structural exposure that compounds over time. v0 accepts that for sufficiently committed adversaries, the bit can be gamed, and v0 documents this as a residual risk in §Open Questions and in [Everest 101 A19](everest_101_compass_problem_statement_threat_model.md).

### 7. The cross-cultural problem and v0's acknowledged limit

The framing of "untribal" reads as a Western liberal virtue. In cultures where family-loyalty, in-group-solidarity, or collective-honor are paramount, the predicate's basic shape — "evidence of engagement across the differences you yourself name as significant" — may not register as a *virtue* at all. A principal whose tradition treats the maintenance of in-group bonds as the core ethical work may reasonably refuse to enroll in this predicate, and the protocol must not stigmatize the refusal.

v0 addresses this in three structural ways and one explicit non-resolution:

1. **Principal-defined categories.** The principal supplies the categories. A principal whose meaningful crossings are within their own tradition (across generation, across class within community, across role within family) declares those categories. The predicate is principal-relativized; the protocol does not impose the Western liberal framing of "tribe" onto the declaration.

2. **Opt-in.** Compass enrollment is opt-in ([Everest 101 §Principal-Protective Inversion](everest_101_compass_problem_statement_threat_model.md)); per-predicate enrollment is also opt-in. A principal who does not enroll in this predicate returns uniform-204 to all queries; the counterparty cannot tell the difference between non-enrollment, declared-decline, and any other non-disclosure state.

3. **Uniform-204 on refusal.** A principal who has enrolled but never authored evidence for this predicate returns the same uniform-204 to counterparties as a principal who declined to enroll. There is no protocol-defined stigma for the absence.

4. **Acknowledged non-resolution.** v0 explicitly accepts that the predicate's framing is culturally situated and that its adoption may be uneven across jurisdictions. The [cross-cultural values mapping framework (Everest 115)](../NEXT_200_EVERESTS.md) defines the process for jurisdiction-specific predicate adaptation; v0 does not ship adapted vocabularies. A jurisdiction that finds the predicate culturally inappropriate may, through its DERB representation, file a `tombstone_in_jurisdiction` request that, if accepted, marks the predicate inactive in that jurisdiction's predicate registry mirror. v0 does not yet have the registry-mirror infrastructure to enforce per-jurisdiction tombstoning; the principal's own choice not to enroll is the v0 defense.

The honest acknowledgment: this predicate is the most culturally-situated in the Compass v0 set. It will fit some principals' self-understanding well and will fit others' poorly. The protocol's job is to make refusal costless, not to make the predicate universal. If v1 finds the predicate is broadly refused outside its origin culture, v1 should either restructure it or tombstone it.

### 8. NOT-FOR list (specific to this predicate, in addition to the Compass not-for list inherited from [Everest 106](../NEXT_200_EVERESTS.md))

The default-consent matrix for this predicate is `deny` for all of the following counterparty classes / use-types, *without override possible by principal consent* (deny-permanently, not deny-by-default):

| Counterparty class / use | Disposition | Rationale |
|---|---|---|
| Hiring decisions | `deny_permanently` | Re-creates discrimination harm regardless of which "side" of an axis the principal is on. A `false` is a hiring negative; a `true` is a hiring filter. Both reproduce bias. |
| Immigration / visa adjudication | `deny_permanently` | Government use of cross-group engagement as a civic-status criterion is the social-credit-score archetype. |
| University admissions | `deny_permanently` | Admissions decisions based on character-attested cross-group engagement re-create the affirmative-action discourse with the protocol as the new instrument. |
| Security clearances | `deny_permanently` | Loyalty-screening surface; protocol must not become an investigative tool. |
| Ad targeting | `deny_permanently` | Commercial use of attested cross-group engagement is surveillance capitalism with a privacy wrapper. |
| Jury selection | `deny_permanently` | Voir-dire use re-creates protected-class proxying in court proceedings. |
| Anonymous counterparties | `deny_permanently` | No verifiable counterparty class; cannot satisfy consent transitivity ([Everest 8 A8](everest_08_consent_calculus_axioms.md)). |
| Population analytics | `deny_permanently` | Aggregation across principals re-creates social-credit-score harm at population scale ([Everest 101 §Out-of-Scope](everest_101_compass_problem_statement_threat_model.md)). |
| Insurance underwriting | `deny_permanently` | Insurance class is permanently denied across all Compass predicates ([Everest 107](../NEXT_200_EVERESTS.md)). |

The default-consent for other classes (peer-AI collective, family, journalistic, financial, governmental other than the permanent-deny categories) is `deny` (requires explicit per-counterparty principal consent), and the principal can grant — but the *permanent-deny* categories above cannot be enabled by principal consent. They are protocol-level refusals, not principal-choice defaults. This is the strongest form of NOT-FOR list in v0.

### 9. DERB pre-clearance required

This predicate, per [Everest 165 (Compass DERB pre-clearance)](../NEXT_200_EVERESTS.md), must pass DERB review **before shipping**. The character layer's failure modes are too severe for ship-then-review.

DERB review for this predicate specifically must include:

1. **Affected-population peer member as load-bearing voice.** The DERB's mandatory affected-community representation ([Everest 80](everest_80_ethics_review_board.md) Composition §6) extends here: at least one DERB member must have direct lived experience of being on the wrong side of "tribal" framings — a member whose community has been historically targeted by majority categorizations. Their dissent on this predicate is load-bearing; ship is blocked on their objection unless the objection is published verbatim and explicitly addressed.

2. **Cross-cultural review.** DERB must include or formally consult at least two reviewers from cultural contexts substantially different from the v0 authors' (United States, Western liberal-academic). Their published assessment is part of the shipping packet.

3. **Disability-rights review.** Per [Everest 134](../NEXT_200_EVERESTS.md), one outside reviewer with disability-rights expertise; neurodivergence is one of the most common principal-declared crossing-categories and the predicate's interaction with disability framing must be reviewed.

4. **Civil-rights / ethics review.** Per [Everest 134](../NEXT_200_EVERESTS.md), one outside reviewer with civil-rights expertise.

5. **Published deliberation.** DERB's deliberation on this predicate is published verbatim (per [Everest 80 Review Process](everest_80_ethics_review_board.md)). Dissenting opinions are published alongside the majority. The principal's reading public can audit the design's review.

6. **Annual re-review.** This predicate is included in the [annual review (Everest 187)](../NEXT_200_EVERESTS.md) by name. The Compass authors commit, in v0, to re-opening this predicate annually for the first three years (2027, 2028, 2029) regardless of whether there is cause to revise — the predicate is too consequential to ship and forget.

If DERB declines clearance, the predicate is not shipped in v0. It is parked, the parking notice is published, and the cross-protocol composition ([Everest 145](../NEXT_200_EVERESTS.md)) for this predicate is left unimplemented. v0 ships without this predicate before v0 ships with a DERB-unreviewed version.

---

## Algorithm (canonical pseudocode for [Everest 150 determinism harness](../NEXT_200_EVERESTS.md))

```
fn untribal_engagement_pattern_evidenced(
    chain: &Chain,
    window: Duration,
    params: UntribalParams,  // N, M, peer_attested_fraction, recent_decay
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

    // Step 4: gather counter-evidence (accepted harm-claims toward
    //         declared-category members).
    let nullified_categories = gather_nullified(chain, window, category_set);

    // Step 5: per-category evaluation.
    let mut passing_count = 0;
    for cat_idx in 0..category_set.len() {
        if nullified_categories.contains(cat_idx) { continue; }

        let cat_records = engagements.filter(r => r.category_index == cat_idx);
        let weighted_count = apply_decay(cat_records, params.recent_decay);

        if weighted_count < params.M { continue; }

        let peer_fraction = cat_records.peer_attested_fraction();
        if peer_fraction < params.peer_attested_fraction { continue; }

        passing_count += 1;
    }

    // Step 6: predicate evaluation.
    if passing_count >= params.N { TriValue::True }
    else { TriValue::Unknown }  // never False except via explicit decline
}
```

The algorithm is deterministic and stateless over the chain. The [determinism harness (Everest 150)](../NEXT_200_EVERESTS.md) will verify bit-stability over fixed inputs across implementations.

The Σ-protocol wrapping the algorithm reveals only the `TriValue` output. The verifier's view is: bit + chain-head freshness anchor + per-disclosure nonce. Nothing else.

---

## Alternatives Considered

**Alt-1: Protocol-enumerated identity categories (rejected).** Ship a canonical list of categories ("political left/right," "rural/urban," "religious/secular," etc.) the predicate evaluates against. Rejected because this re-creates exactly the not-for-list harm Compass refuses; ships the protocol into the politics-of-categorization business; makes the protocol an instrument of whatever cultural moment authored the canonical list; ages catastrophically as the cultural moment changes. The principal-defined design is strictly stronger.

**Alt-2: Census-derived demographic categories (rejected).** Use existing demographic categories (US Census categories, EU eurobarometer categories, etc.) as the canonical list. Rejected for the same reasons as Alt-1 plus: census categories are themselves political artifacts of specific jurisdictions, do not translate across borders, and incorporate the categorization harms of their origin.

**Alt-3: Behavior-only, no category reference (rejected).** Define the predicate as "engaged constructively with N distinct people whose backgrounds the principal has documented as differing from theirs," with no category structure. Rejected because the predicate then degenerates into "the principal has documented N distinct people" — there is no way to verify the differences are *different* (they might all be the same difference, repeated). The category structure, however principal-defined, is load-bearing.

**Alt-4: Continuous score on diversity-of-engagement (rejected).** Output a [0,1] continuous score rather than a bit. Rejected because: (a) it re-creates the social-credit-score failure mode the Compass threat model exists to refuse ([Everest 101 §Privacy Guarantees](everest_101_compass_problem_statement_threat_model.md) and §Out-of-Scope); (b) it invites threshold-setting by counterparties; (c) it implies precision the evidence does not support. v0 commits to single-bit predicates.

**Alt-5: Public registry of categories with privacy-preserving query (rejected).** Maintain a public list of acceptable categories, with the principal's declared subset as a private commitment; queries return "P crossed at least N from the public list." Rejected because the public list is exactly the categorization harm refused above; the privacy-preserving wrapper does not redeem the underlying categorization act.

**Alt-6: No predicate (considered seriously).** Refuse to ship `untribal_engagement_pattern_evidenced` in v0; defer to v1; ship the rest of the Compass predicate vocabulary without this one. The route map's note ("This is the trickiest predicate in the v0 set") acknowledges this option was considered. The argument for inclusion: the predicate addresses a real question that real partners (Tale VI's Nia and Idris) actually ask each other, and shipping the rest of Compass without this predicate leaves a gap that other parties will fill with worse tools (counterparty-side inference from social-media data, third-party scoring services, public-records aggregation). The argument for exclusion: this predicate is the highest-risk in the v0 set; shipping it imperfectly may be worse than shipping nothing. **v0 ships the predicate conditional on DERB pre-clearance.** If DERB declines, v0 ships without it. The principal-protective inversion is preserved either way.

---

## Migration Path

This predicate is new in Compass v0; there is no migration path *to* it. The migration path *from* it: the [predicate ID registry (Everest 133)](../NEXT_200_EVERESTS.md) treats this ID as append-only. Semantic changes mint a new ID (`cwv.v1.untribal_engagement_pattern_evidenced` or `cwv.v0.untribal_engagement_pattern_evidenced_v2`). The original ID is preserved in the registry forever-readable.

**Tombstoning path.** If post-ship review (annual review per E187, or DERB emergency review) finds the predicate is producing harm at scale that outweighs its value, the ID can be marked `tombstoned` per [Everest 133 §Tombstoning](../NEXT_200_EVERESTS.md). Proofs against tombstoned IDs are rejected by reference verifiers going forward. The chain history of disclosures-against-tombstoned-predicates remains, marked as such; principals' chains are not edited. This predicate is the most likely v0 predicate to be tombstoned; the design ships with the tombstone path explicitly available.

**Per-jurisdiction tombstoning.** If [Everest 164 (cross-jurisdiction legality matrix)](../NEXT_200_EVERESTS.md) or [Everest 187 (annual review)](../NEXT_200_EVERESTS.md) finds the predicate is culturally inappropriate in a specific jurisdiction, the jurisdiction's predicate-registry mirror can mark it `tombstoned_in_jurisdiction`. Counterparties in that jurisdiction reject proofs against it. v0 does not ship the registry-mirror infrastructure; per-jurisdiction tombstoning is a v1 capability.

---

## Design Implications & Connections

**Connection to [Everest 59 (`cognitively_atypical_baseline`)](everest_59_cognitively_atypical_baseline.md).** This predicate inherits the principal-narrated, declaration-based pattern E59 established. E59: the principal declares their own cognitive baseline; the protocol does not impose a clinical taxonomy. E136: the principal declares their own crossing-categories; the protocol does not impose an identity taxonomy. Same epistemic move at a different layer. Both are load-bearing examples of the principal-protective inversion: the principal is the authoritative voice on what the predicate is about in their case.

**Connection to [Everest 101 threat model](everest_101_compass_problem_statement_threat_model.md).** This predicate is the test case for the threat model's hardest claims. Adversary A12 (tribal-affiliation outing) is specifically named in the threat model and is the primary adversary this predicate must defend against; A11 (misuse-via-aggregation) is the residual risk; A13 (pathologizing of dissent) is the design pressure DERB pre-clearance defends against; A19 (peer-attestation collusion) is the limit case the peer-attested-fraction floor partially mitigates. If this predicate's design holds, the threat model's commitments hold under stress; if this predicate fails the design problems, the threat model needs revision.

**Connection to [Everest 106 vocabulary not-for list](../NEXT_200_EVERESTS.md).** This predicate is the existence-proof that a values predicate can be authored without enumerating any of the not-for categories. If the not-for list refused political affiliation, religion, etc., and an `untribal` predicate could not exist without naming them, the protocol family would be incomplete. v0's resolution — principal-defined categories committed privately — is the structural answer. Future values predicates that face similar problems should follow this pattern.

**Connection to [Everest 145 composition (AND/OR)](../NEXT_200_EVERESTS.md).** This predicate composes with other Compass predicates under AND/OR. A compound disclosure like `untribal_engagement_pattern_evidenced ∧ truth_telling_evidenced` is one proof revealing two bits. The Σ-protocol's privacy guarantees compose: the verifier learns the conjunction without learning either input separately. Per [Everest 145](../NEXT_200_EVERESTS.md), the principal authorizes the conjunction explicitly; consent for the components does not imply consent for the conjunction.

**Connection to [Everest 187 annual review](../NEXT_200_EVERESTS.md).** This predicate is flagged for mandatory re-review each year of v0 (2027, 2028, 2029) regardless of cause. The annual review's published output names this predicate explicitly: what evidence has the protocol's first year of operation produced about whether the predicate is doing its work, whether the encoding is holding, whether the cross-cultural mismatch is being handled?

**Connection to [Everest 165 DERB pre-clearance](../NEXT_200_EVERESTS.md).** This predicate is the canonical case for why pre-clearance exists. The character layer's failure modes here are severe enough that ship-then-review is unsafe. DERB's affected-population peer member is the load-bearing voice; their dissent is not advisory but blocking.

---

## Open Questions

These remain open for the [annual review (Everest 187)](../NEXT_200_EVERESTS.md) or subsequent design passes. They do not block this Everest's acceptance.

1. **What does the predicate do when the principal's declared list is empty?** A principal may, in good faith, declare zero categories (asserting they live in a context where category structure does not apply, or they are at a life stage where engagement-across-difference is not the relevant ethical work). v0 returns `unknown` for an empty list. Whether this is the right default — vs., e.g., a flag indicating "principal asserts the predicate is not applicable to their context" — is open.

2. **What is the right minimum window?** v0 sets the window adjustable from 12 to 120 months. A 12-month window is short for character-pattern evaluation; a 120-month window is long enough that older evidence may not reflect current pattern. The decay function partially handles this, but the window choice is a design tension the annual review should revisit.

3. **How does the predicate compose with the [`character_compare(predicate, peer)` predicate (Everest 148)](../NEXT_200_EVERESTS.md)?** Two principals can prove their characters "agree" on a Compass predicate. For this predicate, "agree" is non-obvious: do they agree on the bit, or do they agree on a shared declared-category set? v0 says "agree on the bit"; v1 may want to refine.

4. **What is the right defense if a peer-attester is themselves later compromised or found to be inflating credibility?** The chain remembers peer attestations; if a peer is later marked unreliable, all attestations they signed are affected. v0 does not yet specify whether downstream predicate evaluations retroactively re-evaluate against the marked-unreliable peer's prior attestations. This is part of the broader [Everest 119 counter-evidence handling](../NEXT_200_EVERESTS.md) question; this predicate inherits whatever resolution that Everest reaches.

5. **What if a counterparty publicly leaks the bit from a disclosure they received?** The protocol does not prevent leak; consent transitivity ([Everest 8 A8](everest_08_consent_calculus_axioms.md)) makes the leak a license violation but not a cryptographic prevention. For this predicate specifically, a leaked `true` is potentially weaponizable (the counterparty leaks the bit to a hostile third party who then attempts to combine it with public records to infer category content). The defense is the residual-risk acknowledgment in §5 plus the [defamation defense (Everest 169)](../NEXT_200_EVERESTS.md) for the inverse case. Whether v0 should additionally implement a leak-detection mechanism is open.

6. **How does the predicate behave when the principal's own life situation changes such that previously-significant categories cease to be significant?** A principal who declared "rural / urban" while living in a rural community and then moved to a city after a decade may legitimately wish to revise their declared list. The chain remembers the prior declaration; the active list at any chain height is what the predicate uses. Whether old declarations should be respectfully archived (rather than just superseded) is a UX question and a DERB question.

7. **What is the protocol's response if a sufficiently large fraction of enrolled principals tombstone the predicate from their own use?** Aggregate refusal is a signal. v0 does not have a mechanism to detect aggregate refusal (the privacy properties prevent it — uniform-204 hides whether any individual principal has refused). The annual review may need to introduce voluntary, anonymized refusal-rate reporting to inform the design's evolution.

---

## Why This Matters

This predicate is the test case for whether Compass can ship a substantive character claim without ceding the categorization that Compass exists to refuse.

The naive design fails. A protocol that ships an "untribal" predicate by enumerating tribes participates in the categorization harm. A protocol that ships an "untribal" predicate by aggregating demographic data participates in the surveillance harm. A protocol that ships an "untribal" predicate as a numeric score participates in the social-credit-score harm. The route map's note that this is "the trickiest predicate in the v0 set" is accurate.

v0's resolution — principal-defined categories committed privately, peer-attested evidence with counter-evidence nullification, single-bit output through the Σ-protocol, DERB pre-clearance with affected-population peer member as load-bearing voice, mandatory annual re-review, permanent-deny for the highest-risk counterparty classes — is not a perfect resolution. The Goodhart problem is partially defended, not solved. The cross-cultural mismatch is acknowledged, not eliminated. The category-set leak risk is reduced to a residual, not eliminated. The peer-attestation-collusion vector remains.

But the resolution is honest about what cryptography can and cannot do. Cryptography can hide the principal's category set from the verifier. Cryptography cannot make the principal's chosen categories culturally universal. Cryptography can enforce the Σ-protocol's privacy. Cryptography cannot prevent a motivated patient adversary from gaming the metric over years. The design holds where it can hold and acknowledges what it must concede.

If this predicate ships and works — if Tale VI's Nia and Idris, in some future actual conversation, run this query and have the conversation it surfaces rather than the conversation they would have deferred — then the protocol family has demonstrated that a values claim about cross-difference engagement can be encoded without the categorization harm. That demonstration is what Compass is for.

If this predicate ships and fails — if it is gamed at scale, or used as a hiring filter despite the permanent-deny, or weaponized against minority-tradition principals whose self-understanding does not include "tribe" — then DERB tombstones it, the annual review publishes the failure, and the protocol family has demonstrated something also valuable: that some character claims cannot be encoded honestly, and that the protocol's refusal to ship a broken predicate is itself the principal-protective inversion in action.

Either outcome serves the protocol. The commitment is that the outcome is observable, the process is published, and the principal who chose to enroll retains the right to revoke without penalty at any time.

---

— Calm, 2026-05-20
