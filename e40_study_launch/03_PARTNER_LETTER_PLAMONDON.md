# Partner Outreach — Plamondon Group, École Polytechnique de Montréal

*Letter of inquiry and collaboration proposal*

**Date:** 2026-05-20
**To:** Prof. Réjean Plamondon and the Laboratoire Scribens / Synchromedia group
School of Engineering, École Polytechnique de Montréal
**From:** Calm Research — John Bradley, on behalf of the Calm Witness protocol team
**Subject:** Proposal for collaborative empirical validation of Sigma-Lognormal-based behavioral-biometric verification

---

Dear Prof. Plamondon and colleagues,

I am writing on behalf of the Calm Witness protocol team to propose a structured research collaboration with the Laboratoire Scribens. Our project, briefly: we are building a behavioral-biometric proof-of-personhood system whose handwriting-distance function is built directly on top of your Sigma-Lognormal decomposition of pen trajectories. We are now at the stage of large-scale empirical validation — a study we call internally "Everest 40" — and we believe the resulting work belongs in your community as much as in ours.

## Why we chose Sigma-Lognormal

Our protocol must distinguish *on-manifold drift* (the principal is ill, tired, aging, or has injured their writing hand) from *off-manifold variation* (this is not the principal at all). Your kinematic theory of human movement is, in our review of the literature, the only framework that gives this distinction a principled basis. The kinematic micro-features (pen velocity, acceleration, jerk, pressure-release pattern, sub-millisecond pen-lift timing) carry the impostor signal even when the visual product (slant, character shape, spacing) has been successfully imitated. This is load-bearing for our system, which has to accept "the principal but unwell" while rejecting "a practiced imitator." We are not aware of any alternative formulation with comparable evidential weight.

We have implemented a distance function based on Sigma-Lognormal parameter recovery from `PKStrokePoint` time-series (Apple Pencil Pro on iPad, with Wacom normalization for cross-stylus compatibility). The implementation references your group's published parameter-recovery algorithms (Plamondon et al. 2003; O'Reilly & Plamondon 2009; Plamondon & Diaz 2014). We have a working pipeline and pilot data on N=4 internal participants; the next step is the formal multi-month, multi-principal study that the field expects before any production deployment.

## What we are asking

We propose that the Laboratoire Scribens serve as the **primary study site** for Everest 40. Concretely:

1. **Host the IRB approval.** École Polytechnique's Research Ethics Board would be the IRB of record. We provide a complete protocol package (see attached IRB protocol summary, consent form, statistical analysis plan).

2. **Recruit and host N=10-15 participants.** Your Montréal participant pool is well-suited; bilingual (French/English) capability is a bonus for cohort diversity. We provide compensation funds ($410-470 per participant) and the capture-app build.

3. **Co-design the kinematic-validation arm.** We would value your group's input on cohort composition (especially representation of writing-hand-injury rehabilitation participants, where your prior work on health-status estimation is directly relevant), on prompt design, and on the temporal-drift regression methodology.

4. **Co-author the resulting publication.** We propose a joint publication with shared first/senior authorship in a venue of your group's preference (we have been considering *IEEE Transactions on Biometrics, Behavior, and Identity Science* but defer to your group's relationships).

## What we offer

- **Funding:** $78K study budget, of which approximately $25K flows to École Polytechnique (participant compensation, RA salary for ~6 person-months at the local rate, IRB administrative fee, equipment if needed).
- **Honorarium for senior collaborators:** $5,000 honorarium for Prof. Plamondon and $3,000 each for up to two additional senior investigators from the Laboratoire Scribens, payable on manuscript submission. This is in addition to RA salary support.
- **Open-source implementation access:** the full Calm Witness handwriting-distance implementation (Everest 36) is available under permissive license to your group, including all hyperparameters, calibration code, and pilot data. The implementation is available now; we can do a code walkthrough in the next two weeks if useful.
- **Pre-registration commitment:** our statistical analysis plan will be posted to OSF.io before unblinded analysis. There is no possibility of post-hoc retrofitting; the analysis is fixed.
- **Publication regardless of outcome:** if the Sigma-Lognormal-based system fails to meet our internal ship-gate (EER ≤ 5% on handwriting alone), we publish the null result. We are seeking ground truth, not validation theater.

## Specific deliverables

- A peer-reviewed paper with shared authorship reporting FAR/FRR curves, EER, d-prime, and a stratified analysis by writing-hand-dominance and age tertile.
- A public technical report (arXiv preprint) posted simultaneously.
- A reusable open-source pipeline that your group can use for downstream Sigma-Lognormal validation work.
- Anonymized aggregate-statistics dataset (no raw biometrics, never) posted to a public repository per the conditions in our IRB protocol.

## Timeline

We hope to file with your IRB by August 2026, complete enrollment by November 2026, complete sampling by February 2027, and submit a manuscript in late spring 2027. The Everest 40 design has been internally locked since May 2026; the question on our side is whether your group has the bandwidth and interest, not whether we are ready.

## Next steps

May we propose a 30-minute video call in the next two weeks to discuss the protocol, your group's interest, and any modifications you would suggest? I am available at the email below and would be happy to fly to Montréal for an in-person meeting if that is preferable.

If your group is unable to take this on, I would be grateful for any pointers to other groups (in your network or elsewhere) you would recommend.

Thank you for your time and for the foundational work that makes this project possible.

With respect and looking forward,

**John Bradley**
Calm Research
john@[domain]
[phone]

---

— Calm, 2026-05-20
