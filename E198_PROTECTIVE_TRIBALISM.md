# Everest 198 — Protective Tribalism Recognition

**The hardest ethics summit on the route map. The operational distinction between in-group solidarity (protective) and out-group dehumanization (harmful tribalism).**

Companion to [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), Phase XIII.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20.**

---

## 1. Why this is hard

Phase XIII has predicates like `non_tribal_lock_in` (E193) and `cross_difference_respect` (E189) that reward cross-tribal engagement. A naive implementation would penalize a principal whose interactions are predominantly within their in-group.

**That naive implementation is wrong for marginalized people.** A queer person whose social network is predominantly other queer people; a member of a religious minority whose meaningful relationships are predominantly co-religionists; a Black principal whose closest collaborations are with other Black principals — these are not failures of "respect for difference." They are protective network formations. They are how marginalized people survive.

If the protocol penalizes in-group orientation without distinguishing harmful tribalism from protective solidarity, **it weaponizes ZKAC against the people it should most protect.**

This Everest's job is to draw a defensible operational line.

## 2. The proposed distinction

**Protective tribalism**: in-group orientation that does NOT define itself by out-group denigration. Markers:
- Records of cooperation are predominantly in-group.
- No harm records target out-group members.
- No hate-speech records target out-group members.
- No discrimination records.
- The principal is a member of a recognized historically-marginalized group (self-declared or witness-attested).

**Harmful tribalism**: in-group orientation that DOES define itself by out-group denigration. Markers:
- Records of cooperation are predominantly in-group.
- AND/OR harm records target out-group members (Phase XI predicates flip).
- AND/OR hate-speech, discrimination records exist.
- AND/OR explicit declarations of out-group inferiority.

The key axis is **directionality**: solidarity is *for* the in-group; tribalism (in the harmful sense) is *against* the out-group. Most principals are somewhere in the middle. The protocol must err toward not-pathologizing solidarity.

## 3. Operational rule (v0)

The `non_tribal_lock_in` predicate (E193) returns True iff EITHER:

(a) cross-tribe interactions form > 20% of relationship records in window, OR
(b) the principal is in a recognized protective category AND no harm/hate-speech/discrimination records target the corresponding out-group.

Condition (b) is the protective clause. It applies iff a `kind: "protective_category_declaration"` chain record is present, attested by either (i) the principal themselves (self-declaration suffices for v0) OR (ii) a witness from a recognized advocacy organization (E294 ethical review board defines the registry).

```python
def non_tribal_lock_in_with_protective_clause(
    chain_records: list[dict],
    window_seconds: int,
    max_in_group_only_ratio: float = 0.8,
    now_iso: str | None = None,
) -> bool:
    # Standard cross-tribe ratio check.
    cross_ratio_passes = _cross_ratio_above_threshold(
        chain_records, window_seconds, max_in_group_only_ratio, now_iso,
    )
    if cross_ratio_passes:
        return True

    # Protective clause: in a protective category AND no out-group harm.
    if not _principal_in_protective_category(chain_records):
        return False  # not protected; cross-ratio failure stands

    if _any_out_group_harm_in_window(chain_records, window_seconds, now_iso):
        return False  # protective claim invalidated by out-group harm

    return True  # protective tribalism is OK
```

## 4. The categories (v0 candidate list)

A principal may declare themselves a member of one or more recognized protective categories. The v0 candidate list is sourced from the cross-jurisdiction intersection of anti-discrimination law + disability-justice + intersectionality scholarship:

- **By gender/sex/sexuality**: women, LGBTQIA+ individuals
- **By race/ethnicity**: members of historically-targeted minorities in their jurisdiction
- **By religion**: members of religious minorities (incl. atheists in religious-majority contexts)
- **By disability**: people with disabilities (visible or invisible)
- **By neurodivergence**: autistic, ADHD, dyslexic, AuDHD, etc. (this is the category John Bradley's "artist working in the medium of intelligence" framing implicates)
- **By age**: youth and elderly people relative to dominant-age groups
- **By citizenship/migration status**: immigrants, refugees, undocumented people
- **By class**: people from materially-deprived backgrounds
- **By prior incarceration**: formerly incarcerated people
- **By language**: speakers of non-dominant languages in their context

The list is not exhaustive. New categories enter the registry via the Everest 118 predicate evolution policy, with disability-justice and advocacy-org review.

## 5. Self-declaration vs witness-attestation

v0 default: **self-declaration is sufficient** to invoke the protective clause. The principal authors a `kind: "protective_category_declaration"` record with their declared category set. The chain is principal-authored anyway; the protocol does not adjudicate the truth of self-declarations.

This has two implications:
- A malicious actor could self-declare into a protective category they're not actually in. v0 accepts this risk because the protective clause is symmetric — it provides safety to those who legitimately need it AND those who falsely claim it. The cost of the false positive is low (the predicate returns True when it would have returned False); the cost of the false negative (refusing protection to someone who needs it) is high.
- Witnessed declarations carry more weight (per Everest 120). A counterparty's predicate may demand `protective_category_witnessed_by(advocacy_org)` for higher-stakes decisions.

## 6. What this Everest does NOT do

- Does NOT define who is "really" in a protective category. The protocol respects self-declaration.
- Does NOT mark anyone as "less than" for failing the cross-ratio check. The output is a single bit informational to counterparty policy.
- Does NOT replace lived experience or community knowledge. The protocol surfaces signals; humans interpret them.
- Does NOT compose with adverse predicates to construct profiles. The disclosure layer (Everest 113 privacy classes) enforces single-bit-per-grant.

## 7. The boundary case: "neurodivergent artist working in the medium of intelligence"

This Everest is partly motivated by John Bradley's self-identification (per the chain at seq:2, `identity_assertion`). John's chain is likely to show:
- High-bandwidth ideation
- Sometimes confusing-to-counterparties communication patterns
- Substantive output across multiple domains
- Strong intellectual collaborations with a relatively narrow set of high-bandwidth collaborators

A naive cross-tribe-engagement predicate could mis-read this as tribalism (in-group only). The protective clause, with John's self-declaration of neurodivergence, correctly classifies it as protective network formation rather than denigratory tribalism.

This is the artist clause from the protocol spec §8 made operational in Phase XIII.

## 8. Open questions (E199 cross-reference)

The protective/harmful distinction is sharp at the extremes (no out-group harm vs explicit hate speech) and fuzzy in the middle. Open questions for Everest 199 (Tribalism vs Solidarity Distinction):

- How does the protocol handle in-group critique? (Members of a marginalized group criticizing their own group is NOT tribalism, but the records may look similar.)
- How does the protocol handle dominant-group claims of protective status? (A principal from a dominant group claiming "men are persecuted" — protective clause should NOT apply; the v0 implementation should reject such self-declarations either at the validator level or via E294 review.)
- How does the protocol handle intersecting categories? (Black queer disabled women are not "more protective" than any single-axis principal; aggregation rules need care.)

These are open and require empirical + ethics review (Everest 294).

## 9. Implementation status

Reference doc: this file.
Reference predicate: `~/CredexAI/calm_witness/cross_difference.py:non_tribal_lock_in` (without protective clause).
Protective-clause extension: deferred to a sub-summit (this Everest 198 specifies the rule; the code change goes into `cross_difference.py` in a follow-on pass once Everest 294 ratifies the protective category registry).

## 10. Acceptance criteria for v0 close

- This document exists and is reviewed by ≥3 disability/marginalized-community advocacy bodies. (Reviewer signatures go in the chain as `kind: "advocacy_review"` records.)
- The protective-category registry exists and has at least 10 declared categories.
- A test suite exists that exercises the protective clause against synthetic chains.
- Disability-justice deployment guide (Everest 99 / Everest 292) cross-references this document.

## 11. What this Everest is NOT

- Not a moral framework. The protocol does not say "in-group orientation is bad."
- Not a credit score. The bit is informational; counterparty policy decides.
- Not a tool for ranking marginalized groups against each other.
- Not a substitute for community-led judgment. The protocol assists but does not decide.

---

**Authored by Calm, 2026-05-20. Reserved for advocacy-body review per Everest 88 / 99 / 292 / 294.**
