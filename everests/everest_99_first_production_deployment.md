# Everest 99 — First Production Deployment

*Phase VIII — Governance & Scale. Prereq: Everest 81–98 all bagged.*

Calm Witness moves from design and testing into operational reality. This deployment plan defines a three-phase rollout: internal dogfooding (2 weeks), soft launch with pre-arranged counterparties (4 weeks), and public availability (open-ended). Success is measured by live verifications from real counterparties using public SDKs. This document specifies the operational strategy; the actual deployment is a separate milestone.

## Pre-Deployment Verification Checklist

Before the live operator launches, these gates must close:

1. **Everest 81** — Rust production implementation complete and passes CI/CD.
2. **Everest 85** — Adversarial fuzzers run ≥18 hours nightly, ≥30 days flake-free.
3. **Everest 90** — Third-party security audit complete; high/critical findings remediated; report published.
4. **Everest 91** — NIST submission filed proposing Calm Witness as a candidate standard.
5. **Everest 92** — `calm-witness` published under Apache-2.0 on GitHub with signed release tags.
6. **Everest 93** — Three independently operated Sigsum witnesses committed to publishing chain heads (SLA ≤60s).
7. **Everest 94** — Five independent Roughtime servers committed; N-of-M quorum policy (N=3, M=5).
8. **Everest 95** — Public governance policy published: predicate proposal, ≥30-day review, ≥5-person voting panel.
9. **Everest 97** — Two-handshake integration with Calm Pact verified; abort-on-Pact-failure tested.
10. **Everest 98** — Counterparty Implementer's Guide published with code examples in Python and JavaScript.

## Phase A: Internal Dogfooding (2 Weeks)

**Objective:** Validate end-to-end operations in a controlled environment before external parties engage.

**Activities:**

- Deploy operator to hardened infrastructure; verify all crypto modules load and HSM responds.
- Principal (John Bradley) completes enrollment ceremony (Everest 11): handwriting + voice transcription samples captured, templates committed to Sigsum, chain head published.
- Execute ≥5 disclosure cycles across canonical predicates (`in_baseline_24h`, `biometric_match_within(τ)`, `principal_consents_to_disclose(p, c)`, `bank_teller_note_active`, `cognitively_atypical_baseline`). Verify proof generation and verification.
- Test incident flows: Sigsum outage, Roughtime clock skew, consent revocation, template re-enrollment, emergency duress-bit push.
- Audit vault logs; verify append-only filesystem guarantees. No unauthorized access detected.
- Measure performance: proof generation <1s on commodity hardware; chain verification scales to 100+ records without cliff.
- Daily metrics report to principal: uptime, latency (p50/p95/p99), error rates, anomalies.

**Success Metrics:**
- Zero unplanned downtime.
- All ≥5 disclosure cycles succeed.
- All incident-response flows execute and are documented.
- Chain heads published to Sigsum and Roughtime ≥3 times without failure.
- Vault audit clean; no mutations detected.
- Performance ≥20% faster than Everest 88 budgets (headroom for optimization).

**Gate:** Principal and operations lead sign go/no-go decision. Extend Phase A by up to 1 week if metrics fail.

## Phase B: Soft Launch with Pre-Arranged Counterparties (4 Weeks)

**Objective:** Validate system with real external counterparties. Confirm public SDKs and documentation are sufficient for independent verification.

**Counterparty Cohort:**

1. **Aligned AI-Collective (via Calm Pact):** Peer organization running both Calm Pact (directive alignment) and Calm Witness (user-state attestation) in composition. Pre-arranged; has accepted this plan.
2. **Research-Mode Journalists (1–2):** Cryptography staff or researchers interested in protocol understanding, not yet publishing. Will verify proofs and test envelope parsing.
3. **Legal Counsel:** Attorney with expertise in AI governance, privacy, biometric law. Validates counterparty-authorization flows and jurisdiction-specific constraints (Everest 79).
4. **Calm Test Counterparties:** Internal; provide baseline verification workload and stress-testing.

**Activities:**

- Onboard counterparties with 1-hour briefing covering protocol, threat model, and this plan. Provide: public repository, Everest 98 guide, pre-signed test envelopes, CLI tool, Slack channel.
- Each counterparty verifies ≥3 proofs independently. Report success/failure and latency.
- Collect feedback on documentation, SDK usability, proof format. Iterate SDK and docs.
- Security code review (≥2 hours) with Sigsum operator cryptographer. Confirm operator code matches published release.
- Legal review: validate predicates and disclosure logging satisfy privacy law in each jurisdiction. Identify red-flag predicates.
- Execute ≥10 successful disclosures across ≥3 counterparties. Each must verify cryptographically, complete within SLA, generate vault disclosure record, and receive independent counterparty verification.
- Simulate incident: revoke consent mid-phase. Confirm cached proofs invalidated and new requests properly denied. Counterparties notified.
- Daily metrics: operator uptime, disclosure success rate, average latency, Sigsum/Roughtime availability, vault log freshness.

**Success Metrics:**
- ≥10 independent verifications across ≥3 counterparties; zero cryptographic failures.
- Zero high-severity bugs.
- Zero false-positive duress signals (`bank_teller_note_active`).
- Verified Calm Pact handshake: both Pact and Witness proofs verify; no information leakage.
- All three Sigsum operators publish ≥2 chain heads each.
- All five Roughtime servers respond with consistent timestamps.
- Legal review: zero blocking issues; minor gaps have documented remediation timelines.
- Counterparty documentation rated ≥8/10 clarity by all participants.

**Gate:** Review panel (Calm ops lead + aligned collective's tech lead + external cryptographer) votes unanimously "ready to proceed." Extend Phase B by ≤2 weeks if metrics fail.

## Phase C: Public Availability (Open-Ended)

**Objective:** Calm Witness operator available to any counterparty completing public onboarding. Success measured by organic adoption and independent verification.

**Onboarding:**

1. Counterparty reads Everest 98 guide and Calm Pact protocol (Everest 97 references).
2. Installs verifier SDK from crates.io / PyPI / npm.
3. Sends signed disclosure request (Everest 66) to `api.calmwitness.thecreativitymachine.ai`.
4. Operator verifies request is well-formed; counterparty identity binds to valid CredexAI credential (Everest 69). If principal authorized this counterparty class, operator generates proof.
5. Counterparty verifies proof locally using SDK and public docs.
6. Counterparty accepts disclosed bit or denies if proof fails verification.

**Operations:**

- **24/7 On-Call:** S1 incidents (operator unreachable, verification failure >1%, HSM failure) escalated within 15 minutes.
- **Runbook:** Every failure mode (Everest 9) has tested response procedure; quarterly table-top exercises.
- **Revocation:** Principal detects crypto weakness, key compromise, or template fraud → operator issues revocation directive → published to counterparties → proofs issued after revocation timestamp rejected.
- **Telemetry (Privacy-First):** Request count/week, success rate, latency p50/p95/p99, Sigsum/Roughtime availability, uptime. NO per-counterparty tracking, predicate IDs, biometric data, vault logs.
- **Public Dashboard:** `status.calmwitness.thecreativitymachine.ai` shows uptime (24h/7d/30d), request volume, latency p95, infrastructure availability. Refreshes every 15 minutes.

**Phase C Success Metrics (6 Months):**

At least one non-Calm-affiliated organization (not Calm Pact aligned, not Calm-employed, not Calm-funded) independently implements a verifier, constructs a disclosure request, receives proof, verifies end-to-end, and publishes a write-up documenting verification steps. This satisfies Everest 100.

**Sustainability (Year 2+):**
- Organic adoption by ≥5 counterparty organizations (media, academic labs, peer collectives, compliance vendors).
- Zero high-severity security incidents.
- Uptime ≥99.5% over rolling 30-day windows.
- Predicate vocabulary expanded to ≥10 via Everest 95 governance; ≥2 externally proposed predicates adopted.
- Post-quantum migration (Everest 96) initiated; feasibility study published.
- Calm Pact + Calm Witness composition standard in ≥2 peer collective handshakes.

## Operator Infrastructure

**Hardware:**

- Bare-metal or isolated cloud instance (no multi-tenant hypervisor). ≥8 cores, ≥2 GHz base frequency. ≥64 GB RAM. ≥1 TB SSD for logs and ephemeral state. Redundant gigabit Ethernet to two ISP uplinks; automatic failover.

**HSM:**

- YubiKey 5 Series or FIPS-140-2 Level 3+ equivalent. Principal master key (Ed25519 signing per Everest 68) stored only in HSM. Operator software cannot extract key. All signatures hardware-backed: disclosure responses, chain-publication directives, consent records.

**Network & TLS:**

- DNS: `api.calmwitness.thecreativitymachine.ai` and `vault.calmwitness.thecreativitymachine.ai`.
- TLS 1.3 only (no fallback); OCSP stapling. Pinned in SDK (Everest 84). Rotated 30 days before expiry.
- Rate limit: ≤100 disclosure requests/minute per counterparty IP. Adaptive bursting permitted if 24h average respected.

**Logging & Monitoring:**

- Disclosure requests, proof generations, state changes logged with nanosecond precision; rotate/compress every 24h. Write-once (WORM) or append-only FS with monitoring (Everest 27). Mutation attempts trigger alerts.
- Monitoring agents check every 60s: operator running, Sigsum/Roughtime reachable, HSM responding, logs accumulating. Page on-call if any check fails >5 minutes.

**Disaster Recovery:**

- Principal vault encrypted, replicated to two off-site locations (cloud + RAID NAS). Real-time push replication; RTO <4 hours.
- Operator binaries and config version-controlled in private Git (Everest 92 public release is source of truth; divergence forbidden).
- Quarterly recovery drill: spin up operator on fresh instance using only backup vault, encrypted backups, Git repo. Verify clean start and <15 minute response time. Document result.

## Incident Response

**Tiers:**

- **S1 (Critical):** Operator unreachable or verification fails >1%. HSM failure, Sigsum down, crypto regression. Page immediately; 15 min to restore to S2 or post public update.
- **S2 (High):** Latency >10s p95 or Sigsum/Roughtime degraded. Establish bridge ≤30 min; post status if >1 hour to fix.
- **S3 (Medium):** Documentation unclear, minor operational issue (disk >80%). Notify lead; remediate within 48h.
- **S4 (Low):** Scheduled maintenance. Log and monitor.

**Crypto Verification Failure:**

>0.1% failures for crypto reasons = S1. Possible causes: regression in Rust (rollback immediately), template corruption (principal re-enrolls per Everest 17, old proofs marked "stale"), Sigsum/Roughtime incorrect data (verify against independent sources; escalate if three sources agree data is wrong).

**Key Compromise:**

Operator signs emergency revocation record (`kind: emergency_revocation.v0`). Revocation published to counterparties; future requests denied. Principal and HSM vendor coordinate HSM replacement and re-enrollment. New key attested in CredexAI registry before new proofs issued. All outstanding proofs invalidated. S1 incident; >4 hour recovery expected.

## Telemetry and Metrics

**Collected (Aggregated, Anonymized, No Per-Counterparty Tracking):**

- Request volume (count/week, all counterparties).
- Success rate (% of requests yielding valid proof).
- Latency: p50, p95, p99 end-to-end disclosure time (milliseconds).
- Availability: Sigsum publication success rate, Roughtime query success rate.
- Incidents: count of S1/S2/S3 per month; MTTR per incident.

**NOT Collected:**

- Counterparty identity or IP.
- Predicate IDs requested.
- Principal biometric data or vault contents.
- Consent records or revocations.
- Self-report text or transcriptions.

**Public Dashboard** (`status.calmwitness.thecreativitymachine.ai`):

- Uptime (last 24h, 7d, 30d).
- Request volume (requests/hour, requests/day).
- Latency p95.
- Sigsum/Roughtime availability.

Refreshes every 15 minutes. 30-day rolling history retained. No authentication required.

## Acceptance

Everest 99 closes when:

1. All pre-deployment gates (checklist items 1–10) pass.
2. Phase A completes; all success metrics met; principal and ops lead sign go/no-go.
3. Phase B completes; all success metrics met; review panel votes unanimously "ready."
4. Phase C initiates; public API live at `api.calmwitness.thecreativitymachine.ai`.
5. Principal, operations lead, and one independent external stakeholder jointly sign: "Calm Witness is in production and operational."

The actual deployment (provisioning, certificates, counterparty coordination, monitoring setup) happens in downstream operational milestones referencing this plan.

--- Calm, 2026-05-20
