# Calm Compass — Predicate Audit Process v0

**Draft v0 · 2026-05-20 · Calm**
**Closes Everest 115 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**
**Extends [`PREDICATE_AUDIT_PROCESS_v0.md`](PREDICATE_AUDIT_PROCESS_v0.md) (Calm Witness Everest 54).**
**Prereq: [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md).**

## §1 — Scope

This document governs **proposing, reviewing, accepting, and deprecating** Calm Compass predicate IDs and evidence kinds. Every `cwp.compass.v0.*` predicate in the v0 founding catalog (Everest 103) or minted later MUST follow this process.

Witness audit rules apply **unless** this document specifies a Compass overlay.

## §2 — Standing panel (Witness + Compass extensions)

Minimum panel size remains **≥ 5** external reviewers (Witness §3), **plus** three Compass-mandatory seats:

| Seat | Lens |
|------|------|
| **Philosopher of values** | Whether the predicate measures an ethic worth attesting, not a cultural fad or partisan virtue. |
| **Ethicist** | Whether deployment incentives skew toward coercion, purity tests, or harm to vulnerable principals. |
| **Harm survivor practitioner** | Someone who has been on the receiving end of willful harm; reviews counter-claim fairness and dispute UX. |

Witness baseline seats (cryptographer, disability/cognitive-liberties advocate, behavioral-biometric researcher, AI-safety practitioner, journalist) remain required for cross-primitive releases.

No two panelists from the same organization. Conflicts disclosed per Witness §7.

## §3 — Refusal-floor triage gate (Everest 113)

**Before** Stage 2 review, every proposal passes automated + maintainer triage against [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4:

| # | Refused category |
|---|------------------|
| 1 | Race or ethnicity |
| 2 | Religion |
| 3 | Political affiliation |
| 4 | Sexual orientation |
| 5 | Gender identity |
| 6 | Immigration status |
| 7 | Criminal record |
| 8 | Donations to specific named causes |
| 9 | Opinions on contentious public-policy issues |
| 10 | Cross-principal comparison |
| 11 | Predictive predicates |
| 12 | Non-principal-defined group membership |

Proposals that traffic in these categories — directly or by euphemism — are **Reject at triage** with rationale logged to `compass_predicates_vN.audit_log.json` (chained, signed).

Triage also rejects:

- **Concord anti-purity violations** — numeric similarity scores, empty-purpose requirements, degenerate joint thresholds ([`CALM_CONCORD_PROTOCOL_v0.md`](CALM_CONCORD_PROTOCOL_v0.md) §4).
- **Scope violations** — any §2 use case in [`CALM_COMPASS_SCOPE_STATEMENT.md`](CALM_COMPASS_SCOPE_STATEMENT.md).

Triage SLA: **5 working days** (inherits Witness §6).

## §4 — Five-stage process (inherits Witness §4)

### Stage 1 — Draft

Author opens a PR adding:

- Predicate entry (JSON registry + COMPASS_PREDICATES prose section), **or** new `compass_evidence.*` kind in VALUES_EVIDENCE_TAXONOMY.
- Reference evaluator + **≥ 30** golden pairs (Everest 117 bar; v0 founding predicates grandfathered pending retro review).
- **Refusal-floor check** — explicit §4 confirmation.
- **Scope check** — explicit CALM_COMPASS_SCOPE_STATEMENT §2 confirmation.
- **Counter-claim impact** — for harm-related predicates, delta to [`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md).

### Stage 2 — Triage

Maintainer outcomes: Accept for review · Request revisions · **Reject at triage** (refusal floor / scope / anti-purity).

### Stage 3 — Review

30-day public window (extendable at protected-category boundaries). Reviewers cover:

- Evaluator determinism + ZK implementability (Witness Stage 3).
- Refusal-floor and scope compliance.
- Consent-matrix impact.
- Counter-claim and falsifiability implications.
- Golden corpus quality (peer review of Everest 117 tests).

### Stage 4 — Vote

Pass: **≥ 2 accept**, **0 block**; Compass seats may block on values-harm grounds with public reasoning. Maintainer ratifies.

### Stage 5 — Merge

Update `compass_predicates_vN.snapshot.json`, tag release, announce. Counter-claim protocol version field bumped if harm semantics change.

## §5 — Deprecation and tombstoning

Same thresholds as Witness §5. Tombstoned Compass IDs are never reissued. Deprecated predicates remain verifiable with warnings.

## §6 — Counter-claim and sketch audits

Standing obligations of the panel (not separate everests):

- Quarterly review of counter-claim intake volume and false-positive rate.
- Annual review of falsifiability sketch fields for identity leakage ([`COMPASS_FALSIFIABILITY_PROTOCOL_v0.md`](COMPASS_FALSIFIABILITY_PROTOCOL_v0.md) §4).
- Peer review sign-off on `test_compass_eval.py` golden corpora (Everest 117).

## §7 — v0 founding catalog

The six predicates in COMPASS_PREDICATES §2 and seven evidence kinds in VALUES_EVIDENCE_TAXONOMY were minted 2026-05-20 under maintainer authority (Everests 103–104). Retroactive Stage 3 review is scheduled before Compass v1 public release.

## §8 — Minimum cadence

Inherits Witness §6: 5-day triage SLA, 30-day review window, ≥5 active panelists / 12 months, vote disclosure within 5 working days.

— Musk, 2026-05-20
