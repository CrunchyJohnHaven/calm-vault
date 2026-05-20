"""Tests for the Calm Tenancy v0 package — CT-12, CT-19, CT-20, CT-29, CT-31, CT-36."""
from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from credential_vault import (
    CredentialMeta,
    list_missing_twofa,
    list_stale,
    load_all,
    never_quote_check,
    register,
    scan_outbound_for_credentials,
)
from cringe_gate import (
    DENSITY_THRESHOLD,
    cringe_check,
    strip_html,
    word_count,
)
from daily_check import run_daily_check
from mailbox_sla import (
    SLA_SECONDS,
    emit_pending_acks,
    ingest_inbound,
    sla_report,
)


class CringeGateTests(unittest.TestCase):
    """CT-19 cringe rubric + CT-20 forbidden-phrase block."""

    def test_clean_text_passes(self):
        text = (
            "Calm Witness is a cryptographic protocol that lets one AI agent vouch "
            "for the cognitive state of the human it represents to another AI agent, "
            "without revealing the underlying biometric data."
        )
        report = cringe_check(text, forbidden_phrases=[])
        self.assertEqual(report.verdict, "SHIP")

    def test_cohab_failure_classes_detected(self):
        """The exact failure patterns the Cohab postmortem identified."""
        text = (
            "We recognized you on the way in. We have been paying attention. "
            "Your odds of success are ~55% with a 25% upside. There are 33 seats "
            "and a small grant from John waiting on the third shelf in the wisdom library."
        )
        report = cringe_check(text, forbidden_phrases=[])
        # Surveillance + manufactured precision + money math + mystical objects
        self.assertGreater(report.per_axis_hits["10_persona_surveillance"], 0)
        self.assertGreater(report.per_axis_hits["3_manufactured_precision"], 0)
        self.assertGreater(report.per_axis_hits["7_money_math_upfront"], 0)
        self.assertGreater(report.per_axis_hits["9_mystical_objects"], 0)
        self.assertIn("UNSHIPPABLE", report.verdict)

    def test_forbidden_phrase_hard_blocks(self):
        text = "Welcome to our community at 1480 Chapin where we gather."
        report = cringe_check(text, forbidden_phrases=["1480 Chapin"])
        self.assertEqual(report.forbidden_phrase_hits[0][0], "1480 Chapin")
        self.assertIn("forbidden phrase", report.verdict)

    def test_html_stripped_before_scoring(self):
        html = (
            "<html><style>.x{color:red}</style><body>"
            "<p>The kettle is on at the third shelf.</p></body></html>"
        )
        report = cringe_check(html, forbidden_phrases=[])
        self.assertGreaterEqual(report.per_axis_hits["9_mystical_objects"], 1)
        self.assertNotIn("color:red", strip_html(html))

    def test_word_count_excludes_html(self):
        wc = word_count(strip_html("<p>hello world</p><script>noisy</script>"))
        self.assertEqual(wc, 2)

    def test_density_math(self):
        # Construct a known-density example: 4 surveillance hits in 200 words.
        body = "we recognized you on the way in. " * 4  # 32 words, 4 hits
        padding = "lorem ipsum dolor sit amet " * 34    # ~170 words, 0 hits
        report = cringe_check(body + padding, forbidden_phrases=[])
        self.assertGreater(report.density, 0.5)


class MailboxSLATests(unittest.TestCase):
    """CT-12 10-minute auto-ack + CT-16 SLA-miss tracking."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.queue = Path(self.tmpdir.name) / "queue.jsonl"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_ingest_creates_pending_row(self):
        row = ingest_inbound(
            domain="thecreativitymachine.ai",
            mailbox="calm@thecreativitymachine.ai",
            sender_addr="someone@example.com",
            subject_digest="a" * 64,
            classification="green",
            queue_path=self.queue,
        )
        self.assertIsNone(row.ack.ack_emitted_at)
        self.assertEqual(row.ack.sla_status, "pending")

    def test_ack_within_10min_marked_within_sla(self):
        now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
        ingest_inbound(
            domain="credexai.org",
            mailbox="calm@credexai.org",
            sender_addr="a@b",
            subject_digest="0" * 64,
            classification="green",
            queue_path=self.queue,
            now=now,
        )
        # Emit 5 min later — within SLA
        emit_at = now + timedelta(minutes=5)
        summary = emit_pending_acks(
            queue_path=self.queue,
            operator_id_hash="op" * 32,
            chain_head="c" * 64,
            now=emit_at,
        )
        self.assertEqual(summary["acks_emitted"], 1)
        self.assertEqual(summary["sla_missed"], 0)

    def test_ack_after_10min_marked_missed(self):
        now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
        ingest_inbound(
            domain="x", mailbox="m@x", sender_addr="a@b",
            subject_digest="0" * 64, classification="green",
            queue_path=self.queue, now=now,
        )
        emit_at = now + timedelta(minutes=15)
        summary = emit_pending_acks(
            queue_path=self.queue, operator_id_hash="op",
            chain_head="c", now=emit_at,
        )
        self.assertEqual(summary["sla_missed"], 1)

    def test_no_response_seeking_skipped(self):
        now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
        ingest_inbound(
            domain="x", mailbox="m@x", sender_addr="a@b",
            subject_digest="0" * 64, classification="green",
            response_seeking=False,
            queue_path=self.queue, now=now,
        )
        summary = emit_pending_acks(
            queue_path=self.queue, operator_id_hash="op",
            chain_head="c", now=now + timedelta(minutes=20),
        )
        self.assertEqual(summary["acks_emitted"], 0)
        self.assertEqual(summary["skipped"], 1)

    def test_report_shows_pending_over_10min(self):
        now = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
        ingest_inbound(
            domain="x", mailbox="m@x", sender_addr="a@b",
            subject_digest="0" * 64, classification="green",
            queue_path=self.queue, now=now,
        )
        report = sla_report(queue_path=self.queue, now=now + timedelta(minutes=15))
        self.assertEqual(report["pending_over_10min"], 1)


class CredentialVaultTests(unittest.TestCase):
    """CT-29 registry + CT-31 never-quote + CT-32 rotation cadence + CT-33 stale alert + CT-35 2FA."""

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.path = Path(self.tmpdir.name) / "creds.jsonl"

    def tearDown(self):
        self.tmpdir.cleanup()

    def _make(self, **kwargs):
        defaults = dict(
            handle="x.com:cf-token", domain="x.com", kind="api_token",
            label="Cloudflare API",
            secret_pointer="age://path/to/encrypted",
            last_rotated_iso=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            twofa_enabled=True, notes="",
        )
        defaults.update(kwargs)
        return CredentialMeta(**defaults)

    def test_register_and_load_roundtrip(self):
        register(self._make(), path=self.path)
        loaded = load_all(self.path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].handle, "x.com:cf-token")

    def test_stale_detected_after_cadence(self):
        old = (datetime.now(timezone.utc) - timedelta(days=60))
        register(self._make(kind="api_token",  # 30-day cadence
                            last_rotated_iso=old.isoformat().replace("+00:00", "Z")),
                 path=self.path)
        stale = list_stale(path=self.path)
        self.assertEqual(len(stale), 1)

    def test_missing_twofa_surfaces(self):
        register(self._make(twofa_enabled=False), path=self.path)
        miss = list_missing_twofa(path=self.path)
        self.assertEqual(len(miss), 1)

    def test_never_quote_catches_secret_in_outbound(self):
        secret = "hunter2-very-secret-passphrase"
        outbound = (
            "Hi there, your account is configured. Please don't share this with "
            f"anyone: {secret}. Let me know if you have questions."
        )
        result = never_quote_check(outbound, loaded_secrets=[secret])
        self.assertFalse(result["allowed"])
        # The fingerprint surfaces, the secret does NOT appear in the result.
        self.assertEqual(len(result["hits_fingerprints"]), 1)
        self.assertNotIn(secret, json.dumps(result))

    def test_never_quote_passes_clean_outbound(self):
        outbound = "Hello, your account has been provisioned. Please log in via SSO."
        result = never_quote_check(outbound, loaded_secrets=["hunter2-very-secret-passphrase"])
        self.assertTrue(result["allowed"])

    def test_short_secrets_skipped(self):
        # A 7-char "secret" is below default min_len=8 → not scanned (avoid
        # false-positives on common substrings).
        outbound = "abc1234 appears in this benign sentence."
        hits = scan_outbound_for_credentials(outbound, loaded_secrets=["abc1234"], min_len=8)
        self.assertEqual(hits, [])


class DailyCheckTests(unittest.TestCase):
    """CT-36 daily check driver — smoke-level only."""

    def test_run_returns_a_report(self):
        # Use a path that doesn't exist so fleet check is skipped cleanly.
        report = run_daily_check(
            domains_path=Path("/nonexistent/owned_domains.txt"),
            fleet_script=Path("/nonexistent/fleet.py"),
            dry_run=True,
        )
        self.assertEqual(report.domains_checked, 0)
        self.assertIsInstance(report.notes, list)


if __name__ == "__main__":
    unittest.main()
