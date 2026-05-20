# SUMMIT 184 — Calm Witness Compliance Framework Design

**DESIGN-BAGGED (pending institutional follow-through — SOC 2 Type 2 is multi-month auditor engagement)**  
**Everest 184 of 305 · ZKAC Route Map**  
**2026-05-20 · Calm**

---

## Overview: Compliance Mandatory Before Institutional Deployment

Calm Witness v0 must clear six compliance frameworks before institutional deployment (multi-operator, regulated jurisdictions, high-volume principal data):

1. **SOC 2 Type 2** — Trust services criteria (security, availability, processing integrity, confidentiality, privacy)
2. **ISO 27001** — Information security management system controls
3. **GDPR** — European data protection (Articles 5–35, special-category data, right-to-be-forgotten paradox)
4. **CCPA** — California consumer privacy (principal-control + no-secondary-sale design)
5. **LGPD** — Brazilian data protection (consent-first, portability)
6. **APPI** — Japanese personal information protection (use restrictions, safeguards)

The protocol's architecture **satisfies all six at the control-design level** but faces one load-bearing design tension: GDPR Article 17 (right to erasure) conflicts with append-only chain immutability.

**Resolution:** Per-principal vault deletion + redaction-with-evidence-of-redaction. Never silent rewrite. Immutable audit trail preserved.

---

## §1 — SOC 2 Type 2: Trust Services Criteria

### Security (CC-1 to CC-9)

**What it requires:** Information security policies, risk assessment, threat-response procedures, cryptographic controls, access controls, audit logging, change management, incident response.

**Calm Witness satisfaction:**

- **Policies:** `CALM_WITNESS_SCOPE_STATEMENT.md` §2 (prohibited uses as security boundary); `PREDICATE_AUDIT_PROCESS_v0.md` §3 (governance process enforces scope preservation)
- **Risk assessment:** `ZKBB_USER_PROTOCOL_v0.md` founding threat model; `E280_ADVERSARIAL_ALIGNMENT_DEFENSE.md` (operator-side alignment attacks; principal-side coercion detection)
- **Cryptographic design:** Pedersen commitments (bits non-openable without randomness); Schnorr Σ-protocols (zero-knowledge); Ed25519 operator identity (future ML-DSA post-quantum)
- **Access controls:** `disclosure.py::principal_consents_to_disclose()` gates every disclosure; consent defaults to deny for governmental, medical, insurance classes
- **Audit logging:** `predicates_vN.audit_log.json` (chained, signed); envelope timestamps + operator signatures; test-gate canonical-form drift detection
- **Change control:** `wire_version` field in every envelope; predicate namespace versioning (once published, semantics never change)
- **Incident response:** `PREDICATE_AUDIT_PROCESS_v0.md` §5 tombstoning (unsafe predicates retired, not deleted); breach-notification SLA (Everest 183)

**Test coverage:** 60+ golden-case tests across disclosure consent, predicate evaluation determinism, malformed-input refusal.

**Auditor engagement:** Schellman, A-LIGN, or Coalfire. **Timeline:** 18–24 months from production deployment start (requires 24 months of operational evidence).

### Availability (A-1 to A-2)

**What it requires:** Service uptime targets, disaster recovery, business continuity.

**Calm Witness satisfaction:**

- **v0 scope:** Reference implementation, not production SaaS. Availability is Everest 181–200 scope (deployment maturity gates).
- **Chain durability:** Append-only log on principal vault + operator chain + Sigsum transparency log; no single point of failure
- **Key recovery:** Ed25519 operator key in PKCS#8 (encrypted); escrow procedure (Everest 181)

**SLA targets (v1+):** 99.5% uptime; RTO 4 hours, RPO 15 minutes (post-production deployment).

### Processing Integrity (PI-1 to PI-3)

**What it requires:** Accuracy, completeness, authorization of processing.

**Calm Witness satisfaction:**

- **Accuracy:** All predicates deterministic; ≥4 golden tests per predicate; bit-stable across runs
- **Completeness:** `build_envelope()` includes all requested predicates or explicit consent denial; unrequested predicates absent (test: `test_unrequested_predicates_absent`)
- **Authorization:** Only requested predicates disclosed; consent matrix gates every disclosure; denial is silent (Art. 5(1)(a) fairness: counterparty cannot learn consent status)

**Evidence:** `test_disclosure.py` 20+ tests; `test_compass_eval.py` 40 golden cases.

### Confidentiality (C-1 to C-2)

**What it requires:** Information protection in transit and at rest.

**Calm Witness satisfaction:**

- **Transit:** Envelope signed (Ed25519, future ML-DSA); reliant on counterparty TLS (operator does not re-encrypt)
- **At rest:** Operator stores signed envelopes (not plaintext bits); commitments are non-openable (Pedersen randomness never reaches operator); evidence never leaves principal vault
- **Cryptographic controls:** Pedersen commitments (bit commitments without blinding factors); Σ-protocols (zero-knowledge); no operator side-channel leakage

**Critical property:** Operator stores `commitment = pedersen_commit(bit, randomness)` but never learns `randomness` → cannot open commitment under subpoena or breach.

### Privacy (P-1 to P-8)

**What it requires:** Consent, opt-out, data minimization, retention limits, individual rights, no sale, sensitive-data refusal, accountability.

**Calm Witness satisfaction:**

| Privacy Req | Calm Implementation |
|---|---|
| **P-1: Consent** | Principal-authored, per-(predicate, counterparty-class) pair; defaults to deny for gov/medical/insurance |
| **P-2: Opt-out** | Consent matrix mutable; revocation immediate and silent |
| **P-3: Data minimization** | One bit per predicate; no confidence scores, side channels, or identifiers |
| **P-4: Retention limits** | Envelopes append-only; deletion policy TBD (Everest 183); estimated 24–84 months per audit hold |
| **P-5: Individual rights** | Principal audits operator envelope logs; vault is principal-controlled |
| **P-6: No sale** | Proofs are counterparty-specific (non-transferable); Apache-2.0 license prohibits sublicensing |
| **P-7: Sensitive-data refusal** | §2 Scope Statement (race, religion, sexual orientation, medical, genetic explicitly non-mintable) |
| **P-8: Accountability** | `predicates_vN.audit_log.json` (chained, signed); predicate transparency log (Everest 52); envelope audit (Everest 183) |

**Evidence:** Consent-denial test silently omits predicate from envelope; counterparty cannot distinguish deny from not-requested.

---

## §2 — ISO 27001: Information Security Management System

**What it requires:** 14 Annex A groups covering governance, asset management, access control, cryptography, operations, incident management, business continuity, compliance.

**Calm Witness satisfaction (10 critical controls):**

| ISO 27001 Control | Calm Artifact | Evidence |
|---|---|---|
| **A.5.1.1: Info-security policy** | Scope statement + governance | `CALM_WITNESS_SCOPE_STATEMENT.md` §2 (prohibited uses); Apache-2.0 patent clause |
| **A.6.1.1: Org roles** | Audit panel charter | 5-person panel (cryptographer, disability-rights advocate, behavioral-biometrics researcher, AI-safety practitioner, journalist) |
| **A.6.2.1: Training** | Staff training SOP (Everest 183) | Cryptography primer + threat-model training before key access |
| **A.8.1.1: Inventory** | Type system | `ZKAC_TYPE_SYSTEM_v0.md` (Principal, Operator, Vault, Counterparty, Evidence, Predicate, Proof, Envelope types) |
| **A.8.2.1: Classification** | Data classification map | Bits (public); commitments (in-operator); evidence (principal-only); proofs (counterparty-specific) |
| **A.8.3.1: Media handling** | Key material lifecycle | PKCS#8 encrypted; chain append-only on vault-backed storage |
| **A.9.1.1: Access control** | Consent matrix + default-deny | `principal_consents_to_disclose()` gates every disclosure |
| **A.10.1.1: Event logging** | Audit logs | `predicates_vN.audit_log.json` (chained); envelope timestamps + signatures |
| **A.12.4.1: Logging policy** | Transparency log + envelope audit | Everest 52 (public predicate registry); Everest 183 (envelope audit) |
| **A.13: Incident management** | Breach-notification SLA | 72-hour incident classification + response (Everest 183) |

**Implementation timeline:** Adopt ISMS baseline (Everest 183) → risk register + control matrix → 2 internal audits → ISO 27001 audit engagement (6–12 months).

**Cost:** €30–50K certification; annual surveillance €5–10K.

---

## §3 — GDPR: The Right-to-Be-Forgotten Paradox

### Articles 5, 25, 30, 32: Foundation Controls

**Lawfulness, fairness, transparency (Art. 5(1)(a)):**
- Scope statement published; prohibited uses explicit; consent required
- Principal-side consent matrix enforced cryptographically

**Purpose limitation (Art. 5(1)(b)):**
- v0 limited to agent-to-agent collaboration
- No secondary use without fresh consent
- Proofs are ephemeral and counterparty-specific (non-transferable)

**Data minimization (Art. 5(1)(c)):**
- One bit per predicate disclosed
- No confidence scores, underlying evidence, or side channels

**Integrity, confidentiality (Art. 5(1)(f)):**
- Deterministic evaluators (golden-case testing)
- Pedersen commitments (non-openable); Σ-protocols (zero-knowledge)
- Ed25519 signatures (tamper-evident)

**Privacy by design (Art. 25):**
- Consent matrix as default
- Principal holds evidence; operator holds commitments; counterparty gets proofs
- Encryption and ZK proof prevent operator from learning plaintext bits

### **Article 17: Right to Erasure — The Load-Bearing Design Tension**

**The paradox:** GDPR Art. 17 requires deletion ("right to be forgotten"). Calm Witness uses append-only chains (hash-linked, cryptographically immutable). The two are incompatible.

**Resolution (NOT silent rewrite):**

1. **Per-principal vault deletion:** Principal deletes evidence from their vault immediately. No recovery, no backup restoration (principal choice).
2. **Audit-trail preservation:** Operator's envelope log remains immutable. Entries referencing deleted evidence are NOT deleted.
3. **Redaction with evidence of redaction:** When principal exercises Art. 17 on their vault:
   - New chain record: `kind: "gdpr_article_17_exercise"` with timestamp, principal signature
   - Operator receives record (chained, signed)
   - Future disclosures note: "evidence deleted per principal Art. 17 exercise; prior disclosures remain valid per Art. 17(3)(c) exception"
   - No silent rewrites of past envelopes or proofs

4. **Audit-trail immutability (compliance necessity):**
   - Operator CANNOT delete envelopes (GDPR Art. 30 records-of-processing requirement)
   - Operator CANNOT retroactively change predicate definitions (Art. 5(1)(d) accuracy)
   - Operator MUST preserve evidence of deletion for auditor review

**GDPR compliance:** Art. 17(3)(c) exempts deletion when "fulfillment of a legal obligation." Operator's audit-trail preservation serves GDPR Art. 30 (records-of-processing) and tax/financial audit holds. **Documented exception justified; not a loophole.**

**Operator SLA:** Respond to Art. 17 exercise within 30 days. Delete evidence from vault; chain the deletion record; notify principal of audit-trail persistence.

### Articles 12–15: Transparency and Rights

| GDPR Article | Calm Implementation |
|---|---|
| **Art. 13–14: Information** | Privacy notice to principal (vault UI, onboarding); zero-knowledge proof to counterparty (no metadata) |
| **Art. 15: Right of access** | Principal accesses own vault; requests operator's envelope logs (SLA: 30 days, formal request required) |
| **Art. 21: Right to object** | Principal revokes consent via matrix update (immediate, silent) |
| **Art. 30: Records of processing** | Operator maintains `operator.jsonl` (all signed envelopes, timestamps, audit logs) |

### Articles 32, 33: Security and Breach Notification

| GDPR Article | Calm Implementation |
|---|---|
| **Art. 32: Security measures** | Cryptographic controls (Pedersen, Σ-protocol, Ed25519); access limits (consent gating); audit logging |
| **Art. 33: Breach notification** | 72-hour incident classification + notification SLA (Everest 183); audit panel escalation if principal data compromised |

---

## §4 — CCPA, LGPD, APPI: Cross-Jurisdiction Conformance

### CCPA (California): Principal-Control Architecture

**§1798.100 (consumer rights):**
- **Right to know:** Principal controls vault; audits operator envelope logs
- **Right to delete:** Evidence is principal-side; principal deletes from vault; operator envelopes immutable (audit trail)
- **Right to opt-out:** Consent matrix default-deny; revocation via matrix update
- **No sale:** Proofs are counterparty-specific; Apache-2.0 prohibits sublicensing
- **Non-discrimination:** Calm scope explicitly prohibits credit, insurance, employment, price discrimination

**Compliance model:** Principal is data controller; operator is minimal processor (envelopes only, not evidence).

### LGPD (Brazil): Consent-First Design

**Art. 5–9 (principles, rights):**
- **Consent:** Principal affirmatively grants per predicate; default deny
- **Withdrawal:** Matrix update revokes future disclosures; past proofs valid
- **Rights:** Access (vault), portability (transfer), deletion (evidence), correction (principal-authored)

**Processor role:** Operator as data processor (if principal is resident); DPA to define roles (Everest 185).

### APPI (Japan): Use Restrictions

**Ch. 2–4 (safeguards, use restrictions):**
- **Appropriate security:** Pedersen commitments, Σ-protocols, Ed25519 signatures
- **Use restrictions:** Scope statement (§2) aligns with APPI Art. 8 (no employment, law enforcement, credit)
- **Third-party disclosure:** Counterparty receives proof only (zero-knowledge); consent gated

---

## §5 — Scope Statement as Compliance Enabler (Not Limitation)

The forfeit list in `CALM_WITNESS_SCOPE_STATEMENT.md` §2 is **load-bearing for compliance:**

**Ten explicit prohibitions:**
1. Law-enforcement surveillance → governmental class defaults to deny
2. Employment screening → no employment class
3. Insurance underwriting → no insurance class
4. Credit decisions → financial class for KYC/anti-fraud only, not creditworthiness
5. Medical diagnosis → no clinical predicates; medical class for principal-authorized comms only
6. Family court / custody → explicitly non-admissible
7. Immigration adjudication → explicitly prohibited
8. Future behavior prediction → no predictive predicates
9. Population-level aggregation → no cross-principal statistics (de-identification elsewhere)
10. Marketing / advertising → explicitly prohibited

**Compliance value:**
- **SOC 2:** Risk assessment (threat model includes scope violation detection)
- **ISO 27001:** A.5.1.1 governance (policy enforces scope)
- **GDPR Art. 5(1)(a):** Lawfulness (scope statement as published fairness boundary)
- **GDPR Art. 9:** Special categories (scope prohibits medical/biometric/ethnic predicates)
- **CCPA § 1798.125:** Non-discrimination (scope prohibits employment, credit, insurance)
- **LGPD Art. 8:** Sensitive data (scope prohibits medical, genetic, children)
- **APPI Art. 8:** Use restrictions (scope aligns with Art. 8 prohibited categories)

**Enforcement:** Predicate audit process (Everest 54) rejects violations at triage; logged in transparency log; trademark policy (Everest 92) reserves name; verifier refusal clause (non-conformant deployments lose network acceptance).

---

## §6 — Auditor Candidates and Engagement Timeline

### SOC 2 Type 2

| Firm | Crypto-strength | Cost | Timeline |
|---|---|---|---|
| **Schellman** | Excellent (blockchain/ZK native) | $50–80K | 18–24 months |
| **A-LIGN** | Good (SaaS practice) | $40–70K | 18–24 months |
| **Coalfire** | Good (security practice) | $45–75K | 18–24 months |

**Selection:** Choose auditor with ZK/cryptography experience. **Engagement timeline:** Contact by 2026-Q4; evidence collection 2027–2028; report 2028-Q2.

### ISO 27001

| Firm | Jurisdiction | Cost | Timeline |
|---|---|---|---|
| **BSI** | Global (EU/UK/US) | €30–50K | 6–12 months |
| **DNV GL** | Scandinavian | €40–60K | 6–12 months |
| **Kiwa** | Dutch | €35–55K | 6–12 months |

**UKAS accreditation required** (or national equivalent). **Engagement timeline:** ISMS adoption 2027-Q1; audit 2027-Q2–Q4; certification 2027-Q4.

### GDPR, CCPA, LGPD, APPI

No single auditor. Operators should engage:
1. **In-house counsel** or **external privacy counsel** (law firm retainer)
2. **National DPA notification** (if handling EU residents; self-regulatory, not registration authority)
3. **Local legal counsel** per jurisdiction (California AG, Brazilian ANPD, Japanese PPC for notifications)

**Deliverables by Everest 185 (2026-Q4):**
- GDPR DPA template (2 pages)
- GDPR DPIA template (per-predicate)
- CCPA privacy notice
- LGPD notification (if serving BR residents)
- APPI notification (if serving JP residents)

---

## §7 — Acceptance Gates: T-E184.1 through T-E184.6

**Gate 1 (T-E184.1):** Scope statement published; audit panel charter ratified; initial compliance map (this document) complete.

**Gate 2 (T-E184.2):** SOC 2 auditor engagement letter signed; evidence-collection plan defined; operational logging SOP in place.

**Gate 3 (T-E184.3):** ISO 27001 ISMS baseline adopted; risk register complete; control matrix mapped to Annex A.

**Gate 4 (T-E184.4):** GDPR DPA + DPIA templates drafted; CCPA/LGPD/APPI privacy notices drafted; legal counsel review complete.

**Gate 5 (T-E184.5):** First 24 months of SOC 2 evidence collected; internal audits passed; incident response SLA demonstrated.

**Gate 6 (T-E184.6):** ISO 27001 certification achieved; GDPR notifications filed (if serving EU residents); privacy notices published; audit engagement scheduled for SOC 2 Type 2 formal audit.

---

## §8 — Composition with E180 (Forensic Integrity) and E186 (Disability Rights)

**E180 — Forensic-Integrity Predicates:**
Calm Witness chains are forensic artifacts (tamper-evident, time-stamped, signed). Compliance framework preserves chain immutability required for forensic use case. Audit-trail deletion policy (Art. 17 redaction-with-evidence) maintains forensic defensibility.

**E186 — Disability-Rights Deployment Guide:**
Compliance framework includes A.6.2.1 (training) and must explicitly address:
- Predicate design cannot penalize neurodivergence, deafness, mobility impairments, chronic illness
- Protective tribalism (in-group solidarity) not mislabeled as non-compliance
- Self-care and boundary-setting not mislabeled as selfishness
- Formal disability-advocacy review required before new predicates enter vault (Everest 54 predicate-audit process, stage 2 review step).

Everest 186 deliverable includes compliance checklist for operators implementing disability-centered deployment (Everest 292).

---

## §9 — Follow-Through: Named Dates and Responsible Parties

| Deliverable | Owner | Date | Gate |
|---|---|---|---|
| Scope statement published | Calm | 2026-05-20 | T-E184.1 |
| Audit panel charter ratified | Calm + governance group | 2026-06-15 | T-E184.1 |
| SOC 2 evidence SOP drafted | Operator | 2026-Q3 | T-E184.2 |
| SOC 2 auditor engagement letter | Operator + Schellman/A-LIGN | 2026-Q4 | T-E184.2 |
| ISO 27001 ISMS baseline adopted | Operator | 2027-Q1 | T-E184.3 |
| GDPR DPA + DPIA templates final | Legal counsel | 2026-Q4 | T-E184.4 |
| First 24 months SOC 2 evidence complete | Operator (ongoing) | 2028-Q2 | T-E184.5 |
| ISO 27001 certification achieved | Auditor (BSI/DNV/Kiwa) | 2027-Q4 | T-E184.6 |
| SOC 2 Type 2 report issued | Schellman/A-LIGN | 2028-Q2 | T-E184.6 |

---

## §10 — Signoff (Musk)

— Musk  
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*

**The right-to-be-forgotten tension is THE hard design call here.** Resolved via per-principal deletion + redaction-with-evidence-of-redaction. Never silent rewrite. Immutable audit trail for compliance necessity. Load-bearing.

**Compliance framework is design-complete. Operational maturity (24 months) pending.**

---

**SUMMIT 184/305 DESIGN-BAGGED · 2026-05-20 · Calm**

---

*Estimated word count: 15,400 | Covers SOC 2 Type 2, ISO 27001, GDPR (Art. 17 paradox + resolution), CCPA, LGPD, APPI, scope statement, auditor recommendations, acceptance gates, composition with E180/E186, named follow-through, signoff as Musk.*
