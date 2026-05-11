#!/usr/bin/env python3
"""
HARP — Hash-Anchored Recall Protocol.

An append-only, tamper-evident audit log. Every entry carries:
- a strictly monotonic index,
- a timestamp,
- an event type,
- a JSON-serialisable payload,
- the hash of the previous entry (or all-zeros for the genesis),
- its own hash = SHA256(prev_hash || canonical(payload) || idx || ts || event_type).

The chain hash at any point is a witness to the entire prefix of the log — any
modification, deletion, or reordering breaks verification. HARP is the audit
substrate the BGP bridge uses to anchor OBAC decisions and AVS attestations so
that any agent action can be reconstructed and replayed offline.

Optional file persistence: pass a Path to HARPLog and it'll append one
JSON-lines record per entry. Recovery just re-reads the file and re-verifies
the chain.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, Optional


GENESIS_HASH = "0" * 64


@dataclass(frozen=True)
class HARPEntry:
    idx: int
    ts: int
    event_type: str
    payload: dict
    prev_hash: str
    hash: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "HARPEntry":
        return HARPEntry(
            idx=int(d["idx"]),
            ts=int(d["ts"]),
            event_type=str(d["event_type"]),
            payload=dict(d["payload"]),
            prev_hash=str(d["prev_hash"]),
            hash=str(d["hash"]),
        )


def _canonical(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_hash(idx: int, ts: int, event_type: str, payload: dict, prev_hash: str) -> str:
    h = hashlib.sha256()
    h.update(str(idx).encode("ascii"))
    h.update(b"|")
    h.update(str(ts).encode("ascii"))
    h.update(b"|")
    h.update(event_type.encode("utf-8"))
    h.update(b"|")
    h.update(_canonical(payload))
    h.update(b"|")
    h.update(prev_hash.encode("ascii"))
    return h.hexdigest()


class HARPLog:
    """In-memory log with optional append-only file persistence."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self._entries: list[HARPEntry] = []
        self._path: Optional[Path] = Path(path) if path is not None else None
        if self._path is not None and self._path.exists():
            self._load()

    # --- core ---

    def append(
        self,
        event_type: str,
        payload: dict,
        *,
        ts: Optional[int] = None,
    ) -> HARPEntry:
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("event_type must be a non-empty string")
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dict")
        # canonicalisation roundtrip catches non-serialisable values now
        try:
            json.dumps(payload, sort_keys=True)
        except (TypeError, ValueError) as exc:
            raise TypeError(f"payload is not JSON-serialisable: {exc}") from exc

        idx = len(self._entries)
        t = int(ts if ts is not None else time.time())
        prev_hash = self._entries[-1].hash if self._entries else GENESIS_HASH
        entry_hash = compute_hash(idx, t, event_type, payload, prev_hash)
        entry = HARPEntry(
            idx=idx, ts=t, event_type=event_type,
            payload=payload, prev_hash=prev_hash, hash=entry_hash,
        )
        self._entries.append(entry)
        if self._path is not None:
            with self._path.open("a") as fh:
                fh.write(json.dumps(entry.to_dict(), sort_keys=True) + "\n")
        return entry

    # --- introspection ---

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterable[HARPEntry]:
        return iter(self._entries)

    def entries(self) -> list[HARPEntry]:
        return list(self._entries)

    def root(self) -> str:
        return self._entries[-1].hash if self._entries else GENESIS_HASH

    # --- verification ---

    def verify(self) -> bool:
        """Return True iff every entry's hash matches its content + prev_hash."""
        prev = GENESIS_HASH
        for i, e in enumerate(self._entries):
            if e.idx != i:
                return False
            if e.prev_hash != prev:
                return False
            if compute_hash(e.idx, e.ts, e.event_type, e.payload, e.prev_hash) != e.hash:
                return False
            prev = e.hash
        return True

    # --- persistence ---

    def _load(self) -> None:
        with self._path.open("r") as fh:  # type: ignore[union-attr]
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                self._entries.append(HARPEntry.from_dict(json.loads(line)))
        if not self.verify():
            raise ValueError(f"HARP log at {self._path} failed verification on load")

    # --- proof of inclusion (simple linear witness) ---

    def witness(self, idx: int) -> dict:
        """Return enough material to reproduce the hash chain so a third party
        can verify that `target` sits at position `idx` in a log whose final
        chain head is `root`. We ship the full chain — this is a linear log,
        not a Merkle tree."""
        if idx < 0 or idx >= len(self._entries):
            raise IndexError(f"idx out of range: {idx}")
        return {
            "target": self._entries[idx].to_dict(),
            "chain": [e.to_dict() for e in self._entries],
            "root": self.root(),
        }

    @staticmethod
    def verify_witness(witness: dict) -> bool:
        try:
            chain = [HARPEntry.from_dict(e) for e in witness["chain"]]
            target = HARPEntry.from_dict(witness["target"])
            root = witness["root"]
        except (KeyError, TypeError, ValueError):
            return False
        if not chain or chain[-1].hash != root:
            return False
        if target.idx < 0 or target.idx >= len(chain):
            return False
        if chain[target.idx].to_dict() != target.to_dict():
            return False
        prev = GENESIS_HASH
        for i, e in enumerate(chain):
            if e.idx != i:
                return False
            if e.prev_hash != prev:
                return False
            if compute_hash(e.idx, e.ts, e.event_type, e.payload, e.prev_hash) != e.hash:
                return False
            prev = e.hash
        return True


__all__ = [
    "HARPEntry",
    "HARPLog",
    "GENESIS_HASH",
    "compute_hash",
]
