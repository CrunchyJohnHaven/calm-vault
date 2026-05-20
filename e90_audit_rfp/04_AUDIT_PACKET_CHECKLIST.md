# Pre-Audit Packet Checklist

*Internal document. The contents auditors receive at engagement kickoff. Owners fill in `Status` as items move from Pending → In Progress → Ready → Delivered. No kickoff until every row is `Ready`.*

This checklist consolidates and operationalizes Section "Audit Packet Contents" of Everest 90. It is the procurement owner's primary tracking artifact during the 4–6 week pre-audit preparation phase.

---

## Specification Documents

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 1 | Protocol specification v0 | `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_PROTOCOL_v0.md` | Documentation | Pending |
| 2 | Naming and branding glossary | `/Users/johnbradley/AllData/calm_vault_market/NAMING_AND_BRANDING.md` | Documentation | Pending |
| 3 | Route map (100 Everests) | `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_EVERESTS_100.md` | Documentation | Pending |
| 4 | Pedersen parameters reference | `/Users/johnbradley/AllData/calm_vault_market/PEDERSEN_PARAMETERS_v0.md` | Engineering | Pending |
| 5 | Pedersen on Ristretto255 design doc | `/Users/johnbradley/AllData/calm_vault_market/EVEREST_44b_PEDERSEN_RISTRETTO_v0.md` | Engineering | Pending |
| 6 | Predicate language specification | `/Users/johnbradley/AllData/calm_vault_market/PREDICATE_LANGUAGE_v0.md` | Engineering + DERB | Pending |
| 7 | Predicate vocabulary v0 | `/Users/johnbradley/AllData/calm_vault_market/PREDICATE_VOCABULARY_v0.md` | DERB | Pending |
| 8 | User state substrate protocol | `/Users/johnbradley/AllData/.calm-vault/USER_STATE_PROTOCOL.md` | Engineering | Pending |
| 9 | Calm Pact (sister protocol context) | `/Users/johnbradley/AllData/calm_vault_market/CALM_PACT_PROTOCOL_v0.md` | Engineering | Pending |
| 10 | Selected per-Everest design docs (E1, E26–28, E36–38, E41, E44–45, E51–58, E66–78) | `everests/everest_NN_*.md` (path list provided in audit packet manifest) | Documentation | Pending |

## Reference Implementation Code Freeze

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 11 | Git tag of `calm-witness` Rust crate at audit-start commit (`v0.X.Y-audit-frozen`) | `git tag v0.X.Y-audit-frozen` in `calm-witness` repo | Engineering | Pending |
| 12 | Build instructions reproducing the audited binary bit-for-bit | `BUILD.md` in `calm-witness` repo at frozen tag | Engineering | Pending |
| 13 | Source tree archive at the tagged commit (`.tar.gz` with checksum) | `audit_packet/calm-witness-v0-frozen.tar.gz` | Engineering | Pending |
| 14 | `cargo audit` clean report at tag time | `audit_packet/cargo-audit-report.txt` | Engineering | Pending |
| 15 | Test suite passing log (`cargo test --all-features`) | `audit_packet/test-suite-log.txt` | Engineering | Pending |
| 16 | WASM/JS port frozen tag + build artifacts | `calm-witness-wasm` repo tag + `audit_packet/wasm-build/` | Engineering | Pending |
| 17 | Python reference implementation (auxiliary, for differential testing) | `calm-witness-py` repo tag + `audit_packet/python-impl/` | Engineering | Pending |

## Threat Model and Privacy Claims

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 18 | Threat model document (adversaries A1–A6 from E1 §2; biometric threats T1–T12 from E41) | `audit_packet/THREAT_MODEL.md` | Engineering + DERB | Pending |
| 19 | Privacy claims P1–P5 with attack-tree analysis | `audit_packet/PRIVACY_CLAIMS.md` | Engineering | Pending |
| 20 | Out-of-scope and non-claim list (rubber-hose, enrollment compromise, PQC, etc.) | `audit_packet/OUT_OF_SCOPE.md` | Engineering | Pending |

## Dependency SBOM

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 21 | Complete `cargo tree` output | `audit_packet/sbom/cargo-tree.txt` | Engineering | Pending |
| 22 | Per-dependency: version, license, last-update date, known-CVE status | `audit_packet/sbom/dependencies.csv` | Engineering | Pending |
| 23 | Flagged unmaintained or deprecated dependencies with rationale | `audit_packet/sbom/dependency-flags.md` | Engineering | Pending |
| 24 | WASM/JS dependency SBOM (npm or equivalent) | `audit_packet/sbom/wasm-dependencies.csv` | Engineering | Pending |

## Known-Issue List

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 25 | All open issues from the tracker, severity-tagged | `audit_packet/known_issues/open.md` | Engineering | Pending |
| 26 | Previously-found-and-fixed bugs with commit references | `audit_packet/known_issues/fixed.md` | Engineering | Pending |
| 27 | Deliberate design decisions with alternatives-considered rationale | `audit_packet/known_issues/design_choices.md` | Engineering | Pending |
| 28 | Internal review notes from prior Calm-side reviews | `audit_packet/known_issues/prior_reviews.md` | Engineering | Pending |
| 29 | Open issue from `CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md` (cross-reference flagged for auditor awareness) | `/Users/johnbradley/AllData/calm_vault_market/CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md` | Engineering | Pending |

## Cryptographic Construction Notes

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 30 | Curve choice rationale (Curve25519 / Ed25519 / X25519 / Ristretto255) | `audit_packet/crypto_notes/curves.md` | Engineering | Pending |
| 31 | Pedersen generator selection method (proof that `log_g(h)` is unknown) | `audit_packet/crypto_notes/pedersen_generators.md` | Engineering | Pending |
| 32 | Σ-protocol composition with Fiat-Shamir — transcript order + hash function | `audit_packet/crypto_notes/sigma_fiat_shamir.md` | Engineering | Pending |
| 33 | Threshold aggregation choice (BLS12-381 vs FROST) with rationale | `audit_packet/crypto_notes/threshold.md` | Engineering | Pending |
| 34 | Range proof construction (Bulletproofs on Ristretto255) | `audit_packet/crypto_notes/range_proofs.md` | Engineering | Pending |
| 35 | Hash function choices (SHA-256 chain; Poseidon-friendly considerations) | `audit_packet/crypto_notes/hashes.md` | Engineering | Pending |

## Differential Testing & Fuzzing Evidence

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 36 | Differential test results (Everest 94 cross-implementation) | `audit_packet/testing/differential.md` | Engineering | Pending |
| 37 | Golden test corpus (Everest 64) frozen at audit version | `audit_packet/testing/golden_corpus/` | Engineering | Pending |
| 38 | Property-based test results (Everest 86, 87) | `audit_packet/testing/properties.md` | Engineering | Pending |
| 39 | Adversarial fuzzing logs (Everest 85) — 30+ days clean | `audit_packet/testing/fuzz_logs/` | Engineering | Pending |
| 40 | Coverage report indicating fuzz-target coverage of critical paths | `audit_packet/testing/coverage.html` | Engineering | Pending |

## Operational Notes

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 41 | Deployment topology (operator location, verifier location) | `audit_packet/ops/topology.md` | Engineering | Pending |
| 42 | Key-management overview (master key custody, agent key issuance) | `audit_packet/ops/key_mgmt.md` | Engineering | Pending |
| 43 | Logging and monitoring posture | `audit_packet/ops/logging.md` | Engineering | Pending |
| 44 | Incident-response procedures | `audit_packet/ops/incident_response.md` | Engineering | Pending |
| 45 | Principal's audit interface (Everest 78 disclosure logging) | `audit_packet/ops/principal_audit.md` | Engineering | Pending |

## Procedural and Administrative

| # | Item | File Path | Owner | Status |
|---|------|-----------|-------|--------|
| 46 | Scope document (the 2–4 page summary that begins the packet) | `audit_packet/SCOPE.md` | Calm operations | Pending |
| 47 | Auditor onboarding doc (how to use the issue tracker, weekly cadence, etc.) | `audit_packet/ONBOARDING.md` | Calm operations | Pending |
| 48 | Designated audit-liaison contact details | `audit_packet/LIAISON.md` | Calm operations | Pending |
| 49 | Signed SoW (copy in packet) | `audit_packet/SIGNED_SOW.pdf` | Legal | Pending |
| 50 | Signed mutual NDA (copy in packet) | `audit_packet/SIGNED_NDA.pdf` | Legal | Pending |

---

## Acceptance Criterion

No audit kickoff until every row above is `Ready`. The procurement owner and the engineering lead co-sign a one-page "packet ready" memo confirming completeness; this memo is anchored into the chain as `kind: "audit_packet_ready"` per Everest 90's coordination notes.

Items derived from Everest 90's pre-audit checklist (Status: Pending) that gate this packet (Everest 81 feature-complete, Everest 82 feature-complete, Everest 83 WASM port, Everest 84 SDK polished, Everest 85 fuzzers 30 days clean, Everest 86/87 property tests, Everest 88 performance budget) are tracked separately on the engineering board; this checklist assumes those gates are green.

---

— Calm, 2026-05-20
