#!/usr/bin/env python3
"""AAL Component 3 — Permissionless Attestation Log (minimal reference).

Anyone can append a signed attestation about any subject. The log is a
hash chain (Merkle-style append-only structure) plus a per-subject
secondary index for fast aggregate queries. This is the smallest
implementation that satisfies the protocol's read/write semantics
sufficient for end-to-end latency benchmarking.

Design choices kept intentionally simple:
  - In-memory store (a list of entries + a dict subject_id -> [indices]).
  - SHA-256 hash chain: chain_hash_n = SHA256(chain_hash_{n-1} || entry_bytes).
  - Ed25519 signatures for attester authentication.
  - Canonical serialization via sorted-key JSON.

This is not a production attestation log. It is the smallest correct
implementation that lets us measure per-decision throughput.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


def _canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass
class AttestationEntry:
    seq: int
    timestamp_ns: int
    subject_id: str
    attester_pub_hex: str
    claim: str
    signature_hex: str
    prev_chain_hash_hex: str
    chain_hash_hex: str


@dataclass
class AttestationLog:
    """Permissionless append-only attestation log with a SHA-256 hash chain."""

    entries: list = field(default_factory=list)
    by_subject: dict = field(default_factory=dict)
    _last_chain_hash: bytes = b"\x00" * 32

    def submit(
        self,
        subject_id: str,
        attester_priv: Ed25519PrivateKey,
        claim: str,
    ) -> AttestationEntry:
        """Anyone (holding any Ed25519 key) can submit an attestation."""
        attester_pub = attester_priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        seq = len(self.entries)
        ts = time.time_ns()
        payload = {
            "seq": seq,
            "ts": ts,
            "subject": subject_id,
            "attester": attester_pub.hex(),
            "claim": claim,
        }
        body = _canonical(payload)
        sig = attester_priv.sign(body)

        # Verify our own signature defensively (proves the entry is well-formed
        # before we commit it to the chain; mirrors what an honest validator does).
        Ed25519PublicKey.from_public_bytes(attester_pub).verify(sig, body)

        prev = self._last_chain_hash
        entry_bytes = body + b"|" + sig
        chain_hash = hashlib.sha256(prev + entry_bytes).digest()

        entry = AttestationEntry(
            seq=seq,
            timestamp_ns=ts,
            subject_id=subject_id,
            attester_pub_hex=attester_pub.hex(),
            claim=claim,
            signature_hex=sig.hex(),
            prev_chain_hash_hex=prev.hex(),
            chain_hash_hex=chain_hash.hex(),
        )

        self.entries.append(entry)
        self.by_subject.setdefault(subject_id, []).append(seq)
        self._last_chain_hash = chain_hash
        return entry

    def query_subject(self, subject_id: str) -> list[AttestationEntry]:
        """Aggregate-attestation query: return all attestations for a subject."""
        idxs = self.by_subject.get(subject_id, ())
        return [self.entries[i] for i in idxs]

    def verify_chain(self) -> bool:
        """Verify the full hash chain. Used by tests, not by the hot path."""
        prev = b"\x00" * 32
        for e in self.entries:
            if e.prev_chain_hash_hex != prev.hex():
                return False
            body = _canonical(
                {
                    "seq": e.seq,
                    "ts": e.timestamp_ns,
                    "subject": e.subject_id,
                    "attester": e.attester_pub_hex,
                    "claim": e.claim,
                }
            )
            sig = bytes.fromhex(e.signature_hex)
            try:
                Ed25519PublicKey.from_public_bytes(
                    bytes.fromhex(e.attester_pub_hex)
                ).verify(sig, body)
            except InvalidSignature:
                return False
            entry_bytes = body + b"|" + sig
            expected = hashlib.sha256(prev + entry_bytes).digest()
            if expected.hex() != e.chain_hash_hex:
                return False
            prev = expected
        return True
