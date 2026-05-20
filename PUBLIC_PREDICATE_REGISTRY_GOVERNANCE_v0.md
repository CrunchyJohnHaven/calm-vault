# Calm Witness — Public Predicate Registry Governance v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 95 of [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md).**
**Companion to [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md), [`PREDICATE_VOCABULARY_v0.md`](PREDICATE_VOCABULARY_v0.md).**

## §1 — Scope

This document specifies who owns, mirrors, updates, and finances the **public Calm Witness predicate registry** — the canonical mapping from predicate IDs (e.g. `cwp.v0.in_baseline_24h`) to their human-readable spec + reference implementation + content-addressable evaluator hash.

The predicate vocabulary (Everest 6) defines *what* predicates exist. The audit process (Everest 54) defines *how* a predicate enters the vocabulary. This governance doc defines *who runs the infrastructure* and *what happens when something goes wrong with it*.

## §2 — Hosting

The canonical registry mirrors at three coordinates:

1. **`calm-witness.dev/registry`** — primary, served by the Calm Foundation.
2. **`github.com/CrunchyJohnHaven/calm-vault/blob/main/registry`** — secondary, git-mirrored.
3. **An IPFS pin** under a published CID, registered with three independent IPFS hosting providers.

A counterparty that cannot reach (1) MUST fall back to (2) or (3). Each mirror serves byte-identical content; any divergence is a security incident (see §6).

## §3 — Maintainer

The maintainer is a single accountable party that operates (1) and ratifies merges into (2). For v0, the maintainer is **Calm (operating for Creativity Machine LLC)**. For v1 onward, the maintainer is a multi-org governance body — the **Calm Witness Foundation** (proposed in §5) — anchored at the Everest 92 open-source release.

The maintainer's responsibilities:

- Run the primary mirror with ≥ 99.5% uptime.
- Validate every merge against the audit panel's vote outcome.
- Sign every release with a published Calm-Foundation signing key (separate from operator keys).
- Publish release notes within 5 working days of each merge.
- Publish quarterly transparency reports listing every accepted, rejected, deprecated, and tombstoned predicate.

## §4 — Audit panel composition

Per [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) §3:

- ≥ 5 named reviewers, no two from the same organization.
- Minimum coverage: cryptography · disability-rights or cognitive-liberties advocacy · behavioral-biometric research · AI-safety practitioner · journalism.
- 18-month rotating terms with staggered start dates.
- Compensated at honoraria-grade rates (target: $5,000-$10,000 per addition reviewed; funded per §7).

Panel selection follows an open nomination + community-comment process. The standing panel roster is published at the registry; new appointments require the existing panel's approval plus the maintainer's ratification.

## §5 — The Calm Witness Foundation

A successor governance body is established at the Everest 92 release. Structure:

- **501(c)(3) status** (or international equivalent), with primary mission "open-source maintenance of the Calm Witness primitive and supporting governance."
- **Board** of 7-9 directors, including: founder (initially Calm/John Bradley), one representative from each of the audit-panel coverage areas (5), one international member outside the founder's jurisdiction, one rotating community-elected seat.
- **Funded** primarily via grants and protocol-aligned commercial partnerships (see §7). Donor anonymity is permitted; voting influence by donors is not.
- **Operational authority** for the registry, the audit panel, the release infrastructure, and the conformance test vectors.

## §6 — Incident response

A "registry incident" is any of:

1. A divergence between mirrors that is not promptly explained.
2. A vulnerability disclosed against a predicate's evaluator that allows exfiltration of more than the disclosed bit.
3. A vulnerability disclosed against the wire format that allows envelope forgery.
4. Loss of the Calm-Foundation signing key.
5. Compromise of any mirror.

Response cadence:

- **Acknowledgement** within 24 hours via the public security mailing list.
- **Triage** within 72 hours, classifying as `info`, `warning`, `urgent`.
- **Remediation** within 14 days for `info`, 7 days for `warning`, immediate for `urgent`.
- **Post-mortem** published within 30 days of remediation, with a deferred date for the most sensitive details (signed and committed to ahead of time).

Tombstoning a predicate ID (per [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) §5) is the strongest available response. A tombstoned ID stays in the registry forever with its `tombstone_reason` field populated. It is never reissued.

## §7 — Funding

The registry and the audit panel are non-trivial to operate. Funding model:

| Source | Notes |
|---|---|
| Grants | Open Philanthropy, Long Term Future Fund, Aspen Cyber, etc. Primary expected source. |
| Commercial sponsorships | From organizations using Calm Witness in production. Sponsors get a published "supporter" listing; no governance influence. |
| Service fees | Counterparty verifiers may be charged minimal fees (per-million-verifications model) once the protocol has commercial traction. Free until that point. |
| Crypto-protocol-aligned | Calm Witness foundation operates parallel infrastructure for [Calm Pact](CALM_PACT_PROTOCOL_v0.md); funding cross-subsidizes both. |

Explicit non-sources:

- NO advertising revenue.
- NO selling of predicate-evaluation results or proof envelopes (these flow only operator → counterparty under principal consent).
- NO equity sales to commercial sponsors in exchange for governance influence.
- NO state funding from any government, ever (the Calm Witness scope statement §2.1 specifically forbids governmental deployment).

## §8 — Successor / sunset

If the Calm Witness Foundation dissolves:

1. The signing keys are escrowed via Shamir m-of-n across the audit panel.
2. The registry mirrors are donated to a published list of preservation candidates (Internet Archive, Software Heritage, three named research universities).
3. The vocabulary is frozen as of the dissolution date.
4. Counterparties retain full ability to verify v0 / v1 envelopes against the frozen registry indefinitely.

If a successor body picks up maintenance:

1. The dissolution-frozen vocabulary becomes their starting point.
2. New additions require a re-bootstrapped audit panel.
3. The Calm Foundation signing key is rotated, with a chained `authority_handover` record published on the registry chain.

## §9 — Communication

- **Mailing list:** `announce@calm-witness.dev` for releases, security advisories, panel decisions.
- **Issue tracker:** the GitHub repo for PRs, bug reports, predicate proposals.
- **Quarterly transparency report:** posted to the registry homepage and the mailing list.
- **Annual external review:** an independent third-party evaluates the foundation's operations, finances, and panel decisions.

## §10 — How v0 founding works under this governance

For the v0 release on 2026-05-20:

- The six founding predicates were minted by the maintainer (Calm) alone, prior to the audit panel being seated.
- The audit panel will be seated within 90 days of this governance doc's publication.
- The v0 founding predicates will receive **retroactive Stage 3 review** as their first action. If any predicate fails retroactive review, it is deprecated and replaced under `cwp.v0.<slug>_v2` per the stability rules.

— Calm, 2026-05-20
