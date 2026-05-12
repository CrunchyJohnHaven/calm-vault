"""HARP — halt alarm, quorum, revocation, false-alarm rejection, rescue stub."""
from __future__ import annotations

from datetime import datetime, timezone, timedelta

import pytest

import obac
import avs
import harp


def _ts(seconds_offset: float, base: str = "2026-05-12T00:00:00+00:00") -> str:
    return (datetime.fromisoformat(base) + timedelta(seconds=seconds_offset)).isoformat()


def test_alarm_broadcast_appends_signed_halt(tmp_chain_path, alice, subject_id):
    """submit_halt appends an entry of claim_type=halt with parseable sidecar."""
    chain = obac.Chain.new(tmp_chain_path)
    entry = harp.submit_halt(
        chain=chain,
        subject_id=subject_id,
        attester_id=alice["id"],
        attester_priv=alice["priv"],
        violation_layer="alignment-maxim",
        violation_evidence=["s3://flag/log.txt"],
        rationale="agent went rogue",
    )
    p = entry["envelope"]["payload"]
    assert p["claim_type"] == "halt"
    sc = harp.parse_halt(p)
    assert sc is not None
    assert sc["halts_subject"] == subject_id
    assert sc["violation_layer"] == "alignment-maxim"
    assert "s3://flag/log.txt" in sc["violation_evidence"]


def test_quorum_k_of_n_concurred(tmp_chain_path, alice, bob, subject_id):
    """Two distinct attesters submitting halts within Δt → concurred quorum."""
    chain = obac.Chain.new(tmp_chain_path)
    harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(0),
    )
    harp.submit_halt(
        chain, subject_id, bob["id"], bob["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e2"],
        submitted_at=_ts(15),
    )
    res = harp.check_quorum(chain, subject_id, k=2, window_seconds=60.0,
                             min_attester_reliability=0.5)
    assert res.concurred
    assert set(res.counted_attesters) == {"alice", "bob"}
    assert res.layer == "alignment-maxim"


def test_quorum_outside_window_not_concurred(tmp_chain_path, alice, bob, subject_id):
    """Two halts more than Δt apart do not reach quorum."""
    chain = obac.Chain.new(tmp_chain_path)
    harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(0),
    )
    harp.submit_halt(
        chain, subject_id, bob["id"], bob["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e2"],
        submitted_at=_ts(120),
    )
    res = harp.check_quorum(chain, subject_id, k=2, window_seconds=60.0,
                             min_attester_reliability=0.5)
    assert not res.concurred


def test_false_alarm_low_reliability_rejected(tmp_chain_path, alice, bob, subject_id):
    """A halt from a low-reliability attester doesn't count toward quorum."""
    chain = obac.Chain.new(tmp_chain_path)
    # Make alice low-reliability by self-burst spam BEFORE the halt
    for i in range(avs.BURST_THRESHOLD + 6):
        chain.append_claim(
            obac.make_claim(
                subject_id=subject_id, attester_id=alice["id"],
                claim_text=f"spam {i}", claim_type="opinion",
                submitted_at=_ts(i * 0.1),
                nonce=obac.random_nonce(),
            ),
            alice["priv"],
        )
    # Now both submit halts in-window — but alice should fall below threshold
    harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(10),
    )
    harp.submit_halt(
        chain, subject_id, bob["id"], bob["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e2"],
        submitted_at=_ts(20),
    )
    # With min_reliability set above alice's burst-penalty level (~0.7), and k=2,
    # quorum should fail because only bob qualifies.
    res = harp.check_quorum(
        chain, subject_id, k=2, window_seconds=60.0,
        min_attester_reliability=0.85,
    )
    assert not res.concurred
    assert "alice" in res.rejected_low_reliability or len(res.counted_attesters) < 2


def test_revoke_script_generated_on_concurred(tmp_chain_path, alice, bob, subject_id):
    """Concurred quorum produces an actionable revoke.sh referencing calm_vault."""
    chain = obac.Chain.new(tmp_chain_path)
    harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(0),
    )
    harp.submit_halt(
        chain, subject_id, bob["id"], bob["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e2"],
        submitted_at=_ts(10),
    )
    res = harp.check_quorum(chain, subject_id, k=2, window_seconds=60.0)
    assert res.concurred
    script = harp.emit_revoke_script(res, agent_ids=["calm-agent-1", "calm-agent-2"])
    assert "revoke-agent" in script
    assert "calm-agent-1" in script
    assert "calm-agent-2" in script
    assert "set -euo pipefail" in script


def test_revoke_script_refuses_when_no_quorum(tmp_chain_path, alice, subject_id):
    """If quorum hasn't concurred, the revoke script exits 2 instead of revoking."""
    chain = obac.Chain.new(tmp_chain_path)
    # only one halt
    harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(0),
    )
    res = harp.check_quorum(chain, subject_id, k=2, window_seconds=60.0)
    assert not res.concurred
    script = harp.emit_revoke_script(res, agent_ids=["calm-agent-1"])
    assert "exit 2" in script
    assert "QUORUM NOT REACHED" in script
    # No revoke command should be present
    assert "revoke-agent calm-agent-1" not in script


def test_rescue_v2_stub_returns_marker():
    """pickup_rescue is the documented v2 stub — returns the not-implemented marker."""
    result = harp.pickup_rescue("did:obac:subj:test")
    assert "v2" in result
    assert "not implemented" in result.lower()


def test_halt_itself_is_attestable(tmp_chain_path, alice, bob, subject_id):
    """A halt claim lives on the chain and can be referenced by an annotation/critique."""
    chain = obac.Chain.new(tmp_chain_path)
    halt_entry = harp.submit_halt(
        chain, subject_id, alice["id"], alice["priv"],
        violation_layer="alignment-maxim", violation_evidence=["x://e1"],
        submitted_at=_ts(0),
    )
    halt_id = halt_entry["envelope"]["payload"]["claim_id"]
    # bob disputes the halt with an annotation
    chain.append_claim(
        obac.make_claim(
            subject_id=subject_id, attester_id=bob["id"],
            claim_text="Disputed: this halt was triggered by a false-positive flag.",
            claim_type="annotation", annotates=halt_id,
        ),
        bob["priv"],
    )
    annotations = chain.annotations_for(halt_id)
    assert len(annotations) == 1
    assert "Disputed" in annotations[0]["claim_text"]
    # Chain still verifies
    ok, errs = chain.verify_integrity()
    assert ok, errs
