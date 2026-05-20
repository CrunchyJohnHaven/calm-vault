# Calm Witness — Standing Red-Team Protocol v0 (S225)

## Overview

This document specifies the Standing Red-Team Protocol for the Calm Witness system. Red-teaming is a continuous, adversarial assurance program — not a one-time audit. Without sustained offensive pressure, defenses calcify, threat models go stale, and the master attack corpus (S224) stops reflecting real attacker capability. S225 defines the operational rules that keep red-team activity ongoing, bounded, and integrated with the broader conformance and bounty infrastructure.

---

## 1. Scheduling Cadence

**Minimum obligation:** One documented attack attempt per calendar month. An "attempt" means a structured engagement that produces a written finding — positive (vulnerability confirmed), negative (control held), or inconclusive (scope gap identified).

Engagement types rotate across three tracks to prevent coverage fixation:

- **Track A — Structural attacks.** Attestation chain forgery, zkBB circuit manipulation, commitment reuse, Merkle proof spoofing. Prioritized in months 1, 4, 7, 10.
- **Track B — Behavioral attacks.** Prompt injection against Calm Witness inference layers, context poisoning of user-state snapshots, adversarial compaction triggering false priors. Prioritized in months 2, 5, 8, 11.
- **Track C — Social and protocol attacks.** Sybil injection into trust networks, coercion-path exploitation, coordinator collusion, timing-side-channel leakage across the disclosure window. Prioritized in months 3, 6, 9, 12.

Unscheduled surge engagements are permitted at any time and do not satisfy the monthly minimum unless they produce a complete finding artifact. All findings, regardless of track, are filed to the master attack corpus within 72 hours of conclusion.

---

## 2. Rules of Engagement

**Authorization.** Only operators listed in the current red-team roster may conduct authorized engagements. Roster changes require approval from the CALM project lead and are logged with a timestamp and scope delta.

**Tooling.** Automated scanners are permitted in sandbox only. Production-scoped work must be manual or use tooling explicitly pre-approved per engagement. No tooling that generates synthetic user-state records indistinguishable from real ones is permitted in production at any time.

**Data handling.** Findings that contain extracted production data must be sanitized within 24 hours of capture. Raw extracts may not leave the secure finding repository. Red teamers sign a data-handling acknowledgment before roster entry.

**Stopping conditions.** An engagement must halt immediately if: (a) it threatens real user data integrity beyond controlled extraction, (b) it triggers cascading failures observable to users, or (c) the operator loses confidence in scope containment. Halted engagements are documented as partial findings; partial findings count toward corpus coverage but not the monthly minimum.

**Conflict of interest.** A red teamer may not assess a component they personally implemented within the preceding 90 days without a co-operator who has no authorship stake.

---

## 3. Scope

**In-scope (sandbox):** All Calm Witness system components running in the designated sandbox environment. This includes the zkBB attestation pipeline, user-state snapshot store, Merkle proof infrastructure, conformance test harness (S226), and all API surfaces exposed to external validators.

**In-scope (production — read-path only):** Passive traffic analysis, timing measurement, and public-surface probing. Explicit written approval required per engagement, logged before work begins.

**Out of scope (production — write-path):** Any action that creates, modifies, or deletes real user-state records, attestation anchors, or conformance suite state. Out-of-scope actions performed by a red teamer — even accidentally — must be disclosed to the CALM lead within one hour of discovery.

**Bounty intersection:** External reports submitted through the bounty program (S234) that fall within red-team scope are triaged by red team before bounty adjudication. Red teamers may not submit bounty claims for findings generated during authorized engagements.

---

## 4. Disclosure Window

**Internal disclosure (Day 0):** Finding filed to the secure finding repository and the master attack corpus (S224) within 72 hours of conclusion.

**Fix window:** Owners of the affected component receive a minimum 30-day window to ship a confirmed fix before any external disclosure. Complex structural vulnerabilities (circuit-level, cryptographic) may be granted a 60-day window with written justification from the CALM lead. Extensions beyond 60 days require disclosure of the extension fact to the Public Hall (see Section 5) without revealing the vulnerability detail.

**Responsible disclosure:** If a finding represents an active exploitation risk, the fix window begins immediately and disclosure to affected stakeholders is evaluated case-by-case. Red teamers do not have unilateral authority to accelerate public disclosure.

**Stale findings:** A finding with no fix action and no extension granted at day 45 is escalated automatically to the CALM lead for decision. Escalation fact is logged in the corpus regardless of outcome.

---

## 5. Public Hall of Findings

A public Hall of Findings is maintained at a stable URI. Each entry records: finding ID, affected component, severity classification, track, discovery date, disclosure date, resolution status, and corpus cross-reference. Vulnerability detail is omitted until the fix window closes. Negative findings (controls held) are published without restriction after filing.

The Hall serves as the primary accountability surface for the red-team program. Gaps between monthly cadence obligations and Hall entries signal process failures and must be explained in the subsequent finding.

---

## 6. Cross-References

| Reference | Relationship |
|---|---|
| S224 — Master Attack Corpus | All red-team findings file here within 72 hours; corpus coverage drives track prioritization. |
| S226 — Conformance Suite | Red-team findings that expose conformance gaps trigger suite updates before the finding is closed. |
| S234 — Bounty Program | External bounty reports within red-team scope are triaged by red team; red teamers cannot claim bounties for authorized-engagement findings. |

---

Calm 2026-05-20
