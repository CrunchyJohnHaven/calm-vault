#!/usr/bin/env python3
"""AAL Component 5 — Permissionless Kill Switch (minimal reference).

ANY participant in the network can fire the kill switch on a target entity.
A FireMessage is a signed, canonical record naming the target. Honest
validators verify the signature and commit the target to the frozen set.
Once frozen, the target's authority is revoked: every subsequent action
attempted by the target returns FROZEN.

Latency definition (matches the manifesto's claim):
    fire-to-freeze = time from the moment a fire() call is initiated to
    the moment the target's status flips to FROZEN in the registry.

This minimal implementation collapses the network into a single in-process
KillSwitchRegistry — the cryptographic work and the freeze-state mutation
are exactly what an honest validator performs; we just measure that
work directly without the network-transport overhead, which is what the
manifesto's "millisecond" claim is about (the protocol step, not the
gossip / propagation).
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
class FireMessage:
    target_id: str
    fired_by_pub_hex: str
    reason: str
    timestamp_ns: int
    signature_hex: str
    digest_hex: str


@dataclass
class KillSwitchRegistry:
    """The shared registry validators consult to decide if an entity is frozen."""

    frozen: dict = field(default_factory=dict)  # target_id -> FireMessage
    # Permissionless: anyone with an Ed25519 key can fire. We do NOT consult an
    # allowlist; a real production deployment would gate by stake/quorum, but
    # for the latency benchmark the protocol cost is the signature-verify
    # plus a single map mutation, regardless of access policy.

    def fire(
        self,
        target_id: str,
        firer_priv: Ed25519PrivateKey,
        reason: str,
    ) -> FireMessage:
        """Anyone fires the kill switch on `target_id`.

        Returns the FireMessage once the target is frozen.
        """
        firer_pub = firer_priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        ts = time.time_ns()
        body = _canonical(
            {
                "target": target_id,
                "firer": firer_pub.hex(),
                "reason": reason,
                "ts": ts,
            }
        )
        sig = firer_priv.sign(body)

        # Honest validator path: verify the signature, then freeze.
        Ed25519PublicKey.from_public_bytes(firer_pub).verify(sig, body)
        digest = hashlib.sha256(body + sig).digest()

        msg = FireMessage(
            target_id=target_id,
            fired_by_pub_hex=firer_pub.hex(),
            reason=reason,
            timestamp_ns=ts,
            signature_hex=sig.hex(),
            digest_hex=digest.hex(),
        )
        self.frozen[target_id] = msg
        return msg

    def is_frozen(self, target_id: str) -> bool:
        return target_id in self.frozen

    def authorize(self, target_id: str) -> bool:
        """Authorize a proposed action by `target_id`.

        Returns True iff the entity is NOT frozen. This is what every
        downstream protocol step calls; once frozen=True, every subsequent
        authorize() call returns False, which is the operational definition
        of "the entity is revoked".
        """
        return target_id not in self.frozen
