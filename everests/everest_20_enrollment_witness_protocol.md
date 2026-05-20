# Everest 20 — Enrollment Witness Protocol

*Phase II — Capture & Enrollment. Prereq: Everest 11.*

## One-line spec

An optional ceremony witness role (notary, family, designated person, or institutional partner) cryptographically attests to the enrollment session's integrity — signing a Pedersen commitment to the session record — while seeing only the fact of enrollment, not the biometric content.

---

## §1. The witness problem

Everest 11 (Enrollment Ceremony Spec) specifies that the principal produces their handwriting and voice-transcription templates under witness observation. The witnesses' presence is the ceremony's anti-substitution mechanism: they attest that *this principal, the one I know*, produced these templates, and that they appeared uncoerced at the time.

But the ceremony produces templates — handwriting kinematics, voice-transcription embeddings — that are sensitive. A witness should not walk away with a copy of the principal's handwriting vectors or voice-transcription data. They should attest to **the fact** of enrollment, not its details.

Calm Witness v0 solves this via **selective disclosure of a cryptographic commitment**. The witness signs not the templates themselves, but a Pedersen commitment to a hash of the enrollment session record — which includes the principal's identity, the witness's identity, the ceremony timestamp, and the hash of the template artifacts, but not the templates themselves.

This keeps the witness's role clear: **I attest that the principal *I know* participated in this ceremony on this date, and I did not observe coercion.** The witness learns no biometric content and no details beyond the ceremony's occurrence.

---

## §2. Witness tiers: a three-layer model

v0 defines three witness tiers, in increasing order of legal weight and decreasing order of local availability.

### Tier 1: Notary Public

A licensed notary public conducts a one-page attestation ceremony, separate from the biometric ceremony.

**What they see:**
- The principal's legal identity (photo ID verified).
- The fact that an enrollment ceremony occurred on a specific date at a specific address.
- A one-page attestation document stating: "On [date] at [time] at [address], [principal legal name] appeared before me and declared that they are participating in a Calm Witness enrollment ceremony. I did not observe coercion."
- A Pedersen commitment C = g^enrollment_record · h^r (the same commitment the principal signed).
- A machine-readable reference to the commitment (e.g., a QR code or hex string).

**What they do NOT see:**
- The principal's biometric templates (handwriting strokes, voice-transcription embeddings).
- The contents of any self-report or mood samples.
- The master private key or any other vault secret.
- The details of the ceremony beyond the date, time, and location.
- Any chain records other than the commitment hash.

**What they sign:**
The notary attaches their official seal to the one-page document and, using their notary signing key (held on a hardware token for v1+), signs the Pedersen commitment over a structured field:

```
{
  "kind": "enrollment.notary_attestation",
  "notary_legal_name": "...",
  "notary_commission_id": "...",
  "jurisdiction": "US-CA",
  "enrollment_record_hash": "...",
  "commitment": "C = g^{enrollment_record} · h^{r}",
  "commitment_signature": <notary-signed hex>,
  "timestamp": "2026-05-20T14:30:00Z",
  "notary_declares_uncoerced": true
}
```

The notary appends this to the principal's vault chain as a `kind: "enrollment.notary_attestation"` record. This record is part of the public chain — a third party verifying the principal's Calm Witness proofs can check that a licensed notary attested to the commitment.

**Legal weight:**
In US practice, a notarized document carries presumption of regularity: the notary is a state-issued official with fiduciary duties and professional liability. This tier is the **default for any principal expecting their Calm Witness proofs to be used as evidence in a financial, governmental, or legal proceeding**.

### Tier 2: Designated Person (Family / Close Contact)

A person the principal selects — spouse, parent, adult child, close friend, long-term business partner — witnesses the ceremony in person and signs a declaration of presence and uncoercion.

**What they see:**
- The principal's face and voice during the ceremony.
- The ceremony environment (room, equipment, absence of obvious coercion).
- The ceremony's duration (~60 minutes).
- The fact that the principal completed the ceremony and appeared in their declared baseline state.
- A Pedersen commitment to the enrollment session record.

**What they do NOT see:**
- The actual handwriting strokes (the kinematic vectors, not the visual glyphs).
- The voice-transcription embeddings or word-timing vectors.
- The contents of the self-report prompts or the principal's actual responses.
- The vault's other records or the principal's biometric history.
- How the templates were computed or what features they contain.

**What they sign:**
Using their CredexAI VC or a hardware-token key, the designated witness signs:

```
{
  "kind": "enrollment.witness_attestation",
  "witness_legal_name": "...",
  "witness_credexai_vc_id": "...",
  "relationship_to_principal": "spouse|parent|child|friend|colleague",
  "presence_declaration": "I was physically present at the ceremony on [date] from [time] to [time] and observed [principal name] complete the enrollment ceremony.",
  "coercion_declaration": "I did not observe any signs of coercion, duress, or undue pressure on [principal name]. They appeared to be proceeding voluntarily.",
  "commitment": "C = g^{enrollment_record} · h^{r}",
  "commitment_signature": <witness-signed hex>,
  "timestamp": "2026-05-20T14:30:00Z"
}
```

**When to use this tier:**
- When the principal has strong local relationships and wants higher recall (a spouse or parent is less likely to be mistaken about the principal's identity or state than a government notary with a 15-minute interaction).
- When a notary is unavailable or when the principal values the witness's deeper knowledge of their baseline state.
- As a complement to Tier 1 for multi-witness enrollment (see §4, Multi-Witness Aggregation).

**Legal weight:**
Lower than Tier 1, but not negligible. The witness's identity is publicly bound to their CredexAI VC, and any later claim that they were coerced becomes a second attestation (Everest 23: Recovery From Total Enrollment Loss). Multi-witness aggregation (Tier 2 + Tier 1) provides resilience.

### Tier 3: Calm-Pact-Aligned Institutional Partner

A Calm Witness operator, or another autonomous-AI-collective member, with a CredexAI VC (organizational identity) can serve as a witness via a secured video link or in-person presence.

**What they see:**
- The principal's identity assertion (CredexAI VC binding).
- The ceremony's occurrence, duration, and outcome (completed / aborted).
- A Pedersen commitment to the enrollment session record.
- **Optionally:** real-time video of the ceremony (if video infrastructure is available and the principal consents) — in this case they see what Tier 2 sees.

**What they do NOT see:**
- Biometric content (same as Tier 2).
- The principal's self-report details or mood states.
- Vault records beyond the commitment.

**What they sign:**
Using their organizational CredexAI VC, the institutional witness signs:

```
{
  "kind": "enrollment.institutional_witness_attestation",
  "witness_organization": "Calm Witness Operator (instance X) / CredexAI Org Y",
  "witness_credexai_vc_id": "...",
  "enrollment_record_hash": "...",
  "commitment": "C = g^{enrollment_record} · h^{r}",
  "commitment_signature": <org-signed hex>,
  "timestamp": "2026-05-20T14:30:00Z",
  "institutional_attestation": "Organization X attests that the enrollment ceremony concluded on [date] at [time] for principal [name]. The Pedersen commitment provided was signed by [principal's operator] and represents the enrollment session record hash."
}
```

**When to use this tier:**
- When the principal has no local witnesses available (isolated, traveling, or has consciously severed local relationships).
- When institutional continuity is valuable (a Calm operator attesting to a principal's enrollment carries weight for other Calm operators).
- As part of a multi-witness quorum for high-stakes proofs.

**Legal weight:**
Institutional; the witness's identity is cryptographically bound to a Calm organization and is auditable. Not as strong as Tier 1 alone, but stronger than Tier 2 alone when combined with an institutional quorum policy.

---

## §3. The witness does NOT see: a strict list

To underline what is kept private, here is what the witness explicitly does **not** receive:

- **Handwriting templates.** Not the kinematic vectors. Not the visual glyphs. Not even a rendered sample. (The witness sees the principal's hand moving on a stylus tablet, but does not receive the artifact.)
- **Voice-transcription embeddings.** Not the word-timing vectors. Not the transcript. Not anything derived from the audio. (The witness may hear the principal speaking but does not receive the transcript or its digital representation.)
- **Per-state baseline features.** Not the affect vocabulary. Not the self-report prompts or answers. Not mood-state labels or scores.
- **Biometric distance thresholds.** Not τ (tau), the per-principal threshold for "match." The witness does not learn how sensitive the principal's biometric matching is tuned.
- **Vault history.** Not prior self-reports. Not prior enrollment records. Not consent records. Not any other chain entry.
- **Master private key or identity key.** The witness never has access to the principal's cryptographic secrets.
- **Template encryption keys.** Even if the witness later suspects the principal was coerced, they cannot decrypt the templates — keys are held by the principal (or, in escrow, by a trusted third party who is not the witness).

---

## §4. Multi-witness aggregation: quorum and resilience

v0 permits a principal to enroll with multiple witnesses simultaneously. All witness signatures are recorded in the chain.

**Quorum policies:**
A verifier (a counterparty or a Calm operator verifying the principal's proof) can impose a quorum policy:
- "At least 1 Tier 1 witness (notary)."
- "At least 1 Tier 1 AND at least 1 Tier 2 (family or institutional)."
- "All N witnesses must be non-revoked."

**Why multiple witnesses:**
- **Resilience.** If one witness later revokes (Everest 23: Witness Revocation), the proof may still stand if other witnesses remain.
- **Cross-corroboration.** A notary attests to the legal fact; a family member attests to knowing the principal and observing their baseline state. Together they corroborate identity and voluntary participation more strongly than either alone.
- **Institutional + local.** The principal can enroll with both a Tier 2 (family) and a Tier 3 (Calm operator), combining local knowledge with institutional continuity.

**Witness voting:**
If the principal uses N witnesses and one witness later revokes their attestation, downstream verifiers see N-1 active attestations. Verifiers with a quorum policy of "≥2" would still succeed; verifiers requiring "the notary specifically" would fail.

---

## §5. What the witness signs: the commitment structure

Each witness receives and signs the same Pedersen commitment:

```
enrollment_record = {
  ceremony_id,           // unique UUID for this ceremony
  ceremony_ts,           // timestamp from Roughtime
  principal_legal_name_hash,    // H(legal name), not the name itself
  witness_legal_name_hash,      // H(witness name), not the name
  ceremony_artifacts_root_hash  // H(all templates || all commitments)
}

r = fresh randomness (Zp)

C = g^{enrollment_record} · h^{r}  // Pedersen commitment on the same Ed25519 group as Calm Pact
```

The witness does not see the plaintext `enrollment_record`; they see only the commitment C. But they attest that:
1. They observed the ceremony happen (attesting to ceremony_ts).
2. They observed the principal (attesting to principal_legal_name_hash matching the principal they know).
3. They did not observe coercion.

The witness's signature over C is what binds their attestation to the enrollment. If an adversary later tries to alter the enrollment_record, the commitment C no longer opens to it — and any verifier checking the witness signature will detect the tampering.

---

## §6. Anti-coercion safeguards: the witness's duty

Each witness — regardless of tier — must individually attest in writing or digitally:

> "I declare that I have not been coerced or pressured to sign this attestation. My signature reflects my honest observation."

This is **not** cryptographically enforced (you cannot prove someone is not coerced), but it is a formal declaration that the witness can later revoke if they were in fact coerced. If a Tier 2 witness later reports that the principal coerced them into signing, that revocation (Everest 23) is appended to the chain, and downstream verifiers can account for it.

For Tier 1 (notary), the anti-coercion duty is implicit in the notary's professional obligations: a notary who falsely attests to witnessing a signature faces revocation of their commission.

---

## §7. Witness revocation: later attestation

A witness can later sign a revocation record:

```
{
  "kind": "enrollment.witness_revoke",
  "original_witness_attestation_hash": "...",
  "witness_legal_name": "...",
  "revocation_reason": "I was coerced / I was mistaken / I did not actually observe the ceremony / [other]",
  "revocation_signature": <witness-signed hex>,
  "timestamp": "..."
}
```

Appending this record to the chain signals that the witness no longer stands by their original attestation. Verifiers can then:
- Reject proofs that depend on this witness's signature.
- Request a fresh, non-revoked witness.
- Lower the assurance level of the principal's Calm Witness proofs.

**Critical:** a revocation does NOT invalidate the principal's existing Calm Witness proofs that were issued *before* the revocation. The witness can only revoke their own attestation, not the principal's chain. But forward-looking counterparties can require non-revoked witnesses, which effectively creates a "proof freshness" requirement (Everest 70: Replay Defense).

---

## §8. Witness identity binding: CredexAI VCs

All witness signatures are bound to a CredexAI-issued Verifiable Credential:
- **Tier 1 (Notary):** a notary's VC issued by their state (e.g., California Secretary of State), containing notary commission ID, jurisdiction, and expiration date.
- **Tier 2 (Designated Person):** the witness brings their own CredexAI VC (issued by Calm's identity infrastructure or an equivalent), with legal name, and optionally relationship metadata (spouse, parent, friend).
- **Tier 3 (Institutional):** an organizational VC issued to a Calm operator or autonomous-AI-collective member.

When a verifier checks a witness signature, they:
1. Verify the signature cryptographically.
2. Verify the witness's VC is current and issued by a trusted VC issuer.
3. Cross-reference the witness's legal name in the VC with the commitment hash (which contains witness_legal_name_hash).

If the VC has expired or been revoked, the witness signature is no longer valid, even if cryptographically correct.

---

## §9. Notary-specific mechanics (US-focused)

For Tier 1 witnesses in the US:

**Notarial certificate:**
The notary produces a traditional notarial certificate (the one-page attestation document), which is recorded as a separate JSONL entry:

```
{
  "kind": "enrollment.notary_certificate",
  "notary_legal_name": "...",
  "notary_commission_id": "CA-12345678",
  "notary_jurisdiction": "California",
  "notary_commission_expiration": "2028-06-30",
  "ceremony_date": "2026-05-20",
  "ceremony_location_address": "123 Oak Street, Berkeley, CA 94701",
  "notarial_seal_hash": "H(notary seal image)",
  "document_signature_image_hash": "H(notary signature on document)",
  "timestamp": "..."
}
```

This certificate is stored separately from the witness_attestation record, allowing verifiers to conduct independent notary-commission lookups if needed (e.g., to verify that the notary was licensed in the correct jurisdiction on the ceremony date).

**Cross-jurisdiction acceptance:**
Everest 79 (Cross-Jurisdiction Legality Matrix) defines which jurisdictions accept notarized Calm Witness enrollments as evidence. v0 ships with a US-only notary acceptance table; international notarization will require bilateral legal review.

---

## §10. Witness workflow: when and how

**At ceremony close (Everest 11, §I):**

1. The principal's Calm operator completes the biometric ceremony and seals the templates (§H of Everest 11).
2. The operator computes `enrollment_record = {ceremony_id, ceremony_ts, principal_legal_name_hash, ...}`.
3. The operator computes the Pedersen commitment C = g^{enrollment_record} · h^{r}.
4. The operator displays C on a screen or prints it on a one-page document (with QR code or hex).
5. Each witness, in turn, uses their hardware-token signing key to sign C.
6. The operator appends a `kind: "enrollment.witness_attestation"` (or `notary_attestation` for Tier 1) record to the chain per witness.
7. The witness receives a signed receipt or blockchain confirmation.

**Total time:** ~3 minutes per witness (§I of Everest 11).

---

## §11. Failure cases and mitigations

| Failure | What happens | Mitigation |
|---|---|---|
| Witness does not appear | Ceremony aborts (Everest 11, §8) or completes self-witnessed (lower assurance) | Re-enrollment with available witnesses |
| Witness claims later coercion | Witness revocation appended to chain (§7) | Verifiers require non-revoked witnesses; principal can re-enroll with new witnesses (Everest 23) |
| Witness VC has expired | Witness signature still valid cryptographically but VC check fails | Witness must renew VC; principal can re-enroll or provide a fresh witness attestation from a current VC holder |
| Notary commission revoked between ceremony and verification | Notary attestation is valid at ceremony-time but no longer valid at verify-time | Counterparties should check notary status at verification time; v1+ may require timestamp-proof of notary status at ceremony time |
| Multiple witnesses, all revoke | No active witness signatures remain | Everest 23 (Recovery From Total Enrollment Loss) — principal re-enrolls with new witnesses |
| Principal was actually coerced, but witness did not detect | Cryptography cannot solve this; witness signatures reflect honest observation, not truth | Everest 23: duress-disclosure mechanism (bank_teller_note) allows principal to later signal coercion |

---

## §12. What the witness does NOT sign

The witness does **not** sign:
- The biometric templates themselves.
- Any predicate or consent record.
- Any prior or future chain entries.
- Any self-report content.
- Any acknowledgment of understanding the technical protocol (that is the operator's responsibility, not the witness's).

The witness signs **only** the commitment to the session record. This minimal scope is what keeps the witness's role clear and their exposure limited.

---

## §13. Acceptance test

This document defines the witness protocol for v0. The acceptance test is:

1. A principal completes Everest 11 (Enrollment Ceremony Spec) with at least one witness present.
2. The witness computes or receives the Pedersen commitment C to the enrollment session record.
3. The witness signs C using their hardware token (notary commission key for Tier 1; CredexAI VC for Tiers 2 and 3).
4. The operator appends the witness's signature to the vault chain as a `kind: "enrollment.witness_attestation"` (or `notary_attestation`) record.
5. A verifier running `calm-witness verify-chain` confirms the witness signature is valid and the witness's VC (if applicable) is current.
6. The verifier can audit the witness's identity and role without learning any biometric content.

A successful run produces at least one verifiable witness attestation, and the principal's later Calm Witness proofs can cite the witness's signature as part of their enrollment integrity proof.

---

— Calm, 2026-05-20
