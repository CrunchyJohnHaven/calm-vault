# Calm Suite — SOC 2 Type 2 + ISO 27001 Control Map v0 (E184, DESIGN-BAGGED)

**Status:** DESIGN-BAGGED — architectural control claims only. No audit-firm engagement has occurred. Not for external distribution until Trail of Bits / NCC Group or equivalent engagement is complete.
**Date:** 2026-05-20
**Author:** Calm (operating for John Bradley, Creativity Machine LLC)
**Scope primitives:** Calm Pact v0, Calm Witness v0, Calm Compass v0, Calm Concord v0, Calm Tenancy v0

---

## Scope

This document maps every Calm Stack primitive to at least one SOC 2 Type 2 Trust Service Criterion (TSC) and at least one ISO 27001:2022 Annex A control. Each mapping identifies the protocol artifact that would serve as primary audit-trail evidence. Gaps where the Calm design exceeds either baseline are enumerated and tagged DESIGN-BAGGED pending audit-firm engagement.

Primitives in scope:

| Primitive | Function |
|---|---|
| **Calm Pact** | ZK directive-equality proof for agent-to-agent alignment; Pedersen commitment on Ristretto255 + Σ-protocol |
| **Calm Witness** | Single-bit principal-state attestation with refusal floor; consent matrix gating all disclosure |
| **Calm Compass** | ZK values-predicate proof over principal's append-only chain; principal-authored vocabulary |
| **Calm Concord** | Purpose-scoped alignment calculator; structured outcome only, no numeric score |
| **Calm Tenancy** | Conduct protocol for operator-held domain: cringe gate, SLA, credential vault, daily chain |

Primitives **out of scope** for this version: ZKAC credential infrastructure, CredexAI identity layer, Sigsum/Roughtime anchoring (handled in separate cryptographic audit packet).

---

## SOC 2 Trust Service Criteria Mapping

### CC — Security (Common Criteria)

**CC6 — Logical and Physical Access Controls**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Pact | Directive commitments are Pedersen-committed; the opening value (the directive text) never crosses the wire. Only the equality bit and Σ-proof are transmitted. Unauthorised access to the directive is cryptographically infeasible. | Per-session proof transcript; Ristretto255 commitment bytes in chain record |
| Calm Witness | `principal_consents_to_disclose(predicate_id, counterparty_class)` gates all external disclosure. Default consent matrix is `deny` for governmental, medical, anonymous classes. Access to principal state is consent-mediated, not operator-mediated. | `consent_matrix_v0.json` snapshot; per-session `witness_disclosure_record` in vault chain |
| Calm Tenancy | Domain credentials live in Calm Vault, encrypted at rest, retrieved only via deterministic policy. Operator never reads credentials directly; only Pedersen-committed handles cross the model boundary. Daily credential-rotation freshness check chained. | `tenancy_daily_check` chain record; vault access log |

**CC7 — System Operations**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Tenancy | Daily scripted sweep: DNS health, TLS cert expiry, mailbox queue, response-time distribution, content-drift detection. Every sweep result is chained with a `tenancy_daily_check` record. | Append-only chain; `tenancy_daily_check` records with timestamps |
| Calm Pact | Proof verification is deterministic; a failed equality check returns a structured refusal. No partial-information leak on failure. | Session result log (pass/fail bit only) |

**CC8 — Change Management**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Compass | Classifier evaluator hash is pinned into every proof. A principal can refuse to use an updated classifier. Classifier version changes require predicate-vocabulary audit (Everest 54 process). | Proof header; `classifier_hash` field; Predicate Audit Log |
| Calm Witness | Predicate additions require Predicate Audit Process (Everest 54). §2 prohibited uses are a one-way ratchet — uses can be prohibited, never permitted. Change log is public. | Audit triage log; public predicate-audit transparency log |

---

### A — Availability

**A1 — Availability**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Tenancy | Every inbound response-seeking email receives an auto-generated acknowledgement within 10 minutes, machine-signed. SLA published at `/.well-known/calm-tenancy.json`. Daily response-time distribution check chained. | `tenancy_daily_check` record; `calm-tenancy.json` public assertion; mailbox response-time log |
| Calm Pact | Protocol is stateless per session; no persistent service required for proof generation. Verifier can be run by any counterparty from open-source reference implementation. | Open-source reference impl; session transcript |

---

### PI — Processing Integrity

**PI1 — Processing Integrity**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Pact | Σ-protocol proof is complete (honest prover always succeeds) and sound (dishonest prover succeeds with negligible probability over Ristretto255). Verification is deterministic and public. | Proof bytes; verifier source; Fiat-Shamir challenge derivation |
| Calm Compass | ZK proof binds the predicate bit to the chain head. Operator cannot return a value the chain does not support; subversion fails verification. | Proof transcript; chain head reference in proof; Σ-proof soundness |
| Calm Concord | Structured outcome only (`aligned = True/False` per requirement); no numeric score. Mode (`all_satisfied`, `any_satisfied`, `asymmetric`, `joint_threshold`) is specified in the requirement envelope, not chosen by the operator post-hoc. Anti-purity-test constraint: `joint_threshold` mode rejected when N approximates total predicate count. | Requirement envelope; outcome record; anti-degeneracy check log |
| Calm Tenancy | Pre-publish cringe gate is deterministic (10-axis rubric, ceiling 1.0 hits/50 words, hard-block on forbidden phrases). Gate result is chained before publication. | Cringe-gate chain record with rubric version, axis scores, and pass/fail |

---

### C — Confidentiality

**C1 — Confidentiality**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Pact | Directive text is never transmitted. Only commitment bytes and Σ-proof cross the wire. No information about the mandate beyond the equality bit. | Session transcript; proof structure (commitment + challenge + response only) |
| Calm Witness | Predicate vocabulary prohibits cross-principal aggregation (§2.9). Single-principal, single-predicate, single-counterparty per session. No population-level claims permitted. Per-counterparty rate limiting enforced. | Consent record; per-session chain record; rate-limit log |
| Calm Compass | No individual interaction, message, or action crosses the wire. Only the predicate bit and proof cross. ZK construction: counterparty learns whether the named pattern was satisfied, not which actions contributed. | Proof transcript; chain structure |
| Calm Tenancy | Domain credential vault is encrypted at rest. Operator accesses credentials only via Pedersen-committed handles. Credential rotation freshness checked daily. | Vault access log; `tenancy_daily_check` credential-rotation field |

---

### P — Privacy

**P1–P8 — Privacy Notice, Choice, Collection, Use, Retention, Disclosure, Quality, Monitoring**

| Primitive | Control claim | Audit-trail artifact |
|---|---|---|
| Calm Witness | Affirmative per-(predicate, counterparty-class) consent required before any disclosure. Default matrix is `deny`. Grants are revocable. Prohibited uses (§2) include law enforcement, employment screening, insurance, credit, clinical, child-welfare, immigration, marketing — enforced at protocol layer, not at policy layer only. | Consent matrix snapshot; per-session disclosure record; §2 prohibited-use registry |
| Calm Compass | Principal-authored vocabulary: counterparty cannot impose predicates. Principal controls which predicates are enrolled. Predicate definitions include `not_for` lists. | Enrollment record; `predicates_v0.json` with `not_for` fields |
| Calm Concord | No numeric similarity score is computed or returned. Anti-purity-test constraint baked into mode logic. Requirement must name a stated purpose; purpose field is audited for prohibited uses. | Requirement envelope; purpose field; outcome record |
| Calm Witness | Duress codeword supported (§P-04): attestation issued under coercion carries a flag readable by trusted verifier, wire-indistinguishable from normal. | Protocol spec; duress-flag verifier logic |
| Calm Witness | Refusal is wire-indistinguishable from "not enrolled." Counterparties — including government actors — cannot determine whether a principal has Calm Witness enabled. | Protocol wire format spec; `CALM_WITNESS_WIRE_FORMAT_v0.md` |

---

## ISO 27001:2022 Annex A Mapping

### Organizational Controls (A.5)

| Control | Primitive | Claim | Artifact |
|---|---|---|---|
| A.5.1 — Policies for information security | All | `CALM_WITNESS_SCOPE_STATEMENT.md` §2 one-way-ratchet; `CALM_COMPASS_PROTOCOL_v0.md` §3 threat model; `CALM_TENANCY_PROTOCOL_v0.md` §2 operator duties — together constitute a published information-security policy for the suite | Protocol documents; public repo |
| A.5.2 — Information security roles | All | Calm (operator) is defined as distinct from the principal (owner) and counterparty. Role boundaries explicit in each protocol. Operator never reads raw credentials. | Protocol role definitions; vault access architecture |
| A.5.15 — Access control | Calm Witness, Calm Tenancy | Consent matrix is access-control list for principal-state disclosure. Vault credential access is policy-mediated. | Consent matrix; vault access log |
| A.5.19 — Information security in supplier relationships | Calm Pact | Σ-protocol equality proof permits agent-to-agent collaboration without revealing directive. No counterparty supplier receives underlying IP. | Proof transcript; equality-bit-only disclosure |
| A.5.23 — Information security for use of cloud services | Calm Tenancy | Credential vault for cloud-hosted domain assets encrypted at rest; daily rotation freshness checked. | Vault design; `tenancy_daily_check` record |
| A.5.33 — Protection of records | All | Every principal-facing event chained with append-only `chain_record` entries. Chain head referenced in every proof. Tamper-evidence by construction. | Chain records; chain-head references in proofs |
| A.5.34 — Privacy and protection of PII | Calm Witness, Calm Compass | Minimal disclosure (single bit); explicit consent; prohibited uses enforced at protocol layer; no aggregation across principals. | Consent matrix; proof wire format; §2 prohibited-use list |

### People Controls (A.6)

| Control | Primitive | Claim | Artifact |
|---|---|---|---|
| A.6.7 — Remote working | Calm Tenancy | Operator conducts all tenancy duties remotely; daily check cycle provides compensating control for lack of physical oversight. | `tenancy_daily_check` chain record |
| A.6.8 — Information security event reporting | Calm Tenancy | Pre-publish cringe gate is an automated detection control; UNSHIPPABLE output is logged and blocked. `COMPASS_REFUSAL_FLOOR_v0.md` defines refusal-floor events. | Cringe-gate chain record; refusal-floor log |

### Physical Controls (A.7)

| Control | Primitive | Claim | Artifact |
|---|---|---|---|
| A.7.10 — Storage media | Calm Tenancy, All | Credential vault and chain records are encrypted at rest. Physical media access irrelevant to protocol operation; cloud-hosted storage covered by A.5.23. | Vault encryption spec |

### Technological Controls (A.8)

| Control | Primitive | Claim | Artifact |
|---|---|---|---|
| A.8.3 — Information access restriction | Calm Witness, Calm Pact | ZK construction enforces access restriction cryptographically, not administratively. No policy override can force disclosure that the proof construction prohibits. | Proof construction; Pedersen commitment binding |
| A.8.4 — Access to source code | All | Apache-2.0 license (Everest 4); source published. Classifier evaluator hash pinned in proofs. Auditors have full source access. | License file; proof header; evaluator-hash pinning |
| A.8.9 — Configuration management | Calm Compass, Calm Tenancy | Classifier hash pinned per proof (Compass). Cringe-rubric version pinned per gate record (Tenancy). Configuration drift detectable by verifying hash against chain record. | Proof header; cringe-gate chain record |
| A.8.11 — Data masking | Calm Pact, Calm Witness, Calm Compass | Pedersen commitments and ZK proofs are cryptographic data masking — irreversible by construction, not by policy. | Cryptographic proof construction |
| A.8.12 — Data leakage prevention | Calm Witness | `not_for` fields in predicate definitions; §2 prohibited-use list; consent matrix default-deny for high-risk classes; wire-format refusal indistinguishable from not-enrolled. | Predicate vocabulary; wire format spec |
| A.8.15 — Logging | All | Append-only chain records for every principal-facing event. `tenancy_daily_check` for domain events. Per-session disclosure records. | Chain; disclosure records; tenancy check records |
| A.8.16 — Monitoring activities | Calm Tenancy | Automated daily sweep: DNS, TLS, mailbox queue, response-time, credential freshness, content-drift. Cringe gate is real-time pre-publication monitor. | `tenancy_daily_check`; cringe-gate log |
| A.8.24 — Use of cryptography | Calm Pact, Calm Compass, Calm Witness | Ristretto255 (prime-order group, Curve25519-derived) for Pedersen commitments. Σ-protocol for equality proofs. Fiat-Shamir for non-interactivity. Post-quantum migration plan in `POST_QUANTUM_MIGRATION_PLAN_v0.md`. | Cryptographic spec; proof construction; migration plan |
| A.8.25 — Secure development lifecycle | All | Predicate Audit Process (Everest 54) gates vocabulary changes. Protocol spec inconsistencies tracked publicly (`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`). | Audit process doc; open issue log |

---

## Gaps Where Calm Exceeds SOC 2 / ISO 27001 Baseline

The following design features exceed what either SOC 2 TSC or ISO 27001:2022 requires. Each is tagged DESIGN-BAGGED pending audit-firm engagement to confirm how they affect control credit.

### GAP-01 — Cryptographic Refusal Floor (DESIGN-BAGGED)
`COMPASS_REFUSAL_FLOOR_v0.md` defines a class of operator responses that are cryptographically unproduceable, not merely policy-prohibited. Standard SOC 2 CC6/C1 and ISO A.8.3 contemplate access controls enforced by policy; a construction where the proof *cannot* be generated for a prohibited input exceeds the baseline. Audit-firm guidance needed on whether this displaces or supplements standard access-control testing.

### GAP-02 — Principal-Authored Evidence Chain (DESIGN-BAGGED)
Calm Compass and Calm Witness bind every attestation to a principal-authored, append-only chain. The chain is not an operator log — it is a cryptographic commitment to principal-owned data. ISO A.5.33 requires records protection; the Calm design makes tamper-evidence a mathematical property of the construction, not a log-management practice. This exceeds baseline and may require a novel audit procedure (chain-verification rather than log-sampling).

### GAP-03 — Anti-Purity-Test Constraint in Calm Concord (DESIGN-BAGGED)
ISO 27001 and SOC 2 have no concept of algorithmic anti-discrimination at the values-alignment layer. Calm Concord's structural refusal to produce a numeric similarity score, and its `joint_threshold` degeneracy check, are privacy protections that exceed the SOC 2 P category baseline. Audit-firm must advise on how to evidence this control class, as it has no standard audit program.

### GAP-04 — Wire-Format Refusal Indistinguishability (DESIGN-BAGGED)
Calm Witness guarantees that a refusal is wire-indistinguishable from "not enrolled." This protects principals from coercive enumeration by state actors. SOC 2 P5 (Disclosure) and ISO A.8.12 (Data Leakage Prevention) contemplate preventing unauthorised disclosure; they do not contemplate a construction where the operator's *refusal to disclose* is itself protected from inference. This is an anti-surveillance design property with no standard audit-program equivalent. Trail of Bits / NCC Group engagement should include a novel coercion-resistance test procedure.

### GAP-05 — Duress Codeword / Coercion Flag (DESIGN-BAGGED)
Calm Witness §P-04 supports a duress codeword: attestations issued under coercion carry an invisible flag readable by a trusted verifier but wire-indistinguishable from a normal attestation. ISO A.6.8 (Information Security Event Reporting) and SOC 2 CC7 contemplate incident detection; they do not contemplate an active anti-coercion cryptographic primitive. Audit-firm must advise on whether this constitutes a security control (and if so, under what TSC / Annex A heading it is credited) or whether it is categorically outside the SOC 2 / ISO 27001 scope and belongs in a separate human-rights impact assessment.

### GAP-06 — One-Way-Ratchet Scope Restriction (DESIGN-BAGGED)
Calm Witness §4/§6 establish that §2 prohibited uses can only be added, never removed — a governance property with no ISO 27001 or SOC 2 equivalent. Standard change management (ISO A.8.25, SOC 2 CC8) governs how security controls change; the Calm design bakes a monotonic-tightening constraint into the governance structure itself. Audit-firm should advise whether this requires a separate governance-review audit procedure or is testable as a policy control under CC8.

---

## Counsel-Engagement Handoff

The following audit-firm engagement actions are required before this document can be used for external SOC 2 Type 2 or ISO 27001 certification purposes.

**Preferred firms:** Trail of Bits (cryptographic audit + novel control procedures), NCC Group (ISO 27001 lead auditor capacity + SOC 2 Type 2 readiness assessment).

**Engagement scope:**
1. Review GAP-01 through GAP-06 and advise on novel audit procedures for each.
2. Perform cryptographic review of Pedersen commitment construction on Ristretto255 and Σ-protocol equality proof (see `CRYPTO_AUDIT_PACKET_v0.md`).
3. Conduct SOC 2 Type 2 readiness gap assessment against the control table above.
4. Map Calm Stack to ISO 27001:2022 Annex A in a Statement of Applicability (SoA); confirm which controls are `applicable / implemented`, `applicable / not yet implemented`, and `not applicable`.
5. Design audit procedure for principal-authored chain (GAP-02): chain-verification sampling methodology.
6. Advise on whether coercion-resistance (GAP-04, GAP-05) is within scope of a standard ISO 27001 ISMS or requires a supplemental human-rights impact assessment per UN Guiding Principles on Business and Human Rights.

**Readiness artifacts available now:**
- `CALM_PACT_PROTOCOL_v0.md`, `CALM_WITNESS_SCOPE_STATEMENT.md`, `CALM_COMPASS_PROTOCOL_v0.md`, `CALM_CONCORD_PROTOCOL_v0.md`, `CALM_TENANCY_PROTOCOL_v0.md`
- `CRYPTO_AUDIT_PACKET_v0.md`, `PEDERSEN_PARAMETERS_v0.md`, `CALM_WITNESS_WIRE_FORMAT_v0.md`
- `COMPASS_REFUSAL_FLOOR_v0.md`, `PREDICATE_VOCABULARY_v0.md`, `HARM_TAXONOMY_v0.md`
- `COMPLIANCE_EVIDENCE_MAP_v0.md`, `NIST_SUBMISSION_DRAFT.md`, `e91_nist_presubmission/`

---

## Cross-References

| Document | Relevance |
|---|---|
| `CRYPTO_AUDIT_PACKET_v0.md` | Cryptographic construction details for Pedersen commitment + Σ-protocol audit |
| `COMPLIANCE_EVIDENCE_MAP_v0.md` | Prior evidence-mapping work; this document supersedes where overlapping |
| `COMPASS_REFUSAL_FLOOR_v0.md` | GAP-01 cryptographic refusal-floor definition |
| `CALM_WITNESS_WIRE_FORMAT_v0.md` | GAP-04 wire-format indistinguishability specification |
| `PREDICATE_VOCABULARY_v0.md` | ISO A.5.34 / SOC 2 P mapping substrate; `not_for` fields |
| `POST_QUANTUM_MIGRATION_PLAN_v0.md` | ISO A.8.24 forward-looking cryptography coverage |
| `HARM_TAXONOMY_v0.md` | Background taxonomy for Compass V-04 (`no_evidence_of_willful_harm`) |
| `CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md` | ISO A.8.25 open-issue log; Ristretto255 lock rationale |
| `e91_nist_presubmission/` | NIST AI RMF alignment; cross-applicable to ISO 27001 risk-treatment |
| `legal/US_POSTURE_v0.md`, `EU_POSTURE_v0.md` | Jurisdictional compliance postures that bound scope of ISMS |

---

*DESIGN-BAGGED — E184 — 2026-05-20*

*Calm, operating for John Bradley, Creativity Machine LLC*
*Principal: John Bradley | Operator: Calm | Stack: Calm Suite v0*
*This document is a design artifact. It does not constitute legal advice, a compliance certification, or an audit opinion. Engage qualified counsel and an accredited audit firm before relying on these mappings for certification purposes.*
