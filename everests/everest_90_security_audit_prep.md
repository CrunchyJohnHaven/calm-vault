# Everest 90 — Third-Party Security Audit Prep

*Phase VII — Engineering Reliability. Prereq: Everest 81 (Rust Production Implementation), Everest 85 (CI with Adversarial Fuzzers).*

## Decision (v0)

**Calm Witness commissions a paid independent security audit from a top-tier cryptographic auditor (Trail of Bits, NCC Group, or equivalent) before Everest 91 (NIST Submission) is filed and before Everest 99 (First Production Deployment) carries any real principal's state. The audit packet is prepared, the vendor is selected, the engagement is funded, and the published audit report becomes a permanent reference artifact for downstream Everests (91, 92, 98, 100).**

The audit is not optional. Calm Witness's claim of cryptographic soundness depends on external validation. Internal review (Calm contributors, the DERB per Everest 80, the open-source community) is necessary but not sufficient — internal review cannot establish independence. External paid audit by an organization whose business is finding cryptographic bugs is the precondition for adoption beyond the Calm collective.

---

## Audit Packet Contents

The packet handed to the auditor at engagement start contains:

### 1. Scope Document (2-4 pages)

What the auditor is asked to evaluate, in priority order:

- **Cryptographic soundness** of the verifier circuit, the Pedersen commitment construction, the Σ-protocol composition with Fiat-Shamir, the threshold signature aggregation, the chain anchoring to Sigsum.
- **Side-channel resistance** of the operator-side prover and the counterparty-side verifier (timing, constant-time, memory-access patterns).
- **Implementation soundness** of the Rust reference crate against its specification (no overflow, no panic-on-untrusted-input, no buffer issues).
- **Hash-chain integrity** of the user_state.jsonl substrate; verification of the canonical-bytes computation; tamper-evidence properties.
- **Privacy properties** P1-P5 from the protocol spec — does the implementation actually preserve them?

What is OUT OF SCOPE:

- The biometric distance functions themselves (separate study — Everest 40/41)
- The behavioral interpretation of predicates (DERB territory — Everest 80)
- The Roughtime servers' or Sigsum operators' security (their infrastructure, not Calm Witness's)
- The principal's own device security (assumed trusted per threat model)

### 2. Specification Documents (consolidated, ~100 pages)

- [`ZKBB_USER_PROTOCOL_v0.md`](../ZKBB_USER_PROTOCOL_v0.md) — protocol spec
- [`NAMING_AND_BRANDING.md`](../NAMING_AND_BRANDING.md) — terminology
- [`ZKBB_USER_EVERESTS_100.md`](../ZKBB_USER_EVERESTS_100.md) — full route map
- Selected per-Everest design docs: E1, E26-28, E36-38, E41, E44-45, E51-58, E66-78
- [`USER_STATE_PROTOCOL.md`](../../../.calm-vault/USER_STATE_PROTOCOL.md) — substrate
- [`CALM_PACT_PROTOCOL_v0.md`](../CALM_PACT_PROTOCOL_v0.md) — sister primitive (composes with Calm Witness)

### 3. Reference Implementation Code Freeze

- Git tag of the `calm-witness` Rust crate at audit-start commit
- Build instructions: how to reproduce the audited binary bit-for-bit
- Source tree at the tagged commit (no further commits during audit window)
- `cargo audit` clean report at tag time
- Test suite passing (`cargo test --all-features`)

### 4. Threat Model

- Adversary catalogue from Everest 1 §2 (A1-A6) and Everest 41 (T1-T12 biometric)
- Privacy claims P1-P5 from Everest 1 §3
- Explicit out-of-scope: rubber-hose, enrollment-ceremony compromise, post-quantum (covered separately in E96)
- Explicit non-claims: no clinical assertions, no identity-of-strangers verification, no aggregate analytics

### 5. Dependency SBOM (Software Bill of Materials)

- Complete dependency tree (`cargo tree`)
- Per-dependency: version, license, last-update date, known-CVE status
- Flag any unmaintained or deprecated dependencies for auditor attention
- Pin policy: minimum supported versions; vendoring strategy for critical deps

### 6. Known-Issue List

- All open issues in the project's issue tracker, tagged with severity
- All previously-found-and-fixed bugs (commit references)
- All deliberate design decisions that an auditor might flag as concerning, with explicit rationale: *"We chose X because Y; here are the alternatives we rejected and why."*
- Internal review notes from prior Calm-side reviews (so the auditor knows what's been examined)

### 7. Cryptographic Construction Notes

- Curve choice: Curve25519 / Ed25519 / X25519 — why and how
- Pedersen generator selection — how `g` and `h` are generated such that `log_g(h)` is unknown
- Σ-protocol composition with Fiat-Shamir — exact transcript order and hash function
- Threshold aggregation — BLS12-381 vs. FROST choice and why
- Range proof construction — Bulletproofs on Ristretto255 per research memo
- Hash function choices — SHA-256 for chain integrity, Poseidon-friendly considerations for ZK circuits

### 8. Differential Testing Evidence

- Output of Everest 94's differential tests (multiple independent implementations cross-checked)
- Test corpus (Everest 64) — golden inputs and expected outputs
- Property-based test results (Everest 86, 87) — Hypothesis/proptest invariants

### 9. Fuzzing Evidence

- Adversarial fuzz results from Everest 85's nightly fuzzers
- 30+ days of clean runs prior to audit start (per route-map acceptance)
- Coverage report indicating fuzz target coverage of critical paths

### 10. Operational Notes

- Deployment topology (where the operator runs, where the verifier runs)
- Key management: master key custody, agent key issuance per Calm Vault patterns
- Logging and monitoring posture
- Incident response procedures
- The principal's audit interface (Everest 78 disclosure logging) — how the principal verifies their own chain post-incident

---

## Vendor Selection

**Top-tier auditors (in approximately equal-rank order):**

- **Trail of Bits** — strong in cryptographic protocol audits, ZK proofs, secure-enclave work. Past clients include cosmos / Tezos / Compound / Chia. Bid range: $120K-$250K for a 6-12 week engagement of this scope.
- **NCC Group** — global, deep in protocol-level cryptography; published audit reports on Signal, Whisper, WhatsApp. Slightly cheaper at the bottom end; comparable at top end.
- **Cure53** — Berlin-based; known for browser-side and web cryptography. Strong for the WASM verifier component (Everest 83). May lead the WASM portion if a multi-vendor approach is used.
- **Kudelski Security** — Swiss; strong in financial-grade cryptography. Less well-known in public open-source audits but very thorough.
- **Least Authority** — smaller; focuses on cryptocurrency and ZK protocols. May offer a competitive price for the ZK-circuit portion.
- **Quarkslab** — Paris-based; strong in low-level systems. Useful if hardware-attestation (E47) work is in audit scope.

**Selection criteria:**

1. **Public track record on cryptographic protocols** (not just smart contracts) — published audits of similar-shape work
2. **Familiarity with the specific primitives** (Bulletproofs, Pedersen, BLS, Σ-protocols) — auditor's prior reports demonstrate competence
3. **Capacity for a 6-12 week engagement window** in the v0 release timeframe
4. **Willingness to publish a redacted audit report** (full report internal, public summary or anonymized findings as a separate document)
5. **Independence**: no consulting or development relationship with Calm Witness contributors or affiliated organizations
6. **Cost**: within the Everest 90 budget envelope (~$200K target)

**Decision process:**

- RFP to 3-4 candidates with the audit packet attached
- 2-3 of them respond with proposals
- Selection committee: Calm contributor + DERB member (Everest 80) + independent cryptography advisor
- Decision documented and published

---

## Engagement Timeline

**Pre-audit (4-6 weeks before kickoff):**

- Audit packet assembled
- Vendor RFP sent and bids received
- Selection completed
- Statement of Work signed
- Code freeze on the reference implementation
- Auditor reviews packet, asks clarifying questions

**Audit (6-12 weeks):**

- Kickoff meeting (auditor + Calm contributors + DERB representative)
- Weekly status calls
- Auditor's questions answered via shared issue tracker (Calm contributors must NOT discuss specifics with auditor outside the SoW-defined channels — preserves auditor independence)
- Preliminary findings shared mid-engagement
- Final report drafted

**Post-audit (4-6 weeks):**

- Auditor's report received (full, internal)
- Calm contributors triage findings; prioritize remediation
- Bug fixes implemented and tested
- Auditor re-tests fixes (per SoW)
- Final public summary report drafted and published
- DERB reviews remediation completeness
- Chain-anchored `kind: "security_audit_completed"` record appended to user_state.jsonl

**Total elapsed:** 14-24 weeks from RFP to public report.

---

## What Gets Published

The audit produces two artifacts:

**Full audit report (internal):** Contains specific exploit details, code paths, potentially-leaky reproduction steps. Held in confidence between auditor and Calm contributors. Shared with DERB members under NDA.

**Public summary report (published):** A redacted version safe for public consumption. Contains:
- Audit scope, dates, vendor
- Summary of findings by severity (Critical / High / Medium / Low / Informational)
- Per-finding: description, recommendation, current status (fixed / mitigated / accepted / open)
- Overall verdict: ready for production / ready with caveats / not ready
- Vendor's signature

The public summary is signed by the auditor and anchored into the chain. The full report's sha256 is published; the report itself is held in escrow with the auditor.

---

## Pre-Audit Checklist (Must Be Complete Before Kickoff)

| Item | Owner | Status |
|---|---|---|
| Everest 81 — Rust production implementation feature-complete | Engineering | Pending |
| Everest 82 — Python reference implementation feature-complete | Engineering | Pending |
| Everest 83 — WASM/JS port for browser verifiers | Engineering | Pending |
| Everest 84 — SDK ergonomics polished | Engineering | Pending |
| Everest 85 — CI with adversarial fuzzers running clean for 30 days | Engineering | Pending |
| Everest 86, 87 — Property-based tests for chain + predicates | Engineering | Pending |
| Everest 88 — Performance budget met | Engineering | Pending |
| All `cargo audit` warnings resolved or accepted with documented rationale | Engineering | Pending |
| All known-issues triaged and documented | Engineering + DERB | Pending |
| All deliberate design choices documented with alternatives-considered | Engineering | Pending |
| Specification documents consolidated and reviewed for accuracy | Documentation | Pending |
| Threat model documented and ratified by DERB | Engineering + DERB | Pending |
| Dependency SBOM generated and reviewed | Engineering | Pending |
| Test corpus (Everest 64) frozen at audit-version | Engineering | Pending |
| Audit budget approved | Calm operations | Pending |
| Vendor selection completed | Calm operations + DERB | Pending |
| SoW signed | Legal | Pending |
| Code freeze announced and enforced | Engineering | Pending |
| Auditor onboarded and packet delivered | Calm operations | Pending |

No audit kickoff until every line in this checklist is green.

---

## Disclosure Policy

**Findings classified by severity:**

| Severity | Disclosure timing |
|---|---|
| Critical (live exploit, principal data at risk, signature forgeable) | Immediate disclosure to affected parties; fix-or-rollback within 24-72 hours |
| High (substantial weakening of privacy/integrity claim) | Disclosed in public summary on schedule; fixed before next release |
| Medium (could enable attack chain; no immediate exploit) | Disclosed in public summary; fixed in next minor release |
| Low (best-practice violation, no current exploit) | Disclosed in public summary; fixed at next opportunity |
| Informational (suggestion, code quality, ergonomics) | Disclosed; tracked as enhancement |

**Responsible-disclosure window:**

- The auditor's full findings are confidential for 90 days post-final-report
- During this window: Calm contributors fix the issues; affected counterparties (under NDA) are informed if needed for their own deployments
- After 90 days: full findings are publishable (or at least, all Critical and High findings)

This window aligns with industry-standard responsible-disclosure practice (Google Project Zero policy, etc.).

---

## Post-Audit Remediation

Each finding is tracked through:

1. **Triage** — confirmed reproducible, severity-assigned
2. **Fix implementation** — code changes
3. **Fix verification** — test cases prove the fix; CI is green
4. **Auditor re-test** — auditor confirms the fix per SoW (typically a 1-2 week re-test window)
5. **DERB review** — DERB approves remediation; the audit's overall verdict can be updated
6. **Chain anchor** — `kind: "audit_finding_remediated"` record appended with sha256 of the fix commit

If a finding cannot be fixed (architectural limitation, accepted residual risk), it is documented as such in the public summary with rationale.

---

## Cost

**Audit fee:** $120K - $250K, depending on vendor and scope.

**Code-freeze opportunity cost:** ~2-3 weeks of held development across all Calm Witness engineering. Real but absorbed.

**Calm-side coordination effort:** ~80 hours of senior engineer time (questions answered, clarifications provided, follow-ups). One engineer designated audit-liaison full-time during the engagement window.

**Remediation effort:** Variable. Budget 2-4 weeks of additional engineering for typical findings; up to 8 weeks if Critical findings emerge.

**Total cash budget for v0 audit:** ~$250K with buffer.

Funded from the Calm Witness operator's annual operations budget. Listed in the 2026/2027 budget approval cycle with the Creativity Machine LLC member-manager.

---

## What Could Go Wrong

| Risk | Mitigation |
|---|---|
| Critical finding emerges that requires substantial architecture change | Engagement is structured to surface architecture concerns early (preliminary findings mid-engagement); v0 release is paused if needed; not optional to ship past a Critical finding |
| Vendor capacity constraints delay the engagement window | Have 2-3 candidates lined up; willingness to use a non-first-choice vendor if the timeline matters |
| Audit cost exceeds budget | Renegotiate scope (e.g., audit Rust crate first, WASM port in a second engagement); raise additional funding if needed |
| Confidentiality breach (auditor accidentally leaks findings) | NDA with auditor; smaller risk because top-tier auditors have strong confidentiality records; insurance |
| Audit finds nothing significant — the protocol is actually solid | Acceptable but unlikely outcome; still publish the public summary as evidence of having sought external review |
| Follow-up audits needed (annual cadence) — ongoing cost | Budget annually; future audits should be cheaper because the auditor is familiar with the codebase |

---

## Coordination With Other Everests

- **Everest 1, 5, 26-28, 36-38, 41, 44-45, 51-58, 66-78:** Specification artifacts that constitute the audit packet
- **Everest 4 (License & IP):** Auditor's contract aligns with Apache 2.0 terms
- **Everest 40 (FAR/FRR):** Empirical evidence appendix in the audit packet
- **Everest 41 (Adversarial Robustness):** Threat model T1-T12 informs the audit's threat scope (though biometric distance functions themselves are out of audit scope per §1)
- **Everest 80 (DERB):** DERB reviews vendor selection, remediation completeness, public summary
- **Everest 81-89:** All must be substantially complete pre-audit
- **Everest 91 (NIST Submission):** Audit report attached as a key submission credibility artifact
- **Everest 92 (Open-Source Release):** Audit report published alongside the release
- **Everest 96 (Post-Quantum Migration):** Audit explicitly does NOT cover PQC primitives in v0; flagged for future audit
- **Everest 98 (Counterparty Implementer's Guide):** References the audit report so counterparty implementers know what's been verified
- **Everest 99 (First Production Deployment):** No production deployment before audit findings are resolved (Critical/High remediated)
- **Everest 100 (Third-Party Verification):** Independent verification builds on the audited foundation; the audit report is a precondition for credible third-party verification

---

## Annual Re-Audit

The first audit covers v0. Subsequent annual audits cover the deltas since the previous audit:

- **Year 2:** Smaller scope (focused on changes since v0); cheaper (~$80K-$150K); shorter engagement (4-6 weeks)
- **Year 3+:** Similar to Year 2; rotate vendors every 2-3 cycles to avoid auditor capture
- **On material change:** Any architectural change to the cryptographic stack triggers an unscheduled audit, regardless of annual cadence

The annual cadence aligns with Everest 40's annual FAR/FRR re-characterization and Everest 80's annual DERB report.

---

## Why This Matters

A protocol that ships without external security audit has a credibility ceiling. Counterparties evaluating whether to verify Calm Witness proofs ask: "Has anyone independent looked at the code?" If the answer is no, the answer about verification is also no. The audit is the precondition for the protocol leaving the Calm collective and operating in the broader world.

It is also the protocol's commitment to *operating honestly under scrutiny.* By committing to a paid third-party audit, with a published summary report, with chain-anchored evidence that the audit happened, Calm Witness binds itself to producing artifacts that an outside observer can use to check the protocol's claims. The audit is, in a small way, the protocol's first act of subjecting itself to checking by parties who are not Calm.

Finally, the audit is the structural antidote to a specific failure mode: the implementing team's blind spots. Every protocol team has them. The audit is the team paying for someone else to find them.

The cost — $200K-$250K + 14-24 weeks of calendar time — is real but bounded. It is the smallest fee for the largest credibility step Calm Witness can take in its v0 cycle.

— Calm, 2026-05-20
