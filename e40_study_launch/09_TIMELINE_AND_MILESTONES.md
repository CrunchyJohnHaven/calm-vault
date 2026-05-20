# Timeline and Milestones — Everest 40 Study

*Kickoff: Q3 2026 (July 1, 2026). All target dates assume kickoff at that anchor and may shift by ±2 weeks without re-baselining.*

---

## Summary

| Milestone | Owner | Target |
|---|---|---|
| **M0 — Kickoff** | Calm | 2026-07-01 |
| **M1 — Partner MOAs signed** | Calm + Plamondon + Halvani | 2026-07-31 |
| **M2 — IRB submission filed (Montréal primary)** | Plamondon site PI | 2026-08-21 |
| **M3 — Statistical Analysis Plan locked at OSF.io** | Calm + biostats consultant | 2026-08-28 |
| **M4 — Capture app v1.0 acceptance signed off** | Calm engineering | 2026-09-04 |
| **M5 — IRB approval received (Montréal)** | Plamondon site PI | 2026-09-25 |
| **M6 — Recruitment posting goes live** | Both site coordinators | 2026-10-01 |
| **M7 — ASQDE engagement confirmed; 3-5 examiners under contract** | Calm + ASQDE | 2026-10-15 |
| **M8 — N=15 enrollment ceremony complete** | Site coordinators | 2026-11-15 |
| **M9 — Week 1 sampling begins** | Site coordinators | 2026-11-22 |
| **M10 — Mid-study check-in (week 6)** | Both site PIs | 2027-01-03 |
| **M11 — Active sampling complete (week 12)** | Site coordinators | 2027-02-14 |
| **M12 — Data lockdown; unblinded analysis begins** | Calm biostats | 2027-02-28 |
| **M13 — Primary analysis complete; full results memo** | Calm biostats | 2027-03-28 |
| **M14 — Manuscript draft circulated to all co-authors** | Calm + Plamondon + Halvani | 2027-04-25 |
| **M15 — Manuscript submitted to target journal + arXiv preprint posted** | All authors | 2027-05-16 |

**Total elapsed: ~10.5 months from kickoff to submission.**

## Phase Detail

**Setup phase (M0 - M4, July - early September 2026, ~10 weeks):**
Partner contracts, IRB protocol package finalization and submission, SAP pre-registration to OSF.io, capture-app build sign-off (Everest 12/13 capture apps; Everest 49 liveness detector; Everest 44 Pedersen-commitment integration). The SAP must be locked on OSF before any recruitment begins — this is the pre-registration discipline.

**IRB review phase (M2 - M5, late August - late September 2026, ~5 weeks):**
Allow 5 weeks for IRB review on the assumption of expedited-review eligibility (minimal-risk behavioral study). If the IRB requires full board review, this phase extends by 4-6 weeks; the timeline slips accordingly but downstream milestones each shift by the same amount. Plamondon site is the primary IRB of record; Halvani site applies in parallel under their local REB.

**Recruitment and enrollment phase (M6 - M8, October - mid-November 2026, ~6 weeks):**
Recruitment posting circulated through partner-institution channels (university listservs, departmental newsletters, social media). Enrollment ceremonies are scheduled in week-by-week batches as participants sign up; the M8 milestone is the *completion* of enrollment for all 15 principals. ASQDE engagement happens in parallel (M7).

**Active sampling phase (M9 - M11, late November 2026 - mid-February 2027, ~12 weeks):**
The 12 weekly sessions per principal. Mid-study check-in at week 6 (M10) confirms retention and uncovers any operational issues. Mid-study is also when the first interim *operational* check on liveness-rejection rates is performed (this is a quality-control check, not an interim analysis, and is explicitly distinguished from any unblinded scientific interim analysis, which is not performed).

**Analysis and write-up phase (M12 - M15, late February - mid-May 2027, ~12 weeks):**
Data lockdown is the formal moment when the dataset is frozen and analysis begins on the unblinded numbers. Primary analyses (per the pre-registered SAP) take ~4 weeks. Secondary analyses, manuscript drafting, and co-author review take an additional ~8 weeks. Submission target is mid-May 2027.

## Risk-Adjusted Milestones

The above is the "no slip" timeline. Three known risks may extend it:

- **IRB delay (60% likelihood of some delay).** Expected slip: 2-6 weeks. Mitigation: pre-submission consultation with both IRBs in the first weeks of July.
- **Recruitment shortfall (30% likelihood at N=15).** Expected slip if shortfall: 4-8 weeks to expand recruitment channels or accept N=10-12 as cohort. Mitigation: launch recruitment with N=20-22 invitation target, expecting some attrition.
- **Capture-app build slippage (low likelihood — Everest 12/13 already in late development).** Expected slip if it materializes: 4-6 weeks. Mitigation: M4 sign-off is a hard gate; recruitment does not begin until app is signed off.

Best-case timeline: as above, ~10 months. Realistic timeline with one moderate slip: 11-12 months. Worst-case (all three risks materialize): 14-15 months.

## Dependencies on Other Everests

- **Everest 12 / 13** (handwriting and voice capture apps): must reach acceptance-test pass by M4.
- **Everest 36 / 37 / 38** (distance functions): implementations must be production-grade by M4. Currently in late development; on track.
- **Everest 44** (Pedersen commitments): integration with capture-app session-record commitments by M4.
- **Everest 49** (liveness detector): production-grade by M9 (week 1 of sampling). Pilot exercises during recruitment phase.
- **Everest 27** (chain withdrawal-marking): operational by M9 in case any enrolled participant withdraws.

## Successor Milestone (out of scope for Everest 40)

- **M16 — Everest 41 launch.** Adversarial-robustness data collection begins approximately 2-4 weeks after Everest 40 data lockdown (M12), using the calibrated thresholds from this study as the baseline and the ASQDE-produced adversarial samples that have been accumulating throughout Everest 40's active phase. Target: April-May 2027.

---

— Calm, 2026-05-20
