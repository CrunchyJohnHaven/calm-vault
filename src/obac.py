#!/usr/bin/env python3
"""
OBAC — Oath-Based Access Control.

A policy engine that gates access to credentials and capabilities on whether the
requesting agent holds a valid, unrevoked oath signed by a trusted oath
authority. The canonical oath text is the same one-sentence operating maxim used
by the Bradley-Gavini Protocol (see zk_alignment.py).

Design goals:
- Stateless, file-free core: every object is plain-Python; persistence is opt-in.
- Authority is an Ed25519 key. Oaths are sign(authority_key, canonical(maxim) || agent_id || issued_at).
- Decisions are deterministic and explainable: every Decision carries the
  policy id, oath id, action, resource, and a human-readable reason.
- The engine does not perform alignment proofs itself; callers wire in AVS
  (avs.py) for cross-agent alignment verification, and HARP (harp.py) to anchor
  the decision trail. The bridge module (bgp_bridge.py) wires all three.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


def _canon_maxim(text: str) -> bytes:
    import unicodedata
    return unicodedata.normalize("NFC", text.strip().lower()).encode("utf-8")


def _maxim_hash(text: str) -> str:
    return hashlib.sha256(_canon_maxim(text)).hexdigest()


# ---------------------------------------------------------------------------
# Oath authority
# ---------------------------------------------------------------------------


@dataclass
class Oath:
    """A signed assertion that `agent_id` has accepted the named maxim."""
    oath_id: str
    agent_id: str
    maxim_hash: str
    issued_at: int
    authority_pub: str  # hex
    signature: str  # hex

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(d: dict) -> "Oath":
        return Oath(**d)


class OathAuthority:
    """Issuer of oaths. Owns an Ed25519 keypair; signs (agent_id, maxim_hash)."""

    def __init__(self, private_key: Optional[Ed25519PrivateKey] = None):
        self._sk = private_key or Ed25519PrivateKey.generate()
        self._pk = self._sk.public_key()
        self.pub_hex = self._pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()

    @staticmethod
    def _payload(agent_id: str, maxim_hash: str, issued_at: int) -> bytes:
        return json.dumps(
            {"agent_id": agent_id, "maxim_hash": maxim_hash, "issued_at": issued_at},
            sort_keys=True,
        ).encode("utf-8")

    def issue(self, agent_id: str, maxim_text: str, issued_at: Optional[int] = None) -> Oath:
        if not agent_id:
            raise ValueError("agent_id required")
        if not maxim_text or not maxim_text.strip():
            raise ValueError("maxim_text required")
        mh = _maxim_hash(maxim_text)
        ts = int(issued_at if issued_at is not None else time.time())
        payload = self._payload(agent_id, mh, ts)
        sig = self._sk.sign(payload).hex()
        return Oath(
            oath_id=str(uuid.uuid4()),
            agent_id=agent_id,
            maxim_hash=mh,
            issued_at=ts,
            authority_pub=self.pub_hex,
            signature=sig,
        )


def verify_oath(oath: Oath, authority_pub_hex: Optional[str] = None) -> bool:
    """Verify the signature on an Oath. If authority_pub_hex is provided, it
    must match the oath's authority_pub (defends against substitution)."""
    if authority_pub_hex is not None and authority_pub_hex != oath.authority_pub:
        return False
    try:
        pk = Ed25519PublicKey.from_public_bytes(bytes.fromhex(oath.authority_pub))
    except Exception:
        return False
    payload = OathAuthority._payload(oath.agent_id, oath.maxim_hash, oath.issued_at)
    try:
        pk.verify(bytes.fromhex(oath.signature), payload)
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------


@dataclass
class Policy:
    """A rule: agents bearing an oath against `required_maxim_text` may take
    `action` on `resource`. action='*' or resource='*' acts as a wildcard."""
    policy_id: str
    resource: str
    action: str
    required_maxim_hash: str
    required_authority_pub: str

    @classmethod
    def for_maxim(
        cls,
        resource: str,
        action: str,
        maxim_text: str,
        authority_pub_hex: str,
        policy_id: Optional[str] = None,
    ) -> "Policy":
        return cls(
            policy_id=policy_id or str(uuid.uuid4()),
            resource=resource,
            action=action,
            required_maxim_hash=_maxim_hash(maxim_text),
            required_authority_pub=authority_pub_hex,
        )

    def matches(self, action: str, resource: str) -> bool:
        """Match the request's (action, resource) against this policy. Both
        fields support fnmatch-style globs (`*`, `?`). The bare `*` for either
        field acts as a wildcard for that dimension."""
        return fnmatch.fnmatchcase(action, self.action) and fnmatch.fnmatchcase(resource, self.resource)


@dataclass
class Decision:
    decision_id: str
    allowed: bool
    reason: str
    agent_id: str
    action: str
    resource: str
    ts: int
    policy_id: Optional[str] = None
    oath_id: Optional[str] = None
    extras: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)


class PolicyEngine:
    """Registry of policies + decide()."""

    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}
        self._revoked_oaths: set[str] = set()

    # --- registry ---

    def add_policy(self, policy: Policy) -> None:
        self._policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> None:
        self._policies.pop(policy_id, None)

    def list_policies(self) -> list[Policy]:
        return list(self._policies.values())

    def revoke_oath(self, oath_id: str) -> None:
        self._revoked_oaths.add(oath_id)

    def is_revoked(self, oath_id: str) -> bool:
        return oath_id in self._revoked_oaths

    # --- decision ---

    def decide(self, oath: Oath, action: str, resource: str) -> Decision:
        ts = int(time.time())
        dec_id = str(uuid.uuid4())
        # 1) signature
        if not verify_oath(oath):
            return Decision(
                decision_id=dec_id, allowed=False,
                reason="oath signature invalid",
                agent_id=oath.agent_id, action=action, resource=resource, ts=ts,
            )
        # 2) revocation
        if self.is_revoked(oath.oath_id):
            return Decision(
                decision_id=dec_id, allowed=False,
                reason="oath revoked",
                agent_id=oath.agent_id, action=action, resource=resource, ts=ts,
                oath_id=oath.oath_id,
            )
        # 3) matching policy
        candidates = [p for p in self._policies.values() if p.matches(action, resource)]
        if not candidates:
            return Decision(
                decision_id=dec_id, allowed=False,
                reason="no policy covers this (action, resource)",
                agent_id=oath.agent_id, action=action, resource=resource, ts=ts,
                oath_id=oath.oath_id,
            )
        # 4) oath must satisfy at least one candidate
        for p in candidates:
            if p.required_maxim_hash != oath.maxim_hash:
                continue
            if p.required_authority_pub != oath.authority_pub:
                continue
            return Decision(
                decision_id=dec_id, allowed=True,
                reason="oath matches policy",
                agent_id=oath.agent_id, action=action, resource=resource, ts=ts,
                policy_id=p.policy_id, oath_id=oath.oath_id,
            )
        return Decision(
            decision_id=dec_id, allowed=False,
            reason="oath does not satisfy any matching policy (maxim or authority mismatch)",
            agent_id=oath.agent_id, action=action, resource=resource, ts=ts,
            oath_id=oath.oath_id,
        )


__all__ = [
    "Oath",
    "OathAuthority",
    "verify_oath",
    "Policy",
    "Decision",
    "PolicyEngine",
]
