# ZKAC Browser Extension v0

**Everest 127 · 2026-05-20 · Calm**
**Browser surface for Pact-passing counterparty disclosure and one-click consent**
**Companion:** [`everests/everest_127_zkac_browser_extension.md`](everests/everest_127_zkac_browser_extension.md)

## Status

**DESIGN-BAGGED (Summit 127/300) 2026-05-20**

This bag ships the normative design specification (this document), a gate script, a route-map status line, and a `summit_bagged` chain anchor. The **full** Chromium Manifest V3 extension (content scripts, service worker, store packaging, cross-browser QA) is **XL** effort and is explicitly **follow-through**, not in scope for this Haiku pass. Gate: `~/CredexAI/scripts/everest_127_zkac_browser_extension_gate.py` exit 0.

Implementation sketch lives at `~/CredexAI/calm_witness/browser-extension/DESIGN.md`. No packaged `.crx` or Web Store listing is claimed here.

## Acceptance (verbatim)

**Everest 127 | ZKAC browser extension.** *Acceptance:* browser extension that surfaces a Calm-suite disclosure request when an aligned counterparty (Pact-passing) is on the page, with one-click consent. *Effort:* L (design); **XL** (full extension binary). *Prereq:* 122.

Design-bagged acceptance for this pass:

1. Normative spec at least 1500 words with gate, route, and chain sections.
2. Anti-purity-test: browser UI MUST NOT show numeric similarity scores, cosine values, Mahalanobis distances, per-dimension vectors, or ranked alignment percentages.
3. Scope-statement forfeits inherited from [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) and [`CALM_REFUSAL_FLOOR_INDEX.md`](CALM_REFUSAL_FLOOR_INDEX.md).
4. Pact-passing detection and one-click consent flows documented with local-only data paths.
5. In-house only: no third-party analytics, session replay, or remote decisioning on PII.

Full extension acceptance (follow-through): load unpacked MV3 build, detect Pact-passing counterparty on fixture pages, show disclosure prompt, record consent locally, gate green on integration tests.

## XL designation

The surface is **XL** because it joins four hard problems in one shipping unit:

1. **Page-origin binding.** Content scripts must bind prompts to the active tab origin without leaking context across sites.
2. **Local policy engine.** Background worker must evaluate Pact-passing state using vault-fed proof metadata, not remote APIs.
3. **Consent UX under refusal floor.** UI may show at most coarse bands and explicit consent/refusal controls, never similarity scores or vector heatmaps.
4. **Vault bridge security.** Native messaging or localhost companion must stage minimum proof bytes without exfiltrating page HTML.

A design bag is correct: policy and architecture are summit-blocking; the Chrome Web Store pipeline is not.

## Problem statement

Counterparties that pass Calm Pact checks may request a Calm-suite disclosure bit during a web session. Today that flow assumes a desktop operator or server SDK. Many real sessions start in the browser. The extension is the **thin local wrapper** that:

- Notices when the page presents a Pact-passing counterparty signal (DOM hook, meta tag, or companion-injected marker defined in follow-through).
- Asks the local vault whether disclosure is permitted for this `(predicate, counterparty_class, origin)` tuple.
- Surfaces a **single** disclosure request with **one-click** consent or explicit local refusal.
- Records the consent decision in extension-local storage scoped to `(origin, session_nonce)` only.

The extension is not a wallet, not a verifier farm, and not a values-alignment dashboard.

## Architecture (Manifest V3)

### Components

| Component | Responsibility | Must not |
| --- | --- | --- |
| Content script | Detect counterparty marker; request policy decision | Scrape full page text; call third-party APIs |
| Service worker | Policy, consent state, message routing | Hold long-lived PII logs |
| Consent panel | Injected UI or action popup | Show similarity scores or per-dim bars |
| Vault bridge | Read minimum proof metadata; stage disclosure | Upload page HTML or proofs to cloud |

### Message flow

```
Page marker detected
  → content script → runtime.sendMessage({ kind: "counterparty_candidate", origin, marker_digest })
  → service worker evaluates:
       (a) origin allowlist / blocklist
       (b) vault bridge: pact_passing_bit for session
       (c) consent matrix: principal_consents_to_disclose
  → if qualified: inject consent panel
  → user one-click consent → local record + optional vault notify
  → panel dismissed; no background polling
```

### Pact-passing detection

**Pact-passing** means the counterparty satisfies the local Pact verifier for the active session wire version (see Everest 136 bridge). The extension does **not** re-implement Pact crypto in v0 design. It consumes a **boolean** `pact_passing` from:

1. Vault companion over native messaging (`calm-vault-bridge/v0`), or
2. A page-embedded `calm-pact-marker` element whose digest was pre-verified by the companion.

Ambiguous state (`unknown`, stale head, version skew) MUST result in **no prompt**, not a guess.

### One-click consent

The consent panel presents exactly:

- Counterparty display name (operator-supplied, not inferred demographics).
- Disclosure type label from predicate vocabulary (single bit name).
- Primary button: **Allow once for this site session**.
- Secondary: **Refuse** (no penalty copy).

No multi-step wizard, no email capture, no analytics checkbox. Consent records:

```json
{
  "kind": "browser_consent.v0",
  "origin": "https://example.com",
  "session_nonce": "…",
  "predicate_id": "cwp.v0.in_baseline_24h",
  "decision": "allow_once",
  "recorded_at_iso": "…"
}
```

Stored in `chrome.storage.session` (or `local` with TTL). Never mirrored to third parties.

## Anti-purity-test (UI and logs)

Per [`CALM_REFUSAL_FLOOR_INDEX.md`](CALM_REFUSAL_FLOOR_INDEX.md) §2, the browser extension inherits the **output-shape refusal floor**:

1. **No numeric similarity scores.** The UI MUST NOT render cosine similarity, Mahalanobis distance, "87% aligned", heatmaps over 15 value dimensions, or per-predicate numeric gauges.
2. **No cardinality reveals.** Do not show "3 of 5 predicates matched."
3. **No per-predicate-bit vectors** in the panel. At most: `aligned | partial | divergent | insufficient_evidence | unknown` as **text bands** without numbers.
4. **No cross-tab profiling** to triangulate values across sites.

Allowed UI copy examples:

- "This site is Pact-passing. Allow a baseline disclosure bit for this session?"
- "Refusal floor: this request category is not permitted for browser counterparties."

Forbidden UI copy examples:

- "Values alignment: 0.82"
- "Cosine to charter: 0.91"
- "You match 12/15 dimensions"

Extension logs (local debug) MUST redact page content and MUST NOT include similarity floats. Gate checks enforce string markers in this spec.

## Scope-statement forfeits

The extension inherits [`CALM_WITNESS_SCOPE_STATEMENT.md`](CALM_WITNESS_SCOPE_STATEMENT.md) §2 **verbatim categories**. Deployments that use the extension for any §2 use **forfeit** the Calm Witness name and trademark license path.

| §2 category | Extension behavior |
| --- | --- |
| Law-enforcement surveillance | No `governmental` class prompts; default deny |
| Employment screening | No employment context detection; no HR integrations |
| Insurance underwriting | No insurance counterparty class |
| Lending / credit | `financial` class limited to transactional KYC per scope doc; no credit score copy |
| Medical diagnosis | No clinical labels; engineering bands only |
| Child welfare / custody | No family-court integrations |
| Immigration adjudication | No immigration class |
| Future-behavior prediction | No predictive predicates in browser requests |
| Population aggregation | No cross-user telemetry |
| Marketing targeting | No ad-network hooks |

**Ratchet:** Scope may tighten in v0.x patches; §2 entries MUST NOT be removed or weakened from extension policy without a successor protocol name.

Operator-visible **scope forfeits** banner (optional, recommended): link to `CALM_WITNESS_SCOPE_STATEMENT.md` from the extension options page.

## Refusal floor inheritance

Beyond scope forfeits, the extension MUST respect predicate refusal floor (12 categories in CALM_REFUSAL_FLOOR_INDEX §1). If a page or counterparty requests a predicate in a forbidden category, the worker returns `refusal_floor_block` and does not inject UI.

Concord alignment exchanges on the page MUST use `{ aligned: true | false | unknown }` per purpose, never numeric scores. If a site embeds forbidden shapes, the extension treats the site as **non-Pact-passing** for prompt purposes.

## Threat model

| Threat | Mitigation |
| --- | --- |
| Spoofed Pact marker on malicious origin | Marker digest verified by vault companion; stale markers rejected |
| Prompt injection via page DOM | Content script ignores arbitrary text; only signed marker channel |
| Cross-origin consent reuse | Consent keyed to origin + session_nonce |
| Extension supply-chain | In-house build; no third-party SDKs in consent path |
| Fingerprinting via extension ID | No broadcast of principal identity to page JS |
| Analytics exfiltration | No third-party analytics on PII (hard ban) |

Out of scope: nation-state compromise of Chrome, malicious vault companion binary (handled by vault summit track).

## Vault bridge (design)

Native messaging host `com.calm.vault.bridge` (name TBD in follow-through):

- **Inbound:** `{ pact_passing: bool, session_nonce, chain_head, allowed_predicates[] }`
- **Outbound:** `{ consent_recorded: bool, predicate_id, origin }`

If companion offline: extension stays silent (no prompt). No cloud fallback.

## Permissions (minimal MV3)

Follow-through manifest SHOULD request only:

- `storage` (session consent)
- `activeTab` (inject on user gesture or marker event)
- `nativeMessaging` (vault bridge)

MUST NOT request: `history`, `webRequest` broad host access, `clipboardRead`, remote `http://*` to analytics vendors.

## Wire integration

Composite envelopes (Everest 123/128) may arrive on pages as JSON-LD or `data-calm-envelope` attributes. The extension **verifies** via local `verify_zkac` stub (Python reference in CI; WASM follow-through) before trusting `pact_passing`. Design-bagged pass documents the hook points only.

## Privacy and retention

- Page HTML: not retained.
- Proof bytes: not retained in extension storage after verify.
- Consent records: TTL 24h default, user-clearable.
- Export: operator-triggered JSON export under `chrome://extensions` options.

## Follow-through checklist (XL)

1. `manifest.json` MV3 + service worker bootstrap
2. Content script + marker fixture pages in `calm_witness/browser-extension/fixtures/`
3. Native messaging host protocol tests
4. Consent panel component (no numeric scores; axe accessibility)
5. Integration test: Pact-passing page → prompt → one-click → local record
6. `npm run gate:everest127` wired into CredexAI verify suite
7. Store packaging deferred until operator requests distribution

## Gate

| Artifact | Path |
| --- | --- |
| This spec | `~/AllData/calm_vault_market/ZKAC_BROWSER_EXTENSION_v0.md` |
| Gate | `~/CredexAI/scripts/everest_127_zkac_browser_extension_gate.py` |
| Route | `~/AllData/calm_vault_market/ZKAC_NEXT_200_EVERESTS.md` Everest 127 line |
| Chain | `~/.calm-vault/user_state.jsonl` `kind: summit_bagged` |
| Design stub | `~/CredexAI/calm_witness/browser-extension/DESIGN.md` |

## Falsifiability

| Claim | Falsifier |
| --- | --- |
| Design meets anti-purity-test | Any UI mock showing numeric similarity |
| Scope forfeits present | Spec missing employment/insurance/credit prohibitions |
| One-click consent | Flow requires more than one confirmation click for default allow |
| In-house only | Spec names a third-party analytics SDK |
| DESIGN-BAGGED honest | Gate passes while claiming shipping Chrome Web Store build |

## Non-claims

This design bag does **not** claim:

- Chrome Web Store approval or public listing
- Firefox/Safari parity (Chromium first)
- Automatic detection on all sites without marker contract
- Values vector ZK proofs in the browser (Witness/Compass bits only per predicate vocabulary)
- Replacement of desktop vault UX

## Chain anchor

On gate exit 0, append `summit_bagged` with `design_bagged: true` and `follow_through` listing MV3 implementation items above.

## One-line result

Everest 127 is **DESIGN-BAGGED**: the browser extension policy, architecture, anti-purity UI rules, and scope forfeits are specified and gated; the XL packaged extension remains follow-through.

Musk sign-off: The best part is no part; the extension ships consent, not scores.
