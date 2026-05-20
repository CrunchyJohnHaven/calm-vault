"""Tests for SUMMITs 241/256/276 (compute_budget, claim_protocol, emergency_stop).

Stripe verify (247) is not unit-tested here — it does live HTTP. Run manually with
STRIPE_API_KEY set to confirm.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from claim_protocol import bag_summit, claim_summit, is_claimed, list_active_claims
from compute_budget import (
    ComputeEvent,
    authorize_dispatch,
    budget_check,
    record_event,
    window_totals,
)
from emergency_stop import engage, gate_outbound, is_engaged, release


class ClaimProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.chain = Path(self.tmp.name) / "chain.jsonl"
        self.chain.touch()

    def tearDown(self):
        self.tmp.cleanup()

    def test_claim_then_list(self):
        claim_summit(247, "Operations", chain_path=self.chain)
        active = list_active_claims(self.chain)
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].summit_id, 247)

    def test_double_claim_rejected(self):
        claim_summit(247, "Operations", chain_path=self.chain)
        with self.assertRaises(ValueError):
            claim_summit(247, "Operations", chain_path=self.chain)

    def test_bagging_releases_claim(self):
        rec = claim_summit(247, "Operations", chain_path=self.chain)
        session_id = rec["payload"]["session_id"]
        bag_summit(247, "Stripe Verify", "Operations",
                   evidence_paths=["calm_operations/stripe_verify.py"],
                   session_id=session_id, chain_path=self.chain)
        active = list_active_claims(self.chain)
        self.assertEqual(len(active), 0)

    def test_claim_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            claim_summit(301, "Operations", chain_path=self.chain)
        with self.assertRaises(ValueError):
            claim_summit(0, "Operations", chain_path=self.chain)

    def test_expired_claim_not_active(self):
        # TTL of 0 minutes - expires immediately
        claim_summit(247, "Operations", chain_path=self.chain, ttl_minutes=0)
        future = datetime.now(timezone.utc) + timedelta(minutes=1)
        active = list_active_claims(self.chain, now=future)
        self.assertEqual(active, [])


class ComputeBudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Path(self.tmp.name) / "ledger.jsonl"

    def tearDown(self):
        self.tmp.cleanup()

    def _add(self, cost):
        record_event(ComputeEvent(
            ts_iso=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            provider="anthropic", operator_did="did:calm:test",
            model="claude-opus-4-7", input_tokens=1000, output_tokens=500,
            cost_usd=cost, purpose="test",
        ), ledger_path=self.ledger)

    def test_authorize_under_budget(self):
        d = authorize_dispatch(1.00, ledger_path=self.ledger)
        self.assertTrue(d["allowed"])

    def test_authorize_blocked_when_over(self):
        # Daily cap is $25; spend $30
        self._add(30.0)
        d = authorize_dispatch(1.00, ledger_path=self.ledger)
        self.assertFalse(d["allowed"])

    def test_window_totals(self):
        self._add(5.0)
        self._add(7.0)
        t = window_totals(ledger_path=self.ledger)
        self.assertAlmostEqual(t["daily"], 12.0, places=2)

    def test_budget_check_overall_ok(self):
        self._add(1.0)
        c = budget_check(ledger_path=self.ledger)
        self.assertEqual(c["overall"], "ok")

    def test_budget_check_soft_warn(self):
        # Daily cap is $25; 80% = $20. Spend $22 -> soft warn.
        self._add(22.0)
        c = budget_check(ledger_path=self.ledger)
        self.assertEqual(c["per_window"]["daily"], "SOFT-WARN")


class EmergencyStopTests(unittest.TestCase):
    def setUp(self):
        # Use tmp paths to avoid touching the real ~/.calm-vault
        self.tmp = tempfile.TemporaryDirectory()
        self.chain = Path(self.tmp.name) / "chain.jsonl"
        self.chain.touch()
        # Monkeypatch the state file to be tmp-local
        import emergency_stop as e
        self._orig_state = e.STATE_FILE
        e.STATE_FILE = Path(self.tmp.name) / "stop.state"

    def tearDown(self):
        import emergency_stop as e
        if e.STATE_FILE.exists():
            e.STATE_FILE.unlink()
        e.STATE_FILE = self._orig_state
        self.tmp.cleanup()

    def test_engage_then_status(self):
        r = engage(reason="manual test", chain_path=self.chain)
        self.assertTrue(r["engaged"])
        self.assertTrue(is_engaged())
        self.assertFalse(gate_outbound())

    def test_release_without_principal_signature_refused(self):
        engage(reason="test", chain_path=self.chain)
        r = release(principal_signed=False, chain_path=self.chain)
        self.assertFalse(r["released"])
        self.assertTrue(is_engaged())

    def test_release_with_principal_signature(self):
        engage(reason="test", chain_path=self.chain)
        r = release(principal_signed=True, chain_path=self.chain)
        self.assertTrue(r["released"])
        self.assertFalse(is_engaged())
        self.assertTrue(gate_outbound())

    def test_double_engage_idempotent(self):
        engage(reason="test1", chain_path=self.chain)
        r = engage(reason="test2", chain_path=self.chain)
        self.assertTrue(r["already_engaged"])


if __name__ == "__main__":
    unittest.main()
