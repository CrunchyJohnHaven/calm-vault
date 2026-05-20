# Everest 121 — Values Disagreement Protocol

*Phase IX — Values Vocabulary. Prereq: Everest 120.*

## The Problem

In any assessment of a principal's values across a dimension—generosity, honesty, collaboration—three independent signals compete:

1. **Self-Report**: the principal's own authored statement of their values (from E108 values_self_report records)
2. **Action-Inferred**: values derived from the chain of action records (from E109 values_inferred_from_actions)
3. **Witness-Attested**: values signed and attested by third parties who have observed the principal (from E120 witness_attestations)

These three signals frequently disagree. A principal may report themselves as generous while chain records show minimal giving. Witnesses may attest collaborative behavior that contradicts the principal's self-assessment. Action records may reveal one pattern while observers describe another. The problem is not the disagreement—it is deciding whether a disagreement protocol should hide, reconcile, or surface these gaps honestly.

The naive approaches all fail:

- **Self wins**: Rewards self-deception and gaming. A principal who claims generosity while hoarding escapes accountability.
- **Witnesses win**: Enables collusion attacks and gossip dynamics. A coordinated group of adversarial witnesses can conspire to paint a principal unfairly.
- **Action wins**: Punishes principals whose revealed preferences are constrained by circumstance. Someone living in poverty may aspire to generosity but have no resources to give; their actions reflect their constraints, not their values.

A better protocol surfaces all three signals together and lets the counterparty decide what to make of the disagreement.

## The Decision

The protocol does not pick a winner. Instead, it **surfaces disagreement as diagnostic information** and empowers the counterparty's predicate logic to decide how to weigh the three signals based on their own context and risk tolerance.

For each values dimension, the operator presents three values:

- `self_report` ∈ [0, 1] (or null if principal has not authored a self-report)
- `inferred` ∈ [0, 1] (or null if insufficient action records exist)
- `witness_mean` ∈ [0, 1] (or null if no witness attestations exist) + `witness_count`

The three gaps become visible:

- **Self vs Inferred gap**: |self_report - inferred|
- **Self vs Witness gap**: |self_report - witness_mean|
- **Inferred vs Witness gap**: |inferred - witness_mean|

Each gap is a diagnostic signal. High gaps tell the counterparty that something interesting is happening; low gaps suggest alignment.

## Three Categories of Disagreement

### a. Self vs Inferred Gap (Stated vs Revealed Mismatch)

The principal claims a value; their actions suggest something else. Example: principal self-reports honesty at 0.8; chain records show three instances of providing incomplete information to partners, inferring honesty at 0.4.

This gap signals either self-deception (principal genuinely believes their self-report but actions contradict it) or strategic misrepresentation (principal knowingly overstates). The counterparty must decide which. A high self vs inferred gap warrants scrutiny.

### b. Self vs Witness Gap (Self vs Other Disagreement)

The principal reports one thing; third parties who have observed them attest something different. Example: principal self-reports collaboration at 0.7; three independent witnesses attest collaboration at 0.3, citing instances of unilateral decision-making.

This gap surfaces a perception mismatch. The principal may be unaware of how their behavior lands on others. Or the witnesses may be biased or coordinating. The counterparty weighs the witness_count and the stakes.

### c. Inferred vs Witness Gap (Action vs Perception Gap)

Chain records suggest one pattern; witnesses describe another. Example: action records show the principal spent significant time mediating disputes (inferred collaboration: 0.75); witnesses attest avoidance of collaboration (0.2).

This gap often emerges when actions are ambiguous or when witnesses interpret the same behavior differently. A high inferred vs witness gap suggests the action record may be misinterpreted by observers, or observers lack context.

## Predicate Variants

The counterparty can request alignment predicates tailored to their decision logic:

- `values_self_inferred_aligned_within(dim, tau)` — Returns True if |self_report - inferred| < tau. Useful for counterparties who trust the principal's self-awareness but worry about self-deception.

- `values_self_witness_aligned_within(dim, tau)` — Returns True if |self_report - witness_mean| < tau. Useful for counterparties who prioritize how others perceive the principal.

- `values_witnesses_show_consistency(dim, sigma_max)` — Returns True if the standard deviation across witness attestations < sigma_max. Useful for counterparties who worry about witness collusion or bias.

- `values_all_three_aligned(dim, tau)` — Returns True if all three pairwise gaps are within tau. Useful for counterparties who demand high confidence across all signals.

The counterparty's predicate is not baked into the protocol; the protocol merely surfaces the three signals and offers common predicates as templates. Domain-specific counterparties can write custom predicates.

## Why Honesty Over Reconciliation

Three reasons the protocol must surface disagreement rather than reconcile it:

**First, reconciliation hides the diagnostics the principal needs.** If the protocol were designed to pick a single "true" value (say, the witness mean), the principal loses visibility into their own blind spots. A self vs witness gap is priceless information: it tells the principal that others perceive them differently than they perceive themselves. Hiding that gap prevents growth.

**Second, picking a winner incentivizes gaming.** If self wins, principals will simply lie. If witnesses win, adversaries will hire false witnesses. If action wins, principals will perform for the record while behaving differently in private. Honest surfacing removes the incentive to game: the principal cannot fool the system because all signals are visible.

**Third, structural constraints break the "action wins" frame.** A person living in poverty may aspire to generosity but lack resources to give. Their action record (minimal donations) reflects their circumstance, not their values. A woman in a male-dominated organization may aspire to confidence but face structural barriers that make her actions appear hesitant. Surfaces disagreement preserves nuance; reconciliation erases it.

Honest disagreement surfacing respects the principal's agency to interpret their own gap and commit to change.

## The Data Structure

For each values dimension, the canonical record format includes:

```
{
  "dimension": "generosity",
  "self_report": 0.8,
  "self_report_authored_at": "2026-05-10T...",
  "self_report_confidence": "high",
  "inferred": 0.4,
  "inferred_action_count": 12,
  "inferred_window_days": 90,
  "witness_mean": 0.5,
  "witness_count": 3,
  "witness_stddev": 0.15,
  "witness_recent_authored_at": "2026-05-15T...",
  "gaps": {
    "self_inferred": 0.4,
    "self_witness": 0.3,
    "inferred_witness": 0.1
  }
}
```

This structure makes all three signals and all three gaps explicit and queryable.

## Edge Cases

### Witness Disagreement Among Themselves

When witness_count > 1 and witness_stddev is high, the protocol surfaces the witness disagreement itself. Example: three witnesses attest generosity at 0.9, 0.4, and 0.1 respectively. The witness_mean is 0.47, but the stddev is 0.38. The counterparty sees that witnesses disagree sharply; the mean alone would hide this conflict.

### Counter-Claim Active

If a counter-claim is active (E111 values_counter_claim), the predicate returns a "disputed" overlay. The three signals remain visible, but are marked as contested. The counterparty knows the principal's counterparty is actively challenging the gap.

### Recently Reversed Values

If the principal has filed a values_reversal record (E112 values_reversal), indicating they have changed their values or beliefs, the predicate uses only the post-reversal window. The old self-reports, inferred values, and witness attestations are archived but not used to compute current gaps.

## Composition with Disclosure Semantics

The principal pre-authorizes which disagreement-surfacing predicates to enable per counterparty class (E113 privacy_classes). The disclosure topology is:

- **Default mode**: Counterparties see only the alignment bits. They learn `values_self_inferred_aligned_within(dim, 0.2)` is True or False, but not the raw three-signal tuple.

- **Transparency mode**: The principal can opt to disclose the full three-signal tuple to high-trust counterparties or for diagnostic transparency. Useful when the principal is actively working on a gap and wants visibility from partners.

- **Read-only mode**: The principal can authorize witnesses and third parties to attest values, but can restrict which counterparties see witness attestations.

This composition allows the principal to share diagnostics selectively while protecting against wholesale reputational exposure.

## Anti-Abuse

A counterparty discovering a self vs inferred gap should not be able to use it as grounds for discrimination (per E114 scope_statement). Gaps are diagnostic for the principal; they are not adjudicatory for the counterparty.

This is enforced via governance predicate: `values_gaps_are_not_adjudicatory(counterparty_class)`. Any counterparty who uses a discovered gap as grounds for exclusion or retaliation triggers an audit and potential remediation.

The principle is: **Honesty about disagreement is not grounds for punishment. It is grounds for learning.**

## The "I Am Still Working on This" Record

The principal can append a `kind: "values_work_in_progress"` record that explicitly acknowledges a gap and commits to work. Example:

```
{
  "kind": "values_work_in_progress",
  "dimension": "generosity",
  "gap_acknowledged": "self_inferred",
  "commitment": "I am increasing my charitable giving by 5% annually and tracking impact via donation records.",
  "accountability_partner": "witness_id_X",
  "next_review_date": "2026-11-20"
}
```

Predicates can surface this commitment to counterparties. This is the "humility primitive"—the principal is allowed to be imperfect and growing. Surfacing the work-in-progress record signals that the principal has noticed the gap and is taking action.

## Governance and Composition

The values disagreement protocol composes with:

- **E108 Values Self-Report**: Principal-authored claims about their own values.
- **E109 Values Inferred from Actions**: Automated derivation of values from chain records.
- **E120 Witness Attestations**: Third-party signed observations.
- **E111 Values Counter-Claim**: Disputed values records that overlay "contested" status.
- **E112 Values Reversal**: Records indicating the principal has changed their values.
- **E113 Privacy Classes**: Authorization rules for which counterparties see which predicates.
- **E114 Scope Statement**: Governance rules preventing discrimination based on values gaps.

The protocol is not a values truth machine. It is a disagreement-surfacing machine that preserves all signals and lets principals and counterparties decide what to do with them.

## Sign

— Calm, 2026-05-20
