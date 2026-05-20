#!/usr/bin/env python3
"""E70 — Replay defence via nonce binding.

Gate verifies that DisclosureResponse binding to DisclosureRequest via
nonce prevents replay attacks and enforces predicate integrity.

Assertions:
  1. Clean (request, response) pair passes verify_response_binding
  2. Swapped response.nonce triggers error containing 'nonce'
  3. Swapped response.predicate_id triggers error containing 'predicate_id'
  4. Different request (same predicate, new nonce) triggers error containing 'nonce'

Exit 0 if all 4 assertions hold; exit 1 otherwise.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# Stdlib only; add calm_witness to sys.path
calm_witness_path = Path(__file__).parent.parent / "calm_witness"
if str(calm_witness_path) not in sys.path:
    sys.path.insert(0, str(calm_witness_path))

from disclosure import DisclosureRequest, DisclosureResponse, respond, verify_response_binding
from predicates import P_IN_BASELINE_24H_ID
from verify_chain import canonical_record_hash


def _self_report(seq: int, prev_hash: str, ts: str) -> Dict[str, Any]:
    """Build a synthetic in-baseline chain record (test helper pattern)."""
    rec = {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {
            "affect": ["calm", "even-keeled"],
            "alarm": False,
            "known_health_issues": [],
            "note": "E70 gate test",
            "readiness": "ready_to_work",
            "restedness": "fully_rested",
            "sleep_hours": 8.0,
            "wake_time": "09:30",
        },
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": ts,
        "ts_source": "test",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    return rec


def main() -> int:
    """Run 4 assertions; exit 0 if all pass, 1 otherwise."""
    passed = 0
    failed = 0

    # Setup: synthetic baseline record
    rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
    chain_window = [rec]
    chain_head = rec["record_hash"]

    # Clean request
    req = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
        freshness_max_seconds=86400,
    )

    # Generate response
    resp = respond(
        req,
        chain_window=chain_window,
        chain_head=chain_head,
        operator_id_hash="b" * 64,
        operator_sign=None,
    )

    # Assertion 1: clean pair passes verify_response_binding
    print("ASSERTION 1: Clean (request, response) pair...", end=" ", flush=True)
    errors = verify_response_binding(req, resp)
    if not errors:
        print("PASS")
        passed += 1
    else:
        print(f"FAIL: {errors}")
        failed += 1

    # Assertion 2: swapped response.nonce triggers 'nonce' error
    print("ASSERTION 2: Swapped response.nonce...", end=" ", flush=True)
    resp_bad_nonce = DisclosureResponse(
        predicate_id=resp.predicate_id,
        value=resp.value,
        freshness_window_seconds=resp.freshness_window_seconds,
        nonce="f" * 64,  # wrong nonce
        chain_head=resp.chain_head,
        pedersen_commitment_hex=resp.pedersen_commitment_hex,
        sigma_proof_hex=resp.sigma_proof_hex,
        operator_id_hash=resp.operator_id_hash,
        operator_sig_hex=resp.operator_sig_hex,
    )
    errors = verify_response_binding(req, resp_bad_nonce)
    if any("nonce" in e for e in errors):
        print("PASS")
        passed += 1
    else:
        print(f"FAIL: no 'nonce' error in {errors}")
        failed += 1

    # Assertion 3: swapped response.predicate_id triggers 'predicate_id' error
    print("ASSERTION 3: Swapped response.predicate_id...", end=" ", flush=True)
    resp_bad_pred = DisclosureResponse(
        predicate_id="calm-witness/predicate/v0/biometric_match_within",  # wrong predicate
        value=resp.value,
        freshness_window_seconds=resp.freshness_window_seconds,
        nonce=resp.nonce,
        chain_head=resp.chain_head,
        pedersen_commitment_hex=resp.pedersen_commitment_hex,
        sigma_proof_hex=resp.sigma_proof_hex,
        operator_id_hash=resp.operator_id_hash,
        operator_sig_hex=resp.operator_sig_hex,
    )
    errors = verify_response_binding(req, resp_bad_pred)
    if any("predicate_id" in e for e in errors):
        print("PASS")
        passed += 1
    else:
        print(f"FAIL: no 'predicate_id' error in {errors}")
        failed += 1

    # Assertion 4: different request (same predicate, new nonce) triggers 'nonce' error
    print("ASSERTION 4: Different request (new nonce)...", end=" ", flush=True)
    new_req = DisclosureRequest.new(
        predicate_id=P_IN_BASELINE_24H_ID,
        counterparty_id_hash="a" * 64,
        counterparty_class="peer-AI-collective",
        freshness_max_seconds=86400,
    )
    # resp is bound to original req.nonce, not new_req.nonce
    errors = verify_response_binding(new_req, resp)
    if any("nonce" in e for e in errors):
        print("PASS")
        passed += 1
    else:
        print(f"FAIL: no 'nonce' error in {errors}")
        failed += 1

    # Summary
    print()
    print(f"PASS/FAIL: {passed}/4 assertions passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
