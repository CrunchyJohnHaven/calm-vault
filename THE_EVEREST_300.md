# THE EVEREST — 300 Summits to a Values-Aligned Behavioral-Attested ZKAC

**John Bradley, 2026-05-20:** *"300 SUMMITS to a Values-Aligned Behavioral-Attested ZKAC => This our EVEREST."*

Canonical registry. Stable IDs (1…300). Maps to home route maps. Single source of truth for parallel-session coordination.

## §1. Range map

|| Range | Pillar | Source route map | IDs in this doc |
||---|---|---|---|
|| **1–100** | Witness (state attestation) | `ZKBB_USER_EVERESTS_100.md` | E1 … E100 |
|| **101–130** | Pact (directive equality) | `CALM_PACT_EVERESTS_30.md` | CP-01 … CP-30 |
|| **131–180** | Compass (values attestation) | `CALM_COMPASS_EVERESTS_50.md` | CC-01 … CC-50 |
|| **181–230** | Tenancy (operator conduct) | `CALM_TENANCY_EVERESTS_50.md` | CT-01 … CT-50 |
|| **231–280** | Operations (substrate) | `CALM_OPERATIONS_EVERESTS_50.md` | CO-01 … CO-50 |
|| **281–300** | Stack Governance | `STACK_GOVERNANCE_20.md` | CS-01 … CS-20 |
|| **Total** | | | **300** |

Stretch (post-EVEREST, not counted toward 300): Witness +30 (`WITNESS_EXTENSIONS_30.md` IDs EW-101…130) and Tenancy +20 (`TENANCY_EXTENSIONS_20.md` IDs CT-51…70).

## §2. Bagged-as-of 2026-05-20

|| Range | Bagged | Of |
||---|---|---|
|| 1–100  Witness   | 63 | 100 |
|| 101–130 Pact     | 0   | 30  |
|| 131–180 Compass  | 2 | 50  |
|| 181–230 Tenancy  | 8  | 50  |
|| 231–280 Operations | 0 | 50  |
|| 281–300 Governance | 0 | 20  |
|| **Total** | **73** | **300** |

Verified via `everest_300_registry_sync_gate.py` (grep **BAGGED) ±1 tolerance on 2026-05-20.

## §3. Parallel-session contract

Multiple Claude/Calm sessions may be working concurrently. Rules:

1. **Claim before bag.** Before a session writes code/docs for SUMMIT N/300, it appends a `kind: "summit_claim"` record to `~/.calm-vault/user_state.jsonl` with `{summit_id, range, session_id, claimed_at_iso}`. If another session has an unexpired claim (TTL 60 min) on the same SUMMIT, the new session picks something else.
2. **Bag at completion.** When a session finishes, it appends a `kind: "summit_bagged"` record with the standard payload + the `claim_record_hash`.
3. **One bagged-doc per SUMMIT.** Lives at `everests/everest_NN_<slug>.md` where NN is the 1–300 ID. (Existing per-pillar IDs are aliased; see §4.)
4. **No silent overwrite.** A session that wants to revise a prior bagged-doc adds `_v2`, `_v3`, etc. The first version is canonical for audit; later versions are amendments.
5. **Cringe gate before publish.** Every `everest_NN_*.md` passes `calm_tenancy/cringe_gate.py` density ≤ 1.0 + no forbidden phrases before commit.

## §4. ID alias table (per-pillar ↔ Everest)

\`\`\`
Everest 1   = E1                Everest 101 = CP-01           Everest 231 = CO-01
Everest 2   = E2                Everest 102 = CP-02           Everest 232 = CO-02
…                               …                              …
Everest 100 = E100              Everest 130 = CP-30           Everest 280 = CO-50
                                Everest 131 = CC-01           Everest 281 = CS-01
                                Everest 132 = CC-02           …
                                …                              Everest 300 = CS-20
                                Everest 180 = CC-50
                                Everest 181 = CT-01
                                …
                                Everest 230 = CT-50
\`\`\`

Use whichever ID is most local in context. The 1–300 ID is canonical for parallel-session claims; per-pillar IDs remain in their home route maps.

## §5. The next 10 priority SUMMITS

Per the master prioritisation (NEXT_200_SUMMITS_2026-05-20.md §3), the next 10 to bag, in order:

|| EV  | Per-pillar | Why now |
||---|---|---|
|| 109 | CP-09 | Pact Rust reference impl — unlocks real crypto kernel |
|| 234 | CO-04 (DID rotation) wait → CO-03 (CredexAI VC) | Unblocks identity binding |
|| 247 | CO-17 Stripe Live-Mode verify | The 2026-05-17 lesson |
|| 139 | CC-09 Compass enrollment ceremony | Compass cannot run without tribe map |
|| 169 | CC-39 Compass disclosure request schema | **bagging this pass** |
|| 170 | CC-40 Compass disclosure response schema | **bagging this pass** |
|| 171 | CC-41 per-counterparty rate limit | **bagging this pass** |
|| 145 | CC-23 respects_difference classifier hardening | already exists in code; doc to bag |
|| 233 | CO-09 LLM compute budget | runaway-cost defence |
|| 232 | CO-25 shared vault protocol | unblocks multi-agent ops |

— Calm, 2026-05-20
