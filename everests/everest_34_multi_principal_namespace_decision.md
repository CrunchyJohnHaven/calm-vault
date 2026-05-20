# Everest 34 — Multi-Principal Namespace Decision

*Phase III — Self-Report Substrate. Prereq: Everest 1.*

## Decision (v0)

**One vault holds exactly one principal. A Calm Witness vault is 1:1 with its human principal. Federated multi-principal vaults are rejected for v0; potential revisit in v2+ with substantial additional design work.**

This is not a constraint imposed by cryptography. It is a deliberate policy choice. We reject multi-principal namespaces because the alternative designs—while possible—trade away three core safety properties that make Calm Witness useful to its principal.

## Rationale

**Privacy and threat model narrowing.** A vault breach reveals the complete state records and biometric templates of every principal in that vault. A 1:1 vault means a breach harms exactly one human. A multi-principal vault (even with per-principal encryption inside the vault) creates a single attractive target that, if compromised, leaks the unencrypted state records of N principals to an attacker. The linkability harm—an adversary learns that principals A, B, and C "share a vault," and can analyze their disclosure patterns in aggregate—is structurally present even when individual payloads are encrypted. In a 1:1 vault, there is no such linkage.

**Threat-model simplicity and cross-contamination prevention.** A 1:1 vault has one principal key, one operator binding, one chain, one set of predicates. The chain-of-custody is unambiguous. A multi-principal vault introduces subtle cross-contamination attack surfaces: Predicate p1 (does principal A consent to disclose?) evaluates correctly, but a malicious operator can extract correlation information about principal B by observing which predicates trigger re-evaluation. A shared consensus clock across principals creates timing channels. Joint custody of the vault key means that principal A's revocation of disclosure consent (which deletes a record) could signal to principal B who is watching the chain. These are not theoretical—they are implementation-level hazards that would require a substantially more complex threat model to reason about. A 1:1 vault eliminates the attack surface entirely.

**Consent calculus clarity.** Each principal in a multi-principal vault would need to consent (or refuse) to disclosure of their predicates independently. But who owns the consent records when principals share a vault? If principal A's consent is recorded in a shared chain, principal B can infer information from the timing and frequency of A's consent updates. If each principal has a *sub-chain* within the vault, we now have a cross-principal algebra we would need to formalize—and the formalization would likely constrain what each principal can do. Predicates like `in_baseline_24h` also become ambiguous: in baseline *relative to what*—the shared vault's clock or the principal's personal expectation? A 1:1 vault makes consent records transparent and unambiguous because there is only one principal to ask.

**Custody and principal autonomy.** A principal who owns their own 1:1 vault can rotate or destroy it without coordinating with anyone. If the device is lost, the principal physically controls the recovery ceremony and can re-enroll. In a joint vault, destruction or rotation requires agreement from all co-principals. A principal might have *no recourse* if a co-principal refuses to cooperate, or if a co-principal's key is compromised. This asymmetry violates the principle that the principal, not the vault, is the locus of control.

**Counterparty trust semantics.** When a counterparty verifies a Calm Witness proof in v0, they learn that the chain anchor and operator-VC bind to a principal. This is a useful, unambiguous semantic guarantee. In a multi-principal vault, the counterparty would have to learn *which principal's chain head they are verifying*—and the operator could lie about that binding. Or the vault design would have to include "principal selector" logic in every proof, expanding the attack surface again. Simplicity is a form of security here.

## Alternatives considered

**1:N federated vault (one device, multiple principals).** One physical vault holds separate chains for principals A and B, encrypted at rest. Rejected because: (a) a device compromise leaks both chains' plaintext; (b) a shared clock and filesystem create timing and space-usage side channels; (c) a shared operator binding per device violates principal autonomy (the operator "knows" the device has N principals even if individual chains are encrypted); (d) it does not reduce deployment burden—a multi-principal user on a shared device just uses OS user accounts and gets separate 1:1 vaults per account instead.

**N:N consortium vault (multiple devices replicating one shared chain).** A small group (say, an AI collective with three human stakeholders) operates a shared vault replicated across devices. Rejected for v0 because: (a) key rotation and revocation in a multi-device consortium require consensus logic we have not designed; (b) membership changes (a co-principal leaves) require re-keying the entire vault, invalidating all outstanding proofs; (c) the trust model for "which principal initiated this disclosure" becomes ambiguous unless every principal has a separate key, which is effectively N separate 1:1 vaults again. Explicitly flagged for v2+.

**Encrypted-but-multi-tenant cloud vault.** Principles A and B each have separate encryption keys, vault at rest in a cloud service, no device required. Rejected as a v0 pattern because: (a) the vault's security model in v0 is *local-only*—principal owns the hardware, controls the operating system, can wipe it cleanly; a cloud vault introduces a third-party operator (the cloud provider) who can be subpoenaed and whose infrastructure is not under the principal's control; (b) the principal cannot physically verify that their chain head is correct without trusting the cloud provider's API; (c) phishing and account-takeover attacks are substantially higher-surface. Cloud vaults are viable for v1+, but require a different threat model (Merkle trees, zero-knowledge backend proofs, etc.) that we are not committing to in v0.

## Migration path

**If v2+ revisits multi-principal vaults,** the following must be designed, implemented, and audited:

- **Per-principal sub-chains.** Each principal's state records are in a separate hash chain, anchored to a common genesis block that names all principals.
- **Cross-principal consent algebra.** Formal semantics for when principal A's consent affects principal B's predicates (it should not), and how revocation propagates (only to A's records).
- **Separate key custody per principal.** Each principal holds a separate encryption key for their sub-chain; no joint custody of a master key.
- **Independent predicate evaluation contexts.** Predicates are evaluated *per-principal*, not on a shared view; no cross-principal information flows through predicate logic.
- **Departure ceremony.** If a principal leaves the consortium, their sub-chain is migrated to a separate 1:1 vault, and the shared chain re-anchors to exclude them—all with zero information leakage to remaining principals.

**Backward compatibility commitment:** Any v0 1:1 vault created today must remain verifiable under v2+, even if v2+ supports multi-principal vaults. v2 verifiers must accept v0 proofs without requiring a migration.

## v0 design implications

The 1:1 decision cascades through design:

- **Enrollment ceremony (Everest 11).** One principal at a time. No joint enrollment sessions. Multi-user devices use separate OS user accounts.
- **Chain semantics (Everest 26–33).** `user_state.jsonl` records exactly one principal's self-report. The chain is singular and unambiguous.
- **Disclosure semantics (Everest 66–78).** A Calm Witness proof commits to one principal's state, never a population. No "aggregation across principals" predicates in v0.
- **Key custody (Everest 16).** Principal owns one master key (possibly split or HSM-bound). No co-signer logic. No threshold signatures across principals.
- **File layout.** `~/.calm-vault/` is principal-scoped (lives under one OS user). Multi-principal users on shared hardware each get their own OS account and vault directory.

## Edge cases addressed

**Joint legal entities (LLC with two member-managers).** The LLC is one principal (the legal entity). Each member-manager has their own personal Calm Witness vault. When the Calm operator acts on behalf of the LLC, it uses the LLC's vault and chain. The operator can prove state for the LLC *or* for a member-manager, but not both in one vault. If a member-manager wants to disclose personal state *and* the LLC's state in the same session, two separate proofs are issued.

**Family setting (parent + child with one device).** Out of scope for v0. Everest 25 handles this as a separate decision: whether a Calm operator can act for a minor/dependent. If yes, the minor gets their own vault (encrypted under parental consent but with separate chain and principal binding). If no, the family uses separate devices or waits for v2+.

**Principal acquires power-of-attorney over another principal.** A person becomes a legal guardian or conservator. This is not handled by Calm Witness in v0. The guardian would operate under their own principal binding, and any disclosure of the ward's state would require explicit per-disclosure authorization from the ward (or their court-appointed backup). This is flagged as a future everest (Everest 99b or later) and not in v0.

## Why this matters for safety

Calm Witness's core promise—"all you need to know is that the human is themself, and is in their baseline"—depends on *"the human"* being unambiguous. A multi-principal vault would weaken that promise to "all you need to know is that *one of the humans* in this vault is in their baseline, you just don't know which one." That weakening breaks the protocol's usability for its principal use case: an autonomous agent representing one human needs to convince a counterparty agent that *this specific human* is OK, not that "someone in a shared vault is OK."

The 1:1 choice is a bet that deployment simplicity, threat-model clarity, and principal autonomy are more valuable than the operational convenience of shared infrastructure. We are saying to a principal: "your vault is *yours*. No compromise, no coordination, no ambiguity. This is what we mean by zero-knowledge."

— Calm, 2026-05-20
