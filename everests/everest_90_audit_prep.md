# Everest 90 — Third-Party Security Audit Prep

*Phase VII — Engineering Reliability. Prereq: Everest 81, 85.*

---

## Acceptance

An audit-ready packet is prepared and stored in `/calm_witness_audit/`, containing all material needed for a third-party security review. The packet includes threat model, protocol specification, reference implementation at a frozen commit, complete dependency SBOM, prior-bug catalogue, security-relevant changelog, cryptographic proof sketches, CI artifacts (fuzzer reports, property tests), an audit RFP, and a briefing-call agenda. Audit firm candidates (Trail of Bits, NCC Group, Cure53) have received the packet and timeline. Scope, budget, and timeline are locked.

---

## Contents of the Audit Packet

### 1. Threat Model (Consolidated)

A single consolidated document synthesizing threat analysis from Everests 1, 9, 21, and 41. Covers six actor roles (Principal, Calm operator, vault, counterparty operator, verifier infrastructure, adversaries), explicit trust assumptions, and a ranked table of 30 failure modes (F01–F30) with severity, detection, and response per row. Maps each failure to the Everest that mitigates it. Explicitly scopes what the protocol does and does not defend against — coercion of the principal is out-of-scope; cryptographic soundness under nation-state attacks (Everest 96) is deferred. The threat model is the lens through which auditors will evaluate every design decision.

Location: `/calm_witness_audit/threat_model_consolidated.md` (sourced from E1, E9, E21, E41).

### 2. Protocol Specification

The full Calm Witness specification locked at the version under audit. Includes the current draft of `ZKBB_USER_PROTOCOL_v0.md` and all relevant everest specifications (E26, E28, E36–E37, E45–E46, E51–E65). Specifically includes:
- Schema specifications (chain format, predicate vocabulary, consent calculus axioms).
- Cryptographic primitives (Pedersen commitments on Ristretto255, Σ-protocol range proofs, Bulletproofs soundness claims).
- Disclosure flow (selective disclosure, replay defense, nonce binding).
- Enrollment and template-management procedures.

All specs are versioned and immutable for the audit period.

Location: `/calm_witness_audit/protocol_specification_v0.1.md` (consolidated from ZKBB_USER_PROTOCOL_v0.md + everests E26, E28, E36–E37, E45–E46, E51–E65).

### 3. Reference Implementation (Code Freeze)

The Rust `calm-witness-rs` crate at a tagged commit, read-only, pinned to the audit period. Includes:
- Core modules: chain verification, biometric-distance functions, Pedersen commitments, Σ-protocol proof generation.
- Predicate evaluators for all six v0 predicates (in_baseline_24h, biometric_match_within, principal_consents_to_disclose, bank_teller_note_active, cognitively_atypical_baseline, mental_state_unusual).
- Disclosure envelope construction and verification.
- Dependency pinning (no transitive updates during audit).

Frozen commit hash recorded in audit packet metadata.

Location: `~/CredexAI/calm_witness/` (Rust crate) at commit `[FROZEN_HASH]`; snapshot copy in `/calm_witness_audit/calm_witness_rs_v[VERSION].tar.gz`.

### 4. Dependency Software Bill of Materials (SBOM)

A complete inventory of all direct and transitive dependencies, with version pins, licensing information, and security advisories. Generated via `cargo tree --depth=unlimited` and enriched with CVSS scores from public vulnerability databases. Includes:
- Cryptography libraries: `ristretto255` (fork of curve25519-dalek), `sha2`, `chacha20poly1305`.
- Serialization: `serde`, `serde_json`, `bincode`.
- Development: `proptest`, `cargo-fuzz`, sanitizer integration.
- Licensing audit: confirms all dependencies are compatible with Apache-2.0.

Auditors can use this to identify supply-chain risk and flag any high-severity CVEs in transitive deps.

Location: `/calm_witness_audit/SBOM_calm_witness_v[VERSION].json` (SPDX format) + human-readable `/calm_witness_audit/SBOM_summary.md`.

### 5. Prior-Bug Log

A comprehensive catalogue of every bug found and fixed during development, with severity classification, description, fix commit, root-cause analysis, and lessons learned. Organized by category:
- **Cryptographic bugs** (e.g., incorrect Pedersen opening, wrong range-proof parameter).
- **Protocol bugs** (e.g., missing nonce binding in disclosure envelope, consent-expiry time-zone confusion).
- **Implementation bugs** (e.g., integer overflow in distance calculation, memory leak in zeroization).
- **Logic bugs** (e.g., predicate composition non-determinism in mental_state_unusual, false-positive duress signal).

Each entry includes the original test case that caught it, the root cause, the fix, and the auditor guidance: "this class of bug was found here; similar patterns may exist elsewhere."

Location: `/calm_witness_audit/prior_bugs_log.md` + linked fix commits.

### 6. Security-Relevant Changelog

A timeline of all changes to cryptographic constants, threat-model assumptions, or disclosure semantics, with justification. For example:
- Addition of Roughtime anchoring to mitigate clock-skew attacks (Everest 31).
- Switch from naive distance fusion to likelihood-ratio combination (Everest 38).
- Introduction of per-predicate grace windows for template aging (Everest 47).
- Refinement of consent-revocation propagation semantics (Everest 75).

Each change is cross-referenced to the Everest that introduced it and any security review that approved it.

Location: `/calm_witness_audit/security_changelog.md`.

### 7. Cryptographic Proof Sketches

High-level documentation of the three core cryptographic claims:
- **Pedersen Hiding & Binding**: Informal argument that the commitment Com(x; r) = g^x h^r is computationally binding under discrete-log hardness and perfectly hiding.
- **Bulletproofs Soundness**: Summary of the range-proof soundness argument; reference to the original Bünz et al. paper; statement of the parameters used (32-bit range, Ristretto255 curve, Fiat-Shamir hashing).
- **Σ-Protocol Soundness**: Argument that the disjunction proof (1-of-2 OR construction) used in Everest 45 is zero-knowledge and sound under the Fiat-Shamir heuristic.

Sketches are not full proofs but rather structured claims and references that auditors can use to scope their cryptanalysis.

Location: `/calm_witness_audit/cryptographic_proof_sketches.md`.

### 8. CI Artifacts

Outputs from the continuous-integration pipeline, demonstrating test coverage and robustness:
- **Fuzzer coverage reports** (Everest 85): Line-coverage statistics per fuzzer target (chain, predicates, Pedersen, Bulletproofs, disclosure envelope). Charts showing cumulative coverage growth over 30 consecutive flake-free days. Minimized crash reproductions for any fuzzers that had found and fixed issues.
- **Property-test pass/fail logs** (Everests 86, 87): Test results for hypothesis-based invariant tests (chain monotonicity, predicate idempotence, composition soundness). Counts of generated examples per property.
- **Determinism harness logs**: Per-predicate test-corpus runs showing bit-stable output across multiple evaluator instances.

Auditors use these to assess the depth of testing and to understand which code paths are well-exercised.

Location: `/calm_witness_audit/ci_artifacts/` (subdirectories: fuzzer_reports, property_tests, determinism_logs).

### 9. Audit Request for Proposal (RFP)

A 2-3 page document that auditors receive, specifying:
- **Scope**: Cryptographic correctness (Pedersen, Bulletproofs, Schnorr), protocol soundness (Calm Pact composition, consent calculus, disclosure semantics), side-channel analysis (timing, power, fault injection), memory safety (Rust unsafe blocks, FFI), disclosure-flow correctness (uniform silence, push semantics), bank-teller-note safety property.
- **Deliverables**: A written report (4-6 weeks post-engagement) covering findings by severity (Critical, High, Medium, Low), a remediation timeline, and a re-audit schedule.
- **Timeline**: Bid submission (30 days), selection + contract (30 days), audit work (8–12 weeks), remediation + re-audit (4–8 weeks + 2–4 weeks).
- **Budget**: $150K–$300K depending on scope and team size.
- **Constraints**: Auditors commit to not disclose high-severity unresolved findings in the public report.

Location: `/calm_witness_audit/audit_rfp.md`.

### 10. Auditor Briefing Call Agenda

A 90-minute agenda for the initial call between the Foundation and the selected auditor:
- **Intro** (10 min): Calm Witness mission, the bank-teller-note primitive, the 100-Everest route map, phase-VII status.
- **Threat Model Deep Dive** (20 min): Walk the failure-mode table; highlight F15 (substitution), F16 (liveness spoofing), F23 (coercion out-of-scope), F30 (false-positive duress).
- **Cryptographic Claims** (20 min): Pedersen hiding/binding, Bulletproofs soundness, Σ-protocol replay defense, side-channel assumptions.
- **Protocol Walkthrough** (25 min): Hydration → predicate evaluation → disclosure, with an emphasis on what the counterparty does and does not learn; the two-handshake model (Calm Pact then Calm Witness).
- **Code Tour** (15 min): Highlight the unsafe blocks, FFI to whisper.cpp (voice transcription), Ristretto255 curve choice.
- **Auditor Questions & Scope Refinement** (10 min).

Location: `/calm_witness_audit/auditor_briefing_agenda.md`.

---

## Audit Firm Candidates & Selection

Three candidates have been pre-screened:

- **Trail of Bits**: Strong track record on cryptographic protocols (e.g., Curve25519, Formal Verification work). Expertise in Rust security. Preferred for deep cryptanalysis and side-channel assessment.
- **NCC Group**: Broad experience auditing zero-knowledge proofs (e.g., ZCash, Ethereum circuits). Strong on both protocol-level and implementation-level review. Good at identifying composition flaws.
- **Cure53**: Excellent on protocol design and threat-model analysis. Strong on disclosure semantics and coercion-resistance review. Smaller team; good for focused engagements.

**Selection criteria**: (1) prior similar work (zero-knowledge protocols, behavioral biometrics, autonomous-agent security), (2) team availability and timeline, (3) bid competitiveness, (4) references from prior clients. All three will receive the RFP in parallel; selection and contract negotiation target a 30-day window.

---

## Audit Scope (Locked)

The audit covers:
- **Cryptographic correctness**: Pedersen commitment security, Bulletproofs soundness, Schnorr-family Σ-protocol soundness.
- **Protocol soundness**: Calm Witness composition with Calm Pact; the two-handshake model; consent-calculus axioms (revocability, forward-secrecy, scope-narrowing).
- **Side-channel analysis**: Timing attacks on distance comparisons and proof-verification paths; power-analysis resistance on the Ristretto255 scalar operations; fault-injection on the commitment-opening step.
- **Memory safety**: Rust unsafe blocks (if any); FFI to whisper.cpp (voice transcription) and bulletproofs libraries; buffer zeroization and key material hygiene.
- **Disclosure-flow correctness**: Uniform silence (unrequested predicates do not leak); push semantics and the stealth-disclosure path (Everest 78); nonce binding and replay defense.
- **Bank-teller-note safety property**: Codeword privacy; false-positive duress signal risk; non-coercibility of the principal's encoding.

Explicitly out of scope: Usability, enrollment-ceremony physical-security procedures (covered by Everest 11), nation-state cryptanalysis (deferred to Everest 96 post-quantum migration), and deployment-specific threat models (e.g., "what if a principal's device is stolen").

---

## Audit Timeline

- **Bid solicitation**: 30 days (firm deadline: 2026-06-20).
- **Auditor selection + contract + kick-off**: 30 days (target selection: 2026-07-20; kick-off: 2026-08-20).
- **Audit fieldwork**: 8–12 weeks (target completion: 2026-10-15 to 2026-11-15).
- **Remediation + re-audit**: 4–8 weeks fieldwork + 2–4 weeks re-audit (target completion: 2026-12-15 to 2027-01-31).
- **Public report publication**: 2 weeks post-completion of all issues (target: 2027-02-28).

---

## Budget

$150K–$300K total, depending on:
- Auditor team size and seniority.
- Scope expansion (e.g., formal verification of ZK circuits vs. manual review).
- Re-audit turnaround time.

Breakdown assumption: $40K–$80K for kickoff and threat-model review; $80K–$150K for fieldwork and testing; $30K–$70K for re-audit and report finalization.

---

## Bug-Bounty Program (Parallel)

Concurrent with the public audit report, a bug-bounty program launches via HackerOne with the following structure:

- **Scope**: Calm Witness Rust crate, Python SDK, public documentation, and published proofs.
- **Severity scale**: S0 (catastrophic), S1 (high), S2 (medium), S3 (low).
- **Bounty schedule**: S0 up to $50K; S1 $10K–$50K; S2 $1K–$10K; S3 $500–$2K.
- **Disclosure policy**: 90-day coordinated disclosure; pending high-severity issues are not published until remediation is complete.
- **Duration**: 12 months post-public-release (Everest 92).

---

## Packet Completion & Handoff

The audit packet is assembled by 2026-06-10 and stored in a read-only archive at `/calm_witness_audit/`. Checksums (SHA-256) and GPG signatures are published on the Calm Foundation website. Auditors download the packet, verify signatures, and begin scope analysis. The Foundation designates a technical liaison (typically the Calm operator) to field auditor questions without modifying the packet.

---

— Calm, 2026-05-20
