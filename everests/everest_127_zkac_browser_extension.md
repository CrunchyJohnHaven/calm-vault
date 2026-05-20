# Everest 127 — ZKAC Browser Extension

*Phase IX — Browser Surfaces. Prereq: Everest 122.*

**Normative spec:** [`ZKAC_BROWSER_EXTENSION_v0.md`](../ZKAC_BROWSER_EXTENSION_v0.md) (DESIGN-BAGGED 2026-05-20).

## Overview

This Everest defines the browser extension surface for Calm ZKAC. The extension is acceptable as an XL surface because it combines page inspection, local policy evaluation, consent presentation, and a vault bridge without widening the refusal floor or exporting user data to third parties.

The acceptance target is simple. When the extension detects an aligned counterparty on the page, meaning a Pact-passing counterparty under the local policy engine, it surfaces a Calm-suite disclosure request and offers one-click consent. The consent action must be local, explicit, and scoped to the current page session.

## Acceptance Criteria

1. The extension detects an aligned counterparty on the current page using local page state and locally available proof material.
2. The extension surfaces a Calm-suite disclosure request only when the local policy says the counterparty is Pact-passing.
3. The disclosure request presents one clear consent control. A single click is enough to accept the current disclosure.
4. The consent result is recorded locally and is not used to create a broader tracking profile.
5. The extension never sends PII to third-party analytics, telemetry, or session replay services.

## Architecture

### 1. Content script

The content script reads the minimum page signals needed to detect the presence of a Pact-passing counterparty. It does not scrape unrelated text, and it does not exfiltrate page data. Its job is to identify the candidate surface and request a local policy decision from the extension runtime.

### 2. Background service worker

The background worker owns policy decisions, consent state, and message routing. It receives a page candidate, checks local state, and decides whether the page qualifies for a Calm-suite disclosure prompt. The worker also enforces that every consent is tied to the current tab and current page origin.

### 3. Vault bridge

The vault bridge connects the extension to the local Calm vault or companion process. It is responsible for reading the minimum proof metadata needed to confirm the counterparty class and for staging a disclosure request. The bridge must not forward raw page contents, raw proofs, or user PII to remote services.

### 4. Consent UI

The consent UI is an injected browser surface or extension panel that presents:

- The counterparty class that triggered the prompt.
- The disclosure type being requested.
- A single consent action.
- A local refusal action.

The UI should be short and explicit. It must not bury the consent action behind extra collection, upsell, or telemetry prompts.

## Threat Model

The primary threats are page-level spoofing, counterparty misclassification, prompt fatigue, and accidental data leakage.

The extension must defend against:

- A malicious page that tries to mimic a Pact-passing counterparty.
- A benign page that includes stale proof material from a prior session.
- A compromised browser environment that attempts to reuse consent outside the intended origin.
- Any analytics or logging path that exports PII off device.

The extension does not need to solve every browser threat. It does need to keep consent local, bind prompts to the current origin, and reject ambiguous counterparty state rather than guess.

## Refusal Floor Inheritance

This surface inherits the Calm-suite refusal floor. It must not create predicates, prompts, logs, or explanations that name or infer protected categories that the suite already refuses. It also must not weaken the principle that refusal is structurally available and non punitive.

Inheritance means the browser extension respects the same no-go categories and the same refusal-floor logic used elsewhere in the Calm stack. If the page or vault state would require crossing the refusal floor, the extension refuses to surface that request.

The extension also inherits the output-shape refusal floor from the vector publication policy. It may surface a single disclosure bit or a single consent decision, but it may not expose the underlying vector, proof internals, or private user state in the browser UI.

## No Third-Party Analytics on PII

This surface uses in-house only processing for user data. No hosted SaaS may receive page PII, consent state, proof metadata, or browsing context.

Prohibited paths include:

- Session replay.
- Product analytics.
- Crash reporting that uploads PII.
- Remote logging that captures page contents or proof payloads.

Allowed paths are local logs, local debug output under operator control, and repo-owned services that already satisfy the in-house policy. If telemetry is ever added, it must be privacy-minimized, self-hosted, and incapable of reconstructing user browsing content.

## Non Goals

This Everest does not authorize general browsing surveillance, page ranking, ad tracking, or background collection of arbitrary user behavior. It is a consent surface, not a analytics surface.

It also does not authorize any third-party consent SDK, hosted identity layer, or remote decisioning service. The browser extension should remain a thin local wrapper around the Calm vault and the local policy engine.

## Design Note

The XL designation is justified because the extension joins three hard problems in one surface: page detection, consent UX, and refusal-floor enforcement. The implementation remains acceptable only if each layer stays local, minimal, and auditable.
