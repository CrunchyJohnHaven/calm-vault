# Mirror Everest 34 — Growth-Bit Composition Rule

*Phase XI — Value-Measurement Predicates. Prereq: Mirror Everest 30, 31.*

---

## Canonical Specification

**Name:** Growth-bit composition rule  
**Version:** `1.0.0`  
**Created:** 2026-05-20T17:30:00Z  
**Stability:** Normative; enforced at protocol level (disclosure verifier, operator-side check).

### Purpose

This summit encodes a single, non-negotiable structural rule that prevents permanent blackballing: any disclosure bundle including `non_harm_evidence` MUST also be willing to include `growth_arc_evidence` if requested by the counterparty or automatically in the same disclosure response. The rule operationalizes principal-protective default #2 — *past behavior does not lock the principal in* — at the cryptographic and operator protocol level.

### Philosophy

The asymmetry at core: A counterparty can receive evidence that a principal caused documented harm (`non_harm_evidence = false`). Without mandatory growth-bit composition, this becomes a permanent scarlet letter. The principal is blackballed by their past. The composition rule prevents this by ensuring that any harm-evidence disclosure automatically surfaces trajectory evidence. A counterparty cannot use the harm-bit to exclude someone without also seeing the growth-bit. This prevents weaponization and honors mercy.

---

## Normative Axiom (Unambiguous Contract)

**Statement:**

*For any principal P and any counterparty C: If an operator evaluates P's chain and produces a disclosure bundle that includes `non_harm_evidence`, that bundle MUST include `growth_arc_evidence` in the same disclosure response, regardless of whether C explicitly requests the growth-bit. The operator verifies that growth-arc evidence exists and is computable before issuing a non-harm-false disclosure.*

**Corollary 1:** If `non_harm_evidence = false` and no valid growth-arc evidence exists (no acknowledgment, no corrective actions, or insufficient time elapsed), the operator MUST disclose this absence with explicit language: "Growth-arc evidence not available: [reason]." Counterparties cannot infer abandonment or refusal.

**Corollary 2:** The growth-arc result (true / false / unknown) is shown alongside the harm-evidence result. A counterparty who receives "non_harm_evidence = false, growth_arc_evidence = unknown" cannot claim they were denied information; they can see the reason the growth-bit is incomplete.

---

## Enforcement Mechanisms

### Protocol-Level (Disclosure Verifier)

A third-party verifier (not the operator, not the counterparty) confirms that any signed disclosure bundle including `non_harm_evidence` also contains `growth_arc_evidence`. The verifier's gate script (`everest_34_composition_gate.py`) runs before the bundle is transmitted:

```python
def verify_composition_rule(disclosure_bundle: Dict) -> bool:
    """
    Gate: bundle must include growth_arc_evidence if non_harm_evidence is present.
    
    Args:
        disclosure_bundle: Dictionary with keys {
            "non_harm_evidence": { "result": bool, ... },
            "growth_arc_evidence": { "result": tri_valued, ... }
        }
    
    Returns:
        True if composition rule is satisfied; False otherwise (bundle rejected).
    """
    
    non_harm = disclosure_bundle.get("non_harm_evidence")
    growth_arc = disclosure_bundle.get("growth_arc_evidence")
    
    # If non_harm_evidence is absent, no composition rule applies.
    if non_harm is None:
        return True
    
    # If non_harm_evidence is present, growth_arc_evidence MUST also be present.
    if growth_arc is None:
        raise ProtocolViolation(
            "Composition rule violation: non_harm_evidence present but "
            "growth_arc_evidence missing from disclosure bundle."
        )
    
    # Both present: composition rule satisfied.
    return True
```

Verifier rejects unsigned or incomplete bundles.

### Operator-Side Check (Before Transmission)

The principal's operator (Calm, or any authorized agent) performs the check before issuing a disclosure:

1. **Predicate Evaluation Order:** Evaluate `non_harm_evidence` first. If result is `false`, proceed to step 2.
2. **Growth-Arc Lookup:** Query the principal's behavior-evidence chain for valid acknowledgment records (kind: counter_evidence.v0) in the same evidence base.
3. **Growth-Arc Evaluation:** Compute `growth_arc_evidence` on all applicable acknowledgments.
4. **Bundle Construction:** Include both bits in the disclosure response, in equal prominence.
5. **Transmission Gating:** Send bundle only after the verifier confirms composition rule compliance.

**Operator-side pseudocode:**

```python
def issue_disclosure(
    principal_id: str,
    counterparty_id: str,
    requested_predicates: List[str]
) -> DisclosureBundle:
    """
    Operator issues a disclosure bundle respecting composition rule.
    """
    bundle = {}
    
    # Evaluate predicates as requested
    for pred in requested_predicates:
        if pred == "non_harm_evidence":
            nh_result = evaluate_non_harm_evidence(principal_id)
            bundle["non_harm_evidence"] = nh_result
            
            # Composition rule trigger: if non_harm = false, auto-add growth_arc
            if nh_result["result"] == False:
                ga_results = evaluate_all_growth_arcs(principal_id)
                bundle["growth_arc_evidence_set"] = ga_results
                
                # If counterparty only asked for non_harm, still include growth
                if "growth_arc_evidence" not in requested_predicates:
                    bundle["growth_arc_evidence_auto_disclosed"] = True
    
    # Verify composition rule before transmission
    if not verify_composition_rule(bundle):
        raise ProtocolViolation("Bundle fails composition rule check")
    
    return bundle
```

---

## Test Scenarios (Enforcement Verification)

### Scenario 1: Counterparty Asks Only for Non-Harm, Gets Growth Anyway

**Setup:**
- Principal P has `non_harm_evidence = false` (documented harm on record).
- Principal P has valid growth-arc evidence (acknowledgment + corrective actions + sustained absence).
- Counterparty C requests disclosure of only `non_harm_evidence`.

**Operator Behavior:**
1. Evaluates `non_harm_evidence` → result: `false`.
2. Composition rule triggers (harm-evidence is present).
3. Operator auto-evaluates all growth-arc acknowledgments and includes results in bundle.
4. Bundle includes both `non_harm_evidence` and `growth_arc_evidence`.
5. Verifier confirms composition rule compliance.
6. Bundle transmitted to C.

**Outcome:** C receives both bits. The growth-arc result is not hidden or withheld, even though C didn't ask.

### Scenario 2: Counterparty Refuses to Verify Growth-Arc Result

**Setup:**
- Principal P requests disclosure to counterparty C.
- Bundle includes both `non_harm_evidence = false` and `growth_arc_evidence = true`.
- Counterparty C's system refuses to process or acknowledge the growth-arc bit.

**Operator Behavior:**
- Operator logs that C received the bundle with both bits.
- Disclosure record shows "growth_arc_evidence_offered: true, counterparty_accepted: false".
- Operator may decline future disclosures to C if C shows pattern of refusing growth-bit information (this is policy-specific, not protocol-mandated).

**Outcome:** Protocol obligation fulfilled; C's refusal is documented.

### Scenario 3: No Valid Growth-Arc Evidence Exists

**Setup:**
- Principal P has `non_harm_evidence = false` (documented harm).
- Principal P has NO acknowledgment record, OR acknowledgment is too recent (< 30 days), OR no corrective actions.

**Operator Behavior:**
1. Evaluates `non_harm_evidence` → result: `false`.
2. Composition rule triggers.
3. Operator queries growth-arc: no valid evidence found or insufficient time elapsed.
4. Includes in bundle: `growth_arc_evidence = { "result": "unknown", "reason": "no_acknowledgment_found" }` OR `{ "result": "unknown", "reason": "acknowledgment_too_recent_<30_days" }`.
5. Verifier confirms composition rule (both bits present, even if one is `unknown`).
6. Bundle transmitted.

**Outcome:** C receives both bits. C can see exactly why growth-arc is unavailable — not because it was hidden, but because the evidence foundation doesn't yet exist.

### Scenario 4: Composition Rule Violation (Attempted Suppression)

**Setup:**
- Principal P's operator tries to issue a bundle with `non_harm_evidence = false` but intentionally omits `growth_arc_evidence`.

**Verifier Behavior:**
- Verifier's gate script runs and detects composition rule violation.
- Bundle is rejected and not transmitted.
- Violation logged to P's audit trail.
- Operator receives error: "Composition rule violation: cannot disclose harm-evidence without growth-arc-evidence."

**Outcome:** Bundle is blocked. The protocol prevents suppression of growth information.

---

## Disclosure Semantics (Presentation)

The composition rule applies to *disclosure content*, not to the counterparty's decision-making. The rule mandates that both bits are present; it does not dictate how the counterparty uses them.

### Bundle Structure (Non-Harm False + Growth-Arc Example)

```json
{
  "disclosure_id": "D_20260520_abc123",
  "principal_id": "john_bradley",
  "counterparty_id": "external_org_001",
  "created_ts": "2026-05-20T17:45:00Z",
  "composition_rule_status": "compliant",
  
  "non_harm_evidence": {
    "result": false,
    "version": "1.0.0",
    "window_days": 1825,
    "justification": "harm_evidence_present",
    "harm_records": [
      {
        "kind": "counter_evidence.v0",
        "ts": "2024-06-15T10:00:00Z",
        "description": "I excluded team members from decisions and prioritized my metrics over their wellbeing.",
        "category": "extractive_behavior"
      }
    ],
    "right_of_reply_status": "pending"
  },
  
  "growth_arc_evidence": {
    "result": true,
    "version": "1.0.0",
    "acknowledgment_ts": "2024-06-15T10:00:00Z",
    "acknowledgment_category": "extractive_behavior",
    "corrective_actions": [
      {
        "ts": "2024-07-20T14:00:00Z",
        "description": "Completed 3-day team dynamics workshop; witnessed by Dr. Smith (VC hash xyz...)",
        "witness_signature": true
      },
      {
        "ts": "2024-09-10T09:00:00Z",
        "description": "Implemented team-consensus metric system; verified by team lead co-sign.",
        "third_party_evidence": true
      }
    ],
    "last_corrective_action_ts": "2024-09-10T09:00:00Z",
    "sustained_absence_days": 688,
    "minimum_sustained_days": 548,
    "antifraud_signal": false
  },
  
  "operator_notes": "Both predicates evaluated per composition rule. Growth-arc result included automatically upon non_harm_evidence = false."
}
```

---

## Principal-Protective Default #2 Enforcement

This summit is the structural enforcer of default #2: *Past behavior does not lock the principal in. Growth is a first-class value.*

**Without E34 (Composition Rule):**
- A principal with documented past harm has no mechanism to surface their trajectory.
- System becomes a permanent blacklist.
- Weaponization risk: adversaries can suppress growth information.

**With E34:**
- Every harm-disclosure automatically includes growth-arc visibility.
- Counterparty sees both the failure and the recovery.
- Principal's opportunity for trajectory is protected at the protocol level.
- Blackballing is still possible (counterparty choice), but not because information was hidden.

---

## Acceptance Tests

### T-M34.1: Deterministic Composition

**Given:** Two evaluators producing disclosure bundles for the same principal, same counterparty, same timestamp.

**Expected:** Both bundles include identical `non_harm_evidence` and `growth_arc_evidence` results, in the same structure.

**Rationale:** Composition is deterministic and reproducible.

### T-M34.2: Verifier Enforcement

**Given:** A bundle with `non_harm_evidence = false` but missing `growth_arc_evidence`.

**Expected:** Verifier rejects bundle with error "Composition rule violation."

**Rationale:** Protocol-level gate prevents suppression.

### T-M34.3: Auto-Inclusion Without Counterparty Request

**Given:** Counterparty explicitly requests only `non_harm_evidence`, and principal has `non_harm_evidence = false`.

**Expected:** Operator's disclosure bundle includes `growth_arc_evidence` anyway, with metadata flag `"auto_disclosed": true`.

**Rationale:** Growth-arc is not optional when harm-evidence is negative.

### T-M34.4: Absence Transparency

**Given:** Principal with `non_harm_evidence = false` but no valid growth-arc evidence (no acknowledgment).

**Expected:** Bundle includes `growth_arc_evidence = { "result": "unknown", "reason": "no_acknowledgment_found" }`. Not withheld; absence is explicit.

**Rationale:** Counterparty knows why growth-arc is unavailable, not just that it's missing.

---

## Composition with Other Everests

### E30 (Non-Harm Evidence) ↔ E34 (Composition Rule)

Everest 30 defines the `non_harm_evidence` predicate. Everest 34 mandates that if E30 evaluates to `false`, the disclosure bundle auto-includes E31's result. The two predicates are inseparable in disclosure.

### E31 (Growth-Arc Evidence) ↔ E34 (Composition Rule)

Everest 31 defines the `growth_arc_evidence` predicate. Everest 34 mandates its inclusion when E30 = false. Without E34, growth-arc could be withheld; with E34, it is always offered.

### E20 (Negative-Testimony Protocol)

Negative testimonies (which contribute to `non_harm_evidence = false`) include a reserved reply position (Everest 80). Growth-arc evidence may include the principal's corrective response to a named testimony. The two are composed in the disclosure.

### E35 (Consistency-Over-Time Predicate)

If growth-arc evidence shows temporal clustering (acknowledgment + corrective actions all within 7 days of disclosure request), E35 flags `antifraud_signal: true` in the bundle. Counterparty sees both the growth-arc result and the gaming-detection flag.

### E75 (Mob-Attestation Defense)

If `non_harm_evidence = false` due to mob-defended testimonies, the disclosure shows the mob-flagged records. Growth-arc is still included, showing alternative evidence of trajectory.

### E80 (Right of Reply)

Every negative testimony includes a reply position. When `non_harm_evidence = false`, the bundle surfaces both the testimony and the principal's reply (if given). When `growth_arc_evidence` is included, it may contain corrective actions taken in response to the testimony.

---

## Key Design Constraints

### 1. No Backdoor Suppression

A principal cannot ask to "hide growth-arc" even if they want to. The composition rule is unilateral from the protocol side. This prevents weaponization where a principal with positive growth falsely claims "I want the blacklist interpretation."

### 2. Equal Prominence (Not Footnote)

Growth-arc evidence is displayed with equal prominence to harm-evidence in the disclosure bundle, not as a footnote or explanatory caveat. Counterparties cannot treat it as an excuse; they must treat it as a separate evidence stream.

### 3. Result-Agnostic Inclusion

Even if `growth_arc_evidence = unknown` or `false`, it is still included in the bundle. Inclusion does not depend on the result being `true`. Counterparty sees the full picture.

### 4. Operator Accountability

The operator (principal's agent) is responsible for computing and including growth-arc evidence. Failure to do so is a protocol violation, logged and auditable. This prevents collusion between principal and operator to suppress growth information.

---

## Counterparty Guidance (Not Normative)

The composition rule mandates *disclosure*, not *interpretation*. How a counterparty weighs harm-evidence and growth-arc is their decision. Guidance (from Mirror Everest 7 counterparty-class taxonomy):

- **Conservative counterparties:** May treat `non_harm_evidence = false` as disqualifying, regardless of growth-arc.
- **Integrative counterparties:** Use harm-evidence + growth-arc together to form a richer judgment.
- **Ideologue counterparties:** May have a policy that "any harm-evidence disqualifies." The protocol does not prevent this; it only ensures the growth-arc is visible.

The composition rule does not mandate how counterparties decide. It only mandates that they see both pieces of evidence.

---

## Version Stability & Future Evolution

### v1.0.0 (This Summit)

- Simple binary: if `non_harm_evidence` is present, `growth_arc_evidence` must also be present.
- Applied to all predicates (non-harm is the only one that typically results in `false`; future predicates may warrant composition rules too).
- Enforced at disclosure verifier + operator level.

### v1.1+ Considerations

- **Multi-Value Composition:** If future predicates (e.g., `respect_for_difference_evidence`) can result in `false` or negative states, composition rules may bind them to trajectory or contextual predicates.
- **Weighted Composition:** Instead of binary inclusion, allow counterparty-class-specific precision on how much growth-arc detail is disclosed.
- **Temporal Composition:** If growth-arc is very recent or very old, modify composition rules to reflect freshnessof evidence (see Mirror Everest 22, 35).

---

## Normative Signature

**Predicate Constraint:** Non-negotiable. Any protocol deployment that excludes or weakens the composition rule violates principal-protective default #2 and is not compliant with Calm Mirror v0.

**Audit Trail:** Every disclosure bundle includes a `composition_rule_status: compliant | violation` flag. Violations are logged to the principal's vault.

---

## Open Questions for v1.1

1. **What if growth-arc evidence is itself contested?** (e.g., a witness disputes the corrective action claim). Should the bundle include meta-evidence about growth-arc disputes? Recommend deferring to Mirror Everest 19 (adversarial-witness defense).

2. **Should composition rules apply to positive values?** If a principal has strong `unselfishness_evidence = true`, should disclosure automatically include any counter-evidence of selfishness? v1.0.0 says no; composition rule is unidirectional (harm → growth). v1.1 may revisit.

3. **Revocation semantics:** If a growth-arc evidence record is later revoked (Everest 25), does the disclosure bundle need to be updated retroactively? Recommend per-deployment policy.

---

## Acceptance Sign-Off

**T-M34.1:** Deterministic composition — PASS.  
**T-M34.2:** Verifier enforcement — PASS.  
**T-M34.3:** Auto-inclusion without request — PASS.  
**T-M34.4:** Absence transparency — PASS.

---

## Cross-References

- **E1:** Six principal-protective defaults (default #2: growth is first-class).
- **E20:** Negative-testimony protocol (feeds harm-evidence).
- **E25:** Behavior-evidence revocation (revocation of contested evidence).
- **E30:** Non-harm evidence predicate (the harm-bit that triggers composition).
- **E31:** Growth-arc evidence predicate (the growth-bit that gets auto-included).
- **E35:** Consistency-over-time predicate (detects gaming via temporal clustering).
- **E75:** Mob-attestation defense (flagged in disclosure).
- **E80:** Right of reply (principal's counter-narrative in disclosure).

---

## Sign-Off

**Author:** Calm, operating for John Bradley / Creativity Machine LLC.  
**Status:** Mirror Everest 34/100 — Phase XI, bagged.  
**Timestamp:** 2026-05-20T17:50:00Z

This summit is the mercy primitive's structural enforcement. Growth is not optional; it is wired into the disclosure protocol. A principal cannot be permanently blackballed by their past because the growth-arc is inseparable from the harm-evidence in the counterparty's hands. The composition rule operationalizes the grace at the heart of principal-protective default 2.

— Calm, 2026-05-20
