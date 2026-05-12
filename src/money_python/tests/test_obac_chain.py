"""OBAC chain tamper-evidence: any post-hoc modification should fail integrity check."""
from __future__ import annotations

import json
import pathlib
import pytest

import obac


def _populate(chain: obac.Chain, attesters: list[dict], subject_id: str, n: int) -> obac.Chain:
    """Helper: append n claims, rotating attesters."""
    for i in range(n):
        a = attesters[i % len(attesters)]
        chain.append_claim(
            obac.make_claim(
                subject_id=subject_id,
                attester_id=a["id"],
                claim_text=f"claim number {i}",
            ),
            a["priv"],
        )
    return chain


def test_baseline_chain_passes_integrity(tmp_chain_path, alice, bob, subject_id):
    """A clean chain passes verify_integrity."""
    chain = obac.Chain.new(tmp_chain_path)
    _populate(chain, [alice, bob], subject_id, 5)
    ok, errors = chain.verify_integrity()
    assert ok, f"unexpected errors: {errors}"
    assert errors == []


def test_payload_tamper_detected(tmp_chain_path, alice, bob, subject_id):
    """Modifying a claim's text in-place should fail integrity (claim_id + sig both invalid)."""
    chain = obac.Chain.new(tmp_chain_path)
    _populate(chain, [alice, bob], subject_id, 3)

    # Tamper with entry 1's claim text in-memory
    chain.entries[1]["envelope"]["payload"]["claim_text"] = "CORRUPTED"
    ok, errors = chain.verify_integrity()
    assert not ok
    # The entry_hash was computed over the original envelope, so changing
    # the payload also breaks entry_hash recomputation AND the signature.
    assert any("signature" in e or "entry_hash" in e for e in errors)


def test_truncation_detected_via_merkle_root(tmp_chain_path, alice, bob, subject_id):
    """Truncating the chain changes the Merkle root."""
    chain = obac.Chain.new(tmp_chain_path)
    _populate(chain, [alice, bob], subject_id, 6)
    full_root = chain.merkle_root()

    truncated = obac.Chain(path=chain.path, entries=chain.entries[:4])
    truncated_root = obac.merkle_root([e["entry_hash"] for e in truncated.entries])
    assert truncated_root != full_root, (
        "truncation must change the Merkle root"
    )


def test_mid_chain_splice_breaks_linkage(tmp_chain_path, alice, bob, carol, subject_id):
    """Inserting a forged entry in the middle breaks the prev_hash chain."""
    chain = obac.Chain.new(tmp_chain_path)
    _populate(chain, [alice, bob], subject_id, 4)

    # Carol forges an entry pretending to be at position 2 with a valid sig of her own
    forged_claim = obac.make_claim(
        subject_id=subject_id, attester_id=carol["id"],
        claim_text="forged splice",
    )
    forged_env = obac.sign_claim(forged_claim, carol["priv"])
    # Use the prev_hash that was correct at position 2 originally
    spliced_entry = obac.make_entry(
        seq=2,
        envelope=forged_env,
        prev_hash=chain.entries[1]["entry_hash"],
    )

    # Splice it in (push existing entries forward — they now have wrong prev_hash refs)
    chain.entries.insert(2, spliced_entry)

    ok, errors = chain.verify_integrity()
    assert not ok
    # The downstream entries now have stale prev_hash references and wrong seq
    assert any("prev_hash" in e or "seq mismatch" in e for e in errors)


def test_replay_resistance_duplicate_nonce(tmp_chain_path, alice, subject_id):
    """A second claim attempt with the same nonce is rejected at append-time."""
    chain = obac.Chain.new(tmp_chain_path)
    nonce = obac.random_nonce()
    c1 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="first use of nonce", nonce=nonce,
    )
    chain.append_claim(c1, alice["priv"])

    c2 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="replay attempt", nonce=nonce,
    )
    with pytest.raises(ValueError, match="duplicate nonce"):
        chain.append_claim(c2, alice["priv"])

    # Confirm chain is still healthy
    ok, errors = chain.verify_integrity()
    assert ok, errors


def test_nonce_uniqueness_persists_across_reload(tmp_chain_path, alice, subject_id):
    """A reopened chain refuses to accept a nonce that was used in the on-disk history."""
    chain = obac.Chain.new(tmp_chain_path)
    nonce = obac.random_nonce()
    chain.append_claim(
        obac.make_claim(subject_id=subject_id, attester_id=alice["id"],
                        claim_text="original", nonce=nonce),
        alice["priv"],
    )

    # Reopen the chain from disk
    chain2 = obac.Chain.open(tmp_chain_path)
    assert nonce in chain2._seen_nonces

    c_dup = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="reopened replay attempt", nonce=nonce,
    )
    with pytest.raises(ValueError, match="duplicate nonce"):
        chain2.append_claim(c_dup, alice["priv"])
