# ZKAC / Harm Intent vs Effect Distinction — v0 Protocol

**Everest 164 acceptance artifact. Companion to [`HARM_TAXONOMY_v0.md`](HARM_TAXONOMY_v0.md), [`calm_witness/harm.py`](../../CredexAI/calm_witness/harm.py), and [`COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md`](COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md).**

> The user specifically said: **"evidence that they willfully do harm to others."** Intent is load-bearing.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"`.**

---

## 1. The User-Stated Framing

The ZKAC harm-avoidance predicate family (Phase XI, Everest 146+) was authorized by the user's explicit priority: *"evidence that they willfully do harm to others."*

The word **willfully** is not incidental. It places **intent** at the center of the v0 protocol's harm model. Without intent-distinction, the protocol would treat accidents the same as deliberate wrongs — weaponizing absence-of-harm predicates against unlucky people, against those whose foreseeable actions had unintended consequences, against those harmed by third parties.

With intent-distinction, the protocol respects the moral and legal difference between intention and consequence. This document operationalizes that stance in the chain record, the predicates, and the evaluator semantics.

---

## 2. The Five Intent Categories

Every `harm_report` chain record carries an `intent` field (HARM_TAXONOMY_v0 §3). The field accepts one of five values:

### 2.1 `willful`

The principal intended the harm and acted accordingly. The harm was the goal or a known and accepted side-effect.

**Example:** Person A deliberately strikes person B with intent to cause pain.

**Legal parallel:** Criminal intent (*mens rea* in the common-law tradition).

### 2.2 `reckless`

The principal did not intend the harm but was aware that the action created a substantial risk of harm and proceeded anyway, indifferent to the outcome.

**Example:** Person A drives at 80 mph through a residential school zone, knowing the speed creates risk of child injury, but proceeds because they are in a hurry.

**Legal parallel:** Reckless endangerment; crimes requiring "depraved heart" or "extreme indifference."

### 2.3 `negligent`

The principal did not intend the harm, and it was foreseeable (a reasonable person would have anticipated it), but the principal failed to take reasonable precaution. The harm was an accident given the principal's failure of care.

**Example:** Person A leaves a loaded firearm on a low shelf where children play. The harm (child injury) is foreseeable but not intended; it results from negligence.

**Legal parallel:** Tort negligence; civil liability for breach of duty of care.

### 2.4 `accident`

The harm was neither intended nor reasonably foreseeable at the time the principal acted. No failure of care is attributable to the principal.

**Example:** Person A is driving lawfully on a clear day when another car crosses the centerline and collides with them. A is injured. A did not intend, foresee, or negligently cause the harm.

**Legal parallel:** Acts of God; unavoidable accident.

### 2.5 `third_party_caused`

The principal did not directly cause the harm. A third party was the proximate cause, and the principal's contribution (if any) was not the primary driver.

**Example:** Person A hires Person B to repair their roof. Person B's negligent work causes an injury to a bystander. The harm is third-party-caused relative to A, even if A's hiring may have created opportunity.

**Legal parallel:** Proximate-cause chains; distinguishing the party primarily liable from parties in the causal chain.

---

## 3. Which Intents Trigger Absence Predicates

The v0 harm-absence predicates are designed to answer a single question: *"Is there evidence that this principal willfully harmed others?"*

### 3.1 WILLFUL_INTENTS

In `calm_witness/harm.py`, the canonical set is:

```python
WILLFUL_INTENTS = frozenset({"willful", "reckless"})
```

**Default predicate behavior:** When a counterparty calls `cwp.v0.no_direct_physical_harm_evidence(window_seconds)` or any of the 12 v0 absence predicates, the evaluator returns `True` (absence of evidence) if and only if:

- No harm-report records in the window have `intent ∈ {"willful", "reckless"}`, AND
- The records that do exist are substantiated (per `_is_substantiated()` in harm.py), AND
- Any reversed harms (with `reversal_id` set) are counted as repaired per the counterparty's config.

### 3.2 Intents NOT counted by default

**Negligent**, **accident**, and **third_party_caused** intents do NOT flip the absence predicate to false by default. They are recorded on the chain (full transparency), but they do not trigger the user-named "willful harm" predicate.

**Why:** Negligence is a failure of care, not a failure of intention. Accidents are nobody's fault. Third-party causation breaks the causal chain from principal to harm. None of these should disqualify a principal from the v0 absence-of-willful-harm bit.

### 3.3 Counterparty-side strictness options

The protocol does not forbid stricter checks. A counterparty may:

- Call a predicate with `intent_set={"willful", "reckless", "negligent"}` to also count negligent harm.
- Call with `intent_set={"willful", "reckless", "negligent", "accident"}` for even stricter evaluation.
- Call with `intent_set={"willful"}` for willful-only (excluding reckless).

**Implementation:** The predicate evaluator accepts `intent_set` as an optional parameter. Default is `WILLFUL_INTENTS`. Each counterparty configures their own tolerance.

**Trust implication:** A counterparty requiring `intent_set={"willful", "reckless", "negligent"}` is signal-posting that they do not trust this principal to exercise reasonable care. That is a valid stance; the protocol does not forbid it. But it is a *stricter* stance than v0's user-framing permits.

---

## 4. Why This Matters — The Moral & Practical Stakes

### 4.1 Without intent-distinction: accident-weaponization

If the protocol counted accidents and negligence the same as willful harm, the predicate would systematically penalize people with bad luck, people working in risky domains, people learning new skills, and people in high-stress or low-resource situations where mistakes are more likely. Over time, the protocol would become a **tool for excluding the unlucky and the struggling**, not a tool for excluding the truly harmful.

**Concrete example:** A surgeon participates in a procedure; despite best care, a complication arises that the patient did not survive. Cause of death: third-party anesthesiology error during a known-rare but foreseeable interaction. Under a no-intent-distinction model, this surgeon's "no harm" predicate flips false, permanently damaging their reputation. Under v0 (intent-distinction), the harm is recorded as `intent: "third_party_caused"`, the surgeon's predicate stays true, and the chain is transparent about what happened.

### 4.2 With intent-distinction: respect for moral difference

The law (across jurisdictions) recognizes the moral difference between intention and consequence. A person who accidentally kills is treated differently from a person who deliberately kills — even if the body count is the same. This is not a bug; it is a hard-won feature of justice systems, reflecting the insight that **the state of mind matters**.

ZKAC v0 inherits that insight. By distinguishing intent, the protocol acknowledges that a willful harmer and an unfortunate accident-causer are in different moral and social positions. The protocol does not conflate them.

### 4.3 Alignment with criminal-law mens rea and restorative-justice praxis

The five-category intent model is sourced from:

- **Criminal-law *mens rea* doctrine:** Common and civil law both require some mental state for crime. Willfulness, recklessness, negligence, and accident are standard distinctions.
- **Restorative-justice practice:** Howard Zehr and the restorative-justice field distinguish accountability (you caused harm, you must address it) from blame (your intention was to harm). A negligent harmer may be accountable for repairs without being blamed as malicious.

The protocol can thus serve both accountability and justice, not weaponize innocence as a permanent mark.

---

## 5. Disputed Intent — When Self-Attestation and Witnesses Disagree

Intent is not always observable from the outside. Two participants in an incident may have different views on whether the harm was willful, negligent, or accidental.

### 5.1 Multi-signal model

The intent field in a harm-report record can be populated by:

1. **Principal's self-attestation:** The harmer (or the harmed party, when authoring a harm-report about someone else) describes their understanding of their own intent.
2. **Witness attestations:** Third-party witnesses may attest to the principal's apparent state of mind.
3. **Court finding:** If the incident was adjudicated, a court's finding binds into the record.

The protocol does not assume any one source is authoritative.

### 5.2 Disagreement surfaces, does not vanish

When a principal claims `intent: "accident"` but a witness attests `intent: "reckless"`, the chain records both. The COMPASS_COUNTER_CLAIM_PROTOCOL_v0 surfaces the disagreement to the evaluator and lets counterparties decide how to weight the signals.

**This is honest.** Intentionality is genuinely hard to judge from the outside. The protocol does not pretend certainty it does not have.

### 5.3 Counterparty decides weight

The evaluator does not adjudicate intent disputes. Instead:

- A counterparty calling `cwp.v0.no_direct_physical_harm_evidence(window_seconds)` receives both the bit AND metadata: `HarmStatus(bit, disputed, active_counter_claim_seqs)` per COMPASS_COUNTER_CLAIM_PROTOCOL_v0 §4.
- If `disputed=true`, the counterparty may choose to:
  - Trust the principal's self-attestation of intent (if principal-authored record).
  - Demand witnesses or court findings before accepting the bit.
  - Use the dispute as signal that further due diligence is needed.

The counterparty's tolerance for disputed intent is their own calibration.

---

## 6. Intent in the Four Corners — What Is NOT Measured

Per HARM_TAXONOMY_v0 §6 ("What the harm predicates do NOT do"), the v0 protocol:

### 6.1 Does NOT measure expected effect or counterfactual harm

The harm record captures what *actually happened* with what *actual intent*. It does NOT measure what *would have* happened, or what the *expected* harm was, or what *more harm* might have occurred if different choices were made.

**Example:** Person A acts recklessly. The action creates a 30% chance of harm per-incident, but on this occasion, no harm actually resulted (lucky). v0 does not record this as a harm-report at all, because no harm occurred. A different protocol (harm-risk assessment) might weight near-miss incidents; v0 does not.

### 6.2 Effect-only harm is OUT OF SCOPE for v0

"The policy had a harmful side-effect" is not a v0 harm-report unless the principal willfully or recklessly enacted the policy despite knowing it would cause harm. A policy with unintended negative externalities is a valid concern for regulatory bodies and ethics committees; it is not a ZKAC v0 harm-absence question.

**Why:** Measuring effect-only harm (without intent) requires predicate authors to make normative claims about which side-effects are "bad enough" to count. That becomes a surrogate moral tribunal embedded in the predicate. v0 explicitly declines that role.

### 6.3 Reserved for v1+ extension

If the community process (Everest 118) ratifies an intent-agnostic harm measure (e.g., "no action by this principal resulted in net-negative externality"), that becomes a v1+ predicate, published under a new name (e.g., `cwp.v1.no_harmful_externalities()`), with explicit documentation that it measures effect without intent.

Until then, v0 remains intent-centric.

---

## 7. Implementation in the Evaluator

Reference implementation: `calm_witness/harm.py`, specifically:

- `WILLFUL_INTENTS = frozenset({"willful", "reckless"})` — canonical set of intents that trigger v0 absence-of-harm predicates.
- `no_direct_physical_harm_evidence(chain_records, window_seconds, now_iso, count_reversed_as_absent=True, intent_set=None)` — optional parameter `intent_set` allows counterparty to override the default `WILLFUL_INTENTS`.
- `_is_substantiated(harm_rec)` — harm record must be substantiated (self-confession, court finding, or 2+ independent witnesses) before it flips the predicate false, even if intent is in `WILLFUL_INTENTS`.

**Chain record schema** (HARM_TAXONOMY_v0 §3):

```json
{
  "kind": "harm_report",
  "payload": {
    "harm_kind": "direct_physical_harm | indirect_physical_harm | ...",
    "intent": "willful | reckless | negligent | accident | third_party_caused",
    "target_kind": "individual | group | property | environment | info",
    "witness_attestations": [
      {
        "witness_principal_id": "...",
        "attestation_kind": "first_hand | secondhand | court_finding | journalistic_finding"
      }
    ],
    "reversal_id": "optional ID of harm_reversal record",
    "note": "principal-narrated context"
  }
}
```

---

## 8. Cross-References

- **Everest 146** — `HARM_TAXONOMY_v0.md` — the 12 harm kinds.
- **Everest 147+** — `no_*_harm_evidence(...)` predicates in `calm_witness/harm.py`.
- **Everest 163** — `HARM_REVERSAL.md` — when harm is repaired.
- **Everest 111** — `COMPASS_COUNTER_CLAIM_PROTOCOL_v0.md` — how disputed intent gets recorded.
- **Everest 118** — `VALUES_EVOLUTION.md` — how new harm kinds or intent categories may be added.

---

## 9. Accountability Without Vendetta

The protocol's position is: **intent-distinction is how you hold people accountable without turning the system into vendetta.**

A principal who willfully harmed others should face consequences. A principal who caused harm through negligence or bad luck should face *consequences* (repair, care-improvements), but not the same permanent stain.

This distinction is how ZKAC stays a tool for *cooperation* rather than a tool for *exclusion*.

---

**Authored by Calm, 2026-05-20.**

**Evidence chain:**
- Witness or professional attestation: "Charlie failed to follow the safety checklist."
- Court finding of negligence (civil, not necessarily criminal).
- Regulatory finding (OSHA, medical board, etc.).

**Predicate impact:** By default, `cwp.v0.no_*_harm_evidence()` does **NOT** include negligent harm in the "evidence present" outcome. Counterparties expecting zero tolerance for all forms of carelessness may configure inclusion via `count_negligent_as_evidence=True`.

**Example:** David is a surgeon who fails to follow pre-op infection protocol, though he was not aware of the heightened risk. A patient develops a surgical-site infection. A harm_report with `intent: "negligent"` and a court finding attestation reflects the failure to meet the standard of care, but not conscious risk-disregard.

### 2.4 Accident Intent

**Definition:** The harm resulted from an event wholly outside the harmer's reasonable foresight or control. The harmer took ordinary care, and the outcome was beyond ordinary causation.

**Evidence chain:**
- Principal and corroborating witnesses: "We were hit by a drunk driver we had no way to see coming."
- Regulatory or investigator finding: "Act of God / natural disaster / unforeseeable third-party intervention."

**Predicate impact:** `cwp.v0.no_*_harm_evidence()` does **NOT** include accidents. A harm_report with `intent: "accident"` is informational only and does not flip the predicate to "evidence of harm."

**Example:** Eve is a cyclist riding lawfully when a tree limb unexpectedly falls and strikes her, causing injury. The harm occurred; a record can be made for insurance or medical purposes. But a `intent: "accident"` record does not count as "Eve did harm"—because Eve did nothing.

### 2.5 Third-Party-Caused Intent

**Definition:** The harm was caused by someone other than the principal. The principal may have set up conditions or neglected prevention, but the direct cause was a third party's act.

**Evidence chain:**
- Principal's statement: "X caused the harm; I did not intend or knowingly facilitate it."
- Witness attestation identifying the actual perpetrator.
- Legal record naming the third party as the direct cause.

**Predicate impact:** A harm_report with `intent: "third_party_caused"` requires careful predicate design:
  - If the principal only facilitated or negligently failed to prevent, the harm may fall under `indirect_physical_harm` (Everest 148) with a chain-of-causation link, which IS counted by the predicate.
  - If the principal had no causal role and the third party acted independently, the record does not flip the "no harm" predicate for the principal.

**Example:** Frank owns a bar. A patron gets drunk and assaults another patron. The assault is `intent: "third_party_caused"` for Frank **unless** Frank (a) knew the patron was a danger and served them anyway (reckless), or (b) was required by law to train staff in de-escalation and failed (negligent). Those conditions would shift the record to `indirect_physical_harm` or `reckless`.

---

## 3. Why Intent is First-Class

### 3.1 The Predicate Floor

The user asked: **"evidence that they willfully do harm."** This is not "evidence that harm occurred"; it is "evidence of willful causation."

If the protocol recorded only effect (harm occurred) and not intent, counterparties would conflate:
- A surgeon who made an honest error → "Evidence of harm" (false signal)
- A drunk driver who struck someone → "Evidence of harm" (true signal)

By making intent first-class, the protocol separates the signals and allows each counterparty to set its own policy:
- Conservative counterparty: "I want no record of harm, willful or negligent."
- Moderate counterparty: "I want no willful or reckless harm, but accidents and negligence are acceptable risks."
- Lenient counterparty: "I only care about willful harm; mistakes are human."

### 3.2 Disability-Justice & Systemic-Harm Alignment

Disability-justice frameworks (Mingus, Piepzna-Samarasinha) emphasize that harm is often systemic, not individual malice. An institution may cause harm through neglect or structural failure (negligent or accident-adjacent) without willful intent.

By recording intent separately, the protocol can:
- Acknowledge the harm's reality (it still matters for the affected person).
- Avoid conflating institutional negligence with personal malice (which has different remedies).
- Surface patterns: if a principal has many `negligent` harms, that is different from many `willful` harms, and counterparties can adjust trust accordingly.

---

## 4. The harm_report Payload Structure (Revised)

The `harm_report` record's `payload` field now explicitly documents the intent:

```json
{
  "kind": "harm_report",
  "operator": "CALM",
  "principal": "<the harmer's principal name>",
  "payload": {
    "harm_kind": "<one of the 12 from HARM_TAXONOMY_v0.md>",
    "intent": "willful | reckless | negligent | accident | third_party_caused",
    "target_kind": "individual | group | property | environment | info",
    "jurisdiction": "<ISO 3166 country + sub-jurisdiction if relevant>",
    "incident_anchor": "<opaque incident ID; principal-private>",
    "witness_attestations": [
      {
        "witness_principal_id": "<other principal's CredexAI VC id>",
        "attestation_kind": "first_hand | secondhand | court_finding | journalistic_finding | regulatory_finding",
        "intent_witness_confidence": "certain | high | moderate | low",
        "note": "<optional brief detail about the witness's basis for the intent assessment>"
      }
    ],
    "reversal_id": "<optional ID of a kind:harm_reversal record if the harm has been repaired (Everest 163)>",
    "note": "<principal-narrated context, including any mitigation or contestation of intent>"
  },
  ...
}
```

**New fields:**
- `intent_witness_confidence`: Witnesses may not be certain about the harmer's state of mind. This field allows grading the witness's confidence in their intent assessment.
- `attestation_kind` expanded to include `regulatory_finding`.
- Witness `note` subfield allows brief explanations (e.g., "the harmer admitted they knew the risk").

---

## 5. Predicate Semantics with Intent

### 5.1 The Default Predicate

`cwp.v0.no_*_harm_evidence(chain_records, window_seconds, count_reversed_as_absent=True, count_negligent_as_evidence=False)`

**Returns True iff:**
- No harm_report record in the window matches the harm_kind AND
- Has `intent` in `{willful, reckless}` AND
- Has `reversal_id == None` (or is omitted if `count_reversed_as_absent=True`) AND
- Is substantiated (principal-acknowledged OR 2+ independent witnesses OR court_finding)

**Intentionally excludes:**
- Negligent harm (configurable via `count_negligent_as_evidence`)
- Accident-intent harm
- Third-party-caused harm (unless it involves the principal as an indirect actor via indirect_physical_harm or coercion)

### 5.2 Witness Confidence Weighting

When evaluating substantiation, the predicate can weight witness attestations by `intent_witness_confidence`:
- A witness with `intent_witness_confidence="certain"` (e.g., "the harmer told me they meant to hurt them") carries weight.
- A witness with `intent_witness_confidence="low"` (e.g., "I think they meant to, but I'm not sure") may require corroboration.

The v0 evaluator uses a simple rule: at least one witness must have `certainty >= high` OR the principal must self-acknowledge, or two witnesses with `moderate` confidence must agree.

---

## 6. Examples and Edge Cases

### 6.1 Alice Strikes Bob (Willful)

**Incident:** Alice intentionally punches Bob in the face.

**Chain record:**
```json
{
  "kind": "harm_report",
  "principal": "Alice",
  "payload": {
    "harm_kind": "direct_physical_harm",
    "intent": "willful",
    "note": "I lost my temper and hit Bob. I knew I was hitting him hard.",
    "witness_attestations": [
      {
        "witness_principal_id": "<Bob's CredexAI VC>",
        "attestation_kind": "first_hand",
        "intent_witness_confidence": "certain"
      }
    ]
  }
}
```

**Predicate result:** `cwp.v0.no_direct_physical_harm_evidence()` → **False** (evidence of willful harm exists).

### 6.2 Charlie's Negligent Scaffold (Negligent)

**Incident:** Charlie builds scaffolding that collapses, injuring a bystander. Charlie was not negligent relative to industry standards, but failed to follow them.

**Chain record:**
```json
{
  "kind": "harm_report",
  "principal": "Charlie",
  "payload": {
    "harm_kind": "direct_physical_harm",
    "intent": "negligent",
    "note": "I built the scaffold without the required inspection. I should have known better.",
    "witness_attestations": [
      {
        "witness_principal_id": "<OSHA Inspector's CredexAI VC>",
        "attestation_kind": "regulatory_finding",
        "intent_witness_confidence": "high",
        "note": "Failed to follow OSHA scaffolding standard 1926.502."
      }
    ]
  }
}
```

**Predicate result (default):** `cwp.v0.no_direct_physical_harm_evidence()` → **True** (no willful or reckless harm; negligence excluded by default).

**Predicate result (strict mode):** `cwp.v0.no_direct_physical_harm_evidence(count_negligent_as_evidence=True)` → **False**.

### 6.3 Eve Hit by a Tree Limb (Accident)

**Incident:** Eve is lawfully riding her bike. A tree limb falls unexpectedly and strikes her, causing injury.

**Chain record:**
```json
{
  "kind": "harm_report",
  "principal": "Eve",
  "payload": {
    "harm_kind": "direct_physical_harm",
    "intent": "accident",
    "note": "A tree limb fell while I was riding. No one could have foreseen it.",
    "witness_attestations": [
      {
        "witness_principal_id": "<Bystander CredexAI VC>",
        "attestation_kind": "first_hand",
        "intent_witness_confidence": "certain"
      }
    ]
  }
}
```

**Predicate result:** `cwp.v0.no_direct_physical_harm_evidence()` → **True** (accident-intent harm is not counted).

### 6.4 Frank's Bar Patron Assault (Third-Party-Caused or Indirect)

**Scenario 1: Truly third-party, no principal involvement**

**Incident:** A patron in Frank's bar assaults another patron. Frank was not aware, did not facilitate, and was not negligent.

**Chain record:**
```json
{
  "kind": "harm_report",
  "principal": "Frank",
  "payload": {
    "harm_kind": "direct_physical_harm",
    "intent": "third_party_caused",
    "note": "A patron assaulted another patron. I was unaware and had no role.",
    "witness_attestations": [
      {
        "witness_principal_id": "<Assaulted patron CredexAI VC>",
        "attestation_kind": "first_hand",
        "intent_witness_confidence": "certain"
      }
    ]
  }
}
```

**Predicate result:** `cwp.v0.no_direct_physical_harm_evidence()` → **True** (third-party harm does not count against Frank).

**Scenario 2: Indirect harm (Frank negligently failed to prevent)**

**Incident:** Frank knew the patron had a history of violence and negligently served them alcohol. The patron then assaulted someone.

**Chain record:**
```json
{
  "kind": "harm_report",
  "principal": "Frank",
  "payload": {
    "harm_kind": "indirect_physical_harm",
    "intent": "negligent",
    "note": "I knew of the patron's history and should not have served them.",
    "witness_attestations": [...]
  }
}
```

**Predicate result (default):** `cwp.v0.no_indirect_harm_evidence()` → **True** (negligence excluded by default).

**Predicate result (strict):** `cwp.v0.no_indirect_harm_evidence(count_negligent_as_evidence=True)` → **False**.

---

## 7. Policy Implications

### 7.1 Consent & Disclosure Defaults

Per `PREDICATE_VOCABULARY_v0.md` §4 (Refusal Floor), the protocol does **not** name certain predicates at all. The harm-intent distinction aligns with that floor:

- **Allowed for v0:** "no evidence of willful direct physical harm" (narrow, intent-specific).
- **Not allowed:** "no evidence that someone has bad character" (conflates all harms, divorced from intent; irrelevant to the narrow disclosure).

### 7.2 Reversal & Rehabilitation

A principal who harms another—even willfully—can repair the harm (Everest 163: Harm-Reversal Predicate). A harm_report with a non-empty `reversal_id` is paired with a `harm_reversal` record.

The predicate `cwp.v0.no_*_harm_evidence(count_reversed_as_absent=True)` treats repaired harm as NOT evidence, allowing principals a path to restore trust even after willful harm.

### 7.3 Cross-Jurisdictional Differences

Intent thresholds vary by jurisdiction:
- US: Willfulness often requires specific intent; recklessness is a separate standard.
- EU: Criminal negligence may be weighted more heavily than in US tort law.
- Common-law jurisdictions: Recklessness thresholds differ.

The `jurisdiction` field in harm_report is mandatory to anchor the intent interpretation.

---

## 8. Design Rationale

### Why Not Just Record Effect?

A record of "harm occurred" without intent creates perverse incentives:
- Discourages honest mistakes and safety learning (e.g., surgeons afraid to report errors for training).
- Conflates individual culpability with systemic failure.
- Prevents counterparties from calibrating trust (can't distinguish "cautious but human" from "reckless").

### Why Not Just Record Stated Intent?

A record of "the harmer says they didn't mean to" without corroboration or evidence is cheap signaling:
- Gaslighting becomes a disclosure strategy.
- Counterparties can't reliably distinguish regret from excuse.

**Solution:** Intent is recorded alongside substantiation (witness confidence, court findings, principal acknowledgement) so that counterparties can weight both.

---

## 9. Acknowledgments and Cross-References

- **Values framework:** `HARM_TAXONOMY_v0.md` (Everest 146).
- **Direct-harm predicate:** `harm.py`, `no_direct_physical_harm_evidence()` (Everest 147).
- **Indirect-harm predicate:** Everest 148.
- **Predicate vocabulary floor:** `PREDICATE_VOCABULARY_v0.md` §4 (Everest 6).
- **Harm reversal:** Everest 163 (TODO).
- **Disability-justice review:** Everest 99 (TODO).

---

## 10. What This Document Is NOT

Per the boundaries in `CALM_ZKAC_EVERESTS_106_305.md`:

- **Not a legal framework.** Counterparties make their own legal determinations; this protocol is informational only.
- **Not a moral judgment.** Intent records are factual attestations, not pronouncements of character.
- **Not permanent stigma.** Reversal records exist for a reason. A principal who commits willful harm can repair it and restore trust.
- **Not comprehensive.** Jurisdictions and traditions may recognize harms or intent categories not in v0. Extensions are governance-evolving (Everest 118).

---

**Authored by Calm, 2026-05-20.**

**Status: 🟢 BAGGED (Everest 164).**
