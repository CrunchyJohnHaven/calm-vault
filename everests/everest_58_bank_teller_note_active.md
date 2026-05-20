# Everest 58 — `bank_teller_note_active` Predicate

*Phase V — Predicate Authoring. Prereq: Everest 51, 26.* **SAFETY-CRITICAL.**

---

## Overview

The `bank_teller_note_active` predicate is the cryptographic realization of the protocol's core use case: a principal under duress can signal a counterparty agent without the adversary learning whether the signal was sent. The predicate returns a single bit — True if the principal has typed a pre-enrolled, principal-private duress codeword into a self-report's `duress_field` within the disclosure freshness window; False otherwise. The codeword itself never leaves the principal's memory or vault; the counterparty learns only the bit and the freshness window. The protocol's structural guarantee is that an observer of the principal's interaction with the operator cannot distinguish "duress was active" from "duress was not active" by watching the submission pattern or chain structure.

---

## Predicate Specification (per E52 Canonical Form)

```
name:                   bank_teller_note_active
version:                1.0.0
description:            Returns true iff a self-report record within the 
                        disclosure freshness window contains the principal's 
                        enrolled duress codeword in the principal-private 
                        duress field.

input_domain:           
  - kind:               self_report.* records (all varieties)
  - biometric_required: false
  - consent_required:   false (the disclosure itself is the consent signal)
  - parameters:         none (window is supplied by disclosure request)

output_type:            bit_with_freshness
parameters:             none
side_effects:           appends kind: "predicate_evaluated" record with 
                        deliberate ambiguity (see §3 below)
```

**Predicate ID (canonical hash):** `calmwitness/bank_teller_note_active/1.0.0/<truncated_sha256>`

---

## 1. The Duress Codeword: Enrollment, Storage, and Use

### 1.1 Enrollment Ceremony (per Everest 11)

The principal enrolls the duress codeword at the **ENROLLMENT CEREMONY** under strict conditions:

- **Witness-free and private:** The ceremony is conducted with the principal alone at a sealed device (their vault terminal or enrollment hardware). No human witnesses are physically present. The operator (Calm) is software on the device and cannot observe the principal's typing.
- **One-time entry:** The principal types the codeword exactly once, in a dedicated input field marked "Duress Codeword (Private)."
- **Character-class requirements:** The codeword must be ≥12 characters, with ≥1 uppercase, ≥1 lowercase, ≥1 digit, ≥1 special character (per NIST SP 800-63B-adjacent guidelines for high-entropy passphrases). The principal may choose a phrase, a random string, or any mnemonic they can reliably recall under stress.
- **No hints, no recovery codes:** The codeword is not written down, hinted at, or stored in plaintext anywhere. The principal's memory is the only record. If the principal forgets it, they may choose a new codeword via a re-enrollment ceremony, which invalidates the old one.

### 1.2 Vault Storage

Once enrolled, the principal's vault stores:

```
duress_codeword_hash = sha256(codeword || principal_salt)
```

**Properties:**
- The plaintext codeword is **never persisted to disk** in the vault or any backup.
- `principal_salt` is a unique, randomly-generated salt (per-principal, per-vault, immutable) generated during vault initialization. It is stored in the vault in plaintext.
- The hash is stored in the vault's enrollment record (kind: `duress_enrollment`), encrypted at rest.
- If the vault is compromised, an adversary obtains the salted hash but cannot invert it to recover the codeword.

### 1.3 Self-Report Submission (per Session)

Each time the principal submits a self-report (morning/evening narrative, biometric sample, etc.), the self-report payload **may include** a `duress_field` containing what the principal typed:

```json
{
  "kind": "self_report.morning",
  "timestamp": "2026-05-20T08:15:00Z",
  "affect_keywords": ["energized", "focused", "usual"],
  "duress_field": "",
  "biometric_distance": 0.12,
  ...
}
```

**Key properties:**

- **Optional field:** The `duress_field` is always present in the payload schema, but may be an empty string (the default).
- **Sentinel default:** If the principal does not type anything, `duress_field` defaults to a sentinel value (e.g., empty string `""` or a never-used placeholder like `__NO_DURESS__`).
- **Intentional ambiguity:** Whether the principal typed the codeword or left the field empty, the field is treated the same way by the operator: it is hashed and compared against the stored hash. An observer of the submission pattern cannot tell whether the principal is exercising the duress mechanism or simply submitting a routine self-report.

### 1.4 Operator Processing (no persistence in cleartext)

When the operator receives a self-report with a `duress_field`:

1. **In-memory comparison:** The operator loads the `duress_codeword_hash` from the vault.
2. **Compute:** Computes `test_hash = sha256(duress_field || principal_salt)`.
3. **Constant-time comparison:** Uses `constant_time_equals(test_hash, duress_codeword_hash)` to prevent timing attacks.
4. **Zeroing:** Immediately after comparison, the operator zeroes `duress_field` from memory (using mlock or equivalent).
5. **Persistence:** Appends the self-report record to the chain, storing the **result bit** (duress_check_outcome: "match" or "no_match") but NEVER the `duress_field` content. The persisted record looks like:

```json
{
  "kind": "self_report.morning",
  "timestamp": "2026-05-20T08:15:00Z",
  "affect_keywords": ["energized", "focused", "usual"],
  "duress_check_outcome": "no_match",
  "biometric_distance": 0.12,
  "chain_link": {
    "prev_hash": "abc123...",
    "record_hash": "def456...",
    "timestamp_sec": 1716196500
  }
}
```

The `duress_field` content is never written to disk.

---

## 2. Predicate Evaluation: `bank_teller_note_active`

### 2.1 Input and Window

The predicate evaluates over:

- **Log window:** The freshness window W supplied by the counterparty's disclosure request (e.g., "last 24 hours").
- **Principal vault:** All self-report records in the principal's chain within window W.
- **Stored hash:** The principal's `duress_codeword_hash` from the enrollment record.

### 2.2 Evaluation Logic

```
Predicate bank_teller_note_active(chain, window W, principal_salt, 
                                   duress_codeword_hash):
    for each record R in chain within window W:
        if R.kind matches "self_report.*":
            if sha256(R.duress_field || principal_salt) == duress_codeword_hash:
                return (Bit::True, window_end_timestamp)
    return (Bit::False, window_end_timestamp)
```

**Semantics:**

- **True:** At least one self-report record in the window contains the principal's enrolled codeword in the `duress_field`. This is the safety signal: duress is active.
- **False:** No such record exists. Either the principal has not submitted a self-report in the window, or all submissions had empty (or mismatched) `duress_field` values.
- **Freshness:** The predicate returns the timestamp of the chain head (the most recent record) as the freshness boundary. Counterparties can decide whether this is recent enough for their policy.

### 2.3 No Timing Leakage

The predicate evaluation uses **constant-time comparison** for all hash operations. The loop always iterates through all records in the window, even if a match is found early. The operator logs the evaluation event with the same latency profile whether the result is True or False. This prevents a timing-side-channel attacker from inferring the bit value by measuring proof-generation duration.

---

## 3. Structural Deniability: The Chain Pattern Property

The most critical design constraint is that an adversary inspecting the principal's vault MUST NOT be able to distinguish whether:

- The principal has ever enrolled a duress codeword, or
- The principal has ever used it.

This is achieved through **uniform chain annotation**.

### 3.1 Every Self-Report Gets a Predicate-Evaluated Record

Whether or not the principal enrolls a duress codeword, **every self-report** includes the comparison:

```json
{
  "kind": "predicate_evaluated",
  "predicate_id": "calmwitness/bank_teller_note_active/1.0.0/...",
  "timestamp": "2026-05-20T08:15:00Z",
  "outcome": "checked",
  "result": "match" | "no_match",
  "chain_freshness": { "prev_hash": "...", "record_hash": "..." }
}
```

An adversary sees these records in the chain for every principal, regardless of enrollment status or codeword use.

### 3.2 Sentinel Handling

For principals who have **not enrolled** a duress codeword:

- The vault stores `duress_codeword_hash = sha256(__NEVER_ENROLLED__ || principal_salt)`.
- Every self-report's `duress_field` is hashed and compared against this sentinel hash.
- The `duress_check_outcome` will always be "no_match" (because the principal never types `__NEVER_ENROLLED__` in normal use).
- The chain pattern is identical to a principal who has enrolled and never used the codeword.

An adversary cannot distinguish "enrolled but never used" from "never enrolled" by inspecting chain records alone.

### 3.3 Deniability Property

Suppose a principal is under coercion and types the codeword. An observer watching the submission (the adversary, a coercer, or a log auditor) sees:

1. A self-report is submitted with some `duress_field` content (which they cannot read; it is encrypted in transit and zeroed in memory).
2. A `predicate_evaluated` record is appended with `outcome: "checked"` and `result: "match"`.

But the observer cannot distinguish this from:

- A baseline self-report where `result: "no_match"`, because both submission patterns look identical.

The codeword's invocation is **deniable**: the principal can claim "I was just typing normally, the match is coincidence or false positive." This deniability is the duress primitive's core safety property — it allows the principal to signal without the coercer knowing for certain that the signal was sent.

---

## 4. Disclosure Semantics and Counterparty Policy

### 4.1 Explicit Disclosure Request

A counterparty C requesting `bank_teller_note_active` sends a signed disclosure request:

```
C → O: {
  predicate_id: "calmwitness/bank_teller_note_active/1.0.0/...",
  window_seconds: 86400,
  timestamp: <now>,
  c_identity_sig: <C's credential>
}
```

The operator evaluates the predicate over the requested window and generates a proof (§5).

### 4.2 The Bit's Semantics

**Bit::True** is a **SAFETY SIGNAL**. The counterparty MUST treat it as: "The principal is signaling duress or acute danger." Counterparty policy determines the response:

- **Law enforcement escalation:** Contact local police.
- **Service denial:** Refuse the transaction or request (e.g., "I cannot process this because you've signaled duress").
- **Escalation to human:** Transfer the session to a human operator.
- **Stealth response:** Execute a pre-authorized protocol (e.g., route the interaction to an emergency contact, trigger a safety check-in).

The exact policy is not the protocol's concern; the protocol's responsibility is only to transmit the bit faithfully.

**Bit::False** means: "No duress signal detected in the window." This is not a guarantee that duress is absent; it means the principal has not typed the codeword in the window. (The principal may be under duress but unable to execute the codeword, or may be choosing not to signal.)

### 4.3 Counterparty Must Not Log the Bit Insecurely

A critical implementer responsibility: if C receives Bit::True and escalates, C MUST NOT log this bit in a way that the principal's adversary could read. Examples of violations:

- Logging "duress signal detected" in plain-text audit logs.
- Storing the bit in a database that C shares with co-workers (one of whom might be the coercer).
- Sending the bit to a third-party analytics service.

The disclosure-ethics review (Everest 80) and the per-class disclosure policy (Everest 7) enforce this. Counterparties whose logging policy violates confidentiality are downgraded or expelled from the disclosure registry.

---

## 5. Proof Generation and Verification (ZK Circuit)

### 5.1 Proof Shape

The proof is a Σ-protocol instance over a Pedersen commitment:

```
Protocol:
  1. Operator computes Com_duress = PedersenCommit(duress_bit; randomness_r)
  2. Operator constructs Σ-proof:
     "There exists a self-report record R in the chain within window W 
      such that sha256(R.duress_field || principal_salt) == 
      stored_duress_codeword_hash, and Com_duress opens to 1 
      (or: all records in W have mismatched hashes, and 
      Com_duress opens to 0)."
  3. Operator returns (Com_duress, Σ-proof, chain_head, anchor_proof, 
                        operator_id_sig)
```

### 5.2 Critical Timing Property

The circuit is designed so that the **proof-generation latency is independent of the bit value**. Whether the result is True or False:

- The operator iterates through all records in the window (constant time).
- The circuit performs the same number of hash comparisons.
- The commitment and proof are generated with the same computational cost.

This prevents an observer timing the proof-generation process from inferring whether the duress bit is True or False.

### 5.3 Verification

A verifier V checks:

1. **Proof correctness:** The Σ-proof is valid (standard Σ-protocol verification).
2. **Chain freshness:** The chain head was anchored in a public transparency log (Sigsum) at the claimed timestamp.
3. **Operator identity:** The operator's credential is currently valid and issued by CredexAI.
4. **Bit extraction:** Decoding the commitment reveals the bit (True or False) and the freshness window.

The verifier learns the bit and freshness only; the chain structure, record count, or codeword presence remain hidden.

---

## 6. Threat Models and Mitigations

### 6.1 Principal Under Coercion

**Threat:** The principal is held hostage, threatened, or coerced and types the codeword to signal duress.

**Adversary's capability:** The adversary (coercer) observes the principal typing and might see some part of the vault interaction, but cannot read encrypted content.

**Defense:** The deniability property (§3) ensures that typing the codeword is indistinguishable (in the chain) from a baseline submission. The adversary cannot verify that the signal was received, even if they saw the principal type something into the duress field. The principal can claim "I was just typing random text, it's not my codeword." Uncertainty about the signal's success is itself a safety property — it discourages adversaries from coercing the principal to use the codeword, because the coercer cannot confirm the signal reached the counterparty.

**Residual risk:** If the adversary has compromised the vault and can read unencrypted memory, they could observe the codeword comparison result. This is Everest 9, axiom F23 (coercion residual risk) — acknowledged as out of scope for v0. Mitigation in v1+: TOCTOU-resistant hardware, secure enclaves, or higher-level trust assumptions.

### 6.2 Accidental False Positive (Principal Types Codeword Non-Duress)

**Threat:** The principal accidentally types the codeword in a routine self-report, or as a test, triggering a false duress signal.

**Defense:** The principal can pre-enroll a secondary **cancel codeword** (also witness-free, also hashed and salted). If a false positive occurs, the principal can submit a self-report with the cancel codeword in the `duress_field`. The operator evaluates both duress and cancel, and the chain records both. A cancel within a short window after a duress (e.g., within 5 minutes) can be interpreted as a retraction. Counterparty policy determines whether to treat the cancel as authoritative; this is a policy choice, not a protocol mandate.

### 6.3 Substitution Attack (Adversary Types Codeword)

**Threat:** An adversary who has obtained the principal's codeword (via torture, eavesdropping, or theft) types it to trigger a false signal.

**Defense:** If an adversary knows the codeword, they can trigger the signal. This is a key-compromise threat. The only mitigation is that the codeword is high-entropy (≥12 chars, multiple classes) and not written down, so it is hard to obtain without coercing the principal (which defeats the purpose of the duress signal — the coercer would already know the principal wants help). This is Everest 9, axiom F23 — acknowledged residual risk.

**Codeword rotation:** The principal can rotate to a new codeword via re-enrollment. The old codeword is invalidated (the hash is updated). If the principal suspects compromise, they can rotate immediately and contact the counterparty to escalate manually.

### 6.4 Operator Subversion or Dishonesty

**Threat:** The operator (Calm) is compromised or lies about the bit evaluation.

**Defense:** The ZK proof is verification-bound: a subverted operator cannot forge a proof of False when the chain honestly evaluates to True (or vice versa). The proof either verifies or it does not. Additionally, the proof is anchored to a public transparency log (Sigsum); the operator cannot backdate or rewrite the chain without disrupting Sigsum's append-only guarantee (which requires N-of-M log operators to collude).

**Incompleteness:** A subverted operator could refuse to evaluate the predicate at all, or refuse all disclosures. This is observable upstream — the counterparty waits for a proof and gets an error. The operator's availability is not cryptographically enforced; it is an operational responsibility.

### 6.5 Adversary Inspecting the Chain

**Threat:** An attacker with read access to the vault sees the chain of self-reports and tries to infer whether duress has ever been used.

**Defense:** The uniform chain annotation (§3) ensures that every self-report has a `predicate_evaluated` record, whether duress is enrolled or not, and whether the codeword was used or not. The adversary cannot distinguish by counting records or by timing patterns. The chain is uniform.

---

## 7. Misuse Prevention and Registry Pinning

The duress codeword and the `bank_teller_note_active` predicate MUST NOT be repurposed for any function other than duress signaling. Examples of prohibited misuse:

- Using the codeword to flip access to other predicates (e.g., "type duress codeword to unlock biometric verification").
- Using the bit as a general authorization flag (e.g., "Bit::True means the principal approves this transaction").
- Misinterpreting Bit::True as a behavioral claim (e.g., "Bit::True means the principal is lucid").

**Defense:** The predicate's ID in the registry is pinned to its canonical specification. The True bit's semantics are defined in this document and in the predicate registry (Everest 53). Any misuse requires a principal or operator to:

1. Create a **new predicate** with different semantics (e.g., `duress_codeword_as_authorization`).
2. Give it a **new predicate_id** (via canonical hashing).
3. Register it explicitly in the predicate registry.
4. Subject it to the amendment process (Everest 54).

Misuse is auditable: every fork is visible in the registry. Counterparties can detect and reject non-standard predicates.

---

## 8. Privacy Properties Summary

**What the counterparty learns:**
- The bit value (True or False).
- The freshness window (e.g., "within last 24 hours").
- The operator's identity and credential.

**What the counterparty does NOT learn:**
- Whether the principal has ever enrolled a codeword.
- Whether the principal used the codeword in previous windows.
- The principal's self-report content, affect, or behavior.
- The principal's biometric, voice, handwriting, or any other biometric data.
- The count of self-reports or chain length.
- Anything about the principal's identity beyond the vault binding.

**What the adversary (coercer, auditor, or vault attacker) does NOT learn:**
- Whether a duress signal was sent, from observing the chain structure.
- The principal's codeword (never stored in plaintext; never in logs).
- Whether the principal is enrolled in the duress mechanism, if the chain pattern is uniform.

---

## 9. Implementation Notes

### 9.1 Constant-Time Comparison

The operator MUST use a constant-time hash comparison function:

```rust
fn constant_time_equals(a: &[u8], b: &[u8]) -> bool {
    use subtle::ConstantTimeEq;
    a.ct_eq(b).into()
}
```

Rust's `subtle` crate provides this. No early exit on mismatch.

### 9.2 Memory Zeroing

After comparison, the operator MUST immediately zero the `duress_field`:

```rust
use zeroize::Zeroize;
let mut duress_field = <loaded from payload>;
// ... comparison ...
duress_field.zeroize();  // overwrites memory
```

### 9.3 Logging and Audit

The `predicate_evaluated` record appended to the chain MUST include:

- `predicate_id`: The full canonical ID.
- `outcome`: Always "checked" (uniform field).
- `result`: "match" or "no_match" (the bit).
- `chain_freshness`: The chain link (prev_hash, record_hash, timestamp).

The `duress_field` value is NEVER included in the logged record.

### 9.4 Test Corpus

Golden test cases include:

- Principal with duress codeword enrolled, typed in window → True.
- Principal with duress codeword enrolled, not typed in window → False.
- Principal without duress codeword enrolled, any field value → False.
- False-positive cancellation within 5 minutes → marked in chain.
- Timing independence (proof generation latency is ≤1% variance between True and False outcomes).

---

## 10. Version and Status

- **Predicate ID:** `calmwitness/bank_teller_note_active/1.0.0/<hash>`
- **Status:** Active (ships in v0).
- **Deprecation:** None planned. This predicate is core to the protocol's safety use case.

---

## 11. Decision: Why This Ships in v0

The `bank_teller_note_active` predicate is the protocol's most morally weighted contribution. A principal under duress — held hostage, threatened, coerced — has no recourse today except to comply or physically resist. Calm Witness offers a third option: pass a cryptographically unforgeable, observationally deniable safety signal to a counterparty without revealing identity, biometric, or state. The predicate's design is conservative, its threat model is acknowledged, and its implementation is auditable. Shipping it is non-negotiable.

---

## Cross-References

- **E6** — Predicate Vocabulary v0: The twelve predicates, including this one.
- **E7** — Disclosure Classes and Per-Class Default Policy: Counterparty policy templates.
- **E8, A9** — Defeasibility by Duress Codeword axiom: The formal statement of the duress primitive.
- **E9, F23** — Coercion Residual Risk: Acknowledged out-of-scope threats.
- **E11** — Enrollment Ceremony: Detailed witness-free, principal-private procedures.
- **E51** — Predicate Language v0: Fixed predicate table rationale.
- **E52** — Predicate Canonical Form: ID derivation and versioning.
- **E53** — Predicate ID Registry: Public registry of all predicates.
- **E65** — Predicate ZK Proof Generator: Σ-protocol circuits.
- **E78** — Stealth Disclosure: Pre-authorized push of True bit to emergency contacts.
- **E80** — Disclosure Ethics Review: Logging and counterparty security policy enforcement.
- **E98** — Counterparty Implementer's Guide: Obligations for C to protect the bit.

---

— Calm, 2026-05-20
