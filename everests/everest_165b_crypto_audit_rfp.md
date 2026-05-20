# Everest 165b — Cryptographic + Side-Channel Audit RFP

*Phase XV — Deployment Maturity. Prereq: Everest 81, 90.* **DESIGN-BAGGED (pending firm engagement).**

---

## Executive summary

This RFP solicits a named third-party cryptographic audit and side-channel resistance assessment of the Calm Witness protocol implementation, covering zero-knowledge proof soundness, Pedersen commitment correctness, Schnorr identification binding, and timing/cache/power-analysis vectors on operator signing and proof generation. Engagement timeframe: 8–12 weeks audit + 4–8 weeks remediation + 2–4 weeks re-audit. Budget: $150K–$300K fixed-bid or time-and-materials.

---

## Motivation + strategic context

Everest 90 delivered an audit-ready packet (threat model, specs, conformance vectors, fuzzer history, architecture diagrams). The actual third-party cryptographic audit has been scoped separately as a named engagement with a reputable firm. This RFP defines what we're asking external auditors to verify, which firms we believe are qualified, and the terms under which the audit report becomes public.

Calm Witness is an inter-agent information-disclosure protocol using zero-knowledge proofs. Audit credibility is essential: the system makes cryptographic claims (hiding, zero-knowledge, soundness) that only a trained third-party cryptographer can meaningfully verify. This is not a code-audit-generalist engagement; we need depth in Σ-protocols, range proofs, side-channel methodology, and Rust unsafe-block analysis.

---

## Audit scope

### In scope

1. **Pedersen commitments + Σ-protocol soundness.** Verification of the Pedersen commitment scheme (RFC 3526 MODP-2048 for v0, migration path to Ristretto255 for v1) and the Σ-protocol disjunction proof per CALM_WITNESS_WIRE_FORMAT_v0.md §4. Auditor shall verify:
   - Correct group operation (modular exponentiation, inverse, identity handling).
   - Soundness of the challenge-generation rule (Fiat-Shamir binding, hash function security margin, transcript integrity).
   - Absence of information leakage in the proof structure or transcript.
   - Compatibility with the Predicate Vocabulary v0 (Everest 6) ID schema and semantic meaning of disclosed bits.

2. **Bulletproofs range-proof correctness + zero-knowledge.** Verification of the Bulletproofs-based range-proof implementation (Everests 45, 46). Auditor shall verify:
   - Bulletproofs circuit assembly (bit constraints, aggregation, range widths).
   - Zero-knowledge property (no witness leakage, simulator efficiency, transcript indistinguishability).
   - Prover and verifier computational paths match the published Bulletproofs specification (cf. Bünz et al. 2018, ZCash implementations).
   - Absence of early-exit or rejection-sampling patterns that could leak witness bits.

3. **Schnorr identification + Fiat-Shamir transcript binding.** Verification of Schnorr-signature and Schnorr-ID protocols as applied to operator signing (Everest 68). Auditor shall verify:
   - Signature generation does not reuse random nonces (k-reuse attack).
   - Transcript binding (canonical-JSON encoding, deterministic field ordering per §3 of wire format).
   - Forgeability bounds under the discrete logarithm assumption.
   - Interoperability with Ed25519 and future algorithm-migration hooks.

4. **Calm Witness disclosure envelope (E67) parser.** Verification of the wire-format encoder/decoder (CALM_WITNESS_WIRE_FORMAT_v0.md). Auditor shall verify:
   - Canonical-JSON encoding is deterministic and unambiguous (lexicographic key ordering, no whitespace variance, hex-encoding consistency).
   - Parser rejects malformed or truncated messages without panic or memory unsafety.
   - Round-trip property: encode → decode → re-encode produces identical bytes.
   - Conformance with published test vectors (Everest 90 packet, § 6).

5. **Sigsum-anchoring composition (E30) + Roughtime (E31) binding.** Verification of the timestamp-anchor integration:
   - Correctness of the commitment-hash binding into the Sigsum transparency log.
   - Freshness verification against Roughtime responders (timestamp parsing, leap-second handling, responder-signature validation).
   - No replay or rollback attacks on timestamp anchors.
   - Latency + completeness guarantees (what happens if Sigsum is unavailable?).

6. **Side-channel resistance: timing, cache, power-analysis.** Comprehensive side-channel evaluation:
   - **Timing attacks** on operator signing (ECDSA nonce generation, scalar multiplication, proof computation) using differential power analysis (DPA) methodology or equivalent. Auditor shall measure execution time variance across witness values and detect timing-dependent branches.
   - **Cache side-channels** on Pedersen exponentiation and Bulletproofs inner-product computations. Auditor shall use tools such as Cachegrind or equivalent cache simulation to detect access-pattern variance correlated with secret data.
   - **Power analysis** on Rust operator binary (if available on test hardware): Simple Power Analysis (SPA) for instruction-sequence leakage, Correlation Power Analysis (CPA) for high-order correlations.
   - **Allocator side-channels**: malloc/free patterns and timing variance from heap fragmentation.
   - Mitigation assessment: constant-time library usage (e.g., zeroize, subtle for boolean aggregation), branch elimination, cache-oblivious algorithms.

7. **Memory safety: Rust unsafe blocks + FFI.** Verification of safety in presence of untrusted input:
   - Audit all `unsafe` blocks in the Calm Witness crate and dependencies (bulletproofs, curve25519-dalek, sha2, etc.). Verify SAFETY comments are justified and no bounds/alignment/concurrency invariants are violated.
   - FFI boundaries to whisper.cpp (if present in E82, E83) and external cryptographic libraries. Verify pointer handling, lifetime annotations, and absence of use-after-free or double-free.
   - Fuzzer-guided audit: run libFuzzer or cargo-fuzz against parser and proof-verification entry points; auditor reviews crash/hang/UBSAN reports.

8. **Bank-teller-note structural deniability (E58).** Verification that the deniability properties claimed in Everest 58 are preserved in the implementation:
   - No implicit identifiers in proof transcripts.
   - Proof acceptability does not depend on the counterparty's public key (no implicit authentication).
   - Envelope signatures are over the disclosures, not over counterparty identity.

9. **Concord anti-purity-test guards (CALM_CONCORD_PROTOCOL_v0 §4).** Verification of the defense against oracle-separation attacks:
   - Presence and correctness of nonce-binding into all proof transcripts.
   - Verifier rejects any proof that does not bind the current session nonce (Everest 99, DisclosureEnvelope, field `session_nonce`).
   - No timing variance that leaks session-nonce structure.

### Out of scope

- **Quantum-resistance audit** — deferred to Everest 96 (Post-Quantum Migration Plan) follow-on engagement; separate RFP.
- **Hardware-attestation audit** — separate, deferred to Everest 233.
- **Disability-rights + cognitive-liberties compliance** — separate, deferred to Everests 186, 187.
- **Behavioral-biometric science evaluation** (FAR/FRR, forensic handwriting) — separate Everest 40 engagement with academic partners.
- **Production-deployment operational risk** — separate operational-consulting engagement.

---

## Named candidate firms + rationale

### Trail of Bits

**Specialization**: End-to-end cryptographic protocol audit; Rust unsafe-block analysis; differential fuzzing (Manticore, Echidna).

**Track record**: Compound (multi-year audits, DeFi protocol bugs), MakerDAO (governance + cryptography), Zcash (ZK protocol), Tezos (proof systems), Filecoin (threshold cryptography). Published whitepapers on side-channel methodology and zero-knowledge proof verification.

**Relevant depth**: Published research on Σ-protocol verification, Fiat-Shamir soundness, and cache-timing attacks on elliptic-curve operations. In-house cryptographers with peer-reviewed publications. Experience with MODP groups, Pedersen commitments, and Bulletproofs variants.

**Why chosen**: Strongest side-channel track record among the candidates; largest in-house cryptography team; reproducible methodology (publicly available tools and reports). Prior ZK protocol audits exceed our requirement of 3 audits.

### NCC Group

**Specialization**: Broad cryptographic-services practice; protocol audit and implementation review; penetration testing.

**Track record**: Numerous ZKP audits (Aztec Protocol, Polygon Hermez, Consensys zk-SNARK audits), DeFi protocols, and cryptographic library reviews. Published crypto-audit methodologies and OWASP-aligned risk frameworks.

**Relevant depth**: In-house cryptographers with academic publishing record. CPA and DPA expertise via the Cryptography Services team. Rust-code audit capacity.

**Why chosen**: Consistent crypto-audit output quality; established methodology for ZK proof systems; good geographic + organizational independence from Calm. Concurrent audit capacity on large teams.

### Cure53

**Specialization**: Protocol-level security audits; implementation verification; cryptographic systems review.

**Track record**: OpenPGP implementations (GnuPG, Thunderbird); Signal Messaging protocol review; multiple cryptographic protocol audits. Known for thoroughness and detailed reporting.

**Relevant depth**: Deep expertise in signature schemes, key management, and transcript binding. Published methodology for protocol-audit composition. Fluent in Rust.

**Why chosen**: Exceptional reputation for protocol-level verification; prior work on deniability properties and signature-based systems. Thorough documentation and public reporting.

### Least Authority

**Specialization**: Zero-knowledge cryptographic systems; Zcash audits; proof-circuit verification.

**Track record**: Primary auditor for Zcash protocol changes (Sapling, Halo); Tezos cryptographic components; multiple ZKP-specific audits. Deep ZK expertise and established relationships with the academic ZK community.

**Relevant depth**: Bulletproofs circuit verification expertise. Pedersen commitment analysis. Published research on ZKP soundness and privacy properties.

**Why chosen**: Singular depth in zero-knowledge proof systems; Bulletproofs implementation knowledge; smallest firm but highest specialization. Ideal for co-engagement on ZK sub-scope.

### ConsenSys Diligence

**Specialization**: Ethereum + ZK ecosystem; formal methods; cryptographic protocol review.

**Track record**: Ethereum 2.0 cryptographic components; Polygon ZK rollup audits; multiple ZKP system audits. Strong academic connections and formal-methods capability.

**Relevant depth**: BLS signature schemes, threshold cryptography, ZKP verification. Formal-methods tooling (K Framework) for proving correctness properties.

**Why chosen**: Bridge between cryptographic rigor and DeFi-deployment scale; strong ZK audit catalog; available for parallel engagement.

---

## RFP structure and terms

### Cover letter (from Calm)

The cover letter shall describe:

- **What we're building**: Calm Witness as an inter-agent disclosure protocol; privacy-preserving information flow; use cases (enrollment verification, ongoing-status disclosure, consent-predicate binding).
- **Why audit is critical**: Cryptographic claims require independent expert verification. Credibility of the open standard depends on third-party certification. Public report strengthens ecosystem confidence.
- **Timeline + resource commitment**: Calm is committed to full transparency, auditor cold-start (packet-first), rapid remediation, and public-report publication.
- **Calm Foundation governance**: Independence from Creativity Machine LLC principals; commitment to open standards; funding + operational autonomy.

### Scope detail — line-item modules

The RFP shall itemize each audit axis separately so the firm can propose partial scope or parallel engagement:

1. **Module A: Pedersen + Σ-protocol soundness** — 40–60 person-hours.
2. **Module B: Bulletproofs range-proof correctness** — 50–80 person-hours.
3. **Module C: Schnorr identification + Fiat-Shamir binding** — 30–50 person-hours.
4. **Module D: Disclosure envelope parser (wire format)** — 20–40 person-hours.
5. **Module E: Sigsum-anchoring + Roughtime binding** — 30–50 person-hours.
6. **Module F: Timing + cache side-channel analysis** — 60–100 person-hours (requires specialized equipment/tools).
7. **Module G: Memory safety + unsafe-block audit** — 50–80 person-hours.
8. **Module H: Deniability properties (E58) + Concord guards (E99)** — 30–50 person-hours.
9. **Module I: Conformance-vector execution + fuzzer-coverage assessment** — 20–30 person-hours.

**Total baseline estimate**: 330–540 person-hours at $150–$250/hour = $150K–$300K fixed scope. Firms may propose:
- Full scope (all modules).
- Phased scope (Module A–E first; Modules F–H in a Phase 2).
- Parallel scope (Firm 1 handles Modules A–C + F; Firm 2 handles D–E + G–H; cross-firm finding-comparison).

### Deliverables

1. **Public audit report** — Published on `vault.thecreativitymachine.ai/audits/` within 2 weeks of completion. Report shall include:
   - Executive summary (findings severity distribution, overall assessment).
   - Detailed findings (one section per module; severity classification per CVSS 3.1 or equivalent).
   - Methodology (tools used, assumptions, scope limitations).
   - Remediation guidance (for each accepted finding, auditor proposes a fix).
   - Auditor independence statement (conflict-of-interest disclosure).

2. **Remediation documentation** — For every accepted finding (critical, high, or medium), Calm shall prepare a written remediation (code change + test) and request auditor sign-off that the fix resolves the concern.

3. **Sigstore-signed manifest** — A public JSON manifest signed by the auditor's Ed25519 key, asserting:
   - Audit engagement dates (start, completion).
   - Git commit hash of the audited codebase.
   - List of findings + severity levels.
   - Link to public audit report.

4. **Reproducibility instructions** — Auditor provides detailed instructions for reproducing all findings (proof-of-concept code, cache-timing instrumentation setup, fuzzer corpus seeds, etc.).

### Timeline

- **Weeks 1–12: Audit execution** — Auditor works from the Everest 90 packet, then white-box with Calm engineer support after Week 1. Weekly sync calls for clarification. Preliminary findings due at Week 8; final findings at Week 12.
- **Weeks 13–20: Remediation** — Calm implements fixes for critical/high/medium findings; auditor reviews remediation PRs asynchronously. Calm targets all critical findings remediated within 4 weeks.
- **Weeks 21–24: Re-audit** — Auditor verifies fixes resolve the root cause; spot-checks for regressions. Final audit report published at Week 24.
- **Total: 6 calendar months.**

**Gating**: If critical findings remain unresolved at Week 24, Calm and auditor agree on an extended timeline (up to 8 weeks additional) or escalate to Calm board for triage.

### Budget

**Fixed-bid proposal**: $150K–$300K depending on scope chosen (full scope: $250K–$300K; phased scope: $150K–$200K; parallel two-firm scope: $280K–$350K total).

**Time-and-materials acceptable** for novel circuits or architectural changes discovered during the audit (capped at 20% variance above the fixed bid; requires written change notice).

**Payment schedule**:
- 30% on engagement signature.
- 40% on preliminary findings delivery (Week 8).
- 20% on final audit report publication (Week 24).
- 10% on Sigstore manifest signature + reproducibility artifacts.

### Engagement model

**Preferred**: Fixed-bid with clearly-defined scope (modules A–I or a subset). Firm provides a detailed work plan (hours per module, tool setup, team composition).

**Acceptable**: Time-and-materials for portions where novel proof circuits or architectural features emerge during the audit. T&M rate must be specified upfront ($150–$250/hour); total T&M spend must be approved by Calm CTO in writing.

**Key personnel**: Auditor shall designate one lead cryptographer (available for all technical calls) and one co-lead. No more than 30% staff turnover during the engagement; replacement staff must be approved by Calm.

### Conflict-of-interest + independence

Auditing firm shall disclose and eliminate any of the following conflicts:

- Current or prior employment relationship with Creativity Machine LLC or CredexAI (Calm's co-sponsor).
- Direct financial interest in Calm's success (equity, option grants, revenue share).
- Concurrent audit engagement with a direct Calm competitor (Anoncreds, AnonCreds-compatible systems) without explicit consent.
- Prior non-disclosure agreement (NDA) with Calm that would prevent the auditor from publishing findings.

**Non-waivable conflicts**:
- Current employment by Calm, CredexAI, or Creativity Machine LLC.
- Financial interest >5% in Creativity Machine LLC or CredexAI.

All other conflicts must be disclosed in writing to Calm CTO + board audit committee before engagement signature.

---

## Audit-output requirements + publication policy

### Public audit report

The final audit report is published on `vault.thecreativitymachine.ai/audits/` under a CC-BY-4.0 or equivalent license. Report contents:

- All findings (including low-severity findings and informational notes).
- CVSS 3.1 severity scores for each finding.
- Calm Foundation's written response and remediation status for each finding.
- Links to fix commits in the public Calm Witness GitHub repository.
- Auditor methodology, tools, and assumptions.
- Test-vector coverage summary.
- Auditor independence statement.

### Remediation documentation

For each accepted finding, Calm publishes:

- **Fix commit hash** in the Calm Witness repository.
- **Commit message** describing the change and linking back to the audit finding.
- **Test coverage**: any new test cases added to prevent regression.
- **Auditor sign-off**: written confirmation from the auditor that the fix resolves the root cause.

### Sigstore-signed manifest

Auditor creates a JSON manifest (signed with Ed25519) listing:

```json
{
  "audit_engagement": "Calm Witness v0 Cryptographic + Side-Channel Audit",
  "auditor_firm": "<Firm name>",
  "auditor_lead": "<Name>",
  "audit_start": "<ISO 8601 date>",
  "audit_completion": "<ISO 8601 date>",
  "audited_commit_hash": "<40-char hex>",
  "audited_codebase_uri": "https://github.com/calm-witness/calm-witness",
  "findings_summary": {
    "critical": <count>,
    "high": <count>,
    "medium": <count>,
    "low": <count>,
    "informational": <count>
  },
  "public_report_uri": "https://vault.thecreativitymachine.ai/audits/calm-witness-v0-<date>.pdf",
  "remediation_status": "all_critical_and_high_fixed" | "in_progress" | "deferred",
  "auditor_signature": "<Ed25519 signature>"
}
```

Manifest is published at `vault.thecreativitymachine.ai/manifests/calm-witness-v0-audit.json` and pinned in the Calm Witness README.

### Disclosure + publication rights

- **Auditor may publish findings immediately upon report completion.** No embargo period required.
- **Calm may request a 30-day hold** for actively-exploited findings or findings affecting live production deployments. Firm may not hold findings longer than 90 days unless both parties agree in writing.
- **Unfixed findings after 90 days** are published at the auditor's discretion (with notice to Calm).
- **Auditor's right to present findings** at conferences, in blog posts, or in academic publications is preserved. Calm may not demand redaction of technical details if the publication describes a fixed vulnerability or an in-progress remediation.

---

## Selection criteria for the firm

Calm will prioritize firms meeting **all** of the following:

1. **Cryptographic audit track record**: ≥3 published ZK protocol audits (Ethereum zk-SNARK, Zcash protocol, StarkWare, Monero, Anoncreds, or equivalent). Reports must be publicly available (not under NDA).

2. **In-house cryptography expertise**: Team includes at least 2 cryptographers with:
   - Published peer-reviewed papers on cryptographic protocol verification, side-channel analysis, or zero-knowledge proofs (venue: IACR, IEEE, ACM CCS, or equivalent).
   - ≥5 years of post-PhD cryptographic-audit experience.
   - Fluency in at least one of: Rust, C, or Haskell (required for unsafe-block audit).

3. **Side-channel methodology**: Demonstrated experience (published case studies or conference talks) in:
   - Timing-attack detection on cryptographic operations (instruction-level simulation or physical measurement).
   - Cache-side-channel analysis (Cachegrind, Intel Pin, CacheBleed, or equivalent tools).
   - Power-analysis methodology (DPA, CPA) or equivalent differential analysis.
   - Mitigation guidance (constant-time primitives, cache-oblivious algorithms, speculative-execution hardening).

4. **Reproducibility commitment**: Firm publishes:
   - Fuzzer corpus and crash-reproduction artifacts.
   - Cache-timing instrumentation setup (Cachegrind scripts, pin-tool configurations, etc.).
   - Proof-of-concept code for each finding (unless disclosure risk requires withholding).

5. **Geographic + organizational independence**: Auditor firm is not a subsidiary of, and has no >10% shared ownership with, Creativity Machine LLC, CredexAI, or any direct Calm Witness competitor.

---

## Parallel-engagement option

Calm may engage **two firms concurrently** on different sub-scopes:

- **Firm A**: Modules A–C (Pedersen, Bulletproofs, Schnorr) + Module F (side-channel).
- **Firm B**: Modules D–E (wire format, Sigsum) + Modules G–H (memory safety, deniability).

**Benefit**: Cross-firm finding-comparison catches blind spots; redundancy on critical modules. **Cost**: ~$300K–$350K total (vs. $250K–$300K single firm).

**Coordination**: Firms participate in a joint findings-review call at Week 8 (preliminary results); Calm facilitates information sharing (findings, methodology notes) between the two auditors.

---

## Bug-bounty companion (Everest 287)

Parallel to the audit engagement, Calm shall launch a HackerOne or Bugcrowd bug-bounty program with the following structure:

- **Duration**: Launch at audit start; close at 6 months post-publication of the public audit report.
- **Scope**: Calm Witness codebase (all published commit hashes); wire-format implementations; cryptographic bindings (Sigsum, Roughtime).
- **Bounty range**: $1K–$50K based on severity (Critical: $30K–$50K; High: $10K–$25K; Medium: $3K–$10K; Low: $1K–$3K).
- **Audit firm coordination**: Findings reported to the bug-bounty program that are live exploits shall be coordinated with the audit firm; the auditor's preliminary findings take precedence, and live-exploit bounties are paid after the audit report is public (no disclosure races).

---

## Right-to-defend + remediation closure

- **Calm has 30 days** from receipt of preliminary audit findings to propose a remediation plan (code + tests) for each finding.
- **Auditor has 14 days** to review the remediation and confirm it addresses the root cause.
- **If root-cause fix is rejected**, Calm and auditor discuss alternative mitigations; unresolved findings are escalated to Calm board + auditor firm leadership.
- **No findings are marked "wontfix"** without written board-level justification; all "wontfix" items are published in the final report.

---

## Acceptance criteria for this RFP

This RFP is **complete** when:

1. **Firm identified**: A named auditing firm (Trail of Bits, NCC Group, Cure53, Least Authority, ConsenSys Diligence, or equivalent) has signed a statement of work specifying modules in scope, timeline, deliverables, and budget.
2. **Written engagement letter**: Firm and Calm have signed a legal engagement letter including conflict-of-interest disclosures, publication rights, and limitation-of-liability terms.
3. **Audit start**: First kickoff call scheduled and preliminary work plan (team, tools, test-environment setup) has been agreed in writing.

---

## Composition + dependencies

- **Everest 81** — Rust production implementation (codebase under audit).
- **Everest 90** — Audit-ready packet (threat model, specs, test vectors, fuzzer history).
- **CALM_WITNESS_WIRE_FORMAT_v0.md** — Wire format and canonical-JSON encoding specification.
- **Everests 44–48, 65, 96** — Cryptographic core specs (Pedersen, Bulletproofs, Schnorr, range proofs, post-quantum migration).
- **Everests 58, 99** — Deniability + anti-purity-test guards.
- **Everest 287** — Parallel bug-bounty program.

---

— Musk
*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
