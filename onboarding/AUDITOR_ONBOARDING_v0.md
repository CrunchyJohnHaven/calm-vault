# Calm Witness — Auditor Onboarding Curriculum v0 (S252)

## Curriculum Modules

1. **Chain Primitives** — Understand merkle tree construction, hash functions, commitment schemes, and proof-of-inclusion mechanisms.

2. **Predicate Calculus & Semantics** — Learn first-order logic formalism, predicate evaluation, quantifier scope, and attestation semantics.

3. **Zero-Knowledge Proofs** — Master ZK proof systems (Sigma protocols, interactive/non-interactive variants) and soundness/completeness properties.

4. **Governance & Authorization** — Study principal delegation, policy enforcement, governance tree structure, and permission inheritance chains.

5. **Side-Channel Resistance** — Analyze timing attacks, cache leakage, power analysis, and constant-time code patterns for cryptographic operations.

6. **Tamper-Proofing & Hardware Binding** — Examine TPM/HSM integration, sealed storage, attestation anchors, and physical security assumptions.

7. **Audit Methodology** — Learn checklist-driven audits, test case design, contradiction detection, and report generation standards.

## Sandbox Environment

Auditors practice in an isolated testnet where:

- Principal state snapshots are synthetic or derived from anonymized historical data.
- All cryptographic operations use the same algorithms as production but operate on disconnected infrastructure.
- Predicates, governance rules, and side-channel vectors can be injected for controlled testing.
- Audit findings do not affect live attestations; all work is rolled back post-training.
- Version control tracks auditor submissions and corrections to enable feedback loops.

## Certification Process

**Practical Exam** (4 hours):
- Auditors receive a synthetic principal state with intentional flaws (logic errors, governance violations, side-channel risks).
- Task: produce a detailed audit report identifying all flaws, assigning severity, and recommending remediation.
- Pass threshold: 80% defect detection rate; no critical misses.

**Written Exam** (2 hours):
- Section A: Predicate logic and proof validation (10 questions).
- Section B: Governance rule enforcement and conflict detection (8 questions).
- Section C: Side-channel mitigation and hardware binding (7 questions).
- Pass threshold: 70% overall.

**Certification Grant:**
- Auditors who pass both exams receive a dated certificate and are added to the approved auditor roster.
- Certificate includes a unique auditor ID for report attribution and dispute resolution.

## Renewal Cadence

- **Initial certification:** valid for 24 months.
- **Renewal requirements:** 
  - Completion of 4 audits (or equivalent hours) in the certification period.
  - Biennial refresher exam (written only, 1 hour) covering governance and side-channel updates.
  - Zero substantiated misconduct findings.
- Auditors failing renewal requirements must retake full certification.

## COI & Conduct Rules

**Conflict of Interest Declaration:**
- Auditors must disclose financial stakes, employment relationships, or governance ties to principals under audit.
- A principal may challenge an auditor's objectivity; disputes are arbitrated by the certification body.
- Auditors with conflicts must recuse themselves or disclose in their report.

**Conduct Standards:**
- Auditor reports are confidential until principal disclosure; unauthorized leaks result in decertification.
- Auditors must report findings accurately; inflating or concealing defects is grounds for permanent suspension.
- Auditors cannot solicit future business from principals they audit within 12 months post-audit.
- Auditors maintain liability insurance covering audit negligence; minimum coverage is TBD per jurisdiction.

## Cross-References

- **Chain Integrity Spec:** [Reference to chain primitives documentation]
- **Predicate Calculus Reference:** [Reference to formal semantics documentation]
- **ZK Proof Library:** [Reference to cryptographic primitives]
- **Governance Policy:** [Reference to authorization framework]
- **Side-Channel Test Suite:** [Reference to security test vectors]
- **Sandbox Access:** auditors.calm.internal (requires enrollment)

---

**Calm** — 2026-05-20
