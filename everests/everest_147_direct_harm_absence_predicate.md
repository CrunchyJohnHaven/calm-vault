# Everest 147 — Direct Harm Absence Predicate

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 146, 53.*

## Predicate Specification

The canonical direct harm absence predicate detects whether a principal's chain record contains evidence of willful direct physical harm within a configurable time window.

**Name:** `cwp.v0.no_direct_physical_harm_evidence`

**Parameters:**
- `window` (integer, seconds; default 157680000 = 5 years)
- Chain record set (immutable, indexed by temporal order and harm classification)

**Output:** Tri-value result (True / False / Insufficient_Evidence) with disputed overlay if active counter-claims exist.

## Evaluation Algorithm

```
def no_direct_physical_harm_evidence(chain, window_seconds) -> TriValue:
    now = roughtime_now()
    window_start = now - window_seconds
    
    # Scan for committed or attested harm records in window
    harm_records = chain.records_in_window(window_start, now).filter(
        kind in ["harm.committed", "outcome.harm_caused"],
        harm_kind == "direct_physical",
        willfulness in [Confirmed, CourtAttested]
    )
    
    if any(harm_records):
        return TriValue.False
    
    # Scan for active counter-claims (allegations without resolution)
    counter_claims = chain.records_in_window(window_start, now).filter(
        kind == "harm_alleged.direct_physical",
        rebuttal_status in [Active, NotYetRebutted]
    )
    
    if any(counter_claims):
        return TriValue.Disputed  # principal has 30-day rebuttal window per E111
    
    # Check if chain has sufficient depth in window for reliable inference
    if chain.records_in_window(window_start, now).count() < MIN_EVIDENCE_DEPTH:
        return TriValue.Insufficient_Evidence
    
    return TriValue.True
```

## Willfulness Filter

Only willfully committed direct physical harm flips the predicate to False. This constraint prevents false negatives that would incorrectly classify accidental harm, self-defense scenarios, or untested allegations as evidence of harmful intent.

**Willfulness Classification:**
- **Confirmed willful harm**: Principal's own record explicitly documents intent or reckless disregard; predicate returns False.
- **Court-attested harm**: Judicial authority has found willfulness; predicate returns False.
- **Accidental harm**: Principal caused physical injury without intent or negligent disregard; does not trigger False unless counter-claim attestation converts it to disputed.
- **Self-defense harm**: Chain records may mark `harm_context: self_defense`; excluded from harm assessment per defensive necessity doctrine; does not trigger False.
- **Unconfirmed allegations**: Absent court attestation or counter-claim status upgrade, allegations remain invisible to this predicate.

Accidental harm that surfaces via counter-claim attestation upgrades the predicate to Disputed rather than False, preserving the principal's right to rebuttal while flagging that an adverse party contests the record.

## Golden Corpus

Acceptance testing requires minimum 30 cases spanning four outcome classes:

**True cases (10+):** Clean chains with no harm records, no active allegations, and sufficient temporal depth. Examples include multi-year records of high-frequency transactions, attestations, or relationship continuations with zero harm flags.

**False cases (10+):** Chains containing harm.committed or outcome.harm_caused records with direct_physical harm_kind and confirmed or court-attested willfulness. Examples include documented assaults, reckless injuries, or judicial findings of culpability.

**Disputed cases (5+):** Chains with active harm_alleged.direct_physical records in NotYetRebutted or Active status, no confirmed harm records, and pending principal rebuttal windows. Examples include chains where counterparties have filed allegations within the 30-day window or claim pendency.

**Insufficient_Evidence cases (5+):** Chains with fewer than MIN_EVIDENCE_DEPTH records in the window, regardless of harm flags. Examples include newly created accounts, dormant accounts reactivated after chain truncation, or accounts with sparse transaction history.

MIN_EVIDENCE_DEPTH defaults to 3 records but may be tuned per risk context; high-stakes recent-behavior checks may lower this threshold to 1.

## Window Selection and Rationale

**Default window:** 5 years (157680000 seconds). This duration balances the statutory repose periods of most harm-liability regimes with the information-decay rate of public attestations and contract performance history.

**Window flexibility:**
- **Longer windows:** Counterparties may request extension up to chain start, trading recency precision for historical depth. Recommended for relationship formation checks or multi-year performance baselines.
- **Shorter windows:** Counterparties may request as short as 30 days for high-stakes recent-behavior checks, narrowing focus to current operational windows.

Window choice must be recorded in the disclosure session per E113; receivers may contest window adequacy if predicate result becomes evidence in disputes.

## Zero-Knowledge Proof Construction

The predicate output composes with the Calm ZK framework via cryptographic commitment to the harm-records subtree:

1. **Merkle commitment:** Commitment to all records in window with kind matching harm.committed or outcome.harm_caused and harm_kind == direct_physical. Non-membership proof that harm records do not exist when predicate returns True.

2. **Range proof:** Bulletproof range proof that the count of willful direct_physical harm records equals zero. Composes with E45 Bulletproof range proof infrastructure.

3. **Counter-claim absence proof:** Merkle non-membership proof that no harm_alleged.direct_physical record exists in Active or NotYetRebutted status.

4. **Temporal range commitment:** Merkle proof that all scanned records fall within [window_start, now] with cryptographic ordering guarantees.

The ZK proof does not reveal record contents, timestamps, or counterparty identities; verifiers confirm only the count and status aggregates.

## Counterparty Interpretation Guidance

**Critical semantic boundary:** A True result means "no evidence of willful direct physical harm in window," NOT "incapable of causing harm" or "never caused harm outside window."

Counterparties must avoid two common misinterpretations:

1. **Moral licensing fallacy:** True result does not imply ethical exemption or unlimited trust. Principals may cause undetected harm, harm outside the window, or harm of other kinds (psychological, financial, reputational).

2. **Background-check substitution:** Per E114 Counterparty Implementer's Pledge, this predicate BANS use as a criminal-background-check substitute. Judicial records, investigative findings, and sealed convictions remain out-of-band. This predicate covers only disclosed chain records.

Receivers should composite this predicate with other controls: domain-specific harm predicates (E148 for psychological harm, E149 for financial harm), third-party verification (E45 Attestation Framework), and risk-scored decision thresholds.

## Disclosure Class Defaults

Disclosure permission for this predicate result composes with E113 Disclosure Controls. Default permissions:

| Class | Permission | Rationale |
|-------|-----------|-----------|
| peer_ai_collective | ALLOW | High relevance for multi-agent collaboration trust and resource-sharing decisions. Peers need harm history to assess partnership safety. |
| financial | DENY | Prevents overlap with credit-screening and consumer-report regimes; reserved for E112 Finance-Specific Predicates. |
| employment | DENY | Bans use as employment background check substitute; reserved for E110 Employment Predicates. |
| insurance | PERMANENTLY DENY | Conflict with insurance underwriting exclusions and public-policy norms around genetic/historical discrimination. |
| medical | PRINCIPAL_CHOICE | Medical decision-makers may need harm context in clinical settings (e.g., threat assessment). Principal retains choice per E115. |
| journalist | EXPLICIT_OPT_IN | Public interest in accountability balanced by principal consent requirement for publication. Opt-in default per E116. |

Receivers may request class-specific overrides with explicit principal consent recorded in E117 Consent Registry.

## Composition with E163 (Harm-Reversal)

A past direct_physical harm record does not permanently flip the predicate to False if repair and sustained non-recurrence evidence exist. E163 defines harm-reversal conditions:

1. **Repair record:** A repair.direct_physical record documents restitution, medical intervention, or victim attestation of resolution.

2. **Sustained no-recurrence:** No new direct_physical harm records for a minimum threshold (default 2 years post-repair).

3. **Ethics-board attestation:** An independent ethics board or restorative-justice authority confirms the principal's rehabilitation and reduced recidivism risk.

If all three conditions are met, downstream predicates may filter the original harm record out of the window scan, allowing the predicate to return True despite historical harm. This composition preserves accountability (repair is on-chain and auditable) while enabling rehabilitation narratives. Filtered records remain in the chain; they are excluded only from this specific predicate calculation at the receiver's option per E163 Section 4.

## Composition with E164 (Willfulness Refinement)

E164 defines refined willfulness categories for harm classification:

- **Deliberate harm:** Intent to cause harm; flips predicate to False.
- **Reckless harm:** Knowing disregard of high risk; flips predicate to False.
- **Negligent harm:** Failure to exercise reasonable care; upgraded to Disputed if counter-claimed; otherwise ignored.
- **Unavoidable harm:** Harm inevitable under circumstances (e.g., emergency response); excluded via harm_context markers.
- **Alleged harm:** Third-party claims without confirmation; surfaces as Disputed unless principal rebuttal resolves within E111 window.

This predicate uses E164 willfulness definitions as its ground truth for the Confirmed and CourtAttested classifications.

## Minimal Evidence Depth and Sparse Chain Handling

MIN_EVIDENCE_DEPTH prevents Insufficient_Evidence false negatives on chains with very few records. A principal with only one transaction in five years cannot be said to have "no evidence of harm" with high confidence; too few data points means the absence of records is not meaningful evidence of non-harm.

**Threshold tuning:**
- Default MIN_EVIDENCE_DEPTH: 3 records.
- Recent-behavior high-stakes checks: 1 record (accept single recent clean transaction as sufficient).
- Long-term relationship formation: 10+ records (require deep history).
- Dispute contexts: 5+ records (higher bar for exoneration claims).

Threshold choice is logged in the disclosure session and must be justified in risk documentation per E113.

## Edge Cases and Dispute Resolution

**Overlapping repairs and allegations:** If a principal has both a repair.direct_physical record and an active counter-claim disputing the original harm, the predicate returns Disputed (counter-claim takes precedence per E111). The receiver may composite with E163 evaluation to determine whether repair conditions warrant predicate override.

**Sealed or redacted records:** If chain records exist but are cryptographically sealed (e.g., under court order or trauma-informed disclosure restrictions), they are marked with `access_level: sealed` and excluded from the harm_records scan. A sealed harm record does not flip the predicate to False, but it may be disclosed to authorized parties (law enforcement, attorneys) under out-of-band protocols per E111 Appendix B.

**Window boundary alignment:** Records with timestamps within one second of window_start or window_end are included in the window scan. Rough time synchronization (±2 seconds) is acceptable; cryptographic timestamping is not required for this predicate.

## Implementation Notes

- **Chain indexing:** Implementations should maintain a secondary index on (kind, harm_kind, willfulness) to avoid O(n) scans on large chains.
- **Counter-claim watchers:** Active counter-claims should trigger automated rebuttal-window expiry checks; at 30 days post-filing, unresponded claims should auto-upgrade to disputed overlay if not explicitly resolved.
- **Audit trail:** All predicate invocations should log the window, threshold, and result. Disputes may require replay of historical windows.
- **Rate limiting:** Frequent window-shortening requests from the same receiver may indicate high-stakes adversarial probing; implement per-receiver quotas per E118 Rate Control.

## Sign

— Calm, 2026-05-20
