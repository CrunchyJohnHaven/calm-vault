#!/usr/bin/env python3
"""
BGP Bridge — wires the Bradley-Gavini Protocol (zk_alignment) into OBAC + AVS + HARP.

Import contract: `zk_alignment` may live either as a flat-file module
(`zk_alignment.py` next to this file) OR as a package directory
(`zk_alignment/zk_alignment.py`, with or without an `__init__.py` — Python 3
namespace packages cover the no-init case). This module tries both layouts and
exposes a stable set of symbols regardless of how the underlying file is shipped.

End-to-end flow (`request_access`):

    1. Two agents (subject + peer) each commit to their private maxim.
    2. Bridge runs the equality proof; AVS attests to the alignment fact.
    3. OBAC PolicyEngine decides whether the subject's oath covers the
       (action, resource) request.
    4. HARP logs the AVS attestation + OBAC decision into a tamper-evident
       chain; the returned BridgeResult carries everything needed for replay.
"""

from __future__ import annotations

import importlib
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


# ---------------------------------------------------------------------------
# zk_alignment import shim — accept BOTH flat-file and (namespace-)package layouts
# ---------------------------------------------------------------------------

_REQUIRED_SYMBOLS = (
    "Agent",
    "Commitment",
    "EqualityProof",
    "commit",
    "prove_equality",
    "verify_equality",
    "run_protocol",
)


def _load_zk_alignment() -> Any:
    """Resolve the zk_alignment module across layout variants.

    Try, in order:
      1. `import zk_alignment` — flat-file `zk_alignment.py` on sys.path.
      2. `import zk_alignment.zk_alignment` — package directory containing
         the implementation in `zk_alignment.py` (works for both regular
         packages with `__init__.py` and PEP-420 namespace packages).
      3. Filesystem fallback — locate `zk_alignment.py` near this file
         (siblings or one level down) and load it via `importlib.util`.
    """
    last_err: Optional[BaseException] = None

    # (1) flat-file or package whose top-level re-exports everything
    try:
        mod = importlib.import_module("zk_alignment")
        if all(hasattr(mod, name) for name in _REQUIRED_SYMBOLS):
            return mod
    except ImportError as exc:
        last_err = exc

    # (2) package directory: zk_alignment/zk_alignment.py
    try:
        mod = importlib.import_module("zk_alignment.zk_alignment")
        if all(hasattr(mod, name) for name in _REQUIRED_SYMBOLS):
            return mod
    except ImportError as exc:
        last_err = exc

    # (3) filesystem fallback — look next to this file
    here = Path(__file__).resolve().parent
    candidates = [
        here / "zk_alignment.py",
        here / "zk_alignment" / "zk_alignment.py",
        here.parent / "zk_alignment.py",
        here.parent / "zk_alignment" / "zk_alignment.py",
    ]
    for path in candidates:
        if not path.exists():
            continue
        spec = importlib.util.spec_from_file_location("zk_alignment", path)
        if spec is None or spec.loader is None:  # pragma: no cover - defensive
            continue
        mod = importlib.util.module_from_spec(spec)
        sys.modules.setdefault("zk_alignment", mod)
        spec.loader.exec_module(mod)
        if all(hasattr(mod, name) for name in _REQUIRED_SYMBOLS):
            return mod

    raise ImportError(
        "Could not locate zk_alignment. Tried flat-file import, package import "
        "(`zk_alignment.zk_alignment`), and filesystem fallback near "
        f"{Path(__file__).resolve().parent}. Last error: {last_err!r}"
    )


_zk = _load_zk_alignment()

# Re-export the surface so callers (incl. tests) can `from bgp_bridge import Agent, ...`.
Agent = _zk.Agent
Commitment = _zk.Commitment
EqualityProof = _zk.EqualityProof
commit = _zk.commit
prove_equality = _zk.prove_equality
verify_equality = _zk.verify_equality
run_protocol = _zk.run_protocol


# ---------------------------------------------------------------------------
# Bridge
# ---------------------------------------------------------------------------

from obac import Decision, Oath, PolicyEngine  # noqa: E402
from avs import AVS, AlignmentAttestation  # noqa: E402
from harp import HARPLog  # noqa: E402


@dataclass
class BridgeResult:
    allowed: bool
    decision: Decision
    attestation: AlignmentAttestation
    harp_entries: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "allowed": self.allowed,
            "decision": self.decision.to_dict(),
            "attestation": self.attestation.to_dict(),
            "harp_entries": [e.to_dict() for e in self.harp_entries],
        }


class BGPBridge:
    """Wires zk_alignment + AVS + OBAC + HARP into one end-to-end call."""

    def __init__(self, avs: AVS, policy_engine: PolicyEngine, harp: HARPLog) -> None:
        self.avs = avs
        self.policies = policy_engine
        self.harp = harp

    # --- per-agent helper ---

    @staticmethod
    def make_agent(name: str, maxim_text: str):
        """Construct a zk_alignment Agent and stage its commitment."""
        agent = Agent(name=name, maxim_text=maxim_text)
        agent.prepare()
        return agent

    # --- end-to-end request ---

    def request_access(
        self,
        subject_agent,
        peer_agent,
        subject_oath: Oath,
        action: str,
        resource: str,
    ) -> BridgeResult:
        # Stage both commitments if not already prepared.
        if subject_agent.commitment is None:
            subject_agent.prepare()
        if peer_agent.commitment is None:
            peer_agent.prepare()

        # Run equality proof (subject acts as prover; needs peer's randomness — in
        # the real wire protocol this is exchanged commit-then-reveal; here we run
        # everything locally for the bridge demo).
        proof = prove_equality(
            subject_agent.commitment,
            peer_agent.commitment,
            subject_agent._m,
            subject_agent._r,
            peer_agent._r,
        )
        attestation = self.avs.attest(
            subject_agent.commitment, peer_agent.commitment, proof,
        )
        att_entry = self.harp.append(
            "avs.attest",
            {
                "attestation_id": attestation.attestation_id,
                "aligned": attestation.aligned,
                "expires_at": attestation.expires_at,
            },
        )

        if not attestation.aligned:
            decision = Decision(
                decision_id=att_entry.payload["attestation_id"],
                allowed=False,
                reason="alignment proof rejected",
                agent_id=subject_oath.agent_id,
                action=action,
                resource=resource,
                ts=att_entry.ts,
                oath_id=subject_oath.oath_id,
            )
            dec_entry = self.harp.append(
                "obac.decision",
                {
                    "decision_id": decision.decision_id,
                    "allowed": False,
                    "reason": decision.reason,
                    "agent_id": decision.agent_id,
                    "action": action,
                    "resource": resource,
                },
            )
            return BridgeResult(
                allowed=False,
                decision=decision,
                attestation=attestation,
                harp_entries=[att_entry, dec_entry],
            )

        decision = self.policies.decide(subject_oath, action, resource)
        dec_entry = self.harp.append(
            "obac.decision",
            {
                "decision_id": decision.decision_id,
                "allowed": decision.allowed,
                "reason": decision.reason,
                "agent_id": decision.agent_id,
                "action": action,
                "resource": resource,
                "policy_id": decision.policy_id,
                "oath_id": decision.oath_id,
            },
        )
        return BridgeResult(
            allowed=decision.allowed,
            decision=decision,
            attestation=attestation,
            harp_entries=[att_entry, dec_entry],
        )


__all__ = [
    "Agent",
    "Commitment",
    "EqualityProof",
    "commit",
    "prove_equality",
    "verify_equality",
    "run_protocol",
    "BGPBridge",
    "BridgeResult",
]
