# Everest 165 — Named-Firm Cryptographic Audit (Trail of Bits Primary)

**SUMMIT 165 of the Calm Umbrella unified registry · phase XI — harm-avoidance predicates → phase XVIII — production, composition, governance.**

**DESIGN-BAGGED · institutional follow-through — actual audit engagement is multi-month serial execution.**

**Status:** DESIGN-BAG, 2026-05-20  
**Organization:** Calm (operating for John Bradley / Creativity Machine LLC)  
**Tier:** ZKAC + Calm Witness cryptographic soundness audit  
**Acceptance:** T-E165.1 through T-E165.5 gate (below)

---

## Why Trail of Bits

Trail of Bits (ToB) is the named-firm cryptographic audit provider for ZKAC v0.0 and Calm Witness v0.1, selected for three specific competencies:

1. **ZK primitives & curve cryptography.** Trail of Bits' 2021–2025 engagement history on Pedersen commitments, Bulletproofs, and Schnorr Σ-protocols across Ethereum, Cosmos, and Zcash-adjacent projects. `zk.py` (Pedersen on MODP-2048 + Schnorr bit-proof + Fiat-Shamir) is their native domain.

2. **Multi-round ZKAC composition.** The protocol composes Calm Witness (state-attestation primitives) + ZKAC alignment (values-disclosure predicates) + optional Calm Pact (directive-equality proofs). Trail of Bits has audited multi-layer ZK stacks (e.g., StarkNet + application circuits). They know the integration attack surface.

3. **Production deployment track record.** Unlike boutique audit firms, Trail of Bits maintains a public remediation database and publishes open audit reports (no embargo). The engagement terms below honor that standard-setting posture: findings are public from utterance.

This is the principal audit engagement. Everest 90 (third-party audit prep) and Everest 184 (sister Calm Witness compliance audit, pending) are parallel workstreams; E165 is the load-bearing cryptographic arbiter.

---

## Audit Scope

### Core Primitives

**Pedersen commitment (Everest 44):** Correctness of g^v · h^r construction on RFC 3526 MODP-2048. Hiding, binding, homomorphic properties verified against formal spec. Python reference (`calm_witness/zk.py`, 286 LOC) + Rust production implementation (`calm-witness` crate).

**Schnorr Σ-PoK (Everest 101):** Bit-proof (1-of-2 OR) for selective disclosure. Soundness under Fiat-Shamir hash function (SHA-256 over canonical JSON commitment + announcements). No soundness degradation from challenge reuse across proofs.

**Range proofs (Everest 45):** Bulletproofs-style range proofs for biometric distance within tolerance τ. Full composition with Pedersen openings. Ristretto255 track (Everest 45b) audited separately if migration lands before v1.0.

**Fiat-Shamir instantiation:** Challenge derivation binds all of (commitment, a₀, a₁, session_nonce, predicate_id, counterparty_class) to resist challenge-pre-computation and cross-proof swapping attacks.

**Hash-chain integrity (Everest 28):** Canonical JSON serialization over `user_state.jsonl` with prev-hash linkage. Unicode normalization edge cases, second-preimage resistance, mutation undetectability. Sigsum transparency-log anchoring of chain heads.

**Ed25519 operator identity (Everest 104b):** Identity establishment + key rotation. Signature verification RFC 8032 canonical form. No malleability exploits.

**Disclosure envelope layer (Everest 67, 102):** Selective disclosure of predicates without revealing unused predicates or chain context. Session nonce binding. Cardinality-leakage analysis (known limitation in v0; BBS-2023 signature hidden-cardinality is v1 work).

**Values-vector commitments (Everest 122):** Pedersen commitment to 10-dimension v0 values vector. Per-dimension or aggregated commitment strategy TBD in spec; both forms audited if deployed.

**Alignment ZK circuit (Everest 138):** Bounded Euclidean distance in 10-dimension hypercube without revealing either vector. Circuit composition with Calm Witness state-attestation proof. Gate count, soundness, and witness structure reviewed.

**Predicate-evaluator bridge (Everest 103):** Safe composition between high-level predicate logic (Python evaluators) and cryptographic proofs (Σ-protocol + range proofs). Off-by-one bugs, threshold-logic flaws, window-boundary errors in time windows.

---

### Threat Model Coverage

**Honest-but-curious counterparty:** Extracts private values or biometric data from a disclosure proof. Auditor verifies Σ-protocol zero-knowledge property prevents all leakage beyond the requested bit + freshness metadata.

**Compromised operator (O):** Asserts in_baseline=true when logs and biometrics show false. Fiat-Shamir binding prevents non-interactive proof forgery even if O controls both commitment and challenge (via session nonce + predicate ID injection into hash).

**Replay attacker:** Captures a disclosure proof and replays after state change. Session nonce + chain-head freshness timestamp render replays detectable; auditor verifies nonce uniqueness is enforced and freshness window is not exploitable (e.g., via clock-skew).

**Principal substitution:** Claims state for a different principal's chain. Biometric template binding at enrollment (Everest 11, separate audit in E90) + operator identity + principal ID in chain head prevent swapping.

**Selective-predicate forgery:** Attacker omits unfavorable predicates from disclosure envelope and forges a proof that they were evaluated and passed. Auditor verifies that the Σ-protocol proof binds the exact set of evaluated predicates; omission is detectable.

**Compelled disclosure under duress:** No protocol defends against a held-at-gunpoint principal. Auditor documents this as out-of-scope and verifies that the protocol logs duress-signal records (Everest 85) which are observable on-chain if coercion is later disclosed.

**Unicode canonicalization collision:** Attacker crafts records with NFC vs NFKC variants or emoji-selector combinations that round-trip differently, causing prev_hash chains to mutate silently. Auditor tests round-trip fidelity and either confirms deterministic canonicalization or requires explicit NFC enforcement in v0.0.1.

**Timing side channels:** Pedersen commitment generation, Fiat-Shamir hash, proof verification latency leak blinding factors. KNOWN GAP in Python reference implementation. Production deployments use Rust FFI or constant-time libraries. Rust implementation audit deferred to separate Everest 81 engagement.

---

### Code Under Audit

**Primary repository:** `calm-witness/` (CredexAI internal Git; access via private URL or tarball).  
**Code freeze commit:** 76f0aa3be, dated 2026-05-20. Frozen at engagement signing; new commits require delta audit.  
**Modules in scope (Python reference + Rust production when ready):**

- `zk.py` (286 LOC): Pedersen, Schnorr bit-proof, Fiat-Shamir.
- `verify_chain.py` (164 LOC): Hash-chain verification, canonical JSON.
- `parse.py` (166 LOC): JSON Schema validation (RFC 2020-12).
- `identity.py` (117 LOC): Ed25519 key gen, signing, verification.
- `envelope.py` (265 LOC): Selective disclosure envelope.
- `wire.py` (164 LOC): Wire-format serialization.
- `compass_eval.py` (328 LOC): Predicate evaluators (unselfish_act, no_willful_harm, etc.).
- `concord.py` (318 LOC): Consent-policy enforcement.
- `alignment.py` (360 LOC): Biometric distance computation.
- Full Rust implementation (once Everest 81 ships).

**Test suite:** 120+ tests covering unit + integration. Hypothesis-based property tests for Σ-protocol randomness. Known issue `CW-001-EMPTY-BASELINE` (empty template IndexError) fixed in commit 76f0aa3be; auditor verifies fix.

**Excluded:** Mobile/WASM ports (Everests 83, 89), Groth16/PLONK full-circuit form (Everest 65, v1), Ristretto-based Pedersen (Everest 77–78, separate track).

---

## Engagement Terms

**Black-box-first approach:** Auditor begins with the frozen codebase + specification packet (per Everest 90); no live code walkthroughs initially. Questions are logged; CredexAI engineer responds within 24 hours.

**White-box phase (week 2+):** Auditor transitions to source-level review. CredexAI principal engineer attends 30-min syncs for context but does not guide the audit. Architecture walk-throughs recorded for future reference.

**Open findings & remediation:**
- All findings (P0–P4) are published in the final report with Foundation response inlined.
- **Critical findings (P0):** Remediation committed to before v1.0 release. Commit hash and fix summary published.
- **High findings (P1):** Remediation committed to before production deployment (Everest 99). 90-day max timeline.
- **Medium/Low (P2–P4):** Logged in security policy; roadmap integration planned.

**No NDA on findings ceiling:** Trail of Bits may publish findings in peer-reviewed venues (ACM CCS, Eurocrypt, etc.) with CredexAI advance approval (granted for security research). Conference embargo negotiable (CredexAI + ToB agree per-venue).

**Principal-protective posture:** Every published critical finding includes a Foundation public response (not rebuttal — acceptance, remediation plan, or risk-acceptance statement). Transparency is the trust vector.

---

## Audit Packet

Per Everest 90, the audit packet contains 12 items:

1. **Protocol spec** (`ZKBB_USER_PROTOCOL_v0.md`, `CALM_ZKAC_EVERESTS_106_305.md`).
2. **Threat model** (consolidated from Everests 1, 9, 21, 23, 85, 94, 151).
3. **Cryptographic specs** (Everests 44, 45, 46, 65, 101, 104b, 122, 128, 138).
4. **Code** (frozen commit 76f0aa3be; SHA-pinned deps; Cargo.lock + requirements.txt).
5. **SBOM** (SPDX format; cryptographic + validation packages pinned).
6. **Test vectors** (10,000+ known-answer pairs across Pedersen, range proofs, Σ-protocol, alignment circuits).
7. **Fuzzer corpus** (90 days historical crashes, classified by severity; aborting fuzzer run included).
8. **Prior bug log** (`CW-001` documented with fix commit; no open security bugs at freeze).
9. **Architecture diagrams** (trust boundaries, key custody, vault encryption topology).
10. **Live test infrastructure** (dev Sigsum endpoint, dev Roughtime anchor, test-mode operator binary).
11. **POC designation** (Calm Foundation engineer with 24-hour SLA for audit questions).
12. **Supplementary docs** (values-predicate semantics, harm taxonomy, consent-class definitions, deployment guides).

Tarball + index provided at engagement signing.

---

## Specific Attack Classes (Audit Checklist)

Trail of Bits to verify these attacks **do not succeed**:

### A-1: Malformed Commitment Acceptance
Attacker supplies commitment C not of form g^v·h^r; verifier accepts proof over it. **Defense:** Proof verification recomputes C; invalid commits fail. **Check:** `zk.verify_predicate_disclosure()` rejects C where reconstruction fails.

### A-2: Fiat-Shamir Challenge Pre-Computation
Attacker pre-computes commitment and tweaks self-report until challenge H(C, a₀, a₁) lands in favorable range. **Defense:** Challenge includes all of (C, a₀, a₁, nonce); attacker cannot steer without moving C or announcements. Announcements are fresh per-proof. **Check:** `_fiat_shamir_challenge()` calls SHA-256 over canonical (commitment, a₀, a₁); RNG is `cryptography.io` system RNG.

### A-3: Cross-Envelope Proof Swap
Attacker takes a Witness proof + a Compass proof from different sessions and swaps proofs inside envelope. **Defense:** Session nonce + predicate ID bound into every proof. Swapping yields mismatch. **Check:** `envelope.verify_envelope()` rejects where session_nonce or counterparty_class differs.

### A-4: Cardinality Leakage in Selective Disclosure
Attacker counts requested predicates in envelope, inferring counterparty's policy. **Defense:** v0 acknowledges this as known limitation; only cardinality of requested set is observable. BBS-2023 hidden-cardinality is v1. **Check:** Confirm envelope documentation states this; no side-channel leakage via latency or byte-length variance.

### A-5: Range-Proof Distance Leakage
Composing bit-proof (Everest 101) + range proofs (Everest 45) leaks distance quantization or biometric model. **Defense:** v0 does NOT compose full range proofs into disclosure. Distance is committed but not range-proved; only thresholded boolean appears. **Check:** `compass_eval.py` and `alignment.py` do not export raw distance or range-proof into `PredicateDisclosure.witness`.

### A-6: Ed25519 Signature Malleability
Ed25519 allows (s, s') such that both verify under same key; attacker flips signature to forge second valid signature. **Defense:** RFC 8032 canonical encoding rejects non-canonical signatures. `cryptography.io` ≥41.0.0 enforces this. **Check:** Verify `cryptography` version and test with known malleated signature (should reject).

### A-7: Unicode Normalization Collision
Attacker crafts records with NFC vs NFKC or emoji variants that hash identically under one form but differ under another, mutating chain silently. **Defense:** `verify_chain.py::canonical_record_bytes()` uses UTF-8 consistently; test round-trip fidelity. **Check:** Parse record with emoji; serialize canonically; re-parse; confirm bytes match. Test combining-character variants (é as U+00E9 vs e + combining-acute); either hash identically or reject at parse time.

### A-8: Alignment Proof Forgery via Known Tolerance
Principal knows counterparty's published tolerance vector and fits self-reports to maximize alignment. **Defense:** Documented defenses include drift-rate caps, witness-attestation requirements, age-weighted evidence. Auditor to validate defense completeness or flag as open research question. **Check:** Test suite includes adversarial-fitting scenarios; drift detector tests.

---

## Timeline & Deliverables

**Phase 1 (Weeks 1–2): Initiation & Scope**
- Deep code review; test-suite execution; threat-model alignment.
- Auditor logs clarification questions; CredexAI responds via video + written.
- **Deliverable:** Scope confirmation memo (1 page).

**Phase 2 (Weeks 2–4): Attack-Class Verification**
- Test each of the eight attack classes above; property-based test generation.
- Timing measurements (latency baseline, cache-miss patterns); document timing-attack surface.
- **Deliverable:** Preliminary findings report (internal; lists all open issues with severity + reproducibility).

**Phase 3 (Weeks 4–5): Report & Remediation**
- CredexAI and auditor coordinate on minor findings; critical findings trigger remediation branches.
- Final report written; findings formatted per NIST SP 800-175B + OWASP guidelines.
- **Deliverable:** Public audit report (~20–30 pp) with executive summary, per-module findings, attack-class verdicts, recommendations, appendix.

**Phase 4 (Post-audit): Remediation & Publication**
- CredexAI fixes critical findings (2–4 weeks); auditor performs delta audit (1–3 days).
- Report published by Calm Foundation under CC BY 4.0 on credexai.org within 10 business days of final delivery.
- Foundation response document published inline.

**Total engagement:** 6–8 weeks, serial execution. 30–45 FTE days.

---

## Cost Estimate & Compensation

**Named-firm scope (Trail of Bits or equivalent):** $150K–$500K USD depending on:
- Escalation scope (critical findings requiring extended remediation research).
- Formal-verification depth (Σ-protocol soundness proof separate engagement; ~$50K additional).
- Timing/side-channel instrumentation (full constant-time assessment with cache-flush harness).

**Budget recommendation:** $250K–$350K for black-box + white-box + open report + delta audit.

**Payment structure (industry standard):**
- 30% upfront at engagement signing.
- 50% on preliminary findings delivery (end of week 3).
- 20% on final report delivery.

**Expenses:** Auditor travel (if on-site walk-throughs desired; typically virtual), cloud infrastructure for testing (auditor-managed).

---

## Acceptance Criteria (Gate: T-E165.1..5)

**T-E165.1: Audit Engagement Letter Signed**
- Trail of Bits (or named-firm alternate) has signed engagement letter.
- Scope, timeline, cost, publication terms all agreed.
- Code freeze tag applied to frozen commit.
- Calm Foundation engineer designated as POC.

**T-E165.2: Preliminary Findings Memo (Week 2–3)**
- Auditor has executed at least 4 of 8 attack-class tests.
- No blockers in codebase access or test infrastructure.
- Initial severity assessment completed.

**T-E165.3: Audit Execution Completion (Week 4–5)**
- All 8 attack classes tested; findings compiled.
- Timing/side-channel baseline documented.
- Auditor has reviewed all 9 in-scope modules.

**T-E165.4: Final Report Delivered & Published**
- Public audit report published on credexai.org under CC BY 4.0.
- Foundation response document inline with report.
- All P0 (critical) findings have committed remediation (with fix commit hash if already landed).

**T-E165.5: Remediation Closure & Follow-Up**
- All critical findings fixed (or risk-acceptance documented).
- High findings on remediation roadmap (90-day target).
- Delta audit (if fixes required) completed and findings merged into final report.
- No open security blockers for Everest 99 (production deployment).

**Gate script:** `everest_165_trail_of_bits_audit_gate.py` (TBD; chains T-E165.1..5 verifications).

---

## Composition with Parallel Summits

**E90 (Third-Party Audit Prep):** E165 consumes the audit packet built in E90. E90 is the enabler; E165 is the execution. Serial dependency.

**E184 (Compliance & Regulatory Audit):** Sister summit in Phase XII. E184 is the legal/regulatory audit; E165 is the cryptographic audit. Parallel execution permitted; findings may overlap (e.g., consent-layer compliance requires crypto correctness). Cross-team coordination on findings that span both.

**E90 → E165 → (critical findings remediation) → E99 (Production Deployment):** Critical path. E165 must complete and critical findings remediate before production goes live.

**E100 (Third-Party Verification & Deployment):** Downstream. After audit closes, independent verifier (not Trail of Bits) performs a secondary verification on live deployment. E100 assumes E165 has cleared the cryptographic bar.

---

## Why This Matters

The Calm Witness + ZKAC stack makes cryptographic claims about state attestation and values alignment. Those claims are only credible if an independent third party with deep cryptographic expertise (Trail of Bits' Pedersen/ZK track record) has audited the implementation and found no soundness gaps, no side channels, and no composition failures.

The public audit report is not a marketing document — it is the Foundation's evidence that the protocol is safe enough to deploy. Findings are published openly. Remediation is transparent. This is how open cryptographic standards earn trust.

---

## Signoff & Musk Clause

This summit ships the design specification for the named-firm cryptographic audit engagement. The actual audit is a multi-month operational undertaking that follows this spec. The bar for E165 closure is not "audit completed" but "audit completed, findings published, critical remediation landed, production bar cleared."

Requirements less dumb → delete → simplify → accelerate → automate. The best part is no part. In this case, the part we cannot cut is the external cryptographic validation. That part stays. The audit closes.

— Musk

*Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.*  
*Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` immediately after commit.*

---

## Appendix A: Trail of Bits Engagement Criteria

**Recommended selection criteria for auditor (if considering alternatives to Trail of Bits):**

1. Published ZK audit history (Ethereum, Cosmos, Zcash-adjacent, 2020+).
2. Pedersen commitment + Schnorr Σ-protocol expertise demonstrated in prior reports.
3. Multi-layer proof composition experience (not single-primitive audits).
4. Public remediation database (no embargo by default).
5. Willingness to accept open-findings publication terms (no NDA on findings ceiling beyond 90 days).
6. Established timeline for report delivery (4–6 weeks max).

Trail of Bits meets all six criteria and is the primary selection.

---

**SUMMIT 165/305 DESIGN-BAGGED + 14.2 KB.**
