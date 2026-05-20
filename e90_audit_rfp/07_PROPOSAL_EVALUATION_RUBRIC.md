# Proposal Evaluation Rubric — Calm Witness v0 Audit

*Internal document. The instrument the selection committee uses to score incoming proposals. Each axis is scored 1–10; weighted score is the sum of (axis_score × axis_weight). Total maximum: 100.*

---

## Weighted Axes

| # | Axis | Weight | Scoring Anchors |
|---|------|--------|-----------------|
| 1 | **Public track record on cryptographic protocol audits** | 40% | **10**: 3+ published audits of similar-shape cryptographic protocol work (ZK proofs, threshold signatures, Σ-protocols) in the past 3 years, with named senior auditors on the proposed team. **5**: At least one published audit of a comparable cryptographic protocol; some senior involvement. **1**: No published cryptographic-protocol audits; only smart-contract or general-application work. |
| 2 | **Primitive expertise** | 25% | **10**: Demonstrated direct experience with Bulletproofs, Pedersen commitments on Ristretto255, BLS12-381 or FROST, Σ-protocols with Fiat-Shamir, and hash-chain integrity primitives — evidenced by published reports or named-engineer publications. **5**: Familiar with ZK and threshold signatures generally; specific primitive expertise inferred but not directly demonstrated. **1**: General cryptographic competence; would need to ramp on the specific primitives. |
| 3 | **Capacity for the 6–12 week engagement window** | 15% | **10**: Vendor confirms the proposed engagement window is available; named team has dedicated capacity; kickoff in 6–8 weeks is feasible. **5**: Vendor has capacity with some flexibility on dates; staffing details to be confirmed. **1**: Vendor's earliest availability is significantly later than Calm's target; or staffing is unclear or contingent. |
| 4 | **Cost within envelope** | 10% | **10**: Bid within $120K–$200K with clear scope coverage. **7**: Bid $200K–$250K, justified by scope. **3**: Bid above $250K; requires scope renegotiation or budget extension. **1**: Bid significantly above $250K without clear scope-driven justification. |
| 5 | **Willingness to publish a signed public summary** | 10% | **10**: Vendor explicitly confirms signature on public summary as part of the bid; provides examples of prior signed public summaries. **5**: Vendor willing in principle; specifics negotiable. **1**: Vendor resists publication or restricts to anonymized findings only. |

**Total maximum weighted score: 100.**

## Tie-Breaker — Independence

If two or more proposals are within 3 weighted points of each other, **independence from Calm contributors and DERB members** is the tie-breaker.

Independence is evaluated as:

- **Strongest** (preferred): Vendor has no prior commercial relationship with Calm contributors, Creativity Machine LLC, or DERB-affiliated organizations, and no named engagement-team member has a personal relationship with Calm contributors that would impair perceived independence.
- **Strong**: Vendor has no current relationship; minor historical contact (e.g., conference acquaintance) but no commercial entanglement.
- **Acceptable**: Vendor has a historical but non-current relationship; recused individuals from the engagement team; documented mitigation.
- **Disqualifying**: Vendor is currently advising Calm contributors on related matters, holds equity in Creativity Machine LLC, or includes a named auditor with current relationship to a DERB member.

Disqualifying independence concerns override total weighted score: a proposal with disqualifying independence is excluded regardless of other scoring.

## Scoring Sheet (per evaluator)

| Bidder | Axis 1 (×40%) | Axis 2 (×25%) | Axis 3 (×15%) | Axis 4 (×10%) | Axis 5 (×10%) | Total (/100) | Independence | Notes |
|--------|---------------|---------------|---------------|---------------|---------------|--------------|--------------|-------|
| Trail of Bits |  |  |  |  |  |  |  |  |
| NCC Group |  |  |  |  |  |  |  |  |
| Least Authority |  |  |  |  |  |  |  |  |
| Cure53 |  |  |  |  |  |  |  |  |
| Kudelski |  |  |  |  |  |  |  |  |
| Quarkslab |  |  |  |  |  |  |  |  |

## Committee Process

- Each committee member (Calm contributor, DERB member, independent cryptography advisor) scores independently using the above sheet.
- Scores are then discussed in a single 90-minute session; outliers (>2-point spread on any axis) are reviewed and reconciled.
- Final committee score is the mean of reconciled member scores.
- Top-ranked proposal is selected; runner-up is held in reserve in case primary selection falls through.
- Selection rationale (1–2 pages) is documented and shared with the Calm operator. The selection memo is anchored into the chain as a `kind: "audit_vendor_selected"` entry.

---

— Calm, 2026-05-20
