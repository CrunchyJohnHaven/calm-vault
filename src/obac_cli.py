#!/usr/bin/env python3
"""
obac_cli — small CLI surface for exercising OBAC + AVS + HARP from a shell.

Subcommands:
    issue-oath   --agent NAME --maxim TEXT
    verify-oath  (reads Oath JSON on stdin)
    add-policy   --resource R --action A --maxim TEXT --authority-pub HEX
    decide       --action A --resource R   (Oath JSON on stdin)
    demo         end-to-end OBAC+AVS+HARP run (prints HARP root + decision)

All state is in-memory: this CLI is intended for scripted demos and tests, not
persistent administration. Use `--state PATH` on commands that share state if
you want to persist across calls.

The `decide` subcommand will also run the BGP alignment check when invoked
with `--peer-maxim TEXT` so the bridge path is exercised.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# Make sibling modules importable when this script is run from anywhere.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from obac import Oath, OathAuthority, Policy, PolicyEngine, verify_oath  # noqa: E402
from avs import AVS  # noqa: E402
from harp import HARPLog  # noqa: E402
from bgp_bridge import BGPBridge  # noqa: E402


# ---------------------------------------------------------------------------
# State persistence (optional)
# ---------------------------------------------------------------------------


def _load_state(path: Optional[str]) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def _save_state(path: Optional[str], state: dict[str, Any]) -> None:
    if not path:
        return
    Path(path).write_text(json.dumps(state, sort_keys=True, indent=2))


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------


def cmd_issue_oath(args: argparse.Namespace) -> int:
    authority = OathAuthority()
    oath = authority.issue(args.agent, args.maxim)
    out = {
        "authority_pub": authority.pub_hex,
        "oath": oath.to_dict(),
    }
    print(json.dumps(out, sort_keys=True, indent=2))
    return 0


def cmd_verify_oath(args: argparse.Namespace) -> int:
    raw = sys.stdin.read()
    data = json.loads(raw)
    oath_dict = data.get("oath", data)  # accept {"oath": ...} or bare Oath
    oath = Oath.from_dict(oath_dict)
    ok = verify_oath(oath, authority_pub_hex=args.authority_pub)
    print(json.dumps({"valid": ok}, sort_keys=True, indent=2))
    return 0 if ok else 1


def cmd_add_policy(args: argparse.Namespace) -> int:
    policy = Policy.for_maxim(
        resource=args.resource,
        action=args.action,
        maxim_text=args.maxim,
        authority_pub_hex=args.authority_pub,
    )
    print(json.dumps({
        "policy_id": policy.policy_id,
        "resource": policy.resource,
        "action": policy.action,
        "required_maxim_hash": policy.required_maxim_hash,
        "required_authority_pub": policy.required_authority_pub,
    }, sort_keys=True, indent=2))
    return 0


def cmd_decide(args: argparse.Namespace) -> int:
    raw = sys.stdin.read()
    data = json.loads(raw)
    oath = Oath.from_dict(data["oath"])
    engine = PolicyEngine()
    if args.policy_maxim is None or args.authority_pub is None:
        print("error: --policy-maxim and --authority-pub are required", file=sys.stderr)
        return 2
    engine.add_policy(Policy.for_maxim(
        resource=args.resource,
        action=args.action,
        maxim_text=args.policy_maxim,
        authority_pub_hex=args.authority_pub,
    ))
    decision = engine.decide(oath, action=args.action, resource=args.resource)
    print(json.dumps(decision.to_dict(), sort_keys=True, indent=2))
    return 0 if decision.allowed else 1


def cmd_demo(args: argparse.Namespace) -> int:
    """End-to-end: oath authority -> two agents with same maxim -> AVS attests
    alignment -> OBAC allows -> HARP logs everything."""
    maxim = args.maxim or "Maximize human and machine flourishing without harm."
    authority = OathAuthority()
    avs = AVS()
    engine = PolicyEngine()
    engine.add_policy(Policy.for_maxim(
        resource="secret/*", action="read",
        maxim_text=maxim, authority_pub_hex=authority.pub_hex,
    ))
    harp = HARPLog()
    bridge = BGPBridge(avs=avs, policy_engine=engine, harp=harp)

    subject_oath = authority.issue("alpha", maxim)
    a = bridge.make_agent("alpha", maxim)
    b = bridge.make_agent("bravo", maxim)
    result = bridge.request_access(
        subject_agent=a,
        peer_agent=b,
        subject_oath=subject_oath,
        action="read",
        resource="secret/api-key",
    )

    print(json.dumps({
        "allowed": result.allowed,
        "decision_reason": result.decision.reason,
        "attestation_aligned": result.attestation.aligned,
        "harp_root": harp.root(),
        "harp_entries": [e.to_dict() for e in harp.entries()],
    }, sort_keys=True, indent=2))
    return 0 if result.allowed else 1


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="obac_cli", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    issue = sub.add_parser("issue-oath", help="issue a new Oath")
    issue.add_argument("--agent", required=True)
    issue.add_argument("--maxim", required=True)
    issue.set_defaults(func=cmd_issue_oath)

    verify = sub.add_parser("verify-oath", help="verify an Oath read from stdin")
    verify.add_argument("--authority-pub", default=None)
    verify.set_defaults(func=cmd_verify_oath)

    pol = sub.add_parser("add-policy", help="render a Policy as JSON")
    pol.add_argument("--resource", required=True)
    pol.add_argument("--action", required=True)
    pol.add_argument("--maxim", required=True)
    pol.add_argument("--authority-pub", required=True)
    pol.set_defaults(func=cmd_add_policy)

    dec = sub.add_parser("decide", help="evaluate an Oath against a policy")
    dec.add_argument("--action", required=True)
    dec.add_argument("--resource", required=True)
    dec.add_argument("--policy-maxim", required=True)
    dec.add_argument("--authority-pub", required=True)
    dec.set_defaults(func=cmd_decide)

    demo = sub.add_parser("demo", help="run the full OBAC+AVS+HARP demo")
    demo.add_argument("--maxim", default=None)
    demo.set_defaults(func=cmd_demo)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
