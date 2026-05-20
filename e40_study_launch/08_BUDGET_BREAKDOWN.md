# Budget Breakdown — Everest 40 Study

*All figures in USD. Envelope per Everest 40 design doc: ~$78K total.*

| Category | Item | Detail | Amount |
|----------|------|--------|--------|
| **Participant compensation** | Enrollment honorarium | $50 × 15 principals | $750 |
| | Weekly session compensation | $30 × 12 sessions × 15 principals | $5,400 |
| | Completion bonus | $60 × 13 principals (~85% completion) | $780 |
| | Subtotal | | **$6,930** |
| **Plamondon site (primary, École Polytechnique de Montréal)** | RA salary | ~6 person-months @ local rate | $14,400 |
| | Local IRB administrative fee | One-time | $1,200 |
| | Equipment (iPad + Apple Pencil Pro loan pool) | 8 units × $1,000 (returned after study) | $8,000 |
| | Senior collaborator honorarium (Plamondon + 2) | $5K + $3K + $3K | $11,000 |
| | Indirect / institutional overhead | ~15% on direct costs at site | $3,000 |
| | Subtotal | | **$37,600** |
| **Halvani site (secondary, Hochschule Darmstadt)** | RA salary | ~4 person-months @ local rate | $9,600 |
| | Local IRB administrative fee | One-time | $800 |
| | Equipment (iPad + Apple Pencil Pro loan pool) | 4 units × $1,000 | $4,000 |
| | Senior collaborator honorarium (Halvani + 2) | $4K + $2.5K + $2.5K | $9,000 |
| | Indirect / institutional overhead | ~15% on direct costs at site | $1,800 |
| | Subtotal | | **$25,200** |
| **ASQDE adversarial-sample arm (Everest 41 prep, included in E40 launch)** | Examiner commissions | 3 examiners × $3K base | $9,000 |
| | Per-sample fees | ~30 samples × $200 (avg) | $6,000 |
| | Society honoraria | $500 × 3 examiners referred | $1,500 |
| | Subtotal | | **$16,500** |
| | | | |
| **Cross-site infrastructure (Calm-side)** | Capture-app maintenance and bug-fix during study | ~1 engineer-month | $12,000 |
| | OSF.io pre-registration + reproducibility container hosting | One-time | $300 |
| | Statistical analysis support (consultant, ~80 hours) | $150/hr | $12,000 |
| | Subtotal | | **$24,300** |
| | | | |
| **Publication and dissemination** | arXiv preprint and figure preparation | | $800 |
| | Open-access fee (target journal APC) | One-time | $2,500 |
| | Subtotal | | **$3,300** |
| | | | |
| **Contingency (10%)** | Reserve for protocol deviations, additional recruitment, IRB amendments | | $11,400 |
| | | | |
| **TOTAL** | | | **$125,230** |

## Reconciliation with the $78K Envelope

The full budget as itemized is **$125K**, materially above the Everest 40 design doc envelope. This reflects two scope additions explicitly authorized by the chain:

1. **The Halvani secondary site** ($25.2K). The Everest 40 design doc anticipated a single primary site at ~$30-40K of site-level spend; the Halvani-arm voice-stylometry collaboration is a substantive scope addition justified by the value of cross-lingual generalization to publication strength and to defensibility under Everest 41 threat modeling.
2. **The ASQDE adversarial-sample arm** ($16.5K). This is the upstream-prep arm for Everest 41 (adversarial robustness), bundled here because the consent infrastructure and ASQDE engagement must be in place at Everest 40 launch (you cannot retroactively consent participants to adversarial use).

**Two budget options for steering review:**

- **Option A — De-scope to $78K envelope.** Drop the ASQDE arm (-$16.5K) and the Halvani site (-$25.2K), pushing them to Everest 41's own budget. The Everest 40 study then runs single-site at Montréal at ~$83K (after contingency adjustment), close to envelope.
- **Option B — Fund at $125K.** Treat Everest 40 and the Everest 41 prep as a single integrated launch (which is what this packet does). Total spend $125K but the marginal cost of Everest 41 itself drops correspondingly. This is the option this packet is built around.

**Recommendation:** Option B. Treating the ASQDE arm as Everest 40 work (which it logically is, given that adversarial-use consent must be obtained at enrollment) avoids the operational risk of having to re-consent participants months later. The $47K marginal spend is the right way to spend the project's adversarial-robustness budget.

If Option A is chosen, the steering decision should be documented and `00_README.md` adjusted accordingly.

---

— Calm, 2026-05-20
