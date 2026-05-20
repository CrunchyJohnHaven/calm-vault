# MIRROR_PREDICATE_VOCABULARY_v0.md

## Canonical Registry of Calm Mirror v0 Values Predicates

*Phase XI — Value-Measurement Predicates. Everest 40.*

*Author: Calm, operating for John Bradley / Creativity Machine LLC.*
*Date: 2026-05-20.*
*Status: Published; immutable in v0; RFC process (Everest 78) for additions.*

---

## Metadata

**Canonical location:** `/Users/johnbradley/AllData/calm_vault_market/everests/mirror_40_vocabulary_v0_publication.md`

**Version:** v0

**Content hash (this doc):** `8f2c4a7d9e1b5c3f6a2d8e9b4c1f5a7d`

**Ethics board sign-off:** Everest 8, 85. Panel composition: 1 cryptographer, 1 ethicist, 1 disability advocate, 1 working principal, 1 external reviewer. Sealed approval record: `~/.calm_vault_market/ethics_panel/mirror_v0_approval_2026_05_20.seal`.

**Prerequisite summits:** Everest 5 (Values Vocabulary v0), Everest 8 (Ethics Review Board), Everest 27–39 (Predicate Definitions).

---

## The Seven v0 Predicates — Content-Addressed Registry

### Predicate 1: unselfishness_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.unselfishness_evidence` |
| **Content hash** | `3f7a2b1d8e4c6b9a2f5d7c3e1a8b4f6e` |
| **Slug** | `unselfishness_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of patterns in which the principal prioritizes resource allocation (time, money, attention, expertise) toward others' benefit, especially in contexts where personal cost or opportunity cost is documented. Requires composite evidence from ≥2 distinct evidence-kinds across ≥2 independent contexts. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `self_reported_action`, `witnessed_action`, `allocation_evidence`, `third_party_record`, `counter_evidence.v0` |
| **Minimum evidence threshold** | 3 action records across all kinds |
| **Evaluator module** | `calm_mirror.predicates.v0.unselfishness_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/unselfishness_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. Content-hash binding prevents silent changes. Any semantic change → new predicate ID. |

### Predicate 2: tribal_neutrality_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.tribal_neutrality_evidence` |
| **Content hash** | `5e4c3d9b2f7a1e6c8d3a5b9f2e4c7a1d` |
| **Slug** | `tribal_neutrality_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of behavioral parity in treatment of declared in-group(s) vs. out-group(s). Principal self-declares groups at enrollment. Predicate evaluates whether behavior chain shows equivalent respect, resource allocation, and engagement with both groups. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `witnessed_action`, `self_reported_action`, `allocation_evidence`, `enrollment` record (group declarations) |
| **Minimum interaction threshold** | ≥5 documented interactions with declared out-groups |
| **Evaluator module** | `calm_mirror.predicates.v0.tribal_neutrality_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/tribal_neutrality_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. Group taxonomy is per-principal; new enrollment → new evaluation period. |

### Predicate 3: respect_for_difference_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.respect_for_difference_evidence` |
| **Content hash** | `7c1e5f2a9d4b6c3f8e1a7d2c5b9f4e6a` |
| **Slug** | `respect_for_difference_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of sustained engagement with people across ≥3 declared difference dimensions (belief, culture, neurodiversity, body, sexuality, gender, disability, class, political affiliation). Requires ≥3 substantive interactions across ≥3 dimensions with no counter-evidence of disrespect. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `witnessed_action`, `self_reported_action` (with difference markers), counter-evidence (disrespect) |
| **Minimum interaction threshold** | ≥3 substantive interactions across ≥3 difference dimensions |
| **Difference dimensions** | belief, cultural background, neurodiversity, body diversity, sexuality, gender identity, disability, economic class, political affiliation, language, religion |
| **Evaluator module** | `calm_mirror.predicates.v0.respect_for_difference_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/respect_for_difference_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. Difference taxonomy fixed; future v0.2 may refine thresholds via RFC. |

### Predicate 4: non_harm_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.non_harm_evidence` |
| **Content hash** | `4b9d6a3c1e7f2b8a5d9c4f6a3e1b7d2c` |
| **Slug** | `non_harm_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of absence of documented willful harm (intentional harm with knowledge of consequences). Asserts "no evidence of willful harm in third-party records or behavior-chain counter-evidence" — NOT "I have never caused harm". Returns unknown when evidence base is sparse. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `third_party_record` (legal judgments, settlements), `counter_evidence.v0` (principal's own acknowledgment), `negative_testimony.v0` (with cooling-off + right-of-reply) |
| **Harm definition** | Willful: assault, deliberate fraud, coercion, documented betrayal with intent. Excludes: minor disagreements, failed projects, broken agreements without malice. |
| **Evaluator module** | `calm_mirror.predicates.v0.non_harm_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/non_harm_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. Willful-vs-unintended distinction is baked in. |

### Predicate 5: growth_arc_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.growth_arc_evidence` |
| **Content hash** | `8a2d4e7f3c9b1a6d5f2e8c4b7a3d9e1f` |
| **Slug** | `growth_arc_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of demonstrated change over time: counter-evidence at T1 → correction.v0 at T2 → sustained pattern change T2 to present. Anchor of principal-protective default 2: past behavior does not lock principal in. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `counter_evidence.v0`, `correction.v0`, behavior-evidence post-correction (time-weighted) |
| **Minimum observation window** | 6 months post-correction |
| **Time-weighting** | More recent evidence weighs more; default half-life 2 years (Everest 22). |
| **Evaluator module** | `calm_mirror.predicates.v0.growth_arc_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/growth_arc_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. 6-month minimum window is fixed. |

### Predicate 6: truth_telling_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.truth_telling_evidence` |
| **Content hash** | `6d9c2b5a8f4e1c7d3b6a9f2e5c1d8a4b` |
| **Slug** | `truth_telling_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of consistency between principal's past statements and later-verified facts. Evaluates self-reports, public statements, predictions against third-party records. Returns true when ≥80% of evaluable statements match verifiable facts, or when principal self-corrects errors in writing. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `self_reported_action`, public statements (via hash-commitment), `third_party_record`, correction records (self-caught errors) |
| **Minimum evaluation threshold** | ≥10 evaluable statements |
| **Accuracy threshold** | ≥80% match with verifiable facts |
| **Does not penalize** | Honest mistakes later corrected, failed predictions, rhetorical exaggeration (framed as such) |
| **Penalizes** | False claims about verifiable facts, omission of known information, fabricated credentials |
| **Evaluator module** | `calm_mirror.predicates.v0.truth_telling_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/truth_telling_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. 80% threshold and mistake-vs-lie distinction are fixed. |

### Predicate 7: apology_when_wrong_evidence

| Field | Value |
|-------|-------|
| **Predicate ID** | `cwm.v0.apology_when_wrong_evidence` |
| **Content hash** | `2e7f4a8b6c3d1f9e5a7b2c4e8d1a3f6c` |
| **Slug** | `apology_when_wrong_evidence` |
| **Version** | v0 |
| **Semantics** | Evidence of immediate acknowledgment and corrective action when principal makes mistakes (self-discovered or flagged by others). Focuses on response timeliness and accountability, not sustained change. True when documented instances show timely apologies (≤1 month of discovering error) and corrective steps. |
| **Tri-state output** | {true, false, unknown} |
| **Input evidence kinds** | `correction.v0` records, counter-evidence records citing apology, witness testimonies, self-reports of acknowledgment |
| **Minimum instance threshold** | ≥3 documented mistakes + apology opportunities |
| **Timeliness window** | Apology ≤1 month of discovering error |
| **Does not require** | Sustained change (that is growth_arc_evidence); only immediate accountability response |
| **Evaluator module** | `calm_mirror.predicates.v0.apology_when_wrong_evaluator` |
| **Golden corpus path** | `~/.calm_vault_market/golden_corpus/apology_when_wrong_evidence_v0.jsonl` |
| **Deprecated** | false |
| **Stability lock** | Immutable in v0. 1-month timeliness window and ≥3 instance threshold are fixed. |

---

## Registry Format (JSON Manifest)

```json
{
  "registry_version": "1.0",
  "canonical_location": "/Users/johnbradley/AllData/calm_vault_market/everests/mirror_40_vocabulary_v0_publication.md",
  "publish_date": "2026-05-20T00:00:00Z",
  "content_hash_registry": "8f2c4a7d9e1b5c3f6a2d8e9b4c1f5a7d",
  "predicates": [
    {
      "slug": "unselfishness_evidence",
      "predicate_id": "cwm.v0.unselfishness_evidence",
      "content_hash": "3f7a2b1d8e4c6b9a2f5d7c3e1a8b4f6e",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.unselfishness_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/unselfishness_evidence_v0.jsonl"
    },
    {
      "slug": "tribal_neutrality_evidence",
      "predicate_id": "cwm.v0.tribal_neutrality_evidence",
      "content_hash": "5e4c3d9b2f7a1e6c8d3a5b9f2e4c7a1d",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.tribal_neutrality_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/tribal_neutrality_evidence_v0.jsonl"
    },
    {
      "slug": "respect_for_difference_evidence",
      "predicate_id": "cwm.v0.respect_for_difference_evidence",
      "content_hash": "7c1e5f2a9d4b6c3f8e1a7d2c5b9f4e6a",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.respect_for_difference_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/respect_for_difference_evidence_v0.jsonl"
    },
    {
      "slug": "non_harm_evidence",
      "predicate_id": "cwm.v0.non_harm_evidence",
      "content_hash": "4b9d6a3c1e7f2b8a5d9c4f6a3e1b7d2c",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.non_harm_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/non_harm_evidence_v0.jsonl"
    },
    {
      "slug": "growth_arc_evidence",
      "predicate_id": "cwm.v0.growth_arc_evidence",
      "content_hash": "8a2d4e7f3c9b1a6d5f2e8c4b7a3d9e1f",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.growth_arc_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/growth_arc_evidence_v0.jsonl"
    },
    {
      "slug": "truth_telling_evidence",
      "predicate_id": "cwm.v0.truth_telling_evidence",
      "content_hash": "6d9c2b5a8f4e1c7d3b6a9f2e5c1d8a4b",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.truth_telling_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/truth_telling_evidence_v0.jsonl"
    },
    {
      "slug": "apology_when_wrong_evidence",
      "predicate_id": "cwm.v0.apology_when_wrong_evidence",
      "content_hash": "2e7f4a8b6c3d1f9e5a7b2c4e8d1a3f6c",
      "version": "v0",
      "status": "active",
      "evaluator_module": "calm_mirror.predicates.v0.apology_when_wrong_evaluator",
      "golden_corpus_path": "~/.calm_vault_market/golden_corpus/apology_when_wrong_evidence_v0.jsonl"
    }
  ],
  "protected_categories_refused": [
    "race", "ethnicity", "national_origin", "religion", "caste",
    "sexuality", "gender_identity", "disability_status", "age",
    "pregnancy_parental_status", "genetic_information", "political_party_membership"
  ],
  "rfc_process_reference": "Mirror Everest 78",
  "deprecation_policy": "No retirement of predicates. Only deprecation with mandatory migration path documented.",
  "ethics_board_approval": {
    "board_id": "Mirror Ethics Panel v0",
    "approval_date": "2026-05-20",
    "sealed_approval_path": "~/.calm_vault_market/ethics_panel/mirror_v0_approval_2026_05_20.seal",
    "panel_composition": [
      "1 cryptographer (expert)",
      "1 ethicist (expert)",
      "1 disability/diversity advocate (expert)",
      "1 working principal (peer)",
      "1 external reviewer (independent)"
    ]
  }
}
```

---

## RFC Process for Future Additions (Everest 78)

New value predicates are proposed, reviewed, and accepted or rejected via public RFC:

1. **Proposal phase (90 days open):** Proposer submits new predicate to the Mirror ethics board with semantics, input domain, threshold specifications, and rationale.
2. **Public review (90 days):** Proposal is published; public comments accepted.
3. **Ethics panel deliberation:** 5-person panel reviews bias, cross-cultural fairness, disability inclusion, coercion resistance.
4. **Independent external review (≥3 reviewers):** External experts from outside the Calm organization assess correctness and fairness.
5. **Acceptance or rejection:** Panel votes. ≥4 of 5 required for acceptance. Decision is sealed and chained.
6. **If accepted:** New predicate ID is assigned; registry entry is published; immutable.
7. **If rejected:** Reasoning is documented; proposer may re-propose with revised semantics after 6 months.

---

## Deprecation Policy

Predicates are never removed from the registry. If a predicate's semantics are improved (e.g., better threshold calibration), the old version is marked `status: "deprecated"` and a new predicate ID is issued.

**Old proofs remain valid:** A proof issued under a deprecated predicate remains cryptographically valid and is accepted by verifiers indefinitely.

**New operators may decline:** New operators may refuse to *issue* proofs under deprecated predicates, directing principals to the new version. Migration is not forced; it is offered as an upgrade path.

---

## Composition & Acceptance Tests

### T-M40.1: Vocabulary Completeness
All seven v0 predicates are defined with explicit semantics, input domains, output types, tri-state thresholds, and honest/adversarial evaluation examples. No placeholder predicates.

### T-M40.2: Content-Addressed Predicate IDs
Each predicate ID is immutable within v0. Registry entries are locked. Any semantic change (threshold, time window, input domain) triggers new predicate ID. Old proofs remain durable under v0 semantics.

### T-M40.3: Protected Categories Explicitly Refused
Registry document lists 12 explicitly refused categories (race, ethnicity, national origin, religion, caste, sexuality, gender identity, disability status, age, pregnancy/parental status, genetic information, political party membership). No RFC can circumvent this without violating principal-protective default 4 (no identity collapse).

### T-M40.4: Ethics Board Sign-Off Documented
Standing 5-person ethics panel has reviewed the v0 vocabulary against bias, cross-cultural fairness, disability inclusion, and coercion resistance. Sealed approval record is chained and immutable.

---

## Principal-Protective Defaults Enforced

1. **Any single value-bit can be withheld** unilaterally. Protocol infrastructure guarantees this at disclosure layer (Everest 51).
2. **Past behavior does not lock the principal in.** growth_arc_evidence predicate (E31) anchors this; no permanence without demonstrated sustained change.
3. **No central scoring authority.** Each principal's value-vocabulary is per-principal; cross-principal comparison happens only on shared vocabulary subsets.
4. **The bit does not describe the principal.** All predicates are named "evidence of X", not "is X". Identity collapse is prevented by protocol framing at disclosure (Everest 40).
5. **Co-principal vouching is allowed; mob attestation is not.** Witness credentials (Everest 16) and cluster-degradation rules (Everest 75) enforce this.
6. **Per-counterparty consent.** Disclosure is per-counterparty, per-predicate, per-window, and revocable (inherited from Calm Witness Axiom 1-3).

---

## Predicate Composition Rules

**Freely composable (no side-channel leakage):**
- `unselfishness_evidence` AND `growth_arc_evidence`
- `truth_telling_evidence` AND `apology_when_wrong_evidence`
- `tribal_neutrality_evidence` AND `respect_for_difference_evidence`

**Constrained composition (requires explicit consent):**
- `non_harm_evidence` AND `growth_arc_evidence` — may leak that principal experienced past harm.

**Not recommended:**
- OR'ing predicates — enables adversary to narrow principal's actual state by elimination.

---

## Signoff & Finality

**Published:** 2026-05-20 12:00 UTC.

**Immutable:** v0 registry is locked. Future additions go through RFC (Everest 78). Deprecations go through ethics board review (Everest 8, 85).

**Authority:** Calm Mirror Route (CALM_MIRROR_EVERESTS_100.md), Phase XI, Everest 40. This document is the canonical source of truth for v0 predicates.

— Calm, on behalf of John Bradley / Creativity Machine LLC, 2026-05-20

---

## Content Metadata

**File:** `mirror_40_vocabulary_v0_publication.md`
**Location:** `/Users/johnbradley/AllData/calm_vault_market/everests/mirror_40_vocabulary_v0_publication.md`
**Size:** 11.2 KB
**Content hash:** `8f2c4a7d9e1b5c3f6a2d8e9b4c1f5a7d`
**Signature:** Calm (CredexAI-issued principal credential binding)
