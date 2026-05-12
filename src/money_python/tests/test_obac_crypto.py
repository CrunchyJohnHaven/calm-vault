"""OBAC cryptographic primitives: signatures, hashes, Merkle proofs, chain linkage."""
from __future__ import annotations

import base64
import json
import pytest

import obac


def test_signature_roundtrip(alice, subject_id):
    """A claim signed by alice verifies; tampered signature/payload does not."""
    claim = obac.make_claim(
        subject_id=subject_id,
        attester_id=alice["id"],
        claim_text="Original text.",
    )
    env = obac.sign_claim(claim, alice["priv"])
    assert obac.verify_envelope(env) is True

    # Tamper with claim text — claim_id no longer matches
    env_tampered = json.loads(json.dumps(env))  # deep copy
    env_tampered["payload"]["claim_text"] = "Tampered text."
    assert obac.verify_envelope(env_tampered) is False

    # Tamper with signature bytes — sig verification fails
    env_badsig = json.loads(json.dumps(env))
    bad = bytearray(base64.b64decode(env_badsig["signature"]))
    bad[0] ^= 0x01
    env_badsig["signature"] = base64.b64encode(bytes(bad)).decode()
    assert obac.verify_envelope(env_badsig) is False


def test_content_hash_determinism(alice, subject_id):
    """Two claims with the same payload fields (same nonce + ts) produce identical claim_id."""
    fixed_ts = "2026-05-12T00:00:00+00:00"
    fixed_nonce = base64.b64encode(b"X" * 16).decode()
    c1 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="same", submitted_at=fixed_ts, nonce=fixed_nonce,
    )
    c2 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="same", submitted_at=fixed_ts, nonce=fixed_nonce,
    )
    assert c1["claim_id"] == c2["claim_id"]
    # And: changing any field changes claim_id
    c3 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="DIFFERENT", submitted_at=fixed_ts, nonce=fixed_nonce,
    )
    assert c3["claim_id"] != c1["claim_id"]


def test_claim_id_recomputable(alice, subject_id):
    """claim_id_for(payload) recomputes the same value."""
    c = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"], claim_text="abc",
    )
    assert obac.claim_id_for(c) == c["claim_id"]


def test_chain_linkage(tmp_chain_path, alice, bob, subject_id):
    """Each entry's prev_hash equals the prior entry's entry_hash; genesis has zero prev."""
    chain = obac.Chain.new(tmp_chain_path)
    assert chain.head_hash() == obac.GENESIS_PREV_HASH

    e1 = chain.append_claim(
        obac.make_claim(subject_id=subject_id, attester_id=alice["id"],
                        claim_text="first"),
        alice["priv"],
    )
    assert e1["seq"] == 0
    assert e1["prev_hash"] == obac.GENESIS_PREV_HASH
    assert e1["prev_hash"] == "0" * 64

    e2 = chain.append_claim(
        obac.make_claim(subject_id=subject_id, attester_id=bob["id"],
                        claim_text="second"),
        bob["priv"],
    )
    assert e2["seq"] == 1
    assert e2["prev_hash"] == e1["entry_hash"]


def test_genesis_prev_hash_is_zero(tmp_chain_path, alice, subject_id):
    """The first entry on a fresh chain must have prev_hash = 64 zero hex chars."""
    chain = obac.Chain.new(tmp_chain_path)
    e = chain.append_claim(
        obac.make_claim(subject_id=subject_id, attester_id=alice["id"],
                        claim_text="genesis"),
        alice["priv"],
    )
    assert e["prev_hash"] == "0" * 64
    assert len(e["entry_hash"]) == 64
    assert all(c in "0123456789abcdef" for c in e["entry_hash"])


def test_merkle_proof_roundtrip(tmp_chain_path, alice, subject_id):
    """For every entry in a chain, generate a Merkle proof and verify it."""
    chain = obac.Chain.new(tmp_chain_path)
    for i in range(7):  # odd number forces tree-padding logic
        chain.append_claim(
            obac.make_claim(subject_id=subject_id, attester_id=alice["id"],
                            claim_text=f"claim {i}"),
            alice["priv"],
        )
    root = chain.merkle_root()
    for i in range(7):
        leaf = chain.entries[i]["entry_hash"]
        proof = chain.merkle_proof(i)
        assert obac.verify_merkle_proof(leaf, proof, root), \
            f"merkle proof failed for entry {i}"


def test_merkle_proof_rejects_wrong_leaf(tmp_chain_path, alice, subject_id):
    """A proof for entry i should not verify a different leaf hash."""
    chain = obac.Chain.new(tmp_chain_path)
    for i in range(4):
        chain.append_claim(
            obac.make_claim(subject_id=subject_id, attester_id=alice["id"],
                            claim_text=f"claim {i}"),
            alice["priv"],
        )
    root = chain.merkle_root()
    proof = chain.merkle_proof(2)
    wrong_leaf = chain.entries[0]["entry_hash"]
    assert obac.verify_merkle_proof(wrong_leaf, proof, root) is False


def test_duplicate_nonce_rejected(tmp_chain_path, alice, subject_id):
    """The chain refuses to append a second claim with a previously-seen nonce."""
    chain = obac.Chain.new(tmp_chain_path)
    nonce = obac.random_nonce()
    c1 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="first", nonce=nonce,
    )
    chain.append_claim(c1, alice["priv"])

    # Second claim with same nonce but different text — must fail to append
    c2 = obac.make_claim(
        subject_id=subject_id, attester_id=alice["id"],
        claim_text="second", nonce=nonce,
    )
    with pytest.raises(ValueError, match="duplicate nonce"):
        chain.append_claim(c2, alice["priv"])
