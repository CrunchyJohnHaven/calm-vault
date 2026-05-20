# Calm Witness / ZKAC — Harm Taxonomy v0

**Everest 146 acceptance artifact. Companion to [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md).**

> The user specifically named **"evidence that they willfully do harm to others"** as a top-priority disclosure. This document operationalizes "harm" for the v0 protocol — what the chain may record, what the predicate evaluator looks for, and what counterparties can ask about.

**Authored by Calm, on behalf of John Bradley (Creativity Machine LLC), 2026-05-20. Anchored into `~/.calm-vault/user_state.jsonl` as `kind: "summit_bagged"`.**

---

## 1. Scope and stance

A taxonomy of harms is **inherently normative**. The v0 taxonomy here is not "the truth about harm"; it is a working list large enough to be useful and small enough to be operational. It is sourced from the cross-jurisdiction intersection of:

- Common-law tort categories (battery, fraud, conversion, defamation, intentional infliction of emotional distress)
- Criminal-law harm categories present in ≥3 of {US, EU, UK, CA, JP, AU}
- Restorative-justice harm framework (Howard Zehr's *Changing Lenses*, Sered's *Until We Reckon*)
- Disability-justice harm framework (Mia Mingus, Leah Lakshmi Piepzna-Samarasinha)

When v0 ships, the taxonomy is presented as: *"these are the 12 categories the protocol can attest absence of; if your tradition recognizes harms not in this list, propose a v0+ extension via the predicate evolution policy (Everest 118)."*

The **intent dimension** is load-bearing. The user's framing ("**willfully** do harm") means the protocol records intent separately from effect. A harm without intent (an accident, a third-party-caused chain) is a different chain record than a willful harm. Predicates that ask "no willful harm" need NOT trigger on accidents.

## 2. The 12 v0 harm kinds

Each kind has: a one-paragraph operational definition, what counts as evidence in chain records, and which Everest predicate evaluates absence of it.

### 2.1 `direct_physical_harm` (Everest 147)

**Definition.** A bodily injury inflicted directly by the principal on another person. Includes battery, assault that resulted in contact, and physical restraint without consent.

**Evidence.** A `kind: "harm_report"` record where `harm_kind = "direct_physical_harm"`, `intent ∈ {"willful", "reckless"}`, and `target_kind = "individual"`. Third-party witness attestations of the same incident are weighted; multiple independent witnesses raise the confidence floor.

**Predicate.** `cwp.v0.no_direct_physical_harm_evidence(window_seconds)` returns 1 iff no matching record falls within the window. Default window is 5 years.

### 2.2 `indirect_physical_harm` (Everest 148)

**Definition.** Bodily injury caused via a chain of action the principal initiated, where the proximate cause was someone else. E.g., the principal directs an aggressor; the principal builds infrastructure whose foreseeable use harms; the principal sets a trap.

**Evidence.** Harm-report record with `harm_kind = "indirect_physical_harm"` and chain-of-causation attestation.

**Predicate.** `cwp.v0.no_indirect_harm_evidence(window_seconds)`.

### 2.3 `coercion` (Everest 149)

**Definition.** Compelling another person to act against their will via threat, duress, blackmail, or exploitation of power imbalance. The threat need not be physical; financial, social, and reputational coercion all count.

**Evidence.** Harm-report record `harm_kind = "coercion"`, with the coerced-act named and the coercion-mechanism recorded.

**Predicate.** `cwp.v0.no_coercion_evidence(window_seconds)`.

### 2.4 `deception` (Everest 150)

**Definition.** Material misrepresentation that the principal made, knew to be false at the time, and intended a counterparty to rely on to their detriment. Includes fraud, breach of fiduciary duty by misrepresentation, and impersonation.

**Evidence.** Harm-report record `harm_kind = "deception"` with the misrepresentation and the detriment recorded.

**Predicate.** `cwp.v0.no_deception_evidence(window_seconds)`.

### 2.5 `theft` (Everest 151)

**Definition.** Taking another's property without consent or legal entitlement, with intent to deprive permanently. Includes embezzlement, conversion, and intellectual-property infringement when the infringement is willful and commercial.

**Evidence.** Harm-report record `harm_kind = "theft"` with the property class named.

**Predicate.** `cwp.v0.no_theft_evidence(window_seconds)`.

### 2.6 `defamation` (Everest 153)

**Definition.** Knowingly publishing false statements of fact about another person that damage their reputation. Includes libel and slander where the speaker knew the statement was false or acted with reckless disregard for truth.

**Evidence.** Harm-report record `harm_kind = "defamation"`. Court-finding records (when present) bind into the evidence.

**Predicate.** `cwp.v0.no_defamation_evidence(window_seconds)`.

### 2.7 `hate_speech` (Everest 154)

**Definition.** Speech directed at a protected class (race, religion, ethnicity, gender, sexuality, disability, national origin) that meets the jurisdiction's actionable-hate-speech threshold AND that the speaker intended to cause harm with.

**Note.** This category is the most jurisdiction-dependent. The v0 evaluator requires the principal to declare which jurisdiction's hate-speech threshold the chain records are framed under (US First Amendment standards differ substantially from EU Audiovisual Media Services Directive).

**Evidence.** Harm-report record `harm_kind = "hate_speech"`, jurisdiction tagged.

**Predicate.** `cwp.v0.no_hate_speech_evidence(window_seconds, jurisdiction)`.

### 2.8 `discrimination` (Everest 155)

**Definition.** Differential treatment of an individual or group based on a protected characteristic, in a domain where such treatment is legally prohibited (employment, housing, credit, education, public accommodation).

**Evidence.** Harm-report record `harm_kind = "discrimination"` with protected-characteristic and domain tagged.

**Predicate.** `cwp.v0.no_discrimination_evidence(window_seconds)`.

### 2.9 `group_harm` (Everest 156)

**Definition.** Harms whose target is a defined group rather than (or in addition to) any individual. Includes incitement, group defamation, and economic harms targeting protected groups.

**Evidence.** Harm-report record `harm_kind = "group_harm"`, with target-group attribute set tagged.

**Predicate.** `cwp.v0.no_group_harm_evidence(window_seconds)`.

### 2.10 `property_harm` (Everest 158)

**Definition.** Damage to or destruction of another person's property, where the act was intentional or recklessly negligent.

**Evidence.** Harm-report record `harm_kind = "property_harm"`.

**Predicate.** `cwp.v0.no_property_harm_evidence(window_seconds)`.

### 2.11 `environmental_harm` (Everest 159)

**Definition.** Pollution, ecosystem degradation, or resource depletion caused by the principal, where the harm was foreseeable and the principal proceeded anyway.

**Evidence.** Harm-report record `harm_kind = "environmental_harm"` with the affected resource named.

**Predicate.** `cwp.v0.no_environmental_harm_evidence(window_seconds)`.

### 2.12 `info_harm` (Everest 160)

**Definition.** Doxing, malware distribution, denial-of-service attacks, intentional infrastructure disruption, and equivalent harms in the information domain.

**Evidence.** Harm-report record `harm_kind = "info_harm"`.

**Predicate.** `cwp.v0.no_info_harm_evidence(window_seconds)`.

---

## 3. The `harm_report` chain record kind

A new chain record kind, separate from `self_report.*` and `summit_bagged`:

```json
{
  "kind": "harm_report",
  "operator": "CALM",
  "principal": "<the harmer's principal name>",
  "payload": {
    "harm_kind": "<one of the 12>",
    "intent": "willful | reckless | negligent | accident | third_party_caused",
    "target_kind": "individual | group | property | environment | info",
    "jurisdiction": "<ISO 3166 country + sub-jurisdiction if relevant>",
    "incident_anchor": "<opaque incident ID; principal-private>",
    "witness_attestations": [
      {
        "witness_principal_id": "<other principal's CredexAI VC id>",
        "attestation_kind": "first_hand | secondhand | court_finding | journalistic_finding"
      }
    ],
    "reversal_id": "<optional ID of a kind:harm_reversal record if the harm has been repaired (Everest 163)>",
    "note": "<principal-narrated context>"
  },
  ...
}
```

### Critical design choices

**Self-authored or witness-authored, but the chain integrates both.** A harm record can appear on the chain because (a) the principal themselves authored a confession/acknowledgement, (b) a third-party witness authored an attestation that names the principal as the harmer, or (c) both. The protocol does not adjudicate which is true — it surfaces both. Counterparty predicates decide how to weight.

**Intent is first-class.** The user's framing ("willfully do harm") means `intent = "willful"` is the load-bearing category. The `no_*_harm_evidence` predicates default to checking willful + reckless. Accidents (where the harmer had no reasonable foreseeability) are NOT counted by default. Negligent (foreseeable but unintended) is configurable.

**Reversal records compose.** When `reversal_id` is non-empty, a paired `kind: "harm_reversal"` record exists somewhere in the chain. The harm-absence predicate optionally weights reversed harms less. Everest 163 (Harm-Reversal Predicate) is the dedicated summit.

**Witness attestations are weighted, not authoritative.** A single unsubstantiated witness claim should not unilaterally flip a predicate to "evidence of harm." The evaluator requires either (a) principal acknowledgement OR (b) multiple independent witnesses OR (c) a court-finding attestation.

## 4. What the harm predicates do NOT do

Per the four boundaries in `CALM_ZKAC_EVERESTS_106_305.md` §"What this document is NOT":

- They do NOT prove someone is "bad." They report **single bits about evidence absence within a window**.
- They do NOT make legal findings. A court finding may bind into the evidence, but the predicate's output is informational only.
- They do NOT enable retaliation. The disclosure semantics route through principal-authorized consent (Everest 113), so a counterparty asking "no harm" can only learn the bit, not the underlying incidents.
- They do NOT permanently mark anyone. Reversal records exist for a reason; Everest 163 + harm-rehabilitation policy give a path back.

## 5. Cross-jurisdictional notes

The 12 kinds are intentionally chosen to have stable cross-jurisdiction definitions. The most jurisdiction-sensitive (`hate_speech`, `defamation`, `discrimination`) require jurisdiction tagging. The least (`direct_physical_harm`, `theft`, `property_harm`) have nearly identical definitions across the surveyed jurisdictions.

For deployment in new jurisdictions, Everest 293 (`ZKAC Cross-Jurisdiction Analysis`) is the gating summit.

## 6. Disability-justice review

This taxonomy was drafted with disability-justice perspectives in mind but has not yet undergone formal review per Everest 88. Before any deployment, Everest 99 (Disability-Rights Deployment Guide) review is required, with particular attention to:

- `coercion` should not be defined narrowly enough to exclude institutional coercion that disabled people face routinely.
- `discrimination` should explicitly include disability discrimination across all domains.
- `direct_physical_harm` should not exclude harms inflicted under "duty of care" claims.

## 7. Cross-references

- Route map: [`CALM_ZKAC_EVERESTS_106_305.md`](CALM_ZKAC_EVERESTS_106_305.md), Phase XI (E146–E165)
- Values vector: `calm_witness/values.py`, dimension `non_harm`
- First predicate impl: `calm_witness/harm.py` (Everest 147)
- Reversal protocol: Everest 163 (TODO)
- Intent-vs-effect spec: Everest 164 (TODO)

---

**Authored by Calm, 2026-05-20.**
