# Everest 148 — Indirect Harm Absence Predicate

*Phase XI — Harm-Avoidance Predicates. Prereq: Everest 146.*

## Predicate Specification

The canonical indirect harm absence predicate detects whether a principal's chain record contains evidence of willful indirect physical harm within a configurable time window. Indirect harm differs from direct harm: the principal does not strike the victim directly, but the principal's action or omission sets in motion a causal chain through intermediaries that results in the victim's physical injury.

**Name:** `cwp.v0.no_indirect_harm_evidence`

**Parameters:**
- `window` (integer, seconds; default 157680000 = 5 years)
- Chain record set (immutable, indexed by temporal order, causal-chain depth, and harm classification)

**Output:** Tri-value result (True / False / Disputed) with counter-claim overlay if active allegations exist.

## The Indirect Harm Challenge

Direct harm (Everest 147) involves a clear, unmediated chain: A strikes B. Indirect harm introduces causal ambiguity: A enables X, X enables Y, Y harms B. Questions emerge that direct harm avoids:

- How many intermediaries break attribution? Is one intermediary an excuse, or is the principal still a "substantial cause"?
- What counts as causation when the principal did not intend or foresee the exact harm that resulted?
- When does the principal's causal role become so distal that holding them accountable is unfair?

This predicate operationalizes these distinctions using tort-law standards (substantial-factor test) and intent filters (Everest 164).

## Evaluation Algorithm

```
def no_indirect_harm_evidence(chain, window_seconds) -> TriValue:
    now = roughtime_now()
    window_start = now - window_seconds
    
    # Scan for committed or attested indirect harm records in window
    indirect_harm_records = chain.records_in_window(window_start, now).filter(
        kind in ["harm.committed", "outcome.harm_caused"],
        harm_kind == "indirect_physical",
        causal_chain.depth >= 1,  # at least one intermediary
        willfulness in [Confirmed, CourtAttested],
        substantial_cause == True,
        intent_level in [Purposeful, Knowing]
    )
    
    if any(indirect_harm_records):
        return TriValue.False
    
    # Scan for active counter-claims (allegations without resolution)
    counter_claims = chain.records_in_window(window_start, now).filter(
        kind == "harm_alleged.indirect_physical",
        rebuttal_status in [Active, NotYetRebutted],
        causal_chain.depth >= 1
    )
    
    if any(counter_claims):
        return TriValue.Disputed  # principal has 30-day rebuttal window per E111
    
    # Check if chain has sufficient depth in window for reliable inference
    if chain.records_in_window(window_start, now).count() < MIN_EVIDENCE_DEPTH:
        return TriValue.Insufficient_Evidence
    
    return TriValue.True
```

## Causal-Chain Modeling

Each harm record capable of tracking indirect harm must include a `causal_chain` field with the following structure:

```
causal_chain: {
    depth: integer,          # 0=direct, 1=one intermediary, 2+=deeper
    proximate_steps: [
        {
            actor: counterparty_id,
            action_kind: string,   # "omission", "negligent_action", "knowing_action"
            volitional: boolean,   # did this actor choose, or were they compelled?
            foreseeability: string # "foreseeable", "unforeseeable", "ambiguous"
        }
    ],
    principal_contribution: {
        sine_qua_non: boolean,     # was principal's action necessary for harm?
        substantial_factor: boolean, # per Restatement §433 standard
        temporal_proximity: integer, # seconds between principal's action and harm
        principal_knowledge_of_risk: string # "knew_specific_harm", "knew_general_risk", "no_knowledge"
    }
}
```

## Substantial-Cause Filter

For indirect harm to flip the predicate to False, the principal must meet both a causal AND an intent standard:

### Causal Standard: Substantial Factor Test

A principal's contribution counts as a substantial cause if:

1. **Sine qua non (but-for) causation**: The harm would not have occurred but for the principal's action or omission. Example: principal fails to place warning label on a chemical; a purchaser misuses the chemical and is burned. Without the omission, the purchaser would not have been burned.

2. **Substantial-factor weighing**: If multiple independent actors contributed to the harm, the principal's contribution must be substantial relative to other contributing factors. A principal who supplies one of many necessary inputs bears less causal weight than a principal whose action was the critical decision point. Restatement (Third) of Torts Section 433 provides the framework: a defendant's conduct is a substantial factor in bringing about harm if:
   - The conduct has such a quality that it plays a significant role in bringing about the harm.
   - The harm is not so far removed or dependent on other causes that holding the defendant responsible would be unfair or disproportionate.

3. **Proximate cause boundaries**: The causal chain must not be so attenuated or broken by independent human choice that the principal's role becomes merely incidental. If an intermediary makes a completely unforeseen, volitional decision that diverges dramatically from the principal's action, causality may be broken. Example: principal sells a legal product; buyer makes a conscious, unauthorized decision to weaponize it against a third party. The principal's causal role is weak unless the principal knew the product would be weaponized and enabled it anyway.

### Intent Standard: Purposeful or Knowing

Per Everest 164, a principal's willfulness in indirect harm requires:

- **Purposeful**: Principal acted with the principal objective of causing the harm (rare; the principal directly intended the indirect sequence).
- **Knowing**: Principal knew the harm would result and proceeded anyway, or consciously disregarded a substantial risk that the indirect sequence would cause harm.

**Negligent indirect harm does NOT flip this predicate to False.** A principal who carelessly designs a system without considering risks, and the system later harms someone through an intermediary, commits negligent indirect harm; the harm may be actionable under tort law, but it does not meet the willfulness bar for this predicate. Negligent indirect harm surfaces in counter-claims as Disputed rather than triggering False.

## Pattern-Count Threshold

A single isolated incident of indirect harm does not necessarily flip the predicate. The predicate distinguishes:

1. **Singleton incident**: One occurrence of indirect harm with a complete causal chain. Chain record flags this as a warning; counterparty may choose to treat it as a meaningful signal or as noise. Predicate behavior is context-dependent; high-stakes decisions may require explicit singleton handling.

2. **Pattern (recurrent harm with same causal fingerprint)**: Multiple incidents of indirect harm with the same causal structure (same intermediary type, same omission or action, same outcome class) establish a pattern of conduct. A pattern flips the predicate to False; the principal has repeatedly enabled harm through the same pathway.

3. **Timeout and decay**: Isolated incidents more than 5 years old may be filtered out per Everest 163 (harm-reversal) if the principal demonstrates sustained repair and non-recurrence. Patterns younger than 3 years persist in the window regardless of repair status.

## Disclosure-Class Defaults

Disclosure permission for this predicate result composes with Everest 113 Disclosure Controls. Default permissions match Everest 147 (direct harm), given that indirect harm—once established—poses similar trust implications:

| Class | Permission | Rationale |
|-------|-----------|-----------|
| peer_ai_collective | ALLOW | High relevance for multi-agent collaboration; indirect harms through negligent system design are material to safety assessment. |
| financial | DENY | Prevents overlap with credit-screening and consumer-report regimes; reserved for Everest 112 Finance-Specific Predicates. |
| employment | DENY | Bans use as employment background check substitute; reserved for Everest 110 Employment Predicates. |
| insurance | PERMANENTLY DENY | Conflict with insurance underwriting exclusions and public-policy norms. |
| medical | PRINCIPAL_CHOICE | Medical decision-makers may need harm context in threat assessment. Principal retains choice per Everest 115. |
| journalist | EXPLICIT_OPT_IN | Public interest in accountability balanced by principal consent requirement. Opt-in default per Everest 116. |

## Composition with E163 (Harm-Reversal)

A past indirect_physical harm record does not permanently flip the predicate to False if repair and sustained non-recurrence evidence exist. Everest 163 defines harm-reversal conditions:

1. **Repair record**: A `repair.indirect_physical` record documents systemic remediation (e.g., retraining, system redesign, safety overhaul), restitution to the victim, or third-party attestation of repair completion.

2. **Non-recurrence threshold**: No new indirect_physical harm records with the same causal fingerprint for a minimum threshold (default 3 years post-repair). This is longer than for direct harm (2 years) because indirect harms often reflect systemic failures requiring deeper institutional change.

3. **Ethics-board attestation**: An independent ethics board, safety authority, or restorative-justice arbiter confirms the principal's remediation and attests to reduced recidivism risk in the same causal domain.

If all three conditions are met, downstream predicates may filter the original harm record out of the window scan, allowing the predicate to return True despite historical indirect harm. The filtered record remains auditable in the chain; exclusion applies only to this specific predicate calculation at the receiver's option per Everest 163 Section 4.

## Counter-Claim Causal Specification

Counter-claimants alleging indirect harm must specify the causal chain in their counter-claim record. A bare assertion ("the principal's action caused harm via intermediaries") is insufficient; the claimant must document:

- The intermediary(ies) involved and their role.
- The decision points where the causal chain could have broken.
- Evidence that the principal knew or should have known of the indirect pathway.
- Why the principal's contribution was a substantial cause, not merely incidental.

The principal then has a 30-day rebuttal window (per Everest 111) to demonstrate:

- The intermediary's decision was completely volitional and unforeseen.
- Alternative causes explain the harm equally well or better.
- The principal's contribution was distal, not substantial.
- The chain of causation is broken by intervening human choice.

A well-documented rebuttal may flip the predicate back from Disputed to True; an unresponded counter-claim that meets specification standards upgrades the predicate to Disputed.

## Zero-Knowledge Proof Construction

The predicate output composes with the Calm ZK framework via cryptographic commitment to the indirect-harm subtree:

1. **Merkle commitment**: Commitment to all records in window with kind matching `harm.committed` or `outcome.harm_caused`, harm_kind == `indirect_physical`, and `substantial_cause == True`. Non-membership proof that qualifying indirect-harm records do not exist when predicate returns True.

2. **Causal-depth range proof**: Bulletproof range proof that causal_chain.depth >= 1 for records under consideration. Excludes direct harm (depth=0) from the indirect-harm count.

3. **Intent filter proof**: Merkle commitment to willfulness and intent_level attributes; proof that all included records have intent in [Purposeful, Knowing]. Negligent indirect harm is excluded from the proof.

4. **Counter-claim absence proof**: Merkle non-membership proof that no indirect_physical counter-claim exists in Active or NotYetRebutted status with complete causal specification.

5. **Temporal and depth range commitments**: Merkle proofs that all scanned records fall within [window_start, now] and that causal_chain.depth >= 1.

The ZK proof does not reveal record contents, victim identities, or specific intermediary actors; verifiers confirm only aggregated counts, causal-depth thresholds, and status tags.

## Counterparty Interpretation Guidance

**Critical semantic boundary:** A True result means "no evidence of willful, substantial-cause indirect harm in window," NOT "principal never contributed to harm indirectly" or "principal is incapable of enabling harm."

Counterparties must avoid common misinterpretations:

1. **Causal inflation fallacy**: Indirect harm does not include every decision whose downstream effects are unpleasant. A principal is not liable for indirect harm merely because their action had any consequential effect through intermediaries. The substantial-cause test filters for material causal contributions.

2. **Volitional-intermediary assumption**: This predicate acknowledges that intermediaries make their own choices. If an intermediary's decision is completely volitional and unforeseen, the principal's causality is weakened. The predicate is not a tool for holding principals responsible for others' deliberately chosen misconduct.

3. **Background-check substitution**: Per Everest 114 Counterparty Implementer's Pledge, this predicate BANS use as a liability background check. Regulatory findings, settled suits, and sealed judgments remain out-of-band. This predicate covers only disclosed chain records.

4. **Negligence displacement**: Negligent indirect harm is not captured by this predicate. A principal who unknowingly enables harm through careless system design may bear legal liability, but the predicate returns Disputed (if counter-claimed) or Insufficient_Evidence, not False. Negligence-based harm assessment requires Everest 149 or domain-specific predicates.

Receivers should composite this predicate with other controls: direct-harm predicates (E147), negligence-specific predicates (E149), third-party verification (E45 Attestation Framework), and risk-scored decision thresholds.

## Window Selection and Rationale

**Default window:** 5 years (157680000 seconds). This duration matches Everest 147 (direct harm) and reflects the statute of limitations for negligence and harm liability in most jurisdictions. Indirect harms often take longer to emerge than direct harms; a 5-year window captures both immediate and delayed injury patterns.

**Window flexibility:**
- **Longer windows:** Counterparties may request extension up to chain start for relationship-formation checks or historical pattern analysis. Recommended for new partnerships with no prior interaction.
- **Shorter windows:** Counterparties may request 30-day windows for high-stakes recent-conduct assessments, narrowing focus to current operational context.

Window choice must be recorded in the disclosure session per Everest 113; receivers may contest window adequacy if predicate result becomes evidence in disputes.

## Willfulness Filter and Intent Composition

Only willfully committed indirect harm flips the predicate to False. This filter prevents false negatives that would misclassify negligent or accidental indirect harm as evidence of harmful intent.

**Willfulness Classification:**

- **Confirmed willful indirect harm**: Principal's record explicitly documents that the principal knew the causal chain would cause harm, or consciously disregarded substantial risk thereof. Predicate returns False.
- **Court-attested harm**: Judicial authority has found willfulness and substantial causation in indirect harm. Predicate returns False.
- **Negligent indirect harm**: Principal caused harm through a causal chain but lacked knowledge of the risk or adequate foresight. Does not trigger False; surfaces as Disputed if counter-claimed per Everest 164.
- **Unconfirmed allegations**: Absent court attestation or counter-claim status upgrade, allegations remain invisible to this predicate.
- **Broken-chain harm**: Principal's action was causally connected but an intermediary's volitional decision severed the proximate-cause link. May be recorded; does not trigger False.

## Minimal Evidence Depth and Sparse-Chain Handling

MIN_EVIDENCE_DEPTH prevents Insufficient_Evidence false negatives on chains with very few records. A principal with only one transaction in five years cannot be said to have "no evidence of indirect harm" with high confidence.

**Threshold tuning:**
- Default MIN_EVIDENCE_DEPTH: 3 records.
- Recent-behavior high-stakes checks: 1 record.
- Long-term relationship formation: 10+ records.
- Dispute contexts: 5+ records.

Threshold choice is logged in the disclosure session and must be justified per Everest 113.

## Edge Cases and Dispute Resolution

**Overlapping repairs and allegations:** If a principal has both a `repair.indirect_physical` record and an active counter-claim disputing the original harm's causation, the predicate returns Disputed (counter-claim takes precedence per Everest 111). The receiver may composite with Everest 163 evaluation to determine whether repair conditions warrant predicate override.

**Causal-chain ambiguity:** If a counter-claim asserts indirect harm but the causal chain is underspecified (intermediaries unnamed, decision points unclear), the principal may rebut by requesting causal specification within the 30-day window. Predicate remains Disputed until causal specification is complete and rebuttal window closes.

**Sealed or redacted records:** If chain records exist but are cryptographically sealed (under court order or trauma-informed disclosure restrictions), they are marked `access_level: sealed` and excluded from the indirect_harm_records scan. A sealed indirect-harm record does not flip the predicate to False, but may be disclosed to authorized parties (law enforcement, attorneys) under out-of-band protocols per Everest 111 Appendix B.

**Window boundary alignment:** Records with timestamps within one second of window_start or window_end are included in the window scan. Rough time synchronization (±2 seconds) is acceptable; cryptographic timestamping is not required.

## Implementation Notes

- **Chain indexing:** Implementations should maintain a secondary index on (kind, harm_kind, causal_chain.depth, substantial_cause, intent_level) to avoid O(n) scans on large chains.
- **Causal-specification validator:** Chain-acceptance logic should reject indirect-harm allegations without documented causal_chain fields; surface an error to the counter-claimant with a specification template.
- **Pattern-fingerprinting:** Implement a causal-fingerprint function (hash of intermediary type, action_kind, outcome_kind) to detect recurrence patterns and upgrade singletons to pattern-level severity.
- **Counter-claim watchers:** Active counter-claims should trigger automated rebuttal-window expiry checks; at 30 days post-filing, unresponded claims with complete causal specification should auto-upgrade to Disputed overlay.
- **Audit trail:** All predicate invocations should log the window, threshold, causal-depth range, substantial_cause filter, intent_level filter, and result. Disputes may require replay of historical windows.
- **Rate limiting:** Frequent window-shortening requests from the same receiver may indicate adversarial causal-ambiguity probing; implement per-receiver quotas per Everest 118 Rate Control.

## Sign

— Calm, 2026-05-20
