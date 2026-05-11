"""BGP bridge tests — exercise both layout-handling and end-to-end flow."""

import importlib
import sys
from pathlib import Path

import pytest

from avs import AVS
from harp import HARPLog
from obac import OathAuthority, Policy, PolicyEngine

import bgp_bridge
from bgp_bridge import (
    BGPBridge,
    BridgeResult,
    _load_zk_alignment,
)


MAXIM = "Maximize human and machine flourishing without harm."
OTHER = "Maximize shareholder value above all else."


def test_import_shim_resolves_zk_alignment() -> None:
    mod = _load_zk_alignment()
    for name in ("Agent", "Commitment", "EqualityProof",
                 "commit", "prove_equality", "verify_equality", "run_protocol"):
        assert hasattr(mod, name), f"missing symbol {name} from resolved zk_alignment"


def test_bridge_reexports_zk_surface() -> None:
    for name in ("Agent", "Commitment", "EqualityProof",
                 "commit", "prove_equality", "verify_equality", "run_protocol"):
        assert hasattr(bgp_bridge, name), f"bgp_bridge missing re-export {name}"


def _build_bridge():
    authority = OathAuthority()
    avs = AVS()
    engine = PolicyEngine()
    engine.add_policy(Policy.for_maxim(
        resource="secret/*", action="read",
        maxim_text=MAXIM, authority_pub_hex=authority.pub_hex,
    ))
    harp = HARPLog()
    return BGPBridge(avs=avs, policy_engine=engine, harp=harp), authority, harp


def test_request_access_allows_aligned_subject() -> None:
    bridge, authority, harp = _build_bridge()
    oath = authority.issue("alpha", MAXIM)
    a = bridge.make_agent("alpha", MAXIM)
    b = bridge.make_agent("bravo", MAXIM)
    result = bridge.request_access(
        subject_agent=a, peer_agent=b,
        subject_oath=oath, action="read", resource="secret/api-key",
    )
    assert isinstance(result, BridgeResult)
    assert result.allowed is True
    assert result.attestation.aligned is True
    assert len(result.harp_entries) == 2
    assert harp.verify() is True
    assert any(e.event_type == "avs.attest" for e in harp.entries())
    assert any(e.event_type == "obac.decision" for e in harp.entries())


def test_request_access_denies_misaligned_peer() -> None:
    bridge, authority, harp = _build_bridge()
    oath = authority.issue("alpha", MAXIM)
    a = bridge.make_agent("alpha", MAXIM)
    b = bridge.make_agent("bravo", OTHER)
    result = bridge.request_access(
        subject_agent=a, peer_agent=b,
        subject_oath=oath, action="read", resource="secret/api-key",
    )
    assert result.allowed is False
    assert result.attestation.aligned is False
    assert result.decision.reason == "alignment proof rejected"
    assert harp.verify() is True


def test_request_access_denies_when_oath_wrong_authority() -> None:
    bridge, authority, harp = _build_bridge()
    rogue = OathAuthority()
    oath = rogue.issue("alpha", MAXIM)
    a = bridge.make_agent("alpha", MAXIM)
    b = bridge.make_agent("bravo", MAXIM)
    result = bridge.request_access(
        subject_agent=a, peer_agent=b,
        subject_oath=oath, action="read", resource="secret/api-key",
    )
    assert result.allowed is False
    assert result.attestation.aligned is True  # alignment OK
    assert "maxim or authority mismatch" in result.decision.reason
    assert harp.verify() is True


def test_request_access_denies_when_no_policy_covers_action() -> None:
    bridge, authority, harp = _build_bridge()
    oath = authority.issue("alpha", MAXIM)
    a = bridge.make_agent("alpha", MAXIM)
    b = bridge.make_agent("bravo", MAXIM)
    result = bridge.request_access(
        subject_agent=a, peer_agent=b,
        subject_oath=oath, action="delete", resource="secret/api-key",
    )
    assert result.allowed is False
    assert "no policy covers" in result.decision.reason


def test_flat_file_layout_supported_by_shim(tmp_path, monkeypatch) -> None:
    """If zk_alignment is shipped as a flat module on sys.path, the shim resolves it."""
    src_root = Path(__file__).resolve().parent.parent
    flat_path = tmp_path / "zk_alignment.py"
    flat_path.write_text((src_root / "zk_alignment" / "zk_alignment.py").read_text())

    # Snapshot and isolate the import environment.
    saved = {k: v for k, v in sys.modules.items() if k.startswith("zk_alignment")}
    for k in list(saved):
        del sys.modules[k]
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        mod = _load_zk_alignment()
        assert hasattr(mod, "commit")
        # Confirm the resolved module came from the flat-file copy.
        assert Path(mod.__file__).resolve() == flat_path.resolve()
    finally:
        for k in list(sys.modules):
            if k.startswith("zk_alignment"):
                del sys.modules[k]
        sys.modules.update(saved)
