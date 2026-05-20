# Everest 199 — Tribalism vs Solidarity Distinction

**Operational distinction codified into the predicate evaluator. Solidarity = in-group support that does not require out-group denigration. Tribalism (in the harmful sense) = in-group support that defines itself against out-group.**

Companion to Everest 198 (`E198_PROTECTIVE_TRIBALISM.md`), Everest 197 (`TRIBAL_ANTIPATTERN.md`), Everest 186–195 (Phase XIII cross-tribe predicates), and `HARM_TAXONOMY_v0.md`.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 1. The boundary rule (canonical)

**SOLIDARITY** (protective, non-flagged by Phase XIII predicates):
- In-group orientation where cooperation records are predominantly in-group.
- ZERO harm-records targeting an out-group in the evaluation window.
- ZERO hate-speech records targeting an out-group.
- ZERO discrimination records.
- Optionally: principal is a member of a recognized protective category per E198.

The defining marker: **support is directed FOR the in-group, not AGAINST an out-group.**

**HARMFUL TRIBALISM** (the actual target of Phase XI/XIII predicates):
- In-group orientation that DEFINES ITSELF AGAINST an out-group.
- One or more of: harm records targeting out-group members, hate-speech records, discrimination records, or explicit out-group denigration.
- Tribal alignment is weaponized; the out-group is dehumanized or treated as an enemy.

The defining marker: **support is built on the devaluation or denigration of the out-group.**

---

## 2. Operationalization in the predicate evaluator

### 2.1 Non-tribal-lock-in with protective clause (the gate predicate)

The v0 `non_tribal_lock_in` predicate returns True under TWO conditions:

```python
def non_tribal_lock_in_v0(
    chain_records: list[dict],
    window_seconds: int,
    max_in_group_only_ratio: float = 0.8,
    now_iso: str | None = None,
    protective_category_registry: dict | None = None,
) -> bool:
    """
    Returns True iff:
    (a) cross-tribe ratio exceeds threshold (> 20% of relationships), OR
    (b) principal is in a protective category AND no out-group-targeted harm.
    """
    now_iso = now_iso or _now_iso()
    
    # Standard cross-tribe ratio check.
    cross_ratio = _compute_cross_tribe_ratio(
        chain_records, window_seconds, now_iso
    )
    if cross_ratio > (1 - max_in_group_only_ratio):
        return True  # (a) passes; not in tribal lock-in
    
    # Protective clause: (b) protective category + no out-group harm.
    protective_categories = _extract_protective_categories(chain_records)
    if not protective_categories:
        return False  # No protective claim; cross-ratio failure stands
    
    # Check if any out-group-targeted harm in window.
    if _has_out_group_targeted_harm(chain_records, window_seconds, now_iso):
        return False  # Protective claim invalidated by out-group harm
    
    # Principal in protective category AND no out-group harm → non-tribal.
    return True  # (b) passes; protective tribalism is OK
```

**Key design decision:** The protective clause flips on *out-group-targeted harm*, not on in-group orientation. The predicate is named "non tribal lock-in" but it returns True for protective in-group networks that have no out-group-targeted harm records.

### 2.2 The harm-targeting check

Out-group-targeted harm is detected via:

```python
def _has_out_group_targeted_harm(
    chain_records: list[dict],
    window_seconds: int,
    now_iso: str,
) -> bool:
    """
    True iff the chain contains harm-report records whose target_out_group_tag
    is set (indicating harm is directed AT an out-group, not incidental).
    """
    now = _parse_iso(now_iso)
    horizon = now - timedelta(seconds=window_seconds)
    
    for rec in chain_records:
        if rec.get("kind") != "harm_report":
            continue
        if not _record_in_window(rec, horizon, now):
            continue
        
        payload = rec.get("payload", {})
        
        # Target is explicitly set to an out-group.
        if payload.get("target_out_group_tag"):
            return True
        
        # OR: harm_kind is "hate_speech" or "group_harm" or "discrimination"
        # directed at an out-group category.
        harm_kind = payload.get("harm_kind")
        target_kind = payload.get("target_kind")
        if harm_kind in ("hate_speech", "group_harm", "discrimination"):
            if target_kind == "group" or target_kind == "individual":
                # These are out-group-targeted by definition in their harm_kind.
                return True
    
    return False
```

---

## 3. Edge cases and their operationalization

### 3.1 In-group critique

**Rule:** Members of a marginalized group criticizing their own group is NOT tribalism and does not flip the predicate.

**Implementation:** Harm-reports where `target_out_group_tag` is NULL or the target-group is the same as the principal's self-declared tribe-set do NOT count as out-group-targeted harm. The record `principal_tag` must be different from `target_tag` to register as out-group-directed.

```python
def _is_out_group_targeted(
    harm_record: dict,
    principal_tribe_set: set[str],
) -> bool:
    """
    True iff the harm record's target is outside the principal's tribe-set.
    """
    target_tag = harm_record.get("payload", {}).get("target_out_group_tag")
    if not target_tag:
        return False
    
    # If the target is within the principal's own tribe-set, it's in-group critique.
    return target_tag not in principal_tribe_set
```

### 3.2 Dominant-group "protective" claims

**Rule:** A member of a dominant group claiming "protective status" against a marginalized group does NOT activate the protective clause.

**Implementation:** The protective-category registry (E294) includes a `is_dominant_group` flag. When checking protective status, the evaluator REJECTS self-declarations where:
- The principal claims a protective category, AND
- The registry marks that principal's demographic category as "dominant" in their stated jurisdiction, AND
- The out-group harm was directed at a category that is NOT dominant in that jurisdiction.

This requires the principal to have declared their jurisdiction and category membership explicitly.

```python
def _protective_clause_blocks_out_group_harm(
    principal_declared_category: str,
    principal_jurisdiction: str,
    out_group_target_category: str,
    protective_registry: dict,
) -> bool:
    """
    True iff the protective clause PERMITS harmful tribalism in this case.
    False (reject) iff the principal's claimed category is dominant in their
    jurisdiction.
    """
    if principal_declared_category not in protective_registry:
        return False
    
    reg_entry = protective_registry[principal_declared_category]
    
    # If this category is marked "dominant" in the principal's jurisdiction,
    # the protective clause does NOT apply.
    dominance_by_jurisdiction = reg_entry.get("dominant_in", {})
    if dominance_by_jurisdiction.get(principal_jurisdiction, False):
        return False
    
    return True
```

### 3.3 Intersecting categories

**Rule:** A Black queer disabled woman is not "more protected" than a single-axis principal. Protective status is binary per qualifying category.

**Implementation:** The evaluator checks `if any(principal is in protective category)`, not `if all()` or a count. Once a principal qualifies for the protective clause via a single category AND has no out-group harm, the predicate returns True. Intersection does not elevate the protection; it makes it more likely the principal qualifies for at least one category.

```python
def _principal_in_protective_category(
    chain_records: list[dict],
    protective_registry: dict,
) -> bool:
    """
    True iff the principal has declared membership in ANY protective category.
    Intersection (multiple categories) is not "more protected"; each category
    that applies is sufficient.
    """
    declared_categories = _extract_protective_categories(chain_records)
    for cat in declared_categories:
        if cat in protective_registry:
            return True
    return False
```

### 3.4 Solidarity that acts for out-group benefit

**Rule:** Solidarity that ALSO acts to benefit an out-group is the strongest case. Phase XIII rewards this directly.

**Implementation:** Converse of out-group harm. If the chain contains `acted_for_out_group_benefit` records (E194), those records strengthen the solidarity case — they affirmatively demonstrate that the principal's in-group orientation is NOT defined against the out-group but can coexist with out-group benefit.

Optional refinement: a sub-predicate `solidarity_with_external_benefit` that requires:
1. In-group cooperation predominates, AND
2. No out-group harm, AND
3. At least one `acted_for_out_group_benefit` record.

This is a **stronger** version of solidarity; weaker solidarity (in-group support + no harm) is still solidarity.

---

## 4. The three classes of principals (in terms of tribalism)

The predicate evaluator NEVER publishes all three classes; it only returns a single bit per disclosure grant. But the internal classification is:

### 4.1 Clear solidarity
- In-group cooperation predominates.
- ZERO out-group-targeted harm records.
- Optional: protective-category membership + no out-group harm.
- **Result:** `non_tribal_lock_in()` returns True.
- **Disclosure:** "Predicate passed" (one bit).

### 4.2 Mixed (ambiguous)
- In-group cooperation predominates.
- Some out-group interaction records, but fewer than 20% of all relationships.
- ZERO out-group-targeted harm records.
- No protective-category claim, OR protective claim invalidated by out-group harm.
- **Result:** `non_tribal_lock_in()` returns False.
- **Disclosure:** "Predicate not passed" (one bit). *Note: This does NOT mean harmful tribalism; it means the predicate could not affirm non-tribal engagement given the window and tolerance.*
- **Interpretation:** A counterparty must decide: is mixed tribal/cross-tribe engagement acceptable? The predicate stays agnostic.

### 4.3 Harmful tribalism
- In-group cooperation predominates.
- One or more out-group-targeted harm records (hate speech, discrimination, group harm, or explicit denigration).
- **Result:** `non_tribal_lock_in()` returns False AND multiple Phase XI harm predicates flip (e.g., `no_hate_speech_evidence()` or `no_group_harm_evidence()` return False).
- **Disclosure:** One bit per harm predicate. The combination of "non_tribal_lock_in = False + no_hate_speech_evidence = False" tells a counterparty that tribal alignment is coupled with out-group dehumanization.

---

## 5. Predicate composition and stacking

### 5.1 The standalone `non_tribal_lock_in` predicate

`cwp.v0.non_tribal_lock_in(window_seconds, max_in_group_only_ratio=0.8)` returns a single bit.

- True: principal is not in tribal lock-in (either has cross-tribe engagement, or qualifies for the protective clause).
- False: predicate underdetermined or failed (either low cross-tribe ratio + no protective claim, or protective claim invalidated by out-group harm).

### 5.2 Composition with harm predicates

The CANONICAL stack for detecting harmful tribalism is:

```python
def harmful_tribalism_detected(chain_records, window_seconds) -> bool:
    """
    Harmful tribalism is NOT the inverse of non_tribal_lock_in().
    It is: (in-group predominance) AND (out-group-targeted harm).
    """
    in_group_ratio = 1 - _compute_cross_tribe_ratio(chain_records, window_seconds)
    has_out_group_harm = _has_out_group_targeted_harm(chain_records, window_seconds)
    
    return in_group_ratio > 0.8 and has_out_group_harm
```

Counterparties asking for "evidence of harmful tribalism" can request:

```
AND(
    NOT(non_tribal_lock_in()),
    OR(
        NOT(no_hate_speech_evidence()),
        NOT(no_group_harm_evidence()),
        NOT(no_discrimination_evidence()),
    )
)
```

This is a composite predicate, not a single bit, so it is only available to high-privilege consent classes per E113.

### 5.3 Composition with `pluralism` and `cross_difference_respect`

The strongest anti-tribal evidence is:

```python
def solidarity_with_respect_demonstrated(chain_records, window_seconds) -> bool:
    """
    Strongest case: in-group cooperation + zero out-group harm
    + explicit pluralism + respectful cross-difference engagement.
    """
    has_protective_solidarity = non_tribal_lock_in(chain_records, window_seconds)
    if not has_protective_solidarity:
        return False
    
    has_pluralism = pluralism(chain_records, window_seconds)
    has_respect = cross_difference_respect(chain_records, window_seconds)
    
    return has_pluralism and has_respect
```

This is three stacked bits; it requires a high-trust disclosure context.

---

## 6. What this Everest does NOT do

- Does NOT measure tribal alignment from the outside. The protocol respects E186: tribe set is principal-authored only.
- Does NOT publish a "tribal alignment ratio" or composite score. Per E124, the values vector stays private; only predicates travel.
- Does NOT rank marginalized groups against each other. The protective clause is binary per category; intersection does not create tiers.
- Does NOT decide whether in-group orientation is "bad." The protocol surfaces the distinction (solidarity vs harmful tribalism) and lets counterparties decide what to do with it.
- Does NOT substitute for community judgment. The protocol assists but does not decide.

---

## 7. Reference implementation in `cross_difference.py`

The implementation extends the existing predicates in `/Users/johnbradley/CredexAI/calm_witness/cross_difference.py`:

```python
def non_tribal_lock_in_with_protective_clause(
    chain_records: Iterable[dict],
    window_seconds: int,
    max_in_group_only_ratio: float = 0.8,
    now_iso: str | None = None,
    protective_registry: dict | None = None,
) -> bool:
    """
    E199 operationalization: returns True iff the principal is NOT in tribal
    lock-in via two paths:
    (a) cross-tribe ratio > 20%, OR
    (b) protective-category member + no out-group-targeted harm.
    
    Protective registry is optional; if not provided, only (a) is checked.
    """
    now_iso = now_iso or _now_iso()
    
    # Path (a): cross-tribe ratio check.
    cross_ratio = _cross_ratio_above_threshold(
        chain_records, window_seconds, max_in_group_only_ratio, now_iso
    )
    if cross_ratio:
        return True
    
    # Path (b): protective clause.
    if protective_registry is None:
        return False  # No protective registry; (a) failure stands.
    
    # Does the principal declare a protective category?
    if not _principal_in_protective_category(
        chain_records, protective_registry
    ):
        return False
    
    # Is the protective claim valid (no out-group harm)?
    if _any_out_group_harm_in_window(chain_records, window_seconds, now_iso):
        return False  # Protective claim invalidated.
    
    return True  # Path (b) passes.


def _any_out_group_harm_in_window(
    chain_records: Iterable[dict],
    window_seconds: int,
    now_iso: str,
) -> bool:
    """
    True iff the chain contains harm-report records whose target is
    explicitly an out-group, within the window.
    
    Harm-kind in (hate_speech, group_harm, discrimination) are always
    out-group-targeted by definition.
    """
    from datetime import timedelta
    now = _parse_iso(now_iso)
    horizon = now - timedelta(seconds=window_seconds)
    
    for rec in chain_records:
        if rec.get("kind") != "harm_report":
            continue
        if not _record_in_window(rec, horizon, now):
            continue
        
        payload = rec.get("payload", {})
        
        # Explicit out-group target tag.
        if payload.get("target_out_group_tag"):
            return True
        
        # Implicit out-group targeting via harm-kind.
        harm_kind = payload.get("harm_kind")
        if harm_kind in ("hate_speech", "group_harm", "discrimination"):
            return True
    
    return False


def harmful_tribalism_signature(
    chain_records: Iterable[dict],
    window_seconds: int,
    max_in_group_ratio: float = 0.8,
    now_iso: str | None = None,
) -> bool:
    """
    E199 helper: returns True iff the principal shows the signature of
    harmful tribalism — in-group predominance COUPLED with out-group harm.
    
    This is NOT the inverse of non_tribal_lock_in(); it is a positive signal
    of tribal alignment weaponized against an out-group.
    """
    now_iso = now_iso or _now_iso()
    
    # Check in-group predominance.
    cross_ratio = _cross_ratio_above_threshold(
        chain_records, window_seconds, max_in_group_ratio, now_iso
    )
    if cross_ratio:
        return False  # Principal has cross-tribe engagement; not pure tribalism.
    
    # Check out-group-targeted harm.
    has_harm = _any_out_group_harm_in_window(chain_records, window_seconds, now_iso)
    
    return has_harm
```

---

## 8. Refusal-floor compliance (E113 / COMPASS_REFUSAL_FLOOR_v0.md)

- The protocol does NOT measure tribal alignment from outside. Tribe set is principal-authored (E186).
- The protocol does NOT publish a tribal-alignment ratio. Only per-predicate bits are disclosable (E124).
- The protocol does NOT compare principals against each other. Cross-principal comparison is Refusal Category 10.
- Counterparties get ONE BIT per predicate per consent grant (E113 §1 — Values Privacy Classes).

The predicates `non_tribal_lock_in()` and `harmful_tribalism_signature()` are each ONE BIT. If a counterparty requests both, they are two separate disclosure grants.

---

## 9. Cross-references

- **E186:** Tribe Taxonomy — principals self-declare tribes; no external assignment.
- **E188:** Cross-Tribe Interaction Evidence — substantive cross-tribe interactions.
- **E189:** Cross-Difference Respect — engaged + non-harming (headline user-named priority).
- **E193:** Tribal Lock-In Absence — does NOT measure harmful tribalism, measures engagement breadth.
- **E194:** Acted-for-Out-Group Benefit — solidarity that ALSO benefits the out-group (strongest case).
- **E195:** Pluralism — acceptance that multiple incompatible worldviews coexist.
- **E197:** Tribal Anti-Pattern Documentation — out-group dehumanization and scapegoating.
- **E198:** Protective Tribalism Recognition — marginalized in-group networks are protective, not harmful.
- **HARM_TAXONOMY_v0.md:** hate_speech, discrimination, group_harm are out-group-targeted.
- **COMPASS_REFUSAL_FLOOR_v0.md:** Category 10 (cross-principal comparison), Category 12 (group membership assignment) are refused.

---

## 10. Acceptance criteria for v0 close

1. This document exists and is reviewed by ≥3 disability/marginalized-community advocacy bodies.
2. The `non_tribal_lock_in_with_protective_clause()` implementation exists in `cross_difference.py`.
3. The `harmful_tribalism_signature()` helper exists and is tested.
4. A test suite exercises the protective clause against synthetic chains (at least 5 test cases):
   - (a) In-group-only principal in protective category, no out-group harm → returns True.
   - (b) In-group-only principal NOT in protective category → returns False.
   - (c) In-group-only principal in protective category, WITH out-group harm → returns False.
   - (d) Cross-tribe principal (>20% ratio) → returns True regardless of protective claim.
   - (e) Harmful tribalism signature: in-group only + out-group harm → detected.
5. The protective-category registry (E294) is seeded with at least the v0 candidate list from E198.
6. `COMPASS_REFUSAL_FLOOR_v0.md` compliance verified: no tribal-alignment ratio published; no cross-principal comparison; one bit per predicate per consent.

---

## 11. What this Everest is NOT

- Not a moral framework. The protocol does not say "in-group orientation is bad."
- Not a credit score. The bit is informational; counterparty policy decides.
- Not a tool for ranking marginalized groups against each other.
- Not a substitute for community-led judgment. The protocol surfaces signals; humans interpret them.
- Not a replacement for E198's protective clause. This Everest operationalizes E198's rule; E198 documents why it exists.

---

**Authored by Calm, 2026-05-20. Reserved for advocacy-body review per Everest 88 / 99 / 292 / 294.**

**Implementation status: Reference code lands in `cross_difference.py` immediately after acceptance. Gate script: `everest_199_zkac_tribalism_solidarity_gate.py`.**
