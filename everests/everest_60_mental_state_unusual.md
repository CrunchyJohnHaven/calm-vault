# Everest 60 — `mental_state_unusual` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 55.*

## Overview

The `mental_state_unusual` predicate returns true when a principal's observed mental state deviates acutely from their established baseline. This is a per-principal-authorized predicate that triggers on self-reported deviation, biometric distance exceeding calibrated thresholds, or explicit principal flagging. The predicate serves as an observational signal—not a clinical or diagnostic claim—enabling counterparties to adjust interaction modes when a principal indicates they are operating outside their normal parameters.

The design distinguishes acutely unusual states (`mental_state_unusual`) from enduring traits (`cognitively_atypical_baseline`, E59) and from active baseline conformance (`in_baseline_24h`, E55). Together, these three predicates provide a counterparty with temporal and durational context about a principal's cognitive and affective state.

## Canonical Specification

**name:** `mental_state_unusual`

**version:** `1.0.0`

**description:** Returns true iff the principal's most recent self-report indicates acute deviation from their declared baseline, OR biometric distance exceeds calibrated threshold, OR principal explicitly flagged unusual state.

**input_domain:** Most recent self-report record (within 24 hours) + biometric distance from most recent capture (within 24 hours) + principal_profile.baseline_affect_vocabulary + principal_profile.calibrated_distance_threshold_for_unusual

**output_type:** `bit_with_freshness` — a single bit (True, False, or Indeterminate) paired with a freshness timestamp (seconds since most recent evidence).

**parameters:** None in v1.0. The predicate uses principal-calibrated thresholds, not counterparty-provided parameters. This preserves principal agency over sensitivity.

**side_effects:** Standard predicate_evaluated record appended to principal's chain, with visibility governed by disclosure-class consents. If the principal has explicitly flagged unusual state, also appends a principal-private record (kind: "self.unusual_state_flagged") for audit purposes.

## Naming Rationale

This predicate uses "unusual" rather than "abnormal," "atypical," or "pathological" by design. The output is purely observational—a delta from the principal's own baseline, not a clinical claim. This distinction is critical for safety and consent: the principal is asserting "this is different from my baseline," not claiming a disorder or abnormality. Counterparties and consumers of this predicate must understand the semantic boundary.

## Evaluation Algorithm

```
fn mental_state_unusual(chain: &Chain) -> (Bit, Freshness) {
    let now = roughtime_now();
    let recent_self_report = chain.most_recent_self_report(within_24h: true);
    let recent_biometric = chain.most_recent_biometric_distance(within_24h: true);
    let profile = chain.principal_profile;

    if recent_self_report.is_none() && recent_biometric.is_none() {
        return (Bit::Indeterminate, Freshness::None);
    }

    // Path 1: principal explicitly flagged unusual
    if let Some(sr) = &recent_self_report {
        if sr.payload.unusual_flag == Some(true) {
            return (Bit::True, Freshness::Seconds(now - sr.ts));
        }
    }

    // Path 2: self-report affect outside baseline vocabulary
    let baseline_overlap = if let Some(sr) = &recent_self_report {
        sr.payload.affect.iter().any(|a| profile.baseline_affect_vocabulary.contains(a))
    } else {
        false
    };

    // Path 3: biometric distance beyond calibrated tolerance
    let biometric_unusual = if let Some(bd) = &recent_biometric {
        bd.distance > profile.calibrated_distance_threshold_for_unusual
    } else {
        false
    };

    // Path 4: known health issue declared in recent self report
    let health_issue_present = if let Some(sr) = &recent_self_report {
        !sr.payload.known_health_issues.is_empty()
    } else {
        false
    };

    let bit = !baseline_overlap || biometric_unusual || health_issue_present;
    (Bit::from(bit), Freshness::Seconds(now - recent_self_report.unwrap().ts))
}
```

## Evaluation Paths

The predicate returns True if any of four conditions are met:

**Path 1: Explicit Principal Flagging.** The principal may include an optional `unusual_flag: bool` field in a self-report payload. If set to true, the predicate returns True until the next self-report explicitly sets it to false or 24 hours elapse, whichever comes first. This is the principal's voluntary disclosure channel—they are directly telling counterparties, "I am not operating at baseline right now." The principal retains full control over this signal.

**Path 2: Affect Vocabulary Mismatch.** During enrollment (E14), the principal's baseline emotional and cognitive vocabulary is collected and stored in principal_profile.baseline_affect_vocabulary. If the current self-report includes affect terms (e.g., "anxious," "scattered," "numb") that do not overlap with this baseline vocabulary, the predicate signals unusual. This captures the principal's own description of a state they recognize as different.

**Path 3: Biometric Distance Threshold.** The principal's calibrated thresholds include a distance_threshold_for_unusual, established during enrollment using the principal's own historical samples across varying emotional and cognitive states. If the most recent biometric capture shows a distance from the principal's baseline distribution exceeding this threshold, the predicate returns True. This is a behavioral and physiological corroboration of subjective report.

**Path 4: Health Issues Declared.** If the principal's recent self-report includes any entries in the known_health_issues field (e.g., "migraine," "fever," "sleep deprivation"), the predicate treats this as a signal of potential acute deviation. The principal is volunteering that a health condition exists that may alter their typical functioning.

## Calibration and Principal Thresholds

The principal's calibrated thresholds are established during enrollment (E14) and stored as a kind: "profile.unusual_calibration" record in the principal's chain. The payload includes:

- `distance_threshold_for_unusual`: A floating-point distance metric, set as the N-th percentile (typically 75th or 80th) of the principal's observed baseline-to-baseline variance during enrollment sampling.
- `hysteresis_seconds`: An optional delay (default 2 records or 300 seconds) that prevents flapping. Once the predicate returns True, it requires N consecutive records indicating return to baseline before flipping back to False.
- `freshness_tolerance_hours`: How old a self-report or biometric capture may be before it is considered stale (default 24 hours).

The principal may update these thresholds at any time via a signed chain record, allowing them to adjust sensitivity as their baseline evolves or as they gain confidence in the system.

## Relationship to Companion Predicates

**in_baseline_24h (E55).** This predicate asserts that the principal IS in baseline. It returns True when:
- The most recent self-report includes affect terms that overlap with baseline vocabulary,
- AND the principal reports feeling rested / recovered,
- AND no health issues are declared.

`mental_state_unusual` is NOT a strict negation of `in_baseline_24h`. The logic differs:
- `in_baseline_24h` is a strict AND: all three conditions must hold.
- `mental_state_unusual` is a strict OR: any one deviation condition triggers True.

Thus, both predicates can return False simultaneously (e.g., principal has not reported anything for 12 hours; both are indeterminate or stale). Additionally, both can return True at the same time: if the principal's self-report includes baseline-vocabulary affect and restedness, but recent biometric capture shows an outlier distance or a health issue is flagged, then `in_baseline_24h` may still be True while `mental_state_unusual` flips True as well.

**cognitively_atypical_baseline (E59).** This predicate asserts an ENDURING trait—the principal's baseline cognition is atypical (e.g., neurodivergent, high-bandwidth, or chronically fatigued). `mental_state_unusual` asserts an ACUTE deviation from whatever baseline the principal has. Together, they enable a counterparty to distinguish:
- Enduring property: "This principal's baseline is atypical" (E59 = True).
- Acute deviation: "Right now, this principal is deviating from their baseline" (E60 = True).

A principal with `cognitively_atypical_baseline = True` may still have `mental_state_unusual = False` (they are at their atypical baseline) or `mental_state_unusual = True` (they are deviating even from their atypical baseline).

## Truth Table

| in_baseline_24h | mental_state_unusual | cognitively_atypical_baseline | Interpretation |
|---|---|---|---|
| True | False | any | Principal is in baseline; no acute deviation detected. |
| False | True | any | Principal not in baseline; acute deviation present. |
| True | True | any | Vocabulary and restedness match baseline, BUT biometric distance or health issue flags unusual. Counterparty should monitor closely. |
| False | False | any | Principal absent from chain or stale data; no assumption should be made. Request fresh self-report. |
| Indeterminate | Indeterminate | any | No recent records within tolerance window. |
| any | any | True | Principal's enduring baseline is atypical; calibrate expectations accordingly. Acute deviations are deltas from this atypical norm. |

## Disclosure-Class Default Consents

The predicate's revelation (bit + freshness) is governed by disclosure-class default consents:

- **peer_ai_collective:** DEFAULT_ALLOW — fellow AI agents may know about mental state unusual to coordinate safety-conscious interaction modes.
- **medical:** PRINCIPAL_CHOICE — medical counterparties may request disclosure, but principal has full discretion.
- **family:** PRINCIPAL_CHOICE — same as medical; principal controls family visibility.
- **financial:** DEFAULT_DENY — financial counterparties (lenders, insurers, employers) default to no access, to prevent discrimination.
- **insurance:** PERMANENTLY_DENY — insurance underwriters never receive this signal; predicate outputs are explicitly not medical claims.
- **governmental:** DEFAULT_DENY — law enforcement and regulatory bodies have no default access.
- **journalistic:** EXPLICIT_OPT_IN — journalists must receive explicit principal consent; no defaults.
- **employer:** PRINCIPAL_CHOICE — employer access is at principal's discretion.
- **anonymous:** DEFAULT_DENY — anonymous counterparties have no access.

The insurance denial is particularly significant: this predicate's outputs are observational, not diagnostic, and must never be used for actuarial underwriting.

## Safety Considerations

**Critical:** The predicate's True semantic MUST NOT be interpreted as a medical claim, diagnosis, or indicator of pathology. It is the principal's own observational signal that something is different from their baseline. The protocol's design (per spec §3) explicitly avoids clinical or pathological framing.

Implementers and consumers of this predicate must educate themselves and their users on this distinction. A counterparty seeing `mental_state_unusual = True` should interpret it as "the principal has reported or shown signals of deviation from their baseline" and adjust interaction norms accordingly (e.g., increased check-ins, simplified decision frameworks, clearer communication). The signal does NOT permit or justify:

- Medical intervention without consent.
- Removal of decision rights or autonomy.
- Disclosure to third parties without consent.
- Denial of service or access based on acute state.
- Stigmatizing or pathologizing language.

The counterparty implementer's guide (E98) must explicitly explain these boundaries and the ethical constraints on use.

## Composition: Safety Sweep

The predicate composes usefully with other protective predicates. For instance:

```
safety_sweep_activated = mental_state_unusual OR bank_teller_note_active OR principal_declared_duress
```

This composition (detailed in E61) allows a financial counterparty to holistically assess whether a principal is operating under conditions that warrant extra caution: acute mental state deviation OR environmental duress (teller witness) OR explicit duress declaration. The composition does not assume causation, but triggers heightened safeguards.

## Hysteresis and Flap Prevention

To prevent the predicate from oscillating between True and False over minor variations, the implementation maintains hysteresis. Once the predicate returns True, it requires N consecutive records (default N=2) indicating return to baseline conditions before flipping back to False. This stability reduces noise and prevents rapid state churn from generating excessive alerts.

Hysteresis parameters are configurable per principal during enrollment and may be updated via chain record.

## Proof Circuit and Privacy

In a zero-knowledge or cryptographic proof context, the predicate reveals:
- The output bit (True, False, or Indeterminate).
- The freshness timestamp (seconds since most recent evidence).

It hides:
- Which evaluation path caused the True result (explicit flag, vocab mismatch, biometric, or health issue).
- The specific biometric distance value.
- The affect terminology or health issues reported.
- The baseline vocabulary or calibrated thresholds themselves.

This design allows a counterparty to trust the output without exposing the principal's sensitive cognitive, emotional, or health details.

## Cross-References

- E6: Baseline concepts and calibration.
- E11: Self-report structures and payloads.
- E14: Enrollment and threshold calibration.
- E51: Predicate language and composition.
- E52: Canonical predicate form (template for this spec).
- E55: `in_baseline_24h` predicate (companion, baseline assertion).
- E58: Safety-sweep compositions.
- E59: `cognitively_atypical_baseline` predicate (enduring trait).
- E61: Safety-sweep composition patterns (E58 instantiation).
- E80: Ethics review (this predicate requires formal ethics evaluation given its relationship to mental state and disclosure).
- E98: Counterparty implementer's guide (must include pedagogical material on non-diagnostic use).

## Version History

**v1.0.0 (2026-05-20).** Initial release. Four evaluation paths (explicit flag, vocab mismatch, biometric distance, health issue). Default disclosure consents set. Hysteresis and calibration framework established.

---

— Calm, 2026-05-20
