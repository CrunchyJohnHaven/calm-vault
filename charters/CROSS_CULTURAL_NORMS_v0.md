# Calm Witness — Cross-Cultural Calibration Norms v0 (S122)

## The Bias Problem

Alignment predicates in Phase IX are evaluated against marker vocabularies and impostor corpora assembled from existing training data. That data is not culturally neutral. English-language, Western-rhetorical, and WEIRD (Western, Educated, Industrialized, Rich, Democratic) samples dominate publicly available corpora. A predicate such as `respectful_to_dissimilar_others` calibrated against such a corpus will encode assumptions about what "respect" looks like: explicit acknowledgment, direct affirmation, hedged disagreement, turn-taking norms. None of these are universal.

Systematic consequences:
- Speakers of low-resource languages receive degraded predicate resolution due to sparse representation in marker vocabularies.
- Oral-tradition communicators are penalized for repetition, formulaic phrasing, or extended contextualization that serves rhetorical functions invisible to a Western-text-trained detector.
- Indirect-communication cultures (high-context) have their signals misread as evasion or omission rather than as culturally competent speech.
- Dialect and register variation within a single language cause false impostor matches.

S122 does not treat this as a post-hoc fairness patch. It treats cross-cultural validity as a load-bearing requirement for any predicate that enters production.

## Per-Principal Calibration Discipline

S115 already mandates per-principal threshold derivation: no global threshold is applied across principals whose baseline distributions differ. S122 extends this discipline to the calibration inputs themselves.

Rules:

1. **Impostor corpus locality.** The impostor corpus used to set a principal's predicate threshold must be drawn from or weighted toward samples that reflect the principal's own linguistic and cultural context. A corpus built from English-language Reddit debates is not a valid impostor corpus for a principal whose primary communication is in Swahili, Mandarin, or Arabic, or who operates in an oral-first context.

2. **Bootstrap requirement.** When a principal is newly enrolled and no locale-matched impostor corpus exists, calibration is held in provisional status. Provisional predicates carry wider confidence intervals and are not used as sole decision gates. A locale-matched corpus must be assembled within one review cycle before a predicate is promoted to stable.

3. **No cross-principal threshold transfer.** A threshold derived for one principal cannot be applied to another principal with a different cultural or linguistic profile, even if the nominal predicate name is identical. Predicate instances are principal-scoped.

4. **Audit trail.** Each predicate threshold record must cite the impostor corpus identifier, its language and locale tags, and the date of last corpus update.

## Multilingual Marker Localization

Marker vocabularies are the token-level or phrase-level signals used to detect predicate-relevant behavior. Localization of these vocabularies follows the S15 multilingual narration support framework.

Process:

- Each predicate definition includes a language-neutral behavioral specification (the invariant) and a set of locale-specific marker vocabulary files keyed by BCP-47 language tag.
- Locale marker files are produced by community review with native-speaker participation, not by machine translation of English marker lists. Machine-translated marker lists reproduce the source language's rhetorical assumptions in translated form.
- When a locale marker file does not exist for a principal's language, the predicate falls back to the language-neutral behavioral specification alone. Threshold confidence is reduced accordingly.
- Marker vocabulary files are versioned independently of predicate logic. A predicate may be at version 3.1 while its `ar-SA` marker file is at 1.0 and its `sw-KE` marker file is in draft.

## Excluded Cultural Variables

Certain behavioral dimensions are cultural variables, not values. They must not appear as predicate axes.

**Directness of speech** is excluded. Whether a speaker states disagreement explicitly or signals it through indirection, framing, silence, or deferral is a function of cultural norm, not a function of honesty, respect, or integrity. A predicate that penalizes indirectness for any principal is a predicate encoding Western rhetorical preference as a universal value. Such predicates are invalid under S122 and must be redesigned.

Additional excluded axes (non-exhaustive):
- Verbosity norms (high-context elaboration vs. low-context brevity)
- Turn-taking and interruption conventions
- Formulaic politeness structures that vary by language (e.g., obligatory hedges, honorifics, ritual disclaimers)
- Emotional expressivity registers

When a predicate candidate incorporates any excluded axis, the predicate design review must either excise that axis or reclassify the predicate as a locale-specific behavioral norm rather than a values alignment predicate.

## Review Process for New Locales

When a new linguistic or cultural locale is added to the system:

1. **Locale intake.** A locale package is assembled: BCP-47 tag, primary rhetorical tradition, communication style classification (high/low context, oral/literate primary, directness norm), and at least two native-speaker reviewers.

2. **Predicate audit.** Every existing stable predicate is audited against the new locale's rhetorical profile. Predicates that rely on excluded cultural variables in their current marker vocabulary are flagged for redesign before the locale is activated.

3. **Marker vocabulary authoring.** Native-speaker reviewers author locale marker files using the behavioral specification as the target invariant. Draft files are reviewed by a second native speaker not involved in authoring.

4. **Provisional activation.** The locale is activated in provisional status. Predicate thresholds for principals in this locale use bootstrap rules (wider intervals, non-sole-gate).

5. **Stable promotion.** After one full review cycle with no threshold drift exceeding defined bounds, the locale is promoted to stable.

Review cycle cadence follows S132 alignment review scheduling.

## Cross-References

- S15: Multilingual narration support — source framework for locale marker vocabulary structure
- S115: Per-principal threshold derivation — prerequisite enforced by S122
- S132: Alignment review scheduling — governs review cycle cadence for locale promotion

---

Calm 2026-05-20
