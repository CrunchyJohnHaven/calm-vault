# Calm Witness — Deprecation Timeline Spec v0 (S211)

**Status:** Draft  
**Summit:** S211  
**Date:** 2026-05-20  
**Depends on:** S125 (Predicate Registry), S128 (Vocabulary Governance), S212 (Tombstone Process)

---

## Overview

This spec defines the fixed timeline governing retirement of predicates, vocabularies, or other registry items within the Calm Witness system. All deprecations must follow three phases in sequence: announcement, migration window, and sunset. Skipping or compressing phases is not permitted without a governance exception recorded in the Review Board log (see S128).

---

## Announcement Cadence

A deprecation is initiated by publishing a signed Deprecation Notice to the Predicate Registry (S125). Requirements:

- The notice must be published no fewer than **90 days** before the sunset date.
- The notice must identify: (a) the item being deprecated by canonical URI and version, (b) the sunset timestamp as a UTC ISO-8601 date, (c) the replacement item or migration path, and (d) the issuing authority (agent identity or Review Board seat).
- The notice must carry a valid Calm Witness attestation; unsigned notices are rejected by the registry.
- Once published, the sunset date is fixed. Extensions require a separate amendment notice, also subject to the 90-day floor from the extended date.

---

## Migration Window

The period between announcement and sunset is the migration window. Obligations during this window:

- The deprecated item remains fully operational and resolvable throughout the migration window. Registry operators must not degrade resolution, rate-limit selectively, or remove documentation ahead of sunset.
- The replacement item or migration path must be live and documented no later than **T-60** (60 days before sunset). Announcing a deprecation without a ready migration path at T-60 triggers a review-board escalation.
- Producers who have issued proofs referencing the deprecated item are responsible for re-issuance using the successor item before sunset. Calm Witness does not auto-migrate existing proofs.
- Consumers are expected to update verification logic to accept both old and new items during the migration window; the grace window (see below) covers the transition period after sunset.

---

## Warning Cadence

The registry emits timed warnings to all subscribed consumers and registered producers at the following intervals before sunset:

| Checkpoint | Action |
|---|---|
| T-90 | Initial deprecation notice broadcast; window opens. |
| T-60 | Reminder broadcast; migration path must be live by this date. |
| T-30 | Final-month warning; consumers with no acknowledged plan flagged. |
| T-7 | Last-call warning; registry marks item as sunset-imminent in all resolution responses. |
| T-0 | Sunset. Item transitions to tombstone state per S212. |

Warnings are delivered via the Consumer Notification mechanism (see below). Silence is not acknowledgment; consumers who have not confirmed migration readiness by T-30 are flagged in the registry metadata.

---

## Tombstone Linkage

At sunset (T-0), the deprecated item is handed off to the Tombstone Process defined in S212. Key linkage points:

- The registry sets item state to `TOMBSTONED` and records the tombstone timestamp.
- The tombstone record preserves the canonical URI, all historical attestations, and a pointer to the successor item. Resolution of the URI returns a 410-equivalent response with tombstone metadata attached.
- Tombstone records are immutable and permanent. They serve as audit anchors for proofs issued before sunset.
- S211 does not define tombstone internals; those are owned by S212. This spec only defines the handoff trigger (T-0) and the requirement that tombstone records be resolvable within 24 hours of sunset.

---

## Grace Window

A **30-day grace window** follows sunset to support verification of proofs issued before T-0:

- During the grace window, verifiers may resolve the tombstone record to confirm that a proof was issued against a valid item at time-of-issuance.
- No new proofs referencing the deprecated item are accepted after T-0, including within the grace window.
- After the grace window closes (T+30), historical proof verification must route through archival attestation records maintained by the registry operator. Availability of archival records is governed by S128 retention policy, not this spec.

---

## Consumer Notification Mechanism

Subscribed consumers receive warnings through the registry event feed:

- Subscription is established at predicate or vocabulary resolution time; any resolver that queries an item is auto-enrolled for deprecation notices on that item.
- Notices are delivered as signed registry events, structurally identical to attestation events (S125 format).
- Consumers may additionally register an explicit notification endpoint (webhook or pull-queue) in the registry. Explicit registration overrides auto-enrollment and allows batching.
- Delivery failure at T-30 or later must be logged and escalated; the registry operator is responsible for confirming receipt or escalating to the Review Board.

---

## Cross-References

| Spec | Relevance |
|---|---|
| S125 | Predicate Registry; home of the Deprecation Notice schema and subscription model. |
| S128 | Vocabulary Governance; defines authority to issue deprecations and retention policy for archival records. |
| S212 | Tombstone Process; owns tombstone record structure, resolution behavior, and post-grace archival. |

---

*Calm 2026-05-20*
