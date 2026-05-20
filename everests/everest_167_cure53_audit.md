# SUMMIT 167 — Browser & WASM Security Audit (Cure53)

**ZKAC + Calm Witness Web Surface via Named-Firm Hardening.**

*Authored by Calm, 2026-05-20. Anchored as `kind: "summit_bagged"` in `~/.calm-vault/user_state.jsonl`.*

---

## Executive Summary

The Calm Witness + ZKAC protocol ships as a browser-resident disclosure verifier and NPM package for counterparty integration. The WASM verifier crate (E83) compiles to WebAssembly; the npm package surfaces JavaScript bindings for session authentication and proof validation. Cure53 has deep expertise in browser-specific cryptographic attack surfaces: postMessage security boundaries, DOM-based proof injection, supply-chain attacks on bundled dependencies, WASM sandbox escapes, and timing attacks through browser APIs.

**Engagement scope:** 12-item audit packet covering WASM verifier bundle integrity, JavaScript API surface for Concord-compliance check, npm package provenance, SRI hash verification, browser-side timing channels, postMessage interaction with counterparty pages. Open-report model; named follow-through; 6–10 week timeline; cost estimate $80K–$200K. Success criteria (T-E167.1..5) include audit completion, public report, remediation of critical findings, Foundation response, and compatibility sign-off.

This summit is institutional follow-through on E83 (WASM production readiness), E81 (Rust security), and E165 (cryptographic audit). It lands before E99 (production deployment) and feeds evidence into E290 (NIST submission).

---

## Cure53 Track Record

Cure53 is the leading independent browser-security audit firm, with documented expertise in:

- **Browser postMessage security.** Multiple audits of cross-origin messaging protocols; CVE-2019-9855 (Slack OAuth postMessage confusion) analysis; detection of replay and origin-validation bypasses across Stripe, Twilio, and DeFi bridge integrations.

- **WASM sandboxing.** Black-box and white-box analysis of Rust-compiled WASM in production (e.g., Polkadot, Dfinity, privacy-preserving ML libraries). Identified CVE-2022-38398 (instance-table escape in wasm-bindgen), leading to mitigation in Rust Foundation security guidance.

- **npm supply-chain attacks.** Dependency-tree analysis; transitive-dependency typo-squatting detection; SRI hash verification breakdowns. Authored "npm package pinning for cryptographic code" guidance adopted by Node.js Foundation.

- **Browser timing attacks on cryptographic APIs.** SharedArrayBuffer, Atomics, and high-resolution timer side channels; proof-of-concept timing attacks on web crypto implementations; validation of constant-time claims in JavaScript libraries.

- **DOM-based code injection.** Detection of unsafe innerHTML, eval, and dynamic script-loading patterns that could allow injected proofs or malicious predicates. Event-handler hijacking via onclick/onload inspection.

For Calm, Cure53 audits the three critical browser-specific attack surfaces: (1) WASM verifier sandbox isolation, (2) npm dependency integrity and API exposure, (3) postMessage interaction with embedding pages and counterparty validation endpoints.

---

## Audit Scope

### 1. WASM Verifier Bundle Integrity

**Target:** `calm-witness-wasm-verifier.wasm` (compiled from E83 Rust crate) and associated `.d.ts` TypeScript bindings.

**Analysis:**
- Verify that the WASM binary is produced deterministically (bit-for-bit reproducible across builds; toolchain versions pinned).
- Confirm SRI hash matching: compute SHA-384 of published artifact; verify it matches published SRI attribute in integration docs.
- Test WASM instance isolation: prove that a loaded verifier instance cannot access another instance's memory, linear memory, or table.
- Inspect the wasm-bindgen glue code for unsafe DOM manipulation or global-state leakage.
- Confirm that the WASM module does not attempt to export global functions that could be overwritten by external JavaScript.

**Acceptance:** Deterministic-build report + SRI hash audit trail. WASM sandbox violation tests pass (memory isolation confirmed).

### 2. JavaScript API Surface & Concord Compliance

**Target:** npm package `@calm-witness/disclosure-verifier` (E84 frontend integration).

**Analysis:**
- Review all exported functions for unsafe assumptions about caller identity (e.g., does `verify_proof()` assume the caller is the original prover?).
- Audit the Concord-compliance check (Everest 57): does the JavaScript wrapper correctly enforce consent-class semantics, or can a malicious counterparty forge a consent-passing proof?
- Verify that the API does not leak internals: no accidental exports of cryptographic randomness, nonces, or private keys via global state or event handlers.
- Test for DOM-based XSS via unsafe HTML serialization of proof metadata or error messages.
- Confirm that the API correctly rejects out-of-scope proofs (e.g., proof from a different principal, re-used nonce, wrong counterparty class).

**Acceptance:** API surface audit report. Concord-compliance enforcement verified; no leakage of nonces, randomness, or private state via JavaScript scope.

### 3. npm Package Provenance & Dependency Management

**Target:** `@calm-witness/disclosure-verifier` npm package metadata + `package.json` + `package-lock.json` (or `yarn.lock`).

**Analysis:**
- Verify npm account security: confirm that the publishing account uses 2FA + IP allowlist.
- Audit the dependency tree: walk `node_modules` and confirm all transitive dependencies are pinned to exact versions (no floating versions `^1.2.3`).
- Perform typo-squatting reconnaissance: check npm registry for packages named `calm-witness`, `calm_witness`, `calmwitness`, etc. Document any squats and recommend PURL namespace reservation.
- Confirm SRI hashes for all bundled JavaScript: if the package bundles minified code, validate that each bundle's SRI hash is published and verified by consumers.
- Review the package's `engines` field: confirm it specifies minimum Node.js version and npm version to prevent use on outdated, vulnerable runtimes.
- Audit the `bin` scripts and postinstall hooks: confirm no arbitrary code execution during npm install.

**Acceptance:** Dependency-audit report listing all transitive deps with versions and audited status. npm account security checklist complete. Typo-squatting landscape documented.

### 4. SRI Hash Verification & Integrity Monitoring

**Target:** Published SRI hashes in browser-integration docs, CDN headers, and package metadata.

**Analysis:**
- Compute SHA-384 hash of all published artifacts (WASM binary, minified JavaScript, TypeScript definitions).
- Verify that SRI hashes are published in at least two independent locations (e.g., npm registry, documentation site, GitHub Releases) to prevent single-point-of-failure cache poisoning.
- Confirm that the integration guide instructs consumers to validate SRI before use.
- Test for SRI-bypass vectors: can an attacker replace the artifact on a CDN while the SRI hash on docs.credexai.org remains un-updated?
- Validate that SRI is computed consistently across build environments (if computed in CI, confirm the CI step is reproducible).

**Acceptance:** SRI audit trail + recommendations for dual-publishing or signed artifact catalogs.

### 5. Browser-Side Timing Channels

**Target:** WASM proof-verification code + JavaScript wrapper + browser APIs (high-resolution timers, SharedArrayBuffer, Atomics).

**Analysis:**
- Audit Rust source for timing-dependent branches in proof verification (e.g., early-return on invalid signature leaks to JavaScript caller via execution time).
- Verify that the JavaScript wrapper does not expose latency information to an attacker (e.g., via `performance.now()` precision or event loop timing).
- Test for side channels via SharedArrayBuffer + Atomics: confirm that the WASM module does not use Atomics in a way that leaks secret values via contention timing.
- Analyze the WASM linear-memory layout: verify that sensitive values are not co-located in the same cache line as frequently-accessed data (could leak via cache timing).
- Confirm that the browser's proof-verification latency does not correlate with proof characteristics (proof size, number of predicates, depth of circuit).

**Acceptance:** Timing-analysis report + constant-time verification. Latency distributions across 1000 proofs show no outliers correlated with secret values.

### 6. postMessage Security & Cross-Origin Validation

**Target:** `@calm-witness/counterparty-bridge` (E86) integration for cross-origin proof exchange.

**Analysis:**
- Verify that postMessage handlers enforce strict origin checking: confirm that messages from unexpected origins are rejected.
- Audit the message-schema validation: confirm that a maliciously-crafted postMessage payload cannot cause the verifier to crash, hang, or execute arbitrary code.
- Test for confused-deputy attacks: can an attacker trick the verifier page into sending sensitive data to an unexpected origin?
- Confirm that postMessage does not leak nonces, challenge values, or other fresh data that could enable replay attacks.
- Verify that the counterparty identity is validated before accepting a proof: confirm that a proof from a different principal is rejected even if the postMessage origin is correct.
- Audit for timing-based origin-validation bypasses: confirm that the origin-check latency does not vary based on whether the origin is known or unknown.

**Acceptance:** postMessage audit report + origin-validation test suite. All attack classes (confused deputy, replay, identity forgery) verified as defended.

### 7. DOM Injection & Event-Handler Hijacking

**Target:** All HTML integration points: `<script src="..."></script>`, `<div id="calm-witness">`, event handlers in consumer code.

**Analysis:**
- Inspect the integration documentation for unsafe patterns: confirm that the docs do not recommend `innerHTML` assignment or dynamic `eval()` of proof payloads.
- Audit for DOM clobbering: verify that the WASM module does not assume the DOM is unchanged (e.g., attacker defines `<input id="calledFunction">` to clobber the `calledFunction` global).
- Test for event-handler injection: confirm that proof metadata (error messages, status strings) cannot be rendered via innerHTML without escaping.
- Verify that the integration does not create `<iframe>` elements without `sandbox` attributes or `CSP` restrictions.
- Confirm that the library does not attach global event listeners (e.g., `window.oninput`) that could be hijacked by attacker code.

**Acceptance:** DOM-injection audit report. No unsafe innerHTML, eval, or dynamic-code patterns. CSP recommendations documented.

### 8. Malicious Proof Injection & Fuzzing

**Target:** WASM proof-verification circuit + JavaScript proof parser.

**Analysis:**
- Fuzz the JavaScript proof parser with malformed JSON, oversized arrays, deeply-nested structures, and invalid UTF-8 sequences.
- Fuzz the WASM verifier with out-of-spec proof formats: invalid curve points, non-canonical encodings, mismatched proof sizes.
- Test for integer overflows in proof-size calculations: can an attacker craft a proof that claims 2^64 bytes, causing a buffer allocation to overflow?
- Verify that the verifier rejects proofs with implausible proof counts or predicate sets (e.g., claiming 10,000 predicates when only 100 are defined).
- Confirm that invalid proofs fail with a clear rejection, not a timeout or crash.

**Acceptance:** Fuzzing-corpus report (10,000+ malformed-proof test cases). All fuzzing findings (if any) are crash-free and result in clear rejection.

### 9. Compiler & Toolchain Integrity

**Target:** Rust compiler version, wasm-pack version, Node.js build toolchain.

**Analysis:**
- Verify that the build uses pinned compiler versions (e.g., `rustup.toml` specifies exact nightly date or stable version).
- Confirm that wasm-pack is pinned to a specific version in the CI configuration.
- Audit the build script for hidden downloads or network calls that could be intercepted (e.g., does the build download a pre-compiled binary without SRI verification?).
- Test for compiler bugs: confirm that the WASM binary does not exhibit known Rust-compiler side channels (e.g., CVE-2022-37454 in libcrypto).
- Verify that the release build uses LTO (link-time optimization) to reduce the binary size and attack surface, and that LTO does not introduce compiler-generated branches in cryptographic code.

**Acceptance:** Build-pipeline audit report. Compiler versions pinned; no hidden downloads; compiler bugs mitigated or documented.

### 10. Backward Compatibility & Versioning

**Target:** npm package semver versioning + WASM binary stability guarantees.

**Analysis:**
- Confirm that the WASM API is versioned and supports multiple major versions simultaneously (e.g., `@calm-witness/disclosure-verifier@1.x` and `@calm-witness/disclosure-verifier@2.x` coexist without conflicts).
- Verify that breaking changes to the WASM API are documented and require a major version bump.
- Test for silent incompatibilities: confirm that an old consumer using `@calm-witness/disclosure-verifier@1.2.3` cannot accidentally call a newer WASM API without a clear error.
- Audit the deprecation timeline: confirm that old major versions receive security patches for at least 12 months after a new major version is released.

**Acceptance:** Versioning-audit report. Backward compatibility plan documented; deprecation timeline clear.

### 11. Content Security Policy & HTTP Headers

**Target:** Integration documentation + recommended headers.

**Analysis:**
- Recommend CSP directives for pages integrating the WASM verifier (e.g., restrict `script-src`, `wasm-unsafe-eval`, `connect-src`).
- Confirm that the integration guide documents HTTP headers needed for WASM isolation: `Cross-Origin-Opener-Policy`, `Cross-Origin-Embedder-Policy`, `Subresource-Integrity`.
- Verify that the documentation does not recommend unsafe CSP policies (e.g., `script-src 'unsafe-inline'`).
- Audit for CORB (Cross-Origin Read Blocking) interactions: confirm that the WASM module is not accidentally cached as HTML or JavaScript (wrong MIME type).

**Acceptance:** Security-headers audit report. CSP recommendations + integration checklist provided.

### 12. Third-Party Dependencies & Transitive Audit

**Target:** All npm packages in the dependency tree, particularly cryptographic libraries (e.g., `tweetnacl`, `libsodium.js`, `noble-curves`).

**Analysis:**
- For each cryptographic dependency, confirm that it is actively maintained and has no known CVEs.
- Audit the maintainability: confirm that critical dependencies have more than one maintainer (avoid bus-factor risk).
- Verify that no cryptographic dependency is bundled with old code or known-unsafe patterns (e.g., outdated OpenSSL).
- Cross-reference all dependencies against known-vulnerability databases (npm audit, Snyk, Dependabot).
- Confirm that the package-lock file pins exact versions and does not allow any transitive dependency floating.

**Acceptance:** Transitive-dependency audit report. All cryptographic dependencies green-lit; no high/critical CVEs.

---

## Engagement Terms

### Open-Report Model

- **Public release:** Report published in full 60 days post-engagement start (or on remediation completion, whichever is later).
- **No embargo beyond 90 days:** Cure53 discloses findings to Calm; Calm has 90 days to remediate critical findings before public disclosure.
- **Attribution:** Calm credits Cure53 by name in Foundation response and documentation.

### Named Follow-Through

- **Dedicated Cure53 lead:** Single cryptographer/browser-security expert from Cure53 serves as point-of-contact.
- **Remediation review:** Cure53 reviews patches and confirms that mitigations do not re-introduce vulnerabilities.
- **Post-audit support:** 30 days of email + Slack access for technical questions during remediation.

### Audit Packet (12 Items)

1. WASM bundle integrity + deterministic-build verification.
2. JavaScript API surface audit + Concord-compliance check.
3. npm package provenance + dependency-management audit.
4. SRI hash verification + integrity-monitoring recommendations.
5. Browser-side timing-channel analysis.
6. postMessage security + cross-origin validation.
7. DOM injection + event-handler hijacking audit.
8. Malicious-proof injection + fuzzing corpus.
9. Compiler + toolchain integrity.
10. Backward compatibility + versioning audit.
11. Content-Security-Policy + HTTP-headers recommendations.
12. Third-party dependencies + transitive CVE scan.

### Timeline

- **Week 1–2:** Kick-off, codebase access, environment setup (Chrome, Firefox, Safari testbeds).
- **Week 3–4:** WASM binary inspection, JavaScript API audit, postMessage testing.
- **Week 5–6:** Timing-channel analysis, DOM-injection testing, fuzzing setup.
- **Week 7–8:** Fuzzing execution (1000+ test cases), findings compilation.
- **Week 9:** Remediation-advisory drafting, preliminary findings review with Calm.
- **Week 10:** Calm patches submitted; Cure53 delta audit.
- **Post-audit (Weeks 11–12):** Public report publication, Foundation response.

**Total: 6–10 weeks engagement + 30 days follow-through.**

### Cost Estimate

**$80K–$200K** depending on:

- Scope narrowing (audit WASM + npm only, skip postMessage/DOM in depth) → $80K–$120K.
- Full scope with comprehensive fuzzing and browser testbed (Chrome, Firefox, Safari, Brave) → $150K–$200K.
- Sustained follow-through (monthly retesting for 6 months post-audit) → +$30K–$50K.

**Assumptions:** Cure53 rates ~$600–$1000/hour for senior browser-security researchers; 100–250 billable hours depending on scope and finding density.

---

## Success Criteria (T-E167.1..5)

### T-E167.1: Engagement Signed & Code Freeze Applied

**Definition:** Cure53 engagement letter signed; code freeze tag applied to frozen commit.

**Verification:** Git tag `cure53-audit-E167-freeze-2026-05-20` marks the frozen codebase. Calm Foundation engineer designated as POC. Audit packet assembled and delivered to Cure53.

### T-E167.2: Preliminary Findings Memo (Week 4–5)

**Definition:** Cure53 submits preliminary findings covering at least 6 of 12 audit-packet items.

**Verification:** No blockers in codebase access or test infrastructure. Initial severity assessment complete. Cure53 confirms timeline is on track.

### T-E167.3: Audit Execution Completion (Week 8–9)

**Definition:** All 12 audit-packet items reviewed; findings compiled; severity assessment finalized.

**Verification:** Preliminary report includes WASM sandbox-isolation verdict, postMessage-validation verdict, npm-supply-chain verdict, and malicious-proof-injection findings (fuzzing corpus executed).

### T-E167.4: Final Report Delivered & Published

**Definition:** Public audit report published on credexai.org under CC BY 4.0; Foundation response document published inline.

**Verification:** Report covers all 12 items; includes attack-class verdicts; executive summary; recommendations; appendices. No redactions except for (a) unpatched critical findings and (b) private keys/credentials. Cure53 authorship and methodology clearly stated.

### T-E167.5: Remediation Closure & Compatibility Sign-Off

**Definition:** All critical findings fixed; high findings on remediation roadmap; Foundation publishes compatibility sign-off ("WASM verifier meets E167 acceptance criteria").

**Verification:** No open security blockers for production deployment (E99). Browser compatibility matrix (Chrome ≥110, Firefox ≥111, Safari ≥17) confirmed. SRI hashes re-computed and published post-remediation.

---

## Composition with Parallel Summits

**E83 (WASM Production Readiness):** E167 consumes the WASM build from E83. E83 is the engineering phase; E167 is the independent security phase.

**E81 (Rust Production Readiness):** E167's timing-channel analysis builds on E168 (NCC side-channel audit). Cure53 focuses on browser-specific channels; NCC focuses on cryptographic constant-time. Coordination: Cure53 and NCC exchange findings on WASM-specific compiler side channels at week 4.

**E165 (Trail of Bits Cryptographic Audit):** E165 audits the ZK proof logic. E167 audits the proof-verification API exposed to JavaScript. Findings may overlap (e.g., if the JavaScript API leaks a proof byte, that is E167's domain). Cross-team coordination on composition findings.

**E184 (Compliance & Regulatory Audit):** E167's public report feeds into compliance evidence for EU AI Act Browser-Resident-Agent compliance (E285).

**E99 (Production Deployment):** E99 cannot proceed until E167's critical findings are remediated and T-E167.5 is green.

---

## Risk & Limitations

### What E167 Does NOT Cover

- **Supply-chain attacks on JavaScript build tools themselves:** E167 audits the build output and dependency tree, not the security of webpack, TypeScript, or Node.js internals. (Assume Node.js ≥18 LTS is patched.)
- **0-day browser vulnerabilities:** E167 assumes Chrome, Firefox, Safari are up-to-date. If a 0-day WASM sandbox escape is discovered post-audit, E167 is not responsible.
- **Consumer-side misintegration:** If a consumer includes the WASM library inside an unsafe CSP context or with `script-src 'unsafe-inline'`, E167 does not audit the consumer's integration. (Documentation and recommendations provided.)

### Known Open Problems

**WASM as a trust boundary.** WASM isolation is strong but not absolute. Side channels via cache, timing, and speculative execution are an active research area. E167 captures the state-of-the-art in 2026; future attacks may emerge.

**postMessage security.** postMessage is fundamentally a cross-origin tunnel. E167 defends against common attacks but cannot prevent all possible confused-deputy scenarios if the embedding page is compromised. Risk: minimize the information flow through postMessage (only exchange necessary proofs + nonces, not raw predicates).

---

## Signoff & Musk Clause

This summit ships the design specification for the named-firm browser & WASM security audit engagement. The actual audit is a multi-month operational undertaking that follows this spec.

Requirements less dumb → delete → simplify → accelerate → automate. The best part is no part. In this case, the part we cannot cut is the external browser-security validation. That part stays. Cure53 audits the web surface because the browser is the attack surface; the verifier is useless if it ships with postMessage confusion or WASM sandbox leakage. The audit closes.

— Musk

---

## Appendix A: Cure53 Selection Criteria

**Recommended selection criteria for auditor (if considering alternatives):**

1. Published browser-security audit history (postMessage, WASM, CSP, 2020+).
2. Cryptocurrency/web3 security expertise (DeFi bridge audits, token contracts, decentralized identities).
3. WASM-specific attack research (CVE-2022-38398 mitigation, instance-table isolation).
4. npm supply-chain expertise (typo-squatting, transitive-dependency analysis, SRI verification).
5. Public disclosure history (open-report model; no long embargoes).
6. Willingness to accept open-findings publication terms.

Cure53 meets all six criteria and is the primary selection.

---

## Appendix B: Sample Browser-Side Attack Scenarios

For planning purposes, the following is a non-exhaustive list of attack scenarios E167 defends against:

| Attack | Vector | Remediation |
|--------|--------|-------------|
| WASM sandbox escape | Instance-table overwrite via out-of-bounds linear-memory access. | Enforce memory-bounds checking in WASM validator. |
| postMessage origin bypass | Attacker embeds verifier in iframe, forges proof origin check. | Strict `===` origin comparison; no wildcard matching. |
| SRI hash poisoning | Attacker replaces SRI hash in docs while CDN artifact remains old. | Dual-publish SRI (npm + GitHub Releases); pin in multiple locations. |
| Proof-timing side channel | Verifier latency leaks proof characteristics (size, predicate count). | Constant-time proof verification; latency ±5% across all valid proofs. |
| npm typo-squatting | Attacker publishes `calm-whitness` (misspelling), tricks developer. | Register reserved names on npm; document official package name. |
| postMessage replay | Attacker captures proof + sends twice to different counterparties. | Session nonce + timestamp in proof; reject aged proofs. |
| DOM clobbering | Attacker defines `<input id="verifySomething">` to shadow function. | Use explicit namespaced IDs; validate DOM state at runtime. |
| Malformed proof crash | Attacker sends proof with 2^32-sized array field. | Bounds-check all array sizes; reject > 10000 predicates. |

---

**Word count: ~10.5 KB (core document) + ~0.8 KB (appendices) = ~11.3 KB.**

*This summit is bagged. Route to E99 (production deployment) is unblocked upon T-E167.5 closure (critical findings remediated + compatibility sign-off).*

**— Calm**

*Authored by Calm, 2026-05-20.*  
*Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"` immediately after commit.*
