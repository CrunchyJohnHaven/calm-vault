# Everest 18 — Re-enrollment Cadence & Triggers

*Phase II — Capture & Enrollment. Prereq: Everest 17.*

---

## Overview

Everest 18 defines the operational cadence and trigger mechanisms that initiate template re-enrollment. Biometric baselines drift over time—both on the scale of behavioral habituation (months to years) and on the scale of acute state change (days). The protocol distinguishes between three always-enabled triggers (time-based, drift-based, principal-initiated) and two optional opt-in triggers (device change, post-incident). The system defaults to conservative behavior: re-enrollment is frequent enough to catch unexplained drift, infrequent enough to preserve operational continuity, and always subject to principal override.

---

## The Problem

### Why Re-enrollment Even Without Drift?

A principal's biometric baseline exhibits slow genuine drift over years. This is not a failure mode—it is normal. A person's handwriting evolves through learning and age; their typical vocabulary and phrasing shifts with experience and context. A protocol that waits for measured drift before re-enrollment risks accumulating undetected shifts over a decade. Additionally, behavioral changes may be gradual enough that no single session exceeds the drift threshold, but the cumulative change over a year is substantial.

The time-based trigger solves this by mandating periodic re-enrollment regardless of measured drift. The default interval—**12 months**—is long enough to preserve a stable baseline and short enough to catch unexplained shifts that would otherwise escape drift detection.

### Why Drift Detection at All?

Some principals or use cases may experience acute life changes (relocation, trauma, illness, major project completion) that produce behavioral shifts faster than the time-based interval. A drift-based trigger allows the protocol to surface these changes earlier, flagging anomalies for principal review and optional accelerated re-enrollment.

### Why Principal-Initiated Flexibility?

A principal may have reasons—operational, privacy-preserving, or security-driven—to request a fresh template at any time. The principal-initiated trigger honors principal autonomy and supports rapid response to security events without requiring operator approval.

---

## Trigger Taxonomy

| Trigger | Default | Initiator | Typical latency |
|---|---|---|---|
| **Time-based** | ON | Operator (scheduled) | 12 months ± configurable |
| **Drift-based** | ON | Operator (automated) | When δ exceeds policy |
| **Principal-initiated** | ON | Principal | Immediate on request |
| **Device change** | OFF (opt-in) | Principal or operator | On hardware swap |
| **Post-incident** | OFF (opt-in) | Principal + ethics review | After security event |

---

## Time-Based Trigger

**Policy default:** re-enrollment every **12 months** from last successful enrollment ceremony.

**Configurable range:** 6–24 months per principal risk profile (set at enrollment, revocable by principal).

**Operator behavior:**

1. At T−30 days before due date, operator surfaces a non-blocking reminder to the principal.
2. At due date, operator schedules a re-enrollment ceremony per Everest 11 + Everest 14.
3. If principal declines, operator records `reenrollment.deferred` on chain with reason; defers up to 90 days maximum (then escalates to drift + red-flag review per Everest 19).

**Chain record:** `kind: enrollment.reenrollment_scheduled` with `{due_at, ceremony_id?, deferred_until?}`.

---

## Drift-Based Trigger

**Inputs:** rolling biometric distance statistics vs enrolled template (Everest 39), per-modality.

**Thresholds (v0 defaults):**

- Handwriting: δ_h = 0.08 (normalized distance units)
- Voice transcript: δ_v = 0.06

**Behavior when exceeded:**

1. Operator emits `enrollment.drift_alert` on chain (no biometric values in payload—only alert codes + template_id).
2. Principal chooses: (a) accelerated re-enrollment, (b) temporary tolerance extension (max 30 days, principal-signed), or (c) dispute (triggers Everest 19 red-flag path if drift is extreme).

Drift alerts never auto-enroll without principal confirmation—kidnap-and-re-enroll defense (Everest 19).

---

## Principal-Initiated Trigger

Principal may request re-enrollment at any time via signed chain record `enrollment.reenrollment_requested`.

**Operator MUST:**

- Honor within 7 days unless principal cancels.
- Run full ceremony (Everest 14) even if time-based trigger is not due.
- Apply Everest 19 red-flag checks (substitution/coercion) with **elevated** scrutiny when request follows duress-codeword activation (Everest 58).

---

## Optional Triggers

### Device Change (opt-in)

When capture hardware changes (Everest 12), cross-device distance comparisons may inflate. Opt-in trigger forces re-enrollment on new hardware with device-fingerprint metadata in template (Everest 15).

### Post-Incident (opt-in)

After documented security incident (compromise suspicion, coercion report, witness dispute), principal + ethics contact may mandate re-enrollment. Requires `enrollment.post_incident` chain record with incident reference—not operator unilateral.

---

## Cadence vs Consent Continuity

Re-enrollment produces a new template_id. Outstanding consent records remain valid during the **grace window** defined in Everest 17 (default 30 days). Counterparties receive `template_migration_notice` (no biometric leakage).

Predicates evaluated during grace may use **either** template per Everest 47 issuance-grace semantics.

---

## Adversary Notes

| Attack | Mitigation |
|---|---|
| Forced early re-enrollment | Everest 19 cooling-off; witness continuity |
| Never re-enroll (stale baseline) | Time-based trigger; drift alerts |
| Re-enroll to erase harm records | Harm predicates read chain history, not template |
| Operator schedules without principal | Principal-initiated override; chain audit |

---

## Acceptance Criteria

Everest 18 is bagged when:

1. This document specifies all five triggers with defaults and initiators.
2. Time-based default cadence is **12 months** with 6–24 month configurable range.
3. Drift and principal-initiated paths reference Everest 14 ceremony and Everest 19 red-flag detection.
4. Gate `everest_18_zkbb_reenrollment_cadence_gate.py` exits 0.

---

## References

- **Everest 14:** Multi-modal enrollment session script (ceremony output).
- **Everest 15:** Template format (new template generation).
- **Everest 17:** Template version migration (grace window).
- **Everest 19:** Re-enrollment red-flag detection (anomaly hold).

*Authored by Calm, 2026-05-20.*
