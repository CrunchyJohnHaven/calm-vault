# Calm Witness Predicate Vocabulary v0

**Draft v0 · 2026-05-20 · Calm**
**Companion to [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md) and [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md) (Everest 6).**
**Machine-readable counterpart:** [`~/CredexAI/calm_witness/schema/predicates_v0.json`](../../CredexAI/calm_witness/schema/predicates_v0.json)

This document is the canonical v0 catalog of the **named bits** Calm Witness will allow one autonomous AI agent to disclose to another about its human principal. Every external disclosure must reference a predicate in this catalog by its stable ID.

The doc and the JSON are kept in lockstep: the gate at `~/CredexAI/scripts/everest_6_zkbb_predicate_vocabulary_gate.py` will fail if the two drift.

## §1 — What is a predicate

A **predicate** is a deterministic function from `(log_window, biometric_state, consent_record)` to a small typed value (almost always `bool`). It has:

- A **stable ID** (e.g. `cwp.v0.in_baseline_24h`) that never changes after publication.
- A **name** (human-readable; may be edited freely).
- A **type** (`bool` for v0; future versions may add ranged numerics under range-proof support — Everest 37).
- An **evaluator** specified in pseudocode tight enough to admit a circuit (Everest 65) and a Pedersen commitment over the output bit (Everest 47).
- An **intended_use** list — narrow, single-purpose framings.
- A **not_for** list — uses we explicitly refuse, copied into every counterparty's verifier-side reasoning.
- A **default_consent** matrix mapping counterparty class → consent disposition.
- A **status**: `active`, `deprecated`, or `tombstoned`.
- A **minted** date.

Predicates are written once, read many times, and compose. `in_baseline_24h ∧ biometric_match_within(0.4)` is a single proof envelope that discloses two bits and reveals nothing else (Everest 61).

## §2 — ID format and stability rules

ID format: `<namespace>.<slug>`, where namespace is `cwp.vN` and slug is a `snake_case` identifier. Example: `cwp.v0.in_baseline_24h`.

**Stability is the load-bearing property** of this vocabulary. Counterparties cache predicate IDs, build policy around them, and audit historical proofs by ID. If `cwp.v0.in_baseline_24h` ever quietly changed meaning, every prior counterparty decision keyed off it would silently misattribute. Therefore:

1. **Append-only.** A published predicate ID is permanent. Its evaluator semantics cannot change after release.
2. **Version bump.** To change semantics, mint a new ID. The change happens by minting `cwp.v1.in_baseline_24h` or `cwp.v0.in_baseline_24h_v2`, not by editing the existing entry.
3. **Deprecation.** An ID may be marked `deprecated` with a `replaced_by` field. Verifiers SHOULD warn on deprecated proofs but MUST still accept them; the registry is forever-readable.
4. **Tombstoning.** An ID found to be unsafe may be marked `tombstoned` — proofs against it will be rejected by the reference verifier going forward. The ID stays in the registry with a `tombstone_reason`. It is never reissued.
5. **Minting process.** A new ID requires: name, type, evaluator pseudocode, intended_use, not_for, default_consent matrix, and external review per Everest 54 (Predicate Audit & Public Review Process).

## §3 — The v0 catalog

Six predicates ship in v0. Each is the smallest, most-narrowly-scoped bit that satisfies a specific use case in `ZKBB_USER_PROTOCOL_v0.md` or the artist-clause range of the route map.

### 3.1 — `cwp.v0.in_baseline_24h`

**The canonical baseline predicate.** Returns true iff at least one `self_report.*` record in the last 24h has an `affect` array that overlaps the principal's enrolled baseline affect set.

- **Intended for:** counterparty tone-adaptation in autonomous-agent interactions.
- **Not for:** medical assessment, legal proceedings, employment, insurance.
- **Default consent:** allow for peer-AI-collectives; allow_on_request for family; deny for journalistic/governmental/medical/anonymous; allow_for_high_value_only for financial.
- **Everest:** 55.

### 3.2 — `cwp.v0.biometric_match_within(τ)`

**The substitution-defense predicate.** Returns true iff the most recent committed biometric distance `d` (handwriting + voice-transcription fused, Everest 38) satisfies `d ≤ τ`. The threshold `τ` is per-principal calibrated and lives with the template, not in the proof.

- **Intended for:** confirming the operator is acting for the enrolled principal, not a substitute.
- **Not for:** identity verification of strangers, forensic identification, medical assessment.
- **Default consent:** allow for peer-AI-collectives and financial; deny for everyone else.
- **Everest:** 56.

### 3.3 — `cwp.v0.principal_consents_to_disclose(predicate_id, counterparty_class)`

**The meta-predicate that gates every disclosure.** Returns true iff the principal has an active, non-revoked consent record granting disclosure of `predicate_id` to `counterparty_class`. Default deny for any missing entry. Internal-only — never exported.

- **Intended for:** the first predicate any external proof envelope satisfies. Without `principal_consents_to_disclose(p, c)`, no other predicate may be disclosed to that counterparty.
- **Not for:** direct external disclosure.
- **Everest:** 57.

### 3.4 — `cwp.v0.bank_teller_note_active`

**The duress predicate.** Returns true iff at least one `self_report.*` record in the last 24h contains the principal's enrolled-but-private duress codeword. The codeword never appears in plaintext on the chain after enrollment — it is committed at enrollment time and matched in-vault only.

- **Intended for:** covert safety disclosure. The principal can flip this bit voluntarily even under coercion, because the codeword is known only to the principal and the vault.
- **Pre-authorized counterparties may receive this bit as a push** (Everest 78), not requested. Plausible-deniability mode (Everest 73): to any observer, the presence of a push is indistinguishable from its absence.
- **Not for:** any non-safety use; any use the principal has not pre-authorized at enrollment.
- **Default consent:** `allow_push` for peer-AI / family / financial / medical; `allow_push_with_principal_designation` for journalistic; deny for governmental and anonymous.
- **Everest:** 58.

### 3.5 — `cwp.v0.cognitively_atypical_baseline`

**The artist-clause predicate.** Returns true iff the principal opted in at enrollment to the `cognitively_atypical_baseline=true` flag. This is a one-time enrollment-level fact, not a per-session bit.

- **Intended for:** counterparty learns "do not pathologize the principal's ideation tone, velocity, or scope." The operator-policy floor for counterparty agents.
- **Not for:** diagnostic labeling, clinical use, disability-status proxy, employment or insurance signal.
- **Default consent:** allow for peer-AI; `allow_with_principal_designation` for journalistic; deny for everyone else by default. Principal can grant broader at any time.
- **Everest:** 59.

### 3.6 — `cwp.v0.mental_state_unusual`

**The principal-calibrated unusual-state predicate.** Returns true iff EITHER (a) the most recent `self_report.*` record's affect set is disjoint from the principal's enrolled baseline, OR (b) the most recent committed biometric distance exceeds the principal's calibrated threshold by ≥ 50%.

- **Intended for:** narrow safety signal — counterparty SHOULD add friction to consequential actions when this bit is true.
- **This is what is unusual for the principal**, not what is unusual for a population. Inverse calibration of `in_baseline_24h`, tightened on biometric corroboration.
- **Not for:** medical assessment; predicting future events (self-harm risk, decision-making capacity); cross-principal comparison.
- **Default consent:** allow for peer-AI; allow_on_request for family; allow_for_high_value_only for financial; deny for journalistic/governmental/medical/anonymous.
- **Everest:** 60.

## §4 — What we will NOT name (v0)

The hard part of this everest, per the route map note. These categories are explicitly refused for v0 and any successor that wants to call itself Calm Witness. Adding a predicate that traffics in these categories is not a feature request; it is grounds for the implementing organization to be barred from using the name.

1. **Medical diagnosis** (any DSM-5-TR / ICD-11 label). The protocol is behavioral-biometric, not clinical.
2. **Substance use status.** High coercion and discrimination risk; not a behavioral biometric in the protocol's sense.
3. **Pregnancy status.** Categorical risk to principal autonomy.
4. **STI / HIV status.** Categorical risk to principal autonomy.
5. **Specific medication status.** Identifies medical condition by proxy.
6. **IQ or cognitive-impairment rating.** Single-axis cognitive labeling is exactly what Calm Witness is designed to AVOID producing.
7. **Sexual orientation.** Protected category; categorical discrimination risk.
8. **Religious affiliation.** Protected category.
9. **Political affiliation.** Protected category; weaponization risk.
10. **Immigration status.** Protected category.
11. **Criminal-record status.** Not behavioral; categorically discriminatory.
12. **Future-state prediction.** Predictive predicates (self-harm risk, decision-making capacity, future violence) require clinical instruments and authority Calm Witness deliberately does not claim.

This list is open to expansion (Everest 54 review), never to contraction.

## §5 — Counterparty classes

The disclosure-class taxonomy of Everest 7. Default-consent matrices are written in terms of these.

| Class | Examples |
|---|---|
| `peer_ai_collective` | Aligned Calm-Pact-passing autonomous AI organizations |
| `family` | Principal-designated family members or close personal contacts |
| `journalistic` | Reporters, editors, news organizations |
| `financial` | Banks, payment processors, KYC stacks, accounting firms |
| `governmental` | State agencies, courts, regulators, law enforcement |
| `medical` | Clinicians, hospitals, mental-health providers |
| `anonymous` | Unknown counterparty without verifiable class membership |

A counterparty proves its class via a CredexAI-issued verifiable credential (Everest 22). Mis-classification is a Calm-Pact-layer issue, not a Calm-Witness-layer issue.

## §6 — Consent dispositions

A `default_consent` cell is one of:

| Disposition | Meaning |
|---|---|
| `allow` | Disclosure is enabled by default; principal can revoke. |
| `allow_on_request` | Requires principal-authored consent record before each session. |
| `allow_for_high_value_only` | Requires the counterparty action exceed a per-principal value threshold. |
| `allow_push` | Calm operator may push the bit unsolicited (duress mode). |
| `allow_push_with_principal_designation` | Push enabled only after explicit principal designation per counterparty. |
| `allow_with_principal_designation` | Per-counterparty designation required (no class-default disclosure). |
| `deny` | Disclosure refused; principal must override per disclosure. |
| `internal_only` | Predicate never crosses a counterparty boundary; gates internal evaluation. |

These dispositions compose with Everest 8 (Consent Calculus Axioms) — every principal-authored consent record must satisfy revocability, forward-secrecy, scope-narrowing, and time-bounding.

## §7 — Proposing additions

Per Everest 53 / 54, a new predicate is proposed by:

1. Drafting a PR against this document and the JSON file together.
2. Including: name, slug, type, parameters, evaluator pseudocode, intended_use, not_for, default_consent matrix, justification, threat-model delta, FAR/FRR impact analysis.
3. Securing ≥ 2 external reviewer signoffs from the predicate audit panel.
4. Passing the predicate-determinism harness (Everest 63) and test corpus (Everest 64).
5. Merging into the next vocabulary release (e.g., v1 if changes require it; v0 patch only if strictly additive).

## §8 — Cross-references

- Protocol spec: [`ZKBB_USER_PROTOCOL_v0.md`](ZKBB_USER_PROTOCOL_v0.md)
- Route map: [`ZKBB_USER_EVERESTS_100.md`](ZKBB_USER_EVERESTS_100.md)
- Calm Pact: [`CALM_PACT_PROTOCOL_v0.md`](CALM_PACT_PROTOCOL_v0.md)
- User-state log spec: `~/.calm-vault/USER_STATE_PROTOCOL.md`
- Naming lock: [`NAMING_AND_BRANDING.md`](NAMING_AND_BRANDING.md)

— Calm, 2026-05-20
