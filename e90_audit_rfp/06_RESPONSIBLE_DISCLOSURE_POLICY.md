# Responsible Disclosure Policy — Calm Witness v0 Audit

*Auditors accept this policy as a condition of the engagement, by reference in the Statement of Work. Counterparties and downstream implementers of Calm Witness are encouraged to adopt aligned policies for findings they identify in their own deployments.*

This policy governs how findings from the Calm Witness third-party security audit (Everest 90), and any related security disclosures, are handled. The policy aligns with industry-standard responsible-disclosure practice (Google Project Zero, CERT/CC) and integrates with Calm's internal review processes (Everest 80 DERB).

---

## 1. Finding Severity Classification

All findings shall be classified at the time of discovery, with severity confirmed jointly by the auditor and Calm's audit-liaison within 5 business days of disclosure to Calm. The DERB has consultative input on classification disputes.

| Severity | Definition | Examples |
|---|---|---|
| **Critical** | Live exploit feasible; principal data at risk; signature or proof forgeable; arbitrary code execution against verifier or operator from untrusted input. | Soundness break in the Σ-protocol composition. A Pedersen-commitment binding-property violation. Forgery of a chain-anchored witness statement. |
| **High** | Substantial weakening of a core privacy or integrity claim. No immediate live exploit, but a credible attack chain exists. | Side-channel leak revealing committed value over many queries. Hash-chain tamper-evidence weakening under adversarial input. P1–P5 privacy property weakened in realistic adversary model. |
| **Medium** | Could enable an attack chain in combination with other findings; no current standalone exploit. | Constant-time violation in a path the adversary controls only weakly. Input validation gap in a path with multiple defenses. SBOM dependency CVE without an exploit path. |
| **Low** | Best-practice violation; no current exploit; potential for future relevance. | Suboptimal error messages leaking minor information. Outdated dependency without a known exploit path. Minor code-quality issue in a security-critical file. |
| **Informational** | Suggestion, recommendation, code quality, ergonomics. No security impact. | Recommendation to improve documentation. Suggestion for additional test coverage. Style note. |

## 2. Disclosure Timing

### 2.1 Critical Findings

- **Auditor discloses to Calm within 24 hours** of discovery, regardless of normal weekly reporting cadence. Channel: encrypted email plus follow-up call with the audit-liaison.
- **Calm initiates fix-or-rollback within 24–72 hours** of confirmed classification. If a deployed system is affected, Calm notifies counterparties under NDA so they can pause use or apply mitigation.
- **Public disclosure**: included in the public summary report on the standard schedule (after the 90-day window), unless Calm and the auditor jointly determine earlier public disclosure is necessary to protect users of the protocol. Calm prefers the standard schedule.

### 2.2 High, Medium, Low Findings

- Disclosed to Calm via the normal weekly status cadence or in the preliminary findings deliverable.
- Calm triages and assigns a fix target: next release (High), next minor release (Medium), next opportunity (Low).
- Disclosed in the public summary report on the standard schedule.

### 2.3 Informational Findings

- Disclosed via the normal weekly cadence.
- Tracked as enhancement requests in the Calm issue tracker.
- Disclosed in the public summary report's appendix.

## 3. Responsible-Disclosure Window

- The auditor's full findings, including reproduction steps and exploit details, are **confidential for 90 days** from the date of final report acceptance (SoW deliverable D4).
- During the 90-day window:
  - Calm contributors implement fixes.
  - Affected counterparties (if any have deployed pre-v0 builds under NDA) are informed of relevant findings so they can apply mitigations or pause use.
  - The auditor and Calm do not discuss specifics with third parties beyond the above.
- **After 90 days**, Calm publishes the public summary report (per SoW D5/D7). The public summary contains all findings at all severities, with reproduction steps redacted or omitted for any finding where full disclosure would create residual risk.
- **Full report publication**: At Calm's discretion, the full report may be published after the 90-day window. Calm prefers not to publish full reports for findings where redaction is needed to protect deployed systems, but the choice is Calm's.

The 90-day window may be extended by mutual agreement of Calm and the auditor if remediation is incomplete (e.g., architectural change required). Extensions are documented in writing and disclosed in the public summary.

## 4. Public Summary Report

The public summary report (SoW deliverables D5 and D7) is signed by the auditor and published by Calm. It contains:

- Audit scope, dates, vendor identity.
- Summary of findings by severity (counts and brief description per finding).
- Per-finding: title, severity, summary description, recommended remediation, current status (fixed / mitigated / accepted-residual-risk / open).
- Overall verdict: one of **ready for production**, **ready with caveats**, **not ready**, with brief rationale.
- Vendor's signature.

The public summary omits reproduction steps and exploit details where their inclusion would weaken defenses. The auditor and Calm jointly determine redaction scope; defaults favor security over disclosure granularity.

**Chain anchoring**: The sha256 of the published public summary is recorded in a `kind: "security_audit_completed"` entry appended to the canonical `user_state.jsonl` chain. The sha256 of the full internal report is also recorded (without releasing the report itself) so its integrity is verifiable when eventually published.

## 5. Coordination With DERB (Everest 80)

The DERB reviews:

- Severity classification disputes, on referral from the audit-liaison.
- Remediation completeness, before the post-remediation public summary (D7) is published. DERB confirms that fixes resolve the original findings and that no architectural concerns remain.
- Accepted-residual-risk findings — DERB ratifies any finding Calm elects not to remediate and approves the rationale documented in the public summary.

DERB members are bound by the same NDA as audit participants for full-report content during the 90-day window.

## 6. Post-Audit Remediation Workflow

Each finding moves through:

1. **Triage** — confirm reproducibility; assign final severity.
2. **Fix implementation** — code changes; PR linked to finding ID.
3. **Fix verification** — Calm-side test cases prove the fix; CI green.
4. **Auditor re-test** (per SoW D6) — auditor confirms the fix; written per-finding confirmation provided.
5. **DERB review** — DERB ratifies remediation completeness for High and Critical findings.
6. **Chain anchor** — `kind: "audit_finding_remediated"` entry appended with sha256 of fix commit.

If a finding cannot be fully fixed (architectural limitation, accepted residual risk), it is documented in the public summary with explicit rationale, DERB ratification, and a future-work entry on the route map.

## 7. Out-of-Band Findings

If anyone outside the engagement (researchers, users, counterparties) discovers a Calm Witness security issue, they may disclose to:

- **Primary channel**: encrypted email to `security@calm-witness.example` *(channel published with the open-source release)*.
- **Backup channel**: GitHub security advisory in the `calm-witness` repository.

Calm acknowledges receipt within 5 business days, assigns severity per this policy, and follows the same 90-day responsible-disclosure window. Discoverers are credited in the public summary (or the next regular release notes) unless they request anonymity.

Calm does not currently operate a paid bug-bounty program. This may change post-v0. Discoverers acting in good faith are protected under Calm's safe-harbor commitment: Calm will not pursue legal action against researchers who follow this policy.

## 8. Auditor's Acceptance

By signing the Statement of Work, the auditor accepts this policy and agrees to:

- Classify findings per Section 1.
- Disclose per the timing in Section 2.
- Honor the 90-day confidentiality window per Section 3.
- Sign and consent to publication of the public summary per Section 4.
- Cooperate with DERB review per Section 5.
- Re-test remediated findings per Section 6.

---

— Calm, 2026-05-20
