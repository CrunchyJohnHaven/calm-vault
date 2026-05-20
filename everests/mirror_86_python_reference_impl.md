# Mirror Everest 86 — Python Reference Implementation

**Phase XV — Engineering Reliability. Prereq: Everest 40, 58.**

---

## What this summit ships

A production-ready Python package implementing the full Calm Mirror protocol at protocol-clarity level, suitable for embedding in research notebooks, conformance harnesses, integration tests, and counterparty verification stacks. This is the reference implementation that defines protocol semantics; Everest 87 (Rust production) will compile to bit-stable output against this.

The package is distributed as `calm-mirror` on PyPI, installable via `pip install calm-mirror`, with comprehensive documentation and determinism harness for cross-implementation conformance.

---

## Package structure

```
calm_mirror/
  __init__.py              # 42-symbol public API
  __main__.py              # CLI entry point
  cli.py                   # calm-mirror binary interface
  parse.py                 # Behavior-evidence record parsing (Everest 11)
  predicates.py            # Values vocabulary v0 (Everest 5)
  predicate_eval.py        # The 7 v0 value predicates (Everest 27-33)
  aligned_bit.py           # Pedersen commitments (Everest 42)
  mpc.py                   # Two-party MPC, v0 trusted-coordinator (Everest 58)
  zk_proofs.py             # ZK proofs of alignment + MPC correctness (Everest 43, 59)
  disclosure.py            # Mirror exchange envelope (Everest 49)
  consent.py               # Per-counterparty values consent (Everest 46)
  withhold.py              # Withhold-any-bit machinery (Everest 51)

golden/                    # Golden test corpus (empty in v0; populated by Everest 64)

tests/
  __init__.py
  test_parse.py            # Behavior-evidence parsing
  test_predicates.py       # Predicate evaluation
  test_alignment.py        # MPC + ZK proofs
  test_disclosure.py       # Full end-to-end exchanges
  test_properties.py       # Property-based invariants (hypothesis)
  test_conformance.py      # Cross-language vectors (Python <-> Rust)

examples/
  basic_predicate_eval.py  # Load chain, evaluate unselfishness_evidence
  mirror_exchange.py       # Full two-party exchange end-to-end
  prove_alignment.py       # Generate and verify ZK proof

README.md                  # Usage guide, five canonical examples
pyproject.toml             # PEP 621; Python 3.10+; pinned deps
```

---

## Two integration modes

### Mode 1: Pure Python (reference and prototyping)

No Rust dependency. All cryptographic primitives implemented in Python:

- **Behavior-evidence parsing:** JSON schema validation via `jsonschema`, JSONL parsing.
- **Predicate evaluation:** Pure-Python evaluators for all seven v0 predicates; deterministic, no side effects.
- **Pedersen commitments:** Via `py_ecc` (Ristretto255 arithmetic) or RFC 3526 MODP-2048 fallback.
- **ZK proofs (Everest 43, 59):** Stub implementations in v0; placeholder proof format for determinism harness.
- **Two-party MPC (Everest 58):** Trusted-coordinator mode v0 (simplified for reference); real 2PC deferred to v1.
- **Disclosure envelope:** JSON serialization, Ed25519 signing via `cryptography`.

**Acceptance:** Mode 1 is the canonical reference. Every mode-2 (Rust-backed) call must produce identical output on the same input when run against the same golden test corpus.

### Mode 2: Rust-backed via PyO3 (production parity)

Optional Rust FFI bindings to `calm-mirror-rs` (Everest 87). When installed with `pip install calm-mirror[rust]`, expensive operations (MPC, ZK proofs, commitments on Ristretto255) delegate to compiled Rust. Same API, 10–100x faster.

Mode 2 is not a hard requirement for v0; it is the optimization path for agents running high-throughput disclosure pipelines.

---

## Public API (42 symbols)

```python
from calm_mirror import (
    # Parsing
    BehaviorEvidenceRecord, EvidenceKind, parse_behavior_evidence,
    # Predicates
    PREDICATE_VOCABULARY_V0, PredicateRegistry, load_predicates,
    unselfishness_evidence, tribal_neutrality_evidence,
    respect_for_difference_evidence, non_harm_evidence,
    growth_arc_evidence, truth_telling_evidence,
    apology_when_wrong_evidence,
    # Evaluation
    Tri, PredicateResult, EvaluationContext, evaluate_predicate,
    tri_and, tri_or, tri_not,
    # Cryptography
    AlignedBitCommitment, commit_aligned_bit, verify_aligned_bit,
    AlignmentProof, prove_alignment, verify_alignment_proof,
    # MPC
    MPCContext, compute_intersection_bits,
    # Disclosure
    DisclosureRequest, DisclosureResponse, MirrorEnvelope,
    build_mirror_exchange, verify_exchange,
    # Consent & withhold
    ConsentRecord, ConsentStatus, check_per_counterparty_consent,
    WithholdBitGuarantee, assert_withhold_enabled,
)
```

All operations raise explicit exception types; no silent failures. All functions are deterministic; same input → same output, every time.

---

## Dependency pinning and compatibility

```toml
[dependencies]
python = ">=3.10"
py-ecc = "~=6.0"           # Ristretto255 + MODP arithmetic
jsonschema = "~=4.20"      # Behavior-evidence schema validation
cryptography = "~=42.0"    # Ed25519 signing/verification
msgpack = "~=1.0"          # Wire-format serialization

[optional-dependencies]
rust = ["calm-mirror-rs == 0.1.0"]  # PyO3 Rust backend
```

All dependencies are version-pinned to exact minor; patch updates via Dependabot with manual review.

---

## Security and quality disciplines

- **No panics / exceptions in production paths.** All errors are explicit; verifier exceptions are catchable.
- **No secrets in tracebacks.** All exception messages are sanitized; keys, seeds, and evidence hashes never appear in error text.
- **Constant-time cryptography.** Comparison via `hmac.compare_digest()` (Python 3.3+). Scalar multiplication delegated to `py_ecc` (constant-time by design).
- **Buffer zeroing.** All buffers holding randomness or keys are explicitly overwritten before GC.
- **Reproducible builds.** Proof generation uses deterministic PRNG seeding (RFC 6979 extended to commitments); same input always yields same output.
- **Type safety.** Python 3.10+ pattern matching + dataclasses + `mypy --strict` passes clean.
- **Test coverage.** Target ≥85% line coverage; `coverage.py` gates PR merges.

---

## Cross-language conformance (Everest 87)

The same golden test corpus drives both Python and Rust implementations:

```python
# conformance/run_determinism_harness.py
for predicate_id in PREDICATES_V0:
    for case in load_golden_corpus(predicate_id):
        py_result = evaluate_python(predicate_id, case)
        rs_result = evaluate_rust(predicate_id, case)
        assert py_result == rs_result, f"Divergence on {case}"

for (envelope_spec,) in load_disclosure_cases():
    py_envelope = build_exchange_python(envelope_spec)
    rs_envelope = build_exchange_rust(envelope_spec)
    assert py_envelope == rs_envelope  # Byte-for-byte with deterministic PRNG
```

Conformance violations surface immediately in CI; bar is bit-stable output across all Mirror v0 test cases.

---

## Acceptance criteria

**T-M86.1 (API stability).** The 42 public symbols in `__init__.py` are frozen per semver; breaking changes only in major versions.

**T-M86.2 (Mode 1 test parity).** Every test passes in pure-Python mode; hypothesis discovers no counterexamples to the property suite.

**T-M86.3 (Conformance with Rust).** All predicate-evaluation cases + all disclosure-envelope cases run against both Python and Rust; byte-for-byte output match on proofs, tri-state match on predicates.

**T-M86.4 (Performance floor).** Pure-Python end-to-end disclosure (7 predicates, envelope construction + verification) completes in ≤5 seconds on commodity hardware (macOS M-series, Ubuntu 22.04 x86). Rust mode: ≤500ms.

**T-M86.5 (Documentation completeness).** Every public function has docstring with signature, semantics, exceptions, and usage example. README contains five canonical code examples with expected output.

**T-M86.6 (PyPI publication).** Package published under PyPI namespace `calm-mirror` by Calm Foundation; wheels for Python 3.10–3.13 on manylinux_2_28, macosx_13_0, win_amd64.

**T-M86.7 (Integration with Everest 87).** When Rust production implementation ships, conformance harness runs daily; any divergence surfaces within 2 hours of commit.

---

## Use cases

1. **Research notebooks.** Cryptographers load a live behavior-evidence chain, evaluate predicates, reason about protocol behavior without Rust compilation. Code cells are short; results appear inline.

2. **Counterparty verification.** A financial institution or AI-agent collective embeds `calm_mirror.verify_exchange()` in their Python service (FastAPI, Django) to validate incoming Mirror disclosures without production Rust infrastructure.

3. **Cross-implementation conformance tests.** The determinism harness runs the same test corpus against Python and Rust; divergence is a bug. The harness itself is written once in pytest; Rust harness mirrors it in Criterion.

4. **Integration tests in dependent services.** A principal's Calm agent and a counterparty's verifier both import `calm_mirror`; their unit tests exercise full round-trip (chain load, predicate evaluation, MPC, proof generation, verification) in CI.

5. **Rapid prototyping.** A new predicate or proof strategy sketched in Python, tested against the corpus, and validated against Rust reference before production Rust code.

---

## Composition with Everest 87

This package ships before Rust production. The critical path (Everest 1–79, 85) was complete before Everest 87 design finalized. Python reference lets counterparty operators and researchers start building immediately; Rust comes next for operator-side hot path.

When Everest 87 lands, the conformance harness becomes a permanent CI step. Any future predicate addition or protocol revision must pass the harness first; Python and Rust outputs must match.

---

## What we are NOT shipping in v0

- **Custom-predicate DSL.** Everest 5 chose a fixed predicate table for v0; DSL is deferred to v1.
- **Real 2PC.** MPC uses trusted-coordinator mode (simplified); real garbled-circuits or SPDZ is Everest 58 v1 scope.
- **Full ZK backend.** Proofs are stubs in v0; Bulletproofs or SNARK backend lands in v1 (Everest 59 follow-on).
- **Hardware wallet integration.** Signing is software Ed25519; hardware-key binding is future.
- **Multi-principal federation.** One vault = one principal; multi-vault is v1+.

---

## Signing

**Gate script:** `everest_86_python_reference_impl_gate.py`.

**Signoff:** Acceptance of T-M86.1 through T-M86.7 closure. Code review by Calm Witness reference author (to verify architectural parity). Conformance harness green against Rust reference once Everest 87 ships.

— Calm, 2026-05-20
