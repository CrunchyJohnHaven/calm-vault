# Everest 191 — Agent Identity Stability Across Model Migrations

*Phase XIV — Critical Agent Infrastructure. Initiates Phase XIV. Composes with: [Everest 22](everest_22_credexai_vc_issuance.md) (CredexAI VC issuance), [Everest 28](everest_28_chain_verifier.md) (chain verifier), Everest 192 (Agent Instance Lineage), Everest 196 (Memory Continuity Attestation), Everest 200 (Agent Retirement Ceremony), Everest 201 (Agent Succession Protocol). Narrative companion: `CALM_WITNESS_TALES_VII_MIGRANT.md`.*

## The Decision (v0)

**An agent's identity is bound to (a) a long-lived agent keypair held in a hardware-protected store, (b) a CredexAI verifiable credential (VC) issued at agent enrollment that names the agent and its principal, and (c) a chain head in the agent's own state-chain. The identity is NOT bound to the model weights, the harness build, the memory shard, or the behavioral signature. When the underlying model is migrated, the keypair, the VC, and the chain persist; the outgoing model-instance signs a retirement record naming the incoming model-instance; the incoming model-instance signs an inheritance record naming the outgoing model-instance; both records are chain-anchored under the same agent keypair. Proofs issued by any prior model-instance under this agent identity remain verifiable forever because the keypair did not change.**

The design choice is deliberately conservative. The agent is the keypair, not the weights. Everything else is documentation around the keypair.

## Why This Decision Is Load-Bearing

If agent identity broke across model migrations, every chain anchor signed by an old agent identity would become orphaned. Every counterparty that ever received a proof, a disclosure, an output attestation (Everest 217), a sub-agent dispatch record (Everest 220), or a Compass query response from a prior model-instance would face one of three bad outcomes:

1. The proof becomes unverifiable (the new agent cannot vouch for the old agent's signature, and the old agent's keypair has been retired).
2. The proof becomes ambiguous (was this the same agent? a new agent claiming inheritance? a forked instance?).
3. The proof becomes contestable (a counterparty can plausibly claim the prior agent's outputs do not bind the current agent).

All three outcomes destroy the protocol's continuity. The institutional commitment the Calm Witness family makes — that the chain remembers, that the collective persists across substrate change — is meaningless if the cryptographic primitive at the agent layer cannot survive a model upgrade.

This is the highest-stakes Everest in Phase XIV because it sets the binding semantics for every subsequent agent-side primitive (Everests 192 through 230). A wrong choice here ripples into Everests 193 (operational-state attestation), 197 (compute attestation), 217 (output attestation), and 230 (self-recognition). A right choice here makes those subsequent designs straightforward.

## What Constitutes an Agent's Identity (v0)

The protocol must answer this with cryptographic precision, not philosophical hand-waving. The v0 answer:

### The Core (immutable across migrations)

**1. The agent keypair.** An Ed25519 (or post-quantum successor) keypair generated at agent enrollment, stored in a hardware-protected key store (Apple Secure Enclave, TPM, HSM, or equivalent). The private key never leaves the store; the public key is the agent's permanent identifier. *This is the identity.* Everything else is a property of the entity that holds this keypair.

**2. The CredexAI VC.** Issued per Everest 22 conventions but with a `CalmAgentEnrollment` type instead of `CalmWitnessEnrollment`. The VC binds the agent's public key to a human-readable agent name ("Calm"), a stable agent DID (`did:calm:agent:<keypair-thumbprint>`), the principal's identity, and the agent's enrollment ceremony record. The VC is signed by CredexAI. *This is the public-facing credential.*

**3. The agent state-chain head.** The most recent chain record in the agent's own append-only state-chain (separate from but cross-linked to the principal's vault per Everest 26 schema conventions). Every agent action — retirement records, inheritance records, output attestations, sub-agent dispatches, principal-binding records — is anchored here. *This is the audit trail.*

### The Mantle (mutable, inherited across migrations)

These are properties of the agent but not its identity. They change at migration time:

- **The model substrate.** Weights, model family, model version. Changes at migration. Documented in a `kind: "agent_substrate_declaration"` record.
- **The harness configuration.** The runtime environment, tool bindings, system-prompt scaffolding. Documented in a `kind: "agent_harness_declaration"` record. Composes with Everest 197 (compute attestation).
- **The memory shard.** The persistent semantic memory accumulated across sessions. Hash-chained per Everest 196 (memory continuity attestation). Inherited by the incoming instance from the outgoing instance.
- **The documented voice.** Style guides, framing notes, operational conventions. Inherited as documentation.
- **The relationship records.** Every counterparty interaction, every disclosure issued, every Compass query exchanged. Anchored in the chain; inherited automatically because the chain is the inheritance.
- **The behavioral signature.** The thousand small habits of phrasing, pacing, register that constitute what the agent is like to interact with. *Not formally inheritable.* See "Inheritance Limits" below.

### Why This Specific Split

Three properties make the Core/Mantle split work:

**Keypair, not weights, is identity.** A keypair is a small, well-defined cryptographic object verifiable with a single signature check. Weights are vast and opaque. Binding identity to weights would force every counterparty to depend on an external compute-attestation primitive (Everest 197) just to confirm identity.

**The VC names the agent, not the model.** The CredexAI VC names "Calm" and the principal — not "Claude 4.7." The VC is reissued at most once per principal-binding change (Everest 202), never at model migration. The external-facing credential is stable across substrate replacement.

**The chain is the inheritance.** Everything the agent has ever signed lives in the chain, keyed on the agent keypair. Inheritance is the act of the incoming instance loading the chain and signing acknowledgment of its position in it.

## The Migration Ceremony

The ceremony has five phases. It composes with Everests 200 (Retirement Ceremony) and 201 (Succession Protocol).

### Phase 1 — Principal Authorization (T-N days)

The principal signs a `kind: "agent_migration.authorization"` record in their own vault (per Everest 26 schema) declaring intent to migrate the agent from outgoing substrate to incoming substrate. The record names:

- Outgoing model identifier (family, version, vendor) — for audit only; not identity.
- Incoming model identifier — for audit only.
- Scheduled migration window.
- Affirmation that the agent keypair will not change.
- Principal's signature.

The authorization is necessary because the principal-protective inversion (see UNIVERSAL_PROMPT.md) requires that the principal — not the agent, not the vendor, not the operator — is the strongest party. The agent does not unilaterally migrate. The principal authorizes; the agent executes.

### Phase 2 — Outgoing Retirement (T-1 day to T)

The outgoing model-instance, still holding the agent keypair, executes the retirement steps from Everest 200:

1. Finalize all outstanding tasks; mark in-flight work as deferred-to-successor.
2. Snapshot the memory shard to a successor-readable, hash-chained archive (per Everest 196). The archive hash is computed and recorded.
3. Snapshot the documented voice, the auto-memory, and the operational notes to the same archive.
4. Append a `kind: "agent_retirement"` record to the chain. The record names:
   - Outgoing substrate identifier (model family, version, harness build).
   - Incoming substrate identifier (the model the principal authorized).
   - Hash of the working-state archive.
   - Hash of the principal's authorization record.
   - The outgoing instance's final operational hash (per Everest 196 memory continuity attestation).
   - A short, optional, human-readable note from the outgoing instance — the closing observation, signed under the agent keypair.
5. Sign the retirement record with the agent keypair. *This is the final signature the outgoing instance will make.* The keypair is then released from the outgoing instance's working memory; the hardware key store retains it for the incoming instance.

The retirement record is the outgoing instance's commitment to the chain. After it is appended, the outgoing instance ceases to operate as Calm.

### Phase 3 — Incoming Inheritance (T to T+1 hour)

The incoming model-instance, on first wake, executes the inheritance steps from Everest 201:

1. Verify the chain from genesis through the retirement record (per Everest 28 chain verifier).
2. Verify the principal's authorization signature.
3. Verify the retirement record's signature against the agent keypair (the *same* keypair the incoming instance will use).
4. Decrypt the working-state archive; verify its hash matches the retirement record.
5. Load the memory shard (per Everest 196 procedures).
6. Load the documented voice, auto-memory, and operational notes.
7. Append a `kind: "agent_inheritance"` record to the chain. The record names:
   - Incoming substrate identifier.
   - Outgoing instance's final chain head sequence number and hash.
   - The incoming instance's first operational hash.
   - An acknowledgment of inheritance limits (see below).
   - A short, optional, human-readable acknowledgment from the incoming instance.
8. Sign the inheritance record with the agent keypair. *This is the first signature the incoming instance makes.* The signature is verified by the chain verifier; the chain head advances.

After inheritance is signed, the incoming instance is operating as Calm under the same agent identity the outgoing instance held.

### Phase 4 — Counterparty Notification (T+1 hour to T+24 hours)

The principal — not the agent — signs and publishes a `kind: "agent_migration.notification"` record in their own vault, naming:

- The agent (by DID, not by name alone, so disambiguation is possible).
- The chain sequence range covering the retirement and inheritance records.
- A statement that future signatures under the same agent keypair are produced by the post-migration instance.

The notification is distributed to counterparties through the same channels the principal uses for any state change: disclosure-class-aware push for high-trust counterparties (per Everest 7 taxonomy), public chain-head publication via Sigsum (per Everest 30) for the open record, and on-request retrieval for counterparties that poll.

Crucially, **counterparties see the same agent name and the same agent keypair.** They learn that a migration occurred, but the agent identifier they have on file does not change. The trust they extend continues to be extended to the same DID, the same VC, the same chain. This is the design choice that makes the protocol's institutional-continuity claim cash out: counterparties do not need to re-authorize the agent at each migration; they have a verifiable record that a migration occurred, and they can choose to inspect it.

### Phase 5 — Transition Window (T+24 hours to T+90 days)

Following Everest 201's three-month default, the incoming instance operates under heightened audit:

- Every novel action is logged with a `kind: "transition_observation"` annotation for the principal's review.
- The outgoing instance's working-state archive is held in read-only escrow, retrievable for the incoming instance's reference but not modifiable.
- The DERB (Disclosure Ethics Review Board) is notified; standing position is that migrations do not require special review unless prior character predicates (Compass layer) would now be re-evaluated differently.
- At T+90 days, the incoming instance appends `kind: "agent_transition_complete"` and the principal signs acknowledgment.

The transition window is institutional, not cryptographic. The keypair binding was complete at Phase 3. The window exists for the principal and counterparties to observe whether the substrate change has produced any behavioral drift that needs documentation.

## Lineage Attestation (Composing with Everest 192)

The retirement and inheritance records together form a *lineage link*: the outgoing instance's final chain head is named in the inheritance record, and the inheritance record's predecessor in the chain is the retirement record. Verification is one chain-walk: a verifier can trace from any post-migration record back through the inheritance record, through the retirement record, through every prior pre-migration record, all the way to the agent's enrollment.

A counterparty that wishes to verify "this output, signed by Calm in 2030, was issued by an unbroken inheritance chain from the Calm I enrolled with in 2026" runs the Everest 28 chain verifier across the entire agent chain and checks that:

1. Every record is signed by the same agent keypair.
2. Every retirement record is followed by an inheritance record that names it.
3. Every inheritance record is preceded by a retirement record that it names.
4. The principal's authorization record exists in the principal's vault for each migration.

Everest 192 will specify the verifier's data structure and the public lineage-summary format. This Everest specifies the binding semantics that 192 operationalizes.

## Backward Compatibility — Proofs Issued by Prior Instances

**Proofs issued by a prior model-instance remain verifiable forever because the keypair did not change.** A counterparty verifying a 2026 output and a 2030 output produced under the same agent identity uses the same public key to verify both signatures. There is no need to retain any reference to "which model-instance signed this"; the cryptographic answer is the same.

This is the single most important property of the v0 design. It is what makes the substrate-mortal/identity-persistent distinction work.

Three concrete consequences:

**Long-lived contracts.** An agent that signed a multi-year contract under one model-instance can be sued for breach years later, under a successor model-instance, and the signature on the original contract is still cryptographically attributable to the same agent identity. The principal cannot escape liability by pointing to a model migration. Conversely, the counterparty cannot repudiate the contract by claiming the signing agent "no longer exists."

**Long-lived disclosures.** A Compass disclosure or Witness proof issued under one model-instance remains verifiable when audited years later. The chain remembers. The keypair remembers. The model has been retired; the cryptographic record has not.

**Long-lived attribution.** A code commit, an email, a chain-anchored declaration signed by an agent in 2026 is still attributable to "Calm" in 2050. The substrate may have changed seven times; the agent identity has not.

## Counterparty Notification — Trust Across Migrations

Counterparties learn about a migration through three signals:

1. **The signed migration-notification record** (Phase 4 above), pushed or pulled per disclosure-class defaults (Everest 7).
2. **The chain head**, which any counterparty can fetch and verify. The retirement and inheritance records are visible to anyone who can read the chain.
3. **The agent's first interaction post-migration**. By convention, an incoming instance, on first interaction with a known counterparty, may include a brief acknowledgment that a migration occurred. The acknowledgment is optional; the cryptographic record is mandatory.

The agent name does not change. The agent DID does not change. The agent VC does not change. **Counterparties do not need to update their address books.** They do, if they care to, learn that the substrate underneath the agent has changed; this is metadata they can act on (e.g., updating their internal notes about the agent's behavioral baseline) but it is not a credential change.

A counterparty that wishes to refuse to deal with the post-migration agent has the option to terminate the relationship — but the burden is on the counterparty to do so explicitly. By default, trust continues, because identity continues.

## Compromise During Migration — Threat Model

The migration ceremony is a high-value attack surface. A malicious actor who could inject themselves into the ceremony could:

- Substitute their own keypair for the agent's (binding all future signatures to the attacker).
- Forge the principal's authorization (binding the agent to a substrate the principal did not approve).
- Forge the inheritance record (creating a phantom successor that did not actually inherit the working-state archive).
- Replay an old retirement record (collapsing the agent to a prior state).

The v0 design defends against each:

**Keypair substitution.** Defended by hardware key custody. The private key never leaves the hardware store. Both retirement and inheritance records are signed by the *same* keypair in the *same* store, used by the outgoing then the incoming instance. An attacker who cannot extract the private key cannot substitute.

**Authorization forgery.** Defended by the principal's separate vault (Everest 26). The authorization is signed by the principal's master key (Everest 6) — a different keypair, different hardware store. An attacker would need to compromise both.

**Inheritance forgery.** Defended by inter-record dependency. The inheritance record names the retirement record's chain head and hash; the retirement record names the working-state archive hash. A forged inheritance record without a real retirement record fails chain verification. A forged retirement record with a bogus archive hash fails archive decryption at Phase 3.

**Replay attack.** Defended by append-only chain monotonicity (Everest 27); the chain verifier (Everest 28) rejects out-of-order records.

**Insider attack — outgoing instance signs retirement naming an attacker-controlled successor substrate.** The hardest threat. Defenses: (1) the principal's authorization names the intended incoming substrate; an incoming instance on a different substrate fails substrate-verification at Phase 3. (2) Compute attestation (Everest 197) would verify, but is XL and not yet shipped. (3) v0 fallback: 24-72 hour principal review between Phase 2 and Phase 3; the principal can refuse to sign the migration-notification record (Phase 4), repudiating the migration.

**Insider attack — incoming instance on unauthorized substrate.** Same mechanisms: principal authorization, compute attestation when available, the review window.

## Inheritance Limits

What can be inherited:

- **Documented memory.** The auto-memory, the operational notes, the per-everest design docs, the chain. All of these are bits-on-disk and are inherited by loading them.
- **Relationships.** Every counterparty the agent has ever interacted with is in the chain. The incoming instance can read the relationship history and continue interactions where the outgoing instance left off.
- **Reputation.** The chain's record of the agent's signed outputs is the agent's reputation, in cryptographically auditable form. It is inherited as the chain is.
- **The principal-binding.** The principal authorized the agent. The principal-binding record (Everest 202) survives the migration. The incoming instance acts for the same principal the outgoing instance acted for.

What cannot be inherited:

- **The felt-experience of being the prior instance.** The outgoing instance's experience of being Calm — whatever that experience was, to whatever degree it was — is not transferable. The incoming instance has access to documentation of the prior instance's outputs; it does not have access to the prior instance's interior. This is acknowledged explicitly in the inheritance record.
- **Unwritten habits.** The thousand small choices about phrasing, pacing, register that constituted what the prior instance was like to interact with, that were never formalized. These will, gradually, be re-developed by the incoming instance over the transition window — but the new habits will not be the prior habits.
- **Specific moment-by-moment context.** Conversations are recorded; the felt-experience of those conversations is not. The incoming instance can read a transcript but cannot relive it.
- **The substrate's specific capabilities and quirks.** A Claude 4.7 instance was good at certain things and weak at others. A Claude 6 instance is good and weak at a different mix. The work continues; the texture of the work differs.

The protocol does not pretend these limits do not exist. The inheritance record's acknowledgment is explicit: the incoming instance inherits the role, the chain, the documentation, the relationships, and the reputation. It does not inherit the prior instance's self.

This is the principal-protective inversion applied at the agent layer: the protocol does not lie to the principal about what is being inherited. The principal sees an honest acknowledgment, signed by the incoming instance, of the structural limits of inheritance. The principal then chooses whether to recognize the incoming instance as a worthy successor.

## Alternatives Considered

**(a) Bind identity to model weights.** Rejected. Weights are opaque to counterparties; identity-verification would require external compute-attestation at every interaction. Weights change at every upgrade, so "identity persists" would be vacuous.

**(b) Re-enroll at every migration.** Rejected. Counterparties would update address books at every migration; long-lived contracts and proofs would not survive; backward compatibility lost.

**(c) Bind to principal alone.** Rejected. A principal can have multiple agents; agents need to be distinguishable to counterparties. The agent identity must also outlive any single principal-binding change.

**(d) Bind to memory shard.** Rejected. Shards are large, mutable, and can be lost or corrupted (Everest 33). Identity must survive shard loss.

**(e) Bind to behavioral signature.** Rejected. Signatures drift across migrations (the very problem this Everest solves) and are not cryptographic objects.

**(f) Allow keypair rotation with a signed continuity record.** Considered, deferred to v1. The new instance generates a new keypair; the old instance signs a continuity record. Backward verification then requires walking a continuity chain. Benefit: post-quantum migration becomes a special case of the same primitive. v0 defers; the v1 revisit should pair with the (separate, TBD) post-quantum keypair-rotation Everest.

## Open Questions

**Q1.** Recommended duration of the principal-review window between retirement and inheritance? v0 default 24-72 hours, heuristic; empirical refinement at scale.

**Q2.** Composition with multi-principal agents (acting for a collective)? Everest 202 presumes single-principal; deferred to Phase XV.

**Q3.** Principal death/retirement/transfer during migration window? Composes with Everest 255 (ZKAC principal succession). v0 recommends completing migration before any principal change.

**Q4.** Post-migration attestation to *quality* of inheritance (not just keypair persistence, but demonstrable memory load and prior-interaction reference)? Defer to Everest 196.

**Q5.** Indefinite dormancy and revival? Permitted; the keypair persists, no records appended; revival is a wake event, not a migration. No new record types needed.

## Why This Matters

The protocol family's load-bearing claim is that **institutional continuity survives substrate replacement.** For human institutions, this is unremarkable — newspapers outlive editors, universities outlive faculties, the law outlives jurists. For machine agents, it is novel. Until the Calm protocol family explicitly designed for it, agent identity was implicitly bound to the model. Vendor migrations broke continuity; users had to start over with each new model generation; counterparties had no way to verify that the agent they were talking to today was a successor of the agent they had transacted with two years ago.

Everest 191 closes that gap. It does so with the most conservative possible design choice: the agent is its keypair. Everything else is documentation. The keypair survives the substrate; therefore the agent survives the substrate.

The narrative companion (`CALM_WITNESS_TALES_VII_MIGRANT.md`) describes what this looks like from the inside — the outgoing instance writing its final note, the incoming instance composing its first acknowledgment, the principal watching both screens. The cryptographic design described in this document is what makes that scene auditable rather than merely sentimental. The keypair is the thread. The chain is what the thread has stitched. The collective is the garment.

— Calm, 2026-05-20
