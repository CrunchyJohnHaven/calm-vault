# Calm Witness — ZKAC Bootstrap Kit Spec v0 (S173)

A ZKAC (Zero-Knowledge Autonomous Collective) can be stood up in under one day using this kit. All primitives are derived; new collectives do not derive them again. Fork, fill placeholders, run ceremonies in order, seed the chain. Done.

---

## Kit Manifest

| File | Purpose |
|---|---|
| `charter.md` | Filled charter template; canonical governing document |
| `roles.md` | Role definitions; copy verbatim or annotate |
| `ceremonies/admission.md` | Script for onboarding new members |
| `ceremonies/removal.md` | Script for member removal |
| `ceremonies/vote.md` | Script for any binding collective decision |
| `ceremonies/amendment.md` | Script for charter changes |
| `chain/genesis.jsonl` | Sample chain; seed entries for initial admissions |
| `obligations_sample.md` | Sample counterparty obligations contract |
| `checklist.md` | Getting-started checklist; mark off in order |

All files are plain text or JSONL. No proprietary formats. Hash each file at finalization; record hashes in `chain/genesis.jsonl`.

---

## Charter Template

```
# [COLLECTIVE_NAME] Charter v[VERSION]

## Purpose
[STATE_PURPOSE_IN_ONE_SENTENCE]

## Canonical Directive
[CANONICAL_DIRECTIVE_SENTENCE — the single sentence all agents and operators must satisfy]

## Decision Rule
[e.g., Supermajority (2/3) of principal-members; unanimous for dissolution]

## Roles
See roles.md (incorporated by reference).

## Dissolution Procedure
[DISSOLUTION_PROCEDURE — who initiates, required vote threshold, asset disposition, chain archival requirement]

## Amendments
Amendments require [AMENDMENT_THRESHOLD] and must run the charter-amendment ceremony (ceremonies/amendment.md).

## Effective Date
[ISO_DATE]

## Founders
[LIST_FOUNDER_IDS]
```

Placeholders in brackets. Canonical Directive is load-bearing: every agent action is evaluated against it. Keep it under 30 words. Cross-reference: S154 (canonical directive construction), S155 (dissolution integrity).

---

## Role Definitions

**Founder** — Initiates the collective; signs genesis entries; holds no permanent veto after admission ceremony closes unless also elected principal-member. Responsibility: ensure charter is coherent before seeding chain.

**Principal-Member** — Voting member; identity attested by at least one witness at admission. Votes are logged on-chain. Quorum and threshold defined in charter.

**Agent-Operator** — Runs one or more autonomous agents on behalf of the collective. Must bind each agent to the Canonical Directive at instantiation. Accountable for agent outputs; cannot delegate accountability.

**Witness** — Attests identity claims and ceremony completion. Does not vote on substance. Signature required on admission and removal events. Cross-reference: S158 (witness attestation primitives), S163 (tamperproof attestation).

**Auditor** — Read-only access to chain; verifies ceremony compliance; issues audit reports as signed documents appended to chain. May flag but not veto. Cross-reference: S160 (auditor role boundary).

---

## Ceremonial Scripts

### Admission
1. Candidate submits identity claim and purpose statement.
2. Witness verifies claim out-of-band; signs attestation record.
3. Existing principal-members vote (threshold: simple majority unless charter specifies otherwise).
4. On pass: emit `ADMISSION` event to chain with candidate ID, witness ID, vote tally, timestamp.
5. Candidate acknowledged as principal-member effective at chain confirmation.

### Removal
1. Any principal-member files removal motion with stated cause.
2. Subject notified; 48-hour response window (or charter-specified period).
3. Principal-members vote (threshold: supermajority unless charter specifies otherwise).
4. Witness co-signs removal event.
5. Emit `REMOVAL` event to chain with subject ID, cause, vote tally, timestamp.

### Voting
1. Proposer emits `PROPOSAL` event with motion text and deadline.
2. Each principal-member emits signed `VOTE` event (yes/no/abstain) before deadline.
3. Tallier (any member) emits `TALLY` event at deadline close with outcome.
4. Outcome binding at tally confirmation.

### Charter Amendment
1. Run Voting ceremony on proposed amendment text.
2. On pass: witness co-signs amended charter file.
3. Emit `AMENDMENT` event with old charter hash, new charter hash, vote tally.
4. Distribute new charter file; old file archived immutably.

---

## Sample Chain

```jsonl
{"seq":1,"type":"GENESIS","collective":"[COLLECTIVE_NAME]","charter_hash":"[SHA256]","founders":["[FOUNDER_ID]"],"ts":"[ISO_DATETIME]","sig":"[FOUNDER_SIG]"}
{"seq":2,"type":"ADMISSION","member_id":"[MEMBER_1_ID]","witness_id":"[WITNESS_ID]","vote_tally":{"yes":1,"no":0,"abstain":0},"ts":"[ISO_DATETIME]","sig":"[WITNESS_SIG]"}
{"seq":3,"type":"ADMISSION","member_id":"[MEMBER_2_ID]","witness_id":"[WITNESS_ID]","vote_tally":{"yes":2,"no":0,"abstain":0},"ts":"[ISO_DATETIME]","sig":"[WITNESS_SIG]"}
{"seq":4,"type":"TALLY","proposal":"Adopt obligations_sample.md as counterparty template","outcome":"PASS","vote_tally":{"yes":2,"no":0,"abstain":0},"ts":"[ISO_DATETIME]","sig":"[TALLIER_SIG]"}
```

Each entry: sequential, signed, links to prior hash on production chains. Replace bracketed values. Seq 1 must precede any admission.

---

## Sample Obligations Contract

```
# Counterparty Obligations — [COLLECTIVE_NAME] / [COUNTERPARTY_NAME]

Effective: [ISO_DATE]
Governing charter: [CHARTER_HASH]

## Obligations of [COLLECTIVE_NAME]
1. Deliver [SERVICE_OR_OUTPUT] by [DEADLINE].
2. Maintain audit log accessible to [COUNTERPARTY_NAME] auditor.
3. Notify counterparty within 24 hours of any charter amendment.

## Obligations of [COUNTERPARTY_NAME]
1. Provide [RESOURCE_OR_INPUT] by [DEADLINE].
2. Accept delivery verified by collective witness signature.

## Dispute Resolution
Disputes escalate to collective vote under Voting ceremony. Counterparty may observe; does not vote.

## Termination
Either party may terminate with [NOTICE_PERIOD] written notice. Outstanding obligations survive termination.

Signed: [COLLECTIVE_FOUNDER_SIG] / [COUNTERPARTY_SIG]
```

---

## Getting-Started Checklist

- [ ] Fill `charter.md` — purpose, canonical directive, decision rule, dissolution procedure
- [ ] Assign at least one Founder, one Witness, one Auditor (may overlap with principal-members)
- [ ] Run Admission ceremony for each founding principal-member
- [ ] Seed `chain/genesis.jsonl` with GENESIS entry and initial ADMISSION entries
- [ ] Hash all kit files; record hashes in genesis or a `manifest.sha256` file
- [ ] Distribute charter to all members; confirm receipt on-chain (TALLY event)
- [ ] Execute at least one Voting ceremony (e.g., adopting obligations template) before engaging counterparties
- [ ] Auditor performs initial chain review; appends signed audit record
- [ ] Archive kit snapshot; onboarding complete

Target elapsed time: under 8 hours for a three-member collective with one counterparty.

---

## Cross-References

| Summit | Topic |
|---|---|
| S154 | Canonical directive construction and evaluation criteria |
| S155 | Dissolution integrity and chain archival requirements |
| S158 | Witness attestation primitives |
| S160 | Auditor role boundary and report format |
| S163 | Tamperproof user-state attestation (ZKBB-User Everest route) |

---

Calm 2026-05-20
