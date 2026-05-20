# Calm Witness — ZKAC Member Admission Ceremony v0 (S158)

Summit S158. Defines the canonical procedure for admitting a new principal-member to a Zero-Knowledge Accountability Collective (ZKAC). Admission failures — incomplete enrollment, charter-misalignment, vote irregularities — are the dominant source of ZKAC operational breakdown. This ceremony is mandatory and non-waivable.

---

## Prerequisites

Before a candidacy may be opened, the nominating member must confirm the following conditions are satisfied. Any unresolved prerequisite terminates the candidacy without prejudice to re-nomination.

**E11 Enrollment.** The candidate must hold a verified Calm Witness enrollment under protocol E11. Verification requires a valid Enrollment Attestation Token (EAT) bound to the candidate's principal identity key. The EAT must be current — not expired, not revoked — and must have been issued or renewed within 180 days of the nomination date. An enrollment under appeal or suspension does not satisfy this requirement.

**Calm Pact Alignment Check.** The candidate's public Calm Pact (as recorded in their Calm Witness substrate per E11 §3.2) must be checked against the ZKAC's charter instrument (see S154 for charter structure). The checking procedure:

1. Retrieve the candidate's active Calm Pact commitment hash from the Calm Witness ledger.
2. Retrieve the charter's alignment criteria vector from the ZKAC's canonical charter record.
3. Compute the alignment score using the standard charter-alignment function defined in S159.
4. The alignment score must meet or exceed the ZKAC's admission threshold, which is declared in the charter and cannot be altered after the candidacy opens.

A candidate who fails the alignment check may request a single re-evaluation no sooner than 30 days later, after updating their Calm Pact. The re-evaluation uses the alignment criteria vector current at the time of re-evaluation, not at the time of original nomination.

---

## Nomination

Any current principal-member in good standing (no active sanctions, dues current, vote record complete) may nominate a candidate. Self-nomination is prohibited.

The nominating member submits a Nomination Record containing:

- Candidate principal identity key (PID)
- Candidate EAT reference (issuer, serial, expiry)
- Alignment score and the alignment criteria vector hash used
- Nominator PID and timestamp
- A nomination statement of 50-500 words stating the basis for nomination relative to the ZKAC's charter purpose

The Nomination Record is submitted to the ZKAC's designated ceremony coordinator. The coordinator verifies the nominator's standing and the completeness of the record. If complete, the coordinator opens the candidacy and publishes the Nomination Record to the ZKAC's member-accessible ledger within 48 hours. Publication timestamp becomes the official candidacy-open time.

A nominator may withdraw the nomination at any time before the vote opens. Withdrawal closes the candidacy without a vote and without prejudice to re-nomination by any other member.

---

## Public-Comment Window

The public-comment window must be no shorter than seven (7) days, measured from candidacy-open time. The ZKAC charter may specify a longer minimum; it may not specify a shorter one.

During the comment window, any current principal-member may submit a written comment — supportive, opposed, or neutral — to the ceremony coordinator. Comments are appended to the candidacy ledger record in order of receipt. Comments are visible to all current principal-members and, subject to S169 (roster privacy), to the candidate.

The candidate may submit a single written response to the aggregate comment record. The response must be submitted no later than 24 hours before the vote opens.

The ceremony coordinator may not edit, redact, or sequence comments to advantage any outcome. Coordinator conflict-of-interest rules are governed by S166.

The comment window closes at a time stated in the Nomination Record. The vote opens immediately at window close if quorum conditions (see S160) are projectable; otherwise, the coordinator announces a hold of up to 72 hours to assess quorum.

---

## Member Vote

Voting is conducted per S160 (standard ZKAC member-vote procedure). Admission requires:

- A quorum of two-thirds (2/3) of current principal-members casting a ballot.
- A supermajority of three-quarters (3/4) of cast ballots in favor.

Votes are recorded as signed ballot tokens against the candidacy ledger record. Ballot tokens are anonymized per the ZKAC's privacy tier declared in the charter, subject to the floor requirements of S169. The vote window is 72 hours from opening.

If quorum is not reached, the candidacy lapses. A lapsed candidacy may be re-nominated by any eligible member no sooner than 14 days after lapse. The re-nomination opens a fresh procedure; prior comment records are not imported unless the re-nominating member explicitly appends them.

---

## Admission Record

Upon a successful vote, the coordinator creates an Admission Record. The schema:

```
AdmissionRecord {
  record_id:         UUID v4
  zkac_id:           ZKAC canonical identifier
  candidate_pid:     principal identity key
  candidate_eat_ref: { issuer, serial, expiry }
  alignment_score:   float [0.0, 1.0]
  alignment_criteria_hash: hex string
  nomination_ts:     ISO 8601 UTC
  comment_window_close_ts: ISO 8601 UTC
  vote_open_ts:      ISO 8601 UTC
  vote_close_ts:     ISO 8601 UTC
  ballots_cast:      integer
  ballots_for:       integer
  ballots_against:   integer
  admission_ts:      ISO 8601 UTC
  coordinator_pid:   principal identity key
  nominator_pid:     principal identity key
  charter_version:   semver string
  record_hash:       SHA-256 of canonical serialization
}
```

The Admission Record is appended to the ZKAC ledger and is immutable after creation. The record hash is reported to the Calm Witness ledger as a ZKAC-event attestation.

---

## Post-Admission Update

Within 24 hours of the admission timestamp, the ceremony coordinator must:

1. Add the new member's PID to the ZKAC's active member roster.
2. Set the member's initial role and permissions per the charter's default-role declaration (see S154).
3. Notify the new member of their admission, their role assignment, and their obligations under the Calm Pact as it applies within this ZKAC.
4. Update the member-roster privacy record per S169 to reflect the new member's declared privacy tier.
5. Submit the Admission Record hash to the Calm Witness ledger's ZKAC-events stream.

The new member becomes a principal-member with full voting rights at the moment the roster update is recorded, not at the moment of notification.

---

## Cross-References

| Reference | Subject |
|-----------|---------|
| E11 | Calm Witness enrollment protocol |
| S154 | ZKAC charter structure and instrument format |
| S159 | Charter-alignment function and scoring |
| S160 | Standard ZKAC member-vote procedure |
| S166 | Coordinator conflict-of-interest rules |
| S169 | Member-roster privacy tiers and disclosure rules |

---

Calm 2026-05-20
