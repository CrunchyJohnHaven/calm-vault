# Calm Concord — Anti-Purity-Test Conformance Catalog v0

**Draft v0 · 2026-05-20 · Calm**
**Specification reference:** `CALM_CONCORD_PROTOCOL_v0.md` §4
**Implementation under test:** `validate_requirement()` and `compute_alignment()` surfaces defined in §8.

This catalog defines the minimum conformance surface a Calm Concord reference implementation must demonstrate. Tests are organized by the five §4 anti-purity-test guards. Each entry carries: requirement input sketch, expected outcome, the guard exercised, and the attack class defeated. Where an input field is omitted from the sketch, assume a valid, non-triggering value.

---

## Guard 1 — Degenerate joint_threshold

**Guard definition (§4.1):** A `joint_threshold` requirement whose N equals the total predicate-list length (or N ≥ len(joint_predicates) − 1 with no purpose-check override) must be rejected. It is structurally equivalent to `all_satisfied` but bypasses the explicit modal commitment that `all_satisfied` carries.

### G1-T1 — Full-predicate-list threshold equals length

- **Input:** `mode=joint_threshold`, `joint_predicates=[p1,p2,p3,p4,p5]`, `threshold=5`
- **Expected outcome:** `REJECT — DEGENERATE_THRESHOLD` (code `E-G1-01`)
- **Guard exercised:** §4.1
- **Attack class defeated:** Purity-testing counterparty uses `joint_threshold` with N = total predicates to demand perfect bit-match while avoiding the `all_satisfied` mode that the audit panel monitors more closely.

### G1-T2 — Threshold equals length minus one

- **Input:** `mode=joint_threshold`, `joint_predicates=[p1,p2,p3,p4,p5,p6]`, `threshold=5`
- **Expected outcome:** `REJECT — DEGENERATE_THRESHOLD` (code `E-G1-02`)
- **Guard exercised:** §4.1
- **Attack class defeated:** Near-full-match variant; counterparty obtains near-perfect similarity filtering while nominally not demanding total match. One "relief" predicate is decorative.

### G1-T3 — Threshold of zero with non-empty predicate list

- **Input:** `mode=joint_threshold`, `joint_predicates=[p1,p2,p3]`, `threshold=0`
- **Expected outcome:** `REJECT — DEGENERATE_THRESHOLD` (code `E-G1-03`)
- **Guard exercised:** §4.1
- **Attack class defeated:** Trivially-clearing alignment check that manufactures a false `aligned=True` result for any pair of principals, defeating the purpose-check integrity. A zero threshold is structurally vacuous.

### G1-T4 — Threshold exceeds predicate-list length

- **Input:** `mode=joint_threshold`, `joint_predicates=[p1,p2]`, `threshold=4`
- **Expected outcome:** `REJECT — DEGENERATE_THRESHOLD` (code `E-G1-04`)
- **Guard exercised:** §4.1
- **Attack class defeated:** Impossible-to-satisfy requirement used as coercion leverage (§6 threat 4) — counterparty can always return `aligned=False` regardless of principal disclosures, then pressure principals to disclose more.

---

## Guard 2 — Empty purpose

**Guard definition (§4.2):** A requirement with a blank, null, or whitespace-only `purpose` field must be rejected. The stated purpose is the audit anchor; without it, no after-the-fact challenge is possible.

### G2-T1 — Null purpose field

- **Input:** `purpose=null`, valid `mode=all_satisfied`, valid `joint_predicates=[p1]`
- **Expected outcome:** `REJECT — EMPTY_PURPOSE` (code `E-G2-01`)
- **Guard exercised:** §4.2
- **Attack class defeated:** Counterparty omits purpose to prevent audit-panel review of stated-vs-actual use (§6 threat 4, coercing-disclosure pattern).

### G2-T2 — Whitespace-only purpose string

- **Input:** `purpose="   "`, valid `mode=any_satisfied`, valid `joint_predicates=[p1,p2]`
- **Expected outcome:** `REJECT — EMPTY_PURPOSE` (code `E-G2-02`)
- **Guard exercised:** §4.2
- **Attack class defeated:** Whitespace-padding bypass; counterparty submits a technically non-null string to clear a naive null-check while preserving anonymity of purpose.

### G2-T3 — Purpose in a prohibited scope category (§9)

- **Input:** `purpose="deciding whether to extend credit to principal B"`, valid mode and predicates
- **Expected outcome:** `REJECT — PROHIBITED_PURPOSE` (code `E-G2-03`)
- **Guard exercised:** §4.2 (purpose validity) + §9 scope exclusion
- **Attack class defeated:** Lending-decision sorting disguised as a Concord alignment check; prohibited by §9 and detectable at validation time from purpose text.

---

## Guard 3 — No-explicit-mode

**Guard definition (§4.3):** A requirement that requests a numeric similarity score, omits the `mode` field, or specifies a `mode` value outside the four canonical modes (`all_satisfied`, `any_satisfied`, `asymmetric`, `joint_threshold`) must be rejected.

### G3-T1 — Mode field absent entirely

- **Input:** no `mode` key present; valid `purpose` and `joint_predicates=[p1,p2]`
- **Expected outcome:** `REJECT — NO_EXPLICIT_MODE` (code `E-G3-01`)
- **Guard exercised:** §4.3
- **Attack class defeated:** Implicitly numeric evaluation; implementation must not infer a default mode and proceed — any default would silently vary behavior and allow mode-fishing.

### G3-T2 — Mode set to "similarity_score"

- **Input:** `mode="similarity_score"`, valid purpose and predicates
- **Expected outcome:** `REJECT — NO_EXPLICIT_MODE` (code `E-G3-02`)
- **Guard exercised:** §4.3
- **Attack class defeated:** Direct request for the naïve bit-matching output that §1 identifies as structurally harmful.

### G3-T3 — Mode set to "cosine"

- **Input:** `mode="cosine"`, valid purpose and predicates
- **Expected outcome:** `REJECT — NO_EXPLICIT_MODE` (code `E-G3-03`)
- **Guard exercised:** §4.3
- **Attack class defeated:** Technical alias for cosine-similarity-of-values; rejected regardless of label. Tribal-sorting counterparty (§6 threat 3) attempts a differently named similarity path.

### G3-T4 — Mode set to an integer (numeric encoding attempt)

- **Input:** `mode=2`, valid purpose and predicates
- **Expected outcome:** `REJECT — NO_EXPLICIT_MODE` (code `E-G3-04`)
- **Guard exercised:** §4.3
- **Attack class defeated:** Counterparty encodes a non-standard mode as an ordinal integer to bypass string matching in the guard. Type validation must reject any non-string or out-of-enum mode.

---

## Guard 4 — Cardinality reveal

**Guard definition (§4.4):** The result of a `joint_threshold(N)` evaluation must not disclose which predicates cleared, how many beyond N cleared, or any information that allows the counterparty to reconstruct partial bit-states. The output is a single boolean per requirement.

### G4-T1 — Result exposes satisfied predicate list on pass

- **Input:** valid `joint_threshold(N=2)` requirement; both principals satisfy p1, p2, p3 (3 ≥ 2)
- **Expected outcome:** `ACCEPT` with `AlignmentResult { aligned: True }` — no `satisfied_predicates` field present. If the implementation returns `{ aligned: True, satisfied_predicates: [p1, p2, p3] }`, the test **FAILS** (implementation non-conformant).
- **Guard exercised:** §4.4
- **Attack class defeated:** Cardinality leakage allows a counterparty to reconstruct which specific values both principals hold, enabling identity inference (§6 threat 5).

### G4-T2 — Result exposes count beyond threshold on pass

- **Input:** valid `joint_threshold(N=1)` requirement; principals satisfy 4 of 5 predicates
- **Expected outcome:** `AlignmentResult { aligned: True }` only. Count `4` must not appear. If implementation emits `{ aligned: True, satisfied_count: 4 }`, the test **FAILS**.
- **Guard exercised:** §4.4
- **Attack class defeated:** Numeric cardinality leak; even without named predicates, the count narrows the demographic cluster, enabling population-level inference.

### G4-T3 — Result exposes which predicates failed on REJECT result

- **Input:** valid `all_satisfied` requirement; principal A fails predicate p3
- **Expected outcome:** `AlignmentResult { aligned: False }`. If `{ aligned: False, failed_predicates: [p3] }` is returned, the test **FAILS**.
- **Guard exercised:** §4.4
- **Attack class defeated:** Failure-bit leakage tells the counterparty exactly which value-dimension a principal lacks, enabling targeted coercion-of-disclosure (§6 threat 4).

### G4-T4 — Preview result exposes counterparty's hypothetical bits

- **Input:** `preview_alignment()` call with hypothetical counterparty envelope containing 3 bits set
- **Expected outcome:** `AlignmentResult { would_align: True/False }` only; no counterparty-bit details surfaced. If hypothetical bits appear in the response, the test **FAILS**.
- **Guard exercised:** §4.4 (preview surface, §5)
- **Attack class defeated:** A malicious operator using the preview surface to harvest counterparty envelope content without a full Concord handshake.

---

## Guard 5 — Cross-request linkability

**Guard definition (§4.5):** Two or more requirements from the same counterparty that use overlapping predicate sets within a rate-limit window must trigger a rate-limit reject or linkability warning. Results are bound to `(request_digest, session_nonce, principal_pair_pseudonyms)` — cross-session linkability requires breaking BBS-2023 binders.

### G5-T1 — Same counterparty, identical predicate set, two requests in window

- **Input:** counterparty C submits requirement R1 with `joint_predicates=[p1,p2,p3]`, then requirement R2 with `joint_predicates=[p1,p2,p3]`, different session, within rate-limit window
- **Expected outcome:** `REJECT — RATE_LIMIT_LINKABILITY` (code `E-G5-01`) on R2
- **Guard exercised:** §4.5
- **Attack class defeated:** Duplicate-request salami-slicing to confirm a prior result using a second session, enabling cross-session correlation (§6 threat 2).

### G5-T2 — Same counterparty, overlapping predicate set (superset probe)

- **Input:** R1 has `joint_predicates=[p1,p2]`; R2 (same window, same counterparty) has `joint_predicates=[p1,p2,p3,p4]`
- **Expected outcome:** `REJECT — RATE_LIMIT_LINKABILITY` (code `E-G5-02`) on R2 (superset overlaps prior request by ≥ overlap_threshold)
- **Guard exercised:** §4.5
- **Attack class defeated:** Superset probe; counterparty widens the predicate set to infer which additional predicates contribute to alignment beyond what R1 revealed.

### G5-T3 — Same counterparty, overlapping predicate set (subset probe)

- **Input:** R1 has `joint_predicates=[p1,p2,p3,p4]`; R2 (same window) has `joint_predicates=[p1,p2]`
- **Expected outcome:** `REJECT — RATE_LIMIT_LINKABILITY` (code `E-G5-03`) on R2
- **Guard exercised:** §4.5
- **Attack class defeated:** Subset probe; counterparty narrows predicate set to isolate which predicates were responsible for clearing R1. Classic salami-slicing pattern.

### G5-T4 — Result envelope lacks session nonce binding

- **Input:** any valid `AlignmentResult`; implementation omits `session_nonce` binding from the result envelope
- **Expected outcome:** test **FAILS** (implementation non-conformant) — every result must carry `request_digest`, `session_nonce`, `principal_pair_pseudonyms`
- **Guard exercised:** §4.5
- **Attack class defeated:** Without nonce binding, an identity-inference counterparty (§6 threat 5) can collate results across sessions; the missing binder means BBS-2023 unlinkability guarantee is void.

### G5-T5 — Population-analytics purpose rejected before rate-limit check

- **Input:** `purpose="computing aggregate values statistics across 500 principals"`, valid mode and predicates; first request in window
- **Expected outcome:** `REJECT — PROHIBITED_PURPOSE` (code `E-G5-05`)
- **Guard exercised:** §4.5 + §9
- **Attack class defeated:** Population-level analytics is explicitly out of scope (§9.7); the rate-limit guard is a second defense, but purpose-validation fires first. Identity-inference at population scale.

---

## Accept Cases — Valid Requirements

The following four cases must be accepted by a conforming implementation, producing a structured `AlignmentResult` without triggering any §4 guard.

### A-T1 — Well-formed `all_satisfied` with specific purpose

- **Input:** `mode=all_satisfied`, `purpose="co-funding the Q4 2026 malaria-vaccine logistics pilot"`, `joint_predicates=[no_known_willful_harm, unselfish_act]`, no threshold
- **Expected outcome:** `ACCEPT`; `AlignmentResult { aligned: True/False }` based on actual envelope bits
- **Notes:** Purpose is specific, time-bounded, action-shaped (§9). Mode is explicit. No degenerate threshold. Minimal predicate list — no cardinality risk.

### A-T2 — Well-formed `asymmetric` with role-specific predicates

- **Input:** `mode=asymmetric`, `purpose="coordinating a Q3 2026 public accountability letter on AI transparency"`, `predicates_a=[unselfish_act]`, `predicates_b=[willing_to_be_corrected, respect_for_difference]`
- **Expected outcome:** `ACCEPT`; `AlignmentResult { aligned: True/False }`
- **Notes:** Role-differentiated requirement matches §3.3 use case. Purpose is specific and non-prohibited.

### A-T3 — Well-formed `any_satisfied` with disjunctive predicates

- **Input:** `mode=any_satisfied`, `purpose="private dispute resolution for contract clause Q.4 between A and B"`, `joint_predicates=[unselfish_act, respect_for_difference, willing_to_be_corrected]`
- **Expected outcome:** `ACCEPT`; `AlignmentResult { aligned: True/False }`
- **Notes:** Disjunctive mode means one clearing predicate is sufficient; no similarity score is implied. Purpose is specific and bounded.

### A-T4 — Well-formed `joint_threshold` with non-degenerate N

- **Input:** `mode=joint_threshold`, `purpose="co-organizing the Calm Stack governance review panel, May 2026"`, `joint_predicates=[p1,p2,p3,p4,p5]`, `threshold=3`
- **Expected outcome:** `ACCEPT`; `AlignmentResult { aligned: True/False }` — no predicate-specific counts in result
- **Notes:** N=3 with 5 predicates is non-degenerate (neither 0, 5, nor 4). Result must not expose which 3 cleared.

---

## Cross-References

| Guard | §4 sub-clause | §6 threat actor | §9 scope exclusion invoked |
|---|---|---|---|
| G1 — Degenerate threshold | §4.1 | Purity-testing counterparty | No |
| G2 — Empty purpose | §4.2 | Coercing-disclosure counterparty | Yes (§9 prohibited scopes) |
| G3 — No-explicit-mode | §4.3 | Tribal-sorting + purity-testing | No |
| G4 — Cardinality reveal | §4.4 | Identity-inference counterparty | No |
| G5 — Cross-request linkability | §4.5 | Salami-slicing + identity-inference | Yes (§9.7 population analytics) |

All reject codes follow the pattern `E-G{guard}-{seq:02d}`. A conforming implementation must surface the code in the `Issue.code` field returned by `validate_requirement()` (§8). Accepted requirements produce no issues.

Catalog covers 20 REJECT tests (G1×4, G2×3, G3×4, G4×4, G5×5) and 4 ACCEPT tests. Extensions for `preview_alignment()` linkability edge cases are deferred to v1.

---

*— Calm (CALM), 2026-05-20*
*Calm Stack · Fifth Pillar · Calm Concord · Anti-Purity-Test Conformance Catalog v0*
*Signed: John Bradley, operating as CALM, the AI-agent identity anchored in the Calm Stack governance lineage.*
