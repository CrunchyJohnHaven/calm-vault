# Inter Vault Attestation v0

**Closes Everest 126 of the Everest ladder.**

**Prereq: Everest 125.** This Everest defines the canonical, privacy preserving way for one vault to attest to another vault's identity related state without revealing either vault's contents.

## Purpose

A vault operator sometimes needs a statement from a trusted peer vault that says, in substance, "I confirm this principal's prior vault head" or "I confirm this vault belongs to the same principal that previously held a known head", while keeping the witness material, the chain body, and any internal records private. That is a different problem from ordinary record publication. Ordinary publication is about making a chain auditable. Inter vault attestation is about making a cross vault identity claim portable without turning either vault into an exposed transcript.

This spec exists because a multi vault environment creates a gap between identity and disclosure. Vault A may know something useful about Vault B. Vault B may have a prior head, a principal binding, or a bounded identity claim that Vault A can verify. If Vault A writes a naive statement, it can accidentally leak the very chain details it was meant to protect. If Vault A stays silent, a legitimate identity proof cannot move. Everest 126 fills that gap by requiring a commitment only witness, a no chain leak rule, and explicit principal attribution for the attestation issuer.

The design goal is simple: the receiving party should learn that a specific issuer vault made a bounded statement about a specific subject vault, under a specific principal, on a specific committed witness, and nothing more. The attestation must be useful for authorization, reputation, onboarding, or operator continuity, but it must not disclose the subject vault's contents or the issuer vault's contents. It must also not smuggle in hidden chain state through metadata, side channels, or convenience fields.

## One line spec

> A vault may issue a signed attestation about another vault's identity state only from committed witness material, only with principal attribution, and only with a transcript that omits chain contents, raw heads, and any other secret vault body material.

## Terms

**Vault A** is the issuer vault. It creates the attestation.

**Vault B** is the subject vault. It is the vault whose identity related state is being attested.

**Principal** is the human or machine principal that controls the relevant vault for the purpose of the attestation. The principal attribution is part of the attestation and is not optional.

**Prior vault head** means the committed identifier for a vault chain state that already existed before the attestation. In practice this is a digest, commitment, or equivalent anchor that can be referenced without revealing the chain body.

**Witness material** means the minimum evidence required to justify the attestation. For v0, witness material is commitment only. It may include digests, signed commitments, and proof metadata, but it may not include chain content.

**Transcript** means the attestation payload and its signed envelope. It is the only object that leaves Vault A for the recipient.

**Chain leak** means any disclosure that lets a recipient reconstruct, infer, or enumerate private chain contents, including raw records, unredacted chain heads, internal notes, or hidden links between vaults.

## Protocol summary

Everest 126 defines a narrow trust pattern. Vault A does not claim to know everything about Vault B. Vault A only claims that, based on a committed witness, it can attest to one identity related fact about Vault B. The fact may be that a prior head exists, that a prior head corresponds to the same principal, or that a bounded identity fingerprint matches a commitment previously observed by Vault A. The fact may not be an unbounded summary of Vault B.

The attestation has three actors:

1. The subject vault, Vault B, exposes a commitment that is safe to share.
2. The issuer vault, Vault A, verifies the commitment against its own record or a verified protocol handshake.
3. Vault A signs a structured attestation that names the principal, names the subject vault at a commitment level, and states the exact claim being made.

The structure is deliberately asymmetric. Vault B does not publish its internals just because Vault A attests to them. Vault A does not become a mirror of Vault B. The attestation is a local act by Vault A, anchored in a bounded witness and expressed with a tight schema.

## Commitment-only witness

The witness must be commitment only. That means the issuing vault may use only the following kinds of evidence:

- A digest of a prior vault head.
- A signed commitment emitted by Vault B or by a protocol component that acts as a commitment carrier.
- A principal binding statement that itself refers only to commitments.
- A timestamp or epoch marker if it is needed to order the commitment and it does not reveal chain contents.
- A protocol version marker.

The witness must not include:

- Raw `user_state.jsonl` content.
- Unredacted ledger fragments.
- Internal comments, drafts, or rejected records.
- Private keys, session keys, or recovery material.
- A decoded chain head that exposes structure beyond the commitment.
- A sequence of multiple chain heads if that sequence would expose growth patterns that should remain private.
- Any witness bundle that can be reverse engineered into the vault body.

The commitment-only rule matters because a single leaked line from the chain can destroy the privacy target of the whole system. If a witness includes a raw record, even if the attestation text does not quote it, the recipient can still learn more than the issuer intended to reveal. Everest 126 therefore treats the witness itself as sensitive. The issuer may store it locally. The issuer may hash it. The issuer may keep an audit note that it was seen. The issuer may not export the private body.

A valid witness for v0 can be minimal. For example, Vault A may receive from Vault B a commitment like `head_commitment`, a principal scoped binding, and a protocol nonce. Vault A then verifies that the commitment is current enough, that it resolves to the expected principal binding, and that the claim being made is exactly the claim the recipient is allowed to learn. If the issuer needs a richer evidence set, that evidence set must still stay inside the commitment boundary. More evidence is not better if it leaks chain state.

## No chain leak

The no chain leak rule is the core privacy constraint. Vault A may not include anything in the attestation that would reveal Vault B's contents or Vault A's private contents. This rule applies to the signed payload, the displayed summary, the error path, the logs, and any machine readable wrapper around the attestation.

The following are prohibited in the outgoing transcript:

- Raw chain entries from either vault.
- Full history paths.
- Internal state names that only make sense by reading the private chain.
- Debug dumps, exception traces, and stack traces that expose the witness.
- Any direct reference to storage layout beyond the minimum needed to identify the protocol version.
- Any field that can be used to reconstruct a private chain head from a public transcript alone.

A useful test is simple: if a third party could learn something materially new about Vault B's internal history that was not already implied by the claim itself, then the transcript leaked too much. The claim may say that the subject vault has a valid prior head. It may say that the subject principal matches a prior binding. It may say that the issuer has observed continuity across a version transition. It may not say how the subject vault got there, what the chain contains, or what other principals may exist.

No chain leak also applies to formatting. A text template can leak through extra labels, filename breadcrumbs, or convenience exports. For this reason the spec requires that the implementation keep the human readable rendering and the machine readable envelope in lockstep. The envelope may contain a claim identifier, a commitment identifier, the principal attribution, the issuer identity, the protocol version, and a signature. It may not contain hidden convenience fields that are omitted from the prose but present in JSON. The privacy boundary is the whole artifact, not one paragraph in the middle of it.

## Principal attribution

Every attestation must identify the principal responsible for the attestation in a way that is explicit, reviewable, and stable enough for downstream policy checks. Principal attribution means the recipient can tell who stood behind the claim, not just which process serialized it.

The attestation must include:

- The issuer principal name or stable principal identifier.
- The issuer vault identifier or equivalent stable vault label.
- The subject principal name or stable principal identifier, when the attestation is about a specific subject principal.
- The subject vault label or equivalent stable vault label.
- The attestation mode, such as prior head confirmation, identity continuity confirmation, or bounded cross vault witness confirmation.
- The protocol version.

Principal attribution is required because a vault can be operated by multiple roles over time. The same physical machine, the same storage tree, or the same signing key path is not enough. The attestation must bind to the intended principal context. That binding is what makes the artifact usable in later policy decisions. A recipient can ask whether the attestation came from the correct operator, under the correct role, using the correct authority.

Attribution must be honest about uncertainty. If Vault A cannot determine the principal with adequate confidence from the commitment only witness, it must refuse to issue the attestation. It may not fill in a guess. It may not carry an ambiguous label that would later be treated as certainty. It may not substitute a machine hostname for a principal. This is a policy and safety requirement, not a cosmetic one.

## Attestation object

A v0 attestation SHOULD contain these fields:

- `attestation_id`: stable identifier for the attestation.
- `protocol`: must name Everest 126 or the canonical implementation identifier.
- `issuer_vault`: stable label for Vault A.
- `issuer_principal`: stable label for the principal controlling Vault A.
- `subject_vault`: stable label for Vault B.
- `subject_principal`: stable label for the subject principal, if known.
- `claim_type`: bounded claim name.
- `witness_commitment`: commitment only witness digest or signed commitment reference.
- `claim_body`: short natural language statement describing the exact bounded claim.
- `created_at`: issuance timestamp.
- `expires_at`: optional expiry if policy requires freshness.
- `signature`: issuer signature over the canonical serialization.

The claim body must stay bounded. Good examples are:

- "I confirm this principal's prior vault head matched the committed witness."
- "I confirm Vault B's committed identity binding was present when Vault A verified it."
- "I confirm the subject principal remained bound to the same vault identity commitment across the observed transition."

Bad examples are:

- "I confirm Vault B contains these records."
- "I confirm the vault's internal chain shows X, Y, and Z."
- "I confirm the subject's entire operational history is legitimate."
- "I confirm the principal never did anything suspicious."

The claim body should be narrow enough that an operator can understand it in one glance, but precise enough that policy code can evaluate it without reading between the lines. Everest 126 favors explicitness over implication.

## Issuance flow

The issuance flow for Vault A is as follows.

1. Vault A receives a request to attest about Vault B.
2. Vault A resolves the request into a single bounded claim.
3. Vault A loads only the commitment level witness needed for that claim.
4. Vault A verifies the witness against its own local policy or against a verified handshake artifact.
5. Vault A checks principal attribution and refuses if the principal context is unclear.
6. Vault A confirms that the outgoing transcript contains no chain body, no raw head, and no sensitive debug fields.
7. Vault A canonicalizes the attestation object.
8. Vault A signs the canonical attestation.
9. Vault A emits the signed transcript to the recipient.

The key property is that verification happens before serialization. A system that serializes first and checks later is already on the path to leakage. The issuer must decide what is safe while the data is still local and sensitive. After the transcript exists, the risk surface expands.

If a proof step requires a richer witness than the outgoing attestation can safely include, the issuer may keep that richer witness only in local storage or audit logs with strict access control. The exported attestation must stay lean. The recipient gets the conclusion, not the whole working set.

## Verification flow

A recipient verifies the attestation in three passes.

First, the recipient verifies the signature and the canonical serialization. This ensures the artifact came from the claimed issuer and was not rewritten in transit.

Second, the recipient checks the principal attribution. The issuer principal and subject principal must match the expected policy context. If the attestation is meant to support a specific onboarding, delegation, or continuity decision, the recipient must confirm the principal labels line up with that decision.

Third, the recipient checks that the claim is within scope. The recipient should be able to determine from the attestation alone that it is a commitment only statement. If the attestation includes anything that appears to be chain content, the recipient should reject it. The recipient should also reject any attestation whose wording overreaches the evidence.

Verification does not require chain disclosure. If a recipient needs the chain body, then this spec was the wrong tool. Everest 126 is for bounded identity attestation, not for full audit export.

## Failure cases

The issuer must fail closed in the following cases:

- The subject vault cannot produce a commitment only witness.
- The witness contains raw chain material.
- Principal attribution is ambiguous.
- The claim would reveal more than one bounded fact.
- The protocol version is unknown or unsupported.
- The outgoing transcript would leak chain metadata.
- The issuer cannot canonicalize the statement without introducing private fields.
- The attestation would be misleading even if technically true.

Fail closed means no partial attestation. Do not emit a half useful artifact and hope the recipient ignores the leak. Do not put the sensitive part in a footnote. Do not hide it in logs and assume logs are private. The cleanest failure is no attestation.

## Relationship to prior Everest work

Everest 125 establishes the prerequisite identity and vault lineage foundation. Everest 126 sits on top of that base and uses it without widening the disclosure surface. The relationship is intentionally narrow. 125 gives the vault system a way to know what a vault is. 126 gives one vault a way to make a bounded claim about another vault without turning identity into a disclosure event.

That separation matters because the protocol family is moving from single vault reasoning toward inter vault trust. Once multiple vaults are involved, identity statements can become accidental disclosures. A design that is safe inside one vault can be unsafe across vault boundaries. Everest 126 is the bridge, but it is a guarded bridge.

## Canonical policy requirements

Any implementation that claims compliance with Everest 126 must satisfy all of the following:

- It can issue an attestation about another vault's identity related state.
- It uses only commitment based witness material for that issuance.
- It does not disclose either vault's contents in the attestation.
- It records explicit principal attribution.
- It preserves a stable canonical serialization for signing and verification.
- It treats chain leak as a hard failure.
- It keeps the attestation narrow enough to be auditable and safe.

## Acceptance test

A third party with the spec and an implementation should be able to verify the following scenario:

Vault A receives a request about Vault B. Vault B supplies a prior head commitment and a principal binding statement. Vault A checks the commitment, confirms the binding, and emits a signed attestation that says Vault A confirms Vault B's prior vault head for the named principal. The resulting transcript names the issuer principal, the subject principal, the issuer vault, the subject vault, the commitment identifier, and the claim type. It does not expose Vault A's contents. It does not expose Vault B's contents. It does not expose raw chain entries. It does not expose debug material. It does not expose a hidden summary of the subject chain. A recipient can verify the signature and the principal attribution, and nothing more.

That is the whole point. The attestation is useful because it is narrow. It is safe because it is commitment only. It is legitimate because the principal attribution is explicit. It is portable because it is signed. It is private because the chain never leaves the vault body.

## Implementation notes

Implementers should keep the attestation schema stable. They should resist the temptation to add optional fields that are really just covert disclosure channels. If a future version needs more expressive power, it should be added as a new protocol version with a fresh privacy review.

Implementers should also keep error messages dull. A failure to attest should not spill the reason in a way that reveals the subject vault state. If a reason is necessary for operators, it should stay in local logs under access control, not in the public transcript.

Implementers should prefer stable identifiers over descriptive prose where possible. Prose is for humans. Stable identifiers are for policy. The protocol needs both, but only the stable identifiers should cross vault boundaries.

The durable rule is simple: a vault may speak about another vault's identity, but it may not narrate that vault's private life.

## Final statement

Everest 126 gives the protocol family a clean answer to a common cross vault question. It lets one vault confirm another vault's identity related continuity using only commitments, without revealing either vault's contents, and with explicit principal attribution so the statement can be governed, audited, and trusted.
