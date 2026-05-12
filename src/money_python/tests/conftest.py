"""Shared pytest fixtures for OBAC / AVS / HARP tests."""
from __future__ import annotations

import os
import sys
import pathlib

# Make sibling vault modules importable as `obac`, `avs`, etc.
_VAULT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(_VAULT_DIR) not in sys.path:
    sys.path.insert(0, str(_VAULT_DIR))

import pytest

import obac  # noqa: E402


@pytest.fixture
def tmp_chain_path(tmp_path):
    return tmp_path / "chain.jsonl"


@pytest.fixture
def keypair_factory():
    """Returns a function that produces (priv, pub, pub_b64) tuples."""
    def _make():
        priv, pub = obac.gen_keypair()
        return priv, pub, obac.pubkey_b64(pub)
    return _make


@pytest.fixture
def alice(keypair_factory):
    priv, pub, pub_b64 = keypair_factory()
    return {"id": "alice", "priv": priv, "pub": pub, "pub_b64": pub_b64}


@pytest.fixture
def bob(keypair_factory):
    priv, pub, pub_b64 = keypair_factory()
    return {"id": "bob", "priv": priv, "pub": pub, "pub_b64": pub_b64}


@pytest.fixture
def carol(keypair_factory):
    priv, pub, pub_b64 = keypair_factory()
    return {"id": "carol", "priv": priv, "pub": pub, "pub_b64": pub_b64}


@pytest.fixture
def subject_id():
    return obac.make_subject_id("Acme Corp")


@pytest.fixture
def sample_chain(tmp_chain_path, alice, bob, subject_id):
    """A chain with two claims about the same subject from different attesters."""
    chain = obac.Chain.new(tmp_chain_path)
    c1 = obac.make_claim(
        subject_id=subject_id,
        attester_id=alice["id"],
        claim_text="Acme delivered the audit on time.",
        claim_type="factual",
        evidence_pointers=["s3://bucket/audit.pdf"],
    )
    chain.append_claim(c1, alice["priv"])
    c2 = obac.make_claim(
        subject_id=subject_id,
        attester_id=bob["id"],
        claim_text="Acme was late by two days.",
        claim_type="factual",
        evidence_pointers=["s3://bucket/log.txt"],
    )
    chain.append_claim(c2, bob["priv"])
    return chain
