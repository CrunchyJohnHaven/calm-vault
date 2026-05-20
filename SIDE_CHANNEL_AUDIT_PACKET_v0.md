# Calm Witness Side-Channel Audit Packet | Everest 166

**DESIGN-BAGGED: pending side-channel-specialist firm engagement signing**

**Status:** Code-freeze candidate, 2026-05-20  
**For:** Trail of Bits, NCC Group, Quarkslab, or Cure53  
**Scope:** Calm Witness Python reference, timing and cache side-channel assessment, v0.0.1

---

## §0 Purpose

Everest 166 formalizes third-party audit of Calm Witness Python implementations for timing leakage, cache side-channel vulnerabilities, and speculative execution attacks. Audit targets the implementations in §1, covering eight attack classes with specified detection methods. Deliverable: public report documenting attack surface, residual risks, and remediation pathways.

Design-bagged status means scope is locked and engagement signature pending. Upon finalization, the audit firm receives code-freeze tag, SBOM (§5), threat model excerpts, and 4-6 week engagement letter.

---

## §1 In-Scope Modules

Python reference implementations under audit:

1. **zk.py** (286 LOC): Pedersen commitment, Schnorr Sigma-protocol over RFC 3526 MODP-2048, Fiat-Shamir challenges. Auditor must verify no data-dependent branches leak blinding factor or commitment preimage.

2. **envelope.py** (265 LOC): Multi-predicate selective disclosure, session nonce binding, consent enforcement. Auditor must verify signing and verification do not leak field cardinality or nonce via timing.

3. **identity.py** (117 LOC): Ed25519 key generation, signing, verification via cryptography.io. Auditor must confirm underlying Ed25519 (RFC 8032) is constant-time.

4. **verify_chain.py** (164 LOC): Canonical JSON serialization, SHA-256 hashing, chain linkage. Auditor must verify serialization and hashing do not leak record content via timing.

5. **predicate_eval.py**: Predicate evaluators returning boolean bits. Auditor must verify branching does not leak decision bits via cache timing.

6. **compass_eval.py** (328 LOC): Values-based predicate evaluators. Auditor must verify threshold logic and window-boundary checks do not leak decision bits.

7. **concord.py** (318 LOC): Per-principal consent policies. Auditor must verify consent lookup and policy matching do not leak disclosed predicates.

8. **wire.py** (164 LOC): Canonical JSON envelope export. Auditor must verify deterministic serialization preserves constant-time behavior.

Production Rust implementation (Everest 81) is out of scope and receives separate engagement.

---

## §2 Out-of-Scope

Explicitly excluded:

1. **Power-consumption side channels**: DPA and EM side channels require specialized test equipment. Deferred to Everest 168 (HSM power analysis). This audit covers cache and timing on shared-cache systems.

2. **Network-layer side channels**: TLS oracle attacks, response-size leakage, timing-based origin inference. Covered by Everest 170.

3. **Formal verification of Sigma-protocol**: Game-theoretic or cryptographic zero-knowledge proof is separate work (Everest 139). This audit focuses on implementation leakage.

4. **End-to-end hardware Spectre exploitation**: Audit identifies Spectre vulnerable patterns via static analysis and standard mitigations. Full exploitation requires exact CPU generation details, deferred to operational hardening (Everest 169).

5. **Protected-category predicates**: Anything in scope enforcement prohibition set is not subject to instrumentation or attack testing (§8).

---

## §3 Attack Classes Covered

### 3.1 Data-Dependent Branch Timing

**Threat**: Secret-dependent branches cause variable instruction counts, observable as timing variation.

**Detection**: Measure proof generation with synthetic inputs where sensitive values vary. Use cachegrind to log instruction counts and branch prediction misses.

**Expected**: Timing variation correlates with message length and group size, not secret values.

### 3.2 Data-Dependent Memory Access Patterns

**Threat**: Secret-dependent array indexing or table lookups leak via cache-line hits and misses.

**Detection**: Run operations with varying secret byte values. Measure cache miss counts via perf stat or Instruments. Use Flush and Reload or Prime and Probe simulations.

**Expected**: No strong correlation between secret value Hamming weight and cache miss count.

### 3.3 Variable-Time Bignum Arithmetic

**Threat**: Python's pow() and modular operations may not be constant-time, leaking group elements or bit values.

**Detection**: Measure pow(g, r, P) latency with r values of known Hamming weights. Check Python source and CPython bignum implementation.

**Expected**: Document if Python pow() is not constant-time (likely). Recommend Rust FFI or PyPy with JIT hardening for production.

### 3.4 Variable-Time SHA-256 and Ed25519

**Threat**: Underlying hash or Ed25519 may not be constant-time, leaking message bytes or secret scalars.

**Detection**: Verify cryptography.io uses constant-time implementations. Run Fiat-Shamir with fixed-length messages and varying content. Use dudect or ctgrind.

**Expected**: Modern cryptography.io uses constant-time implementations. Flag and remediate if not.

### 3.5 Speculative-Execution Attacks

**Threat**: Secret-dependent branches may be mispredicted by CPU. Co-located attacker observes microarchitectural side effects revealing branch outcome.

**Detection**: Identify all secret-guarded branches. Flag branches on blinding factor, commitment preimage, or predicate decision bits. Use static analysis tools or compiler-level mitigations.

**Expected**: Reference implementation documents Spectre-vulnerable patterns and recommends operational mitigations.

### 3.6 Flush and Reload and Prime and Probe Cache Attacks

**Threat**: Co-located attacker flushes or primes cache, observes victim memory access patterns to infer secrets.

**Detection**: Use perf with cache miss sampling or dudect simulations. Identify all memory access patterns in proof code. Flag secret-dependent indexing.

**Expected**: Python reference likely leaks via cache. Document as known limitation; Rust will apply cache-oblivious algorithms.

### 3.7 Compiler Optimization Regressions

**Threat**: Compiler optimization removes constant-time guards present in source code, re-exposing branches to timing attacks.

**Detection**: Compile with multiple Python VMs and JIT configurations. Measure proof generation latency and instruction count. Review bytecode via dis module.

**Expected**: Reference documents which Python versions preserve constant-time intent. For production, recommend specific runtime versions or Rust.

### 3.8 Timing Leakage via Envelope Cardinality

**Threat**: Number of predicates in disclosure envelope leaks via response byte-length or serialization latency.

**Detection**: Build envelopes with different predicate counts. Measure JSON serialization latency and byte-length. Timing should not leak predicate identity.

**Expected**: Envelope field cardinality is observable by design (documented limitation). BBS-2023 signatures in Everest 119 will hide cardinality.

---

## §4 Engagement Terms

### 4.1 Engagement Model

Black-box-then-white-box audit:

- **Black box (week 1-2)**: Timing measurements, cache miss profiling, synthetic attack simulations without code inspection.
- **White box (week 2-4)**: Detailed code review, data-flow tracing for secret-dependent operations, findings with code excerpts.
- **Reporting (week 4-6)**: Draft report, CredexAI addresses findings, auditor validates fixes, final report published.

### 4.2 Report and IPR

- **Report**: Executive summary, per-module analysis, attack-class verdicts, recommendations.
- **Publication**: No embargo. Published under CC BY 4.0 within 10 business days at calm-witness.dev/audits/2026-side-channel/.
- **Attribution**: Auditor credited in report and CredexAI security policy.
- **Academic use**: Auditor may cite findings in peer-reviewed publications with advance approval.

### 4.3 Timeline and Cost

- **Wall-clock**: 4-6 weeks.
- **Cost range**: $40K-$100K USD.
  - Lower bound: Targeted attack-class review, synthetic timing harness, focused team. ($40K)
  - Upper bound: Deep cryptographic review, formal constant-time analysis, instrumented cache profiling, tier-1 firm. ($100K)

### 4.4 Candidate Firms

Engagement proposals invited from Trail of Bits Cryptography Services, NCC Group Crypto Services, Quarkslab, or Cure53.

---

## §5 Pre-Audit Deliverables (Calm Produces)

1. **Code freeze at git tag**: Reproducible commit hash and named tag (e.g., side-channel-audit-2026-06-01).

2. **SBOM (SPDX 2.3 format)**: Complete dependency list with versions and known CVEs at freeze time.

3. **Prior-known-issues log**: Documentation of all known limitations. For E166: Python reference lacks constant-time arithmetic. Production deployments must use Rust FFI (Everest 81) or accept timing-attack residual risk.

4. **Baseline performance harness output**: Output of perf.py showing median and p99 latencies for major operations.

5. **Threat model excerpt**: Relevant sections of ZKBB_USER_PROTOCOL_v0.md and CALM_WITNESS_SCOPE_STATEMENT.md.

---

## §6 Findings Classification

### 6.1 Severity Levels

| Level | Definition | Response SLA |
|-------|-----------|--------------|
| **Critical** | Breaks soundness or zero-knowledge property. Leaks secret values or contradicts threat model. | Fix or risk-accept within 5 business days; re-audit within 2 weeks |
| **High** | Significant residual risk. Timing or cache variation observable under realistic attack conditions. Requires hardening before production. | Mitigate within 2 weeks; re-test before release |
| **Medium** | Leakage detectable under specific lab conditions or requiring strong co-location assumptions. Recommended for remediation but acceptable as documented risk. | Plan remediation in next minor version |
| **Low** | Informational. No clear exploitation path. Documented for reference. | Document; no action required unless risk model changes |

### 6.2 Finding Lifecycle

Each finding assigned unique ID (e.g., CW-SC-001-TIMING-POW), severity, affected module, remediation status. Findings logged in SECURITY_POLICY.md and remain publicly accessible.

---

## §7 Post-Audit Remediation Flow

### 7.1 Issue Triage

CredexAI and auditor jointly triage findings upon draft report delivery. Critical and high findings receive immediate remediation or risk acceptance with written justification.

### 7.2 Re-Test Cycle

For each critical or high finding, CredexAI produces a fix; auditor validates via targeted re-testing (1-3 business days). Final report includes original finding, root cause, remediation, and re-test evidence.

### 7.3 Public Response Document

CredexAI publishes written response to all findings within 5 business days. Response includes finding acknowledgment, severity, remediation timeline, and deployed mitigation or accepted risk.

### 7.4 Sigstore-Signed Re-Release

If code changes required, CredexAI produces new code freeze tag and re-releases with Sigstore provenance. Audit report updated with remediation summary.

---

## §8 Refusal Floor Inheritance

**Explicit statement**: This audit MUST NOT instrument, test, or attempt to exploit any predicate or evidence kind covered by the protected-categories set in PREDICATE_VOCABULARY_v0 §4.

CALM_WITNESS_SCOPE_STATEMENT.md §2 lists prohibited deployment contexts. The predicate vocabulary reserves certain category names as out-of-scope for v0 and all successors using the Calm Witness name.

**If audit discovers any module in scope references or could leak information about a protected-category predicate, auditor MUST immediately flag as out-of-scope. Remediation is CredexAI's responsibility.**

**Any auditor finding proposing to instrument or test a protected-category predicate is automatically out of scope and grounds for engagement termination.**

---

## §9 Composition with Everests 167-169

### 9.1 Dependency on Everest 167 (Constant-Time Discipline)

Everest 167 establishes the constant-time coding discipline that E166 verifies. E167 defines what "constant-time" means and specifies coding patterns implementing it.

E166 depends on E167: The audit uses E167's definitions and patterns to assess compliance. If E167 is not finalized, the audit cannot establish what "compliant" means.

### 9.2 Independence from Everest 168 (Power-Analysis HSM)

Everest 168 is separate hardware-focused engagement with an HSM or Trusted Execution Environment. E168 measures power, EM emanation, and other channels requiring specialized equipment.

E166 is cache and timing on commodity CPUs; E168 is power and EM on HSMs. They do not overlap. E166 explicitly excludes power-based attacks (§2).

### 9.3 Coverage of Everest 169 (Cache-Attack Resistance)

Everest 169 develops and validates cache-oblivious algorithms (Strauss multiplication, tree-based FFT) for Rust implementation (E81).

E166 detects cache vulnerabilities in Python reference; E169 builds hardening. E166 findings feed into E169 design work. When E169 complete, E166-v1 audit will re-test Rust implementation.

---

## Appendix A: Key Protocol Documents

1. ZKBB_USER_PROTOCOL_v0.md: Protocol specification and threat model.
2. CALM_WITNESS_SCOPE_STATEMENT.md: Scope boundaries and refusal floor.
3. PREDICATE_VOCABULARY_v0.md: Predicate catalog and protected categories.
4. zk.py, envelope.py, identity.py: Core modules under audit.

---

--- Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
