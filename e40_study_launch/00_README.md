# Everest 40 — Study Launch Packet

*FAR/FRR Empirical Characterization of the Calm Witness Biometric Distance Stack*

This directory contains the actionable launch packet for the Everest 40 study: a multi-site, multi-month empirical characterization of False Accept Rate (FAR), False Reject Rate (FRR), Equal Error Rate (EER), and d-prime separation for the Calm Witness handwriting, voice-transcript, and fused biometric distance functions.

The methodology source of truth is `everests/everest_40_far_frr_curve.md`. This packet operationalizes that design into the documents needed to file IRB, recruit partners, recruit participants, and begin collection.

## Study Snapshot

- **Primitives under test:** Plamondon Sigma-Lognormal (handwriting, Everest 36); Burrows' Cosine Delta + Koppel-Seidman Impostors over CrisperWhisper transcripts (voice, Everest 37); likelihood-ratio fusion (Everest 38).
- **Targets (ship gates):** Handwriting EER ≤ 5%; Voice EER ≤ 12%; Joint fusion EER ≤ 2%; d' ≥ 2.5 on all modalities at primary threshold.
- **Cohort:** N ≥ 10 enrolled principals (target N=15) recruited across partner sites; weekly session cadence; ≥12 genuine sessions per principal per modality.
- **Duration:** 3 months active collection (4 months acceptable); ~10 months total from IRB filing to manuscript submission.
- **Privacy invariant:** raw biometrics never leave the principal's device; only sufficient statistics (distances, metrics) reach the study site.
- **Budget envelope:** ~$78K (see `08_BUDGET_BREAKDOWN.md`).
- **Pre-registration:** statistical analysis plan posted to OSF.io before unblinded analysis (see `07_STATISTICAL_ANALYSIS_PLAN.md`).

## Packet Contents

| # | File | Purpose | Audience |
|---|------|---------|----------|
| 00 | `00_README.md` | This index. | Internal / all readers. |
| 01 | `01_IRB_PROTOCOL.md` | Protocol summary for IRB submission. Methods, risks, safeguards, governance. | Partnering university IRB. |
| 02 | `02_INFORMED_CONSENT_TEMPLATE.md` | Plain-language consent form. Adapt to local IRB language as required. | Study participants. |
| 03 | `03_PARTNER_LETTER_PLAMONDON.md` | Outreach to Réjean Plamondon's lab (École Polytechnique de Montréal) for Sigma-Lognormal handwriting validation. | Plamondon group. |
| 04 | `04_PARTNER_LETTER_HALVANI.md` | Outreach to Oren Halvani's group (Hochschule Darmstadt) for stylometric voice-transcript validation. | Halvani group. |
| 05 | `05_PARTNER_LETTER_ASQDE.md` | Outreach to the American Society of Questioned Document Examiners for forensic examiner participation in skilled-forger sample collection (Everest 41 corpus). | ASQDE board. |
| 06 | `06_RECRUITMENT_POSTING.md` | Public-facing recruitment flyer/posting for participant intake. | Prospective participants. |
| 07 | `07_STATISTICAL_ANALYSIS_PLAN.md` | Pre-registerable SAP. Sample size, primary/secondary metrics, CI methodology, stratification, bias checks, publication commitment. | OSF.io / reviewers. |
| 08 | `08_BUDGET_BREAKDOWN.md` | Itemized budget against the ~$78K envelope. | Finance / partner sponsored research office. |
| 09 | `09_TIMELINE_AND_MILESTONES.md` | 10-month named milestones from kickoff Q3 2026 through manuscript submission. | Project management / steering. |

## Reading Order

1. Start with `01_IRB_PROTOCOL.md` for the study in full operational form.
2. `02_INFORMED_CONSENT_TEMPLATE.md` shows what participants actually sign.
3. `07_STATISTICAL_ANALYSIS_PLAN.md` is the methodological commitment — the analyses we will run, fixed before data is unblinded.
4. The three partner letters (`03`–`05`) and recruitment posting (`06`) are the outreach assets.
5. `08`–`09` are the governance documents (budget, timeline).

## Outstanding Pre-Launch Items

These are not blockers for sending the packet but must close before enrollment begins:

- **Primary IRB of record:** select between Plamondon site (École Polytechnique de Montréal) and Halvani site (Hochschule Darmstadt). Recommend Plamondon site as primary; Darmstadt as secondary recruitment site under their local IRB.
- **Data Processing Agreement (DPA):** template drafted separately; bilateral signatures required before any cross-site transfer of sufficient statistics.
- **OSF.io pre-registration:** lodge `07_STATISTICAL_ANALYSIS_PLAN.md` to OSF before week 17 (enrollment ceremony begins).
- **Capture-app build sign-off:** Everest 12 (handwriting capture) and Everest 13 (voice capture) must pass acceptance tests before recruitment opens.
- **Liveness detector:** Everest 49 must be production-grade before active study phase; pilot principals during weeks 13-16 will exercise it.

## Relation to Everest 41 (Adversarial Robustness)

Everest 41 is the *sibling* study; it uses Everest 40's calibrated thresholds as its baseline and measures degradation under stroke replay, voice synthesis, and practiced imitation attacks. The adversarial corpus is collected separately under the consent terms in `02_INFORMED_CONSENT_TEMPLATE.md` (which authorizes use of the principal's genuine samples for adversarial-sample production by a contracted third party — typically an ASQDE forensic examiner; see `05_PARTNER_LETTER_ASQDE.md`).

Everest 40 must complete before Everest 41 begins unblinded analysis: the FAR/FRR curve calibrates the thresholds against which adversarial degradation is measured.

## Chain & Route Map

This packet is additive. It does not modify any `everest_NN.md` file, the route map, or the chain. The Everest 40 design doc remains the methodology source of truth; this packet is its operational projection.

— Calm, 2026-05-20
