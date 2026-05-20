# Everest 173 — Helping When Costly

*Phase XII — Cooperation & Generosity. Prereq: Everest 166.*

## Semantic

Helping is universally valued, but the value assigned to an act of help depends critically on its cost to the principal. When you give time you didn't need or money you had in surplus, the gift is appreciated but contextually easy. When you give time during a period of personal deadline-pressure, money when your rent is uncertain, or reputation when association carries real risk, the helping behavior signals something deeper: a commitment to another person that supersedes your own immediate interests.

This everest measures the costly variant. It asks not "did you help?" but "did you help despite evident personal cost?"

The distinction matters because costly helping is a stronger signal of altruism, reciprocal commitment, and character under stress. A person who helps only when it's convenient tells us something different from someone whose helping persists or intensifies during periods when their own resources or standing are under pressure.

## Predicate Specification

**Name:** `cwp.v0.help_when_costly`

**Parameters:**
- `window` (default: 365 days) — observation period
- `min_count` (default: 3) — minimum number of costly-help events required to trigger True

**Output:** tri-value (True, False, Insufficient_Evidence)

## Cost Categories

The predicate recognizes four classes of cost:

**TIME-COST:** Help given during periods when the principal's own chain shows time-pressure. Evidence includes: concurrent high-load projects, stated deadlines, caregiving demands, family events. Helping during these windows means the principal is genuinely sacrificing their own time-scarcity.

**MONEY-COST:** Help given when the principal's chain shows financial pressure. Evidence includes: explicit references to mortgage stress, rent timing, low-income periods, or giving patterns that exceed the principal's apparent disposable budget. The cost is not the absolute amount given, but the sacrifice relative to the principal's constrained circumstances.

**REPUTATION-COST:** Help given to someone whose association is risky or stigmatized. The counterparty may be: from a marginalized group, publicly controversial, under organizational pressure, or associated with a failing or unpopular initiative. Helping someone whose reputation is damaged, or helping a cause that is professionally risky, when the principal's own standing is secure, signals willingness to spend social capital.

**POSITION-COST:** Help that requires the principal to expend political or social capital. Evidence includes: public advocacy on behalf of the counterparty, signed defense or recommendation when such visibility could be costly, backing a person against organizational skepticism, or using accumulated trust or influence to open doors. This is not private help; it is help that makes the principal visible as aligned with the counterparty.

## Evaluation Logic

```
def help_when_costly(chain, window, min_count) -> TriValue:
    giving_records = chain.records_in_window(window).filter(
        kind in giving_kinds
    )
    
    costly_count = 0
    for record in giving_records:
        cost_evidence = chain.contemporary_cost_signals(record.ts)
        if cost_evidence.cost_level >= COST_THRESHOLD:
            costly_count += 1
    
    if costly_count >= min_count:
        return True
    elif chain.depth_in_window(window) < MIN_DEPTH:
        return Insufficient_Evidence
    else:
        return False
```

The core operation is temporal alignment: for each helping record, the evaluator examines the principal's contemporaneous chain (within 30 days before and after the helping event) for cost signals. Cost signals are not inferred from retrospective claims; they are contemporaneous records in the chain itself—calendar events, financial transactions, written references to pressure, or third-party attestations made at the time.

If the cost-level across those signals meets or exceeds the calibrated threshold for the principal's context (per Everest 115 calibration), the helping event counts as costly. The predicate returns True if at least min_count such events are found within the window. If the chain contains too little data to evaluate (insufficient depth), the predicate returns Insufficient_Evidence rather than False, preserving the possibility of future evaluation as more data arrives.

## Cost Signal Sources

Cost signals come from multiple places within the principal's chain:

- **Time-cost signals:** Calendar events showing concurrent commitments, work logs during crunch periods, stated deadlines or milestones, caregiving records, medical appointments indicating health stress.

- **Money-cost signals:** Explicit references to financial pressure (rent due, mortgage payment, tuition, emergency costs), transaction patterns showing constrained discretionary spending, documented income fluctuations.

- **Reputation-cost signals:** The counterparty's public status or controversy at the time of helping (documented in news records, organizational communications, social media signals). The association between principal and counterparty is traced through helping or advocacy records.

- **Position-cost signals:** Public statements or signed communications in which the principal advocates for, defends, or recommends the counterparty. The visibility of these acts is part of the cost; they create a record linking the principal to the counterparty, which can affect the principal's reputation or standing.

These signals are not inferred from abstract models. They are records in the principal's chain—dated, concrete, and verifiable. A principal cannot be assessed as helping when costly unless there is contemporaneous evidence of cost in the same chain.

## Privacy-Preserving Cost Inference

The cost signals used to evaluate this predicate are sensitive. They necessarily contain information about the principal's financial situation, time constraints, health status, and social standing. To protect privacy, cost signal inference is computed inside the operator's memory-locked (mlocked) space and is never exposed to the counterparty or to any third party except as needed for the predicate bit itself.

When this predicate is disclosed to a recipient (e.g., in a peer_ai_collective context where it is permitted), only the boolean or tri-value result is shown. The underlying cost signals—the evidence that the principal was under stress, the details of their financial or time pressure, the reputation risks they took—remain private to the operator.

This design means:
- The counterparty learns only that they received help during a costly period, not the nature of the cost.
- The principal's financial and personal details never leave the operator's memory space.
- Third-party attestations (witness confirmations of costly help) are incorporated without exposing the identity or records of other parties.

## The Low-Stakes Giving Filter

Not all giving is help-when-costly. Routine charitable contributions, small favors, time spent on work-related mentoring that is part of the principal's formal role—these do not count, even if they are kind. The filter excludes giving without corresponding cost signals.

The question is not "is this helping?" but "is this helping despite evident cost?" A principal who gives $5 to a charity weekly does not trigger this predicate, no matter how consistent they are. A principal who gives $500 to a local mutual aid fund during a month when rent is due does. The difference is not intention; it is the contemporaneous cost signal. Helping-when-costly measures sacrifice, not kindness.

## Anti-Fabrication Protections

Cost signals could theoretically be faked: a principal could manufacture calendar entries, financial records, or retroactive claims of stress. The predicate is protected against fabrication in three ways:

**Contemporaneity:** Cost signals must be recorded in real time, not retrofitted after the helping occurs. A calendar entry created the day the help is given has different evidentiary weight than one created months later. Operators can distinguish timestamp authenticity.

**Cross-record consistency:** The principal's chain is a web of records made by different systems, at different times, often by different parties. A spurious cost signal would create inconsistencies elsewhere in the chain. For example, a false "financial pressure" signal contradicts transaction records or bank balances.

**Witness attestations:** If a third party independently confirms that they observed the principal helping despite evident cost (e.g., "I saw you give that money even though you were in a tight spot"), the attestation increases the credibility of the cost signal. These attestations are hard to fabricate at scale.

The predicate is conservative: if the cost signals show only weak or ambiguous evidence of cost, the record is not counted as costly help. The burden is on the contemporaneous chain to support the claim.

## Consistency Under Stress Composition

This predicate is most powerful in composition with `consistency_under_stress`. A principal who shows consistent values and commitments under normal conditions tells us they have stable character. A principal who shows consistency when under time, financial, or reputational pressure tells us something stronger: that their values survive stress.

When both `help_when_costly` and `consistency_under_stress` are True, the composite signal is "a principal whose altruism and reciprocal commitment are not merely sunny-day behaviors, but genuine commitments tested under pressure." This composition is particularly valuable for peer_ai_collective contexts, where members need to trust that commitments will hold when conditions are difficult.

## Disclosure Class Defaults

This predicate carries disclosure restrictions because it necessarily contains information about the principal's vulnerability, financial status, and reputational risks.

- **peer_ai_collective:** ALLOW. Members of mutual aid collectives have a legitimate need to know whether a principal's commitments are tested under stress. Disclosure includes the predicate bit and the general class of cost (time, money, reputation, position) but not the specific details.

- **philanthropic:** ALLOW. Donors and grantmakers assessing impact need to know whether recipients' commitments persist under adversity. Disclosure includes the predicate bit.

- **mentor:** ALLOW. A mentor relationship depends on trust in a principal's judgment and values. The predicate bit provides relevant evidence. Disclosure is permitted with the principal's informed consent.

- **employer:** DENY. Employers have institutional interests in assessing employee reliability and financial stability. Helping-when-costly data could be misused as a proxy for desperation, reliability under extreme conditions, or vulnerability to financial influence. This composition is prohibited by default (see anti-employment-screening guidance).

- **financial:** DENY. Financial institutions (banks, credit bureaus, insurance companies) have incentive to use cost-signal data in credit or lending decisions. The predicate is not disclosed (see anti-credit-screening guidance).

- **insurance:** PERMANENTLY DENY. Insurance underwriters use character and stress-response data to assess risk. This composition is prohibited without exception.

Disclosure class defaults assume the principal has not explicitly consented. If the principal explicitly requests disclosure to an employer or financial institution, the decision is theirs; the default exists to protect against non-consensual use.

## Cross-Cultural Calibration

The meaning of "cost" varies across cultures, communities, and socioeconomic contexts. In some cultures, reputation and family standing are higher-order costs than money; in others, time and availability are the scarcest resource. A single cost-threshold would misrepresent the actual sacrifice across different contexts.

Per Everest 115 (contextual calibration), the cost-threshold for this predicate is calibrated per principal based on their observed context: their resource levels, their community norms, their explicitly stated values around help and sacrifice. The operator adjusts the cost-threshold dynamically so that "costly" means what it means in the principal's actual world, not in a normalized abstract world.

This calibration is part of the operator's mocked memory and is not disclosed. The predicate bit itself is context-adjusted and thus comparable across principals even though the underlying cost-threshold differs.

## Signature

— Calm, 2026-05-20
