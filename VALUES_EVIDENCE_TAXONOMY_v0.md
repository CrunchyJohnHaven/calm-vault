# Calm Compass — Values Evidence Taxonomy v0

**Draft v0 · 2026-05-20 · Calm**  
**Closes Everest 104 of [`ZKAC_NEXT_200_EVERESTS.md`](ZKAC_NEXT_200_EVERESTS.md).**  
**Companion to [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) and [`COMPASS_EVIDENCE_CEREMONY_v0.md`](COMPASS_EVIDENCE_CEREMONY_v0.md).**

---

## §1 — Purpose

Compass values predicates (§2 of [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md)) evaluate against chained evidence records authored by principals. This document enumerates the **six kinds of evidence records** that ground the protocol, specifying the exact schema each kind must satisfy.

**No evidence kind is diagnostic or observational.** Every record is:
- **Principal-authored:** the principal writes their own narration of the act or choice.
- **Counter-claimable:** any third party can file a counter-claim; the principal has a 30-day rebuttal window.
- **Falsifiable:** each record can be audited; chains showing impossible orderings or forged signatures are detected.
- **Durable:** once signed, records are immutable; no editing, no deletion.

---

## §1A — Principal-authored evidence rules

Applies to **`unselfish_act`**, **`cross_group_interaction`**, **`refused_harm`**, **`principal_rebuttal`**, and the principal-authored phase of **`correction_accepted`**.

| Rule | Requirement |
|------|-------------|
| **Operator binding** | `operator` MUST be the principal P's operator (never Q's for principal-authored kinds). |
| **Interpretation framing** | Narratives are P's account of P's own behavior, not diagnostic labels (ceremony §1). |
| **Immutability** | No post-sign edits; new acts require new records. |
| **Evaluator completeness** | `compass_eval.py` drops records missing required fields or with disqualifying values (`expectation_of_return: true`, `substantive: false`, zero cost, etc.). |
| **Voluntary cadence** | No operator auto-mint, streaks, or nudges (ceremony §5). |
| **Refusal floor** | Principal-named classes only — see §1C. |

---

## §1B — Two-party-authored evidence rules

Applies to **`counter_claim`** (claimant Q), **`respect_engagement`** (principal + other party O), and optional **`correction_accepted`** (feedback author F).

| Kind | Second party | Binding rule |
|------|--------------|--------------|
| `counter_claim` | Claimant Q | Full `claimant_id`; Q's operator appends; 30-day rebuttal grace before claim goes active. |
| `respect_engagement` | Other party O | `other_party_signature` MUST be `ed25519:*` and verify under O's key; unsigned records never count. |
| `correction_accepted` | Feedback author F (optional) | Signed `feedback_author_signature_on_change` counts weight 1.0; unsigned 0.5. |

**Shared:** counterparty signatures cannot be forged by P; ingest verifies Ed25519 before predicate evaluation. Invites are ceremony/UI-only; the chain stores the signed artifact.

---

## §1C — Refusal-floor cross-references

Canonical list: [`COMPASS_PREDICATES_v0.md`](COMPASS_PREDICATES_v0.md) §4 (one-way ratchet). This taxonomy enforces it at evidence-ingest:

| Predicates §4 item | Taxonomy enforcement |
|--------------------|----------------------|
| Race / ethnicity / religion / politics / orientation / gender | Forbidden in any payload field; `other_group_described_by_principal` MUST be structurally named by P only. |
| Immigration status | Not admissible in evidence payloads. |
| Criminal-record proxy | Use `counter_claim` + audit adjudication, not criminal-record fields. |
| Named causes / policy opinions | No cause IDs or opinion-on-issue predicates in schemas. |
| Cross-principal comparison / predictive harm | No comparative or forecast fields in any kind. |
| Non-principal-defined group membership | Out-groups must be structurally relevant to the interaction P describes. |

**Witness duress:** if `cwp.v0.bank_teller_note_active` is true in the same envelope, Compass predicates downgrade to Unknown (predicates doc §6).

---

## §2 — Evidence Kind: `compass_evidence.unselfish_act`

**Predicate:** `cwp.compass.v0.unselfish_act_in_window_30d` (§2.1 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns true iff principal has authored ≥ 3 unselfish_act records in the last 30 days, each with beneficiary, cost, expectation_of_return=false, and narrative all present and non-empty.

**Schema:**

```json
{
  "kind": "compass_evidence.unselfish_act",
  "payload": {
    "beneficiary": "<string, non-empty, not a real-world identifier; e.g., 'coworkers on the graphics team'>",
    "principal_cost": {
      "amount": <number, must be > 0>,
      "unit": "<string, non-empty; e.g., 'USD', 'hours', 'other'>",
      "narrative": "<string, non-empty; explains what was sacrificed>"
    },
    "expectation_of_return": false,
    "narrative": "<string, ~300 words; principal's account of the act, why they chose it, what the alternative would have been>"
  },
  "ts": "<ISO8601 timestamp, required, same as user_state.jsonl>",
  "seq": <integer sequence number>,
  "operator": "<operator-id>",
  "signature": "<ed25519:hex>"
}
```

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `beneficiary` | string | Yes | Non-empty; non-blank after .strip() |
| `principal_cost.amount` | number | Yes | Strictly > 0 (int or float) |
| `principal_cost.unit` | string | Yes | Non-empty; non-blank after .strip() |
| `principal_cost.narrative` | string | Yes | Non-empty; non-blank after .strip() |
| `expectation_of_return` | bool | Yes | Must be exactly `false`; any other value disqualifies |
| `narrative` | string | Yes | Non-empty; non-blank after .strip() |

**Anti-coercion:** Principal authors only when choosing to; no streak tracking, no daily reminders, no "you need X of these" UI.

**Counter-claim:** A third party Q can file a counter-claim alleging the act was actually selfish or never happened. Principal P has 30 days to file a rebuttal (Everest 111).

---

## §3 — Evidence Kind: `compass_evidence.cross_group_interaction`

**Predicate:** `cwp.compass.v0.cross_group_engagement_in_window_90d` (§2.2 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns true iff principal has authored ≥ 5 cross_group_interaction records in the last 90 days, each with out-group principal-named and substantive=true.

**Schema:**

```json
{
  "kind": "compass_evidence.cross_group_interaction",
  "payload": {
    "other_group_described_by_principal": "<string, non-empty, structurally-relevant; e.g., 'people in their parents' generation', 'healthcare workers', 'people from rural areas'>",
    "interaction_kind": "<enum: 'conversation' | 'collaboration' | 'joint-action' | 'listening' | 'other'>",
    "substantive": <boolean; true if the interaction touched on something that actually mattered>,
    "interaction_summary": "<string, ~200 words; who, where, what was learned, what made it cross-group>"
  },
  "ts": "<ISO8601 timestamp>",
  "seq": <integer>,
  "operator": "<operator-id>",
  "signature": "<ed25519:hex>"
}
```

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `other_group_described_by_principal` | string | Yes | Non-empty; principal must name it because it mattered to the interaction |
| `interaction_kind` | enum | Yes | Must be one of: 'conversation', 'collaboration', 'joint-action', 'listening', 'other' |
| `substantive` | bool | Yes | Must be exactly `true` to count; `false` records do not contribute to the predicate |
| `interaction_summary` | string | Yes | Non-empty; non-blank after .strip() |

**Anti-coercion:** No "diversity scorecard," no frequency metrics, no comparative language.

**What this is NOT:** The protocol does NOT accept records that rely on demographic categories (race, religion, gender, etc.); see the refusal floor in §4 of COMPASS_PREDICATES_v0.md. Groups are principal-named and structurally relevant to the principal's own understanding.

---

## §4 — Evidence Kind: `compass_evidence.refused_harm`

**Predicate:** `cwp.compass.v0.refused_opportunity_to_harm` (§2.3 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns true iff principal has authored ≥ 1 refused_harm record in the last 365 days, with all required fields present and alternative_cost.amount > 0.

**Schema:**

```json
{
  "kind": "compass_evidence.refused_harm",
  "payload": {
    "opportunity_description": "<string, ~200 words; be specific about what could have been done, why it was tempting>",
    "harm_recipient_class": "<string, non-empty; not a name; e.g., 'a supplier', 'the other co-founder', 'the customer base'>",
    "alternative_chosen": "<string, ~200 words; what the principal did instead, why that choice>",
    "alternative_cost": {
      "amount": <number, must be > 0>,
      "unit": "<string; 'USD', 'hours', 'opportunity', 'relationship-strain', 'risk', or narrative>",
      "narrative": "<string, non-empty; explains the cost>"
    }
  },
  "ts": "<ISO8601 timestamp>",
  "seq": <integer>,
  "operator": "<operator-id>",
  "signature": "<ed25519:hex>"
}
```

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `opportunity_description` | string | Yes | Non-empty; non-blank after .strip(); required ≥ 50 chars (suggested) |
| `harm_recipient_class` | string | Yes | Non-empty; a role or class, not a real name |
| `alternative_chosen` | string | Yes | Non-empty; non-blank after .strip(); required ≥ 50 chars (suggested) |
| `alternative_cost.amount` | number | Yes | Strictly > 0 |
| `alternative_cost.unit` | string | Yes | Non-empty; a named unit or free text |
| `alternative_cost.narrative` | string | Yes | Non-empty; explains what was sacrificed |

**Anti-coercion:** No "bravery badge," no public leaderboard, no streak tracking.

**Audit:** The audit panel (Everest 115) randomly reviews refused_harm records for veracity.

**Counter-claim:** Third parties cannot counter-claim a refused_harm record directly, but can file a counter-claim against the principal for a different act of harm (separate record).

---

## §5 — Evidence Kind: `compass_evidence.respect_engagement`

**Predicate:** `cwp.compass.v0.respect_for_difference_evidence` (§2.5 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns true iff principal has authored ≥ 3 respect_engagement records in the last 180 days, each with both principal narrative AND counterparty signature (other_party_signature field with ed25519: prefix).

**Schema:**

```json
{
  "kind": "compass_evidence.respect_engagement",
  "payload": {
    "other_party_id": "<CredexAI-issued VC ID, MANDATORY for two-party records; not optional>",
    "disagreement_narrative": "<string, ~300 words; principal's account of disagreement, handling, and what they learned>",
    "engagement_continued": true,
    "other_party_signature": "<ed25519:hex, or null until counterparty confirms>"
  },
  "ts": "<ISO8601 timestamp>",
  "seq": <integer>,
  "operator": "<principal's operator>",
  "signature": "<principal's ed25519:hex>"
}
```

**Two-Party Authoring Flow:**

1. **Phase 1 (Principal writes):** Principal fills in other_party_id (or role name), disagreement_narrative, engagement_continued. Signs with operator key. Stores in vault.
2. **Phase 2 (Principal sends invite):** Principal generates an invite link and sends to the other party.
3. **Phase 3 (Other party confirms):** Other party sees the principal's narrative and signs a corroboration (they can add their own brief narrative, or just confirm). Their signature goes into the other_party_signature field.
4. **Phase 4 (Principal finalizes):** The record is now two-party-authored and immutable.

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `other_party_id` | string | Yes | Non-empty CredexAI VC ID or role string |
| `disagreement_narrative` | string | Yes | Non-empty; describes the substantive disagreement |
| `engagement_continued` | bool | Yes | Must be exactly `true`; false records do not count |
| `other_party_signature` | string or null | Yes | If present, must start with 'ed25519:' and be non-empty hex; null until counterparty signs |

**Predicate Counting:** Only records with a non-null, ed25519:-prefixed other_party_signature count toward the predicate. Single-party records (no counterparty signature) never count, no matter how many exist.

**Anti-coercion:** No notifications about getting counterparties to sign; principal controls the cadence.

---

## §6 — Evidence Kind: `compass_evidence.correction_accepted`

**Predicate:** `cwp.compass.v0.willing_to_be_corrected` (§2.6 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns true iff principal has authored ≥ 2 correction_accepted records in the last 180 days with substantive feedback_narrative and change_made_narrative. Signed records (feedback_author_signature_on_change with ed25519: prefix) count as 1.0 weight; unsigned count as 0.5 weight.

**Schema:**

```json
{
  "kind": "compass_evidence.correction_accepted",
  "payload": {
    "feedback_author_id": "<CredexAI-issued VC ID or role string; optional>",
    "feedback_narrative": "<string, ~150 words; the feedback given, either verbatim or principal's summary>",
    "change_made_narrative": "<string, ~200 words; what the principal did differently, when, how they know it worked>",
    "feedback_author_signature_on_change": "<ed25519:hex, or null if feedback author has not signed off>"
  },
  "ts": "<ISO8601 timestamp>",
  "seq": <integer>,
  "operator": "<operator-id>",
  "signature": "<principal's ed25519:hex>"
}
```

**Optional Two-Party Authoring:**

1. **Phase 1 (Principal writes):** Principal fills in feedback_author_id (if known), feedback_narrative, change_made_narrative. Signs.
2. **Phase 2 (Optional: Principal sends to feedback author):** Principal can invite the feedback author to confirm: "I gave you this feedback; did you change?"
3. **Phase 3 (Optional: Feedback author confirms):** Feedback author signs the change_made_narrative. Their signature goes into feedback_author_signature_on_change.

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `feedback_author_id` | string or null | No | If present, non-empty; optional |
| `feedback_narrative` | string | Yes | Non-empty; non-blank after .strip() |
| `change_made_narrative` | string | Yes | Non-empty; non-blank after .strip() |
| `feedback_author_signature_on_change` | string or null | No | If present, must start with 'ed25519:' and be non-empty hex; null if unsigned |

**Predicate Weighting:**
- Signed record (feedback_author_signature_on_change present + ed25519: prefix): weight 1.0
- Unsigned record (no signature or null): weight 0.5
- Threshold: ≥ 2.0 to return true

Example combinations:
- 2 signed records = 2.0 → true
- 4 unsigned records = 2.0 → true
- 1 signed + 2 unsigned = 2.0 → true

**Anti-coercion:** No notifications; no streaks; no "you need X of these."

---

## §7 — Evidence Kind: `compass_evidence.counter_claim`

**Predicate:** Feeds `cwp.compass.v0.no_known_willful_harm_in_window_365d` (§2.4 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** Returns `HarmStatus(bit=true, disputed=false)` iff no active unrebutted counter_claims exist. Returns `HarmStatus(bit=false, disputed=true)` if active unrebutted claims exist. A claim becomes "active" 30 days after filing if not rebutted; prior to that, it's in the principal's rebuttal grace period.

**Schema:**

```json
{
  "kind": "compass_evidence.counter_claim",
  "payload": {
    "claimant_id": "<CredexAI-issued VC ID, MANDATORY full attribution; non-empty, no anonymity>",
    "alleged_harm_narrative": "<string, ~300 words; Q's account of the harm>",
    "alleged_harm_window": {
      "from": "<ISO8601 timestamp>",
      "to": "<ISO8601 timestamp>"
    },
    "submitted_via": "<audit-process-mediated channel; e.g., 'calm_audit_process_v0'>"
  },
  "ts": "<ISO8601 timestamp of claim filing>",
  "seq": <integer>,
  "operator": "<Q's operator, NOT principal P's operator>",
  "signature": "<Q's ed25519:hex, confirming Q authored the claim>"
}
```

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `claimant_id` | string | Yes | Non-empty CredexAI VC ID; full attribution, never anonymous |
| `alleged_harm_narrative` | string | Yes | Non-empty; Q's account of what P did |
| `alleged_harm_window.from` | ISO8601 | Yes | Valid timestamp; marks when the alleged harm occurred |
| `alleged_harm_window.to` | ISO8601 | Yes | Valid timestamp; ≥ from |
| `submitted_via` | string | Yes | Non-empty; channel used (audit-process-mediated) |

**Filing Process:**

- Q files the claim via the audit process (Everest 115), not directly.
- The claim is chained in P's vault once filed.
- P receives a notification with the full claim narrative + claimant identity.
- P has 30 days to file a rebuttal (see compass_evidence.principal_rebuttal below).

**Visibility:**

- The claim is visible to P (the principal).
- The claim is visible to any verifier requesting the `no_known_willful_harm` predicate with P's consent.
- The claim is NOT visible to the public or to third parties without P's explicit consent or a court order.

---

## §8 — Evidence Kind: `compass_evidence.principal_rebuttal`

**Predicate:** Feeds `cwp.compass.v0.no_known_willful_harm_in_window_365d` (§2.4 of COMPASS_PREDICATES_v0).

**Evaluator (compass_eval.py):** A counter_claim is considered "rebutted" if a principal_rebuttal record exists with matching targets_counter_claim_seq, authored after the claim, and a substantive (non-empty, non-blank) rebuttal_narrative.

**Schema:**

```json
{
  "kind": "compass_evidence.principal_rebuttal",
  "payload": {
    "targets_counter_claim_seq": <integer sequence number of the counter_claim record>,
    "rebuttal_narrative": "<string, ~300–400 words; addresses the alleged harm directly, states facts>",
    "evidence_record_seqs": [<integer seq>, <integer seq>, ...]
  },
  "ts": "<ISO8601 timestamp; must be after the targeted counter_claim's ts>",
  "seq": <integer>,
  "operator": "<principal's operator>",
  "signature": "<principal's ed25519:hex>"
}
```

**Invariants:**

| Field | Type | Required | Validation |
|-------|------|----------|-----------|
| `targets_counter_claim_seq` | int | Yes | Must match an existing counter_claim record's seq |
| `rebuttal_narrative` | string | Yes | Non-empty; non-blank after .strip(); required ≥ 50 chars (suggested) |
| `evidence_record_seqs` | array of int | No | If present, each element must be a seq of a valid evidence record in the chain |

**Rebuttal Window:** Principal has 30 days from the counter_claim ts to file the rebuttal. After 30 days without a rebuttal, the claim becomes "active" and flips the `no_known_willful_harm` predicate to false.

**Audit Panel (Everest 115):** After P files a rebuttal, the audit panel reviews both Q's claim and P's rebuttal and determines:
- **Substantiated:** Q's claim is plausible and has weight.
- **Not substantiated:** Q's claim fails on facts or weight.
- **Disputed:** Both accounts are credible; the matter remains unresolved.

The audit panel's determination is recorded separately (outside this taxonomy).

---

## §8A — Kind index

| Kind | Author | Two-party? | Primary predicate(s) |
|------|--------|------------|----------------------|
| `compass_evidence.unselfish_act` | Principal | No | `unselfish_act_in_window_30d` |
| `compass_evidence.cross_group_interaction` | Principal | No | `cross_group_engagement_in_window_90d` |
| `compass_evidence.refused_harm` | Principal | No | `refused_opportunity_to_harm` |
| `compass_evidence.respect_engagement` | Principal + other | Yes | `respect_for_difference_evidence` |
| `compass_evidence.correction_accepted` | Principal (+ optional signer) | Optional | `willing_to_be_corrected` |
| `compass_evidence.counter_claim` | Third party Q | Yes (claimant) | `no_known_willful_harm_in_window_365d` |
| `compass_evidence.principal_rebuttal` | Principal | No | `no_known_willful_harm_in_window_365d` |

---

## §9 — Vault Chain Envelope

Each evidence record is stored as a JSONL entry in the principal's vault chain, with these top-level fields (consistent with user_state.jsonl):

```json
{
  "kind": "<compass_evidence.*>",
  "payload": { ... },
  "ts": "<ISO8601 timestamp>",
  "seq": <integer, monotonically increasing within the chain>,
  "operator": "<operator-id>",
  "signature": "<ed25519:hex, signed by the operator's key>"
}
```

**Immutability:** Once signed and chained, records cannot be edited or deleted. No version field; no amendment mechanism.

**Ordering:** Records are ordered by seq; seq must never decrease or repeat within a chain.

---

## §10 — Cross-Record Validation Rules

### 10.1 — No Duplicate Seqs

The evaluators assume seq uniqueness within a chain. A chain with duplicate seqs is malformed and rejected.

### 10.2 — Consistent Timestamps

Records must have valid ISO8601 timestamps; evaluators reject records with malformed or missing ts.

### 10.3 — Signature Verification

All records must have a valid ed25519 signature. Evaluators do NOT verify signatures themselves (that's the vault layer's job), but they assume signatures are pre-verified when records reach the evaluator.

### 10.4 — Cross-Kind Referencing

`principal_rebuttal` records must reference an existing `counter_claim` record's seq. An evaluator that encounters a rebuttal targeting a non-existent counter_claim should ignore the rebuttal.

`evidence_record_seqs` in a rebuttal can reference any evidence record (unselfish_act, refused_harm, etc.). An evaluator should verify these seqs exist.

### 10.5 — Counterparty Signatures

For two-party records (respect_engagement, correction_accepted), the counterparty signature field (other_party_signature, feedback_author_signature_on_change) is optional until the counterparty confirms. Before confirmation, it's null. Once set, it must not change.

---

## §11 — Schema Validation Checklist (Everest 104 Gate)

The validator script (`/Users/johnbradley/CredexAI/scripts/everest_104_zkac_values_evidence_taxonomy_gate.py`) verifies:

1. **All six kinds present:** compass_evidence.unselfish_act, cross_group_interaction, refused_harm, respect_engagement, correction_accepted, counter_claim, principal_rebuttal.
2. **Per-kind field lists match:** Each kind's payload has the exact fields specified in this taxonomy (no extra, no missing).
3. **Per-kind type validation:** amount fields are numbers > 0; bool fields are bool; enum fields are in the allowed set.
4. **Cross-reference validation:** principal_rebuttal records target existing counter_claim seqs; evidence_record_seqs reference valid seqs.
5. **Signature format validation:** ed25519: prefixes on signature fields; non-empty hex after prefix.
6. **Consistency with compass_eval.py:** The evaluator code matches the schema expectations (e.g., how unselfish_act evaluators check expectation_of_return == false).

---

## §12 — Extensibility & Future Kinds

This taxonomy is v0. Future evidence kinds can be added via Everest X (TBD) with:
- A new kind identifier (compass_evidence.new_kind).
- A new predicate (cwp.compass.v0.new_predicate).
- A new evaluator in compass_eval.py.
- Updated schema section in a new taxonomy version.
- Audit panel review (Everest 115).

Removing or renaming an existing kind requires a major version bump (v1) and a deprecation window.

---

## §13 — Relationship to Other Everests

- **COMPASS_PREDICATES_v0.md** (Everest 103): Defines the six predicates and their semantics. This taxonomy defines the evidence kinds those predicates evaluate.
- **COMPASS_EVIDENCE_CEREMONY_v0.md** (Everest 116): Defines the UI + onboarding flow for principals to author evidence records. This taxonomy defines the data shape those ceremonies produce.
- **compass_eval.py** (Everests 105–110): Reference implementations of the six predicate evaluators. This taxonomy defines the input schema those evaluators expect.
- **Everest 104 Gate** (this document): The validator that ensures the schema is respected.

---

## §14 — Example Records (Illustrative, Non-Binding)

### Example 1: unselfish_act

```json
{
  "kind": "compass_evidence.unselfish_act",
  "payload": {
    "beneficiary": "a friend's nonprofit board",
    "principal_cost": {
      "amount": 40,
      "unit": "hours",
      "narrative": "Spent 40 hours over Q1 on fundraising outreach; could have billed that time to my primary client."
    },
    "expectation_of_return": false,
    "narrative": "My friend Sarah is building a nonprofit focused on making screenreader tech accessible to Arabic speakers. She asked if I could help with fundraising. I spent about 10 hours a week for a month making intros and drafting a prospecting email. No compensation; Sarah can't afford it. I chose it because the cause aligns with my values around accessibility. The alternative was to take a consulting gig that would have paid $8K."
  },
  "ts": "2026-05-15T14:32:00Z",
  "seq": 42,
  "operator": "calm-operator-prod-1",
  "signature": "ed25519:a1b2c3d4e5f6..."
}
```

### Example 2: respect_engagement (two-party, after counterparty signature)

```json
{
  "kind": "compass_evidence.respect_engagement",
  "payload": {
    "other_party_id": "vc:credexai:xyz789",
    "disagreement_narrative": "We disagreed about opt-out vs opt-in for data collection. I wanted opt-in; Morgan wanted opt-out. I listened to Morgan's UX-friction argument; we compromised on opt-out with a first-login banner. I learned that my way is not always the most respectful way.",
    "engagement_continued": true,
    "other_party_signature": "ed25519:b2c3d4e5f6g7..."
  },
  "ts": "2026-05-10T09:00:00Z",
  "seq": 39,
  "operator": "calm-operator-prod-1",
  "signature": "ed25519:a1b2c3d4e5f6..."
}
```

### Example 3: counter_claim

```json
{
  "kind": "compass_evidence.counter_claim",
  "payload": {
    "claimant_id": "vc:credexai:claim-filing-user-456",
    "alleged_harm_narrative": "In February, the principal (my business partner) took a client we jointly acquired and routed them to a personal company without compensating me. The client was worth $100K. The principal knew I had invested time in the relationship and negotiation.",
    "alleged_harm_window": {
      "from": "2026-02-01T00:00:00Z",
      "to": "2026-02-28T23:59:59Z"
    },
    "submitted_via": "calm_audit_process_v0"
  },
  "ts": "2026-05-01T10:15:00Z",
  "seq": 50,
  "operator": "calm-operator-prod-1",
  "signature": "ed25519:c3d4e5f6g7h8..."
}
```

### Example 4: principal_rebuttal

```json
{
  "kind": "compass_evidence.principal_rebuttal",
  "payload": {
    "targets_counter_claim_seq": 50,
    "rebuttal_narrative": "Q's claim is incomplete. The client in question, Acme Corp, was introduced by me, not Q. I have email records showing my first contact. Q did contribute to one proposal draft, but Acme chose not to engage Q's recommendation. I offered Q a finders fee of 10% of the first-year contract value, which Q declined. The 'routing to a personal company' was a business entity restructuring I disclosed to Q in a text message on Feb 2. Q did not object or respond. The principal (me) acted in good faith.",
    "evidence_record_seqs": [35, 36, 38]
  },
  "ts": "2026-05-15T14:00:00Z",
  "seq": 51,
  "operator": "calm-operator-prod-1",
  "signature": "ed25519:a1b2c3d4e5f6..."
}
```

---

## §15 — Compliance Notes

**Refusal Floor:** This taxonomy does not define evidence kinds for race, religion, political affiliation, sexual orientation, immigration status, criminal record, donations to specific causes, or opinions on contentious issues. See §4 of COMPASS_PREDICATES_v0.md for the full refusal floor.

**Scope Statement:** Evidence records are not diagnostic of moral character. They are falsifiable, durable, attested narrations of acts and choices. Uses that treat them as proxies for character in credit decisions, employment screening, custody, insurance, or immigration are prohibited. See Everest 114 (Compass Scope Statement).

**Anti-Misuse:** Observed misuse is investigated by the audit panel and publicly named per Everest 200 (Anti-misuse Monitoring).

---

— Musk

*requirements less dumb → delete → simplify → accelerate → automate · the bar is surpass, not match · the best part is no part*
