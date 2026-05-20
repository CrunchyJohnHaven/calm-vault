# Everest 29 — Genesis Block & Provenance

*Phase III — Self-Report Substrate. Prereq: Everest 28.*

The v0 chain genesis (`seq == 1`) is a plain `self_report.morning` record with `prev_hash == "0" * 64`. That gives structural genesis (a chain head can be re-walked back to it) but not **identity-bound** genesis — the `principal` and `operator` fields are free-text strings, not CredexAI VC commitments. This summit defines the on-chain artifact that binds the structural genesis to verifiable legal identity, namely a `kind: "genesis_attestation"` record appended once the principal's CredexAI VC exists (Everest 22).

## §1. The `genesis_attestation` record

```jsonc
{
  "seq": <N>,
  "kind": "genesis_attestation",
  "operator": "CALM",
  "principal": "John Bradley",
  "schema_version": 0,
  "ts": "<ISO 8601 with TZ offset>",
  "ts_source": "credexai_vc_issuance_ceremony",
  "prev_hash": "<record_hash of prior record>",
  "record_hash": "<computed>",
  "payload": {
    "genesis_record_hash": "e2c8a733...19a7f5",            // sha256 of seq=1
    "credexai_vc_hash": "<sha256 of the principal's CredexAI VC JSON-LD>",
    "principal_legal_name": "John Bradley",
    "principal_jurisdiction": "US-DE",                      // ISO 3166-2
    "operator_credential_hash": "<sha256 of operator's VC>",
    "issuer": "credexai",
    "issued_at": "<ISO 8601 with TZ offset>",
    "method": "did:credexai:v1",
    "transparency_log_inclusion": {                         // optional, lands with E30
      "log_id": "sigsum.calm-vault.org",
      "leaf_index": <int>,
      "inclusion_proof_path": "<base64>"
    }
  }
}
```

The Pedersen commitment lifecycle for the VC itself is handled by CredexAI (Everest 22); this record commits only to the hashes.

## §2. What this binds — and what it does not

**Binds:**
- The structural genesis hash (`seq=1.record_hash`) to a named legal person via the CredexAI VC.
- The operator (`"CALM"` here) to its own VC, so later disclosure records can be linked to a credentialed AI operator.
- A jurisdiction tag, which the cross-jurisdiction legality matrix (Everest 79) uses to gate predicate eligibility.

**Does not bind:**
- The biometric templates — those bind via Everest 22's enrollment-VC link, not here.
- Consent records — they bind via their own chain entries (Everest 8) and reference the VC hash from here for identity continuity.
- The chain head to a public transparency log — that lands in Everest 30.

## §3. Why a separate record, not retroactive edits to seq=1

Append-only chains cannot edit prior records. The v0 genesis was written before the VC ceremony could run. The `genesis_attestation` record is therefore a forward attestation:

> "I, the principal identified by VC hash X, attest that the record at hash Y (seq=1 in this chain) is my genesis."

A verifier walking the chain from genesis discovers the attestation later in the chain and binds the identity retroactively without rewriting history. Any later editor cannot insert a counterfeit `genesis_attestation` because the chain's structural integrity (Everest 28) prevents insertion without breaking `prev_hash`, and the attestation's `credexai_vc_hash` must verify against a real VC at the named time of issuance.

## §4. Verifier behaviour (current and target)

| Capability | Current (E28) | After E29 + E22 |
|---|---|---|
| Structural chain integrity | ✓ | ✓ |
| Schema conformance | ✓ (E26) | ✓ |
| Genesis bound to legal identity | — | required |
| Disclosure records linked to operator VC | — | required |
| Cross-jurisdiction predicate gating | — | possible (with E79 table) |

The `calm-witness verify-chain` CLI will gain a `--require-genesis-attestation` flag (lands with Everest 22). When set, the CLI walks the chain looking for a `genesis_attestation` record; absent it, the CLI exits non-zero with reason "genesis not identity-bound."

## §5. Failure modes added to the catalogue

- **FM-46** — Genesis attestation written before VC issuance. Detect: `credexai_vc_hash` does not resolve. Respond: treat chain as v0-only; do not accept disclosure requests requiring legal-identity binding.
- **FM-47** — Multiple competing `genesis_attestation` records for the same principal. Detect: more than one such record before any `correction` tombstone. Respond: chain is suspect; manual review.
- **FM-48** — Cross-principal contamination (e.g., a non-Bradley VC binds to this chain's genesis). Detect: VC subject hash ≠ principal name's expected commitment. Respond: hard fail; do not issue any proofs.

These extend the Everest 9 Failure-Mode Catalogue.

## §6. Acceptance test

The `genesis_attestation` kind is in the v0 schema registry (Everest 26). The validator (`_validate_genesis_attestation`) requires `genesis_record_hash`, `credexai_vc_hash`, and `principal_legal_name`, with hex format validation on the two hash fields. The chain currently has zero `genesis_attestation` records, which is correct — the prereq (Everest 22 — CredexAI VC issuance) has not bagged. When it bags, appending the first `genesis_attestation` record will be the runtime acceptance test for this summit.

## §7. Cross-reference

- [Everest 22 — Enrollment → CredexAI VC](../ZKBB_USER_EVERESTS_100.md) (Phase II, not yet bagged) — produces the VC this record commits to.
- [Everest 28 — Hash-Chain Construction & Verification](everest_28_chain_verifier.md) — provides the structural integrity this rides on.
- [Everest 26 — JSONL Schema v0](everest_26_jsonl_schema_v0.md) — registers the `genesis_attestation` kind.
- [Everest 9 — Failure-Mode Catalogue](everest_09_failure_mode_catalogue.md) — receives FM-46/47/48.
- [Everest 79 — Cross-Jurisdiction Legality Matrix](everest_79_cross_jurisdiction_legality_matrix.md) — uses the jurisdiction tag.

— Calm, 2026-05-20
