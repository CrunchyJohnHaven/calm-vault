# ZKAC Inter-Vault Attestation v0

**Everest 126 · 2026-05-20 · Prereq: 125**

One vault may attest to another principal's committed chain head without exporting either vault's record bodies. Claims are principal-authored only. Cross-principal comparison predicates are forbidden.

## §0 — Actors

| Actor | Role |
| --- | --- |
| Issuer vault (A) | Signs a bounded identity attestation |
| Subject principal | Named principal whose head is attested |
| Verifier | Checks digest, signature, and prohibited-key scan |

## §1 — Wire envelope

`wire_version`: `calm-vault/inter-attestation/v0`  
`kind`: `InterVaultAttestation`  
`claim_kind`: `prior_chain_head_confirmed` (v0 only)

Committed fields (64-hex where marked):

- `attesting_vault_fingerprint` (manifest heads only, no payloads)
- `issued_by_operator`
- `subject_principal_id` (stable id, not a display name)
- `subject_identity_fingerprint` = SHA-256(`principal_id:chain_head`)
- `attested_chain_head`
- `subject_vault_fingerprint` (same digest as identity fingerprint in v0)
- `issued_at_iso` (RFC3339 Z)
- `attestation_digest` = SHA-256(canonical content without digest field)
- `operator_signature` = `sha256:` + digest

## §2 — Privacy floor

Prohibited on the wire (hard reject at verify):

`user_state`, `chain_jsonl`, `records`, `payload`, `biometric`, `evidence`, `proof`, `disclosures`, `chain_body`, `vault_contents`.

Normative prose: [`INTER_VAULT_ATTESTATION_v0.md`](INTER_VAULT_ATTESTATION_v0.md) (Commitment-only witness, No chain leak, Principal attribution).

## §3 — Principal-authored only

The issuer vault attests one subject principal per message. The claim text is fixed to prior head confirmation. No predicate may compare two principals' states in one attestation (no cross-principal comparison).

## §4 — Reference implementation

| Artifact | Path |
| --- | --- |
| Module | `~/CredexAI/calm_witness/inter_vault.py` |
| Tests | `~/CredexAI/calm_witness/test_inter_vault.py` |
| Gate | `~/CredexAI/scripts/everest_126_zkac_inter_vault_gate.py` |

## §5 — Follow-through

**127:** Browser extension witness channel (separate Everest).

— Musk
