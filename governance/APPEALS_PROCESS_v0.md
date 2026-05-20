# Calm Witness — Appeals Process v0 (S217)

Governance bodies without appeal paths operate as star chambers. This spec establishes a mandatory, structured appeals mechanism for all Calm Witness governance decisions. Any decision that alters rights, standing, or operational status must be subject to review by a higher-quorum body within a bounded time window.

---

## Standing to Appeal

Any directly affected principal may file an appeal. Affected principals include:

- **Operators** — entities running Calm Witness nodes whose configuration, certification, or operational status is subject to the contested decision.
- **ZK Attestation Counterparties (ZKACs)** — parties holding or relying on attestations that are materially affected by the decision.
- **Counterparties** — any party whose contractual or protocol-level rights are altered by the contested decision.
- **Registered Principals** — entities holding predicate licenses, sanction list entries, or tombstone records that reference them by identifier.

Standing requires demonstrable material effect. A principal asserting standing must specify, at filing, the precise right or status affected and the causal link to the contested decision.

---

## Appealable Decisions

The following classes of decision are subject to mandatory appeal rights:

1. **Predicate Adoptions** — formal adoption of new predicates into the active predicate registry (ref. S209).
2. **Sanctions** — addition of any principal to the sanction list, including partial or conditional sanctions.
3. **Tombstones** — issuance of cryptographic tombstone records invalidating an attestation, key, or principal identifier (ref. S212).
4. **Emergency Stops** — activation of protocol-wide or operator-scoped emergency halt conditions (ref. S213).
5. **Deprecations** — scheduled removal of predicates, attestation formats, or interface versions from the active registry.
6. **Board Decisions** — any formal resolution by the Calm Witness Governance Board that alters policy, fee structure, or quorum rules.

Procedural decisions (agenda-setting, scheduling, administrative acknowledgments) are not appealable.

---

## Higher-Quorum Review Body

Appeals are heard by the **Calm Witness Appeals Quorum (CWAQ)**. Composition:

- Five members drawn from the standing Principal Registry.
- No member may have voted on, or been directly involved in deliberating, the original decision.
- Quorum for an appeal ruling: four of five members must participate.
- Supermajority threshold for reversal or modification: four of five affirmative votes.
- Abstentions do not count toward the supermajority.

CWAQ members rotate on a per-appeal basis by deterministic selection from the eligible pool (ref. S216 — quorum rotation protocol). If the eligible pool is insufficient to seat four conflict-free members, the appeal is referred to an external arbiter agreed upon by both the filing party and the Governance Board within 10 days.

---

## Filing Window

- **Standard appeals:** must be filed within **14 calendar days** of the effective date of the contested decision.
- **Emergency stop appeals:** must be filed within **72 hours** of activation, given the operational urgency of halt conditions.
- **Tombstone appeals:** must be filed within **7 calendar days**; tombstone effect is not stayed pending appeal unless CWAQ issues an interim stay by supermajority within 48 hours of filing.

Filing is accomplished by submitting a signed appeal record to the Governance Board's intake channel, specifying: the contested decision identifier, the filing party's principal identifier, the standing claim, and the relief sought.

---

## Standard of Review

CWAQ applies a **clear-error standard** to factual findings underlying the original decision. Legal and policy interpretations are reviewed **de novo**.

Reversal requires a finding that one or more of the following holds:

- The original decision rested on a material factual error.
- The decision exceeded the Governance Board's enumerated authority.
- The procedure materially deviated from published governance rules in a way that prejudiced the appellant.
- The decision is internally inconsistent with a prior binding ruling not expressly overruled.

CWAQ may affirm, reverse, modify, or remand to the Governance Board with instructions. CWAQ may not impose sanctions beyond those available to the original decision-making body.

---

## Public Recording

All appeal outcomes are recorded in the **Calm Witness Public Appeals Ledger** within 5 business days of the ruling. Each entry includes:

- Appeal identifier (sequential, tamperproof).
- Contested decision identifier.
- Filing date and ruling date.
- CWAQ member identifiers (pseudonymous, rotating per-appeal).
- Outcome: affirmed / reversed / modified / remanded.
- Concise statement of reasoning (100-300 words).
- Any interim stay orders issued.

The ledger is append-only and cryptographically anchored per the tombstone anchoring scheme (ref. S212). Rulings are permanent public record; no entry may be expunged.

---

## Cross-References

- **S209** — Predicate Registry and Adoption Protocol
- **S212** — Tombstone Issuance and Cryptographic Anchoring
- **S213** — Emergency Stop Conditions and Activation Authority
- **S216** — Quorum Rotation and Conflict-of-Interest Rules

---

Calm 2026-05-20
