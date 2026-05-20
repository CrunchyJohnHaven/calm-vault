# Everest 287 | Public Security Disclosure Policy

*Phase S-I | Cross-Protocol Governance. Stable ID: CS-07. Effort: S. Prereq: none. Composes with: Everest 92 (trademark enforcement), Everest 4 (Apache-2.0 license + patent non-aggression), CALM_REFUSAL_FLOOR_INDEX.md (§1-§4), CALM_WITNESS_SCOPE_STATEMENT.md (use-case forfeit list), bug-hunt-to-report-loop.mdc (reporter intake + credit routing).*

## The Decision (v0)

**The Calm Stack (comprising the four pillar crates, Concord, reference verifiers, and foundation infrastructure) will accept security vulnerability reports via a published channel, triage reports into four severity tiers, apply a 90-day default embargo from triage date, accelerate embargo to 7 days for in-the-wild exploitation, offer reporter credit by consent, decline monetary bounties during v0 (Foundation treasury not yet established), substitute gift acknowledgement aligned with the project's security-first ethos, refuse to test external infrastructure without written authorization, delete reporter artifacts within 30 days of disclosure, coordinate CVE issuance through a CVE Numbering Authority partnership, and escalate to the multi-maintainer quorum any vulnerability whose fix would require loosening the refusal floor (CALM_REFUSAL_FLOOR_INDEX.md §1-§3).**

This policy codifies the security intake, triage, and disclosure pipeline as a structural commitment: not a convenience layer, but a load-bearing part of the public-good claim the Calm Stack makes.

---

## §1 — Scope

### §1.1 — Covered Surface

This policy applies to security vulnerabilities in:

1. **Pillar crates**: all four canonical protocol implementations (Witness, Pact, Compass, Concord) as versioned in the public registry.
2. **Foundation infrastructure**: Calm Stack verifier reference implementations, the official wire-format codecs, the predicate registry and its type checker, the ethics review board process documentation.
3. **Coordinated counterparty infrastructure**: the published CredexAI operator VC root, the public-registry agent DIDs, the Sigsum and Roughtime anchors, the attestation-chain anchors.
4. **Cryptographic primitives**: Ristretto255 bindings, Bulletproof verification, Schnorr proof verification, and hash-chain freshness checks used in any of the above.

**Out of scope** (handled by operators, not by this policy):

- Vulnerabilities in private operator deployments or local vault implementations (operator security responsibility).
- Social-engineering attacks not exploiting a cryptographic or protocol flaw.
- Configuration mistakes (e.g., a deployed verifier running with debugging enabled); reported to the operator, not escalated to Calm.

### §1.2 — Covered Vulnerability Classes

Security vulnerabilities covered by this policy:

1. **Cryptographic flaws**: incorrect proof verification, protocol state-machine errors, nonce reuse, timing attacks, side-channel leakage.
2. **Implementation bugs**: memory unsafety, buffer overflows, integer overflow, logic errors in state transitions.
3. **Protocol ambiguities**: specification errors that could cause interoperability failures, divergent behavior across implementations, or silent disagreements on freshness/replay.
4. **Refusal-floor violations**: a code path that could admit a forbidden predicate category, emit a forbidden output shape, or enable a forbidden use case (cf. CALM_REFUSAL_FLOOR_INDEX.md §1-§3).
5. **Disclosure mechanics failures**: confidentiality or integrity breaks in the reporter intake channel, consent record leakage, audit-log poisoning.

---

## §2 — Reporter Intake Channel

### §2.1 — Primary Channel

Security vulnerability reports MUST be sent to:

**`security@<calm-domain>`** (exact domain TBD; use the canonical domain listed in `STACK_GOVERNANCE_20.md` at policy release time).

All reports sent to this address are received by the designated security team (initially: the Calm operator + one external reviewer, rotating quarterly).

### §2.2 — PGP Encryption

The Foundation publishes a PGP public key at `/.well-known/security.txt` (RFC 9116) and on the public verifier registry. Reporters MAY encrypt reports with this key; reporters SHOULD encrypt when reporting on behalf of an organization.

**Key rotation**: The Foundation rotates the PGP key annually and publishes 60-day advance notice. Prior keys are retained for 12 months after rotation to allow deferred reports sent using cached keys to be decrypted.

### §2.3 — Intake SLA

The security team acknowledges receipt of a report within:

- **10 minutes** during active windows (defined as 09:00-20:00 UTC, Monday-Friday; on-call duty rotates weekly).
- **24 hours** outside active windows.

Acknowledgement is a brief automated response confirming receipt and providing a reference number. No triage decision is included in the acknowledgement.

---

## §3 — Triage and Severity Classification

### §3.1 — Triage Classification

All reports are triaged into one of four severity tiers:

1. **Critical**: The vulnerability allows unauthorized disclosure of principal state, forging proofs, defeating cryptographic bindings, or enabling a refusal-floor category violation. Patch required immediately; embargo accelerated (see §4.2).
2. **High**: The vulnerability impacts availability, operator security, or the precision of proof verification under specific (reproducible) conditions. Patch required within 30 days; standard 90-day embargo applies.
3. **Medium**: The vulnerability is a logic error, inefficiency, or edge case that does not undermine core security but should be fixed in the next release. Standard 90-day embargo; patch timeline negotiable.
4. **Low**: The vulnerability is a documentation issue, a non-critical configuration recommendation, or a potential issue that does not affect deployed code. No embargo; may be published in a public advisory immediately with the reporter's consent.

### §3.2 — Triage SLA

Triage classification is completed and communicated to the reporter within:

- **48 hours** for Critical reports.
- **7 days** for High reports.
- **14 days** for Medium and Low reports.

If triage requires clarification from the reporter (e.g., a detailed PoC), the SLA clock resets after clarification is provided.

### §3.3 — Ambiguous or Boundary Cases

If a report falls between two severity tiers, the security team escalates to the multi-maintainer quorum (see §6). The reporter is notified of the escalation and the expected timeline for a decision (5 additional business days).

---

## §4 — Embargo and Disclosure Timeline

### §4.1 — Default Embargo: 90 Days

For all triaged vulnerabilities (Critical, High, Medium), the embargo period is **90 days from the triage date**. The reporter agrees not to disclose details, proof-of-concept code, or exploitation techniques until:

1. A patch is available in the public repository, AND
2. The 90-day period has elapsed, OR
3. The Foundation releases a public advisory explicitly permitting earlier disclosure.

At the close of the embargo period, the Foundation publishes a security advisory (see §4.4) and the vulnerability is considered public.

### §4.2 — Accelerated Embargo: In-the-Wild Exploitation

If the security team becomes aware that the vulnerability is being actively exploited in the wild (through public disclosures, CVE databases, or operational reports from verifier operators), the embargo is **accelerated to 7 days** from the date of in-the-wild confirmation.

**Immediate action**: Upon confirmation of in-the-wild exploitation, the Foundation MUST:
- Notify all registered verifier operators and counterparties within 24 hours.
- Publish a public emergency advisory naming the vulnerability, the affected versions, and the temporary mitigation.
- Provide a hotfix release or workaround.

The 7-day clock then runs for full public disclosure (patch + advisory).

### §4.3 — Reporter Request for Extension or Acceleration

A reporter MAY request:

1. **Embargo extension** (up to 180 days total) if additional time is needed for patch development or coordination. The request must include a technical justification. The security team has discretion to grant, with priority given to cross-organization coordination scenarios.
2. **Embargo acceleration** if the reporter has coordinated a patch with a downstreaming organization and wishes to ship simultaneously. Requests must be specific (e.g., "coordinated with Organization X; they deploy on date Y"). The security team approves if all parties agree.

All extension/acceleration requests are logged and included in the final advisory.

---

## §4.4 — Public Advisory Format

At embargo end (or upon acceleration), the Foundation publishes a security advisory containing:

1. **Vulnerability summary**: a one-sentence description accessible to non-experts.
2. **Affected versions**: semver range(s) of affected pillar crates, reference implementations, or coordinated infrastructure.
3. **Severity classification**: the CVSS v3.1 base score (if applicable; for protocol issues, a narrative severity assessment).
4. **Impact summary**: what an attacker can do; who is affected; is the impact confirmed in production deployments.
5. **Technical details**: sufficient detail for a downstream integrator to assess patch necessity, without being a step-by-step exploitation tutorial.
6. **Remediation**: specific version(s) to upgrade to; workarounds if available; deployment guidance.
7. **Timeline**: triage date, embargo period, in-the-wild detection date (if applicable), patch availability date, disclosure date.
8. **Credits**: reporter name (if the reporter consented) and any organizations that coordinated the response.
9. **CVE identifier**: the assigned CVE number (see §7).

---

## §5 — Reporter Credit

### §5.1 — Opt-In Credit Policy

Upon triage, the reporter is offered three credit options:

1. **Named credit**: "Security advisory prepared in coordination with [Reporter Name]" in the public advisory.
2. **Organization credit**: "[Organization Name] Security Team" (for reporters submitting on behalf of an employer).
3. **Anonymous**: no credit line; the advisory notes "reported by a third party."

The choice is made at triage time and is binding for that disclosure. The reporter may opt for a different choice for future reports.

### §5.2 — No Monetary Bounty (v0)

**The Calm Foundation does not offer monetary bounties during v0.** The Foundation's treasury is not yet established, and the project's governance model does not support bounty programs until the Phase VIII public-good declaration (Everest 298).

### §5.3 — Gift Acknowledgement (Aligned with Project Ethos)

Instead of monetary bounty, reporters whose vulnerability is triaged as Critical or High are offered:

1. **Lifetime perpetual license** to use any artifact of the Calm Stack under the Apache-2.0 license, with no attribution requirement (the license itself is the gift; no additional consideration).
2. **Public recognition** in a "Security Contributors" section of the canonical repository README, with the option to include a GitHub profile link or personal website URL.
3. **Advance copy** of all future security advisories for 12 months (acting as a preview reviewers if they wish).
4. **Invitation to join the annual security workshop** hosted by the Foundation (travel/accommodation covered if feasible).

The second and third options are contingent on the reporter's consent and require no additional consideration.

---

## §6 — Refusal-Floor Escalation Gate

### §6.1 — The Escalation Trigger

If the security team identifies that a proposed patch for any Critical or High vulnerability would require **loosening, narrowing, or reinterpreting any part of CALM_REFUSAL_FLOOR_INDEX.md §1-§3**, the vulnerability is immediately escalated to the **multi-maintainer quorum** (per CALM_REFUSAL_FLOOR_INDEX.md §8). This includes:

- The canonical Calm operator.
- At least one external reviewer (rotating, maintained by the Foundation).
- The ethics review board (3-person panel, per ZKAC_TYPE_SYSTEM_v0).

### §6.2 — Escalation Timeline

Upon escalation:

1. **Day 1**: The quorum is notified; the reporter is informed that escalation occurred (without revealing the specific quorum members or their identities).
2. **Days 1-5**: The quorum reviews the proposed patch, the refusal-floor tension, and any alternative approaches that do not weaken the floor.
3. **Day 5**: The quorum publishes a written decision (private to the reporter and the security team; may be made public if the decision has precedent value).

If the quorum concludes that the patch would require loosening the floor, the vulnerability is **NOT patched** by the Calm Stack. Instead:

- A detailed refusal note is published in the advisory (e.g., "this vulnerability cannot be patched without weakening the refusal-floor commitment; see the detailed reasoning here").
- The Foundation coordinates with downstreaming organizations on workarounds or local patches.
- The finding is logged as a precedent for future governance decisions.

### §6.3 — Rationale

The refusal floor is the most valuable property of the Calm Stack. A patch that undermines it is worse than the vulnerability. This gate ensures that governance decisions about the floor are made by quorum, not by a single maintainer or by the urgency of a patch timeline.

---

## §7 — CVE Issuance

### §7.1 — CVE Numbering Authority Partnership

The Foundation partners with an official CVE Numbering Authority (CNA) to issue CVE identifiers for all triaged Critical and High vulnerabilities that:

1. Are publicly disclosed (embargo ended or accelerated), AND
2. Have a clear attack surface and demonstrable impact (e.g., "unauthorized proof forgery" or "biometric distance disclosure").

### §7.2 — CVE Timeline

The CVE is requested from the CNA partner on the public disclosure date (or within 24 hours thereafter). The CVE number is included in all public advisories retroactively if necessary.

### §7.3 — No CVE for Low/Medium

Low and Medium vulnerabilities are not assigned CVE numbers unless they have cross-organization impact or affect widely deployed derivatives. The advisory notes whether a CVE is in scope.

---

## §8 — Forbidden Testing

### §8.1 — Authorization Requirement

**The security team MUST NOT engage in active security testing of any external infrastructure, service, system, or organization without explicit written authorization from that organization.** This includes:

- Penetration testing of verifier operators' infrastructure.
- Fuzzing or scanning of any external API or service.
- Attempting to trigger the vulnerability on a live deployment.

**Exception**: The security team MAY test the vulnerability on infrastructure owned by the Calm Foundation or on the reporter's systems, with the reporter's prior consent.

### §8.2 — Reporter PoC Handling

If a reporter submits a proof-of-concept (PoC) that could be used to exploit live systems, the security team:

1. Reviews the PoC locally, in an isolated environment.
2. Does NOT run the PoC against any external system or operator deployment.
3. Documents the PoC's effectiveness internally (for patch validation) but does not retain the PoC itself in the repository or in long-term storage.

---

## §9 — Data Handling and Deletion

### §9.1 — Reporter PII and Artifacts

Any personally identifiable information (PII) provided by the reporter during intake (email, organization, contact details) or embedded in the PoC/technical artifacts is:

1. Stored securely (encrypted at rest, access-limited to the security team and the multi-maintainer quorum).
2. Used solely for the purpose of coordinating disclosure and crediting the reporter.
3. **Deleted within 30 days of the embargo end date** or the public disclosure date, whichever is later.

### §9.2 — PoC Artifacts and Patches

Proof-of-concept code, preliminary patches, and technical notes prepared during triage are:

1. Retained during the embargo period for patch development and coordination.
2. Deleted within 7 days of the embargo end (or the public disclosure date).

Exception: If the PoC or patch is of academic or technical interest and the reporter has given explicit consent in writing, a redacted version (with reporter PII and sensitive details removed) may be retained for 12 months as a case study. The retention period and use are disclosed to the reporter.

### §9.3 — Audit Log

An audit log recording the date, severity, reporter, embargo period, and disclosure outcome for each vulnerability is retained indefinitely (for governance and transparency purposes) but does not include PoC details, technical artifacts, or reporter PII.

---

## §10 — Operator Notification and Coordination

### §10.1 — Verifier Operator Notification

If a Critical vulnerability is confirmed, the Foundation notifies all registered verifier operators (via a private channel) at least **7 days before** public disclosure, providing:

1. A technical summary of the vulnerability and the patch.
2. A timeline for when the patch will be available.
3. Guidance on fallback or temporary mitigation during the patch deployment window.

### §10.2 — Coordination with Downstreaming Organizations

If the Foundation is aware that another organization has forked or vendored the Calm Stack code, the security team attempts to coordinate disclosure with that organization, offering them advance notice and a shared embargo period (if feasible).

---

## §11 — Failure Modes and Out-of-Band Disclosure

### §11.1 — Public Disclosure Before Embargo Ends

If a vulnerability is publicly disclosed before the embargo period ends (e.g., a reporter goes public, or a researcher publishes), the Foundation:

1. Immediately publishes its own advisory (with or without a final patch), clearly marking it as "disclosure accelerated."
2. Provides temporary guidance to verifier operators on mitigation or rollback.
3. Assesses whether the disclosure constitutes "in-the-wild exploitation" (triggering the 7-day accelerated timeline per §4.2).

### §11.2 — Reporter Breach of Embargo

If a reporter discloses details before the embargo ends (without Foundation permission), the Foundation:

1. Documents the breach and dates.
2. Publishes its advisory immediately under "emergency disclosure" framing.
3. Logs the breach in the audit trail but does not pursue legal action unless the breach materially harms the Foundation or a verifier operator (threshold: demonstrable loss or security incident traceable to the breach).

### §11.3 — Discovered During Policy Enforcement

If the security team discovers that a previously disclosed vulnerability was not reported through this channel (e.g., a GitHub issue containing exploit details), the team:

1. Files a report on the original discoverer (if identifiable), acknowledging their discovery.
2. Credits them under the acknowledgement procedures in §5 if they can be reached and provide consent.
3. Applies retroactive embargo periods and disclosure dates as if the report had been received on the date of the public discovery.

---

## §12 — Interactions with CALM_REFUSAL_FLOOR_INDEX.md

### §12.1 — Alignment with §1-§4

This policy honors CALM_REFUSAL_FLOOR_INDEX.md §1-§4 as the canonical reference:

1. **§1 (predicate refusal)**: No predicate vulnerability is accepted as "acceptable risk." Any predicate that admits a forbidden category is treated as Critical.
2. **§2 (output-shape refusal)**: Any vulnerability allowing forbidden shapes (numeric scores, cardinality reveals, etc.) is Critical.
3. **§3 (use-case refusal)**: If a vulnerability enables a forbidden use case listed in CALM_WITNESS_SCOPE_STATEMENT.md §2, it is escalated immediately (per §6).
4. **§4 (operator-behavior refusal)**: If a proposed patch would require an operator to violate §4 commitments (e.g., pathologizing a principal's ideation), the escalation gate (§6) is triggered.

### §12.2 — No Weakening Without Quorum

As per CALM_REFUSAL_FLOOR_INDEX.md §3's one-way ratchet, this policy ensures that no vulnerability patch loosens the refusal floor. The escalation gate (§6) is the structural enforcement.

---

## §13 — Scope Limitations (Out of Scope)

The following are NOT covered by this policy:

1. **Vulnerabilities in third-party dependencies**: reported to the dependency maintainer; the Calm Stack publishes an advisory if the dependency is widely used.
2. **Deployment misconfigurations**: reported to the operator; Calm publishes hardening guidance if patterns emerge.
3. **Social engineering or policy abuse**: not a security vulnerability; reported to the relevant organizational authority.
4. **Performance, usability, or design concerns**: not security issues; may be tracked as enhancements in the public issue tracker.

---

## §14 — Policy Evolution and Versioning

### §14.1 — Policy Version

This policy is **v0 (2026-05-20)**. 

### §14.2 — Policy Updates

Changes to this policy require:

1. A 30-day public comment period (issue filed in the public repository).
2. Approval by the canonical Calm operator + at least one external reviewer.
3. A 7-day deployment grace period before the new version takes effect.

Urgent changes (e.g., to the refusal-floor escalation gate in response to a governance finding) may bypass the comment period but require quorum sign-off and public notification within 24 hours.

### §14.3 — Backwards Compatibility

This policy applies to all vulnerabilities reported after its effective date (2026-05-20). Vulnerabilities reported prior are handled under the previously published guidance (if any) or under good-faith discretion if no prior guidance existed.

---

## §15 — Closing

Security is foundational to the Calm Stack's claim to be a public good. A protocol without a refusal floor is a weapon; a protocol with a refusal floor but no security commitment is a promise waiting to fail. This policy is the commitment: we will listen, we will triage fairly, we will patch diligently, and we will never sacrifice the refusal floor for convenience.

Reporters are trusted as partners in that commitment. The 90-day embargo balances their safety with the public's right to know. The refusal-floor gate ensures that we do not patch our way into compromising our own values. The 10-minute acknowledgement SLA and the public audit trail are the evidence that this is not theater.

The policy is published at `security@<calm-domain>`, pinned in the canonical repository's `SECURITY.md`, and signed by the canonical Calm operator and the external reviewer.

---

**This policy honors and defers to CALM_REFUSAL_FLOOR_INDEX.md §1-§4 as the normative reference. In any conflict between this policy and that index, the index wins.**

— Calm, 2026-05-20
