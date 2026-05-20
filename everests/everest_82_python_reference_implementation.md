# Everest 82 — Python Reference Implementation

*Phase VII — Engineering Reliability. Prereq: Everest 81.*

---

## What this summit ships

A production-ready Python package implementing the full Calm Witness protocol at protocol-clarity level, suitable for embedding in research notebooks, conformance harnesses, integration tests, and counterparty verification stacks. This is the reference implementation that defines protocol semantics; Everest 81 (Rust production) will compile to bit-stable output against this.

The package is distributed as `calm-witness` on PyPI, installable via `pip install calm-witness`, with comprehensive documentation, Jupyter notebook tutorials, and a test corpus shared with the Rust implementation.

---

## Package structure

```
calm_witness/
  __init__.py              # 31-symbol public API: Chain, Predicate, Prove, Verify, etc.
  chain.py                 # Chain load, append, verify; hash-chain core
  predicate.py             # Predicate value classes; evaluation result types
  prove.py                 # Disclosure proof generation; envelope construction
  verify.py                # Proof verification; freshness anchor checks
  disclose.py              # Disclosure request/response semantics
  _ffi.py                  # Optional Rust FFI bindings (MODE 2 only)
  _crypto.py               # Pedersen commitments, Bulletproofs range proofs
  _parse.py                # JSONL schema parsing + validation
  _envelope.py             # Disclosure envelope structure + serialization

tests/
  test_chain.py            # Chain verification properties
  test_predicates.py       # Predicate evaluation + composition
  test_proofs.py           # Proof generation/verification round-trips
  test_properties.py       # Hypothesis-based invariants
  test_conformance.py      # Cross-language vector sets (Rust parity)

examples/
  basic_chain_verify.py    # Load vault; verify chain; print status
  predicate_eval.py        # Evaluate `in_baseline_24h` against live chain
  generate_disclosure.py   # Full end-to-end: prove + verify
  notebook_tutorial.ipynb  # Jupyter walkthrough for researchers

pyproject.toml             # PEP 621; Python 3.10+; pinned deps
README.md                  # Usage guide; 5 canonical examples
```

---

## Two integration modes

### Mode 1: Pure Python (research and prototyping)

No Rust dependency. All cryptographic primitives implemented in Python:

- **Chain verification:** SHA-256 hash-chain walking, JSON-Schema validation via `jsonschema`, append-only JSONL parsing.
- **Pedersen commitments:** Via `py_ecc` (elliptic curve arithmetic over Ristretto255, RFC 3526 MODP-2048 fallback for portability).
- **Range proofs (Bulletproofs):** Via `py_bulletproofs` (native Python range-proof generator and verifier; ~10x slower than Rust but fully compatible).
- **Predicate evaluation:** Pure-Python evaluators for all six v0 predicates (`in_baseline_24h`, `biometric_match_within`, `principal_consents_to_disclose`, `bank_teller_note_active`, `cognitively_atypical_baseline`, `mental_state_unusual`); deterministic, no side effects.
- **Envelope construction:** Serialization to JSON, Ed25519 signing via `cryptography`, proof assembly.

**Acceptance:** Mode 1 is the canonical reference. Every mode-2 (Rust-backed) call must produce identical output on the same input when run against the same golden test corpus.

### Mode 2: Rust-backed via PyO3 (production parity)

Optional Rust FFI bindings to `calm-witness-rs` (Everest 81). When installed with `pip install calm-witness[rust]`, expensive operations (`prove_bit`, range-proof generation, commitments on Ristretto255) delegate to compiled Rust. Same API, 10–100x faster.

Mode 2 is not a hard requirement for v0; it is the optimization path for agents running high-throughput disclosure pipelines.

---

## Public API

```python
from calm_witness import Chain, Predicate, Prove, Verify

# Load a vault
chain = Chain.load('~/.calm-vault/user_state.jsonl')

# Verify structural and cryptographic integrity
chain.verify()  # Raises ChainVerificationError if invalid

# Evaluate a predicate
bit, freshness_window = Predicate.evaluate(
    'in_baseline_24h',
    chain=chain,
    baseline_vocabulary=chain.baseline_from_enrollment()
)
assert bit in {True, False, None}  # None = undetermined

# Generate a disclosure proof (Mode 1 or Mode 2)
proof = Prove.generate(
    predicate_id='in_baseline_24h',
    chain=chain,
    counterparty_vc=json.loads(open('counterparty.json').read()),
    nonce='unique-per-request-uuid',
    consent_record=chain.latest_consent('in_baseline_24h', 'financial')
)

# Verify the proof (counterparty side)
Verify.verify_proof(
    proof=proof,
    verifier_sigsum_logs=['https://log.sigsum.org/...'],
    verifier_roughtime_servers=['https://roughtime.google.com', ...]
)  # Raises ProofVerificationError if invalid
```

All operations raise explicit exception types; no silent failures. All functions are deterministic; same input → same output, every time.

---

## Dependency pinning and compatibility

```toml
# pyproject.toml [dependencies]
python = ">=3.10"
py-ecc = "~=6.0"           # Ristretto255 + MODP arithmetic
py-bulletproofs = "~=0.2"  # Range proofs (pure Python)
jsonschema = "~=4.20"      # JSONL schema validation
cryptography = "~=42.0"    # Ed25519 signing / verification
msgpack = "~=1.0"          # Wire-format serialization

# Optional
calm-witness-rs = {version = "~=0.1", optional = true}  # Rust backend
```

All dependencies are version-pinned to exact minor; patch updates via Dependabot with manual review. No `python-dateutil`, `pandas`, `numpy`, or other heavy dependencies; the module is lightweight enough to embed in notebooks.

---

## Security and quality disciplines

- **No panics / exceptions in production paths.** All errors are explicit; verifier exceptions are catchable and introspectable.
- **No secrets in tracebacks.** All exception messages are sanitized; cryptographic values (seeds, private scalars, biometric templates) never appear in error text or repr.
- **Constant-time cryptography.** Comparison operations use `hmac.compare_digest()` (Python 3.3+). Scalar multiplication on elliptic curves delegated to `py_ecc` (constant-time by design).
- **Buffer zeroing.** All buffers holding randomness, keys, or biometric data are `bytes` instances; when no longer needed, explicitly overwritten with `os.urandom(len(buf))` before GC.
- **Reproducible builds.** Proof generation uses deterministic PRNG seeding from RFC 6979 (DSA/ECDSA deterministic-nonce scheme extended to commitments); same input always yields same output, enabling diff debugging.
- **Type safety.** Python 3.10+ pattern matching + dataclasses + explicit type hints throughout; `mypy --strict` passes clean.
- **Test coverage.** Target ≥85% line coverage on `_crypto.py` and `chain.py`; `coverage.py` gates PR merges.

---

## Cross-language conformance

The same golden test corpus (Everests 64, 86, 87) drives both Python and Rust implementations. CI harness:

```python
# conformance/run_determinism_harness.py (pseudo)
for predicate_id in PREDICATES_V0:
    for case in load_golden_corpus(predicate_id):
        py_result = evaluate_python(predicate_id, case)
        rs_result = evaluate_rust(predicate_id, case)
        assert py_result == rs_result, f"Divergence on {case}"

for (chain_head, proof_spec) in load_proof_cases():
    py_proof = prove_python(chain_head, proof_spec)
    rs_proof = prove_rust(chain_head, proof_spec)
    # Deterministic PRNG ensures byte-for-byte match
    assert py_proof == rs_proof
```

Conformance violations surface immediately in CI; the bar is bit-stable output across all 193 predicate test cases (Everest 64) plus 50+ property-based hypothesis-generated cases (Everests 86, 87).

---

## Distribution and discoverability

- **PyPI package:** `calm-witness` maintained by Calm Foundation; package index shows version history, readme, dependencies.
- **Documentation:** Sphinx-built HTML + PDF at `python.calmwitness.thecreativitymachine.ai` (same DNS structure as Calm Pact). README badges (PyPI, CI/CD, coverage, docs) point to all four.
- **Pre-built wheels:** `pip install calm-witness` pulls the wheel matching the user's Python version and platform (cp310-py310-manylinux_2_28_x86_64, macosx_13_0_arm64, win_amd64, etc.). Mode 2 (Rust backend) ships as an optional extra wheel.
- **Jupyter notebook tutorials:** `examples/notebook_tutorial.ipynb` runs in Google Colab, Binder, or local JupyterLab without special setup; loads a sample chain and runs the five canonical use cases end-to-end.

---

## Acceptance criteria

**T-82.1 (API stability).** The 31 public symbols exported in `__init__.py` are frozen per semver; breaking changes only in major versions.

**T-82.2 (Mode 1 test parity).** Every test passes in pure-Python mode; hypothesis discovers no counterexamples to the property suite.

**T-82.3 (Conformance with Rust).** 193 golden predicate-evaluation cases + 50+ property-based cases run against both Python and Rust implementations; byte-for-byte output match on proofs, bit-match on predicates.

**T-82.4 (Performance floor).** Pure-Python end-to-end disclosure round-trip (2–4 predicates, envelope construction + verification) completes in ≤2 seconds on commodity hardware (macOS M-series, Ubuntu 22.04 x86, Windows 11); 5-predicate envelope in ≤5 seconds. (Rust mode: ≤500ms / ≤1s respectively.)

**T-82.5 (Documentation completeness).** Sphinx-built docs render cleanly; every public function has a docstring with signature, semantics, exceptions, and a usage example; `README.md` contains five canonical code examples with expected output.

**T-82.6 (PyPI publication).** Package published under PyPI namespace `calm-witness` by Calm Foundation; wheels for Python 3.10, 3.11, 3.12, 3.13 on manylinux_2_28, macosx_13_0, win_amd64; `pip install calm-witness` succeeds on all platforms.

**T-82.7 (Integration with Everest 81).** When Rust production implementation ships, conformance harness runs daily; any divergence in output is surfaced as a failing test within 2 hours of commit.

**Gate script:** `everest_82_86_87_zkbb_python_ref_impl_gate.py`.

---

## Use cases this enables

1. **Research notebooks.** Cryptographers and AI-safety researchers load a live chain, evaluate predicates, and reason about protocol behavior without needing to compile Rust. Code cells are short; results appear inline.

2. **Counterparty verification stacks.** A financial institution or AI-agent collective embeds `calm-witness.Verify` in their own Python service (Django, FastAPI, etc.) to validate incoming disclosure proofs without needing production Rust infrastructure; Mode 2 (Rust backend) is an optional upgrade.

3. **Cross-implementation conformance tests.** The determinism harness runs the same test corpus against Python and Rust; divergence is a bug. The harness itself is written once in pytest; the Rust harness mirrors it in Criterion.

4. **Integration tests in dependent services.** A principal's Calm agent and a counterparty's verifier both import `calm-witness`; their unit tests exercise the full round-trip (chain construction, proof generation, verification) in CI without a live Sigsum transparency log or Roughtime quorum.

5. **Rapid prototyping.** A new predicate or proof strategy can be sketched in Python, tested against the corpus, and validated against the Rust reference before investing in production Rust code.

---

## Composition with Everest 81

This package is intentionally shipped before the Rust production implementation. The critical path (Everests 1–79, 92) was complete before Everest 81 design was finalized. Python reference lets counterparty operators and researchers start building and testing immediately; Rust comes next for the operator-side hot path.

When Everest 81 lands, the conformance harness becomes a permanent CI step. Any future predicate addition or protocol revision must pass the harness first; Python and Rust outputs must match.

---

## What we are NOT shipping in v0

- **DSL for custom predicates.** Everest 51 chose a fixed predicate table for v0; DSL support is deferred to v1.
- **Trusted-setup Groth16 circuits.** Range proofs use Bulletproofs (no trusted setup); SNARKs are a future optimization.
- **Hardware wallet integration.** Signing is software-based Ed25519; hardware-key binding (YubiKey, TPM) is Everest 16 (template encryption) scope, not this summit.
- **Multi-principal federation.** One vault = one principal (Everest 34 decision); multi-vault namespace is v1+.

---

## Signing

— Calm, 2026-05-20
