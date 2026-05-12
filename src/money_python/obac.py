#!/usr/bin/env python3
"""
OBAC — Origin-Bound Attestation Chain.

Tamper-evident, hash-linked, append-only ledger of signed claims about a subject.
Provides cryptographic provenance: every claim is signed by its attester, every
chain entry links to its predecessor by hash, and the chain itself can be Merkle-
summarized for O(log n) proof of inclusion.

Schema
------
Claim = {
    "schema_version": "obac/1",
    "claim_id": str,                # sha256(canonical_json(payload-excluding-claim_id))
    "subject_id": str,              # subject the claim is about
    "attester_id": str,             # logical attester identity (human/agent string)
    "claim_text": str,              # max 4096 chars
    "claim_type": str,              # factual|opinion|critique|endorsement|annotation|halt
    "evidence_pointers": list[str],
    "annotates": str | None,        # claim_id this annotates (only if claim_type=="annotation")
    "submitted_at": str,            # ISO-8601 UTC
    "nonce": str                    # base64 16 random bytes, unique across chain
}

ClaimEnvelope = {
    "payload": Claim,
    "signature": str,               # base64 Ed25519 over canonical_json(payload)
    "attester_pub": str             # base64 raw 32-byte Ed25519 pubkey
}

ChainEntry = {
    "seq": int,
    "envelope": ClaimEnvelope,
    "prev_hash": str,               # 64-hex; "0"*64 for genesis
    "entry_hash": str               # sha256(canonical_json({seq, envelope, prev_hash}))
}

Design notes
------------
- Single-writer assumption for chain.jsonl (documented, not enforced in v1).
- Pure stdlib + cryptography; no extra deps.
- The chain is append-only on disk. Tamper-evidence comes from:
  1. Ed25519 signatures on every payload.
  2. Hash links: prev_hash references prior entry_hash.
  3. Entry hash includes seq, so out-of-order insertion changes downstream hashes.
- Merkle root computed on demand from entry_hash values (binary tree, duplicated
  rightmost leaf if odd).

Subject DIDs (did:obac:<sha256(pubkey)[:16]>) are convenience identifiers; the
canonical subject identifier is whatever the chain creator chose. Different
subjects live on different chain files.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import pathlib
import secrets
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


SCHEMA_VERSION = "obac/1"
MAX_CLAIM_TEXT = 4096
GENESIS_PREV_HASH = "0" * 64
VALID_CLAIM_TYPES = {
    "factual",
    "opinion",
    "critique",
    "endorsement",
    "annotation",
    "halt",
}


# ---------------------------------------------------------------------------
# Canonical encoding helpers
# ---------------------------------------------------------------------------


def canonical_json(obj: Any) -> bytes:
    """Stable canonical JSON encoding: sort keys, no spaces."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def random_nonce() -> str:
    return base64.b64encode(secrets.token_bytes(16)).decode("ascii")


# ---------------------------------------------------------------------------
# Key helpers
# ---------------------------------------------------------------------------


def gen_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    priv = Ed25519PrivateKey.generate()
    return priv, priv.public_key()


def pubkey_bytes(pub: Ed25519PublicKey) -> bytes:
    return pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


def pubkey_b64(pub: Ed25519PublicKey) -> str:
    return base64.b64encode(pubkey_bytes(pub)).decode("ascii")


def pubkey_from_b64(s: str) -> Ed25519PublicKey:
    return Ed25519PublicKey.from_public_bytes(base64.b64decode(s))


def did_for_pubkey(pub: Ed25519PublicKey) -> str:
    """did:obac:<first 16 hex chars of sha256(raw pubkey)>"""
    return "did:obac:" + sha256_hex(pubkey_bytes(pub))[:16]


# ---------------------------------------------------------------------------
# Claim construction
# ---------------------------------------------------------------------------


def make_claim(
    subject_id: str,
    attester_id: str,
    claim_text: str,
    claim_type: str = "factual",
    evidence_pointers: Optional[list[str]] = None,
    annotates: Optional[str] = None,
    submitted_at: Optional[str] = None,
    nonce: Optional[str] = None,
) -> dict:
    """Construct a Claim dict with a deterministic claim_id."""
    if claim_type not in VALID_CLAIM_TYPES:
        raise ValueError(f"invalid claim_type: {claim_type}")
    if len(claim_text) > MAX_CLAIM_TEXT:
        raise ValueError(f"claim_text exceeds {MAX_CLAIM_TEXT} chars")
    if claim_type == "annotation" and not annotates:
        raise ValueError("annotation claims must reference annotates=<claim_id>")
    if annotates is not None and claim_type != "annotation":
        raise ValueError("annotates field requires claim_type='annotation'")

    payload_no_id = {
        "schema_version": SCHEMA_VERSION,
        "subject_id": subject_id,
        "attester_id": attester_id,
        "claim_text": claim_text,
        "claim_type": claim_type,
        "evidence_pointers": list(evidence_pointers or []),
        "annotates": annotates,
        "submitted_at": submitted_at or now_iso(),
        "nonce": nonce or random_nonce(),
    }
    claim_id = sha256_hex(canonical_json(payload_no_id))
    return {"claim_id": claim_id, **payload_no_id}


def claim_id_for(payload: dict) -> str:
    """Recompute claim_id deterministically from payload (claim_id excluded)."""
    p = {k: v for k, v in payload.items() if k != "claim_id"}
    return sha256_hex(canonical_json(p))


def sign_claim(
    claim: dict, attester_priv: Ed25519PrivateKey
) -> dict:
    """Wrap a Claim in a signed envelope."""
    sig = attester_priv.sign(canonical_json(claim))
    return {
        "payload": claim,
        "signature": base64.b64encode(sig).decode("ascii"),
        "attester_pub": pubkey_b64(attester_priv.public_key()),
    }


def verify_envelope(envelope: dict) -> bool:
    """Verify (a) claim_id matches payload, (b) Ed25519 sig matches payload."""
    payload = envelope["payload"]
    expected_id = claim_id_for(payload)
    if payload.get("claim_id") != expected_id:
        return False
    try:
        pub = pubkey_from_b64(envelope["attester_pub"])
        sig = base64.b64decode(envelope["signature"])
        pub.verify(sig, canonical_json(payload))
    except (InvalidSignature, Exception):
        return False
    return True


# ---------------------------------------------------------------------------
# Chain entry construction
# ---------------------------------------------------------------------------


def make_entry(seq: int, envelope: dict, prev_hash: str) -> dict:
    """Build a chain entry and compute its entry_hash."""
    body = {"seq": seq, "envelope": envelope, "prev_hash": prev_hash}
    entry_hash = sha256_hex(canonical_json(body))
    return {**body, "entry_hash": entry_hash}


def entry_hash_for(entry: dict) -> str:
    """Recompute entry_hash from {seq, envelope, prev_hash}."""
    body = {
        "seq": entry["seq"],
        "envelope": entry["envelope"],
        "prev_hash": entry["prev_hash"],
    }
    return sha256_hex(canonical_json(body))


# ---------------------------------------------------------------------------
# Merkle root over entry_hash values
# ---------------------------------------------------------------------------


def merkle_root(entry_hashes: list[str]) -> str:
    """Binary Merkle root over hex hashes. Duplicates last leaf if odd."""
    if not entry_hashes:
        return GENESIS_PREV_HASH
    level = [bytes.fromhex(h) for h in entry_hashes]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level = []
        for i in range(0, len(level), 2):
            next_level.append(hashlib.sha256(level[i] + level[i + 1]).digest())
        level = next_level
    return level[0].hex()


def merkle_proof(entry_hashes: list[str], index: int) -> list[tuple[str, str]]:
    """Inclusion proof for entry_hashes[index].

    Returns a list of (sibling_hash, side) where side is 'L' or 'R' (sibling is
    on the left or right when hashing).
    """
    if index < 0 or index >= len(entry_hashes):
        raise IndexError("index out of range")
    proof: list[tuple[str, str]] = []
    level = [bytes.fromhex(h) for h in entry_hashes]
    idx = index
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        sibling_idx = idx ^ 1
        side = "L" if sibling_idx < idx else "R"
        proof.append((level[sibling_idx].hex(), side))
        next_level = []
        for i in range(0, len(level), 2):
            next_level.append(hashlib.sha256(level[i] + level[i + 1]).digest())
        level = next_level
        idx //= 2
    return proof


def verify_merkle_proof(
    leaf_hash: str, proof: list[tuple[str, str]], root: str
) -> bool:
    """Verify a Merkle inclusion proof."""
    cur = bytes.fromhex(leaf_hash)
    for sibling_hex, side in proof:
        sib = bytes.fromhex(sibling_hex)
        if side == "L":
            cur = hashlib.sha256(sib + cur).digest()
        else:
            cur = hashlib.sha256(cur + sib).digest()
    return cur.hex() == root


# ---------------------------------------------------------------------------
# Chain class
# ---------------------------------------------------------------------------


@dataclass
class Chain:
    """In-memory + on-disk OBAC chain.

    Disk format: JSONL — one ChainEntry per line, append-only. Single-writer
    assumption (no fcntl locking in v1; documented limitation).
    """

    path: pathlib.Path
    entries: list[dict] = field(default_factory=list)
    _seen_nonces: set[str] = field(default_factory=set)

    @classmethod
    def open(cls, path: str | os.PathLike) -> "Chain":
        p = pathlib.Path(path)
        c = cls(path=p)
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                e = json.loads(line)
                c.entries.append(e)
                c._seen_nonces.add(e["envelope"]["payload"]["nonce"])
        return c

    @classmethod
    def new(cls, path: str | os.PathLike) -> "Chain":
        """Create a fresh chain (clears any existing file at path)."""
        p = pathlib.Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            p.unlink()
        return cls(path=p)

    def head_hash(self) -> str:
        if not self.entries:
            return GENESIS_PREV_HASH
        return self.entries[-1]["entry_hash"]

    def next_seq(self) -> int:
        return len(self.entries)

    def append_envelope(self, envelope: dict) -> dict:
        """Append a signed envelope to the chain. Raises on bad sig / dup nonce."""
        if not verify_envelope(envelope):
            raise ValueError("envelope failed signature/claim-id verification")
        nonce = envelope["payload"]["nonce"]
        if nonce in self._seen_nonces:
            raise ValueError(f"duplicate nonce: {nonce!r}")
        entry = make_entry(
            seq=self.next_seq(),
            envelope=envelope,
            prev_hash=self.head_hash(),
        )
        self.entries.append(entry)
        self._seen_nonces.add(nonce)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def append_claim(self, claim: dict, attester_priv: Ed25519PrivateKey) -> dict:
        """Convenience: sign + append in one call."""
        env = sign_claim(claim, attester_priv)
        return self.append_envelope(env)

    def merkle_root(self) -> str:
        return merkle_root([e["entry_hash"] for e in self.entries])

    def merkle_proof(self, seq: int) -> list[tuple[str, str]]:
        return merkle_proof([e["entry_hash"] for e in self.entries], seq)

    def find(self, claim_id: str) -> Optional[dict]:
        """Return chain entry containing claim_id, or None."""
        for e in self.entries:
            if e["envelope"]["payload"]["claim_id"] == claim_id:
                return e
        return None

    def claims_about(self, subject_id: str) -> list[dict]:
        return [
            e["envelope"]["payload"]
            for e in self.entries
            if e["envelope"]["payload"]["subject_id"] == subject_id
            and e["envelope"]["payload"]["claim_type"] != "annotation"
        ]

    def annotations_for(self, claim_id: str) -> list[dict]:
        return [
            e["envelope"]["payload"]
            for e in self.entries
            if e["envelope"]["payload"]["claim_type"] == "annotation"
            and e["envelope"]["payload"]["annotates"] == claim_id
        ]

    def attester_pubkey(self, attester_id: str) -> Optional[str]:
        """Return the (base64) Ed25519 pubkey used by an attester_id, if seen."""
        for e in self.entries:
            p = e["envelope"]["payload"]
            if p["attester_id"] == attester_id:
                return e["envelope"]["attester_pub"]
        return None

    # ---------- verification ----------

    def verify_integrity(self) -> tuple[bool, list[str]]:
        """Full chain integrity check. Returns (ok, errors)."""
        errors: list[str] = []
        seen_nonces: set[str] = set()
        prev = GENESIS_PREV_HASH
        for i, e in enumerate(self.entries):
            if e["seq"] != i:
                errors.append(f"entry {i}: seq mismatch (got {e['seq']})")
            if e["prev_hash"] != prev:
                errors.append(
                    f"entry {i}: prev_hash {e['prev_hash'][:12]}... != expected {prev[:12]}..."
                )
            expected_hash = entry_hash_for(e)
            if expected_hash != e["entry_hash"]:
                errors.append(f"entry {i}: entry_hash recomputation mismatch")
            if not verify_envelope(e["envelope"]):
                errors.append(f"entry {i}: envelope signature/claim-id invalid")
            nonce = e["envelope"]["payload"]["nonce"]
            if nonce in seen_nonces:
                errors.append(f"entry {i}: duplicate nonce {nonce!r}")
            seen_nonces.add(nonce)
            prev = e["entry_hash"]
        return (len(errors) == 0, errors)


# ---------------------------------------------------------------------------
# Subject convenience
# ---------------------------------------------------------------------------


def make_subject_id(label: str) -> str:
    """Stable subject_id for a free-form label (e.g. an org name)."""
    return "did:obac:subj:" + sha256_hex(label.encode("utf-8"))[:16]


# ---------------------------------------------------------------------------
# __main__ — quick demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl") as tf:
        path = tf.name
    chain = Chain.new(path)
    priv, pub = gen_keypair()
    subj = make_subject_id("Acme Corp")
    c = make_claim(
        subject_id=subj,
        attester_id="alice",
        claim_text="Acme delivered the audit on time.",
        claim_type="factual",
        evidence_pointers=["s3://bucket/audit.pdf"],
    )
    chain.append_claim(c, priv)
    ok, errs = chain.verify_integrity()
    print(json.dumps({
        "path": path,
        "entries": len(chain.entries),
        "head_hash": chain.head_hash()[:16],
        "merkle_root": chain.merkle_root()[:16],
        "integrity_ok": ok,
        "errors": errs,
    }, indent=2))
