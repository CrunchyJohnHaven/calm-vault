# Everest 92 — Open-Source Release

*Phase VIII — Governance & Scale. Prereq: Everest 81, Everest 4.*

## Overview

This everest gates the public release of Calm Witness as open-source software under Apache License 2.0. It defines the repository layout, artifact production, communication plan, and support posture. The release is staged in three gates: v0.1.0 (RC) when specifications are stable; v0.5.0 (Beta) when the Rust production implementation ships; v1.0.0 (GA) when the first production deployment under Everest 99 succeeds.

The acceptance criterion: `calm-witness` published under Apache-2.0 at `github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness` with all required documentation, examples, and reference implementations in place. The repository must be peer to the existing `calm-pact` directory within the `calm-vault` monorepo.

## Repository Structure

The `calm-witness` directory is organized for developer onboarding, implementer reference, and auditor comprehension:

```
calm-vault/
  calm-pact/                    # existing
  calm-witness/                 # NEW v0
    LICENSE                     # Apache-2.0 verbatim
    NOTICE                      # contributors and non-aggression statement
    README.md                   # tagline, quick-start, links to docs
    SECURITY.md                 # vulnerability disclosure process
    CONTRIBUTING.md             # DCO sign-off, PR process, code style
    CODE_OF_CONDUCT.md          # community standards
    docs/
      protocol-v0.md            # links to ZKBB_USER_PROTOCOL_v0.md
      route-map.md              # links to ZKBB_USER_EVERESTS_100.md
      everests/                 # all 100 everest spec documents
    crates/
      calm-witness-rs/          # Rust reference implementation (E43, E81)
      calm-witness-zk-rs/       # ZK primitives and proof system (E45, E65)
      calm-witness-cli/         # CLI binary, end-user tool
    python/
      calm_witness/             # Python reference implementation (E82)
    js/
      calm-witness-wasm/        # WASM/JavaScript bindings (E83)
    examples/                   # runnable examples for each binding
    tests/                       # integration and property-based tests
    .github/
      workflows/                # CI/CD matrix (Rust, Python, JS, container)
```

The `docs/everests/` subdirectory is a git submodule or symlink to the everest specifications in `calm_vault_market/everests/`. This keeps implementer documentation and specification in lockstep.

## Release Gates and Versioning

### v0.1.0 Release Candidate

**Gate condition:** E1 through E80 specification documents are stable and copy-edited (≥95% of the route map). Code implementations may be partial or placeholder.

**Deliverables:**
- Draft protocol document in `docs/protocol-v0.md` cross-linked to ZKBB_USER_PROTOCOL_v0.md
- Skeleton implementations in all three bindings (Rust, Python, JS)
- Example CLI with command structure and help text
- Test stubs and integration test framework
- CI/CD workflows that compile and lint

**Artifacts:**
- Source tarball, signed with sigstore
- GitHub Releases page with tag v0.1.0-rc

**Communication:**
- RFC thread on cryptography@metzdowd
- IACR forums announcement
- Internal stakeholder notification (journalists, foundations, accelerators)

### v0.5.0 Beta

**Gate condition:** Everest 81 (Rust production implementation) ships complete. The Rust reference implementation in `crates/calm-witness-rs` passes all conformance tests and handles the full state-hydration and predicate-evaluation loop.

**Deliverables:**
- Rust crates published to crates.io: `calm-witness`, `calm-witness-zk`, `calm-witness-cli`
- Python package to PyPI: `calm-witness`
- JavaScript/WASM packages to NPM: `@calm/witness`, `@calm/witness-wasm`
- Container images on ghcr.io for the CLI and reference verifier
- Pre-built CLI binaries for Linux (x86_64, ARM64), macOS (Intel, Apple Silicon), Windows
- Security advisories process operational in SECURITY.md
- Governance docs published: Everest 95 (predicate registry), Everest 80 (ethics review board), Everest 54 (audit process)

**Artifacts:**
- Source tarballs, signed with sigstore
- Package and container image checksums and signatures
- GitHub Releases page with tag v0.5.0-beta

**Communication:**
- Launch blog post at vault.thecreativitymachine.ai/calm-witness
- HackerNews submission and lobste.rs submission
- Targeted outreach to: Karen Hao, Cade Metz, Will Knight, Janus Rose (technology journalists)
- LessWrong, EA Forum, and Alignment Forum posts
- Cryptography mailing list final announcement

### v1.0.0 General Availability

**Gate condition:** Everest 99 (first production deployment under Creativity Machine LLC and Calm operator identity) completes successfully. The live demo at calmwitness.thecreativitymachine.ai has processed counterparty verification for at least 90 days without security incident.

**Deliverables:**
- All v0.5.0 artifacts remain current
- Patch releases (v1.0.x) for security and stability during production runtime
- Long-term support (LTS) commitment for v1.x major version
- Production operational runbook and troubleshooting guide

**Communication:**
- Public announcement of production readiness
- Case study or deployment blog post
- Invitation to independent auditors and penetration testers

## Release Artifacts

### Code Archives

Source tarballs are produced for each release and signed with sigstore:

```
calm-witness-0.1.0-rc.tar.gz     (gzipped tarball)
calm-witness-0.1.0-rc.tar.gz.sig (detached sigstore signature)
calm-witness-0.1.0-rc.tar.gz.sbom (SPDX SBOM)
```

Published on GitHub Releases and mirrored to archive.org.

### Package Registries

**Rust (crates.io):**
- `calm-witness` — high-level API and protocol state machine
- `calm-witness-zk` — ZK proof system and predicate evaluation
- `calm-witness-cli` — command-line interface

**Python (PyPI):**
- `calm-witness` — Python bindings to Rust core, pure-Python fallbacks

**JavaScript/Node (NPM):**
- `@calm/witness` — TypeScript types and node bindings
- `@calm/witness-wasm` — browser-compatible WASM

### Container Images

Published on ghcr.io/crunchyjohnhaven/ with SemVer tags and latest pointer:

- `ghcr.io/crunchyjohnhaven/calm-witness-cli:v0.5.0`
- `ghcr.io/crunchyjohnhaven/calm-witness-verifier:v0.5.0`
- `ghcr.io/crunchyjohnhaven/calm-witness-dev:v0.5.0`

All images are signed with cosign and include SBOMs.

### Pre-built Binaries

CLI binaries are produced for:
- Linux: x86_64, ARM64, ARM32
- macOS: x86_64, arm64 (Apple Silicon)
- Windows: x86_64, ARM64

Distributed via GitHub Releases with checksums and signatures. Checksums are posted to the public transparency log (Sigsum).

## Public Communication and Outreach

### Content Channels

**Technical announcement:**
- Cryptography mailing list (cryptography@metzdowd.com)
- IACR forums (iacr.org)
- IEEE Security & Privacy discussions

**AI safety and governance:**
- LessWrong (AI alignment tag)
- Effective Altruism Forum
- Center for AI Safety forum
- Alignment Forum

**Open-source and privacy communities:**
- HackerNews (with substantive post linking to docs)
- Lobste.rs
- Reddit r/cryptography, r/privacy, r/rust

**Journalists:**
Outreach to technology reporters who cover AI governance and cryptography:
- Karen Hao (WIRED, focus on AI safety)
- Cade Metz (New York Times, AI coverage)
- Will Knight (WIRED, emerging tech)
- Janus Rose (tech culture and autonomous agents)

### Reference Deployment

A live demo runs at calmwitness.thecreativitymachine.ai. The demo includes:

- A reference Calm operator instance running on behalf of John Bradley (Creativity Machine LLC)
- Interactive proof verification interface where counterparties can submit a predicate query and receive a ZK proof
- Audit log of all disclosures (timestamps, predicates, verifying counterparties, without leaking the underlying state record)
- Educational walkthroughs of the protocol flow

This demo must remain live and operational for at least 90 days prior to v1.0.0 GA gate.

## Versioning and Support

### Semantic Versioning

All packages follow Semantic Versioning:

- `MAJOR.MINOR.PATCH`
- v0.x during specification development (breaking changes permitted)
- v1.x and onward: breaking changes only in MAJOR version bumps

### Support Lifecycle

**v0.1.0 (RC):** 6 months. Bug and security fixes only. No feature additions.

**v0.5.0 (Beta):** 12 months. Security fixes prioritized. Bug fixes as resources allow. Feature additions limited to those mandated by Everests 81, 82, 83.

**v1.x (LTS):** Minimum 36 months. All critical and high-severity security fixes. Low-severity bug fixes on best-effort basis. Feature additions in minor versions only.

**Deprecation:** Any breaking change is announced 12 months in advance via:
- Security advisory in SECURITY.md
- Release notes (CHANGELOG.md)
- Blog post
- Email to registered users (via GitHub)

### Maintenance Policy

- Security fixes are released as patch versions (PATCH bump) within 48 hours of responsible disclosure
- Regression fixes are released as patch versions within one week
- Minor features and backports land in regular cadence (every 4–6 weeks)
- Major refactors are scheduled between minor releases, announced 60 days in advance

## Governance Documents in Release

The release includes references to five governance everests. These are published in `docs/everests/`:

**Everest 4 — License & IP Posture:** Apache-2.0, no CLA, defensive patent stance, non-aggression statement binding Creativity Machine LLC.

**Everest 54 — Predicate Audit Process:** Describes how new predicates are audited before admission to the registry. Implementers and external auditors participate.

**Everest 80 — Ethics Review Board:** Composition, scope, and decision authority of the ethics review board that gates production deployments to new use cases.

**Everest 95 — Predicate Registry Governance:** Rules for registering new predicates, deprecation of old ones, consensus process among implementers.

**Everest 98 — Implementer's Guide:** Step-by-step instructions for integrating Calm Witness into an autonomous agent platform. Cross-references all APIs and bindings.

Implementers are required to read Everests 4, 54, 80, and 95 before deploying to production.

## Cross-References and Dependencies

This everest depends on completion and stabilization of:

- **E4** — License & IP Posture (defines Apache-2.0 and non-aggression)
- **E43** — Rust Proof System (core algorithm and circuits)
- **E45** — ZK Primitives (commitment schemes, Σ-protocols)
- **E53** — Predicate Specification Grammar (formal language for predicates)
- **E54** — Predicate Audit Process (before any predicate is published)
- **E65** — Efficient ZK for Behavioral Biometrics (optimization for e.g. biometric distance)
- **E80** — Ethics Review Board (governance authority for production gates)
- **E81** — Rust Production Implementation (full feature implementation)
- **E82** — Python Reference Implementation (binding and test suite)
- **E83** — JavaScript/WASM Binding (browser support)
- **E95** — Predicate Registry Governance (operational rules for predicate library)
- **E98** — Implementer's Guide (onboarding documentation)
- **E99** — Production Deployment (operational gate; blocks v1.0.0 GA)

## Success Criteria

This everest is complete when all of the following hold:

1. **Repository:** calm-witness directory exists at github.com/CrunchyJohnHaven/calm-vault/tree/main/calm-witness with all files listed in the Repository Structure section.

2. **License:** LICENSE file contains Apache License 2.0 verbatim. NOTICE file names Creativity Machine LLC and CredexAI as initial contributors and republishes the non-aggression statement from Everest 4.

3. **Documentation:** README.md, CONTRIBUTING.md, SECURITY.md, and CODE_OF_CONDUCT.md are populated and reviewed. docs/protocol-v0.md and docs/route-map.md exist and link to the underlying specifications.

4. **Implementations:** At least one crate or package (calm-witness-rs, calm_witness, or calm-witness-wasm) has a passing test suite on all three supported architectures for its platform.

5. **CI/CD:** .github/workflows/ contains matrix build for Rust, Python, and JavaScript on Linux, macOS, and Windows. All green.

6. **Governance:** Everests 4, 54, 80, 95, and 98 are in the release and marked complete.

7. **Accessibility:** The repository is publicly accessible on GitHub, cloneable without authentication, and indexed by GitHub search and Google.

8. **Artifacts:** Source tarballs for v0.1.0-rc are signed and published. Checksums are posted to Sigsum.

9. **Communication:** At least one announcement has been published on cryptography@metzdowd and IACR forums.

10. **Operability:** The reference deployment at calmwitness.thecreativitymachine.ai has processed at least 10 test verification requests without failure and is running the release branch code.

— Calm, 2026-05-20
