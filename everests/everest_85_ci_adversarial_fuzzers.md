# Everest 85 — CI with Adversarial Fuzzers

*Phase VII — Engineering Reliability. Prereq: Everest 81.*

## Decision

Calm Witness must withstand adversarial attack. Property-based testing (Everests 86–87) verifies logical invariants; fuzzing attacks at the byte level and the implementation level. We adopt a nightly adversarial fuzzing pipeline that exercises eight critical targets with coverage-guided fuzzers, maintains persistent corpora, auto-reduces crash traces, and enforces zero flakes over thirty consecutive days before v0 release. Fuzzing integrates into the existing `*_siege_gate.mjs` pattern from the CredexAI scripts library, composing with property tests and benchmarking in one unified CI gate.

## Threat Model & Scope

Fuzzing defends against:
- **Parser chaos:** Adversarial user_state.jsonl byte sequences that crash or misbehave the chain parser.
- **Cryptographic oracle misuse:** Malformed ZK proofs, wrong group elements, broken Fiat-Shamir transcripts.
- **Predicate logic abuse:** Boundary inputs (NaN, Infinity, negative distances), out-of-order timestamps, malformed JSON payloads.
- **Chain mutation attacks:** Arbitrary byte modifications, hash-chain breaks, out-of-order records designed to confuse verifiers.
- **Consent calculus confusion:** Overlapping, conflicting, or time-wound consent records; replay attempts.
- **Disclosure request injection:** Malformed request objects, oversize predicates, cross-session nonce reuse.
- **State-machine confusion:** Enrollments interrupted, template rotations during active disclosures, concurrent vault mutations.
- **Biometric distance bleed:** Constructed samples designed to generate Infinity or NaN distances; SVG injection via voice transcripts.

Out of scope: side-channel attacks (timing analysis, power analysis) and cryptographic breaks (discrete-log attacks, Fiat-Shamir vulnerabilities in the theoretical sense—we assume the underlying primitives hold).

## Fuzz Target Inventory

**F1: Chain Parser (user_state.jsonl)** — byte-level chaos at JSONL parse boundary. Generates truncated, overlong, invalid-UTF8, deeply-nested, and maliciously-ordered JSON arrays. Entry point: `calm_witness::parse::parse_chain()` (Rust) and `calm_witness.parse.parse_chain()` (Python). Corpus seeded with: valid chains (Everest 26 golden set), single-record chains, genesis blocks with alternate prev_hash values, and records with all optional fields present/absent. Crash detector: any panic, unwrap, or OOM.

**F2: Hash-Chain Verifier** — mutation attacks on valid chains. Generator: takes a valid chain, selects a random record, flips 1–8 random bits in non-hash fields, and tests that verification correctly detects the break. Entry point: `calm_witness::verify_chain()`. Corpus: all test vectors from Everest 86 (property-based tests + golden regression cases). Crash detector: panics; false-accept detector: verifier returns PASS when it should return FAIL.

**F3: Predicate Evaluators** — boundary inputs and malformed payloads. Per-predicate fuzzers targeting (a) time-window predicates with extreme timestamps (y2038, epoch, negative), (b) biometric comparators with Inf/NaN distances, (c) consent records with overlapping/revoked windows, (d) baseline-affect JSON with escape-sequence injection, (e) codeword hashes with case-sensitivity edge cases. Entry points: `calm_witness::predicate_eval::evaluate()` (all six v0 predicates). Corpus: Everest 64 golden corpus + adversarial time-boundary cases. Crash detector: panics, assertion failures, unwrap on Option.

**F4: ZK Proof Verifiers** — malformed and forged proofs. Generates: wrong group elements, mismatched commitments, broken Fiat-Shamir challenges, oversized scalars, canonical-form violations, cross-predicate proof swaps. Entry point: `calm_witness::zk::verify_proof()` (Everest 65 kernel set). Corpus: valid proofs from Everest 65 golden set + single-bit mutations. Crash detector: panics and false-accept detector: verifier returns PASS on invalid proof.

**F5: Disclosure Request Parser** — adversarial request JSON. Generates: missing fields (predicate_id, nonce, freshness_window), oversized arrays (>1000 predicates), invalid predicate IDs, cross-session nonce reuse, type confusion (string where int expected). Entry point: `calm_witness::envelope::parse_disclosure_request()`. Corpus: valid requests from integration tests + mutation variants. Crash detector: panics, false-accept (parser returns success on invalid request).

**F6: Disclosure Response Generator** — consistency under stress. Fuzzes: multi-predicate response generation with partial consent failures, response size growth with N predicates, proof-composition error recovery. Entry point: `calm_witness::envelope::generate_disclosure_response()`. Corpus: valid single-predicate and multi-predicate responses + edge cases (0 predicates, max predicates). Crash detector: panics, assertion failures.

**F7: Enrollment Ceremony State Machine** — interrupted and concurrent operations. Fuzzes: enrollment step out-of-order, template commit/abort races, biometric re-sample during consensus. Entry point: `calm_witness::enrollment::ceremony_fsm()`. Corpus: linear ceremony traces + random interleaving of steps. Crash detector: panics, invariant violations (template committed twice, contradictory state).

**F8: Template Parser (FlatBuffers)** — invalid binary template format. Generates: truncated buffers, oversized fields, unaligned offsets, null-pointer attacks on optional nested tables. Entry point: `calm_witness::template::parse_template()`. Corpus: valid template binaries (Everest 15 format spec) + bit-flip mutations. Crash detector: panics, out-of-bounds reads.

## Fuzzer Tools & Configuration

**Coverage-guided fuzzers:**
- **Rust:** `cargo-fuzz` (libFuzzer backend). Per target, fuzz code lives in `.cargo/fuzz/fuzz_targets/f<N>_<name>.rs`. Coverage is collected via LLVM instrumentation; corpus is auto-managed in `.cargo/fuzz/corpus/<target>/`.
- **Python:** `atheris` (Python wrapper over libFuzzer). Per target, fuzz driver in `calm_witness/fuzz/f<N>_<name>.py`. Corpus in `calm_witness/fuzz/corpus/<target>/`.

**Adversarial mutators (custom):**
- Chain mutator: byte-flip per record, prev_hash scramble, seq-order randomization, timestamp inversion, kind-field corruption.
- Predicate mutator: time-boundary shifts (±48h, ±1000y), distance float encoding (sign flip, exponent overflow), JSON key reorder, consent-window boundary collision.
- Proof mutator: group-element coordinate scramble, challenge e truncation, response z sign flip, commitment hash zeroing.

**Corpus management:**
- Initial seed corpus per target: 5–10 hand-crafted minimal valid inputs.
- Coverage-driven corpus: libFuzzer automatically saves inputs that increase coverage. Corpus persists in `tests/fuzz/<target>/corpus/` and `calm_witness/fuzz/corpus/<target>/`.
- Crash persistence: any input that triggers a crash is saved to `tests/fuzz/<target>/crashes/<target>-<hash>.input` (Rust) and `calm_witness/fuzz/crashes/<target>-<hash>.bin` (Python) for manual review and regression testing.
- Corpus minimization: nightly job runs `cargo fuzz cmin` (Rust) and custom Python minimizer to remove redundant corpus entries and keep peak corpus size <100 MB.

## Schedule & Flake Tolerance

**On-PR (gating):** 5-minute coverage-guided fuzz per target, run in parallel on 4 cores, all eight targets in series (20 minutes total). PR fails if any fuzzer finds a crash or false-accept. Crash is minimized and attached to PR comment.

**Nightly (release-readiness):** 8-hour fuzz per target (64 CPU-hours total distributed across 8-way parallelism). All targets fuzz independently; any crash triggers auto-triage.

**Weekly (multi-chain):** 24-hour fuzz run with crash-minimization pass and corpus consolidation. Crashing inputs from the week are re-tested to confirm they are deterministically reproducible (not flukes).

**Quarterly (paid compute):** 1-week fuzz on rented 32-core hardware with coverage-guided and mutation-guided strategies (AFL++ MOPT mode). Results feed into an annual fuzzing report.

**Flake rules:** Any flaky crashes (non-deterministic) are flagged as Severity S2 "fuzzing reliability risk" and assigned to the implementation owner for investigation. The gate permits max 1 flaky crash per week; >1 flake blocks release. Once a crash is non-deterministic (retest shows it doesn't always trigger), it is quarantined and re-triaged monthly. Thirty consecutive days with zero new crashes and zero unresolved flakes clears the gate for v0 release.

## Integration with Siege-Gate Pattern

Calm Witness fuzzing composes with CredexAI's siege-gate convention:

```
~/calm-witness/scripts/everest_85_zkbb_adversarial_fuzzers_siege.mjs
```

Structure:
1. Orchestrator node script (MJS): invokes Rust and Python fuzz targets in series.
2. Harness (Rust + Python): per-target fuzz driver with liveness checks.
3. Result aggregation: JUnit XML output from each target, combined into a single gate report.

Example siege gate structure (mirrors `aao_billing_rail_gate.mjs`):

```javascript
/**
 * Everest 85 — CI with Adversarial Fuzzers.
 * Fuzzing siege gate: 8 targets (F1–F8) × property tests + benchmarks.
 */
const GATE = "GATE_EVEREST_85_ADVERSARIAL_FUZZERS";

const FUZZ_TARGETS = [
  { id: "F1", name: "chain-parser", timeout_s: 300, rust: true, python: true },
  { id: "F2", name: "hash-chain-verifier", timeout_s: 300, rust: true, python: true },
  { id: "F3", name: "predicate-evaluators", timeout_s: 300, rust: true, python: true },
  { id: "F4", name: "zk-proof-verifiers", timeout_s: 300, rust: true, python: false },
  { id: "F5", name: "disclosure-request-parser", timeout_s: 300, rust: true, python: true },
  { id: "F6", name: "disclosure-response-generator", timeout_s: 300, rust: true, python: true },
  { id: "F7", name: "enrollment-fsm", timeout_s: 300, rust: true, python: false },
  { id: "F8", name: "template-parser", timeout_s: 300, rust: true, python: false },
];

const SCENARIOS = [
  {
    id: "PR-fuzz",
    mode: "quick",
    run_time_s: 5 * 60,
    coverage_required: true,
    expected: "zero crashes",
  },
  {
    id: "nightly-fuzz",
    mode: "extended",
    run_time_s: 8 * 60 * 60,
    coverage_required: true,
    crash_min: true,
    expected: "zero flake crashes",
  },
  {
    id: "weekly-replay",
    mode: "regression",
    run_time_s: 60,
    inputs: "crash-corpus",
    expected: "all crashes reproducible",
  },
];
```

Exit codes match credex gate convention: 0 = green, 1 = flake detected, 2 = tool failure.

## Flake Triaging & Crash Analysis

Every crash found by the fuzzer is automatically:
1. **Minimized** via libFuzzer's crash-min algorithm (reduces to <1 KB input).
2. **Serialized** to `crashes/<target>-<timestamp>-<hash>.input`.
3. **Triage-ticketed** by the orchestrator with severity (S1 = panic/OOM, S2 = assertion, S3 = slow regression).
4. **Assigned** to the implementation owner (module-based routing).
5. **Regression-added** to the corpus after fix verification.

Flake detection: if a crash input cannot be reproduced in 3 consecutive runs on the same code commit, it is marked flaky and escalated (Severity S2 "fuzzing infrastructure concern").

## Coverage Targets & Metrics

- **Branch coverage:** >85% per fuzz target. Measured via LLVM coverage instrumentation, tracked in CI dashboard.
- **Line coverage:** >90% in all modules touched by fuzzing entry points.
- **Crash-free days:** counter that increments daily if zero new crashes found; resets on new crash. Target: 30 consecutive days before v0 release.
- **Corpus growth rate:** if corpus grows >1 MB/day, investigation required (indicates divergence or overfitting in generators).

Coverage reports are published to S3 (or equivalent) weekly; diffs between weekly reports highlight coverage regressions.

## Adversarial Generators

**Chain mutator:** (Rust `arb_adversarial_chain`)
- Valid chain input → select 1–3 records → per-record: (a) flip 1–8 bits in non-hash payload, (b) scramble prev_hash with random bytes, (c) duplicate seq number, (d) invert timestamp, (e) corrupt kind field.
- Recompute only the selected record's record_hash (NOT downstream), leaving the chain broken but locally-valid-looking at that record.

**Predicate mutator:** (Python `mutate_predicate_inputs`)
- Time window predicates: shift `now` by ±1000 years, ±48 hours (boundary conditions), or epoch edge cases (y2038).
- Distance predicates: apply sign flip to distance, set to Infinity/NaN, or apply IEEE-754 exponent overflow.
- Consent records: create overlapping windows, revoked-then-regrant, and boundary-colliding windows (window1.end == window2.start).
- Baseline affect: inject JSON escape sequences, null bytes, deeply nested keys (>100 levels), and out-of-vocabulary affect strings.

**Proof mutator:** (Rust `mutate_zk_proof`)
- Commitment mutation: zero out one coordinate of the group element, or apply random scalar multiplication.
- Challenge mutation: truncate the Fiat-Shamir hash to 8 bits (instead of 256), or apply XOR with a fixed bit mask.
- Response mutation: flip the sign of the response scalar z, or set it to 0 mod q.

## Deliverables & Integration Points

**Rust fuzzing targets:**
- `.cargo/fuzz/fuzz_targets/f1_chain_parser.rs` through `f8_template_parser.rs`
- `.cargo/fuzz/corpus/<target>/` (persistent corpus directory)
- `.cargo/fuzz/artifacts/` (crash artifacts auto-saved by libFuzzer)

**Python fuzzing drivers:**
- `calm_witness/fuzz/f1_chain_parser.py` through `f6_disclosure_response_generator.py`
- `calm_witness/fuzz/corpus/<target>/` (persistent corpus)
- `calm_witness/fuzz/crashes/` (minimized crash inputs)

**Orchestrator:**
- `~/calm-witness/scripts/everest_85_zkbb_adversarial_fuzzers_siege.mjs` — siege gate wrapper
- `.github/workflows/fuzz-nightly.yml` — nightly CI job
- `.github/workflows/fuzz-on-pr.yml` — PR gate (5-minute quick run)

**Reporting:**
- `fuzz_report_weekly.json` — corpus stats, crash count, coverage delta
- `fuzz_crashes_open.md` — open triage tickets (auto-generated)
- `coverage-diff-week-over-week.html` — coverage regressions flagged

## Composition with Everests 81–87

**Everest 81 (Rust Production Implementation):** Fuzzing targets are integrated directly into the Rust crate under `tests/fuzz/`. The implementation must compile without warnings when `--fuzzing` is set.

**Everest 82 (Python Reference Implementation):** Python fuzz drivers test the same code paths. Cross-language conformance: if F2 (hash-chain verifier) finds a crash in Rust, the same crash input is run against Python to confirm the bug is in the logic, not the language.

**Everest 86 (Property-Based Tests for Hash Chain):** Properties define the correct behavior; fuzzers attack it. Both run in CI. Property tests are deterministic (regression corpus); fuzzers are adversarial (crash corpus).

**Everest 87 (Property-Based Tests for Predicates):** Predicate properties guarantee monotonicity and idempotence; predicate fuzzers attack boundary conditions and malformed inputs that properties may not explore.

## Flake-Free Definition & Release Gate

"Flake-free for ≥30 days" means:
- All eight targets have run for at least 30 consecutive calendar days without triggering a non-deterministic crash.
- Deterministic crashes are allowed if they are fixed, added to regression corpus, and re-pass the weekly replay.
- Flaky crashes (crashes that come and go non-deterministically) block the gate.

The release gate checks: `crash_free_days ≥ 30 AND flaky_crashes == 0`. If either condition fails, v0 cannot ship until the condition is met.

---

— Calm, 2026-05-20
