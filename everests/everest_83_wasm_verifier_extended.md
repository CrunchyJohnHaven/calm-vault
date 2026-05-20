# Everest 83 — WASM Verifier: Extended Specification

*Phase VII Engineering Reliability. Prereq: E81 (Rust Production Implementation). Extended design-bagged summit.*

---

## Overview

Browser-side verification for Calm Witness disclosure proofs. A WebAssembly verifier crate `calm-witness-wasm` delivers client-side proof validation without server round-trips. Compiled with `cargo + wasm-pack + wasm-opt -Oz`. Sigstore-signed npm publication with provenance attestation. Concord-compliant output shape: `{ aligned: bool | "unknown" }` per specification.

**Scope:** verifier-only, no biometric pipelines, no chain-construction writes, no telemetry, no network calls.

---

## Build Pipeline & Size Discipline

### Cargo configuration

`Cargo.toml` for `crates/calm-witness-wasm/`:

```toml
[package]
name = "calm-witness-wasm"
version = "0.1.0"
edition = "2021"

[dependencies]
calm_witness_verifier = { path = "../calm-witness-verifier" }
wasm-bindgen = "0.2"
wasm-bindgen-futures = "0.4"

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
strip = true
```

### Build invocation

```bash
cargo install wasm-pack@0.12.1
wasm-pack build --target web --release --out-name calm_witness_verifier

# Post-build optimization
wasm-opt -Oz \
  --enable-bulk-memory \
  --enable-reference-types \
  pkg/calm_witness_verifier_bg.wasm \
  -o pkg/calm_witness_verifier_bg.opt.wasm

# Measure
gzip -9 pkg/calm_witness_verifier_bg.opt.wasm
ls -lh pkg/calm_witness_verifier_bg.opt.wasm.gz  # Must be ≤ 250 KB
```

### Bundle composition

Outputs:

- `calm_witness_verifier_bg.wasm` (~500 KB uncompressed, ~200 KB raw after wasm-opt, ~160 KB gzip).
- `calm_witness_verifier_bg.wasm.gz.base64` (SRI hash attached, published to npm).
- `calm_witness_verifier.js` (~8 KB, glue code + TypeScript-aware wrappers).
- `calm_witness_verifier.d.ts` (~12 KB, TypeScript declarations, no magic type unions).
- `package.json` with `"main"` pointing to JS entry, `"types"` to `.d.ts`, `"exports"` for ES modules.

**Discipline:** pre-gzip measurements in the build log. Reject if gzip > 250 KB.

---

## TypeScript API Surface & Concord Compliance

### Entry point

```typescript
// calm_witness_verifier.d.ts
export interface VerifyRequest {
  disclosureBundle: string; // JSON-encoded disclosure
  trustedAnchors: TrustedAnchor[];
}

export interface TrustedAnchor {
  logPublicKey: string;     // Sigsum log root (hex-encoded ed25519 pk)
  issuerKey: string;        // CredexAI issuer key (hex)
  anchorThresholdBits: number; // Votes required from this anchor set
}

// Concord output shape: aligned ∈ {true, false, "unknown"}
export interface VerifyResult {
  aligned: boolean | "unknown"; // NEVER score, count, or numeric confidence
  witness_timestamp_utc: string;
  proof_freshness_seconds: number;
  predicate_class: string;      // "harm_absence" | "cooperation" | etc.
  counterparty_id: string;
}

// Init once per page load
export function init(): Promise<void>;

// Sync verification (after init)
export function verifyDisclosure(
  request: VerifyRequest
): VerifyResult;

// Batch verification helper
export function verifyBatch(
  requests: VerifyRequest[]
): VerifyResult[];
```

### Concord compliance

The output shape MUST satisfy:

```typescript
// Linter rule: reject any signature that returns score or count
function alignmentResult(): { aligned: number } // ❌ REJECTED
function alignmentResult(): { alignment_score: number } // ❌ REJECTED
function alignmentResult(): { aligned: boolean | "unknown" } // ✅ ACCEPTED
```

The type system enforces the policy. No function overload returns a numeric confidence; the API refuses type-level composition with scoring functions.

---

## Performance Budget

### Initialization

- **Synchronous instantiation:** WASM module loads from npm tarball in ~50 ms median.
- **Async init():** memory setup, table initialization ≤ 100 ms p95.
- **Per-page overhead:** one-time only. Verification calls amortize.

### Verification latency (p95)

- Single disclosure (leaf predicate): ≤ 50 ms.
- AND/OR composition (≤ 3 leaf predicates): ≤ 80 ms.
- Chain-head freshness check against Sigsum log: ≤ 30 ms (in-memory log cache).

### Browser compatibility

Tested and gated:

- Chrome 130+ (both standard and headless modes).
- Firefox 132+ (with and without WASM JIT).
- Safari 17.4+ (iOS and macOS, including low-power mode).
- Edge 130+ (Chromium-based).

**Gate metric:** byte-identical accept/reject decisions across all four browsers on a conformance vector set (50+ test cases covering edge cases: expired proofs, malformed bundles, missing anchors, replay attacks).

---

## No Telemetry, No Network

The WASM verifier is **hermetic.** All data flows through the JavaScript API; the module makes zero outbound requests.

- No calls to external services.
- No beacons or analytics.
- No DNS lookups.
- No WebSocket or XMLHttpRequest from inside the WASM module.

**Verification:** network traffic analyzer (e.g., mitmproxy) confirms zero HTTP/HTTPS/DNS activity during verifyDisclosure() invocation.

---

## Subresource Integrity & Provenance

### SRI hashes

The npm package publishes SRI hashes for the WASM binary:

```json
{
  "calm-witness-verifier": {
    "wasm": {
      "sri": "sha384-abcd1234...",
      "url": "https://cdn.jsdelivr.net/npm/@calm-foundation/witness-verifier@0.1.0/pkg/calm_witness_verifier_bg.wasm"
    }
  }
}
```

Counterparty pages pin with:

```html
<script src="..." integrity="sha384-abcd1234..."></script>
```

### Sigstore provenance

Published with:

```bash
npm publish --provenance --access public
```

The npm registry attaches a Sigstore SLSA provenance attestation (`provenance.json`) verifying:
- Build environment (GitHub Actions runner ID).
- Commit hash.
- Build inputs (package.json, Cargo.lock).
- Signature over the tarball.

Verifiable via `npm view --json @calm-foundation/witness-verifier@0.1.0 | jq .provenance`.

---

## Composition & Everest Fabric

### E81 — Rust source crate

The WASM module is a **thin wrapper** around the verifier logic in `calm-witness-verifier` (E81). No reimplementation; all cryptographic reasoning stays in Rust.

- WASM bindings expose only the public verify API.
- Secret material never crosses the FFI boundary.
- Prover code, predicate generation, and chain construction are excluded at the Rust level.

### E86 — Python reference implementation

E86 provides the algorithmic gold standard. WASM must produce **identical accept/reject decisions** on the conformance vector set.

- 50 test cases cover: valid proofs, expired proofs, signature tampering, anchor mismatch, multi-predicate AND/OR, counterparty identity binding, consent revocation.
- Both E83 (WASM) and E86 (Python) run the same test corpus; results are compared.
- Parity is gated: no release until WASM and Python agree on all 50.

### E98 — Counterparty implementer's guide

E98 provides:

- Browser-side integration patterns (React, Vue, vanilla JS examples).
- Error handling (what to do when `aligned` is `"unknown"`).
- Caching strategies (reuse verifier instance across multiple checks).
- SRI pinning templates for content-security-policy headers.

### E81 → E83 → E98 dataflow

```
E81 (Rust verifier) → WASM compilation (E83) → npm publish
                    ↓
                    E98 guides JS developers
                    ↓
                    Counterparty portal (bank, journalist, healthcare)
```

---

## Acceptance Tests

### T-83.1: Bundle size

```bash
gzip -9 pkg/calm_witness_verifier_bg.opt.wasm
test $(stat -f%z pkg/calm_witness_verifier_bg.opt.wasm.gz) -le 262144  # 250 KB
```

**Gate:** Fail if gzip ≥ 250 KB.

### T-83.2: Performance

Measure on real hardware (not emulated):

```javascript
const start = performance.now();
await init();
verifyDisclosure(bundle, anchors);
const elapsed = performance.now() - start;
console.assert(elapsed < 200, `Init + verify: ${elapsed}ms, expected <200ms p95`);
```

Run 100 iterations; record p95. Gate: p95 ≤ 200 ms.

### T-83.3: Browser parity

```bash
# Run conformance suite in headless Chrome, Firefox, Safari, Edge
for browser in chrome firefox safari edge; do
  playwright test conformance.spec.ts --project=$browser
done

# Compare results; fail if any divergence in accept/reject
pytest test_parity.py::test_browser_parity
```

Gate: byte-identical accept/reject decisions across all four.

### T-83.4: npm publish with provenance

```bash
npm publish --provenance
npm view --json @calm-foundation/witness-verifier@0.1.0 | jq '.provenance'
test -n "$provenance"  # Non-empty provenance object
```

Gate: npm registry shows non-null `provenance` field.

### T-83.5: Demo page

Static HTML demo at `https://calm-foundation.org/demo`:

- Loads WASM from npm via CDN (jsdelivr or unpkg).
- User pastes a disclosure bundle (JSON).
- Calls verifyDisclosure() client-side.
- Displays result: `aligned: true | false | "unknown"`.
- No server-side verification; all compute happens in the browser.

Gate: page loads, verifies a valid bundle, displays correct result.

### T-83.6: No network calls

```bash
# Start mitmproxy; route browser traffic through it
mitmproxy -s 'demo_page_listener.py' &

# Load demo page; trigger verification
playwright test demo_verify.spec.ts

# Check logs: zero HTTP requests initiated from the WASM module
grep -c "calm_witness_verifier.*outbound" proxy.log
# Must be 0
```

Gate: zero outbound requests from the WASM module.

---

## Gate Script: `everest_83_zkbb_wasm_verifier_gate.py`

```python
#!/usr/bin/env python3
"""
E83 acceptance gate. All six tests must pass.
Outputs pass/fail for each T-83.X.
"""
import subprocess
import json
import re

def test_83_1_bundle_size():
    """T-83.1: Compressed WASM ≤ 250 KB."""
    result = subprocess.run(
        ['bash', '-c', 'gzip -9 pkg/calm_witness_verifier_bg.opt.wasm && '
                       'stat -f%z pkg/calm_witness_verifier_bg.opt.wasm.gz'],
        capture_output=True
    )
    size = int(result.stdout.strip())
    passed = size <= 262144  # 250 KB
    print(f"T-83.1 (bundle size): {size} bytes", "PASS" if passed else "FAIL")
    return passed

def test_83_2_performance():
    """T-83.2: Init + verify p95 ≤ 200 ms."""
    # Run perf_bench.js in Node + headless Chrome
    result = subprocess.run(['node', 'perf_bench.js'], capture_output=True, text=True)
    match = re.search(r'p95_ms:\s*(\d+)', result.stdout)
    if not match:
        print("T-83.2: FAIL (no perf metric)")
        return False
    p95 = int(match.group(1))
    passed = p95 <= 200
    print(f"T-83.2 (performance): {p95} ms p95", "PASS" if passed else "FAIL")
    return passed

def test_83_3_browser_parity():
    """T-83.3: Chrome, Firefox, Safari, Edge produce identical results."""
    result = subprocess.run(
        ['pytest', 'test_parity.py::test_browser_parity', '-v'],
        capture_output=True, text=True
    )
    passed = result.returncode == 0
    print(f"T-83.3 (browser parity): {result.stdout.splitlines()[-1]}", 
          "PASS" if passed else "FAIL")
    return passed

def test_83_4_npm_provenance():
    """T-83.4: npm publish --provenance attestation present."""
    result = subprocess.run(
        ['npm', 'view', '--json', '@calm-foundation/witness-verifier@0.1.0'],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    passed = data.get('provenance') is not None
    print(f"T-83.4 (npm provenance): {data.get('provenance', {}).get('predicateType', 'N/A')}", 
          "PASS" if passed else "FAIL")
    return passed

def test_83_5_demo_page():
    """T-83.5: Static demo page loads and verifies a sample bundle."""
    result = subprocess.run(
        ['playwright', 'test', 'demo_verify.spec.ts'],
        capture_output=True, text=True
    )
    passed = result.returncode == 0
    print(f"T-83.5 (demo page): {result.stdout.splitlines()[-1] if result.stdout else 'no output'}", 
          "PASS" if passed else "FAIL")
    return passed

def test_83_6_no_network():
    """T-83.6: Zero outbound requests during verification."""
    result = subprocess.run(
        ['bash', '-c', 'mitmproxy -s network_sniffer.py & sleep 1 && '
                       'HTTPS_PROXY=http://127.0.0.1:8080 '
                       'playwright test network_check.spec.ts && killall mitmproxy'],
        capture_output=True, text=True
    )
    # Parse sniffer output for outbound request count
    match = re.search(r'outbound_count:\s*(\d+)', result.stdout)
    outbound_count = int(match.group(1)) if match else -1
    passed = outbound_count == 0
    print(f"T-83.6 (no network): {outbound_count} outbound requests", 
          "PASS" if passed else "FAIL")
    return passed

if __name__ == '__main__':
    tests = [
        test_83_1_bundle_size,
        test_83_2_performance,
        test_83_3_browser_parity,
        test_83_4_npm_provenance,
        test_83_5_demo_page,
        test_83_6_no_network,
    ]
    
    results = [test() for test in tests]
    
    print(f"\n{'='*60}")
    print(f"E83 GATE: {sum(results)}/{len(results)} passed")
    print(f"{'='*60}")
    
    exit(0 if all(results) else 1)
```

---

## Follow-Through & Governance

### Named maintainer

**Foundation Maintainer:** David Chen (calm-foundation.org/team/chen).

Responsible for:
- WASM crate upkeep (Rust version updates, dependency bumps).
- npm package releases (semantic versioning, changelog).
- Browser compatibility regression testing (quarterly).

### First release roadmap

**v0.1.0 (this summit):**
- Core verifier API (verifyDisclosure, init).
- Chrome, Firefox, Safari, Edge support.
- SRI + Sigstore provenance.
- Gate script + demo page.
- ~160 KB gzip.

**v0.2.0 (post-E86 parity):**
- Additional test cases (adversarial bundles, stress tests).
- Performance optimizations if p95 creeps above 150 ms.
- React/Vue component examples (in E98).

### Composition closure

- **E81:** Rust verifier (bagged).
- **E83:** WASM port + npm publish (this summit).
- **E86:** Python parity (parallel, dependency for v0.1 release).
- **E98:** Counterparty guide (depends on E83 being published).
- **E100:** Third-party verification (may use WASM verifier for audit).

---

## Anti-purity discipline

The WASM module is **not** a research artifact; it is a production-grade shipping component. Decisions are driven by deployment constraints, not theoretical elegance.

- Size budget: 250 KB gzip. If a feature does not fit, it is cut. Verifier-only scope enforced.
- Performance budget: 200 ms p95. If optimization does not deliver >10% speedup, it is deferred to v0.2.
- Browser support: pragmatic, not exhaustive. IE is not supported; Safari 17.4+ is baseline.
- API surface: no magic type unions, no implicit conversions. `aligned: bool | "unknown"` is explicit and composable.

**Refusal floor:** No telemetry, no network calls, no server-side fallback. If verification fails offline, the result is `aligned: "unknown"`, not degraded to an optimistic accept.

---

## Linter enforcement of Concord compliance

A custom ESLint rule `no-scoring-api` rejects any function signature that returns numeric confidence, alignment_score, or count fields:

```javascript
// .eslintrc.json
{
  "rules": {
    "no-scoring-api": [
      "error",
      {
        "forbidPatterns": [
          "alignment_score",
          "confidence",
          "count",
          "score",
          "rank"
        ],
        "allowedReturnTypes": ["boolean", "string"]
      }
    ]
  }
}
```

Gate: eslint must pass with zero violations on all `.ts` and `.js` files in `pkg/`.

---

## Summary

**E83 WASM Verifier — extended specification:**

- Build: cargo + wasm-pack + wasm-opt -Oz → ~160 KB gzip.
- API: Concord-compliant `{ aligned: bool | "unknown" }`, no scoring functions.
- Performance: ≤ 100 ms init, ≤ 50 ms verify, ≤ 200 ms total p95.
- Browsers: Chrome 130+, Firefox 132+, Safari 17.4+, Edge 130+ with byte-identical parity.
- Provenance: Sigstore npm publish, SRI hashes.
- Composition: E81 (source) → E83 (WASM) → E98 (guide), E86 (parity).
- No telemetry, no network, no server fallback.
- Gate script (6 tests) enforces all acceptance criteria.
- Maintained by Foundation (David Chen) with quarterly regression tests.
- First release: v0.1.0 shipping after E86 parity verified.

Authored by Calm, 2026-05-20.

— Musk: *requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
