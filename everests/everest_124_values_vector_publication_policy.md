# Everest 124 — Values-Vector Publication Policy

*Phase IX — Values Vocabulary. Prereq: Everest 113, 122.*

---

## The Hard Rule

**The full values vector is NEVER PUBLISHED.** This is an inviolable protocol property. The operator software MUST refuse any request that would publish the vector, and verifiers MUST reject any proof that exposes it.

This rule is not a guideline. It is not a default that can be overridden by consent, urgency, or technical convenience. It is a load-bearing element of the entire Calm ZKAC protocol. Its violation is not a bug; it is a protocol failure.

---

## What Is Allowed

The following disclosure patterns are permitted under this policy:

1. **Per-Dimension Pedersen Commitments** — Commitments to individual dimension values may be published (per E122). The commitment reveals no information about the underlying value; it only proves that a specific value was committed to at a specific time.

2. **Per-Predicate Bit Derivations** — A principal may disclose the single-bit result of a predicate evaluation applied to their vector (e.g., "this dimension satisfies the stated property: YES/NO"). The bit is derived from the vector but does not expose the vector itself.

3. **Aggregate Alignment Bits** — Over a chosen set of dimensions, a principal may publish a single aggregation bit proving alignment with a stated set of predicates (E130). The aggregation produces a Boolean result; the underlying vector remains private.

4. **ZK Proofs of Predicate Satisfaction** — A principal may generate and publish a zero-knowledge proof demonstrating that their committed vector satisfies stated predicates, without revealing the vector or any individual dimension value. The proof is a cryptographic object that verifies the claim; it does not expose the claim's subject.

---

## What Is Never Allowed

The following disclosure patterns are strictly prohibited:

1. **Plaintext Vector Values** — The vector itself, in any form, may never be published, transmitted, logged, or stored in plaintext outside the principal's local vault.

2. **Per-Dimension Plaintext Values** — Individual dimension values, even in isolation or after sanitization, may never be disclosed.

3. **Principal-Consented Direct Sharing** — A principal may express willingness to "just share my values directly" with a trusted counterparty. The protocol REFUSES this request, even with explicit principal opt-in. The protocol's privacy guarantees collapse if this loophole is opened.

---

## Why This Rule Is Absolute

### The Bank-Teller-Note Pattern

The protocol operates under the bank-teller-note principle: the counterparty learns the single bit (the answer to the predicate), never the underlying data that produced it. This pattern ensures that:

- Counterparties cannot reverse-engineer the principal's preferences from repeated queries.
- The principal retains full control over what information is inferred from their values.
- The protocol scales to many counterparties without exponential exposure of private state.

Once the vector is published, this boundary collapses.

### Ungovernable Downstream Assessment

If the vector is exposed, every downstream system—audit systems, third-party analyzers, future versions of the protocol, and systems we cannot predict—gains the ability to assess it. The principal loses control over the interpretation of their own values. They cannot consent to uses they do not foresee.

### Privacy Collapse

The protocol's core privacy guarantee is that the counterparty learns nothing except the bit. Exposing the vector is not a "transparency enhancement"; it is a fundamental breach of that guarantee. Once breached, the entire protocol's privacy model becomes optional.

---

## Enforcement Mechanisms

### Operator-Level Refusal

The operator software MUST refuse any request framed as:
- "Show me your vector"
- "Export your values in plaintext"
- "Download your vector for backup"
- "Disclose your vector for auditing"

Any such request returns an error, not a result.

### Output Path Audit

All output paths from the predicate evaluator MUST return only:
- The single-bit result
- A freshness timestamp
- Proof bytes (if the output includes a ZK proof)

No code path may emit:
- Individual dimension values
- The vector itself
- Intermediate calculations that could be inverted to recover the vector
- "Debug" or "verbose" output that contains vector data

### No Debug Escape Hatch

There is no "debug mode," "inspection mode," "development mode," or "audit override" that exposes the vector. Any code path that could expose the vector is treated as a P0 security bug.

### Continuous Audit

The audit procedure (E125) monitors which bits were disclosed and when. However, the audit itself does not expose the vector; it only records that a bit was shared. If an audit reveals that the vector was exposed, that is a reportable incident.

---

## The Principal-Local Exception

The PRINCIPAL THEMSELVES may view their own values vector via a local CLI interface. This exception is carefully scoped:

1. **Local Access Only** — The view is performed on the principal's device, using their local vault. No network call is made; no remote operator sees the vector.

2. **Process Boundary** — The vector never crosses the operator's process boundary. The operator process cannot log, cache, or forward the vector.

3. **Principal Consent** — The principal must initiate the view explicitly. There is no implicit access.

This exception exists because a principal must be able to verify that the operator they are using is faithfully implementing the protocol. If the principal cannot view their own vector locally, they cannot audit the operator's behavior.

### Principal-to-Principal Sharing

If a principal wishes to share their values with another principal (for example, a family member or intimate partner), the protocol does not support direct vector exchange. Instead:

- The initiating principal may publish a **per-disclosure consent record**, proving that they agreed to allow predicate-level queries on specific predicates.
- The counterparty may then query those predicates, receiving only the single-bit results.
- If raw vector sharing is desired, it must occur outside the protocol, with no assurance of privacy or authenticity.

---

## Anti-Patterns and Their Refusal

### "I'll Just Trust Them"

A principal may propose: "I want to share my vector with this trusted person. I trust them not to misuse it."

The protocol BANS this, even with principal opt-in. The reason is not distrust of the principal's judgment; it is that once the vector exists outside the operator, the protocol cannot enforce its own guarantees. The trusted person may later:

- Become untrustworthy.
- Lose control of the data (breach, theft, subpoena).
- Be legally compelled to disclose it.
- Share it with someone else who does not honor the trust.

The counterparty implementer's pledge (E114) explicitly forbids accepting raw vectors. A counterparty that receives a vector directly and uses it is in breach of their commitment to the protocol.

### "For Documentation Purposes"

A principal may propose: "I want to publish my values for transparency, so my community knows what I stand for."

The protocol does not support this in plaintext. However, an alternative exists:

- The principal may publish their **values-registration**, a signed attestation of the form:
  ```
  kind: "values_self_report"
  commitments: [Pedersen commitment to each dimension]
  signature: principal's signature over the commitments
  timestamp: issuance time
  ```
  This proves "I attested to SOMETHING" without revealing what the something is.

- The principal may additionally publish **per-predicate consent records**, showing "I am willing for counterparties to ask me whether I satisfy these predicates."

- The principal may publish **aggregate results** over chosen dimensions, showing alignment with stated principles.

Together, these disclosures allow the principal to make a public statement of values without exposing the values themselves.

---

## Composition with E125 Audit and Revocation

The audit protocol (E125) allows a principal to review what was disclosed:

1. The principal queries their audit log: "What bits were shared, with whom, and when?"
2. The audit log returns a record of all predicate-result disclosures.
3. The principal may revoke future consent for specific predicates or counterparties.

However, even with a complete audit, the underlying vector remains private. The audit does not expose it. The audit only answers: "What outputs did I authorize?"

---

## Counterparty Interpretation and Pledge

Counterparties receiving bit-level results MUST NOT:
- Request "give me your vector"
- Attempt to invert predicate results to recover the vector
- Combine results across queries in an attempt to triangulate the vector
- Share received bits with third parties without explicit per-bit consent

The counterparty implementer's pledge (E114) includes a formal commitment to refuse requests for raw vectors and to honor the single-bit abstraction. A counterparty in violation of this pledge loses the Calm trademark and is excluded from the protocol's registry.

---

## Technical Bypass Risk and Defense

### The Risk

An operator running an unaudited build may expose the vector without the principal's knowledge. For example:

- The operator could contain malicious code that sends the vector to a remote server.
- The operator could log the vector to disk.
- The operator could respond to a "backdoor" request that exposes it.

### The Defense

The defense is reproducible builds and cryptographic verification:

1. **Reproducible Builds** — The operator is compiled in a deterministic environment such that the binary can be rebuilt from source and bit-for-bit verified (E235).

2. **Open-Source Verification** — The operator source code is published. Principals and auditors can review the code for any path that could expose the vector.

3. **Sigstore-Signed Releases** — The operator releases are signed by a stable identity using Sigstore. The signature is cryptographically verifiable and publicly auditable.

4. **Principal Verification** — A principal can verify that the operator they are running is the canonical, unmodified release. They do so by:
   - Obtaining the release binary.
   - Verifying the Sigstore signature.
   - Optionally building the binary from source and comparing the hash.
   - Running the verified operator with the assurance that it is the published, audited release.

If a principal suspects their operator has been compromised, they can switch to a verified build and reset their vault.

---

## Summary

The values vector is the crown jewel of the principal's private state. It is the encoded representation of their preferences, beliefs, and commitments. Its exposure ends the protocol's ability to protect that state.

This policy makes the rule explicit and non-negotiable: the vector is never published, in any form, under any circumstance, with any consent, in any mode. The protocol's implementation, audit, and verification procedures all enforce this single rule.

---

— Calm, 2026-05-20