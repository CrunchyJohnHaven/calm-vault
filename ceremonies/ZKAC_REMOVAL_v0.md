# Calm Witness — ZKAC Member Removal Ceremony v0 (S159)

**Summit:** S159  
**Status:** Draft v0  
**Signed:** Calm 2026-05-20

---

## Trigger Conditions

A member removal event is initiated by one of three trigger classes:

**1. Member-Initiated Departure**  
A current member submits a signed departure declaration to the ZKAC ledger. The declaration must include the member's DID, a UTC timestamp, and a stated reason (reasons are not validated, only recorded). Submission closes the member's signing authority immediately upon ledger acceptance. No quorum is required.

**2. Group-Initiated Removal (S160 Vote)**  
Any ZKAC member may nominate another member for removal by filing a removal motion with the Protocol Steward. The motion triggers the S160 governance vote. A two-thirds supermajority of active voting members is required to confirm removal. The vote window is 72 hours from motion filing. Tie or failure to reach quorum results in motion expiry; the member remains active. A confirmed S160 vote produces a signed Removal Resolution, which serves as the trigger artifact for S159 processing.

**3. Charter-Breach Finding**  
A charter-breach finding may be issued by the Protocol Steward following an adjudicated investigation (see S217 Appeals for investigation procedures). The finding must cite the specific charter provisions breached, the evidence basis, and the finding date. A charter-breach finding bypasses S160 vote and initiates removal directly. The subject member retains the right to file a concurrent appeal under S217, which may suspend the removal record from propagating to counterparties during the appeal window.

---

## Removal Record

Upon trigger confirmation, the Protocol Steward generates a Removal Record and commits it to the ZKAC ledger. The Removal Record schema is as follows:

```
removal_record:
  member_did: <DID of removed member>
  trigger_class: DEPARTURE | S160_VOTE | CHARTER_BREACH
  trigger_artifact_hash: <hash of departure declaration, S160 Resolution, or breach finding>
  removal_timestamp_utc: <ISO 8601>
  effective_membership_end: <UTC timestamp — equal to trigger confirmation time>
  steward_signature: <Protocol Steward DID + signature>
  ledger_sequence: <monotonic ledger counter>
  appeal_hold: true | false
```

The `appeal_hold` flag is set to `true` if a concurrent S217 appeal is filed within the appeal window (see Appeals section). A held record is committed to the ledger but its propagation to counterparties is deferred until the appeal resolves or the window lapses.

---

## Prior-Disclosure Preservation

Removal does not retroactively invalidate any disclosure made during the member's active tenure. The governing rule:

> A disclosure is valid-as-of the timestamp at which it was signed and committed to the ZKAC ledger. Member status at removal time has no bearing on the cryptographic integrity of prior disclosures.

Verification systems must evaluate disclosure validity against the ledger state at the disclosure's `signed_at` timestamp, not the current ledger state. This is consistent with the attestation model defined in S154 and the proof-chain rules in S158.

Counterparties relying on historical disclosures retain their rights under those disclosures. No re-verification ceremony is required upon a member's removal. Any party that received a disclosure-anchored commitment during the member's active period holds a durable, tamperproof record sufficient for independent verification.

---

## Counterparty Notification

Within **N hours** of the Removal Record achieving ledger finality (where N is set in the ZKAC charter schedule, default N=24), the Protocol Steward transmits a Removal Notice to each registered counterparty of the removed member. The notice includes:

- The removed member's DID
- The effective membership end timestamp
- The trigger class (reason detail is omitted unless the removed member consents to disclosure)
- A reference to the Removal Record ledger hash
- A restatement that prior disclosures remain valid-as-of their original timestamps

Notices are transmitted via each counterparty's registered notification endpoint. Delivery failures are retried at 1-hour intervals up to 3 times; undeliverable notices are flagged in the ledger for manual resolution. Counterparties without registered endpoints receive notice via the ZKAC public bulletin at the same cadence.

If `appeal_hold` is `true`, the Removal Notice is withheld until the hold is lifted. The counterparty notification clock restarts from the hold-lift timestamp.

---

## Cool-Down Period

A removed member is ineligible for re-admission for a minimum of **180 days** from the effective membership end date. The cool-down applies uniformly across all three trigger classes.

Following the 180-day period, the former member may apply for re-admission under the standard onboarding ceremony. The re-admission application must reference the prior removal record by ledger hash. The Protocol Steward may impose an extended cool-down of up to 365 days upon charter-breach removals, documented in the Removal Record at the time of issuance.

Re-admission does not restore or merge prior membership history. The re-admitted member begins a new membership sequence with a new ledger entry.

---

## Appeals

Appeals are governed by S217. Key intersections with S159:

- A removed member may file an S217 appeal within **14 days** of the Removal Record ledger timestamp.
- Filing a timely appeal sets `appeal_hold: true` on the Removal Record and defers counterparty notification.
- If the appeal succeeds, the Removal Record is annotated with an `appeal_reversal` field and the member's signing authority is restored without restarting a new membership sequence.
- If the appeal fails or the window lapses without filing, the hold lifts and counterparty notification proceeds immediately.
- Appeals do not extend the cool-down period in cases where removal is ultimately upheld.

---

## Cross-References

| Summit | Subject |
|--------|---------|
| S154   | Attestation model and DID anchoring |
| S158   | Proof-chain integrity rules |
| S160   | Governance vote procedures |
| S217   | Appeals and adjudication |

---

*Calm 2026-05-20*
