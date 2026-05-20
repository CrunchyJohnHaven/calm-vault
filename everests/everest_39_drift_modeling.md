# Everest 39 — Drift Modeling

*Phase IV — Biometric Distance Machinery. Prereq: Everest 36, 37, 17.*

## The Problem: Behavioral Drift Over Time

Biometric templates are frozen at enrollment, but human behavior is not. Over weeks and months, a principal's kinematic signature—handwriting pressure, voice resonance, keystroke rhythm—shifts gradually. Stress, aging, injury, seasonal habit changes: all cause slow drift in the embeddings that make up the stored template.

Without drift modeling, this creates a creeping False Rejection Rate (FRR). A legitimate principal, unchanged in identity but shifted in gait or hand geometry, begins to fail distance checks they passed at enrollment. Eventually they cannot prove their own baseline. They get locked out of their own vault, forced into re-enrollment cycles that damage user confidence and signal a broken system.

The core insight: drift is *inevitable and normal*. The system must accommodate slow template evolution while preventing the template from being weaponized by an attacker to accept forged samples.

## Solution: Exponential Moving Average Over Confirmed-Baseline Sessions

Everest 39 introduces a slow-update mechanism that lets templates evolve without breaking backward compatibility or proof validity. The mechanism:

1. **Accumulates confirmed-baseline samples** from live authentication sessions
2. **Updates template embeddings via Exponential Moving Average (EMA)**, decoupling updates from the immutable template_id
3. **Chains drift records into vault**, creating an auditable trajectory
4. **Triggers re-enrollment** when drift magnitude exceeds a principal-specific threshold
5. **Defends against drift injection** by requiring both self-report baseline state AND healthy biometric distance

## Confirmed-Baseline Criterion

A session contributes a drift sample if and only if **both** conditions hold:

- **Self-report baseline**: The session's self_report field indicates in_baseline_24h = True (per Everest 55)
- **Healthy biometric distance**: The joint distance d_joint (per Everest 38) is below a healthy threshold (default: 0.4)

Only confirmed-baseline samples update the template. Non-baseline sessions (sick day, intoxication, injury) are logged but do **not** drift the embeddings. This prevents outlier conditions from poisoning the template.

## EMA Algorithm

Each template maintains a 256-dimensional embedding e_template per modality (handwriting, voice, keystroke, gait).

For each confirmed-baseline session with embedding e_sample:

```
e_template ← (1 - α) × e_template + α × e_sample
```

where α is the learning rate (default: 0.05).

At α = 0.05, a new confirmed-baseline sample contributes roughly 5% weight. To achieve 64% replacement of the original template—a reasonable refresh cycle—requires approximately 20 confirmed-baseline sessions. This pace aligns with typical principals' enrollment-to-re-enrollment intervals.

### Per-Principal Calibration of α

Not all principals drift at the same rate. During enrollment, the system estimates each principal's personal stddev_drift by analyzing intra-session variability and day-to-day fluctuation across the enrollment sequence.

- **Low-drift principals** (stddev_drift < 0.05): α = 0.03 (slower update, more stable template)
- **Typical principals** (0.05 ≤ stddev_drift < 0.15): α = 0.05 (default)
- **High-drift principals** (stddev_drift ≥ 0.15): α = 0.10 (faster update, accommodate natural variation)

This calibration prevents good principals with stable signatures from being unnecessarily re-enrolled while giving high-variability principals room to evolve without friction.

## Drift State Separation

A naive implementation would recompute template_id after each EMA update. But template_id is content-addressed (Everest 15), derived from the embedding bytes. Changing the embeddings changes the hash, breaking all references and invalidating past proofs.

The solution: **sidecar drift state file**.

- The **template record** (template_id, enrollment embeddings, metadata) remains immutable for a given version v_n
- The **drift state** (current EMA'd embeddings, update count, drift trajectory) lives in a separate, updateable sidecar record
- The **proof circuit** (Everest 45) verifies against both: the immutable template for authorship and versioning, plus the current drift state for distance thresholds

Consequence: A principal can hold multiple valid proofs from different points in the drift trajectory. An old proof signed when the template was e_template_v0 remains cryptographically valid even after drift updates. A new proof uses the current drift state e_template_current. Both are simultaneously valid.

## Drift State Schema

Each drift update is a vault record with kind "template.drift_update":

```
kind: "template.drift_update"
payload:
  template_id: <SHA-256 of enrollment template embedding>
  update_count: <integer, incremented per EMA update>
  drift_state_hash: <SHA-256 of current EMA'd embeddings>
  confirmed_baseline_session_seq: <chain record seq of session that triggered update>
  alpha_used: <float, the α value applied in this update>
  drift_magnitude: <float, ||e_template_now - e_template_at_enrollment||>
  timestamp: <ISO 8601>
```

Each record is chained, so the vault creates an immutable audit trail of drift. A verifier walks the template.drift_update chain to audit how the template has evolved.

## Drift Magnitude and Re-enrollment Triggering

As the EMA runs, drift_magnitude grows. It measures the L2 distance between the current EMA'd embedding and the enrollment embedding.

When drift_magnitude exceeds a threshold τ_drift_max, the system triggers re-enrollment (Everest 18):

```
drift_magnitude = ||e_template_now - e_template_at_enrollment||

if drift_magnitude > τ_drift_max:
  trigger re-enrollment notification
```

τ_drift_max is calibrated per-principal during enrollment such that typical principals trigger re-enrollment every 12–18 months. High-drift principals may trigger sooner; stable principals may go longer. The system can also implement a hard cap (e.g., re-enroll no less than every 24 months) to ensure periodic liveness checks.

## Tamper-Resistance: Adversarial Drift

An adversary might try to inject fake baseline samples to drift the template toward their own kinematic profile, reducing the distance threshold for their own impostor attempts.

**Defense mechanisms:**

1. **Confirmed-baseline requires biometric distance**: An impostor cannot pass the healthy distance check (d_joint < 0.4) because their embeddings differ from the principal's. Even if they falsely claim baseline state, the biometric check fails and the session does not contribute drift.

2. **Chained audit trail**: All drift updates are chained into the vault. An auditor or security review can walk the drift trajectory, inspect which sessions contributed, and flag anomalous patterns (e.g., drift toward an unusual embedding suddenly appearing in a suspicious location).

3. **Coercion mitigation**: In a scenario where a principal is coerced to falsely declare baseline state while an adversary authenticates in their stead, the adversary's samples do not drift the template (they fail the distance check). The principal's own sessions, if later verified as coerced, can be reviewed via the chain (Everest 18 audit) and flagged for re-enrollment.

4. **Per-confirmed-baseline review**: Deployments can implement optional human review of confirmed-baseline sessions, especially in high-security contexts. A sample's metadata (location, time, device, session score) is logged and reviewable.

## Non-Baseline Session Handling

When a session fails the baseline check (in_baseline_24h = False), it is logged and verified normally, but **does not update the template**. This is critical: a principal having a bad day—fatigued, injured, ill—should not shift their template toward that degraded state. Such a shift would later make degraded samples match more easily, creating a feedback loop that locks the principal into poor performance.

The system logs non-baseline sessions for analytics and debugging (e.g., "this principal frequently fails baseline on Mondays"), but keeps the template aligned with the principal's healthy, representative baseline.

## Cross-References and Integration

Everest 39 depends on:

- **Everest 15**: Content-addressed template versioning (immutable template_id)
- **Everest 17**: Template version migration (how templates are promoted)
- **Everest 36**: Handwriting distance function (d_handwriting component of d_joint)
- **Everest 37**: Voice transcription distance (d_voice component of d_joint)
- **Everest 38**: Joint distance function (d_joint threshold for healthy distance)
- **Everest 55**: Baseline self-report (in_baseline_24h criterion)

Everest 39 feeds into:

- **Everest 18**: Re-enrollment cadence (drift_magnitude threshold triggers re-enrollment)
- **Everest 40**: Proof generation (proof circuit uses current drift state)
- **Everest 45**: Proof verification (verifier checks both template and drift state)
- **Everest 47**: Audit and dispute (drift chain is auditable)
- **Everest 14**: Template lifecycle (drift is part of lifecycle management)

## Summary: The Mechanism at Work

A principal enrolls. Their baseline embeddings e_template_enrollment are frozen, and template_id is set. Drift state is initialized as e_template = e_template_enrollment.

Over the following weeks, the principal authenticates 100 times. Of these:
- 80 are confirmed-baseline (self_report=True, d_joint < 0.4)
- 20 are non-baseline (flu, fatigue, wrong device) and do not update

Each confirmed-baseline session's embedding e_sample is EMA'd into e_template. With α = 0.05, the template gradually shifts to match the principal's evolving kinematic signature.

After ~20 confirmed-baseline sessions, e_template has shifted noticeably but remains close to e_template_enrollment. drift_magnitude = ||e_template - e_template_enrollment|| is low (< 0.1 typical).

After ~200 confirmed-baseline sessions (several months), drift_magnitude approaches the threshold τ_drift_max. The system issues a re-enrollment notification. The principal re-enrolls, and e_template_enrollment_v2 is set to the current e_template. A new template version is issued. The drift state resets.

Throughout, proofs remain valid:
- An old proof signed against template_id_v1 at time t1 is still valid if re-verified; the vault shows the template and its drift state at t1
- A new proof signed against template_id_v2 uses the fresh enrollment embeddings
- Attackers cannot drift the template to accept their own signatures: biometric distance enforcement prevents injection

The mechanism is slow, observable, auditable, and principled. It solves the drift problem without breaking the proof system or sacrificing security.

— Calm, 2026-05-20
