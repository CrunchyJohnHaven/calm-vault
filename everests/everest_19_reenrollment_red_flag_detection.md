# Everest 19 — Re-enrollment Red-Flag Detection

*Phase II — Capture & Enrollment. Prereq: Everest 18.*

---

## Overview

Everest 19 specifies an automated detection system that identifies anomalous re-enrollment ceremonies and flags them for human-in-the-loop review. The threat is kidnap-and-re-enroll: an adversary coerces or kidnaps a principal and forces them into a re-enrollment ceremony in which the adversary's biometrics are substituted for the principal's. The resulting template would be cryptographically valid but biometrically different, binding the principal's identity to the adversary's samples. Everest 19 detects such attacks by comparing the new template against baseline properties of the principal's existing templates and enrollment history, emitting risk scores that trigger escalated confirmation protocols. The system defaults to conservative behavior: flagged enrollments are NOT immediately activated; instead, they enter a cooling-off period with mandatory additional verification, allowing the principal and their emergency contacts to reject a coerced ceremony.

---

## The Problem

### Why Re-enrollment Can Be Weaponized

Re-enrollment (Everest 18) is operationally necessary—baselines drift, hardware changes, and principals themselves may request fresh templates. However, the re-enrollment ceremony (Everest 11) is also a high-value target for attackers. Unlike the initial enrollment, which has explicit adversary assumption and anti-substitution witness requirements, a re-enrollment ceremony may occur with reduced friction: the principal is known, the process is familiar, and social engineering may convince the principal to skip certain verification steps.

An attacker who successfully coerces a principal into a re-enrollment ceremony can:

1. **Physically substitute themselves** during biometric capture (providing their own handwriting and voice).
2. **Control the ceremony environment** (via kidnapping, threats to third parties, or extortion).
3. **Produce a template** that is cryptographically valid (signed by the operator, witnessed, and anchored to Sigsum) but biometrically distinct (encoding the attacker's motor and behavioral signatures, not the principal's).

The poisoned template would pass all format and cryptographic checks. Future proofs generated over this template would bind the principal's identity and consent predicates to the attacker's samples, enabling the attacker to masquerade as the principal in downstream disclosures (Everest 65, witness predicates).

### Why Baseline Comparison is Effective

The principal's biometric baseline—accumulated across multiple prior enrollments and sessions—is a strong prior. A new template should exhibit:

- **Small drift relative to the old template:** Behavioral-biometric samples from the same human show slow, predictable drift over time (Everest 39). If the new template is dramatically different from the old one, it suggests a different human provided the samples.
- **Consistency with population statistics:** The principal's baseline handwriting and voice transcription statistics (mean pressure, stroke velocity, vocabulary diversity) should remain within the population-level statistics for the principal's demographic cohort.
- **Temporal continuity in enrollment cadence:** If re-enrollment is well outside the expected cadence (Everest 18 policy) and was not initiated by the principal, it may indicate coercion or system compromise.
- **Witness consistency:** The witnesses who attested to prior enrollments should still be available and willing to attest to the new enrollment. If all witnesses have suddenly changed, the principal may have been isolated.
- **Geolocation and device continuity:** The principal typically re-enrolls from familiar locations and on familiar hardware. A ceremony from a previously unknown location or device, especially if combined with other risk factors, raises suspicion.

---

## Acceptance Criteria

Everest 19 is acceptable when the system automatically evaluates these five detection criteria on every re-enrollment ceremony, computes a composite risk score, and triggers one of two behaviors:

1. **Risk score ≤ 0.5:** Approve and activate the new template immediately. Emit an informational record to the chain.
2. **Risk score > 0.5:** Flag the enrollment as anomalous. Do NOT activate immediately. Invoke the cooling-off protocol (72-hour hold, notifications to principal and emergency contacts, ethics review board escalation). New proof generation over the flagged template is blocked pending confirmation.

---

## Detection Criteria

### Criterion 1: Distance-to-Old-Template

**Rationale:** A principal's biometric samples exhibit slow drift under normal circumstances (Everest 39). If a new template's aggregate distance to the old template is far outside the expected drift envelope, it suggests the samples come from a different human.

**Specification:**

1. **Compute drift metrics:** For the new template, measure biometric distance against each of the principal's prior templates (or, if multiple enrollments exist, against the most recent template and the 12-month-prior template if available).
   - For handwriting: compute feature distance (velocity, pressure, jitter; Everest 39 feature set) between the new sample set and the old template.
   - For voice transcription: compute lexical and temporal distance (vocabulary overlap, phrase-structure similarity, mean word length).
   - Use the same distance function as predicate evaluation (Everest 56).

2. **Compare against drift envelope:** The drift envelope is defined by Everest 39 analysis: for a given principal, the expected drift over a re-enrollment interval (e.g., 12 months) is approximately 1× to 2× the within-session standard deviation.
   - Let `drift_expected = 2 * stddev_baseline` (tunable, conservative default).
   - Let `drift_observed = distance(new_template, old_template)` (normalized).

3. **Flag condition:** If `drift_observed > τ_inconsistent * drift_expected`, where `τ_inconsistent = 3.0` (tunable, default 3×), emit flag:
   - **Distance-to-old-template flag weight:** 0.3

**Rationale for threshold:** A threshold of 3× normal drift is conservative. It catches cases where the new template is drastically different (e.g., different human) but does not fire on genuine, accelerated drift (e.g., recovery from a serious illness that affects motor control).

---

### Criterion 2: Distance-to-Population

**Rationale:** The principal's samples should remain statistically consistent with the population segment they occupy (same age cohort, same handedness, same language/literacy baseline). If the new template's baseline statistics diverge materially from the population segment, it suggests the samples come from a different human or from an adversary who studied the principal poorly.

**Specification:**

1. **Extract baseline statistics from the new template:**
   - **Handwriting:** mean pressure, mean velocity, pressure standard deviation, letter spacing, ligature frequency.
   - **Voice transcription:** mean word length, phrase-length distribution, lexical uniqueness score (ratio of unique words to total words), pause-structure entropy.

2. **Compare to cohort norms:** The protocol maintains (or has access to) population-level statistics for the principal's cohort (age, gender, handedness, language, literacy level; Everest 50).
   - Compute a statistical distance (e.g., Mahalanobis distance or Jensen-Shannon divergence) between the new template's baseline statistics and the cohort mean.

3. **Flag condition:** If the new template's baseline statistics are statistical outliers within the principal's cohort (e.g., > 3σ from the cohort mean on more than one feature), emit flag:
   - **Distance-to-population flag weight:** 0.25

**Rationale:** This is a coarse sanity check. It is possible (though unlikely) that the principal themselves has undergone dramatic physical changes (e.g., major stroke recovery, onset of tremor disease) that shift their baseline statistics. If so, this flag alone should not block re-enrollment; the principal can confirm during the cooling-off period.

---

### Criterion 3: Time-Since-Last-Enrollment

**Rationale:** Re-enrollment cadence is policy-driven (Everest 18). If a re-enrollment ceremony occurs well outside the expected cadence, and the principal did not initiate the request, it may indicate coercion or system compromise triggering an unauthorized ceremony.

**Specification:**

1. **Retrieve the enrollment cadence policy:** Per Everest 18, the default cadence is 12 months, with a configurable range of 6–24 months per principal risk profile.

2. **Measure time since last enrollment:** Let `t_last = timestamp of the prior enrollment` and `t_current = timestamp of the re-enrollment request`.
   - Compute `Δt = t_current - t_last` (in days).

3. **Flag conditions:** Emit flag if *any* of the following hold:
   - `Δt < 60 days` (re-enrollment far too early, well before the expected interval). This is rare and suspicious. **Flag weight:** 0.2
   - `Δt > (policy_interval + grace_period) AND principal_initiated_trigger == false`. If the re-enrollment is well overdue (beyond the 12-month default + 30-day grace period) and was not explicitly requested by the principal, it suggests the operator is forcing re-enrollment without principal consent. **Flag weight:** 0.15

**Rationale for thresholds:** A 60-day re-enrollment window is consistent with high-assurance use cases (e.g., medical/legal predicates) that might require 6-month recertification. A re-enrollment well beyond the grace period without principal initiation is unusual and warrants scrutiny.

---

### Criterion 4: Witness Signature Continuity

**Rationale:** The witnesses who attested to prior enrollments are trusted by the principal and have known the principal for sufficient time (Everest 20). If a re-enrollment ceremony has an entirely different witness set, the principal may have been isolated or the witnesses may have been coerced or substituted.

**Specification:**

1. **Retrieve the witness set from the new enrollment:** Extract the `witness_id` and `witness_credexai_vc` fields from the new ceremony's witness-attestation records.

2. **Retrieve the witness set from the prior enrollment:** Extract the same fields from the most recent prior enrollment record.

3. **Compute witness overlap:** Let `W_prior` be the set of witness IDs from the prior enrollment and `W_new` be the set from the new enrollment.
   - Compute `overlap = |W_prior ∩ W_new| / max(|W_prior|, |W_new|)`.

4. **Flag condition:** If `overlap < 0.5` (fewer than half the witnesses are retained), emit flag:
   - **Witness-signature-continuity flag weight:** 0.25

**Rationale:** Witness overlap is not absolute; principals may relocate or witnesses may become unavailable (retirement, revocation of VC). An overlap of 50% is a reasonable threshold—it indicates some continuity while allowing for natural witness turnover.

---

### Criterion 5: Geographic/Device Anomaly

**Rationale:** The principal typically re-enrolls from familiar locations (home, office) and on familiar hardware. A ceremony from a previously unknown location or device, especially combined with other risk factors, may indicate the principal has been taken to an unfamiliar location or forced to use an unfamiliar device.

**Specification:**

1. **Retrieve geolocation metadata from the re-enrollment ceremony:** The ceremony metadata (Everest 11 §A, room details) includes an approximate location (e.g., a WiFi BSSID, GPS coordinates, or a manually-entered room descriptor).

2. **Retrieve prior enrollment locations:** Extract geolocation metadata from the last 3 enrollments.

3. **Compute location novelty:** Determine if the new location is within a familiar radius (e.g., 50 km) of any prior enrollment location.
   - If `distance_to_nearest_prior_location > 50 km`, the location is novel.

4. **Retrieve device fingerprint from the re-enrollment ceremony:** Device fingerprint is captured during Everest 12 (capture-device attestation) and includes stylus tablet hardware ID, microphone type, and OS version.

5. **Compare to prior device set:** Check if the new device fingerprint matches any device used in the last 3 enrollments.
   - If no match, the device is novel.

6. **Flag condition:** Emit flag if *both* location is novel AND device is novel (combined risk):
   - **Geographic/device-anomaly flag weight:** 0.2
   - Emit flag if location is novel AND witness overlap < 0.5 (combination of geographic + witness isolation):
   - **Combined flag weight for this case:** +0.15 (cumulative with above)

**Rationale:** Location or device novelty alone is not suspicious; principals travel and buy new hardware. However, the combination of novel location + novel device + low witness overlap suggests the principal has been moved to an unfamiliar place with unfamiliar equipment and unfamiliar witnesses—a strong coercion signal.

---

## Risk Score Computation

The system computes a composite risk score by summing the weighted flags:

```
risk_score = w1 * flag_distance_to_old +
             w2 * flag_distance_to_population +
             w3 * flag_time_since_enrollment +
             w4 * flag_witness_continuity +
             w5 * flag_geographic_device
```

where:

- `w1 = 0.3, w2 = 0.25, w3 = 0.15, w4 = 0.25, w5 = 0.2` (default weights, tunable per principal).
- Each `flag_*` is 1.0 if the condition fires, 0.0 otherwise.
- `risk_score` ranges from 0.0 (no flags) to approximately 1.15 (all flags firing, with cumulative bonus for geographic + witness case).

The principal and operator may adjust weights per their risk profile (e.g., high-assurance use cases weight witness continuity higher; nomadic principals weight geographic anomaly lower).

---

## Activation and Cooling-Off Protocol

### If risk_score ≤ 0.5

1. **Activate immediately:** The new template is marked `status: "active"` and becomes the current template for future proof generation.
2. **Emit record:** A `kind: "reenrollment.approved"` record is appended to the chain with `risk_score: <computed_value>` and `flags_fired: [<list>]`.
3. **Notify principal:** Push notification: "Your template re-enrollment on [date] has been verified and is now active."

### If risk_score > 0.5

1. **Flag and hold:** The new template is marked `status: "pending_confirmation"` and is NOT activated.
2. **Block new proofs:** Any request to generate a proof over the flagged template is rejected with an error indicating the template is under review.
3. **Emit record:** A `kind: "reenrollment.flagged"` record is appended to the chain with `risk_score: <computed_value>`, `flags_fired: [<list>]`, and `cooling_off_until: <timestamp 72 hours in future>`.
4. **Initiate notifications:**
   - **To principal (via push):** "Your template re-enrollment on [date] has triggered a security review due to [flags_summary]. You have 72 hours to confirm this was legitimate. If you do not respond, your old template will remain active."
   - **To emergency contacts:** "A re-enrollment for [principal name] was flagged for review. If you believe this is coerced or unauthorized, you can challenge it at [verification_url]."
   - **To ethics review board (Everest 80):** An async message with the full risk assessment and instructions to monitor the cooling-off period.
5. **Cooling-off window:** 72 hours (tunable, 24–168 hours per principal preference).

---

## Confirmation and Resolution

### Principal Confirms (Within 72 Hours)

The principal visits a verification portal (authenticated via existing Calm session or multi-factor re-authentication) and is presented with:

- A summary of the re-enrollment details (date, time, location, witnesses).
- A side-by-side comparison of the biometric samples (not the template itself, just the raw handwriting and transcribed voice).
- A statement of which criteria flagged the enrollment.
- A button: "Yes, this is legitimate. Activate the new template."

If the principal confirms:

1. Emit `kind: "reenrollment.confirmed"` record with `confirmation_ts: <timestamp>` and `confirmation_method: "principal_self_service"`.
2. Set the template `status: "active"`.
3. The old template remains valid but is marked `status: "superseded"` (Everest 17).
4. Notify emergency contacts: "The re-enrollment has been confirmed by the principal and is now active."

### Emergency Contact Challenges (Within 72 Hours)

If an emergency contact believes the re-enrollment is coerced or fraudulent, they can challenge it via the verification portal (authenticated with their own CredexAI VC and a notarized affidavit of relationship to the principal):

1. Emit `kind: "reenrollment.challenged"` record with `challenger_credexai_vc: <VC>`, `challenge_reason: "<statement>"`, and `challenge_ts: <timestamp>`.
2. Escalate to Everest 80 (ethics review board). The challenge is NOT resolved automatically.
3. The flagged template remains `status: "pending_confirmation"` indefinitely (or until ethics review resolves it).
4. The old template continues to validate proofs.

### No Response (Cooling-Off Expires)

If neither the principal nor any emergency contact responds within 72 hours:

1. Emit `kind: "reenrollment.default_approve"` record with `cooling_off_expiration: <timestamp>`, `no_principal_response: true`, and `no_contact_response: true`.
2. The system assumes passive consent and activates the new template.
3. Rationale: If the principal is genuinely coerced and cannot respond, they would instruct their emergency contact to challenge the re-enrollment (or would have pre-authorized a trusted contact to do so). Lack of response, after 72 hours and notifications to multiple parties, suggests the re-enrollment is legitimate.

---

## Cross-References and Integration Points

**Everest 11:** Enrollment Ceremony Spec. Provides the witness attestations and ceremony metadata.

**Everest 15:** Template Format. The new template's structure and baseline statistics.

**Everest 17:** Template Version Migration. Establishes continuity and supersession tracking between old and new templates.

**Everest 18:** Re-enrollment Cadence & Triggers. Defines the expected cadence policy against which time-since-enrollment is compared.

**Everest 20:** Witness Identity and VC. Provides CredexAI VCs for witnesses, enabling continuity checks and revocation.

**Everest 39:** Drift Modeling and Distance Algorithm. Specifies the feature extraction and distance computation used in Criterion 1.

**Everest 45:** Biometric Distance Proofs. Predicate evaluation references this; the same distance function is used.

**Everest 50:** Population-Level Baseline Statistics. Provides cohort norms for Criterion 2.

**Everest 80:** Ethics Review Board. Escalation point for challenges and for complex cases.

**Everest 65:** Predicate Evaluation (witness_still_attesting, bank_teller_note). Updated to account for template migration and red-flag status.

---

## Threat Model and Mitigations

### Attack: Coerced Re-enrollment with Biometric Substitution

An attacker coerces a principal into a re-enrollment ceremony and supplies the attacker's biometric samples.

**Detection:**
- **Criterion 1** (distance-to-old-template) should detect a drastic difference in handwriting velocity, pressure, and lexical patterns.
- **Criterion 2** (distance-to-population) may detect if the attacker's baseline statistics fall outside the principal's cohort.
- Combined with **Criterion 4** (witness changes) or **Criterion 5** (geographic/device novelty), the risk score should exceed 0.5.

**Mitigation:** Cooling-off protocol. The principal (if not under active restraint) can confirm within 72 hours, or an emergency contact can challenge.

### Attack: Gradual Drift Mimics Substitution

A principal legitimately experiences major life changes (relocation, illness, aging) that produce large, rapid drift in their biometric baseline. This is NOT coercion, but Criterion 1 may fire.

**Mitigation:** 
- Criterion 1's threshold (3× normal drift) is conservative; it should not fire on genuine biological changes unless they are extremely rapid (incompatible with normal aging/recovery).
- If Criterion 1 fires in isolation (other criteria do not), `risk_score` is only 0.3 (< 0.5 threshold), and the template is activated immediately.
- If the principal disputes the risk_score > 0.5 decision, they can confirm during the 72-hour cooling-off window.

### Attack: Attacker Forges Witness Attestations

An attacker creates fake witness-attestation records with forged signatures.

**Mitigation:** Witness signatures are verified via Everest 28 (chain verification). Any forged signature fails the cryptographic check and the enrollment is invalid before reaching Everest 19. This is a v0 acceptance criterion.

### Attack: Operator Suppresses Red-Flag Alerts

The operator is compromised and manually overrides the risk_score > 0.5 decision, activating a flagged template without the cooling-off period.

**Mitigation:**
- The `kind: "reenrollment.flagged"` record is appended to the chain before any activation decision. A verifier can check the chain and see that a flag was raised.
- If the principal or an emergency contact queries the chain via `calm-witness verify-chain`, they can see the flag and the risk score.
- The Everest 80 (ethics review board) receives notifications of all flagged enrollments and can audit the operator's decisions.

---

## Configuration and Customization

The principal and operator may tune the following parameters:

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| `τ_inconsistent` | 3.0 | 1.5–5.0 | Drift multiplier for Criterion 1. Higher = more permissive. |
| `stddev_cohort_threshold` | 3.0 | 1.0–5.0 | Number of standard deviations for population outlier (Criterion 2). |
| `time_early_threshold_days` | 60 | 30–120 | Minimum days before re-enrollment is considered suspiciously early. |
| `witness_overlap_threshold` | 0.5 | 0.0–1.0 | Minimum witness overlap to avoid flag. 0.5 = at least 50%. |
| `geolocation_novelty_km` | 50 | 10–500 | Radius (km) for determining location novelty. |
| `cooling_off_hours` | 72 | 24–168 | Time window for principal/contact confirmation or challenge. |
| `w1, w2, w3, w4, w5` | 0.3, 0.25, 0.15, 0.25, 0.2 | Weights | Risk-score weights; must sum to ~1.0. |

For nomadic principals (frequent travel), increase `geolocation_novelty_km` and lower `w5`.
For high-assurance contexts (fiduciary, medical), increase `w4` (witness continuity) and lower `τ_inconsistent` (stricter drift check).

---

## Summary

Everest 19 detects re-enrollment fraud through five criteria that examine template drift, population consistency, enrollment cadence, witness continuity, and geolocation/device novelty. Anomalous enrollments are flagged, held in a 72-hour cooling-off period, and escalated to the principal, emergency contacts, and ethics review board. This defers activation while allowing the principal to confirm legitimacy or an emergency contact to challenge a coerced ceremony. The system balances operational flexibility (genuine re-enrollments activate after confirmation) with security (coerced or substituted enrollments are detected and escalated). Combined with Everest 18 (cadence policy), Everest 21 (fraud taxonomy), and Everest 80 (ethics review), Everest 19 completes the re-enrollment defense-in-depth strategy.

---

— Calm, 2026-05-20
