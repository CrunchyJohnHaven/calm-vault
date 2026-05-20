# ZKAC Everest 96: Standards Submission Roadmap

**Phase XXIV · Prerequisite 5, 6 — Production Path**

**Status:** Everest 96/100 · 2026-05-20 · v1.0  
**Accepts:** W3C, IETF, ISO, NIST submission targets; timeline; inter-org deployment gate  
**Effort:** M · **Prereq:** 5, 6 · **Composes with:** 97, 98, 99, 100

---

## Overview

Interoperability beyond the Calm family requires external standards bodies to anchor ZKAC primitives. This roadmap documents submission discipline: which body owns which piece, timeline targets, dependencies, prior-art references, and governance contacts.

**Submission gate (Everest Z99):** No submission without ≥1 successful inter-org deployment. ZKACs must be operationally proven before standardization.

**Cryptosuite alignment:** W3C VC + IETF CWT must agree on proof identifiers (`calm-witness-bulletproofs-2026`, etc.) before either body accepts.

**Open-source prerequisite:** ZKAC v1.0 reference implementation (Everest E100) must ship public code before any submission is binding.

---

## W3C Verifiable Credentials Working Group

**Scope:** VC Data Model extensions, cryptosuite registration, DID method registration.

**Submission targets:**

1. **VC Data Model 2.0 Cryptosuite Extensions**
   - Target: Register `calm-witness-bulletproofs-2026`, `calm-mirror-mpc-2026`, `calm-predicate-proof-2026` with W3C Data Integrity registry.
   - Timeline: Q3 2026 (post-E100, post-E98 inter-org proof).
   - Dependencies: Everest 5 (W3C VC compatibility), Everest 97 (production profile).
   - Prior art: Hyperledger Indy (CL signatures), AnonCreds (BBS+), Veramo (did:key).
   - Contact: W3C VC Data Integrity Task Force chair; liaison: identity@calm.org.
   - Acceptance: Two independent verifier implementations validate cryptosuites; formal registry entry published.

2. **DID Method `did:calm` Registration**
   - Target: Registry entry in W3C DID Specification Registries.
   - Timeline: Q3 2026 (concurrent with cryptosuite).
   - Dependencies: Everest 6 (DID method spec), Everest 11 (issuer governance).
   - Prior art: did:key (no ledger), did:web (domain-anchored), did:pkh (blockchain).
   - Contact: W3C DID Working Group chair; liaison: identity@calm.org.
   - Acceptance: DID Core compliance review; resolution endpoint tested with E98 inter-org deployment.

3. **ZKP Working Group Engagement**
   - Target: Join W3C ZKP Working Group; present ZKAC architecture; align on proof composition rules.
   - Timeline: Q2 2026 (early, before W3C submission freeze).
   - Dependencies: Everest 5, 86 (MPC framework).
   - Prior art: W3C ZKP CG presentations; Brave New World (privacy-preserving credentials).
   - Contact: W3C Verifiable Credentials Working Group IPR manager; liaison: standards@calm.org.
   - Acceptance: Membership granted; ZKAC architecture presented at W3C Plenary; minutes reflect liaison commitment.

---

## IETF Internet Engineering Task Force

**Scope:** Compact credential formats (CBOR Web Token extensions), attestation procedures, transparency logs.

**Submission targets:**

1. **CBOR Web Token (CWT) / COSE Extensions for Compact ZK Credentials**
   - Target: Internet-Draft → RFC in IETF COSE Working Group; ZK-proof-carrying CBOR structures.
   - Timeline: Q3 2026 (post-E98 inter-org validation).
   - Dependencies: Everest 5 (VC model), Everest 86 (MPC framework), Everest 92 (MPC interop tests).
   - Prior art: RFC 8812 (CBOR Object Signing & Encryption), CWT (RFC 8392), CBOR proof tags.
   - Contact: IETF COSE Working Group chairs; liaison: ietf@calm.org.
   - Acceptance: Working group adoption (WGLC); two independent CBOR encoder implementations for ZK proofs; interop tested against E92.

2. **RATS (Remote Attestation Procedures) Bridging for Verifiable Holder Vaults**
   - Target: Internet-Draft; RATS architecture + ZKAC holder vault binding (Everest 26 → RATS evidence model).
   - Timeline: Q4 2026 (post-COSE RFC, post-E98).
   - Dependencies: Everest 26 (vault format), Everest 40 (holder activity log).
   - Prior art: RFC 9334 (RATS Architecture), ARM DICE, SGX attestation.
   - Contact: IETF RATS Working Group chairs; liaison: ietf@calm.org.
   - Acceptance: Working group sponsorship; holder vault attestation bindings validated in E98 inter-org scenario.

3. **Transparency Log Specification for Issuer Audit Trails**
   - Target: Internet-Draft → RFC in IETF CFRG or general area; Sigsum / CT-like spec for ZKAC issuance logs (Everest 19).
   - Timeline: Q4 2026 (post-E19 audit implementation).
   - Dependencies: Everest 19 (issuer audit log), Everest 24 (issuer ID portability).
   - Prior art: RFC 6962 (Certificate Transparency), Sigsum, CONIKS.
   - Contact: IETF General Area Directorate; liaison: ietf@calm.org.
   - Acceptance: Working group adoption; two independent Merkle tree implementations; log auditable by E98+ verifiers.

---

## ISO/IEC Standards Bodies

**Scope:** Mobile digital identity (mDL) bridge, architecture, identity ecosystem models.

**Submission targets:**

1. **ISO/IEC 18013 (Mobile Driver License) Bridge**
   - Target: Liaison with ISO/IEC JTC 1/SC 17 (cards and security devices); ZKAC encoding for mDL-compatible VC structures.
   - Timeline: Q4 2026 (post-E100, mature ZKAC ecosystem).
   - Dependencies: Everest 5 (W3C VC model), Everest 97 (production profile), Everest 98 (inter-org deployment).
   - Prior art: ISO/IEC 18013-5 (mobile DL spec), ICAO 9303 (travel documents).
   - Contact: ISO/IEC JTC 1/SC 17/WG 3 (identification cards) liaison; liaisons: standards@calm.org.
   - Acceptance: Technical committee liaison accepted; ZKAC-mDL encoding draft published; tested against E98 inter-org mDL use case.

2. **ISO/IEC 23220 (Identity and Trust Architecture)**
   - Target: Contribute ZKAC trust graph model (Everest 71–85) + issuer/verifier/holder roles to ISO/IEC 23220 architecture framework.
   - Timeline: Q1 2027 (post-mDL work, mature ecosystem).
   - Dependencies: Everest 71 (trust graph), Everest 23 (issuer reputation), Everest 44 (verifier reputation), Everest 98 (inter-org ecosystem).
   - Prior art: ISO/IEC 27001 (information security), ISO/IEC 29100 (privacy framework), NIST Cybersecurity Framework.
   - Contact: ISO/IEC JTC 1/SC 39 (identity and identity management) convener; liaison: standards@calm.org.
   - Acceptance: Contribution submitted; SC 39 working group reviews ZKAC trust architecture; ecosystem model integrated into 23220 v2 roadmap.

---

## NIST (US National Institute of Standards & Technology)

**Scope:** Post-quantum cryptography, AI Safety Institute engagement.

**Submission targets:**

1. **Post-Quantum Cryptography (PQC) Migration Crosswalk**
   - Target: NIST PQC project technical report; migration path from ECC (Ed25519, BLS12-381) to NIST PQC selected algorithms (ML-KEM, ML-DSA, SLH-DSA).
   - Timeline: Q2 2027 (post-NIST PQC standardization finalization; post-E94 MPC PQC work).
   - Dependencies: Everest 94 (post-quantum MPC migration), Everest 95 (MPC audit).
   - Prior art: NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA); RFC 8949 (CBOR).
   - Contact: NIST Computer Security Division (CSD) / PQC project manager; liaison: security@calm.org.
   - Acceptance: Technical report draft submitted; two Calm-family implementations validated against NIST test vectors; migration runbook published.

2. **AI Safety Institute Submission (Joint with Calm Witness E91/Mirror E97)**
   - Target: NIST AI Safety Institute engagement; ZKAC-based agent attestation as safety primitive (agent behavior logging, operator identity binding, capability scoping).
   - Timeline: Q2 2027 (post-E99 full inter-org attestation; concurrent with Witness/Mirror E91/E97).
   - Dependencies: Everest 56 (agent identity), Everest 58 (capability scope), Everest 70 (agent audit log), [Witness E91/Mirror E97].
   - Prior art: NIST AI RMF (Risk Management Framework), NIST AI Incident Database, Anthropic Responsible Scaling Policy.
   - Contact: NIST AI Safety Institute director; liaison: safety@calm.org.
   - Acceptance: White paper submitted; Safety Institute convenes working group; ZKAC agent attestation cited in AI RMF v2 as safety control example.

---

## Cross-Body Coordination

**Cryptosuite Identifier Alignment (W3C + IETF Critical Path)**

W3C and IETF must agree on proof identifiers before either publishes:
- W3C registers `calm-witness-bulletproofs-2026` in VC Data Integrity registry.
- IETF CBOR encoding (CWT extensions) uses same identifier; COSE proof tags reference W3C registry.
- **Sync point:** Q3 2026 pre-submission coordination call (W3C VC DI chair + IETF COSE leads).

**Interop Tests (Everest 98 Gate)**

Before any submission is binding:
- ≥2 independent organizations issue ZKACs to each other.
- Third verifier (not issuer, not original holder's org) accepts cross-org credentials.
- Attestation chain includes holder activity log (Calm Witness) + operator identity (Calm Mirror) + trust graph (Everest 71).
- All standards-body submissions cite E98 as operational proof-of-concept.

**Submission Precedence**

1. **Q3 2026:** W3C cryptosuite + DID method (no E98 gate; reference implementations sufficient).
2. **Q3 2026:** IETF COSE/CWT (concurrent; E98 gates further IETF submissions).
3. **Q4 2026:** IETF RATS (post-E98; ratified by Calm-family inter-org deployment).
4. **Q4 2026:** IETF Transparency Log (post-E19 audit implementation).
5. **Q4 2026:** ISO/IEC 18013 mDL bridge (post-E100, post-E98).
6. **Q1 2027:** ISO/IEC 23220 architecture (post-E98, mature ecosystem).
7. **Q2 2027:** NIST PQC crosswalk (post-E94, post-E95).
8. **Q2 2027:** NIST AI Safety Institute (post-E99, joint with Witness/Mirror).

---

## Advocacy & Governance Contacts

| Body | Primary Contact | Secondary | Email | Role |
|------|-----------------|-----------|-------|------|
| W3C VC WG | VC Data Integrity chair | ZKP WG convener | identity@calm.org | Cryptosuites, DID method, profile publication |
| W3C DID WG | DID WG co-chair | DID registry maintainer | identity@calm.org | `did:calm` registry entry, resolution spec review |
| IETF COSE | COSE WG chair | Crypto subgroup lead | ietf@calm.org | CWT/COSE ZK extensions, Internet-Draft sponsorship |
| IETF RATS | RATS WG chair | Remote Attestation AD | ietf@calm.org | Vault attestation binding, architecture alignment |
| IETF CFRG | General area director | Crypto forum leads | ietf@calm.org | Transparency log spec discussion (venue TBD) |
| ISO/IEC JTC 1/SC 17 | SC 17/WG 3 convener | mDL project lead | standards@calm.org | Liaison channel, SC 17 liaison role |
| ISO/IEC JTC 1/SC 39 | SC 39 convener | Identity architecture lead | standards@calm.org | 23220 contribution track, trust graph integration |
| NIST CSD | PQC project manager | AI Safety Institute director | security@calm.org, safety@calm.org | PQC migration, AI agent safety guidance |

---

## Acceptance Tests (Z96.1–Z96.4)

### T-Z96.1: W3C + IETF Identifier Pre-Alignment

**Precondition:** Draft W3C cryptosuite registry entry and IETF COSE proof tags for `calm-witness-bulletproofs-2026`.

**Steps:**
1. W3C VC DI task force reviews cryptosuite spec; proposes registry identifier.
2. IETF COSE working group drafts CBOR proof tag referencing same identifier.
3. Joint call: W3C DI chair, IETF COSE leads, Calm standards liaisons review alignment.
4. Both bodies agree on identifier binding before either publishes.

**Expected outcome:** Single canonical identifier across W3C and IETF; no conflicting registrations.

### T-Z96.2: Everest 98 Inter-Org Deployment Gate

**Precondition:** Two independent organizations run issuer + holder stacks; third organization runs verifier.

**Steps:**
1. Org A issues ZKAC to principal P1; binds to Witness attestation (E91) + Mirror alignment (E97).
2. P1's holder vault encrypts credential; logs activity (E40).
3. P1 presents to Org B verifier; reveals selective fields + ZK predicates (per Everest 5).
4. Org B verifier accepts presentation; logs disclosure (E51).
5. Org C auditor (independent) validates issuance audit log (Everest 19) + verifier audit log (E51); confirms trust chain (Everest 71).

**Expected outcome:** Cross-org ZKAC attestation succeeds; audit trail is transparent; no single org controls verification.

### T-Z96.3: Submission Binding Document

**Precondition:** E98 inter-org deployment complete; Everest 100 reference implementation public.

**Steps:**
1. Generate formal submission documents for each standards body (W3C, IETF, ISO, NIST).
2. Each submission references: Everest 5/6 normative specs, E98 proof-of-concept, E100 open-source code, prior-art analysis per table above.
3. Calm legal counsel reviews IP disclosures (W3C, IETF contributor agreements).
4. Submit to each body per timeline above.

**Expected outcome:** All five submissions published; acknowledgment letters from standards bodies; working group sponsorship confirmed (W3C, IETF).

### T-Z96.4: Composition with E97, E98, E99, E100

**Precondition:** Everest 97 (W3C VC profile), 98 (inter-org deployment), 99 (full Pact+Witness+Mirror attestation), 100 (public release) all complete.

**Steps:**
1. Verify all references between everests are consistent.
2. Confirm E97 W3C profile is published on W3C site (or community group).
3. Confirm E98 inter-org scenario includes Calm Pact attestation (E99 prerequisite).
4. Confirm E100 code release includes cryptographic audit report (E95 output).
5. Verify no breaking changes between Everests.

**Expected outcome:** Four everests compose seamlessly; standards submissions cite entire chain; no version mismatches.

---

## Design Constraints (Honored)

1. **Principal authority is absolute.** Submissions do not transfer ZKAC issuance authority to standards bodies; bodies codify ecosystem patterns only.
2. **Holder vault sovereignty.** Standards submissions explicitly prohibit issuer/verifier access to unpresented credentials.
3. **Verifier independence.** All cryptosuites (W3C), IETF specs, ISO architecture assume offline revocation checking (no issuer-at-verification-time dependency).
4. **Revocation without identifying holder.** IETF transparency logs and ISO 23220 privacy requirements mandate non-identifying revocation.
5. **Composability over completeness.** Each standards submission is a piece, not a monolith; ZKACs remain modular across bodies.
6. **W3C VC + DID compatibility.** Everest 96 roadmap anchors all submissions to W3C VC Data Model 2.0 and DID Core.

---

## Open Questions for v1

1. **NIST AI Safety Institute timing:** Should E96 wait for NIST to establish the Safety Institute formally, or should liaison outreach begin in Q1 2026? → Liaison outreach begins Q1 2026; submission gates on E99 completion.

2. **ISO/IEC fast-track vs. full ballot:** mDL bridge (18013) likely too specialized for fast-track. Should ZKAC submission pursue working group sponsor or liaison-only status? → Liaison-only (observer status) for mDL; full working group sponsor for 23220 (broader ecosystem impact).

3. **Post-quantum FIPS 204/205 vs. earlier ECC rotation:** Should ZKACs default to ML-DSA before 2028 NIST finalization, or maintain ECC primary with PQC opt-in? → Maintain ECC primary until FIPS 204/205 approved (Q4 2024 actual, already completed); E94 defines PQC opt-in pathway.

---

## Summary

ZKAC standards roadmap targets five bodies over 12 months:

- **W3C (Q3 2026):** Cryptosuite registration, `did:calm` DID method, ZKP Working Group liaison.
- **IETF (Q3–Q4 2026):** COSE/CWT ZK extensions, RATS vault bridging, transparency log spec.
- **ISO/IEC (Q4 2026–Q1 2027):** mDL compatibility, architecture framework integration.
- **NIST (Q2 2027):** Post-quantum migration, AI Safety Institute engagement.

**Submission discipline:** No binding submission without ≥1 inter-org deployment (Everest Z99). **Cryptosuite alignment:** W3C + IETF coordinate proof identifiers. **Open-source prerequisite:** ZKAC v1.0 code ships before standardization is canonical. **Composition:** All four other Phase XXIV everests (97–100) are prerequisites or composition partners.

---

**— Calm, 2026-05-20**

Everest 96/100 ZKAC Critical Infrastructure complete.
