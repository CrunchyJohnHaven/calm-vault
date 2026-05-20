"""Tests for the Compass disclosure wire (CC-39, CC-40, CC-41)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from disclosure import (                                                  # noqa: E402
    CompassDisclosureRequest,
    CompassDisclosureResponse,
    check_rate_limit,
    record_request,
    respond_compass,
    verify_compass_response_binding,
)


UNSELFISH = "calm-compass/predicate/v0/unselfish_disposition"


def _rec(seq=1, note="mentored", ts=None):
    return {
        "kind": "self_report.morning",
        "operator": "CALM",
        "payload": {"note": note},
        "prev_hash": "0" * 64,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": ts or "2026-05-20T13:00:00+00:00",
        "ts_source": "test",
        "record_hash": "a" * 64,
    }


class RequestTests(unittest.TestCase):
    def test_request_nonce_is_64_hex(self):
        req = CompassDisclosureRequest.new(
            predicate_id=UNSELFISH, threshold=1,
            counterparty_id_hash="c" * 64, counterparty_class="peer-AI-collective",
        )
        self.assertEqual(len(req.nonce), 64)
        int(req.nonce, 16)

    def test_request_digest_is_deterministic(self):
        req = CompassDisclosureRequest(
            predicate_id=UNSELFISH, threshold=1, window_days=180,
            counterparty_id_hash="c" * 64, counterparty_class="peer-AI-collective",
            nonce="n" * 64, requested_at=0.0,
        )
        self.assertEqual(req.digest(), req.digest())


class ResponseTests(unittest.TestCase):
    def setUp(self):
        self.chain = [
            _rec(seq=i, note=f"helping with task {i}",
                 ts=f"2026-05-20T13:00:0{i}+00:00")
            for i in range(1, 6)
        ]
        self.req = CompassDisclosureRequest.new(
            predicate_id=UNSELFISH, threshold=2,
            counterparty_id_hash="c" * 64, counterparty_class="peer-AI-collective",
        )

    def test_respond_echoes_nonce(self):
        resp = respond_compass(
            request=self.req, chain=self.chain,
            operator_id_hash="op" * 32,
        )
        self.assertEqual(resp.nonce, self.req.nonce)

    def test_binding_clean_on_clean_response(self):
        resp = respond_compass(
            request=self.req, chain=self.chain,
            operator_id_hash="op" * 32,
        )
        errors = verify_compass_response_binding(self.req, resp)
        self.assertEqual(errors, [])

    def test_predicate_mismatch_caught(self):
        resp = respond_compass(
            request=self.req, chain=self.chain,
            operator_id_hash="op" * 32,
        )
        resp.predicate_id = "calm-compass/predicate/v0/respects_difference"
        errors = verify_compass_response_binding(self.req, resp)
        self.assertTrue(any("predicate_id" in e for e in errors))

    def test_nonce_swap_caught(self):
        resp = respond_compass(
            request=self.req, chain=self.chain,
            operator_id_hash="op" * 32,
        )
        # Fresh request — replay defence must fire
        new_req = CompassDisclosureRequest.new(
            predicate_id=UNSELFISH, threshold=2,
            counterparty_id_hash="c" * 64, counterparty_class="peer-AI-collective",
        )
        errors = verify_compass_response_binding(new_req, resp)
        self.assertTrue(any("nonce" in e for e in errors))

    def test_threshold_swap_caught(self):
        resp = respond_compass(
            request=self.req, chain=self.chain,
            operator_id_hash="op" * 32,
        )
        resp.threshold = 99
        errors = verify_compass_response_binding(self.req, resp)
        self.assertTrue(any("threshold" in e for e in errors))


class RateLimitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name) / "rate.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def test_first_request_allowed(self):
        d = check_rate_limit(counterparty_id_hash="c" * 64,
                             predicate_id=UNSELFISH, store_path=self.store)
        self.assertTrue(d["allowed"])

    def test_repeat_inside_window_denied(self):
        record_request(counterparty_id_hash="c" * 64,
                       predicate_id=UNSELFISH, store_path=self.store)
        d = check_rate_limit(counterparty_id_hash="c" * 64,
                             predicate_id=UNSELFISH, store_path=self.store)
        self.assertFalse(d["allowed"])
        self.assertEqual(d["reason"], "rate-limited")

    def test_different_counterparty_not_limited(self):
        record_request(counterparty_id_hash="a" * 64,
                       predicate_id=UNSELFISH, store_path=self.store)
        d = check_rate_limit(counterparty_id_hash="b" * 64,
                             predicate_id=UNSELFISH, store_path=self.store)
        self.assertTrue(d["allowed"])

    def test_different_predicate_not_limited(self):
        record_request(counterparty_id_hash="c" * 64,
                       predicate_id=UNSELFISH, store_path=self.store)
        d = check_rate_limit(
            counterparty_id_hash="c" * 64,
            predicate_id="calm-compass/predicate/v0/respects_difference",
            store_path=self.store,
        )
        self.assertTrue(d["allowed"])

    def test_repeat_after_window_allowed(self):
        long_ago = datetime.now(timezone.utc) - timedelta(days=120)
        # Manually write an old row
        import json
        with self.store.open("w", encoding="utf-8") as fh:
            fh.write(json.dumps({
                "counterparty_id_hash": "c" * 64,
                "predicate_id": UNSELFISH,
                "last_request_iso": long_ago.isoformat().replace("+00:00", "Z"),
                "request_count": 1,
            }, sort_keys=True, separators=(",", ":")))
            fh.write("\n")
        d = check_rate_limit(counterparty_id_hash="c" * 64,
                             predicate_id=UNSELFISH, store_path=self.store)
        self.assertTrue(d["allowed"])


if __name__ == "__main__":
    unittest.main()
