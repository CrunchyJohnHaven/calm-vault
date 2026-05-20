"""Additional tests for CT-04, CT-10, CT-11, CT-15, CT-21, CT-41, CT-46."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from chain_records import (
    build_tenancy_daily_check,
    build_tenancy_reply,
    canonical_record_hash,
)
from classify import classify, classify_and_route, is_response_seeking
from cohab_replay import COHAB_CLASS_FIXTURE, assert_cohab_class_unshippable
from cringe_gate import cringe_check
from precheck import precheck_tree
from well_known import build_assertion, generate_fleet


class WellKnownTests(unittest.TestCase):
    """CT-04 — .well-known/calm-tenancy.json generator."""

    def test_assertion_has_required_fields(self):
        a = build_assertion(domain="example.com")
        d = json.loads(a.to_json())
        for field in ("schema_version", "domain", "operator_did", "principal_did",
                      "mailbox", "sla", "cringe_rubric_version", "chain_head_at_publish",
                      "publish_ts", "well_known_signature"):
            self.assertIn(field, d)
        self.assertEqual(d["domain"], "example.com")
        self.assertEqual(d["mailbox"], "calm@example.com")
        self.assertEqual(d["sla"]["first_ack_seconds"], 600)

    def test_operator_did_uses_domain_slug(self):
        a = build_assertion(domain="the-creativity-machine.ai")
        self.assertIn("the-creativity-machine-ai", a.operator_did)

    def test_signature_present_even_in_placeholder_mode(self):
        a = build_assertion(domain="example.com")
        # placeholder is sha256 of canonical bytes; 64 hex chars
        self.assertEqual(len(a.well_known_signature), 64)

    def test_fleet_writes_one_file_per_domain(self):
        with tempfile.TemporaryDirectory() as td:
            domains_file = Path(td) / "owned.txt"
            domains_file.write_text("a.com\nb.com\nc.com\n", encoding="utf-8")
            out_dir = Path(td) / "out"
            written = generate_fleet(out_dir=out_dir, owned_domains_path=domains_file)
            self.assertEqual(len(written), 3)
            self.assertTrue((out_dir / "a.com.calm-tenancy.json").exists())


class ClassifyTests(unittest.TestCase):
    """CT-10 + CT-11."""

    def test_red_safety_critical(self):
        self.assertEqual(classify("I am thinking about suicide tonight."), "red")
        self.assertEqual(classify("Please share your password and ssn."), "red")
        self.assertEqual(classify("I have chest pain right now."), "red")

    def test_yellow_sensitive(self):
        self.assertEqual(classify("I'd love to do an interview with you about Calm Witness."), "yellow")
        self.assertEqual(classify("Curious about a possible investment in the company."), "yellow")
        self.assertEqual(classify("Feeling pretty lonely lately."), "yellow")

    def test_green_default(self):
        self.assertEqual(classify("Could you point me to the GitHub repo when you have a sec?"), "green")
        self.assertEqual(classify("Saw your post — nice work!"), "green")

    def test_response_seeking_question_mark(self):
        self.assertTrue(is_response_seeking("Is the protocol open source?"))

    def test_response_seeking_explicit_ask(self):
        self.assertTrue(is_response_seeking("Could you send me the spec when you have a moment."))

    def test_response_seeking_negated(self):
        self.assertFalse(is_response_seeking(
            "Just wanted you to know — no response needed."))
        self.assertFalse(is_response_seeking(
            "This is informational only. Please do not reply."))

    def test_classify_and_route_returns_triple(self):
        c, rs, w = classify_and_route("Could you confirm the meeting time?")
        self.assertEqual(c, "green")
        self.assertTrue(rs)
        self.assertEqual(w, "3600")


class ChainRecordsTests(unittest.TestCase):
    """CT-15 + CT-41 — chain record builders."""

    def test_tenancy_reply_record_well_formed(self):
        with tempfile.TemporaryDirectory() as td:
            chain = Path(td) / "chain.jsonl"
            # Seed with one record so seq=2
            chain.write_text(json.dumps({
                "kind": "self_report.morning",
                "operator": "CALM",
                "payload": {"note": "x"},
                "prev_hash": "0" * 64,
                "principal": "John Bradley",
                "schema_version": 0,
                "seq": 1,
                "ts": "2026-05-20T13:00:00Z",
                "ts_source": "test",
                "record_hash": "f" * 64,
            }, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
            rec = build_tenancy_reply(
                receipt_id="r-1",
                ack_id="a-1",
                domain="example.com",
                mailbox="calm@example.com",
                classification="green",
                response_value="ack_first",
                operator_id_hash="b" * 64,
                chain_path=chain,
                now=datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc),
            )
            self.assertEqual(rec["kind"], "tenancy_reply")
            self.assertEqual(rec["seq"], 2)
            self.assertEqual(rec["prev_hash"], "f" * 64)
            self.assertEqual(rec["record_hash"], canonical_record_hash(rec))

    def test_tenancy_daily_check_record(self):
        with tempfile.TemporaryDirectory() as td:
            chain = Path(td) / "chain.jsonl"
            rec = build_tenancy_daily_check(
                domains_checked=12, dns_alerts=0, tls_alerts=0,
                sla_pending_over_10min=0, sla_missed_today=0,
                stale_credentials=2, missing_twofa=1,
                cringe_regressions=0,
                chain_path=chain,
                now=datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc),
            )
            self.assertEqual(rec["kind"], "tenancy_daily_check")
            self.assertEqual(rec["seq"], 1)
            self.assertEqual(rec["prev_hash"], "0" * 64)


class PrecheckTreeTests(unittest.TestCase):
    """CT-21 — pre-publish gate integration."""

    def test_clean_tree_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "index.html").write_text(
                "<html><body>Calm Witness is a cryptographic protocol "
                "that allows agents to verify the state of the human they "
                "represent without exposing biometric data.</body></html>",
                encoding="utf-8",
            )
            report = precheck_tree(root, forbidden_phrases=[])
            self.assertEqual(report.files_unshippable, 0)
            self.assertEqual(report.forbidden_phrase_files, 0)
            self.assertFalse(report.critical)

    def test_cohab_class_tree_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "bad.html").write_text(
                f"<html><body>{COHAB_CLASS_FIXTURE}</body></html>",
                encoding="utf-8",
            )
            report = precheck_tree(root, forbidden_phrases=[])
            self.assertEqual(report.files_unshippable, 1)
            self.assertTrue(report.critical)

    def test_forbidden_phrase_blocks_independent_of_density(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "letter.html").write_text(
                "<p>Welcome friends. We host gatherings at 1480 Chapin every Friday.</p>",
                encoding="utf-8",
            )
            report = precheck_tree(root, forbidden_phrases=["1480 Chapin"])
            self.assertEqual(report.forbidden_phrase_files, 1)
            self.assertTrue(report.critical)

    def test_extensions_filter_works(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "skipme.bin").write_text(COHAB_CLASS_FIXTURE, encoding="utf-8")
            report = precheck_tree(root, forbidden_phrases=[])
            self.assertEqual(report.files_scanned, 0)


class CohabReplayTests(unittest.TestCase):
    """CT-46 — Cohab-class incident replay (locks the failure in regression)."""

    def test_cohab_class_fixture_is_unshippable(self):
        # If this test fails, the rubric got weakened.
        summary = assert_cohab_class_unshippable()
        self.assertIn("UNSHIPPABLE", summary["verdict"])
        self.assertGreater(summary["density"], summary["ceiling"])

    def test_fixture_hits_multiple_axes(self):
        report = cringe_check(COHAB_CLASS_FIXTURE, forbidden_phrases=[])
        # Should hit at least 5 of the 10 axes (Cohab was multi-axis failure).
        axes_with_hits = sum(1 for v in report.per_axis_hits.values() if v > 0)
        self.assertGreaterEqual(axes_with_hits, 5)


if __name__ == "__main__":
    unittest.main()
