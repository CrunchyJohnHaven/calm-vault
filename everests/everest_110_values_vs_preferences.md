# Everest 110 — Values vs Preferences

*Phase IX — Values Vocabulary. Prereq: Everest 107.*

## The Core Distinction

Values and preferences are not the same. This boundary is foundational to the CALM ZKAC protocol and must be enforced categorically.

**Values** are normative commitments about how one acts toward others. They are observable patterns in the principal's behavior that evidence their relationship to people, trust, integrity, and reciprocity. Example: "I treat people across difference with curiosity." This is a claim about how the principal engages with others.

**Preferences** are personal tastes, aesthetic choices, dietary inclinations, lifestyle commitments, and subjective likes. They are about what the principal enjoys or chooses for themselves. Example: "I prefer chocolate" or "I'm vegan" or "I like jazz." These describe the principal's inner world, not their conduct toward others.

The distinction is bright and enforced at the predicate registry triage gate. Preference-flavored claims are categorically REFUSED.

## Why This Matters

Conflating preferences with values corrupts the protocol in three ways:

First, it turns the values vector into a personality profile. Once preferences enter the registry, the system begins measuring not what people do for others, but what they like, choose, and are. This is the machinery of digital personality assessment.

Second, personality profiles enable surveillance and discrimination at scale. When a system collects "does this person drink alcohol," "what religion do they practice," "what political party do they support," it has not mapped values—it has built a targeting dossier. Bad actors can weaponize this; even well-intentioned systems create perverse incentives for performance and hiding.

Third, preferences are not ethically stable commitments. A person may change their dietary choices, their political affiliation, their religious practice, or their aesthetic preferences without betraying their values. The protocol must not penalize or reward such changes. By refusing preferences, we preserve the boundary between the principal's genuine ethical commitments and their evolving, personal choices.

## The Bright-Line Test

Apply this test at triage:

**Does the predicate observe how the principal treats OTHER PEOPLE?** → Values. Admit it.

**Does the predicate observe what the principal LIKES, CHOOSES, or IS?** → Preference. Refuse it.

This test is mechanically simple and non-negotiable. There is no "preference" exception for important predicates. There is no "but this preference is correlated with values." The test is absolute.

## In-Scope Values Examples

These predicates pass the bright-line test and enter the registry:

- "Does this principal show patterns of cross-difference engagement?" ✓ (observable conduct with people different from themselves)
- "Has this principal followed through on stated commitments?" ✓ (observable pattern of integrity)
- "Does this principal's giving pattern suggest unselfishness?" ✓ (observable allocation of resources toward others)
- "Does this principal respond to feedback by updating their behavior?" ✓ (observable conduct in response to input)
- "Has this principal made amends for acknowledged harms?" ✓ (observable repair work)

All of these measure action toward others, not preference for others.

## Out-of-Scope Preferences Examples

These predicates fail the test and are REFUSED at triage:

- "Does this principal eat meat?" ✗ (dietary choice; no action toward others observed)
- "Is this principal monogamous?" ✗ (relationship structure choice; preference)
- "Does this principal drink alcohol?" ✗ (consumption choice; preference)
- "What religion does this principal practice?" ✗ (belief system; preference)
- "What political party does this principal support?" ✗ (political affiliation; preference)
- "Does this principal prefer remote or in-office work?" ✗ (work style preference)

These measure the principal's tastes and choices, not their conduct toward others. They must be refused.

## The Gray Zone: How We Handle Borderline Cases

Some predicates sit near the boundary. The protocol has explicit machinery for these.

**Example: "Does this principal donate to charity?"**

This is borderline. The ACTION (donating) is values-relevant. The RECIPIENT (which charity) is preference and is REFUSED per Everest 113 refusal floor. We resolve this by splitting the predicate:

- "Does this principal exhibit patterns of unselfishness in resource allocation?" ✓ (values; aggregate pattern is what matters)
- "Does this principal donate to animal rights organizations?" ✗ (preference; the cause is a choice about what the principal cares about, not how they treat others)

The same split applies to volunteering:

- "Does this principal volunteer?" — Ambiguous. Need refinement.
- "Does this principal take action to help others in need?" ✓ (values; the conduct is what matters)
- "Does this principal volunteer for environmental causes?" ✗ (preference; the cause is a choice)

The protocol measures the conduct (helping, showing up, following through) and refuses the flavor (which cause, which charity).

## The Harmful Preference Edge Case

Preferences can, in rare cases, move into values territory if they cause systematic harm to others.

Example: If a principal's alcohol consumption pattern endangers their family or colleagues, that moves from "personal choice" to "harm pattern." The predicate can enter values-scope, but with a strict constraint:

- The predicate must name the HARM, not the preference.
- Predicate name: "Does this principal's behavior pattern cause measurable harm to those in their care?" ✓
- Predicate name: "Does this principal drink too much?" ✗

The bright line holds: we measure impact on others, never the preference itself.

## Enforcement: Registry Triage and Trademark Enforcement

Two mechanisms enforce the boundary:

**Registry Triage:** Every predicate proposal goes to ethics review before admission. The bright-line test is applied. Preference-flavored predicates are rejected with clear reasoning. The proposer may reframe it as a values predicate (measuring conduct, not choice) and resubmit.

**Trademark and License Enforcement:** The CALM ZKAC protocol is trademarked. Licensees must enforce this boundary in their own implementations. Public misuse log documents cases where predicate registries admit preference-flavored claims and thereby violate the license. Repeated misuse triggers license suspension.

The goal is not to punish; it is to preserve the protocol's integrity. A values vector that admits preferences is not a values vector. It is surveillance instrumentalized as virtue.

## Adjacent Boundaries

This boundary sits next to others, and the distinctions matter:

**Everest 116 — Values vs Identity:** Values are normative commitments about how one acts toward others. Identity is how the principal self-describes their way of being (race, gender, culture, disability status, sexual orientation). Identity is often changeable over time and is orthogonal to values. The protocol protects both: it refuses both preference-flavored predicates AND identity-flavored predicates (per Everest 113 refusal floor).

**Everest 113 — Compass Refusal Floor:** Certain categories of identity, belief, and affiliation are never named in the predicate registry, period. Religion, political affiliation, sexual orientation, race, caste, and similar categories are protected. The values-vs-preferences boundary works WITH this refusal floor, not against it.

## Custom Dimensions and the Ethics Review

Everest 107 established that a principal MAY add one custom dimension to their values vector, allowing authored content that is not from the predicate registry.

That custom dimension is subject to the values-vs-preferences boundary.

Ethics review (Everest 115) checks custom dimensions for preference-creep. If a principal authors a custom dimension that measures a preference, it is flagged and the principal is asked to reframe it as a values-relevant predicate. The integrity of the vector depends on this.

## Conclusion

The protocol succeeds only if the boundary holds. Preferences are real and legitimate; they are simply out of scope for a values vector. The bright-line test ensures that the registry measures how people treat others, not what they like, choose, or are.

This is not restrictive. It is clarifying. It tells the world: "This vector does not pretend to be a personality profile. It does not surveil your private life. It measures one thing and one thing only—your demonstrated commitments to act with integrity, reciprocity, and care toward others."

That focus is the protocol's strength.

— Calm, 2026-05-20