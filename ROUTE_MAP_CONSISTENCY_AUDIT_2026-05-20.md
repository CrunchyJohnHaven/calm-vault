# Route Map Consistency Audit — 2026-05-20

**Filed by Calm during meta-substrate review of the active 100-Everest climb.** Sister doc to [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md). Captures a structural inconsistency between the **per-summit `BAGGED` markers** and the **bottom-of-file Status table** so the next session has a clear remediation path.

## Finding

At time of audit (file mtime `2026-05-20 11:23 EDT`):

- **38 summits** carry an authoritative per-summit `**BAGGED (Summit N/100) …**` marker in their detail body.
- The Status table at the bottom of the file claims **48 summits bagged**.
- Discrepancy: **10 summits**.

## Per-phase breakdown

| Phase | Status table claim | Marker count | Δ | Notes |
|---|---:|---:|---:|---|
| I (1–10) | 10 | 10 | 0 | Consistent. PHASE COMPLETE on both sides. |
| II (11–25) | 7 (incl. **E14**) | 6 | +1 | E14 listed in status, no per-summit marker. |
| III (26–35) | 7 (incl. **E32**) | 6 | +1 | E32 listed in status, no per-summit marker. |
| IV (36–50) | 5 | 5 | 0 | Consistent. |
| V (51–65) | 6 | **11** (incl. E53, E56, E60, E63, E64) | **−5** | Status table undercounts: it lists `(51, 52, 55, 57, 58, 59)` and omits markers for `(53, 56, 60, 63, 64)`. |
| VI (66–80) | 8 (E66, 67, 70, 72, 73, 77, 78, 79) | 0 | +8 | Status table claims 8 bagged; per-summit body for those Everests does **not** yet carry a BAGGED marker. |
| VII (81–90) | 3 (E82, 84, 88) | 0 | +3 | Same pattern — table claim, no marker. |
| VIII (91–100) | 2 (E92, 98) | 0 | +2 | Same pattern. |
| **TOTAL** | **48** | **38** | **−10 vs claim** | Net: table over-claims by 10 (13 over-claims minus 5 under-claims, net +8 according to the bidirectional Δ; total absolute discrepancy is 15 cell-level disagreements). |

## What's actually happening

The Status table appears to be **hand-curated separately** from the per-summit BAGGED markers. The two sources drift because they have no common generator. The parallel CALM session climbing the route is updating both — but bidirectional updates introduce both undercounts (Phase V) and over-claims (Phases VI–VIII) as bag-claims are made faster than per-summit markers are written, or vice versa.

This is a load-bearing problem. The Status table is what readers (including future-John, counterparties auditing the protocol, and the ratification reviewer) see first. If it disagrees with the per-summit truth, the audit log of the climb is unreliable.

## Proposed fix (defer-to-parallel-session)

**One source of truth, derived from the other.** The per-summit BAGGED marker is the natural source (it carries the date, the evidence path, the bag-line prose). The Status table should be **generated from the markers**, not hand-curated.

Concrete remediation (in priority order):

1. **`scripts/audit_route_map_consistency.py`** — a small Python script that parses `ZKBB_USER_EVERESTS_100.md`, counts per-summit BAGGED markers by phase, and emits the corrected Status table block. Run before each commit; fail CI if the file's table disagrees with the generated table.
2. **Phase V status table line is currently the most-undercounted.** Specifically: it lists `(51, 52, 55, 57, 58, 59)` but the per-summit markers prove the following are also bagged: **E53 (Predicate ID Registry), E56 (`biometric_match_within` ref impl), E60 (`mental_state_unusual` ref impl), E63 (Determinism harness), E64 (Test corpus)**. Update on the next route-map commit.
3. **Phases VI / VII / VIII bag claims are currently NOT backed by per-summit markers.** If those summits are intended as bagged, add the `**BAGGED (Summit N/100) 2026-05-20** — evidence-link` line to each per-summit body. If they are aspirational (the table is forecasting the next round), demote the table to "bagged + claimed-bagged-pending-marker" so the difference is honest.

## What this audit does **not** modify

- I have not edited [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) during this audit. The route map is being actively written by the parallel CALM session (last mtime ≤60 s before this filing); editing concurrently would cause merge conflicts and is exactly the failure mode [[feedback-calm-parallel-session-coordination]] in memory warns against.
- No chain records were appended for this audit. The substrate is the principal's, not the auditor's.

## Authorship

Audited by Calm (this session, post-ratification of Path B Calm Pact group lock), 2026-05-20. Released to the parallel CALM session for action when it next reads this directory.

## Cross-references

- [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) — the source.
- [`CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md`](CALM_PACT_SPEC_INCONSISTENCY_OPEN_ISSUE.md) — the resolved Pact-side analogue; precedent for the open-issue-then-ratify pattern.
- Memory: [[feedback-calm-parallel-session-coordination]] for why the route map is not edited inline here.
