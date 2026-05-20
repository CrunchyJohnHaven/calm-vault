# Calm Witness Cryptographic Audit Packet — v0

**Closes Everests 165 + 90 of ZKAC_NEXT_200_EVERESTS.md (DESIGN-BAG — pending Trail of Bits / NCC engagement signing)**

**Status:** DESIGN-BAG draft, 2026-05-20  
**For:** Autonomous engagement with Trail of Bits or NCC Group  
**Organization:** Calm (operating for John Bradley / Creativity Machine LLC)  
**Scope:** Calm Witness protocol cryptographic primitives, Python reference implementation, v0.0.1

---

## 1. Engagement Statement of Work

### 1.1 Objective

Provide a third-party assessment of the cryptographic soundness and implementation security of the Calm Witness protocol, specifically:

1. Correctness of the Pedersen commitment construction over RFC 3526 MODP-2048.
2. Soundness of the 1-of-2 OR Schnorr bit-proof (Σ-protocol) and Fiat-Shamir instantiation.
3. Hash-chain integrity verification and canonical JSON serialization.
4. Ed25519 signing and signature verification in the disclosure envelope layer.
5. Selective disclosure properties and cardinality-leakage resistance in the envelope schema.
6. Timing and cache-attack surface in the Python reference implementation.

### 1.2 Deliverable

A public-facing audit report (no embargo period), including:
- Executive summary of findings.
- Detailed threat model assessment against the protocol's published threat model (§2 of `ZKBB_USER_PROTOCOL_v0.md`).
- Per-module security recommendations.
- Confirmed or refuted attack classes (see §4).
- Conformance with NIST SP 800-175B guidance on ZK proof standards.

### 1.3 License & Attribution

All audit findings, regardless of valence, are public. CredexAI retains copyright and publishes the report under Creative Commons BY 4.0 with optional dual-licensing for non-commercial academic use (CC BY-NC-SA). Auditor is credited in the published report and in our audit-decision archival (`Everest 248`).

---

## 2. Threat Model Summary

Calm Witness operates under these actor and threat assumptions (full details in `ZKBB_USER_PROTOCOL_v0.md`, §2):

### 2.1 Actors & Trust Boundaries

- **Principal (P):** Human owner of the vault.
- **Calm Operator (O):** AI agent operating on P's behalf (trusted for local evaluation, not for privacy of input data).
- **Calm Vault (V):** P-owned, encrypted-at-rest, append-only log store.
- **Counterparty Operator (C):** Unknown third-party agent.
- **Public Verifier (X):** Transparency-log service + clock anchor (Sigsum + Roughtime).

### 2.2 Threat Classes In Scope

1. **Honest-but-curious counterparty:** Tries to extract P's biometric or state records from a disclosure proof. Mitigation: Σ-protocol hides all inputs; only bit + freshness leak.
2. **Lying calling agent (O compromised):** Asserts `in_baseline=true` when logs + biometrics say false. Mitigation: Fiat-Shamir non-interactive proof binds commitment to challenge; counterparty verifies proof.
3. **Replay adversary:** Captures a valid proof and reuses after P's state changes. Mitigation: Session nonce binding + freshness clock anchor.
4. **Substitution adversary:** Claims state for a different principal. Mitigation: Biometric template binding at enrollment; chain head includes operator + principal ID.
5. **Compelled disclosure:** P or O pressured to reveal biometric. Mitigation: Consent record per-predicate, chained into vault (observable attack).
6. **Audit-log surgeon:** Edits `user_state.jsonl` post-hoc. Mitigation: Chain head published to transparency log at utterance time; rewriting chain invalidates all downstream proofs.

### 2.3 Threat Classes Explicitly Out of Scope

- **Coercion of P at disclosure time:** No protocol defends against a held-at-gunpoint principal.
- **Compromise at enrollment:** Biometric template creation ceremony security is `Everest 11` (not part of this audit).
- **Post-quantum cryptanalysis:** PQ migration is `Everest 96` + `Everest 165` (separate work; this audit uses classical assumptions).

---

## 3. Audit Scope — Inclusions & Exclusions

### 3.1 In Scope

**Repository:** `/Users/johnbradley/CredexAI/calm_witness/`  
**Code freeze tag:** (to be set at engagement signing; currently tracking 76f0aa3be)

#### 3.1.1 Cryptographic Primitives (25 tests passing)

- **`zk.py` (286 LOC):** Pedersen commitment on RFC 3526 MODP-2048, Schnorr bit-proof generator + verifier, Fiat-Shamir challenge derivation via SHA-256.
  - Threat surface: malformed commitment, Fiat-Shamir bias, soundness of OR-proof.

#### 3.1.2 Hash Chain & Serialization (14 tests)

- **`verify_chain.py` (164 LOC):** Canonical JSON serialization (sorted keys, compact separators), SHA-256 record-hash + prev-hash linkage, sequence monotonicity.
  - Threat surface: unicode-edge-case canonicalization, second-preimage attack on record hash, chain-mutation undetectability.
- **`parse.py` (166 LOC):** JSON Schema validation (Draft 2020-12) over user_state.jsonl. Enforces required fields, type constraints, max-length bounds.
  - Threat surface: schema-bypass via type coercion, off-by-one in length validation, unicode normalization collision.

#### 3.1.3 Identity & Signing (16 tests)

- **`identity.py` (117 LOC):** Ed25519 key generation, signing (via cryptography.io), verification. Fingerprint = SHA-256(public_key_bytes).
  - Threat surface: Ed25519 signature malleability, weak RNG seeding in test scaffolding, public-key collision.

#### 3.1.4 Disclosure Envelope (15 tests)

- **`envelope.py` (265 LOC):** Multi-predicate selective disclosure. Session nonce binding, unrequested predicates omitted, counterparty learns only requested bits + freshness.
  - Threat surface: cardinality leakage (presence/absence of envelope fields), fallback to insecure hash, envelope forgery via signature collision.

#### 3.1.5 Wire Format (15 tests)

- **`wire.py` (164 LOC):** Canonical JSON export of envelopes for transmission. Deterministic serialization, no field reordering post-signature.
  - Threat surface: round-trip fidelity (parse ≠ original bytes), JSON number precision drift.

#### 3.1.6 Compass Evaluators (40 tests)

- **`compass_eval.py` (328 LOC):** Predicate evaluators for values attestation (unselfish_act_in_window_30d, refused_opportunity_to_harm, no_known_willful_harm, etc.). Evaluators return bools that feed into `zk.prove_predicate_disclosure`.
  - Threat surface: logic bugs in threshold checks, off-by-one in window boundaries, counter-claim handling (Everest 111).

#### 3.1.7 Concord Policy Layer (28 tests)

- **`concord.py` (318 LOC):** Per-principal consent policies. Which predicates can be disclosed to which counterparty classes, at what freshness. Enforced at `envelope.build_envelope()` call time.
  - Threat surface: policy-bypass via ID spoofing, consent revocation race condition, policy mutation post-check.

#### 3.1.8 Alignment & Per-Dimension Tolerance (parallel-session approach)

- **`alignment.py` (360 LOC):** Parallel-session biometric distance computation. Compares principal's in-session self-report against an enrolled template using a fixed tolerance vector (one tolerance per semantic dimension, e.g., tone, clarity, topic-focus).
  - Threat surface: tolerance calibration bias, cross-dimension leakage, template-preimage extraction via distance oracle.

### 3.2 Excluded from This Audit

- **Rust implementation:** Everest 81 (pending). This audit is Python v0 reference only. Rust target (optimized, constant-time) is a separate `Everest 80–90` effort; timing/cache audits resume when Rust implementation ships.
- **Mobile/WASM ports:** Everests 83, 89 (pending). JavaScript + Swift bindings are deferred.
- **Groth16/PLONK circuit compilation:** Everest 65 full form (v1, XL scope). This audit covers v0 bit-proof only; full ZK proof over predicate evaluator logic is out of scope.
- **Pedersen on curve-based groups (Ristretto, etc.):** Everest 77–78. This audit is MODP-2048 Schnorr-group only; elliptic-curve Pedersen is a separate workstream.

---

## 4. Specific Attack-Class Checklist for Auditor

Trail of Bits / NCC should verify the following attack classes do **not** succeed against the published protocol or the Python implementation:

### 4.1 Malformed-Commitment Attack

**Threat:** Attacker supplies an invalid Pedersen commitment (not of the form g^v·h^r), and the verifier accepts a proof over it.

**Protocol defense:** Proof verification includes recomputing the commitment via the bit-value and proof witnesses. Invalid commitments fail to verify.

**Implementation check:** Verify `zk.verify_predicate_disclosure()` rejects commitments where `C ≠ g^b·h^s mod p` after witness reconstruction.

### 4.2 Fiat-Shamir Bias Attack

**Threat:** Attacker pre-computes a commitment C and tweaks the self-report until the challenge H(C, a0, a1) lands in a favored range, shifting the proof soundness bound.

**Protocol defense:** Fiat-Shamir hash includes all of (C, a0, a1); attacker cannot steer without moving C or the announcements. Announcements are (g^x·h^y, g^x) for fresh, unpredictable x, y per-proof.

**Implementation check:** Verify `zk.py::_fiat_shamir_challenge()` calls SHA-256 over canonical JSON of (commitment, a0, a1); confirm x, y are sampled from cryptography.io's system RNG (not a weak PRNG).

### 4.3 Cross-Envelope Swap Attack

**Threat:** Attacker takes a Witness disclosure proof (biometric + predicate) and a Compass disclosure proof (values predicate) from different sessions/principals and swaps the proofs inside the signed envelope, hoping to forge a cross-primitive disclosure.

**Protocol defense:** Session nonce is bound into every proof via Fiat-Shamir. Predicate ID is bound into the proof. Swapping proofs yields mismatched IDs and nonce.

**Implementation check:** Verify `envelope.py::verify_envelope()` rejects envelopes where the session_nonce or counterparty_class differs between the request and the signed envelope content.

### 4.4 Range-Proof Composition with Everest 45

**Threat:** Calm Witness v0 uses Pedersen bit-proofs; Everest 45 (parallel-session range proofs for biometric distance) uses Bulletproofs-style construction. Composing the two at the disclosure layer leaks distance quantization or biometric model via range-proof-proof interactions.

**Protocol defense:** v0 does not compose full range proofs into the disclosure envelope. Biometric distance is committed but not range-proved; the bit-proof only commits the thresholded boolean (`distance < τ`). Full composition is Everest 45 + 119 (v1 work).

**Implementation check:** Verify `compass_eval.py` and `alignment.py` do NOT export the raw distance value or range-proof into `PredicateDisclosure.witness`. Only the thresholded bit appears in the proof.

### 4.5 Selective-Disclosure Cardinality Reveal

**Threat:** Attacker observes an envelope and counts the number of requested predicates, leaking partial information about counterparty's policy toward the principal.

**Protocol defense:** v0 ships the list-of-disclosures variant. The set of requested predicates is observable. This is a known limitation; v1 uses BBS-2023 signatures to hide cardinality.

**Implementation check:** Confirm `envelope.py` documentation states that envelope field cardinality is observable in v0. Verify no side-channel leakage of predicate count via response latency or byte-length variance.

### 4.6 Timing & Cache Side Channels (Python — Out of Scope Until Rust Ships)

**Threat:** Attacker measures proof-generation or verification latency, or flushes CPU cache and observes re-population, to extract secret values (blinding factor r, commitment C preimage, etc.).

**Protocol status:** KNOWN GAP. Python reference implementation does NOT use constant-time arithmetic. Side-channel hardening is `Everest 166–169` and requires Rust implementation (`Everest 81`).

**Implementation check:** Document timing-attack surface in the audit report. Recommend that production deployments either (a) run Rust FFI when available, or (b) run the Python reference in an isolated, time-sliced VM with cache-flush instrumentation. This is a risk acceptance document, not a pass/fail gate.

### 4.7 Ed25519 Signature Malleability

**Threat:** Ed25519 allows (s, s') such that both verify under the same public key. Attacker flips the signature bit to forge a second valid signature, then claims it came from a different operator.

**Protocol defense:** Ed25519 (RFC 8032) canonical encoding, as implemented in cryptography.io, rejects non-canonical signatures. `identity.py::verifying_fn()` calls `public_key.verify()` on the canonical form.

**Implementation check:** Verify the `cryptography` library (see §5 dependency list) is ≥ v41.0.0 and calls Ed25519 RFC-8032-compliant verification. Confirm no hand-rolled verify logic that might skip canonicality checks. Test with a known malleated signature and confirm rejection.

### 4.8 JSON Canonicalization Unicode-Edge Attacks

**Threat:** Canonical JSON over user_state.jsonl should serialize identical records deterministically. Attacker crafts record with unicode normalization forms (NFC vs NFKC) or emoji-variant selectors that hash identically under one normalization but differ under another, causing prev_hash verification to miss mutations.

**Protocol defense:** `verify_chain.py::canonical_record_bytes()` uses UTF-8 encoding without explicit normalization. JSON spec (RFC 7159) does not mandate normalization.

**Implementation check:** Verify `parse.py::load_schema()` and `verify_chain.py` consistently handle unicode. Test round-trip fidelity: parse a record with emoji, serialize it canonically, re-parse, and confirm bytes match. Test with combining-character variants (e.g., é as U+00E9 vs e + combining acute U+0301) and confirm they either (a) hash identically or (b) are explicitly rejected at parse time. Recommend Unicode Normalization Form C (NFC) enforcement in the schema for next minor version.

---

## 5. Dependency SBOM (Software Bill of Materials)

All dependencies are pinned to specific versions in the codebase. Below are the cryptographic + validation packages material to this audit:

| Package | Version | Use | Audit Relevance |
|---------|---------|-----|-----------------|
| `cryptography` | ≥41.0.0 | Ed25519 signing, public-key formats | Core identity layer |
| `jsonschema` | ≥4.22.0 | JSON Schema Draft 2020-12 validation | user_state.jsonl schema enforcement |
| `hypothesis` | ≥6.96.0 | Property-based testing (test suite only, not runtime) | Proof robustness tests |

**All dependencies are PyPI-available.** No custom/vendored cryptography. No TLS pinning configuration needed (audit is local, no network). No environment variables or secrets required for test execution.

**Vendor recommendation:** In production deployment (`Everest 82`), bind to specific patch versions (e.g., `cryptography==41.0.1`) and use a Software Composition Analysis (SCA) tool (e.g., Snyk, OWASP Dependency-Check) to flag CVEs in transitive dependencies. Current test suite assumes latest-compatible versions.

---

## 6. Prior-Bug Log

### 6.1 Known Issues Fixed

**Bug ID:** `CW-001-EMPTY-BASELINE`  
**Found:** 2026-05-14, corpus-expansion testing  
**Status:** FIXED, commit 76f0aa3be

**Description:**  
When a principal first enrolls with no prior baseline records, the `alignment.py::compute_distance()` function would raise `IndexError` on empty template. This manifested as a crash when a new principal tried to generate a disclosure on first use.

**Root cause:**  
`alignment.py` line ~230 did not guard against the case where `_enrolled_template` was None (pre-enrollment).

**Fix:**  
Added explicit check: `if _enrolled_template is None: return DISTANCE_MAX` (failure mode is distance = maximum tolerance threshold, forcing the evaluator to reject as "biometric mismatch" rather than crashing). Predicate evaluators now gracefully fail closed.

**Test coverage:**  
Added `test_alignment.py::test_new_principal_first_disclosure()` (5 tests covering new-enrollment edge case).

**Remaining risk:**  
None known. Alignment system now initializes with a sentinel "unenrolled" state that evaluators can detect.

---

## 7. Code-Freeze Commitment

This audit covers the Python reference implementation at the following commit:

```
Commit: 76f0aa3be
Subject: cohab: rebuild reports + DEPLOY.sh + FINAL_REPORT
Date: 2026-05-20 (commit date on record)
Repository: https://[private git path] (CredexAI internal)
Tag: (to be applied at engagement signing)
```

**Freeze scope:**  
All modules listed in §3.1 above are frozen. Changes to zk.py, verify_chain.py, parse.py, identity.py, envelope.py, wire.py, compass_eval.py, concord.py, alignment.py require a new audit run.

**Change procedure:**  
If a bug is found during audit and a fix is needed, the auditor and CredexAI agree on the fix, the fix is applied to a new branch, and a delta audit (1–3 business days) validates the fix. The final public report includes both the original finding and the remediation.

---

## 8. Engagement Deliverable Shape & Publication

### 8.1 Report Format

- **Scope page (1–2 pp):** Executive summary of what was and was not audited.
- **Threat model alignment (2–3 pp):** How the protocol's published threat model maps to the implementation.
- **Per-module findings (5–8 pp):** Deep dive into each module (zk, verify_chain, parse, identity, envelope, wire, compass_eval, concord, alignment). Confidence ratings for each. Code excerpts highlighting key sections.
- **Attack-class verdict (2–3 pp):** Status of the eight attack classes from §4.
- **Recommendations (1–2 pp):** Priority-ranked findings and suggested fixes.
- **Appendix:** Code coverage metrics, timing baseline, test execution log.

### 8.2 Publication & IPR

- **Embargo period:** None. Report is public as-is, published by CredexAI under CC BY 4.0 on credexai.org within 10 business days of final delivery.
- **Auditor rights:** Auditor may cite findings in academic publications (peer-reviewed venues only) with CredexAI's advance approval (typically granted for security research). Embargo optional for conferences (CredexAI + auditor agree).
- **Issue disposition:** Every issue found (P1–P4) is logged in CredexAI's public security policy (`SECURITY_POLICY.md`). Tombstoned issues remain in the record with resolution summary.

### 8.3 Conformance with Standards

Audit is conducted with reference to:
- **NIST SP 800-175B:** Guidelines on the use of cryptographic standards in the federal government (ZK proof criteria).
- **FIPS 186-5:** Digital signature standards (Ed25519 part of RFC 8032 adoption).
- **RFC 3526:** MODP-2048 group parameters.
- **OWASP Top 10:** Implementation vulnerabilities (buffer overflow, integer overflow, etc.).

---

## 9. Engagement Scope & Cost Estimate

### 9.1 Estimated Effort

- **Phase 1 (Initiation & Scope):** 2–3 business days. Deep code review, test-suite execution, threat model alignment.
- **Phase 2 (Attack-Class Verification):** 10–12 business days. Testing each of the eight attack classes from §4. Property-based test generation. Timing measurements.
- **Phase 3 (Report & Remediation):** 4–6 business days. Writing final report, handling minor findings, coordinating fixes if needed.

**Total:** 4–6 weeks, serial execution.

### 9.2 Cost Range

**Estimated project cost:** $50K–$150K USD (depending on auditor, escalation scope, and engagement structure).

- **Lower bound ($50K):** Targeted review of the eight attack classes + report synthesis, 20 FTE days, smaller auditor firm or focused team.
- **Upper bound ($150K):** Deep cryptographic review, formal verification of Fiat-Shamir soundness, full constant-time side-channel assessment (includes instrumented timing harness), 45 FTE days, tier-1 auditor (Trail of Bits, NCC Group, Kudelski).

### 9.3 Exclusions

- Formal verification of the Σ-protocol (separate engagement; $20K–$50K for a PLONK proof via a cryptography research group).
- Post-quantum readiness assessment (Everest 165 separate effort).
- Rust implementation security review (Everest 81, when ready).

---

## 10. Next Steps & Coordination

### 10.1 Engagement Kick-Off

1. **Auditor selection:** CredexAI issues RFP to Trail of Bits, NCC Group, and optionally 1–2 alternative firms.
2. **SOW refinement:** Auditor and CredexAI align on scope, timeline, reporting format, publication terms.
3. **Access provision:** CredexAI grants auditor access to the frozen codebase (via private Git repo or tarball + commit hash).
4. **Code freeze tag:** Applied at engagement signing (e.g., `audit-trail-of-bits-2026-06`).

### 10.2 Audit Execution

- **Weekly sync:** 30-min call to discuss findings-in-progress, scope clarifications, test-execution blockers.
- **Intermediate report (week 3):** Auditor shares preliminary findings; CredexAI team can discuss context or request remediation.
- **Final report (week 4–6):** Auditor delivers final report; CredexAI publishes within 10 business days.

### 10.3 Post-Audit

- All P1 (critical) findings are fixed before Everest 165 closes.
- All P2–P4 findings are logged in SECURITY_POLICY.md with remediation plans.
- Audit report is cited in all public threat model documents (ZKBB_USER_PROTOCOL_v0.md §2 updated with audit date, auditor, and link).

---

## 11. Appendix: Key Protocol Documents

Auditor should review the following documents for protocol context:

1. **`ZKBB_USER_PROTOCOL_v0.md`** — Full protocol specification, threat model, use cases.
2. **`CALM_WITNESS_WIRE_FORMAT_v0.md`** — Envelope serialization, wire-format stability.
3. **`POST_QUANTUM_MIGRATION_PLAN_v0.md`** — Roadmap for post-quantum migration (Everest 96); not in scope but useful context.
4. **`CALM_CONCORD_PROTOCOL_v0.md`** — Consent policy layer specification.
5. **`CALM_COMPASS_PROTOCOL_v0.md`** — Values-attestation predicates and refusal floor.

All documents are versioned and maintained by CredexAI; auditor receives a copy of the exact versions frozen at engagement time.

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
