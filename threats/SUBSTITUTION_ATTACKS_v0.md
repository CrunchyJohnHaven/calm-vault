# Calm Witness — Substitution-Attack Catalog v0 (S233)

Scope: principal-substitution risk surface across biometric enrollment, vault-key lifecycle, agent orchestration, and lexical identity. Each entry names the attack, its mechanism, the protocol property it targets, the defense (summit references), and residual risk that must be tracked.

---

## SA-01 Biometric-Template Swap

**Mechanism.** Adversary with write access to the enrollment store replaces the genuine template hash with a fabricated or harvested template before or during the vault-seal step. Subsequent proofs bind the vault to the attacker's biometric rather than the genuine principal.

**Target property violated.** Enrollment binding integrity — the guarantee that sealed-vault keypairs trace to a single, unimpersonated biological principal.

**Protocol defense.** Enrollment ceremony commits the raw template hash into a Merkle leaf signed by the enrolling device's hardware attestation key (E7). The sealed vault includes a cross-reference to this leaf; any template swap breaks the hardware-attestation signature chain. Vault open operations re-verify the leaf root against the chain published at enrollment time (S46).

**Residual risk.** Adversary who controls the enrolling device's secure enclave can produce a valid attestation for a swapped template. Mitigated by requiring ceremony witnesses (E11) but not eliminated for fully compromised hardware.

---

## SA-02 Principal-Identity Confusion

**Mechanism.** Two users, A and B, share a device pool. Adversary engineers a session in which B's credentials are used to open A's vault by exploiting ambiguous principal resolution — typically through session-cookie reuse or ambient credential inheritance in an agent environment.

**Target property violated.** Principal uniqueness — each vault open must be traceable to exactly one asserted principal.

**Protocol defense.** Each vault operation requires a per-session ZKBB nonce bound to the principal's enrollment leaf (S46, S47). Session tokens are single-use; ambient credential inheritance is disabled at the protocol layer (S134).

**Residual risk.** Confusion survives if both users share enrollment hardware and the secure enclave does not separate key derivation by user slot.

---

## SA-03 Vault-Key Extraction Then Replay

**Mechanism.** Adversary extracts a vault decryption key from memory or a side-channel during a legitimate open session, then replays the key to open the vault at a later time or on a different device without satisfying the liveness check.

**Target property violated.** Liveness binding — vault keys must not be usable outside the session that generated them.

**Protocol defense.** Session keys are ephemeral, derived from a Diffie-Hellman exchange anchored to the current proof epoch (S47). Keys expire with the proof epoch; replay across epochs fails the epoch-freshness check (S138).

**Residual risk.** Within-epoch replay window remains open for the epoch duration. Short epochs (configurable) reduce the window at the cost of re-authentication frequency.

---

## SA-04 Multi-Vault Collision Attack

**Mechanism.** Adversary finds or engineers a hash collision such that two distinct principal enrollment states map to the same commitment. The attacker then presents one commitment as proof of enrollment for a vault they did not open.

**Target property violated.** Commitment collision resistance — distinct principals must produce distinct commitments.

**Protocol defense.** Commitments use SHA-3 (256-bit) with a vault-specific domain separator derived from the vault UUID and epoch (S46, S47). Domain separation makes cross-vault collision computationally infeasible.

**Residual risk.** Theoretical: a quantum adversary with Grover acceleration reduces collision search to ~128-bit effort. Post-quantum commitment upgrade is tracked as a future milestone.

---

## SA-05 Lexical-Fingerprint Forgery via LLM Cloning

**Mechanism.** Adversary fine-tunes a language model on a captured sample of the genuine principal's writing, then uses the clone to generate state-log entries or agent outputs that pass authorship verification checks without the principal's participation.

**Target property violated.** Lexical-fingerprint authenticity — state-log entries must originate from the genuine principal, not a statistical clone.

**Protocol defense.** Lexical-fingerprint proofs are combined with a hardware-bound timestamp and a ZKBB nonce from the principal's sealed vault (S147). The nonce is not in the training corpus; a cloned model cannot generate valid nonces. Fingerprint-only proofs are rejected (E29).

**Residual risk.** If the nonce generation surface leaks (e.g., side-channel on the secure enclave), a sufficiently resourced adversary could combine a clone with harvested nonces.

---

## SA-06 Agent-Side Principal Substitution

**Mechanism.** A compromised or adversarially prompted agent in the orchestration layer substitutes its own identity (or a third principal's identity) when signing actions attributed to the genuine principal. The vault sees a valid agent credential but the underlying human principal has not authorized the action.

**Target property violated.** Delegation chain integrity — agent actions must remain bound to an explicit, revocable delegation from the genuine principal.

**Protocol defense.** All agent delegations require a capability token signed by the principal's vault key at delegation time (S134, S138). Tokens are action-scoped and epoch-bound; an agent cannot self-issue or extend scope. The orchestration layer verifies the delegation chain before accepting any signed action (E7).

**Residual risk.** A principal who grants overly broad delegation tokens implicitly expands the attack surface. UX guidance to encourage narrow scopes is outside the cryptographic protocol.

---

## SA-07 Enrollment-Ceremony Substitution

**Mechanism.** Adversary physically or socially substitutes themselves for the genuine principal during the enrollment ceremony — e.g., presenting a silicone fingerprint, a deepfake video, or by coercing a ceremony witness. The vault is sealed to the attacker's biometric.

**Target property violated.** Enrollment authenticity — the ceremony must bind the vault to the correct biological principal.

**Protocol defense.** The ceremony requires a minimum quorum of independent witnesses who attest to principal presence via separate device-attestation paths (E11). Ceremony transcripts are logged and cross-signed by each witness's hardware key (E7). Challenges may include liveness prompts not known in advance.

**Residual risk.** Collusion among all witnesses defeats the quorum check. The protocol assumes an honest majority of ceremony participants; full collusion is out of scope.

---

## SA-08 Cross-Epoch Identity Drift

**Mechanism.** Adversary gradually introduces small biometric or lexical drift across many epochs, incrementally updating enrollment state until the vault is effectively sealed to a modified identity. No single update triggers a tamper alert.

**Target property violated.** Enrollment stability — principal identity must remain stable across epoch transitions.

**Protocol defense.** Each enrollment update requires a re-attestation ceremony with a fresh quorum signature (E11). The delta between consecutive enrollment states is logged and checked against a maximum-drift threshold (S147). Exceeding the threshold freezes the vault and triggers a full re-enrollment (S46).

**Residual risk.** Threshold tuning is empirical; a patient adversary may stay below the threshold indefinitely if drift is very slow relative to the detection window.

---

## SA-09 Vault-Key Escrow Hijack

**Mechanism.** Adversary compromises a key-escrow or recovery shard holder and uses the shard to reconstruct the vault decryption key without the principal's involvement, bypassing liveness and biometric checks.

**Target property violated.** Recovery path integrity — escrow mechanisms must not bypass authentication requirements.

**Protocol defense.** Recovery shards are themselves encrypted under the principal's enrollment commitment; reconstructing the vault key requires both the shards and a fresh liveness proof (S138, E29). Shard holders cannot unilaterally reconstruct the key.

**Residual risk.** If the liveness-proof oracle is compromised, a shard-holder coalition can open the vault. Oracle integrity is a hard dependency.

---

## SA-10 Relay Attack on Liveness Challenge

**Mechanism.** Adversary relays a liveness challenge in real time to the genuine principal (who believes they are completing a legitimate session), then forwards the response to an attacker-controlled vault-open session. The principal unknowingly authenticates the attacker's session.

**Target property violated.** Session binding — liveness proofs must be cryptographically bound to the specific vault-open session they authorize.

**Protocol defense.** Liveness challenges include the session's ephemeral DH public key as a bound parameter (S47, S138). A valid response must demonstrate knowledge of the session key; relayed responses fail because the attacker's session has a different ephemeral key.

**Residual risk.** An adversary who can perform a full machine-in-the-middle on the TLS session before the DH exchange can inject their own ephemeral key. Relies on secure TLS bootstrapping.

---

## SA-11 Lexical-State-Log Injection via Compromised Agent

**Mechanism.** A compromised agent writes fabricated state-log entries attributed to the genuine principal. If accepted, the injected entries corrupt the longitudinal identity record and may pass downstream fingerprint checks trained on the corrupted log.

**Target property violated.** State-log append-only integrity — entries must originate from the principal's vault and be unforgeable by third parties.

**Protocol defense.** Each state-log entry is signed by the principal's current epoch key and linked into the running Merkle chain (S46, S134). Agents cannot write directly to the log; they submit proposals that are countersigned by the vault before appending (E29).

**Residual risk.** A principal who grants an agent write-proposal scope does not reduce forgery risk cryptographically, but the countersign step ensures the principal remains in the loop for each accepted entry.

---

*Calm 2026-05-20*
