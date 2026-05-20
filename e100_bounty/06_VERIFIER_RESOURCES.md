# Verifier Resources — Everest 100 Bounty

*Resources Calm provides to verifiers. Public document. Last updated 2026-05-20.*

This document lists every resource Calm makes available to an independent third-party verifier attempting an Everest 100 verification. The list is intentionally exhaustive; if something a verifier needs is missing from this list, it is by design (the gap is itself a doc-bug worth filing) or by independence-preservation (we cannot provide implementation help; see below).

---

## What we provide

### 1. Open-source repository — `calm-witness`

- **URL:** `https://github.com/[ORG]/calm-witness` (replace with the canonical URL at launch).
- **License:** Apache 2.0.
- **Contents:** Rust reference implementation; WASM/JS verifier port; build scripts; integration tests; example proofs; documentation source.
- **Issue tracker:** Public. Verifiers may open issues for any bug found during V1–V7. The `everest-100-verification` tag is reserved for the verifier's submission-tracking issue itself; bugs are filed under standard tags (`bug`, `doc`, `spec`).

### 2. Counterparty Implementer's Guide (Everest 98)

- **URL:** `https://[PROJECT-SITE]/docs/implementers-guide` (replace at launch).
- **Purpose:** The implementer's guide is the verifier's primary reference. It is written specifically for someone building a verifier from scratch. It walks through the protocol's primitives in implementation-friendly language, with worked examples and test vectors.
- **Scope:** Verifier-side only. The proof-generation side is documented separately in the technical specification (different document).
- **Versioning:** Tied to releases of the `calm-witness` crate. A verifier should match the implementer's-guide version to the source-version they are building from.

### 3. Test corpus (Everest 94 — Differential Testing)

- **URL:** `https://[PROJECT-SITE]/test-corpus` (replace at launch) or, more durably, `calm-witness/test-corpus/` in the repository.
- **Format:** Each test case is a tuple of (input proof bytes, expected verifier output JSON). Inputs and expected outputs are both content-addressable.
- **Coverage:** Every predicate defined in the canonical Predicate Vocabulary (Everest 65) has at least one positive and one negative test case. Edge cases are documented.
- **Purpose for V2:** The verifier runs every test case through their built verifier; all outputs must match.

### 4. Live test deployment — permanent test proof

- **URL:** `https://test.[PROJECT-SITE]` (replace at launch).
- **Purpose:** A long-running deployment that produces and serves a fixed test proof, plus a generator endpoint that produces fresh proofs on request with documented inputs.
- **Stability commitment:** Calm commits to keeping the live test deployment available for at least 5 years from the bounty's launch date. The deployment's URL, signing keys, and anchor chain are versioned; any breaking change is announced 90 days in advance.
- **Purpose for V3:** The verifier obtains a real proof (either the permanent fixed proof or a fresh one) and verifies it end-to-end.

### 5. Spec Q&A channel

- **Format:** A public chat channel (Slack/Discord/IRC — final choice at launch). Anyone may join; messages are publicly archived.
- **Purpose:** Verifiers may ask spec questions — "what does the specification mean by X in section Y?" — and get answers from Calm contributors.
- **Important limit:** **The Q&A channel is for spec questions, not implementation help.** Calm contributors will answer "what does the spec say?" but will not answer "why is my build failing?" or "what should my Rust code look like?" The independence criterion requires that the verifier's build be theirs. Coaching the build would compromise the verification.
- **Why it is public, not private:** The Q&A is public so that other verifiers see answered questions and benefit from them, and so that Calm cannot privately favor one verifier over another. If a Calm contributor accidentally provides too much implementation guidance, the public archive lets the DERB notice and intervene.

### 6. Differential-test baseline

- **URL:** Published as part of the test corpus and additionally as a separate baseline-results file in the repository.
- **Purpose:** When a verifier runs the test corpus through their built verifier, they can compare not only against the expected outputs but also against the outputs produced by the reference implementation in published form. This catches build-portability bugs (the verifier's build differs subtly from the reference build) earlier in V1/V2 than they would otherwise be caught.

### 7. Public key material

- **Verifying organization key directory:** A public list of cryptographic keys for Calm contributors who sign protocol artifacts. Verifiers use this to confirm the authenticity of the spec, the implementer's guide, the test corpus, and the live deployment's proofs.
- **Trust anchor:** The Calm Witness chain itself — verifiers may walk the chain to confirm the key material is consistent with the chain's records.

### 8. Security audit report (Everest 90)

- **URL:** Published when the audit completes (Everest 90 prereq).
- **Purpose:** Verifiers may read the audit report to understand what kinds of bugs the auditor looked for and what was found. This helps the verifier scope V6 (adversarial probing) — the verifier should attempt tests *not* covered by the audit, since covering the same ground produces less marginal value.

### 9. T1–T12 adversarial-test enumeration (Everest 41)

- **URL:** Published as part of the protocol specification.
- **Purpose:** V6 asks the verifier to attempt at least one creative adversarial test *not* already in T1–T12. The enumeration tells the verifier what is already covered, so they know where to look for novel territory.

### 10. Prior verification write-ups (after the first successful verification)

- **URL:** Each accepted write-up is anchored into the chain and referenced from the project site.
- **Purpose:** Future verifiers may read prior verifications to understand what kinds of tests have already been run, what kinds of findings have already been filed, and what kinds of doc improvements have already been proposed. The intent is not to coordinate verifications — that would compromise independence — but to let each verifier add marginal value rather than duplicate prior work.

---

## What we do not provide

This list is as important as the previous one.

- **Implementation help.** Calm does not write code for the verifier, debug the verifier's build, review the verifier's verifier-code, or coach the verifier through specific implementation choices. The independence criterion forbids it.
- **Custom-configured binaries.** Calm does not provide a pre-built `calm-witness` binary that the verifier just runs. The verifier must build from source.
- **Calm-supplied forks.** Calm does not maintain a fork of `calm-witness` "for the verifier's use." If the verifier wants to fork, they fork from the canonical upstream and own the fork themselves.
- **Pre-review.** Calm does not pre-review draft write-ups before publication. The write-up is the verifier's; Calm reviews it only after it is published.
- **Compensation beyond the bounty.** Calm does not pay separate hourly rates, expenses, or per-bug discovery fees. The bounty tier table is the total compensation Calm offers for the work.
- **Promises about verdicts.** Calm does not commit to accepting any particular finding, adopting any particular doc change, or fixing any particular bug. The protocol's commitment is to *respond publicly* to findings, not to *agree* with them.

## Updating this resource list

If a verifier encounters a need for which no resource on this list applies — and the gap is not deliberately omitted per the "what we do not provide" section — please file a `doc` issue on the `calm-witness` repository. The gap itself is a finding; it counts toward V5 (doc accuracy) and may count toward the substantive-bug bonus.

— Calm, 2026-05-20
