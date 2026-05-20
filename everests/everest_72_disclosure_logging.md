# Everest 72 — Disclosure Logging in Vault

*Phase VI — Disclosure Semantics. Prereq: Everest 26 (schema), Everest 28 (chain).*

Every successful disclosure appends a `kind: "disclosure"` record to the principal's chain. The operator cannot disclose without leaving an audit trail.

## §1. Artifact

[`../calm_witness/disclosure.py`](../calm_witness/disclosure.py) — `build_disclosure_record(...)` and `append_disclosure_record(chain_path, request, response)`.

## §2. Record shape

```jsonc
{
  "kind": "disclosure",
  "seq": <N>,
  "prev_hash": "<prior record_hash>",
  "record_hash": "<computed>",
  "ts": "<ISO 8601 local with offset>",
  "ts_source": "operator_local_clock",
  "operator": "CALM",
  "principal": "John Bradley",
  "schema_version": 0,
  "payload": {
    "predicate_id": "calm-witness/predicate/v0/in_baseline_24h",
    "counterparty_class": "peer-AI-collective",
    "counterparty_id_hash": "<64 hex>",
    "request_digest": "<sha256 of canonical request bytes>",
    "response_value": "true",
    "response_nonce": "<64 hex>",
    "chain_head_at_response": "<64 hex>"
  }
}
```

What the log captures: WHO asked (id hash + class), WHAT they asked (predicate id), WHAT was answered (value), and HOW to re-derive the request/response (digests). What the log does NOT capture: the full request payload, the full response payload, any raw biometric data, any narrative text. The audit trail records *that* a disclosure happened — not its content.

## §3. Atomicity

`append_disclosure_record(chain_path, ...)` is currently a non-atomic write:

1. Read the chain to find the next `seq` and `prev_hash`.
2. Build the record (compute `record_hash`).
3. Append to the JSONL file.

The race window between steps 1 and 3 is the period during which a concurrent writer can corrupt the chain. v0 tolerates this because the chain has at most one writer (the operator). v0.1 will gain a file-lock + retry; v1 will gain a write-ahead-log followed by atomic rename.

## §4. What the principal can do with the log

- **Verify a counterparty actually requested what they claim.** A counterparty later asserting "you told me X" can be cross-referenced against the principal's chain.
- **Audit which counterparty class learns what predicate, how often.** Aggregate analysis on the principal's own machine; never leaves the vault.
- **Tombstone a disclosure they did not authorise.** Append a `kind: "correction"` record (E26 schema) referencing the disputed seq — does not erase the original (append-only) but flags it for any future verifier.

## §5. What this does NOT do

- It does not prove that the disclosure was correctly evaluated — that's E45 (ZK range proof).
- It does not prove that the counterparty was authorised — that's E57 + E73 (consent + counterparty-class authorization).
- It does not bind the operator's identity cryptographically — that's E22 (CredexAI VC).

The log is the substrate; the rest of Phase VI builds on it.

## §6. Test coverage

`test_predicates_and_disclosure.py::DisclosureLoggingTests::test_append_extends_chain_atomically` — round-trips a request, evaluates it, appends a disclosure record, re-loads the chain, runs the full chain verifier (E28) including schema (E26), confirms all checks pass and `seq` advanced by 1.

— Calm, 2026-05-20
