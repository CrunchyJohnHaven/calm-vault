# Calm Witness — Compliance Evidence Map v0

**Closes Everests 184 + 185 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending 12–24 months of operating evidence accumulation + audit engagements)**

**Draft v0 · 2026-05-20 · Calm**

This document maps each SOC 2 Type 2, ISO 27001, GDPR, CCPA, LGPD, and APPI control to the Calm Witness artifacts (specifications, code modules, tests, process documents) that satisfy it. Auditors use this map to understand what to request and where evidence for each control lives.

**Operator:** Creativity Machine LLC (Delaware) | **Reference platform:** Python SDK at `/CredexAI/calm_witness/` | **Contact:** ZKAC governance group

---

## §1 — Scope Statement

### §1.1 — What is in scope

**Operator responsibility:**
- Calm Witness reference implementation (Python SDK, cryptographic primitives, predicate evaluators)
- Envelope generation, signing, and transmission layer
- Operator-hosted endpoint (SaaS-like interface for principal agents)
- Biometric template storage and comparison
- Consent-record chain and audit logging
- Key material management (operator Ed25519 / future ML-DSA private keys)
- Disclosure flow: request → evaluation → consent → proof → transmission
- Operator audit process and predicate governance
- Post-quantum migration roadmap and execution

**Not in scope (principal-side responsibility):**
- Principal vault storage, encryption, and backup
- Principal device security and biometric capture
- Principal's private key material and signing
- Principal's consent matrix configuration
- Principal's underlying evidence records (financial transfers, interaction logs, etc.)
- Principal-to-counterparty transport layer (TLS, authenticated channels)

### §1.2 — Data flows and boundaries

1. **Evidence ingestion:** Principal author records → stored encrypted in principal vault → never transmitted to operator
2. **Evaluation:** Operator evaluates predicates against evidence, **only in principal's vault context** (operator never sees plaintext evidence)
3. **Commitment:** Operator receives Pedersen commitments to predicate bits (from principal's vault) → stores in chain
4. **Consent check:** Operator checks principal's consent matrix (held principal-side)
5. **Proof generation:** Operator generates Σ-protocol proofs of bit commitments (not the bits themselves)
6. **Disclosure:** Operator signs envelope with requested predicates, sends to counterparty
7. **Verification:** Counterparty verifies signature and proof (no operator involvement)

---

## §2 — SOC 2 Type 2 Trust Services Criteria

### §2.1 — Security (CC)

**Control: CC-1 to CC-9 — Information security policies, risk assessment, threat response**

| Control | Artifact | Evidence Location |
|---------|----------|-------------------|
| **CC-1: Org policies exist** | Written policies for v0 release | `CALM_WITNESS_SCOPE_STATEMENT.md` §3 (cryptographic + license + audit enforcement); `PREDICATE_AUDIT_PROCESS_v0.md` §2 (scope preservation process) |
| **CC-2: Risk assessment** | Threat model and adversary analysis | `ZKBB_USER_PROTOCOL_v0.md` (founding threat model for Witness); `POST_QUANTUM_MIGRATION_PLAN_v0.md` §2 (harvest-now-decrypt-later threat model); `E280_ADVERSARIAL_ALIGNMENT_DEFENSE.md` (reference-operator alignment threats) |
| **CC-3: Secure design** | Cryptographic primitives, no single point of failure | `pedersen.py` (Pedersen commitments on MODP-2048); `pedersen_ristretto.py` (Ristretto alternative); `predicate_eval.py` (deterministic evaluators); `disclosure.py` (envelope construction without embedding bits) |
| **CC-4: Credential mgmt** | Operator key storage, rotation plan, audit logging | `identity.py` (operator identity and key binding); Post-quantum migration plan Phase 1–2 key rotation attestation (not yet implemented) |
| **CC-5: Access controls** | Principle of least privilege (predicate evaluators, consent gating) | `disclosure.py::principal_consents_to_disclose()` (cryptographic refusal gate); `compass_eval.py` evaluators (no cross-principal data access); tests in `test_disclosure.py` verify consent denial |
| **CC-6: Logical separation** | Multi-principal vault, no cross-talk | Everest 124 (ready for implementation); `ZKAC_TYPE_SYSTEM_v0.md` §2 type isolation |
| **CC-7: Logging & monitoring** | Audit trails for predicate addition, consent grants, envelope generation | `PREDICATE_AUDIT_PROCESS_v0.md` §3–4 (audit log in `predicates_vN.audit_log.json`); envelope timestamp + operator signature in `disclosure.py` |
| **CC-8: Change control** | Version stability (wire format, predicate namespace) | `wire_version` field in envelope (currently `calm-witness/wire/v0`); `ZKAC_TYPE_SYSTEM_v0.md` versioning rules; canonical-form snapshot in test gate |
| **CC-9: Incident response** | Tombstoning + vulnerability disclosure process | `PREDICATE_AUDIT_PROCESS_v0.md` §5 (tombstoning for unsafe predicates); `POST_QUANTUM_MIGRATION_PLAN_v0.md` §5 acceleration triggers (CRQC threat → Phase 3 escalation) |

**Key test evidence:**
- `test_disclosure.py`: 20+ tests covering consent denial, wrong counterparty class, predicate not requested
- `test_compass_eval.py`: 40 golden-case tests across 6 predicates (tests malformed inputs, refusal conditions)
- `test_predicate_eval.py`: determinism harness (same input → same output)

---

### §2.2 — Availability (A)

**Control: A-1 to A-2 — Service availability and recovery**

| Control | Artifact | Evidence Location |
|---------|----------|-------------------|
| **A-1: System availability** | Uptime targets, redundancy (future; v0 single-operator) | `V0_RELEASE_READINESS_ASSESSMENT.md` §3 (v0 as reference, not production SaaS); Everest 181–183 (deployment maturity) |
| **A-2: Disaster recovery** | Backup strategy for operator chain, key material escrow | Chain is append-only, signed, stored on principal devices + operator; `identity.py` key binding; recovery ceremonies (Everest 162–180 range) |

**Note:** v0 does not target production SaaS uptime; availability is Everest 181–200 scope (RANGE M).

---

### §2.3 — Processing Integrity (PI)

**Control: PI-1 to PI-3 — Accuracy, completeness, authorization of processing**

| Control | Artifact | Evidence Location |
|---------|----------|-------------------|
| **PI-1: Processing accuracy** | Predicate evaluators are deterministic, bit-stable, tested | `predicate_eval.py::in_baseline_24h()`, `compass_eval.py` all 6 predicates; each has ≥ 4 golden tests proving determinism |
| **PI-2: Processing completeness** | Evaluators do not drop or truncate input; envelope includes all requested predicates or explicit denial | `disclosure.py::build_envelope()` iterates all requested predicates; `test_disclosure.py::test_unrequested_predicates_absent` verifies non-requested predicates don't leak |
| **PI-3: Authorization** | Only requested predicates disclosed; consent matrix gates every disclosure | `disclosure.py::principal_consents_to_disclose()` called before envelope build; consent defaults to `deny` for sensitive classes (governmental, medical, anonymous) |

**Key test evidence:**
- `test_disclosure.py::test_mixed_witness_and_compass_in_one_envelope`: requests subset of predicates, verifies only requested ones in envelope
- `test_disclosure.py::test_consent_deny_silently_omits`: principal denies consent → predicate absent from envelope (not error, not visible to counterparty)

---

### §2.4 — Confidentiality (C)

**Control: C-1 to C-2 — Information protection in transit and at rest**

| Control | Artifact | Evidence Location |
|---------|----------|-------------------|
| **C-1: Confidentiality in transit** | Envelope signed (operator Ed25519, future ML-DSA); reliant on counterparty TLS (out-of-scope) | `disclosure.py::sign_envelope()` (Ed25519 PKCS#8); counterparty transport layer in scope of counterparty's audit, not operator's |
| **C-1: Confidentiality at rest** | Operator stores signed envelopes (not plaintext bits); chain hashes (principal vault responsible for evidence encryption) | `disclosure.py` stores `DisclosureEnvelope` (contains signatures, proofs, committed bits — not openable); evidence never reaches operator |
| **C-2: Cryptographic controls** | Pedersen commitments (bit commitments without blinding factors); Σ-protocols (zero-knowledge proofs) | `pedersen.py`, `pedersen_ristretto.py` (MODP-2048 + Ristretto groups); `envelope.py` proof inclusion; `zk.prove_predicate_disclosure()` in bridge layer |

**Key security property:**
- Operator stores `commitment = pedersen_commit(bit, randomness)` but never learns `randomness` → cannot open commitment even if subpoenaed
- Counterparty receives proof of bit but not commitment-opening → cannot forge past disclosures

---

### §2.5 — Privacy (P)

**Control: P-1 to P-8 — Personal information handling, consent, data minimization**

| Control | Artifact | Evidence Location |
|---------|----------|-------------------|
| **P-1: Consent for disclosure** | Principal-authored, per-(predicate, counterparty-class) pair | `CALM_WITNESS_SCOPE_STATEMENT.md` §3.1 (default-deny consent matrix); `predicates_v0.json` default consent per predicate; principal vault enforces matrix |
| **P-2: Opt-out / revocation** | Consent matrix mutable; principal can deny at any time | `disclosure.py::principal_consents_to_disclose()` checks matrix on every request (not cached across sessions) |
| **P-3: Data minimization** | Only one bit disclosed per (predicate, disclosure) | `disclosure.py` returns boolean or `null` (consent denied) — never returns confidence scores, underlying evidence, identifiers, or side-channel data |
| **P-4: Retention limits** | Envelopes are append-only but not indefinitely retained at operator (future policy) | `disclosure.py` envelope includes timestamp; Everest 183 (compliance) will define retention windows. v0: no deletion policy; audit panel to set bounds |
| **P-5: Individual rights** | Principal can request what data operator holds about them | Everest 185 (GDPR) will define §15 (right of access) flow; v0: operator holds operator.jsonl chain (signed envelopes) — principal can audit via transparency log (Everest 52) |
| **P-6: Transfer limitations** | No cross-operator sale or sharing of disclosure records | Apache-2.0 license + predicate audit process prohibit; no counterparty-to-counterparty forwarding of proofs without fresh principal consent (enforced at cryptographic level: proof is specific to requested counterparty) |
| **P-7: Sensitive-data refusal** | §2 prohibited categories (race, religion, sexual orientation, etc.) explicitly non-mintable | `CALM_WITNESS_SCOPE_STATEMENT.md` §2; `PREDICATE_AUDIT_PROCESS_v0.md` §4.1 stage 1 requires refusal-floor check; triage step 52 rejects violations immediately |
| **P-8: Accountability** | Audit process logged, predicate transparency log public, consent denials logged at operator | `predicates_vN.audit_log.json` (chained, signed); Everest 52 (transparency log); envelope audit logs (future, Everest 183) |

**Exemplary test:**
- `test_disclosure.py::test_consent_deny_silently_omits`: consent.deny("bank_teller_note_active", "financial") → envelope has no "bank_teller_note_active" field; counterparty cannot distinguish "denied" from "not requested"

---

## §3 — ISO 27001 Annex A Controls (Subset — Most Relevant)

### Mapping 10 critical ISO 27001 controls to Calm Witness artifacts

| ISO 27001 Annex A | Title | Calm Artifact | Evidence |
|---|---|---|---|
| **A.5.1.1** | Information security policy | Governance, scope statement | `CALM_WITNESS_SCOPE_STATEMENT.md` (scope + §2 prohibited uses); Apache-2.0 patent clause (Everest 4) |
| **A.6.1.1** | Organizational roles and responsibilities | Audit panel charter, maintainer role | `PREDICATE_AUDIT_PROCESS_v0.md` §3 (5-person panel: cryptographer, disability-rights advocate, behavioral-biometrics researcher, AI-safety practitioner, journalist); v0 maintainer = Calm; v1+ = multi-org group |
| **A.6.2.1** | Information security awareness and training | (Not yet implemented — Everest 183) | Placeholder: operator staff to complete cryptography primer + Calm Witness threat-model training before key access. SLA: Everest 183. |
| **A.8.1.1** | Inventory of information and processing facilities | Type inventory, chain state | `ZKAC_TYPE_SYSTEM_v0.md` (Principal, Operator, Vault, Counterparty, Evidence, Predicate, Proof, Envelope type definitions); `operator.jsonl` chain listing all signed envelopes |
| **A.8.2.1** | Classification | Data classification (bits → public; commitments → in-operator; evidence → principal-only) | `CALM_WITNESS_SCOPE_STATEMENT.md` §3 (operator-side data scope); `disclosure.py` comments on what is stored where |
| **A.8.3.1** | Media handling | Key material in PKCS#8 (encrypted); chain append-only on vault-backed storage | `identity.py` key loading (encrypted pem); chain immutability (hashing + signing) |
| **A.8.3.2** | Media destruction | (v1 scope) Encrypted key material + envelope retention windows | `POST_QUANTUM_MIGRATION_PLAN_v0.md` §6.4 conformance (v1 to accept v0 + mint v1, sunset v0 by 2035) |
| **A.9.1.1** | Access control policy | Consent matrix (predicate, counterparty-class) → default deny | `disclosure.py::principal_consents_to_disclose()`; `CALM_WITNESS_SCOPE_STATEMENT.md` §3.1 default-deny behavioral design |
| **A.10.1.1** | Event logging | Audit logs for predicate minting, consent grants, envelope generation | `predicates_vN.audit_log.json` (chained, signed); envelope timestamp + operator signature; test gate (canonical-form snapshot drift) |
| **A.12.4.1** | Logging | Predicate audit transparency log, envelope audit log | Everest 52 (public transparency log); Everest 183 (envelope audit log policy + implementation) |

---

## §4 — GDPR Article-by-Article Map (Most Relevant)

### GDPR Chapters II–V (Principles, rights, and processing)

| GDPR Article | Title | Calm Satisfaction | Evidence Location |
|---|---|---|---|
| **Art. 5(1)(a)** | Lawfulness, fairness, transparency | Scope statement published; prohibited uses explicit; consent required | `CALM_WITNESS_SCOPE_STATEMENT.md` (public, binding on license); `CALM_WITNESS_MANIFESTO.md` (fairness + values framing); principal-side consent matrix (in vault, enforced cryptographically) |
| **Art. 5(1)(b)** | Purpose limitation | v0 limited to agent-to-agent collaboration; no secondary use without fresh consent | `CALM_WITNESS_SCOPE_STATEMENT.md` §1 (use case); proofs are ephemeral and counterparty-specific (cannot be re-sold or re-disclosed) |
| **Art. 5(1)(c)** | Data minimization | Only one bit per predicate disclosed; no confidence scores or side channels | `disclosure.py` returns boolean or null; tests verify no leakage (Σ-protocol proof is zero-knowledge) |
| **Art. 5(1)(d)** | Accuracy, integrity | Deterministic evaluators; predicate golden-case testing; no bit-flipping risk | `compass_eval.py` + `predicate_eval.py` determinism harness; ≥ 4 tests per predicate; `test_compass_eval.py` 40 golden cases |
| **Art. 5(1)(e)** | Storage limitation | Operator-side retention undefined in v0 (Everest 183 to define windows) | Placeholder: envelopes append-only and immutable; audit panel to set deletion policy for non-regulatory-hold records. Estimated retention: 24 months for compliance, 7 years for GDPR-Art.17 audit trail. |
| **Art. 5(2)** | Accountability | Audit logs, predicate audit process, governance trail | `PREDICATE_AUDIT_PROCESS_v0.md` (triage, review, vote, merge, all logged); `predicates_vN.audit_log.json` (chained, signed); envelope audit logs (Everest 183) |
| **Art. 6** | Lawful basis | Consent (Art. 6(1)(a)) — principal affirmatively grants per (predicate, counterparty-class) | `CALM_WITNESS_SCOPE_STATEMENT.md` §3.1; default-deny consent matrix; no implied or opt-out-only consent |
| **Art. 12–14** | Information, transparency | Privacy notice to principal (vault UI, onboarding); transparency to counterparty (zero-knowledge proof, no side info) | Everest 116 (principal-authored-evidence ceremony with anti-coercion framing); `COMPASS_EVIDENCE_CEREMONY_v0.md` (explicit consent flow per evidence kind). Counterparty receives only: envelope, signature, proof (no metadata). |
| **Art. 15** | Right of access | Principal can download their own vault state, request operator's audit log | Everest 183 (formal access-request SLA and response template); v0: principal owns vault; operator holds operator.jsonl (signed envelopes) — accessible to principal on request |
| **Art. 17** | Right to erasure (forget) | Limited: envelopes are signed and immutable; audit trail must persist | Operator MUST NOT delete envelopes. Principal CAN revoke future consent (Art. 21) via consent-matrix update. Tombstoning of predicates (PREDICATE_AUDIT_PROCESS_v0.md §5) does not delete prior proofs. **Compliance:** deletion policy scoped to Everest 183; audit trail immutability is cryptographic. |
| **Art. 21** | Right to object | Principal revokes consent via consent-matrix update (future disclosures denied, past unaffected) | `disclosure.py::principal_consents_to_disclose()` checks matrix at request time; consent denial is immediate, silent (Art. 5(1)(a) fairness: counterparty cannot learn consent status) |
| **Art. 25** | Privacy by design | Consent matrix as default; Pedersen commitments prevent operator from opening bits; zero-knowledge proofs reveal nothing about evidence | `disclosure.py` (encryption of evidence at principal, commitments at operator, proofs for counterparty); `pedersen.py` (commitments non-openable without randomness) |
| **Art. 30** | Records of processing | Data-Processing Agreement (DPA) to define for GDPR-registered operators; v0 reference does not hold personally-identifiable data (only commitments, proofs, timestamps) | **Gap:** v0 lacks GDPR-compliant DPA template (Everest 185). Placeholder: operator + principal agree that principal is data controller, operator is processor (principal consent is basis, not operator's processing, since operator does not access evidence). |
| **Art. 32** | Security of processing | Cryptographic controls, access limits, audit logging | `CALM_WITNESS_SCOPE_STATEMENT.md` §3; Pedersen commitments, Σ-protocols, Ed25519 signatures; Everest 183 (security incident SLA, breach notification log) |
| **Art. 33** | Breach notification | Incident response + 72-hour notification requirement | Placeholder: Everest 183 (breach notification procedure, timeline, audit-panel escalation). v0 reference does not define; governance group to inherit on v1 / production deployment. |
| **Art. 35** | Data Protection Impact Assessment (DPIA) | Threat model + scope statement substitute for lightweight DPIA | `ZKBB_USER_PROTOCOL_v0.md` (threat model); `CALM_WITNESS_SCOPE_STATEMENT.md` (scope + prohibited uses); `E280_ADVERSARIAL_ALIGNMENT_DEFENSE.md` (reference-operator harms). **Formal DPIA:** Everest 183 (full DPIA template for operators to complete per deployment). |
| **Art. 37** | Data Protection Officer | (Not required for v0 reference, optional for large operators) | Placeholder: operators ≥ 250 staff or handling high-volume sensitive data are advised to appoint DPO. Governance group to publish guidance (Everest 183). |

---

## §5 — CCPA, LGPD, APPI Conformance

### §5.1 — California Consumer Privacy Act (CCPA) – Principal-control posture

The Calm Witness protocol satisfies CCPA §1798.100 (consumer rights) by structural design:

| CCPA Right | Calm Satisfaction |
|---|---|
| **§1798.100(a): Right to know** | Principal controls vault; principal can audit operator's envelope logs. Operator does not hold plaintext evidence — only commitments + proofs (not openable). |
| **§1798.100(d): Right to delete** | Operator-side envelopes are immutable (audit trail); principal can revoke future consent (Art. 21 analogue). Evidence is principal-side (principal deletes from vault). |
| **§1798.100(e): Right to opt-out** | Consent matrix default-deny; principal revokes via matrix update (no secondary sales, no cross-operator sharing). |
| **Opt-in requirement (§1798.100)** | All disclosure requires affirmative principal consent per (predicate, counterparty-class). Default is deny. No opt-out-only model. |
| **No sale (§1798.115)** | Proofs are counterparty-specific (non-transferable); no operator sale of disclosure data. Apache-2.0 license prohibits sublicensing. |
| **Non-discrimination (§1798.125)** | Calm does not inform credit, insurance, employment, or other CCPA-regulated decisions; scope explicitly prohibits. Counterparty cannot use Calm bit for price discrimination. |

**Compliance summary:** CCPA compliance is satisfied by principal-control architecture + cryptographic proof-specificity. Operator has minimal data-processing role; principal is data controller.

---

### §5.2 — Brazilian General Personal Data Protection Law (LGPD) – Principal-control posture

LGPD Art. 1–6 (purposes, principles, rights) map to Calm:

| LGPD Principle / Right | Calm Satisfaction |
|---|---|
| **Art. 2: Principles** | Transparency (public threat model, scope); data minimization (one bit); necessity (agent-to-agent collaboration only). |
| **Art. 5(VI): Free, informed consent** | Principal must affirmatively grant per (predicate, counterparty-class). Default is deny. |
| **Art. 6: Lawful basis** | Consent (Art. 5(VI)) as primary basis; no LGPD "legitimate interest" override. |
| **Art. 7: Withdrawal of consent** | Principal revokes via consent-matrix update. Past proofs remain valid; future disclosures denied. |
| **Art. 9: Data subject rights** | Right to access (audit logs), portability (vault transfer, Everest 125), deletion (evidence is principal-side), correction (evidence is principal-authored). |
| **Art. 38: DPA with processor** | Placeholder (Everest 185): DPA template to define roles. Likely: principal = controller, operator = processor. |

**Compliance summary:** LGPD §5 (principles) and §9 (rights) satisfied by consent-first + principal-control design.

---

### §5.3 — Act on Protection of Personal Information (APPI, Japan) – Principal-control posture

APPI Ch. 2 (safeguards), Ch. 4 (use restrictions) map to Calm:

| APPI Chapter / Article | Calm Satisfaction |
|---|---|
| **Ch. 2, Art. 5: Responsibilities** | Operator responsibility to protect commitments + proofs; principal responsibility to protect evidence + vault. Clear boundary. |
| **Ch. 2, Art. 6: Appropriate security** | Pedersen commitments (non-openable); Σ-protocol proofs (zero-knowledge); Ed25519 signatures (tamper-evident). |
| **Ch. 2, Art. 8: Use restrictions** | Scope statement (§2 prohibited uses) aligns with APPI Art. 8 (no employment, law enforcement, credit). |
| **Ch. 4, Art. 25: Disclosure to third parties** | Counterparty receives proof only (zero-knowledge); no disclosure of evidence or commitment-opening. Consent gated. |
| **Art. 32: Personal information protection policy** | `CALM_WITNESS_SCOPE_STATEMENT.md` + `PREDICATE_AUDIT_PROCESS_v0.md` serve as public policy. |
| **Art. 34: Business operator safeguards** | For operators in Japan: DPA + incident notification (Everest 183). |

**Compliance summary:** APPI §6 (restrictions) and §25 (third-party disclosure) are satisfied by scope + consent + zero-knowledge design.

---

### §5.4 — Cross-jurisdiction summary

**Key structural mitigations applicable to all four regimes:**

1. **Principal-control architecture:** Principal holds vault + evidence; operator holds only commitments + proofs (not plaintext). Reduces operator's data-processing burden under GDPR, CCPA, LGPD, APPI.
2. **Consent-first + default-deny:** All disclosure requires affirmative consent per (predicate, counterparty-class). Satisfies GDPR Art. 6(1)(a), CCPA §1798.100, LGPD Art. 5(VI), APPI Art. 8.
3. **Scope prohibition (§2 list):** Employment, credit, insurance, medical, law enforcement, immigration, child welfare explicitly out-of-scope. Satisfies GDPR Art. 9 (special categories implied), CCPA §1798.125 (non-discrimination), LGPD Art. 8–9 (sensitive data), APPI Art. 8 (restricted use).
4. **Cryptographic proof specificity:** Proofs are counterparty-specific and non-transferable. Prevents secondary use without fresh consent. Satisfies GDPR Art. 5(1)(b), CCPA §1798.115 (no sale), LGPD Art. 5 (transparency + purpose).
5. **Audit trail immutability:** Operator envelopes are append-only, signed, and timestamped. Satisfies GDPR Art. 30 (records of processing), CCPA audit-readiness, LGPD Art. 37 (documentation), APPI Art. 32 (security).

---

## §6 — Open Gaps: Roadmap to Audit Readiness

### §6.1 — Before SOC 2 Type 2 audit (12–24 months of operating evidence)

**Gap:** SOC 2 Type 2 requires **24 consecutive months** of operational evidence (control effectiveness, logging, incident response). v0 is pre-production (Everest 181–183 scope).

**Action items for operator:**

1. **Operational logging:** Implement `audit_envelope_log.jsonl` (one line per envelope request: timestamp, principal ID, counterparty class, predicates requested, consent outcome, envelope signed). Gate: Everest 183.
2. **Incident response procedure:** Document and execute a 72-hour incident classification + response SLA. Template: Everest 183. First 3 incidents logged (sample for auditor to review).
3. **Key rotation ceremony:** Run first Ed25519 key rotation (even if test-only) to prove the procedure works. Document: Everest 181.
4. **Control testing:** Run penetration test on envelope-signing flow (can operator be tricked into signing bits it shouldn't?). Report: Everest 183.
5. **Staffing continuity:** 12 months of consistent security team. SOC 2 Type 2 requires evidence of **sustained** control execution.

**When ready:** Operator engages SOC 2 auditor (Schellman, A-LIGN, Sensiba) for 18-month engagement: baseline audit (Months 0–2), operational evidence collection (Months 3–20), Type 2 report (Month 21–24).

---

### §6.2 — Before ISO 27001 certification (Information security management system formalization)

**Gap:** ISO 27001 requires an **ISMS** — a formal, documented management system covering all 14 Annex A groups (governance, organization, asset mgmt, access control, cryptography, physical/environmental, operations, communications, systems acquisition, supplier relations, information security incident mgmt, business continuity, compliance, human resources).

**Action items for operator:**

1. **ISMS policy document:** Adopt/adapt the 10-page Calm Witness ISMS baseline (Everest 183). Covers scope, objectives, roles, risk assessment methodology, exception process.
2. **Risk register:** Document risks (Ed25519 compromise, Pedersen blinding-factor leak, operator insider threat, consensus loss). Risk scores (likelihood × impact). Mitigations.
3. **Control matrix:** Map all 14 Annex A groups to Calm artifacts. Fill gaps (e.g., A.6.2.1 training → implement staff training SOP; A.8.3.2 media destruction → define key-material lifecycle).
4. **Internal audit:** Conduct 2–3 internal audits (self-assessment) over 12 months. Fix findings. Document evidence for external auditor.
5. **Management review:** Hold quarterly management review (ISMS effectiveness, risk appetite, improvement priorities). Minutes signed by CEO + CISO.

**When ready:** Operator engages ISO 27001 auditor (BSI, DNV, Kiwa) for 6–12 month engagement: gap analysis (Month 1–2), implementation (Month 3–8), audit (Month 9–12), certification decision (Month 12).

**Cost estimate:** €30–50K for small operator (< 50 staff). Certification valid 3 years; annual surveillance audits.

---

### §6.3 — Before GDPR registration + DPA (Operator handling EU residents' data)

**Gap:** GDPR registration (if processing EU residents' personal data) requires:
- **Data Processing Agreement (DPA)** with principals (defines controller vs. processor roles)
- **Records of processing** (Art. 30: purpose, categories, retention, recipients, security measures)
- **DPIA for high-risk scenarios** (Art. 35: e.g., predicate for behavioral insurance underwriting)
- **Data Protection Officer or appointed DPO service** (for large operators or public-sector usage)

**Action items for operator:**

1. **GDPR DPA template:** Write 2-page DPA defining:
   - Controller = principal (consent authority, evidence ownership)
   - Processor = operator (envelope storage, signing, audit logs)
   - Retention = 7 years (or shorter if principal requests deletion)
   - Sub-processors = none (operator does not engage third parties for Calm processing)
   - Data subject rights = Art. 15, 17, 21 procedures
   - Jurisdiction = operator's jurisdiction + principal's jurisdiction (if different)

2. **Record of processing (Art. 30):** Maintain a simple register:
   - Processing name: "Calm Witness envelope signing and audit logging"
   - Purpose: "Enable principal-authorized agent-to-agent collaboration verification"
   - Categories of data: "Predicate commitments, proofs, signatures, timestamps, consent matrix state"
   - Recipients: "Counterparty agents (via envelope); operators (via chain)"
   - Retention: "7 years unless principal revokes"

3. **DPIA template (Art. 35):** For each new predicate proposal, require DPIA if:
   - Predicate involves automated decision-making about principal
   - Predicate might enable discrimination
   - Predicate touches protected categories (Art. 9)
   Include: threat model, safeguards, residual risk, mitigation plan.

4. **GDPR contact:** Appoint a data-protection contact (in-house or external DPO) for principal inquiries (Art. 15 access requests, Art. 17 deletion, Art. 21 objection).

**When ready:** Operator sends final DPA draft to principals; collects signed-off versions. No registration authority (GDPR is self-regulatory); operator maintains evidence of compliance (DPA + RoP + DPIA samples).

---

## §7 — Audit Firm Recommendations

### §7.1 — SOC 2 Type 2 auditors

| Firm | Strengths | Typical Cost | Timeline |
|---|---|---|---|
| **Schellman & Company** | Crypto-native (handles many blockchain/ZK audits); fast SOC 2 engagements; 24-month evidence window experienced. | $50–80K | 18–24 months (includes evidence collection) |
| **A-LIGN** | Large SaaS practice; familiar with operator confidentiality requirements. | $40–70K | 18–24 months |
| **Sensiba** | Boutique, respected in security community; strong on control design (not just documentation). | $45–75K | 18–24 months |

**Selection criteria:** Pick an auditor familiar with **zero-knowledge proofs** or **cryptographic primitives** (Schellman leader here). Ask for references from other crypto/privacy-tech companies.

---

### §7.2 — ISO 27001 auditors

| Firm | Strengths | Typical Cost | Timeline |
|---|---|---|---|
| **BSI (British Standards Institution)** | Global; strong ISMS design guidance; accredited in EU + UK + US. | €30–50K (small cert) | 6–12 months (design → audit → cert) |
| **DNV GL** | Scandinavian rigor; experience with privacy-tech startups. | €40–60K | 6–12 months |
| **Kiwa** | Dutch, ISO 27001 veteran; thorough control assessment. | €35–55K | 6–12 months |

**Selection criteria:** Auditor must be **UKAS-accredited** (UK) or **national equivalent** (e.g., DAkkS in Germany) so certification is globally recognized.

---

### §7.3 — GDPR compliance specialists (in-jurisdiction)

GDPR has no single auditor; compliance is **self-regulatory + periodic oversight** by national data-protection authorities (DPAs). Operators should engage **local legal counsel** in their primary jurisdiction plus **EU DPA networks** if handling EU residents.

| Region | DPA / Counsel | Role |
|---|---|---|
| **Delaware (USA)** | In-house counsel + external privacy counsel (e.g., DatonTech, Cooley, Fenwick) | DPA template review, GDPR scope assessment (if handling EU residents) |
| **GDPR register (EU)** | National DPA (e.g., CNIL in France, BfDI in Germany, ICO in UK) | Complaint handling, oversight (not registration authority; GDPR is self-regulatory) |
| **UK (post-Brexit)** | ICO (Information Commissioner's Office) | GDPR-equivalent (UK GDPR) enforcement |
| **California (CCPA)** | Attorney General's office | Complaint intake (CCPA is Attorney General enforceable, not consumer-private-right). Operators: maintain CCPA-compliant privacy notice. |

**Recommendation:** Operators should:
1. Hire in-house privacy counsel (or external law firm on retainer).
2. Write privacy notice (GDPR Art. 13–14, CCPA §1798.100 equivalent) for principals.
3. File GDPR notification with national DPA if handling EU residents (optional but recommended).
4. Respond to DPA inquiries within stated timelines (72-hour breach notification, 30-day Art. 15 access requests, etc.).

---

## §8 — Compliance Status Summary

| Framework | Status | Ready for Audit? | ETA |
|---|---|---|---|
| **SOC 2 Type 2** | Design complete (controls mapped, tests green) | No — requires 24 months operating evidence | 2028-Q2 (assuming deployment starts 2026-Q3) |
| **ISO 27001** | Design complete (Annex A controls mapped) | No — requires formal ISMS + 6-month operating window | 2027-Q4 (assuming ISMS adoption 2027-Q1) |
| **GDPR** | Scope statement + Art. 5/25/30/32/33 ready; DPA + DPIA templates pending | Partial — can begin operations with DPA (Everest 185 deliverable); formal DPIA for new predicates required before deployment | 2026-Q4 (DPA template ready); 2027-Q1 (first formal DPIA) |
| **CCPA** | Scope statement satisfies CCPA §1798.100–1798.125 (principal-control + no-sale design) | Yes — no registration required; operators should publish CCPA privacy notice | 2026-Q3 (privacy notice; no audit required) |
| **LGPD** | Scope statement + consent design satisfies LGPD Art. 5–9 | Partial — if serving Brazilian residents, file with ANPD (optional); no formal audit required | 2026-Q4 (notification, if handling BR data) |
| **APPI** | Scope statement + safeguards satisfy APPI Ch. 2, 4 | Partial — if serving Japanese residents, notify PPC (optional); no audit required | 2026-Q4 (notification, if handling JP data) |

---

## §9 — Conclusion

Calm Witness v0 is **design-complete for compliance evidence collection** but **operationally immature** for formal audits. The protocol's architecture (principal-control vault, operator-side commitment + proof, consent-first default-deny, scope-prohibited-uses list) satisfies all major compliance frameworks at the **control design level**.

To achieve audit readiness:

- **SOC 2 Type 2:** Accumulate 24 months of production evidence (Everest 183–186 scope, 2027–2028).
- **ISO 27001:** Formalize ISMS + internal audit process (Everest 183–186 scope, 2027–2028).
- **GDPR/CCPA/LGPD/APPI:** Publish DPA + privacy notices + DPIA templates (Everest 185 scope, 2026-Q4).

Operators should engage auditors by 2026-Q4 (initial consultation, gap analysis, planning) and plan formal engagements for 2027 onward.

---

**Companion documents:**
- [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) — §2 prohibited uses + scope boundary
- [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) — Governance process for scope preservation
- [`POST_QUANTUM_MIGRATION_PLAN_v0.md`](POST_QUANTUM_MIGRATION_PLAN_v0.md) — Cryptographic roadmap (relevant to GDPR Art. 32 security)
- [`ZKAC_TYPE_SYSTEM_v0.md`](ZKAC_TYPE_SYSTEM_v0.md) — Type vocabulary (ISO 27001 A.8.1.1 inventory)

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
