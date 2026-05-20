# Everest 22 — Enrollment → CredexAI Credential Issuance

*Phase II — Capture & Enrollment. Prereq: Everest 16 (Template Encryption), Everest 20 (Witness Protocol).*

A successful enrollment ceremony culminates in a CredexAI-issued verifiable credential (VC) that binds the principal's legal identity, the enrolled template commitments, the witness signatures, and the operator's identity into a single signed object. The VC is the linchpin between Calm Witness (which attests state) and CredexAI (which attests identity).

## §1. Artifact (design only — implementation lands at v0.1 with CredexAI integration)

Spec doc; the binding code path lives at `credexai/sdks/python/credexai/zkac.py` (CredexAI SDK). Calm Witness consumes the VC; it does not issue it.

## §2. The VC shape

```jsonc
{
  "@context": ["https://www.w3.org/2018/credentials/v1",
               "https://credexai.org/contexts/calm-witness/v0"],
  "type": ["VerifiableCredential", "CalmWitnessEnrollment"],
  "issuer": "did:credexai:v1:<issuer-key-thumbprint>",
  "issued_at": "<ISO 8601>",
  "expires_at": "<ISO 8601 (default: issued_at + 5 years)>",
  "credentialSubject": {
    "id": "did:calm:<principal-stable-id>",
    "principal_legal_name": "John Bradley",
    "principal_jurisdiction": "US-DE",
    "enrollment_ceremony": {
      "ceremony_record_hash": "<sha256 of the kind:enrollment chain record>",
      "ceremony_ts": "<ISO 8601 of ceremony completion>",
      "ceremony_address_commit": "<sha256 over address+salt; address itself not in VC>"
    },
    "template_commitments": {
      "handwriting:calm":        "<Pedersen commitment, 32 bytes hex>",
      "handwriting:creative":    "<32 hex>",
      "handwriting:focused":     "<32 hex>",
      "voice-transcription:calm":      "<32 hex>",
      "voice-transcription:creative":  "<32 hex>",
      "voice-transcription:focused":   "<32 hex>"
    },
    "witness_attestations": [
      {"witness_did": "did:credexai:v1:<witness-1-key>", "sig": "<Ed25519 hex>"},
      {"witness_did": "did:credexai:v1:<witness-2-key>", "sig": "<Ed25519 hex>"}
    ],
    "operator_did": "did:credexai:v1:<calm-operator-key>",
    "protocol": "calm-witness/v0"
  },
  "proof": {
    "type": "Ed25519Signature2020",
    "created": "<ISO 8601>",
    "verificationMethod": "did:credexai:v1:<issuer-key>",
    "proofPurpose": "assertionMethod",
    "proofValue": "<base64 Ed25519 sig over the canonicalised credential>"
  }
}
```

The VC follows W3C VC Data Model 1.1 (Rec, 2022). The `@context` extension at `credexai.org/contexts/calm-witness/v0` defines the Calm-Witness-specific terms.

## §3. What the VC binds (and why each binding matters)

| Field | Binds to | Why |
|---|---|---|
| `principal_legal_name` | the human responsible for consent | establishes legal accountability for issued disclosures |
| `principal_jurisdiction` | applicable law | gates cross-jurisdiction predicate eligibility (E79) |
| `ceremony_record_hash` | the enrollment chain entry | proves the ceremony actually happened |
| `template_commitments` | the AEAD-wrapped templates in the vault | the operator cannot substitute templates after enrollment |
| `witness_attestations` | the human witnesses' signatures | substitution resistance (FM-10) |
| `operator_did` | the AI operator | a different operator cannot impersonate Calm without re-enrollment |

What the VC does NOT bind:
- The principal's address (only a salted commitment to it).
- The principal's biometric features themselves (only Pedersen commitments).
- The contents of any individual self-report record.

## §4. Verification flow

A counterparty receiving a Calm Witness disclosure verifies the operator's identity by:

1. Fetching the operator's VC from the CredexAI DID resolver.
2. Confirming `proof.verificationMethod` resolves to a known CredexAI issuer key.
3. Confirming `proof.proofValue` verifies the canonicalised VC against the issuer key.
4. Confirming `expires_at` is in the future.
5. Confirming `credentialSubject.protocol == "calm-witness/v0"`.
6. Storing `sha256(canonicalised(VC))` as the operator-identity hash for the response binding (`operator_id_hash` field in [DisclosureResponse](../calm_witness/disclosure.py)).

Steps 1–5 are CredexAI's standard VC verification. Step 6 is Calm-Witness specific and produces the operator-identity hash already referenced throughout v0.

## §5. Composition with Everest 29

Everest 29 (Genesis Block & Provenance) requires a `kind: "genesis_attestation"` chain record after VC issuance. That record's `credexai_vc_hash` field is exactly `sha256(canonicalised(VC))` from step 6 above. The genesis attestation is the bridge between the structural chain (E28) and the legal-identity layer (E22).

## §6. Failure modes added to the catalogue

- **FM-49** — VC issued but never bound to chain via `kind: genesis_attestation`. Detect: chain walk passes but `--require-genesis-attestation` fails. Respond: chain is v0-only; no identity-bound disclosures.
- **FM-50** — Operator's VC expires mid-disclosure. Detect: `expires_at < now` at verification time. Respond: counterparty treats response as `refused`; operator should refresh VC.
- **FM-51** — Template commitments in VC do not match templates in vault. Detect: `kind: enrollment` record's commitments diverge from VC `template_commitments`. Respond: hard fail; suspected vault tampering or VC mis-issuance.

These extend Everest 9.

## §7. Out of scope for v0 (deferred to v1 / v2)

- **Multi-device VC consolidation.** A principal enrolling on N devices needs N VCs joined; the joining ceremony is Everest 24.
- **Operator-rotation VCs.** Replacing the AI operator (e.g., upgrading from one Claude version to another) without re-enrollment. The current v0 design re-runs the ceremony; v1 supports a delta-VC.
- **Witness-only re-issuance.** Replacing a single witness without re-enrolling templates. v0 requires a full re-ceremony.

## §8. Acceptance test

The acceptance criterion is integration with CredexAI's SDK. Until that integration ships:

1. `genesis_attestation` records pass schema validation (E26 — already true).
2. `disclosure.py`'s `operator_id_hash` field accepts a 64-hex value (— already true).
3. The placeholder hex flows end-to-end through `respond → verify_response_binding` without errors (— already covered by E67 tests).

When CredexAI integration ships:

4. A real VC's hash matches the genesis-attestation record's `credexai_vc_hash`.
5. A counterparty fetches the VC and verifies the operator's signature on a real `DisclosureResponse`.

— Calm, 2026-05-20
