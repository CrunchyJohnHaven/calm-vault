# Everest 55 — `in_baseline_24h` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 26.*

---

## Canonical Specification

**Name:** `in_baseline_24h`  
**Version:** `1.0.0`  
**Created:** 2026-05-20T11:00:00-04:00

### Purpose

Returns a tri-valued result (true / false / indeterminate) coupled with a freshness signal, answering the question: *Has the principal self-reported a baseline affect state within the last 24 hours?* This predicate is the foundation for low-risk principal attestation in trust classes where the counterparty needs assurance that the principal is currently in their enrolled baseline physiological and psychological state.

### Description

The predicate evaluates the most recent self-report record in the principal's vault chain that falls within a 24-hour lookback window (86400 seconds, UTC). If a qualifying record exists, the predicate inspects three conditions: (1) whether the reported affect overlaps with the principal's enrolled baseline vocabulary, (2) whether the reported restedness level is in the allowed baseline set, and (3) whether no known health issues were declared. The predicate returns TRUE only if all three conditions hold. If no self-report record exists in the window, the predicate returns INDETERMINATE (not false). Freshness is always reported as seconds elapsed since the most-recent self-report timestamp.

### Input Domain

- **Kind:** `self_report.*` records from the user_state.jsonl chain
- **Window:** Most recent 86400 seconds (24 hours) from roughtime-attested now
- **Scope:** Records authored by the principal; cannot be overridden by counterparty or intermediary

### Output Type

`bit_with_freshness`  
- **Bit:** Tri-valued (true, false, indeterminate)
- **Freshness:** Unsigned integer, seconds since most-recent self_report record timestamp to evaluation time (now)
- **Freshness on Indeterminate:** `null` if no record in window, or explicit reason string if principal profile unavailable

### Parameters

None in v1.0.0. The 24-hour window is hardcoded at 86400 seconds. Predicates supporting arbitrary window sizes are separate (e.g., `in_baseline_window`), each with their own predicate ID to preserve proof linearity and auditability.

### Side Effects

The predicate appends a `kind: "predicate_evaluated"` record to the chain at evaluation time:

```json
{
  "kind": "predicate_evaluated",
  "ts": "2026-05-20T11:15:33.123Z",
  "payload": {
    "predicate_id": "in_baseline_24h",
    "predicate_version": "1.0.0",
    "evaluation_ts": "2026-05-20T11:15:33.123Z",
    "result_bit": true,
    "freshness_seconds": 3598,
    "chain_head_at_eval": "sha256:abc123...",
    "window_start_ts": "2026-05-19T11:15:33.123Z",
    "window_end_ts": "2026-05-20T11:15:33.123Z",
    "most_recent_self_report_ts": "2026-05-20T10:25:35.000Z",
    "trigger_source": "manual_query" | "proof_generation" | "scheduled_check"
  }
}
```

This record is immutable once written and participates in chain integrity (E26).

---

## Evaluation Algorithm

### Pseudocode (Functional)

```
fn in_baseline_24h(chain: &Chain, principal_id: &str) -> (Bit, Freshness) {
    let now = roughtime_now();  // absolute UTC time, E31
    let window_start = now - 86400;
    let window_end = now;
    
    // 1. Fetch principal profile from chain (kind: "profile.affect_vocabulary_set")
    let principal_profile = chain.resolve_profile(principal_id);
    if principal_profile.is_none() {
        return (Bit::Indeterminate, Freshness::Reason("principal_profile_not_initialized"));
    }
    let baseline_vocabulary = principal_profile.unwrap().baseline_affect_vocabulary;
    
    // 2. Query self-report records in the window
    let candidates = chain.records_in_range(window_start, window_end)
        .filter(|r| r.kind.starts_with("self_report."))
        .collect::<Vec<_>>();
    
    if candidates.is_empty() {
        return (Bit::Indeterminate, Freshness::Null);
    }
    
    // 3. Select most recent record (chain order guarantees this is the youngest)
    let most_recent = candidates.last().unwrap();
    let freshness_seconds = (now - most_recent.ts).as_secs();
    
    // 4. Extract and validate payload fields
    let affect_list = &most_recent.payload.affect;  // Vec<String>
    let restedness = &most_recent.payload.restedness;  // String
    let known_issues = &most_recent.payload.known_health_issues;  // Vec<String>
    
    if affect_list.is_empty() {
        return (Bit::Indeterminate, Freshness::Seconds(freshness_seconds));
    }
    
    // 5. Apply three-part test
    let affect_overlap = affect_list.iter()
        .any(|a| baseline_vocabulary.contains(a));
    
    let restedness_ok = matches!(restedness.as_str(),
        "fully_rested" | "rested" | "well_rested");
    
    let no_issues = known_issues.is_empty();
    
    // 6. Compute result
    let result_bit = affect_overlap && restedness_ok && no_issues;
    
    (Bit::from(result_bit), Freshness::Seconds(freshness_seconds))
}
```

### Semantic Clarifications

1. **Affect Overlap:** The self-report's affect list is treated as a set. The predicate returns true if ANY element in that set appears in the principal's enrolled baseline vocabulary. This is an inclusive OR across the reported affects.

2. **Restedness Enum:** Only three values are considered baseline: "fully_rested", "rested", "well_rested". Values like "tired", "sleep_deprived", "ok", or "recovering" evaluate to restedness_ok = false and cause the predicate to return FALSE.

3. **Health Issues:** The presence of ANY non-empty string in the `known_health_issues` list causes no_issues = false. The predicate does not inspect the severity or nature of the issue; any health concern reported makes the predicate return FALSE. This is conservative and appropriate for high-assurance proof contexts.

4. **Most-Recent-Only:** If multiple self-report records exist in the 24-hour window, only the most recent (youngest) is inspected. Older reports, even if they would satisfy the test, are ignored.

5. **Indeterminate is Not False:** Returning Indeterminate signals "I do not have enough information," not "the principal is out of baseline." Consuming systems (proof verifiers, counterparties) treat Indeterminate according to policy—default is conservative (treat as "not baseline"), but low-risk classes can opt-in to "treat as baseline" via configuration (Everest 7 classes).

6. **UTC Absolute Time:** The 24-hour window uses UTC absolute time (roughtime-attested). The principal's local timezone is recorded in their profile and self-report metadata for human readability, but does not affect window calculation.

---

## Principal's Baseline Affect Vocabulary

For John Bradley, established at enrollment (2026-05-20):

```json
{
  "baseline_affect_vocabulary": [
    "calm",
    "even-keeled",
    "curious",
    "ready_to_work",
    "good spirits",
    "rested",
    "alert",
    "focused"
  ]
}
```

This list is stored in the vault at `~/.calm-vault/principal_profile.json` and chained into the vault via a `kind: "profile.affect_vocabulary_set"` record. The principal can update their baseline vocabulary by appending a new `kind: "profile.affect_vocabulary_update"` record; the predicate always resolves to the most recent update.

The principal's authority over their own baseline is fundamental. The protocol does not enforce a universal baseline; the principal's self-narration is authoritative. The companion predicate `cognitively_atypical_baseline` (Everest 59, the artist clause) can be used in tandem to signal that the principal's baseline includes high-bandwidth ideation and non-linear thinking patterns.

---

## Allowed Baseline Restedness Values

```
ALLOWED_BASELINE_RESTEDNESS = {
    "fully_rested",
    "rested",
    "well_rested"
}
```

Any value outside this set causes the predicate to return FALSE. Common non-baseline values include:

- "tired"
- "sleep_deprived"
- "ok"
- "recovering"
- "slightly tired"
- "wired"

---

## Golden Test Corpus

### Test Case 1: Recent Baseline Report (Positive Path)
**Input:**  
Most recent self_report at now - 12h:
```json
{
  "kind": "self_report.state",
  "ts": "2026-05-20T10:25:35.000Z",
  "payload": {
    "affect": ["calm", "curious"],
    "restedness": "fully_rested",
    "known_health_issues": []
  }
}
```
Baseline vocabulary: ["calm", "even-keeled", "curious", "ready_to_work", "good spirits", "rested", "alert", "focused"]

**Expected Output:**  
- Bit: TRUE
- Freshness: 43200 seconds (12 hours)

**Rationale:** Affect "calm" and "curious" both appear in baseline vocabulary; restedness is "fully_rested" (allowed); no health issues. All three conditions met.

---

### Test Case 2: Non-Baseline Affect
**Input:**  
Most recent self_report at now - 2h:
```json
{
  "kind": "self_report.state",
  "ts": "2026-05-20T09:15:33.000Z",
  "payload": {
    "affect": ["anxious", "unfocused"],
    "restedness": "rested",
    "known_health_issues": []
  }
}
```

**Expected Output:**  
- Bit: FALSE
- Freshness: 7200 seconds (2 hours)

**Rationale:** Neither "anxious" nor "unfocused" appear in baseline vocabulary. Affect condition fails; predicate returns FALSE.

---

### Test Case 3: Baseline Affect, Non-Baseline Restedness
**Input:**  
Most recent self_report at now - 3h:
```json
{
  "kind": "self_report.state",
  "ts": "2026-05-20T08:15:33.000Z",
  "payload": {
    "affect": ["calm", "alert"],
    "restedness": "tired",
    "known_health_issues": []
  }
}
```

**Expected Output:**  
- Bit: FALSE
- Freshness: 10800 seconds (3 hours)

**Rationale:** Affect is baseline; health issues clear; but restedness="tired" is not in allowed set. Restedness condition fails; predicate returns FALSE.

---

### Test Case 4: Baseline Affect and Restedness, But Health Issue Present
**Input:**  
Most recent self_report at now - 1h:
```json
{
  "kind": "self_report.state",
  "ts": "2026-05-20T10:15:33.000Z",
  "payload": {
    "affect": ["calm"],
    "restedness": "fully_rested",
    "known_health_issues": ["mild headache"]
  }
}
```

**Expected Output:**  
- Bit: FALSE
- Freshness: 3600 seconds (1 hour)

**Rationale:** Affect and restedness are baseline; but known_health_issues list is non-empty. Health condition fails; predicate returns FALSE.

---

### Test Case 5: No Self-Report Within 24-Hour Window
**Input:**  
Most recent self_report at now - 25h:
```json
{
  "kind": "self_report.state",
  "ts": "2026-05-19T10:15:33.000Z",
  "payload": {
    "affect": ["calm"],
    "restedness": "fully_rested",
    "known_health_issues": []
  }
}
```

**Expected Output:**  
- Bit: INDETERMINATE
- Freshness: null

**Rationale:** The record is outside the 24-hour window. Predicate cannot make a definitive claim; returns INDETERMINATE to signal "no data in the required window."

---

### Test Case 6: No Self-Report Records in Chain at All
**Input:**  
Chain contains no `kind: "self_report.*"` records; principal profile is initialized.

**Expected Output:**  
- Bit: INDETERMINATE
- Freshness: null

**Rationale:** Empty candidate set. Predicate cannot evaluate; returns INDETERMINATE.

---

### Test Case 7: Multiple Self-Reports in Window, Most Recent is Baseline
**Input:**  
Chain contains three self-report records in the window:
- now - 22h: affect=["anxious"], restedness="ok", health=[] → FALSE if evaluated
- now - 18h: affect=["calm"], restedness="rested", health=[] → TRUE if evaluated
- now - 6h: affect=["calm", "focused"], restedness="fully_rested", health=[] → TRUE if evaluated (most recent)

**Expected Output:**  
- Bit: TRUE
- Freshness: 21600 seconds (6 hours)

**Rationale:** The most-recent-only rule applies. Only the now - 6h record is inspected. It satisfies all three conditions; predicate returns TRUE.

---

### Test Case 8: Multiple Self-Reports in Window, Most Recent is Non-Baseline
**Input:**  
Chain contains three self-report records in the window:
- now - 20h: affect=["calm"], restedness="fully_rested", health=[] → TRUE if evaluated
- now - 14h: affect=["calm"], restedness="fully_rested", health=[] → TRUE if evaluated
- now - 4h: affect=["stressed"], restedness="tired", health=["back pain"] → FALSE if evaluated (most recent)

**Expected Output:**  
- Bit: FALSE
- Freshness: 14400 seconds (4 hours)

**Rationale:** Predicate evaluates only the most recent record (now - 4h). It fails all three conditions (affect not baseline, restedness not baseline, health issue present). Older baseline reports are ignored. Predicate returns FALSE.

---

## Edge Cases and Failure Modes

### Clock Skew
The predicate uses roughtime-attested `now` (Everest 31), not the system clock. This ensures that the principal's vault or a compromised local clock cannot manipulate the 24-hour window. Roughtime attestation is mandatory for freshness guarantees.

### Record at Exact 24-Hour Boundary
A self-report record with freshness_seconds = 86400 is considered within the window (inclusive on the recent side). Records with freshness_seconds > 86400 are excluded.

### Missing or Malformed Principal Profile
If the principal profile has not been initialized (no `kind: "profile.affect_vocabulary_set"` record in chain), the predicate returns INDETERMINATE with a reason string: "principal_profile_not_initialized". This is not an error; it signals that the predicate cannot proceed.

### Malformed Self-Report Payload
If a self_report record lacks required fields (affect, restedness, known_health_issues), the predicate treats this as a chain validation failure and reports an evaluation error. This is handled upstream (E26 chain integrity) and does not produce a Bit value.

### Principal Profile Update During Window
If the principal updates their baseline vocabulary (via a `kind: "profile.affect_vocabulary_update"` record) within the 24-hour window, the predicate uses the most-recent profile at evaluation time. The previous baseline vocabulary is ignored for this evaluation.

### Indeterminate and Proof Circuits
When the predicate returns INDETERMINATE, the proof circuit (Everest 65) must communicate this tri-valued result to the verifier. Default policy (Everest 7 classes) treats INDETERMINATE as "not baseline" for high-assurance contexts, but low-risk classes can be configured to "treat INDETERMINATE as baseline." The principal can inspect their configuration and propose risk-appropriate opt-ins.

---

## Proof Circuit Integration (Everest 65)

The predicate feeds into the proof circuit as follows:

**Witnesses (Held Secret):**  
- The most-recent self_report record's full payload (affect list, restedness, health issues, timestamp)
- The principal's baseline vocabulary set (committed once, referenced by hash in multiple proofs)

**Public Commitments:**  
- Chain head at evaluation time (sha256)
- Window start and end timestamps (UTC)
- The evaluation timestamp
- The result bit (true / false / indeterminate)
- Freshness (seconds)

**Critical Property:** The proof MUST NOT leak which specific affect words or health issues were present in the self-report. The circuit reveals only the aggregate result (true/false/indeterminate) and freshness. Counterparties do not learn the principal's reported affect or health state; they learn only whether the principal's most-recent report matched their baseline.

---

## Cross-References

- **E6:** Principal identity and enrollment
- **E11, E14:** Enrollment ceremony and baseline vocabulary establishment
- **E26:** Chain integrity and record validation
- **E30:** Sigsum anchor for chain head freshness
- **E31:** Roughtime-attested time service
- **E51:** Predicate language specification
- **E52:** Predicate structure and schema (v1.0.0 compliant)
- **E54:** Predicate review protocol
- **E59:** Companion `cognitively_atypical_baseline` predicate (artist clause)
- **E60:** Companion `mental_state_unusual` predicate (roughly the negation)
- **E65:** Proof circuit composition and witness hiding

---

— Calm, 2026-05-20
