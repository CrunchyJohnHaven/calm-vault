# Everest 69 — Counterparty Identity Binding

*Phase VIII — Disclosure · Prereq: Everest 22 (CredexAI Credential Issuance), Everest 68 (Operator Identity Binding).*

## Acceptance (verbatim)

C presents its CredexAI VC; O records it; disclosure is C-identity-bound.

---

## Summary

A counterparty (C) presents its CredexAI Verifiable Credential (VC) when requesting disclosure. The operator (O) verifies C's VC signature against CredexAI's issuer key, records the VC fingerprint in the chain, and computes a Pedersen commitment to C's Ed25519 public key. This commitment is folded into the Σ-PoK context (Everest 101 + 75), so a proof issued for one C cannot be relayed to a different C without breaking verification. Relay-to-different-C is **cryptographically rejected**.

---

## 1. Wire format additions

**DisclosureRequest** (Everest 66):
- Add `counterparty_vc_jws: str` — the counterparty's CredexAI VC, JWS-signed.

**DisclosureResponse** (Everest 67):
- Add `counterparty_vc_fingerprint: str` — SHA-256(canonicalised VC).
- Add `counterparty_id_commitment_hex: str` — Pedersen(C's Ed25519 public key bytes; blinding).

---

## 2. Operator (O) flow

1. **Receive request** with `counterparty_vc_jws`.
2. **Parse and verify VC signature** against CredexAI's published Ed25519 issuer key.
3. **Check VC not revoked** (online or cached revocation list).
4. **Extract C's public key** from VC's `credentialSubject.calmWitness.masterPubKey`.
5. **Compute VC fingerprint**: `sha256(canonicalised_vc_bytes)`.
6. **Record in chain**: append `counterparty_vc_recorded` entry to `user_state.jsonl`.
7. **Generate blinding**: `blinding_hex = secrets.token_hex(32)`.
8. **Compute Pedersen commitment** to C's public key bytes (as integer) with blinding.
9. **Fold commitment into context** by extending `build_context()` to include `counterparty_id_commitment_hex`.
10. **Issue response** with commitment and updated context.

---

## 3. Counterparty (C) verification

When C receives the response:

1. **Extract commitment** from response.
2. **Verify Σ-PoK** with updated context that includes the commitment.
3. **Implicit opening check**: if the commitment was tampered or belongs to a different C, the context hash changes and the Σ-PoK fails.

---

## 4. Relay defense

A relay attack: attacker obtains proof intended for C1, sends it to O falsely claiming to be C2.

**Mitigation**: The proof's context was built with C1's `counterparty_id_commitment`. When C2 tries to verify, C2 recomputes the context using its own identity. The context hashes do not match (because C1_pubkey ≠ C2_pubkey), so the Σ-PoK fails.

**Relay-to-different-C is cryptographically rejected.**

---

## 5. Refusal floor

The counterparty VC is subject to the same refusal floor as the principal's VC (Everest 22 §9):

- VC must NOT carry claims about the counterparty's protected-category attributes.
- VC must NOT carry claims about the principal's protected-category attributes.

Operator rejects any VC carrying forbidden claims before recording.

---

## 6. Chain records

**counterparty_vc_recorded** (new kind):
```json
{
  "kind": "counterparty_vc_recorded",
  "counterparty_principal_legal_name": "Bob Smith",
  "counterparty_did": "did:calm:<id>",
  "counterparty_vc_fingerprint": "sha256_hex",
  "vc_expiration": "2028-05-20T14:40:00Z",
  "vc_issuer": "did:credexai:v1:<issuer>",
  "requested_at_utc": "2026-05-20T13:25:00Z"
}
```

---

## 7. Cross-links

- **Everest 22**: VC issuance schema and issuer signature.
- **Everest 68**: operator identity binding (counterparty-side dual).
- **Everest 70**: replay defense via nonce; counterparty binding complements it.
- **Everest 72**: disclosure logging includes counterparty_vc_fingerprint.

---

## 8. Threat model

| Threat | Mitigation |
|--------|------------|
| VC forged | issuer signature verification fails |
| Response relayed to different C | commitment bound into Σ-PoK context; verification fails |
| VC tampered in transit | JWS signature fails |
| Protected-category claims in VC | refusal floor preflight rejects |

---

## 9. Acceptance test

1. O verifies C's VC signature against CredexAI issuer key.
2. O extracts C's public key from VC.
3. O computes Pedersen commitment to C's pubkey.
4. O records VC fingerprint in chain.
5. Commitment is bound into Σ-PoK context.
6. Relay-to-different-C fails: Σ-PoK verification fails.
7. Tampered commitment fails: context hash mismatch.
8. VC signature mismatch fails: issuer verification fails.

Gate: `~/CredexAI/scripts/everest_69_zkbb_counterparty_identity_binding_gate.py` (exit 0 = green).

---

— Calm, 2026-05-20
