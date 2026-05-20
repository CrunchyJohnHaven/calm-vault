# S239 — IETF Draft v1 (Sections 1-3, Partial Bag)

```
Internet-Draft                                              J. Bradley
Intended status: Standards Track                    Creativity Machine LLC
Expires: 2026-11-20                                        May 20, 2026

    Calm Witness: A Zero-Knowledge User-State Attestation Protocol
                    for Autonomous AI Agents

                   draft-calm-witness-00
```

---

## Status of This Memo

This document is an Internet-Draft and is submitted in full conformance with the provisions of BCP 78 and BCP 79.

Internet-Drafts are working documents of the Internet Engineering Task Force (IETF). Note that other groups may also distribute working documents as Internet-Drafts. The list of current Internet-Drafts is at https://datatracker.ietf.org/drafts/current/.

Internet-Drafts are draft documents valid for a maximum of six months and may be updated, replaced, or obsoleted by other documents at any time. It is inappropriate to use Internet-Drafts as reference material or to cite them other than as "work in progress."

This Internet-Draft will expire on November 20, 2026.

---

## Copyright Notice

Copyright (c) 2026 IETF Trust and the persons identified as the document authors. All rights reserved.

This document is subject to BCP 78 and the IETF Trust's Legal Provisions Relating to IETF Documents (https://trustee.ietf.org/license-info) in effect on the date of publication of this document. Please review these documents carefully, as they describe your rights and restrictions with respect to this document. Code Components extracted from this document must include Revised BSD License text as described in Section 4.e of the Trust Legal Provisions and are provided without warranty as described in the Revised BSD License.

---

## Abstract

Autonomous AI agents operating on behalf of human principals increasingly interact with counterparty agents representing distinct organizations. A frequently required safety input is a determination of whether the human principal is currently operating in a state consistent with their enrolled behavioral baseline. Existing approaches require either the principal's synchronous presence, unchecked reliance on the calling agent's assertion, or transmission of raw biometric and psychiatric evidence to the counterparty — each of which is operationally unscalable, cryptographically unsound, or privacy-destructive.

This document specifies the Calm Witness protocol, which enables an operator agent to present a single authorized Boolean attestation ("the principal is in baseline" or "the principal is not in baseline") to a counterparty agent. The attestation is derived from a hash-chained, principal-authored self-narration log and an optional on-device behavioral-biometric distance proof, but neither the log contents nor the biometric material are disclosed. The protocol uses a Sigma-protocol zero-knowledge proof over Pedersen commitments, anchored to a public transparency log providing tamper-evidence and freshness guarantees. The counterparty learns exactly one bit and its freshness window. Nothing else is disclosed.

The Calm Witness protocol is designed to compose with the Calm Pact directive-equality protocol [I-D draft-calm-witness-00], forming a two-handshake model for autonomous-agent session establishment.

---

## Table of Contents

```
1.  Introduction
    1.1.  Problem Statement
    1.2.  Threat Model Overview
    1.3.  Scope and Non-Goals
2.  Conventions and Definitions
    2.1.  Requirements Language
    2.2.  Terminology
3.  (Sections 4-N: Reserved — see Handoff)
```

---

## 1. Introduction

### 1.1. Problem Statement

The deployment of autonomous AI agents as first-class participants in multi-party transactions — executing financial instructions, negotiating agreements, representing principals before institutional counterparties — introduces a class of safety question that has no adequate answer in current protocol specifications: *how should one agent credibly inform a counterparty agent about the current behavioral state of the human principal the calling agent represents?*

The question is not hypothetical. Consider a scenario in which an autonomous Calm operator agent representing a human principal seeks to execute a high-value transaction on behalf of that principal with a counterparty agent representing a financial institution. The counterparty's compliance policy requires reasonable assurance that the authorizing human is not under duress, is coherent, and is the same individual who established the account relationship. At present, the counterparty's policy options include the following:

(a) Require the principal to appear synchronously on a verified video call. This option negates the operational value of autonomous agency entirely and does not scale to high-frequency agent interactions.

(b) Accept the calling agent's own assertion about principal state. This option is cryptographically unsound: the calling agent may itself be compromised, subject to prompt injection, or instructed by an adversarial payload to misrepresent principal state.

(c) Demand transmission of raw evidentiary material — voice recordings, handwriting samples, behavioral transcripts, or clinical assessments. This option is privacy-destructive: sensitive biometric and behavioral data accumulates at counterparty infrastructure with no defined retention, consent, or deletion semantics, and creates compelled-disclosure risk under multiple jurisdictions.

This specification defines a fourth option: a cryptographically verifiable, principal-authorized, single-bit attestation derived from evidence that never leaves the principal's personal vault. The protocol is designed so that a counterparty agent can verify the attestation's freshness, its binding to an enrolled principal identity, and its derivation from a principal-authorized consent record, without receiving any underlying evidence. The counterparty learns the bit and its freshness window. Nothing else is disclosed.

The design is motivated by a well-understood analogy in physical security: the bank-teller distress signal. An employee under duress is able to pass a single bit — "I am being coerced" — to a teller through a pre-arranged codeword or signal, without revealing the details of the coercion and without alerting an observing adversary. The teller receives exactly one bit and acts on it according to standing policy. The Calm Witness protocol generalizes this pattern to the autonomous-agent domain: a principal may pre-enroll a per-principal-secret duress indicator that, when present in the self-narration log, flips the disclosed bit, invisible to any observer who does not hold the principal's secret.

### 1.2. Threat Model Overview

The protocol is designed to withstand the following adversarial scenarios, which are treated formally in Section 5 of this document (reserved in this partial-bag):

**Honest-but-curious counterparty.** A counterparty agent that executes the protocol correctly but attempts to extract additional information about the principal's biometric or behavioral state from the disclosed proof. The proof MUST reveal no information beyond the named predicate identifier, the Boolean evaluation result, and the freshness window.

**Lying calling agent.** An operator agent that is subverted — through compromise, prompt injection, or malicious instruction — and attempts to assert an incorrect predicate evaluation. The disclosed proof MUST be verifiable against the public transparency-log anchor; a falsified proof MUST fail verification with overwhelming probability under standard cryptographic assumptions.

**Replay adversary.** A party that captures a valid Calm Witness proof and reuses it after the freshness window has expired or in a different session context. The protocol MUST bind proofs to a per-disclosure nonce and to a Roughtime-anchored timestamp; replayed proofs MUST fail freshness verification.

**Substitution adversary.** A party that presents a valid proof constructed for a different principal. The proof MUST bind the predicate evaluation to the principal's enrolled biometric template identifier; a proof constructed for a different principal MUST fail template-binding verification.

**Audit-log surgeon.** A party that attempts to retroactively modify the principal's `user_state.jsonl` log to alter what predicates would evaluate to. Because each log record includes the cryptographic hash of its predecessor, and the chain head at proof-generation time is anchored in an externally auditable transparency log (e.g., Sigsum), retroactive modification MUST produce a chain inconsistency detectable against the public anchor.

**Compelled-disclosure adversary.** A legal, regulatory, or coercive party that demands the principal or operator reveal the underlying biometric or behavioral data. The protocol does not eliminate this risk entirely; however, it MUST ensure that (a) each disclosure is bound to a principal-signed consent record specifying the authorized counterparty class and expiry, and (b) the principal is always able to withhold consent even when an earlier policy would have permitted disclosure. The consent record itself is chained into the vault and publicly anchored.

The following are explicitly outside the scope of this specification:

- Rubber-hose attacks against the principal directly. No cryptographic protocol defends against a principal coerced at the point of enrollment.
- Compromise of the principal's enrollment device at template-creation time.
- Nation-state-level cryptographic attacks. Resistance to quantum adversaries is deferred to a future post-quantum migration profile for this protocol.

### 1.3. Scope and Non-Goals

This specification defines:

- The wire format and verification procedure for a Calm Witness disclosure proof.
- The predicate vocabulary for v1 required predicates and the extension mechanism for additional predicates.
- The hydration protocol by which an operator agent constructs and anchors a new self-narration record into the principal's vault.
- The consent-record schema and binding mechanism.
- Composition with Calm Pact for two-handshake session establishment.

This specification does not define:

- The internal format or storage mechanism of the `user_state.jsonl` vault. Operators MAY implement any append-only, hash-chained log store conforming to the chain-head interface defined in Section 4 (reserved).
- The behavioral-biometric comparison algorithm. The protocol commits to a distance value and a template identifier; the comparison algorithm is operator-local and is not exposed to the counterparty.
- Counterparty policy semantics. What a counterparty agent does in response to a disclosed bit is entirely the counterparty's responsibility and is out of scope for this specification.
- Clinical or medical inference from principal state. The predicate vocabulary is explicitly behavioral and self-reported. This specification makes no medical claims and MUST NOT be used as a substitute for clinical assessment.

---

## 2. Conventions and Definitions

### 2.1. Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

### 2.2. Terminology

This section defines the principal terms used throughout this specification. Where a term maps to an existing concept in the Calm Witness design vocabulary (as used in [I-D draft-calm-witness-00] working documents and companion specifications), the mapping is indicated.

**Principal (P)**
The human individual on whose behalf the operator agent acts. The principal is the sole source of authority for vault contents, predicate-evaluation policies, and disclosure consent records. In the Calm Witness design vocabulary: "Principal (P)."

**Operator Agent (O)**
An autonomous AI agent authorized to act on behalf of the Principal. The Operator Agent is responsible for hydration (collecting self-narration records), predicate evaluation, and proof generation. The Operator Agent is explicitly not fully trusted by the Principal: the protocol is designed so that a compromised Operator Agent cannot produce a verifiable false proof. In the Calm Witness design vocabulary: "Calm operator (O)."

**Vault (V)**
A principal-owned, principal-encrypted, append-only data store holding the self-narration log (`user_state.jsonl`), enrolled biometric templates, predicate-evaluation policies, and consent records. The Vault MUST reside on hardware under the Principal's control. The Vault MUST be encrypted at rest with a key that the Operator Agent cannot independently recover. In the Calm Witness design vocabulary: "Calm vault (V)."

**Counterparty Agent (C)**
An autonomous AI agent representing a different principal or organization. The Counterparty Agent is the recipient of a Calm Witness disclosure proof. The Counterparty Agent is not trusted by the Principal and MUST independently verify all proof components before acting on the disclosed bit. In the Calm Witness design vocabulary: "Counterparty operator (C)."

**Verifier Infrastructure (X)**
A set of publicly auditable services used to provide tamper-evidence and freshness guarantees. In v1, this MUST include a Sigsum-compatible transparency log for chain-head anchoring and a Roughtime-compatible service for timestamp binding. The Principal does not trust X to be honest but relies on X's public auditability. In the Calm Witness design vocabulary: "Verifier (X)."

**Self-Narration Record**
A structured entry appended to the Vault's `user_state.jsonl` log during a hydration event. Each record MUST include: a unique record identifier, a cryptographic hash of the preceding record (prev_hash), a Roughtime-anchored timestamp of the time of writing, a principal-supplied affect annotation, and an optional behavioral-biometric distance value. The plaintext content of the record is not disclosed by this protocol.

**Hydration**
The per-session protocol step in which the Operator Agent collects a self-narration input from the Principal, optionally processes a behavioral-biometric sample, appends a new Self-Narration Record to the Vault log, and publishes the resulting chain head to the Verifier Infrastructure.

**Chain Head (H)**
The cryptographic hash of the most recent Self-Narration Record in the Vault log. The Chain Head is the public commitment to the current state of the log without revealing any log contents. The Chain Head MUST be published to the Verifier Infrastructure at the conclusion of each Hydration event.

**Inclusion Proof**
A proof returned by the Verifier Infrastructure demonstrating that a given Chain Head value is present in the transparency log at a specific log index. The Inclusion Proof is included in every Calm Witness disclosure proof to permit the Counterparty Agent to verify log anchoring against the public transparency log.

**Predicate (p)**
A deterministic Boolean function over the current Vault state (a log window, a biometric distance value, and a consent record). Section 4 of this specification (reserved) defines the v1 required predicate vocabulary. Operators MAY extend the predicate vocabulary subject to the extension mechanism defined therein.

**Predicate Identifier**
A string of the form `urn:calm-witness:predicate:<label>` uniquely identifying a named predicate. The Counterparty Agent receives the Predicate Identifier as part of a disclosure proof. Section 4 defines the IANA-registered predicate identifier namespace.

**Baseline**
The enrolled behavioral envelope of the Principal, as defined by the Principal's own self-narration over a reference window. The term is self-reported and behavioral, not clinical. Whether the Principal is "in baseline" is always a function of the Principal's own historical self-narration, not an external evaluation.

**Disclosure Proof (Pi)**
The complete protocol artifact transmitted from Operator Agent to Counterparty Agent in a Calm Witness disclosure exchange. A Disclosure Proof consists of: the Predicate Identifier, a Pedersen commitment to the predicate evaluation result, a Sigma-protocol zero-knowledge proof of correct evaluation, the Chain Head and associated Inclusion Proof, a Roughtime timestamp binding, and an Operator Identity Signature. The exact wire encoding is defined in Section 4 (reserved).

**Pedersen Commitment**
A computationally binding, perfectly hiding commitment scheme used to commit to the predicate evaluation bit prior to proof generation. The Counterparty Agent learns the committed value only after verifying the accompanying Sigma-protocol proof. This specification assumes a standard elliptic-curve Pedersen commitment over a suitable curve defined in Section 4 (reserved).

**Sigma-Protocol Proof**
A three-move interactive zero-knowledge proof (commitment, challenge, response) rendered non-interactive via the Fiat-Shamir heuristic. The Sigma-Protocol Proof in Calm Witness demonstrates that a Pedersen-committed bit is the honest evaluation of the named predicate over the current Chain Head, the enrolled biometric template identifier, and a valid consent record. This proof construction is in the same family as the Calm Pact Sigma-protocol [I-D draft-calm-witness-00] and composes with it directly.

**Biometric Template**
An enrolled reference representation of the Principal's behavioral biometric, stored exclusively in the Vault. The Biometric Template MUST NOT be transmitted outside the Vault. The protocol binds the Disclosure Proof to the Template's identifier (a hash), not to the Template itself. The distance between a current biometric sample and the Biometric Template is committed via a Pedersen commitment; only this committed distance enters the predicate evaluation.

**Biometric Distance (d)**
A non-negative real value representing the degree of divergence between a current behavioral-biometric sample and the enrolled Biometric Template. Distance semantics and thresholds are Principal-configurable. The Biometric Distance value is committed to the Vault during Hydration and enters predicate evaluation but is not disclosed to the Counterparty Agent.

**Consent Record**
A principal-signed, Vault-chained record authorizing disclosure of a named predicate to a specified counterparty class for a specified validity window. A Disclosure Proof MUST include a reference to a valid, unexpired Consent Record. The existence and identifier of the Consent Record are included in the Disclosure Proof; the content of the Consent Record is not disclosed to the Counterparty Agent.

**Duress Indicator**
A per-principal-secret codeword or pattern that, when present in a Self-Narration Record, causes the relevant predicate to evaluate to the "not in baseline" bit regardless of other predicate inputs. The Duress Indicator is the protocol's implementation of the bank-teller distress note: a Principal under coercion can transmit a single bit to a Counterparty Agent through the normal proof mechanism, without the coercing party being able to detect that the bit has been set. The Duress Indicator value MUST be known only to the Principal and MUST NOT be recoverable from any component of the Disclosure Proof.

**Freshness Window**
The time interval, bounded by a Roughtime-anchored timestamp, within which a Disclosure Proof is considered valid. A Counterparty Agent MUST reject any Disclosure Proof whose Freshness Window has expired at the time of verification. The default Freshness Window for v1 required predicates is defined in Section 4 (reserved). Counterparty Agents MAY require shorter Freshness Windows by policy.

**Operator Identity Signature**
A cryptographic signature over the Disclosure Proof produced by the Operator Agent using a credential issued by the CredexAI identity infrastructure (or a compatible operator-identity registry as defined in Section 4). The Operator Identity Signature binds the Disclosure Proof to a specific, registered Operator Agent, permitting the Counterparty Agent to verify that the proof was produced by an enrolled operator rather than an arbitrary party.

**Calm Pact**
A companion protocol, specified separately, that enables two Operator Agents to verify that their respective principals share a categorically equivalent primary directive, without disclosing the directive. Calm Witness is designed to compose with Calm Pact in a two-handshake model: Calm Pact is evaluated first (directive alignment), and Calm Witness is evaluated second (principal state). If either handshake fails, the session MUST abort without additional information exchange.

---

## Handoff: Remaining Sections for Full I-D Submission

This partial-bag covers Sections 1 through 3 (IETF boilerplate, Introduction, Conventions and Definitions). The following work remains before a complete I-D is ready for datatracker submission:

**Section 4 — Protocol Mechanics**
Full specification of the Hydration protocol, Predicate evaluation procedure, v1 required predicate vocabulary and identifier registry, Disclosure Proof wire format (CBOR encoding), Sigma-protocol construction and Fiat-Shamir binding, chain-head anchoring procedure against Sigsum, Roughtime timestamp binding, Operator Identity Signature construction, and Calm Pact composition semantics. This section is the largest remaining body of work and requires working-group iteration on the cryptographic construction.

**Section 5 — Security Considerations**
Formal treatment of all threat-model scenarios introduced in Section 1.2. This section MUST include: zero-knowledge property of the Sigma-protocol proof, binding security of the Pedersen commitment, soundness of the chain-head anchor against log-surgeon attacks, replay resistance of the freshness binding, substitution resistance of the template-identifier binding, and a discussion of residual risks (enrollment-ceremony attacks, rubber-hose, quantum adversaries, and jurisdiction-specific compelled-disclosure regimes).

**Section 6 — Privacy Considerations**
Analysis of the protocol's privacy properties from the Principal's perspective, including: minimum-disclosure design rationale, threat surface created by the Operator Identity Signature (operator linkability), consent record freshness and revocation semantics, relationship to GDPR Article 9 (biometric data), and recommendations for Principal-protective deployment configurations.

**Section 7 — IANA Considerations**
Registration of the `urn:calm-witness:predicate:` namespace. Registration of the v1 required predicate identifiers (`in_baseline_24h`, `biometric_match_within`, `principal_consents_to_disclose`, `bank_teller_note_active`). Registration of the Calm Witness proof content-type identifier for CBOR encoding.

**Section 8 — References**
Normative references: RFC 2119, RFC 8174, Pedersen commitment construction, Fiat-Shamir heuristic, Sigsum transparency log specification, Roughtime (RFC 8915), W3C Verifiable Credentials (for Operator Identity Credential encoding), Calm Pact I-D.
Informative references: Forensic document examination literature on handwriting behavioral biometrics, prior work on anonymous credential schemes (Camenisch-Lysyanskaya), prior work on selective disclosure (BBS+ signatures).

**Working-Group Review**
This I-D requires working-group sponsorship before datatracker submission on a standards track. Candidate homes: SAAG (Security Area Advisory Group), OAUTH WG (for operator credential binding), or a proposed new WG under the Security Area. The two-handshake composition with Calm Pact may warrant joint submission.

**Datatracker Submission**
ID submission requires a valid author affiliation, IPR disclosure, and confirmation of IETF Trust compliance. Creativity Machine LLC is named as the author institution; legal review of the IPR statement is required before submission.

**Plugfest Interop**
Before advancing beyond Proposed Standard, the protocol requires at least two independent implementations demonstrating interoperability on the Disclosure Proof exchange. A plugfest scenario document (covering enrollment ceremony, hydration, disclosure request, and proof verification against a reference implementation) is required. The 100-Everest route map at `/Users/johnbradley/AllData/calm_vault_market/ZKBB_USER_EVERESTS_100.md` tracks implementation summits; plugfest preparation corresponds approximately to Everest 80-90 on that route.

---

*[I-D draft-calm-witness-00] — Partial bag produced session S239, 2026-05-20. Sections 1-3 only. See Handoff above for remaining work.*
