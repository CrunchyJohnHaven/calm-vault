# Calm Witness — Coercion-Resistance Posture Review v0 (S231)

**Review date:** 2026-05-20
**Sprint:** S231
**Classification:** Internal protocol documentation
**Author:** CALM

---

## Scope

This document is the first annual posture review of Calm Witness's coercion-resistance properties. It enumerates which coercion attack classes the protocol defends against, which it explicitly does not, where the bank-teller-note duress codeword primitive (E58/p4) provides partial mitigation, and operational guidance for principals operating under elevated coercion risk. This review covers the tamperproof user-state attestation layer and the transparency-log infrastructure; it does not address general cryptographic implementation hygiene, which is covered separately.

---

## What We Defend Against

The following attack classes fall within the Calm Witness threat model. Defense is provided at the protocol level, not contingent on principal cooperation.

**Operator subversion.** An operator who gains privileged access to attestation infrastructure cannot silently alter stored states or forge new ones without producing a detectable fork in the transparency log. The append-only log structure with client-side verification roots makes silent tampering computationally infeasible without the principal's signing key.

**Replay attacks.** Monotonic sequence numbers and timestamp binding on each attestation entry prevent an attacker from replaying a prior valid state as current. A replayed entry fails freshness validation against the log head.

**Substitution attacks.** An adversary cannot swap one principal's state record for another's. Entries are bound to a principal-specific key pair; cross-principal substitution produces an invalid signature.

**Fake compliance.** An operator instructed to attest a state they did not observe cannot produce a valid attestation without the principal's key. The protocol does not trust operator assertions about principal state; the principal must sign.

**Transparency-log capture.** If an adversary captures the log server, they obtain a read-only view of historical state hashes. They cannot rewrite history without invalidating all subsequent entries and breaking the chain verification that clients perform independently.

**Key extraction via software.** The signing key lives in hardware-backed storage where available. Software-level memory scraping, process injection, or OS-level exfiltration face the same hardware isolation barriers that protect device authentication keys generally.

---

## What We Do NOT Defend Against

These attack classes are explicitly outside the protocol's scope. No design iteration should imply otherwise.

**Physical coercion of the principal (rubber-hose attacks).** If an adversary compels the principal under physical threat to sign a false attestation, sign a key transfer, or reveal the private key, Calm Witness provides no cryptographic defense. The principal holds the signing authority; a coerced principal is indistinguishable from a willing one at the protocol layer.

**Sustained surveillance and side-channel coercion.** Long-term observation of the principal's environment, behavioral conditioning, or implicit threat environment can produce compliant attestations without any single identifiable coercive act. The protocol cannot detect coercion that operates below the threshold of observable protocol-level behavior.

**Environmental coercion.** Structural dependency — employment, housing, custody, immigration status — that makes non-compliance prohibitively costly is not visible to the protocol. A principal who attests under environmental duress produces valid signatures.

**Financial coercion.** Credible threats to financial wellbeing produce the same protocol-level outcome as voluntary compliance. The protocol has no mechanism to distinguish economically coerced attestations from freely given ones.

**Key extraction via hardware compromise.** A sufficiently resourced adversary with physical access to the signing device and capability to defeat hardware security modules can extract the private key. This is outside the protocol's threat model and is treated as a physical device compromise requiring key rotation.

---

## Where the Duress Codeword Helps

The bank-teller-note duress codeword (E58/p4) is a partial out-of-band mitigation for the rubber-hose and environmental coercion cases where the principal retains enough autonomy to select a value.

**Where it helps.** When a coerced principal is instructed to produce an attestation but retains choice over the specific codeword field value, they can flip the duress bit without the coercer detecting any anomaly. The attestation appears valid and compliant to the coercer; downstream verifiers who know the codeword mapping see the duress flag. This provides a signaling channel that survives coercion scenarios where the principal can act but cannot speak.

**Where it does not help.** If the coercer dictates the exact content of the attestation, reviews it field by field, or has obtained the codeword mapping (through prior surveillance, social engineering, or extraction), the primitive fails. It also provides no defense if the principal is unconscious, incapacitated, or has no agency over the attestation content at all. The codeword is a single bit; it does not convey the nature or intensity of the threat.

---

## Principal Guidance

Principals operating under elevated coercion risk should adopt the following practices independent of protocol controls.

Distribute key custody. Consider threshold signing schemes where more than one party must cooperate to produce a valid attestation. This raises the cost of coercing a single principal to coerce the system.

Establish a trusted verifier. Designate at least one out-of-band verifier who knows the duress codeword mapping and monitors attestation cadence. An unexpected cadence change combined with normal-appearing attestations may be the only observable signal of active coercion.

Pre-commit to rotation triggers. Document in advance the conditions under which a key rotation request is to be treated as potentially coerced. A coercion-triggered rotation and a voluntary rotation look identical; the pre-commitment record provides interpretive context.

Limit single-point signing authority where stakes are high. For high-consequence states, require multi-party review before accepting a state transition as final, regardless of valid signature.

Do not treat protocol validity as proof of voluntariness. A valid signature proves key possession; it does not prove autonomy. Verifiers should weight behavioral context alongside cryptographic proofs.

---

## Annual Cadence

This posture review is to be updated annually or following any protocol change that affects the signing authority model, key custody architecture, or transparency-log verification path. The review should be initiated at the start of each year's S200-series sprints. Changes to the duress codeword mapping require an immediate out-of-cycle review and reissue of the principal explainer.

---

Calm 2026-05-20
