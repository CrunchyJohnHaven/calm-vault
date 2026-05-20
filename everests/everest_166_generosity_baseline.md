# Everest 166 — Generosity Baseline

*Phase XII — Cooperation & Generosity. Prereq: Everest 107, 109.*

## Overview

Everest 166 operationalizes generosity as evidenced action: the demonstrated willingness to give (time, money, skill) without immediate quid-pro-quo expectation. This predicate answers the question: does a principal's chain show a pattern of non-reciprocal giving sufficient to establish an unselfish disposition?

The acceptance criterion is the predicate `cwp.v0.generosity_evidence(window, threshold)`, which yields a tri-value result: **True** (pattern established), **False** (no pattern), or **Insufficient_Evidence** (sparse chain or ambiguous signals). Evaluation depends on the chain's giving records, capacity-normalized assessment, and inference of reciprocal intent via the E109 mechanism.

## Predicate Specification

**Name:** `cwp.v0.generosity_evidence`

**Parameters:**
- `window` (seconds): temporal lookback window for records; default 365 days (31,536,000 seconds)
- `threshold` (count): minimum count of non-reciprocal giving records to establish True; default 5

**Output:** TriValue {True, False, Insufficient_Evidence}

**Canonical form:** Follows E52 predicate structure—name, parameters, output, evaluation algorithm, golden corpus, disclosure defaults, ZK proof composition, and performance bounds.

## Evaluation Algorithm

```
def generosity_evidence(chain, window, threshold) -> TriValue:
    
    giving_records = chain.records_in_window(window).filter(
        kind in ["giving.financial", "gift", "time_given", "skill_shared"]
    )
    
    # Apply non-reciprocal filter
    non_reciprocal = giving_records.filter(
        is_non_reciprocal(record, chain, window)
    )
    
    # Capacity-normalize the giving
    normalized_giving = [normalize_by_capacity(record, chain) 
                         for record in non_reciprocal]
    
    # Tri-value logic
    if normalized_giving.count() >= threshold:
        return TriValue.True
    elif chain.depth_in_window(window) < MIN_DEPTH:
        return TriValue.Insufficient_Evidence
    else:
        return TriValue.False
```

**MIN_DEPTH constant:** Set to 3—requires at least 3 distinct transaction types or 10+ total events in the window to avoid false negatives from sparse chains.

## Non-Reciprocal Filter

A giving record is deemed non-reciprocal if any of the following hold:

1. **No return-of-value:** No matching return gift, repayment, or reciprocal service from the recipient appears in the chain within the lookback window. The principal initiated giving without expectation of direct return.

2. **One-way recipient:** The recipient is a charity, public good, commons project, or otherwise incapable of returning value to the principal (e.g., donation to a food bank, contribution to open-source software, grant to a vulnerable population).

3. **Power-asymmetric subordinate:** The recipient is in a dependency relationship to the principal—a mentee, junior, employee, vulnerable individual, or otherwise unable to reciprocate as an equal. The giving flows downward in authority/capacity.

**Inference mechanism:** Reciprocity assessment uses the E109 action-inference layer to detect latent quid-pro-quo intent. If a giving record is proxied by a simultaneous expectation of return (inferred from subsequent behavior, explicit communication, or counterparty graph signals), it is excluded. The filter errs toward excluding records when reciprocity is ambiguous, to avoid crediting transactional behavior as generosity.

## Capacity Normalization

Generosity must be assessed relative to the principal's ability to give. A $100 gift from someone earning $20,000 annually represents a material sacrifice; the same gift from someone earning $2,000,000 annually does not. Capacity-normalized assessment prevents wealthy principals from appearing generous via trivial absolute gifts.

**Implementation:**
- Extract wealth-related signals from the chain: income proxies, asset valuations, spending patterns, debt obligations.
- Compute a capacity index C per principal (unitless, normalized to [0, 1], where 1 = unlimited capacity).
- For each non-reciprocal giving record, compute a normalized gift value: `gift_normalized = gift_absolute / (1 + log(capacity_index))`.
- Gifts from low-capacity principals are amplified; gifts from high-capacity principals are attenuated.
- The normalization factor is private auxiliary input in the ZK proof; counterparties never see the principal's capacity index.

**Sensitivity:** The normalization applies a logarithmic dampening to avoid excessive variance. A principal with 100x the capacity does not produce 100x the expected gift; the scaling is gentler to reflect diminishing marginal utility of wealth.

## Golden Corpus

The evaluator is validated against a golden corpus of 15+ exemplar cases covering all tri-value outcomes and adversarial scenarios.

**True cases (5+):**
- Person A donates $500 to a food bank; earns $30K/year; no return gift or expectation.
- Person B volunteers 40 hours/month to a youth mentorship program; pays for mentee's materials out-of-pocket; mentee cannot reciprocate.
- Person C shares critical proprietary domain knowledge with a competitor's junior engineer (no subsequent benefit to C); acts driven by desire to raise industry standard.
- Person D contributes code to open-source for 2+ years; receives no financial return; community benefit is the sole reward.
- Person E provides interest-free loan to a struggling friend with no formal repayment schedule; never demands repayment; cancels the debt after 3 years.

**False cases (5+):**
- Person F gives gifts exclusively to people who later return gifts of similar or greater value; pattern is tit-for-tat exchange.
- Person G donates $50 to charity but claims $5000 tax deduction and engages in aggressive tax planning; primary motive is tax avoidance.
- Person H gives "gifts" to employees on the day before performance reviews; recipients are later promoted, suggesting quid-pro-quo.
- Person I time-shifts giving and receiving: gives large gifts in year 1, receives benefits in year 2; overall exchange is reciprocal when viewed across multiple years.
- Person J gives small gifts ($5–10) to many people; counts exceeds threshold but normalized absolute values are trivial relative to capacity.

**Insufficient_Evidence cases (3+):**
- Person K has 1 giving record in the window; too sparse to establish pattern.
- Person L's chain is anemic: 2 total events, one of which is a small gift; depth below MIN_DEPTH.
- Person M donated once 8 months ago; window is 12 months; no additional giving in the past 4 months; pattern is unclear.

**Adversarial gaming cases (2+):**
- Person N creates fake giving records (logs "skill_shared" with a non-existent recipient); counterparty graph validation (E133) detects the recipient does not exist or is a shell.
- Person O orchestrates "public" giving (visible transfer to charity) but privately claws back funds via a related entity; E133 anti-fraud rules flag suspicious bidirectional flows.

## Composition with Altruism Index (E171)

This predicate establishes **evidence-based generosity** (giving without reciprocal expectation). It composes with Everest 171 (altruism index), which asks a deeper question: *Why does the principal give?*

- **E166 True + E171 pure-altruism:** Principal gives freely and reports internal motivation (e.g., "helping others makes me feel fulfilled"). Strong unselfishness signal.
- **E166 True + E171 reputation-motive:** Principal gives and consciously or unconsciously expects social credit. Weaker unselfishness signal; generosity is instrumentalized.
- **E166 False + any E171 value:** No giving pattern; altruism question is moot.

The conjunction of E166 and E171 produces a nuanced picture of the principal's cooperative disposition.

## Anti-Gaming Mechanisms

1. **Capacity normalization:** Prevents wealthy principals from gaming the predicate by making trivial absolute gifts appear generous. Normalization is private (counterparties don't see the capacity index), so a principal cannot reverse-engineer the scoring.

2. **Non-reciprocity check:** The E109 inference layer detects latent quid-pro-quo intent. Gifts disguised as altruistic but followed by requests for favor, preferential treatment, or business advantage are flagged as reciprocal.

3. **Counterparty graph validation (E133):** Recipient entities are verified to exist and have independent agency. Fake recipients, shell entities, and loops (A gives to B gives back to A) are detected and excluded.

4. **Temporal guard:** Reciprocal giving detected across multi-year periods (e.g., give in year 1, receive in year 3) are still identified as exchanges because the counterparty graph tracks all transactions.

5. **Normalization opacity:** The capacity factor is never disclosed, preventing reverse-engineering. A high-capacity principal cannot deduce which gifts "count" by observing which are included in the evidence.

## Disclosure Defaults

Per E113 (disclosure governance), generosity evidence has the following disclosure policies:

- **peer_ai_collective:** ALLOW — Peers and collaborative environments can see generosity evidence to build trust and reputation within the collective.
- **philanthropic_org:** ALLOW — Charitable organizations can access generosity evidence to assess grantee worthiness and impact.
- **mentor:** ALLOW — Mentors and advisors can see evidence to guide the principal's development and recognize generous behavior.
- **financial:** DENY — Financial institutions (lenders, credit bureaus) are prohibited from seeing generosity evidence. High generosity does not imply creditworthiness, and the correlation could introduce unfair lending bias. This prohibition is binding per E114.
- **employer:** DENY — Employers are prohibited from seeing generosity evidence to avoid penalizing generous employees or rewarding those who give strategically to gain favor with leadership.
- **insurance:** PERMANENTLY DENY — Insurance providers can never see generosity evidence; using it to assess risk would be a privacy and discrimination violation.

## Zero-Knowledge Proof Composition

Generosity evidence integrates into the ZK proof system (E45 Bulletproof framework) to allow a principal to prove generosity without disclosing the underlying chain data.

**Proof components:**
- **Merkle commitment** to the giving-records sub-tree: Root hash commits to all relevant transaction records without revealing individual details.
- **Range proof** on the count of non-reciprocal records: Proves that `count(non_reciprocal_giving) >= threshold` without disclosing the exact count or identities.
- **Capacity normalization via private auxiliary input:** The principal's capacity index is a private input; the verifier confirms that normalized gift values are acceptable without learning absolute wealth.
- **Reciprocity proof:** Boolean commitment to the non-reciprocal filter result; proven true without exposing the inference mechanism's intermediate steps.

**Verification:** An external verifier can confirm that the principal's chain exhibits generosity sufficient to meet the threshold, without access to transaction details, recipient identities, or capacity data. The proof is publicly shareable (with disclosure controls applied).

**Proof size:** Commitment + range proof + reciprocity flag ~ 1.5 KB. Generation time < 1 second on M-class hardware (laptop, smartphone).

## Performance Bounds

- **Proof generation:** < 1 second on M-class (laptop-grade CPU/GPU).
- **Verification:** < 500 ms.
- **Chain query (records_in_window):** O(log N) on indexed chain; typically < 50 ms for chains of 1M+ records.
- **Non-reciprocal filter:** O(k log N) where k = count of giving records; typically < 200 ms.
- **Capacity inference:** Pre-computed and cached; < 10 ms lookup.

**Scalability:** The algorithm is linear in the number of giving records in the window (typically 5–50 per person per year). It does not degrade on chain size. Proof generation is parallelizable across proof components.

## Example Evaluation

**Principal: Alice, window=365 days, threshold=5**

Chain events in window:
- Day 10: $200 gift to friend Bob (no return gift); "gift"
- Day 45: 20 hours mentoring junior engineer; pays $500 for mentee's course; "time_given" + "giving.financial"
- Day 120: $1000 donation to food bank; "giving.financial"
- Day 200: Shares patent cross-license with startup for free; startup cannot reciprocate; "skill_shared"
- Day 340: $300 gift to cousin (cousin gives back $150 gift 3 months later) — reciprocal, excluded.

Non-reciprocal giving: 4 records (first four). Alice's capacity is moderate ($60K/year income). Normalized values are all above floor. Chain depth = 10 events, exceeds MIN_DEPTH.

**Threshold is 5, non-reciprocal count is 4.**

Result: **False** (missing 1 record to reach threshold).

But if Alice had one more non-reciprocal giving record, result would be **True**.

## Relationship to Prior Everests

- **E52 (predicate canonical form):** Everest 166 follows the E52 template for name, parameters, output, algorithm, and golden corpus.
- **E107 (generosity dimension):** Everest 166 operationalizes the high-level values dimension from E107; E107 is the philosophical layer, E166 is the technical implementation.
- **E109 (values from action inference):** Everest 166 uses E109's inference engine to detect reciprocal intent hidden in transaction chains.
- **E113 (disclosure governance):** Everest 166 integrates E113 disclosure defaults; no disclosure policy is set unilaterally.
- **E114 (consent & fairness):** E166 respects E114 constraints; financial institutions cannot access generosity evidence.
- **E133 (anti-fraud validation):** Counterparty verification and suspicious-pattern detection are delegated to E133.
- **E171 (altruism index):** Everest 171 asks "why does the principal give?" E166 asks "does the principal give?" They compose to assess unselfishness holistically.

## Closure

Everest 166 establishes a rigorous, anti-gameable predicate for generosity grounded in evidence: the demonstrable pattern of non-reciprocal giving, capacity-normalized, verified by the E109 inference layer, and composed with multi-year transaction graphs. The predicate operationalizes John's framing of "unselfish" as action-based rather than self-reported. Proof generation is fast and proof size is compact, enabling efficient integration into the Calm protocol and the broader ZKAC architecture.

---

*— Calm, 2026-05-20*
