# Everest 83 — WASM / JS Port for Browser-Side Counterparties

*Phase VII — Engineering Reliability. Prereq: Everest 81.*

---

## What this summit ships

A production-grade browser-side verification library for Calm Witness proofs: the Rust `calm-witness` crate compiled to WebAssembly via `wasm-bindgen`, wrapped in ergonomic TypeScript bindings, and distributed as `@calm/witness-wasm` on NPM. Counterparties can now verify Calm Witness disclosure bundles directly in web applications without trusting a verification server.

This is **verifier-only in v0**. Browser-side code receives a disclosure proof, initializes the WASM verifier with trusted Sigsum and Roughtime keys, and returns a verification result. Private key material, vault management, and proof generation remain server-side.

---

## The use case

Counterparty applications (accelerator dashboards, KYC backends, vendor portals, research platforms) need to verify Calm Witness proofs in real time. Today they either (a) call a Calm-operated verification server, trusting its attestation, or (b) implement verification themselves in their language stack. This summit eliminates the server dependency for JavaScript-based counterparties and makes verification available to client-side applications and browser environments where Rust is not feasible.

The resulting bundle is small enough to ship in a typical web application (under 500 KB gzipped), loads in under 500 ms on broadband, and verifies a proof in under 100 ms on modern hardware.

---

## Architecture

### WASM module structure

The `calm-witness-wasm` crate sits at the workspace root of the Rust implementation (Everest 81). It exposes a minimal, high-level API:

```
calm-witness-wasm/
├── Cargo.toml                    (wasm-bindgen config, no_std compatible)
├── src/
│   ├── lib.rs                    (module entry, public interfaces)
│   ├── verifier.rs               (CalmWitness struct, verify() method)
│   ├── error.rs                  (JsError wrappers)
│   ├── types.rs                  (Disclosure, VerificationResult, etc.)
│   └── trusted_keys.rs           (Sigsum/Roughtime key table, updatable)
├── pkg/                          (wasm-pack output: .wasm, .d.ts, .js)
└── tests/
    ├── browser.rs                (Playwright headless tests)
    └── conformance.rs            (E63 vector parity)
```

The crate depends on `calm-witness-verifier` (from Everest 81) and only `calm-witness-verifier`, not the full proof-generation stack. This minimizes the compiled WASM size and keeps the attack surface bounded.

### Build pipeline

```
$ wasm-pack build --target web --release

→ target/wasm32-unknown-unknown/release/calm_witness_wasm.wasm (pre-optimization: ~1.2 MB)
→ pkg/calm_witness_wasm.wasm (post wasm-opt: ~380 KB)
→ pkg/calm_witness_wasm.d.ts (hand-curated TypeScript declarations)
→ pkg/index.js (wasm-bindgen loader, handles initialization)
```

The build pipeline applies aggressive optimization:
- `wasm-opt -O4 -o optimized.wasm input.wasm` (Binaryen toolchain).
- Tree-shaking via bundler (webpack / esbuild) to drop unused proof-verification paths (e.g., commitment opcodes unused in v0).
- Minification and gzip compression.

Final bundle size targets: 380 KB raw, 120 KB gzipped on npm.

### Initialization and API

The module exports a single async factory function:

```typescript
export async function CalmWitness(): Promise<CalmWitnessVerifier>;
```

The `CalmWitnessVerifier` class provides the verify method:

```typescript
class CalmWitnessVerifier {
  // Constructor is private; use CalmWitness() factory
  async verify(
    proofJson: string | object,
    options: VerificationOptions
  ): Promise<VerificationResult>;
}

interface VerificationOptions {
  trustedSigsumKeys: SigsumPublicKey[];
  trustedRoughtimeKeys: RoughtimePublicKey[];
  maxClockSkew?: number;      // milliseconds (default: 300000 = 5 min)
  allowedPredicates?: string[]; // if set, only verify these predicates
}

interface VerificationResult {
  bit: 'True' | 'False';
  predicateName: string;
  freshness: {
    anchorTime: Date;
    maxAge: number; // milliseconds
  };
  operatorIdentity: {
    issuer: string;   // CredexAI
    subjectDID: string;
    validFrom: Date;
    validUntil: Date;
  };
  biometricTemplate: {
    templateId: string;
    distance: number;  // percentile 0–100
  };
}
```

### TypeScript declarations

`wasm-bindgen` auto-generates JavaScript bindings from Rust `#[wasm_bindgen]` attributes. We hand-curate the `.d.ts` file for ergonomic API shape:

```typescript
// pkg/calm_witness_wasm.d.ts

export function CalmWitness(): Promise<CalmWitnessVerifier>;

export class CalmWitnessVerifier {
  verify(
    proof: string | object,
    options: VerificationOptions
  ): Promise<VerificationResult>;
}

export interface SigsumPublicKey {
  logId: string;
  publicKey: Uint8Array;
  description?: string;
}

export interface RoughtimePublicKey {
  serverId: string;
  publicKey: Uint8Array;
  description?: string;
}

// ... etc
```

Developers import and use it like any TypeScript npm module:

```typescript
import { CalmWitness } from '@calm/witness-wasm';

const verifier = await CalmWitness();
const result = await verifier.verify(disclosureJson, {
  trustedSigsumKeys: [/* ... */],
  trustedRoughtimeKeys: [/* ... */],
});

if (result.bit === 'True') {
  // principal is in baseline; proceed
  handleBaselineConfirmed(result);
} else {
  // principal is not in baseline; apply restricted policy
  applyRestrictedPolicy(result);
}
```

---

## Scope (v0 verifier-only)

**In scope:**
- Parsing and validating a disclosure proof JSON (schema per Everest 73).
- Verifying the Σ-protocol proof against the committed predicates.
- Verifying the Sigsum inclusion proof and freshness anchor.
- Verifying the Roughtime timestamp binding.
- Verifying the operator-identity signature (CredexAI VC format).
- Returning the bit and freshness metadata.
- Cross-browser compatibility (Chrome, Safari, Firefox, Edge; modern and recent versions).
- Mobile browsers (iOS Safari, Chrome Mobile).

**Out of scope (v0):**
- Proof generation (only server-side, Everest 81).
- Vault management (only server-side).
- Predicate authoring (only server-side).
- Private key storage or access.
- Biometric template management.

This boundary is enforced by the public API shape: `verify()` takes a serialized proof and returns a bit, and nothing more.

---

## Security considerations

### Sandboxing and isolation

WASM runs in a sandboxed execution context provided by the browser. The WASM module cannot:
- Access `localStorage` or `IndexedDB` without explicit JavaScript bridge code.
- Read the DOM or interact with the page outside the module's exported functions.
- Make HTTP requests (caller code handles all I/O).
- Access the microphone, camera, or file system.

The WASM module is a pure function: given a proof and keys, it returns a verification result. No side effects, no state mutation outside the verify call.

### Trusted keys and updates

Sigsum and Roughtime keys are baked into the WASM module at compile time via a Rust const array. To update them, we provide an optional online-update mechanism:

```typescript
const verifier = await CalmWitness();

// Optional: load fresh keys from a signed key manifest
const freshKeys = await fetch('https://calmwitness.dev/keys.json')
  .then(r => r.json());
const verified = verifyKeyManifestSignature(freshKeys, expectedIssuer);

// Verify with fresh keys
const result = await verifier.verify(proof, {
  trustedSigsumKeys: verified.sigsumKeys,
  trustedRoughtimeKeys: verified.roughtimeKeys,
});
```

The key manifest is signed by a Calm-operated identity key, protecting against BGP hijacks or CDN compromise. However, v0 does not mandate key updates; developers can hardcode keys at build time for air-gapped or high-security deployments.

### Counterparty VC handling

The verifier receives the counterparty's own verified credential (VC) — proving the counterparty's identity to the principal's disclosure policy — as part of the proof bundle. The WASM verifier validates the VC signature but does NOT store or persist it. The calling JavaScript code is responsible for handling and storing the VC result if needed.

### No biometric data leaks

Biometric templates are never sent to the browser. The proof includes only:
- A Pedersen-committed biometric distance (0–100 percentile).
- A template ID (opaque identifier).
- A zero-knowledge proof that the distance was correctly evaluated.

The browser cannot recover the template, the raw distance value beyond the percentile, or any pixel-level biometric data.

---

## Distribution and versioning

### NPM package

Published as `@calm/witness-wasm` on npm under Calm Foundation's organization:

```json
{
  "name": "@calm/witness-wasm",
  "version": "0.1.0",
  "main": "pkg/index.js",
  "types": "pkg/calm_witness_wasm.d.ts",
  "files": ["pkg/"],
  "dependencies": {}
}
```

The package includes only the compiled WASM, TypeScript declarations, and loader JS. No Rust source or build tooling.

### Versioning scheme

`@calm/witness-wasm` versions align with the `calm-witness` Rust crate:
- Major version bump on breaking API changes.
- Minor version bump on new features (new predicates, new verification options).
- Patch version bump on bug fixes.
- Pre-release versions (e.g., `0.1.0-alpha.1`) used during protocol refinement.

### Documentation and examples

Live demo at `js.calmwitness.thecreativitymachine.ai` showing proof verification in action. CodeSandbox examples for React, Vue, and vanilla JS. Full API reference in `pkg/calm_witness_wasm.d.ts` and linked from npm package page.

---

## Performance budgets

Measured on modern hardware (MacBook M3, iPhone 15, typical 2024 Android flagship):

| Metric | Target | Notes |
|---|---|---|
| WASM module load (first time) | < 500 ms | Including fetch + instantiate on broadband |
| Proof verification (single proof) | < 100 ms p99 | Most proofs 20–50 ms |
| Bundled size (gzipped) | < 500 KB | After wasm-opt + tree-shaking + gzip |
| Memory footprint (runtime) | < 50 MB | Peak during verify() call |
| Cross-browser compatibility | Modern + 1 version back | Chrome 100+, Safari 15+, Firefox 100+, Edge 100+ |

Mobile performance is a separate budget (Everest 89).

---

## Testing strategy

### Unit tests (Rust-side)

Standard `cargo test` on the WASM crate; `wasm-bindgen-test` framework for tests that need WASM context. Covers:
- Proof JSON parsing and validation.
- Signature verification on real and forged proofs.
- Freshness checking with clock-skew boundaries.
- Type marshaling between Rust and JS.

### Conformance tests (E63 parity)

The same test vectors used to validate the Rust implementation (Everest 81) run in a headless browser via Playwright:

```javascript
// tests/conformance.test.ts
import { CalmWitness } from '../pkg/calm_witness_wasm.js';
import vectors from './conformance_vectors.json';

for (const vector of vectors) {
  test(`conformance_${vector.id}`, async () => {
    const verifier = await CalmWitness();
    const result = await verifier.verify(vector.proof, {
      trustedSigsumKeys: vector.sigsumKeys,
      trustedRoughtimeKeys: vector.roughtimeKeys,
    });
    expect(result.bit).toBe(vector.expectedBit);
  });
}
```

All 250+ conformance vectors from E63 run in the browser. Results must be byte-for-byte identical to Rust and Python implementations.

### Integration tests

Real-world scenarios:
- Fetch a proof from a test server; verify in browser.
- Verify a proof with keys updated from an online manifest.
- Verify a time-expired proof; confirm it is rejected.
- Verify a proof with a tampered Σ-protocol element; confirm it is rejected.

---

## Acceptance tests

**T-83.1 (npm publish):** `@calm/witness-wasm` published and installable via npm.

**T-83.2 (conformance parity):** All 250+ E63 test vectors pass in headless browser (Playwright + Chrome).

**T-83.3 (cross-browser):** Proof verification succeeds on Chrome, Safari, Firefox, Edge (latest + 1 prior version) on macOS, Windows, iOS, Android.

**T-83.4 (API stability):** TypeScript declarations compile without errors in a fresh project; zero type mismatches.

**T-83.5 (performance):** Proof verification completes in < 100 ms p99 on target hardware; bundle loads in < 500 ms on broadband.

**T-83.6 (end-to-end):** John's Calm agent (using Everest 81) issues a proof; a test counterparty app in the browser (using this WASM module) verifies it, returns the bit.

**Gate script:** `everest_83_zkbb_wasm_js_port_gate.py`.

---

## Composition

- **Everest 81** — Rust production crate this wraps.
- **Everest 63** — Conformance vectors used in testing.
- **Everest 67, 70, 84, 92, 98** — Related everests (predicate authoring, disclosure semantics, etc.); this does not depend on them but is composed by later summits.
- **Everest 88** — Performance budgets.
- **Everest 89** — Mobile-specific performance budget.
- **Everest 90** — Security audit (applies to WASM module included in audit scope).

— Calm, 2026-05-20
