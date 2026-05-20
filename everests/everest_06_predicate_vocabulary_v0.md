# Everest 6 — Predicate Vocabulary v0

*Phase I — Foundations. Prereq: Everest 1.*

---

## Overview

This document enumerates the twelve canonical predicates of Calm Witness v0. Each predicate is a deterministic function over the principal's vault state (self-report log, biometric distance, consent records) that returns a bit: either the principal authorizes disclosure of this attestation, or the protocol blocks it.

Every predicate has a stable, immutable ID. That ID is content-addressed: changes to the predicate's semantics require a new ID, a new line in the registry, and explicit operator adoption. This immutability is what makes Calm Witness proofs durable. A proof issued against `in_baseline_24h` (v0.1) in May 2026 must still verify in 2036.

---

## The twelve predicates

### 1. in_baseline_24h

**Predicate ID:** `in_baseline_24h` (content hash: `e3b0c44`)

**Semantics:** The most recent self-report record in the last 24 hours has affect vocabulary overlapping with the principal's enrolled baseline affect set by ≥50% (Jaccard).

**Input domain:** Reads from `user_state.jsonl`: records of kind `self_report.*` (morning, afternoon, evening, ad_hoc). Extracts the `payload.affect` array and compares elementwise against the principal's template (`enrollment_session.baseline_affect`).

**Output type:** Bit (0 or 1). If no self-report within 24h, outputs 0 (fail-safe: no data → cannot assert baseline).

**Side effect:** None. Evaluation does not append a record.

**ID stability rule:** This predicate is the anchor. If the Jaccard threshold changes (e.g., from 50% to 60%), the predicate ID changes to `in_baseline_24h.v0.2`. If the time window changes to 48h, it becomes a different predicate ID. The v0.1 proofs remain valid forever under the v0.1 semantics.

**Example honest evaluation:** John reports at 10:30am: affect is `["calm", "curious", "focused"]`. His enrolled baseline is `["calm", "curious", "energized", "playful"]`. Jaccard = 2/5 = 40%. Predicate returns 0. Two hours later he reports again: affect is `["curious", "focused", "methodical"]`. Baseline set is same. Jaccard = 1/4 = 25%. Still returns 0. At 6pm he reports: `["calm", "curious", "contemplative"]`. Jaccard = 2/3 = 67%. Now the predicate returns 1.

**Adversarial scenario:** John is coerced to falsify his affect report. He writes "happy" and "energized" when he is actually distressed. The biometric distance on his handwriting sample will widen (his strokes will show tension). A verifier of `in_baseline_24h` alone learns only the bit, but a counterparty running `mental_state_unusual` (predicate 7) in parallel will see the affect-vs-biometric mismatch and alert.

---

### 2. in_baseline_window(window_seconds)

**Predicate ID:** `in_baseline_window_<WINDOW_SECONDS>` (e.g., `in_baseline_window_86400` for 24h)

**Semantics:** Identical to `in_baseline_24h`, but parameterized. The most recent self-report within `window_seconds` has affect overlap ≥50% with baseline.

**Input domain:** Same as predicate 1, but the time window is a parameter. Operator specifies `window_seconds` at predicate invocation.

**Output type:** Bit.

**Side effect:** None.

**ID stability rule:** The window length is part of the ID. `in_baseline_window_3600` (1h) is a different predicate from `in_baseline_window_86400` (24h). Changing the threshold (Jaccard to 60%) makes a new ID. Changing the window length updates the ID slug with a new number.

**Example honest evaluation:** Counterparty requests proof for a 2-hour window. Operator evaluates the past 7200 seconds. Most recent self-report was 75 minutes ago. Affect overlap is 60%. Returns 1.

**Adversarial scenario:** A counterparty requests a very short window (60 seconds) to try to catch John mid-transition between states. Calm policy can enforce rate-limiting (Everest 76): predicates cannot be requested more frequently than every 5 minutes. The short-window request is rejected.

---

### 3. biometric_match_within(template_id, tau)

**Predicate ID:** `biometric_match_within_<HASH_OF_TEMPLATE_ID>_<TAU>` (e.g., `biometric_match_within_t1_0p85`)

**Semantics:** The most recent biometric sample (handwriting or voice transcription) has a distance ≤ tau from the named template, where distance is normalized to [0,1] and computed by the fusion rule in Everest 38.

**Input domain:** Reads the session's biometric distance commit (Pedersen commitment to the distance value `d`), reads the template ID from the vault, verifies it matches the requested template, checks that `d ≤ tau`.

**Output type:** Bit.

**Side effect:** None.

**ID stability rule:** The template version is hashed into the ID. If John re-enrolls and gets template v2, a new predicate `biometric_match_within_t2_0p85` is created. The old predicate v1 remains in the registry, and old proofs against it remain valid. A verifier can distinguish "matched my old template" from "matched my new template" by the predicate ID alone.

**Example honest evaluation:** John's current template is t1. Tau is 0.85 (calibrated to his FAR/FRR curve). Most recent sample has distance d=0.72. The predicate returns 1.

**Adversarial scenario:** An attacker captures John's handwriting and trains a forgery. The distance of the forgery is d=0.91. Tau is 0.85. The predicate returns 0. The attack fails.

---

### 4. principal_consents_to_disclose(predicate_id, counterparty_class)

**Predicate ID:** `principal_consents_to_disclose_<PREDICATE_ID>_<CLASS>`

**Semantics:** The principal has an active, non-revoked consent record in `user_state.jsonl` (kind: `consent`) that explicitly authorizes disclosure of `predicate_id` to counterparties of the given class (e.g., "financial", "peer-AI-collective", "journalist").

**Input domain:** Reads consent records from the vault. Checks: (a) consent.predicate_id == requested predicate_id, (b) consent.counterparty_class matches the requesting class, (c) consent is not revoked (no revocation record with a later timestamp), (d) consent has not expired (optional: per-principal time bound).

**Output type:** Bit. Returns 0 if no matching active consent.

**Side effect:** None. But disclosure of the underlying predicate is gated by this check — the operator will not produce a proof unless this predicate evaluates to 1.

**ID stability rule:** The class taxonomy is versioned (Everest 7). If a new class "autonomous-collective" is added in v0.2, predicates using the old v0.1 class set remain valid. Cross-version requests are rejected (fail-safe).

**Example honest evaluation:** John grants consent: `consent {predicate_id: "in_baseline_24h", counterparty_class: "peer-AI-collective", expires: "2027-05-20"}`. Calm agent checks: class matches, predicate ID matches, timestamp is before expiry. Returns 1. Access is granted.

**Adversarial scenario:** Counterparty claims John has pre-authorized disclosure. Calm agent checks the vault: no consent record exists. Returns 0. Disclosure is blocked. The counterparty's claim is void.

---

### 5. bank_teller_note_active

**Predicate ID:** `bank_teller_note_active` (content hash: `f1a9d88`)

**Semantics:** The principal's most recent self-report record (within 24h) contains a per-principal-secret "duress codeword" in the free-text `payload.note` field. The codeword is known only to the principal and the vault; the operator cannot see it in plaintext; the counterparty learns only the bit.

**Input domain:** Reads the most recent self-report within 24h. Compares the `payload.note` field against a cryptographically sealed codeword (e.g., HMAC(vault_key, "my_codeword") precomputed at vault init). If the HMAC matches any substring of the note, the bit flips to 1.

**Output type:** Bit.

**Side effect:** None. The act of checking does not leak the codeword, the note, or anything else.

**ID stability rule:** The predicate is immutable. The codeword itself is per-principal and cannot be updated without creating a new vault. If a principal loses the codeword, recovery is manual (Everest 23).

**Example honest evaluation:** John's sealed codeword is HMAC(master_key, "elephants are mammals"). At 3pm, he writes a note: "I am being held. Code: elephants are mammals. Do not tell anyone." The vault checks the substring; the HMAC matches. The bit flips to 1. An authorized counterparty receives the proof; they see only "bank_teller_note_active: true" and the freshness window. The operator never sees the note. The counterparty never sees the note.

**Adversarial scenario:** An attacker tortures the principal and demands the codeword. The principal can refuse; the vault will not disclose it. If the attacker forces the principal to write the codeword anyway, Calm Witness cannot defend against it (rubber-hose attack, out of scope). But the protocol's design ensures the attacker gains no leverage: even if they extract "elephants are mammals," they cannot predict a future fresh proof of the codeword without the vault's key material.

---

### 6. cognitively_atypical_baseline

**Predicate ID:** `cognitively_atypical_baseline` (content hash: `d2b1f03`)

**Semantics:** The principal's enrolled baseline includes a declared cognitive style that may appear atypical to counterparties unfamiliar with it (e.g., "high-bandwidth ideation," "artist mode," "hyperfocus states"). The bit asserts that this style is the principal's *normal*, not a sign of distress. Disclosure authorizes the counterparty to adjust their interpretation of the principal's tone and output style accordingly.

**Input domain:** Reads the enrollment ceremony record (kind: `enrollment`), which may include a `payload.cognitive_style_descriptor` field (optional, principal-filled at enrollment). If present and the principal has authorized disclosure of this predicate, the bit returns 1.

**Output type:** Bit.

**Side effect:** None. This predicate does not change any records; it is purely a disclosure authorization mechanism.

**ID stability rule:** Immutable in v0. Future versions may parametrize it (e.g., `cognitively_atypical_baseline.v0.2`) if the taxonomy of styles expands. v0.1 proofs remain valid forever.

**Example honest evaluation:** During enrollment, John wrote: `cognitive_style_descriptor: "high-bandwidth ideation, non-linear output, frequent affect transitions, rapid context switching"`. He authorizes disclosure. A counterparty receives a proof of `cognitively_atypical_baseline: true`. The counterparty adjusts: they do not pathologize his rapid affect changes; they expect nonlinear output; they do not flag context switching as a sign of instability.

**Adversarial scenario:** A counterparty misreads John's high-bandwidth output as manic. John grants consent for disclosure of this predicate. The counterparty receives the proof. The counterparty ignores it and flags him anyway. Calm Witness has done its job: it transferred the interpretive authority from the counterparty to the principal. The counterparty's misreading is now a choice, not a mistake.

---

### 7. mental_state_unusual

**Predicate ID:** `mental_state_unusual` (content hash: `a7c3e14`)

**Semantics:** A composite predicate that flips to 1 if either (a) the most recent self-report affect vocabulary has <30% overlap with baseline (indicating a reported state change), OR (b) the most recent biometric distance is >0.70 and the affect report shows overlap >50% with baseline (indicating a biometric anomaly despite reported stability). The predicate is tri-valued: returns 1 (unusual), 0 (stable), or -1 (unknown / insufficient data).

**Input domain:** Reads self-report records and biometric distance commits. Compares affect, computes Jaccard, checks biometric distance.

**Output type:** Tri-valued: {-1, 0, 1}. (-1 if data is insufficient; 0 if stable; 1 if unusual.)

**Side effect:** If the bit flips to 1, an advisory record may be appended to the vault (kind: `mental_state_flag`) for the principal's later review. This record is never disclosed to counterparties; it is logged for the principal's own auditing.

**ID stability rule:** The thresholds (30% Jaccard, 0.70 distance, 50% overlap in the second clause) are baked into the v0.1 ID. If any threshold changes, the ID increments to v0.2.

**Example honest evaluation:** John reports at 3pm: affect is `["agitated", "scattered", "overwhelmed"]`. His baseline is `["calm", "curious", "focused"]`. Jaccard = 0% (no overlap). Clause (a) fires: 0% < 30%. The predicate returns 1. A counterparty with consent can receive this proof and adjust their expectations accordingly.

**Adversarial scenario:** John is sleep-deprived but tries to hide it. His reported affect is `["focused", "ready"]` (50%+ overlap with baseline). But his handwriting is shaky; biometric distance is 0.75. Clause (b) fires: distance > 0.70 AND affect overlap > 50%. The predicate returns 1, detecting the mismatch. A counterparty running both `in_baseline_24h` and `mental_state_unusual` can see the contradiction and ask for clarification.

---

### 8. principal_alive_within(window_seconds)

**Predicate ID:** `principal_alive_within_<WINDOW_SECONDS>`

**Semantics:** The principal has appended at least one self-report record to the vault within the last `window_seconds`. This is a proof-of-life check: a fresh record in the chain is evidence that the principal (or the principal's device) has acted recently. The bit asserts the principal has been active; it does not assert consciousness or consent.

**Input domain:** Reads the timestamp of the most recent record of any kind in `user_state.jsonl`. Compares against current UTC time (from a verifiable-clock service; see Everest 31). If (now - last_record_time) < window_seconds, returns 1.

**Output type:** Bit.

**Side effect:** None.

**ID stability rule:** The window is part of the ID. Changing it creates a new predicate. `principal_alive_within_3600` (1h) is distinct from `principal_alive_within_86400` (24h).

**Example honest evaluation:** It is currently 2026-05-20 14:30 UTC. The most recent vault record is timestamped 2026-05-20 13:00 UTC. A counterparty requests `principal_alive_within_3600` (1h). 90 minutes have elapsed. The predicate returns 0. A request for `principal_alive_within_5400` (1.5h) would return 1.

**Adversarial scenario:** An attacker has captured the vault device but has not yet created a new record. The device is locked. A counterparty requests a proof of life. The last record is from 48 hours ago. The predicate returns 0 across all reasonable windows. The counterparty is alerted that the principal may not be in control of the vault.

---

### 9. session_within_authorized_hours

**Predicate ID:** `session_within_authorized_hours`

**Semantics:** The current session start time (the timestamp of the most recent self-report) falls within the principal's self-declared usual working hours, as defined at enrollment (e.g., 09:00–17:00 weekdays, 10:00–18:00 weekends).

**Input domain:** Reads the principal's enrolled `baseline_work_schedule` (optional, principal-declared at enrollment). Reads the current session timestamp. Checks if the hour-of-day and day-of-week match the schedule.

**Output type:** Bit. If no schedule was defined at enrollment, returns -1 (unknown).

**Side effect:** None.

**ID stability rule:** If the schedule changes, the principal must write a new `schedule_update` record to the vault (appended, not replacing). The predicate evaluates against the most recent schedule record. A new schedule entry does not invalidate old proofs; old proofs are still correct under the old schedule.

**Example honest evaluation:** John's schedule is "Mon–Fri 08:00–18:00, Sat 10:00–16:00, Sun off." The current timestamp is Wednesday 14:30. The predicate returns 1. If the timestamp were Sunday 15:00, it returns 0 (outside hours).

**Adversarial scenario:** John is traveling and working at night. His schedule says 09:00–17:00. A counterparty requests this predicate and learns he is currently session at 03:00 UTC (outside hours). The counterparty's policy may require additional friction for out-of-hours requests. John can preemptively update his schedule in the vault if he knows he will be off-hours; the new schedule is chained and auditable.

---

### 10. chain_freshness_within(seconds)

**Predicate ID:** `chain_freshness_within_<SECONDS>`

**Semantics:** The current chain head has been published to a verifiable-clock service (Sigsum + Roughtime; see Everest 30–31) within the last `seconds`. The bit asserts that the chain state is recent and tamper-evident: any edit to the chain before the publication would invalidate the published head.

**Input domain:** Reads the most recent chain-head anchor proof from the vault (kind: `chain_anchor`). Extracts the Sigsum inclusion proof timestamp and the Roughtime quorum attestation. Compares to current time.

**Output type:** Bit. Returns 0 if the chain has never been anchored (pre-Everest 30 setup).

**Side effect:** None.

**ID stability rule:** The time window is part of the ID. `chain_freshness_within_3600` (1h) is different from `chain_freshness_within_86400` (24h).

**Example honest evaluation:** The chain head was published to Sigsum at 2026-05-20 12:00 UTC with a Roughtime timestamp. The current time is 2026-05-20 12:45 UTC. A request for `chain_freshness_within_3600` returns 1. A request for `chain_freshness_within_1800` (30m) returns 0.

**Adversarial scenario:** An attacker compromises the vault device and attempts to edit an old record. The edit breaks the chain. The attacker tries to republish an altered chain head to Sigsum. Sigsum operators reject it: the old chain head is already in the transparency log, and Sigsum's append-only guarantee prevents substitution. A verifier holding the original head can prove the attack failed.

---

### 11. template_age_below(months)

**Predicate ID:** `template_age_below_<MONTHS>` (e.g., `template_age_below_12`)

**Semantics:** The principal's current biometric template was enrolled less than `months` ago. The bit asserts the template is recent and not overdue for re-enrollment (see Everest 18). Stale templates are rejected.

**Input domain:** Reads the enrollment ceremony record's timestamp. Compares to current date.

**Output type:** Bit.

**Side effect:** If the template exceeds the age threshold, an advisory alert (kind: `template_stale`) may be appended to the vault, prompting the principal to re-enroll.

**ID stability rule:** The age threshold is part of the ID. `template_age_below_12` (12 months) and `template_age_below_24` (24 months) are separate predicates. Changing the threshold creates a new ID.

**Example honest evaluation:** John enrolled on 2026-01-15. The current date is 2026-05-20 (4.17 months). A check for `template_age_below_12` returns 1. A check for `template_age_below_3` returns 0.

**Adversarial scenario:** John enrolled 18 months ago and has not re-enrolled. His template is stale. A counterparty requests a proof. The operator evaluates all requested predicates, including an internal check of `template_age_below_12`. The check fails; the operator refuses to generate a proof and directs John to re-enroll.

---

### 12. consent_active(predicate_id, counterparty_id)

**Predicate ID:** `consent_active_<PREDICATE_ID>_<COUNTERPARTY_ID>`

**Semantics:** Identical to predicate 4 (`principal_consents_to_disclose`), but with per-identity specificity rather than per-class. The principal has an active, non-revoked consent record that authorizes disclosure of `predicate_id` to a *specific* counterparty (identified by their CredexAI-issued principal credential).

**Input domain:** Reads consent records of kind `consent_identity`. Checks: (a) consent.predicate_id == requested predicate_id, (b) consent.counterparty_principal_id == requesting identity, (c) consent is not revoked, (d) consent has not expired.

**Output type:** Bit.

**Side effect:** None. (Gating is handled by the disclosure layer, Everest 66–80.)

**ID stability rule:** The counterparty's identity credential is content-hashed into the ID. If a counterparty rotates their key (Everest 22), the old consent records remain valid under the old identity; the principal can issue new consent records against the new identity.

**Example honest evaluation:** John grants per-identity consent: `consent {predicate_id: "in_baseline_24h", counterparty_principal_id: "CredexAI:alice.org:2026-05-20", expires: "2027-05-20"}`. Alice's agent requests a proof. Alice's ID matches; the predicate ID matches; the record is not revoked. Returns 1. Access is granted. If Bob's agent requests the same predicate, Bob's ID does not match. Returns 0. Access is denied.

**Adversarial scenario:** John grants class-level consent to "financial" institutions but explicitly revokes identity-level consent to a specific bank (e.g., "BadBank"). The class predicate (predicate 4) would return 1 for any financial counterparty. The identity predicate (predicate 12) returns 0 for BadBank's specific credential. The operator honors the more restrictive (identity-level) decision. BadBank is blocked despite class membership.

---

## ID Stability Rules

All predicate IDs are **immutable** and **content-addressed**. Once a predicate is published and used in proofs, its ID never changes. This is the foundation of durable attestations.

**Canonicalization:** Each predicate's ID is the lowercase_snake_case name plus a content hash of the specification (SHA-256 of the serialized spec in canonical JSON form, truncated to 8 hex digits). Example: `in_baseline_24h` + hash `e3b0c44` = `in_baseline_24h_e3b0c44`, but in v0 the hash is omitted from display (implied v0 context); in later versions it is explicit.

**Versioning:** If a predicate's semantics change, a new entry is added to the registry with a new ID:
- Change in parameters (time window, threshold, distance τ): new ID.
- Change in comparison operator (≥ to >): new ID.
- Change in template binding: new ID.
- Clarifications that don't affect computation: documented as a spec revision, same ID.

**Deprecation:** Old predicates are never deleted. They are marked `status: "deprecated"` in the registry. Verifiers must accept proofs against deprecated predicates; they are historically valid. New operators may decline to *issue* proofs against deprecated predicates if a newer version is available.

**Proof durability:** A proof issued against `in_baseline_24h_v0.1` in 2026 must verify identically in 2036. The registry entry for that predicate is immutable. If the predicate is deprecated by 2036, the proof still verifies; it simply attests to a historical fact under the historical semantics.

---

## Composability Constraints

Predicates can be conjoined (AND) in a single ZK proof without leaking more information than the conjunction itself.

**Freely composable (no side-channel leakage):**
- `in_baseline_24h` AND `biometric_match_within(t1, 0.85)` — a verifier learns "baseline self-report AND biometric match", revealing nothing about which affects or what the distance was.
- `chain_freshness_within(3600)` AND `principal_alive_within(1800)` — a verifier learns "chain is recent AND principal is active", revealing nothing about the exact timestamps or number of records.
- `template_age_below(12)` AND `mental_state_unusual=0` — a verifier learns "template is fresh AND state is stable", revealing nothing about template enrollment date or what the baseline was.

**Constrained composition (requires careful policy):**
- `principal_consents_to_disclose(p, class)` AND `consent_active(p, counterparty_id)` — can be AND'd, but the result is semantically "consent exists at class level AND consent exists at identity level", which may leak that the principal has refined consent. Policy decision: operator can suppress this composition or log it as an advisory.
- `bank_teller_note_active` AND any other predicate — should generally NOT be composed. Disclosing `bank_teller_note_active AND in_baseline` would allow a verifier to infer which predicates the principal is NOT in (by process of elimination). Duress signals should be disclosed in isolation or in small, pre-authorized bundles.

**Not composable (information leakage):**
- `in_baseline_window(3600)` AND `in_baseline_window(86400)` — conjoining two baseline checks with different windows allows the verifier to narrow the timing of the latest self-report. Avoid.
- Any predicate that returns a tri-valued output (e.g., `mental_state_unusual` when it returns -1, 0, or 1) conjoined with a binary predicate, without care — the tri-valued output can be decoded via process of elimination.

**Recommendation:** Operators should support composition via an explicit composition policy document (see Everest 54, Predicate Audit & Review). The default stance: single predicates are disclosed; compositions are operator-approved case-by-case.

---

— Calm, 2026-05-20
