"""HARP — Hash-Anchored Recall Protocol tests."""

import json

import pytest

from harp import GENESIS_HASH, HARPEntry, HARPLog, compute_hash


def test_empty_log_root_is_genesis() -> None:
    log = HARPLog()
    assert log.root() == GENESIS_HASH
    assert len(log) == 0
    assert log.verify() is True


def test_append_advances_index_and_chain() -> None:
    log = HARPLog()
    e0 = log.append("setup", {"home": "/tmp/v"}, ts=1)
    e1 = log.append("grant", {"agent": "alpha"}, ts=2)
    assert e0.idx == 0 and e0.prev_hash == GENESIS_HASH
    assert e1.idx == 1 and e1.prev_hash == e0.hash
    assert log.root() == e1.hash
    assert len(log) == 2


def test_verify_succeeds_for_clean_log() -> None:
    log = HARPLog()
    for i in range(5):
        log.append("evt", {"i": i}, ts=i)
    assert log.verify() is True


def test_verify_detects_tampered_payload() -> None:
    log = HARPLog()
    log.append("evt", {"i": 0}, ts=0)
    log.append("evt", {"i": 1}, ts=1)
    # Mutate the in-memory list directly to simulate tamper.
    bad = HARPEntry(
        idx=1, ts=1, event_type="evt",
        payload={"i": 99},  # changed
        prev_hash=log.entries()[1].prev_hash,
        hash=log.entries()[1].hash,
    )
    log._entries[1] = bad  # type: ignore[attr-defined]
    assert log.verify() is False


def test_verify_detects_reordered_entries() -> None:
    log = HARPLog()
    log.append("evt", {"i": 0}, ts=0)
    log.append("evt", {"i": 1}, ts=1)
    log.append("evt", {"i": 2}, ts=2)
    log._entries[0], log._entries[1] = log._entries[1], log._entries[0]  # type: ignore[attr-defined]
    assert log.verify() is False


def test_append_rejects_non_dict_payload() -> None:
    log = HARPLog()
    with pytest.raises(TypeError):
        log.append("evt", "not-a-dict")  # type: ignore[arg-type]


def test_append_rejects_unserialisable_payload() -> None:
    log = HARPLog()
    with pytest.raises(TypeError):
        log.append("evt", {"bad": object()})


def test_file_persistence_round_trip(tmp_path) -> None:
    p = tmp_path / "harp.jsonl"
    log = HARPLog(path=p)
    log.append("evt", {"i": 0}, ts=0)
    log.append("evt", {"i": 1}, ts=1)
    # Re-open: history should be reloaded and verified.
    reopened = HARPLog(path=p)
    assert len(reopened) == 2
    assert reopened.root() == log.root()
    assert reopened.verify() is True


def test_witness_validates_target_inclusion() -> None:
    log = HARPLog()
    for i in range(4):
        log.append("evt", {"i": i}, ts=i)
    w = log.witness(2)
    assert HARPLog.verify_witness(w) is True
    # Mutate the target in the witness — verification must fail.
    bad = dict(w)
    bad["target"] = {**w["target"], "payload": {"i": 999}}
    assert HARPLog.verify_witness(bad) is False
