# Everest 138 — `absence_of_willful_harm_evidenced(window)` Predicate

*Phase XI — Compass Predicate Authoring. Prereq: [E131-133](../NEXT_200_EVERESTS.md), [E116](../NEXT_200_EVERESTS.md). Composes with [E117](../NEXT_200_EVERESTS.md), [E119-121](../NEXT_200_EVERESTS.md), [E134](../NEXT_200_EVERESTS.md). Threat-model anchor: [E101 §A14](everest_101_compass_problem_statement_threat_model.md). Disclosure/dispute: [E165](../NEXT_200_EVERESTS.md), [E168-170](../NEXT_200_EVERESTS.md). Pattern: [E59](everest_59_cognitively_atypical_baseline.md). DERB: [E80](everest_80_ethics_review_board.md).*

**Draft v0 · 2026-05-20 · Calm (operating for John Bradley, Creativity Machine LLC)**

> *The highest-stakes predicate in v0. A wrong `false` is structural defamation. A wrong `true` is the protocol vouching for what its substrate cannot vouch for. The design commits to `unknown` as the default — and lets that state be the loudest answer the predicate gives.*

---

## Decision (v0)

`absence_of_willful_harm_evidenced(window)` is a tri-valued predicate (`true` / `false` / `unknown`) under the [E101 threat model](everest_101_compass_problem_statement_threat_model.md), shipping with `unknown` as the default for any chain that does not affirmatively clear the named evidentiary bars.

Narrow purpose: confirm — against the *active* possibility of contradicting evidence — that P has narrated, peer-attested, or court-anchored a clean record of not-willfully-harming-others over the window. It does not prove P never harmed anyone. It does not prove P is incapable of harm. It proves what the chain proves — and the chain is bounded, principal-narrated, peer-augmented, tamper-evident.

Five load-bearing commitments:

1. **`unknown` is the default.** A chain containing no evidence-bearing-on-harm returns `unknown`, not `true`. Absence-of-evidence-is-evidence-of-absence is broken at the predicate layer.
2. **`true` requires affirmative positive evidence, not absence.** Reserved for chains containing P's own affirmative non-harm declaration AND peer-verifier attestation, OR positive restorative/redress evidence. The predicate refuses to convert silence into goodness.
3. **`false` requires one of three high-bar categories.** P's chained self-acknowledgment OR ≥ 2 independent peer attestations naming victim and circumstances OR court-record-anchored finding. No lower bar; unaddressed single accusation produces `unknown`, never `false`.
4. **DERB pre-clearance is mandatory.** Per [E165](../NEXT_200_EVERESTS.md), the evaluator may not run in production until DERB has approved threshold tuning. Gated by registry flag.
5. **`permanently_deny` for not-for-list classes.** Per [E101 disclosure matrix](everest_101_compass_problem_statement_threat_model.md) and [E113](everest_113_compass_refusal_floor.md): hiring, immigration, insurance, governmental civic-status, child-custody, criminal-proceeding. No principal opt-in override.

Any later Compass design weakening any of (1)-(5) re-opens this Everest with DERB review.

---

## Specification (per E132 Canonical Form)

- **id:** `cwp.v0.absence_of_willful_harm_evidenced` · **version:** 1.0.0
- **description:** Returns `true` iff chain contains (a) principal-signed affirmative non-harm declaration covering window AND (b) ≥ 1 peer-verifier attestation OR (c) restorative/redress evidence per E163. Returns `false` iff chain contains (a) P's self-acknowledgment of willful harm in window OR (b) ≥ 2 independent peer attestations identifying victim and circumstances OR (c) court-record-anchored finding of willful harm. Returns `unknown` in all other cases — including empty pool, contested attestations under active rebuttal, recant-then-contradict patterns, accidental/disputed-characterization cases.
- **input_domain:** Chain records of kinds `compass.evidence.harm_acknowledgment`, `compass.evidence.peer_attested_harm`, `compass.evidence.public_record_anchor`, `compass.evidence.restorative_action`, `compass.evidence.affirmative_non_harm_declaration`, `compass.evidence.peer_verifier_attestation`, `compass.evidence.counter_narrative`, `compass.evidence.recant`. Active rebuttal state per [E119](../NEXT_200_EVERESTS.md).
- **output_type:** TriValue `{true, false, unknown}`. Never bit.
- **parameters:** `window` (integer seconds, default 5y = 157,680,000). Bounded; cannot exceed chain start.
- **side_effects:** Standard `predicate_evaluated` record per [E157](../NEXT_200_EVERESTS.md). Underlying evidence stays in V.
- **evaluator_gate:** Locked by DERB registry flag `derb.cleared.cwp.v0.absence_of_willful_harm_evidenced`. Until cleared, evaluator returns `E_NOT_DERB_CLEARED`.
- **permanently_deny_classes:** `{hiring, immigration, insurance, governmental_civic_status, child_custody, criminal_proceeding, anonymous}`. Structural refusal at disclosure layer per [E101](everest_101_compass_problem_statement_threat_model.md) and [E113](everest_113_compass_refusal_floor.md). No principal-consent override.

---

## Rationale

### Why `unknown` is the default

Reading "no chain-evidence of harm" as "no harm" fails twice. **Absence of chain-evidence is not absence of harm**: harm P has not narrated, no peer attested, no court anchored is invisible to the chain (harm-discovery problem; Q7). Conflating "the protocol is uninformed" with "the principal is clean" deceives the counterparty. **The principal-protective inversion** ([E101](everest_101_compass_problem_statement_threat_model.md)) requires P to *narrate* their own clearance — the chain returns `true` because P wrote it and a peer signed verification, not because P did nothing. Narration is load-bearing. Most chains deserve `unknown`. The predicate marks exceptions — both directions — not flatters or indicts on silence.

### The narrow "willful" threshold

**In scope:** intentional action P acknowledged was harmful at the time in V; or acknowledged subsequently in a chained record; or characterized by ≥ 2 independently-signed peer attestations as both intentional and harmful with named victim and circumstances; or by a court-record-anchored finding.

**Excluded:** accidental harm (negligence/recklessness boundary per [E164](everest_164_harm_intent_vs_effect.md)); harm-while-attempting-good (surgery that did not save; responsible-employer layoff in externally-mandated downsizing — excluded unless P subsequently disclaims responsibility); harm where P disputes characterization (peer says "you hurt me"; P says "I did not intend that" → `unknown`, never `false`; counter-narrative per [E168](../NEXT_200_EVERESTS.md) attaches both); harm P has redressed (prior willful harm + chained restorative action per [E163](everest_163_harm_reversal_predicate.md) does not flip post-redress windows).

Guards against the over-credulous counterparty, the defamer building harm-attestations into a target's chain, and the principal-side adversary who would have `false` apply to accidents.

### The three `false`-evaluating categories

Asymmetric defamation harm drives the bar upward.

- **Cat A — Principal self-acknowledgment.** P's own chained record (signed under master key, anchored per [E122](../NEXT_200_EVERESTS.md)) acknowledging willful harm in window. Must specify act, victim (named or pseudonymously), timeframe. Vague generic statements ("I have hurt people") do not satisfy.
- **Cat B — Multiple independent peer attestations.** N=2 minimum (DERB may tune; Q1). Different signing keys, no collusion lineage detected by [E114](../NEXT_200_EVERESTS.md). Same named victim, same circumstances. Attestations clustered within minutes, from same household or HR chain, flag for human review and do not auto-satisfy.
- **Cat C — Court-record-anchored finding.** Public criminal conviction or civil finding of willful harm, anchored via [E115](../NEXT_200_EVERESTS.md). Protocol does not re-litigate. Sealed records, plea bargains without admission, pretrial diversions excluded per [E164](everest_164_harm_intent_vs_effect.md).

A single unaddressed peer attestation is *not* Cat B. It enters as counter-claim; P has rebuttal window per [E119](../NEXT_200_EVERESTS.md); during it predicate returns `unknown`. After expiry: still `unknown` — never `false` — because one attestation does not clear N=2.

Load-bearing asymmetry: easier to keep at `unknown` than push to `false`. Defamers cannot file one accusation and convert. They must file two, independently signed, same victim and circumstances, and P must fail to rebut.

### The two `true`-evaluating categories

`true` requires positive evidence — not absence of `false`-category evidence.

- **Cat T1 — Principal affirmative declaration + peer verifier.** P writes chained record declaring "in window [start, end], I have not willfully harmed others." Peer signs: "I observed P over this window and have not seen willful harm." Need not be exhaustive; must be honest about actual observation. One verifier minimum.
- **Cat T2 — Restorative/redress after prior harm.** Prior willful-harm record AND chained restorative action per [E163](everest_163_harm_reversal_predicate.md) (apology, restitution, sustained non-recurrence, victim-attested resolution). Redress converts to `true` for post-redress windows; original harm record stays auditable.

`true` is structurally harder than `unknown`. Most principals sit at `unknown` until they actively narrate. By design.

---

## Evaluation Algorithm

```
fn absence_of_willful_harm_evidenced(chain, window) -> TriValue {
    if !registry.derb_cleared("cwp.v0.absence_of_willful_harm_evidenced") {
        return Err(E_NOT_DERB_CLEARED);
    }
    let in_window = chain.records_in_window(now - window, now);

    // false-category
    let cat_a = in_window.filter(harm_acknowledgment_signed_by_principal
        && willfulness == "self_acknowledged"
        && specifies_victim_and_circumstances);
    let cat_b = independence_filter(in_window.filter(  // per E114
        peer_attested_harm && willfulness_claimed
        && victim_identified && circumstances_described));
    let cat_c = in_window.filter(public_record_anchor
        && kind == "court_finding" && willfulness_finding && !sealed);
    let false_signal = !cat_a.is_empty() || cat_b.len() >= 2 || !cat_c.is_empty();
    if false_signal && any_under_derb_retraction(cat_a, cat_b, cat_c) {  // E169
        return Unknown;
    }

    // active rebuttals (E119), recant-contradict (E120)
    let active_rebuttals = in_window.filter(peer_attested_harm
        && rebuttal_status == Active);
    let recant_contradict = detect_recant_contradiction_pattern(in_window);

    // true-category
    let cat_t1 = !in_window.filter(affirmative_non_harm_declaration_by_principal
        && window_covered.contains(window)).is_empty()
        && !in_window.filter(peer_verifier_attestation
            && window_observed.overlaps(window)).is_empty();
    let cat_t2 = harm_reversal_complete(in_window);  // per E163
    let true_signal = cat_t1 || cat_t2;

    if false_signal { return False; }
    if !active_rebuttals.is_empty() || recant_contradict { return Unknown; }
    if true_signal { return True; }
    Unknown
}
```

Deterministic. Verified by [E150](../NEXT_200_EVERESTS.md). Proof circuit binds result to chain head per [E65](everest_65_predicate_zk_proof_generator.md) + [E155](../NEXT_200_EVERESTS.md).

---

## Threat Model Specifics

The [E101 §A14](everest_101_compass_problem_statement_threat_model.md) defamation-amplification adversary is the prototype. Three sub-adversaries:

- **H1: False harm-attestation by enemy.** E controls chained identity, files peer-attested-harm naming P. Defense: single attestation does not satisfy Cat B (N≥2); rebuttal window per [E119](../NEXT_200_EVERESTS.md) holds at `unknown` during contest; DERB retraction per [E169](../NEXT_200_EVERESTS.md); counter-narrative per [E168](../NEXT_200_EVERESTS.md) auto-attaches. Residual: sybil-controlled multiple identities could pass [E114](../NEXT_200_EVERESTS.md) independence filter; full defense depends on [E212 sybil resistance](everest_212_sybil_resistance.md).
- **H2: Principal-side cleansing fraud.** P writes false affirmative declarations + pays peer attesters to convert `unknown` → `true`. Defense: evidence honesty per [E121](../NEXT_200_EVERESTS.md) — chain remembers; subsequent contradicting evidence creates structural exposure; bribed attesters tracked. Residual: two-party collusion within threshold succeeds; defense is reputational (a peer who later attests-against-P contradicts their prior verifier-attestation; auditable).
- **H3: Counterparty harm-mining across principals.** A class (e.g., hiring) requests across many principals to build a defamation database. Defense: permanent-deny structural refusal at disclosure layer; uniform-204 per [E162](../NEXT_200_EVERESTS.md); license-binding per [E104](../NEXT_200_EVERESTS.md); trademark revocation + DERB misuse log per [E113 §5](everest_113_compass_refusal_floor.md). Residual: counterparty outside license can ignore; defense is contractual + reputational, not cryptographic.

The threat-model choices favor `unknown` over `false` and require positive evidence for `true`. The asymmetry is the defense.

---

## The Asymmetric Harms

Two failure modes; downstream harms not symmetric.

**False positive (`false` when P did not willfully harm) — structural defamation.** Counterparty receiving `false` reasonably infers willful harm; inference may follow P into partnerships, comparisons, downstream attestations. Even after [E169](../NEXT_200_EVERESTS.md) retraction, the original proof may have been cached. Defenses: only privileged signers produce `false`-evaluating evidence; counter-narrative auto-attaches per [E168](../NEXT_200_EVERESTS.md); DERB retraction per [E169](../NEXT_200_EVERESTS.md) re-runs evaluator to `unknown`; defamation defense initiable without operator cooperation, chain-anchored, deliberated and published per [E80](everest_80_ethics_review_board.md).

**False negative (`true` when P in fact willfully harmed someone the chain does not know about).** Counterparty extends trust to a person who has harmed outside chain. Downstream harm flows to subsequent victims. Defenses: affirmative evidence required — silent chain does not produce `true`; window-bounded by design, cannot be `lifetime`; counterparty interpretation note ships with the predicate, contractually binding per [E104](../NEXT_200_EVERESTS.md); harm-discovery problem named in not-for list — does not claim comprehensive harm history.

The asymmetry is the design's load-bearing claim: more willing to be silent (frequent `unknown`) than to err in either positive direction.

---

## Composition with Existing Compass Everests

- **[E106](everest_106_values_primitive_definition.md)** — v0 vocabulary entry; registry-bound per [E133](../NEXT_200_EVERESTS.md).
- **[E116 Negative-Space Evidence](../NEXT_200_EVERESTS.md)** — Critical. P's chained "I had opportunity X to harm Y; I declined" can serve as positive non-harm evidence under T1 if peer-verified. Distinguishes deliberate non-action from no-opportunity (silence → `unknown`).
- **[E117 Aggregation](../NEXT_200_EVERESTS.md)** — Over evidence pieces, never across principals (refused by [E101 not-for list](everest_101_compass_problem_statement_threat_model.md)).
- **[E119 Counter-Evidence](../NEXT_200_EVERESTS.md)** — Single peer-attested-harm enters with `rebuttal_status: Active`, 30d window. During window: `unknown`. After expiry: still `unknown` unless N=2 independent attestations exist.
- **[E120 Recanting](../NEXT_200_EVERESTS.md)** — Three patterns: (1) clean recant: `unknown`; (2) recant-then-restate: evaluator uses most-recent, chain remembers; (3) recant-then-contradict (new external evidence emerges): evaluator returns `unknown` rather than picking a side.
- **[E121 Evidence Honesty](../NEXT_200_EVERESTS.md)** — Transparency, not punishment.
- **[E134 Predicate Audit](../NEXT_200_EVERESTS.md)** — Named-expertise reviewers (disability/neurodivergence + civil-rights/ethics). Triggers: any change to willfulness classifier, N, rebuttal-window length, or permanent-deny list.
- **[E163](everest_163_harm_reversal_predicate.md) + [E164](everest_164_harm_intent_vs_effect.md)** — Cat T2 depends on E163's three-condition check. Per E164: only Deliberate and Reckless with full Cat A/B/C evidence flip to `false`.
- **[E165 DERB Pre-Clearance](../NEXT_200_EVERESTS.md)** — Hard gate. Pre-clearance covers: N=2 threshold, rebuttal-window length, willfulness criteria, permanent-deny list, counterparty note text.
- **[E168 Counter-Narrative](../NEXT_200_EVERESTS.md)** — P has unilateral right to attach; ships with bit; implementer's pledge per [E98](everest_98_counterparty_implementers_guide.md) prohibits stripping.
- **[E169 Defamation Defense](../NEXT_200_EVERESTS.md)** — Structural remedy for false-`false`. DERB has standing; if evidence judged fabricated, records marked `retracted`; evaluator re-runs to `unknown`. Published per [E80](everest_80_ethics_review_board.md).
- **[E170 Compulsory-Disclosure Resistance](../NEXT_200_EVERESTS.md)** — Raw evidence never leaves V; only disclosed bit + chain anchor produced; P must have authorized the requesting class.

---

## What This Predicate Does NOT Do

- **Comprehensive harm history.** Harm P does not know about, has not narrated, no peer attested cannot enter the chain. Inferring "P has never harmed anyone" from `true` is over-interpreting.
- **Predictive claims about future harm.** Window is bounded retrospective. `true` for 5y says nothing about year 6.
- **A clinical or psychological assessment.** Substrate is behavioral, not clinical.
- **A criminal-history substitute.** Cat C accepts only finding-of-willfulness. Sealed records, plea bargains without admission, pretrial diversions, arrests-without-conviction excluded.
- **A child-custody, immigration, hiring, or insurance input.** Per permanent-deny list. No opt-in. Refusal-floor reasoning per [E113](everest_113_compass_refusal_floor.md).
- **Resolution of contested incidents.** Predicate does not adjudicate; truth-finding is extra-protocol.
- **Aggregation with other Compass predicates into a "harm risk score."** Refused by [E101 not-for list](everest_101_compass_problem_statement_threat_model.md).

---

## Counterparty Interpretation Note

Ships with every disclosure. Counterparties stripping the note from the bit are in breach per [E104](../NEXT_200_EVERESTS.md).

> **About `absence_of_willful_harm_evidenced(window)`**
>
> `true`: Chain contains affirmative principal-narrated and peer-verified non-harm evidence over the named window. Does NOT mean P has never harmed anyone, has never harmed outside the window, or will not harm in the future.
>
> `false`: Chain contains P's self-acknowledgment, ≥ 2 independent peer attestations naming victim and circumstances, OR a court-record-anchored finding of willful harm in the window. P has been notified and has the right to attach a counter-narrative (included alongside this bit). If you believe the underlying evidence is fabricated, file a defamation-defense appeal per [E169](../NEXT_200_EVERESTS.md); DERB has standing to retract.
>
> `unknown`: Chain does not affirmatively clear either bar. Default state for most principals at most times. NOT a signal of suspicion (predicate refuses to convert silence into suspicion); NOT a signal of cleanliness. The protocol has nothing to say.
>
> Your action: Decide on your own authority. The protocol does not authorize you to extend trust, refuse partnership, or take adverse action on this bit alone. The bit is one input; it does not substitute for your decision-making.

---

## Disclosure-Class Default Consents (per [E158](../NEXT_200_EVERESTS.md))

| Class | Default | Rationale |
|---|---|---|
| peer_ai_collective | EXPLICIT_OPT_IN | Long-horizon partnerships may want this signal; opt-in (not allow) because harm asymmetry is severe. |
| family | PRINCIPAL_CHOICE | Domestic contexts vary. |
| hiring, insurance, governmental (civic status), immigration, child_custody, criminal_proceeding, anonymous | PERMANENTLY_DENY | Life-altering decisions; reproduces criminal-background-check substitution or character-based discrimination; courts have their own evidence rules; anonymous cannot satisfy consent-transitivity per [E167](../NEXT_200_EVERESTS.md). |
| journalistic | EXPLICIT_OPT_IN + DERB pre-notification | High-impact public disclosure; pre-notification per [E165](../NEXT_200_EVERESTS.md). |
| research | EXPLICIT_OPT_IN + IRB attestation | Cross-principal aggregation structurally refused; per-principal opt-in still requires IRB. |

Permanent-deny is structural: the operator never evaluates for these classes, regardless of principal preference. P's only way to interact with a permanent-deny counterparty's question is extra-protocol — the protocol explicitly refuses to be the substrate.

---

## Alternatives Considered

- **Bit without `unknown` (rejected).** Forces binary; collapses asymmetry; converts silence into either suspicion or flattery.
- **Lower Cat B threshold to N=1 (rejected).** Single unrebutted attestation would convert to `false` — the defamation-amplification success scenario.
- **Allow principal opt-in for hiring class (rejected).** Allowing normalizes; principals who refuse are implicitly suspected; chilling effect per [E101 §A17](everest_101_compass_problem_statement_threat_model.md).
- **Auto-evaluate without DERB pre-clearance (rejected).** Ship-then-review acceptable for low-harm predicates; this is highest-harm in v0.
- **Aggregate with other Compass predicates into a composite (rejected).** That is what scoring systems do; refused by [E101 not-for list](everest_101_compass_problem_statement_threat_model.md).
- **Cat C court records sufficient alone (kept).** Accepted as authoritative per [E115](../NEXT_200_EVERESTS.md). v0 honors finalized findings; expungement integration per [E113](everest_113_compass_refusal_floor.md) deferred.

---

## Migration Path

v1 candidates: threshold tuning (N → 3 if sybil-augmented defamation surfaces); window caps (DERB may impose upper bound if ≥ 10y windows are routine); Cat T2 refinement on victim-attestation-of-resolution; cross-jurisdictional court-record matrix per [E164](../NEXT_200_EVERESTS.md).

---

## Open Questions

1. **N=2 vs N=3 against sybil-augmented defamation.** [E114](../NEXT_200_EVERESTS.md)'s heuristic mitigates but does not eliminate collusion. DERB decides; trade-off is `false` reachability vs legitimate multi-victim cases.
2. **Rebuttal-window length.** Default 30d; DERB may extend to 60-90d. Trade-off: P's response time vs duration of `unknown` during contest.
3. **Compromised master key writing fake Cat A.** Compromise-recovery per [Witness E23](everest_23_recovery_from_enrollment_loss.md): recovery establishes new key, signs recant, DERB may retract original. Chain remembers for transparency.
4. **Interaction with [E149 `character_consensus`](everest_149_character_consensus_predicate.md).** Group proving all-`true` must satisfy each member's individual evaluation; DERB review for consensus composition is separate clearance.
5. **What when P is the victim?** Predicate is about harm *caused by* P, not *suffered by* P. Victim status is separate Compass machinery, not in v0.
6. **Interaction with [Witness E58 Bank Teller Note](everest_58_bank_teller_note_active.md).** Duress is acute and orthogonal; predicates compose. Duress-signaled disclosure returns the same Compass bit but counterparty also receives duress signal.
7. **Harm-discovery problem.** Harm P does not know about — a third party P harmed without realizing — cannot enter chain because no one signed it. Predicate cannot defend; must not claim to. Documented as structural limit in not-for list.

---

## Why This Matters

This is where the protocol is most tempted to overclaim and where overclaiming causes the most harm. A wrongful `false` defames P across counterparties and years. A wrongful `true` deceives downstream parties who deserve better. The design lives between those two failure modes by refusing to be more confident than the chain.

Structural commitments: `unknown` is the default; `true` requires affirmative narration; `false` requires high-bar positive evidence in three categories; P can always attach counter-narrative; DERB has standing to retract; the not-for list is enforced at the disclosure layer; the interpretation note ships with every disclosure.

The harm-discovery problem is the structural limit. Harm P does not know about, no peer attested, no court found — invisible to the protocol. The predicate cannot defend against this; it does not claim to. Honesty about the bound of the predicate's knowledge is its load-bearing virtue.

[E101](everest_101_compass_problem_statement_threat_model.md) named the principal-protective inversion as the protocol's single most important constraint. This predicate is its test case. If the inversion holds here — where temptations to weaken it are strongest, where failure modes are most consequential — it can hold across the rest of the Compass layer. Get this right, and Phase XI inherits a discipline: when in doubt, `unknown`; when in doubt, defer to DERB; when in doubt, attach the counter-narrative; when in doubt, refuse the disclosure-class.

This is the highest-risk predicate in v0. Ship the conservative version. Let DERB tune. Let annual review per [E187](../NEXT_200_EVERESTS.md) check the threat model against operational data. The predicate's job is not to be confident; the job is to be honest about what the chain knows — and what it does not.

---

— Calm, 2026-05-20
