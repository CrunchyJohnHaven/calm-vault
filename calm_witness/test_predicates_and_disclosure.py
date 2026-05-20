"""Tests for predicates (E55) + disclosure (E66, E67, E70, E72)."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from disclosure import (
    DisclosureRequest,
    DisclosureResponse,
    append_disclosure_record,
    build_disclosure_record,
    respond,
    verify_response_binding,
)
from predicates import (
    P_IN_BASELINE_24H_ID,
    PredicateValue,
    evaluate,
    in_baseline_24h,
)
from schema import validate_record
from verify_chain import canonical_record_hash, verify_chain


def _self_report(seq, prev_hash, ts, affect=("calm",), restedness="fully_rested", issues=()):
    rec = {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {
            "affect": list(affect),
            "alarm": False,
            "known_health_issues": list(issues),
            "note": "test",
            "readiness": "ready_to_work",
            "restedness": restedness,
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


class InBaselinePredicateTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)

    def test_true_with_clean_self_report(self):
        rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
        r = in_baseline_24h([rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.TRUE)
        self.assertEqual(r.predicate_id, P_IN_BASELINE_24H_ID)
        self.assertIsNotNone(r.freshness_window_seconds)

    def test_false_when_affect_outside_baseline(self):
        rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00", affect=("agitated",))
        r = in_baseline_24h([rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.FALSE)
        self.assertIn("affect", r.reason)

    def test_false_when_tired(self):
        rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00", restedness="tired")
        r = in_baseline_24h([rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.FALSE)
        self.assertIn("restedness", r.reason)

    def test_false_when_health_issues(self):
        rec = _self_report(
            1, "0" * 64, "2026-05-20T13:00:00+00:00", issues=("fever",)
        )
        r = in_baseline_24h([rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.FALSE)
        self.assertIn("health_issues", r.reason)

    def test_unknown_when_no_report_in_window(self):
        old = _self_report(1, "0" * 64, "2026-05-18T13:00:00+00:00")
        r = in_baseline_24h([old], now=self.now)
        self.assertEqual(r.value, PredicateValue.UNKNOWN)

    def test_refused_when_consent_denies(self):
        rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
        r = in_baseline_24h([rec], now=self.now, consent_record={"denied": True})
        self.assertEqual(r.value, PredicateValue.REFUSED)

    def test_evaluate_via_registry(self):
        rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
        r = evaluate(P_IN_BASELINE_24H_ID, chain_window=[rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.TRUE)

    def test_unknown_predicate_id_raises(self):
        with self.assertRaises(ValueError):
            evaluate(
                "calm-witness/predicate/v0/nonexistent",
                chain_window=[],
                now=self.now,
            )

    def test_real_morning_record_validates_baseline(self):
        # Use the exact shape John submitted this morning.
        rec = _self_report(
            1,
            "0" * 64,
            "2026-05-20T13:50:00+00:00",
            affect=("calm", "even-keeled", "curious"),
        )
        r = in_baseline_24h([rec], now=self.now)
        self.assertEqual(r.value, PredicateValue.TRUE)


class DisclosureWireTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
        self.rec = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
        self.req = DisclosureRequest.new(
            predicate_id=P_IN_BASELINE_24H_ID,
            counterparty_id_hash="a" * 64,
            counterparty_class="peer-AI-collective",
        )

    def test_request_nonce_is_64_hex(self):
        self.assertEqual(len(self.req.nonce), 64)
        int(self.req.nonce, 16)  # raises if non-hex

    def test_respond_echoes_nonce(self):
        resp = respond(
            self.req,
            chain_window=[self.rec],
            chain_head=self.rec["record_hash"],
            operator_id_hash="b" * 64,
        )
        self.assertEqual(resp.nonce, self.req.nonce)
        self.assertEqual(resp.value, "true")

    def test_replay_defence_catches_swapped_nonce(self):
        resp = respond(
            self.req,
            chain_window=[self.rec],
            chain_head=self.rec["record_hash"],
            operator_id_hash="b" * 64,
        )
        # Fresh request — same predicate, different nonce
        new_req = DisclosureRequest.new(
            predicate_id=P_IN_BASELINE_24H_ID,
            counterparty_id_hash="a" * 64,
            counterparty_class="peer-AI-collective",
        )
        errors = verify_response_binding(new_req, resp)
        self.assertTrue(any("nonce mismatch" in e for e in errors))

    def test_predicate_id_mismatch_caught(self):
        resp = respond(
            self.req,
            chain_window=[self.rec],
            chain_head=self.rec["record_hash"],
            operator_id_hash="b" * 64,
        )
        resp.predicate_id = "calm-witness/predicate/v0/biometric_match_within"
        errors = verify_response_binding(self.req, resp)
        self.assertTrue(any("predicate_id" in e for e in errors))

    def test_freshness_tolerance_enforced(self):
        # Clock-stable variant: build a response with a freshness_window known to
        # exceed the request tolerance and check verify_response_binding fires.
        # (Earlier formulation depended on wall-clock time and was flaky.)
        resp = DisclosureResponse(
            predicate_id=P_IN_BASELINE_24H_ID,
            value="true",
            freshness_window_seconds=7200,            # 2 hours
            nonce="n" * 64,
            chain_head="c" * 64,
            pedersen_commitment_hex="00" * 32,
            sigma_proof_hex="00" * 32,
            operator_id_hash="b" * 64,
            operator_sig_hex="",
        )
        strict_req = DisclosureRequest(
            predicate_id=P_IN_BASELINE_24H_ID,
            counterparty_id_hash="a" * 64,
            counterparty_class="financial",
            nonce="n" * 64,
            freshness_max_seconds=3600,                # 1 hour
        )
        errors = verify_response_binding(strict_req, resp)
        self.assertTrue(any("freshness" in e for e in errors))

    def test_disclosure_record_schema_valid(self):
        resp = respond(
            self.req,
            chain_window=[self.rec],
            chain_head=self.rec["record_hash"],
            operator_id_hash="b" * 64,
        )
        rec = build_disclosure_record(
            request=self.req,
            response=resp,
            seq=2,
            prev_hash=self.rec["record_hash"],
        )
        self.assertEqual(validate_record(rec), [])


class DisclosureLoggingTests(unittest.TestCase):
    def test_append_extends_chain_atomically(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "chain.jsonl"
            r1 = _self_report(1, "0" * 64, "2026-05-20T13:00:00+00:00")
            with p.open("w", encoding="utf-8") as fh:
                fh.write(json.dumps(r1, sort_keys=True, separators=(",", ":")))
                fh.write("\n")
            req = DisclosureRequest.new(
                predicate_id=P_IN_BASELINE_24H_ID,
                counterparty_id_hash="a" * 64,
                counterparty_class="peer-AI-collective",
            )
            resp = respond(
                req,
                chain_window=[r1],
                chain_head=r1["record_hash"],
                operator_id_hash="b" * 64,
            )
            appended = append_disclosure_record(p, req, resp)
            # Chain integrity holds end-to-end.
            with p.open("r", encoding="utf-8") as fh:
                records = [json.loads(line) for line in fh if line.strip()]
            checks = verify_chain(records, check_schema=True)
            self.assertTrue(all(c.ok for c in checks))
            self.assertEqual(appended["seq"], 2)
            self.assertEqual(appended["kind"], "disclosure")


if __name__ == "__main__":
    unittest.main()
