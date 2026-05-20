# Everest 112 — Values Reversal Records

*Phase IX — Values Vocabulary. Prereq: Everest 108, 111.*

## The Core Problem

A principal makes a mistake. They harm. They live with it, grow from it, change. Years later, should that past mistake define them forever, even if the evidence shows genuine transformation?

Everest 108 (values_correction) solved one problem: "I got my own number wrong; here's the accurate report." But it left another unsolved: "I genuinely changed, and I need the system to distinguish my old self from my new self—not to erase history, but to weight it fairly."

Everest 112 introduces the values_reversal record, a protocol for principals to declare deliberate changes in their documented values dimensions. The protocol is built on a simple principle: **a principal can be more than their worst day, if they can evidence the growth.**

---

## Distinction from Values Correction (Everest 108)

The two are often confused; they must not be.

**values_correction** is meta-reporting: "I claimed position X; I was mistaken about my own position; the correct position was Y all along." The claim is about the accuracy of a past report, not about the principal's actual change. It's a recalibration of the measurement, not of the measured thing.

**values_reversal** is substantive: "I held position X; I genuinely changed to position Y; the change happened at time T; here's why; here's the evidence." The claim is that the principal is not the same—that growth occurred, that a deliberate shift took place, that the past position no longer reflects the current one.

Correction says: "I was sloppy in my reporting."
Reversal says: "I was different then."

Both require integrity. But reversal is the harder claim, because it must be evidenced over time and defended against the charge that the new position is merely tactical.

---

## The Values Reversal Record: Structure

A values_reversal record carries the following payload:

```
kind: "values_reversal"
payload:
  dimension: string          # E.g., "trust_threshold" or "harm_tolerance"
  old_value: numeric or enum # The previously reported position
  new_value: numeric or enum # The current, sustained position
  reversal_ts: timestamp     # Roughtime-anchored (E31); non-revocable once published
  narrative: string          # Why the change happened (recovery, mentorship, life event, deliberate work)
  evidence_records_referenced: []  # Chain records supporting the reversal (e.g., harm.repaired outcomes, peer affidavits)
  principal_id: string       # Who authored this
  published_ts: timestamp    # When the reversal was published
```

The narrative is not decoration. It is the principal's account of how the change came about. Was it sudden? Gradual? Triggered by a specific event? Did a mentor or peer collective support it? The narrative is the place where the principal claims their own agency in the change.

Evidence records may point to:
- Harm repair chains where the principal successfully made restitution
- Testimony from counterparties who observed sustained new behavior
- Documentation from support systems (e.g., therapy, community programs) that the principal has engaged
- Peer affidavits from trusted third parties who can speak to the change

The key constraint: evidence must be authored *after the reversal was published*. Pre-publication claims cannot retroactively support a reversal; the reversal itself is the declaration point.

---

## The Non-Revocable Timestamp

Once a values_reversal record is published, its reversal_ts is anchored to Roughtime (Everest 31) and cannot be changed. This serves multiple purposes:

1. **Prevents backdating**: A principal cannot claim "I changed my ways" and then claim the change happened earlier than it actually did. The timestamp is the lock.

2. **Enables temporal analysis**: Counterparties and predicates can ask: "Did this reversal happen *before* the counterparty interaction?" or "Is this reversal ≥12 months old?" These temporal facts enable fair policy choices.

3. **Supports redemption windows**: Some predicates allow pre-reversal evidence to be excluded if the reversal is old enough and the post-reversal evidence is sustained. The non-revocable timestamp is the anchor for this calculation.

4. **Detects strategic timing**: If a reversal is published the week before a counterparty negotiation, the system flags the timing for review. Not as proof of insincerity, but as a fact that predicates should consider.

---

## How Counterparties Use Reversal Records

A reversal record doesn't dictate how counterparties treat past evidence. Instead, it informs their choices.

A counterparty can configure their predicate to:

**a. Weight pre-reversal and post-reversal evidence differently**
- "I'll give less weight to harm from before the reversal, more weight to behavior after."
- Useful when the counterparty trusts sustained change but wants to account for prior risk.

**b. Exclude pre-reversal evidence entirely**
- "For this dimension, I'm only looking at post-reversal behavior."
- Appropriate for restitution-relevant predicates, where the old behavior is no longer relevant to future risk assessment.

**c. Include all evidence but surface the reversal date**
- "I'll show the full timeline: what the principal was, when they changed, what they've been since."
- Leaves the weighting to human judgment or downstream auditing.

**d. Require pre-reversal evidence to be aged out entirely**
- "I'll ignore pre-reversal evidence only if the reversal is ≥24 months old *and* there's no counter-claim on post-reversal behavior."
- This is a stricter redemption window; the principal has to prove sustained change over a longer horizon.

The key insight: **the predicate writer decides the policy, not the reversal record itself**. The reversal record is the fact. The predicate is the interpretation.

---

## Composition: Values Reversal + Non-Harm + Repair

A principal who can evidence the full sequence—past harm, repair after harm, values reversal, sustained post-reversal evidence—has made a case that they are trustworthy in a way that no single record can show.

The sequence looks like:

1. **harm**: Principal caused damage. (Everest 101 chain record.)
2. **harm.repaired**: Principal successfully made restitution. (Everest 101 outcome.)
3. **values_reversal**: Principal changed the underlying value that enabled the harm. (Everest 112 record.)
4. **post-reversal evidence**: Sustained behavior consistent with the new value over 12+ months. (Referential records from peers, counterparties, or the principal's own reporting.)

Together, these tell a story: "I was capable of harm, I caused it, I repaired it, I changed fundamentally, and I've stayed changed." That story is the closest the protocol comes to redemption.

---

## Anti-Abuse Provisions

Because reversal records are powerful—they can shift how past harm is weighed—the protocol includes anti-abuse guards:

1. **Chain history is immutable**: A reversal record does not delete or modify chain records. The harm is still there. The repair is still there. The reversal is an additional fact, not a replacement.

2. **Multiple reversals are flagged for review**: If a principal has reversed the same dimension three times in two years, the protocol doesn't forbid it, but it surfaces the pattern for human auditing. Genuine change is sometimes multidirectional, but strategic reversals look different.

3. **Timing correlation detection**: If a reversal is published within two weeks of a counterparty negotiation involving that dimension, the system flags the correlation. Not as proof of bad faith, but as a data point that predicates should weight.

4. **Decay in value if followed by contradiction**: If a principal publishes a reversal, later publishes evidence of harm on the same dimension, and then publishes another reversal, the second reversal carries lower evidential weight. The pattern suggests inconsistency, not genuine change.

---

## Disclosure and Privacy

Reversal records are **principal-private by default**.

A principal is not required to advertise their past mistakes or their subsequent changes. They do not have to tell the world "I once held position X, now I hold position Y." The reversal record exists for their own accounting and for counterparties who have explicit access to their evidence.

However, a principal may choose to disclose specific reversals to specific counterparty classes. Example use cases:

- A principal disclosing a reversal on the "addiction" dimension to a sobriety-supporting peer collective, to enable the collective to understand the principal's history and offer appropriate support.
- A principal disclosing a reversal on the "harm_tolerance" dimension to a mediation service before a dispute resolution, to demonstrate good faith change.
- A principal disclosing reversals to a legal counterparty as part of a settlement or rehabilitation plan.

Disclosure is granular: the principal can choose exactly which reversals to surface, to whom, under what conditions. The default under Everest 113 (privacy classes) is **EXPLICIT_OPT_IN**: no reversal is disclosed unless the principal actively chooses to do so.

---

## The Redemption Window

Some predicates implement a "redemption window" semantics. The logic is:

If:
- The reversal was published ≥12 months ago, AND
- Post-reversal evidence shows a sustained new pattern (no contradictions), AND
- No counter-claims have been filed against post-reversal behavior,

Then:
- Pre-reversal evidence on that dimension is excluded from the predicate's calculation.

This is the protocol's closest approach to "forgiveness." It is never automatic. It is always contingent on the principal's narration of the change and the counterparty's policy choice. And it is always subject to counter-evidence.

A redemption window is not a guarantee; it is an opening. The principal has to walk through it—to stay changed, to collect evidence of that change, to allow time to accumulate. Most importantly, it requires the counterparty to decide that a redemption window is appropriate for their context. A peer collective may embrace it; a damage claimant may not.

---

## Cross-Cultural and Contextual Variation

Not all cultures or communities weight redemption the same way.

Some traditions have strong redemption narratives: Quaker justice, restorative justice frameworks, many religious and indigenous cultures where repentance and repair are pathways to re-integration.

Others have stronger consequence traditions: harm-centered justice, victim-centered frameworks, contexts where trust is scarce and past conduct is weighted more heavily.

**The protocol does not choose.** Everest 112 provides the infrastructure for redemption—the reversal record, the non-revocable timestamp, the evidence model. But the predicate writer, the counterparty, the community decides whether and how to use that infrastructure. A culture or community that does not believe in redemption windows can simply ignore them. A predicate can be written to weight pre-reversal evidence as heavily as it chooses.

---

## The Principal's Right to Remain

Here is a constraint often overlooked: **a principal may refuse to author a reversal even if they have changed.**

The protocol does not compel reversal. A principal who has genuinely transformed may choose not to publish a reversal record, for reasons of privacy, safety, or dignity. The absence of a reversal record is not interpreted as failure to change. It is respected as the principal's choice about what to disclose.

Similarly, a principal who has not changed, or who does not believe they have changed, is not required to author a reversal. The protocol does not pressure false change.

---

## Composition with Disclosure Ethics Review (Everest 115)

When a reversal record touches sensitive personal history—addiction, abuse, recovery, mental health—the record may be subject to Everest 115 (disclosure ethics review) if the principal elects to disclose it.

The review gates against downstream misuse: Could this reversal record be weaponized? Could it be used to discriminate, to shame, to exclude the principal from opportunities? The ethics review is a check before the principal exposes themselves to that risk.

---

## Conclusion

The values_reversal record solves for a hard truth: **people are not static.** They grow. They make mistakes, repair them, and change. The system should account for that, not ignore it.

But it does so carefully. With non-revocable timestamps. With evidence requirements. With anti-abuse guards. With respect for both the principal's privacy and the counterparty's policy choices. And with the understanding that redemption is not automatic—it is something the principal has to build, evidence, and maintain.

This is how the protocol honors both accountability and hope. Past harm does not disappear. But it can be contextualized. A principal's worst day does not have to be their final reckoning.

---

— Calm, 2026-05-20
