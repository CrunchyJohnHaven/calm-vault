# Everest 126 — Alignment Metric Definition

*Phase V — Values Alignment Computation. Prereq: Everest 107.*

## The Normative Choice Hiding in Technical Language

This document makes a normative claim about what "alignment" means, framed as a technical metric selection. The choice of distance function is not morally neutral. It shapes judgment about which value-vector pairs qualify as "aligned enough" to transact, lend, or trust. Different metrics encode different philosophies of alignment: some penalize one catastrophic deviation differently than many small ones; some ignore absolute magnitude in favor of direction; some demand probabilistic interpretation. v0 selects one and documents the road not taken.

This is not an engineering detail. It is a values choice.

---

## Decision: Weighted Manhattan Distance (L1)

**Formal Definition:**

Let:
- **Principal vector** P = (p_1, ..., p_10) ∈ [0, 1]^10 (principal's disclosed values across 10 dimensions from Everest 107)
- **Counterparty target** T = (t_1, ..., t_10) ∈ [0, 1]^10 (counterparty's disclosed values, same dimensions)
- **Counterparty weights** W = (w_1, ..., w_10) ∈ R_{≥0}^10, where Σ w_i = 1
- **Tolerance threshold** τ ∈ [0, 1] (counterparty-published alignment requirement)

**Distance formula:**

```
distance(P, T, W) = Σ_{i=1}^{10} w_i × |p_i - t_i|
```

**Alignment decision:**

```
alignment_bit = (distance ≤ τ)
```

If distance ≤ τ, the principal and counterparty are aligned at the v0 threshold. If distance > τ, they are not.

---

## Why Weighted L1 (Manhattan) Distance

### The Metric Candidates

**L1 (Manhattan):**
- Sum of absolute per-dimension differences, weighted
- Interpretation: "total Manhattan blocks" between value vectors
- Cost in ZK: single addition per dimension, then sum; no squaring, no roots
- Sensitivity: linear; one gap of 0.3 equals three gaps of 0.1

**L2 (Euclidean):**
- Square root of sum of squared per-dimension differences
- Interpretation: "straight-line distance" in values space
- Cost in ZK: quadratic (requires squaring), plus square root; expensive
- Sensitivity: quadratic; one gap of 0.3 costs 0.09 vs. three gaps of 0.1 cost 0.03 total
- Implication: penalizes large deviations on any single dimension; forgives many small ones

**Cosine Similarity:**
- Dot product of normalized vectors; measures direction not magnitude
- Interpretation: "are they pointing the same way?"
- Cost in ZK: moderate
- Limitation: vectors (1, 0, 0, ...) and (0.01, 0, 0, ...) would appear fully aligned
- Use case: appropriate if values are "directions" not "positions"; not our model

**Kullback-Leibler Divergence:**
- Measures divergence between probability distributions
- Requires interpreting values as probabilities; forces normalization and positivity
- Cost in ZK: expensive (logarithms)
- Limitation: asymmetric; P→T ≠ T→P
- Use case: appropriate if values encode subjective probabilities; not our model

**Chebyshev Distance (L∞):**
- Maximum per-dimension gap: max_i |p_i - t_i|
- Interpretation: "how much do they disagree on their worst dimension?"
- Cost in ZK: cheap (single max operation)
- Limitation: ignores all but the largest disagreement; two parties differing by 0.05 on all 10 dimensions are aligned if tolerance = 0.1
- Implication: loses information about breadth of agreement/disagreement

### L1 Wins v0

**L1 is chosen because:**

1. **Linear per-dimension semantics.** A gap of 0.3 on one dimension costs exactly what it should: 0.3 contribution to distance (weighted). No quadratic magnification of outliers; no probabilistic forcing. Matches the intuition that values are on a spectrum, not a probability distribution.

2. **Interpretability.** The distance number is human-readable. "You differ by 0.18 total Manhattan distance across your 10 value dimensions" is comprehensible. The principal can see which dimensions contribute most to the gap.

3. **Counterparty control via weighting.** The weight vector W is the counterparty's normative lever. Setting w_non_harm = 0.5 and others = 0.5/9 ≈ 0.056 means: "I care 9× more about harm-avoidance alignment than any other dimension." L1 preserves this weighting linearly; no hidden non-linearity.

4. **ZK efficiency.** L1 distance requires only addition, subtraction, and absolute value—no squaring, no roots, no logarithms. In zero-knowledge proofs, this matters. The proof that distance(P, T, W) ≤ τ is substantially cheaper than for L2 or KL.

5. **No forced interpretation.** L2 quietly says: "large deviations are disproportionately bad; forgive many small ones." Cosine says: "direction is what matters; magnitude is noise." KL says: "these are probabilities." L1 says: "these are positions in a space; sum the gaps." For values disclosure, the neutral stance is L1.

**L1 is not neutral.** But it does not disguise its philosophy. It treats each dimension equally (modulo weights) and each point in the dimension equally. That is a defensible position: it does not require a philosophical commitment to, say, "one catastrophic failure invalidates everything" or "many small failures are worse than one big one."

---

## The Weight Vector W: Counterparty's Normative Lever

The counterparty publishes W alongside their values disclosure request. This is public and non-hidden; the principal sees exactly how the counterparty is prioritizing alignment checks.

**Default weights:** Uniform. w_i = 0.1 for each of the 10 dimensions.

**Recommended non-harm weighting:** If the 10 dimensions include a non-harm or safety dimension, the counterparty should publish w_non_harm ≥ 0.2 (at minimum 2× the average weight of 0.1). This reflects the brief's framing: harm-avoidance is not one concern among many; it is load-bearing. The principal can see this weighting and decide whether to engage.

**Example weight vector:** 
- non_harm: 0.25
- honesty: 0.12
- transparency: 0.12
- fairness: 0.10
- sustainability: 0.10
- autonomy: 0.08
- privacy: 0.08
- consent: 0.07
- accountability: 0.05
- open_source: 0.03
- Sum: 1.00

This vector says: "I care most about non-harm (25% of my alignment check), then honesty and transparency equally (12% each), then fairness and sustainability (10% each), then the rest." The principal decides whether this weight distribution matches their own values and risk tolerance.

**Counterparty prerogative:** The counterparty (the entity requesting values disclosure) sets W. They own their definition of alignment. If principal and counterparty disagree about which dimensions matter most, that disagreement is visible in their weight vectors—not hidden in the metric choice.

---

## The Tolerance Threshold τ

The counterparty publishes their tolerance threshold alongside W. This is a trust parameter, not a moral one.

**Interpretation:** "For me to transact with you (lend, trade, partner), your values vector must be within τ Manhattan distance from mine, weighted by my priorities."

**Suggested defaults:**
- **τ = 0.1**: Extremely tight alignment. Principal and counterparty must be nearly identical in values. Appropriate for existential partnerships, deep collaboration, board membership.
- **τ = 0.2**: Moderate alignment. Broad orientation is shared; 20% total distance tolerated. Appropriate for major business partnerships, long-term supply relationships.
- **τ = 0.3**: Loose alignment. Compatible enough to transact, but significant value differences accepted. Appropriate for one-off market transactions, arms-length partnerships.
- **τ ≥ 0.5**: Very loose. Essentially no alignment filter. Appropriate for anonymous commodity markets where values are irrelevant to the transaction.

**Counterparty's choice:** The tolerance is a statement of "how much value-distance am I willing to absorb in this relationship?" It is not universal; the same counterparty might set τ = 0.15 for a board-member candidate and τ = 0.35 for a vendor relationship.

---

## Normative Implications

**What L1 encodes:**

1. **Equal treatment of dimensions (modulo weights).** A gap on honesty counts the same as a gap on autonomy, absent explicit weighting otherwise. This assumes dimensions are commensurable and independently valuable.

2. **No catastrophe weighting.** There is no mechanism that says "one dimension > 0.5 disqualifies entirely." The principal can be 0.4 apart on harm-avoidance and 0.0 on all others, and they will align if τ ≥ 0.4. This is a choice: we do not embed a "veto dimension." (If we did, we would use Chebyshev or a two-stage check. We don't.)

3. **Counterparty defines alignment.** The principal does not judge whether they are aligned with the counterparty. The counterparty does, via W and τ. The principal's disclosure is an answer to the counterparty's question: "Are you aligned *with me*, by my lights?"

4. **No hidden magnification of outliers.** L2 would secretly say "a 0.5 gap on one dimension is worse than five 0.2 gaps." L1 treats them differently only if weighted differently.

---

## Alternatives for v1+ Consideration

**L2 (Euclidean):**
- If values judgment benefits from "outlier penalty," L2 is superior.
- Cost: ZK complexity; harder to interpret; quadratic sensitivity.
- Appropriate for: if one dimension really should veto (approximated via asymptotic L2 behavior).

**Asymmetric Divergences (Bregman):**
- If principal's values are "baseline" and counterparty is evaluated as "deviation," asymmetry may be semantically correct.
- Cost: more complex; requires direction.
- Appropriate for: if one party is applicant and other is gatekeeper.

**Multidimensional Ranking:**
- Instead of "aligned enough?" ask "how aligned?" and rank candidates.
- Cost: no binary decision; requires comparison.
- Appropriate for: competitive selection (e.g., multiple principals applying for one partnership slot).

**Metric Registry (E117 pattern):**
- Future versions could allow counterparties to specify which metric W applies to.
- Cost: complexity; requires ZK support for multiple metrics.
- Benefit: counterparties with non-standard alignment philosophies can opt in.

v0 does not include these. L1 with uniform (or counterparty-tuned) weights and published tolerance is the canonical metric.

---

## Implementation Notes

**For disclosure systems:**
- Principal computes P from their self-assessment on Everest 107 dimensions.
- Counterparty publishes T, W, and τ with their disclosure request.
- System computes distance(P, T, W) and returns alignment_bit.
- Principal sees the distance and the counterparty's weights; can decide whether to engage.

**For zero-knowledge proofs:**
- Proving distance ≤ τ requires range proofs on each |p_i - t_i| term.
- With L1, this is Σ w_i × |p_i - t_i| ≤ τ: sum of bounded terms.
- Simple arithmetic constraints; polynomial number of constraints in dimension count (10).
- Efficient in modern ZK frameworks (Plonk, Halo2, etc.).

**For versioning:**
- This metric is v0. It is not final.
- Uptake, user feedback, and ZK evolution will inform v1+.
- Catalog of alternative metrics is maintained for future reference.

---

## Conclusion

Weighted Manhattan distance is v0's canonical alignment metric. It is not morally neutral—it assumes dimensions are independent, commensurable, and equally valuable absent explicit weighting. It encodes linearity: gaps are additive, not multiplicative. It cedes normative authority to the counterparty, who sets W and τ.

This is intentional. The principal discloses their values; the counterparty judges alignment by their own standards, openly. The metric is the vehicle for that judgment, not a hidden bias.

v0 ships with L1. Future versions will expand the metric registry and support alternatives as ZK and disclosure practice mature.

---

— Calm, 2026-05-20