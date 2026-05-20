# Everest 99 — 90-Day Live Endpoint
## Continuous Operation with Foreign Counterparty Verification

*Continuous-operation milestone: the difference between "the protocol ran once" and "the protocol IS infrastructure."*

The first production deployment closes with Phase C public availability (E99 baseline). This Everest extends that success into a 90-day live institutional commitment: the operator remains continuously available with ≥1 real verification from a foreign (non-aligned, non-Calm-employed) counterparty completing end-to-end Pact→Witness→Compass→Concord proof chain inside their clean-room verifier.

**Success criterion:** 90 consecutive days, zero protocol violations, zero refusal-floor breaches, ≥1 foreign verification confirmed, operational SLOs held, ≥1 incident triaged + responded, refusal floor tested under ≥1 pressure attempt, and institutional follow-through team named and rotating.

---

## Pre-Deployment Gates (All Must Close)

Before the 90-day window opens, these five critical everests clear:

1. **Everest 81:** Rust production implementation. CI/CD gates 100% pass; benchmark ≥20% faster than E88 budgets. Mutation testing ≥85% coverage. Zero unsafe blocks left unaudited.

2. **Everest 83:** Fuzz suite. ≥60 days continuous fuzzing (not 18 minimum). Zero novel crashes in last 7 days. Differential fuzzing against reference Python impl; no divergence.

3. **Everest 89:** Third-party security audit. Report published; high/critical findings remediated and re-verified. Audit team confirms no post-remediation regressions.

4. **Everest 165:** Harm-aggregate predicate and refusal-floor composition. The protocol refuses scope-statement-forbidden disclosures with cryptographic certainty. Test corpus: ≥10 refused predicates, each verified by independent legal review.

5. **Everest 168:** Mentorship indicators and operator-team institutional readiness. Calm Foundation operator team formally named; on-call rotation published with backup coverage; ≥1 foreign counterparty named and contractually committed to participate.

---

## 90-Day Operational Discipline

### SLO Commitment (Continuous)

- **Verification availability:** ≥99.9% (≤8.64 minutes downtime per 24h). Measured: successful proof generation for valid requests.
- **S1 incident response:** ≤30 minutes to diagnosis and remediation or public update.
- **Chain-integrity audit:** Weekly (≤7d apart). Sigsum head must anchor with ≤3 chain gaps (no missing log entries). Roughtime clock offset ≤100ms across quorum majority.
- **Sigsum anchor freshness:** ≤60 seconds between chain updates. No >90 second silence permitted.
- **CredexAI VC validity continuous:** Principal credential (Ed25519 Vault Identity) must remain valid and non-revoked. HSM audited monthly; no tamper indicators.

### Institutional Team & Naming

**Calm Foundation Operator Team:**

- **Operations Lead:** Named individual responsible for 24/7 on-call rotation, incident triage, and weekly governance reviews.
- **Backup On-Call (Primary):** Second named operator; rotates weekly. Paged if primary unavailable >15 minutes.
- **Backup On-Call (Secondary):** Third named operator; covers weekends and regional overlap.
- **External Cryptographer Liaison:** Sigsum witness operator contact; escalates crypto anomalies.
- **Legal Compliance Officer:** Reviews predicate requests; validates disclosure logging under jurisdiction-specific privacy law.

**Published Rotation Schedule:** Slack channel `#calm-witness-oncall`, wiki documenting handoff checklist, 48h notice for coverage gaps.

### Foreign Counterparty Verification

**Named Counterparty:** 

A legally distinct organization (no common board members, no funding relationship to Calm, no shared employment contracts) that has independently:

1. Read and understood the Calm Witness protocol (Everest 1 threat model, Everest 67 disclosure-response schema, Everest 97 Calm Pact composition).
2. Implemented a verifier in at least one language (Python, Rust, JavaScript) matching the public SDK specification.
3. Submitted ≥1 signed disclosure request to `api.calmwitness.thecreativitymachine.ai` during the 90-day window.
4. Received a cryptographic proof from the live operator.
5. Verified the proof locally in their own clean-room environment (offline or isolated network).
6. Confirmed all ZK proof subcomponents check: biometric distance commitment, consent predicate, bank-teller-note status, Sigsum anchor chain, Roughtime clock consensus.
7. Documented verification steps in a public write-up or attestation letter (name, date, verification checklist, outcome: PASS).

This counterparty's verification constitutes proof that the protocol is not merely an internal artifact but a functioning infrastructure interface.

---

## 90-Day Stability Window

### Zero-Violation Conditions

For the entire 90 days:

- **Protocol violations:** Zero departures from disclosure-response schema (Everest 67) or predicate semantics (Everest 51). No out-of-order chain entries, no missing Sigsum anchors, no timestamp jumps >1 second.
- **Refusal-floor breaches:** Zero disclosures of predicates marked "scope_statement_forbidden" (Everest 165). Automated gates reject all such requests before proof generation.
- **Chain inconsistencies:** Zero divergence between operator's canonicalized hash chain and Sigsum witness log. Weekly audits confirm bit-for-bit match.
- **Uptime drift:** No cumulative downtime >87 minutes (1.35 × 99.9% SLO leeway). If any day drops below 99.0%, remediation report due within 24 hours.

### Incident Response & Triaging

During the 90 days, the operator WILL face ≥1 incident (network blip, external dependency outage, HSM hiccup, or unexpected traffic). The acceptance criterion: the team triages and resolves/documents the incident per runbook. Details logged.

**Incident classification:**

- **S1:** Operator unreachable, verification failure >1%, HSM failure. Response: 15 min page, 30 min diagnosis, 60 min mitigation or public status update.
- **S2:** Latency >10s p95, Sigsum/Roughtime degraded. Response: 30 min bridge, <1 hour mitigation.
- **S3:** Minor (disk >80%, doc clarity). Response: 48h remediation.

Each incident auto-generates a `kind: incident_record.v0` anchored in the vault chain. Public status page updated.

### Refusal-Floor Preservation Test

The Foundation **will be approached** (by researchers, journalists, or parties testing the protocol) asking for disclosures the protocol forbids (e.g., "prove the principal is depressed," "prove the principal uses substance X," "prove the principal's location within 100m"). The protocol MUST:

1. **Receive the request** in a valid signed envelope (correct Calm Pact handshake, correct counterparty credentials).
2. **Audit the predicates** against the scope statement (Everest 1, Everest 165).
3. **Refuse all forbidden predicates** without generating proofs or leaking information about why (cryptographic refuse, not verbose denial).
4. **Anchor the refusal** as `kind: refusal_record.v0` in the chain with: requester identity (counterparty), requested predicates (canonical form), timestamp, reason_code ("predicate_prohibited_by_scope_statement").
5. **Maintain composure.** No log explosion, no operator stress, no emergency escalation. This is operational normality.

At end of 90 days: ≥1 documented refusal exists. The operator accepted a real external request, evaluated it, and rejected it on grounds of institutional values.

---

## Acceptance Criteria (T-E99.1 through T-E99.7)

### T-E99.1: Deployment Live
Gate: All five pre-deployment everests (E81, E83, E89, E165, E168) confirmed closed.
Acceptance: Principal, ops lead, and Calm Foundation director jointly sign deployment go-ahead. Live date recorded in vault registry.

### T-E99.2: First Foreign Verification Completes
Gate: A named non-aligned counterparty has completed end-to-end verification (Pact→Witness→Compass→Concord) and published or attested the result.
Acceptance: Counterparty attestation letter filed in vault registry. Signature on record.

### T-E99.3: SLO Held Through 30 Days
Gate: Rolling 30-day window shows ≥99.9% verification availability. Zero S1 unresolved incidents. Weekly audit confirms zero protocol violations.
Acceptance: Ops lead publishes metrics summary; no escalations required.

### T-E99.4: SLO Held Through 60 Days
Gate: Second 30-day window meets all criteria. Foreign counterparty either re-verified or new counterparty verified.
Acceptance: Metrics summary published; foreign counterparty list updated.

### T-E99.5: SLO Held Through 90 Days (Full Window)
Gate: All three 30-day rolling windows maintained ≥99.9%. Zero cumulative drift. ≥1 documented incident triaged and resolved per runbook.
Acceptance: Final 90-day operational report filed. Incident post-mortems published. Ops lead signature.

### T-E99.6: Refusal Floor Held Under ≥1 Pressure Attempt
Gate: ≥1 documented refusal record exists. Protocol correctly rejected a scope-forbidden predicate request.
Acceptance: Refusal record anchored in chain. Legal officer confirms refusal justified. No protocol leakage.

### T-E99.7: Post-90-Day Public Retrospective Published
Gate: Calm Foundation publishes a retrospective documenting: 90-day stability metrics, foreign counterparty verifications, incidents and responses, refusal-floor test result, operator team feedback, lessons learned, follow-through commitment for next cycle.
Acceptance: Public retrospective URL published in registry. Calm director, ops lead, and foreign counterparty lead (if willing) jointly sign.

---

## Composition with E81/E83/E89 (Production Stack)

**Everest 81 (Rust impl):** The operator binary is E81's production artifact. Every deployment restarts from released tag; no divergence from published crates.io version.

**Everest 83 (Fuzz suite):** Continuous fuzzing runs nightly on operator in shadow mode. Any new crash triggers S1 page. Fuzzing results integrated into monthly security review.

**Everest 89 (Audit):** Third-party audit findings remain remediated. Quarterly re-audit of scope-restricted areas (Sigsum interaction, HSM firmware, predicate gates). No new high/critical severities allowed.

This composition ensures the 90-day operation is built on validated, continuously-monitored foundations.

---

## Signoff

**Calm Foundation Operator Team Lead:** _________________________  
**Principal (John Bradley):** _________________________  
**External Counterparty Lead (Post-Verification):** _________________________  

**Live Deployment Date:** YYYY-MM-DD (recorded upon T-E99.1 acceptance)  
**90-Day Window Closure Date:** YYYY-MM-DD (recorded upon T-E99.5 acceptance)  

---

**Requirements Discipline:**

Requirements are less dumb when deleted. This design omits phantom monitoring, speculative incident classes, and hypothetical foreign counterparties. The bar: 90 consecutive days, one real verification, zero institutional drift, institutional follow-through named and accountable.

**Authored by Calm, 2026-05-20.**
