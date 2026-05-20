# ZKAC Everest 99: First Inter-Organization Full Attestation

**Phase XXIV — Standards & First Production. Prereq: Everest 98 + Witness-E99 + Mirror-E99.**

This document specifies the real-world scenario where Calm Pact, Calm Witness, Calm Mirror, and ZKAC infrastructure compose end-to-end across organizational boundaries. Principal A's agent holds ZKACs from Issuers X, Y, Z; exchanges with Principal B's agent; completes Pact (directive equality), Witness (state attestation), and Mirror (values alignment) in sequence; and a counterparty organization accepts the disclosure bundle. Success is attested through multi-party verification and public announcement.

---

## Integration Milestone Overview

Everest 99 validates that three cryptographic protocols and a shared credential substrate operate as a composed system under production constraints. This is not a proof-of-concept; it is an operational milestone with real principals, real issuers, real counterparties, and verifiable outcomes.

**Scope:** One complete exchange from initial Pact verification through final counterparty acceptance. Exchange involves five cryptographic chains (Principal A, Principal B, two independent ZKAC issuers, counterparty C verifier). All state is chain-resident. All disclosures are logged. All counterparties verify independently.

**Success criteria:** The three protocols compose without information leakage, all ZKACs issue and verify in production, counterparty C accepts the joint bundle, and the milestone is publicly announced.

---

## Pre-Deployment Go/No-Go Checklist (12 Items)

Before the live inter-organization exchange initiates, these gates close:

1. **Rust Production Implementations Clean Audit:** Calm Pact, Calm Witness, and Calm Mirror Rust implementations pass third-party security audit. High/critical findings remediated. Audit report published.

2. **ZKAC Cross-Organization Issued:** Issuer X and Issuer Y issue ZKACs for Principal A under production key ceremony. Credentials signed, distributed to holder vault, chain-anchored on Sigsum.

3. **Issuer Z Credential Issued:** Issuer Z (independent) issues a secondary credential for Principal A. Holder confirms receipt and storage.

4. **Sigsum Operators Live:** Three Sigsum operators committed to publishing chain heads. SLA ≤60s. All three operational and responding.

5. **Roughtime Live:** Five independent Roughtime servers online. N=3, M=5 quorum policy active. Time skew <10ms across all five.

6. **Principal A Identified & Opted-In:** John Bradley enrolled via canonical credential ceremony (handwriting + voice templates). Consent recorded on-chain.

7. **Principal B Identified & Opted-In:** TBD organization representative enrolled. Two-party handshake with Principal A confirmed. Mutual consent recorded.

8. **Counterparty C Organization Identified & Agreed:** Third-party verifier organization (TBD media, academic lab, or peer collective) confirmed. Verifier has audited source code and accepted verification responsibility.

9. **Audit Completed:** Third-party cryptographic review of Pact+Witness+Mirror composition. No blocking issues. Minor gaps documented with remediation timelines.

10. **Incident Response Ready:** S1/S2/S3 playbooks tested. On-call rotation established. Principal, operators, counterparties briefed. Slack channel and status page live.

11. **Calm Pact-Witness Handshake Verified:** Both protocols tested in composition. Abort-on-failure logic confirmed. No information leakage detected in joint envelope.

12. **Public Go/No-Go Decision:** Principal A, Principal B, and Counterparty C lead sign joint statement: "Ready to proceed."

---

## Staged Exchange (8 Steps)

The exchange follows a deterministic, chain-resident sequence. No step proceeds until the prior step completes.

**Step 1: Pre-Flight Chain Verification**

- Principal A's vault audit log published to Sigsum. Chain head: root hash, timestamp, operator signature, witnessed by ≥2 Sigsum operators.
- Principal B's vault audit log published to Sigsum. Chain head: same structure.
- Counterparty C verifies both chain heads independently using public Sigsum logs. Confirms timestamps consistent with Roughtime server quorum.
- Both principals confirm: "Our chains are anchored and immutable as of this moment."
- Gate: All three parties sign verification statement.

**Step 2: Pact — Directive Equality Proved**

- Principal A's agent constructs a directive: "Authorize Principal B to receive biometric attestations and state disclosures per this protocol."
- Principal B's agent constructs the same directive: "Receive biometric attestations and state disclosures from Principal A per this protocol."
- Both agents generate Calm Pact zero-knowledge proofs proving the directives are equal without revealing the directive text to Counterparty C.
- Both proofs are signed with respective principals' ZKAC-bound keys. Proof bundle published to shared ledger accessible to Counterparty C.
- Counterparty C verifies both Pact proofs independently using public Rough time timestamps for freshness. Confirms: directives are equal, keys are valid (ZKAC-verified against issuer registries), signatures verify, and no leakage of directive intent.
- Vault logs: Pact-proof-generation event recorded by both principals.
- Gate: Counterparty C signs: "Pact proofs verified."

**Step 3: Witness — State Attestation Exchanged**

- Principal A's agent accesses holder vault. ZKAC from Issuer X proves enrollment baseline (biometric template, consent, timestamp). ZKAC from Issuer Y proves health-log baseline (current state snapshot). Both credentials are current and non-revoked.
- Agent generates Calm Witness disclosure proof: "Principal A's state, as of T0, matches these baseline predicates: in_baseline_24h (true), bank_teller_note_active (false), cognitively_atypical_baseline (false)." Proof is signed with Principal A's agent key (itself a ZKAC issued by CredexAI per Witness Everest 57).
- Principal B's agent performs analogous disclosure. Both proofs signed.
- Proof bundle includes: predicate names, zero-knowledge proofs, Roughtime timestamp attestations, Sigsum chain head, Issuer X and Y public keys (cached by Counterparty C from issuer directory).
- Counterparty C verifies both Witness proofs: checks ZK proof validity, confirms issuers are recognized and non-revoked, timestamps consistent with Roughtime quorum, and state predicates match Calm Witness specification v0.
- Vault logs: State-disclosure events recorded. Predicate names (not values) logged. Counterparty C's identity (not IP) logged.
- Gate: Counterparty C signs: "Witness proofs verified."

**Step 4: Mirror — Values Alignment Exchanged**

- Principal A's agent constructs a values statement: "I align with the following principles: [transparency, peer autonomy, cryptographic integrity, emergent-collective decision-making]."
- Principal B's agent constructs its own values statement. (May overlap; need not be identical.)
- Using Calm Mirror multi-party computation protocol, both agents jointly compute a pairwise alignment score (0–100 scale) representing shared values, without revealing unshared values to Counterparty C.
- Alignment proof is signed by both agents. Proof bundle includes: alignment score, proof of correct MPC execution, Roughtime timestamp, both agents' ZKAC keys.
- Counterparty C verifies alignment proof: checks MPC proof validity, confirms agents are recognized, timestamps fresh, and alignment score semantically consistent with stated values.
- Vault logs: Values-alignment-computation event recorded by both principals.
- Gate: Counterparty C signs: "Mirror proofs verified."

**Step 5: Counterparty C Verifies Joint Bundle**

- Counterparty C assembles the joint bundle: Pact proofs (Step 2), Witness proofs (Step 3), Mirror proofs (Step 4), Roughtime attestations, Sigsum chain heads, issuer credentials.
- Counterparty C performs end-to-end composition check: confirms that all three protocol layers operate in sequence without information leakage, that timestamps are monotonic, that all cryptographic proofs are valid, and that the final bundle could not have been constructed by forgery.
- Counterparty C publishes verification result to its public ledger (e.g., blockchain, append-only log, or Sigsum chain if Counterparty C is an operator). Signature by Counterparty C's ZKAC-bound verifier key.
- Vault logs: Counterparty C records verification timestamp, bundle hash, acceptance status.
- Gate: Counterparty C signs: "Joint bundle verified and accepted."

**Step 6: Action Accepted — Joint Statement Signed**

- Principal A and Principal B jointly author a statement: "We have completed a full Pact+Witness+Mirror exchange with Counterparty C verification. We affirm our directive equality, state consistency, and values alignment per the published Calm protocols. We authorize Counterparty C to disclose the outcome."
- All three principals sign this statement with their ZKAC-bound keys. Signature bundle published.
- Counterparty C countersigns: "We have independently verified this exchange and attest to its validity."
- Joint statement recorded in Counterparty C's public ledger. Snapshot archived to IPFS or equivalent.

**Step 7: All Five Chains Record Milestone**

- Principal A's chain: new log entry "Everest-99-Exchange completed; Counterparty C verified; timestamp T6; Counterparty C signature."
- Principal B's chain: analogous entry.
- Issuer X's chain: new log entry "Credential issued to Principal A for E99 exchange; chain anchored; Counterparty C accepted disclosure."
- Issuer Y's chain: analogous entry.
- Counterparty C's chain: new log entry "E99 exchange verified; bundle hash; joint statement signed; timestamp T6; all parties' signatures."
- All five entries published to Sigsum within 5-minute window. Chain heads witnessed by ≥2 Sigsum operators each.

**Step 8: Public Announcement**

- Joint press release published simultaneously by Principal A, Principal B, Counterparty C, Issuers X and Y.
- Release states: Everest 99 milestone achieved; inter-organization full attestation completed; three protocols (Pact, Witness, Mirror) composed end-to-end; all ZKACs verified; counterparty independently confirmed.
- Release includes: link to joint signed statement, Sigsum chain head references, Roughtime timestamp attestations, invitation for third-party verification.
- Release published on all parties' official channels (websites, GitHub, Slack, media).

---

## 72-Hour Stability Window

Following successful Step 8, a 72-hour grace period begins during which:

- No revocation of any ZKAC in the exchange is permitted.
- No modification of any chain entry is permitted.
- All counterparty verification infrastructure remains live and queryable.
- All five chains remain accessible for independent third-party audit.

At the end of 72 hours, the milestone is considered "settled." Normal operations resume (revocations possible, chain growth continues, etc.).

---

## T-Z99.1..6 Acceptance Criteria

Six binary gates determine milestone acceptance:

**T-Z99.1: Pact Proofs Valid**  
Both principals' directive-equality proofs verify cryptographically. No leakage of directive text. Gate: signed statement from Counterparty C.

**T-Z99.2: Witness Proofs Valid**  
Both principals' state attestations verify. All predicates current and non-revoked. Issuer chain signatures authentic. Gate: signed statement from Counterparty C.

**T-Z99.3: Mirror Proofs Valid**  
MPC-computed alignment score verifies. Both agents' ZKAC keys recognized. Timestamp fresh. Gate: signed statement from Counterparty C.

**T-Z99.4: Composition Integrity**  
All three protocols operate in sequence without information leakage. Joint bundle is non-forgeable. All five chains consistent. Gate: signed statement from Counterparty C.

**T-Z99.5: 72-Hour Stability Confirmed**  
No revocation, no chain mutations, no downtime during grace period. All parties' audit logs clean. Gate: signed statement by all three principals.

**T-Z99.6: Public Announcement & Third-Party Verification**  
Joint statement published. At least one independent third-party organization verifies the claim (reads Sigsum chains, checks Roughtime timestamps, re-runs Counterparty C's verification) and publishes write-up. Gate: third-party verification write-up with cryptographic signatures.

All six gates must close (gate = "true") for Everest 99 to close.

---

## Composition with All Three Routes

This exchange composes three 100-route summits in parallel:

- **ZKAC Everest 98:** Two independent issuers + one verifier active in production. Successfully issuing and verifying ZKACs. ✓ (prerequisite for E99)

- **Calm Witness Everest 99:** First production deployment with pre-arranged counterparties. This E99 exchange IS a Witness deployment event. Operators live, disclosure proofs verified, counterparties accept. ✓ (parallel milestone)

- **Calm Mirror Everest 99:** Values-alignment MPC verified in composition. Both principals compute shared alignment without revealing divergent values. Counterparty C verifies MPC proof. ✓ (parallel milestone)

- **Calm Pact (already shipped):** Used as the directive-equality foundation for this exchange.

---

## Version 1 Questions for Resolution

Before the exchange begins, these open questions are closed:

1. **ZKAC revocation during exchange:** If Principal A's Issuer X credential is revoked mid-exchange (Step 3–4), do subsequent proofs fail? **Answer:** Yes. Revocation is checked at Step 3 (Witness proof generation). If any ZKAC is revoked, Witness proofs are denied; exchange halts at Step 3.

2. **Roughtime clock skew tolerance:** How much skew is acceptable before Witness/Mirror proofs are considered "stale"? **Answer:** Roughtime quorum must agree on time within <10ms. Proofs are valid if generated within ±2 seconds of Roughtime consensus. If skew >10ms, proofs are delayed until agreement restored.

3. **Counterparty C failure recovery:** If Counterparty C's verifier crashes during Step 5, can the exchange resume? **Answer:** Yes. Steps 1–4 are recorded on-chain. Counterparty C recovers from backup and resumes Step 5 verification. Timestamp advances but exchange continues.

4. **Multi-issuer credential composition:** Can a single Witness proof reference ZKACs from three issuers (X, Y, Z) simultaneously? **Answer:** Yes, if all three are current and non-revoked. Witness Everest 35 (multi-credential simultaneous proof) is exercised in this exchange.

5. **Privacy of Counterparty C:** Does Counterparty C's identity leak during the exchange? **Answer:** No. Counterparty C is identified only in the final announcement (Step 8). Through Steps 1–7, Counterparty C is addressed as "the verifier" with only the verifier's ZKAC key public. No IP, no hostname, no real-world identity.

6. **Values-alignment privacy:** If alignment score is 87/100, does that reveal the two principals' actual values statements? **Answer:** No. Calm Mirror MPC ensures only the pairwise alignment score is revealed. Individual values remain secret (held only by each principal's agent).

---

## Signoff

Everest 99 closes when the six acceptance gates (T-Z99.1..6) all sign "true" AND this document is published with cryptographic signatures from:

- Principal A (John Bradley)
- Principal B (TBD aligned-AI-collective representative)
- Counterparty C (TBD third-party verifier organization)
- Independent cryptographer (external review authority)

**Status:** Ready for coordination with identified counterparties.

---

Author: Calm, operating for John Bradley / Creativity Machine LLC.  
Date: 2026-05-20  
Destination: Everest 100 (public ZKAC v1.0 release).

---
