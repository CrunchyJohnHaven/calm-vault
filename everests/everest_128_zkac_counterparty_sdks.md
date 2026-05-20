# Everest 128 | ZKAC Counterparty SDKs

Status: **DESIGN-BAGGED (Summit 128/300) 2026-05-20**

## Goal

Ship verify-only counterparty SDK contract in Go and JS matching Python `verify_zkac`. Full Go package deferred; JS composite stub ships in this bag.

## Acceptance

- Python reference: `~/CredexAI/calm_witness/zkac_verify.py::verify_zkac`
- API doc: `~/AllData/calm_vault_market/ZKAC_COUNTERPARTY_SDK_v0.md`
- Conformance: `~/CredexAI/calm_witness/schema/conformance/counterparty_sdk_v0.json` (6/6)
- Gate: `~/CredexAI/scripts/everest_128_zkac_counterparty_sdk_gate.py` exit 0
- No PII in logs; no third-party SaaS

## Deliverables

| Artifact | Path | Status |
| --- | --- | --- |
| API surface | `ZKAC_COUNTERPARTY_SDK_v0.md` | shipped |
| Normative spec | `ZKAC_COUNTERPARTY_SDK_SPEC_v0.md` | shipped |
| Python reference | `calm_witness/zkac_verify.py` | shipped |
| JS composite stub | `calm_witness/sdk-js/verify_envelope.mjs` | shipped |
| Go package | `calm_witness/sdk-go/` | follow-through |
| Conformance vectors | `schema/conformance/counterparty_sdk_v0.json` | shipped |

## Follow-through

Implement Go `Verify`/`VerifyComposite` under `calm_witness/sdk-go/` and extend JS stub with Witness-only bit-proof verification before Everest 129 server SDK integration.
