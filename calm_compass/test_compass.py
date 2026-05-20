"""Tests for the v0 Calm Compass package."""
from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from aggregator import (                                                # noqa: E402
    build_compass_proof,
    verify_compass_proof,
    PROTOCOL_VERSION,
)
from classifiers import (                                               # noqa: E402
    CLASSIFIERS,
    classifier_hash,
    cross_tribal_engagement_score,
    no_evidence_of_willful_harm_score,
    respects_difference_score,
    score_chain,
    unselfish_disposition_score,
)


def _rec(seq=1, note="x", kind="self_report.morning", extras=None):
    rec = {
        "kind": kind,
        "operator": "CALM",
        "payload": {"note": note, **(extras or {})},
        "prev_hash": "0" * 64,
        "principal": "John Bradley",
        "schema_version": 0,
        "seq": seq,
        "ts": f"2026-05-20T13:00:0{seq % 10}+00:00",
        "ts_source": "test",
        "record_hash": "a" * 64,
    }
    return rec


class ClassifierTests(unittest.TestCase):
    def test_unselfish_recognizes_generosity(self):
        self.assertEqual(unselfish_disposition_score(
            _rec(note="Spent the afternoon mentoring a junior engineer.")), 1)
        self.assertEqual(unselfish_disposition_score(
            _rec(note="Just introduced my friend Maria to a great recruiter.")), 1)
        self.assertEqual(unselfish_disposition_score(
            _rec(note="Donated $200 to GiveDirectly today.")), 1)

    def test_unselfish_rejects_transactional(self):
        self.assertEqual(unselfish_disposition_score(
            _rec(note="I'll help him in exchange for a referral.")), 0)
        self.assertEqual(unselfish_disposition_score(
            _rec(note="Sure, after you pay the deposit.")), 0)

    def test_unselfish_default_zero(self):
        self.assertEqual(unselfish_disposition_score(
            _rec(note="Worked on the protocol draft today.")), 0)

    def test_cross_tribal_with_tribe_map(self):
        tribe_map = {"self": {"groups": ["tech"]},
                     "edges": {"local_grocers": "across", "neighbors": "across"}}
        self.assertEqual(cross_tribal_engagement_score(
            _rec(note="Had a long chat with our local_grocers about the new policy."),
            tribe_map=tribe_map), 1)
        self.assertEqual(cross_tribal_engagement_score(
            _rec(note="Met with my CTO peers."), tribe_map=tribe_map), 0)

    def test_cross_tribal_without_map(self):
        self.assertEqual(cross_tribal_engagement_score(_rec(note="anyone")), 0)

    def test_respects_difference_positive(self):
        self.assertEqual(respects_difference_score(
            _rec(note="I hear you — that's a fair point I hadn't considered.")), 1)
        self.assertEqual(respects_difference_score(
            _rec(note="I was wrong about that; apologies.")), 1)

    def test_respects_difference_contempt(self):
        self.assertEqual(respects_difference_score(
            _rec(note="Those people always cause trouble.")), -1)
        self.assertEqual(respects_difference_score(
            _rec(note="Typical engineers — never get the user.")), -1)

    def test_respects_difference_neutral(self):
        self.assertEqual(respects_difference_score(
            _rec(note="Worked on the docs today.")), 0)

    def test_no_harm_default(self):
        self.assertEqual(no_evidence_of_willful_harm_score(_rec()), 0)

    def test_no_harm_flag_negative(self):
        self.assertEqual(no_evidence_of_willful_harm_score(
            _rec(extras={"flag_willful_harm": True})), -1)

    def test_no_harm_external_claim_negative(self):
        self.assertEqual(no_evidence_of_willful_harm_score(
            _rec(kind="harm_claim_external")), -1)

    def test_classifier_hash_is_deterministic(self):
        h1 = classifier_hash("calm-compass/predicate/v0/unselfish_disposition")
        h2 = classifier_hash("calm-compass/predicate/v0/unselfish_disposition")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 64)


class AggregatorTests(unittest.TestCase):
    def setUp(self):
        self.window_start = datetime(2026, 5, 1, tzinfo=timezone.utc)
        self.window_end = datetime(2026, 5, 31, tzinfo=timezone.utc)
        self.unselfish_id = "calm-compass/predicate/v0/unselfish_disposition"

    def test_build_proof_true_when_threshold_met(self):
        chain = [_rec(seq=i, note=f"helping with task {i}") for i in range(1, 8)]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=5,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        self.assertEqual(proof.value, "true")
        self.assertEqual(proof.n_records_considered, 7)

    def test_build_proof_false_when_threshold_missed(self):
        chain = [_rec(seq=1, note="worked on docs")]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=5,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        self.assertEqual(proof.value, "false")

    def test_verify_clean_proof(self):
        chain = [_rec(seq=i, note=f"mentored junior {i}") for i in range(1, 8)]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=5,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        errors = verify_compass_proof(
            proof=proof,
            expected_threshold=5,
            expected_predicate_id=self.unselfish_id,
        )
        self.assertEqual(errors, [])

    def test_verify_catches_threshold_mismatch(self):
        chain = [_rec(seq=1, note="mentored")]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=5,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        errors = verify_compass_proof(
            proof=proof,
            expected_threshold=10,
            expected_predicate_id=self.unselfish_id,
        )
        self.assertTrue(any("threshold mismatch" in e for e in errors))

    def test_verify_catches_predicate_mismatch(self):
        chain = [_rec(seq=1, note="x")]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=1,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        errors = verify_compass_proof(
            proof=proof,
            expected_threshold=1,
            expected_predicate_id="calm-compass/predicate/v0/respects_difference",
        )
        self.assertTrue(any("predicate_id mismatch" in e for e in errors))

    def test_proof_protocol_version_is_v0(self):
        chain = [_rec(seq=1, note="x")]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=1,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        self.assertEqual(proof.protocol_version, PROTOCOL_VERSION)

    def test_proof_carries_classifier_hash(self):
        chain = [_rec(seq=1, note="x")]
        proof = build_compass_proof(
            chain=chain,
            predicate_id=self.unselfish_id,
            threshold=1,
            window_start=self.window_start,
            window_end=self.window_end,
            operator_id_hash="op" * 32,
        )
        self.assertEqual(proof.classifier_hash_hex, classifier_hash(self.unselfish_id))


if __name__ == "__main__":
    unittest.main()
