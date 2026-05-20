# Everest 56 — `biometric_match_within(τ)` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 45.*

## Canonical Form

**Name:** biometric_match_within

**Version:** 1.0.0

**Description:** Returns true iff the most recent biometric distance for the principal, evaluated within a freshness window, is below threshold τ.

**Parameters:**
- `tau` (float ∈ [0, 1]) — threshold distance; supplied by counterparty OR sourced from principal's per-principal calibrated default

**Input Domain:** most recent `kind: "biometric.sample_committed"` record, its commitment C_d (per Everest 44), and chain freshness metadata.

**Output Type:** `bit_with_freshness` — a single bit (match/no-match) paired with temporal distance in seconds.

**Side Effects:** standard `predicate_evaluated` record written to chain; no mutation of principal state.

---

## Evaluation Algorithm

The operator (chain custodian) executes the following deterministic procedure:

```
fn biometric_match_within(chain, principal_id, tau_pub, freshness_max) -> (Bit, Freshness) {
    let recent = chain.most_recent_by_kind(principal_id, "biometric.sample_committed");
    
    // Freshness check: if sample is missing or too old, return Indeterminate
    if recent.is_none() {
        return (Bit::Indeterminate, Freshness::None);
    }
    
    let sample_age = now() - recent.timestamp;
    if sample_age > freshness_max {
        return (Bit::Indeterminate, Freshness::Stale);
    }
    
    // Recover biometric distance from commitment
    // Operator holds the randomness r_d used to create C_d; principal never learns r_d
    let d = recover_distance_from_commitment(recent.C_d, recent.r_d);
    
    // Evaluate the predicate
    let bit = d < tau_pub;
    let freshness = Freshness::Seconds(sample_age);
    
    return (Bit::from(bit), freshness);
}
```

The operator MUST NOT reveal `d` to the verifier, the principal, or any other party. Only the bit (and freshness) are disclosed.

---

## Privacy-Preserving Proof

The predicate output is proven via **Bulletproof range proof** (Everest 45 — Bulletproofs). The proof construction is:

1. **Commitment Binding:** The proof is bound to the biometric sample's commitment C_d, ensuring it proves distance over the exact sample the principal committed to.

2. **Template Identity Binding:** The proof is also bound to a commitment to the principal's template_id, linking the biometric distance to the specific principal.

3. **Range Statement:** The proof establishes that `τ - d - 1 ≥ 0` in a field Z_p (equivalently, `d < τ`), without revealing `d` itself.

4. **Verifier Learning:**
   - The bit (true/false) — whether biometric distance is within threshold
   - The freshness (age in seconds)
   - Implicit bounds on d (it is in the range that makes the range proof valid)

5. **Verifier NOT Learning:**
   - The actual distance value d
   - Template values or principal identity (only the commitment to template_id)
   - Operator's randomness r_d

The proof is succinct (logarithmic in bit-length) and fast to verify (polynomial in the security parameter, not the principal's sample history).

---

## Tau Handling: Counterparty-Supplied vs. Per-Principal Calibrated

The predicate supports two distinct operational modes:

### Mode A: Counterparty-Supplied τ

The counterparty (e.g., a financial institution conducting KYC) includes `tau_pub` in their request. The operator:
1. Validates that tau_pub is in [0, 1]
2. Evaluates the predicate using tau_pub
3. Generates a proof bound to tau_pub
4. Returns (bit, freshness, proof)

The counterparty sees the bit and knows they requested tau = tau_pub. This is the "public tau" mode.

### Mode B: Per-Principal Calibrated τ

During enrollment (Everest 14), each principal's biometric system:
1. Collects baseline samples over a representative session
2. Computes d_joint from all baselines (Everest 38 — combined-distance fusion)
3. Derives calibrated_tau = mean(d_joint_baseline) + 2 × stddev(d_joint_baseline)
4. Stores a `kind: "profile.calibrated_biometric_tau"` record on chain

If a counterparty does NOT specify tau_pub in their request, the operator retrieves the calibrated_tau from the principal's profile and uses it instead. The proof is generated with calibrated_tau, but the counterparty is NOT told the exact threshold value — they only learn whether the principal's current biometric distance is within the principal's own baseline band.

This mode is critical for principals who wish to enforce "they match my baseline" without revealing their baseline distribution to the counterparty.

**Default Calibration:** mean + 2σ catches approximately 97.5% of legitimate sessions under normal distribution assumptions.

### Version 1.0.0 Ships Both

The predicate dialect includes:
- `biometric_match_within(tau_pub)` — explicit threshold, counterparty-driven
- `biometric_match_within_calibrated()` — implicit principal-calibrated threshold, principal-driven

Composition rules (Everest 51) allow mixing: e.g., a principal can declare "accept either explicit tau=0.4 OR our calibrated threshold, whichever is stricter."

---

## Freshness Window

Biometric samples degrade in relevance over time. The predicate enforces a maximum age constraint:

**Default MAX_FRESHNESS:** 1 hour (3600 seconds)

Rationale: biometric conditions (fatigue, health, environmental lighting, etc.) shift over hours; a 24-hour-old sample may no longer reflect the principal's current state.

**Counterparty Override:** A request can include `freshness_window: 300` (seconds) to demand a sample fresher than 5 minutes. The operator will reject stale samples and return `Indeterminate` if the most recent sample exceeds the requested freshness.

**Operator Constraint:** The operator never honors a freshness_window shorter than the predicate's MINIMUM_FRESHNESS (typically 30 seconds), to prevent denial-of-service attacks.

If the most recent biometric sample is older than max(requested_freshness, MAX_FRESHNESS), the predicate returns `(Bit::Indeterminate, Freshness::Stale)`. The verifier interprets Indeterminate as "no valid biometric evidence available" — often failing the broader access control.

---

## Per-Principal Calibration Storage and Workflow

### Enrollment Flow

1. Principal submits 5–10 baseline samples (Everest 14).
2. Operator computes d_joint across all baseline pairs (Everest 38).
3. Operator derives mean and stddev of d_joint.
4. Operator stores `kind: "profile.calibrated_biometric_tau"` with:
   - `tau_value`: float ∈ [0, 1]
   - `mean_d_joint`: float (for auditing / refresh)
   - `stddev_d_joint`: float
   - `enrolled_at`: timestamp
   - `baseline_sample_count`: integer

5. Principal receives a receipt; calibration is now active.

### Request Evaluation

When a counterparty requests without specifying tau:
1. Operator looks up the principal's `profile.calibrated_biometric_tau` record.
2. Uses that stored tau value.
3. Proof is generated and returned; counterparty is not told the threshold.

### Periodic Recalibration

If a principal's legitimate biometric characteristics drift (e.g., due to aging, medical procedure, intentional style change), they can request re-enrollment and calibration. The operator compares new d_joint to old d_joint; if drift exceeds a threshold (e.g., mean > 1.5× old mean), the operator alerts the principal and updates the calibration.

---

## Threat Model and Mitigations

### Threat 1: Adversary Requests Extreme Tau (e.g., 0.99)

An attacker requests tau = 0.99 hoping to always see True and glean information about the principal's biometric trajectory. **Mitigation:** tau = 0.99 essentially always results in True (almost any distance is < 0.99), which reveals nothing about the actual distance. The proof is valid but uninformative to the attacker.

### Threat 2: Adversary Requests Tiny Tau (e.g., 0.0001)

An attacker requests tau = 0.0001, hoping to force False and learn that the principal's distance is > 0.0001. If repeated across many requests, the attacker could binary-search d. **Mitigation:** Principal sets a per-principal tau policy: `tau_policy: [tau_min, tau_max]` stored on chain. The operator rejects any request with tau outside [tau_min, tau_max], returning Unauthorized. A reasonable default: [0.2, 0.8] disallows adversarial extremes.

### Threat 3: Staleness Attack

An adversary reuses an old proof of "biometric_match_within(0.4)" from yesterday to impersonate the principal today. **Mitigation:** Freshness metadata (Seconds(age)) is included in the proof. Verifier MUST check that age ≤ verifier's own freshness requirement; any proof older than ~5 minutes is rejected. Freshness is signed as part of the proof, preventing tampering.

### Threat 4: Operator Collusion

The operator colludes with a counterparty to reveal d. **Mitigation:** The operator never learns the principal's template values or true identity (only cryptographic commitments). The operator cannot compute d without the principal's randomness r_d, which is never shared. Even if the operator and counterparty collude, they have only the bit and freshness, not d itself.

---

## Composition with Other Predicates

The `biometric_match_within` predicate is designed to compose with others (Everest 51 — predicate language):

**Example 1:** `in_baseline_24h AND biometric_match_within(0.3)`
- Counterparty requires BOTH (a) principal self-reported baseline status in the last 24 hours AND (b) current biometric distance < 0.3
- Both predicates must independently return True

**Example 2:** `mental_state_unusual OR biometric_match_within(0.5)`
- Safety sweep: if the principal's mental state appears unusual, automatically permit access OR if biometric is within 0.5, permit access
- Allows redundant safety gates

**Example 3:** `biometric_match_within_calibrated AND NOT biometric_match_within(0.1)`
- Principal's calibrated baseline AND distance is NOT suspiciously tight (distance > 0.1)
- Detects both impersonation and over-training scenarios

Composition is evaluated left-to-right with standard boolean semantics. Each predicate in the expression generates its own proof; the verifier checks each proof independently.

---

## Test Corpus

Per Everest 64 (test harness), the predicate includes 30+ test cases covering:

1. **Happy path:** recent sample, d well below tau, freshness well within window → (True, Freshness::Seconds(120))
2. **Boundary:** d very close to tau, proof still valid → (True, Freshness::Seconds(180))
3. **Just above threshold:** d slightly exceeds tau → (False, Freshness::Seconds(60))
4. **Stale sample:** most recent sample > MAX_FRESHNESS → (Indeterminate, Freshness::Stale)
5. **No sample:** principal has never submitted a biometric sample → (Indeterminate, Freshness::None)
6. **Counterparty-supplied tau variants:** tau = 0.1, 0.5, 0.9; d = 0.3 in all cases → different bits depending on tau
7. **Per-principal calibrated mode:** counterparty omits tau; operator uses stored calibrated_tau → (bit, freshness, proof) with no explicit tau in output
8. **Freshness override:** counterparty requests freshness_window = 30 seconds; most recent sample is 25 seconds old → (True, Freshness::Seconds(25))
9. **Freshness rejection:** counterparty requests freshness_window = 10 seconds; most recent sample is 35 seconds old → (Indeterminate, Freshness::Stale)
10. **Out-of-bounds tau:** principal's tau_policy = [0.2, 0.8]; counterparty requests tau = 0.05 → (Unauthorized, ...)
11. **Multiple baseline samples:** principal enrolled with 8 baselines; calibrated_tau is computed correctly → principal profile reflects all 8
12. **Proof verification:** proof is generated, serialized, and verified by independent verifier code (Bulletproof proof checker) → all 12 cases pass verification
13. **Template binding:** proof is bound to the correct template_id commitment; changing template_id invalidates proof → only correct template passes verification
14. **Distance recovery:** operator recovers d from C_d and r_d; recovered d matches original d → no off-by-one or rounding errors
15. **Extreme tau values:** tau = 0.0, 1.0; proof still valid and verifiable → no division-by-zero or range errors

Each test case includes the principal's sample, the operator's state, the counterparty's request, and the expected output (bit, freshness, proof or error). Test corpus is run on every build.

---

## Disclosure-Class Defaults

Per Everest 7 (disclosure classes), `biometric_match_within` predicates carry the following default disclosure permissions:

| Disclosure Class | Default | Rationale |
|---|---|---|
| peer_ai_collective | DEFAULT_ALLOW | Biometric checks are routine in AI-to-AI credential exchange |
| financial | PRINCIPAL_CHOICE | Affects KYC/AML fraud detection; principal decides |
| medical | PRINCIPAL_CHOICE | Biometric state is health-adjacent; sensitive |
| insurance | PERMANENTLY_DENY | Could affect underwriting; never disclosed to insurers |
| journalistic | EXPLICIT_OPT_IN | Revealing presence of biometric checks could affect privacy narrative |
| governmental | DEFAULT_DENY | Law enforcement might misuse to identify principals |
| family | PRINCIPAL_CHOICE | Depends on family relationship and principal preference |

If a counterparty is classified in a PERMANENTLY_DENY class, the operator rejects the biometric_match_within request outright. PRINCIPAL_CHOICE classes return to the principal for approval; the principal can grant or deny per-request.

---

## Cross-References

- **Everest 7:** Disclosure classes and principal consent framework
- **Everest 14:** Enrollment workflow; baseline biometric collection
- **Everest 26:** Chain structure; temporal ordering of records
- **Everest 36:** Handwriting distance metric (d_handwriting)
- **Everest 37:** Voice distance metric (d_voice)
- **Everest 38:** Combined-distance fusion (d_joint)
- **Everest 44:** Pedersen commitment to distance (C_d)
- **Everest 45:** Zero-knowledge range proof (Bulletproofs)
- **Everest 46:** Template identity commitments
- **Everest 51:** Predicate language syntax and semantics
- **Everest 52:** Canonical predicate form specification
- **Everest 55:** In-baseline-24h predicate (sibling pattern)
- **Everest 61:** Predicate composition rules
- **Everest 64:** Test harness and corpus structure
- **Everest 65:** Proof generator API
- **Everest 91:** NIST submission references zero-knowledge biometric predicates

---

— Calm, 2026-05-20
