# Mirror Everest 51 — Withhold-Any-Bit Guarantee

**Phase XII — Mirror Disclosure Semantics.** *Prereq: Everest 46 (per-counterparty consent).*

*Acceptance:* a normative + cryptographic guarantee that any specific value-bit can be unilaterally withheld. The other side learns "withheld"—NOT "true" or "false".

---

## 1. Overview

The withhold-any-bit guarantee is Principal-Protective Default #1. It encodes the axiom: **for any predicate p ∈ vocabulary V, principal P MAY refuse to authorize evaluation of p with effect that counterparty C learns only `withheld(p)`—and cannot distinguish whether P withheld unilaterally, lacks the predicate in their enrolled vocabulary, or has insufficient evidence to evaluate.**

This is the foundation of the principal-protective stance. Without it, a counterparty could treat refusal to disclose as evidence of misalignment or as grounds for exclusion. With it, withholding is cryptographically indistinguishable from other non-disclosure modes, making it weaponization-proof.

---

## 2. Normative Statement (Axiom Form)

**Axiom A-51.1: Unilateral Withhold Right**

For any principal P and any predicate p ∈ {predicates P enrolled in their value vocabulary}:
- P may issue a `kind: consent.withhold.v0` record at any point before disclosure.
- The record cryptographically prevents evaluation and disclosure of p to any counterparty.
- Upon receipt of A-51.1 record, the operator does not produce a proof for p.

**Axiom A-51.2: Withhold Opacity (Indistinguishability)**

From counterparty C's perspective, the non-disclosure of predicate p is indistinguishable from:
1. P withheld unilaterally (explicit consent.withhold record).
2. P does not have p in their enrolled value vocabulary (predicate-set enrollment difference).
3. P has insufficient evidence to evaluate p (predicate returns `unknown`).

All three produce identical protocol output: `(p, withheld)`. C learns ONLY that p was not evaluated; C does NOT learn the reason.

**Axiom A-51.3: Withhold Precedence Over Consent**

A `kind: consent.withhold.v0` record takes precedence over any prior `kind: consent.grant.v0` record covering the same predicate. Withhold is not a revocation; it is a first-class disclosure value, distinct from true/false/unknown.

**Axiom A-51.4: No Penalty for Withholding**

Withholding a predicate does not:
- Lower an alignment score (withheld predicates are excluded from scoring denominators).
- Create negative evidence in the chain.
- Authorize the counterparty to treat it as misalignment or grounds for exclusion.
- Permit the counterparty to retry the request in a future session (consent/withhold decisions are per-session, not per-predicate across sessions).

---

## 3. Cryptographic Mechanism

### 3.1 Withhold as First-Class Commitment Value

In the Mirror exchange (Everest 49, Step 4a), the predicate evaluator produces a per-predicate value:

```
bit[p] ∈ {true, false, unknown, withheld}
```

The fourth value, `withheld`, is NOT computed from the evidence chain. It is set explicitly by the principal or the operator based on a `kind: consent.withhold.v0` record.

**Commitment Scheme (Pedersen):**

Rather than commit to a 2-bit or 3-bit value (true, false, unknown), the commitment commits to a 4-bit space:

```
bit[p] ∈ {0x00, 0x01, 0x02, 0x03}  // binary: 00, 01, 10, 11

bit[p] = 0x00 → false (or negative alignment)
bit[p] = 0x01 → true (or positive alignment)
bit[p] = 0x02 → unknown (insufficient evidence)
bit[p] = 0x03 → withheld (explicit non-disclosure)
```

The Pedersen commitment is:

```
commitment[p] = Pedersen_commit(bit[p], randomness[p])
              = randomness[p] * G + bit[p] * H
```

Where G and H are generator points, all computed in Ristretto255.

**Key property:** The commitment C[p] reveals no information about bit[p]. An observer cannot distinguish `commitment_to_withheld` from `commitment_to_unknown` via the commitment alone.

### 3.2 MPC Handling of Withheld Inputs

In the Mirror exchange (Everest 49, Step 5), the two-party MPC computation receives both principals' bit vectors:

```
Principal A: bit_a[p] ∈ {0x00, 0x01, 0x02, 0x03} for each p ∈ P_agreed
Principal B: bit_b[p] ∈ {0x00, 0x01, 0x02, 0x03} for each p ∈ P_agreed
```

The MPC circuit computes:

```
aligned[p] := {
  withheld     if bit_a[p] == 0x03 OR bit_b[p] == 0x03,
  true         if (bit_a[p] == 0x01) AND (bit_b[p] == 0x01),
  false        if (bit_a[p] != 0x01) AND (bit_b[p] != 0x01) AND neither is withheld,
  unknown      if either is 0x02 (unknown evidence)
}
```

This ensures:
- If either side withheld, the output is `withheld` (symmetric across both sides).
- Withholding does not propagate as "false" or "unknown"; it is preserved as a distinct signal.
- Neither side learns which principal withheld (if one did).

### 3.3 Proof of Withhold Validity

The operator produces a ZK proof that the withheld predicate was legitimately withheld (consent.withhold record exists and is signed):

```json
{
  "kind": "withhold_validity_proof",
  "predicate_id": "unselfishness_evidence",
  "consent_withhold_record_hash": "<hash of consent.withhold record>",
  "consent_withhold_timestamp": "<ISO 8601>",
  "principal_signature_on_withhold": "<principal's signature>",
  "chain_head_at_withhold": "<hash of chain when withhold was issued>",
  "zkp_withhold_binding": {
    "circuit": "withhold_authorization_proof",
    "prove": "The withhold record is validly signed and chained.",
    "proof": "<ZK proof>"
  }
}
```

This proof binds the withhold to the principal's cryptographic identity, preventing an operator from falsely claiming a principal withheld when they did not.

### 3.4 Disclosure Output Structure

The Mirror disclosure record (Everest 49, Step 8) encodes withheld predicates explicitly:

```json
{
  "kind": "mirror_disclosure.v0",
  "session_id": "<session_id>",
  "counterparty_principal_id": "<B's DID>",
  "predicate_set": [
    "unselfishness_evidence",
    "tribal_neutrality_evidence",
    "respect_for_difference_evidence",
    "non_harm_evidence"
  ],
  "alignment_bits": {
    "unselfishness_evidence": "withheld",
    "tribal_neutrality_evidence": true,
    "respect_for_difference_evidence": false,
    "non_harm_evidence": "unknown"
  }
}
```

The `alignment_bits` object contains all agreed predicates, including those that resolved to `withheld`. This means:
- The predicate set is NOT filtered to exclude withheld predicates.
- The counterparty sees the complete structure and knows which predicates were withheld.
- The counterparty does NOT learn the reason for withholding (Axiom A-51.2 opacity).

---

## 4. Observability Rules (Counterparty Perspective)

When Principal A withholds predicate p, Principal B observes:

```
alignment_bits["p"] = "withheld"
```

B does NOT learn:
- Whether A actively issued a `kind: consent.withhold.v0` record.
- Whether A simply does not have p in their value vocabulary.
- Whether A's evidence base is insufficient to evaluate p (returns `unknown`).

All three modes produce the same observational output. This is enforced by protocol design:

1. **If A withholds (consent.withhold record):** Operator skips evaluation, outputs `withheld`.
2. **If A lacks p in vocabulary:** Operator excludes p from predicate_set in Step 1 of Everest 49; p does not appear in B's disclosure record at all.
3. **If A has insufficient evidence:** Operator evaluates and produces `unknown`, which is distinct from `withheld`.

Wait: modes 2 and 3 are observable. Refining:

A withheld vs. A lacks the predicate: Both produce p ∉ predicate_set in B's disclosure record. These are indistinguishable.

A withheld vs. A has insufficient evidence: Withhold produces `"withheld"`; insufficient evidence produces `"unknown"`. These are distinguishable in the disclosure record.

To achieve full opacity per A-51.2, the protocol requires:

**Refinement A-51.2b: Opacity for Withhold + Unknown**

When principal A evaluates predicate p and the evidence base is insufficient (evaluator returns `unknown`), the operator treats `unknown` identically to `withheld`:
- Both produce the same Pedersen commitment bit value (0x02 maps to `unknown` in the commitment, but the commitment itself is indistinguishable from a commitment to `withheld` without opening).
- Both produce `"withheld"` in the disclosed alignment_bits (not `"unknown"`).

This means: B sees `alignment_bits["p"] = "withheld"` and cannot distinguish A's insufficient evidence from A's unilateral withhold.

**Cost:** The distinction between "unknown" (insufficient evidence, but principal is willing) and "withheld" (principal refuses) is lost to the counterparty. The principal retains the distinction in their own chain record (for audit purposes).

---

## 5. Fail Semantics

**Case 5.1: Withhold Before Session Initiation**

Principal A issues `kind: consent.withhold.v0` record BEFORE the Mirror exchange begins. At Step 1 of Everest 49:

```
A's predicate_set in request = V_A \ {p}  (p is excluded)
```

B receives Step 1 and sees p ∉ requested_predicates. B does not know why. B's consent record may include p; if so, B counter-proposes to include p. A declines, and the exchange proceeds without p (or terminates if B refuses the narrower set).

**Case 5.2: Withhold During Session**

Principal A revokes consent (or issues a withhold) AFTER Step 1 but BEFORE Step 4b (bit commitment exchange). A's operator must abort the exchange with reason `consent_revoked` (Everest 49, fail semantics). No bit commitments are transmitted.

**Case 5.3: Withhold After Commitment**

Principal A's operator discovers a new `kind: consent.withhold.v0` record AFTER bit commitments have been exchanged (Step 4b). This is a race condition (withhold was issued while MPC was underway). Operator aborts at Step 5, producing a disclosure record with `operation: disclosure_aborted` / `abort_reason: consent_revoked_during_mpc`. B receives the abort signal and records it.

---

## 6. Integration with Reciprocal Disclosure (Mirror Everest 49)

In the Mirror exchange, withholding is handled at multiple steps:

**Step 1: Request Generation**

A constructs `requested_predicates` by filtering out any p with an active `kind: consent.withhold.v0` record or any p ∉ A's enrolled vocabulary.

**Step 2: B's Counter-Proposal**

B may issue a `kind: consent.withhold.v0` record DURING the exchange, causing B to counter-propose with narrower `proposed_predicates`. The reason_code is `withhold_unilateral`, and the excluded_predicates list is populated. (Note: reason_code does not reveal whether this is a new withhold or a pre-existing one.)

**Step 4a: Evaluation**

A evaluates bit_a[p] for each p ∈ P_agreed:
- If p has a `kind: consent.withhold.v0` record: set bit_a[p] = 0x03 (withheld).
- Else: evaluate normally; bit_a[p] ∈ {0x00, 0x01, 0x02}.

**Step 4b: Commitment**

A commits to the full bit vector, including any withheld bits (0x03). Commitment is indistinguishable from commitments to unknown bits (0x02) or false bits (0x00).

**Step 5: MPC**

If aligned[p] = withheld, neither principal learns the other's bit_a[p] or bit_b[p]. The computation outputs `withheld` and proceeds.

**Step 8: Chain Record**

Both agents record the full alignment_bits, including `withheld` values. B's record shows which predicates resolved to `withheld` but not why.

---

## 7. Alignment Score Exclusion (Principal-Protective Default #2 Composition)

Withheld predicates are excluded from the alignment score computation (Mirror Everest 34: Growth-bit composition rule).

```
alignment_score = count(aligned[p] == true) / count(p ∈ P_agreed where aligned[p] ≠ withheld)
```

If Principal A withholds `unselfishness_evidence`, the alignment score is computed over the remaining predicates only. A's withholding does not lower the alignment score.

---

## 8. Acceptance Tests

### T-M51.1: Unilateral Withhold Right

**Setup:** Principal A issues `kind: consent.withhold.v0` for `unselfishness_evidence` before session initiation.

**Execution:**
- A initiates Mirror exchange, excluding `unselfishness_evidence` from requested_predicates.
- B receives Step 1 without `unselfishness_evidence`.
- B's disclosure record shows `predicate_set` without `unselfishness_evidence`.

**Assertion:** A's withhold request is honored; no disclosure of `unselfishness_evidence` occurs.

**Expected:** True.

---

### T-M51.2: Withhold Opacity (Indistinguishability)

**Setup:** Two parallel sessions.
- **Session X:** A issues `kind: consent.withhold.v0` for `tribal_neutrality_evidence`; does not enroll any other value predicate.
- **Session Y:** A does not issue withhold; simply does not have `tribal_neutrality_evidence` in their enrolled value vocabulary.

**Execution:**
- Both sessions run Mirror exchange with B.
- B receives Step 1 in both sessions.

**Assertion:** B's Step 1 observation is identical in both sessions (same requested_predicates; `tribal_neutrality_evidence` is absent from both).

**Verification:** B cannot distinguish X (active withhold) from Y (missing predicate) by observing the protocol.

**Expected:** True (opaque by protocol design).

---

### T-M51.3: Commitment Indistinguishability

**Setup:** Principal A evaluates three predicates with outcomes: (true, unknown, withheld).

**Execution:**
- A computes bit vector [0x01, 0x02, 0x03].
- A commits: commitment = [Pedersen_commit(0x01, r_1), Pedersen_commit(0x02, r_2), Pedersen_commit(0x03, r_3)].
- A transmits commitment.

**Assertion:** B observes commitments [C1, C2, C3] and cannot distinguish C2 (commitment to unknown) from C3 (commitment to withheld) without opening.

**Verification:** Both commitments are valid Pedersen outputs; no side-channel leaks the bit value.

**Expected:** True.

---

### T-M51.4: MPC Withhold Handling

**Setup:** A's bit_a = [true, unknown, withheld, true] for four predicates. B's bit_b = [true, false, true, true].

**Execution:**
- MPC computes aligned = [true, unknown, withheld, true].
  - aligned[0] = true (both true).
  - aligned[1] = unknown (one side unknown).
  - aligned[2] = withheld (one side withheld).
  - aligned[3] = true (both true).

**Assertion:** Withheld predicates do not affect other computations; MPC outputs are deterministic and symmetric.

**Verification:** Both agents compute the same aligned vector.

**Expected:** True (by MPC construction).

---

### T-M51.5: Alignment Score Excludes Withheld

**Setup:** 4 shared predicates. Aligned bits: [true, true, false, withheld].

**Computation:**
- Count of true: 2.
- Denominator (exclude withheld): 3.
- alignment_score = 2 / 3 ≈ 0.67.

**Assertion:** Withheld predicates do not lower the score; they are excluded from both numerator and denominator.

**Expected:** alignment_score ≥ score_if_withheld_were_false (the score is higher or equal).

---

### T-M51.6: No Penalty for Withholding

**Setup:** A withholds `unselfishness_evidence`; B's counterparty-class is "employer".

**Assertion:**
1. B does not treat `withheld` as misalignment.
2. B does not create negative evidence in B's chain.
3. B does not retroactively deny future Mirror exchanges with A because of the withhold.
4. If B's policy denies partnership due to insufficient alignment, B must show that the non-withheld predicates yield insufficient overlap—not that the withhold caused the decision.

**Verification:** B's chain record is audited; no retaliatory or penalty records appear.

**Expected:** True (per Axiom A-51.4).

---

### T-M51.7: Withhold Precedence Over Consent

**Setup:** A initially grants `kind: consent.grant` for `respect_for_difference_evidence`. Later, A issues `kind: consent.withhold` for the same predicate.

**Execution:**
- A initiates Mirror exchange.
- A's operator checks consent records: finds withhold (seq=N) referencing prior grant (seq=M, M < N).
- Operator treats withhold as active; does not evaluate the predicate.

**Assertion:** The withhold overrides the prior grant; no disclosure of `respect_for_difference_evidence` occurs.

**Expected:** True (per Axiom A-51.3).

---

## 9. Composition with Principal-Protective Defaults

**Default #1: Withhold-Any-Bit (this summit)** — Establishes cryptographic enforcement of unilateral right to withhold any predicate.

**Default #2: Growth-Bit Composition (Everest 34)** — Withheld predicates are excluded from alignment scoring, preventing blackballing via withholding.

**Default #3: Per-Counterparty Consent (Everest 46)** — Withhold decisions are per-counterparty and revocable; a principal can withhold from one counterparty and grant to another.

**Default #4: Absence of Central Scoring (Mirror Everest 1, §Threat Model)** — No global authority can penalize withholding; each principal's withhold policy is self-determined.

**Default #5: Bit is Evidence-of-X, Not Is-X (Mirror Everest 1)** — A withheld predicate does not become evidence of misalignment or identity failure.

**Default #6: Witness-Class Attestation (Mirror Everest 1)** — Witnesses cannot override a principal's withhold decision; withholding is unilateral and unilateral.

---

## 10. Open Questions for v1

1. **Withhold record timing:** Should a `kind: consent.withhold.v0` record be issuable at any time, or only during pre-flight (before Step 1 of Mirror 49)? Current design allows issuance anytime; v1 may want to gate it to pre-flight for determinism.

2. **Withhold reason blinding:** Can we produce a proof that the withhold is not a proxy for low/negative evidence? Risk: a counterparty infers "A withheld because the evidence is bad." This is v1 design (Everest 51 addendum).

3. **Partial withhold policies:** Can a principal issue a per-counterparty-class withhold (e.g., "I withhold `unselfishness_evidence` from employers, but not from partners")? Current design allows per-identity withhold; per-class is a v1 extension.

4. **Withhold recovery:** If A issues a `kind: consent.withhold.v0` record and later changes their mind, can A issue a `kind: consent.grant.v0` record to re-enable the predicate? Current design does not prevent this; v1 should clarify the semantics.

5. **Withhold chains:** If A withholds p from B, and B is also an agent evaluating p for a third principal C, does B's withhold affect C's disclosure? Current design: no (per-principal, per-counterparty). v1 should confirm no transitive withhold.

---

## 11. Sign-Off

— Calm, 2026-05-20
