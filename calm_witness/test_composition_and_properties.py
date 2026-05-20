"""Tests for predicate composition (E61) + property-based chain tests (E86, E87).

Stdlib-only property tests using random seeds. We don't use Hypothesis (no
PyPI deps); the property loop is small and deterministic via a fixed seed.
"""
from __future__ import annotations

import json
import random
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from composition import compose_and, compose_or, negate
from predicates import EvaluationResult, P_IN_BASELINE_24H_ID, PredicateValue, in_baseline_24h
from schema import validate_record
from verify_chain import canonical_record_hash, verify_chain


def _r(v: PredicateValue) -> EvaluationResult:
    return EvaluationResult(P_IN_BASELINE_24H_ID, v, None, "test")


T, F, U, R = (_r(v) for v in PredicateValue.__members__.values())  # exhausted by repeat
TRUE, FALSE, UNKNOWN, REFUSED = _r(PredicateValue.TRUE), _r(PredicateValue.FALSE), _r(PredicateValue.UNKNOWN), _r(PredicateValue.REFUSED)


class CompositionTruthTables(unittest.TestCase):
    """Everest 61 — AND/OR/NOT truth tables."""

    def test_and_truth_table(self):
        # row × col format
        T_, F_, U_, R_ = TRUE, FALSE, UNKNOWN, REFUSED
        table = {
            (PredicateValue.TRUE, PredicateValue.TRUE): PredicateValue.TRUE,
            (PredicateValue.TRUE, PredicateValue.FALSE): PredicateValue.FALSE,
            (PredicateValue.TRUE, PredicateValue.UNKNOWN): PredicateValue.UNKNOWN,
            (PredicateValue.TRUE, PredicateValue.REFUSED): PredicateValue.REFUSED,
            (PredicateValue.FALSE, PredicateValue.UNKNOWN): PredicateValue.FALSE,
            (PredicateValue.FALSE, PredicateValue.REFUSED): PredicateValue.REFUSED,
            (PredicateValue.UNKNOWN, PredicateValue.UNKNOWN): PredicateValue.UNKNOWN,
            (PredicateValue.UNKNOWN, PredicateValue.REFUSED): PredicateValue.REFUSED,
            (PredicateValue.REFUSED, PredicateValue.REFUSED): PredicateValue.REFUSED,
        }
        for (a, b), expected in table.items():
            self.assertEqual(compose_and([_r(a), _r(b)]), expected, f"{a} AND {b}")

    def test_or_truth_table(self):
        table = {
            (PredicateValue.TRUE, PredicateValue.FALSE): PredicateValue.TRUE,
            (PredicateValue.TRUE, PredicateValue.UNKNOWN): PredicateValue.TRUE,
            (PredicateValue.TRUE, PredicateValue.REFUSED): PredicateValue.REFUSED,
            (PredicateValue.FALSE, PredicateValue.FALSE): PredicateValue.FALSE,
            (PredicateValue.FALSE, PredicateValue.UNKNOWN): PredicateValue.UNKNOWN,
            (PredicateValue.FALSE, PredicateValue.REFUSED): PredicateValue.REFUSED,
            (PredicateValue.UNKNOWN, PredicateValue.UNKNOWN): PredicateValue.UNKNOWN,
        }
        for (a, b), expected in table.items():
            self.assertEqual(compose_or([_r(a), _r(b)]), expected, f"{a} OR {b}")

    def test_refused_is_absorbing(self):
        self.assertEqual(compose_and([TRUE, REFUSED, TRUE]), PredicateValue.REFUSED)
        self.assertEqual(compose_or([FALSE, REFUSED, FALSE]), PredicateValue.REFUSED)

    def test_double_negation_when_true_or_false(self):
        self.assertEqual(negate(_r(negate(TRUE))), PredicateValue.TRUE)
        self.assertEqual(negate(_r(negate(FALSE))), PredicateValue.FALSE)

    def test_negation_preserves_unknown_and_refused(self):
        self.assertEqual(negate(UNKNOWN), PredicateValue.UNKNOWN)
        self.assertEqual(negate(REFUSED), PredicateValue.REFUSED)


class ChainPropertyTests(unittest.TestCase):
    """Everest 86 — property-based hash-chain invariants."""

    SEED = 0xC04E_8170  # deterministic

    def _record(self, seq, prev_hash, payload_note):
        rec = {
            "kind": "self_report.test",
            "operator": "CALM",
            "payload": {"note": payload_note},
            "prev_hash": prev_hash,
            "principal": "John Bradley",
            "schema_version": 0,
            "seq": seq,
            "ts": f"2026-05-20T10:{seq % 60:02d}:00-04:00",
            "ts_source": "prop_test",
        }
        rec["record_hash"] = canonical_record_hash(rec)
        return rec

    def test_random_chain_always_verifies(self):
        """Property: any chain built by sequentially appending verifies cleanly."""
        rng = random.Random(self.SEED)
        prev = "0" * 64
        chain = []
        for seq in range(1, 101):
            rec = self._record(seq, prev, rng.choice(["a", "b", "c", "d"]))
            chain.append(rec)
            prev = rec["record_hash"]
        checks = verify_chain(chain)
        self.assertTrue(all(c.ok for c in checks))

    def test_any_single_byte_flip_breaks_chain(self):
        """Property: mutating any byte of any payload invalidates that record."""
        rng = random.Random(self.SEED + 1)
        prev = "0" * 64
        chain = []
        for seq in range(1, 21):
            rec = self._record(seq, prev, rng.choice(["x", "y"]))
            chain.append(rec)
            prev = rec["record_hash"]

        # Flip a byte in a random middle record's payload.
        target_idx = rng.randint(1, len(chain) - 2)
        chain[target_idx]["payload"]["note"] = "TAMPERED"
        # Recompute hash; chain still breaks because prev_hash on next won't match.
        chain[target_idx]["record_hash"] = canonical_record_hash(chain[target_idx])

        checks = verify_chain(chain)
        self.assertFalse(all(c.ok for c in checks))


class PredicatePropertyTests(unittest.TestCase):
    """Everest 87 — property-based predicate invariants."""

    SEED = 0xCA1D_BEEF
    NOW = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)

    def test_in_baseline_is_deterministic(self):
        """Calling the predicate twice on the same inputs returns the same result."""
        rec = {
            "kind": "self_report.morning",
            "operator": "CALM",
            "payload": {
                "affect": ["calm", "curious"],
                "alarm": False,
                "known_health_issues": [],
                "note": "n",
                "readiness": "ready_to_work",
                "restedness": "fully_rested",
                "sleep_hours": 8.0,
                "wake_time": "09:30",
            },
            "prev_hash": "0" * 64,
            "principal": "John Bradley",
            "schema_version": 0,
            "seq": 1,
            "ts": "2026-05-20T13:00:00+00:00",
            "ts_source": "prop_test",
        }
        rec["record_hash"] = canonical_record_hash(rec)
        for _ in range(50):
            r1 = in_baseline_24h([rec], now=self.NOW)
            r2 = in_baseline_24h([rec], now=self.NOW)
            self.assertEqual(r1.value, r2.value)
            self.assertEqual(r1.reason, r2.reason)

    def test_predicate_value_enum_closed(self):
        """Property: every PredicateValue is one of the four canonical values."""
        for v in PredicateValue:
            self.assertIn(v.value, {"true", "false", "unknown", "refused"})


if __name__ == "__main__":
    unittest.main()
