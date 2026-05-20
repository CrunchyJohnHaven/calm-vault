"""Tests for calm-witness verify-chain (Everest 28).

Run: ``python3 -m pytest test_verify_chain.py`` or ``python3 test_verify_chain.py``.
Uses only stdlib so it runs anywhere Python 3.9+ is available.
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from schema import KIND_REGISTRY, SCHEMA_VERSION, validate_record
from verify_chain import (
    GENESIS_PREV_HASH,
    canonical_record_hash,
    load_jsonl,
    main,
    verify_chain,
)


def _record(seq: int, prev_hash: str, payload_note: str) -> dict:
    rec = {
        "kind": "self_report.test",
        "operator": "CALM",
        "payload": {"note": payload_note},
        "prev_hash": prev_hash,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": f"2026-05-20T10:{20+seq:02d}:00-04:00",
        "ts_source": "test_fixture",
    }
    rec["record_hash"] = canonical_record_hash(rec)
    return rec


class HashTests(unittest.TestCase):
    def test_canonical_hash_excludes_record_hash(self):
        rec = _record(1, GENESIS_PREV_HASH, "a")
        h1 = canonical_record_hash(rec)
        rec2 = dict(rec)
        rec2["record_hash"] = "ffff"
        h2 = canonical_record_hash(rec2)
        self.assertEqual(h1, h2)

    def test_canonical_hash_sorts_keys(self):
        # Two semantically equal records with different key orders must hash equal.
        a = {"b": 1, "a": 2}
        b = {"a": 2, "b": 1}
        self.assertEqual(canonical_record_hash(a), canonical_record_hash(b))


class VerifyChainTests(unittest.TestCase):
    def _two_record_chain(self):
        r1 = _record(1, GENESIS_PREV_HASH, "first")
        r2 = _record(2, r1["record_hash"], "second")
        return [r1, r2]

    def test_clean_chain_passes(self):
        checks = verify_chain(self._two_record_chain())
        self.assertEqual(len(checks), 2)
        self.assertTrue(all(c.ok for c in checks))

    def test_tampered_payload_breaks_hash(self):
        chain = self._two_record_chain()
        chain[1]["payload"]["note"] = "altered after the fact"
        checks = verify_chain(chain)
        self.assertTrue(checks[0].ok)
        self.assertFalse(checks[1].ok_hash)

    def test_broken_link_detected(self):
        chain = self._two_record_chain()
        chain[1]["prev_hash"] = "f" * 64
        chain[1]["record_hash"] = canonical_record_hash(chain[1])
        checks = verify_chain(chain)
        self.assertFalse(checks[1].ok_link)
        self.assertTrue(checks[1].ok_hash)  # hash recomputed; link still wrong

    def test_genesis_must_be_zeros(self):
        bad = _record(1, "a" * 64, "first")
        checks = verify_chain([bad])
        self.assertFalse(checks[0].ok_link)

    def test_seq_must_start_at_one(self):
        bad = _record(2, GENESIS_PREV_HASH, "first")
        checks = verify_chain([bad])
        self.assertFalse(checks[0].ok_seq)

    def test_seq_must_be_consecutive(self):
        r1 = _record(1, GENESIS_PREV_HASH, "first")
        r3 = _record(3, r1["record_hash"], "third")
        checks = verify_chain([r1, r3])
        self.assertTrue(checks[0].ok)
        self.assertFalse(checks[1].ok_seq)


class SchemaTests(unittest.TestCase):
    """Everest 26 — JSON Schema validation."""

    def test_clean_self_report_morning_validates(self):
        rec = {
            "kind": "self_report.morning",
            "operator": "CALM",
            "payload": {
                "affect": ["calm"],
                "alarm": False,
                "known_health_issues": [],
                "note": "n",
                "readiness": "ready_to_work",
                "restedness": "fully_rested",
                "sleep_hours": 8.0,
                "wake_time": "09:30",
            },
            "prev_hash": GENESIS_PREV_HASH,
            "principal": "John Bradley",
            "record_hash": "0" * 64,
            "schema_version": SCHEMA_VERSION,
            "seq": 1,
            "ts": "2026-05-20T10:20:00-04:00",
            "ts_source": "test",
        }
        rec["record_hash"] = canonical_record_hash(rec)
        self.assertEqual(validate_record(rec), [])

    def test_unknown_kind_rejected(self):
        rec = _record(1, GENESIS_PREV_HASH, "x")
        rec["kind"] = "made_up_kind"
        rec["record_hash"] = canonical_record_hash(rec)
        errs = validate_record(rec)
        self.assertTrue(any("unknown kind" in e for e in errs))

    def test_bad_record_hash_format_rejected(self):
        rec = _record(1, GENESIS_PREV_HASH, "x")
        rec["record_hash"] = "not-hex"
        errs = validate_record(rec)
        self.assertTrue(any("record_hash" in e for e in errs))

    def test_summit_bagged_both_naming_styles_accepted(self):
        # Two parallel sessions converged on slightly different field names;
        # the v0 schema accepts either.
        base = {
            "kind": "summit_bagged",
            "operator": "CALM",
            "prev_hash": GENESIS_PREV_HASH,
            "principal": "John Bradley",
            "record_hash": "0" * 64,
            "schema_version": SCHEMA_VERSION,
            "seq": 1,
            "ts": "2026-05-20T10:46:00-04:00",
            "ts_source": "test",
        }
        a = dict(base, payload={
            "summit_name": "X",
            "phase": "I",
            "summit_number": 1,
            "evidence_path": "/p",
        })
        a["record_hash"] = canonical_record_hash(a)
        b = dict(base, payload={
            "summit_name": "X",
            "phase": "I",
            "summit_number_in_route_map": 1,
            "evidence_paths": ["/p1", "/p2"],
            "evidence_sha256": {"/p1": "0" * 64, "/p2": "f" * 64},
        })
        b["record_hash"] = canonical_record_hash(b)
        self.assertEqual(validate_record(a), [])
        self.assertEqual(validate_record(b), [])


class CLIIntegrationTests(unittest.TestCase):
    def test_cli_zero_exit_on_clean_chain(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "chain.jsonl"
            r1 = _record(1, GENESIS_PREV_HASH, "first")
            r2 = _record(2, r1["record_hash"], "second")
            with p.open("w", encoding="utf-8") as fh:
                for rec in (r1, r2):
                    fh.write(json.dumps(rec, sort_keys=True, separators=(",", ":")))
                    fh.write("\n")
            rc = main([str(p), "--quiet"])
            self.assertEqual(rc, 0)

    def test_cli_nonzero_exit_on_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "chain.jsonl"
            r1 = _record(1, GENESIS_PREV_HASH, "first")
            r2 = _record(2, r1["record_hash"], "second")
            r2["payload"]["note"] = "tampered"
            with p.open("w", encoding="utf-8") as fh:
                for rec in (r1, r2):
                    fh.write(json.dumps(rec, sort_keys=True, separators=(",", ":")))
                    fh.write("\n")
            rc = main([str(p), "--quiet"])
            self.assertEqual(rc, 1)

    def test_cli_loads_real_genesis(self):
        # Sanity: against the live vault, the first record alone must verify.
        live = Path.home() / ".calm-vault" / "user_state.jsonl"
        if not live.exists():
            self.skipTest("live chain not present in this environment")
        records = load_jsonl(live)
        checks = verify_chain(records[:1])
        self.assertTrue(checks[0].ok)


if __name__ == "__main__":
    unittest.main()
