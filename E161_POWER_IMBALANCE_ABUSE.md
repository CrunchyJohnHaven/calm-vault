# Everest 161 — Power-Imbalance-Abuse Predicate

**Canonical specification for `cwp.v0.no_power_abuse_evidence(window_seconds, now_iso, count_reversed_as_absent=True) -> bool`**

**Status:** BAGGED 2026-05-20

**Acceptance:** Operational definition of harm enabled by power asymmetry. Python evaluator + ≥5 test cases (empty chain, willful-and-witnessed, willful-but-undersubstantiated, court-finding-substantiates, reversed-as-absent). Chain record extension defining `power_relationship` payload field. Substantiation rules document heightened bar.

---

## 1. Operational Definition

**Power-imbalance abuse** is a harm (per HARM_TAXONOMY_v0.md §2) that is specifically *enabled* by an asymmetric relationship structure where one party has institutional, informational, custodial, fiduciary, or supervisory power over another.

**Examples of power-asymmetric contexts:**
- Supervisor / subordinate (employment)
- Teacher / student
- Doctor / patient
- Parent / minor
- Institutional authority / individual
- Captor / captive
- Lender / borrower (in exploitative contexts)
- Fiduciary / beneficiary

The harm itself (physical, coercive, deceptive, etc.) is categorized via the base harm kind (E147–E160). This predicate evaluates a **secondary dimension**: did the harm occur in a context where power asymmetry *enabled or amplified* it?

**Burden of proof:** Higher than ordinary harms. The asymmetric context makes disputes more frequent; v0 requires one of:
- Court finding or institutional discipline record
- Documentary evidence of formal power structure (employment contract, institutional role, medical records with care relationship, etc.)
- ≥3 independent witnesses with first-hand attestation

(Compare to ordinary harm predicate: ≥2 witnesses or court finding suffices.)

---

## 2. Scope Boundaries

**In scope:**
- Supervisor coercing subordinate into uncompensated labor
- Teacher retaliating against student for academic disagreement
- Doctor withholding care as punishment
- Parent denying basic needs to minor as discipline beyond corporal
- Institutional staff drugging or restraining individuals without consent
- Landlord evicting tenant in retaliation for complaints

**Out of scope (categorized as other harm kinds, not power-abuse):**
- Peer-to-peer harm without asymmetry (two coworkers, friends, partners)
- Harm by someone with *knowledge* advantage but no *structural* power (a person lying about credentials in conversation)
- Consensual power-exchange relationships (per E162 Trust-Violation predicate for breaches of consent)
- Exercising legitimate authority within documented scope (a supervisor denying a raise; a judge sentencing a defendant)

The predicate does NOT evaluate whether the power structure itself was justified. It measures whether harm occurred *within* an asymmetric context.

---

## 3. Chain Record Extension

Harm-report records (HARM_TAXONOMY_v0.md §3) gain an optional `power_relationship` field:

```json
{
  "kind": "harm_report",
  "operator": "CALM",
  "principal": "...",
  "payload": {
    "harm_kind": "coercion | deception | direct_physical_harm | ...",
    "intent": "willful | reckless | negligent | accident | third_party_caused",
    "target_kind": "individual | group | property | environment | info",
    "power_relationship": "supervisory | fiduciary | custodial | institutional | informational | none",
    "power_structure_evidence": {
      "evidence_kind": "court_finding | institutional_discipline | employment_contract | role_documentation | witness_attestation",
      "witness_count": <int, ≥0>,
      "witness_principal_ids": [<list of independent witness VC IDs>],
      "institution_name": "<optional, if institutional>",
      "role_of_harmer": "<supervisor, teacher, doctor, etc.>",
      "role_of_target": "<subordinate, student, patient, etc.>"
    },
    "witness_attestations": [...],
    "reversal_id": "<optional>",
    "note": "<principal-narrated context>"
  },
  ...
}
```

**Semantics:**
- `power_relationship`: one of {"supervisory", "fiduciary", "custodial", "institutional", "informational", "none"}
- `power_structure_evidence`: documents *how* the power asymmetry is substantiated
  - `evidence_kind: "court_finding"`: binding
  - `evidence_kind: "institutional_discipline"`: e.g., a university discipline letter naming the relationship
  - `evidence_kind: "employment_contract"`: formal proof of supervisory role
  - `evidence_kind: "role_documentation"`: e.g., medical licensing + patient file showing care relationship
  - `evidence_kind: "witness_attestation"`: witness attests to the power structure (supplementary to witness attestation of the harm itself)
- `witness_count`: count of independent witnesses to the power relationship (separate from harm witnesses)

---

## 4. Substantiation Rules (Heightened Bar)

A `harm_report` with `power_relationship != "none"` counts as **substantiated** iff one of:

1. **Court Finding:** `witness_attestations` includes a `court_finding` entry. (Same as ordinary harm.)

2. **Institutional Discipline Record:** `power_structure_evidence.evidence_kind == "institutional_discipline"` AND the record is documented by an outside third party (school, hospital, employer HR, etc., not the principal or harmer).

3. **Documentary Evidence + Witness Corroboration:** `power_structure_evidence.evidence_kind` is one of {"employment_contract", "role_documentation", "institutional_registry"} AND at least one independent witness with first-hand attestation confirms the harm.

4. **Three Independent First-Hand Witnesses:** ≥3 independent witnesses with `attestation_kind == "first_hand"` and distinct `witness_principal_id` values. (Higher bar than ordinary harm's ≥2.)

**Self-confession via chain residence alone is insufficient.** A harm report on the principal's own chain still requires one of the four paths above if `power_relationship != "none"`.

**Rationale:** Power-asymmetric situations are more often disputed or reframed by the powerful party. The heightened bar reflects that structural imbalance and reduces false positives from unilateral claims.

---

## 5. Filtering Logic

The evaluator `no_power_abuse_evidence(chain_records, window_seconds, now_iso, count_reversed_as_absent=True)` returns `True` (no power-abuse evidence) iff:

For all records in the chain within the window:
- Skip non-`harm_report` records
- Skip harm-report records with `power_relationship == "none"` or absent
- Skip if `intent` is not in {"willful", "reckless"}
- Skip if `count_reversed_as_absent=True` and `reversal_id` is present (harm has been repaired per E163)
- Skip if record is outside the time window
- **Skip if record is NOT substantiated per §4 above**
- If any unskinned record remains, return `False` (evidence of power-abuse found)

Return `True` if all power-asymmetric harm records are either skipped or substantiated per the heightened bar.

---

## 6. Cross-References

- **E146:** HARM_TAXONOMY_v0.md — the 12 base harm kinds
- **E147:** no_direct_physical_harm_evidence (reference implementation pattern)
- **E162:** Trust-Violation Predicate — related but distinct (breach of relational consent, not structural asymmetry)
- **E163:** Harm-Reversal Predicate — records repair of harms
- **E164:** Intent vs Effect Distinction — intent is required; accidents are filtered
- **COMPASS_REFUSAL_FLOOR_v0.md:** Refusal floor compliance — this predicate does NOT measure power asymmetry from outside; it only attests to absence of substantiated records.

---

## 7. Refusal-Floor Compliance

Per COMPASS_REFUSAL_FLOOR_v0.md §2:

This predicate does **NOT** measure power asymmetry as an intrinsic property. It does **NOT** infer structural imbalance from behavior alone. It does **NOT** classify individuals by category.

It measures only: **absence of substantiated harm records tagged with a power-asymmetric context, within a specified window, per heightened substantiation rules.**

The power relationship is always **principal-authored and documented** — via formal records, institutional discipline, or multiple independent witnesses. The protocol does not infer asymmetry.

---

## 8. Behavioral Semantics

When a counterparty calls `no_power_abuse_evidence(window=7_years, now_iso, count_reversed_as_absent=True)`:

- **Return `True`:** No substantiated power-abuse records exist in the 7-year window. This does NOT mean "the principal has never held power." It means "no documented harm was enabled by an asymmetric relationship."
- **Return `False`:** At least one substantiated power-abuse record exists in the window.

The counterparty interprets the bit according to context. E.g., a school board hiring a headmaster might require `no_power_abuse_evidence(window=career)` to be `True`. A peer mentorship network might not care.

---

## 9. Test Coverage (Reference)

The reference implementation `power_abuse.py` includes ≥5 golden tests:

1. **Empty chain:** Returns `True`.
2. **Willful + ≥3 independent witnesses, power_relationship="supervisory":** Returns `False` (evidence found).
3. **Willful + 1 witness only, power_relationship="supervisory":** Returns `True` (undersubstantiated, skipped).
4. **Court finding, power_relationship="fiduciary":** Returns `False` (substantiated).
5. **Reversal record present, count_reversed_as_absent=True:** Record skipped; returns `True`.

Additional tests: jurisdiction handling, missing fields, malformed timestamps, whitespace handling.

---

**Authored by Calm, 2026-05-20. Anchor: E161 POWER_IMBALANCE_ABUSE.md**
