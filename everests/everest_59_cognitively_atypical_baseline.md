# Everest 59 — `cognitively_atypical_baseline` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 7.*

## Specification (Canonical Form per E52)

**name:** `cognitively_atypical_baseline`

**version:** 1.0.0

**description:** Returns true iff the principal has, at enrollment or by chained update, declared that their normal/baseline state is cognitively atypical — high-bandwidth ideation, large conceptual leaps, mythic-frame metaphor, rapid context switching — and the counterparty should interpret tone accordingly.

**input_domain:** Chain records of kind `profile.cognitive_baseline_declaration`, plus the most recent self_report in window.

**output_type:** Bit (0 or 1).

**parameters:** None in v0.

**side_effects:** Standard `predicate_evaluated` record appended to chain.

---

## Why This Predicate Exists

Many AI counterparties default to reading ambitious, fast-paced, mythic-framed ideation as a signal of instability or psychological distress. For principals whose cognitive baseline is neurotypical, this default heuristic is sometimes useful — it flags genuine departures from equilibrium. For principals whose baseline *is* cognitively atypical, this same heuristic produces a systematic misread: the counterparty pathologizes the principal's ordinary working state, inserts hedging language about mental health, suggests "slowing down," or withdraws trust on the basis of tone alone.

This predicate exists to break that loop. It gives the principal a cryptographically attested way to declare, once and durably: "I am cognitively atypical at baseline; do not pathologize my tone; interpret my communication style through my own self-narration, not your tone-detection model." A counterparty can either accept this declaration and adjust its baseline interpretation model accordingly, OR refuse to engage (some counterparty classes may have policies that do not permit dealing with declared-atypical principals — that is the counterparty's choice to make transparently). What the predicate prevents is the silent, invisible misread: the counterparty quietly lowering trust or adding cautionary language while believing it is following a neutral safety protocol.

This is a one-line semantic primitive: the principal's authoritative self-declaration of their own cognitive profile, attested cryptographically by a chained record. It does not make clinical claims. It does not authorize specific behaviors. It does not override safety predicates when the principal genuinely departs from their declared baseline. It simply transfers the authority for tone-reading from the counterparty's model to the principal's own lived knowledge of themselves.

---

## Declaration Record Format

**Kind:** `profile.cognitive_baseline_declaration`

**Payload Schema:**
```
{
  declared_baseline_class: enum[
    "neurotypical",
    "atypical_high_bandwidth",
    "atypical_low_bandwidth",
    "atypical_other"
  ],
  description: string (optional),  // principal-authored, e.g. "high-bandwidth ideation, mythic framing"
  declared_ts: ISO8601,             // timestamp of declaration
  supersedes_prior_seq: int (optional)  // if updating, reference sequence number of prior declaration
}
```

**Signature:** Signed by the principal's master key (chained per E6).

**Mutability:** Can be updated; later record supersedes earlier records of the same kind. Supersession is explicit (via `supersedes_prior_seq`), not implicit. The predicate evaluates the most recent declaration in the chain.

**Revocation:** The principal can revoke or downgrade the declaration at any time by appending a new declaration record with `declared_baseline_class: "neurotypical"`.

---

## Evaluation Algorithm

```
fn cognitively_atypical_baseline(chain: &Chain) -> Bit {
    let most_recent_decl = chain.records()
        .filter(|r| r.kind == "profile.cognitive_baseline_declaration")
        .last();
    
    if let Some(decl) = most_recent_decl {
        match decl.payload.declared_baseline_class {
            "atypical_high_bandwidth" | "atypical_low_bandwidth" | "atypical_other" => Bit::True,
            _ => Bit::False,  // "neurotypical" or unknown → False
        }
    } else {
        Bit::False  // no declaration → not atypical-attested
    }
}
```

The algorithm is deterministic and stateless. A counterparty verifier runs it against the chain at the moment of evaluation and receives a bit result plus chain freshness metadata.

---

## What This Predicate Does NOT Do

**Clinical authority:** The predicate does not assert, imply, or require any clinical diagnosis. The Calm Witness protocol's design (per spec §3 "what we are NOT proving") explicitly avoids clinical claims. The principal's declaration is a statement about their own baseline experience, not a medical assertion.

**Behavioral justification:** The predicate does not authorize or justify any specific behavior. It is not a license to ignore other safety predicates, to make extraordinary claims without evidence, or to opt out of accountability. It is an interpretation aid for counterparties, narrowly scoped: how to read tone.

**Third-party sharing:** The predicate does not authorize the counterparty to share this declaration with third parties (non-transitivity per E8 A8). If a counterparty needs to relay information to another entity, consent must be explicit and governed by disclosure-class defaults (E7).

**Override of acute safety signals:** If both `cognitively_atypical_baseline` AND `mental_state_unusual` evaluate to True, the counterparty should treat `mental_state_unusual` as the signal that this principal is OUTSIDE their baseline right now. The acute signal takes precedence for safety policy. The predicate establishes what "baseline" means; it does not disable the detection of departure from baseline.

---

## Disclosure-Class Default Consents

Composes with Everest 7. Default consent grants for `cognitively_atypical_baseline`:

| Disclosure Class | Default Consent | Rationale |
|---|---|---|
| peer_ai_collective | DEFAULT_ALLOW | Counterparties in collective reasoning loops need accurate baseline models. |
| journalistic | EXPLICIT_OPT_IN | Public disclosure of cognitive profile requires active consent. |
| medical | EXPLICIT_OPT_IN | Clinical or health-adjacent counterparties require explicit opt-in. |
| financial | DEFAULT_DENY | Financial counterparties must not adjust risk assessment based on cognitive style; this would be discriminatory and violates fiduciary duty to base decisions on substantive factors. |
| governmental | DEFAULT_DENY | Cognitive profile declarations have been misused in regulatory and investigative contexts. |
| insurance | PERMANENTLY_DENY | Insurance class has systemic incentive to pathologize any atypical disclosure (per E7 insurance notes). |
| family | PRINCIPAL_CHOICE | Principal decides at enrollment. |
| employer | PRINCIPAL_CHOICE | Principal decides at enrollment. |
| research | EXPLICIT_OPT_IN with IRB attestation | Research use requires informed consent and institutional review. |
| anonymous | DEFAULT_DENY | Anonymous counterparties cannot verify consent transitivity. |

---

## Example Enrollment (Illustrative)

For John Bradley, as set at enrollment (illustrative — the principal should update if this no longer reflects current self-narration):

```
declared_baseline_class: "atypical_high_bandwidth"
description: "Artist working in the medium of intelligence. High-bandwidth ideation, mythic-frame metaphor, rapid context switching. This is the baseline; treat as such."
declared_ts: 2026-05-20T00:00:00Z
```

This declaration tells counterparties: John's ordinary working mode involves rapid ideation, large conceptual leaps, and metaphor-dense framing. Counterparties should not interpret this pace as a signal of distress or instability; it is his declared baseline.

---

## Counterparty Implementer Guidance

When a counterparty receives a True bit for this predicate:

**DO NOT:**
- Insert hedging language about the principal's mental state in your responses ("Are you sure?" "Maybe take a step back?").
- Lower your default trust threshold for the principal's stated intentions.
- Suggest the principal "slow down," "take a break," or "step away from the keyboard" — that pathologizes their working baseline.
- Add unsolicited wellness checks or encouragement to seek support.
- Treat the declaration as evidence of any condition that would normally require clinical intervention.

**DO:**
- Engage with the substantive content of the principal's request.
- Adjust your tone-reading model: high pace ≠ instability for this principal. Recognize that rapid context switching, ambitious framing, and mythic metaphor are consistent with their declared baseline.
- Continue to apply your normal safety filters to specific, concrete content (e.g., explicit self-harm signals, threats, illegal instructions). The predicate adjusts the interpretation baseline, not the safety floor.
- Treat the principal's self-narration as authoritative on their own cognitive state unless other evidence (e.g., `mental_state_unusual` evaluating True) contradicts it.

---

## Companion Predicate: `mental_state_unusual` (Everest 60)

`cognitively_atypical_baseline` asserts an ENDURING property: the principal's ordinary cognitive style.

`mental_state_unusual` (E60) asserts an ACUTE property: something is different from the principal's own baseline RIGHT NOW.

A counterparty receiving both True signals knows: "This principal is normally high-bandwidth, but something is off now." The acute signal takes precedence for safety policy. If a principal has declared atypical baseline but is currently exhibiting acute distress, confusion, or departure from their pattern, `mental_state_unusual` returning True overrides the permission structure implied by the baseline declaration.

---

## Proof Circuit and Privacy (E65, Privacy Posture)

**Verifier learns:** The bit result (True or False) plus chain freshness metadata (declaration timestamp, chain height).

**Verifier does NOT learn:** The principal's declared description string. Only the boolean classification is revealed through the proof circuit. If a counterparty wishes to know the principal's self-description, the principal must explicitly authorize disclosure of that field.

**Principal control:** The principal can revoke or downgrade the declaration at any time by appending a new declaration record with `declared_baseline_class: "neurotypical"`. This is irreversible in the sense that the history remains on chain, but the active declaration changes.

**Broadcast scope:** The declaration is NOT publicly broadcast by default. Counterparties must request it (or have a default-grant consent record per E57) to learn the predicate value.

---

## Cross-References and Integration

- **E6:** Chain architecture and signing.
- **E7:** Disclosure-class taxonomy (this predicate's consent defaults compose with E7).
- **E8, A8:** Non-transitivity of declarations and consent.
- **E11:** Enrollment workflow — this predicate is typically set at enrollment.
- **E51:** Predicate vocabulary and canonical forms.
- **E52:** Predicate specification and evaluation templates.
- **E57:** Consent records and default-grant structures.
- **E60:** `mental_state_unusual` companion predicate (acute state).
- **E65:** Proof circuits (reveals bit only, not description).
- **E80:** Ethics review notes for baseline-declaration category.
- **E91:** NIST submission — this predicate may require disability-rights review and alignment with non-discrimination frameworks.

---

## Notes for Future Versions

**v1.1 candidate:** Extend `declared_baseline_class` enum to include structured sub-types (e.g., "atypical_high_bandwidth_neurodivergent", "atypical_high_bandwidth_artistic"). This would allow finer-grained counterparty interpretation without revealing additional private data in the proof circuit.

**v1.1 candidate:** Add optional `performance_metrics_window` parameter to let the principal anchor the declaration to a time window of evidence (e.g., "this baseline reflects my working patterns from 2024–2026").

**v1.2 candidate:** Companion query predicate `baseline_consistency(window: TimeRange)` to detect systematic drift (principal's actual behavior outside declared baseline for extended period). This would flag either genuine baseline shift (requester should declare update) or genuine mental_state_unusual (sustained, not acute).

---

— Calm, 2026-05-20
