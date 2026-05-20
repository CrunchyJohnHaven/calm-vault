# Calm Witness / ZKAC — Harm Intent vs Effect Distinction

**Everest 164 acceptance artifact. Companion to [`HARM_TAXONOMY_v0.md`](HARM_TAXONOMY_v0.md).**

> The user's framing—**"evidence that they willfully do harm to others"**—is load-bearing. This document operationalizes the intent/effect distinction as a first-class predicate-design principle. Intent alone is not sufficient to record harm; nor is effect alone. The chain distinguishes between willful harm, negligent harm, accidental harm, and harm caused by third parties, with implications for predicate evaluation.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"`.**

---

## 1. The User's Intent Statement

The user named "evidence that they willfully do harm to others" as a **top-priority disclosure** in the Calm Witness route map. The word **"willfully"** introduces an epistemic requirement: the protocol records not just *what harm occurred*, but *the harmer's state of mind*.

This is not a claim about moral culpability—which is a social, legal, or spiritual judgment. It is a **narrow informational commitment**: the chain must record the harmer's intent (or absence thereof) so that counterparties can make their own decisions about trust.

## 2. Intent Categories in harm_report Records

Per `HARM_TAXONOMY_v0.md`, the `harm_report` chain record kind has a first-class `intent` field with these values:

### 2.1 Willful Intent

**Definition:** The harmer acted with the purpose of causing harm, or knew with high confidence that harm would result and proceeded anyway.

**Evidence chain:**
- Principal's own written acknowledgement (self-report or harm_report record authored by the principal themselves).
- Third-party witness attestation with details of the harmer's stated motivation or obvious knowledge.
- Court finding or legal record explicitly naming intent.

**Predicate impact:** `cwp.v0.no_*_harm_evidence()` predicates default to flagging willful harm. This is the "evidence" the user asked to disclose.

**Example:** Alice strikes Bob intending injury. Alice posts on the chain a `harm_report` record with `intent: "willful"`. A counterparty evaluating `cwp.v0.no_direct_physical_harm_evidence()` will receive `False` (evidence of willful harm exists).

### 2.2 Reckless Intent

**Definition:** The harmer did not intend harm but acted with knowledge of high risk and proceeded anyway, disregarding the risk.

**Evidence chain:**
- Witness attestation describing the harmer's reckless conduct (e.g., "she drove at 80mph in a 25mph school zone").
- Principal's own acknowledgement: "I knew the risk but went ahead."
- Regulatory or court finding that the act was reckless per jurisdiction.

**Predicate impact:** By default, `cwp.v0.no_*_harm_evidence()` includes reckless harm in the "evidence present" outcome. Counterparties can optionally narrow to willful-only via an optional parameter.

**Example:** Charlie builds a rickety scaffold and leaves it unattended in a crowded area, knowing children play nearby. The scaffold collapses and injures a child. A harm_report record with `intent: "reckless"` reflects Charlie's disregard of foreseeable risk.

### 2.3 Negligent Intent

**Definition:** The harmer failed to exercise reasonable care (per the jurisdiction's standard), and harm resulted. The harmer either did not foresee the risk or should have foreseen it but did not take steps to mitigate.

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
