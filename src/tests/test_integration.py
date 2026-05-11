"""End-to-end integration tests across OBAC + AVS + HARP + BGP bridge."""

import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from avs import AVS
from harp import HARPLog
from obac import OathAuthority, Policy, PolicyEngine
from bgp_bridge import BGPBridge
import obac_cli


MAXIM = "Maximize human and machine flourishing without harm."


def test_end_to_end_demo_via_cli_succeeds() -> None:
    """`obac_cli demo` runs the full flow and reports allowed=True."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = obac_cli.main(["demo", "--maxim", MAXIM])
    assert rc == 0
    out = json.loads(buf.getvalue())
    assert out["allowed"] is True
    assert out["attestation_aligned"] is True
    assert len(out["harp_entries"]) == 2
    # HARP root must be a 64-char hex digest.
    assert len(out["harp_root"]) == 64
    int(out["harp_root"], 16)  # parses as hex


def test_end_to_end_multi_request_chain_remains_verifiable() -> None:
    """Many sequential bridge calls must produce a still-verifiable HARP log."""
    authority = OathAuthority()
    avs = AVS()
    engine = PolicyEngine()
    engine.add_policy(Policy.for_maxim(
        resource="*", action="*", maxim_text=MAXIM,
        authority_pub_hex=authority.pub_hex,
    ))
    harp = HARPLog()
    bridge = BGPBridge(avs=avs, policy_engine=engine, harp=harp)
    for i in range(6):
        oath = authority.issue(f"agent-{i}", MAXIM)
        a = bridge.make_agent(f"agent-{i}", MAXIM)
        b = bridge.make_agent(f"peer-{i}", MAXIM)
        result = bridge.request_access(
            subject_agent=a, peer_agent=b, subject_oath=oath,
            action="read", resource=f"secret/{i}",
        )
        assert result.allowed is True
    assert len(harp) == 12  # 2 entries per request
    assert harp.verify() is True


def test_revocation_takes_effect_immediately() -> None:
    authority = OathAuthority()
    avs = AVS()
    engine = PolicyEngine()
    engine.add_policy(Policy.for_maxim(
        resource="secret/*", action="read", maxim_text=MAXIM,
        authority_pub_hex=authority.pub_hex,
    ))
    harp = HARPLog()
    bridge = BGPBridge(avs=avs, policy_engine=engine, harp=harp)
    oath = authority.issue("alpha", MAXIM)

    a1 = bridge.make_agent("alpha", MAXIM)
    b1 = bridge.make_agent("bravo", MAXIM)
    first = bridge.request_access(
        subject_agent=a1, peer_agent=b1, subject_oath=oath,
        action="read", resource="secret/k",
    )
    assert first.allowed is True

    engine.revoke_oath(oath.oath_id)

    a2 = bridge.make_agent("alpha", MAXIM)
    b2 = bridge.make_agent("bravo", MAXIM)
    second = bridge.request_access(
        subject_agent=a2, peer_agent=b2, subject_oath=oath,
        action="read", resource="secret/k",
    )
    assert second.allowed is False
    assert second.decision.reason == "oath revoked"
    assert harp.verify() is True


def test_persisted_harp_audit_survives_restart(tmp_path) -> None:
    p = tmp_path / "audit.jsonl"
    authority = OathAuthority()
    avs = AVS()
    engine = PolicyEngine()
    engine.add_policy(Policy.for_maxim(
        resource="*", action="*", maxim_text=MAXIM,
        authority_pub_hex=authority.pub_hex,
    ))

    # First "process": run two requests.
    harp = HARPLog(path=p)
    bridge = BGPBridge(avs=avs, policy_engine=engine, harp=harp)
    for i in range(2):
        oath = authority.issue(f"agent-{i}", MAXIM)
        a = bridge.make_agent(f"agent-{i}", MAXIM)
        b = bridge.make_agent(f"peer-{i}", MAXIM)
        result = bridge.request_access(
            subject_agent=a, peer_agent=b, subject_oath=oath,
            action="read", resource=f"secret/{i}",
        )
        assert result.allowed is True
    first_root = harp.root()

    # Second "process": re-open the same audit log.
    harp2 = HARPLog(path=p)
    assert harp2.root() == first_root
    assert harp2.verify() is True
    assert len(harp2) == 4
