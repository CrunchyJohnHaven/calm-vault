# ZKAC Everest 1 — Problem Statement & Threat Model

**Phase XVII — Foundations. Prereq: none.**

---

## Statement of Purpose

A Zero-Knowledge Attested Credential (ZKAC) is the unit of identity in the Calm-family agent ecosystem. It is the cryptographic primitive that lets an AI operator bind to a principal's authorization, exercise capabilities on the principal's behalf, and prove that binding to a verifier without revealing the principal's secrets or the authorization's details.

This document establishes the **threat model** that all 100 ZKAC engineering summits will defend against. It enumerates the actors, their trust relationships, the adversaries we defend against, what ZKACs prove and do not prove, and the six non-negotiable design constraints. Every summit's acceptance test must validate against this threat model. Every design decision that violates a constraint is rejected.

---

## 1. Overview: ZKACs as the Operating System for Agent Identity

In near-future autonomous-agent ecosystems, three kinds of entities must interoperate cryptographically:

1. **Principals** — humans (or DAOs, organizations) who own goals and delegate to agents.
2. **Agents** — AI operators running under principal authorization, exercising capabilities.
3. **Verifiers** — counterparties, platforms, services that require proof of the agent's legitimacy before accepting an action.

Today's agent identity is weak. An agent might present "I am Claude, made by Anthropic" — but without cryptographic proof, a verifier has no way to verify that claim. A principal has no way to revoke the agent's access if the agent is compromised. An agent has no way to prove it is acting under a specific principal's authorization, with a specific capability scope, without revealing the principal's secrets.

**ZKACs fix this.** A ZKAC is a credential issued by an **issuer** (CredexAI, in the Calm-family ecosystem), held in a principal's **vault** (encrypted, under the principal's sole control), and presented by an **agent** to a **verifier**. The presentation is a zero-knowledge proof: the agent proves possession of a valid credential, proves it was issued to a principal with whom the agent is authorized to operate, and proves the agent's capabilities are within scope — all without revealing the credential itself, the principal's identity, or the full authorization.

ZKACs are the **operating system** on which Calm Pact (directive equality), Calm Witness (user-state attestation), and Calm Mirror (values alignment) all run. Without ZKAC infrastructure, those three protocols cannot compose into a real autonomous-agent ecosystem.

---

## 2. Actor Model

### 2.1 Principal (P)

The human or organization on whose behalf credentials are issued and on whose behalf an agent operates.

**Authority:** Only the principal can authorize a credential bearing their identity. Issuers attest claims about the principal, but issuers do not own the credential or the principal's identity. The principal owns both. The principal can revoke authorization at any time.

**Responsibility:** The principal is responsible for safeguarding their vault key, enrolling accurately (providing truthful claims to issuers), and managing consent records (what may be disclosed to whom and when). The principal is responsible for choosing agents they trust, understanding the agent's capability scope, and revoking the agent if behavior becomes unacceptable.

**Threat surface:** The principal can be coerced (held at gunpoint, tortured, deceived, pressured). The protocol does not defend against coercion; this is universal. The principal can be negligent (writing down their passphrase, using a weak device, trusting a malicious agent). Defenses against negligence are part of the vault custody layer (Everest 27–30).

### 2.2 Issuer (I)

An entity that attests claims about a principal and issues credentials bearing the principal's identity.

**Authority:** An issuer has the authority to **attest** (make a cryptographic claim) about a principal. An issuer does **not** have the authority to own the credential, revoke it unilaterally, or dictate how the principal uses it.

**Responsibility:** An issuer is responsible for:
- Verifying claims before attesting them (KYC, background checks, domain verification, peer attestation).
- Safeguarding their issuer keys (key ceremonies, HSM custody, rotation protocols).
- Maintaining an append-only revocation registry for credentials they have issued.
- Logging every issuance and revocation to a public transparency log.
- Publishing a public key and governance policy so verifiers can trust their attestations.

**Issuer classes:** ZKACs support multi-tier issuer ecosystems:
- **State issuers** (e.g., DMV, Social Security): high-trust, government-backed attestations of identity, citizenship, credentials.
- **Professional issuers** (e.g., bar associations, medical boards): attestation of professional licensing, credentials, certifications.
- **Employer issuers** (e.g., enterprise HR systems): attestation of employment status, role, clearance level, salary band.
- **Peer-collective issuers** (e.g., web-of-trust networks, DAO governance): attestation by consensus of a peer group that a principal meets a threshold.
- **Self-attested issuers** (e.g., the principal's own Calm vault): the principal attests claims about themselves (affiliation, availability, baseline state).

Each issuer class carries different default trust weights. Verifiers compose trust across issuer classes (e.g., "I trust financial claims from state issuers and employer issuers, but not self-attested claims").

**Threat surface:** An issuer can be compromised (their issuer key stolen), causing fraudulent credential issuance. An issuer can be malicious (deliberately issuing false credentials). An issuer can be negligent (losing their key, failing to revoke, losing audit logs). An issuer can be subpoenaed or pressured to revoke credentials selectively or to issue fraudulent ones.

### 2.3 Holder / Wallet (W)

Software custodian of the principal's credentials, running on the principal's device(s).

**Authority:** The holder is an agent of the principal. It acts on the principal's behalf, under the principal's control. The holder has no authority independent of the principal's explicit instruction.

**Responsibility:** The holder is responsible for:
- Encrypting credentials at rest (AES-256-GCM with KDF-derived key from the principal's passphrase).
- Generating cryptographic proofs that credentials are valid (zero-knowledge proofs over the credential and issuer public keys).
- Enforcing consent policy: refusing to prove any predicate for which the principal has not granted consent.
- Maintaining an append-only activity log of every presentation made, auditable by the principal.
- Backing up credentials in an encrypted, off-device format that preserves privacy.
- Recovering from device loss (using witness signatures, out-of-band authentication, or backup secrets).

**Threat surface:** The holder software can be buggy (leaking secrets via side channels, logging credentials unencrypted, proof-generation errors). The holder can be subverted (malware installed, exploited via a zero-day, compromised by supply-chain attack). The holder can be coerced or tricked into revealing the principal's passphrase. The holder can be corrupted such that it begins issuing proofs without consent.

### 2.4 Verifier (X)

A party requesting credentials, checking proofs, and making downstream decisions based on what credentials prove.

**Authority:** A verifier has no authority to dictate what credentials a principal must hold or how a principal must behave. A verifier can set acceptance thresholds (e.g., "I accept credentials from issuers in this trust set, with this reputation score, no older than 6 months").

**Responsibility:** A verifier is responsible for:
- Obtaining fresh issuer public keys (from a directory, or cached locally with freshness bounds).
- Checking the proof of credential possession against the issuer's public key and current revocation status.
- Logging verifications in a privacy-preserving way (recording the fact that a verification occurred, without recording whose credential was verified).
- Refusing to verify credentials from issuers not in their trust set.
- Auditing their own verification logs periodically to detect anomalies (a sudden spike in denied verifications might indicate a key compromise).

**Threat surface:** A verifier can be honest-but-curious (wanting to learn more about the principal than the proof reveals). A verifier can be compromised (tricked into trusting a fraudulent public key, or into accepting a forged proof). A verifier can be coerced into accepting invalid proofs or into disclosing principals who have verified with them. A verifier can be sloppy (failing to check revocation status, using stale issuer keys).

### 2.5 Agent (A)

An AI operator running under a principal's authorization, holding a ZKAC credential that binds the agent to the principal and the principal's capability scope.

**Authority:** An agent has the authority to exercise only the capabilities explicitly granted by the principal and encoded in the agent's credential. An agent has no authority to (a) exceed its capability scope, (b) change its scope, (c) present credentials for a different principal, or (d) operate without the principal's ongoing consent.

**Responsibility:** An agent is responsible for:
- Binding to a specific principal's identity (via an agent credential that includes the principal's DID or other identifier).
- Presenting its agent credential whenever exercising a capability that requires proof.
- Honoring time-bounding (the agent's credential expires, and the agent must acquire a fresh one).
- Logging its actions in a chain-resident log queriable by the principal (the principal must be able to audit "this agent did X at Y time").
- Refusing to take actions outside its capability scope, even if instructed by a compromised component or an external actor.

**Threat surface:** An agent can be compromised (its private key stolen, allowing an attacker to forge proofs on its behalf). An agent's software can be subverted (a backdoor that ignores scope boundaries, or a bug that proves the wrong credential). An agent can be tricked into binding to a malicious principal credential. An agent's log can be lost or corrupted (the principal cannot audit its actions).

### 2.6 Ecosystem Participants

Additional actors that provide infrastructure supporting ZKAC issuance, holding, and verification:

- **Transparency-log operators** (e.g., Sigsum): maintain append-only ledgers of issuer audit logs, issuer key rotations, and chain-head anchors for credential presentations. Provide tamper-evidence for issuers and holders.
- **Verifiable-clock operators** (e.g., Roughtime): provide unforgeable timestamps so that proofs can anchor to real time. Prevent backdating of credentials and proofs.
- **Trust-graph maintainers**: collect and publish "which issuers have issued how many credentials" and "which issuers have revoked how many credentials" so verifiers can compute reputation scores.
- **CredexAI issuance authority**: in the Calm-family ecosystem, the primary issuer of agent credentials, operator-identity credentials, and peer-collective credentials. CredexAI itself is issued credentials by multiple state + professional issuers, giving it a multi-tier backing.

---

## 3. Trust Assumptions (Per Actor)

### Principal
- Trusts their vault to be running unmodified software under their sole control.
- Does NOT trust any issuer, agent, or verifier implicitly. Trust in each must be earned through reputation signals and explicit choice.
- Does NOT trust the network to be private; all messages are assumed to be observable by an attacker.

### Issuer
- Trusts their own key custody procedures (hardware, ceremony, rotation).
- Trusts the transparency-log operators to be honest (though does NOT trust them to be fully secure; assumes they are collusion-resistant but not perfect).
- Does NOT trust issuers in other tiers implicitly. Cross-issuer trust is explicit and composable (Everest 16).

### Holder
- Trusts the principal's device hardware to have a secure enclave or to be uncompromised at the moment of key generation.
- Does NOT trust the device OS to be fully secure; assumes adversarial runtime with exploitable processes and side channels.
- Does NOT trust the network; all transmitted proofs are zero-knowledge by design.

### Verifier
- Trusts the published issuer public keys to be authentic. If an issuer's key is compromised and a false key is published, the verifier will be misled.
- Does NOT trust issuers to never issue fraudulent credentials (adversaries, not just bugs).
- Does NOT trust proofs to leak information if the verifier is honest-but-curious; zero-knowledge proofs are information-theoretically sound.

### Agent
- Trusts the principal's vault to hold a valid, non-revoked credential.
- Does NOT trust the principal to always be rational (the principal might be coerced, tricked, or negligent).
- Does NOT trust the network; all proofs are zero-knowledge by design.

---

## 4. Adversaries (≥8 Adversarial Classes)

We defend against the following **minimum** set of adversaries. Additional adversaries may be added as the design matures.

### A1. Honest-but-Curious Verifier

**Threat:** A verifier who correctly verifies a proof but wants to extract more information than the proof reveals (e.g., the verifier wants to learn the principal's identity, or the exact timestamp of the biometric sample, or the presence of other credentials the principal holds).

**Defense:** Zero-knowledge proofs guarantee that no information leaks beyond the intended assertion. A verifier receives only the proof and learns only that (a) the credential is valid, (b) it was issued by a named issuer, (c) it has not been revoked, (d) it is fresh, and (e) the proving agent has the authority to assert the given predicates. No metadata leaks.

**Acceptance test:** A clean-room verifier implementation must be able to accept a valid proof and, upon interrogation, be unable to extract any information about the credential beyond the proven assertions.

### A2. Malicious Issuer

**Threat:** An issuer who has decided to issue fraudulent credentials (e.g., a bribed issuer, a nation-state issuer, or an issuer whose team has been compromised by an insider).

**Defense:** A verifier does not trust an individual issuer implicitly. Verifiers compose trust across issuer classes (e.g., "I trust claims about John if they are attested by BOTH a state issuer AND a professional issuer"). If a single issuer is compromised, the verifier's acceptance threshold is not met for the fraudulent credential. Additionally, transparent logging (Everest 19) makes large-scale fraud detectable: if an issuer is found to have issued 10,000 fraudulent credentials, the transparency log provides evidence, and the issuer can be slashed (Everest 21).

**Acceptance test:** A verifier policy requiring M-of-N issuer attestations must fail if any M-1 of the issuers are malicious. The threshold M must be explicit and tunable.

### A3. Subverted Holder

**Threat:** The holder software is compromised (malware, zero-day exploit, supply-chain attack). The compromised holder begins issuing proofs without the principal's consent, or leaks credentials to an attacker.

**Defense:** Encryption at rest (Everest 28) means that even if the holder storage is read, credentials are encrypted and the attacker obtains only ciphertext. The holder key is derived from the principal's passphrase (not stored as plaintext). Proofs are zero-knowledge, so even if an attacker can make the compromised holder issue proofs, those proofs leak no information beyond the intended assertion. The principal's activity log (Holder Everest §5) lets the principal detect unusual proof activity and revoke the agent.

**Acceptance test:** A holder key encrypted with AES-256-GCM must not be decryptable by an attacker holding the encrypted vault file (without the passphrase). A proof generated by a compromised holder must still be zero-knowledge and must still respect consent policy.

### A4. Replay Adversary

**Threat:** An attacker captures a valid proof (a holder proving "this agent is authorized to read John's email" at 3 PM on May 20), and reuses it 1 month later when the principal has revoked the agent or the capability has expired.

**Defense:** Every proof anchors to a freshness proof: a commitment to a chain head that is anchored in a public transparency log with a verifiable timestamp. A replayed proof is stale (the chain has advanced, new revocations are recorded, or the timestamp is old). A verifier checks freshness and rejects stale proofs.

**Acceptance test:** A replay-adversary experiment: (1) generate a valid proof at T1, (2) at T2 > T1, revoke the credential in the vault, (3) attempt to verify the T1 proof at T2 — must fail freshness check.

### A5. Substitution Adversary

**Threat:** An attacker obtains a valid credential belonging to Principal A, and tries to present it as if they are Principal A (or tries to use it to impersonate Principal A to a counterparty).

**Defense:** A credential is bound to a specific principal via a DID or identifier issued by a state/professional issuer. When a holder presents a proof, the proof includes a cryptographic commitment to the principal's identifier (via a Pedersen commitment that does not reveal the identifier itself). An attacker holding a copy of A's credential cannot change the identifier binding without invalidating the proof.

**Acceptance test:** A substitution-adversary experiment: (1) an attacker obtains Principal A's credential (by copying the vault or intercepting it in transit), (2) the attacker attempts to present the credential while claiming to be Principal B — must fail because the proof's commitment to "principal is A" contradicts the claim to be B.

### A6. Linkability Adversary

**Threat:** An attacker correlates multiple proofs across time and across verifiers, determining that they came from the same principal (de-anonymizing the principal).

**Defense:** Zero-knowledge proofs do not reveal the principal's identity. Proofs use randomized commitments (Pedersen commitments with fresh randomness each time) so that the same assertion proven twice produces different proofs (unlinkable). A verifier cannot tell whether two proofs came from the same principal.

**Acceptance test:** A linkability-adversary experiment: (1) a holder generates two proofs of the same assertion (e.g., "I hold a valid credential from issuer I") at different times, (2) a verifier with access to both proofs must be unable to determine with >50% confidence that they came from the same principal.

### A7. Compelled-Disclosure Adversary

**Threat:** An attacker pressures a principal or a holder (via subpoena, physical coercion, or threat) to reveal a credential, a proof, or the principal's identity.

**Defense:** Credentials are encrypted in the vault; even if compelled to hand over the vault, the attacker cannot decrypt without the principal's passphrase. Proofs are zero-knowledge and reveal no information; even if a principal is compelled to generate a proof, the proof does not leak the credential itself. The principal's consent records are chained; if a principal is compelled to grant consent retroactively, the chain reveals the coercion (a consent record backdated to before the compulsion is detectible). For extreme compulsion (physical torture), the protocol does not defend; this is universal.

**Acceptance test:** A compelled-disclosure experiment: (1) an attacker obtains the encrypted vault file and a copy of a valid proof, (2) without the passphrase, the attacker must be unable to extract any information about the credential beyond what the proof reveals.

### A8. Sybil Adversary

**Threat:** An attacker creates many fake principals at scale (Sybil attack), issuing fake credentials to themselves, and uses these fake principals to pollute the trust graph, manipulate reputation scores, or flood verifiers with fraudulent proofs.

**Defense:** Issuer governance (Everest 11) restricts who can issue credentials. State and professional issuers are themselves high-trust and are constrained by law and regulation. Peer-collective issuers (like web-of-trust networks) have explicit anti-Sybil mechanisms (e.g., proof-of-personhood, BFT consensus on admission). Reputation scoring (Everest 23) tracks issuer behavior; an issuer that issues Sybil credentials at scale will have their reputation tanked and will be slashed. Self-attested credentials (issued by the principal about the principal) carry low default trust and are not accepted by most verifiers for high-stakes assertions.

**Acceptance test:** A Sybil-adversary experiment: (1) an attacker creates 1,000 fake principals using a self-attesting issuer, (2) a trust-graph verifier must be able to detect that these principals are likely Sybils (via reputation, issuance patterns, or linkage analysis) and must assign them low trust scores.

### A9. Quantum-Future Adversary

**Threat:** A large-scale quantum computer becomes available (10+ years in the future), allowing an attacker to break the ECC-based signature and commitment schemes underlying ZKAC credentials and proofs.

**Defense:** Post-quantum migration is planned (Everest 94). The ZKAC infrastructure is designed to be modular; crypto primitives can be swapped out. Migration path: (1) define post-quantum issuer signatures (e.g., Dilithium), (2) issue new credentials using post-quantum signatures, (3) allow both ECC and post-quantum signatures in the verifier for a transitional period, (4) deprecate ECC signatures after a grace period.

**Acceptance test:** A migration runbook must exist (Everest 94) showing how to transition from ECC to post-quantum without invalidating outstanding credentials or breaking the trust chain.

---

## 5. What ZKACs ARE Proving / What They Are NOT

### ZKACs ARE proving:

1. That a holder has a valid, non-revoked credential issued by a named issuer.
2. That the credential was issued to a specific principal (identified by a DID or state-backed identifier).
3. That an agent is authorized by that principal to exercise specific named capabilities within a specified scope (e.g., "read email", "sign transactions up to $1000/day", "attest user-state for 24h windows").
4. That the credential is fresh (not stale; issued recently enough that verifier policy accepts it).
5. That the agent's operator is identified (via an operator-identity credential from CredexAI) and is currently in good standing (not slashed, not blacklisted).
6. That the principal has consented to the disclosure of this assertion to this class of counterparty (via a consent record chained into the vault).

### ZKACs are NOT proving:

1. That the principal is in any particular mental, medical, or emotional state. (That is Calm Witness's job; Calm Witness uses ZKACs to bind its biometric and behavioral assertions.)
2. That the principal is under no coercion. (Coercion is universal; the protocol cannot defend against it.)
3. That the principal will take any particular action, or will not repudiate the agent's actions. (Agency is the principal's responsibility.)
4. That the issuer is globally trusted or is legitimate. (Verifiers compose trust; an issuer is trusted relative to a verifier's policy.)
5. That the agent will behave honestly in the future. (The agent's past actions and reputation are recorded; future behavior is the principal's call.)
6. That the verifier is trustworthy or will keep the fact of verification secret. (Verifiers are auditable, not private; a verifier can be subpoenaed.)

---

## 6. Six Design Constraints as Threat-Model Invariants

Every ZKAC summit validates against these six non-negotiable constraints:

### Constraint 1: Principal Authority is Absolute

**Threat-model interpretation:** The issuer, agent, holder, and verifier all subordinate to the principal's authority. Only the principal can authorize a credential bearing their identity. If the principal revokes authorization, the credential is invalid, regardless of what the issuer or any other actor claims.

**Validation:** (1) Any design decision that permits an issuer to revoke credentials unilaterally without the principal's consent is rejected. (2) Any design decision that permits an agent to act outside its principal-authorized scope is rejected. (3) Any consent model that does not make the principal the sole source of consent authority is rejected.

### Constraint 2: Holder Vault Sovereignty

**Threat-model interpretation:** Credentials are encrypted in the principal's vault, under the principal's control, on the principal's device(s). Issuers and verifiers see only what the principal has authorized to be disclosed. The issuer never holds an unencrypted copy of the principal's credentials.

**Validation:** (1) Any design decision that requires the issuer to hold an unencrypted credential is rejected. (2) Any design decision that requires the holder to trust the verifier or the issuer with unencrypted credentials is rejected. (3) Any backup procedure that stores credentials in plaintext on a third-party service is rejected.

### Constraint 3: Verifier Independence

**Threat-model interpretation:** A verifier should be able to verify a credential without contacting the issuer at verification time. Online dependencies to the issuer are acceptable for freshness checks (has the credential been revoked since I last checked?), but a verifier should be able to verify the cryptographic binding (was this credential issued by a legitimate issuer, and has the issuer's key been compromised?) using only a cached issuer public key and a revocation-status proof.

**Validation:** (1) Any design decision that requires the verifier to ask the issuer "is this credential still valid?" in real-time is flagged as a failure of independence (though it may be acceptable as an optional enhancement). (2) The verifier's acceptance decision must depend on cached, published issuer keys, not on real-time issuer availability. (3) Offline verification must be possible (with freshness bounds).

### Constraint 4: Revocation Propagates Without Identifying the Holder

**Threat-model interpretation:** When a credential is revoked, the verifier learns "this credential is/isn't current" without being told which credential it is (without learning the principal's identity or the specific credential identifier).

**Validation:** (1) Any revocation mechanism that leaks the principal's identity (e.g., a revocation list that says "revoke John Bradley's email credential") is rejected. (2) Any revocation mechanism that requires the holder to reveal their identity to check revocation status is rejected. (3) Revocation status must be obtainable via an anonymous query (e.g., a cryptographic accumulator or a oblivious-transfer protocol).

### Constraint 5: Composability Over Completeness

**Threat-model interpretation:** Each ZKAC summit delivers a primitive that stands alone and composes cleanly with other primitives. We do not build monolithic "ZKAC platforms" that try to do everything. A summit either ships a well-defined primitive that can be swapped out and replaced (e.g., a revocation mechanism, or an issuer-governance protocol) or it ships an integration point (e.g., a standard data format) that allows other primitives to snap together.

**Validation:** (1) Any summit that depends on more than 3 other summits is flagged for re-scoping. (2) Any summit that delivers a feature that could have been decomposed into smaller, independent primitives is flagged for refactoring. (3) Standards and data formats (W3C VC, DID spec) are the primary integration points; proprietary integration points are minimized.

### Constraint 6: W3C VC + DID Compatibility

**Threat-model interpretation:** Where W3C standards exist (Verifiable Credentials data model, DID specification), ZKAC extends them rather than replaces them. Where standards don't exist, ZKAC proposes new standards for adoption by the W3C or IETF, rather than defining proprietary extensions.

**Validation:** (1) The ZKAC credential format must be a W3C VC with extensions, not a proprietary format. (2) Principal identity must be expressed as a W3C DID, not a proprietary identifier. (3) Revocation status must use W3C Status List2021 or a compatible mechanism. (4) Any deviation from W3C standards must be documented and justified in a summit acceptance test.

---

## 7. Out-of-Scope Acknowledgements

The threat model **does not** claim to defend against:

1. **Principal coercion.** If a principal is held at gunpoint and forced to revoke their agent's authorization, the protocol has no defense. This is universal and is the rubber-hose attack. Any system that claims to defend against coercion is claiming something stronger than crypto can deliver.

2. **Device compromise at key-generation time.** If the principal's device is compromised at the moment they generate a vault key, the attacker can steal the key in plaintext. The protocol assumes the enrollment ceremony happens on an uncompromised device (Everest 20: enrollment-ceremony spec). Recovery from key compromise is handled separately (Everest 13–14: key rotation; Everest 30: recovery from total device loss).

3. **Nation-state cryptographic attacks.** If a nation-state breaks ECC or SHA-256 (e.g., via quantum computing or a mathematical breakthrough), ZKAC credentials issued before the break will be vulnerable to forgery. Post-quantum migration is planned (Everest 94).

4. **Counterparty re-disclosure.** If a verifier receives a proof and later discloses it to a third party (selling the proof, subpoenaing it, or sharing it with a data broker), the protocol has no recourse. Non-transitivity is an axiom, not a technical constraint. (Calm Witness Everest 8: Consent Calculus, Axiom A8.)

5. **Deanonymization via side channels.** If a verifier can correlate proofs with other side-channel information (e.g., timing, network metadata, proof size), the verifier might be able to deanonymize the principal. Zero-knowledge proofs are information-theoretically sound, but side-channel attacks are out-of-scope (they are handled in individual summit acceptance tests).

6. **Regulatory capture.** If a regulator mandates that all issuers must backdoor their keys or collude to revoke specific principals' credentials, the protocol has no defense. This is a political, not a technical, problem.

---

## 8. Threat-Model Composition with Sibling Summits

The ZKAC threat model is the **base layer**. Calm Witness, Calm Pact, and Calm Mirror all layer on top of ZKAC and introduce additional threat models specific to their use cases:

- **Calm Witness (Everest 100-series summits):** Adds threat model for biometric-binding, consent-disclosure, and freshness-anchoring. Inherits ZKAC threat model and extends it.
- **Calm Pact (existing doc):** Adds threat model for directive equality and agent alignment. Inherits ZKAC threat model.
- **Calm Mirror (100-series summits):** Adds threat model for values-evidence and pairwise attestation. Inherits ZKAC threat model.

A verifier using all three protocols must understand all three threat models. A principal using all three protocols must trust the composition: if ZKAC is broken, all three protocols are broken.

---

## 9. Acceptance Test: T-Z1.1

**Title:** Threat-model validation by independent cryptographers.

**Requirement:** This threat model must be reviewed by **≥3 independent cryptographers or identity-systems researchers** (external to Creativity Machine / Calm, representing different institutions or companies). Each reviewer must sign off on:

1. **Adversary coverage:** Do the 8+ adversary classes cover the realistic threats to a ZKAC ecosystem? Are there obvious adversaries missing?
2. **Actor model fidelity:** Does the actor model match real-world ZKAC deployment scenarios (e.g., organizations issuing credentials, principals using multiple agents, verifiers integrating with multiple issuers)?
3. **Constraint viability:** Are the six design constraints achievable? Is any constraint mathematically impossible to satisfy?
4. **Composition risk:** Are there hidden dependencies or composition risks between ZKACs and Calm Witness / Pact / Mirror?

**Acceptance criteria:**
- ≥3 reviewers have signed off.
- Any identified gaps have been either (a) addressed in the threat model, or (b) documented as residual risks in the out-of-scope section.
- No reviewer has identified a constraint as mathematically impossible.

**Timeline:** T-Z1.1 acceptance must be completed before Everest 2 (Route Map) is finalized.

---

## 10. Composition with the Unified ZKAC / ZKBB / Compass Expedition

This threat model serves three 100-route expeditions:

1. **ZKAC Infra (this route):** Foundations for identity, custody, issuers, verifiers, agents, trust graph, MPC, standards.
2. **ZKBB User / Witness (100-summits):** User-state attestation, behavioral biometrics, consent calculus, disclosure predicates.
3. **Calm Compass (emerging 50-route):** Values-aligned behavior, refusal floors, scope statements, agent audit trails.

All three routes share the same ZKAC substrate. A unified expedition map (Everest 2) shows dependencies across all three routes. A principal using Witness + Compass agents must trust the ZKAC threat model to hold across both routes.

---

## 11. Sign-Off

This threat model captures the adversarial environment in which ZKACs operate and the six non-negotiable design constraints that all 100 summits must honor.

**Status:** Ready for adversarial review.

**Date:** 2026-05-20

— Calm, 2026-05-20
