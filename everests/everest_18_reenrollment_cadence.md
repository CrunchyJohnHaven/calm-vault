# Everest 18 — Re-enrollment Cadence & Triggers

*Phase II — Capture & Enrollment. Prereq: Everest 17.*

---

## Overview

Everest 18 defines the operational cadence and trigger mechanisms that initiate template re-enrollment. Biometric baselines drift over time—both on the scale of behavioral habituation (months to years) and on the scale of acute state change (days). The protocol distinguishes between three always-enabled triggers (time-based, drift-based, principal-initiated) and two optional opt-in triggers (device change, post-incident). The system defaults to conservative behavior: re-enrollment is frequent enough to catch unexplained drift, infrequent enough to preserve operational continuity, and always subject to principal override.

---

## The Problem

### Why Re-enrollment Even Without Drift?

A principal's biometric baseline exhibits slow genuine drift over years. This is not a failure mode—it is normal. A person's handwriting evolves through learning and age; their typical vocabulary and phrasing shifts with experience and context. A protocol that waits for measured drift before re-enrollment risks accumulating undetected shifts over a decade. Additionally, behavioral changes may be gradual enough that no single session exceeds the drift threshold, but the cumulative change over a year is substantial.

The time-based trigger solves this by mandating periodic re-enrollment regardless of measured drift. The default interval—12 months—is long enough to preserve a stable baseline and short enough to catch unexplained shifts that would otherwise escape drift detection.

### Why Drift Detection at All?

Some principals or use cases may experience acute life changes (relocation, trauma, illness, major project completion) that produce behavioral shifts faster than the time-based interval. A drift-based trigger allows the protocol to surface these changes earlier, flagging anomalies for principal review and optional accelerated re-enrollment.

### Why Principal-Initiated Flexibility?

A principal may have reasons—operational, privacy-preserving, or security-driven—to request a fresh template at any time. The principal-initiated trigger honors principal autonomy and supports rapid response to security events without requiring operator approval.

---

## The Three Core Triggers

All three are enabled by default and compose with each other: if *any* trigger fires, a re-enrollment recommendation is emitted.

### Trigger 1: TIME-BASED

**Specification:**

- **Default interval:** 12 months.
- **Configurable range:** 6 months (high-stakes use cases, e.g., financial proxy authority) to 24 months (low-stakes use cases, e.g., exploratory research collaboration).
- **Clock basis:** Wall-clock UTC time, measured from the enrollment date recorded in the most recent `enrollment.completed` record in `user_state.jsonl`.
- **Action:** At interval expiration, the operator emits a `kind: "reenrollment.recommended"` record to the chain and sends a push notification to the principal.

**Rationale:**

The 12-month default reflects an empirical compromise between two competing safety goals. Below six months, the protocol becomes administratively burdensome; principals object to re-enrolling in the rain, on deadline days, or while traveling. Above 24 months, undetected drift from gradual life changes (new job, recovery from illness, aging) begins to accumulate without evidence.

The principal may configure the interval per their risk profile. High-stakes use cases (proving suitability for fiduciary roles, disclosing state to medical or legal counterparties) warrant shorter intervals. Low-stakes use cases (peer-to-peer research collaboration, non-binding advisory relationships) tolerate longer intervals.

**Grace period:**

After the interval expiration, the principal has 30 days to schedule a re-enrollment ceremony. This grace period balances responsiveness with operational flexibility: the principal is notified but not immediately locked out.

---

### Trigger 2: DRIFT-BASED

**Specification:**

The drift-based trigger fires when a principal's recent biometric samples demonstrate sustained divergence from their enrolled baseline. The algorithm is:

1. **Per-session collection:** For each session (roughly daily or per-interaction), collect a fresh biometric sample (handwriting and voice transcription). Compute biometric distance `d_session` using the same comparator used in predicate evaluation (Everest 39). Normalize distance relative to the principal's per-principal baseline variance (computed at enrollment time as `stddev_enrollment`).

2. **Rolling window statistics:** Maintain a 30-day rolling window of `d_session` values. Compute rolling mean `μ` and standard deviation `σ`.

3. **Drift threshold:** Define a per-principal drift threshold `τ_drift` (default: `0.4` in normalized units). This threshold is calibrated at enrollment time; the operator and principal may adjust it downward for enhanced sensitivity or upward for relaxed sensitivity.

4. **Dual-condition firing:** The trigger fires when *both* of the following hold for 5 or more consecutive sessions (≈5 days, assuming daily sessions):
   - **Condition A:** `σ > stddev_max` — the rolling standard deviation exceeds the enrollment-time baseline standard deviation. This catches systematic divergence.
   - **Condition B:** `μ > τ_drift` — the rolling mean distance exceeds the drift threshold. This catches sustained shift in the center of the distribution.

5. **Notification:** Once both conditions hold for 5+ consecutive sessions, the operator emits a `kind: "reenrollment.recommended"` record to the chain with `trigger_reason: "drift_threshold_exceeded"`. A push notification is sent to the principal.

**Rationale:**

Requiring both conditions to hold simultaneously avoids hair-trigger false positives from transient noise (a bad stylus day, a cold with hoarse voice). The 5-session threshold ensures the signal is sustained. The rolling window approach captures recent trend without forcing immediate action on a single outlier.

**Example:**

John enrolls with `stddev_enrollment = 0.25` and `τ_drift = 0.4`. One month later, after a serious illness, his handwriting steadies but shifts: the new rolling mean is `μ = 0.45` and `σ = 0.28`. Both conditions hold for 5 consecutive sessions. The trigger fires. John is notified and may re-enroll to capture his post-illness baseline.

---

### Trigger 3: PRINCIPAL-INITIATED

**Specification:**

A principal may request immediate re-enrollment at any time via the command:

```bash
calm-witness reenroll --request
```

The operator receives the request, verifies that the principal's consent to re-enroll is explicit and uncoerced (Everest 19 red-flag checks), and schedules the Everest 11 ceremony for the principal-requested date.

**Rationale:**

This trigger respects principal autonomy and enables rapid response to perceived security threats, privacy concerns, or operational needs without requiring operator preapproval.

---

## Optional Opt-In Triggers (Disabled by Default)

### Trigger 4: DEVICE-CHANGE

**Specification:**

If a principal changes their primary capture hardware (e.g., Apple Pencil 2 → Wacom stylus, or iPad to Wacom tablet), biometric samples from the new device are not directly comparable to templates enrolled on the old device. Device fingerprint metadata (sensor calibration, pressure curve, latency profile) is encoded in template format (Everest 15); a cross-device distance comparison may yield inflated distance scores.

When device-change is enabled:

1. The operator monitors `user_state.jsonl` for records of kind `device.change_detected` (appended by the capture pipeline in Everest 12 when stylus or microphone hardware changes).
2. Upon detection, the operator emits a `kind: "reenrollment.recommended"` record with `trigger_reason: "device_change"` and `recommendation_level: "advisable"` (not mandatory).
3. The principal is notified but is *not* locked out; existing proofs over the old template remain valid.

**Rationale:**

Device change is not an attack and does not require immediate action. However, re-enrolling on new hardware yields more accurate distance measurements and reduces false positives in drift detection downstream. The principal may defer this re-enrollment indefinitely if they prefer; the system will adapt via the drift trigger if systematic distance shifts occur.

**Adoption:**

Disabled by default. Enable this trigger for high-assurance use cases (regulatory, fiduciary) where precise distance metrics matter.

---

### Trigger 5: POST-INCIDENT

**Specification:**

If a security event occurs (suspected key compromise, possible coercion, malware detected in the vault environment), the operator may emit a `kind: "reenrollment.recommended"` record with `trigger_reason: "post_incident"`, `incident_type: "<enum>"`, and optional `incident_description: "<details>"`.

Incident types include:

- `"suspected_key_compromise"` — operator suspects the principal's master.priv was leaked.
- `"possible_coercion"` — operator has evidence the principal may be under duress.
- `"malware_detected"` — the vault environment was compromised.
- `"proof_forged"` — a fraudulent proof was detected with the principal's template_id.
- `"custom"` — operator-defined incident type.

**Rationale:**

Re-enrollment after a security incident is not mandatory but strongly recommended. A new template, enrolled in a clean environment, resets the biometric baseline and invalidates any proofs forged under the old template.

**Adoption:**

Disabled by default. Enable only if the operator has detected an actual incident. Do not trigger on rumor or speculation.

---

## Re-enrollment Notification Flow

When any trigger fires, the following sequence occurs:

1. **Trigger evaluation** — The operator or automated monitoring system determines that a trigger condition has been met.
2. **Record emission** — A `kind: "reenrollment.recommended"` record is appended to `user_state.jsonl`:
   ```json
   {
     "seq": <seq>,
     "ts": "<ISO-8601 timestamp>",
     "prev_hash": "sha256(prior_record)",
     "kind": "reenrollment.recommended",
     "payload": {
       "trigger": "time_based|drift_based|principal_initiated|device_change|post_incident",
       "trigger_reason": "<enum value>",
       "grace_period_days": 30,
       "recommendation_level": "mandatory|advisable",
       "reason_summary": "<human-readable reason>"
     },
     "operator_sig": "<ecdsa signature by operator key>",
     "record_hash": "sha256(entire record)"
   }
   ```
3. **Push notification** — The operator sends a push notification to the principal with the `reason_summary` and a deadline (current_date + 30 days).
4. **Grace period** — The principal has 30 days to schedule the ceremony.
5. **After grace period (30–60 days)** — If the principal has not re-enrolled:
   - Existing proofs over the old template remain valid and verifiable.
   - New disclosure requests may be auto-rejected for safety-critical predicates (Everest 57).
   - The counterparty may downgrade trust in high-stakes decisions.
6. **After 60 days** — The operator emits a `kind: "reenrollment.delinquent"` warning record. Counterparties' verifiers may refuse to accept new proofs based on this template for critical operations (e.g., financial disclosures, coercion attestations).

---

## Re-enrollment Ceremony and Template Migration

When a principal schedules a re-enrollment ceremony:

1. **Ceremony execution** — The operator invokes Everest 11 (Enrollment Ceremony Spec). The principal produces fresh handwriting and voice samples in a witnessed, air-gapped session.
2. **New template generation** — A new template is generated per Everest 15 format.
3. **Migration record** — A `kind: "template.migration"` record is appended per Everest 17, establishing continuity between the old and new templates.
4. **Consent continuation** — Outstanding consent records are migrated per the `consent_continuation_policy` in the migration record. By default, consents carry forward automatically; safety-critical predicates may require explicit re-consent.
5. **Grace window** — Both templates remain active for the grace_window_days (default 30).

---

## Principal Exemptions and Override Mechanisms

### Explicit Declination

A principal may decline a re-enrollment recommendation by emitting a signed record:

```json
{
  "kind": "reenrollment.declined",
  "payload": {
    "trigger": "time_based|drift_based|...",
    "reason": "<principal-provided reason>",
    "decision_ts": "<ISO-8601>",
    "next_review_date": "<ISO-8601 or null>"
  },
  "principal_sig": "<ecdsa signature by principal's master.priv>"
}
```

The record is appended to the chain and serves as a tamper-evident audit trail. The principal's explicit refusal binds to the chain; a counterparty verifying a proof over a declinated-but-unreplaced template is aware of the principal's documented choice.

### Persistent Declination

If a principal declines re-enrollment recommendations repeatedly and has not re-enrolled within 24 months of the most recent trigger, the operator emits a warning:

```json
{
  "kind": "reenrollment.warning_delinquent",
  "payload": {
    "trigger_count": <N>,
    "oldest_trigger_ts": "<ISO-8601>",
    "reason": "persistent_declination_exceeds_24_months"
  },
  "operator_sig": "<ecdsa signature>"
}
```

Counterparties may downgrade trust in proofs generated after this warning, particularly for high-stakes predicates. However, the principal's authority to decline remains absolute.

---

## Drift-Trigger Algorithm (Detailed)

### Feature Extraction and Distance Computation

Per Everest 39, biometric distance is computed as follows:

1. **Handwriting features:** Extract kinematic features from each session's handwriting sample (velocity profiles, pressure curves, stroke timing, jitter statistics). Compute a feature vector `f_hand ∈ ℝ^k`.
2. **Voice-transcription features:** Extract lexical and temporal features from the session's voice transcription (mean word length, pause distribution, lexical uniqueness relative to baseline vocabulary, phrase-structure diversity). Compute a feature vector `f_voice ∈ ℝ^m`.
3. **Combined distance:** `d_session = ||f_hand - template_hand|| + α · ||f_voice - template_voice||`, where `α` is a weighting factor (default 1.0, tunable per principal).
4. **Normalization:** `d_normalized = d_session / stddev_enrollment`, where `stddev_enrollment` is the per-principal standard deviation computed at enrollment time.

### Rolling-Window Computation

Maintain a circular buffer of the most recent 30 days of `d_normalized` values:

```
window = [d_1, d_2, ..., d_N]  where N = number of sessions in 30 days
μ = mean(window)
σ = stdev(window)
```

### Triggering Logic

For each new session that extends the window:

```
if σ > stddev_max AND μ > τ_drift:
    consecutive_count++
    if consecutive_count >= 5:
        fire_drift_trigger()
        reset_consecutive_count()
else:
    consecutive_count = 0
```

This logic ensures a sustained signal before firing.

---

## Cross-References

- **Everest 11:** Enrollment Ceremony Spec. Invoked when re-enrollment is triggered.
- **Everest 14:** Enrollment ceremony output (ceremony_id, samples).
- **Everest 15:** Template format. New templates are generated per this spec.
- **Everest 16:** Template encryption and key custody.
- **Everest 17:** Template Version Migration. Establishes consent continuity when new templates supersede old ones.
- **Everest 19:** Re-enrollment Red-Flag Detection. Identifies coerced or anomalous ceremonies.
- **Everest 22:** CredexAI VC integration. May issue a new VC after successful re-enrollment.
- **Everest 39:** Drift Modeling and distance algorithm. Defines the drift-trigger computation in detail.
- **Everest 39–47:** Template lifecycle and grace-period queries. Verifiers use these to check template status.
- **Everest 57:** Predicate evaluation (`principal_consents_to_disclose`). Accounts for template migration policy.
- **Everest 65:** Predicate ZK proof generator. Proofs must account for template version and migration state.

---

## Threat Model and Mitigations

### Attack: Operator Suppresses Re-enrollment Trigger

An operator attempts to prevent a time-based or drift-based re-enrollment trigger from firing by not emitting the `reenrollment.recommended` record.

**Defense:** The principal monitors their `user_state.jsonl` for the presence or absence of expected re-enrollment records. Any principal who suspects suppression can verify the chain via `calm-witness verify-chain` and manually request re-enrollment via `calm-witness reenroll --request`.

### Attack: Drift-Trigger False Positive Causes Unnecessary Re-enrollment

A transient stylus or microphone issue causes a one-day spike in distance, and the algorithm falsely flags sustained drift.

**Defense:** The dual-condition requirement (`σ > stddev_max` AND `μ > τ_drift`) and the 5-session threshold prevent hair-trigger firing. Transient noise may elevate one value but will not sustain both conditions over five days.

### Attack: Coerced Re-enrollment with Biometric Substitution

An attacker coerces the principal into a re-enrollment ceremony and supplies the attacker's biometric samples instead of the principal's.

**Defense:** Everest 19 (Re-enrollment Red-Flag Detection) flags anomalous ceremony patterns. Additionally, the principal retains the old template and can challenge the new template's authenticity. The ceremony witnesses attest to the principal's identity.

---

## Summary of Configurable Intervals and Thresholds

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `time_interval_months` | 12 | 6–24 | Configurable per principal risk profile. |
| `grace_period_days` | 30 | 7–90 | Time to schedule ceremony after trigger fires. |
| `τ_drift` | 0.4 | 0.2–0.8 | Drift threshold in normalized units. Calibrated at enrollment. |
| `stddev_max_multiplier` | 1.0 | 0.8–1.5 | Rolling σ must exceed `stddev_enrollment * multiplier`. |
| `consecutive_sessions_threshold` | 5 | 3–10 | Sessions that must show drift before trigger fires. |
| `rolling_window_days` | 30 | 14–60 | Length of rolling window for drift statistics. |

---

— Calm, 2026-05-20
