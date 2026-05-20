# Everest 83 — WASM Port for Browser-Side Counterparties

*Phase VII — Engineering Reliability. Prereq: Everest 81 (Rust Production Implementation).*

---

## What this summit ships

A WebAssembly compilation of the `calm-witness-verifier` crate that runs in any modern browser. A counterparty implemented in browser JavaScript (a bank's customer-facing portal, a journalist's verification tool, a healthcare-facing app, an AI-safety researcher's audit dashboard) can verify Calm Witness disclosure proofs without server-side dependencies.

This is what makes Calm Witness deployable into JavaScript-heavy environments — counterparty agents whose verifier needs to live near the user-facing surface.

---

## Build pipeline

`crates/calm-witness-wasm/`:

```
cargo install wasm-pack
wasm-pack build --target web --release
wasm-opt -Oz pkg/calm_witness_verifier_bg.wasm -o pkg/calm_witness_verifier_bg.opt.wasm
```

Outputs:
- `calm_witness_verifier_bg.wasm` — the compiled WASM binary (~500 KB raw; ~200 KB after `wasm-opt -Oz`; gzip-compressed in transit).
- `calm_witness_verifier.js` — JS glue code (~30 KB).
- `calm_witness_verifier.d.ts` — TypeScript declarations.

Published as `@calm-foundation/witness-verifier` on npm with cosigned provenance (`npm publish --provenance`).

---

## API (TypeScript)

```typescript
import init, {
  verifyDisclosure,
  VerifierResult,
} from '@calm-foundation/witness-verifier';

// Initialize once per page load.
await init();

// disclosureBundle is the wire-format JSON from the operator.
// trustedAnchors lists trusted Sigsum log roots + CredexAI issuer keys.
const result: VerifierResult = verifyDisclosure(disclosureBundle, trustedAnchors);

// result.accept: boolean
// result.reason: string (e.g., "anchor_signature_invalid", "consent_revoked")
// result.freshness_window_s: number (how fresh the proof is)
// result.bit: 'true' | 'false' | 'unknown'
```

Returns synchronously after WASM initialization completes.

---

## Performance target

- **Initialize:** ≤ 100 ms (one-time per page load). Subsequent verifications reuse the WASM instance.
- **Single disclosure verify:** ≤ 50 ms p95.
- **Aggregated multi-predicate verify:** ≤ 80 ms p95.

Tested across:
- Chrome 130+
- Firefox 132+
- Safari 17.4+
- Edge 130+

---

## Bundle-size discipline

Counterparty pages are bandwidth-sensitive. Strict size budget:

- Compressed WASM (gzip): ≤ 250 KB.
- Compressed JS + TS: ≤ 15 KB.
- Total page-load addition (WASM + JS): ≤ 265 KB.

Exclusions from the verifier crate (to hit budget):
- All prover code — verifier-only.
- Biometric pipelines — verifier never touches biometric data.
- Chain construction code — verifier reads, never writes.
- CLI bindings.
- File-system access — browser-side has none.

---

## Browser-compat scope

Targets:
- Chrome 130+, Firefox 132+, Safari 17.4+, Edge 130+, Brave (Chromium-based).
- iOS Safari 17.4+.
- Android Chrome 130+.

Not supported in v0:
- IE / pre-Chromium Edge.
- Browsers without WebAssembly (very rare; <0.5% of traffic).

---

## Security disciplines

- **No side-channel exposure** beyond what WASM inherits from the browser. Timing leakage in JS is documented as residual risk; mitigated by avoiding secret-dependent branches in hot paths.
- **Subresource Integrity (SRI).** The npm package publishes SRI hashes; counterparty pages can pin them.
- **Provenance.** `npm publish --provenance` attaches a Sigstore-signed attestation of the build chain.
- **No telemetry.** The WASM verifier makes zero network requests. All data passes through the JS API.

---

## Acceptance test

**T-83.1 (bundle size).** Compressed WASM ≤ 250 KB.
**T-83.2 (performance).** Initialize + single verify under 200 ms total p95.
**T-83.3 (browser parity).** Chrome, Firefox, Safari, Edge all produce byte-identical accept/reject decisions on the conformance vector set.
**T-83.4 (npm publish with provenance).** Package available on npm with verified provenance attestation.
**T-83.5 (demo page).** A static HTML demo page at `calm-foundation.org/demo` accepts a sample disclosure bundle and verifies it entirely client-side.
**T-83.6 (no network calls).** Network traffic analysis confirms zero outbound requests from the WASM module during verification.

**Gate script:** `everest_83_zkbb_wasm_port_gate.py`.

---

## Composition

- **Everest 81** — source crate.
- **Everest 86** — verifier reference impl (the Rust verifier this WASM-compiles).
- **Everest 98** — counterparty implementer's guide references this for browser-side deployments.
- **Everest 100** — independent third-party verification may use the WASM verifier.

— Calm, 2026-05-20
