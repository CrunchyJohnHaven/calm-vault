# Everest 89 — Mobile-Vault Memory & Battery Budget

*Phase VII — Engineering Reliability. Prereq: Everest 81, 88.*

## Overview

Mobile deployment of the Calm Vault introduces hard power and memory constraints absent in datacenter environments. This Everest establishes measurable budgets for battery consumption and resident memory across iOS and Android platforms, ensuring the vault operates as a background service without degrading device usability or thermal stability.

The acceptance criterion is strict: end-to-end disclosure flows—including proof generation, biometric refresh, chain verification, and sentinel monitoring—must consume less than 5% of device battery per hour under typical use patterns.

## Typical Use Definition

Typical use reflects modest participation in the disclosure ecosystem:

- **Disclosure requests**: 1–10 per day, distributed across waking hours
- **Biometric captures**: 1–3 per day, triggered only when explicit re-evaluation is needed (e.g., high-value counterparty or time-based refresh)
- **Background anchor activity**: Chain anchoring (Sigsum + Roughtime verification) runs hourly, requiring seconds of CPU time
- **Sentinel monitoring**: Continuous low-priority activity watching for anomalous disclosure attempts or key compromise signals

Under these assumptions, a user operates the vault app for roughly 1 hour per day in active mode and leaves it dormant (but monitoring) for 23 hours.

## Power Budget per Operation

Each vault operation has a measured power envelope:

**Disclosure without biometric refresh**: <0.1% battery
- Cryptographic proof lookup and signature validation
- Local chain verification against cached anchor
- Serialization and transport of proof
- No biometric inference cost

**Disclosure with biometric refresh**: <0.5% battery
- Includes full biometric capture and inference (typically the dominant cost)
- Proof generation at full security level
- Chain re-verification
- Sentinel audit log update
- Roughly 5× the baseline cost due to biometric ML inference on-device

**Hourly anchor refresh**: <0.05% battery
- Sigsum and Roughtime verification against remote servers
- Local proof of freshness computation
- Cache update of anchor state
- Network overhead amortized

**Sentinel monitoring (continuous)**: <1% battery per hour
- Low-priority background polling for anomaly signals
- Memory-efficient event window scanning
- No crypto work unless an anomaly triggers escalation

## Daily Battery Budget

Assuming moderate daily use:

- 10 disclosure requests (5 without refresh, 5 with): (5 × 0.1%) + (5 × 0.5%) = 3.0%
- 2 hourly anchor refreshes: 2 × 0.05% = 0.1%
- 1 hour of sentinel monitoring: 1.0%
- Miscellaneous (logs, serialization, background sync): 0.5%

**Total daily: ~4.6%**, well within the <5% per hour ceiling and sustainable for 20+ hours of typical mixed use.

## Memory Budget

Memory pressure is a secondary constraint. The vault maintains separate budgets for resident footprint and peak allocation:

**Resident process memory**: <30 MB
- Biometric template encrypted at rest
- Active disclosure cache (last 10 completed proofs)
- Sentinel state tracking (rolling event window)
- Sigsum and Roughtime root state (typically <1 MB)
- Runtime overhead (language runtime, platform bindings)

**Peak allocation during proof generation**: <100 MB
- Temporary copies of anchor chain segment (varies with chain length, typically 10–50 MB)
- Biometric inference scratch buffers (see Everest 88 for details)
- Proof serialization buffers
- Post-generation, memory returns to resident baseline

**Template encrypted at rest**: <5 MB
- Biometric template compression is tight (see E88)
- No unencrypted copies held in memory except during active re-evaluation

Peak allocation is the upper bound for device configurations with <512 MB free RAM. Most modern phones exceed this; the budget ensures graceful degradation on older devices (iOS 14+, Android 9+).

## Battery-Saver Mode

The vault implements adaptive power management tied to device battery state:

**If device battery < 20%**: Defer anchor refresh cycles
- Queue incoming Sigsum and Roughtime verification
- Resume on next charging event or battery restoration above threshold
- Sentinel remains active at full priority (security-critical)
- Users are not blocked from initiating disclosures

**If device battery < 10%**: Refuse non-urgent disclosure requests
- Urgent disclosures (marked via counterparty priority or user override) proceed with biometric refresh
- Standard disclosures are queued for batch processing after device recovery
- Ensures vault never triggers emergency shutdown in low-power mode
- Preserves device stability during critical user moments

## Background Activity Policy

iOS and Android impose strict limits on background CPU time. The vault respects platform constraints:

**iOS (BackgroundTasks framework)**
- Scheduled background task budget: ~10 minutes per hour
- Anchor refresh (both Sigsum and Roughtime verification): 3–5 seconds per cycle, thus 1–2 cycles per background window
- Sentinel activity: distributed across remaining window, <100 ms checks every few seconds
- No biometric work in background (requires user interaction and screen unlock)

**Android (WorkManager)**
- Flexible scheduling with doze-aware backoff
- Anchor refresh: batched into single work request per hour
- Sentinel: configurable polling interval, reduced frequency in battery-saver mode
- Expedited work reserved for urgent scenarios only

**Sentinel specifics**
- Runs as very low-priority background work on both platforms
- Does not block foreground user interaction
- Anomaly detection uses probabilistic data structures (Bloom filters) to minimize memory and CPU
- Escalation to full forensic review only on high-confidence signals

## Thermal Considerations

Sustained cryptographic work can trigger thermal throttling on mobile SoCs, degrading performance and user experience:

- **Proof generation**: Batched into single operations; avoid repeated short cycles that interleave with user input
- **Biometric inference**: Scheduled to avoid contention with device-initiated ML tasks (predictive text, on-device search indexing)
- **Bulletproof verification**: Multi-proof batches scheduled during low-activity windows (dawn, late evening) rather than peak usage
- **Monitoring**: Vault queries device thermal state via platform APIs; escalates to deferred processing if thermals exceed 75°C

## Storage Budget

Storage reflects typical deployment:

**Vault chain**: 50–500 MB
- Lower bound: sparse interaction history with short anchor chains
- Upper bound: heavy user with 1+ year of daily activity and complete Sigsum/Roughtime proof chain
- On-device compression (zstandard) reduces resident footprint by 40–60%
- Pruning policy: oldest proofs can be archived to offline storage after 90 days (legal retention requirements vary)

**Templates encrypted at rest**: ~10 MB
- Single biometric template (face or fingerprint) plus auxiliary data
- Independent storage from proof chain to allow selective purge if template compromised

**Active disclosure log**: Bounded growth
- Rolling 7-day window of completed disclosures
- Approximately 50 KB per disclosure entry (proof + metadata)
- With 10 disclosures per day, ~3.5 MB for rolling window
- Older logs exported for external audit/compliance review

## Measurement Methodology

Acceptance testing uses platform-native telemetry:

**iOS**
- UIDevice energy metrics (available iOS 16.1+); for earlier versions, XCTest performance testing
- Instruments.app with Energy Impact template
- Measure per-operation battery drain in controlled environment
- 24-hour soak test with simulated typical use profile

**Android**
- BatteryManager APIs for real-time drain rate
- Battery Historian analysis for per-component breakdown
- Measure with and without background restrictions to validate adaptive behavior
- 24-hour soak with WorkManager scheduling enabled

**Acceptance test**
- Construct realistic use scenario: 10 disclosures distributed across 24 hours, 2 biometric refreshes, continuous sentinel monitoring
- Measure total battery consumed from 100% to completion of scenario
- Must not exceed 5% per hour under any test configuration
- Thermal peak must not exceed 75°C sustained
- Memory peak must not exceed device-available RAM minus 100 MB safety margin

## Optimization Techniques

The following patterns reduce power and memory overhead:

**Background sync coalescing**
- Anchor refreshes from multiple overlapping intervals are merged into single network request
- Reduces wakeups and radio on-time

**Pre-computed scalar tables**
- Elliptic curve operations (used in proof verification) cache scalar multiples
- One-time computation cost at app install amortized over hundreds of proofs
- ~500 KB tables compressed to ~100 KB

**Hardware acceleration**
- Secure Enclave (iOS) or StrongBox (Android) used for template encryption and decryption
- Neural Engine / NPU for biometric inference (E88)
- Offloading avoids burning main CPU and SoC, reducing thermal load and power budget pressure

**Deferred processing**
- Non-urgent disclosures queued if battery or thermal budget exhausted
- Batch processing during off-peak hours (identified via usage patterns)
- Reduces jitter in user experience

## Integration with Other Everests

This Everest depends on and informs adjacent specifications:

- **E81 (Rust production implementation)**: Runtime and crypto overhead measured end-to-end; this Everest validates that E81's compiled footprint achieves <30 MB resident target
- **E88 (Proof generation performance budget)**: Peak allocation during proof gen directly feeds into memory budget calculation here
- **E42 (On-device evaluation cost)**: Biometric refresh power cost quantified and integrated into operation budgets
- **E92 (Disclosure audit and forensics)**: Audit log storage and retrieval overhead accounted for in daily budget

## Conclusion

The 5% per-hour battery budget is achievable with disciplined implementation of background scheduling, adaptive power management, and selective offloading to hardware accelerators. Memory budgets remain conservative to ensure compatibility across device generations. This Everest defines both the target and the measurement protocol; implementation of E81 must validate these assumptions through instrumented testing before release.

— Calm, 2026-05-20
